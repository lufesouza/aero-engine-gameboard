"""Boeing balance-sheet tracker for the dash-2050 game (game master only).

It scores Control's objective "repair the balance sheet: debt back to historical levels". It never changes a payoff:
the board's ΔPV, including its own debt penalty on $45B of debt, is untouched.

Debt is net debt (total debt minus cash and short-term investments) at year end, in constant 2026 dollars. The
airframer board's flows are unescalated 2026 prices, so they enter as they are; consensus cash flow is deflated
at the engine board's 2.2% CPI, and the debt stock loses the same 2.2% of real value each year. Each year:

    free cash   = base free cash flow (analyst consensus, see finance_inputs.json)
                + (1 - tax) x (game profit change - programme cash spend)    # one tax treatment for both
                - real interest on the debt the game has added above the no-programme path
    debt        = last year's debt in today's money - free cash, but never below the historical level once there:
                  from then on surplus cash goes to the owners (dividends, buybacks), as Boeing's Board reserves.

The game profit change is Boeing's operating profit less the board's baseline (no one launches a new programme). It
counts from the first decision year (2030), and as played: each year is valued on the state of the latest round at
or before it (runs/<run>/state_rN.json), so a later round cannot rewrite earlier years. The board's 737 rate
increase adds its share only once the rate rises (2032). Programme cash is each bill spread over its development
years on a standard curve, plus the board's two-front strain over the fps / 787 Re-engine overlap years.
The no-programme path ("debt_no_programme") is the same recursion with base free cash flow only.
"""
import copy
import functools
import json
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS_PATH = os.path.join(HERE, "finance_inputs.json")
ROUNDS = [2030, 2035, 2045, 2050]          # rules.ROUNDS (not imported: rules imports model, keep finance light)
RATE_YEAR = 2032                           # the board books the 737 rate increase and its share from 2032


def inputs():
    with open(INPUTS_PATH) as f:
        return json.load(f)


def stretch(curve, n):
    """Stretch a development-spend curve (shares by year, summing to 1) onto n years, keeping its shape."""
    m = len(curve)
    cum = [0.0]
    for c in curve:
        cum.append(cum[-1] + c)

    def at(x):                       # cumulative share at fraction x of the development time
        p = x * m
        i = min(int(p), m - 1)
        return cum[i] + (cum[i + 1] - cum[i]) * (p - i)
    out = [at((k + 1) / n) - at(k / n) for k in range(n)]
    s = sum(out)
    return [x / s for x in out]


def programme_cash(state, F=None):
    """Boeing's programme cash spend by calendar year: {year: {item: $B}}. A bill is spent over its development years
    (launch to EIS - 1) on the planning curve; a cancelled programme stops spending in its cancel year. The board's
    two-front strain is spread over the years the fps and 787 Re-engine developments overlap."""
    F = F or inputs()
    curve = F["phasing_curve"]
    out = {}

    def put(y, item, x):
        if x:
            out.setdefault(y, {}).setdefault(item, 0.0)
            out[y][item] += x
    recs = []
    for k, r in state["prog"].items():           # live programmes and cancelled ones (kept as _cancelled_<key>_<year>)
        key = k.split("_")[2] if k.startswith("_cancelled_") else k
        if key in ("fps", "re787"):
            recs.append((key, r))
    for key, r in recs:
        bill = M.af_bill(key, r.get("variant"))
        launch, eis = r["launch"], r["eis"]
        n = max(1, eis - launch)
        shares = stretch(curve, n)
        stop = r["cancel"] if r.get("cancel") is not None else eis
        label = "fps (%s)" % r.get("variant") if key == "fps" else "787 Re-engine"
        for k, sh in enumerate(shares):
            y = launch + k
            if y < stop:
                put(y, label, bill * sh)
    fps, re = M.live(state, "fps"), M.live(state, "re787")
    if fps and re:                                 # the board's strain: $ x overlap of the two development windows
        p = M.af_params()
        y0, y1 = max(fps["eis"] - 7, re["eis"] - 5), min(fps["eis"], re["eis"])
        frac = max(0.0, min(1.0, (y1 - y0) / 5.0))
        if frac > 0:
            for y in range(y0, y1):
                put(y, "Two-front strain", p["v_capex_strain_b"] * frac / (y1 - y0))
    if state.get("rate737"):
        p = M.af_params()
        y0 = state["rate737"]["launch"]
        yrs = list(range(y0, RATE_YEAR + 1))         # spent evenly from the order to the board's 2032 booking
        for y in yrs:
            put(y, "737 rate increase", p["v_capex_737_rate_hike"] / len(yrs))
    return out


def base_fcf(F, y):
    b = F["base_fcf_b"]
    if str(y) in b:
        return b[str(y)]
    last = max(int(k) for k in b)
    return F["base_fcf_after_b"] if y > last else b[str(min(int(k) for k in b))]


def _run_dir():
    run = os.environ.get("DASH_RUN")
    return os.path.join(HERE, "..", "runs", run) if run else None


