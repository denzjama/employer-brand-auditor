# Changelog

## v0.4.1

- **Complete texts.** The collector saves pages, posts and reviews in full, so every quotation can be checked against the saved source.
- **Quieter chat.** Progress notes during an audit are one short line about the audit; tools, files and checks are never narrated.

## v0.4.0

- **Deep audit on request.** The plugin maps the employer's whole careers site from its sitemaps and links, selects sources critically and records in a source map why each was used or left out, samples job ads evenly across roles, and reports how many ads it found.
- **Social media.** Official Telegram channels (public preview), YouTube channels (public feed) and VK communities (official API, with your key) are read and analysed: purpose, rhythm, share of posts about people and work, themes, consistency with the careers site. Accounts must be verifiably official.
- **Closed networks by manual import.** Instagram, Facebook, TikTok, X, LinkedIn and Glassdoor are never scraped; the report lists the official accounts and what to screenshot, and audits screenshots added to `social/`.
- **Promise and perception.** Public employee reviews form a separate section: themes over the sample read, compared with the company's promises. Reviews never change the score; reviewers are never identifiable.
- **New tools:** `discover_site.py`, `telegram_channel.py`, `youtube_channel.py`, `vk_wall.py`, and a `source-collector` agent that runs deep collection on a faster model.
- **Evals:** TC-109 – TC-116.

## v0.3.1

- The page-fetch script is now called as one plain command per page, so a single `python3` permission covers every fetch and the plugin no longer falls back to the paraphrasing page tool when other shell commands are refused.
- The report records the actual plugin version.

## v0.3.0

- **Audit a company by name.** "Audit the employer brand of <company>" with no files: the auditor finds the company's public careers site, current job ads, employee stories and hiring-process pages, saves them as a source pack and audits them.
- **Every source is listed** in the report with its link and capture date; types not found are left out of the score and named in the audit scope.
- **Links work in the other skills:** an EVP or a job ad can be given as a link.
- **Unchanged:** evidence comes only from fetched page text, never from memory, news or review sites; scoring and the report are the same as in v0.2.0.
- **Evals:** TC-102 rewritten; new cases TC-104 – TC-108.

## v0.2.0

- **HTML report.** A full audit is delivered as a ready-to-share HTML report (built from templates shipped with the plugin) plus a short chat summary. The report can be saved as a PDF.
- **Built-in methodology explanation.** Every report includes "How to read this report": score scale and weights, coverage, score reliability, the eight dimensions, the genericity test and the labels.
- **Executive summary, audit scope and an actionable plan** (effort, who to involve, what to watch) in every report.
- **Labels in the conversation's language.** Russian conversations get Russian labels; internal codes no longer appear in reader-facing text.
- **Plain-language writing rules** for all reader-facing text.
- **Red flags folded into the main problems;** all confirmation and missing-information items collected into one checklist.
- **Unchanged:** scoring, evidence grading, genericity test, red-flag definitions and rewrite safeguards.
- **Evals:** six new cases (TC-98 – TC-103); TC-02 updated for Russian labels.

## v0.1.5 — Release Candidate

- **Licence:** released under the MIT License (`LICENSE`).
- **Manifest metadata:** added `author` and `license` to the plugin manifests.
- **No behaviour change.** The skills and methodology are byte-identical to v0.1.4, so audits, scores and verdicts work exactly as in v0.1.4.

## v0.1.4 — Release Candidate

Employer Brand Auditor v0.1.4 — Release Candidate.

- **Evidence-first audit.** Findings are built only from the supplied material. No invented facts, statistics or benchmarks; missing proof is marked `EVIDENCE NEEDED`, facts to check are marked `CONFIRM`.
- **Three core skills:**
  - `employer-brand-audit` (full audit);
  - `evp-stress-test` (EVP verdict);
  - `career-content-review` (single assets and short transformations such as summaries, bullets, headlines and quotes).
- **Coverage and Confidence** with every score. Items the material cannot show are excluded rather than scored as zero. Thin material gives a provisional score, or no score below 40% coverage.
- **Claim → Proof methodology.** Material claims are extracted and their support is graded. Evidence source, support strength and verification are kept separate.
- **Genericity detection.** Core claims are tested for substitutability, stock language, specificity and defensibility.
- **Rewrite fidelity safeguards:**
  - rewrites keep every number, scope, condition, time period and attribution;
  - quotations stay verbatim or become a labelled paraphrase;
  - unconfirmed facts stay out of copy.
- **Real-world pilot completed** on public candidate-facing materials from eleven employers.
- **Documentation:** quick start, first-run guide, example prompts, a guide to reading an audit, limitations, install and troubleshooting.
- **Demo:** a synthetic demo with the unedited output of a real run.
