"""Checks for the Embraer options of supply_demand (third_party.entrant_share_no_fps, price_pressure), on the MAX phase-out
run's market (sd_options_phaseout.json).

1. entrant_share_no_fps equal to entrant_share gives the same rows as leaving it out, every plan, every year.
2. A price_pressure with a zero cut gives the same values, to the cent, as no price_pressure.
3. With the second-source share on, the entrant wins more in the years before the fps is in service; the books balance
   (no maker above its capacity, nothing negative).
4. price_pressure lowers each side's value by exactly the cut times the price of every aircraft it delivers in its
   counted window, less the same for the status quo, discounted (Boeing and Airbus, Do Nothing and an fps plan).
5. The briefs describe both options when they are set, and nothing changes when they are not.

  python3 test_embraer_options.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reports", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402
import briefs  # noqa: E402

M, SD = L.M, L.SD
BASE = {k: v for k, v in json.load(open(os.path.join(HERE, "sd_options_phaseout.json"))).items() if not k.startswith("_")}
P = M.af_params()


def with_entrant(share, no_fps=None, peak=12.0, ytp=7):
    o = copy.deepcopy(BASE)
    tp = o["third_party"]
    tp["entrant"] = {"eis": 2038, "peak_a_month": peak, "years_to_peak": ytp}
    tp["entrant_share"] = share
    if no_fps is not None:
        tp["entrant_share_no_fps"] = no_fps
    return o


def rows(opts, st):
    with L.patched(options=opts):
        ys = list(range(2026, 2061))
        return SD.year_rows(st, {y: 0.40 for y in ys}, ys), SD.year_rows(SD.sq_state(), {y: 0.40 for y in ys}, ys)


def value(opts, st, cv):
    with L.patched(options=opts):
        v = M.value(st, covert=cv, series=True)
    return v


def main():
    ok = []
    dn, dn_cv = L.grid_states(L.PLAN_DN)[1]            # Do Nothing, Airbus launches NGSA in 2030 (EIS 2037)
    fst, f_cv = L.grid_states(L.PLAN_NEW)[1]           # a 10-year fps launched in 2030 (EIS 2040), new sites
    assert fst["prog"]["fps"]["eis"] == 2040 and not dn["prog"].get("fps")
    # 1. the no-fps share equal to the share is the same rule
    for st in (dn, fst):
        a, aq = rows(with_entrant(0.05), st)
        b, bq = rows(with_entrant(0.05, 0.05), st)
        assert all(a[y] == b[y] for y in a) and all(aq[y] == bq[y] for y in aq)
    ok.append("entrant_share_no_fps equal to entrant_share: the same rows, every year (Do Nothing and an fps)")
    # 2. a zero cut changes nothing
    for st, cv in ((dn, dn_cv), (fst, f_cv)):
        v0 = value(with_entrant(0.05, 0.10), st, cv)
        v1 = value(dict(with_entrant(0.05, 0.10), price_pressure={"from": 2036, "ramp_years": 5, "cut": 0.0}), st, cv)
        for side in ("boeing", "airbus"):
            assert abs(v0[side]["pv_delta"] - v1[side]["pv_delta"]) < 1e-12, side
    ok.append("a zero price cut: the same values for both makers")
    # 3. the second-source share: more while Boeing has no new narrowbody in service
    r, _ = rows(with_entrant(0.05, 0.10, peak=40.0, ytp=1), fst)      # a large entrant, so the share binds, not capacity
    r0, _ = rows(with_entrant(0.05, peak=40.0, ytp=1), fst)
    early = [y for y in range(2038, 2040) if r[y]["cap_entrant"] > 0]
    assert early and all(r[y]["dlv_entrant"] >= r0[y]["dlv_entrant"] - 1e-9 for y in early)
    assert any(r[y]["dlv_entrant"] > r0[y]["dlv_entrant"] + 1e-6 for y in early)
    for st in (dn, fst):
        rr, qq = rows(with_entrant(0.05, 0.10), st)
        for x in list(rr.values()) + list(qq.values()):
            assert x["dlv_entrant"] <= x["cap_entrant"] + 1e-6 and x["dlv_comac"] <= x["cap_comac"] + 1e-6
            assert x["delivered_b"] <= x["cap_b"] + 1e-6 and x["delivered_a"] <= x["cap_a"] + 1e-6
            assert min(v for k, v in x.items() if isinstance(v, float)) >= -1e-9
    ok.append("second-source share: the entrant wins more before the fps is in service; the books balance")
    # 4. the price cut, closed form
    pp = {"from": 2036, "ramp_years": 5, "cut": 0.03}
    worst = 0.0
    for st, cv in ((dn, dn_cv), (fst, f_cv)):
        o = with_entrant(0.05, 0.10)
        v0 = value(o, st, cv)
        v1 = value(dict(o, price_pressure=pp), st, cv)
        with L.patched(options=o):
            eis, a, b, dt = M.af_inputs(st, cv)
            cell = M.eval_cell(eis, a, b, trace=True)
            srs = M.af_series(st, cell, eis, dt)
            SD.apply(st, srs["years"], {"boeing": P["WACC_B"], "airbus": P["WACC_A"]})
        for side, pre, new_p, old_p in (("boeing", "b", P["PRICE_fps"], P["PRICE_737"]), ("airbus", "a", P["PRICE_NGSA"], P["PRICE_A320"])):
            want = 0.0
            for rw in srs["years"]:
                x, y = rw[side], rw["year"]
                if not x["nb_in_window"]:
                    continue
                c = 0.0 if y < pp["from"] else pp["cut"] * min(1.0, (y - pp["from"] + 1) / pp["ramp_years"])
                sq_units = x["sq_nb_units"]
                want -= c * (x["nb_units_new"] * x["nb_price"] / 1000.0 + x["nb_units_old"] * x["legacy_nb_price"] / 1000.0
                             - sq_units * x["legacy_nb_price"] / 1000.0) * rw["df_" + pre]
            got = v1[side]["pv_delta"] - v0[side]["pv_delta"]
            worst = max(worst, abs(got - want))
            assert abs(got - want) < 1e-9, (side, got, want)
    ok.append("price cut = cut x price x aircraft delivered, less the status quo's, discounted (worst gap %.1e)" % worst)
    # 5. the briefs
    with L.patched(options=BASE):
        t0 = briefs.sd_option_rules()
    o = dict(with_entrant(0.05, 0.10), price_pressure={"from": 2036, "ramp_years": 5, "cut": 0.02})
    with L.patched(options=o):
        t1 = briefs.sd_option_rules()
    assert "second source" not in t0 and "cuts single-aisle prices" not in t0
    assert "second source" in t1 and "cuts single-aisle prices" in t1 and "2.0%" in t1 and "wins 5% of new customers" in t1
    ok.append("briefs: both options described when set, absent otherwise")
    for line in ok:
        print("ok  ", line)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
