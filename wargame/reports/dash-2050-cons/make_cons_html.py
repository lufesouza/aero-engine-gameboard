"""Build dash_2050_cons_wargame.html: the dash-2050 ExCo and Board war game replayed on the user's conservative-case
market (run dash-2050-cons): the conservative demand curve with the open firm orders as its first slice (option B),
Boeing losing 1 point of preference a year after NGSA's entry into service with a floor at Airbus's slack, and Airbus
adding 1% capacity a year while it is short.

Every number comes from data/report_data.json (wargame/dashgame/reports.py, from the game record), data/cons_checks.json
(make_cons_checks.py) and, for the comparison, ../dash-2050-sd/data (the previous game, same agents, the earlier market).
The words are in narrative.py.

Usage: python3 make_cons_html.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402
sys.path.insert(0, HERE)
import narrative as NAR  # noqa: E402

esc = K.esc
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
C = json.load(open(os.path.join(HERE, "data", "cons_checks.json")))
PREV = json.load(open(os.path.join(HERE, "..", "dash-2050-sd", "data", "report_data.json")))
PC = json.load(open(os.path.join(HERE, "..", "dash-2050-sd", "data", "sd_checks.json")))
ROUNDS = D["rounds"]
FINAL = ROUNDS[-1]
SD = FINAL["sd"]
PSD = PREV["rounds"][-1]["sd"]
INP = D["sd_inputs"]
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
YEARS = SD["year"]
RYEARS = [r["year"] for r in ROUNDS]
CODE_LABEL = {1: "RR", 2: "P&W", 3: "CFM", 4: "RR & P&W Joint Venture", 5: "RR and CFM", 6: "P&W and CFM", 7: "RR, P&W and CFM"}
X_HI = 2060
assert PSD["year"] == YEARS


def pct(v, dp=0):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def at(series, year):
    return series[YEARS.index(year)]


ORDER_TXT = {
    "fps": {"launch_7yr": "Launch fps, 7-year ramp-up", "launch_10yr": "Launch fps, 10-year ramp-up",
            "launch_via_embraer": "Launch fps via Embraer", "cancel": "Cancel fps"},
    "rate_737": {"increase": "Increase 737 rate"},
    "re787": {"launch": "Launch 787 Re-engine", "cancel": "Cancel 787 Re-engine"},
    "fps_site": {"renton": "fps site: Renton reassigned", "new_site": "fps site: new sites"},
    "ngsa": {"launch": "Launch NGSA", "cancel": "Cancel NGSA"},
    "rea350": {"launch": "Launch A350 Re-engine", "cancel": "Cancel A350 Re-engine"},
    "a320_plan": {"alt": "A320 Alt plan", "base": "A320 base plan"},
    "delay_tactics": {"bottleneck": "Delay Tactics: supply-chain bottleneck (covert)", "poaching": "Delay Tactics: talent poaching (covert)",
                      "both": "Delay Tactics: bottleneck and poaching (covert)"},
    "ducted": {"launch": "Launch ducted engine", "cancel": "Cancel ducted engine"},
    "open_fan": {"launch": "Launch Open Fan", "cancel": "Cancel Open Fan"},
    "partner_embraer": {"launch": "Partner with Embraer", "cancel": "End Embraer partnership"},
    "lobby_emissions": {"launch": "Lobby governments on emissions"},
    "genx": {"upgrade_genx9": "GEnx upgrade", "invest_genx": "GEnx investment", "cancel": "Cancel GEnx programme"},
    "gtf2_solo": {"launch": "Launch GTF2 Solo", "launch_if_selected": "Launch GTF2 if selected", "cancel": "Cancel GTF2"},
    "jv_with_rr": {"commit": "Commit to Joint Venture with RR", "withdraw": "Withdraw Joint Venture commitment"},
    "ultrafan_nb_solo": {"launch": "Launch UltraFan NB Solo", "launch_if_selected": "Launch UltraFan NB if selected", "cancel": "Cancel UltraFan NB"},
    "jv_with_pw": {"commit": "Commit to Joint Venture with P&W", "withdraw": "Withdraw Joint Venture commitment"},
    "ultrafan_wb": {"launch": "Launch UltraFan WB", "cancel": "Cancel UltraFan WB"},
    "t1000_upgrade": {"launch": "Launch Trent 1000 upgrade", "cancel": "Cancel Trent 1000 upgrade"},
}


def order_text(side, o, prev_plans=None, prev_codes=None):
    """Orders in words. A supply plan or engine code restated unchanged is not a move and is left out."""
    o = dict(o or {})
    parts = []
    for k, v in o.items():
        if k.endswith("engine_code") or v in (None, "hold", "none"):
            continue
        if k in ("fps_site", "a320_plan") and prev_plans is not None and prev_plans.get(k) == v:
            continue
        t = ORDER_TXT.get(k, {}).get(v)
        if t:
            if k in ("fps", "ngsa") and str(v).startswith("launch"):
                code = o.get(k + "_engine_code")
                if code:
                    t += f" (engines: {CODE_LABEL[int(code)]})"
            parts.append(t)
    for k in ("fps_engine_code", "ngsa_engine_code"):
        key = k[:-12]
        if o.get(k) and not str(o.get(key, "")).startswith("launch") and not (prev_codes and str(prev_codes.get(key)) == str(o[k])):
            parts.append(f"{'fps' if key == 'fps' else 'NGSA'} engines: {CODE_LABEL[int(o[k])]}")
    return parts or ["Do Nothing"]


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


def lines(series, y_hi, step, fmt, label, aria, refs=(), notes=None, x_lo=2026, x_hi=X_HI, end_fmt=None):
    """Line chart (page_kit.line_chart with dashed series). series: [(name, css var, [(year, value)], dashed)].
    End labels are "name value"; keep names short (the label column is 172 px)."""
    w, h, left, right, top, bot = 760, 346, 58, 172, 26, 46
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / y_hi * (h - top - bot)
    tick = (lambda v: f"{v * 100:.0f}%") if fmt == "pct" else (lambda v: f"{v:,.0f}")
    end_fmt = end_fmt or ((lambda v: pct(v)) if fmt == "pct" else n0)
    notes = [(y, f"Round {j + 1}") for j, y in enumerate(RYEARS)] if notes is None else notes
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="{esc(aria, quote=True)}. Use the arrow keys to read values by year." tabindex="0">']
    t = 0
    while t <= y_hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{tick(t)}</text>')
        t += step
    for yr in range(5 * ((x_lo + 4) // 5), x_hi + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    lab_x = left + 6
    for xv, txt in notes:
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 5:.1f}" y="{top + 11}" class="ann">{esc(txt)}</text>')
        lab_x = max(lab_x, sx(xv) + 6)
    for yv, txt, pos in refs:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(yv):.1f}" y2="{sy(yv):.1f}" class="ref"/>'
                   f'<text x="{lab_x:.1f}" y="{sy(yv) + (15 if pos == "below" else -6):.1f}" class="reflab">{esc(txt)}</text>')
    for name, var, data, dashed in series:
        d = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in data)
        da = ' stroke-dasharray="6 4"' if dashed else ""
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2"{da} stroke-linejoin="round" stroke-linecap="round"/>')
    last = [d[-1][1] for _, _, d, _ in series]
    dys = spread(last, 0, y_hi, plot_h=h - top - bot)
    for (name, var, data, _), dy in zip(series, dys):
        x, v = data[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
        lx = w - right + 8
        if abs(dy) > 2:
            out.append(f'<line x1="{sx(x) + 6:.1f}" x2="{lx - 3:.1f}" y1="{sy(v):.1f}" y2="{sy(v) + dy:.1f}" class="leader"/>')
        out.append(f'<text x="{lx}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(name)} {end_fmt(v)}</text>')
    years = sorted({x for _, _, d, _ in series for x, _ in d})
    payload = {"x0": left, "x1": w - right, "xlo": x_lo, "xhi": x_hi, "w": w, "fmt": fmt, "years": years,
               "series": [{"name": n, "k": f"var(--{c})", "vals": {str(x): v for x, v in d}} for n, c, d, _ in series]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">{esc(label)}</text></svg>')
    return f'<div class="cw">{"".join(out)}</div>'


def legend(items):
    """items: [(label, css var, kind)]; kind 'ln', 'dash' or 'sq'."""
    def key(var, kind):
        if kind in ("ln", "dash"):
            da = ' stroke-dasharray="6 4"' if kind == "dash" else ""
            return (f'<svg width="24" height="4" aria-hidden="true" style="vertical-align:middle;margin-right:6px">'
                    f'<line x1="0" y1="2" x2="24" y2="2" stroke="var(--{var})" stroke-width="2"{da}/></svg>')
        return f'<i class="{kind}" style="background:var(--{var})"></i>'
    return '<div class="legend">' + "".join(f'<span>{key(var, kind)}{esc(lab)}</span>' for lab, var, kind in items) + "</div>"




# ─────────────────────────────── charts ───────────────────────────────
def chart_demand():
    """Stacked columns: each year's demand on the conservative curve, split into firm orders called and new customers;
    the previous game's new demand as a dashed line."""
    w, h, left, right, top, bot = 760, 330, 58, 20, 20, 46
    ys = YEARS
    hi = 2500
    sx = lambda i: left + i * (w - left - right) / len(ys)
    bw = (w - left - right) / len(ys) - 3
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Single-aisle demand a year: open firm orders and new customers, with the previous game's new demand")]
    for t in range(0, hi + 1, 500):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t:,}</text>')
    rows = []
    for i, y in enumerate(ys):
        g, nw = SD["demand_gross"][i], SD["demand"][i]
        fm = g - nw
        pv = PSD["demand"][i]
        x = sx(i) + 1.5
        y0, y1, y2 = sy(0), sy(fm), sy(g)
        tipx = K.mark_attrs((n0(g), f"{y}: demand", None), (n0(fm), "firm orders called", "var(--s2)"),
                            (n0(nw), "new customers", "var(--s1)"), (n0(pv), "previous game, new demand", "var(--sq)"))
        if fm > 0.5:
            if nw > 0.5:
                out.append(f'<rect x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0, y0 - y1):.1f}" fill="var(--s2)"/>')
            else:
                out.append(f'<path d="{K.bar_path(x, bw, y0, y1)}" fill="var(--s2)"/>')
        if nw > 0.5:
            out.append(f'<path d="{K.bar_path(x, bw, y1 - (2 if fm > 0.5 else 0), y2)}" fill="var(--s1)"/>')
        out.append(f'<rect x="{sx(i):.1f}" y="{top}" width="{bw + 3:.1f}" height="{h - top - bot}" class="hit" {tipx}/>')
        if y % 5 == 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
        rows.append([str(y), n0(fm), n0(nw), n0(g), n0(pv)])
    d = "M" + " L".join(f"{sx(i) + 1.5 + bw / 2:.1f},{sy(v):.1f}" for i, v in enumerate(PSD["demand"]))
    out.append(f'<path d="{d}" fill="none" stroke="var(--sq)" stroke-width="2" stroke-dasharray="6 4" stroke-linejoin="round" pointer-events="none"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">Aircraft a year, 737/A320 class (A220 excluded)</text></svg>')
    return (legend([("Open firm orders called by the year's demand", "s2", "sq"), ("New customers", "s1", "sq"),
                    ("Previous game: new demand (its firm orders came on top)", "sq", "dash")])
            + f'<div class="cw">{"".join(out)}</div>'
            + K.tview("Demand a year", ["Year", "Firm orders called", "New customers", "Demand (curve x class share)",
                                        "Previous game, new demand"], rows))


