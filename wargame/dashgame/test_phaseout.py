"""Checks for the MAX phase-out options of supply_demand (max_phaseout, airbus_extra, third_party), run dash-2050-cons's
market with the user's page demand.

1. With COMAC's first-call share at 0, the engine's Do Nothing rows equal the manual build
   (reports/dash-2050-cons/analysis/max_phaseout/build_scenario.py, every switch on), year by year, exactly.
2. With the run's own options (sd_options_phaseout.json: COMAC sells its capacity first), the engine's Do Nothing rows give
   back the table the user set in the Do Nothing tuner (1 Nov 2026), to the aircraft (half-aircraft rounding aside).
3. Every year's books balance: no maker delivers above its capacity, nothing is negative.

  python3 test_phaseout.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reports", "dash-2050-cons", "analysis"))
sys.path.insert(0, os.path.join(HERE, "..", "reports", "dash-2050-cons", "analysis", "max_phaseout"))
import lib as L  # noqa: E402
import build_scenario as BS  # noqa: E402

M, SD = L.M, L.SD
OPTS = {k: v for k, v in json.load(open(os.path.join(HERE, "sd_options_phaseout.json"))).items() if not k.startswith("_")}
# the user's table (Do Nothing tuner, 1 Nov 2026): year, demand, 737 cap, 737 sold, Airbus cap, Airbus sold, COMAC, entrant, lost
TABLE = """2026 724 510 285 1020 438 0 0 0|2027 905 594 357 1020 548 0 0 0|2028 1084 624 427 1020 657 0 0 0|2029 1257 654 496 1020 762 0 0 0
|2030 1406 684 554 1020 852 0 0 0|2031 1500 684 591 1020 909 0 0 0|2032 1569 684 618 1020 951 0 0 0|2033 1630 684 642 1020 987 0 0 0
|2034 1685 684 664 1020 1020 0 0 0|2035 1724 684 628 1020 947 150 0 0|2036 1721 684 626 1020 940 155 0 0|2037 1712 684 618 935 935 160 0 0
|2038 1402 684 543 694 694 165 0 0|2039 1931 684 684 721 721 170 0 36|2040 1972 684 684 607 607 175 40 79|2041 2046 684 684 749 749 180 80 106
|2042 2090 684 684 907 907 185 120 115|2043 1938 684 684 1018 1018 190 160 92|2044 1825 684 684 1177 1177 195 200 40
|2045 1847 641 641 1340 1247 200 116 0|2046 1904 599 508 1407 1186 210 0 0|2047 1881 556 482 1467 1180 220 0 0|2048 1917 513 472 1527 1215 230 0 0
|2049 1976 470 469 1527 1267 240 0 0|2050 1933 428 428 1527 1250 250 5 0|2051 2016 385 385 1527 1352 250 29 0|2052 2018 342 342 1527 1384 250 42 0
|2053 1838 299 299 1527 1255 250 34 0|2054 1785 257 257 1527 1237 250 42 0|2055 1701 214 214 1527 1191 250 47 0|2056 1622 171 171 1527 1148 250 53 0
|2057 1458 128 128 1527 1028 250 52 0|2058 1312 86 86 1527 923 250 54 0|2059 1208 43 43 1527 854 250 62 0|2060 1106 0 0 1527 786 250 70 0"""


def dn_rows(opts):
    with L.patched(options=opts):
        st, cv = L.grid_states(L.PLAN_DN)[1]                  # Do Nothing, Airbus launches NGSA
        eis, a, b, dt = M.af_inputs(st, cv)
        cell = M.eval_cell(eis, a, b, trace=True)
        ser = M.af_series(st, cell, eis, dt)
        pref = {r["year"]: r["boeing"]["nb_share"] for r in ser["years"]}
        ys = list(range(2026, 2061))
        return st, pref, ys, SD.year_rows(st, pref, ys)


def main():
    # 1. engine = manual build (COMAC's first call at 0, the build's own inputs)
    o1 = dict(OPTS, third_party=dict(OPTS["third_party"], comac_first=0.0, comac={str(k): v for k, v in BS.COMAC.items()},
                                     entrant=BS.ENTRANT, willing=BS.WILLING),
              max_phaseout=BS.MAX_PHASE, airbus_extra=BS.AIRBUS_EXTRA)
    st, pref, ys, eng = dn_rows(o1)
    base = {k: v for k, v in OPTS.items() if k not in ("max_phaseout", "airbus_extra", "third_party")}
    with L.patched(options=dict(base, max_phaseout=None, airbus_extra=None, third_party=None)):   # the build adds its own
        bld = BS.year_rows(st, pref, ys, phase=True, extra=True, third=True)
    worst = 0.0
    for y in ys:
        for k_e, k_b in (("delivered_b", "delivered_b"), ("delivered_a", "delivered_a"), ("lost", "lost"),
                         ("dlv_comac", "dlv_comac"), ("dlv_entrant", "dlv_entrant"), ("cap_max", "cap_max")):
            worst = max(worst, abs(eng[y][k_e] - bld[y][k_b]))
    assert worst < 1e-9, worst
    print("ok   engine = manual build, every year (worst gap %.1e)" % worst)
    # 2. the run's options give back the user's table
    _, _, ys, eng = dn_rows(OPTS)
    for line in TABLE.replace("\n", "").split("|"):
        t = [float(x) for x in line.split()]
        r = eng[int(t[0])]
        mine = [t[0], r["demand_gross"], r["cap_max"], r["delivered_b"], r["cap_a320"] + r["cap_ngsa"], r["delivered_a"],
                r["dlv_comac"], r["dlv_entrant"], r["lost"]]
        assert all(abs(a - b) <= 0.5 + 1e-6 for a, b in zip(mine, t)), (t, [round(x, 2) for x in mine])
    print("ok   the run's options give back the user's tuner table, all 35 years")
    # 3. within capacity, nothing negative
    for y, r in eng.items():
        assert r["delivered_b"] <= r["cap_max"] + r["cap_fps"] + 1e-6 and r["delivered_a"] <= r["cap_a320"] + r["cap_ngsa"] + 1e-6
        assert r["dlv_comac"] <= r["cap_comac"] + 1e-6 and r["dlv_entrant"] <= r["cap_entrant"] + 1e-6
        assert min(r["delivered_b"], r["delivered_a"], r["dlv_comac"], r["dlv_entrant"], r["lost"]) >= -1e-9
    print("ok   within capacity, nothing negative")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
