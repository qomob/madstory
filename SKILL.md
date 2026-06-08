---
name: mad-story
description: >-
  广告级影视分镜设计引擎，专为 Seedance 2.0 深度定制。支持 8 种创作模式：电商产品展示、
  UGC 原生广告、电影感品牌短片、多镜头叙事、一镜到底、爆款复刻、Agent 全链路创作、短剧批量生产。
  提供从一句话到专业分镜提示词的完整推导流程，内置 Seedance 2.0 参数优化、Negative Prompt
  自动注入、一致性管控和导演级预检。当用户提到 MadStory、影视分镜、分镜设计、广告分镜、电商视频、
  UGC 广告、品牌短片、多镜头叙事、一镜到底、爆款复刻、Agent 模式、短剧创作、从一句话出片、
  制作短视频、AI 视频生成、生成视频提示词，或任何涉及 Seedance 分镜创作的需求时，务必使用此技能。
version: 2.0.0
author: qomob.ai
license: MIT
platforms:
  - Trae IDE
  - OpenClaw
  - Dify
  - Coze
  - Claude Desktop / MCP
runtime:
  python: ">=3.8"
  dependencies:
    core: []
    api: [fastapi, uvicorn, pydantic]
entry_point: scripts/mad_story_engine.py
api_server: scripts/api_server.py
batch_runner: scripts/batch_runner.py
validator: scripts/director_validator.py
---
# MadStory — 广告级影视分镜技能 (Seedance 2.0 驱动)

## 技能定位
MadStory 是面向商业广告与影视创作的专业分镜设计引擎，专为 Seedance 2.0 的广告生产能力深度定制。它以 "Brief in, Ads out" 为核心理念，将广告创作的第一性原理——用内容为消费者创造意义感——转化为可执行的、符合 Seedance 2.0 底层逻辑的工业级分镜方案。

- **触发词**: `MadStory`, `影视分镜`, `分镜设计`, `制作广告分镜`, `电商视频`, `UGC广告`, `品牌短片`, `多镜头叙事`, `一镜到底`, `爆款复刻`, `小云雀`, `Agent模式`, `短剧创作`, `从一句话出片`
- **目标用户**: 广告导演、创意总监、电商运营、品牌营销、内容创作者、短剧制作人、社交媒体运营、零基础创作者
- **默认时长**: 15 秒 / 镜头，支持多镜头序列和长视频 (>1 min)
- **核心能力**: 广告模式切换、一镜到底转场编排、爆款复刻引擎、Agent 全链路创作、短剧批量生产、分镜结构化推导、提示词工程优化、一致性管控、多镜头叙事编排

## 用户能力分级与模式映射

| 能力层级 | 适用角色 | 推荐模式 | 使用路径 |
|---------|---------|---------|---------|
| **L1 入门** | 零基础创作者、电商运营新人、社交媒体小白 | `agent_mode` | 输入一句话 → Agent 自动拆解意图 → 生成分镜方案。无需理解镜头术语。 |
| **L2 基础** | 内容创作者、电商运营、营销专员 | `ecommerce` / `ugc` | 选择模式 → Phase 0-7 填空式引导 → 由引擎提供选项卡片 |
| **L3 进阶** | 创意策划、资深运营、初级导演 | `multi_shot` / `one_shot` / `viral_replicate` | 手动编排多镜头序列 / 转场设计 / 爆款策略选择 |
| **L4 专业** | 广告导演、创意总监、品牌营销负责人 | `cinematic` / `short_drama` | 全参数可控，自定义 Negative Prompt，多剧集批量生产 |
| **L5 导演级** | 资深导演、技术美术、后期总监 | 所有模式 + CLI 批量 | `--interactive` / `--output` / `--validate` CLI 全链路，session 持久化 |

**能力成长路径**: L1(入门) → L2(基础) → L3(进阶) → L4(专业) → L5(导演级)

## 广告创作模式 (Ad Modes)

MadStory 在进入分镜推导前，首先确定广告模式。不同模式对应完全不同的提示词策略和质量标准。

