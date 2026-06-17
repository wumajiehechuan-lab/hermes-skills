# 复杂 Skill 设计方案论

> **这是给人类阅读的完整参考文档（12KB）。Agent 执行时不要加载此文件。**
> Agent 请使用按 Phase 拆分的小文件：`control-tower-design.md`（Phase 2）、`warehouse-design.md`（Phase 3）、`hermes-format-cheatsheet.md`（Phase 5）。

> 基于 [garden-skills](https://github.com/ConardLi/garden-skills) 的工程实践提炼，适配 Hermes Agent 的 skill 格式规范。

---

## 一、核心问题

当一个 skill 需要管理 50+ 个模板、10+ 个脚本、覆盖多种运行环境时，**把全部内容塞进 SKILL.md 是自杀**——Agent 的上下文会被撑爆，定位信息的效率急剧下降。

garden-skills 的解法：**控制塔 + 仓库** 二层架构。

---

## 二、「控制塔 + 仓库」架构

```
skill-name/
├── SKILL.md              ← 控制塔：不超过 15k 字符
│                           只放结构、索引、决策逻辑、工作流
├── references/           ← 仓库：模板、数据、详细文档
│   ├── category-a/       ← 按类型分子目录
│   │   ├── template-1.md
│   │   └── template-2.md
│   ├── category-b/
│   └── prompt-writing.md ← 方法论总文档（先读）
├── scripts/              ← 引擎：确定性操作
│   ├── check-mode.js     ← 环境探测脚本
│   ├── generate.py       ← 核心执行脚本
│   └── shared.py         ← 共享逻辑
├── templates/            ← 可复用的脚手架/样板
└── assets/               ← 静态资源（字体、图标等）
```

### 控制塔（SKILL.md）放什么

| 内容类型 | 说明 |
|---|---|
| **运行模式判断** | 放最前面——Agent 必须先知道自己处于什么环境 |
| **技能结构概览** | scripts/ references/ 各有什么，一句话说清 |
| **模板索引** | 列出所有分类目录 + 每个目录下有哪些文件。不列具体内容 |
| **工作流** | 分步流程，标注检查点和分叉点 |
| **规则/约束** | 保存路径、命名规则、什么时候该问用户 |
| **决策表** | 多维度条件 → 行为映射 |

### 仓库（references/）放什么

- 每个具体模板一个 `.md` 文件
- 按任务类型分目录（gpt-image-2 分了 18 个目录）
- 不设嵌套超过 2 层（目录 → 文件）
- 提供一个大而全的 **方法论总文档**（如 `prompt-writing.md`），Agent 迷茫时先读这个

### 引擎（scripts/）放什么

- 环境探测脚本（**第一步必跑**）
- 核心执行脚本（API 调用、文件生成等）
- 共享工具函数

### 关键原则

> **Agent 永远不要一次性加载整个 references/。**

SKILL.md 的索引让 Agent 先定位到正确的分类目录（1 次 read），再加载具体模板文件（1 次 read），总共 2 次文件读取就能拿到需要的内容。不要写 "read all templates" 这类指令。

---

## 三、环境探测优先（Mode Detection）

skill 不应该假设自己的运行环境——它应该**先探测，再决定怎么干活**。

### 模式

```python
# scripts/check_mode.py
import os

def detect_mode():
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    has_image_tool = check_host_image_tools()  # 这里需要由 Agent 自检
    
    if os.getenv("ENABLE_LOCAL_GEN") == "1" and has_api_key:
        return "A"  # 完全自主模式
    elif has_image_tool:
        return "B"  # 委托宿主模式
    else:
        return "C"  # 纯顾问模式
```

### 在 SKILL.md 中的写法

```
## 运行模式（第一步：必须先确定）

运行 `python scripts/check_mode.py` 确定当前模式。

| 条件 | 模式 | 调用脚本？ | 落盘结果？ |
|---|---|---|---|
| API key + 开关开启 | **A** 自主 | ✅ | ✅ |
| 无 key，但宿主有工具 | **B** 委托 | ❌ | 可选 |
| 什么都没 | **C** 顾问 | ❌ | ❌ |

### Mode A · 自主模式
（完整端到端流程）

### Mode B · 委托模式
（当提示词工程指南用，调用宿主工具）

### Mode C · 顾问模式
（只输出结果给用户，明确告知"你需要在工具 X 中执行"）
```

### 为什么这很重要

Agent 可能在完全不同的宿主中运行（Hermes 桌面端 vs IDE 插件 vs 云端 cron job），skill 如果假设了某个环境，换一个环境就炸。**探测 → 分叉** 让一个 skill 适应所有环境。

---

## 四、模板索引设计

### 分层索引，不列内容

```markdown
## 模板索引

### 1. 方法论总文档
先读：`references/prompt-writing.md`

### 2. UI Mockups（`references/ui-mockups/`）
- `live-commerce-ui.md` — 电商直播截图样机
- `social-interface-mockup.md` — 社交平台动态详情页
- `product-card-overlay.md` — 落地页 hero/详情页主图

### 3. 产品视觉（`references/product-visuals/`）
- `exploded-view-poster.md` — 产品爆炸视图海报
- `white-background-product.md` — 电商纯白底主图
...
```

Agent 读到这个索引就知道：用户要做直播 UI → 进 `ui-mockups/` → 读 `live-commerce-ui.md`。不需要读完 80 个模板。

### 模板文件内部格式

**结构化任务**（UI、图表、技术图）→ JSON 模板：

```json
{
  "task": "generate_image",
  "style": "cinematic_product_photography",
  "subject": {"type": "{user_input}", "description": "{argument ...}"},
  "background": {"default": "studio_gradient", "override": "{argument ...}"},
  "composition": "centered_with_negative_space",
  "lighting": "dramatic_rim_light"
}
```

**创意任务**（手绘、科学示意图）→ 结构化自然语言：

```markdown
## 参数
- 主题: {topic}
- 风格: {style}（默认 macaron）
- 密度: {density}（低/中/高）

## Prompt 结构
[画面描述] 以 {style} 风格绘制 {topic} 的信息图。
[布局要求] 模块化网格排布，每格一个独立知识点...
[色彩约束] 使用 {color_palette} 色板，背景留白...
```

**不强行统一格式**——用 JSON 套创意任务会限制发挥，用自然语言套结构化任务会不够精确。

---

## 五、决策表替代嵌套条件

当 Agent 面临多维度判断时，**不要写 if-else 散文，画表**。

### 错误写法

> 如果用户给了 PRD 且目标明确，就直接开始；如果用户给了 PRD 但目标不明确，就要问受众和渠道；如果没有 PRD 但用户给了参考图，就提取设计 tokens；如果没有 PRD 也没有参考图但提到了品牌名，就去搜索品牌信息；如果什么都没有……

### 正确写法

```markdown
## Step 1: 判断要不要问用户

| 场景 | 行为 |
|---|---|
| 给了 PRD + 明确目标 | ❌ 不问，直接开始 |
| 给了 PRD 但目标模糊 | ⚠️ 只问 1-2 个关键问题 |
| 只有一句话（"做个海报"） | ✅ 必须深入询问 |
| 给了参考图/URL | ❌ 先提取参考信息，不够再问 |
| 什么都没给 | ⚡ 切换到设计方向建议模式 |
```

Agent 对表格的理解比长段散文准确得多。

---

## 六、硬检查点（Human-in-the-Loop）

复杂多阶段任务必须在关键节点停下来等用户确认，否则 Agent 一口气跑到底，产出全废。

```markdown
## 工作流

Phase 1: 内容准备
  1.1 分析输入 → 产出草案
  1.2 产出 script.md + outline.md
  ▼
**[检查点 1]** ← 必须停！确认 5 件事：稿子 / 大纲 / 主题 / 素材 / 模式
  ▼
Phase 2: 执行
  2.1 做第一章
  ▼
**[检查点 2]** ← 必须停！用户验收第一章
  ▼
  2.2 做剩余章节
```

在 Hermes 中用 `clarify()` 实现检查点。

### 检查点设计原则

- **放在不可逆操作之前**（生成 100 张图之前先确认 1 张样图）
- **放在信息分叉点**（用户的一个选择会改变后续所有输出）
- **每次最多确认 5 件事**（超过 5 件就拆成两个检查点）

---

## 七、反模式防护

告诉 Agent **不准做什么**，比告诉它做什么更重要——AI 最擅长在边界条件处走歪。

### 三类防护

**① 禁止短语**

```markdown
## 禁止行为
- ❌ 禁止在未读到实际结果时说"已完成"
- ❌ 禁止把元信息（模式说明、索引结构）混入用户可见的输出
- ❌ 禁止跳过文件处理步骤直接对原始 PDF 检索
```

**② 强制检查清单**

```markdown
## 处理 PDF 前的强制检查清单
- [ ] ✅ 已读取 references/pdf-reading.md
- [ ] ✅ 已理解推荐的工具和命令
- [ ] ✅ 已将文件处理（提取/转换）完成
- [ ] ⏭️ 现在可以开始检索
```

**③ 错误回退路径**

```markdown
### Mode A 失败时
生成脚本返回 401/网络错误/配额耗尽 → 
不要重试 → 立即报错并询问用户："切到 Mode B 或 C？"
```

---

## 八、输出约定

复杂 skill 产出的文件必须有统一的落盘规则，否则项目目录会变成垃圾场。

```markdown
## 默认输出目录

- 中间产物: `project-name/prompt/`
- 最终产物: `project-name/output/`
- 目录不存在时自动 `mkdir -p`

## 默认命名规则

`<task-slug>-<timestamp>.<ext>`

- `task-slug`: 根据任务自动提取的短名（如 `live-commerce-ui`）
- `timestamp`: `YYYYMMDD-HHMMSS`

示例:
- `project-name/prompt/live-commerce-ui-20260424-153045.md`
- `project-name/output/live-commerce-ui-20260424-153045.png`
```

---

## 九、适配 Hermes 格式规范

garden-skills 的设计技法完全适用于 Hermes，但需要套上 Hermes 的格式壳：

### Frontmatter 补全

```yaml
---
name: my-complex-skill
description: Use when <trigger>. <one-line behavior>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [domain, task-type]
    related_skills: [other-skill-name]
---
```

### 结构对齐

```
# Skill Title

## Overview
（控制塔概览：这个 skill 做什么、分几层）

## When to Use
- 触发器 1
- 触发器 2
- 不要用于: 边界情况

## 运行模式（如有）
（探测 → 分叉 → 决策表）

## Skill 结构
（scripts/ references/ 各有什么）

## 模板索引
（分类目录 → 文件列表，不列内容）

## 工作流
（分步 + 检查点标注）

## 规则与约束
（输出路径、命名规则、询问规则）

## Common Pitfalls
（禁止行为 + 错误回退路径）

## Verification Checklist
- [ ] 已跑环境探测脚本
- [ ] 已确认运行模式
- [ ] 产物已落盘到正确路径
- [ ] 已告知用户模式和输出位置
```

### 体量控制

| 内容 | 目标大小 | 说明 |
|---|---|---|
| SKILL.md | 8,000–15,000 字符 | Hermes 推荐范围 |
| 单个 reference 文件 | 2,000–5,000 字符 | 一次加载不吃力 |
| references/ 总规模 | 不限 | 按需加载，不影响上下文 |
| 描述 | ≤ 1,024 字符 | Hermes 硬限制 |

---

## 十、设计检查清单

设计一个复杂 skill 时，逐项勾对：

- [ ] SKILL.md ≤ 15k 字符（超了就往 references/ 搬）
- [ ] 模板/数据全部放在 references/ 子目录中
- [ ] 模板索引在 SKILL.md 中，只列文件名+一句话描述，不列内容
- [ ] 不确定的运行环境有探测脚本 + 决策表
- [ ] 多维度条件判断用表格而非散文
- [ ] 长流程有硬检查点（用 `clarify()` 暂停等确认）
- [ ] 有明确的禁止行为列表
- [ ] 有错误回退路径
- [ ] 输出路径和命名规则明确
- [ ] Frontmatter 完整（name/description/version/author/license/metadata）
- [ ] 有 `## Common Pitfalls` 章节
- [ ] 有 `## Verification Checklist` 章节
- [ ] 描述以 "Use when" 开头，≤ 1024 字符

---

## 参考案例

- [garden-skills/gpt-image-2](https://github.com/ConardLi/garden-skills/tree/main/skills/gpt-image-2) — 80+ 模板、18 分类、3 运行模式的图像生成 skill
- [garden-skills/web-design-engineer](https://github.com/ConardLi/garden-skills/tree/main/skills/web-design-engineer) — 6 步设计工作流、25 种风格配方的 Web 设计 skill
- [garden-skills/kb-retriever](https://github.com/ConardLi/garden-skills/tree/main/skills/kb-retriever) — 分层索引 + 先学再处理的本地知识库检索 skill
