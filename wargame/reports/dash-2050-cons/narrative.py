"""Words for the conservative-case game page. Every number is read from data/report_data.json (run dash-2050-cons),
data/cons_checks.json (make_cons_checks.py) or ../dash-2050-sd/data (the previous game) and formatted here, so the text
cannot drift from the data. Players' reasons are paraphrased from their own returns in the run record."""
import json
import os
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
C = json.load(open(os.path.join(HERE, "data", "cons_checks.json")))
PREV = json.load(open(os.path.join(HERE, "..", "dash-2050-sd", "data", "report_data.json")))
PC = json.load(open(os.path.join(HERE, "..", "dash-2050-sd", "data", "sd_checks.json")))
F = D["rounds"][-1]
SD = F["sd"]
Y = SD["year"]
PSD = PREV["rounds"][-1]["sd"]
MINUS = "−"
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAMES = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt &amp; Whitney", "rolls_royce": "Rolls-Royce"}


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


def at(key, year, side=None, src=None):
    src = src or SD
    s = src[side] if side else src
    return s[key][src["year"].index(year)]


def span(years):
    """'2035-2047' for a run of years, '2050' for one."""
    return f"{years[0]}-{years[-1]}" if len(years) > 1 else str(years[0])


def runs(years):
    """Contiguous runs of years as text: '2035-2043, 2045-2046 and 2050-2051'."""
    out, cur = [], []
    for y in years:
        if cur and y != cur[-1] + 1:
            out.append(cur)
            cur = []
        cur.append(y)
    if cur:
        out.append(cur)
    t = [span(x) for x in out]
    return t[0] if len(t) == 1 else ", ".join(t[:-1]) + " and " + t[-1]


# ─────────────────────────────── values ───────────────────────────────
V = {s: F["value"][s]["pv_delta"] for s in SIDES}
VP = {s: PREV["rounds"][-1]["value"][s]["pv_delta"] for s in SIDES}
BC = D["board_check"]
NL = C["no_layer"]
BR = {s: F["value"][s]["bridge"] for s in ("boeing", "airbus")}
FPS = {x["plan"]: x for x in C["fps_2030"]["with_sd"]}
FPS0 = {x["plan"]: x for x in C["fps_2030"]["board"]}
RI = {x["year"]: x["now"] for x in C["round_items"]}
RIP = {x["year"]: x["now"] for x in PC["round_items"]}
REG = D["regret"]
REGP = PREV["regret"]
INP = D["sd_inputs"]
OPT = INP["options"]
STEPS = C["steps"]
AS = {x["case"]: x for x in C["assumptions"]}
U = C["fps_units"]
WACC_B = D["rounds"][0]["value"]["boeing"]["wacc"]
RYEARS = [x["year"] for x in D["rounds"]]

fps_d = lambda plan: FPS[plan]["boeing"] - FPS["Do Nothing"]["boeing"]
fps_d0 = lambda plan: FPS0[plan]["boeing"] - FPS0["Do Nothing"]["boeing"]
FPS_REN = {y: RI[y]["fps_10yr_renton"] for y in RYEARS}
FPS_NEW = {y: RI[y]["fps_10yr_new_site"] for y in RYEARS}
FPS_REN_P = {y: RIP[y]["fps_10yr_renton"] for y in RYEARS}
# change from one round to the next, net of moving the same launch later (discounting only)
REAL_GAIN = {y1: FPS_REN[y1] - FPS_REN[y0] / (1 + WACC_B) ** (y1 - y0) for y0, y1 in zip(RYEARS, RYEARS[1:])}
_rise = FPS_REN[RYEARS[-1]] - FPS_REN[RYEARS[0]]
_disc = 1 - sum(REAL_GAIN.values()) / _rise
DISC_WORD = "Most" if _disc > 0.6 else ("About half" if _disc >= 0.4 else "Part")

# the moves are the previous game's, round for round
def _norm(o):
    return {k: v for k, v in (o or {}).items() if v not in (None, "hold", "none") and not k.endswith("engine_code")}


SAME_MOVES = all(_norm(a["orders"][s]) == _norm(p["orders"][s]) for a, p in zip(D["rounds"], PREV["rounds"]) for s in SIDES) \
    and [x["year"] for x in PREV["rounds"]] == RYEARS
assert SAME_MOVES, "the moves differ from the previous game: rewrite the page's framing"
SAME_BEST = all(REG[n][s]["best_ex_post"]["plan"] == REGP[n][s]["best_ex_post"]["plan"] for n in REG for s in SIDES)

