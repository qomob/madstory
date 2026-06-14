# 案例 1: 电影创意探索 — 《城市孤岛》概念短片
> **Mode**: `creative_film` (Mode 0) | **平台**: Seedance 3.0 | **时长**: 30s | **风格**: 塔可夫斯基式诗意现实主义

## 用户输入 (Raw Input)

```
我想做一个关于"城市里孤独的人"的短视频，要有电影感，不要太俗套的那种。
```

## 分镜推导过程

### 创意方向筛选

引擎并行生成 3 个创意方向，通过评分矩阵筛选：

| 方向 | 导演参照 | 视觉核心 | 情绪弧线 | 评分 |
|------|---------|---------|---------|------|
| A: 雨夜窗景 | 王家卫 | 湿玻璃反射 + 霓虹虚化 | 孤独→温暖(?) | 6.5 |
| B: 地铁长镜头 | 贾樟柯 | 手持跟拍 + 人群流动 | 疏离→融入→疏离 | 8.2 |
| C: 废墟花园 | 塔可夫斯基 | 固定机位 + 光影流转 | 寂静→顿悟 | **8.8** |

**选定方向**: C（独特性 + 情感深度最优）

### Shot 1: 开场 — 废墟中的光 (0-8s)
- **STANDARD_PROMPT**: `A solitary figure stands motionless in an abandoned rooftop garden overgrown with wild grass, shafts of golden hour sunlight pierce through broken concrete pillars, dust particles float in slow motion, the figure's silhouette barely visible against the intense backlight, cinematic wide shot, static camera, anamorphic lens flare, muted earth tones with selective color on a single red flower`
- **CAMERA**: Static wide shot (固定广角)
- **MOTION_STRENGTH**: 2
- **LIGHTING**: Natural golden hour backlighting through architectural gaps, high contrast between shadow and light pools

### Shot 2: 中段 — 凝视 (8-18s)
- **STANDARD_PROMPT**: `Close-up of weathered hands holding a small cracked mirror, reflecting fragments of the city skyline beyond the garden fence, shallow depth of field, the reflection shifts subtly as wind moves the mirror angle, warm skin tones against cool blue city background, gentle handheld micro-movements`
- **CAMERA**: Extreme close-up with subtle handheld drift
- **MOTION_STRENGTH**: 3
- **LIGHTING**: Mixed warm (skin/mirror) and cool (city reflection)

### Shot 3: 结尾 — 回归 (18-30s)
- **STANDARD_PROMPT**: `The figure now sits on the edge of the rooftop, legs dangling over the cityscape below, camera slowly pulls back (dolly out) revealing the vast urban landscape at dusk, thousands of windows beginning to glow like stars, the figure becomes smaller but no longer alone in frame — the city itself becomes a companion, final frame holds on this composition`
- **CAMERA**: Slow dolly out (缓慢后拉)
- **MOTION_STRENGTH**: 4
- **LIGHTING**: Magic hour transition to blue hour, city lights gradually illuminating

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
  "MULTI_MODAL_ADVICE": "参考图: Tarkovsky Stalker Zone interiors / Theo Angelopoulos long take compositions / Edward Hopper Nighthawks mood board\n参考视频: Wings of Desire (1987) dolly-out sequence\n音频建议: Minimal piano + field recording — Arvo Pärt style",
  "SOUND_DESIGN": "melancholic but hopeful minimal instrumentation; ambient urban rooftop atmosphere",
  "SHOT_LIST": [
    {"shot_id": 1, "duration": 8, "camera": "static_wide", "subject": "figure_silhouette_in_garden"},
    {"shot_id": 2, "duration": 10, "camera": "ecu_handheld", "subject": "hands_mirror_reflection"},
    {"shot_id": 3, "duration": 12, "camera": "dolly_out", "subject": "figure_cityscape"}
  ]
}
```

## Quality Checklist

| 检查项 | 状态 |
|--------|------|
| 输出结构完整性 | PASS |
| 创意探索模式专项（情绪方向/反套路） | PASS |
| 参数范围合规 (DURATION=30, MOTION=3) | PASS |
