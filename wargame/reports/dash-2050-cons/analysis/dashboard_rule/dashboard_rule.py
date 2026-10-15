"""Would the dashboard's share rule (Airbus +3 points a year after NGSA enters service, Boeing floored at 20%) change
run dash-2050-cons, in place of the user's rule (Boeing loses 1 point a year from 40% after NGSA EIS)? Everything else
as played: the conservative demand curve with the firm orders inside it, the slack floor, Airbus's 1% capacity response.

1. Every player's brief, every round: each own plan against each rival scenario, valued as briefs.payoff_grid does,
   from the state the player decided in. Under the run's own rule the values must reproduce the grids the players
   saw (checked); then the same grid under the dashboard rule. For each side and round: the played plan, the best
   plan in each column, and every plan whose value against the played plan changes sign.
2. Boeing's 2030 tests (lib.tests) for the fps (10-year at Renton and at new sites, 7-year) and the 787 Re-engine.
3. Holding everyone else's actual orders (the report's myopic regret): each side's best plan each round.
4. The final state (everyone's moves as played) valued under both rules, all five players, with Boeing's and Airbus's
   narrowbody deliveries and shares by year.
Writes dashboard_rule.json next to this file.

  python3 dashboard_rule.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M, SD, R, B, RP = L.M, L.SD, L.R, L.B, L.RP
DASH = {"boeing_pp_after_ngsa": None}          # the board's own share rule; the rest of the run's options kept
RULES = (("run", {}), ("dashboard", DASH))


def grid(state, side, year):
    """payoff_grid's ΔPV values (series off: the same pv_delta, without the yearly series)."""
    opts = B.own_options(state, side, year)
    scen = B.rival_scenarios(state, side, year)
    covert = B.sees_covert(state, side, year)
    rows = []
    for olab, o in opts:
        row = []
        for slab, so in scen:
            orders = {k: dict(v) for k, v in so.items()}
            orders[side] = dict(orders.get(side, {}), **o)
            s1, _ = R.adjudicate(state, year, orders)
            row.append(M.value(s1, covert=(covert or slab.startswith("Risk case")), series=False)[side]["pv_delta"])
        rows.append((olab, o, row))
    return rows, [s for s, _ in scen]


def played_plan(rows, actual):
    """The grid row whose orders the player actually gave (fields the grid varies)."""
    hit = [lab for lab, o, _ in rows if all(actual.get(k) == v for k, v in o.items()
                                            if not k.endswith("_engine_code"))]
    assert len(hit) == 1, (hit, actual)
    return hit[0]


def briefs(n_last):
    out = []
    for n in range(1, n_last + 1):
        prev, rec, seen = RP.jl("state_r%d.json" % (n - 1)), RP.jl("record_r%d.json" % n), RP.jl("grids_r%d.json" % n)
        year = rec["year"]
        for side in M.SIDES:
            g = {}
            for tag, kw in RULES:
                with L.patched(options=kw):
                    g[tag] = grid(prev, side, year)
            rows_run, scen = g["run"]
            # the run's rule reproduces the brief the player saw
            seen_rows = {r["plan"]: [c[0] for c in r["cells"]] for r in seen[side]["rows"]}
            assert scen == seen[side]["scenarios"], (n, side)
            assert {lab for lab, _, _ in rows_run} == set(seen_rows), (n, side)
            err = max(abs(a - b) for lab, _, row in rows_run for a, b in zip(row, seen_rows[lab]))
            assert err < 1e-6, (n, side, err)
            played = played_plan(rows_run, rec["orders"][side])
            vals = {tag: {lab: row for lab, _, row in g[tag][0]} for tag in g}
            best = {tag: [max(vals[tag], key=lambda p: vals[tag][p][j]) for j in range(len(scen))] for tag in vals}
            flips = []
            for lab in vals["run"]:
                if lab == played:
                    continue
                for j, s in enumerate(scen):
                    a = vals["run"][lab][j] - vals["run"][played][j]
                    b = vals["dashboard"][lab][j] - vals["dashboard"][played][j]
                    if (a > 1e-9) != (b > 1e-9):
                        flips.append({"plan": lab, "column": s, "run": a, "dashboard": b})
            out.append({"round": n, "year": year, "side": side, "scenarios": scen, "played": played, "reproduced_to": err,
                        "values": vals, "best": best, "flips": flips})
            print("r%d %-13s played %-45s | best changes in %d of %d columns | %d plan-column sign flips vs played" % (
                n, side, played, sum(a != b for a, b in zip(best["run"], best["dashboard"])), len(scen), len(flips)))
    return out


