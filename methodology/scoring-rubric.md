# Scoring Rubric — Canonical Employer Brand Score

This file is the single source of truth for the Employer Brand Score. Skills reference it; they do not redefine it. Weights total exactly 100 and are checked by `scripts/validate_plugin.py`.

The score is a structured expert judgement made transparent, not a measurement instrument. Present it with that modesty: whole numbers only, no decimals, no claims of statistical validity, no percentile language.

---

## 1. Procedure overview

1. **Inventory** the supplied material: list each touchpoint, its type (T1–T8, see `terminology.md`), its apparent audience and whether it is candidate-facing.
2. **Decide assessability** for every sub-criterion (section 4) *before* scoring anything. Record NOT ASSESSABLE decisions with a one-line reason.
3. **Gate on coverage.** Compute coverage. If coverage is below 40%, the headline score is SCORE WITHHELD (section 6).
4. **Extract material claims** using the fixed sequence in `evidence-rules.md` §1 (read → list promises → merge duplicates → classify CORE / SUPPORTING / HYGIENE → select 3–8 material claims). Hygiene facts are set aside for Candidate Relevance, Conversion and Clarity.
5. **Build the Claim → Proof Ledger** for the material claims only (`evidence-rules.md` §3), and run the **Genericity Test** (`genericity-test.md`) on the core claims. Proof and Differentiation reasons must refer to these artefacts.
6. **Score** each assessable sub-criterion using the anchors in section 3. Award whole points only. Every awarded score needs a one-line reason tied to the supplied material. Score each dimension on its own anchors (section 5: no cross-dimension caps).
7. **Calculate** score, coverage and confidence (section 6). Show the arithmetic.
8. **Self-check** (section 8).

---

## 2. Dimension weights

| Dimension | Max | Sub-criteria |
|---|---|---|
| Clarity | 12 | CL1–CL4 |
| Differentiation | 16 | DI1–DI5 |
| Proof | 16 | PR1–PR4 |
| Audience Fit | 12 | AF1–AF4 |
| Employee Truth | 10 | ET1–ET4 |
| Consistency | 12 | CO1–CO4 |
| Candidate Relevance | 12 | CR1–CR4 |
| Conversion | 10 | CV1–CV5 |
| **Total** | **100** | 34 sub-criteria |

---

## 3. Sub-criteria and anchors

Anchors describe the top, middle and bottom of each scale. Intermediate whole numbers are allowed when the material sits between anchors. Do not award a point "for effort": score what a candidate would actually get from the material.

### 3.0 Anchor-faithful scoring (binding)

- **Lower-anchor rule.** When the evidence falls materially between two anchors, award the **lower** score unless every requirement of the higher anchor is clearly satisfied by something you can point to in the material.
- No automatic rounding up, no benefit of the doubt, and no points because a text is professionally written. Polish is not clarity, differentiation, support or relevance.
- **Each reason must name the observable evidence that meets the anchor** (a fact or a location in the material, paraphrased with its anchors, or a complete-sentence quote). A reason that only restates the anchor's words is not sufficient.
- **The reason must not contradict the score.** If the explanation says "no core claim breaks under substitution", DI1 cannot sit in the 3–4 band.

Pay particular attention to Clarity and Differentiation (see the operational notes under CL1, DI1 and DI5).

### CLARITY — 12

#### CL1 · Employer proposition identifiable · 4
Question: after one read, can a candidate say in one sentence what this employer offers people?
- **4** — A single, restatable offer is evident within the first screen or first paragraph of the **candidate-facing** material, and the restatement would be about *working here*, not about the company's products. An offer stated only in an internal EVP document, and not carried into what candidates read, cannot score 4.
- **2–3** — An offer exists but is buried, split between competing ideas, or has to be reconstructed from several places.
- **1** — Only fragments: a slogan plus scattered perks or values with no connecting idea.
- **0** — No identifiable offer; the material only describes the company, its values or its ambitions.

#### CL2 · Candidate benefit explicit · 4
Question: does the material state what the employee gets or experiences, rather than what the company is?
- **4** — Benefits are expressed from the candidate's side ("you will…", "you get…") and are concrete.
- **2–3** — Some candidate benefits, mixed with large amounts of company self-description.
- **1** — Benefits are implied only; the reader must infer what is in it for them.
- **0** — Company-first throughout (RF04).

