"""Checks and sensitivities for the conservative-case game page (run dash-2050-cons), written to data/cons_checks.json.

1. The fps decision in 2030: Boeing's ΔPV for Do Nothing, fps 10-year (new sites and Renton), fps 7-year and the 787
   Re-engine, everyone else's round-1 orders as played, with this run's market rules and on the dashboard alone.
2. Round by round: the value against Do Nothing of Boeing's fps 10-year (new sites, Renton) and 787 Re-engine, and of
   Airbus's A350 Re-engine, in the column that was played, as briefed (the players' grids) and as valued now; every
   player's best alternative now; and the final state valued with the supply-and-demand layer off.
3. The user's assumptions, one at a time: the 2030 fps business case (10-year fps at Renton and at new sites, minus
   Do Nothing, round-1 orders as played) and the final state's ΔPV for Boeing and Airbus when one assumption moves:
   Boeing's share loss a year after NGSA EIS, the slack floor, Airbus's capacity response, the firm-order netting.
4. The same values stepping from the previous game's market (dash-2050-sd: no options) to this game's, one assumption
   added at a time.
5. Boeing's deliveries by year with Do Nothing and with a 10-year fps at Renton from 2030, in both markets.
6. CFM's loss from Airbus's capacity response, split between its yardstick (the status quo) and the game.

  DASH_RUN=dash-2050-cons python3 make_cons_checks.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
os.environ.setdefault("DASH_RUN", "dash-2050-cons")
import model as M  # noqa: E402
import reports as RP  # noqa: E402
import rules as R  # noqa: E402
import supply_demand as SD  # noqa: E402

BASE_OPTIONS = dict(SD.options())
assert BASE_OPTIONS.get("demand_curve"), "run without its sd_options.json"


def set_options(**kw):
    """Value under this run's options with some changed (None removes one)."""
    o = dict(BASE_OPTIONS)
    for k, v in kw.items():
        if v is None:
            o.pop(k, None)
        else:
            o[k] = v
    SD.options = lambda: o
    SD._curve.cache_clear()
    SD._annual.cache_clear()


def reset_options():
    set_options()


def build_2030(bo, site="new_site"):
    s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
    o = dict(rec["orders"]["boeing"])
    o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None})
    o.update(bo)
    o["fps_site"] = site
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
    return R.adjudicate(s0, 2030, orders)[0]


PLAYS = [("Do Nothing", {}, "new_site"),
         ("fps 10-year, new sites", {"fps": "launch_10yr", "fps_engine_code": 7}, "new_site"),
         ("fps 10-year, Renton", {"fps": "launch_10yr", "fps_engine_code": 7}, "renton"),
         ("fps 7-year, new sites", {"fps": "launch_7yr", "fps_engine_code": 7}, "new_site"),
         ("787 Re-engine", {"re787": "launch"}, "new_site")]


def fps_2030():
    out = {}
    for sd in (False, True):
        M.SD_ON = sd
        rows = []
        for lab, bo, site in PLAYS:
            v = M.value(build_2030(bo, site), covert=True, series=True)
            rows.append({"plan": lab, "boeing": v["boeing"]["pv_delta"], "airbus": v["airbus"]["pv_delta"], "bridge": v["boeing"]["bridge"]})
        out["with_sd" if sd else "board"] = rows
    M.SD_ON = True
    return out


