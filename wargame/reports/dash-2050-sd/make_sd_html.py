"""Build dash_2050_sd_wargame.html: the dash-2050 ExCo and Board war game replayed with the supply-and-demand layer
(wargame/dashgame/supply_demand.py): the user's Airbus Rev. B production plan, the user's single-aisle replacement
demand plus fleet growth, the firm backlog, and Boeing's plans (737 MAX to 2050; the fps at new sites or at Renton).

Every number comes from data/report_data.json, written by wargame/dashgame/reports.py from the game record (run
dash-2050-sd), and, for the comparison, from ../dash-2050-obj/data/report_data.json (the same game without supply and
demand). The words are in narrative.py.

Usage: python3 make_sd_html.py [out.html]"""
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
OBJ = json.load(open(os.path.join(HERE, "..", "dash-2050-obj", "data", "report_data.json")))
ROUNDS = D["rounds"]
FINAL = ROUNDS[-1]
SD = FINAL["sd"]
SQ = D["status_quo"]["sd"]
INP = D["sd_inputs"]
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
YEARS = SD["year"]
RYEARS = [r["year"] for r in ROUNDS]
CODE_LABEL = {1: "RR", 2: "P&W", 3: "CFM", 4: "RR & P&W Joint Venture", 5: "RR and CFM", 6: "P&W and CFM", 7: "RR, P&W and CFM"}
X_HI = 2060


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