#### CL3 · Message hierarchy · 2
Question: is there a recognisable central message with supporting points beneath it?
- **2** — One lead idea; pillars or sections visibly support it.
- **1** — Several ideas of equal weight; or a lead idea that the rest of the material ignores.
- **0** — No hierarchy; a list of unconnected claims.

#### CL4 · Accessibility · 2
Question: is the language understandable, specific and reasonably free of internal jargon?
- **2** — Plain, specific language a candidate outside the company understands.
- **1** — Some jargon, acronyms or abstract corporate language that slows comprehension.
- **0** — Dense internal jargon or abstraction that blocks understanding (RF19).

### DIFFERENTIATION — 16

#### DI1 · Competitor substitution resistance · 5
Question: if the employer name were replaced by a comparable competitor's, would the central message stop being plausible?
- **5** — Central claims break under substitution: they depend on named assets, places, constraints, practices or numbers unique to this employer.
- **3–4** — Some central claims break under substitution; others survive unchanged.
- **1–2** — Most central claims survive substitution; specificity only in secondary detail.
- **0** — The material could be published unchanged by almost any employer in the category.
The reason must cite the Genericity Test verdicts for the core claims and **name which core claims break under substitution**. Operational rule: no core claim breaks → DI1 ≤ 2 (2 only if specific, employer-tied detail appears in secondary material); at least one core claim breaks but others survive → 3–4; all core claims break → 5.

#### DI2 · Category cliché resistance · 3
Question: does the material avoid relying mainly on stock category claims from the genericity-test lexicon (growth, innovation, great people, challenging work, impact, dynamic culture, family)?
- **3** — Clichés absent or incidental; the argument rests on specific content.
- **2** — Clichés present but supported or outweighed by specific material.
- **1** — Clichés carry most of the argument.
- **0** — The material is essentially a sequence of clichés.

#### DI3 · Employer-specific advantages · 4
Question: does the proposition use specific assets, realities, capabilities or characteristics of this employer?
- **4** — Several specific, relevant employer realities are used as the basis of the offer.
- **2–3** — One or two specific realities, or specifics present but not connected to the offer.
- **1** — Specifics exist only as company facts (size, founding year) with no link to the employee experience.
- **0** — No employer-specific content.

#### DI4 · Defensibility · 2
Question: would it be difficult for competitors to make the same promise honestly?
- **2** — The promise rests on something structural (location, mission-critical service, a practice with cost or constraint) that others cannot honestly copy.
- **1** — Partly defensible; others could claim it with some effort.
- **0** — Anyone could claim it honestly or dishonestly with no cost.

#### DI5 · Memorability · 2
Question: is there a meaningful and recognisable idea worth remembering? Score the idea as candidates encounter it: a line that appears only in an internal document, or only once, scores at most 1.
- **2** — A distinct idea a candidate could repeat to a friend, and it means something about the work.
- **1** — Memorable phrasing without substance, or substance without a memorable idea.
- **0** — Nothing to remember.

### PROOF — 16

Proof evaluates how well the **material employer claims** (CORE and SUPPORTING claims selected in `evidence-rules.md` §1) are supported by evidence that candidates can see in the audited material. Hygiene facts (pay, hours, holiday, standard benefits, address, application steps) are not material claims and do not raise Proof, however precise they are — they are scored under CR3, CV and CL2. USER-SUPPLIED facts stated in conversation do not raise Proof for the audited material (`evidence-rules.md` §3.3).

**Meaningful support** means a ledger status of STRONGLY or PARTIALLY SUPPORTED (support strength STRONG or MODERATE, `evidence-rules.md` §2.2). WEAKLY SUPPORTED claims have relevant but insufficient evidence; they do not count as meaningful support. The anchors below make Proof low whenever no material claim has meaningful support, without any cross-dimension cap: PR1 ≤ 1 and PR2–PR4 ≤ 1 each in that case.

