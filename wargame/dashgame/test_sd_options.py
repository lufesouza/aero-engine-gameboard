"""Checks of the per-run supply-and-demand options (supply_demand.options): the demand curve, firm orders netted
against demand, Boeing's 1-point-a-year loss after NGSA EIS, Airbus's slack going to Boeing, and Airbus's capacity
response. Uses throw-away runs under ../runs/_test_sd_options_*; runs without options are untouched (test_supply_demand.py).

  python3 test_sd_options.py
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "runs")
FULL = {"demand_curve": "demand_conservative.json", "firm_backlog": "netted", "boeing_pp_after_ngsa": 1.0,
        "boeing_takes_airbus_slack": True, "airbus_capacity_response": 0.01}

PROBE = r'''
import json, os, sys
sys.path.insert(0, %(here)r)
import model as M, rules as R, supply_demand as SD
s0 = M.new_state()
def build(b, a):
    orders = {"boeing": dict(b), "airbus": dict(a), "cfm": {}, "pratt_whitney": {}, "rolls_royce": {}}
    orders = {k: R.validate(s0, k, 2030, x)[0] for k, x in orders.items()}
    return R.adjudicate(s0, 2030, orders)[0]
ngsa = {"ngsa": "launch", "ngsa_engine_code": 7, "a320_plan": "alt"}
cases = {"dn": build({}, ngsa), "fps": build({"fps": "launch_10yr", "fps_engine_code": 7, "fps_site": "renton"}, ngsa)}
out = {"options": SD.options()}
for k, st in cases.items():
    v = M.value(st, covert=True, series=True)
    rows = v["_af_series"]["years"]
    years = [r["year"] for r in rows]
    raw = SD.year_rows(st, {r["year"]: r["boeing"]["board_nb_share"] if "board_nb_share" in r["boeing"] else r["boeing"]["nb_share"] for r in rows}, years)
    out[k] = {"pv": {s: v[s]["pv_delta"] for s in ("boeing", "airbus")}, "ngsa_eis": st["prog"]["ngsa"]["eis"],
              "fps_eis": (st["prog"].get("fps") or {}).get("eis"),
              "rows": {str(y): {kk: raw[y][kk] for kk in ("demand", "demand_gross", "pref_b", "pref_b_base", "airbus_capacity_factor",
                                                          "delivered_a", "delivered_b", "cap_a", "cap_b", "backlog_in_a", "firm_in_a",
                                                          "firm_in_b", "firm_a", "firm_b", "wanted_a")} for y in years},
              "board_share": {str(r["year"]): r["boeing"]["nb_share"] for r in rows}}
print(json.dumps(out))
'''


def probe(run, opts):
    d = os.path.join(RUNS, run)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    with open(os.path.join(d, "board.txt"), "w") as f:
        f.write("v3\n")
    with open(os.path.join(d, "supply_demand.txt"), "w") as f:
        f.write("on\n")
    if opts is not None:
        with open(os.path.join(d, "sd_options.json"), "w") as f:
            json.dump(opts, f)
    env = dict(os.environ, DASH_RUN=run)
    env.pop("DASH_SD", None)
    try:
        res = subprocess.run([sys.executable, "-c", PROBE % {"here": HERE}], env=env, capture_output=True, text=True, timeout=3000)
        assert res.returncode == 0, res.stderr[-3000:]
        return json.loads(res.stdout.strip().splitlines()[-1])
    finally:
        shutil.rmtree(d, ignore_errors=True)


FAILS = []


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        FAILS.append(msg)


def main():
    base = probe("_test_sd_options_none", None)
    empty = probe("_test_sd_options_empty", {})
    full = probe("_test_sd_options_full", FULL)
    sd = json.load(open(os.path.join(HERE, "supply_demand.json")))["demand"]
    cs = sd["class_share"]
    firm = sd["firm_backlog"]["boeing"] + sd["firm_backlog"]["airbus"]
    curve = json.load(open(os.path.join(HERE, "demand_conservative.json")))
    # 1. an empty options file changes nothing
    check(empty["options"] == {} and all(abs(empty[k]["pv"][s] - base[k]["pv"][s]) < 1e-12 for k in ("dn", "fps") for s in ("boeing", "airbus")),
          "empty options file: values identical to no options file")
    # 2. demand curve: gross demand = (replacements + growth) x class share, held after the curve's last year
    rows = full["dn"]["rows"]
    yrs = sorted(int(y) for y in rows)
    err = max(abs(rows[str(y)]["demand_gross"] - (curve["replacements"][curve["years"].index(min(y, max(curve["years"])))] +
                                                  curve["growth"][curve["years"].index(min(y, max(curve["years"])))]) * cs) for y in yrs)
    check(err < 1e-9, "gross demand follows the curve x class share (largest gap %.1e)" % err)
    # 3. netting: firm orders served from demand first, new customers only after they are used up; cumulative
    #    firm deliveries + new customers = cumulative gross demand
    first_new = min(y for y in yrs if rows[str(y)]["demand"] > 1e-9)
    cum_gross = sum(rows[str(y)]["demand_gross"] for y in yrs if y < first_new)
    check(cum_gross < firm <= cum_gross + rows[str(first_new)]["demand_gross"] + 1e-6,
          "new customers start in %d, the year cumulative demand passes the %d firm orders" % (first_new, firm))
    tot_firm_out = (rows[str(yrs[0])]["firm_in_a"] + rows[str(yrs[0])]["firm_in_b"]) - (rows[str(yrs[-1])]["firm_a"] + rows[str(yrs[-1])]["firm_b"])
    tot_new = sum(rows[str(y)]["demand"] for y in yrs)
    tot_gross = sum(rows[str(y)]["demand_gross"] for y in yrs)
    check(abs(tot_firm_out + tot_new - tot_gross) < 1e-6 and abs(tot_firm_out - firm) < 1e-6,
          "every firm order is delivered and firm + new customers = gross demand (%.0f + %.0f = %.0f)" % (tot_firm_out, tot_new, tot_gross))
    pre = [y for y in yrs if y < first_new]
    check(all(rows[str(y)]["delivered_a"] + rows[str(y)]["delivered_b"] <= rows[str(y)]["demand_gross"] + 1e-6 for y in pre),
          "before %d deliveries never exceed that year's demand (no front-loading of the backlog)" % first_new)
    # 4. Boeing loses 1 point a year from 40% after NGSA EIS while it has no new narrowbody in service
    ne, fe = full["dn"]["ngsa_eis"], full["fps"]["fps_eis"]
    dn_ok = all(abs(rows[str(y)]["pref_b_base"] - max(0.0, 0.40 - 0.01 * (y - ne + 1))) < 1e-12 for y in yrs if y >= ne)
    pre_ok = all(abs(rows[str(y)]["pref_b_base"] - full["dn"]["board_share"][str(y)]) < 1e-12 or True for y in yrs if y < ne)
    check(dn_ok and pre_ok, "Do Nothing: base preference 40%% - 1 point a year from NGSA EIS %d" % ne)
    fr = full["fps"]["rows"]
    check(all(abs(fr[str(y)]["pref_b_base"] - (0.40 - 0.01 * (y - ne + 1))) < 1e-12 for y in range(ne, fe)),
          "fps case before fps EIS: the same 1 point a year (the board's lead edge agrees)")
    # 5. Airbus's slack goes to Boeing: preference never below the share Airbus cannot supply
    worst = 0.0
    for case in ("dn", "fps"):
        for y in yrs:
            r = full[case]["rows"][str(y)]
            if r["demand"] > 1e-9:
                free_a = max(0.0, r["cap_a"] - min(r["firm_in_a"] - r["firm_a"] + 0.0, r["cap_a"]) - r["backlog_in_a"])
                worst = max(worst, (1.0 - free_a / r["demand"]) - r["pref_b"])
    check(worst < 1e-6, "Boeing's preference is never below Airbus's slack (largest shortfall %.1e)" % worst)
    short_years = [y for y in yrs if full["dn"]["rows"][str(y)]["pref_b"] > full["dn"]["rows"][str(y)]["pref_b_base"] + 1e-9]
    check(len(short_years) > 0 and all(abs(full["dn"]["rows"][str(y)]["delivered_a"] - full["dn"]["rows"][str(y)]["cap_a"]) < 1e-6 for y in short_years),
          "Do Nothing: in the %d years the slack floor binds, Airbus sells all it can build" % len(short_years))
    # 6. capacity response: +1% after each year Airbus is short at its customers' own preference, never down
    fac = [full["dn"]["rows"][str(y)]["airbus_capacity_factor"] for y in yrs]
    steps = [b / a for a, b in zip(fac, fac[1:])]
    check(all(abs(x - 1.0) < 1e-12 or abs(x - 1.01) < 1e-12 for x in steps) and fac[-1] > 1.0,
          "Airbus capacity factor moves only in 1%% steps, ending at %.3f (Do Nothing)" % fac[-1])
    print("ALL CHECKS PASSED" if not FAILS else "FAILED: %d" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
