"""Build fps_delay_assessment.html: the 3-year fps delay on the user's dashboard (business case, Airbus's response,
third-player odds, engine makers).

Every board number is read from analysis/results/*.json (reproduce with analysis/run_all.sh). Probabilities are
judgement and web facts come from the analysts' notes in review/; both are written inline and labelled as such.

Usage: python3 make_fps_delay_html.py [out.html]"""
import html
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "analysis", "results")
J = lambda n: json.load(open(os.path.join(RES, n + ".json")))
DELAY, A2, VAC, ENG, ROB, REC, PAGE = (J("delay"), J("analysis2"), J("vacuum"), J("engines"), J("robustness"),
                                       J("recovery_threshold"), J("page_data"))
esc = html.escape
MOD = "NGSA + Re-engine A350"
DT = "NGSA + Bottleneck + Re-engine A350"
SCEN = [("fps 2041", "s1"), ("fps 2044", "s2"), ("Boeing Do Nothing", "s3")]
MINUS = "−"


def rnd(v, dp):
    """Round halves away from zero (results carry 6 dp, so this is a single rounding)."""
    return float(Decimal(str(v)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))


def num(v, f="+.2f"):
    """Format with a true minus sign."""
    if f.endswith("f"):
        v = rnd(v, int(f.split(".")[1][:-1]))
    return format(v, f).replace("-", MINUS)


def usd(v, dp=2, sign=False):
    """$1.06B / −$2.53B, kept on one line."""
    r = rnd(v, dp)
    s = f"${abs(r):.{dp}f}B"
    if r < 0:
        s = MINUS + s
    elif sign:
        s = "+" + s
    return f'<span class="nw">{s}</span>'


def tip(*rows):
    """data-tip payload: rows of (value, label, key colour or None). The JS renders it with textContent."""
    return esc(json.dumps([{"v": v, "l": l, "k": k} for v, l, k in rows]), quote=True)


def mark_attrs(*rows):
    """Attributes for a focusable chart mark: tooltip payload plus an accessible name."""
    name = "; ".join(f"{l}: {v}" if l else v for v, l, k in rows)
    return f'tabindex="0" role="img" aria-label="{esc(name, quote=True)}" data-tip="{tip(*rows)}"'


def bar_path(x, w, y0, y1, r=4):
    """Column from baseline y0 to y1, 4px rounded at the data end, square at the baseline."""
    top, bot = min(y0, y1), max(y0, y1)
    r = min(r, (bot - top) / 2, w / 2)
    if y1 < y0:
        return (f"M{x:.1f},{bot:.1f}V{top + r:.1f}Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f}H{x + w - r:.1f}"
                f"Q{x + w:.1f},{top:.1f} {x + w:.1f},{top + r:.1f}V{bot:.1f}Z")
    return (f"M{x:.1f},{top:.1f}V{bot - r:.1f}Q{x:.1f},{bot:.1f} {x + r:.1f},{bot:.1f}H{x + w - r:.1f}"
            f"Q{x + w:.1f},{bot:.1f} {x + w:.1f},{bot - r:.1f}V{top:.1f}Z")


def hbar_path(x0, x1, y, h, r=4):
    """Horizontal bar from baseline x0 to x1, rounded at the data end."""
    left, right = min(x0, x1), max(x0, x1)
    r = min(r, (right - left) / 2, h / 2)
    if x1 > x0:
        return (f"M{left:.1f},{y:.1f}H{right - r:.1f}Q{right:.1f},{y:.1f} {right:.1f},{y + r:.1f}V{y + h - r:.1f}"
                f"Q{right:.1f},{y + h:.1f} {right - r:.1f},{y + h:.1f}H{left:.1f}Z")
    return (f"M{right:.1f},{y:.1f}H{left + r:.1f}Q{left:.1f},{y:.1f} {left:.1f},{y + r:.1f}V{y + h - r:.1f}"
            f"Q{left:.1f},{y + h:.1f} {left + r:.1f},{y + h:.1f}H{right:.1f}Z")


def svg_open(w, h, label, cls="chart"):
    return f'<svg viewBox="0 0 {w} {h}" class="{cls}" role="group" aria-label="{esc(label, quote=True)}">'


