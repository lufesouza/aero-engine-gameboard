"""Game-master command line for dash-2050 (the GM only; players are blocked from this folder and from wargame/runs).

  python3 gm.py init                      # new run: state_r0.json, public rules to each player's folder
  python3 gm.py brief N                   # bulletin + private briefs for round N (from state after round N-1)
  python3 gm.py adjudicate N orders.json  # validate and adjudicate round N; writes state_rN.json and the record
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import briefs as B  # noqa: E402
import model as M  # noqa: E402
import rules as R  # noqa: E402

RUN = os.environ.get("DASH_RUN", "dash-2050")
RUN_DIR = os.path.join(HERE, "..", "runs", RUN)
ROUNDS = R.ROUNDS


def pdir(side):
    return "/tmp/wargame-%s/%s" % (side, RUN)


def jload(name):
    with open(os.path.join(RUN_DIR, name)) as f:
        return json.load(f)


def jsave(name, obj):
    with open(os.path.join(RUN_DIR, name), "w") as f:
        json.dump(obj, f, indent=1, default=str)


def init():
    os.makedirs(RUN_DIR, exist_ok=True)
    s = M.new_state()
    jsave("state_r0.json", s)
    rules_txt = B.public_rules()
    with open(os.path.join(RUN_DIR, "rules.md"), "w") as f:
        f.write(rules_txt)
    for side in M.SIDES:
        os.makedirs(pdir(side), exist_ok=True)
        with open(os.path.join(pdir(side), "rules.md"), "w") as f:
            f.write(rules_txt)
    print("initialised", RUN_DIR)


def brief(n):
    year = ROUNDS[n - 1]
    s = jload("state_r%d.json" % (n - 1))
    rec = jload("record_r%d.json" % (n - 1)) if n > 1 else {}
    statements = rec.get("public_statements")
    public_other = rec.get("public_other_moves")
    gm_notes = rec.get("bulletin_notes")
    bul = B.bulletin(s, year, n, statements, public_other, gm_notes)
    with open(os.path.join(RUN_DIR, "bulletin_r%d.md" % n), "w") as f:
        f.write(bul)
    grids = {}
    for side in M.SIDES:
        notes = (rec.get("private_notes") or {}).get(side)
        txt, grid, scen = B.private_brief(s, side, year, n, gm_notes=notes)
        full = bul + "\n\n---\n\n" + txt
        os.makedirs(pdir(side), exist_ok=True)
        with open(os.path.join(pdir(side), "round%d.md" % n), "w") as f:
            f.write(full)
        with open(os.path.join(RUN_DIR, "brief_r%d_%s.md" % (n, side)), "w") as f:
            f.write(full)
        grids[side] = {"scenarios": [x[0] for x in scen],
                       "rows": [{"plan": g[0], "orders": g[1], "cells": g[2]} for g in grid]}
        print(side, "brief written:", len(full), "chars;", len(grid), "plans x", len(scen), "scenarios")
    jsave("grids_r%d.json" % n, grids)


def adjudicate(n, orders_path):
    year = ROUNDS[n - 1]
    s = jload("state_r%d.json" % (n - 1))
    with open(orders_path) as f:
        returned = json.load(f)
    orders, problems = {}, {}
    for side in M.SIDES:
        o = (returned.get(side) or {}).get("orders", {})
        clean, probs = R.validate(s, side, year, o)
        orders[side] = clean
        problems[side] = probs
    s1, log = R.adjudicate(s, year, orders)
    jsave("state_r%d.json" % n, s1)
    v = M.value(s1, covert=True, series=False)
    vpub = M.value(s1, covert=False, series=False)
    statements = {side: (returned.get(side) or {}).get("public_statement", "") for side in M.SIDES}
    public_other, private_other = {}, {}
    for side in M.SIDES:
        for it in (returned.get(side) or {}).get("other_moves", []) or []:
            (public_other if it.get("public") else private_other).setdefault(side, []).append(it)
    public_log = [e for e in log if "[covert]" not in e and "conditional launch" not in e]
    notes = ["Round %d (%d) adjudicated. Public events: %s." % (n, year, "; ".join(public_log) if public_log else "none")]
    rec = {"round": n, "year": year, "orders": orders, "problems": problems, "log": log,
           "public_statements": statements, "public_other_moves": public_other, "private_other_moves": private_other,
           "bulletin_notes": notes,
           "private_notes": {side: ["Your round-%d orders were adjusted: %s" % (n, "; ".join(problems[side]))]
                             for side in M.SIDES if problems[side]},
           "value": {side: {"pv_delta": v[side]["pv_delta"], "yield": v[side]["yield"]} for side in M.SIDES},
           "value_public_view": {side: {"pv_delta": vpub[side]["pv_delta"], "yield": vpub[side]["yield"]} for side in M.SIDES},
           "returned": returned}
    jsave("record_r%d.json" % n, rec)
    for side in M.SIDES:   # each player keeps its own sealed orders and reasoning (nobody else's)
        with open(os.path.join(pdir(side), "my_orders_r%d.json" % n), "w") as f:
            json.dump({"round": n, "year": year, "as_returned": returned.get(side), "as_adjudicated": orders[side],
                       "adjustments": problems[side]}, f, indent=1)
    print("round", n, year, "adjudicated")
    for e in log:
        print("  -", e)
    for side in M.SIDES:
        if problems[side]:
            print("  !", side, problems[side])
    for side in M.SIDES:
        print("  %-14s ΔPV %+8.2f  yield %6.2f%%" % (side, v[side]["pv_delta"], v[side]["yield"]))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "init":
        init()
    elif cmd == "brief":
        brief(int(sys.argv[2]))
    elif cmd == "adjudicate":
        adjudicate(int(sys.argv[2]), sys.argv[3])
