"""Supply and demand: the game master's narrowbody layer for runs that switch it on (runs/<run>/supply_demand.txt).

The board sells a fixed 2,000 narrowbodies a year, split by its share rules, and books every one. This layer keeps
the board's shares as each customer's *preference* and its unit price and margin, but delivers only what the
factories can build:

  demand(y)        = base + replacements(y)        (supply_demand.json: base makes 2026-2045 average 2,000 a year;
                                                     replacements of today's MAX, A320neo and A220 fleets, Cirium)
  wanted_X(y)      = preference share_X(y) x demand(y)
  delivered_X(y)   = min(capacity_X(y), wanted_X(y) + backlog_X) + spill in
  spill X -> Y     = min(flex x unmet_X, spare_Y)   (flex: customers flying both types, lessors, unannounced
                                                     customers take the other maker's free slots; the rest wait)
  backlog_X(y+1)   = (unmet_X - spill out) x (1 - lapse)   (a fifth of the waiting customers give up each year:
                                                     they keep old aircraft longer or defer growth)

Capacity, aircraft a year:
- Airbus: A320 at 85 a month until NGSA enters service, then the Rev. B rundown (base or Alt) and the NGSA ramp to
  100 a month, both read off the user's chart and shifted with the NGSA date. No NGSA: A320 stays at 85.
- Boeing: 737 MAX on Boeing's stated path (42.5, 49.5, 52, 54.5, then 57 a month from 2030); the 737 rate increase
  adds the board's 100 a year from 2032. fps at new sites ramps like NGSA (the same chart shape, shifted to the fps date) while the MAX
  carries on to 2050. With Renton reassigned to fps, the Renton MAX lines (47 a month) run down like the A320 base plan
  and the Everett North Line carries on to 2050 at up to 15 a month. With fps in service by 2050 the MAX stops after 2050; without fps it carries on.

The status quo (no new programme anywhere) runs the same rules with today's capacity and the board's 40/60 split.
The value change is priced with the board's own per-year unit price and margin, inside the board's windows, so with
unlimited capacity and demand of 2,000 a year the layer changes nothing (test_supply_demand.py).
"""
import functools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "supply_demand.json")
CHART_YEAR = 2037              # NGSA entry-into-service year of the chart (mid-2037)
NB_BOARD = 2000.0


@functools.lru_cache(maxsize=None)
def inputs():
    with open(PATH) as f:
        return json.load(f)


def _interp(pts, x):
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y1 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


@functools.lru_cache(maxsize=None)
def _annual(curve, shift, year):
    """Aircraft built in calendar `year` on a chart curve (rate a month) moved `shift` years later."""
    pts = inputs()["airbus"][curve]
    n = 48
    return sum(_interp(pts, year - shift + (k + 0.5) / n) for k in range(n)) / n * 12.0


def _rundown(curve, shift, year):
    """A320 output on the chart curve, flat at 85 a month before the rundown (the chart's 2025 ramp is not used)."""
    if year < CHART_YEAR - 1 + shift:
        return 85 * 12.0
    return _annual(curve, shift, year)


def demand(year):
    d = inputs()["demand"]
    ys, rep = d["years"], d["replacements"]
    y = min(max(year, ys[0]), ys[-1])
    return d["base_per_year"] + rep[ys.index(y)]


def flex():
    return inputs()["demand"]["flex_share"]


def _live(state, key):
    r = state["prog"].get(key)
    return r if (r and r.get("cancel") is None) else None


def plans(state):
    sd = state.get("sd") or {}
    return sd.get("a320_plan", "base"), sd.get("fps_site", "new_site")


def airbus_capacity(state, year):
    """(A320, NGSA) aircraft in `year`."""
    ngsa = _live(state, "ngsa")
    if not ngsa:
        return 85 * 12.0, 0.0
    shift = ngsa["eis"] - CHART_YEAR
    plan = plans(state)[0]
    return _rundown("a320_alt" if plan == "alt" else "a320_base", shift, year), _annual("ngsa", shift, year)


def max_path(year):
    b = inputs()["boeing"]
    return 12.0 * b["max_rate"].get(str(year), b["max_rate_after"])


def boeing_capacity(state, year):
    """(737 MAX, fps) aircraft in `year`."""
    b = inputs()["boeing"]
    m = max_path(year)
    hike = b["rate_increase_per_year"] if (state.get("rate737") and year >= b["rate_increase_from"]) else 0.0
    fps = _live(state, "fps")
    if not fps:
        return m + hike, 0.0
    shift = fps["eis"] - CHART_YEAR
    f = _annual("ngsa", shift, year) * b.get("fps_ramp_scale", 1.0)
    if plans(state)[1] == "renton":
        # Renton's MAX lines (up to renton_rate a month) wind down like the A320 base plan as the fps ramps up there;
        # the Everett North Line carries on and can rise to its own capacity (everett_rate a month)
        keep = _rundown("a320_base", shift, year) / (85 * 12.0)
        m = max(min(m, 12.0 * b["everett_rate"]), m - min(m, 12.0 * b["renton_rate"]) * (1.0 - keep))
    mx = m + hike
    if fps["eis"] <= b["max_last_year"] and year > b["max_last_year"]:
        mx = 0.0
    return mx, f


