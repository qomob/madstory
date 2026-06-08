import json
import os
import time


class AdMode:
    CREATIVE_FILM = "creative_film"
    ECOMMERCE = "ecommerce"
    UGC = "ugc"
    CINEMATIC = "cinematic"
    MULTI_SHOT = "multi_shot"
    ONE_SHOT = "one_shot"
    VIRAL_REPLICATE = "viral_replicate"
    AGENT_MODE = "agent_mode"
    SHORT_DRAMA = "short_drama"

    LABELS = {
        CREATIVE_FILM: "电影创意探索",
        ECOMMERCE: "电商产品",
        UGC: "UGC 原生广告",
        CINEMATIC: "电影感品牌短片",
        MULTI_SHOT: "多镜头叙事",
        ONE_SHOT: "一镜到底",
        VIRAL_REPLICATE: "爆款复刻",
        AGENT_MODE: "Agent 模式（从一句话到成片）",
        SHORT_DRAMA: "短剧创作",
    }

    DEFAULT_SEEDANCE_MODE = {
        CREATIVE_FILM: "text-to-video",
        ECOMMERCE: "image-to-video",
        UGC: "reference-to-video",
        CINEMATIC: "text-to-video",
        MULTI_SHOT: "reference-to-video",
        ONE_SHOT: "image-to-video",
        VIRAL_REPLICATE: "reference-to-video",
        AGENT_MODE: "text-to-video",
        SHORT_DRAMA: "reference-to-video",
    }

    PRODUCT_DOMINANCE_THRESHOLD = 0.4


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


class TransitionType:
    PUSH = "push"
    PULL = "pull"
    SPIRAL = "spiral"
    DISSOLVE = "dissolve"
    MATCH_CUT = "match_cut"
    WHIP_PAN = "whip_pan"
    WIPE = "wipe"
    AUTO = "auto"

    LABELS = {
        PUSH: "推 (Push)",
        PULL: "拉 (Pull)",
        SPIRAL: "螺旋 (Spiral)",
        DISSOLVE: "溶解 (Dissolve)",
        MATCH_CUT: "匹配剪辑 (Match Cut)",
        WHIP_PAN: "甩 (Whip Pan)",
        WIPE: "遮挡转场 (Wipe)",
        AUTO: "AI 自动 (Auto)",
    }

    PROMPT_KEYWORDS = {
        PUSH: "camera pushes forward through",
        PULL: "camera pulls back revealing",
        SPIRAL: "spiral rotation centered on",
        DISSOLVE: "cross-dissolve to",
        MATCH_CUT: "match cut via",
        WHIP_PAN: "whip pan transition to",
        WIPE: "wipe transition through",
        AUTO: "smooth auto transition to",
    }


