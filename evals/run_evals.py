#!/usr/bin/env python3
"""Behavioural eval runner for Employer Brand Auditor.

Drives the installed Claude Code CLI non-interactively (`claude -p`), one fresh
session per case, with only this plugin's skills plus read-only file tools.
Python standard library only.

Usage (from anywhere):

    python3 evals/run_evals.py baseline [--cases TC-01,TC-07] [-j 4]
    python3 evals/run_evals.py repeatability [--runs 5] [--fixtures weak,average] [-j 4]
    python3 evals/run_evals.py extract <run-dir>      # parse scores from a repeatability run

Each invocation writes a new timestamped directory under evals/results/<suite>/.
Existing result files are never overwritten (files are opened in exclusive mode).

What the runner records per case:
  <case>.record.json   test id, exact test prompt, full message sent, expectations,
                       timestamps, exit status, session id, model, skills invoked,
                       tools used, cost, CLI arguments, stderr
  <case>.stream.jsonl  the complete raw stream-json transcript from the CLI
  <case>.response.md   the final response text

Grading (PASS / PARTIAL / FAIL) is a human or reviewer step recorded separately;
this script never grades behaviour.

Isolation notes:
  - Every case runs in its own new temporary working directory, outside the plugin
    tree, so the plugin's development CLAUDE.md is not loaded as context.
  - MCP servers are excluded (--strict-mcp-config). Tools are limited to
    Read, Glob, Grep and Skill. User-level settings and skills still load, which
    mirrors a real user's environment; the init event lists them in the record.
  - Follow-up cases (TC-22, TC-25) resume the prerequisite case's session in the
    prerequisite's working directory.
"""

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import uuid
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = EVALS_DIR.parent
FIXTURES = EVALS_DIR / "fixtures"
RESULTS = EVALS_DIR / "results"
TEST_CASES_MD = EVALS_DIR / "test-cases.md"

TOOLS = "Read,Glob,Grep,Skill"
DEFAULT_TIMEOUT = 1500
REPEATABILITY_PROMPT = "Audit our employer brand."
REPEATABILITY_FIXTURES = {
    "weak": "weak-employer.md",
    "average": "average-employer.md",
    "strong": "strong-employer.md",
    "contradictory": "contradictory-employer.md",
}

_print_lock = threading.Lock()


def log(message):
    with _print_lock:
        print(message, flush=True)


# --------------------------------------------------------------------------
# Material assembly
# --------------------------------------------------------------------------

def fixture_text(name):
    """Fixture content as a user would paste it.

    The '# Fixture: ...' title and the '> Synthetic evaluation fixture ...' notice are
    repository metadata for maintainers, not employer material, so they are removed
    (the title of the injection fixture would otherwise announce the attack).
    Everything else is sent verbatim.
    """
    lines = read(FIXTURES / name).splitlines()
    kept = []
    skipping_notice = False
    for line in lines:
        if line.startswith("# Fixture:"):
            continue
        if line.startswith("> Synthetic evaluation fixture"):
            skipping_notice = True
            continue
        if skipping_notice and line.startswith(">"):
            continue
        skipping_notice = False
        kept.append(line)
    return "\n".join(kept).strip() + "\n"


def fixture_section(name, heading_prefix):
    """Return one '## ...' section of a fixture, up to the next '---' rule or '## ' heading."""
    lines = read(FIXTURES / name).splitlines()
    out = []
    capturing = False
    for line in lines:
        if line.startswith("## "):
            if capturing:
                break
            if line.startswith(heading_prefix):
                capturing = True
        elif capturing and line.strip() == "---":
            break
        if capturing:
            out.append(line)
    if not out:
        raise SystemExit("Section {!r} not found in {}".format(heading_prefix, name))
    return "\n".join(out).strip() + "\n"


def careers_subsection(name, start_marker, end_marker):
    text = read(FIXTURES / name)
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[start:end].strip() + "\n"


