"""Who picks up what, inside the phase-out world: the final state of the game (record/state_r4.json) valued with the
run's own options, then with one assumption switched off at a time, everything else as the run:
  no phase-out  - the MAX line keeps its rate after 2045 (max_phaseout off)
  no COMAC      - COMAC sells nothing (its capacity at 0 every year)
Sums 2045-60 deliveries by maker, and customers lost, and records the customers still waiting at the end of 2044 (they
are delivered from 2045, so a case's 2045-60 deliveries need not balance against another's). Writes data/who_picks_up.json.

  python3 who_picks_up.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

M = L.M
O = {k: v for k, v in json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json"))).items() if not k.startswith("_")}
CASES = {"as run": O, "no phase-out": dict(O, max_phaseout=None),
         "no COMAC": dict(O, third_party=dict(O["third_party"], comac={"2026": 0}))}
KEYS = ("boeing", "airbus", "comac", "entrant", "lost")


def market(opts):
    st = json.load(open(os.path.join(HERE, "record", "state_r4.json")))
    with L.patched(options=opts):
        v = M.value(st, covert=True, series=True)
    out = {}
    w44 = None
    for r in v["_af_series"]["years"]:
        sd = r.get("sd", {})
        out[r["year"]] = {"boeing": r["boeing"]["nb_units"], "airbus": r["airbus"]["nb_units"], "comac": sd.get("dlv_comac", 0.0),
                          "entrant": sd.get("dlv_entrant", 0.0), "lost": sd.get("lost") or 0.0}
        if r["year"] == 2044:
            w44 = sd["backlog_b"] + sd["backlog_a"]
    return out, w44


def main():
    res = {"years": [2045, 2060], "cases": {}}
    for name, opts in CASES.items():
        m, w44 = market(opts)
        res["cases"][name] = {k: sum(m[y][k] for y in range(2045, 2061)) for k in KEYS}
        res["cases"][name]["waiting_end_2044"] = w44
        print("%-13s" % name, {k: round(v) for k, v in res["cases"][name].items()})
    ext = json.load(open(os.path.join(HERE, "data", "dash-2050-phaseout.json")))["market"]
    want = {k: sum(x[k] or 0.0 for x in ext if 2045 <= x["year"] <= 2060) for k in KEYS}
    assert all(abs(want[k] - res["cases"]["as run"][k]) < 1e-6 for k in KEYS), (want, res["cases"]["as run"])
    for name in ("no phase-out", "no COMAC"):
        res["effect_of_" + name.replace("no ", "").replace(" ", "_").replace("-", "_").lower()] = {
            k: res["cases"]["as run"][k] - res["cases"][name][k] for k in KEYS + ("waiting_end_2044",)}
    print({k: {a: round(b) for a, b in v.items()} for k, v in res.items() if k.startswith("effect")})
    json.dump(res, open(os.path.join(HERE, "data", "who_picks_up.json"), "w"), indent=1)
    print("wrote data/who_picks_up.json")


if __name__ == "__main__":
    main()
