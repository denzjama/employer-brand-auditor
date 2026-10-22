#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch one public web page and return its visible text verbatim, as JSON.

Used by the employer-brand-audit skill to collect an employer's public candidate-facing pages
(methodology/source-collection.md). Standard library only.

    python3 fetch_page.py <url> [--ca-bundle PATH] [--timeout SECONDS]

Network behaviour:
- Uses this computer's own connection; honours HTTPS_PROXY / HTTP_PROXY if they are set.
- Certificates are always verified. Extra root certificates (for example the Russian Trusted
  Root CA used by some Russian sites) are trusted only if a PEM file is supplied with
  --ca-bundle, in EBA_EXTRA_CA, or at ~/.eb-auditor/extra-ca.pem. Nothing system-wide changes.

Output fields: ok, url, final_url, status, title, description, text, chars, problem, hint.
problem is one of: null, "geoblocked", "blocked", "certificate", "script_shell", "not_found",
"http_error", "network", "not_html".
"""
import argparse
import gzip
import html
import json
import os
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request
import zlib
from html.parser import HTMLParser

USER_AGENT = ("Mozilla/5.0 (compatible; EmployerBrandAuditor/0.3; "
              "+https://github.com/denzjama/employer-brand-auditor)")
DEFAULT_CA = os.path.expanduser("~/.eb-auditor/extra-ca.pem")
SKIP = {"script", "style", "noscript", "svg", "template", "iframe", "canvas"}
BLOCK = {"p", "div", "section", "article", "main", "header", "footer", "li", "ul", "ol", "tr",
         "table", "h1", "h2", "h3", "h4", "h5", "h6", "br", "blockquote", "dd", "dt", "figcaption"}
STUB_PATTERNS = re.compile(
    r"(VPN|впн|доступ (?:к сайту )?ограничен|access (?:is )?denied|not available in your (?:country|region)|"
    r"недоступ\w* в вашем регионе|unavailable for legal reasons|проверка браузера|are you a robot|captcha)",
    re.I)
MAX_CHARS = 60000


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.title, self.in_title, self.description = [], 0, "", False, ""
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
            if tag == "script":
                self.scripts += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            a = dict(attrs)
            if (a.get("name") or a.get("property") or "").lower() in ("description", "og:description") and not self.description:
                self.description = (a.get("content") or "").strip()
        if tag in BLOCK:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
            return
        if not self.skip:
            self.parts.append(data)

    def text(self):
        raw = "".join(self.parts)
        lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in raw.split("\n")]
        out, blank = [], False
        for ln in lines:
            if ln in ("", "-"):
                if not blank and out:
                    out.append("")
                blank = True
            else:
                out.append(ln)
                blank = False
        return "\n".join(out).strip()


def ssl_context(ca_bundle):
    ctx = ssl.create_default_context()
    extra = ca_bundle or os.environ.get("EBA_EXTRA_CA") or (DEFAULT_CA if os.path.exists(DEFAULT_CA) else None)
    if extra:
        ctx.load_verify_locations(cafile=os.path.expanduser(extra))
    try:  # macOS python.org builds may lack system roots; fall back to certifi only if it is installed
        if not ctx.get_ca_certs():
            import certifi  # noqa: F401
            ctx.load_verify_locations(cafile=certifi.where())
    except Exception:
        pass
    return ctx, extra


def decode(body, headers):
    enc = (headers.get("Content-Encoding") or "").lower()
    if enc == "gzip":
        body = gzip.decompress(body)
    elif enc == "deflate":
        body = zlib.decompress(body)
    m = re.search(r"charset=([\w-]+)", headers.get("Content-Type") or "", re.I)
    charset = m.group(1) if m else None
    if not charset:
        m = re.search(rb'<meta[^>]+charset=["\']?([\w-]+)', body[:4000], re.I)
        charset = m.group(1).decode() if m else "utf-8"
    return body.decode(charset, errors="replace")


def result(url, **kw):
    base = {"ok": False, "url": url, "final_url": None, "status": None, "title": "", "description": "",
            "text": "", "chars": 0, "problem": None, "hint": None}
    base.update(kw)
    return base


def fetch(url, ca_bundle=None, timeout=25):
    ctx, extra = ssl_context(ca_bundle)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml",
                                               "Accept-Language": "ru,en;q=0.8", "Accept-Encoding": "gzip, deflate"})
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.ProxyHandler())
    try:
        resp = opener.open(req, timeout=timeout)
        status, final_url, headers, body = resp.status, resp.geturl(), resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        status, final_url, headers, body = e.code, e.geturl(), e.headers, e.read() or b""
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(reason):
            return result(url, problem="certificate", hint=(
                "The site's certificate is not trusted on this computer. Russian sites often use the Russian "
                "Trusted Root CA. Save that root certificate as a PEM file at ~/.eb-auditor/extra-ca.pem (or pass "
                "--ca-bundle) to trust it for these fetches only." + (" An extra CA file was used: " + extra if extra else "")))
        return result(url, problem="network", hint="Network error: %s" % reason)
    except (socket.timeout, TimeoutError):
        return result(url, problem="network", hint="Timed out")

    try:
        text_html = decode(body, headers)
    except Exception:
        text_html = ""
    ctype = (headers.get("Content-Type") or "").lower()
    if text_html and "html" not in ctype and not text_html.lstrip().startswith("<"):
        return result(url, final_url=final_url, status=status, problem="not_html", hint="Content-Type: " + ctype)

    p = TextExtractor()
    try:
        p.feed(text_html)
    except Exception:
        pass
    text = p.text()
    title = html.unescape(p.title.strip())
    common = dict(final_url=final_url, status=status, title=title, description=p.description,
                  text=text[:MAX_CHARS], chars=len(text))

    if status == 451:
        return result(url, problem="geoblocked", hint=(
            "HTTP 451: the site refuses requests from this network, usually because the connection goes through "
            "a VPN or a foreign address. Turn the VPN off for this site, exclude its domain from the VPN, or set "
            "HTTPS_PROXY to a proxy in the site's country."), **common)
    if re.search(r"captcha|challenge|/checkcaptcha|showcaptcha", final_url or "", re.I):
        return result(url, problem="blocked", hint=(
            "The site answered with a captcha or bot check. Do not try to pass it. Wait a few minutes before the "
            "next request to this site, fetch fewer pages from it, or ask the user for the page text."), **common)
    if status == 404:
        return result(url, problem="not_found", **common)
    if status in (401, 403, 429) or (len(text) < 1500 and STUB_PATTERNS.search(text + " " + title)):
        return result(url, problem="blocked", hint=(
            "The site returned a block or check page instead of content (HTTP %s). If it mentions a VPN or region, "
            "change the network as for HTTP 451. Do not try to get around bot checks." % status), **common)
    if status >= 400:
        return result(url, problem="http_error", hint="HTTP %s" % status, **common)
    if len(text) < 400 and p.scripts >= 3:
        return result(url, problem="script_shell", hint=(
            "The page is built by scripts in the browser; the raw page has almost no text. Look for the same "
            "content on other pages (sections, vacancies, blog) or ask the user for the text."), **common)
    return result(url, ok=True, **common)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url")
    ap.add_argument("--ca-bundle")
    ap.add_argument("--timeout", type=int, default=25)
    a = ap.parse_args()
    if not re.match(r"^https?://", a.url, re.I):
        print(json.dumps(result(a.url, problem="http_error", hint="Only http(s) addresses are fetched"), ensure_ascii=False))
        return 2
    out = fetch(a.url, a.ca_bundle, a.timeout)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