# ─────────────────────────────── market ───────────────────────────────
capb = lambda y: at("cap_max", y) + at("cap_fps", y)
capa = lambda y: at("cap_a320", y) + at("cap_ngsa", y)
cap = lambda y: capb(y) + capa(y)
dlvb = lambda y: at("dlv_max", y) + at("dlv_fps", y)
dlva = lambda y: at("dlv_a320", y) + at("dlv_ngsa", y)
gross = lambda y: at("demand_gross", y)
FIRM0 = INP["demand"]["firm_backlog"]["boeing"] + INP["demand"]["firm_backlog"]["airbus"]
FIRST_NEW = next(y for y in Y if at("demand", y) > 1e-6)
FIRM_CLEAR = next(y for y in Y if at("firm_b", y) < 0.5 and at("firm_a", y) < 0.5)
UNDER_TO = max(y for y in Y if y < FIRST_NEW and dlvb(y) + dlva(y) < cap(y) - 0.5)
B_SOLD = [y for y in Y if abs(dlvb(y) - capb(y)) < 0.5 and y >= FIRST_NEW - 1]
B_SOLD_RUN = []
for y in B_SOLD:
    if B_SOLD_RUN and y != B_SOLD_RUN[-1] + 1:
        break
    B_SOLD_RUN.append(y)
B_FADE_FROM = B_SOLD_RUN[-1] + 1
FLOOR_YEARS = [y for y in Y if at("pref_share", y, "boeing") > at("pref_b_base", y) + 1e-6]
PREF_PEAK = max(at("pref_share", y, "boeing") for y in Y)
PREF_PEAK_Y = max(Y, key=lambda y: at("pref_share", y, "boeing"))
NGSA_EIS = next(x["due"] for x in F["timeline"]["programmes"] if x["key"] == "ngsa")
BASE_END = at("pref_b_base", Y[-1])
WAIT_PEAK = max(SD["backlog_b"])
WAIT_PEAK_Y = Y[SD["backlog_b"].index(WAIT_PEAK)]
LAPSED = sum(SD["lost"])
SQ_LAPSED = sum(SD["sq_lost"])
FAC = SD["airbus_capacity_factor"]
FAC_FIRST = next(y for y, f in zip(Y, FAC) if f > 1 + 1e-9)
FAC_END = FAC[-1]
FAC_STOP = next(y for y, f in zip(Y, FAC) if abs(f - FAC_END) < 1e-9)
A_DIP = min(capa(y) for y in Y if y >= NGSA_EIS)
A_DIP_Y = min((y for y in Y if y >= NGSA_EIS), key=capa)
SQ_B_FULL_TO = max(y for y in Y if abs(at("sq_delivered_b", y) - 684) < 0.5)
SHARE_END = at("delivered_share", Y[-1], "boeing")
DEM_PEAK = max(gross(y) for y in Y)
DEM_PEAK_Y = max(Y, key=gross)
_y4060 = [y for y in Y if y >= 2040]
AVG_THIS = sum(gross(y) for y in _y4060) / len(_y4060)
AVG_PREV = sum(at("demand", y, src=PSD) for y in _y4060) / len(_y4060)
PREV_FIRM_CLEAR = next(y for y in PSD["year"] if PSD["firm_b"][PSD["year"].index(y)] < 0.5 and PSD["firm_a"][PSD["year"].index(y)] < 0.5)
assert PREV_FIRM_CLEAR < 2040


def _units(tag):
    o = U[tag]
    yy = o["do_nothing"]["year"]
    bd = lambda k, i: o[k]["dlv_max"][i] + o[k]["dlv_fps"][i]
    eis = o["fps_eis"]
    gain = sum(bd("fps_renton", i) - bd("do_nothing", i) for i, y in enumerate(yy) if y >= eis)
    ramp = [(y, bd("fps_renton", i) - bd("do_nothing", i)) for i, y in enumerate(yy) if y >= eis]
    neg = [(y, d) for y, d in ramp if d < -0.5]
    sd_line = o["fps_renton"]["bridge"]["supply_demand"] - o["do_nothing"]["bridge"]["supply_demand"]
    board = o["fps_renton"]["bridge"]["nb_profit_vs_sq"] - o["do_nothing"]["bridge"]["nb_profit_vs_sq"]
    pos = [(y, d) for y, d in ramp if d > 0.5]
    site = o["fps_renton"]["bridge"].get("supply_plan", 0.0) - o["do_nothing"]["bridge"].get("supply_plan", 0.0)
    return {"eis": eis, "gain": gain, "neg": neg, "neg_sum": sum(d for _, d in neg), "pos": pos,
            "pos_sum": sum(d for _, d in pos), "sd": sd_line, "board": board, "site": site}


UT, UP = _units("this_game"), _units("previous_market")
STEP = {x["step"].split(" (")[0]: x for x in STEPS}
ST0, ST_END = STEPS[0], STEPS[-1]
_ren = [x["fps_renton"] for x in STEPS]
_dn = [x["final"]["boeing"] for x in STEPS]
STEP_D = [(STEPS[i]["step"], _ren[i] - _ren[i - 1], STEPS[i]["final"]["boeing"] - STEPS[i - 1]["final"]["boeing"],
           STEPS[i]["final"]["airbus"] - STEPS[i - 1]["final"]["airbus"]) for i in range(1, len(STEPS))]
