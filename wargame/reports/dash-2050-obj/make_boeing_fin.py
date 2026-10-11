"""Boeing's financials in the dash-2050-obj game, in detail: boeing_financials.html (BOEING PROPRIETARY).

Data: data/boeing_fin.json (make_boeing_fin_data.py) and data/report_data.json. Two bases, never mixed in one chart:
  - the dashboard's P&L and value: Boeing's new-airplane business as the board models it, at unescalated 2026 prices,
    and ΔPV at 2026 (WACC 10.5%);
  - the GM's balance-sheet tracker: Boeing's whole-company net debt and free cash flow in 2026 dollars, the analysts'
    consensus plus the game's changes (finance.py).

  python3 make_boeing_fin.py [out.html]
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402

esc = K.esc
BF = json.load(open(os.path.join(HERE, "data", "boeing_fin.json")))
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
PL = BF["pl"]
YRS = [r["year"] for r in PL]
CASH = BF["cash"]
BASE, STRESS = CASH["base"], CASH["stress"]
ALTS = {a["plan"]: a for a in BF["alts"]}
PLAY = ALTS["fps 10-yr + 787: hold"]
HOLD = ALTS["fps: hold + 787: hold"]
INP = BF["inputs"]
V = BF["value"]
RY = [2030, 2035, 2045, 2050]
PY = {r["year"]: r for r in PL}
BY = {r["year"]: r for r in BASE}
SY = {r["year"]: r for r in STRESS}


def b(v, dp=2, sign=False):
    return K.usd(v, dp, sign)


def f1(v):
    return K.num(v, ".1f")


def f2(v):
    return K.num(v, ".2f")


def pct(v, dp=0):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def cum(xs):
    return list(itertools.accumulate(xs))


# ─────────────────────────────── derived figures (all checked below) ───────────────────────────────
OWN_PLAY = cum(PLAY["owners"])
OWN_HOLD = cum(HOLD["owners"])
OWN_NOGAME = cum(CASH["owners_noprog"])
CYRS = [r["year"] for r in PLAY["rows"]]
PAYBACK = next(y for y, a, h in zip(CYRS, OWN_PLAY, OWN_HOLD) if y > 2030 and a >= h)
O50 = {k: s[CYRS.index(2050)] for k, s in (("play", OWN_PLAY), ("hold", OWN_HOLD), ("nogame", OWN_NOGAME))}
O60 = {k: s[-1] for k, s in (("play", OWN_PLAY), ("hold", OWN_HOLD), ("nogame", OWN_NOGAME))}
SPEND = {r["year"]: r["spend"] for r in BASE}
PEAK_Y = max(SPEND, key=SPEND.get)
MIN_STRESS = min((r["fcf"], r["year"]) for r in STRESS if r["year"] >= 2030)
MIN_BASE = min((r["fcf"], r["year"]) for r in BASE if r["year"] >= 2030)
assert abs(sum(SPEND.values()) - 60.32) < 1e-6 and PEAK_Y == 2036
assert abs(PLAY["pv"] - V["pv_delta"]) < 1e-9
assert BY[2029]["debt"] == 0 and SY[2029]["debt"] > 0 and SY[2030]["debt"] == 0
assert all(r["debt"] == 0 for r in BASE if r["year"] >= 2029) and all(r["debt"] == 0 for r in STRESS if r["year"] >= 2030)
PEN = lambda d_: d_ * BF["params"]["v_alpha"] * (d_ / V["ev"]) ** 2          # the board's debt penalty (undiscounted)
PEN_UNDISC = PEN(BF["params"]["v_debt_boeing"] + 60.32) - PEN(BF["params"]["v_debt_boeing"])


# ─────────────────────────────── charts ───────────────────────────────
def spread(values, y_lo, y_hi, gap=18, plot_h=274, floor=14):
    pos = [(y_hi - v) / (y_hi - y_lo) * plot_h for v in values]
    order = sorted(range(len(values)), key=lambda i: pos[i])
    placed, last = {}, None
    for i in order:
        p = pos[i] if last is None else max(pos[i], last + gap)
        placed[i] = p
        last = p
    limit = plot_h - floor
    for i in reversed(order):
        if placed[i] > limit:
            placed[i] = limit
        limit = placed[i] - gap
    return [placed[i] - pos[i] for i in range(len(values))]


def stack_bars(years, stacks, lines, y_hi, y_step, label, aria, fmt="{:.2f}", unit="$B", notes=(), tip_fn=None, end_names=None):
    """Stacked columns, one per year (2px surface gap between segments), plus lines on the same axis.
    stacks: [(name, css var, values)]; lines: [(name, css var, values, dashed)]. Each year is one focusable hover target
    (tip_fn(i) gives its tooltip rows; default: the stacks, their total and the lines)."""
    w, h, left, right, top, bot = 760, 340, 52, 150, 26, 46
    x_lo, x_hi = years[0] - 0.6, years[-1] + 0.6
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / y_hi * (h - top - bot)
    step = sx(1) - sx(0)
    bw = step * 0.72
    out = [K.svg_open(w, h, aria)]
    t = 0
    while t <= y_hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t:g}</text>')
        t += y_step
    for yr in range(2030, years[-1] + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    for xv, txt in notes:
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 4:.1f}" y="{top + 11}" class="ann">{esc(txt)}</text>')
    for i, yr in enumerate(years):
        x0 = sx(yr) - bw / 2
        base = 0.0
        segs = [(n, c, vals[i]) for n, c, vals in stacks if vals[i] > 1e-9]
        for j, (n, c, v) in enumerate(segs):
            y0, y1 = sy(base), sy(base + v)
            if j > 0:
                y0 -= 1                                    # 2px surface gap: 1px off each side of the joint
            if j < len(segs) - 1:
                y1 += 1
            r = 2 if j == len(segs) - 1 else 0
            if y0 - y1 > 0.5:
                out.append(f'<path d="{K.bar_path(x0, bw, y0, y1, r)}" fill="var(--{c})"/>')
            base += v
    for name, c, vals, dashed in lines:
        d = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in zip(years, vals))
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        out.append(f'<path d="{d}" fill="none" stroke="var(--{c})" stroke-width="2" stroke-linejoin="round"{dash} pointer-events="none"/>')
    for i, yr in enumerate(years):
        if tip_fn:
            rows = tip_fn(i)
        else:
            rows = [(fmt.format(vals[i]) + " " + unit, n, f"var(--{c})") for n, c, vals in stacks]
            if len(stacks) > 1:
                rows.append((fmt.format(sum(vals[i] for _, _, vals in stacks)) + " " + unit, "Total", None))
            rows += [(fmt.format(vals[i]) + " " + unit, n, f"var(--{c})") for n, c, vals, _ in lines]
        out.append(f'<rect x="{sx(yr) - step / 2:.1f}" y="{top}" width="{step:.1f}" height="{h - top - bot}" fill="transparent" '
                   f'class="hit" {K.mark_attrs((str(yr), "", None), *rows)}/>')
    last, acc = [], 0.0
    names = end_names or {}
    for n, c, vals in stacks:
        last.append((names.get(n, n), acc + vals[-1] / 2, vals[-1]))
        acc += vals[-1]
    for n, c, vals, _ in lines:
        last.append((names.get(n, n), vals[-1], vals[-1]))
    dys = spread([v for _, v, _ in last], 0, y_hi, gap=16, plot_h=h - top - bot)
    for (n, v, val), dy in zip(last, dys):
        if not n:
            continue
        out.append(f'<text x="{w - right + 8}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(n)} {fmt.format(val)}</text>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">{esc(label)}</text></svg>')
    return f'<div class="cw">{"".join(out)}</div>'


def legend(items):
    return '<div class="legend">' + "".join(
        f'<span><i class="{kind}" style="background:var(--{c})"></i>{esc(n)}</span>' for n, c, kind in items) + "</div>"


def chart_revenue():
    nb = [r["nb_revenue"] for r in PL]
    wb = [r["wb_revenue"] for r in PL]
    svg = stack_bars(YRS, [("Narrowbody", "s1", nb), ("Widebody", "s3", wb)], [("Status quo", "sq", [r["sq_revenue"] for r in PL], True)],
                     80, 20, "Revenue, $B a year at 2026 prices (the dashboard's new-airplane business)",
                     "Boeing revenue by year: narrowbody and widebody, with the status quo", fmt="{:.1f}",
                     notes=[(y, f"R{i + 1}") for i, y in enumerate(RY)])
    return legend([("Narrowbody", "s1", "sq"), ("Widebody", "s3", "sq"), ("Status quo (nobody launches)", "sq", "ln")]) + svg


def chart_profit():
    nb = [r["nb_profit"] for r in PL]
    wb = [r["wb_profit"] for r in PL]

    def tip_fn(i):
        r = PL[i]
        rows = [(f'{r["nb_profit"]:.2f} $B', "Narrowbody", "var(--s1)"), (f'{r["wb_profit"]:.2f} $B', "Widebody", "var(--s3)"),
                (f'{r["profit"]:.3f} $B', "Total", None), (f'{r["sq_profit"]:.3f} $B', "Status quo", "var(--sq)"),
                (K.num(r["vs_sq"]) + " $B", "vs status quo", None)]
        if r["nonrecurring"]:
            rows.append((f'{r["nonrecurring"]:.2f} $B', "fps bill booked this year (outside operating profit)", None))
        return rows
    svg = stack_bars(YRS, [("Narrowbody", "s1", nb), ("Widebody", "s3", wb)], [("Status quo", "sq", [r["sq_profit"] for r in PL], True)],
                     20, 5, "Operating profit, $B a year at 2026 prices", "Boeing operating profit by year: narrowbody and widebody, "
                     "with the status quo", notes=[(y, f"R{i + 1}") for i, y in enumerate(RY)], tip_fn=tip_fn)
    return legend([("Narrowbody", "s1", "sq"), ("Widebody", "s3", "sq"), ("Status quo", "sq", "ln")]) + svg


def chart_cash():
    yrs = [r["year"] for r in BASE]

    def tip_fn(i):
        r, s_ = BASE[i], STRESS[i]
        return [(f"{r['spend']:.2f} $B", "fps programme cash", "var(--pos)"), (f"{r['fcf']:.2f} $B", "Free cash flow, base", "var(--s1)"),
                (f"{s_['fcf']:.2f} $B", "Free cash flow, stress", "var(--s2)"),
                (f"{r['debt']:.2f} / {s_['debt']:.2f} $B", "Net debt, base / stress", None)]
    svg = stack_bars(yrs, [("fps cash", "pos", [r["spend"] for r in BASE])],
                     [("Base FCF", "s1", [r["fcf"] for r in BASE], False), ("Stress FCF", "s2", [r["fcf"] for r in STRESS], False)],
                     25, 5, "$B a year, 2026 dollars (whole company, the GM's tracker)",
                     "Boeing fps programme cash and free cash flow by year, base and stress", fmt="{:.1f}", tip_fn=tip_fn,
                     end_names={"fps cash": ""},
                     notes=[(2030, "R1"), (2035, "R2"), (2045, "R3"), (2050, "R4")])
    return (legend([("fps programme cash", "pos", "sq"), ("Free cash flow, base case", "s1", "ln"),
                    ("Free cash flow, stress case (consensus cash flow one-third lower)", "s2", "ln")]) + svg)


def chart_debt():
    rows = [r for r in BASE if r["year"] <= 2040]
    st = [r for r in STRESS if r["year"] <= 2040]
    series = [("Base case", "s1", [(2026, INP["start_debt_b"])] + [(r["year"], r["debt"]) for r in rows]),
              ("Stress case", "s2", [(2026, INP["start_debt_b"])] + [(r["year"], r["debt"]) for r in st]),
              ("No new programme", "sq", [(2026, INP["start_debt_b"])] + [(r["year"], r["debt_no_programme"]) for r in rows])]
    svg = K.line_chart(series, -5, 25, 5, "int", "Net debt at year end, $B, 2026 dollars (2026-2040)",
                       refs=[(0, "historical level", "below")], aria_label="Boeing net debt by year, 2026 to 2040: base, stress, no new programme",
                       end_labels=[(-10, "All three: $0"), (0, ""), (0, "")], notes=[(2030, "R1"), (2035, "R2")], x_lo=2026, x_hi=2040)
    return (legend([("Base case", "s1", "ln"), ("Stress case", "s2", "ln"), ("No new programme (analysts' path)", "sq", "ln")])
            + f'<div class="cw">{svg}</div>')


def chart_owners():
    series = [("fps 10-year (played)", "s1", list(zip(CYRS, OWN_PLAY))), ("Do Nothing (no fps)", "s2", list(zip(CYRS, OWN_HOLD))),
              ("No game (analysts' path)", "sq", list(zip(CYRS, OWN_NOGAME)))]
    last = [OWN_PLAY[-1], OWN_HOLD[-1], OWN_NOGAME[-1]]
    labels = [f"Played {last[0]:.0f}", f"Do Nothing {last[1]:.0f}", f"No game {last[2]:.0f}"]
    ends = list(zip(spread(last, 0, 600), labels))
    svg = K.line_chart(series, 0, 600, 100, "int", "Cumulative cash to owners from 2027, $B, 2026 dollars, undiscounted",
                       refs=[], aria_label="Cumulative cash to Boeing's owners: the played fps, Do Nothing, and the analysts' path",
                       end_labels=ends, notes=[(PAYBACK, f"fps pays back {PAYBACK}")], x_lo=2026, x_hi=2060)
    return (legend([("fps 10-year, as played", "s1", "ln"), ("Do Nothing: no fps, Airbus launches NGSA", "s2", "ln"),
                    ("No game: the analysts' cash flow, nobody launches", "sq", "ln")]) + f'<div class="cw">{svg}</div>')


def chart_bridge():
    items = [("NB profit vs status quo", V["bridge"]["nb_profit_vs_sq"]), ("fps bill ($60.32B, 2040)", V["bridge"]["programme_investment"]),
             ("Debt penalty", V["bridge"]["debt_penalty"]), ("ΔPV", V["pv_delta"])]
    w, left, right, top, row = 760, 260, 90, 18, 40
    h = top + row * len(items) + 34
    lo, hi = -5, 25
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "Boeing ΔPV bridge, PV at 2026")]
    for t in range(lo, hi + 1, 5):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 6}" y2="{h - 30}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 12}" text-anchor="middle" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
    run = 0.0
    for i, (n, v) in enumerate(items):
        y = top + i * row
        total = i == len(items) - 1
        x0, x1 = (sx(0), sx(v)) if total else (sx(run), sx(run + v))
        cls = "pos" if total else ("t41" if v >= 0 else "neg")
        out.append(f'<text x="{left - 12}" y="{y + 20}" text-anchor="end" class="rowlab sm">{esc(n)}</text>')
        out.append(f'<path d="{K.hbar_path(x0, x1 if abs(x1 - x0) > 2 else x0 + 2, y + 6, 22)}" class="b {cls}" '
                   f'{K.mark_attrs((K.num(v) + " $B", n, None))}/>')
        out.append(f'<text x="{max(x0, x1) + 6:.1f}" y="{y + 21}" class="val sm">{K.num(v)}</text>')
        if not total:
            run += v
    out.append("</svg>")
    return f'<div class="cw">{"".join(out)}</div>'


# ─────────────────────────────── tables ───────────────────────────────
def pl_table():
    rows = []
    for r in PL:
        rows.append([str(r["year"]), pct(r["nb_share"]), f'{r["nb_units"]:,.0f}', f'{r["nb_price"]:.0f}', pct(r["nb_margin"], 1),
                     f'{r["nb_revenue"]:.2f}', f'{r["nb_profit"]:.2f}', f'{r["wb_units"]:,.0f}', f'{r["wb_revenue"]:.2f}', f'{r["wb_profit"]:.2f}',
                     f'{r["revenue"]:.2f}', f'{r["profit"]:.2f}', f'{r["sq_profit"]:.2f}', f2(r["vs_sq"]),
                     (f'{r["nonrecurring"]:.2f}' if r["nonrecurring"] else "—")])
    return K.tview("Boeing P&L by year (the dashboard, 2026 prices)",
                   ["Year", "NB share", "NB deliveries", "NB price $M", "NB margin", "NB revenue $B", "NB profit $B", "WB deliveries",
                    "WB revenue $B", "WB profit $B", "Revenue $B", "Operating profit $B", "Status-quo profit $B", "vs status quo $B",
                    "fps bill booked $B"], rows)


def periods_table():
    rows = [[p["period"], f'{p["nb_units"]:,.0f}', f'{p["wb_units"]:,.0f}', f'{p["revenue"]:,.1f}', f'{p["profit"]:,.1f}',
             f'{p["sq_profit"]:,.1f}', f2(p["profit"] - p["sq_profit"]), (f'{p["nonrecurring"]:.1f}' if p["nonrecurring"] else "—")]
            for p in BF["periods"]]
    t = [sum(p[k] for p in BF["periods"]) for k in ("nb_units", "wb_units", "revenue", "profit", "sq_profit", "nonrecurring")]
    rows.append(["<b class=nw>2026-2060</b>", f"<b>{t[0]:,.0f}</b>", f"<b>{t[1]:,.0f}</b>", f"<b>{t[2]:,.1f}</b>", f"<b>{t[3]:,.1f}</b>",
                 f"<b>{t[4]:,.1f}</b>", f"<b>{f2(t[3] - t[4])}</b>", f"<b>{t[5]:.1f}</b>"])
    return K.table(["Period", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B", "Status-quo profit $B",
                    "vs status quo $B", "fps bill booked $B"], rows, num_cols=tuple(range(1, 8)))


def cash_table():
    rows = []
    for r, s, ob, os_, on in zip(BASE, STRESS, CASH["owners_base"], CASH["owners_stress"], CASH["owners_noprog"]):
        tax = (1 - INP["tax_rate"]) * (r["profit_vs_baseline"] - r["spend"])
        rows.append([str(r["year"]), f'{r["base_fcf"]:.2f}', f2(r["profit_vs_baseline"]), (f'{r["spend"]:.2f}' if r["spend"] else "—"),
                     f2(tax), (f'{r["interest"]:.2f}' if r["interest"] else "—"), f'{r["fcf"]:.2f}', f'{r["debt"]:.2f}', f'{ob:.2f}',
                     f'{s["base_fcf"]:.2f}', f'{s["fcf"]:.2f}', f'{s["debt"]:.2f}', f'{os_:.2f}', f'{r["debt_no_programme"]:.2f}', f'{on:.2f}'])
    return K.tview("Boeing cash and net debt by year (the GM's tracker, 2026 dollars)",
                   ["Year", "Base FCF (consensus)", "Profit vs game baseline", "fps cash", "After-tax game effect", "Interest on added debt",
                    "Free cash flow", "Net debt", "Cash to owners", "Stress base FCF", "Stress FCF", "Stress net debt", "Stress cash to owners",
                    "Net debt, no programme", "Cash to owners, no programme"], rows)


def alts_table():
    order = sorted(BF["alts"], key=lambda a: -a["pv"])
    rows = []
    for a in order:
        played = a is PLAY
        nm = esc(a["plan"]) + (" <b>(played)</b>" if played else "")
        met = sum(1 for _, ok in a["objectives"] if ok)
        st = ("met" if a["stress_held"] else "<b>not met</b>")
        pk = a["stress_peak_after"]
        pk_s = f'{pk[1]:.2f} ({pk[0]})' if pk and pk[1] > 1e-6 else "0"
        sp = a["peak_spend"]
        rows.append([nm, K.num(a["pv"]), str(a["fps_eis"] or "—"), pct(a["nb_share"]["2040"] if "2040" in a["nb_share"] else a["nb_share"][2040]),
                     pct(a["nb_share"]["2050"] if "2050" in a["nb_share"] else a["nb_share"][2050]),
                     (f'{sp[0]:.2f} ({sp[1]})' if sp[1] else "—"), f'{a["total_spend"]:.2f}',
                     f'{a["min_stress_fcf"][0]:.2f} ({a["min_stress_fcf"][1]})', pk_s, st, f'{a["owners_2027_50"]:.1f}', f'{a["owners_2027_60"]:.1f}',
                     f"{met} of {len(a['objectives'])}"])
    return K.table(["Boeing's 2030 plan (everyone else as played)", "Final ΔPV $B", "fps in service", "NB share 2040", "NB share 2050",
                    "Peak programme cash $B (year)", "Programme cash, total $B", "Lowest stress FCF $B (year)",
                    "Stress net debt after repair, peak $B (year)", "Stress line (2035-2050)", "Cash to owners 2027-2050 $B",
                    "Cash to owners 2027-2060 $B", "Objectives met"], rows, num_cols=tuple(range(1, 13)))


ANALYST = [
    ("Net debt, end-2026", "$22.53B", "consensus mean (5 estimates); GS $22.55B, MS $23.01B", "Consensus 'Net Debt'; GS BA BS r64; MS BA Balance_Sheet_Annual"),
    ("Net debt, end-2027 / end-2028", "$16.94B / $7.21B", "consensus; the tracker gives $16.49B / $6.70B in 2026 dollars against $16.57B / $6.90B deflated", "Consensus 'Net Debt'"),
    ("Free cash flow 2026-2030", "$2.2B, $5.7B, $9.9B, $13.0B, $15.0B", "consensus; $45.8B in all (computed). Boeing guides $1-3B for 2026", "Consensus 'Free Cash Flow'; guidance rows 225/227"),
    ("Net debt 2010-2018", "average about −$0.6B", "a small net cash: the objective's historical level, rounded to $0", "GS BA BS r64"),
    ("Gross debt, mid-2026", "$45.9B", "the dashboard's $45B", "GS BA BS r63"),
    ("Commercial Airplanes revenue", "2026E $48.3B (MS) / $45.3B (GS); 2030E $62.8B / $84.9B", "2025A $41.5B; 2018A $57.5B", "MS BA BCA_Annual; GS BA SEG r36"),
    ("Commercial Airplanes operating profit", "2026E −$0.3B (MS) / −$1.2B (GS); 2030E $6.2B / $12.2B", "2025A −$7.1B; 2018A $7.8B", "MS BA BCA_Annual; GS BA SEG r168"),
    ("Capital allocation 2027-2030", "GS $42B of buybacks; MS none", "GS ends 2030 at $17.4B net debt, MS at $16.2B net cash", "GS BA CFLO r45, BS r64; MS BA Cash_Flow_Annual r51, Balance_Sheet_Annual 'Net Debt'"),
    ("A new airplane in the forecasts", "none", "every launch is on top of the analysts' cash flow", "analyst note, Boeing profile"),
]


def analyst_table():
    nb = lambda t: esc(t).replace("\u2212$", "\u2212\u2060$")
    return K.table(["Item", "Analysts", "Note", "Source"], [[esc(a), nb(b_), nb(c), esc(d)] for a, b_, c, d in ANALYST])


# ─────────────────────────────── page ───────────────────────────────
def tiles():
    t = [("ΔPV vs status quo", K.usd(V["pv_delta"], 2, True), f'Yield {K.rnd(V["yield"], 2):.2f}%; the same as the previous game'),
         ("fps, 10-year ramp", "$60.32B", f"launched 2030, in service 2040; cash peaks at ${SPEND[PEAK_Y]:.2f}B in {PEAK_Y}"),
         ("Operating profit, 2050", f'${PY[2050]["profit"]:.2f}B', f'${PY[2050]["vs_sq"]:.2f}B a year above the status quo (${PY[2050]["sq_profit"]:.3f}B)'),
         ("Narrowbody share", pct(PY[2050]["nb_share"]), f'40% today, a low of {pct(PY[2039]["nb_share"])} in 2039, 47% from 2049'),
         ("Net debt", "$0 from 2029", "from 2030 in the stress case; held through the fps spending peak"),
         ("Cash to owners, 2027-2050", f'${O50["play"]:.1f}B', f'${O50["play"] - O50["hold"]:.1f}B more than Do Nothing; the fps pays back in {PAYBACK}')]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v}</div><div class="d">{esc(d_)}</div></div>'
                                           for k, v, d_ in t) + "</div>"


def points():
    p = [
        ("Nothing moves until 2037; then Airbus's NGSA takes share for three years.",
         f"<ul><li>Through 2036 the board books the status quo every year: 800 narrowbodies at $48M and an 8% margin, 100 "
         f"widebodies, ${PY[2030]['revenue']:.1f}B of revenue and ${PY[2030]['profit']:.2f}B of operating profit.</li>"
         f"<li>NGSA enters service in 2037 and Boeing's share falls a point a year to {pct(PY[2039]['nb_share'])} in 2039: "
         f"{PY[2039]['nb_units']:,.0f} deliveries, ${-PY[2039]['vs_sq']:.2f}B a year below the status quo.</li></ul>"),
        ("From 2040 the fps lifts profit by $7.65B a year, rising to $10.18B.",
         f"<ul><li>The fps sells at $55M against the 737 MAX's $48M, at a {pct(PY[2040]['nb_margin'], 1)} margin against 8%.</li>"
         f"<li>Share recovers a point a year from 38% in 2040 to 47% in 2049, so operating profit goes from "
         f"${PY[2040]['profit']:.2f}B to ${PY[2049]['profit']:.2f}B, against ${PY[2040]['sq_profit']:.2f}B in the status quo. The "
         "widebody is unchanged: no 787 Re-engine.</li>"
         f"<li>Over 2026-2060 the game adds ${sum(r['vs_sq'] for r in PL):.1f}B of operating profit at 2026 prices.</li></ul>"),
        ("In present value, the bill and the debt penalty absorb almost all of it: ΔPV +$0.66B.",
         f"<ul><li>Narrowbody profit above the status quo: +${V['bridge']['nb_profit_vs_sq']:.2f}B in PV at 2026 (10.5%).</li>"
         f"<li>The fps bill: the dashboard charges all $60.32B at entry into service in 2040, −${-V['bridge']['programme_investment']:.2f}B in PV.</li>"
         f"<li>The debt penalty: the board's α (0.3) on $45B of debt, rising by ${PEN_UNDISC:.2f}B undiscounted when the "
         f"bill is added, −${-V['bridge']['debt_penalty']:.2f}B in PV.</li></ul>"),
        ("In cash, the fps costs the owners in 2030-2039 and pays back, cumulatively, in 2046.",
         f"<ul><li>The tracker spends the bill over 2030-2039 on the standard curve, from ${SPEND[2030]:.2f}B in 2030 to "
         f"${SPEND[PEAK_Y]:.2f}B in {PEAK_Y}. Free cash flow never goes negative: from 2030 at least ${MIN_BASE[0]:.2f}B in "
         f"the base case and ${MIN_STRESS[0]:.2f}B in the stress case ({MIN_STRESS[1]}).</li>"
         f"<li>Net debt is at its historical level from 2029 (2030 in the stress case), so the fps is paid from cash that "
         "would otherwise go to the owners.</li>"
         f"<li>Against Do Nothing (no fps while Airbus launches NGSA) the owners receive less each year in 2030-2039 and more "
         f"from 2040; their cumulative cash trails until {PAYBACK - 1} and leads from {PAYBACK}: ${O50['play'] - O50['hold']:.1f}B more by 2050 and ${O60['play'] - O60['hold']:.1f}B more by 2060, in 2026 "
         "dollars, undiscounted.</li></ul>"),
        ("Every plan on the 10-year ramp keeps the stress line; the 7-year keeps it only with the 737 rate increase and no 787 Re-engine.",
         f"<ul><li>The 7-year ramp alone is worth ${ALTS['fps 7-yr + 787: hold']['pv'] - PLAY['pv']:.2f}B more and gives the "
         f"owners ${ALTS['fps 7-yr + 787: hold']['owners_2027_50'] - O50['play']:.1f}B more by 2050, but its spend peaks at "
         f"${ALTS['fps 7-yr + 787: hold']['peak_spend'][0]:.2f}B in 2034 and the stress case puts net debt back to "
         f"${ALTS['fps 7-yr + 787: hold']['stress_2035']:.2f}B at end-2035.</li>"
         f"<li>With the 737 rate increase (and the 787 held) the 7-year keeps the line (net debt ${ALTS['fps 7-yr + 737 rate up + 787: hold']['stress_peak_after'][1]:.2f}B "
         f"at its 2034 peak, zero by end-2035), but it is then worth {K.num(ALTS['fps 7-yr + 737 rate up + 787: hold']['pv'])}, less "
         "than the 10-year's +0.66.</li>"
         f"<li>A 787 Re-engine beside the 10-year was worth ${ALTS['fps 10-yr + 787 Re-engine']['pv'] - PLAY['pv']:.2f}B more and "
         "keeps every debt line; it was kept out by Boeing's one-development-at-a-time rule and its Board's downside test.</li>"
         f"<li>Do Nothing is −${-HOLD['pv']:.2f}B: Boeing's narrowbody share falls to {pct(HOLD['nb_share']['2050'] if '2050' in HOLD['nb_share'] else HOLD['nb_share'][2050])} by 2050.</li></ul>"),
    ]
    return '<div class="bl">' + "".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in p) + "</div>"


def build(out_path):
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;", "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }", "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; color-scheme: dark; }")
    css += (".chart .hit { cursor: crosshair; } .chart .hit:focus { outline: none; stroke: var(--fg); stroke-width: 1; }\n"
            ".tiles { grid-template-columns: repeat(3, 1fr); } @media (max-width: 760px) { .tiles { grid-template-columns: 1fr 1fr; } }\n"
            "@media (max-width: 420px) { .tiles { grid-template-columns: 1fr; } }\n"
            "#alts th[scope=row] { min-width: 15em; } .nw { white-space: nowrap; }\n")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boeing Financials, Objectives Replay</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · dash-2050 objectives replay · Boeing financials · BOEING PROPRIETARY</p>
<h1>Boeing financials: the fps pays back in {PAYBACK}, and the balance sheet stays repaired throughout</h1>
<p class="lede">Boeing launched fps on the 10-year ramp in 2030, open to all three engine makers, and held everything else. Two views of
its money follow. <b>The dashboard</b> values Boeing's new-airplane business at 2026 prices: +$0.66B of present value against the
status quo, the same as in the previous game. <b>The GM's balance-sheet tracker</b> follows the whole company's cash and net debt
in 2026 dollars, starting from the analysts' consensus and adding the game's changes. The two are never mixed in one chart.</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#pl">P&amp;L</a><a href="#value">Present value</a><a href="#cash">Cash and net debt</a>
<a href="#alts">The 2030 alternatives</a><a href="#analysts">Analysts' baseline</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}{points()}</section>

<section id="pl"><h2>P&amp;L: the dashboard's new-airplane business</h2>
<p class="lede">Revenue and operating profit of Boeing's narrowbody and widebody deliveries as the dashboard models them, at 2026
prices (it does not escalate airframe prices). Hover a column for the year's figures.</p><div class="stack">
<div class="panel"><p class="ctitle">Revenue: flat at ${PY[2030]['revenue']:.1f}B until 2036, a dip while NGSA is alone, then up to ${PY[2050]['revenue']:.1f}B as the fps gains share</p>{chart_revenue()}</div>
<div class="panel"><p class="ctitle">Operating profit: ${PY[2040]['vs_sq']:.2f}B a year above the status quo from 2040, ${PY[2050]['vs_sq']:.2f}B from 2049</p>{chart_profit()}
<p class="cap">The fps margin ({pct(PY[2040]['nb_margin'], 1)} at $55M) against the 737 MAX's (8% at $48M) does most of the work. The dashboard books the whole
$60.32B fps bill in 2040, outside operating profit; the tracker below spreads it as cash over 2030-2039.</p></div>
<div class="panel"><p class="label">By period, 2026 prices</p>{periods_table()}{pl_table()}</div>
</div></section>

<section id="value"><h2>Present value: how +$0.66B is built</h2><div class="stack">
<div class="panel"><p class="ctitle">ΔPV bridge, $B at 2026 (WACC 10.5%)</p>{chart_bridge()}
<p class="cap">Narrowbody operating profit above the status quo, discounted; less the fps bill, charged in full at entry into service
(2040) as the dashboard does; less the board's debt penalty, D × α × (D ÷ value)² with α 0.3, D = $45B and value $130B, which rises
to D = $105.32B when the bill is added (${PEN_UNDISC:.2f}B undiscounted). Widebody profit, the 737 rate increase, Delay Tactics and
the two-front strain are zero for Boeing in this game.</p></div></div></section>

<section id="cash"><h2>Cash and net debt: the GM's tracker</h2>
<p class="lede">Whole-company free cash flow and net debt in 2026 dollars. Base free cash flow is the analysts' consensus for
2027-2030 (deflated at 2.2%), flat after; the stress case is one-third lower. The game adds 79% of (its profit change − fps cash),
and charges 3% real interest on any debt it adds. Debt comes first; once net debt is at its historical level (about zero), the surplus is
cash to the owners. This is how Control's balance-sheet objective is scored; it does not change the dashboard's payoff.</p><div class="stack">
<div class="panel"><p class="ctitle">fps cash peaks at ${SPEND[PEAK_Y]:.2f}B in {PEAK_Y}; free cash flow stays positive, at least ${MIN_STRESS[0]:.2f}B in the stress case</p>{chart_cash()}</div>
<div class="panel"><p class="ctitle">Net debt reaches $0 in 2029 (2030 in the stress case) and stays there</p>{chart_debt()}</div>
<div class="panel"><p class="ctitle">Cumulative cash to owners: behind Do Nothing until {PAYBACK - 1}, ahead from {PAYBACK}</p>{chart_owners()}</div>
<div class="panel"><p class="label">Year by year</p>{cash_table()}
<p class="cap">Cash to owners is free cash flow once net debt is at the historical level (in 2029, what is left after clearing
the last of the debt). "No programme" is the analysts' path with no game at all; Do Nothing (in the chart and the next section)
is the game with Boeing holding while Airbus launches NGSA. The game profit change counts from 2030 as played; the 2037-2039
values are NGSA's effect.</p></div>
</div></section>

<section id="alts"><h2>The 2030 alternatives, on both measures</h2>
<p class="lede">Every plan Boeing could order in 2030, replayed with every other company's actual orders in every round, as the
regret table does. The fps engine code is kept at 7 (all three makers): it does not change Boeing's value.</p><div class="stack">
<div class="panel">{alts_table()}
<p class="cap">The stress line is Control's objective: net debt back to its historical level by end-2030 and held at end-2035, 2040,
2045 and 2050 with free cash flow one-third lower. It looks only at those years, so a plan can pass with net debt above zero in
between (fps via Embraer with the rate increase peaks at $2.71B in 2037 and passes). Objectives met counts all seven of Boeing's,
the two share objectives included.</p></div></div></section>

<section id="analysts"><h2>The analysts' baseline (real world: broker models July 2026, consensus October 2026)</h2>
<p class="lede">The tracker starts from these. The dashboard's P&amp;L is a stylised model of the new-airplane business; it is not
Boeing's reported Commercial Airplanes segment, which loses money in 2026 on the analysts' numbers.</p><div class="stack">
<div class="panel">{analyst_table()}<p class="cap">MS = Morgan Stanley (29 July 2026), GS = Goldman Sachs (28 July 2026), consensus =
S&amp;P Capital IQ (around 10-11 October 2026); nominal dollars. From the analyst note in Boeing's profile, checked against the model files.</p></div>
</div></section>

<section id="method"><h2>Method and sources</h2><div class="panel stack"><ul class="cav">
<li><b>Game.</b> Run dash-2050-obj: four sealed rounds (2030, 2035, 2045, 2050) on combined_dash.py at the Game_v3.txt snapshot.
Boeing's orders: fps on the 10-year ramp in 2030 with engine code 7, then hold. The final state equals the 2035 state.</li>
<li><b>P&amp;L and ΔPV.</b> The GM valuation of the final state (data/report_data.json): the dashboard's own airframer model at the
game's dates (fps 2040, NGSA 2037). ΔPV is against the status quo in which nobody launches anything.</li>
<li><b>Tracker.</b> wargame/dashgame/finance.py and finance_inputs.json. Start $22.53B net debt at end-2026; base free cash flow
$5.55B, $9.44B, $12.20B, $13.79B (2027-2030, 2026 dollars), then $13.79B flat; tax 21%; real rate 3%; CPI 2.2%; development cash on a
standard curve (5% in year 1 of 10, peaking at 14% in year 7).</li>
<li><b>Alternatives.</b> data/boeing_fin.json, from make_boeing_fin_data.py, which replays each 2030 plan through the game rules.</li>
<li>Built by make_boeing_fin.py. BOEING PROPRIETARY.</li></ul></div></section>
<footer>BOEING PROPRIETARY. dash-2050 objectives replay, Boeing financials. Built from wargame/runs/dash-2050-obj.</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page), "payback", PAYBACK)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "boeing_financials.html"))