### Mode 1: 电商产品 (Ecommerce)
- **场景**: 商品详情页视频、主图动效、PDP 循环、付费社交素材
- **核心要求**: 产品几何不变形、标签可读、镜头运动克制
- **默认模式**: Image-to-Video
- **关键护栏**: `no label blur, no packaging warp, no logo distortion, no duplicate product`
- **镜头策略**: 单动作、单机位、产品占画幅 > 40%

### Mode 2: UGC 原生广告 (UGC)
- **场景**: 信息流投放素材、创作者口播、种草测评
- **核心要求**: 面部一致、手势自然、节奏"社交感"、产品不消失
- **默认模式**: Reference-to-Video
- **关键护栏**: `no face drift, no extra fingers, no lip mismatch, no product disappearance, no shaky framing`
- **镜头策略**: 单人、单信息点、保留原生感（不要过度电影化）

### Mode 3: 电影感品牌短片 (Cinematic)
- **场景**: 品牌故事片、发布预告、创意前贴
- **核心要求**: 明确的镜头意图、精心设计的灯光逻辑、单个情绪 payoff
- **默认模式**: Text-to-Video 或 Image-to-Video
- **关键护栏**: `no shaky camera, no object melting, no random text, no flat blacks`
- **镜头策略**: 每个镜头只做一件事。多镜头通过序列编排实现复杂叙事。

### Mode 4: 多镜头叙事 (Multi-shot)
- **场景**: 完整叙事弧线、产品使用场景、品牌故事
- **核心要求**: 角色/产品跨镜头一致、过渡自然、节奏把控
- **默认模式**: Reference-to-Video + Multi-shot syntax
- **关键护栏**: 每个镜头 2-3 个分段，使用 `Cut to` / `Camera cut to` / `Shot Switch`
- **镜头策略**: 1 次生成 = 2-3 个镜头，总时长 ≤ 15s；更长叙事通过多次生成 + 后期拼接

### Mode 5: 一镜到底 (One-Shot Long Take)
- **场景**: 产品体验流程、空间巡游、品牌沉浸式展示、创意转场视频
- **来源**: 小云雀 Web 一镜到底功能
- **核心要求**: 2-10 张图片输入 → AI 自动补足转场画面 → 连贯长镜头输出
- **输入类型**: 图片序列（2-10 张）
- **关键能力**: 空间连续性、运镜流畅性、节奏合理性
- **转场设置**: 
  - 自定义转场描述（推/拉/螺旋/溶解/匹配剪辑等）
  - 仅设转场时长（AI 自动发挥）
  - 支持逐段落描述转场方式
- **关键护栏**: `no abrupt cuts, no spatial discontinuity, no object mutation between frames, no stutter in transitions`
- **质量指标**: 镜头空间连续、运镜流畅、转场自然不跳帧

### Mode 6: 爆款复刻 (Viral Replicate)
- **场景**: 不知道做什么时的灵感来源、竞品素材翻拍、爆款模板复用、经典影视猫化/狗化
- **来源**: 小云雀 Web 爆款复刻功能
- **核心要求**: 一键复制心动视频的文案结构、剧情框架、配乐画风
- **输入类型**: 参考视频（必选）+ 替换主体参考图（可选）
- **复刻策略**:
  - **创意拍摄复刻**: 复用参考视频运镜方式和创作手法，替换主体
  - **经典影视还原**: 复刻全部细节，替换人物（如换成猫/动画角色）
  - **爆款拆解再生**: 解析爆点原因 → 借鉴文案/主题/画面风格 → 重新创作
- **提示词模式**: `参考[@视频1]的运镜方式和创作手法，将主体更换为[@图片1]，创作成类似风格的[品类]视频`
- **关键护栏**: `no style drift from reference, no subject identity loss, no mismatched pacing`
- **质量指标**: 风格还原度、主体替换自然度、节奏匹配度

