"""fps in service in 2039, 2041 or 2044 under the demand scenarios of the user's page (chart 4.1), run dash-2050-cons.

Demand: the page's chart 4.1 (page_demand.json, make_page_demand.py): replacement of today's fleet plus as much again for
growth, with every aircraft retiring N = 0..4 years later than chapter 1 sets out. The page draws its demand from 2038
("before then half and half understates it"), so each scenario curve is the game's own conservative curve to 2037 and the
page's from 2038 (curves/*.json, in the game's curve format; the game applies its 737/A320 class share, 0.9483, as it does
to its own curve). Everything else is the game as played: the firm orders netted, Boeing's preference falling 1 point a
year while NGSA flies alone, the slack floor, Airbus's 1% capacity response, the game's supply (supply_demand.py).

The fps: the 10-year plan (bill $60.32B, booked at entry into service as the dashboard books it; the 10-year capture
speed), with its entry into service moved to 2039, 2041 or 2044 (launch 2030, 2031, 2034 for the cash view). Do Nothing
is unchanged. Each plan is valued exactly as Boeing's 2030 brief values it (lib.grid_items: six rival columns) and held to
Boeing's three 2030 tests (lib.tests). For every scenario and date: the item at both sites, and what would make it pass:
the fps margin, price or bill alone (exact: linear in each column's fps deliveries, the bill with its debt penalty), the
ramp-up speed and the preference uplift alone (bisection on the brief's own valuation), and launch packages (a partner
paying part of the bill, a faster ramp) with the margin they still need. Sensitivities: the page's demand tail after
2055 replaced by the game's curve; Tianjin building 20 a month on top of Airbus's plan; the page's own Boeing supply.
Writes demand_scenarios.json next to this file.

  python3 demand_scenarios.py
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M, SD = L.M, L.SD
P = M.af_params()
PAGE = json.load(open(os.path.join(HERE, "page_demand.json")))
GAME = json.load(open(os.path.join(L.DASHGAME, "demand_conservative.json")))
EIS = (2039, 2041, 2044)
NS = ("0", "1", "2", "3", "4")
PLANS = {"renton": L.PLAN_REN, "new_site": L.PLAN_NEW}
BILL0, M0, PRICE0 = P["v_capex_fps_10yr"], P["v_margin_fps"], P["PRICE_fps"] * 1000.0
FROM = PAGE["drawn_from"]


# ─────────────────────────────── demand curves ───────────────────────────────
def write_curve(name, n, tail_from=None):
    """Game curve before 2038, the page's scenario n from 2038 (the game's again from tail_from, if given); returns the
    path supply_demand reads (relative to dashgame)."""
    game = {y: (r, g) for y, r, g in zip(GAME["years"], GAME["replacements"], GAME["growth"])}
    gl = max(game)
    s = PAGE["retire_later"][n]
    page = {y: (o + w, o + w) for y, o, w in zip(PAGE["years"], s["old"], s["new"])}
    years, rep, gro = [], [], []
    for y in PAGE["years"]:
        if y < FROM or (tail_from and y >= tail_from):
            r, g = game[min(y, gl)]
        else:
            r, g = page[y]
        years.append(y)
        rep.append(round(r, 4))
        gro.append(round(g, 4))
    os.makedirs(os.path.join(HERE, "curves"), exist_ok=True)
    path = os.path.join(HERE, "curves", name + ".json")
    about = ("the user's page, chart 4.1, every aircraft retiring %s years later: replacement (old + new) and growth (as much "
             "again) from %d%s; the game's conservative curve (demand_conservative.json) before %d%s. Whole single-aisle "
             "market, before the game's class share." % (n, FROM, (" to %d" % (tail_from - 1)) if tail_from else "", FROM,
                                                        (" and from %d" % tail_from) if tail_from else ""))
    with open(path, "w") as f:
        json.dump({"about": about, "years": years, "replacements": rep, "growth": gro}, f, separators=(",", ":"))
    return os.path.relpath(path, L.DASHGAME)


CURVE = {n: write_curve("page_N%s" % n, n) for n in NS}
CURVE_TAIL = {n: write_curve("page_N%s_tail2056" % n, n, tail_from=2056) for n in NS}


def demand_kw(n, tail=False):
    return {"options": {"demand_curve": (CURVE_TAIL if tail else CURVE)[n]}}


# ─────────────────────────────── supply patches ───────────────────────────────
TJ = PAGE["supply"]["tianjin"]


def tianjin(f):
    def g(state, year):
        a3, ng = f(state, year)
        on = TJ["years"][0] <= year <= TJ["years"][1]
        return a3 + (12.0 * TJ["rate"] if on else 0.0), ng
    return g


def page_boeing(state, year):
    """Boeing's capacity as the page draws it: the 737 on its steps (42/47/52 a month) until the fps enters service
    (mid-year), then in a straight line to none at the end of 2050; the fps up to 80 a month seven years later."""
    b, fp = PAGE["supply"]["b737"], PAGE["supply"]["fps"]
    st, end = b["steps"], b["end"]
    fps = SD._live(state, "fps")
    eis = fps["eis"] + 0.5 if fps else None

    def step(u):
        r = st[0][1]
        for y, v in st:
            if u >= y:
                r = v
        return r
    mx = f = 0.0
    for m in range(12):
        t = year + (m + 0.5) / 12
        if eis is None or t < eis:
            mx += step(t)
        else:
            mx += step(eis) * max(0.0, (end - t) / (end - eis))
            f += fp["top"] * min(1.0, (t - eis) / fp["years"])
    return mx, f


class supply:
    """Context manager for the supply sensitivities (on top of lib.patched)."""
    def __init__(self, tj=False, page=False):
        self.tj, self.page = tj, page

    def __enter__(self):
        self.saved = (SD.airbus_capacity, SD.boeing_capacity)
        if self.tj:
            SD.airbus_capacity = tianjin(SD.airbus_capacity)
        if self.page:
            SD.boeing_capacity = page_boeing

    def __exit__(self, *a):
        SD.airbus_capacity, SD.boeing_capacity = self.saved


# ─────────────────────────────── valuation ───────────────────────────────
def at_eis(eis):
    """The fps (if live) enters service in `eis` (launch 2030, or eis - 10 if later: the cash view only)."""
    def post(st):
        f = st["prog"].get("fps")
        if f and f.get("cancel") is None:
            f["eis"] = eis
            f["launch"] = max(f["launch"], eis - 10)
        return st
    return post


def states(plan, eis):
    return L.grid_states(plan, at_eis(eis))


def evaluate(eis, kw=None, tj=False, page=False):
    out = {}
    with L.patched(**(kw or {})), supply(tj, page):
        dn = L.grid_row(L.PLAN_DN)
        for site, plan in PLANS.items():
            row = L.grid_row(plan, at_eis(eis))
            items = [a - b for a, b in zip(row, dn)]
            out[site] = {"items": items, "plan_row": row, "dn_row": dn, **L.tests(items), "margin": L.margin(items)}
    out["best"] = max(PLANS, key=lambda s: out[s]["margin"])
    return out


def pen_pv(bill, df):
    pv = bill * df
    return M.true_cost(bill, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"]) - pv


def terms(plan, eis):
    """Per column: $B of value per point of fps margin (U, per 1.0 of margin) and per $M of fps price (V), the
    discount factor at entry into service, from each column state's own series (call inside the patches)."""
    out = []
    for st, cv in states(plan, eis):
        v = M.value(st, covert=cv, series=True)
        U = V = Q = 0.0
        for r in v["_af_series"]["years"]:
            x = r["boeing"]
            if x["nb_in_window"]:
                n = x.get("nb_units_new", 0.0)
                if n:
                    assert abs(x["nb_price"] - PRICE0) < 1e-9 and abs(x["nb_margin"] - M0) < 1e-12, (r["year"], x["nb_price"], x["nb_margin"])
                Q += n * r["df_b"]
                U += n * r["df_b"] * x["nb_price"] / 1000.0
                V += n * r["df_b"] * x["nb_margin"] / 1000.0
        e = st["prog"]["fps"]["eis"]
        assert e == eis
        df = 1.0 / (1 + P["WACC_B"]) ** (e - 2026)
        br = v["boeing"]["bridge"]
        assert abs(br["programme_investment"] + BILL0 * df) < 1e-6, (br["programme_investment"], BILL0 * df)
        assert abs(br["debt_penalty"] + pen_pv(BILL0, df)) < 1e-6
        out.append({"U": U, "V": V, "Q": Q, "df": df})
    return out


