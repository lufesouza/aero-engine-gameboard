"""Counterfactual replays for the comparison with the earlier game. The two games' orders differ in four places:
Boeing's fps ramp and 737 rate (2030), Airbus's Delay Tactics and Rolls-Royce's Joint Venture commitment (2035). Start
from the earlier game's orders, set each of the four to either game's value (16 combinations), replay all four rounds
with the game master's rules, and value the final state on both boards. Writes data/replay16.json.
Combination keys are four bits F R D J: 0 = the earlier game's order, 1 = this game's order.

  python3 make_replay16.py              (runs itself once per board in a subprocess; the board loads at import)
"""
import copy
import itertools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GM = os.path.join(HERE, "..", "..", "dashgame")
OLD_REC = os.path.join(HERE, "..", "dash-2050", "record")
FLIPS = {"F": (0, "boeing", "fps", ("launch_7yr", "launch_10yr")),
         "R": (0, "boeing", "rate_737", ("increase", "hold")),
         "D": (1, "airbus", "delay_tactics", ("bottleneck", "none")),
         "J": (1, "rolls_royce", "jv_with_pw", ("hold", "commit"))}


def one_board():
    sys.path.insert(0, GM)
    import model as M  # noqa: E402
    import rules as R  # noqa: E402
    recs = [json.load(open(os.path.join(OLD_REC, "record_r%d.json" % n))) for n in range(1, 5)]
    base = [r["orders"] for r in recs]
    s0 = json.load(open(os.path.join(OLD_REC, "state_r0.json")))
    out = {}
    for combo in itertools.product((0, 1), repeat=4):
        orders = copy.deepcopy(base)
        for (k, (rnd, side, field, vals)), bit in zip(FLIPS.items(), combo):
            orders[rnd][side][field] = vals[bit]
        s = s0
        for n, rec in enumerate(recs):
            year = rec["year"]
            clean = {side: R.validate(s, side, year, orders[n][side])[0] for side in M.SIDES}
            s, _ = R.adjudicate(s, year, clean)
        v = M.value(s, covert=True, series=False)
        out["".join(map(str, combo))] = {side: v[side]["pv_delta"] for side in M.SIDES}
    print(json.dumps({"board": M.H.VERSION, "res": out}))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        one_board()
        sys.exit(0)
    res = {}
    for board in ("v2", "v3"):
        env = {k: v for k, v in os.environ.items() if k != "DASH_RUN"}
        env["DASH_BOARD"] = board
        r = subprocess.run([sys.executable, __file__, "--one"], env=env, capture_output=True, text=True, check=True)
        res[board] = json.loads(r.stdout.strip().splitlines()[-1])["res"]
    # the endpoints must reproduce both games exactly
    xv = json.load(open(os.path.join(HERE, "data", "crossvalue.json")))
    for key, game in (("0000", "earlier"), ("1111", "this")):
        for board in ("v2", "v3"):
            for side, val in res[board][key].items():
                assert abs(val - xv[f"{game}_{board}"][side]) < 1e-5, (key, board, side, val, xv[f"{game}_{board}"][side])
    with open(os.path.join(HERE, "data", "replay16.json"), "w") as f:
        json.dump({"flips": {k: {"round": v[0] + 1, "side": v[1], "field": v[2], "earlier": v[3][0], "this": v[3][1]}
                             for k, v in FLIPS.items()}, "res": res}, f, indent=1)
    print("endpoints reproduce both games on both boards; wrote data/replay16.json")
