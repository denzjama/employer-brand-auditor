# Report Format — How a Full Audit Is Delivered

A full audit (`employer-brand-audit`) is delivered as two things:

1. **An HTML report file**, built from the template shipped with the plugin. This is the complete audit.
2. **A short chat summary** that points to the file.

The analysis behind them is unchanged. Scoring, evidence grading, genericity testing, red flags, quarantine and rewrite fidelity follow the other methodology files exactly. This file defines only how the result is presented to a reader who has never seen the methodology.

---

## 1. Reader and language

### 1.1 The reader

Write for an HR or employer-brand professional who:
- knows hiring in practice;
- has never read this methodology;
- will show the report to a manager.

Every sentence must make sense to that reader without a glossary.

### 1.2 Language

- **The report language is the language of the user's request and conversation.**
  - A Russian conversation gets a Russian report, Russian labels and the Russian template.
  - An English conversation gets English throughout.
- **Everything in the reader's language.** Labels, statuses, severities, verdicts and section names are all written in the report language. The template supplies the labels for every coded field (section 4). In prose, use the reader-facing wording in `terminology.md` §7, never the English capitals.
- **Quotations stay in their original language.** Quotations from the material are reproduced verbatim in the language of the material.
- **Canonical codes are internal.** The English canonical labels (GENERIC, PARTIALLY SUPPORTED, CONFIRM, EVIDENCE NEEDED, RF codes, sub-criterion codes, T1–T8, Q1–Q6) are the methodology's internal identifiers. They appear in the data file as codes (section 3) and never in reader-facing prose.

---

## 2. Delivery procedure

### 2.1 Write the HTML report

1. **Choose the template** for the report language:
   - `../../templates/audit-report.ru.html` for Russian;
   - `../../templates/audit-report.en.html` for English and any other language.

   For a third language, use the English template and write all prose in the user's language.
2. **Build the audit data object** described in section 3.
3. **Serialise it as JSON.**
   - Escape every `</` inside string values as `<\/` so that the data cannot close the script block.
   - Use `\n` for line breaks inside strings.
4. **Create the report file** in the user's working directory.
   - **File name:** `hr-brand-audit-<company-slug>-<YYYY-MM-DD>.html` (Latin letters, digits and hyphens).
   - **Content:** the template with the single placeholder `REPORT_DATA_JSON` replaced by the JSON.
   - **Do not change anything else in the template.**
   - If a shell is available, the most reliable way is to copy the template to the target path and then replace the placeholder with an edit. Otherwise write the full file: the complete template text with the placeholder replaced.
5. **Check the file** by rereading it (no tool is needed):
   - the placeholder is gone;
   - the JSON parses;
   - every quotation in it passes the quotation preflight (`evidence-rules.md` §10.3).

### 2.1a A company name without material

If the user names a company but supplies no candidate-facing material, collect its public candidate-facing pages under `source-collection.md` and audit them; the report then lists every page in `sources` and states the capture date and the limits of automatic collection. Only when no web tools are available, or nothing usable is found, is no report written: explain in the chat, in plain words, what was searched, and list what to supply, in priority order (`output-contracts.md` §1.2). Nothing about the company is invented.

### 2.2 When no file can be written

If the environment cannot create files, or the user asks for the audit in the chat only:
- give the full audit in the chat, in the reader-facing structure of section 5;
- follow the same language and vocabulary rules;
- do not print the JSON.

### 2.3 The chat summary

After the file is written, the chat reply contains only the following, in the user's language:

