# Quick start

Two minutes from install to your first audit.

## 1. Install

Install from GitHub with two commands:

```bash
claude plugin marketplace add denzjama/employer-brand-auditor
```

```bash
claude plugin install employer-brand-auditor@employer-brand-auditor
```

Then start a new Claude Code session. To load the plugin from a local folder instead, or to update and remove it, see [`docs/INSTALL.md`](docs/INSTALL.md).

## 2. Give it employer-brand materials

Collect **3–5 candidate-facing materials** as text:
- your careers page;
- your EVP or employer proposition;
- one or two job ads;
- an employee story.

Paste them into the chat, or attach them as files. The auditor does not browse the web, so it sees only what you give it.

## 3. Ask for an audit

Copy and paste this, then add your materials underneath:

```text
Run a full employer brand audit of the materials below. They are our current candidate-facing materials.
```

In Russian: `Проведи полный аудит бренда работодателя по этим материалам.`

## 4. Read Coverage and Confidence first

The top of the audit shows three numbers:
- the **Employer Brand Score** (0–100);
- **Coverage**: how much of the method your material allowed it to assess;
- **Confidence**: how much the score can be relied on.

Read **Coverage** and **Confidence** before the score. A score from thin material is marked **PROVISIONAL**. Below 40% coverage, no score is given at all. See [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md).

## 5. Use the diagnosis before the rewrite

Start with the **biggest problems** and the **Top 3 fixes**. Rewrites come last, and use only facts that are in your material. Missing facts are marked `EVIDENCE NEEDED:` and facts to check are marked `CONFIRM:`. Review any rewritten copy before publishing it.

**Next:** see [`docs/EXAMPLE_PROMPTS.md`](docs/EXAMPLE_PROMPTS.md) for other tasks (EVP stress test, job-ad review, claim-to-proof). For a worked example, see [`demo/`](demo/README.md).