def round_items(n_last):
    D = RP.jl("report_data.json")
    out = []
    for n in range(1, n_last + 1):
        g = RP.jl("grids_r%d.json" % n)
        bo, ab = g["boeing"], g["airbus"]
        rec = RP.jl("record_r%d.json" % n)
        col_b = bo["scenarios"].index("Airbus launches NGSA on the A320 Alt plan") if n == 1 else bo["scenarios"].index("Rivals hold")
        col_a = ab["scenarios"].index("Rivals hold")
        brief_b = {r["plan"]: r["cells"][col_b][0] for r in bo["rows"]}
        brief_a = {r["plan"]: r["cells"][col_a][0] for r in ab["rows"]}
        now_b = {a["plan"]: a["myopic"] for a in D["regret"][str(n)]["boeing"]["alternatives"]}
        now_a = {a["plan"]: a["myopic"] for a in D["regret"][str(n)]["airbus"]["alternatives"]}
        row = {"round": n, "year": rec["year"]}
        for tag, vb, va in (("briefed", brief_b, brief_a), ("now", now_b, now_a)):
            hb = vb["fps: hold + 787: hold"]
            played_a = next(p for p in va if "A350: hold" in p and ("Alt" in p) and ("cancel" not in p))
            rea_a = played_a.replace("A350: hold", "A350 Re-engine")
            ha = va[played_a]
            g_ = lambda k: (vb[k] - hb) if k in vb else None
            row[tag] = {"boeing_do_nothing": hb, "fps_10yr_new_site": g_("fps 10-yr + 787: hold"),
                        "fps_10yr_renton": g_("fps 10-yr at Renton + 787: hold"), "fps_7yr_new_site": g_("fps 7-yr + 787: hold"),
                        "re787": g_("fps: hold + 787 Re-engine"), "airbus_played_plan": played_a, "airbus_played": ha,
                        "rea350": (va[rea_a] - ha) if rea_a in va else None,
                        "boeing_best": max(vb, key=vb.get), "boeing_best_gain": max(vb.values()) - hb,
                        "airbus_best": max(va, key=va.get), "airbus_best_gain": max(va.values()) - ha}
        out.append(row)
    return out


def decisions_now(n_last):
    D = RP.jl("report_data.json")
    return [{"round": n, "side": side, "actual": D["regret"][str(n)][side]["actual_myopic"],
             "best_plan": D["regret"][str(n)][side]["best_myopic"]["plan"], "best": D["regret"][str(n)][side]["best_myopic"]["myopic"],
             "gain": D["regret"][str(n)][side]["regret_myopic"]} for n in range(1, n_last + 1) for side in M.SIDES]


def no_layer(n_last):
    s = RP.jl("state_r%d.json" % n_last)
    M.SD_ON = False
    try:
        v = M.value(s, covert=True, series=True)
        return {side: v[side]["pv_delta"] for side in M.SIDES}
    finally:
        M.SD_ON = True


VARIANTS = [("As played", {}),
            ("Boeing loses 0.5 points a year", {"boeing_pp_after_ngsa": 0.5}),
            ("Boeing loses 2 points a year", {"boeing_pp_after_ngsa": 2.0}),
            ("Boeing loses 3 points a year", {"boeing_pp_after_ngsa": 3.0}),
            ("Dashboard share rule after NGSA (Airbus +3 points a year to 80%)", {"boeing_pp_after_ngsa": None}),
            ("No slack floor (flexible customers' overflow only)", {"boeing_takes_airbus_slack": None}),
            ("No Airbus capacity response", {"airbus_capacity_response": None}),
            ("Airbus capacity response 2% a year", {"airbus_capacity_response": 0.02}),
            ("Firm orders on top of demand (not part of it)", {"firm_backlog": None})]


def assumption_sensitivity(n_last):
    s_final = RP.jl("state_r%d.json" % n_last)
    dn, f_new, f_ren = build_2030({}), build_2030({"fps": "launch_10yr", "fps_engine_code": 7}), \
        build_2030({"fps": "launch_10yr", "fps_engine_code": 7}, "renton")
    out = []
    for lab, kw in VARIANTS:
        set_options(**kw)
        vb = {k: M.value(st, covert=True, series=False)["boeing"]["pv_delta"] for k, st in (("dn", dn), ("new", f_new), ("ren", f_ren))}
        vf = M.value(s_final, covert=True, series=True)
        rows = [r for r in vf["_af_series"]["years"] if r["year"] <= M.REPORT_END]
        ngsa = s_final["prog"]["ngsa"]["eis"]
        out.append({"case": lab, "options": kw, "do_nothing_2030": vb["dn"], "fps_new_site": vb["new"] - vb["dn"],
                    "fps_renton": vb["ren"] - vb["dn"], "final_boeing": vf["boeing"]["pv_delta"], "final_airbus": vf["airbus"]["pv_delta"],
                    "floor_years_from_ngsa": sum(1 for r in rows if r["year"] >= ngsa and r["boeing"]["nb_pref_share"] > r["sd"]["pref_b_base"] + 1e-6),
                    "years_from_ngsa": sum(1 for r in rows if r["year"] >= ngsa),
                    "spill_b": sum(r["boeing"]["sd"]["spill_in"] for r in rows),
                    "airbus_capacity_factor_end": rows[-1]["sd"]["airbus_capacity_factor"],
                    "pref_b_end": rows[-1]["boeing"]["nb_pref_share"],
                    "dlv_b": [r["sd"]["dlv_max"] + r["sd"]["dlv_fps"] for r in rows]})
    reset_options()
    return out


