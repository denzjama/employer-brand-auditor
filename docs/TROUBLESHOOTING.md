# Troubleshooting

## The plugin is not detected

- **Symptom:** the skills don't run; `claude plugin list` doesn't show the plugin; the auditor's typical structure (score, coverage, confidence) never appears.
- **Why it happens:**
  - `--plugin-dir` points to the wrong folder. It must be the folder that contains `.claude-plugin/plugin.json`, not its parent or a subfolder.
  - The plugin was installed but is disabled.
  - The session was started before installation.
- **What to do:**
  1. Check that the path contains `.claude-plugin/plugin.json` and `skills/`.
  2. For a permanent install, run `claude plugin list` and `claude plugin enable employer-brand-auditor@employer-brand-auditor` if it is disabled.
  3. Start a new session.
  4. See [`INSTALL.md`](INSTALL.md).

## The skill does not trigger

- **Symptom:** you get a general answer instead of an audit, review or EVP verdict.
- **Why it happens:** skills are chosen from what you ask. A request that doesn't mention employer brand, careers, EVP, job ads or recruitment content may not match. Very short requests without any material may not match either.
- **What to do:**
  - Say what you want and what the material is, for example "Run a full employer brand audit of the materials below" or "Review this job ad".
  - Or call the skill explicitly: `/employer-brand-auditor:employer-brand-audit`, `/employer-brand-auditor:evp-stress-test` or `/employer-brand-auditor:career-content-review`.

## Too little material

- **Symptom:** many items are "not assessed", coverage is low, or the audit recommends a narrower task.
- **Why it happens:** some parts of the method need several touchpoints. Consistency, for example, cannot be judged from one page. Items the material cannot show are excluded rather than scored as zero.
- **What to do:** add materials of different types: careers page, EVP, 1–2 job ads, an employee story. For a single asset, ask for an EVP stress test or a content review instead. See [`FIRST_RUN.md`](FIRST_RUN.md).

## Score reliability is low

- **Symptom:** score reliability is low and the score is marked provisional.
- **Why it happens:** coverage is below 60%: the material did not allow most of the method to be assessed. Reliability is medium rather than high when fewer than three types of material were supplied.
- **What to do:** read the score as indicative only. Add more types of material for a firmer result. Low reliability is about the material, not a verdict on your employer brand.

## The headline score is missing

- **Symptom:** the audit says the score is withheld.
- **Why it happens:** coverage is below 40%. A headline score from so little material would be misleading, so the auditor withholds it, explains why and lists the materials it would need.
- **What to do:** supply more material, or use the narrower task it suggests (usually an EVP stress test or a content review).

## You supplied only one vacancy

- **Symptom:** a full audit request on a single job ad gives limited coverage or recommends a content review.
- **Why it happens:** one job ad cannot show your proposition across touchpoints, your employee voice or your consistency.
- **What to do:** for the ad itself, ask "Review this job ad". For a brand-level view, add your careers page, EVP and an employee story.

## You expected market benchmarking

- **Symptom:** the audit does not say whether your pay, benefits or proposition are better or worse than other employers'.
- **Why it happens:** by design. Without comparable data, the auditor makes no claims about markets, competitors or what is "typical". The score bands are reading aids, not percentiles.
- **What to do:**
  - For a comparison, supply comparable material for each employer.
  - For pay benchmarking, use a dedicated salary-survey source; it is outside this tool's scope.

## Russian sites do not open (VPN, certificates)

- **Symptom:** the report lists Russian pages as unavailable: "blocked from this network", "VPN", HTTP 451, or "certificate not trusted". hh.ru and some company sites are typical.
- **Why it happens:**
  - **VPN or foreign address.** Many Russian sites, including hh.ru, refuse connections that come from abroad or through a VPN.
  - **Certificates.** Some Russian sites use certificates issued by the Russian Trusted Root CA. Operating systems and browsers outside Russia do not trust it by default, so the connection is refused.
- **What to do:**
  - **For blocked sites:** turn the VPN off while the audit collects pages, or exclude Russian domains (for example `hh.ru`, `.ru`, `.рф`) from the VPN in its split-tunnelling settings. If you use a proxy in Russia, set it for the session: `export HTTPS_PROXY=http://host:port` before starting Claude Code.
  - **For certificate errors:** you can let the plugin trust the Russian root certificate for its own page fetches only, without changing your system. Download the root certificate from the official Gosuslugi certificates page, convert it to PEM if needed, and save it as `~/.eb-auditor/extra-ca.pem`. The plugin's fetch script then accepts sites signed by it; nothing else on your computer changes.

    ```bash
    mkdir -p ~/.eb-auditor
    ```

    ```bash
    openssl x509 -inform der -in ~/Downloads/russian_trusted_root_ca.cer -out ~/.eb-auditor/extra-ca.pem
    ```

    Trusting a root certificate is your decision: it lets that authority vouch for any site the plugin opens.
  - The plugin never turns certificate checks off and never tries to get around a block or a captcha. If a site stays closed, paste its text into the chat.

## The auditor did not find the company's pages

- **Symptom:** you named a company and the reply says nothing usable was found, or the report has low coverage.
- **Why it happens:**
  - the name is ambiguous;
  - the company has little public candidate-facing material;
  - its site blocks automatic reading;
  - web tools are not available in your environment, or you declined the permission to open pages.
- **What to do:**
  - add details: industry, city, the careers-site address;
  - allow page access when Claude Code asks;
  - or paste the pages' text.

## You expected the auditor to know the company

- **Symptom:** the audit ignores things you know are true about your company, or marks them "Information needed".
- **Why it happens:** by design, the audit uses only the supplied material, so it reflects what a candidate reading that material can see. A missing item is marked as missing evidence; it is not taken as proof that the practice is absent.
- **What to do:**
  - Add the material where that information appears.
  - Or state the fact in chat. It is then treated as user-supplied: usable, labelled, in recommendations and rewrites, but it does not raise the score of the material.

## No report file was created

- **Symptom:** you got the audit in the chat, but no HTML file appeared.
- **Why it happens:** the environment did not allow writing files (for example, file writing was denied), or you asked for the audit in the chat.
- **What to do:** allow the file write when Claude Code asks, or ask again: "Write the audit as an HTML report."

## The report says its data could not be read

- **Symptom:** the HTML file opens but shows a message that the report data could not be read.
- **Why it happens:** the audit data inside the file was written incorrectly.
- **What to do:** ask in the same conversation: "Rebuild the HTML report." The audit itself does not need to be redone.

## The report is in the wrong language

- **Symptom:** you wrote in one language and got the report in another.
- **Why it happens:** the report follows the language of the conversation. A mixed conversation can be read either way.
- **What to do:** say which language you want: "Make the report in Russian" or "in English".

## Scores differ slightly between runs

- **Symptom:** running the same audit twice gives somewhat different scores.
- **Why it happens:** the rules and arithmetic are fixed, but each criterion is judged by the model within defined anchors.
- **What to do:** compare runs on the same material using the dimension scores and the main problems, not a single point of difference in the headline score.
