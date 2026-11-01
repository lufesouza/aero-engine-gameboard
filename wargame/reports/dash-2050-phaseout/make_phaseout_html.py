"""Build dash_2050_phaseout.html: the MAX phase-out game (run dash-2050-phaseout) against the conservative-case game
(dash-2050-cons): the moves, Boeing's fps case round by round and why it moved, how much rests on demand after 2060,
the market in the final state, and each company's value.

Reads data/dash-2050-phaseout.json and data/dash-2050-cons.json (extract.py, one run each), data/steps_2030.json and
data/steps_2050.json (steps.py), data/tail.json (tail.py) and data/comac_units.json (comac_units.py). Every figure on the page comes from those files; the
claims in the copy are asserted against them below.

  python3 make_phaseout_html.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
D = lambda n: json.load(open(os.path.join(HERE, "data", n)))
P, C, S30, S50, T = D("dash-2050-phaseout.json"), D("dash-2050-cons.json"), D("steps_2030.json"), D("steps_2050.json"), D("tail.json")
OPT = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json")))
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
REN = "fps 10-yr at Renton + 787: hold"
DEFAULTS = {"hold", None, "none", "new_site", "base"}
# the column of each round's Boeing brief that matches what Airbus then did
REAL = {2030: "Airbus launches NGSA on the A320 Alt plan", 2035: "Rivals hold", 2045: "Rivals hold", 2050: "Rivals hold"}


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def moves(o):
    return {k: v for k, v in o.items() if v not in DEFAULTS and not (k.endswith("engine_code") and v is None)}


LABEL = {"ngsa": "NGSA", "ngsa_engine_code": "NGSA engine code", "a320_plan": "A320 plan", "genx": "GEnx", "gtf2_solo": "GTF2 Solo",
         "ultrafan_nb_solo": "UltraFan NB Solo", "ducted": "ducted engine", "partner_embraer": "Embraer partnership",
         "jv_with_rr": "Joint Venture with Rolls-Royce", "jv_with_pw": "Joint Venture with Pratt & Whitney", "fps": "fps",
         "re787": "787 Re-engine", "rate_737": "737 rate", "fps_site": "fps site", "rea350": "A350 Re-engine",
         "delay_tactics": "Delay Tactics"}
VAL = {"launch": "launch", "launch_if_selected": "launch if selected", "alt": "Alt (A320 kept longer)", "upgrade_genx9": "upgrade",
       "commit": "commit", "launch_10yr": "launch, 10-year", "launch_7yr": "launch, 7-year"}


def move_txt(o):
    m = moves(o)
    if not m:
        return '<span class="muted">holds everything</span>'
    return "; ".join(f"{LABEL.get(k, k)}: {VAL.get(v, v)}" for k, v in m.items())


# ─────────────────────────────── facts (asserted) ───────────────────────────────
YEARS = [r["year"] for r in P["rounds"]]
SAME = [[moves(P["rounds"][i]["orders"][s]) == moves(C["rounds"][i]["orders"][s]) for s in SIDES] for i in range(4)]
ALL_SAME = all(all(r) for r in SAME)
LAUNCHED = any(P["rounds"][i]["orders"]["boeing"].get("fps") not in ("hold", None) for i in range(4))
assert ALL_SAME and not LAUNCHED   # the copy says so


def real_col(g, i):
    cols = g["rounds"][i]["columns"]
    return g["rounds"][i]["fps_vs_dn"][REN][cols.index(REAL[YEARS[i]])]


GAP_P = [real_col(P, i) for i in range(4)]
GAP_C = [real_col(C, i) for i in range(4)]
RANGE_P = [(min(P["rounds"][i]["fps_vs_dn"][REN]), max(P["rounds"][i]["fps_vs_dn"][REN])) for i in range(4)]
RANGE_C = [(min(C["rounds"][i]["fps_vs_dn"][REN]), max(C["rounds"][i]["fps_vs_dn"][REN])) for i in range(4)]
WIDER = [c - p for p, c in zip(GAP_P, GAP_C)]
assert all(0.9 < w < 1.55 for w in WIDER), WIDER                        # the title quotes min-max rounded to 0.1
assert all(GAP_P[i] < GAP_P[i + 1] for i in range(3)) and all(GAP_C[i] < GAP_C[i + 1] for i in range(3))   # narrows
# Airbus did what the column says
ab = [P["rounds"][i]["orders"]["airbus"] for i in range(4)]
assert ab[0]["ngsa"] == "launch" and ab[0]["a320_plan"] == "alt" and all(a["ngsa"] == "hold" and a["rea350"] == "hold"
                                                                         and a["delay_tactics"] == "none" and a["a320_plan"] == "alt" for a in ab[1:])
for st in (S30, S50):   # the bridges add up and start/end on each game's own grid
    assert abs(sum(x["change"] for x in st["steps"][1:]) - (st["steps"][-1]["item"] - st["steps"][0]["item"])) < 1e-9
assert abs(S30["steps"][0]["item"] - GAP_C[0]) < 1e-9 and abs(S30["steps"][-1]["item"] - GAP_P[0]) < 1e-9
assert abs(S50["steps"][0]["item"] - GAP_C[3]) < 1e-9 and abs(S50["steps"][-1]["item"] - GAP_P[3]) < 1e-9
CH30 = {x["step"]: x["change"] for x in S30["steps"]}
CH50 = {x["step"]: x["change"] for x in S50["steps"]}
K_DEM, K_PH, K_XA, K_CO, K_EN = (x["step"] for x in S30["steps"][1:])
assert min(CH30.values()) == CH30[K_CO] and min(CH50.values()) == CH50[K_DEM]   # COMAC drives 2030; demand drives 2050
# COMAC hurts the fps far more than Do Nothing (Do Nothing's own move at that step, realised column)
DN_CO = S30["steps"][4]["dn_vs_sq"][S30["columns"].index(REAL[2030])] - S30["steps"][3]["dn_vs_sq"][S30["columns"].index(REAL[2030])]
assert abs(DN_CO) < 0.25 * abs(CH30[K_CO])
# demand after 2060
TR = {r["year"]: r for r in T["rounds"]}
TAILS = [("as run", "Your page's curve after 2060 (as run: 1,166 a year in 2060, 320 in 2072, 78 in 2080)"),
         ("held", "Held at the 2060 level after 2060"),
         ("game", "The conservative game's curve after 2060 (rising to 2,400)")]


def tail_real(year, tname):
    t = TR[year]["tails"][tname]
    return t["items"][REN][t["columns"].index(REAL[year])]


assert all(abs(tail_real(y, "as run") - GAP_P[i]) < 1e-9 for i, y in enumerate(YEARS))
assert all(abs(tail_real(2030, k) - GAP_P[0]) < 1e-9 for k, _ in TAILS)          # no effect in 2030
assert not any(TR[y]["tails"][k]["any_fps_passes_business_case"] for y in YEARS for k, _ in TAILS)
BEST_ANY = max(TR[y]["tails"][k]["best_expected"] for y in YEARS for k, _ in TAILS)
assert BEST_ANY < 0
MP = {x["year"]: x for x in P["market"]}
MC = {x["year"]: x for x in C["market"]}
SUM = lambda m, k, a, z: sum(m[y][k] or 0.0 for y in range(a, z + 1))
B45P, B45C = SUM(MP, "boeing", 2045, 2060), SUM(MC, "boeing", 2045, 2060)
A45P, A45C = SUM(MP, "airbus", 2045, 2060), SUM(MC, "airbus", 2045, 2060)
CO45, EN45 = SUM(MP, "comac", 2045, 2060), SUM(MP, "entrant", 2045, 2060)
assert A45P < A45C and CO45 + EN45 > B45C - B45P                                 # COMAC and the entrant, not Airbus
# the user's tuner table (Do Nothing, Airbus launching NGSA on its base plan), from test_phaseout.py
_src = open(os.path.join(HERE, "..", "..", "dashgame", "test_phaseout.py")).read()
_tab = re.search(r'TABLE = """(.*?)"""', _src, re.S).group(1).replace("\n", "")
TAB = {int(t[0]): dict(zip(("demand", "cap_max", "boeing", "cap_airbus", "airbus", "comac", "entrant", "lost"), map(float, t[1:])))
       for t in (line.split() for line in _tab.split("|"))}
assert sorted(TAB) == list(range(2026, 2061))
FEWER = [y for y in range(2026, 2061) if MP[y]["boeing"] < TAB[y]["boeing"] - 5]
MORE_CAP = [y for y in range(2026, 2061) if MP[y]["cap_airbus"] > TAB[y]["cap_airbus"] + 5]
assert FEWER == [2037, 2038, 2044, 2045], FEWER
FEWER_TXT = ", ".join(f"{y} ({n0(MP[y]['boeing'])} against {n0(TAB[y]['boeing'])})" for y in FEWER[:-1]) + f" and {FEWER[-1]} ({n0(MP[FEWER[-1]]['boeing'])} against {n0(TAB[FEWER[-1]]['boeing'])})"
assert MORE_CAP == list(range(2037, 2045)), MORE_CAP
CU = D("comac_units.json")
CU_DN, CU_F = CU["plans"]["fps: hold + 787: hold"], CU["plans"][REN]
assert CU["column"] == REAL[2030] and CU_F["total"] > 4 * CU_DN["total"]
assert sum(CU_DN["by_period"][3:]) < 0.5 and CU_F["by_period"][2] + CU_F["by_period"][3] > 0.7 * CU_F["total"]


# ─────────────────────────────── charts and tables ───────────────────────────────
def gap_chart():
    w, h, left, right, top, bot = 760, 300, 64, 196, 24, 44
    lo, hi = -7.0, 1.5
    pad = 30
    sx = lambda i: left + pad + i / 3 * (w - left - right - pad)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "Boeing's 10-year fps at Renton against Do Nothing, by round, in both games")]
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{bp(v, 0, False)}</text>')
        v += 1.0
    out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" class="zero"/>')
    out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(1):.1f}" y2="{sy(1):.1f}" class="ref"/><text x="{left + 6}" y="{sy(1) - 6:.1f}" class="reflab">The Board needs more than +$1B</text>')
    for i, y in enumerate(YEARS):
        out.append(f'<text x="{sx(i):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    ends = []
    for vals, var, lab in ((GAP_C, "s3", "Conservative-case game"), (GAP_P, "s1", "MAX phase-out game")):
        d = "M" + " L".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2"/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="5" fill="var(--{var})" class="ring" {K.mark_attrs((bp(v), f"{lab}, {YEARS[i]} brief", f"var(--{var})"))}/>')
        ends.append((sy(vals[-1]), lab, vals[-1]))
    for yy, lab, v in ends:
        out.append(f'<text x="{w - right + 10}" y="{yy + 4:.1f}" class="endlab">{esc(lab.replace("-case game", "").replace(" game", ""))} {bp(v)}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">The brief column that matches what Airbus then did; $B PV at 2026</text></svg>')
    return "".join(out)


def market_chart():
    w, h, left, right, top, bot = 760, 330, 54, 16, 20, 44
    ys = list(range(2026, 2061))
    top_v = max(max(MP[y]["demand"] or 0, MP[y]["boeing"] + MP[y]["airbus"] + MP[y]["comac"] + MP[y]["entrant"]) for y in ys)
    hi = (int(top_v / 500) + 1) * 500
    bw = (w - left - right) / len(ys)
    sx = lambda y: left + (y - ys[0] + 0.5) * bw
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Aircraft delivered each year by maker, MAX phase-out game, final state")]
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
            gap = 1.0 if j else 0.0                  # 2px surface gap between stacked segments
            if j == len(segs) - 1:
                out.append(f'<path d="{K.bar_path(sx(y) - bw * 0.38, bw * 0.76, y0 - gap, y1)}" fill="var(--{var})"/>')
            else:
                out.append(f'<rect x="{sx(y) - bw * 0.38:.1f}" width="{bw * 0.76:.1f}" y="{y1 + 1:.1f}" height="{max(0.0, y0 - y1 - 1 - gap):.1f}" fill="var(--{var})"/>')
            acc += val
        out.append(f'<rect x="{sx(y) - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" '
                   + K.mark_attrs((str(y), "", None), (n0(m["boeing"]), "Boeing 737", "var(--s1)"), (n0(m["airbus"]), "Airbus", "var(--s2)"),
                                  (n0(m["comac"]), "COMAC", "var(--comac)"), (n0(m["entrant"]), "New entrant", "var(--s3)"),
                                  (n0(m["lost"] or 0), "Customers lost", None), (n0(m["demand"] or 0), "Demand", None)) + "/>")
    d = "M" + " L".join(f"{sx(y):.1f},{sy(MP[y]['demand'] or 0):.1f}" for y in ys)
    out.append(f'<path d="{d}" fill="none" stroke="var(--fg)" stroke-width="2" pointer-events="none"/>')
    for y in ys:
        if y % 5 == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">737/A320-class aircraft delivered a year, final state of the MAX phase-out game</text></svg>')
    return "".join(out)


def moves_table():
    head = ["Round"] + [NAME[s] for s in SIDES]
    rows = [[str(r["year"])] + [move_txt(r["orders"][s]) for s in SIDES] for r in P["rounds"]]
    return K.table(head, rows)


def gap_table():
    head = ["10-year fps at Renton against Do Nothing"] + [str(y) for y in YEARS]
    rows = [["MAX phase-out game"] + [b(v) for v in GAP_P],
            ['<span class="muted">range across the brief\'s columns</span>'] + [f'<span class="muted">{bp(lo)} to {bp(hi)}</span>' for lo, hi in RANGE_P],
            ["Conservative-case game"] + [b(v) for v in GAP_C],
            ['<span class="muted">range across the brief\'s columns</span>'] + [f'<span class="muted">{bp(lo)} to {bp(hi)}</span>' for lo, hi in RANGE_C],
            ["<b>Weaker by</b>"] + [f"<b>{b(w, 2, False)}</b>" for w in WIDER]]
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def steps_table():
    head = ["Assumption added", "2030 brief", "Change", "2050 brief", "Change"]
    rows = []
    for i, (x30, x50) in enumerate(zip(S30["steps"], S50["steps"])):
        assert x30["step"] == x50["step"]
        rows.append([esc(x30["step"]), b(x30["item"]), "" if i == 0 else b(x30["change"]), b(x50["item"]), "" if i == 0 else b(x50["change"])])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def tail_table():
    head = ["Demand after 2060"] + [str(y) for y in YEARS]
    rows = [[esc(lab)] + [b(tail_real(y, k)) for y in YEARS] for k, lab in TAILS]
    rows.append(['<span class="muted">Best fps plan in the CEO\'s expected column, any tail</span>']
                + [f'<span class="muted">{bp(max(TR[y]["tails"][k]["best_expected"] for k, _ in TAILS))}</span>' for y in YEARS])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def market_table():
    head = ["Aircraft delivered", "2026-44, this game", "2026-44, conservative", "2045-60, this game", "2045-60, conservative"]
    rows = []
    for k, lab in (("boeing", "Boeing 737"), ("airbus", "Airbus"), ("comac", "COMAC"), ("entrant", "New entrant"), ("lost", "Customers lost")):
        rows.append([lab, n0(SUM(MP, k, 2026, 2044)), n0(SUM(MC, k, 2026, 2044)), n0(SUM(MP, k, 2045, 2060)), n0(SUM(MC, k, 2045, 2060))])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def value_table():
    head = ["Company", "MAX phase-out game", "Conservative-case game", "Difference"]
    rows = [[NAME[s], b(P["final_value"][s]), b(C["final_value"][s]), b(P["final_value"][s] - C["final_value"][s])] for s in SIDES]
    return K.table(head, rows, num_cols=(1, 2, 3))


CSS_EXTRA = """
:root { --comac: #8a5cc4; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --comac: #9b6fd6; } }
:root[data-theme="dark"] { --comac: #9b6fd6; }
ul.cav li, footer { overflow-wrap: anywhere; }
.chart .zero { stroke: var(--line); stroke-width: 1; }
"""


def build(out_path):
    tp = OPT["third_party"]
    t50 = TR[2050]["tails"]
    tiles = [("Outcome", "Same moves, no fps", "All five companies made the same orders as in the conservative-case game, round by round. Boeing held the fps in all four rounds."),
             ("fps against Do Nothing, 2050", bp(GAP_P[-1]), f"against {bp(GAP_C[-1])} in the conservative-case game. The Board needs more than +$1B."),
             ("737s sold 2045-60", n0(B45P), f"against {n0(B45C)} in the conservative-case game. COMAC sells {n0(CO45)} and the entrant {n0(EN45)} in those years."),
             ("Boeing's value", bp(P["final_value"]["boeing"]), f"against {bp(C['final_value']['boeing'])} in the conservative-case game: Do Nothing against the status quo of its own world, PV at 2026.")]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MAX Phase-out Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun (dash-2050-phaseout) · BOEING PROPRIETARY</p>
<h1>The MAX phase-out game: same moves, no fps, and a weaker fps case in every round</h1>
<p class="lede">The game replayed in the world you set in the Do Nothing tuner. That world has your page's demand. The 737 MAX
phases out from {OPT["max_phaseout"]["start"]}, with none built from {OPT["max_phaseout"]["gone"]}. Airbus adds extra lines from {OPT["airbus_extra"]["from"]}, up to {OPT["airbus_extra"]["cap"]:.0f} more a month.
COMAC sells its capacity to its own customers first: 150 a year in 2035, rising to 250 from 2050. A new entrant enters service in {tp["entrant"]["eis"]}
and serves the customers nobody else can. Every company played as before, through its Board and ExCo, round by round. The page compares
this game with the conservative-case game.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>What each company did</h2><div class="panel">{moves_table()}
<p class="cap">Every order matches the conservative-case game, round by round. Boeing held the fps in all four rounds.
In 2030 its Board vetoed the 787 Re-engine on its downside test. In 2035, 2045 and 2050 the CEO held the Re-engine back,
because its lead was inside the $1B margin. Airbus launched NGSA in 2030 on its Alt plan, which keeps the A320 longer.
In 2035 CFM launched its ducted engine and an Embraer partnership, and Pratt &amp; Whitney and Rolls-Royce committed to their Joint Venture.</p></div></section>

<section><h2>Boeing's fps case, round by round</h2><div class="stack">
<div class="panel"><p class="ctitle">The fps case is {bp(min(WIDER), 1, False)}-{bp(max(WIDER), 1, False)} weaker than in the conservative-case game in every round, and never near the Board's +$1B</p><div class="cw">{gap_chart()}</div>
<p class="cap">Each round's brief: the 10-year fps at Renton against Do Nothing, in the column that matches what Airbus then did.
In both games the gap narrows round by round.</p></div>
<div class="panel">{gap_table()}</div>
<div class="panel"><p class="label">Why the case is weaker: your assumptions switched on one at a time</p>{steps_table()}
<p class="cap"><b>2030:</b> the biggest step is COMAC selling its capacity first ({bp(CH30[K_CO])}). It takes {n0(CU_DN["total"])} aircraft
from Boeing under Do Nothing, all before 2050, but {n0(CU_F["total"])} from the fps plan, {n0(CU_F["by_period"][2] + CU_F["by_period"][3])} of them in 2045-59.
By then the MAX is phasing out, so under Do Nothing Boeing has no aircraft for those customers anyway; with an fps it would.
Do Nothing's own value moves only {bp(DN_CO)} at this step. The phase-out itself helps the fps ({bp(CH30[K_PH])}), because it makes Do Nothing worse.
<b>2050:</b> the biggest step is the demand curve ({bp(CH50[K_DEM])}). An fps launched in 2050 enters service around 2060 and sells after 2060,
where your page's curve falls away.</p></div>
<div class="panel"><p class="label">Demand after 2060: your table stops there, but the late rounds look beyond it</p>{tail_table()}
<p class="cap">Your tuner table runs to 2060. After 2060 the run uses your page's curve, which counts replacement of today's fleet plus
as much again for growth, so it fades out. This does not touch 2030: an fps launched then sells before 2060. It matters from 2035, and most in 2045 and 2050.
With the conservative curve after 2060, the 2050 gap is {bp(tail_real(2050, "game"))}, close to the conservative-case game's {bp(GAP_C[-1])}.
Boeing's decision does not change under any of these tails. In no round does any fps plan reach +$1B in the CEO's expected column:
the best, in 2050 with the conservative curve, is {bp(BEST_ANY)}. The other companies were not replayed under these tails.</p></div>
</div></section>

<section><h2>The market in the final state</h2><div class="stack">
<div class="panel"><p class="ctitle">COMAC and the entrant, not Airbus, pick up the customers the MAX loses</p>
<div class="legend"><span><i class="sq" style="background:var(--s1)"></i>Boeing 737 MAX</span><span><i class="sq" style="background:var(--s2)"></i>Airbus</span><span><i class="sq" style="background:var(--comac)"></i>COMAC</span><span><i class="sq" style="background:var(--s3)"></i>New entrant</span><span><i class="ln" style="background:var(--fg);width:16px;height:2px;display:inline-block;vertical-align:middle"></i> Demand</span></div>
<div class="cw">{market_chart()}</div>
<p class="cap">Over 2045-60 Boeing sells {n0(B45C - B45P)} fewer 737s than in the conservative-case game, and Airbus sells {n0(A45C - A45P)} fewer.
COMAC sells {n0(CO45)} and the entrant {n0(EN45)}. The final state is not quite your tuner table, because Airbus played its Alt plan
(the A320 kept longer). That gives it more capacity in {MORE_CAP[0]}-{str(MORE_CAP[-1])[2:]} than the base plan your table shows, so Boeing sells fewer 737s
than your table in {FEWER_TXT}. In every other year Boeing's deliveries match your table. In some years the bars rise above
that year's demand: customers left unserved in earlier years wait, and a tenth of them drop out each year.</p></div>
<div class="panel">{market_table()}</div>
</div></section>

<section><h2>Value at the end of the game</h2><div class="panel">{value_table()}
<p class="cap">Each company's change against the status quo, PV at 2026. Each game's status quo runs that game's own world, so
these values compare plans within a world, not one world with the other.</p></div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The world</b> is sd_options_phaseout.json, the settings behind your Do Nothing tuner table (1 Nov 2026). The engine gives back that table to the aircraft (test_phaseout.py).</li>
<li><b>The phase-out applies to every Boeing plan</b>, not only Do Nothing, because the MAX ages either way. COMAC and the entrant compete in every plan too.</li>
<li><b>Everything else</b> is the conservative-case game: firm orders inside demand, Boeing losing 1 point a year while NGSA flies alone, Boeing taking Airbus's slack, Airbus adding 1% capacity a year when short, and the same Boards, ExCos and objectives.</li>
<li><b>The bridges</b> (steps.py) switch your assumptions on in the order shown. A different order would split the total differently, but the total is the same. Both the first and the last step give back each game's own brief, every column, to the cent.</li>
<li><b>The demand tails</b> (tail.py) re-value every Boeing plan in every column of every round, from the state each round started in. The "as run" tail gives back the run's own briefs to the cent.</li>
<li><b>Source:</b> extract.py, steps.py, tail.py, comac_units.py and make_phaseout_html.py. The round records are in record/.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_phaseout_html.py from runs dash-2050-phaseout and dash-2050-cons.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_phaseout.html"))
