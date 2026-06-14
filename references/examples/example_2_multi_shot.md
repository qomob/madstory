# 案例 2: 多镜头叙事 — 咖啡品牌故事
> **Mode**: `multi_shot` (Mode 4) | **平台**: Runway Gen-3 | **时长**: 3 shots × 5s = 15s

## 用户输入

```
为一个精品咖啡品牌做一支15秒品牌广告，要有温度感，重点展示咖啡豆到杯子的过程。
```

## 分镜方案

### Shot 1 (0-5s)
- **画面**: 咖啡农的手采摘成熟的红樱桃咖啡果，晨光穿过树叶洒在手上，清晰可见的露珠和果实色泽
- **景别**: 特写
- **运镜**: 缓推
- **光影**: 暖金色晨光 (Golden Hour)

### Shot 2 (5-10s)
- **画面**: 新鲜烘焙的咖啡豆从烘焙机中倾泻而出，热气腾腾，近距离展示豆子的油亮表面和色泽
- **景别**: 极近特写
- **运镜**: 微距跟踪
- **光影**: 暖黄工业光

### Shot 3 (10-15s)
- **画面**: 手冲咖啡水流穿过咖啡粉，琥珀色液体滴入杯中，背景虚化中隐约可见咖啡农的微笑
- **景别**: 俯拍特写转中景
- **运镜**: 垂直俯拍到缓拉
- **光影**: 侧逆光突出液体通透感

## 完整输出 JSON

```json
{
  "STANDARD_PROMPT": "[Shot 1] Hands of a coffee farmer picking ripe red cherries, golden morning light filtering through leaves, dewdrops and fruit texture clearly visible, macro extreme close-up, slow push-in, cinematic warm tones. [Shot 2] Freshly roasted coffee beans cascading from roaster, steam rising, oily surfaces glistening, extreme close-up, macro tracking shot, warm industrial lighting. [Shot 3] Pour-over coffee stream through grounds, amber liquid dripping into glass carafe, farmer's smile softly visible in bokeh background, top-down macro to mid-length slow pull-out, side-backlight highlighting liquid translucency.",
  "NEGATIVE_PROMPT": "no inconsistent lighting between shots, no drift in color grading, no mismatch in product appearance, no jumpy transitions, no flat blacks",
  "TIMELINE": "0-5s: Farm harvest; 5-10s: Roasting process; 10-15s: Final brewing",
  "CAMERA": "Slow push-in → Macro tracking → Top-down pull-out",
  "MOTION_STRENGTH": 4,
  "DURATION": "5+5+5=15s",
  "MODE": "多镜头叙事",
  "MODE_KEY": "multi_shot",
  "MULTI_MODAL_ADVICE": "统一色温: 暖色调贯穿三镜头; 建议上传参考图确保咖啡豆/杯具的品牌一致性",
  "SOUND_DESIGN": "Acoustic guitar + ambient farm nature sounds → roasting crackle → pour-over drip",
  "SHOT_LIST": [
    {"shot_id": 1, "duration": "5s", "scene": "coffee_farm_harvest", "focus": "hands_and_cherries"},
    {"shot_id": 2, "duration": "5s", "scene": "roasting_facility", "focus": "beans_cascading"},
    {"shot_id": 3, "duration": "5s", "scene": "brew_bar", "focus": "pour_over_drip"}
  ]
}
```

## Quality Checklist

| 检查项 | 状态 |
|--------|------|
| 镜头数量 ≤ 3 | PASS (3 shots) |
| 跨镜头风格一致 | PASS (统一暖色调) |
| Negative Prompt 完整 | PASS |
| 单镜头单运动原则 | PASS |
