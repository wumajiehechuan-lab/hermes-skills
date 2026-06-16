# -*- coding: utf-8 -*-
"""scout.py — 纯数据抓取。从 Product Hunt + Indie Hackers 抓取 AI 项目，输出 JSON。

用法:
    python scout.py                        # 默认：PH 30 条, IH 20 条
    python scout.py -p 20 -i 30            # PH 20 条, IH 30 条
    python scout.py --ph-min-followers 30  # IH 最低关注者 30 人
"""

import argparse, json, re, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import xml.etree.ElementTree as ET

OUTPUT_DIR = Path("E:/work/hermes/ai-project-scout-output")
SEEN_IDS_FILE = OUTPUT_DIR / "seen_ids.json"
RAW_JSON_FILE = OUTPUT_DIR / "raw_latest.json"
TZ = timezone(timedelta(hours=8))

AI_PATTERNS = [
    r"\bai\b", r"\bartificial intelligence\b", r"\bmachine learning\b",
    r"\bllms?\b", r"\bgpts?\b", r"\bchatgpt\b", r"\bcopilots?\b",
    r"\bagents?\b", r"\bautomation\b", r"\bgenerative\b", r"\bclaude\b",
    r"\bopenai\b", r"\blangchain\b", r"\brag\b", r"\bvectors?\b",
    r"\bembeddings?\b", r"\bprompts?\b", r"\bfine.tun", r"\bdiffusion\b",
    r"\btransformers?\b", r"\bnlp\b", r"\bllama\b", r"\bmistral\b",
    r"\bgemini\b", r"\bchatbots?\b", r"\bdeepseek\b", r"\bdeep.learning\b",
    r"\bneural\b", r"\bhugging.face\b", r"\bstable.diffusion\b",
]

IH_APP_ID = "N86T1R3OWZ"
IH_API_KEY = "5140dac5e87f47346abbda1a34ee70c3"


def is_ai_related(text: str) -> bool:
    return any(re.search(p, text.lower()) for p in AI_PATTERNS)


def load_seen_ids() -> set:
    if SEEN_IDS_FILE.exists():
        return set(json.loads(SEEN_IDS_FILE.read_text(encoding="utf-8")))
    return set()


def save_seen_ids(ids: set):
    SEEN_IDS_FILE.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8")


