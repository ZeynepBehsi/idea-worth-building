# Research Playbook

Query templates per dimension. Replace `{category}`, `{problem}`, `{task}`, `{competitor}`, `{year}`
with the idea's terms (`{year}` = the current year from the environment). Always run English and
local-language variants separately — the `[local]` lines below show the pattern; translate them into
the user's local language and use the sources from `locale-packs.md`. Use several synonyms for the category — users rarely
describe a problem with the founder's words.

## Contents
1. Competitors (Gate 1)
2. Pain & need evidence (Gate 2)
3. Market size & niche
4. Pricing & willingness to pay (Gate 5)
5. Costs (Gate 4)
6. Distribution
7. Risk & regulation
8. Suggested search plan (~28 searches)

---

## 1. Competitors (Gate 1)

Global:
- `{category} app`, `{category} software`, `best {category} tools {year}`
- `{problem} tool`, `alternatives to {known competitor}`
- `site:producthunt.com {category}`, `{category} startup funding`
- `{category} G2` / `Capterra {category}` (B2B)
- `{category} app store` / Google Play listing searches (B2C mobile)

[local] (example in Turkish: `{category} uygulaması`, `{category} platformu`, `{problem} çözümü`):
- `{category} app` / `{category} platform` / `{problem} solution` in the local language
- `{category} startup funding` in local startup media (see locale pack)
- local app store listings for the category

Per competitor, fetch the **pricing page** and one **reviews source**. Look for 1–3 star reviews:
- `{competitor} reviews complaints`, `{competitor} reddit`, and `{competitor}` + "complaint" on local complaint sites/forums

## 2. Pain & need evidence (Gate 2)

- `reddit {problem}`, `"how do you" {problem}`, `{problem} workaround`, `{problem} spreadsheet template`
- [local] `{problem}` + "how to solve" / forum / local community sites
- Job posts that pay humans to do the task: `{task} freelancer`, `{task} job` (and local-language equivalent)
- Trend signals: news coverage, growth of related communities, "Google Trends {term}" articles

Strong evidence: people paying for workarounds, building their own spreadsheets, repeated
complaints with high engagement. Weak evidence: "that would be cool" comments, listicles.

## 3. Market size & niche

**Bottom-up (primary):**
`SOM = reachable customers in beachhead × realistic conversion × annual price`
Find the count of the target unit (e.g., number of university students in a program, number of
SMEs in a sector, number of exam takers per year) from official sources:
- Local: the official statistics office and sector bodies listed in `locale-packs.md`
- Global: World Bank, OECD, UN data, Eurostat/US Census where relevant, industry associations

**Top-down (sanity check only):**
- `{category} market size {year}`, `{category} market CAGR`, [local] `{category} market size {country}`
Report publishers (Grand View, Statista, Mordor) often cover a much broader category — note it.

TAM = everyone who has the problem × annual price. SAM = those you can serve with your product/
language/channel. SOM = what you can realistically capture in 1–3 years (usually 0.5–5% of SAM for
a solo founder; justify the number).

**Local vs global comparison dimensions:** purchasing power & typical price points, willingness to
pay for software, currency volatility (pricing currency per market), payment infrastructure (local
providers vs Stripe/others for the founder's entity), competition density, language moat, distribution cost.

## 4. Pricing & willingness to pay

- Competitor pricing pages (fetch them), `{category} pricing`, [local] `{category}` + price / subscription fee
- Adjacent products the same user already pays for (anchor prices)
- Evidence of payment: paid tiers with visible reviews, revenue disclosures (Indie Hackers, open startups), funding

## 5. Costs

Always look up current prices; they change often.
- LLM/API pricing pages for the models you'd use; estimate tokens per request × requests per user
- Hosting/DB/auth (e.g., Vercel, Supabase, Firebase, Cloudflare) free-tier limits and paid tiers
- App Store ($99/year) / Google Play (one-off) fees, store commission (15–30%)
- Payment processor fees (global and local providers)
- Any data licensing costs

## 6. Distribution

- Where the target user already gathers: subreddits, Discord/Telegram groups, LinkedIn groups,
  Instagram/TikTok niches, university clubs, professional associations, local forums
- How competitors acquired users: `{competitor} growth story`, `{competitor} marketing strategy`
- Typical ad costs: `{category} CPC`, `{category} customer acquisition cost`

## 7. Risk & regulation

- `{category} regulation`, `{category}` + local data-protection law name (see locale pack), `{category} GDPR` if selling to the EU
- Sensitive areas: health data, finance/credit, children/minors, education claims, gambling-like mechanics
- Platform policy: app store rules for the category, API terms of the model provider
- Big-player risk: `{big player} launches {feature}`

## 8. Suggested search plan (~28 searches)

| Block | Searches |
|---|---|
| Competitors (English) | 5 |
| Competitors (local language) | 4 |
| Competitor reviews/complaints | 4 |
| Pain evidence (English + local) | 4 |
| Market size (bottom-up counts + top-down) | 4 |
| Pricing benchmarks | 3 |
| Costs | 2 |
| Distribution + regulation | 2 |

Plus fetch 5–10 key pages (pricing pages, review pages, statistics tables).
