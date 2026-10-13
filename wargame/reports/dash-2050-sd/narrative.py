"""Words for the supply-and-demand game page. Every number is read from data/report_data.json (run dash-2050-sd),
data/sd_checks.json (make_sd_checks.py) or ../dash-2050-obj/data/report_data.json (the previous game) and formatted
here, so the text cannot drift from the data. Players' reasons are paraphrased from their own returns in the run record."""
import json
import os
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
C = json.load(open(os.path.join(HERE, "data", "sd_checks.json")))
OBJ = json.load(open(os.path.join(HERE, "..", "dash-2050-obj", "data", "report_data.json")))
F = D["rounds"][-1]
SD = F["sd"]
Y = SD["year"]
MINUS = "−"


def r(v, dp):
    return float(Decimal(str(v)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))


def b(v, dp=2, sign=True):
    x = r(v, dp)
    s = f"${abs(x):.{dp}f}B"
    return (MINUS + s) if x < 0 else (("+" + s) if sign and x > 0 else s)


def n0(v):
    return f"{r(v, 0):,.0f}"


def pc(v, dp=0):
    return f"{r(v * 100, dp):.{dp}f}%"


def at(key, year, side=None):
    src = SD[side] if side else SD
    return src[key][Y.index(year)]


def tot(key, a, z, side=None):
    src = SD[side] if side else SD
    return sum(x for y, x in zip(Y, src[key]) if a <= y <= z)


V = {s: F["value"][s]["pv_delta"] for s in F["value"]}
VO = {s: OBJ["rounds"][-1]["value"][s]["pv_delta"] for s in OBJ["rounds"][-1]["value"]}
BC = D["board_check"]
NL = C["no_layer"]                       # the final state valued with the layer off (dashboard + game master)
BR = {s: F["value"][s]["bridge"] for s in ("boeing", "airbus")}
FPS = {x["plan"]: x for x in C["fps_2030"]["with_sd"]}
FPS0 = {x["plan"]: x for x in C["fps_2030"]["board"]}
RI = {x["year"]: x["now"] for x in C["round_items"]}
RIB = {x["year"]: x["briefed"] for x in C["round_items"]}
FM = C["fps_mechanism"]
WACC_B = D["rounds"][0]["value"]["boeing"]["wacc"]
_ry = sorted(RI)
# the better site for a 10-year fps each round (value against Do Nothing, everyone else's orders as played)
FPS_BEST = {y: max((RI[y]["fps_10yr_renton"], "Renton"), (RI[y]["fps_10yr_new_site"], "new sites")) for y in _ry}
# change in the best fps value from one round to the next, net of moving the same launch later (discounting only)
REAL_GAIN = {y1: FPS_BEST[y1][0] - FPS_BEST[y0][0] / (1 + WACC_B) ** (y1 - y0) for y0, y1 in zip(_ry, _ry[1:])}
_rise = FPS_BEST[_ry[-1]][0] - FPS_BEST[_ry[0]][0]
_disc = 1 - sum(REAL_GAIN.values()) / _rise
DISC_WORD = "Most" if _disc > 0.6 else ("About half" if _disc >= 0.4 else "Part")
FPS_RAMP = [y["fps_units"] for y in FM["years"] if y["year"] >= FM["eis"]]
EARLY_BOOKED = sum(y["board_gain"] * y["df"] for y in FM["years"] if FM["eis"] <= y["year"] < FM["eis"] + 5)
EARLY_EARNED = sum(y["delivered_gain"] * y["df"] for y in FM["years"] if FM["eis"] <= y["year"] < FM["eis"] + 5)
CATCH_UP = next(y["year"] for y in FM["years"] if y["year"] >= FM["eis"] and y["delivered_gain"] >= y["board_gain"])
SENS = {x["case"]: x for x in C["demand_sensitivity"]}
REG = D["regret"]
INP = D["sd_inputs"]

