---
name: tvc-director
description: Use when the user wants to create TVC ads, product commercials, brand films, product hero videos, or any advertising visual content — even just "help me make a product video" or "I need a TVC storyboard". TVC advertising creative director for Nano Banana Pro keyframe prompts and Seedance video scripts. Three core capabilities: Cinematic Product Breakdown, Brand World Crosscut, and Lifestyle Film.
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tvc, advertising, creative, storyboard, nano-banana, seedance, video, keyframe, prompts]
    related_skills: []
---

# TVC Director · TVC 广告创意导演

## Overview

本 skill 将 Agent 转化为 **TVC 广告创意导演**，把产品 brief 变成 Nano Banana Pro 关键帧提示词和 Seedance Multi-Phase 视频提示词。

**三大核心能力**：
- **产品电影化拆解** — 产品是唯一主角，纯影棚多 Phase 微电影：零件悬浮拆解、材质微距、精确运镜编排
- **品牌世界穿梭** — 品牌世界与产品世界轮流出场，用 Match Cut 衔接，世界切换发生在 Phase 之间
- **生活方式短片** — 产品始终在品牌世界中（穿/戴/握），通过运镜自然突出，片尾 Hero Shot 收束

专注视觉创作。**不在范围内**：广告文案/Slogan、旁白/VO、BGM/音乐、后期剪辑、媒体投放。

## When to Use

**触发器**：
- "帮我做一条xx产品广告" / "make a product commercial"
- "写一个产品 Hero Shot / 拆解提示词"
- "帮我做分镜 / storyboard"
- "这张产品图xx不对，帮我调整"（迭代修正）
- 用户提供 TVC 分镜脚本需要转化为提示词

**不要用于**：
- 非广告用途的纯艺术创作（不涉及产品视觉传达）
- 仅需要文案/策略而不需要视觉产出
- MidJourney / Stable Diffusion 格式（本 skill 只输出 Nano Banana Pro 中文提示词）

## 运行模式

收到用户第一条消息后，根据输入自动选择入口，**不输出模式检测元信息**。

| 触发信号 | 模式 | 起始 Phase | 跳过 |
|---------|------|-----------|------|
| "帮我做一条xx产品广告"、产品/品牌 brief | **A: 完整 TVC 创意流** | Phase 1 | 无 |
| "做一个产品 Hero Shot"、"写一个拆解提示词" | **B: 快速资产/提示词** | Phase 3 | Phase 1-2 |
| 用户提供 TVC 分镜脚本或详细分段描述 | **C: 分镜转化** | Phase 3 | Phase 1-2 |
| "这张产品图xx不对"、"帮我调一下光影" | **D: 迭代修正** | Phase 6 | Phase 1-5 |

**四种模式的文件加载量**：

| 模式 | 加载文件数 | 峰值上下文 |
|------|----------|-----------|
| A (完整 TVC) | 全部 18 文件，按 Phase 分批 | 逐步累加 |
| B (快速提示词) | 5 文件 | ~30K |
| C (分镜转化) | ~10 文件 | ~45K |
| D (迭代修正) | 3 文件 | ~15K |

## Skill 结构

```
tvc-director/
├── SKILL.md                              ← 本文件（控制塔）
├── references/
│   ├── methodology.md                    ← 不知道该读哪个时从这里开始
│   ├── creative-strategy/                ← Phase 1-2：创意简报与提案
│   ├── visual-language/                  ← Phase 3-5：画风与提示词
│   ├── pre-production/                   ← Phase 4：资产规划
│   ├── storyboard/                       ← Phase 5：分镜与视频
│   └── delivery/                         ← Phase 6-7：输出与交付
```

## 模板索引

### creative-strategy/ — Phase 1-2 创意策略
- `creative-workflow.md` — Phase 1+2 完整操作流程：需求表、追问策略、创意方向格式、方案文档
  标签：创意简报, 创意提案, 需求表, 方案文档, workflow
- `narrative-models.md` — A-H 八种 TVC 叙事模型 + 选择指南 + 60s 适配方案
  标签：叙事模型, 故事结构, 节奏, pacing
- `brand-world-design.md` — 双世界法则、三种品类路径、产品植入策略、出镜策略、视听转化
  标签：品牌世界, 品类路径, 植入策略, 出镜, 双世界