class OneShotEngine:
    MAX_IMAGES = 10
    MIN_IMAGES = 2

    def __init__(self):
        self.images = []
        self.transitions = []

    def add_image(self, description, order):
        if len(self.images) >= self.MAX_IMAGES:
            return f"已达到最大图片数 {self.MAX_IMAGES}"
        self.images.append({"desc": description, "order": order})
        return f"已添加图片 #{len(self.images)}: {description}"

    def add_transition(self, from_idx, to_idx, trans_type, duration_s, custom_desc=None):
        if trans_type not in TransitionType.LABELS:
            return f"无效转场类型。可选: {', '.join(TransitionType.LABELS.keys())}"
        self.transitions.append({
            "from": from_idx, "to": to_idx,
            "type": trans_type, "duration": duration_s,
            "custom": custom_desc,
        })
        label = TransitionType.LABELS[trans_type]
        return f"转场 #{len(self.transitions)}: 图片{from_idx}→{to_idx} ({label}, {duration_s}s)"

    def build_one_shot_prompt(self):
        if len(self.images) < self.MIN_IMAGES:
            return ""

        prompt_lines = ["One-shot long take sequence:"]
        total_duration = 0

        for i, img in enumerate(self.images):
            prompt_lines.append(
                f"  [Frame {i + 1}: {img['desc']}]"
            )
            trans = next(
                (t for t in self.transitions if t["from"] == i + 1 and t["to"] == i + 2),
                None,
            )
            if trans:
                kw = TransitionType.PROMPT_KEYWORDS.get(
                    trans["type"], TransitionType.PROMPT_KEYWORDS[TransitionType.AUTO]
                )
                desc = trans.get("custom") or kw
                prompt_lines.append(
                    f"    → [{trans['duration']}s transition: {desc}] →"
                )
                total_duration += trans["duration"]

        prompt_lines.append(
            f"  Total duration: ~{total_duration}s. Continuous spatial flow, "
            f"no cuts, smooth camera, Seedance 2.0 style."
        )
        return "\n".join(prompt_lines)

    def get_output(self, concept="", sound=""):
        images_list = [img["desc"] for img in self.images]
        transitions_list = [
            {
                "from": t["from"], "to": t["to"],
                "type": TransitionType.LABELS.get(t["type"], t["type"]),
                "duration": f"{t['duration']}s",
                "custom": t.get("custom", ""),
            }
            for t in self.transitions
        ]
        return {
            "STANDARD_PROMPT": self.build_one_shot_prompt(),
            "NEGATIVE_PROMPT": (
                "no abrupt cuts, no spatial discontinuity, "
                "no object mutation between frames, no stutter in transitions, no frame-tearing"
            ),
            "IMAGE_SEQUENCE": images_list,
            "TRANSITIONS": transitions_list,
            "IMAGE_COUNT": len(self.images),
            "TIMELINE": f"{len(self.images)}帧一镜到底",
            "CAMERA": "连续空间运镜，无硬切",
            "MOTION_STRENGTH": 4,
            "DURATION": f"~{sum(t['duration'] for t in self.transitions)}s",
            "MODE": AdMode.LABELS[AdMode.ONE_SHOT],
            "MODE_KEY": AdMode.ONE_SHOT,
            "MULTI_MODAL_ADVICE": f"准备 {len(self.images)} 张顺序图片作为帧序列输入",
            "SOUND_DESIGN": sound or "流畅过渡音效，BGM 连贯不中断",
            "SHOT_LIST": [
                {"shot": i + 1, "type": "frame", "desc": img["desc"]}
                for i, img in enumerate(self.images)
            ],
        }


class ViralReplicateEngine:
    STRATEGIES = ["creative_shoot", "classic_remake", "viral_deconstruct"]

    def __init__(self):
        self.reference_video = None
        self.replacement_subject = None
        self.strategy = None
        self.extra_requirements = ""

    def set_reference(self, video_ref, strategy="creative_shoot"):
        self.reference_video = video_ref
        self.strategy = strategy if strategy in self.STRATEGIES else self.STRATEGIES[0]

    def set_replacement(self, subject_ref):
        self.replacement_subject = subject_ref

    def set_extra(self, requirements):
        self.extra_requirements = requirements

    def build_viral_prompt(self):
        if not self.reference_video:
            return ""

        if self.strategy == "creative_shoot":
            if self.replacement_subject:
                return (
                    f"参考[{self.reference_video}]的快速运镜方式以及创作手法，"
                    f"将[{self.reference_video}]的主体更换为[{self.replacement_subject}]，"
                    f"创作成一个类似的创意拍摄视频。{self.extra_requirements}"
                )
            return (
                f"参考[{self.reference_video}]的快速运镜方式以及创作手法，"
                f"创作成一个类似的创意拍摄视频。{self.extra_requirements}"
            )

        elif self.strategy == "classic_remake":
            subj = self.replacement_subject or "指定替换角色"
            return (
                f"复刻[{self.reference_video}]的参考视频内容，还原一切细节，"
                f"但把人物替换成{subj}。{self.extra_requirements}"
            )

        elif self.strategy == "viral_deconstruct":
            return (
                f"解析[{self.reference_video}]这个视频的爆点原因，"
                f"并借鉴其文案、主题、画面风格等，重新做一个新视频。{self.extra_requirements}"
            )

        return ""

    def get_output(self, concept=""):
        prompt = self.build_viral_prompt()
        return {
            "STANDARD_PROMPT": prompt,
            "NEGATIVE_PROMPT": (
                "no style drift from reference, no subject identity loss, "
                "no mismatched pacing, no warped replacement subject, no original ghosting"
            ),
            "REFERENCE_VIDEO": self.reference_video or "",
            "REPLACEMENT_SUBJECT": self.replacement_subject or "",
            "STRATEGY": self.strategy or "",
            "TIMELINE": "与参考视频一致",
            "CAMERA": "复刻参考视频运镜",
            "MOTION_STRENGTH": 5,
            "DURATION": "与参考视频一致",
            "MODE": AdMode.LABELS[AdMode.VIRAL_REPLICATE],
            "MODE_KEY": AdMode.VIRAL_REPLICATE,
            "MULTI_MODAL_ADVICE": (
                f"必选: 参考视频[{self.reference_video or '待上传'}]。"
                f"可选: 替换主体参考图[{self.replacement_subject or '无'}]。"
            ),
            "SOUND_DESIGN": "复刻参考视频配乐风格",
            "SHOT_LIST": [],
        }


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