def deliveries(b_pref, d, cap_b, cap_a, fx, back_b=0.0, back_a=0.0, lapse=0.0):
    """One year's market: preference share of Boeing, demand, capacities, flexible share and the backlogs waiting
    from earlier years -> delivered, spill and the backlogs carried into next year (after the lapse)."""
    wb, wa = b_pref * d, (1.0 - b_pref) * d
    qb, qa = min(wb + back_b, cap_b), min(wa + back_a, cap_a)
    ub, ua = wb + back_b - qb, wa + back_a - qa
    to_b = min(fx * ua, cap_b - qb)
    to_a = min(fx * ub, cap_a - qa)
    nb, na = (ub - to_a) * (1.0 - lapse), (ua - to_b) * (1.0 - lapse)
    return {"demand": d, "wanted_b": wb, "wanted_a": wa, "cap_b": cap_b, "cap_a": cap_a,
            "backlog_in_b": back_b, "backlog_in_a": back_a,
            "delivered_b": qb + to_b, "delivered_a": qa + to_a, "spill_to_b": to_b, "spill_to_a": to_a,
            "backlog_b": nb, "backlog_a": na, "lost": (ub - to_a + ua - to_b) * lapse}


def sq_state():
    return {"prog": {}, "rate737": None, "sd": {}}


def year_rows(state, b_pref_by_year, years):
    out = {}
    fx, lapse = flex(), inputs()["demand"]["lapse_per_year"]
    bb, ba = 0.0, 0.0
    for y in sorted(years):
        mb, fb = boeing_capacity(state, y)
        a3, ng = airbus_capacity(state, y)
        r = deliveries(b_pref_by_year[y], demand(y), mb + fb, a3 + ng, fx, bb, ba, lapse)
        r.update({"cap_max": mb, "cap_fps": fb, "cap_a320": a3, "cap_ngsa": ng})
        bb, ba = r["backlog_b"], r["backlog_a"]
        out[y] = r
    return out


def costs(state):
    """GM costs of the supply plans: [(side, year, item, $B nominal)]. Negative = a saving."""
    b, a = inputs()["boeing"], inputs()["airbus"]
    out = []
    ngsa, fps = _live(state, "ngsa"), _live(state, "fps")
    a320, site = plans(state)
    if ngsa and a320 == "alt":
        out.append(("airbus", ngsa["eis"], "A320 Alt plan (lines kept longer)", a["alt_cost_b"]))
    if fps and site == "renton":
        out.append(("boeing", fps["eis"], "fps at Renton: new-site capex avoided", -b["renton_saving_b"]))
    return out


def apply(state, rows, waccs):
    """Re-deliver the airframer series rows (from model.af_series) under supply and demand, in place.
    Returns {side: {"supply_demand": PV $B, "supply_plan": PV $B}} to add to each side's bridge."""
    years = [r["year"] for r in rows]
    pref = {r["year"]: r["boeing"]["nb_share"] for r in rows}
    sc = year_rows(state, pref, years)
    sq = year_rows(sq_state(), {y: 0.40 for y in years}, years)
    adj = {"boeing": 0.0, "airbus": 0.0}
    for r in rows:
        y = r["year"]
        s, q = sc[y], sq[y]
        for side, pre, sq_sh in (("boeing", "b", 0.40), ("airbus", "a", 0.60)):
            x = r[side]
            unit = x["nb_price"] / 1000.0 * x["nb_margin"]          # $B profit per aircraft, the board's mix
            sq_unit = x["sq_nb_profit"] / (NB_BOARD * sq_sh)
            dlv = s["delivered_" + pre]
            sq_dlv = q["delivered_" + pre]
            x["board_nb_units"], x["board_nb_profit"], x["board_sq_nb_profit"] = x["nb_units"], x["nb_profit"], x["sq_nb_profit"]
            x["nb_units"] = dlv
            x["nb_revenue"] = dlv * x["nb_price"] / 1000.0
            x["nb_profit"] = dlv * unit
            x["sq_nb_units"] = sq_dlv
            x["sq_nb_profit"] = sq_dlv * sq_unit
            x["nb_delivered_share"] = dlv / max(1e-9, s["delivered_a"] + s["delivered_b"])
            x["nb_pref_share"] = x["nb_share"]                        # the board's share: what customers want
            x["nb_share"] = x["nb_delivered_share"]                   # market share = share of deliveries
            x["sd"] = {"demand": s["demand"], "wanted": s["wanted_" + pre], "capacity": s["cap_" + pre],
                       "backlog_in": s["backlog_in_" + pre], "backlog_out": s["backlog_" + pre],
                       "spill_in": s["spill_to_" + pre], "sq_delivered": sq_dlv, "sq_capacity": q["cap_" + pre]}
            if x["nb_in_window"]:
                adj[side] += ((x["nb_profit"] - x["board_nb_profit"]) - (x["sq_nb_profit"] - x["board_sq_nb_profit"])) * r["df_" + pre]
        r["sd"] = {k: s[k] for k in ("demand", "cap_max", "cap_fps", "cap_a320", "cap_ngsa", "lost", "backlog_b", "backlog_a")}
        r["sd_sq"] = {"delivered_b": q["delivered_b"], "delivered_a": q["delivered_a"], "lost": q["lost"]}
    plan = {"boeing": 0.0, "airbus": 0.0}
    items = []
    for side, y, item, x in costs(state):
        plan[side] -= x / ((1 + waccs[side]) ** (y - 2026))
        items.append((side, y, item, x))
    return {side: {"supply_demand": adj[side], "supply_plan": plan[side]} for side in adj}, items, sc, sq
