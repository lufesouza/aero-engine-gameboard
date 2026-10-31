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
paying part of the bill, a faster ramp) with the margin they still need. A partner's money is counted first as free, then
with the largest share of the fps's profit it could take back before the pass is lost. The price lever is reported both
with the margin % held (cost per aircraft rises with price) and with today's cost per aircraft held. For 2039 (a 9-year
programme from 2030 or a 2029 launch) the margin needed is also given at a 9-year bill (between the 7- and 10-year
bills) and at the 7-year bill (exactly the game's own 7-year fps launched in 2032; checked). The margin by programme length is also
given with the bill spent over the development years on the game's cash phasing curve instead of booked at entry into service. Counting convention: Boeing's brief counts Do Nothing to 2060 (its fps reference date,
2041, + 19) whatever the fps date; the same-window variant counts Do Nothing over the same years as each fps.
Sensitivities: the page's demand tail after 2055 replaced by the game's curve; the page's own demand from 2026 (no
splice); Tianjin building 20 a month on top of Airbus's plan; the page's own Boeing supply. Every pass line (each lever
alone, the packages, the 9-year bill, the same-window and sensitivity margins) is re-checked on a re-solved dashboard.
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
import finance as FIN  # noqa: E402

M, SD = L.M, L.SD
P = M.af_params()
PAGE = json.load(open(os.path.join(HERE, "page_demand.json")))
GAME = json.load(open(os.path.join(L.DASHGAME, "demand_conservative.json")))
EIS = (2039, 2041, 2044)
NS = ("0", "1", "2", "3", "4")
PLANS = {"renton": L.PLAN_REN, "new_site": L.PLAN_NEW}
BILL0, M0, PRICE0 = P["v_capex_fps_10yr"], P["v_margin_fps"], P["PRICE_fps"] * 1000.0
FROM = PAGE["drawn_from"]
COST0 = PRICE0 * (1.0 - M0)              # $M cost per fps today (the dashboard's price less its margin)
BILL7 = P["v_capex_fps_7yr"]
BILL9 = BILL0 + (BILL7 - BILL0) * (10 - 9) / (10 - 7)      # a 9-year programme: between the 7- and 10-year bills
BILLS = {10: BILL0, 9: BILL9, 8: BILL0 + (BILL7 - BILL0) * (10 - 8) / (10 - 7), 7: BILL7}   # by programme length (8, 9: interpolated)


# ─────────────────────────────── demand curves ───────────────────────────────
def write_curve(name, n, tail_from=None, page_from=FROM):
    """Game curve before page_from (2038), the page's scenario n from then on (the game's again from tail_from, if
    given); returns the path supply_demand reads (relative to dashgame)."""
    game = {y: (r, g) for y, r, g in zip(GAME["years"], GAME["replacements"], GAME["growth"])}
    gl = max(game)
    s = PAGE["retire_later"][n]
    page = {y: (o + w, o + w) for y, o, w in zip(PAGE["years"], s["old"], s["new"])}
    years, rep, gro = [], [], []
    for y in PAGE["years"]:
        if y < page_from or (tail_from and y >= tail_from):
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
             "market, before the game's class share." % (n, page_from, (" to %d" % (tail_from - 1)) if tail_from else "", page_from,
                                                        (" and from %d" % tail_from) if tail_from else ""))
    if page_from <= PAGE["years"][0]:
        about = ("the user's page, chart 4.1, every aircraft retiring %s years later: replacement (old + new) and growth (as "
                 "much again) in every year (no splice). Whole single-aisle market, before the game's class share." % n)
    with open(path, "w") as f:
        json.dump({"about": about, "years": years, "replacements": rep, "growth": gro}, f, separators=(",", ":"))
    return os.path.relpath(path, L.DASHGAME)


CURVE = {n: write_curve("page_N%s" % n, n) for n in NS}
CURVE_TAIL = {n: write_curve("page_N%s_tail2056" % n, n, tail_from=2056) for n in NS}
CURVE_ALL = {n: write_curve("page_N%s_from2026" % n, n, page_from=PAGE["years"][0]) for n in NS}


def demand_kw(n, tail=False, whole=False):
    return {"options": {"demand_curve": (CURVE_ALL if whole else CURVE_TAIL if tail else CURVE)[n]}}


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


