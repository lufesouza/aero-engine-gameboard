"""Why Boeing's fps case moves between the conservative-case game and the phase-out game: switch the phase-out run's
assumptions on one at a time and read Boeing's 10-yr fps at Renton against Do Nothing, as the brief values it.

Both bridges read the brief column that matches what Airbus then did ("item"; every column is kept in "items"):
- 2030 (round 1): over dash-2050-cons's round-1 market; Airbus launched NGSA on the A320 Alt plan (column S3).
- 2050 (round 4): over the state both games reached after round 3 (identical: same moves); Airbus held (column S1).
The first and last steps must give back each game's own grid (grids_rN.json), every column.

Writes data/steps_2030.json and data/steps_2050.json.

  python3 steps.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

M, R, B = L.M, L.R, L.B
O = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json")))
TP = O["third_party"]
STEPS = [("Conservative-case game (as played)", {}),
         ("+ your page's demand", {"demand_curve": "demand_page_n0.json"}),
         ("+ MAX phase-out 2045-2060", {"max_phaseout": O["max_phaseout"]}),
         ("+ Airbus extra lines from 2045", {"airbus_extra": O["airbus_extra"]}),
         ("+ COMAC selling its capacity first", {"third_party": {"comac": TP["comac"], "comac_first": 1.0, "willing": 1.0}}),
         ("+ new entrant from 2040 (takes leftovers)", {"third_party": TP})]
REC = os.path.join(HERE, "record")
CONS = os.path.join(HERE, "..", "dash-2050-cons", "record")
PLAN_DN, PLAN_REN = L.PLAN_DN, L.PLAN_REN


COL = {2030: "Airbus launches NGSA on the A320 Alt plan", 2050: "Rivals hold"}


def check(n, first, last):
    """The first and last steps give back each game's own round-n grid, every column."""
    for path, step in ((CONS, first), (REC, last)):
        g = json.load(open(os.path.join(path, "grids_r%d.json" % n)))["boeing"]
        rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
        want = [a - b for a, b in zip(rows[PLAN_REN], rows[PLAN_DN])]
        assert all(abs(a - b) < 1e-9 for a, b in zip(want, step["items"])), (path, want, step["items"])


def bridge_2030():
    acc, out, prev = {}, [], None
    ci = L.SCEN_LABELS.index(COL[2030])
    for lab, add in STEPS:
        acc.update(add)
        with L.patched(options=dict(acc)):
            items, row, dn = L.grid_items(PLAN_REN)
        v = items[ci]
        out.append({"step": lab, "items": items, "item": v, "change": 0.0 if prev is None else v - prev,
                    "expected_50_50": L.expected(items), "dn_vs_sq": dn})
        prev = v
        print("2030 %-44s %s  %s" % (lab, " ".join("%+6.2f" % x for x in items), "" if len(out) == 1 else "%+.2f" % out[-1]["change"]))
    check(1, out[0], out[-1])
    return {"plan": "fps 10-yr at Renton + 787: hold, against Do Nothing", "round": 1, "year": 2030, "columns": L.SCEN_LABELS,
            "column": COL[2030], "basis": "the brief column matching what Airbus did", "steps": out}


def grid_2050(state):
    scen = B.rival_scenarios(state, "boeing", 2050)
    own = dict(B.own_options(state, "boeing", 2050))
    covert = B.sees_covert(state, "boeing", 2050)
    rows = {}
    for plan in (PLAN_DN, PLAN_REN):
        row = []
        for slab, so in scen:
            orders = {k: dict(v) for k, v in so.items()}
            orders["boeing"] = dict(orders.get("boeing", {}), **own[plan])
            s1, _ = R.adjudicate(state, 2050, orders)
            row.append(M.value(s1, covert=(covert or slab.startswith("Risk case")), series=False)["boeing"]["pv_delta"])
        rows[plan] = row
    return [s for s, _ in scen], [a - b for a, b in zip(rows[PLAN_REN], rows[PLAN_DN])], rows[PLAN_DN]


def bridge_2050():
    st = json.load(open(os.path.join(REC, "state_r3.json")))
    assert st == json.load(open(os.path.join(CONS, "state_r3.json"))), "the two games reached different states"
    acc, out, prev, cols = {}, [], None, None
    for lab, add in STEPS:
        acc.update(add)
        with L.patched(options=dict(acc)):
            cols, items, dn = grid_2050(st)
        v = items[cols.index(COL[2050])]
        out.append({"step": lab, "items": items, "item": v, "dn_vs_sq": dn, "change": 0.0 if prev is None else v - prev})
        prev = v
        print("2050 %-44s %s  %s" % (lab, " ".join("%+6.2f" % x for x in items), "" if len(out) == 1 else "%+.2f" % out[-1]["change"]))
    check(4, out[0], out[-1])
    return {"plan": "fps 10-yr at Renton + 787: hold, against Do Nothing", "round": 4, "year": 2050, "columns": cols,
            "column": COL[2050], "basis": "the brief column matching what Airbus did", "steps": out}


def main():
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    for name, fn in (("steps_2030.json", bridge_2030), ("steps_2050.json", bridge_2050)):
        json.dump(fn(), open(os.path.join(HERE, "data", name), "w"), indent=1)
        print("wrote data/" + name)


if __name__ == "__main__":
    main()
