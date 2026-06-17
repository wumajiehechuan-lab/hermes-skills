# Complex Skill Builder

**用控制塔+仓库架构系统化构建复杂 Skill。让 80+ 模板、多运行环境、长流程的 skill 不再撑爆 Agent 上下文。**

[回到合集](../../README.md) · [SKILL.md](./SKILL.md)

---

## 解决什么问题

当一个 skill 需要管理 50+ 个模板、10+ 个脚本、覆盖多种运行环境时，**把所有内容塞进 SKILL.md 会撑爆 Agent 上下文**，定位信息的效率急剧下降。

解法来自 [garden-skills](https://github.com/ConardLi/garden-skills) 的工程实践：**控制塔 + 仓库** 二层架构。

| 层 | 文件 | 大小 | 内容 |
|---|---|---|---|
| 控制塔 | `SKILL.md` | ≤ 15k 字符 | 结构、索引、决策逻辑、工作流 |
| 仓库 | `references/` | 按需加载 | 模板、数据、详细文档 |

## 怎么工作

六阶段工作流，Agent 引导你一步步完成：

```
Phase 0: 复杂度评估（3 个问题判 simple 还是 complex）
   ↓
Phase 1: 搭骨架（目录结构 + 你确认）← 硬检查点
   ↓
Phase 2: 写控制塔（SKILL.md 按 9 章节顺序填充）
   ↓
Phase 3: 拆仓库（references/ 分类建模板文件）
   ↓
Phase 4: 加脚本（环境探测、API 封装——只加确定性逻辑）
   ↓
Phase 5: 验证（9 项 Hermes 格式合规检查）
   ↓
Phase 6: 交付（文件清单 + 测试指引）
```

**关键设计：每 Phase 只加载自己需要的 reference 文件（2-4KB），不预加载整个方法论。**

## 文件结构

```
complex-skill-builder/
├── SKILL.md                              ← 控制塔（8.7k）
├── references/
│   ├── control-tower-design.md           ← Phase 2 用：SKILL.md 各节写法 + 决策表 + 检查点（4.4k）
│   ├── warehouse-design.md               ← Phase 3 用：模板结构规范 + 参数语法 + 拆分粒度（7.1k）
│   ├── scripts-design.md                 ← Phase 4 用：脚本 vs SKILL.md 规则的分工标准（3.7k）
│   ├── hermes-format-cheatsheet.md       ← Phase 5 用：Hermes 格式合规速查（2.5k）
│   └── methodology.md                    ← 人类阅读的完整参考（Agent 不加载，16.4k）
```

## 内置设计知识

- **模板文件 7 章节内部结构规范**（对标 gpt-image-2 实战模板）：适用于 / 不要用于 / 使用规则 / 缺失信息优先提问顺序 / 参数策略 / 约束条件 / 变体指南
- **参数占位符完整语法**：`{argument name="..." default="..." required=true}` ——有 default 不问，required=true 必问
- **索引与模板联动**：SKILL.md 索引怎么写（文件名 + 描述 + 关键词标签），Agent 如何通过关键词匹配定位模板
- **决策表**：多维度条件判断用表格，不写 if-else 散文
- **硬检查点**：放在不可逆操作前和信息分叉点，用 `clarify()` 暂停
- **反模式防护**：禁止短语 + 强制检查清单 + 错误回退路径
- **拆分粒度原则**：2-5KB 甜点区，合并优于拆分过碎
- **脚本分工**：精确计算 → 脚本，语义判断 → SKILL.md 规则

## 触发词

在 Hermes Agent 中说以下任意一句即可触发：

- 「帮我建一个复杂 skill」
- 「这个 skill 太大了怎么拆」
- 「设计一个多模板的 skill」
- 「skill 架构设计」
- 「用 complex-skill-builder 设计」

## 不用于

- 简单的一次性 skill（≤3 步，无变体）——直接用 `skill_manage(action='create')` 更快
- 对已有 skill 的小修小补——用 `skill_manage(action='patch')` 更快

## 安装

### Hermes Agent（运行时）

```bash
# 从合集仓库复制到 Hermes skills 目录
cp -r complex-skill-builder ~/hermes/skills/software-development/
```

或通过 `skill_manage` 安装。

### 开发者（源码）

```bash
git clone https://github.com/wumajiehechuan-lab/hermes-skills.git
cd hermes-skills/complex-skill-builder
```

---

*基于 [garden-skills](https://github.com/ConardLi/garden-skills) 设计方法论 · MIT License*
