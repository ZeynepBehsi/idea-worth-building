#!/usr/bin/env python3
"""Quality gate for an idea-worth-building report.

Usage: python check_report.py report.md [--min-searches 20] [--min-sources 10] [--no-render]
Exit code 0 = pass, 1 = errors found. Language-agnostic: checks structure by section numbers,
evidence tags by symbol (✓ ~ ?), diagrams by Mermaid type.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

VERDICTS = ["NO-GO", "PIVOT", "VALIDATE FIRST", "ÖNCE DOĞRULA", "GO"]
TEMPLATE_LEFTOVERS = ["Competitor A", "Competitor B", "{START_DATE}", "{idea name}", "{fikir adı}"]
PLACEHOLDER = re.compile(r"\{[A-Za-zÇĞİÖŞÜçğıöşü_][A-Za-zÇĞİÖŞÜçğıöşü_ /\-]{1,40}\}")


def find_chrome():
    for env in ("PUPPETEER_EXECUTABLE_PATH", "CHROME_PATH"):
        if os.environ.get(env) and os.path.exists(os.environ[env]):
            return os.environ[env]
    for root in (os.path.expanduser("~/.cache/puppeteer"), "/opt/pw-browsers", "/usr/bin"):
        if not os.path.isdir(root):
            continue
        for dp, _, files in os.walk(root):
            for f in files:
                if f in ("chrome", "chromium", "chromium-browser", "google-chrome") and os.access(os.path.join(dp, f), os.X_OK):
                    return os.path.join(dp, f)
    return None


def render_check(blocks):
    mmdc = shutil.which("mmdc")
    if not mmdc:
        return None, ["mmdc not installed — Mermaid render check skipped (re-read diagrams manually)"]
    chrome = find_chrome()
    errs = []
    with tempfile.TemporaryDirectory() as d:
        cfg = os.path.join(d, "p.json")
        with open(cfg, "w") as f:
            f.write('{"args":["--no-sandbox"]' + (f',"executablePath":"{chrome}"' if chrome else "") + "}")
        for i, (_, code) in enumerate(blocks):
            src, out = os.path.join(d, f"m{i}.mmd"), os.path.join(d, f"m{i}.svg")
            with open(src, "w", encoding="utf-8") as f:
                f.write(code)
            p = subprocess.run([mmdc, "-p", cfg, "-i", src, "-o", out], capture_output=True, text=True, timeout=120)
            msg = (p.stdout + p.stderr)
            if "Could not find Chrome" in msg or "Failed to launch" in msg:
                return None, ["mmdc found but no browser available — render check skipped"]
            if p.returncode != 0 or not os.path.exists(out):
                first = next((l for l in msg.splitlines() if "rror" in l), msg.strip()[:200])
                errs.append(f"Mermaid block {i + 1} failed to render: {first}")
    return errs, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--min-searches", type=int, default=20)
    ap.add_argument("--min-sources", type=int, default=None)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    min_sources = a.min_sources if a.min_sources is not None else (10 if a.min_searches >= 20 else 5)

    text = open(a.report, encoding="utf-8").read()
    errors, warnings = [], []

    # 1. Sections 1..14 by number
    nums = {int(n) for n in re.findall(r"^##\s+(\d+)\.", text, re.M)}
    missing = [n for n in range(1, 15) if n not in nums]
    if missing:
        errors.append(f"Missing numbered sections: {missing}")

    # 2. Mermaid diagrams
    blocks = [(m.group(1).strip().split()[0] if m.group(1).strip() else "", m.group(1))
              for m in re.finditer(r"```mermaid\n(.*?)```", text, re.S)]
    kinds = {k for k, _ in blocks}
    for need in ("flowchart", "quadrantChart", "gantt"):
        if not any(k.startswith(need) or (need == "flowchart" and k == "graph") for k in kinds):
            errors.append(f"Missing Mermaid diagram: {need}")
    for _, code in blocks:
        if code.strip().startswith(("flowchart", "graph")):
            if "classDef" not in code or not re.search(r"^\s*class\s", code, re.M):
                errors.append("Decision map has no pass/fail/unknown colouring (classDef + class lines)")

    # 3. Evidence tags
    ver, est, need = text.count("[✓"), text.count("[~"), text.count("[?")
    if ver < 10:
        errors.append(f"Only {ver} [✓ ...] verified tags (need ≥ 10)")
    if est < 3:
        warnings.append(f"Only {est} [~ ...] estimate tags — are estimates being passed off as facts?")
    if need < 2:
        warnings.append(f"Only {need} [? ...] tags — Gate 2 and Gate 5 normally need the founder")

    # 4. Sources
    urls = set(re.findall(r"https?://[^\s)\]>\"']+", text))
    if len(urls) < min_sources:
        errors.append(f"Only {len(urls)} distinct source URLs (need ≥ {min_sources})")

    # 5. Search count in header
    m = re.search(r"(searches|search count|arama sayısı|arama)\s*[:：]\s*(\d+)", text, re.I)
    if not m:
        errors.append("Header has no search count (e.g. 'Searches: 27' / 'Arama sayısı: 27')")
    elif int(m.group(2)) < a.min_searches:
        errors.append(f"Search count {m.group(2)} < required {a.min_searches}")

    # 6. Verdict near the top
    head = "\n".join(text.splitlines()[:40])
    if not any(v in head for v in VERDICTS):
        errors.append("No verdict (GO / VALIDATE FIRST / PIVOT / NO-GO) in the first 40 lines")

    # 7. Leftover placeholders / template samples
    left = sorted(set(PLACEHOLDER.findall(text)))
    if left:
        errors.append(f"Unfilled placeholders: {left[:10]}")
    for s in TEMPLATE_LEFTOVERS:
        if s in text:
            errors.append(f"Template sample text left in report: '{s}'")

    # 8. Riskiest-assumption table in section 11 (warning only)
    sec = re.search(r"^##\s+11\.(.*?)(?=^##\s+\d+\.|\Z)", text, re.S | re.M)
    if sec and not re.search(r"^\s*\|.*\|\s*$", sec.group(1), re.M):
        warnings.append("Section 11 has no assumption table — list must-be-true assumptions with importance and evidence")

    # 9. Render diagrams
    if not a.no_render and blocks:
        rerrs, rwarn = render_check(blocks)
        warnings += rwarn
        if rerrs:
            errors += rerrs

    print(f"Sections: {len(nums)}/14 · Diagrams: {len(blocks)} · Tags ✓{ver} ~{est} ?{need} · Sources: {len(urls)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
