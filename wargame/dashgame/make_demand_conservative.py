"""Build demand_conservative.json: an annual single-aisle demand curve for the game, 2026-2070, from the user's
"Conservative case, single-aisle aircraft per year" table (14 Oct 2026).

The table gives eleven years (2026, 2030, 2035, 2040, 2045, 2050, 2051, 2055, 2060, 2065, 2070), each split into
replacement of old-generation aircraft, replacement of today's 737 MAX / A320neo / A220 fleets, replacement of aircraft
delivered after 2026, and fleet growth, with the fleet at year end, plus four period totals (2026-45, 2046-55,
2056-65, 2066-70). The game needs every year. This script finds the smoothest annual curve (least squared second
differences, component by component) that
  - passes exactly through every component value of the table,
  - matches the four period totals exactly,
  - keeps the year-end fleet (19.7k in 2026 plus each year's growth) close to the table's fleet column (soft,
    the column is rounded to 0.1k),
  - ends old-generation replacement after 2045: the table has 336 in 2045 and 0 in 2050, and the 2046-55 total
    (18.7k) is met only if the old-generation fleet is used up by 2046 (a straight run-down to 2050 would add about
    650 aircraft to that period),
  - has no replacement of post-2026 deliveries before 2046 (the table has 0 to 2045).
Values are whole single-aisle market (A220 included), before the game's 737/A320 class share. After 2070 the game
holds the 2070 values.

Usage: python3 make_demand_conservative.py   (needs numpy; writes demand_conservative.json next to this file)
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = "user's table 'Conservative case, single-aisle aircraft per year' (14 Oct 2026)"
# year: (old-gen repl., MAX/neo/A220 repl., post-2026 repl., total repl., growth, total, repl. share, fleet k)
TABLE = {2026: (125, 0, 0, 125, 638, 763, .16, 19.7), 2030: (735, 20, 0, 755, 728, 1483, .51, 22.5),
         2035: (820, 140, 0, 960, 858, 1818, .53, 26.5), 2040: (577, 310, 0, 887, 1012, 1899, .47, 31.3),
         2045: (336, 600, 0, 936, 1193, 2130, .44, 36.9), 2050: (0, 880, 11, 891, 1062, 1953, .46, 42.5),
         2051: (0, 915, 19, 934, 1022, 1957, .48, 43.5), 2055: (0, 790, 122, 912, 825, 1737, .53, 47.1),
         2060: (0, 560, 574, 1134, 498, 1632, .69, 50.3), 2065: (0, 360, 1312, 1672, 523, 2195, .76, 52.9),
         2070: (0, 180, 1801, 1981, 550, 2531, .78, 55.6)}
PERIODS = [((2026, 2045), 33700), ((2046, 2055), 18700), ((2056, 2065), 18100), ((2066, 2070), 12200)]
Y0, Y1 = 2026, 2070
OLD_ZERO_FROM = 2050                # old-generation replacement is 0 from here (the table: 0 in 2050 and after)
POST_ZERO_TO = 2045                 # post-2026 replacement is 0 up to here (the table: 0 to 2045)
FLEET_TOL = 50.0                    # the fleet column is rounded to 0.1k: the curve's fleet stays within +/-50
COMPS = ["old_gen", "max_neo_a220", "post_2026", "growth"]
COL = {"old_gen": 0, "max_neo_a220": 1, "post_2026": 2, "growth": 4}


def problem():
    """Variables, the roughness matrix, equality constraints (anchors, period totals) and inequality constraints
    (non-negativity, fleet band). Every component is a full 2026-2070 series; values the table fixes at zero are
    constants, so the roughness also counts how a component runs into and out of them."""
    years = list(range(Y0, Y1 + 1))
    fixed0 = {("old_gen", y) for y in years if y >= OLD_ZERO_FROM} | {("post_2026", y) for y in years if y <= POST_ZERO_TO}
    idx, k = {}, 0
    for c in COMPS:
        for y in years:
            if (c, y) not in fixed0:
                idx[(c, y)] = k
                k += 1
    m = k
    rows = []
    for c in COMPS:
        for a, b, cc in zip(years, years[1:], years[2:]):
            r = np.zeros(m)
            for yy, w in ((a, 1.0), (b, -2.0), (cc, 1.0)):
                if (c, yy) in idx:
                    r[idx[(c, yy)]] += w
            if r.any():
                rows.append(r)
    R = np.array(rows)
    Q = R.T @ R
    E, e = [], []
    for y, t in TABLE.items():
        for c in COMPS:
            if (c, y) in idx:
                a = np.zeros(m); a[idx[(c, y)]] = 1.0
                E.append(a); e.append(float(t[COL[c]]))
            else:
                assert t[COL[c]] == 0, (c, y)
    for (lo, hi), tot in PERIODS:
        a = np.zeros(m)
        for c in COMPS:
            for y in range(lo, hi + 1):
                if (c, y) in idx:
                    a[idx[(c, y)]] = 1.0
        E.append(a); e.append(float(tot))
    G, g = [], []                                     # G x >= g
    for key, i in idx.items():
        a = np.zeros(m); a[i] = 1.0
        G.append(a); g.append(0.0)
    for y, t in TABLE.items():
        if y == Y0:
            continue
        a = np.zeros(m)
        for yy in range(Y0 + 1, y + 1):
            a[idx[("growth", yy)]] = 1.0
        target = t[7] * 1000 - TABLE[Y0][7] * 1000
        G.append(a.copy()); g.append(target - FLEET_TOL)
        G.append(-a); g.append(-(target + FLEET_TOL))
    return years, idx, Q, np.array(E), np.array(e), np.array(G), np.array(g)


def solve_qp(Q, E, e, G, g, tol=1e-7, max_iter=500):
    """min x'Qx  s.t.  E x = e,  G x >= g, by a primal-dual active set: active inequalities are solved as equalities;
    the most violated inactive one is added, an active one with a multiplier of the wrong sign is dropped."""
    n = Q.shape[0]
    W = []
    for _ in range(max_iter):
        A = np.vstack([E] + [G[W]]) if W else E
        b = np.concatenate([e, g[W]]) if W else e
        K = np.block([[2 * Q, A.T], [A, np.zeros((A.shape[0], A.shape[0]))]])
        sol = np.linalg.lstsq(K, np.concatenate([np.zeros(n), b]), rcond=None)[0]
        x, lam = sol[:n], sol[n:]
        mu = -lam[len(e):]                           # multipliers of the active inequalities (must be >= 0)
        if W and mu.min() < -tol:
            W.pop(int(np.argmin(mu)))
            continue
        viol = g - G @ x
        viol[W] = -np.inf
        j = int(np.argmax(viol))
        if viol[j] <= tol:
            return x, W
        W.append(j)
    raise RuntimeError("active set did not settle")


def solve():
    years, idx, Q, E, e, G, g = problem()
    x, W = solve_qp(Q, E, e, G, g)
    n_bounds = len(idx)
    held = sorted([key for key, i in idx.items() if i in W])
    fleet_bound = len([w for w in W if w >= n_bounds])
    out = {c: [max(0.0, float(x[idx[(c, y)]])) if (c, y) in idx else 0.0 for y in years] for c in COMPS}
    return years, out, held, fleet_bound, float(x @ Q @ x)


def main():
    years, comp, held, fleet_bound, rough = solve()
    rep = [comp["old_gen"][i] + comp["max_neo_a220"][i] + comp["post_2026"][i] for i in range(len(years))]
    tot = [rep[i] + comp["growth"][i] for i in range(len(years))]
    fleet = [TABLE[Y0][7] * 1000]
    for i in range(1, len(years)):
        fleet.append(fleet[-1] + comp["growth"][i])
    # checks
    checks = {"anchors_max_abs_error": 0.0, "periods": [], "fleet": [], "min_value": min(min(v) for v in comp.values())}
    for y, t in TABLE.items():
        i = years.index(y)
        for c in COMPS:
            checks["anchors_max_abs_error"] = max(checks["anchors_max_abs_error"], abs(comp[c][i] - t[COL[c]]))
        checks["fleet"].append({"year": y, "table_k": t[7], "curve_k": round(fleet[i] / 1000, 4)})
    for (lo, hi), target in PERIODS:
        s = sum(tot[years.index(y)] for y in range(lo, hi + 1))
        checks["periods"].append({"period": f"{lo}-{hi}", "table": target, "curve": round(s, 1)})
    assert checks["anchors_max_abs_error"] < 1e-6
    assert all(abs(p["curve"] - p["table"]) < 1e-6 for p in checks["periods"])
    assert all(abs(f["curve_k"] - f["table_k"]) <= FLEET_TOL / 1000 + 1e-9 for f in checks["fleet"]), checks["fleet"]
    assert checks["min_value"] > -1e-6, checks["min_value"]
    out = {"source": SOURCE, "about": __doc__, "years": years,
           "components": {c: [round(v, 2) for v in comp[c]] for c in COMPS},
           "replacements": [round(v, 2) for v in rep], "growth": [round(v, 2) for v in comp["growth"]],
           "total": [round(v, 2) for v in tot], "fleet_end_year": [round(v, 1) for v in fleet],
           "table": {str(y): dict(zip(["old_gen", "max_neo_a220", "post_2026", "total_replacement", "growth", "total",
                                       "replacement_share", "fleet_k"], t)) for y, t in TABLE.items()},
           "periods_table": {f"{lo}-{hi}": v for (lo, hi), v in PERIODS},
           "method": {"objective": "least squared second differences, each component, over 2026-2070",
                      "old_gen_zero_from": OLD_ZERO_FROM, "post_2026_zero_to": POST_ZERO_TO, "fleet_tolerance": FLEET_TOL,
                      "held_at_zero": [f"{c} {y}" for c, y in held], "fleet_bounds_active": fleet_bound,
                      "roughness": rough, "solver": "primal-dual active set (exact KKT)",
                      "after_last_year": "the game holds the 2070 values"},
           "checks": checks,
           "note": "whole single-aisle market, A220 included; the game applies its 737/A320 class share once, in "
                   "supply_demand.demand(). Two table totals are one above their parts (2045: 2,130 against 936 + 1,193; "
                   "2051: 1,957 against 934 + 1,022): rounding; the curve keeps the parts."}
    path = os.path.join(HERE, "demand_conservative.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)
    print("periods", [(p["period"], p["table"], p["curve"]) for p in checks["periods"]])
    print("fleet", [(f["year"], f["table_k"], f["curve_k"]) for f in checks["fleet"]])
    print("min value %.2f; held at zero: %s; fleet bounds active %d; roughness %.1f" % (checks["min_value"], held, fleet_bound, rough))
    for y in years:
        i = years.index(y)
        print(y, " ".join("%7.1f" % comp[c][i] for c in COMPS), " | repl %7.1f total %7.1f fleet %7.0f" % (rep[i], tot[i], fleet[i]))


if __name__ == "__main__":
    main()
