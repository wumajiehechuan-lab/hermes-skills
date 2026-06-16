---
name: ai-project-scout
description: 从 Product Hunt 和 Indie Hackers 抓取 AI/agent 创业项目，agent 翻译为中文日报。触发词：AI日报、AI创业项目、今天有什么新项目、抓取AI产品、AI工具推荐。
---

# AI 项目侦察员

从 Product Hunt、Indie Hackers 抓取 AI 创业项目，翻译为中文日报。

## 工作流

1. 运行 `python scripts/scout.py [参数]` 抓取数据
2. 读取 `E:/work/hermes/ai-project-scout-output/raw_latest.json`
3. agent 逐条翻译 `description` 为流畅中文
4. 按模板写入 `E:/work/hermes/ai-project-scout-output/YYYY-MM-DD.md`

## 自然语言 → 参数

| 用户意图 | 命令 |
|----------|------|
| "AI 日报" / "今天有什么新项目" | `python scripts/scout.py` |
| "少一点" / "只看 10 条" | `python scripts/scout.py -p 10 -i 10` |
| "快速预览" / "不用太详细" | `python scripts/scout.py --no-detail` |
| "只要高关注度" | `python scripts/scout.py --ph-min-followers 50` |
| "只看 PH" | `python scripts/scout.py -i 0` |

## 输出路径

所有输出文件统一存放到工作目录下：
- 原始 JSON：`E:/work/hermes/ai-project-scout-output/raw_latest.json`
- 中文日报：`E:/work/hermes/ai-project-scout-output/YYYY-MM-DD.md`
- 已见去重：`E:/work/hermes/ai-project-scout-output/seen_ids.json`

输出目录在 `scripts/scout.py` 中定义（`OUTPUT_DIR`），不要放在 skill 目录内。

## 翻译要求

- 保留原意，简洁流畅（每条 2-4 句）
- 标签用中文映射：`commitment-full-time→全职`、`founders-solo→单人创业`、`funding-bootstrapped→自筹资金`、`revenue-model-subscription→订阅制` 等
- 映射表见 `scripts/scout.py` 内 `TAG_CN`

## 日报模板

```markdown
# AI 创业项目日报 — YYYY-MM-DD

> 自动抓取自 Product Hunt、Indie Hackers，agent 翻译为中文
> 本次新增 N 个项目

---

## 一、Product Hunt 新 AI 产品

共 N 个新产品。

### 1. 产品名
- 链接：URL
- 上架日期：YYYY-MM-DD
- 简介：中文翻译

---

## 二、Indie Hackers 有收入的 AI 项目

共 N 个项目，附收入数据与商业模式标签。

### 1. 产品名
- 链接：URL
- 标语：英文 tagline
- 关注者：N 人 | 收入：$XXX
- 简介：中文翻译
- 标签：全职、单人创业、自筹资金、订阅制...

---

> 生成时间：YYYY-MM-DD HH:MM CST
> 累计追踪项目数：N
```
