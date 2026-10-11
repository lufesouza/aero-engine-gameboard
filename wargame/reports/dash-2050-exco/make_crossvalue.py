"""Value the final state of this game (dash-2050-exco, board v3) and of the earlier dash-2050 game (board v2) on both
boards, so the report can separate what the board change did from what the players did. Writes data/crossvalue.json.

  python3 make_crossvalue.py   (needs ../../runs/dash-2050-exco/state_r4.json and ../dash-2050/record/state_r4.json)
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
GM = os.path.join(HERE, "..", "..", "dashgame", "crossvalue.py")
STATES = {"this": os.path.join(HERE, "record", "state_r4.json"),
          "earlier": os.path.join(HERE, "..", "dash-2050", "record", "state_r4.json")}
out = {}
for game, path in STATES.items():
    for board in ("v2", "v3"):
        env = {k: v for k, v in os.environ.items() if k != "DASH_RUN"}
        env["DASH_BOARD"] = board
        r = subprocess.run(["python3", GM, path], env=env, capture_output=True, text=True, check=True)
        out[f"{game}_{board}"] = json.loads(r.stdout.strip().splitlines()[-1])
with open(os.path.join(HERE, "data", "crossvalue.json"), "w") as f:
    json.dump(out, f, indent=1)
for k, v in out.items():
    print(k, v)
