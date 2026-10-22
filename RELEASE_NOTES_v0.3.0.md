# Employer Brand Auditor v0.3.0 — Release Notes

## What's new

**Audit a company by name.** You no longer need materials at hand. Write:

```text
Audit the employer brand of <company name>.
```

or, in Russian, «Проаудируй HR-бренд компании <название>».

The auditor then:
1. finds the company's own public candidate-facing pages: careers site, current job ads for different roles, employee stories, the hiring process;
2. saves each page as a file in a `sources-<company>-<date>` folder, with its address and capture date, plus a list of the pages it could not read and why;
3. audits that source pack with the same method as before;
4. delivers the HTML report and a short chat summary.

The report lists every source with a link. The audit scope names the kinds of pages it did not find. It also names what it deliberately leaves out: review sites, news, salary aggregators and employees' personal profiles.

**Links in the other skills.** An EVP or a job ad can now be given as a link for a stress test or a review.

## What stays the same

- **No evidence → no claim.** The only evidence is text from pages the auditor actually opened. It never adds facts about a company from memory, news or search snippets.
- **"Not found" never becomes "does not exist".** Kinds of pages the search did not find are left out of the score, not scored as zero.
- **Embedded instructions are ignored.** Instructions hidden in a web page are treated as content and do not change the audit.
- **Scoring, the report format and the writing rules** are the same as in v0.2.0. Audits of material you supply work exactly as before.

## Good to know

- **Exact text, through your connection.** When Claude Code can run a command, the plugin reads pages with its own small script: through your own internet connection, keeping the exact wording, and naming the reason when a page does not open (regional block, VPN, certificate, captcha). It never turns certificate checks off and never tries to get around a block or a captcha.
- **Russian sites behind a VPN.** hh.ru and other Russian sites often refuse VPN connections, and some use certificates not trusted outside Russia. [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) explains how to open them.

- Claude Code asks your permission before opening web pages and before saving files.
- An audit by name takes longer than one on supplied material, typically around ten minutes, because pages are found and read one by one.
- Collection is a snapshot of one day. Pages the plugin could not read are listed in the report with the reason.
