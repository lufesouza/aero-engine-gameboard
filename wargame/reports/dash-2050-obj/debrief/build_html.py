"""Boeing management debrief (dash-2050-obj): the same 8-slide storyline as the PPTX, as one HTML page of slide
cards (Boeing PD colours, BCG layout: action title, evidence, takeaway, source; speaker notes folded under each slide).
Charts are inline SVG drawn from factpack.json by dataset id, with hover tooltips and a table view.

Usage: python3 build_html.py storyline.json factpack.json <out.html>
"""
import html
import json
import sys

esc = html.escape
MINUS = "−"
COL = {"Boeing": ("--bb", False), "Airbus": ("--fl", False), "Game": ("--bb", False), "Status quo": ("--gm", True),
       "CFM/GE": ("--sp", False), "P&W (Joint Venture)": ("--bb", False), "Rolls-Royce (Joint Venture)": ("--fl", True),
       "fps programme cash": ("--sp", False), "Free cash flow, base": ("--bb", False), "Free cash flow, stress": ("--lo", False),
       "Base case": ("--bb", False), "Stress case": ("--lo", False), "No new programme": ("--gm", True),
       "fps 10-year (played)": ("--bb", False), "Do Nothing (no fps)": ("--lo", False), "No game (analysts' path)": ("--gm", True)}
FALLBACK = [("--bb", False), ("--fl", False), ("--sp", False)]


def tipattr(rows):
    return esc(json.dumps([{"v": v, "l": l, "k": k} for v, l, k in rows]), quote=True)


