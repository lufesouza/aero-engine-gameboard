"""Build dash_2050_phaseout.html: the MAX phase-out game (run dash-2050-phaseout) against the conservative-case game
(dash-2050-cons): the moves, the value, Boeing's fps case round by round, and the market in the final state.

Reads data/dash-2050-phaseout.json and data/dash-2050-cons.json (extract.py, one run each) and the step-by-step split of
the 2030 fps case (data/steps_2030.json, steps.py).

  python3 make_phaseout_html.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
P = json.load(open(os.path.join(HERE, "data", "dash-2050-phaseout.json")))
C = json.load(open(os.path.join(HERE, "data", "dash-2050-cons.json")))
ST = json.load(open(os.path.join(HERE, "data", "steps_2030.json")))
OPT = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json")))
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
REN = "fps 10-yr at Renton + 787: hold"
DEFAULTS = {"hold", None, "none", "new_site", "base"}


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def bp(v, dp=2, sign=True):
    import re
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def moves(o):
    return {k: v for k, v in o.items() if v not in DEFAULTS and not (k.endswith("engine_code") and v is None)}


LABEL = {"ngsa": "NGSA", "ngsa_engine_code": "NGSA engine code", "a320_plan": "A320 plan", "genx": "GEnx", "gtf2_solo": "GTF2 Solo",
         "ultrafan_nb_solo": "UltraFan NB Solo", "ducted": "ducted engine", "partner_embraer": "Embraer partnership",
         "jv_with_rr": "Joint Venture with RR", "jv_with_pw": "Joint Venture with P&W", "fps": "fps", "re787": "787 Re-engine",
         "rate_737": "737 rate", "fps_site": "fps site", "rea350": "A350 Re-engine", "delay_tactics": "Delay Tactics"}
VAL = {"launch": "launch", "launch_if_selected": "launch if selected", "alt": "Alt (A320 kept longer)", "upgrade_genx9": "upgrade",
       "commit": "commit", "launch_10yr": "launch, 10-year", "launch_7yr": "launch, 7-year"}


def move_txt(o):
    m = moves(o)
    if not m:
        return '<span class="muted">holds everything</span>'
    return "; ".join(f"{LABEL.get(k, k)}: {VAL.get(v, v)}" for k, v in m.items())


# ─────────────────────────────── facts (asserted) ───────────────────────────────
SAME = [[moves(P["rounds"][i]["orders"][s]) == moves(C["rounds"][i]["orders"][s]) for s in SIDES] for i in range(4)]
ALL_SAME = all(all(r) for r in SAME)
LAUNCHED = any(P["rounds"][i]["orders"]["boeing"].get("fps") not in ("hold", None) for i in range(4))
GAP_P = [min(P["rounds"][i]["fps_vs_dn"][REN]) for i in range(4)]
GAP_PX = [max(P["rounds"][i]["fps_vs_dn"][REN]) for i in range(4)]
GAP_C = [min(C["rounds"][i]["fps_vs_dn"][REN]) for i in range(4)]
GAP_CX = [max(C["rounds"][i]["fps_vs_dn"][REN]) for i in range(4)]
YEARS = [r["year"] for r in P["rounds"]]
MP = {x["year"]: x for x in P["market"]}
MC = {x["year"]: x for x in C["market"]}
SUM = lambda m, k, a, z: sum(m[y][k] or 0.0 for y in range(a, z + 1))
assert abs(sum(ST["steps"][i]["change"] for i in range(1, len(ST["steps"]))) - (ST["steps"][-1]["item"] - ST["steps"][0]["item"])) < 1e-9


def gap_chart():
    w, h, left, right, top, bot = 760, 300, 64, 150, 24, 40
    lo, hi = -7.0, 1.5
    sx = lambda i: left + i / 3 * (w - left - right)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Boeing fps at Renton against Do Nothing by round, both games">']
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{bp(v, 0)}</text>')
        v += 1.0
    out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(1):.1f}" y2="{sy(1):.1f}" class="ref"/><text x="{left + 6}" y="{sy(1) - 6:.1f}" class="reflab">Board\'s +$1B</text>')
    for i, y in enumerate(YEARS):
        out.append(f'<text x="{sx(i):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    for vals, var, lab in ((GAP_C, "s3", "Conservative-case game"), (GAP_P, "s1", "MAX phase-out game")):
        d = "M" + " L".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2.4"/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="5" fill="var(--{var})" class="ring" {K.mark_attrs((bp(v), f"{lab}, {YEARS[i]} brief (worst column)", f"var(--{var})"))}/>')
        out.append(f'<text x="{w - right + 8}" y="{sy(vals[-1]) + 4:.1f}" class="endlab">{esc(lab.split(" game")[0])} {bp(vals[-1])}</text>')
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">10-year fps at Renton against Do Nothing, worst column of each round\'s brief, $B PV at 2026</text></svg>')
    return "".join(out)


def market_chart():
    w, h, left, right, top, bot = 760, 330, 54, 16, 20, 40
    ys = list(range(2026, 2061))
    top_v = max(max(MP[y]["demand"] or 0, MP[y]["boeing"] + MP[y]["airbus"] + MP[y]["comac"] + MP[y]["entrant"]) for y in ys)
    hi = (int(top_v / 500) + 1) * 500
    bw = (w - left - right) / len(ys)
    sx = lambda y: left + (y - ys[0] + 0.5) * bw
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Deliveries by maker each year, MAX phase-out game, final state">']
    v = 0
    while v <= hi:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{n0(v)}</text>')
        v += 500
    for y in ys:
        acc = 0.0
        m = MP[y]
        for k, var in (("boeing", "s1"), ("airbus", "s2"), ("comac", "comac"), ("entrant", "s3")):
            val = m[k] or 0.0
            if val <= 0.5:
                continue
            out.append(f'<rect x="{sx(y) - bw * 0.4:.1f}" width="{bw * 0.8:.1f}" y="{sy(acc + val):.1f}" height="{sy(acc) - sy(acc + val):.1f}" fill="var(--{var})"/>')
            acc += val
        out.append(f'<rect x="{sx(y) - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" '
                   + K.mark_attrs((str(y), "", None), (n0(m["boeing"]), "Boeing 737", "var(--s1)"), (n0(m["airbus"]), "Airbus", "var(--s2)"),
                                  (n0(m["comac"]), "COMAC", "var(--comac)"), (n0(m["entrant"]), "New entrant", "var(--s3)"),
                                  (n0(m["demand"] or 0), "Demand", None)) + "/>")
    d = "M" + " L".join(f"{sx(y):.1f},{sy(MP[y]['demand'] or 0):.1f}" for y in ys)
    out.append(f'<path d="{d}" fill="none" stroke="var(--fg)" stroke-width="1.6"/>')
    for y in ys:
        if y % 5 == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">Aircraft delivered a year (737/A320 class), final state of the MAX phase-out game</text></svg>')
    return "".join(out)


def moves_table():
    head = ["Round"] + [NAME[s] for s in SIDES]
    rows = []
    for i, r in enumerate(P["rounds"]):
        rows.append([str(r["year"])] + [move_txt(r["orders"][s]) + ("" if SAME[i][j] else ' <span class="muted small">(differs from the conservative-case game)</span>')
                                         for j, s in enumerate(SIDES)])
    return K.table(head, rows)


def value_table():
    head = ["Company", "MAX phase-out game", "Conservative-case game", "Difference"]
    rows = [[NAME[s], b(P["final_value"][s]), b(C["final_value"][s]), b(P["final_value"][s] - C["final_value"][s])] for s in SIDES]
    return K.table(head, rows, num_cols=(1, 2, 3))


def gap_table():
    head = ["Round brief"] + [str(y) for y in YEARS]
    rows = [["MAX phase-out game"] + [f"{bp(GAP_P[i])} to {bp(GAP_PX[i])}" for i in range(4)],
            ["Conservative-case game"] + [f"{bp(GAP_C[i])} to {bp(GAP_CX[i])}" for i in range(4)]]
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def steps_table():
    head = ["Step (Boeing's 2030 brief, expected case)", "fps against Do Nothing", "Change"]
    rows = [[esc(s["step"]), b(s["item"]), "" if i == 0 else b(s["change"])] for i, s in enumerate(ST["steps"])]
    return K.table(head, rows, num_cols=(1, 2))


def market_table():
    head = ["Aircraft", "2026-44", "2045-60", "Conservative-case game, 2045-60"]
    rows = []
    for k, lab in (("boeing", "Boeing 737"), ("airbus", "Airbus"), ("comac", "COMAC"), ("entrant", "New entrant"), ("lost", "Customers lost")):
        rows.append([lab, n0(SUM(MP, k, 2026, 2044)), n0(SUM(MP, k, 2045, 2060)), n0(SUM(MC, k, 2045, 2060))])
    return K.table(head, rows, num_cols=(1, 2, 3))


CSS_EXTRA = """
:root { --comac: #c03b5b; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --comac: #d0506f; } }
:root[data-theme="dark"] { --comac: #d0506f; }
ul.cav li, footer { overflow-wrap: anywhere; }
"""


def build(out_path):
    tp = OPT["third_party"]
    b45, b60 = SUM(MP, "boeing", 2045, 2060), SUM(MC, "boeing", 2045, 2060)
    tiles = [("Outcome", "Same moves, no fps" if (ALL_SAME and not LAUNCHED) else ("No fps" if not LAUNCHED else "fps launched"),
              "Every company made the same orders as in the conservative-case game, round by round." if ALL_SAME else "Some orders differ from the conservative-case game (see the table)."),
             ("Boeing's value", bp(P["final_value"]["boeing"]), f"against {bp(C['final_value']['boeing'])} in the conservative-case game (change against the status quo, PV at 2026)."),
             ("fps gap in 2050", bp(GAP_P[-1]), f"10-year fps at Renton against Do Nothing, worst column; {bp(GAP_C[-1])} in the conservative-case game. The Board needs +$1B."),
             ("737s sold 2045-60", n0(b45), f"against {n0(b60)} in the conservative-case game; COMAC {n0(SUM(MP, 'comac', 2026, 2060))} and the entrant {n0(SUM(MP, 'entrant', 2026, 2060))} over 2026-60.")]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MAX Phase-out Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun (dash-2050-phaseout) · BOEING PROPRIETARY</p>
<h1>The MAX phase-out game: same moves, a weaker fps case</h1>
<p class="lede">The game replayed in the world you set in the Do Nothing tuner: your page's demand, the 737 MAX phased out from
{OPT["max_phaseout"]["start"]} with none built from {OPT["max_phaseout"]["gone"]}, Airbus adding up to {OPT["airbus_extra"]["cap"]:.0f} a month of extra lines from {OPT["airbus_extra"]["from"]},
COMAC selling its capacity to its own customers first (150 a year in 2035, 250 from 2050), and a new entrant in service in
{tp["entrant"]["eis"]} serving customers nobody else can. Every company played as before: its Board and ExCo, round by round.
Below, against the conservative-case game.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>What each company did</h2><div class="panel">{moves_table()}
<p class="cap">Boeing held the fps in all four rounds, and its Board vetoed the 787 Re-engine in 2030. The engine makers regrouped in 2035, as before.</p></div></section>

<section><h2>Boeing's fps case, round by round</h2><div class="stack">
<div class="panel"><p class="ctitle">The phase-out narrows the gap over time, but COMAC keeps it about $1.5B wider than in the conservative-case game</p><div class="cw">{gap_chart()}</div>
<p class="cap">Each round's brief, the 10-year fps at Renton against Do Nothing (worst and best columns below). The gap narrows round by round in both
games, mostly because a later bill is discounted further; neither reaches the Board's +$1B.</p></div>
<div class="panel">{gap_table()}</div>
<div class="panel"><p class="label">Why the 2030 case is weaker: one assumption at a time</p>{steps_table()}
<p class="cap">The phase-out makes Do Nothing worse and helps the fps by {bp(ST["steps"][2]["change"], 2, False)}. COMAC selling its capacity first takes
150-250 customers a year off the top: with Do Nothing, Boeing could not build enough 737s to serve them anyway, but with an fps it could.</p></div>
</div></section>

<section><h2>The market in the final state</h2><div class="stack">
<div class="panel"><p class="ctitle">Airbus takes most of the MAX's customers; COMAC sells its full capacity</p>
<div class="legend"><span><i class="sq" style="background:var(--s1)"></i>Boeing 737 MAX</span><span><i class="sq" style="background:var(--s2)"></i>Airbus</span><span><i class="sq" style="background:var(--comac)"></i>COMAC</span><span><i class="sq" style="background:var(--s3)"></i>New entrant</span><span><i class="ln" style="background:var(--fg);width:16px;height:2px;display:inline-block"></i>Demand</span></div>
<div class="cw">{market_chart()}</div></div>
<div class="panel">{market_table()}</div>
</div></section>

<section><h2>Value at the end of the game</h2><div class="panel">{value_table()}
<p class="cap">Each company's change against the status quo, PV at 2026; the status quo runs the same world (the phase-out, Airbus's extra lines,
COMAC and the entrant), so the values compare plans within each world.</p></div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The world</b> is sd_options_phaseout.json, the settings of your Do Nothing tuner table (1 Nov 2026); the engine gives back that table to the aircraft (test_phaseout.py).</li>
<li><b>The phase-out applies to every Boeing plan</b>, not only Do Nothing: the MAX ages either way. COMAC and the entrant compete in every plan too.</li>
<li><b>Everything else</b> is the conservative-case game: firm orders inside demand, Boeing losing 1 point a year while NGSA flies alone, Boeing taking Airbus's slack, Airbus adding 1% capacity a year when short, the same Boards, ExCos and objectives.</li>
<li><b>Source:</b> extract.py (one run each) and make_phaseout_html.py; the round records are in record/.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_phaseout_html.py from runs dash-2050-phaseout and dash-2050-cons.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_phaseout.html"))
