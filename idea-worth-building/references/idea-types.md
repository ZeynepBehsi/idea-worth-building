# Idea Types — type-specific checks

Read only the sections that match the idea (mixes are common: e.g., an AI-wrapper B2C app). Rules of
thumb below are heuristics to *verify with current sources*, not facts to quote.

## Contents
B2C app · B2B SaaS · Marketplace · API / devtool · AI-wrapper · Hardware / IoT ·
Content / community / education · E-commerce / D2C · Non-commercial goals

---

## B2C app (mobile / web consumer)
- Key questions: how often is the problem felt (daily beats yearly)? who pays — the user, a parent, an employer?
- Metrics to research: category conversion to paid, retention benchmarks (day-1/day-30), store rankings, typical subscription prices in the local market.
- Pitfalls: consumers say "I'd use it" and don't pay; paid acquisition often costs more than LTV; store commission 15–30%; retention collapses after novelty.
- Distribution: short-video platforms, communities, SEO, referral loops. Paid ads rarely work before retention is proven.

## B2B SaaS
- Key questions: who feels the pain vs who signs the cheque vs who uses it? What is the cost of the problem in money or hours?
- Metrics: price per seat/company from competitor pricing pages, sales cycle length, number of target companies (official business registries/statistics).
- Pitfalls: long sales cycles, integration demands, security questionnaires, "we already use a spreadsheet" inertia.
- Distribution: founder-led outreach, LinkedIn, niche associations, integrations marketplaces, partners.
- Rule of thumb: LTV/CAC ≥ 3 and CAC payback < 12 months are commonly cited healthy targets.

## Marketplace (two-sided)
- Key questions: which side is harder to get? Can one side be seeded manually? What stops users from taking transactions off-platform?
- Metrics: take rate of comparable marketplaces, liquidity (share of listings that transact), local supply counts.
- Pitfalls: chicken-and-egg; disintermediation; needs density in one geography/niche before expanding.
- MVP: usually a manual/concierge version (a form + spreadsheet + messaging) — Gate 3 fits well.

## API / devtool
- Key questions: what does the developer do today (open-source library, DIY)? Is there a free OSS alternative?
- Metrics: GitHub stars/activity of alternatives, usage-based pricing of competitors, developer community size.
- Pitfalls: developers prefer free/OSS; buyers are often not the users; docs and DX are the product.
- Distribution: GitHub, Hacker News, dev communities, content, open-core.

## AI-wrapper (product built mainly on a third-party model)
- Key questions: what is the moat besides the prompt — proprietary data, workflow integration, distribution, niche expertise?
- Must check: current model/API prices → cost per request and per active user; whether the model providers or big platforms already offer this natively or could easily.
- Pitfalls: big-player risk is highest here; margins squeezed by inference cost; quality depends on a provider's model changes and terms.
- Score `risk` and `differentiation` conservatively unless a real moat is shown.

## Hardware / IoT
- Key questions: BOM cost, manufacturing minimums, certifications (e.g., CE/FCC), shipping and returns.
- Pitfalls: "1-week MVP" rarely applies — use a prototype, video, or pre-order campaign as Gate 3/4 instead. Capital intensive; inventory risk.

## Content / community / education
- Key questions: who creates content, how is it kept fresh, what's the acquisition loop (SEO, social)?
- Metrics: search volume signals, competitor audience sizes, course/membership prices.
- Pitfalls: content is easy to copy; free alternatives (video platforms, forums); education claims and minors may raise regulatory questions.

## E-commerce / D2C
- Key questions: product margin after COGS, shipping, returns, marketplace/payment fees, ad costs.
- Pitfalls: paid acquisition dependency; marketplace competition on price; working capital tied in stock.

## Non-commercial goals

**portfolio** (learning, showcase, CV): "worth it" means it teaches something valuable, is finishable, and demonstrates skill to the intended audience (employers, clients, academia). Market research still matters for differentiation and visibility, but revenue criteria carry zero weight. Gate 5 = will ~10 relevant people look at, use or star it?

**internal** (tool for own team/company): main question is build vs buy. Compare with off-the-shelf tools and their price; value = hours saved × people × hourly cost; adoption is the main risk. Gate 5 = will 10 colleagues actually use it weekly?

**opensource**: check existing projects' activity (stars, issues, last commit), whether the gap is real, and how the project is sustained (maintainer time, sponsorship, open-core). Gate 5 = 10 people who commit time (users, contributors, issue reporters).
