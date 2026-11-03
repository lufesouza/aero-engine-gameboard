"""Build fps_cash_flows.html and data/fps_cash_flows_2030.csv: the year-by-year cash flows behind Boeing's 2030 fps
decision in the MAX phase-out game (data/cashflows.json, cashflows.py), and what changes at the margin that would flip
the decision (data/thresholds.json, thresholds.py). Every figure on the page comes from those files; the claims in the
copy are asserted below.

  python3 make_cashflows_html.py
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
CF = json.load(open(os.path.join(HERE, "data", "cashflows.json")))
TH = json.load(open(os.path.join(HERE, "data", "thresholds.json")))
PR = CF["params"]
DN = CF["plans"]["Do Nothing"]
PL = {"10-year at Renton": CF["plans"]["10-year at Renton"], "7-year at Renton": CF["plans"]["7-year at Renton"]}
YRS = [r["year"] for r in DN["rows"]]
DNY = {r["year"]: r for r in DN["rows"]}


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def num(v, dp=2):
    """A $B figure in a table cell: blank when zero."""
    if abs(v) < 0.5 * 10 ** -dp:
        return '<span class="muted">·</span>'
    return K.num(v, f"+.{dp}f")


def nw(s):
    return f'<span class="nw">{s}</span>'


# ─────────────────────────────── facts (asserted) ───────────────────────────────
MAX_UNIT = PR["max_price"] / 1000.0 * PR["max_margin"]
FPS_UNIT = PR["fps_price"] / 1000.0 * PR["fps_margin"]
assert abs(MAX_UNIT - 0.00384) < 1e-12 and abs(FPS_UNIT - 0.0141020) < 1e-9
DIFF = {}
for name, p in PL.items():
    ys = {r["year"]: r for r in p["rows"]}
    rows, cum = [], 0.0
    for y in YRS:
        a, d = ys[y], DNY[y]
        if a["fps_units"]:
            assert abs(a["fps_unit_profit"] - FPS_UNIT) < 1e-12
        net = a["net"] - d["net"]
        pv = a["pv"] - d["pv"]
        cum += pv
        rows.append({"year": y, "df": a["df"], "max": a["max_units"], "max_dn": d["max_units"], "fps": a["fps_units"],
                     "in_plan": a["in_window"], "in_dn": d["in_window"], "nb": a["nb_vs_sq"], "nb_dn": d["nb_vs_sq"],
                     "bill": a["bill"], "penalty": a["penalty"], "renton": a["renton"], "net": net, "pv": pv, "cum": cum,
                     "cash": a["cash_spend"], "cash_other": a["cash_other"], "debt": a["net_debt"], "debt_stress": a["net_debt_stress"],
                     "debt_dn": d["net_debt"], "debt_stress_dn": d["net_debt_stress"]})
    assert abs(cum - p["item_vs_dn"]) < 1e-9
    e = p["eis"]
    ey = next(r for r in rows if r["year"] == e)
    lump_pv = (ey["bill"] + ey["penalty"] + ey["renton"]) * ey["df"]
    after = sum((r["nb"] - (r["nb_dn"] if r["in_dn"] else 0.0)) * r["df"] if r["in_plan"] else -(r["nb_dn"] if r["in_dn"] else 0.0) * r["df"] for r in rows)
    assert abs(lump_pv + after - p["item_vs_dn"]) < 1e-9          # the lump (bill, penalty, Renton saving) and the profit
    uncounted = [(r["year"], r["fps"]) for r in rows if r["fps"] > 0.5 and not r["in_plan"]]
    DIFF[name] = {"rows": rows, "eis": e, "lump_pv": lump_pv, "after_pv": after, "uncounted": uncounted,
                  "window_end": p["window_end"], "bill": p["bill"], "penalty_nom": ey["penalty"], "renton": ey["renton"],
                  "launch": p["launch"]}
D10, D7 = DIFF["10-year at Renton"], DIFF["7-year at Renton"]
assert D10["eis"] == 2040 and D7["eis"] == 2037 and D10["window_end"] == 2059 and D7["window_end"] == 2056 and DN["window_end"] == 2060
assert all(r["max"] <= r["max_dn"] + 1e-6 for r in D10["rows"])      # the fps line at Renton takes over the MAX lines
DIP = [r for r in D10["rows"] if r["year"] >= D10["eis"] and r["max"] + r["fps"] < r["max_dn"] - 50]
assert DIP and DIP[-1]["year"] <= 2043
# what the decision's margin threshold (2030, the CEO's normal rule) does to the same flows: exact, linear in the margin
R30 = TH["rounds"]["1"]
M_RULE = R30["rule"]["margin"]
PP = R30["per_point"]
UP = {name: (M_RULE - PR["fps_margin"]) * 100 * PP[name] for name in PL}
RE_S2 = TH["rounds"]["1"]["rows"]["Re-engine"]["items"][1]
PAIR_S2 = TH["rounds"]["1"]["rows"]["10-year at Renton + Re-engine"]["items"][1] + UP["10-year at Renton"]
SEVEN_S2 = PL["7-year at Renton"]["item_vs_dn"] + UP["7-year at Renton"]
assert PAIR_S2 - RE_S2 > 1.0 - 1e-6 and 0 < PAIR_S2 - SEVEN_S2 < 1.0 and SEVEN_S2 - RE_S2 < 1.0
# net debt: back to $0 before either fps spends, and held there
for name in PL:
    rr = DIFF[name]["rows"]
    z_base = min(r["year"] for r in rr if r["debt"] is not None and r["debt"] < 1e-9)
    z_str = min(r["year"] for r in rr if r["debt_stress"] is not None and r["debt_stress"] < 1e-9)
    assert z_base == 2029 and z_str == 2030 and all((r["debt_stress"] or 0) < 1e-9 for r in rr if r["year"] >= z_str)
Z_BASE, Z_STR = 2029, 2030
for name in PL:
    q = sum(r["fps"] * r["df"] for r in DIFF[name]["rows"] if r["in_plan"])        # discounted fps deliveries counted
    assert abs(q * PR["fps_price"] / 1000.0 / 100.0 - PP[name]) < 1e-9


# ─────────────────────────────── charts and tables ───────────────────────────────
def cum_chart():
    w, h, left, right, top, bot = 760, 300, 60, 150, 20, 44
    lo, hi = -30.0, 5.0
    ys = [y for y in YRS if 2030 <= y <= 2061]
    pad = 24
    sx = lambda y: left + pad + (y - ys[0]) / (ys[-1] - ys[0]) * (w - left - right - pad)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "Cumulative present value of the fps against Do Nothing, 2030 brief")]
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="{"zero" if v == 0 else "grid"}"/><text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{bp(v, 0, False)}</text>')
        v += 5.0
    for y in ys:
        if y % 5 == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    for name, col, dash in (("10-year at Renton", "var(--s1)", ""), ("7-year at Renton", "var(--s2)", ' stroke-dasharray="6 4"')):
        rows = [r for r in DIFF[name]["rows"] if r["year"] in ys]
        d = "M" + " L".join(f"{sx(r['year']):.1f},{sy(r['cum']):.1f}" for r in rows)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
        for r in rows:
            out.append(f'<circle cx="{sx(r["year"]):.1f}" cy="{sy(r["cum"]):.1f}" r="7" fill="transparent" class="hit" '
                       f'{K.mark_attrs((str(r["year"]), "", None), (bp(r["cum"]), name + ", cumulative PV", col), (bp(r["pv"]), "this year, PV", None))}/>')
        last = rows[-1]
        out.append(f'<text x="{w - right + 8}" y="{sy(last["cum"]) + (4 if name.startswith("10") else 18):.1f}" class="endlab">{esc(name.split(" at")[0])} {bp(last["cum"])}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">Running total of present values against Do Nothing, $B at 2026</text></svg>')
    return "".join(out)


def bars_chart(name):
    rows = [r for r in DIFF[name]["rows"] if 2030 <= r["year"] <= 2061]
    w, h, left, right, top, bot = 760, 260, 60, 16, 20, 44
    lo, hi = -80.0, 20.0
    bw = (w - left - right) / len(rows)
    sx = lambda y: left + (y - rows[0]["year"] + 0.5) * bw
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, f"Yearly cash flow of the {name} fps against Do Nothing, 2030 brief")]
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="{"zero" if v == 0 else "grid"}"/><text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{bp(v, 0, False)}</text>')
        v += 20.0
    for r in rows:
        x = sx(r["year"])
        if abs(r["net"]) > 1e-6:
            col = "var(--s1)" if r["net"] > 0 else "var(--neg)"
            out.append(f'<path d="{K.bar_path(x - bw * 0.36, bw * 0.72, sy(0), sy(r["net"]))}" fill="{col}"/>')
        tip = [(str(r["year"]), "", None), (bp(r["net"]), "cash flow against Do Nothing", None)]
        if r["bill"]:
            tip += [(bp(r["bill"]), "fps bill, booked at entry into service", None), (bp(r["penalty"]), "debt penalty", None), (bp(r["renton"]), "Renton saving", None)]
        tip += [(bp(r["nb"] - r["nb_dn"]), "narrowbody profit gained", None), (f"{r['df']:.3f}", "discount factor", None), (bp(r["pv"]), "present value", None)]
        if r["fps"] > 0.5 and not r["in_plan"]:
            tip.append((n0(r["fps"]), "fps delivered, not counted (after the 20-year window)", None))
        out.append(f'<rect x="{x - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" {K.mark_attrs(*tip)}/>')
        if r["year"] % 5 == 0:
            out.append(f'<text x="{x:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{r["year"]}</text>')
    e = next(r for r in rows if r["year"] == DIFF[name]["eis"])
    out.append(f'<text x="{sx(e["year"]) + bw * 0.8:.1f}" y="{sy(-45):.1f}" class="ann">{bp(e["net"], 1)} in {e["year"]}: the bill, its debt penalty</text>')
    out.append(f'<text x="{sx(e["year"]) + bw * 0.8:.1f}" y="{sy(-45) + 16:.1f}" class="ann">and the Renton saving</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">$B a year, constant 2026 dollars, before discounting</text></svg>')
    return "".join(out)


def bridge_table():
    head = ["Present value at 2026, $B", "Do Nothing", "10-year at Renton", "7-year at Renton"]
    lines = (("Narrowbody profit against the status quo", lambda p: p["bridge"]["nb_profit_vs_sq"] + p["bridge"]["supply_demand"]),
             ("Renton saving (new-site capex avoided)", lambda p: p["bridge"]["supply_plan"]),
             ("fps bill", lambda p: p["bridge"]["programme_investment"]),
             ("Debt penalty", lambda p: p["bridge"]["debt_penalty"]))
    plans = [DN, PL["10-year at Renton"], PL["7-year at Renton"]]
    for p in plans:
        assert abs(sum(f(p) for _, f in lines) - p["pv"]) < 1e-9
    rows = [[lab] + [b(f(p)) for p in plans] for lab, f in lines]
    rows.append(["<b>Value against the status quo</b>"] + [f"<b>{b(p['pv'])}</b>" for p in plans])
    rows.append(["<b>fps against Do Nothing (the brief's item)</b>", ""] + [f"<b>{b(p['item_vs_dn'])}</b>" for p in plans[1:]])
    return K.table(head, rows, num_cols=(1, 2, 3))


def year_table(name):
    d = DIFF[name]
    head = ["Year", "737 MAX delivered", "fps delivered", "Narrowbody profit vs status quo", "Do Nothing's", "fps bill", "Debt penalty",
            "Renton saving", "Cash flow vs Do Nothing", "Discount factor", "Present value", "Cumulative"]
    rows = []
    for r in d["rows"]:
        if r["year"] < 2030:
            continue
        cnt = "" if r["in_plan"] else ' <span class="muted small">(not counted)</span>'
        rows.append([str(r["year"]), f'{n0(r["max"])} <span class="muted">({n0(r["max_dn"])})</span>', n0(r["fps"]) + cnt,
                     num(r["nb"]) if r["in_plan"] else '<span class="muted">–</span>', num(r["nb_dn"]) if r["in_dn"] else '<span class="muted">–</span>',
                     num(r["bill"]), num(r["penalty"]), num(r["renton"]), num(r["net"]), f'{r["df"]:.3f}', num(r["pv"], 3), num(r["cum"])])
    return K.table(head, rows, num_cols=tuple(range(1, 12)))


def cash_table():
    head = ["Year", "10-year: development spend", "Renton saving (cash)", "Net debt, base", "Net debt, stress", "7-year: development spend",
            "Renton saving (cash)", "Net debt, base", "Net debt, stress"]
    rows = []
    r10 = {r["year"]: r for r in D10["rows"]}
    r7 = {r["year"]: r for r in D7["rows"]}
    debt = lambda v: '<span class="muted">\u2013</span>' if v is None else ('<span class="muted">0</span>' if v < 0.05 else f"{v:.1f}")
    yrs = [y for y in range(2026, 2061) if any(abs(r[y][k] or 0.0) > 1e-9 for r in (r10, r7) for k in ("cash", "cash_other", "debt", "debt_stress"))]
    for y in range(min(yrs), max(yrs) + 1):
        a, c = r10[y], r7[y]
        rows.append([str(y), num(-a["cash"]), num(-a["cash_other"]), debt(a["debt"]), debt(a["debt_stress"]),
                     num(-c["cash"]), num(-c["cash_other"]), debt(c["debt"]), debt(c["debt_stress"])])
    return K.table(head, rows, num_cols=tuple(range(1, 9)))


def write_csv(path):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["plan", "year", "counted_in_window", "max_delivered", "fps_delivered", "max_profit_per_aircraft_musd", "fps_profit_per_aircraft_musd",
                     "narrowbody_profit_vs_status_quo_busd", "fps_bill_busd", "debt_penalty_busd", "renton_saving_busd", "net_vs_status_quo_busd",
                     "discount_factor", "present_value_busd", "dev_spend_cash_view_busd", "renton_saving_cash_view_busd", "net_debt_base_busd",
                     "net_debt_stress_busd"])
        for name, p in [("Do Nothing", DN)] + list(PL.items()):
            for r in p["rows"]:
                wr.writerow([name, r["year"], int(bool(r["in_window"])), round(r["max_units"], 3), round(r["fps_units"], 3),
                             round(r["max_unit_profit"] * 1000, 4), round(r["fps_unit_profit"] * 1000, 4), round(r["nb_vs_sq"], 6),
                             round(r["bill"], 6), round(r["penalty"], 6), round(r["renton"], 6), round(r["net"], 6), round(r["df"], 6),
                             round(r["pv"], 6), round(-r["cash_spend"], 6), round(-r["cash_other"], 6),
                             "" if r["net_debt"] is None else round(r["net_debt"], 4), "" if r["net_debt_stress"] is None else round(r["net_debt_stress"], 4)])


CSS_EXTRA = """
.legend .dash2 { display: inline-block; width: 18px; height: 0; border-top: 2px dashed var(--s2); vertical-align: middle; margin-right: 6px; }
.legend .solid1 { display: inline-block; width: 18px; height: 0; border-top: 2px solid var(--s1); vertical-align: middle; margin-right: 6px; }
.chart .zero { stroke: var(--faint); stroke-width: 1; }
.chart .ann { fill: var(--fg); font: 500 12px var(--font-body); }
.scroll { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.scroll > table { background: transparent; }
ul.cav li, footer { overflow-wrap: anywhere; }
"""


def build(out_path, csv_path):
    p10, p7 = PL["10-year at Renton"], PL["7-year at Renton"]
    tiles = [("737 MAX, per aircraft", f"${MAX_UNIT * 1000:.2f}M", f"profit: ${PR['max_price']:.0f}M price at {K.rnd(100 * PR['max_margin'], 0):.0f}% margin."),
             ("fps, per aircraft", f"${FPS_UNIT * 1000:.2f}M", f"profit: ${PR['fps_price']:.0f}M price at {K.rnd(100 * PR['fps_margin'], 2):.2f}% margin."),
             ("10-year fps at Renton", bp(p10["item_vs_dn"]), f"against Do Nothing: the bill in {D10['eis']}, with its debt penalty and the Renton saving, costs {bp(D10['lump_pv'], 1)} today; the extra profit recovers {bp(D10['after_pv'], 1)}."),
             ("7-year fps at Renton", bp(p7["item_vs_dn"]), f"against Do Nothing: the bill in {D7['eis']}, with its debt penalty and the Renton saving, costs {bp(D7['lump_pv'], 1)} today; the extra profit recovers {bp(D7['after_pv'], 1)}.")]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    unc10 = D10["uncounted"]
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>fps Cash Flows</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · MAX phase-out world · BOEING PROPRIETARY</p>
<h1>The fps cash flows behind Boeing's 2030 decision</h1>
<p class="lede">What Boeing's 2030 brief counts for the fps, year by year, in the column the CEO expected ({esc(CF["column"])}). Every figure is in constant 2026 dollars,
pre-tax, and measured against the status quo in which nobody launches anything. The brief discounts each year to 2026 at Boeing's {K.rnd(100 * PR["wacc"], 1):.1f}% cost of capital.
The discounted totals below are the brief's own values, to the cent.</p>
<p class="gloss"><b>What is counted.</b> Narrowbody operating profit: 737 MAX delivered times its profit per aircraft, plus fps delivered times the fps's, less the status quo's MAX deliveries
times the MAX profit. The fps's sales count for 20 years from its entry into service ({D10["eis"]}-{D10["window_end"]} for the 10-year, {D7["eis"]}-{D7["window_end"]} for the 7-year), and Do Nothing's to {DN["window_end"]}.
The fps bill is booked as one lump in its entry-into-service year, with the dashboard's debt penalty for the extra debt it implies. Building at Renton avoids new-site capex, booked in the same year.
No widebody change: no plan here re-engines the 787. <b>Not counted:</b> tax, working capital, and anything after the 20-year window.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>How the value builds up</h2><div class="stack">
<div class="panel"><p class="ctitle">The bill lands in one year at full weight; the profit arrives over the next two decades, heavily discounted</p>
<div class="legend"><span><i class="solid1"></i>10-year at Renton</span><span><i class="dash2"></i>7-year at Renton</span></div>
<div class="cw">{cum_chart()}</div>
<p class="cap">The running total of present values against Do Nothing. Nothing differs until the fps enters service. Then the bill, booked in that one year, drops the 10-year
to {bp(D10["lump_pv"], 1)} and the 7-year to {bp(D7["lump_pv"], 1)} in today's money. Profit in later years climbs back, but a dollar in 2050 is worth only
{K.rnd(next(r["df"] for r in D10["rows"] if r["year"] == 2050) * 100, 0):.0f} cents today, and neither line gets back to zero.</p></div>
<div class="panel">{bridge_table()}
<p class="cap">The same totals by line. Narrowbody profit includes the supply-and-demand adjustment the game makes to the board's own estimate. The debt penalty is the dashboard's charge for
the extra debt the bill implies: {bp(D10["penalty_nom"], 1)} for the 10-year and {bp(D7["penalty_nom"], 1)} for the 7-year, in money of the entry-into-service year.</p></div>
</div></section>

<section><h2>Year by year: the 10-year fps at Renton</h2><div class="stack">
<div class="panel"><p class="ctitle">One {bp(next(r["net"] for r in D10["rows"] if r["year"] == D10["eis"]), 1)} year, then, once the fps has ramped up, about $6-10B a year of extra profit</p><div class="cw">{bars_chart("10-year at Renton")}</div>
<p class="cap">Cash flow against Do Nothing each year, before discounting. In {D10["eis"]}-{DIP[-1]["year"]} Boeing delivers fewer aircraft than with Do Nothing: building the fps at Renton converts the
MAX lines while the fps is still ramping up. Sales after {D10["window_end"]} ({", ".join(f"{n0(u)} in {y}" for y, u in unc10[:2])}) are not counted.</p></div>
<div class="panel">{year_table("10-year at Renton")}
<p class="cap">$B, constant 2026 dollars; MAX delivered with Do Nothing in brackets. A dash means the year is outside the plan's counted window.</p></div>
</div></section>

<section><h2>Year by year: the 7-year fps at Renton</h2><div class="stack">
<div class="panel"><div class="cw">{bars_chart("7-year at Renton")}</div></div>
<div class="panel">{year_table("7-year at Renton")}
<p class="cap">The 7-year enters service three years earlier, so its bill is booked earlier and costs more today, and its counted window ends in {D7["window_end"]}.</p></div>
</div></section>

<section><h2>The cash view Boeing's net-debt test uses</h2><div class="panel">{cash_table()}
<p class="cap">For the net-debt test (not the value), the brief spreads the same bill over the development years on the game's phasing curve: 5% in the first year of ten, peaking at 14% in the seventh.
The Renton saving is spread over the years the new site would have been built. Net debt is the GM's balance-sheet tracker in constant 2026 $B: base case, and the stress case with free cash flow
one-third lower. Net debt is back to $0 by {Z_BASE} in the base case and {Z_STR} in the stress case, before either fps spends, and both plans keep it there.</p></div></section>

<section><h2>What would flip the decision, in these terms</h2><div class="panel">
<p>Margin works on every fps delivered in the counted window. At the {K.rnd(100 * M_RULE, 1):.1f}% margin that makes an fps Boeing's 2030 decision under the CEO's normal rule, each fps earns
{nw(f"${PR['fps_price'] * M_RULE:.1f}M")} instead of {nw(f"${FPS_UNIT * 1000:.1f}M")}. That adds {bp(UP["10-year at Renton"])} to the 10-year (to {bp(p10["item_vs_dn"] + UP["10-year at Renton"])})
and {bp(UP["7-year at Renton"])} to the 7-year (to {bp(p7["item_vs_dn"] + UP["7-year at Renton"])}) against Do Nothing. At that margin the 10-year beside the 787 Re-engine ({bp(PAIR_S2)}) leads the Re-engine alone ({bp(RE_S2)}),
the CEO's other pick that year, by more than the CEO's $1B margin, and the 7-year at Renton ({bp(SEVEN_S2)}) is the smaller plan within $1B of it, so the CEO takes the 7-year
(see the main report). Each point of margin is worth {b(PP["10-year at Renton"], 2, False)} for the 10-year and {b(PP["7-year at Renton"], 2, False)} for the 7-year.</p></div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Source:</b> cashflows.py (data/cashflows.json) re-values each plan from the state the 2030 round started in, and checks that the discounted flows equal the brief's value of each plan and the fps-against-Do-Nothing items, to the cent. The year-by-year rows are in fps_cash_flows_2030.csv.</li>
<li><b>Status quo:</b> nobody launches anything, so the values compare each plan with the same baseline; the fps against Do Nothing is the difference. In this world the MAX phases out from 2045 in every plan, the status quo included.</li>
<li><b>Discounting:</b> each year at {K.rnd(100 * PR["wacc"], 1):.1f}% to 2026; the bill and its debt penalty at the entry-into-service year, as the dashboard books them. A bill spent through the development years would cost more in today's money.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_cashflows_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    write_csv(csv_path)
    print("wrote", out_path, len(page), "and", csv_path)


if __name__ == "__main__":
    build(os.path.join(HERE, "fps_cash_flows.html"), os.path.join(HERE, "data", "fps_cash_flows_2030.csv"))