CAP_RESP = STEPS[-1]["final"]
NO_RESP = STEPS[-2]["final"]
assert abs(ST0["final"]["boeing"] - VP["boeing"]) < 1e-9 and abs(ST_END["final"]["boeing"] - V["boeing"]) < 1e-9
assert abs(ST0["fps_renton"] - (PC["fps_2030"]["with_sd"][2]["boeing"] - PC["fps_2030"]["with_sd"][0]["boeing"])) < 1e-9

OBJ_B = {o["label"].split(":")[0]: o for o in F["objectives"]["boeing"]}


def re787_if_a350(n):
    """The 787 Re-engine against hold, in the brief's column where Airbus launches the A350 Re-engine."""
    g = json.load(open(os.path.join(HERE, "record", "grids_r%d.json" % n)))["boeing"]
    rows = {x["plan"]: x["cells"] for x in g["rows"]}
    col = next(i for i, c in enumerate(g["scenarios"]) if c == "Airbus launches A350 Re-engine")
    return rows["fps: hold + 787 Re-engine"][col][0] - rows["fps: hold + 787: hold"][col][0]


RE787_A350 = {n: re787_if_a350(n) for n in (1, 2)}
DIP_YEARS = [y for y in Y if y >= NGSA_EIS and capa(y) < 0.9 * capa(NGSA_EIS - 1)]
B_SH = [at("delivered_share", y, "boeing") for y in Y if FIRST_NEW <= y <= B_SOLD_RUN[-1]]
FAC_STEPS = sum(1 for a, c in zip(FAC, FAC[1:]) if c > a + 1e-9)
FAC_AT_FADE = FAC[Y.index(B_FADE_FROM)]
_ua = [y for y in Y if y < FIRST_NEW and dlva(y) < capa(y) - 0.5]
_ub = [y for y in Y if y < FIRST_NEW and dlvb(y) < capb(y) - 0.5]
BOTH_UNDER_TO = max(set(_ua) & set(_ub))
B_UNDER_ONLY = [y for y in _ub if y > BOTH_UNDER_TO]
assert _ua == list(range(Y[0], BOTH_UNDER_TO + 1)) and _ub == list(range(Y[0], UNDER_TO + 1))
CR = C["cfm_response"]
assert abs(CR["delta"] - (CAP_RESP["cfm"] - NO_RESP["cfm"])) < 1e-6
assert not UP["neg"], "the fps cost deliveries in the previous market too: rewrite FPS_CAP"
assert all(abs(RI[y]["re787"] - RIP[y]["re787"]) < 5e-3 for y in RYEARS), "787 Re-engine value moved"

# ─────────────────────────────── words ───────────────────────────────
TITLE = "The war game on your conservative demand case"
LEDE = (f"We replayed the war game (ExCo and Board agents, Control's objectives, rounds 2030, 2035, 2045 and 2050) on "
        f"your new market assumptions. <b>Demand</b> is your conservative-case curve, and the {n0(FIRM0)} open firm orders "
        f"are its first slice, not extra (option B). <b>Boeing</b> loses 1 point of preference a year after NGSA enters "
        f"service, but never falls below the share Airbus cannot build. <b>Airbus</b> adds 1% capacity a year while it "
        f"is short. Every company played exactly the moves of the previous game: Airbus launched NGSA in 2030, the "
        f"engine makers settled by 2035, and Boeing never launched the fps. What changed is the money. The fps case "
        f"is much worse: a 10-year fps at Renton launched in 2030 is worth {b(FPS_REN[2030])} against Do Nothing, "
        f"against {b(FPS_REN_P[2030])} before. And with Do Nothing, Boeing's deliveries fall from 684 a year in "
        f"{B_SOLD_RUN[-1]} to {n0(dlvb(Y[-1]))} by {Y[-1]} ({pc(SHARE_END)} of the market).")

TILES = {
    "boeing": "Held every round; the fps never came near its Board's +$1B",
    "airbus": f"NGSA in 2030 on the Alt plan; {b(BC['airbus']['board'])} on the dashboard alone",
    "cfm": "GEnx upgrade in 2030; ducted engine and Embraer partnership in 2035",
    "pratt_whitney": "GTF2 folded into the Joint Venture in 2035",
    "rolls_royce": "UltraFan NB folded into the Joint Venture in 2035",
}

