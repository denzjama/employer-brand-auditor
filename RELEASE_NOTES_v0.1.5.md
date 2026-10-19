# Employer Brand Auditor v0.1.5 — Release Notes (Release Candidate)

## What changed since v0.1.4

- **MIT License** added (`LICENSE`), with `author` and `license` in the plugin manifests.
- **Nothing else.** The skills and methodology are byte-identical to v0.1.4, so the auditor behaves exactly as in v0.1.4.

## What's included

- **Three skills for Claude Code,** chosen automatically from your request:
  - **Employer brand audit:** an Employer Brand Score (0–100) with Coverage and Confidence; an eight-dimension scorecard; what's working; biggest problems; Genericity Test; Claim → Proof ledger; red flags; Top 3 fixes; before → after rewrites; missing evidence.
  - **EVP stress test:** a verdict (STRONG / PROMISING BUT GENERIC / WEAK / NOT YET AN EVP), with the reasoning behind it.
  - **Career content review:** for a careers page, job ad, recruiting post or employee story, with keep / fix / remove / add and an evidence-bound rewrite. It also handles short tasks such as summaries, bullets, headlines and pulling quotes.
- **The full methodology** the skills follow, in `methodology/`.
- **Documentation and a synthetic demo** in `docs/` and `demo/`.

## Best use cases

- **A full audit** of your careers page, EVP, job ads and employee stories together.
- **Testing whether an EVP or slogan** is a real, ownable proposition.
- **Finding which employer claims your material actually proves,** and which need evidence.
- **Spotting generic employer-brand language,** and inconsistencies between touchpoints.
- **Getting a prioritised list of fixes** before rewriting anything.

## What to expect

- **It works only on the material you supply.** It does not browse the web, use outside knowledge about your company, or benchmark you against the market.
- **Every score comes with Coverage and Confidence.** Thin material gives a provisional score, or no score below 40% coverage.
- **Missing proof is reported as missing evidence,** never as proof that a practice doesn't exist.
- **Rewrites use only your facts.** Anything the auditor would need from you is marked `EVIDENCE NEEDED` or `CONFIRM`.
- **Answers come in your language** (tested in English and Russian). Labels stay in English.
- **Repeated runs on the same material** are usually close, but not identical.

## Known limitations

In the real-world pilot, the auditor did not invent company facts. Occasionally, mostly in long audits:
- a paraphrase appears in quotation marks;
- a qualifier is dropped in a short restatement;
- an item flagged `CONFIRM` is treated as settled in a fix or rewrite;
- a short unsupported comparative remark appears.

With very little material, a provisional score can look more precise than the evidence warrants. Review quotations, `CONFIRM` items and rewritten copy before publishing. Full details: [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

## How to start

1. Install: [`docs/INSTALL.md`](docs/INSTALL.md).
2. Follow [`QUICKSTART.md`](QUICKSTART.md): paste 3–5 materials and ask "Run a full employer brand audit of the materials below."
3. Read Coverage and Confidence first: [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md).
4. See a worked example in [`demo/`](demo/README.md).