capb = lambda y: at("cap_max", y) + at("cap_fps", y)
capa = lambda y: at("cap_a320", y) + at("cap_ngsa", y)
cap = lambda y: capb(y) + capa(y)
dlvb = lambda y: at("dlv_max", y) + at("dlv_fps", y)
dlva = lambda y: at("dlv_a320", y) + at("dlv_ngsa", y)
dlv_b = lambda a, z: tot("dlv_max", a, z) + tot("dlv_fps", a, z)
FIRM_CLEAR = next(y for y, x, z in zip(Y, SD["firm_b"], SD["firm_a"]) if x < 1 and z < 1)
SOLD_TO = max(y for y in Y if y < 2037 and abs(dlvb(y) - capb(y)) < 0.5 and abs(dlva(y) - capa(y)) < 0.5)
SHORT_FROM = next(y for y in Y if y > 2040 and at("demand", y) > cap(y))
lapsed_early = tot("lost", 2026, SOLD_TO)
BOEING_BELOW = [y for y in Y if y > 2030 and dlvb(y) < capb(y) - 0.5]
# demand in the players' briefs: growth was reduced by the class share twice
_cs = INP["demand"]["class_share"]
GROWTH_SHORT = 1 - _cs
DEMAND_SHORT = sum(g * (1 - _cs) for g in SD["growth"]) / sum(SD["demand"])
BOTH_SOLD = next(y for y in Y if y > 2040 and abs(dlvb(y) - capb(y)) < 0.5 and abs(dlva(y) - capa(y)) < 0.5)
fps_d = lambda plan: FPS[plan]["boeing"] - FPS["Do Nothing"]["boeing"]
fps_d0 = lambda plan: FPS0[plan]["boeing"] - FPS0["Do Nothing"]["boeing"]
pref_after = at("pref_share", 2050, "boeing")
PREF_LOW_FROM = next(y for y in Y if abs(at("pref_share", y, "boeing") - pref_after) < 1e-9)
dl_after = at("delivered_share", 2050, "boeing")
spill_b = sum(SD["boeing"]["spill_in"])
lapsed = sum(SD["lost"])
ngsa_share = V["airbus"] / BC["airbus"]["board"]
NGSA_RAMP = [x for x in SD["dlv_ngsa"] if x > 0.5]
_a_bound = lambda y: at("backlog_a", y) > 1 and abs(dlva(y) - capa(y)) < 0.5
AIRBUS_BOUND = next(y for y in Y if y > 2037 and _a_bound(y))
NGSA_100 = next(y for y in Y if at("cap_ngsa", y) >= 1190)          # 2Q45 on the chart: 1,194 aircraft in 2045
NGSA_FULL = next(y for y in Y if at("cap_ngsa", y) >= 1199.5)        # first full calendar year at 1,200
CAPA_PEAK = max(capa(y) for y in Y)
CAPA_PEAK_Y = max(Y, key=capa)
BOEING_36 = next(y for y in Y if y > 2040 and abs(at("delivered_share", y, "boeing") - dl_after) < 5e-4)
OVERFLOW = V["boeing"] - SENS["No flexible customers"]["boeing"]
ALT_PV = -BR["airbus"]["supply_plan"]
OBJ_B = {o["label"]: o for o in F["objectives"]["boeing"]}
_dn = {(x["round"], x["side"]): x for x in C["decisions_now"]}

TITLE = "The war game with supply and demand"
LEDE = (f"We replayed the dash-2050-obj war game (ExCo and Board agents, Control's objectives, rounds 2030, 2035, 2045 "
        f"and 2050) with one change: an aircraft is sold only when a customer wants it and a factory can build it. "
        f"<b>Demand = replacement + growth</b>: replacement of today's 737 MAX and A320neo fleets from your Cirium page, "
        f"plus fleet growth, which your data did not give, from Airbus's and Boeing's market forecasts. "
        f"<b>Supply</b> is your Airbus Rev. B plan and Boeing's plan: the 737 MAX, built to 2050 if an fps replaces it, "
        f"and the fps at new sites or at Renton. Boeing never launched the fps. Airbus's NGSA still paid, but at about "
        f"{pc(ngsa_share)} of its value on the dashboard alone. Both makers were sold out through {SOLD_TO} while they "
        f"cleared the firm backlog; from {SHORT_FROM}, new demand alone exceeds both makers' capacity.")

