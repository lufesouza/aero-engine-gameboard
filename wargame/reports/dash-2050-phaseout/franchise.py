"""A narrowbody-franchise overlay on the MAX phase-out game: what staying in, or leaving, the narrowbody market is worth
beyond what Boeing's brief counts, built from Boeing's history and how analysts and other companies value it
(data/franchise_research.json: the sourced findings, the model design and its two adversarial checks).

The game values each plan on its own counted window (an fps for 20 years from entry into service, Do Nothing to 2060),
in constant 2026 dollars at 10.5%, against the status quo. This module rebuilds every plan's yearly flows (the game's
own lines, asserted to give back the brief's value of every plan in every column to the cent) and adds these terms,
every plan in a round counted to the same end year (the latest fps entry into service + 49):

  demand after 2060    - every year after 2060 comes from the game's own supply-and-demand engine run on one of three
                         demand tails (as run, held at its 2060 value, rising on the conservative curve's shape), with
                         Boeing's board share held at its last value in the game. The tails follow the run's curve to
                         2060, so each tail is one world from 2061 for every plan and every year, counted or not.
  C0 counted years     - the brief's own counted years after 2060 restated on the tail (zero on the run's own curve and
                         for every 2030 plan; it matters for launches from 2035, whose counted years run past 2060).
  C1 continuing value  - narrowbody profit against the status quo after the plan's counted window: the fps to its 50th
                         year in service (Boeing's "50-year product"), its margin fading toward the game's A320neo margin
                         (Mauboussin's fade of excess returns), less a sustaining derivative (a share of the fps bill at
                         entry into service + 27, with the game's debt penalty). Do Nothing has none here: the MAX is
                         gone from 2060 in every plan and in the status quo.
  C2 services          - OEM services profit on every Boeing narrowbody delivered to the end year, by age, over its life.
  C3 stranded overhead - shared BCA overhead carried by narrowbody volume: it falls only so fast (alpha x F a year) and
                         never below a residual (rho x F). Two readings, because the repo does not document the margins'
                         basis: "fully loaded" (the game's margins already absorb overhead per aircraft, so only the
                         unabsorbed part is extra; used in the views) and "programme" (the game never charges overhead,
                         so each plan carries all it keeps; a sensitivity: it works against the fps).
  C4 widebody erosion  - widebody share lost while Boeing has no new narrowbody in service, in proportion to the MAX's
                         run-off (judgement; the last view only).
  C5 MAX price fade    - Do Nothing's MAX conceding price against NGSA (sensitivity only: it conflicts with the game's
                         own supply-and-demand state, per the logic check).
  C6 closing costs     - half when the MAX ends (every plan; about 2042-45 with an fps, as its buyers move to the fps),
                         half when Boeing's narrowbody business ends (Do Nothing when the MAX ends; an fps after its 50th
                         year). Held at $3.0B in the low and high cases: it costs the fps in 2030-35 and helps it later.

Views: game (none), core (C0, C1, C2, C6), core+overhead (+ C3 fully loaded), full (+ C4); sensitivities full+programme,
full+price and full-C0. Rival moves are held as the game played them (an overlay on Boeing's valuation, not a replay). Each plan
is valued in every column of every round's brief, Boeing's decision (thresholds.decide, all four readings) is re-run
with the terms on, at 10.5% and at 8.1% (10.5% read as nominal), and the game-only thresholds are asserted equal to
thresholds.json. The derivative is always bought (in the low case it can cost more than the late-life profit it
sustains).

  python3 franchise.py            writes data/franchise.json
"""
import functools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402
import thresholds as T  # noqa: E402

M, R, B, SD = L.M, L.R, L.B, L.SD
P = M.af_params()
M0, PRICE = P["v_margin_fps"], P["PRICE_fps"]             # 0.2564, $B per aircraft (0.055)
MAX_UNIT = P["PRICE_737"] * P["v_margin_737"]              # $B per MAX delivered (0.00384)
A320NEO_MARGIN = P["v_margin_a320"]                       # the game's A320neo margin (the fade floor)
WB_PER_PP = 0.01 * P["WB_PER_YR"] * P["PRICE_WB"] * P["v_margin_787"]     # $B a year per widebody share point
D_REF = 684.0                                              # Do Nothing's full MAX rate (2039-44)
Y0 = 2026
DG = os.path.join(HERE, "..", "..", "dashgame")
ROWS = ["Do Nothing", "Re-engine"] + list(T.SOLO) + list(T.PAIRS)
PLAN_OF = {"Do Nothing": T.DN, "Re-engine": T.RE}
PLAN_OF.update({k: v[0] for k, v in T.SOLO.items()})
PLAN_OF.update({k: v[0] for k, v in T.PAIRS.items()})

