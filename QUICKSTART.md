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

## 2. Name the company, or give it materials

The simplest start needs no files:

```text
Audit the employer brand of <company name>.
```

The auditor finds the company's public careers site, current job ads, employee stories and hiring-process pages, saves them as a source pack in your folder, and audits them. Claude Code asks your permission before it opens web pages.

To audit material that is not public, such as a new EVP or draft job ads, collect **3–5 candidate-facing materials** as text:
- your careers page;
- your EVP or employer proposition;
- one or two job ads;
- an employee story.

Paste them into the chat, attach them as files, or put them in a folder and name the folder in your request. When you supply material, the auditor works on exactly that material.

## 3. Ask for an audit

Copy and paste this, then add your materials underneath:

```text
Run a full employer brand audit of the materials below. They are our current candidate-facing materials.
```

In Russian: `Проведи полный аудит бренда работодателя по этим материалам.`

## 4. Open the report

You get a short reply in the chat and an **HTML report** in your working folder. Open it in any browser; the button in the corner saves it as a PDF. The report is in the language of your conversation.

At the top you see three numbers, each with a one-line explanation:
- the **score** (0–100) and what it means on the method's scale;
- **coverage**: how much of the method your material allowed it to assess;
- **score reliability**: whether there was enough material of different types for a stable score.

A score from thin material is marked **provisional**. Below 40% coverage, no score is given at all. The report has a built-in "How to read this report" section; the same explanation is in [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md).

If you prefer the audit in the chat without a file, say so: "Give me the audit here in the chat.

## 5. Use the diagnosis before the rewrite

Start with the **executive summary**, the **main problems** and the **plan**. Rewrites come last, and use only facts that are in your material. Missing facts are marked **Information needed** and facts to check are marked **Confirm**; all of them are collected in "Questions for the company". Review any rewritten copy before publishing it.

**Next:** see [`docs/EXAMPLE_PROMPTS.md`](docs/EXAMPLE_PROMPTS.md) for other tasks (EVP stress test, job-ad review, claim-to-proof). For a worked example, see [`demo/`](demo/README.md).
