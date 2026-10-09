"""Game-level checks for the dash-2050 rules (run after test_model.py).

1. The recorded game replays exactly: each round's orders, validated and adjudicated, give the recorded state and value.
2. Years already played never change: after every round, and under a late Joint Venture (formed 2045), every player's
   shares before the decision year equal those of the previous state.
3. Rule arithmetic: conditional launches, the Joint Venture fold-in write-off, the Delay Tactics spending window,
   cancellation write-offs.

Uses the record in ../reports/dash-2050/record (or ../runs/dash-2050 if present).
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import rules as R  # noqa: E402

REC = next(p for p in (os.path.join(HERE, "..", "runs", "dash-2050"), os.path.join(HERE, "..", "reports", "dash-2050", "record"))
           if os.path.exists(os.path.join(p, "record_r4.json")))
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def jl(n):
    return json.load(open(os.path.join(REC, n)))


def shares(state):
    v = M.value(state, covert=True, series=True)
    af = {r["year"]: (r["boeing"]["nb_share"], r["boeing"]["wb_share"]) for r in v["_af_series"]["years"]}
    en = {r["year"]: tuple(r[s][k] for s in ("cfm", "pratt_whitney", "rolls_royce") for k in ("nb_share", "wb_share"))
          for r in v["_en_series"]["years"]}
    return af, en


def same_past(s_before, s_after, year, label):
    a0, e0 = shares(s_before)
    a1, e1 = shares(s_after)
    for y in range(2026, year):
        check(all(abs(x - z) < 1e-12 for x, z in zip(a0[y], a1[y])), (label, "airframer share changed in past year", y))
        check(all(abs(x - z) < 1e-12 for x, z in zip(e0[y], e1[y])), (label, "engine share changed in past year", y))


# 1. replay
s = jl("state_r0.json")
for n in range(1, 5):
    rec = jl("record_r%d.json" % n)
    year = rec["year"]
    orders = jl("orders_r%d.json" % n)
    clean = {side: R.validate(s, side, year, (orders.get(side) or {}).get("orders", {}))[0] for side in M.SIDES}
    s1, _ = R.adjudicate(s, year, clean)
    want = jl("state_r%d.json" % n)
    check(json.loads(json.dumps(s1)) == want, ("replay state differs", n))
    v = M.value(s1, covert=True, series=False)
    for side in M.SIDES:
        check(abs(v[side]["pv_delta"] - rec["value"][side]["pv_delta"]) < 1e-9, ("replay value", n, side))
    same_past(s, s1, year, "round %d" % n)
    s = s1
print("1-2. record replays exactly; no past year changes in any round")

# 2b. a Joint Venture formed late (2045) must not rewrite 2037-2044
s2 = jl("state_r2.json")
o3 = {side: R.validate(s2, side, 2045, (jl("orders_r3.json").get(side) or {}).get("orders", {}))[0] for side in M.SIDES}
o3["rolls_royce"]["jv_with_pw"] = "commit"
s3, log = R.adjudicate(s2, 2045, o3)
check(M.live(s3, "jv") is not None, "JV should form in 2045")
same_past(s2, s3, 2045, "late JV")
print("2b. a Joint Venture formed in 2045 leaves 2026-2044 unchanged")

# 3. rule arithmetic
s1 = jl("state_r1.json")
check(M.live(s1, "pw_solo") and M.live(s1, "rr_solo"), "conditional launches in 2030")
o2 = {side: R.validate(s1, side, 2035, (jl("orders_r2.json").get(side) or {}).get("orders", {}))[0] for side in M.SIDES}
o2["rolls_royce"]["jv_with_pw"] = "commit"
sj, _ = R.adjudicate(s1, 2035, o2)
wo = [d for d in sj["dead"] if d["key"] == "rr_solo"]
check(wo and abs(wo[0]["sunk_nom"] - (8 * 5 / 7 - 4)) < 1e-12, ("RR fold-in write-off", wo))
check(M.live(sj, "jv")["ready"] == 2036, "JV inherits the 2036 GTF2 schedule")
v = M.value(jl("state_r2.json"), covert=True)
check(abs(v["airbus"]["bridge"]["delay_tactics_spend"] + (0.5 / 1.08 ** 9 + 0.5 / 1.08 ** 10)) < 1e-9,
      ("Delay Tactics spend 2035-36", v["airbus"]["bridge"]["delay_tactics_spend"]))
st = M.new_state()
st, _ = R.adjudicate(st, 2030, {"boeing": {"fps": "launch_10yr", "fps_engine_code": 7}})
st, _ = R.adjudicate(st, 2035, {"boeing": {"fps": "cancel"}})
d = [x for x in st["dead"] if x["key"] == "fps"][0]
check(abs(d["sunk_nom"] - 55.25 * 5 / 10) < 1e-9, ("fps cancellation write-off", d))
print("3. conditional launches, fold-in write-off (RR %.3f), Delay Tactics window, cancellation write-off" % (8 * 5 / 7 - 4))

if fails:
    print("FAILURES:", len(fails))
    for f in fails[:20]:
        print("  ", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
