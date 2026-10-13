"""Checks of the supply-and-demand layer (supply_demand.py). Run with the layer on:

  DASH_SD=1 DASH_BOARD=v3 python3 test_supply_demand.py

1. Neutral case: with unlimited capacity and demand of 2,000 a year, every player's value equals the board's
   (the layer off), for the played states of dash-2050-obj and a few variants.
2. The digitised Airbus chart: the Alt plan adds about 1,500 A320s (the chart says "+~1,500"); NGSA reaches 100 a
   month; the plans move with the NGSA date.
3. Conservation every year: wanted + backlog in = delivered + backlog out + lost; deliveries never exceed capacity;
   spill only into spare capacity.
4. Orders: the supply-plan fields are legal only with the layer on, a missing field keeps the current plan, the plan
   locks at entry into service, and a change is logged in public.
5. Direction checks: the Alt plan raises Airbus deliveries in the transition; Renton lowers Boeing's MAX capacity
   after the fps enters service and books the saving; the 737 rate increase adds 100 aircraft a year from 2032.
"""
import copy
import json
import os
import sys

os.environ["DASH_SD"] = "1"
os.environ.setdefault("DASH_BOARD", "v3")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import rules as R  # noqa: E402
import supply_demand as SD  # noqa: E402

assert M.SD_ON
RUN = os.path.join(HERE, "..", "runs", "dash-2050-obj")
fails = []


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


def states():
    out = [("played r%d" % n, json.load(open(os.path.join(RUN, "state_r%d.json" % n)))) for n in (1, 2, 4)]
    s0 = json.load(open(os.path.join(RUN, "state_r0.json")))
    for lab, b, a in (("both hold", {}, {}), ("fps 7-yr + 787, NGSA + A350", {"fps": "launch_7yr", "re787": "launch"},
                                                                         {"ngsa": "launch", "rea350": "launch"}),
                      ("fps only, rate up", {"fps": "launch_10yr", "rate_737": "increase"}, {})):
        s1, _ = R.adjudicate(s0, 2030, {"boeing": b, "airbus": a})
        out.append((lab, s1))
    return out


# 1. neutral case
def neutral(fn):
    keep = (SD.boeing_capacity, SD.airbus_capacity, SD.demand)
    SD.boeing_capacity = lambda s, y: (1e9, 0.0)
    SD.airbus_capacity = lambda s, y: (1e9, 0.0)
    SD.demand = lambda y: 2000.0
    try:
        return fn()
    finally:
        SD.boeing_capacity, SD.airbus_capacity, SD.demand = keep


for lab, s in states():
    on = neutral(lambda: M.value(s, covert=True, series=False))
    M.SD_ON = False
    try:
        off = M.value(s, covert=True, series=False)
    finally:
        M.SD_ON = True
    d = max(abs(on[k]["pv_delta"] - off[k]["pv_delta"]) for k in M.SIDES)
    check(d < 1e-9, "neutral case equals the board (%s): max |ΔPV difference| %.2e" % (lab, d))

# 2. the chart
alt = sum(SD._rundown("a320_alt", 0, y) - SD._rundown("a320_base", 0, y) for y in range(2030, 2050))
check(1400 <= alt <= 1600, "Alt plan adds %.0f A320s (chart: ~1,500)" % alt)
check(abs(SD._annual("ngsa", 0, 2046) - 1200) < 1e-6, "NGSA at 100 a month from 2046 on the chart dates")
check(abs(SD._rundown("a320_base", 5, 2041) - 1020) < 1e-6 and SD._rundown("a320_base", 5, 2045) < 1020,
      "a later NGSA (EIS 2042) moves the A320 rundown five years later")

# 3. conservation
s4 = json.load(open(os.path.join(RUN, "state_r4.json")))
v = M.value(s4, covert=True, series=True)
lapse = SD.inputs()["demand"]["lapse_per_year"]
worst = 0.0
cap_ok = spill_ok = True
for r in v["_af_series"]["years"]:
    b, a = r["boeing"]["sd"], r["airbus"]["sd"]
    lhs = b["wanted"] + a["wanted"] + b["backlog_in"] + a["backlog_in"]
    rhs = r["boeing"]["nb_units"] + r["airbus"]["nb_units"] + b["backlog_out"] + a["backlog_out"] + r["sd"]["lost"]
    worst = max(worst, abs(lhs - rhs))
    cap_ok &= r["boeing"]["nb_units"] <= b["capacity"] + 1e-6 and r["airbus"]["nb_units"] <= a["capacity"] + 1e-6
    spill_ok &= (b["spill_in"] <= 1e-9 or r["boeing"]["nb_units"] <= b["capacity"] + 1e-6)
