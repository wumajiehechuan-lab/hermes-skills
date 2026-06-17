---
name: complex-skill-builder
description: Use when the user asks to build, extend, or refactor a complex Skill with many templates, scripts, or environment variants. Applies control-tower + warehouse architecture with progressive disclosure, mode detection, and hard checkpoints. Not for simple one-shot skills.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, authoring, architecture, complex-skills]
    related_skills: [hermes-agent-skill-authoring]
---

# Complex Skill Builder

## Overview

Build complex Skills that stay maintainable when they grow past 50+ templates, 10+ scripts, or multiple runtime environments. Applies the "control-tower + warehouse" architecture distilled from [garden-skills](https://github.com/ConardLi/garden-skills).

The core insight: **SKILL.md is a control tower, not a warehouse.** Keep it under 15k chars — only structure, indexes, decision logic, and workflows. Everything else goes into `references/`, loaded on-demand by the Agent **only when that phase needs it**.

This skill itself demonstrates the pattern: SKILL.md is 6k (control tower), details live in small phase-aligned references.

## When to Use

- User asks to create a skill with many variants/templates/categories
- Skill needs to work across different environments (local, cloud, different agents)
- Skill has long multi-phase workflows with decision points
- Existing skill is ballooning past 15k chars and needs structural refactoring

Don't use for:
- Simple one-shot skills (≤3 steps, no variants)
- Skills that are just a short list of commands
- Quick fixes to existing skills (use `skill_manage(action='patch')` instead)

## Skill Structure

```
complex-skill-builder/
├── SKILL.md                              ← 本文件（6k 控制塔）
├── references/
│   ├── control-tower-design.md           ← Phase 2 用：SKILL.md 各节怎么写（2.5k）
│   ├── warehouse-design.md               ← Phase 3 用：模板索引、格式选择、输出约定（2.4k）
│   ├── hermes-format-cheatsheet.md       ← Phase 5 用：Hermes 格式规范速查（2.1k）
│   └── methodology.md                    ← 人类阅读完整参考（Agent 不加载）
```

**不预加载。** 每个 Phase 只读自己需要的那个 reference 文件。

## Workflow

### Phase 0: 复杂度评估（先问再动手）

问用户 3 个问题（用 `clarify()` 一次问完）：

1. 这个 skill 有几个变体/模板/子分类？
2. 是否需要在不同环境下工作？各环境行为差异大吗？
3. 是否有长流程（5+ 步）需要用户中途确认？

| 条件 | 判定 | 策略 |
|---|---|---|
| 模板<5, 单一环境, 短流程 | **Simple** | 直接写 SKILL.md，不拆 references |
| 任一条件触发 | **Complex** | 走 Phase 1-6 完整流程 |

### Phase 1: 搭骨架（必须用户确认）

1. 调用 `skill_manage(action='create')` 创建 skill（此时 SKILL.md 只放占位符）
2. 用 `skill_manage(action='write_file')` 创建目录结构:
   ```
   skill-name/
   ├── SKILL.md
   ├── references/
   │   ├── category-a/
   │   └── category-b/
   ├── scripts/        # 如有探测/生成脚本
   └── templates/      # 如有脚手架
   ```
3. **停。** 用 `clarify()` 展示骨架给用户确认后再继续。

### Phase 2: 写控制塔（SKILL.md）

**加载 `references/control-tower-design.md`** 获取各节写法指南。

SKILL.md 按此顺序写，每节控制在 500-1500 字符：

1. **Overview** — ≤3 句说清 skill 做什么
2. **When to Use** — 触发器 + 排除条件
3. **运行模式**（如有环境差异）— 先写探测方法，再画决策表。探测放最前面。
4. **Skill 结构** — 目录树 + 一行注释
5. **模板索引** — 分类目录 + 文件名 + 一句话描述（**不列内容！**）
6. **工作流** — 分步流程，标注 `[硬检查点]`
7. **规则与约束** — 输出路径、命名规则、询问规则
8. **Common Pitfalls** — ≥3 条（错误 + 原因 + 正确做法）
9. **Verification Checklist** — ≥5 项可自检项

关键技法（详见 control-tower-design.md）：
- **决策条件用表格**，不写 if-else 散文。多行表格 Agent 理解更准确。
- **硬检查点放在不可逆操作前**。用 `clarify()` 实现，每次确认 ≤5 件事。
- **反模式防护**：禁止短语 + 强制检查清单 + 错误回退路径。

硬约束：SKILL.md ≤ 15,000 字符。Description "Use when ..." 开头，≤ 1024 字符。

### Phase 3: 拆仓库（references/）

**加载 `references/warehouse-design.md`** 获取格式指南。

每个分类：
1. 创建 `references/<category>/` 子目录（按任务类型分，不按文件格式分）
2. 写入 `.md` 模板文件，每个 2,000-5,000 字符
3. 结构化的用 JSON 模板，创意的用自然语言模板——**不强行统一**

用 `skill_manage(action='write_file', file_path='references/...')` 写入。

### Phase 4: 加脚本（如有）

只加需要确定性执行的逻辑（环境探测、API 封装、文件转换）。
用 `skill_manage(action='write_file', file_path='scripts/...')` 写入。

### Phase 5: 验证

**加载 `references/hermes-format-cheatsheet.md`** 获取格式规范。

逐项检查：
- [ ] Frontmatter 完整，以 `---` 开头（第 0 字节）
- [ ] Description "Use when ..." 开头，≤ 1024 字符
- [ ] SKILL.md ≤ 15,000 字符（硬限 100,000）
- [ ] 有 `## Common Pitfalls` 章节（≥3 条）
- [ ] 有 `## Verification Checklist` 章节（≥5 项）
- [ ] 模板索引只列文件名+描述，不列内容
- [ ] 决策条件用表格
- [ ] 长流程标注了硬检查点
- [ ] 输出路径和命名规则明确（如有产出）

### Phase 6: 交付

告知用户：创建了哪些文件及各文件大小、SKILL.md 总大小、如何在新 session 中测试。

## Rules

1. **永远不要跳过 Phase 0**。3 个问题 30 秒能避免选错策略。
2. **Phase 1 骨架必须用户确认**后再写入内容。一口气写完 10 个文件然后全跑偏 = 浪费时间。
3. **每 Phase 只加载自己需要的 reference**。不要「先读 methodology.md」——那是给人类看的完整参考，Agent 按 Phase 按需加载小文件。
4. **SKILL.md 用 `skill_manage(action='edit')` 编辑，references/ 用 `skill_manage(action='write_file')` 写入**。
5. **不重复造轮子**——`hermes-agent-skill-authoring` 覆盖的格式细节直接引用。

## Common Pitfalls

1. **预加载所有 references**。本 skill 的 `references/methodology.md` 是 12KB 的人类参考文档，Agent **不要**加载它。每 Phase 只加载对应的 2-3KB 小文件。

2. **把模板内容写进索引**。索引只列文件名+一句话描述，具体内容在 references/ 里。Agent 需要时按路径加载。

3. **references/ 单个文件过大**。超过 5,000 字符的 reference 考虑再拆。Agent 按文件加载，加载 20k 的 reference = 没拆分。

4. **没有硬检查点**。用户说「做个海报生成 skill」，Agent 写了 10 个模板全跑偏。Phase 1 骨架必须等用户点头。

5. **忽略 Hermes 格式规范**。garden-skills 的 frontmatter 只放 name+description，Hermes 还要求 version/author/license/metadata。

6. **跳过环境探测设计**。如果 skill 可能在不同环境下运行（Hermes 桌面 vs cron job vs 不同 Agent），必须有模式检测和分叉逻辑。

## Verification Checklist

After building the skill, confirm:

- [ ] Phase 0 复杂度评估已完成（3 个问题已答）
- [ ] Phase 1 骨架已创建且用户已确认
- [ ] SKILL.md ≤ 15,000 字符
- [ ] Frontmatter 完整（name/description/version/author/license/metadata）
- [ ] Description "Use when ..." 开头，≤ 1024 字符
- [ ] 所有模板内容在 references/ 下，SKILL.md 只放索引
- [ ] 决策条件用表格
- [ ] 长流程标注了硬检查点
- [ ] 有 `## Common Pitfalls`（≥3 条）
- [ ] 有 `## Verification Checklist`（≥5 项）
- [ ] 输出路径和命名规则明确（如有产出文件）
