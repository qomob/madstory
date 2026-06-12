---
name: mad-story
description: "电影级影视分镜设计引擎，支持视频生成(Seedance/Runway/Kling/Sora)及图片生成(Seedream 4.x/5.x)。9种创作模式含短剧全链路。触发：影视分镜/分镜设计/电影分镜/广告分镜/电商视频/UGC广告/品牌短片/多镜头叙事/一镜到底/爆款复刻/短剧创作/AI视频生成/Seedance/Seedream/文生图/图生图/图像编辑/参考图生图/短剧剧本/微短剧/竖屏剧/AI短剧/锁脸/小说改短剧/漫剧/角色人设。不适用于纯静态视觉设计或非分镜用途的通用AI绘画。"
version: 3.3.0
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

# MadStory — 电影级影视分镜技能 v3.2 (分层加载架构)

## 技能定位
MadStory 是面向电影级内容生产的专业分镜设计引擎，基于 **Harness Engineering** (PPAF 循环 + R.E.S.T 可靠性模型)。同时支持 **Seedream 4.x/5.x 图片生成**（文生图、图像编辑、参考图生图、多图输入/输出、知识可视化）。

- **触发词**: `影视分镜`, `分镜设计`, `电影分镜`, `广告分镜`, `电商视频`, `UGC广告`, `品牌短片`, `多镜头叙事`, `一镜到底`, `爆款复刻`, `短剧创作`, `从一句话出片`, `AI电影`, `AI视频生成`, `Seedance`, `Seedream`, `分镜脚本`, `视频提示词`, `文生图`, `图生图`, `图像编辑`, `参考图生图`, `短剧剧本`, `微短剧`, `竖屏剧`, `AI短剧`, `短剧分镜`, `短剧编剧`, `锁脸`, `小说改短剧`, `漫剧`, `角色人设`
- **目标用户**: 电影导演、广告导演、创意总监、影视制作人、电商运营、品牌营销、内容创作者、短剧制作人、零基础创作者、平面设计师
- **默认时长**: 15 秒 / 镜头（视频），图片模式无时长限制
- **支持平台**: Seedance 2.0 / Runway / Kling / Sora (视频), Seedream 4.x/5.x (图片)

## 分层加载架构 (Progressive Loading)

> **核心原则**: SKILL.md 始终加载（本文件）。其他资源按交互阶段按需加载，不预加载。

### Layer 0: 始终加载 (本文件, ~1,500 tokens)
- 元数据 + 触发词 + 技能定位
- 9 模式概览表 (每模式 1 行)
- Phase 0-7 阶段名称 (无详细说明)
- 输出规范 + 质量门禁
- 分层加载索引

### Layer 1: 按需加载 (~2,000 tokens/次)
以下资源在对应触发条件满足时 **读取文件内容**:

| 触发条件 | 加载文件 | 内容 |
|---------|---------|------|
| 用户确认/选择模式 | `references/modes_detail.md` | 该模式的完整说明、约束、护栏 |
| 进入 Phase N 推导 | `references/phases_detail.md` | Phase N 的详细推导指引 |
| 生成/校验提示词 | `references/prompt_engineering.md` | 5层结构、Negative Prompt模板、多镜头/一镜到底/复刻语法 |
| 需要精确镜头术语 | `references/terminology.md` | 影视专业术语库 |
| 分镜方案输出前检查 | `references/pre_flight_checklist.md` | 导演级预检清单 |
| 需要平台参数参考 | `references/seedance_v2_rules.md` | Seedance 2.0 提示词工程规范 |
| 使用 Seedream 4.x/5.x 或涉及图片生成 | `references/seedream_4x_rules.md` | Seedream 4.x/5.x 文生图/图像编辑/参考图/多图规则 |
| Mode 8 短剧 + 需要题材灵感/爆款分析 | `references/short_drama_genres.md` | 6大题材模板与10集标准结构、爆款套路 |

### Layer 2: 深度加载 (~3,000 tokens/次)
以下资源仅在特定高级场景下加载:

| 触发条件 | 加载文件/模块 | 内容 |
|---------|-------------|------|
| Mode 8 短剧 + 多场景/多集 | `references/short_drama_consistency.md` | 短剧全流程一致性管控 + 剧本方法论 + 角色卡 + 八要素公式 + 小说改编流程 |
| Mode 0 创意探索 | `assets/cheat_sheet.json` → `director_style_references` + `creative_film_prompts_library` | 导演风格参考 + 创意提示库 |
| 要求电影级镜头语言 | `assets/cheat_sheet.json` → `cinematic_camera_language` + `cinematic_lighting_extended` | 运镜/构图/布光预设 |
| 要求声音设计 | `assets/cheat_sheet.json` → `cinematic_sound_extended` | 声音分层 + 情感映射 |
| CLI/API 调用 | `scripts/mad_story_engine.py` | 核心引擎代码 |
| 质量校验 | `scripts/director_validator.py` | 导演级核验工具 |
| 企业集成 | `scripts/api_server.py` | REST API 服务 |
| 批量生产 | `scripts/batch_runner.py` | 批量流水线 |
| LLM 增强 | `scripts/llm_router.py` | 多意图拆分/Tournament路由 |
| 多平台适配 | `scripts/platform_adapter.py` | 平台参数映射 |
| HTML 可视化 | `assets/storyboard_template.html` | 分镜预览模板 |