def shifted(base, tm, margin=M0, price=PRICE0, bill=BILL0):
    """The six items with the fps margin, price and bill changed (exact: the dashboard's unit profit is price x margin
    on every fps delivered in the window; the bill is a lump at entry into service with its debt penalty)."""
    out = []
    for b, t in zip(base, tm):
        dv = t["Q"] * (price * margin - PRICE0 * M0) / 1000.0     # discounted fps deliveries x unit profit change ($B)
        dv -= (bill - BILL0) * t["df"] + (pen_pv(bill, t["df"]) - pen_pv(BILL0, t["df"]))
        out.append(b + dv)
    return out


def analytic(eis, ev, kw=None, tj=False, page=False, ramp_k=None):
    """Margin, price and bill thresholds at both sites (each alone), plus the margin needed when a partner pays part of
    the bill. `ev`: evaluate()'s result for the same patches (ramp_k: the ramp speed, already in kw)."""
    res = {}
    with L.patched(**(kw or {})), supply(tj, page):
        for site, plan in PLANS.items():
            base, tm = ev[site]["items"], terms(plan, eis)
            fm = lambda m: L.margin(shifted(base, tm, margin=m))
            fp = lambda p: L.margin(shifted(base, tm, price=p))
            fb = lambda x: L.margin(shifted(base, tm, bill=x))
            m = L.bisect(fm, M0, 1.0, 0.0, tol=1e-7)
            p = L.bisect(fp, PRICE0, 400.0, 0.0, tol=1e-5)
            bl = L.bisect(fb, BILL0, 0.0, 0.0, tol=1e-5)
            share = {}
            for paid in (0.25, 0.5):       # a partner pays this share of the bill
                x = BILL0 * (1 - paid)
                share[str(paid)] = L.bisect(lambda mm: L.margin(shifted(base, tm, margin=mm, bill=x)), 0.0, 1.0, 0.0, tol=1e-7) \
                    if L.margin(shifted(base, tm, bill=x)) < 0 else "passes"
            res[site] = {"margin": m, "price": p, "bill": bl, "at_zero_bill": L.margin(shifted(base, tm, bill=1e-9)),
                         "margin_with_partner": share,
                         "per_point": [t["U"] / 100.0 for t in tm],      # $B per margin point, each column
                         "per_10m_price": [t["V"] * 10.0 for t in tm],
                         "df": tm[0]["df"]}
    return res


