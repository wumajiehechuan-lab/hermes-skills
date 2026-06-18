# Hermes Agent Skills 合集

> 一套面向独立开发者的 AI Agent 商业工具链 — 从概念打磨、竞品拆解到市场侦察，覆盖一个人创业的完整决策闭环。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-ready-blue)

---

## 概览

本项目是 [Hermes Agent](https://hermes-agent.nousresearch.com/docs) 的 Skills 合集，包含五个递进式的商业分析 + 创意 + 开发工具：

||| Skill | 功能 | 适用阶段 |
|||-------|------|---------|
||| **[concept-to-canvas](#-concept-to-canvas)** | 从模糊概念到 Lean Canvas + VPC 商业方案骨架 | 想法萌芽期 → 方案设计 |
||| **[biz-canvas](#-biz-canvas)** | 五维分析法拆解已有项目，评估可复制性与天花板 | 竞品分析期 → 可行性判断 |
||| **[ai-project-scout](#-ai-project-scout)** | 自动抓取 Product Hunt / Indie Hackers AI 项目，生成中文日报 | 市场侦察期 → 灵感获取 |
||| **[tvc-director](#-tvc-director)** | TVC 广告创意导演 — 产品 Brief → Nano Banana Pro 关键帧 + Seedance 视频脚本 | 创意产出期 → 广告物料 |
||| **[complex-skill-builder](#-complex-skill-builder)** | 控制塔+仓库架构，系统化构建复杂 Skill（模板/多环境/长流程） | Skill 开发期 → 架构设计 |

**使用路径：** 有了点子 → `concept-to-canvas` 打磨方案 → 找到竞品 → `biz-canvas` 拆解验证 → 日常喂信息 → `ai-project-scout` 持续侦察 → 做广告 → `tvc-director` 生成物料。

---

## 🧠 concept-to-canvas

**从模糊概念到结构化商业方案的「乐高说明书」。**

当脑子里只有一个粗略的想法（一段话、一句话、几个关键词），用精益画布（Lean Canvas）+ 价值主张画布（Value Proposition Canvas）两步法，1 小时内从 0 到 1 生成可验证的商业方案骨架。

### 工作流程

```
用户输入概念（一句话 / 几个关键词）
       │
       ▼
Step 1：精益画布（Lean Canvas）— 按商业逻辑填充 9 格
       │  ← 用户修改确认
       ▼
Step 2：价值主张画布（VPC）— 客户画像 ↔ 价值地图齿轮咬合
       │  ← 用户优化确认
       ▼
Step 3：输出 MD + PDF 方案文档
```

### 核心文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | Hermes Agent Skill 指令 — 完整的交互流程、填充规则、输出模板 |
| `scripts/md_to_pdf.py` | Markdown → PDF 转换脚本（自动检测 WeasyPrint / Chrome headless） |

### 触发词

「我有一个想法…」「帮我用精益画布…」「我想做个…产品」「帮我理一下这个商业想法」

---

## 🔍 biz-canvas

**商业模式五维分析法 — 快速拆解一个商业项目的本质。**

核心理念：**九分靠营销，一分靠技术。** 看一个项目时，多看它的流量来源，少看它的界面功能。

### 五维框架

| 维度 | 核心提问 |
|------|---------|
| 🎯 需求与痛点 | 谁在用？为什么不用免费替代品？止痛药还是维他命？ |
| 💰 商业变现与成本 | 怎么收钱？毛利率多少？API 算力成本 > 月费？ |
| 🚀 流量与增长 | 第一批用户怎么来的？获客渠道可持续吗？SEO 潜力？ |
| 🛡️ 技术壁垒与护城河 | 三天能抄一个一样的吗？真正的壁垒在哪？ |
| 📈 天花板与生命周期 | 长期需求还是一阵风？大厂下场会死吗？ |

### 核心文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 完整的五维分析框架、子 Agent 分工策略、输出模板 |
| `scripts/md_to_pdf.py` | Markdown → PDF 转换脚本（含 CSS 排版 + Chrome headless 打印） |
| `business-concept-workout/SKILL.md` | **子 Skill：** 多轮交互式概念打磨 — 精益画布 → VPC → 精益创业验证三部曲 |

### 触发词

「这个项目怎么赚钱」「帮我拆解一下这个生意」「这个能抄吗」「值不值得做」「可行性评估」

---

## 🤖 ai-project-scout

**AI 创业项目侦察员 — 从 Product Hunt + Indie Hackers 自动抓取 AI 项目，翻译为中文日报。**

### 功能

- 🕸️ 自动抓取 **Product Hunt** 当日 AI 新产品
- 📊 自动抓取 **Indie Hackers** 有收入的 AI 项目（含关注者、收入数据）
- 🌐 智能翻译为流畅中文（保留原意、标签中文化）
- 🔄 去重追踪 — 已见过的项目不重复收录
- 📅 每日产出格式化中文日报（Markdown 格式）

### 核心文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | Hermes Agent Skill 指令 — 工作流、参数映射、翻译要求、日报模板 |
| `scripts/scout.py` | Python 数据抓取脚本 — Product Hunt RSS + Indie Hackers API |
| `references/openai-agent.yaml` | OpenAI Agent SDK 兼容接口声明 |

### 触发词

「AI 日报」「今天有什么新项目」「抓取 AI 产品」「AI 工具推荐」

---

## 🎬 tvc-director

**TVC 广告创意导演 — 把产品 Brief 变成 Nano Banana Pro 关键帧提示词和 Seedance Multi-Phase 视频提示词。**

> 原作者：[Ethanxwang/tvc-director](https://github.com/Ethanxwang/tvc-director) — 本版本基于 `complex-skill-builder` 进行控制塔+仓库架构重构（v2.0），19 个 reference 文件按需加载，最简模式仅 15K 上下文。

### 三大核心能力

| 能力 | 说明 | 适用产品 |
|------|------|---------|
| **产品电影化拆解** | 产品是唯一主角，纯影棚多 Phase 微电影：零件悬浮拆解、材质微距 | 耳机/相机/手机/机械表芯 |
| **品牌世界穿梭** | 品牌世界与产品世界轮流出场，Match Cut 衔接 | 运动相机/越野车/潜水表 |
| **生活方式短片** | 产品始终在品牌世界中，通过运镜自然突出 | 跑鞋/手表/眼镜/手袋 |

### 七阶段工作流

```
Phase 1：创意简报 → Phase 2：创意提案 [检查点]
    → Phase 3：视觉定调（A-E 画风）→ Phase 4：前期筹备 [检查点]
    → Phase 5：分镜与拍摄（多宫格 + 视频提示词 + End Frame）
    → Phase 6：审片 → Phase 7：交付
```

### 核心文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 控制塔 — 4 种运行模式、7 Phase 工作流、19 个模板索引 |
| `references/methodology.md` | 导航入口 — 按 Phase/模式的文件加载指南 |
| `references/creative-strategy/` | Phase 1-2：创意简报、叙事模型、品牌世界设计 |
| `references/visual-language/` | Phase 3-5：A-E 画风锚定词库、6层提示词结构、场景模板 |
| `references/pre-production/` | Phase 4：资产规划逻辑、三类资产生成标准 |
| `references/storyboard/` | Phase 5：多宫格系统、视频提示词、产品拆解、End Frame |
| `references/delivery/` | Phase 6-7：输出格式模板、迭代策略、交付流程 |

### 触发词

「帮我做一条xx产品广告」「写一个产品 Hero Shot 提示词」「帮我做分镜」「这张产品图xx不对」

---

## 🏗 complex-skill-builder

**复杂 Skill 构建器 — 用控制塔+仓库架构系统化构建大规模 Skill。**

基于 [garden-skills](https://github.com/ConardLi/garden-skills) 的工程实践。当一个 skill 需要管理 50+ 模板、10+ 脚本、覆盖多种运行环境时，把全部内容塞进 SKILL.md 会撑爆 Agent 上下文。解法：**控制塔（SKILL.md ≤15k）+ 仓库（references/ 按需加载）**。

### 六阶段工作流

```
Phase 0: 复杂度评估（3 个问题判 simple/complex）
   ↓
Phase 1: 搭骨架（目录结构 + 用户确认）← 硬检查点
   ↓
Phase 2: 写控制塔（SKILL.md 9 章节按序写）
   ↓
Phase 3: 拆仓库（references/ 分类建模板）
   ↓
Phase 4: 加脚本（环境探测、API 封装等确定性逻辑）
   ↓
Phase 5: 验证（9 项 Hermes 格式合规检查）
   ↓
Phase 6: 交付（文件清单 + 测试指引）
```

### 核心文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 控制塔 — 复杂度评估 + 6 阶段工作流 + 决策表 |
| `references/methodology.md` | 完整方法论文档（10 个设计维度） |
| `references/hermes-format-cheatsheet.md` | Hermes Skill 格式规范速查 |

### 触发词

「帮我建一个复杂 skill」「这个 skill 太大了怎么拆」「设计一个多模板的 skill」「skill 架构设计」

---

## 🚀 安装为 Hermes Agent Skill

本项目中的每个 skill 都是 Hermes Agent 的原生 Skill（遵循 SKILL.md 规范）。

### 方式一：作为独立 Skill 安装

在 Hermes Agent 中运行：

```bash
hermes tools install path/to/ai-project-scout/SKILL.md
```

或直接复制到 Hermes 的 skills 目录：

```bash
cp -r ai-project-scout ~/AppData/Local/hermes/skills/
```

### 方式二：克隆整个合集

```bash
git clone https://github.com/wumajiehechuan-lab/hermes-skills.git
cd hermes-skills
```

然后按需加载各 skill。

---

## 📋 技能关系图

```
                    ┌─────────────────────┐
                    │  ai-project-scout    │
                    │  (市场侦察·灵感获取)  │
                    └─────────┬───────────┘
                              │ 发现竞品/趋势
                              ▼
┌─────────────────┐    ┌─────────────────────┐
│ concept-to-canvas│───▶│     biz-canvas      │
│ (从0到1生成方案)  │    │  (拆解验证已有项目)  │
└─────────────────┘    └──────────┬──────────┘
                                  │
                                  ▼
                        ┌─────────────────────┐
                        │ business-concept-    │
                        │ workout (多轮打磨)    │
                        └─────────────────────┘

        ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
        │   complex-skill-builder         │
        │   (构建复杂 Skill 的基础设施)     │
        │                                 │
        │   所有 skill 的开发都由此驱动     │
        └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘

┌─────────────────────┐
│    tvc-director      │
│ (TVC广告创意导演)     │
│                      │
│ 复杂 Skill 设计范例   │
│ 控制塔+仓库架构落地   │
└─────────────────────┘
```

---

## 🛠 开发环境

- **操作系统：** Windows 11 / macOS / Linux
- **Python 版本：** ≥ 3.10
- **包管理：** `pip install -r requirements.txt`（各 skill 依赖见脚本头部）
- **依赖：** `markdown`, `httpx`（scout.py 用）

---

## 🤝 贡献

欢迎提交 Issue 和 PR！如果你有自己的 Hermes Agent Skill 想加入合集，请先开 Issue 讨论。

### 开发约定

- 所有 Skill 遵循 Hermes Agent 的 `SKILL.md` 规范（YAML frontmatter + markdown 正文）
- 脚本输出路径统一使用 `/e/work/hermes/<skill-name>-output/`（开发环境约定）
- 注释用中文，代码用英文
- `snake_case` 命名，PEP8 标准

---

## 📄 License

MIT — 可自由使用、修改、分享。

---

*由 [四喜](https://github.com/wumajiehechuan-lab) 创建 — 一个人全栈开发者的 AI Agent 工具箱*
