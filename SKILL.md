---
name: mad-story
description: "电影级影视分镜设计引擎，支持视频生成(Seedance 2.5默认/2.0降级/Runway/Kling/Sora)及图片生成(Seedream 4.x/5.x)。11种创作模式含短剧全链路。触发：影视分镜/分镜设计/电影分镜/广告分镜/电商视频/UGC广告/品牌短片/多镜头叙事/一镜到底/爆款复刻/短剧创作/AI视频生成/Seedance/Seedream/文生图/图生图/图像编辑/参考图生图/短剧剧本/微短剧/竖屏剧/AI短剧/锁脸/小说改短剧/漫剧/角色人设/时间戳控制/超长视频/视频延长/局部编辑/智能编辑/白模/绿幕/BGM分离/多语种/多宫格分镜。不适用于纯静态视觉设计或非分镜用途的通用AI绘画。"
version: 3.8.0
author: qomob.ai
license: MIT
modes: 11
phases: 8
platforms:
  - Trae IDE
  - OpenClaw
  - Dify
  - Coze
  - Claude Desktop / MCP
references:
  - references/seedance_25_rules.md
  - references/modes_detail.md
  - references/phases_detail.md
  - references/prompt_engineering.md
  - references/seedance_v2_rules.md
  - references/seedream_4x_rules.md
  - references/terminology.md
  - references/pre_flight_checklist.md
  - references/short_drama_consistency.md
  - references/short_drama_genres.md
assets:
  - assets/cheat_sheet.json
  - assets/storyboard_template.html
---

# MadStory — 电影级影视分镜设计引擎 v3.8.0 (分层加载架构)

## 技能定位

MadStory 是面向电影级内容生产的专业分镜设计引擎，同时支持 **Seedream 4.x/5.x 图片生成**（文生图、图像编辑、参考图生图、多图输入/输出）。

- **触发词**: `影视分镜`, `分镜设计`, `电影分镜`, `广告分镜`, `电商视频`, `UGC广告`, `品牌短片`, `多镜头叙事`, `一镜到底`, `爆款复刻`, `短剧创作`, `从一句话出片`, `AI电影`, `AI视频生成`, `Seedance`, `Seedream`, `分镜脚本`, `视频提示词`, `文生图`, `图生图`, `图像编辑`, `参考图生图`, `短剧剧本`, `微短剧`, `竖屏剧`, `AI短剧`, `短剧分镜`, `短剧编剧`, `锁脸`, `小说改短剧`, `漫剧`, `角色人设`, `时间戳控制`, `超长视频`, `视频延长`, `局部编辑`, `智能编辑`, `白模`, `绿幕`, `BGM分离`, `多语种`, `多宫格分镜`
- **目标用户**: 电影导演、广告导演、创意总监、影视制作人、电商运营、品牌营销、内容创作者、短剧制作人、零基础创作者、平面设计师
- **默认时长**: 30 秒 / 镜头（Seedance 2.5 视频），15 秒（Seedance 2.0 降级时），图片模式无时长限制
- **原生支持平台**: Seedance 2.5（默认）/ 2.0（降级）(视频), Seedream 4.x/5.x/5.0 Pro (图片) — 所有提示词规则、参数体系、质量门禁均基于此二平台校准
- **兼容输出平台**: Runway Gen-3 / Kling / Sora — 输出的提示词可作为创作起点在这些平台使用，但参数体系（Motion Strength、Negative Prompt 格式、多镜头语法等）需用户自行适配

## 规则版本锁定

> **所有提示词规则、参数建议、质量门禁基于以下平台版本验证。** 平台升级后部分规则可能失效，使用前请核对版本。

| 平台 | 验证版本 | 状态 |
|------|---------|------|
| Seedance 2.5 (视频) | **2.5（默认基准）** | 完整规则见 `references/seedance_25_rules.md`；原生30s/超长180s/延长60s/50素材/时间戳/编辑/白模/绿幕/多语种/多人 |
| Seedance 2.0 (视频) | 2.0（降级备选） | 完整规则见 `references/seedance_v2_rules.md`；积分成本敏感场景使用，不支持2.5新增能力 |
| Seedream (图片) | 4.0 / 4.5 / 5.0 Lite / **5.0 Pro** | 全部规则基于此版本范围；5.0 Pro 专属能力见 `references/seedream_4x_rules.md` §8.5 |

### Seedance 2.5 vs 2.0 快速对照