def chart_airbus_plan():
    """The Airbus Rev. B plan as digitised (annual output, chart dates: NGSA in service mid-2037), and as played."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("sdm", os.path.join(HERE, "..", "..", "dashgame", "supply_demand.py"))
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)
    shift = 0
    ys = list(range(2026, 2051))
    base = [(y, S._rundown("a320_base", shift, y)) for y in ys]
    alt = [(y, S._rundown("a320_alt", shift, y)) for y in ys]
    ng = [(y, S._annual("ngsa", shift, y)) for y in ys]
    tb = [(y, a + n) for (y, a), (_, n) in zip(base, ng)]
    ta = [(y, a + n) for (y, a), (_, n) in zip(alt, ng)]
    series = [("Total, Alt", "fg", ta, False), ("Total, base", "fg", tb, True), ("A320 Alt", "s2", alt, False),
              ("A320 base", "s2", base, True), ("NGSA", "s3", ng, False)]
    svg = lines(series, 1400, 200, "int", "Airbus single-aisle aircraft a year (chart dates: NGSA in service mid-2037)",
                "Airbus Rev. B plan: A320 base and Alt rundown and NGSA ramp, aircraft a year",
                notes=[(2037, "NGSA enters service")], x_hi=2050)
    rows = [[str(y), n0(a), n0(c), n0(n), n0(a + n), n0(c + n)] for (y, a), (_, c), (_, n) in zip(base, alt, ng)]
    return svg + K.tview("Airbus Rev. B plan, aircraft a year", ["Year", "A320 base", "A320 Alt", "NGSA", "Total base", "Total Alt"], rows)


def chart_demand():
    """Stacked columns: new demand = replacement + growth, 2026-2060 (737/A320 class)."""
    w, h, left, right, top, bot = 760, 330, 58, 20, 20, 46
    ys = YEARS
    hi = 2500
    sx = lambda i: left + i * (w - left - right) / len(ys)
    bw = (w - left - right) / len(ys) - 3
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "New single-aisle demand a year: replacement plus growth")]
    for t in range(0, hi + 1, 500):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t:,}</text>')
    for i, y in enumerate(ys):
        rep, gr = SD["replacement"][i], SD["growth"][i]
        x = sx(i) + 1.5
        y0, y1, y2 = sy(0), sy(rep), sy(rep + gr)
        tipx = K.mark_attrs((n0(rep + gr), f"{y}: new demand", None), (n0(rep), "replacement", "var(--s1)"), (n0(gr), "growth", "var(--s3)"))
        if rep > 0.5:
            out.append(f'<rect x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0, y0 - y1):.1f}" fill="var(--s1)"/>')
        out.append(f'<path d="{K.bar_path(x, bw, y1 - (2 if rep > 0.5 else 0), y2)}" fill="var(--s3)"/>')
        out.append(f'<rect x="{sx(i):.1f}" y="{top}" width="{bw + 3:.1f}" height="{h - top - bot}" class="hit" {tipx}/>')
        if y % 5 == 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">Aircraft a year, 737/A320 class (A220 excluded); the firm backlog comes on top</text></svg>')
    rows = [[str(y), n0(r), n0(g), n0(r + g)] for y, r, g in zip(ys, SD["replacement"], SD["growth"])]
    return (legend([("Replacement of today's MAX and A320neo fleets (your Cirium page)", "s1", "sq"),
                    ("Fleet growth (Airbus GMF 2025, Boeing CMO; not in your data)", "s3", "sq")])
            + f'<div class="cw">{"".join(out)}</div>'
            + K.tview("New demand a year", ["Year", "Replacement", "Growth", "New demand"], rows))


def chart_market():
    """Final state: new demand, combined capacity and deliveries; the status quo's deliveries dashed."""
    cap = [a + b_ + c + d for a, b_, c, d in zip(SD["cap_max"], SD["cap_fps"], SD["cap_a320"], SD["cap_ngsa"])]
    dlv = [a + b_ + c + d for a, b_, c, d in zip(SD["dlv_max"], SD["dlv_fps"], SD["dlv_a320"], SD["dlv_ngsa"])]
    sqd = [a + b_ for a, b_ in zip(SD["sq_delivered_b"], SD["sq_delivered_a"])]
    dem = SD["demand"]
    series = [("Status quo", "sq", list(zip(YEARS, sqd)), True), ("Capacity", "muted", list(zip(YEARS, cap)), False),
              ("Demand", "s3", list(zip(YEARS, dem)), False), ("Delivered", "fg", list(zip(YEARS, dlv)), False)]
    svg = lines(series, 2600, 500, "int", "Aircraft a year, Boeing + Airbus (final state of the game)",
                "Supply and demand: capacity, new demand and deliveries a year")
    rows = [[str(y), n0(cap[i]), n0(dem[i]), n0(SD["firm_b"][i] + SD["firm_a"][i]), n0(dlv[i]),
             n0(SD["backlog_b"][i] + SD["backlog_a"][i]), n0(SD["lost"][i]), n0(sqd[i])] for i, y in enumerate(YEARS)]
    return (legend([("Capacity (both makers)", "muted", "ln"), ("New demand (replacement + growth)", "s3", "ln"),
                    ("Delivered (firm backlog first)", "fg", "ln"), ("Status quo, delivered", "sq", "dash")])
            + svg + K.tview("Supply and demand by year", ["Year", "Capacity", "New demand", "Firm backlog left", "Delivered",
                                                          "Waiting backlog", "Lapsed", "Status quo delivered"], rows))


def chart_lines(side):
    """Final state: capacity by line and deliveries for one airframer."""
    if side == "boeing":
        sr = [("MAX line", "s1", SD["cap_max"], False), ("fps line", "s3", SD["cap_fps"], False),
              ("Delivered", "fg", [a + b_ for a, b_ in zip(SD["dlv_max"], SD["dlv_fps"])], False),
              ("Status quo", "sq", SD["sq_delivered_b"], True)]
    else:
        sr = [("A320 line", "s2", SD["cap_a320"], False), ("NGSA line", "s3", SD["cap_ngsa"], False),
              ("Delivered", "fg", [a + b_ for a, b_ in zip(SD["dlv_a320"], SD["dlv_ngsa"])], False),
              ("Status quo", "sq", SD["sq_delivered_a"], True)]
    series = [(n, c, list(zip(YEARS, v)), d) for n, c, v, d in sr[3:] + sr[:3]]
    svg = lines(series, 1400, 200, "int", f"{NAME[side]} aircraft a year (final state)", f"{NAME[side]} capacity by line and deliveries")
    lg = legend([(f"{sr[0][0]} capacity", sr[0][1], "ln"), (f"{sr[1][0]} capacity", "s3", "ln"), ("Delivered", "fg", "ln"),
                 ("Status quo, delivered", "sq", "dash")])
    rows = [[str(y)] + [n0(v[i]) for _, _, v, _ in sr] for i, y in enumerate(YEARS)]
    return lg + svg + K.tview(f"{NAME[side]} capacity and deliveries", ["Year", f"{sr[0][0]} capacity", f"{sr[1][0]} capacity",
                                                                         "Delivered", "Status quo delivered"], rows)


