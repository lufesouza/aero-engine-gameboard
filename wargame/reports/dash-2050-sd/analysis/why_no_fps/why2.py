"""Second pass: Shapley attribution, dashboard-only items by round, proper fast-ramp levers, Airbus ceiling only,
the value of the fps's extra capacity."""
import itertools, json, math, os, sys
sys.path.insert(0, "/home/user/aero-engine-gameboard/wargame/dashgame")
os.environ["DASH_RUN"] = "dash-2050-sd"
import model as M, rules as R, reports as RP, supply_demand as SD

REAL = {"boeing": SD.boeing_capacity, "airbus": SD.airbus_capacity, "demand": SD.demand, "firm": SD.firm_backlog}
def restore():
    SD.boeing_capacity, SD.airbus_capacity, SD.demand, SD.firm_backlog = REAL["boeing"], REAL["airbus"], REAL["demand"], REAL["firm"]

def play(n, bo, site="new_site"):
    prev, rec = RP.jl("state_r%d.json" % (n - 1)), RP.jl("record_r%d.json" % n)
    o = dict(rec["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    if "rate_737" in o and o.get("rate_737") not in (None, "hold"): o["rate_737"] = "hold"
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(prev, k, rec["year"], x)[0] for k, x in orders.items()}
    return R.adjudicate(prev, rec["year"], orders)[0]

F10 = {"fps": "launch_10yr", "fps_engine_code": 7}
F7 = {"fps": "launch_7yr", "fps_engine_code": 7}
ST = {("hold", 1): play(1, {}), ("f10", 1): play(1, F10), ("f10r", 1): play(1, F10, "renton"), ("f7", 1): play(1, F7), ("f7r", 1): play(1, F7, "renton")}
pv = lambda s: M.value(s, covert=True)["boeing"]["pv_delta"]
item = lambda key, n=1: pv(ST[(key, n)]) - pv(ST[("hold", n)])

def unl(key):
    def f(s, y):
        r = SD._live(s, key)
        return (0.0, 1e9) if (r and y >= r["eis"]) else (1e9, 0.0)
    return f
NEUTRAL = {"boeing": unl("fps"), "airbus": unl("ngsa"), "demand": lambda y: 2000.0, "firm": lambda: (0.0, 0.0)}
COMP = ["demand", "firm", "airbus", "boeing"]
def setc(on):
    for c in COMP:
        src = REAL if c in on else NEUTRAL
        if c == "boeing": SD.boeing_capacity = src[c]
        elif c == "airbus": SD.airbus_capacity = src[c]
        elif c == "demand": SD.demand = src[c]
        else: SD.firm_backlog = src[c]

out = {}
# ---- 1. Shapley over the 16 combinations (2030 decision; 10-year and 7-year, new sites)
for key in ("f10", "f7"):
    val = {}
    for r in range(5):
        for on in itertools.combinations(COMP, r):
            setc(set(on)); val[frozenset(on)] = item(key)
    restore()
    sh = {}
    for c in COMP:
        tot = 0.0
        for r in range(4):
            for S in itertools.combinations([x for x in COMP if x != c], r):
                S = frozenset(S)
                w = math.factorial(len(S)) * math.factorial(len(COMP) - len(S) - 1) / math.factorial(len(COMP))
                tot += w * (val[S | {c}] - val[S])
        sh[c] = tot
    out["shapley_" + key] = {"neutral": val[frozenset()], "full": val[frozenset(COMP)], "shares": sh,
                             "demand_effect_range": [min(val[S | {"demand"}] - val[S] for S in val if "demand" not in S),
                                                     max(val[S | {"demand"}] - val[S] for S in val if "demand" not in S)]}

# ---- 2. dashboard-only and layer items by round (10-year, best site), others as played
rows = []
for n in (1, 2, 3, 4):
    ST[("hold", n)] = ST.get(("hold", n)) or play(n, {})
    ST[("f10", n)] = ST.get(("f10", n)) or play(n, F10)
    ST[("f10r", n)] = ST.get(("f10r", n)) or play(n, F10, "renton")
    lay = max(item("f10", n), item("f10r", n))
    M.SD_ON = False
    dash = max(item("f10", n), item("f10r", n))
    M.SD_ON = True
    rows.append({"round": n, "year": RP.jl("record_r%d.json" % n)["year"], "dashboard": dash, "layer": lay, "penalty": lay - dash})
out["by_round"] = rows

# ---- 3. levers with a proper k-times time compression of the fps ramp (and of the Renton wind-down)
def cap_with(ramp):
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
def compressed(k):
    def ramp(eis, shift, y):
        if y < eis - 1:
            return 0.0, 1.0
        ys = [eis + k * (y - eis) + j for j in range(k)] if y >= eis else [y]
        f = sum(SD._annual("ngsa", shift, z) for z in ys) / len(ys)
        keep = sum(SD._rundown("a320_base", shift, z) for z in ys) / len(ys) / SD.a320_full()
        return (f if y >= eis else SD._annual("ngsa", shift, y)), keep
    return ramp
def instant(eis, shift, y):
    return (SD.fps_full(), 0.0) if y >= eis else (0.0, 1.0)
# sanity: k=1 must reproduce the real capacity
SD.boeing_capacity = cap_with(compressed(1))
chk = max(abs(a - b) for s in (ST[("f10", 1)], ST[("f10r", 1)]) for y in range(2026, 2080)
          for a, b in zip(SD.boeing_capacity(s, y), REAL["boeing"](s, y)))
restore()
best = lambda: max((item("f10"), "new sites"), (item("f10r"), "Renton"))
lev = [("As played", best())]
for lab, fn in (("ramp twice as fast", cap_with(compressed(2))), ("ramp three times as fast", cap_with(compressed(3))),
                ("full rate from entry into service (under the 100-a-month cap)", cap_with(instant))):
    SD.boeing_capacity = fn
    lev.append((lab, best()))
    restore()
out["k1_check_max_abs_diff"] = chk
out["levers"] = [{"lever": l, "item": v, "site": s} for l, (v, s) in lev]
# with growth x1.5 combined
import copy
saved = copy.deepcopy(SD.inputs())
SD.inputs()["demand"]["growth"] = {k: x * 1.5 for k, x in SD.inputs()["demand"]["growth"].items()}
lev2 = [("growth x1.5", best())]
SD.boeing_capacity = cap_with(compressed(2)); lev2.append(("ramp twice as fast + growth x1.5", best())); restore()
SD.inputs().clear(); SD.inputs().update(saved); SD._annual.cache_clear()
out["levers"] += [{"lever": l, "item": v, "site": s} for l, (v, s) in lev2]

# ---- 4. Airbus: ceiling only, dip only, both
def airbus_mod(no_ceiling, no_dip):
    def g(state, y):
        a3, ng = REAL["airbus"](state, y)
        if no_ceiling and SD._live(state, "ngsa") and a3 < 1 and ng >= 1199.5:
            ng = 1e9
        if no_dip and y <= 2045 and a3 + ng < SD.a320_full():
            a3 = SD.a320_full() - ng
        return a3, ng
    return g
air = {}
for lab, nc, nd in (("no ceiling (NGSA unlimited once at 100 a month)", True, False), ("no transition dip (Airbus at least 85 a month to 2045)", False, True), ("neither", True, True)):
    SD.airbus_capacity = airbus_mod(nc, nd)
    air[lab] = {"fps_minus_hold": item("f10"), "hold": pv(ST[("hold", 1)])}
    restore()
out["airbus_cases"] = air
# ---- 5. value of the fps's extra capacity: Boeing's total held to the no-fps MAX path
def no_extra(state, y):
    mx, f = REAL["boeing"](state, y)
    lim = SD.max_path(y)
    tot = min(mx + f, lim)
    f2 = min(f, tot)
    return max(0.0, tot - f2), f2
SD.boeing_capacity = no_extra
out["no_extra_capacity_item"] = item("f10")
restore()
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "why2.json"), "w"), indent=1)
print(json.dumps(out, indent=1, default=lambda x: round(x, 3))[:4000])
