"""Build dash_2050_phaseout.html: the MAX phase-out game (run dash-2050-phaseout) against the conservative-case game
(dash-2050-cons): the orders, Boeing's fps case round by round and why it moved, how much rests on demand after 2060,
the market in the final state and who picks up what, and each company's value.

Reads data/dash-2050-phaseout.json and data/dash-2050-cons.json (extract.py, one run each), data/steps_2030.json and
data/steps_2050.json (steps.py), data/tail.json (tail.py), data/comac_units.json (comac_units.py) and
data/who_picks_up.json (who_picks_up.py), data/thresholds.json (thresholds.py), dashgame/demand_page_n0.json and demand_conservative.json, and the round
records under record/. Every figure on the page comes from those files; the claims in the copy are asserted against
them below.

  python3 make_phaseout_html.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HERE, "..", "..", "dashgame")
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
D = lambda n: json.load(open(os.path.join(HERE, "data", n)))
P, C, S30, S50, T = D("dash-2050-phaseout.json"), D("dash-2050-cons.json"), D("steps_2030.json"), D("steps_2050.json"), D("tail.json")
CU, WP, TH = D("comac_units.json"), D("who_picks_up.json"), D("thresholds.json")
OPT = json.load(open(os.path.join(DG, "sd_options_phaseout.json")))
CLASS = json.load(open(os.path.join(DG, "supply_demand.json")))["demand"]["class_share"]
REC = lambda run, n: json.load(open(os.path.join(HERE, "..", run, "record", "exco_result_r%d.json" % n)))["sides"]["boeing"]
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
REN = "fps 10-yr at Renton + 787: hold"
DN = "fps: hold + 787: hold"
DEFAULTS = {"hold", None, "none", "new_site", "base"}
# the column of each round's Boeing brief that matches what Airbus then did
REAL = {2030: "Airbus launches NGSA on the A320 Alt plan", 2035: "Rivals hold", 2045: "Rivals hold", 2050: "Rivals hold"}
# Boeing's CEO's expected column per round (record/exco_result_rN.json, decision/expected_scenario), as in tail.py and
# thresholds.py: 2030 S2 alone (the CEO's column, which the Board also used); 2035 70/30; 2045 and 2050 80/20
CEO_W = {2030: {1: 1.0}, 2035: {0: 0.7, 2: 0.3}, 2045: {0: 0.8, 1: 0.2}, 2050: {0: 0.8, 1: 0.2}}


def b(v, dp=2, sign=True):
    """Dollar figure for HTML: kept on one line."""
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    """Dollar figure as plain text (SVG, tooltips, tiles)."""
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def r2(v):
    return K.rnd(v, 2)


def nw(s):
    return f'<span class="nw">{s}</span>'


# ─────────────────────────────── the orders ───────────────────────────────
CODE_TXT = {7: "CFM/GE, Pratt & Whitney and Rolls-Royce"}
LABEL = {"ngsa": "NGSA", "a320_plan": "A320 plan", "genx": "GEnx", "gtf2_solo": "GTF2 Solo", "ultrafan_nb_solo": "UltraFan NB Solo",
         "ducted": "ducted engine", "partner_embraer": "Embraer partnership", "jv_with_rr": "Joint Venture with Rolls-Royce",
         "jv_with_pw": "Joint Venture with Pratt & Whitney", "fps": "fps", "re787": "787 Re-engine", "rate_737": "737 rate",
         "fps_site": "fps site", "rea350": "A350 Re-engine", "delay_tactics": "Delay Tactics"}
VAL = {"launch": "launch", "launch_if_selected": "launch if selected", "alt": "Alt (A320 kept longer)", "upgrade_genx9": "upgrade",
       "commit": "commit", "launch_10yr": "launch, 10-year", "launch_7yr": "launch, 7-year"}


def moves(o):
    """Orders that differ from holding (an engine code rides with its launch, below)."""
    return {k: v for k, v in o.items() if not k.endswith("engine_code") and v not in DEFAULTS}


def move_txt(o):
    m = moves(o)
    if not m:
        return '<span class="muted">holds everything</span>'
    parts = []
    for k, v in m.items():
        t = f"{LABEL.get(k, k)}: {VAL.get(v, v)}"
        code = o.get(k + "_engine_code")
        if str(v).startswith("launch") and code is not None:
            t += f", engines from {CODE_TXT[code]}"
        parts.append(t)
    return "; ".join(parts)


# ─────────────────────────────── facts (asserted) ───────────────────────────────
YEARS = [r["year"] for r in P["rounds"]]
SAME = all(P["rounds"][i]["orders"][s] == C["rounds"][i]["orders"][s] for i in range(4) for s in SIDES)
LAUNCHED = any(P["rounds"][i]["orders"]["boeing"].get("fps") not in ("hold", None) for i in range(4))
assert SAME and not LAUNCHED
# the one split: in 2030 this game's CEO put the 787 Re-engine to the Board (vetoed); the conservative game's CEO held it.
# The item was the same in both games.
_p1, _c1 = REC("dash-2050-phaseout", 1), REC("dash-2050-cons", 1)
assert _p1["decision"]["orders"]["re787"] == "launch" and _c1["decision"]["orders"]["re787"] == "hold"
_veto = [x for x in _p1["board_review"]["items"] if x["order_field"] == "re787"]
assert len(_veto) == 1 and _veto[0]["decision"] == "veto" and _veto[0]["ground"].startswith("Downside test fails")
assert not _c1["board_review"]["items"] and _p1["final_orders"]["re787"] == "hold"
assert "even odds" in _c1["decision"]["expected_scenario"] and "one-third" in _p1["decision"]["expected_scenario"]
for n in (2, 3, 4):
    assert REC("dash-2050-phaseout", n)["decision"]["orders"]["re787"] == "hold"


def re787_item(run, n):
    g = json.load(open(os.path.join(HERE, "..", run, "record", "grids_r%d.json" % n)))["boeing"]
    rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
    return [a - c for a, c in zip(rows["fps: hold + 787 Re-engine"], rows[DN])], g["scenarios"]


RE_P, _ = re787_item("dash-2050-phaseout", 1)
RE_C, _ = re787_item("dash-2050-cons", 1)
assert all(abs(a - c) < 1e-9 for a, c in zip(RE_P, RE_C))
RE_UP, RE_DOWN = max(RE_P), min(RE_P)
RE30_EVEN = 0.5 * RE_P[1] + 0.5 * RE_P[4]                     # conservative-case CEO: S2 and S5 at even odds
RE30_S2 = RE_P[1]                                              # this game's CEO: the expected column, S2 alone
assert RE30_EVEN < 1.0 < RE30_S2 and abs(RE30_S2 - RE_UP) < 1e-9 and RE_DOWN < -1.0
assert _p1["decision"]["expected_scenario"].startswith("S2") and "Re-engine adds +3.30" in _p1["decision"]["rationale"]
assert "40%" in REC("dash-2050-cons", 2)["decision"]["expected_scenario"]
# 2035: inside $1B on the CEO's weighted column, not if Airbus held; 2045 and 2050: inside $1B in every column
RE35, COLS35 = re787_item("dash-2050-phaseout", 2)
RE35_W = sum(RE35[i] * w for i, w in CEO_W[2035].items())
RE35_HOLD = RE35[COLS35.index("Rivals hold")]
assert RE35_W < 1.0 < RE35_HOLD and "30%" in REC("dash-2050-phaseout", 2)["decision"]["expected_scenario"]
for n in (3, 4):
    assert max(re787_item("dash-2050-phaseout", n)[0]) < 1.0


def real_col(g, i):
    cols = g["rounds"][i]["columns"]
    return g["rounds"][i]["fps_vs_dn"][REN][cols.index(REAL[YEARS[i]])]


GAP_P = [real_col(P, i) for i in range(4)]
GAP_C = [real_col(C, i) for i in range(4)]
RANGE_P = [(min(P["rounds"][i]["fps_vs_dn"][REN]), max(P["rounds"][i]["fps_vs_dn"][REN])) for i in range(4)]
RANGE_C = [(min(C["rounds"][i]["fps_vs_dn"][REN]), max(C["rounds"][i]["fps_vs_dn"][REN])) for i in range(4)]
WIDER = [r2(c) - r2(p) for p, c in zip(GAP_P, GAP_C)]            # from the rounded figures, so the table adds up
assert all(0.9 <= w <= 1.55 for w in WIDER), WIDER
assert all(GAP_P[i] < GAP_P[i + 1] for i in range(3)) and all(GAP_C[i] < GAP_C[i + 1] for i in range(3))   # shrinks
assert not all(WIDER[i] > WIDER[i + 1] for i in range(3))       # the difference between the games does not shrink
ab = [P["rounds"][i]["orders"]["airbus"] for i in range(4)]
assert ab[0]["ngsa"] == "launch" and ab[0]["a320_plan"] == "alt" and all(a["ngsa"] == "hold" and a["rea350"] == "hold"
                                                                         and a["delay_tactics"] == "none" and a["a320_plan"] == "alt" for a in ab[1:])
LOG1 = " | ".join(P["rounds"][0]["log"])
LOG2 = " | ".join(P["rounds"][1]["log"])
for s in ("P&W GTF2 (Solo) launched in 2030", "RR UltraFan NB (Solo) launched in 2030", "GEnx (CFM/GE) launched in 2030",
          "NGSA engine selection: RR, PW and CFM"):
    assert s in LOG1, s
for s in ("P&W GTF2 (Solo) folded into the Joint Venture", "RR UltraFan NB (Solo) folded into the Joint Venture",
          "P&W-RR Joint Venture NB engine launched in 2035", "CFM ducted engine launched in 2035", "CFM-Embraer partnership launched in 2035"):
    assert s in LOG2, s

# the bridges, on the rounded levels (so every displayed change is the difference of the displayed levels)
for st in (S30, S50):
    assert abs(sum(x["change"] for x in st["steps"][1:]) - (st["steps"][-1]["item"] - st["steps"][0]["item"])) < 1e-9
assert abs(S30["steps"][0]["item"] - GAP_C[0]) < 1e-9 and abs(S30["steps"][-1]["item"] - GAP_P[0]) < 1e-9
assert abs(S50["steps"][0]["item"] - GAP_C[3]) < 1e-9 and abs(S50["steps"][-1]["item"] - GAP_P[3]) < 1e-9
CH30 = [0.0] + [r2(S30["steps"][i]["item"]) - r2(S30["steps"][i - 1]["item"]) for i in range(1, 6)]
CH50 = [0.0] + [r2(S50["steps"][i]["item"]) - r2(S50["steps"][i - 1]["item"]) for i in range(1, 6)]
I_DEM, I_PH, I_XA, I_CO, I_EN = 1, 2, 3, 4, 5
assert min(CH30) == CH30[I_CO] and min(CH50) == CH50[I_DEM]
_c30 = S30["columns"].index(REAL[2030])
DN30 = [x["dn_vs_sq"][_c30] for x in S30["steps"]]
FPS30 = [x["item"] + d for x, d in zip(S30["steps"], DN30)]   # the fps plan against the status quo
PH_DN, PH_FPS = DN30[I_PH] - DN30[I_DEM], FPS30[I_PH] - FPS30[I_DEM]
CO_DN, CO_FPS = DN30[I_CO] - DN30[I_XA], FPS30[I_CO] - FPS30[I_XA]
assert PH_FPS > PH_DN > 0 and CO_FPS < CO_DN < 0 and abs(CO_DN) < 0.25 * abs(CO_FPS)
CU_DN, CU_F = CU["plans"][DN], CU["plans"][REN]
assert CU["column"] == REAL[2030] and CU["periods"][2] == [2045, 2049] and CU["periods"][3] == [2050, 2059]
assert CU_DN["by_period"][3] < 0.5 and CU_DN["by_period"][4] < 0.5 and CU_DN["by_period"][2] > 100
assert CU_F["to_2059"] > 3 * CU_DN["to_2060"]

# demand after 2060
TR = {r["year"]: r for r in T["rounds"]}
_page = json.load(open(os.path.join(DG, "demand_page_n0.json")))
_pg = {y: (r + g) * CLASS for y, r, g in zip(_page["years"], _page["replacements"], _page["growth"])}
_game = json.load(open(os.path.join(DG, "demand_conservative.json")))
_gm = {y: (r + g) * CLASS for y, r, g in zip(_game["years"], _game["replacements"], _game["growth"])}
_gtop = max(_gm.values())
assert abs(_pg[2060] - P["market"][-1]["demand"]) < 1e-6 and P["market"][-1]["year"] == 2060
TAILS = [("as run", f"Your page's curve (as run): {n0(_pg[2060])} a year in 2060, {n0(_pg[2072])} in 2072, {n0(_pg[2080])} in 2080"),
         ("held", f"Held at the 2060 level: {n0(_pg[2060])} a year"),
         ("game", f"The conservative curve: {n0(_gm[2061])} in 2061, rising to {n0(_gtop)} by {min(y for y, v in _gm.items() if v == _gtop)}")]


def tail_real(year, tname):
    t = TR[year]["tails"][tname]
    return t["items"][REN][t["columns"].index(REAL[year])]


def fps_items(year, tname):
    """Every fps launch as the Board tests it: the plan against the same plan with the fps held."""
    it = TR[year]["tails"][tname]["items"]
    out = {}
    for p, x in it.items():
        if p.startswith("fps: hold"):
            continue
        base = "fps: hold + " + p.split(" + ", 1)[1]
        out[p] = x if base == DN else [a - c for a, c in zip(x, it[base])]
    return out


def best_launch(year, tname):
    w = CEO_W[year]
    items = fps_items(year, tname)
    p = max(items, key=lambda q: sum(items[q][i] * x for i, x in w.items()))
    return sum(items[p][i] * x for i, x in w.items()), tname, p


assert all(abs(tail_real(y, "as run") - GAP_P[i]) < 1e-9 for i, y in enumerate(YEARS))
assert all(abs(tail_real(2030, k) - GAP_P[0]) < 1e-9 for k, _ in TAILS)
BEST = {y: max(best_launch(y, k) for k, _ in TAILS) for y in YEARS}
BEST_ANY = max(BEST.values())
assert BEST_ANY[0] < 0 and BEST_ANY[2] == REN and BEST_ANY[1] == "game"
assert all(v[2] == REN for v in BEST.values())                 # the 10-year at Renton is the best launch everywhere

# the market
MP = {x["year"]: x for x in P["market"]}
MC = {x["year"]: x for x in C["market"]}
SUM = lambda m, k, a, z: sum(m[y][k] or 0.0 for y in range(a, z + 1))
B45P, B45C = SUM(MP, "boeing", 2045, 2060), SUM(MC, "boeing", 2045, 2060)
A45P, A45C = SUM(MP, "airbus", 2045, 2060), SUM(MC, "airbus", 2045, 2060)
CO45, EN45 = SUM(MP, "comac", 2045, 2060), SUM(MP, "entrant", 2045, 2060)
CO_YRS = [y for y in range(2026, 2061) if (MP[y]["comac"] or 0) > 0.5]
assert CO_YRS[0] == 2035 and MP[2060]["boeing"] < 0.5 and A45P > 0.6 * SUM(MP, "demand", 2045, 2060)
DEM_P, DEM_C = SUM(MP, "demand", 2026, 2060), SUM(MC, "demand", 2026, 2060)
assert abs(DEM_P / DEM_C - 1) < 0.002
assert all(abs(MP[y]["demand"] - MC[y]["demand"]) < 1e-6 for y in range(2026, 2038)) and MP[2038]["demand"] < MC[2038]["demand"] - 250
assert all(MP[y]["demand"] < MC[y]["demand"] for y in range(2057, 2061))
EP, EC = WP["effect_of_phase_out"], WP["effect_of_comac"]
WAIT = WP["cases"]["no COMAC"]["waiting_end_2044"] - WP["cases"]["as run"]["waiting_end_2044"]
assert abs(-(EC["boeing"] + EC["airbus"] + EC["comac"] + EC["entrant"] + EC["lost"]) - WAIT) < 1.0 and WAIT > 0
assert abs(WP["cases"]["as run"]["boeing"] - B45P) < 1e-6 and abs(WP["cases"]["as run"]["comac"] - CO45) < 1e-6
assert abs(EP["comac"]) < 0.5 and EP["boeing"] < 0 < EP["airbus"] and EP["entrant"] > 0 and abs(EP["lost"]) < 0.5
assert abs(EP["boeing"] + EP["airbus"] + EP["entrant"]) < 1.0         # the MAX's lost customers all land somewhere
assert EC["airbus"] < EC["boeing"] < 0 and -EC["airbus"] > 0.8 * EC["comac"]
_src = open(os.path.join(DG, "test_phaseout.py")).read()
_tab = re.search(r'TABLE = """(.*?)"""', _src, re.S).group(1).replace("\n", "")
TAB = {int(t[0]): dict(zip(("demand", "cap_max", "boeing", "cap_airbus", "airbus", "comac", "entrant", "lost"), map(float, t[1:])))
       for t in (line.split() for line in _tab.split("|"))}
assert sorted(TAB) == list(range(2026, 2061))
FEWER = [y for y in range(2026, 2061) if MP[y]["boeing"] < TAB[y]["boeing"] - 5]
MORE_CAP = [y for y in range(2026, 2061) if MP[y]["cap_airbus"] > TAB[y]["cap_airbus"] + 5]
assert FEWER == [2037, 2038, 2044, 2045], FEWER
assert MORE_CAP == list(range(2037, 2045)), MORE_CAP
assert all(abs(MP[y]["boeing"] - TAB[y]["boeing"]) <= 0.5 + 1e-6 for y in range(2026, 2061) if y not in FEWER)
FEWER_TXT = ", ".join(f"{y} ({n0(MP[y]['boeing'])} against {n0(TAB[y]['boeing'])})" for y in FEWER[:-1]) + \
    f" and {FEWER[-1]} ({n0(MP[FEWER[-1]]['boeing'])} against {n0(TAB[FEWER[-1]]['boeing'])})"
assert any(MP[y]["boeing"] + MP[y]["airbus"] + MP[y]["comac"] + MP[y]["entrant"] > MP[y]["demand"] + 1 for y in range(2026, 2061))
B_ALL = sum(K.rnd(SUM(MC, "boeing", a, z), 0) - K.rnd(SUM(MP, "boeing", a, z), 0) for a, z in ((2026, 2044), (2045, 2060)))
_c50 = S50["columns"].index(REAL[2050])
DN50 = [x["dn_vs_sq"][_c50] for x in S50["steps"]]
assert abs(DN50[0] - C["final_value"]["boeing"]) < 1e-9 and abs(DN50[-1] - P["final_value"]["boeing"]) < 1e-9
V_PH = DN50[I_PH] - DN50[I_DEM]
V_REST = (DN50[-1] - DN50[0]) - V_PH
assert V_PH > 0 and abs(V_REST) < 0.1 * V_PH
assert B_ALL > 0


# what would change Boeing's decision (thresholds.py)
M0 = TH["base"]["margin"]
PRICE = TH["base"]["price_musd"]
BILL10, BILL7 = TH["base"]["bill"]["10yr"], TH["base"]["bill"]["7yr"]
THR = {int(n): r for n, r in TH["rounds"].items()}
THG = {int(n): r for n, r in TH["game_tail"].items()}
TP10, TP7 = "10-year at Renton", "7-year at Renton"
FR = TH["rounds"]["1"]["rule"]["frontier"]["fractions"]
fr = lambda r, mode, k: r[mode]["frontier"]["margin"][FR.index(k)]
assert TH["eps"] == 1.0 and TH["h8"] == 2.0
for n, r in THR.items():
    y = r["year"]
    assert y == YEARS[n - 1] and r["weights"] == {str(k): v for k, v in CEO_W[y].items()}
    assert r["base"]["rule"] is None and r["base"]["premium"] is None                 # nothing launches in the base case
    assert r["base"]["pick"] == ("Re-engine" if n == 1 else "Do Nothing")              # the CEO's decision in the record
    assert abs(r["rows"][TP10]["items"][r["columns"].index(REAL[y])] - GAP_P[n - 1]) < 1e-9
    for mode in ("rule", "premium"):
        assert r[mode]["margin_monotone"] and r[mode]["cut_monotone"]
    assert r["premium"]["margin"] <= r["rule"]["margin"] + 1e-9
    assert r["rule"]["cut"] is None or r["premium"]["cut"] <= r["rule"]["cut"] + 1e-9
    for k, c in r["confirm"].items():
        assert c["gap"] < 1e-5 and c["decision"] and all(m["stress_ok"] and m["stress_peak"] < 1e-9 for m in c["metrics"]), (n, k)
    assert r["rule"]["plan_at_margin"] == TP7
assert set(THR[1]["confirm"]) == set(THR[2]["confirm"]) == {"margin", "cut", "half"} and set(THR[3]["confirm"]) == {"cut", "half"}
assert THR[4]["rule"]["cut"] is None and THR[4]["premium"]["cut"] is None and THR[3]["premium"]["margin"] > 1.0
assert all(THG[n]["rule"]["plan_at_margin"] == TP10 for n in (3, 4))
R30, R35 = THR[1], THR[2]
_r7 = R30["rows"][TP7]["items"]
PP7 = R30["per_point"][TP7]
BOARD_ONLY_30 = M0 + (1.0 - sum(_r7[i] * w for i, w in CEO_W[2030].items())) / (100 * PP7)   # the Board's +$1B alone, 7-year
assert BOARD_ONLY_30 < R30["premium"]["margin"] < R30["rule"]["margin"]
P25 = fr(R30, "rule", 0.75) / 0.75          # a partner taking the same share of profit as it pays of the bill
P50 = fr(R30, "rule", 0.5) / 0.5
assert P25 > R30["rule"]["margin"] and P50 > P25
_f45 = THR[3]["rule"]["frontier"]["margin"]
LAST45 = max(k for k, m in zip(FR, _f45) if m is not None and m <= 1.0)     # the largest share of the bill 2045 can bear
assert 0.5 <= LAST45 < 1.0 and all(m is not None and m > 1.0 for k, m in zip(FR, _f45) if k > LAST45)
assert R30["per_point"][TP7] > R30["per_point"][TP10] and R30["rows"][TP7]["eis"] == R30["rows"][TP10]["eis"] - 3


def pctv(m, dp=1):
    return f"{K.rnd(100 * m, dp):.{dp}f}"


def mtxt(m):
    return None if (m is None or m > 1.0) else pctv(m) + "%"


def rng(lo, hi):
    """A threshold as premium-rule; over 100% margin cannot be reached (the unit cost would be negative)."""
    a, c = mtxt(lo), mtxt(hi)
    if a is None and c is None:
        return '<span class="muted">impossible</span>'
    if c is None:
        return nw(f"{a} \u2013 impossible")
    return nw(a if a == c else f"{a[:-1]}\u2013{c}")


def cut_rng(lo, hi):
    if lo is None and hi is None:
        return '<span class="muted">fails even at $0</span>'
    a, c = K.rnd(100 * lo, 0), K.rnd(100 * hi, 0)
    return nw(f"{a:.0f}%" if a == c else f"{a:.0f}\u2013{c:.0f}%")


def cost(m):
    return PRICE * (1 - m)


# ─────────────────────────────── charts and tables ───────────────────────────────
def gap_chart(narrow=False):
    w, h, left, right, top, bot = (360, 300, 46, 80, 24, 44) if narrow else (760, 300, 64, 196, 24, 44)
    lo, hi = -7.0, 1.5
    pad = 18 if narrow else 30
    sx = lambda y: left + pad + (y - YEARS[0]) / (YEARS[-1] - YEARS[0]) * (w - left - right - pad)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "Boeing's 10-year fps at Renton against Do Nothing, by round, in both games", "chart narrow" if narrow else "chart")]
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{bp(v, 0, False)}</text>')
        v += 1.0
    out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(1):.1f}" y2="{sy(1):.1f}" class="ref"/><text x="{left + 6}" y="{sy(1) - 6:.1f}" class="reflab">{"Board needs +$1B" if narrow else "The Board needs more than +$1B"}</text>')
    for y in YEARS:
        out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    for vals, col, dash, lab in ((GAP_C, "var(--muted)", ' stroke-dasharray="6 4"', "Conservative-case game"), (GAP_P, "var(--s1)", "", "MAX phase-out game")):
        d = "M" + " L".join(f"{sx(YEARS[i]):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{sx(YEARS[i]):.1f}" cy="{sy(v):.1f}" r="5" fill="{col}" class="ring" {K.mark_attrs((bp(v), f"{lab}, {YEARS[i]} brief", col))}/>')
        name = "" if narrow else esc(lab.replace("-case game", "").replace(" game", "")) + " "
        out.append(f'<text x="{w - right + 8}" y="{sy(vals[-1]) + 4:.1f}" class="endlab">{name}{bp(vals[-1])}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">{"$B PV at 2026" if narrow else "The brief column that matches what Airbus then did; $B PV at 2026"}</text></svg>')
    return "".join(out)


def market_chart(narrow=False):
    w, h, left, right, top, bot = (360, 300, 44, 22, 20, 44) if narrow else (760, 330, 54, 16, 20, 44)
    ys = list(range(2026, 2061))
    top_v = max(max(MP[y]["demand"] or 0, MP[y]["boeing"] + MP[y]["airbus"] + MP[y]["comac"] + MP[y]["entrant"]) for y in ys)
    hi = (int(top_v / 500) + 1) * 500
    bw = (w - left - right) / len(ys)
    sx = lambda y: left + (y - ys[0] + 0.5) * bw
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Aircraft delivered each year by maker, MAX phase-out game, final state", "chart narrow" if narrow else "chart")]
    v = 0
    while v <= hi:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{n0(v)}</text>')
        v += 500
    for y in ys:
        acc = 0.0
        m = MP[y]
        segs = [(k, var) for k, var in (("boeing", "s1"), ("airbus", "s2"), ("comac", "comac"), ("entrant", "s3")) if (m[k] or 0.0) > 0.5]
        for j, (k, var) in enumerate(segs):
            val = m[k]
            y0, y1 = sy(acc), sy(acc + val)
            gap = 1.0 if j else 0.0
            if j == len(segs) - 1:
                out.append(f'<path d="{K.bar_path(sx(y) - bw * 0.38, bw * 0.76, y0 - gap, y1)}" fill="var(--{var})"/>')
            else:
                out.append(f'<rect x="{sx(y) - bw * 0.38:.1f}" width="{bw * 0.76:.1f}" y="{y1 + 1:.1f}" height="{max(0.0, y0 - y1 - 1 - gap):.1f}" fill="var(--{var})"/>')
            acc += val
        out.append(f'<rect x="{sx(y) - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" '
                   + K.mark_attrs((str(y), "", None), (n0(m["boeing"]), "Boeing 737 MAX", "var(--s1)"), (n0(m["airbus"]), "Airbus", "var(--s2)"),
                                  (n0(m["comac"]), "COMAC", "var(--comac)"), (n0(m["entrant"]), "New entrant", "var(--s3)"),
                                  (n0(m["lost"] or 0), "Customers lost", None), (n0(m["demand"] or 0), "Demand", None)) + "/>")
    d = "M" + " L".join(f"{sx(y):.1f},{sy(MP[y]['demand'] or 0):.1f}" for y in ys)
    out.append(f'<path d="{d}" fill="none" stroke="var(--fg)" stroke-width="2" pointer-events="none"/>')
    for y in ys:
        if y % (10 if narrow else 5) == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">{"Aircraft a year, final state" if narrow else "737/A320-class aircraft delivered a year, final state of the MAX phase-out game"}</text></svg>')
    return "".join(out)


def frontier_chart(narrow=False):
    w, h, left, right, top, bot = (360, 340, 44, 64, 30, 48) if narrow else (760, 350, 56, 170, 30, 48)
    lo, hi = 0.0, 1.0
    pad = 14
    sx = lambda k: left + pad + k * (w - left - right - pad)
    sy = lambda m: top + (hi - m) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "fps margin needed for Boeing to launch, against the share of its fps investment Boeing pays, by round", "chart narrow" if narrow else "chart")]
    cid = "fclip-n" if narrow else "fclip-w"
    out.append(f'<defs><clipPath id="{cid}"><rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}"/></clipPath></defs>')
    for v in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{K.rnd(100 * v, 0):.0f}%</text>')
    for k in (0.0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<text x="{sx(k):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{K.rnd(100 * k, 0):.0f}%</text>')
    styles = {1: ("var(--s1)", ""), 2: ("var(--s1)", ' stroke-dasharray="7 4"'), 3: ("var(--muted)", ""), 4: ("var(--muted)", ' stroke-dasharray="7 4"')}
    labels = []
    for n, r in THR.items():
        pts = [(k, m) for k, m in zip(FR, r["rule"]["frontier"]["margin"]) if m is not None]
        col, dash = styles[n]
        d = "M" + " L".join(f"{sx(k):.1f},{sy(m):.1f}" for k, m in pts)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.2"{dash} clip-path="url(#{cid})"/>')
        for k, m in pts:
            if k in (0.0, 0.25, 0.5, 0.75, 1.0) and m <= hi:
                val = pctv(m) + "%"
                tip = "%d: margin needed if Boeing pays %.0f%% of its fps investment" % (r["year"], K.rnd(100 * k, 0))
                out.append(f'<circle cx="{sx(k):.1f}" cy="{sy(m):.1f}" r="4" fill="{col}" class="ring" {K.mark_attrs((val, tip, col))}/>')
        inside = [(k, m) for k, m in pts if m <= hi]
        k_end, m_end = inside[-1] if inside else (0.0, hi)
        y_lab = sy(m_end) + 4 if k_end == 1.0 else sy(hi) + 16
        labels.append([sx(k_end) + 8, y_lab, str(r["year"])])
    right_end = sorted((l for l in labels if abs(l[0] - (sx(1.0) + 8)) < 1e-6), key=lambda l: l[1])
    for a, b2 in zip(right_end, right_end[1:]):          # keep the right-hand labels apart (one text line)
        if b2[1] - a[1] < 20:
            b2[1] = a[1] + 20
    for x, y, t in labels:
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" class="endlab">{t}</text>')
    attrs = K.mark_attrs((pctv(M0) + "%", "The game's base case: margin with the full investment", "var(--fg)"))
    out.append(f'<circle cx="{sx(1.0):.1f}" cy="{sy(M0):.1f}" r="6" fill="var(--fg)" class="ring" {attrs}/>')
    out.append(f'<text x="{sx(1.0) + 10:.1f}" y="{sy(M0) + 4:.1f}" class="endlab">{"Base" if narrow else "Base case: " + pctv(M0) + "%"}</text>')
    out.append(f'<text x="{left}" y="14" class="tick">fps margin needed</text>')
    note = "Boeing's share of its fps bill"
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">{esc(note)}</text></svg>')
    return "".join(out)


def thr_table():
    head = ["Round", "Margin needed, full investment", "Investment cut needed, base margin", "Margin needed, Boeing pays 75%",
            "Boeing pays 50%", "Boeing pays nothing"]
    rows = []
    for grp, muted in ((THR, False), (THG, True)):
        for n, r in grp.items():
            lab = str(r["year"]) + (", conservative curve after 2060" if muted else "")
            cells = [rng(r["premium"]["margin"], r["rule"]["margin"]), cut_rng(r["premium"]["cut"], r["rule"]["cut"])]
            cells += [rng(fr(r, "premium", k), fr(r, "rule", k)) for k in (0.75, 0.5, 0.0)]
            if muted:
                lab = f'<span class="muted">{lab}</span>'
                cells = [f'<span class="muted">{c}</span>' for c in cells]
            rows.append([lab] + cells)
    return K.table(head, rows, num_cols=(1, 2, 3, 4, 5))


def moves_table():
    head = ["Round"] + [NAME[s] for s in SIDES]
    rows = [[str(r["year"])] + [move_txt(r["orders"][s]) for s in SIDES] for r in P["rounds"]]
    return K.table(head, rows).replace("<table>", '<table class="moves">', 1)


def gap_table():
    head = ["10-year fps at Renton against Do Nothing"] + [str(y) for y in YEARS]
    rows = [["MAX phase-out game"] + [b(v) for v in GAP_P],
            ['<span class="muted">range across the brief\'s columns</span>'] + [f'<span class="muted">{nw(bp(lo))} to {nw(bp(hi))}</span>' for lo, hi in RANGE_P],
            ["Conservative-case game"] + [b(v) for v in GAP_C],
            ['<span class="muted">range across the brief\'s columns</span>'] + [f'<span class="muted">{nw(bp(lo))} to {nw(bp(hi))}</span>' for lo, hi in RANGE_C],
            ["<b>Phase-out game weaker by</b>"] + [f"<b>{b(w, 2, False)}</b>" for w in WIDER]]
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def steps_table():
    head = ["Assumption added", "2030 brief", "Change", "2050 brief", "Change"]
    rows = []
    for i, (x30, x50) in enumerate(zip(S30["steps"], S50["steps"])):
        assert x30["step"] == x50["step"]
        rows.append([esc(x30["step"]), b(x30["item"]), "" if i == 0 else b(CH30[i]), b(x50["item"]), "" if i == 0 else b(CH50[i])])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def tail_table():
    head = ["Demand after 2060"] + [str(y) for y in YEARS]
    rows = [[esc(lab)] + [b(tail_real(y, k)) for y in YEARS] for k, lab in TAILS]
    rows.append(['<span class="muted">Best fps launch of any plan, the CEO\'s weighted column, best of the three curves</span>']
                + [f'<span class="muted">{b(BEST[y][0])}</span>' for y in YEARS])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def market_table():
    head = ["737/A320-class aircraft", nw("2026-44") + ", this game", nw("2026-44") + ", conservative", nw("2045-60") + ", this game", nw("2045-60") + ", conservative"]
    rows = []
    for k, lab in (("boeing", "Boeing 737 MAX delivered"), ("airbus", "Airbus delivered"), ("comac", "COMAC delivered"),
                   ("entrant", "New entrant delivered"), ("lost", "Customers lost (gave up waiting)")):
        rows.append([lab, n0(SUM(MP, k, 2026, 2044)), n0(SUM(MC, k, 2026, 2044)), n0(SUM(MP, k, 2045, 2060)), n0(SUM(MC, k, 2045, 2060))])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def signed(v):
    if abs(v) < 0.5:
        return "0"
    return ("+" if v > 0 else K.MINUS) + n0(abs(v))


def who_table():
    head = ["Over 2045-60, aircraft", "Boeing 737 MAX", "Airbus", "COMAC", "New entrant", "Customers lost"]
    rows = [[lab] + [signed(WP[key][k]) for k in ("boeing", "airbus", "comac", "entrant", "lost")]
            for key, lab in (("effect_of_phase_out", "The MAX phase-out"), ("effect_of_comac", "COMAC selling first"))]
    return K.table(head, rows, num_cols=(1, 2, 3, 4, 5))


def value_table():
    head = ["Company", "MAX phase-out game", "Conservative-case game"]
    rows = [[NAME[s], b(P["final_value"][s]), b(C["final_value"][s])] for s in SIDES]
    return K.table(head, rows, num_cols=(1, 2))


CSS_EXTRA = """
:root { --comac: #8a5cc4; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --comac: #9b6fd6; } }
:root[data-theme="dark"] { --comac: #9b6fd6; }
ul.cav li, footer { overflow-wrap: anywhere; }
.scroll { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.scroll > table { background: transparent; }
.legend .dash { display: inline-block; width: 18px; height: 0; border-top: 2px dashed var(--muted); vertical-align: middle; margin-right: 6px; }
@media (max-width: 760px) {
  .moves thead { display: none; }
  .moves, .moves tbody, .moves tr, .moves th, .moves td { display: block; width: auto; }
  .moves tr { border-bottom: 1px solid var(--line); padding: 8px 0; }
  .moves tbody th { min-width: 0; font-weight: 600; border: 0; }
  .moves td { border: 0; padding: 2px 0; }
  .moves td::before { display: block; font: 600 11px var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
  .moves td:nth-of-type(1)::before { content: "Boeing"; } .moves td:nth-of-type(2)::before { content: "Airbus"; }
  .moves td:nth-of-type(3)::before { content: "CFM/GE"; } .moves td:nth-of-type(4)::before { content: "Pratt & Whitney"; }
  .moves td:nth-of-type(5)::before { content: "Rolls-Royce"; }
}
.legend .solid { display: inline-block; width: 18px; height: 0; border-top: 2px solid var(--s1); vertical-align: middle; margin-right: 6px; }
"""


def build(out_path):
    tp = OPT["third_party"]
    tiles = [("Outcome", "Same orders, no fps", "All five companies' final orders match the conservative-case game, round by round. Boeing held the fps in all four rounds."),
             ("10-year fps against Do Nothing, 2050", bp(GAP_P[-1]), f"at Renton, against {b(GAP_C[-1])} in the conservative-case game. The Board needs more than +$1B."),
             ("737 MAX delivered 2045-60", n0(B45P), f"against {n0(B45C)} in the conservative-case game. COMAC delivers {n0(CO45)} and the new entrant {n0(EN45)} in those years."),
             ("Board's +$1B test", "Not met", f"in any round, under all three demand curves tested after 2060 (the highest rising to {n0(_gtop)} a year). The closest any fps launch comes is {b(BEST_ANY[0])} (2050).")]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{d}</div></div>' for k, v, d in tiles) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MAX Phase-out Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · MAX phase-out world · BOEING PROPRIETARY</p>
<h1>The MAX phase-out game: same orders, no fps, and a weaker fps case in every round</h1>
<p class="lede">The game replayed in the world you set in the Do Nothing tuner. It differs from the conservative-case game (the earlier play of the same game on the conservative demand curve) in five ways.
<b>Demand</b> follows the conservative curve to 2037 and your Single-Aisle Replacement Story page from 2038. That page counts replacement of today's fleet plus as much again for growth.
Over 2026-60 the two curves total about the same ({n0(DEM_P)} against {n0(DEM_C)} aircraft). Yours dips where they join in 2038 ({n0(MP[2038]["demand"])} against {n0(MC[2038]["demand"])}), and it falls away in the late 2050s and after 2060.
<b>The 737 MAX</b> phases out from {OPT["max_phaseout"]["start"]}, with none built from {OPT["max_phaseout"]["gone"]}.
<b>Airbus</b> adds extra lines from {OPT["airbus_extra"]["from"]}, up to {OPT["airbus_extra"]["cap"]:.0f} more aircraft a month.
<b>COMAC</b> sells its capacity first, to its own customers: 150 a year in 2035, rising to 250 from 2050.
<b>A new entrant</b> enters service in {tp["entrant"]["eis"]} and sells to customers left waiting: those who cannot get the aircraft they want and do not switch.
Every company played as before, through its Board and ExCo, in the same four rounds: 2030, 2035, 2045 and 2050.</p>
<p class="gloss"><b>How to read the figures.</b> Values are $B, PV at 2026, against the <b>status quo</b>, in which nobody launches anything.
<b>Do Nothing</b> is not the status quo: Boeing launches nothing, but Airbus and the engine makers still move.
Each round Boeing's ExCo gets a <b>brief</b>: a grid that values every Boeing plan against each move Airbus could make that round, one <b>column</b> per move.
Where the page quotes one figure, it uses the column for what Airbus then did. The <b>10-year fps at Renton</b> is the fps on a 10-year development, built at Renton.
The brief counts each programme's sales for 20 years from its entry into service, and Do Nothing's to 2060.
Boeing's Board approves a launch only if it adds more than +$1B in the column its CEO expects, and vetoes any order that could lose more than $1B in any column it thinks plausible (its <b>downside test</b>).</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>What each company did</h2><div class="panel">{moves_table()}
<p class="cap">All five companies' final orders match the conservative-case game, round by round, and Boeing held the fps in all four rounds.
The one difference is how Boeing got there in 2030. The 787 Re-engine scored the same in both games: {b(RE_UP)} against Do Nothing, or {b(RE_DOWN)} if Airbus
re-engines the A350 in the same round. The conservative-case CEO put even odds on that A350 move, which made the Re-engine worth {b(RE30_EVEN)}, inside the $1B margin, and held it back.
This game's CEO took the column where Airbus launches NGSA without re-engining the A350 as the expected one, valued the Re-engine there at {b(RE30_S2)}, and proposed it.
The Board vetoed it on its downside test, because it loses {b(-RE_DOWN, 2, False)} if Airbus does re-engine.
In 2035 this game's CEO adopted the CFO's 30% odds of an A350 Re-engine (the conservative-case CEO used 40%). On that weighting the Re-engine's
expected lead ({b(RE35_W)}) was inside the $1B margin, so the CEO held it back; it would have led by {b(RE35_HOLD)} if Airbus held, as it did. In 2045 and 2050
its lead was inside $1B in every column. Airbus launched NGSA in 2030 on its Alt plan, which keeps the A320 longer. NGSA's engine choice set off Pratt &amp; Whitney's
GTF2 and Rolls-Royce's UltraFan NB launches in 2030, and CFM/GE upgraded the GEnx. In 2035 those two engines folded into the Pratt &amp; Whitney-Rolls-Royce
Joint Venture, and CFM/GE launched its ducted engine and an Embraer partnership.</p></div></section>

<section><h2>Boeing's fps case, round by round</h2><div class="stack">
<div class="panel"><p class="ctitle">The fps case is {bp(min(WIDER), 1, False)}-{bp(max(WIDER), 1, False)} weaker than in the conservative-case game in every round, and never near the Board's +$1B</p>
<div class="legend"><span><i class="solid"></i>MAX phase-out game</span><span><i class="dash"></i>Conservative-case game</span></div>
<div class="cw only-wide">{gap_chart()}</div><div class="cw only-narrow">{gap_chart(True)}</div>
<p class="cap">Each round's brief: the 10-year fps at Renton against Do Nothing, in the column that matches what Airbus then did.
In both games the fps's shortfall against Do Nothing shrinks round by round. The difference between the games does not.</p></div>
<div class="panel">{gap_table()}</div>
<div class="panel"><p class="label">Why the case is weaker: your assumptions switched on one at a time</p>{steps_table()}
<p class="cap"><b>2030:</b> the biggest step is COMAC selling its capacity first ({b(CH30[I_CO])}). Under Do Nothing, in the years the brief counts, COMAC takes {n0(CU_DN["to_2060"])} aircraft
from Boeing: {n0(CU_DN["by_period"][0])} in 2035-39, {n0(CU_DN["by_period"][2])} in 2045-49, and none from 2050, when the shrinking MAX line is sold out anyway.
From the fps plan it takes {n0(CU_F["to_2059"])}: the same {n0(CU_F["by_period"][0])} in 2035-39 and {n0(CU_F["by_period"][2] + CU_F["by_period"][3])} in 2045-59, when an fps would have aircraft to sell.
Measured against its own status quo, Do Nothing loses only {b(-CO_DN, 2, False)} at this step and the fps plan {b(-CO_FPS, 2, False)}.
The phase-out helps the fps case ({b(CH30[I_PH])}). The status quo also loses its MAX, and measured against it the fps plan gains {b(PH_FPS, 2, False)} and Do Nothing only {b(PH_DN, 2, False)}.
<b>2050:</b> the biggest step is the demand curve ({b(CH50[I_DEM])}). The brief counts an fps's sales for 20 years from its entry into service. An fps launched in 2050
enters service in 2060, so its whole case rests on 2060-79, where your page's curve falls away.</p></div>
<div class="panel"><p class="label">Demand after 2060: your table stops there, but the late rounds rest on it</p>{tail_table()}
<p class="cap">The first three rows show the 10-year fps at Renton against Do Nothing, in the column that matches what Airbus did, as in the table above ($B, PV at 2026).
Demand is in 737/A320-class aircraft a year.
The last row takes every fps launch the brief offers, each measured against the same plan with the fps held (the Board's own test). It weights Airbus's options the way
Boeing's CEO weighted them in that round. The best launch is the 10-year at Renton in every round.
Your tuner table runs to 2060. After that the run uses your page's curve, which fades out because it counts only replacement of today's fleet plus as much again for growth.
This does not touch 2030: the brief counts a 2030 fps's sales only to 2059 (it enters service in 2040), and Do Nothing's to 2060.
It matters from 2035, and most in 2045 and 2050. With the conservative curve after 2060, the 2050 fps comes to {b(tail_real(2050, "game"))}, close to the
conservative-case game's {b(GAP_C[-1])}. Boeing's decision does not change under any of these curves: no fps launch reaches +$1B in any round.
The other companies were not replayed under these curves.</p></div>
</div></section>

<section><h2>What would change Boeing's decision</h2><div class="stack">
<div class="panel"><p class="ctitle">Only an early launch can be bought: in 2030 about {pctv(R30["rule"]["margin"], 0)}% fps margin, or {cut_rng(R30["premium"]["cut"], R30["rule"]["cut"])} less investment; from 2045 nothing realistic</p>
<div class="legend"><span><i class="solid"></i>2030</span><span><i class="dash" style="border-top-color:var(--s1)"></i>2035</span><span><i class="solid" style="border-top-color:var(--muted)"></i>2045</span><span><i class="dash"></i>2050</span><span><i class="sq" style="background:var(--fg);border-radius:50%"></i>Base case</span></div>
<div class="cw only-wide">{frontier_chart()}</div><div class="cw only-narrow">{frontier_chart(True)}</div>
<p class="cap">Each line is one round: the fps operating margin needed, for each share of its fps investment that Boeing pays, before an fps launch becomes Boeing's decision
(under the CEO's normal rule; the table below also gives the lower figure if the CEO uses the premium allowance). Above a round's line Boeing launches the fps that round. The game's base case,
{pctv(M0)}% margin with the full investment, sits below every line. 2045 needs more than 100% margin once Boeing pays more than {K.rnd(100 * LAST45, 0):.0f}% of the bill, and 2050 needs
{mtxt(fr(THR[4], "rule", 0.0))} even if Boeing pays nothing.</p></div>
<div class="panel">{thr_table()}
<p class="cap"><b>How the decision is taken.</b> An fps launches only if it is the CEO's pick and the Board approves it. The CEO takes the plan worth most in the column the CEO expects,
and among plans within the CEO's $1B margin of it, the one with less to execute. The Board then judges each order on its own: an fps must add more than +$1B in that column,
lose no more than $1B in any column, and leave the plan's risk case no more than $2B below Do Nothing. A vetoed order reverts to hold, and the CEO cannot add an fps afterwards.
In 2030 the CEO's pick was the 787 Re-engine, worth {b(RE30_S2)} in the CEO's column, so the fps has to beat it by that margin, not just clear the Board's +$1B: the Board's tests alone
would ask {pctv(BOARD_ONLY_30)}% of the 7-year, the CEO's rule asks {pctv(R30["rule"]["margin"])}%. The <b>lower figure</b> in each range is what is needed if the CEO uses the allowance to give up
to $2B of value to pick the fps for its objective (the 50/50 split with Airbus); the <b>higher figure</b> is the CEO's normal rule. Each round is taken alone, from the state it started in.
<b>Which fps.</b> The first plan to cross is the 7-year at Renton in every round of this game: it enters service three years earlier, so each point of its margin is worth more
({b(R30["per_point"][TP7], 2, False)} against {b(R30["per_point"][TP10], 2, False)} a point for the 10-year in 2030). Renton saves new-site capex, and the Board made it conditional on Pope's
readiness result for winding down Renton's MAX lines; at new sites a little more is needed.
<b>Margin</b> is on every fps delivered, the {nw(f"${PRICE:.0f}M")} price held. The base {pctv(M0)}% is {nw(f"${PRICE * M0:.1f}M")} of profit on a {nw(f"${cost(M0):.1f}M")} cost;
{pctv(R30["rule"]["margin"])}% means a {nw(f"${cost(R30['rule']['margin']):.1f}M")} cost, 60% about {nw(f"${cost(0.6):.0f}M")} (about half the base cost), and over 100% a negative cost, which is impossible.
<b>Investment</b> is Boeing's fps bill (10-year {nw(f"${BILL10:.2f}B")}, 7-year {nw(f"${BILL7:.1f}B")}), counted as the brief counts it: at entry into service, with its debt penalty.
The "Boeing pays" columns assume the rest is a grant that takes no share of the profit. A partner that takes the same share of the profit as it pays of the bill does not help:
in 2030 it would need {pctv(P25)}% with a 25% partner and {pctv(P50)}% with a 50/50 partner, against {pctv(R30["rule"]["margin"])}% alone. A budget spent through the development years,
rather than counted at entry into service, would need more margin or a deeper cut than shown.
<b>Why late rounds cannot be bought.</b> A point of margin is worth {b(R30["per_point"][TP10], 2, False)} for the 10-year in 2030 but {b(THR[4]["per_point"][TP10], 2, False)} in 2050: a later fps
sells far fewer aircraft in its 20 counted years, and further in the future; from 2045 mostly after 2060, where your page's demand falls away. With the conservative curve
after 2060 (grey rows) the late rounds need {pctv(min(THG[n]["premium"]["margin"] for n in THG), 0)}-{pctv(max(THG[n]["rule"]["margin"] for n in THG), 0)}% margin, or {K.rnd(100 * min(THG[n]["premium"]["cut"] for n in THG), 0):.0f}-{K.rnd(100 * max(THG[n]["rule"]["cut"] for n in THG), 0):.0f}% less investment.
Every threshold of the normal rule in 2030-45 is re-checked on a re-solved dashboard (every competing plan, every column), and Boeing's stress-case net debt stays at $0 there.</p></div>
</div></section>

<section><h2>The market in the final state</h2><div class="stack">
<div class="panel"><p class="ctitle">The MAX runs down to none by 2060; Airbus delivers most of the market, and COMAC 150-250 a year from 2035</p>
<div class="legend"><span><i class="sq" style="background:var(--s1)"></i>Boeing 737 MAX</span><span><i class="sq" style="background:var(--s2)"></i>Airbus</span><span><i class="sq" style="background:var(--comac)"></i>COMAC</span><span><i class="sq" style="background:var(--s3)"></i>New entrant</span><span><i class="ln" style="background:var(--fg);width:16px;height:2px;display:inline-block;vertical-align:middle"></i> Demand</span></div>
<div class="cw only-wide">{market_chart()}</div><div class="cw only-narrow">{market_chart(True)}</div>
<p class="cap">Over 2045-60 Boeing delivers {n0(B45C - B45P)} fewer 737s than in the conservative-case game, and Airbus {n0(A45C - A45P)} fewer.
COMAC delivers {n0(CO45)} and the new entrant {n0(EN45)}. Those gaps mix all five assumptions, which overlap. The table below takes the two that move the MAX's
customers, inside this world. The phase-out costs Boeing {n0(-EP["boeing"])} aircraft: {n0(EP["airbus"])} of those customers switch to Airbus and {n0(EP["entrant"])} buy from the new entrant.
COMAC sells its {n0(EC["comac"])} first, off the top of each year's demand, so it sells them with or without the phase-out. Without COMAC, Airbus would deliver {n0(-EC["airbus"])} more,
the new entrant {n0(-EC["entrant"])} more and Boeing {n0(-EC["boeing"])} more; that is {n0(WAIT)} more than COMAC's {n0(EC["comac"])}, because without COMAC {n0(WAIT)} customers are still waiting at the end of 2044 and are delivered later.
The final state is not quite your tuner table, because Airbus played its Alt plan (the A320 kept longer). That gives it more capacity in {MORE_CAP[0]}-{str(MORE_CAP[-1])[2:]} than the
base plan your table shows. As a result Boeing delivers fewer 737s than your table in {FEWER_TXT}. In every other year Boeing's deliveries match your table.
In some years the bars rise above that year's demand: customers left unserved in earlier years wait, and a tenth of them give up each year.</p></div>
<div class="panel"><p class="label">The MAX's lost customers go to Airbus and the new entrant; COMAC's sales come mostly out of Airbus's</p>{who_table()}
<p class="cap">The final state of this game with each assumption, against the same state with only that assumption switched off, 2045-60.</p></div>
<div class="panel">{market_table()}</div>
</div></section>

<section><h2>Value at the end of the game</h2><div class="panel">{value_table()}
<p class="cap">What the final state, after all five companies' moves, is worth to each company against the status quo of its own world, PV at 2026. Boeing held everything
in both games, so its figures are what the other companies' moves cost it. The two columns are measured from different starting points, so they should not be subtracted.
Boeing's {b(P["final_value"]["boeing"])} is a smaller loss than its {b(C["final_value"]["boeing"])} mainly because its status quo here also loses the MAX's late sales: that alone is worth
{b(V_PH)} to the comparison, and the other assumptions together {b(V_REST)}. In absolute terms Boeing delivers {n0(B_ALL)} fewer 737s over 2026-60 in this world (the two periods in the table above).</p></div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The world</b> is the settings behind your Do Nothing tuner table (1 Nov 2026), in sd_options_phaseout.json. With Airbus on its base A320 plan the game gives back your table to the aircraft (test_phaseout.py).</li>
<li><b>The phase-out applies to every Boeing plan</b>, not only Do Nothing, because the MAX ages either way. COMAC and the new entrant compete in every plan too.</li>
<li><b>Everything else</b> is the conservative-case game. Firm orders, Boards, ExCos and objectives are the same. So are the market rules: Boeing's share drifts down 1 point a year while NGSA flies alone, Boeing sells to the customers Airbus cannot build for, and Airbus adds 1% capacity a year when it is short.</li>
<li><b>The step tables</b> (steps.py) switch your assumptions on in the order shown. Another order would split the total differently but give the same total. The first and last steps give back each game's own brief, every column, to the cent. Changes are shown as the differences of the rounded figures.</li>
<li><b>The demand curves after 2060</b> (tail.py) re-value every Boeing plan in every column of every round, from the state each round started in. The "as run" curve gives back the run's own briefs to the cent.</li>
<li><b>What would change the decision</b> (thresholds.py) values each fps plan as the brief does and moves only the fps margin and Boeing's bill. The value moves exactly with the margin (fps deliveries, discounted, times price times the margin change), and the bill is the dashboard's own formula, so the thresholds are exact. Each one is re-checked on a re-solved dashboard to within $0.00001B.</li>
<li><b>Source:</b> extract.py, steps.py, tail.py, comac_units.py, who_picks_up.py, thresholds.py and make_phaseout_html.py. The round records are in record/.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_phaseout_html.py from runs dash-2050-phaseout and dash-2050-cons.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_phaseout.html"))
