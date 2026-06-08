# 案例 1: 电影创意探索 — 《城市孤岛》概念短片
> **Mode**: `creative_film` (Mode 0) | **平台**: Seedance 3.0 | **时长**: 30s | **风格**: 塔可夫斯基式诗意现实主义

## 用户输入 (Raw Input)

```
我想做一个关于"城市里孤独的人"的短视频，要有电影感，不要太俗套的那种。
```

## PPAF 循环执行记录

### Phase 0: Perception (感知) — 意图解析

**LLM Enhanced Intent Parsing:**
```json
{
  "raw_intent": "城市孤独主题，电影感，反套路",
  "detected_emotion": ["孤独", "疏离", "内省"],
  "detected_style": "poetic realism / 塔可夫斯基 / 安哲罗普洛斯",
  "detected_platform": "抖音/B站/艺术展",
  "suggested_duration": 30,
  "complexity_score": 7,
  "mode_recommendation": "creative_film",
  "anti_cliche_directive": true
}
```

### Phase 1: Planning (规划) — Tournament 创意方向生成

引擎并行生成 3 个创意方向，通过评分矩阵筛选：

| 方向 | 导演参照 | 视觉核心 | 情绪弧线 | 评分 |
|------|---------|---------|---------|------|
| A: 雨夜窗景 | 王家卫 | 湿玻璃反射 + 霓虹虚化 | 孤独→温暖(?) | 6.5 |
| B: 地铁长镜头 | 贾樟柯 | 手持跟拍 + 人群流动 | 疏离→融入→疏离 | **8.2** |
| C: 废墟花园 | 塔可夫斯基 | 固定机位 + 光影流转 | 寂静→顿悟 | **8.8** |

**Tournament 结果**: 方向 C 胜出（独特性 + 情感深度最优）

### Phase 2-6: Action (执行) — 分镜推导

#### Shot 1: 开场 — 废墟中的光 (0-8s)
- **STANDARD_PROMPT**: `A solitary figure stands motionless in an abandoned rooftop garden overgrown with wild grass, shafts of golden hour sunlight pierce through broken concrete pillars, dust particles float in slow motion, the figure's silhouette barely visible against the intense backlight, cinematic wide shot, static camera, anamorphic lens flare, muted earth tones with selective color on a single red flower`
- **CAMERA**: Static wide shot (固定广角)
- **MOTION_STRENGTH**: 2
- **LIGHTING**: Natural golden hour backlighting through architectural gaps, high contrast between shadow and light pools
- **TIMELINE**: 0-3s: 全景建立空间感; 3-6s: 尘埃粒子慢浮; 6-8s: 人物剪影微动

#### Shot 2: 中段 — 凝视 (8-18s)
- **STANDARD_PROMPT**: `Close-up of weathered hands holding a small cracked mirror, reflecting fragments of the city skyline beyond the garden fence, shallow depth of field, the reflection shifts subtly as wind moves the mirror angle, warm skin tones against cool blue city background, gentle handheld micro-movements`
- **CAMERA**: Extreme close-up with subtle handheld drift (极近特写+手持微漂)
- **MOTION_STRENGTH**: 3
- **LIGHTING**: Mixed warm (skin/mirror) and cool (city reflection), practical light source from mirror reflection

#### Shot 3: 结尾 — 回归 (18-30s)
- **STANDARD_PROMPT**: `The figure now sits on the edge of the rooftop, legs dangling over the cityscape below, camera slowly pulls back (dolly out) revealing the vast urban landscape at dusk, thousands of windows beginning to glow like stars, the figure becomes smaller but no longer alone in frame — the city itself becomes a companion, final frame holds on this composition`
- **CAMERA**: Slow dolly out (缓慢后拉)
- **MOTION_STRENGTH**: 4
- **LIGHTING**: Magic hour transition to blue hour, city lights gradually illuminating

### Phase 7: Feedback (反思) — 输出与校验

## 完整输出 JSON