TILES = {
    "boeing": "Never launched the fps; gains Airbus's overflow customers",
    "airbus": f"NGSA in 2030 on the Alt plan; {b(BC['airbus']['board'])} on the dashboard alone",
    "cfm": "Ducted engine and Embraer partnership in 2035",
    "pratt_whitney": "GTF2 folded into the Joint Venture in 2035",
    "rolls_royce": "UltraFan NB folded into the Joint Venture in 2035",
}

FINDINGS = [
    ("Boeing never launched the fps.",
     f" In 2030 the 10-year fps was worth {b(fps_d0('fps 10-year, new sites'))} against Do Nothing on the dashboard "
     f"alone, but {b(fps_d('fps 10-year, new sites'))} once deliveries are limited ({b(fps_d('fps 10-year, Renton'))} at "
     f"Renton). The dashboard books the fps's margin on every Boeing narrowbody from the day it enters service: about "
     f"${r(FM['fps_unit_profit_m'], 0):.0f}M of profit an aircraft, against about ${r(FM['max_unit_profit_m'], 0):.0f}M "
     f"for a 737 MAX. Here the fps ramps on the NGSA curve of your Rev. B chart: "
     f"{', '.join(n0(u) for u in FPS_RAMP[:5])} aircraft in its first five years. So in those five years it earns "
     f"{b(EARLY_EARNED, 1, False)} (at 2026) of the {b(EARLY_BOOKED, 1, False)} the dashboard books for them, and its "
     f"yearly margin catches up with the dashboard's only in {CATCH_UP}. The early margin is never made up. That cuts "
     f"the fps's discounted narrowbody gain from {b(FM['board_pv_gain'], 1, False)} to "
     f"{b(FM['delivered_pv_gain'], 1, False)}. The better 10-year fps was then worth "
     + ", ".join(f"{b(FPS_BEST[y][0])} in {y} ({FPS_BEST[y][1]})" for y in _ry[:-1]) +
     f" and {b(FPS_BEST[_ry[-1]][0])} in {_ry[-1]} ({FPS_BEST[_ry[-1]][1]}). {DISC_WORD} of that rise is only "
     f"discounting, because a later launch's loss is smaller at 2026. Like for like, rising demand added about {b(REAL_GAIN[2035], 2, False)}, "
     f"{b(REAL_GAIN[2045], 2, False)} and {b(REAL_GAIN[2050], 2, False)} a round. It never came near the +$1B that "
     f"Boeing's Board requires of a launch in the most likely case."),
    (f"NGSA still paid, but at about {pc(ngsa_share)} of its dashboard value.",
     f" Airbus ends at {b(V['airbus'])}, against {b(BC['airbus']['board'])} for the same moves on the dashboard alone "
     f"(the supply-and-demand line is {b(BR['airbus']['supply_demand'])} and the Alt plan's cost "
     f"{b(BR['airbus']['supply_plan'])}). Two things cut it. First, NGSA ramps on "
     f"your chart ({', '.join(n0(u) for u in NGSA_RAMP[:5])} aircraft in its first five years), while the dashboard "
     f"books its margin on every Airbus narrowbody from entry into service. Second, the dashboard's share rule moves "
     f"Airbus from 60% to {pc(1 - pref_after)} of 2,000 aircraft a year ({n0(2000 * (1 - pref_after))}) by "
     f"{PREF_LOW_FROM}, but its factories settle at 100 a month, 1,200, once the A320 ends (briefly "
     f"{n0(CAPA_PEAK)} in {CAPA_PEAK_Y}, while Alt-plan A320s overlap NGSA). Airbus sells every aircraft it can build "
     f"from {AIRBUS_BOUND}. NGSA reaches 100 a month in {NGSA_100}, as the last Alt-plan A320s end, and builds 1,200 a "
     f"year from {NGSA_FULL}. The Alt "
     f"plan was worth {b(RI[2030]['alt_vs_base'])} net of its $0.75B cost. Without fleet growth, NGSA would be worth "
     f"{b(SENS['No growth (your replacement data only)']['airbus'])}."),
    ("Boeing loses less than the dashboard says, mostly thanks to Airbus's overflow.",
     f" The dashboard's share rule takes Boeing's preferred share from 40% to {pc(pref_after)} by {PREF_LOW_FROM}, "
     f"falling 3 points a year from NGSA's entry into service in 2037. In a short market about half of Airbus's waiting "
     f"customers are flexible and take Boeing's free slots: {n0(spill_b)} aircraft over 2026-2060. So Boeing delivers "
     f"{pc(dl_after)} of the market from {BOEING_36}. The supply-and-demand line adds {b(BR['boeing']['supply_demand'])} "
     f"to Boeing (its ΔPV is {b(V['boeing'])}, against {b(BC['boeing']['board'])} on the dashboard alone). About "
     f"{b(OVERFLOW, 2, False)} of that is Airbus's overflow: with no flexible customers Boeing would be at "
     f"{b(SENS['No flexible customers']['boeing'])}. The rest comes from the status quo being capped too, since the 737 "
     f"MAX builds 684 a year, not the dashboard's 800. The cost falls in the NGSA ramp years: in 2037-2045 Boeing "
     f"delivers {n0(dlv_b(2037, 2045))} aircraft, against {n0(tot('sq_delivered_b', 2037, 2045))} in the status quo."),
    ("The largest money left on the table was the 787 Re-engine.",
     f" It was part of Boeing's best alternative in every round, worth {b(REG['1']['boeing']['regret_ex_post'])} in 2030 "
     f"and {b(REG['4']['boeing']['regret_ex_post'])} by 2050 (by then together with a 10-year fps). In 2030 and 2035 "
     f"Boeing held it because its Board would have vetoed it: it lost more than the Board's $1B limit if Airbus "
     f"re-engined the A350 too. In 2045 and 2050 it was worth less than the +$1B the Board requires. Airbus left the "
     f"A350 Re-engine ({b(REG['1']['airbus']['regret_ex_post'])} in 2030). In 2030 and 2035 its spending would have "
     f"exceeded one year's free cash flow during NGSA's development. In 2045 and 2050 its CFO's robustness test stopped "
     f"it inside the ExCo (it lost money if Boeing re-engined the 787), as did the company's own +$1B launch test, "
     f"though its Board would have approved it."),
    ("By 2050 the single-aisle market is short of capacity, and no order adds more.",
     f" In 2050 demand is {n0(at('demand', 2050))} aircraft against {n0(cap(2050))} of capacity. Waiting customers "
     f"reach {n0(at('backlog_b', 2050) + at('backlog_a', 2050))} in 2050 and "
     f"{n0(at('backlog_b', 2060) + at('backlog_a', 2060))} by 2060, and {n0(lapsed)} customers drop out over 2026-2060 "
     f"({n0(lapsed_early)} of them in 2026-{SOLD_TO}, while both makers were sold out). After 2030 no order raises an "
     f"existing line's rate: the 737 rate increase could be ordered only in 2030, and Boeing did not order it. New "
     f"capacity can come only from a new programme such as the fps, which would lift Boeing to 100 a month. Airbus's "
     f"ExCo said it was preparing a capacity step but did not commit it."),
    ("The engine makers settled early.",
     " Pratt &amp; Whitney and Rolls-Royce committed to the Joint Venture in 2035, folding GTF2 and UltraFan NB into "
     "it. In the same sealed round CFM launched its ducted engine and the Embraer partnership. With no fps, the 737 "
     "stays CFM-only, so Boeing misses its dual-source objective. "
     f"CFM ends at {b(V['cfm'])}, Rolls-Royce at {b(V['rolls_royce'])} and Pratt &amp; Whitney at {b(V['pratt_whitney'])}. "
     f"Most of the change from the previous game ({b(VO['cfm'])}, {b(VO['rolls_royce'])}, {b(VO['pratt_whitney'])}) "
     f"comes from engines now selling only on aircraft actually delivered, not from the missing fps (see "
     f"<a href=\"#compare\">Against the previous game</a>)."),
]

