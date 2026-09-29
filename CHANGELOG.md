# Changelog

## 1.1.0 — 2026-09-30

### Added
- **Riskiest assumption** (Phase 7, report §11): must-be-true assumptions rated by importance and
  evidence; the riskiest one is named and Week 1 of the 30-day roadmap tests it.
- **Existing-owner check** (Phase 0, playbook §0): when an idea comes from an existing product or
  organisation, the skill first researches that owner's own stated plans.
- **Vendor-claim rule:** claims from companies that sell the solution are tagged as estimates
  unless an independent source confirms them.
- `check_report.py` warns when section 11 has no assumption table.

### Changed
- **Pain** is judged on severity × frequency × urgency (rubric, Phase 2, playbook §2).
- **Confidence cap:** `score.py` caps any `low`-confidence criterion at 3 and prints a note;
  `--json` output lists capped criteria.
- README: one-click release zip, current Claude.ai upload path, prerequisites, update steps
  (English and Turkish).

## 1.0.0 — 2026-09-27
- First public release.
