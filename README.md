# MadStory: 电影级影视分镜设计引擎 v3.2 (Harness Engineering Powered)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)
[![Version: 3.2](https://img.shields.io/badge/Version-3.2.0-green.svg)](https://clawhub.ai/qomob/mad-story)
[![ClawHub: mad-story](https://img.shields.io/badge/ClawHub-Install-orange)](https://clawhub.ai/qomob/mad-story)

**MadStory v3.2** 是一款 **电影级影视分镜设计引擎**，融合 **Harness Engineering 工程哲学**（PPAF 循环 + R.E.S.T 可靠性模型）。支持多平台视频生成（Seedance / Runway / Kling / Sora）**及图片生成（Seedream 4.x/5.x）**，能将你模糊的电影构思，通过专业推导流程，逐步转化为包含构图、运镜、光影、声音等全维度细节的专业分镜提示词。

## 核心特性 (v3.2 新增)

- **Seedream 4.x/5.x 图片生成**: 文生图、图像编辑（增加/删除/替换/修改）、参考图生图（4种参考类型）、多图输入/输出、知识可视化
- **分层懒加载架构**: SKILL.md 始终加载，其他资源按交互阶段按需加载，视频场景零图片内容 token 开销
- **双模式输出规范**: 视频模式（5层提示词结构 + Negative Prompt）与图片模式（3层结构 + 文字渲染 + 图像编辑语法）独立定义
- **双模式质量门禁**: 视频模式与图片模式分别定义质量不合格条件
- **图片模式预检清单**: 新增 Seedream 4.x/5.x 专项预检项（文字渲染、编辑指令、参考图类型等）

## 核心特性 (v3.0)

- **9 种创作模式**: 电影创意探索 / 电商产品 / UGC 原生广告 / 电影感品牌短片 / 多镜头叙事 / 一镜到底 / 爆款复刻 / Agent 全链路创作 / 短剧批量生产
- **Harness Engineering 融合**: PPAF 循环状态追踪 + R.E.S.T 四维合规检查 + 失败降级路径 (Design for Failure)
- **多平台适配层**: 解耦单一平台依赖，支持 Seedance 2.0 / Runway Gen-3 / Kling / Sora 参数自动映射与约束校验
- **LLM Router v2 增强**: 多意图拆分(Classify-and-Act) + Tournament 创意评分 + 语义解析增强（导演参照/视觉隐喻/反套路检测）
- **电影级数据资产**: 导演风格参考库(5位大师) / 电影镜头语言(7种景别+12种运镜+7种构图) / 光影预设(9种情绪布光) / 声音设计(6种情感映射+5位导演签名) / 叙事结构(7种模式)
- **暗色电影级 UI**: 分镜预览模板升级 — 时间轴可视化 + 多镜头序列图形展示 + PPAF 循环指示器
- **API 安全加固**: Session TTL (30min) + 滑动窗口限流 (60 req/min)

##  9 种创作模式

| 模式 | 适用场景 | 输入方式 | 核心约束 / 工作流 |
|------|---------|----------|------------------|
| **电影创意探索** | 概念开发、风格实验、艺术短片、品牌概念片 | Text-to-Video | Generate-and-Filter + Tournament 筛选 |
| **电商产品** | 商品详情页、主图动效、付费素材 | Image-to-Video | 产品几何不变形、标签可读 |
| **UGC 原生广告** | 信息流投放、口播、种草测评 | Reference-to-Video | 人脸一致、手势自然 |
| **电影感品牌短片** | 品牌故事片、发布预告 | Text-to-Video | 镜头意图明确、灯光有逻辑 |
| **多镜头叙事** | 完整叙事弧线、品牌故事 | Reference-to-Video | ≤3 镜头/次生成，跨镜头一致 |
| **一镜到底** | 产品体验、空间巡游 | Image-to-Video | 2-10 张图片，空间连续 |
| **爆款复刻** | 灵感来源、竞品翻拍 | Reference-to-Video | 风格还原、主体替换自然 |
| **Agent 模式** | 零基础创作、有脚本/素材 | Text-to-Video | 一句话到成片，自动规划 |
| **短剧创作** | AI 短剧生产、漫剧、小说改编 | Reference-to-Video | 跨集角色一致、>15s 一致性管控 |

##  分镜推导流程 (Phase 0-7)

| Phase | 内容 | 产出 |
|-------|------|------|
| **Phase 0** | 模式选择与意图澄清 | Mode 确认 + 输入策略 |
| **Phase 1** | 核心创意锁定 | Subject + Action 描述 |
| **Phase 2** | 时间轴与节奏 | Timeline 描述 + 关键帧 |
| **Phase 3** | 视觉构图 | Composition + 画幅建议 |
| **Phase 4** | 镜头运动 | Camera 描述 + Motion Strength |
| **Phase 5** | 光影与质感 | Lighting + 风格预设 |
| **Phase 6** | 声音设计 | Sound + BGM 建议 |
| **Phase 7** | 最终合成与参数输出 | 完整提示词 + Negative Prompt + 多模态建议 |

##  目录结构

```text
mad-story/
├── SKILL.md                 # 技能定义 v3.2 — 双模式/分层懒加载/Harness架构
├── README.md                # 本文件
├── scripts/
│   ├── mad_story_engine.py  # 核心引擎 + PPAFState/RESTCompliance/FailurePath
│   ├── platform_adapter.py  # 多平台适配层 (Seedance/Runway/Kling/Sora/Seedream)
│   ├── llm_router.py        # LLM Router v2 — 多意图拆分/Tournament/Classify-and-Act
│   ├── director_validator.py # 导演级核验工具 (271项全模式边界测试)
│   ├── api_server.py        # REST API + WebSocket (安全加固: TTL+限流)
│   └── batch_runner.py      # 目录级批量生产流水线
├── references/
│   ├── modes_detail.md      # 9种模式详细说明 (Layer 1 按需加载)
│   ├── phases_detail.md     # Phase 0-7 详细推导指引 (Layer 1)
│   ├── prompt_engineering.md # 视频提示词5层结构+Negative Prompt (Layer 1)
│   ├── seedance_v2_rules.md # Seedance 2.0 提示词工程规范 (Layer 1)
│   ├── seedream_4x_rules.md # Seedream 4.x/5.x 图片生成规范 (Layer 1, v3.2 NEW)
│   ├── terminology.md       # 影视分镜专业术语库 (Layer 1)
│   ├── pre_flight_checklist.md # 导演级预检清单 (含图片模式预检, Layer 1)
│   ├── short_drama_consistency.md # 短剧全流程一致性管控 (Layer 2)
│   └── examples/            # 电影级端到端案例
│       ├── example_1_creative_film.md
│       ├── example_2_multi_shot.md
│       └── example_3_short_drama.md
└── assets/
    ├── cheat_sheet.json     # 参数速查表 v3 — 含电影级镜头语言/光影/声音/导演参考
    └── storyboard_template.html # 分镜预览模板 v3 — 暗色UI/时间轴可视化/镜头序列
```

## ️ 如何使用

### 作为 AI Skill 触发
在 AI 助手中输入触发词即可：
`MadStory` / `影视分镜` / `分镜设计` / `电商视频` / `UGC广告` / `品牌短片` / `多镜头叙事` / `一镜到底` / `爆款复刻` / `短剧创作` / `从一句话出片` / `Seedream` / `文生图` / `图像编辑` / `参考图生图` / `AI绘图` / `AI生图`

### CLI 命令行
```bash
# 交互式引导
python3 scripts/mad_story_engine.py --interactive

# 一键生成
python3 scripts/mad_story_engine.py --mode cinematic --concept "雨夜赛博武士" --output result.json --html preview.html

# 短剧模式
python3 scripts/mad_story_engine.py --mode short_drama --script 剧本.txt --output drama.json

# 批量生产
python3 scripts/batch_runner.py ./input_specs/ ./output/

# 校验 & 一致性验收
python3 scripts/director_validator.py --validate result.json
python3 scripts/director_validator.py --check-consistency drama.json
```

### REST API
```bash
pip install fastapi uvicorn pydantic
python3 scripts/api_server.py --port 8787
```

### 用户能力分级
| 层级 | 推荐模式 | 使用路径 |
|------|---------|---------|
| **L1 入门** | Agent 模式 | 输入一句话 → 自动拆解 → 生成分镜方案 |
| **L2 基础** | 电商 / UGC | Phase 0-7 填空式引导 → 选项卡片 |
| **L3 进阶** | 多镜头 / 一镜到底 / 爆款复刻 | 手动编排多镜头序列 / 转场设计 |
| **L4 专业** | 电影感 / 短剧 | 全参数可控、多剧集批量 |
| **L5 导演级** | 所有模式 + CLI 批量 | `--interactive` / `--validate` 全链路 |

##  短剧一致性管控方案

针对单集 3~5 分钟短剧，单条 >15s 拍摄脚本自动启用全流程一致性管控：

| 阶段 | 管控内容 |
|------|---------|
| **前期筹备** | 人物设定档案（外观/性格/行为/台词/时间线）、场景全景清单（空间/陈设/光线/色温/噪音/道具）、全片时间线轴（>15s 自动拆分标记） |
| **拍摄执行** | 开拍前对照核查、每 10~12s 校验节点 + Reference Frame、环境参数同步留存 |
| **后期制作** | 剪辑逐帧核查、调色统一、音轨对齐 |
| **最终验收** | 人物外观无矛盾 / 行为逻辑无冲突 / 场景空间无冲突 / 拼接自然（4 项硬性标准） |

##  示例输出

### 视频模式
```json
{
  "STANDARD_PROMPT": "雨夜赛博武士穿行霓虹街道，侧面跟拍，快速可控节奏，反光水洼，电影感红蓝对比色调",
  "NEGATIVE_PROMPT": "no shaky camera, no object melting, no random text, no muddy lighting, no flat blacks",
  "TIMELINE": "0-5s intro, 5-12s core action, 12-15s ending",
  "CAMERA": "Second-by-second: 0-5s intro, 5-12s core action, 12-15s ending. Camera: side tracking dolly shot.",
  "MOTION_STRENGTH": 5,
  "DURATION": "15s",
  "MODE": "电影感品牌短片",
  "MODE_KEY": "cinematic",
  "MULTI_MODAL_ADVICE": "建议上传具有相似色调和光位的高质量参考图以获得最佳光效",
  "SOUND_DESIGN": "ambient drone",
  "SHOT_LIST": []
}
```

### 图片模式 (Seedream 4.x/5.x)
```json
{
  "IMAGE_PROMPT": "一个穿着华丽服装的女孩，撑着遮阳伞走在林荫道上，莫奈油画风格，柔和光影，印象派色彩",
  "TEXT_CONTENT": "\"Seedream 4.5\"",
  "REFERENCE_TYPE": "无",
  "EDIT_OPERATION": "无",
  "MULTI_IMAGE_OP": "无",
  "MODE": "电影创意探索",
  "PLATFORM": "Seedream 4.5"
}
```

##  质量保障

`director_validator.py` 内置 **271 项** 全模式核验用例，覆盖：

- 输出结构完整性 (所有 8 模式)
- Negative Prompt 合规性扫描
- 边界条件测试 (空输入/无效模式/全空字段)
- 镜头运动约束强制 (单运动原则)
- 一镜到底/爆款复刻/Agent 模式引擎边界
- 一致性管控台账 + 校验器全流程 (B1-D4)
- 短剧长戏份一致性
- 资源文件完整性 & 模式枚举完整性

##  ️ CLI 参数参考

| 参数 | 说明 |
|------|------|
| `--mode, -m` | 创作模式 (creative_film/ecommerce/ugc/cinematic/multi_shot/one_shot/viral_replicate/agent_mode/short_drama) |
| `--concept, -c` | 核心创意描述 |
| `--output, -o` | 输出 JSON 文件路径 |
| `--html` | 输出 HTML 预览文件路径 |
| `--validate` | 校验已生成的 JSON 输出 |
| `--check-consistency` | 短剧一致性最终验收 |
| `--script` | 短剧剧本文件路径 |
| `--interactive, -i` | 交互式引导模式 |
| `--session` / `--load` | Session 持久化 |
| `--list-modes` | 列出所有模式 |

## 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>

##  贡献与反馈

欢迎提交 Issue 或 Pull Request 来优化分镜引导逻辑或术语库。

##  许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源协议。

---
**MadStory v3.2** — 电影级影视分镜设计引擎 | Harness Engineering Powered | Created by **[qomob.ai](https://qomob.ai)** | [Install on ClawHub](https://clawhub.ai/qomob/mad-story)