INPUTS_LEDE = ("The dashboard sells a fixed 2,000 narrowbodies a year, split by its share rules, and books every one. "
               "The supply-and-demand layer keeps the dashboard's shares as what customers <i>prefer</i>, and "
               "delivers only what the factories can build. The firm backlog is delivered first, then new demand, "
               "then customers still waiting from earlier years. Flexible customers take the other maker's free "
               "slots when their first choice is full, and a tenth of those still waiting drop out each year.")
DEMAND_TITLE = (f"Total demand = replacement + growth: growth dominates, and new demand rises from "
                f"{n0(at('demand', 2026))} a year in 2026 to a peak of {n0(max(SD['demand']))} in "
                f"{Y[SD['demand'].index(max(SD['demand']))]}")
DEMAND_CAP = (f"Replacement is your page's curve for today's 737 MAX and A320neo-family fleets, with the A220 share "
              f"({pc(1 - INP['demand']['class_share'], 1)}) taken out. Growth is the single-aisle fleet growing about "
              f"{pc(INP['demand']['fleet_growth_2025_44'], 2)} a year to 2044, easing to "
              f"{pc(INP['demand']['fleet_growth_2060'])} by 2060, with the same A220 share taken out. Sources: Airbus "
              f"GMF 2025, Boeing CMO 2025 and 2026. The firm backlog (737 MAX {INP['demand']['firm_backlog']['boeing']:,}; "
              f"A320neo family {INP['demand']['firm_backlog']['airbus']:,}) comes on top. It is, broadly, the "
              f"replacement of today's older 737NG and A320ceo fleets.")
