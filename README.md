# 🎬 MadStory: 专业的影视分镜 AI 技能 (Seedance 2.0 驱动)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author: qomob.ai](https://img.shields.io/badge/Author-qomob.ai-blue)](https://qomob.ai)

**MadStory** 是一款专为即梦 **Seedance 2.0** 多模态创作设计的影视分镜引导技能。它能将你模糊的电影构思，通过多轮专业对话，逐步推导为包含构图、运镜、光影、声音等全维度细节的专业分镜提示词（Prompts）。

## ✨ 核心特性

- 🚀 **Seedance 2.0 深度集成**: 完美支持图、影、音、文四模态输入逻辑。
- 🎭 **六阶段引导法**: 从核心创意到进阶创作，一步步带你从“外行”变成“导演”。
- 📽️ **专业术语支持**: 内置影视工业级术语库，涵盖镜头焦距、运镜方式、光影氛围等。
- 📊 **可视化输出**: 生成精美的 HTML 分镜预览卡片，让方案一目了然。
- 🛠️ **可控性强**: 提供动态强度（Motion Strength）、CFG Scale 等即梦核心参数建议。

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

1. **触发技能**: 在 AI 助手（如 OpenClaw、Trae）中输入 `MadStory` 或 `影视分镜`。
2. **多轮引导**:
   - **Phase 1**: 锁定核心创意 (Core Concept)
   - **Phase 2**: 确定视觉构图 (Visual Composition)
   - **Phase 3**: 设计动态运镜 (Dynamic Camera)
   - **Phase 4**: 营造光影氛围 (Lighting & Atmosphere)
   - **Phase 5**: 规划声音设计 (Sound Design)
   - **Phase 6**: 导出最终方案 (Final Export)
3. **获取产出**: 复制生成的标准提示词，直接在 [即梦官方网站](https://jimeng.com) 使用。

## 🌟 示例输出

> **分镜预览**:
> - **提示词**: `Cinematic shot: A cyber-samurai walking in rain, neon lights reflection, eye-level, slow push-in camera, 35mm lens, high contrast...`
> - **参数建议**: 运动强度 (Motion Strength): 5 | CFG Scale: 7
> - **多模态**: 建议上传雨夜街头参考图以获得最佳光效。

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来优化分镜引导逻辑或术语库。

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---
Created with ❤️ by **[qomob.ai](https://qomob.ai)**