def best_of(res, key, better):
    vals = {s: res[s][key] for s in PLANS if isinstance(res[s][key], (int, float))}
    if not vals:
        return None, None
    s = better(vals, key=vals.get)
    return vals[s], s


def lever(eis, mk, lo, hi, tol, kw=None):
    """Value of a lever (ramp speed, preference points) at which the better site passes, by bisection."""
    def f(x):
        k = dict(kw or {})
        k.update(mk(x))
        e = evaluate(eis, k)
        return max(e[s]["margin"] for s in PLANS)
    return L.bisect(f, lo, hi, 0.0, tol=tol)


def context(eis, kw=None, tj=False, page=False):
    """Deliveries and shares behind the expected columns (S2: NGSA; S5: NGSA + A350 Re-engine; the fps at Renton)."""
    out = {}
    with L.patched(**(kw or {})), supply(tj, page):
        for lab, (st, cv) in (("fps", states(L.PLAN_REN, eis)[1]), ("do_nothing", L.grid_states(L.PLAN_DN)[1])):
            v = M.value(st, covert=cv, series=True)
            ys = {r["year"]: r for r in v["_af_series"]["years"]}
            b = {y: ys[y]["boeing"] for y in ys}
            sd = {y: ys[y].get("sd", {}) for y in ys}
            win = [y for y in ys if b[y]["nb_in_window"]]
            out[lab] = {
                "fps_units_window": sum(b[y].get("nb_units_new", 0.0) for y in win),
                "fps_units_first10": sum(b[y].get("nb_units_new", 0.0) for y in win if eis <= y < eis + 10),
                "boeing_units_2038_60": sum(b[y]["nb_units"] for y in ys if 2038 <= y <= 2060),
                "share": {y: b[y]["nb_share"] for y in (2040, 2045, 2050, 2055, 2060) if y in b},
                "pref": {y: b[y].get("nb_pref_share") for y in (2040, 2045, 2050, 2055, 2060) if y in b},
                "lost_2038_60": sum(sd[y].get("lost", 0.0) for y in ys if 2038 <= y <= 2060),
                "demand_2038_60": sum(sd[y].get("demand_gross", 0.0) for y in ys if 2038 <= y <= 2060),
                "window_end": max(win)}
    return out