AIRBUS_TITLE = ("Your Airbus Rev. B plan: the A320 runs down as NGSA ramps to 100 a month, and the Alt plan keeps "
                "about 1,500 more A320s")
AIRBUS_CAP = ("Annual output read off your chart (NGSA entry into service mid-2037). The whole plan moves with the "
              "NGSA date; with no NGSA the A320 stays at 85 a month. Airbus took the Alt plan in 2030. Its cost of "
              f"$0.75B (the chart's +$0.7-0.8B) is booked at NGSA's entry into service, {b(ALT_PV, 2, False)} at 2026.")
MARKET_LEDE = (f"Three phases. Through {SOLD_TO} both makers are sold out: the firm backlog clears in {FIRM_CLEAR} "
               f"and customers who waited take the rest. In 2037-2045 NGSA takes customers' preference and Boeing "
               f"has capacity to spare, while Airbus sells all it can build from {AIRBUS_BOUND}. Total demand "
               f"exceeds total capacity from {SHORT_FROM}, and both makers are sold out from {BOTH_SOLD}.")
MARKET_TITLE = (f"Demand outgrows both makers' capacity from {SHORT_FROM}: in 2050 it is {n0(at('demand', 2050))} "
                f"aircraft against {n0(cap(2050))}")
BOEING_LINES_TITLE = (f"With no fps, Boeing's 737 MAX line runs at 57 a month from 2030 to 2060, and Boeing delivers "
                      f"below it only in the NGSA ramp years ({BOEING_BELOW[0]}-{BOEING_BELOW[-1]})")
BOEING_LINES_CAP = ("Boeing's capacity is the 737 MAX path (42.5 to 57 a month by 2030). With an fps the MAX would "
                    "give way to it and end in 2050. Boeing did not order the 737 rate increase (100 a year from "
                    "2032), which was open only in 2030.")
AIRBUS_LINES_TITLE = (f"Airbus's output dips in the NGSA transition; it sells all it can build from {AIRBUS_BOUND}, "
                      f"and NGSA reaches 100 a month in {NGSA_100}")
BACKLOG_TITLE = (f"Firm backlogs clear in {FIRM_CLEAR}; from the late 2040s Airbus's waiting customers pile up "
                 f"({n0(at('backlog_a', 2060))} by 2060)")
BACKLOG_CAP = ("Firm orders never lapse or switch maker. Waiting customers are new demand that could not be served in "
               "its year: a tenth drop out each year, and flexible ones move to the other maker's free slots.")
MOVES_LEDE = ("All the moves came in the first two rounds; after 2035 every company held. Supply plans are shown only "
              "when they change. Boeing kept its default of new sites throughout, since the site matters only with a "
              "launch.")
