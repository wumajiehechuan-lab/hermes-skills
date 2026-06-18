# tvc-director v3.0 — 导航索引

> **给 Agent 的导航手册。** 不知道该加载哪个 reference 时，先读本文件。
> 本文件约 3,000 chars，加载成本极低。

---

## 一、完整目录地图（13 个 references）

```
references/
├── methodology.md                    ← 本文件（导航索引）
│
├── creative-strategy/
│   └── brand-world-design.md         （4,183 chars）品牌世界思维 + 创意方向 + 分镜脚本格式
│
├── visual-language/
│   ├── prompt-structure.md           （2,640 chars）提示词 6 层结构 + 长度控制
│   ├── art-style-vocabulary.md       （1,809 chars）画风 A-E 锚定词库
│   └── scene-templates.md            （6,957 chars）TVC 场景类型 + 构图范式 + 视觉设计清单
│
├── pre-production/
│   └── asset-standards.md            （6,263 chars）资产规划 + 三种资产定义 + 一致性维护
│
├── storyboard/
│   ├── multi-grid.md                 （5,974 chars）通用多宫格 8 节写法
│   ├── grid-tvc-special.md           （5,854 chars）TVC 多宫格专用写法
│   ├── video-prompt-structure.md     （3,682 chars）视频提示词语法 + 自检清单
│   ├── product-breakdown.md          （5,975 chars）产品电影化拆解（机制 + 3 示例）
│   ├── transition-design.md          （1,410 chars）品牌世界穿梭切换技法
│   └── video-prompt-types.md         （2,845 chars）TVC 时长模板（15s/30s/60s）
│
└── delivery/
    ├── output-formats.md             （4,030 chars）输出格式模板
    └── iteration-guide.md            （5,933 chars）11 种失败模式 + 调试策略
```

> **合并说明**：`creative-strategy/creative-workflow.md`（853 chars）已合并入 `creative-strategy/brand-world-design.md`；`pre-production/asset-planning.md`（743 chars）已合并入 `pre-production/asset-standards.md`。合并源文件保留在仓库中但不再被 SKILL.md 引用，v3.0 部署时一并清理。

---

## 二、Phase → Reference 加载映射

| Phase | 任务 | 应加载的 references | 数量 |
|-------|------|-------------------|------|
| **Phase 0** | 启动检测（Mode A/B/C/D） | 无 | 0 |
| **Phase 1** | 创意简报 | 无 | 0 |
| **Phase 2** | 创意提案 | `creative-strategy/brand-world-design.md` | 1 |
| **Phase 3** | 视觉定调 | `visual-language/art-style-vocabulary.md` | 1 |
| **Phase 4** | 前期筹备 | `pre-production/asset-standards.md` + `visual-language/prompt-structure.md` + `visual-language/scene-templates.md` | 3 |
| **Phase 5** | 分镜与拍摄 | `storyboard/multi-grid.md` + `storyboard/grid-tvc-special.md` + `storyboard/video-prompt-structure.md` + `storyboard/product-breakdown.md` + `storyboard/transition-design.md` + `storyboard/video-prompt-types.md` + `delivery/output-formats.md` | 7 |
| **Phase 6** | 审片 | `delivery/iteration-guide.md` | 1 |
| **Phase 7** | 交付 | 无 | 0 |

> **加载原则**：按需加载，不预加载。每 Phase 只加载自己需要的文件。Phase 5 是核心产出阶段，7 个文件逐个按需加载——不要一次性全部加载。

---

## 三、模式加载量表（Mode 加载预算）

| Mode | 触发信号 | 涉及 Phase | 需加载 references 数 | 总 chars 预算 |
|------|---------|-----------|-------------------|-------------|
| **A：完整 TVC 创意流** | 产品 brief、品牌需求 | Phase 0→1→2→3→4→5→6→7 | 0+0+1+1+3+7+1+0 = 13 | ~57,000 |
| **B：快速资产/提示词** | 单帧/单图需求 | Phase 0→3→4 | 0+1+3 = 4 | ~18,000 |
| **C：分镜转化** | 已有分镜脚本 | Phase 0→3→4→5 | 0+1+3+7 = 11 | ~50,000 |
| **D：迭代修正** | 修改已有产出 | Phase 0→6 | 0+1 = 1 | ~6,000 |

---

## 四、文件加载顺序建议

### Phase 5 内部加载顺序（7 个文件，按需分步）

```
1. multi-grid.md             → 先学通用多宫格写法
2. grid-tvc-special.md       → 再学 TVC 专用差异
3. product-breakdown.md      → 产品电影化拆解系统
4. transition-design.md      → 品牌世界切换技法
5. video-prompt-structure.md → 视频提示词语法结构
6. video-prompt-types.md     → 时长模板适配
7. output-formats.md         → 输出格式（最后看）
```

> **不要同时加载 7 个文件。** 按上述顺序，当前任务需要哪个就加载哪个。大多数 TVC 只需要前 3-4 个。

### Phase 4 内部加载顺序（3 个文件）

```
1. asset-standards.md        → 资产规划 + 定义 + 一致性
2. prompt-structure.md       → 提示词 6 层结构
3. scene-templates.md        → 场景模板（按需，不是每次都需要）
```