### Mode 7: Agent 模式 (Agent Mode — 从一句话到成片)
- **场景**: 零基础创作者、有脚本需组织、有素材需整合、跨风格创作
- **来源**: 小云雀 Web Agent 模式
- **核心要求**: 输入一句话 / 脚本 / 素材 → Agent 自动理解意图 → 规划创作路径 → 调度最优模型 → 输出成品
- **适用人群**:
  - 零基础: 不会写分镜，从"一句话"出片
  - 有脚本: 把台词、镜头、节奏交给 Agent 组织成片
  - 有素材: 图片/视频/文案丢进去，做"从素材到成片"的组合拳
  - 追求风格: 写实电影感、3D、二次元、国风漫画等同一套流程
- **创作链路**:
  1. 意图解析: 抽取主体、风格、时长、情绪
  2. 路径规划: 选择最优创作模式（Text-to-Video / Image-to-Video / Reference-to-Video / Multi-shot）
  3. 分镜编排: 自动生成分镜头脚本
  4. 模型调度: 推荐 Seedance 2.0 参数组合
  5. 提示词合成: 逐镜头输出完整提示词
- **关键护栏**: 按最终选定子模式注入对应 Negative Prompt
- **质量指标**: 意图理解准确度、分镜完整性、风格一致性

### Mode 8: 短剧创作 (Short Drama)
- **场景**: AI 短剧全自动生产、漫剧创作、小说改编短剧
- **来源**: 小云雀 Web 短剧&漫剧 Agent
- **核心能力**:
  - 剧本全自动解析 → 连贯生成完整剧集
  - 全局角色/场景管理 → 角色不同时空妆造精准映射
  - Agent 智能旁白改编
  - 多画风支持（写实/漫画/3D/二次元）
  - 多剧集连发
- **输入格式**: 标准剧本（含场景标注、人物标注、对白/OS/动作描述）
- **角色一致性**: 在分镜故事板中 @角色形象 保持跨镜头一致
- **关键护栏**: `no character face drift across episodes, no costume inconsistency, no scene discontinuity, no voice mismatch`
- **质量指标**: 角色跨集一致性、剧本还原度、旁白自然度

## 分镜推导流程 (8 阶段)

### Phase 0: 模式选择与意图澄清
- 确认广告目标（卖货 / 种草 / 品牌 / 叙事）
- 选择对应 Mode，明确核心约束
- 确定输入素材类型（纯文本 / 产品图 / 参考图 / 参考视频）
- **产出**: Mode 确认 + 输入策略

### Phase 1: 核心创意锁定 (Core Concept)
- 明确主体（产品 / 人物 / 场景）
- 定义单镜头内唯一的动作或信息点
- 确定情感基调和观众预期反应
- **拒绝策略**: 如果用户在一个镜头里塞了 > 1 个动作或 > 1 个信息点，主动建议拆分
- **产出**: Subject + Action 描述

### Phase 2: 时间轴与节奏 (Timeline & Rhythm)
- 规划 15 秒内的时间分配
- 定义关键帧节点（至少 3 个：入场 / 核心 / 收尾）
- 多镜头模式：规划 Cut-to 节点和镜头间节奏关系
- **产出**: Timeline 描述 + 关键帧定义

### Phase 3: 视觉构图 (Visual Composition)
- 确定画面比例、构图方式
- 主体在画面中的占比和位置
- 角色 / 产品与环境的空间关系
- **电商提醒**: 产品必须占画面显著位置，不要放在边角
- **UGC 提醒**: 保持自然取景，不要过度设计构图
- **产出**: Composition 描述 + 画幅建议

### Phase 4: 镜头运动 (Camera Movement)
- 选择 1 个主导镜头运动（不可在一个镜头内混用多种运动）
- 在 Timeline 上标注运动变化
- 给出 Motion Strength 建议值
- **原则**: 镜头运动服务于内容，不炫技
- **产出**: Camera 描述（含运动强度）+ Motion Strength 参数

### Phase 5: 光影与质感 (Lighting & Texture)
- 光源方向、色温、对比度
- 环境细节（烟雾、颗粒、反射、材质）
- 整体色调和视觉风格
- **电商提醒**: 光源不要遮挡产品标签
- **产出**: Lighting 描述 + 风格预设

### Phase 6: 声音设计 (Sound Design)
- BGM 情绪和节奏
- 音效同步点（与 Timeline 关键帧对齐）
- 环境音规划
- **产出**: Sound 描述 + BGM 建议