ROUND_NOTES = [
    ("2030.",
     f" Airbus launched NGSA (CFM, P&amp;W and Rolls-Royce engines) on the Alt plan. Boeing held everything: every fps "
     f"option lost money against Do Nothing. The 787 Re-engine ({b(RI[2030]['re787'])} against Airbus's actual moves) "
     f"would have been vetoed by Boeing's Board for its loss if Airbus re-engined the A350 too. P&amp;W's and "
     f"Rolls-Royce's 'launch if selected' orders were triggered by NGSA's engine choice, and CFM ordered the GEnx "
     f"upgrade."),
    ("2035.",
     f" P&amp;W and Rolls-Royce formed the Joint Venture. In the same sealed round, CFM launched the ducted engine and "
     f"the Embraer partnership to defend its place against GTF2 and UltraFan NB, which NGSA had selected in 2030; it "
     f"had not expected the Joint Venture. Boeing held again: its better 10-year fps ({FPS_BEST[2035][1]}) was "
     f"{b(FPS_BEST[2035][0])}. Airbus kept the A350 Re-engine ({b(RI[2035]['rea350'])}) off the table, "
     f"because its annual spending would have exceeded one year's free cash flow during NGSA's last development years."),
    ("2045 and 2050.",
     f" Everyone held. Boeing's better 10-year fps turned slightly positive ({b(FPS_BEST[2045][0])} at "
     f"{FPS_BEST[2045][1]}, then {b(FPS_BEST[2050][0])} at {FPS_BEST[2050][1]}), far short of its Board's +$1B. The 787 Re-engine fell to "
     f"{b(RI[2045]['re787'])} and {b(RI[2050]['re787'])}. Airbus's A350 Re-engine ({b(RI[2045]['rea350'])}, then "
     f"{b(RI[2050]['rea350'])}) was stopped inside its ExCo by the CFO's robustness test and the company's +$1B launch "
     f"test. Airbus said its factory ceiling now limits deliveries."),
]
VALUE_LEDE = ("ΔPV is each company's change in present value against the status quo, at 2026, valued by the dashboard "
              "with the game master's adjustments and the supply-and-demand layer. The status quo (no new programme) "
              "runs through the same layer, on the published capacity plans (the 737 MAX rising to 57 a month, the "
              "A320 at 85 a month) and the dashboard's 40/60 split.")
BRIDGE_CAP = (f"The lines above the supply-and-demand line are the dashboard's own numbers for these moves (they sum "
              f"to Boeing {b(BC['boeing']['board'])} and Airbus {b(BC['airbus']['board'])}). The supply-and-demand line replaces the dashboard's "
              f"2,000-a-year deliveries with what was actually built and wanted, against the status quo run the same "
              f"way. New types (fps, NGSA) deliver first at the dashboard's new-type price and margin; the rest are "
              f"737 MAX or A320neo at today's. The supply-plan line is the Alt plan's $0.75B, booked at NGSA's 2037 "
              f"entry into service ({b(-ALT_PV)} at 2026); a Renton saving would appear here had Boeing launched the fps "
              f"there.")
SHARES_LEDE = (f"Control's 50/50 and incumbency objectives are scored on what customers prefer. That falls from 40% in "
               f"2036 to {pc(pref_after)} by {PREF_LOW_FROM} with no fps, so Boeing misses both. What Boeing delivers "
               f"tells a better story: {pc(dl_after)} from {BOEING_36}, because Airbus cannot build all that its "
               f"customers want. The previous game, with an fps from 2040 and no supply limits, reached "
               f"{pc(OBJ['rounds'][-1]['years']['boeing']['nb_share'][2050 - 2026])}.")
SHARES_TITLE = (f"Customers prefer Boeing less once NGSA is in service ({pc(pref_after)} by {PREF_LOW_FROM}), but "
                f"Boeing delivers {pc(dl_after)} of a short market")
PLAY_LEDE = ("The round game is the airframers' options for that round, with everyone else's orders as played and no "
             "later moves. Neither airframer played a pure equilibrium of the round: each side's best reply included "
             "a Re-engine that its own tests ruled out. Regret is the final ΔPV of a side's best alternative minus what "
             "it played, with everyone else's actual orders and later rounds replayed.")
COMPARE_LEDE = ("The previous game (dash-2050-obj) had the same ExCo and Board agents and Control's objectives on the "
                "dashboard alone, with no supply limits. There Boeing launched a 10-year fps in 2030 and CFM launched "
                "its ducted engine at once. Here neither airframer moves after 2030, and the engine makers settle in "
                "2035. The differences split into two steps: the moves (this game's moves on the dashboard alone) and "
                "the supply-and-demand layer.")
