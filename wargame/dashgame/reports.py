"""Game-master reports for dash-2050: everything the HTML and the markdown reports show, computed from the run record.

For each round: the state after that round valued by the board ("state as of round": nobody moves afterwards),
market shares, programme dates, year-by-year financials and period totals for every player. After the game: the final
outcome, objective attainment, each player's regret, and the covert moves revealed.

  python3 reports.py            # writes ../runs/dash-2050/report_data.json
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import briefs as B  # noqa: E402
import model as M  # noqa: E402
import rules as R  # noqa: E402

RUN = os.environ.get("DASH_RUN", "dash-2050")
RUN_DIR = os.path.join(HERE, "..", "runs", RUN)
PERIODS = [(2026, 2030), (2031, 2035), (2036, 2045), (2046, 2050), (2051, 2060)]
SNAP_YEARS = [2030, 2035, 2040, 2045, 2050, 2055, 2060]


def jl(name):
    with open(os.path.join(RUN_DIR, name)) as f:
        return json.load(f)


def rounds_played():
    n = 0
    while os.path.exists(os.path.join(RUN_DIR, "record_r%d.json" % (n + 1))):
        n += 1
    return n


def years_block(v):
    """Per-year series 2026-2060 for all five players."""
    af = {r["year"]: r for r in v["_af_series"]["years"]}
    en = {r["year"]: r for r in v["_en_series"]["years"]}
    out = {"year": list(range(2026, M.REPORT_END + 1))}
    for s in ("boeing", "airbus"):
        nr = v["_af_series"]["nonrecurring"][s]
        d = {k: [] for k in ("nb_share", "wb_share", "nb_units", "wb_units", "nb_revenue", "wb_revenue", "revenue",
                             "nb_profit", "wb_profit", "profit", "sq_profit", "nonrecurring", "nb_margin", "nb_price")}
        for y in out["year"]:
            x = af[y][s]
            for k in ("nb_share", "wb_share", "nb_units", "wb_units", "nb_revenue", "wb_revenue", "nb_profit", "wb_profit",
                      "nb_margin", "nb_price"):
                d[k].append(x[k])
            d["revenue"].append(x["nb_revenue"] + x["wb_revenue"])
            d["profit"].append(x["nb_profit"] + x["wb_profit"])
            d["sq_profit"].append(x["sq_nb_profit"] + x["sq_wb_profit"])
            d["nonrecurring"].append(sum(nr.get(y, {}).values()))
        d["nonrecurring_items"] = {str(y): items for y, items in nr.items()}
        out[s] = d
    for s in ("cfm", "pratt_whitney", "rolls_royce"):
        nr = v["_en_series"]["nonrecurring"][s]
        d = {k: [] for k in ("nb_share", "wb_share", "nb_units", "wb_units", "nb_value", "wb_value", "value", "sq_value",
                             "nonrecurring")}
        for y in out["year"]:
            x = en[y][s]
            for k in ("nb_share", "wb_share", "nb_units", "wb_units", "nb_value", "wb_value"):
                d[k].append(x[k])
            d["value"].append(x["nb_value"] + x["wb_value"])
            d["sq_value"].append(x["sq_nb_value"] + x["sq_wb_value"])
            d["nonrecurring"].append(sum(nr.get(y, {}).values()))
        d["nonrecurring_items"] = {str(y): items for y, items in nr.items()}
        out[s] = d
    out["engine_moves"] = {str(r["year"]): list(r["moves"]) for r in v["_en_series"]["years"] if r["year"] <= M.REPORT_END}
    return out


def period_sums(yb):
    out = {}
    for s in M.SIDES:
        d = yb[s]
        keys = ["nb_units", "wb_units", "revenue", "profit", "sq_profit", "nonrecurring"] if s in ("boeing", "airbus") else \
            ["nb_units", "wb_units", "value", "sq_value", "nonrecurring"]
        out[s] = []
        for a, b in PERIODS:
            idx = [i for i, y in enumerate(yb["year"]) if a <= y <= b]
            out[s].append({"period": "%d-%d" % (a, b), **{k: sum(d[k][i] for i in idx) for k in keys}})
    return out


def timeline(state, year):
    rows = B.programme_rows(state, year if year else 2100)
    for r in rows:
        r["owner"] = {"fps": "boeing", "re787": "boeing", "rate737": "boeing", "ngsa": "airbus", "rea350": "airbus",
                      "jv": "pratt_whitney+rolls_royce"}.get(r["key"], M.EN_SIDE.get(r["key"], ""))
        if r["key"] in M.EN_SIDE and r["key"] != "jv":
            r["owner"] = M.EN_SIDE[r["key"]]
    fit = R.engine_fit(state)
    return {"programmes": rows, "engine_fit": fit, "codes": state["codes"], "jv_commit": state["jv_commit"],
            "delay_tactics": state["dt"], "write_offs": state["dead"]}


def objectives_block(state, v):
    return {s: [{"label": lab, "met": ok, "detail": det} for lab, ok, det in B.objective_status(s, state, v)] for s in M.SIDES}


def round_block(n):
    rec = jl("record_r%d.json" % n)
    s = jl("state_r%d.json" % n)
    v = M.value(s, covert=True, series=True)
    yb = years_block(v)
    return {
        "round": n, "year": rec["year"],
        "orders": rec["orders"], "adjustments": rec["problems"], "log": rec["log"],
        "public_statements": rec["public_statements"], "public_other_moves": rec["public_other_moves"],
        "private_other_moves": rec["private_other_moves"],
        "returned": {side: {k: x for k, x in (rec["returned"].get(side) or {}).items() if k != "orders"} for side in M.SIDES},
        "value": {side: {"pv_delta": v[side]["pv_delta"], "yield": v[side]["yield"], "bridge": v[side]["bridge"],
                         "ev": v[side]["ev"], "wacc": v[side]["wacc"]} for side in M.SIDES},
        "board_inputs": v["_af_inputs"], "engine_timing": v["_engine_timing"],
        "timeline": timeline(s, None), "years": yb, "periods": period_sums(yb),
        "snapshots": {str(y): {side: {"nb_share": yb[side]["nb_share"][y - 2026], "wb_share": yb[side]["wb_share"][y - 2026]}
                               for side in M.SIDES} for y in SNAP_YEARS},
        "objectives": objectives_block(s, v),
    }


# ─────────────────────────────── regret ───────────────────────────────
def _replay(state, n_from, records, override_side=None, override_orders=None):
    """Adjudicate rounds n_from..last from `state`, using the recorded orders (re-validated against the counterfactual
    state; anything no longer legal becomes hold). For round n_from, `override_side` plays `override_orders`."""
    s = state
    for n in range(n_from, len(records) + 1):
        rec = records[n - 1]
        year = rec["year"]
        orders = {}
        for side in M.SIDES:
            o = override_orders if (n == n_from and side == override_side) else rec["orders"][side]
            orders[side], _ = R.validate(s, side, year, o)
        s, _ = R.adjudicate(s, year, orders)
    return s


def regret(n_rounds):
    """For each round and player: the payoff of every own alternative, holding the other players' actual orders.
    Myopic: nobody moves after the round (the brief's view). Ex post: later rounds replayed with everyone's actual
    orders. Regret = best alternative minus the actual choice."""
    records = [jl("record_r%d.json" % n) for n in range(1, n_rounds + 1)]
    states = [jl("state_r%d.json" % n) for n in range(0, n_rounds + 1)]
    out = {}
    for n in range(1, n_rounds + 1):
        rec = records[n - 1]
        year = rec["year"]
        prev = states[n - 1]
        out[str(n)] = {}
        for side in M.SIDES:
            actual = rec["orders"][side]
            alts = []
            for lab, o in B.own_options(prev, side, year):
                o = dict(o)
                for f in ("fps_engine_code", "ngsa_engine_code"):   # keep the player's own engine choice
                    if f in actual and f in o and o[f] is not None and actual.get(f):
                        o[f] = actual[f]
                orders = {s2: (o if s2 == side else rec["orders"][s2]) for s2 in M.SIDES}
                s1, _ = R.adjudicate(prev, year, {k: R.validate(prev, k, year, x)[0] for k, x in orders.items()})
                my = M.value(s1, covert=True, series=True)[side]["pv_delta"]
                fin = _replay(prev, n, records, side, o)
                ep = M.value(fin, covert=True, series=True)[side]["pv_delta"]
                alts.append({"plan": lab, "orders": o, "myopic": my, "ex_post": ep})
            act_my = M.value(states[n], covert=True, series=True)[side]["pv_delta"]
            act_ep = M.value(states[n_rounds], covert=True, series=True)[side]["pv_delta"]
            bm = max(alts, key=lambda a: a["myopic"])
            be = max(alts, key=lambda a: a["ex_post"])
            out[str(n)][side] = {"actual_myopic": act_my, "actual_ex_post": act_ep,
                                 "best_myopic": bm, "best_ex_post": be,
                                 "regret_myopic": bm["myopic"] - act_my, "regret_ex_post": be["ex_post"] - act_ep,
                                 "alternatives": alts}
    return out


def board_check(state):
    """The user's board alone at the final state, next to the GM valuation: airframers from evaluate_scenario() at the
    state's dates, engine makers from simulate() with the final engine selections at the board's fixed 50/50 split."""
    H = M.H
    va = M.value_airframers(state, covert=True, series=False)
    v = M.value(state, covert=True, series=True)
    mod = M.en_board()["_MOD"]
    sup = {c: o for o, c in mod.SUPPLIER_CODE.items()}
    bc, ac = state["codes"].get("fps", 7), state["codes"].get("ngsa", 7)
    rr, pw, cfm = mod.derive_nb_engine_shares(bc, ac, 50)
    eis = va["_inputs"]["eis"]
    over = {"_b_supplier": sup[bc], "_a_supplier": sup[ac], "_last_b_supp_seen": sup[bc], "_last_a_supp_seen": sup[ac],
            "_last_boeing_share_seen": 50, "f_cfm_nb": cfm, "f_pw_nb": pw, "f_rr_nb": rr, "f_jv_nb": pw + rr,
            "af_fps_eis": eis[0], "af_ngsa_eis": eis[1], "af_787_eis": eis[2], "af_a350_eis": eis[3]}
    SE = H.en(over)
    last = [r for r in v["_en_series"]["years"] if r["year"] == M.REPORT_END][0]["moves"]
    res = SE["_ESIM"](last[0], SE["_EPW"], last[2], 31)
    out = {"boeing": {"board": va["boeing"]["board_pv_delta"], "gm": va["boeing"]["pv_delta"]},
           "airbus": {"board": va["airbus"]["board_pv_delta"], "gm": va["airbus"]["pv_delta"]}}
    for side, k in (("cfm", "A"), ("pratt_whitney", "B"), ("rolls_royce", "C")):
        out[side] = {"board": res[k]["delta_b"], "gm": v[side]["pv_delta"]}
    out["_engine_inputs"] = {"codes": [bc, ac], "pw_lock": SE["_EPW"], "cfm_move": last[0], "rr_move": last[2],
                             "f_nb": [cfm, pw, rr], "eis": list(eis)}
    return out


def build(n_rounds=None):
    n_rounds = n_rounds or rounds_played()
    data = {"run": RUN, "rounds": [round_block(n) for n in range(1, n_rounds + 1)]}
    data["status_quo"] = {"note": "Status quo: nobody launches anything; every ΔPV is measured against it."}
    s0 = jl("state_r0.json")
    v0 = M.value(s0, covert=True, series=True)
    data["status_quo"]["years"] = years_block(v0)
    data["regret"] = regret(n_rounds)
    data["board_check"] = board_check(jl("state_r%d.json" % n_rounds))
    data["stage"] = {str(n): jl("stage_r%d.json" % n) for n in range(1, n_rounds + 1)
                     if os.path.exists(os.path.join(RUN_DIR, "stage_r%d.json" % n))}
    data["audit"] = {str(n): jl("audit_r%d.json" % n) for n in range(1, n_rounds + 1)
                     if os.path.exists(os.path.join(RUN_DIR, "audit_r%d.json" % n))}
    data["params"] = {"af": {k: v for k, v in M.af_params().items() if isinstance(v, (int, float))},
                      "en": M.engine_params()}
    with open(os.path.join(RUN_DIR, "report_data.json"), "w") as f:
        json.dump(data, f, indent=1, default=str)
    return data


if __name__ == "__main__":
    d = build()
    print("rounds", len(d["rounds"]))
    for r in d["rounds"]:
        print(r["year"], {s: round(r["value"][s]["pv_delta"], 2) for s in M.SIDES})
