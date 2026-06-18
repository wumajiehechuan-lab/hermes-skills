# TVC 导演方法论入口

> 18 个 reference 文件的导航页。不知道该读哪个时从这里开始。

## 按 Phase 导航

| Phase | 需要加载的文件 | 数量 |
|-------|-------------|------|
| **Phase 1** (创意简报) | creative-strategy/creative-workflow.md | 1 |
| **Phase 2** (创意提案) | creative-strategy/creative-workflow.md + narrative-models.md + brand-world-design.md | 3 |
| **Phase 3** (视觉定调) | visual-language/art-style-index.md | 1 |
| **Phase 4** (前期筹备) | pre-production/asset-planning.md + asset-standards.md + visual-language/prompt-structure.md | 3 |
| **Phase 5** (分镜与拍摄) | storyboard/multi-grid.md + grid-tvc-special.md + video-prompt-structure.md + video-prompt-types.md + product-breakdown.md + product-breakdown-camera.md + end-frame.md + delivery/output-formats.md | 8 |
| **Phase 6** (审片) | delivery/iteration-guide.md | 1 |
| **Phase 7** (交付) | delivery/delivery-workflow.md | 1 |

## 按模式加载量

| 模式 | 场景 | 加载文件数 | 峰值上下文 |
|------|------|----------|-----------|
| A (完整 TVC) | "帮我做一条广告" | 全部 18 文件，按 Phase 分批 | 逐步累加 |
| B (快速提示词) | "写一个产品 Hero Shot" | SKILL.md + art-style-index + vocabulary + prompt-structure + output-formats = 5 文件 | ~30K |
| C (分镜转化) | 用户提供现成分镜 | SKILL.md + art-style-index + vocabulary + pre-production/ + storyboard/ + output-formats | ~45K |
| D (迭代修正) | "光影不对" | SKILL.md + iteration-guide + product-breakdown-camera = 3 文件 | ~15K |

## 目录地图

```
references/
├── methodology.md                    ← 本文件
├── creative-strategy/                ← 创意策略
│   ├── creative-workflow.md          ← Phase 1+2 操作流程
│   ├── narrative-models.md           ← A-H 叙事模型
│   └── brand-world-design.md         ← 品牌世界设计
├── visual-language/                  ← 视觉语言
│   ├── art-style-index.md            ← A-E 画风选择
│   ├── art-style-vocabulary.md       ← 锚定词库
│   ├── prompt-structure.md           ← 6层提示词结构
│   └── scene-templates.md            ← 12种场景模板
├── pre-production/                   ← 前期筹备
│   ├── asset-planning.md             ← 资产规划逻辑
│   └── asset-standards.md            ← 资产生成标准
├── storyboard/                       ← 分镜与视频
│   ├── multi-grid.md                 ← 多宫格系统
│   ├── grid-tvc-special.md           ← TVC特殊写法
│   ├── video-prompt-structure.md     ← 视频提示词结构
│   ├── video-prompt-types.md         ← 三种TVC类型
│   ├── product-breakdown.md          ← 产品拆解系统
│   ├── product-breakdown-camera.md   ← 运镜与光影
│   └── end-frame.md                  ← End Frame系统
└── delivery/                         ← 交付
    ├── output-formats.md             ← 输出格式模板
    ├── iteration-guide.md            ← 迭代指南
    └── delivery-workflow.md          ← 交付流程
```