def tview(title, head, rows):
    """Table view inside <details>; each row's first cell is a row header."""
    th = "".join(f'<th scope="col"{" class=n" if i else ""}>{esc(h)}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else f'<td class="n">{c}</td>')
                                    for j, c in enumerate(r)) + "</tr>" for r in rows)
    return (f'<details class="tv"><summary>Table view: {esc(title)}</summary><div class="scroll"><table>'
            f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></details>')


def table(head, rows, num_cols=()):
    th = "".join(f'<th scope="col"{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else f'<td{" class=n" if j in num_cols else ""}>{c}</td>')
                                    for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


# ------------------------------------------------------------------ chart 1: fps value by entry year
def chart_eis():
    rows = DELAY["sweep_fps_eis"]
    key = "NGSA + Re-engine A350 | Milk_787 | fps10-DN"
    w, h, left, right, top, bot = 760, 340, 56, 16, 34, 92
    lo, hi = -4, 10
    band = (w - left - right) / len(rows)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [svg_open(w, h, "fps 10-year minus Do Nothing by fps entry year, 2037 to 2047")]
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    yb = h - bot + 22
    out.append(f'<text x="4" y="{yb + 30:.1f}" class="tick">in eq.</text>')
    focus = 0
    for i, r in enumerate(rows):
        v, y, eq = r[key], r["fps_eis"], r["fps_in_any_eq"]
        bw = min(24, band * .55)
        x = left + i * band + (band - bw) / 2
        cx = x + bw / 2
        hl = y in (2041, 2044)
        if y == 2042:
            focus = cx + band / 2
        if hl:
            cap = "Snapshot" if y == 2041 else "3-year delay"
            end = sy(v) - 24 if v >= 0 else sy(0) - 4
            out.append(f'<text x="{cx:.1f}" y="{top - 14}" text-anchor="middle" class="ann">{cap}</text>'
                       f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{top - 8}" y2="{end:.1f}" class="leader"/>')
        out.append(f'<path d="{bar_path(x, bw, sy(0), sy(v))}" class="b {"pos" if v >= 0 else "neg"}{" hl" if hl else ""}"/>')
        out.append(f'<text x="{cx:.1f}" y="{yb:.1f}" text-anchor="middle" class="tick{" strong" if hl else ""}">{y}</text>')
        out.append(f'<circle cx="{cx:.1f}" cy="{yb + 26:.1f}" r="4.5" class="{"eqy" if eq else "eqn"}"/>')
        if hl:
            ly = sy(v) - 8 if v >= 0 else sy(v) + 17
            out.append(f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle" class="val">{num(v)}</text>')
        rows_t = ((num(v) + " $B", f"fps {y}: fps 10-year minus Do Nothing", None), ("yes" if eq else "no", "fps in any equilibrium", None))
        out.append(f'<rect x="{left + i * band:.1f}" y="{top}" width="{band:.1f}" height="{h - top - bot + 44}" class="hit" {mark_attrs(*rows_t)}/>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">$B, present value · Airbus NGSA + Re-engine A350 · Boeing Do Nothing on the 787</text>')
    out.append("</svg>")
    tv = tview("fps value by entry year", ["fps entry", "fps minus Do Nothing ($B)", "fps in any equilibrium"],
               [[r["fps_eis"], num(r[key]), "yes" if r["fps_in_any_eq"] else "no"] for r in rows])
    return "".join(out), tv, focus


# ------------------------------------------------------------------ chart 2: bridge 2041 -> 2044, timing grouped
def bridge_steps():
    d41 = DELAY["snapshot_2041"]["decomp_fps10_vs_dn"][MOD]
    d44 = DELAY["delay3_2044"]["decomp_fps10_vs_dn"][MOD]
    sp = A2["nb_split"]
    return [("fps 2041", d41["b_total_delta"], "t41"),
            ("Same cash,\n3 years later", sp["timing_only"], "step"),
            ("Bill paid later\n(present value)", d41["fps_pv_capex"] - d44["fps_pv_capex"], "step"),
            ("Lower debt\npenalty", d41["fps_alpha_pen"] - d44["fps_alpha_pen"], "step"),
            ("Deeper\nshare hole", sp["share_effect"], "step"),
            ("fps 2044", d44["b_total_delta"], "t44")]


def chart_bridge():
    steps = bridge_steps()
    w, h, left, right, top, bot = 760, 360, 56, 16, 48, 62
    lo, hi = -8, 2
    band = (w - left - right) / len(steps)
    bw = 38
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [svg_open(w, h, "Bridge from fps 2041 to fps 2044, fps minus Do Nothing in $B")]
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    timing = sum(v for _, v, _ in steps[1:4])
    bx0 = left + 1 * band + (band - bw) / 2
    bx1 = left + 3 * band + (band + bw) / 2
    by = top - 22
    out.append(f'<path d="M{bx0:.1f},{by + 8:.1f}V{by:.1f}H{bx1:.1f}V{by + 8:.1f}" class="bracket"/>'
               f'<text x="{(bx0 + bx1) / 2:.1f}" y="{by - 6:.1f}" text-anchor="middle" class="ann">Timing effects, net {num(timing)}</text>')
    run = 0.0
    for i, (lab, v, kind) in enumerate(steps):
        x = left + i * band + (band - bw) / 2
        cx = x + bw / 2
        if kind != "step":
            run = v
            vy = sy(v) - 8 if v >= 0 else sy(v) + 17
            out.append(f'<path d="{bar_path(x, bw, sy(0), sy(v))}" class="b {kind}"/>')
        else:
            y0, y1 = sy(run), sy(run + v)
            run += v
            vy = min(y0, y1) - 8
            out.append(f'<path d="M{x:.1f},{min(y0, y1):.1f}h{bw:.1f}v{abs(y1 - y0):.1f}h{-bw:.1f}Z" class="b {"pos" if v >= 0 else "neg"}"/>')
        out.append(f'<text x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle" class="val">{num(v)}</text>')
        if i < len(steps) - 1:
            nx = left + (i + 1) * band + (band - bw) / 2
            out.append(f'<line x1="{x + bw:.1f}" x2="{nx:.1f}" y1="{sy(run):.1f}" y2="{sy(run):.1f}" class="leader"/>')
        for k, part in enumerate(lab.split("\n")):
            out.append(f'<text x="{cx:.1f}" y="{h - bot + 20 + k * 15:.1f}" text-anchor="middle" class="tick{" strong" if kind != "step" else ""}">{esc(part)}</text>')
        out.append(f'<rect x="{left + i * band:.1f}" y="{top}" width="{band:.1f}" height="{h - top - bot}" class="hit" '
                   f'{mark_attrs((num(v) + " $B", lab.replace(chr(10), " "), None))}/>')
    out.append("</svg>")
    return "".join(out), timing


# ------------------------------------------------------------------ line charts with a crosshair
def line_chart(series, y_lo, y_hi, y_step, y_fmt, label, refs, aria_label, end_labels, notes, x_lo=2026, x_hi=2063, wash=None):
    """series: [(name, css var, [(year, value)])]; y_fmt 'pct' or 'int'; refs: [(y, text, 'above'|'below')]."""
    w, h, left, right, top, bot = 760, 346, 58, 172, 26, 46
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / (y_hi - y_lo) * (h - top - bot)
    fmt = (lambda v: f"{v * 100:.0f}%") if y_fmt == "pct" else (lambda v: f"{v:,.0f}")
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="{esc(aria_label, quote=True)}. Use the arrow keys to read values by year." tabindex="0">']
    t = y_lo
    while t <= y_hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{fmt(t)}</text>')
        t += y_step
    for yr in range(2030, x_hi + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    if wash:
        name, var, base = wash
        pts = [(x, v) for n, c, d in series if n == name for x, v in d if v > base]
        poly = " ".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in pts) + " " + " ".join(f"{sx(x):.1f},{sy(base):.1f}" for x, v in reversed(pts))
        out.append(f'<polygon points="{poly}" fill="var(--{var})" opacity=".12"/>')
    lab_x = left + 6
    for xv, txt in notes:   # notes first, so reference labels (with a halo) sit on top of the note line
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 5:.1f}" y="{top + 11}" class="ann">{esc(txt)}</text>')
        lab_x = max(lab_x, sx(xv) + 6)
    for yv, txt, pos in refs:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(yv):.1f}" y2="{sy(yv):.1f}" class="ref"/>'
                   f'<text x="{lab_x:.1f}" y="{sy(yv) + (15 if pos == "below" else -6):.1f}" class="reflab">{esc(txt)}</text>')
    for name, var, data in series:
        d = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in data)
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for (name, var, data), (dy, txt) in zip(series, end_labels):
        x, v = data[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
        lx = w - right + 8
        if sx(x) + 10 < lx:
            out.append(f'<line x1="{sx(x) + 6:.1f}" x2="{lx - 3:.1f}" y1="{sy(v):.1f}" y2="{sy(v) + dy:.1f}" class="leader"/>')
        out.append(f'<text x="{lx}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(txt)}</text>')
    years = sorted({x for _, _, d in series for x, _ in d})
    payload = {"x0": left, "x1": w - right, "xlo": x_lo, "xhi": x_hi, "w": w, "fmt": y_fmt, "years": years,
               "series": [{"name": n, "k": f"var(--{c})", "vals": {str(x): v for x, v in d}} for n, c, d in series]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">{esc(label)}</text></svg>')
    return "".join(out)


def chart_share():
    p = PAGE["paths"]
    ser = [(n, c, [(y, b) for y, b, a, u in p[n]]) for n, c in SCEN]
    svg = line_chart(ser, 0, .6, .1, "pct", "Boeing share of narrowbody deliveries (board rule)",
                     refs=[(.5, "50/50 balance point", "above")], aria_label="Boeing narrowbody share by year: fps 2041, fps 2044 and Boeing Do Nothing",
                     end_labels=[(0, "fps 2041: 48%"), (0, "fps 2044: 40%"), (0, "Do Nothing: 20%")], notes=[(2037, "NGSA enters")])
    rows = [[y] + [next((f"{b * 100:.0f}%" for yy, b, a, u in p[n] if yy == y), "—") for n, _ in SCEN] for y in range(2035, 2064)]
    return svg, tview("Boeing narrowbody share by year", ["Year"] + [n for n, _ in SCEN], rows)


def chart_airbus_units():
    p = PAGE["paths"]
    ser = [(n, c, [(y, u) for y, b, a, u in p[n] if y >= 2030]) for n, c in SCEN]
    svg = line_chart(ser, 800, 1700, 100, "int", "Airbus narrowbody deliveries a year implied by the board (2,000-a-year market)",
                     refs=[(900, "Rate 75 (Airbus’s stated plan)", "above"), (1200, "~100 a month (reported NGSA sizing)", "below")],
                     aria_label="Airbus narrowbody deliveries a year implied by the board, against rate 75 and about 100 a month",
                     end_labels=[(14, "fps 2041: 1,040"), (0, "fps 2044: 1,200"), (0, "Do Nothing: 1,600")],
                     notes=[(2037, "NGSA enters")], x_lo=2030, wash=("Boeing Do Nothing", "s3", 1200))
    rows = [[y] + [next((f"{u:,}" for yy, b, a, u in p[n] if yy == y), "—") for n, _ in SCEN] for y in range(2035, 2064)]
    return svg, tview("Airbus deliveries a year implied by the board", ["Year"] + [n for n, _ in SCEN], rows)


# ------------------------------------------------------------------ chart 4: NGSA lead
def lead_status(r):
    if r["fps_in_pure"]:
        return "fps in every pure equilibrium"
    if r["pure"] == 0:
        return "no pure equilibrium exists; fps near-Nash only"
    if r["fps_in_near"]:
        return "fps in a few near-Nash cells only"
    return "fps in no equilibrium"


def chart_lead():
    w, h, left, right, top, bot = 760, 392, 56, 16, 74, 62
    lo, hi = -6, 7
    leads = list(range(8, -1, -1))
    band = (w - left - right) / len(leads)
    sx = lambda L: left + (8 - L) * band + band / 2
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    rows = {fe: {r["lead"]: r for r in PAGE["ngsa_lead"][fe]} for fe in ("2041", "2044")}
    for fe in rows:   # the zones are drawn from this rule; fail loudly if the solved data disagree
        for L in leads:
            r = rows[fe][L]
            exp = "pure" if L <= 3 else "nopure" if L == 4 else "few" if L == 5 else "none"
            got = "pure" if r["fps_in_pure"] else "nopure" if r["pure"] == 0 else "few" if r["fps_in_near"] else "none"
            assert exp == got, (fe, L, got)
        assert rows[fe][8]["fps_minus_dn"] == rows[fe][9]["fps_minus_dn"] == rows[fe][7]["fps_minus_dn"]
    out = [svg_open(w, h, "fps 10-year minus Do Nothing by NGSA head start, for fps 2041 and fps 2044")]
    zones = [(8, 6, ["fps in no equilibrium"]), (5, 5, ["near-Nash,", "few cells"]), (4, 4, ["no pure eq.", "exists"]),
             (3, 0, ["fps in every pure equilibrium"])]
    for i, (a, b, lines) in enumerate(zones):
        x0, x1 = left + (8 - a) * band, left + (8 - b + 1) * band
        if i % 2 == 1:
            out.append(f'<rect x="{x0:.1f}" y="{top - 38}" width="{x1 - x0:.1f}" height="{h - bot - top + 38}" class="zone"/>')
        for k, part in enumerate(lines):
            out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{top - 22 - (len(lines) - 1 - k) * 13}" text-anchor="middle" class="zlab">{esc(part)}</text>')
    for t in range(-6, hi + 1, 2):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    for L in leads:
        out.append(f'<text x="{sx(L):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{L} yr</text>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - bot + 38}" text-anchor="middle" class="tick">NGSA head start over fps (years)</text>')
    for fe, var in (("2041", "s1"), ("2044", "s2")):
        d = "M" + " L".join(f"{sx(L):.1f},{sy(rows[fe][L]['fps_minus_dn']):.1f}" for L in leads)
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2" stroke-linejoin="round"/>')
        for L in leads:
            out.append(f'<circle cx="{sx(L):.1f}" cy="{sy(rows[fe][L]["fps_minus_dn"]):.1f}" r="4" fill="var(--{var})" class="ring"/>')
    for fe, L, l1, l2, tyv in (("2041", 4, "Snapshot: fps 2041,", "4-yr lead", 4.6), ("2044", 7, "Delay: fps 2044,", "7-yr lead", -5.3)):
        r = rows[fe][L]
        cx, cy = sx(L), sy(r["fps_minus_dn"])
        lx, ly = left + 8, sy(tyv)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9" class="mark"/>')
        if L == 4:
            out.append(f'<line x1="{cx - 8:.1f}" y1="{cy - 6:.1f}" x2="{lx + 152:.1f}" y2="{ly - 4:.1f}" class="leader"/>')
        else:
            out.append(f'<line x1="{cx - 2:.1f}" y1="{cy + 10:.1f}" x2="{cx - 2:.1f}" y2="{ly - 26:.1f}" class="leader"/>')
        out.append(f'<text x="{lx:.1f}" y="{ly - 14:.1f}" class="val">{esc(l1)}</text>'
                   f'<text x="{lx:.1f}" y="{ly + 2:.1f}" class="val">{esc(l2)} ({num(r["fps_minus_dn"])})</text>')
    for L in leads:   # one hit column per lead, reporting both fps dates
        a, b = rows["2041"][L], rows["2044"][L]
        lab = f"{L}-year lead" + (" or more" if L == 8 else "")
        rows_t = ((num(a["fps_minus_dn"]) + " $B", f"fps 2041, NGSA {a['ngsa_eis']}", "var(--s1)"),
                  (num(b["fps_minus_dn"]) + " $B", f"fps 2044, NGSA {b['ngsa_eis']}", "var(--s2)"),
                  (lead_status(b), lab, None))
        out.append(f'<rect x="{left + (8 - L) * band:.1f}" y="{top}" width="{band:.1f}" height="{h - top - bot}" class="hit" {mark_attrs(*rows_t)}/>')
    out.append("</svg>")
    tv = tview("fps value by NGSA head start", ["NGSA lead", "fps 2041 ($B)", "fps 2044 ($B)", "Status (both fps dates)"],
               [[f"{L} yr" + ("+" if L == 8 else ""), num(rows['2041'][L]['fps_minus_dn']), num(rows['2044'][L]['fps_minus_dn']), lead_status(rows['2044'][L])] for L in leads])
    return "".join(out), tv


# ------------------------------------------------------------------ chart 5: readings of the delay (wide + stacked)
def readings_rows():
    bt = ROB["bill_timing"]
    return [(["Board rule: bill paid at entry", "(a planned later programme)"], bt["board_lump"]["2041"], bt["board_lump"]["2044"]),
            (["Slip found after the bill is", "committed on the 2041 schedule"], None, bt["lump_at_2041"]["2044"]),
            (["…plus a 30% overrun", "paid at the new date"], None, bt["lump_at_2041_plus_30pct_at_2044"]["2044"]),
            (["Bill spread over the 6 years", "before entry into service"], bt["spread6"]["2041"], bt["spread6"]["2044"]),
            (["Bill spread over the 9 years", "before entry into service"], bt["spread9"]["2041"], bt["spread9"]["2044"]),
            (["Spent over 9 years on the 2041", "schedule, then a 3-year slip"], None, bt["slip_spread9"]["2044"])]


def chart_readings(stacked=False):
    rows = readings_rows()
    w, left, right, top, rowh, lab_h = (400, 10, 16, 8, 78, 38) if stacked else (760, 290, 40, 14, 50, 0)
    h = top + rowh * len(rows) + 46
    lo, hi = -24, 4
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [svg_open(w, h, "fps 10-year minus Do Nothing under six readings of the delay", "chart narrow" if stacked else "chart")]
    for t in range(lo, hi + 1, 8 if stacked else 4):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 40}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 24}" text-anchor="middle" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    for i, (lines, a, b) in enumerate(rows):
        y = top + i * rowh
        cy = y + lab_h + (rowh - lab_h) / 2 + (4 if stacked else 0)
        for k, ln in enumerate(lines):
            if stacked:
                out.append(f'<text x="{left}" y="{y + 14 + k * 16:.1f}" class="rowlab sm">{esc(ln)}</text>')
            else:
                out.append(f'<text x="{left - 14}" y="{cy - 4 + k * 16:.1f}" text-anchor="end" class="rowlab sm">{esc(ln)}</text>')
        out.append(f'<path d="{hbar_path(sx(0), sx(b), cy - 8, 16)}" class="b neg"/>')
        out.append(f'<text x="{sx(b) - 6:.1f}" y="{cy + 4:.1f}" text-anchor="end" class="val">{num(b)}</text>')
        if a is not None:
            out.append(f'<circle cx="{sx(a):.1f}" cy="{cy:.1f}" r="6" class="hollow"/>')
            if a >= 0:
                out.append(f'<text x="{sx(a) + 10:.1f}" y="{cy + 4:.1f}" class="val muted">{num(a)}</text>')
            else:
                out.append(f'<text x="{sx(a):.1f}" y="{cy - 12:.1f}" text-anchor="middle" class="val muted sm">{num(a)}</text>')
        rows_t = [(" ".join(lines), "", None), (num(b) + " $B", "fps 2044", None)] + ([(num(a) + " $B", "fps 2041", None)] if a is not None else [])
        out.append(f'<rect x="0" y="{y:.1f}" width="{w}" height="{rowh}" class="hit" {mark_attrs(*rows_t)}/>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 5}" text-anchor="middle" class="tick">fps 10-year minus Do Nothing, $B</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ chart 7: odds (wide + stacked)
ODDS = [("Third player", [("Embraer, independent entrant", 6, 10, "Clean sheet with sovereign or industrial partners, launched by 2035"),
                          ("COMAC, real exporter outside China", 11, 15, "EASA-validated C919 at 100+ a year abroad, or a funded export-grade new single-aisle"),
                          ("Embraer or COMAC (combined)", 15, 22, "They compete for the same gap, so slightly below independent odds (about 16% → 24%)")]),
        ("Not a third player", [("Boeing–Embraer Joint Venture or buy-back", 10, 12, "Embraer’s engineering goes into Boeing’s product"),
                                ("COMAC supplies 40%+ of China’s deliveries", 45, 50, "Takes Boeing’s China business; the bigger effect on Boeing")])]


def chart_odds(stacked=False):
    w, left, right, top, rowh, lab_h = (400, 10, 24, 6, 58, 22) if stacked else (760, 300, 40, 10, 40, 0)
    n = sum(len(r) for _, r in ODDS) + len(ODDS)
    h = top + rowh * n + 46
    lo, hi = 0, 60
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [svg_open(w, h, "Probability of each outcome with fps 2041 and fps 2044 (judgement)", "chart narrow" if stacked else "chart")]
    for t in range(lo, hi + 1, 20 if stacked else 10):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 40}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 24}" text-anchor="middle" class="tick">{t}%</text>')
    i = 0
    for grp, rows in ODDS:
        y = top + i * rowh + rowh / 2 + 6
        anchor = "start" if stacked else "end"
        out.append(f'<text x="{left if stacked else left - 14}" y="{y:.1f}" text-anchor="{anchor}" class="grp">{esc(grp.upper())}</text>')
        i += 1
        for lab, a, b, note in rows:
            y0 = top + i * rowh
            cy = y0 + lab_h + (rowh - lab_h) / 2
            strong = " strong" if "combined" in lab else ""
            if stacked:
                out.append(f'<text x="{left}" y="{y0 + 15:.1f}" class="rowlab sm{strong}">{esc(lab)}</text>')
            else:
                out.append(f'<text x="{left - 14}" y="{cy + 4:.1f}" text-anchor="end" class="rowlab sm{strong}">{esc(lab)}</text>')
            out.append(f'<line x1="{sx(a) + 7:.1f}" x2="{sx(b) - 6:.1f}" y1="{cy:.1f}" y2="{cy:.1f}" class="conn"/>')
            out.append(f'<circle cx="{sx(a):.1f}" cy="{cy:.1f}" r="6" class="hollow"/><circle cx="{sx(b):.1f}" cy="{cy:.1f}" r="5.5" class="filled"/>')
            out.append(f'<text x="{sx(b) + 12:.1f}" y="{cy + 4:.1f}" class="val">{a}% → {b}%</text>')
            out.append(f'<rect x="0" y="{y0:.1f}" width="{w}" height="{rowh}" class="hit" {mark_attrs((f"{a}% → {b}%", lab, None), (note, "", None))}/>')
            i += 1
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 5}" text-anchor="middle" class="tick">Probability (judgement)</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ chart 8: engine makers (wide + stacked)
ENG_SCEN = [("Snapshot (fps 2041)", "s1"), ("fps launched late", "s2"), ("Boeing Do Nothing (737 on LEAP)", "s3")]
MAKERS = [("CFM/GE", "cfm_b"), ("Pratt & Whitney", "pw_b"), ("Rolls-Royce", "rr_b")]


