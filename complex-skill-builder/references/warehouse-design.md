# 仓库设计指南

> 给 Phase 3 使用。Agent 拆 references/ 时参考，不一次性加载其他 reference。

---

## 模板文件内部结构规范

每个模板文件必须包含以下元信息章节。参考 gpt-image-2 的 `live-commerce-ui.md` 模板：

```markdown
# <模板名称>

<一句话说清这个模板做什么>

## 适用于
- 场景 1
- 场景 2
- 场景 3

## 不要用于（如适用）
- 不适合的场景（避免 Agent 误匹配）

## 使用规则
<这个模板的核心逻辑——哪些字段用户可以指定、可默认、可随机>

## 缺失信息优先提问顺序
当用户信息不足时，按此顺序逐一询问（最重要的排第一）：
1. 问题 1 — 为什么关键
2. 问题 2
3. 问题 3

如果用户不想逐项回答，提供「自动补全模式」入口。

## 参数策略
| 参数名 | 策略 | 说明 |
|---|---|---|
| product_name | **必问** | 没有商品名画面无意义 |
| background | **可默认** | studio 背景通用且安全 |
| chat_messages | **可随机** | 随机生成合理对话不影响质量 |

## 模板
<JSON 或自然语言模板正文>

## 变体指南（如适用）
<告诉 Agent 如何根据用户输入切换变体>
```

### 章节说明

| 章节 | 必须 | 说明 |
|---|---|---|
| 标题 + 一句话 | ✅ | Agent 加载后第一眼就知道这个模板干什么 |
| 适用于 | ✅ | 正向匹配条件，帮助 Agent 判定是否选这个模板 |
| 不要用于 | 推荐 | 反向排除，防止 Agent 错误匹配 |
| 使用规则 | ✅ | 告诉 Agent 这个模板的「玩法」——哪些可以定制、默认、随机 |
| 缺失信息优先提问顺序 | ✅ | 避免 Agent 问一堆无关问题；最重要的问题排第一 |
| 参数策略 | 推荐 | 结构化列出每个参数的策略（必问/可默认/可随机） |
| 模板正文 | ✅ | JSON 或自然语言 |
| 变体指南 | 推荐 | 告诉 Agent 如何根据用户输入切换变体 |

---

## 模板索引与模板文件的联动

**索引（SKILL.md 里）怎么写，才能让 Agent 快速判定该用哪个模板？**

索引每一条必须包含：(1) 文件名 (2) 一句话描述 (3) 关键词标签。

```markdown
## 模板索引

### 直播/社交 UI（`references/ui-mockups/`）
- `live-commerce-ui.md` — 电商直播带货截图样机（主播+聊天+礼物+商品卡）
  标签：直播, 电商, 带货, 主播, 抖音, 小红书, 淘宝
- `social-interface-mockup.md` — 社交平台动态详情页（Twitter/X/微博/Threads）
  标签：社交, 截图, 推文, 动态, 评论区
- `chat-interface-scene.md` — 聊天/对话界面样机（iMessage/微信/群聊/AI助手）
  标签：聊天, 对话, 气泡, 消息, 微信, iMessage
```

**Agent 匹配逻辑**：用户说「做个直播带货图」→ Agent 扫索引 → `live-commerce-ui.md` 的「直播, 电商, 带货」命中 → 加载该文件。不需要读完所有模板。

---

## 参数占位符完整语法

```
{argument name="参数名" default="默认值"}
```

### 语法规则

| 元素 | 必须 | 说明 |
|---|---|---|
| `argument` | ✅ | 关键字，固定不变 |
| `name="..."` | ✅ | 参数名，给 Agent 看懂用的（如 `host name`、`product price`） |
| `default="..."` | 可选 | 默认值。Agent 在用户未提供时使用此值，不提问 |
| `required=true` | 可选 | 标记必填参数（Agent 必须询问用户） |

### 使用示例

```json
{
  "subject": {
    "name": "{argument name=\"host name\" default=\"Elon Musk\"}",
    "photo_url": "{argument name=\"host photo\" required=true}",
    "pose": "{argument name=\"host pose\" default=\"正对镜头，轻微前倾\"}"
  },
  "product": {
    "price": "{argument name=\"product price\" default=\"¥ 1,618,000\"}",
    "custom_text": "{argument name=\"custom overlay text\" required=true}"
  }
}
```

- `host name`：有 default → Agent 直接使用默认值，不提问
- `host photo`：required=true，无 default → Agent **必须**问用户
- `host pose`：有 default → 直接用
- `product price`：有 default → 直接用
- `custom overlay text`：required=true，无 default → **必须**问

### Agent 行为规则

1. 有 `default` 且无 `required` → 直接使用默认值
2. `required=true` 且无 `default` → **必须**调用 `clarify()` 询问
3. 都没有 → 如果字段对结果影响小，随机生成；影响大就询问
4. 用户说了「全部随机」→ 所有非核心字段随机生成

---

## 结构化 vs 创意任务的判断标准

| 维度 | 结构化任务 | 创意任务 |
|---|---|---|
| **输出可验证性** | 高——可以逐字段检查是否正确 | 低——质量取决于观感而非字段 |
| **字段边界** | 清晰——每个参数有明确的类型和范围 | 模糊——参数更像方向指引 |
| **举例** | UI 样机、技术图表、电商主图、架构图 | 手绘信息图、氛围插画、科学示意图、海报 |
| **推荐格式** | JSON 模板 | 结构化自然语言 |

判断方法：**闭眼想一下这个任务的输出，能用检查清单逐项验收吗？能 → JSON；不能 → 自然语言。**

---

## 拆分粒度原则

| 文件大小 | 判断 |
|---|---|
| 2,000–5,000 字符 | ✅ **甜点区**——Agent 一次加载不吃力，信息密度刚好 |
| < 1,000 字符 | ⚠️ 可能太碎——考虑合并到父级或相关文件 |
| 5,000–10,000 字符 | ⚠️ 偏大——如果 Agent 很少需要全部内容，拆开 |
| > 10,000 字符 | ❌ 太大——必须拆 |

**合并优于拆分的场景：**
- 两个模板**总是一起被使用**（如主模板 + 变体）→ 放同一个文件
- 三个以上 <1KB 的小模板属于同一个子分类 → 合并成一个文件，用 `## 模板 1 / ## 模板 2` 区分

**拆分过头的代价：** 模板太碎 → Agent 需要在多个文件间跳转 → 每次跳转是一次工具调用 → 延迟增加 + 出错概率增加。2-3 个 3KB 的文件比 6 个 1KB 的文件好。

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
└── markdown/
```

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
```