1. **One line:** the company, the score with its reading band (`scoring-rubric.md` §7), coverage and score reliability. If the score is provisional or withheld, say so.
2. **The one-line verdict.**
3. **Three to five key findings** (the same items as the summary's `points`).
4. **The three first actions.**
5. **The file:** its path, and that it opens in any browser and can be saved as PDF with the button in the corner.
6. **Questions, if any.** At most one or two questions whose answers would change a conclusion.

The chat summary does not repeat the scorecard, the ledger, the genericity table or the rewrites. It follows the writing rules in section 6, including no first person, and says nothing about how the file was built or checked.

---

## 3. Audit data (JSON)

All prose fields are reader-facing text in the report language and follow section 6. All fields marked *code* take one of the listed values exactly. Omit a field or use an empty list when it does not apply.

```
{
  "lang": "ru" | "en",
  "company": "Employer name as given in the material, or a neutral description",
  "date": "YYYY-MM-DD",
  "plugin_version": "the version in .claude-plugin/plugin.json, e.g. 0.3.1",
  "score": {
    "value": 0-100 integer, omitted when withheld,
    "provisional": true | false,
    "withheld": true | false,
    "coverage": 0-100 integer,
    "confidence": code "high" | "medium" | "low",
    "reliability_note": "short plain reason, e.g. 'all 34 criteria assessed, four types of material'"
  },
  "verdict": "the one-line verdict",
  "notices": ["optional notices shown under the cover, e.g. the embedded-instruction notice"],
  "materials": [{"name": "Careers page", "type": "plain type name, e.g. 'Job ad'"}],
  "sources": [{"title": "page title", "url": "https://…", "type": "plain type name", "captured": "YYYY-MM-DD"}],
  "source_map": [{"source": "plain name, or a group such as '401 job ads in the careers sitemap'", "url": "https://…", "kind": "plain kind", "decision": code "included" | "excluded" | "unavailable" | "manual", "reason": "plain reason"}],
  "social": [{"platform": "Telegram", "account": "@name", "url": "https://…", "purpose": "plain", "sample": "N posts, period", "rhythm": "posts per month in the sample", "people_share": "N of M posts", "themes": ["…"], "notes": "…"}],
  "perception": {
    "sample": [{"platform": "…", "reviews": N, "period": "…", "rating": "as shown on the platform, with date and review count"}],
    "thin": true | false,
    "themes": [{"theme": "…", "mentions": N, "of": M, "tone": code "positive" | "negative" | "mixed", "promise": "the related employer promise, or empty", "match": code "consistent" | "mixed" | "tension" | "not_addressed", "note": "…"}],
    "caveat": "optional extra caveat"
  },
  "manual_import": [{"platform": "Instagram", "url": "https://…", "capture": ["what to screenshot"]}],
  "scope": {
    "reviewed": ["what the audit covered, e.g. 'five texts supplied by you: careers page, EVP, two job ads, one employee story'"],
    "not_reviewed": ["candidate-facing channels that were not supplied, e.g. social media, review sites, the interview process, what employees say outside official channels"]
  },
  "summary": {
    "points": ["3–5 key findings, one or two sentences each: what works, what does not, the non-obvious insight"],
    "actions": ["the three first actions, one line each"]
  },
  "dimensions": [
    {
      "id": code "clarity" | "differentiation" | "proof" | "audience_fit" | "employee_truth" | "consistency" | "candidate_relevance" | "conversion",
      "score": integer, "max": integer (the dimension maximum: 12, 16, 16, 12, 10, 12, 12, 10),
      "assessable": true | false,
      "why": "2–3 plain sentences: what in the material drove the score",
      "criteria": [{"name": "plain name of the sub-criterion", "score": n, "max": n, "assessable": true | false, "note": "one plain line"}]
    }
  ],
  "strengths": [{"title": "short title", "text": "what works and the evidence for it"}],
  "problems": [
    {
      "severity": code "critical" | "high" | "medium" | "low",
      "title": "the problem in one plain sentence",
      "evidence": ["verbatim quotation or anchored paraphrase from the material"],
      "why": "why it matters, stated about the material",
      "flags": ["red-flag codes this problem triggers, e.g. 'RF14'; the template shows their plain names"]
    }
  ],
  "fixes": [
    {
      "title": "the fix in one line",
      "needs_new_data": true | false,
      "steps": ["what to do and where"],
      "why_first": "why it is in this position",
      "needs": ["information the fix requires"],
      "effort": code "small" | "medium" | "large",
      "effort_note": "what the effort consists of, in one line",
      "who": ["roles to involve, e.g. 'finance (salary range)', 'café managers (stories)'"],
      "check": ["what to watch after the change, stated as something to observe, never as a predicted result"]
    }
  ],
  "rewrites": [
    {
      "title": "which passage",
      "original": "verbatim original",
      "problem": "what is wrong",
      "logic": "how the rewrite fixes it",
      "rewrite": "the rewritten copy",
      "notes": [{"kind": code "confirm" | "evidence", "text": "..."}]
    }
  ],
  "questions": [{"kind": code "confirm" | "evidence", "for": code "audit" | "communication", "text": "..."}],
  "genericity": [
    {
      "claim": "the claim (quoted or anchored paraphrase)",
      "verdict": code "distinctive" | "partial" | "generic",
      "substitution": code "breaks" | "bends" | "survives",
      "ubiquity": code "rare" | "common" | "ubiquitous",
      "specificity": code "high" | "some" | "none",
      "defensibility": code "owned" | "supportable" | "unowned",
      "why": "plain reason"
    }
  ],
  "ledger": [
    {
      "claim": "the claim",
      "class": code "core" | "supporting",
      "evidence": "what supports it, with its location, or 'not found'",
      "strength": code "strong" | "moderate" | "weak" | "none",
      "status": code "strong" | "partial" | "weak" | "none" | "conflicting",
      "comment": "plain reason, including any open question in plain words"
    }
  ]
}
```

### 3.1 Code mapping

| Methodology label | Data code |
|---|---|
| HIGH / MEDIUM / LOW confidence | `high` / `medium` / `low` |
| CRITICAL / HIGH / MEDIUM / LOW severity | `critical` / `high` / `medium` / `low` |
| DISTINCTIVE / PARTIALLY DIFFERENTIATED / GENERIC | `distinctive` / `partial` / `generic` |
| Substitution: Breaks / Bends / Survives | `breaks` / `bends` / `survives` |
| Ubiquity: Rare / Common / Ubiquitous | `rare` / `common` / `ubiquitous` |
| Specificity: High / Some / None | `high` / `some` / `none` |
| Defensibility: Owned / Supportable / Unowned | `owned` / `supportable` / `unowned` |
| CORE CLAIM / SUPPORTING CLAIM | `core` / `supporting` |
| Support strength: STRONG / MODERATE / WEAK / NONE | `strong` / `moderate` / `weak` / `none` |
| STRONGLY / PARTIALLY / WEAKLY SUPPORTED / UNSUPPORTED / CONFLICTING | `strong` / `partial` / `weak` / `none` / `conflicting` |
| CONFIRM / EVIDENCE NEEDED | `confirm` / `evidence` |
| Red flag RF01–RF24 | `RF01` … `RF24` in `problems[].flags` |
| Source decision | `included` / `excluded` / `unavailable` / `manual` |
| Review theme tone and match | `positive` / `negative` / `mixed`; `consistent` / `mixed` / `tension` / `not_addressed` |
| Fix effort | `small` (rewording with facts already in the material) / `medium` (needs one or two new facts or a person's input) / `large` (needs new information gathered across the company or new content such as stories) |

The template turns these codes into reader-facing labels with explanations. For example, `survives` is shown as "fits anyone" and `confirm` as "Confirm".

---

## 4. Sections of the report

The template renders the following, in this order.
1. **Cover:** company, the one-line verdict, the score with its reading band, coverage and reliability, each with a one-line explanation.
2. **Executive summary:** key findings and the first actions.
3. **How to read this report:** fixed text supplied by the template. Do not restate it in the data.
4. **Score by dimension:** a bar for each of the eight dimensions with its plain description, the score and the reason.
5. **What works.**
6. **Main problems.**
6a. **Social media** and **Promise and perception** (deep mode): one row per official account analysed; the review layer with its sample, caveat and themes. Reviews never enter the score (`source-collection.md` §7). Red flags are folded into the problems as "common mistake" names; there is no separate red-flag section.
7. **Plan:** the three most important fixes, each marked as possible with existing material or as needing new information.
8. **Before → after.**
9. **Questions for the company:** every CONFIRM and EVIDENCE NEEDED item in one checklist, grouped by purpose.
9a. **What to add for the full picture** (when `manual_import` is not empty): the closed-platform accounts and what to capture.
10. **Appendix:**
    - the source map (deep mode): every source found, its decision and the reason;
    - the sources, when material was collected from the web: title, type, capture date and a link for each page;
    - the genericity test table;
    - the claims-and-proof table;
    - criterion-level scores;
    - the materials reviewed.

For a partial audit (confidence LOW), set `provisional: true` and add a notice that names what the audit covers and what it does not. For a withheld score, set `withheld: true` and omit `value`. In that case:
- fill `dimensions` only with what can be assessed;
- use `summary`, `questions` and `notices` to say what a full audit needs.

---

## 5. Reader-facing structure in chat (fallback)

When the audit is given in the chat (section 2.2), use the same order as section 4, with plain headings in the reader's language:
- cover line;
- summary;
- a three-line "how to read" note (scale and bands, coverage, reliability);
- scorecard as a short table (dimension, score, reason);
- what works;
- main problems;
- plan;
- before → after;
- questions;
- a short appendix.

Use the vocabulary in section 6. Never use sub-criterion codes or English labels.

---

## 6. Reader-facing writing rules

These rules apply to every prose field, the chat summary and the chat fallback. They come on top of the tone and evidence rules in `output-contracts.md` §0.3–0.4.

### 6.1 No internal vocabulary

**Never write internal codes in reader-facing text** (codes belong only in coded data fields such as `flags`):
- sub-criterion codes (CL1, PR3, DI1…);
- decision-tree steps (Q1–Q6);
- red-flag numbers (RF01–RF24);
- touchpoint codes (T1–T8);
- English status words (SUPPORTED, UNVERIFIED, GENERIC, HIGH…);
- `RELATIONSHIP: UNRESOLVED`, PR1 arithmetic, "assessable points", "anchor".

Put the meaning in plain words instead:
- Instead of `RELATIONSHIP: UNRESOLVED (PERIOD) — CONFIRM`, write "It is unclear whether the 2025 figure still holds today" and add the item to `questions` as `confirm`.
- Instead of "PR1 = 2", write "only one of five claims has meaningful support".
- Instead of "survives substitution", write "fits any comparable employer unchanged".

**Use the reader-facing names of the dimensions:**

| Dimension | English | Russian |
|---|---|---|
| Clarity | Clarity | Ясность |
| Differentiation | Differentiation | Отличие от других |
| Proof | Proof | Доказательства |
| Audience Fit | Audience fit | Попадание в аудиторию |
| Employee Truth | Employee voice and work reality | Голос сотрудников и реальность работы |
| Consistency | Consistency | Согласованность |
| Candidate Relevance | Candidate questions answered | Ответы на вопросы кандидата |
| Conversion | Path to applying | Путь к отклику |

### 6.2 Voice

- **No first person and no gendered self-reference.**
  - Russian: never «я оценивал», «я бы заменил».
  - English: avoid "I".
  - Use impersonal or material-centred sentences: «В материалах нет…», «Аудит не учитывает…», "The material does not show…".
- **Address the company as "you".** Use «вы» in Russian. This is the reader's own company unless the user said otherwise.
- **Do not narrate the method.** Skip "I treated", "the audit counts", "by your words". State the finding.

### 6.3 Plain, human sentences

Write the way a sharp colleague explains a finding across the table.
- **One idea per sentence.** Short sentences. Concrete subjects and verbs.
- **No staged contrasts.** Skip "this is not X, it is Y" and "not a contradiction, however…". If something is unclear, say what is unclear.
- **No arguing with no one.** Skip "This is not to say", "To be clear", «Это не противоречие, однако».
- **No dashes as all-purpose connectors.** Use a full stop, comma or colon. Keep a dash only inside quoted material and number ranges.
- **No forced lists of three.** No closing one-liners that repeat the point. No rhetorical questions.
- **No inflated words or stock phrases:**
  - English: crucial, key (as an adjective), robust, leverage, showcase, highlight (as a verb), underscore, pivotal, landscape, "it is worth noting", "plays a role";
  - Russian: ключевой, важно отметить, стоит отметить, играет роль, является, данный, осуществлять, в рамках, на текущий момент, позволяет (as a filler), «наследует», «сущность», «профиль» (meaning the score pattern).
- **No bold run-in labels** on every bullet. Use a label only when it names a field the reader needs to find.
- **Numbers and quotations do the work.** Prefer "salary range 62–78 thousand roubles take-home, paid twice a month" to "transparent pay".
- **Before finishing, reread every prose field once with these rules.** Rewrite any sentence that would sound odd if said out loud to the reader.

### 6.4 One consistent story

- Every comparative statement in prose ("the best-supported promise", "the strongest material", "the weakest dimension") must agree with the ledger statuses, strengths and dimension scores. If growth is WEAKLY SUPPORTED and craft is PARTIALLY SUPPORTED, no sentence may say growth is the best supported. Check every superlative against the data before writing the file.
- Say each fact once in detail, in the section where it does its work (what works, a problem, a fix). The summary and the verdict refer to it briefly. Do not repeat the same figures and quotations across the summary, strengths, problems and plan.
- State the scope of the audit once, plainly, in `scope`. Do not repeat absence-of-evidence disclaimers in every section; the fixed "How to read" text already explains the rule. Use the disclaimer in prose only where a reader could otherwise take a gap for a fact about the company.

### 6.5 Plan items the reader can act on

For each fix, give its effort, who needs to be involved and what to watch afterwards. Effort and roles are recommendations about the work; "what to watch" names observable signs (for example "the number of responses to the café manager vacancy", "whether candidates ask about pay at the first call") and never predicts a result or a number.

### 6.6 Explain every judgement in candidate terms, about the material

Each reason names what in the material caused the judgement:
- a quotation;
- a missing fact;
- a contradiction between two documents.

Keep the evidence rules: no claims about how candidates react, no market comparisons (`evidence-rules.md` §8).
