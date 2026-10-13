"""Checks and sensitivities for the supply-and-demand game page, written to data/sd_checks.json.

1. The fps decision in 2030 with and without the supply-and-demand layer: Boeing's ΔPV for hold, fps 10-year (new
   sites and Renton), fps 7-year and the 787 Re-engine, everyone else's round-1 orders as played, and the bridge lines
   that move.
2. The final state's ΔPV for Boeing and Airbus when one demand input moves: growth (x0, x0.5, x1.5), the share of
   waiting customers who drop out each year (5%, 30%) and the flexible share (half, none).

  DASH_RUN=dash-2050-sd python3 make_sd_checks.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
os.environ.setdefault("DASH_RUN", "dash-2050-sd")
import model as M  # noqa: E402
import reports as RP  # noqa: E402
import rules as R  # noqa: E402
import supply_demand as SD  # noqa: E402


def fps_2030():
    s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
    plays = [("Do Nothing", {}, "new_site"),
             ("fps 10-year, new sites", {"fps": "launch_10yr", "fps_engine_code": 7}, "new_site"),
             ("fps 10-year, Renton", {"fps": "launch_10yr", "fps_engine_code": 7}, "renton"),
             ("fps 7-year, new sites", {"fps": "launch_7yr", "fps_engine_code": 7}, "new_site"),
             ("787 Re-engine", {"re787": "launch"}, "new_site")]
    out = {}
    for sd in (False, True):
        M.SD_ON = sd
        rows = []
        for lab, bo, site in plays:
            o = dict(rec["orders"]["boeing"])
            o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None})
            o.update(bo)
            o["fps_site"] = site
            orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
            orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
            s1, _ = R.adjudicate(s0, 2030, orders)
            v = M.value(s1, covert=True, series=True)
            rows.append({"plan": lab, "boeing": v["boeing"]["pv_delta"], "airbus": v["airbus"]["pv_delta"],
                         "bridge": v["boeing"]["bridge"]})
        out["with_sd" if sd else "board"] = rows
    M.SD_ON = True
    return out


def demand_sensitivity(n_last):
    s = RP.jl("state_r%d.json" % n_last)
    d = SD.inputs()["demand"]
    base_growth = dict(d["growth"])
    keep = {k: d[k] for k in ("lapse_per_year", "flex_share")}

    def run(label, growth_x=1.0, **kw):
        d["growth"] = {k: x * growth_x for k, x in base_growth.items()}
        d.update(keep)
        d.update(kw)
        SD._annual.cache_clear()
        v = M.value(s, covert=True, series=True)
        rows = [r for r in v["_af_series"]["years"] if r["year"] <= M.REPORT_END]
        res = {"case": label, "boeing": v["boeing"]["pv_delta"], "airbus": v["airbus"]["pv_delta"],
               "boeing_sd_line": v["boeing"]["bridge"]["supply_demand"], "airbus_sd_line": v["airbus"]["bridge"]["supply_demand"],
               "boeing_delivered_2026_2060": sum(r["sd"]["dlv_max"] + r["sd"]["dlv_fps"] for r in rows),
               "airbus_delivered_2026_2060": sum(r["sd"]["dlv_a320"] + r["sd"]["dlv_ngsa"] for r in rows),
               "lapsed_2026_2060": sum(r["sd"]["lost"] for r in rows)}
        return res
    out = [run("As played"), run("No growth (your replacement data only)", 0.0), run("Half the growth", 0.5),
           run("Growth x1.5", 1.5), run("5% of waiting customers drop out a year", lapse_per_year=0.05),
           run("30% drop out a year", lapse_per_year=0.30), run("Half the flexible customers", flex_share=keep["flex_share"] / 2),
           run("No flexible customers", flex_share=0.0)]
    d["growth"] = base_growth
    d.update(keep)
    return out


def main():
    n = RP.rounds_played()
    out = {"rounds_played": n, "fps_2030": fps_2030(), "demand_sensitivity": demand_sensitivity(n)}
    path = os.path.join(HERE, "data", "sd_checks.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    for k in ("board", "with_sd"):
        print(k, [(r["plan"], round(r["boeing"], 2)) for r in out["fps_2030"][k]])
    for r in out["demand_sensitivity"]:
        print(r["case"], round(r["boeing"], 2), round(r["airbus"], 2), round(r["lapsed_2026_2060"]))
    print("wrote", path)


if __name__ == "__main__":
    main()
