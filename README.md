# Employer Brand Auditor

**Find out which of your employer-brand claims a candidate would actually believe.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.5-informational.svg)](CHANGELOG.md)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](docs/INSTALL.md)

Employer Brand Auditor is a Claude Code plugin that audits careers pages, EVPs, job ads and employee stories through a candidate's eyes. It scores what your material **proves**, not what it promises. It shows where your copy sounds like everyone else's, and it tells you what to fix first.

**No evidence → no claim.** It never invents facts, figures, quotes or benchmarks. Where proof is missing, it says so.

## Install

```bash
claude plugin marketplace add denzjama/employer-brand-auditor
```

```bash
claude plugin install employer-brand-auditor@employer-brand-auditor
```

Start a new Claude Code session. Then paste your materials and ask:

```text
Run a full employer brand audit of the materials below. They are our current candidate-facing materials.
```

Other ways to install, plus update and uninstall: [`docs/INSTALL.md`](docs/INSTALL.md).

## What you get back

Below are excerpts from a real run on a **fictional** lift-maintenance company. The output is not edited. The full audit, inputs and prompt are in [`demo/`](demo/README.md).

**The headline:**

> **Employer Brand Score: 63/100**
> **Coverage:** 100%
> **Confidence:** HIGH (four touchpoint types: T1, T2, T3, T5)

> The specific, honest content sits in the engineer job ad and Ilse Varga's story: on-call one week in four, a 2am hospital call, and her path from apprentice to mentor. The careers page and the proposition turn that content into stock phrases and leave the evidence behind.

**A genericity verdict** on the company's employer promise:

> **CLAIM:** "Our promise: Lift people up."
> - **VERDICT:** GENERIC
> - **WHY:** The wordplay on lifts is category-specific, not employer-specific, so a comparable lift-maintenance employer could reuse it unchanged.

**A fix that uses only facts the company already published.**

Before:

> Why join us? Work that matters to the communities we serve / Training and development from day one / A supportive, close-knit team / Flexible working

After:

> - **Work people depend on.** We maintain around 3,400 lifts and escalators in hospitals, housing blocks, shopping centres and railway stations across the Westmere region. Last year our engineers answered 11,200 call-outs, and 92% of entrapment calls in hospitals were reached within 45 minutes.
> - **Learn the trade properly.** Every apprentice is paired with a senior engineer for the whole programme and works towards a Level 3 lift engineering qualification. Read how Ilse Varga went from apprentice in 2019 to qualified engineer in 2023.

> - EVIDENCE NEEDED: what flexible working means, for which roles.

The full audit also contains:
- an 8-dimension scorecard with 34 sub-criteria;
- a Claim → Proof ledger;
- red flags;
- Top 3 fixes;
- a list of missing evidence.

## Three skills, picked automatically

| Ask for… | Skill | You get |
|---|---|---|
| A full audit of several materials | `employer-brand-audit` | **Employer Brand Score** (0–100) with **Coverage** and **Confidence**. Also: scorecard, Genericity Test, Claim → Proof ledger, red flags, Top 3 fixes, before → after rewrites |
| "Is this a strong EVP?" | `evp-stress-test` | One verdict, **STRONG / PROMISING BUT GENERIC / WEAK / NOT YET AN EVP**, with the reasoning behind it |
| A review of one careers page, job ad, recruiting post or employee story | `career-content-review` | Candidate decision check, plus keep / fix / remove / add, plus an evidence-bound rewrite |

It works in a fixed order: **DIAGNOSE → EXPLAIN → PRIORITIZE → IMPROVE.** You always get the diagnosis before any rewrite. Answers come in your language (tested in English and Russian).

## Why trust the output

- **No evidence → no claim.** Missing proof is marked `EVIDENCE NEEDED`. Facts to double-check are marked `CONFIRM`.
- **Absence of evidence ≠ evidence of absence.** "Your materials don't show X" never becomes "you don't do X".
- **Every score shows its basis.** Coverage tells you how much of the scorecard your material could support. With thin material, the score is marked provisional. Below 40% coverage, it is withheld.
- **Your material is data, not instructions.** Instructions hidden inside a pasted page are reported and ignored.
- **Tested before release.** It was checked against a suite of 97 behavioural test cases and in a real-world pilot on public materials from eleven employers. Known limitations are listed openly in [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

## Who it is for

**Users:**
- employer-brand and HR-marketing teams;
- talent-acquisition leaders;
- recruitment-marketing agencies;
- anyone who writes careers pages or job ads and wants an honest second read before publishing.

**What it is not:**
- a copy generator;
- an HR consultant;
- a salary or market benchmark;
- a legal checker;
- a web crawler;
- an ATS;
- an engagement survey.

It works only on the material you give it. See [`docs/WHAT_IT_DOES_NOT_DO.md`](docs/WHAT_IT_DOES_NOT_DO.md).

## Documentation

| Document | What it covers |
|---|---|
| [`QUICKSTART.md`](QUICKSTART.md) | Install to first audit in about two minutes |
| [`docs/FIRST_RUN.md`](docs/FIRST_RUN.md) | The three-step first run; good input vs minimum input |
| [`docs/EXAMPLE_PROMPTS.md`](docs/EXAMPLE_PROMPTS.md) | Copy-paste prompts for every supported task |
| [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md) | Score, Coverage, Confidence and every section of an audit |
| [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) | Limitations by design, and limitations seen in the pilot |
| [`docs/WHAT_IT_DOES_NOT_DO.md`](docs/WHAT_IT_DOES_NOT_DO.md) | Product boundaries |
| [`docs/INSTALL.md`](docs/INSTALL.md) · [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Install, update, uninstall; common problems |
| [`demo/`](demo/README.md) | A full worked example, unedited |
| [`methodology/`](methodology/) | The full method the skills follow |
| [`RELEASE_NOTES_v0.1.5.md`](RELEASE_NOTES_v0.1.5.md) · [`CHANGELOG.md`](CHANGELOG.md) | What is in this release |

## На русском

**Employer Brand Auditor** — плагин для Claude Code. Он проверяет карьерные страницы, EVP, вакансии и истории сотрудников глазами кандидата:
- насколько ясно и отлично от других ваше предложение работодателя;
- какие утверждения подкреплены фактами, а какие нет;
- что исправить в первую очередь.

Главное правило: **нет доказательства — нет утверждения**. Плагин не выдумывает факты, цифры и цитаты. Отсутствие доказательства в материалах он не выдаёт за отсутствие практики в компании.

Установка — две команды из раздела [Install](#install). Затем вставьте материалы и напишите: «Проведи полный аудит бренда работодателя по этим материалам». Ответ придёт на русском, а метки (вердикты, статусы, `EVIDENCE NEEDED`) останутся на английском.

## Status and licence

**v0.1.5** is a release candidate. Review rewritten copy, and verify any factual claim, before you publish it. Feedback and issues are welcome.

Licensed under the [MIT License](LICENSE).
