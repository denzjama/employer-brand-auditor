#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Map an employer's careers site: list candidate-facing pages from robots.txt, sitemaps and links.

Used in deep collection (methodology/source-collection.md §4). Standard library only.

    python3 discover_site.py <careers-or-company-url> [--max-pages 400] [--crawl 15]

What it does:
1. Reads robots.txt for the host and respects its Disallow rules for this tool and for "*".
2. Reads the sitemaps listed in robots.txt (and /sitemap.xml), following sitemap indexes,
   and keeps URLs that look candidate-facing (careers, jobs, vacancies, teams, culture, benefits,
   life, blog, stories, students, internships, hiring process; Russian equivalents too).
3. If sitemaps give few results, follows links from the start page and up to --crawl pages of
   the same host whose path looks candidate-facing.

Output JSON: start_url, host, robots, sitemaps_read, urls: [{url, kind, source}], counts by kind,
notes. kind is a guess from the address (careers, vacancy, vacancy_list, team, culture, benefits,
story, process, students, other) and must be checked when the page is read.
"""
import argparse
import gzip
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_page import USER_AGENT, ssl_context  # noqa: E402

import urllib.error  # noqa: E402
import urllib.request  # noqa: E402


def site_of(netloc):
    """Registrable part of a host name, approximately: example.co.uk, lidl.de, yandex.ru."""
    labels = netloc.split(":")[0].lower().split(".")
    if len(labels) >= 3 and labels[-2] in ("co", "com", "org", "net", "gov", "ac", "edu") and len(labels[-1]) == 2:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])

KIND_PATTERNS = [
    ("vacancy", r"/(vacancies|vacancy|ваканси[яи]|vakansii|vakansiya)/[^/?#]+|/jobs?/(view|details|\d)[^/?#]*|/(job|position|opening)/[^/?#]+|/(jobs?|stellen\w*|career\w*|karriere)/[^/?#]*\d{4,}[^/?#]*/?$|[?&](job|jobid|vacancy|id)=\d+"),
    ("vacancy_list", r"/(vacancies|jobs|openings|positions|ваканси[ия]|vakansii)/?($|\?)|/search"),
    ("process", r"(interview|hiring|how-we-hire|recruit|selection|process|faq|собеседован|how-to-get|naym|найм)"),
    ("benefits", r"(benefit|perk|compensat|bonus|льгот|бенефит|соцпакет)"),
    ("culture", r"(culture|values|life|atmosphere|about|why|mission|ценност|культур|атмосфер|почему)"),
    ("story", r"(blog|stories|story|people|employee|interview-with|истори|блог|сотрудник)"),
    ("students", r"(student|intern|graduate|campus|junior|стаж|студент|выпускник|school)"),
    ("team", r"(team|teams|department|direction|services|professions|команд|направлен|професс)"),
    ("careers", r"(career|careers|jobs|work-with-us|join|карьер|работа|rabota)"),
]
CANDIDATE_RE = re.compile("|".join(p for _, p in KIND_PATTERNS), re.I)


TRACKING = re.compile(r"^(from|utm_\w+|ref|source|src|gclid|yclid|fbclid|_openstat|lang)$", re.I)


def normalize(url):
    """Drop fragments, tracking parameters and trailing slashes so one page is listed once."""
    s = urllib.parse.urlsplit(url)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(s.query, keep_blank_values=True) if not TRACKING.match(k)]
    path = s.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((s.scheme, s.netloc, path, urllib.parse.urlencode(q), ""))


def kind_of(url):
    s = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(s.path + ("?" + s.query if s.query else "")).lower()
    for kind, pat in KIND_PATTERNS:
        if re.search(pat, path, re.I):
            return kind
    return "other"


def get(url, timeout=20):
    ctx, _ = ssl_context(None)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.ProxyHandler())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    try:
        r = opener.open(req, timeout=timeout)
        body = r.read()
        if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
            try:
                body = gzip.decompress(body)
            except OSError:
                pass
        return r.status, r.geturl(), body
    except urllib.error.HTTPError as e:
        return e.code, url, b""
    except ValueError as e:
        return None, url, str(e).encode()
    except Exception as e:  # noqa: BLE001 - report every other network problem the same way
        return None, url, str(e).encode()


def sitemap_urls(sm_url, budget, read, notes, depth=0):
    if depth > 3 or len(read) > 25:
        return []
    status, _, body = get(sm_url)
    read.append({"url": sm_url, "status": status})
    if status != 200:
        return []
    root = safe_xml(body)
    if root is None:
        notes.append("sitemap skipped (not parseable or unsafe): " + sm_url)
        return []
    ns = re.match(r"\{.*\}", root.tag)
    ns = ns.group(0) if ns else ""
    out = []
    if root.tag.endswith("sitemapindex"):
        children = [urllib.parse.urljoin(sm_url, e.text.strip()) for e in root.iter(ns + "loc") if e.text]
        # careers-looking child sitemaps first
        children.sort(key=lambda u: 0 if CANDIDATE_RE.search(u) else 1)
        for child in children:
            if len(out) >= budget:
                break
            out += sitemap_urls(child, budget - len(out), read, notes, depth + 1)
        return out
    for e in root.iter(ns + "loc"):
        if e.text and len(out) < budget:
            out.append(urllib.parse.urljoin(sm_url, e.text.strip()))
    return out


class Robots:
    """robots.txt rules with * and $ wildcards, longest match wins, ties go to Allow (Google's spec)."""

    def __init__(self, text, agent="employerbrandauditor"):
        groups, cur, agents, last_was_agent = [], None, [], False
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            key, val = [x.strip() for x in line.split(":", 1)]
            key = key.lower()
            if key == "user-agent":
                if not last_was_agent:
                    agents = []
                    cur = {"agents": agents, "rules": []}
                    groups.append(cur)
                agents.append(val.lower())
                last_was_agent = True
            elif key in ("allow", "disallow") and cur is not None:
                cur["rules"].append((key == "allow", val))
                last_was_agent = False
            else:
                last_was_agent = False
        mine = [g for g in groups if any(a != "*" and a in agent for a in g["agents"])]
        star = [g for g in groups if "*" in g["agents"]]
        chosen = mine or star
        self.rules = [r for g in chosen for r in g["rules"] if r[1] != "" or r[0]]

    @staticmethod
    def _match(pattern, path):
        regex = re.escape(pattern).replace(r"\*", ".*")
        if regex.endswith(r"\$"):
            regex = regex[:-2] + "$"
        return re.match(regex, path) is not None

    def allowed(self, url):
        s = urllib.parse.urlsplit(url)
        path = (s.path or "/") + ("?" + s.query if s.query else "")
        best = None
        for allow, pattern in self.rules:
            if pattern and self._match(pattern, path):
                if best is None or len(pattern) > len(best[1]) or (len(pattern) == len(best[1]) and allow):
                    best = (allow, pattern)
        return True if best is None else best[0]


def safe_xml(body):
    """Refuse documents with a DTD or entities (entity-expansion attacks) and very large files."""
    if len(body) > 30 * 1024 * 1024:
        return None
    head = body[:2000].lower()
    if b"<!doctype" in head or b"<!entity" in body.lower():
        return None
    try:
        return ET.fromstring(body)
    except ET.ParseError:
        return None


SOCIAL = [
    ("telegram", r"^https?://(t\.me|telegram\.me)/(s/)?([A-Za-z0-9_]{4,})/?$"),
    ("vk", r"^https?://(m\.)?vk\.(com|ru)/([A-Za-z0-9_.]+)/?$"),
    ("youtube", r"^https?://(www\.|m\.)?youtube\.com/(@[\w.-]+|c/[\w.-]+|channel/[\w-]+|user/[\w.-]+)/?"),
    ("linkedin", r"^https?://([a-z]{2,3}\.)?linkedin\.com/(company|school|showcase)/[\w.%-]+/?"),
    ("instagram", r"^https?://(www\.)?instagram\.com/([\w.]+)/?$"),
    ("facebook", r"^https?://(www\.|m\.)?facebook\.com/([\w.-]+)/?$"),
    ("tiktok", r"^https?://(www\.)?tiktok\.com/@[\w.]+/?$"),
    ("x", r"^https?://(www\.)?(twitter|x)\.com/([A-Za-z0-9_]+)/?$"),
    ("ok", r"^https?://(www\.)?ok\.ru/([\w.]+)/?$"),
    ("dzen", r"^https?://(www\.)?dzen\.ru/([\w.-]+)/?$"),
    ("habr", r"^https?://(career\.)?habr\.com/(ru/)?(companies|company)/[\w-]+/?"),
    ("hh", r"^https?://([a-z]+\.)?hh\.(ru|kz|by)/employer/\d+/?$"),
    ("glassdoor", r"^https?://(www\.)?glassdoor\.[a-z.]+/(Overview|Reviews|Jobs)/[^?#]+"),
    ("indeed", r"^https?://([a-z]+\.)?indeed\.com/cmp/[\w-]+"),
]


def social_kind(url):
    for kind, pat in SOCIAL:
        if re.match(pat, url, re.I):
            return kind
    return None


class LinkParser(__import__("html.parser").parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def page_links(url):
    status, final, body = get(url)
    if status != 200:
        return final, []
    p = LinkParser()
    try:
        p.feed(body.decode("utf-8", errors="replace"))
    except Exception:  # noqa: BLE001
        pass
    return final, [urllib.parse.urljoin(final, h).split("#")[0] for h in p.links]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url")
    ap.add_argument("--max-pages", type=int, default=800)
    ap.add_argument("--crawl", type=int, default=15)
    ap.add_argument("--max-vacancies", type=int, default=60)
    a = ap.parse_args()
    if not re.match(r"^https?://", a.url, re.I):
        print(json.dumps({"error": "Only http(s) addresses are accepted"}))
        return 2
    parts = urllib.parse.urlsplit(a.url)
    host = parts.netloc
    base = "%s://%s" % (parts.scheme, host)
    notes, read = [], []

    status, _, body = get(base + "/robots.txt")
    robots_ok = status == 200
    robots = Robots(body.decode("utf-8", errors="replace") if robots_ok else "")
    if not robots_ok:
        notes.append("robots.txt not readable (status %s); no rules applied" % status)
    listed = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", body.decode("utf-8", errors="replace")) if robots_ok else []
    start_path = parts.path.rstrip("/")
    # 1) the careers section's own sitemap, 2) listed sitemaps that look careers-related, 3) the root sitemap
    sitemaps = []
    if start_path:
        sitemaps.append(base + start_path + "/sitemap.xml")
    sitemaps += [s for s in listed if (start_path and start_path in s) or (not start_path and CANDIDATE_RE.search(s))]
    if not sitemaps:
        sitemaps = listed[:2] or [base + "/sitemap.xml"]

    def allowed(u):
        return robots.allowed(u)

    def in_scope(u):
        us = urllib.parse.urlsplit(u)
        same_site = site_of(us.netloc) == site_of(host)
        if not same_site:
            return False
        if start_path:
            if us.netloc == host:
                return urllib.parse.unquote(us.path).startswith(start_path)
            return bool(re.match(r"(careers?|jobs|rabota|hr|team)\.", us.netloc))
        return bool(CANDIDATE_RE.search(urllib.parse.unquote(u)))

    found, vacancy_pool, vacancy_cap = {}, [], a.max_vacancies
    for sm in sitemaps[:6]:
        for u in sitemap_urls(sm, 50000, read, notes):
            u = normalize(u)
            if not (in_scope(u) and allowed(u)) or u in found or re.search(r"/(404|500|error)(/|$)", u):
                continue
            if kind_of(u) == "vacancy":
                vacancy_pool.append(u)
                continue
            found[u] = "sitemap"
    vacancies_total = len(set(vacancy_pool))
    pool = sorted(set(vacancy_pool))
    if pool:  # an even spread across the whole list, so the sample covers different roles and places
        step = max(1, len(pool) // vacancy_cap)
        for u in pool[::step][:vacancy_cap]:
            found[u] = "sitemap (sample)"

    # Link crawl from the start page and candidate-looking pages on the same host
    socials = {}
    queue, seen, crawled = [a.url], set(), 0
    while queue and crawled < a.crawl:
        u = queue.pop(0)
        if u in seen or not allowed(u):
            continue
        seen.add(u)
        final, links = page_links(u)
        crawled += 1
        for raw in links:
            sk = social_kind(raw.split("?")[0])
            if sk:
                key = raw.split("?")[0].rstrip("/")
                socials.setdefault(key, {"platform": sk, "url": key, "found_on": final})
            l = normalize(raw)
            ls = urllib.parse.urlsplit(l)
            if ls.scheme not in ("http", "https") or ls.netloc != urllib.parse.urlsplit(final).netloc:
                continue
            if in_scope(l) and allowed(l):
                if l not in found and (kind_of(l) != "vacancy" or sum(1 for v in found if kind_of(v) == "vacancy") < vacancy_cap):
                    found[l] = "link"
                if l not in seen and len(queue) < 200 and kind_of(l) not in ("vacancy",):
                    queue.append(l)

    urls = [{"url": u, "kind": kind_of(u), "source": s} for u, s in found.items()]
    order = ["careers", "culture", "benefits", "process", "team", "story", "students", "vacancy_list", "vacancy", "other"]
    urls.sort(key=lambda x: (order.index(x["kind"]), len(x["url"])))
    counts = {}
    for x in urls:
        counts[x["kind"]] = counts.get(x["kind"], 0) + 1
    print(json.dumps({"start_url": a.url, "host": host, "robots": "read" if robots_ok else "not readable",
                      "sitemaps_read": [r for r in read][:30], "pages_crawled": crawled, "counts": counts,
                      "vacancies_in_sitemaps": vacancies_total,
                      "social_accounts": list(socials.values()),
                      "urls": urls[:a.max_pages], "notes": notes}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