FINDINGS = [
    ("The same moves as the previous game, round for round.",
     " Airbus launched NGSA in 2030 on the Alt plan with all three engine makers. Pratt &amp; Whitney's and "
     "Rolls-Royce's 'launch if selected' orders were triggered, and CFM ordered the GEnx upgrade. In 2035 Pratt "
     "&amp; Whitney and Rolls-Royce formed the Joint Venture, and CFM launched its ducted engine and the Embraer "
     "partnership. Everyone held in 2045 and 2050. "
     + ("Each company's best alternative in every round is also the same as before: for Boeing the 787 Re-engine, for "
        "Airbus the A350 Re-engine. The same tests stopped both." if SAME_BEST else
        "The same tests stopped Boeing's 787 Re-engine. Airbus's A350 Re-engine failed the same CFO tests as "
        "before; in 2045 and 2050 its operating head also vetoed it, because no A350 engine would be mature in time. "
        "In the previous game that was only a warning.")),
    ("The fps case got much worse: the conservative curve is the main reason.",
     f" In 2030 a 10-year fps was worth {b(fps_d('fps 10-year, Renton'))} against Do Nothing at Renton and "
     f"{b(fps_d('fps 10-year, new sites'))} at new sites, against {b(FPS_REN_P[2030])} and "
     f"{b(RIP[2030]['fps_10yr_new_site'])} in the previous game. On the dashboard alone it is worth "
     f"{b(fps_d0('fps 10-year, Renton'))} at either site. At Renton, deliveries take {b(-UT['sd'], 2, False)} off it "
     f"here (against {b(-UP['sd'], 2, False)} before), and building at Renton saves {b(UT['site'], 2, False)} of "
     f"new-site capex. Your curve is smaller where the fps would sell: {n0(AVG_THIS)} aircraft a year "
     f"on average over 2040-{Y[-1]}, against {n0(AVG_PREV)} in the previous game's market. Stepping from the previous "
     f"market to this one, the curve alone moves the Renton case by {b(STEP_D[0][1])} and putting the firm orders "
     f"inside demand by {b(STEP_D[1][1])}. Your three share and capacity rules together move it by "
     f"{b(sum(x[1] for x in STEP_D[2:]))}. The case improved each round, to {b(FPS_REN[RYEARS[-1]])} at Renton in "
     f"{RYEARS[-1]}, but " + (f"all of that rise is discounting, because a later launch's loss is smaller at 2026. "
     f"Like for like, the case lost {b(-REAL_GAIN[2035], 2, False)} from 2030 to 2035 and moved by "
     f"{b(REAL_GAIN[2045])} and {b(REAL_GAIN[2050])} in the later rounds. " if sum(REAL_GAIN.values()) < 0 else
     f"{DISC_WORD.lower()} of that rise is only discounting. ") + "It never came near the +$1B that Boeing's Board "
     "requires."),
    (f"With Do Nothing, Boeing sells all it can build until {B_SOLD_RUN[-1]}, then fades to {pc(SHARE_END)}.",
     f" Boeing's preference falls 1 point a year from 40% after NGSA enters service in {NGSA_EIS}. But Airbus cannot "
     f"build all its customers want in most years to {FLOOR_YEARS[-1]}, and its slack comes to Boeing. NGSA's "
     f"transition cuts Airbus's capacity to {n0(A_DIP)} in {A_DIP_Y}, and Boeing's preference rises to "
     f"{pc(PREF_PEAK, 1)} that year. So the 737 MAX sells all the 684 aircraft it can build every year in "
     f"{span(B_SOLD_RUN)}, with up to {n0(WAIT_PEAK)} customers waiting for a Boeing slot ({WAIT_PEAK_Y}). Airbus's "
     f"capacity rises 1% after each year it is short: {FAC_STEPS} steps from {FAC_FIRST} to {FAC_STOP}, "
     f"{pc(FAC_END - 1, 1)} in all. From {B_FADE_FROM} Airbus can build nearly all its customers want, and Boeing's line runs below capacity: {n0(dlvb(B_FADE_FROM))} "
     f"aircraft in {B_FADE_FROM} and {n0(dlvb(Y[-1]))} in {Y[-1]}. In the status quo Boeing builds 684 a year to {SQ_B_FULL_TO} and {n0(at('sq_delivered_b', Y[-1]))} in "
     f"{Y[-1]}. Boeing's ΔPV is only {b(V['boeing'])} ({b(BC['boeing']['board'])} on the dashboard alone), because "
     f"the decline comes late and is heavily discounted."),
    (f"Airbus's capacity response is worth about {b(CAP_RESP['airbus'] - NO_RESP['airbus'], 0, False)} to Airbus "
     f"and costs Boeing about {b(NO_RESP['boeing'] - CAP_RESP['boeing'], 1, False)}.",
     f" Without it Airbus would end at {b(NO_RESP['airbus'])} and Boeing at {b(NO_RESP['boeing'])}. With 1% a year "
     f"they end at {b(CAP_RESP['airbus'])} and {b(CAP_RESP['boeing'])}, and at 2% a year at "
     f"{b(AS['Airbus capacity response 2% a year']['final_airbus'])} and "
     f"{b(AS['Airbus capacity response 2% a year']['final_boeing'])}. CFM loses most from it "
     f"({b(CR['delta'])}). In the status quo Airbus's extra aircraft are A320neos, 60% of them on CFM engines, "
     f"which raises CFM's yardstick by {b(CR['yardstick'], 2, False)}. In the game they are mostly NGSAs, on which "
     f"CFM has about {pc(CR['cfm_share_of_ngsa_engines_2050'])} of the engines. From {CR['displaced_years'][0]} "
     f"they also replace CFM-only 737 MAXs, which costs CFM {b(-CR['game_displacement'], 2, False)}, offset by "
     f"{b(CR['game_before_displacement'], 2, False)} gained from Airbus's extra output before then. Rolls-Royce gains {b(CAP_RESP['rolls_royce'] - NO_RESP['rolls_royce'], 2, False)}. Airbus ends at "
     f"{b(V['airbus'])}, against {b(VP['airbus'])} in the previous game; on the dashboard alone it would be "
     f"{b(BC['airbus']['board'])}."),
    ("The largest money left on the table is still the 787 Re-engine.",
     f" It was Boeing's best alternative in every round: worth {b(REG['1']['boeing']['regret_ex_post'])} in 2030, "
     f"{b(REG['2']['boeing']['regret_ex_post'])} in 2035, {b(REG['3']['boeing']['regret_ex_post'])} in 2045 and "
     f"{b(REG['4']['boeing']['regret_ex_post'])} in 2050. Against Do Nothing it is worth what it was worth in the "
     f"previous game, because the market rules touch only narrowbodies. In 2030 and 2035 its Board's −$1B downside limit stopped it: it lost more than that if Airbus "
     f"re-engined the A350 too. In 2045 and 2050 it was below the Board's +$1B business case. Airbus left the A350 "
     f"Re-engine ({b(REG['1']['airbus']['regret_ex_post'])} in 2030, {b(REG['4']['airbus']['regret_ex_post'])} in "
     f"2050) on its CFO's cash and robustness tests, and later on his +$1B test and its operating head's engine "
     f"readiness test."),
    ("The engine makers settled early; CFM and Pratt & Whitney lose more in this market, Rolls-Royce gains.",
     f" CFM ends at {b(V['cfm'])} (previous game {b(VP['cfm'])}), Rolls-Royce at {b(V['rolls_royce'])} "
     f"({b(VP['rolls_royce'])}) and Pratt &amp; Whitney at {b(V['pratt_whitney'])} ({b(VP['pratt_whitney'])}). With "
     f"no fps, the 737 stays CFM-only, so Boeing misses its dual-source objective again."),
]

