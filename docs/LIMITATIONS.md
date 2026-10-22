# Limitations

## By design

These are deliberate choices, not defects.

- **Evidence-first.** The auditor judges only the material you supply. It does not use outside knowledge about your company, your competitors or your market.
- **No automatic external validation.** Employer facts are treated as not independently checked unless you supply an independent source. That does not mean "doubtful".
- **No market benchmarking without evidence.** Scores are measured against the method, not against other employers. The score bands are reading aids, not percentiles.
- **Missing public evidence does not mean a missing internal practice.** The audit says what candidates can see, not what happens inside the company.
- **Thin material gives limited results.** With little material, coverage and confidence drop. Below 40% coverage, no score is given.
- **Scores are structured expert judgements.** The rules and arithmetic are fixed, but judging each criterion involves interpretation. Repeated runs on the same material are usually close, but not identical.
- **No memory between sessions.**
- **Collection from the web is a snapshot.** When you name a company, the auditor collects its public candidate-facing pages on that day. Search can miss pages, some sites block automatic reading, and pages change. Types of material it could not find are left out of the score and listed in the report. Quotations are checked against the captured text, which is saved in the source pack.
- **How pages are read.** With a shell available, the plugin reads pages itself through your connection and keeps their exact wording. Without it, it uses Claude's page-reading tool, which can return part of a page as a paraphrase; the report says when this happened, and only exact wording is quoted.
- **Regional blocks and certificates.** Some Russian sites refuse VPN or foreign connections, and some use certificates that are not trusted outside Russia. The plugin never bypasses either; see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) for how to open them.
- **The HTML report is for the full audit.** EVP stress tests and single-asset reviews reply in the chat.
- **A full audit with its report takes longer and costs more** than a chat-only answer, typically several minutes, because the report file is written in full. Ask for the audit "here in the chat" if you do not need the file.
- **The report uses a web font.** Offline, it falls back to a system font; the content is unchanged.

## Limitations seen in the pilot

In the real-world pilot (public materials from eleven employers), the auditor **did not invent any company facts**. Some smaller issues were observed occasionally, mostly in long, full audits:

- **Quote and paraphrase formatting.** Occasionally a paraphrase appears inside quotation marks, as if it were the material's exact wording. The meaning was preserved in the cases observed.
- **Scope drift in long audits.** Occasionally a qualifier is dropped in a short restatement (for example "about" or "at one site"), although it is stated correctly elsewhere in the same audit.
- **"Confirm" items leaking into recommendations or rewrites.** Occasionally something the audit itself flagged as needing confirmation is treated as settled in a fix heading or in rewritten copy.
- **Unsupported normative or comparative asides.** Occasionally a short remark about typical reader reactions or rarity appears next to an otherwise material-based judgement.
- **Thin-footprint score presentation.** When very little material is supplied, coverage can still pass the 40% threshold. The resulting provisional score may then look more precise than the evidence warrants. The audit marks it provisional and explains the limits; read it as indicative.

**What to do about them:**
- check quotations against your source before reusing them;
- check every "Confirm" item before publishing;
- treat comparative remarks without a source as hypotheses;
- review rewritten copy before it goes live.

These issues are on the roadmap for a future version.
