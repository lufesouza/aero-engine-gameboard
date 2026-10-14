"""Build fps_business_case.html: Boeing's fps business case in the supply-and-demand game (run dash-2050-sd): launch a
10-year fps in 2030 against Do Nothing, year-by-year incremental cash flow, the bridge from cash flow to value, key
assumptions and sensitivities. Every number comes from analysis/fps_business_case/case.json (make_case.py), which
reconciles exactly with the game's ΔPV.

Usage: python3 make_fps_case_html.py [out.html]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
C = json.load(open(os.path.join(HERE, "analysis", "fps_business_case", "case.json")))
P = C["params"]
R = C["cases"]["renton"]
N = C["cases"]["new_site"]
ROWS = R["rows"]
BY = {r["year"]: r for r in ROWS}
NBY = {r["year"]: r for r in N["rows"]}
BRIEFED = next(x for x in json.load(open(os.path.join(HERE, "data", "sd_checks.json")))["round_items"] if x["year"] == 2030)["briefed"]
Y_LO, Y_HI = 2030, 2059
YEARS = list(range(Y_LO, Y_HI + 1))
MINUS = K.MINUS


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def bp(v, dp=2, sign=True):
    """Plain-text $B for SVG text and tooltips (no HTML)."""
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def f1(v):
    x = K.rnd(v, 1)
    return (MINUS if x < 0 else "") + f"{abs(x):,.1f}"


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def pc(v, dp=1):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def legend(items):
    def key(var, kind):
        if kind in ("ln", "dash"):
            da = ' stroke-dasharray="6 4"' if kind == "dash" else ""
            return (f'<svg width="24" height="4" aria-hidden="true" style="vertical-align:middle;margin-right:6px">'
                    f'<line x1="0" y1="2" x2="24" y2="2" stroke="var(--{var})" stroke-width="2"{da}/></svg>')
        return f'<i class="sq" style="background:var(--{var})"></i>'
    return '<div class="legend">' + "".join(f'<span>{key(v, k)}{esc(l)}</span>' for l, v, k in items) + "</div>"


# ─────────────────────────────── charts ───────────────────────────────
def chart_annual():
    """Cash view, $B a year: incremental operating profit and the Renton credit up, development spend down."""
    w, h, left, right, top, bot = 760, 360, 58, 20, 20, 46
    lo, hi, step = -10, 15, 5
    sx = lambda i: left + i * (w - left - right) / len(YEARS)
    bw = (w - left - right) / len(YEARS) - 3
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "fps cash flow by year against Do Nothing, cash view")]
    t = lo
    while t <= hi + 1e-9:
        cls = "zero" if t == 0 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
        t += step
    for i, y in enumerate(YEARS):
        r = BY[y]
        x = sx(i) + 1.5
        op, sp, rc = r["op_profit_inc"], r["bill_cash"], r["renton_cash"]
        if sp < -1e-9:
            out.append(f'<path d="{K.bar_path(x, bw, sy(0) + 1, sy(sp))}" fill="var(--s2)"/>')
        y0 = 0.0
        if op > 1e-9:
            top_v = op + (rc if rc > 1e-9 else 0)
            out.append(f'<path d="{K.bar_path(x, bw, sy(0) - 1, sy(op)) if rc <= 1e-9 else ""}" fill="var(--s1)"/>' if rc <= 1e-9 else
                       f'<rect x="{x:.1f}" y="{sy(op):.1f}" width="{bw:.1f}" height="{max(0, sy(0) - 1 - sy(op)):.1f}" fill="var(--s1)"/>')
            y0 = op
        if rc > 1e-9:
            out.append(f'<path d="{K.bar_path(x, bw, sy(y0) - (2 if y0 > 0 else 1), sy(y0 + rc))}" fill="var(--s3)"/>')
        rows = [(bp(r["net_cash"]), f"{y}: net cash flow", None), (bp(op), "incremental operating profit", "var(--s1)")]
        if sp < -1e-9:
            rows.append((bp(sp), "development spend", "var(--s2)"))
        if rc > 1e-9:
            rows.append((bp(rc), "Renton: new-site capex avoided", "var(--s3)"))
        out.append(f'<rect x="{sx(i):.1f}" y="{top}" width="{bw + 3:.1f}" height="{h - top - bot}" class="hit" {K.mark_attrs(*rows)}/>')
        if y % 5 == 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">$B a year, pre-tax, constant 2026 dollars (fps at Renton minus Do Nothing)</text></svg>')
    lg = legend([("Incremental operating profit (fps minus Do Nothing, as delivered)", "s1", "sq"),
                 ("Development spend ($60.3B over 2030-2039)", "s2", "sq"), ("Renton: new-site capex avoided", "s3", "sq")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def chart_cumulative():
    """Cumulative net cash, undiscounted and discounted to 2026 (cash view); the game view's discounted path dashed."""
    w, h, left, right, top, bot = 760, 340, 58, 206, 20, 46
    lo, hi, step = -90, 150, 30
    sx = lambda x: left + (x - Y_LO) / (Y_HI - Y_LO) * (w - left - right)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    cum, cpv, gpv = [], [], []
    a = p_ = g_ = 0.0
    for y in YEARS:
        r = BY[y]
        a += r["net_cash"]; p_ += r["net_cash"] * r["df"]; g_ += r["net_game"] * r["df"]
        cum.append((y, a)); cpv.append((y, p_)); gpv.append((y, g_))
    series = [("Cash", "s1", cum, False), ("Cash view PV", "fg", cpv, False), ("Game view PV", "muted", gpv, True)]
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="Cumulative net cash of the fps, undiscounted and '
           f'discounted. Use the arrow keys to read values by year." tabindex="0">']
    t = lo
    while t <= hi + 1e-9:
        cls = "zero" if t == 0 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
        t += step
    for yr in range(2030, Y_HI + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    pb = R["payback_cash"]
    out.append(f'<line x1="{sx(pb):.1f}" x2="{sx(pb):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
               f'<text x="{sx(pb) + 5:.1f}" y="{top + 11}" class="ann">cash back {pb}</text>')
    py = R["peak_funding_cash_year"]
    out.append(f'<text x="{sx(py):.1f}" y="{sy(R["peak_funding_cash"]) + 20:.1f}" text-anchor="middle" class="ann">peak need {bp(-R["peak_funding_cash"], 1, False)} ({py})</text>')
    for name, var, d, dash in series:
        path = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in d)
        da = ' stroke-dasharray="6 4"' if dash else ""
        out.append(f'<path d="{path}" fill="none" stroke="var(--{var})" stroke-width="2"{da} stroke-linejoin="round"/>')
    last = [d[-1][1] for _, _, d, _ in series]
    ys = sorted(range(3), key=lambda i: -last[i])
    placed, prev = {}, None
    for i in ys:
        p = sy(last[i]) if prev is None else max(sy(last[i]), prev + 18)
        placed[i] = p; prev = p
    for i, (name, var, d, _) in enumerate(series):
        x, v = d[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
        out.append(f'<text x="{w - right + 8}" y="{placed[i] + 4:.1f}" class="endlab">{esc(name)} {bp(v, 1)}</text>')
    payload = {"x0": left, "x1": w - right, "xlo": Y_LO, "xhi": Y_HI, "w": w, "fmt": "int", "years": YEARS,
               "series": [{"name": n + " ($B)", "k": f"var(--{c})", "vals": {str(x): round(v, 1) for x, v in d}}
                          for n, (_, c, d, _) in zip(("Cumulative cash", "Cumulative PV, cash view", "Cumulative PV, game view"), series)]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">$B, cumulative from 2030; PV discounted at 10.5% to 2026</text></svg>')
    lg = legend([("Cumulative net cash (cash view)", "s1", "ln"), ("Cumulative present value at 2026 (cash view)", "fg", "ln"),
                 ("Cumulative present value, game view (bill and debt penalty booked in 2040)", "muted", "dash")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def short(lab):
    """Bar-end label for the tornado (the table keeps the full wording)."""
    lab = lab.split(" (")[0]
    lab = {"three times as fast": "3× as fast", "50% more growth": "+50% growth", "+10 years at the 2059 profit": "+10 years"}.get(lab, lab)
    return lab.replace("-", MINUS)


def chart_tornado():
    S = C["sensitivities"]
    base = C["base_for_sensitivities"]["game_npv"]
    S = sorted(S, key=lambda s: -abs(s["high"] - s["low"]))
    w, left, right, top, row = 760, 20, 20, 40, 56
    h = top + row * len(S) + 44
    lo, hi = -10, 5
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    halo = 'style="paint-order:stroke;stroke:var(--surface);stroke-width:4px;stroke-linejoin:round"'
    out = [K.svg_open(w, h, "Sensitivity of the fps value, game view")]
    for t in range(lo, hi + 1, 2 if lo % 2 == 0 else 1):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 8}" y2="{h - 38}" class="grid"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 22}" text-anchor="middle" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
    out.append(f'<line x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{top - 8}" y2="{h - 38}" class="zero"/>')
    out.append(f'<line x1="{sx(1):.1f}" x2="{sx(1):.1f}" y1="{top - 14}" y2="{h - 38}" class="ref"/>'
               f'<text x="{sx(1) + 4:.1f}" y="{top - 18}" class="reflab">Board bar +$1B</text>')
    out.append(f'<line x1="{sx(base):.1f}" x2="{sx(base):.1f}" y1="{top - 14}" y2="{h - 38}" class="leader"/>'
               f'<text x="{sx(base) - 4:.1f}" y="{top - 18}" text-anchor="end" class="ann">base {bp(base)}</text>')
    for i, s in enumerate(S):
        y = top + i * row
        out.append(f'<text x="{left}" y="{y + 12}" class="rowlab sm" {halo}>{esc(s["factor"])}</text>')
        for v, lab in ((s["low"], s["low_label"]), (s["high"], s["high_label"])):
            if abs(v - base) < 1e-6:
                continue
            col = "s1" if v > base else "s2"
            x0, x1 = sx(base), sx(max(lo, min(hi, v)))
            attrs = K.mark_attrs((bp(v), f"{s['factor']}: {lab}", f"var(--{col})"), (bp(s["low_cash"] if v == s["low"] else s["high_cash"]), "same change, cash view", None))
            out.append(f'<path d="{K.hbar_path(x0, x1, y + 20, 18)}" fill="var(--{col})" {attrs}/>')
            anchor = "start" if v > base else "end"
            tx = x1 + (6 if v > base else -6)
            out.append(f'<text x="{tx:.1f}" y="{y + 33}" text-anchor="{anchor}" class="val sm">{esc(short(lab))} {bp(v)}</text>')
    out.append(f'<text x="{left}" y="{h - 3}" class="tick">fps minus Do Nothing, $B PV at 2026, game view (Renton)</text></svg>')
    lg = legend([("Better than the base case", "s1", "sq"), ("Worse than the base case", "s2", "sq")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


# ─────────────────────────────── tables ───────────────────────────────
def cash_table():
    head = ["Year", "fps delivered", "Boeing delivered: fps case", "Boeing delivered: Do Nothing", "Incremental operating profit",
            "Development spend", "Renton credit", "Net cash flow", "Cumulative cash", "Discount factor", "Present value"]
    rows, cum = [], 0.0
    for y in YEARS:
        r = BY[y]
        cum += r["net_cash"]
        rows.append([str(y), n0(r["fps_units"]), n0(r["boeing_units_fps_case"]), n0(r["boeing_units_dn"]),
                     f1(r["op_profit_inc"]), f1(r["bill_cash"]), f1(r["renton_cash"]), f1(r["net_cash"]), f1(cum),
                     f"{r['df']:.3f}", f"{K.num(r['net_cash'] * r['df'], '+.2f')}"])
    tot_op = sum(BY[y]["op_profit_inc"] for y in YEARS)
    tot_sp = sum(BY[y]["bill_cash"] for y in YEARS)
    tot_rc = sum(BY[y]["renton_cash"] for y in YEARS)
    rows.append(["<b>Total</b>", "", "", "", f"<b>{f1(tot_op)}</b>", f"<b>{f1(tot_sp)}</b>", f"<b>{f1(tot_rc)}</b>",
                 f"<b>{f1(tot_op + tot_sp + tot_rc)}</b>", "", "", f"<b>{K.num(R['cash_npv'], '+.2f')}</b>"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def bridge_table():
    head = ["$B, present value at 2026", "Game view, Renton", "Cash view, Renton", "Game view, new sites", "Cash view, new sites"]
    def row(lab, gr, cr, gn, cn):
        return [lab] + [("—" if v is None else K.num(v, "+.2f")) for v in (gr, cr, gn, cn)]
    rows = [
        row("Incremental operating profit, as delivered (2037-2059)", R["op_profit_pv"], R["op_profit_pv"], N["op_profit_pv"], N["op_profit_pv"]),
        row("Development bill ($60.3B)", -R["bill_pv_game"], -R["bill_pv_cash"], -N["bill_pv_game"], -N["bill_pv_cash"]),
        row("Debt penalty (valuation haircut, not cash)", -R["debt_penalty_pv"], None, -N["debt_penalty_pv"], None),
        row("Renton: new-site capex avoided ($3.0B)", R["renton_pv_game"], R["renton_pv_cash"], None, None),
        ["<b>Net present value</b>"] + [f"<b>{K.num(v, '+.2f')}</b>" for v in (R["game_npv"], R["cash_npv"], N["game_npv"], N["cash_npv"])],
        row("Same, valued at 2030 (the decision year)", R["game_npv_2030"], R["cash_npv_2030"], N["game_npv_2030"], N["cash_npv_2030"]),
    ]
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def sens_table():
    S = sorted(C["sensitivities"], key=lambda s: -abs(s["high"] - s["low"]))
    head = ["Factor (base)", "Change", "Game view", "Cash view", "Change", "Game view", "Cash view", "Note"]
    rows = [[esc(s["factor"]), esc(s["low_label"]), K.num(s["low"], "+.2f"), K.num(s["low_cash"], "+.2f"),
             esc(s["high_label"]), K.num(s["high"], "+.2f"), K.num(s["high_cash"], "+.2f"), esc(s["note"])] for s in S]
    rows.insert(0, ["<b>Base case</b>", "", f'<b>{K.num(R["game_npv"], "+.2f")}</b>', f'<b>{K.num(R["cash_npv"], "+.2f")}</b>', "", "", "", "fps at Renton"])
    return K.table(head, rows, num_cols=(2, 3, 5, 6))


def risk_table():
    head = ["Risk", "Game view", "Cash view", "Why"]
    rows = [[esc(x["risk"]), K.num(x["game"], "+.2f"), K.num(x["cash"], "+.2f"), esc(x["note"])] for x in C["risks"]]
    return K.table(head, rows, num_cols=(1, 2))


def assumptions():
    sd, d = P["sd"], P["demand"]
    pref_f = [BY[y]["pref_fps_case"] for y in (2037, 2040, 2049)]
    pref_d = [BY[y]["pref_dn"] for y in (2037, 2043)]
    unit_fps = P["price_fps_m"] * P["margin_fps"]
    unit_max = P["price_737_m"] * P["margin_737"]
    ramp = [n0(BY[y]["fps_capacity"]) for y in range(2040, 2047)]
    groups = [
        ("Decision", [
            ("Option", "Launch a 10-year fps in 2030: in service 2040, offered with engines from all three makers (CFM, Pratt &amp; Whitney's own GTF2 and Rolls-Royce's own UltraFan, both launched in 2030; no Joint Venture). Base case at Renton (the better site); new sites shown alongside."),
            ("Counterfactual", "Do Nothing: the 737 MAX carries on, no fps, no 787 Re-engine, no rate increase."),
            ("Rivals", "As played in 2030: Airbus launches NGSA (in service 2037) on the A320 Alt plan; no A350 Re-engine; no Delay Tactics. Nobody moves after 2030."),
        ]),
        ("Market", [
            ("Demand", f"New demand = replacement (your Cirium page) + fleet growth (Airbus GMF 2025, Boeing CMO): {n0(BY[2030]['new_demand'])} aircraft in 2030, {n0(BY[2040]['new_demand'])} in 2040, {n0(BY[2050]['new_demand'])} in 2050 (737/A320 class)."),
            ("Firm backlog", f"737 MAX {d['firm_backlog']['boeing']:,}, A320neo family {d['firm_backlog']['airbus']:,}: delivered first."),
            ("Customer preference (dashboard's share rule)", f"With the fps: Boeing {pc(pref_f[0], 0)} in 2037, easing 1 point a year to {pc(BY[2039]['pref_fps_case'], 0)} in 2039 while NGSA leads, then {pc(pref_f[1], 0)} in 2040, rising 1 point a year to {pc(pref_f[2], 0)} from 2049. With Do Nothing: {pc(pref_d[0], 0)} in 2037, falling 3 points a year to {pc(pref_d[1], 0)} from 2043."),
            ("Overflow", f"{pc(d['flex_share'])} of unserved customers take the other maker's free slots; {pc(d['lapse_per_year'], 0)} of those still waiting drop out each year."),
        ]),
        ("Prices and margins (constant 2026 $, no escalation)", [
            ("fps", f"${P['price_fps_m']:.0f}M at {pc(P['margin_fps'], 2)} = ${unit_fps:.1f}M operating profit an aircraft."),
            ("737 MAX", f"${P['price_737_m']:.0f}M at {pc(P['margin_737'], 0)} = ${unit_max:.2f}M an aircraft."),
        ]),
        ("Capacity", [
            ("737 MAX", f"{', '.join(f'{v:g}' for v in sd['max_rate'].values())} a month in 2026-2029, then {sd['max_rate_after']:g}. With the fps it gives way under Boeing's {sd['total_rate_cap']:g}-a-month total, keeping a {sd['max_tail_rate']:g}-a-month tail to 2050. At Renton its lines ({sd['renton_rate']:g} a month) wind down as the fps ramps; Everett keeps up to {sd['everett_rate']:g}."),
            ("fps ramp", f"Your NGSA Rev. B curve, moved to 2040: {', '.join(ramp)} aircraft a year in 2040-2046, then 1,080 (90 a month) to 2050 and 1,200 from 2051."),
        ]),
        ("Investment", [
            ("Development bill", f"${P['bill_10yr']:.2f}B for the 10-year fps (${P['bill_7yr']:.1f}B for the 7-year), constant 2026 $, from the dashboard (v3 snapshot)."),
            ("Timing", "Game view: one lump in 2040, the entry-into-service year (the dashboard's convention). Cash view: spent over 2030-2039 on the game's development curve: "
                       + ", ".join(f"{int(v * 100)}%" for v in P["phasing_curve"]) + "."),
            ("Renton", f"${sd['renton_saving_b']:.1f}B of new-site capex avoided (range ${sd['renton_saving_range_b'][0]:.1f}B-${sd['renton_saving_range_b'][1]:.1f}B): in 2040 in the game view, $1.0B a year in 2037-2039 in the cash view."),
        ]),
        ("Financing and valuation", [
            ("Debt penalty (game view only)", f"The dashboard adds a leverage haircut as if the whole bill were added to Boeing's ${P['debt_boeing']:.0f}B gross debt: α × ((D+bill)³ − D³) / EV², with α {P['alpha']}, EV ${P['ev_boeing']:.0f}B. That is ${R['debt_penalty_nominal']:.1f}B booked in 2040, {b(-R['debt_penalty_pv'])} at 2026. It is not a cash flow; the game's balance-sheet tracker has Boeing's net debt (debt less cash) back at zero, its historical level, from 2029 either way."),
            ("Discount rate", f"Boeing's WACC, {pc(P['WACC_B'], 1)}, to 2026. It is applied to constant-2026-dollar flows, so it is conservative if read as a nominal rate."),
            ("Horizon", f"The dashboard counts {P['post_eis_years']} years from entry into service (to 2059). Nothing is counted after that, though the fps still earns about $12B a year in 2060."),
            ("Basis", "Pre-tax operating profit. No tax, working capital, recurring capex or support revenue. Widebody unaffected (no 787 Re-engine in either case)."),
        ]),
    ]
    rows = []
    for g, items in groups:
        rows.append([f"<b>{g}</b>", ""])
        for k, v in items:
            rows.append([k, v])
    return K.table(["Assumption", "Value and source"], rows)


def tiles():
    t = [("Net present value, game view", b(R["game_npv"]), f"The game's own valuation, on corrected demand (briefed in 2030: {b(BRIEFED['fps_10yr_renton'])}). Boeing's Board needs more than +$1B. New sites {b(N['game_npv'])}."),
         ("Net present value, cash view", b(R["cash_npv"]), f"The bill spent over 2030-2039, no debt penalty. New sites {b(N['cash_npv'])}."),
         ("Internal rate of return, cash view", pc(R["irr_cash"]), f"Against Boeing's {pc(P['WACC_B'])} cost of capital."),
         ("Peak funding need", b(-R["peak_funding_cash"], 1, False), f"Cumulative cash at its lowest, end-{R['peak_funding_cash_year']}."),
         ("Cash payback", str(R["payback_cash"]), "Undiscounted. Discounted at 10.5%, it never pays back within the 20 years counted."),
         ("Dashboard alone", b(C["dashboard_alone_item"]), "The same decision with every forecast aircraft delivered: the case Boeing launched on in the previous game.")]
    return '<div class="tiles">' + "".join(
        f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v}</div><div class="d">{d_}</div></div>' for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS + "\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }\n"
    op_dash = N["op_profit_dashboard_pv"]
    early_dash = sum(NBY[y]["op_profit_inc_dashboard"] * NBY[y]["df"] for y in range(2040, 2045))
    early_dlv = sum(NBY[y]["op_profit_inc"] * NBY[y]["df"] for y in range(2040, 2045))
    gap = op_dash - N["op_profit_pv"]
    assert abs(gap - (C["dashboard_alone_item"] - N["game_npv"])) < 1e-9
    top3 = [s["factor"].split(" (")[0] for s in sorted(C["sensitivities"], key=lambda s: -abs(s["high"] - s["low"]))[:3]]
    disc = next(s for s in C["sensitivities"] if s["factor"].startswith("Discount"))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>fps Business Case</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · supply-and-demand war game (dash-2050-sd) · BOEING PROPRIETARY</p>
<h1>fps business case</h1>
<p class="lede">The decision Boeing faced in 2030: launch a 10-year fps (in service 2040) or Do Nothing, given Airbus's 2030
orders as played (NGSA launched the same year on the A320 Alt plan). The fps adds about {b(R["op_profit_undiscounted"], 0, False)} of operating profit over 2037-2059, but it
needs {b(P["bill_10yr"], 1, False)} first, and its margin arrives late as production ramps up. As the game values it, the fps
is worth {b(R["game_npv"])} at Renton against Do Nothing; with the bill spent as it would really go out, {b(R["cash_npv"])}.
Either way it is short of the +$1B Boeing's Board requires.</p>
<nav class="toc"><a href="#cash">Cash flow</a><a href="#table">Year by year</a><a href="#value">From cash flow to value</a><a href="#assumptions">Key assumptions</a><a href="#sens">Sensitivities</a><a href="#notes">Notes</a></nav></header>

<section style="margin-top:22px">{tiles()}</section>

<section id="cash"><h2>Cash flow</h2><p class="lede">Ten years of development spend, then a slow climb. Production
follows your NGSA Rev. B ramp, so the fps adds little profit until 2043. Cumulative cash bottoms out at
{b(R["peak_funding_cash"], 1)} in {R["peak_funding_cash_year"]} and turns positive in {R["payback_cash"]}; discounted at
10.5%, it never does within the 20 years the game counts.</p><div class="stack">
<div class="panel"><p class="ctitle">Spend {b(P["bill_10yr"], 1, False)} in 2030-2039; profit reaches $9B a year only in 2045 and peaks near $14B in 2053</p>{chart_annual()}</div>
<div class="panel"><p class="ctitle">Cash comes back in {R["payback_cash"]}; in present value the fps ends {b(-R["cash_npv"], 1, False)} short (cash view) or {b(-R["game_npv"], 1, False)} short (game view)</p>{chart_cumulative()}
<p class="cap">The game view books the whole bill, and the debt penalty, in 2040; that is why its line is flat until then and then drops. The cash view spends the bill as it goes out, so it is further below zero in present value.</p></div>
</div></section>

<section id="table"><h2>Year by year (cash view, fps at Renton)</h2><p class="lede">Aircraft and $B, pre-tax, constant 2026
dollars. Incremental operating profit is the fps case minus Do Nothing, each against the status quo, as delivered. The game
counts it to 2059 (20 years from entry into service, 2040-2059). $B figures are rounded to one decimal; totals and the
cumulative column use unrounded values, so they may not add exactly.</p><div class="panel">{cash_table()}
<p class="cap">The 2037-2039 profit comes before the fps flies: with an fps announced, the dashboard's share rule lets NGSA gain only 1 point a year instead of 3, so the 737 MAX keeps more customers. In 2040 the game view also books the {b(P["bill_10yr"], 2, False)} bill, the {b(R["debt_penalty_nominal"], 2, False)} debt penalty and the {b(R["renton_saving"], 1, False)} Renton saving.</p></div></section>

<section id="value"><h2>From cash flow to value</h2><p class="lede">The two views share the operating profit. They differ in when
the bill and the Renton saving are counted, and in the debt penalty. The game books the bill at entry into service, which cuts its present
value to {b(R["bill_pv_game"], 2, False)} from {b(R["bill_pv_cash"], 2, False)}; the cash view spends it over 2030-2039 and drops the penalty, which is not a cash flow.</p><div class="stack">
<div class="panel">{bridge_table()}<p class="cap">The game view equals the game's ΔPV exactly (fps {b(R["dpv_fps"])} minus Do Nothing {b(R["dpv_dn"])} at Renton).
On the dashboard alone, with every forecast aircraft delivered, the same operating profit is worth {b(op_dash, 2, False)} instead of
{b(N["op_profit_pv"], 2, False)} at new sites: in 2040-2044 the dashboard books {b(early_dash, 1, False)} of incremental profit (PV) on fps margins from day one, while
the ramp delivers {b(early_dlv, 1, False)}. That {b(gap, 2, False)} gap is the whole difference between the dashboard's {b(C["dashboard_alone_item"])} and the game's {b(N["game_npv"])} at new sites.</p></div>
</div></section>

<section id="assumptions"><h2>Key assumptions</h2><div class="panel">{assumptions()}</div></section>

<section id="sens"><h2>Sensitivities</h2><p class="lede">What moves the value, one factor at a time from the Renton base case.
The {top3[0].lower()}, the {top3[1].lower()} and the {top3[2].lower()} matter most. Only a much faster ramp, a much cheaper bill, a better margin or a lower discount
rate clears the Board's +$1B in the game view; nothing shown clears zero in the cash view.</p><div class="stack">
<div class="panel"><p class="ctitle">The {top3[0].lower()}, the {top3[1]} and the {top3[2].lower()} move the value most</p>{chart_tornado()}</div>
<div class="panel"><p class="label">The same changes in both views</p>{sens_table()}
<p class="cap">Margin and price change only the fps's profit an aircraft: deliveries in the game do not depend on them, so these rows are exact. The ramp and growth rows are game runs from the levers analysis, both at Renton; with 50% more growth, new sites would do slightly better ({b(next(s for s in C["sensitivities"] if s["factor"].startswith("Fleet"))["best_site"]["game"])} game view). The horizon row adds ten years of profit at the 2059 level, which the game does not count.</p></div>
<div class="panel"><p class="label">Two risks the tornado leaves out</p>{risk_table()}</div>
</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Two views, one decision.</b> The game view is the game's own valuation, the method Boeing's ExCo and Board decided on, on the demand corrected after play. As briefed in 2030, the same choice was {b(BRIEFED["fps_10yr_renton"])} against Do Nothing at Renton and {b(BRIEFED["fps_10yr_new_site"])} at new sites; either way far short of the Board's +$1B. The cash view is how the same plan would look to a finance team: spend when it goes out, no leverage haircut. Neither includes tax.</li>
<li><b>Real or nominal.</b> All flows are constant 2026 dollars (no escalation), discounted at Boeing's 10.5% WACC, as the dashboard does. Read as a real rate, 10.5% is demanding; at 8% the game view is {b(disc["high"])}.</li>
<li><b>What is ours, not yours.</b> The fps ramp (your NGSA curve), fleet growth, the overflow and drop-out rates, the MAX path, the Renton figures and the development curve are game-master assumptions. The prices, margins, bill, debt penalty and share rules are the dashboard's.</li>
<li><b>Source.</b> analysis/fps_business_case/make_case.py writes case.json. The base-case game-view figures (value, bill, debt penalty, operating profit) are checked against the game's own ΔPV. In the sensitivities, the ramp and growth rows are game runs; the margin, price and bill rows are computed from the base case; the discount-rate and horizon rows lie outside the game's convention.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_fps_case_html.py from analysis/fps_business_case/case.json (run dash-2050-sd, corrected demand).</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fps_business_case.html"))