INPUTS_LEDE = ("Your assumptions change the market in three ways; everything else is as it was. <b>Demand</b> is your "
               "conservative-case curve, and open firm orders are the first slice of it. <b>Boeing's preference</b> "
               "after NGSA follows your rule, with a floor at the share Airbus cannot build. <b>Airbus's capacity</b> "
               "rises 1% after each year in which it could not build all its customers wanted. The dashboard's share "
               "rule still applies before NGSA and once an fps is in service.")
DEMAND_TITLE = (f"Your conservative curve: {n0(gross(Y[0]))} aircraft in {Y[0]}, a peak of {n0(DEM_PEAK)} in "
                f"{DEM_PEAK_Y}; open firm orders are served first, and new customers start in {FIRST_NEW}")
DEMAND_CAP = (f"The curve is the smoothest annual fit to your table (see the demand-curve page), times the 737/A320 "
              f"class share ({pc(INP['demand']['class_share'], 2)}), held at its 2070 value after 2070. The "
              f"{n0(FIRM0)} open firm orders (737 MAX {INP['demand']['firm_backlog']['boeing']:,}; A320neo family "
              f"{INP['demand']['firm_backlog']['airbus']:,}) are part of this demand, not extra. Each year's demand is "
              f"served from them first, split by each maker's remaining orders, until the last are delivered in "
              f"{FIRM_CLEAR}" + (", the year new customers start." if FIRM_CLEAR == FIRST_NEW else f"; new customers start in {FIRST_NEW}.") + f" Through {UNDER_TO} demand is below what the two makers plan to build "
              f"({n0(gross(Y[0]))} against {n0(cap(Y[0]))} in {Y[0]}), so both run below plan through {BOTH_UNDER_TO}"
              f"{', and Boeing in ' + span(B_UNDER_ONLY) if B_UNDER_ONLY else ''}, in the status quo too. "
              f"The dashed line is the previous game's new demand (replacement plus growth), on top of which its firm "
              f"orders came.")
PREF_TITLE = (f"Boeing's preference: 40% less 1 point a year from NGSA's {NGSA_EIS} entry into service, lifted to "
              f"Airbus's slack whenever Airbus is short ({runs(FLOOR_YEARS)})")