def line_svg(v, FP):
    ds = FP["datasets"][v["dataset"]]
    yrs = ds["years"]
    lo_y, hi_y = (v.get("years") or [yrs[0], yrs[-1]])[:2]
    idx = [i for i, y in enumerate(yrs) if lo_y <= y <= hi_y]
    names = [n for n in (v.get("series") or list(ds["series"])) if n in ds["series"]]
    share = ds["unit"] == "share"
    k = 100 if share else 1
    vals = [ds["series"][n][i] * k for n in names for i in idx]
    if share:
        y_lo, y_hi, step = 0, (100 if max(vals) > 80 else 80), 20
    else:
        top = max(vals)
        step = 5 if top <= 30 else (50 if top <= 300 else 100)
        y_lo, y_hi = min(0, min(vals)), step * (int(top / step) + 1)
    w, h, left, right, top_, bot = 720, 330, 50, 150, 18, 40
    xs = [yrs[i] for i in idx]
    sx = lambda x: left + (x - xs[0]) / max(1, xs[-1] - xs[0]) * (w - left - right)
    sy = lambda val: top_ + (y_hi - val) / (y_hi - y_lo) * (h - top_ - bot)
    fmt = (lambda x: f"{x:.0f}%") if share else (lambda x: f"{x:,.0f}")
    out = [f'<svg viewBox="0 0 {w} {h}" class="ch" role="img" aria-label="{esc(ds["title"], quote=True)}">']
    t = y_lo
    while t <= y_hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{fmt(t)}</text>')
        t += step
    span = xs[-1] - xs[0]
    tstep = 5 if span > 15 else (2 if span > 8 else 1)
    for yr in xs:
        if yr % tstep == 0:
            out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    ends = []
    for j, n in enumerate(names):
        var, dash = COL.get(n, FALLBACK[j % 3])
        pts = " L".join(f"{sx(yrs[i]):.1f},{sy(ds['series'][n][i] * k):.1f}" for i in idx)
        dash_attr = ' stroke-dasharray="6 4"' if dash else ""
        out.append(f'<path d="M{pts}" fill="none" stroke="var({var})" stroke-width="2.5" stroke-linejoin="round"{dash_attr}/>')
        ends.append((n, ds["series"][n][idx[-1]] * k, var))
    # end labels, spread
    order = sorted(range(len(ends)), key=lambda i: -ends[i][1])
    placed, last = {}, None
    for i in order:
        y = sy(ends[i][1])
        y = y if last is None else max(y, last + 16)
        placed[i] = y
        last = y
    for i, (n, val, var) in enumerate(ends):
        short = n.split(" (")[0]
        out.append(f'<text x="{w - right + 8}" y="{placed[i] + 4:.1f}" class="endlab">{esc(short)} {fmt(val) if share else f"{val:.1f}"}</text>')
    for a in v.get("annotations") or []:
        yr = a["year"]
        if yr not in xs or not names:
            continue
        val = ds["series"][names[0]][yrs.index(yr)] * k
        out.append(f'<circle cx="{sx(yr):.1f}" cy="{sy(val):.1f}" r="5" fill="var({COL.get(names[0], FALLBACK[0])[0]})" stroke="#fff" stroke-width="2"/>'
                   f'<text x="{sx(yr):.1f}" y="{sy(val) - 12:.1f}" text-anchor="middle" class="ann">{esc(a["text"])}</text>')
    # hover columns
    step_px = (w - left - right) / max(1, len(xs) - 1)
    for i in idx:
        yr = yrs[i]
        rows = [(str(yr), "", None)] + [((f"{ds['series'][n][i] * 100:.1f}%" if share else f"{ds['series'][n][i]:.2f} $B"), n,
                                          f"var({COL.get(n, FALLBACK[j % 3])[0]})") for j, n in enumerate(names)]
        out.append(f'<rect x="{sx(yr) - step_px / 2:.1f}" y="{top_}" width="{step_px:.1f}" height="{h - top_ - bot}" fill="transparent" '
                   f'class="hit" tabindex="0" data-tip="{tipattr(rows)}" aria-label="{esc("; ".join(f"{l} {v_}" for v_, l, _ in rows), quote=True)}"/>')
    out.append("</svg>")
    unit = "% of deliveries" if share else ("$B, 2026 dollars" if v["dataset"] in ("boeing_cash", "net_debt", "owners_cash") else "$B a year, 2026 prices")
    legend = "".join(f'<span><i style="background:var({COL.get(n, FALLBACK[j % 3])[0]})"></i>{esc(n)}</span>' for j, n in enumerate(names))
    table = ("<details class='tv'><summary>Table view</summary><div class='scroll'><table><thead><tr><th>Year</th>"
             + "".join(f"<th>{esc(n)}</th>" for n in names) + "</tr></thead><tbody>"
             + "".join("<tr><th>" + str(yrs[i]) + "</th>" + "".join(
                 f"<td>{(ds['series'][n][i] * 100):.1f}%</td>" if share else f"<td>{ds['series'][n][i]:.2f}</td>" for n in names) + "</tr>" for i in idx)
             + "</tbody></table></div></details>")
    return f'<div class="legend">{legend}</div><div class="cw">{"".join(out)}</div><p class="unit">{unit}</p>{table}'


def bridge_svg(FP):
    items = FP["datasets"]["pv_bridge"]["items"]
    w, h, left, right, top, bot = 720, 300, 50, 20, 20, 60
    n = len(items)
    hi = 25
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    bw = (w - left - right) / n * 0.6
    out = [f'<svg viewBox="0 0 {w} {h}" class="ch" role="img" aria-label="Boeing value bridge, present value at 2026">']
    for t in range(0, hi + 1, 5):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t}</text>')
    run = 0.0
    for i, (lab, d) in enumerate(items):
        cx = left + (i + 0.5) * (w - left - right) / n
        last = i == n - 1
        if last:
            y0, y1 = 0, d
        elif d >= 0:
            y0, y1 = run, run + d
            run += d
        else:
            y0, y1 = run + d, run
            run += d
        var = "--sp" if last else ("--bb" if d >= 0 else "--gm")
        top_px, bot_px = sy(max(y0, y1)), sy(min(y0, y1))
        val = f"{d:+.2f}".replace("-", MINUS)
        out.append(f'<rect x="{cx - bw / 2:.1f}" y="{top_px:.1f}" width="{bw:.1f}" height="{max(2, bot_px - top_px):.1f}" rx="3" fill="var({var})" '
                   f'tabindex="0" class="hit" data-tip="{tipattr([(val + " $B", lab, None)])}" aria-label="{esc(lab + " " + val, quote=True)}"/>'
                   f'<text x="{cx:.1f}" y="{top_px - 6:.1f}" text-anchor="middle" class="val">{val}</text>'
                   f'<text x="{cx:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick wrap">{esc(lab.split(" (")[0])}</text>')
    out.append("</svg>")
    return f'<div class="cw">{"".join(out)}</div><p class="unit">$B, present value at 2026</p>'


