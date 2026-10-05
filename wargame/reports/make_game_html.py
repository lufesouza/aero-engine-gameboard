#!/usr/bin/env python3
"""Build a self-contained HTML report of a finished (or running) war-game run.

Usage: python3 wargame/reports/make_game_html.py <run id> <out.html> [--narrative <narrative.json>]

Everything numeric comes from the engine: the run state, the round reports (engine `rounds`), the
final report and the referee scorecard. The optional narrative JSON adds the referee's words:

  {"title": "...", "lede": "...", "summary": ["paragraph", ...], "findings": ["...", ...],
   "rounds": {"1": "commentary", ...}, "players": {"boeing": {"verdict": "...", "highlights": ["..."]}},
   "caveats": ["...", ...], "leadership": {"boeing": "ortberg-malave-pope-2026", ...}}

The page holds every player's orders and private rationale: it is a referee's document.
"""
import argparse
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from wargame import engine as E  # noqa: E402
from wargame import model as M  # noqa: E402
from wargame import solver as S  # noqa: E402

esc = html.escape
COLORS = {"boeing": "var(--boeing)", "airbus": "var(--airbus)", "rolls_royce": "var(--rolls_royce)",
          "pratt_whitney": "var(--pratt_whitney)", "cfm": "var(--cfm)", "other_makers": "var(--faint)"}


def comp_text(comp):
    return "; ".join(k.replace("_", " ") + f" {v:+.1f}" for k, v in comp.items() if abs(v) >= 0.05)


def slips_text(slips):
    return "; ".join(f"+{x['years']}y {x['cause']}" for x in slips) or "–"


def label(cfg, s):
    return "Other makers" if s == "other_makers" else M.player_label(cfg, s)


def fmt_b(x, sign=True):
    if x is None:
        return "–"
    return f"{x:+,.1f}" if sign else f"{x:,.1f}"


def pct(x):
    return "–" if x is None else f"{x * 100:.1f}%"


# ---------------------------------------------------------------------------
# SVG charts (inline, theme-aware through CSS variables)
# ---------------------------------------------------------------------------

def line_chart(series, x0, x1, y0, y1, title, fmt=lambda v: f"{v:.0%}", dashed=(), marks=(), w=560, h=240):
    """series: [(name, color, [(x, y)])]. marks: [(x, text)] vertical rules."""
    pl, pr, pt, pb = 46, 12, 16, 28
    W, H = w - pl - pr, h - pt - pb
    sx = lambda x: pl + (x - x0) / (x1 - x0) * W
    sy = lambda y: pt + (1 - (y - y0) / (y1 - y0)) * H
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" class="chart">']
    for i in range(5):
        v = y0 + (y1 - y0) * i / 4
        out.append(f'<line x1="{pl}" x2="{w - pr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/>'
                   f'<text x="{pl - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{esc(fmt(v))}</text>')
    step = 5 if x1 - x0 <= 40 else 10
    for x in range(x0 - x0 % step + (step if x0 % step else 0), x1 + 1, step):
        out.append(f'<text x="{sx(x):.1f}" y="{h - 8}" text-anchor="middle" class="tick">{x}</text>')
    for x, t in marks:
        out.append(f'<line x1="{sx(x):.1f}" x2="{sx(x):.1f}" y1="{pt}" y2="{pt + H}" class="mark"/>'
                   f'<text x="{sx(x) + 3:.1f}" y="{pt + 10}" class="tick">{esc(t)}</text>')
    for name, color, pts in series:
        if not pts:
            continue
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(pts))
        dash = ' stroke-dasharray="5 4"' if name in dashed else ""
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2"{dash}><title>{esc(name)}</title></path>')
    out.append("</svg>")
    leg = "".join(f'<span class="lg"><i style="background:{c}{";opacity:.5" if n in dashed else ""}"></i>{esc(n)}</span>'
                  for n, c, _ in series)
    return f'<figure class="fig"><figcaption>{esc(title)}</figcaption>{"".join(out)}<div class="legend">{leg}</div></figure>'


