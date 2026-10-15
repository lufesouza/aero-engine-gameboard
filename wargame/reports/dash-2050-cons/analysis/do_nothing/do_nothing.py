"""The Do Nothing case of run dash-2050-cons, broken down: Boeing launches nothing in 2030 (no fps, no 787 Re-engine,
no rate increase); everyone else's 2030 orders as played (Airbus launches NGSA on the A320 Alt plan, in service 2037);
nobody moves after 2030. Valued against the status quo (nobody launches anything).

For Boeing and Airbus, year by year, 2026-2060:
- the dashboard's narrowbody share (what the dashboard alone books: 2,000 aircraft a year split by its share rule);
- the user's preference rule (Boeing 40% less 1 point a year from NGSA's entry into service), the preference after
  the slack floor, and the delivered share; the same for the status quo;
- demand, capacity by line, deliveries, waiting customers;
- operating profit as delivered and in the status quo, and as the dashboard books it, with the discount factor and
  each programme's counting window;
plus every price and margin, and the value bridge of both makers (checked against the game's ΔPV).
Writes do_nothing.json next to this file.

  python3 do_nothing.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M, SD = L.M, L.SD
P = M.af_params()


def main():
    st = L.build({}, "new_site")
    v = M.value(st, covert=True, series=True)
    rows = [r for r in v["_af_series"]["years"] if r["year"] <= M.REPORT_END]
    years = [r["year"] for r in rows]
    # the layer's own year rows for the game and for the status quo (preference, floor, capacity, backlogs)
    board_pref = {r["year"]: r["boeing"]["board_nb_units"] / P["NB_PER_YR"] for r in rows}
    sc = SD.year_rows(st, board_pref, years)
    sq = SD.year_rows(SD.sq_state(), {y: 0.40 for y in years}, years)
    out_rows = []
    for r in rows:
        y = r["year"]
        b, a, s, q = r["boeing"], r["airbus"], sc[y], sq[y]
        # the layer's rows are the ones the valuation used
        assert abs(s["delivered_b"] - b["nb_units"]) < 1e-9 and abs(s["delivered_a"] - a["nb_units"]) < 1e-9
        assert abs(q["delivered_b"] - b["sq_nb_units"]) < 1e-9 and abs(q["delivered_a"] - a["sq_nb_units"]) < 1e-9
        tot, tot_q = s["delivered_b"] + s["delivered_a"], q["delivered_b"] + q["delivered_a"]
        out_rows.append({
            "year": y, "df_b": r["df_b"], "df_a": r["df_a"], "in_window_b": b["nb_in_window"], "in_window_a": a["nb_in_window"],
            "demand_gross": s["demand_gross"], "new_customers": s["demand"], "lost": s["lost"],
            # shares
            "board_share_b": b["board_nb_units"] / P["NB_PER_YR"], "board_share_a": a["board_nb_units"] / P["NB_PER_YR"],
            "base_pref_b": s["pref_b_base"], "pref_b": s["pref_b"], "pref_a": 1.0 - s["pref_b"],
            "delivered_share_b": s["delivered_b"] / tot, "delivered_share_a": s["delivered_a"] / tot,
            "sq_pref_b": q["pref_b"], "sq_delivered_share_b": q["delivered_b"] / tot_q, "sq_delivered_share_a": q["delivered_a"] / tot_q,
            # volumes
            "cap_b": s["cap_max"] + s["cap_fps"], "cap_a320": s["cap_a320"], "cap_ngsa": s["cap_ngsa"],
            "airbus_capacity_factor": s["airbus_capacity_factor"],
            "dlv_b": s["delivered_b"], "dlv_max": s["dlv_max"], "dlv_a320": s["dlv_a320"], "dlv_ngsa": s["dlv_ngsa"], "dlv_a": s["delivered_a"],
            "firm_b": s["firm_b"], "firm_a": s["firm_a"], "waiting_b": s["backlog_b"], "waiting_a": s["backlog_a"],
            "sq_dlv_b": q["delivered_b"], "sq_dlv_a": q["delivered_a"], "sq_cap_b": q["cap_b"], "sq_cap_a": q["cap_a"],
            "sq_capacity_factor_a": q["airbus_capacity_factor"], "sq_waiting_b": q["backlog_b"], "sq_waiting_a": q["backlog_a"],
            "sq_lost": q["lost"],
            # profit, $B a year, constant 2026 dollars
            "profit_b": b["nb_profit"], "sq_profit_b": b["sq_nb_profit"], "board_profit_b": b["board_nb_profit"], "board_sq_profit_b": b["board_sq_nb_profit"],
            "profit_a": a["nb_profit"], "sq_profit_a": a["sq_nb_profit"], "board_profit_a": a["board_nb_profit"], "board_sq_profit_a": a["board_sq_nb_profit"],
            "price_b": b["nb_price"], "price_a": a["nb_price"], "legacy_price_a": a["legacy_nb_price"], "margin_a": a["nb_margin"],
        })
    # value bridges, checked: the narrowbody lines are the window sum of (profit - status quo) x discount factor
    br = {s: v[s]["bridge"] for s in ("boeing", "airbus")}
    for side, k, dfk, w in (("boeing", "b", "df_b", "in_window_b"), ("airbus", "a", "df_a", "in_window_a")):
        layer = sum((x["profit_" + k] - x["sq_profit_" + k]) * x[dfk] for x in out_rows if x[w])
        board = sum((x["board_profit_" + k] - x["board_sq_profit_" + k]) * x[dfk] for x in out_rows if x[w])
        assert abs(layer - (br[side]["nb_profit_vs_sq"] + br[side]["supply_demand"])) < 1e-9, (side, layer)
        assert abs(board - br[side]["nb_profit_vs_sq"]) < 1e-9, (side, board)
    ng = st["prog"]["ngsa"]
    prices = {
        "737 MAX": {"price_m": P["PRICE_737"] * 1000, "margin": P["v_margin_737"]},
        "A320neo family": {"price_m": P["PRICE_A320"] * 1000, "margin": P["v_margin_a320"]},
        "NGSA": {"price_m": P["PRICE_NGSA"] * 1000, "margin": P["v_margin_angsa"]},
        "fps (for reference)": {"price_m": P["PRICE_fps"] * 1000, "margin": P["v_margin_fps"]},
        "787 (widebody)": {"price_m": P["PRICE_WB"] * 1000, "margin": P["v_margin_787"], "alone": P["v_margin_787_alone"], "both": P["v_margin_787_both"]},
        "A350 (widebody)": {"price_m": P["PRICE_WB"] * 1000, "margin": P["v_margin_a350"], "alone": P["v_margin_a350_alone"], "both": P["v_margin_a350_both"]},
    }
    for x in prices.values():
        x["unit_profit_m"] = x["price_m"] * x["margin"]
    # the prices the valuation used are these, year by year
    for x in out_rows:
        assert abs(x["price_b"] - prices["737 MAX"]["price_m"]) < 1e-9
        assert abs(x["legacy_price_a"] - prices["A320neo family"]["price_m"]) < 1e-9
    wb = {r["year"]: (r["boeing"]["wb_share"], r["boeing"]["wb_units"]) for r in rows}
    out = {"rows": out_rows, "prices": prices,
           "dashboard": {"nb_per_year": P["NB_PER_YR"], "wb_per_year": P["WB_PER_YR"], "wacc_b": P["WACC_B"], "wacc_a": P["WACC_A"],
                         "ngsa_bill_b": P["v_capex_angsa"], "boeing_wb_share": wb[2030][0], "boeing_wb_units": wb[2030][1],
                         "wb_share_constant": len({round(s_, 9) for s_, _ in wb.values()}) == 1},
           "ngsa": {"launch": ng["launch"], "eis": ng["eis"]}, "a320_plan": SD.plans(st)[0],
           "inputs": {"demand": {k: SD.inputs()["demand"][k] for k in ("class_share", "flex_share", "lapse_per_year", "firm_backlog")},
                      "options": SD.options(), "boeing": {k: SD.inputs()["boeing"][k] for k in ("max_rate", "max_rate_after", "rate_increase_per_year")}},
           "value": {s: {"pv_delta": v[s]["pv_delta"], "bridge": br.get(s, v[s]["bridge"])} for s in M.SIDES},
           "windows": {"boeing": [min(x["year"] for x in out_rows if x["in_window_b"]), max(x["year"] for x in out_rows if x["in_window_b"])],
                       "airbus": [min(x["year"] for x in out_rows if x["in_window_a"]), max(x["year"] for x in out_rows if x["in_window_a"])]}}
    M.SD_ON = False
    vd = M.value(st, covert=True, series=False)
    M.SD_ON = True
    out["dashboard_alone"] = {s: vd[s]["pv_delta"] for s in M.SIDES}
    json.dump(out, open(os.path.join(HERE, "do_nothing.json"), "w"), indent=1)
    print("values", {s: round(x["pv_delta"], 2) for s, x in out["value"].items()}, "dashboard alone", {s: round(x, 2) for s, x in out["dashboard_alone"].items()})
    print("windows", out["windows"], "wb", out["dashboard"])
    print("yr  dem | dash B  base B  pref B  dlvsh B  sqdlvsh B | B dlv sq | A320 NGSA A dlv sq | capfac | profB-sq profA-sq")
    for x in out_rows:
        if x["year"] % 2 == 0 or x["year"] in (2037, 2047):
            print(x["year"], "%5.0f | %.3f %.3f %.3f %.3f %.3f | %4.0f %4.0f | %4.0f %4.0f %4.0f %4.0f | %.3f | %+.2f %+.2f" % (
                x["demand_gross"], x["board_share_b"], x["base_pref_b"], x["pref_b"], x["delivered_share_b"], x["sq_delivered_share_b"],
                x["dlv_b"], x["sq_dlv_b"], x["dlv_a320"], x["dlv_ngsa"], x["dlv_a"], x["sq_dlv_a"], x["airbus_capacity_factor"],
                x["profit_b"] - x["sq_profit_b"], x["profit_a"] - x["sq_profit_a"]))
    print("wrote do_nothing.json")


if __name__ == "__main__":
    main()
