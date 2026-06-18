# 交付工作流

> Phase 6 审片 + Phase 7 交付的完整操作流程 + 目录结构。Phase 6-7 加载。

## Phase 6：审片

用户反馈生成结果后，精准定位问题并提供修正版提示词。

### 核心原则

- **单变量修改**：每次只改一个维度
- **加减法判断**：多了不想要的→减词；少了想要的→加词；方向错了→换词
- **位置权重**：越靠前的词权重越高，关键效果描述前移
- **避免越改越差**：超过 3 次微调无效时，退一步分析根本原因

### TVC 专属迭代重点

- **产品材质不对** → 调整材质描述词
- **产品光影太平** → 加强侧光/轮廓光描述
- **品牌世界不够极限** → 加强环境极端性描述
- **产品在场景中不够突出** → 调整产品描述的位置权重

完整的迭代策略和失败模式见 iteration-guide.md。

### 版本管理建议

1. 给每个提示词编号：v1、v2、v3...
2. 记录每次修改了什么：v2 vs v1 = 加入了体积雾描述
3. 标记满意度：★★★☆☆
4. 保留最佳版本

---

## Phase 7：交付

所有提示词输出完毕且用户满意后，主动提议整理交付物：

> "要我帮您把所有创意方案、提示词和视频脚本整理到一个项目文件夹吗？"

### 交付目录结构

```
tvc-director-output/<project-name>/
├── concept.md                      # TVC 创意方案文档
├── storyboard.md                   # 分镜脚本（如有）
│
├── assets/                         # 前期筹备：资产图提示词
│   └── prompts/
│       ├── product-multiview.md    # 产品多视图提示词
│       ├── product-detail-01.md
│       ├── env-01-<name>.md
│       └── ...
│
├── keyframes/                      # 分镜与拍摄：关键帧提示词
│   └── prompts/
│       ├── grid-01-<name>.md       # 多宫格提示词
│       ├── endframe-<name>.md      # End Frame 提示词
│       └── ...
│
└── video-scripts/                  # Seedance 视频提示词（Multi-Phase 格式）
    ├── segment-01-<name>.md
    └── ...
```

### 文件命名规则

`<task-slug>-<timestamp>.<ext>`

- `task-slug`：从任务自动提取的短名
- `timestamp`：`YYYYMMDD-HHMMSS`