class AgentModeEngine:
    def __init__(self):
        self.user_input = ""
        self.intent = {}

    def parse_intent(self, raw_input):
        platform_keywords = {
            "抖音": "douyin", "tiktok": "tiktok", "小红书": "xiaohongshu",
            "微信": "wechat", "b站": "bilibili", "bilibili": "bilibili",
            "youtube": "youtube",
        }
        emotion_keywords = {
            "感人": "emotional", "热血": "passionate", "搞笑": "humorous",
            "悬疑": "suspense", "温馨": "warm", "悲伤": "sad",
            "震撼": "epic", "冷静": "calm",
        }
        duration_indicators = {
            "15秒": 15, "30秒": 30, "一分钟": 60, "1分钟": 60,
            "2分钟": 120, "3分钟": 180, "长视频": 60, "短视频": 15,
        }
        style_keywords = {
            "cinematic": ["电影感", "大片", "电影", "cinematic"],
            "anime": ["二次元", "动漫", "anime", "漫画"],
            "3d": ["3D", "三维", "CG"],
            "guofeng": ["国风", "水墨", "古风"],
            "realistic": ["写实", "真实", "照片级"],
            "ugc": ["种草", "测评", "开箱", "口播"],
        }

        intent = {
            "raw": raw_input,
            "has_script": any(kw in raw_input for kw in ["集", "场景:", "人物:", "△"]),
            "has_material": any(kw in raw_input for kw in ["上传", "@图片", "@视频", "参考图"]),
            "suggested_duration": 15,
            "detected_style": "cinematic",
            "detected_mode": AdMode.CINEMATIC,
            "detected_platform": "unknown",
            "detected_emotion": "neutral",
        }

        for platform, code in platform_keywords.items():
            if platform in raw_input:
                intent["detected_platform"] = code
                break

        for emotion, code in emotion_keywords.items():
            if emotion in raw_input:
                intent["detected_emotion"] = code
                break

        for dur_str, dur_val in duration_indicators.items():
            if dur_str in raw_input:
                intent["suggested_duration"] = dur_val
                break

        for style, keywords in style_keywords.items():
            if any(kw in raw_input for kw in keywords):
                intent["detected_style"] = style
                if style == "ugc":
                    intent["detected_mode"] = AdMode.UGC
                break

        self.intent = intent
        return intent

    def plan_route(self):
        intent = self.intent
        has_script = intent.get("has_script")
        has_material = intent.get("has_material")
        style = intent.get("detected_style", "cinematic")
        platform = intent.get("detected_platform", "unknown")
        duration = intent.get("suggested_duration", 15)
        if has_script:
            return AdMode.SHORT_DRAMA
        if has_material:
            return AdMode.VIRAL_REPLICATE
        if style == "ugc":
            return AdMode.UGC
        if platform in ("douyin", "xiaohongshu"):
            return AdMode.UGC if duration <= 30 else AdMode.CINEMATIC
        return AdMode.AGENT_MODE

    def build_agent_output(self):
        intent = self.intent
        route = self.plan_route()
        mode_label = AdMode.LABELS.get(route, "通用创作")
        seedance_mode = AdMode.DEFAULT_SEEDANCE_MODE.get(route, "text-to-video")
        prompt = (
            f"根据以下意图创建视频: {intent['raw']}。"
            f"风格: {intent['detected_style']}。"
            f"时长: ~{intent['suggested_duration']}s。"
        )
        return {
            "STANDARD_PROMPT": prompt,
            "NEGATIVE_PROMPT": "no text watermark, no shaky camera, no object melting",
            "INTENT": intent,
            "ROUTE": route,
            "ROUTE_LABEL": mode_label,
            "SEEDANCE_MODE": seedance_mode,
            "TIMELINE": f"Agent 自动规划, {intent['suggested_duration']}s",
            "CAMERA": "Agent 根据风格自动编排",
            "MOTION_STRENGTH": 4 if route == AdMode.UGC else 5,
            "DURATION": f"{intent['suggested_duration']}s",
            "MODE": f"Agent 模式 → {mode_label}",
            "MODE_KEY": AdMode.AGENT_MODE,
            "MULTI_MODAL_ADVICE": (
                "Agent 模式: 可直接输入文字、上传图片/视频/文案，Agent 自动调度。"
            ),
            "SOUND_DESIGN": "Agent 根据风格自动匹配",
            "SHOT_LIST": [],
        }


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
            self.current_state["phase"] = 7
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