def chart_shares():
    pref = SD["boeing"]["pref_share"]
    dl = SD["boeing"]["delivered_share"]
    sq = [b_ / max(1e-9, b_ + a) for b_, a in zip(SD["sq_delivered_b"], SD["sq_delivered_a"])]
    obj = [x for x in OBJ["rounds"][-1]["years"]["boeing"]["nb_share"]][:len(YEARS)]
    series = [("Status quo", "sq", list(zip(YEARS, sq)), True), ("Previous game", "muted", list(zip(YEARS, obj)), True),
              ("Preferred", "s1", list(zip(YEARS, pref)), False), ("Delivered", "fg", list(zip(YEARS, dl)), False)]
    svg = lines(series, .8, .1, "pct", "Boeing share of 737/A320-class deliveries", "Boeing narrowbody share: preferred and delivered",
                refs=[(.5, "50/50", "above")])
    rows = [[str(y), pct(pref[i], 1), pct(dl[i], 1), pct(sq[i], 1), pct(obj[i], 1)] for i, y in enumerate(YEARS)]
    return (legend([("What customers prefer (the board's share)", "s1", "ln"), ("What Boeing delivers", "fg", "ln"),
                    ("Status quo, delivered", "sq", "dash"), ("Previous game (no supply limits)", "muted", "dash")])
            + svg + K.tview("Boeing narrowbody share", ["Year", "Preferred", "Delivered", "Status quo delivered", "Previous game"], rows))


def chart_backlog():
    series = [("Boeing firm", "s1", list(zip(YEARS, SD["firm_b"])), False), ("Airbus firm", "s2", list(zip(YEARS, SD["firm_a"])), False),
              ("Boeing waiting", "s1", list(zip(YEARS, SD["backlog_b"])), True), ("Airbus waiting", "s2", list(zip(YEARS, SD["backlog_a"])), True)]
    hi = max(max(v for _, _, d, _ in series for _, v in d) * 1.1, 1000)
    hi = 1000 * (int(hi / 1000) + 1)
    return lines(series, hi, 1000 if hi <= 8000 else 2000, "int", "Aircraft still to deliver at year end (final state)",
                 "Firm and waiting backlogs by maker")


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
        pl = r["sd"]["plans"]
        prev_plans = dict(pl)
        prev_codes = dict(r["timeline"]["codes"])
    return K.table(["Round"] + [esc(NAME[s]) for s in SIDES], rows)


def obj_moves_table():
    rows = []
    prev_codes = {}
    for r in OBJ["rounds"]:
        cells = ["<br>".join(esc(t) for t in order_text(s, r["orders"][s] or {}, None, prev_codes)) for s in SIDES]
        rows.append([f'{r["year"]}'] + cells)
        prev_codes = dict(r["timeline"]["codes"])
    return K.table(["Round"] + [esc(NAME[s]) for s in SIDES], rows)


def value_table():
    rows = []
    for s in SIDES:
        rows.append([esc(NAME[s])] + [K.num(r["value"][s]["pv_delta"]) for r in ROUNDS]
                    + [K.num(OBJ["rounds"][-1]["value"][s]["pv_delta"]), K.num(FINAL["value"][s]["pv_delta"] - OBJ["rounds"][-1]["value"][s]["pv_delta"])])
    return K.table(["Player"] + [f"After {y}" for y in RYEARS] + ["Previous game, final", "Difference"], rows,
                   num_cols=tuple(range(1, len(RYEARS) + 3)))


BRIDGE_LAB = {"nb_profit_vs_sq": "Narrowbody profit vs status quo (board)", "wb_profit_vs_sq": "Widebody profit vs status quo",
              "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
              "write_offs": "Write-offs", "debt_penalty": "Debt penalty", "two_front_strain": "Two-front strain", "naked_fine": "Naked fine",
              "supply_demand": "Supply and demand: deliveries limited by capacity and demand", "supply_plan": "Supply plans (A320 Alt cost, Renton saving)"}


