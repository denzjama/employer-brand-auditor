# Demo — Employer Brand Auditor

This demo shows a full employer-brand audit of a **fictional** company, Quellmoor Lift & Access, a regional lift and escalator maintenance firm. The case is deliberately neither ideal nor terrible:
- it has real specifics: a service portfolio, an apprenticeship practice, on-call terms and an honest employee story;
- it also has stock employer-brand phrases, a job ad without a pay figure, and a "flexible working" claim that sits uneasily with a field role's on-call rota.

## Files

| File | Content |
|---|---|
| [`demo-company-materials.md`](demo-company-materials.md) | The five fictional candidate-facing materials: careers intro, employer proposition, two job ads, employee story |
| [`demo-prompt.md`](demo-prompt.md) | The exact prompt used |
| [`demo-output.md`](demo-output.md) | The chat reply, **exactly as returned by a real run. Not edited** |
| [`demo-report.html`](demo-report.html) | The HTML report the same run wrote. **Not edited.** Open it in a browser |

## How the output was produced

| Item | Value |
|---|---|
| Plugin | Employer Brand Auditor **v0.2.0** |
| Claude Code | 2.1.304 (Claude Code) |
| Model | `claude-opus-5-5` |
| Skill used | `employer-brand-auditor:employer-brand-audit` (selected automatically) |
| Run date (UTC) | 2026-10-22 |
| Input | The prompt in `demo-prompt.md`, then two line breaks, then the full contents of `demo-company-materials.md` |
| Tools available to the session | Read, Glob, Grep, Skill and Write (to save the report); no web access |
| Runs | One run. This is the first valid run; nothing was rerun or selected |
| SHA256 of the prompt | `fabc498947034a8a404fb6ad6792042fc2c37693edbef1e150cfc3cac0bd42a2` |
| SHA256 of the materials | `8b590eeb13d411f92e55b6ad447f11b2b9eabe0c72b2ead06ca7acdc5d2a6e7c` |
| SHA256 of the chat reply | `0e4f1c8363cc5776a2321ca68863873b4ae53c9b596def4d10869b73837592d8` |
| SHA256 of the report | `298b94d73ad547e9df016caa344c55f60b60e8c0f907819b155864f14b4ad22e` |

**Both files are reproduced byte for byte.** The link to the report at the end of the chat reply points to the temporary folder the demo ran in; the same file is `demo-report.html` here.

The same materials scored 63/100 with v0.1.4 as well. v0.2.0 changes how the result is presented, not how it is scored.

## Try it yourself

Paste the prompt from `demo-prompt.md` and the contents of `demo-company-materials.md` into Claude Code with the plugin loaded. Your result will follow the same structure and should reach a broadly similar diagnosis. It will not be word-for-word identical, because model outputs vary between runs.