# From the previous game's market (no options: replacement + growth demand, firm orders on top, the board's share
# rule, flexible customers only) to this game's, one assumption added at a time, in this order.
STEPS = [("Previous game's market", {"demand_curve": None, "firm_backlog": None, "boeing_pp_after_ngsa": None,
                                     "boeing_takes_airbus_slack": None, "airbus_capacity_response": None}),
         ("+ conservative demand curve (firm orders on top)", {"firm_backlog": None, "boeing_pp_after_ngsa": None,
                                                               "boeing_takes_airbus_slack": None, "airbus_capacity_response": None}),
         ("+ firm orders part of demand (option B)", {"boeing_pp_after_ngsa": None, "boeing_takes_airbus_slack": None,
                                                      "airbus_capacity_response": None}),
         ("+ Boeing loses 1 point a year after NGSA", {"boeing_takes_airbus_slack": None, "airbus_capacity_response": None}),
         ("+ Airbus's slack goes to Boeing", {"airbus_capacity_response": None}),
         ("+ Airbus adds 1% capacity a year when short (this game)", {})]


def assumption_steps(n_last):
    s_final = RP.jl("state_r%d.json" % n_last)
    dn, f_new, f_ren = build_2030({}), build_2030({"fps": "launch_10yr", "fps_engine_code": 7}), \
        build_2030({"fps": "launch_10yr", "fps_engine_code": 7}, "renton")
    out = []
    for lab, kw in STEPS:
        set_options(**kw)
        vb = {k: M.value(st, covert=True, series=False)["boeing"]["pv_delta"] for k, st in (("dn", dn), ("new", f_new), ("ren", f_ren))}
        vf = M.value(s_final, covert=True, series=False)
        out.append({"step": lab, "options": kw, "do_nothing_2030": vb["dn"], "fps_new_site": vb["new"] - vb["dn"],
                    "fps_renton": vb["ren"] - vb["dn"], "final": {s: vf[s]["pv_delta"] for s in M.SIDES}})
    reset_options()
    return out


def fps_units():
    """Boeing's deliveries year by year with Do Nothing and with a 10-year fps at Renton launched in 2030 (round-1
    orders as played), in this game's market and in the previous game's, with the value bridge of each."""
    dn, fr = build_2030({}), build_2030({"fps": "launch_10yr", "fps_engine_code": 7}, "renton")
    out = {}
    for tag, kw in (("this_game", {}), ("previous_market", STEPS[0][1])):
        set_options(**kw)
        o = {}
        for k, st in (("do_nothing", dn), ("fps_renton", fr)):
            v = M.value(st, covert=True, series=True)
            rows = [r for r in v["_af_series"]["years"] if r["year"] <= M.REPORT_END]
            o[k] = {"pv": v["boeing"]["pv_delta"], "bridge": v["boeing"]["bridge"], "year": [r["year"] for r in rows],
                    "dlv_max": [r["sd"]["dlv_max"] for r in rows], "dlv_fps": [r["sd"]["dlv_fps"] for r in rows],
                    "cap_b": [r["sd"]["cap_max"] + r["sd"]["cap_fps"] for r in rows],
                    "dlv_a": [r["sd"]["dlv_a320"] + r["sd"]["dlv_ngsa"] for r in rows],
                    "pref_b": [r["boeing"]["nb_pref_share"] for r in rows]}
        o["fps_eis"] = fr["prog"]["fps"]["eis"]
        out[tag] = o
    reset_options()
    return out


