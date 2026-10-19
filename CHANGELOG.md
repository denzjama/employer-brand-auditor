# Changelog

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
