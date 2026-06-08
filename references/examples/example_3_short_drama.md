# 案例 3: 短剧生产 — 《时间当铺》第3集
> **Mode**: `short_drama` (Mode 8) | **平台**: Seedance 2.0 | **时长**: 45s (3 scenes) | **类型**: 悬疑/奇幻短剧

## 用户输入 (Raw Input)

```
剧本如下：

【场景1】时间当铺内。老板（中年男子，穿旧西装）把一块怀表推到柜台对面。"你的时间，我收了。" 年轻女子颤抖着手去拿，怀表突然自己转了起来。

【场景2】女子家。她看着怀表，表盘上的数字在倒计时。她冲到窗边，外面是同一个夜晚，但街道上空无一人。所有钟表都停在12点。

【场景3】当铺外。女子跑回来砸门。门开了，里面是一片废墟。她低头看怀表——秒针刚好归零。她的身体开始像老照片一样褪色。
```

## PPAF 循环执行记录

### Phase 0: Perception — 剧本解析

```json
{
  "raw_intent": "悬疑奇幻短剧，时间循环主题",
  "detected_genre": "fantasy thriller / time loop / supernatural",
  "character_count": 2,
  "scene_count": 3,
  "total_duration_estimate": 45,
  "key_props": ["怀表（pocket watch）", "旧柜台", "窗户"],
  "visual_style_reference": "dark fantasy + film noir elements",
  "consistency_requirements": ["pocket_watch_appearance", "female_protagonist_look", "shop_interior_continuity"]
}
```

### 一致性管控台账 (Consistency Ledger)

| 约束项 | 值 | 跨场景锁定 |
|--------|-----|-----------|
| 怀表外观 | 古铜色外壳, 白色珐琅表盘, 黑色罗马数字 | SCENE 1 = SCENE 2 = SCENE 3 |
| 女主外观 | 20-25岁, 长发(黑色), 浅色上衣, 焦虑表情 | SCENE 1 = SCENE 2 = SCENE 3 |
| 当铺内部 | 深色木柜, 黄昏光线, 尘埃微粒 | SCENE 1 ↔ SCENE 3 (对比: 正常→废墟) |
| 时间色调 | SCENE1暖黄 → SCENE2冷蓝 → SCENE3灰白(褪色感) | 渐进式色调变化 |

## 完整输出 JSON

