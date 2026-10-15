"""Build do_nothing_case.html: Boeing's Do Nothing case on the conservative-case market (run dash-2050-cons), broken
down: the market-share rules for Boeing and Airbus (the dashboard's, the user's, the slack floor, the capacity
response, the status quo), the volumes, the prices and margins, and how each maker's ΔPV is built.

Every number comes from analysis/do_nothing/do_nothing.json (do_nothing.py; its bridges are checked against the
game's ΔPV).

Usage: python3 make_do_nothing_html.py [out.html]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
J = json.load(open(os.path.join(HERE, "analysis", "do_nothing", "do_nothing.json")))
ROWS = J["rows"]
BY = {r["year"]: r for r in ROWS}
YEARS = [r["year"] for r in ROWS]
PR = J["prices"]
DSH = J["dashboard"]
V = J["value"]
DA = J["dashboard_alone"]
NGSA = J["ngsa"]["eis"]
WIN_B, WIN_A = J["windows"]["boeing"], J["windows"]["airbus"]
MINUS = K.MINUS


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def pc(v, dp=0):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def legend(items):
    def key(var, kind):
        if kind in ("ln", "dash"):
            da = ' stroke-dasharray="6 4"' if kind == "dash" else ""
            return (f'<svg width="24" height="4" aria-hidden="true" style="vertical-align:middle;margin-right:6px">'
                    f'<line x1="0" y1="2" x2="24" y2="2" stroke="var(--{var})" stroke-width="2"{da}/></svg>')
        return f'<i class="sq" style="background:var(--{var})"></i>'
    return '<div class="legend">' + "".join(f'<span>{key(v, k)}{esc(l)}</span>' for l, v, k in items) + "</div>"


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


def lines(series, y_lo, y_hi, step, fmt, label, aria, notes=(), x_lo=2026, x_hi=2060):
    """series: [(end label, css var, [(year, value)], dashed)]."""
    w, h, left, right, top, bot = 760, 346, 58, 190, 26, 46
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / (y_hi - y_lo) * (h - top - bot)
    tick = (lambda v: f"{v * 100:.0f}%") if fmt == "pct" else ((lambda v: (K.num(v, "+.1f" if step < 1 else "+.0f") if abs(v) > 1e-9 else "0")) if fmt == "usd" else (lambda v: f"{v:,.0f}"))
    endf = (lambda v: pc(v)) if fmt == "pct" else ((lambda v: bp(v, 1)) if fmt == "usd" else n0)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="{esc(aria, quote=True)}. Use the arrow keys to read values by year." tabindex="0">']
    t = y_lo
    while t <= y_hi + 1e-9:
        cls = "zero" if abs(t) < 1e-9 and y_lo < 0 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{tick(t)}</text>')
        t += step
    for yr in range(2030, x_hi + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    for xv, txt in notes:
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 5:.1f}" y="{top + 11}" class="ann">{esc(txt)}</text>')
    for name, var, data, dashed in series:
        d = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in data)
        da = ' stroke-dasharray="6 4"' if dashed else ""
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2"{da} stroke-linejoin="round" stroke-linecap="round"/>')
    dys = spread([d[-1][1] for _, _, d, _ in series], y_lo, y_hi, plot_h=h - top - bot)
    for (name, var, data, _), dy in zip(series, dys):
        x, v = data[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
        lx = w - right + 8
        if abs(dy) > 2:
            out.append(f'<line x1="{sx(x) + 6:.1f}" x2="{lx - 3:.1f}" y1="{sy(v):.1f}" y2="{sy(v) + dy:.1f}" class="leader"/>')
        out.append(f'<text x="{lx}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(name)} {endf(v)}</text>')
    years = sorted({x for _, _, d, _ in series for x, _ in d})
    payload = {"x0": left, "x1": w - right, "xlo": x_lo, "xhi": x_hi, "w": w, "fmt": fmt, "years": years,
               "series": [{"name": n, "k": f"var(--{c})", "vals": {str(x): (v if fmt == "pct" else round(v, 2)) for x, v in d}} for n, c, d, _ in series]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">{esc(label)}</text></svg>')
    return f'<div class="cw">{"".join(out)}</div>'


ser = lambda key, f=lambda x: x: [(r["year"], f(r[key])) for r in ROWS]


# ─────────────────────────────── facts ───────────────────────────────
FLOOR = [r["year"] for r in ROWS if r["pref_b"] > r["base_pref_b"] + 1e-6]
PEAK = max(ROWS, key=lambda r: r["pref_b"])
DASH20 = next(r["year"] for r in ROWS if abs(r["board_share_b"] - min(x["board_share_b"] for x in ROWS)) < 1e-9)
SOLD = [r["year"] for r in ROWS if abs(r["dlv_b"] - r["cap_b"]) < 0.5]
SOLD_RUN = []
for y in SOLD:
    if y >= 2035 and (not SOLD_RUN or y == SOLD_RUN[-1] + 1):
        SOLD_RUN.append(y)
FADE = SOLD_RUN[-1] + 1
SAME_AS_SQ = [r["year"] for r in ROWS if abs(r["dlv_b"] - r["sq_dlv_b"]) < 0.5]
GAP_B = {r["year"]: r["profit_b"] - r["sq_profit_b"] for r in ROWS}
GAP_A = {r["year"]: r["profit_a"] - r["sq_profit_a"] for r in ROWS}
BGAP_B = {r["year"]: r["board_profit_b"] - r["board_sq_profit_b"] for r in ROWS}
FIRST_LOSS = next(y for y in YEARS if GAP_B[y] < -1e-6)
assert all(abs(GAP_B[y]) < 1e-6 for y in YEARS if y < FIRST_LOSS)
U = {k: x["unit_profit_m"] for k, x in PR.items()}
CS = J["inputs"]["demand"]["class_share"]
SQP_MAX = max(((r["year"], r["sq_pref_b"]) for r in ROWS), key=lambda t: t[1])
FIRM_SHARE = J["inputs"]["demand"]["firm_backlog"]["boeing"] / (J["inputs"]["demand"]["firm_backlog"]["boeing"] + J["inputs"]["demand"]["firm_backlog"]["airbus"])
A_DIP = min((r for r in ROWS if r["year"] >= NGSA), key=lambda r: r["dlv_a"])
A_STEADY = [GAP_A[y] for y in YEARS if 2044 <= y <= WIN_A[1]]
A320_LAST = max(r["year"] for r in ROWS if r["dlv_a320"] > 0.5)
BR_B, BR_A = V["boeing"]["bridge"], V["airbus"]["bridge"]


def chart_share(side):
    if side == "boeing":
        sr = [("Status quo", "sq", ser("sq_delivered_share_b"), True), ("SQ preference", "sq", ser("sq_pref_b"), False), ("Dashboard", "muted", ser("board_share_b"), True),
              ("Your rule", "s1", ser("base_pref_b"), True), ("Preference", "s1", ser("pref_b"), False),
              ("Delivered", "fg", ser("delivered_share_b"), False)]
        lo, hi = 0.0, 0.6
    else:
        sr = [("Status quo", "sq", ser("sq_delivered_share_a"), True), ("SQ preference", "sq", ser("sq_pref_b", lambda v: 1 - v), False), ("Dashboard", "muted", ser("board_share_a"), True),
              ("Your rule", "s2", ser("base_pref_b", lambda v: 1 - v), True), ("Preference", "s2", ser("pref_a"), False),
              ("Delivered", "fg", ser("delivered_share_a"), False)]
        lo, hi = 0.4, 1.0
    svg = lines(sr, lo, hi, 0.1, "pct", f"{'Boeing' if side == 'boeing' else 'Airbus'} share of 737/A320-class customers and deliveries",
                f"{'Boeing' if side == 'boeing' else 'Airbus'} narrowbody share in Do Nothing", notes=[(NGSA, "NGSA in service")])
    col = "s1" if side == "boeing" else "s2"
    lg = legend([("Dashboard's share rule (what the dashboard alone books)", "muted", "dash"), ("Your rule: 1 point a year after NGSA", col, "dash"),
                 ("Preference after Airbus's slack (what the game uses)", col, "ln"), ("Share of deliveries", "fg", "ln"),
                 ("Status quo, preference after the slack", "sq", "ln"), ("Status quo, share of deliveries", "sq", "dash")])
    k = "b" if side == "boeing" else "a"
    rows = [[str(r["year"]), pc(r[f"board_share_{k}"], 1), pc(r["base_pref_b"] if k == "b" else 1 - r["base_pref_b"], 1), pc(r[f"pref_{k}"], 1),
             pc(r[f"delivered_share_{k}"], 1), pc(r["sq_pref_b"] if k == "b" else 1 - r["sq_pref_b"], 1), pc(r[f"sq_delivered_share_{k}"], 1)] for r in ROWS]
    return lg + svg + K.tview(f"{'Boeing' if side == 'boeing' else 'Airbus'} narrowbody share", ["Year", "Dashboard", "Your rule", "Preference",
                                                                                                "Delivered", "Status quo preference", "Status quo delivered"], rows)


def chart_volumes(side):
    if side == "boeing":
        sr = [("Status quo", "sq", ser("sq_dlv_b"), True), ("Capacity", "muted", ser("cap_b"), False), ("Delivered", "fg", ser("dlv_b"), False)]
        hi = 800
        rows = [[str(r["year"]), n0(r["cap_b"]), n0(r["dlv_b"]), n0(r["sq_dlv_b"]), n0(r["waiting_b"]), n0(r["firm_b"])] for r in ROWS]
        head = ["Year", "737 MAX capacity", "Delivered", "Status quo delivered", "Customers waiting for Boeing", "Open firm orders"]
        lg = legend([("737 MAX capacity", "muted", "ln"), ("Delivered", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
    else:
        sr = [("Status quo", "sq", ser("sq_dlv_a"), True), ("Capacity", "muted", [(r["year"], r["cap_a320"] + r["cap_ngsa"]) for r in ROWS], False),
              ("A320neo", "s2", ser("dlv_a320"), False), ("NGSA", "s3", ser("dlv_ngsa"), False), ("Delivered", "fg", ser("dlv_a"), False)]
        hi = 1600
        rows = [[str(r["year"]), n0(r["cap_a320"] + r["cap_ngsa"]), f"{r['airbus_capacity_factor']:.3f}", n0(r["dlv_a320"]), n0(r["dlv_ngsa"]),
                 n0(r["dlv_a"]), n0(r["sq_dlv_a"]), n0(r["waiting_a"])] for r in ROWS]
        head = ["Year", "Capacity", "Capacity factor", "A320neo delivered", "NGSA delivered", "Delivered", "Status quo delivered", "Customers waiting"]
        lg = legend([("Capacity (A320 + NGSA, with the 1% steps)", "muted", "ln"), ("A320neo delivered", "s2", "ln"), ("NGSA delivered", "s3", "ln"),
                     ("Delivered, total", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
    svg = lines(sr, 0, hi, 200, "int", f"{'Boeing' if side == 'boeing' else 'Airbus'} narrowbodies a year", f"{'Boeing' if side == 'boeing' else 'Airbus'} capacity and deliveries in Do Nothing",
                notes=[(NGSA, "NGSA in service")])
    return lg + svg + K.tview(f"{'Boeing' if side == 'boeing' else 'Airbus'} volumes", head, rows)


def chart_profit_gap():
    sr = [("Dashboard", "muted", [(y, BGAP_B[y]) for y in YEARS if BY[y]["in_window_b"]], True),
          ("This game", "s1", [(y, GAP_B[y]) for y in YEARS if BY[y]["in_window_b"]], False)]
    svg = lines(sr, -2.0, 0.5, 0.5, "usd", "Boeing narrowbody operating profit, Do Nothing minus status quo, $B a year (2026 dollars)",
                "Boeing's narrowbody profit against the status quo, dashboard alone and this game", notes=[(NGSA, "NGSA in service")])
    rows = [[str(y), K.num(BGAP_B[y]), K.num(GAP_B[y]), f"{BY[y]['df_b']:.3f}"] for y in YEARS if BY[y]["in_window_b"]]
    lg = legend([("Dashboard alone: 2,000 a year at the dashboard's shares", "muted", "dash"), ("This game: as delivered", "s1", "ln")])
    return lg + svg + K.tview("Boeing profit against the status quo", ["Year", "Dashboard alone", "This game", "Discount factor"], rows)


def chart_airbus_gap():
    sr = [("Dashboard", "muted", [(y, BY[y]["board_profit_a"] - BY[y]["board_sq_profit_a"]) for y in YEARS if BY[y]["in_window_a"]], True),
          ("This game", "s2", [(y, GAP_A[y]) for y in YEARS if BY[y]["in_window_a"]], False)]
    svg = lines(sr, -4.0, 20.0, 4.0, "usd", "Airbus narrowbody operating profit, Do Nothing minus status quo, $B a year (2026 dollars)",
                "Airbus's narrowbody profit against the status quo, dashboard alone and this game", notes=[(NGSA, "NGSA in service")], x_hi=WIN_A[1])
    rows = [[str(y), K.num(BY[y]["board_profit_a"] - BY[y]["board_sq_profit_a"]), K.num(GAP_A[y]), f"{BY[y]['df_a']:.3f}"] for y in YEARS if BY[y]["in_window_a"]]
    lg = legend([("Dashboard alone", "muted", "dash"), ("This game: as delivered", "s2", "ln")])
    return lg + svg + K.tview("Airbus profit against the status quo", ["Year", "Dashboard alone", "This game", "Discount factor"], rows)


# ─────────────────────────────── tables ───────────────────────────────
def rules_table():
    o = J["inputs"]["options"]
    d = J["inputs"]["demand"]
    rows = [
        ["Dashboard's share rule", "What the dashboard alone books (and the game in the dashboard-only valuation): 2,000 narrowbodies a year, "
         f"Boeing 40% and Airbus 60% until NGSA enters service in {NGSA}, then Airbus gains 3 points a year to 80% "
         f"(Boeing {pc(BY[NGSA]['board_share_b'])} in {NGSA}, 20% from {DASH20}). Every aircraft is sold.", "Not used for deliveries in this game"],
        ["Your rule: Boeing's base preference", f"40% less {o['boeing_pp_after_ngsa']:.0f} point a year from NGSA's entry into service while Boeing has no new narrowbody: "
         f"{pc(BY[NGSA]['base_pref_b'])} in {NGSA}, {pc(BY[2050]['base_pref_b'])} in 2050, {pc(BY[2060]['base_pref_b'])} in 2060. Airbus gets the rest.", "Yours"],
        ["Airbus's slack goes to Boeing", "Boeing's preference is never below the share of new customers Airbus cannot build after its own firm orders and "
         f"waiting customers. It lifts Boeing in {len(FLOOR)} years, most in {PEAK['year']} ({pc(PEAK['pref_b'], 1)}), when NGSA's transition cuts Airbus's output.", "Yours"],
        ["Airbus adds capacity when short", f"+{pc(o['airbus_capacity_response'])} after each year its customers want more than it can build; "
         f"{pc(BY[2060]['airbus_capacity_factor'] - 1, 1)} above its plan by 2060.", "Yours"],
        ["Market measured", f"Your conservative curve (whole single-aisle market) times the 737/A320 class share, {pc(CS, 2)}: the A220 is "
         "taken out. Every share here is a share of 737/A320-class customers or deliveries.", "Yours (curve); game master (class share)"],
        ["Firm orders (option B)", f"The {d['firm_backlog']['boeing'] + d['firm_backlog']['airbus']:,} open firm orders are the first slice of each year's demand, split by "
         f"each maker's remaining orders: Boeing {d['firm_backlog']['boeing']:,} ({pc(FIRM_SHARE, 1)}), Airbus {d['firm_backlog']['airbus']:,}. That is why "
         f"Boeing's delivered share is {pc(FIRM_SHARE, 1)} until new customers start in 2035.", "Yours"],
        ["Customers who cannot be served", f"{pc(d['flex_share'], 1)} of them take the other maker's free slots; {pc(d['lapse_per_year'])} of those still "
         "waiting drop out each year.", "Game master"],
        ["Status quo", "Nobody launches anything. Boeing's base preference stays at 40% and Airbus's at 60%; the same slack floor and capacity "
         f"response apply, so the status quo also runs into Airbus's limits (Boeing's preference up to {pc(SQP_MAX[1], 1)} in {SQP_MAX[0]}).", "Game master"],
    ]
    return K.table(["Rule", "What it does in Do Nothing", "Source"], rows)


def price_table():
    rows = []
    note = {"737 MAX": "Every Boeing narrowbody in Do Nothing and the status quo",
            "A320neo family": f"Airbus's narrowbodies before NGSA, and the A320s still built after it (Alt plan, last delivered {A320_LAST}); every Airbus narrowbody in the status quo",
            "NGSA": f"Airbus's new narrowbody from {NGSA}: NGSAs are delivered first, at the NGSA price and margin",
            "fps (for reference)": "Not built in Do Nothing",
            "787 (widebody)": f"Boeing's widebody, {pc(DSH['boeing_wb_share'], 1)} of {DSH['wb_per_year']} widebodies a year in both Do Nothing and the status quo, so it does not move ΔPV",
            "A350 (widebody)": "Airbus's widebody; unchanged in Do Nothing"}
    for k, x in PR.items():
        extra = f" (alone {pc(x['alone'], 2)}; both re-engined {pc(x['both'], 2)})" if "alone" in x else ""
        rows.append([esc(k), f"${x['price_m']:.0f}M", pc(x["margin"], 2) + extra, f"${x['unit_profit_m']:.2f}M", esc(note[k])])
    return K.table(["Aircraft", "Price", "Operating margin", "Operating profit an aircraft", "Where it applies in Do Nothing"], rows)


def bridge_table():
    lab = {"nb_profit_vs_sq": "Narrowbody profit vs status quo, dashboard alone", "supply_demand": "Supply and demand: deliveries as built and wanted",
           "programme_investment": "Programme investment (NGSA bill)", "debt_penalty": "Debt penalty", "supply_plan": "A320 Alt plan cost"}
    rows = []
    for k, l in lab.items():
        vb, va = BR_B.get(k, 0.0) or 0.0, BR_A.get(k, 0.0) or 0.0
        if abs(vb) > 5e-3 or abs(va) > 5e-3:
            rows.append([l, K.num(vb) if abs(vb) > 5e-3 else "0.00", K.num(va) if abs(va) > 5e-3 else "0.00"])
    rows.append(["<b>ΔPV against the status quo</b>", f"<b>{K.num(V['boeing']['pv_delta'])}</b>", f"<b>{K.num(V['airbus']['pv_delta'])}</b>"])
    rows.append(["Same moves, dashboard alone", K.num(DA["boeing"]), K.num(DA["airbus"])])
    return K.table(["$B, present value at 2026", "Boeing", "Airbus"], rows, num_cols=(1, 2))


def year_table():
    head = ["Year", "Demand", "Boeing: dashboard", "Boeing: your rule", "Boeing: preference", "Boeing: delivered share", "Boeing: delivered",
            "Boeing: status quo delivered", "Boeing profit vs status quo", "Airbus: preference", "Airbus: delivered share", "Airbus: A320neo delivered",
            "Airbus: NGSA delivered", "Airbus: status quo delivered", "Airbus profit vs status quo"]
    rows = []
    for r in ROWS:
        rows.append([str(r["year"]), n0(r["demand_gross"]), pc(r["board_share_b"]), pc(r["base_pref_b"]), pc(r["pref_b"], 1), pc(r["delivered_share_b"], 1),
                     n0(r["dlv_b"]), n0(r["sq_dlv_b"]), K.num(GAP_B[r["year"]]), pc(r["pref_a"], 1), pc(r["delivered_share_a"], 1),
                     n0(r["dlv_a320"]), n0(r["dlv_ngsa"]), n0(r["sq_dlv_a"]), K.num(GAP_A[r["year"]]) if r["in_window_a"] else "—"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def tiles():
    t = [("Boeing ΔPV, Do Nothing", b(V["boeing"]["pv_delta"]), f"Against the status quo. On the dashboard alone {b(DA['boeing'])}."),
         ("Airbus ΔPV, same case", b(V["airbus"]["pv_delta"]), f"NGSA launched in 2030. On the dashboard alone {b(DA['airbus'])}."),
         ("Boeing share in 2060", pc(BY[2060]["delivered_share_b"]), f"Of deliveries; {pc(BY[2060]['sq_delivered_share_b'])} in the status quo. Airbus {pc(BY[2060]['delivered_share_a'])}."),
         ("Boeing deliveries in 2060", n0(BY[2060]["dlv_b"]), f"Against {n0(BY[2060]['sq_dlv_b'])} in the status quo; the same as the status quo until {FIRST_LOSS - 1}.")]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v}</div><div class="d">{d_}</div></div>'
                                           for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;", "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }", "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; color-scheme: dark; }")
    assert css.count("--sq:") >= 2
    old = "const fmt = v => P.fmt === 'pct' ? Math.round(v * 100) + '%' : Math.round(v).toLocaleString('en-US');"
    assert K.JS.count(old) == 1
    JS = K.JS.replace(old, "const fmt = v => P.fmt === 'pct' ? Math.round(v * 100) + '%' : P.fmt === 'usd' ? (v < -0.005 ? '\\u2212' : (v > 0.005 ? '+' : '')) + '$' + Math.abs(v).toFixed(2) + 'B' : Math.round(v).toLocaleString('en-US');")
    css += "\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }\n"
    gap_b = [GAP_B[y] for y in YEARS if y >= FIRST_LOSS and BY[y]["in_window_b"]]
    dash_floor = BGAP_B[DASH20]
    findings = [
        ("Boeing loses nothing until " + str(FIRST_LOSS - 1) + ".",
         f" In Do Nothing Boeing builds and sells exactly what it builds in the status quo, every year to {FIRST_LOSS - 1}: the 737 MAX line is "
         f"full (684 a year from 2035) in both. Your 1-point rule would cut Boeing's preference from {NGSA}, but Airbus cannot build the share it "
         f"wins, so its slack keeps Boeing's line full to {SOLD_RUN[-1]}. From {FADE} Airbus, {pc(BY[FADE]['airbus_capacity_factor'] - 1)} above "
         f"its plan, can serve nearly all its customers, and Boeing's deliveries fall to {n0(BY[2060]['dlv_b'])} in 2060 "
         f"(status quo {n0(BY[2060]['sq_dlv_b'])}). The profit gap is {bp(max(gap_b), 1)} to {bp(min(gap_b), 1)} a year, late and heavily "
         f"discounted: {b(V['boeing']['pv_delta'])} in all."),
        ("The dashboard alone sees a much bigger loss.",
         f" It sells 2,000 narrowbodies a year and moves Airbus 3 points a year from NGSA's entry into service, so Boeing falls to 20% (400 "
         f"aircraft) from {DASH20}, against 800 in the status quo. At ${U['737 MAX']:.2f}M an aircraft that is {bp(dash_floor, 2)} a year from "
         f"{DASH20}, after a ramp from {bp(BGAP_B[NGSA], 2)} in {NGSA}: {b(DA['boeing'])} in all."),
        ("Airbus's gain is NGSA's margin.",
         f" NGSA earns ${U['NGSA']:.2f}M an aircraft against ${U['A320neo family']:.2f}M for an A320neo, and Airbus builds "
         f"{n0(BY[2050]['dlv_a'])} a year by 2050 against {n0(BY[2050]['sq_dlv_a'])} in the status quo. From 2044 that is "
         f"{bp(min(A_STEADY), 1, False)}-{bp(max(A_STEADY), 1, False)} a year more profit. Against it: the ${DSH['ngsa_bill_b']:.2f}B NGSA "
         f"bill, the transition dip ({n0(A_DIP['dlv_a'])} aircraft in {A_DIP['year']}) and the Alt plan's cost. Airbus ends at "
         f"{b(V['airbus']['pv_delta'])}, against {b(DA['airbus'])} on the dashboard alone, where it sells 1,600 NGSAs a year."),
    ]
    panels = '<div class="bl">' + "".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in findings) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Do Nothing Breakdown</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · conservative-case war game (dash-2050-cons) · BOEING PROPRIETARY</p>
<h1>The Do Nothing case, broken down</h1>
<p class="lede">Boeing launches nothing in 2030: no fps, no 787 Re-engine, no rate increase. Airbus launches NGSA in 2030 on the
A320 Alt plan, in service {NGSA}, as played. Nobody moves after 2030. Every value is measured against the status quo, in which
nobody launches anything. Below: the market-share rules for Boeing and Airbus, the volumes they produce, the prices and margins,
and how each maker's value is built.</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#shares">Market shares</a><a href="#volumes">Volumes</a><a href="#prices">Prices</a><a href="#value">Value</a><a href="#years">Year by year</a><a href="#notes">Notes</a></nav></header>

<section id="summary" style="margin-top:22px">{tiles()}{panels}</section>

<section id="shares"><h2>Market-share assumptions</h2><p class="lede">Two kinds of share. <b>Preference</b> is the share
of customers who want each maker's aircraft; the rules below set it. <b>Delivered share</b> is what each maker actually builds
and sells, once demand, the firm orders and both makers' factories are applied. The game values deliveries.</p><div class="stack">
<div class="panel"><p class="label">The rules</p>{rules_table()}</div>
<div class="panel"><p class="ctitle">Boeing: your rule takes its preference from 40% to {pc(BY[2060]['base_pref_b'])}, but Airbus's slack holds it up until {FLOOR[-1]}; Boeing delivers {pc(BY[2060]['delivered_share_b'])} by 2060</p>{chart_share("boeing")}</div>
<div class="panel"><p class="ctitle">Airbus: preference rises from 60% to {pc(BY[2060]['pref_a'])}; it delivers {pc(BY[2060]['delivered_share_a'])} of the market by 2060, against {pc(BY[2060]['sq_delivered_share_a'])} in the status quo</p>{chart_share("airbus")}</div>
</div></section>

<section id="volumes"><h2>Volumes</h2><p class="lede">Your conservative demand curve sets the market, times the 737/A320 class
share ({pc(CS, 2)}: the A220 is taken out, so every share on this page is a share of the 737/A320 class): {n0(BY[2026]['demand_gross'])}
aircraft in 2026, a peak of {n0(max(r['demand_gross'] for r in ROWS))} in {max(ROWS, key=lambda r: r['demand_gross'])['year']}, {n0(BY[2060]['demand_gross'])}
in 2060 (737/A320 class). The firm orders are delivered first, as each year's demand calls them; new customers start in 2035.</p><div class="stack">
<div class="panel"><p class="ctitle">Boeing builds 684 a year from 2035 in both cases until {SOLD_RUN[-1]}; then its line runs below capacity</p>{chart_volumes("boeing")}</div>
<div class="panel"><p class="ctitle">Airbus: NGSA's transition cuts output to {n0(A_DIP['dlv_a'])} in {A_DIP['year']}, then NGSA and the 1% steps take it to {n0(BY[2060]['dlv_a'])} a year</p>{chart_volumes("airbus")}</div>
</div></section>

<section id="prices"><h2>Price and margin assumptions</h2><p class="lede">All from your dashboard (v3 snapshot), in constant
2026 dollars with no escalation. The game multiplies each year's deliveries by these: new types (NGSA) are delivered first at the
new type's price and margin, the rest at today's. Boeing discounts at {pc(DSH['wacc_b'], 1)}, Airbus at {pc(DSH['wacc_a'], 1)}.</p>
<div class="panel">{price_table()}<p class="cap">The widebody margins depend on who re-engines: the dashboard's base margin, its margin if that maker re-engines alone, and if both do. Neither re-engines in Do Nothing.</p></div></section>

<section id="value"><h2>How the value is built</h2><p class="lede">Each maker's ΔPV is its narrowbody operating profit
minus the status quo's, year by year, discounted to 2026, over its programme window, less any programme bill. Airbus counts
{WIN_A[0]}-{WIN_A[1]}, to 19 years after NGSA's entry into service. Boeing, with no new narrowbody, counts {WIN_B[0]}-{WIN_B[1]}, to 19 years
after the dashboard's default fps date ({WIN_B[1] - 19}). The dashboard's line is its own
2,000-a-year view; the supply-and-demand line replaces it with what was actually built and sold.</p><div class="stack">
<div class="panel">{bridge_table()}</div>
<div class="panel"><p class="ctitle">Boeing: nothing lost until {FIRST_LOSS - 1}, then {bp(max(gap_b), 1)} to {bp(min(gap_b), 1)} a year; the dashboard books {bp(dash_floor)} a year from {DASH20}</p>{chart_profit_gap()}</div>
<div class="panel"><p class="ctitle">Airbus: a dip in the NGSA transition, then {bp(min(A_STEADY), 1)}-{bp(max(A_STEADY), 1, False)} a year more profit from 2044</p>{chart_airbus_gap()}</div>
</div></section>

<section id="years"><h2>Year by year</h2><p class="lede">Shares as percentages, aircraft a year, profit in $B a year (2026
dollars) against the status quo. Airbus's profit is counted to {WIN_A[1]}.</p><div class="panel">{year_table()}</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Same case as the business case.</b> This is the Do Nothing the fps is measured against on the fps business case page, and the state Boeing actually ended in.</li>
<li><b>The status quo runs into Airbus's limits too.</b> Boeing's base preference stays at 40%, but Airbus is short in the status quo as well, so the slack lifts Boeing's preference to as much as {pc(SQP_MAX[1], 1)} ({SQP_MAX[0]}); its capacity grows {pc(BY[2060]['sq_capacity_factor_a'] - 1, 1)} by 2060 and the slack keeps Boeing's line full until demand falls in the late 2050s.</li>
<li><b>What is yours, what is ours.</b> The demand curve, option B, the 1-point rule, the slack floor and the 1% response are yours; the prices, margins, bills and the dashboard's share rule are your dashboard's; the 737/A320 class share, the 737 MAX path, the flexible and drop-out rates and the Airbus plan's digitisation are the game master's.</li>
<li><b>Source.</b> analysis/do_nothing/do_nothing.py writes do_nothing.json; it checks that the layer's rows are the ones the valuation used, that the prices are the ones applied, and that both makers' narrowbody lines add up to the game's ΔPV.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_do_nothing_html.py from analysis/do_nothing/do_nothing.json (run dash-2050-cons).</footer></div>
<script>{JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "do_nothing_case.html"))