def bridge_table():
    keys = [k for k in BRIDGE_LAB if any(abs(FINAL["value"][s]["bridge"].get(k, 0) or 0) > 5e-3 for s in ("boeing", "airbus"))]
    z = lambda v: "0.00" if abs(v) < 5e-3 else K.num(v)
    rows = [[esc(BRIDGE_LAB[k])] + [z(FINAL["value"][s]["bridge"].get(k, 0) or 0) for s in ("boeing", "airbus")] for k in keys]
    rows.append(["<b>ΔPV</b>"] + [f'<b>{K.num(FINAL["value"][s]["pv_delta"])}</b>' for s in ("boeing", "airbus")])
    return K.table(["Line, $B PV at 2026", "Boeing", "Airbus"], rows, num_cols=(1, 2))


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
        o = OBJ["rounds"][-1]["value"][s]["pv_delta"]
        out.append(f'<div class="panel tile"><div class="k">{esc(NAME[s])}</div><div class="v">{b(v)}</div>'
                   f'<div class="d">Previous game {b(o)} ({K.num(v - o)})<br>{esc(NAR.TILES.get(s, ""))}</div></div>')
    return '<div class="tiles">' + "".join(out) + "</div>"


def inputs_table():
    d = INP["demand"]
    bo = INP["boeing"]
    rows = [
        ["Replacement demand", "Your Cirium page: replacements a year of today's 737 MAX, A320neo-family and A220 fleets "
         "(default schedule); the A220 share is taken out", f"{n0(sum(SD['replacement'][:YEARS.index(2045) + 1]))} aircraft 2026-2045"],
        ["Growth", "Not in your data. Single-aisle fleet from 66% of 24,730 aircraft (2024) to 72% of 49,210 (2044), "
         f"{d['fleet_growth_2025_44'] * 100:.2f}% a year, easing to {d['fleet_growth_2060'] * 100:.0f}% by 2060 "
         "(Airbus GMF 2025; Boeing CMO 2025 and 2026)", f"{n0(sum(SD['growth'][:YEARS.index(2045) + 1]))} aircraft 2026-2045"],
        ["Firm backlog", "Your page's firm orders, delivered first, never lapse",
         f"MAX {d['firm_backlog']['boeing']:,}; A320neo family {d['firm_backlog']['airbus']:,}"],
        ["Flexible customers", "Customers flying both types, lessors and unannounced customers (your page, 2030-2060): "
         "they take the other maker's free slots", pct(d["flex_share"], 1)],
        ["Waiting customers who drop out", "Share of unserved new demand lost each year (not calibrated)", pct(d["lapse_per_year"])],
        ["Airbus", "Your Rev. B chart: A320 at 85 a month to NGSA, then the base or Alt rundown; NGSA ramp to 100 a month; "
         "both move with the NGSA date. Alt plan cost", f"${INP['airbus']['alt_cost_b']:.2f}B"],
        ["Boeing 737 MAX", "42.5, 49.5, 52, 54.5 a month (2026-29), then 57. With an fps it gives way to it, down to a "
         "10-a-month tail, and ends in 2050; with no fps it carries on. The 737 rate increase (orderable in 2030 only) adds "
         "100 a year from 2032", f"{bo['max_rate_after'] * 12:,.0f} a year"],
        ["Boeing fps", "Ramps on the NGSA curve from its entry into service; Boeing's single-aisle total is capped at 100 a month",
         f"{bo['total_rate_cap'] * 12:,.0f} a year cap"],
        ["fps site", "New sites (default), or Renton reassigned: Renton's MAX lines (47 a month) wind down as the fps ramps and "
         "Everett carries on at up to 15 a month. Saves the new-site capex, pro-rated if chosen less than 3 years before "
         "entry into service", f"${bo['renton_saving_b']:.1f}B saving"],
    ]
    return K.table(["Input", "What it is", "Value"], rows)