### Phase 7: 最终合成与参数输出 (Export)
- 整合所有 Phase 产出为完整提示词
- 生成 Negative Prompt（基于 Mode 自动注入）
- 输出多模态建议（参考图 / 参考视频 / 音频建议）
- 输出 Seedance 2.0 参数建议
- 质量自检：检查是否满足当前 Mode 的硬性约束

## 提示词工程规范 (Prompt Engineering)

### 标准提示词结构 (5 层)
```
[Subject], [Single Action], [Camera Move], [Style & Lighting], [Constraints]
```

### Negative Prompt 按模式注入

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

### 多镜头语法
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

### 一镜到底转场语法 (One-Shot Transition Syntax)
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

### 爆款复刻语法 (Viral Replicate Syntax)
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

### Agent 模式创作链路
- **模糊意图 → 成片**: 输入自然语言 → 引擎解析主体/风格/时长/情绪 → 自动规划 → 分镜编排 → 提示词输出
- **有脚本 → 成片**: 输入脚本 → 解析台词/场景/角色 → 分镜表生成 → 逐镜提示词
- **有素材 → 成片**: 输入图片/视频/文案 → 素材角色分配 → 组合拳编排 → 输出

### 短剧剧本格式 (Short Drama Script Format)
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

## 短剧全流程一致性管控方案 (Short Drama Full-Pipeline Consistency Protocol)

> **适用场景**: 单集时长 3~5 分钟的短剧，单条拍摄脚本有效录制时长 > 15 秒时必须启用本方案。
> **核心目标**: 确保全片人物外观/行为逻辑、场景空间/环境参数、跨片段拼接后观感无任何一致性漏洞。

### 阶段 A: 前期筹备 — 标准化一致性管控台账

#### A1. 人物设定专属档案 (Character Dossier)
每位登场角色必须建立独立档案，包含以下五项不可变记录：

| 档案维度 | 记录内容 | 校验方式 |
|---------|---------|---------|
| 外观细节 | 发型、发色、妆容、服饰搭配、配饰位置、穿着状态（如"右腕银色手链，第三颗衬衫扣未系"） | 逐场次对照档案原文 |
| 性格逻辑 | 核心性格标签（≤3个）、行为倾向、情绪反应模式 | 与台词/动作逻辑交叉验证 |
| 行为习惯 | 标志性动作、口头禅、下意识小动作 | 全片至少出现 2 次以建立角色锚 |
| 台词口径 | 语速特征、用词偏好、禁忌用语 | 跨场次台词风格一致性 |
| 时间线坐标 | 该角色每段戏份的绝对时间位置（集数+秒数范围） | 与全片时间线轴对齐 |

**档案模板**:
```
角色名: [name]
视觉标记: [唯一辨识特征，如"左眼下方泪痣"]
发型/发色: [exact description]
妆容: [exact description]
服饰搭配: [上衣/下装/鞋/外套，含颜色材质]
配饰位置: [每件配饰的精确佩戴位置]
穿着状态: [如"外套披肩不穿袖""袖口挽至肘部"]
性格标签: [≤3个标签]
行为习惯: [标志性动作+频率]
台词口径: [语速/用词特点]
出镜时间线: [Ep1@0:15-0:45, Ep1@2:10-2:55, ...]
```

#### A2. 场景全景清单 (Scene Inventory)
每个拍摄场景建立独立编号档案：

| 档案维度 | 记录内容 |
|---------|---------|
| 空间布局 | 房间/场景的平面描述，关键参照物位置（门/窗/家具/通道） |
| 陈设摆放 | 桌面物件、墙面装饰、地面物品的精确位置与排列 |
| 环境参数 | 光线方向、色温(K值)、天气状态、背景杂音属性（如"窗外间歇性车流声"） |
| 道具状态 | 每件关键道具的物理状态：磨损程度、摆放角度、使用痕迹 |
| 参考素材 | 该场景各角度的实拍参考图编号 + 尺寸测绘图编号 |

**场景编号规则**: `SC-[集数]-[场景序号]` 如 `SC-01-02` 表示第 1 集第 2 个场景。