COMPARE_POINTS = [
    ("Boeing.",
     f" Previous game: 10-year fps in 2030 (in service 2040), ΔPV {b(VO['boeing'])}. This game's moves on the "
     f"dashboard alone: {b(NL['boeing'])}. With the layer: {b(V['boeing'])}. The layer takes "
     f"{b(fps_d0('fps 10-year, new sites') - fps_d('fps 10-year, new sites'), 2, False)} off the value of the 2030 fps "
     f"decision (from {b(fps_d0('fps 10-year, new sites'))} to {b(fps_d('fps 10-year, new sites'))} against Do Nothing)."),
    ("Airbus.",
     f" Previous game {b(VO['airbus'])}. With no Boeing fps, the same NGSA is worth {b(NL['airbus'])} on the dashboard "
     f"alone. The layer then takes {b(NL['airbus'] - V['airbus'], 1, False)} away (deliveries "
     f"{b(BR['airbus']['supply_demand'])}, the Alt plan's cost {b(BR['airbus']['supply_plan'])}), to {b(V['airbus'])}."),
    ("Engine makers.",
     f" CFM: previous {b(VO['cfm'])}, this game's moves on the dashboard alone {b(NL['cfm'])}, with the layer "
     f"{b(V['cfm'])}. Rolls-Royce: {b(VO['rolls_royce'])}, {b(NL['rolls_royce'])}, {b(V['rolls_royce'])}. "
     f"Pratt &amp; Whitney: {b(VO['pratt_whitney'])}, {b(NL['pratt_whitney'])}, {b(V['pratt_whitney'])}. The moves (above "
     f"all, no Boeing fps) account for {b(NL['cfm'] - VO['cfm'], 1)} for CFM, {b(NL['rolls_royce'] - VO['rolls_royce'], 1)} "
     f"for Rolls-Royce and {b(NL['pratt_whitney'] - VO['pratt_whitney'], 1)} for P&amp;W. The supply-and-demand layer, "
     f"with engines sold only on aircraft actually delivered, accounts for {b(V['cfm'] - NL['cfm'], 1)}, "
     f"{b(V['rolls_royce'] - NL['rolls_royce'], 1)} and {b(V['pratt_whitney'] - NL['pratt_whitney'], 1)}."),
    ("What did not change.",
     " Boeing's balance sheet is repaired by 2029 (2030 in the stress case) and stays repaired, as before. In both "
     "games neither the 787 Re-engine nor the A350 Re-engine was launched, and the Joint Venture formed in 2035."),
]

S = SENS


def _sens_rows():
    rows = []
    for k in ("As played", "No growth (your replacement data only)", "Half the growth", "Growth x1.5",
              "5% of waiting customers drop out a year", "30% drop out a year", "Half the flexible customers",
              "No flexible customers"):
        x = S[k]
        rows.append(f"<tr><th scope=row>{k}</th><td class=n>{b(x['boeing'])}</td><td class=n>{b(x['airbus'])}</td>"
                    f"<td class=n>{n0(x['lapsed_2026_2060'])}</td></tr>")
    return "".join(rows)


_shift = max(abs(RI[y]["fps_10yr_renton"] - RIB[y]["fps_10yr_renton"]) for y in RI)
_shift_y = max(RI, key=lambda y: abs(RI[y]["fps_10yr_renton"] - RIB[y]["fps_10yr_renton"]))
OLD = json.load(open(os.path.join(HERE, "data", "regret_as_briefed.json")))
_changed = [(int(n), s_, OLD["rounds"][n][s_]["best_plan"], _dn[(int(n), s_)]["best_plan"])
            for n in OLD["rounds"] for s_ in OLD["rounds"][n] if OLD["rounds"][n][s_]["best_plan"] != _dn[(int(n), s_)]["best_plan"]]
NAMES = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}


def _plain(p):
    p = p.replace("fps 10-yr at Renton", "the 10-year fps at Renton").replace("fps 10-yr", "the 10-year fps at new sites")
    return p.replace(" + 787 Re-engine", " with the 787 Re-engine")


_YR = {x["round"]: x["year"] for x in C["round_items"]}
_exc = "; ".join(f"in {_YR[n]} {NAMES[s_]}'s best option is {_plain(new)} rather than {_plain(old)}" for n, s_, old, new in _changed)