def chart_engines(stacked=False):
    keys = list(ENG.keys())
    w, left, right, top, lab_h = (400, 10, 10, 6, 24) if stacked else (760, 150, 30, 10, 0)
    bh, gap, grp = 14, 4, 22
    h = top + len(MAKERS) * (lab_h + 3 * (bh + gap) + grp) + 46
    lo, hi = (-80, 40) if stacked else (-70, 30)
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [svg_open(w, h, "Engine makers’ payoffs in three narrowbody outcomes", "chart narrow" if stacked else "chart")]
    for t in range(lo, hi + 1, 20 if stacked else 10):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 40}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 24}" text-anchor="middle" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    y = top
    for pn, fld in MAKERS:
        if stacked:
            out.append(f'<text x="{left}" y="{y + 16:.1f}" class="rowlab">{esc(pn)}</text>')
            y += lab_h
        else:
            out.append(f'<text x="{left - 14}" y="{y + 3 * (bh + gap) / 2 + 3:.1f}" text-anchor="end" class="rowlab">{esc(pn)}</text>')
        for k, (sn, var) in zip(keys, ENG_SCEN):
            v = ENG[k]["pure"][0][fld]
            zero = abs(v) < 0.005
            if not zero:
                out.append(f'<path d="{hbar_path(sx(0), sx(v), y, bh)}" fill="var(--{var})"/>')
            txt = "0" if zero else num(v, "+.2f")
            out.append(f'<text x="{sx(v) + (6 if v >= 0 else -6):.1f}" y="{y + bh - 3:.1f}" text-anchor="{"start" if v >= 0 else "end"}" class="val">{txt}</text>')
            out.append(f'<rect x="0" y="{y - gap / 2:.1f}" width="{w}" height="{bh + gap}" class="hit" {mark_attrs((txt + " $B", f"{pn}: {sn}", f"var(--{var})"))}/>')
            y += bh + gap
        y += grp
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 5}" text-anchor="middle" class="tick">$B against the engine board’s status quo</text>')
    out.append("</svg>")
    return "".join(out)


def both(fn):
    """Wide chart for desktop, stacked-label chart for phones; CSS shows one."""
    return f'<div class="only-wide cw">{fn(False)}</div><div class="only-narrow">{fn(True)}</div>'


