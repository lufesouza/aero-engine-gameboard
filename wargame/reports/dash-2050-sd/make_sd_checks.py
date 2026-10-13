"""Checks and sensitivities for the supply-and-demand game page, written to data/sd_checks.json.

1. The fps decision in 2030 with and without the supply-and-demand layer: Boeing's ΔPV for hold, fps 10-year (new
   sites and Renton), fps 7-year and the 787 Re-engine, everyone else's round-1 orders as played, and the bridge lines
   that move.
2. Round by round: the value against Do Nothing of Boeing's fps 10-year (new sites, Renton) and 787 Re-engine, and of
   Airbus's Alt plan (against the base plan) and A350 Re-engine, in the column that was played (Airbus's NGSA on the
   Alt plan in 2030, rivals hold after), as briefed (the players' grids) and as valued now; every player's best
   alternative now; and the final state valued with the layer off.
3. The final state's ΔPV for Boeing and Airbus when one demand input moves: growth (x0, x0.5, x1.5), the share of
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


def fps_mechanism():
    """Why the 2030 fps loses value under supply and demand: Boeing's narrowbody profit gain from the fps (fps 10-year,
    new sites, minus Do Nothing), discounted, as the board books it and as delivered, with the fps ramp and unit profits."""
    s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
    M.SD_ON = True

    def run(bo):
        o = dict(rec["orders"]["boeing"])
        o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": "new_site"})
        o.update(bo)
        orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
        orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
        s1, _ = R.adjudicate(s0, 2030, orders)
        return {r["year"]: r for r in M.value(s1, covert=True, series=True)["_af_series"]["years"]}
    h, f = run({}), run({"fps": "launch_10yr", "fps_engine_code": 7})
    board = sd = 0.0
    years = []
    for y in sorted(f):
        a, b_ = f[y]["boeing"], h[y]["boeing"]
        if not a["nb_in_window"] or y > M.REPORT_END:
            continue
        bd, sdd = a["board_nb_profit"] - b_["board_nb_profit"], a["nb_profit"] - b_["nb_profit"]
        board += bd * f[y]["df_b"]
        sd += sdd * f[y]["df_b"]
        years.append({"year": y, "board_gain": bd, "delivered_gain": sdd, "fps_units": f[y]["sd"]["dlv_fps"],
                      "max_units": f[y]["sd"]["dlv_max"], "df": f[y]["df_b"]})
    eis = min(y["year"] for y in years if y["fps_units"] > 0)
    x = f[eis]["boeing"]
    return {"eis": eis, "board_pv_gain": board, "delivered_pv_gain": sd,
            "fps_unit_profit_m": x["nb_price"] * x["nb_margin"],
            "max_unit_profit_m": h[eis]["boeing"]["sq_nb_profit"] / h[eis]["boeing"]["sq_nb_units"] * 1000.0,
            "years": years}


def round_items(n_last):
    """Per round, the value against Do Nothing of the airframers' key options, everyone else's orders as played and no
    later moves: as briefed (the players' grids, written before the round) and as valued now (report_data regret
    alternatives, re-valued on the current inputs)."""
    D = RP.jl("report_data.json")
    out = []
    for n in range(1, n_last + 1):
        g = RP.jl("grids_r%d.json" % n)
        bo, ab = g["boeing"], g["airbus"]
        col_b = bo["scenarios"].index("Airbus launches NGSA on the A320 Alt plan") if n == 1 else bo["scenarios"].index("Rivals hold")
        col_a = ab["scenarios"].index("Rivals hold")
        brief_b = {r["plan"]: r["cells"][col_b][0] for r in bo["rows"]}
        brief_a = {r["plan"]: r["cells"][col_a][0] for r in ab["rows"]}
        now_b = {a["plan"]: a["myopic"] for a in D["regret"][str(n)]["boeing"]["alternatives"]}
        now_a = {a["plan"]: a["myopic"] for a in D["regret"][str(n)]["airbus"]["alternatives"]}
        if n == 1:
            played_a, base_a, rea_a = "NGSA (A320 Alt plan) + A350: hold", "NGSA + A350: hold", "NGSA (A320 Alt plan) + A350 Re-engine"
        else:
            played_a, base_a, rea_a = ("NGSA: hold (A320 Alt plan) + A350: hold", "NGSA: hold (A320 base plan) + A350: hold",
                                       "NGSA: hold (A320 Alt plan) + A350 Re-engine")
        row = {"round": n, "year": RP.jl("record_r%d.json" % n)["year"]}
        for tag, vb, va in (("briefed", brief_b, brief_a), ("now", now_b, now_a)):
            hb, ha = vb["fps: hold + 787: hold"], va[played_a]
            row[tag] = {"boeing_do_nothing": hb, "fps_10yr_new_site": vb["fps 10-yr + 787: hold"] - hb,
                        "fps_10yr_renton": vb["fps 10-yr at Renton + 787: hold"] - hb, "fps_7yr_new_site": vb["fps 7-yr + 787: hold"] - hb,
                        "re787": vb["fps: hold + 787 Re-engine"] - hb, "airbus_played": ha,
                        "alt_vs_base": (ha - va[base_a]) if base_a in va else None, "rea350": va[rea_a] - ha,
                        "boeing_best": max(vb, key=vb.get), "boeing_best_gain": max(vb.values()) - hb,
                        "airbus_best": max(va, key=va.get), "airbus_best_gain": max(va.values()) - ha}
        out.append(row)
    return out


def decisions_now(n_last):
    """For every round and player: the played plan's value and its best alternative, re-valued now (myopic: nobody
    moves after the round), next to the regret recorded in the stored report data of the game as briefed, if given."""
    D = RP.jl("report_data.json")
    out = []
    for n in range(1, n_last + 1):
        for side in M.SIDES:
            x = D["regret"][str(n)][side]
            out.append({"round": n, "side": side, "actual": x["actual_myopic"], "best_plan": x["best_myopic"]["plan"],
                        "best": x["best_myopic"]["myopic"], "gain": x["regret_myopic"]})
    return out


def no_layer(n_last):
    """The final state valued with the supply-and-demand layer off (the dashboard with the game master's adjustments)."""
    s = RP.jl("state_r%d.json" % n_last)
    M.SD_ON = False
    try:
        v = M.value(s, covert=True, series=True)
        return {side: v[side]["pv_delta"] for side in M.SIDES}
    finally:
        M.SD_ON = True


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
    out = {"rounds_played": n, "fps_2030": fps_2030(), "fps_mechanism": fps_mechanism(), "round_items": round_items(n), "decisions_now": decisions_now(n),
           "no_layer": no_layer(n), "demand_sensitivity": demand_sensitivity(n)}
    path = os.path.join(HERE, "data", "sd_checks.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    for k in ("board", "with_sd"):
        print(k, [(r["plan"], round(r["boeing"], 2)) for r in out["fps_2030"][k]])
    fm = out["fps_mechanism"]
    print("fps mechanism", fm["eis"], round(fm["board_pv_gain"], 2), round(fm["delivered_pv_gain"], 2), round(fm["fps_unit_profit_m"], 1),
          round(fm["max_unit_profit_m"], 1), [round(y["fps_units"]) for y in fm["years"] if y["year"] >= fm["eis"]][:9])
    for r in out["round_items"]:
        for tag in ("briefed", "now"):
            print(r["year"], tag, {k: (round(x, 2) if isinstance(x, float) else x) for k, x in r[tag].items()})
    print("no layer", {k: round(x, 2) for k, x in out["no_layer"].items()})
    for r in out["demand_sensitivity"]:
        print(r["case"], round(r["boeing"], 2), round(r["airbus"], 2), round(r["lapsed_2026_2060"]))
    print("wrote", path)


if __name__ == "__main__":
    main()
