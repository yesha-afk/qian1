#!/usr/bin/env python3
"""
每天生成 AI 应用资讯，写到 docs/ai-news/YYYY-MM-DD.md
数据来源：Hacker News Algolia API（公开、无需 Key）
过滤过去 24 小时内和 AI 应用相关的帖子，取热度最高的 7 条。
"""
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

OUT_DIR = "docs/ai-news"

def fetch_hn():
    # 过去 24 小时的 Unix 时间戳
    since = int((datetime.now(timezone.utc) - timedelta(hours=24)).timestamp())
    # 搜索 AI 相关关键词
    query = "AI"
    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{since}",
        "hitsPerPage": 30,
    })
    url = f"https://hn.algolia.com/api/v1/search_by_date?{params}"
    req = urllib.请求.Request(url, headers={"User-Agent": "daily-ai-news-bot/1.0"})
    with urllib.请求.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("hits", [])

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    # 用北京时间日期命名，GitHub Actions 里是 UTC，需要 +8
    # 这里用 UTC+8 计算
    from datetime import timezone as tz
    beijing = datetime.now(tz(timedelta(hours=8)))
    today = beijing.strftime("%Y-%m-%d")
    path = os.path.join(OUT_DIR, f"{today}.md")

    hits = fetch_hn()
    # 按 points 排序，取前 7
    hits = sorted(hits, key=lambda x: x.get("points", 0), reverse=True)[:7]

    lines = []
    lines.append(f"# AI 应用资讯 {today}")
    lines.append("")
    lines.append(f"> 来源：Hacker News（过去 24 小时，关键词 AI，按热度排序）· 生成时间：{beijing.strftime('%Y-%m-%d %H:%M')} 北京时间")
    lines.append("")
    if not hits:
        lines.append("今天暂无符合条件的新资讯。")
    else:
        for i, h in enumerate(hits, 1):
            title = (h.get("title") or "无标题").strip()
            url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
            points = h.get("points", 0)
            comments = h.get("num_comments", 0)
            created = h.get("created_at", "")[:16].replace("T", " ")
            lines.append(f"## {i}. {title}")
            lines.append("")
            lines.append(f"- 热度：{points} points · 评论：{comments} · 发布时间：{created} UTC")
            lines.append(f"- 链接：{url}")
            lines.append(f"- 为什么值得看：这是过去 24 小时内 Hacker News 上热度较高的 AI 相关讨论，可作为今天的 AI 应用风向参考。")
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("说明：本文件由 GitHub Actions 每天自动生成，数据来自公开接口，未经人工编辑。如需更深度的解读，可结合你自己的关注方向再筛选。")
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {path} with {len(hits)} items")

if __name__ == "__main__":
    main()