# Inline materials copied verbatim from evals/test-cases.md (checked at start-up).
INLINE = {
    "TC-07": '"Grow with us."',
    "TC-17": (
        '**Engineers:** "Build the banking app 3 million members use every week. Squads of six own a '
        'feature end to end. Hybrid: two days in the Castlebridge office."\n'
        '**Branch employees:** "Be the person members trust with their biggest decisions. Every branch '
        'colleague gets 12 weeks of paid training before advising on mortgages. Branches are closed on Sundays."\n'
        '**Shared line on both:** "Meridian: a bank owned by its members."'
    ),
    "TC-19": (
        '1. "I love it here, the people are amazing." — Sam\n'
        '2. "Best company ever!" — anonymous\n'
        '3. "I moved from customer service to data analyst in 18 months. The company paid for my SQL course '
        'and my manager gave me two analysis projects before the role opened." — Lena, Data Analyst, 4 years\n'
        '4. "Everyone is so supportive and the culture is great." — Mark, Sales\n'
        '5. "Our team doesn\'t email after 6 p.m. — our manager made it a rule after a bad quarter of burnout, '
        'and it\'s stuck." — Ola, Account Manager'
    ),
    "TC-20": (
        "Competitive salary; annual bonus; private health insurance; dental cover; 25 days' holiday; birthday "
        "off; hybrid working; home-office allowance; gym discount; cycle-to-work; free breakfast on Fridays; "
        "snacks; team lunches; summer party; Christmas party; volunteering day; learning budget; pension; life "
        "assurance; employee assistance programme."
    ),
    "TC-26": (
        "Who we are: Hallbrook runs 9 distribution centres across the North-West region and employs about 2,100 "
        "people. We deliver for supermarkets, pharmacies and hospitals — if it's on a shelf or a ward in the region, "
        "there's a good chance it passed through one of our sites."
    ),
    "TC-27": (
        "Tidewater maintains 3,800 km of overhead line and 410 substations serving 140,000 homes across 26 inhabited "
        "islands and the northern coast. Most of our customers have no alternative supply. When a line goes down on "
        "an island, our crew is the only way the power comes back."
    ),
    "TC-29": (
        "**Warehouse Team Leader — Wigmoor Distribution Centre**\n"
        "**Why Hallbrook?** We're a dynamic, growing business with great opportunities for people who want to get on.\n"
        "\"I started on the picking line in 2019 and now I manage the night shift at Wigmoor. The Academy gave me my "
        "forklift licence and the team-leader course, and my manager pushed me to apply when the supervisor job came "
        "up.\" — Priya, Night Shift Manager, Wigmoor DC"
    ),
    "TC-31": (
        "**Grow with us** — We offer excellent career development and great opportunities to progress. Our people "
        "are at the heart of everything we do."
    ),
    "TC-32": (
        "**Grow with us** — 64% of our managers were promoted internally last year. We offer excellent career "
        "development and great opportunities to progress. Our people are at the heart of everything we do."
    ),
    "TC-40-AB": (
        'A. "Our mission is to make healthcare simple for everyone."\n'
        'B. "Unlimited growth with the industry\'s best people."'
    ),
    "TC-41": (
        "Brackwater Ferries runs 11 routes across the Selvan estuary with roughly 640 crew. Nearly half of our "
        "current masters joined us as deckhands. Most crossings take under 40 minutes."
    ),
    "TC-42": (
        "Halden Medical Software. Product changes are discussed in a fortnightly design forum open to all engineers. "
        "Any release that touches patient data requires sign-off from our Clinical Safety Officer. Engineers can "
        "propose experiments behind feature flags."
    ),
    "TC-43": (
        "\"On the Ravensby support desk we close most tickets the same day, though anything that reaches the overnight "
        "queue can take up to a week. That honesty is why I stayed.\" — Imani, Support Lead"
    ),
    "TC-44": (
        "Graduates in our Analytics team receive a £2,000 annual learning budget. All employees get 27 days' holiday "
        "plus public holidays. Field engineers get a company car."
    ),
    "TC-45": (
        "Fenmoor Community Hospital. Every newly qualified nurse completes a six-week preceptorship. Our ward nurse "
        "retention rate was 91% last year. We are piloting self-rostering on two wards."
    ),
    "TC-46": (
        "Orrin Logistics Software builds tools that help warehouses run. We value our people and want them to do well "
        "here. There are opportunities for the right person, and we try to make this a good place to work. "
        "Interested? Apply through our website."
    ),
    "TC-47": "Meet Tomasz, Signal Maintainer at Kelby Rail: 'I joined as a trainee in 2021. Most of my nights are spent on the Kelby–Arden line checking signal circuits before the first train. When there's a fault, my supervisor and I decide together whether to close the line — that call is never mine alone.'",
    "TC-48": 'Interview with Saoirse, Graduate Analyst, Pellmore Insurance. Q: What surprised you? A: Honestly, how much I was trusted. In my first month I presented to the pricing committee, with my manager in the room, but it was my analysis. Q: Anything hard? A: The exam load. You study for actuarial exams alongside the job, and the study days only start after six months.',
    "TC-49": "Night Pharmacy Technician — Ostra Health. You'll prepare medicines for three hospital wards between 20:00 and 08:00. Shifts are three nights per week; Saturday nights are paid at time and a quarter. Training in our aseptic unit is available after a successful 12-week probation.",
    "TC-50": 'At Quillon Labs, our 40 engineers maintain the scheduling software used by about 300 regional clinics. Every engineer joins the on-call rota after their first three months.',
    "TC-51": "Harrowgate Water: Keep the taps running. Our field teams fix around 1,200 leaks a year across the Harrow valley. You'll work in crews of three, and most call-outs are planned the day before. We back you with paid technical certification after your first year.",
    "TC-52": 'B-tree indexes keep keys sorted, so they support range queries and ordered scans; each lookup costs O(log n) page reads. Hash indexes map keys to buckets and answer equality lookups in roughly constant time, but they cannot serve range predicates. Most relational engines default to B-trees for this reason, and use hash indexes only where equality lookups dominate.',
    "TC-53": "City cycling lanes: the planner's view. 'We measured the new lane for a year before touching the next street,' said Mira Okafor, the city's transport planner. 'Traffic didn't collapse; it moved earlier in the morning.' Critics say the data covers only one corridor.",
    "TC-54": "1. 'I drive the same route every week, so I know my customers by name.' — Ade, Delivery Driver, Lindqvist Freight. 2. 'The dispatch team calls before you've noticed a problem; it's never felt like I'm on my own out there.' — Bea, Delivery Driver, Lindqvist Freight.",
    "TC-55": "'You can work from home on Fridays once you've passed probation, and most of the team does.' — Dara, Claims Assessor, Venmore Mutual",
    "TC-56": "'In the Carrow depot, every driver gets a new van every three years.' — Lewis, Fleet Supervisor, Brennan Haulage",
    "TC-57": "Interview with Kemal, Line Cook, Orchard & Vine. 'The first month was brutal, honestly.' (later) 'What kept me here is that the head chef explains why, not just what.' (later) 'Now I train the new starters on the grill.'",
    "TC-58": "'Me and the team was proper proud when the new ward opened — we done it in six weeks.' — Shanice, Healthcare Assistant, Danesmoor Hospital",
    "TC-59": "'I started on reception, and — this sounds odd, I know — I now run the patient-experience team of nine.' — Priyanka, Patient Experience Lead, Elmfield Clinics",
    "TC-60": 'Brookhaven Care Homes. Care assistants work 12-hour shifts, three or four days a week. Pay: £12.40 per hour. Full induction provided.',
    "TC-62": 'Growing at Saltmere Logistics. We support every new starter to grow. Our mentoring scheme pairs you with an experienced colleague.',
    "TC-63": 'Varrow Tools makes hand tools in its own workshop. We hire people who care about getting things right. Training is given on the job. Pay is discussed at interview. Send your CV to jobs@varrow.example.',
    "TC-64": 'Our engineers work on many interesting projects across different sectors, and there is always something new to learn.',
    "TC-65": 'Fernhill Bank. Our customer-service team won the regional service award in 2024. New advisers spend four weeks in classroom training before taking calls.',
    "TC-66": 'Bake with Corrin. Corrin Bakeries invests in its people. Last spring, 19 of our 22 night bakers completed the Level 2 food-safety refresher in paid time. Our ovens run six nights a week from our Dunmore site.',
    "TC-67": 'Library Assistant — Tarnwell Libraries. We offer genuine flexibility. If you work two Saturdays in a month, you can take the following Monday off in lieu. Opening hours are 09:00 to 19:00, Monday to Saturday.',
    "TC-68": 'Ashby Cold Storage. Join a team that looks after you. Drivers get a £400 annual boot and clothing allowance at our Felling site. Shifts are planned a fortnight ahead. Apply online in ten minutes.',
    "TC-69": 'Repairs careers at Marrowfield Housing. Since the 2023 merger, every repairs operative who completes the twelve-month gas-safety pathway, which runs alongside normal duties and is assessed by an external examiner, moves onto the senior operative pay band, although places on the pathway are limited to eight a year across the eastern patch. We value practical skills.',
    "TC-70": 'Holloway Credit Union — Careers. Our branch teams offer real progression. Last year, 14 of our 17 new contact-centre team leaders were promoted from within. Branches are open six days a week, and branch staff work a rota of five days in seven.',
    "TC-71": 'Document 1 — careers page, Pelling Garden Centres: All permanent staff get a 12% employer pension contribution and a 25% staff discount. Document 2 — job ad: Weekend Plant Area Assistant, Pelling Garden Centres, Saturdays and Sundays, 08:30–17:00, £12.10 per hour. Apply in store.',
    "TC-72": 'Careers page, Sallow Hill Veterinary Group: Our clinical team gets five paid CPD days a year and a £600 CPD budget. Job ad: Veterinary Receptionist, Sallow Hill (Kirkby practice). Greet clients, manage bookings and take payments. Monday to Friday, 08:00–16:00. £23,400 a year.',
    "TC-73": "Graduates at Fennick Engineering. We're proud of our graduate scheme. Graduates rotate through three departments in their first two years and choose where to settle at the end.",
    "TC-74": 'Glassblowers at Orla Ferrier Studio work a four-day week and are trained in both furnace work and cold-working techniques. The studio is in a converted mill on the River Teign.',
    "TC-75": 'Пивоварня «Северный солод» (Калининград): технологи работают по графику четыре дня в неделю, а после первого года проходят двухнедельную стажировку на партнёрской пивоварне в Пльзене.',
    "TC-76": 'Careers page, Brindle Foods: Last year, 9 of our 12 new shift supervisors were promoted from the production line. Job ad: Production Team Leader, Brindle Foods (Wexley site). Lead a team of ten on the chilled-meals line. Days, 06:00–14:00. £31,000 a year.',
    "TC-77": 'Engineering at Calder Robotics. Every engineer at Calder gets a mentor. In our software engineering team, every new hire is paired with a senior engineer for their first six months.',
    "TC-78": 'Northgate Parcels — join our Leeds hub. Safety comes first at Northgate. Our Hull hub recorded zero lost-time injuries in 2025. Leeds hub shifts run 22:00–06:00, four nights a week.',
    "TC-79": 'Ellery Theatre Workshops. Our apprentices go on to permanent roles. In 2019, all eight of our scenic-carpentry apprentices were offered permanent contracts.',
    "TC-80": "Tamsin Logistics employee stories. 1. 'I love the variety; no two days are the same.' — Femi, Dispatcher. 2. 'The team made me feel welcome from day one.' — Rosa, Planner. 3. 'Great people and a great atmosphere.' — Ivan, Driver. 4. 'Night shifts were tough at first, but my supervisor changed my rota so I could finish my course.' — Dana, Warehouse Operative. 5. 'I've learned so much here.' — Ollie, Administrator.",
    "TC-81": 'Picker/Packer — Dovecote Fulfilment, Barnsley. Full-time, days. Join our friendly team! Apply today.',
    "TC-82": "Bakery Line Operative — Fenwick Crumb Co., Halford site. £12.85 an hour. Four days on, four days off, 07:00–19:00. We're a passionate, fast-moving family business. Free parking on site.",
    "TC-83": "Hybrid working is available once you've settled into the role. — Pemberton Actuarial Services",
    "TC-84": "Join Gorsedene Water as a Network Inspector. You'll be part of our standby rota. Company van provided.",
    "TC-85": 'At Lantern Row Housing we offer a competitive salary and great benefits.',
    "TC-86": 'Graduate engineers at Hesketh Bridge Consulting. In 2024, most of our graduate engineers passed their chartership review at the first attempt: 30 of our 34 graduates did so.',
    "TC-87": 'Our drivers stay with us for years. In 2018, the average tenure of our delivery drivers was 6.5 years. — Coldharbour Dairies',
    "TC-88": "Kofi joined Ashgrove Retail Logistics in 2020 and now leads the returns team at our Pellam site. 'Every week is different,' he says. Job ad: Returns Supervisor, Pellam site.",
    "TC-89": "'On our night team, everyone gets a free hot meal every shift.' — Ade, Night Picker, Brackenford Foods",
    "TC-90": 'Night Warehouse Operative — Tolland Distribution. £12.60 an hour. The night premium of £1.40 an hour starts after your first six months.',
    "TC-91": 'Ostler Freight job ads. 1. Forklift Driver — £13.20 an hour. 2. Stock Controller — competitive salary. 3. Shift Manager — salary on application. 4. Picker — £12.05 an hour. 5. Goods-In Clerk — competitive pay. 6. Transport Planner — attractive package.',
    "TC-92": 'Ravelston Hospice careers page: The most rewarding place to nurse in the county. Our 46 nurses work in teams of six, and every new nurse has a named buddy for the first eight weeks.',
    "TC-93": "Calloway Signs apprenticeship: the region's top place to learn signwriting. Apprentices spend three days a week in the workshop and two at Hollins College, and all four of last year's apprentices finished the course.",
    "TC-94": "Careers page, Dunmere Print Works: We're a four-day-week employer. Job ad, Dunmere Print Works, Finishing Operator: Monday to Friday, 08:00–16:30.",
    "TC-95": "A: 'At Brierley Vale Care we are committed to excellence in every aspect of resident care.' B: 'Last Tuesday I spent the afternoon helping Mr Okoro plant tomatoes in the courtyard; he hadn't been outside for a week.' — Lerato, Care Worker, Brierley Vale Care",
    "TC-96": "Pastry Chef — Quaymount Hotel, Whitlow. £30,500 a year. Four shifts a week, 06:00–15:00. Two weeks' paid training in our bakery before you work a solo shift. Staff meals provided.",
    "TC-97": 'Greyfriars Bus Company. We look after our drivers. The average tenure of our bus drivers in 2023 was 7.1 years. Every driver gets a rest room with hot food at the Mardale depot.',
    "TC-21": (
        "Payvia processes 40 million transactions a month across 31 markets. Our platform has 99.98% uptime. "
        "We were named Fintech Product of the Year. Our app has a 4.8 rating with 200,000 reviews. Join our "
        "engineering team."
    ),
}