def fundable(eis, kw=None):
    with L.patched(**(kw or {})):
        cols = []
        for st, cv in states(L.PLAN_REN, eis):
            v = M.value(st, covert=cv, series=True)
            m = L.B.plan_metrics("boeing", st, v, cv)
            cols.append({"stress_ok": m["stress_ok"], "stress_peak": m["stress_peak"]})
    return cols


class board:
    """Re-solve the dashboard with some of its own inputs changed (af_m_fps in %, af_price_fps in $M, af_cx_fps10 in
    $B): the check that a threshold found by the linear shortcut really is the pass line."""
    def __init__(self, **over):
        self.over = over

    def __enter__(self):
        import functools
        self.saved = M.af_board
        over = self.over

        @functools.lru_cache(maxsize=None)
        def af_board(eis):
            o = {"af_fps_eis": eis[0], "af_ngsa_eis": eis[1], "af_787_eis": eis[2], "af_a350_eis": eis[3]}
            o.update(over)
            return M.H.af(o, M.AF_PATCH)[3]
        M.af_board = af_board

    def __exit__(self, *a):
        M.af_board = self.saved


def confirm(eis, kw, site, **over):
    """Boeing's test margin for `site` with the board re-solved at `over` (0 at a pass line)."""
    with board(**over):
        return evaluate(eis, kw)[site]["margin"]


LINES = ("nb_profit_vs_sq", "supply_demand", "programme_investment", "debt_penalty", "supply_plan", "rate_hike",
         "wb_profit_vs_sq", "delay_tactics_spend", "write_offs", "two_front_strain", "naked_fine")


def bridge(eis, kw=None, site="renton"):
    """The item in the expected columns (S2 and S5 at even odds), line by line: the plan's bridge minus Do Nothing's."""
    out = {k: 0.0 for k in LINES}
    with L.patched(**(kw or {})):
        plan = states(PLANS[site], eis)
        dn = L.grid_states(L.PLAN_DN)
        for i, w in L.EXPECTED.items():
            bp = M.value(plan[i][0], covert=plan[i][1], series=False)["boeing"]["bridge"]
            bd = M.value(dn[i][0], covert=dn[i][1], series=False)["boeing"]["bridge"]
            assert set(bp) <= set(LINES) and set(bd) <= set(LINES), (set(bp) | set(bd)) - set(LINES)
            for k in LINES:
                out[k] += w * (bp.get(k, 0.0) - bd.get(k, 0.0))
    return out


def ngsa_at(eis):
    def post(st):
        ng = st["prog"].get("ngsa")
        if ng and ng.get("cancel") is None:
            ng["eis"] = eis
        return st
    return post


def evaluate_post(eis, kw, post_all):
    """evaluate() with an extra change to every column state, Do Nothing's included (a world, not a Boeing lever)."""
    out = {}
    fps_eis = at_eis(eis)
    with L.patched(**(kw or {})):
        dn = L.grid_row(L.PLAN_DN, post_all)
        for site, plan in PLANS.items():
            row = L.grid_row(plan, lambda st: post_all(fps_eis(st)))
            items = [a - b for a, b in zip(row, dn)]
            out[site] = {"items": items, **L.tests(items), "margin": L.margin(items)}
    out["best"] = max(PLANS, key=lambda s: out[s]["margin"])
    return out


def ramp_profile(k, eis):
    """fps capacity a year (Renton plan, column S2) on the game's ramp run k times as fast: aircraft by year and the
    years after entry into service to 50 and to 90 a month."""
    st = states(L.PLAN_REN, eis)[1][0]
    with L.patched(ramp=L.compressed(k)):
        caps = {y: SD.boeing_capacity(st, y)[1] for y in range(eis, eis + 16)}
    first = lambda r: next((y - eis for y in sorted(caps) if caps[y] >= 12.0 * r - 1e-6), None)
    return {"k": k, "by_year": caps, "to_50": first(50), "to_90": first(90), "first5": sum(caps[y] for y in range(eis, eis + 5))}


