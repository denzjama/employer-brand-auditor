# Employer Brand Auditor v0.2.0 — Release Notes

v0.2.0 changes how results reach the reader. The analysis behind them is the same as in v0.1.x: the same scoring, evidence rules, genericity test and rewrite safeguards.

## What's new

- **A ready-to-share HTML report.** A full audit now produces a report file in your working folder. It opens in any browser and saves as a PDF with one button. It contains:
  - a cover with the score and what it means;
  - an executive summary for a manager;
  - what the audit covered and what it did not;
  - a score for each of the eight dimensions, with the reason;
  - what works and the main problems, with quotations from your material;
  - a plan of three fixes, each with effort, who to involve and what to watch afterwards;
  - before → after rewrites;
  - one checklist of questions for the company;
  - an appendix with the detailed analysis.
- **"How to read this report"** is built into every report. It explains the score scale and weights, coverage, score reliability, the eight dimensions, the genericity test and the labels in plain words, so the report can be read without knowing the method.
- **A short chat reply.** The chat shows the score, the main conclusion, three to five findings, the first three actions and the path to the report. Ask for the audit "here in the chat" if you do not want a file.
- **Your language, labels included.** A Russian conversation gets a Russian report with Russian labels ("уточнить", "нужны данные", "шаблонное"); an English conversation gets English. Internal codes such as RF numbers or sub-criterion codes no longer appear in the text.
- **Plainer writing.** Reports and replies follow new writing rules:
  - short concrete sentences;
  - no first person;
  - no bureaucratic filler or stock phrases;
  - every judgement explained through your own material;
  - the same facts not repeated across sections.
- **Fewer duplicates.** Red flags are shown on the problems they belong to, and every point that needs your confirmation or new information is collected in one list.

## What stays the same

- No evidence → no claim. Nothing is invented: no facts, figures, quotations or market comparisons.
- Missing proof is reported as missing for candidates, never as proof that a practice does not exist.
- Scores, coverage and reliability follow the same rules. On the reference fixtures, v0.2.0 scores fall in the same calibrated ranges as before.
- EVP stress tests and single-asset reviews still reply in the chat, now with labels in your language.

## Good to know

- A full audit with its report takes several minutes and costs more than a chat-only answer, because the report file is written in full.
- The report loads a web font; offline it falls back to a system font.
- Claude Code asks for permission to write the report file. If writing is not allowed, the audit is given in the chat.

## How to start

1. Install or update: [`docs/INSTALL.md`](docs/INSTALL.md).
2. Follow [`QUICKSTART.md`](QUICKSTART.md).
3. Read [`docs/HOW_TO_READ_AN_AUDIT.md`](docs/HOW_TO_READ_AN_AUDIT.md) or just the "How to read this report" section in your report.
4. See a full example in [`demo/`](demo/README.md).