#### PR1 · Claim evidence coverage · 6
Question: how many of the material claims — and which ones — have meaningful support in the audited material? PR1 is **not** a ratio: deleting or ignoring unsupported claims does not raise it. Count the claims as the material makes them; an unsupported core claim always counts against PR1. Importance matters: core claims weigh more than supporting claims.
- **6** — Nearly all material claims, including every core claim, are STRONGLY SUPPORTED.
- **5** — Most material claims (including most core claims) are STRONGLY SUPPORTED.
- **4** — Most material claims have meaningful support (STRONGLY or PARTIALLY SUPPORTED), including most core claims.
- **3** — Several material claims are PARTIALLY SUPPORTED, **or** one important core claim is STRONGLY SUPPORTED while most others lack meaningful support.
- **2** — A minority of claims (one or two, not the most important) have partial support; most core claims lack meaningful support.
- **1** — Only isolated WEAK evidence exists; no claim has meaningful support.
- **0** — No material claim has any meaningful supporting evidence, and none has even weak evidence.

Operational procedure: (a) list core claims in order of prominence, then supporting claims; (b) mark each STRONGLY / PARTIALLY / WEAKLY / UNSUPPORTED / CONFLICTING (CONFLICTING counts as no support); (c) pick the highest anchor whose words are fully satisfied, applying the lower-anchor rule (§3.0); (d) state which claims drove the score.

**Scaling PR2–PR4 with the supported claim set.** Let M be the number of material claims in the ledger and S the number with meaningful support (STRONGLY or PARTIALLY SUPPORTED). PR2–PR4 judge the quality of evidence *across the claim set*, so a single excellent proof point cannot lift them high when most claims lack support. Use these anchors; when S is between anchors, apply the lower-anchor rule (§3.0).

#### PR2 · Evidence specificity · 4
Question: across the material claims, how concrete and specific (checkable in principle) is the meaningful support?
- **4** — Most material claims (S ≥ most of M, including most core claims) have meaningful support, and that support is mostly STRONG: numbers with scope and timeframe, named programmes with participation, mechanisms with outcomes.
- **3** — At least half of the material claims have meaningful support; the support is a mix of STRONG and MODERATE.
- **2** — Only a minority of material claims (one or two of several) have meaningful support, however specific that support is; **or** about half have support that is mostly MODERATE.
- **1** — No material claim has meaningful support; only WEAK evidence exists (adjectives, generic testimonials, unexplained awards).
- **0** — No evidence for any material claim.

#### PR3 · Evidence relevance · 3
Question: across the material claims, does the meaningful support demonstrate the claims it is offered for, at the right scope? Precise evidence for a different claim is irrelevant here.
- **3** — Meaningful support demonstrates most of the material claims, at the scope they are made.
- **2** — Meaningful support demonstrates some of the claims, or demonstrates most claims only at a narrower scope.
- **1** — Meaningful support demonstrates only one of several claims; **or** there is no meaningful support and the only evidence is weak or demonstrates something else (e.g. product scale offered for career growth).
- **0** — No evidence for any material claim.

#### PR4 · Claim/evidence proximity · 3
Question: across the material claims, can the candidate easily connect each promise to the evidence that meaningfully supports it?
- **3** — For most material claims, meaningful support sits next to the claim.
- **2** — For several claims, meaningful support sits in the same touchpoint but separated from the claim; or it sits next to the claim for only some claims.
- **1** — Meaningful support exists for only one of several claims, or only in a different touchpoint, or the only evidence is weak.
- **0** — No evidence for any material claim.

Worked example (abstract; no evaluation fixture has this shape): eight material claims — three CORE and five SUPPORTING; no contradictions. One CORE claim is STRONGLY SUPPORTED; two SUPPORTING claims are PARTIALLY SUPPORTED; the other two CORE claims are WEAKLY SUPPORTED and three SUPPORTING claims are UNSUPPORTED (S = 3, M = 8). Each supported claim has its evidence in the same paragraph. → PR1 3 (one important core claim strongly supported, most others without meaningful support), PR2 2 (a minority of claims supported, however specific), PR3 2 (support demonstrates some of the claims), PR4 2 (support sits next to the claim for only some claims) = 9/16.

### AUDIENCE FIT — 12

