#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read recent posts from the wall of a public VK community through the official VK API.

VK does not show community walls to anonymous visitors, so this needs a VK *service token*
that the user creates for their own VK app (vk.com/apps?act=manage -> create app -> service
token). Put it in the VK_SERVICE_TOKEN environment variable or in ~/.eb-auditor/vk-token.
The token only reads public data. Used in deep collection (methodology/source-collection.md §5).

    python3 vk_wall.py <vk.com link or community short name> [--posts 40]

Output JSON: ok, community, url, name, members, posts_read, period {from, to},
posts: [{id, date, text, likes, reposts, views, attachments, link}], problem, hint.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_page import USER_AGENT, ssl_context  # noqa: E402

API = "https://api.vk.com/method/"
VERSION = "5.199"
TOKEN_FILE = os.path.expanduser("~/.eb-auditor/vk-token")


def token():
    t = os.environ.get("VK_SERVICE_TOKEN")
    if not t and os.path.exists(TOKEN_FILE):
        t = open(TOKEN_FILE, encoding="utf-8").read().strip()
    return t


def call(method, **params):
    params.update({"access_token": token(), "v": VERSION})
    ctx, _ = ssl_context(None)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.ProxyHandler())
    req = urllib.request.Request(API + method, data=urllib.parse.urlencode(params).encode(),
                                 headers={"User-Agent": USER_AGENT})
    try:
        return json.loads(opener.open(req, timeout=25).read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": {"error_msg": "HTTP %s" % e.code}}
    except Exception as e:  # noqa: BLE001
        return {"error": {"error_msg": str(e)}}


def out(obj, code):
    print(json.dumps(obj, ensure_ascii=False, indent=1))
    return code


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("community")
    ap.add_argument("--posts", type=int, default=40)
    a = ap.parse_args()
    name = re.sub(r"^(https?://)?(m\.)?vk\.(com|ru)/", "", a.community.strip()).strip("/@ ").split("?")[0]
    if not re.fullmatch(r"[A-Za-z0-9_.]{2,64}", name):
        return out({"ok": False, "community": a.community, "problem": "bad_name", "hint": "Give a vk.com link"}, 2)
    if not token():
        return out({"ok": False, "community": name, "url": "https://vk.com/" + name, "problem": "no_token",
                    "hint": "VK shows community walls only through its API. Create a VK app at vk.com/apps?act=manage, "
                            "copy its service token, and save it in ~/.eb-auditor/vk-token or VK_SERVICE_TOKEN. "
                            "Until then, list this community as not reviewed or ask for screenshots."}, 1)
    info = call("groups.getById", group_id=name, fields="members_count,description")
    if "error" in info:
        return out({"ok": False, "community": name, "problem": "api_error", "hint": info["error"].get("error_msg")}, 1)
    groups = info.get("response", {})
    groups = groups.get("groups", groups) if isinstance(groups, dict) else groups
    g = groups[0] if groups else {}
    wall = call("wall.get", domain=name, count=max(1, min(a.posts, 100)), filter="owner")
    if "error" in wall:
        return out({"ok": False, "community": name, "problem": "api_error", "hint": wall["error"].get("error_msg")}, 1)
    posts = []
    for p in wall.get("response", {}).get("items", []):
        posts.append({"id": p.get("id"),
                      "date": datetime.datetime.utcfromtimestamp(p.get("date", 0)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "text": p.get("text", ""), "likes": (p.get("likes") or {}).get("count"),
                      "reposts": (p.get("reposts") or {}).get("count"), "views": (p.get("views") or {}).get("count"),
                      "attachments": [x.get("type") for x in p.get("attachments", [])],
                      "pinned": bool(p.get("is_pinned")),
                      "link": "https://vk.com/wall%s_%s" % (p.get("owner_id"), p.get("id"))})
    dates = [p["date"] for p in posts]
    return out({"ok": True, "community": name, "url": "https://vk.com/" + name, "name": g.get("name"),
                "members": g.get("members_count"), "description": g.get("description", "")[:2000],
                "posts_read": len(posts), "period": {"from": min(dates) if dates else None, "to": max(dates) if dates else None},
                "posts": posts, "problem": None, "hint": None}, 0)


if __name__ == "__main__":
    sys.exit(main())