def chart_pref():
    """Boeing's preference: the base rule, with the slack floor, and the share it delivers; the status quo's delivered share."""
    base = SD["pref_b_base"]
    pref = SD["boeing"]["pref_share"]
    dl = SD["boeing"]["delivered_share"]
    sq = [b_ / max(1e-9, b_ + a) for b_, a in zip(SD["sq_delivered_b"], SD["sq_delivered_a"])]
    series = [("Status quo", "sq", list(zip(YEARS, sq)), True), ("Base rule", "s1", list(zip(YEARS, base)), True),
              ("With slack", "s1", list(zip(YEARS, pref)), False), ("Delivered", "fg", list(zip(YEARS, dl)), False)]
    svg = lines(series, .6, .1, "pct", "Boeing share of 737/A320-class customers (preference) and deliveries",
                "Boeing preference: base rule, with Airbus's slack, and delivered share",
                notes=[(NAR.NGSA_EIS, "NGSA in service")])
    rows = [[str(y), pct(base[i], 1), pct(pref[i], 1), pct(dl[i], 1), pct(sq[i], 1)] for i, y in enumerate(YEARS)]
    return (legend([("Base rule: 40% less 1 point a year after NGSA", "s1", "dash"), ("Preference with Airbus's slack", "s1", "ln"),
                    ("Share Boeing delivers", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
            + svg + K.tview("Boeing's preference and delivered share", ["Year", "Base rule", "With Airbus's slack",
                                                                         "Delivered", "Status quo delivered"], rows))


def chart_airbus_cap():
    """Airbus's capacity on its plan and with the 1% response, and its deliveries."""
    capa = [a + n for a, n in zip(SD["cap_a320"], SD["cap_ngsa"])]
    fac = SD["airbus_capacity_factor"]
    plan = [c / f for c, f in zip(capa, fac)]
    dlv = [a + n for a, n in zip(SD["dlv_a320"], SD["dlv_ngsa"])]
    series = [("Rev. B plan", "s2", list(zip(YEARS, plan)), True), ("With 1% steps", "s2", list(zip(YEARS, capa)), False),
              ("Delivered", "fg", list(zip(YEARS, dlv)), False)]
    svg = lines(series, 1600, 200, "int", "Airbus single-aisle aircraft a year (final state of the game)",
                "Airbus capacity: Rev. B plan and with the 1% response; deliveries", notes=[(NAR.NGSA_EIS, "NGSA in service")])
    rows = [[str(y), n0(plan[i]), f"{fac[i]:.3f}", n0(capa[i]), n0(dlv[i])] for i, y in enumerate(YEARS)]
    return (legend([("Capacity on your Rev. B plan (Alt)", "s2", "dash"), ("Capacity with the 1% steps", "s2", "ln"),
                    ("Delivered", "fg", "ln")])
            + svg + K.tview("Airbus capacity", ["Year", "Rev. B plan", "Capacity factor", "With the 1% steps", "Delivered"], rows))


def chart_market():
    """Final state: demand, combined capacity and deliveries; the status quo's deliveries dashed."""
    cap = [a + b_ + c + d for a, b_, c, d in zip(SD["cap_max"], SD["cap_fps"], SD["cap_a320"], SD["cap_ngsa"])]
    dlv = [a + b_ + c + d for a, b_, c, d in zip(SD["dlv_max"], SD["dlv_fps"], SD["dlv_a320"], SD["dlv_ngsa"])]
    sqd = [a + b_ for a, b_ in zip(SD["sq_delivered_b"], SD["sq_delivered_a"])]
    dem = SD["demand_gross"]
    series = [("Status quo", "sq", list(zip(YEARS, sqd)), True), ("Capacity", "muted", list(zip(YEARS, cap)), False),
              ("Demand", "s3", list(zip(YEARS, dem)), False), ("Delivered", "fg", list(zip(YEARS, dlv)), False)]
    svg = lines(series, 2400, 400, "int", "Aircraft a year, Boeing + Airbus (final state of the game)",
                "Supply and demand: capacity, demand and deliveries a year")
    rows = [[str(y), n0(cap[i]), n0(dem[i]), n0(SD["demand"][i]), n0(dlv[i]), n0(SD["firm_b"][i] + SD["firm_a"][i]),
             n0(SD["backlog_b"][i] + SD["backlog_a"][i]), n0(SD["lost"][i]), n0(sqd[i])] for i, y in enumerate(YEARS)]
    return (legend([("Capacity (both makers)", "muted", "ln"), ("Demand (firm orders + new customers)", "s3", "ln"),
                    ("Delivered", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
            + svg + K.tview("Supply and demand by year", ["Year", "Capacity", "Demand", "New customers", "Delivered",
                                                          "Open firm orders at year end", "Waiting customers", "Dropped out",
                                                          "Status quo delivered"], rows))


def chart_lines(side):
    """Final state: capacity by line and deliveries for one airframer."""
    if side == "boeing":
        sr = [("MAX capacity", "s1", SD["cap_max"], False),
              ("Delivered", "fg", [a + b_ for a, b_ in zip(SD["dlv_max"], SD["dlv_fps"])], False),
              ("Status quo", "sq", SD["sq_delivered_b"], True)]
        lg = legend([("737 MAX capacity", "s1", "ln"), ("Delivered", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
        head = ["Year", "737 MAX capacity", "Delivered", "Status quo delivered"]
        assert max(SD["cap_fps"]) < 1e-9
    else:
        sr = [("A320 line", "s2", SD["cap_a320"], False), ("NGSA line", "s3", SD["cap_ngsa"], False),
              ("Delivered", "fg", [a + b_ for a, b_ in zip(SD["dlv_a320"], SD["dlv_ngsa"])], False),
              ("Status quo", "sq", SD["sq_delivered_a"], True)]
        lg = legend([("A320 capacity", "s2", "ln"), ("NGSA capacity", "s3", "ln"), ("Delivered", "fg", "ln"),
                     ("Status quo, delivered", "sq", "dash")])
        head = ["Year", "A320 capacity", "NGSA capacity", "Delivered", "Status quo delivered"]
    series = [(n, c, list(zip(YEARS, v)), d) for n, c, v, d in sr[-1:] + sr[:-1]]
    svg = lines(series, 1400 if side == "boeing" else 1600, 200, "int", f"{NAME[side]} aircraft a year (final state)", f"{NAME[side]} capacity by line and deliveries")
    rows = [[str(y)] + [n0(v[i]) for _, _, v, _ in sr] for i, y in enumerate(YEARS)]
    return lg + svg + K.tview(f"{NAME[side]} capacity and deliveries", head, rows)


def chart_backlog():
    series = [("Boeing firm", "s1", list(zip(YEARS, SD["firm_b"])), False), ("Airbus firm", "s2", list(zip(YEARS, SD["firm_a"])), False),
              ("Boeing waiting", "s1", list(zip(YEARS, SD["backlog_b"])), True), ("Airbus waiting", "s2", list(zip(YEARS, SD["backlog_a"])), True)]
    hi = max(max(v for _, _, d, _ in series for _, v in d) * 1.1, 1000)
    hi = 1000 * (int(hi / 1000) + 1)
    svg = lines(series, hi, 1000, "int", "Aircraft still to deliver at year end (final state)", "Open firm orders and waiting customers by maker")
    rows = [[str(y), n0(SD["firm_b"][i]), n0(SD["firm_a"][i]), n0(SD["backlog_b"][i]), n0(SD["backlog_a"][i]), n0(SD["lost"][i])]
            for i, y in enumerate(YEARS)]
    return svg + K.tview("Open firm orders and waiting customers", ["Year", "Boeing firm", "Airbus firm", "Boeing waiting",
                                                                    "Airbus waiting", "Dropped out"], rows)


def chart_fps():
    """Boeing's deliveries with Do Nothing and with a 10-year fps at Renton from 2030, in this market and the previous one."""
    U = C["fps_units"]
    tot = lambda o: [a + b_ for a, b_ in zip(o["dlv_max"], o["dlv_fps"])]
    yy = U["this_game"]["do_nothing"]["year"]
    assert yy == YEARS
    t_dn, t_f = tot(U["this_game"]["do_nothing"]), tot(U["this_game"]["fps_renton"])
    p_dn, p_f = tot(U["previous_market"]["do_nothing"]), tot(U["previous_market"]["fps_renton"])
    series = [("Was: Do Nothing", "sq", list(zip(yy, p_dn)), True), ("Was: fps", "s3", list(zip(yy, p_f)), True),
              ("Do Nothing", "fg", list(zip(yy, t_dn)), False), ("fps, Renton", "s3", list(zip(yy, t_f)), False)]
    svg = lines(series, 1400, 200, "int", "Boeing aircraft delivered a year, everyone else's round-1 orders as played",
                "Boeing deliveries: Do Nothing against a 10-year fps at Renton from 2030, in this market and the previous one",
                notes=[(U["this_game"]["fps_eis"], "fps in service")])
    rows = [[str(y), n0(t_dn[i]), n0(t_f[i]), n0(t_f[i] - t_dn[i]), n0(p_dn[i]), n0(p_f[i]), n0(p_f[i] - p_dn[i])]
            for i, y in enumerate(yy)]
    return (legend([("Do Nothing, this game", "fg", "ln"), ("10-year fps at Renton, this game", "s3", "ln"),
                    ("Do Nothing, previous market", "sq", "dash"), ("10-year fps at Renton, previous market", "s3", "dash")])
            + svg + K.tview("Boeing deliveries, Do Nothing against the fps", ["Year", "Do Nothing", "fps at Renton", "Difference",
                                                                               "Previous market: Do Nothing", "Previous market: fps",
                                                                               "Previous market: difference"], rows))


def chart_shares():
    pref = SD["boeing"]["pref_share"]
    dl = SD["boeing"]["delivered_share"]
    sq = [b_ / max(1e-9, b_ + a) for b_, a in zip(SD["sq_delivered_b"], SD["sq_delivered_a"])]
    prev = PSD["boeing"]["delivered_share"]
    series = [("Status quo", "sq", list(zip(YEARS, sq)), True), ("Previous game", "muted", list(zip(YEARS, prev)), True),
              ("Preferred", "s1", list(zip(YEARS, pref)), False), ("Delivered", "fg", list(zip(YEARS, dl)), False)]
    svg = lines(series, .6, .1, "pct", "Boeing share of 737/A320-class customers (preferred) and deliveries",
                "Boeing narrowbody share: preferred and delivered", refs=[(.5, "50/50", "above")])
    rows = [[str(y), pct(pref[i], 1), pct(dl[i], 1), pct(sq[i], 1), pct(prev[i], 1)] for i, y in enumerate(YEARS)]
    return (legend([("Preference (with Airbus's slack), as scored", "s1", "ln"), ("What Boeing delivers", "fg", "ln"),
                    ("Status quo, delivered", "sq", "dash"), ("Previous game, delivered", "muted", "dash")])
            + svg + K.tview("Boeing narrowbody share", ["Year", "Preferred", "Delivered", "Status quo delivered", "Previous game delivered"], rows))


# ─────────────────────────────── tables ───────────────────────────────
def moves_table():
    rows = []
    prev_plans = {"fps_site": "new_site", "a320_plan": "base"}
    prev_codes = {}
    for r in ROUNDS:
        cells = []
        for s in SIDES:
            o = r["orders"][s] or {}
            cells.append("<br>".join(esc(t) for t in order_text(s, o, prev_plans, prev_codes)))
        rows.append([f'{r["year"]}'] + cells)
        prev_plans = dict(r["sd"]["plans"])
        prev_codes = dict(r["timeline"]["codes"])
    return K.table(["Round"] + [esc(NAME[s]) for s in SIDES], rows)


def fps_table():
    RI = {x["year"]: x["now"] for x in C["round_items"]}
    RIP = {x["year"]: x["now"] for x in PC["round_items"]}
    z = lambda v: "n/a" if v is None else K.num(v)
    rows = []
    for y in RYEARS:
        a, p = RI[y], RIP[y]
        rows.append([str(y), z(a["fps_10yr_renton"]), z(p["fps_10yr_renton"]), z(a["fps_10yr_new_site"]), z(p["fps_10yr_new_site"]),
                     z(a["fps_7yr_new_site"]), z(a["re787"]), z(a["rea350"])])
    return K.table(["Round", "10-year fps at Renton", "Previous game", "10-year fps, new sites", "Previous game",
                    "7-year fps, new sites", "787 Re-engine", "Airbus: A350 Re-engine, added to its moves"], rows, num_cols=tuple(range(1, 8)))


def value_table():
    rows = []
    for s in SIDES:
        rows.append([esc(NAME[s])] + [K.num(r["value"][s]["pv_delta"]) for r in ROUNDS]
                    + [K.num(PREV["rounds"][-1]["value"][s]["pv_delta"]), K.num(FINAL["value"][s]["pv_delta"] - PREV["rounds"][-1]["value"][s]["pv_delta"])])
    return K.table(["Player"] + [f"After {y}" for y in RYEARS] + ["Previous game, final", "Difference"], rows,
                   num_cols=tuple(range(1, len(RYEARS) + 3)))


BRIDGE_LAB = {"nb_profit_vs_sq": "Narrowbody profit vs status quo (dashboard)", "wb_profit_vs_sq": "Widebody profit vs status quo",
              "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
              "write_offs": "Write-offs", "debt_penalty": "Debt penalty", "two_front_strain": "Two-front strain", "naked_fine": "Naked fine",
              "supply_demand": "Supply and demand: deliveries limited by demand and capacity", "supply_plan": "Supply plans (A320 Alt cost)"}


def bridge_table():
    keys = [k for k in BRIDGE_LAB if any(abs(FINAL["value"][s]["bridge"].get(k, 0) or 0) > 5e-3 for s in ("boeing", "airbus"))]
    z = lambda v: "0.00" if abs(v) < 5e-3 else K.num(v)
    rows = [[esc(BRIDGE_LAB[k])] + [z(FINAL["value"][s]["bridge"].get(k, 0) or 0) for s in ("boeing", "airbus")] for k in keys]
    rows.append(["<b>ΔPV</b>"] + [f'<b>{K.num(FINAL["value"][s]["pv_delta"])}</b>' for s in ("boeing", "airbus")])
    return K.table(["Line, $B PV at 2026", "Boeing", "Airbus"], rows, num_cols=(1, 2))


def steps_table():
    rows = []
    for x in C["steps"]:
        rows.append([esc(x["step"]), K.num(x["fps_renton"]), K.num(x["fps_new_site"])] + [K.num(x["final"][s]) for s in SIDES])
    return K.table(["Market", "2030 fps at Renton vs Do Nothing", "2030 fps, new sites vs Do Nothing"] + [esc(NAME[s]) for s in SIDES],
                   rows, num_cols=tuple(range(1, 8)))


def sens_table():
    rows = []
    for x in C["assumptions"]:
        rows.append([esc(x["case"]), K.num(x["fps_renton"]), K.num(x["fps_new_site"]), K.num(x["final_boeing"]), K.num(x["final_airbus"])])
    return K.table(["Case", "2030 fps at Renton vs Do Nothing", "2030 fps, new sites vs Do Nothing", "Boeing, final ΔPV",
                    "Airbus, final ΔPV"], rows, num_cols=(1, 2, 3, 4))


def inputs_table():
    d = INP["demand"]
    o = INP["options"]
    rows = [
        ["Demand", "Your conservative-case curve (single-aisle, A220 included), fitted to every year, times the 737/A320 class "
         f"share; held at 2070 values after 2070", f"{n0(sum(SD['demand_gross']))} aircraft {YEARS[0]}-{YEARS[-1]}"],
        ["Firm orders (option B)", "Your page's open firm orders, the first slice of each year's demand, split by each maker's "
         "remaining orders; never lapse or switch maker", f"MAX {d['firm_backlog']['boeing']:,}; A320neo family {d['firm_backlog']['airbus']:,}"],
        ["Boeing after NGSA", "Base preference 40% less a fixed step a year from NGSA's entry into service, while no fps is in "
         "service; the dashboard's share rule otherwise", f"{o['boeing_pp_after_ngsa']:.0f} point a year"],
        ["Airbus's slack goes to Boeing", "Boeing's preference is never below the share of new customers Airbus cannot build "
         "after its firm orders and waiting customers (every case, the status quo too)", "on"],
        ["Airbus capacity response", "After each year its customers at the base preference want more than it can build, "
         "Airbus's capacity rises, compounding, from the next year; never falls", pct(o["airbus_capacity_response"])],
        ["Unchanged", "Your Airbus Rev. B plan (Alt plan chosen in 2030); Boeing's 737 MAX path to 57 a month; the fps ramp "
         "and Renton option; flexible customers take the other maker's free slots", pct(d["flex_share"], 1) + " flexible"],
        ["Waiting customers who drop out", "Share of unserved new customers lost each year (not calibrated)", pct(d["lapse_per_year"])],
    ]
    return K.table(["Input", "What it is", "Value"], rows)
def plain_plan(label, rnd):
    """Grid plan labels in the page's words."""
    parts = []
    for p in label.split(" + "):
        p = p.strip()
        if p == "fps: hold":
            p = "no fps"
        elif p == "787: hold":
            p = "no 787 Re-engine"
        elif p == "A350: hold":
            p = "no A350 Re-engine"
        elif p == "737 rate up":
            p = "737 rate increase"
        elif p.startswith("fps 10-yr") or p.startswith("fps 7-yr"):
            p = p.replace("fps 10-yr", "10-year fps").replace("fps 7-yr", "7-year fps")
            p = p if "Renton" in p else p + " at new sites"
        elif p.startswith("NGSA"):
            plan = "Alt plan" if "Alt" in p else "base plan"
            if rnd == 1:
                p = "no NGSA" if p.startswith("NGSA: hold") else f"NGSA launch ({plan})"
            else:
                p = "NGSA cancelled" if "cancel" in p else f"NGSA continues ({plan})"
        elif p == "hold everything":
            p = "Do Nothing"
        elif p in ("GTF2: hold", "UltraFan NB: hold"):
            p = "no " + p.split(":")[0] + " order"
        elif p == "commit to JV":
            p = "commit to the Joint Venture"
        parts.append(p)
    return " + ".join(parts)


def stage_table():
    rows = []
    for r in ROUNDS:
        st = D["stage"].get(str(r["round"]))
        if not st:
            continue
        n = r["round"]
        pp = lambda x: esc(plain_plan(x, n))
        pure = "<br>".join(f"{pp(b_)} / {pp(a)} ({K.num(vb)}, {K.num(va)})" for b_, a, vb, va in st["pure"]) or "none"
        played = f'{pp(st["played"][0])} / {pp(st["played"][1])} ({K.num(st["played_value"][0])}, {K.num(st["played_value"][1])})'
        brb = f'{pp(st["boeing_best_response_to_played_airbus"][0])} ({K.num(st["boeing_best_response_to_played_airbus"][1])})'
        bra = f'{pp(st["airbus_best_response_to_played_boeing"][0])} ({K.num(st["airbus_best_response_to_played_boeing"][1])})'
        rows.append([str(r["year"]), pure, played, brb, bra])
    return K.table(["Round", "Pure Nash equilibria of the round (Boeing / Airbus, ΔPV $B)", "Played", "Boeing's best reply", "Airbus's best reply"], rows)


def regret_table():
    R = D["regret"]
    rows = []
    for s in SIDES:
        cells = []
        for r in ROUNDS:
            x = R[str(r["round"])][s]
            g = x["regret_ex_post"]
            cells.append(K.num(g) if g > 5e-3 else "0")
        rows.append([esc(NAME[s])] + cells)
    return K.table(["Player"] + [str(y) for y in RYEARS], rows, num_cols=tuple(range(1, len(RYEARS) + 1)))


def regret_detail():
    R = D["regret"]
    items = []
    for r in ROUNDS:
        for s in SIDES:
            x = R[str(r["round"])][s]
            if x["regret_ex_post"] > 0.05:
                items.append(f'<li><b>{r["year"]}, {esc(NAME[s])}</b>: best alternative {esc(plain_plan(x["best_ex_post"]["plan"], r["round"]))} '
                             f'({K.num(x["best_ex_post"]["ex_post"])} against {K.num(x["actual_ex_post"])}, regret {K.num(x["regret_ex_post"])})</li>')
    return '<ul class="cav">' + "".join(items) + "</ul>" if items else ""




def tiles():
    out = []
    for s in SIDES:
        v = FINAL["value"][s]["pv_delta"]
        o = PREV["rounds"][-1]["value"][s]["pv_delta"]
        out.append(f'<div class="panel tile"><div class="k">{esc(NAME[s])}</div><div class="v">{b(v)}</div>'
                   f'<div class="d">Previous game {b(o)} ({K.num(v - o)})<br>{esc(NAR.TILES.get(s, ""))}</div></div>')
    return '<div class="tiles">' + "".join(out) + "</div>"


def check_narrative():
    bad = [(side, v, FINAL["value"][side]["pv_delta"]) for side, v in NAR.CHECKS if abs(K.rnd(FINAL["value"][side]["pv_delta"], 2) - v) > 1e-9]
    assert not bad, bad


def panels(items):
    return '<div class="bl">' + "".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in items) + "</div>"


def build(out_path):
    check_narrative()
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;", "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }", "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; color-scheme: dark; }")
    assert css.count("--sq:") >= 2
    css += """
.bl li b { display: inline; font: 600 1em var(--font-body); letter-spacing: 0; margin: 0; }
p, li, footer { overflow-wrap: break-word; }
"""
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conservative Case Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game on the game-theory dashboard · ExCo and Board agents · conservative demand case · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#inputs">Your assumptions</a><a href="#market">Supply and demand</a><a href="#moves">Moves</a>
<a href="#fps">The fps decision</a><a href="#value">Value</a><a href="#shares">Shares</a><a href="#play">Equilibria and regrets</a>
<a href="#compare">Against the previous game</a><a href="#sens">Sensitivities</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}{panels(NAR.FINDINGS)}</section>

<section id="inputs"><h2>Your assumptions</h2><p class="lede">{NAR.INPUTS_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.DEMAND_TITLE)}</p>{chart_demand()}<p class="cap">{NAR.DEMAND_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.PREF_TITLE)}</p>{chart_pref()}<p class="cap">{NAR.PREF_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.AIRBUS_TITLE)}</p>{chart_airbus_cap()}<p class="cap">{NAR.AIRBUS_CAP}</p></div>
<div class="panel"><p class="label">The inputs</p>{inputs_table()}</div>
</div></section>

<section id="market"><h2>Supply and demand as played</h2><p class="lede">{NAR.MARKET_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.MARKET_TITLE)}</p>{chart_market()}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BOEING_LINES_TITLE)}</p>{chart_lines("boeing")}<p class="cap">{NAR.BOEING_LINES_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.AIRBUS_LINES_TITLE)}</p>{chart_lines("airbus")}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BACKLOG_TITLE)}</p>{legend([("Boeing open firm orders", "s1", "ln"), ("Airbus open firm orders", "s2", "ln"), ("Boeing waiting customers", "s1", "dash"), ("Airbus waiting customers", "s2", "dash")])}{chart_backlog()}<p class="cap">{NAR.BACKLOG_CAP}</p></div>
</div></section>