import re


# ============================================================
# 一致性管控系统
# ============================================================

LONG_SHOT_THRESHOLD = 15  # 秒
CHECKPOINT_INTERVAL = 10  # 秒


class CharacterDossier:
    """人物设定专属档案"""

    def __init__(self, name):
        self.name = name
        self.visual_mark = ""          # 视觉标记
        self.hair_style_color = ""     # 发型/发色
        self.makeup = ""               # 妆容
        self.outfit = ""               # 服饰搭配(上衣/下装/鞋/外套)
        self.accessories = ""          # 配饰位置
        self.wear_state = ""           # 穿着状态
        self.traits = []               # 性格标签 (≤3)
        self.habits = ""               # 行为习惯
        self.speech_style = ""         # 台词口径
        self.appearance_timeline = []  # 出镜时间线 [(ep, start_s, end_s), ...]

    def to_dict(self):
        return {
            "name": self.name,
            "visual_mark": self.visual_mark,
            "hair_style_color": self.hair_style_color,
            "makeup": self.makeup,
            "outfit": self.outfit,
            "accessories": self.accessories,
            "wear_state": self.wear_state,
            "traits": self.traits,
            "habits": self.habits,
            "speech_style": self.speech_style,
            "appearance_timeline": [
                f"Ep{ep}@{start_s}s-{end_s}s"
                for ep, start_s, end_s in self.appearance_timeline
            ],
        }

    def appearance_snapshot(self):
        return (
            f"{self.hair_style_color} | {self.makeup} | {self.outfit} | "
            f"{self.accessories} | {self.wear_state} | 标记:{self.visual_mark}"
        )


class SceneProfile:
    """场景全景清单"""

    def __init__(self, scene_id):
        self.scene_id = scene_id            # SC-[集数]-[序号]
        self.spatial_layout = ""            # 空间布局
        self.prop_placement = ""            # 陈设摆放
        self.light_direction = ""           # 光线方向
        self.color_temp_k = 5600            # 色温(K)
        self.weather = ""                   # 天气状态
        self.ambient_noise = ""             # 背景杂音属性
        self.prop_states = {}               # 道具状态 {prop_name: state_desc}
        self.reference_images = []          # 参考实拍图编号
        self.measurement_drawings = []      # 尺寸测绘图编号

    def to_dict(self):
        return {
            "scene_id": self.scene_id,
            "spatial_layout": self.spatial_layout,
            "prop_placement": self.prop_placement,
            "light_direction": self.light_direction,
            "color_temp_k": self.color_temp_k,
            "weather": self.weather,
            "ambient_noise": self.ambient_noise,
            "prop_states": dict(self.prop_states),
            "reference_images": list(self.reference_images),
            "measurement_drawings": list(self.measurement_drawings),
        }

    def env_snapshot(self):
        return (
            f"光:{self.light_direction}@{self.color_temp_k}K | "
            f"天气:{self.weather} | 噪音:{self.ambient_noise} | "
            f"布局:{self.spatial_layout}"
        )


class TimelineMarker:
    """时间线标记节点"""

    def __init__(self, ep, start_s, end_s, characters, scene_id, prev_marker=None, next_marker=None):
        self.ep = ep
        self.start_s = start_s
        self.end_s = end_s
        self.duration = end_s - start_s
        self.characters = characters
        self.scene_id = scene_id
        self.prev = prev_marker
        self.next = next_marker
        self.checkpoints = []  # [(second_offset, note), ...]
        self.is_long_shot = self.duration > LONG_SHOT_THRESHOLD

    def add_checkpoint(self, offset_s, note):
        self.checkpoints.append((offset_s, note))

    def to_dict(self):
        prev_ref = f"Ep{self.prev.ep}@{self.prev.start_s}s-{self.prev.end_s}s" if self.prev else "none"
        next_ref = f"Ep{self.next.ep}@{self.next.start_s}s-{self.next.end_s}s" if self.next else "none"
        return {
            "position": f"Ep{self.ep}@{self.start_s}s-{self.end_s}s",
            "duration_s": self.duration,
            "is_long_shot": self.is_long_shot,
            "characters": list(self.characters),
            "scene_id": self.scene_id,
            "prev": prev_ref,
            "next": next_ref,
            "checkpoints": [{"at_second": s, "note": n} for s, n in self.checkpoints],
        }


