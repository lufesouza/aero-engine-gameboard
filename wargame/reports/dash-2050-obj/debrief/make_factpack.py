"""Fact pack for the Boeing management debrief (dash-2050-obj): every number the deck may use, from the GM's data.

Writes factpack.json (datasets the deck builder charts directly, by id) and factpack.md (the same, readable, for the
consultant agent). Sources: ../data/report_data.json, ../data/boeing_fin.json, ../../dash-2050-exco/data/report_data.json,
and replays of Boeing's alternatives through the game rules (as the regret table).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
os.environ["DASH_RUN"] = "dash-2050-obj"; os.environ["DASH_BOARD"] = "v3"
sys.path.insert(0, ROOT + "/dashgame")
import model as M, rules as R, briefs as B, reports as RP  # noqa

D = json.load(open(os.path.join(HERE, "..", "data", "report_data.json")))
BF = json.load(open(os.path.join(HERE, "..", "data", "boeing_fin.json")))
OLD = json.load(open(os.path.join(ROOT, "reports", "dash-2050-exco", "data", "report_data.json")))
F = D["rounds"][-1]
Y = F["years"]; YRS = Y["year"]
SQ = D["status_quo"]["years"]
r2 = lambda v, n=2: round(v, n)
ser = lambda side, key: [r2(v, 4) for v in Y[side][key]]

# ---- alternatives with widebody shares: Boeing's 787 Re-engine in each round, everyone else as played (ex post)
records = [json.load(open(f"{ROOT}/runs/dash-2050-obj/record_r{n}.json")) for n in range(1, 5)]
states = [json.load(open(f"{ROOT}/runs/dash-2050-obj/state_r{n}.json")) for n in range(0, 5)]
def replay_alt(n, orders_b):
    prev, rec = states[n - 1], records[n - 1]
    orders = {s: (orders_b if s == "boeing" else rec["orders"][s]) for s in M.SIDES}
    s1, _ = R.adjudicate(prev, rec["year"], {k: R.validate(prev, k, rec["year"], x)[0] for k, x in orders.items()})
    s4 = RP._replay(s1, n + 1, records) if n < 4 else s1
    v = M.value(s4, covert=True, series=True)
    yb = {r["year"]: r for r in v["_af_series"]["years"]}
    return {"pv_boeing": v["boeing"]["pv_delta"], "pv_airbus": v["airbus"]["pv_delta"],
            "nb_share": {y: yb[y]["boeing"]["nb_share"] for y in (2039, 2040, 2045, 2050)},
            "wb_share": {y: yb[y]["boeing"]["wb_share"] for y in (2040, 2045, 2050, 2055)},
            "re787_eis": (M.live(s4, "re787") or {}).get("eis")}
alts = []
for n in range(1, 5):
    year = records[n - 1]["year"]
    actual = dict(records[n - 1]["orders"]["boeing"])
    for re in ("hold", "launch"):
        o = dict(actual); o["re787"] = re
        try:
            res = replay_alt(n, o)
        except Exception as e:  # noqa
            res = {"error": str(e)}
        alts.append({"round": n, "year": year, "re787": re, **res})
# Airbus's response risk: from Boeing's own grids (both re-engine)
G1 = json.load(open(f"{ROOT}/runs/dash-2050-obj/grids_r1.json"))["boeing"]


def replay_mod(mods):
    """Replay the whole game from the start with some orders changed: mods = {round: {side: {field: value}}}."""
    s = states[0]
    for n in range(1, 5):
        rec = records[n - 1]
        orders = {}
        for side in M.SIDES:
            o = dict(rec["orders"][side])
            o.update(mods.get(n, {}).get(side, {}))
            orders[side], _ = R.validate(s, side, rec["year"], o)
        s, _ = R.adjudicate(s, rec["year"], orders)
    v = M.value(s, covert=True, series=True)
    yb = {r["year"]: r for r in v["_af_series"]["years"]}
    return {"pv_boeing": v["boeing"]["pv_delta"], "pv_airbus": v["airbus"]["pv_delta"],
            "nb_share": {y: yb[y]["boeing"]["nb_share"] for y in (2039, 2040, 2041, 2044, 2045, 2050)},
            "wb_share": {y: yb[y]["boeing"]["wb_share"] for y in (2035, 2040, 2045, 2050, 2055)},
            "re787_eis": (M.live(s, "re787") or {}).get("eis"), "rea350_eis": (M.live(s, "rea350") or {}).get("eis"),
            "dt": s["dt"]}


RE = {1: {"boeing": {"re787": "launch"}}}
answer = {"as_played": replay_mod({}), "re787_2030": replay_mod(RE)}
for n, yr in ((1, 2030), (2, 2035), (3, 2045), (4, 2050)):
    a_only = replay_mod({n: {"airbus": {"rea350": "launch"}}})
    both = replay_mod({**RE, n: {**RE.get(n, {}), "airbus": {"rea350": "launch"}}} if n != 1 else {1: {"boeing": {"re787": "launch"}, "airbus": {"rea350": "launch"}}})
    gain = answer["re787_2030"]["pv_boeing"] - answer["as_played"]["pv_boeing"]
    cost = a_only["pv_boeing"] - both["pv_boeing"]
    answer[f"airbus_answers_{yr}"] = {"airbus_a350_reengine_only": a_only, "boeing_787_2030_and_airbus_a350": both,
                                     "boeing_gain_if_no_answer": gain, "boeing_cost_if_answer": cost,
                                     "break_even_answer_probability": gain / (gain + cost),
                                     "airbus_cost_of_answering": answer["re787_2030"]["pv_airbus"] - both["pv_airbus"]}
answer["delay_tactics_2030"] = replay_mod({1: {"airbus": {"delay_tactics": "bottleneck"}}})
answer["delay_tactics_2030_with_787"] = replay_mod({1: {"airbus": {"delay_tactics": "bottleneck"}, "boeing": {"re787": "launch"}}})

played = BF["alts"]
plans = []
for a in played:
    plans.append({"plan": a["plan"], "pv": r2(a["pv"]), "fps_in_service": a["fps_eis"],
                  "nb_share_2040": a["nb_share"]["2040"] if "2040" in a["nb_share"] else a["nb_share"][2040],
                  "nb_share_2050": a["nb_share"]["2050"] if "2050" in a["nb_share"] else a["nb_share"][2050],
                  "peak_programme_cash": [r2(a["peak_spend"][0]), a["peak_spend"][1]], "programme_cash_total": r2(a["total_spend"]),
                  "lowest_stress_fcf": [r2(a["min_stress_fcf"][0]), a["min_stress_fcf"][1]],
                  "stress_line_met": a["stress_held"], "stress_net_debt_2035": r2(a["stress_2035"]),
                  "owners_cash_2027_2050": r2(a["owners_2027_50"], 1), "owners_cash_2027_2060": r2(a["owners_2027_60"], 1),
                  "objectives_met": sum(1 for _, ok in a["objectives"] if ok), "objectives": a["objectives"]})

import itertools
cum = lambda xs: [r2(v, 1) for v in itertools.accumulate(xs)]
A = {a["plan"]: a for a in played}
PL, DN = A["fps 10-yr + 787: hold"], A["fps: hold + 787: hold"]
cy = [r["year"] for r in PL["rows"]]
op, oh, on = cum(PL["owners"]), cum(DN["owners"]), cum(BF["cash"]["owners_noprog"])
payback = next(y for y, a, h in zip(cy, op, oh) if y > 2030 and a >= h)

datasets = {
    "nb_share": {"title": "Narrowbody delivery share by year", "unit": "share", "years": YRS,
                 "series": {"Boeing": ser("boeing", "nb_share"), "Airbus": ser("airbus", "nb_share")}},
    "wb_share": {"title": "Widebody delivery share by year", "unit": "share", "years": YRS,
                 "series": {"Boeing": ser("boeing", "wb_share"), "Airbus": ser("airbus", "wb_share")}},
    "nb_engine_share": {"title": "Narrowbody engine share by year", "unit": "share", "years": YRS,
                        "series": {"CFM/GE": ser("cfm", "nb_share"), "P&W (Joint Venture)": ser("pratt_whitney", "nb_share"),
                                   "Rolls-Royce (Joint Venture)": ser("rolls_royce", "nb_share")}},
    "boeing_profit": {"title": "Boeing operating profit vs status quo, $B a year at 2026 prices (the dashboard)", "unit": "$B", "years": YRS,
                      "series": {"Game": ser("boeing", "profit"), "Status quo": [r2(v, 4) for v in Y["boeing"]["sq_profit"]]}},
    "airbus_profit": {"title": "Airbus operating profit vs status quo, $B a year (the dashboard)", "unit": "$B", "years": YRS,
                      "series": {"Game": ser("airbus", "profit"), "Status quo": [r2(v, 4) for v in Y["airbus"]["sq_profit"]]}},
    "boeing_cash": {"title": "Boeing fps programme cash and free cash flow, $B a year, 2026 dollars (the GM's tracker)", "unit": "$B",
                    "years": [r["year"] for r in BF["cash"]["base"]],
                    "series": {"fps programme cash": [r2(r["spend"], 4) for r in BF["cash"]["base"]],
                               "Free cash flow, base": [r2(r["fcf"], 4) for r in BF["cash"]["base"]],
                               "Free cash flow, stress": [r2(r["fcf"], 4) for r in BF["cash"]["stress"]]}},
    "net_debt": {"title": "Boeing net debt at year end, $B, 2026 dollars", "unit": "$B", "years": [2026] + [r["year"] for r in BF["cash"]["base"]],
                 "series": {"Base case": [22.53] + [r2(r["debt"], 4) for r in BF["cash"]["base"]],
                            "Stress case": [22.53] + [r2(r["debt"], 4) for r in BF["cash"]["stress"]],
                            "No new programme": [22.53] + [r2(r["debt_no_programme"], 4) for r in BF["cash"]["base"]]}},
    "owners_cash": {"title": "Cumulative cash to Boeing's owners from 2027, $B, 2026 dollars, undiscounted", "unit": "$B", "years": cy,
                    "series": {"fps 10-year (played)": op, "Do Nothing (no fps)": oh, "No game (analysts' path)": on}},
    "pv_bridge": {"title": "Boeing ΔPV bridge, $B at 2026", "unit": "$B",
                  "items": [["Narrowbody profit vs status quo", r2(F["value"]["boeing"]["bridge"]["nb_profit_vs_sq"])],
                            ["fps bill ($60.32B charged in 2040)", r2(F["value"]["boeing"]["bridge"]["programme_investment"])],
                            ["Debt penalty", r2(F["value"]["boeing"]["bridge"]["debt_penalty"])],
                            ["ΔPV", r2(F["value"]["boeing"]["pv_delta"])]]},
    "dpv_all": {"title": "Final ΔPV by company, $B at 2026 (this game and the previous one)", "unit": "$B",
                "rows": [[s, r2(F["value"][s]["pv_delta"]), r2(OLD["rounds"][-1]["value"][s]["pv_delta"])] for s in M.SIDES]},
    "boeing_objectives": {"title": "Boeing's objectives, final state", "rows": [[o["label"], o["met"], o["detail"]] for o in F["objectives"]["boeing"]]},
    "plans_2030": {"title": "Boeing's 2030 plans, replayed with everyone else as played", "rows": plans},
    "re787_by_round": {"title": "787 Re-engine in each round, replayed (Boeing's other orders and everyone else as played)", "rows": alts},
    "airbus_answer": {"title": "Boeing's 787 Re-engine in 2030 against an Airbus A350 Re-engine in each round, and Airbus Delay Tactics "
                               "(bottleneck) in 2030: whole-game replays, everyone else as played", "cases": answer},
    "boeing_grid_2030": {"title": "Boeing's 2030 payoff grid as its brief showed it: ΔPV $B by plan against what Airbus might do (nobody moves later)",
                         "scenarios": G1["scenarios"], "rows": [[r["plan"]] + [r2(c[0]) for c in r["cells"]] for r in G1["rows"]]},
}
facts = {
    "payback_year_vs_do_nothing": payback,
    "owners_cash_2027_2050": {"played": op[cy.index(2050)], "do_nothing": oh[cy.index(2050)], "no_game": on[cy.index(2050)]},
    "owners_cash_2027_2060": {"played": op[-1], "do_nothing": oh[-1], "no_game": on[-1]},
    "boeing_value": {k: r2(v) for k, v in F["value"]["boeing"]["bridge"].items()} | {"pv_delta": r2(F["value"]["boeing"]["pv_delta"]), "yield": r2(F["value"]["boeing"]["yield"])},
    "airbus_value": r2(F["value"]["airbus"]["pv_delta"]),
    "regret_boeing": {n: {"best": D["regret"][n]["boeing"]["best_ex_post"]["plan"], "regret": r2(D["regret"][n]["boeing"]["regret_ex_post"])} for n in D["regret"]},
    "regret_airbus": {n: {"best": D["regret"][n]["airbus"]["best_ex_post"]["plan"], "regret": r2(D["regret"][n]["airbus"]["regret_ex_post"])} for n in D["regret"]},
    "stage_equilibria": {n: {"pure": [[p[0], p[1], r2(p[2]), r2(p[3])] for p in D["stage"][n]["pure"]],
                             "played": D["stage"][n]["played"], "played_value": [r2(x) for x in D["stage"][n]["played_value"]]} for n in D["stage"]},
    "orders": {r["year"]: {s: r["orders"][s] for s in ("boeing", "airbus")} for r in D["rounds"]},
    "timeline": F["timeline"]["programmes"],
    "control2_sources_fps": F["control2"]["sources"]["boeing"]["2050"],
    "tracker_inputs": {k: BF["inputs"][k] for k in ("start_debt_b", "historical_level_b", "target_year", "hold_years", "base_fcf_b",
                                                     "base_fcf_after_b", "tax_rate", "real_rate", "cpi", "stress_fcf_scale")},
}
out = {"datasets": datasets, "facts": facts}
json.dump(out, open(os.path.join(HERE, "factpack.json"), "w"), indent=1, default=str)

# readable version for the consultant
L = ["# Fact pack: Boeing management debrief, dash-2050-obj", "",
     "Every number in the deck must come from here (or from a source file named in the agent definition). Datasets are "
     "charted by the deck builder directly from this file, by their id.", ""]
def pct(v): return f"{v * 100:.1f}%"
def yrs_line(ds, key, fmt, pick=(2026, 2030, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2045, 2049, 2050, 2055, 2060)):
    ys = ds["years"]; vals = ds["series"][key]
    return ", ".join(f"{y}: {fmt(vals[ys.index(y)])}" for y in pick if y in ys)
for did, ds in datasets.items():
    L += [f"## Dataset `{did}`: {ds['title']}", ""]
    if "series" in ds:
        fmt = pct if ds["unit"] == "share" else (lambda v: f"{v:.2f}")
        for k in ds["series"]:
            L.append(f"- {k}: " + yrs_line(ds, k, fmt))
    elif "items" in ds:
        L += [f"- {a}: {b:+.2f}" for a, b in ds["items"]]
    elif did == "dpv_all":
        L += [f"- {a}: this game {b:+.2f}, previous game {c:+.2f}" for a, b, c in ds["rows"]]
    elif did == "boeing_objectives":
        L += [f"- {'MET' if m else 'NOT MET'}: {lab} ({det})" for lab, m, det in ds["rows"]]
    elif did == "plans_2030":
        for p in sorted(ds["rows"], key=lambda x: -x["pv"]):
            L.append(f"- {p['plan']}: ΔPV {p['pv']:+.2f}; fps in service {p['fps_in_service']}; NB share 2040 {pct(p['nb_share_2040'])}, "
                     f"2050 {pct(p['nb_share_2050'])}; peak programme cash ${p['peak_programme_cash'][0]}B ({p['peak_programme_cash'][1]}); "
                     f"lowest stress FCF ${p['lowest_stress_fcf'][0]}B ({p['lowest_stress_fcf'][1]}); stress debt line "
                     f"{'met' if p['stress_line_met'] else 'NOT met'} (stress net debt end-2035 ${p['stress_net_debt_2035']}B); cash to owners "
                     f"2027-2050 ${p['owners_cash_2027_2050']}B, 2027-2060 ${p['owners_cash_2027_2060']}B; objectives met {p['objectives_met']} of 7: "
                     + "; ".join(f"{'Y' if ok else 'N'} {lab.split(':')[0]}" for lab, ok in p["objectives"]))
    elif did == "re787_by_round":
        for a in ds["rows"]:
            if "error" in a:
                L.append(f"- {a['year']} 787 {a['re787']}: {a['error']}"); continue
            L.append(f"- {a['year']}, 787 Re-engine {a['re787']}: Boeing ΔPV {a['pv_boeing']:+.2f}, Airbus {a['pv_airbus']:+.2f}; 787 Re-engine in service "
                     f"{a['re787_eis']}; Boeing WB share 2040 {pct(a['wb_share'][2040])}, 2045 {pct(a['wb_share'][2045])}, 2050 {pct(a['wb_share'][2050])}; "
                     f"NB share 2050 {pct(a['nb_share'][2050])}")
    elif did == "airbus_answer":
        c = ds["cases"]
        f = lambda x: (f"Boeing ΔPV {x['pv_boeing']:+.2f}, Airbus {x['pv_airbus']:+.2f}; Boeing NB share 2040 {pct(x['nb_share'][2040])}, "
                       f"2044 {pct(x['nb_share'][2044])}, 2050 {pct(x['nb_share'][2050])}; Boeing WB share 2040 {pct(x['wb_share'][2040])}, "
                       f"2045 {pct(x['wb_share'][2045])}, 2050 {pct(x['wb_share'][2050])}, 2055 {pct(x['wb_share'][2055])}; "
                       f"787 Re-engine in service {x['re787_eis']}, A350 Re-engine in service {x['rea350_eis']}")
        L.append(f"- As played: " + f(c["as_played"]))
        L.append(f"- 787 Re-engine in 2030, Airbus never answers: " + f(c["re787_2030"]))
        for yr in (2030, 2035, 2045, 2050):
            x = c[f"airbus_answers_{yr}"]
            L.append(f"- Airbus launches an A350 Re-engine in {yr}, Boeing holds the 787: " + f(x["airbus_a350_reengine_only"]))
            L.append(f"- Airbus launches an A350 Re-engine in {yr}, Boeing launched the 787 Re-engine in 2030: " + f(x["boeing_787_2030_and_airbus_a350"]))
            L.append(f"  - Boeing's gain from the 787 Re-engine if Airbus never answers {x['boeing_gain_if_no_answer']:+.2f}; its cost if Airbus answers in {yr} "
                     f"{x['boeing_cost_if_answer']:.2f}; break-even chance of that answer {x['break_even_answer_probability'] * 100:.0f}%; "
                     f"Airbus's own cost of answering in {yr} {x['airbus_cost_of_answering']:.2f}")
        L.append("- Airbus Delay Tactics (bottleneck) in 2030, Boeing as played: " + f(c["delay_tactics_2030"]))
        L.append("- Airbus Delay Tactics (bottleneck) in 2030, Boeing with the 787 Re-engine: " + f(c["delay_tactics_2030_with_787"]))
    elif did == "boeing_grid_2030":
        L.append("| Plan | " + " | ".join(f"S{i + 1} {sc}" for i, sc in enumerate(ds["scenarios"])) + " |")
        L.append("|---|" + "---:|" * len(ds["scenarios"]))
        L += ["| " + r[0] + " | " + " | ".join(f"{v:+.2f}" for v in r[1:]) + " |" for r in ds["rows"]]
    L.append("")
L += ["## Other facts", "", "```json", json.dumps(facts, indent=1, default=str), "```"]
open(os.path.join(HERE, "factpack.md"), "w").write("\n".join(L))
print("payback", payback)
for a in alts: print(a.get("year"), a.get("re787"), {k: (round(v, 3) if isinstance(v, float) else v) for k, v in a.items() if k not in ("round", "year", "re787")})