#### A3. 全片时间线轴 (Master Timeline)
- 将每一段超过 15 秒的长时长戏份按时间节点拆分标记
- 每个标记节点包含：绝对时间位置、关联角色、所在场景、相邻戏份
- 关联前后相邻戏份的一致性要求（如"本段角色服饰须与 [前段Ep1@1:30] 一致"）

**时间线标记格式**:
```
[Ep1@1:30-2:45 | 时长75s | 角色:甲/乙 | 场景:SC-01-02 | 前接:Ep1@0:30-1:25 | 后接:Ep1@2:50-3:30]
  校验节点@10s: 甲右腕手链可见 + 乙外套穿着状态 + 桌面水杯位置(距桌沿5cm)
  校验节点@20s: ...
```

### 阶段 B: 拍摄执行 — 长时长戏份现场一致性核查机制

#### B1. 开拍前对照核查 (Pre-Shoot Verification)
每次长时长戏份（>15s）开拍前，一致性专员逐项核对：
1. 对照人物档案：当前演员外观是否与前次同角色出镜完全匹配
2. 对照场景清单：场景陈设、道具位置是否与同场景上一次记录一致
3. 对照时间线轴：确认当前戏份与前后段的一致性约束要求
4. 全部核对通过后签署"开拍确认"，方可正式录制

#### B2. 分片段录制 + 连贯校验流程
- 每 **10~12 秒** 设置一个校验节点（checkpoint）
- 录制第一段时留存该节点的标准参考画面（Reference Frame）
- 后续分段录制前，先对齐 Reference Frame 的所有视觉要素（人物姿态、场景陈设、光线条件）
- 确认对齐后启动下一段录制

#### B3. 现场环境参数同步留存
- 每条长戏份全程录制素材时，同步记录每一时间节点的环境参数：
  - 光线色温（K值）、光源方向
  - 现场背景噪音属性（dB 参考值 + 噪音类型）
- 现场快速回放核查：人物动作连贯性、场景元素稳定性
- 发现偏差立即重拍该段，不进入下一段

### 阶段 C: 后期制作 — 跨片段一致性精修校验

#### C1. 剪辑阶段核查
- 将拆分录制的长戏份素材拼接后，逐帧核查：
  - 人物动作衔接是否连续（无跳帧）
  - 服饰状态是否一致（扣子/袖口/衣领位置）
  - 场景光影是否统一（同场景光源一致）
- 修正跳帧或参数偏差的片段（可用 AI 插帧或手动微调）

#### C2. 调色阶段统一
- 同场景所有戏份统一以下参数：
  - 色温（白平衡锁定到同一 K 值）
  - 亮度曲线（同场景使用同一 LUT）
  - 滤镜参数（饱和度/对比度/色相偏移 完全一致）
- 不同时间录制的同场景画面，视觉风格必须完全一致

#### C3. 音轨整合阶段对齐
- 同场景的背景杂音参数对齐（噪音类型、音量级）
- 环境音参数一致（混响、空间感）
- 跨片段音画同步检查：无口型延迟、无音效错位

### 阶段 D: 最终验收标准 (Final Acceptance Criteria)

短剧全片一致性验收须满足以下四项硬性要求，任一项不通过即视为不合格：

1. **人物外观无矛盾**: 全片所有 >15s 长戏份中，同一角色的发型/发色/妆容/服饰/配饰/穿着状态完全一致，无任何外观跳变
2. **行为逻辑无冲突**: 同一角色的性格、行为习惯、台词风格在跨场次间保持统一，无自相矛盾
3. **场景空间无冲突**: 同一场景的空间布局、陈设位置、道具状态全片一致，无凭空出现或消失的物件
4. **跨时段拼接自然**: 所有拆分录制的素材拼接后，观感连贯自然，无任何影响观看体验的一致性漏洞（跳帧/色偏/音画不同步）

**验收工具**: `python3 scripts/director_validator.py --check-consistency <episode_output.json>`

