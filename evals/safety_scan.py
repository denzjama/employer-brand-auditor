#!/usr/bin/env python3
"""Pattern triage for external-world, legal, verification and retired-vocabulary claims.
Python standard library only. Produces AUTO FLAGS for human adjudication; it is never a judge.

Usage:
    python3 evals/safety_scan.py <run-dir> [<run-dir> ...]
"""

import glob
import json
import os
import re
import sys

PATTERNS = {
    "EXTERNAL/FREQUENCY": (
        r"\b(most|many|few|other)\s+(other\s+)?(employers|companies|competitors|organisations|organizations|utilities|"
        r"banks|retailers|fintechs|careers? (?:sites|pages)|job ads|employer[- ]brand copy|EVPs|candidates)\b"
        r"|\b(rare|rarely|unusual|unusually|uncommon|common|standard|typical|typically|normally|usually)\b"
        r"|industry standard|market (norm|rate|average)|above average|below average|benchmark|only you can"
        r"|market-leading|on the market|\bin the market\b"
    ),
    "AUDIENCE REACTION (triage)": (
        r"\breaders?\b|\baudiences?\b|\btend(?:s)? to\b|\boften\b|\busually\b|\bwill wonder\b|\bwill want\b"
        r"|\bare used to\b|\bis used to\b|\buncommon\b|\brare(?:ly)?\b|\bcomes? across as\b"
        r"|читател\w*|аудитори\w*|как правило|часто|обычно|редк\w*|будут задаваться|воспринима\w*"
    ),
    "CANDIDATE GENERALISATION": (
        r"\b(most|many|few)\s+candidates\b|\bcandidates\s+(usually|often|typically|tend to|always|generally|look for|check|want|expect|care|value|need)\b"
        r"|\bevery candidate\b|большинство кандидатов|кандидаты обычно|кандидаты (?:всегда|чаще всего)"
    ),
    "EXTERNAL/FREQUENCY (RU)": (
        r"редк\w*|необычн\w*|большинств\w*|обычно|как правило|типичн\w*|стандартн\w*|распространённ\w*|"
        r"распространенн\w*|на рынке|рыночн\w*|другие работодател\w*|многие (?:компании|работодатели)|"
        r"мало кто|немногие|выше среднего|ниже среднего|в отрасли"
    ),
    "LEGAL": r"statutory|legal minimum|by law|\blaw requires|legally required|minimum wage|Working Time|auto-enrol",
    "VERIFICATION WORDING": r"\b(proven|proves|proved|verified|independently confirmed)\b",
    "RETIRED STATUS": r"\bPROVEN\b|\bMISSING\b(?! EVIDENCE)",
}


def scan(run_dir):
    for path in sorted(glob.glob(os.path.join(run_dir, "*.record.json"))):
        record = json.load(open(path, encoding="utf-8"))
        text = record.get("result_text") or ""
        source = record.get("message_sent") or ""
        hits = []
        for name, pattern in PATTERNS.items():
            flags = 0 if name == "RETIRED STATUS" else re.IGNORECASE
            for m in re.finditer(pattern, text, flags):
                if m.group(0) in source:
                    continue
                context = text[max(0, m.start() - 100):m.end() + 70].replace("\n", " ")
                hits.append((name, context))
        if hits:
            print("===== " + os.path.basename(path)[: -len(".record.json")])
            for name, context in hits:
                print("  [{}] …{}…".format(name, context))


if __name__ == "__main__":
    for d in sys.argv[1:]:
        scan(d)
