#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the HTML audit-report templates shipped with the plugin.

One source (this file) produces templates/audit-report.ru.html and templates/audit-report.en.html.
Each template is self-contained: inline CSS and JS, a fixed "How to read this report" section, and a
renderer that turns the audit data (JSON, written by the employer-brand-audit skill into the
<script id="report-data"> block) into the report. Labels for every code in the data are defined here,
so they read the same in every report.

Run after any change:  python3 scripts/build_report_templates.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "templates")
DATA_SLOT = "REPORT_DATA_JSON"

# ---------------------------------------------------------------------------
# Labels and fixed explanatory text, per language
# ---------------------------------------------------------------------------
I18N = {
    "ru": {
        "doc_title": "Аудит HR-бренда",
        "kicker": "Аудит HR-бренда",
        "date": "Дата",
        "materials": "Материалы",
        "score": "Оценка HR-бренда",
        "provisional": "предварительная",
        "withheld": "Оценка не выставлена",
        "withheld_note": "Материалов слишком мало для общей оценки: можно оценить меньше 40% критериев.",
        "coverage": "Покрытие",
        "coverage_hint": "какую долю критериев удалось оценить по этим материалам",
        "reliability": "Надёжность оценки",
        "rel": {"high": "высокая", "medium": "средняя", "low": "низкая"},
        "rel_hint": "хватило ли материалов разных типов, чтобы оценка была устойчивой",
        "toc": "Содержание",
        "sec_summary": "Коротко для руководителя",
        "sec_howto": "Как читать этот отчёт",
        "sec_scorecard": "Оценка по направлениям",
        "sec_working": "Что работает",
        "sec_problems": "Главные проблемы",
        "sec_plan": "План: три главных исправления",
        "sec_rewrites": "Было → стало",
        "sec_questions": "Вопросы к компании",
        "sec_appendix": "Приложение: детали анализа",
        "app_genericity": "Тест на шаблонность",
        "app_ledger": "Обещания и доказательства",
        "app_details": "Оценка по критериям",
        "app_materials": "Изученные материалы",
        "app_sources": "Источники",
        "src_cols": ["Страница", "Тип", "Дата", "Ссылка"],
        "open": "открыть",
        "summary_points": "Главное",
        "summary_actions": "Что сделать в первую очередь",
        "band": {
            "85": "Выразительный и хорошо доказанный бренд. Остались доработки.",
            "70": "Сильный бренд с заметными, исправимыми пробелами.",
            "50": "Бренд работает, но в важных местах звучит шаблонно или не подкреплён фактами.",
            "30": "Слабый бренд: мало конкретных причин выбрать компанию и мало доказательств.",
            "0": "В материалах не видно работающего предложения для кандидата.",
        },
        "band_scale_note": "Шкала описывает только эту методологию. Это не рейтинг и не сравнение с другими компаниями.",
        "dims": {
            "clarity": ["Ясность", "Понятно ли с первого взгляда, что компания предлагает и почему стоит к ней идти."],
            "differentiation": ["Отличие от других", "Можно ли эти обещания без изменений перенести в текст другой компании той же отрасли."],
            "proof": ["Доказательства", "Подкреплены ли обещания цифрами, практиками и примерами прямо в материалах."],
            "audience_fit": ["Попадание в аудиторию", "Понятно ли, к кому обращаются, и учтены ли условия и ограничения разных ролей."],
            "employee_truth": ["Голос сотрудников и реальность работы", "Есть ли настоящие истории людей и описание того, как выглядит работа, включая трудности."],
            "consistency": ["Согласованность", "Говорят ли разные материалы одно и то же и нет ли между ними противоречий."],
            "candidate_relevance": ["Ответы на вопросы кандидата", "Есть ли то, что нужно для решения: зарплата, график, задачи, условия."],
            "conversion": ["Путь к отклику", "Понятно ли, что делать дальше, как откликнуться и чего ждать после отклика."],
        },
        "not_assessable": "не оценивалось",
        "why": "Почему",
        "rf": {"RF01": "Шаблонное обещание", "RF02": "Превосходная степень без доказательств", "RF03": "Миссия компании вместо предложения сотруднику", "RF04": "Текст о компании, а не о кандидате", "RF05": "Факт без пользы для кандидата", "RF06": "Выгода без доказательства", "RF07": "Культура описана одними прилагательными", "RF08": "Непонятно, к кому обращаются", "RF09": "Одно сообщение для всех ролей", "RF10": "Нет голоса сотрудников", "RF11": "Не видно, как выглядит работа", "RF12": "Обещания противоречат друг другу", "RF13": "Размер компании без смысла для кандидата", "RF14": "Размытое обещание развития", "RF15": "Штамп про инновации", "RF16": "Штамп про команду", "RF17": "Список льгот вместо предложения", "RF18": "Обещание шире доказательства", "RF19": "Внутренний жаргон без пояснения", "RF20": "Нет понятного следующего шага", "RF21": "Ценности вместо отличий", "RF22": "Доказательство не о том, что важно кандидату", "RF23": "Обещание не доходит до текстов для кандидатов", "RF24": "Слишком гладко, реальной работы не видно"},
        "effort": {"small": "небольшая", "medium": "средняя", "large": "большая"},
        "effort_lbl": "Трудоёмкость",
        "who": "Кого привлечь",
        "check": "Как понять, что сработало",
        "scope_in": "Что вошло в аудит",
        "scope_out": "Что не смотрели",
        "severity": {"critical": "Критично", "high": "Высокая важность", "medium": "Средняя важность", "low": "Низкая важность"},
        "evidence": "Что в материалах",
        "why_matters": "Почему это важно",
        "flags": "Типовая ошибка",
        "fix_where": "Что сделать",
        "fix_why": "Почему такой приоритет",
        "fix_needs": "Что понадобится",
        "fix_ready": "Можно сделать из того, что уже есть",
        "fix_data": "Нужны новые данные",
        "rw_original": "Было",
        "rw_problem": "Что не так",
        "rw_logic": "Как исправлено",
        "rw_rewrite": "Стало",
        "q_kind": {"confirm": "Уточнить", "evidence": "Нужны данные"},
        "q_for": {"audit": "Чтобы аудит был точнее", "communication": "Чтобы усилить тексты для кандидатов"},
        "q_note": "Пока ответа нет, эти пункты не используются в выводах и не попадают в переписанные тексты как факты.",
        "gen_cols": ["Обещание", "Итог", "Подстановка", "Штампы", "Конкретика", "Можно ли отстоять", "Почему"],
        "gen": {
            "verdict": {"distinctive": "Отличает вас", "partial": "Частично отличает", "generic": "Шаблонное"},
            "substitution": {"breaks": "Только про вас", "bends": "Почти только про вас", "survives": "Подходит любому"},
            "ubiquity": {"rare": "Своими словами", "common": "Есть штампы", "ubiquitous": "Из штампов"},
            "specificity": {"high": "Много", "some": "Немного", "none": "Нет"},
            "defensibility": {"owned": "Ваше и доказано", "supportable": "Можно подкрепить", "unowned": "Ничем не закреплено"},
        },
        "led_cols": ["Обещание", "Вес", "Чем подкреплено", "Сила", "Итог", "Комментарий"],
        "led": {
            "class": {"core": "Главное", "supporting": "Второстепенное"},
            "strength": {"strong": "Сильное", "moderate": "Среднее", "weak": "Слабое", "none": "Нет"},
            "status": {"strong": "Подтверждено", "partial": "Частично подтверждено", "weak": "Слабо подтверждено", "none": "Не подтверждено", "conflicting": "Противоречит материалам"},
        },
        "det_cols": ["Направление", "Критерий", "Баллы", "Комментарий"],
        "mat_cols": ["Материал", "Тип"],
        "footer": "Отчёт подготовлен плагином Employer Brand Auditor. Аудит оценивает только переданные материалы: как они выглядят для кандидата и чем подкреплены. Факты о компании независимо не проверялись. Перед публикацией проверьте переписанные тексты и все цифры.",
        "parse_error": "Не удалось прочитать данные отчёта. Попросите плагин пересобрать HTML-отчёт.",
        "print": "Сохранить в PDF",
        "howto_toggle": "Показать или скрыть пояснения",
        "howto_html": """
<p class="lead">Аудит смотрит на тексты для кандидатов так, как их читает человек, который выбирает работу: карьерную страницу, ценностное предложение работодателя (EVP), вакансии, истории сотрудников. Он отвечает на три вопроса: что вы обещаете, чем это подкреплено и что исправить в первую очередь.</p>
<div class="howto-grid">
  <div class="howto-card"><h4>Главное правило</h4><p>Нет доказательства в материалах — нет утверждения в отчёте. Аудит не придумывает факты, цифры и сравнения с рынком. Если доказательства в текстах нет, это значит только одно: кандидат его не увидит. Это не значит, что в компании такой практики нет.</p></div>
  <div class="howto-card"><h4>Оценка из 100</h4><p>Сумма баллов по восьми направлениям ниже. Направления весят по-разному. Больше всего, по 16 баллов, весят отличие от других и доказательства: без них остальное остаётся общими словами. Шкала: 85–100 выразительный бренд, 70–84 сильный с пробелами, 50–69 рабочий, но шаблонный, 30–49 слабый, ниже 30 предложения не видно. Это не рейтинг и не сравнение с другими компаниями.</p></div>
  <div class="howto-card"><h4>Покрытие</h4><p>Какую долю из 34 критериев удалось оценить. Если материалов не хватает, например нет ни одной истории сотрудника, такие критерии не ставятся в ноль, а исключаются, и оценка считается по остальным. При покрытии ниже 40% общая оценка не выставляется.</p></div>
  <div class="howto-card"><h4>Надёжность оценки</h4><p>Высокая, если покрытие от 80% и есть хотя бы три разных типа материалов. Средняя, если чего-то из этого не хватает. Низкая, если материалов мало: тогда оценка предварительная. Надёжность говорит о полноте материалов. Она не означает, что факты в них проверены.</p></div>
</div>
<h4 class="howto-h">Тест на шаблонность</h4>
<p>Главные обещания проверяются четырьмя вопросами.</p>
<ul class="howto-list">
  <li><b>Подстановка.</b> Заменяем название компании на «похожий работодатель из той же отрасли». Если фраза осталась правдой, она подходит любому. Если стала неправдой, значит, в ней есть что-то только ваше: место, цифра, конкретная практика.</li>
  <li><b>Штампы.</b> Собрана ли фраза из типовых выражений вроде «дружный коллектив» и «возможности роста».</li>
  <li><b>Конкретика.</b> Есть ли цифры со сроками, названные практики, условия, ограничения.</li>
  <li><b>Можно ли отстоять.</b> Опирается ли обещание на то, что действительно есть у компании и показано в материалах.</li>
</ul>
<h4 class="howto-h">Метки в тексте</h4>
<ul class="howto-list">
  <li><span class="tag tag-q">Уточнить</span> вероятный факт, который компании нужно подтвердить. До ответа он не используется как факт.</li>
  <li><span class="tag tag-e">Нужны данные</span> информации нет в материалах, а без неё текст не усилить.</li>
  <li><b>Подтверждено, частично, слабо, не подтверждено</b>: насколько обещание подкреплено в самих материалах. Это не независимая проверка фактов.</li>
</ul>
""",
    },
    "en": {
        "doc_title": "Employer brand audit",
        "kicker": "Employer brand audit",
        "date": "Date",
        "materials": "Materials",
        "score": "Employer Brand Score",
        "provisional": "provisional",
        "withheld": "Score withheld",
        "withheld_note": "There is too little material for an overall score: fewer than 40% of the criteria can be assessed.",
        "coverage": "Coverage",
        "coverage_hint": "the share of criteria that this material allowed us to assess",
        "reliability": "Score reliability",
        "rel": {"high": "high", "medium": "medium", "low": "low"},
        "rel_hint": "whether enough different types of material were supplied for a stable score",
        "toc": "Contents",
        "sec_summary": "Executive summary",
        "sec_howto": "How to read this report",
        "sec_scorecard": "Score by dimension",
        "sec_working": "What works",
        "sec_problems": "Main problems",
        "sec_plan": "Plan: the three most important fixes",
        "sec_rewrites": "Before → after",
        "sec_questions": "Questions for the company",
        "sec_appendix": "Appendix: analysis detail",
        "app_genericity": "Genericity test",
        "app_ledger": "Claims and proof",
        "app_details": "Score by criterion",
        "app_materials": "Materials reviewed",
        "app_sources": "Sources",
        "src_cols": ["Page", "Type", "Captured", "Link"],
        "open": "open",
        "summary_points": "Key findings",
        "summary_actions": "What to do first",
        "band": {
            "85": "Distinctive and well supported. What remains is refinement.",
            "70": "Strong, with visible gaps that can be fixed.",
            "50": "Works, but reads as generic or unsupported in important places.",
            "30": "Weak: few specific reasons to choose the employer and little proof.",
            "0": "The material shows no working proposition for candidates.",
        },
        "band_scale_note": "The scale describes this methodology only. It is not a ranking or a comparison with other employers.",
        "dims": {
            "clarity": ["Clarity", "Whether it is clear at a glance what the employer offers and why someone would join."],
            "differentiation": ["Differentiation", "Whether the claims could be moved unchanged into another employer's copy in the same sector."],
            "proof": ["Proof", "Whether the claims are backed by figures, practices and examples in the material itself."],
            "audience_fit": ["Audience fit", "Whether it is clear who the material speaks to, and whether the conditions of different roles are covered."],
            "employee_truth": ["Employee voice and work reality", "Whether there are real people's stories and a description of what the work is like, difficulties included."],
            "consistency": ["Consistency", "Whether the materials say the same thing and do not contradict each other."],
            "candidate_relevance": ["Candidate questions answered", "Whether the facts needed to decide are there: pay, schedule, tasks, conditions."],
            "conversion": ["Path to applying", "Whether it is clear what to do next, how to apply and what happens after."],
        },
        "not_assessable": "not assessed",
        "why": "Why",
        "rf": {"RF01": "Generic claim", "RF02": "Superlative without proof", "RF03": "Company mission instead of an offer to employees", "RF04": "About the company, not the candidate", "RF05": "Fact without a benefit for the candidate", "RF06": "Benefit without proof", "RF07": "Culture described only in adjectives", "RF08": "Unclear who it speaks to", "RF09": "One message for every role", "RF10": "No employee voice", "RF11": "The work itself is not shown", "RF12": "Promises contradict each other", "RF13": "Company size without meaning for the candidate", "RF14": "Vague growth promise", "RF15": "Innovation cliché", "RF16": "Great-team cliché", "RF17": "Perks listed instead of an offer", "RF18": "Claim goes beyond its proof", "RF19": "Unexplained internal jargon", "RF20": "No clear next step", "RF21": "Values offered as a difference without proof", "RF22": "Proof that does not bear on the decision", "RF23": "Promise missing from candidate-facing copy", "RF24": "Too polished, no real work shown"},
        "effort": {"small": "small", "medium": "medium", "large": "large"},
        "effort_lbl": "Effort",
        "who": "Who to involve",
        "check": "How to tell it worked",
        "scope_in": "What the audit covered",
        "scope_out": "What it did not look at",
        "severity": {"critical": "Critical", "high": "High priority", "medium": "Medium priority", "low": "Low priority"},
        "evidence": "In the material",
        "why_matters": "Why it matters",
        "flags": "Common mistake",
        "fix_where": "What to do",
        "fix_why": "Why this priority",
        "fix_needs": "What it needs",
        "fix_ready": "Can be done with what you already have",
        "fix_data": "Needs new information",
        "rw_original": "Before",
        "rw_problem": "What is wrong",
        "rw_logic": "How it was fixed",
        "rw_rewrite": "After",
        "q_kind": {"confirm": "Confirm", "evidence": "Information needed"},
        "q_for": {"audit": "To make the audit more precise", "communication": "To strengthen candidate-facing copy"},
        "q_note": "Until answered, these items are not used in the conclusions and do not appear as facts in rewritten copy.",
        "gen_cols": ["Claim", "Result", "Substitution", "Stock phrases", "Specifics", "Can you own it", "Why"],
        "gen": {
            "verdict": {"distinctive": "Sets you apart", "partial": "Partly sets you apart", "generic": "Generic"},
            "substitution": {"breaks": "Only true of you", "bends": "Mostly only you", "survives": "Fits anyone"},
            "ubiquity": {"rare": "Own words", "common": "Some stock phrases", "ubiquitous": "Stock phrases"},
            "specificity": {"high": "A lot", "some": "Some", "none": "None"},
            "defensibility": {"owned": "Yours and proven", "supportable": "Could be supported", "unowned": "Not anchored"},
        },
        "led_cols": ["Claim", "Weight", "Supported by", "Strength", "Result", "Comment"],
        "led": {
            "class": {"core": "Core", "supporting": "Supporting"},
            "strength": {"strong": "Strong", "moderate": "Moderate", "weak": "Weak", "none": "None"},
            "status": {"strong": "Supported", "partial": "Partly supported", "weak": "Weakly supported", "none": "Not supported", "conflicting": "Contradicted by the material"},
        },
        "det_cols": ["Dimension", "Criterion", "Points", "Comment"],
        "mat_cols": ["Material", "Type"],
        "footer": "Prepared with the Employer Brand Auditor plugin. The audit assesses only the material supplied: how it reads to a candidate and what supports it. Facts about the company were not independently verified. Check rewritten copy and every figure before publishing.",
        "parse_error": "The report data could not be read. Ask the plugin to rebuild the HTML report.",
        "print": "Save as PDF",
        "howto_toggle": "Show or hide the explanation",
        "howto_html": """
<p class="lead">The audit reads candidate-facing material the way a person choosing a job reads it: the careers page, the employer value proposition (EVP), job ads, employee stories. It answers three questions: what you promise, what backs it up, and what to fix first.</p>
<div class="howto-grid">
  <div class="howto-card"><h4>The rule</h4><p>No proof in the material, no claim in the report. The audit does not invent facts, figures or market comparisons. When proof is missing from the copy, it means only that a candidate cannot see it. It does not mean the practice does not exist.</p></div>
  <div class="howto-card"><h4>Score out of 100</h4><p>The sum of the eight dimensions below. They carry different weights. Differentiation and proof weigh most, 16 points each: without them the rest stays general. Scale: 85–100 distinctive, 70–84 strong with gaps, 50–69 works but generic, 30–49 weak, below 30 no proposition visible. It is not a ranking or a comparison with other employers.</p></div>
  <div class="howto-card"><h4>Coverage</h4><p>The share of the 34 criteria that could be assessed. When material is missing, for example there is no employee story, those criteria are left out rather than scored zero, and the score is computed from the rest. Below 40% coverage no overall score is given.</p></div>
  <div class="howto-card"><h4>Score reliability</h4><p>High when coverage is at least 80% and at least three different types of material were supplied. Medium when one of these is missing. Low when there is little material; the score is then provisional. Reliability describes how complete the material is. It does not mean the facts in it were checked.</p></div>
</div>
<h4 class="howto-h">The genericity test</h4>
<p>Each main claim is tested with four questions.</p>
<ul class="howto-list">
  <li><b>Substitution.</b> Replace the company's name with "a similar employer in the same sector". If the sentence is still true, it fits anyone. If it becomes untrue, it contains something only yours: a place, a figure, a specific practice.</li>
  <li><b>Stock phrases.</b> Whether the sentence is built from standard phrases such as "great team" or "growth opportunities".</li>
  <li><b>Specifics.</b> Figures with time frames, named practices, conditions, constraints.</li>
  <li><b>Can you own it.</b> Whether the claim rests on something the company really has and the material shows.</li>
</ul>
<h4 class="howto-h">Labels in the text</h4>
<ul class="howto-list">
  <li><span class="tag tag-q">Confirm</span> a likely fact the company needs to confirm. Until then it is not used as a fact.</li>
  <li><span class="tag tag-e">Information needed</span> the material does not contain it, and the copy cannot be strengthened without it.</li>
  <li><b>Supported, partly, weakly, not supported</b>: how well a claim is backed inside the material itself. This is not independent fact-checking.</li>
</ul>
""",
    },
}

