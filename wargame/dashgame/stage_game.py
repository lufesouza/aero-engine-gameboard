"""GM benchmark: the airframer stage game in a round (Boeing's plans x Airbus's plans, engine makers holding, nobody
moving later), solved on the board. Players never see it. Writes ../runs/dash-2050/stage_rN.json."""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import briefs as B  # noqa: E402
import model as M  # noqa: E402
import rules as R  # noqa: E402

RUN_DIR = os.path.join(HERE, "..", "runs", os.environ.get("DASH_RUN", "dash-2050"))


def stage(n, eps=1.0):
    year = R.ROUNDS[n - 1]
    prev = json.load(open(os.path.join(RUN_DIR, "state_r%d.json" % (n - 1))))
    rec = json.load(open(os.path.join(RUN_DIR, "record_r%d.json" % n)))
    bo, ao = B.own_options(prev, "boeing", year), B.own_options(prev, "airbus", year)
    cells = {}
    for (bl, b), (al, a) in itertools.product(bo, ao):
        orders = {"boeing": b, "airbus": a}
        for s in ("cfm", "pratt_whitney", "rolls_royce"):   # engine makers as actually played that round
            orders[s] = rec["orders"][s]
        s1, _ = R.adjudicate(prev, year, orders)
        v = M.value(s1, covert=True, series=False)
        cells[(bl, al)] = (v["boeing"]["pv_delta"], v["airbus"]["pv_delta"])
    pure, near = [], []
    for bl, _ in bo:
        for al, _ in ao:
            vb, va = cells[(bl, al)]
            bb = max(cells[(x, al)][0] for x, _ in bo)
            ba = max(cells[(bl, y)][1] for y, _ in ao)
            if vb >= bb - 1e-9 and va >= ba - 1e-9:
                pure.append((bl, al, vb, va))
            elif vb >= bb - eps and va >= ba - eps:
                near.append((bl, al, vb, va))

    def match(side, opts):
        act = rec["orders"][side]
        for lab, o in opts:
            if all(act.get(k) == v or (k.endswith("engine_code")) or (k == "delay_tactics" and {act.get(k), v} <= {"bottleneck", "poaching"})
                   for k, v in o.items()):
                return lab
    played = (match("boeing", bo), match("airbus", ao))
    out = {"round": n, "year": year, "pure": pure, "near_within_1b": near, "played": played,
           "played_value": cells.get(played), "eps_b": eps,
           "boeing_best_response_to_played_airbus": max(((x, cells[(x, played[1])][0]) for x, _ in bo), key=lambda t: t[1]),
           "airbus_best_response_to_played_boeing": max(((y, cells[(played[0], y)][1]) for y, _ in ao), key=lambda t: t[1])}
    json.dump(out, open(os.path.join(RUN_DIR, "stage_r%d.json" % n), "w"), indent=1)
    return out


if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        o = stage(n)
        print("round", n, "played", o["played"], [round(x, 2) for x in o["played_value"]])
        print("  pure:", [(p[0], p[1], round(p[2], 2), round(p[3], 2)) for p in o["pure"]])
        print("  near (within $1B):", [(p[0], p[1], round(p[2], 2), round(p[3], 2)) for p in o["near_within_1b"]][:8])
        print("  Boeing BR:", o["boeing_best_response_to_played_airbus"], "| Airbus BR:", o["airbus_best_response_to_played_boeing"])
