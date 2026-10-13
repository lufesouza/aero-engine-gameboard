"""Supply and demand: the game master's narrowbody layer for runs that switch it on (runs/<run>/supply_demand.txt).

The board sells a fixed 2,000 narrowbodies a year, split by its share rules, and books every one. This layer keeps
the board's shares as each customer's *preference*, but delivers only what the factories can build:

  demand(y)        = growth + older types' replacement(y) + today's fleets' replacement(y)
                     (supply_demand.json: growth is 56% of the board's 2,000 a year, Airbus GMF 2025; the older 737NG /
                     A320ceo fleets' replacement runs down to nothing in 2050; today's MAX, A320neo and A220 fleets'
                     replacement is the user's Cirium page; 2026-2045 averages the board's 2,000 a year)
  wanted_X(y)      = preference share_X(y) x demand(y)
  delivered_X(y)   = min(capacity_X(y), wanted_X(y) + backlog_X) + spill in
  spill X -> Y     = min(flex x unmet_X, spare_Y)   (flexible customers: airlines flying both types, lessors and
                                                     unannounced customers take the other maker's free slots)
  backlog_X(y+1)   = (unmet_X - spill out) x (1 - lapse)   (a tenth of the waiting customers drop out each year)

Capacity, aircraft a year:
- Airbus: A320 at 85 a month until NGSA enters service, then the Rev. B rundown (base or Alt) and the NGSA ramp to
  100 a month, both read off the user's chart and shifted with the NGSA date. No NGSA: A320 stays at 85.
- Boeing: 737 MAX on Boeing's stated path (42.5, 49.5, 52, 54.5, then 57 a month from 2030); the 737 rate increase
  adds the board's 100 a year from 2032 while the MAX is built. The fps ramps like NGSA (the chart's shape, shifted to
  the fps date). Boeing's single-aisle total is capped at 100 a month (Airbus's Rev. B peak): as the fps fills it the
  MAX gives way, down to the Everett tail of 10 a month. New sites: the MAX carries on at Renton and Everett. Renton
  reassigned to the fps: the Renton MAX lines (47 a month, with the rate increase that rides on them) wind down like the
  A320 base plan and the Everett North Line carries on at up to 15 a month, saving the new-site capex (pro-rated if
  the switch comes late). After 2050 the MAX builds only what the fps cannot yet (it tops Boeing up to the fps's full
  rate while the fps ramps); with no fps the MAX carries on.

Pricing: new-type aircraft (fps, NGSA) are delivered first, up to their line's capacity, at the board's new-type
price and margin; the rest are 737 MAX or A320neo at the legacy price and margin. The status quo (no new programme
anywhere) runs the same rules with today's capacity and the board's 40/60 split. With unlimited capacity and demand
of 2,000 a year the layer changes nothing (test_supply_demand.py).
"""
import functools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "supply_demand.json")
CHART_YEAR = 2037              # NGSA entry-into-service year of the chart (mid-2037)
NB_BOARD = 2000.0
FAL_BUILD_YEARS = 3            # a final assembly site takes about 2-4 years to build (research notes)


@functools.lru_cache(maxsize=None)
def inputs():
    with open(PATH) as f:
        return json.load(f)


def reload():
    """Forget cached inputs and curves (for in-process sensitivities that edit supply_demand.json)."""
    inputs.cache_clear()
    _annual.cache_clear()


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


def a320_full():
    return 12.0 * inputs()["airbus"]["a320_rate_no_ngsa"]


def _rundown(curve, shift, year):
    """A320 output on the chart curve, flat at 85 a month before the rundown (the chart's 2025 ramp is not used)."""
    if year < CHART_YEAR - 1 + shift:
        return a320_full()
    return _annual(curve, shift, year)


def demand(year):
    d = inputs()["demand"]
    ys, rep = d["years"], d["replacements"]
    y = min(max(year, ys[0]), ys[-1])          # after 2075 the replacement wave is held at its 2075 value
    older = max(0.0, d["older_2026"] * (1.0 - (year - 2026) / (d["older_end_year"] - 2026)))
    return d["growth_per_year"] + older + rep[ys.index(y)]


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
        return a320_full(), 0.0
    shift = ngsa["eis"] - CHART_YEAR
    plan = plans(state)[0]
    return _rundown("a320_alt" if plan == "alt" else "a320_base", shift, year), _annual("ngsa", shift, year)


def max_path(year):
    b = inputs()["boeing"]
    return 12.0 * b["max_rate"].get(str(year), b["max_rate_after"])


def fps_full():
    b = inputs()["boeing"]
    return 12.0 * max(r for _, r in inputs()["airbus"]["ngsa"]) * b.get("fps_ramp_scale", 1.0)


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
        # Renton's MAX lines (up to renton_rate a month) wind down like the A320 base plan as the fps ramps up there,
        # and the rate increase rides on them; the Everett North Line carries on, up to its own capacity
        keep = _rundown("a320_base", shift, year) / a320_full()
        m = max(min(m, 12.0 * b["everett_rate"]), m - min(m, 12.0 * b["renton_rate"]) * (1.0 - keep))
        hike *= keep
    mx = m + hike
    # Boeing's single-aisle total is capped; the fps fills it first and the MAX keeps at least its Everett tail
    cap = 12.0 * b["total_rate_cap"]
    tail = min(mx, 12.0 * b["max_tail_rate"]) if year <= b["max_last_year"] else 0.0
    f = min(f, max(0.0, cap - tail))
    mx = min(mx, max(0.0, cap - f))
    if year > b["max_last_year"]:
        mx = min(mx, max(0.0, fps_full() - f))        # after 2050 the MAX only tops Boeing up while the fps ramps
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
        # new types are delivered first, up to their own line's capacity; the rest are today's types
        r["dlv_fps"] = min(r["delivered_b"], fb)
        r["dlv_max"] = r["delivered_b"] - r["dlv_fps"]
        r["dlv_ngsa"] = min(r["delivered_a"], ng)
        r["dlv_a320"] = r["delivered_a"] - r["dlv_ngsa"]
        bb, ba = r["backlog_b"], r["backlog_a"]
        out[y] = r
    return out