PREF_CAP = (f"The base rule reaches {pc(BASE_END)} in {Y[-1]}. The floor is the share of the year's new customers that "
            f"Airbus cannot build after its own firm orders and waiting customers. It binds hardest in {PREF_PEAK_Y}, "
            f"when NGSA's transition cuts Airbus's capacity to {n0(A_DIP)}. A preference above what Boeing can build "
            f"becomes customers waiting for a Boeing slot, and a tenth of them drop out each year. From "
            f"{FLOOR_YEARS[-1] + 1} Airbus can build all its customers want, and Boeing's delivered share follows "
            f"the base rule.")
AIRBUS_TITLE = (f"Airbus adds 1% capacity after each year it is short, from {FAC_FIRST}: {pc(FAC_END - 1, 1)} above "
                f"your Rev. B plan by {FAC_STOP}")
AIRBUS_CAP = ("The plan is your Airbus Rev. B chart on the Alt plan, which Airbus chose in 2030 (NGSA in service in "
              f"{NGSA_EIS}). 'Short' means its customers, at the base preference, want more than it can build after its "
              "firm orders and waiting customers. The step is compounding and applies from the next year. Capacity "
              "never comes down.")
MARKET_LEDE = (f"Four phases. Through {UNDER_TO} demand is below the factories' plans and the firm orders are "
               f"delivered as demand calls them. From {FIRST_NEW} new customers arrive and the market is short: Boeing "
               f"sells all it can build, and the slack Airbus cannot cover waits for Boeing. In {span(DIP_YEARS)}, "
               f"NGSA's transition cuts Airbus's output. From {B_FADE_FROM} Airbus, now {pc(FAC_AT_FADE - 1)} above its "
               f"plan, can build nearly all its customers want (it is short again only in "
               f"{runs([y for y in FLOOR_YEARS if y > B_FADE_FROM])}), and Boeing's line runs below capacity as its "
               f"preference keeps falling.")
MARKET_TITLE = (f"Demand runs below the factories' plans through {UNDER_TO}; from {B_FADE_FROM} Airbus nearly "
                f"catches up and Boeing's deliveries fall")
BOEING_LINES_TITLE = (f"With Do Nothing, Boeing's 737 MAX sells all 684 aircraft a year it can build in "
                      f"{span(B_SOLD_RUN)}, then falls to {n0(dlvb(Y[-1]))} by {Y[-1]}")
BOEING_LINES_CAP = ("Boeing's capacity is the 737 MAX path (42.5 to 57 a month by 2030). Boeing did not order the 737 "
                    "rate increase (100 a year from 2032), which was open only in 2030. In the status quo Boeing keeps "
                    "40% of customers' preference, so its line stays full until demand falls in the late 2050s.")
AIRBUS_LINES_TITLE = (f"Airbus's output dips to {n0(dlva(A_DIP_Y))} in {A_DIP_Y} in the NGSA transition; with the 1% "
                      f"steps its capacity ends at {n0(capa(Y[-1]))} a year")
BACKLOG_TITLE = (f"Open firm orders run off by {FIRM_CLEAR}; customers waiting for Boeing peak at {n0(WAIT_PEAK)} in "
                 f"{WAIT_PEAK_Y}")
BACKLOG_CAP = (f"Firm orders never lapse or switch maker. Waiting customers are new customers who could not be served "
               f"in their year: a tenth drop out each year ({n0(LAPSED)} over {Y[0]}-{Y[-1]}, against "
               f"{n0(SQ_LAPSED)} in the status quo).")
MOVES_LEDE = ("All the moves came in the first two rounds; after 2035 every company held. They are the previous game's "
              "moves exactly. Supply plans are shown only when they change. Boeing kept its default of new sites "
              "throughout, since the site matters only with a launch.")


def _r(y, k):
    return b(RI[y][k])


ROUND_NOTES = [
    ("2030.",
     f" Airbus launched NGSA (CFM, P&amp;W and Rolls-Royce engines) on the Alt plan. Boeing held everything: every fps "
     f"option lost money against Do Nothing ({_r(2030, 'fps_10yr_renton')} for a 10-year fps at Renton). The 787 "
     f"Re-engine ({_r(2030, 're787')} against Airbus's actual moves) lost {b(-RE787_A350[1], 2, False)} if Airbus "
     f"re-engined the A350 too. That is past the Board's −$1B limit, so Boeing expected a veto. Airbus's A350 "
     f"Re-engine ({_r(2030, 'rea350')}) beside NGSA was a second launch in one round and broke its CFO's "
     f"peak-cash line; alone it failed his robustness test."),
    ("2035.",
     f" P&amp;W and Rolls-Royce formed the Joint Venture; CFM launched the ducted engine and the Embraer partnership. "
     f"Boeing held: its CFO's buffer test vetoed every fps row (Renton {_r(2035, 'fps_10yr_renton')}), and the Board's "
     f"downside limit stopped the 787 Re-engine ({_r(2035, 're787')}; {b(RE787_A350[2])} if Airbus re-engined the "
     f"A350). Airbus's A350 Re-engine "
     f"({_r(2035, 'rea350')}) failed its CFO's peak-cash and robustness tests during NGSA's last development years."),
    ("2045 and 2050.",
     f" Everyone held. The fps at Renton improved to {_r(2045, 'fps_10yr_renton')} and then "
     f"{_r(2050, 'fps_10yr_renton')}, inside Boeing's downside limit in 2050 for the first time but still about "
     f"{b(1 - FPS_REN[2050], 1, False)} short of the Board's +$1B business case. The 787 Re-engine fell to {_r(2045, 're787')} and "
     f"{_r(2050, 're787')}, below the business case. Airbus's A350 Re-engine ({_r(2045, 'rea350')}, then "
     f"{_r(2050, 'rea350')}) failed its CFO's +$1B test and its operating head's engine-readiness test: no A350 "
     f"engine was mature in time. In 2050 Boeing's CEO said publicly that 57 a month is capacity, not the build "
     f"rate, as deliveries fall to {n0(dlvb(2050))}."),
]
FPS_LEDE = (f"Boeing's fps decision each round: the value of each launch against Do Nothing, with everyone else's "
            f"orders as played and nobody moving after the round, here and in the previous game. Boeing's Board "
            f"requires more than +$1B in the expected case and never more than −$1B in any plausible column.")
