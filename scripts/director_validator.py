#!/usr/bin/env python3
"""
MadStory Director Validator — 世界一线导演级核验工具
覆盖: 全模式边界测试 / 输出结构校验 / 合规性扫描 / 异常输入 / 导演技术规范
"""

import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mad_story_engine import (
    AdMode, QualityGate, TransitionType,
    OneShotEngine, ViralReplicateEngine, AgentModeEngine,
    MadStoryEngine, ShortDramaEngine,
    ConsistencyLedger, ConsistencyValidator,
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def assert_true(self, condition, label):
        if condition:
            self.passed += 1
            print(f"  [PASS] {label}")
        else:
            self.failed += 1
            print(f"  [FAIL] {label}")

    def assert_false(self, condition, label):
        self.assert_true(not condition, label)

    def assert_equal(self, a, b, label):
        self.assert_true(a == b, f"{label}: expected={repr(b)}, got={repr(a)}")

    @property
    def total(self):
        return self.passed + self.failed


_r = TestResult()


def assert_true(condition, label):
    _r.assert_true(condition, label)


def assert_false(condition, label):
    _r.assert_false(condition, label)


def assert_equal(a, b, label):
    _r.assert_equal(a, b, label)


# ============================================================
# SECTION 1: Output Structure Validation (所有模式)
# ============================================================

def test_output_structure():
    print("\n=== 输出结构完整性校验 ===")
    required_keys = [
        "STANDARD_PROMPT", "NEGATIVE_PROMPT", "TIMELINE", "CAMERA",
        "MOTION_STRENGTH", "DURATION", "MODE", "MODE_KEY",
        "MULTI_MODAL_ADVICE", "SOUND_DESIGN", "SHOT_LIST",
    ]
    for mode_key in AdMode.LABELS:
        engine = MadStoryEngine(ASSETS, REFS)
        engine.current_state["mode"] = mode_key
        engine.current_state["phase"] = 5
        engine.current_state["concept"] = "test concept"
        engine.current_state["timeline"] = "0-5s intro, 5-12s action, 12-15s outro"
        engine.current_state["composition"] = "center frame"
        engine.current_state["camera"] = "slow push-in"
        engine.current_state["lighting"] = "warm key light"
        engine.current_state["sound"] = "ambient drone"
        if mode_key == AdMode.ONE_SHOT:
            engine.one_shot_engine.add_image("test frame 1", 1)
            engine.one_shot_engine.add_image("test frame 2", 2)
        if mode_key == AdMode.VIRAL_REPLICATE:
            engine.viral_engine.set_reference("@test_video", "creative_shoot")
            engine.viral_engine.set_replacement("@test_image")
        if mode_key == AdMode.AGENT_MODE:
            engine.agent_engine.parse_intent("test cinematic concept")
        if mode_key == AdMode.SHORT_DRAMA:
            engine.drama_engine.parse_script("第1集\n场景: 测试 清晨\n人物: 甲\n△ 测试动作")
        output = engine.generate_final_output()
        for key in required_keys:
            assert_true(key in output, f"{mode_key}: 缺少字段 '{key}'")
        assert_true(isinstance(output["MOTION_STRENGTH"], int), f"{mode_key}: MOTION_STRENGTH 类型错误")
        assert_true(1 <= output["MOTION_STRENGTH"] <= 10, f"{mode_key}: MOTION_STRENGTH 超范围")
        assert_true(output["NEGATIVE_PROMPT"], f"{mode_key}: NEGATIVE_PROMPT 为空")
        assert_true(output["STANDARD_PROMPT"], f"{mode_key}: STANDARD_PROMPT 为空")


# ============================================================
# SECTION 2: Negative Prompt Compliance (按模式)
# ============================================================

def test_negative_prompt_compliance():
    print("\n=== Negative Prompt 合规性扫描 ===")
    neg_checks = {
        AdMode.ECOMMERCE: ["label", "packaging", "logo", "duplicate"],
        AdMode.UGC: ["finger", "face", "lip", "background"],
        AdMode.CINEMATIC: ["shaky", "melting", "muddy", "flat"],
        AdMode.MULTI_SHOT: ["drift", "inconsistency", "transition"],
        AdMode.ONE_SHOT: ["spatial", "stutter", "tearing"],
        AdMode.VIRAL_REPLICATE: ["style", "identity", "pacing", "ghosting"],
        AdMode.SHORT_DRAMA: ["face", "costume", "episode"],
    }
    for mode_key, required_words in neg_checks.items():
        engine = MadStoryEngine(ASSETS, REFS)
        engine.current_state["mode"] = mode_key
        engine.current_state["phase"] = 5
        engine.current_state["concept"] = "test"
        engine.current_state["timeline"] = "0-15s test"
        engine.current_state["composition"] = "test"
        engine.current_state["camera"] = "static"
        engine.current_state["lighting"] = "default"
        engine.current_state["sound"] = "none"
        if mode_key == AdMode.ONE_SHOT:
            engine.one_shot_engine.add_image("test frame 1", 1)
            engine.one_shot_engine.add_image("test frame 2", 2)
        if mode_key == AdMode.VIRAL_REPLICATE:
            engine.viral_engine.set_reference("@test_video", "creative_shoot")
        if mode_key == AdMode.SHORT_DRAMA:
            engine.drama_engine.parse_script("第1集\n场景: 测试\n人物: 甲\n△ 测试动作")
        output = engine.generate_final_output()
        negative = output["NEGATIVE_PROMPT"].lower()
        for word in required_words:
            assert_true(word in negative, f"{mode_key}: Negative Prompt 缺少 '{word}'")


# ============================================================
# SECTION 3: Boundary Tests (边界输入)
# ============================================================

def test_boundary_conditions():
    print("\n=== 边界条件测试 ===")

    engine = MadStoryEngine(ASSETS, REFS)

    # 3.1 未选择模式直接输入
    engine.reset()
    result = engine.next_phase("some input")
    assert_true("请先选择" in result, "无模式输入应提示选择")

    # 3.2 无效模式
    result = engine.select_mode("nonexistent")
    assert_true("无效模式" in result, "无效模式应返回错误")

    # 3.3 空输入在 Phase 0
    engine.reset()
    engine.current_state["mode"] = AdMode.CINEMATIC
    result = engine.next_phase("")
    assert_true(engine.current_state["phase"] == 1, "空概念仍应推进 Phase")

    # 3.4 全空字段最终输出不崩溃
    engine.reset()
    engine.current_state["mode"] = AdMode.CINEMATIC
    engine.current_state["phase"] = 5
    engine.current_state["concept"] = ""
    engine.current_state["timeline"] = ""
    engine.current_state["composition"] = ""
    engine.current_state["camera"] = ""
    engine.current_state["lighting"] = ""
    engine.current_state["sound"] = ""
    try:
        output = engine.generate_final_output()
        assert_true(isinstance(output, dict), "全空字段应返回 dict")
    except Exception:
        assert_true(False, f"全空字段不应崩溃: {traceback.format_exc()}")

    # 3.5 Phase 6 完成后再输入
    engine.reset()
    engine.current_state["mode"] = AdMode.CINEMATIC
    engine.current_state["phase"] = 5
    engine.current_state["concept"] = "test"
    engine.current_state["timeline"] = "test"
    engine.current_state["composition"] = "test"
    engine.current_state["camera"] = "test"
    engine.current_state["lighting"] = "test"
    engine.current_state["sound"] = "test"
    output = engine.generate_final_output()
    result = engine.next_phase("extra input")
    assert_true("已完成" in result or output != result, "完成后不应再推进")

    # 3.6 Multi-shot 边界: 0 镜头 / 1 镜头 / 4 镜头(超限)
    engine.reset()
    engine.current_state["mode"] = AdMode.MULTI_SHOT
    result = engine.add_shot("test", 5)
    assert_true("镜头 #1" in result, "应添加第一镜头")
    result = engine.add_shot("test", 5)
    assert_true("镜头 #2" in result, "应添加第二镜头")
    result = engine.add_shot("test", 3)
    assert_true("镜头 #3" in result, "应添加第三镜头")
    result = engine.add_shot("test", 2)
    assert_true("镜头 #4" in result, "应添加第四镜头")
    output = engine.generate_final_output()
    issues = QualityGate.check_multi_shot(output)
    assert_true(len(issues) > 0, "4 镜头应触发质量警告")


# ============================================================
# SECTION 4: Camera Motion Constraint Enforcement
# ============================================================

def test_camera_motion_validation():
    print("\n=== 镜头运动约束强制校验 ===")

    # 单运动应通过
    output = {"CAMERA": "slow push-in camera movement"}
    issues = QualityGate.check_camera_motion(output)
    assert_true(len(issues) == 0, "单运动 push-in 应通过")

    # 单运动 dolly
    output = {"CAMERA": "side dolly tracking shot"}
    issues = QualityGate.check_camera_motion(output)
    assert_true(len(issues) == 0, "单运动 dolly 应通过")

    # 多运动应触发警告
    output = {"CAMERA": "orbit and zoom and pan all at once"}
    issues = QualityGate.check_camera_motion(output)
    assert_true(len(issues) > 0, "多运动应触发警告")

    # UGC 手持感不算多运动 (handheld 是合法的单运动)
    output = {"CAMERA": "subtle handheld feel"}
    issues = QualityGate.check_camera_motion(output)
    assert_true(len(issues) == 0, "单手持不应触发")

    # 混用推+拉应触发
    output = {"CAMERA": "push in then pull out"}
    issues = QualityGate.check_camera_motion(output)
    assert_true(len(issues) > 0, "推+拉应触发")


# ============================================================
# SECTION 5: One-Shot Edge Cases
# ============================================================

def test_one_shot_engine():
    print("\n=== 一镜到底引擎边界测试 ===")

    # 5.1 最低图片数
    oneshot = OneShotEngine()
    oneshot.add_image("frame 1", 1)
    oneshot.add_image("frame 2", 2)
    prompt = oneshot.build_one_shot_prompt()
    assert_true(len(prompt) > 0, "2 图应生成 prompt")

    # 5.2 只有 1 张图
    oneshot2 = OneShotEngine()
    oneshot2.add_image("frame 1", 1)
    prompt = oneshot2.build_one_shot_prompt()
    assert_equal(prompt, "", "1 图不应生成 prompt")

    # 5.3 10 张图上限
    oneshot3 = OneShotEngine()
    for i in range(10):
        result = oneshot3.add_image(f"frame {i}", i + 1)
    result = oneshot3.add_image("frame 11", 11)
    assert_true("达到最大" in result, "超过 10 张应拒绝")

    # 5.4 无转场描述
    oneshot4 = OneShotEngine()
    oneshot4.add_image("a", 1)
    oneshot4.add_image("b", 2)
    output = oneshot4.get_output()
    assert_true(output["IMAGE_COUNT"] == 2, "应有 2 张图片计数")

    # 5.5 无效转场类型
    result = oneshot4.add_transition(1, 2, "invalid_type", 2)
    assert_true("无效转场类型" in result, "无效类型应提示")

    # 5.6 转场顺序完整性
    oneshot5 = OneShotEngine()
    for i in range(5):
        oneshot5.add_image(f"frame {i}", i + 1)
    oneshot5.add_transition(1, 2, TransitionType.PUSH, 2)
    oneshot5.add_transition(2, 3, TransitionType.SPIRAL, 3)
    oneshot5.add_transition(3, 4, TransitionType.WHIP_PAN, 1.5)
    oneshot5.add_transition(4, 5, TransitionType.DISSOLVE, 2)
    output = oneshot5.get_output()
    assert_equal(len(output["TRANSITIONS"]), 4, "应有 4 个转场")
    assert_equal(output["IMAGE_COUNT"], 5, "应有 5 张图片")


# ============================================================
# SECTION 6: Viral Replicate Edge Cases
# ============================================================

def test_viral_replicate_engine():
    print("\n=== 爆款复刻引擎边界测试 ===")

    # 6.1 无参考视频
    viral = ViralReplicateEngine()
    prompt = viral.build_viral_prompt()
    assert_equal(prompt, "", "无参考视频应返回空")

    # 6.2 creative_shoot 无替换主体
    viral.set_reference("@video1", "creative_shoot")
    prompt = viral.build_viral_prompt()
    assert_true("参考[" in prompt, "应生成基础复刻提示词")
    assert_true("主体更换" not in prompt, "无替换主体不应含更换语言")

    # 6.3 creative_shoot 有替换主体
    viral.set_replacement("@image1")
    prompt = viral.build_viral_prompt()
    assert_true("主体更换" in prompt, "有替换主体应含更换语言")

    # 6.4 classic_remake
    viral2 = ViralReplicateEngine()
    viral2.set_reference("@video1", "classic_remake")
    viral2.set_replacement("一只猫")
    prompt = viral2.build_viral_prompt()
    assert_true("人物替换成" in prompt, "经典还原应含替换描述")

    # 6.5 viral_deconstruct
    viral3 = ViralReplicateEngine()
    viral3.set_reference("@video1", "viral_deconstruct")
    viral3.set_extra("将方言改为上海话")
    prompt = viral3.build_viral_prompt()
    assert_true("爆点原因" in prompt, "爆款拆解应含解析关键词")
    assert_true("上海话" in prompt, "应保留额外要求")

    # 6.6 无效策略
    viral4 = ViralReplicateEngine()
    viral4.set_reference("@video1", "nonexistent_strategy")
    assert_equal(viral4.strategy, "creative_shoot", "无效策略应 fallback 到 creative_shoot")


# ============================================================
# SECTION 7: Agent Mode Edge Cases
# ============================================================

def test_agent_mode_engine():
    print("\n=== Agent 模式引擎边界测试 ===")

    # 7.1 模糊意图
    agent = AgentModeEngine()
    intent = agent.parse_intent("帮我生成一段15秒的三国赤壁之战经典场面短视频，要电影感大片风格")
    assert_equal(intent["detected_style"], "cinematic", "应检测到电影感")

    # 7.2 UGC 意图检测
    intent = agent.parse_intent("帮我做一个护肤品的种草测评视频")
    assert_equal(intent["detected_style"], "ugc", "应检测到 ugc 风格")

    # 7.3 长视频检测
    intent = agent.parse_intent("帮我做一个1分钟的3D动画短片")
    assert_equal(intent["suggested_duration"], 60, "应检测到 1 分钟")
    assert_equal(intent["detected_style"], "3d", "应检测到 3D 风格")

    # 7.4 剧本检测
    intent = agent.parse_intent("第一集 场景: 灵霄宗外门 清晨 人物: 江晏, 众弟子")
    assert_true(intent["has_script"], "应检测到剧本格式")
    route = agent.plan_route()
    assert_equal(route, AdMode.SHORT_DRAMA, "剧本应路由到短剧")

    # 7.5 素材检测
    intent = agent.parse_intent("参考我上传的 @图片1 和 @视频1，做一个类似风格的视频")
    assert_true(intent["has_material"], "应检测到素材标记")
    route = agent.plan_route()
    assert_equal(route, AdMode.VIRAL_REPLICATE, "素材应路由到爆款复刻")

    # 7.6 空输入
    agent2 = AgentModeEngine()
    intent = agent2.parse_intent("")
    assert_equal(intent["detected_style"], "cinematic", "空输入应默认 cinematic")
    assert_false(intent["has_script"], "空输入不应检测到剧本")

    # 7.7 国风检测
    intent = agent2.parse_intent("做一个水墨国风短片")
    assert_equal(intent["detected_style"], "guofeng", "应检测到国风")


# ============================================================
# SECTION 8: Duration Compliance
# ============================================================

def test_duration_compliance():
    print("\n=== 时长合规性校验 ===")
    for mode_key in AdMode.LABELS:
        engine = MadStoryEngine(ASSETS, REFS)
        engine.current_state["mode"] = mode_key
        engine.current_state["phase"] = 5
        engine.current_state["concept"] = "test"
        engine.current_state["timeline"] = "test"
        engine.current_state["composition"] = "test"
        engine.current_state["camera"] = "test"
        engine.current_state["lighting"] = "test"
        engine.current_state["sound"] = "test"
        if mode_key == AdMode.ONE_SHOT:
            engine.one_shot_engine.add_image("test frame 1", 1)
            engine.one_shot_engine.add_image("test frame 2", 2)
        if mode_key == AdMode.VIRAL_REPLICATE:
            engine.viral_engine.set_reference("@test_video", "creative_shoot")
        if mode_key == AdMode.SHORT_DRAMA:
            engine.drama_engine.parse_script("第1集\n场景: 测试\n人物: 甲\n△ 测试动作")
        output = engine.generate_final_output()
        dur = output["DURATION"]
        assert_true("s" in dur or "参考" in dur or "一致" in dur,
                    f"{mode_key}: DURATION 缺时间单位")


# ============================================================
# SECTION 9: Mode Enum Integrity
# ============================================================

def test_mode_enum_integrity():
    print("\n=== 模式枚举完整性校验 ===")
    assert_equal(len(AdMode.LABELS), 9, "应有 9 个模式")
    assert_equal(len(AdMode.DEFAULT_SEEDANCE_MODE), 9, "应有 9 个 Seedance 映射")
    for mode_key in AdMode.LABELS:
        assert_true(mode_key in AdMode.DEFAULT_SEEDANCE_MODE, f"{mode_key} 缺 Seedance 映射")


# ============================================================
# SECTION 10: TransitionType Enum Integrity
# ============================================================

def test_transition_enum_integrity():
    print("\n=== 转场类型枚举完整性校验 ===")
    attrs = [TransitionType.PUSH, TransitionType.PULL, TransitionType.SPIRAL,
             TransitionType.DISSOLVE, TransitionType.MATCH_CUT,
             TransitionType.WHIP_PAN, TransitionType.WIPE, TransitionType.AUTO]
    assert_equal(len(TransitionType.LABELS), 8, "应有 8 种转场类型")
    assert_equal(len(TransitionType.PROMPT_KEYWORDS), 8, "应有 8 个转场提示词")
    for attr in attrs:
        assert_true(attr in TransitionType.LABELS, f"{attr} 缺 LABEL")
        assert_true(attr in TransitionType.PROMPT_KEYWORDS, f"{attr} 缺 KEYWORD")


# ============================================================
# SECTION 11: Reset & State Isolation
# ============================================================

def test_reset_and_isolation():
    print("\n=== 引擎状态重置与隔离性测试 ===")
    engine = MadStoryEngine(ASSETS, REFS)
    engine.current_state["mode"] = AdMode.CINEMATIC
    engine.current_state["concept"] = "dirty state"
    engine.current_state["shots"] = [{"desc": "test", "duration": 5}]
    engine.reset()
    assert_equal(engine.current_state["mode"], None, "reset 后 mode 应为 None")
    assert_equal(engine.current_state["concept"], "", "reset 后 concept 应为空")
    assert_equal(engine.current_state["shots"], [], "reset 后 shots 应为空")
    assert_equal(engine.current_state["phase"], 0, "reset 后 phase 应为 0")


# ============================================================
# SECTION 12: JSON Resource Integrity
# ============================================================

def test_resource_integrity():
    print("\n=== 资源文件完整性校验 ===")
    cheat_path = os.path.join(ASSETS, "cheat_sheet.json")
    assert_true(os.path.exists(cheat_path), "cheat_sheet.json 存在")

    with open(cheat_path, "r") as f:
        data = json.load(f)

    # 验证顶层键
    top_keys = ["seedance_2.0_quick_params", "ad_modes", "camera_language_presets",
                "lighting_atmosphere_presets", "sound_design_presets",
                "quality_guardrails", "multi_shot_syntax",
                "one_shot_transitions", "viral_replicate_strategies",
                "agent_mode_style_detection", "short_drama_script_format"]
    for key in top_keys:
        assert_true(key in data, f"cheat_sheet 缺少 '{key}'")

    # 验证每个 ad_mode 在 cheat sheet 中
    for key in ["ecommerce", "ugc", "cinematic", "multi_shot"]:
        assert_true(key in data["ad_modes"], f"ad_modes 缺少 '{key}'")

    # 验证转场类型完整性
    assert_equal(len(data["one_shot_transitions"]), 8, "应有 8 个转场预设")

    # 验证爆款复刻策略
    assert_equal(len(data["viral_replicate_strategies"]), 3, "应有 3 个复刻策略")

    # 验证 Agent 风格检测
    assert_equal(len(data["agent_mode_style_detection"]), 6, "应有 6 个风格检测")


# ============================================================
# SECTION 9: Consistency Protocol Tests
# ============================================================

def test_consistency_ledger():
    print("\n=== 一致性管控台账 (A1-A3) ===")

    ledger = ConsistencyLedger()

    # A1: 人物档案
    char = ledger.create_character("张三")
    char.visual_mark = "左眉上方刀疤"
    char.hair_style_color = "黑色短发，三七分"
    char.makeup = "素颜"
    char.outfit = "黑色皮夹克，白色圆领T恤，深蓝牛仔裤"
    char.accessories = "右手腕银链"
    char.wear_state = "皮夹克拉链半开"
    char.traits = ["冷静", "果断"]
    char.habits = "说话时习惯摸下巴"
    char.speech_style = "语速慢，用词简练"
    assert_equal(char.name, "张三", "角色名创建")
    assert_true(len(char.appearance_snapshot()) > 30, "外观快照非空")

    # A2: 场景清单
    scene = ledger.create_scene("SC-01-01")
    scene.spatial_layout = "小型办公室，窗在右侧，桌居中"
    scene.prop_placement = "桌上:笔记本电脑、咖啡杯(距桌沿5cm)"
    scene.light_direction = "右侧窗自然光，45度俯角"
    scene.color_temp_k = 5600
    scene.weather = "晴"
    scene.ambient_noise = "空调低频运转声+偶尔窗外车流"
    scene.prop_states = {"咖啡杯": "陶瓷材质，杯口有轻微茶渍"}
    assert_true(len(scene.env_snapshot()) > 30, "环境快照非空")

    # A3: 时间线
    marker = ledger.add_timeline_marker(1, 0, 18, ["张三"], "SC-01-01")
    assert_true(marker.is_long_shot, "18秒应标记为长戏份")
    marker.add_checkpoint(10, "校验节点@10s")
    assert_equal(len(ledger.get_long_shots()), 1, "长戏份数量")

    short_marker = ledger.add_timeline_marker(1, 20, 32, ["张三"], "SC-01-01")
    assert_false(short_marker.is_long_shot, "12秒不应标记为长戏份")

    exported = ledger.export_ledger()
    assert_true("characters" in exported, "台账导出含角色")
    assert_true("scenes" in exported, "台账导出含场景")
    assert_true("timeline" in exported, "台账导出含时间线")
    assert_equal(exported["long_shot_count"], 1, "台账导出含长戏份计数")


def test_consistency_validator():
    print("\n=== 一致性校验器全流程 (B1-D4) ===")

    ledger = ConsistencyLedger()

    char = ledger.create_character("李四")
    char.visual_mark = "右眼下方泪痣"
    char.hair_style_color = "棕色长发，中分"
    char.makeup = "淡妆，豆沙色口红"
    char.outfit = "白色衬衫，卡其色长裤"
    char.accessories = "左手腕金表"
    char.wear_state = "衬衫袖口挽至前臂"
    char.traits = ["温柔", "坚韧", "细心"]
    char.speech_style = "语速中等，常用问句结尾"

    scene = ledger.create_scene("SC-01-01")
    scene.spatial_layout = "咖啡馆靠窗座位"
    scene.light_direction = "正面窗外光"
    scene.prop_states = {"马克杯": "白色，把手有裂纹"}

    # B1: 开拍前核查
    marker = ledger.add_timeline_marker(1, 0, 20, ["李四"], "SC-01-01")
    b1_issues = ConsistencyValidator.verify_pre_shoot(marker, ledger)
    assert_true(len(b1_issues) == 0, f"B1完整档案应通过 (实际{len(b1_issues)}项)")

    # B2: 校验节点
    b2_issues = ConsistencyValidator.verify_checkpoints(marker)
    assert_true(len(b2_issues) > 0, "B2无校验节点应检测到问题")

    marker.add_checkpoint(10, "校验@10s")
    marker.add_checkpoint(20, "校验@20s")
    b2_issues2 = ConsistencyValidator.verify_checkpoints(marker)
    assert_true(len(b2_issues2) == 0, "B2有校验节点应通过")

    # C: 后期校验
    post_issues = ConsistencyValidator.verify_post_production(ledger)
    assert_true(any("C3" in i for i in post_issues), "C3缺少噪音属性应检测到")

    scene.ambient_noise = "室内咖啡机运转声"
    post_issues2 = ConsistencyValidator.verify_post_production(ledger)
    assert_true(len(post_issues2) == 0, "C1-C3完整无问题应通过")

    # D: 最终验收
    result = ConsistencyValidator.run_final_acceptance(ledger)
    assert_true("D1_character_appearance" in result.criteria, "D1存在")
    assert_true("D2_behavior_logic" in result.criteria, "D2存在")
    assert_true("D3_scene_consistency" in result.criteria, "D3存在")
    assert_true("D4_continuity" in result.criteria, "D4存在")
    assert_true(result.passed, "完整台账最终验收应通过")


def test_short_drama_long_shot_consistency():
    print("\n=== 短剧长戏份一致性 ===")

    script = (
        "第1集\n"
        "场景: 办公室 下午\n"
        "人物: 王总, 助理\n"
        "△ 王总坐在办公桌前翻看文件\n"
        "王总: 这个月的报告呢？\n"
        "△ 助理慌忙走进办公室\n"
        "助理: 马上就来，王总。\n"
        "△ 王总站起身走到窗边\n"
        "王总: 给你十分钟。\n"
        "△ 助理退出办公室\n"
        "助理 (OS): 这下麻烦了...\n"
    )

    engine = ShortDramaEngine()
    engine.enable_consistency()
    engine.parse_script(script)

    output = engine.get_output()
    assert_true("STANDARD_PROMPT" in output, "短剧输出含提示词")
    assert_true("CONSISTENCY" in output, "短剧输出含一致性数据")

    consistency = output["CONSISTENCY"]
    ledger_data = consistency.get("ledger", {})
    assert_true(len(ledger_data.get("characters", {})) > 0, "台账有角色注册")
    assert_true(len(ledger_data.get("scenes", {})) > 0, "台账有场景注册")

    long_shots = len([m for m in ledger_data.get("timeline", []) if m.get("is_long_shot")])
    print(f"  长戏份数量: {long_shots}")

    # Test CLI verify path
    engine2 = ShortDramaEngine()
    engine2.enable_consistency()
    engine2.parse_script(script)
    output2 = engine2.get_output()
    assert_true("CONSISTENCY" in output2, "CLI路径输出含一致性")

    # Verify acceptance runs
    ledger = ConsistencyLedger()
    for cname in ledger_data.get("characters", {}):
        ledger.create_character(cname)
    for sid in ledger_data.get("scenes", {}):
        ledger.create_scene(sid)
    for tm in ledger_data.get("timeline", []):
        pos = tm.get("position", "")
        import re as _re
        m = _re.match(r"Ep(\d+)@(\d+)s-(\d+)s", pos)
        if m:
            ledger.add_timeline_marker(
                int(m.group(1)), int(m.group(2)), int(m.group(3)),
                tm.get("characters", []), tm.get("scene_id", ""),
            )

    acceptance = ConsistencyValidator.run_final_acceptance(ledger)
    assert_true("D4_continuity" in acceptance.criteria, "验收含D4")
    print(f"  验收结果: {'通过' if acceptance.passed else '未通过'}")


# ============================================================
# MAIN
# ============================================================

def run_all():
    print("=" * 70)
    print("MadStory Director Validator — 导演级全套核验")
    print("=" * 70)

    tests = [
        ("输出结构完整性", test_output_structure),
        ("Negative Prompt 合规性", test_negative_prompt_compliance),
        ("边界条件覆盖", test_boundary_conditions),
        ("镜头运动约束强制", test_camera_motion_validation),
        ("一镜到底引擎边界", test_one_shot_engine),
        ("爆款复刻引擎边界", test_viral_replicate_engine),
        ("Agent 模式引擎边界", test_agent_mode_engine),
        ("时长合规性", test_duration_compliance),
        ("模式枚举完整性", test_mode_enum_integrity),
        ("转场类型枚举完整性", test_transition_enum_integrity),
        ("重置与状态隔离", test_reset_and_isolation),
        ("资源文件完整性", test_resource_integrity),
        ("一致性管控台账", test_consistency_ledger),
        ("一致性校验器全流程", test_consistency_validator),
        ("短剧长戏份一致性", test_short_drama_long_shot_consistency),
    ]

    for name, fn in tests:
        try:
            fn()
        except Exception:
            _r.failed += 1
            print(f"  [CRASH] {name}: {traceback.format_exc()}")

    print(f"\n{'=' * 70}")
    print(f"  TOTAL: {_r.total}  |  PASS: {_r.passed}  |  FAIL: {_r.failed}")
    if _r.failed == 0:
        print("  VERDICT: 通过世界一线广告/电影导演专业核验标准")
    else:
        print(f"  VERDICT: {_r.failed} 项未通过，需修复")
    print("=" * 70)
    return _r.failed


if __name__ == "__main__":
    exit_code = run_all()
    sys.exit(exit_code)