def renton_share(state):
    """Share of the Renton saving Boeing still gets: full if Renton was chosen at least FAL_BUILD_YEARS before the
    fps entry into service (no new site built yet), pro-rated if later."""
    fps = _live(state, "fps")
    if not fps or plans(state)[1] != "renton":
        return 0.0
    since = (state.get("sd") or {}).get("fps_site_year") or fps["launch"]
    return max(0.0, min(1.0, (fps["eis"] - since) / FAL_BUILD_YEARS))


def costs(state):
    """GM costs of the supply plans: [(side, year, item, $B nominal)]. Negative = a saving."""
    b, a = inputs()["boeing"], inputs()["airbus"]
    out = []
    ngsa, fps = _live(state, "ngsa"), _live(state, "fps")
    a320, site = plans(state)
    if ngsa and a320 == "alt":
        out.append(("airbus", ngsa["eis"], "A320 Alt plan (lines kept longer)", a["alt_cost_b"]))
    sh = renton_share(state)
    if sh > 0:
        out.append(("boeing", fps["eis"], "fps at Renton: new-site capex avoided", -b["renton_saving_b"] * sh))
    return out


def apply(state, rows, waccs):
    """Re-deliver the airframer series rows (from model.af_series) under supply and demand, in place.
    Returns ({side: {"supply_demand": PV $B, "supply_plan": PV $B}}, cost items, scenario rows, status-quo rows)."""
    years = [r["year"] for r in rows]
    pref = {r["year"]: r["boeing"]["nb_share"] for r in rows}
    sc = year_rows(state, pref, years)
    sq = year_rows(sq_state(), {y: 0.40 for y in years}, years)
    adj = {"boeing": 0.0, "airbus": 0.0}
    for r in rows:
        y = r["year"]
        s, q = sc[y], sq[y]
        for side, pre, sq_sh, new, old in (("boeing", "b", 0.40, "fps", "max"), ("airbus", "a", 0.60, "ngsa", "a320")):
            x = r[side]
            sq_unit = x["sq_nb_profit"] / (NB_BOARD * sq_sh)           # legacy (737 MAX / A320neo) profit per aircraft
            new_unit = x["nb_price"] / 1000.0 * x["nb_margin"]         # the board's unit in this year (new type from EIS)
            n_new, n_old = s["dlv_" + new], s["dlv_" + old]
            x["board_nb_units"], x["board_nb_profit"], x["board_sq_nb_profit"] = x["nb_units"], x["nb_profit"], x["sq_nb_profit"]
            x["board_nb_revenue"] = x["nb_revenue"]
            legacy_price = x["legacy_nb_price"]                         # $M per aircraft
            x["nb_units"] = n_new + n_old
            x["nb_units_new"], x["nb_units_old"] = n_new, n_old
            x["nb_revenue"] = (n_new * x["nb_price"] + n_old * legacy_price) / 1000.0
            x["nb_profit"] = n_new * new_unit + n_old * sq_unit
            sq_dlv = q["delivered_" + pre]
            x["sq_nb_units"] = sq_dlv
            x["sq_nb_profit"] = sq_dlv * sq_unit
            x["nb_delivered_share"] = (n_new + n_old) / max(1e-9, s["delivered_a"] + s["delivered_b"])
            x["nb_pref_share"] = x["nb_share"]                        # the board's share: what customers want
            x["nb_share"] = x["nb_delivered_share"]                   # market share = share of deliveries
            x["sd"] = {"demand": s["demand"], "wanted": s["wanted_" + pre], "capacity": s["cap_" + pre],
                       "backlog_in": s["backlog_in_" + pre], "backlog_out": s["backlog_" + pre],
                       "spill_in": s["spill_to_" + pre], "sq_delivered": sq_dlv, "sq_capacity": q["cap_" + pre],
                       "new_units": n_new, "old_units": n_old}
            if x["nb_in_window"]:
                adj[side] += ((x["nb_profit"] - x["board_nb_profit"]) - (x["sq_nb_profit"] - x["board_sq_nb_profit"])) * r["df_" + pre]
        r["sd"] = {k: s[k] for k in ("demand", "cap_max", "cap_fps", "cap_a320", "cap_ngsa", "lost", "backlog_b", "backlog_a",
                                     "dlv_max", "dlv_fps", "dlv_a320", "dlv_ngsa")}
        r["sd_sq"] = {"delivered_b": q["delivered_b"], "delivered_a": q["delivered_a"], "lost": q["lost"],
                      "dlv_max": q["dlv_max"], "dlv_a320": q["dlv_a320"]}
    plan = {"boeing": 0.0, "airbus": 0.0}
    items = []
    for side, y, item, x in costs(state):
        plan[side] -= x / ((1 + waccs[side]) ** (y - 2026))
        items.append((side, y, item, x))
    return {side: {"supply_demand": adj[side], "supply_plan": plan[side]} for side in adj}, items, sc, sq