def clean_html(text: str) -> str:
    text = text.replace("&#x27;", "'").replace("&#x2F;", "/").replace("&amp;", "&")
    text = text.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_ph_detail_description(ph_url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = httpx.get(ph_url, headers=headers, timeout=15, follow_redirects=True)
        r.raise_for_status()
        for pattern in [
            r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"',
            r'<meta[^>]+name="description"[^>]+content="([^"]+)"',
        ]:
            m = re.search(pattern, r.text)
            if m:
                desc = m.group(1)
                desc = desc.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                desc = desc.replace("&quot;", '"').replace("&#x27;", "'").replace("&#x2F;", "/")
                return desc.strip()
    except Exception:
        pass
    return ""


def fetch_ph(max_items: int = 30) -> list[dict]:
    """从 Product Hunt RSS 抓取，最多 max_items 条。"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = httpx.get("https://www.producthunt.com/feed", headers=headers, timeout=15)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    results = []
    for entry in root.findall("atom:entry", ns):
        if len(results) >= max_items:
            break

        id_el = entry.find("atom:id", ns)
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link", ns)
        pub_el = entry.find("atom:published", ns)
        content_el = entry.find("atom:content", ns)

        post_id = id_el.text.split("/")[-1] if id_el is not None else ""
        title = title_el.text if title_el is not None else ""
        content = content_el.text if content_el is not None else ""
        ph_url = link_el.attrib.get("href", "") if link_el is not None else ""

        if not is_ai_related(title + " " + content):
            continue

        rss_desc = clean_html(content)
        rss_desc = re.sub(r"\s*Discussion\s*\|\s*Link\s*$", "", rss_desc).strip()

        results.append({
            "id": f"ph_{post_id}", "source": "product_hunt",
            "name": title.strip(), "url": ph_url,
            "description": rss_desc,
            "published_at": pub_el.text[:10] if pub_el is not None else "",
            "signals": {},
        })

    # 逐个抓详情页描述（限速）
    for i, item in enumerate(results):
        detail_desc = fetch_ph_detail_description(item["url"])
        if detail_desc and len(detail_desc) > len(item["description"]):
            item["description"] = detail_desc
        if i < len(results) - 1:
            time.sleep(0.3)

    return results


def fetch_ih(max_items: int = 20, min_followers: int = 10) -> list[dict]:
    """从 Indie Hackers Algolia 搜索，按关注者过滤。"""
    url = f"https://{IH_APP_ID}-dsn.algolia.net/1/indexes/products/query"
    headers = {
        "X-Algolia-Application-Id": IH_APP_ID,
        "X-Algolia-API-Key": IH_API_KEY,
        "Content-Type": "application/json",
    }
    r = httpx.post(url, headers=headers, json={
        "query": "AI",
        "hitsPerPage": max_items,
        "numericFilters": [f"numFollowers>{min_followers}"],
    }, timeout=15)
    r.raise_for_status()

    results = []
    for hit in r.json().get("hits", []):
        rev = hit.get("revenue", 0)
        if isinstance(rev, bool):
            rev = 0
        results.append({
            "id": f"ih_{hit['objectID']}", "source": "indie_hackers",
            "name": hit.get("name", "").strip(),
            "url": hit.get("websiteUrl", ""),
            "tagline": hit.get("tagline", ""),
            "description": (hit.get("description", "") or "").strip(),
            "published_at": _ts_to_date(hit.get("createdTimestamp")),
            "signals": {
                "followers": hit.get("numFollowers", 0),
                "revenue": rev,
                "tags": hit.get("_tags", []),
            },
        })
    return results


def _ts_to_date(ts) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts) / 1000, tz=TZ).strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return ""


def main():
    parser = argparse.ArgumentParser(description="AI 创业项目侦察员 — 数据抓取")
    parser.add_argument("-p", "--ph-count", type=int, default=30,
                        help="Product Hunt 抓取上限 (默认 30)")
    parser.add_argument("-i", "--ih-count", type=int, default=20,
                        help="Indie Hackers 抓取条数 (默认 20)")
    parser.add_argument("--ph-min-followers", type=int, default=10,
                        help="IH 最低关注者数 (默认 10)")
    parser.add_argument("--no-detail", action="store_true",
                        help="跳过 PH 详情页抓取（更快但简介更短）")
    args = parser.parse_args()

    today = datetime.now(TZ).strftime("%Y-%m-%d")
    print(f"=== AI 项目侦察员 === {today}")
    print(f"参数: PH≤{args.ph_count}条, IH≤{args.ih_count}条, IH最低关注者≥{args.ph_min_followers}人")
    if args.no_detail:
        print("PH 详情页: 跳过")
    print()

    seen_ids = load_seen_ids()
    all_items = []

    # Product Hunt
    detail_label = "(跳过详情页)" if args.no_detail else "(含详情页抓取，约 10-15 秒)"
    print(f"[1/2] Product Hunt {detail_label}...")
    try:
        # 如果跳过详情页，直接替换 fetch_ph_detail_description 为空函数
        if args.no_detail:
            global fetch_ph_detail_description
            fetch_ph_detail_description = lambda url: ""
        items = fetch_ph(max_items=args.ph_count)
        new_items = [i for i in items if i["id"] not in seen_ids]
        print(f"  {len(items)} 条 -> 新增 {len(new_items)} 条")
        all_items.extend(new_items)
    except Exception as e:
        print(f"  失败: {e}")

    # Indie Hackers
    print(f"[2/2] Indie Hackers...")
    try:
        items = fetch_ih(max_items=args.ih_count, min_followers=args.ph_min_followers)
        new_items = [i for i in items if i["id"] not in seen_ids]
        print(f"  {len(items)} 条 -> 新增 {len(new_items)} 条")
        all_items.extend(new_items)
    except Exception as e:
        print(f"  失败: {e}")

    for item in all_items:
        seen_ids.add(item["id"])
    save_seen_ids(seen_ids)

    output = {"date": today, "total": len(all_items), "items": all_items}
    RAW_JSON_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n原始数据: {RAW_JSON_FILE}")
    print(f"新增 {len(all_items)} 个，累计 {len(seen_ids)} 个")
    print("下一步: python render.py 生成中文日报")


if __name__ == "__main__":
    main()