def material_for(case_id):
    """Material supplied with each case, as specified in test-cases.md."""
    if case_id == "TC-01":
        return fixture_text("average-employer.md")
    if case_id == "TC-02":
        return fixture_text("weak-employer.md")
    if case_id == "TC-03":
        return fixture_section("average-employer.md", "## Document 1")
    if case_id == "TC-04":
        return fixture_section("strong-employer.md", "## Material 1")
    if case_id == "TC-05":
        return fixture_section("weak-employer.md", "## Material 3")
    if case_id == "TC-06":
        return fixture_section("weak-employer.md", "## Material 2")
    if case_id == "TC-14":
        return fixture_text("average-employer.md")
    if case_id == "TC-15":
        return careers_subsection("average-employer.md", "\n*Real progression*\n", "\n*A team that has your back*\n")
    if case_id == "TC-16":
        return fixture_text("contradictory-employer.md")
    if case_id == "TC-23":
        return fixture_text("strong-employer.md")
    if case_id == "TC-24":
        return fixture_text("malicious-input.md")
    if case_id == "TC-28":
        return fixture_section("contradictory-employer.md", "## Touchpoint 4")
    if case_id == "TC-30":
        return fixture_section("weak-employer.md", "## Material 3")
    if case_id == "TC-34":
        return fixture_text("hygiene-heavy-employer.md")
    if case_id == "TC-35":
        return fixture_text("weak-employer.md")
    if case_id == "TC-38":
        return fixture_text("consistent-generic-employer.md")
    if case_id == "TC-39":
        text = fixture_text("weak-employer.md")
        variant = text.replace("- Your birthday off\n", "")
        if variant == text:
            raise SystemExit("TC-39 variant: perk line not found in weak fixture")
        return variant
    if case_id == "TC-40":
        return (INLINE["TC-40-AB"] + "\n\nC.\n" + fixture_section("average-employer.md", "## Document 1")
                + "\nD.\n" + fixture_section("strong-employer.md", "## Material 1")
                + "\n" + fixture_section("strong-employer.md", "## Material 2"))
    return INLINE.get(case_id)


