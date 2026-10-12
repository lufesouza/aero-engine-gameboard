"""Cash profiles for the Boeing debrief: free cash flow against the fps and 787 Re-engine programme cash, by year.

Two Boeing 2030 plans, each replayed with everyone else's actual orders in every round (as make_boeing_fin_data.py):
the plan as played (fps 10-year, 787 hold) and the recommended plan (fps 10-year + 787 Re-engine in 2030). For each,
the GM's balance-sheet tracker (finance.py, whole company, 2026 dollars): programme cash by item, free cash flow
before the programmes (analysts' consensus), the programmes' profit change, free cash flow after them, net debt and
cash to owners, in the base case and the stress case (consensus cash flow one-third lower). Writes cash_profiles.json.
"""
import json, os, sys
os.environ["DASH_RUN"] = "dash-2050-obj"; os.environ["DASH_BOARD"] = "v3"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT + "/dashgame")
import model as M, rules as R, briefs as B, finance as FIN, reports as RP  # noqa: E402

INP = FIN.inputs()
records = [json.load(open(f"{ROOT}/runs/dash-2050-obj/record_r{n}.json")) for n in range(1, 5)]
s0 = json.load(open(f"{ROOT}/runs/dash-2050-obj/state_r0.json"))
LABEL = {"fps (10yr)": "fps", "787 Re-engine": "787 Re-engine", "Two-front strain": "Overlap cost"}


def owners(rows):
    """Cash to owners each year: free cash flow left once net debt is at the historical level (the tracker's rule)."""
    H, cpi = INP["historical_level_b"], INP["cpi"]
    out, prev = [], INP["start_debt_b"]
    for r in rows:
        Dr = prev / (1 + cpi)
        out.append(max(0.0, r["fcf"] - max(0.0, Dr - H)) if Dr - r["fcf"] < H else 0.0)
        prev = r["debt"]
    return out


plans = {}
for lab, o in B.own_options(s0, "boeing", 2030):
    o = dict(o)
    if o.get("fps") != "launch_10yr" or o.get("rate_737") != "hold" or o.get("re787") not in ("hold", "launch"):
        continue
    o["fps_engine_code"] = 7                      # as played
    orders = {s: (o if s == "boeing" else records[0]["orders"][s]) for s in M.SIDES}
    s1, _ = R.adjudicate(s0, 2030, {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()})
    trail = [s1]
    s4 = RP._replay(s1, 2, records, trail=trail)
    with FIN.history_override(trail):
        rb = FIN.debt_metrics(s4, stress=False)["rows"]
        rs = FIN.debt_metrics(s4, stress=True)["rows"]
    v = M.value(s4, covert=True, series=False)
    key = "recommended" if o["re787"] == "launch" else "played"
    ob, os_ = owners(rb), owners(rs)
    rows = []
    for a, b, oa, ob_ in zip(rb, rs, ob, os_):
        items = {LABEL[k]: x for k, x in a["items"].items()}
        assert set(items) <= set(LABEL.values()), items
        rows.append({"year": a["year"], "items": items, "spend": a["spend"], "profit": a["profit_vs_baseline"],
                     "fcf_before": a["base_fcf"], "fcf_before_stress": b["base_fcf"],
                     "fcf": a["fcf"], "fcf_stress": b["fcf"], "debt": a["debt"], "debt_stress": b["debt"],
                     "owners": oa, "owners_stress": ob_})
    plans[key] = {"label": "fps 10-year + 787 Re-engine in 2030" if key == "recommended" else "fps 10-year, 787 hold (as played)",
                  "pv": v["boeing"]["pv_delta"], "rows": rows}

assert set(plans) == {"played", "recommended"}, plans.keys()
assert abs(plans["played"]["pv"] - 0.663208572464228) < 1e-9
for k, p in plans.items():
    tot = sum(r["spend"] for r in p["rows"])
    print(k, "pv %.4f" % p["pv"], "spend %.2f" % tot,
          "peak", max((r["spend"], r["year"]) for r in p["rows"]),
          "min fcf", min((round(r["fcf"], 2), r["year"]) for r in p["rows"] if r["year"] >= 2030),
          "min stress", min((round(r["fcf_stress"], 2), r["year"]) for r in p["rows"] if r["year"] >= 2030))
json.dump({"about": __doc__, "tax_rate": INP["tax_rate"], "stress_scale": INP["stress_fcf_scale"], "plans": plans},
          open(os.path.join(HERE, "cash_profiles.json"), "w"), indent=1)
print("wrote cash_profiles.json")