#### AF1 · Audience definition · 3
Question: is it reasonably clear which candidate audience the communication addresses?
- **3** — Target audience is explicit or unmistakable from content (role family, seniority, motivations).
- **2** — Audience is inferable but not consistently addressed.
- **1** — Several possible audiences, none clearly served.
- **0** — Addressed to "everyone" (RF08).

#### AF2 · Motivation relevance · 4
Question: does the material address likely decision factors for that audience?
- **4** — Addresses the factors this audience is likely to weigh for this kind of role (reasoned from the role, never from invented survey data) (e.g. pay, shift pattern and progression for operational roles; technical problems, autonomy and tooling for engineers), with specifics.
- **2–3** — Some relevant factors, others ignored or covered only generically.
- **1** — Factors addressed are mostly what the company wants to say, not what the audience needs.
- **0** — No relevant decision factors addressed.
Judge "likely decision factors" from the role and context in the material and from professional reasoning; never cite invented survey statistics to justify them.

#### AF3 · Segmentation · 3
Question: where materially different audiences exist, is the proposition appropriately adapted?
- **3** — Distinct audiences receive adapted messages built on a shared core.
- **2** — Some adaptation; one audience well served, another treated generically.
- **1** — Different audiences receive identical messaging where their decision factors clearly differ (RF09).
- **0** — Messaging actively mismatches an audience.
Assessable only when the material targets, or clearly should target, more than one materially different audience (see section 4).

#### AF4 · Trade-offs · 2
Question: does the proposition represent meaningful choices rather than appealing equally to everyone?
- **2** — Makes explicit choices that will deter some candidates and attract the right ones.
- **1** — Choices implied but softened or hidden.
- **0** — Tries to be everything to everyone.

### EMPLOYEE TRUTH — 10

#### ET1 · Employee voice · 3
Question: is there authentic employee perspective rather than only corporate narration?
- **3** — Attributable employees describe concrete experiences in their own words.
- **2** — Employee voice present but polished, short or generic in places.
- **1** — Token quotes ("I love working here").
- **0** — No employee voice (RF10).

#### ET2 · Work reality · 3
Question: does the communication reveal what working there actually looks like?
- **3** — Concrete tasks, schedules, tools, conditions, team set-up or pace.
- **2** — Some concrete reality, mostly at a high level.
- **1** — Work described only in aspirational terms.
- **0** — No work reality (RF11).

#### ET3 · Tensions and trade-offs · 2
Question: is there useful reality or honest complexity rather than only polished claims?
- **2** — Names real difficulties, demands or downsides and how they are handled.
- **1** — Hints at difficulty ("fast-paced") without specifics.
- **0** — Uniformly polished (RF24).

#### ET4 · Behaviour over adjectives · 2
Question: is culture demonstrated through practices and behaviour rather than adjectives?
- **2** — Culture shown through concrete practices, rituals, decisions or policies.
- **1** — Some practices, mostly adjectives.
- **0** — Culture described only with adjectives (RF07).

### CONSISTENCY — 12

Consistency is NOT ASSESSABLE from a single touchpoint. Never award zero for lack of a second touchpoint.

#### CO1 · Core promise alignment · 5
Question: do multiple touchpoints communicate a coherent proposition?
- **5** — Every touchpoint expresses or supports the same core promise.
- **3–4** — Most touchpoints align; one drifts or ignores the promise.
- **1–2** — Touchpoints tell different stories, or the promise appears only in the EVP and nowhere else (RF23).
- **0** — Touchpoints directly undercut the core promise.

#### CO2 · Proof alignment · 3
Question: does evidence across materials support the same employer story?
- **3** — Proof in different touchpoints reinforces the same story.
- **2** — Proof supports parts of the story; some proof is off-story.
- **1** — Proof in one touchpoint is irrelevant to the promise made in another.
- **0** — Evidence in one touchpoint contradicts another touchpoint's promise.

#### CO3 · Tone and message coherence · 2
- **2** — Recognisably the same employer speaking across touchpoints.
- **1** — Noticeable tonal or message drift.
- **0** — Touchpoints sound like unrelated organisations.

#### CO4 · Contradiction resistance · 2
- **2** — No material contradictions found between touchpoints.
- **1** — Minor or ambiguous tensions.
- **0** — At least one material contradiction (RF12).

