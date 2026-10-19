# Employer Brand Auditor

**v0.1.5 — Release Candidate** · A skills-only plugin for Claude Code

## What is Employer Brand Auditor?

Employer Brand Auditor is an **evidence-first diagnostic tool for employer-brand materials**: careers pages, EVP statements, job ads, employee stories and recruitment content. It reads your materials the way a candidate would and tells you:

- **how clear** your employer proposition (EVP) is;
- **how different** it is from generic employer-brand language;
- **which claims are actually proven** by the material, and which are not;
- **how relevant** the material is to the candidates you want;
- **how consistent** your touchpoints are with each other;
- **which problems to fix first.**

It always works in the same order: **DIAGNOSE → EXPLAIN → PRIORITIZE → IMPROVE.** It diagnoses before it rewrites anything, and a rewrite uses only facts that are in your material.

## The principle: no evidence, no claim

- **No evidence → no claim.** The auditor does not invent facts, statistics, programmes, quotes or benchmarks. Where proof would help but is missing, it writes `EVIDENCE NEEDED: …`. Where a fact needs checking, it writes `CONFIRM: …`.
- **Absence of evidence ≠ evidence of absence.** "Your materials don't show candidates proof of X" never becomes "you don't do X". The audit judges what candidates can see, not what happens inside your company.
- **Support is not verification.** The auditor judges how convincing your material is to a candidate. It does not independently verify your claims.

## Who it is for

**Best for:**
- employer-brand leaders;
- HR marketing teams;
- talent-acquisition leaders;
- recruitment-marketing teams;
- HR and People teams;
- agencies working with employer brands.

**Typical use cases:**
- full employer-brand audit;
- EVP stress test;
- careers-site review;
- job-ad and recruitment-content review;
- claim-to-proof analysis;
- genericity review;
- consistency check across touchpoints.

## What you get

Three skills, chosen automatically from what you ask:

| Skill | Use it for | Main output |
|---|---|---|
| `employer-brand-audit` | A full audit from several materials | Employer Brand Score (0–100) with **Coverage** and **Confidence**; 8-dimension scorecard; what's working; biggest problems; Genericity Test; Claim → Proof ledger; red flags; Top 3 fixes; before → after rewrites; missing evidence |
| `evp-stress-test` | Testing an EVP, employer promise or slogan | Verdict **STRONG / PROMISING BUT GENERIC / WEAK / NOT YET AN EVP**, with the reasoning behind it |
| `career-content-review` | One asset: a careers page, job ad, recruiting post or employee story, plus short tasks like "summarise this" or "pull the best quote" | Candidate decision check, problems, keep / fix / remove / add, and an evidence-bound rewrite |

The auditor answers in your language (tested in English and Russian). Labels such as verdicts, statuses and red-flag codes stay in English.

## Start here

1. **Install:** [`docs/INSTALL.md`](docs/INSTALL.md).
2. **Two-minute start:** [`QUICKSTART.md`](QUICKSTART.md).
3. **See a real example:** [`demo/`](demo/README.md). It contains fictional materials and the unedited output of a real run.

```text
Run a full employer brand audit of the materials below. They are our current candidate-facing materials.

[paste your careers page, EVP, 1–2 job ads and an employee story]
```

## Documentation

| Document | What it covers |
|---|---|
| [`QUICKSTART.md`](QUICKSTART.md) | Install to first audit in about two minutes |
| [`docs/FIRST_RUN.md`](docs/FIRST_RUN.md) | The three-step first run; good input vs minimum input |
| [`docs/EXAMPLE_PROMPTS.md`](docs/EXAMPLE_PROMPTS.md) | Copy-paste prompts for every supported task |
| [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md) | Score, Coverage, Confidence and every section of an audit |
| [`docs/WHAT_IT_DOES_NOT_DO.md`](docs/WHAT_IT_DOES_NOT_DO.md) | Product boundaries |
| [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) | Limitations by design, and limitations observed in the pilot |
| [`docs/INSTALL.md`](docs/INSTALL.md) | Install, verify, update, disable, uninstall |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Common problems and what to do |
| [`RELEASE_NOTES_v0.1.5.md`](RELEASE_NOTES_v0.1.5.md) · [`CHANGELOG.md`](CHANGELOG.md) | What is in this release |
| [`methodology/`](methodology/) | The full method the skills follow |

## What it is not

Employer Brand Auditor is **not**:
- a copy generator;
- a general HR consultant;
- a market or salary benchmark;
- a legal or compliance checker;
- a web crawler;
- an applicant tracking system;
- an employee-engagement survey.

It works only on the material you give it. See [`docs/WHAT_IT_DOES_NOT_DO.md`](docs/WHAT_IT_DOES_NOT_DO.md).

## Status

**v0.1.5 is a release candidate.** It has completed internal evaluation and a real-world pilot on public materials from eleven employers. Known limitations are listed openly in [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md). Review rewritten copy, and verify any factual claim, before you publish it.

**Licence:** MIT. See [`LICENSE`](LICENSE).
