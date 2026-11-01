"""Why the 2030 fps case moves between the conservative-case game and the phase-out game: switch the phase-out run's
assumptions on one at a time over dash-2050-cons's round-1 market and read Boeing's expected fps-vs-Do Nothing value
(10-yr fps at Renton, the brief's 50/50 columns). Writes data/steps_2030.json.

  python3 steps.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

O = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json")))
TP = O["third_party"]
STEPS = [("Conservative-case game (as played)", {}),
         ("+ your page's demand", {"demand_curve": "demand_page_n0.json"}),
         ("+ MAX phase-out 2045-2060", {"max_phaseout": O["max_phaseout"]}),
         ("+ Airbus extra lines from 2045", {"airbus_extra": O["airbus_extra"]}),
         ("+ COMAC selling its capacity first", {"third_party": {"comac": TP["comac"], "comac_first": 1.0, "willing": 1.0}}),
         ("+ new entrant from 2040 (takes leftovers)", {"third_party": TP})]


def main():
    acc, out, prev = {}, [], None
    for lab, add in STEPS:
        acc.update(add)
        with L.patched(options=dict(acc)):
            items, row, dn = L.grid_items(L.PLAN_REN)
            v = L.expected(items)
        out.append({"step": lab, "item": v, "change": 0.0 if prev is None else v - prev, "fps_vs_sq": L.expected(row),
                    "dn_vs_sq": L.expected(dn)})
        prev = v
        print("%-44s %+6.2f  %s" % (lab, v, "" if len(out) == 1 else "%+.2f" % out[-1]["change"]))
    # the last step must be the run's own options
    full = {k: v for k, v in O.items() if not k.startswith("_")}
    with L.patched(options=full):
        v_full = L.expected(L.grid_items(L.PLAN_REN)[0])
    assert abs(v_full - out[-1]["item"]) < 1e-9, (v_full, out[-1]["item"])
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    json.dump({"plan": "fps 10-yr at Renton + 787: hold, against Do Nothing", "round": 1, "year": 2030, "steps": out},
              open(os.path.join(HERE, "data", "steps_2030.json"), "w"), indent=1)
    print("wrote data/steps_2030.json (last step = the run's own options: %+.2f)" % v_full)


if __name__ == "__main__":
    main()
