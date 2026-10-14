"""Decompose each lever of the 2030 fps decision (10-year fps, launched 2030, in service 2040; everyone else's orders as
played; nobody moves after the round): fps capacity, Boeing deliveries with and without the fps, profit gain by period,
and the value lines. Writes levers.json next to this file."""
import copy, json, os, sys
sys.path.insert(0, "/home/user/aero-engine-gameboard/wargame/dashgame")
os.environ["DASH_RUN"] = "dash-2050-sd"
import model as M, rules as R, reports as RP, supply_demand as SD

REAL_B = SD.boeing_capacity
s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
def play(bo, site):
    o = dict(rec["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
    return R.adjudicate(s0, 2030, orders)[0]
F10 = {"fps": "launch_10yr", "fps_engine_code": 7}
ST = {"hold": play({}, "new_site"), "new sites": play(F10, "new_site"), "Renton": play(F10, "renton")}

def cap_with(ramp):
    """supply_demand.boeing_capacity with the fps output (and the Renton wind-down) taken from `ramp`."""
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
    """The NGSA chart's ramp run k times faster: year y gets the chart's average output over the k chart years
    starting at eis + k*(y - eis). k = 1 reproduces the game."""
    def ramp(eis, shift, y):
        if y < eis:
            return SD._annual("ngsa", shift, y), SD._rundown("a320_base", shift, y) / SD.a320_full()
        ys = [eis + k * (y - eis) + j for j in range(k)]
        return (sum(SD._annual("ngsa", shift, z) for z in ys) / k,
                sum(SD._rundown("a320_base", shift, z) for z in ys) / k / SD.a320_full())
    return ramp
def instant(eis, shift, y):
    return (SD.fps_full(), 0.0) if y >= eis else (0.0, 1.0)

def measure():
    v = {k: M.value(s, covert=True, series=True) for k, s in ST.items()}
    site = max(("new sites", "Renton"), key=lambda k: v[k]["boeing"]["pv_delta"])
    f, h = v[site], v["hold"]
    rf = {r["year"]: r for r in f["_af_series"]["years"]}
    rh = {r["year"]: r for r in h["_af_series"]["years"]}
    per = {}
    for lo, hi in ((2040, 2045), (2046, 2050), (2051, 2059)):
        ys = [y for y in range(lo, hi + 1) if rf[y]["boeing"]["nb_in_window"]]
        per[f"{lo}-{hi}"] = {
            "boeing_dlv_fps_case": sum(rf[y]["boeing"]["nb_units"] for y in ys),
            "fps_units": sum(rf[y]["sd"]["dlv_fps"] for y in ys),
            "boeing_dlv_do_nothing": sum(rh[y]["boeing"]["nb_units"] for y in ys),
            "new_demand": sum(rf[y]["sd"]["demand"] for y in ys),
            "pv_profit_gain": sum((rf[y]["boeing"]["nb_profit"] - rh[y]["boeing"]["nb_profit"]) * rf[y]["df_b"] for y in ys)}
    ramp = [round(SD.boeing_capacity(ST[site], y)[1] / 12.0, 1) for y in range(2040, 2052)]
    br = {k: f["boeing"]["bridge"].get(k, 0) - h["boeing"]["bridge"].get(k, 0) for k in f["boeing"]["bridge"]}
    return {"site": site, "item": f["boeing"]["pv_delta"] - h["boeing"]["pv_delta"],
            "item_other_site": v["Renton" if site == "new sites" else "new sites"]["boeing"]["pv_delta"] - h["boeing"]["pv_delta"],
            "fps": f["boeing"]["pv_delta"], "do_nothing": h["boeing"]["pv_delta"],
            "fps_a_month_2040_2051": ramp, "periods": per,
            "bridge_delta": {k: x for k, x in br.items() if abs(x) > 0.005}}

out = {}
def run(label, cap=None, edit=None):
    saved = copy.deepcopy(SD.inputs())
    try:
        if edit:
            edit(SD.inputs()["boeing"], SD.inputs()["demand"])
            SD._annual.cache_clear()
        if cap:
            SD.boeing_capacity = cap
        out[label] = measure()
    finally:
        SD.boeing_capacity = REAL_B
        SD.inputs().clear(); SD.inputs().update(saved); SD._annual.cache_clear()
g15 = lambda b, d: d.update({"growth": {k: x * 1.5 for k, x in d["growth"].items()}})
run("As played")
run("fps ramp twice as fast", cap_with(compressed(2)))
run("fps ramp three times as fast", cap_with(compressed(3)))
run("fps at full rate from entry into service", cap_with(instant))
run("50% more growth", edit=g15)
run("Ramp twice as fast plus 50% more growth", cap_with(compressed(2)), g15)
run("Boeing cap of 120 a month", edit=lambda b, d: b.update({"total_rate_cap": 120.0}))
run("No MAX tail", edit=lambda b, d: b.update({"max_tail_rate": 0.0}))
# check: the k = 1 compression reproduces the game exactly
SD.boeing_capacity = cap_with(compressed(1))
out["_k1_check"] = measure()["item"] - out["As played"]["item"]
SD.boeing_capacity = REAL_B
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "levers.json"), "w"), indent=1)
for k, x in out.items():
    if k.startswith("_"):
        print(k, x); continue
    print(f"{k:45s} item {x['item']:+.2f} ({x['site']}; other {x['item_other_site']:+.2f})  fps {x['fps']:+.2f}  DN {x['do_nothing']:+.2f}")
    print("    fps a month 2040-51:", x["fps_a_month_2040_2051"])
    for p, y in x["periods"].items():
        print(f"    {p}: Boeing {y['boeing_dlv_fps_case']:.0f} (fps {y['fps_units']:.0f}) vs DN {y['boeing_dlv_do_nothing']:.0f}; demand {y['new_demand']:.0f}; PV gain {y['pv_profit_gain']:+.2f}")
    print("    bridge:", {k: round(v, 2) for k, v in x["bridge_delta"].items()})
