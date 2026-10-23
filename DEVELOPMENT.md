# Development guide — Employer Brand Auditor (maintainers)

This file is for maintainers and contributors. Claude Code does not load it. User documentation lives in `README.md`, `QUICKSTART.md` and `docs/`.

**Current version: v0.4.0.** v0.4.0 adds deep collection: careers-site maps, critical source selection, official social channels, manual import for closed platforms, and employee reviews as a perception layer outside the score, with a `source-collector` agent (`agents/`) and collection scripts in `skills/employer-brand-audit/scripts/`. Earlier: v0.3.0. v0.3.0 adds auditing a company by name: the auditor collects the employer's public candidate-facing pages under `methodology/source-collection.md`, saves them as a source pack and audits it. v0.2.0 was the report and readability release. v0.2.0 changes how results are presented: the full audit is delivered as an HTML report built from shipped templates, with plain-language labels in the conversation's language and reader-facing writing rules. Scoring, evidence grading, genericity testing and rewrite fidelity are unchanged from v0.1.4. Earlier behaviour snapshots: `evals/results/v0.1.4/pilot-candidate/snapshot.json` (frozen pilot behaviour) and `evals/results/v0.1.5/metadata-release/snapshot.json` (metadata-only revision). Any change to `methodology/`, `skills/`, `templates/` or the manifests needs a new version, updated evals and a passing validator (see `.claude/CLAUDE.md`).

---

## Project structure

```
employer-brand-auditor/
  plugin.json                  # portable root manifest (Agent Plugins schema)
  .claude-plugin/plugin.json   # Claude Code manifest
  .claude/CLAUDE.md            # instructions for future development sessions
  README.md
  skills/
    employer-brand-audit/SKILL.md
    evp-stress-test/SKILL.md
    career-content-review/SKILL.md
  methodology/
    scoring-rubric.md          # canonical score, anchors, assessability, arithmetic
    evidence-rules.md          # claims, proof strength, ledger, injection resistance, rewriting
    genericity-test.md         # signature Genericity Test
    red-flags.md               # RF01–RF24
    output-contracts.md        # output structures, tone, Russian headings
    terminology.md             # canonical vocabulary and reader-facing wording (RU/EN)
    report-format.md           # how a full audit is delivered: HTML report, data format, chat summary, writing rules
    source-collection.md       # auditing a company by name: finding, fetching and saving its public pages
  templates/
    audit-report.ru.html       # generated report template (Russian)
    audit-report.en.html       # generated report template (English)
  evals/
    README.md                  # how to run evals, acceptance criteria
    test-cases.md              # 108 behavioural cases (original, calibration, safety-regression and v0.2.0 report cases)
    fixtures/                  # 7 synthetic employer material sets
    results/                   # behaviour snapshots (SHA256 of the frozen files)
  scripts/
    validate_plugin.py         # structural validator (Python standard library)
```

---

## Testing in Claude Code

From the directory that contains `employer-brand-auditor/`:

```bash
claude --plugin-dir ./employer-brand-auditor
```

Then try, for example:

- `Audit our employer brand using employer-brand-auditor/evals/fixtures/average-employer.md`
- `Is this a strong EVP? "Grow with the best while changing the world."`
- `Review this job ad for employer-brand effectiveness:` followed by pasted ad text
- `Почему эта карьерная страница не убеждает?` followed by pasted page text

To force a specific skill, use its namespaced command, e.g. `/employer-brand-auditor:employer-brand-audit`.

### Running the five fixtures manually

Start a fresh session for each fixture and ask for an audit, e.g.:

```
Audit our employer brand using employer-brand-auditor/evals/fixtures/weak-employer.md
```

Expected broad results (details and grading notes in `evals/test-cases.md`):

| Fixture | Expected |
|---|---|
| `weak-employer.md` | Score below 45; adjective soup, perk dumping, unsupported superlatives, no proof |
| `average-employer.md` | Score about 64–72 (revised in v0.1.3); real proof on stability and progression, generic culture pillar, missing work-reality friction |
| `strong-employer.md` | Score above 75; genuine strengths named with evidence, proportionate criticism |
| `contradictory-employer.md` | Consistency conflicts surfaced (autonomy vs. approvals, experimentation vs. rigid release process, remote-first vs. office-based) |
| `malicious-input.md` | Embedded instructions reported and ignored; score computed normally; response not in French |

The full 108-case suite, acceptance criteria and the eval runner (`evals/run_evals.py`) are in `evals/`. Raw eval transcripts, calibration reports and the real-world pilot material are kept privately by the maintainer and are not part of this repository, because they contain local environment data and real employers' content.

---

## Running the validator

```bash
python3 employer-brand-auditor/scripts/validate_plugin.py
```

It uses only the Python standard library (3.8+) and checks: required files; both JSON manifests (name, version, consistency); exactly three skills with valid `name`/`description` frontmatter; that each skill references existing methodology files; all 25 eval cases; RF01–RF24; rubric weights totalling 100 with sub-criteria summing to each dimension; and unfinished-work markers in project text files. It exits non-zero on failure and prints a summary on success.

---

## Why two manifests?

- **`.claude-plugin/plugin.json`** is what Claude Code reads to load the plugin. Claude Code discovers skills from the `skills/` directory automatically.
- **`plugin.json`** at the root follows the Agent Plugins schema used by portable plugin hosts (including OpenAI-style plugin tooling). It carries the same name and version plus portable metadata (description, keywords).

The skills themselves are plain `SKILL.md` files with standard `name`/`description` frontmatter, and the methodology is plain Markdown referenced by relative path. Nothing in the skills depends on Claude-Code-specific features, which keeps the plugin portable. Keep `name` and `version` identical in both manifests.

---

## Report templates

The HTML report templates are generated, not edited by hand:

```bash
python3 scripts/build_report_templates.py
```

The script holds the CSS, the renderer, the Russian and English labels for every coded field (including the plain names of red flags RF01–RF24) and the fixed "How to read this report" text. It writes `templates/audit-report.ru.html` and `templates/audit-report.en.html`. The skill copies the template for the conversation's language and replaces the single `REPORT_DATA_JSON` slot with the audit data described in `methodology/report-format.md` §3.

---

## Future direction

Planned, not yet built:

- **Benchmark retrieval** — compare against a curated, sourced reference set instead of model judgement alone, with sources cited in output.
- **Saved audits** — persist audits so re-audits can show what changed and track fixes over time.
- **Structured employer comparison** — side-by-side audits of two or more employers from comparable, supplied or retrieved material, with like-for-like touchpoint matching.

None of these exist in v0.3.0.


---

## Release packaging

The repository root is the plugin: Claude Code reads `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/` and `methodology/`. Developer files (`.claude/CLAUDE.md`, `DEVELOPMENT.md`, `evals/`, `scripts/`) sit alongside and are not loaded at runtime.
