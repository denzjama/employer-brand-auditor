#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read recent posts of a public Telegram channel from its public web preview (t.me/s/<channel>).

No login, no bot and no API key: only channels that publish a public web preview can be read.
Used in deep collection (methodology/source-collection.md §5). Standard library only.

    python3 telegram_channel.py <channel name or t.me link> [--posts 40]

Output JSON: ok, channel, url, title, description, subscribers (as shown), posts_read,
period {from, to}, posts: [{id, date, views, text, media, link}], problem, hint.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_page import USER_AGENT, ssl_context  # noqa: E402

MAX_POSTS = 120


def get(url):
    ctx, _ = ssl_context(None)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.ProxyHandler())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "ru,en;q=0.8"})
    try:
        r = opener.open(req, timeout=25)
        return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def strip(fragment):
    fragment = re.sub(r"<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"<i class=\"emoji\"[^>]*>(.*?)</i>", r"\1", fragment, flags=re.S)
    text = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(text).strip()


def parse(page):
    posts = []
    for block in re.split(r'<div class="tgme_widget_message_wrap', page)[1:]:
        m_id = re.search(r'data-post="[^"/]+/(\d+)"', block)
        if not m_id or "tgme_widget_message_service" in block[:600]:
            continue  # service messages (photo changed, pinned, ...) are not posts
        m_text = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>\s*(?:<div class="tgme_widget_message_(?:footer|reply_markup|link_preview)|</div>)', block, re.S)
        m_date = re.search(r'<time[^>]+datetime="([^"]+)"', block)
        m_views = re.search(r'<span class="tgme_widget_message_views">([^<]+)</span>', block)
        media = bool(re.search(r"tgme_widget_message_(photo|video|document|roundvideo|poll)", block))
        posts.append({"id": int(m_id.group(1)), "date": m_date.group(1) if m_date else None,
                      "views": m_views.group(1).strip() if m_views else None,
                      "text": strip(m_text.group(1)) if m_text else "", "media": media})
    return posts


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("channel")
    ap.add_argument("--posts", type=int, default=40)
    a = ap.parse_args()
    name = re.sub(r"^(https?://)?(t\.me|telegram\.me)/(s/)?", "", a.channel.strip()).strip("/@ ").split("/")[0]
    if not re.fullmatch(r"[A-Za-z0-9_]{4,64}", name):
        print(json.dumps({"ok": False, "channel": a.channel, "problem": "bad_name",
                          "hint": "Give a public channel name or a t.me link"}, ensure_ascii=False))
        return 2
    want = max(1, min(a.posts, MAX_POSTS))
    url = "https://t.me/s/" + name
    status, page = get(url)
    if status != 200 or "tgme_channel_info" not in page:
        print(json.dumps({"ok": False, "channel": name, "url": url, "status": status, "problem": "not_public",
                          "hint": "This channel has no public web preview (private, a group, a bot or a person), "
                                  "or the address is wrong. Ask the user for screenshots instead."}, ensure_ascii=False))
        return 1
    title = re.search(r'<div class="tgme_channel_info_header_title"[^>]*>(.*?)</div>', page, re.S)
    desc = re.search(r'<div class="tgme_channel_info_description"[^>]*>(.*?)</div>', page, re.S)
    subs = re.search(r'<span class="counter_value">([^<]+)</span>\s*<span class="counter_type">(subscribers|подписчик\w*)</span>', page)
    posts = {p["id"]: p for p in parse(page)}
    pages = 1
    while len(posts) < want and pages < 8:
        before = min(posts) if posts else None
        if not before or before <= 1:
            break
        time.sleep(1.5)  # be polite to the public preview
        status, more = get("%s?before=%d" % (url, before))
        new = parse(more) if status == 200 else []
        if not new:
            break
        for p in new:
            posts.setdefault(p["id"], p)
        pages += 1
    items = sorted(posts.values(), key=lambda p: p["id"], reverse=True)[:want]
    for p in items:
        p["link"] = "https://t.me/%s/%d" % (name, p["id"])
    dates = [p["date"] for p in items if p["date"]]
    print(json.dumps({"ok": True, "channel": name, "url": url,
                      "title": strip(title.group(1)) if title else "", "description": strip(desc.group(1)) if desc else "",
                      "subscribers": subs.group(1) if subs else None, "posts_read": len(items),
                      "period": {"from": min(dates) if dates else None, "to": max(dates) if dates else None},
                      "posts": items, "problem": None, "hint": None}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
