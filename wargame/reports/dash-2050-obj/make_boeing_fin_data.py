"""Boeing's financials in the dash-2050-obj game, for boeing_financials.html. Writes data/boeing_fin.json.

P&L: the GM valuation of the final state (report_data.json), the dashboard's commercial-airplane model at unescalated
2026 prices. Cash and net debt: the GM's balance-sheet tracker (finance.py), 2026 dollars. Alternatives: every Boeing
2030 plan, replayed with everyone else's actual orders in every round (as the regret table), tracker metrics on each.
"""
import copy, json, os, sys
os.environ["DASH_RUN"] = "dash-2050-obj"; os.environ["DASH_BOARD"] = "v3"
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT + "/dashgame")
import model as M, rules as R, briefs as B, finance as FIN, reports as RP  # noqa

D = json.load(open(ROOT + "/reports/dash-2050-obj/data/report_data.json"))
F = D["rounds"][-1]
b, sq = F["years"]["boeing"], D["status_quo"]["years"]["boeing"]
YRS = F["years"]["year"]
P = M.af_params()
INP = FIN.inputs()

pl = []
for i, y in enumerate(YRS):
    pl.append({k: b[k][i] for k in ("nb_share", "wb_share", "nb_units", "wb_units", "nb_price", "nb_margin", "nb_revenue",
                                     "wb_revenue", "revenue", "nb_profit", "wb_profit", "profit", "sq_profit", "nonrecurring")}
              | {"year": y, "sq_revenue": sq["revenue"][i], "sq_nb_units": sq["nb_units"][i], "vs_sq": b["profit"][i] - b["sq_profit"][i]})

C2 = F["control2"]
def owners(rows):
    """Cash to owners each year: free cash flow left once net debt is at the historical level (the tracker's rule)."""
    H, cpi = INP["historical_level_b"], INP["cpi"]
    out, prev = [], INP["start_debt_b"]
    for r in rows:
        Dr = prev / (1 + cpi)
        o = max(0.0, r["fcf"] - max(0.0, Dr - H)) if Dr - r["fcf"] < H else 0.0
        out.append(o); prev = r["debt"]
    return out
def owners_sq(rows):
    H, cpi = INP["historical_level_b"], INP["cpi"]
    out, prev = [], INP["start_debt_b"]
    for r in rows:
        Dr = prev / (1 + cpi)
        o = max(0.0, r["base_fcf"] - max(0.0, Dr - H)) if Dr - r["base_fcf"] < H else 0.0
        out.append(o); prev = r["debt_no_programme"]
    return out
cash = {"base": C2["debt_base"], "stress": C2["debt_stress"],
        "owners_base": owners(C2["debt_base"]), "owners_stress": owners(C2["debt_stress"]),
        "owners_noprog": owners_sq(C2["debt_base"]), "owners_noprog_stress": owners_sq(C2["debt_stress"])}

