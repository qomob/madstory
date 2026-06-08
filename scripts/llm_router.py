#!/usr/bin/env python3
"""MadStory LLM Router — 多模型路由 + LLM 增强意图解析"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mad_story_engine import AdMode, AgentModeEngine


class ModelTier:
    """模型层级定义 — 按任务复杂度分级"""
    LITE = "lite"
    STANDARD = "standard"
    PRO = "pro"
    ULTRA = "ultra"

    TIERS = {
        LITE: {
            "label": "轻量级 (Haiku / GPT-4o-mini)",
            "cost_multiplier": 1,
            "best_for": ["关键词提取", "简单分类", "格式校验"],
        },
        STANDARD: {
            "label": "标准级 (Sonnet / GPT-4o)",
            "cost_multiplier": 3,
            "best_for": ["意图解析", "风格检测", "路由决策"],
        },
        PRO: {
            "label": "专业级 (Opus / GPT-4.5)",
            "cost_multiplier": 10,
            "best_for": ["复杂剧本解析", "创意生成", "分镜优化"],
        },
        ULTRA: {
            "label": "旗舰级 (GPT-5 / Claude-Next)",
            "cost_multiplier": 25,
            "best_for": ["全链路创作", "批量剧本分析", "多轮迭代"],
        },
    }


class TaskRouter:
    """任务复杂度评估 → 模型层级推荐 → Token 成本预估"""

    def __init__(self, llm_client=None, api_key=None, base_url=None):
        self.llm_client = llm_client
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL", "")
        self.usage_stats = {"total_tasks": 0, "total_estimated_tokens": 0, "by_tier": {}}

    def estimate_complexity(self, user_input, task_type="intent_parsing"):
        """基于规则 + 可选 LLM 增强的复杂度评估"""
        input_len = len(user_input)
        has_multi_intent = len(user_input.split("。")) > 2 or len(user_input.split("\n")) > 5
        has_script = any(kw in user_input for kw in ["集", "场景:", "人物:", "△", "分镜"])

        if task_type == "script_parsing":
            complexity = 0
            complexity += min(input_len / 100, 5)
            complexity += 5 if "人物:" in user_input else 0
            complexity += 5 if "场景:" in user_input else 0
            complexity += 3 if "\n" in user_input and len(user_input.split("\n")) > 10 else 0

            if complexity >= 12:
                return ModelTier.ULTRA
            if complexity >= 8:
                return ModelTier.PRO
            if complexity >= 4:
                return ModelTier.STANDARD
            return ModelTier.LITE

        if task_type == "intent_parsing":
            if has_script:
                return ModelTier.PRO if input_len > 500 else ModelTier.STANDARD
            if has_multi_intent:
                return ModelTier.STANDARD
            if input_len > 200:
                return ModelTier.STANDARD
            return ModelTier.LITE

        if task_type == "creative_generation":
            if has_script or input_len > 300:
                return ModelTier.PRO
            return ModelTier.STANDARD

        return ModelTier.STANDARD

    def estimate_tokens(self, user_input, tier):
        multipliers = {ModelTier.LITE: 1.0, ModelTier.STANDARD: 3.0, ModelTier.PRO: 10.0, ModelTier.ULTRA: 25.0}
        base_tokens = len(user_input) * 0.6 + 500
        return int(base_tokens * multipliers.get(tier, 1.0))

    def estimate_cost(self, user_input, tier, price_per_1m_input=3.0, price_per_1m_output=15.0):
        in_tokens = self.estimate_tokens(user_input, tier)
        out_tokens = min(in_tokens * 0.3, 4000)
        cost = (in_tokens / 1_000_000) * price_per_1m_input + (out_tokens / 1_000_000) * price_per_1m_output
        return {"input_tokens": int(in_tokens), "output_tokens": int(out_tokens), "estimated_cost_usd": round(cost, 4)}

    def route(self, user_input, task_type="intent_parsing"):
        tier = self.estimate_complexity(user_input, task_type)
        cost = self.estimate_cost(user_input, tier)
        self.usage_stats["total_tasks"] += 1
        self.usage_stats["total_estimated_tokens"] += cost["input_tokens"]
        self.usage_stats["by_tier"][tier] = self.usage_stats["by_tier"].get(tier, 0) + 1
        return {
            "tier": tier,
            "tier_label": ModelTier.TIERS[tier]["label"],
            "cost_multiplier": ModelTier.TIERS[tier]["cost_multiplier"],
            "estimated_cost": cost,
            "saved_vs_ultra": round(
                self.estimate_cost(user_input, ModelTier.ULTRA)["estimated_cost_usd"] - cost["estimated_cost_usd"], 4
            ),
        }


class LLMEnhancedAgent(AgentModeEngine):
    """LLM 增强版 Agent — 可选接入 OpenAI 兼容 API 提升意图解析准确率"""

    def __init__(self, llm_client=None, api_key=None, base_url=None, model="gpt-4o"):
        super().__init__()
        self.llm_client = llm_client
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o")
        self.router = TaskRouter()

    def parse_intent(self, raw_input, use_llm=False):
        if not use_llm or not self.api_key:
            return super().parse_intent(raw_input)

        route_info = self.router.route(raw_input, "intent_parsing")
        try:
            import urllib.request
            body = json.dumps({
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._llm_system_prompt()},
                    {"role": "user", "content": raw_input},
                ],
                "temperature": 0.1,
                "max_tokens": 300,
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url.rstrip('/')}/chat/completions",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            llm_output = data["choices"][0]["message"]["content"]
            parsed = json.loads(self._extract_json(llm_output))
            intent = super().parse_intent(raw_input)
            intent.update({
                k: v for k, v in parsed.items()
                if k in ("detected_style", "detected_emotion", "detected_platform", "suggested_duration")
            })
            intent["_llm_enhanced"] = True
            intent["_llm_model"] = self.model
            intent["_route_tier"] = route_info["tier"]
            self.intent = intent
            return intent
        except Exception:
            return super().parse_intent(raw_input)

    def _llm_system_prompt(self):
        return """你是 MadStory 影视分镜引擎的意图解析模块。分析用户输入，提取创作意图。