def check_narrative():
    bad = [(side, v, FINAL["value"][side]["pv_delta"]) for side, v in NAR.CHECKS if abs(K.rnd(FINAL["value"][side]["pv_delta"], 2) - v) > 1e-9]
    assert not bad, bad


def build(out_path):
    check_narrative()
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;", "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }", "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; color-scheme: dark; }")
    css += """
.bl li b { display: inline; font: 600 1em var(--font-body); letter-spacing: 0; margin: 0; }
p, li, footer { overflow-wrap: break-word; }
"""
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Supply and Demand Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game on the game-theory dashboard · ExCo and Board agents · supply and demand · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#inputs">What we added</a><a href="#market">Supply and demand</a><a href="#moves">Moves</a>
<a href="#value">Value</a><a href="#shares">Shares</a><a href="#play">Equilibria and regrets</a><a href="#compare">Against the previous game</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.FINDINGS)}</div></section>

<section id="inputs"><h2>What we added: supply and demand</h2><p class="lede">{NAR.INPUTS_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.DEMAND_TITLE)}</p>{chart_demand()}<p class="cap">{NAR.DEMAND_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.AIRBUS_TITLE)}</p>{legend([("A320, Alt plan", "s2", "ln"), ("A320, base plan", "s2", "dash"), ("NGSA", "s3", "ln"), ("Airbus total, Alt", "fg", "ln"), ("Airbus total, base", "fg", "dash")])}{chart_airbus_plan()}<p class="cap">{NAR.AIRBUS_CAP}</p></div>
<div class="panel"><p class="label">The inputs</p>{inputs_table()}</div>
</div></section>

<section id="market"><h2>Supply and demand as played</h2><p class="lede">{NAR.MARKET_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.MARKET_TITLE)}</p>{chart_market()}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BOEING_LINES_TITLE)}</p>{chart_lines("boeing")}<p class="cap">{NAR.BOEING_LINES_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.AIRBUS_LINES_TITLE)}</p>{chart_lines("airbus")}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BACKLOG_TITLE)}</p>{legend([("Boeing firm backlog", "s1", "ln"), ("Airbus firm backlog", "s2", "ln"), ("Boeing waiting customers", "s1", "dash"), ("Airbus waiting customers", "s2", "dash")])}{chart_backlog()}<p class="cap">{NAR.BACKLOG_CAP}</p></div>
</div></section>

<section id="moves"><h2>Moves by round</h2><p class="lede">{NAR.MOVES_LEDE}</p><div class="panel">{moves_table()}</div>
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.ROUND_NOTES)}</div></section>

<section id="value"><h2>Value</h2><p class="lede">{NAR.VALUE_LEDE}</p><div class="stack">
<div class="panel"><p class="label">ΔPV vs status quo by round, $B at 2026 (nobody moves after the round)</p>{value_table()}</div>
<div class="panel"><p class="label">How the airframers' final ΔPV is built</p>{bridge_table()}<p class="cap">{NAR.BRIDGE_CAP}</p></div>
</div></section>

<section id="shares"><h2>Market shares</h2><p class="lede">{NAR.SHARES_LEDE}</p><div class="panel"><p class="ctitle">{esc(NAR.SHARES_TITLE)}</p>{chart_shares()}</div></section>

<section id="play"><h2>Equilibria and regrets</h2><p class="lede">{NAR.PLAY_LEDE}</p><div class="stack">
<div class="panel"><p class="label">The airframers' round game, with supply and demand</p>{stage_table()}</div>
<div class="panel"><p class="label">Regret by round, $B (final ΔPV of the best alternative minus the actual, everyone else's orders as played)</p>{regret_table()}{regret_detail()}</div>
</div></section>

<section id="compare"><h2>Against the previous game</h2><p class="lede">{NAR.COMPARE_LEDE}</p><div class="stack">
<div class="panel"><p class="label">Previous game (dash-2050-obj, no supply limits): moves by round</p>{obj_moves_table()}</div>
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.COMPARE_POINTS)}</div>
</div></section>

<section id="method"><h2>Method and caveats</h2><div class="panel stack">{NAR.METHOD}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_sd_wargame.html"))