# alternatives: Boeing's 2030 plans, others as played, later rounds replayed (ex post), as the regret table
records = [json.load(open(f"{ROOT}/runs/dash-2050-obj/record_r{n}.json")) for n in range(1, 5)]
s0 = json.load(open(f"{ROOT}/runs/dash-2050-obj/state_r0.json"))
rec = records[0]
alts = []
for lab, o in B.own_options(s0, "boeing", 2030):
    o = dict(o)
    if o.get("fps_engine_code") is not None:
        o["fps_engine_code"] = 7
    orders = {s: (o if s == "boeing" else rec["orders"][s]) for s in M.SIDES}
    s1, _ = R.adjudicate(s0, 2030, {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()})
    trail = [s1]
    s4 = RP._replay(s1, 2, records, trail=trail)
    with FIN.history_override(trail):
        mb = FIN.debt_metrics(s4, stress=False); ms = FIN.debt_metrics(s4, stress=True)
        cash_items = FIN.programme_cash(s4)
    v = M.value(s4, covert=True, series=True)
    yb = {r["year"]: r for r in v["_af_series"]["years"]}
    spend_by = {y: sum(x.values()) for y, x in cash_items.items()}
    alts.append({"plan": lab, "orders": o, "pv": v["boeing"]["pv_delta"],
                 "nb_share": {y: yb[y]["boeing"]["nb_share"] for y in (2039, 2040, 2045, 2050)},
                 "fps_eis": (M.live(s4, "fps") or {}).get("eis"),
                 "base_first": mb["first_year"], "base_held": mb["held_ok"], "stress_first": ms["first_year"], "stress_held": ms["held_ok"],
                 "stress_peak_after": ms["peak_after_first"], "stress_2035": ms["held"][2035],
                 "min_stress_fcf": min((r["fcf"], r["year"]) for r in ms["rows"] if r["year"] >= 2030),
                 "peak_spend": max(((v_, y) for y, v_ in spend_by.items()), default=(0, None)),
                 "total_spend": sum(spend_by.values()),
                 "owners_2027_50": sum(x for r, x in zip(mb["rows"], owners(mb["rows"])) if r["year"] <= 2050),
                 "owners_2027_60": sum(owners(mb["rows"])),
                 "objectives": [(lab_, ok) for lab_, ok, _ in B.objective_status("boeing", s4, v)],
                 "bridge": v["boeing"]["bridge"],
                 "rows": [{"year": r["year"], "profit": r["profit_vs_baseline"], "spend": r["spend"], "fcf": r["fcf"], "debt": r["debt"],
                           "stress_fcf": rs["fcf"], "stress_debt": rs["debt"]} for r, rs in zip(mb["rows"], ms["rows"])],
                 "owners": owners(mb["rows"]), "owners_stress": owners(ms["rows"])})
played = next(a for a in alts if a["orders"].get("fps") == "launch_10yr" and a["orders"].get("re787") == "hold" and a["orders"].get("rate_737") == "hold")
assert abs(played["pv"] - F["value"]["boeing"]["pv_delta"]) < 1e-9, (played["pv"], F["value"]["boeing"]["pv_delta"])

pen = lambda Dd: Dd * P.get("alpha", 0.3) * (Dd / 130.0) ** 2
out = {"pl": pl, "cash": cash, "alts": alts, "value": F["value"]["boeing"], "periods": F["periods"]["boeing"],
       "inputs": INP, "params": {k: P[k] for k in P if isinstance(P[k], (int, float))},
       "objectives": F["objectives"]["boeing"], "prev_pv": json.load(open(ROOT + "/reports/dash-2050-exco/data/report_data.json"))["rounds"][-1]["value"]["boeing"]["pv_delta"]}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "boeing_fin.json"), "w"), indent=1, default=str)
print("alts", len(alts))
for a in alts:
    print(f'{a["plan"]:42s} pv {a["pv"]:7.2f} eis {a["fps_eis"]} nb40 {a["nb_share"][2040]:.2f} nb50 {a["nb_share"][2050]:.2f} base {a["base_first"]} stress {a["stress_first"]} held {a["stress_held"]} s2035 {a["stress_2035"]:.2f} peak {a["stress_peak_after"]} minFCF {a["min_stress_fcf"][0]:.2f}/{a["min_stress_fcf"][1]} spendpk {a["peak_spend"][0]:.2f}/{a["peak_spend"][1]} tot {a["total_spend"]:.2f} owners50 {a["owners_2027_50"]:.1f} owners60 {a["owners_2027_60"]:.1f}')
print('owners base 27-50', round(sum(x for r,x in zip(C2["debt_base"],cash["owners_base"]) if r["year"]<=2050),2), 'noprog', round(sum(x for r,x in zip(C2["debt_base"],cash["owners_noprog"]) if r["year"]<=2050),2))
print([ (r["year"], round(x,2)) for r,x in zip(C2["debt_base"],cash["owners_base"]) if r["year"] in (2027,2028,2029,2030,2036,2040,2050)])
print(P.get("alpha"), {k:P[k] for k in P if 'alpha' in k or 'debt' in k})