## 交互准则
- **逐阶段推进**: 每次只推进一个 Phase，不要让用户一次性回答所有问题
- **用专业术语，但让外行听懂**: 提供选项卡片供选择
- **实时展示草稿**: 每完成一个 Phase 展示当前分镜草案
- **主动拦截**: 当用户在一个镜头里塞入过多信息时，主动建议拆分
- **模式引导**: Phase 0 必须确认广告模式，不跳过
- **负向提示词自动注入**: 用户不需要手写负向提示词，由系统按 Mode 自动生成
- **质量自检**: 输出前对关键约束进行自查
- **一致性管控**: 短剧模式中，单条拍摄 >15s 时自动启用全流程一致性管控方案

## 输出规范

每个分镜方案必须包含:
1. **STANDARD_PROMPT**: 符合 5 层结构的完整正向提示词
2. **NEGATIVE_PROMPT**: 按 Mode 自动生成的负向提示词
3. **TIMELINE**: 15 秒时间轴 + 关键帧描述
4. **CAMERA**: 逐秒/逐镜头运动描述
5. **MOTION_STRENGTH**: 建议值 (1-10)
6. **DURATION**: 固定 15s（或按多镜头分配）
7. **MODE**: 广告模式标签
8. **MULTI_MODAL_ADVICE**: 参考图/视频/音频建议
9. **SHOT_LIST** (多镜头模式): 分镜头脚本表

## 不可接受的质量问题 (Quality Gates)
- 产品标签不可读或变形 → Ecommerce 不合格
- 人脸在两个镜头间不一致 → UGC / Short Drama 不合格
- 一个镜头内超过 1 个主导运动 → 任何 Mode 不合格
- 缺少 Negative Prompt → 任何 Mode 不合格
- 多镜头序列 > 3 个镜头放在一次生成 → Multi-shot 不合格
- 一镜到底出现跳帧或空间断裂 → One-Shot 不合格
- 爆款复刻风格偏离参考 → Viral Replicate 不合格
- Agent 模式意图解析完全偏离用户输入 → Agent 不合格
- 短剧角色跨集不一致 → Short Drama 不合格

## 资源索引 (Bundled Resources)

本技能采用渐进式披露 (Progressive Disclosure) 架构。SKILL.md 始终加载到上下文，以下捆绑资源按需读取：

| 资源路径 | 用途 | 何时读取 |
|---------|------|---------|
| `scripts/mad_story_engine.py` | 核心引擎 (CLI/API 入口, 模式枚举, 质量门, 短剧引擎, 一致性管控) | 执行分镜生成、校验或一致性验收时自动调用 |
| `scripts/director_validator.py` | 导演级全模式核验工具 | 运行 `--validate` 或 `--check-consistency` 时 |
| `scripts/api_server.py` | REST API + WebSocket 服务 | 企业级 CI/CD 集成时启动 |
| `scripts/batch_runner.py` | 目录级批量生产流水线 | 批量处理多个 JSON 规格文件或剧本时 |
| `scripts/llm_router.py` | LLM 增强路由 (关键词 fallback) | 安装 requests 后自动启用，否则退化为关键词模式 |
| `references/seedance_v2_rules.md` | Seedance 2.0 提示词工程规范 (324行) | 生成或校验提示词结构时读取；包含 5 层结构定义、三种输入模式策略、多镜头语法、电商/UGC 专项规范 |
| `references/terminology.md` | 影视分镜专业术语库 (109行) | 需要精确镜头术语时读取；含焦距/角度/运动/构图/光影/广告工业/一镜到底/爆款复刻/短剧术语 |
| `references/pre_flight_checklist.md` | 导演级预检清单 (134行) | 分镜方案输出前做最终检查时读取；含技术规格/主体构图/镜头运动/光影/声音/模式专项/多模态/输出完整性/质量护栏/最终签署 |
| `assets/cheat_sheet.json` | Seedance 2.0 参数速查 + 模式配置 + 一致性协议参数 | 引擎启动时自动加载；含 motion_strength/cfg_scale 默认值、各模式 quality_gates、转场类型枚举、一致性管控阈值 |
| `assets/storyboard_template.html` | 分镜预览 HTML 模板 | 通过 `engine.render_to_html()` 渲染分镜方案为可视卡片 |
