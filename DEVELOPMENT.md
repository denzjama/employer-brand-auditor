# Development guide — Employer Brand Auditor (maintainers)

This file is for maintainers and contributors. Claude Code does not load it. User documentation lives in `README.md`, `QUICKSTART.md` and `docs/`.

**Behaviour is frozen at v0.1.4.** The SHA256 of `methodology/`, `skills/`, both manifests and `CLAUDE.md` are recorded in `evals/results/v0.1.4/pilot-candidate/snapshot.json`. v0.1.5 is a metadata-only revision (manifest version, `author`, `license`); its snapshot, with a per-file comparison against v0.1.4, is `evals/results/v0.1.5/metadata-release/snapshot.json`. Any change to those files needs a new version, updated evals, a passing validator and a new snapshot (see `CLAUDE.md`).

---

## Project structure

```
employer-brand-auditor/
  plugin.json                  # portable root manifest (Agent Plugins schema)
  .claude-plugin/plugin.json   # Claude Code manifest
  CLAUDE.md                    # instructions for future development sessions
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
    terminology.md             # canonical vocabulary
  evals/
    README.md                  # how to run evals, acceptance criteria
    test-cases.md              # 97 behavioural cases (original, calibration and safety-regression cases)
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

The full 97-case suite, acceptance criteria and the eval runner (`evals/run_evals.py`) are in `evals/`. Raw eval transcripts, calibration reports and the real-world pilot material are kept privately by the maintainer and are not part of this repository, because they contain local environment data and real employers' content.

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

## v0.2 direction

Planned, not yet built:

- **MCP-backed URL analysis** — fetch careers pages and job ads directly, with source capture so every quote remains traceable.
- **Benchmark retrieval** — compare against a curated, sourced reference set instead of model judgement alone, with sources cited in output.
- **Saved audits** — persist audits so re-audits can show what changed and track fixes over time.
- **Structured employer comparison** — side-by-side audits of two or more employers from comparable, supplied or retrieved material, with like-for-like touchpoint matching.

None of these exist in v0.1.4.


---

## Release packaging

The repository root is the plugin: Claude Code reads `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/` and `methodology/`. Developer files (`CLAUDE.md`, `DEVELOPMENT.md`, `evals/`, `scripts/`) sit alongside and are not loaded at runtime. `claude plugin validate` reports one expected warning: `CLAUDE.md` at the plugin root is not loaded as project context.
