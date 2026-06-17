# 仓库设计指南

> 给 Phase 3 使用。Agent 拆 references/ 时参考，不一次性加载其他 reference。

---

## 模板索引格式

在 SKILL.md 中只列目录 + 文件名 + 一句话描述：

```markdown
## 模板索引

### 分类 A（`references/category-a/`）
- `template-1.md` — 电商直播截图样机
- `template-2.md` — 社交平台动态详情页

### 分类 B（`references/category-b/`）
- `template-3.md` — 产品爆炸视图海报
```

**Agent 使用路径**：用户说「做个直播 UI」→ Agent 在索引中定位 `category-a/` → 加载 `template-1.md`。总共 2 次文件读取。

---

## 模板文件内部格式

**不强行统一。** 根据任务性质选格式：

| 任务类型 | 推荐格式 | 原因 |
|---|---|---|
| UI 设计、技术图表、结构化输出 | **JSON 模板** | 字段明确，参数可验证 |
| 手绘信息图、科学示意图、创意文案 | **结构化自然语言** | 保留创作自由度 |

### JSON 模板示例

适合结构化任务。`{argument ...}` 标记可替换参数，`default` 标记默认值：

```json
{
  "task": "generate_image",
  "style": "cinematic_product_photography",
  "subject": {"type": "{user_input}", "description": "{argument ...}"},
  "background": {"default": "studio_gradient"},
  "composition": "centered_with_negative_space"
}
```

### 自然语言模板示例

适合创意任务：

```markdown
## 参数
- 主题: {topic}
- 风格: {style}（默认 macaron）
- 密度: {density}（低/中/高）

## Prompt 结构
[画面描述] 以 {style} 风格绘制 {topic} 的信息图。
[布局要求] 模块化网格排布，每格一个独立知识点。
[色彩约束] 使用 {color_palette} 色板，背景留白。
```

---

## 文件大小

| 内容 | 目标大小 |
|---|---|
| 单个 reference 文件 | 2,000–5,000 字符 |
| SKILL.md 总体 | 8,000–15,000 字符 |
| references/ 总规模 | 不限（按需加载，不影响上下文） |

单个 reference 超过 5,000 字符 → 考虑再拆。

---

## 输出约定

复杂 skill 产出文件必须有统一的落盘规则：

```markdown
## 默认输出目录

- 中间产物: `<skill-name>-output/prompt/`
- 最终产物: `<skill-name>-output/image/`
- 目录不存在时自动创建

## 默认命名规则

`<task-slug>-<timestamp>.<ext>`

- `task-slug`: 从任务自动提取的短名（如 `live-commerce-ui`）
- `timestamp`: `YYYYMMDD-HHMMSS`

示例:
- `<skill-name>-output/prompt/live-commerce-ui-20260424-153045.md`
- `<skill-name>-output/image/live-commerce-ui-20260424-153045.png`
```

---

## 分类目录设计

- 按**任务类型**分类，不按文件格式分类
- 嵌套不超过 2 层（目录 → 文件）
- 每个分类可加 `README.md` 作为子导航（可选）

好的分类：
```
references/
├── ui-mockups/         ← 界面样机
├── product-visuals/    ← 产品视觉
└── technical-diagrams/ ← 技术图表
```

坏的分类：
```
references/
├── json/               ← 按格式分，Agent 无法判断哪个模板适用
├── markdown/
└── prompts/
```