def stacked_chart(layers, xs, title, marks=(), w=560, h=240):
    """layers: [(name, color, [y per x])] summing to <= 1."""
    pl, pr, pt, pb = 46, 12, 16, 28
    W, H = w - pl - pr, h - pt - pb
    x0, x1 = xs[0], xs[-1]
    sx = lambda x: pl + (x - x0) / (x1 - x0) * W
    sy = lambda y: pt + (1 - y) * H
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" class="chart">']
    for i in range(5):
        v = i / 4
        out.append(f'<line x1="{pl}" x2="{w - pr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/>'
                   f'<text x="{pl - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{v:.0%}</text>')
    for x in range(x0 - x0 % 5 + (5 if x0 % 5 else 0), x1 + 1, 5 if x1 - x0 <= 40 else 10):
        out.append(f'<text x="{sx(x):.1f}" y="{h - 8}" text-anchor="middle" class="tick">{x}</text>')
    base = [0.0] * len(xs)
    for name, color, ys in layers:
        top = [b + y for b, y in zip(base, ys)]
        d = "M" + " L".join(f"{sx(x):.1f},{sy(t):.1f}" for x, t in zip(xs, top))
        d += " L" + " L".join(f"{sx(x):.1f},{sy(b):.1f}" for x, b in reversed(list(zip(xs, base)))) + " Z"
        out.append(f'<path d="{d}" fill="{color}" fill-opacity=".78" stroke="none"><title>{esc(name)}</title></path>')
        base = top
    for x, t in marks:
        out.append(f'<line x1="{sx(x):.1f}" x2="{sx(x):.1f}" y1="{pt}" y2="{pt + H}" class="mark"/>'
                   f'<text x="{sx(x) + 3:.1f}" y="{pt + 10}" class="tick">{esc(t)}</text>')
    out.append("</svg>")
    leg = "".join(f'<span class="lg"><i style="background:{c}"></i>{esc(n)}</span>' for n, c, _ in layers)
    return f'<figure class="fig"><figcaption>{esc(title)}</figcaption>{"".join(out)}<div class="legend">{leg}</div></figure>'


def bar_chart(groups, players, values, title, cfg, w=560, h=250):
    """Grouped bars: groups (round labels) x players; values[(group, player)] in $B (can be negative)."""
    pl, pr, pt, pb = 50, 12, 16, 30
    W, H = w - pl - pr, h - pt - pb
    vals = [v for v in values.values() if v is not None] or [0]
    lo, hi = min(0, min(vals)), max(0, max(vals))
    pad = (hi - lo) * .08 or 1
    lo, hi = lo - pad, hi + pad
    sy = lambda y: pt + (1 - (y - lo) / (hi - lo)) * H
    gw = W / len(groups)
    bw = gw * .8 / len(players)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" class="chart">']
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        out.append(f'<line x1="{pl}" x2="{w - pr}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/>'
                   f'<text x="{pl - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{v:+.0f}</text>')
    out.append(f'<line x1="{pl}" x2="{w - pr}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" class="zero"/>')
    for gi, g in enumerate(groups):
        gx = pl + gi * gw + gw * .1
        for pi, p in enumerate(players):
            v = values.get((g, p))
            if v is None:
                continue
            y_top, y_bot = sy(max(v, 0)), sy(min(v, 0))
            out.append(f'<rect x="{gx + pi * bw:.1f}" y="{y_top:.1f}" width="{bw * .9:.1f}" height="{max(1, y_bot - y_top):.1f}" '
                       f'fill="{COLORS[p]}"><title>{esc(label(cfg, p))} {esc(g)}: {v:+.2f} $B</title></rect>')
        out.append(f'<text x="{pl + gi * gw + gw / 2:.1f}" y="{h - 9}" text-anchor="middle" class="tick">{esc(g)}</text>')
    out.append("</svg>")
    leg = "".join(f'<span class="lg"><i style="background:{COLORS[p]}"></i>{esc(label(cfg, p))}</span>' for p in players)
    return f'<figure class="fig"><figcaption>{esc(title)}</figcaption>{"".join(out)}<div class="legend">{leg}</div></figure>'


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------

