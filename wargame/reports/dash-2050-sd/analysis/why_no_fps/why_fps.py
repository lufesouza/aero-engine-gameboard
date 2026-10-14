"""Why Boeing did not launch the fps in dash-2050-sd: waterfall of the 2030 decision value and levers."""
import json, os, sys
sys.path.insert(0, "/home/user/aero-engine-gameboard/wargame/dashgame")
os.environ["DASH_RUN"] = "dash-2050-sd"
import model as M, rules as R, reports as RP, supply_demand as SD

s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
REAL = (SD.boeing_capacity, SD.airbus_capacity, SD.demand, SD.firm_backlog)

def play(bo, site="new_site"):
    o = dict(rec["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
    s1, _ = R.adjudicate(s0, 2030, orders)
    return s1

S_HOLD = play({})
S_F10 = play({"fps": "launch_10yr", "fps_engine_code": 7})
S_F10R = play({"fps": "launch_10yr", "fps_engine_code": 7}, "renton")
S_F7 = play({"fps": "launch_7yr", "fps_engine_code": 7})

def val(s, series=False):
    return M.value(s, covert=True, series=series)

def item(s_fps, s_hold=S_HOLD):
    a, h = val(s_fps), val(s_hold)
    return a["boeing"]["pv_delta"] - h["boeing"]["pv_delta"], a, h

def unlimited_after_eis(key, real):
    def f(s, y):
        r = SD._live(s, key)
        if r and y >= r["eis"]:
            return (0.0, 1e9)
        return real(s, y) if real else (1e9, 0.0)
    return f

def restore():
    SD.boeing_capacity, SD.airbus_capacity, SD.demand, SD.firm_backlog = REAL
    SD.reload()

out = {}
# ---- waterfall
steps = []
M.SD_ON = False
v, a, h = item(S_F10); steps.append(("Dashboard alone", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
M.SD_ON = True
try:
    SD.boeing_capacity, SD.airbus_capacity = unlimited_after_eis("fps", None), unlimited_after_eis("ngsa", None)
    SD.demand, SD.firm_backlog = (lambda y: 2000.0), (lambda: (0.0, 0.0))
    v, a, h = item(S_F10); steps.append(("Layer, neutral (2,000 a year, unlimited capacity)", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
    SD.demand = REAL[2]
    v, a, h = item(S_F10); steps.append(("+ real new demand (replacement + growth), capacity unlimited", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
    SD.firm_backlog = REAL[3]
    SD.boeing_capacity = unlimited_after_eis("fps", lambda s, y: (SD.max_path(y), 0.0))
    SD.airbus_capacity = unlimited_after_eis("ngsa", lambda s, y: (SD.a320_full(), 0.0))
    v, a, h = item(S_F10); steps.append(("+ firm backlog and today's lines (MAX path, A320 at 85) until the new types; new types instant and unlimited", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
    SD.airbus_capacity = REAL[1]
    v, a, h = item(S_F10); steps.append(("+ Airbus's real plan (Rev. B: A320 rundown, NGSA ramp, 100 a month)", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
    SD.boeing_capacity = REAL[0]
    v, a, h = item(S_F10); steps.append(("+ Boeing's real plan (fps ramp, MAX gives way, 100 a month) = the game", v, a["boeing"]["pv_delta"], h["boeing"]["pv_delta"]))
finally:
    restore()
out["waterfall"] = [{"step": s, "fps_minus_hold": v, "fps": f, "hold": hh} for s, v, f, hh in steps]

# ---- bridge of the decision in the game, and deliveries
a, h = val(S_F10, True), val(S_HOLD, True)
out["bridge_delta"] = {k: a["boeing"]["bridge"].get(k, 0) - h["boeing"]["bridge"].get(k, 0) for k in a["boeing"]["bridge"]}
ra = {r["year"]: r for r in a["_af_series"]["years"]}; rh = {r["year"]: r for r in h["_af_series"]["years"]}
per = []
for lo, hi in ((2026, 2036), (2037, 2039), (2040, 2045), (2046, 2050), (2051, 2059)):
    ys = range(lo, hi + 1)
    per.append({"period": f"{lo}-{hi}",
                "boeing_dlv_fps_case": sum(ra[y]["boeing"]["nb_units"] for y in ys), "boeing_dlv_hold": sum(rh[y]["boeing"]["nb_units"] for y in ys),
                "fps_units": sum(ra[y]["sd"]["dlv_fps"] for y in ys),
                "board_units_fps_case": sum(ra[y]["boeing"]["board_nb_units"] for y in ys), "board_units_hold": sum(rh[y]["boeing"]["board_nb_units"] for y in ys),
                "pref_fps_case": ra[hi]["boeing"]["nb_pref_share"], "pref_hold": rh[hi]["boeing"]["nb_pref_share"],
                "dlv_share_fps_case": ra[hi]["boeing"]["nb_delivered_share"], "dlv_share_hold": rh[hi]["boeing"]["nb_delivered_share"],
                "pv_profit_gain_board": sum((ra[y]["boeing"]["board_nb_profit"] - rh[y]["boeing"]["board_nb_profit"]) * ra[y]["df_b"] for y in ys if ra[y]["boeing"]["nb_in_window"]),
                "pv_profit_gain_delivered": sum((ra[y]["boeing"]["nb_profit"] - rh[y]["boeing"]["nb_profit"]) * ra[y]["df_b"] for y in ys if ra[y]["boeing"]["nb_in_window"])})
out["periods"] = per
out["spare_boeing_hold"] = {y: rh[y]["boeing"]["sd"]["capacity"] - rh[y]["boeing"]["nb_units"] for y in range(2036, 2050)}

# ---- levers on the 2030 decision (best of new sites / Renton), everyone else as played
def best_item():
    v1 = item(S_F10)[0]; v2 = item(S_F10R)[0]
    return max((v1, "new sites"), (v2, "Renton"))
levers = [("As played (corrected demand)", best_item())]
import copy
def with_inputs(label, fn, cap_fn=None):
    SD.reload()
    saved = copy.deepcopy(SD.inputs())
    try:
        fn(SD.inputs()["boeing"], SD.inputs()["demand"])
        SD._annual.cache_clear()
        if cap_fn:
            SD.boeing_capacity = cap_fn
        levers.append((label, best_item()))
    finally:
        SD.boeing_capacity = REAL[0]
        SD.inputs().clear(); SD.inputs().update(saved); SD._annual.cache_clear()
def fast_ramp(k):
    real = REAL[0]
    def f(s, y):
        b = SD.inputs()["boeing"]
        fps = SD._live(s, "fps")
        if not fps or y < fps["eis"]:
            return real(s, y)
        y2 = int(min(fps["eis"] + k * (y - fps["eis"]), 2100))
        _, fp = real(s, y2) if y2 <= b["max_last_year"] or y > b["max_last_year"] else real(s, y2)
        fp_full = SD._annual("ngsa", fps["eis"] - SD.CHART_YEAR, y2) * b.get("fps_ramp_scale", 1.0)
        mx0, _ = real({"prog": {}, "rate737": s.get("rate737"), "sd": s.get("sd")}, y)   # the MAX with no fps
        cap = 12 * b["total_rate_cap"]
        tail = min(mx0, 12 * b["max_tail_rate"]) if y <= b["max_last_year"] else 0.0
        fp = min(fp_full, max(0.0, cap - tail))
        mx = min(mx0, max(0.0, cap - fp))
        if y > b["max_last_year"]:
            mx = min(mx, max(0.0, SD.fps_full() - fp))
        return mx, fp
    return f
noop = lambda bb, dd: None
with_inputs("fps ramp twice as fast", noop, fast_ramp(2))
with_inputs("fps ramp three times as fast", noop, fast_ramp(3))
with_inputs("fps at full rate from entry into service", noop, fast_ramp(100))
with_inputs("No MAX tail (fps can use the full 100 a month at once)", lambda bb, dd: bb.update({"max_tail_rate": 0.0}))
with_inputs("Boeing cap 120 a month (fps up to 120)", lambda bb, dd: bb.update({"total_rate_cap": 120.0}))
with_inputs("Growth x1.5", lambda bb, dd: dd.update({"growth": {k: x * 1.5 for k, x in dd["growth"].items()}}))
with_inputs("No flexible customers (no Airbus overflow to Boeing)", lambda bb, dd: dd.update({"flex_share": 0.0}))
with_inputs("5% of waiting customers drop out a year", lambda bb, dd: dd.update({"lapse_per_year": 0.05}))
with_inputs("Ramp twice as fast + growth x1.5", lambda bb, dd: dd.update({"growth": {k: x * 1.5 for k, x in dd["growth"].items()}}), fast_ramp(2))
with_inputs("Ramp twice as fast + Boeing cap 120", lambda bb, dd: bb.update({"total_rate_cap": 120.0}), fast_ramp(2))
out["levers"] = [{"lever": l, "item": v, "site": s} for l, (v, s) in levers]
out["fps7"] = item(S_F7)[0]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "why_fps.json"), "w"), indent=1, default=float)
for w in out["waterfall"]:
    print("%-110s %+6.2f  (fps %+6.2f, hold %+6.2f)" % (w["step"], w["fps_minus_hold"], w["fps"], w["hold"]))
print("bridge delta", {k: round(x, 2) for k, x in out["bridge_delta"].items() if abs(x) > 0.005})
for p in per:
    print(p["period"], {k: (round(x) if abs(x) > 2 else round(x, 3)) for k, x in p.items() if k != "period"})
print("spare Boeing capacity (hold)", {y: round(x) for y, x in out["spare_boeing_hold"].items()})
for l in out["levers"]:
    print("%-60s %+6.2f %s" % (l["lever"], l["item"], l["site"]))
print("fps 7yr item", round(out["fps7"], 2))
