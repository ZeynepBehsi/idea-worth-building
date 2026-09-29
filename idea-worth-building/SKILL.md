---
name: idea-worth-building
description: Evaluates whether any product, startup, app, SaaS, open-source or side-project idea is worth coding before development starts. Runs deep web research (20+ searches) comparing the user's local market with global — competitors, TAM/SAM/SOM, niche, pricing, costs, unit economics, profit, competition, distribution, regulation — passes the idea through a 5-gate decision tree, scores it with scripts, and delivers a Markdown report with Mermaid decision map, competitor quadrant and 30-day roadmap, ending in GO / VALIDATE FIRST / PIVOT / NO-GO. Also re-evaluates an idea when the user returns with interview or test results. Use whenever someone shares an idea and asks if it is worth building, or wants market research, competitor analysis, idea validation, feasibility or MVP scoping — in any language, e.g. "bu fikir kodlamaya değer mi", "fikrimi analiz et", "pazar araştırması yap", "rakip analizi", "geliştirmeye değer mi".
---

# Idea Worth Building

Turn any raw idea into an evidence-based build / don't-build decision. The backbone is a 5-gate
decision tree; every gate is fed by
real web research and every number that matters is computed by a script, not by feel.

The most important property of this skill: **it must be willing to say no.** Founders already
over-believe in their ideas; an assistant that cheers along makes them spend weeks building
something nobody uses or pays for. Be warm about the person, strict about the evidence.

This skill is project-agnostic. Never assume anything about the user's idea, skills, market or
goals that they didn't state or that the research didn't show.

## Files

| File | Read when |
|---|---|
| `references/idea-types.md` | Phase 0, after classifying the idea — type-specific checks and pitfalls |
| `references/locale-packs.md` | Phase 0, after fixing the local market — where to find local data |
| `references/research-playbook.md` | Before Phase 1 — query templates, market sizing method, search plan |
| `references/scoring-rubric.md` | Phase 8 — criteria, goal profiles, kill criteria, verdict rules |
| `references/report-template.md` | Phase 9 — exact report structure |
| `references/mermaid-templates.md` | Phase 9 — diagram templates and syntax rules |
| `scripts/unit_economics.py` | Phase 6 — margins, LTV, CAC payback, break-even, 12-month scenarios |
| `scripts/score.py` | Phase 8 — weighted score, uncertainty range, verdict |
| `scripts/check_report.py` | Phase 10 — quality gate before delivery |

Scripts need only Python 3 standard library. Run them from the skill folder.

## Environment

- **Claude.ai:** web search/fetch tools; bash tool for scripts; save the report to `/mnt/user-data/outputs/<slug>-report.md` (or the equivalent word in the report language) and present it.
- **Claude Code / other agents:** WebSearch/WebFetch; save to `./idea-reports/<slug>-report.md`.
- No web access → stop and say so. Without research this skill is only an opinion, and presenting it as analysis would mislead the user.

## Evidence tags (use on every factual line)

- **[✓ Verified]** — from a source you actually retrieved; link it.
- **[~ Estimate]** — your reasoned estimate; show assumption and arithmetic.
- **[? Needs you]** — only the founder can know or test this (user conversations, their time, budget).

Translate the tag words into the report language (TR: Doğrulandı / Tahmin / Senin cevabın gerek) but
keep the symbols `✓ ~ ?` — the quality-gate script counts them. Never upgrade an estimate to verified.
When sources conflict, show the range and both sources.

## Modes

1. **New analysis** (default) — full workflow below, deep research.
2. **Quick scan** — only if the user explicitly asks for a fast/short check: 8–12 searches, same structure, header clearly says "Quick scan — lower confidence", and the verdict can't be better than VALIDATE FIRST.
3. **Re-evaluation** — the user returns with results (interviews, landing-page numbers, pre-sales) or a changed idea. If a previous report exists in the conversation or files, reuse its research, update only affected gates, re-run the scripts, and add a "What changed" section showing old vs new score and verdict. Treat real-user evidence as the strongest evidence in the whole analysis.
4. **Pivot exploration** — when the verdict is PIVOT (or the user asks), generate 2–3 concrete alternative angles (different niche, different payer, different format), research each briefly (3–4 searches each), score each with `score.py`, and compare in a table.