def boeing_tests():
    out = {}
    for tag, kw in RULES:
        with L.patched(options=kw):
            out[tag] = {}
            for plan in (L.PLAN_REN, L.PLAN_NEW, L.PLAN_7, L.PLAN_787):
                items = L.grid_items(plan)[0]
                out[tag][plan] = {"items": items, **L.tests(items), "margin": L.margin(items)}
    for plan in out["run"]:
        a, b = out["run"][plan], out["dashboard"][plan]
        print("2030 %-34s expected %+6.2f -> %+6.2f  worst %+6.2f -> %+6.2f  risk %+6.2f -> %+6.2f  passes %s -> %s" % (
            plan, a["expected"], b["expected"], a["worst"], b["worst"], a["risk_case"], b["risk_case"], a["passes"], b["passes"]))
    return out


def myopic(n_last):
    """Each side's alternatives each round, everyone else's actual orders, nobody moving after (reports.regret's myopic
    view, with the player's own engine choice kept)."""
    out = []
    for n in range(1, n_last + 1):
        prev, rec = RP.jl("state_r%d.json" % (n - 1)), RP.jl("record_r%d.json" % n)
        year = rec["year"]
        for side in M.SIDES:
            actual = rec["orders"][side]
            states = []
            for lab, o in B.own_options(prev, side, year):
                o = dict(o)
                for f in ("fps_engine_code", "ngsa_engine_code"):
                    if f in actual and f in o and o[f] is not None and actual.get(f):
                        o[f] = actual[f]
                orders = {s2: (o if s2 == side else rec["orders"][s2]) for s2 in M.SIDES}
                s1, _ = R.adjudicate(prev, year, {k: R.validate(prev, k, year, x)[0] for k, x in orders.items()})
                states.append((lab, s1))
            row = {"round": n, "year": year, "side": side}
            for tag, kw in RULES:
                with L.patched(options=kw):
                    act = M.value(RP.jl("state_r%d.json" % n), covert=True, series=False)[side]["pv_delta"]
                    alts = {lab: M.value(s1, covert=True, series=False)[side]["pv_delta"] for lab, s1 in states}
                bp = max(alts, key=alts.get)
                row[tag] = {"actual": act, "best_plan": bp, "best": alts[bp], "gain": alts[bp] - act}
            out.append(row)
            print("r%d %-13s best now: %-45s %+5.2f | dashboard rule: %-45s %+5.2f" % (
                n, side, row["run"]["best_plan"], row["run"]["gain"], row["dashboard"]["best_plan"], row["dashboard"]["gain"]))
    return out


def final(n_last):
    s = RP.jl("state_r%d.json" % n_last)
    out = {}
    for tag, kw in RULES:
        with L.patched(options=kw):
            v = M.value(s, covert=True, series=True)
        rows = [r for r in v["_af_series"]["years"] if r["year"] <= M.REPORT_END]
        out[tag] = {"pv": {x: v[x]["pv_delta"] for x in M.SIDES}, "bridge_boeing": v["boeing"]["bridge"],
                    "bridge_airbus": v["airbus"]["bridge"],
                    "years": [{"year": r["year"], "base_pref_b": r["sd"]["pref_b_base"], "pref_b": r["boeing"]["nb_pref_share"],
                               "dlv_b": r["sd"]["dlv_max"] + r["sd"]["dlv_fps"], "dlv_a": r["sd"]["dlv_a320"] + r["sd"]["dlv_ngsa"],
                               "board_share_b": r["boeing"]["board_nb_units"] / M.af_params()["NB_PER_YR"],
                               "airbus_capacity_factor": r["sd"]["airbus_capacity_factor"]} for r in rows]}
    print("final", {t: {x: round(y, 2) for x, y in out[t]["pv"].items()} for t in out})
    return out


def main():
    n = RP.rounds_played()
    out = {"rule_change": DASH, "final": final(n), "boeing_2030_tests": boeing_tests(), "myopic": myopic(n),
           "briefs": briefs(n)}
    json.dump(out, open(os.path.join(HERE, "dashboard_rule.json"), "w"), indent=1)
    print("wrote dashboard_rule.json")


if __name__ == "__main__":
    main()
