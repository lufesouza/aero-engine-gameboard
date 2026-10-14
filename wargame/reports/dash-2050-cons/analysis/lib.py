"""Shared tools for the fps analyses of run dash-2050-cons (the conservative-case game).

- build(): the 2030 state after Boeing's chosen orders, everyone else's round-1 orders as played (or a brief column).
- grid_items(): Boeing's 2030 fps decision exactly as the brief valued it: the item value (plan minus Do Nothing) in each
  of the six rival-scenario columns, built with briefs.rival_scenarios, valued as briefs.payoff_grid does.
- tests(): Boeing's 2030 decision tests (Board guidance, round 1) applied to those items.
- patched(): a context manager that changes one thing in the market or the programme for the length of a block
  (demand level, growth, fps preference, fps ramp speed, Boeing's total cap, the layer's options, neutral switches).
Every patch is undone on exit, and nothing in the run or the engine is written.
"""
import contextlib
import copy
import os
import sys

DASHGAME = "/home/user/aero-engine-gameboard/wargame/dashgame"
sys.path.insert(0, DASHGAME)
os.environ["DASH_RUN"] = "dash-2050-cons"
import model as M  # noqa: E402
import rules as R  # noqa: E402
import reports as RP  # noqa: E402
import briefs as B  # noqa: E402
import supply_demand as SD  # noqa: E402

YEAR = 2030
S0, REC = RP.jl("state_r0.json"), RP.jl("record_r1.json")
F10 = {"fps": "launch_10yr", "fps_engine_code": 7}
F7 = {"fps": "launch_7yr", "fps_engine_code": 7}
RE787 = {"re787": "launch"}
BASE_OPTIONS = dict(SD.options())
assert BASE_OPTIONS.get("demand_curve"), "run without its sd_options.json"
REAL = {"boeing": SD.boeing_capacity, "airbus": SD.airbus_capacity, "demand": SD.demand, "firm": SD.firm_backlog,
        "base_pref": SD.boeing_base_pref, "options": SD.options}

# Boeing's 2030 tests (Board guidance, round 1, record/exco_result_r1.json): a launch needs more than +$1B in the
# expected column; no Board item below -$1B in any of the six columns; the plan's risk-case column (S6) no more than
# $2B below Do Nothing's. Boeing's CEO expected S2 and S5 at even odds (record_r1.json, expected_scenario).
BUSINESS_CASE, DOWNSIDE, BUFFER = 1.0, -1.0, -2.0
EXPECTED = {1: 0.5, 4: 0.5}          # column index -> weight (S2: NGSA; S5: NGSA + A350 Re-engine)


def build(bo, site="new_site", airbus=None, extra=None, state=None, rec=None, year=YEAR):
    """State after Boeing's orders `bo` at `site`, everyone else as played in round 1 unless `airbus`/`extra` say
    otherwise (airbus: Airbus's full orders; extra: {side: fields to update})."""
    st, rc = (state or S0), (rec or REC)
    o = dict(rc["orders"]["boeing"])
    o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site})
    o.update(bo)
    orders = {k: (o if k == "boeing" else dict(rc["orders"][k])) for k in M.SIDES}
    if airbus is not None:
        orders["airbus"] = dict(airbus)
    for k, v in (extra or {}).items():
        orders[k] = dict(orders[k], **v)
    orders = {k: R.validate(st, k, year, x)[0] for k, x in orders.items()}
    return R.adjudicate(st, year, orders)[0]


def pv(state, covert=True):
    return M.value(state, covert=covert, series=False)["boeing"]["pv_delta"]


def played_item(bo, site="renton"):
    """fps (or other plan) minus Do Nothing, everyone else's round-1 orders as played."""
    return pv(build(bo, site)) - pv(build({}, "new_site"))


SCEN = B.rival_scenarios(S0, "boeing", YEAR)
SCEN_LABELS = [s for s, _ in SCEN]
COVERT = B.sees_covert(S0, "boeing", YEAR)


def _cell(own, so, slab, post=None):
    orders = {k: dict(v) for k, v in so.items()}
    orders["boeing"] = dict(orders.get("boeing", {}), **own)
    s1, _ = R.adjudicate(S0, YEAR, orders)
    if post:
        s1 = post(copy.deepcopy(s1))
    return M.value(s1, covert=(COVERT or slab.startswith("Risk case")), series=False)["boeing"]["pv_delta"]


