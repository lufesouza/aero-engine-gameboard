"""Value a saved game state on the board selected by DASH_BOARD (v2 or v3), for comparing games played on different
boards. Prints JSON {side: pv_delta}. Run without DASH_RUN so no run's board.txt overrides DASH_BOARD.

  DASH_BOARD=v2 python3 crossvalue.py ../runs/dash-2050-exco/state_r4.json
"""
import json
import os
import sys

assert not os.environ.get("DASH_RUN"), "unset DASH_RUN: the board comes from DASH_BOARD here"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as M  # noqa: E402

if __name__ == "__main__":
    st = json.load(open(sys.argv[1]))
    v = M.value(st, covert=True, series=False)
    print(json.dumps({"board": M.H.VERSION, **{s: round(v[s]["pv_delta"], 6) for s in M.SIDES}}))