# ─────────────────────────────── parameters (low / base / high value to the fps) ───────────────────────────────
PARAMS = {
    "tail": {"low": "as run", "base": "held", "high": "rising"},
    "fade_years": {"low": 10, "base": None, "high": 0},          # None: fade to the floor by EIS+50; 0: no fade
    "kappa": {"low": 0.25, "base": 0.125, "high": 0.10},         # sustaining derivative, share of the fps bill
    "pi_s": {"low": 0.045, "base": 0.0836, "high": 0.135},       # services profit, $M per aircraft-year (0.30/0.38/0.45 x 15/22/30%)
    "F_nb": {"low": 1.51, "base": 1.91, "high": 2.40},           # $B a year: (BCA D&A 0.74 + 40/45/50% of G&A 5.0) x NB share 0.55/0.64/0.74
    "rho": {"low": 0.20, "base": 0.35, "high": 0.50},            # irreducible share of it
    "alpha": {"low": 0.25, "base": 0.15, "high": 0.10},          # share of it removable per year
    "dsh": {"low": 0.0, "base": 5.0, "high": 15.0},              # widebody share points lost when no longer full-line
    "c_price": {"low": 0.0, "base": 0.015, "high": 0.03},        # Do Nothing MAX price concession at full effect
    "c_exit": {"low": 3.0, "base": 3.0, "high": 3.0},            # $B (precedents $1-3B today); held in the combined cases,
                                                                 # because it costs the fps in 2030-35 and helps it later
}
AGE_MULT = [(1, 3, 0.4), (4, 8, 0.8), (9, 20, 1.2), (21, 25, 0.9), (26, 30, 0.5), (31, 40, 0.3)]


def age_mult(a):
    return next(v for lo, hi, v in AGE_MULT if lo <= a <= hi)


def surv(a):
    if a <= 18:
        return 1.0
    if a <= 32:
        return 1.0 - (1.0 - 0.08) * (a - 18) / 14.0
    if a <= 40:
        return 0.08 * (40 - a) / 8.0
    return 0.0


# ─────────────────────────────── demand after 2060 ───────────────────────────────
@functools.lru_cache(maxsize=None)
def tail_curve(kind):
    """A demand_curve option for the run's world: the page curve to 2060, then as run, held at its 2060 value, or
    following the conservative curve's shape rescaled to the page's 2060 level (no splice jump)."""
    page = json.load(open(os.path.join(DG, "demand_page_n0.json")))
    if kind == "as run":
        return "demand_page_n0.json"
    game = json.load(open(os.path.join(DG, "demand_conservative.json")))
    pg = {y: (r, g) for y, r, g in zip(page["years"], page["replacements"], page["growth"])}
    gm = {y: r + g for y, r, g in zip(game["years"], game["replacements"], game["growth"])}
    years = list(range(min(pg), 2141))
    rep, gro = [], []
    for y in years:
        if y <= 2060:
            r, g = pg[y]
        else:
            r, g = pg[2060]
            if kind == "rising":
                f = gm[min(y, max(gm))] / gm[2060]
                r, g = r * f, g * f
        rep.append(r)
        gro.append(g)
    path = os.path.join(HERE, "data", "curves", "franchise_%s.json" % kind)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"about": "page curve to 2060, then %s; whole single-aisle market before the class share. Built by franchise.py." % kind,
               "years": years, "replacements": rep, "growth": gro}, open(path, "w"))
    return os.path.abspath(path)


TAILS = ("as run", "held", "rising")
TAIL_START = 2060          # the tails follow the run's curve to 2060 and apply to every year after it, counted or not
LIFE = 50                  # years in service counted for an fps: entry into service to EIS + 49 (the brief: EIS to EIS + 19)


