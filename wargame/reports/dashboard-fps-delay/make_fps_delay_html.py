"""Build fps_delay_assessment.html: the 3-year fps delay on the user's dashboard (business case, Airbus's response,
third-player odds, engine makers). Board numbers are read from analysis/results/*.json (reproduce with
analysis/run_all.sh). Probabilities and web facts are judgement/evidence from review/ and are written inline.

Usage: python3 make_fps_delay_html.py [out.html]"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "analysis", "results")
J = lambda n: json.load(open(os.path.join(RES, n + ".json")))
DELAY, A2, VAC, ENG, ENGALL, ROB, REC, PAGE = (J("delay"), J("analysis2"), J("vacuum"), J("engines"), J("engines_all"),
                                               J("robustness"), J("recovery_threshold"), J("page_data"))
esc = html.escape
MOD = "NGSA + Re-engine A350"
DT = "NGSA + Bottleneck + Re-engine A350"


def num(v, f="+.2f"):
    """Format with a true minus sign, rounding halves away from zero (as the markdown report does)."""
    if f.endswith("f"):
        from decimal import Decimal, ROUND_HALF_UP
        dp = int(f.split(".")[1][:-1])
        v = float(Decimal(str(v)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))
    return format(v, f).replace("-", "−")


def tip(*rows):
    """data-tip payload: rows of (value, label, key-colour or None). Rendered with textContent in JS."""
    return esc(json.dumps([{"v": v, "l": l, "k": k} for v, l, k in rows]), quote=True)


def bar_path(x, w, y0, y1, r=4):
    """Column from baseline y0 to y1, 4px rounded at the data end, square at the baseline."""
    top, bot = min(y0, y1), max(y0, y1)
    h = bot - top
    r = min(r, h / 2, w / 2)
    if y1 < y0:   # grows up: round the top
        return (f"M{x:.1f},{bot:.1f}V{top + r:.1f}Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f}H{x + w - r:.1f}"
                f"Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f}V{bot:.1f}Z")
    return (f"M{x:.1f},{top:.1f}V{bot - r:.1f}Q{x:.1f},{bot:.1f} {x + r:.1f},{bot:.1f}H{x + w - r:.1f}"
            f"Q{x + w:.1f},{bot:.1f} {x + w:.1f},{bot - r:.1f}V{top:.1f}Z")


def hbar_path(x0, x1, y, h, r=4):
    """Horizontal bar from baseline x0 to x1, rounded at the data end."""
    left, right = min(x0, x1), max(x0, x1)
    w = right - left
    r = min(r, w / 2, h / 2)
    if x1 > x0:
        return (f"M{left:.1f},{y:.1f}H{right - r:.1f}Q{right:.1f},{y:.1f} {right:.1f},{y + r:.1f}V{y + h - r:.1f}"
                f"Q{right:.1f},{y + h:.1f} {right - r:.1f},{y + h:.1f}H{left:.1f}Z")
    return (f"M{right:.1f},{y:.1f}H{left + r:.1f}Q{left:.1f},{y:.1f} {left:.1f},{y + r:.1f}V{y + h - r:.1f}"
            f"Q{left:.1f},{y + h:.1f} {left + r:.1f},{y + h:.1f}H{right:.1f}Z")


# ------------------------------------------------------------------ chart 1: fps value by entry year
def chart_eis():
    rows = DELAY["sweep_fps_eis"]
    key = "NGSA + Re-engine A350 | Milk_787 | fps10-DN"
    w, h, left, right, top, bot = 760, 330, 52, 16, 30, 86
    lo, hi = -4, 10
    n = len(rows)
    band = (w - left - right) / n
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Boeing fps 10-year minus Do Nothing by fps entry year, 2037 to 2047">']
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    yb = h - bot + 22
    out.append(f'<text x="{left - 8}" y="{yb + 30:.1f}" text-anchor="end" class="tick">in eq.</text>')
    for i, r in enumerate(rows):
        v, y, eq = r[key], r["fps_eis"], r["fps_in_any_eq"]
        bw = min(24, band * .55)
        x = left + i * band + (band - bw) / 2
        cx = x + bw / 2
        hl = y in (2041, 2044)
        cls = ("pos" if v >= 0 else "neg") + (" hl" if hl else "")
        out.append(f'<path d="{bar_path(x, bw, sy(0), sy(v))}" class="b {cls}"/>')
        out.append(f'<text x="{cx:.1f}" y="{yb:.1f}" text-anchor="middle" class="tick{" strong" if hl else ""}">{y}</text>')
        out.append(f'<circle cx="{cx:.1f}" cy="{yb + 26:.1f}" r="4.5" class="{"eqy" if eq else "eqn"}"/>')
        if hl:
            ly = sy(v) - 8 if v >= 0 else sy(v) + 17
            out.append(f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle" class="val">{num(v)}</text>')
            cap = "Snapshot" if y == 2041 else "3-year delay"
            out.append(f'<text x="{cx:.1f}" y="{top - 12}" text-anchor="middle" class="ann">{cap}</text>'
                       f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{top - 6}" y2="{min(sy(v), sy(0)) - (16 if v >= 0 else 4):.1f}" class="leader"/>')
        out.append(f'<rect x="{left + i * band:.1f}" y="{top}" width="{band:.1f}" height="{h - top - bot + 44}" class="hit" tabindex="0" '
                   f'data-tip="{tip((num(v) + " $B", f"fps {y}: fps 10-year minus Do Nothing", None), ("yes" if eq else "no", "fps in any equilibrium", None))}"/>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">$B PV-2026 · Airbus NGSA + Re-engine A350 · Boeing Do Nothing on the 787</text>')
    out.append("</svg>")
    table = "".join(f"<tr><td>{r['fps_eis']}</td><td class='n'>{num(r[key])}</td><td>{'yes' if r['fps_in_any_eq'] else 'no'}</td></tr>" for r in rows)
    return "".join(out), table


# ------------------------------------------------------------------ chart 2: bridge 2041 -> 2044
def bridge_steps():
    d41 = DELAY["snapshot_2041"]["decomp_fps10_vs_dn"][MOD]
    d44 = DELAY["delay3_2044"]["decomp_fps10_vs_dn"][MOD]
    sp = A2["nb_split"]
    return [("fps 2041", d41["b_total_delta"], "total"),
            ("Same cash,\n3 years later", sp["timing_only"], "step"),
            ("Deeper\nshare hole", sp["share_effect"], "step"),
            ("Bill paid later\n(present value)", d41["fps_pv_capex"] - d44["fps_pv_capex"], "step"),
            ("Lower debt\npenalty", d41["fps_alpha_pen"] - d44["fps_alpha_pen"], "step"),
            ("fps 2044", d44["b_total_delta"], "total")]


def chart_bridge():
    steps = bridge_steps()
    w, h, left, right, top, bot = 760, 330, 52, 16, 20, 62
    lo, hi = -8, 2
    n = len(steps)
    band = (w - left - right) / n
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Bridge from fps 2041 (+1.06) to fps 2044 (−2.53), $B">']
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    run = 0.0
    bw = 24 * 1.6
    for i, (lab, v, kind) in enumerate(steps):
        x = left + i * band + (band - bw) / 2
        cx = x + bw / 2
        if kind == "total":
            y0, y1 = sy(0), sy(v)
            run = v
            cls = "t41" if i == 0 else "t44"
            vy = sy(v) - 8 if v >= 0 else sy(v) + 17
        else:
            y0, y1 = sy(run), sy(run + v)
            cls = "pos" if v >= 0 else "neg"
            vy = min(y0, y1) - 8
            run += v
        if kind == "total" or abs(y1 - y0) >= 2:
            path = bar_path(x, bw, y0, y1) if kind == "total" else (
                f"M{x:.1f},{min(y0, y1):.1f}h{bw:.1f}v{abs(y1 - y0):.1f}h{-bw:.1f}Z")
            out.append(f'<path d="{path}" class="b {cls}"/>')
        out.append(f'<text x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle" class="val">{num(v)}</text>')
        if i < n - 1:
            nx = left + (i + 1) * band + (band - bw) / 2
            out.append(f'<line x1="{x + bw:.1f}" x2="{nx:.1f}" y1="{sy(run):.1f}" y2="{sy(run):.1f}" class="leader"/>')
        for k, part in enumerate(lab.split("\n")):
            out.append(f'<text x="{cx:.1f}" y="{h - bot + 20 + k * 14:.1f}" text-anchor="middle" class="tick{" strong" if kind == "total" else ""}">{esc(part)}</text>')
        out.append(f'<rect x="{left + i * band:.1f}" y="{top}" width="{band:.1f}" height="{h - top - bot}" class="hit" tabindex="0" '
                   f'data-tip="{tip((num(v) + " $B", lab.replace(chr(10), " "), None))}"/>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ line charts with a crosshair
SCEN = [("fps 2041", "s1"), ("fps 2044", "s2"), ("Boeing Do Nothing", "s3")]


def line_chart(series, y_lo, y_hi, y_step, y_fmt, label, refs=(), aria="", x_lo=2026, x_hi=2063, end_labels=None, notes=(), wash=None):
    """series: [(name, css-var, [(year, value)])]. y_fmt: 'pct' or 'int'."""
    w, h, left, right, top, bot = 760, 340, 56, 150, 24, 40
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / (y_hi - y_lo) * (h - top - bot)
    fmt = (lambda v: f"{v * 100:.0f}%") if y_fmt == "pct" else (lambda v: f"{v:,.0f}")
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="{esc(aria)}" tabindex="0">']
    t = y_lo
    while t <= y_hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{fmt(t)}</text>')
        t += y_step
    for yr in range(2030, x_hi + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    for ref in refs:
        yv, txt = ref[0], ref[1]
        below = len(ref) > 2 and ref[2] == "below"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(yv):.1f}" y2="{sy(yv):.1f}" class="ref"/>'
                   f'<text x="{left + 6}" y="{sy(yv) + (14 if below else -5):.1f}" class="reflab">{esc(txt)}</text>')
    for xv, txt in notes:
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 4:.1f}" y="{top + 10}" class="ann">{esc(txt)}</text>')
    if wash:
        name, var, base = wash
        pts = [(x, v) for n, c, d in series if n == name for x, v in d if v > base]
        if pts:
            poly = " ".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in pts) + " " + " ".join(f"{sx(x):.1f},{sy(base):.1f}" for x, v in reversed(pts))
            out.append(f'<polygon points="{poly}" fill="var(--{var})" opacity=".12"/>')
    for name, var, data in series:
        d = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in data)
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for name, var, data in series:
        x, v = data[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
    for (name, var, data), (dy, txt) in zip(series, end_labels or [(0, None)] * len(series)):
        x, v = data[-1]
        lab = txt or f"{name}: {fmt(v)}"
        out.append(f'<line x1="{sx(x) + 6:.1f}" x2="{w - right + 2:.1f}" y1="{sy(v):.1f}" y2="{sy(v) + dy:.1f}" class="leader"/>'
                   f'<text x="{w - right + 6}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(lab)}</text>')
    years = sorted({x for _, _, d in series for x, _ in d})
    payload = {"x0": left, "x1": w - right, "xlo": x_lo, "xhi": x_hi, "top": top, "bot": h - bot, "fmt": y_fmt,
               "years": years, "series": [{"name": n, "k": f"var(--{c})", "vals": {str(x): v for x, v in d}} for n, c, d in series]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">{esc(label)}</text></svg>')
    return "".join(out)


def chart_share():
    p = PAGE["paths"]
    ser = [(n, c, [(y, b) for y, b, a, u in p[n]]) for n, c in SCEN]
    svg = line_chart(ser, 0, .6, .1, "pct", "Boeing share of narrowbody deliveries (board rule)",
                     refs=[(.5, "50/50 balance")], aria="Boeing narrowbody share by year: fps 2041, fps 2044, Boeing Do Nothing",
                     end_labels=[(0, "fps 2041: 48%"), (0, "fps 2044: 40%"), (0, "Do Nothing: 20%")],
                     notes=[(2037, "NGSA enters")])
    years = range(2035, 2064)
    rows = "".join("<tr><td>{}</td>{}</tr>".format(y, "".join(
        "<td class='n'>{}</td>".format(next((f"{b * 100:.0f}%" for yy, b, a, u in p[n] if yy == y), "—")) for n, _ in SCEN)) for y in years)
    return svg, rows


def chart_airbus_units():
    p = PAGE["paths"]
    ser = [(n, c, [(y, u) for y, b, a, u in p[n] if y >= 2030]) for n, c in SCEN]
    svg = line_chart(ser, 800, 1700, 100, "int", "Airbus narrowbody deliveries a year implied by the board (2,000-a-year market)",
                     refs=[(900, "Rate 75 (stated plan)"), (1200, "~100 a month (reported)", "below")],
                     aria="Airbus deliveries per year implied by the board, against rate 75 and about 100 a month",
                     x_lo=2030, end_labels=[(14, "fps 2041: 1,040"), (0, "fps 2044: 1,200"), (-14, "Do Nothing: 1,600")],
                     notes=[(2037, "NGSA enters")], wash=("Boeing Do Nothing", "s3", 1200))
    years = range(2035, 2064)
    rows = "".join("<tr><td>{}</td>{}</tr>".format(y, "".join(
        "<td class='n'>{}</td>".format(next((f"{u:,}" for yy, b, a, u in p[n] if yy == y), "—")) for n, _ in SCEN)) for y in years)
    return svg, rows


# ------------------------------------------------------------------ chart 4: NGSA lead
def chart_lead():
    w, h, left, right, top, bot = 760, 360, 52, 16, 64, 60
    lo, hi = -5, 7
    leads = list(range(9, -1, -1))
    band = (w - left - right) / len(leads)
    sx = lambda L: left + (9 - L) * band + band / 2
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="fps 10-year minus Do Nothing by NGSA head start, for fps 2041 and fps 2044">']
    zones = [(9, 6, "fps in no equilibrium"), (5, 5, "near-Nash\nonly"), (4, 4, "no pure\neq. at all"), (3, 0, "fps in every pure equilibrium")]
    for i, (a, b, txt) in enumerate(zones):
        x0 = left + (9 - a) * band
        x1 = left + (9 - b + 1) * band
        if i % 2 == 1:
            out.append(f'<rect x="{x0:.1f}" y="{top - 30}" width="{x1 - x0:.1f}" height="{h - bot - top + 30}" class="zone"/>')
        parts = txt.split("\n")
        for k, part in enumerate(parts):
            out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{top - 14 - (len(parts) - 1 - k) * 12}" text-anchor="middle" class="zlab">{esc(part)}</text>')
    for t in range(-4, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    for L in leads:
        out.append(f'<text x="{sx(L):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{L} yr</text>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - bot + 36}" text-anchor="middle" class="tick">NGSA head start over fps (years)</text>')
    for fe, var in (("2041", "s1"), ("2044", "s2")):
        rows = {r["lead"]: r for r in PAGE["ngsa_lead"][fe]}
        d = "M" + " L".join(f"{sx(L):.1f},{sy(rows[L]['fps_minus_dn']):.1f}" for L in leads)
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2" stroke-linejoin="round"/>')
        for L in leads:
            r = rows[L]
            status = ("fps in every pure equilibrium" if r["fps_in_pure"] else
                      f"fps in {r['fps_in_near']} near-Nash cells, {r['pure']} pure equilibria" if r["fps_in_near"] else "fps in no equilibrium")
            head = "fps {}, NGSA {} ({}-year lead)".format(fe, r["ngsa_eis"], L)
            payload = tip((num(r["fps_minus_dn"]) + " $B", head, "var(--" + var + ")"),
                          (num(r["fps_minus_dn_vs_delay_tactics"]) + " $B", "against Delay Tactics", None), (status, "", None))
            out.append(f'<g class="pt" tabindex="0" data-tip="{payload}">'
                       f'<circle cx="{sx(L):.1f}" cy="{sy(r["fps_minus_dn"]):.1f}" r="12" class="hitc"/>'
                       f'<circle cx="{sx(L):.1f}" cy="{sy(r["fps_minus_dn"]):.1f}" r="4" fill="var(--{var})" class="ring"/></g>')
    # annotations sit in empty space: the snapshot label up-left of its point, the delay label below the lines
    for fe, L, txt, tx, tyv, anchor in (("2041", 4, "Snapshot: fps 2041, 4-yr lead", 6.5, 3.6, "middle"),
                                         ("2044", 7, "Delay: fps 2044, 7-yr lead", 6.2, -4.45, "start")):
        r = {r["lead"]: r for r in PAGE["ngsa_lead"][fe]}[L]
        cx, cy = sx(L), sy(r["fps_minus_dn"])
        lx, ly = sx(tx), sy(tyv)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9" class="mark"/>'
                   f'<line x1="{cx:.1f}" y1="{cy + (-10 if ly < cy else 10):.1f}" x2="{lx + (0 if anchor == "middle" else -4):.1f}" y2="{ly + (6 if ly < cy else -14):.1f}" class="leader"/>'
                   f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="val">{esc(txt)} ({num(r["fps_minus_dn"])})</text>')
    out.append("</svg>")
    table = "".join("<tr><td>{} yr</td>{}</tr>".format(L, "".join(
        "<td class='n'>{}</td><td>{}</td>".format(num(r["fps_minus_dn"]),
            "every pure eq." if r["fps_in_pure"] else ("near-Nash only" if r["fps_in_near"] else "none"))
        for fe in ("2041", "2044") for r in [{x["lead"]: x for x in PAGE["ngsa_lead"][fe]}[L]])) for L in leads)
    return "".join(out), table


# ------------------------------------------------------------------ chart 5: readings of the delay
def chart_readings():
    bt = ROB["bill_timing"]
    rows = [("Board rule: bill paid at entry into service (planned later programme)", bt["board_lump"]["2041"], bt["board_lump"]["2044"]),
            ("Slip found after the bill is committed on the 2041 schedule", None, bt["lump_at_2041"]["2044"]),
            ("…plus a 30% overrun paid at the new date", None, bt["lump_at_2041_plus_30pct_at_2044"]["2044"]),
            ("Bill spread over the 6 years before entry", bt["spread6"]["2041"], bt["spread6"]["2044"]),
            ("Bill spread over the 9 years before entry", bt["spread9"]["2041"], bt["spread9"]["2044"]),
            ("Spent over 9 years on the 2041 schedule, then a 3-year slip", None, bt["slip_spread9"]["2044"])]
    w, left, right, top, rowh = 760, 300, 64, 14, 48
    h = top + rowh * len(rows) + 40
    lo, hi = -24, 4
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="fps 10-year minus Do Nothing under six readings of the delay">']
    for t in range(lo, hi + 1, 4):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 34}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 18}" text-anchor="middle" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    for i, (lab, a, b) in enumerate(rows):
        y = top + i * rowh
        cy = y + rowh / 2
        words, line, lines = lab.split(), "", []
        for wd in words:
            if len(line) + len(wd) > 38:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        for k, ln in enumerate(lines):
            out.append(f'<text x="{left - 14}" y="{cy - (len(lines) - 1) * 7 + k * 14 + 4:.1f}" text-anchor="end" class="rowlab sm">{esc(ln)}</text>')
        out.append(f'<path d="{hbar_path(sx(0), sx(b), cy - 9, 18)}" class="b neg"/>')
        out.append(f'<text x="{sx(b) - 6:.1f}" y="{cy + 4:.1f}" text-anchor="end" class="val">{num(b)}</text>')
        if a is not None:
            out.append(f'<circle cx="{sx(a):.1f}" cy="{cy:.1f}" r="6" class="hollow"/>')
            if a >= 0:
                out.append(f'<text x="{sx(a) + 10:.1f}" y="{cy + 4:.1f}" class="val muted">{num(a)}</text>')
            else:
                out.append(f'<text x="{sx(a):.1f}" y="{cy - 11:.1f}" text-anchor="middle" class="val muted sm">{num(a)}</text>')
        tips = [(num(b) + " $B", "fps 2044", None)] + ([(num(a) + " $B", "fps 2041", None)] if a is not None else [])
        out.append(f'<rect x="0" y="{y:.1f}" width="{w}" height="{rowh}" class="hit" tabindex="0" data-tip="{tip(*tips)}"/>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 2}" text-anchor="middle" class="tick">fps 10-year minus Do Nothing, $B PV-2026</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ chart 7: odds
ODDS = [("Third player", [("Embraer, independent entrant", 6, 10, "Clean sheet with sovereign or industrial partners, launched by 2035"),
                          ("COMAC, real exporter outside China", 11, 15, "EASA-validated C919 at 100+ a year abroad, or a funded export-grade new single-aisle"),
                          ("Embraer or COMAC (combined)", 15, 22, "They compete for the same gap, so slightly below independent odds")]),
        ("Not a third player", [("Boeing–Embraer Joint Venture or buy-back", 10, 12, "Embraer's engineering goes into Boeing's product"),
                                ("COMAC supplies 40%+ of China's deliveries", 45, 50, "Takes Boeing's China share; the bigger effect on Boeing")])]


def chart_odds():
    w, left, right, top, rowh = 760, 300, 40, 10, 40
    n = sum(len(r) for _, r in ODDS) + len(ODDS)
    h = top + rowh * n + 40
    lo, hi = 0, 60
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Probabilities with fps 2041 and fps 2044 (judgement)">']
    for t in range(lo, hi + 1, 10):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 34}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 18}" text-anchor="middle" class="tick">{t}%</text>')
    i = 0
    for grp, rows in ODDS:
        y = top + i * rowh + rowh / 2 + 6
        out.append(f'<text x="{left - 14}" y="{y:.1f}" text-anchor="end" class="grp">{esc(grp.upper())}</text>')
        i += 1
        for lab, a, b, note in rows:
            cy = top + i * rowh + rowh / 2
            strong = "combined" in lab
            out.append(f'<text x="{left - 14}" y="{cy + 4:.1f}" text-anchor="end" class="rowlab sm{" strong" if strong else ""}">{esc(lab)}</text>')
            out.append(f'<line x1="{sx(a) + 7:.1f}" x2="{sx(b) - 6:.1f}" y1="{cy:.1f}" y2="{cy:.1f}" class="conn"/>')
            out.append(f'<circle cx="{sx(a):.1f}" cy="{cy:.1f}" r="6" class="hollow"/><circle cx="{sx(b):.1f}" cy="{cy:.1f}" r="5.5" class="filled"/>')
            out.append(f'<text x="{sx(b) + 12:.1f}" y="{cy + 4:.1f}" class="val">{a}% → {b}%</text>')
            out.append(f'<rect x="0" y="{cy - rowh / 2:.1f}" width="{w}" height="{rowh}" class="hit" tabindex="0" '
                       f'data-tip="{tip((f"{a}% → {b}%", lab, None), (note, "", None))}"/>')
            i += 1
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 2}" text-anchor="middle" class="tick">Probability (judgement): ring = fps 2041, dot = fps 2044</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ chart 8: engine makers
def chart_engines():
    names = list(ENG.keys())
    scen = [(names[0], "Snapshot (fps 2041)", "s1"), (names[1], "fps launched late", "s2"), (names[2], "Boeing Do Nothing (737 on LEAP)", "s3")]
    makers = [("cfm", "CFM/GE", "cfm_b"), ("pratt_whitney", "Pratt & Whitney", "pw_b"), ("rolls_royce", "Rolls-Royce", "rr_b")]
    w, left, right, top = 760, 150, 30, 10
    bh, gap, grp = 14, 4, 22
    h = top + len(makers) * (3 * (bh + gap) + grp) + 40
    lo, hi = -70, 30
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Engine makers’ payoffs in three narrowbody outcomes">']
    for t in range(lo, hi + 1, 10):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 34}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 18}" text-anchor="middle" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    y = top
    for pk, pn, fld in makers:
        out.append(f'<rect x="{left - 140}" y="{y + 3 * (bh + gap) / 2 - 5:.1f}" width="10" height="10" rx="3" fill="var(--{pk})"/>'
                   f'<text x="{left - 124}" y="{y + 3 * (bh + gap) / 2 + 4:.1f}" class="rowlab">{esc(pn)}</text>')
        for k, sn, var in scen:
            v = ENG[k]["pure"][0][fld]
            if abs(v) > 0.05:
                out.append(f'<path d="{hbar_path(sx(0), sx(v), y, bh)}" fill="var(--{var})"/>')
            tx = sx(v) + (6 if v >= 0 else -6)
            out.append(f'<text x="{tx:.1f}" y="{y + bh - 3:.1f}" text-anchor="{"start" if v >= 0 else "end"}" class="val">{"0" if abs(v) < 0.05 else num(v, "+.1f")}</text>')
            out.append(f'<rect x="0" y="{y - gap / 2:.1f}" width="{w}" height="{bh + gap}" class="hit" tabindex="0" '
                       f'data-tip="{tip((num(v, "+.2f") + " $B", f"{pn}: {sn}", f"var(--{var})"))}"/>')
            y += bh + gap
        y += grp
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 2}" text-anchor="middle" class="tick">$B PV-2026 against the engine board’s status quo, pure equilibrium</text>')
    out.append("</svg>")
    leg = "".join(f'<span><i class="sq" style="background:var(--{var})"></i>{esc(sn)}</span>' for _, sn, var in scen)
    return "".join(out), leg


# ------------------------------------------------------------------ page sections
def table(head, rows, cls="", num_cols=()):
    th = "".join(f'<th scope="col"{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join(
        (f'<th scope="row">{c}</th>' if j == 0 else f'<td{" class=n" if j in num_cols else ""}>{c}</td>') for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def details(title, inner):
    return f'<details class="tv"><summary>{esc(title)}</summary>{inner}</details>'


def airbus_cards():
    D = [("NGSA timing", [("Keep the plan: 2030 launch, ~2037 entry into service", 65), ("Slip for technology reasons", 25), ("Pull earlier", 10)],
          "Each year of NGSA slip costs Airbus $2.6–3.3B against a Boeing that does nothing ($4.7–5.3B against fps), and at a 5-year lead or less fps comes back. Each year earlier pays about $3.8–4.1B.",
          "Profile rule “own clock”: don’t wait for Boeing; its default is the technology-ready year (entry 2035). Both war games launched NGSA in 2028 for 2035; the late-fps game noted “a delayed fps does not change it”. Public plan (Farnborough, July 2026): launch 2030, entry in the second half of the 2030s."),
         ("Delay Tactics", [("Drop them (if NGSA holds)", 95), ("Keep in reserve for a visible fps launch", 5)],
          "Worth +$1.16B only if Boeing actually launches fps. Against a Boeing that does nothing they cost −$12.5B: the $48.3B naked fine is about $12.1B in present value, plus about $0.4B of operating cost. They pay only if Boeing launches with more than ~91% probability.",
          "The war-game Airbus never used them in either game: always below its $1B test and against its integrity pillar. The profile says stop Delay Tactics once fps is off."),
         ("Widebody Chicken (now the main contest)", [("Stay out once Boeing re-engines the 787 first", 50), ("Pre-empt with an A350 Re-engine", 30), ("Both re-engine", 10), ("Neither", 10)],
          "A350 Re-engine alone +50.12; stay out +47.68; both +45.36. Pre-empting gains +1.8 if Boeing stays out but loses −2.3 if Boeing re-engines anyway, so it fails Airbus’s own test of beating Do Nothing by $1B against every plausible Boeing move.",
          "Late-fps war game: Boeing, freed from fps, re-engined the 787 first (2031); Airbus deferred, then shelved (+$0.33B). On-time game: Airbus pre-empted while Boeing was busy with fps."),
         ("Price (not on the board)", [("Hold or raise prices on scarce slots", 60), ("Targeted launch-price campaigns at Boeing and COMAC customers", 30), ("Broad price war", 10)],
          "+1 point of NGSA margin is worth about $3.8B on the board’s conventions.",
          "Airbus priced up on slot scarcity before (the neo premium) and is paid on EBIT and free cash flow; July 2026 brought a €5B buyback over 3 years."),
         ("Capacity (not on the board)", [("Hold rate 75 and price the scarcity", 40), ("Add 5–10%, timed to NGSA, with engine deals", 30), ("Size NGSA for ~100 a month", 20), ("Absorb or partner (A220-500, CSeries precedent)", 10)],
          "The delay’s whole gain to Airbus is narrowbody volume above its current capacity (see the chart below).",
          "Stated plan: 70–75 a month by end-2027, “stabilising at rate 75”, gated by engines. 2026 reports: NGSA prepared for about 100 a month (Aviation Week, June 2026; Air Data News, 7 Oct 2026; search snippets only); rate 83 under study for the A320neo (Leeham, August 2026). Airbus historically out-ramped Boeing and opened new lines in 2025–26.")]
    out = []
    for title, opts, board, ev in D:
        top_p = max(p for _, p in opts)
        bars = "".join(f'<li class="{"top" if p == top_p else ""}"><span class="ol">{esc(o)}</span><span class="pb"><span class="pf" style="width:{p}%"></span></span>'
                       f'<span class="pv">{p}%</span></li>' for o, p in opts)
        out.append(f'<article class="panel dcard"><h3>{esc(title)}</h3><ul class="probs" aria-label="Probabilities (judgement)">{bars}</ul>'
                   f'<p class="label">On the board</p><p>{esc(board)}</p><p class="label">Profile and war games</p><p class="muted">{esc(ev)}</p></article>')
    return "".join(out)


CSS = r"""
:root {
  --bg: #f4f6f9; --surface: #ffffff; --sunk: #eef2f7; --line: #d5dce6; --grid: #e3e8ef;
  --fg: #141c28; --muted: #556275; --faint: #8a95a5;
  --boeing: #2a78d6; --airbus: #e34948; --pratt_whitney: #4a3aa7; --rolls_royce: #eda100; --cfm: #008300;
  --s1: #2a78d6; --s2: #eb6834; --s3: #1baf7a;
  --pos: #3b4a5e; --neg: #9aa6b6; --tot: #141c28;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --r: 8px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #22a32a;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70;
  --pos: #c9d3e0; --neg: #5d6a7c; --tot: #e7ecf3; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #22a32a;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70;
  --pos: #c9d3e0; --neg: #5d6a7c; --tot: #e7ecf3; color-scheme: dark; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
.wrap { max-width: 1140px; margin: 0 auto; padding: 0 20px 56px; }
header.top { padding: 34px 0 10px; }
.eyebrow { font: 500 .74rem/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
h1 { font: 700 clamp(2.1rem, 5vw, 3.2rem)/1.02 var(--font-display); margin: 10px 0 12px; letter-spacing: .01em; }
h2 { font: 700 1.9rem/1.1 var(--font-display); margin: 0 0 8px; }
h3 { font: 600 1.3rem/1.2 var(--font-display); margin: 0 0 8px; letter-spacing: .02em; }
p { margin: 0 0 10px; }
.lede { font-size: 1.08rem; max-width: 78ch; }
.muted { color: var(--muted); } .small { font-size: .85rem; }
nav.toc { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 14px 0 6px; font-size: .9rem; }
nav.toc a { color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--line); }
nav.toc a:hover { color: var(--fg); }
section { margin-top: 42px; }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 18px 20px; }
.panel + .panel, .panel + .scroll, .scroll + .panel, .scroll + p, .panel + p, p + .panel, p + .scroll, .grid2 + .panel, .panel + .grid2 { margin-top: 14px; }
.label { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(196px, 1fr)); gap: 12px; margin-top: 18px; }
.tiles > .panel, .dcards > .panel, .grid2 > .panel, .bl > .panel { margin-top: 0; }
.tile .k { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.tile .v { font: 600 1.45rem/1.2 var(--font-body); margin: 6px 0 4px; letter-spacing: -.01em; text-wrap: balance; }
.tile .d { font-size: .86rem; color: var(--muted); line-height: 1.4; }
.bl { display: grid; gap: 10px; margin-top: 14px; counter-reset: bl; }
.bl .panel { display: grid; grid-template-columns: 34px 1fr; gap: 4px 12px; }
.bl .panel::before { counter-increment: bl; content: counter(bl); font: 700 1.5rem/1 var(--font-display); color: var(--muted); }
.bl b { display: block; font: 600 1.15rem/1.25 var(--font-display); letter-spacing: .02em; margin-bottom: 2px; }
.bl ul { margin: 4px 0 0; padding-left: 18px; } .bl li { margin-bottom: 3px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.cw { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.chart { width: 100%; height: auto; display: block; overflow: visible; }
.grid2 > * { min-width: 0; }
.chart .grid { stroke: var(--grid); } .chart .zero { stroke: var(--muted); }
.chart .ref { stroke: var(--muted); stroke-width: 1; }
.chart .reflab { fill: var(--muted); font: 500 11px var(--font-mono); }
.chart .tick { fill: var(--muted); font: 11px var(--font-mono); }
.chart .tick.strong { fill: var(--fg); font-weight: 600; }
.chart .rowlab { fill: var(--fg); font: 600 14px var(--font-body); }
.chart .rowlab.sm { font: 500 12.5px var(--font-body); }
.chart .rowlab.strong { font-weight: 700; }
.chart .grp { fill: var(--muted); font: 500 10.5px var(--font-mono); letter-spacing: .1em; }
.chart .val { fill: var(--fg); font: 500 12.5px var(--font-mono); paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
.chart .val.muted { fill: var(--muted); }
.chart .val.sm { font-size: 11px; }
.chart .ann { fill: var(--muted); font: 600 11px var(--font-mono); letter-spacing: .04em; }
.chart .zlab { fill: var(--muted); font: 500 10.5px var(--font-mono); }
.chart .zone { fill: var(--sunk); }
.chart .endlab { fill: var(--fg); font: 500 12px var(--font-mono); }
.chart .leader { stroke: var(--faint); stroke-width: 1; }
.chart .b.pos { fill: var(--pos); } .chart .b.neg { fill: var(--neg); } .chart .b.t41 { fill: var(--s1); } .chart .b.t44 { fill: var(--s2); }
.chart .b.hl { stroke: var(--fg); stroke-width: 1.5; }
.chart .eqy { fill: var(--fg); } .chart .eqn { fill: none; stroke: var(--faint); stroke-width: 1.5; }
.chart .ring { stroke: var(--surface); stroke-width: 2; }
.chart .mark { fill: none; stroke: var(--fg); stroke-width: 1.5; }
.chart .hollow { fill: var(--surface); stroke: var(--fg); stroke-width: 2; }
.chart .filled { fill: var(--fg); stroke: var(--surface); stroke-width: 2; }
.chart .conn { stroke: var(--faint); stroke-width: 2; }
.chart .hit, .chart .xhit, .chart .hitc { fill: transparent; }
.chart .hit:hover, .chart .hit:focus { fill: var(--fg); fill-opacity: .05; outline: none; }
.chart .pt:focus { outline: none; } .chart .pt:focus .ring, .chart .pt:hover .ring { stroke: var(--fg); }
.chart .cross { stroke: var(--muted); stroke-width: 1; }
.chart.xh:focus { outline: 2px solid var(--line); outline-offset: 4px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: .85rem; color: var(--muted); margin: 4px 0 6px; }
.legend i { display: inline-block; vertical-align: middle; margin-right: 6px; }
.legend i.ln { width: 16px; height: 2px; border-radius: 1px; }
.legend i.sq { width: 11px; height: 11px; border-radius: 3px; }
.legend i.dot { width: 10px; height: 10px; border-radius: 50%; background: var(--fg); }
.legend i.ring { width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--fg); }
.legend i.bar { width: 14px; height: 10px; border-radius: 2px; }
.tip { position: fixed; z-index: 20; pointer-events: none; display: none; max-width: 300px; background: var(--surface); color: var(--fg);
  border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; font-size: .82rem; box-shadow: 0 6px 18px rgba(0,0,0,.18); }
.tip div { display: flex; align-items: baseline; gap: 6px; line-height: 1.35; }
.tip b { font: 600 .86rem var(--font-mono); white-space: nowrap; }
.tip span.l { color: var(--muted); }
.tip .k { display: inline-block; width: 12px; height: 2px; border-radius: 1px; flex: none; align-self: center; }
.tip .yr { font: 600 .78rem var(--font-mono); color: var(--muted); margin-bottom: 4px; }
details.tv { margin-top: 8px; font-size: .88rem; }
details.tv summary { cursor: pointer; color: var(--muted); }
details.tv table { margin-top: 8px; }
.loop { display: flex; flex-wrap: wrap; gap: 6px; align-items: stretch; margin: 12px 0 6px; padding: 0; list-style: none; counter-reset: lp; }
.loop li { flex: 1 1 150px; border: 1px solid var(--line); border-radius: 6px; padding: 9px 11px; background: var(--sunk); font-size: .9rem; position: relative; }
.loop li::before { counter-increment: lp; content: counter(lp); font: 600 .78rem var(--font-mono); color: var(--muted); display: block; }
.loop li.back { background: var(--surface); border-style: dashed; color: var(--muted); }
.dcards { display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap: 12px; }
.dcard h3 { margin-bottom: 10px; }
.dcard p { font-size: .9rem; }
ul.probs { list-style: none; margin: 0 0 12px; padding: 0; display: grid; gap: 5px; }
ul.probs li { display: grid; grid-template-columns: minmax(0, 1fr) 90px 38px; gap: 8px; align-items: center; font-size: .88rem; }
ul.probs li.top .ol { font-weight: 600; }
.pb { height: 8px; background: var(--sunk); border-radius: 2px; overflow: hidden; }
.pf { display: block; height: 100%; background: var(--pos); border-radius: 0 2px 2px 0; }
.pv { font: 500 .82rem var(--font-mono); text-align: right; }
.scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { border-collapse: separate; border-spacing: 0; width: 100%; background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; font-size: .92rem; }
thead th { font: 500 .72rem/1.25 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); background: var(--sunk); vertical-align: bottom; }
thead th:first-child { border-top-left-radius: var(--r); } thead th:last-child { border-top-right-radius: var(--r); }
tbody th { font-weight: 500; }
td.n, th.n { text-align: right; font-family: var(--font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
tbody tr:last-child > * { border-bottom: 0; }
tr.em > * { font-weight: 700; }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 3px; background: var(--pc); margin-right: 6px; }
.callout { border-left: 4px solid var(--fg); }
ul.cav { margin: 0; padding-left: 18px; } ul.cav li { margin-bottom: 6px; }
.facts { margin: 0; padding-left: 18px; } .facts li { margin-bottom: 4px; }
.lede, .bl .panel, .dcard p, .facts li, ul.cav li { text-wrap: pretty; }
footer { margin-top: 40px; font-size: .82rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 12px; }
@media (max-width: 760px) {
  .wrap { padding: 0 16px 48px; }
  .chart { min-width: 620px; }
  .grid2 { grid-template-columns: 1fr; }
  .dcards { grid-template-columns: 1fr; }
  .panel { padding: 14px 14px; }
  ul.probs li { grid-template-columns: minmax(0, 1fr) 60px 36px; }
  .chart .tick, .chart .reflab, .chart .zlab, .chart .ann { font-size: 13px; }
  .chart .val, .chart .endlab, .chart .rowlab.sm { font-size: 14px; }
}
@media (prefers-reduced-motion: no-preference) { a { transition: color .15s; } }
"""

JS = r"""
(() => {
  const tip = document.createElement('div'); tip.className = 'tip'; tip.setAttribute('role', 'status'); document.body.appendChild(tip);
  const place = (x, y) => {
    const r = tip.getBoundingClientRect(), pad = 12;
    let left = x + 14, top = y + 14;
    if (left + r.width > innerWidth - pad) left = x - r.width - 14;
    if (top + r.height > innerHeight - pad) top = y - r.height - 14;
    tip.style.left = Math.max(pad, left) + 'px'; tip.style.top = Math.max(pad, top) + 'px';
  };
  const show = (rows, x, y, head) => {
    tip.replaceChildren();
    if (head) { const h = document.createElement('div'); h.className = 'yr'; h.textContent = head; tip.appendChild(h); }
    for (const r of rows) {
      const d = document.createElement('div');
      if (r.k) { const k = document.createElement('span'); k.className = 'k'; k.style.background = r.k; d.appendChild(k); }
      const v = document.createElement('b'); v.textContent = r.v; d.appendChild(v);
      if (r.l) { const l = document.createElement('span'); l.className = 'l'; l.textContent = r.l; d.appendChild(l); }
      tip.appendChild(d);
    }
    tip.style.display = 'block'; place(x, y);
  };
  const hide = () => { tip.style.display = 'none'; };
  document.querySelectorAll('[data-tip]').forEach(el => {
    const rows = JSON.parse(el.dataset.tip);
    el.addEventListener('pointermove', e => show(rows, e.clientX, e.clientY));
    el.addEventListener('pointerleave', hide);
    el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); show(rows, r.left + r.width / 2, r.top + r.height / 2); });
    el.addEventListener('blur', hide);
  });
  document.querySelectorAll('rect[data-cross]').forEach(hit => {
    const P = JSON.parse(hit.dataset.cross), svg = hit.ownerSVGElement, line = svg.querySelector('.cross');
    const fmt = v => P.fmt === 'pct' ? Math.round(v * 100) + '%' : Math.round(v).toLocaleString('en-US');
    const xOf = yr => P.x0 + (yr - P.xlo) / (P.xhi - P.xlo) * (P.x1 - P.x0);
    let idx = P.years.length - 1;
    const render = (cx, cy) => {
      const yr = P.years[idx], x = xOf(yr);
      line.setAttribute('x1', x); line.setAttribute('x2', x); line.setAttribute('visibility', 'visible');
      const rows = P.series.filter(s => s.vals[yr] !== undefined).map(s => ({ v: fmt(s.vals[yr]), l: s.name, k: s.k }));
      show(rows, cx, cy, String(yr));
    };
    const fromEvent = e => {
      const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      const p = pt.matrixTransform(svg.getScreenCTM().inverse());
      const yr = P.xlo + (p.x - P.x0) / (P.x1 - P.x0) * (P.xhi - P.xlo);
      let best = 0; P.years.forEach((y, i) => { if (Math.abs(y - yr) < Math.abs(P.years[best] - yr)) best = i; });
      idx = best; render(e.clientX, e.clientY);
    };
    hit.addEventListener('pointermove', fromEvent);
    hit.addEventListener('pointerdown', fromEvent);
    hit.addEventListener('pointerleave', () => { line.setAttribute('visibility', 'hidden'); hide(); });
    svg.addEventListener('keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault(); idx = Math.max(0, Math.min(P.years.length - 1, idx + (e.key === 'ArrowRight' ? 1 : -1)));
      const r = svg.getBoundingClientRect(); render(r.left + r.width / 2, r.top + 20);
    });
    svg.addEventListener('focus', () => { const r = svg.getBoundingClientRect(); render(r.left + r.width / 2, r.top + 20); });
    svg.addEventListener('blur', () => { line.setAttribute('visibility', 'hidden'); hide(); });
  });
})();
"""


def build():
    s41, s44 = DELAY["snapshot_2041"], DELAY["delay3_2044"]
    c41, c44 = s41["boeing_by_airbus_ctx"], s44["boeing_by_airbus_ctx"]
    eis_svg, eis_tbl = chart_eis()
    share_svg, share_tbl = chart_share()
    lead_svg, lead_tbl = chart_lead()
    units_svg, units_tbl = chart_airbus_units()
    eng_svg, eng_leg = chart_engines()
    thr = A2["thresholds_2044"]
    lev = ROB["pure_equilibrium_levers_2044"]
    bt = ROB["bill_timing"]
    sp = A2["nb_split"]
    proj = A2["project_split"]
    w787 = ROB["with_787_reengine"]
    vac = VAC["cases"]
    ent = {(e["case"], e["eis"], e["capex_b"]): e["npv"] for e in VAC["entrant_unserved_only"]}
    p44 = s44["pure"]
    steps = bridge_steps()
    d41 = s41["decomp_fps10_vs_dn"][MOD]; d44 = s44["decomp_fps10_vs_dn"][MOD]

    numbers = table(["Boeing: fps 10-year Solo minus Do Nothing ($B)", "fps 2041 (snapshot)", "fps 2044 (delay)"], [
        ["Airbus NGSA + Re-engine A350, Boeing Do Nothing 787", f"<b>{num(c41[MOD]['Milk_787']['fps10_vs_dn'])}</b>", f"<b>{num(c44[MOD]['Milk_787']['fps10_vs_dn'])}</b>"],
        ["…with Airbus Delay Tactics (the slip test)", num(c41[DT]['Milk_787']['fps10_vs_dn']), num(c44[DT]['Milk_787']['fps10_vs_dn'])],
        ["Boeing also re-engines the 787", num(w787["2041"]["vs_A350_reengine"]), num(w787["2044"]["vs_A350_reengine"])],
        ["fps 7-year Solo instead", num(c41[MOD]['Milk_787']['fps7_vs_dn']), num(c44[MOD]['Milk_787']['fps7_vs_dn'])],
        ["fps via Embraer ($100B, paid by Boeing) instead", num(c41[MOD]['Milk_787']['via_embraer_vs_dn']), num(c44[MOD]['Milk_787']['via_embraer_vs_dn'])]],
        num_cols=(1, 2))

    def lv(name, val, fmt):
        return fmt(val)
    levers = table(["Lever (snapshot value)", "Beats Do Nothing", "Beats Do Nothing by $1B", "Back in a pure equilibrium"], [
        ["fps margin (25.64%)", f"{thr['fps margin (%) | modal']['breakeven']:.1f}%", f"{thr['fps margin (%) | modal']['value_at_hurdle']:.1f}%", "<b>34.1%</b>"],
        ["fps 10-year bill ($55.25B)", "$45.0B", "$40.7B", "<b>$40.8B</b>"],
        ["fps price ($55M)", f"${thr['fps price ($M) | modal']['breakeven']:.1f}M", f"${thr['fps price ($M) | modal']['value_at_hurdle']:.1f}M", f"<b>${thr['fps price ($M) | delay_tactics']['breakeven']:.1f}M</b>"],
        ["Boeing’s share recovery after entry (1 point/yr)", f"{REC['breakeven_modal']:.2f}", f"{REC['hurdle_1B_modal']:.2f}", f"<b>{REC['breakeven_delay_tactics']:.2f}</b>"],
        ["“fps via Embraer” bill paid by Boeing ($100B)", "$45.0B", "—", "—"]], num_cols=(1, 2, 3))

    eqtab = table(["2044 equilibrium", "Airbus", "Boeing", "Airbus $B", "Boeing $B"], [
        ["A", "NGSA + Re-engine A350", "Do Nothing 737 + Do Nothing 787", num(p44[0]["da"]), num(p44[0]["db"])],
        ["B", "NGSA + Do Nothing A350", "Do Nothing 737 + Re-engine 787", num(p44[1]["da"]), num(p44[1]["db"])],
        ["<i>Snapshot, typical cell</i>", "<i>NGSA + Delay Tactics + Re-engine A350</i>", "<i>fps 10-year + Do Nothing 787</i>",
         f"<i>{num(DELAY['snapshot_2041']['airbus_best_response']['fps10 + Do Nothing 787']['da'])}</i>", f"<i>{num(c41[DT]['Milk_787']['fps10'])}</i>"]],
        num_cols=(3, 4))

    gap = table(["Unserved demand 2037–2056 (aircraft)", "fps 2041", "fps 2044, launched", "Boeing Do Nothing (the 2044 equilibrium)"], [
        [lab, *[f"{vac[c][f'unserved_cap{cap}']['cum_2037_2056']:,}" for c in ("fps 2041", "fps 2044", "Boeing Do Nothing")]]
        for lab, cap in (("Airbus at rate 75 (900/yr)", 900), ("Airbus at ~100/month (1,200/yr)", 1200), ("Airbus at ~110/month (1,320/yr)", 1320))],
        num_cols=(1, 2, 3))

    entrant = table(["Entrant NPV, $B (board conventions)", "fps 2041", "fps 2044", "Boeing Do Nothing"], [
        ["Bill paid at entry in 2038, Airbus capped at 1,200 a year", num(ent[("fps 2041", 2038, 15.0)]), num(ent[("fps 2044", 2038, 15.0)]), num(ent[("Boeing Do Nothing", 2038, 15.0)])],
        ["Embraer-realistic timing (entry 2042), bill paid at entry", num(-2.44), num(-0.49), "—"],
        ["Same, but bill spread over 2034–41", num(-4.31), num(-2.36), num(-1.44)],
        ["The 737 at rate 47 absorbs part of the overflow", "—", num(-1.45), num(-1.35)],
        ["Airbus capped at rate 75 (900 a year)", num(1.68), num(4.03), num(4.95)]], num_cols=(1, 2, 3))

    embraer_paths = table(["Embraer path", "fps 2041", "fps 2044"], [
        ["Independent 180–210 seat clean sheet with sovereign or industrial partners, launched by 2035 (<b>third player</b>)", "~5%", "~8%"],
        ["Smaller 150–170 seat step above the E195-E2 (counts only above 150 seats)", "~1–2%", "~2–3%"],
        ["<b>Embraer becomes a third player</b>", "<b>~6%</b>", "<b>~10%</b>"],
        ["Boeing’s partner: Joint Venture or buy-back (not a third player)", "~10%", "~12%"]], num_cols=(1, 2))
    comac_paths = table(["COMAC path", "fps 2041", "fps 2044"], [
        ["EASA-validated C919 exported at 100+ a year outside China by 2045 (<b>third player</b>)", "~7–11%", "~9–15%"],
        ["Funded, export-oriented new single-aisle by 2035 (<b>third player</b>; no study is cited, and the C929 widebody competes for engineers)", "~5%", "~7%"],
        ["<b>COMAC becomes a third player</b> (either path; they overlap)", "<b>~11%</b>", "<b>~15%</b>"],
        ["COMAC supplies 40% or more of China’s single-aisle deliveries by 2045 (<b>not</b> a third player, but the bigger effect)", "~45%", "~50%"]], num_cols=(1, 2))

    eng_tbl = table(["Engine board, pure equilibrium ($B)", "CFM/GE", "Pratt & Whitney", "Rolls-Royce"], [
        [lab, num(v["pure"][0]["cfm_b"]), num(v["pure"][0]["pw_b"]), num(v["pure"][0]["rr_b"]) if abs(v["pure"][0]["rr_b"]) > 0.005 else "0 (Do Nothing on narrowbody)"]
        for lab, v in zip(["Snapshot (fps 2041, fps engines from all three, Boeing 50%)", "fps launched late, Boeing at ~30% of the new-generation market",
                           "Boeing Do Nothing: 737 stays on LEAP at 20%"], ENG.values())], num_cols=(1, 2, 3))

    readings_tbl = table(["fps 10-year minus Do Nothing, by reading of the delay", "fps 2041", "fps 2044"], [
        ["Board: bill paid at entry into service (a planned later programme)", num(bt["board_lump"]["2041"]), num(bt["board_lump"]["2044"])],
        ["Slip found after the bill is committed on the 2041 schedule", "—", num(bt["lump_at_2041"]["2044"])],
        ["…plus a 30% overrun paid at the new date (war-game rule: +10% per year of slip)", "—", num(bt["lump_at_2041_plus_30pct_at_2044"]["2044"])],
        ["Bill spread over the 6 years before entry into service", num(bt["spread6"]["2041"]), num(bt["spread6"]["2044"])],
        ["Bill spread over the 9 years before entry into service", num(bt["spread9"]["2041"]), num(bt["spread9"]["2044"])],
        ["Spent over 9 years on the 2041 schedule, then a 3-year slip", "—", num(bt["slip_spread9"]["2044"])]], num_cols=(1, 2))

    bridge_tbl = table(["Driver (2041 → 2044)", "$B"], [
        [f"Narrowbody profit, fps minus Do Nothing: {num(sp['nb_2041'])} → {num(sp['nb_2044'])}", num(sp["nb_2044"] - sp["nb_2041"])],
        ["   …the same cash, 3 years later", num(sp["timing_only"])],
        ["   …Boeing re-enters from a deeper hole", f"<b>{num(sp['share_effect'])}</b>"],
        [f"The fps bill in present value: {d41['fps_pv_capex']:.2f} → {d44['fps_pv_capex']:.2f}", num(d41["fps_pv_capex"] - d44["fps_pv_capex"])],
        [f"Debt penalty: {d41['fps_alpha_pen']:.2f} → {d44['fps_alpha_pen']:.2f}", num(d41["fps_alpha_pen"] - d44["fps_alpha_pen"])],
        ["<b>Net</b>", f"<b>{num(d44['b_total_delta'] - d41['b_total_delta'])}</b>"]], num_cols=(1,))

    v41 = c41[MOD]["Milk_787"]["fps10_vs_dn"]; v44 = c44[MOD]["Milk_787"]["fps10_vs_dn"]
    tiles = [("fps vs Do Nothing", f"{num(v41, '+.1f')} → {num(v44, '+.1f')}", f"$B PV. Against Airbus Delay Tactics: {num(c41[DT]['Milk_787']['fps10_vs_dn'], '+.1f')} → {num(c44[DT]['Milk_787']['fps10_vs_dn'], '+.1f')}"),
             ("fps in equilibrium", "None at 2044", "In 14 of the snapshot’s 17 near-Nash cells; in none of the 2 pure and 2 near-Nash equilibria at 2044"),
             ("Airbus gain", "+$8–11B", "Almost all of it is volume beyond what Airbus can build today"),
             ("Third player", "~15% → ~22%", "Embraer or COMAC (judgement)"),
             ("CFM if Boeing keeps the 737", f"+${ENG[list(ENG)[2]]['pure'][0]['cfm_b'] - ENG[list(ENG)[0]]['pure'][0]['cfm_b']:.0f}B", "LEAP keeps Boeing’s slot; Rolls-Royce loses its narrowbody entry")]
    tiles_html = "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles)

    eis_head = "<thead><tr><th>fps entry</th><th class='n'>fps minus Do Nothing ($B)</th><th>fps in any equilibrium</th></tr></thead>"
    share_head = "<thead><tr><th>Year</th>" + "".join(f"<th class='n'>{esc(n)}</th>" for n, _ in SCEN) + "</tr></thead>"
    lead_head = "<thead><tr><th>NGSA lead</th><th class='n'>fps 2041 ($B)</th><th>fps 2041 status</th><th class='n'>fps 2044 ($B)</th><th>fps 2044 status</th></tr></thead>"
    scen_leg = "".join(f'<span><i class="ln" style="background:var(--{c})"></i>{esc(n)}</span>' for n, c in SCEN)

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>fps Three Years Late</title>
<meta name="description" content="What a 3-year fps delay (entry into service 2041 to 2044) does to Boeing's business case on the dashboard, how Airbus would respond, and the odds of Embraer or COMAC entering.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><span class="eyebrow">Game-theory dashboard snapshot · fps entry into service 2041 → 2044</span>
<h1>fps Three Years Late</h1>
<p class="lede">What a 3-year fps delay does to Boeing’s business case on your dashboard, how Airbus would respond, and the odds that it brings Embraer or COMAC in as a third player. Everything else stays as in the snapshot: NGSA in service 2037, both Re-engines 2035, and the snapshot’s costs, margins, prices and capture speeds.</p>
<nav class="toc" aria-label="Contents"><a href="#bottom-line">Bottom line</a><a href="#board">Board vs snapshot</a><a href="#business-case">Business case</a><a href="#airbus">Airbus’s response</a><a href="#third-player">Third player</a><a href="#engines">Engine makers</a><a href="#limits">Limits</a></nav>
</header>
<main>
<section id="bottom-line"><h2>The fps case flips from indifferent to no, and Airbus wins by doing little</h2>
<div class="tiles">{tiles_html}</div>
<div class="bl">
<div class="panel"><div><b>The fps business case flips from “indifferent” to “no”.</b>fps (10-year ramp) against Do Nothing goes from {num(v41)} to {num(v44)} $B, and from {num(c41[DT]['Milk_787']['fps10_vs_dn'])} to {num(c44[DT]['Milk_787']['fps10_vs_dn'])} against Airbus Delay Tactics. fps leaves every equilibrium: the game goes from 0 pure and 17 near-Nash equilibria to 2 pure ones, and in both Boeing does nothing on the narrowbody. These are the board’s mildest numbers: if the slip is found after the bill is committed, fps is {num(bt['lump_at_2041']['2044'], '+.1f')}, or {num(bt['lump_at_2041_plus_30pct_at_2044']['2044'], '+.1f')} with a 30% overrun.</div></div>
<div class="panel"><div><b>The cause is share, not discounting.</b>NGSA gets 7 years alone instead of 4, so Boeing re-enters at 20% share instead of 28% and, at 1 point a year, never gets back to parity inside the window. Share costs {num(-proj['share_effect'], '.1f')} $B; timing only {num(-proj['pure_timing'], '.1f')}. NGSA’s lead decides it: fps is a pure equilibrium only when NGSA leads by 3 years or less. The snapshot’s 4-year lead is the knife edge; the delay makes it 7.</div></div>
<div class="panel"><div><b>Airbus’s best response is to do very little.</b>Keep NGSA on its 2030-launch plan, drop Delay Tactics (the delay does their job, and against a Boeing that doesn’t launch they risk a fine worth about $12B today), and let the contest move to widebody Chicken. Airbus gains $8–11B on the board, but almost all of it is narrowbody volume beyond what it can build today. Whether Airbus adds that capacity also sets the odds of a third player.</div></div>
<div class="panel"><div><b>A third player becomes more likely, but stays the less likely outcome.</b>Judgement: Embraer or COMAC enters ~15% → ~22%; Embraer independently ~6% → ~10%; COMAC as a real exporter ~11% → ~15%. More likely: Airbus builds more and prices the scarcity, 737 MAX volumes stay higher than the board assumes, and COMAC takes much of Boeing’s China share (~45% → ~50%), which hurts Boeing more than any exporting entrant.</div></div>
<div class="panel"><div><b>A Boeing that doesn’t launch fps is a large gain for CFM.</b>About +$38B against the snapshot, because the LEAP-powered 737 keeps Boeing’s slot. Rolls-Royce loses its narrowbody entry (+$17B in the snapshot) and Pratt &amp; Whitney about $4B. Your engine board has a CFM “Partner Embraer” move it never evaluates; included, it is in every engine equilibrium.</div></div>
</div></section>

<section id="board"><h2>Your snapshot came from a later build than the file you attached</h2>
<div class="panel"><ul class="facts">
<li><b>Attached file:</b> charges the full $3B Boeing two-front strain whenever fps and a 787 Re-engine overlap. Solved as uploaded it gives 1 pure and 13 near-Nash equilibria and misses 4 of your 17 cells.</li>
<li><b>Overlap-aware strain</b> (strain scaled by how far the development windows overlap) reproduces the snapshot exactly: 0 pure and 17 near-Nash, the same cells and every rounded yield. Boeing’s windows overlap one year in five, so its strain is $0.6B. A flat strain of $1.55B or less would also fit, but the snapshot prints $3.00B.</li>
<li><b>What it changes:</b> only cells where Boeing also re-engines the 787. Both rules give the same equilibria at 2044.</li>
<li><b>The engine board can’t see the delay.</b> It takes the earlier of fps and NGSA (2037) as the narrowbody entry year. That is a decoupling in the board, not evidence that engine makers are unaffected (see <a href="#engines">engine makers</a>).</li>
</ul>
<p class="muted small" style="margin:10px 0 0">How it was done: your board was solved headlessly (Streamlit never runs; a mock harness executes its code). Five AI analysts covered Airbus’s response, Embraer, COMAC, an independent re-derivation of every board number and a completeness review, each with an adversarial checker; their corrections are applied. $ figures are the board’s measure: present value at 2026, $B, against the status quo (Boeing WACC 10.5%, Airbus 8%, debt penalty α = 0.30).</p></div></section>

<section id="business-case"><h2>Business case: fps goes from indifferent to clearly negative</h2>
<div class="panel"><p class="label">fps 10-year minus Do Nothing by fps entry year ($B)</p>
<div class="legend"><span><i class="bar" style="background:var(--pos)"></i>fps beats Do Nothing</span><span><i class="bar" style="background:var(--neg)"></i>fps loses</span><span><i class="dot"></i>fps in an equilibrium</span><span><i class="ring" style="border-color:var(--faint)"></i>not in any</span></div>
{eis_svg}
{details("Table view", f"<div class='scroll'><table>{eis_head}<tbody>{eis_tbl}</tbody></table></div>")}
<p class="muted small" style="margin-top:8px">After 2044 the value rises slightly. That is a quirk of the board: its evaluation window runs to entry into service + 19, so a later fps is the same losing project, discounted further.</p></div>
{numbers}
<div class="panel callout"><h3>At 2041 Boeing is indifferent, not committed</h3>
<p>+$1.06B is inside Boeing’s tolerance band of one yield point ($1.3B). The snapshot has no pure equilibrium because the best responses chase each other in a loop. Delay Tactics keep Boeing out at 2041; at 2044 the delay does that job by itself. fps 10-year appears in 13 of the 17 near-Nash cells (fps 7-year in one more).</p>
<ol class="loop" aria-label="Best-response loop at 2041"><li>Boeing launches fps</li><li>Airbus answers with Delay Tactics</li><li>Boeing switches to Do Nothing</li><li>Airbus drops Delay Tactics, which would now be naked</li><li class="back">Boeing launches fps again, and the loop restarts</li></ol></div>

<h3 style="margin-top:28px">Why it flips: share, not discounting</h3>
<div class="panel"><p class="label">Bridge, fps minus Do Nothing, 2041 → 2044 ($B)</p>
<div class="legend"><span><i class="bar" style="background:var(--s1)"></i>fps 2041 total</span><span><i class="bar" style="background:var(--s2)"></i>fps 2044 total</span><span><i class="bar" style="background:var(--pos)"></i>Raises the case</span><span><i class="bar" style="background:var(--neg)"></i>Lowers it</span></div>
{chart_bridge()}{details("Table view", bridge_tbl)}</div>
<div class="panel"><p class="label">Boeing narrowbody share by year (board rule)</p>
<div class="legend">{scen_leg}</div>
{share_svg}{details("Table view", f"<div class='scroll'><table>{share_head}<tbody>{share_tbl}</tbody></table></div>")}</div>
<p style="margin-top:12px">NGSA takes 3 points of share a year from 2037 until fps arrives, up to an 80% cap; fps then wins back 1 point a year. With fps in 2041 Boeing re-enters at 28% and reaches 48% by 2060. With fps in 2044 it re-enters at 20% and reaches only 40% by 2063. Netting the cheaper bill against discounting, pure timing costs only {num(proj['pure_timing'])} $B; the deeper share hole costs <b>{num(proj['share_effect'])} $B</b>.</p>

<div class="panel"><p class="label">NGSA’s head start decides it: fps minus Do Nothing by NGSA lead ($B)</p>
<div class="legend"><span><i class="ln" style="background:var(--s1)"></i>fps 2041</span><span><i class="ln" style="background:var(--s2)"></i>fps 2044</span></div>
{lead_svg}
{details("Table view", f"<div class='scroll'><table>{lead_head}<tbody>{lead_tbl}</tbody></table></div>")}
<p class="muted small" style="margin-top:8px">The rule is the same for both fps dates: in every pure equilibrium at a lead of 3 years or less; at 4 years fps beats Do Nothing pairwise but there is no pure equilibrium (the snapshot sits here); at 5 years it survives only in a few near-Nash cells; at 6 or more it is in none. The delay moves the lead from 4 years to 7.</p></div>

<h3 style="margin-top:28px">It depends on what kind of delay this is</h3>
<div class="panel"><p>Your board books the entire fps bill as one payment in the entry-into-service year, so a later fps looks cheaper (+$4.1B). That only holds if the delay is planned and the spending moves with it. The direction holds under every reading; only the size changes. The positive 2041 case exists only under the board’s pay-at-entry rule; a stale caption in the board says the bill is spread over 9 years, and if it were, fps would already be a no-go on time.</p>
<div class="legend"><span><i class="bar" style="background:var(--neg)"></i>fps 2044</span><span><i class="ring"></i>fps 2041</span></div>
{chart_readings()}{details("Table view", readings_tbl)}</div>

<h3 style="margin-top:28px">What would bring fps back at 2044</h3>
<p class="muted">Each lever moves on its own; every level is solved on the board.</p>
{levers}
<p style="margin-top:10px"><b>Breaking even is not enough.</b> Between “beats Do Nothing” and the pure-equilibrium level the board cycles with no pure equilibrium; fps settles only once it beats Do Nothing even against Delay Tactics. “fps via Embraer” differs from the 10-year Solo only in its bill, so its break-even is the same $45B, less than half the $100B the slider is set to.</p>

<h3 style="margin-top:28px">What the game becomes</h3>
{eqtab}
<div class="grid2" style="margin-top:14px">
<div class="panel"><b>Boeing’s own payoff hardly moves</b> ({num(c41[DT]['Milk_787']['fps10'])} → {num(p44[0]['db'])}). Do Nothing was already almost as good as fps. The delay destroys the option, the fps path back into the narrowbody market, and leaves Boeing at 20% narrowbody share from 2043. Its best remaining move is to re-engine the 787 first (equilibrium B): winning the widebody Chicken is worth +$5.6B to Boeing and only +$2.4B to Airbus.</div>
<div class="panel"><b>Our late-fps war game reached the same end state.</b> In wg5-2045d Boeing failed its own go/no-go test (−0.73 against a +$1B hurdle; −4.71 in the slip test), re-engined the 787 instead, and Airbus shelved the A350 Re-engine: equilibrium B. Its calibration differs (NGSA 2035, a $30B fps bill), but measured as NGSA lead it also crosses the knife edge, from 3 years to 6.</div>
</div></section>

<section id="airbus"><h2>Airbus’s response: hold, drop Delay Tactics, and decide on capacity</h2>
<p class="muted">The board solves for what pays; Airbus’s behavioural profile and both war games show what Airbus tends to do. Probabilities are judgement; board values are solved. They depend on each other: if NGSA slips to 2039–2041, fps comes back and Delay Tactics come back with it, so the 95% “drop” assumes NGSA holds.</p>
<div class="dcards">{airbus_cards()}</div>
<div class="panel" style="margin-top:14px"><p class="label">The capacity decision links Airbus’s response to the third-player question</p>
<div class="legend">{scen_leg}</div>
{units_svg}
{details("Table view", f"<div class='scroll'><table>{share_head}<tbody>{units_tbl}</tbody></table></div>")}
<p style="margin-top:10px">The board gives Airbus 80% of a 2,000-a-year market from 2043 if Boeing does nothing: about 1,600 aircraft a year, against 900 at rate 75 or 1,200 at about 100 a month (the shaded gap). On the board the delay is worth +$8.4B to Airbus against a launched fps (39.21 → 47.60), and NGSA margin on volume above 1,200 a year rises by the same +$8.4B. <b>Every dollar of Airbus’s delay gain is volume it cannot build today.</b></p>
{table(["If Airbus…", "Airbus captures the delay gain?", "The gap left for others"], [
        ["Holds rate 75 and prices the scarcity", "No: it earns price, not volume", "Large: queues lengthen, the 737 sells more, an entrant has a case"],
        ["Builds NGSA for ~100 a month, as the 2026 reports suggest", "Yes, largely", "Small: little demand is left unserved after about 2040"]])}</div>
</section>

<section id="third-player"><h2>Third player: more likely, still the less likely outcome</h2>
<div class="panel"><p class="label">Probabilities, fps 2041 → fps 2044 (judgement)</p>
<div class="legend"><span><i class="ring"></i>fps 2041</span><span><i class="dot"></i>fps 2044</span></div>
{chart_odds()}
<p class="muted small" style="margin-top:8px"><b>Definition.</b> A third player is a company other than Boeing or Airbus that, by 2045, delivers a 150–210 seat single-aisle at 100 or more a year (5% of the board’s market) to customers outside its home country, or that has committed funding to such a programme by 2035. Entering as Boeing’s partner (the board’s “fps via Embraer” Joint Venture) does not count.</p></div>

<h3 style="margin-top:28px">How big is the gap, and can an entrant make money in it?</h3>
<p>The size of the gap depends on Airbus’s capacity. Board aircraft are treated as real aircraft a year; 2,000 a year is close to the OEMs’ 2040s forecasts.</p>
{gap}
<ul class="facts" style="margin-top:10px"><li><b>The board overstates the gap.</b> In the late-fps war game Boeing still holds 32% in 2045, so the 2045 gap above 1,200 a year is about 150 aircraft, not 400.</li>
<li><b>The 737 already exceeds the board’s Boeing slot.</b> Boeing built 447 737s in 2025 and is cleared to 47 a month, above the 400 a year the board allows. Part of the overflow becomes queues.</li></ul>
<p style="margin-top:12px" class="muted">Entrant economics on the board’s conventions ($48M price, 12% margin, 10% WACC, a $15B programme):</p>
{entrant}
<p style="margin-top:10px"><b>The delay improves an entrant’s case by about $2B, but Airbus’s capacity moves it more than the delay does.</b> With realistic spending an entrant needs Airbus to stay at rate 75 or a protected home market. COMAC’s case doesn’t hinge on this: its development spending is sunk and its capital comes from the state.</p>

<div class="grid2" style="margin-top:18px">
<div class="panel"><h3>Embraer</h3>
<p class="label">Capability</p><ul class="facts">
<li>Market value about $13B (August 2026); FY2025 revenue $7.6B, adjusted operating profit $0.66B; investing about $0.4B a year.</li>
<li>The E2 cost $1.7B and came in under budget. A 150–210 seat clean sheet costs $10–25B, so partners would fund roughly two-thirds to four-fifths. Fitch upgraded Embraer to BBB in September 2026.</li></ul>
<p class="label" style="margin-top:10px">What it says and does</p><ul class="facts">
<li>“Studies for a new cycle of products… commercial jet or business jet” (May 2026). Leeham (January 2026) reports a 180–240 seat design being explored; its research and technology director calls a single-aisle “one of our potential products” (June 2026). The CEO said the market has room for “three or four” manufacturers (FT, October 2025, via secondary sources).</li>
<li>Partner talks with PIF, Korea, Japan, Turkey and India are early; nothing is funded. In 2011 Embraer waited for Boeing’s choice, then built the E2; Boeing walked away from their Joint Venture in 2020. Faury told Embraer in June 2026 to “think twice”.</li>
<li>Embraer’s 2016 entry rule (incumbents leaving the 104–150 seat segment) is not triggered: a Boeing that does nothing keeps the 737 there.</li></ul>
<div style="margin-top:12px">{embraer_paths}</div>
<p class="small" style="margin-top:10px"><b>Money is the binding constraint, not demand.</b> The delay roughly doubles the opportunity but not the ability to fund it.</p></div>
<div class="panel"><h3>COMAC</h3>
<p class="label">Where it stands</p><ul class="facts">
<li>The C919 (158–192 seats) has been in service since 2023 on Chinese certification only. Deliveries were 10–13 in 2024 and 15 in 2025, against a 2025 target cut to 25; 2026 is tracking at about 25–28. COMAC targets 150 a year by 2027–28 and 200 by 2029, with about $6B of new state capital.</li>
<li>Over 1,000 orders, almost all Chinese. AirAsia confirmed purchase talks (September 2025); Malaysia Airlines is evaluating.</li>
<li>EASA validation expected 2028–31; test flying reportedly found no major hardware issues (July 2026).</li>
<li>US parts: LEAP-1C licences were suspended May–July 2025; in October 2026 Reuters reported, citing unnamed sources, a cap on parts licences to COMAC. China’s CJ-1000A engine is expected around 2027–28.</li></ul>
<div style="margin-top:12px">{comac_paths}</div>
<p class="small" style="margin-top:10px"><b>What binds COMAC is production, US parts and certification, not demand.</b> The delay mostly gives Beijing more reason to steer Chinese orders to COMAC and Airbus Tianjin.</p></div>
</div>
<div class="grid2" style="margin-top:14px">
<div class="panel"><h3>Who bears the risk</h3><p><b>An exporting entrant mostly fills demand Airbus cannot build</b>: chiefly an Airbus risk, and a check on Airbus’s delay gain.</p><p><b>COMAC taking China hits Boeing.</b> China is about 20% of global single-aisle demand. Losing about 6% of the board’s market (about 30% of China) wipes out the 2041 fps case (+1.06 → 0); at 2044 it deepens the loss from −2.53 to −3.46 at 10%.</p></div>
<div class="panel"><h3>Signals to watch</h3><ul class="facts">
<li><b>Airbus:</b> an NGSA production-rate decision; a line or engine deal above rate 75.</li>
<li><b>Embraer:</b> money signed with PIF, Korea or Japan; an engine selection; investment above ~$0.4B a year rather than buybacks.</li>
<li><b>COMAC:</b> deliveries above 60 in 2028 and 100 in 2030; EASA validation; firm orders outside China; formal US parts caps.</li>
<li><b>Boeing:</b> a narrowbody launch around 2031–34, or silence. Its CEO said in 2026 the next narrowbody is “moving to the right”.</li></ul></div>
</div></section>

<section id="engines"><h2>Engine makers: Boeing staying on the 737 is a large gain for CFM</h2>
<div class="panel"><p class="label">Engine board, pure equilibrium, three narrowbody outcomes ($B)</p>
<div class="legend">{eng_leg}</div>
{eng_svg}{details("Table view", eng_tbl)}
<p style="margin-top:10px">The engine board ignores whether Boeing launches fps, so the delay’s end state is represented by setting Boeing’s slot to the 737 on LEAP at 20% share. <b>CFM gains about $38B</b>; Rolls-Royce loses its narrowbody entry; Pratt &amp; Whitney gives up about $4B. In both war games Pratt &amp; Whitney cancelled its next-generation geared turbofan in 2031, and CFM never used its Embraer lever.</p></div>
<div class="panel"><h3>CFM’s hidden “Partner Embraer” move</h3><p>It exists in your code but is never among the 16 CFM moves the board evaluates, because the board keeps only the first four combinations for each base move. Included, it enters every pure engine equilibrium (as Ducted + Partner Embraer + a GEnx upgrade), worth +$2.5B to CFM in the snapshot and +$0.6B if Boeing does nothing. It is a fixed +5 points of share, so it says nothing about the delay, but it shows your board would favour an engine maker backing Embraer.</p></div>
</section>

<section id="limits"><h2>Limits to keep in mind</h2><div class="panel"><ul class="cav">
<li><b>Bill timing.</b> The board pays the whole programme bill in the entry-into-service year. This drives both the positive 2041 case and the “cheaper delay” (see the readings above).</li>
<li><b>Evaluation window.</b> It runs from 2026 to entry into service + 19, so Boeing’s Do Nothing payoff moves with the fps slider (−$0.13B between 2041 and 2044). On a common calendar horizon the delay costs Boeing $3.9–4.8B, not $3.6B; the verdict holds for any horizon up to 2089.</li>
<li><b>No third player, capacity, price or move order.</b> The board lets Airbus build 1,600 a year and has no Embraer or COMAC. Who moves first in the widebody Chicken comes from the war game.</li>
<li><b>Slider settings.</b> The $48.3B naked fine is discounted to the fps date; “fps via Embraer” is $100B, the slider’s maximum.</li>
<li><b>Board build.</b> The uploaded build is not the one that produced the snapshot. The engine board doesn’t read Boeing’s launch decision, and CFM’s Embraer move is never evaluated.</li>
<li><b>War games.</b> Each is one run, calibrated differently (NGSA 2035, a $30B fps bill), and neither had a third airframer.</li>
<li><b>Web evidence.</b> Some 2026 facts were seen only in search snippets: NGSA at about 100 a month, the October 2026 parts-licence caps, and some Embraer quotes.</li>
</ul></div></section>
</main>
<footer>Source: the attached dashboard (Combined_Game_Board.py) and Game.txt snapshot, solved headlessly with overlap-aware strain; scripts and results in wargame/reports/dashboard-fps-delay/analysis (run_all.sh reproduces every board number). Airbus profile and war games wg5-2045 / wg5-2045d; Embraer files in the repo; 2024–26 news as cited in review/. Probabilities are judgement.</footer>
</div><script>{JS}</script></body></html>"""
    # every chart scrolls inside its panel on narrow screens instead of shrinking its text
    n_svg = page.count("<svg viewBox")
    page = page.replace("<svg viewBox", '<div class="cw"><svg viewBox').replace("</svg>", "</svg></div>")
    assert page.count('<div class="cw">') == n_svg == 8, n_svg
    # pure-equilibrium thresholds stated in the levers table must match the solved grid
    assert lev["fps margin %"]["34.1"]["fps_in_pure"] > 0 and lev["fps margin %"]["34.0"]["fps_in_pure"] == 0
    assert lev["fps 10yr bill $B"]["40.7"]["fps_in_pure"] > 0 and lev["fps 10yr bill $B"]["40.9"]["fps_in_pure"] == 0
    assert lev["fps price $M"]["73.0"]["fps_in_pure"] > 0 and lev["Boeing recovery pp/yr"]["2.3"]["fps_in_pure"] > 0
    assert lev["Boeing recovery pp/yr"]["2.25"]["fps_in_pure"] == 0
    return page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fps_delay_assessment.html")
    page = build()
    with open(out, "w") as f:
        f.write(page)
    print(out, len(page))