```json
{
  "STANDARD_PROMPT": "Three-scene supernatural short drama 'The Time Pawnshop' Episode 3: [SCENE 1 - 15s] Interior of a dusty antique pawnshop, warm amber light through grimy windows, middle-aged shopkeeper in worn suit pushes an antique bronze pocket watch across dark wood counter toward a young woman in her 20s with long black hair wearing a pale blouse, her hand trembles reaching for it, the pocket watch suddenly begins ticking on its own, close-up on the watch face with Roman numerals glowing faintly, shallow depth of field. [SCENE 2 - 15s] The woman's apartment at night, she holds the same bronze pocket watch — its hands spinning backwards counting down, she rushes to the window revealing the same nighttime street but completely empty, all visible clocks frozen at 12:00, cold blue moonlight, expression of dawning horror. [SCENE 3 - 15s] Exterior of the pawnshop — she pounds on the door desperately clutching the watch, door creaks open revealing not the shop interior but ruins and rubble inside, she looks down at the watch — second hand hits zero, her figure begins to desaturate and fade like an old photograph losing color, final frame half-faded.",
  "NEGATIVE_PROMPT": "no modern objects in pawnshop, no bright colors, no cheerful lighting, no text artifacts, no logo distortion, no inconsistent character appearance across scenes, no watch design change between scenes, no color palette inconsistency",
  "TIMELINE": "SCENE1 (0-15s): Transaction + supernatural trigger; SCENE2 (15-30s): Discovery + escalation; SCENE3 (30-45s): Confrontation + climax/fade",
  "CAMERA": [
    {"scene": 1, "shot": "over_shoulder_two_shot → CU_watch", "move": "slow_push_in"},
    {"scene": 2, "shot": "medium_wide_window → CU_face", "move": "handheld_anxious"},
    {"scene": 3, "shot": "exterior_medium → CU_watch_fade", "move": "static_ominous"}
  ],
  "MOTION_STRENGTH": [3, 4, 2],
  "DURATION": 45,
  "MODE": "短剧创作",
  "MODE_KEY": "short_drama",
  "SCRIPT_PARSE_RESULT": {
    "scenes_parsed": 3,
    "characters_detected": ["老板(shopkeeper)", "年轻女子(protagonist)"],
    "key_props_locked": ["pocket_watch_bronze_roman"],
    "emotional_arc": "tense_transaction → horrified_discovery → tragic_fade"
  },
  "CONSISTENCY_LEDGER": {
    "pocket_watch": {"lock_id": "prop_001", "description": "bronze case, white enamel dial, black Roman numerals", "scenes": [1, 2, 3]},
    "protagonist": {"lock_id": "char_001", "description": "woman 20-25y, long black hair, pale top, anxious demeanor", "scenes": [1, 2, 3]},
    "color_progression": {"scene_1": "warm_amber", "scene_2": "cold_blue", "scene_3": "desaturated_grey"}
  },
  "MULTI_MODAL_ADVICE": {
    "reference_images": [
      "Pan's Labyrinth (2006) — pale fantasy aesthetic for fade effect",
      "The Pawnbroker (1964) — dim interior pawnshop reference",
      "Donnie Darko — liquid/supernatural time visual motif"
    ],
    "character_reference": "需要提供女主和老板的参考照片以确保跨场景一致性",
    "prop_reference": "需要提供古董怀表的参考图片（正面+侧面）"
  },
  "SOUND_DESIGN": {
    "bgm_emotion": "SCENE1: tense strings; SCENE2: low drone + clock ticking; SCENE3: silence + single tone decay",
    "sync_points": [
      {"time": "12s", "event": "watch starts ticking", "sound": "loud tick against silence"},
      {"time": "22s", "event": "empty street reveal", "sound": "all ambient sound cuts out abruptly"},
      {"time": "35s", "event": "door opens to ruins", "sound": "creak + wind howl"},
      {"time": "43s", "event": "fade begins", "sound": "music box slowing down"}
    ]
  },
  "SHOT_LIST": [
    {"scene": 1, "shot_id": 1, "duration": 8, "camera": "two_shot_over_counter", "subject": "shopkeeper_woman_transaction"},
    {"scene": 1, "shot_id": 2, "duration": 7, "camera": "CU_watch_glowing", "subject": "pocket_watch_self_activating"},
    {"scene": 2, "shot_id": 3, "duration": 8, "camera": "medium_woman_window", "subject": "woman_discovers_empty_street"},
    {"scene": 2, "shot_id": 4, "duration": 7, "camera": "CU_face_horror", "subject": "woman_horrified_expression"},
    {"scene": 3, "shot_id": 5, "duration": 8, "camera": "exterior_woman_door", "subject": "woman_desperate_at_door"},
    {"scene": 3, "shot_id": 6, "duration": 7, "camera": "CU_fade_effect", "subject": "woman_fading_like_photo"}
  ],
  "PLATFORM_PARAMS": {
    "platform": "seedance_2.0",
    "adapted_motion_strength": 3,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "notes": "每场景需单独生成后剪辑合成，一致性通过 CONSISTENCY_LEDGER 锁定关键元素"
  }
}
```

## Quality Checklist

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 输出结构完整性 | PASS | 所有必需字段已填充 |
| 短剧模式专项 | PASS | 剧本解析完整、一致性台账建立、角色/道具锁定 |
| 参数范围合规 | PASS | DURATION=45, MOTION range=[2,4] |

## Harness Engineering 追溯

| 维度 | 记录 |
|------|------|
| Reliability | 一致性台账确保跨场景元素可追溯可重放 |
| Efficiency | 结构化剧本解析减少 LLM 循环次数 |
| Security | Negative Prompt 包含跨场景一致性约束 |
| Traceability | 每个 shot 都有 scene_id + shot_id 双索引，支持精确定位 |