# ─────────────────────────────── one plan in one column: its yearly flows ───────────────────────────────
def flows(n, name, j, horizon):
    """The game's own yearly lines for one plan and column, and what the franchise terms need, out to `horizon`.
    (L.patched does not nest: leaving an inner block restores the module's real options, so every block here is
    opened on its own, never inside another.)"""
    with L.patched(options=T.O):
        slab, s, c = T.column_states(n, PLAN_OF[name])[j]
        v = M.value(s, covert=c, series=True)
        eis, a, b, dt = M.af_inputs(s, c)
        cell = M.eval_cell(eis, a, b)
        costs = SD.costs(s)
    bo = v["boeing"]
    ser = {r["year"]: r for r in v["_af_series"]["years"]}
    tcd = cell["b_tc_data"]
    fps, re = M.live(s, "fps"), M.live(s, "re787")
    out = {"label": slab, "pv": bo["pv_delta"], "years": {}, "fps_eis": fps["eis"] if fps else None,
           "fps_bill": M.af_bill("fps", fps["variant"]) if fps else 0.0, "re_eis": re["eis"] if re else None,
           "re_bill": M.af_bill("re787") if re else 0.0, "strain": -cell["b_strain"],
           "nom": tcd.get("nom_capex", 0.0), "pv_capex": tcd.get("pv_capex", 0.0), "renton": 0.0, "bridge": bo["bridge"]}
    for side, yy, item, xx in costs:
        if side == "boeing":
            out["renton"] += -xx
            out["renton_year"] = yy
    for y, r in ser.items():
        x = r["boeing"]
        out["years"][y] = {"in_nb": bool(x["nb_in_window"]), "fps": x["nb_units_new"], "max": x["nb_units_old"],
                           "sq": x["sq_nb_profit"], "wb": (x["wb_profit"] - x["sq_wb_profit"]) if x["wb_in_window"] else 0.0,
                           "fps_unit": x["nb_price"] / 1000.0 * x["nb_margin"] if x["nb_units_new"] else 0.0}
        if x["nb_units_new"]:
            assert abs(x["nb_price"] / 1000.0 - PRICE) < 1e-12 and abs(x["nb_margin"] - M0) < 1e-12
        if x["nb_units_old"]:
            assert abs(x["sq_nb_profit"] - x["sq_nb_units"] * MAX_UNIT) < 1e-9
    # after the game's last year: the game's own supply-and-demand engine run on, with the board's share for Boeing
    # (the input SD.apply gives it: the board's units / 2000) held at its last value
    pref = {y: ser[y]["boeing"]["board_nb_units"] / SD.NB_BOARD for y in ser}
    last = max(pref)
    out["pref_last"] = pref[last]
    ext = {}
    for kind in (TAILS if horizon else ()):
        with L.patched(options=dict(T.O, demand_curve=tail_curve(kind))):
            ys = list(range(Y0, max(horizon, last) + 1))
            rows = SD.year_rows(s, {y: pref.get(y, pref[last]) for y in ys}, ys)
            sq = SD.year_rows(SD.sq_state(), {y: 0.40 for y in ys}, ys)
        for y in ser:       # the engine run on gives back the game's own rows (every year for the run's own curve; to
            if kind == "as run" or y <= 2060:        # 2060, where the tails start, for the others)
                x = out["years"][y]
                assert abs(rows[y]["dlv_fps"] - x["fps"]) < 1e-6 and abs(rows[y]["dlv_max"] - x["max"]) < 1e-6, (name, j, kind, y)
                assert abs(sq[y]["dlv_max"] * MAX_UNIT - x["sq"]) < 1e-6, (name, j, kind, y)
        ext[kind] = {y: {"fps": rows[y]["dlv_fps"], "max": rows[y]["dlv_max"], "sq": sq[y]["dlv_max"] * MAX_UNIT}
                     for y in ys if y > TAIL_START}
    out["ext"] = ext
    out["window_end"] = max(y for y, r in out["years"].items() if r["in_nb"])
    return out


def check_game(f, r=P["WACC_B"]):
    """The game's value of the plan from its yearly lines (no franchise terms)."""
    return game_pv(f, r, M0, 1.0)


def df(y, r):
    return 1.0 / (1.0 + r) ** (y - Y0)


