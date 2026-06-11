# 提示词工程规范 (Layer 1 — 按需加载)

> 本文件包含提示词结构、Negative Prompt 模板和特殊语法。在生成提示词时加载。

---

## 标准提示词结构 (5 层)
```
[Subject], [Single Action], [Camera Move], [Style & Lighting], [Constraints]
```

## Negative Prompt 按模式注入

**Creative Film (Mode 0):**
```
no generic composition, no cliché visual language, no random style mixing, no emotional disconnect, no flat narrative, no derivative imagery
```

**Ecommerce:**
```
no logo distortion, no text artifacts, no packaging collapse, no duplicate product, no label blur, no warped glass, no cap drift
```

**UGC:**
```
no extra fingers, no face drift, no lip mismatch, no background warping, no product disappearance, no shaky framing, no eye drift
```

**Cinematic:**
```
no shaky camera, no object melting, no random text, no muddy lighting, no flat blacks, no text watermark
```

**Multi-shot:**
```
no character drift between cuts, no scene inconsistency, no transition artifacts, no text watermark
```

**One-Shot:**
```
no abrupt cuts, no spatial discontinuity, no object mutation between frames, no stutter in transitions, no frame-tearing
```

**Viral Replicate:**
```
no style drift from reference, no subject identity loss, no mismatched pacing, no warped replacement subject, no original ghosting
```

**Short Drama:**
```
no character face drift across episodes, no costume inconsistency, no scene discontinuity, no voice mismatch, no subtitle desync
```

## 多镜头语法
- 过渡关键词: `Cut to`(硬切) / `Camera cut to`(机位切换) / `Shot Switch`(场景转场)
- 每段必须包含: 主体 + 动作 + 机位方向
- 格式:
```
[Shot 1: Subject + Action + Camera]
Cut to
[Shot 2: Subject + Action + Camera + New Scene Details]
Cut to
[Shot 3: Subject + Action + Camera]
```

## 一镜到底转场语法 (One-Shot Transition Syntax)
- **输入**: 2-10 张顺序图片
- **转场类型**:
  - `推 (Push)`: 镜头推进，从全景到特写
  - `拉 (Pull)`: 镜头拉远，从特写到全景
  - `螺旋 (Spiral)`: 镜头螺旋变化，中心点保持不变
  - `溶解 (Dissolve)`: 画面叠化过渡
  - `匹配剪辑 (Match Cut)`: 利用画面中的相似元素衔接
  - `甩 (Whip Pan)`: 快速横向甩镜转场
  - `遮挡转场 (Wipe)`: 物体遮挡画面完成转场
  - `AI自动 (Auto)`: 仅设时长，AI 自动生成转场
- **提示词格式**:
```
图片1 → [转场描述: 镜头推进穿过门框, 2.5s] → 图片2 → [转场描述: 螺旋旋转至水晶中心, 3s] → 图片3
```
- **限制**: 2 ≤ 图片数 ≤ 10，总时长建议 15-60s

## 爆款复刻语法 (Viral Replicate Syntax)
- **创意拍摄复刻格式**:
```
参考[@视频1]的快速运镜方式以及创作手法，将[@视频1]的主体更换为[@图片1]，创作成一个类似的[品类]创意拍摄视频
```
- **经典影视还原格式**:
```
复刻[@视频1]的参考视频内容，还原一切细节，但把人物替换成[替换角色描述]
```
- **爆款拆解再生格式**:
```
解析[@视频1]这个视频的爆点原因，并借鉴其文案、主题、画面风格等，重新做一个新视频，[差异化要求]
```

## Agent 模式创作链路
- **模糊意图 → 成片**: 输入自然语言 → 引擎解析主体/风格/时长/情绪 → 自动规划 → 分镜编排 → 提示词输出
- **有脚本 → 成片**: 输入脚本 → 解析台词/场景/角色 → 分镜表生成 → 逐镜提示词
- **有素材 → 成片**: 输入图片/视频/文案 → 素材角色分配 → 组合拳编排 → 输出

## 短剧剧本格式 (Short Drama Script Format)
```
第X集
场景: [场景描述] [时间]
人物: [人物列表]

△ [动作/环境描述]
[人物] (OS): [内心独白]
[人物]: [对白]
```

## 一致性管控 (Consistency Protocol)

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
当输出出现漂移时，按以下顺序排查:
1. 是否定义了不变要素？
2. 当前 Mode 是否过于开放？
3. 镜头运动是否过于激进？
4. 主体在画面中是否过小？
5. 多个 Reference 是否存在冲突？

> **Seedream 4.x/5.x 图片模式**: 当检测到用户使用 Seedream 平台或需要图片生成时，加载 `references/seedream_4x_rules.md` 获取图片模式提示词结构、文字渲染、图像编辑、参考图生图、多图输入/输出语法。图片模式不适用本文件的 5 层结构和 Negative Prompt。
