# 提示词工程规范 (Layer 1 — 按需加载)

> 本文件包含提示词结构概要、专项公式索引和 Negative Prompt 索引。**完整平台规范见 `references/seedance_25_rules.md`（2.5 默认基准）/ `references/seedance_v2_rules.md`（2.0 降级）**——本文件仅提供快速查阅的结构骨架，避免与平台规范重复。

---

## 标准提示词结构（4 段式主公式）

> 2.5 默认基准。完整说明见 `references/seedance_25_rules.md` §2.1。

```
完整提示词 = 【素材描述】+【一句话概述】+【具体情节描述】+【全局补充（结尾）】
```

| 段落 | 回答 | 要点 |
|------|------|------|
| 素材描述 | 哪个素材是什么？ | 素材编号(按上传顺序) + 具体用途(人物/音色/动作/场景)。无素材可省略 |
| 一句话概述 | 整体拍什么？ | 主体 + 地点 + 事件 + 题材/风格 + 特殊运镜 |
| 具体情节描述 | 每段发生什么？ | 分时间轴/故事线。每段含 ➕正向(画面+运镜+动作+台词+音效) + ➖反向(不要的元素) |
| 全局补充（结尾） | 贯穿始终的约束 | 机位 + 环境/场景特征 + 整体声音/氛围 + 光影；全局禁止项(字幕/bgm/崩坏点)再次强调 |

> 降级 2.0 时：4 段式主体结构兼容，但参考素材上限收紧（9 图/3 视频/3 音频），且 2.5 专项能力（时间戳/编辑/白模等）不可用。

## 专项公式索引

> 以下公式的完整格式、要点和使用示例见 `references/seedance_25_rules.md` 对应章节。专项场景必须用对应公式替代基础 4 段式。

| 场景 | 公式 | 参考章节 | 适用 Mode |
|------|------|---------|----------|
| 真人人物描写 | 7 维公式（年龄种族+肤色质感+面部特征+眼神+发型发色+服装质感+体型气质） | §2.2 | 2/3/6/8（含真人） |
| 30s 长视频 | 3 模块公式（多模态参考层+全局设定+时间戳剧本分镜） | §2.3 | 0/3/4/5/8（30s 长叙事） |
| 超长视频(30-180s) | 超长公式（全局参数+素材描述+一句话概述+具体情节+全局补充） | §2.4 | 4（超长叙事） |
| 视频延长(≤60s) | 延长公式（一镜到底延长 / 切镜转场延长） | §2.5 | 4/5（续拍加长） |
| 智能编辑 | 编辑公式（智能编辑文字 / 高级编辑圈选标记） | §2.6 | 9（局部修改） |
| 白模预演 | 白模公式（粗颗粒度 / 细颗粒度） | §2.7 | 10（3D 预演） |
| 时间戳控制 | 时间切片公式（秒级/帧级） | §3 | 长视频/多镜头/卡点 |
| 音色参考 | `参考@音频1说XX，并保持[语调]` | §4.3 | 2/8（音色锁定） |
| 多语种 | 强制语言输出 | §4.5 | 出海/本土化 |
| 绿幕编辑 | `将背景替换为[场景描述]` | §5 能力 13 | 6/9（绿幕合成） |

## 5 层元素检查清单（降级为校验）

> 原 5 层结构（Subject→Action→Camera→Style→Constraints）不再作为输出主结构，降级为每个分镜的元素完整性校验。输出主结构使用 4 段式。完整清单见 `references/seedance_25_rules.md` §2.8。

- [ ] **Subject**：主体明确且可识别？
- [ ] **Single Action**：单一动作/信息点（一个镜头 ≤ 1 个主导运动）？
- [ ] **Camera Move**：镜头运动 ≤ 1 个主导方式？
- [ ] **Style & Lighting**：风格光影明确？
- [ ] **Constraints**：禁止项已声明？

## Negative Prompt 索引

> 2.5 用"禁止"表述响应更好；2.0 用 `no xxx`。完整定义、使用场景和原理见 `references/seedance_25_rules.md` §7（2.5）/ `references/seedance_v2_rules.md` §3（2.0）。