## Workflow

### Phase 0 — Intake and framing

The idea may arrive as a sentence, a long description, a file (pitch deck, PDF, doc) or a URL — read
whatever is provided first. Then extract: one-sentence idea, target user, problem, solution, revenue
idea, platform, and founder constraints.

Settle these four framing decisions, because they change the whole analysis:

1. **Project goal** → scoring profile: `commercial` (make money — default), `portfolio` (learning / showcase / CV), `internal` (tool for own team or company), `opensource` (community project). A portfolio project shouldn't fail because it has no business model.
2. **Idea type** — B2C app, B2B SaaS, marketplace, API/devtool, AI-wrapper, hardware/IoT, content/community/education, e-commerce/D2C, or a mix. Read the matching sections of `references/idea-types.md`.
3. **Local market** — the user's stated market; else infer from the language they write in or context they gave; if still unclear, ask. The analysis always compares **local market vs global** (if the user is global-only, compare the two most relevant regions). Read the matching section of `references/locale-packs.md`.
4. **Report language** — the user's language unless they ask otherwise.

If critical facts are missing, ask **one batch** of at most 5 questions (use a tappable-options tool
if available): who is the first user; how will it make money / what the goal is; have they talked to
any potential users and what they heard; time and budget for the next 3 months; any unfair advantage
(data, audience, expertise, channel). If the user says "just analyze", proceed and mark those items
[? Needs you]. Restate the idea and your assumptions in 2–3 lines, then start research.

**Existing-owner check.** If the idea is inspired by, copied from or built on an existing product,
company, lab or non-profit, first search what *that owner* has said about its own plans (pricing,
licensing, commercial roadmap, open-sourcing, partnerships) in its site, press releases and recent
interviews. "They don't sell it" and "they plan to sell it" lead to completely different analyses;
state which one the evidence shows before Gate 1.

### Phase 1 — Gate 1: Has it been done before?

Follow `research-playbook.md` §1. Search in English **and** in the local language separately — "no
local competitor but ten global ones" is a very different situation from "crowded locally". Find
5–10+ competitors across three types: direct, indirect, and the do-nothing substitute (spreadsheet,
messaging groups, a human service, paper).

For each: name, country, pricing, segment, key features, traction signals, and **top complaints**
from low-star reviews. Complaints are the most valuable output of this phase — differentiation
usually lives there.

"Nobody has done this" is usually a warning: either the search was too narrow or there's no demand.
Search harder with synonyms and adjacent categories before accepting it, and say which explanation
you believe.

### Phase 2 — Gate 2: Is there real need / what is the difference?

- Pain evidence: forums, Reddit, local complaint sites, app reviews, workarounds people built, jobs that pay humans to do the task.
- Judge pain on three axes, not one: **severity** (how bad when it happens), **frequency** (daily, monthly, once a year?) and **urgency** (must it be solved now, or can it wait?). A severe but once-a-year problem is a much weaker business than a moderate daily one; say which pattern the evidence shows.
- Differentiation matrix vs top 3–5 competitors: faster / cheaper / different audience / better UX / different business model / local advantage (language, local pricing and payments, local regulation).
- **Net difference?** It counts only if a user would switch for it. "Uses AI" alone is not a difference.
- Desk research can at best reach "Partial — desk research". A full pass needs the founder's 5 user conversations. Provide a 5–7 question interview script about past behaviour ("last time this happened, what did you do?"), not hypothetical future ("would you use…?").

### Phase 3 — Market size, niche, target market

Follow playbook §3. TAM/SAM/SOM for the local market and for global, **bottom-up first** (reachable
customers × realistic conversion × price), top-down report numbers only as a sanity check. Then:
beachhead niche, growth/timing signals, competition intensity (Low/Medium/High with reasons), and a
local vs global comparison table with a recommendation of where to start and why.

### Phase 4 — Gate 3: Can it be tested without code?

