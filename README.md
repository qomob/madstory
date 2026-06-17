# MadStory: 电影级影视分镜设计引擎 v3.4.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)
[![Version: 3.4.1](https://img.shields.io/badge/Version-3.4.1-green.svg)](https://clawhub.ai/qomob/mad-story)

**MadStory v3.4.1** 是一款电影级影视分镜设计引擎，支持多平台视频生成（Seedance / Runway / Kling / Sora）及图片生成（Seedream 4.x/5.x）。能将模糊的电影构思，通过 8 阶段专业推导流程，逐步转化为包含构图、运镜、光影、声音等全维度细节的专业分镜提示词。

## v3.4.1 更新内容

- **新增 焦段→情绪决策表** (`references/terminology.md`): 24/35/50/85/135mm 焦段与情绪暗示、适用 Mode 的映射，补齐摄影指导选焦段的决策依据
- **新增 剪辑技巧库** (`assets/cheat_sheet.json` → `editing_techniques`): L-Cut / J-Cut / Jump Cut / Match Cut / Smash Cut / Montage 六种剪辑手法的提示词模板，补齐 15s 短片节奏设计的术语缺口

## 核心特性

- **9 种创作模式**: 电影创意探索 / 电商产品 / UGC 原生广告 / 电影感品牌短片 / 多镜头叙事 / 一镜到底 / 爆款复刻 / Agent 全链路创作 / 短剧批量生产
- **8 阶段推导流程 (Phase 0-7)**: 从模式选择到最终合成，逐阶段引导
- **双模式输出**: 视频模式（5层提示词结构 + Negative Prompt）与图片模式（3层结构 + 文字渲染 + 图像编辑语法）独立定义
- **双模式质量门禁**: 视频模式与图片模式分别定义不合格判定条件
- **分层加载架构**: SKILL.md 始终加载，参考文献按交互阶段按需加载
- **短剧一致性管控**: 角色档案 + 场景清单 + 时间线轴 + 四阶段验收
- **电影级数据资产**: 导演风格参考 / 镜头语言 / 光影预设 / 声音设计 / 叙事结构

## 9 种创作模式

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

## 分镜推导流程 (Phase 0-7)

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

## 目录结构

```text
mad-story/
├── SKILL.md                 # 技能定义 v3.4.1 — 分层加载/双模式输出
├── README.md                # 本文件
├── references/
│   ├── modes_detail.md      # 9种模式详细说明 (Layer 1)
│   ├── phases_detail.md     # Phase 0-7 详细推导指引 (Layer 1)
│   ├── prompt_engineering.md # 视频提示词5层结构+Negative Prompt (Layer 1)
│   ├── seedance_v2_rules.md # Seedance 2.0 提示词工程规范 (Layer 1)
│   ├── seedream_4x_rules.md # Seedream 4.x/5.x 图片生成规范 (Layer 1)
│   ├── terminology.md       # 影视分镜专业术语库 (Layer 1)
│   ├── pre_flight_checklist.md # 导演级预检清单 (Layer 1)
│   ├── short_drama_consistency.md # 短剧全流程一致性管控 (Layer 2)
│   ├── short_drama_genres.md # 短剧6大题材模板 (Layer 1)
│   └── examples/
│       ├── example_1_creative_film.md
│       ├── example_2_multi_shot.md
│       └── example_3_short_drama.md
└── assets/
    ├── cheat_sheet.json     # 参数速查表 — 镜头语言/光影/声音/导演参考
    ├── cs_core.json         # 核心数据资产
    ├── cs_cinematic.json    # 电影感数据
    ├── cs_drama.json        # 短剧数据
    ├── cs_narrative.json    # 叙事结构数据
    ├── cs_sound.json        # 声音设计数据
    └── storyboard_template.html # 分镜预览模板
```

> 独立工具包（CLI/API/验证）位于 `tools/mad-story-scripts/`，非技能运行时必需，按需使用。

## 如何使用

### 作为 AI Skill 触发
在 AI 助手中输入触发词即可：
`MadStory` / `影视分镜` / `分镜设计` / `电影分镜` / `广告分镜` / `电商视频` / `UGC广告` / `品牌短片` / `多镜头叙事` / `一镜到底` / `爆款复刻` / `短剧创作` / `从一句话出片` / `AI电影` / `AI视频生成` / `Seedance` / `Seedream` / `分镜脚本` / `视频提示词` / `文生图` / `图生图` / `图像编辑` / `参考图生图` / `短剧剧本` / `微短剧` / `竖屏剧` / `AI短剧` / `短剧分镜` / `短剧编剧` / `锁脸` / `小说改短剧` / `漫剧` / `角色人设`

### 用户能力分级
| 层级 | 推荐模式 | 使用路径 |
|------|---------|---------|
| **L1 入门** | Agent 模式 | 输入一句话 → 自动拆解 → 生成分镜方案 |
| **L2 基础** | 电商 / UGC | Phase 0-7 填空式引导 → 选项卡片 |
| **L3 进阶** | 多镜头 / 一镜到底 / 爆款复刻 | 手动编排多镜头序列 / 转场设计 |
| **L4 专业** | 电影感 / 短剧 | 全参数可控、多剧集批量 |
| **L5 导演级** | 所有模式 | 全链路创作、一致性管控 |

### CLI 工具包（独立部署）
独立工具包位于 `tools/mad-story-scripts/`，提供 CLI 批量生成、REST API 服务、质量校验等功能：
```bash
cd tools/mad-story-scripts/
pip install -r requirements.txt  # 仅 API 模式需要
python3 mad_story_engine.py --interactive
python3 api_server.py --port 8787
```

## 短剧一致性管控方案

针对单集 3~5 分钟短剧，单条 >15s 拍摄脚本自动启用全流程一致性管控：

| 阶段 | 管控内容 |
|------|---------|
| **前期筹备** | 人物设定档案（外观/性格/行为/台词/时间线）、场景全景清单（空间/陈设/光线/色温/噪音/道具）、全片时间线轴（>15s 自动拆分标记） |
| **拍摄执行** | 开拍前对照核查、每 10~12s 校验节点 + Reference Frame、环境参数同步留存 |
| **后期制作** | 剪辑逐帧核查、调色统一、音轨对齐 |
| **最终验收** | 人物外观无矛盾 / 行为逻辑无冲突 / 场景空间无冲突 / 拼接自然（4 项硬性标准） |

## 示例输出

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

## 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源协议。

---
**MadStory v3.4.1** — 电影级影视分镜设计引擎 | Created by **[qomob.ai](https://qomob.ai)** | [Install on ClawHub](https://clawhub.ai/qomob/mad-story)
