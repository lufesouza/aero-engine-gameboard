"""fps business case (run dash-2050-cons, the user's conservative-case market): launch a 10-year fps in 2030 (in service
2040) against Do Nothing, everyone else's 2030 orders as played (Airbus launches NGSA on the A320 Alt plan), nobody
moving after 2030. Adapted from ../../../dash-2050-sd/analysis/fps_business_case/make_case.py.

Two views of the same decision, both pre-tax, constant 2026 dollars, discounted at Boeing's WACC to 2026:
- Game view: what the game values. Incremental narrowbody operating profit as delivered (supply-and-demand layer), the
  development bill as one lump at entry into service (the dashboard's convention), the dashboard's debt penalty (a
  non-cash valuation haircut) and, at Renton, the new-site capex avoided, also at entry into service. Reconciles exactly
  with the game's ΔPV.
- Cash view: the same operating profit, the bill spent over the development years on finance.py's phasing curve, the
  Renton saving over the three years before entry into service (as finance.py books it), no debt penalty.

Writes case.json next to this file. Run from any folder: python3 make_case.py
"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402  (sets DASH_RUN=dash-2050-cons)
import model as M, rules as R, reports as RP, supply_demand as SD, finance as FN

P = M.af_params()
W = P["WACC_B"]
Y0 = 2026
df = lambda y: 1.0 / (1.0 + W) ** (y - Y0)
s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
LAUNCH = 2030


def build(bo, site="new_site", airbus=None, s_start=None, year=LAUNCH, recd=None):
    st, rc = (s_start or s0), (recd or rec)
    o = dict(rc["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    orders = {k: (o if k == "boeing" else rc["orders"][k]) for k in M.SIDES}
    if airbus:
        orders["airbus"] = dict(orders["airbus"]); orders["airbus"].update(airbus)
    orders = {k: R.validate(st, k, year, x)[0] for k, x in orders.items()}
    return R.adjudicate(st, year, orders)[0]


F10 = {"fps": "launch_10yr", "fps_engine_code": 7}


def series(sf, sh):
    vf, vh = M.value(sf, covert=True, series=True), M.value(sh, covert=True, series=True)
    # Do Nothing looked up by year: a later entry into service (the slip) runs the fps series past Do Nothing's, and a
    # year missing from Do Nothing's series is outside its window.
    dn = {r["year"]: r for r in vh["_af_series"]["years"]}
    assert set(dn) <= {r["year"] for r in vf["_af_series"]["years"]}, "Do Nothing series runs past the fps series"
    rows = []
    for rf in vf["_af_series"]["years"]:
        y = rf["year"]
        rh = dn.get(y)
        bf, bh = rf["boeing"], (rh["boeing"] if rh else None)
        inf, inh = bf["nb_in_window"], bool(bh and bh["nb_in_window"])
        op = ((bf["nb_profit"] - bf["sq_nb_profit"]) if inf else 0.0) - ((bh["nb_profit"] - bh["sq_nb_profit"]) if inh else 0.0)
        op_board = ((bf["board_nb_profit"] - bf["board_sq_nb_profit"]) if inf else 0.0) - ((bh["board_nb_profit"] - bh["board_sq_nb_profit"]) if inh else 0.0)
        rows.append({"year": y, "df": rf["df_b"], "in_window_fps": inf, "in_window_dn": inh,
                     "fps_units": rf["sd"]["dlv_fps"], "max_units_fps_case": rf["sd"]["dlv_max"], "boeing_units_fps_case": bf["nb_units"],
                     "boeing_units_dn": bh["nb_units"] if bh else None, "pref_fps_case": bf["nb_pref_share"], "pref_dn": bh["nb_pref_share"] if bh else None,
                     "new_demand": rf["sd"]["demand"], "fps_capacity": rf["sd"]["cap_fps"], "max_capacity_fps_case": rf["sd"]["cap_max"],
                     "revenue_fps_case": bf["nb_revenue"], "revenue_dn": bh["nb_revenue"] if bh else None,
                     "op_profit_inc": op, "op_profit_inc_dashboard": op_board})
    return vf, vh, rows


def npv(flows, rate=W):
    return sum(v / (1.0 + rate) ** (y - Y0) for y, v in flows.items())


def irr(flows):
    lo, hi = -0.5, 1.0
    f = lambda r: sum(v / (1.0 + r) ** (y - Y0) for y, v in flows.items())
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2


def payback(flows, discounted=False):
    cum, out = 0.0, None
    peak, peak_y = 0.0, None
    for y in sorted(flows):
        cum += flows[y] * (df(y) if discounted else 1.0)
        if cum < peak: peak, peak_y = cum, y
        if out is None and cum >= 0 and y > LAUNCH and any(flows[z] < 0 for z in flows if z <= y):
            out = y
    return out, peak, peak_y


def case(site):
    sf, sh = build(F10, site), build({}, "new_site")
    vf, vh, rows = series(sf, sh)
    bf, bh = vf["boeing"]["bridge"], vh["boeing"]["bridge"]
    inc_bridge = {k: bf.get(k, 0) - bh.get(k, 0) for k in bf}
    bill = M.af_bill("fps", "10yr")
    eis = sf["prog"]["fps"]["eis"]
    eis_inp, a_s, b_s, _ = M.af_inputs(sf)
    cell = M.eval_cell(eis_inp, a_s, b_s)
    tc = cell["b_tc_data"]
    pen_nom = tc["delta_pen_nom"]
    renton = -sum(x for s, y, item, x in SD.costs(sf) if s == "boeing")       # +3.0 when Renton (a saving)
    # finance.py spreads
    F = FN.inputs()
    pc = FN.programme_cash(sf, F)                                            # {year: {item: spend}} incl. any Renton credit
    spend = {y: sum(v for k, v in d.items() if "fps (" in k) for y, d in pc.items()}
    renton_cash = {y: -sum(v for k, v in d.items() if "Renton" in k) for y, d in pc.items()}
    years = [r["year"] for r in rows]
    op = {r["year"]: r["op_profit_inc"] for r in rows}
    game = {y: op[y] for y in years}
    game[eis] = game.get(eis, 0) - bill - pen_nom + renton
    cash = {y: op[y] - spend.get(y, 0.0) + renton_cash.get(y, 0.0) for y in sorted(set(years) | set(spend))}
    # checks against the game's ΔPV
    game_npv = npv(game)
    dpv = vf["boeing"]["pv_delta"] - vh["boeing"]["pv_delta"]
    assert abs(game_npv - dpv) < 1e-9, (site, game_npv, dpv)
    assert abs(npv({eis: -bill}) - inc_bridge["programme_investment"]) < 1e-9
    assert abs(npv({eis: -pen_nom}) - inc_bridge["debt_penalty"]) < 1e-9
    assert abs(npv(op) - (inc_bridge["nb_profit_vs_sq"] + inc_bridge["supply_demand"])) < 1e-9
    assert abs(sum(spend.values()) - bill) < 1e-9
    for r in rows:
        y = r["year"]
        r.update({"bill_game": -bill if y == eis else 0.0, "debt_penalty_game": -pen_nom if y == eis else 0.0,
                  "renton_game": renton if y == eis else 0.0, "net_game": game[y],
                  "bill_cash": -spend.get(y, 0.0), "renton_cash": renton_cash.get(y, 0.0), "net_cash": cash[y]})
    pb_c, peak_c, peak_cy = payback(cash)
    pbd_c, _, _ = payback(cash, True)
    pb_g, peak_g, peak_gy = payback(game)
    return {"site": site, "eis": eis, "rows": rows, "bridge": inc_bridge, "game_npv": game_npv, "cash_npv": npv(cash),
            "game_npv_2030": game_npv * (1 + W) ** (LAUNCH - Y0), "cash_npv_2030": npv(cash) * (1 + W) ** (LAUNCH - Y0),
            "op_profit_pv": npv(op), "op_profit_undiscounted": sum(op.values()),
            "op_profit_dashboard_pv": npv({r["year"]: r["op_profit_inc_dashboard"] for r in rows}),
            "bill": bill, "bill_pv_game": bill * df(eis), "bill_pv_cash": npv(spend), "spend": spend,
            "debt_penalty_nominal": pen_nom, "debt_penalty_pv": pen_nom * df(eis), "debt_inputs": {"D": P["v_debt_boeing"], "EV": P["v_ev_boeing"], "alpha": P["v_alpha"]},
            "renton_saving": renton, "renton_pv_game": renton * df(eis), "renton_pv_cash": npv(renton_cash),
            "irr_cash": irr(cash), "irr_game": irr(game), "payback_cash": pb_c, "payback_cash_discounted": pbd_c,
            "peak_funding_cash": peak_c, "peak_funding_cash_year": peak_cy, "payback_game": pb_g,
            "dpv_fps": vf["boeing"]["pv_delta"], "dpv_dn": vh["boeing"]["pv_delta"],
            "dashboard_alone_item": None, "engines": R.engine_fit(sf)["fps"]["fitted_if_no_change"],
            "engine_programmes": {k: v["launch"] for k, v in sf["prog"].items() if k in ("pw_solo", "pw_jv", "rr_solo", "rr_jv", "jv")}}


out = {"params": {"WACC_B": W, "price_fps_m": P["PRICE_fps"] * 1000, "margin_fps": P["v_margin_fps"], "price_737_m": P["PRICE_737"] * 1000,
                  "margin_737": P["v_margin_737"], "bill_10yr": P["v_capex_fps_10yr"], "bill_7yr": P["v_capex_fps_7yr"],
                  "post_eis_years": P["NPV_POST_EIS_YRS"], "debt_boeing": P["v_debt_boeing"], "ev_boeing": P["v_ev_boeing"], "alpha": P["v_alpha"],
                  "phasing_curve": FN.inputs()["phasing_curve"], "sd": {k: SD.inputs()["boeing"][k] for k in ("max_rate", "max_rate_after", "total_rate_cap", "max_tail_rate", "renton_saving_b", "renton_saving_range_b", "renton_rate", "everett_rate")},
                  "demand": {k: SD.inputs()["demand"][k] for k in ("class_share", "flex_share", "lapse_per_year", "fleet_growth_2025_44", "fleet_growth_2060", "firm_backlog")}},
       "cases": {}}
for site in ("renton", "new_site"):
    out["cases"][site] = case(site)
# dashboard alone (no supply-and-demand layer), same decision
M.SD_ON = False
sf, sh = build(F10, "new_site"), build({}, "new_site")
out["dashboard_alone_item"] = M.value(sf, covert=True)["boeing"]["pv_delta"] - M.value(sh, covert=True)["boeing"]["pv_delta"]
M.SD_ON = True

# ---- sensitivities (Renton base). The operating-profit line is the same in both views, so a change that only moves
# operating profit moves both views equally; bill and discount-rate changes are recomputed in each view.
base = out["cases"]["renton"]
rows = base["rows"]
fps_units_pv = sum(r["fps_units"] * r["df"] for r in rows if r["in_window_fps"])      # aircraft x df, in window
g, c = base["game_npv"], base["cash_npv"]
adj = {site: (out["cases"][site]["cash_npv"] - out["cases"][site]["game_npv"]) for site in out["cases"]}   # cash minus game, per site
sens = []
def add(name, low_label, low_g, low_c, high_label, high_g, high_c, note=""):
    sens.append({"factor": name, "low_label": low_label, "low": low_g, "low_cash": low_c,
                 "high_label": high_label, "high": high_g, "high_cash": high_c, "note": note})
dm = fps_units_pv * P["PRICE_fps"] * 0.05
add("fps margin (25.6%)", "20.6%", g - dm, c - dm, "30.6%", g + dm, c + dm, "computed from the base case: deliveries do not depend on margin")
dp = fps_units_pv * 0.005 * P["v_margin_fps"]
add("fps price ($55M)", "$50M", g - dp, c - dp, "$60M", g + dp, c + dp, "computed from the base case: deliveries do not depend on price")
def game_with_bill(k):
    nom = base["bill"] * k
    pv_b = nom * df(base["eis"])
    pen_pv = M.true_cost(nom, pv_b, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"]) - pv_b
    return g + base["bill_pv_game"] + base["debt_penalty_pv"] - pv_b - pen_pv
add("Development bill ($60.3B)", "+20% ($72.4B)", game_with_bill(1.2), c - 0.2 * base["bill_pv_cash"],
    "−20% ($48.3B)", game_with_bill(0.8), c + 0.2 * base["bill_pv_cash"], "game view recomputes the debt penalty")
fg = {r["year"]: r["net_game"] for r in rows}; fc = {r["year"]: r["net_cash"] for r in rows}
for y, v in base["spend"].items():
    fc.setdefault(y, 0.0)
add("Discount rate (10.5%)", "12%", npv(fg, 0.12), npv(fc, 0.12), "8%", npv(fg, 0.08), npv(fc, 0.08), "flows rediscounted")
def item_at(kw, site):
    with L.patched(**kw):
        return L.played_item(F10, site)
for kw, name, lab in (({"ramp": L.compressed(3)}, "fps ramp (NGSA Rev. B curve)", "three times as fast"),
                      ({"demand_k": 1.2}, "Demand (your conservative curve)", "20% more"),
                      ({"growth_k": 1.5}, "Fleet growth in your curve", "50% more growth")):
    it = item_at(kw, "renton")
    add(name, "as assumed", g, c, lab, it, it + adj["renton"], "at Renton; game run")
    other = item_at(kw, "new_site")
    sens[-1]["best_site"] = {"site": "Renton" if it >= other else "new sites", "game": max(it, other)}
last = [r for r in rows if r["in_window_fps"]][-1]
tv = sum(last["op_profit_inc"] * df(y) for y in range(last["year"] + 1, last["year"] + 11))
# rows after the fps window already in the value (Do Nothing counted a year longer) are replaced, not added to
tv -= sum(r["op_profit_inc"] * r["df"] for r in rows if last["year"] < r["year"] <= last["year"] + 10)
add("Horizon (20 years from entry into service)", "as booked", g, c, "+10 years at the 2059 profit", g + tv, c + tv, "outside the game's convention")
out["sensitivities"] = sens
out["base_for_sensitivities"] = {"site": "renton", "game_npv": g, "cash_npv": c}
out["fps_units_pv"] = fps_units_pv

# ---- risks shown separately
risks = []
# 3-year slip: in service 2043 instead of 2040, same bill. Game view as the model books it (bill moves to 2043, nothing
# charged for the slip); cash view with the bill spent over 2030-2042 on the stretched phasing curve.
sf = copy.deepcopy(build(F10, "renton")); sf["prog"]["fps"]["eis"] = 2043
sh = build({}, "new_site")
vf, vh, srows = series(sf, sh)
slip_game = vf["boeing"]["pv_delta"] - vh["boeing"]["pv_delta"]
Fi = FN.inputs()
pc = FN.programme_cash(sf, Fi)
spend = {y: sum(v for k, v in d.items() if "fps (" in k) for y, d in pc.items()}
rcash = {y: -sum(v for k, v in d.items() if "Renton" in k) for y, d in pc.items()}
op = {r["year"]: r["op_profit_inc"] for r in srows}
bfs, bhs = vf["boeing"]["bridge"], vh["boeing"]["bridge"]
assert abs(npv(op) - ((bfs["nb_profit_vs_sq"] + bfs.get("supply_demand", 0)) - (bhs["nb_profit_vs_sq"] + bhs.get("supply_demand", 0)))) < 1e-9
slip_cash = npv(op) - npv(spend) + npv(rcash)
risks.append({"risk": "3-year slip (in service 2043), same bill", "game": slip_game, "cash": slip_cash,
              "note": "the game books the bill at entry into service and charges nothing for a slip, so its value rises; in cash the bill is spent over 13 years and profit comes later"})
sf = build(F10, "renton", airbus={"rea350": "launch"}); sh = build({}, "new_site", airbus={"rea350": "launch"})
rea = M.value(sf, covert=True)["boeing"]["pv_delta"] - M.value(sh, covert=True)["boeing"]["pv_delta"]
risks.append({"risk": "Airbus also re-engines the A350 in 2030", "game": rea, "cash": rea + adj["renton"],
              "note": "a widebody move: it changes Boeing's widebody value in both cases equally, not the fps decision"})
out["risks"] = risks
json.dump(out, open(os.path.join(HERE, "case.json"), "w"), indent=1)
for site, c in out["cases"].items():
    print(site, "game NPV %.3f (=ΔPV fps %.3f - DN %.3f)  cash NPV %.3f  op PV %.3f  bill PV game %.3f cash %.3f  pen PV %.3f  renton PV game %.3f cash %.3f" % (
        c["game_npv"], c["dpv_fps"], c["dpv_dn"], c["cash_npv"], c["op_profit_pv"], c["bill_pv_game"], c["bill_pv_cash"], c["debt_penalty_pv"], c["renton_pv_game"], c["renton_pv_cash"]))
    print("    IRR cash %s game %s  payback cash %s (disc %s)  peak funding %.2f in %s  NPV@2030 game %.2f cash %.2f  op undiscounted %.1f" % (
        c["irr_cash"] and round(c["irr_cash"] * 100, 2), c["irr_game"] and round(c["irr_game"] * 100, 2), c["payback_cash"], c["payback_cash_discounted"],
        c["peak_funding_cash"], c["peak_funding_cash_year"], c["game_npv_2030"], c["cash_npv_2030"], c["op_profit_undiscounted"]))
print("dashboard alone", round(out["dashboard_alone_item"], 3))
for x in sens:
    print("%-45s %-24s %+.2f (cash %+.2f) | %-28s %+.2f (cash %+.2f) %s" % (x["factor"], x["low_label"], x["low"], x["low_cash"], x["high_label"], x["high"], x["high_cash"], x["note"]))
for x in out["risks"]:
    print("RISK", x["risk"], round(x["game"], 2), round(x["cash"], 2))