Design a concrete no-code test for this idea: landing page + waitlist, fake-door pricing, concierge /
manual service, survey, template, demo video, pre-sale. Name the tools, the specific communities to
post in, the metric, and a **success threshold fixed in advance**.

### Phase 5 — Gate 4: Can the MVP ship in about a week?

One core feature; an explicit "not in v1" list; build-time estimate for a solo AI-assisted developer
(adjust if the user told you their team or skill level). If > 1–2 weeks, shrink scope and re-estimate.
Look up **current** prices (never from memory) for APIs/models, hosting, DB, auth, store and payment
fees, and derive cost per active user per month.

### Phase 6 — Gate 5: Will 10 people spend money or time on it?

Pricing benchmark from competitors (local currency and USD, with exchange-rate date), revenue-model
recommendation. Put the inputs in a JSON file and run:

```bash
python scripts/unit_economics.py ue.json
```

Paste its tables into the report and interpret them; don't recompute by hand. For non-commercial
profiles, replace revenue with the relevant value measure (time saved × users for internal tools;
adoption/contributor signals for open source; skills demonstrated for portfolio) and skip the script
if it doesn't apply. Give the exact way to find the 10 people (who, where, what offer).

### Phase 7 — What the 5 gates miss

- **Distribution:** 2–3 realistic channels to the first 100 users, with cost.
- **Founder fit:** only from what the user told you about their skills, time and situation; otherwise [? Needs you].
- **Risks:** regulation (data protection, health, finance, minors, education claims), platform dependency, big-player risk (could a large company ship this as a feature?).
- **Devil's advocate:** the 3 strongest reasons this fails, argued seriously and specifically.
- **Riskiest assumptions:** list 5–8 things that *must be true* for the idea to work (users have the problem, they will switch, they will pay this price, the channel works, the tech is feasible, the law allows it). Rate each for **importance** (H/M/L) and **current evidence** (strong/weak) in a table. The one with high importance and the weakest evidence is **the riskiest assumption**; name it in one sentence. Week 1 of the 30-day roadmap must test it, because if it is false nothing else matters.

### Phase 8 — Scoring and verdict

Read `references/scoring-rubric.md`, write `scores.json`, run:

```bash
python scripts/score.py scores.json --profile <commercial|portfolio|internal|opensource> --lang <tr|en>
```

Evidence quality caps the score: a criterion with `low` confidence can't score above 3, and the
script enforces this (it caps the value and prints a note). Use the script's score, range, verdict and kill-flag output as-is. If you disagree with the verdict,
say so and explain — never tweak scores to reach a verdict you prefer.

### Phase 9 — Write the report

Follow `report-template.md` and `mermaid-templates.md`. One Markdown file with the coloured decision
map, competitor quadrant, 30-day roadmap, and full report. Diagram labels in the report language.

### Phase 10 — Quality gate (don't skip)

```bash
python scripts/check_report.py <report.md> --min-searches 20   # 8 for quick scan
```

It checks sections, diagrams, evidence tags, sources, leftover placeholders and — if `mmdc` is
installed — that every Mermaid block renders. Fix every error and re-run until it passes. Only then
deliver.

In chat, give only: verdict and score, top 3 findings, the one action for this week, and the file.
Don't paste the report into chat.

## Research quality rules

- Deep mode: at least 20 searches (typically 25–35) plus fetching 5–10 key pages. Count them; list sources at the end.
- Use the current year in time-sensitive queries — take it from the environment/date, never hard-code one.
- Each query meaningfully different; reformulate on misses.
- Primary sources (pricing pages, official statistics, store listings) over SEO listicles.
- Date every market number; flag anything older than 3 years.
- **Check who is talking.** A claim made by a company that sells the solution (market size from a vendor blog, "few experts exist" from a consultancy that sells the expertise, a competitor's own traction numbers) is a vendor claim: tag it `[~ Estimate]` with "(vendor claim)" — TR "(satıcı beyanı)" — unless an independent source confirms it.
- If the research contradicts the founder's assumption, say so plainly and early.
