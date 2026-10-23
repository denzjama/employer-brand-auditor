#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List the latest videos of a public YouTube channel from its public RSS feed (no login, no key).

Used in deep collection (methodology/source-collection.md §5). Standard library only. The feed
holds the channel's latest 15 uploads: titles, dates, descriptions and view counts. Videos
themselves are not watched or transcribed.

    python3 youtube_channel.py <channel link: /@handle, /channel/UC..., /c/name or /user/name>

Output JSON: ok, channel_id, url, title, videos_read, period {from, to},
videos: [{title, date, link, short, views, description}], problem, hint.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_page import USER_AGENT, ssl_context  # noqa: E402

NS = {"a": "http://www.w3.org/2005/Atom", "media": "http://search.yahoo.com/mrss/",
      "yt": "http://www.youtube.com/xml/schemas/2015"}


def get(url):
    ctx, _ = ssl_context(None)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.ProxyHandler())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en,ru;q=0.8",
                                               "Cookie": "CONSENT=PENDING+999"})
    try:
        r = opener.open(req, timeout=25)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001
        return None, str(e).encode()


def fail(url, problem, hint):
    print(json.dumps({"ok": False, "url": url, "problem": problem, "hint": hint}, ensure_ascii=False))
    return 1


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    url = sys.argv[1].strip()
    if not re.match(r"^https?://(www\.|m\.)?youtube\.com/", url, re.I):
        return fail(url, "bad_link", "Give a youtube.com channel link")
    m = re.search(r"/channel/(UC[\w-]{20,})", url)
    channel_id = m.group(1) if m else None
    page_desc, page_handle = "", None
    if not channel_id:
        status, page = get(url)
        text = page.decode("utf-8", errors="replace")
        handle = re.search(r"/(@[\w.-]+)", url)
        if handle and not re.search(r'"(canonicalBaseUrl|vanityChannelUrl)":"[^"]*/' + re.escape(handle.group(1)) + '"', text, re.I):
            return fail(url, "not_found", "No channel with the handle %s was found; the page did not belong to it. "
                                          "Do not use any other channel in its place." % handle.group(1))
        m = (re.search(r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{20,})"', text)
             or re.search(r'"externalId":"(UC[\w-]{20,})"', text))
        if not m:
            return fail(url, "no_channel_id", "The channel page did not reveal its ID (status %s). "
                                              "Ask the user for the /channel/UC... link." % status)
        channel_id = m.group(1)
        d = re.search(r'<meta property="og:description" content="([^"]*)"', text)
        page_desc = __import__("html").unescape(d.group(1)) if d else ""
        h = re.search(r'"canonicalBaseUrl":"/(@[^"]+)"', text)
        page_handle = h.group(1) if h else None
    feed = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
    status, body = get(feed)
    if status != 200 or b"<!doctype" in body[:200].lower() or b"<!entity" in body.lower():
        return fail(url, "feed_unavailable", "The public feed did not answer (status %s)." % status)
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return fail(url, "feed_unavailable", "The feed could not be read.")
    videos = []
    for e in root.findall("a:entry", NS):
        link = e.find("a:link", NS).get("href") if e.find("a:link", NS) is not None else ""
        stats = e.find("media:group/media:community/media:statistics", NS)
        desc = e.find("media:group/media:description", NS)
        videos.append({"title": (e.findtext("a:title", "", NS) or "").strip(),
                       "date": e.findtext("a:published", "", NS),
                       "link": link, "short": "/shorts/" in link,
                       "views": stats.get("views") if stats is not None else None,
                       "description": (desc.text or "").strip()[:1500] if desc is not None else ""})
    dates = [v["date"] for v in videos if v["date"]]
    print(json.dumps({"ok": True, "channel_id": channel_id, "url": "https://www.youtube.com/channel/" + channel_id,
                      "title": root.findtext("a:title", "", NS), "handle": page_handle, "channel_description": page_desc[:1000],
                      "videos_read": len(videos),
                      "period": {"from": min(dates) if dates else None, "to": max(dates) if dates else None},
                      "videos": videos, "problem": None,
                      "hint": "The public feed holds only the latest 15 uploads. Check that the title and description "
                              "belong to the employer before using this channel."}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
