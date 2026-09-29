#!/usr/bin/env python3
"""Weighted idea score + verdict.

Usage: python score.py scores.json [--profile commercial|portfolio|internal|opensource]
                                   [--lang en|tr] [--json]
"""
import argparse
import json
import sys

PROFILES = {
    "commercial": dict(pain=15, market_size=10, timing=5, competition=10, differentiation=15,
                       monetization=15, distribution=10, mvp_feasibility=10, founder_fit=5, risk=5),
    "portfolio": dict(pain=10, market_size=0, timing=5, competition=5, differentiation=20,
                      monetization=0, distribution=10, mvp_feasibility=25, founder_fit=20, risk=5),
    "internal": dict(pain=25, market_size=5, timing=0, competition=10, differentiation=10,
                     monetization=15, distribution=5, mvp_feasibility=20, founder_fit=5, risk=5),
    "opensource": dict(pain=20, market_size=10, timing=5, competition=10, differentiation=15,
                       monetization=5, distribution=15, mvp_feasibility=10, founder_fit=5, risk=5),
}
LABELS = {
    "en": dict(pain="Pain (severity x frequency x urgency)", market_size="Market size",
               timing="Growth / timing", competition="Competition (inverse)",
               differentiation="Differentiation", monetization="Willingness to pay / value",
               distribution="Distribution (first 100 users)", mvp_feasibility="MVP time / cost",
               founder_fit="Founder fit", risk="Regulatory / platform risk (inverse)"),
    "tr": dict(pain="Acı (şiddet x sıklık x aciliyet)", market_size="Pazar büyüklüğü",
               timing="Büyüme / zamanlama", competition="Rekabet (ters)",
               differentiation="Farklılaşma", monetization="Ödeme isteği / değer",
               distribution="Dağıtım (ilk 100 kullanıcı)", mvp_feasibility="MVP süresi / maliyeti",
               founder_fit="Kurucu uyumu", risk="Regülasyon / platform riski (ters)"),
}
TEXT = {
    "en": dict(title="Scoring", crit="Criterion", w="Weight", s="Score (1-5)", c="Confidence",
               contrib="Contribution", note="Note", total="Total", rng="uncertainty range",
               verdict="Verdict", kills="Kill criteria", profile="Profile",
               todo="Real-world evidence still needed for GO",
               g2="Gate 2 (5 user conversations)", g5="Gate 5 (10 people committing money/time)",
               ignored="Ignored for this profile",
               capped="Capped at 3 because confidence is low (raise the evidence, not the number)",
               v=dict(nogo="NO-GO", pivot="PIVOT", validate="VALIDATE FIRST", go="GO")),
    "tr": dict(title="Puanlama", crit="Kriter", w="Ağırlık", s="Puan (1-5)", c="Güven",
               contrib="Katkı", note="Not", total="Toplam", rng="belirsizlik aralığı",
               verdict="Karar", kills="Öldürücü kriterler", profile="Profil",
               todo="GO için hâlâ gerçek dünya kanıtı gereken kapılar",
               g2="Kapı 2 (5 kullanıcı görüşmesi)", g5="Kapı 5 (para/zaman harcayan 10 kişi)",
               ignored="Bu profilde geçersiz",
               capped="Güven düşük olduğu için 3 ile sınırlandı (sayıyı değil kanıtı yükselt)",
               v=dict(nogo="NO-GO", pivot="PIVOT", validate="ÖNCE DOĞRULA (VALIDATE FIRST)", go="GO")),
}
SPREAD = {"high": 0.0, "medium": 0.5, "low": 1.0}
LOW_CONFIDENCE_CAP = 3.0  # weak evidence cannot justify a high score
KILL_FLAGS = {"free_dominant_no_diff", "negative_unit_economics", "regulatory_blocker", "no_payer"}
PROFILE_IGNORES = {"portfolio": {"no_payer"}, "opensource": {"no_payer"}, "internal": {"no_payer"}}


