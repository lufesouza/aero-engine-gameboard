"""737s Boeing sells each year under Do Nothing, on the user's page demand (chart 4.1, retirement 0-4 years later), run
dash-2050-cons. The case is Airbus launching NGSA (in service 2037), the narrowbody market in Boeing's expected case; the
A350 Re-engine column has the same narrowbody market. Writes do_nothing_737.json and do_nothing_737.png next to this file.

  python3 do_nothing_737.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import demand_scenarios as D  # noqa: E402

L, M = D.L, D.M
Y0, Y1 = 2026, 2060


def series(kw):
    with L.patched(**kw):
        st, cv = L.grid_states(L.PLAN_DN)[1]           # column S2: Airbus launches NGSA
        v = M.value(st, covert=cv, series=True)
    rows = {r["year"]: r for r in v["_af_series"]["years"] if Y0 <= r["year"] <= Y1}
    for r in rows.values():                                # Do Nothing: every Boeing narrowbody is a 737
        assert r["boeing"].get("nb_units_new", 0.0) == 0.0
    return ({y: rows[y]["boeing"]["nb_units"] for y in rows}, {y: rows[y]["sd"]["cap_max"] for y in rows},
            {y: rows[y]["boeing"]["sd"]["sq_delivered"] for y in rows})


def main():
    out = {"case": "Do Nothing, Airbus launches NGSA (2037)", "years": list(range(Y0, Y1 + 1)), "sold": {}, "capacity": None}
    for n in D.NS:
        sold, cap, sq = series(D.demand_kw(n))
        out["sold"][n] = [sold[y] for y in out["years"]]
        out["capacity"] = [cap[y] for y in out["years"]]
    sold, _, _ = series({})
    out["sold"]["game"] = [sold[y] for y in out["years"]]
    json.dump(out, open(os.path.join(HERE, "do_nothing_737.json"), "w"), indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ys = out["years"]
    lab = {"0": "As chapter 1 sets out", "1": "1 year later", "2": "2 years later", "3": "3 years later", "4": "4 years later"}
    ramp = ["#9dc0ea", "#6fa2e0", "#2a78d6", "#1c5aa6", "#123e76"]
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
    ax.plot(ys, out["capacity"], color="#8a95a5", lw=1.5, ls=(0, (5, 4)), label="737 capacity")
    ax.plot(ys, out["sold"]["game"], color="#b7c0cc", lw=2, label="Game's own demand curve")
    for n, c in zip(D.NS, ramp):
        ax.plot(ys, out["sold"][n], color=c, lw=2, label="Retiring " + lab[n].lower() if n != "0" else "Retiring as chapter 1 sets out")
    ax.axvline(2037, color="#556275", lw=1)
    ax.text(2037.3, 770, "NGSA in service", color="#556275", fontsize=9)
    ax.set_xlim(Y0, Y1)
    ax.set_ylim(0, 800)
    ax.set_ylabel("737s sold a year")
    ax.grid(axis="y", color="#e3e8ef")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Do Nothing: Boeing sells every 737 it can build until the late 2040s, then demand runs out",
                 loc="left", fontsize=11.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left", ncol=2)
    fig.text(0.01, 0.01, "Do Nothing, Airbus launches NGSA in 2037 (Boeing's expected case). Your page's demand from 2038, the game's "
             "conservative curve before. BOEING PROPRIETARY.", fontsize=7.5, color="#556275")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(HERE, "do_nothing_737.png"))
    for n in list(D.NS) + ["game"]:
        s = dict(zip(ys, out["sold"][n]))
        full = [y for y in ys if s[y] >= out["capacity"][ys.index(y)] - 1]
        print(n, "sold 2038-60 %.0f" % sum(s[y] for y in ys if y >= 2038), "| at capacity", full[:1], "..", full[-1:],
              "| 2045 %.0f 2050 %.0f 2055 %.0f 2060 %.0f" % (s[2045], s[2050], s[2055], s[2060]))


if __name__ == "__main__":
    main()
