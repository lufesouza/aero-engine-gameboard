"""What would have to change for the 10-year fps to pass Boeing's own 2030 tests (run dash-2050-cons).

Boeing's 2030 decision, exactly as its brief valued it (lib.grid_items: the six rival-scenario columns), against
Boeing's three value tests from its Board's round-1 guidance: more than +$1B against Do Nothing in the expected column
(S2 and S5 at even odds, the CEO's expectation), no worse than -$1B in any column, and the risk case (S6) no more than
$2B below Do Nothing. For each lever alone: the value at which the better site's fps passes all three, found by
bisection on the brief's own valuation (or exactly, for the margin, price and bill, whose effect is linear in each
column's fps deliveries). Also: the market-rule variants, an NGSA delay, the dashboard alone, two-lever combinations,
and the later rounds. Writes thresholds.json next to this file.

  python3 thresholds.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M, SD = L.M, L.SD
PLANS = {"renton": L.PLAN_REN, "new_site": L.PLAN_NEW}
SITE = {"renton": "Renton", "new_site": "new sites"}


def evaluate(kw=None, post=None, sd_on=True):
    out = {}
    M.SD_ON = sd_on
    try:
        with L.patched(**(kw or {})):
            for site, plan in PLANS.items():
                items, row, dn = L.grid_items(plan, post)
                t = L.tests(items)
                out[site] = {"items": items, "plan_row": row, "dn_row": dn, **t, "margin": L.margin(items)}
    finally:
        M.SD_ON = True
    out["best"] = max(PLANS, key=lambda s: out[s]["margin"])
    return out


def binding(t):
    parts = {"business case": t["expected"] - L.BUSINESS_CASE, "downside": t["worst"] - L.DOWNSIDE, "buffer": t["risk_case"] - L.BUFFER}
    return min(parts, key=parts.get)


BASE = evaluate()


def lever_threshold(key, label, unit, make_kw, lo, hi, fmt):
    f = lambda x: max(evaluate(make_kw(x))[s]["margin"] for s in PLANS)
    x = L.bisect(f, lo, hi, 0.0, tol=1e-4)
    rec = {"key": key, "lever": label, "unit": unit, "base": lo, "searched_to": hi, "threshold": x}
    if x is not None:
        ev = evaluate(make_kw(x))
        s = ev["best"]
        rec.update({"site": s, "items": ev[s]["items"], "expected": ev[s]["expected"], "worst": ev[s]["worst"],
                    "risk_case": ev[s]["risk_case"], "binding": binding(ev[s]), "label": fmt(x)})
    else:
        ev = evaluate(make_kw(hi))
        s = ev["best"]
        rec.update({"site": s, "at_limit": {"items": ev[s]["items"], "expected": ev[s]["expected"]}, "label": "not reached"})
    print("%-50s threshold %s (%s) %s" % (label, None if x is None else round(x, 4), rec.get("site"), rec["label"]))
    return rec


# ─────────────────────────────── plain-unit translations ───────────────────────────────
S_DN = L.build({}, "new_site")
S_REN = L.build(L.F10, "renton")


def demand_avg(k, a=2040, z=2060):
    return sum(SD.demand(y) * k for y in range(a, z + 1)) / (z - a + 1)


def growth_avg(k, a=2040, z=2060):
    return sum(SD.growth(y) * k for y in range(a, z + 1)) / (z - a + 1)


def ramp_profile(k, state=S_REN):
    with L.patched(ramp=L.compressed(k)):
        caps = {y: SD.boeing_capacity(state, y)[1] for y in range(2038, 2056)}
    eis = state["prog"]["fps"]["eis"]
    full = next((y for y in sorted(caps) if caps[y] >= 0.99 * SD.fps_full()), None)
    r90 = next((y for y in sorted(caps) if caps[y] >= 1079.0), None)
    return {"by_year": caps, "first5": sum(caps[y] for y in range(eis, eis + 5)), "full_rate_year": full, "rate90_year": r90}


def pref_profile(pp, state=S_REN):
    v = M.value(state, covert=True, series=True)
    return {r["year"]: r["boeing"]["nb_pref_share"] for r in v["_af_series"]["years"] if 2040 <= r["year"] <= 2060}


# ─────────────────────────────── analytic levers ───────────────────────────────
P = M.af_params()


def column_terms(plan):
    """Per column: $B of value per point of fps margin (U) and per $M of fps price (V), the fps entry into service,
    and the bill and debt-penalty lines, from the column state's own series and bridge."""
    out = []
    for st, cv in L.grid_states(plan):
        v = M.value(st, covert=cv, series=True)
        U = V = 0.0
        for r in v["_af_series"]["years"]:
            x = r["boeing"]
            if x["nb_in_window"]:
                n = x.get("nb_units_new", 0.0)
                U += n * r["df_b"] * x["nb_price"] / 1000.0
                V += n * r["df_b"] * x["nb_margin"] / 1000.0
        eis = st["prog"]["fps"]["eis"]
        br = v["boeing"]["bridge"]
        out.append({"U": U, "V": V, "eis": eis, "df": 1.0 / (1 + P["WACC_B"]) ** (eis - 2026),
                    "investment": br.get("programme_investment", 0.0), "debt_penalty": br.get("debt_penalty", 0.0)})
    return out