| 模式 | 核心护栏关键词（2.5 禁止 / 2.0 no） |
|------|----------------------------------|
| Creative Film | 禁止模板化构图 / generic composition, cliché visual language, derivative imagery |
| Ecommerce | 禁止 logo 变形、包装塌陷、标签模糊、产品复制 / logo distortion, packaging collapse, label blur, warped glass |
| UGC | 禁止人脸漂移、多余手指、唇部不匹配、产品消失 / extra fingers, face drift, lip mismatch, product disappearance |
| Cinematic | 禁止镜头抖动、物体融化、随机文字、浑浊光影、死黑 / shaky camera, object melting, muddy lighting, flat blacks |
| Multi-shot | 禁止跨镜头角色漂移、场景不一致、转场瑕疵 / character drift between cuts, scene inconsistency, transition artifacts |
| One-Shot | 禁止硬切、空间断裂、物体变异、跳帧 / abrupt cuts, spatial discontinuity, object mutation, stutter |
| Viral Replicate | 禁止风格偏离、主体身份丢失、节奏不匹配 / style drift, subject identity loss, mismatched pacing, original ghosting |
| Smart Edit | 禁止误伤保留要素、残留伪影、补全不完整 / no unintended modification of preserved elements, no residual artifacts |
| White Model | 禁止四肢僵化、坐标线伪影、模型与渲染主体不匹配 / no rigidity in limb animation, no coordinate line artifacts |
| Short Drama | 禁止跨集角色面部漂移、服装混乱、场景跳跃、配音不匹配 / character face drift across episodes, costume inconsistency, voice mismatch |

### 全局禁止项（2.5 放全局补充段）

```
禁止生成字幕、禁止生成 BGM、禁止[容易崩坏点，如：流鼻涕/眼泪提前滴落/夸张哭腔]
```

## 特殊语法索引

> 2.5 语法见 `references/seedance_25_rules.md`；2.0 语法见 `references/seedance_v2_rules.md` 对应章节。

| 语法 | 2.5 参考 | 2.0 参考 | 用途 |
|------|---------|---------|------|
| 多镜头叙事 | §5 能力 16 + §3 时间戳 | §6 | `Cut to` / `Camera cut to` / `Shot Switch` + 每段格式 |
| 一镜到底转场 | §6 转场表 | §12 | 推/拉/螺旋/溶解/匹配剪辑/甩/遮挡/AI自动 |
| 爆款复刻 | §5 能力 8 迁移创意 | §13 | 创意拍摄/经典影视/爆款拆解三种策略 |
| Agent 模式 | §9 模式专项策略 | §14 | 模糊意图/有脚本/有素材三种输入路径 |
| 短剧剧本 | §9 + §4.4 多人参考 | §15 | 第X集/场景:/人物:/△/(OS) 标准格式 |
| 多模态参考 | §4（@标签绑定/50素材/音色/多人） | §7 一致性管控 | @图片/@视频/@音频 绑定到具体 beat |
| 视频延长 | §2.5 + §6 转场表 | - | 一镜到底延长 / 切镜转场延长 |
| 智能编辑 | §2.6 | - | 文字描述 / 圈选标记+文字 |
| 白模控制 | §2.7 | - | 粗颗粒度 / 细颗粒度 |
| 时间戳控制 | §3 | - | 秒级/帧级精准导戏 |

## 一致性管控 (Consistency Protocol)

> 完整规约见 `references/seedance_v2_rules.md` §7。2.5 在跨镜头一致性上显著改善（见 `seedance_25_rules.md` §8），但仍需多次生成取最佳。

### 不变性清单 (Invariants)
进入分镜推导前，锁定以下不可变要素（根据 Mode 选择）:
- 人脸身份 (UGC / Short Drama)
- 产品几何 (Ecommerce)
- 手部姿态 (UGC / Ecommerce 手持)
- 服装造型 (UGC / Cinematic 角色 / Short Drama)
- 场景光位 (Cinematic / Multi-shot)
- 色彩调性 (所有 Mode，跨镜头一致)
- 保留要素声明 (Smart Edit — 缺则不合格)

### 模式选择决策树
```
需要概念探索 → Text-to-Video
需要首帧锁定 → Image-to-Video
需要身份/产品锁定 → Reference-to-Video
需要修改已有视频 → 智能编辑（2.5 专属）
需要 3D 分镜预演 → 白模控制（2.5 专属）
需要超长叙事 → 超长视频模式（2.5 专属，30-180s）
需要续拍加长 → 视频延长（2.5 专属，≤60s）
```

### 一致性调试规约
当输出出现漂移时，按以下顺序排查（完整版见 `seedance_v2_rules.md` §7.2）:
1. 是否定义了不变要素？ → 2. 当前 Mode 是否过于开放？ → 3. 镜头运动是否过于激进？ → 4. 主体在画面中是否过小？ → 5. 多个 Reference 是否存在冲突？ → 6. (2.5) 多人场景是否用了多人参考？

> **Seedream 4.x/5.x 图片模式**: 当检测到用户使用 Seedream 平台或需要图片生成时，加载 `references/seedream_4x_rules.md` 获取图片模式提示词结构、文字渲染、图像编辑、参考图生图、多图输入/输出语法。图片模式不适用本文件的 4 段式/5 层检查清单和 Negative Prompt。