class dn_window:
    """Do Nothing counted over the same years as an fps entering service in `eis`: Do Nothing's fps reference date (the
    board's default fps EIS, which sets its counting window) moved to `eis`. Only the window changes: Boeing's Do Nothing
    profit year by year is the same (checked in main)."""
    def __init__(self, eis):
        self.eis = eis

    def __enter__(self):
        self.saved = M.DEFAULT_EIS["fps"]
        if self.eis is not None:
            M.DEFAULT_EIS["fps"] = self.eis

    def __exit__(self, *a):
        M.DEFAULT_EIS["fps"] = self.saved


def evaluate(eis, kw=None, tj=False, page=False, sw=False):
    """Both sites' items in the six columns, Boeing's tests and the better site. sw: Do Nothing on the same window."""
    out = {}
    with L.patched(**(kw or {})), supply(tj, page):
        with dn_window(eis if sw else None):
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


def bill_cost(bill, eis, launch=None):
    """Present value at 2026 of a programme bill plus the dashboard's debt penalty on it. launch None: booked as one lump
    at entry into service, as Boeing's brief books it; otherwise spent over launch..eis-1 on the game's cash phasing curve
    (finance.programme_cash), the debt penalty kept (the dashboard's formula on that present value)."""
    w = P["WACC_B"]
    if launch is None:
        df = 1.0 / (1 + w) ** (eis - 2026)
        return bill * df + pen_pv(bill, df)
    shares = FIN.stretch(FIN.inputs()["phasing_curve"], eis - launch)
    pv = sum(bill * sh / (1 + w) ** (launch + k - 2026) for k, sh in enumerate(shares))
    return M.true_cost(bill, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"])


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
            at_bill = lambda x: L.bisect(lambda mm: L.margin(shifted(base, tm, margin=mm, bill=x)), 0.0, 1.0, 0.0, tol=1e-7)
            # the margin needed when the bill costs `extra` $B more (PV) than the 10-year lump at entry into service
            at_cost = lambda extra: L.bisect(lambda mm: L.margin([v - extra for v in shifted(base, tm, margin=mm)]), 0.0, 1.0, 0.0, tol=1e-7)
            for k, v in BILLS.items():         # the lump route through bill_cost gives back the shortcut's own margins
                assert abs(at_cost(bill_cost(v, eis) - bill_cost(BILL0, eis)) - at_bill(v)) < 1e-6
            share = {str(paid): partner(at_bill(BILL0 * (1 - paid)), paid) for paid in (0.25, 0.5)}
            res[site] = {"margin": m, "price": p, "bill": bl, "at_zero_bill": L.margin(shifted(base, tm, bill=1e-9)),
                         "price_cost_held": None if m is None else COST0 + PRICE0 * m,
                         "margin_bill9": at_bill(BILL9), "margin_bill7": at_bill(BILL7),
                         "margin_by_years": {str(k): at_bill(v) for k, v in BILLS.items()},
                         "margin_by_years_phased": {str(k): at_cost(bill_cost(v, eis, eis - k) - bill_cost(BILL0, eis)) for k, v in BILLS.items()},
                         "partner": share,
                         "per_point": [t["U"] / 100.0 for t in tm],      # $B per margin point, each column
                         "per_10m_price": [t["V"] * 10.0 for t in tm],
                         "df": tm[0]["df"]}
    return res


def partner(m_free, paid):
    """A partner pays `paid` of the bill. m_free: the fps margin Boeing needs if the money is free. The most of the fps's
    operating profit the partner can take back before the pass is lost (1 - m_free / today's margin; negative: it fails
    even free), and the margin needed if the partner takes the same share of the profit as it pays of the bill."""
    return {"paid": paid, "margin_free": m_free, "passes_free": m_free is not None and m_free <= M0,
            "max_profit_share": None if m_free is None else 1.0 - m_free / M0,
            "margin_fair": None if m_free is None else m_free / (1.0 - paid)}


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


def context(eis, kw=None, tj=False, page=False):  # noqa: C901
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
                "capacity_window": sum(sd[y]["cap_max"] + sd[y]["cap_fps"] for y in win if y >= eis),
                "delivered_window": sum(b[y]["nb_units"] for y in win if y >= eis),
                "full_years": sum(1 for y in win if y >= eis and b[y]["nb_units"] >= sd[y]["cap_max"] + sd[y]["cap_fps"] - 1.0),
                "spare_by_year": {y: sd[y]["cap_max"] + sd[y]["cap_fps"] - b[y]["nb_units"] for y in win if y >= eis},
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


def confirm(eis, kw, site, tj=False, page=False, sw=False, **over):
    """Boeing's test margin for `site` with the board re-solved at `over` (0 at a pass line)."""
    with board(**over):
        return evaluate(eis, kw, tj, page, sw)[site]["margin"]


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


def firm_left(kw, year=2038):
    """Firm orders still open at the end of `year` (Do Nothing, column S2)."""
    with L.patched(**kw):
        st, cv = L.grid_states(L.PLAN_DN)[1]
        v = M.value(st, covert=cv, series=True)
        r = next(r for r in v["_af_series"]["years"] if r["year"] == year)
        return r["sd"]["firm_b"] + r["sd"]["firm_a"]


def check_dn_window(n, e):
    """Moving Do Nothing's window changes no year's Boeing profit up to 2060 and no bridge line other than the two
    window-driven profit lines, in any of the six columns (only which years count)."""
    worst = 0.0
    with L.patched(**demand_kw(n)):
        for col in range(len(L.SCEN)):
            rows, brs = [], []
            for w in (None, e):
                with dn_window(w):
                    st, cv = L.grid_states(L.PLAN_DN)[col]
                    v = M.value(st, covert=cv, series=True)
                    rows.append({r["year"]: (r["boeing"]["nb_profit"], r["boeing"]["sq_nb_profit"], r["boeing"]["nb_units"])
                                 for r in v["_af_series"]["years"] if r["year"] <= 2060})
                    brs.append(v["boeing"]["bridge"])
            worst = max(worst, max(abs(a - b) for y in rows[0] for a, b in zip(rows[0][y], rows[1][y])))
            worst = max(worst, max(abs(brs[0].get(k, 0.0) - brs[1].get(k, 0.0)) for k in LINES
                                   if k not in ("nb_profit_vs_sq", "supply_demand")))
    return worst


def margin_case(eis, kw, tj=False, page=False, sw=False):
    """Evaluate, then the margin and bill needed at the better site, each re-checked on a re-solved dashboard."""
    ev = evaluate(eis, kw, tj, page, sw)
    an = analytic(eis, ev, kw, tj, page)
    mn, ms = best_of(an, "margin", min)
    bn, bs = best_of(an, "bill", max)
    ck = {"margin": confirm(eis, kw, ms, tj, page, sw, af_m_fps=100.0 * mn),
          "bill": confirm(eis, kw, bs, tj, page, sw, af_cx_fps10=bn)}
    assert all(abs(v) < 1e-5 for v in ck.values()), ck
    return {"eval": ev, "analytic": an, "margin_needed": mn, "margin_site": ms, "bill_needed": bn, "bill_site": bs, "confirm": ck}


def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    out = {"tests": {"business_case": L.BUSINESS_CASE, "downside": L.DOWNSIDE, "buffer": L.BUFFER,
                     "expected_weights": {L.SCEN_LABELS[i]: w for i, w in L.EXPECTED.items()}},
           "columns": L.SCEN_LABELS, "eis": EIS, "scenarios": NS,
           "base": {"bill": BILL0, "margin": M0, "price": PRICE0, "cost": COST0, "bill7": BILL7, "bill9": BILL9},
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
    # the game's own 7-year fps entering service in 2039 (launched 2032) is the 10-year fps at the 7-year bill, exactly
    P7 = {"renton": "fps 7-yr at Renton + 787: hold", "new_site": L.PLAN_7}
    for n in ("0", "4"):
        kw = demand_kw(n)
        ev10 = evaluate(2039, kw)
        for s_, p7 in P7.items():
            with L.patched(**kw):
                dn = L.grid_row(L.PLAN_DN)
                row = L.grid_row(p7, at_eis(2039))
                tm = terms(PLANS[s_], 2039)
            gap = max(abs((a - b) - c) for a, b, c in zip(row, dn, shifted(ev10[s_]["items"], tm, bill=BILL7)))
            assert gap < 1e-9, (n, s_, gap)
    out["dn_window_check"] = max(check_dn_window(n, e) for n in ("0", "4") for e in EIS)
    assert out["dn_window_check"] < 1e-9, out["dn_window_check"]
    # demand of each scenario as the game sees it (class share applied)
    dem = {}
    for n in NS:
        with L.patched(**demand_kw(n)):
            dem[n] = {y: SD.demand(y) for y in range(2026, 2071)}
    with L.patched():
        dem["game"] = {y: SD.demand(y) for y in range(2026, 2071)}
    out["demand"] = dem
    out["firm_left_2038"] = {"splice": {n: firm_left(demand_kw(n)) for n in NS},
                             "page_from_2026": {n: firm_left(demand_kw(n, whole=True)) for n in NS}}
    cases = {}
    for n in NS:
        for e in EIS:
            kw = demand_kw(n)
            ev = evaluate(e, kw)
            an = analytic(e, ev, kw)
            rec = {"eval": ev, "analytic": an, "context": context(e, kw)}
            rec["margin_needed"], rec["margin_site"] = best_of(an, "margin", min)
            rec["price_needed"], rec["price_site"] = best_of(an, "price", min)
            rec["price_cost_held"], _ = best_of(an, "price_cost_held", min)
            rec["bill_needed"], rec["bill_site"] = best_of(an, "bill", max)
            rec["margin_bill9"], rec["bill9_site"] = best_of(an, "margin_bill9", min)
            rec["margin_bill7"], rec["bill7_site"] = best_of(an, "margin_bill7", min)
            s_ = ev["best"]
            a_ = an[s_]
            # the pass lines re-checked on a re-solved dashboard
            ck = {"margin": confirm(e, kw, rec["margin_site"], af_m_fps=100.0 * rec["margin_needed"]),
                  "price": confirm(e, kw, rec["price_site"], af_price_fps=rec["price_needed"]),
                  "price_cost_held": confirm(e, kw, rec["margin_site"], af_price_fps=rec["price_cost_held"],
                                             af_m_fps=100.0 * (rec["price_cost_held"] - COST0) / rec["price_cost_held"]),
                  "bill": confirm(e, kw, rec["bill_site"], af_cx_fps10=rec["bill_needed"]),
                  "bill9": confirm(e, kw, rec["bill9_site"], af_cx_fps10=BILL9, af_m_fps=100.0 * rec["margin_bill9"]),
                  "bill7": confirm(e, kw, rec["bill7_site"], af_cx_fps10=BILL7, af_m_fps=100.0 * rec["margin_bill7"])}
            for yrs in ("8",):
                ck["bill" + yrs] = confirm(e, kw, s_, af_cx_fps10=BILLS[int(yrs)], af_m_fps=100.0 * a_["margin_by_years"][yrs])
            for paid in ("0.25", "0.5"):
                pt = a_["partner"][paid]
                ck["partner" + paid] = confirm(e, kw, s_, af_cx_fps10=BILL0 * (1 - float(paid)), af_m_fps=100.0 * pt["margin_free"])
            if not quick:
                rec["ramp_needed"] = lever(e, lambda k: {"ramp": L.compressed(k)}, 1.0, 12.0, 1e-3, kw)
                inst = evaluate(e, dict(kw, ramp=L.instant))
                rec["ramp_profiles"] = {"game": ramp_profile(1.0, e), "x1.5": ramp_profile(1.5, e)}
                if rec["ramp_needed"]:
                    rec["ramp_profiles"]["needed"] = ramp_profile(rec["ramp_needed"], e)
                rec["ramp_instant"] = {"best": inst["best"], "expected": inst[inst["best"]]["expected"], "margin": inst[inst["best"]]["margin"]}
                rec["pref_needed"] = lever(e, lambda x: {"fps_pref_pp": x}, 0.0, 100.0, 1e-3, kw)
                rec["pref_sweep"] = {}
                for x in (0.0, 10.0, 20.0, 40.0, 60.0, 100.0):
                    kx = dict(kw, fps_pref_pp=x)
                    w = evaluate(e, kx)
                    c = context(e, kx)["fps"]
                    rec["pref_sweep"][str(x)] = {"best": w["best"], "expected": w[w["best"]]["expected"], "margin": w[w["best"]]["margin"],
                                                 "used": c["delivered_window"] / c["capacity_window"], "full_years": c["full_years"],
                                                 "spare_by_year": c["spare_by_year"]}
                # package: customers' preference +10 points once the fps flies; the margin still needed
                kp = dict(kw, fps_pref_pp=10.0)
                evp = evaluate(e, kp)
                anp = analytic(e, evp, kp)
                rec["pref10_margin"], rec["pref10_site"] = best_of(anp, "margin", min)
                ck["pref10"] = confirm(e, kp, rec["pref10_site"], af_m_fps=100.0 * rec["pref10_margin"])
                # packages: a faster ramp (1.5x) alone, and with a partner paying a quarter of the bill
                k15 = dict(kw, ramp=L.compressed(1.5))
                ev15 = evaluate(e, k15)
                an15 = analytic(e, ev15, k15)
                m15, s15 = best_of(an15, "margin", min)
                rec["ramp15"] = {"eval": {s: {kk: ev15[s][kk] for kk in ("items", "expected", "worst", "risk_case", "margin", "passes")}
                                          for s in PLANS}, "analytic": an15, "margin_needed": m15, "site": s15}
                ck["ramp15"] = confirm(e, k15, s15, af_m_fps=100.0 * m15)
                pk = {s: an15[s]["partner"]["0.25"] for s in PLANS}
                ps = min(PLANS, key=lambda s: pk[s]["margin_free"])
                rec["package"] = {"site": ps, **pk[ps]}
                ck["package"] = confirm(e, k15, ps, af_cx_fps10=BILL0 * 0.75, af_m_fps=100.0 * pk[ps]["margin_free"])
                rec["fundable"] = fundable(e, kw)
            assert all(abs(v) < 1e-5 for v in ck.values()), ck
            rec["confirm"] = ck
            rec["bridge"] = bridge(e, kw, s_)
            assert abs(sum(rec["bridge"].values()) - ev[s_]["expected"]) < 1e-9
            # counting convention: Do Nothing over the same years as this fps
            rec["same_window"] = margin_case(e, kw, sw=True)
            # worlds (not Boeing's levers): Boeing loses 3 points a year while NGSA flies alone; NGSA 3 years late
            rec["worlds"] = {}
            for lab, kk, post in (("erosion3", dict(kw, options=dict(kw["options"], boeing_pp_after_ngsa=3.0)), None),
                                  ("ngsa2040", kw, ngsa_at(2040))):
                w = evaluate_post(e, kk, post) if post else evaluate(e, kk)
                rec["worlds"][lab] = {"best": w["best"], **{k: w[w["best"]][k] for k in ("items", "expected", "worst", "risk_case", "margin", "passes")}}
            cases["N%s/%d" % (n, e)] = rec
            if not quick and e != EIS[0]:
                # how much more customers would have to prefer this later fps (a better product) for it to need no more
                # margin than the 2039 fps at the 10-year bill and at a 9-year bill
                c39 = cases["N%s/%d" % (n, EIS[0])]
                rec["pref_to_match"] = {}
                for lab, target in (("10", c39["margin_needed"]), ("9", c39["margin_bill9"])):
                    def f(x, kw=kw):
                        kx = dict(kw, fps_pref_pp=x)
                        a = analytic(e, evaluate(e, kx), kx)
                        return target - min(a[s]["margin"] for s in PLANS)
                    rec["pref_to_match"][lab] = L.bisect(f, 0.0, 40.0, 0.0, tol=1e-3)
            b = ev[s_]
            sw = rec["same_window"]
            print("N=%s fps %d: %-8s exp %+6.2f (same window %+6.2f) | margin %.1f%% price $%.0fM (cost held $%.1fM) bill $%.1fB | "
                  "bill9 %.1f%% ramp %s pref %s  %.0fs" % (
                      n, e, s_, b["expected"], sw["eval"][sw["eval"]["best"]]["expected"], 100 * rec["margin_needed"], rec["price_needed"],
                      rec["price_cost_held"], rec["bill_needed"], 100 * rec["margin_bill9"], rec.get("ramp_needed") and round(rec["ramp_needed"], 2),
                      rec.get("pref_needed") and round(rec["pref_needed"], 1), time.time() - t0))
    out["cases"] = cases
    # sensitivities (the item and the margin and bill needed, both re-checked)
    sens = {}
    for lab, kwf, tj, page in (("tail", lambda n: demand_kw(n, tail=True), False, False),
                               ("page_from_2026", lambda n: demand_kw(n, whole=True), False, False),
                               ("tianjin", lambda n: demand_kw(n), True, False),
                               ("page_supply", lambda n: demand_kw(n), True, True)):
        for n in NS:
            for e in EIS:
                r = margin_case(e, kwf(n), tj, page)
                sens["%s/N%s/%d" % (lab, n, e)] = r
                b = r["eval"][r["eval"]["best"]]
                print("%-14s N=%s fps %d: best %-8s exp %+6.2f worst %+6.2f risk %+6.2f margin %.1f%% bill $%.1fB" % (
                    lab, n, e, r["eval"]["best"], b["expected"], b["worst"], b["risk_case"], 100 * r["margin_needed"], r["bill_needed"]))
    out["sensitivities"] = sens
    with L.patched(), supply(page=True):
        out["page_supply_check"] = {str(e): {y: page_boeing({"prog": {"fps": {"eis": e}}}, y) for y in range(2036, 2053)} for e in EIS}
    json.dump(round_all(out), open(os.path.join(HERE, "demand_scenarios.json"), "w"), indent=1, default=str)
    print("wrote demand_scenarios.json  %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
