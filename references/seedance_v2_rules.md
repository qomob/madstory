# 即梦 Seedance 2.0 广告场景提示词工程规范

## 1. 提示词 5 层结构 (Prompt Hierarchy)

广告场景下，提示词必须按以下优先级排列:

```
[Subject] → [Single Action] → [Camera Move] → [Style & Lighting] → [Constraints]
```

| 层级 | 回答的问题 | 电商示例 | UGC 示例 | 电影感示例 |
|------|-----------|---------|---------|-----------|
| Subject | 什么必须保持可识别？ | @Image1 护肤品瓶身 | @Image1 创作者面部 | 红色跑车在午夜 |
| Action | 正在发生什么？ | 缓慢旋转 | 手持产品面对镜头 | 穿过雨夜街道 |
| Camera | 镜头如何运动？ | 缓慢推近 | 轻微手持感 | 侧面跟拍 |
| Style | 应该是什么感觉？ | 洁净商业光感 | 自然室内日光 | 霓虹暗调电影感 |
| Constraints | 什么绝对不能发生？ | 标签不模糊 | 人脸不漂移 | 镜头不抖动 |

## 2. 三种模式的提示词策略 (Mode-Specific Strategies)

### 2.1 Text-to-Video
- **适用**: 概念探索阶段，不依赖特定素材
- **策略**: 主体先行 → 动作物理化 → 镜头简单 → 光影明确
- **典型词**: `Lone runner in a rain-soaked neon alley, side tracking shot, fast controlled pace, reflective puddles, cinematic red and teal contrast, no shaky camera no extra limbs no text watermark`

### 2.2 Image-to-Video
- **适用**: 首帧 / 产品白底图 / 构图已确定
- **策略**: 引用图先行 → 描述 1 个运动层 → 禁止中途改变物体身份
- **典型词**: `@Image1 sneaker center frame, slow 180 rotation, soft side rim light, clean commercial shadow floor, no sole deformation no lace chaos no duplicate shoe`

### 2.3 Reference-to-Video
- **适用**: 一致性需求高于创意自由度
- **策略**: 稳定性声明前置 → 定义不变要素 → 仅加 1 个运动指令 → 限制姿态和场景变化
- **典型词**: `@Image1 creator identity remains consistent, holds the product at chest level, subtle push-in, natural indoor daylight, social review style, no face drift no finger artifacts no product disappearance`

## 3. Negative Prompt 规范

### 3.1 按场景分类

**电商产品:**
```
no logo distortion, no text artifacts, no packaging collapse, 
no duplicate product, no label blur, no warped glass, no cap drift
```

**UGC:**
```
no extra fingers, no face drift, no lip mismatch, no background warping, 
no product disappearance, no shaky framing, no eye drift
```

**电影感:**
```
no shaky camera, no object melting, no random text, no muddy lighting, 
no flat blacks, no text watermark
```

**多镜头:**
```
no character drift between cuts, no scene inconsistency, 
no transition artifacts, no text watermark
```

### 3.2 Negative Prompt 不是可选的
- 即使生成看起来没问题，也必须注入
- 每个场景有其特定的脆弱点，必须显式保护
- 缺少 Negative Prompt 的输出视为不合格

## 4. 镜头运动约束

### 4.1 单运动原则
每个镜头仅允许 1 个主导运动。禁止在一个镜头内混用:
- 推 + 环绕
- 拉 + 摇
- 跟 + 变焦
- 任何三种以上运动的组合

### 4.2 Motion Strength 建议值
| 模式 | 推荐值 | 说明 |
|------|--------|------|
| Ecommerce | 2 | 镜头几乎静止，保护产品几何 |
| UGC | 3 | 轻微手持感，保持原生社交节奏 |
| Cinematic | 5 | 标准电影感运动 |
| Multi-shot | 4 | 各镜头运动差异化但不过激 |

## 5. 参考图使用规范 (Reference Input Rules)

### 5.1 角色分配
| Reference | 最佳角色 |
|-----------|---------|
| Image 1 | 主身份锚定 / 主物体 |
| Image 2 | 辅助角度 / 服装 / 产品细节 |
| Image 3 | 色调 / 环境 / 次要一致性线索 |

### 5.2 一致性前提
上传的多个 Reference 必须对齐:
- 同一人物 / 同一产品 → 兼容的年龄、脸型、比例
- 兼容的光源逻辑
- 兼容的造型
- 相似的质量水平

