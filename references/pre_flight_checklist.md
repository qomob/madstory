# MadStory 导演级预检清单 (Director Pre-Flight Checklist)

启用 MadStory 技能前，使用以下清单进行创作准备度验证。

## 1. 技术规格 (Technical Specifications)

- [ ] **Mode 已确认** — 9 个模式中选定 1 个 (creative_film / ecommerce / ugc / cinematic / multi_shot / one_shot / viral_replicate / agent_mode / short_drama)
- [ ] **Seedance 输入模式已推荐** — Text-to-Video / Image-to-Video / Reference-to-Video 已提示用户
- [ ] **时长已设定** — 默认 15s，多镜头序列总长 ≤ 15s，长视频可设 60s
- [ ] **画幅比例已确定** — 16:9 / 9:16 / 1:1 / 2.35:1
- [ ] **Motion Strength 已建议** — 按模式: Ecommerce=2 / UGC=3 / Cinematic=5 / Multi-shot=4 / One-shot=4 / Viral=5 / Drama=4

## 2. 主体与构图 (Subject & Composition)

- [ ] **主体已明确** — 产品 / 人物 / 场景，不可含歧义
- [ ] **单镜头信息点检查** — 每个镜头只承载 1 个动作或 1 个信息点
- [ ] **构图方式已确定** — 三分法 / 中心 / 对称 / 对角线 / 框架式
- [ ] **产品占比检查 (Ecommerce)** — 产品占画幅 ≥ 40%，不在边角
- [ ] **取景范围检查 (UGC)** — 半身/特写已确定，自然取景非影楼感
- [ ] **多镜头场景检查 (Multi-shot/One-shot)** — 每段含: 主体 + 动作 + 机位

## 3. 镜头运动 (Camera Movement)

- [ ] **单运动原则检查** — 每个镜头 ≤ 1 个主导运动
- [ ] **运动类型已选择** — orbit / dolly / push-in / pull-out / crane / handheld / whip / follow / static
- [ ] **运动动机已明确** — 每次运动服务于叙事/产品目的，非炫技
- [ ] **时间轴运动标注** — 在 Timeline 上标注运动变化节点
- [ ] **运动强度在合理范围** — Ecommerce ≤ 3 / UGC = 3 / 其他 4-5

## 4. 光影与色彩 (Lighting & Color)

- [ ] **光源方向已确定** — key light 方向、fill ratio
- [ ] **色温已指定** — 暖色 (3200K) / 中性 (4500K) / 冷色 (5600K+)
- [ ] **灯光类型已选择** — 三点布光 / 蝴蝶光 / 伦勃朗 / 侧光 / 逆光 / 霓虹 / 金色时刻
- [ ] **环境细节已描述** — 烟雾/颗粒/反射/材质
- [ ] **电商光位检查** — 光源不遮挡或反射产品标签
- [ ] **UGC 光感检查** — 自然光/环形灯，不过度打光
- [ ] **色彩调性一致** — 跨镜头保持一致的色彩氛围

## 5. 声音设计 (Sound Design)

- [ ] **BGM 情绪已确定** — 激昂/舒缓/悬疑/科技感/自然/电子
- [ ] **音效同步点已标注** — 与 Timeline 关键帧对齐
- [ ] **环境音已规划** — 雨声/风声/人群/房间音
- [ ] **电商/多镜头模式** — BGM 不打断产品信息传达

## 6. 模式专项检查 (Mode-Specific)

### Ecommerce (电商)
- [ ] 产品标签可读性已声明 (Negative Prompt)
- [ ] 产品几何保护已声明 (no warped, no distortion)
- [ ] Image-to-Video 模式已推荐
- [ ] 白底/纯色背景已指定

### UGC (原生广告)
- [ ] 人脸一致性已声明 (no face drift)
- [ ] 手指保护已声明 (no extra fingers)
- [ ] Reference-to-Video 模式已推荐
- [ ] 社交节奏感已描述

### Cinematic (电影感)
- [ ] 镜头抖动保护已声明
- [ ] 灯光逻辑有明确动机
- [ ] 单一情绪 payoff 已识别
- [ ] 物体变形保护已声明

### Multi-shot (多镜头)
- [ ] 镜头数 ≤ 3
- [ ] 过渡关键词已使用 (Cut to / Camera cut to / Shot Switch)
- [ ] 跨镜头一致性约束已声明
- [ ] 时间分配合理 (各镜头时长和 = 总时长)