返回纯 JSON (无 markdown 包裹):
{
  "detected_style": "cinematic|anime|3d|guofeng|realistic|ugc",
  "detected_emotion": "emotional|passionate|humorous|suspense|warm|sad|epic|calm|neutral",
  "detected_platform": "douyin|tiktok|xiaohongshu|bilibili|youtube|wechat|unknown",
  "suggested_duration": 15-180,
  "has_script": true/false,
  "has_material": true/false
}"""

    def _extract_json(self, text):
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        return text.strip()


if __name__ == "__main__":
    print("=" * 60)
    print("MadStory LLM Router — 多模型路由演示")
    print("=" * 60)

    router = TaskRouter()

    test_cases = [
        ("帮我做一个护肤品的种草视频", "intent_parsing"),
        ("做一个电影感赛博朋克短片，要有霓虹灯光", "intent_parsing"),
        ("第1集\n场景: 灵霄宗外门 清晨\n人物: 江晏, 长老\n△ 江晏在山门前练剑\n江晏: 今日必突破筑基！\n长老 (OS): 此子天赋异禀。", "script_parsing"),
        ("分析这个爆款视频的节奏和文案结构，重新创作一个类似的", "creative_generation"),
    ]

    for user_input, task_type in test_cases:
        result = router.route(user_input, task_type)
        print(f"\n任务: {task_type}")
        print(f"输入: {user_input[:60]}...")
        print(f"路由: {result['tier_label']}")
        print(f"预估成本: ${result['estimated_cost']['estimated_cost_usd']}")
        print(f"比旗舰级节省: ${result['saved_vs_ultra']}")

    print(f"\n统计: {router.usage_stats}")

    print("\n" + "=" * 60)
    print("LLM 增强 Agent 演示 (keyword fallback)")
    agent = LLMEnhancedAgent()
    intent = agent.parse_intent("帮我做一个1分钟的3D动画短片，要热血感人风格，发布到B站")
    print(f"风格: {intent.get('detected_style')}")
    print(f"情绪: {intent.get('detected_emotion')}")
    print(f"平台: {intent.get('detected_platform')}")
    print(f"时长: {intent.get('suggested_duration')}s")
    print(f"LLM 增强: {intent.get('_llm_enhanced', False)}")