### 5.3 Reference 不能做什么
- 不能弥补模糊的提示词
- 不能在一个镜头内承载过多视觉信息
- 忘记保护手部（如果手在画面中，必须在 Negative Prompt 中声明）

## 6. 多镜头叙事规范 (Multi-shot Syntax)

### 6.1 过渡关键词
| 关键词 | 行为 | 最佳场景 |
|--------|------|---------|
| `Cut to` | 硬切 | 快节奏动作、戏剧性揭示 |
| `Camera cut to` | 明确机位切换 | 采访风格、纪录片 |
| `Shot Switch` | 场景转换 + 视觉桥接 | 叙事、商业广告 |

### 6.2 格式
```
[Shot 1: Subject + Action + Camera Direction]
Cut to
[Shot 2: Subject + Action + Camera Direction + New Scene Details]
Cut to
[Shot 3: Subject + Action + Camera Direction]
```

### 6.3 限制
- 单次生成 ≤ 3 个镜头
- 总时长 ≤ 15 秒
- 每个镜头后必须描述新场景

## 7. 一致性管控规范 (Consistency Protocol)

### 7.1 不变性清单 (Invariants)
在分镜推导前锁定:
- 人脸身份
- 产品 / 瓶身 / 包装形状
- 服装
- 背景布局
- 色彩调性
- 手与物体的关系

### 7.2 调试优先级
当输出漂移时:
1. 是否定义了不变要素？
2. 当前模式是否过于开放？
3. 镜头运动是否过于激进？
4. 主体在画面中是否过小？
5. 多个 prompt / reference 是否互相冲突？

### 7.3 跨镜头一致性
构建多镜头序列时，锁死以下变量:
- 画幅比例
- 主光源方向
- 镜头感觉
- 主体造型
- Negative Prompt 护栏

## 8. 迭代调试规则

### 8.1 每次改 1 个变量
- Prompt 措辞
- Reference 选择
- 镜头指令
- 时长
- 画幅比例

不要同时改多个。

### 8.2 从简化开始
如果镜头不稳定:
- 减少动作数
- 减少道具数
- 简化运动
- 收紧取景

短 prompt 不一定更好，但窄镜头几乎总是更稳定。

## 9. 电商场景专项规范

### 9.1 核心三要素
- 产品几何不变形
- 标签可读
- 镜头运动克制

### 9.2 标准工作流
1. 确认产品白底图 → Image-to-Video
2. 单镜头 + 单动作
3. 产品占画面 ≥ 40%
4. 光源不遮挡标签

## 10. UGC 场景专项规范

### 10.1 可信度因素
UGC 广告的难点在于「看起来自然」。必须保持:
- 一个创作者身份
- 一个信息点
- 一个简单手势或动作
- 产品始终可见

### 10.2 手势安全范围
优先选择:
- 产品持握在胸前
- 产品面对镜头展示 1 次
- 轻微指向某个特征
- 手中轻转

避免:
- 快速手势
- 复杂拆箱编排
- 多次换手
- 夸张面部表情

## 11. 最终输出自检清单

每个分镜方案输出前必须确认:
- [ ] STANDARD_PROMPT 符合 5 层结构
- [ ] NEGATIVE_PROMPT 已按模式注入
- [ ] 镜头运动 ≤ 1 个主导方式
- [ ] Motion Strength 在合理范围
- [ ] 多镜头场景 ≤ 3 个镜头/次
- [ ] 产品标签/人脸/手部已在护栏中声明
- [ ] Reference 建议已按模式给出

## 12. 一镜到底专项规范 (One-Shot Specification)

### 12.1 输入约束
- **图片数量**: 2 ≤ N ≤ 10
- **图片顺序**: 按时间轴排列，第 1 张 = 起始帧，最后 1 张 = 结束帧
- **构图连续性**: 相邻图片之间应有明确的空间关系或视觉连接点
- **图片质量**: 建议分辨率一致，光位兼容