@functools.lru_cache(maxsize=None)
def _played_state_json(n):
    d = _run_dir()
    p = os.path.join(d, "state_r%d.json" % n) if d else None
    if p and os.path.exists(p):
        with open(p) as f:
            return f.read()
    return None


def _profit_by_year(state, covert):
    """Boeing's (operating profit - baseline profit) by year for one state. Before 2032 a 737 rate increase adds
    nothing (the board counts it in every year when no new narrowbody is launched)."""
    def series(s):
        v = M.value(s, covert=covert, series=True)
        return {r["year"]: (r["boeing"]["nb_profit"] + r["boeing"]["wb_profit"]) -
                (r["boeing"]["sq_nb_profit"] + r["boeing"]["sq_wb_profit"]) for r in v["_af_series"]["years"]}
    out = series(state)
    if state.get("rate737"):
        s0 = copy.deepcopy(state)
        s0["rate737"] = None
        pre = series(s0)
        for y in out:
            if y < RATE_YEAR:
                out[y] = pre[y]
    return out


_HISTORY = None        # {round year: state} set by history_override(), for counterfactual replays


class history_override:
    """Within this block, earlier rounds are valued on the given states (a counterfactual line of play) instead of
    the run's played state files."""
    def __init__(self, states):
        self.states = {s["year"]: s for s in states if s.get("year") is not None}

    def __enter__(self):
        global _HISTORY
        self.prev, _HISTORY = _HISTORY, self.states
        return self

    def __exit__(self, *a):
        global _HISTORY
        _HISTORY = self.prev


def _is_ancestor(old, new):
    lo, ln = old.get("log", []), new.get("log", [])
    return len(lo) <= len(ln) and ln[:len(lo)] == lo


def profit_path(state, covert=True):
    """The game's profit change by year, as played: zero before the first decision year; each later year from the
    state of the latest round at or before it (this state for its own round year onward). Earlier rounds come from
    history_override() if set, else from the run's played states that are ancestors of this state."""
    own = _profit_by_year(state, covert)
    cur = state.get("year")
    segs = []                                          # (from year, profit dict), in round order
    for n, y in enumerate(ROUNDS, start=1):
        if cur is not None and y < cur:
            if _HISTORY is not None and y in _HISTORY:
                s = _HISTORY[y]
            else:
                js = _played_state_json(n)
                s = json.loads(js) if js else None
            if s is not None and s.get("year") == y and _is_ancestor(s, state):
                segs.append((y, _profit_by_year(s, covert)))
    if cur is not None:
        segs.append((cur, own))
    out = {}
    for y in own:
        if y < ROUNDS[0]:
            out[y] = 0.0
            continue
        src = own
        for y0, p in segs:
            if y0 <= y:
                src = p
        out[y] = src[y]
    return out


def debt_path(state, v=None, F=None, fcf_scale=1.0, covert=True):
    """Year-by-year net-debt rows for Boeing. `fcf_scale` scales the base free cash flow (the stress case uses
    F['stress_fcf_scale']). `v` is accepted for call compatibility; profits are valued here, as played."""
    F = F or inputs()
    H, tax, rr, cpi = F["historical_level_b"], F["tax_rate"], F["real_rate"], F["cpi"]
    cash = programme_cash(state, F)
    prof = profit_path(state, covert)
    D, Dsq = F["start_debt_b"], F["start_debt_b"]
    rows = []
    for y in range(F["first_year"], M.REPORT_END + 1):
        upl = prof[y]
        spend = sum(cash.get(y, {}).values())
        interest = rr * max(0.0, D - Dsq)
        base = base_fcf(F, y) * fcf_scale
        fcf = base + (1 - tax) * (upl - spend) - interest
        Dr, Dsqr = D / (1 + cpi), Dsq / (1 + cpi)
        D = max(min(Dr, H), Dr - fcf)
        Dsq = max(min(Dsqr, H), Dsqr - base)
        rows.append({"year": y, "base_fcf": base, "profit_vs_baseline": upl, "spend": spend, "interest": interest,
                     "fcf": fcf, "debt": D, "debt_no_programme": Dsq, "items": cash.get(y, {})})
    return rows


def debt_metrics(state, v=None, F=None, stress=False, covert=True):
    F = F or inputs()
    H = F["historical_level_b"]
    rows = debt_path(state, v, F, F["stress_fcf_scale"] if stress else 1.0, covert)
    by = {r["year"]: r for r in rows}
    eps = 1e-6
    first = next((r["year"] for r in rows if r["debt"] <= H + eps), None)
    first_sq = next((r["year"] for r in rows if r["debt_no_programme"] <= H + eps), None)
    held = {y: by[y]["debt"] for y in F["hold_years"]}
    after = [r for r in rows if first is not None and r["year"] > first]
    peak_after = max(after, key=lambda r: r["debt"]) if after else None
    return {"H": H, "target_year": F["target_year"], "first_year": first, "first_year_no_programme": first_sq,
            "reached_by_target": first is not None and first <= F["target_year"],
            "held": held, "held_ok": all(d <= H + eps for d in held.values()),
            "peak_after_first": (peak_after["year"], peak_after["debt"]) if peak_after else None,
            "rows": rows}
