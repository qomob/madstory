# MadStory: 电影级影视分镜设计引擎 v3.8.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)
[![Version: 3.8.0](https://img.shields.io/badge/Version-3.8.0-green.svg)](https://clawhub.ai/qomob/mad-story)

**MadStory** 是一款电影级影视分镜设计引擎。它将模糊的创作意图，通过 8 阶段专业推导流程，逐步转化为包含构图、运镜、光影、表演调度、声音设计等全维度细节的专业分镜提示词。

- **原生平台**: Seedance 2.5（默认）/ 2.0（降级）(视频) + Seedream 4.x/5.x/5.0 Pro (图片)
- **兼容输出**: Runway / Kling / Sora（参数需用户自行适配）

## 与其他 AI 分镜工具的区别

| 维度 | 典型 AI 分镜工具 | MadStory v3.8 |
|------|----------------|---------------|
| **专业理论** | 提示词模板堆砌 | 电影导演工作流：表演调度 + 剪辑理论 + 声音分类论 |
| **知识诚实** | 声称支持所有功能 | 区分 `[模型可执行]` vs `[导演参考]`，不假装 AI 能做它做不到的事 |
| **学习能力** | 静态知识库 | DEFECT_LOG 反馈回路——从每次生成结果中持续优化 |
| **平台诚实** | "支持所有平台" | 原生 vs 兼容分层声明 + 规则版本锁定 + **双版本策略(2.5默认/2.0降级)** |
| **模型限制** | 隐藏缺陷 | 公开声明已知限制及对策，**2.5 vs 2.0 双版本对照** |

## v3.8.0 更新内容

- **新增 Seedance 2.5 全面能力内化（默认基准）**：30s 原生生成、180s 超长视频、60s 视频延长、时间戳帧级控制、50 多模态参考（30图+10视频+10音频）、智能编辑、白模预演、绿幕合成、BGM 分离、多语种（10+ 语种）、多人参考、无缝转场、多宫格分镜
- **新增 双版本策略**：2.5 为默认基准，2.0 降级为成本敏感备选。所有规则/参数/质量门禁基于双版本对照校准
- **新增 2 个创作模式（9→11）**：Mode 9 智能编辑（局部消除/替换/空间视角修改/BGM分离/绿幕）、Mode 10 白模预演（Maya/Blender 粗/细颗粒度渲染）
- **新增 4 段式提示词主公式**：素材描述+一句话概述+具体情节+全局补充。原 5 层结构降级为元素完整性检查清单
- **新增 专项公式索引**：7 维人物公式、30s 3 模块公式、超长视频公式、视频延长公式、智能编辑公式、白模公式、时间戳控制公式
- **新增 seedance_25_rules.md**：2.5 完整规则独立文件（参数规格/16项能力/转场表/Negative禁止项/AI限制2.5改善对照）
- **升级 Negative Prompt**：2.5 用"禁止"表述响应更好（2.0 仍用 `no xxx`）
- **升级 现有 9 个模式**：均新增「2.5 能力增强」小节，标注各自可用的 2.5 新能力

## v3.7.0 更新内容

- **新增 Seedream 5.0 Pro 全部专属能力**: 交互式精准编辑（坐标/框选/标注框）、高密度信息呈现、原生多语种文字渲染、影视感自动增强、人像质感（毛孔级）、Visual CoT 空间推理、多轮对话式编辑、PNG 透明背景输出
- **新增 版本能力对照速查表**: 4.0/4.5/5.0 Lite/5.0 Pro 四版本 14 项能力对比矩阵
- **优化 seedream_4x_rules.md**: 从覆盖 4.0-5.0 Lite 扩展为 4.0-5.0 Pro，新增 §8.5（8 个 Pro 专属子章节）+ §9（版本对照表）+ §10.8（Pro 专属示例）

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

## 11 种创作模式

| 模式 | 适用场景 | 输入方式 | 核心约束 |
|------|---------|----------|------------------|
| **电影创意探索** | 概念开发、风格实验 | Text-to-Video | Generate-and-Filter + Tournament 筛选 |
| **电商产品** | 商品详情页、主图动效 | Image-to-Video | 产品几何不变形、标签可读 |
| **UGC 原生广告** | 信息流投放、口播种草 | Reference-to-Video | 人脸一致、手势自然 |
| **电影感品牌短片** | 品牌故事片、发布预告 | Text-to-Video | 镜头意图明确、灯光有逻辑 |
| **多镜头叙事** | 完整叙事弧线、超长叙事 | Reference-to-Video | 跨镜头一致、2.5支持超长180s/延长60s/无缝转场 |
| **一镜到底** | 产品体验、空间巡游 | Image-to-Video | 2-10 张图片，空间连续，2.5支持30s长一镜 |
| **爆款复刻** | 灵感翻拍、竞品复刻 | Reference-to-Video | 风格还原、主体替换、迁移创意/绿幕/BGM分离 |
| **Agent 模式** | 零基础创作 | Text-to-Video | 一句话到成片，自动规划（含超长/编辑/白模路由） |
| **短剧创作** | AI 短剧、漫剧、小说改编 | Reference-to-Video | Stage A-H 主线 + Phase 子流程、多人参考/音色/多语种出海 |
| **智能编辑** ⭐ | 局部消除/替换/视角修改/BGM分离 | Video(已有) | 精准定位防误伤、保留不变要素声明 |
| **白模预演** ⭐ | Maya/Blender 白模渲染、分镜预演 | Video(白模)+Image | 镜头/空间/走位精准、粗/细颗粒度 |

> ⭐ = 2.5 专属新增模式，降级 2.0 时不可用

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
| **Phase 7** | 最终合成与输出 | 完整提示词(4段式) + ENGINE_VERSION + Negative Prompt + **TIMESTAMP_CONTROL + KNOWN_RISKS + DEFECT_LOG 模板** |

## AI 模型真实限制（2.5 vs 2.0 双版本对照）

> 完整说明见 SKILL.md「AI 模型真实限制」章节 + `seedance_25_rules.md` §8

| 限制 | 2.0 表现 | 2.5 改善 | 对策 |
|------|---------|---------|------|
| **时长衰减** | 8-12s 后质量下降，15s 末段纹理崩坏 | 30s 保持一致性 | 2.5 可放心用 30s；2.0 仍优先 ≤10s |
| **复杂动作不稳定** | 开门/打斗/转身易变形 | 长尾动作解锁，复杂物理交互流畅 | 2.5 可尝试复杂动作；2.0 用"慢""稳定"修饰+剪辑绕开 |
| **跨镜头一致性** | 靠运气 | 切镜一致性显著提升 | 2.5 多镜头更可靠；2.0 仍需多次生成取最佳 |
| **Motion Strength 偏差** | 高值(≥6)易变形 | 仍需注意 | 从低值(2-3)开始，确认稳定后再调高 |
| **Negative 响应** | 不稳定，写了 `no face drift` 仍会 drift | 大幅优化，"禁止"表述响应更好 | 2.5 用"禁止"表述；2.0 用 `no xxx`；生成后仍需人工检查 |
| **多人双胞胎** | 多人同框长相趋同、换脸错位 | 多人参考升级解决 | 2.5 多人场景用多人参考；2.0 避免多人同框 |
| **多语种** | 发音不准/不支持长素材 | 10+ 语种原生，口型字幕对齐 | 多语种必须用 2.5 |
| **Negative 非万能** | — | — | 记录 DEFECT_LOG 持续增强防护 |

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
├── SKILL.md                 # 技能定义 v3.8.0 — 分层加载/双版本(2.5默认+2.0降级)/11模式
├── README.md                # 本文件
├── references/
│   ├── seedance_25_rules.md # Seedance 2.5 完整规则（默认基准） (Layer 1)
│   ├── modes_detail.md      # 11种模式详细说明 + Tournament Rubric + 2.5能力增强
│   ├── phases_detail.md     # Phase 0-7(+3.5) 推导指引 + AI可执行性标注 + 时间戳控制
│   ├── prompt_engineering.md # 4段式主公式+专项公式索引+5层元素检查清单 (Layer 1)
│   ├── seedance_v2_rules.md # Seedance 2.0 提示词工程规范（降级备选）
│   ├── seedream_4x_rules.md # Seedream 4.x-5.0 Pro 图片生成规范（含 5.0 Pro 专属能力）
│   ├── terminology.md       # 影视分镜专业术语库
│   ├── pre_flight_checklist.md # 导演级预检清单 + 元反思（8 维度）+ Mode 9/10 专项
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
`影视分镜` / `分镜设计` / `电影分镜` / `广告分镜` / `电商视频` / `UGC广告` / `品牌短片` / `多镜头叙事` / `一镜到底` / `爆款复刻` / `短剧创作` / `Seedance` / `Seedream` / `文生图` / `图生图` / `图像编辑` / `短剧剧本` / `微短剧` / `AI短剧` / `锁脸` / `小说改短剧` / `漫剧` / `角色人设` / `时间戳控制` / `超长视频` / `视频延长` / `局部编辑` / `智能编辑` / `白模` / `绿幕` / `BGM分离` / `多语种` / `多宫格分镜`

### 用户能力分级

| 层级 | 推荐模式 | 使用路径 |
|------|---------|---------|
| **L1 入门** | Agent 模式 | 输入一句话 → 自动拆解 → 生成分镜方案 |
| **L2 基础** | 电商 / UGC | Phase 0-7 填空式引导 → 选项卡片 |
| **L3 进阶** | 多镜头 / 一镜到底 / 爆款复刻 | 手动编排多镜头序列 / 转场设计 |
| **L4 专业** | 电影感 / 短剧 / 多镜头 | 全参数可控、多剧集批量、超长视频/时间戳控制 |
| **L5 导演级** | 所有模式（含智能编辑/白模预演） | 全链路创作、一致性管控、DEFECT_LOG 优化、双版本策略切换 |

## 示例输出

### 视频模式
```json
{
  "ENGINE_VERSION": "Seedance 2.5",
  "STANDARD_PROMPT": "【素材描述】@图片1 锁定主角面部特征。【一句话概述】雨夜赛博武士穿行霓虹街道，侧面跟拍，电影感红蓝对比色调。【具体情节描述】0-10s 武士从巷口缓步走出，霓虹光斑在积水倒影中闪烁；10-20s 侧跟拍，武士拔刀转身，雨丝被刀锋切开；20-30s 收刀入鞘，镜头拉远揭示赛博城市全景。【全局补充】机位保持侧面平移跟拍；环境为雨夜霓虹街道，湿润反光质感；整体低频电子音效+雨声；电影感红蓝对比色调。禁止生成字幕、禁止生成 BGM、禁止物体融化。",
  "NEGATIVE_PROMPT": "禁止镜头抖动、禁止物体融化、禁止随机文字、禁止浑浊光影、禁止死黑",
  "TIMELINE": "0-10s 入场, 10-20s 核心动作, 20-30s 收尾",
  "TIMESTAMP_CONTROL": "[0-10s] 入场：中景+三分法构图+武士缓步走出 / 潜台词：孤独感的建立\n[10-20s] 核心：近景+跟拍+拔刀转身 / 潜台词：紧张感升级\n[20-30s] 收尾：全景+拉远+收刀入鞘揭示城市 / 潜台词：渺小与宏大对比",
  "CAMERA": "侧面平移跟拍 dolly shot，20s 后拉远",
  "MOTION_STRENGTH": 5,
  "DURATION": "30s",
  "MODE": "电影感品牌短片",
  "MULTI_MODAL_ADVICE": "@图片1(主角面部) 1-8张效果好；可选 @音频1(低频电子配乐参考)",
  "KNOWN_RISKS": "2.5 30s 一致性良好；Motion Strength=5 有中等变形风险",
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
**MadStory v3.8.0** — 电影级影视分镜设计引擎 | Created by **[qomob.ai](https://qomob.ai)** | [Install on ClawHub](https://clawhub.ai/qomob/mad-story)
