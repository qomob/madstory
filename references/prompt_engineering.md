# 提示词工程规范 (Layer 1 — 按需加载)

> 本文件包含提示词结构概要和 Negative Prompt 索引。**完整平台规范见 `references/seedance_v2_rules.md`**——本文件仅提供快速查阅的结构骨架，避免与平台规范重复。

---

## 标准提示词结构 (5 层)
```
[Subject], [Single Action], [Camera Move], [Style & Lighting], [Constraints]
```

## Negative Prompt 索引

> 完整定义、使用场景和每条护栏的原理见 `references/seedance_v2_rules.md` §3。

| 模式 | 核心护栏关键词 |
|------|--------------|
| Creative Film | generic composition, cliché visual language, derivative imagery |
| Ecommerce | logo distortion, packaging collapse, label blur, warped glass |
| UGC | extra fingers, face drift, lip mismatch, product disappearance |
| Cinematic | shaky camera, object melting, muddy lighting, flat blacks |
| Multi-shot | character drift between cuts, scene inconsistency, transition artifacts |
| One-Shot | abrupt cuts, spatial discontinuity, object mutation, stutter |
| Viral Replicate | style drift, subject identity loss, mismatched pacing, original ghosting |
| Short Drama | character face drift across episodes, costume inconsistency, voice mismatch |

## 特殊语法索引

> 以下语法的完整格式、限制条件和使用示例见 `references/seedance_v2_rules.md` 对应章节。

| 语法 | 参考章节 | 用途 |
|------|---------|------|
| 多镜头叙事语法 | §6 | `Cut to` / `Camera cut to` / `Shot Switch` + 每段格式 |
| 一镜到底转场语法 | §12 | 推/拉/螺旋/溶解/匹配剪辑/甩/遮挡/AI自动 + 提示词格式 |
| 爆款复刻语法 | §13 | 创意拍摄/经典影视/爆款拆解三种策略的提示词模板 |
| Agent 模式创作链路 | §14 | 模糊意图/有脚本/有素材三种输入路径 |
| 短剧剧本格式 | §15 | 第X集/场景:/人物:/△/(OS) 标准格式 |

## 一致性管控 (Consistency Protocol)

> 完整规约见 `references/seedance_v2_rules.md` §7。

### 不变性清单 (Invariants)
进入分镜推导前，锁定以下不可变要素（根据 Mode 选择）:
- 人脸身份 (UGC)
- 产品几何 (Ecommerce)
- 手部姿态 (UGC / Ecommerce 手持)
- 服装造型 (UGC / Cinematic 角色)
- 场景光位 (Cinematic / Multi-shot)
- 色彩调性 (所有 Mode，跨镜头一致)

### 模式选择决策树
```
需要概念探索 → Text-to-Video
需要首帧锁定 → Image-to-Video
需要身份/产品锁定 → Reference-to-Video
```

### 一致性调试规约
当输出出现漂移时，按以下顺序排查（完整版见 `seedance_v2_rules.md` §7.2）:
1. 是否定义了不变要素？ → 2. 当前 Mode 是否过于开放？ → 3. 镜头运动是否过于激进？ → 4. 主体在画面中是否过小？ → 5. 多个 Reference 是否存在冲突？

> **Seedream 4.x/5.x 图片模式**: 当检测到用户使用 Seedream 平台或需要图片生成时，加载 `references/seedream_4x_rules.md` 获取图片模式提示词结构、文字渲染、图像编辑、参考图生图、多图输入/输出语法。图片模式不适用本文件的 5 层结构和 Negative Prompt。
