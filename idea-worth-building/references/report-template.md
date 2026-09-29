# Report Template

Keep the numbered sections exactly (the quality-gate script checks numbers 1–14); translate headings
into the report language — Turkish equivalents are given in brackets. Write prose inside sections;
use tables where data is naturally tabular. Every factual line carries an evidence tag.

`{Local}` = the local market chosen in Phase 0 (e.g., Türkiye, Germany, India).
For non-commercial profiles, adapt sections 6 and 9 as described in `scoring-rubric.md`.

```markdown
# {Idea name} — Worth Building?            [— Kodlamaya Değer mi?]
*Date: YYYY-MM-DD · Searches: N · Markets: {Local} + Global · Profile: commercial · Mode: deep*
[*Tarih · Arama sayısı: N · Pazar · Profil · Mod*]

## 1. Verdict summary                        [Karar Özeti]
- **Verdict:** GO / VALIDATE FIRST / PIVOT / NO-GO · **Score:** x/100 (range lo–hi)
- 3–5 sentences: why, strongest signal, biggest risk.
- **This week's one action:** concrete, doable in 7 days.

## 2. Decision map                           [Karar Haritası]
Mermaid flowchart (the idea's path through the 5 gates, coloured).
Table: Gate | Status (Pass / Fail / Unknown / Partial) | Basis

## 3. Idea and assumptions                   [Fikir ve Varsayımlar]
One-sentence idea, target user, solution, revenue/goal, idea type, assumptions made.

## 4. Competitor analysis (Gate 1)           [Rakip Analizi]
Table: Competitor | Country | Type (direct/indirect/substitute) | Price | Segment | Strength | Top complaint | Source
Mermaid quadrantChart.
Opportunities found in competitor complaints. If "no competitors": demand gap or narrow search?

## 5. Need and differentiation (Gate 2)     [İhtiyaç ve Farklılaşma]
Pain evidence (sourced), judged on severity, frequency and urgency. Differentiation matrix. Net difference? — reasoned.
**Your homework:** 5 user conversations + 5–7 question interview script.

## 6. Market size and niche                 [Pazar Büyüklüğü ve Niş]
TAM/SAM/SOM table with {Local} and Global columns; bottom-up steps shown.
Top-down report numbers (sanity check only).
Beachhead niche. Growth/timing. Competition intensity: Low / Medium / High.
**{Local} vs Global** table (purchasing power, willingness to pay, competition, distribution,
payments, language advantage) + where to start and why.

## 7. Test without code (Gate 3)            [Kodlamadan Test]
Concrete no-code test, tools, where to post, metric, **success threshold set in advance**.

## 8. MVP scope and cost (Gate 4)           [MVP Kapsamı ve Maliyet]
One core feature; "not in v1" list; time estimate.
Cost table: item | unit price (source, date) | monthly estimate. **Cost per active user per month.**

## 9. Revenue model and unit economics (Gate 5)   [Gelir Modeli ve Birim Ekonomisi]
Price proposal (local currency + USD), model. `unit_economics.py` output tables + interpretation.
**Your homework:** where and with what offer to find the 10 people.

## 10. Distribution, founder fit, risks     [Dağıtım, Kurucu Uyumu, Riskler]
2–3 channels for the first 100 users + cost. Founder fit (only what the user stated). Regulation /
platform / big-player risk.

## 11. Devil's advocate and riskiest assumption   [Şeytanın Avukatı ve En Riskli Varsayım]
The 3 strongest, specific reasons this fails.
Table: Assumption (must be true) | Importance H/M/L | Evidence strong/weak | Cheapest test.
One sentence: **the riskiest assumption** (high importance, weakest evidence).

## 12. Scoring                              [Puanlama]
`score.py` output as-is (+ your disagreement, if any, explained).

## 13. 30-day validation roadmap            [30 Günlük Doğrulama Yol Haritası]
Mermaid gantt. A continue/stop criterion for each week. Week 1 tests the riskiest assumption from §11.

## 14. Sources                              [Kaynaklar]
Numbered: title — URL — accessed date.

## 15. What changed (re-evaluation mode only)      [Ne Değişti]
Old vs new score and verdict per gate; which new evidence caused it.

## 16. Pivot options (when verdict is PIVOT)       [Pivot Seçenekleri]
2–3 alternatives, each with brief research, score and one-line verdict, compared in a table.
```

Chat reply after the file: verdict + score, top 3 findings, this week's one action, the file.