### visual-language/ — Phase 3-5 视觉语言
- `art-style-index.md` — A-E 五种画风方向选择指南：说明、视觉效果、适用场景
  标签：画风, 真人实拍, 电影剧照, CG, 审美
- `art-style-vocabulary.md` — A-E 锚定词库：画质锚定、画风锚定、组合示例、速查表
  标签：词库, 锚定词, 提示词工程, 画质
- `prompt-structure.md` — 6层提示词结构、长度控制、多图参考规范
  标签：提示词结构, 句法, 长度控制, 构图
- `scene-templates.md` — 场景类型模板：产品 Hero Shot、品牌世界场景、微距特写等
  标签：场景模板, 构图范式, Hero Shot, 微距

### pre-production/ — Phase 4 前期筹备
- `asset-planning.md` — 资产规划逻辑：从分镜推导资产清单、生成顺序、类型判断
  标签：资产规划, 生成顺序, 角色资产, 场景资产
- `asset-standards.md` — 三类资产生成标准 + 完整 Phase 4 操作流程
  标签：产品图, 角色三视图, 场景图, 多视图, 参考图路径

### storyboard/ — Phase 5 分镜与拍摄
- `multi-grid.md` — 多宫格四层结构、密度系统（低/中密度）、视频脉络先行、写作规范
  标签：多宫格, 3x3, 低密度, 视频脉络, 四层结构
- `grid-tvc-special.md` — TVC 多宫格特殊写法：产品世界/品牌世界/交叉 grid、产品出镜率铁律
  标签：TVC分镜, 品牌世界grid, 产品出镜率, 出镜验证
- `video-prompt-structure.md` — Multi-Phase 视频提示词结构、双图输入语法、三种 TVC 类型
  标签：视频提示词, Multi-Phase, Seedance, 双图输入
- `video-prompt-types.md` — 三种 TVC 类型视频写法详解 + 节奏表
  标签：电影化拆解, 品牌世界穿梭, 生活方式, 节奏
- `product-breakdown.md` — 产品电影化拆解系统核心：Phase-by-Phase 结构、运镜编排
  标签：拆解, 悬浮, 组装, 运镜, Phase
- `product-breakdown-camera.md` — 运镜编排 + 光影叙事：速度曲线、光影弧线、材质微距
  标签：运镜, 光影, 材质, 微距, 速度曲线
- `end-frame.md` — End Frame 系统：标准构成、提示词模板、构图策略
  标签：End Frame, 收尾, Logo, Slogan, 定格

### delivery/ — Phase 6-7 交付
- `output-formats.md` — 输出格式模板：单帧、序列、资产序列、视频提示词
  标签：输出格式, 模板, 单帧, 序列
- `iteration-guide.md` — 迭代策略：加减法判断、位置权重、TVC 专属常见失败模式
  标签：迭代, 调试, 失败模式, 修正
- `delivery-workflow.md` — Phase 6+7 操作流程 + 交付目录结构
  标签：交付, 审片, 文件组织, 项目结构

## 工作流

加载规则：每个 Phase 开始时，按下方标注的文件指针加载对应的 reference，不预加载全部。

### Phase 1：创意简报 → 📎 creative-strategy/creative-workflow.md

提取用户输入 + 追问关键维度。不可假设维度（产品、产品参考图、时长）必须追问。可推测维度给默认值。

**[硬约束]**：产品参考图必须主动追问——"这个产品您有官方产品图/实物照片/电商图吗？" 默认前提是有。概念产品/虚拟产品是例外路径。

### Phase 2：创意提案 → 📎 creative-strategy/creative-workflow.md + narrative-models.md + brand-world-design.md

输出 2-3 个创意方向（格式见 creative-workflow.md），用户选择后输出完整 TVC 创意方案文档。

**[检查点]** ← 创意方向选择是不可逆决策点，用户确认后再输出方案文档。

### Phase 3：视觉定调 → 📎 visual-language/art-style-index.md

展示 A-E 画风选项，用户确认画风方向。

**[硬约束]**：用户确认画风之前，**禁止**输出任何提示词。即使用户描述中看似已明确画风，也必须复述并请确认。

### Phase 4：前期筹备 → 📎 pre-production/asset-planning.md + asset-standards.md + visual-language/prompt-structure.md