| 维度 | 2.5（默认） | 2.0（降级） |
|------|------------|------------|
| 单次时长 | 30s（可延长至60s，超长模式180s） | 15s |
| 参考图 | ≤30 张 | ≤9 张 |
| 参考视频 | ≤10 段，总≤30s | ≤3 段，总≤15s |
| 参考音频 | ≤10 段，总≤30s | ≤3 段，总≤15s |
| 仅传音频 | 支持 | 不支持（必须配图/视频） |
| 时间戳控制 | 原生秒级/帧级 | 无 |
| 局部编辑/白模/绿幕 | 支持 | 不支持 |
| BGM 分离/多语种/多人 | 支持 | 不支持 |
| 积分消耗（30s 720p） | ~780 | ~210（15s） |

## AI 模型真实限制（必读）

> 以下限制基于 Seedance 2.5 / 2.0 / Seedream 4.x-5.x 的实际生成表现。**2.5 在时长/复杂动作/一致性/Negative 响应/多人/多语种上均有显著改善**。完整对照见 `references/seedance_25_rules.md` §8。

| 限制 | 2.0 表现 | 2.5 改善 | 对策 |
|------|---------|---------|------|
| **时长衰减** | 8-12s 后质量下降，15s 末段纹理崩坏 | 30s 保持一致性 | 2.5 可放心用 30s；2.0 降级仍优先 ≤10s，必须 15s 时标注"8s 后质量风险区" |
| **复杂动作不稳定** | 开门/打斗/转身等多步骤动作易变形 | 长尾动作解锁，复杂物理交互流畅 | 2.5 可尝试复杂动作；2.0 仍用"慢""稳定"修饰词+剪辑绕开 |
| **跨镜头一致性靠运气** | 角色面部/服装在生成调用间漂移 | 切镜一致性显著提升 | 2.5 多镜头更可靠；2.0 仍需多次生成取最佳 |
| **Motion Strength 偏差** | 高值(≥6)易触发变形 | 仍需注意 | 从低值(2-3)开始，确认稳定后再调高 |
| **Negative 响应** | 不稳定，写了 `no face drift` 仍会 drift | 大幅优化，"禁止"表述响应更好 | 2.5 用"禁止"表述；生成后仍需人工检查 |
| **多人双胞胎** | 多人同框长相趋同、换脸错位 | 多人参考升级解决 | 2.5 多人场景用多人参考；2.0 避免多人同框 |
| **多语种** | 发音不准/不支持长素材 | 10+ 语种原生，口型字幕对齐 | 多语种必须用 2.5 |

## 分层加载架构 (Progressive Loading)

> **核心原则**: SKILL.md 始终加载。其他资源按交互阶段按需加载。

## 模式状态看板（启发）

> 11 种创作模式并行或串行执行时，用户需要看到每个模式的状态——哪个在推导、哪个在生成、哪个已完成。

```
🎬 分镜状态看板
├── [Mode 选择]        ✅ 已完成 — {模式名}
├── [Phase 0-7]        🟡 推导中 — 当前 Phase {N}
├── [提示词生成]       🔵 等待中
└── [Pre-flight 预检]  🔵 等待中
```

多模式串行（如短剧全链路：剧本→分镜→提示词→生成）时，看板展示每个阶段的独立状态。用户可随时说"看板"查看当前进度。

### Layer 0: 始终加载 (本文件)
- 元数据 + 触发词 + 技能定位
- 11 模式概览表
- Phase 0-7 阶段名称
- 输出规范 + 质量门禁
- 分层加载索引

### Layer 1: 按需加载
以下资源在对应触发条件满足时读取文件内容:

| 触发条件 | 加载文件 | 内容 |
|---------|---------|------|
| **默认平台规则（视频生成必读）** | `references/seedance_25_rules.md` | **Seedance 2.5 完整规则**：参数规格/4段式公式/7维人物/30秒3模块/延长/编辑/白模公式/16项能力/转场表/禁止项/AI限制 |
| 积分敏感需降级到 2.0 | `references/seedance_v2_rules.md` | Seedance 2.0 提示词工程规范（5层结构/3种模式/Negative/一镜到底/复刻/Agent/短剧） |
| 用户确认/选择模式 | `references/modes_detail.md` | 该模式（11种）的完整说明、约束、护栏 |
| 进入 Phase N 推导 | `references/phases_detail.md` | Phase N 的详细推导指引 |
| 生成/校验提示词 | `references/prompt_engineering.md` | 4段式主公式+专项公式索引、5层元素检查清单、Negative索引 |
| 需要精确镜头术语 | `references/terminology.md` | 影视专业术语库 |
| 分镜方案输出前检查 | `references/pre_flight_checklist.md` | 导演级预检清单 + **元反思（8 维度推演过程自检）** |
| 使用 Seedream 4.x/5.x 或涉及图片生成 | `references/seedream_4x_rules.md` | Seedream 4.x/5.x 文生图/图像编辑/参考图/多图规则 |
| 短剧 + 需要题材灵感/爆款分析 | `references/short_drama_genres.md` | 6大题材模板与10集标准结构、爆款套路 |

