import json
import re
import time

from ad_mode import AdMode

# ============================================================
# 转场类型
# ============================================================

LONG_SHOT_THRESHOLD = 15  # 秒
CHECKPOINT_INTERVAL = 10  # 秒


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


# ============================================================
# 一致性管控系统
# ============================================================

class CharacterDossier:
    """人物设定专属档案"""

    def __init__(self, name):
        self.name = name
        self.visual_mark = ""
        self.hair_style_color = ""
        self.makeup = ""
        self.outfit = ""
        self.accessories = ""
        self.wear_state = ""
        self.traits = []
        self.habits = ""
        self.speech_style = ""
        self.appearance_timeline = []

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
        self.scene_id = scene_id
        self.spatial_layout = ""
        self.prop_placement = ""
        self.light_direction = ""
        self.color_temp_k = 5600
        self.weather = ""
        self.ambient_noise = ""
        self.prop_states = {}
        self.reference_images = []
        self.measurement_drawings = []

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
        self.checkpoints = []
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
        self.characters = {}
        self.scenes = {}
        self.timeline = []

    def create_character(self, name):
        if name not in self.characters:
            self.characters[name] = CharacterDossier(name)
        return self.characters[name]

    def get_character(self, name):
        return self.characters.get(name)

    def all_characters(self):
        return list(self.characters.values())

    def create_scene(self, scene_id):
        if scene_id not in self.scenes:
            self.scenes[scene_id] = SceneProfile(scene_id)
        return self.scenes[scene_id]

    def get_scene(self, scene_id):
        return self.scenes.get(scene_id)

    def all_scenes(self):
        return list(self.scenes.values())

    def add_timeline_marker(self, ep, start_s, end_s, characters, scene_id):
        prev = self.timeline[-1] if self.timeline else None
        marker = TimelineMarker(ep, start_s, end_s, characters, scene_id, prev)
        if prev:
            prev.next = marker
        self.timeline.append(marker)
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
        issues = []
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
        for sid, scene in ledger.scenes.items():
            if not scene.ambient_noise:
                issues.append(f"[C3] 场景'{sid}'缺少背景杂音属性")
        return issues

    @staticmethod
    def run_final_acceptance(ledger):

        class AcceptanceResult:
            def __init__(self):
                self.passed = True
                self.criteria = {}

        result = AcceptanceResult()
        d1_issues = ConsistencyValidator._check_character_appearance(ledger)
        result.criteria["D1_character_appearance"] = {
            "passed": len(d1_issues) == 0,
            "issues": d1_issues,
        }
        d2_issues = ConsistencyValidator._check_behavior_logic(ledger)
        result.criteria["D2_behavior_logic"] = {
            "passed": len(d2_issues) == 0,
            "issues": d2_issues,
        }
        d3_issues = ConsistencyValidator._check_scene_consistency(ledger)
        result.criteria["D3_scene_consistency"] = {
            "passed": len(d3_issues) == 0,
            "issues": d3_issues,
        }
        d4_issues = ConsistencyValidator._check_continuity(ledger)
        result.criteria["D4_continuity"] = {
            "passed": len(d4_issues) == 0,
            "issues": d4_issues,
        }
        result.passed = all(v["passed"] for v in result.criteria.values())
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


# ============================================================
# Seedream 图片生成引擎
# ============================================================

