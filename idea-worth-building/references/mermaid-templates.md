# Mermaid Templates

Write all labels in the report language. Templates are in English; a Turkish glossary is at the end.
Replace every `{...}` with real content — the quality-gate script fails on leftover placeholders.

## Syntax safety rules (broken diagrams are the most common failure)

- Wrap node labels in double quotes: `A["Gate 1: Done before?"]`. Non-ASCII letters are fine inside quotes in flowcharts.
- Never put `"` inside a label; use `'`. Avoid `#`, `;`, `{}`, `<>` in label text. Line break: `<br/>`.
- Edge labels: `A -->|"Yes"| B`. Node IDs: ASCII, no spaces.
- Every flowchart node gets exactly one class: `pass`, `fail`, `unknown` or `idle`.
- quadrantChart and gantt text: prefer plain ASCII (drop diacritics, no quotes/parentheses/colons in names) — some renderers fail otherwise. Quadrant coordinates between 0 and 1.
- gantt: `dateFormat YYYY-MM-DD`, start from the analysis date, ASCII task IDs.
- After writing, render with `check_report.py` (uses `mmdc` if installed); otherwise re-read each block for syntax errors.

## 1. Decision map (5 gates, coloured by this idea's result)

Mark every node on the path the idea actually took as `pass` / `fail` / `unknown`; untraveled nodes `idle`.
Put a short evidence note in each gate label (e.g., "12 competitors found").

```mermaid
flowchart TD
    START["START<br/>{idea name}"] --> G1["1. Done before?<br/>{short finding}"]
    G1 -->|"No"| G2N["2. Is there a need?<br/>validate with 5 users"]
    G1 -->|"Yes"| G2Y["2. What is your difference?<br/>faster / cheaper / other audience / better UI"]
    G2N -->|"No"| K1["Change or drop the idea"]
    G2N -->|"Yes"| G3
    G2Y --> DIFF{"Clear difference?<br/>{short finding}"}
    DIFF -->|"No"| DEV1["Develop the idea"]
    DEV1 --> G2Y
    DIFF -->|"Yes"| G3["3. Testable without code?"]
    G3 -->|"Yes"| NC["No-code test<br/>{suggested tool}"]
    NC --> INT{"Is there interest?"}
    INT -->|"No"| DEV2["Develop or change the idea"]
    INT -->|"Yes"| G5
    G3 -->|"No"| G4["4. MVP in 1 week?<br/>{time estimate}"]
    G4 -->|"No"| SHRINK["Shrink scope<br/>one core feature"]
    SHRINK --> G4
    G4 -->|"Yes"| MVP["Code the MVP<br/>test with real users"]
    MVP --> G5["5. 10 people spend money or time?<br/>{short finding}"]
    G5 -->|"No"| K2["Change or drop the idea"]
    G5 -->|"Yes"| GO["WORTH BUILDING"]
    GO --> BUILD["Build now<br/>focus, finish the MVP"]
    START --> VERDICT["VERDICT: {verdict} · {score}/100"]

    classDef pass fill:#d4edda,stroke:#28a745,color:#155724
    classDef fail fill:#f8d7da,stroke:#dc3545,color:#721c24
    classDef unknown fill:#fff3cd,stroke:#ffc107,color:#856404
    classDef idle fill:#f4f4f4,stroke:#bbb,color:#888
    classDef verdict fill:#1f2937,stroke:#111,color:#fff
    class START,G1 pass
    class G2Y,DIFF unknown
    class G2N,K1,DEV1,G3,NC,INT,DEV2,G4,SHRINK,MVP,G5,K2,GO,BUILD idle
    class VERDICT verdict
```
(The `class` lines are an example — set them from the analysis. Gates waiting on the founder's real-user evidence are `unknown`.)

## 2. Competitor positioning quadrant

Choose the two axes that best expose the gap (price vs specialisation, ease vs depth, local vs global…).
Plot real competitors and the idea itself.

```mermaid
quadrantChart
    title Competitor positioning
    x-axis Low price --> High price
    y-axis General purpose --> Niche specific
    quadrant-1 Premium specialists
    quadrant-2 Opportunity zone
    quadrant-3 Crowded cheap
    quadrant-4 Premium generalists
    Competitor A: [0.8, 0.3]
    Competitor B: [0.2, 0.25]
    Our idea: [0.3, 0.8]
```

## 3. 30-day validation roadmap

Replace `{START_DATE}` with the analysis date (YYYY-MM-DD). Tie each week to a gate and a go/stop point.

```mermaid
gantt
    title 30 day validation roadmap
    dateFormat YYYY-MM-DD
    section Week 1 - Need
    5 user interviews              :w1a, {START_DATE}, 5d
    Review interviews go or stop   :milestone, w1m, after w1a, 0d
    section Week 2 - No-code test
    Landing page and waitlist      :w2a, after w1m, 3d
    Share in communities           :w2b, after w2a, 4d
    section Week 3 - MVP
    One-feature MVP                :w3a, after w2b, 7d
    section Week 4 - Payment
    Pre-sale offer to 10 people    :w4a, after w3a, 7d
    Decision                       :milestone, w4m, after w4a, 0d
```

## Turkish glossary

START → BAŞLANGIÇ · Done before? → Daha önce yapıldı mı? · Is there a need? → İhtiyaç var mı? ·
What is your difference? → Senin farkın ne? · Clear difference? → Net fark var mı? ·
Develop the idea → Fikri geliştir · Change or drop the idea → Fikri değiştir / iptal et ·
Testable without code? → Kodlamadan test edebilir misin? · Is there interest? → İlgi var mı? ·
MVP in 1 week? → MVP'yi 1 haftada çıkarabilir misin? · Shrink scope → Kapsamı küçült ·
10 people spend money or time? → Buna para veya zaman harcayacak 10 kişi bulabilir misin? ·
WORTH BUILDING → KODLAMAYA DEĞER · Build now → Şimdi kodla · VERDICT → KARAR ·
Yes/No → Evet/Hayır