def pts(s, w):
    return w * (max(1.0, min(5.0, s)) - 1) / 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--profile", default=None, choices=list(PROFILES))
    ap.add_argument("--lang", default="en", choices=list(LABELS))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    data = json.load(open(a.file, encoding="utf-8"))
    profile = a.profile or data.get("profile", "commercial")
    if profile not in PROFILES:
        sys.exit(f"Unknown profile: {profile}")
    weights, L, T = PROFILES[profile], LABELS[a.lang], TEXT[a.lang]
    scores = data.get("scores", {})

    missing = [k for k, w in weights.items() if w > 0 and k not in scores]
    if missing:
        sys.exit(f"Missing criteria for profile '{profile}': {missing}")

    total = lo = hi = 0.0
    rows, errors, capped = [], [], []
    for k, w in weights.items():
        if w == 0:
            continue
        item = scores[k]
        try:
            s = float(item["score"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{k}: missing/invalid score")
            continue
        if not 1 <= s <= 5:
            errors.append(f"{k}: score must be 1-5")
            continue
        conf = str(item.get("confidence", "low")).lower()
        if conf not in SPREAD:
            conf = "low"
        sp = SPREAD[conf]
        if conf == "low" and s > LOW_CONFIDENCE_CAP:
            capped.append((L[k], s))
            s = LOW_CONFIDENCE_CAP
        p = pts(s, w)
        total, lo, hi = total + p, lo + pts(s - sp, w), hi + pts(s + sp, w)
        rows.append((L[k], w, s, conf, round(p, 1), item.get("note", "")))
    if errors:
        sys.exit("Errors: " + "; ".join(errors))

    ignored = PROFILE_IGNORES.get(profile, set())
    kills, skipped, unknown = [], [], []
    for f in data.get("kill_flags", []):
        flag = f.get("flag")
        if flag not in KILL_FLAGS:
            unknown.append(flag)
        elif flag in ignored:
            skipped.append(flag)
        else:
            kills.append(f)

    g2 = bool(data.get("gate2_confirmed_by_users"))
    g5 = bool(data.get("gate5_confirmed_by_users"))
    if kills or total < 40:
        v = T["v"]["nogo"]
    elif total < 60:
        v = T["v"]["pivot"]
    elif total >= 75 and g2 and g5:
        v = T["v"]["go"]
    else:
        v = T["v"]["validate"]

    result = dict(idea=data.get("idea", ""), profile=profile, score=round(total, 1),
                  range=[round(lo, 1), round(hi, 1)], verdict=v, kill_flags=kills,
                  gate2_confirmed=g2, gate5_confirmed=g5,
                  capped=[dict(criterion=c, original=o, used=LOW_CONFIDENCE_CAP) for c, o in capped])
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"## {T['title']} — {result['idea']}\n")
    print(f"*{T['profile']}: {profile}*\n")
    print(f"| {T['crit']} | {T['w']} | {T['s']} | {T['c']} | {T['contrib']} | {T['note']} |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        note = str(r[5]).replace("|", "/")
        print(f"| {r[0]} | {r[1]} | {r[2]:g} | {r[3]} | {r[4]} | {note} |")
    print(f"\n**{T['total']}: {result['score']}/100** ({T['rng']} {result['range'][0]}–{result['range'][1]})")
    print(f"**{T['verdict']}: {v}**")
    if kills:
        print(f"\n{T['kills']}:")
        for k in kills:
            print(f"- {k['flag']}: {k.get('reason', '')}")
    if capped:
        print(f"\n{T['capped']}: " + ", ".join(f"{c} ({o:g} → 3)" for c, o in capped))
    if skipped:
        print(f"\n({T['ignored']}: {', '.join(skipped)})")
    if unknown:
        print(f"\n(Unknown kill flags ignored: {unknown})", file=sys.stderr)
    if v == T["v"]["validate"]:
        todo = [n for n, ok in ((T["g2"], g2), (T["g5"], g5)) if not ok]
        if todo:
            print(f"\n{T['todo']}: " + ", ".join(todo))


if __name__ == "__main__":
    main()
