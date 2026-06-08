#!/usr/bin/env python3
"""MadStory LLM Router v2 — 多模型路由 + LLM 增强意图解析 + Workflow 模式集成
Harness Engineering 集成:
- PPAF 循环感知: 意图解析 = Perception 阶段
- Classify-and-Act 模式: 先分类意图类型，再路由到对应处理流程
- Tournament 模式: 创意探索模式的多方向生成+筛选
- 多意图拆分: 单次输入包含多个创作需求时自动拆分
"""

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
            "best_for": ["意图解析", "风格检测", "路由决策", "多意图拆分"],
        },
        PRO: {
            "label": "专业级 (Opus / GPT-4.5)",
            "cost_multiplier": 10,
            "best_for": ["复杂剧本解析", "创意生成", "Tournament 评分", "分镜优化"],
        },
        ULTRA: {
            "label": "旗舰级 (GPT-5 / Claude-Next)",
            "cost_multiplier": 25,
            "best_for": ["全链路创作", "批量剧本分析", "多轮迭代", "创意探索 Tournament"],
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
    """LLM 增强版 Agent v2 — 可选接入 OpenAI 兼容 API 提升意图解析准确率
    新增能力:
    - 多意图拆分 (Multi-Intent Splitting): 单次输入含多个创作需求时自动拆分
    - 语义解析增强 (Semantic Parsing): 更丰富的意图字段（类型/导演参照/反套路/视觉隐喻）
    - Classify-and-Act: 先分类意图类型，再路由到对应处理流程
    - Tournament 评分: 创意探索模式的多方向生成+两两比较筛选
    """

    def __init__(self, llm_client=None, api_key=None, base_url=None, model="gpt-4o"):
        super().__init__()
        self.llm_client = llm_client
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o")
        self.router = TaskRouter()

    # === 多意图拆分 ===

    def split_multi_intent(self, raw_input):
        """检测并拆分多意图输入（Classify-and-Act 模式的 Classify 阶段）

        Returns:
            list[dict]: 拆分后的意图列表，每个元素包含原始文本片段和建议的模式
        """
        # 快速规则检测（无需 LLM）
        separators = ["，然后", "另外", "还有", "同时", "以及", "再做一个", "还要", "；", "\n\n"]
        has_multiple = any(sep in raw_input for sep in separators)
        sentence_count = len([s for s in raw_input.split("。") if s.strip()])

        if not has_multiple and sentence_count <= 2:
            return [{"text": raw_input, "is_single": True}]

        # 使用 LLM 进行精确拆分
        if not self.api_key:
            # Fallback: 基于分隔符的简单拆分
            parts = []
            current = ""
            for sep in separators:
                if sep in raw_input:
                    parts = raw_input.split(sep)
                    break
            if not parts:
                parts = [raw_input]
            return [{"text": p.strip(), "is_single": len(parts) == 1} for p in parts if p.strip()]

        try:
            result = self._call_llm([
                {"role": "system", "content": self._multi_intent_system_prompt()},
                {"role": "user", "content": raw_input},
            ], max_tokens=500)
            parsed = json.loads(self._extract_json(result))
            intents = parsed.get("intents", [])
            if not intents:
                return [{"text": raw_input, "is_single": True}]
            for i, intent in enumerate(intents):
                intent["index"] = i
                intent["suggested_mode"] = self._classify_intent_type(intent.get("text", ""))
            return intents
        except Exception:
            return [{"text": raw_input, "is_single": True}]

    # === Workflow 模式集成 ===

    def tournament_select(self, candidates, criteria=None):
        """Tournament 模式：多候选方案两两比较 → 选出最优

        Args:
            candidates: list[str] 或 list[dict] — 候选方案列表
            criteria: list[str] — 评分维度（默认: 独特性、可行性、情感深度）

        Returns:
            dict: {winner_index, scores, comparison_log}
        """
        if not self.api_key or len(candidates) < 2:
            return {"winner_index": 0, "scores": [1.0] * len(candidates), "method": "fallback_first"}

        criteria = criteria or ["创意独特性", "视觉可实现性", "情感传达力", "叙事连贯性"]

        try:
            candidate_texts = []
            for c in candidates:
                if isinstance(c, dict):
                    candidate_texts.append(json.dumps(c, ensure_ascii=False))
                else:
                    candidate_texts.append(c)

            result = self._call_llm([
                {"role": "system", "content": self._tournament_system_prompt(criteria)},
                {"role": "user", "content": f"候选方案:\n" + "\n---\n".join(
                    f"[{i}] {t}" for i, t in enumerate(candidate_texts)
                )},
            ], max_tokens=800)
            parsed = json.loads(self._extract_json(result))
            return {
                "winner_index": parsed.get("winner", 0),
                "scores": parsed.get("scores", []),
                "comparison_log": parsed.get("log", ""),
                "criteria": criteria,
                "method": "llm_tournament",
            }
        except Exception:
            return {"winner_index": 0, "scores": [1.0] * len(candidates), "method": "fallback_error"}

    def classify_and_route(self, raw_input):
        """Classify-and-Act 模式: 先分类用户意图类型，再路由到对应处理策略

        Returns:
            dict: {intent_class, confidence, recommended_mode, processing_strategy, ...}
        """
        base_intent = self.parse_intent(raw_input, use_llm=bool(self.api_key))

        # 意图分类
        intent_classes = {
            "creative_exploration": ["概念", "灵感", "实验", "探索", "风格"],
            "product_commercial": ["产品", "商品", "卖货", "电商", "展示"],
            "narrative_storytelling": ["故事", "剧情", "叙事", "短剧", "剧本", "场景"],
            "viral_content": ["爆款", "复刻", "模仿", "抖音", "热门"],
            "character_driven": ["角色", "人物", "一致性", "主角", "演员"],
        }

        text_lower = raw_input.lower()
        scores = {}
        for cls, keywords in intent_classes.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[cls] = score

        best_class = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"

        # 路由决策
        route_map = {
            "creative_exploration": AdMode.CREATIVE_FILM,
            "product_commercial": AdMode.ECOMMERCE,
            "narrative_storytelling": AdMode.SHORT_DRAMA if base_intent.get("has_script") else AdMode.MULTI_SHOT,
            "viral_content": AdMode.VIRAL_REPLICATE,
            "character_driven": AdMode.CINEMATIC,
            "general": AdMode.AGENT_MODE,
        }

        base_intent["intent_class"] = best_class
        base_intent["intent_confidence"] = max(scores.values()) / 5.0
        base_intent["recommended_mode"] = route_map.get(best_class, AdMode.AGENT_MODE)
        base_intent["processing_strategy"] = self._get_strategy_for_class(best_class)

        return base_intent

    # === 原有方法增强 ===

    def parse_intent(self, raw_input, use_llm=False):
        if not use_llm or not self.api_key:
            return super().parse_intent(raw_input)

        route_info = self.router.route(raw_input, "intent_parsing")
        try:
            llm_output = self._call_llm([
                {"role": "system", "content": self._llm_system_prompt()},
                {"role": "user", "content": raw_input},
            ], max_tokens=400)
            parsed = json.loads(self._extract_json(llm_output))
            intent = super().parse_intent(raw_input)
            intent.update({
                k: v for k, v in parsed.items()
                if k in (
                    "detected_style", "detected_emotion", "detected_platform",
                    "suggested_duration", "detected_genre", "director_reference",
                    "visual_metaphor", "anti_cliche_directive", "narrative_structure"
                )
            })
            intent["_llm_enhanced"] = True
            intent["_llm_model"] = self.model
            intent["_route_tier"] = route_info["tier"]
            self.intent = intent
            return intent
        except Exception:
            return super().parse_intent(raw_input)

    # === 内部方法 ===

    def _call_llm(self, messages, max_tokens=300):
        """统一的 LLM 调用封装"""
        import urllib.request
        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": max_tokens,
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
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

    def _classify_intent_type(self, text):
        """快速意图分类（无需 LLM 的 fallback）"""
        for kw, mode in [
            ("概念", AdMode.CREATIVE_FILM), ("产品", AdMode.ECOMMERCE),
            ("卖货", AdMode.ECOMMERCE), ("剧本", AdMode.SHORT_DRAMA),
            ("场景", AdMode.MULTI_SHOT), ("爆款", AdMode.VIRAL_REPLICATE),
            ("一镜", AdMode.ONE_SHOT), ("复刻", AdMode.VIRAL_REPLICATE),
        ]:
            if kw in text:
                return mode
        return AdMode.AGENT_MODE

    def _get_strategy_for_class(self, intent_class):
        """根据意图类别返回处理策略"""
        strategies = {
            "creative_exploration": "tournament_generate_and_filter",
            "product_commercial": "standard_phased_derivation",
            "narrative_storytelling": "script_parsing_with_consistency",
            "viral_content": "reference_analysis_and_adaptation",
            "character_driven": "consistency_locked_production",
            "general": "agent_auto_detect",
        }
        return strategies.get(intent_class, "standard_phased_derivation")

    def _llm_system_prompt(self):
        return """你是 MadStory 电影级分镜引擎的意图解析模块 (v3)。分析用户输入，提取创作意图。

返回纯 JSON (无 markdown 包裹):
{
  "detected_style": "cinematic|anime|3d|guofeng|realistic|ugc|poetic|noir|fantasy|documentary",
  "detected_emotion": "emotional|passionate|humorous|suspense|warm|sad|epic|calm|neutral|melancholic|hopeful",
  "detected_platform": "douyin|tiktok|xiaohongshu|bilibili|youtube|wechat|unknown",
  "suggested_duration": 15-180,
  "has_script": true/false,
  "has_material": true/false,
  "detected_genre": "可选 — fantasy/thriller/drama/comedy/horror/romance/documentary/experimental",
  "director_reference": "可选 — 参考导演风格如 Tarkovsky/WongKarwai/Nolan/Malick",
  "anti_cliche_directive": true/false,
  "narrative_structure": "single_shot/multi_shot/circular/non_linear"
}"""

    def _multi_intent_system_prompt(self):
        return """分析用户输入是否包含多个独立的创作意图。如果有，请拆分。

返回纯 JSON:
{
  "has_multiple_intents": true/false,
  "intents": [
    {"text": "第一个意图的原文片段", "focus_brief": "一句话概括这个意图的核心"},
    ...
  ]
}

拆分原则:
- 每个意图应该可以独立成为一个完整的视频项目
- 如果多个意图之间有依赖关系（如"先做A，再做B风格的版本"），仍应拆分但标注依赖
- 保留原文的关键描述词，不要概括过度"""

    def _tournament_system_prompt(self, criteria):
        return f"""你是一个电影级创意评审专家。对以下候选方案进行 Tournament 两两比较评分。

评分维度 ({', '.join(criteria)}):
- 每个维度 1-10 分
- 最终得分 = 各维度加权平均（权重相等）

返回纯 JSON:
{
  "winner": 0,
  "scores": [8.5, 7.2, ...],
  "log": "简述选择理由，突出胜出方案的独特优势"
}

评审原则:
- 优先选择有独特视角而非技术堆砌的方案
- 情感深度 > 视觉炫技
- 叙事连贯性 > 创意碎片化"""

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