def round_all(x, d=4):
    if isinstance(x, float):
        return round(x, d)
    if isinstance(x, dict):
        return {k: round_all(v, d) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [round_all(v, d) for v in x]
    return x


def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    out = {"tests": {"business_case": L.BUSINESS_CASE, "downside": L.DOWNSIDE, "buffer": L.BUFFER,
                     "expected_weights": {L.SCEN_LABELS[i]: w for i, w in L.EXPECTED.items()}},
           "columns": L.SCEN_LABELS, "eis": EIS, "scenarios": NS, "base": {"bill": BILL0, "margin": M0, "price": PRICE0},
           "curves": {n: CURVE[n] for n in NS}}
    # the game's own curve, for the check against the stored brief (fps 10-yr in 2040 at Renton: -4.80 expected)
    ref = evaluate(2040)
    stored = json.load(open(os.path.join(HERE, "..", "fps_choice", "thresholds.json")))["base"]
    for s in PLANS:
        assert max(abs(a - b) for a, b in zip(ref[s]["items"], stored[s]["items"])) < 1e-9, s
    out["game_curve"] = {str(e): evaluate(e) for e in (2039, 2040, 2041, 2044)}
    out["game_curve_analytic"] = {str(e): analytic(e, out["game_curve"][str(e)]) for e in EIS}
    print("game curve: fps 2040 reproduces the stored brief; expected (Renton) by EIS",
          {e: round(out["game_curve"][e]["renton"]["expected"], 2) for e in out["game_curve"]}, "%.0fs" % (time.time() - t0))
    # demand of each scenario as the game sees it (class share applied)
    dem = {}
    for n in NS:
        with L.patched(**demand_kw(n)):
            dem[n] = {y: SD.demand(y) for y in range(2026, 2071)}
    with L.patched():
        dem["game"] = {y: SD.demand(y) for y in range(2026, 2071)}
    out["demand"] = dem
    cases = {}
    for n in NS:
        for e in EIS:
            kw = demand_kw(n)
            ev = evaluate(e, kw)
            an = analytic(e, ev, kw)
            rec = {"eval": ev, "analytic": an, "context": context(e, kw)}
            rec["margin_needed"], rec["margin_site"] = best_of(an, "margin", min)
            rec["price_needed"], rec["price_site"] = best_of(an, "price", min)
            rec["bill_needed"], rec["bill_site"] = best_of(an, "bill", max)
            if not quick:
                rec["ramp_needed"] = lever(e, lambda k: {"ramp": L.compressed(k)}, 1.0, 12.0, 1e-3, kw)
                inst = evaluate(e, dict(kw, ramp=L.instant))
                rec["ramp_profiles"] = {"game": ramp_profile(1.0, e), "x1.5": ramp_profile(1.5, e)}
                if rec["ramp_needed"]:
                    rec["ramp_profiles"]["needed"] = ramp_profile(rec["ramp_needed"], e)
                rec["ramp_instant"] = {"best": inst["best"], "expected": inst[inst["best"]]["expected"], "margin": inst[inst["best"]]["margin"]}
                rec["pref_needed"] = lever(e, lambda x: {"fps_pref_pp": x}, 0.0, 60.0, 1e-3, kw)
                rec["pref_sweep"] = {}
                for x in (10.0, 20.0, 60.0):
                    w = evaluate(e, dict(kw, fps_pref_pp=x))
                    rec["pref_sweep"][str(x)] = {"best": w["best"], "expected": w[w["best"]]["expected"], "margin": w[w["best"]]["margin"]}
                # package: customers' preference +10 points once the fps flies; the margin still needed
                kp = dict(kw, fps_pref_pp=10.0)
                evp = evaluate(e, kp)
                anp = analytic(e, evp, kp)
                rec["pref10_margin"], rec["pref10_site"] = best_of(anp, "margin", min)
                # packages: a faster ramp (1.5x: rate 50 in under 3 years) and the margin still needed
                k15 = dict(kw, ramp=L.compressed(1.5))
                ev15 = evaluate(e, k15)
                an15 = analytic(e, ev15, k15)
                rec["ramp15"] = {"eval": {s: {kk: ev15[s][kk] for kk in ("items", "expected", "worst", "risk_case", "margin", "passes")}
                                          for s in PLANS}, "analytic": an15}
                rec["fundable"] = fundable(e, kw)
                # packages: a partner pays a quarter of the bill and the ramp is 1.5x; the margin still needed
                part = {}
                for site in PLANS:
                    base, x = ev15[site]["items"], BILL0 * 0.75
                    with L.patched(**k15):
                        tm = terms(PLANS[site], e)
                    f = lambda mm: L.margin(shifted(base, tm, margin=mm, bill=x))
                    part[site] = "passes" if f(M0) >= 0 else L.bisect(f, M0, 1.0, 0.0, tol=1e-7)
                rec["package"] = part
            rec["bridge"] = bridge(e, kw, ev["best"])
            assert abs(sum(rec["bridge"].values()) - ev[ev["best"]]["expected"]) < 1e-9
            # the pass lines re-checked on a re-solved dashboard (margin, price, bill each alone)
            s_ = ev["best"]
            a_ = an[s_]
            rec["confirm"] = {"margin": confirm(e, kw, s_, af_m_fps=100.0 * a_["margin"]),
                              "price": confirm(e, kw, s_, af_price_fps=a_["price"]),
                              "bill": confirm(e, kw, s_, af_cx_fps10=a_["bill"])}
            assert all(abs(v) < 1e-5 for v in rec["confirm"].values()), rec["confirm"]
            # worlds (not Boeing's levers): Boeing loses 3 points a year while NGSA flies alone; NGSA 3 years late
            rec["worlds"] = {}
            for lab, kk, post in (("erosion3", dict(kw, options=dict(kw["options"], boeing_pp_after_ngsa=3.0)), None),
                                  ("ngsa2040", kw, ngsa_at(2040))):
                w = evaluate_post(e, kk, post) if post else evaluate(e, kk)
                rec["worlds"][lab] = {"best": w["best"], **{k: w[w["best"]][k] for k in ("items", "expected", "worst", "risk_case", "margin", "passes")}}
            cases["N%s/%d" % (n, e)] = rec
            b = ev[ev["best"]]
            print("N=%s fps %d: best %-8s exp %+6.2f worst %+6.2f risk %+6.2f | margin %.1f%% price $%.0fM bill $%sB ramp %s pref %s  %.0fs" % (
                n, e, ev["best"], b["expected"], b["worst"], b["risk_case"], 100 * (rec["margin_needed"] or 0), rec["price_needed"] or 0,
                None if rec["bill_needed"] is None else round(rec["bill_needed"], 1), rec.get("ramp_needed") and round(rec["ramp_needed"], 2),
                rec.get("pref_needed") and round(rec["pref_needed"], 1), time.time() - t0))
    out["cases"] = cases
    # sensitivities (the item and the margin needed; both sites)
    sens = {}
    for lab, kwf, tj, page in (("tail", lambda n: demand_kw(n, tail=True), False, False),
                               ("tianjin", lambda n: demand_kw(n), True, False),
                               ("page_supply", lambda n: demand_kw(n), True, True)):
        for n in NS:
            for e in EIS:
                ev = evaluate(e, kwf(n), tj, page)
                an = analytic(e, ev, kwf(n), tj, page)
                mn, ms = best_of(an, "margin", min)
                bn, bs = best_of(an, "bill", max)
                sens["%s/N%s/%d" % (lab, n, e)] = {"eval": ev, "margin_needed": mn, "margin_site": ms, "bill_needed": bn,
                                                   "bill_site": bs, "analytic": an}
                b = ev[ev["best"]]
                print("%-11s N=%s fps %d: best %-8s exp %+6.2f worst %+6.2f risk %+6.2f margin %.1f%%" % (
                    lab, n, e, ev["best"], b["expected"], b["worst"], b["risk_case"], 100 * (mn or 0)))
    out["sensitivities"] = sens
    with L.patched(), supply(page=True):
        out["page_supply_check"] = {str(e): {y: page_boeing({"prog": {"fps": {"eis": e}}}, y) for y in range(2036, 2053)} for e in EIS}
    json.dump(round_all(out), open(os.path.join(HERE, "demand_scenarios.json"), "w"), indent=1, default=str)
    print("wrote demand_scenarios.json  %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