# ------------------------------------------------------------------ Airbus decision cards
def airbus_cards():
    D = [("NGSA timing", [("Keep the plan: 2030 launch, ~2037 entry into service", 65), ("Slip for technology reasons", 25), ("Pull earlier", 10)],
          "Each year of NGSA slip costs Airbus $2.6–3.2B against a Boeing that does nothing ($4.7–5.3B against fps), and at a head start of 5 years or less fps comes back. Each year earlier pays about $3.8–4.1B. A deliberate slowdown to save cash is unlikely: it never pays.",
          "Profile rule “own clock”: don’t wait for Boeing; its default is the technology-ready year (entry 2035). Both war games launched NGSA in 2028 for 2035; the late-fps game noted “a delayed fps does not change it”. Public plan (Farnborough, July 2026): launch 2030, entry in the second half of the 2030s."),
         ("Delay Tactics", [("Drop them (if NGSA holds)", 95), ("Keep in reserve for a visible fps launch", 5)],
          "Worth +$1.16B only if Boeing actually launches fps. Against a Boeing that does nothing they cost $12.5B: the board’s “naked fine” applies (a $48.3B penalty for Delay Tactics with no fps to delay, about $12.1B in present value) plus about $0.4B of operating cost. They pay only if Boeing launches with more than about 91.5% probability.",
          "The war-game Airbus never used them in either game: always below its $1B test and against its integrity pillar. The profile says stop Delay Tactics once fps is off."),
         ("Widebody Chicken (now the main contest)", [("Stay out once Boeing re-engines the 787 first", 50), ("Pre-empt with an A350 Re-engine", 30), ("Both re-engine", 10), ("Neither", 10)],
          "Chicken: each side wants to re-engine only if the other doesn’t, so whoever commits first wins. A350 Re-engine alone +50.12; stay out +47.68; both +45.36. Pre-empting gains $1.8B if Boeing stays out but loses $2.3B if Boeing re-engines anyway, so it fails Airbus’s own test of beating Do Nothing by $1B against every plausible Boeing move.",
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
        bars = "".join(f'<li class="{"top" if p == top_p else ""}"><span class="ol">{esc(o)}</span><span class="pb" aria-hidden="true"><span class="pf" style="width:{p}%"></span></span>'
                       f'<span class="pv">{p}%</span></li>' for o, p in opts)
        out.append(f'<article class="panel dcard"><h3>{esc(title)}</h3><p class="label">Probability (judgement)</p><ul class="probs">{bars}</ul>'
                   f'<p class="label">On the board</p><p>{esc(board)}</p><p class="label">Profile and war games</p><p class="muted">{esc(ev)}</p></article>')
    return "".join(out)


SOURCES = [
    ("Airbus", [("NGSA launch around 2030, entry in the late 2030s (Farnborough, July 2026)", "https://leehamnews.com/2026/07/28/airbus-walks-line-between-shareholder-returns-and-clean-sheet-ambitions/"),
                ("NGSA prepared for about 100 a month (search snippet)", "https://www.airdatanews.com/airbus-targets-100-aircraft-per-month-for-a320-successor/"),
                ("H1 2026 results: rate 70–75 by end-2027, stabilising at 75", "https://www.airbus.com/en/newsroom/press-releases/2026-07-airbus-reports-half-year-h1-2026-results"),
                ("Rate 83 under study for the A320neo", "https://leehamnews.com/2026/08/19/airbus-pushing-to-increase-monthly-a320neo-production-rate-sooner-than-later/"),
                ("€5B buyback and 2029 targets", "https://www.airbus.com/en/newsroom/press-releases/2026-07-airbus-to-present-new-mid-term-outlook-strengthen-commitment-to-profitable-growth-and-shareholder"),
                ("Faury: Embraer should “think twice”", "https://www.airdatanews.com/airbus-ceo-says-embraer-should-think-twice-before-entering-narrowbody-market/")]),
    ("Embraer", [("Outlook 2026: a 180–240 seat design explored", "https://leehamnews.com/2026/01/12/outlook-2026-embraer-well-positioned-but-new-airplane-launch-fraught-with-risk/"),
                 ("Head of research and technology on a future single-aisle", "https://centreforaviation.com/news/embraer-exploring-new-executive-and-commercial-jets-supersonic-a-possibility-head-of-rt-1362926"),
                 ("Partner talks (WSJ, May 2024)", "https://tovima.com/wsj/brazils-embraer-plots-a-new-737-sized-jet-to-rival-boeing"),
                 ("Q2 2026 results and guidance", "https://leehamnews.com/2026/08/10/embraer-posts-record-q2-revenue-as-deliveries-hit-16-year-high/"),
                 ("Financials, segments, estimates and 2010–2026 call transcripts: Embraer files in the repository root", None),
                 ("Fitch upgrade to BBB (September 2026) and the CEO’s “three or four” manufacturers (FT, October 2025): secondary sources, no link kept", None)]),
    ("COMAC", [("C919 deliveries against target", "https://www.bloomberg.com/news/articles/2025-12-23/china-s-comac-on-track-to-miss-c919-delivery-target-by-half"),
               ("Production ramp and IBA forecasts", "https://leehamnews.com/2026/09/01/boosting-c919-production-rates-remains-comacs-real-test/"),
               ("EASA validation could take up to six years", "https://avitrader.com/2025/04/29/easa-comacs-c919-certification-could-take-up-to-six-years/"),
               ("EASA test pilots find no major hardware risks", "https://www.scmp.com/economy/china-economy/article/3361170/eu-test-pilots-find-no-major-hardware-risks-chinas-c919-jet-sources"),
               ("LEAP-1C licences suspended (May 2025)", "https://www.freemalaysiatoday.com/category/business/2025/05/29/us-suspends-engine-sales-to-chinese-planemaker-comac"),
               ("US caps parts licences to COMAC (Reuters, unnamed sources)", "https://virginiabusiness.com/us-slows-aircraft-part-exports-to-china-trade-talks/"),
               ("AirAsia C919 talks", "https://www.airdatanews.com/airasia-comac-c919-potential-order/"),
               ("Malaysia Airlines evaluation", "https://www.airdatanews.com/malaysia-airlines-keeps-c919-under-evaluation-but-awaits-easa-approval/")]),
    ("Boeing", [("737 cleared to 47 a month", "https://qz.com/boeing-737-max-production-rate-47-month-060526"),
                ("China confirms 200 Boeing aircraft after the May 2026 summit", "https://www.airdatanews.com/china-confirms-boeing-order-for-200-aircraft-after-trump-xi-summit/"),
                ("CEO: next narrowbody “moving to the right” (Aviation Week, 2026; no link kept)", None)]),
]


CSS = r"""
:root {
  --bg: #f4f6f9; --surface: #ffffff; --sunk: #eef2f7; --line: #d5dce6; --grid: #e3e8ef;
  --fg: #141c28; --muted: #556275; --faint: #8a95a5;
  --s1: #2a78d6; --s2: #eb6834; --s3: #1baf7a;
  --pos: #3b4a5e; --neg: #9aa6b6;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --r: 8px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70;
  --pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70;
  --pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
a { color: inherit; text-decoration-color: var(--faint); text-underline-offset: 2px; }
.wrap { max-width: 1140px; margin: 0 auto; padding: 0 20px 56px; }
header.top { padding: 34px 0 10px; }
.eyebrow { font: 500 .74rem/1.4 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
h1 { font: 700 clamp(2.1rem, 5vw, 3.2rem)/1.02 var(--font-display); margin: 10px 0 12px; letter-spacing: .01em; }
h2 { font: 700 1.9rem/1.1 var(--font-display); margin: 0 0 10px; }
h3 { font: 600 1.3rem/1.2 var(--font-display); margin: 0 0 8px; letter-spacing: .02em; }
p { margin: 0 0 10px; }
.lede { font-size: 1.08rem; max-width: 80ch; }
.muted { color: var(--muted); } .small { font-size: .86rem; }
.nw { white-space: nowrap; }
nav.toc { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 14px 0 6px; font-size: .9rem; }
nav.toc a { color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--line); }
nav.toc a:hover { color: var(--fg); }
section { margin-top: 44px; }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 18px 20px; }
.stack > * + * { margin-top: 14px; }
.label { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
.ctitle { font: 600 1.05rem/1.3 var(--font-body); margin: 0 0 4px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(196px, 1fr)); gap: 12px; margin-top: 18px; }
.tile .k { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.tile .v { font: 600 1.45rem/1.2 var(--font-body); margin: 6px 0 4px; letter-spacing: -.01em; text-wrap: balance; }
.tile .d { font-size: .86rem; color: var(--muted); line-height: 1.4; }
.gloss { margin-top: 12px; font-size: .88rem; color: var(--muted); max-width: 110ch; }
.gloss b { color: var(--fg); font-weight: 600; }
.bl { display: grid; gap: 10px; margin-top: 14px; counter-reset: bl; }
.bl .panel { display: grid; grid-template-columns: 34px 1fr; gap: 4px 12px; }
.bl .panel::before { counter-increment: bl; content: counter(bl); font: 700 1.5rem/1 var(--font-display); color: var(--muted); }
.bl b { display: block; font: 600 1.15rem/1.25 var(--font-display); letter-spacing: .02em; margin-bottom: 2px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.grid2 > * { min-width: 0; }
.cw { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.chart { width: 100%; height: auto; display: block; overflow: visible; }
.only-narrow { display: none; }
.chart .grid { stroke: var(--grid); } .chart .zero { stroke: var(--muted); }
.chart .ref { stroke: var(--muted); stroke-width: 1; }
.chart .reflab { fill: var(--muted); font: 500 11px var(--font-mono); paint-order: stroke; stroke: var(--surface); stroke-width: 4px; stroke-linejoin: round; }
.chart .tick { fill: var(--muted); font: 11px var(--font-mono); }
.chart .tick.strong { fill: var(--fg); font-weight: 600; }
.chart .rowlab { fill: var(--fg); font: 600 14px var(--font-body); }
.chart .rowlab.sm { font: 500 12.5px var(--font-body); }
.chart .rowlab.strong { font-weight: 700; }
.chart .grp { fill: var(--muted); font: 500 10.5px var(--font-mono); letter-spacing: .1em; }
.chart .val { fill: var(--fg); font: 500 12.5px var(--font-mono); paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
.chart .val.muted { fill: var(--muted); }
.chart .val.sm { font-size: 11px; }
.chart .ann { fill: var(--muted); font: 600 11px var(--font-mono); letter-spacing: .04em; paint-order: stroke; stroke: var(--surface); stroke-width: 4px; stroke-linejoin: round; }
.chart .zlab { fill: var(--muted); font: 500 11px var(--font-mono); }
.chart .zone { fill: var(--sunk); }
.chart .endlab { fill: var(--fg); font: 500 12px var(--font-mono); }
.chart .leader { stroke: var(--faint); stroke-width: 1; }
.chart .bracket { fill: none; stroke: var(--muted); stroke-width: 1.2; }
.chart .b.pos { fill: var(--pos); } .chart .b.neg { fill: var(--neg); } .chart .b.t41 { fill: var(--s1); } .chart .b.t44 { fill: var(--s2); }
.chart .b.hl { stroke: var(--fg); stroke-width: 1.5; }
.chart .eqy { fill: var(--fg); } .chart .eqn { fill: none; stroke: var(--faint); stroke-width: 1.5; }
.chart .ring { stroke: var(--surface); stroke-width: 2; }
.chart .mark { fill: none; stroke: var(--fg); stroke-width: 1.5; }
.chart .hollow { fill: var(--surface); stroke: var(--fg); stroke-width: 2; }
.chart .filled { fill: var(--fg); stroke: var(--surface); stroke-width: 2; }
.chart .conn { stroke: var(--faint); stroke-width: 2; }
.chart .hit, .chart .xhit { fill: transparent; }
.chart .hit:hover { fill: var(--fg); fill-opacity: .05; }
.chart .hit:focus { outline: none; }
.chart .hit:focus-visible { fill: var(--fg); fill-opacity: .08; stroke: var(--fg); stroke-width: 1.5; }
.chart .cross { stroke: var(--muted); stroke-width: 1; }
.chart.xh:focus { outline: none; }
.chart.xh:focus-visible { outline: 2px solid var(--fg); outline-offset: 4px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: .85rem; color: var(--muted); margin: 6px 0 6px; }
.legend i { display: inline-block; vertical-align: middle; margin-right: 6px; }
.legend i.ln { width: 16px; height: 2px; border-radius: 1px; }
.legend i.sq { width: 11px; height: 11px; border-radius: 3px; }
.legend i.dot { width: 10px; height: 10px; border-radius: 50%; background: var(--fg); }
.legend i.ring { width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--fg); }
.legend i.ringf { width: 11px; height: 11px; border-radius: 50%; border: 1.5px solid var(--faint); }
.legend i.bar { width: 14px; height: 10px; border-radius: 2px; }
.cap { font-size: .88rem; color: var(--muted); margin: 8px 0 0; }
.cap b { color: var(--fg); }
.tip { position: fixed; z-index: 20; pointer-events: none; display: none; max-width: 320px; background: var(--surface); color: var(--fg);
  border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; font-size: .82rem; box-shadow: 0 6px 18px rgba(0,0,0,.18); }
.tip div { display: flex; align-items: baseline; gap: 6px; line-height: 1.35; }
.tip b { font: 600 .86rem var(--font-mono); white-space: nowrap; }
.tip span.l { color: var(--muted); }
.tip .k { display: inline-block; width: 12px; height: 2px; border-radius: 1px; flex: none; align-self: center; }
.tip .yr { font: 600 .78rem var(--font-mono); color: var(--muted); margin-bottom: 4px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
details.tv { margin-top: 8px; font-size: .88rem; }
details.tv summary { cursor: pointer; color: var(--muted); }
details.tv table { margin-top: 8px; }
.loop { display: flex; flex-wrap: wrap; gap: 6px; align-items: stretch; margin: 12px 0 6px; padding: 0; list-style: none; counter-reset: lp; }
.loop li { flex: 1 1 150px; border: 1px solid var(--line); border-radius: 6px; padding: 9px 11px; background: var(--sunk); font-size: .9rem; }
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
thead th.n { text-align: right; }
tbody th { font-weight: 500; }
td.n { text-align: right; font-family: var(--font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
tbody tr:last-child > * { border-bottom: 0; }
.callout { border-left: 4px solid var(--fg); }
ul.cav { margin: 0; padding-left: 18px; } ul.cav li { margin-bottom: 6px; }
.facts { margin: 0; padding-left: 18px; } .facts li { margin-bottom: 4px; }
.src { columns: 2 300px; column-gap: 28px; font-size: .86rem; }
.src h3 { font-size: 1.05rem; margin: 0 0 4px; break-after: avoid; }
.src ul { margin: 0 0 12px; padding-left: 18px; break-inside: avoid; } .src li { margin-bottom: 3px; }
.lede, .bl .panel, .dcard p, .facts li, ul.cav li, .cap, .gloss { text-wrap: pretty; }
footer { margin-top: 40px; font-size: .82rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 12px; }
@media (max-width: 760px) {
  .wrap { padding: 0 16px 48px; }
  .grid2, .dcards { grid-template-columns: 1fr; }
  .panel { padding: 14px; }
  .only-wide { display: none; } .only-narrow { display: block; }
  .chart { min-width: 620px; } .chart.narrow { min-width: 0; }
  ul.probs li { grid-template-columns: minmax(0, 1fr) 60px 36px; }
  .chart .tick, .chart .reflab, .chart .ann { font-size: 13px; }
  .chart .val, .chart .endlab, .chart .rowlab.sm { font-size: 14px; }
  .chart .grp { font-size: 12px; } .chart .val.sm { font-size: 12.5px; }
  .chart.narrow .tick { font-size: 12px; } .chart.narrow .val, .chart.narrow .rowlab.sm { font-size: 13px; }
  tbody th { min-width: 8.5rem; }
  thead th { white-space: normal; }
}
@media (prefers-reduced-motion: no-preference) { a { transition: color .15s; } }
"""

JS = r"""
(() => {
  const tip = document.createElement('div'); tip.className = 'tip'; tip.setAttribute('aria-hidden', 'true'); document.body.appendChild(tip);
  const live = document.createElement('div'); live.className = 'sr'; live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite'); document.body.appendChild(live);
  let lastKey = null;
  const place = (x, y) => {
    const r = tip.getBoundingClientRect(), pad = 12;
    let left = x + 14, top = y + 14;
    if (left + r.width > innerWidth - pad) left = x - r.width - 14;
    if (top + r.height > innerHeight - pad) top = y - r.height - 14;
    tip.style.left = Math.max(pad, left) + 'px'; tip.style.top = Math.max(pad, top) + 'px';
  };
  const show = (key, rows, x, y, head) => {
    if (key !== lastKey) {
      tip.replaceChildren();
      if (head) { const h = document.createElement('div'); h.className = 'yr'; h.textContent = head; tip.appendChild(h); }
      for (const r of rows) {
        const d = document.createElement('div');
        if (r.k) { const k = document.createElement('span'); k.className = 'k'; k.style.background = r.k; d.appendChild(k); }
        const v = document.createElement('b'); v.textContent = r.v; d.appendChild(v);
        if (r.l) { const l = document.createElement('span'); l.className = 'l'; l.textContent = r.l; d.appendChild(l); }
        tip.appendChild(d);
      }
      lastKey = key;
    }
    tip.style.display = 'block'; place(x, y);
  };
  const hide = () => { tip.style.display = 'none'; lastKey = null; };
  let n = 0;
  document.querySelectorAll('[data-tip]').forEach(el => {
    const rows = JSON.parse(el.dataset.tip), key = 'm' + (n++);
    el.addEventListener('pointermove', e => show(key, rows, e.clientX, e.clientY));
    el.addEventListener('pointerleave', hide);
    el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); show(key, rows, r.left + r.width / 2, r.top + r.height / 2); });
    el.addEventListener('blur', hide);
  });
  document.querySelectorAll('rect[data-cross]').forEach((hit, c) => {
    const P = JSON.parse(hit.dataset.cross), svg = hit.ownerSVGElement, line = svg.querySelector('.cross'), box = svg.parentElement;
    const fmt = v => P.fmt === 'pct' ? Math.round(v * 100) + '%' : Math.round(v).toLocaleString('en-US');
    const xOf = yr => P.x0 + (yr - P.xlo) / (P.xhi - P.xlo) * (P.x1 - P.x0);
    let idx = Math.floor(P.years.length / 2);
    const rowsAt = yr => P.series.filter(s => s.vals[yr] !== undefined).map(s => ({ v: fmt(s.vals[yr]), l: s.name, k: s.k }));
    const render = (cx, cy, announce) => {
      const yr = P.years[idx], x = xOf(yr);
      line.setAttribute('x1', x); line.setAttribute('x2', x); line.setAttribute('visibility', 'visible');
      const rows = rowsAt(yr);
      show('x' + c + '-' + yr, rows, cx, cy, String(yr));
      if (announce) live.textContent = yr + ': ' + rows.map(r => r.l + ' ' + r.v).join(', ');
    };
    const follow = () => {   // keep the crosshair in view when the chart scrolls inside its panel
      const scale = svg.getBoundingClientRect().width / P.w, px = xOf(P.years[idx]) * scale;
      if (px < box.scrollLeft + 20 || px > box.scrollLeft + box.clientWidth - 20) box.scrollLeft = px - box.clientWidth / 2;
    };
    const fromEvent = e => {
      const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      const p = pt.matrixTransform(svg.getScreenCTM().inverse());
      const yr = P.xlo + (p.x - P.x0) / (P.x1 - P.x0) * (P.xhi - P.xlo);
      let best = 0; P.years.forEach((y, i) => { if (Math.abs(y - yr) < Math.abs(P.years[best] - yr)) best = i; });
      idx = best; render(e.clientX, e.clientY, false);
    };
    hit.addEventListener('pointermove', fromEvent);
    hit.addEventListener('pointerdown', fromEvent);
    hit.addEventListener('pointerleave', () => { line.setAttribute('visibility', 'hidden'); hide(); });
    const keyRender = () => { follow(); const r = svg.getBoundingClientRect(); render(r.left + xOf(P.years[idx]) * r.width / P.w, r.top + 24, true); };
    svg.addEventListener('keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault(); idx = Math.max(0, Math.min(P.years.length - 1, idx + (e.key === 'ArrowRight' ? 1 : -1))); keyRender();
    });
    svg.addEventListener('focus', keyRender);
    svg.addEventListener('blur', () => { line.setAttribute('visibility', 'hidden'); hide(); });
  });
  // charts that scroll on phones open on their point of interest
  document.querySelectorAll('.cw[data-focus]').forEach(box => {
    const svg = box.querySelector('svg'); if (!svg || box.scrollWidth <= box.clientWidth) return;
    const scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    box.scrollLeft = Math.max(0, +box.dataset.focus * scale - box.clientWidth / 2);
  });
})();
"""


def build():
    s41, s44 = DELAY["snapshot_2041"], DELAY["delay3_2044"]
    c41, c44 = s41["boeing_by_airbus_ctx"], s44["boeing_by_airbus_ctx"]
    v41, v44 = c41[MOD]["Milk_787"]["fps10_vs_dn"], c44[MOD]["Milk_787"]["fps10_vs_dn"]
    d41, d44 = c41[DT]["Milk_787"]["fps10_vs_dn"], c44[DT]["Milk_787"]["fps10_vs_dn"]
    proj, sp = A2["project_split"], A2["nb_split"]
    bt, w787 = ROB["bill_timing"], ROB["with_787_reengine"]
    LT, lev = ROB["lever_thresholds_2044"], ROB["pure_equilibrium_levers_2044"]
    vac, ent = VAC["cases"], VAC["entrant_sensitivities"]
    p44 = s44["pure"]
    a41 = s41["airbus_best_response"]["fps10 + Do Nothing 787"]["da"]
    a44 = s44["airbus_best_response"]["fps10 + Do Nothing 787"]["da"]
    a_dn = p44[0]["da"]
    b41_typ = c41[DT]["Milk_787"]["fps10"]
    keys = list(ENG.keys())
    cfm0, cfm2 = ENG[keys[0]]["pure"][0]["cfm_b"], ENG[keys[2]]["pure"][0]["cfm_b"]
    pw0, pw2 = ENG[keys[0]]["pure"][0]["pw_b"], ENG[keys[2]]["pure"][0]["pw_b"]
    rr0 = ENG[keys[0]]["pure"][0]["rr_b"]
    steps = bridge_steps()
    net = v44 - v41
    dec41, dec44 = DELAY["snapshot_2041"]["decomp_fps10_vs_dn"][MOD], DELAY["delay3_2044"]["decomp_fps10_vs_dn"][MOD]

    # guards: the prose below states these numbers
    assert rnd(-proj["pure_timing"], 2) == 0.28 and rnd(-sp["share_effect"], 2) == 3.31 and rnd(net, 2) == -3.59
    assert lev["fps margin %"]["34.1"]["fps_in_pure"] > 0 and lev["fps margin %"]["34.0"]["fps_in_pure"] == 0
    assert lev["fps 10yr bill $B"]["40.7"]["fps_in_pure"] > 0 and lev["fps 10yr bill $B"]["40.9"]["fps_in_pure"] == 0
    assert lev["fps price $M"]["73.0"]["fps_in_pure"] > 0 and lev["Boeing recovery pp/yr"]["2.3"]["fps_in_pure"] > 0
    assert lev["Boeing recovery pp/yr"]["2.25"]["fps_in_pure"] == 0
    assert rnd(a44 - a41, 1) == 8.4 and rnd(a_dn - a41, 1) == 10.9 and rnd(cfm2 - cfm0, 0) == 38 and rnd(pw0 - pw2, 0) == 4

    eis_svg, eis_tv, eis_focus = chart_eis()
    bridge_svg, timing_net = chart_bridge()
    share_svg, share_tv = chart_share()
    lead_svg, lead_tv = chart_lead()
    units_svg, units_tv = chart_airbus_units()

    tiles = [("fps vs Do Nothing", f"{num(v41)} → {num(v44)}", f"$B, present value. Against Airbus Delay Tactics: {num(d41)} → {num(d44)}"),
             ("fps in equilibrium", "14 of 17 → none", "On time, fps (either ramp) is in 14 of the 17 near-Nash outcomes; at 2044 it is in none of the 4 (2 pure, 2 near-Nash)"),
             ("Airbus gain", f"+${rnd(a44 - a41, 1):.1f}–{rnd(a_dn - a41, 1):.1f}B", f"+${rnd(a44 - a41, 1):.1f}B if Boeing still launches a late fps; +${rnd(a_dn - a41, 1):.1f}B in the new equilibrium where Boeing does nothing (vs the snapshot’s typical outcome)"),
             ("Third player", "~15% → ~22%", "Embraer or COMAC entering (judgement)"),
             ("CFM vs the snapshot", f"+${rnd(cfm2 - cfm0, 0):.0f}B", f"Its engine-board loss shrinks from {num(cfm0, '+.1f')}B to {num(cfm2, '+.1f')}B if Boeing keeps the 737 on LEAP")]
    tiles_html = "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles)

    numbers = table(["Boeing: fps 10-year Solo minus Do Nothing ($B)", "fps 2041 (snapshot)", "fps 2044 (delay)"], [
        ["Airbus NGSA + Re-engine A350, Boeing Do Nothing on the 787", f"<b>{num(v41)}</b>", f"<b>{num(v44)}</b>"],
        ["…against Airbus Delay Tactics (the “slip test”)", num(d41), num(d44)],
        ["Boeing also re-engines the 787", num(w787["2041"]["vs_A350_reengine"]), num(w787["2044"]["vs_A350_reengine"])],
        ["fps 7-year Solo instead", num(c41[MOD]["Milk_787"]["fps7_vs_dn"]), num(c44[MOD]["Milk_787"]["fps7_vs_dn"])],
        ["fps via Embraer ($100B, paid by Boeing) instead", num(c41[MOD]["Milk_787"]["via_embraer_vs_dn"]), num(c44[MOD]["Milk_787"]["via_embraer_vs_dn"])]],
        num_cols=(1, 2))
    readings_tv = tview("fps value by reading of the delay", ["Reading of the delay", "fps 2041", "fps 2044"],
                        [[" ".join(l), num(a) if a is not None else "—", num(b)] for l, a, b in readings_rows()])
    bridge_tv = tview("bridge, 2041 → 2044", ["Driver", "$B"], [
        ["fps 2041", num(v41)], ["Same cash, 3 years later", num(steps[1][1])],
        [f"Bill paid later (present value {dec41['fps_pv_capex']:.2f} → {dec44['fps_pv_capex']:.2f})", num(steps[2][1])],
        [f"Lower debt penalty ({dec41['fps_alpha_pen']:.2f} → {dec44['fps_alpha_pen']:.2f})", num(steps[3][1])],
        ["Timing effects, net", num(timing_net)], ["Deeper share hole", num(steps[4][1])],
        ["fps 2044", num(v44)], ["Change, 2041 → 2044", num(net)]])
    levers = table(["Lever (snapshot value)", "Beats Do Nothing", "Beats Do Nothing by $1B", "Back in a pure equilibrium"], [
        ["fps margin (25.64%)", f"{LT['fps margin %']['breakeven']:.1f}%", f"{LT['fps margin %']['hurdle_1B']:.1f}%", "<b>34.1%</b>"],
        ["fps 10-year bill ($55.25B)", f"${LT['fps 10yr bill $B']['breakeven']:.1f}B", f"${LT['fps 10yr bill $B']['hurdle_1B']:.1f}B", f"<b>${LT['fps 10yr bill $B']['breakeven_vs_delay_tactics']:.1f}B</b>"],
        ["fps price ($55M)", f"${LT['fps price $M']['breakeven']:.1f}M", f"${LT['fps price $M']['hurdle_1B']:.1f}M", f"<b>${LT['fps price $M']['breakeven_vs_delay_tactics']:.1f}M</b>"],
        ["Boeing’s share recovery after entry (1 point/yr)", f"{REC['breakeven_modal']:.2f}", f"{REC['hurdle_1B_modal']:.2f}", f"<b>{REC['breakeven_delay_tactics']:.2f}</b>"],
        ["“fps via Embraer” bill paid by Boeing ($100B)", f"${LT['fps via Embraer bill $B']['breakeven']:.1f}B", "—", "—"]], num_cols=(1, 2, 3))
    eqtab = table(["2044 equilibrium", "Airbus", "Boeing", "Airbus $B", "Boeing $B"], [
        ["A", "NGSA + Re-engine A350", "Do Nothing 737 + Do Nothing 787", num(p44[0]["da"]), num(p44[0]["db"])],
        ["B", "NGSA + Do Nothing A350", "Do Nothing 737 + Re-engine 787", num(p44[1]["da"]), num(p44[1]["db"])],
        ["<i>Snapshot, typical outcome</i>", "<i>NGSA + Delay Tactics + Re-engine A350</i>", "<i>fps 10-year + Do Nothing 787</i>", f"<i>{num(a41)}</i>", f"<i>{num(b41_typ)}</i>"]],
        num_cols=(3, 4))
    gap = table(["Unserved demand 2037–2056 (aircraft)", "fps 2041", "fps 2044, launched", "Boeing Do Nothing (the 2044 equilibrium)"], [
        [lab, *[f"{vac[c][f'unserved_cap{cap}']['cum_2037_2056']:,}" for c in ("fps 2041", "fps 2044", "Boeing Do Nothing")]]
        for lab, cap in (("Airbus at rate 75 (900/yr)", 900), ("Airbus at ~100 a month (1,200/yr)", 1200), ("Airbus at ~110 a month (1,320/yr)", 1320))],
        num_cols=(1, 2, 3))
    E = lambda k: [num(ent[k][c]) for c in ("fps 2041", "fps 2044", "Boeing Do Nothing")]
    entrant = table(["Entrant NPV, $B (board conventions)", "fps 2041", "fps 2044", "Boeing Do Nothing"], [
        ["Bill paid at entry in 2038, Airbus capped at 1,200 a year", *E("lump_eis2038_cap1200")],
        ["Embraer-realistic timing (entry 2042), bill paid at entry", *E("lump_eis2042_cap1200")],
        ["Same, but bill spread over 2034–41", *E("spread2034_41_eis2042_cap1200")],
        ["The 737 at rate 47 absorbs part of the overflow (entry 2038)", *E("lump_eis2038_cap1200_737_rate47")],
        ["Airbus capped at rate 75, 900 a year (entry 2038)", *E("lump_eis2038_cap900")]], num_cols=(1, 2, 3))
    embraer_paths = table(["Embraer path", "fps 2041 (judgement)", "fps 2044 (judgement)"], [
        ["Independent 180–210 seat clean sheet with sovereign or industrial partners, launched by 2035 (<b>third player</b>)", "~5%", "~8%"],
        ["Smaller 150–170 seat step above the E195-E2 (counts only above 150 seats)", "~1–2%", "~2–3%"],
        ["<b>Embraer becomes a third player</b>", "<b>~6%</b>", "<b>~10%</b>"],
        ["Boeing’s partner: Joint Venture or buy-back (not a third player)", "~10%", "~12%"]], num_cols=(1, 2))
    comac_paths = table(["COMAC path", "fps 2041 (judgement)", "fps 2044 (judgement)"], [
        ["EASA-validated C919 exported at 100+ a year outside China by 2045 (<b>third player</b>)", "~7–11%", "~9–15%"],
        ["Funded, export-oriented new single-aisle by 2035 (<b>third player</b>; no study is cited, and the C929 widebody competes for engineers)", "~5%", "~7%"],
        ["<b>COMAC becomes a third player</b> (either path; they overlap)", "<b>~11%</b>", "<b>~15%</b>"],
        ["COMAC supplies 40% or more of China’s single-aisle deliveries by 2045 (<b>not</b> a third player, but the bigger effect)", "~45%", "~50%"]], num_cols=(1, 2))
    eng_rows = [[l, num(v["pure"][0]["cfm_b"]), num(v["pure"][0]["pw_b"]), num(v["pure"][0]["rr_b"]) if abs(v["pure"][0]["rr_b"]) >= 0.005 else "0"]
                for l, v in zip(["Snapshot (fps 2041, fps engines from all three, Boeing 50%)", "fps launched late, Boeing at ~30% of the new-generation market",
                                 "Boeing Do Nothing: 737 stays on LEAP at 20%"], ENG.values())]
    eng_tv = tview("engine makers", ["Outcome", "CFM/GE", "Pratt & Whitney", "Rolls-Royce"], eng_rows)

    scen_leg = "".join(f'<span><i class="ln" style="background:var(--{c})"></i>{esc(n)}</span>' for n, c in SCEN)
    eng_leg = "".join(f'<span><i class="sq" style="background:var(--{var})"></i>{esc(sn)}</span>' for sn, var in ENG_SCEN)
    src_html = "".join(f"<h3>{esc(g)}</h3><ul>" + "".join(
        f'<li><a href="{esc(u, quote=True)}" rel="noopener" target="_blank">{esc(t)}</a></li>' if u else f"<li>{esc(t)}</li>" for t, u in items) + "</ul>"
        for g, items in SOURCES)
    cap_tbl = table(["If Airbus…", "Airbus captures the delay gain?", "The gap left for others"], [
        ["Holds rate 75 and prices the scarcity", "No: it earns price, not volume", "Large: about 700 a year on the board’s share rule; queues lengthen, the 737 sells more, an entrant has a case"],
        ["Builds NGSA for ~100 a month, as the 2026 reports suggest", "Yes, largely", "Smaller but real: up to 400 a year on the board’s share rule (about 150 on the war-game path)"]])

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>fps Three Years Late</title>
<meta name="description" content="What a 3-year fps delay (entry into service 2041 to 2044) does to Boeing's business case on the dashboard, how Airbus would respond, and the odds of Embraer or COMAC entering.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><span class="eyebrow">Game-theory dashboard snapshot · fps entry into service 2041 → 2044</span>
<h1>fps Three Years Late</h1>
<p class="lede">What a 3-year fps delay does to Boeing’s business case on your dashboard, how Airbus would respond, and the odds that it brings Embraer or COMAC in as a third player. Everything else stays as in the snapshot: NGSA in service 2037, both Re-engines 2035, and the snapshot’s costs, margins, prices and capture speeds. The analysis also draws on our two war games: fps on time (wg5-2045) and fps three years late (wg5-2045d).</p>
<nav class="toc" aria-label="Contents"><a href="#bottom-line">Bottom line</a><a href="#business-case">Business case</a><a href="#airbus">Airbus’s response</a><a href="#third-player">Third player</a><a href="#engines">Engine makers</a><a href="#board">Board vs snapshot</a><a href="#limits">Limits</a><a href="#sources">Sources</a></nav>
</header>
<main>
<section id="bottom-line"><h2>The fps case flips from indifferent to no, and Airbus wins by doing little</h2>
<div class="tiles">{tiles_html}</div>
<p class="gloss"><b>Reading the numbers.</b> $B is present value at 2026 against the status quo (Boeing discounts at 10.5%, Airbus at 8%). A <b>pure equilibrium</b> is an outcome where neither company gains by changing its own moves. A <b>near-Nash</b> outcome is one where neither gains more than the board’s tolerance of one yield point (about $1.3B for Boeing), so it is stable in practice. A <b>cell</b> is one combination of Airbus and Boeing moves. The numbers use the board build that reproduces your snapshot exactly (see <a href="#board">board vs snapshot</a>).</p>
<div class="bl">
<div class="panel"><div><b>The fps business case flips from “indifferent” to “no”.</b>fps (10-year ramp) against Do Nothing goes from {usd(v41, sign=True)} to {usd(v44)}, and from {usd(d41)} to {usd(d44)} against Airbus Delay Tactics. On time no outcome is fully stable and fps is in most of the near-stable ones; three years late the only stable outcomes (2 pure equilibria) have Boeing doing nothing on the narrowbody. These are the board’s mildest numbers: they assume a planned delay with the bill deferred too. If the slip is found after the bill is committed, fps is {usd(bt['lump_at_2041']['2044'])}, or {usd(bt['lump_at_2041_plus_30pct_at_2044']['2044'])} with a 30% overrun.</div></div>
<div class="panel"><div><b>The cause is share, not discounting.</b>NGSA gets 7 years alone instead of 4, so Boeing re-enters at 20% share instead of 28% and, at 1 point a year, never gets back to parity inside the window. The share hole costs {usd(-sp['share_effect'])}; the timing effects net to only {usd(-proj['pure_timing'])}. NGSA’s head start decides it: fps is a pure equilibrium only when NGSA leads by 3 years or less. The snapshot’s 4-year lead is the knife edge; the delay makes it 7.</div></div>
<div class="panel"><div><b>Airbus’s best response is to do very little.</b>Keep NGSA on its 2030-launch plan (slowing it never pays: each year of slip costs Airbus $2.6–3.2B), drop Delay Tactics (the delay does their job, and against a Boeing that doesn’t launch they cost about $12.5B), and let the contest move to the widebody game of Chicken. Airbus gains $8.4–10.9B on the board, but almost all of it is narrowbody volume beyond what it can build today. Whether Airbus adds that capacity also sets the odds of a third player.</div></div>
<div class="panel"><div><b>A third player becomes more likely, but stays the less likely outcome.</b>Judgement: Embraer or COMAC enters ~15% → ~22%; Embraer independently ~6% → ~10%; COMAC as a real exporter ~11% → ~15%. More likely: Airbus builds more and prices the scarcity, 737 MAX volumes stay higher than the board assumes, and (≈45% → 50% chance) COMAC supplies 40% or more of China’s single-aisle deliveries by 2045, taking Boeing’s China business. That hurts Boeing more than any exporting entrant.</div></div>
<div class="panel"><div><b>Our late-fps war game reached the same end state.</b>Boeing failed its own go/no-go test (−0.73 against a +$1B hurdle), re-engined the 787 instead, and Airbus shelved the A350 Re-engine: the board’s second equilibrium. The two models differ in calibration but agree on direction and end state.</div></div>
<div class="panel"><div><b>A Boeing that doesn’t launch fps is a large gain for CFM.</b>About +$38B against the snapshot, because the LEAP-powered 737 keeps Boeing’s slot. Rolls-Royce loses its narrowbody entry ({usd(rr0, sign=True)} in the snapshot) and Pratt &amp; Whitney about $4B. Your engine board has a CFM “Partner Embraer” move it never evaluates; included, it is in every engine equilibrium.</div></div>
</div></section>

<section id="business-case"><h2>Business case: fps goes from indifferent to clearly negative</h2>
<div class="stack">
<div class="panel"><p class="ctitle">fps stops paying from 2042 and drops out of every equilibrium from 2043</p>
<p class="label">fps 10-year minus Do Nothing by fps entry year ($B)</p>
<div class="legend"><span><i class="bar" style="background:var(--pos)"></i>fps beats Do Nothing</span><span><i class="bar" style="background:var(--neg)"></i>fps loses</span><span><i class="dot"></i>fps in an equilibrium</span><span><i class="ringf"></i>in none</span></div>
<div class="cw" data-focus="{eis_focus:.0f}">{eis_svg}</div>{eis_tv}
<p class="cap">2042 is slightly negative but inside the board’s $1.3B tolerance, so fps is still near-stable there. After 2044 the value rises slightly; that is a quirk of the board’s evaluation window (entry into service + 19 years), which makes a later fps the same losing project, discounted further.</p></div>
{numbers}
<div class="panel callout"><h3>At 2041 Boeing is indifferent, not committed</h3>
<p>+$1.06B is inside Boeing’s tolerance band of one yield point ($1.3B). The snapshot has no pure equilibrium because the best responses chase each other in a loop. Delay Tactics keep Boeing out at 2041; at 2044 the delay does that job by itself. fps 10-year appears in 13 of the 17 near-Nash cells, and fps 7-year in one more.</p>
<ol class="loop" aria-label="Best-response loop at 2041"><li>Boeing launches fps</li><li>Airbus answers with Delay Tactics</li><li>Boeing switches to Do Nothing</li><li>Airbus drops Delay Tactics, which would now trigger the board’s penalty</li><li class="back">Boeing launches fps again, and the loop restarts</li></ol></div>
</div>

<h3 style="margin-top:30px">Why it flips: share, not discounting</h3>
<div class="stack">
<div class="panel"><p class="ctitle">The three timing effects almost cancel; the deeper share hole flips the case</p>
<p class="label">Bridge, fps minus Do Nothing, 2041 → 2044 ($B)</p>
<div class="legend"><span><i class="bar" style="background:var(--s1)"></i>fps 2041 total</span><span><i class="bar" style="background:var(--s2)"></i>fps 2044 total</span><span><i class="bar" style="background:var(--pos)"></i>Raises the case</span><span><i class="bar" style="background:var(--neg)"></i>Lowers it</span></div>
<div class="cw">{bridge_svg}</div>{bridge_tv}
<p class="cap">The same cash arriving three years later costs {usd(-steps[1][1])}, but your board books the fps bill as one payment at entry into service, so paying it later saves {usd(steps[2][1])} plus {usd(steps[3][1])} of debt penalty: timing nets to a cost of only {usd(-timing_net)}. <b>The deeper share hole ({usd(-steps[4][1])}) is what flips the case</b>, for a total change of {usd(net)}.</p></div>
<div class="panel"><p class="ctitle">Boeing re-enters from 20% instead of 28%, and never recovers to parity</p>
<p class="label">Boeing narrowbody share by year (board rule)</p>
<div class="legend">{scen_leg}</div>
<div class="cw">{share_svg}</div>{share_tv}
<p class="cap">NGSA takes 3 points of share a year from 2037 until fps arrives, up to an 80% cap; fps then wins back 1 point a year. With fps in 2041 Boeing reaches 48% by 2060; with fps in 2044 only 40% by 2063. Boeing never returns to the 50/50 balance point, so that slider has no effect.</p></div>
<div class="panel"><p class="ctitle">NGSA’s head start decides it: 3 years or less and fps is an equilibrium again</p>
<p class="label">fps 10-year minus Do Nothing by NGSA head start ($B)</p>
<div class="legend"><span><i class="ln" style="background:var(--s1)"></i>fps 2041</span><span><i class="ln" style="background:var(--s2)"></i>fps 2044</span></div>
<div class="cw" data-focus="260">{lead_svg}</div>{lead_tv}
<p class="cap">The rule is the same for both fps dates. At a head start of 3 years or less fps is in every pure equilibrium. At 4 years fps beats Do Nothing head to head, but no pure equilibrium exists (the snapshot sits here). At 5 years fps survives only in a few near-Nash cells; at 6 or more it is in none. The delay moves the head start from 4 years to 7. Head starts of 7 years or more give the same values, because NGSA’s capture has hit its 80% cap.</p></div>
</div>

<h3 style="margin-top:30px">It depends on what kind of delay this is</h3>
<div class="panel"><p class="ctitle">However the delay is read, fps at 2044 loses money; only the size changes</p>
<p>Your board books the entire fps bill as one payment in the entry-into-service year, so a later fps looks cheaper (+$4.1B). That only holds if the delay is planned and the spending moves with it. The positive 2041 case exists only under that rule; a stale caption in the board says the bill is spread over the 9 years before entry, and if it were, fps would already be a no-go on time.</p>
<div class="legend"><span><i class="bar" style="background:var(--neg)"></i>fps 2044</span><span><i class="ring"></i>fps 2041</span></div>
{both(chart_readings)}{readings_tv}</div>

<h3 style="margin-top:30px">What would bring fps back at 2044</h3>
<p class="muted">Each lever moves on its own; every level is solved on the board.</p>
{levers}
<p class="cap" style="margin-top:10px"><b>Breaking even is not enough.</b> Between “beats Do Nothing” and the pure-equilibrium level the board cycles with no pure equilibrium; fps settles only once it beats Do Nothing even against Delay Tactics. “fps via Embraer” differs from the 10-year Solo (Boeing alone) only in its bill, so its break-even is the same {usd(LT['fps via Embraer bill $B']['breakeven'], 1)}, less than half the $100B the slider is set to.</p>

<h3 style="margin-top:30px">What the game becomes</h3>
{eqtab}
<div class="grid2" style="margin-top:14px">
<div class="panel"><b>Boeing’s own payoff hardly moves</b> ({num(b41_typ)} → {num(p44[0]['db'])}). Do Nothing was already almost as good as fps. The delay destroys the option, the fps path back into the narrowbody market, and leaves Boeing at 20% narrowbody share from 2043. Its best remaining move is to re-engine the 787 first (equilibrium B): winning the widebody Chicken is worth +$5.6B to Boeing and only +$2.4B to Airbus.</div>
<div class="panel"><b>Our late-fps war game reached the same end state.</b> In wg5-2045d Boeing failed its own go/no-go test (−0.73 against a +$1B hurdle; −4.71 against Delay Tactics), re-engined the 787 instead, and Airbus shelved the A350 Re-engine: equilibrium B. Its calibration differs (NGSA 2035, a $30B fps bill), but measured as NGSA head start it also crosses the knife edge, from 3 years to 6.</div>
</div></section>

<section id="airbus"><h2>Airbus’s response: hold, drop Delay Tactics, and decide on capacity</h2>
<p class="muted">The board solves for what pays; Airbus’s behavioural profile and both war games show what Airbus tends to do. Probabilities are judgement; board values are solved. They depend on each other: if NGSA slips to 2039–2041, fps comes back and Delay Tactics come back with it, so the 95% “drop” assumes NGSA holds.</p>
<div class="dcards">{airbus_cards()}</div>
<div class="panel" style="margin-top:14px"><p class="ctitle">The capacity decision links Airbus’s response to the third-player question</p>
<p class="label">Airbus narrowbody deliveries a year implied by the board</p>
<div class="legend">{scen_leg}</div>
<div class="cw">{units_svg}</div>{units_tv}
<p class="cap">The board gives Airbus 80% of a 2,000-a-year market from 2043 if Boeing does nothing: about 1,600 aircraft a year, against 900 at rate 75 or 1,200 at about 100 a month (the shaded gap). Even before NGSA the board gives Airbus 60% of 2,000, or 1,200 a year, above rate 75, so compare the scenarios with each other rather than reading the units as forecasts. On the board the delay is worth +$8.4B to Airbus against a launched fps ({num(a41)} → {num(a44)}), and NGSA margin on volume above 1,200 a year rises by the same $8.4B. <b>Every dollar of Airbus’s delay gain is volume it cannot build today.</b></p>
<div style="margin-top:12px">{cap_tbl}</div></div>
</section>

<section id="third-player"><h2>Third player: more likely, still the less likely outcome</h2>
<div class="panel"><p class="ctitle">The delay raises the odds by about half; COMAC taking China is the bigger effect</p>
<p class="label">Probabilities, fps 2041 → fps 2044 (judgement)</p>
<div class="legend"><span><i class="ring"></i>fps 2041</span><span><i class="dot"></i>fps 2044</span></div>
{both(chart_odds)}
<p class="cap">Independent odds would be about 16% → 24%; the combined figure is a little lower because Embraer and COMAC compete for the same unserved demand. <b>Definition.</b> A third player is a company other than Boeing or Airbus that, by 2045, delivers a 150–210 seat single-aisle at 100 or more a year (5% of the board’s market) to customers outside its home country, or that has committed funding to such a programme by 2035. Entering as Boeing’s partner (the board’s “fps via Embraer” Joint Venture) does not count.</p></div>

<h3 style="margin-top:30px">How big is the gap, and can an entrant make money in it?</h3>
<p>The size of the gap depends on Airbus’s capacity. Board aircraft are treated as real aircraft a year; 2,000 a year is close to the OEMs’ forecasts for the 2040s.</p>
{gap}
<ul class="facts" style="margin-top:10px"><li><b>The board overstates the gap.</b> In the late-fps war game Boeing still holds 32% in 2045, so the 2045 gap above 1,200 a year is about 150 aircraft, not 400.</li>
<li><b>The 737 already exceeds the board’s Boeing slot.</b> Boeing built 447 737s in 2025 and is cleared to 47 a month, above the 400 a year the board allows. Part of the overflow becomes queues.</li></ul>
<p class="muted" style="margin-top:12px">Entrant economics on the board’s conventions ($48M price, 12% margin, 10% WACC, a $15B programme, serving only demand Airbus cannot build):</p>
{entrant}
<p class="cap" style="margin-top:10px"><b>The delay improves an entrant’s case by about $2B, but Airbus’s capacity moves it more than the delay does.</b> With realistic spending an entrant needs Airbus to stay at rate 75 or a protected home market. COMAC’s case doesn’t hinge on this: its development spending is sunk and its capital comes from the state.</p>

<div class="grid2" style="margin-top:18px">
<div class="panel"><h3>Embraer</h3>
<p class="label">Capability</p><ul class="facts">
<li>Market value about $13B (August 2026); FY2025 revenue $7.6B, adjusted operating profit $0.66B; investing about $0.4B a year.</li>
<li>The E2 cost $1.7B and came in under budget. A 150–210 seat clean sheet costs $10–25B, so partners would fund roughly two-thirds to four-fifths. Fitch upgraded Embraer to BBB in September 2026.</li></ul>
<p class="label" style="margin-top:10px">What it says and does</p><ul class="facts">
<li>“Studies for a new cycle of products… commercial jet or business jet” (May 2026). Leeham (January 2026) reports a 180–240 seat design being explored; its head of research and technology calls a single-aisle “one of our potential products” (June 2026). The CEO said the market has room for “three or four” manufacturers (FT, October 2025, via secondary sources).</li>
<li>Partner talks with PIF, Korea, Japan, Turkey and India are early; nothing is funded. In 2011 Embraer waited for Boeing’s choice, then built the E2; Boeing walked away from their Joint Venture in 2020. Faury told Embraer in June 2026 to “think twice”.</li>
<li>Embraer’s 2016 entry rule (incumbents leaving the 104–150 seat segment) is not triggered: a Boeing that does nothing keeps the 737 there.</li></ul>
<div style="margin-top:12px">{embraer_paths}</div>
<p class="cap"><b>Money is the binding constraint, not demand.</b> The delay roughly doubles the opportunity but not the ability to fund it.</p></div>
<div class="panel"><h3>COMAC</h3>
<p class="label">Where it stands</p><ul class="facts">
<li>The C919 (158–192 seats) has been in service since 2023 on Chinese certification only. Deliveries were 10–13 in 2024 and 15 in 2025, against a 2025 target cut to 25; 2026 is tracking at about 25–28. COMAC targets 150 a year by 2027–28 and 200 by 2029, with about $6B of new state capital.</li>
<li>Over 1,000 orders, almost all Chinese. AirAsia confirmed purchase talks (September 2025); Malaysia Airlines is evaluating.</li>
<li>EASA validation expected 2028–31; test flying reportedly found no major hardware issues (July 2026).</li>
<li>US parts: LEAP-1C licences were suspended May–July 2025; in October 2026 Reuters reported, citing unnamed sources, a cap on parts licences to COMAC. China’s CJ-1000A engine is expected around 2027–28.</li></ul>
<div style="margin-top:12px">{comac_paths}</div>
<p class="cap"><b>What binds COMAC is production, US parts and certification, not demand.</b> The delay mostly gives Beijing more reason to steer Chinese orders to COMAC and to Airbus’s Tianjin line.</p></div>
</div>
<div class="grid2" style="margin-top:14px">
<div class="panel"><h3>Who bears the risk</h3><p><b>An exporting entrant mostly fills demand Airbus cannot build</b>: chiefly an Airbus risk, and a check on Airbus’s delay gain.</p><p><b>COMAC taking China hits Boeing.</b> China is about 20% of global single-aisle demand. Losing about 6% of the board’s market (about 30% of China) wipes out the 2041 fps case (+1.06 → 0). If COMAC takes 10% of the board’s market (about half of China), the 2044 case deepens from −2.53 to −3.46.</p></div>
<div class="panel"><h3>Signals to watch</h3><ul class="facts">
<li><b>Airbus:</b> an NGSA production-rate decision; a line or engine deal above rate 75.</li>
<li><b>Embraer:</b> money signed with PIF, Korea or Japan; an engine selection; investment above about $0.4B a year rather than buybacks.</li>
<li><b>COMAC:</b> deliveries above 60 in 2028 and 100 in 2030; EASA validation; firm orders outside China; formal US parts caps.</li>
<li><b>Boeing:</b> a narrowbody launch around 2031–34, or silence. Its CEO said in 2026 that the next narrowbody is “moving to the right”.</li></ul></div>
</div></section>

<section id="engines"><h2>Engine makers: Boeing staying on the 737 is a large gain for CFM</h2>
<div class="stack">
<div class="panel"><p class="ctitle">CFM stays negative against the engine board’s status quo, but is $38B better off if Boeing keeps the 737</p>
<p class="label">Engine board, pure equilibrium, three narrowbody outcomes ($B)</p>
<div class="legend">{eng_leg}</div>
{both(chart_engines)}{eng_tv}
<p class="cap">The engine board ignores whether Boeing launches fps, so the delay’s end state is represented by setting Boeing’s slot to the 737 on LEAP at 20% share. <b>CFM gains about $38B</b>; Rolls-Royce loses its narrowbody entry (it does nothing on narrowbody, so its value is 0); Pratt &amp; Whitney gives up about $4B. In both war games Pratt &amp; Whitney cancelled its next-generation geared turbofan in 2031, and CFM never used its Embraer lever.</p></div>
<div class="panel"><h3>CFM’s hidden “Partner Embraer” move</h3><p>It exists in your code but is never among the 16 CFM moves the board evaluates, because the board keeps only the first four combinations for each base move. Included, it enters every pure engine equilibrium (as Ducted + Partner Embraer + a GEnx upgrade), worth +$2.5B to CFM in the snapshot and +$0.6B if Boeing does nothing. It is a fixed +5 points of share, so it says nothing about the delay, but it shows your board would favour an engine maker backing Embraer.</p></div>
</div></section>

<section id="board"><h2>Board vs snapshot: your snapshot came from a later build</h2>
<div class="panel"><ul class="facts">
<li><b>Attached file:</b> charges the full $3B Boeing two-front strain whenever fps and a 787 Re-engine are developed together. Solved as uploaded it gives 1 pure and 13 near-Nash equilibria and misses 4 of your 17 cells.</li>
<li><b>Overlap-aware strain</b> (strain scaled by how far the two development windows overlap) reproduces the snapshot exactly: 0 pure and 17 near-Nash, the same cells and every rounded yield. Boeing’s windows overlap one year in five, so its strain is $0.6B. A flat strain of $1.55B or less would also fit, but the snapshot prints $3.00B.</li>
<li><b>What it changes:</b> only cells where Boeing also re-engines the 787. Both rules give the same equilibria at 2044.</li>
<li><b>The engine board can’t see the delay.</b> It takes the earlier of fps and NGSA (2037) as the narrowbody entry year. That is a decoupling in the board, not evidence that engine makers are unaffected.</li>
</ul>
<p class="cap"><b>How it was done.</b> Your board was solved headlessly (Streamlit never runs; a mock harness executes its code). Five AI analysts covered Airbus’s response, Embraer, COMAC, an independent re-derivation of every board number and a completeness review, each with an adversarial checker, and three more checked this page; their corrections are applied.</p></div></section>

<section id="limits"><h2>Limits to keep in mind</h2><div class="panel"><ul class="cav">
<li><b>Bill timing.</b> The board pays the whole programme bill in the entry-into-service year. This drives both the positive 2041 case and the “cheaper delay” (see the readings above).</li>
<li><b>Evaluation window.</b> It runs from 2026 to entry into service + 19, so Boeing’s Do Nothing payoff moves with the fps slider (by $0.13B between 2041 and 2044). On a common calendar horizon the delay costs Boeing $3.9–4.8B, not the $3.59B drop in the bridge; the verdict holds for any horizon up to 2089.</li>
<li><b>No third player, capacity, price or move order.</b> The board lets Airbus build 1,600 a year and has no Embraer or COMAC. Who moves first in the widebody Chicken comes from the war game.</li>
<li><b>Slider settings.</b> The $48.3B penalty for Delay Tactics without an fps is discounted to the fps date; “fps via Embraer” is $100B, the slider’s maximum.</li>
<li><b>Board build.</b> The uploaded build is not the one that produced the snapshot. The engine board doesn’t read Boeing’s launch decision, and CFM’s Embraer move is never evaluated.</li>
<li><b>War games.</b> Each is one run, calibrated differently (NGSA 2035, a $30B fps bill), and neither had a third airframer.</li>
<li><b>Web evidence.</b> Some 2026 facts were seen only in search snippets: NGSA at about 100 a month, the October 2026 parts-licence caps, and some Embraer quotes.</li>
</ul></div></section>

<section id="sources"><h2>Sources</h2><div class="panel src">{src_html}
<p class="small muted">Board numbers: the attached dashboard and snapshot, solved by the scripts in wargame/reports/dashboard-fps-delay/analysis (run_all.sh reproduces every board number on this page). Airbus behaviour: its profile and the two war games in wargame/reports. Full analyst notes with every citation: wargame/reports/dashboard-fps-delay/review.</p></div></section>
</main>
<footer>fps Three Years Late · probabilities are judgement; board values are solved on your dashboard with overlap-aware strain.</footer>
</div><script>{JS}</script></body></html>"""
    assert page.count("<svg viewBox") == 11, page.count("<svg viewBox")
    return page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fps_delay_assessment.html")
    page = build()
    with open(out, "w") as f:
        f.write(page)
    print(out, len(page))
