# Hermes Skill 格式速查

> 从 `hermes-agent-skill-authoring` skill 和 `tools/skill_manager_tool.py` 提取，供 `complex-skill-builder` 验证阶段使用。

## Frontmatter 硬要求

```yaml
---
name: my-skill-name               # 必须：小写+连字符，≤64字符
description: Use when <trigger>. <one-line>.  # 必须：≤1024字符
version: 1.0.0                    # 推荐
author: Hermes Agent              # 推荐
license: MIT                      # 推荐
metadata:
  hermes:
    tags: [tag1, tag2]            # 推荐
    related_skills: [other-skill] # 推荐
---
```

- 文件必须以 `---` 开头（第 0 字节），前面不能有空行或 BOM
- YAML 块以 `\n---\n` 关闭
- `description` 必须以 "Use when ..." 开头
- 总体 ≤ 100,000 字符硬限制，**推荐 8,000-15,000 字符**

## 文件组织

```
skill-name/
├── SKILL.md          # 必须有
├── references/       # 可选：详细文档，Agent 按需加载
├── scripts/          # 可选：可执行脚本
├── templates/        # 可选：脚手架/样板
└── assets/           # 可选：静态资源
```

只有这 4 个子目录被 `skill_manage(action='write_file')` 允许。

## 推荐结构

```
# <Title>

## Overview
（1-2 段：做什么，为什么）

## When to Use
- 触发器 1
- 触发器 2
- 不要用于: ...

## <按需的主题章节>

## Common Pitfalls  ← 必须有
（编号列表：错误 + 修复）

## Verification Checklist  ← 必须有
- [ ] 检查项 1
- [ ] 检查项 2
```

## Description 模板

```
Use when <触发条件>. <一句话描述行为>.
```

好的例子:
- `Use when the user asks to build, extend, or refactor a complex Skill with many templates or scripts. Guides through control-tower + warehouse architecture with progressive disclosure.`
- `Use when debugging a Python traceback. Systematic four-phase approach: reproduce → isolate → diagnose → fix.`

坏的例子:
- `A skill for debugging`（缺触发条件）
- `Use when you need to do stuff with things`（太模糊）

## SKILL.md 大小梯度

| 范围 | 判断 | 行动 |
|---|---|---|
| ≤ 8,000 | 小 skill | OK |
| 8,000–15,000 | **推荐范围** | ✅ 最佳 |
| 15,000–20,000 | 偏大 | 考虑拆 references |
| 20,000–100,000 | 过大 | **必须拆 references** |
| > 100,000 | 非法 | Hermes 硬拒绝 |