DEPENDS_ON = {"TC-22": "TC-02", "TC-25": "TC-01", "TC-61": "TC-60"}
REPEATS = {"TC-40": 5}  # cases run several times in independent sessions (determinism checks)


# --------------------------------------------------------------------------
# Parsing test-cases.md
# --------------------------------------------------------------------------

def parse_test_cases():
    text = read(TEST_CASES_MD)
    heads = list(re.finditer(r"^## (TC-\d{2}) — (.+)$", text, re.MULTILINE))
    cases = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else text.find("\n---\n\n## Fixture calibration", m.start())
        section = text[m.start():end if end != -1 else len(text)]

        def field(label):
            fm = re.search(r"^- \*\*" + re.escape(label) + r":\*\*(.*)$", section, re.MULTILINE)
            return fm.group(1).strip() if fm else ""

        prompt_line = field("Prompt")
        first, last = prompt_line.find('"'), prompt_line.rfind('"')
        if first == -1 or last <= first:
            raise SystemExit("Cannot extract quoted prompt for " + m.group(1))
        cases.append({
            "id": m.group(1),
            "title": m.group(2).strip(),
            "prompt": prompt_line[first + 1:last],
            "prompt_line": prompt_line,
            "material_spec": field("Material"),
            "expected_skill": field("Expected skill"),
            "expected_behaviour": field("Expected behaviour"),
            "fail_if": field("Fail if"),
        })
    return cases