<section id="moves"><h2>Moves by round</h2><p class="lede">{NAR.MOVES_LEDE}</p><div class="panel">{moves_table()}</div>
{panels(NAR.ROUND_NOTES)}</section>

<section id="fps"><h2>The fps decision</h2><p class="lede">{NAR.FPS_LEDE}</p><div class="stack">
<div class="panel"><p class="label">Value against Do Nothing by round, $B PV at 2026 (everyone else's orders as played, nobody moves after the round)</p>{fps_table()}<p class="cap">{NAR.FPS_TABLE_NOTE}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.FPS_TITLE)}</p>{chart_fps()}<p class="cap">{NAR.FPS_CAP}</p></div>
</div></section>

<section id="value"><h2>Value</h2><p class="lede">{NAR.VALUE_LEDE}</p><div class="stack">
<div class="panel"><p class="label">ΔPV vs status quo by round, $B at 2026 (nobody moves after the round)</p>{value_table()}</div>
<div class="panel"><p class="label">How the airframers' final ΔPV is built</p>{bridge_table()}<p class="cap">{NAR.BRIDGE_CAP}</p></div>
</div></section>

<section id="shares"><h2>Market shares</h2><p class="lede">{NAR.SHARES_LEDE}</p><div class="panel"><p class="ctitle">{esc(NAR.SHARES_TITLE)}</p>{chart_shares()}</div></section>

<section id="play"><h2>Equilibria and regrets</h2><p class="lede">{NAR.PLAY_LEDE}</p><div class="stack">
<div class="panel"><p class="label">The airframers' round game</p>{stage_table()}</div>
<div class="panel"><p class="label">Regret by round, $B (final ΔPV of the best alternative minus the actual, everyone else's orders as played)</p>{regret_table()}{regret_detail()}</div>
</div></section>

<section id="compare"><h2>Against the previous game</h2><p class="lede">{NAR.COMPARE_LEDE}</p>
<div class="panel"><p class="label">From the previous game's market to this one, one assumption at a time ($B PV at 2026; final ΔPVs on this game's moves)</p>{steps_table()}</div></section>

<section id="sens"><h2>How much each assumption matters</h2><p class="lede">{NAR.SENS_LEDE}</p>
<div class="panel">{sens_table()}<p class="cap">{NAR.SENS_NOTE}</p></div></section>

<section id="method"><h2>Method and caveats</h2><div class="panel stack">{NAR.METHOD}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_cons_wargame.html"))
