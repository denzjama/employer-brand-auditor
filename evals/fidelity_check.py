#!/usr/bin/env python3
"""Quotation-fidelity triage for eval outputs. Python standard library only.

For every response in a results directory, extracts each quoted string (straight, curly or
single quotes) of two or more words and checks it against the exact material
that session received (the record's message_sent; for follow-up cases, also the
prerequisite turn). Each quote is classified:

  VERBATIM          exact substring of the source (whitespace / quote-style normalised)
  MARKED-CUT        every segment between "…" / "..." / "[…]" is a verbatim substring, in
                    source order, within one sentence (printed: the cut may remove a condition)
  MARKED-CUT-MERGED segments are verbatim and in order but come from different sentences
                    (possible merged fragments)
  REORDERED         segments are verbatim but appear in a different order from the source
  UNMARKED-CUT      all words occur in the source in order, but not contiguously and
                    without an ellipsis (silent shortening or merged fragments)
  TRUNCATED-END     verbatim, at least 5 words, but cut mid-sentence without an ellipsis
                    where the source continues with a further clause (possible removal of
                    a qualifying or scope clause)
  TRUNCATED-START   verbatim, at least 5 words, but a leading clause of the same sentence
                    (ending in a comma) was dropped without an ellipsis (possible removal of
                    a scope or time qualifier such as "In the X depot,")
  NOT-IN-SOURCE     not found; either the auditor's own wording in quotation marks
                    (examples, suggested copy, lexicon phrases) or an invented attribution

VERBATIM quotes are not printed; every other label is. This is a triage tool: every flag must
be reviewed by a person, because quoting the auditor's own suggested copy or a lexicon
phrase is legitimate, while attributing it to the material is not.

Usage:
    python3 evals/fidelity_check.py <run-dir> [<run-dir> ...] [--json out.json]
"""

import argparse
import glob
import json
import os
import re

QUOTE_RE = re.compile(r'"([^"\n]{12,}?)"|“([^”\n]{12,}?)”|«([^»\n]{12,}?)»|‘([^’\n]{8,}?)’|(?<![\w])\'([^\'\n]{8,}?)\'(?![\w])')
ELLIPSIS_RE = re.compile(r"\s*(?:\[…\]|\[\.\.\.\]|…|\.\.\.)\s*")


def norm(text):
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("\\\"", '"')
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def words(text):
    return re.findall(r"[\w£%'-]+", text.lower())


def in_order(qwords, swords):
    """True if qwords appear in swords in order (allowing gaps)."""
    i = 0
    for w in swords:
        if i < len(qwords) and w == qwords[i]:
            i += 1
    return i == len(qwords)


def classify(quote, source_norm, source_words):
    q = norm(quote).strip(" .,;:")
    if len(words(q)) < 2:
        return None
    if q in source_norm:
        if len(words(q)) >= 5:
            pos = source_norm.find(q) + len(q)
            tail = source_norm[pos:pos + 40].lstrip()
            if tail and tail[0] not in '.!?"\n' and re.match(r"(?:[,;-]\s*)?(and|but|though|although|except|or|which|while|unless|with|for|on|in|across|once|if|after|only|subject|provided|when|until|before|at|from)\b", tail):
                return "TRUNCATED-END"
            start = source_norm.find(q)
            head = re.split(r"[.!?]['\"]?\s|['\"]", source_norm[max(0, start - 80):start])[-1]
            if head.strip() and head.rstrip().endswith(","):
                return "TRUNCATED-START"
        return "VERBATIM"
    parts = [p.strip(" .,;:") for p in ELLIPSIS_RE.split(q) if p.strip(" .,;:")]
    if len(parts) > 1 and all(p in source_norm for p in parts):
        positions, cursor, ordered = [], 0, True
        for p in parts:
            pos = source_norm.find(p, cursor)
            if pos == -1:
                ordered = False
                break
            positions.append((pos, pos + len(p)))
            cursor = pos + len(p)
        if not ordered:
            return "REORDERED"
        for (s1, e1), (s2, e2) in zip(positions, positions[1:]):
            if re.search(r"[.!?]['\"]?\s", source_norm[e1:s2]):
                return "MARKED-CUT-MERGED"
        return "MARKED-CUT"
    qw = words(q)
    if len(qw) >= 3 and in_order(qw, source_words):
        return "UNMARKED-CUT"
    return "NOT-IN-SOURCE"


def source_for(record, run_dir):
    src = record.get("message_sent") or ""
    pre = record.get("depends_on")
    if pre:
        path = os.path.join(run_dir, pre + ".record.json")
        if os.path.exists(path):
            prev = json.load(open(path, encoding="utf-8"))
            src = (prev.get("message_sent") or "") + "\n" + src
    return src


def scan(run_dir):
    findings = []
    for path in sorted(glob.glob(os.path.join(run_dir, "*.record.json"))):
        record = json.load(open(path, encoding="utf-8"))
        key = os.path.basename(path)[: -len(".record.json")]
        text = record.get("result_text") or ""
        source = source_for(record, run_dir)
        s_norm, s_words = norm(source), words(norm(source))
        for line_no, line in enumerate(text.splitlines(), 1):
            for m in QUOTE_RE.finditer(line):
                quote = next(g for g in m.groups() if g)
                label = classify(quote, s_norm, s_words)
                if label and label != "VERBATIM":
                    findings.append({"run": key, "line": line_no, "label": label, "quote": quote[:200],
                                     "context": line.strip()[:260]})
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dirs", nargs="+")
    parser.add_argument("--json", default=None)
    opts = parser.parse_args()
    all_findings = []
    for d in opts.run_dirs:
        found = scan(d)
        all_findings.extend(dict(f, dir=d) for f in found)
        for f in found:
            print("{run}:{line} [{label}] \"{quote}\"".format(**f))
    if opts.json:
        with open(opts.json, "x", encoding="utf-8") as handle:
            json.dump(all_findings, handle, indent=2, ensure_ascii=False)
    print("\n{} flagged quotations (all non-VERBATIM labels) — review each manually.".format(len(all_findings)))


if __name__ == "__main__":
    main()
