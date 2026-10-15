"""Does the 7-year fps (launched 2030, in service 2037, $65.0B) improve on the 10-year (in service 2040, $60.3B)?
Run dash-2050-cons. Reads ../fps_business_case/case.json (make_case.py: both cases, game and cash views) and adds:
Boeing's 2030 brief for every 7-year plan and its tests (incl. fundable), deliveries by period, the dashboard alone and
the previous game's market, the 7-year's thresholds (margin, price, bill, ramp speed) next to the 10-year's, and the
7-year in later rounds' briefs. Writes seven_year.json next to this file.

  python3 seven_year.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M, SD = L.M, L.SD
P = M.af_params()
CASE = json.load(open(os.path.join(HERE, "..", "fps_business_case", "case.json")))
PLANS = {("10yr", "renton"): L.PLAN_REN, ("10yr", "new_site"): L.PLAN_NEW,
         ("7yr", "renton"): "fps 7-yr at Renton + 787: hold", ("7yr", "new_site"): L.PLAN_7}
BILL = {"10yr": P["v_capex_fps_10yr"], "7yr": P["v_capex_fps_7yr"]}


def grid(kw=None, sd_on=True):
    M.SD_ON = sd_on
    try:
        with L.patched(**(kw or {})):
            out = {}
            for k, plan in PLANS.items():
                items = L.grid_items(plan)[0]
                out[k] = {"items": items, **L.tests(items), "margin": L.margin(items)}
            return out
    finally:
        M.SD_ON = True


def fundable():
    out = {}
    for k, plan in PLANS.items():
        cols = []
        for st, cv in L.grid_states(plan):
            v = M.value(st, covert=cv, series=True)
            m = L.B.plan_metrics("boeing", st, v, cv)
            cols.append({"stress_ok": m["stress_ok"], "stress_peak": m["stress_peak"]})
        out["%s/%s" % k] = cols
    return out


def pen_pv(bill, df):
    pv = bill * df
    return M.true_cost(bill, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"]) - pv


def analytic(key, kw=None):
    """Margin, price and bill thresholds for one plan (linear in each column's delivered fps; bill with the debt
    penalty), as in thresholds.py, with the plan's own bill."""
    variant, _ = key
    plan = PLANS[key]
    with L.patched(**(kw or {})):
        base = L.grid_items(plan)[0]
        terms = []
        for st, cv in L.grid_states(plan):
            v = M.value(st, covert=cv, series=True)
            U = Vp = 0.0
            for r in v["_af_series"]["years"]:
                x = r["boeing"]
                if x["nb_in_window"]:
                    n = x.get("nb_units_new", 0.0)
                    U += n * r["df_b"] * x["nb_price"] / 1000.0
                    Vp += n * r["df_b"] * x["nb_margin"] / 1000.0
            eis = st["prog"]["fps"]["eis"]
            df = 1.0 / (1 + P["WACC_B"]) ** (eis - 2026)
            br = v["boeing"]["bridge"]
            assert abs(br["programme_investment"] + BILL[variant] * df) < 1e-6
            assert abs(br["debt_penalty"] + pen_pv(BILL[variant], df)) < 1e-6
            terms.append((U, Vp, df))
    m0, p0, b0 = P["v_margin_fps"], P["PRICE_fps"] * 1000.0, BILL[variant]
    im = lambda m: [b + U * (m - m0) for b, (U, _, _) in zip(base, terms)]
    ip = lambda p: [b + Vp * (p - p0) for b, (_, Vp, _) in zip(base, terms)]
    ib = lambda x: [b - (x - b0) * df - (pen_pv(x, df) - pen_pv(b0, df)) for b, (_, _, df) in zip(base, terms)]
    return {"margin": L.bisect(lambda m: L.margin(im(m)), m0, 1.0, 0.0, tol=1e-7),
            "price": L.bisect(lambda p: L.margin(ip(p)), p0, 400.0, 0.0, tol=1e-5),
            "bill": L.bisect(lambda x: L.margin(ib(x)), b0, 0.0, 0.0, tol=1e-5), "bill_base": b0}


