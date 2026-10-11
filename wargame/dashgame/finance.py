"""Boeing balance-sheet tracker for the dash-2050 game (game master only).

It scores Control's objective "repair the balance sheet: debt back to historical levels". It never changes a payoff:
the board's ΔPV, including its own debt penalty on $45B of debt, is untouched.

Debt is net debt (total debt minus cash and short-term investments) at year end, in constant 2026 dollars like the
board. Each year:

    free cash   = base free cash flow (analyst models, see finance_inputs.json)
                + (1 - tax) x (Boeing operating profit - game baseline profit)     # what the game adds or takes away
                - programme cash spend (each bill phased over its development years)
                - real interest on the debt the game has added above the no-programme path
    debt        = previous debt - free cash, but never below the historical level once there: from then on surplus
                  cash goes to the owners (dividends, buybacks), as Boeing's Board reserves for itself.

The game baseline is the board's status quo (no one launches a new programme). The no-programme path ("debt_sq") is
the same recursion with base free cash flow only.
"""
import json
import os

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS_PATH = os.path.join(HERE, "finance_inputs.json")


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
    (launch to EIS - 1) on the planning curve; a cancelled programme stops spending in its cancel year."""
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
    if state.get("rate737"):
        p = M.af_params()
        y0 = state["rate737"]["launch"]
        yrs = list(range(y0, 2033))            # the board books the rate increase in 2032
        for y in yrs:
            put(y, "737 rate increase", p["v_capex_737_rate_hike"] / len(yrs))
    return out


def base_fcf(F, y):
    b = F["base_fcf_b"]
    if str(y) in b:
        return b[str(y)]
    last = max(int(k) for k in b)
    return F["base_fcf_after_b"] if y > last else b[str(min(int(k) for k in b))]


def debt_path(state, v, F=None, fcf_scale=1.0):
    """Year-by-year debt rows for Boeing, from the valuation `v` of `state` (needs v['_af_series']). `fcf_scale`
    scales the base free cash flow (the stress case uses F['stress_fcf_scale'])."""
    F = F or inputs()
    H, tax, rr = F["historical_level_b"], F["tax_rate"], F["real_rate"]
    cash = programme_cash(state, F)
    prof = {r["year"]: r["boeing"] for r in v["_af_series"]["years"]}
    D, Dsq = F["start_debt_b"], F["start_debt_b"]
    rows = []
    for y in range(F["first_year"], M.REPORT_END + 1):
        x = prof[y]
        upl = (x["nb_profit"] + x["wb_profit"]) - (x["sq_nb_profit"] + x["sq_wb_profit"])
        spend = sum(cash.get(y, {}).values())
        interest = rr * max(0.0, D - Dsq)
        base = base_fcf(F, y) * fcf_scale
        fcf = base + (1 - tax) * upl - spend - interest
        D = max(min(D, H), D - fcf)
        Dsq = max(min(Dsq, H), Dsq - base)
        rows.append({"year": y, "base_fcf": base, "profit_vs_baseline": upl, "spend": spend, "interest": interest,
                     "fcf": fcf, "debt": D, "debt_no_programme": Dsq, "items": cash.get(y, {})})
    return rows


def debt_metrics(state, v, F=None, stress=False):
    F = F or inputs()
    H = F["historical_level_b"]
    rows = debt_path(state, v, F, F["stress_fcf_scale"] if stress else 1.0)
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
