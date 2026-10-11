"""Replay any finished run: each round's adjudicated orders, re-validated and re-adjudicated from the previous state,
give the recorded state and value, and no year already played changes in any round.

  DASH_RUN=<run> python3 test_replay.py     (the run's board.txt picks the board)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import rules as R  # noqa: E402

RUN = os.environ.get("DASH_RUN")
assert RUN, "set DASH_RUN"
REC = os.path.join(HERE, "..", "runs", RUN)
fails = []


def jl(n):
    return json.load(open(os.path.join(REC, n)))


def shares(state):
    v = M.value(state, covert=True, series=True)
    af = {r["year"]: (r["boeing"]["nb_share"], r["boeing"]["wb_share"]) for r in v["_af_series"]["years"]}
    en = {r["year"]: tuple(r[s][k] for s in ("cfm", "pratt_whitney", "rolls_royce") for k in ("nb_share", "wb_share"))
          for r in v["_en_series"]["years"]}
    return af, en


s = jl("state_r0.json")
n = 0
while os.path.exists(os.path.join(REC, "record_r%d.json" % (n + 1))):
    n += 1
    rec = jl("record_r%d.json" % n)
    year = rec["year"]
    clean = {side: R.validate(s, side, year, rec["orders"][side])[0] for side in M.SIDES}
    s1, _ = R.adjudicate(s, year, clean)
    want = jl("state_r%d.json" % n)
    if json.loads(json.dumps(s1)) != want:
        fails.append(("replay state differs", n))
    v = M.value(want, covert=True, series=False)
    for side in M.SIDES:
        if abs(v[side]["pv_delta"] - rec["value"][side]["pv_delta"]) > 1e-9:
            fails.append(("value differs", n, side))
    a0, e0 = shares(s)
    a1, e1 = shares(want)
    for y in range(2026, year):
        if any(abs(x - z) > 1e-12 for x, z in zip(a0[y], a1[y])) or any(abs(x - z) > 1e-12 for x, z in zip(e0[y], e1[y])):
            fails.append(("a played year changed", n, y))
    s = want
print("run", RUN, "board", M.H.VERSION, "rounds", n)
if fails:
    print("FAILURES", fails[:20])
    sys.exit(1)
print("replay exact; no played year changed")
