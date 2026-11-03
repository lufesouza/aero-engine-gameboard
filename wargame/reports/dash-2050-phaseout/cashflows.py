"""The cash flows behind Boeing's fps case in the MAX phase-out game: Boeing's 2030 brief (round 1), the column the CEO
expected (S2: Airbus launches NGSA), for Do Nothing, the 10-year fps at Renton and the 7-year fps at Renton.

For each plan, year by year (constant 2026 $B, as the board books them), against the status quo (nobody launches):
  narrowbody profit   - 737 MAX delivered x its profit per aircraft ($48M x 8%) + fps delivered x the fps's ($55M x
                        25.64%), less the status quo's MAX deliveries x the MAX profit; counted only inside the plan's
                        window (20 years from the fps entry into service; Do Nothing to 2060)
  widebody profit     - the same for the 787 (zero here: no plan re-engines it)
  Renton saving       - new-site capex avoided by building the fps at Renton, booked at entry into service
  fps bill            - the development bill, booked as one lump at entry into service, as the brief books it
  debt penalty        - the board's charge on the extra debt, booked at the same date
then discounted to 2026 at Boeing's WACC. The discounted sum is asserted equal to the brief's value of each plan (and the
fps minus Do Nothing to the brief's item), to the cent and better.

Also the cash view Boeing's net-debt test uses: the same bill spent through the development years on the game's
phasing curve (finance.programme_cash; the Renton saving there is spread over the years the new site would have been
built), with each plan's base and stress-case net debt. Writes data/cashflows.json.

  python3 cashflows.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402
import thresholds as T  # noqa: E402

M, B = L.M, L.B
import finance as FIN  # noqa: E402

P = M.af_params()
N, COL = 1, 1                  # round 1 (2030), column S2
PLANS = {"Do Nothing": T.DN, "10-year at Renton": T.SOLO["10-year at Renton"][0], "7-year at Renton": T.SOLO["7-year at Renton"][0]}


def plan_flows(name, plan):
    slab, s, c = T.column_states(N, plan)[COL]
    v = M.value(s, covert=c, series=True)
    bo = v["boeing"]
    ser = v["_af_series"]
    eis, a, b, dt = M.af_inputs(s, c)
    cell = M.eval_cell(eis, a, b)
    tcd = cell["b_tc_data"]
    fps = s["prog"].get("fps")
    bill = M.af_bill("fps", fps["variant"]) if fps else 0.0
    br = bo["bridge"]
    rows = []
    for r in ser["years"]:
        y, x = r["year"], r["boeing"]
        df = r["df_b"]
        max_unit = x["sq_nb_profit"] / x["sq_nb_units"] if x["sq_nb_units"] else P["PRICE_737"] * P["v_margin_737"]
        fps_unit = x["nb_price"] / 1000.0 * x["nb_margin"] if x["nb_units_new"] else 0.0
        nb = x["nb_profit"] - x["sq_nb_profit"] if x["nb_in_window"] else 0.0
        wb = x["wb_profit"] - x["sq_wb_profit"] if x["wb_in_window"] else 0.0
        rows.append({"year": y, "df": df, "in_window": x["nb_in_window"], "max_units": x["nb_units_old"], "fps_units": x["nb_units_new"],
                     "sq_max_units": x["sq_nb_units"], "max_unit_profit": max_unit, "fps_unit_profit": fps_unit,
                     "max_profit": x["nb_units_old"] * max_unit, "fps_profit": x["nb_units_new"] * fps_unit, "sq_profit": x["sq_nb_profit"],
                     "nb_vs_sq": nb, "wb_vs_sq": wb, "renton": 0.0, "bill": 0.0, "penalty": 0.0, "strain": 0.0})
    by = {r["year"]: r for r in rows}
    if fps:
        e = fps["eis"]
        dfe = by[e]["df"]
        by[e]["bill"] = -bill
        by[e]["penalty"] = br["debt_penalty"] / dfe                 # the penalty in money of its year (PV'd at the bill's date)
        by[e]["strain"] = br["two_front_strain"] / dfe
        for side, yy, item, xx in T.L.SD.costs(s):
            if side == "boeing":
                by[yy]["renton"] += -xx
    for r in rows:
        r["net"] = r["nb_vs_sq"] + r["wb_vs_sq"] + r["renton"] + r["bill"] + r["penalty"] + r["strain"]
        r["pv"] = r["net"] * r["df"]
    pv = sum(r["pv"] for r in rows)
    assert abs(pv - bo["pv_delta"]) < 1e-9, (name, pv, bo["pv_delta"])
    # the bridge, line by line
    pv_nb = sum(r["nb_vs_sq"] * r["df"] for r in rows)
    assert abs(pv_nb - (br["nb_profit_vs_sq"] + br["supply_demand"])) < 1e-9
    assert abs(sum(r["bill"] * r["df"] for r in rows) - br["programme_investment"]) < 1e-9
    assert abs(sum(r["renton"] * r["df"] for r in rows) - br["supply_plan"]) < 1e-9
    # the cash view: the bill through the development years, and net debt (base and stress)
    cash = FIN.programme_cash(s)
    spend = {y: sum(x for k, x in d.items() if k.startswith("fps")) for y, d in cash.items()}
    other = {y: sum(x for k, x in d.items() if not k.startswith("fps")) for y, d in cash.items()}
    if fps:
        assert abs(sum(spend.values()) - bill) < 1e-9
    base = {r["year"]: r for r in FIN.debt_path(s)}
    stress = {r["year"]: r for r in FIN.debt_path(s, fcf_scale=FIN.inputs()["stress_fcf_scale"])}
    for r in rows:
        y = r["year"]
        r["cash_spend"] = spend.get(y, 0.0)
        r["cash_other"] = other.get(y, 0.0)              # the Renton saving, spread over the site's build years
        r["net_debt"] = base[y]["debt"] if y in base else None
        r["net_debt_stress"] = stress[y]["debt"] if y in stress else None
    return {"plan": plan, "column": slab, "eis": fps["eis"] if fps else None, "launch": fps["launch"] if fps else None,
            "bill": bill, "pv": pv, "bridge": br, "rows": rows,
            "window_end": max(r["year"] for r in rows if r["in_window"]),
            "tc": {"nom": tcd.get("nom_capex", 0.0), "pv": tcd.get("pv_capex", 0.0)}}


def main():
    with L.patched(options=T.O):
        out = {"round": N, "year": 2030, "params": {"max_price": P["PRICE_737"] * 1000, "max_margin": P["v_margin_737"],
                                                   "fps_price": P["PRICE_fps"] * 1000, "fps_margin": P["v_margin_fps"],
                                                   "wacc": P["WACC_B"], "bill_10": T.BILL0["10yr"], "bill_7": T.BILL0["7yr"],
                                                   "phasing_curve": FIN.inputs()["phasing_curve"]},
               "plans": {name: plan_flows(name, plan) for name, plan in PLANS.items()}}
        # the fps items against Do Nothing match the brief's grid and thresholds.json
        g = json.load(open(os.path.join(HERE, "record", "grids_r1.json")))["boeing"]
        rows = {x["plan"]: [c_[0] for c_ in x["cells"]] for x in g["rows"]}
        out["column"] = out["plans"]["Do Nothing"]["column"]
        for name in ("10-year at Renton", "7-year at Renton"):
            item = out["plans"][name]["pv"] - out["plans"]["Do Nothing"]["pv"]
            want = rows[PLANS[name]][COL] - rows[T.DN][COL]
            assert abs(item - want) < 1e-9, (name, item, want)
            out["plans"][name]["item_vs_dn"] = item
    json.dump(out, open(os.path.join(HERE, "data", "cashflows.json"), "w"), indent=1)
    for name, p in out["plans"].items():
        print("%-18s PV %+7.3f  (EIS %s, window to %d)  bridge %s" % (name, p["pv"], p["eis"], p["window_end"],
              {k: round(v, 3) for k, v in p["bridge"].items() if abs(v) > 1e-9}))
    print("wrote data/cashflows.json")


if __name__ == "__main__":
    main()
