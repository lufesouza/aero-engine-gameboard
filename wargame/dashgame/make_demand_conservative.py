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
OLD_LAST = 2045                     # last year of old-generation replacement
POST_FIRST = 2046                   # first year of post-2026 replacement
FLEET_WEIGHT = 1.0                  # soft weight on the fleet column (per aircraft squared), against roughness
COMPS = ["old_gen", "max_neo_a220", "post_2026", "growth"]
COL = {"old_gen": 0, "max_neo_a220": 1, "post_2026": 2, "growth": 4}


def solve(zeros=()):
    """zeros: (component, year) pairs held at 0 (the non-negativity active set)."""
    years = list(range(Y0, Y1 + 1))
    n = len(years)
    free = {"old_gen": [y for y in years if y <= OLD_LAST], "max_neo_a220": years,
            "post_2026": [y for y in years if y >= POST_FIRST], "growth": years}
    idx, k = {}, 0
    for c in COMPS:
        for y in free[c]:
            idx[(c, y)] = k
            k += 1
    m = k
    # roughness: squared second differences inside each component's free range; post-2026 also against the zeros
    # before it (it starts from nothing), old-gen not across its end (the fleet is used up)
    rows = []
    for c in COMPS:
        ys = free[c]
        if c == "post_2026":
            ys = [POST_FIRST - 2, POST_FIRST - 1] + ys
        for a, b, cc in zip(ys, ys[1:], ys[2:]):
            r = np.zeros(m + 1)
            for yy, w in ((a, 1.0), (b, -2.0), (cc, 1.0)):
                if (c, yy) in idx:
                    r[idx[(c, yy)]] += w
            rows.append(r)
    R = np.array(rows)
    Q = R[:, :m].T @ R[:, :m]
    q = np.zeros(m)
    # soft fleet: fleet(y) = 19.7k + sum of growth 2027..y, against the table at each table year after 2026
    for y, t in TABLE.items():
        if y == Y0:
            continue
        a = np.zeros(m)
        for yy in range(Y0 + 1, y + 1):
            a[idx[("growth", yy)]] = 1.0
        target = t[7] * 1000 - TABLE[Y0][7] * 1000
        Q += FLEET_WEIGHT * np.outer(a, a)
        q -= FLEET_WEIGHT * a * target
    # hard constraints: anchors and period totals
    A, b = [], []
    for y, t in TABLE.items():
        for c in COMPS:
            if (c, y) in idx:
                a = np.zeros(m); a[idx[(c, y)]] = 1.0
                A.append(a); b.append(float(t[COL[c]]))
            else:
                assert t[COL[c]] == 0, (c, y)          # outside a component's range the table must be zero
    for (lo, hi), tot in PERIODS:
        a = np.zeros(m)
        for c in COMPS:
            for y in range(lo, hi + 1):
                if (c, y) in idx:
                    a[idx[(c, y)]] = 1.0
        A.append(a); b.append(float(tot))
    for c, y in zeros:
        a = np.zeros(m); a[idx[(c, y)]] = 1.0
        A.append(a); b.append(0.0)
    A, b = np.array(A), np.array(b)
    K = np.block([[2 * Q, A.T], [A, np.zeros((len(b), len(b)))]])
    rhs = np.concatenate([-2 * q, b])
    x = np.linalg.solve(K, rhs)[:m]
    out = {c: [float(x[idx[(c, y)]]) if (c, y) in idx else 0.0 for y in years] for c in COMPS}
    return years, out


def solve_nonneg():
    """Non-negativity by an active set: hold every value that comes out negative at 0 and solve again."""
    zeros = set()
    for _ in range(200):
        years, comp = solve(sorted(zeros))
        neg = {(c, y) for c in COMPS for y, v in zip(years, comp[c]) if v < -1e-9}
        if not neg:
            return years, comp, sorted(zeros)
        zeros |= neg
    raise RuntimeError("active set did not settle")


def main():
    years, comp, held = solve_nonneg()
    comp = {c: [max(0.0, v) for v in vals] for c, vals in comp.items()}      # held values come out as -1e-12
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
        checks["fleet"].append({"year": y, "table_k": t[7], "curve_k": round(fleet[i] / 1000, 3)})
    for (lo, hi), target in PERIODS:
        s = sum(tot[years.index(y)] for y in range(lo, hi + 1))
        checks["periods"].append({"period": f"{lo}-{hi}", "table": target, "curve": round(s, 1)})
    assert checks["anchors_max_abs_error"] < 1e-6
    assert all(abs(p["curve"] - p["table"]) < 1e-6 for p in checks["periods"])
    assert all(abs(f["curve_k"] - f["table_k"]) <= 0.05 + 1e-9 for f in checks["fleet"]), checks["fleet"]
    assert checks["min_value"] > -1e-6, checks["min_value"]
    out = {"source": SOURCE, "about": __doc__, "years": years,
           "components": {c: [round(v, 2) for v in comp[c]] for c in COMPS},
           "replacements": [round(v, 2) for v in rep], "growth": [round(v, 2) for v in comp["growth"]],
           "total": [round(v, 2) for v in tot], "fleet_end_year": [round(v, 1) for v in fleet],
           "table": {str(y): dict(zip(["old_gen", "max_neo_a220", "post_2026", "total_replacement", "growth", "total",
                                       "replacement_share", "fleet_k"], t)) for y, t in TABLE.items()},
           "periods_table": {f"{lo}-{hi}": v for (lo, hi), v in PERIODS},
           "method": {"objective": "least squared second differences, each component", "old_gen_last_year": OLD_LAST,
                      "held_at_zero": [f"{c} {y}" for c, y in held],
                      "post_2026_first_year": POST_FIRST, "fleet_weight": FLEET_WEIGHT,
                      "after_last_year": "the game holds the 2070 values"},
           "checks": checks,
           "note": "whole single-aisle market, A220 included; the game applies its 737/A320 class share once, in "
                   "supply_demand.demand(). The table's 2045 total (2,130) is one above its parts (936 + 1,193): rounding."}
    path = os.path.join(HERE, "demand_conservative.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)
    print("periods", [(p["period"], p["table"], p["curve"]) for p in checks["periods"]])
    print("fleet", [(f["year"], f["table_k"], f["curve_k"]) for f in checks["fleet"]])
    print("min value %.2f; held at zero: %s" % (checks["min_value"], held))
    for y in years:
        i = years.index(y)
        print(y, " ".join("%7.1f" % comp[c][i] for c in COMPS), " | repl %7.1f total %7.1f fleet %7.0f" % (rep[i], tot[i], fleet[i]))


if __name__ == "__main__":
    main()
