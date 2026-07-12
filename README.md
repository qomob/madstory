# MadStory: 电影级影视分镜设计引擎 v3.6.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)
[![Version: 3.6.0](https://img.shields.io/badge/Version-3.6.0-green.svg)](https://clawhub.ai/qomob/mad-story)

**MadStory** 是一款电影级影视分镜设计引擎。它将模糊的创作意图，通过 9 阶段专业推导流程，逐步转化为包含构图、运镜、光影、表演调度、声音设计等全维度细节的专业分镜提示词。

- **原生平台**: Seedance 2.0 (视频) + Seedream 4.x/5.x (图片)
- **兼容输出**: Runway / Kling / Sora（参数需用户自行适配）

## 与其他 AI 分镜工具的区别

| 维度 | 典型 AI 分镜工具 | MadStory v3.6 |
|------|----------------|---------------|
| **专业理论** | 提示词模板堆砌 | 电影导演工作流：表演调度 + 剪辑理论 + 声音分类论 |
| **知识诚实** | 声称支持所有功能 | 区分 `[模型可执行]` vs `[导演参考]`，不假装 AI 能做它做不到的事 |
| **学习能力** | 静态知识库 | DEFECT_LOG 反馈回路——从每次生成结果中持续优化 |
| **平台诚实** | "支持所有平台" | 原生 vs 兼容分层声明 + 规则版本锁定 |
| **模型限制** | 隐藏缺陷 | 公开声明 5 类已知限制及对策 |

## v3.6.0 更新内容

- **新增 生成结果反馈回路 (DEFECT_LOG)**: 用户返回生成缺陷 → 按 Mode 累积 → 下次生成自动增强 Negative Prompt 和 KNOWN_RISKS。从静态知识库变成动态经验库
- **新增 AI 模型真实限制声明**: 公开声明时长衰减(8-12s)、复杂动作不稳定、跨镜头一致性靠运气等 5 类已知限制及对策
- **新增 规则版本锁定**: 所有规则标注验证平台版本，平台升级后用户可判断哪些规则仍有效
- **新增 AI 可执行性标注**: Phase 3.5/2/6 每项内容标注 `[模型可执行]` 或 `[导演参考]`，区分"AI 能做到"和"仅供创作决策"
- **新增 Phase 3.5 表演与调度**: 走位(Blocking)、视线匹配(Eyeline)、反应镜头策略、潜台词表演(Subtext)
- **新增 剪辑理论集成**: Phase 2 接入 L-Cut/J-Cut/Jump Cut/Match Cut/Smash Cut/Montage + 景别递进 + 180 度线规则
- **新增 Tournament 评分 Rubric**: 3 维加权（独特性 40% + 一致性 30% + 情感 30%）+ 安全方案惩罚 + 防同质化规则
- **新增 Phase 0 时长充分性检查**: 主动评估 15s 是否够用，不够则建议拆分
- **新增 声音来源分类**: Diegetic / Non-Diegetic / Trans-diegetic 三层决策
- **优化 数据架构**: 删除 5 个冗余 JSON 文件，cheat_sheet.json 成为唯一数据源
- **优化 平台声明**: 区分原生支持（Seedance/Seedream）与兼容输出（Runway/Kling/Sora）
- **优化 短剧工作流**: 明确 Stage A-H 为主线、Phase 0-7 为子流程的映射关系
- **优化 提示词工程文件**: 消除 prompt_engineering.md 与 seedance_v2_rules.md 40% 内容重复
- **优化 清理 5 处 no-op**: 将空泛指导替换为可执行规则

## 9 种创作模式

| 模式 | 适用场景 | 输入方式 | 核心约束 |
|------|---------|----------|------------------|
| **电影创意探索** | 概念开发、风格实验 | Text-to-Video | Generate-and-Filter + Tournament 筛选 |
| **电商产品** | 商品详情页、主图动效 | Image-to-Video | 产品几何不变形、标签可读 |
| **UGC 原生广告** | 信息流投放、口播种草 | Reference-to-Video | 人脸一致、手势自然 |
| **电影感品牌短片** | 品牌故事片、发布预告 | Text-to-Video | 镜头意图明确、灯光有逻辑 |
| **多镜头叙事** | 完整叙事弧线 | Reference-to-Video | ≤3 镜头/次，含剪辑理论应用 |
| **一镜到底** | 产品体验、空间巡游 | Image-to-Video | 2-10 张图片，空间连续 |
| **爆款复刻** | 灵感翻拍、竞品复刻 | Reference-to-Video | 风格还原、主体替换 |
| **Agent 模式** | 零基础创作 | Text-to-Video | 一句话到成片，自动规划 |
| **短剧创作** | AI 短剧、漫剧、小说改编 | Reference-to-Video | Stage A-H 主线 + Phase 子流程 |

## 分镜推导流程 (Phase 0-7 + 3.5)

| Phase | 内容 | 产出 |
|-------|------|------|
| **Phase 0** | 模式选择与意图澄清 | Mode 确认 + 输入策略 + **时长充分性评估** |
| **Phase 1** | 核心创意锁定 | Subject + Action |
| **Phase 2** | 时间轴与节奏 | Timeline + 关键帧 + **剪辑策略标注** |
| **Phase 3** | 视觉构图 | Composition + 画幅 |
| **Phase 3.5** | 表演与调度 | Performance Notes（走位/视线/反应镜头/潜台词，含可执行性标注） |
| **Phase 4** | 镜头运动 | Camera + Motion Strength |
| **Phase 5** | 光影与质感 | Lighting + 风格预设 |
| **Phase 6** | 声音设计 | Sound + BGM（含 diegetic/non-diegetic 分类） |
| **Phase 7** | 最终合成与输出 | 完整提示词 + Negative Prompt + **KNOWN_RISKS + DEFECT_LOG 模板** |

## AI 模型真实限制

> 完整说明见 SKILL.md「AI 模型真实限制」章节

| 限制 | 对策 |
|------|------|
| 8-12s 后画面质量衰减 | 优先 10s 以内；必须 15s 时标注"8s 后质量风险区" |
| 复杂动作不稳定 | 用"慢""连续""稳定"修饰；复杂动作用剪辑衔接 |
| 跨镜头一致性靠运气 | 每次生成后检查；接受"相似"而非"相同" |
| Motion Strength 高值易触发变形 | 从低值(2-3)开始，确认稳定后逐步调高 |
| Negative Prompt 非万能 | 记录 DEFECT_LOG 持续增强防护 |

## 生成结果反馈回路

```
Phase 7 输出提示词 → 用户生成视频 → 观察结果 → 报告缺陷
                                                    ↓
                                       DEFECT_LOG（按 Mode 累积）
                                                    ↓
                                       下次生成自动增强 Negative Prompt
                                       + 增加 KNOWN_RISKS 警告
```

## 目录结构

```text
mad-story/
├── SKILL.md                 # 技能定义 v3.6.0 — 分层加载/双模式/反馈回路
├── README.md                # 本文件
├── references/
│   ├── modes_detail.md      # 9种模式详细说明 + Tournament Rubric
│   ├── phases_detail.md     # Phase 0-7(+3.5) 推导指引 + AI可执行性标注
│   ├── prompt_engineering.md # 提示词结构索引（指向 seedance_v2_rules.md）
│   ├── seedance_v2_rules.md # Seedance 2.0 完整提示词工程规范
│   ├── seedream_4x_rules.md # Seedream 4.x/5.x 图片生成规范
│   ├── terminology.md       # 影视分镜专业术语库
│   ├── pre_flight_checklist.md # 导演级预检清单 + 元反思（8 维度）
│   ├── short_drama_consistency.md # 短剧全流程一致性管控 (Stage A-H)
│   ├── short_drama_genres.md # 短剧6大题材模板
│   └── examples/
│       ├── example_1_creative_film.md
│       ├── example_2_multi_shot.md
│       └── example_3_short_drama.md
└── assets/
    ├── cheat_sheet.json     # 参数速查表（单一数据源）
    └── storyboard_template.html # 分镜预览模板
```

## 如何使用

### 作为 AI Skill 触发
在 AI 助手中输入触发词即可：
`影视分镜` / `分镜设计` / `电影分镜` / `广告分镜` / `电商视频` / `UGC广告` / `品牌短片` / `多镜头叙事` / `一镜到底` / `爆款复刻` / `短剧创作` / `Seedance` / `Seedream` / `文生图` / `图生图` / `图像编辑` / `短剧剧本` / `微短剧` / `AI短剧` / `锁脸` / `小说改短剧` / `漫剧` / `角色人设`

### 用户能力分级

| 层级 | 推荐模式 | 使用路径 |
|------|---------|---------|
| **L1 入门** | Agent 模式 | 输入一句话 → 自动拆解 → 生成分镜方案 |
| **L2 基础** | 电商 / UGC | Phase 0-7 填空式引导 → 选项卡片 |
| **L3 进阶** | 多镜头 / 一镜到底 / 爆款复刻 | 手动编排多镜头序列 / 转场设计 |
| **L4 专业** | 电影感 / 短剧 | 全参数可控、多剧集批量 |
| **L5 导演级** | 所有模式 | 全链路创作、一致性管控、DEFECT_LOG 优化 |

## 示例输出

### 视频模式
```json
{
  "STANDARD_PROMPT": "雨夜赛博武士穿行霓虹街道，侧面跟拍，快速可控节奏，反光水洼，电影感红蓝对比色调",
  "NEGATIVE_PROMPT": "no shaky camera, no object melting, no random text, no muddy lighting, no flat blacks",
  "TIMELINE": "0-5s intro, 5-12s core action, 12-15s ending",
  "CAMERA": "side tracking dolly shot",
  "MOTION_STRENGTH": 5,
  "DURATION": "15s",
  "MODE": "电影感品牌短片",
  "KNOWN_RISKS": "8s 后质量风险区；Motion Strength=5 有中等变形风险",
  "DEFECT_LOG": "（用户返回后填写）"
}
```

### 图片模式 (Seedream 4.x/5.x)
```json
{
  "IMAGE_PROMPT": "一个穿着华丽服装的女孩，撑着遮阳伞走在林荫道上，莫奈油画风格",
  "TEXT_CONTENT": "\"Seedream 4.5\"",
  "MODE": "电影创意探索",
  "PLATFORM": "Seedream 4.5"
}
```

## 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>

---

## 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源协议。

---
**MadStory v3.6.0** — 电影级影视分镜设计引擎 | Created by **[qomob.ai](https://qomob.ai)** | [Install on ClawHub](https://clawhub.ai/qomob/mad-story)
