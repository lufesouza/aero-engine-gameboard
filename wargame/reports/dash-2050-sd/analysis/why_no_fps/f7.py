import sys, os, json
sys.path.insert(0, "/home/user/aero-engine-gameboard/wargame/dashgame")
os.environ["DASH_RUN"] = "dash-2050-sd"
import model as M, rules as R, reports as RP
s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
def play(bo, site="new_site"):
    o = dict(rec["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
    return R.adjudicate(s0, 2030, orders)[0]
H = M.value(play({}), covert=True)["boeing"]
out = {}
for lab, bo in (("7-year", {"fps": "launch_7yr", "fps_engine_code": 7}), ("10-year", {"fps": "launch_10yr", "fps_engine_code": 7})):
    v = M.value(play(bo), covert=True)["boeing"]
    out[lab] = {"item": v["pv_delta"] - H["pv_delta"], "bridge": {k: v["bridge"].get(k, 0) - H["bridge"].get(k, 0) for k in v["bridge"] if abs(v["bridge"].get(k, 0) - H["bridge"].get(k, 0)) > 0.005}}
M.SD_ON = False
H0 = M.value(play({}), covert=True)["boeing"]
for lab, bo in (("7-year", {"fps": "launch_7yr", "fps_engine_code": 7}), ("10-year", {"fps": "launch_10yr", "fps_engine_code": 7})):
    out[lab]["dashboard_item"] = M.value(play(bo), covert=True)["boeing"]["pv_delta"] - H0["pv_delta"]
print(json.dumps(out, indent=1, default=lambda x: round(x, 2)))