FPS_TABLE_NOTE = (f"Airbus's column is the A350 Re-engine added to the moves Airbus played; in 2030 that is beside its "
                  f"NGSA launch on the Alt plan. Boeing's columns are each launch against Boeing doing nothing.")
FPS_TITLE = (f"A 10-year fps at Renton from 2030 adds a net {n0(UT['gain'])} Boeing deliveries over "
             f"{UT['eis']}-{Y[-1]} (previous market {n0(UP['gain'])}): {n0(-UT['neg_sum'])} fewer in "
             f"{runs([y for y, _ in UT['neg']])} as Renton's MAX lines wind down, then {n0(UT['pos_sum'])} more in "
             f"{runs([y for y, _ in UT['pos']])}")
FPS_CAP = (f"Boeing's deliveries with Do Nothing and with a 10-year fps at Renton launched in 2030 (in service "
           f"{UT['eis']}), everyone else's round-1 orders as played. At Renton the MAX lines wind down as the fps "
           f"ramps. With Do Nothing the MAX sells everything it builds in those years, because Airbus is short. "
           f"So in {runs([y for y, _ in UT['neg']])} the fps costs Boeing deliveries. In the previous game's market "
           f"Boeing's line had spare capacity then, and the fps added deliveries in every year. On the dashboard "
           f"alone the fps adds {b(UT['board'])} of narrowbody profit in both markets. Deliveries take "
           f"{b(-UT['sd'], 2, False)} back here, against {b(-UP['sd'], 2, False)} there.")
VALUE_LEDE = ("ΔPV is each company's change in present value against the status quo, at 2026, valued by the dashboard "
              "with the game master's adjustments and the supply-and-demand layer. The status quo (no new programme) "
              "runs through the same layer and the same rules: Boeing keeps 40% of customers' preference, the "
              "slack floor applies, and Airbus adds capacity when short.")
BRIDGE_CAP = (f"The lines above the supply-and-demand line are the dashboard's own numbers for these moves (they sum "
              f"to Boeing {b(BC['boeing']['board'])} and Airbus {b(BC['airbus']['board'])}). The supply-and-demand "
              f"line replaces the dashboard's 2,000-a-year deliveries with what was actually wanted and built, against "
              f"the status quo run the same way. The supply-plan line is the Alt plan's $0.75B, booked at NGSA's "
              f"{NGSA_EIS} entry into service.")
_ob = OBJ_B.get("Hold the 50/50 NB split")
SHARES_LEDE = ("Control's 50/50 and incumbency objectives are scored on customers' preference. "
               + (f"Boeing misses both: {_ob['detail']}. " if _ob else "")
               + f"The 2040 figure is above 50% only because Airbus is short that year and its slack counts as "
               f"preference for Boeing. What Boeing delivers falls to {pc(SHARE_END)} by {Y[-1]}. In the previous "
               f"game Boeing delivered {pc(PSD['boeing']['delivered_share'][-1])} in {PSD['year'][-1]}, with flexible "
               f"customers spilling over from a short Airbus.")
SHARES_TITLE = (f"Boeing delivers {pc(min(B_SH))}-{pc(max(B_SH))} of the market while its line is full "
                f"({span(B_SOLD_RUN)}), then {pc(SHARE_END)} by {Y[-1]}")
PLAY_LEDE = ("The round game is the airframers' options for that round, with everyone else's orders as played and no "
             "later moves. As before, neither airframer played a pure equilibrium of the round. Each side's best reply "
             "included a Re-engine that its own tests ruled out. Regret is the final ΔPV of a side's best alternative "
             "minus what it played, with everyone else's actual orders and later rounds replayed.")
