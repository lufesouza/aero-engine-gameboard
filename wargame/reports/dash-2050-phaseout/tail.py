"""Demand after 2060: the user's tuner table stops in 2060, but the page curve the run uses (demand_page_n0.json) carries
on and falls away (1,166 a year in 2060, 320 in 2072, 78 in 2080: replacement of today's fleet only, and as much again
for growth). An fps launched in 2045 or 2050 sells mostly after 2060, so the late rounds rest on years the user never set.

Re-values every round's Boeing grid (every plan, every column, from the state each round started in) under three
demand tails, everything else as the run (sd_options_phaseout.json):
  as run    - the page curve after 2060 (must give back the run's grids_rN.json to the cent: checked)
  held      - the page curve to 2060, then held at its 2060 value
  game      - the page curve to 2060, then the conservative game's curve (demand_conservative.json: rising to 2,400)
and reports, per round, each fps plan against Do Nothing (worst column and the Board's expected column) and whether any
fps plan would pass the Board's tests. Writes data/tail.json and data/curves/*.json.

  python3 tail.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

M, R, B, SD = L.M, L.R, L.B, L.SD
DG = os.path.join(HERE, "..", "..", "dashgame")
O = {k: v for k, v in json.load(open(os.path.join(DG, "sd_options_phaseout.json"))).items() if not k.startswith("_")}
REC = os.path.join(HERE, "record")
CONS = os.path.join(HERE, "..", "dash-2050-cons", "record")
YEARS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
CUT = 2060
DN = "fps: hold + 787: hold"
# Boeing's expected column, per round, as its CEO weighted it (record/exco_result_rN.json, decision/expected_scenario):
# 2030 S2 alone (his expected column; the third on an A350 Re-engine was his downside view, not his column); 2035 S1 70% / S3 30%; 2045 and 2050 S1 80% / S2 20%
EXPECTED = {1: {1: 1.0}, 2: {0: 0.7, 2: 0.3}, 3: {0: 0.8, 1: 0.2}, 4: {0: 0.8, 1: 0.2}}


def curve(name, tail):
    page = json.load(open(os.path.join(DG, "demand_page_n0.json")))
    game = json.load(open(os.path.join(DG, "demand_conservative.json")))
    gm = {y: (r, g) for y, r, g in zip(game["years"], game["replacements"], game["growth"])}
    pg = {y: (r, g) for y, r, g in zip(page["years"], page["replacements"], page["growth"])}
    years = list(range(min(pg), 2101))
    rep, gro = [], []
    for y in years:
        if y <= CUT:
            r, g = pg[y]
        elif tail == "held":
            r, g = pg[CUT]
        else:
            r, g = gm[min(y, max(gm))]
        rep.append(r)
        gro.append(g)
    os.makedirs(os.path.join(HERE, "data", "curves"), exist_ok=True)
    path = os.path.join(HERE, "data", "curves", name + ".json")
    about = {"held": "page curve (demand_page_n0.json) to %d, held at its %d value after" % (CUT, CUT),
             "game": "page curve (demand_page_n0.json) to %d, the conservative game's curve (demand_conservative.json) after" % CUT}[tail]
    json.dump({"about": about + "; whole single-aisle market, before the game's class share. Built by tail.py.",
               "years": years, "replacements": rep, "growth": gro}, open(path, "w"), indent=0)
    return os.path.abspath(path)


def grid(state, year):
    scen = B.rival_scenarios(state, "boeing", year)
    cov = B.sees_covert(state, "boeing", year)
    out = {}
    for olab, o in B.own_options(state, "boeing", year):
        row = []
        for slab, so in scen:
            orders = {k: dict(v) for k, v in so.items()}
            orders["boeing"] = dict(orders.get("boeing", {}), **o)
            s1, _ = R.adjudicate(state, year, orders)
            row.append(M.value(s1, covert=(cov or slab.startswith("Risk case")), series=False)["boeing"]["pv_delta"])
        out[olab] = row
    return [s for s, _ in scen], out


def main():
    tails = {"as run": dict(O), "held": dict(O, demand_curve=curve("page_n0_held2060", "held")),
             "game": dict(O, demand_curve=curve("page_n0_game2061", "game"))}
    res = {"cut": CUT, "rounds": []}
    for n, year in YEARS.items():
        st = json.load(open(os.path.join(REC, "state_r%d.json" % (n - 1))))
        assert st == json.load(open(os.path.join(CONS, "state_r%d.json" % (n - 1)))), n
        rec = json.load(open(os.path.join(REC, "grids_r%d.json" % n)))["boeing"]
        played = {x["plan"]: [c[0] for c in x["cells"]] for x in rec["rows"]}
        rr = {"round": n, "year": year, "tails": {}}
        for tname, opts in tails.items():
            with L.patched(options=opts):
                cols, g = grid(st, year)
            if tname == "as run":
                worst = max(abs(a - b) for p in played for a, b in zip(played[p], g[p]))
                assert worst < 1e-9, (n, worst)
                print("round %d: 'as run' gives back grids_r%d.json (worst gap %.1e)" % (n, n, worst))
            w = EXPECTED[n]
            items = {p: [a - b for a, b in zip(g[p], g[DN])] for p in g if p != DN}
            fps = {p: v for p, v in items.items() if not p.startswith("fps: hold")}
            best_e = max(fps, key=lambda p: sum(fps[p][i] * x for i, x in w.items()))
            best_w = max(fps, key=lambda p: min(fps[p]))
            ren = "fps 10-yr at Renton + 787: hold"
            rr["tails"][tname] = {"columns": cols, "dn_row": g[DN], "items": items,
                                  "ren_worst": min(items[ren]), "ren_expected": sum(items[ren][i] * x for i, x in w.items()),
                                  "best_expected_plan": best_e, "best_expected": sum(fps[best_e][i] * x for i, x in w.items()),
                                  "best_worst_plan": best_w, "best_worst": min(fps[best_w]),
                                  "any_fps_passes_business_case": any(sum(v[i] * x for i, x in w.items()) > 1.0 for v in fps.values())}
            t = rr["tails"][tname]
            print("  %-7s 10-yr Renton worst %+6.2f expected %+6.2f | best fps plan (expected) %s %+6.2f | any > +$1B: %s"
                  % (tname, t["ren_worst"], t["ren_expected"], best_e, t["best_expected"], t["any_fps_passes_business_case"]))
        res["rounds"].append(rr)
    json.dump(res, open(os.path.join(HERE, "data", "tail.json"), "w"), indent=1)
    print("wrote data/tail.json")


if __name__ == "__main__":
    main()