### CANDIDATE RELEVANCE — 12

#### CR1 · Why join · 3
Question: does the material answer why a candidate should consider this employer?
- **3** — A clear, specific reason to choose this employer, from the candidate's perspective.
- **2** — Reasons given, but generic or only partly relevant.
- **1** — The reader has to construct the reason themselves.
- **0** — No reason to join beyond "we are hiring".

#### CR2 · Work and role reality · 3
Question: can the candidate picture the role: what they will do, with whom, under what conditions?
- **3** — Role content, team, conditions and expectations are concrete.
- **2** — Partly concrete; key elements missing.
- **1** — Responsibilities listed in abstract terms only.
- **0** — No role reality.

#### CR3 · Relevant decision factors · 3
Question: are the facts a candidate needs to decide present (pay or pay logic, location and work mode, schedule, contract type, progression path, as relevant)? This is where precise hygiene facts earn credit.
- **3** — The key decision facts for this audience are present.
- **2** — Some present; at least one important factor missing.
- **1** — Only generic statements ("competitive salary").
- **0** — None present.

#### CR4 · Candidate questions and friction · 3
Question: does the material anticipate the questions and doubts a serious candidate would have?
- **3** — Addresses likely objections or uncertainties directly (requirements flexibility, what is hard, how decisions are made).
- **2** — Some questions anticipated.
- **1** — Questions left open; candidate must ask or guess.
- **0** — Material raises doubts it does not address.

### CONVERSION — 10

#### CV1 · Next-step clarity · 3
- **3** — The candidate knows exactly what to do next and where.
- **2** — A next step exists but is vague or hard to find.
- **1** — Only a generic "apply" with no context.
- **0** — No next step (RF20).

#### CV2 · Decision support near CTA · 2
- **2** — The final reasons or key facts sit close to the CTA.
- **1** — Some support near the CTA.
- **0** — CTA is isolated from any decision support.

#### CV3 · Friction reduction · 2
- **2** — Effort is reduced or explained (time to apply, what is required, no cover letter, mobile-friendly, contact person).
- **1** — Some friction acknowledged.
- **0** — Friction ignored or increased.

#### CV4 · CTA relevance · 2
- **2** — The CTA matches the audience and stage (e.g. "talk to a crew lead" for unsure candidates; "apply in 5 minutes" for ready ones).
- **1** — Generic CTA.
- **0** — Mismatched CTA.

#### CV5 · Process transparency · 1
- **1** — Steps, timeline or what happens after applying are described.
- **0** — Not described.

---

## 4. Assessability rules

Decide assessability per sub-criterion before scoring.

### 4.1 General rules

1. **ASSESSABLE** when the supplied material is of a kind in which a candidate would reasonably expect to find the element. If the element is absent from such material, the absence is a property of the *communication* and is scored. Example: a careers page that makes promises with no proof — PR1 is assessable and scores 0. This says candidates are not shown proof; it does not say the company lacks the practice.
2. **NOT ASSESSABLE** when the supplied material type could not be expected to contain the element (an EVP statement alone has no CTA, so Conversion is not assessable), or when the criterion structurally requires something not supplied (Consistency requires at least two touchpoints).
3. **Excerpts.** If the user says material is an excerpt, mark elements likely to sit outside the excerpt as NOT ASSESSABLE and say so. If the user says "this is our full careers page" or "this is everything", absences inside it are scorable.
4. **Never** mark NOT ASSESSABLE to spare the employer a low score. **Never** score 0 to avoid the work of deciding assessability.
5. **Partial dimensions are allowed.** A dimension can have some sub-criteria assessable and others not; only the assessable ones enter the calculation.
6. **State every NOT ASSESSABLE decision** in the scorecard with a short reason.

### 4.2 Assessability by material type

Y = all sub-criteria normally assessable; P = some (see notes); N = normally not assessable.