def tc(nom, pv):
    return M.true_cost(nom, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"])


def game_pv(f, r, m, k):
    """The game's own value of the plan at rate r, fps margin m and Boeing paying share k of the fps bill."""
    v = 0.0
    for y, x in f["years"].items():
        if x["in_nb"]:
            v += (x["fps"] * PRICE * m + x["max"] * MAX_UNIT - x["sq"]) * df(y, r)
        v += x["wb"] * df(y, r)
    if f["renton"]:
        v += f["renton"] * df(f["renton_year"], r)
    nom, pvc = 0.0, 0.0
    if f["fps_eis"]:
        nom += f["fps_bill"] * k
        pvc += f["fps_bill"] * k * df(f["fps_eis"], r)
    if f["re_eis"]:
        nom += f["re_bill"]
        pvc += f["re_bill"] * df(f["re_eis"], r)
    if nom > 0:
        v -= tc(nom, pvc)
        if f["strain"]:
            ratio0 = f["pv_capex"] / f["nom"]
            v -= f["strain"] / ratio0 * (pvc / nom)          # the strain is priced at the PV factor of the whole spend
    return v


# ─────────────────────────────── the franchise terms ───────────────────────────────
def margin_at(y, f, m, prm):
    """fps margin in a year after its counted window: from m toward the A320neo margin (Mauboussin's fade)."""
    fy = prm["fade_years"]
    if fy == 0:
        return m
    T_end = f["window_end"]
    span = fy if fy else (f["fps_eis"] + LIFE - 1 - T_end)
    w = min(1.0, max(0.0, (y - T_end) / span))
    return m + (A320NEO_MARGIN - m) * w


def nb_series(f, tail, horizon):
    """Deliveries (MAX, fps in its 50 years in service) and status-quo MAX profit by year to `horizon`: the game's rows
    to 2060, then the engine run on the tail (for the run's own curve these are the game's rows where they overlap).
    The fps is counted to its 50th year in service only (no successor is assumed)."""
    out = {y: (x["max"], x["fps"], x["sq"]) for y, x in f["years"].items() if y <= TAIL_START}
    for y, x in f["ext"][tail].items():
        out[y] = (x["max"], x["fps"], x["sq"])
    life = f["fps_eis"] + LIFE - 1 if f["fps_eis"] else None
    return {y: (mx, fp if (life and y <= life) else 0.0, sq) for y, (mx, fp, sq) in out.items() if y <= horizon}


def terms(f, r, m, prm, horizon):
    """Each franchise term's PV (2026, rate r) for one plan in one column, fps margin m (only C1 depends on m, linearly).
    C1 is counted against the status quo, as the game's own lines are; the others are levels. Only differences between
    plans enter the decision (every test in thresholds.decide is an item against another plan)."""
    tail = prm["tail"]
    ns = nb_series(f, tail, horizon)
    is_fps = bool(f["fps_eis"])
    out = {}
    # C0: the brief's own counted years after 2060 on the same demand tail (zero for the run's own curve), so each tail
    # is one world: without it, an fps whose counted years run past 2060 would sell on the run's falling curve to the
    # end of its window and on the tail only after it
    c0 = 0.0
    for y, x in f["years"].items():
        if x["in_nb"] and y > TAIL_START:
            mx, fp, sq = ns[y]
            c0 += ((fp - x["fps"]) * PRICE * m + (mx - x["max"]) * MAX_UNIT - (sq - x["sq"])) * df(y, r)
    out["C0"] = c0
    # C1: narrowbody profit against the status quo after the plan's counted window, to the round's common end year;
    # the fps margin fades toward the A320neo margin; less the sustaining derivative at entry into service + 27
    c1 = 0.0
    for y in range(f["window_end"] + 1, horizon + 1):
        mx, fp, sq = ns[y]
        c1 += ((fp * PRICE * margin_at(y, f, m, prm) if fp > 0 else 0.0) + mx * MAX_UNIT - sq) * df(y, r)
    if is_fps:
        dbill = prm["kappa"] * f["fps_bill"]
        c1 -= tc(dbill, dbill * df(f["fps_eis"] + 27, r))
    out["C1"] = c1
    # C2: OEM services on every Boeing narrowbody delivered 2026 to the end year, by age, over the aircraft's life
    c2 = 0.0
    for cy in range(Y0, horizon + 1):
        mx, fp, _ = ns[cy]
        d = mx + fp
        if d > 0:
            c2 += d * sum(prm["pi_s"] / 1000.0 * age_mult(a) * surv(a) * df(cy + a, r) for a in range(1, 41))
    out["C2"] = c2
    # C3: shared overhead carried by narrowbody volume: it falls with volume only at alpha x F a year, and never below
    # rho x F while Boeing builds narrowbodies or after; two readings
    F, rho, alpha = prm["F_nb"], prm["rho"], prm["alpha"]
    K_prev, so_pv, k_pv = None, 0.0, 0.0
    for y in range(Y0, horizon + 1):
        mx, fp, _ = ns[y]
        V = min(1.0, (mx + fp) / D_REF)
        Kstar = F * (rho + (1 - rho) * V)
        K = Kstar if (K_prev is None or Kstar >= K_prev) else max(Kstar, K_prev - alpha * F)
        K_prev = K
        so_pv += (K - F * V) * df(y, r)
        k_pv += K * df(y, r)
    out["C3_loaded"] = -so_pv
    out["C3_programme"] = -k_pv
    # C4: widebody share lost while Boeing has no new narrowbody in service, in proportion to the MAX's run-off (2045 on)
    c4 = 0.0
    for y in range(2045, horizon + 1):
        mx, fp, _ = ns[y]
        if fp <= 0:
            c4 -= prm["dsh"] * max(0.0, 1.0 - mx / D_REF) * WB_PER_PP * df(y, r)
    out["C4"] = c4
    # C5: MAX price concession against NGSA inside the counted window (half on fps plans' MAX run-out)
    c5 = 0.0
    w = 0.5 if is_fps else 1.0
    for y, x in f["years"].items():
        if x["in_nb"] and y >= 2037 and x["max"] > 0:
            c5 -= x["max"] * P["PRICE_737"] * prm["c_price"] * min(1.0, (y - 2036) / 5.0) * w * df(y, r)
    out["C5"] = c5
    # C6: closing costs; half when the MAX ends (every plan), half when Boeing's narrowbody business ends (no MAX and no
    # fps: Do Nothing when the MAX ends, an fps plan after the fps's 50th year)
    last_max = max((y for y, (mx, fp, sq) in ns.items() if mx > 0.5), default=Y0)
    last_nb = max((y for y, (mx, fp, sq) in ns.items() if mx + fp > 0.5), default=Y0)
    if is_fps:
        last_nb = max(last_nb, f["fps_eis"] + LIFE - 1)
    out["C6"] = -0.5 * prm["c_exit"] * (df(last_max + 1, r) + df(last_nb + 1, r))
    out["_years"] = {"last_max": last_max, "last_nb": last_nb}
    return out


def tail_is_run(prm):
    return prm["tail"] == "as run"


def prm_set(level):
    return {k: v[level] for k, v in PARAMS.items()}


SCENARIOS = {                 # which terms count in each view
    "game": (),
    "core": ("C0", "C1", "C2", "C6"),
    "core+overhead": ("C0", "C1", "C2", "C6", "C3_loaded"),
    "full": ("C0", "C1", "C2", "C6", "C3_loaded", "C4"),
    # sensitivities on the full view: the other reading of the overhead, and the MAX price concession
    "full+programme": ("C0", "C1", "C2", "C6", "C3_programme", "C4"),
    "full+price": ("C0", "C1", "C2", "C6", "C3_loaded", "C4", "C5"),
    "full-C0": ("C1", "C2", "C6", "C3_loaded", "C4"),          # the full view without restating the counted years
}


# ─────────────────────────────── per round: every row, every column ───────────────────────────────
def round_flows(n):
    st = T.start(n)
    year = T.YEARS[n]
    ncol = len(B.rival_scenarios(st, "boeing", year))
    probe = {name: flows(n, name, 0, None) for name in ROWS}
    eis_max = max((f["fps_eis"] for f in probe.values() if f["fps_eis"]), default=year + 10)
    horizon = eis_max + LIFE - 1
    fl = {name: [flows(n, name, j, horizon) for j in range(ncol)] for name in ROWS}
    # the game's lines give back the brief's values to the cent, every row and column
    rec = json.load(open(os.path.join(HERE, "record", "grids_r%d.json" % n)))["boeing"]
    g = {x["plan"]: [c[0] for c in x["cells"]] for x in rec["rows"]}
    for name in ROWS:
        for j, f in enumerate(fl[name]):
            assert abs(game_pv(f, P["WACC_B"], M0, 1.0) - g[PLAN_OF[name]][j]) < 1e-9, (n, name, j)
            assert abs(f["pv"] - g[PLAN_OF[name]][j]) < 1e-9
    return fl, horizon


def term_table(fl, horizon, r, prm):
    """Each row's and column's franchise terms at the base margin, and C1's slope in the margin."""
    out = {}
    for name in ROWS:
        cols = []
        for f in fl[name]:
            t0 = terms(f, r, M0, prm, horizon)
            t1 = terms(f, r, M0 + 0.1, prm, horizon)
            t0["C1_slope"] = (t1["C1"] - t0["C1"]) / 0.1
            t0["C0_slope"] = (t1["C0"] - t0["C0"]) / 0.1
            if tail_is_run(prm):
                assert abs(t0["C0"]) < 1e-9 and abs(t1["C0"]) < 1e-9
            for c in ("C2", "C3_loaded", "C3_programme", "C4", "C5", "C6"):
                assert t1[c] == t0[c]
            cols.append(t0)
        out[name] = cols
    return out


def values_at(fl, tt, r, m, k, scen):
    """Every row's value in every column at margin m and bill share k: the game's lines plus the scenario's terms."""
    out = {}
    for name in ROWS:
        vals = []
        for f, t in zip(fl[name], tt[name]):
            v = game_pv(f, r, m, k)
            for c in scen:
                v += t[c] + (t[c + "_slope"] * (m - M0) if c in ("C0", "C1") else 0.0)
            vals.append(v)
        out[name] = vals
    return out


def thresholds_with(n, fl, tt, r, scen):
    """The margin and bill-cut thresholds of Boeing's decision (thresholds.decide, every reading) with the terms on."""
    cols = [{"label": f["label"]} for f in fl["Do Nothing"]]
    rws = {"Do Nothing": {"cols": cols}}
    cache = {}

    def dec(m, k):
        key = (round(m, 10), round(k, 10))
        if key not in cache:
            cache[key] = T.decide(n, rws, m, k, vals=values_at(fl, tt, r, m, k, scen))
        return cache[key]
    out = {}
    for mode in T.MODES:
        launched = lambda m, k: dec(m, k)[mode] is not None
        mm, ok_m = T.first(lambda x: launched(x, 1.0), 0.0, 3.0, steps=300)
        cut, ok_c = T.first(lambda sh: launched(M0, max(1e-9, 1.0 - sh)), 0.0, 1.0, steps=200)
        out[mode] = {"margin": mm, "margin_monotone": ok_m, "cut": cut, "cut_monotone": ok_c,
                     "plan_at_margin": dec(mm + 1e-7, 1.0)[mode] if mm is not None else None,
                     "plan_at_cut": dec(M0, max(1e-9, 1.0 - cut - 1e-7))[mode] if cut is not None else None}
    base = dec(M0, 1.0)
    out["base"] = {k: base[k] for k in ("pick", "pick_pairwise", "pick_worst_first", "best", "e") + T.MODES}
    # every row's value in every column at the base, just past the rule reading's margin and cut thresholds, with the
    # decision there (so the page can say what the CEO picks and what the Board's tests do)
    pts = {"base": (M0, 1.0)}
    if out["rule"]["margin"] is not None:
        pts["rule_margin"] = (out["rule"]["margin"] + 1e-7, 1.0)
    if out["rule"]["cut"] is not None:
        pts["rule_cut"] = (M0, max(1e-9, 1.0 - out["rule"]["cut"] - 1e-7))
    out["points"] = {}
    for key, (m, k) in pts.items():
        d = dec(m, k)
        out["points"][key] = {"m": m, "k": k, "values": values_at(fl, tt, r, m, k, scen),
                              "decision": {c: d[c] for c in ("pick", "pick_pairwise", "pick_worst_first", "best", "e") + T.MODES}}
    return out


def launch_when(n, fl, tt, r, scen):
    """Each plan against Do Nothing in the CEO's expected columns (the CEO's weights), PV 2026."""
    w = T.CEO_W[n]
    v = values_at(fl, tt, r, M0, 1.0, scen)
    dn = v["Do Nothing"]
    return {name: sum((v[name][i] - dn[i]) * wt for i, wt in w.items()) for name in ROWS if name != "Do Nothing"}


RATES = {"10.5%": P["WACC_B"], "8.1%": (1 + P["WACC_B"]) / (1 + 0.022) - 1}


def main():
    res = {"params": PARAMS, "scenarios": {k: list(v) for k, v in SCENARIOS.items()},
           "rates": RATES, "rounds": {},
           "constants": {"M0": M0, "price_musd": PRICE * 1000, "max_unit_musd": MAX_UNIT * 1000, "a320neo_margin": A320NEO_MARGIN,
                         "wb_per_pp_busd": WB_PER_PP, "d_ref": D_REF, "age_mult": AGE_MULT}}
    for n in T.YEARS:
        fl, horizon = round_flows(n)
        if n == 1:
            r0 = P["WACC_B"]
            dn = fl["Do Nothing"]
            ten = fl["10-year at Renton"][1]
            res["calibration"] = {
                "dn_max_profit_pv": {f["label"]: sum(x["max"] * MAX_UNIT * df(y, r0) for y, x in f["years"].items() if x["in_nb"]) for f in dn},
                "share_point_pv_10yr": 0.01 * P["NB_PER_YR"] * PRICE * M0 * sum(df(y, r0) for y in range(ten["fps_eis"], ten["fps_eis"] + 20)),
                "nb_per_yr": P["NB_PER_YR"], "eis_10yr": ten["fps_eis"]}
        rr = {"year": T.YEARS[n], "horizon": horizon, "weights": T.CEO_W[n], "columns": [f["label"] for f in fl["Do Nothing"]],
              "plans": {name: [{"fps_eis": f["fps_eis"], "window_end": f["window_end"], "pref_last": f["pref_last"],
                                "fps_units": {t: sum(nb_series(f, t, horizon)[y][1] for y in range(f["fps_eis"], f["window_end"] + 1)) if f["fps_eis"] else 0.0
                                              for t in TAILS}} for f in fl[name]]
                        for name in ROWS},
              "terms": {}, "tails": {}, "thresholds": {}, "launch_when": {}}
        tts = {}
        for level in ("low", "base", "high"):
            for rname, r in RATES.items():
                tt = term_table(fl, horizon, r, prm_set(level))
                tts[(level, rname)] = tt
                rr["terms"]["%s|%s" % (level, rname)] = {
                    name: [dict(t, game=game_pv(f, r, M0, 1.0)) for f, t in zip(fl[name], tt[name])] for name in ROWS}
        for tail in TAILS:              # the tail alone, other parameters at base
            for rname, r in RATES.items():
                prm = dict(prm_set("base"), tail=tail)
                tt = term_table(fl, horizon, r, prm)
                tts[("tail " + tail, rname)] = tt
                rr["tails"]["%s|%s" % (tail, rname)] = {name: [dict(t) for t in tt[name]] for name in ROWS}
        for (level, rname), tt in tts.items():
            r = RATES[rname]
            for scen, cs in SCENARIOS.items():
                key = "%s|%s|%s" % (level, scen, rname)
                rr["launch_when"][key] = launch_when(n, fl, tt, r, cs)
                if level.startswith("tail") and scen == "game":
                    continue
                t = thresholds_with(n, fl, tt, r, cs)
                rr["thresholds"][key] = t
                print(n, key, {md: (None if t[md]["margin"] is None else round(100 * t[md]["margin"], 1),
                                    None if t[md]["cut"] is None else round(100 * t[md]["cut"], 0)) for md in ("rule", "premium")},
                      "| base:", t["base"]["rule"], "/", t["base"]["premium"], flush=True)
        res["rounds"][str(n)] = rr
        json.dump(res, open(os.path.join(HERE, "data", "franchise.json"), "w"), indent=1)
    # the game-only thresholds give back thresholds.json (the overlay changes nothing when it is off)
    th = json.load(open(os.path.join(HERE, "data", "thresholds.json")))
    for n in T.YEARS:
        a = res["rounds"][str(n)]["thresholds"]["base|game|10.5%"]
        b2 = th["rounds"][str(n)]
        for md in T.MODES:
            for key in ("margin", "cut"):
                x, y = a[md][key], b2[md][key]
                assert (x is None and y is None) or (x is not None and y is not None and abs(x - y) < 1e-5), (n, md, key, x, y)
    print("wrote data/franchise.json")


if __name__ == "__main__":
    main()