CSS = """
:root {
  --bg: #f3f5f8; --surface: #ffffff; --sunk: #e8ecf2; --line: #d3dae4;
  --fg: #16202e; --muted: #556275; --faint: #9aa4b2; --accent: #1d4ed8;
  --boeing: #1f5fbf; --airbus: #c2352b; --rolls_royce: #a16207; --pratt_whitney: #7c3aed; --cfm: #15803d;
  --good: #15803d; --bad: #b42318;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
  --radius: 6px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0d131c; --surface: #141c28; --sunk: #1b2533; --line: #2a3647;
  --fg: #e6ebf2; --muted: #a2adbd; --faint: #6b7688; --accent: #7aa7ff;
  --boeing: #6ea2f2; --airbus: #f07a70; --rolls_royce: #e0a93a; --pratt_whitney: #b394ff; --cfm: #4cc27a;
  --good: #4cc27a; --bad: #f07a70; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0d131c; --surface: #141c28; --sunk: #1b2533; --line: #2a3647;
  --fg: #e6ebf2; --muted: #a2adbd; --faint: #6b7688; --accent: #7aa7ff;
  --boeing: #6ea2f2; --airbus: #f07a70; --rolls_royce: #e0a93a; --pratt_whitney: #b394ff; --cfm: #4cc27a;
  --good: #4cc27a; --bad: #f07a70; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
.wrap { max-width: 1240px; margin: 0 auto; padding-inline: 16px; padding-block: 0 64px; }
h1, h2, h3, h4 { font-family: var(--font-display); font-weight: 600; letter-spacing: .01em; line-height: 1.1; margin: 0; text-wrap: balance; }
h1 { font-size: clamp(2.2rem, 5vw, 3.4rem); font-weight: 700; }
h2 { font-size: 1.9rem; } h3 { font-size: 1.35rem; } h4 { font-size: 1.1rem; }
p { margin: 0; max-width: 78ch; }
.eyebrow { font: 600 .74rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.muted { color: var(--muted); } .mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
.bar { position: sticky; top: 0; z-index: 10; background: var(--bg); border-bottom: 1px solid var(--line); }
.bar .wrap { display: flex; gap: 18px; align-items: center; padding-block: 10px; overflow-x: auto; }
.brand { font: 700 1.05rem/1 var(--font-display); letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; }
.bar nav { display: flex; gap: 14px; }
.bar nav a { font: 500 .82rem/1 var(--font-body); color: var(--muted); text-decoration: none; white-space: nowrap; }
.bar nav a:hover { color: var(--fg); }
section { padding-top: 44px; display: grid; gap: 16px; scroll-margin-top: 52px; }
.lede { font-size: 1.1rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 16px; display: grid; gap: 8px; align-content: start; min-width: 0; border-top: 4px solid var(--pc, var(--line)); }
.card .big { font: 700 1.9rem/1 var(--font-display); font-variant-numeric: tabular-nums; }
.card .role { font: 500 .72rem/1.3 var(--font-mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.card ul { margin: 0; padding-left: 18px; font-size: .86rem; }
.pos { color: var(--good); } .neg { color: var(--bad); }
.dot { display: inline-block; width: .7em; height: .7em; border-radius: 50%; background: var(--pc); margin-right: 6px; vertical-align: baseline; }
.scroll { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: .86rem; }
th, td { text-align: left; vertical-align: top; padding: 8px 11px; border-bottom: 1px solid var(--line); }
thead th { font: 600 .92rem/1.2 var(--font-display); letter-spacing: .03em; background: var(--sunk); white-space: nowrap; }
td.n, th.n { text-align: right; font-family: var(--font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
tbody tr:last-child td { border-bottom: 0; }
tbody td:first-child { white-space: nowrap; }
.grid2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 480px), 1fr)); gap: 14px; }
.fig { margin: 0; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 12px; min-width: 0; }
.fig figcaption { font: 600 1rem/1.2 var(--font-display); margin-bottom: 6px; }
.chart { width: 100%; height: auto; display: block; }
.chart .grid { stroke: var(--line); stroke-width: 1; } .chart .zero { stroke: var(--muted); stroke-width: 1; }
.chart .mark { stroke: var(--muted); stroke-dasharray: 2 3; }
.chart .tick { fill: var(--muted); font: 10px var(--font-mono); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: .78rem; color: var(--muted); margin-top: 4px; }
.lg i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }
.tabs { display: flex; gap: 6px; flex-wrap: wrap; }
.tabs button { font: 600 1rem/1 var(--font-display); letter-spacing: .03em; padding: 9px 14px; border-radius: var(--radius); border: 1px solid var(--line); background: var(--surface); color: var(--muted); cursor: pointer; }
.tabs button[aria-selected="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.round { display: none; gap: 16px; } .round.on { display: grid; }
.callout { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: var(--radius); padding: 12px 16px; display: grid; gap: 8px; }
.callout ul { margin: 0; padding-left: 18px; }
details { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 10px 14px; }
details > summary { cursor: pointer; font: 600 1.02rem/1.3 var(--font-display); }
details[open] > summary { margin-bottom: 8px; }
.quote { font-style: italic; color: var(--muted); }
.pill { display: inline-block; font: 500 .72rem/1 var(--font-mono); padding: 4px 7px; border-radius: 3px; background: var(--sunk); color: var(--muted); white-space: nowrap; }
.pill.yes { background: color-mix(in srgb, var(--good) 22%, transparent); color: var(--good); }
.pill.no { background: color-mix(in srgb, var(--bad) 20%, transparent); color: var(--bad); }
.small { font-size: .82rem; }
pre.rat { white-space: pre-wrap; font: .8rem/1.5 var(--font-mono); margin: 0; color: var(--muted); max-height: 420px; overflow: auto; }
@media (max-width: 600px) { th, td { padding: 7px 8px; } h2 { font-size: 1.6rem; } }
"""

