"""How many aircraft COMAC selling its capacity first takes from Boeing, under Do Nothing and under the 10-yr fps at
Renton: Boeing's 737/A320-class deliveries with and without the COMAC tier, everything else as the 2030 bridge's step
before it (your page's demand, the MAX phase-out, Airbus's extra lines), in the 2030 brief's column that matches what
Airbus did (NGSA on the A320 Alt plan). Writes data/comac_units.json.

  python3 comac_units.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

O = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json")))
PRE = {"demand_curve": "demand_page_n0.json", "max_phaseout": O["max_phaseout"], "airbus_extra": O["airbus_extra"]}
POST = dict(PRE, third_party={"comac": O["third_party"]["comac"], "comac_first": 1.0, "willing": 1.0})
PERIODS = [(2035, 2039), (2040, 2044), (2045, 2049), (2050, 2059), (2060, 2079)]


def units(opts, plan, ci):
    with L.patched(options=opts):
        st, cv = L.grid_states(plan)[ci]
        v = L.M.value(st, covert=cv, series=True)
    return {r["year"]: r["boeing"]["nb_units"] for r in v["_af_series"]["years"]}


def main():
    ci = L.SCEN_LABELS.index("Airbus launches NGSA on the A320 Alt plan")
    out = {"column": L.SCEN_LABELS[ci], "periods": PERIODS, "plans": {}}
    for plan in (L.PLAN_DN, L.PLAN_REN):
        a, z = units(PRE, plan, ci), units(POST, plan, ci)
        taken = {y: a[y] - z[y] for y in a}
        assert min(taken.values()) > -1e-6, plan          # COMAC never adds to Boeing's sales
        out["plans"][plan] = {"by_period": [sum(taken.get(y, 0.0) for y in range(p, q + 1)) for p, q in PERIODS],
                              "total": sum(taken.values())}
        print(plan, [round(x) for x in out["plans"][plan]["by_period"]], round(out["plans"][plan]["total"]))
    json.dump(out, open(os.path.join(HERE, "data", "comac_units.json"), "w"), indent=1)
    print("wrote data/comac_units.json")


if __name__ == "__main__":
    main()