```json
{
  "STANDARD_PROMPT": "A cinematic three-shot sequence exploring urban solitude through poetic visual metaphor: [Shot 1] Abandoned rooftop garden, golden hour light through broken concrete, solitary silhouette, static wide shot, anamorphic lens. [Shot 2] Weathered hands holding cracked mirror reflecting city skyline, extreme close-up, shallow DOF, handheld drift. [Shot 3] Figure sitting on rooftop edge, slow dolly out revealing vast dusk cityscape, transition from isolation to cosmic connection.",
  "NEGATIVE_PROMPT": "no generic composition, no cliché visual language, no random style mixing, no emotional disconnect, no flat narrative, no derivative imagery, no shaky camera without motivation, no oversaturated colors, no text overlay, no watermark",
  "TIMELINE": "0-8s: Establishing — space and light; 8-18s: Intimate — detail and texture; 18-30s: Release — scale and connection",
  "CAMERA": "Static wide → ECU handheld → Slow dolly out",
  "MOTION_STRENGTH": 3,
  "DURATION": 30,
  "MODE": "电影创意探索",
  "MODE_KEY": "creative_film",
  "MULTI_MODAL_ADVICE": {
    "reference_images": [
      "Andrei Tarkovsky 'Stalker' — Zone interiors with natural light",
      "Theo Angelopoulos 'Ulysses' Gaze' — long take compositions",
      "Edward Hopper 'Nighthawks' painting — urban isolation mood board"
    ],
    "reference_video": "Last scene of 'Wings of Desire' (1987) — Damiel's transformation sequence for dolly-out reference",
    "audio_suggestion": "Minimal piano + field recording (wind through concrete, distant traffic rumble) — Arvo Pärt 'Spiegel im Spiegel' style"
  },
  "SOUND_DESIGN": {
    "bgm_emotion": "melancholic but hopeful, minimal instrumentation",
    "sync_points": [
      {"time": "8s", "event": "cut", "sound": "sharp intake of breath"},
      {"time": "18s", "event": "dolly starts", "sound": "low drone begins"},
      {"time": "27s", "event": "final frame hold", "sound": "single piano note decay"}
    ],
    "ambient": "urban rooftop ambience — distant traffic, wind, occasional bird"
  },
  "SHOT_LIST": [
    {"shot_id": 1, "duration": 8, "camera": "static_wide", "subject": "figure_silhouette_in_garden"},
    {"shot_id": 2, "duration": 10, "camera": "ecu_handheld", "subject": "hands_mirror_reflection"},
    {"shot_id": 3, "duration": 12, "camera": "dolly_out", "subject": "figure_cityscape"}
  ],
  "CREATIVE_DIRECTIONS": {
    "selected_concept": "C: 废墟花园 (Tarkovsky-inspired)",
    "rejected_concepts": ["A: 雨夜窗景 (too Wong Kar-wai derivative)", "B: 地铁长镜头 (good but less unique)"],
    "emotional_arc": "isolation → intimate detail → cosmic connection",
    "visual_metaphor": "the garden as inner world, the city as outer world, the mirror as bridge"
  },
  "PLATFORM_PARAMS": {
    "platform": "seedance_3.0",
    "adapted_motion_strength": 3,
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  }
}
```

## Quality Checklist

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 输出结构完整性 | PASS | 所有必需字段已填充 |
| 创意探索模式专项 | PASS | 情绪方向明确、反套路约束完整 |
| 参数范围合规 | PASS | DURATION=30, MOTION=3 |

## Harness Engineering 追溯

| 维度 | 记录 |
|------|------|
| Reliability | 所有决策可回溯至 Tournament 评分矩阵 |
| Efficiency | Token 预算 ~2500 tokens (含创意探索开销) |
| Security | 输入过滤通过、输出护栏触发、Negative Prompt 注入完整 |
| Traceability | PPAF 四阶段日志完整保存、质量门禁全通过 |
