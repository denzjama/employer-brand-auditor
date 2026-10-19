#!/usr/bin/env python3
"""Score stability statistics for a repeatability run. Python standard library only.

Usage:
    python3 evals/stability.py <repeatability-run-dir> [--scores extracted-scores.json]

Reads the scores file written by `run_evals.py extract` (optionally hand-corrected
and saved under another name), prints per-fixture statistics and the fixture
ordering check, and writes stability.json next to it (never overwriting).
"""

import argparse
import json
import statistics
from pathlib import Path

TARGET_RANGE = {"weak": 8, "average": 10, "strong": 8}
ORDER = ("weak", "average", "strong")
DIMENSIONS = ("Clarity", "Differentiation", "Proof", "Audience Fit", "Employee Truth", "Consistency",
              "Candidate Relevance", "Conversion")


def describe(values):
    values = [v for v in values if isinstance(v, (int, float))]
    if not values:
        return None
    return {
        "n": len(values),
        "values": values,
        "mean": round(statistics.mean(values), 2),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "range": max(values) - min(values),
        "stdev_sample": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
        "stdev_population": round(statistics.pstdev(values), 2),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--scores", default="extracted-scores.json")
    opts = parser.parse_args()
    run_dir = Path(opts.run_dir).resolve()
    rows = json.loads((run_dir / opts.scores).read_text(encoding="utf-8"))

    by_fixture = {}
    for row in rows:
        fixture = row["id"].split("-run")[0]
        by_fixture.setdefault(fixture, []).append(row)

    report = {"fixtures": {}, "ordering": {}}
    for fixture, items in sorted(by_fixture.items()):
        items.sort(key=lambda r: int(r["id"].split("-run")[1]))
        stats = describe([r.get("score") for r in items])
        dims = {d: describe([r.get(d) for r in items]) for d in DIMENSIONS}
        target = TARGET_RANGE.get(fixture)
        report["fixtures"][fixture] = {
            "score": stats,
            "coverage": [r.get("coverage") for r in items],
            "confidence": [r.get("confidence") for r in items],
            "dimensions": dims,
            "target_range": target,
            "within_target": (stats["range"] <= target) if (stats and target is not None) else None,
        }

    present = [f for f in ORDER if f in by_fixture]
    if len(present) == 3:
        scores = {f: [r.get("score") for r in sorted(by_fixture[f], key=lambda r: int(r["id"].split("-run")[1]))]
                  for f in ORDER}
        paired = []
        for i in range(min(len(v) for v in scores.values())):
            w, a, s = scores["weak"][i], scores["average"][i], scores["strong"][i]
            ok = None if None in (w, a, s) else (w < a < s)
            paired.append({"run": i + 1, "weak": w, "average": a, "strong": s, "ordered": ok})
        clean = {f: [v for v in scores[f] if v is not None] for f in ORDER}
        all_pairs = bool(all(clean.values())) and max(clean["weak"]) < min(clean["average"]) \
            and max(clean["average"]) < min(clean["strong"])
        report["ordering"] = {
            "paired_by_run_index": paired,
            "every_paired_run_ordered": all(p["ordered"] for p in paired),
            "every_cross_run_combination_ordered": all_pairs,
        }

    print(json.dumps(report, indent=2))
    target = run_dir / "stability.json"
    n = 2
    while target.exists():
        target = run_dir / "stability-{}.json".format(n)
        n += 1
    with open(target, "x", encoding="utf-8") as handle:
        handle.write(json.dumps(report, indent=2))
    print("Wrote {}".format(target))


if __name__ == "__main__":
    main()