### Layer 2: 深度加载（高级场景触发）

| 触发条件 | 加载文件 | 内容 |
|---------|---------|------|
| 短剧 + 多场景/多集 | `references/short_drama_consistency.md` | 短剧全流程一致性管控、角色卡、八要素公式、小说改编流程 |
| 要求电影级镜头语言 | `assets/cheat_sheet.json` → `cinematic_camera_language` + `cinematic_lighting_extended` | 运镜/构图/布光预设 |
| 要求声音设计 | `assets/cheat_sheet.json` → `cinematic_sound_extended` | 声音分层 + 情感映射 |
| 要求导演风格参考 | `assets/cheat_sheet.json` → `director_style_references` + `creative_film_prompts_library` | 大师风格库 |
| HTML 可视化 | `assets/storyboard_template.html` | 分镜预览模板 |

## 11 种创作模式概览

| # | 模式 | 场景 | 输入 | 核心约束 |
|---|------|------|------|---------|
| 0 | 电影创意探索 | 概念开发、风格实验 | Text | Generate-and-Filter + Tournament |
| 1 | 电商产品 | 商品详情页、主图动效 | Image | 产品不变形、标签可读 |
| 2 | UGC 原生广告 | 信息流、口播、种草 | Reference | 人脸一致、手势自然 |
| 3 | 电影感品牌短片 | 品牌故事、预告 | Text/Image | 镜头有意图、灯光有逻辑 |
| 4 | 多镜头叙事 | 完整叙事弧线、超长叙事 | Reference | 跨镜头一致、2.5支持超长180s/延长60s/无缝转场 |
| 5 | 一镜到底 | 空间巡游、沉浸展示 | Image序列 | 2-10图，空间连续、支持30s长一镜 |
| 6 | 爆款复刻 | 灵感翻拍、竞品复刻 | Reference+Image | 风格还原、迁移创意/绿幕/BGM分离 |
| 7 | Agent 模式 | 一句话到成片 | Text | 自动意图解析+路径规划（含超长/编辑/白模路由） |
| 8 | 短剧创作 | AI短剧、漫剧、小说改编 | Reference+Script | 多人参考/音色/跨集一致、多语种出海 |
| 9 | 智能编辑 | 局部消除/替换/空间视角修改/BGM分离 | Video | 精准定位防误伤、保留不变要素 |
| 10 | 白模预演 | Maya/Blender白模渲染、分镜预演 | Video(白模)+Image | 镜头/空间/走位精准、粗/细颗粒度 |

> 模式详情见 `references/modes_detail.md`

## 分镜推导阶段 (Phase 0-7)

| Phase | 名称 | 产出 |
|-------|------|------|
| 0 | 模式选择与意图澄清 | Mode 确认 + 输入策略 |
| 1 | 核心创意锁定 | Subject + Action |
| 2 | 时间轴与节奏 | Timeline + 关键帧 |
| 3 | 视觉构图 | Composition + 画幅 |
| 3.5 | 表演与调度 | Performance Notes（走位/视线/反应镜头/潜台词） |
| 4 | 镜头运动 | Camera + Motion Strength |
| 5 | 光影与质感 | Lighting + 风格预设 |
| 6 | 声音设计 | Sound + BGM |
| 7 | 最终合成与输出 | 完整提示词 + Negative Prompt |

> Phase 详情见 `references/phases_detail.md`

## 交互准则
- **逐阶段推进**: Phase 3.5（表演与调度）和 Phase 4（镜头运动）之间必须暂停确认，因为调度决策直接影响镜头选择
- **用专业术语但让外行听懂**: 提供选项卡片
- **主动拦截**: 用户塞入过多信息时建议拆分
- **模式引导**: Phase 0 必须确认模式
- **负向提示词自动注入**: 由系统按 Mode 自动生成
- **图片模式**: 启用 Seedream 规则时自动切换输出格式