| Material supplied (alone) | CL | DI | PR | AF | ET | CO | CR | CV |
|---|---|---|---|---|---|---|---|---|
| Slogan / tagline only | P¹ | Y | N | N | N | N | N | N |
| EVP statement or platform | Y | Y | Y | P² | P³ | N | P⁴ | N |
| Careers page | Y | Y | Y | P² | Y | N | Y | Y |
| Single job ad | Y | Y | Y | P² | Y | N | Y | Y |
| Recruitment post / campaign asset | Y | Y | Y | P² | P³ | N | P⁴ | Y |
| Employee stories only | P¹ | Y | Y | P² | Y | N | P⁴ | N |
| Candidate email | P¹ | P | P | P² | N | N | P⁴ | Y |
| Internal EB strategy deck only | Y | Y | Y⁵ | Y | P³ | N | P⁴ | N |
| Two or more touchpoints | Y | Y | Y | P² | Y | Y | Y | P⁶ |

Notes:
1. For a slogan only, assess CL1, CL2 and CL4; CL3 (hierarchy) needs more than one line and is NOT ASSESSABLE. For employee stories only or a candidate email, CL1–CL2 are assessable as "does this asset convey the offer"; CL3 only if the asset has structure.
2. **AF3 Segmentation** is assessable only when the material targets more than one materially different audience, or when the user states the employer recruits materially different audiences and supplies material intended for them. If the material deliberately targets one audience (a single job ad), AF3 is NOT ASSESSABLE. AF1, AF2 and AF4 are normally assessable.
3. ET1 (employee voice) is NOT ASSESSABLE for a short-form asset (an EVP line, a single social post) where employee voice is not expected; ET2–ET4 remain assessable if the asset describes culture or work.
4. CR2–CR3 (role reality, decision factors) are assessable only where a candidate would expect them: job ads, careers pages, role-specific campaigns. For an EVP statement, assess CR1 and CR4 only.
5. Internal decks: proof that appears only in the deck is *available but unpublished*. Score PR as the deck presents it, then state clearly in the audit that candidates cannot see this proof unless it is published (see `evidence-rules.md` §6).
6. Conversion is assessable for candidate-facing touchpoints that are meant to drive action (careers page, job ad, campaign, email). If the set contains only an EVP and employee stories, Conversion is NOT ASSESSABLE.

---

## 5. Dimension independence (no cross-dimension caps)

Each dimension is scored only on its own anchors. Version 0.1.0 contained five "dependency caps"; the v0.1.1 calibration removed them because the baseline evaluation showed that caps tied to another dimension's borderline sub-score, to the presence of one trivial benefit, or to an ambiguously defined "central claim" produced discontinuous jumps (e.g. a one-point CL1 judgement moving CO1 by two points on identical material).

Dimensions are conceptually orthogonal. These combinations are legitimate and must be scored as they are:
- **highly consistent but generic** — high Consistency, low Differentiation;
- **clear but unsupported** — high Clarity, low Proof;
- **specific but irrelevant** — some Differentiation, low Candidate Relevance;
- **relevant but poorly differentiated** — good Candidate Relevance, low Differentiation.

Do not lower one dimension because another is weak. Explain the combination in prose instead (e.g. "the material is consistent, but consistently generic").

What replaced the old caps:
- **Contradictions** are scored by the Consistency anchors themselves: CO4 = 0 when there is at least one material contradiction (RF12); CO1 and CO2 anchors already score touchpoints that undercut the promise or each other at 0–2. No extra ceiling is applied.
- **CONFLICTING evidence** counts 0 in PR1 — this is part of the PR1 counting rule, not a cap.
- **Genericity and Differentiation**: DI1 and DI4 reasons must cite the Genericity Test verdicts for the core claims, so the two artefacts agree by reasoning, not by a ceiling.
- **No evidence**: if no material claim has any evidence, the PR2–PR4 anchors already give 0 ("No evidence for any material claim"). A trivial hygiene fact cannot change this, because hygiene facts are not material claims.

The only gate in the rubric is the **coverage gate** (section 6.2): below 40% coverage no headline score is produced.

---

## 6. Calculation

```
EARNED          = sum of awarded points on ASSESSABLE sub-criteria
MAX_ASSESSABLE  = sum of maximum points of ASSESSABLE sub-criteria
SCORE           = round(EARNED / MAX_ASSESSABLE × 100)
COVERAGE        = round(MAX_ASSESSABLE / 100 × 100) %
```