def deliveries():
    """Boeing's deliveries by period, Do Nothing and each fps (played column), and the fps's own."""
    st = {"dn": L.build({}, "new_site"), "10yr/renton": L.build(L.F10, "renton"), "10yr/new_site": L.build(L.F10, "new_site"),
          "7yr/renton": L.build(L.F7, "renton"), "7yr/new_site": L.build(L.F7, "new_site")}
    out = {}
    for k, s in st.items():
        v = M.value(s, covert=True, series=True)
        rows = {r["year"]: r for r in v["_af_series"]["years"]}
        out[k] = {"by_year": {y: {"boeing": rows[y]["boeing"]["nb_units"], "fps": rows[y]["sd"]["dlv_fps"],
                                  "cap_b": rows[y]["sd"]["cap_max"] + rows[y]["sd"]["cap_fps"], "pref": rows[y]["boeing"]["nb_pref_share"]}
                              for y in range(2030, 2061)}}
    return out


def main():
    out = {"bills": BILL}
    base = grid()
    out["grid"] = {"%s/%s" % k: v for k, v in base.items()}
    for k, v in base.items():
        print("%-14s exp %+.2f worst %+.2f risk %+.2f  %s" % ("%s/%s" % k, v["expected"], v["worst"], v["risk_case"], [round(x, 2) for x in v["items"]]))
    out["fundable"] = fundable()
    for k, cols in out["fundable"].items():
        print("fundable", k, [(c["stress_ok"], round(c["stress_peak"], 2)) for c in cols])
    out["dashboard_alone"] = {"%s/%s" % k: v for k, v in grid(sd_on=False).items()}
    prev = {"demand_curve": None, "firm_backlog": None, "boeing_pp_after_ngsa": None, "boeing_takes_airbus_slack": None,
            "airbus_capacity_response": None}
    out["previous_market"] = {"%s/%s" % k: v for k, v in grid({"options": prev}).items()}
    for lab, g in (("dashboard alone", out["dashboard_alone"]), ("previous market", out["previous_market"])):
        print(lab, {k: round(v["expected"], 2) for k, v in g.items()})
    out["analytic"] = {"%s/%s" % k: analytic(k) for k in PLANS}
    for k, a in out["analytic"].items():
        print("thresholds", k, {x: (round(y, 4) if isinstance(y, float) else y) for x, y in a.items()})
    # ramp speed needed, each plan
    ramp = {}
    for k in PLANS:
        f = lambda x, k=k: grid_one(k, {"ramp": L.compressed(x)})
        ramp["%s/%s" % k] = L.bisect(f, 1.0, 12.0, 0.0, tol=1e-4)
    out["ramp_threshold"] = ramp
    print("ramp thresholds", {k: (round(v, 3) if v else v) for k, v in ramp.items()})
    out["deliveries"] = deliveries()
    # later rounds: the 7-year in each brief
    later = []
    for n in (1, 2, 3, 4):
        g = L.RP.jl("grids_r%d.json" % n)["boeing"]
        rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
        dn = rows[L.PLAN_DN]
        for k, plan in PLANS.items():
            if plan in rows:
                it = [a - b for a, b in zip(rows[plan], dn)]
                later.append({"round": n, "year": L.RP.jl("record_r%d.json" % n)["year"], "plan": "%s/%s" % k, "best": max(it), "worst": min(it)})
    out["later_rounds"] = later
    json.dump(out, open(os.path.join(HERE, "seven_year.json"), "w"), indent=1, default=str)
    print("wrote seven_year.json")


def grid_one(key, kw):
    with L.patched(**kw):
        items = L.grid_items(PLANS[key])[0]
    return L.margin(items)


if __name__ == "__main__":
    main()
