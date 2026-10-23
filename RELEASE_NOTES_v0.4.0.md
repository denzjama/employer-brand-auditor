# Employer Brand Auditor v0.4.0 — Release Notes

## What's new: the deep audit

Ask for it by name:

```text
Run a deep audit of <company name>'s employer brand, with social media and reviews.
```

In Russian: «Сделай глубокий аудит HR-бренда компании <название>, с соцсетями и отзывами».

A deep audit adds four things to the regular audit by company name.

**1. A map of everything public, and a critical choice from it.**
- The plugin reads the careers site's sitemaps and links, respecting robots.txt.
- It lists every candidate-facing page it finds: culture, benefits, teams, locations, students, hiring process, stories and job ads.
- It selects from that map and records in the report why each source was used or excluded. For example: not official, a duplicate, outdated, or another brand.
- Job ads are sampled evenly across roles, levels and places, and the report says how many ads it found in total.

**2. Social media.**
- Official Telegram channels (from their public web preview), YouTube channels (from their public feed) and VK communities (through VK's official API, with your own key) are read.
- For each account it reports:
  - its purpose;
  - the posting rhythm;
  - the share of posts about people and work;
  - its themes;
  - whether it carries the same promise as the careers site.
- An account is used only when it is verifiably the company's own.

**3. Closed networks by manual import.**
- Instagram, Facebook, TikTok, X, LinkedIn and Glassdoor are never scraped or logged into.
- The report lists the official accounts with links and exactly what to screenshot.
- Put the screenshots in a `social/` folder and ask again: they are audited like any other material.

**4. Promise and perception.**
- Public employee reviews form a separate section: what reviewers say about pay, growth, workload, management, onboarding and other topics. Each theme is shown as "N of M reviews read", with its tone and how it relates to the company's promise.
- Reviews never change the score.
- No reviewer can be identified.
- With few reviews, themes are listed without counts.

## How it runs

- **A faster collector.** In Claude Code, a separate collector agent on a faster model gathers the sources. The audit itself runs as before.
- **Time.** A deep audit takes considerably longer than a quick one, typically half an hour or more, and uses more of your plan's capacity.
- **Network.** Pages are read through your own connection. VPN and certificate issues are reported with what to do (see [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)).

## What stays the same

- No evidence, no claim: only text the plugin actually read, or screenshots you supplied, counts as evidence. It never uses what a model may remember about a company.
- The scoring, the report and the writing rules are unchanged. Quick audits work as in v0.3.1.
