"""Score the previous ExCo game (run dash-2050-exco, same board v3, base objectives) on Control's added objectives, so
the two games can be compared on the same yardstick. Writes data/compare_prev.json.

The previous game was played without these objectives; this only measures where its decisions left each player on
them: Boeing's net-debt tracker (as played, base and stress), the engine sources on each airframer's narrowbody and
the narrowbody engine makers by year, and Rolls-Royce's narrowbody exposure and NB+WB strain.

  python3 make_compare_prev.py     (needs ../../runs/dash-2050-exco/state_r1..4.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["DASH_RUN"] = "dash-2050-exco"
os.environ["DASH_BOARD"] = "v3"
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
import briefs as B  # noqa: E402
import finance as FIN  # noqa: E402
import model as M  # noqa: E402

RUN = os.path.join(HERE, "..", "..", "runs", "dash-2050-exco")
out = {"run": "dash-2050-exco", "rounds": []}
F = FIN.inputs()
for n in range(1, 5):
    s = json.load(open(os.path.join(RUN, "state_r%d.json" % n)))
    v = M.value(s, covert=True, series=True)
    yrs = list(range(2030, M.REPORT_END + 1))
    _, strain, _, _ = M.engine_costs(s)
    out["rounds"].append({
        "round": n, "year": s["year"],
        "objectives": {side: [{"label": lab, "met": ok, "detail": det} for lab, ok, det in B.control2_status(side, s, v)]
                       for side in ("boeing", "airbus", "rolls_royce")},
        "debt_base": FIN.debt_path(s, v, F, covert=True),
        "debt_stress": FIN.debt_path(s, v, F, F["stress_fcf_scale"], covert=True),
        "sources": {side: {str(y): list(B.nb_sources(s, side, y)) for y in yrs} for side in ("boeing", "airbus")},
        "makers": {str(y): B.nb_engine_makers(v, y) for y in yrs},
        "rr_nb_exposure": B.rr_nb_exposure(s), "rr_strain": strain["rolls_royce"],
        "codes": s["codes"],
    })
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
with open(os.path.join(HERE, "data", "compare_prev.json"), "w") as f:
    json.dump(out, f, indent=1)
for r in out["rounds"]:
    print(r["round"], r["year"], {k: [o["met"] for o in x] for k, x in r["objectives"].items()},
          "fps 2050:", r["sources"]["boeing"]["2050"], "NGSA 2050:", r["sources"]["airbus"]["2050"],
          "RR NB $%.2fB" % r["rr_nb_exposure"])