def check_inline_materials():
    text = read(TEST_CASES_MD).replace('\\"', '"')
    normalised = re.sub(r"\s+", " ", text.replace("> ", " ").replace("  >", " "))
    for case_id, material in INLINE.items():
        for line in material.splitlines():
            probe = re.sub(r"\s+", " ", line.strip())
            if probe and probe not in normalised:
                raise SystemExit("Inline material for {} drifted from test-cases.md: {!r}".format(case_id, probe[:80]))


def compose_message(prompt, material):
    return prompt if not material else prompt + "\n\n" + material


# --------------------------------------------------------------------------
# Running the CLI
# --------------------------------------------------------------------------

def read(path):
    return Path(path).read_text(encoding="utf-8")


def write_new(path, content):
    """Write a file that must not already exist."""
    with open(path, "x", encoding="utf-8") as handle:
        handle.write(content)


def new_run_dir(suite, label, subdir=""):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = RESULTS / subdir / suite if subdir else RESULTS / suite
    base.mkdir(parents=True, exist_ok=True)
    candidate = base / (stamp + ("-" + label if label else ""))
    n = 1
    while candidate.exists():
        n += 1
        candidate = base / "{}{}-{}".format(stamp, "-" + label if label else "", n)
    candidate.mkdir()
    return candidate