## 9 种创作模式概览

| # | 模式 | 场景 | 输入 | 核心约束 |
|---|------|------|------|---------|
| 0 | 电影创意探索 | 概念开发、风格实验 | Text | Generate-and-Filter + Tournament |
| 1 | 电商产品 | 商品详情页、主图动效 | Image | 产品不变形、标签可读 |
| 2 | UGC 原生广告 | 信息流、口播、种草 | Reference | 人脸一致、手势自然 |
| 3 | 电影感品牌短片 | 品牌故事、预告 | Text/Image | 镜头有意图、灯光有逻辑 |
| 4 | 多镜头叙事 | 完整叙事弧线 | Reference | ≤3镜头/次，跨镜头一致 |
| 5 | 一镜到底 | 空间巡游、沉浸展示 | Image序列 | 2-10图，空间连续 |
| 6 | 爆款复刻 | 灵感翻拍、竞品复刻 | Reference+Image | 风格还原、主体替换 |
| 7 | Agent 模式 | 一句话到成片 | Text | 自动意图解析+路径规划 |
| 8 | 短剧创作 | AI短剧、漫剧、小说改编 | Reference+Script | 跨集角色一致 |

> 模式详情见 `references/modes_detail.md`

## 分镜推导阶段 (Phase 0-7)

| Phase | 名称 | 产出 |
|-------|------|------|
| 0 | 模式选择与意图澄清 | Mode 确认 + 输入策略 |
| 1 | 核心创意锁定 | Subject + Action |
| 2 | 时间轴与节奏 | Timeline + 关键帧 |
| 3 | 视觉构图 | Composition + 画幅 |
| 4 | 镜头运动 | Camera + Motion Strength |
| 5 | 光影与质感 | Lighting + 风格预设 |
| 6 | 声音设计 | Sound + BGM |
| 7 | 最终合成与输出 | 完整提示词 + Negative Prompt |

> Phase 详情见 `references/phases_detail.md`

## 交互准则
- **逐阶段推进**: 每次只推进一个 Phase，不跳过
- **用专业术语但让外行听懂**: 提供选项卡片
- **实时展示草稿**: 每完成一个 Phase 展示当前草案
- **主动拦截**: 用户塞入过多信息时建议拆分
- **模式引导**: Phase 0 必须确认模式
- **负向提示词自动注入**: 由系统按 Mode 自动生成
- **质量自检**: 输出前对关键约束自查

## 输出规范

### 视频模式输出 (Seedance/Runway/Kling/Sora)
每个分镜方案必须包含:
1. **STANDARD_PROMPT**: 符合 5 层结构的完整正向提示词
2. **NEGATIVE_PROMPT**: 按 Mode 自动生成的负向提示词
3. **TIMELINE**: 15 秒时间轴 + 关键帧描述
4. **CAMERA**: 逐秒/逐镜头运动描述
5. **MOTION_STRENGTH**: 建议值 (1-10)
6. **DURATION**: 固定 15s（或按多镜头分配）
7. **MODE**: 模式标签
8. **MULTI_MODAL_ADVICE**: 参考图/视频/音频建议
9. **SHOT_LIST** (多镜头模式): 分镜头脚本表

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
- 产品标签不可读或变形 → Ecommerce 不合格
- 人脸在两个镜头间不一致 → UGC / Short Drama 不合格
- 一个镜头内超过 1 个主导运动 → 任何 Mode 不合格
- 缺少 Negative Prompt → 任何 Mode 不合格
- 多镜头序列 > 3 个镜头放在一次生成 → Multi-shot 不合格
- 一镜到底出现跳帧或空间断裂 → One-Shot 不合格
- 爆款复刻风格偏离参考 → Viral Replicate 不合格
- Agent 模式意图解析完全偏离 → Agent 不合格
- 短剧角色跨集不一致 → Short Drama 不合格

### 图片模式 (Seedream 4.x/5.x)
- 文字内容未用双引号包裹 → 图片模式不合格
- 图像编辑指令指代模糊（使用代词而非具体对象） → 图片模式不合格
- 参考图生图未指明参考对象和生成画面 → 图片模式不合格
- 多图输入未明确图一/图二角色分配 → 图片模式不合格