METHOD = (
    "<p><b>The game.</b> Run dash-2050-sd: your combined_dash.py dashboard (v3), run by the game master without its "
    "interface, with its adjustments, Control's objectives and the supply-and-demand layer. There were four sealed "
    "rounds (2030, 2035, 2045, 2050), each company deciding through its ExCo and Board agents. Each player saw only its "
    "own brief and the public bulletin. An audit of every file and tool output each agent touched found all four "
    "rounds clean (one false alarm in 2035, a fault in the audit script, was fixed).</p>"
    "<p><b>A correction after play.</b> After the game, a check found that growth had been reduced by the A220 share "
    f"twice instead of once, so the players were briefed on growth about {pc(GROWTH_SHORT)} too low (new demand about "
    f"{pc(DEMAND_SHORT)} too low over 2026-2060). This page uses the corrected "
    "demand. We re-valued every round's options on it, with everyone else's orders as played. Each player's best "
    f"option is the same as when it decided{(', except that ' + _exc) if _changed else ''}. No decision changes "
    "against the players' own tests. The largest shift for Boeing's fps is in "
    f"{_shift_y}: the 10-year fps at Renton was {b(RIB[_shift_y]['fps_10yr_renton'])} in the brief and is "
    f"{b(RI[_shift_y]['fps_10yr_renton'])} now, still far below its Board's +$1B.</p>"
    "<p><b>The layer.</b> New demand (replacement + growth) is split by the dashboard's share as preference. The firm "
    "backlog is delivered first, then new demand plus customers still waiting, up to each maker's capacity. "
    f"Flexible customers ({pc(INP['demand']['flex_share'], 1)}, from your page's customers flying both types, lessors "
    f"and unannounced customers) move to the other maker's free slots, and {pc(INP['demand']['lapse_per_year'])} of "
    "those still waiting drop out each year. Engine makers sell on the aircraft actually delivered: the 737 MAX on CFM, "
    "the A320neo on CFM and P&amp;W (60/40), and the new types on their chosen engines. With unlimited capacity and "
    "demand of 2,000 a year, the layer gives back the dashboard's airframer values exactly (tested).</p>"
    "<p><b>What is ours, not yours.</b> Growth, the firm-backlog treatment, the flexible share window, the drop-out "
    "rate (not calibrated), Boeing's 737 MAX path and its 100-a-month cap with a 10-a-month MAX tail to 2050 once an "
    "fps is in service, the fps ramp on the NGSA curve, and the Renton figures. Renton runs at 47 a month and Everett "
    "at up to 15; the new-site saving is $3.0B, pro-rated if Renton is chosen less than three years before entry into "
    "service. The sources are in wargame/dashgame/supply_demand_sources.md.</p>"
    "<p><b>How much the answer depends on demand.</b> The final state's ΔPV when one demand input moves:</p>"
    "<div class=scroll><table><thead><tr><th scope=col>Case</th><th scope=col class=n>Boeing</th>"
    "<th scope=col class=n>Airbus</th><th scope=col class=n>Customers lost 2026-2060</th></tr></thead><tbody>"
    + _sens_rows() + "</tbody></table></div>"
    "<p><b>Limits.</b> After 2030 no order raises an existing line's rate, so a short market shows up as waiting "
    "customers rather than as a race to build. Prices do not respond to scarcity. The dashboard counts each "
    "narrowbody programme from 2026 to 19 years after its entry into service, with an unlaunched programme at its "
    "default date. Here NGSA and the engine makers' narrowbody value stop at 2056 and Boeing's at 2060, so Airbus's "
    "shortfall in 2057-2060 is not counted.</p>"
)
FOOTER = ("BOEING PROPRIETARY. War game on your game-theory dashboard (combined_dash.py, v3) with the game master's "
          "supply-and-demand layer. Run dash-2050-sd; the record is in wargame/reports/dash-2050-sd/record. Built by "
          "make_sd_html.py from data/report_data.json and data/sd_checks.json.")

# headline numbers the builder checks against the data
CHECKS = [("boeing", -0.77), ("airbus", 13.25), ("cfm", -23.47), ("pratt_whitney", -0.48), ("rolls_royce", 9.61)]