class SeedreamImageEngine:
    """Seedream 4.x/5.x 图片生成引擎 — 3层提示词结构（主体+行为+环境 + 美学补充）
    与视频引擎的5层结构不同，图片模式不需要 Camera/Motion Strength/Negative Prompt
    """

    # 图片操作类型
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_EDIT = "image_edit"
    REFERENCE_TO_IMAGE = "reference_to_image"
    MULTI_IMAGE_INPUT = "multi_image_input"
    MULTI_IMAGE_OUTPUT = "multi_image_output"

    OPERATION_LABELS = {
        TEXT_TO_IMAGE: "文生图",
        IMAGE_EDIT: "图像编辑",
        REFERENCE_TO_IMAGE: "参考图生图",
        MULTI_IMAGE_INPUT: "多图输入",
        MULTI_IMAGE_OUTPUT: "多图输出",
    }

    # 参考图类型
    REF_CHARACTER = "character"
    REF_STYLE = "style"
    REF_VIRTUAL_ENTITY = "virtual_entity"
    REF_DESIGN = "design"

    REF_TYPE_LABELS = {
        REF_CHARACTER: "参考人物形象",
        REF_STYLE: "参考风格",
        REF_VIRTUAL_ENTITY: "参考虚拟实体形象",
        REF_DESIGN: "参考款式",
    }

    # 图像编辑操作
    EDIT_ADD = "add"
    EDIT_DELETE = "delete"
    EDIT_REPLACE = "replace"
    EDIT_MODIFY = "modify"

    EDIT_LABELS = {
        EDIT_ADD: "增加",
        EDIT_DELETE: "删除",
        EDIT_REPLACE: "替换",
        EDIT_MODIFY: "修改",
    }

    def __init__(self):
        self.operation = self.TEXT_TO_IMAGE
        self.subject = ""
        self.action = ""
        self.environment = ""
        self.aesthetics = ""
        self.text_content = ""  # 需要渲染的文字（双引号包裹）
        self.edit_target = ""
        self.edit_action = ""
        self.edit_keep = ""
        self.ref_type = ""
        self.ref_description = ""
        self.generate_description = ""
        self.multi_images = []  # [{"label": "图一", "ref": "..."}, ...]
        self.multi_operation = ""  # replace / combine / transfer
        self.output_count = 1
        self.output_type = ""  # storyboard / manga / ip_product / sticker

    def set_text_to_image(self, subject, action, environment, aesthetics="", text_content=""):
        self.operation = self.TEXT_TO_IMAGE
        self.subject = subject
        self.action = action
        self.environment = environment
        self.aesthetics = aesthetics
        self.text_content = text_content

    def set_image_edit(self, target, action, keep=""):
        self.operation = self.IMAGE_EDIT
        self.edit_target = target
        self.edit_action = action
        self.edit_keep = keep

    def set_reference_to_image(self, ref_type, ref_description, generate_description):
        self.operation = self.REFERENCE_TO_IMAGE
        self.ref_type = ref_type
        self.ref_description = ref_description
        self.generate_description = generate_description

    def set_multi_image_input(self, images, operation):
        self.operation = self.MULTI_IMAGE_INPUT
        self.multi_images = images
        self.multi_operation = operation

    def set_multi_image_output(self, output_count, output_type, subject, aesthetics=""):
        self.operation = self.MULTI_IMAGE_OUTPUT
        self.output_count = output_count
        self.output_type = output_type
        self.subject = subject
        self.aesthetics = aesthetics

    def build_prompt(self):
        if self.operation == self.TEXT_TO_IMAGE:
            return self._build_t2i_prompt()
        elif self.operation == self.IMAGE_EDIT:
            return self._build_edit_prompt()
        elif self.operation == self.REFERENCE_TO_IMAGE:
            return self._build_ref_prompt()
        elif self.operation == self.MULTI_IMAGE_INPUT:
            return self._build_multi_input_prompt()
        elif self.operation == self.MULTI_IMAGE_OUTPUT:
            return self._build_multi_output_prompt()
        return ""

    def _build_t2i_prompt(self):
        parts = []
        if self.subject:
            parts.append(self.subject)
        if self.action:
            parts.append(self.action)
        if self.environment:
            parts.append(self.environment)
        if self.aesthetics:
            parts.append(self.aesthetics)
        if self.text_content:
            parts.append(f'文字内容 "{self.text_content}"')
        return "，".join(parts)

    def _build_edit_prompt(self):
        parts = [self.edit_action]
        if self.edit_keep:
            parts.append(f"保持{self.edit_keep}不变")
        return "，".join(parts)

    def _build_ref_prompt(self):
        ref_label = self.REF_TYPE_LABELS.get(self.ref_type, "参考图")
        return f"{ref_label}：{self.ref_description}，{self.generate_description}"

    def _build_multi_input_prompt(self):
        return f"多图{self.multi_operation}：{self.multi_operation}描述"

    def _build_multi_output_prompt(self):
        type_labels = {
            "storyboard": "分镜序列",
            "manga": "漫画创作",
            "ip_product": "IP 产品",
            "sticker": "表情包",
        }
        label = type_labels.get(self.output_type, "组图")
        return f"一系列{label}，共{self.output_count}张，{self.subject}"

    def get_output(self):
        prompt = self.build_prompt()
        output = {
            "STANDARD_PROMPT": prompt,
            "NEGATIVE_PROMPT": "",  # 图片模式不需要 Negative Prompt
            "IMAGE_OPERATION": self.OPERATION_LABELS.get(self.operation, "文生图"),
            "IMAGE_OPERATION_KEY": self.operation,
            "TIMELINE": "",  # 图片模式无时间轴
            "CAMERA": "",  # 图片模式无镜头运动
            "MOTION_STRENGTH": None,  # 图片模式无运动强度
            "DURATION": "",  # 图片模式无时长
            "MODE": "Seedream 图片生成",
            "MODE_KEY": "seedream_image",
            "MULTI_MODAL_ADVICE": self._build_multi_modal_advice(),
            "SOUND_DESIGN": "",  # 图片模式无声音
            "SHOT_LIST": [],
            "IS_IMAGE_MODE": True,
        }

        if self.operation == self.IMAGE_EDIT:
            output["EDIT_TARGET"] = self.edit_target
            output["EDIT_KEEP"] = self.edit_keep
        elif self.operation == self.REFERENCE_TO_IMAGE:
            output["REF_TYPE"] = self.ref_type
            output["REF_TYPE_LABEL"] = self.REF_TYPE_LABELS.get(self.ref_type, "")
        elif self.operation == self.MULTI_IMAGE_INPUT:
            output["MULTI_IMAGES"] = self.multi_images
            output["MULTI_OPERATION"] = self.multi_operation
        elif self.operation == self.MULTI_IMAGE_OUTPUT:
            output["OUTPUT_COUNT"] = self.output_count
            output["OUTPUT_TYPE"] = self.output_type

        return output

    def _build_multi_modal_advice(self):
        if self.operation == self.TEXT_TO_IMAGE:
            return "纯文本输入，无需参考图"
        elif self.operation == self.IMAGE_EDIT:
            return "需要上传待编辑的原始图片"
        elif self.operation == self.REFERENCE_TO_IMAGE:
            return f"需要上传参考图（{self.REF_TYPE_LABELS.get(self.ref_type, '参考图')}）"
        elif self.operation == self.MULTI_IMAGE_INPUT:
            return f"需要上传 {len(self.multi_images)} 张图片"
        elif self.operation == self.MULTI_IMAGE_OUTPUT:
            return "可选上传风格参考图"
        return ""