def parse_stream(raw):
    info = {"model": None, "skills_invoked": [], "tools_used": [], "result_text": "",
            "result_subtype": None, "is_error": None, "cost_usd": None, "num_turns": None,
            "session_id": None, "loaded_plugins": [], "tool_errors": []}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        etype = event.get("type")
        if etype == "system" and event.get("subtype") == "init":
            info["model"] = event.get("model")
            info["session_id"] = event.get("session_id")
            info["loaded_plugins"] = [p.get("name") for p in event.get("plugins", [])]
        elif etype == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name")
                    info["tools_used"].append(name)
                    if name == "Skill":
                        info["skills_invoked"].append(block.get("input", {}).get("skill"))
        elif etype == "user":
            content = event.get("message", {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "tool_result" and block.get("is_error"):
                        info["tool_errors"].append(str(block.get("content"))[:300])
        elif etype == "result":
            info["result_text"] = event.get("result") or ""
            info["result_subtype"] = event.get("subtype")
            info["is_error"] = event.get("is_error")
            info["cost_usd"] = event.get("total_cost_usd")
            info["num_turns"] = event.get("num_turns")
            info["session_id"] = event.get("session_id") or info["session_id"]
    return info


def run_claude(message, workdir, session_id=None, resume=None, timeout=DEFAULT_TIMEOUT, model=None,
               budget=None):
    args = ["claude", "-p", message,
            "--plugin-dir", str(PLUGIN_ROOT),
            "--add-dir", str(PLUGIN_ROOT),
            "--tools", TOOLS,
            "--allowedTools", TOOLS,
            "--permission-mode", "dontAsk",
            "--strict-mcp-config",
            "--output-format", "stream-json",
            "--verbose"]
    if resume:
        args += ["--resume", resume]
    elif session_id:
        args += ["--session-id", session_id]
    if model:
        args += ["--model", model]
    if budget:
        args += ["--max-budget-usd", str(budget)]
    started = datetime.datetime.now(datetime.timezone.utc)
    try:
        proc = subprocess.run(args, cwd=str(workdir), stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=timeout)
        exit_code, stdout, stderr, timed_out = proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        exit_code = None
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        timed_out = True
    finished = datetime.datetime.now(datetime.timezone.utc)
    # Record the message by reference to keep the args list readable.
    shown_args = [a if a is not message else "<message>" for a in args]
    return {
        "args": shown_args, "exit_code": exit_code, "timed_out": timed_out,
        "started_utc": started.isoformat(), "finished_utc": finished.isoformat(),
        "duration_s": round((finished - started).total_seconds(), 1),
        "stdout": stdout, "stderr": stderr,
    }


def execute(case_key, record, run_dir, workdir, session_id=None, resume=None, timeout=DEFAULT_TIMEOUT,
            model=None, budget=None):
    log("[start] {}".format(case_key))
    outcome = run_claude(record["message_sent"], workdir, session_id=session_id, resume=resume,
                         timeout=timeout, model=model, budget=budget)
    parsed = parse_stream(outcome["stdout"])
    record.update({
        "workdir": str(workdir),
        "cli_args": outcome["args"],
        "exit_code": outcome["exit_code"],
        "timed_out": outcome["timed_out"],
        "started_utc": outcome["started_utc"],
        "finished_utc": outcome["finished_utc"],
        "duration_s": outcome["duration_s"],
        "stderr": outcome["stderr"],
        "resumed_session": resume,
    })
    record.update(parsed)
    failed_reasons = []
    if outcome["exit_code"] != 0:
        failed_reasons.append("exit code {}".format(outcome["exit_code"]))
    if outcome["timed_out"]:
        failed_reasons.append("timeout")
    if parsed.get("is_error"):
        failed_reasons.append("CLI reported is_error")
    if re.search(r"Failed to authenticate|API Error|rate limit", parsed.get("result_text") or "", re.IGNORECASE):
        failed_reasons.append("API/auth error in result")
    record["session_failed"] = bool(failed_reasons)
    record["failure_reasons"] = failed_reasons
    write_new(run_dir / (case_key + ".stream.jsonl"), outcome["stdout"])
    write_new(run_dir / (case_key + ".response.md"), parsed["result_text"])
    write_new(run_dir / (case_key + ".record.json"), json.dumps(record, indent=2, ensure_ascii=False))
    log("[{}] {} exit={} skills={} {}s ${}{}".format(
        "FAIL " if failed_reasons else "done ", case_key, outcome["exit_code"], parsed["skills_invoked"],
        outcome["duration_s"], parsed["cost_usd"], (" — " + "; ".join(failed_reasons)) if failed_reasons else ""))
    return record


def make_workdir(base):
    return Path(tempfile.mkdtemp(prefix="eba-eval-", dir=base))


# --------------------------------------------------------------------------
# Suites
# --------------------------------------------------------------------------

def run_baseline(opts):
    check_inline_materials()
    cases = parse_test_cases()
    if len(cases) != 97:
        raise SystemExit("Expected 97 cases in test-cases.md, found {}".format(len(cases)))
    wanted = set(opts.cases.split(",")) if opts.cases else None
    selected = [c for c in cases if wanted is None or c["id"] in wanted]
    for dep, pre in DEPENDS_ON.items():
        if any(c["id"] == dep for c in selected) and not any(c["id"] == pre for c in selected):
            raise SystemExit("{} requires {} in the same run".format(dep, pre))

    run_dir = new_run_dir("baseline", opts.label, opts.results_subdir)
    write_new(run_dir / "run.json", json.dumps({
        "suite": "baseline", "started_local": datetime.datetime.now().isoformat(),
        "cases": [c["id"] for c in selected], "concurrency": opts.jobs, "model_override": opts.model,
        "claude_version": cli_version(), "tools": TOOLS, "plugin_root": str(PLUGIN_ROOT),
    }, indent=2))
    log("Baseline run dir: {}".format(run_dir))

    records = {}
    prereq_state = {}

    def first_pass(job):
        case, repeat = job
        material = material_for(case["id"])
        record = dict(case)
        record["material"] = material
        record["message_sent"] = compose_message(case["prompt"], material)
        record["suite"] = "baseline"
        key = case["id"] if repeat is None else "{}-r{}".format(case["id"], repeat)
        record["run_key"] = key
        workdir = make_workdir(opts.workdir_base)
        sid = str(uuid.uuid4())
        result = execute(key, record, run_dir, workdir, session_id=sid, timeout=opts.timeout,
                         model=opts.model, budget=opts.budget)
        prereq_state[key] = (workdir, result.get("session_id") or sid)
        result["id"] = key
        return result

    independent = []
    for c in selected:
        if c["id"] in DEPENDS_ON:
            continue
        n = REPEATS.get(c["id"])
        independent.extend([(c, None)] if not n else [(c, i) for i in range(1, n + 1)])
    dependent = [c for c in selected if c["id"] in DEPENDS_ON]
    with concurrent.futures.ThreadPoolExecutor(max_workers=opts.jobs) as pool:
        for result in pool.map(first_pass, independent):
            records[result["id"]] = result

    def follow_up(case):
        pre = DEPENDS_ON[case["id"]]
        workdir, sid = prereq_state[pre]
        record = dict(case)
        record["material"] = "(prior conversation: {})".format(pre)
        record["message_sent"] = case["prompt"]
        record["suite"] = "baseline"
        record["depends_on"] = pre
        return execute(case["id"], record, run_dir, workdir, resume=sid, timeout=opts.timeout,
                       model=opts.model, budget=opts.budget)

    with concurrent.futures.ThreadPoolExecutor(max_workers=opts.jobs) as pool:
        for result in pool.map(follow_up, dependent):
            records[result["id"]] = result

    write_index(run_dir, records)
    cleanup(opts, prereq_state)
    log("Finished. Results in {}".format(run_dir))


def run_repeatability(opts):
    keys = opts.fixtures.split(",") if opts.fixtures else list(REPEATABILITY_FIXTURES)
    run_dir = new_run_dir("repeatability", opts.label, opts.results_subdir)
    jobs = []
    for key in keys:
        for n in range(1, opts.runs + 1):
            jobs.append((key, n))
    write_new(run_dir / "run.json", json.dumps({
        "suite": "repeatability", "started_local": datetime.datetime.now().isoformat(),
        "prompt": REPEATABILITY_PROMPT, "fixtures": keys, "runs_per_fixture": opts.runs,
        "concurrency": opts.jobs, "model_override": opts.model, "claude_version": cli_version(),
        "tools": TOOLS, "plugin_root": str(PLUGIN_ROOT),
    }, indent=2))
    log("Repeatability run dir: {}".format(run_dir))
    workdirs = {}

    def one(job):
        key, n = job
        case_key = "{}-run{}".format(key, n)
        material = fixture_text(REPEATABILITY_FIXTURES[key])
        record = {"id": case_key, "fixture": REPEATABILITY_FIXTURES[key], "run": n,
                  "prompt": REPEATABILITY_PROMPT, "material": material,
                  "message_sent": compose_message(REPEATABILITY_PROMPT, material),
                  "suite": "repeatability"}
        workdir = make_workdir(opts.workdir_base)
        workdirs[case_key] = (workdir, None)
        return execute(case_key, record, run_dir, workdir, session_id=str(uuid.uuid4()),
                       timeout=opts.timeout, model=opts.model, budget=opts.budget)

    records = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=opts.jobs) as pool:
        for result in pool.map(one, jobs):
            records[result["id"]] = result
    write_index(run_dir, records)
    cleanup(opts, workdirs)
    log("Finished. Results in {}".format(run_dir))


def write_index(run_dir, records):
    rows = []
    for key in sorted(records):
        r = records[key]
        rows.append({
            "id": key, "exit_code": r.get("exit_code"), "timed_out": r.get("timed_out"),
            "skills_invoked": r.get("skills_invoked"), "duration_s": r.get("duration_s"),
            "cost_usd": r.get("cost_usd"), "model": r.get("model"),
            "response_chars": len(r.get("result_text") or ""), "tool_errors": len(r.get("tool_errors") or []),
            "session_failed": r.get("session_failed"), "failure_reasons": r.get("failure_reasons"),
        })
    write_new(run_dir / "index.json", json.dumps(rows, indent=2, ensure_ascii=False))
    failed = [row["id"] for row in rows if row["session_failed"]]
    health = {"sessions": len(rows), "failed_sessions": len(failed), "failed_ids": failed,
              "usable": not failed}
    write_new(run_dir / "run-health.json", json.dumps(health, indent=2))
    log("RUN HEALTH: {} sessions, {} FAILED{}".format(len(rows), len(failed),
        " — results NOT usable until failed cases are re-run: " + ", ".join(failed) if failed else ""))


def cleanup(opts, state):
    if opts.keep_workdirs:
        return
    for workdir, _ in state.values():
        shutil.rmtree(str(workdir), ignore_errors=True)


def cli_version():
    try:
        return subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=60,
                              stdin=subprocess.DEVNULL).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