def cfm_response(n_last):
    """CFM's change in ΔPV from Airbus's capacity response (final state, with and without it), split into its yardstick
    (the status quo, where Airbus's extra aircraft are A320neos) and the game: Airbus's extra output in the years Boeing
    still delivers as before, and the years Airbus's extra NGSAs displace 737 MAXs."""
    s = RP.jl("state_r%d.json" % n_last)
    R = {}
    for lab, kw in (("without", {"airbus_capacity_response": None}), ("with", {})):
        set_options(**kw)
        R[lab] = M.value(s, covert=True, series=True)
    reset_options()
    w = R["with"]["cfm"]["wacc"]
    en = {k: {x["year"]: x for x in R[k]["_en_series"]["years"]} for k in R}
    af = {k: {x["year"]: x for x in R[k]["_af_series"]["years"]} for k in R}
    bd = lambda k, y: af[k][y]["sd"]["dlv_max"] + af[k][y]["sd"]["dlv_fps"]
    displaced = [y for y in sorted(af["with"]) if y <= M.REPORT_END and bd("with", y) < bd("without", y) - 0.5]
    early = late = 0.0
    for y in sorted(en["with"]):
        if not en["with"][y]["nb_in_window"]:
            continue
        d = (en["with"][y]["cfm"]["nb_value"] - en["without"][y]["cfm"]["nb_value"]) / (1 + w) ** (y - M.Y0)
        if y in displaced:
            late += d
        else:
            early += d
    y = 2050
    sd = af["with"][y]["sd"]
    mx, ng = sd["dlv_max"] + sd["dlv_fps"], sd["dlv_a320"] + sd["dlv_ngsa"]
    ngsa_cfm = (en["with"][y]["cfm"]["nb_share"] * (mx + ng) - mx) / ng     # CFM's share of NGSA engines (MAX is all CFM)
    out = {"delta": R["with"]["cfm"]["pv_delta"] - R["without"]["cfm"]["pv_delta"],
           "yardstick": R["with"]["cfm"]["pv_sq"] - R["without"]["cfm"]["pv_sq"],
           "game": R["with"]["cfm"]["pv_new"] - R["without"]["cfm"]["pv_new"], "game_before_displacement": early,
           "game_displacement": late, "displaced_years": displaced, "cfm_share_of_ngsa_engines_2050": ngsa_cfm}
    assert abs(out["delta"] - (out["game"] - out["yardstick"])) < 1e-6 and abs(out["game"] - early - late) < 1e-6
    return out


def main():
    n = RP.rounds_played()
    out = {"rounds_played": n, "options": BASE_OPTIONS, "fps_2030": fps_2030(), "round_items": round_items(n),
           "decisions_now": decisions_now(n), "no_layer": no_layer(n), "assumptions": assumption_sensitivity(n),
           "steps": assumption_steps(n), "fps_units": fps_units(), "cfm_response": cfm_response(n)}
    path = os.path.join(HERE, "data", "cons_checks.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    for k in ("board", "with_sd"):
        print(k, [(r["plan"], round(r["boeing"], 2)) for r in out["fps_2030"][k]])
    for r in out["round_items"]:
        for tag in ("briefed", "now"):
            print(r["year"], tag, {k: (round(x, 2) if isinstance(x, float) else x) for k, x in r[tag].items()})
    print("no layer", {k: round(x, 2) for k, x in out["no_layer"].items()})
    for r in out["assumptions"]:
        print("%-52s DN %6.2f  fps new %6.2f  Renton %6.2f | final B %6.2f A %6.2f" % (
            r["case"], r["do_nothing_2030"], r["fps_new_site"], r["fps_renton"], r["final_boeing"], r["final_airbus"]))
    for r in out["steps"]:
        print("%-58s DN %6.2f  fps new %6.2f  Renton %6.2f | final %s" % (
            r["step"], r["do_nothing_2030"], r["fps_new_site"], r["fps_renton"], {k: round(x, 2) for k, x in r["final"].items()}))
    print("wrote", path)


if __name__ == "__main__":
    main()