def visual(v, FP):
    t = v["type"]
    if t == "line":
        return line_svg(v, FP)
    if t == "bridge":
        return bridge_svg(FP)
    if t == "stats":
        return '<div class="stats">' + "".join(f'<div class="stat"><div class="sv">{esc(s["value"])}</div><div class="sl">{esc(s["label"])}</div></div>'
                                               for s in v["stats"]) + "</div>"
    if t == "table":
        tb = v["table"]
        return ("<div class='scroll'><table class='dt'><thead><tr>" + "".join(f"<th>{esc(c)}</th>" for c in tb["columns"]) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join((f"<th>{esc(str(c))}</th>" if j == 0 else f"<td>{esc(str(c))}</td>") for j, c in enumerate(r)) + "</tr>"
                          for r in tb["rows"]) + "</tbody></table></div>")
    if t == "recs":
        return '<ol class="recs">' + "".join(f'<li><b>{esc(r["recommendation"])}</b><span><em>Why:</em> {esc(r["why"])}</span>'
                                             f'<span><em>Proof:</em> {esc(r["proof"])}</span></li>' for r in v["recs"]) + "</ol>"
    if t == "risks":
        return ("<div class='scroll'><table class='dt risks'><thead><tr><th>Risk</th><th>Trigger</th><th>Cost</th><th>Mitigation</th></tr></thead><tbody>"
                + "".join(f"<tr><th>{esc(r['risk'])}</th><td>{esc(r['trigger'])}</td><td>{esc(r['cost'])}</td><td>{esc(r['mitigation'])}</td></tr>"
                          for r in v["risks"]) + "</tbody></table></div>")
    if t == "columns":
        return '<div class="cols">' + "".join(f'<div class="col"><div class="ch2">{esc(c["header"])}</div><ul>' + "".join(f"<li>{esc(b)}</li>" for b in c["bullets"])
                                              + "</ul></div>" for c in v["columns"]) + "</div>"
    return ""


