"""Narrowbody market shares in the fps business case (run dash-2050-sd): Do Nothing against a 2030 10-year fps at
Renton (in service 2040), everyone else's 2030 orders as played (Airbus NGSA on the A320 Alt plan, in service 2037).

Two shares a year, for Boeing (Airbus is the rest):
- preference: the dashboard's share rule (board v3, _compute_nb_share_unified): the share of new orders customers want;
- delivered: Boeing's share of 737/A320-class deliveries after the supply-and-demand layer (firm backlog first,
  capacity, overflow of unserved customers, drop-out).
Writes shares.json next to this file. Run from /tmp: python3 <path>/shares.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["DASH_RUN"] = "dash-2050-sd"
sys.path.insert(0, "/home/user/aero-engine-gameboard/wargame/dashgame")
import model as M, reports as RP, rules as R, supply_demand as SD

s0, rec = RP.jl("state_r0.json"), RP.jl("record_r1.json")
LAUNCH = 2030


def build(bo, site="new_site"):
    o = dict(rec["orders"]["boeing"]); o.update({"fps": "hold", "re787": "hold", "fps_engine_code": None, "fps_site": site}); o.update(bo)
    orders = {k: (o if k == "boeing" else rec["orders"][k]) for k in M.SIDES}
    orders = {k: R.validate(s0, k, LAUNCH, x)[0] for k, x in orders.items()}
    return R.adjudicate(s0, LAUNCH, orders)[0]


def rows(state):
    v = M.value(state, covert=True, series=True)
    out = {}
    for r in v["_af_series"]["years"]:
        b, a, sd = r["boeing"], r["airbus"], r["sd"]
        out[r["year"]] = {"pref_b": b["nb_pref_share"], "dlv_share_b": b["nb_delivered_share"],
                          "boeing_dlv": b["nb_units"], "airbus_dlv": a["nb_units"],
                          "fps": sd["dlv_fps"], "max": sd["dlv_max"], "ngsa": sd["dlv_ngsa"], "a320": sd["dlv_a320"],
                          "demand": sd["demand"], "wanted_b": b["sd"]["wanted"], "wanted_a": a["sd"]["wanted"],
                          "cap_b": b["sd"]["capacity"], "cap_a": a["sd"]["capacity"],
                          "spill_to_b": b["sd"]["spill_in"], "spill_to_a": a["sd"]["spill_in"],
                          "firm_b": b["sd"]["firm_out"], "firm_a": a["sd"]["firm_out"],
                          "backlog_b": b["sd"]["backlog_out"], "backlog_a": a["sd"]["backlog_out"], "lost": sd["lost"],
                          "board_units_b": b["board_nb_units"], "board_units_a": a["board_nb_units"],
                          "in_window_b": b["nb_in_window"], "df": r["df_b"]}
    return v, out


fps_state = build({"fps": "launch_10yr", "fps_engine_code": 7}, "renton")
dn_state = build({}, "new_site")
vf, F = rows(fps_state)
vh, D = rows(dn_state)
years = sorted(set(F) & set(D))
p = M.af_params()
out = {"years": years, "fps": {str(y): F[y] for y in years}, "do_nothing": {str(y): D[y] for y in years},
       "eis": {"fps": fps_state["prog"]["fps"]["eis"], "ngsa": fps_state["prog"]["ngsa"]["eis"]},
       "a320_plan": fps_state["sd"].get("a320_plan"),
       "board": {"nb_per_year": p["NB_PER_YR"]},
       "check": {"dpv_fps": vf["boeing"]["pv_delta"], "dpv_dn": vh["boeing"]["pv_delta"]}}
# checks: the shares close and the item matches the business case
for k, S in (("fps", F), ("do_nothing", D)):
    for y in years:
        x = S[y]
        tot = x["boeing_dlv"] + x["airbus_dlv"]
        assert abs(x["dlv_share_b"] - x["boeing_dlv"] / tot) < 1e-9
        assert abs(x["boeing_dlv"] - x["fps"] - x["max"]) < 1e-6 and abs(x["airbus_dlv"] - x["ngsa"] - x["a320"]) < 1e-6
case = json.load(open(os.path.join(HERE, "..", "fps_business_case", "case.json")))
assert abs((out["check"]["dpv_fps"] - out["check"]["dpv_dn"]) - case["cases"]["renton"]["game_npv"]) < 1e-9
json.dump(out, open(os.path.join(HERE, "shares.json"), "w"), indent=1)
print("eis", out["eis"], "plan", out["a320_plan"])
print("year | pref DN fps | delivered DN fps | Boeing dlv DN fps | Airbus dlv DN fps | demand | spill to B DN fps")
for y in years:
    d, f = D[y], F[y]
    print(y, "| %4.1f %4.1f | %4.1f %4.1f | %5.0f %5.0f | %5.0f %5.0f | %5.0f | %4.0f %4.0f" % (
        100 * d["pref_b"], 100 * f["pref_b"], 100 * d["dlv_share_b"], 100 * f["dlv_share_b"], d["boeing_dlv"], f["boeing_dlv"],
        d["airbus_dlv"], f["airbus_dlv"], d["demand"], d["spill_to_b"], f["spill_to_b"]))
