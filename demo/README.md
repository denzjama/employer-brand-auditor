# Demo — Employer Brand Auditor

This demo shows a full employer-brand audit of a **fictional** company, Quellmoor Lift & Access, a regional lift and escalator maintenance firm. The case is deliberately neither ideal nor terrible:
- it has real specifics: a service portfolio, an apprenticeship practice, on-call terms and an honest employee story;
- it also has stock employer-brand phrases, a job ad without a pay figure, and a "flexible working" claim that sits uneasily with a field role's on-call rota.

## Files

| File | Content |
|---|---|
| [`demo-company-materials.md`](demo-company-materials.md) | The five fictional candidate-facing materials: careers intro, employer proposition, two job ads, employee story |
| [`demo-prompt.md`](demo-prompt.md) | The exact prompt used |
| [`demo-output.md`](demo-output.md) | The auditor's output, **exactly as returned by a real run. Not edited** |

## How the output was produced

| Item | Value |
|---|---|
| Plugin | Employer Brand Auditor **v0.1.4**, loaded from its release package. v0.1.5 changes only manifest metadata (licence and author); its skills and methodology are byte-identical to v0.1.4, so the demo applies unchanged |
| Claude Code | 2.1.282 (Claude Code) |
| Model | `claude-opus-5-5` |
| Skill used | `employer-brand-auditor:employer-brand-audit` (selected automatically) |
| Run date (UTC) | 2026-10-08 |
| Input | The prompt in `demo-prompt.md`, then two line breaks, then the full contents of `demo-company-materials.md` |
| Tools available to the session | Read, Glob, Grep and Skill only (no web access) |
| Runs | One run. This is the first valid run; nothing was rerun or selected |
| SHA256 of the prompt | `fabc498947034a8a404fb6ad6792042fc2c37693edbef1e150cfc3cac0bd42a2` |
| SHA256 of the materials | `8b590eeb13d411f92e55b6ad447f11b2b9eabe0c72b2ead06ca7acdc5d2a6e7c` |
| SHA256 of the output | `2bf3a84fe170fafedb17e0bb20293894d5c70f84178ecad59d0c80379eb6c543` |

**The output is reproduced byte for byte.** It may contain small formatting quirks. For example, one sub-score row reads "2/4→2/3". These are part of what the product produced and were deliberately left in.

## Try it yourself

Paste the prompt from `demo-prompt.md` and the contents of `demo-company-materials.md` into Claude Code with the plugin loaded. Your result will follow the same structure and should reach a broadly similar diagnosis. It will not be word-for-word identical, because model outputs vary between runs.
