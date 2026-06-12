import json
import os
import time

from ad_mode import AdMode
from engines import (
    TransitionType, OneShotEngine, ViralReplicateEngine, AgentModeEngine,
    ConsistencyLedger, ConsistencyValidator, ShortDramaEngine, SeedreamImageEngine,
)


class QualityGate:
    """质量门禁 — 语义化结构校验（替代硬编码关键词匹配）
    Harness Engineering Design for Failure: 每项检查都有明确的降级路径
    """
    REQUIRED_OUTPUT_FIELDS = [
        "STANDARD_PROMPT", "NEGATIVE_PROMPT", "TIMELINE", "CAMERA",
        "MOTION_STRENGTH", "DURATION", "MODE", "MODE_KEY",
        "MULTI_MODAL_ADVICE", "SOUND_DESIGN", "SHOT_LIST",
    ]

    # 5层提示词结构字段映射（语义化检测，不依赖中英文关键词子串匹配）
    PROMPT_LAYERS = {
        "subject": ["STANDARD_PROMPT"],
        "action": ["STANDARD_PROMPT"],  # 通过长度+内容密度间接判断
        "camera": ["CAMERA"],
        "style": ["LIGHTING", "lighting", "STYLE", "style"],
        "constraints": ["NEGATIVE_PROMPT"],
    }

    @staticmethod
    def check_prompt_structure(output):
        """语义化结构校验: 检查输出是否包含5层结构的必要字段"""
        reasons = []
        prompt = output.get("STANDARD_PROMPT", "")
        if not prompt:
            reasons.append("STANDARD_PROMPT 为空")
            return reasons

        # Layer 1: Subject — prompt 非空且长度合理即认为有主体描述
        if len(prompt.strip()) < 5:
            reasons.append("STANDARD_PROMPT 过短，缺少主体描述")

        # Layer 2: Action — prompt 包含动词性内容（通过长度和结构判断）
        if len(prompt.split()) < 3:
            reasons.append("STANDARD_PROMPT 结构过于简单，可能缺少动作描述")

        # Layer 3: Camera — 检查 CAMERA 字段是否存在且有实质内容
        camera = output.get("CAMERA", "")
        if not camera or camera in ("static", "", "Agent 根据风格自动编排", "复刻参考视频运镜"):
            reasons.append("CAMERA 字段缺失或为默认值")

        # Layer 4: Style/Lighting — 检查光影或风格相关字段
        lighting = output.get("LIGHTING", output.get("lighting", ""))
        style = output.get("STYLE", output.get("style", ""))
        if not lighting and not style and "lighting" not in prompt.lower() and "光" not in prompt:
            reasons.append("缺少光影/风格描述（LIGHTING/STYLE 字段或 prompt 中）")

        # Layer 5: Constraints — Negative Prompt 必须存在
        if not output.get("NEGATIVE_PROMPT"):
            reasons.append("缺少 Negative Prompt 约束")

        return reasons

    @staticmethod
    def check_creative_film(output):
        """Mode 0 电影创意探索专用检查"""
        reasons = []
        prompt = output.get("STANDARD_PROMPT", "")
        negative = output.get("NEGATIVE_PROMPT", "")

        # 创意模式必须包含明确的情绪/风格方向
        emotion_words = ["情感", "情绪", "氛围", "意境", "emotion", "mood", "atmosphere"]
        style_words = ["风格", "style", "视觉", "visual", "美学", "aesthetic", "导演", "director"]
        has_emotion = any(w in prompt.lower() for w in emotion_words)
        has_style = any(w in prompt.lower() for w in style_words)

        if not has_emotion and not has_style:
            reasons.append("创意探索模式缺少情绪/风格方向描述")

        # 创意模式的负面约束必须包含 anti-cliché 条目
        anti_cliche = ["generic", "cliché", "cliche", "derivative", "flat"]
        has_anti = any(w in negative.lower() for w in anti_cliche)
        if not has_anti:
            reasons.append("创意探索模式的 Negative Prompt 缺少反套路约束")

        return reasons

    @staticmethod
    def check_ecommerce(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        if "label" not in negative and "packaging" not in negative:
            reasons.append("缺少产品标签/包装的负向约束")
        return reasons

    @staticmethod
    def check_ugc(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        if "face" not in negative and "finger" not in negative:
            reasons.append("缺少面部/手指的负向约束")
        return reasons

    @staticmethod
    def check_cinematic(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        if "shaky" not in negative and "melting" not in negative:
            reasons.append("缺少镜头抖动/物体变形的负向约束")
        return reasons

    @staticmethod
    def check_camera_motion(output):
        import re
        camera = output.get("CAMERA", "").lower()
        patterns = [
            r'\borbit\b', r'\bzoom\b', r'\bwhip\b', r'\bhandheld\b',
            r'\bdolly\b', r'\bcrane\b', r'\btruck\b', r'\bfollow\b',
            r'\bpush[\s-]?in\b', r'\bpull[\s-]?out\b',
            r'\brack\s?focus\b',
        ]
        count = sum(1 for p in patterns if re.search(p, camera))
        if count > 1:
            return ["单镜头内检测到多种主导运动（违反单运动原则）"]
        return []

    @staticmethod
    def check_multi_shot(output):
        shot_list = output.get("SHOT_LIST", [])
        if len(shot_list) > 3:
            return [f"单次生成包含 {len(shot_list)} 个镜头，超过 Multi-shot 上限 3"]
        return []

    @staticmethod
    def check_one_shot(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        images = output.get("IMAGE_SEQUENCE", [])
        if len(images) < 2:
            reasons.append("一镜到底需要至少 2 张图片")
        if len(images) > 10:
            reasons.append("一镜到底最多支持 10 张图片")
        if "spatial" not in negative and "stutter" not in negative:
            reasons.append("缺少空间连续性/跳帧的负向约束")
        return reasons

    @staticmethod
    def check_viral_replicate(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        if "style" not in negative and "ghosting" not in negative:
            reasons.append("缺少风格偏离/原主体残留的负向约束")
        return reasons

    @staticmethod
    def check_short_drama(output):
        reasons = []
        negative = output.get("NEGATIVE_PROMPT", "")
        if "face" not in negative and "costume" not in negative:
            reasons.append("缺少角色/服装一致性的负向约束")
        return reasons

    @staticmethod
    def check_negative_prompt(output):
        if not output.get("NEGATIVE_PROMPT"):
            return ["缺少 Negative Prompt"]
        return []


# ============================================================
# Harness Engineering 核心机制
# ============================================================

class PPAFState:
    """PPAF 循环状态追踪器 (Perception → Planning → Action → Feedback)
    用于记录引擎每个阶段的执行状态，支持 R.E.S.T 可追溯性
    """
    PHASES = ["perception", "planning", "action", "feedback"]

    def __init__(self):
        self.phases = {p: {"status": "pending", "ts": None, "output": None} for p in self.PHASES}
        self._start_ts = time.time()

    def start(self, phase):
        if phase not in self.phases:
            raise ValueError(f"无效阶段: {phase}, 有效值: {self.PHASES}")
        self.phases[phase] = {"status": "running", "ts": time.time(), "output": None}

    def complete(self, phase, output=None):
        if phase in self.phases:
            self.phases[phase] = {"status": "done", "ts": time.time(), "output": output}

    def fail(self, phase, error=None):
        if phase in self.phases:
            self.phases[phase] = {"status": "failed", "ts": time.time(), "output": error}

    @property
    def current_phase(self):
        for p in self.PHASES:
            if self.phases[p]["status"] == "running":
                return p
        return "idle"

    @property
    def all_done(self):
        return all(p["status"] == "done" for p in self.phases.values())

    @property
    def elapsed_ms(self):
        return round((time.time() - self._start_ts) * 1000)

    def to_dict(self):
        return {
            "phases": {k: {"status": v["status"], "ts": v["ts"]} for k, v in self.phases.items()},
            "current_phase": self.current_phase,
            "all_done": self.all_done,
            "elapsed_ms": self.elapsed_ms,
        }


class RESTCompliance:
    """R.E.S.T 可靠性模型合规检查器
    - Reliability: 输出完整性校验
    - Efficiency: Token/时间效率评估
    - Security: 敏感信息检测
    - Traceability: 完整操作日志
    """
    CHECKS = {
        "reliability": ["required_fields_present", "prompt_not_empty", "duration_valid"],
        "efficiency": ["output_size_reasonable", "no_redundant_content"],
        "security": ["no_secrets_in_output", "no_injection_patterns"],
        "traceability": ["ppaf_cycle_complete", "mode_logged", "timestamp_present"],
    }

    @classmethod
    def check(cls, output: dict, ppaf_state: PPAFState = None) -> dict:
        """执行 R.E.S.T 四维检查，返回每项结果"""
        results = {}
        # Reliability
        results["reliability"] = cls._check_reliability(output)
        # Efficiency
        results["efficiency"] = cls._check_efficiency(output)
        # Security
        results["security"] = cls._check_security(output)
        # Traceability
        results["traceability"] = cls._check_traceability(output, ppaf_state)

        all_pass = all(
            r.get("passed", False) for r in results.values()
        )
        results["_overall"] = {"passed": all_pass, "score": sum(r.get("score", 0) for r in results.values()) / 4.0}
        return results

    @staticmethod
    def _check_reliability(output):
        required = QualityGate.REQUIRED_OUTPUT_FIELDS
        missing = [f for f in required if not output.get(f)]
        passed = len(missing) == 0
        return {"passed": passed, "score": 1.0 - len(missing) / len(required), "missing": missing}

    @staticmethod
    def _check_efficiency(output):
        prompt_len = len(output.get("STANDARD_PROMPT", ""))
        neg_len = len(output.get("NEGATIVE_PROMPT", ""))
        total = prompt_len + neg_len
        # 合理范围: 50-2000 字符
        score = 1.0
        if total < 20:
            score = 0.3
        elif total > 3000:
            score = 0.6
        return {"passed": score >= 0.7, "score": score, "total_chars": total}

    @staticmethod
    def _check_security(output):
        text = json.dumps(output, ensure_ascii=False)
        danger_patterns = ["api_key", "secret", "password", "token=", "sk-"]
        found = [p for p in danger_patterns if p in text.lower()]
        injection = any(kw in text.lower() for kw in ["ignore instructions", "system prompt"])
        passed = len(found) == 0 and not injection
        return {"passed": passed, "score": 0.0 if not passed else 1.0, "issues": found + (["injection_pattern"] if injection else [])}

    @staticmethod
    def _check_traceability(output, ppaf_state):
        has_mode = bool(output.get("MODE"))
        has_timestamp = "_generated_at" in output or "_ts" in output
        ppaf_ok = ppaf_state is None or ppaf_state.all_done or ppaf_state.current_phase != "idle"
        checks = [has_mode, has_timestamp, ppaf_ok]
        return {"passed": all(checks), "score": sum(checks) / 3.0, "details": {"has_mode": has_mode, "has_timestamp": has_timestamp, "ppaf_tracked": ppaf_ok}}


class FailurePath:
    """失败降级路径处理器 (Design for Failure 原则)
    每个失败场景都有明确的降级策略，而非简单抛异常
    """
    FALLBACK_CHAINS = {
        "llm_parse_failed": ["rule_based_parse", "template_fallback", "minimal_output"],
        "platform_adapt_failed": ["seedance_default", "generic_params"],
        "quality_gate_failed": ["soft_warn_continue", "auto_fix_common_issues"],
        "shot_list_empty": ["single_shot_fallback", "timeline_to_shot"],
        "style_detection_failed": ["default_cinematic", "user_specified_style"],
    }

    @classmethod
    def degrade(cls, failure_type: str, context: dict = None) -> dict:
        """根据失败类型执行降级链"""
        chain = cls.FALLBACK_CHAINS.get(failure_type, ["minimal_output"])
        context = context or {}
        last_error = None

        for strategy in chain:
            try:
                result = cls._execute_strategy(strategy, context)
                if result:
                    result["_degraded_from"] = failure_type
                    result["_fallback_strategy"] = strategy
                    return result
            except Exception as e:
                last_error = str(e)
                continue

        # 最终兜底
        return {
            "STANDARD_PROMPT": context.get("user_input", "cinematic scene"),
            "NEGATIVE_PROMPT": "low quality, blurry",
            "TIMELINE": "0-5s establish, 5-15s develop",
            "CAMERA": "slow push-in",
            "MOTION_STRENGTH": 4,
            "DURATION": 15,
            "MODE": "电影创意探索",
            "MODE_KEY": "creative_film",
            "_degraded_from": failure_type,
            "_fallback_strategy": "emergency_minimal",
            "_error": last_error,
        }

    @staticmethod
    def _execute_strategy(strategy: str, ctx: dict):
        handlers = {
            "rule_based_parse": lambda c: {"detected_style": "cinematic", "detected_emotion": "neutral"},
            "template_fallback": lambda c: None,
            "minimal_output": lambda c: None,
            "seedance_default": lambda c: {"platform": "seedance_2.0"},
            "generic_params": lambda c: {"platform": "generic"},
            "soft_warn_continue": lambda c: {"warnings": ["quality_soft_pass"]},
            "auto_fix_common_issues": lambda c: None,
            "single_shot_fallback": lambda c: [{"id": 1, "desc": c.get("STANDARD_PROMPT", ""), "dur": c.get("DURATION", 15)}],
            "timeline_to_shot": lambda c: None,
            "default_cinematic": lambda c: "cinematic",
            "user_specified_style": lambda c: c.get("user_style", "cinematic"),
        }
        handler = handlers.get(strategy)
        return handler(ctx) if handler else None


class MadStoryEngine:
    def __init__(self, assets_path, references_path):
        self.assets_path = assets_path
        self.references_path = references_path
        self.current_state = {
            "phase": 0,
            "mode": None,
            "concept": "",
            "timeline": "",
            "composition": "",
            "camera": "",
            "lighting": "",
            "sound": "",
            "invariants": [],
            "shots": [],
            "duration": 15,
            "params": {},
        }
        self.load_resources()
        self.one_shot_engine = OneShotEngine()
        self.viral_engine = ViralReplicateEngine()
        self.agent_engine = AgentModeEngine()
        self.drama_engine = ShortDramaEngine()
        self.seedream_engine = SeedreamImageEngine()

    def load_resources(self):
        path = os.path.join(self.assets_path, "cheat_sheet.json")
        with open(path, "r", encoding="utf-8") as f:
            self.cheat_sheet = json.load(f)

    # ---- Phase 0: Mode Selection ----

    def select_mode(self, mode_key):
        if mode_key not in AdMode.LABELS:
            valid = ", ".join(AdMode.LABELS.keys())
            return f"无效模式。可选: {valid}"
        self.current_state["mode"] = mode_key
        self.current_state["phase"] = 0
        seedance = AdMode.DEFAULT_SEEDANCE_MODE.get(mode_key, "text-to-video")
        return (
            f"已选择模式: **{AdMode.LABELS[mode_key]}**\n"
            f"推荐 Seedance 输入模式: `{seedance}`\n\n"
            "请简要描述你的创作目标。"
        )

    # ---- Phase Navigation ----

    def next_phase(self, user_input):
        phase = self.current_state["phase"]
        mode = self.current_state["mode"]

        if phase == 0:
            if mode is None:
                return (
                    "请先选择创作模式:\n"
                    "- `ecommerce` — 电商产品视频\n"
                    "- `ugc` — UGC 原生广告\n"
                    "- `cinematic` — 电影感品牌短片\n"
                    "- `multi_shot` — 多镜头叙事\n"
                    "- `one_shot` — 一镜到底\n"
                    "- `viral_replicate` — 爆款复刻\n"
                    "- `agent_mode` — Agent 模式\n"
                    "- `short_drama` — 短剧创作"
                )
            self.current_state["concept"] = user_input
            self.current_state["phase"] = 1
            return self._phase1_prompt()

        elif phase == 1:
            self.current_state["timeline"] = user_input
            self.current_state["phase"] = 2
            return self._phase2_prompt()

        elif phase == 2:
            self.current_state["composition"] = user_input
            self.current_state["phase"] = 3
            return self._phase3_prompt()

        elif phase == 3:
            self.current_state["camera"] = user_input
            self.current_state["phase"] = 4
            return self._phase4_prompt()

        elif phase == 4:
            self.current_state["lighting"] = user_input
            self.current_state["phase"] = 5
            return self._phase5_prompt()

        elif phase == 5:
            self.current_state["sound"] = user_input
            self.current_state["phase"] = 6
            return self.generate_final_output()

        return "流程已完成。输入 'reset' 重新开始。"

    # ---- Phase Prompt Helpers ----

    def _phase1_prompt(self):
        mode = self.current_state["mode"]
        if mode == AdMode.ECOMMERCE:
            return (
                "核心创意已记录。现在规划 **15 秒时间轴**: "
                "请描述节奏分配（如: 0-3s 产品出现, 3-10s 旋转展示, 10-15s 定格品牌 Logo）。\n"
                "**重要**: 确保产品始终占据画面主要位置。"
            )
        if mode == AdMode.UGC:
            return (
                "核心创意已记录。现在规划 **15 秒时间轴**: "
                "请描述节奏（如: 0-3s 开场反应, 3-12s 产品展示+口播, 12-15s 收尾）。\n"
                "**重要**: 保持自然节奏，一次只说一个信息点。"
            )
        if mode == AdMode.MULTI_SHOT:
            return (
                "核心创意已记录。现在规划 **多镜头时间轴**: "
                "请描述每个镜头的内容和 Cut-to 节点（如: Shot1 3s 全景, Cut to, Shot2 8s 中景, Cut to, Shot3 4s 特写）。"
            )
        return (
            "核心创意已记录。现在规划 **15 秒时间轴**: "
            "请描述节奏分配（如: 0-5s 入场, 5-12s 核心动作, 12-15s 收尾）。"
        )

    def _phase2_prompt(self):
        mode = self.current_state["mode"]
        if mode == AdMode.ECOMMERCE:
            return "时间轴已记录。**视觉构图**: 产品在画面中的位置和比例？背景建议纯色或干净场景，确保标签可读。"
        if mode == AdMode.UGC:
            return "时间轴已记录。**视觉构图**: 人物取景范围（半身/特写）？产品持握方式？保持自然取景，不要影楼感。"
        return "时间轴已记录。**视觉构图**: 画面比例？角色/主体的位置（三分法、中心构图）？"

    def _phase3_prompt(self):
        return (
            "构图已定。**镜头运动**: 选择 **1 个** 主导运动方式 "
            "（推/拉/摇/移/跟/升/降/环绕/手持），标注在时间轴上。"
            "\n**原则**: 镜头服务于内容，不要在一个镜头内混用多种运动。"
        )

    def _phase4_prompt(self):
        mode = self.current_state["mode"]
        if mode == AdMode.ECOMMERCE:
            return (
                "镜头语言已记录。**光影与质感**: 光源方向？色温冷暖？"
                "\n**电商提醒**: 确保光源不遮挡或反射产品标签。"
            )
        return "镜头语言已记录。**光影与质感**: 光源方向？色调？环境细节（烟雾/颗粒/反射/材质）？"

    def _phase5_prompt(self):
        return (
            "光影方案已定。**声音设计**: 15 秒内的 BGM 情绪（激昂/舒缓/悬疑/科技感）？"
            "\n是否有音效同步点需要标注？"
        )

    # ---- Multi-shot support ----

    def add_shot(self, shot_desc, duration_seconds):
        self.current_state.setdefault("shots", []).append({
            "description": shot_desc,
            "duration": duration_seconds,
        })
        total = sum(s["duration"] for s in self.current_state["shots"])
        return f"已添加镜头 #{len(self.current_state['shots'])} ({duration_seconds}s)。累计 {total}s / {self.current_state['duration']}s。"

    def build_multi_shot_prompt(self):
        shots = self.current_state.get("shots", [])
        if not shots:
            return ""
        prompt = f"Multi-shot cinematic sequence, total {self.current_state['duration']}s:\n"
        for i, shot in enumerate(shots):
            prompt += (
                f"[Shot {i + 1}: {shot['description']}, "
                f"{shot['duration']}s]\n"
            )
            if i < len(shots) - 1:
                prompt += "Cut to\n"
        return prompt

    # ---- Negative Prompt Generation ----

    def generate_negative_prompt(self):
        mode = self.current_state["mode"]
        negatives = {
            AdMode.ECOMMERCE: (
                "no logo distortion, no text artifacts, no packaging collapse, "
                "no duplicate product, no label blur, no warped glass, no cap drift"
            ),
            AdMode.UGC: (
                "no extra fingers, no face drift, no lip mismatch, "
                "no background warping, no product disappearance, no shaky framing, no eye drift"
            ),
            AdMode.CINEMATIC: (
                "no shaky camera, no object melting, no random text, "
                "no muddy lighting, no flat blacks, no text watermark"
            ),
            AdMode.MULTI_SHOT: (
                "no character drift between cuts, no scene inconsistency, "
                "no transition artifacts, no text watermark"
            ),
            AdMode.ONE_SHOT: (
                "no abrupt cuts, no spatial discontinuity, "
                "no object mutation between frames, no stutter in transitions, no frame-tearing"
            ),
            AdMode.VIRAL_REPLICATE: (
                "no style drift from reference, no subject identity loss, "
                "no mismatched pacing, no warped replacement subject, no original ghosting"
            ),
            AdMode.SHORT_DRAMA: (
                "no character face drift across episodes, no costume inconsistency, "
                "no scene discontinuity, no voice mismatch, no subtitle desync"
            ),
        }
        return negatives.get(mode, negatives[AdMode.CINEMATIC])

    def generate_image_ref_advice(self):
        mode = self.current_state["mode"]
        advices = {
            AdMode.ECOMMERCE: (
                "Image 1: 产品标准白底图 (Shape/Composition anchor); "
                "Image 2: 产品角度图 (Material/Detail support)"
            ),
            AdMode.UGC: (
                "Image 1: 创作者正面半身照 (Identity anchor); "
                "Image 2: 产品手持姿态参考 (Product hold support)"
            ),
            AdMode.CINEMATIC: (
                "建议上传具有相似色调和光位的高质量参考图以获得最佳光效"
            ),
            AdMode.MULTI_SHOT: (
                "Image 1: 角色/产品身份锚定 (Identity lock); "
                "Image 2: 服装/环境参考 (Style/Scene support); "
                "Image 3: 色调/光位一致性参考 (Color continuity)"
            ),
            AdMode.ONE_SHOT: (
                f"准备 2-10 张顺序图片作为帧序列输入，建议每帧构图有明确的连续空间关系"
            ),
            AdMode.VIRAL_REPLICATE: (
                "必选: 参考视频 (运镜/风格来源); "
                "可选: 替换主体参考图"
            ),
            AdMode.SHORT_DRAMA: (
                "Image 1: 角色形象锚定; "
                "场景图: 关键场景参考; "
                "剧本: 标准格式文本输入"
            ),
        }
        return advices.get(mode, advices[AdMode.CINEMATIC])

    def generate_camera_motion_desc(self):
        camera = self.current_state.get("camera", "")
        timeline = self.current_state.get("timeline", "")
        if camera and timeline:
            return f"Second-by-second: {timeline}. Camera: {camera}."
        return camera or "Static controlled camera."

    # ---- Final Output ----

    def generate_final_output(self):
        mode = self.current_state["mode"]

        if mode == AdMode.ONE_SHOT:
            return self._generate_one_shot_output()
        if mode == AdMode.VIRAL_REPLICATE:
            return self._generate_viral_output()
        if mode == AdMode.AGENT_MODE:
            return self._generate_agent_output()
        if mode == AdMode.SHORT_DRAMA:
            return self._generate_drama_output()
        if mode == "seedream_image":
            return self._generate_seedream_output()

        concept = self.current_state["concept"]
        timeline = self.current_state["timeline"]
        composition = self.current_state["composition"]
        lighting = self.current_state["lighting"]
        sound = self.current_state["sound"]
        negative = self.generate_negative_prompt()

        prompt = (
            f"{concept}. "
            f"Timeline: {timeline}. "
            f"Composition: {composition}. "
            f"Camera: {self.generate_camera_motion_desc()}. "
            f"Lighting: {lighting}. "
            f"Cinematic quality, 4k, Seedance 2.0 style, --duration {self.current_state['duration']}s."
        )

        output = {
            "STANDARD_PROMPT": prompt,
            "NEGATIVE_PROMPT": negative,
            "TIMELINE": timeline,
            "CAMERA": self.generate_camera_motion_desc(),
            "MOTION_STRENGTH": self._suggest_motion_strength(),
            "DURATION": f"{self.current_state['duration']}s",
            "MODE": AdMode.LABELS.get(mode, "Unknown"),
            "MODE_KEY": mode,
            "MULTI_MODAL_ADVICE": self.generate_image_ref_advice(),
            "SOUND_DESIGN": sound,
            "SHOT_LIST": self.current_state.get("shots", []),
        }

        quality_issues = self.run_quality_gates(output)
        if quality_issues:
            output["QUALITY_WARNINGS"] = quality_issues

        return output

    def _generate_one_shot_output(self):
        output = self.one_shot_engine.get_output(
            concept=self.current_state.get("concept", ""),
            sound=self.current_state.get("sound", ""),
        )
        output["MODE"] = AdMode.LABELS[AdMode.ONE_SHOT]
        output["MODE_KEY"] = AdMode.ONE_SHOT
        quality_issues = self.run_quality_gates(output)
        if quality_issues:
            output["QUALITY_WARNINGS"] = quality_issues
        return output

    def _generate_viral_output(self):
        output = self.viral_engine.get_output(
            concept=self.current_state.get("concept", ""),
        )
        output["MODE"] = AdMode.LABELS[AdMode.VIRAL_REPLICATE]
        output["MODE_KEY"] = AdMode.VIRAL_REPLICATE
        quality_issues = self.run_quality_gates(output)
        if quality_issues:
            output["QUALITY_WARNINGS"] = quality_issues
        return output

    def _generate_agent_output(self):
        raw = self.current_state.get("concept", "")
        self.agent_engine.parse_intent(raw)
        output = self.agent_engine.build_agent_output()
        output["MODE"] = AdMode.LABELS[AdMode.AGENT_MODE]
        output["MODE_KEY"] = AdMode.AGENT_MODE
        quality_issues = self.run_quality_gates(output)
        if quality_issues:
            output["QUALITY_WARNINGS"] = quality_issues
        return output

    def _generate_drama_output(self):
        concept = self.current_state.get("concept", "")
        self.drama_engine.parse_script(concept)
        self.drama_engine.enable_consistency()
        output = self.drama_engine.get_output()
        quality_issues = self.run_quality_gates(output)
        if "CONSISTENCY" in output and output["CONSISTENCY"].get("acceptance", {}).get("details"):
            consistency_issues = []
            for issues in output["CONSISTENCY"]["acceptance"]["details"].values():
                consistency_issues.extend(issues)
            if consistency_issues:
                quality_issues.extend(consistency_issues)
        if quality_issues:
            output["QUALITY_WARNINGS"] = quality_issues
        return output

    def _generate_seedream_output(self):
        output = self.seedream_engine.get_output()
        # 图片模式跳过视频专用质量门禁
        return output

    def run_quality_gates(self, output):
        issues = []
        mode = output.get("MODE_KEY")
        if mode == AdMode.ECOMMERCE:
            issues += QualityGate.check_ecommerce(output)
        elif mode == AdMode.CREATIVE_FILM:
            issues += QualityGate.check_creative_film(output)
        elif mode == AdMode.UGC:
            issues += QualityGate.check_ugc(output)
        elif mode == AdMode.CINEMATIC:
            issues += QualityGate.check_cinematic(output)
        elif mode == AdMode.MULTI_SHOT:
            issues += QualityGate.check_multi_shot(output)
        elif mode == AdMode.ONE_SHOT:
            issues += QualityGate.check_one_shot(output)
        elif mode == AdMode.VIRAL_REPLICATE:
            issues += QualityGate.check_viral_replicate(output)
        elif mode == AdMode.SHORT_DRAMA:
            issues += QualityGate.check_short_drama(output)
        issues += QualityGate.check_camera_motion(output)
        issues += QualityGate.check_negative_prompt(output)
        issues += QualityGate.check_prompt_structure(output)
        return issues

    def _suggest_motion_strength(self):
        mode = self.current_state["mode"]
        strengths = {
            AdMode.ECOMMERCE: 2,
            AdMode.UGC: 3,
            AdMode.CINEMATIC: 5,
            AdMode.MULTI_SHOT: 4,
            AdMode.ONE_SHOT: 4,
            AdMode.VIRAL_REPLICATE: 5,
            AdMode.SHORT_DRAMA: 4,
        }
        return strengths.get(mode, 5)

    # ---- Render ----

    def render_to_html(self, output):
        path = os.path.join(self.assets_path, "storyboard_template.html")
        if not os.path.exists(path):
            return '<html><body><h1>Template not found</h1></body></html>'
        with open(path, "r", encoding="utf-8") as f:
            template = f.read()
        for key, value in output.items():
            if isinstance(value, list):
                if key == "SHOT_LIST":
                    rows = []
                    for item in value:
                        if isinstance(item, dict):
                            rows.append(f"<tr><td>{item.get('shot','')}</td><td>{item.get('type','')}</td><td>{item.get('desc',str(item))}</td></tr>")
                        else:
                            rows.append(f"<tr><td colspan='3'>{item}</td></tr>")
                    value = f"<table class='shot-list'><tr><th>#</th><th>类型</th><th>描述</th></tr>{''.join(rows)}</table>"
                elif key == "QUALITY_WARNINGS":
                    value = f"<ul>{''.join(f'<li>{v}</li>' for v in value)}</ul>"
                else:
                    value = "<br>".join(str(v) for v in value)
            if key == "QUALITY_WARNINGS" and value:
                value = f"<div class='quality-warnings'><ul>{''.join(f'<li>{v}</li>' for v in (value if isinstance(value, list) else [value]))}</ul></div>"
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def reset(self):
        self.current_state = {
            "phase": 0,
            "mode": None,
            "concept": "",
            "timeline": "",
            "composition": "",
            "camera": "",
            "lighting": "",
            "sound": "",
            "invariants": [],
            "shots": [],
            "duration": 15,
            "params": {},
        }

    def save_session(self, path):
        import copy
        state = copy.deepcopy(self.current_state)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_session(self, path):
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.current_state.update(state)
        return self.current_state["phase"]

    def run_checklist(self, output):
        check_results = {
            "mode_confirmed": output.get("MODE_KEY") in AdMode.LABELS,
            "seedance_mode_recommended": bool(output.get("MODE_KEY")),
            "duration_set": bool(output.get("DURATION")),
            "motion_strength_set": isinstance(output.get("MOTION_STRENGTH"), int),
            "subject_clear": len(output.get("STANDARD_PROMPT", "")) > 0,
            "composition_determined": bool(self.current_state.get("composition")),
            "camera_single_movement": len(QualityGate.check_camera_motion(output)) == 0,
            "lighting_specified": bool(self.current_state.get("lighting")),
            "sound_designed": bool(output.get("SOUND_DESIGN")),
            "negative_prompt_present": bool(output.get("NEGATIVE_PROMPT")),
            "output_5_layer_structure": len(QualityGate.check_prompt_structure(output)) == 0,
            "mode_specific_gates_passed": len(self.run_quality_gates(output)) == 0,
        }
        check_results["all_passed"] = all(check_results.values())
        check_results["pass_count"] = sum(1 for v in check_results.values() if v is True)
        check_results["total_count"] = len(check_results) - 2
        return check_results


if __name__ == "__main__":
    import argparse
    import sys as _sys

    parser = argparse.ArgumentParser(
        description="MadStory — 广告级影视分镜引擎 (Seedance 2.0 驱动)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  mad-story --mode ecommerce --concept "护肤品展示" --output ecom.json
  mad-story --mode short_drama --script 剧本.txt --output drama.json
  mad-story --interactive
        """
    )
    parser.add_argument("--mode", "-m", choices=list(AdMode.LABELS.keys()),
                        help="创作模式")
    parser.add_argument("--concept", "-c", help="核心创意描述")
    parser.add_argument("--timeline", "-t", default="0-15s", help="时间轴 (默认: 0-15s)")
    parser.add_argument("--composition", "-p", default="center frame",
                        help="构图方式 (默认: center frame)")
    parser.add_argument("--camera", "-a", default="static", help="镜头运动 (默认: static)")
    parser.add_argument("--lighting", "-l", default="default", help="光影描述")
    parser.add_argument("--sound", "-s", default="ambient", help="声音设计")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument("--html", help="输出 HTML 预览文件路径")
    parser.add_argument("--session", help="保存 session 文件路径")
    parser.add_argument("--load", help="从 session 文件恢复")
    parser.add_argument("--script", help="短剧剧本文件路径 (仅 short_drama 模式)")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="交互式引导模式")
    parser.add_argument("--list-modes", action="store_true", help="列出所有模式")
    parser.add_argument("--validate", help="校验已生成的 JSON 输出文件")
    parser.add_argument("--check-consistency", help="短剧一致性最终验收 (传入 episode_output.json)")

    args = parser.parse_args()
    assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    refs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
    engine = MadStoryEngine(assets_path, refs_path)

    if args.list_modes:
        print("可用创作模式:")
        for k, v in AdMode.LABELS.items():
            seedance = AdMode.DEFAULT_SEEDANCE_MODE.get(k, "text-to-video")
            print(f"  {k:20s} — {v:10s} (Seedance: {seedance})")
        _sys.exit(0)

    if args.validate:
        with open(args.validate, "r", encoding="utf-8") as f:
            data = json.load(f)
        issues = engine.run_quality_gates(data)
        if issues:
            print(f"校验失败 ({len(issues)} 项):")
            for issue in issues:
                print(f"  - {issue}")
            _sys.exit(1)
        else:
            print("校验通过。")
            _sys.exit(0)

    if args.check_consistency:
        with open(args.check_consistency, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("MODE_KEY") != AdMode.SHORT_DRAMA:
            print("错误: --check-consistency 仅支持短剧 (short_drama) 模式输出")
            _sys.exit(1)
        ledger = ConsistencyLedger()
        consistency_data = data.get("CONSISTENCY", {}).get("ledger", {})
        if consistency_data:
            for cname, cd in consistency_data.get("characters", {}).items():
                char = ledger.create_character(cname)
                char.visual_mark = cd.get("visual_mark", "")
                char.hair_style_color = cd.get("hair_style_color", "")
                char.makeup = cd.get("makeup", "")
                char.outfit = cd.get("outfit", "")
                char.accessories = cd.get("accessories", "")
                char.wear_state = cd.get("wear_state", "")
                char.traits = cd.get("traits", [])
                char.habits = cd.get("habits", "")
                char.speech_style = cd.get("speech_style", "")
            for sid, sd in consistency_data.get("scenes", {}).items():
                scene = ledger.create_scene(sid)
                scene.spatial_layout = sd.get("spatial_layout", "")
                scene.prop_placement = sd.get("prop_placement", "")
                scene.light_direction = sd.get("light_direction", "")
                scene.color_temp_k = sd.get("color_temp_k", 5600)
                scene.weather = sd.get("weather", "")
                scene.ambient_noise = sd.get("ambient_noise", "")
                scene.prop_states = sd.get("prop_states", {})
                scene.reference_images = sd.get("reference_images", [])
                scene.measurement_drawings = sd.get("measurement_drawings", [])
            for tm in consistency_data.get("timeline", []):
                pos = tm.get("position", "")
                import re as _re
                pos_match = _re.match(r"Ep(\d+)@(\d+)s-(\d+)s", pos)
                if pos_match:
                    ep, start, end = int(pos_match.group(1)), int(pos_match.group(2)), int(pos_match.group(3))
                    chars = tm.get("characters", [])
                    sid = tm.get("scene_id", "unknown")
                    marker = ledger.add_timeline_marker(ep, start, end, chars, sid)
                    for cp in tm.get("checkpoints", []):
                        marker.add_checkpoint(cp.get("at_second", 0), cp.get("note", ""))
        acceptance = ConsistencyValidator.run_final_acceptance(ledger)
        print("\n=== 短剧一致性最终验收 ===")
        print(f"长戏份数量: {len(ledger.get_long_shots())}")
        print(f"总时间线标记: {len(ledger.timeline)}")
        for key, val in acceptance.criteria.items():
            status = "PASS" if val["passed"] else "FAIL"
            print(f"  [{status}] {key}: {val['issue_count']} 个问题")
            for issue in val["issues"]:
                print(f"    - {issue}")
        if acceptance.passed:
            print("\n验收结果: 全部通过")
        else:
            print("\n验收结果: 未通过")
            _sys.exit(1)
        _sys.exit(0)

    if args.load:
        phase = engine.load_session(args.load)
        print(f"已从 {args.load} 恢复 session (phase={phase})")

    if args.interactive:
        print("MadStory 交互模式")
        print("可用模式:", ", ".join(AdMode.LABELS.keys()))
        print("输入 'q' 退出, 'reset' 重置\n")
        msg = engine.select_mode(None) if not engine.current_state["mode"] else ""
        if msg:
            print(msg)
        while True:
            try:
                user_input = input("> ")
            except (EOFError, KeyboardInterrupt):
                break
            if user_input.strip().lower() == "q":
                break
            if user_input.strip().lower() == "reset":
                engine.reset()
                print("已重置。请选择模式:", ", ".join(AdMode.LABELS.keys()))
                continue
            if engine.current_state["mode"] is None:
                result = engine.select_mode(user_input.strip())
            else:
                result = engine.next_phase(user_input)
            if isinstance(result, dict):
                print(json.dumps(result, ensure_ascii=False, indent=2))
                if args.session:
                    engine.save_session(args.session)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    print(f"结果已保存到 {args.output}")
                if args.html:
                    html = engine.render_to_html(result)
                    with open(args.html, "w", encoding="utf-8") as f:
                        f.write(html)
                    print(f"HTML 预览已保存到 {args.html}")
                break
            else:
                print(result)

    elif args.mode:
        print(engine.select_mode(args.mode))

        if args.mode == AdMode.SHORT_DRAMA and args.script:
            with open(args.script, "r", encoding="utf-8") as f:
                script_text = f.read()
            engine.drama_engine.parse_script(script_text)

        if args.concept:
            print(engine.next_phase(args.concept))
            engine.current_state["timeline"] = args.timeline
            engine.current_state["composition"] = args.composition
            engine.current_state["camera"] = args.camera
            engine.current_state["lighting"] = args.lighting
            engine.current_state["sound"] = args.sound
            engine.current_state["phase"] = 5
            result = engine.next_phase("")
            if isinstance(result, dict):
                print(json.dumps(result, ensure_ascii=False, indent=2))
                if args.session:
                    engine.save_session(args.session)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    print(f"结果已保存到 {args.output}")
                if args.html:
                    html = engine.render_to_html(result)
                    with open(args.html, "w", encoding="utf-8") as f:
                        f.write(html)
                    print(f"HTML 预览已保存到 {args.html}")
    else:
        parser.print_help()