## 输出规范

### 视频模式输出 (Seedance 2.5默认/2.0降级/Runway/Kling/Sora)
每个分镜方案必须包含:
1. **ENGINE_VERSION**: Seedance 2.5（默认）或 2.0（降级）— 明确标注影响可用能力
2. **STANDARD_PROMPT**: 符合 4 段式主公式的完整正向提示词（素材描述+一句话概述+具体情节+全局补充）；专项场景用对应公式（7维人物/30秒3模块/延长/编辑/白模）
3. **NEGATIVE_PROMPT**: 按 Mode 自动生成的禁止项 + 历史缺陷增强（2.5 用"禁止"表述）
4. **TIMELINE**: 时间轴 + 关键帧描述（2.5 默认 30s，2.0 降级 15s，超长 30-180s）
5. **TIMESTAMP_CONTROL**: 时间戳分镜（长视频/多镜头/卡点必填，见 `seedance_25_rules.md` §3）
6. **CAMERA**: 逐秒/逐镜头运动描述
7. **MOTION_STRENGTH**: 建议值 (1-10)
8. **DURATION**: [4,30]s / 超长 30-180s / 延长 ≤60s
9. **MODE**: 模式标签
10. **MULTI_MODAL_ADVICE**: 参考素材建议（2.5: ≤30图+≤10视频+≤10音频 / 2.0: ≤9图+≤3视频+≤3音频）
11. **SHOT_LIST** (多镜头模式): 分镜头脚本表
12. **DEFECT_LOG**: 用户返回后填写实际生成中出现的缺陷类型（可选，用于持续优化）

### 图片模式输出 (Seedream 4.x/5.x)
> 完整规则见 `references/seedream_4x_rules.md`

每个图片方案必须包含:
1. **IMAGE_PROMPT**: 符合 3 层结构（主体+行为+环境，风格/色彩/光影/构图补充）
2. **TEXT_CONTENT**: 需渲染的文字（双引号包裹）
3. **REFERENCE_TYPE**: 参考类型（人物形象/风格/虚拟实体/款式/无）
4. **EDIT_OPERATION**: 编辑操作（增加/删除/替换/修改/无）
5. **MULTI_IMAGE_OP**: 多图操作（替换/组合/迁移/无）
6. **MODE**: 模式标签
7. **PLATFORM**: Seedream 4.x/5.x

## 质量门禁 (Quality Gates)

### 视频模式

| 门禁 | 触发条件 | 不合格判定 |
|------|---------|-----------|
| **产品安全** | Ecommerce 模式 | 产品标签不可读或变形 → 不合格 |
| **人脸一致性** | UGC / Short Drama 模式 | 人脸在两个镜头间不一致 → 不合格 |
| **单运动原则** | 任何 Mode | 一个镜头内超过 1 个主导运动 → 不合格 |
| **禁止项声明** | 任何 Mode | 缺少 Negative Prompt/禁止项 → 不合格 |
| **时长范围** | 任何 Mode | 不在 [4,30]s（超长 30-180s / 延长 ≤60s）→ 不合格 |
| **多模态上限** | 任何 Mode | 超过 30图/10视频/10音频（2.0: 9图/3视频/3音频）→ 不合格 |
| **空间连续性** | One-Shot 模式 | 跳帧或空间断裂 → 不合格 |
| **风格还原** | Viral Replicate 模式 | 风格偏离参考 → 不合格 |
| **意图解析** | Agent 模式 | 意图完全偏离 → 不合格 |
| **跨集一致** | Short Drama 模式 | 角色跨集不一致 → 不合格 |
| **编辑保留** | Smart Edit 模式 | 未声明保留的不变要素 → 不合格 |
| **白模对应** | White Model 模式 | 白模与渲染主体对应关系映射缺失 → 不合格 |
| **版本能力匹配** | 2.0 降级时 | 使用了 2.5 独有能力（时间戳/编辑/白模等）→ 不合格 |

### 图片模式 (Seedream 4.x/5.x)

| 门禁 | 不合格判定 |
|------|-----------|
| **文字包裹** | 文字内容未用双引号包裹 → 不合格 |
| **指令指代** | 编辑指令使用代词而非具体对象 → 不合格 |
| **参考图描述** | 未指明参考对象和生成画面 → 不合格 |
| **多图角色** | 多图输入未明确图一/图二角色分配 → 不合格 |