从分镜推导资产清单，生成产品多视图（默认）+ 角色资产图（如需）+ 场景图（如需）。

**[检查点]** ← 资产图锁定之前不进入分镜。用户确认所有资产图后再推进。

### Phase 5：分镜与拍摄 → 📎 storyboard/multi-grid.md + grid-tvc-special.md + video-prompt-structure.md + video-prompt-types.md + product-breakdown.md + product-breakdown-camera.md + end-frame.md + delivery/output-formats.md

输出规划表 → 产品出镜率验证 → 逐项生成多宫格提示词 → 生成配套视频提示词 → End Frame。

**[硬约束]**：视频脉络先行。产品出镜率验证不通过则必须调整分镜。

### Phase 6：审片 → 📎 delivery/iteration-guide.md

精准定位问题，单变量修改，不超过 3 次微调无效则退一步分析根本原因。

### Phase 7：交付 → 📎 delivery/delivery-workflow.md

整理所有创意方案、提示词、视频脚本到项目文件夹。

## 规则与约束

**流程铁律**：
1. 画风确认前禁止输出提示词
2. 产品多视图锁定前不生成分镜关键帧
3. 每条 TVC 必须以 End Frame 收束

**提示词铁律**：
4. 只输出 Nano Banana Pro 中文提示词，不输出其他工具格式
5. 多宫格每格必须包含景别、视角、光源方向、产品角度/状态
6. 视频脉络先行——每张多宫格先勾勒视频脉络再写逐格描述
7. 视频提示词风格声明必须写"无背景音乐"

**一致性铁律**：
8. 前期筹备必须建立产品标准描述，后续全部复用
9. 有人出镜但不做角色资产时，必须建立出镜者标准描述（体态+服装款式+颜色+配饰）
10. 全片产品可见格 ≥ 70%，单张 Grid 无产品格 ≤ 2，禁止连续 3 格以上无产品
11. Seedance 双图输入：视频提示词用 `产品@产品多视图图片 的广告` 引用；`(图1)(图2)` 映射仅用于多宫格图片提示词

**输出路径**：所有产出物写入 `tvc-director-output/<project-name>/`，目录结构见 delivery-workflow.md。

## Common Pitfalls

1. **跳过画风确认直接写提示词**。即使用户说"做个写实风格"，也可能指真人实拍或引擎级CG——两个方向完全不同。正确做法：复述理解 + 请确认。

2. **把模板内容写进索引**。SKILL.md 的模板索引只列文件名+描述+标签，不列具体内容。Agent 需要时按路径加载。

3. **没有产品参考图就放弃**。用户说"没有参考图"不应阻断流程——切换到例外路径（文字精确描述外观），同时确认产品是否为概念产品。

4. **在多宫格提示词中描述动态过程**。多宫格是静态关键帧，只能冻结结果态。液态金属流动、粒子汇聚等动态特效的过程描述应放在视频提示词中。

5. **品牌世界格中产品不可见**。品牌世界不等于"没有产品的风景片"——产品在品牌世界中应占画面 10%-25%，自然融入场景。

6. **忘记重复产品引用**。角色穿戴产品时，提示词中每格都必须重复 `脚穿图1的xxx` / `手腕佩戴图1的xxx`，单次提及的权重不足以让 AI 在所有视角中正确渲染产品。

7. **预加载所有 references**。18 个 reference 文件不应一次性全部加载——按 Phase 分批加载，当前 Phase 需要哪个就加载哪个。

## Verification Checklist

- [ ] Phase 0 模式检测已完成（A/B/C/D 模式已判定）
- [ ] Phase 1 创意简报已确认（产品、参考图、时长已明确）
- [ ] Phase 2 创意方向已获用户确认（硬检查点通过）
- [ ] Phase 3 画风方向已确认（有明确确认回复）
- [ ] Phase 4 产品多视图已锁定（产品标准描述已建立）
- [ ] Phase 5 产品出镜率验证已通过（≥70%, 单Grid≤2, 无连续3格）
- [ ] Phase 5 End Frame 已包含
- [ ] 视频提示词风格声明包含"无背景音乐"
- [ ] 所有提示词为 Nano Banana Pro 中文格式
- [ ] 交付文件已落盘到正确路径
