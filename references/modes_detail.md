# 创作模式详情 (Layer 1 — 按需加载)

> 本文件包含 9 种创作模式的完整说明。仅在用户确认模式后加载当前模式的详情。

---

## Mode 0: 电影创意探索 (Creative Film)
- **场景**: 概念开发、风格实验、灵感发散、艺术短片、品牌概念片前期探索
- **核心能力**: 风格混搭建议、意外转场推荐、情绪反差提案、视觉隐喻生成、导演视角切换
- **Harness 机制**: 采用 **Generate-and-Filter + Tournament** 模式——先生成多个创意方向，再通过评分矩阵筛选最优方案
- **默认模式**: Text-to-Video
- **关键护栏**: `no generic composition, no cliché visual language, no random style mixing, no emotional disconnect, no flat narrative, no derivative imagery`
- **工作流**:
  1. **Perception (感知)**: 解析用户模糊意图，提取情绪关键词和参考意象
  2. **Planning (规划)**: 并行生成 3-5 个创意方向（不同导演风格/时代/流派）
  3. **Action (执行)**: 对每个方向生成分镜草案
  4. **Feedback (反思)**: Tournament 两两比较 → 选出 Top 方案 → 迭代优化
- **质量指标**: 创意独特性、视觉一致性、情感传达力

## Mode 1: 电商产品 (Ecommerce)
- **场景**: 商品详情页视频、主图动效、PDP 循环、付费社交素材
- **核心要求**: 产品几何不变形、标签可读、镜头运动克制
- **默认模式**: Image-to-Video
- **关键护栏**: `no label blur, no packaging warp, no logo distortion, no duplicate product`
- **镜头策略**: 单动作、单机位、产品占画幅 > 40%

## Mode 2: UGC 原生广告 (UGC)
- **场景**: 信息流投放素材、创作者口播、种草测评
- **核心要求**: 面部一致、手势自然、节奏"社交感"、产品不消失
- **默认模式**: Reference-to-Video
- **关键护栏**: `no face drift, no extra fingers, no lip mismatch, no product disappearance, no shaky framing`
- **镜头策略**: 单人、单信息点、保留原生感（不要过度电影化）

## Mode 3: 电影感品牌短片 (Cinematic)
- **场景**: 品牌故事片、发布预告、创意前贴
- **核心要求**: 明确的镜头意图、精心设计的灯光逻辑、单个情绪 payoff
- **默认模式**: Text-to-Video 或 Image-to-Video
- **关键护栏**: `no shaky camera, no object melting, no random text, no flat blacks`
- **镜头策略**: 每个镜头只做一件事。多镜头通过序列编排实现复杂叙事。

## Mode 4: 多镜头叙事 (Multi-shot)
- **场景**: 完整叙事弧线、产品使用场景、品牌故事
- **核心要求**: 角色/产品跨镜头一致、过渡自然、节奏把控
- **默认模式**: Reference-to-Video + Multi-shot syntax
- **关键护栏**: 每个镜头 2-3 个分段，使用 `Cut to` / `Camera cut to` / `Shot Switch`
- **镜头策略**: 1 次生成 = 2-3 个镜头，总时长 ≤ 15s；更长叙事通过多次生成 + 后期拼接

## Mode 5: 一镜到底 (One-Shot Long Take)
- **场景**: 产品体验流程、空间巡游、品牌沉浸式展示、创意转场视频
- **核心要求**: 2-10 张图片输入 → AI 自动补足转场画面 → 连贯长镜头输出
- **输入类型**: 图片序列（2-10 张）
- **关键能力**: 空间连续性、运镜流畅性、节奏合理性
- **转场设置**:
  - 自定义转场描述（推/拉/螺旋/溶解/匹配剪辑等）
  - 仅设转场时长（AI 自动发挥）
  - 支持逐段落描述转场方式
- **关键护栏**: `no abrupt cuts, no spatial discontinuity, no object mutation between frames, no stutter in transitions`
- **质量指标**: 镜头空间连续、运镜流畅、转场自然不跳帧

## Mode 6: 爆款复刻 (Viral Replicate)
- **场景**: 灵感来源、竞品素材翻拍、爆款模板复用、经典影视猫化/狗化
- **核心要求**: 一键复制心动视频的文案结构、剧情框架、配乐画风
- **输入类型**: 参考视频（必选）+ 替换主体参考图（可选）
- **复刻策略**:
  - **创意拍摄复刻**: 复用参考视频运镜方式和创作手法，替换主体
  - **经典影视还原**: 复刻全部细节，替换人物（如换成猫/动画角色）
  - **爆款拆解再生**: 解析爆点原因 → 借鉴文案/主题/画面风格 → 重新创作
- **提示词模式**: `参考[@视频1]的运镜方式和创作手法，将主体更换为[@图片1]，创作成类似风格的[品类]视频`
- **关键护栏**: `no style drift from reference, no subject identity loss, no mismatched pacing`
- **质量指标**: 风格还原度、主体替换自然度、节奏匹配度

## Mode 7: Agent 模式 (Agent Mode — 从一句话到成片)
- **场景**: 零基础创作者、有脚本需组织、有素材需整合、跨风格创作
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

## Mode 8: 短剧创作 (Short Drama)
- **场景**: AI 短剧全自动生产、漫剧创作、小说改编短剧
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