OWN = {lab: o for lab, o in B.own_options(S0, "boeing", YEAR)}
PLAN_DN = "fps: hold + 787: hold"
PLAN_REN = "fps 10-yr at Renton + 787: hold"
PLAN_NEW = "fps 10-yr + 787: hold"
PLAN_7 = "fps 7-yr + 787: hold"
PLAN_787 = "fps: hold + 787 Re-engine"
assert all(p in OWN for p in (PLAN_DN, PLAN_REN, PLAN_NEW, PLAN_7, PLAN_787)), list(OWN)


def grid_row(plan, post=None):
    return [_cell(OWN[plan], so, slab, post) for slab, so in SCEN]


def grid_states(plan, post=None):
    """The six column states for one plan (for series-level reads)."""
    out = []
    for slab, so in SCEN:
        orders = {k: dict(v) for k, v in so.items()}
        orders["boeing"] = dict(orders.get("boeing", {}), **OWN[plan])
        s1, _ = R.adjudicate(S0, YEAR, orders)
        out.append((post(copy.deepcopy(s1)) if post else s1, COVERT or slab.startswith("Risk case")))
    return out


def grid_items(plan=PLAN_REN, post=None):
    """Item value (plan minus Do Nothing) in each brief column, as the brief valued it."""
    dn = grid_row(PLAN_DN, post)
    row = grid_row(plan, post)
    return [a - b for a, b in zip(row, dn)], row, dn


def expected(items):
    return sum(items[i] * w for i, w in EXPECTED.items())


def margin(items):
    """How far an item is from passing all three tests ($B; >= 0 passes; the business case is strict)."""
    t = tests(items)
    return min(t["expected"] - BUSINESS_CASE, t["worst"] - DOWNSIDE, t["risk_case"] - BUFFER)


def tests(items):
    """Boeing's three value tests on one item's six columns."""
    risk = next(i for i, s in enumerate(SCEN_LABELS) if s.startswith("Risk case"))
    e = expected(items)
    return {"expected": e, "worst": min(items), "risk_case": items[risk],
            "business_case": e > BUSINESS_CASE, "downside": min(items) >= DOWNSIDE, "buffer": items[risk] >= BUFFER,
            "passes": e > BUSINESS_CASE and min(items) >= DOWNSIDE and items[risk] >= BUFFER}


# ─────────────────────────────── patches ───────────────────────────────
def _unl(key):
    def f(s, y):
        r = SD._live(s, key)
        return (0.0, 1e9) if (r and y >= r["eis"]) else (1e9, 0.0)
    return f


def cap_with(ramp):
    """supply_demand.boeing_capacity with the fps output (and the Renton wind-down) taken from `ramp`; with
    ramp_exact() it is the game's own function, line for line."""
    def g(state, year):
        b = SD.inputs()["boeing"]
        m = SD.max_path(year)
        hike = b["rate_increase_per_year"] if (state.get("rate737") and year >= b["rate_increase_from"]) else 0.0
        fps = SD._live(state, "fps")
        if not fps:
            return m + hike, 0.0
        shift = fps["eis"] - SD.CHART_YEAR
        f, keep = ramp(fps["eis"], shift, year)
        f *= b.get("fps_ramp_scale", 1.0)
        if SD.plans(state)[1] == "renton":
            m = max(min(m, 12.0 * b["everett_rate"]), m - min(m, 12.0 * b["renton_rate"]) * (1.0 - keep))
            hike *= keep
        mx = m + hike
        cap = 12.0 * b["total_rate_cap"]
        tail = min(mx, 12.0 * b["max_tail_rate"]) if year <= b["max_last_year"] else 0.0
        f = min(f, max(0.0, cap - tail))
        mx = min(mx, max(0.0, cap - f))
        if year > b["max_last_year"]:
            mx = min(mx, max(0.0, SD.fps_full() - f))
        return mx, f
    return g


