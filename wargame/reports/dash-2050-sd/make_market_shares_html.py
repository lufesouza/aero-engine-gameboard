"""Build market_shares.html: Boeing's narrowbody market-share assumptions in the fps business case (run dash-2050-sd):
Do Nothing against a 2030 10-year fps at Renton, Airbus's 2030 orders as played. Two shares: what customers prefer (the
dashboard's share rule, the assumption) and what Boeing delivers (the supply-and-demand layer, the outcome). Every number
comes from analysis/market_shares/shares.json (shares.py) and analysis/fps_business_case/case.json.

Usage: python3 make_market_shares_html.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
from make_sd_html import lines, legend, n0  # noqa: E402

esc = K.esc
S = json.load(open(os.path.join(HERE, "analysis", "market_shares", "shares.json")))
C = json.load(open(os.path.join(HERE, "analysis", "fps_business_case", "case.json")))
SDI = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "supply_demand.json")))
F = {int(y): r for y, r in S["fps"].items()}
D = {int(y): r for y, r in S["do_nothing"].items()}
EIS_F, EIS_N = S["eis"]["fps"], S["eis"]["ngsa"]
X_HI = 2060
YEARS = [y for y in S["years"] if y <= X_HI]
BOARD_NB = S["board"]["nb_per_year"]


def pc(v, dp=0):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


# ─────────────────────────────── facts from the data ───────────────────────────────
pref_f = {y: F[y]["pref_b"] for y in YEARS}
pref_d = {y: D[y]["pref_b"] for y in YEARS}
long_f, floor_d = pref_f[X_HI], pref_d[X_HI]
y_long = next(y for y in YEARS if y >= EIS_F and abs(pref_f[y] - long_f) < 1e-9)
y_floor = next(y for y in YEARS if abs(pref_d[y] - floor_d) < 1e-9)
lead = EIS_F - EIS_N
sq_b = pref_d[2026]
lead_edge = (pref_f[EIS_N] - sq_b)                                  # Boeing's change per year while NGSA is alone (fps case)
dn_step = (pref_d[EIS_N] - sq_b)                                    # same, Do Nothing
pre_eis_gap = [(y, pref_f[y] - pref_d[y]) for y in range(EIS_N, EIS_F)]
b_eq = long_f - lead_edge * lead                                    # balance point implied: long run = balance - edge x lead
assert abs(b_eq - 0.50) < 1e-9, b_eq                                # the board's post-2037 split slider (50%)
assert abs(dn_step + 0.03) < 1e-9 and abs(lead_edge + 0.01) < 1e-9
bf = SDI["boeing"]
d2050 = (D[2050], F[2050])
rows_case = {r["year"]: r for r in C["cases"]["renton"]["rows"]}
early_op = sum(rows_case[y]["op_profit_inc"] for y in range(EIS_N, EIS_F))
early_op_pv = sum(rows_case[y]["op_profit_inc"] * rows_case[y]["df"] for y in range(EIS_N, EIS_F))
dn_full = next(y for y in YEARS if y > EIS_N and D[y]["boeing_dlv"] >= D[y]["cap_b"] - 0.5)
dn_trans = (min(D[y]["dlv_share_b"] for y in range(EIS_N + 1, dn_full - 1)), max(D[y]["dlv_share_b"] for y in range(EIS_N + 1, dn_full - 1)))
assert all(abs(D[y]["dlv_share_b"] - D[X_HI]["dlv_share_b"]) < 0.005 for y in range(dn_full - 1, X_HI + 1))
a_dip = [D[y]["cap_a"] for y in range(EIS_N + 1, EIS_F + 1)]
assert all(abs(D[y]["airbus_dlv"] - D[y]["cap_a"]) < 0.5 for y in range(EIS_N + 1, X_HI + 1))   # Airbus sells out from 2038
assert abs(D[EIS_N]["boeing_dlv"] - D[EIS_N]["wanted_b"] - D[EIS_N - 1]["backlog_b"]) < 0.5      # 2037: new + all waiting
assert D[EIS_N]["airbus_dlv"] < D[EIS_N]["cap_a"] - 0.5 and D[EIS_N]["boeing_dlv"] < D[EIS_N]["cap_b"] - 0.5
assert D[EIS_N]["airbus_dlv"] < D[EIS_N - 1]["airbus_dlv"] and D[EIS_N]["boeing_dlv"] <= D[EIS_N - 1]["boeing_dlv"]
spill_dn = [D[y]["spill_to_b"] for y in range(EIS_N + 1, X_HI + 1)]
lost_dn_2050 = D[2050]["lost"]
f_short = [y for y in range(EIS_F, EIS_F + 6) if F[y]["dlv_share_b"] < F[y]["pref_b"] - 0.005]
f_above = [y for y in range(2050, X_HI + 1) if F[y]["dlv_share_b"] > F[y]["pref_b"] + 0.005]
assert f_above[0] == 2050 and F[2050]["spill_to_b"] > 0 and F[2050]["max"] > 0 and F[2051]["max"] < 0.5 and F[2051]["spill_to_b"] > 0


# ─────────────────────────────── charts ───────────────────────────────
def chart_pref():
    series = [("fps", "s1", [(y, pref_f[y]) for y in YEARS], False), ("Do Nothing", "s2", [(y, pref_d[y]) for y in YEARS], False)]
    return lines(series, 0.6, 0.1, "pct", "Boeing share of new 737/A320-class orders customers want (Airbus has the rest)",
                 "Boeing customer-preference share, fps against Do Nothing",
                 notes=[(EIS_N, "NGSA"), (EIS_F, "fps")], x_hi=X_HI)


def chart_case(R, name):
    series = [("Delivered", "s1" if name == "fps" else "s2", [(y, R[y]["dlv_share_b"]) for y in YEARS], False),
              ("Preferred", "s1" if name == "fps" else "s2", [(y, R[y]["pref_b"]) for y in YEARS], True)]
    return lines(series, 0.6, 0.1, "pct", "Boeing share of 737/A320-class orders (dashed) and deliveries (solid)",
                 f"Boeing preferred and delivered share, {name}", notes=[(EIS_N, "NGSA"), (EIS_F, "fps")] if name == "fps" else [(EIS_N, "NGSA")],
                 x_hi=X_HI)


# ─────────────────────────────── tables ───────────────────────────────
def year_table():
    head = ["Year", "Preferred: Do Nothing", "Preferred: fps", "Delivered: Do Nothing", "Delivered: fps",
            "Boeing aircraft: Do Nothing", "Boeing aircraft: fps", "of which fps", "Airbus aircraft: Do Nothing", "Airbus aircraft: fps",
            "New demand", "Overflow to Boeing: Do Nothing", "Overflow to Boeing: fps"]
    rows = []
    for y in YEARS:
        d, f = D[y], F[y]
        rows.append([str(y), pc(d["pref_b"]), pc(f["pref_b"]), pc(d["dlv_share_b"], 1), pc(f["dlv_share_b"], 1),
                     n0(d["boeing_dlv"]), n0(f["boeing_dlv"]), n0(f["fps"]), n0(d["airbus_dlv"]), n0(f["airbus_dlv"]),
                     n0(d["demand"]), n0(d["spill_to_b"]), n0(f["spill_to_b"])])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def rule_table():
    head = ["Year", "Do Nothing (only Airbus launches)", "fps (both launch, NGSA 3 years first)"]
    pts = [2026, EIS_N - 1, EIS_N, EIS_N + 1, EIS_N + 2, EIS_F, EIS_F + 1, EIS_F + 2, y_floor, y_long - 1, y_long, X_HI]
    pts = sorted(set(pts))
    def why_d(y):
        if y < EIS_N:
            return "status quo"
        if y < y_floor:
            return f"NGSA alone in service: Airbus +3 points a year ({y - EIS_N + 1} × 3)"
        return "Airbus at its 80% cap"
    def why_f(y):
        if y < EIS_N:
            return "status quo"
        if y < EIS_F:
            return f"NGSA leads: Airbus +1 point a year of lead ({y - EIS_N + 1} × 1)"
        if y < y_long:
            return f"fps in service: Boeing +1 point a year from {pc(sq_b + lead_edge * lead)} ({y - EIS_F + 1} × 1)"
        return f"long-run split reached: 50% less 1 point × {lead} years of NGSA lead"
    rows = [[str(y) + ("–" + str(EIS_N - 1) if y == 2026 else "") + ("+" if y == X_HI else ""),
             f"<b>{pc(pref_d[y])}</b> · {esc(why_d(y))}", f"<b>{pc(pref_f[y])}</b> · {esc(why_f(y))}"] for y in pts if y != EIS_N - 1]
    return K.table(head, rows)


def tiles():
    t = [("Customers prefer Boeing, Do Nothing", pc(floor_d), f"From {y_floor}: NGSA alone takes Airbus to its 80% cap."),
         ("Customers prefer Boeing, fps", pc(long_f), f"From {y_long}: the 50/50 balance point less NGSA's {lead}-year lead."),
         ("Boeing delivers, Do Nothing", pc(D[X_HI]["dlv_share_b"]),
          f"From {dn_full - 1}: Airbus cannot build 80% of the market, so its overflow buys 737 MAX ({pc(dn_trans[0])}-{pc(dn_trans[1])} in {EIS_N + 1}-{dn_full - 2})."),
         ("Boeing delivers, fps", pc(F[2050]["dlv_share_b"]), f"In 2050: {n0(F[2050]['boeing_dlv'])} aircraft against {n0(D[2050]['boeing_dlv'])} with Do Nothing.")]
    return '<div class="tiles">' + "".join(
        f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d_)}</div></div>' for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS + "\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }\n"
    d50, f50 = d2050
    board_gap = (long_f - floor_d) * BOARD_NB
    game_gap = f50["boeing_dlv"] - d50["boeing_dlv"]
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Narrowbody Share Assumptions</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · supply-and-demand war game (dash-2050-sd) · BOEING PROPRIETARY</p>
<h1>Narrowbody market shares: Do Nothing and fps</h1>
<p class="lede">The fps business case rests on two shares. The first is an assumption: the share of new 737/A320-class orders
customers want to give Boeing, set by the dashboard's share rule. The second is the outcome: Boeing's share of what is actually
delivered, once the game has served the firm backlog and limited each maker to what it can build. With Do Nothing, customers'
preference for Boeing falls to {pc(floor_d)}, but Boeing still delivers {pc(D[X_HI]["dlv_share_b"])} of the market, because Airbus cannot build
the rest. With the fps, preference recovers to {pc(long_f)} and deliveries follow it. Both cases: Airbus's 2030 orders as played
(NGSA in service {EIS_N}, A320 Alt plan); the fps launched in 2030, in service {EIS_F}, at Renton.</p>
<nav class="toc"><a href="#pref">The assumption</a><a href="#rule">The rule</a><a href="#delivered">The outcome</a><a href="#table">Year by year</a><a href="#notes">Notes</a></nav></header>

<section style="margin-top:22px">{tiles()}</section>

<section id="pref"><h2>The assumption: customer preference</h2><p class="lede">Until a new narrowbody enters service,
customers split 40/60 between Boeing and Airbus. NGSA enters service in {EIS_N}. With Do Nothing, Airbus then gains 3 points a
year until it holds 80%. With the fps, Airbus gains only 1 point a year while NGSA is alone, and from {EIS_F} Boeing wins back
1 point a year until it reaches {pc(long_f)} in {y_long}.</p><div class="stack">
<div class="panel"><p class="ctitle">Customers' preference for Boeing falls to {pc(floor_d)} with Do Nothing and recovers to {pc(long_f)} with the fps</p>
{legend([("fps", "s1", "ln"), ("Do Nothing", "s2", "ln")])}{chart_pref()}
<p class="cap">Vertical lines: NGSA enters service in {EIS_N}, the fps in {EIS_F}. Status quo 40%. The two cases part in {EIS_N}, three years before the fps flies: the fps case is
{", ".join(f"{K.rnd(g * 100, 0):.0f}" for _, g in pre_eis_gap)} points ahead in {EIS_N}-{EIS_F - 1} only because an fps has been launched.</p></div>
</div></section>

<section id="rule"><h2>The rule behind it</h2><p class="lede">The dashboard's share rule (board v3), with this game's settings. Only Boeing's
share is shown; Airbus has the rest. No other share moves apply in either case: no 737 rate increase and no Delay Tactics.</p>
<div class="stack"><div class="panel">{rule_table()}</div>
<div class="panel"><p class="label">Settings and where they come from</p><ul class="cav">
<li><b>Status quo: Boeing 40%, Airbus 60%</b> until the first new narrowbody enters service. Dashboard constant.</li>
<li><b>NGSA alone (Boeing does not launch): Airbus +3 points a year to 80%.</b> Fixed in the dashboard, not a slider (an fps alone would
instead climb at the Boeing capture speed below). Here: Boeing {pc(sq_b + dn_step)} in {EIS_N}, falling to {pc(floor_d)} from {y_floor}.</li>
<li><b>Both launch: the leader's edge, 1 point a year of lead</b> (slider "NB share edge per year of EIS lead (pp)", 1.0). While NGSA is alone in service, Airbus gains 1 point a year: Boeing {pc(pref_f[EIS_N])}, {pc(pref_f[EIS_N + 1])}, {pc(pref_f[EIS_N + 2])} in {EIS_N}-{EIS_F - 1}.</li>
<li><b>Long-run split: the balance point less the leader's edge.</b> Balance point 50/50 (slider "Boeing fps share of post-2037 NB market (%)", 50), shifted
1 point per year of lead toward the first new narrowbody in service: 50% − 1 × {lead} = {pc(long_f)} for Boeing.</li>
<li><b>Boeing's capture speed: 1 point a year</b> (slider "Boeing share capture (pp/yr) — 10-yr ramp", 1.0; "fps capture speed" in the snapshot): Boeing climbs from {pc(sq_b + lead_edge * lead)} in {EIS_F - 1} to {pc(long_f)} in {y_long}.</li>
</ul><p class="cap">Source: board v3 (combined_dash.py, the unified narrowbody share rule) and the Game v3 snapshot. The dashboard alone sells
these shares of a fixed {n0(BOARD_NB)} aircraft a year; the game uses them to split real demand.</p></div></div></section>

<section id="delivered"><h2>The outcome: what Boeing delivers</h2><p class="lede">The supply-and-demand layer turns preference into
deliveries. Each year the firm backlog is delivered first (737 MAX {n0(SDI["demand"]["firm_backlog"]["boeing"])}, A320neo family
{n0(SDI["demand"]["firm_backlog"]["airbus"])} at the start). New demand (replacement plus fleet growth, {n0(D[2030]["demand"])}
aircraft in 2030 and {n0(D[2050]["demand"])} in 2050) is split by preference. Each maker delivers what it can build:
{pc(SDI["demand"]["flex_share"], 1)} of customers it cannot serve take the other maker's free slots, and {pc(SDI["demand"]["lapse_per_year"])}
of those still waiting drop out each year.</p><div class="stack">
<div class="panel"><p class="ctitle">Do Nothing: customers want {pc(floor_d)} Boeing, but Boeing delivers {pc(D[2050]["dlv_share_b"])}</p>
{legend([("Delivered share", "s2", "ln"), ("Preferred share", "s2", "dash")])}{chart_case(D, "Do Nothing")}
<p class="cap">From {EIS_N + 1} Airbus sells all it can build: {n0(min(a_dip))}-{n0(max(a_dip))} a year in {EIS_N + 1}-{EIS_F} while it switches from the A320 to NGSA, and at most
{n0(D[2050]["cap_a"])} a year from 2046 (NGSA at 100 a month). In 2050, {n0(D[2050]["wanted_a"])} new customers want an Airbus and {n0(D[2049]["backlog_a"])} are still waiting from
earlier years. Airbus builds {n0(D[2050]["cap_a"])}, {n0(D[2050]["spill_to_b"])} take every 737 MAX slot Boeing has free, {n0(lost_dn_2050)} drop out, and
{n0(D[2050]["backlog_a"])} are still waiting at year end ({n0(D[X_HI]["backlog_a"])} by {X_HI}).
Boeing sells all {n0(D[2050]["cap_b"])} MAX it can build from {dn_full}. Before {EIS_N} both makers sell out, so delivered shares follow capacity, not preference. In {EIS_N} neither sells out: Boeing delivers its last
{n0(D[EIS_N - 1]["backlog_b"])} waiting customers on top of {n0(D[EIS_N]["wanted_b"])} new ones ({n0(D[EIS_N]["boeing_dlv"])} of {n0(D[EIS_N]["cap_b"])}), while Airbus, with only
{n0(D[EIS_N - 1]["backlog_a"])} customers still waiting, delivers {n0(D[EIS_N]["airbus_dlv"])} of {n0(D[EIS_N]["cap_a"])}. Airbus delivering less is what lifts Boeing's
delivered share to its {pc(D[EIS_N]["dlv_share_b"], 1)} peak.</p></div>
<div class="panel"><p class="ctitle">fps: deliveries follow preference once the fps is at rate</p>
{legend([("Delivered share", "s1", "ln"), ("Preferred share", "s1", "dash")])}{chart_case(F, "fps")}
<p class="cap">In {f_short[0]}-{f_short[-1]} Boeing delivers less than customers want ({n0(F[f_short[0]]["boeing_dlv"])}-{n0(F[f_short[-1]]["boeing_dlv"])} aircraft against
{n0(F[f_short[0]]["wanted_b"])}-{n0(F[f_short[-1]]["wanted_b"])} wanted): the fps is still ramping up and Renton's 737 MAX lines are winding down. From {f_above[0]}
NGSA's customers overflow to Boeing, so Boeing delivers slightly more than its preference. In {f_above[0]} they get 737 MAX
({n0(F[f_above[0]]["max"])}), because the fps line is held at {n0(F[f_above[0]]["fps"])} a year while the last MAX are built at Everett; from {f_above[0] + 1} they get the fps.</p></div>
</div></section>

<section id="table"><h2>Year by year</h2><p class="lede">Boeing shares and aircraft a year, 737/A320 class. Preferred share is the
assumption; delivered share and aircraft are the game's outcome. The fps case is at Renton.</p><div class="panel">{year_table()}</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Why this matters for the business case.</b> On the dashboard alone, the long-run gap in preference ({pc(floor_d)} against {pc(long_f)}) is
{n0(board_gap)} aircraft a year of the fixed {n0(BOARD_NB)}. In the game the 2050 gap is {n0(game_gap)} aircraft ({n0(d50["boeing_dlv"])} against {n0(f50["boeing_dlv"])}):
Do Nothing keeps more than its preference because Airbus's overflow buys 737 MAX, which is the Do Nothing benefit the business case nets out.</li>
<li><b>The three years before the fps flies.</b> The fps case is ahead in preference from {EIS_N} only because the rule slows Airbus from 3 points a
year to 1 once Boeing has launched. That earns the fps case {K.usd(early_op, 2, False)} of operating profit in {EIS_N}-{EIS_F - 1} ({K.usd(early_op_pv, 2, False)} at 2026)
before a single fps is delivered. It is a dashboard assumption, not a market observation.</li>
<li><b>What is the dashboard's and what is ours.</b> The share rule and its settings are the dashboard's. Demand, the firm backlog, capacities,
the overflow and drop-out rates are game-master assumptions (supply_demand.json and supply_demand_sources.md).</li>
<li><b>Source.</b> analysis/market_shares/shares.py writes shares.json from the game engine; it checks that the shares close and that the
two cases reproduce the business case's {K.usd(C["cases"]["renton"]["game_npv"])}.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_market_shares_html.py from analysis/market_shares/shares.json (run dash-2050-sd, corrected demand).</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "market_shares.html"))