### 12.2 转场类型与适用场景
| 转场类型 | Seedance 提示词 | 最佳场景 | 建议时长 |
|---------|----------------|---------|---------|
| 推 (Push) | `camera pushes forward through` | 全景→特写，深入场景 | 2-4s |
| 拉 (Pull) | `camera pulls back revealing` | 特写→全景，展示环境 | 2-4s |
| 螺旋 (Spiral) | `spiral rotation centered on` | 魔幻/科幻风格转场 | 2.5-3.5s |
| 溶解 (Dissolve) | `cross-dissolve to` | 时间流逝、回忆切换 | 1.5-3s |
| 匹配剪辑 (Match Cut) | `match cut via` | 利用相似形状/颜色衔接 | 1-2s |
| 甩 (Whip Pan) | `whip pan transition to` | 快速场景切换、动感 | 0.5-1.5s |
| 遮挡 (Wipe) | `wipe transition through` | 物体遮挡自然转场 | 1-2s |
| AI 自动 (Auto) | `smooth auto transition to` | 不指定，AI 自由发挥 | 2-3s |

### 12.3 提示词格式
```
One-shot long take sequence:
[Frame 1: 起始帧描述]
  → [Xs transition: 转场描述] →
[Frame 2: 第二帧描述]
  → [Xs transition: 转场描述] →
[Frame 3: 结束帧描述]
Total duration: ~Xs. Continuous spatial flow, no cuts, smooth camera, Seedance 2.0 style.
```

### 12.4 关键约束
- 全程无硬切 (no abrupt cuts)
- 空间不跳跃 (no spatial discontinuity)
- 物体不突变 (no object mutation between frames)
- 转场不卡顿 (no stutter in transitions)
- 画面不撕裂 (no frame-tearing)

## 13. 爆款复刻专项规范 (Viral Replicate Specification)

### 13.1 三种复刻策略
| 策略 | 核心操作 | 输入要求 | 提示词模式 |
|------|---------|---------|-----------|
| creative_shoot | 复用运镜+创作手法，替换主体 | 参考视频 + 替换主体图 | `参考[@视频]运镜方式，主体更换为[@图片]` |
| classic_remake | 复刻全部细节，仅替换人物 | 参考视频 + 替换角色描述 | `复刻[@视频]内容，人物替换成[角色]` |
| viral_deconstruct | 解析爆点→借鉴风格→重新创作 | 参考视频 + 差异化要求 | `解析[@视频]爆点原因，借鉴风格重新创作` |

### 13.2 关键护栏
- 风格不偏离参考 (no style drift from reference)
- 主体身份不丢失 (no subject identity loss)
- 节奏不失调 (no mismatched pacing)
- 替换主体不变形 (no warped replacement subject)
- 原主体不残留 (no original ghosting)

## 14. Agent 模式专项规范 (Agent Mode Specification)

### 14.1 意图解析分层
输入 → 解析主体/风格/时长/情绪 → 判断是否有脚本 → 判断是否有素材 → 选择最优子模式

### 14.2 风格自动检测
| 检测关键词 | 映射风格 | 默认子模式 |
|-----------|---------|-----------|
| 电影感/大片/film/cinematic | cinematic | Text-to-Video |
| 二次元/动漫/anime/漫画 | anime | Text-to-Video |
| 3D/三维/CG | 3d | Text-to-Video |
| 国风/水墨/古风 | guofeng | Text-to-Video |
| 写实/真实/照片级 | realistic | Text-to-Video |
| 种草/测评/开箱/口播 | ugc | Reference-to-Video |

### 14.3 路由决策
```
有脚本标记(集/场景:/人物:/△) → short_drama
有素材标记(上传/@图片/@视频/参考图) → viral_replicate  
风格为 ugc → UGC
其他 → agent_mode (通用创作)
```

## 15. 短剧专项规范 (Short Drama Specification)

### 15.1 标准剧本格式
```
第X集
场景: [地点描述] [时间]
人物: [角色A], [角色B]

△ [环境/动作描述]
[角色A] (OS): [内心独白]
[角色A]: [对白内容]
[角色B]: [对白内容]
```

### 15.2 角色一致性机制
- 全局角色库: 所有角色在剧本解析时注册
- @角色引用: 分镜中通过 @角色名 锁定形象
- 跨集一致性: 服装、发型、面部特征在各集中保持

### 15.3 关键护栏
- 角色跨集不漂移 (no character face drift across episodes)
- 服装不混乱 (no costume inconsistency)
- 场景不跳跃 (no scene discontinuity)
- 配音不匹配 (no voice mismatch)
- 字幕不同步 (no subtitle desync)