Rounding: compute with full precision, round once at the end, halves round up (57.5 → 58).

### 6.1 Confidence

| Confidence | Rule |
|---|---|
| HIGH | Coverage ≥ 80% **and** at least three materially different touchpoint types (T1–T8) supplied |
| MEDIUM | Coverage 60–79%; **or** coverage ≥ 80% with fewer than three touchpoint types |
| LOW | Coverage < 60% — label the score **PROVISIONAL** |

The second MEDIUM condition is a deliberate design choice: high coverage from one or two touchpoint types (for example a careers page and one job ad) leaves too much of the candidate journey unseen to justify HIGH confidence.

### 6.2 Minimum coverage gate

If coverage is below **40%**, do not publish a headline Employer Brand Score. Output **SCORE WITHHELD — INSUFFICIENT COVERAGE**, show the assessable sub-scores if useful, explain which materials would make a full audit possible, and offer the narrower workflow that does fit (usually `evp-stress-test` for a slogan or EVP line, `career-content-review` for one asset).

Example: a slogan alone makes CL1, CL2, CL4 and DI1–DI5 assessable = 4 + 4 + 2 + 5 + 3 + 4 + 2 + 2 = 26 points. Coverage 26% → SCORE WITHHELD.

### 6.3 Worked example

Material: a careers page and one job ad (types T2, T3). Consistency assessable (two touchpoints). AF3 not assessable (single audience). ET1 assessable.

- Maximum assessable = 100 − 3 (AF3) = 97 → Coverage 97%.
- Earned (illustrative): CL 8, DI 7, PR 9, AF 6 (of 9), ET 5, CO 9, CR 8, CV 6 = 58.
- Score = 58 / 97 × 100 = 59.79 → **60/100**.
- Confidence: coverage ≥ 80% but only two touchpoint types → **MEDIUM**.

Display the arithmetic in the output: "Earned 58 of 97 assessable points → 60/100. Coverage 97%. Confidence MEDIUM (two touchpoint types)."

---

## 7. Reading the score

These bands are reading aids for this rubric only. They are **not** market benchmarks, percentiles or comparisons with other employers, and must never be presented as such.

| Score | Reading |
|---|---|
| 85–100 | Distinctive, well supported, candidate-centred. Remaining issues are refinements. |
| 70–84 | Strong with identifiable, fixable gaps. |
| 50–69 | Functional but generic or under-supported in important places. |
| 30–49 | Weak: the material gives candidates few specific reasons or little proof. |
| 0–29 | No functioning proposition is visible in the supplied material. |

A PROVISIONAL score is read with the band *and* the coverage caveat.

---

## 8. Self-check before output

- [ ] Every sub-criterion is either scored or marked NOT ASSESSABLE with a reason.
- [ ] No NOT ASSESSABLE sub-criterion contributes zero to the calculation.
- [ ] Dimension subtotals add up; total earned matches the sum of subtotals.
- [ ] Maximum assessable equals 100 minus the maxima of NOT ASSESSABLE sub-criteria.
- [ ] Score and coverage are rounded once, at the end.
- [ ] Confidence follows section 6.1, including the touchpoint-type condition.
- [ ] Material claims (3–8 for a full audit) were extracted before evidence was judged; hygiene facts were kept out of the ledger and PR1.
- [ ] PR1 matches the ledger arithmetic; every ledger status follows the strength → status mapping.
- [ ] DI1/DI4 reasons cite the Genericity Test verdicts and name which core claims break; no dimension was lowered because another dimension was weak.
- [ ] Every borderline sub-score took the lower anchor unless the higher anchor's requirements are visibly met; no reason contradicts its score.
- [ ] PR1 was assigned by the operational anchor rule, not a ratio; PR2–PR4 were scaled to the supported claim set (S of M), so one strong proof point did not lift them.
- [ ] Each score's reason refers to something in the supplied material, not to general assumptions about the employer.

---

## 9. Changing the rubric

Adding, removing or reweighting a dimension or sub-criterion requires, in the same change: this file, the relevant skills, `output-contracts.md`, the eval cases and fixture expectations in `evals/`, and a passing run of `scripts/validate_plugin.py`, which checks that weights total 100.