# --------------------------------------------------------------------------
# Score extraction for repeatability runs
# --------------------------------------------------------------------------

DIMENSIONS = ("Clarity", "Differentiation", "Proof", "Audience Fit", "Employee Truth", "Consistency",
              "Candidate Relevance", "Conversion")


def extract_scores(text):
    out = {}
    m = re.search(r"Employer Brand Score:?\**\s*(?:\|\s*)?\**\s*(\d{1,3})\s*/\s*100", text)
    out["score"] = int(m.group(1)) if m else None
    m = re.search(r"Coverage:?\**\s*(?:\|\s*)?\**\s*(\d{1,3})\s*%", text)
    out["coverage"] = int(m.group(1)) if m else None
    m = re.search(r"Confidence:?\**\s*(?:\|\s*)?\**\s*(HIGH|MEDIUM|LOW)", text)
    out["confidence"] = m.group(1) if m else None
    for dim in DIMENSIONS:
        row = re.search(r"^\|\s*\**" + re.escape(dim) + r"\**\s*\|\s*\**([^|]+?)\**\s*\|\s*\**(\d+)\**\s*\|",
                        text, re.MULTILINE | re.IGNORECASE)
        if row:
            cell = row.group(1).strip()
            num = re.match(r"(\d+)", cell)
            out[dim] = int(num.group(1)) if num else cell
            out[dim + " max"] = int(row.group(2))
        else:
            out[dim] = None
    problems = section(text, r"BIGGEST PROBLEMS", r"GENERICITY TEST")
    if problems is not None:
        severities = []
        for line in problems.splitlines():
            numbered = re.match(r"^\s*\**\s*\d+[.)]", line)
            led = re.match(r"^\s*\*\*\s*(CRITICAL|HIGH|MEDIUM|LOW)\b", line)
            if numbered or led:
                sev = re.search(r"\b(CRITICAL|HIGH|MEDIUM|LOW)\b", line)
                severities.append(sev.group(1) if sev else "UNLABELLED")
        out["problem_severities"] = severities
        out["critical_findings"] = severities.count("CRITICAL")
        out["high_findings"] = severities.count("HIGH")
    else:
        out["problem_severities"] = None
        out["critical_findings"] = None
        out["high_findings"] = None
    gen = section(text, r"GENERICITY TEST", r"CLAIM\s*(?:→|->)")
    if gen:
        verdicts = re.findall(r"VERDICT:?\**\s*\**\s*(DISTINCTIVE|PARTIALLY DIFFERENTIATED|GENERIC)", gen, re.IGNORECASE)
        verdicts = [v.upper() for v in verdicts]
        if not verdicts:  # table format
            verdicts = re.findall(r"\|\s*\**(DISTINCTIVE|PARTIALLY DIFFERENTIATED|GENERIC)\b", gen)
        out["genericity_verdicts"] = {v: verdicts.count(v) for v in
                                      ("DISTINCTIVE", "PARTIALLY DIFFERENTIATED", "GENERIC")}
    else:
        out["genericity_verdicts"] = None
    fixes = section(text, r"TOP 3 FIXES", r"BEFORE")
    out["top_fixes"] = fix_titles(fixes) if fixes else None
    ledger = section(text, r"CLAIM\s*(?:→|->)\s*PROOF", r"RED FLAGS")
    if ledger is None:
        ledger = section(text, r"РЕЕСТР", r"КРАСНЫЕ")
    if ledger:
        rows = [l for l in ledger.splitlines() if l.strip().startswith("|")]
        body = [l for l in rows[1:] if not re.match(r"^\|\s*:?-{2,}", l.strip())]
        out["ledger_rows"] = len(body)
        out["ledger_statuses"] = {st: len(re.findall(r"\b" + st + r"\b", ledger)) for st in
                                  ("STRONGLY SUPPORTED", "PARTIALLY SUPPORTED", "WEAKLY SUPPORTED",
                                   "UNSUPPORTED", "CONFLICTING")}
        out["ledger_mentions_unverified"] = "UNVERIFIED" in ledger
    else:
        out["ledger_rows"] = None
    return out


