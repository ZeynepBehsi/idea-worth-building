#!/usr/bin/env python3
"""Unit economics + 12-month scenarios for a subscription-style product.

Usage: python unit_economics.py ue.json [--lang en|tr] [--json]

Input JSON (monthly figures; one market per entry, e.g. local and global):
{
  "markets": [
    {
      "name": "Local", "currency": "TRY",
      "price_monthly": 199,              # price per paying user per month (for one-off/annual, convert to monthly)
      "variable_cost_per_user": 25,      # API/inference + infra per ACTIVE PAYING user per month
      "payment_fee_pct": 3.5,            # payment processor %
      "store_fee_pct": 15,               # app store commission % (0 for web)
      "monthly_churn_pct": 8,            # % of paying users lost per month
      "cac": 300,                        # cost to acquire one paying user
      "fixed_monthly": 4000,             # hosting base, tools, subscriptions, etc.
      "scenarios": {                     # new paying users added per month
        "pessimistic": 5, "base": 15, "optimistic": 40
      }
    }
  ]
}
"""
import argparse
import math
import json
import sys

T = {
    "en": dict(title="Unit economics", net="Net revenue / user / month", contrib="Contribution / user / month",
               margin="Contribution margin", life="Expected lifetime (months)", ltv="LTV", cac="CAC",
               ratio="LTV / CAC", payback="CAC payback (months)", be="Break-even paying users",
               scen="12-month scenario", scenario="Scenario", new="New payers / month",
               users12="Paying users at month 12", mrr12="MRR at month 12", rev="12-month revenue",
               profit="12-month profit (after CAC & fixed)", beMonth="First profitable month",
               never="not reached", warn="Warnings", metric="Metric", value="Value"),
    "tr": dict(title="Birim ekonomisi", net="Kullanıcı başı aylık net gelir", contrib="Kullanıcı başı aylık katkı",
               margin="Katkı marjı", life="Beklenen ömür (ay)", ltv="LTV", cac="CAC",
               ratio="LTV / CAC", payback="CAC geri dönüş (ay)", be="Başabaş ödeyen kullanıcı",
               scen="12 aylık senaryo", scenario="Senaryo", new="Aylık yeni ödeyen",
               users12="12. ayda ödeyen kullanıcı", mrr12="12. ayda MRR", rev="12 aylık gelir",
               profit="12 aylık kâr (CAC ve sabit gider sonrası)", beMonth="İlk kârlı ay",
               never="ulaşılmadı", warn="Uyarılar", metric="Metrik", value="Değer"),
}
REQ = ["name", "currency", "price_monthly", "variable_cost_per_user", "monthly_churn_pct", "cac", "fixed_monthly"]


def analyse(m):
    price = float(m["price_monthly"])
    fees = (float(m.get("payment_fee_pct", 0)) + float(m.get("store_fee_pct", 0))) / 100
    net = price * (1 - fees)
    contrib = net - float(m["variable_cost_per_user"])
    churn = max(float(m["monthly_churn_pct"]) / 100, 1e-6)
    life = 1 / churn
    ltv = contrib * life
    cac = float(m["cac"])
    fixed = float(m["fixed_monthly"])
    r = dict(net=net, contrib=contrib, margin=(contrib / price if price else 0), life=life, ltv=ltv,
             cac=cac, ratio=(ltv / cac if cac else float("inf")),
             payback=(cac / contrib if contrib > 0 else float("inf")),
             be=(fixed / contrib if contrib > 0 else float("inf")), scen={}, warnings=[])
    for name, new in m.get("scenarios", {}).items():
        users, rev, profit, first = 0.0, 0.0, 0.0, None
        for month in range(1, 13):
            users = users * (1 - churn) + float(new)
            month_profit = users * contrib - fixed - float(new) * cac
            rev += users * price
            profit += month_profit
            if first is None and month_profit > 0:
                first = month
        r["scen"][name] = dict(new=new, users12=users, mrr12=users * price, rev=rev, profit=profit, first=first)
    if contrib <= 0:
        r["warnings"].append("negative_or_zero_contribution")
    if r["ratio"] < 3:
        r["warnings"].append("ltv_cac_below_3")
    if r["payback"] > 12:
        r["warnings"].append("cac_payback_over_12_months")
    if churn > 0.10:
        r["warnings"].append("monthly_churn_over_10pct")
    return r


def fmt(x, cur=""):
    if x == float("inf"):
        return "∞"
    return f"{x:,.0f} {cur}".strip() if abs(x) >= 100 else f"{x:,.2f} {cur}".strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--lang", default="en", choices=list(T))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.file, encoding="utf-8"))
    markets = data.get("markets", [])
    if not markets:
        sys.exit("No markets given")
    out = {}
    for m in markets:
        miss = [k for k in REQ if k not in m]
        if miss:
            sys.exit(f"{m.get('name', '?')}: missing {miss}")
        out[m["name"]] = (m, analyse(m))
    if a.json:
        print(json.dumps({k: v[1] for k, v in out.items()}, ensure_ascii=False, indent=2, default=str))
        return
    t = T[a.lang]
    for name, (m, r) in out.items():
        c = m["currency"]
        print(f"### {t['title']} — {name} ({c})\n")
        print(f"| {t['metric']} | {t['value']} |\n|---|---|")
        for key, val in [("net", fmt(r["net"], c)), ("contrib", fmt(r["contrib"], c)),
                         ("margin", f"{r['margin']*100:.0f}%"), ("life", fmt(r["life"])),
                         ("ltv", fmt(r["ltv"], c)), ("cac", fmt(r["cac"], c)),
                         ("ratio", fmt(r["ratio"])), ("payback", fmt(r["payback"])), ("be", "∞" if r["be"] == float("inf") else str(math.ceil(r["be"])))]:
            print(f"| {t[key]} | {val} |")
        if r["scen"]:
            print(f"\n**{t['scen']}**\n")
            print(f"| {t['scenario']} | {t['new']} | {t['users12']} | {t['mrr12']} | {t['rev']} | {t['profit']} | {t['beMonth']} |")
            print("|---|---|---|---|---|---|---|")
            for s, v in r["scen"].items():
                print(f"| {s} | {v['new']} | {v['users12']:.0f} | {fmt(v['mrr12'], c)} | {fmt(v['rev'], c)} | "
                      f"{fmt(v['profit'], c)} | {v['first'] or t['never']} |")
        if r["warnings"]:
            print(f"\n{t['warn']}: " + ", ".join(r["warnings"]))
        print()


if __name__ == "__main__":
    main()
