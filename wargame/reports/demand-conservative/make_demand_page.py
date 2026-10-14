"""Build demand_curve.html: the annual demand curve fitted to the user's conservative-case table
(dashgame/demand_conservative.json, from make_demand_conservative.py), the 737/A320-class demand the game uses (run
dash-2050-cons: the firm orders are the first slice of this demand, option B), and a comparison with the curve of
dash-2050-sd.

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
OPT_B, left = {}, KB
for y in Y:                         # each year's demand is served first from the open firm orders (supply_demand netting)
    need = min(CL[y], left)
    OPT_B[y] = CL[y] - need
    left -= need
B_START = next(y for y in Y if OPT_B[y] > 0)
OLD_SUM = sum(C["old_gen"][I[y]] for y in Y)


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
    series = [("All demand", "s1", [(y, CL[y]) for y in Y], False), ("New customers", "s1", [(y, OPT_B[y]) for y in Y], True),
              ("Last game", "muted", [(y, cur(y)) for y in Y], True)]
    return lines(series, 2600, 500, "int", "737/A320-class demand, aircraft a year",
                 "737/A320-class demand in this game against the new demand of dash-2050-sd",
                 notes=[(B_START, "new customers")], x_hi=2070)


# ─────────────────────────────── tables ───────────────────────────────
def checks_table():
    head = ["Check", "Your table", "Curve"]
    rows = []
    for p in J["checks"]["periods"]:
        rows.append([f"Total demand {p['period']}", n0(p["table"]), n0(p["curve"])])
    fl = {y: v for y, v in zip(Y, J["fleet_end_year"])}
    for f in J["checks"]["fleet"]:
        rows.append([f"Fleet at end-{f['year']}", f"{f['table_k']:.1f}k", f"{fl[f['year']] / 1000:.2f}k"])
    rows.append(["Every component in every year of your table", "11 years × 4", f"exact (largest gap {J['checks']['anchors_max_abs_error']:.1e})"])
    return K.table(head, rows, num_cols=(1, 2))


def year_table():
    head = ["Year", "Old-gen repl.", "MAX/neo/A220 repl.", "Post-2026 repl.", "Total repl.", "Growth", "Total",
            "Repl. share", "Fleet (end-year)", "Your table", "737/A320 class: all demand", "of which new customers"]
    rows = []
    for y in Y:
        i = I[y]
        rep = J["replacements"][i]
        t = J["table"].get(str(y))
        rows.append([f"<b>{y}</b>" if t else str(y), n0(C["old_gen"][i]), n0(C["max_neo_a220"][i]), n0(C["post_2026"][i]), n0(rep),
                     n0(C["growth"][i]), f"<b>{n0(TOT[y])}</b>", f"{K.rnd(rep / TOT[y] * 100, 0):.0f}%", k1(J["fleet_end_year"][i]),
                     n0(t["total"]) if t else "", n0(CL[y]), n0(OPT_B[y])])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def tiles():
    cv = {y: cur(y) for y in Y}
    pk = max((y for y in Y if y < 2060), key=lambda y: TOT[y])
    lo = min((y for y in Y if 2046 <= y <= 2065), key=lambda y: TOT[y])
    t = [("Your curve, 2026-2045", k1(vol(TOT, 2026, 2045)), "Whole single-aisle market, A220 included; equals your table."),
         ("737/A320 class, 2040-2059", k1(vol(CL, 2040, 2059)),
          f"The 20 years a 2030 fps would sell into; {k1(vol(cv, 2040, 2059))} in dash-2050-sd ({K.num((vol(CL, 2040, 2059) / vol(cv, 2040, 2059) - 1) * 100, '+.0f')}%)."),
         ("Peak before 2060", n0(TOT[pk]), f"In {pk}; then old-generation replacement tapers off over 2046-2049 and demand eases to {n0(min(TOT[y] for y in range(2046, 2050)))}."),
         ("Low point after 2045", n0(TOT[lo]), f"In {lo}: growth is down to about {K.rnd(C['growth'][I[lo]], -1):.0f} a year and the replacement of post-2026 deliveries has not yet built up.")]
    return '<div class="tiles">' + "".join(
        f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d_)}</div></div>' for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS.replace("--s3: #17a06f;", "--s3: #17a06f; --s4: #8b5cc4;").replace("--s3: #199e70;", "--s3: #199e70; --s4: #a37ee0;")
    assert css.count("--s4") >= 2, "palette hook"
    css += ("\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }\n"
            ".legend i.ring { width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--fg); background: var(--surface); }\n")
    held = J["method"]["held_at_zero"]
    first_post = next(y for y in Y if C["post_2026"][I[y]] > 0.5)
    old_tail = [y for y in Y if y > 2045 and C["old_gen"][I[y]] > 0.5]
    cv = {y: cur(y) for y in Y}
    fl_dev = max(abs(f["curve_k"] - f["table_k"]) for f in J["checks"]["fleet"]) * 1000
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Game Demand Curve</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game inputs · used in run dash-2050-cons · BOEING PROPRIETARY</p>
<h1>The game's demand curve: your conservative case</h1>
<p class="lede">Your table gives eleven years and four period totals; the game needs every year from 2026. This is the
smoothest annual curve that passes through every component of your table in those eleven years, matches all four period
totals and keeps the fleet within the rounding of your fleet column. The game uses it for the 737/A320 market
({K.rnd(CS * 100, 2):.2f}% of it), with the {n0(KB)} firm orders as the first slice of this demand, not extra to it.</p>
<nav class="toc"><a href="#curve">The curve</a><a href="#compare">Against the last game</a><a href="#backlog">Firm orders</a><a href="#table">Year by year</a><a href="#method">Method</a></nav></header>

<section style="margin-top:22px">{tiles()}</section>

<section id="curve"><h2>The curve</h2><p class="lede">Annual demand by component, whole single-aisle market. Growth carries
demand to {n0(TOT[2045])} in 2045; old-generation replacement tapers off over 2046-{old_tail[-1] if old_tail else 2045}; growth then fades and the
replacement of aircraft delivered after 2026 takes over from about 2060.</p><div class="stack">
<div class="panel"><p class="ctitle">Demand climbs to about 2,130 by 2045, eases as the old-generation fleet is used up, and rebuilds after 2060</p>
{chart_stack()}<p class="cap">Rings are your table's totals; every component also matches your table in those years. Your table has old-generation
replacement at 336 in 2045 and none in 2050; the smoothest path that also meets your 18.7k total for 2046-2055 runs it down to
{", ".join(n0(C["old_gen"][I[y]]) for y in old_tail)} in 2046-{old_tail[-1]}.</p></div>
<div class="panel"><p class="label">Checks against your table</p>{checks_table()}</div>
</div></section>

<section id="compare"><h2>Against the last game</h2><p class="lede">What the game uses: your curve times the 737/A320 class
share. The last game's line is its new demand (on top of its firm backlog), as corrected after that game (the game itself was
played on growth about 5% lower).</p><div class="stack">
<div class="panel"><p class="ctitle">Above the last game to 2045, well below it from 2047 to 2065: growth fades instead of compounding</p>
{legend([("This game: all demand (firm orders + new customers)", "s1", "ln"), ("This game: new customers beyond the firm orders", "s1", "dash"), ("dash-2050-sd: new demand", "muted", "dash")])}{chart_compare()}
<p class="cap">On the same 737/A320 basis, the last game's growth kept rising, to about {n0(SD["growth"]["2060"] * CS)} aircraft a year by 2060; in your curve it
peaks at {n0(C["growth"][I[2045]] * CS)} in 2045 and is about {n0(C["growth"][I[2060]] * CS)} by 2060. From 2035 to 2045 your curve is higher ({K.num((CL[2040] / cv[2040] - 1) * 100, '+.0f')}% in 2040), because it includes
old-generation replacement; from 2047 it is lower ({K.num((CL[2050] / cv[2050] - 1) * 100, '+.0f')}% in 2050, {K.num((CL[2055] / cv[2055] - 1) * 100, '+.0f')}% in 2055); by 2066-2070
the replacement of post-2026 deliveries brings it back within a few percent. Before 2035 the two are not comparable: there the firm orders cover
your demand, while the last game delivered its firm backlog on top of its new demand.</p></div>
</div></section>

<section id="backlog"><h2>Firm orders: the first slice of your demand</h2><p class="lede">The game holds
{n0(FB["boeing"])} 737 MAX and {n0(FB["airbus"])} A320neo-family firm orders (Cirium, October 2026). Your table has its own old-generation
replacement ({k1(OLD_SUM)} aircraft), and part of the firm orders serves growth, so counting the firm orders on top of your demand would count
the same customers twice. In this game they are part of it.</p><div class="panel"><ul class="cav">
<li><b>Each year's demand is served first from the open firm orders,</b> split between the makers in proportion to what each has left
(about 39% Boeing, 61% Airbus). Only the rest is new customers, split by preference.</li>
<li><b>Deliveries follow your curve.</b> The firm orders last until {B_START}; from then all demand is new customers ({n0(OPT_B[B_START])} in {B_START}, then the whole curve).</li>
<li><b>Firm orders never switch maker or lapse.</b> If a maker cannot build its share in a year, those orders wait and do not draw on later demand again.</li>
<li><b>The alternative not used</b> (option A) kept the game's old approach: drop your old-generation column and deliver the firm orders on top of the rest,
as fast as the lines allow. It moves your old-generation demand forward to about 2033 and double counts the growth already in the backlog.</li>
</ul></div></section>

<section id="table"><h2>Year by year</h2><p class="lede">Aircraft a year. Bold years are your table's; the others are fitted.
The components, total and fleet are the whole single-aisle market; the last two columns are what the game uses (737/A320 class).</p>
<div class="panel">{year_table()}</div></section>

<section id="method"><h2>Method</h2><div class="panel"><ul class="cav">
<li><b>Fit.</b> For each component, the 2026-2070 path with the least squared second differences (the smoothest), counted over the whole range, including
where a component starts from or runs down to zero. It passes through your values in all eleven years, makes total demand match your four period totals
exactly, keeps every value at zero or above, and keeps the fleet (19.7k at end-2026 plus each year's growth) within ±50 aircraft of your fleet column (its
rounding; the largest gap is {n0(fl_dev)}). Solved exactly (active-set quadratic programme) and cross-checked with a general-purpose solver.</li>
<li><b>Zeros from your table.</b> Old-generation replacement is 0 from 2050 and post-2026 replacement is 0 to 2045, as in your table. Held at zero by the
non-negativity limit: {esc(", ".join(h.replace("max_neo_a220", "MAX/neo/A220").replace("post_2026", "post-2026") for h in held))}; post-2026 replacement first
appears in {first_post}.</li>
<li><b>Rounding.</b> Two of your totals are one above their parts (2045: 2,130 against 936 + 1,193; 2051: 1,957 against 934 + 1,022); the curve keeps the parts.</li>
<li><b>Class share.</b> Your table covers the whole single-aisle market, A220 included. The game models the 737/A320 market and applies its class share
({K.rnd(CS * 100, 2):.2f}%, from the Cirium fleet and order scope) once.</li>
<li><b>After 2070.</b> The game holds the 2070 values ({n0(TOT[2070])} a year). That matters only for a programme entering service in 2052 or later,
whose 20-year window runs past 2070.</li>
<li><b>Source.</b> dashgame/make_demand_conservative.py writes demand_conservative.json and asserts every check above; run dash-2050-cons uses it through
its sd_options.json.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_demand_page.py from dashgame/demand_conservative.json and dashgame/supply_demand.json.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "demand_curve.html"))