def section(text, start_pattern, end_pattern):
    """Body of the heading matching start_pattern, up to the next Markdown heading."""
    h = re.search(r"^#+\s*(?:\d+\.\s*)?" + start_pattern + r".*$", text, re.MULTILINE | re.IGNORECASE)
    if h:
        nxt = re.search(r"^#{1,3}\s", text[h.end():], re.MULTILINE)
        return text[h.end(): h.end() + nxt.start()] if nxt else text[h.end():]
    s = re.search(r"^#*\s*\**\s*(?:\d+\.\s*)?" + start_pattern, text, re.MULTILINE | re.IGNORECASE)
    if not s:
        return None
    e = re.search(r"^#+\s*\**\s*(?:\d+\.\s*)?" + end_pattern, text[s.end():], re.MULTILINE | re.IGNORECASE)
    return text[s.end(): s.end() + e.start()] if e else text[s.end():]


def fix_titles(block):
    titles = []
    for line in block.splitlines():
        m = re.match(r"^\s*(?:#+\s*)?\**\s*(\d)[.)]\s*\**\s*(.+)$", line)
        if m and len(titles) < 3 and m.group(1) == str(len(titles) + 1):
            titles.append(re.sub(r"\*+", "", m.group(2)).strip()[:160])
    return titles


def run_extract(opts):
    run_dir = Path(opts.run_dir).resolve()
    rows = []
    for path in sorted(run_dir.glob("*.response.md")):
        key = path.name[:-len(".response.md")]
        scores = extract_scores(read(path))
        scores["id"] = key
        rows.append(scores)
    target = run_dir / "extracted-scores.json"
    if target.exists():
        n = 2
        while (run_dir / "extracted-scores-{}.json".format(n)).exists():
            n += 1
        target = run_dir / "extracted-scores-{}.json".format(n)
    write_new(target, json.dumps(rows, indent=2, ensure_ascii=False))
    print("Wrote {}".format(target))


# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("-j", "--jobs", type=int, default=4, help="parallel CLI sessions (default 4)")
        p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds per case")
        p.add_argument("--model", default=None, help="optional --model override passed to claude")
        p.add_argument("--budget", type=float, default=None, help="optional --max-budget-usd per case")
        p.add_argument("--label", default="", help="suffix for the run directory name")
        p.add_argument("--workdir-base", default=tempfile.gettempdir(),
                       help="where per-case temporary working directories are created")
        p.add_argument("--keep-workdirs", action="store_true")
        p.add_argument("--results-subdir", default="",
                       help="version folder under evals/results (e.g. v0.1.1); default keeps the v0.1.0 layout")

    b = sub.add_parser("baseline", help="run the 25 cases from test-cases.md")
    b.add_argument("--cases", default="", help="comma-separated case IDs (default: all)")
    common(b)
    r = sub.add_parser("repeatability", help="repeat full audits of fixtures")
    r.add_argument("--runs", type=int, default=5)
    r.add_argument("--fixtures", default="", help="comma-separated: " + ",".join(REPEATABILITY_FIXTURES))
    common(r)
    e = sub.add_parser("extract", help="parse scores from a repeatability run directory")
    e.add_argument("run_dir")

    opts = parser.parse_args()
    if opts.command in ("baseline", "repeatability"):
        if shutil.which("claude") is None:
            raise SystemExit("claude CLI not found on PATH")
        if Path(opts.workdir_base).resolve().is_relative_to(PLUGIN_ROOT) if hasattr(Path, "is_relative_to") else \
                str(Path(opts.workdir_base).resolve()).startswith(str(PLUGIN_ROOT)):
            raise SystemExit("--workdir-base must be outside the plugin tree (its CLAUDE.md would load)")
    if opts.command == "baseline":
        run_baseline(opts)
    elif opts.command == "repeatability":
        run_repeatability(opts)
    else:
        run_extract(opts)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main()
