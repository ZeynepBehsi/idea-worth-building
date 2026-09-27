# Scoring Rubric

Score each criterion 1–5 with a confidence: `high` (solid sourced evidence), `medium` (partial
evidence + reasoning), `low` (mostly assumption). Low confidence widens the range `score.py`
reports — intended: it shows the founder where the uncertainty lives.

Score what the evidence shows, not what the idea could become. Between two scores, pick the lower
one and say why in the note.

## Criteria

| key | Criterion | 1 = | 5 = |
|---|---|---|---|
| `pain` | Problem severity & pain evidence | No evidence anyone cares | Many complaints, people pay for workarounds |
| `market_size` | Market size (bottom-up SAM) | Too small to sustain the goal | Large and reachable |
| `timing` | Growth & timing | Shrinking / too early | Clearly growing, new enabler exists |
| `competition` | Competition intensity (inverse) | Dominant free incumbents | Few weak competitors, gaps in reviews |
| `differentiation` | Strength of difference | No reason to switch | Clear, defensible reason to switch |
| `monetization` | Willingness to pay / value capture | Nobody pays, no model | Proven payment in category, clear payer |
| `distribution` | Access to first 100 users | No identifiable channel | Founder has or can cheaply reach it |
| `mvp_feasibility` | MVP scope, time & cost | Months of work / unviable per-user cost | Ships in ~1 week, healthy per-user cost |
| `founder_fit` | Founder fit | Wrong skills / unsustainable | Strong skill + interest + situation match |
| `risk` | Regulatory & platform risk (inverse) | Blocking risk | Minimal risk |

For non-commercial profiles reinterpret: `monetization` = sustainability/ROI (internal: hours saved ×
people vs cost; opensource: sponsorship/maintainer sustainability); `market_size` = number of people
who'd use it; `founder_fit` for portfolio = learning and showcase value for the founder's goal.

## Goal profiles (weights, each sums to 100)

| key | commercial | portfolio | internal | opensource |
|---|---|---|---|---|
| pain | 15 | 10 | 25 | 20 |
| market_size | 10 | 0 | 5 | 10 |
| timing | 5 | 5 | 0 | 5 |
| competition | 10 | 5 | 10 | 10 |
| differentiation | 15 | 20 | 10 | 15 |
| monetization | 15 | 0 | 15 | 5 |
| distribution | 10 | 10 | 5 | 15 |
| mvp_feasibility | 10 | 25 | 20 | 10 |
| founder_fit | 5 | 20 | 5 | 5 |
| risk | 5 | 5 | 5 | 5 |

Criteria with weight 0 may be omitted from the JSON.
Formula: `score = Σ weight × (s − 1) / 4` → 0–100.

## Kill criteria (any one → NO-GO regardless of score)

- `free_dominant_no_diff` — a free, dominant incumbent does the same job and differentiation ≤ 2
- `negative_unit_economics` — cost per active user exceeds realistic price (commercial) or cost exceeds value (internal), with no path to fix
- `regulatory_blocker` — legal barrier the founder can't realistically clear
- `no_payer` — nobody identifiable can pay (commercial profile only; ignored for portfolio/opensource)

## Verdict rules (applied by the script)

- **NO-GO** — any applicable kill flag, or score < 40
- **PIVOT** — 40–59; run pivot exploration
- **VALIDATE FIRST** — ≥ 60 but Gate 2 or Gate 5 not confirmed by real people (the normal result of desk research)
- **GO** — ≥ 75 and both Gate 2 and Gate 5 confirmed with real-world evidence from the founder

## JSON format

```json
{
  "idea": "Appointment reminder SaaS for small veterinary clinics",
  "scores": {
    "pain": {"score": 4, "confidence": "medium", "note": "No-show complaints in vet forums"},
    "market_size": {"score": 3, "confidence": "high", "note": "Clinic count from statistics office"}
  },
  "gate2_confirmed_by_users": false,
  "gate5_confirmed_by_users": false,
  "kill_flags": [{"flag": "free_dominant_no_diff", "reason": "..."}]
}
```
All criteria with non-zero weight in the chosen profile are required.