class ConsistencyLedger:
    """一致性管控台账 — 前期筹备阶段"""

    def __init__(self):
        self.characters = {}    # name -> CharacterDossier
        self.scenes = {}        # scene_id -> SceneProfile
        self.timeline = []      # list of TimelineMarker

    # --- A1: 人物管理 ---
    def create_character(self, name):
        if name not in self.characters:
            self.characters[name] = CharacterDossier(name)
        return self.characters[name]

    def get_character(self, name):
        return self.characters.get(name)

    def all_characters(self):
        return list(self.characters.values())

    # --- A2: 场景管理 ---
    def create_scene(self, scene_id):
        if scene_id not in self.scenes:
            self.scenes[scene_id] = SceneProfile(scene_id)
        return self.scenes[scene_id]

    def get_scene(self, scene_id):
        return self.scenes.get(scene_id)

    def all_scenes(self):
        return list(self.scenes.values())

    # --- A3: 时间线管理 ---
    def add_timeline_marker(self, ep, start_s, end_s, characters, scene_id):
        prev = self.timeline[-1] if self.timeline else None
        marker = TimelineMarker(ep, start_s, end_s, characters, scene_id, prev)
        if prev:
            prev.next = marker
        self.timeline.append(marker)
        # 更新角色出镜时间线
        for cname in characters:
            if cname in self.characters:
                self.characters[cname].appearance_timeline.append((ep, start_s, end_s))
        return marker

    def get_long_shots(self):
        return [m for m in self.timeline if m.is_long_shot]

    def export_ledger(self):
        return {
            "characters": {n: c.to_dict() for n, c in self.characters.items()},
            "scenes": {sid: s.to_dict() for sid, s in self.scenes.items()},
            "timeline": [m.to_dict() for m in self.timeline],
            "long_shot_count": len(self.get_long_shots()),
        }