JS = """
document.querySelectorAll('.tabs').forEach(function (tabs) {
  var btns = tabs.querySelectorAll('button');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.round').forEach(function (r) { r.classList.toggle('on', r.id === b.dataset.target); });
      try { localStorage.setItem('wg-round', b.dataset.target); } catch (e) {}
    });
  });
  var saved = null;
  try { saved = localStorage.getItem('wg-round'); } catch (e) {}
  var pick = saved && tabs.querySelector('[data-target="' + saved + '"]');
  if (pick) pick.click();
});
"""


def objectives_table(cfg, objs, only=None):
    rows = []
    for who, rs in objs.items():
        if only and who != only:
            continue
        for r in rs:
            met = r.get("met")
            pill = '<span class="pill">n/a</span>' if met is None else (f'<span class="pill {"yes" if met else "no"}">{"met" if met else "missed"}</span>')
            gap = f"{r['gap_pp']:+.1f}pp" if r.get("gap_pp") is not None else ""
            rows.append(f"<tr><td><span class=\"dot\" style=\"--pc:{COLORS.get(who, 'var(--faint)')}\"></span>{esc(label(cfg, who) if who in COLORS else who)}</td>"
                        f"<td>{esc(r['label'])}</td><td class=\"small\">{esc(E._fmt_obj_values(r))}</td><td class=\"n\">{gap}</td><td>{pill}</td></tr>")
    if not rows:
        return ""
    return ('<div class="scroll"><table><thead><tr><th>Player</th><th>Objective</th><th>Measured</th><th class="n">Gap</th><th>Status</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def build(run_id, narrative):
    st = E.load_state(run_id)
    cfg = st["config"]
    hist = st["history"]
    reps = E.round_reports(st)
    final = E.final_report(st)
    world = M.build_world(cfg, hist)
    ev = M.evaluate(cfg, world, with_series=True)
    sc = S.turn_scorecard(cfg, hist) if hist else {"rows": [], "summary": {}}
    pls = list(M.players(cfg))
    sups = list(M.active_suppliers(cfg))
    y0, y1 = cfg["years"]["start"], cfg["years"]["end"]
    years = list(range(y0, y1 + 1))
    round_ends = [(r["as_of"], f"R{r['round']}") for r in reps]
    nv = narrative or {}
    title = nv.get("title") or f"War game {run_id}"
    P = []
    P.append(f'<header class="bar"><div class="wrap"><span class="brand">{esc(title)}</span><nav>'
             '<a href="#summary">Summary</a><a href="#rounds">Rounds</a><a href="#players">Players</a>'
             '<a href="#dates">Dates</a><a href="#method">Method</a></nav></div></header>')
    P.append('<main class="wrap">')
    turns_txt = ", ".join(f"{t['years'][0]}–{t['years'][1]}" for t in cfg["turns"][:st["turns_total"]])
    P.append(f'<section id="top" style="padding-top:28px"><span class="eyebrow">War game · {esc(cfg["scenario"]["id"])} · '
             f'{len(hist)} of {st["turns_total"]} rounds played · status {esc(st["status"])}</span><h1>{esc(title)}</h1>'
             f'<p class="lede">{esc(nv.get("lede") or cfg["scenario"]["narrative"])}</p>'
             f'<p class="muted small">Players: {", ".join(esc(label(cfg, p)) for p in pls)}. Rounds: {esc(turns_txt)}. '
             f'Money: $B; delta PV is each player\'s full-game present value (to {cfg["years"]["pv_base"]}, at its own WACC) versus the status quo in which nobody moves.</p></section>')

    # Summary
    P.append('<section id="summary"><span class="eyebrow">Summary</span><h2>How the fight ended</h2>')
    if nv.get("summary"):
        P.append("".join(f"<p>{esc(x)}</p>" for x in nv["summary"]))
    if nv.get("findings"):
        P.append('<div class="callout"><h4>Key findings</h4><ul>' + "".join(f"<li>{esc(x)}</li>" for x in nv["findings"]) + "</ul></div>")
    cards = []
    lead = nv.get("leadership", {})
    for p in pls:
        f = ev[p]
        objs = ev.get("objectives", {}).get(p, [])
        met = sum(1 for r in objs if r.get("met"))
        moves = [f"R{r['round']}: {r['orders'].get(p, 'no new moves')}" for r in reps]
        cards.append(f'<div class="card" style="--pc:{COLORS[p]}"><span class="role">{esc(label(cfg, p))}'
                     f'{" · " + esc(lead[p]) if lead.get(p) else ""}</span>'
                     f'<span class="big {"pos" if f["delta_pv_b"] >= 0 else "neg"}">{fmt_b(f["delta_pv_b"])}</span>'
                     f'<span class="muted small">delta PV $B · objectives met {met}/{len(objs)}</span>'
                     f'<ul>{"".join(f"<li>{esc(m)}</li>" for m in moves)}</ul></div>')
    P.append(f'<div class="cards">{"".join(cards)}</div>')

    # charts
    def path(seg, side, key="aircraft"):
        out = []
        for y in years:
            row_b, row_a = ev["boeing"]["series"][str(y)], ev["airbus"]["series"][str(y)]
            tot = row_b[f"{seg}_{key}"] + row_a[f"{seg}_{key}"]
            out.append((y, (row_b if side == "boeing" else row_a)[f"{seg}_{key}"] / tot if tot else 0))
        return out
    charts = []
    for seg, nm in (("nb", "Narrowbody"), ("wb", "Widebody")):
        charts.append(line_chart([("Boeing", COLORS["boeing"], path(seg, "boeing")), ("Airbus", COLORS["airbus"], path(seg, "airbus")),
                                  ("Boeing, status quo", COLORS["boeing"], path(seg, "boeing", "aircraft_sq"))],
                                 y0, y1, 0.0, 1.0, f"{nm} deliveries: airframer share", dashed=("Boeing, status quo",), marks=round_ends))
    if sups:
        for seg, nm in (("nb", "Narrowbody"), ("wb", "Widebody")):
            layers = []
            tot = [sum(ev[s]["series"][str(y)][f"{seg}_aircraft"] for s in M.SIDES) * 2 for y in years]
            acc = [0.0] * len(years)
            for sup in sups:
                ys = [ev[sup]["series"][str(y)][f"{seg}_engines"] / t if t else 0 for y, t in zip(years, tot)]
                acc = [a + b for a, b in zip(acc, ys)]
                layers.append((label(cfg, sup), COLORS[sup], ys))
            layers.append(("Other makers", COLORS["other_makers"], [max(0.0, 1 - a) for a in acc]))
            charts.append(stacked_chart(layers, years, f"{nm} engines delivered: share by engine maker", marks=round_ends))
    P.append(f'<div class="grid2">{"".join(charts)}</div>')
    groups = [f"after R{r['round']} ({r['as_of']})" for r in reps]
    vals = {(g, p): r["financials"][p]["delta_pv_b"] for g, r in zip(groups, reps) for p in pls}
    P.append('<div class="grid2">' + bar_chart(groups, pls, vals, "Projected full-game delta PV after each round ($B)", cfg))
    # scoreboard table
    rows = []
    for p in pls:
        comp = ev[p]["components_pv_b"]
        rows.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p]}"></span>{esc(label(cfg, p))}</td><td class="n">{fmt_b(ev[p]["delta_pv_b"])}</td>'
                    f'<td class="small">{esc(comp_text(comp))}</td></tr>')
    P.append('<div class="scroll"><table><thead><tr><th>Player</th><th class="n">Delta PV $B</th><th>Components (PV $B)</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div></div>')
    if ev.get("objectives"):
        P.append("<h3>Assigned objectives at the end</h3>" + objectives_table(cfg, ev["objectives"]))
    P.append("</section>")

    # Rounds
    P.append('<section id="rounds"><span class="eyebrow">Round by round</span><h2>Rounds, as of each round\'s last year</h2>'
             '<p class="muted small">Shares and dates up to the round\'s last year are what happened; later years are the projection at that point, '
             'assuming nobody moves again. Window figures are undiscounted sums over the round\'s years.</p>')
    P.append('<div class="tabs" role="tablist">' + "".join(
        f'<button role="tab" data-target="round{r["round"]}" aria-selected="{"true" if i == 0 else "false"}">'
        f'Round {r["round"]} · {r["as_of"]}</button>' for i, r in enumerate(reps)) + "</div>")
    for i, r in enumerate(reps):
        P.append(f'<div class="round{" on" if i == 0 else ""}" id="round{r["round"]}">')
        P.append(f'<h3>{esc(r["label"])} <span class="muted">({r["years"][0]}–{r["years"][1]})</span></h3>')
        if nv.get("rounds", {}).get(str(r["round"])):
            P.append(f'<div class="callout"><p>{esc(nv["rounds"][str(r["round"])])}</p></div>')
        if r["injects"]:
            P.append(f'<p><strong>Inject:</strong> {esc(", ".join(r["injects"]))}</p>')
        # moves
        mv = []
        for p in pls:
            stt = r["statements"].get(p, {})
            disc = stt.get("disclose") or []
            mv.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p]}"></span>{esc(label(cfg, p))}</td><td>{esc(r["orders"].get(p, "no new moves"))}</td>'
                      f'<td class="small"><span class="quote">{esc(stt.get("public_statement", ""))}</span>'
                      f'{"<br><strong>Disclosed:</strong> " + esc(" · ".join(disc)) if disc else ""}</td></tr>')
        P.append('<h4>Moves</h4><div class="scroll"><table><thead><tr><th>Player</th><th>Orders</th><th>Public statement and disclosures</th></tr></thead>'
                 f'<tbody>{"".join(mv)}</tbody></table></div>')
        if r.get("market_narrative"):
            mm = r.get("market", {}).get("capture_mult") or {}
            P.append(f'<p class="small"><strong>Market:</strong> {esc(r["market_narrative"])}'
                     + (f' <span class="muted">Capture multipliers: {esc(", ".join(f"{k} ×{v:.2f}" for k, v in mm.items()))}</span>' if mm else "") + "</p>")
        # shares
        sh_rows = []
        for seg in M.SEGMENTS:
            for y, v in r["shares"][seg].items():
                em = v.get("engine_makers", {})
                sh_rows.append(f'<tr><td>{seg.upper()}</td><td class="n">{y}{" *" if int(y) > r["as_of"] else ""}</td><td class="n">{pct(v["boeing"])}</td>'
                               f'<td class="n">{pct(v["airbus"])}</td><td class="n muted">{pct(v["status_quo_boeing"])}</td>'
                               + "".join(f'<td class="n">{pct(em.get(s))}</td>' for s in sups) + f'<td class="n">{v["aircraft_per_year"]:,.0f}</td></tr>')
        P.append('<h4>Market shares</h4><div class="scroll"><table><thead><tr><th>Segment</th><th class="n">Year</th><th class="n">Boeing</th>'
                 '<th class="n">Airbus</th><th class="n">Boeing status quo</th>'
                 + "".join(f'<th class="n">{esc(label(cfg, s))} engines</th>' for s in sups)
                 + f'<th class="n">Aircraft / yr</th></tr></thead><tbody>{"".join(sh_rows)}</tbody></table></div>'
                 '<p class="muted small">* projection as of this round.</p>')
        # programmes
        pr = []
        for p in r["programs"]:
            pr.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p["owner"]]}"></span>{esc(label(cfg, p["owner"]))}</td><td>{esc(p["label"])}'
                      f'{" (" + esc(p["variant"]) + ")" if p.get("variant") else ""}{", " + esc(p["ramp"]) + " ramp-up" if p.get("ramp") else ""}</td>'
                      f'<td class="n">{p["launch_year"]}</td><td class="n">{p["eis"] or "cancelled " + str(p["cancelled_year"])}</td>'
                      f'<td>{esc(p["engine_label"])}{" (asked for " + esc(p["engine_requested"]) + ")" if p.get("engine_requested") else ""}</td><td>{esc(p["status"])}</td></tr>')
        for sp in r.get("supplier_programs", []):
            pr.append(f'<tr><td><span class="dot" style="--pc:{COLORS[sp["supplier"]]}"></span>{esc(label(cfg, sp["supplier"]))}'
                      f'{" + " + esc(label(cfg, sp["joint_venture_partner"])) if sp.get("joint_venture_partner") else ""}</td>'
                      f'<td>{esc(sp["label"])} ({esc(sp["terms"])} terms)</td><td class="n">{sp["launch_year"]}</td>'
                      f'<td class="n">{sp["ready"] or "cancelled"}</td><td>engine ready; flown by {esc(", ".join(sp["selected_by"]) or "none yet")}</td><td></td></tr>')
        com = [f'{label(cfg, s)}: {c["label"]} ({c["year"]})' for s, cs in r.get("supplier_commitments", {}).items() for c in cs.values() if c["year"]]
        P.append('<h4>Programmes and dates</h4><div class="scroll"><table><thead><tr><th>Owner</th><th>Programme</th><th class="n">Launch</th>'
                 f'<th class="n">EIS / ready</th><th>Engine</th><th>Status at {r["as_of"]}</th></tr></thead><tbody>{"".join(pr) or "<tr><td colspan=6 class=muted>No programmes launched yet</td></tr>"}</tbody></table></div>'
                 + (f'<p class="small"><strong>One-time commitments so far:</strong> {esc("; ".join(com))}</p>' if com else ""))
        # financials
        fr = []
        for p in pls:
            f = r["financials"][p]
            w_ = f["round_window"]
            ch = f["change_in_delta_pv_this_round_b"]
            if p in M.SIDES:
                sq = f["round_window_status_quo"]
                fr.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p]}"></span>{esc(label(cfg, p))}</td><td class="n">{fmt_b(f["delta_pv_b"])}</td>'
                          f'<td class="n">{fmt_b(ch) if ch is not None else "–"}</td><td class="n">{w_["revenue_b"]:,.0f}</td><td class="n muted">{sq["revenue_b"]:,.0f}</td>'
                          f'<td class="n">{w_["op_profit_b"]:,.1f}</td><td class="n muted">{sq["op_profit_b"]:,.1f}</td><td class="n">{w_["capex_b"]:,.1f}</td>'
                          f'<td class="n">{w_["strain_b"] + w_["tactics_b"]:,.1f}</td><td class="n">–</td></tr>')
            else:
                sq = f["round_window_status_quo"]
                eng = w_["nb_engines"] + w_["wb_engines"] + w_["partner_engines"]
                fr.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p]}"></span>{esc(label(cfg, p))}</td><td class="n">{fmt_b(f["delta_pv_b"])}</td>'
                          f'<td class="n">{fmt_b(ch) if ch is not None else "–"}</td><td class="n">{w_["engine_value_b"]:,.1f}</td><td class="n muted">{sq["engine_value_b"]:,.1f}</td>'
                          f'<td class="n">–</td><td class="n muted">–</td><td class="n">{w_["capex_b"]:,.1f}</td><td class="n">{w_["strain_b"] + w_["lobby_b"]:,.1f}</td>'
                          f'<td class="n">{eng:,.0f} <span class="muted">(sq {sq["engines"]:,.0f})</span></td></tr>')
        P.append('<h4>Financials</h4><div class="scroll"><table><thead><tr><th>Player</th><th class="n">Delta PV (full game)</th><th class="n">Change this round</th>'
                 '<th class="n">Revenue / engine value in round</th><th class="n">… status quo</th><th class="n">Op. profit in round</th><th class="n">… status quo</th>'
                 '<th class="n">Capex in round</th><th class="n">Strain, tactics, lobbying</th><th class="n">Engines in round</th></tr></thead>'
                 f'<tbody>{"".join(fr)}</tbody></table></div>'
                 '<p class="muted small">Airframers: revenue is deliveries × net price; operating profit uses each product\'s margin. Engine makers: engine value is the lifecycle value '
                 '(OE margin plus PV of aftermarket profit) booked at delivery. Capex is before the alpha loading used in the payoff.</p>')
        if r.get("objectives"):
            P.append(f"<h4>Assigned objectives on the projection after round {r['round']}</h4>" + objectives_table(cfg, r["objectives"]))
        evs = [e for e in r["events"]]
        if evs:
            P.append("<details><summary>Adjudication log</summary><ul class=\"small\">" + "".join(
                f'<li>{esc(e["text"])}{" <span class=pill>private: " + esc(str(e.get("side"))) + "</span>" if e.get("visibility") == "private" else ""}</li>'
                for e in evs) + "</ul></details>")
        P.append("</div>")
    P.append("</section>")

    # Players
    P.append('<section id="players"><span class="eyebrow">Players</span><h2>Each player in detail</h2>')
    summ = sc.get("summary", {})
    for p in pls:
        pv = nv.get("players", {}).get(p, {})
        f = ev[p]
        P.append(f'<details{" open" if p == pls[0] else ""} style="border-top:4px solid {COLORS[p]}"><summary>{esc(label(cfg, p))}: delta PV {fmt_b(f["delta_pv_b"])} $B'
                 f'{" · team " + esc(lead[p]) if lead.get(p) else ""}</summary><div style="display:grid;gap:12px">')
        if pv.get("verdict"):
            P.append(f"<p>{esc(pv['verdict'])}</p>")
        if pv.get("highlights"):
            P.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in pv["highlights"]) + "</ul>")
        s_ = summ.get(p, {})
        if s_:
            P.append('<p class="small muted">Referee scorecard: mean value capture '
                     f'{"–" if s_.get("mean_capture") is None else format(s_["mean_capture"], ".0%")}, total myopic regret {s_.get("total_myopic_regret_b", 0):.2f} $B, '
                     f'prediction accuracy {"–" if s_.get("mean_prediction_accuracy") is None else format(s_["mean_prediction_accuracy"], ".0%")}, '
                     f'mean expectation error {"–" if s_.get("mean_abs_expectation_error_b") is None else format(s_["mean_abs_expectation_error_b"], ".2f")} $B.</p>')
        rows = []
        for r in reps:
            fr_ = r["financials"][p]
            rows.append(f'<tr><td>R{r["round"]} ({r["years"][0]}–{r["years"][1]})</td><td>{esc(r["orders"].get(p, "no new moves"))}</td>'
                        f'<td class="n">{fmt_b(fr_["delta_pv_b"])}</td><td class="small quote">{esc(r["statements"].get(p, {}).get("public_statement", ""))}</td></tr>')
        P.append('<div class="scroll"><table><thead><tr><th>Round</th><th>Orders</th><th class="n">Delta PV after</th><th>Public statement</th></tr></thead>'
                 f'<tbody>{"".join(rows)}</tbody></table></div>')
        P.append('<div class="scroll"><table><thead><tr><th>Component</th><th class="n">PV $B</th><th class="n">Undiscounted $B</th></tr></thead><tbody>'
                 + "".join(f'<tr><td>{esc(k.replace("_", " "))}</td><td class="n">{v:+,.2f}</td><td class="n">{f["undiscounted_b"].get(k, 0):+,.1f}</td></tr>'
                           for k, v in f["components_pv_b"].items()) + "</tbody></table></div>")
        if ev.get("objectives", {}).get(p):
            P.append(objectives_table(cfg, ev["objectives"], only=p))
        for r in reps:
            stt = r["statements"].get(p, {})
            if stt.get("rationale"):
                exp = stt.get("expected_delta_pv_b")
                P.append(f'<details><summary>Round {r["round"]} private rationale{f" · expected delta PV {exp:+.2f} $B" if isinstance(exp, (int, float)) else ""}</summary>'
                         f'<pre class="rat">{esc(stt["rationale"])}</pre>'
                         + (f'<p class="small muted">Prediction: {esc(json.dumps(stt["prediction"]))}</p>' if stt.get("prediction") else "") + "</details>")
        P.append("</div></details>")
    P.append("</section>")

    # Dates
    drows = []
    for p in M.SIDES:
        for pr_ in ev[p]["programs"]:
            drows.append(f'<tr><td><span class="dot" style="--pc:{COLORS[p]}"></span>{esc(label(cfg, p))}</td><td>{esc(pr_["label"])}</td><td class="n">{pr_["launch_year"]}</td>'
                         f'<td class="n">{pr_["planned_eis_at_launch"]}</td><td class="n">{pr_["eis"] or "cancelled"}</td><td>{esc(pr_["engine_label"])}</td>'
                         f'<td class="small">{esc(slips_text(pr_["slips"]))}</td></tr>')
    for sp in final.get("supplier_programs", []):
        drows.append(f'<tr><td><span class="dot" style="--pc:{COLORS[sp["supplier"]]}"></span>{esc(label(cfg, sp["supplier"]))}</td><td>{esc(sp["label"])}</td>'
                     f'<td class="n">{sp["launch_year"]}</td><td class="n">–</td><td class="n">{sp["ready"] or "cancelled"}</td><td>{esc(sp["terms"])} terms</td>'
                     f'<td class="small">{esc(slips_text(sp["slips"]))}</td></tr>')
    P.append('<section id="dates"><span class="eyebrow">Dates</span><h2>Launches and entries into service</h2><div class="scroll"><table><thead><tr><th>Owner</th>'
             '<th>Programme</th><th class="n">Launch</th><th class="n">Planned EIS at launch</th><th class="n">EIS / ready</th><th>Engine / terms</th><th>Slips</th></tr></thead>'
             f'<tbody>{"".join(drows) or "<tr><td colspan=7 class=muted>none</td></tr>"}</tbody></table></div></section>')

    # Method
    cav = nv.get("caveats") or []
    P.append('<section id="method"><span class="eyebrow">Method</span><h2>How this was played and scored</h2><div class="callout"><ul>'
             '<li>Each player is an independent agent that reads only its own company and executive profiles and its own engine view; a runtime hook enforces this. '
             'The game master alone sees the full game-theory board and relays only public moves, statements and chosen disclosures.</li>'
             '<li>Orders are sealed and simultaneous each round. Engine makers\' orders apply first, so an airframer can pick an engine its maker commits to in the same round.</li>'
             '<li>Every number is computed by the war-game engine (wargame/model.py). Volumes are stylised (2,000 narrowbodies and 170 widebodies a year); '
             'per-unit values are calibrated from the evidence, and parameters marked PLACEHOLDER in the config are assumptions.</li>'
             + "".join(f"<li>{esc(c)}</li>" for c in cav) + "</ul></div></section>")
    P.append("</main>")
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{esc(nv.get('short_title') or 'War Game Report')}</title>"
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
            f"<style>{CSS}</style></head><body>{''.join(P)}<script>{JS}</script></body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("out")
    ap.add_argument("--narrative")
    a = ap.parse_args()
    nv = json.load(open(a.narrative)) if a.narrative else None
    page = build(a.run, nv)
    with open(a.out, "w") as f:
        f.write(page)
    print(a.out, len(page))


if __name__ == "__main__":
    main()