def _avg(fn, a, b):
    """Average of a function of whole years over chart time [a, b): each year z counts for its overlap with it."""
    tot, z = 0.0, int(a // 1)
    while z < b:
        ov = min(b, z + 1) - max(a, z)
        if ov > 0:
            tot += fn(z) * ov
        z += 1
    return tot / (b - a)


def compressed(k):
    """The fps ramp (the NGSA chart moved to the fps entry into service) run k times faster, k >= 1 real: calendar
    year y after entry into service gets the chart's average output over chart time [eis + k(y - eis), eis + k(y - eis + 1)),
    and the Renton wind-down runs at the same speed. k = 1 is the game's own ramp."""
    def ramp(eis, shift, y):
        if y < eis:
            return SD._annual("ngsa", shift, y), SD._rundown("a320_base", shift, y) / SD.a320_full()
        a, b = eis + k * (y - eis), eis + k * (y - eis + 1)
        f = _avg(lambda z: SD._annual("ngsa", shift, z), a, b)
        keep = _avg(lambda z: SD._rundown("a320_base", shift, z), a, b) / SD.a320_full()
        return f, keep
    return ramp


def ramp_exact():
    """The game's own ramp (for the check that cap_with reproduces supply_demand.boeing_capacity)."""
    def ramp(eis, shift, y):
        return SD._annual("ngsa", shift, y), SD._rundown("a320_base", shift, y) / SD.a320_full()
    return ramp


def instant(eis, shift, y):
    return (SD.fps_full(), 0.0) if y >= eis else (0.0, 1.0)


@contextlib.contextmanager
def patched(demand_k=None, growth_k=None, fps_pref_pp=None, ramp=None, total_cap=None, options=None, neutral=(),
            dn_pref_pp_extra=None):
    """Change the market or the programme inside a with-block.
    demand_k: the whole demand curve times k. growth_k: only the curve's growth part times k.
    fps_pref_pp: Boeing's base preference raised by that many points while an fps is in service.
    ramp / total_cap: Boeing's capacity from cap_with(ramp, total_cap).
    options: {key: value or None} changes to the run's sd_options (None removes the option).
    neutral: any of 'boeing', 'airbus', 'demand', 'firm' switched to the dashboard's world (unlimited factories, 2,000
    aircraft a year, no firm orders)."""
    saved_inputs = copy.deepcopy(SD.inputs())
    try:
        if options is not None:
            o = dict(BASE_OPTIONS)
            for k, v in options.items():
                if v is None:
                    o.pop(k, None)
                else:
                    o[k] = v
            SD.options = lambda: o
            SD._curve.cache_clear()
        base_demand = SD.demand
        if demand_k is not None:
            SD.demand = lambda y, f=base_demand: f(y) * demand_k
        if growth_k is not None:
            g0 = SD.growth
            SD.demand = lambda y, f=SD.demand: f(y) + (growth_k - 1.0) * g0(y)
        if ramp is not None:
            SD.boeing_capacity = cap_with(ramp)
        if total_cap is not None:
            SD.inputs()["boeing"]["total_rate_cap"] = float(total_cap)
        if fps_pref_pp is not None:
            bp = SD.boeing_base_pref
            def pref(state, year, board_pref, f=bp):
                p = f(state, year, board_pref)
                fps = SD._live(state, "fps")
                return min(1.0, p + fps_pref_pp / 100.0) if (fps and year >= fps["eis"]) else p
            SD.boeing_base_pref = pref
        if "boeing" in neutral:
            SD.boeing_capacity = _unl("fps")
        if "airbus" in neutral:
            SD.airbus_capacity = _unl("ngsa")
        if "demand" in neutral:
            SD.demand = lambda y: 2000.0
        if "firm" in neutral:
            SD.firm_backlog = lambda: (0.0, 0.0)
        yield
    finally:
        SD.boeing_capacity, SD.airbus_capacity, SD.demand, SD.firm_backlog = REAL["boeing"], REAL["airbus"], REAL["demand"], REAL["firm"]
        SD.boeing_base_pref, SD.options = REAL["base_pref"], REAL["options"]
        SD.inputs().clear()
        SD.inputs().update(saved_inputs)
        SD._curve.cache_clear()
        SD._annual.cache_clear()


def bisect(f, lo, hi, target=0.0, tol=1e-4, it=60):
    """x in [lo, hi] where f(x) crosses `target` (f monotone between them); None if it does not cross."""
    flo, fhi = f(lo) - target, f(hi) - target
    if flo * fhi > 0:
        return None
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if abs(hi - lo) < tol:
            break
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2