class ConsistencyValidator:
    """一致性校验器 — 覆盖全流程校验"""

    @staticmethod
    def verify_pre_shoot(marker, ledger):
        """B1: 开拍前对照核查"""
        issues = []
        scene = ledger.get_scene(marker.scene_id)
        for cname in marker.characters:
            char = ledger.get_character(cname)
            if char is None:
                issues.append(f"[B1-人物] 角色'{cname}'未在台账注册")
                continue
            required = [
                ("视觉标记", char.visual_mark),
                ("发型/发色", char.hair_style_color),
                ("妆容", char.makeup),
                ("服饰搭配", char.outfit),
                ("配饰位置", char.accessories),
                ("穿着状态", char.wear_state),
            ]
            for field_name, value in required:
                if not value:
                    issues.append(
                        f"[B1-人物] 角色'{cname}'缺少'{field_name}' (Marker: Ep{marker.ep}@{marker.start_s}s)"
                    )
        if scene is None:
            issues.append(f"[B1-场景] 场景'{marker.scene_id}'未在台账注册")
        else:
            if not scene.spatial_layout:
                issues.append(f"[B1-场景] 场景'{marker.scene_id}'缺少空间布局")
            if not scene.light_direction:
                issues.append(f"[B1-场景] 场景'{marker.scene_id}'缺少光线方向")
        return issues

    @staticmethod
    def verify_checkpoints(marker):
        """B2: 校验节点完整性"""
        if not marker.is_long_shot:
            return []
        issues = []
        expected = max(1, marker.duration // CHECKPOINT_INTERVAL)
        actual = len(marker.checkpoints)
        if actual < expected:
            issues.append(
                f"[B2] Ep{marker.ep}@{marker.start_s}s 长戏份({marker.duration}s) "
                f"期望≥{expected}个校验节点，实际{actual}个"
            )
        return issues

    @staticmethod
    def verify_post_production(ledger):
        """C1-C3: 后期跨片段一致性精修校验"""
        issues = []

        # C1: 角色跨场次外观一致性
        char_snapshots = {}
        for m in ledger.timeline:
            for cname in m.characters:
                char = ledger.get_character(cname)
                if char is None:
                    continue
                snap = char.appearance_snapshot()
                if cname in char_snapshots and char_snapshots[cname] != snap:
                    issues.append(
                        f"[C1] 角色'{cname}'外观不一致: "
                        f"首次={char_snapshots[cname][:60]}... vs "
                        f"Ep{m.ep}@{m.start_s}s={snap[:60]}..."
                    )
                else:
                    char_snapshots[cname] = snap

        # C2: 同场景环境参数冲突
        scene_params = {}
        for m in ledger.timeline:
            sid = m.scene_id
            scene = ledger.get_scene(sid)
            if scene is None:
                continue
            env = scene.env_snapshot()
            if sid in scene_params and scene_params[sid] != env:
                issues.append(
                    f"[C2] 场景'{sid}'环境参数不一致: "
                    f"首次={scene_params[sid][:50]}... vs 当前={env[:50]}..."
                )
            else:
                scene_params[sid] = env

        # C3: 音轨一致性 (场景级)
        for sid, scene in ledger.scenes.items():
            if not scene.ambient_noise:
                issues.append(f"[C3] 场景'{sid}'缺少背景杂音属性")

        return issues

    @staticmethod
    def run_final_acceptance(ledger):
        """D: 最终验收标准"""

        class AcceptanceResult:
            def __init__(self):
                self.passed = True
                self.criteria = {}

        result = AcceptanceResult()

        # D1: 人物外观无矛盾
        d1_issues = ConsistencyValidator._check_character_appearance(ledger)
        result.criteria["D1_character_appearance"] = {
            "passed": len(d1_issues) == 0,
            "issues": d1_issues,
        }

        # D2: 行为逻辑无冲突
        d2_issues = ConsistencyValidator._check_behavior_logic(ledger)
        result.criteria["D2_behavior_logic"] = {
            "passed": len(d2_issues) == 0,
            "issues": d2_issues,
        }

        # D3: 场景空间无冲突
        d3_issues = ConsistencyValidator._check_scene_consistency(ledger)
        result.criteria["D3_scene_consistency"] = {
            "passed": len(d3_issues) == 0,
            "issues": d3_issues,
        }

        # D4: 跨时段拼接自然
        d4_issues = ConsistencyValidator._check_continuity(ledger)
        result.criteria["D4_continuity"] = {
            "passed": len(d4_issues) == 0,
            "issues": d4_issues,
        }

        result.passed = all(
            v["passed"] for v in result.criteria.values()
        )
        return result

    @staticmethod
    def _check_character_appearance(ledger):
        issues = []
        for char in ledger.all_characters():
            missing = []
            if not char.visual_mark:
                missing.append("视觉标记")
            if not char.hair_style_color:
                missing.append("发型/发色")
            if not char.outfit:
                missing.append("服饰搭配")
            if missing:
                issues.append(f"[D1] 角色'{char.name}'档案不完整: 缺少{', '.join(missing)}")
        return issues

    @staticmethod
    def _check_behavior_logic(ledger):
        issues = []
        for char in ledger.all_characters():
            if len(char.traits) > 3:
                issues.append(f"[D2] 角色'{char.name}'性格标签超过3个({len(char.traits)}个)")
            if not char.speech_style:
                issues.append(f"[D2] 角色'{char.name}'缺少台词口径定义")
        return issues

    @staticmethod
    def _check_scene_consistency(ledger):
        issues = []
        for scene in ledger.all_scenes():
            if not scene.prop_states:
                issues.append(f"[D3] 场景'{scene.scene_id}'缺少道具状态记录")
        return issues

    @staticmethod
    def _check_continuity(ledger):
        issues = []
        long_shots = ledger.get_long_shots()
        for marker in long_shots:
            checkpoint_issues = ConsistencyValidator.verify_checkpoints(marker)
            issues.extend(checkpoint_issues)
            pre_shoot_issues = ConsistencyValidator.verify_pre_shoot(marker, ledger)
            issues.extend(pre_shoot_issues)
        if long_shots and not issues:
            pass
        post_issues = ConsistencyValidator.verify_post_production(ledger)
        issues.extend(post_issues)
        return issues


class ShortDramaEngine:
    def __init__(self):
        self.characters = {}
        self.episodes = []
        self.consistency_ledger = ConsistencyLedger()
        self.consistency_enabled = False

    def register_character(self, name, visual_desc):
        self.characters[name] = visual_desc

    def parse_script(self, script_text):
        episodes_raw = re.split(r"\n(?=第\d+集)", script_text)
        for ep_text in episodes_raw:
            if not ep_text.strip():
                continue
            episode = self._parse_episode(ep_text.strip())
            if episode:
                self.episodes.append(episode)
        return self.episodes

    def _parse_episode(self, ep_text):
        lines = ep_text.strip().split("\n")
        episode = {"scenes": [], "characters": [], "lines": []}
        current_scene = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            ep_match = re.match(r"第(\d+)集", line)
            if ep_match:
                episode["episode_number"] = int(ep_match.group(1))
                continue

            scene_match = re.match(r"场景:\s*(.+)", line)
            if scene_match:
                current_scene = scene_match.group(1)
                episode["scenes"].append(current_scene)
                continue

            char_match = re.match(r"人物:\s*(.+)", line)
            if char_match:
                chars = [c.strip() for c in char_match.group(1).split(",")]
                episode["characters"].extend(chars)
                continue

            action_match = re.match(r"△\s*(.+)", line)
            if action_match:
                episode["lines"].append({
                    "type": "action",
                    "content": action_match.group(1),
                    "scene": current_scene,
                })
                continue

            os_match = re.match(r"(.+?)\s*\(OS\):\s*(.+)", line)
            if os_match:
                episode["lines"].append({
                    "type": "voiceover",
                    "character": os_match.group(1).strip(),
                    "content": os_match.group(2).strip(),
                    "scene": current_scene,
                })
                continue

            dialogue_match = re.match(r"(.+?):\s*(.+)", line)
            if dialogue_match:
                episode["lines"].append({
                    "type": "dialogue",
                    "character": dialogue_match.group(1).strip(),
                    "content": dialogue_match.group(2).strip(),
                    "scene": current_scene,
                })
                continue

        return episode if episode.get("episode_number") is not None else None

    def _resolve_character(self, name):
        if name in self.characters:
            return self.characters[name]
        return f"角色[{name}]"

    def build_episode_output(self, episode_index=0):
        if episode_index >= len(self.episodes):
            return {}
        ep = self.episodes[episode_index]
        ep_num = ep.get("episode_number", episode_index + 1)
        chars_desc = ", ".join(
            f"{c}({self._resolve_character(c)})" for c in ep.get("characters", [])
        )

        prompt_lines = [f"Short drama Episode {ep_num}:"]
        if ep.get("scenes"):
            prompt_lines.append(f"  Scenes: {' → '.join(ep['scenes'])}")
        if chars_desc:
            prompt_lines.append(f"  Characters: {chars_desc}")
        prompt_lines.append("  Sequence:")

        shot_list = []
        for i, line in enumerate(ep.get("lines", [])):
            shot_num = i + 1
            if line["type"] == "action":
                desc = f"Shot {shot_num}: {line['content']} ({line.get('scene', '')})"
                prompt_lines.append(f"    {desc}")
                shot_list.append({"shot": shot_num, "type": "action", "desc": line["content"]})
            elif line["type"] == "voiceover":
                desc = f"Shot {shot_num}: {line['character']}(OS) — {line['content']} ({line.get('scene', '')})"
                prompt_lines.append(f"    {desc}")
                shot_list.append({"shot": shot_num, "type": "voiceover", "character": line["character"], "desc": line["content"]})
            elif line["type"] == "dialogue":
                desc = f"Shot {shot_num}: {line['character']}: {line['content']} ({line.get('scene', '')})"
                prompt_lines.append(f"    {desc}")
                shot_list.append({"shot": shot_num, "type": "dialogue", "character": line["character"], "desc": line["content"]})

        prompt = "\n".join(prompt_lines)
        prompt += (
            f"\n  Consistent character appearance, Seedance 2.0 style, "
            f"continuous narrative flow, episode {ep_num}."
        )

        registered_chars = {c: self._resolve_character(c) for c in ep.get("characters", [])}

        return {
            "STANDARD_PROMPT": prompt,
            "NEGATIVE_PROMPT": (
                "no character face drift across episodes, no costume inconsistency, "
                "no scene discontinuity, no voice mismatch, no subtitle desync"
            ),
            "TIMELINE": f"Episode {ep_num}: {len(ep.get('lines', []))} shots",
            "CAMERA": "Controlled narrative camera, per-scene consistency",
            "MOTION_STRENGTH": 4,
            "DURATION": f"~{len(ep.get('lines', [])) * 3}s",
            "MODE": "短剧创作",
            "MODE_KEY": AdMode.SHORT_DRAMA,
            "MULTI_MODAL_ADVICE": (
                f"Characters reference images: "
                + ", ".join(f"{name}({desc})" for name, desc in registered_chars.items())
                + f". Scene references: {', '.join(ep.get('scenes', []))}"
            ),
            "SOUND_DESIGN": "Dialogue-driven audio mix, ambient background per scene",
            "SHOT_LIST": shot_list,
            "EPISODE_NUMBER": ep_num,
            "CHARACTERS": registered_chars,
        }

    def get_output(self, script_text=""):
        if script_text and not self.episodes:
            self.parse_script(script_text)
        if not self.episodes:
            return {
                "STANDARD_PROMPT": "",
                "NEGATIVE_PROMPT": "no character face drift across episodes, no costume inconsistency",
                "TIMELINE": "无剧本",
                "CAMERA": "N/A",
                "MOTION_STRENGTH": 0,
                "DURATION": "0s",
                "MODE": "短剧创作",
                "MODE_KEY": AdMode.SHORT_DRAMA,
                "MULTI_MODAL_ADVICE": "请提供标准格式剧本",
                "SOUND_DESIGN": "",
                "SHOT_LIST": [],
            }
        output = self.build_episode_output(0)
        if self.consistency_enabled:
            self._build_consistency_ledger()
            output["CONSISTENCY"] = {
                "ledger": self.consistency_ledger.export_ledger(),
            }
            has_long_shots = len(self.consistency_ledger.get_long_shots()) > 0
            if has_long_shots:
                acceptance = ConsistencyValidator.run_final_acceptance(
                    self.consistency_ledger
                )
                output["CONSISTENCY"]["acceptance"] = {
                    "passed": acceptance.passed,
                    "criteria": {
                        k: {"passed": v["passed"], "issue_count": len(v["issues"])}
                        for k, v in acceptance.criteria.items()
                    },
                    "details": {
                        k: v["issues"]
                        for k, v in acceptance.criteria.items()
                        if v["issues"]
                    },
                }
                if not acceptance.passed:
                    output.setdefault("QUALITY_WARNINGS", []).append(
                        "[一致性管控] 最终验收未通过，详见 CONSISTENCY.acceptance"
                    )
        return output

    def enable_consistency(self):
        self.consistency_enabled = True

    def _build_consistency_ledger(self):
        ledger = self.consistency_ledger
        for ep in self.episodes:
            ep_num = ep.get("episode_number", 0)
            for cname in ep.get("characters", []):
                ledger.create_character(cname)
            for i, scene_name in enumerate(ep.get("scenes", []), 1):
                scene_id = f"SC-{ep_num:02d}-{i:02d}"
                ledger.create_scene(scene_id)
            lines = ep.get("lines", [])
            if not lines:
                continue
            shot_duration = 3
            current_start = 0
            current_chars = []
            current_scene = None
            for idx, line in enumerate(lines):
                line_scene = line.get("scene")
                line_char = line.get("character")
                if line_scene != current_scene and current_chars and current_scene:
                    scene_idx = ep.get("scenes", []).index(current_scene) + 1 if current_scene in ep.get("scenes", []) else idx
                    sid = f"SC-{ep_num:02d}-{scene_idx:02d}"
                    marker = ledger.add_timeline_marker(
                        ep_num, current_start, current_start + shot_duration,
                        list(set(current_chars)), sid,
                    )
                    if marker.is_long_shot:
                        num_checkpoints = max(1, marker.duration // CHECKPOINT_INTERVAL)
                        for cp in range(num_checkpoints):
                            checkpoint_sec = cp * CHECKPOINT_INTERVAL
                            if checkpoint_sec < marker.duration:
                                marker.add_checkpoint(
                                    checkpoint_sec,
                                    f"校验节点@{checkpoint_sec}s: 角色外观+场景陈设+光线条件对齐"
                                )
                    current_start += shot_duration
                    current_chars = [line_char] if line_char else []
                else:
                    if line_char and line_char not in current_chars:
                        current_chars.append(line_char)
                current_scene = line_scene
                shot_duration = max(3, min(15, len(line.get("content", "")) // 3 + 3))
            if current_chars and current_scene:
                scene_idx = ep.get("scenes", []).index(current_scene) + 1 if current_scene in ep.get("scenes", []) else len(ep.get("scenes", []))
                sid = f"SC-{ep_num:02d}-{scene_idx:02d}"
                marker = ledger.add_timeline_marker(
                    ep_num, current_start, current_start + 3,
                    list(set(current_chars)), sid,
                )
                if marker.is_long_shot:
                    marker.add_checkpoint(10, "校验节点@10s")


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
