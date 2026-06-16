# Hermes Agent Skills 合集

> 一套面向独立开发者的 AI Agent 商业工具链 — 从概念打磨、竞品拆解到市场侦察，覆盖一个人创业的完整决策闭环。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-ready-blue)

---

## 概览

本项目是 [Hermes Agent](https://hermes-agent.nousresearch.com/docs) 的 Skills 合集，包含三个递进式的商业分析工具：

| Skill | 功能 | 适用阶段 |
|-------|------|---------|
| **[concept-to-canvas](#-concept-to-canvas)** | 从模糊概念到 Lean Canvas + VPC 商业方案骨架 | 想法萌芽期 → 方案设计 |
| **[biz-canvas](#-biz-canvas)** | 五维分析法拆解已有项目，评估可复制性与天花板 | 竞品分析期 → 可行性判断 |
| **[ai-project-scout](#-ai-project-scout)** | 自动抓取 Product Hunt / Indie Hackers AI 项目，生成中文日报 | 市场侦察期 → 灵感获取 |

**使用路径：** 有了点子 → `concept-to-canvas` 打磨方案 → 找到竞品 → `biz-canvas` 拆解验证 → 日常喂信息 → `ai-project-scout` 持续侦察。

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
└─────────────────┘    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ business-concept-    │
                    │ workout (多轮打磨)    │
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
