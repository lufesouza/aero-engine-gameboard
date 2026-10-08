"""Shared page kit for the dash-2050 report: formatting helpers, chart primitives, CSS and JS.
Copied from the fps-delay page (wargame/reports/dashboard-fps-delay/make_fps_delay_html.py) so both reports share one
design system."""
import html
import json
from decimal import Decimal, ROUND_HALF_UP

esc = html.escape
MINUS = "\u2212"


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
    name = "; ".join((f"{l}: {v}" if v else l) if l else v for v, l, k in rows)
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


def tview(title, head, rows, num_cols=None):
    """Table view inside <details>; each row's first cell is a row header. num_cols: numeric columns (default all)."""
    nc = set(num_cols) if num_cols is not None else set(range(1, len(head)))
    th = "".join(f'<th scope="col"{" class=n" if i in nc else ""}>{esc(h)}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else f'<td{" class=n" if j in nc else ""}>{c}</td>')
                                    for j, c in enumerate(r)) + "</tr>" for r in rows)
    return (f'<details class="tv"><summary>Table view: {esc(title)}</summary><div class="scroll"><table>'
            f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></details>')


def table(head, rows, num_cols=()):
    th = "".join(f'<th scope="col"{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else f'<td{" class=n" if j in num_cols else ""}>{c}</td>')
                                    for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'



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



CSS = r"""
:root {
  --bg: #f4f6f9; --surface: #ffffff; --sunk: #eef2f7; --line: #d5dce6; --grid: #e3e8ef;
  --fg: #141c28; --muted: #556275; --faint: #8a95a5;
  --s1: #2a78d6; --s2: #eb6834; --s3: #17a06f;
  --pos: #3b4a5e; --neg: #8792a3;
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
.chart.xh:focus-visible { outline: none; }
.cw:has(> .chart.xh:focus-visible) { outline: 2px solid var(--fg); outline-offset: 2px; border-radius: 4px; }
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
.tip span.l { color: var(--muted); flex: 1 1 auto; min-width: 0; }
.tip .k { display: inline-block; width: 12px; height: 2px; border-radius: 1px; flex: none; align-self: center; }
.tip .yr { font: 600 .78rem var(--font-mono); color: var(--muted); margin-bottom: 4px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
details.tv { margin-top: 8px; font-size: .88rem; }
details.tv summary { cursor: pointer; color: var(--muted); }
details.tv table { margin-top: 8px; }
.loop { display: flex; flex-wrap: wrap; gap: 6px; align-items: stretch; margin: 12px 0 6px; padding: 0; list-style: none; counter-reset: lp; }
.loop li { flex: 1 1 150px; border: 1px solid var(--line); border-radius: 6px; padding: 9px 11px; background: var(--sunk); font-size: .9rem; }
.loop li::before { counter-increment: lp; content: counter(lp); font: 600 .78rem var(--font-mono); color: var(--muted); display: block; }
.zkey { margin: 8px 0 0; padding-left: 20px; font-size: .86rem; color: var(--muted); }
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
  th, td { padding: 7px 6px; font-size: .86rem; }
  thead th { white-space: normal; letter-spacing: .02em; }
  tbody th { min-width: 7rem; }
}
@media (max-width: 900px) { .grid2 { grid-template-columns: 1fr; } }
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
        if (r.v) { const v = document.createElement('b'); v.textContent = r.v; d.appendChild(v); }
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