### One-Shot (一镜到底)
- [ ] 图片数 2 ≤ N ≤ 10
- [ ] 转场类型已逐段指定或设为 Auto
- [ ] 空间连续性已声明 (no spatial discontinuity)
- [ ] 跳帧保护已声明 (no stutter)

### Viral Replicate (爆款复刻)
- [ ] 参考视频已指定
- [ ] 复刻策略已选定 (creative/classic/deconstruct)
- [ ] 替换主体已指定 (如适用)
- [ ] 风格偏离保护已声明 (no style drift)

### Agent Mode (Agent)
- [ ] 用户意图已解析 (风格/时长/情绪)
- [ ] 路由决策已执行
- [ ] 子模式的 Negative Prompt 已注入
- [ ] 输出模式标签包含子模式信息

### Short Drama (短剧)
- [ ] 角色注册表已建立
- [ ] @角色引用机制已启用
- [ ] 跨集一致性约束已声明
- [ ] 剧本格式已验证 (场景/人物/△/OS)
- [ ] 一致性管控台账已建立 (Characters / Scenes / Timeline)
- [ ] 长戏份 (>15s) 已拆分标记校验节点
- [ ] 人物档案六项不可变字段已填写 (视觉标记/发型发色/妆容/服饰/配饰/穿着状态)
- [ ] 场景清单四项环境参数已记录 (光线方向/色温/天气/背景杂音)
- [ ] 后期跨片段一致性校验已规划 (C1/C2/C3)

## 7. 多模态输入检查 (Multi-Modal Input)

- [ ] Reference 图已分配角色 — Image1(主身份), Image2(辅助), Image3(色调)
- [ ] 多个 Reference 之间光位/造型/质量对齐
- [ ] Reference 不与模糊 prompt 搭配使用
- [ ] 手部在画面中时已在 Negative Prompt 中保护

## 8. 输出完整性检查 (Output Integrity)

- [ ] STANDARD_PROMPT 包含 5 层结构 (Subject → Action → Camera → Style → Constraints)
- [ ] NEGATIVE_PROMPT 按模式自动注入完整
- [ ] TIMELINE 含关键帧描述
- [ ] CAMERA 逐秒/逐镜头描述
- [ ] MOTION_STRENGTH 在 1-10 范围
- [ ] DURATION 含时间单位
- [ ] MODE 标签正确
- [ ] MULTI_MODAL_ADVICE 具体可用
- [ ] SHOT_LIST 完整 (多镜头模式)

## 9. 质量护栏检查 (Quality Gates)

- [ ] Negative Prompt 非空
- [ ] 每个 Mode 的专项护栏已触发检查
- [ ] 无任何 FAIL 级别的质量问题
- [ ] 如有 WARNING，已确认可接受

## 10. 最终签署 (Final Sign-off)

- [ ] 导演视角确认: 这个分镜方案能否指导一次实际拍摄？
- [ ] 广告视角确认 (如适用): 这个素材适合直接投放吗？
- [ ] 即梦视角确认: 这个提示词在 Seedance 2.0 中能直接使用吗？
- [ ] 一致性确认: 多镜头/多素材间风格统一吗？
- [ ] (可选) 使用独立校验工具验证: `tools/mad-story-scripts/`

## 11. Seedream 4.x/5.x 图片模式预检

> 当检测到用户使用 Seedream 平台或需要图片生成时，执行以下检查项。
> 完整规则见 `references/seedream_4x_rules.md`

- [ ] **平台已确认** — Seedream 4.x/5.x 图片生成模式
- [ ] **提示词结构** — 3层结构（主体+行为+环境，风格/色彩/光影/构图补充），非视频5层
- [ ] **文字渲染** — 需生成的文字已用双引号包裹
- [ ] **图像编辑指令** — 指代明确（无模糊代词），保持不变的部分已强调
- [ ] **视觉信号** — 涂鸦/线框/箭头已标注颜色对应关系（如适用）
- [ ] **参考图类型** — 已指明（人物形象/风格/虚拟实体/款式/无）
- [ ] **参考图双要素** — 已指明参考对象 + 生成画面描述
- [ ] **多图输入** — 图一/图二角色分配已明确（如适用）
- [ ] **多图输出** — 数量和触发词已指定（如适用）
- [ ] **Negative Prompt** — 不注入（图片模式不需要）
- [ ] **Camera/Motion 参数** — 已移除（图片模式不适用）
