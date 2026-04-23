# 🎬 MadStory: 专业的影视分镜 AI 技能 (Seedance 2.0 驱动)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)
[![ClawHub: mad-story](https://img.shields.io/badge/ClawHub-Install-orange)](https://clawhub.ai/qomob/mad-story)

**MadStory** 是一款专为即梦 **Seedance 2.0** 多模态创作设计的影视分镜引导技能。它能将你模糊的电影构思，通过多轮专业对话，逐步推导为包含构图、运镜、光影、声音等全维度细节的专业分镜提示词（Prompts）。

## ✨ 核心特性

- 🚀 **Seedance 2.0 深度集成**: 完美支持图、影、音、文四模态输入逻辑。
- ⏱️ **15秒精准对齐**: 默认生成 15 秒时长分镜，支持 `--duration 15s` 参数自动优化。
- 📅 **逐秒级构思 (Timeline-based)**: 强制引入 15 秒时间轴概念，支持逐秒描述动态变化与关键帧。
- 🎭 **六阶段引导法**: 
  - **Phase 1**: 锁定核心创意 (Core Concept)
  - **Phase 2**: 规划时间轴与节奏 (Timeline & Rhythm) - *New!*
  - **Phase 3**: 确定视觉构图 (Visual Composition)
  - **Phase 4**: 设计逐秒动态运镜 (Dynamic Camera)
  - **Phase 5**: 营造光影与细节 (Lighting & Details)
  - **Phase 6**: 声音设计与最终合成 (Sound & Export)
- 📽️ **专业术语支持**: 内置影视工业级术语库，涵盖镜头焦距、运镜方式、光影氛围等。
- 🛠️ **可控性强**: 提供动态强度 (Motion Strength)、CFG Scale 等即梦核心参数建议。

## 📂 目录结构

```text
mad-story/
├── SKILL.md            # 技能定位、流程定义与交互准则
├── scripts/            # 自动化处理引擎 (Python)
├── references/         # 影视术语库与 Seedance 2.0 规范
├── assets/             # HTML 预览模板与参数速查表
├── README.md           # 项目说明文档
└── LICENSE             # MIT 开源协议
```

## 🛠️ 如何使用

1. **触发技能**: 在 AI 助手（如 OpenClaw、Trae）中输入 `MadStory`、`影视分镜` 或 `做个分镜`。
2. **多轮引导**:
   - 按照 Phase 1-6 的引导，提供您的创意、时间轴规划、构图、运镜等信息。
   - 特别注意：在 Phase 2 和 Phase 4 中，请尽量以“秒”为单位描述您的构思。
3. **获取产出**: 复制生成的标准提示词，直接在 [即梦官方网站](https://jimeng.com) 使用。

## 🌟 示例输出

> **分镜预览 (15s)**:
> - **提示词**: `Cinematic 15s shot: A cyber-samurai walking in rain... Timeline: 0-5s intro, 5-12s core action, 12-15s ending... Camera: 0-5s push in, 5-15s orbit... --duration 15s`
> - **参数建议**: 运动强度 (Motion Strength): 5 | CFG Scale: 7
> - **多模态**: 建议上传雨夜街头参考图以获得最佳光效。

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来优化分镜引导逻辑或术语库。

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="500" alt="XSkill">
</div>

---
Created with ❤️ by **[qomob.ai](https://qomob.ai)** | [Install on ClawHub](https://clawhub.ai/qomob/mad-story)
