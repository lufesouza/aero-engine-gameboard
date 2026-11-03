"""The strategic premium that would flip Boeing's fps decision in the MAX phase-out game: a value the numbers do not
count (the weight of jobs and Washington, Boeing's brand as an engineering company, not leaving the narrowbody market
to Airbus and COMAC), added to every plan with an fps in every column of a round's brief, and found as the smallest
amount at which Boeing's decision rule (thresholds.decide, each of its four readings) launches an fps.

Adding S to every fps plan is the same, for every test in the rule, as charging S to the plans without one (Do Nothing
and the 787 Re-engine alone): every test compares a plan with another (an fps plan against its plan without the fps,
or against the plan beside it), so S is the weight Boeing would have to put on not leaving.

It reads the values data/franchise.json stores for each round (every plan in every column at the base margin and the
bill as briefed), for the brief alone and with the franchise terms, at 10.5% and 8.1%, and reports S in money of 2026
and of the decision year (S / discount factor of that year at the rate).

  python3 premium.py            writes data/premium.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import thresholds as T  # noqa: E402

FR = json.load(open(os.path.join(HERE, "data", "franchise.json")))
FPS = list(T.SOLO) + list(T.PAIRS)
RATES = FR["rates"]
KEYS = [("base", "game"), ("base", "full"), ("low", "full"), ("high", "full"), ("tail as run", "full")]


def with_premium(V, s):
    return {name: [x + (s if name in FPS else 0.0) for x in xs] for name, xs in V.items()}


def solve(n, key):
    r = FR["rounds"][str(n)]
    p = r["thresholds"][key]["points"]["base"]
    V = p["values"]
    cols = [{"label": c} for c in r["columns"]]
    rws = {"Do Nothing": {"cols": cols}}
    dec0 = T.decide(n, rws, vals=V)
    assert all(dec0[md] == r["thresholds"][key]["base"][md] for md in T.MODES), (n, key)     # the stored decision
    out = {}
    for md in T.MODES:
        f = lambda s: T.decide(n, rws, vals=with_premium(V, s))[md] is not None
        s, mono = T.first(f, 0.0, 40.0, steps=400, tol=1e-6)
        d = T.decide(n, rws, vals=with_premium(V, s + 1e-6)) if s is not None else None
        out[md] = {"S": s, "monotone": mono, "plan": d[md] if d else None, "pick": d["pick"] if d else None}
    return out


def main():
    res = {"about": __doc__.split("\n\n")[0], "fps_plans": FPS, "rounds": {}}
    for n in T.YEARS:
        year = T.YEARS[n]
        rr = {"year": year, "weights": FR["rounds"][str(n)]["weights"], "cases": {}}
        for level, view in KEYS:
            for rname, rate in RATES.items():
                key = "%s|%s|%s" % (level, view, rname)
                o = solve(n, key)
                dfy = (1 + rate) ** -(year - 2026)
                for md in T.MODES:
                    o[md]["S_decision_year"] = None if o[md]["S"] is None else o[md]["S"] / dfy
                rr["cases"][key] = o
                print(n, key, {md: (None if o[md]["S"] is None else round(o[md]["S"], 2), o[md]["plan"]) for md in T.MODES})
        res["rounds"][str(n)] = rr
    # the brief's own 2030 decision gives the main report's thresholds: no premium is needed where it already launches
    json.dump(res, open(os.path.join(HERE, "data", "premium.json"), "w"), indent=1)
    print("wrote data/premium.json")


if __name__ == "__main__":
    main()