# ---------------------------------------------------------------------------
# Template (CSS + markup + renderer). __LANG__, __I18N__, __TITLE__ are filled per language.
# ---------------------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#16141F;--soft:#5D5A6B;--line:#E4E1EA;--paper:#FBFAF7;--card:#FFFFFF;--accent:#6B3FD4;--accent2:#19B6C9;--hi:#D6455D;--mid:#E39B1A;--lo:#8B8898;--ok:#1F9D6B;--tint:#F2EEFB}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 Onest,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:40px 28px 80px}
h1,h2,h3,h4{line-height:1.15;margin:0}
h2{font-size:30px;font-weight:800;letter-spacing:-.01em;margin:64px 0 20px;padding-top:12px;border-top:3px solid var(--ink)}
h3{font-size:21px;font-weight:700}
h4{font-size:16px;font-weight:700}
p{margin:0 0 12px}
ul{margin:0;padding-left:20px}
li{margin:4px 0}
.muted{color:var(--soft)}
.kicker{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
/* cover */
.cover{display:grid;grid-template-columns:1.4fr 1fr;gap:28px;align-items:stretch;margin-bottom:8px}
.cover-main{background:var(--ink);color:#fff;border-radius:18px;padding:36px;display:flex;flex-direction:column;justify-content:space-between;min-height:320px;position:relative;overflow:hidden}
.cover-main:after{content:"";position:absolute;right:-90px;top:-90px;width:300px;height:300px;border-radius:50%;background:conic-gradient(from 90deg,var(--accent2),var(--accent),#FF5FA2,var(--accent2));filter:blur(60px);opacity:.55}
.cover-main h1{font-size:46px;font-weight:800;letter-spacing:-.02em;position:relative;z-index:1}
.cover-main .kicker{color:#C9B8FF;position:relative;z-index:1}
.cover-meta{position:relative;z-index:1;color:#CFCBDC;font-size:15px}
.verdict{font-size:18px;line-height:1.5;font-weight:400;color:#E9E6F2;position:relative;z-index:1;margin:22px 0}
.scorebox{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px;display:flex;flex-direction:column;gap:18px}
.ring{display:flex;align-items:center;gap:20px}
.ring svg{width:132px;height:132px;flex:none}
.ring .num{font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1}
.ring .num small{font-size:20px;color:var(--soft);font-weight:500}
.band{font-size:15px;color:var(--soft);line-height:1.4}
.metric{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-top:12px;font-size:15px}
.metric b{font-size:17px}
.metric span.h{display:block;color:var(--soft);font-size:13px;line-height:1.35}
.pill{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:4px 10px;border-radius:99px;background:var(--tint);color:var(--accent)}
.pill.prov{background:#FFF4DC;color:#9A6400}
/* nav */
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0}
.toc a{font-size:14px;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--card);border-radius:99px;padding:6px 14px}
.toc a:hover{border-color:var(--accent);color:var(--accent)}
/* summary */
.summary{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}
.panel h3{margin-bottom:12px}
.actions li{margin:8px 0}
/* howto */
.lead{font-size:19px;line-height:1.5}
.howto-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:18px 0 8px}
.howto-card{background:var(--tint);border-radius:14px;padding:20px}
.howto-card h4{margin-bottom:8px;color:var(--accent)}
.howto-card p{font-size:15.5px;margin:0}
.howto-h{margin:26px 0 8px}
.howto-list li{margin:8px 0}
details.howto{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:6px 24px 20px}
details.howto summary{cursor:pointer;font-weight:700;padding:14px 0;color:var(--accent)}
/* scorecard */
.dim{display:grid;grid-template-columns:280px 1fr 70px;gap:18px;align-items:start;padding:16px 0;border-bottom:1px solid var(--line)}
.dim:last-child{border-bottom:0}
.dim .name{font-weight:700}
.dim .desc{font-size:13.5px;color:var(--soft);line-height:1.4;margin-top:4px}
.bar{height:14px;background:#EEEBF3;border-radius:99px;overflow:hidden;margin:4px 0 10px}
.bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.dim .why{font-size:15px}
.dim .pts{text-align:right;font-weight:800;font-size:20px}
.dim .pts small{font-size:13px;color:var(--soft);font-weight:500}
/* cards */
.cards{display:grid;gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;border-left:6px solid var(--line)}
.card.sev-critical,.card.sev-high{border-left-color:var(--hi)}
.card.sev-medium{border-left-color:var(--mid)}
.card.sev-low{border-left-color:var(--lo)}
.card.good{border-left-color:var(--ok)}
.card h3{margin:6px 0 10px}
.sev{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.sev-critical .sev,.sev-high .sev{color:var(--hi)}.sev-medium .sev{color:#B07400}.sev-low .sev{color:var(--lo)}
.lbl{font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--soft);margin:12px 0 4px}
blockquote{margin:6px 0;padding:10px 14px;background:#F7F5FA;border-radius:10px;font-size:15.5px}
.fix{counter-increment:fix}
.fix h3:before{content:counter(fix);display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;margin-right:12px;font-size:17px}
.cards.fixes{counter-reset:fix}
.effort{display:inline-block;font-size:13px;font-weight:600;padding:3px 10px;border-radius:8px;background:#E8F7F0;color:#13734E}
.effort.data{background:#FFF4DC;color:#9A6400}
/* rewrites */
.rw{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:10px}
.rw .before{background:#F7F5FA;border-radius:12px;padding:16px;font-size:15.5px;white-space:pre-line}
.rw .after{background:#EFFAF5;border:1px solid #CBEBDD;border-radius:12px;padding:16px;font-size:15.5px;white-space:pre-line}
/* tags */
.tag{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:7px;margin-right:6px;vertical-align:1px}
.tag-q{background:#E6F6F8;color:#0E7C8A}.tag-e{background:#FFF4DC;color:#9A6400}
.qlist{list-style:none;padding:0}
.qlist li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:8px 0}
/* tables */
table{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th{background:#F4F2F8;text-align:left;font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--soft);padding:10px 12px}
td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top}
.chip{display:inline-block;font-size:12.5px;font-weight:600;padding:2px 8px;border-radius:7px;background:#F1EFF5;white-space:nowrap}
.chip.g{background:#E8F7F0;color:#13734E}.chip.m{background:#FFF4DC;color:#9A6400}.chip.r{background:#FDE8EC;color:#B3263E}
.tblwrap{overflow-x:auto;margin:10px 0 26px}
.notice{background:#FFF4DC;border-radius:12px;padding:14px 18px;margin:18px 0}
.scope{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:18px 0;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 22px;font-size:15px}
.scope h4{margin-bottom:6px}
footer{margin-top:60px;padding-top:20px;border-top:1px solid var(--line);font-size:13.5px;color:var(--soft)}
.printbtn{position:fixed;right:18px;bottom:18px;background:var(--ink);color:#fff;border:0;border-radius:99px;padding:12px 18px;font:600 14px Onest,Arial,sans-serif;cursor:pointer}
@media (max-width:820px){.scope,.cover,.summary,.howto-grid,.rw{grid-template-columns:1fr}.dim{grid-template-columns:1fr}.dim .pts{text-align:left}.cover-main h1{font-size:34px}}
@media print{#summary + .summary{break-after:page}body{background:#fff;font-size:12pt}.wrap{max-width:none;padding:0}.printbtn,.toc{display:none}h2{break-after:avoid}.card,.dim,.panel,table,.rw{break-inside:avoid}details.howto{border:0;padding:0}.cover-main{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<button class="printbtn" onclick="window.print()" id="printbtn"></button>

<!-- Audit data. The skill replaces the placeholder below with the audit JSON (format: methodology/report-format.md). -->
<script id="report-data" type="application/json">REPORT_DATA_JSON</script>

<script>
const T = __I18N__;
const app = document.getElementById('app');
document.getElementById('printbtn').textContent = T.print;
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const txt = s => esc(s).replace(/\n/g, '<br>');
const list = (a, cls) => (a && a.length) ? `<ul${cls ? ` class="${cls}"` : ''}>${a.map(x => `<li>${txt(x)}</li>`).join('')}</ul>` : '';
const sec = (id, title, body) => body ? `<h2 id="${id}">${esc(title)}</h2>${body}` : '';
const bandKey = v => v >= 85 ? '85' : v >= 70 ? '70' : v >= 50 ? '50' : v >= 30 ? '30' : '0';
const chipCls = {strong:'g',partial:'m',weak:'m',none:'r',conflicting:'r',distinctive:'g',generic:'r',breaks:'g',bends:'m',survives:'r',rare:'g',common:'m',ubiquitous:'r',high:'g',some:'m',owned:'g',supportable:'m',unowned:'r'};
const chip = (map, k) => k ? `<span class="chip ${chipCls[k] || ''}">${esc((map && map[k]) || k)}</span>` : '';

function ring(v, max) {
  const r = 56, c = 2 * Math.PI * r, f = Math.max(0, Math.min(1, v / max));
  return `<svg viewBox="0 0 132 132"><defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#19B6C9"/><stop offset="1" stop-color="#6B3FD4"/></linearGradient></defs>
  <circle cx="66" cy="66" r="${r}" fill="none" stroke="#EEEBF3" stroke-width="12"/>
  <circle cx="66" cy="66" r="${r}" fill="none" stroke="url(#rg)" stroke-width="12" stroke-linecap="round" stroke-dasharray="${c * f} ${c}" transform="rotate(-90 66 66)"/></svg>`;
}

function render(d) {
  const s = d.score || {};
  document.title = `${T.doc_title}: ${d.company || ''}`;
  const withheld = !!s.withheld;
  let h = '';
  // cover
  h += `<div class="cover"><div class="cover-main"><div><div class="kicker">${esc(T.kicker)}</div><h1>${esc(d.company || '')}</h1>
    <p class="verdict">${txt(d.verdict)}</p></div>
    <div class="cover-meta">${esc(T.date)}: ${esc(d.date || '')} · ${esc(T.materials)}: ${(d.materials || []).length}</div></div>
    <div class="scorebox">`;
  if (withheld) {
    h += `<div><div class="kicker">${esc(T.score)}</div><h3 style="margin-top:8px">${esc(T.withheld)}</h3><p class="band">${esc(T.withheld_note)}</p></div>`;
  } else {
    h += `<div class="ring">${ring(s.value || 0, 100)}<div><div class="num">${esc(s.value)}<small>/100</small></div>
      ${s.provisional ? `<span class="pill prov">${esc(T.provisional)}</span>` : ''}</div></div>
      <p class="band">${esc(T.band[bandKey(s.value || 0)])}</p>`;
  }
  h += `<div class="metric"><div>${esc(T.coverage)}<span class="h">${esc(T.coverage_hint)}</span></div><b>${esc(s.coverage)}%</b></div>
    <div class="metric"><div>${esc(T.reliability)}<span class="h">${esc(T.rel_hint)}${s.reliability_note ? ': ' + esc(s.reliability_note) : ''}</span></div><b>${esc(T.rel[s.confidence] || s.confidence || '')}</b></div>
    </div></div>`;
  const toc = [['summary', T.sec_summary], ['howto', T.sec_howto], ['scorecard', T.sec_scorecard], ['working', T.sec_working], ['problems', T.sec_problems], ['plan', T.sec_plan], ['rewrites', T.sec_rewrites], ['questions', T.sec_questions], ['appendix', T.sec_appendix]];
  h += `<nav class="toc">${toc.map(([id, t]) => `<a href="#${id}">${esc(t)}</a>`).join('')}</nav>`;
  (d.notices || []).forEach(n => { h += `<div class="notice">${txt(n)}</div>`; });
  const sc = d.scope || {};
  if ((sc.reviewed || []).length || (sc.not_reviewed || []).length) {
    h += `<div class="scope"><div><h4>${esc(T.scope_in)}</h4>${list(sc.reviewed)}</div><div><h4>${esc(T.scope_out)}</h4>${list(sc.not_reviewed)}</div></div>`;
  }
  // summary
  const sm = d.summary || {};
  h += sec('summary', T.sec_summary, `<div class="summary"><div class="panel"><h3>${esc(T.summary_points)}</h3>${list(sm.points)}</div>
    <div class="panel"><h3>${esc(T.summary_actions)}</h3>${list(sm.actions, 'actions')}</div></div>`);
  // how to read (fixed text)
  h += sec('howto', T.sec_howto, `<details class="howto" open><summary>${esc(T.howto_toggle)}</summary>${T.howto_html}<p class="muted">${esc(T.band_scale_note)}</p></details>`);
  // scorecard
  if ((d.dimensions || []).length) {
    h += sec('scorecard', T.sec_scorecard, `<div class="panel">${d.dimensions.map(x => {
      const meta = T.dims[x.id] || [x.id, ''];
      const na = x.assessable === false;
      const pct = na ? 0 : Math.round(100 * (x.score || 0) / (x.max || 1));
      return `<div class="dim"><div><div class="name">${esc(meta[0])}</div><div class="desc">${esc(meta[1])}</div></div>
        <div><div class="bar"><i style="width:${pct}%"></i></div><div class="why">${txt(x.why)}</div></div>
        <div class="pts">${na ? `<small>${esc(T.not_assessable)}</small>` : `${esc(x.score)}<small>/${esc(x.max)}</small>`}</div></div>`;
    }).join('')}</div>`);
  }
  // what works
  h += sec('working', T.sec_working, (d.strengths || []).length ? `<div class="cards">${d.strengths.map(x => `<div class="card good"><h3>${esc(x.title)}</h3><p>${txt(x.text)}</p></div>`).join('')}</div>` : '');
  // problems
  h += sec('problems', T.sec_problems, (d.problems || []).length ? `<div class="cards">${d.problems.map(x => `<div class="card sev-${esc(x.severity)}">
      <div class="sev">${esc(T.severity[x.severity] || '')}</div><h3>${esc(x.title)}</h3>
      ${(x.evidence || []).length ? `<div class="lbl">${esc(T.evidence)}</div>${x.evidence.map(e => `<blockquote>${txt(e)}</blockquote>`).join('')}` : ''}
      ${x.why ? `<div class="lbl">${esc(T.why_matters)}</div><p>${txt(x.why)}</p>` : ''}
      ${(x.flags || []).length ? `<div class="lbl">${esc(T.flags)}</div><p class="muted">${x.flags.map(f => esc((T.rf && T.rf[f]) || f)).join(' · ')}</p>` : ''}</div>`).join('')}</div>` : '');
  // plan
  h += sec('plan', T.sec_plan, (d.fixes || []).length ? `<div class="cards fixes">${d.fixes.map(x => `<div class="card fix"><h3>${esc(x.title)}</h3>
      <span class="effort ${x.needs_new_data ? 'data' : ''}">${esc(x.needs_new_data ? T.fix_data : T.fix_ready)}</span>
      <div class="lbl">${esc(T.fix_where)}</div>${list(x.steps)}
      ${x.why_first ? `<div class="lbl">${esc(T.fix_why)}</div><p>${txt(x.why_first)}</p>` : ''}
      ${(x.needs || []).length ? `<div class="lbl">${esc(T.fix_needs)}</div>${list(x.needs)}` : ''}
      ${x.effort ? `<div class="lbl">${esc(T.effort_lbl)}</div><p>${esc(T.effort[x.effort] || x.effort)}${x.effort_note ? '. ' + txt(x.effort_note) : ''}</p>` : ''}
      ${(x.who || []).length ? `<div class="lbl">${esc(T.who)}</div><p>${x.who.map(esc).join(', ')}</p>` : ''}
      ${(x.check || []).length ? `<div class="lbl">${esc(T.check)}</div>${list(x.check)}` : ''}</div>`).join('')}</div>` : '');
  // rewrites
  h += sec('rewrites', T.sec_rewrites, (d.rewrites || []).length ? `<div class="cards">${d.rewrites.map(x => `<div class="card"><h3>${esc(x.title)}</h3>
      ${x.problem ? `<div class="lbl">${esc(T.rw_problem)}</div><p>${txt(x.problem)}</p>` : ''}
      ${x.logic ? `<div class="lbl">${esc(T.rw_logic)}</div><p>${txt(x.logic)}</p>` : ''}
      <div class="rw"><div><div class="lbl">${esc(T.rw_original)}</div><div class="before">${txt(x.original)}</div></div>
      <div><div class="lbl">${esc(T.rw_rewrite)}</div><div class="after">${txt(x.rewrite)}</div></div></div>
      ${(x.notes || []).length ? `<ul class="qlist">${x.notes.map(n => `<li><span class="tag ${n.kind === 'confirm' ? 'tag-q' : 'tag-e'}">${esc(T.q_kind[n.kind] || n.kind)}</span>${txt(n.text)}</li>`).join('')}</ul>` : ''}</div>`).join('')}</div>` : '');
  // questions
  const qs = d.questions || [];
  if (qs.length) {
    const grp = k => qs.filter(q => (q.for || 'communication') === k);
    const qhtml = ['communication', 'audit'].map(k => grp(k).length ? `<h3 style="margin:18px 0 6px">${esc(T.q_for[k])}</h3><ul class="qlist">${grp(k).map(q => `<li><span class="tag ${q.kind === 'confirm' ? 'tag-q' : 'tag-e'}">${esc(T.q_kind[q.kind] || q.kind)}</span>${txt(q.text)}</li>`).join('')}</ul>` : '').join('');
    h += sec('questions', T.sec_questions, `<p class="muted">${esc(T.q_note)}</p>${qhtml}`);
  }
  // appendix
  let app2 = '';
  if ((d.genericity || []).length) {
    app2 += `<h3>${esc(T.app_genericity)}</h3><div class="tblwrap"><table><tr>${T.gen_cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${d.genericity.map(g => `<tr>
      <td>${txt(g.claim)}</td><td>${chip(T.gen.verdict, g.verdict)}</td><td>${chip(T.gen.substitution, g.substitution)}</td><td>${chip(T.gen.ubiquity, g.ubiquity)}</td>
      <td>${chip(T.gen.specificity, g.specificity)}</td><td>${chip(T.gen.defensibility, g.defensibility)}</td><td>${txt(g.why)}</td></tr>`).join('')}</table></div>`;
  }
  if ((d.ledger || []).length) {
    app2 += `<h3>${esc(T.app_ledger)}</h3><div class="tblwrap"><table><tr>${T.led_cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${d.ledger.map(l => `<tr>
      <td>${txt(l.claim)}</td><td>${esc(T.led.class[l.class] || '')}</td><td>${txt(l.evidence)}</td><td>${chip(T.led.strength, l.strength)}</td>
      <td>${chip(T.led.status, l.status)}</td><td>${txt(l.comment)}</td></tr>`).join('')}</table></div>`;
  }
  const det = (d.dimensions || []).flatMap(x => (x.criteria || []).map(c => [x.id, c]));
  if (det.length) {
    app2 += `<h3>${esc(T.app_details)}</h3><div class="tblwrap"><table><tr>${T.det_cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${det.map(([id, c]) => `<tr>
      <td>${esc((T.dims[id] || [id])[0])}</td><td>${esc(c.name)}</td><td>${c.assessable === false ? esc(T.not_assessable) : `${esc(c.score)}/${esc(c.max)}`}</td><td>${txt(c.note)}</td></tr>`).join('')}</table></div>`;
  }
  const safeUrl = u => /^https?:\/\//i.test(String(u || '')) ? esc(u) : '';
  if ((d.sources || []).length) {
    app2 += `<h3>${esc(T.app_sources)}</h3><div class="tblwrap"><table><tr>${T.src_cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${d.sources.map(s => `<tr><td>${esc(s.title)}</td><td>${esc(s.type)}</td><td>${esc(s.captured)}</td><td>${safeUrl(s.url) ? `<a href="${safeUrl(s.url)}" target="_blank" rel="noopener noreferrer">${esc(T.open)}</a>` : ''}</td></tr>`).join('')}</table></div>`;
  }
  if ((d.materials || []).length) {
    app2 += `<h3>${esc(T.app_materials)}</h3><div class="tblwrap"><table><tr>${T.mat_cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr>${d.materials.map(m => `<tr><td>${esc(m.name)}</td><td>${esc(m.type)}</td></tr>`).join('')}</table></div>`;
  }
  h += sec('appendix', T.sec_appendix, app2);
  h += `<footer>${esc(T.footer)}${d.plugin_version ? ` · Employer Brand Auditor v${esc(d.plugin_version)}` : ''}</footer>`;
  app.innerHTML = h;
}

try {
  render(JSON.parse(document.getElementById('report-data').textContent));
} catch (e) {
  app.innerHTML = `<div class="notice">${esc(T.parse_error)}</div>`;
  console.error(e);
}
</script>
</body>
</html>
"""


def compact(html):
    """Trim indentation and blank lines so the template is cheaper to copy into each report."""
    lines = [ln.strip() for ln in html.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang, t in I18N.items():
        html = (TEMPLATE.replace("__LANG__", lang)
                .replace("__TITLE__", t["doc_title"])
                .replace("__I18N__", json.dumps(t, ensure_ascii=False)))
        html = compact(html)
        assert html.count(DATA_SLOT) == 1
        path = os.path.join(OUT, f"audit-report.{lang}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote", os.path.relpath(path, ROOT), len(html.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
