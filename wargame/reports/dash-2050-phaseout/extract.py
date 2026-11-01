"""Facts for the dash-2050-phaseout report, from one run's record (run it once per run: the run's options are read at
import). Writes data/<run>.json: the orders and values round by round, Boeing's fps rows against Do Nothing in each
round's brief, and the final state's market year by year (deliveries by maker, COMAC and the new entrant, capacity,
preference and delivered share, customers lost).

  DASH_RUN=dash-2050-phaseout DASH_BOARD=v3 python3 extract.py
  DASH_RUN=dash-2050-cons DASH_BOARD=v3 python3 extract.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.environ["DASH_RUN"]
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
import model as M  # noqa: E402

REC = os.path.join(HERE, "..", RUN, "record")
FPS_ROWS = ("fps 10-yr at Renton + 787: hold", "fps 10-yr + 787: hold", "fps 7-yr at Renton + 787: hold", "fps via Embraer at Renton + 787: hold")


def main():
    out = {"run": RUN, "rounds": []}
    for n in (1, 2, 3, 4):
        r = json.load(open(os.path.join(REC, "record_r%d.json" % n)))
        g = json.load(open(os.path.join(REC, "grids_r%d.json" % n)))["boeing"]
        rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
        dn = rows["fps: hold + 787: hold"]
        fps = {p: [a - b for a, b in zip(rows[p], dn)] for p in FPS_ROWS if p in rows}
        out["rounds"].append({"round": n, "year": r["year"], "orders": r["orders"], "log": [x for x in r["log"] if "[covert]" not in x],
                              "value": {s: r["value"][s]["pv_delta"] for s in r["value"]}, "fps_vs_dn": fps,
                              "columns": g["scenarios"], "dn_row": dn})
    st = json.load(open(os.path.join(REC, "state_r4.json")))
    v = M.value(st, covert=True, series=True)
    yrs = []
    for r in v["_af_series"]["years"]:
        y = r["year"]
        if 2026 <= y <= 2060:
            sd = r.get("sd", {})
            yrs.append({"year": y, "demand": sd.get("demand_gross"), "boeing": r["boeing"]["nb_units"], "airbus": r["airbus"]["nb_units"],
                        "comac": sd.get("dlv_comac", 0.0), "entrant": sd.get("dlv_entrant", 0.0), "lost": sd.get("lost"),
                        "cap_max": sd.get("cap_max"), "cap_airbus": (sd.get("cap_a320") or 0.0) + (sd.get("cap_ngsa") or 0.0),
                        "boeing_share": r["boeing"].get("nb_share"), "boeing_pref": r["boeing"].get("nb_pref_share"),
                        "boeing_wb_share": r["boeing"].get("wb_share")})
    out["market"] = yrs
    out["final_value"] = {s: v[s]["pv_delta"] for s in M.SIDES}
    out["boeing_bridge"] = v["boeing"]["bridge"]
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "data", RUN + ".json"), "w"), indent=1)
    print("wrote data/%s.json" % RUN, {s: round(x, 2) for s, x in out["final_value"].items()})


if __name__ == "__main__":
    main()