CSS = """
:root { --bb: #0033A1; --fl: #009BDF; --sp: #0A2240; --lo: #F37121; --gm: #9AA3AD; --ink: #1F2937; --muted: #5b6572; --line: #C8CED6;
  --tint: #E8EEF7; --page: #eef1f5; --card: #ffffff; color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--ink); font: 16px/1.5 "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
.wrap { max-width: 1180px; margin: 0 auto; padding: 24px 16px 60px; }
.hd { color: var(--sp); margin: 6px 0 18px; } .hd h1 { font-size: 1.9rem; margin: 0 0 6px; line-height: 1.2; }
.hd p { margin: 0; color: var(--muted); }
.slide { background: var(--card); border: 1px solid var(--line); border-radius: 8px; margin: 0 0 26px; overflow: hidden; box-shadow: 0 1px 2px rgba(10,34,64,.06); }
.bar { background: var(--bb); color: #fff; display: flex; justify-content: space-between; align-items: center; padding: 10px 22px; font-weight: 700; font-size: 1rem; }
.bar .pn { font-weight: 400; opacity: .85; font-size: .85rem; }
.at { color: var(--sp); font-size: 1.55rem; font-weight: 700; line-height: 1.25; margin: 18px 22px 14px; text-wrap: balance; }
.body { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 20px; padding: 0 22px; }
.body.full { grid-template-columns: minmax(0, 1fr); }
.body.full.side { grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); }
.ev ul { margin: 0; padding-left: 20px; } .ev li { margin: 0 0 10px; }
.ev li::marker { color: var(--bb); }
.ev { border-left: 3px solid var(--line); padding-left: 16px; }
.take { background: var(--bb); color: #fff; margin: 16px 22px 0; padding: 12px 18px; border-radius: 4px; font-size: 1.05rem; }
.take b { font-size: .8rem; letter-spacing: .08em; margin-right: 10px; }
.src { color: var(--muted); font-style: italic; font-size: .8rem; margin: 10px 22px 6px; }
.foot { display: flex; justify-content: space-between; font-size: .72rem; color: var(--muted); padding: 6px 22px 12px; border-top: 1px solid var(--tint); }
details.notes { margin: 0 22px 14px; font-size: .9rem; } details.notes summary { cursor: pointer; color: var(--bb); font-weight: 600; }
details.notes p { white-space: pre-line; margin: 8px 0 0; }
.cw { overflow-x: auto; } svg.ch { width: 100%; height: auto; min-width: 520px; display: block; }
svg .grid { stroke: var(--line); stroke-width: 1; } svg .tick { fill: var(--muted); font-size: 12px; }
svg .endlab { fill: var(--ink); font-size: 13px; font-weight: 600; } svg .ann { fill: var(--sp); font-size: 12px; font-weight: 700; }
svg .val { fill: var(--sp); font-size: 14px; font-weight: 700; } svg .hit { cursor: crosshair; } svg .hit:focus { outline: none; stroke: var(--sp); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: .85rem; color: var(--muted); margin-bottom: 4px; }
.legend i { display: inline-block; width: 16px; height: 3px; border-radius: 2px; vertical-align: middle; margin-right: 6px; }
.unit { color: var(--muted); font-size: .78rem; font-style: italic; margin: 2px 0 0; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
.stat { background: var(--tint); border-left: 5px solid var(--bb); padding: 14px 16px; border-radius: 4px; }
.sv { font-size: 2.1rem; font-weight: 800; color: var(--bb); line-height: 1.1; } .sl { margin-top: 6px; }
table { border-collapse: collapse; width: 100%; font-size: .92rem; } .scroll { overflow-x: auto; }
table.dt th, table.dt td { padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
table.dt thead th { background: var(--sp); color: #fff; font-size: .82rem; }
table.dt tbody tr:nth-child(odd) { background: var(--tint); }
details.tv { margin-top: 6px; font-size: .85rem; } details.tv summary { cursor: pointer; color: var(--bb); }
details.tv th, details.tv td { padding: 3px 8px; border-bottom: 1px solid var(--tint); text-align: right; } details.tv th:first-child { text-align: left; }
ol.recs { margin: 0; padding: 0; list-style: none; counter-reset: r; }
ol.recs li { counter-increment: r; position: relative; padding: 0 0 14px 48px; display: flex; flex-direction: column; gap: 3px; }
ol.recs li::before { content: counter(r); position: absolute; left: 0; top: 0; width: 34px; height: 34px; border-radius: 50%; background: var(--bb); color: #fff; font-weight: 700; display: grid; place-items: center; }
ol.recs b { color: var(--sp); font-size: 1.05rem; } ol.recs em { color: var(--bb); font-style: normal; font-weight: 700; }
.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.col { background: var(--tint); border-radius: 4px; overflow: hidden; } .ch2 { background: var(--bb); color: #fff; font-weight: 700; padding: 8px 14px; }
.col:nth-child(n+2) .ch2 { background: var(--sp); } .col ul { margin: 10px 0; padding: 0 14px 0 32px; } .col li { margin-bottom: 8px; }
.cover { background: var(--bb); color: #fff; border-radius: 8px; padding: 46px 30px; margin-bottom: 26px; }
.cover h2 { font-size: 2.2rem; margin: 0 0 12px; line-height: 1.15; } .cover p { margin: 0 0 6px; font-size: 1.15rem; opacity: .95; }
.tip { position: fixed; pointer-events: none; background: #0A2240; color: #fff; font-size: 13px; padding: 7px 10px; border-radius: 6px; z-index: 9; display: none; max-width: 280px; }
.tip i { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 6px; }
@media (max-width: 820px) { .body, .body.full.side { grid-template-columns: minmax(0, 1fr); } .at { font-size: 1.3rem; } .ev { border-left: 0; padding-left: 0; } }
"""

