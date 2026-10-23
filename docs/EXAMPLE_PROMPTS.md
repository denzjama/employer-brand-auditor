# Example prompts

These prompts are ready to copy. Paste your material **underneath** the prompt, or attach it as a file. Each task has a short version and a more detailed one. You can write in any language; the auditor answers in the language you use.

The auditor works on the material you supply, or, when you only name a company, on the public pages it finds and lists in the report. Nothing in these prompts adds information about your company.

## Audit a company by name

**Short**
```text
Audit the employer brand of <company name>.
```

**Detailed**
```text
Audit the employer brand of <company name>, the <industry> company in <country or city>. Focus on how it hires <role families>. Find its careers site, current job ads, employee stories and hiring process yourself.
```

In Russian: `Проаудируй HR-бренд компании <название>.` The auditor saves what it found as a source pack in your folder and lists every page in the report.

**Deep audit**
```text
Run a deep audit of <company name>'s employer brand, with social media and reviews.
```
In Russian: `Сделай глубокий аудит HR-бренда компании <название>, с соцсетями и отзывами.`

**Adding closed social networks**
```text
Update the audit: I put screenshots of the company's Instagram and LinkedIn in social/.
```

---

## Full employer brand audit

**Short**
```text
Run a full employer brand audit of the materials below.
```

**Detailed**
```text
Run a full employer brand audit of the materials below. They are our complete set of current candidate-facing materials: careers page, EVP, two job ads and one employee story. Our priority audiences are field engineers and customer-service staff. Start with the diagnosis, then give the top 3 fixes.
```

The full audit is delivered as an HTML report in your working folder, with a short summary in the chat. Variations:
- materials in a folder: `Run a full employer brand audit. Our candidate-facing materials are in materials/.`
- no file, everything in the chat: `Run a full employer brand audit of the materials below and give it here in the chat, without a file.`
- in Russian: `Проведи полный аудит HR-бренда. Материалы для кандидатов лежат в папке materials/.` (the report and its labels will be in Russian)

## EVP stress test

**Short**
```text
Is this a strong EVP?
```

**Detailed**
```text
Stress-test our EVP below. It is meant for experienced software engineers. Tell me whether it is a real employer proposition, where it breaks, and what would make it hold. Supporting material from our careers page follows the EVP.
```

## Career page review

**Short**
```text
Review this careers page. Why doesn't it convince candidates?
```

**Detailed**
```text
Review the careers page below for the candidates we most want: graduates applying for our engineering programme. Tell me what a candidate can and cannot learn from it, what to keep, fix, remove or add, and rewrite the weakest section using only the facts on the page.
```

## Job ad review

**Short**
```text
Review this job ad.
```

**Detailed**
```text
Review the job ad below from a candidate's point of view. Check whether it gives the facts a candidate needs to decide, whether the employer-brand claims in it are supported, and rewrite it using only the information in the ad. Mark anything that needs our confirmation.
```

## Multi-touchpoint consistency

**Short**
```text
Check these materials for consistency. Do they tell the same story?
```

**Detailed**
```text
Below are four of our touchpoints: the EVP, the careers page, a job ad and a LinkedIn recruitment post. Check whether they make the same promise, whether any of them contradict each other, and which inconsistencies a candidate would notice first.
```

## Claim → proof review

**Short**
```text
Which of our claims are actually proven by these materials?
```

**Detailed**
```text
List the main employer claims in the materials below and, for each one, show what evidence the materials contain, how strong it is, and what evidence would be needed to support it properly. Do not include salary and standard benefits as claims.
```

## Genericity test

**Short**
```text
Is this generic? Could any employer say it?
```

**Detailed**
```text
Run a genericity test on the headline and three pillars below. For each, tell me whether a comparable employer could use it unchanged, which words are stock employer-brand language, and what would make it ownable.
```

## Executive summary

Use this as a follow-up in the same conversation, after an audit.

**Short**
```text
Summarise this audit for our HR director in one page.
```

**Detailed**
```text
Turn this audit into a one-page summary for our HR director and CMO: the score with its coverage and confidence, the three most important problems, the top 3 fixes in order, and the evidence we need to collect. Keep every caveat about coverage and missing evidence.
```

## Rewrite after diagnosis

Use this as a follow-up after an audit or a review. The auditor rewrites only with facts that are in the material, and marks anything missing.

**Short**
```text
Now fix the biggest issues without inventing facts.
```

**Detailed**
```text
Based on the diagnosis above, rewrite the careers page introduction and the first job ad. Use only facts from our materials. Keep every number, scope and condition exactly as written. List anything you would need from us, or anything we should confirm, below the copy, not inside it.
```

---

**Forcing a specific skill.** You can call a skill explicitly instead of letting it be chosen automatically:
- `/employer-brand-auditor:employer-brand-audit`
- `/employer-brand-auditor:evp-stress-test`
- `/employer-brand-auditor:career-content-review`
