"""Rebuild every company's brief grid for each round of dash-2050-emb with the current engine and compare it with the
record grids (what the players were briefed). Writes data/grid_recheck.json (every cell that moved, old and new) and
nothing to the run. After the engine fix that counts an Embraer launch's full 20-year window (model.board_t_end),
two cells move: Embraer's launch in the rivals-hold column of rounds 3 and 4, whose loop had ended in 2061.

  DASH_RUN=dash-2050-emb DASH_BOARD=v3 python3 recheck_grids.py      (about ten minutes)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HERE, "..", "..", "dashgame")
OUT = os.path.join(HERE, "data", "grid_recheck.json")
os.environ.setdefault("DASH_RUN", "dash-2050-emb")
os.environ.setdefault("DASH_BOARD", "v3")
ROUNDS = [1, 2, 3, 4]
sys.path.insert(0, DG)
import model as M  # noqa: E402
import briefs as B  # noqa: E402
import rules as R  # noqa: E402

RD = os.path.join(DG, "..", "runs", os.environ["DASH_RUN"])
jl = lambda n: json.load(open(os.path.join(RD, n)))
moved, total = [], 0
for n in ROUNDS:
    s = jl("state_r%d.json" % (n - 1))
    year = R.ROUNDS[n - 1]
    rec = jl("grids_r%d.json" % n)
    for side in M.SIDES:
        _, grid, scen = B.private_brief(s, side, year, n)
        names = [x[0] for x in scen]
        assert names == rec[side]["scenarios"], (n, side, names, rec[side]["scenarios"])
        old = {r["plan"]: [c[0] for c in r["cells"]] for r in rec[side]["rows"]}
        for g in grid:
            o = old[g[0]]
            for j, c in enumerate(g[2]):
                total += 1
                if abs(c[0] - o[j]) > 1e-9:
                    moved.append({"round": n, "side": side, "plan": g[0], "column": names[j], "was": o[j], "now": c[0]})
        print("round", n, side, "rows", len(grid), "moved so far", len(moved), flush=True)
json.dump({"run": os.environ["DASH_RUN"], "cells": total, "moved": moved}, open(OUT, "w"), indent=1)
print("cells", total, "moved", len(moved))
for m in moved:
    print(m)