COMPARE_LEDE = (f"The previous game (dash-2050-sd) had the same agents, objectives and supply plans. Its market was "
                f"replacement of today's fleets plus growth, with the firm orders on top, the dashboard's share rule "
                f"(Airbus +3 points a year to 80%) and flexible customers spilling over; capacity was fixed. Since "
                f"the moves are the same, every difference comes from the market. The table steps from the previous "
                f"market to this one, one of your assumptions at a time, on this game's moves (the first row "
                f"reproduces the previous game exactly).")
SENS_LEDE = ("How much the answer depends on each of your assumptions: the 2030 fps decision (against Do Nothing, "
             "round-1 orders as played) and the final ΔPVs, with one assumption changed and the rest as played.")

_p2, _p3, _nf = AS["Boeing loses 2 points a year"], AS["Boeing loses 3 points a year"], AS["No slack floor (flexible customers' overflow only)"]
_same23 = _p2["dlv_b"] == _p3["dlv_b"] and abs(_p2["airbus_capacity_factor_end"] - _p3["airbus_capacity_factor_end"]) < 1e-12
assert _same23 and _p2["floor_years_from_ngsa"] == _p2["years_from_ngsa"] and _p3["floor_years_from_ngsa"] == _p3["years_from_ngsa"]
SENS_NOTE = (f"Losing 2 or 3 points a year gives the same result. In both cases Airbus is short in every year from NGSA's "
             f"entry into service, so Boeing gets exactly Airbus's slack. Airbus's capacity grows on the same path, to "
             f"{pc(_p2['airbus_capacity_factor_end'] - 1)} above plan by {Y[-1]}, when Boeing's share is "
             f"{pc(_p2['pref_b_end'], 1)}. Without the slack floor Boeing still gets some of Airbus's overflow through "
             f"flexible customers ({n0(_nf['spill_b'])} aircraft over {Y[0]}-{Y[-1]}).")

METHOD = (
    "<p><b>The game.</b> Run dash-2050-cons: your combined_dash.py dashboard (v3), run by the game master without its "
    "interface, with its adjustments, Control's objectives and the supply-and-demand layer, now with your "
    "market assumptions (sd_options.json in the run record). There were four sealed rounds (2030, 2035, 2045, 2050), "
    "each company deciding through its ExCo and Board agents. Each player saw only its own brief and the public "
    "bulletin, and the briefs and rules described the new assumptions. An audit of every file and tool output each "
    "agent touched found all four rounds clean. A false alarm in 2045, from the audit script misreading an escaped "
    "quote, was fixed and the rounds were re-audited.</p>"
    "<p><b>Your assumptions, as built.</b> (1) Demand is the conservative curve, times the class share. (2) Option B: "
    "each year's demand is served first from open firm orders, split by each maker's remaining orders, and only "
    "then from new customers. (3) Boeing's base preference is 40% less 1 point a year from NGSA's entry into service, "
    "while no fps is in service. Once an fps enters service the dashboard's share rule applies again. (4) The floor: "
    "Boeing's preference is never below the share of new customers Airbus cannot build after its firm orders and "
    "waiting customers. It applies in every case, the status quo included. (5) Airbus's capacity rises 1%, "
    "compounding from the next year, after each year in which its customers at the base preference want more than "
    "it can build; it never falls. Everything else is the previous game's layer: flexible customers "
    f"({pc(INP['demand']['flex_share'], 1)}) take the other maker's free slots, {pc(INP['demand']['lapse_per_year'])} "
    "of waiting customers drop out each year, and engine makers sell on the aircraft actually delivered.</p>"
    "<p><b>Tests.</b> test_sd_options.py checks each assumption on throw-away runs: an empty options file changes "
    "nothing, demand follows the curve, firm orders plus new customers add up to demand with no front-loading, "
    "the 1-point rule, the floor, and the 1% steps. Runs without the options file are unchanged: the previous game's "
    "values are reproduced to the cent (the first row of the step table).</p>"
    "<p><b>Limits.</b> After 2030 no order raises Boeing's line rate, so a short market shows up as waiting customers. "
    "Prices do not respond to scarcity. The dashboard counts each narrowbody programme from 2026 to 19 years after its "
    "entry into service, with an unlaunched programme at its default date. Here NGSA and the engine makers' "
    "narrowbody value stop at 2056 and Boeing's at 2060, so the later decline is counted only to then.</p>"
)
FOOTER = ("BOEING PROPRIETARY. War game on your game-theory dashboard (combined_dash.py, v3) with the game master's "
          "supply-and-demand layer and your conservative-case assumptions. Run dash-2050-cons; the record is in "
          "wargame/reports/dash-2050-cons/record. Built by make_cons_html.py from data/report_data.json and "
          "data/cons_checks.json.")

# headline numbers the builder checks against the data
CHECKS = [("boeing", -0.83), ("airbus", 14.09), ("cfm", -28.04), ("pratt_whitney", -1.65), ("rolls_royce", 11.03)]
