"""Facts for the dash-2050-emb report (Embraer as a sixth player, with political terms, in the MAX phase-out game),
from the run's report data (dashgame/reports.py) and round records, and the same for the previous game
(dash-2050-phaseout) for the comparison. Writes data/emb.json; the page builder reads only that file and record/.

  python3 extract_emb.py [run] [prev_run]      (defaults dash-2050-emb, dash-2050-phaseout)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "..", "runs")
RUN = sys.argv[1] if len(sys.argv) > 1 else "dash-2050-emb"
PREV = sys.argv[2] if len(sys.argv) > 2 else "dash-2050-phaseout"
YEARS = list(range(2026, 2061))
KEY_YEARS = [2030, 2035, 2040, 2045, 2050, 2055, 2060]


def jl(run, name):
    with open(os.path.join(RUNS, run, name)) as f:
        return json.load(f)


def market(r):
    """Narrowbody deliveries by maker and type, delivered shares, widebody shares, year by year (final state)."""
    sd, y = r["sd"], r["years"]
    out = []
    for i, yr in enumerate(sd["year"]):
        if yr > 2060:
            break
        e = sd.get("dlv_embraer", [0.0] * len(sd["year"]))[i]
        c = sd["dlv_comac"][i]
        b, a = sd["dlv_max"][i] + sd["dlv_fps"][i], sd["dlv_a320"][i] + sd["dlv_ngsa"][i]
        tot = b + a + c + e
        out.append({"year": yr, "demand": sd["demand_gross"][i], "max": sd["dlv_max"][i], "fps": sd["dlv_fps"][i],
                    "a320": sd["dlv_a320"][i], "ngsa": sd["dlv_ngsa"][i], "comac": c, "embraer": e,
                    "entrant": sd["dlv_entrant"][i] - e, "lost": sd["lost"][i],
                    "sh_boeing": b / tot if tot else 0.0, "sh_airbus": a / tot if tot else 0.0,
                    "sh_comac": c / tot if tot else 0.0, "sh_embraer": e / tot if tot else 0.0,
                    "pref_boeing": sd["boeing"]["pref_share"][i],
                    "wb_boeing": y["boeing"]["wb_share"][i], "wb_airbus": y["airbus"]["wb_share"][i],
                    "cut_boeing": sd.get("price_cut", {}).get("boeing", [0.0] * len(sd["year"]))[i],
                    "cut_airbus": sd.get("price_cut", {}).get("airbus", [0.0] * len(sd["year"]))[i],
                    "sq_boeing": sd["sq_delivered_b"][i], "sq_airbus": sd["sq_delivered_a"][i]})
    return out


def boeing_fin(r):
    """Boeing's P&L (2026 $, the GM valuation) and cash and net debt (the GM's balance-sheet tracker), by year."""
    b = r["years"]["boeing"]
    debt = {x["year"]: x for x in r["control2"]["debt_base"]}
    stress = {x["year"]: x for x in r["control2"]["debt_stress"]}
    out = []
    for i, yr in enumerate(r["years"]["year"]):
        d = debt.get(yr, {})
        out.append({"year": yr, "nb_units": b["nb_units"][i], "wb_units": b["wb_units"][i], "nb_revenue": b["nb_revenue"][i],
                    "wb_revenue": b["wb_revenue"][i], "revenue": b["revenue"][i], "profit": b["profit"][i],
                    "sq_profit": b["sq_profit"][i], "nonrecurring": b["nonrecurring"][i],
                    "nb_share": b["nb_share"][i], "wb_share": b["wb_share"][i],
                    "base_fcf": d.get("base_fcf"), "profit_vs_baseline": d.get("profit_vs_baseline"), "spend": d.get("spend"),
                    "interest": d.get("interest"), "fcf": d.get("fcf"), "debt": d.get("debt"),
                    "debt_no_programme": d.get("debt_no_programme"), "debt_stress": stress.get(yr, {}).get("debt"),
                    "spend_items": d.get("items")})
    return out


def run_facts(run):
    D = jl(run, "report_data.json")
    R = D["rounds"]
    last = R[-1]
    sides = list(last["value"])
    out = {"run": run, "sides": sides,
           "rounds": [{"round": r["round"], "year": r["year"], "orders": r["orders"], "log": [x for x in r["log"] if "[covert]" not in x],
                       "value": {s: r["value"][s]["pv_delta"] for s in sides},
                       "yield": {s: r["value"][s]["yield"] for s in sides},
                       "bridge": {s: r["value"][s]["bridge"] for s in sides},
                       "public_statements": r["public_statements"],
                       "objectives": r["objectives"]} for r in R],
           "market": market(last), "boeing_fin": boeing_fin(last),
           "debt_inputs": last["control2"]["debt_inputs"],
           "timeline": last["timeline"]["programmes"],
           "engine_fit": last["timeline"]["engine_fit"],
           "status_quo": {"boeing_profit": D["status_quo"]["years"]["boeing"]["profit"],
                          "boeing_revenue": D["status_quo"]["years"]["boeing"]["revenue"],
                          "airbus_profit": D["status_quo"]["years"]["airbus"]["profit"]},
           "regret": {n: {s: {k: x[k] for k in ("actual_myopic", "actual_ex_post", "regret_myopic", "regret_ex_post")} |
                          {"best_myopic": x["best_myopic"]["plan"], "best_ex_post": x["best_ex_post"]["plan"],
                           "alternatives": [{"plan": a["plan"], "myopic": a["myopic"], "ex_post": a["ex_post"]} for a in x["alternatives"]]}
                          for s, x in v.items()} for n, v in D["regret"].items()},
           "options": D.get("sd_inputs", {}).get("options", {})}
    if "embraer" in last["years"]:
        e = last["years"]["embraer"]
        out["embraer_years"] = [{"year": yr, **{k: e[k][i] for k in ("nb_units", "nb_share", "nb_revenue", "nb_profit", "capacity", "customer_share")}}
                                for i, yr in enumerate(last["years"]["year"])]
    out["grids"] = {}
    for r in R:
        g = jl(run, "grids_r%d.json" % r["round"])
        out["grids"][str(r["round"])] = {s: {"scenarios": g[s]["scenarios"],
                                             "rows": [{"plan": x["plan"], "cells": [c[0] for c in x["cells"]]} for x in g[s]["rows"]]}
                                         for s in ("boeing", "airbus", "embraer") if s in g}
    return out


def main():
    cur, prev = run_facts(RUN), run_facts(PREV)
    json.dump({"run": cur, "prev": prev}, open(os.path.join(HERE, "data", "emb.json"), "w"), indent=1)
    print("wrote data/emb.json:", RUN, {s: round(x, 2) for s, x in cur["rounds"][-1]["value"].items()},
          "| prev", PREV, {s: round(x, 2) for s, x in prev["rounds"][-1]["value"].items()})


if __name__ == "__main__":
    main()
