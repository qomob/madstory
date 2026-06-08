# 案例 2: 多镜头叙事 — 《最后一班地铁》
> **Mode**: `multi_shot` (Mode 4) | **平台**: Runway Gen-3 | **时长**: 24s (4 shots x 6s) | **风格**: 新黑色电影 / 高对比度

## 用户输入 (Raw Input)

```
做一个关于"深夜末班车"的多镜头短视频，要有悬疑感，4个镜头，每个6秒。
```

## PPAF 循环执行记录

### Phase 0: Perception (感知)

```json
{
  "raw_intent": "深夜末班车，悬疑感，多镜头",
  "detected_emotion": ["紧张", "孤独", "不安"],
  "detected_style": "neo-noir / high contrast / Michael Mann",
  "mode": "multi_shot",
  "shot_count": 4,
  "duration_per_shot": 6
}
```

### Phase 1-6: Action (执行) — 4 镜头序列

## 完整输出 JSON

```json
{
  "STANDARD_PROMPT": "Four-shot neo-noir sequence depicting the last subway train at midnight: [Shot 1] Empty subway platform at night, fluorescent lights flickering, a single figure's shadow stretches across wet tiles, high-contrast chiaroscuro lighting, static wide shot. [Shot 2] Train arrives — blur of light through platform glass doors, motion streaks, reflection of waiting figure in the train window as doors open, medium shot with slight push-in. [Shot 3] Inside the nearly empty car, overhead handrails create geometric shadows on faces, one passenger sits alone reading, another stands by the door staring into darkness outside, slow pan across interior. [Shot 4] Train departs into tunnel — lights recede into perspective vanishing point, platform empties again but something small left behind (a dropped object?), final frame on empty platform.",
  "NEGATIVE_PROMPT": "no shaky camera, no object melting, no random text, no muddy lighting, no flat blacks, no text watermark, no bright daylight, no cheerful colors, no crowd, no oversaturation",
  "TIMELINE": "0-6s: Platform establish; 6-12s: Arrival; 12-18s: Interior; 18-24s: Departure + reveal",
  "CAMERA": [
    {"shot": 1, "move": "static_wide", "strength": 1},
    {"shot": 2, "move": "push_in", "strength": 3},
    {"shot": 3, "move": "slow_pan", "strength": 2},
    {"shot": 4, "move": "static_telephoto", "strength": 1}
  ],
  "MOTION_STRENGTH": [1, 3, 2, 1],
  "DURATION": 24,
  "MODE": "多镜头叙事",
  "MODE_KEY": "multi_shot",
  "MULTI_MODAL_ADVICE": {
    "reference_images": [
      "Michael Mann 'Collateral' — night driving/urban scenes",
      "Se7en (1995) — urban noir color palette reference",
      "Edward Hopper 'Automat' — solitary figure in artificial light"
    ],
    "audio_suggestion": "Low-frequency drone + mechanical hum (subway) + distant metallic echoes"
  },
  "SOUND_DESIGN": {
    "bgm_emotion": "tense, minimal, industrial",
    "sync_points": [
      {"time": "6s", "event": "train arrival", "sound": "low rumble builds"},
      {"time": "12s", "event": "doors open", "sound": "hiss + ding"},
      {"time": "18s", "event": "doors close", "sound": "thud"},
      {"time": "22s", "event": "train leaves", "sound": "fade to silence"}
    ]
  },
  "SHOT_LIST": [
    {"shot_id": 1, "duration": 6, "camera": "static_wide", "transition": "hard_cut", "subject": "empty_platform_shadow"},
    {"shot_id": 2, "duration": 6, "camera": "medium_push_in", "transition": "hard_cut", "subject": "train_arrival_reflection"},
    {"shot_id": 3, "duration": 6, "camera": "interior_pan", "transition": "hard_cut", "subject": "car_interior_geometric"},
    {"shot_id": 4, "duration": 6, "camera": "static_telephoto", "transition": "hold", "subject": "departure_reveal"}
  ],
  "CUT_LOGIC": [
    {"from": 1, "to": 2, "reason": "action_match — train arrival is the event that bridges platform to train"},
    {"from": 2, "to": 3, "reason": "POV shift — from watching train arrive to being inside it"},
    {"from": 3, "to": 4, "reason": "spatial_exit — leaving the confined space back to openness"},
    {"from": 4, "to": null, "reason": "narrative pause — empty platform with mystery object creates lingering question"}
  ],
  "PLATFORM_PARAMS": {
    "platform": "runway_gen3",
    "adapted_motion_bucket_id": "medium",
    "max_duration_per_clip": 10,
    "resolution": "1080p"
  }
}
```

## Quality Checklist

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 输出结构完整性 | PASS | 所有必需字段已填充 |
| 多镜头模式专项 | PASS | Cut logic 清晰、每镜头运动单一 |
| 参数范围合规 | PASS | DURATION=24, MOTION range=[1,3] |

## 导演级备注

本案例展示了 **Cut Logic（剪辑逻辑）** 的完整推导——每个转场都有明确的叙事动机，而非随意切换。这是电影级分镜与广告级分镜的核心差异：广告追求注意力抓取，电影追求叙事连贯性。