JS = """
(() => { const tip = document.createElement('div'); tip.className = 'tip'; document.body.appendChild(tip);
  const show = (el, x, y) => { const rows = JSON.parse(el.dataset.tip); tip.innerHTML = '';
    rows.forEach(r => { const d = document.createElement('div'); if (r.k) { const i = document.createElement('i'); i.style.background = r.k; d.appendChild(i); }
      d.appendChild(document.createTextNode(r.l ? (r.v + '  ' + r.l) : r.v)); tip.appendChild(d); });
    tip.style.display = 'block'; const b = tip.getBoundingClientRect();
    tip.style.left = Math.min(innerWidth - b.width - 8, x + 14) + 'px'; tip.style.top = Math.min(innerHeight - b.height - 8, y + 14) + 'px'; };
  document.querySelectorAll('[data-tip]').forEach(el => {
    el.addEventListener('mousemove', e => show(el, e.clientX, e.clientY)); el.addEventListener('mouseleave', () => tip.style.display = 'none');
    el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); show(el, r.left, r.top); }); el.addEventListener('blur', () => tip.style.display = 'none'); });
})();
"""


def main():
    story_p, fp_p, out = sys.argv[1:4]
    S = json.load(open(story_p))
    FP = json.load(open(fp_p))
    parts = [f'<div class="cover"><h2>{esc(S["cover"]["title"])}</h2><p>{esc(S["cover"]["subtitle"])}</p>'
             f'<p>Debrief to Boeing executive leadership · October 2026 · BOEING PROPRIETARY</p></div>']
    n = len(S["slides"])
    for i, s in enumerate(S["slides"], start=1):
        v = s["visual"]
        charty = v["type"] in ("line", "bridge", "stats")
        bullets = s.get("bullets") or []
        side = charty or (bullets and v["type"] in ("table", "columns"))
        ev = ("<div class='ev'><ul>" + "".join(f"<li>{esc(b)}</li>" for b in bullets) + "</ul></div>") if (side and bullets) else ""
        cls = "body" if charty else ("body full side" if ev else "body full")
        parts.append(f'''<section class="slide" id="s{i}"><div class="bar"><span>{esc(s["section"])}</span><span class="pn">{i + 1}</span></div>
<h2 class="at">{esc(s["action_title"])}</h2>
<div class="{cls}"><div class="vis">{visual(v, FP)}</div>{ev}</div>
<div class="take"><b>KEY TAKEAWAY</b>{esc(s["takeaway"])}</div>
<p class="src">{esc(s["source"])}</p>
<details class="notes"><summary>Speaker notes</summary><p>{esc(s["notes"])}</p></details>
<div class="foot"><span>Copyright © Boeing. All rights reserved.</span><span>BOEING PROPRIETARY</span><span>{i + 1} / {n + 1}</span></div></section>''')
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boeing Debrief: dash-2050</title><style>{CSS}</style></head><body><div class="wrap">
<div class="hd"><h1>{esc(S["cover"]["title"])}</h1><p>{esc(S["cover"]["subtitle"])} · the same eight slides as the PowerPoint, with speaker notes.</p></div>
{"".join(parts)}</div><script>{JS}</script></body></html>'''
    open(out, "w").write(page)
    print("wrote", out, len(page))


if __name__ == "__main__":
    main()