def pen_pv(bill, df):
    pv = bill * df
    return M.true_cost(bill, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"]) - pv


def analytic(site, kw=None):
    plan = PLANS[site]
    with L.patched(**(kw or {})):
        base = L.grid_items(plan)[0] if kw else BASE[site]["items"]
        terms = column_terms(plan)
    bill0 = P["v_capex_fps_10yr"]
    m0, p0 = P["v_margin_fps"], P["PRICE_fps"] * 1000.0
    # the bill and debt penalty lines must be the dashboard's own formula, column by column (Do Nothing has none)
    for t in terms:
        assert abs(t["investment"] + bill0 * t["df"]) < 1e-6, (t["investment"], bill0 * t["df"])
        assert abs(t["debt_penalty"] + pen_pv(bill0, t["df"])) < 1e-6, (t["debt_penalty"], pen_pv(bill0, t["df"]))
    def items_margin(m):
        return [b + t["U"] * (m - m0) for b, t in zip(base, terms)]
    def items_price(p):
        return [b + t["V"] * (p - p0) for b, t in zip(base, terms)]
    def items_bill(x):
        return [b - (x - bill0) * t["df"] - (pen_pv(x, t["df"]) - pen_pv(bill0, t["df"])) for b, t in zip(base, terms)]
    m = L.bisect(lambda m: L.margin(items_margin(m)), m0, 1.0, 0.0, tol=1e-7)
    p = L.bisect(lambda p: L.margin(items_price(p)), p0, 400.0, 0.0, tol=1e-5)
    bl = L.bisect(lambda x: L.margin(items_bill(x)), bill0, 0.0, 0.0, tol=1e-5)
    return {"margin": {"base": m0, "threshold": m, "items": items_margin(m) if m else None},
            "price": {"base": p0, "threshold": p, "items": items_price(p) if p else None},
            "bill": {"base": bill0, "threshold": bl, "items": items_bill(bl) if bl is not None else None,
                     "at_zero": items_bill(1e-9)},
            "terms": terms}


def ngsa_delay(eis):
    def post(st):
        ng = st["prog"].get("ngsa")
        if ng and ng.get("cancel") is None:
            ng["eis"] = eis
        return st
    return post


def main():
    out = {"tests": {"business_case": L.BUSINESS_CASE, "downside": L.DOWNSIDE, "buffer": L.BUFFER,
                     "expected_weights": {L.SCEN_LABELS[i]: w for i, w in L.EXPECTED.items()}},
           "columns": L.SCEN_LABELS, "base": BASE}
    print("base", {s: [round(x, 2) for x in BASE[s]["items"]] for s in PLANS})
    lev = []
    lev.append(lever_threshold("demand", "Single-aisle demand: your whole curve", "x", lambda k: {"demand_k": k}, 1.0, 4.0,
                               lambda k: f"x{k:.2f}: {demand_avg(k):,.0f} aircraft a year in 2040-2060, against {demand_avg(1):,.0f}"))
    lev.append(lever_threshold("growth", "Fleet growth in your curve (replacement unchanged)", "x", lambda k: {"growth_k": k}, 1.0, 6.0,
                               lambda k: f"x{k:.2f}: growth {growth_avg(k):,.0f} a year in 2040-2060, against {growth_avg(1):,.0f}"))
    lev.append(lever_threshold("pref", "Boeing's preference once the fps is in service", "points", lambda x: {"fps_pref_pp": x}, 0.0, 60.0,
                               lambda x: f"+{x:.1f} points"))
    lev.append(lever_threshold("ramp", "fps production ramp-up speed", "x faster", lambda k: {"ramp": L.compressed(k)}, 1.0, 12.0,
                               lambda k: f"{k:.2f} times as fast"))
    out["levers"] = lev
    # translations
    rp = next(x for x in lev if x["key"] == "ramp")
    out["ramp_profiles"] = {"game": ramp_profile(1.0), "threshold": ramp_profile(rp["threshold"]) if rp["threshold"] else None,
                            "instant": None}
    with L.patched(ramp=L.instant):
        caps = {y: SD.boeing_capacity(S_REN, y)[1] for y in range(2038, 2056)}
    out["ramp_profiles"]["instant"] = {"by_year": caps}
    out["pref_profile"] = pref_profile(0)
    out["instant_ramp"] = evaluate({"ramp": L.instant})
    # analytic levers, both sites
    out["analytic"] = {s: analytic(s) for s in PLANS}
    for s in PLANS:
        a = out["analytic"][s]
        print(SITE[s], "margin", a["margin"]["base"], "->", a["margin"]["threshold"], "| price", a["price"]["base"], "->", a["price"]["threshold"],
              "| bill", a["bill"]["base"], "->", a["bill"]["threshold"], "at zero bill", [round(x, 2) for x in a["bill"]["at_zero"]])
    # market rules and other worlds (no threshold: does it pass?)
    worlds = [("As played", {}, None, True),
              ("Boeing loses 2 points a year after NGSA", {"options": {"boeing_pp_after_ngsa": 2.0}}, None, True),
              ("Boeing loses 3 points a year after NGSA", {"options": {"boeing_pp_after_ngsa": 3.0}}, None, True),
              ("No slack floor", {"options": {"boeing_takes_airbus_slack": None}}, None, True),
              ("No Airbus capacity response", {"options": {"airbus_capacity_response": None}}, None, True),
              ("Airbus capacity response 2% a year", {"options": {"airbus_capacity_response": 0.02}}, None, True),
              ("Firm orders on top of demand", {"options": {"firm_backlog": None}}, None, True),
              ("Previous game's market (dash-2050-sd)", {"options": {"demand_curve": None, "firm_backlog": None, "boeing_pp_after_ngsa": None,
                                                                    "boeing_takes_airbus_slack": None, "airbus_capacity_response": None}}, None, True),
              ("Boeing's total cap 120 a month", {"total_cap": 120.0}, None, True),
              ("NGSA in service 2040 (3 years late)", {}, ngsa_delay(2040), True),
              ("NGSA in service 2043 (6 years late)", {}, ngsa_delay(2043), True),
              ("fps at full rate from entry into service", {"ramp": L.instant}, None, True),
              ("Dashboard alone (no supply limits)", {}, None, False)]
    out["worlds"] = []
    for lab, kw, post, on in worlds:
        ev = evaluate(kw, post, on)
        s = ev["best"]
        out["worlds"].append({"world": lab, "site": s, "items": ev[s]["items"], "expected": ev[s]["expected"], "worst": ev[s]["worst"],
                              "risk_case": ev[s]["risk_case"], "passes": ev[s]["passes"], "margin": ev[s]["margin"],
                              "other_site_expected": ev["new_site" if s == "renton" else "renton"]["expected"]})
        print("%-45s %-9s exp %+.2f worst %+.2f risk %+.2f passes %s" % (lab, SITE[s], ev[s]["expected"], ev[s]["worst"], ev[s]["risk_case"], ev[s]["passes"]))
    # combinations: the demand needed at a given ramp speed, and at a given preference uplift
    combos = {"ramp_vs_demand": [], "pref_vs_demand": []}
    for k in (1.0, 1.5, 2.0, 2.5):
        f = lambda d, k=k: max(evaluate({"ramp": L.compressed(k), "demand_k": d})[s]["margin"] for s in PLANS)
        d = L.bisect(f, 0.5, 4.0, 0.0, tol=1e-4)
        combos["ramp_vs_demand"].append({"ramp": k, "demand_k": d, "demand_avg": demand_avg(d) if d else None})
        print("ramp", k, "needs demand x", d)
    for pp in (0.0, 5.0, 10.0, 15.0, 20.0):
        f = lambda d, pp=pp: max(evaluate({"fps_pref_pp": pp, "demand_k": d})[s]["margin"] for s in PLANS)
        d = L.bisect(f, 0.5, 4.0, 0.0, tol=1e-4)
        combos["pref_vs_demand"].append({"pref_pp": pp, "demand_k": d, "demand_avg": demand_avg(d) if d else None})
        print("pref +", pp, "needs demand x", d)
    for k in (1.0, 1.5, 2.0, 2.5):
        best = {}
        for s in PLANS:
            a = analytic(s, {"ramp": L.compressed(k)})
            best[s] = (a["margin"]["threshold"], a["bill"]["threshold"])
        m_s = min(PLANS, key=lambda s: best[s][0] if best[s][0] is not None else 9)
        b_s = max(PLANS, key=lambda s: best[s][1] if best[s][1] is not None else -9)
        combos.setdefault("ramp_vs_margin", []).append({"ramp": k, "margin": best[m_s][0], "site": m_s})
        combos.setdefault("ramp_vs_bill", []).append({"ramp": k, "bill": best[b_s][1], "site": b_s})
        print("ramp", k, "needs margin", best[m_s][0], m_s, "or bill", best[b_s][1], b_s)
    out["combos"] = combos
    # sweeps: the expected-column value (better site) as one lever moves
    sw = {}
    for key, xs, mk in (("demand", [1.0 + 0.1 * i for i in range(21)], lambda x: {"demand_k": x}),
                        ("growth", [1.0 + 0.25 * i for i in range(17)], lambda x: {"growth_k": x}),
                        ("pref", [2.5 * i for i in range(17)], lambda x: {"fps_pref_pp": x}),
                        ("ramp", [1.0 + 0.25 * i for i in range(17)], lambda x: {"ramp": L.compressed(x)})):
        pts = []
        for x in xs:
            ev = evaluate(mk(x))
            pts.append({"x": x, "renton": ev["renton"]["expected"], "new_site": ev["new_site"]["expected"],
                        "worst_renton": ev["renton"]["worst"], "worst_new_site": ev["new_site"]["worst"]})
        sw[key] = pts
    out["sweeps"] = sw
    # later rounds: the 10-year fps against Do Nothing in each round's own brief (Boeing's grids as played)
    later = []
    for n in (1, 2, 3, 4):
        g = L.RP.jl("grids_r%d.json" % n)["boeing"]
        rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
        dn = rows[L.PLAN_DN]
        for site, plan in (("renton", "fps 10-yr at Renton + 787: hold"), ("new_site", "fps 10-yr + 787: hold")):
            if plan in rows:
                items = [a - b for a, b in zip(rows[plan], dn)]
                later.append({"round": n, "year": L.RP.jl("record_r%d.json" % n)["year"], "site": site, "columns": g["scenarios"],
                              "items": items, "best": max(items), "worst": min(items)})
    out["later_rounds"] = later
    # Boeing's other 2030 tests: fundable (net debt held in the stress case) for each plan in each column, and the
    # 787 Re-engine's item values (its downside), from the brief's own cells
    fund = {}
    for key, plan in (("renton", L.PLAN_REN), ("new_site", L.PLAN_NEW), ("do_nothing", L.PLAN_DN)):
        cols = []
        for st, cv in L.grid_states(plan):
            v = M.value(st, covert=cv, series=True)
            m = L.B.plan_metrics("boeing", st, v, cv)
            cols.append({"held_ok": m["held_ok"], "stress_ok": m["stress_ok"], "stress_peak": m["stress_peak"]})
        fund[key] = cols
    out["fundable"] = fund
    out["re787"] = {"items": L.grid_items(L.PLAN_787)[0]}
    print("fundable renton", [(c["stress_ok"], round(c["stress_peak"], 2)) for c in fund["renton"]])
    print("787 items", [round(x, 2) for x in out["re787"]["items"]])
    json.dump(out, open(os.path.join(HERE, "thresholds.json"), "w"), indent=1, default=str)
    print("wrote thresholds.json")


if __name__ == "__main__":
    main()
