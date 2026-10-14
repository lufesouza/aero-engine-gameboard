"""Build demand_curve.html: the proposed annual demand curve for the game, fitted to the user's conservative-case
table (dashgame/demand_conservative.json, from make_demand_conservative.py), the 737/A320-class demand it gives, a
comparison with the curve used in dash-2050-sd, and the firm-backlog choice the game needs before it is wired in.
Nothing here runs the game.

Usage: python3 make_demand_page.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HERE, "..", "..", "dashgame")
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-sd"))
import page_kit as K  # noqa: E402
from make_sd_html import lines, legend  # noqa: E402

esc = K.esc
J = json.load(open(os.path.join(DG, "demand_conservative.json")))
SD = json.load(open(os.path.join(DG, "supply_demand.json")))["demand"]
CS = SD["class_share"]
FB = SD["firm_backlog"]
KB = FB["boeing"] + FB["airbus"]
Y = J["years"]
C = J["components"]
I = {y: i for i, y in enumerate(Y)}
COMP = [("old_gen", "Old-generation replacement", "s2"), ("max_neo_a220", "MAX / A320neo / A220 replacement", "s1"),
        ("post_2026", "Replacement of post-2026 deliveries", "s3"), ("growth", "Fleet growth", "s4")]


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def k1(v):
    return f"{K.rnd(v / 1000, 1):,.1f}k"


def cur(y):
    """The demand curve used in dash-2050-sd, 737/A320 class (supply_demand.demand)."""
    ys = SD["years"]
    yy = min(max(y, ys[0]), ys[-1])
    g = SD["growth"].get(str(y), SD["growth"][max(SD["growth"], key=int)])
    return (g + SD["replacements"][ys.index(yy)]) * CS


TOT = {y: J["total"][I[y]] for y in Y}
CL = {y: TOT[y] * CS for y in Y}                                   # 737/A320 class
OPT_A = {y: (TOT[y] - C["old_gen"][I[y]]) * CS for y in Y}         # old-gen replaced by the firm backlog
OPT_B, cum = {}, 0.0
for y in Y:                                                         # firm orders = the first KB aircraft of demand
    prev, cum = cum, cum + CL[y]
    OPT_B[y] = max(0.0, cum - KB) - max(0.0, prev - KB)
B_START = next(y for y in Y if OPT_B[y] > 0)
OLD_SUM = sum(C["old_gen"][I[y]] for y in Y)
CAP_SQ = 12 * 57 + 12 * 85                                          # status-quo capacity: MAX 57 a month + A320 85


def runs(series):
    """Contiguous year runs (to 2070) in which a demand series is above the status-quo capacity."""
    out, start = [], None
    for y in Y:
        if series[y] > CAP_SQ and start is None:
            start = y
        if series[y] <= CAP_SQ and start is not None:
            out.append((start, y - 1)); start = None
    if start is not None:
        out.append((start, Y[-1]))
    return out


def vol(series, lo, hi):
    return sum(series[y] for y in range(lo, hi + 1))


# ─────────────────────────────── charts ───────────────────────────────
def chart_stack():
    """Annual demand by component (whole single-aisle market), stacked, with the table's totals as rings."""
    w, h, left, right, top, bot = 760, 360, 58, 20, 20, 46
    hi, step = 2600, 500
    n = len(Y)
    sx = lambda i: left + i * (w - left - right) / n
    bw = (w - left - right) / n - 2
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Annual single-aisle demand by component, 2026-2070, with the table's years marked")]
    v = 0
    while v <= hi:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="{"zero" if v == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{n0(v)}</text>')
        v += step
    for i, y in enumerate(Y):
        x = sx(i) + 1
        base = 0.0
        parts = [(key, lab, var, C[key][i]) for key, lab, var in COMP if C[key][i] > 0.5]
        for j, (key, lab, var, val) in enumerate(parts):
            y0, y1 = sy(base) - (0 if j == 0 else 1), sy(base + val)
            if j == len(parts) - 1:
                out.append(f'<path d="{K.bar_path(x, bw, y0, y1, r=2)}" fill="var(--{var})"/>')
            else:
                out.append(f'<rect x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0.0, y0 - y1):.1f}" fill="var(--{var})"/>')
            base += val
        rows = [(n0(TOT[y]), f"{y}: total demand", None)] + [(n0(val), lab, f"var(--{var})") for key, lab, var, val in parts]
        if str(y) in J["table"]:
            rows.append((n0(J["table"][str(y)]["total"]), "your table", None))
        out.append(f'<rect x="{sx(i):.1f}" y="{top}" width="{bw + 2:.1f}" height="{h - top - bot}" class="hit" {K.mark_attrs(*rows)}/>')
        if y % 5 == 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    for ys, t in J["table"].items():
        i = I[int(ys)]
        out.append(f'<circle cx="{sx(i) + 1 + bw / 2:.1f}" cy="{sy(t["total"]):.1f}" r="4.5" class="hollow"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">Aircraft a year, whole single-aisle market (A220 included); rings: your table</text></svg>')
    lg = legend([(lab, var, "sq") for _, lab, var in COMP] + [("Your table's total", "fg", "ring")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def chart_compare():
    series = [("Option B", "s1", [(y, OPT_B[y]) for y in Y], False), ("Option A", "s2", [(y, OPT_A[y]) for y in Y], False),
              ("Last game", "muted", [(y, cur(y)) for y in Y], True)]
    return lines(series, 2600, 500, "int", "New 737/A320-class demand on top of the firm backlog, aircraft a year",
                 "New 737/A320-class demand under options A and B against the curve used in dash-2050-sd",
                 notes=[(B_START, "B starts"), (2046, "A = B")], x_hi=2070)


# ─────────────────────────────── tables ───────────────────────────────
def checks_table():
    head = ["Check", "Your table", "Curve"]
    rows = []
    for p in J["checks"]["periods"]:
        rows.append([f"Total demand {p['period']}", n0(p["table"]), n0(p["curve"])])
    for f in J["checks"]["fleet"]:
        rows.append([f"Fleet at end-{f['year']}", f"{f['table_k']:.1f}k", f"{f['curve_k']:.2f}k"])
    rows.append(["Every component in every year of your table", "11 years × 4", f"exact (largest gap {J['checks']['anchors_max_abs_error']:.1e})"])
    return K.table(head, rows, num_cols=(1, 2))


def year_table():
    head = ["Year", "Old-gen repl.", "MAX/neo/A220 repl.", "Post-2026 repl.", "Total repl.", "Growth", "Total",
            "Repl. share", "Fleet (end-year)", "Your table", "New demand, option A", "New demand, option B"]
    rows = []
    for y in Y:
        i = I[y]
        rep = J["replacements"][i]
        t = J["table"].get(str(y))
        rows.append([f"<b>{y}</b>" if t else str(y), n0(C["old_gen"][i]), n0(C["max_neo_a220"][i]), n0(C["post_2026"][i]), n0(rep),
                     n0(C["growth"][i]), f"<b>{n0(TOT[y])}</b>", f"{K.rnd(rep / TOT[y] * 100, 0):.0f}%", k1(J["fleet_end_year"][i]),
                     n0(t["total"]) if t else "", n0(OPT_A[y]), n0(OPT_B[y])])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def option_table():
    head = ["", "A. Firm orders stand in for old-gen replacement", "B. Firm orders are the first slice of your demand (recommended)"]
    rows = [
        ["Demand the game uses", "Growth + MAX/neo/A220 + post-2026 replacement; your old-gen column is dropped and the firm backlog takes its place",
         "Your whole table; the firm backlog is not extra but the first aircraft of it"],
        ["737/A320 class, 2026-2045", f"{k1(vol(OPT_A, 2026, 2045))} new + {k1(KB)} firm = {k1(vol(OPT_A, 2026, 2045) + KB)}",
         f"{k1(vol(CL, 2026, 2045))} (= your table)"],
        ["New customers beyond firm orders", "from 2026; they queue behind the firm orders and 10% a year drop out",
         f"from {B_START}, when your cumulative demand passes the {n0(KB)} firm orders"],
        ["Your old-gen timing (to 2045)", f"lost: the firm orders are delivered as fast as the lines allow, by about 2033", "kept: after the firm orders, old-gen replacement still arrives each year to 2045"],
        ["Demand in 2035 / 2040 / 2045", f"{n0(OPT_A[2035])} / {n0(OPT_A[2040])} / {n0(OPT_A[2045])}", f"{n0(OPT_B[2035])} (part year) / {n0(OPT_B[2040])} / {n0(OPT_B[2045])}"],
        ["From 2046", "the same in both: " + ", ".join(f"{n0(CL[y])} in {y}" for y in (2046, 2050, 2055, 2060)), "the same"],
        ["Change to the game", "inputs only", "inputs plus a small change: net the firm orders against cumulative demand"],
    ]
    return K.table(head, rows)


def tiles():
    t = [("Your curve, 2026-2045", k1(vol(TOT, 2026, 2045)), "Whole single-aisle market, A220 included; equals your table."),
         ("737/A320 class, 2046-2060", k1(vol(CL, 2046, 2060)), f"Against {k1(vol({y: cur(y) for y in Y}, 2046, 2060))} in the dash-2050-sd game: {K.num((vol(CL, 2046, 2060) / vol({y: cur(y) for y in Y}, 2046, 2060) - 1) * 100, '+.0f')}%."),
         ("Peak before 2060", n0(max(TOT[y] for y in Y if y < 2060)), f"In {max((y for y in Y if y < 2060), key=lambda y: TOT[y])}; then the old-gen fleet is used up and demand steps down to {n0(TOT[2046])} in 2046."),
         ("Low point", n0(min(TOT[y] for y in Y if 2046 <= y <= 2065)), f"In {min((y for y in Y if 2046 <= y <= 2065), key=lambda y: TOT[y])}: growth has faded to about 500 a year and the post-2026 replacement wave has not yet built up.")]
    return '<div class="tiles">' + "".join(
        f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d_)}</div></div>' for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS.replace("--s3: #17a06f;", "--s3: #17a06f; --s4: #8b5cc4;").replace("--s3: #199e70;", "--s3: #199e70; --s4: #a37ee0;")
    assert css.count("--s4") >= 2, "palette hook"
    css += ("\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }\n"
            ".legend i.ring { width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--fg); background: var(--surface); }\n")
    held = J["method"]["held_at_zero"]
    lin_excess = 650
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Game Demand Curve</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game inputs · proposed, not yet in the game · BOEING PROPRIETARY</p>
<h1>A demand curve for the game: your conservative case</h1>
<p class="lede">Your table gives eleven years and four period totals. The game needs every year from 2026. This is the
smoothest annual curve that passes exactly through every number in your table, matches all four period totals and keeps
the fleet within rounding of your fleet column. For the game's 737/A320 market it is {K.rnd((vol(CL, 2046, 2060) / vol({y: cur(y) for y in Y}, 2046, 2060) - 1) * -100, 0):.0f}% below the
curve used in the last game over 2046-2060, the years an fps would sell into. One choice is needed before it goes in:
how the {n0(KB)} firm orders sit against your old-generation replacement.</p>
<nav class="toc"><a href="#curve">The curve</a><a href="#compare">Against the last game</a><a href="#backlog">Firm orders</a><a href="#table">Year by year</a><a href="#method">Method</a></nav></header>

<section style="margin-top:22px">{tiles()}</section>

<section id="curve"><h2>The curve</h2><p class="lede">Annual demand by component, whole single-aisle market. Growth carries
demand to {n0(TOT[2045])} in 2045; old-generation replacement ends after 2045; growth then fades and the replacement of
aircraft delivered after 2026 takes over from about 2060.</p><div class="stack">
<div class="panel"><p class="ctitle">Demand climbs to {n0(TOT[2045])} in 2045, steps down when the old-generation fleet is used up, and rebuilds after 2060</p>
{chart_stack()}<p class="cap">Rings are your table's totals; every component also matches your table in those years.
The 2046 step ({n0(TOT[2045])} to {n0(TOT[2046])}) is the end of old-generation replacement: your 2046-2055 total only works if that fleet is used up by 2046.</p></div>
<div class="panel"><p class="label">Checks against your table</p>{checks_table()}</div>
</div></section>

<section id="compare"><h2>Against the last game</h2><p class="lede">What the game would add on top of the firm backlog: the
curve times the 737/A320 class share ({K.rnd(CS * 100, 2):.2f}%, the A220 left out), under the two firm-backlog options explained below,
against the new demand in the dash-2050-sd game. From 2046 the two options are the same.</p><div class="stack">
<div class="panel"><p class="ctitle">From 2046 both options are well below the last game: growth fades instead of compounding</p>
{legend([("Option B: your whole table, firm orders as its first slice", "s1", "ln"), ("Option A: without old-generation replacement", "s2", "ln"), ("Used in dash-2050-sd", "muted", "dash")])}{chart_compare()}
<p class="cap">The last game grew the fleet about 4% a year to 2044, easing to 3% a year by 2060, so its growth kept rising (about
{n0(SD["growth"]["2060"] * CS)} aircraft a year by 2060, 737/A320 class). Your curve's growth peaks at {n0(C["growth"][I[2045]])} in 2045 and falls to about 500 a year by 2060.
Before 2046 the options differ: A adds growth and today's-fleet replacement from 2026 and leaves old-generation replacement to the firm orders;
B adds nothing until your cumulative demand has used up the firm orders (in {B_START}), then your whole curve, old-generation replacement included.</p></div>
</div></section>

<section id="backlog"><h2>The one choice: firm orders and old-generation replacement</h2><p class="lede">The game delivers
the firm backlog first ({n0(FB["boeing"])} 737 MAX and {n0(FB["airbus"])} A320neo family, Cirium, Oct 2026) and adds new demand on top. Your table
has its own old-generation replacement, {k1(OLD_SUM)} aircraft over 2026-2045, almost the same size as the backlog. Counting both would count
the same customers twice. Two clean ways to avoid that:</p><div class="panel">{option_table()}
<p class="cap">I recommend B: the game's total demand is then exactly your table, and the firm orders are simply the part of it already contracted.
A keeps the game as it is but moves your old-generation demand forward to the years the lines can deliver it and adds about {k1(vol(OPT_A, 2026, 2045) + KB - vol(CL, 2026, 2045))} aircraft.
For reference, the two makers' status-quo capacity is {n0(CAP_SQ)} a year (737 MAX 57 a month, A320 85 a month); new demand is above that in {", ".join(f"{a}-{b}" for a, b in runs(OPT_B))} under B and {", ".join(f"{a}-{b}" for a, b in runs(OPT_A))} under A.</p></div></section>

<section id="table"><h2>Year by year</h2><p class="lede">Aircraft a year. Bold years are your table's; the others are fitted.
The components, total and fleet are the whole single-aisle market. The two new-demand columns are what the game would add on top
of the firm backlog, 737/A320 class, under each option.</p><div class="panel">{year_table()}</div></section>

<section id="method"><h2>Method</h2><div class="panel"><ul class="cav">
<li><b>Fit.</b> For each component, the annual path with the least squared second differences (the smoothest) that passes through your values in all eleven years
and makes total demand match your four period totals exactly. The fleet (19.7k at end-2026 plus each year's growth) is held to your fleet column as a soft constraint;
it ends within {max(abs(f["curve_k"] - f["table_k"]) for f in J["checks"]["fleet"]) * 1000:.0f} aircraft of every value, inside the column's 0.1k rounding.</li>
<li><b>Old-generation replacement ends after 2045.</b> Your table has 336 in 2045 and 0 in 2050. A straight run-down to 2050 would put about {n0(lin_excess)} more aircraft into 2046-2055
than your 18.7k total; ending it after 2045 fits.</li>
<li><b>Held at zero.</b> No value may be negative; {len(held)} tiny values sit at zero ({esc(", ".join(h.replace("max_neo_a220", "MAX/neo/A220").replace("post_2026", "post-2026") for h in held))}).
Post-2026 replacement starts in 2046 (your table has 0 to 2045).</li>
<li><b>Rounding.</b> Your 2045 total (2,130) is one above its parts (936 + 1,193); the curve keeps the parts.</li>
<li><b>Class share.</b> Your table covers the whole single-aisle market, A220 included. The game models the 737/A320 market and applies its class share ({K.rnd(CS * 100, 2):.2f}%,
from the Cirium fleet and order scope) once, as it does now.</li>
<li><b>After 2070.</b> The game holds the 2070 values ({n0(TOT[2070])} a year). That matters only for a programme entering service after 2051, whose
20-year window runs past 2070.</li>
<li><b>Not changed.</b> Firm backlog, customer preference, the overflow and drop-out rates, and every maker's capacity stay as they are.</li>
<li><b>Source.</b> dashgame/make_demand_conservative.py writes demand_conservative.json and asserts every check above. The game has not been run with it.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_demand_page.py from dashgame/demand_conservative.json and dashgame/supply_demand.json.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "demand_curve.html"))