check(worst < 1e-6, "aircraft conserved every year (max error %.1e)" % worst)
check(cap_ok, "deliveries never exceed capacity")
check(spill_ok, "spill only into spare capacity")
pv = sum(r["boeing"]["nb_profit"] * r["df_b"] for r in v["_af_series"]["years"] if r["boeing"]["nb_in_window"])
check(abs(v["boeing"]["bridge"]["supply_demand"] - (pv - sum(r["boeing"]["board_nb_profit"] * r["df_b"] for r in v["_af_series"]["years"] if r["boeing"]["nb_in_window"])
      + sum((r["boeing"]["board_sq_nb_profit"] - r["boeing"]["sq_nb_profit"]) * r["df_b"] for r in v["_af_series"]["years"] if r["boeing"]["nb_in_window"]))) < 1e-9,
      "Boeing's supply-and-demand line equals the PV of delivered minus board profit, net of the status quo")

# 4. orders
s0 = json.load(open(os.path.join(RUN, "state_r0.json")))
L = R.legal_options(s0, "boeing", 2030)
check(L["fps_site"] == ["new_site", "renton"], "fps_site legal in 2030 with the layer on")
M.SD_ON = False
try:
    check("fps_site" not in R.legal_options(s0, "boeing", 2030) and "a320_plan" not in R.legal_options(s0, "airbus", 2030),
          "supply-plan fields not offered with the layer off")
finally:
    M.SD_ON = True
s1, log = R.adjudicate(s0, 2030, {"boeing": {"fps": "launch_10yr", "fps_site": "renton"}, "airbus": {"ngsa": "launch", "a320_plan": "alt"}})
check(s1["sd"] == {"a320_plan": "alt", "fps_site": "renton"} and any("Renton" in e for e in log) and any("Alt plan" in e for e in log),
      "plans set and logged in public")
clean, _ = R.validate(s1, "boeing", 2035, {})
check(clean["fps_site"] == "renton", "a missing field keeps the current plan")
s2, _ = R.adjudicate(s1, 2035, {"boeing": clean})
check(s2["sd"]["fps_site"] == "renton", "the plan carries to the next round")
check(R.legal_options(s2, "airbus", 2045)["a320_plan"] == ["alt"], "the A320 plan locks once NGSA is in service (2037)")

# 5. directions
sb, _ = R.adjudicate(s0, 2030, {"airbus": {"ngsa": "launch"}})
sa, _ = R.adjudicate(s0, 2030, {"airbus": {"ngsa": "launch", "a320_plan": "alt"}})
cb = sum(sum(SD.airbus_capacity(sb, y)) for y in range(2037, 2046))
ca = sum(sum(SD.airbus_capacity(sa, y)) for y in range(2037, 2046))
check(ca - cb > 1400, "Alt plan adds %.0f aircraft of Airbus capacity in 2037-2045" % (ca - cb))
fn, _ = R.adjudicate(s0, 2030, {"boeing": {"fps": "launch_10yr"}})
fr, _ = R.adjudicate(s0, 2030, {"boeing": {"fps": "launch_10yr", "fps_site": "renton"}})
check(SD.boeing_capacity(fr, 2045)[0] < SD.boeing_capacity(fn, 2045)[0] and SD.boeing_capacity(fr, 2045)[1] == SD.boeing_capacity(fn, 2045)[1],
      "Renton: less MAX capacity in 2045 (%.0f vs %.0f), same fps ramp" % (SD.boeing_capacity(fr, 2045)[0], SD.boeing_capacity(fn, 2045)[0]))
check(SD.boeing_capacity(fn, 2051)[0] == 0 and SD.boeing_capacity(sb, 2051)[0] > 0, "MAX stops after 2050 only with the fps in service")
vr = M.value(fr, covert=True, series=False)
check(vr["boeing"]["bridge"]["supply_plan"] > 0, "Renton books a saving (%.2f PV)" % vr["boeing"]["bridge"]["supply_plan"])
va = M.value(sa, covert=True, series=False)
check(va["airbus"]["bridge"]["supply_plan"] < 0, "Alt plan books a cost (%.2f PV)" % va["airbus"]["bridge"]["supply_plan"])
sr, _ = R.adjudicate(s0, 2030, {"boeing": {"rate_737": "increase"}})
check(abs(SD.boeing_capacity(sr, 2032)[0] - SD.boeing_capacity(s0, 2032)[0] - 100) < 1e-9 and
      SD.boeing_capacity(sr, 2031)[0] == SD.boeing_capacity(s0, 2031)[0], "737 rate increase: +100 a year from 2032")

print("ALL CHECKS PASSED" if not fails else "%d FAILED" % len(fails))
sys.exit(1 if fails else 0)