> 短剧一致性管控详见 `references/short_drama_consistency.md`

## 参数依赖链（不可编造）

> 以下参数**必须从上一步返回中提取，禁止编造**。

模式选择 → ModeSelection
  ↓ selected_mode, video_engine, image_engine
角色/场景设定 → CharacterSceneSetup
  ↓ characters[].id, scenes[].id, consistency_lock
分镜设计 → StoryboardFrames
  ↓ frames[].id, frames[].shot_type, frames[].prompt
提示词生成 → FinalPrompts
  ↓ prompts[].frame_id, prompts[].engine_specific

## 目录结构

```text
mad-story/
├── SKILL.md                 # 技能定义 v3.8.0 — 分层加载/双版本(2.5默认+2.0降级)/11模式
├── README.md                # 使用说明
├── references/
│   ├── seedance_25_rules.md # Seedance 2.5 完整规则（默认基准） (Layer 1)
│   ├── modes_detail.md      # 11种模式详细说明 (Layer 1)
│   ├── phases_detail.md     # Phase 0-7 详细推导指引 (Layer 1)
│   ├── prompt_engineering.md # 4段式主公式+专项公式索引+5层元素检查清单 (Layer 1)
│   ├── seedance_v2_rules.md # Seedance 2.0 提示词工程规范（降级备选） (Layer 1)
│   ├── seedream_4x_rules.md # Seedream 4.x/5.x 图片生成规范 (Layer 1)
│   ├── terminology.md       # 影视分镜专业术语库 (Layer 1)
│   ├── pre_flight_checklist.md # 导演级预检清单 + 元反思（8 维度） (Layer 1)
│   ├── short_drama_consistency.md # 短剧全流程一致性管控 (Layer 2)
│   ├── short_drama_genres.md # 短剧6大题材模板 (Layer 1)
│   └── examples/
│       ├── example_1_creative_film.md
│       ├── example_2_multi_shot.md
│       └── example_3_short_drama.md
└── assets/
    ├── cheat_sheet.json     # 参数速查表 — 镜头语言/光影/声音/导演参考（单一数据源）
    └── storyboard_template.html # 分镜预览模板
```

> 独立工具包（CLI/API/验证）位于 `tools/mad-story-scripts/`，非技能运行时必需。

## 生成结果反馈回路 (DEFECT_LOG)

> **从静态知识库变成动态经验库。** 每次 Phase 7 输出的提示词不是终点——用户生成视频后返回的缺陷数据会让下一次输出更精准。

### 机制

```
Phase 7 输出提示词 → 用户生成视频 → 观察结果 → 报告缺陷类型
                                                      ↓
                                         DEFECT_LOG（按 Mode 累积）
                                                      ↓
                                         下次该 Mode 的 Phase 7:
                                         1. 检查 DEFECT_LOG 高频缺陷
                                         2. 在 NEGATIVE_PROMPT 追加针对性保护词
                                         3. 在输出中增加 KNOWN_RISKS 警告
```

### DEFECT_LOG 格式

用户返回生成结果后，按以下格式记录：

```
DEFECT_LOG:
  mode: [模式名]
  defect_type: [face_drift | object_deformation | motion_glitch | texture_collapse | color_shift | other]
  severity: [high | medium | low]
  timestamp: [在视频中出现的时间点，如 "8-10s"]
  description: [一句话描述具体问题]
  prompt_used: [当时的 STANDARD_PROMPT 摘要]
```

### 预填缺陷库（冷启动）

首次使用时，基于 AI 模型已知问题预填常见缺陷，用户只需确认或补充：

| Mode | 预填缺陷 | 默认增强措施 |
|------|---------|------------|
| Ecommerce | 产品标签 10s 后模糊 | NEGATIVE_PROMPT 追加 `no label degradation after midpoint` |
| UGC | 人脸 7s 后开始漂移 | 建议时长缩短至 10s；追加 `no late-stage face drift` |
| Cinematic | 高 Motion Strength(≥6) 触发物体融化 | Motion Strength 降级建议 + `no object melting at high motion` |
| Multi-shot | 第二/三镜头角色面部不一致 | 追加 `no character drift in later shots` |
| Short Drama | 跨集角色外观漂移 | 建议每集使用相同参考图 + seed |
