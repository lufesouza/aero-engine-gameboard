"""Cash-profile page for the Boeing debrief: free cash flow against the fps and 787 Re-engine programme cash.

  python3 build_cash_html.py cash_profiles.json boeing_cash_profiles.html

Data: cash_profiles.json (make_cash_profiles.py), the GM's balance-sheet tracker, whole company, 2026 dollars.
Charts are drawn in the browser at the container's real width, so text keeps its size on a phone.
Palette checked with the dataviz validator (light on #ffffff, dark on #141b26): all checks pass.
"""
import json
import sys

src, out = sys.argv[1], sys.argv[2]
D = json.load(open(src))
P = D["plans"]
tax = D["tax_rate"]


def series(plan, lo, hi):
    rows = [r for r in P[plan]["rows"] if lo <= r["year"] <= hi]
    return {"year": [r["year"] for r in rows],
            "fps": [round(r["items"].get("fps", 0.0), 4) for r in rows],
            "re": [round(r["items"].get("787 Re-engine", 0.0), 4) for r in rows],
            "ovl": [round(r["items"].get("Overlap cost", 0.0), 4) for r in rows],
            "before": [round(r["fcf_before"], 4) for r in rows],
            "before_s": [round(r["fcf_before_stress"], 4) for r in rows],
            "after": [round(r["fcf"], 4) for r in rows],
            "after_s": [round(r["fcf_stress"], 4) for r in rows],
            "profit": [round(r["profit"], 4) for r in rows]}


data = {"bars": {k: series(k, 2027, 2045) for k in P}, "lines": {k: series(k, 2027, 2050) for k in P}}

# headline numbers, from the data (asserted against the debrief's figures)
R = {r["year"]: r for r in P["recommended"]["rows"]}
S = {r["year"]: r for r in P["played"]["rows"]}
tot = sum(r["spend"] for r in R.values())
items = {k: sum(r["items"].get(k, 0.0) for r in R.values()) for k in ("fps", "787 Re-engine", "Overlap cost")}
peak = max((r["spend"], y) for y, r in R.items())
weak = min((r["fcf"], y) for y, r in R.items() if y >= 2030)
weak_s = min((r["fcf_stress"], y) for y, r in R.items() if y >= 2030)
first0 = next(y for y in sorted(R) if R[y]["debt"] <= 1e-9)
first0_s = next(y for y in sorted(R) if R[y]["debt_stress"] <= 1e-9)
assert abs(tot - 66.52) < 1e-6 and peak[1] == 2036 and weak[1] == 2034 and weak_s[1] == 2034
assert all(R[y]["spend"] < R[y]["fcf_before_stress"] for y in R if y >= 2030)
assert max(R[y]["debt_stress"] for y in R if y >= 2030) <= 1e-9
dec = range(2030, 2040)
after_tax = tot * (1 - tax)
share = after_tax / sum(R[y]["fcf_before"] for y in dec)
share_s = after_tax / sum(R[y]["fcf_before_stress"] for y in dec)
f2 = lambda x: f"{x:.2f}"

CSS = """
:root { color-scheme: light;
  --page: #f3f5f9; --surface: #ffffff; --ink: #0a2240; --ink2: #3f4c63; --muted: #5f6b80; --grid: #e2e7ef; --line: #d5dce7;
  --bar: #0033a1; --bar-ink: #ffffff;
  --s-fps: #2357c8; --s-re: #009bdf; --s-ovl: #e8661c; --s-fcf: #8a43a6; --ref: #8a94a6; }
@media (prefers-color-scheme: dark) { :root:where(:not([data-theme="light"])) { color-scheme: dark;
  --page: #0d1219; --surface: #141b26; --ink: #e8edf5; --ink2: #bcc6d5; --muted: #8f9aae; --grid: #263142; --line: #2c3748;
  --bar: #142f78; --bar-ink: #ffffff;
  --s-fps: #4f63e3; --s-re: #0e9ec0; --s-ovl: #cf5f20; --s-fcf: #9f5dc4; --ref: #7d8799; } }
:root[data-theme="dark"] { color-scheme: dark;
  --page: #0d1219; --surface: #141b26; --ink: #e8edf5; --ink2: #bcc6d5; --muted: #8f9aae; --grid: #263142; --line: #2c3748;
  --bar: #142f78; --bar-ink: #ffffff;
  --s-fps: #4f63e3; --s-re: #0e9ec0; --s-ovl: #cf5f20; --s-fcf: #9f5dc4; --ref: #7d8799; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--ink); font: 15px/1.5 Arial, Helvetica, sans-serif; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 16px 24px; }
.top { background: var(--bar); color: var(--bar-ink); padding: 12px 16px; font-weight: 700; }
.top .in { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; gap: 12px; }
h1 { font-size: 1.6rem; line-height: 1.25; margin: 22px 0 6px; text-wrap: balance; }
.sub { color: var(--ink2); margin: 0 0 18px; max-width: 900px; }
.stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 0 0 18px; }
.stat { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--bar); border-radius: 6px; padding: 12px 14px; }
.stat b { display: block; font-size: 1.55rem; line-height: 1.2; }
.stat span { color: var(--ink2); font-size: .9rem; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px 12px; margin: 0 0 18px; position: relative; }
.card h2 { font-size: 1.15rem; margin: 0 0 2px; }
.card .cap { color: var(--muted); font-size: .88rem; margin: 0 0 10px; }
.ctl { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; margin: 0 0 8px; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
.seg button { font: inherit; font-size: .85rem; padding: 5px 10px; border: 0; background: transparent; color: var(--ink2); cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--bar); color: var(--bar-ink); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: .85rem; color: var(--ink2); }
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.sw { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.ln { width: 22px; height: 0; border-top: 2px solid; display: inline-block; }
.ln.d { border-top-style: dashed; }
.chart { width: 100%; }
.chart svg { display: block; width: 100%; overflow: visible; }
.chart text { fill: var(--muted); font-size: 12px; }
.chart .lab { fill: var(--ink2); font-size: 12px; font-weight: 700; }
.chart .ann { fill: var(--ink2); font-size: 11.5px; paint-order: stroke; stroke: var(--surface); stroke-width: 3px; stroke-linejoin: round; }
.tip { position: absolute; pointer-events: none; background: var(--surface); color: var(--ink); border: 1px solid var(--line);
  box-shadow: 0 4px 14px rgba(0,0,0,.15); border-radius: 6px; padding: 8px 10px; font-size: .82rem; line-height: 1.45; display: none; z-index: 5; min-width: 190px; }
.tip b { display: block; margin-bottom: 2px; }
.tip .r { display: flex; justify-content: space-between; gap: 14px; }
.tip .r i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }
.tip .tot { border-top: 1px solid var(--line); margin-top: 3px; padding-top: 3px; }
.key { font-size: .9rem; color: var(--ink2); margin: 8px 0 4px; }
details { margin: 6px 0 2px; font-size: .88rem; }
summary { cursor: pointer; color: var(--bar); font-weight: 700; }
:root[data-theme="dark"] summary { color: #8fb0ff; }
@media (prefers-color-scheme: dark) { :root:where(:not([data-theme="light"])) summary { color: #8fb0ff; } }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; font-size: .82rem; margin-top: 6px; }
th, td { padding: 4px 8px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
th:first-child, td:first-child { text-align: left; }
thead th { color: var(--ink2); }
.note { font-size: .88rem; color: var(--ink2); background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; }
.note p { margin: 0 0 6px; }
.src { font-size: .78rem; color: var(--muted); font-style: italic; margin: 12px 0 0; }
.foot { display: flex; justify-content: space-between; gap: 12px; font-size: .78rem; color: var(--muted); border-top: 1px solid var(--line); margin-top: 18px; padding-top: 10px; }
@media (max-width: 760px) { .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); } h1 { font-size: 1.3rem; } .stat b { font-size: 1.25rem; } }
"""

JS = r"""
const D = __DATA__;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const NS = 'http://www.w3.org/2000/svg';
function el(tag, attrs, parent, text) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (text !== undefined) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
const f2 = x => x.toFixed(2);
function tipShow(card, tip, html, px, py) {
  tip.innerHTML = html; tip.style.display = 'block';
  const cw = card.clientWidth, tw = tip.offsetWidth;
  let x = px + 14; if (x + tw > cw - 8) x = px - tw - 14; if (x < 8) x = 8;
  tip.style.left = x + 'px'; tip.style.top = Math.max(8, py - 10) + 'px';
}
const row = (col, lab, v, dash) => `<div class="r"><span>${col ? (dash ? `<i style="background:none;border-top:2px dashed ${col};height:0;width:16px;border-radius:0;vertical-align:3px"></i>` : `<i style="background:${col}"></i>`) : ''}${lab}</span><span>${v}</span></div>`;

let PLAN = 'recommended';

function drawBars() {
  const host = document.getElementById('c1'), card = host.closest('.card'), tip = card.querySelector('.tip');
  host.innerHTML = '';
  const d = D.bars[PLAN], n = d.year.length;
  const W = host.clientWidth, narrow = W < 560;
  const H = narrow ? 290 : 340, m = {l: 34, r: narrow ? 8 : 150, t: 20, b: 26};
  const pw = W - m.l - m.r, ph = H - m.t - m.b, ymax = 15;
  const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, height: H, role: 'img',
    'aria-label': 'Programme cash by year (fps, 787 Re-engine, overlap cost) against free cash flow before the programmes, base and stress, $B a year'}, host);
  const y = v => m.t + ph * (1 - v / ymax), band = pw / n, x = i => m.l + band * i;
  for (let t = 0; t <= ymax; t += 5) {
    el('line', {x1: m.l, x2: m.l + pw, y1: y(t), y2: y(t), stroke: css('--grid'), 'stroke-width': 1}, svg);
    el('text', {x: m.l - 6, y: y(t) + 4, 'text-anchor': 'end'}, svg, t);
  }
  d.year.forEach((yr, i) => { if (yr % 5 === 0) el('text', {x: x(i) + band / 2, y: H - 6, 'text-anchor': 'middle'}, svg, yr); });
  const keys = [['fps', '--s-fps', 'fps'], ['re', '--s-re', '787 Re-engine'], ['ovl', '--s-ovl', 'Overlap cost']];
  const bw = Math.max(4, Math.min(26, band * 0.62)), surf = css('--surface');
  d.year.forEach((yr, i) => {
    let base = 0; const segs = keys.filter(k => d[k[0]][i] > 1e-9);
    segs.forEach((k, j) => {
      const v = d[k[0]][i], y0 = y(base), y1 = y(base + v), top = j === segs.length - 1;
      const gap = j > 0 ? 2 : 0, x0 = x(i) + (band - bw) / 2, h = Math.max(0, y0 - y1 - gap);
      if (top) {
        const r = Math.min(4, h / 2, bw / 2), yb = y0 - gap, yt = yb - h;
        el('path', {d: `M${x0},${yb} V${yt + r} Q${x0},${yt} ${x0 + r},${yt} H${x0 + bw - r} Q${x0 + bw},${yt} ${x0 + bw},${yt + r} V${yb} Z`, fill: css(k[1])}, svg);
      } else el('rect', {x: x0, y: y0 - gap - h, width: bw, height: h, fill: css(k[1])}, svg);
      base += v;
    });
  });
  // free cash flow before the programmes: base (solid) and stress (dashed)
  const fcf = css('--s-fcf');
  [['before', null], ['before_s', '6 4']].forEach(([k, dash]) => {
    const pts = d.year.map((yr, i) => `${x(i) + band / 2},${y(d[k][i])}`).join(' ');
    const a = {points: pts, fill: 'none', stroke: fcf, 'stroke-width': 2, 'stroke-linejoin': 'round'};
    if (dash) a['stroke-dasharray'] = dash;
    el('polyline', a, svg);
  });
  if (!narrow) {
    const xe = m.l + pw + 8, last = n - 1;
    el('text', {x: xe, y: y(d.before[last]) + 4, class: 'lab'}, svg, `Free cash flow ${d.before[last].toFixed(1)}`);
    el('text', {x: xe, y: y(d.before_s[last]) + 4, class: 'lab'}, svg, `Stress case ${d.before_s[last].toFixed(1)}`);
  }
  // selective labels: the heaviest years
  const tot = i => d.fps[i] + d.re[i] + d.ovl[i];
  const marks = PLAN === 'recommended' && !narrow ? [2034, 2036] : [2036];
  marks.forEach(yr => { const i = d.year.indexOf(yr); el('text', {x: x(i) + band / 2, y: y(tot(i)) - 6, 'text-anchor': 'middle', class: 'ann'}, svg, f2(tot(i))); });
  // hover / focus per year
  d.year.forEach((yr, i) => {
    const r = el('rect', {x: x(i), y: m.t, width: band, height: ph, fill: 'transparent', tabindex: 0,
      'aria-label': `${yr}: programme cash ${f2(tot(i))}, free cash flow ${f2(d.before[i])}, stress ${f2(d.before_s[i])}`}, svg);
    const html = () => `<b>${yr}</b>` + keys.map(k => d[k[0]][i] > 1e-9 ? row(css(k[1]), k[2], f2(d[k[0]][i])) : '').join('')
      + `<div class="r tot"><span>Programme cash</span><span>${f2(tot(i))}</span></div>`
      + row(fcf, 'Free cash flow before', f2(d.before[i])) + row(fcf, 'Stress case', f2(d.before_s[i]), true);
    const show = ev => { const b = card.getBoundingClientRect(), hb = host.getBoundingClientRect();
      const px = ev && ev.clientX ? ev.clientX - b.left : hb.left - b.left + x(i) + band, py = ev && ev.clientY ? ev.clientY - b.top : hb.top - b.top + y(tot(i));
      tipShow(card, tip, html(), px, py); r.setAttribute('fill', 'rgba(127,127,127,.08)'); };
    const hide = () => { tip.style.display = 'none'; r.setAttribute('fill', 'transparent'); };
    r.addEventListener('mousemove', show); r.addEventListener('mouseleave', hide);
    r.addEventListener('focus', () => show()); r.addEventListener('blur', hide);
  });
}

function drawLines() {
  const host = document.getElementById('c2'), card = host.closest('.card'), tip = card.querySelector('.tip');
  host.innerHTML = '';
  const R = D.lines.recommended, S = D.lines.played, n = R.year.length;
  const W = host.clientWidth, narrow = W < 560;
  const H = narrow ? 290 : 340, m = {l: 34, r: narrow ? 8 : 150, t: 34, b: 26};
  const pw = W - m.l - m.r, ph = H - m.t - m.b, ymax = 25, x0 = R.year[0], x1 = R.year[n - 1];
  const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, height: H, role: 'img',
    'aria-label': 'Free cash flow after the programmes by year, recommended plan and fps only, base and stress, $B a year'}, host);
  const y = v => m.t + ph * (1 - v / ymax), x = yr => m.l + pw * (yr - x0) / (x1 - x0);
  for (let t = 0; t <= ymax; t += 5) {
    el('line', {x1: m.l, x2: m.l + pw, y1: y(t), y2: y(t), stroke: css('--grid'), 'stroke-width': 1}, svg);
    el('text', {x: m.l - 6, y: y(t) + 4, 'text-anchor': 'end'}, svg, t);
  }
  for (let yr = 2030; yr <= x1; yr += 5) el('text', {x: x(yr), y: H - 6, 'text-anchor': 'middle'}, svg, yr);
  // in-service markers
  [[2035, '787 Re-engine in service', 12], [2040, 'fps in service', 26]].forEach(([yr, lab, dy]) => {
    el('line', {x1: x(yr), x2: x(yr), y1: m.t - 4, y2: m.t + ph, stroke: css('--ref'), 'stroke-width': 1, 'stroke-dasharray': '2 3'}, svg);
    el('text', {x: x(yr) + 4, y: dy, class: 'ann'}, svg, lab);
  });
  const fcf = css('--s-fcf'), ref = css('--ref');
  const L = [[S, 'after', ref, null, 'fps only'], [S, 'after_s', ref, '6 4', 'fps only, stress'],
             [R, 'after', fcf, null, 'Recommended'], [R, 'after_s', fcf, '6 4', 'Recommended, stress']];
  L.forEach(([d, k, col, dash]) => {
    const a = {points: d.year.map((yr, i) => `${x(yr)},${y(d[k][i])}`).join(' '), fill: 'none', stroke: col, 'stroke-width': 2, 'stroke-linejoin': 'round'};
    if (dash) a['stroke-dasharray'] = dash;
    el('polyline', a, svg);
  });
  // weakest year markers on the recommended lines
  const iw = R.year.indexOf(2034), surf = css('--surface');
  [['after', -10], ['after_s', 18]].forEach(([k, dy]) => {
    el('circle', {cx: x(2034), cy: y(R[k][iw]), r: 4.5, fill: fcf, stroke: surf, 'stroke-width': 2}, svg);
    el('text', {x: x(2034), y: y(R[k][iw]) + dy, 'text-anchor': 'middle', class: 'ann'}, svg, f2(R[k][iw]));
  });
  if (!narrow) {
    const xe = m.l + pw + 8, last = n - 1;
    const ends = [[R.after[last], `Recommended ${R.after[last].toFixed(1)}`], [S.after[last], `fps only ${S.after[last].toFixed(1)}`],
                  [R.after_s[last], `Stress ${R.after_s[last].toFixed(1)}`], [S.after_s[last], `fps only, stress ${S.after_s[last].toFixed(1)}`]]
      .sort((a, b) => b[0] - a[0]);
    let prev = -1e9;
    ends.forEach(([v, lab]) => { let yy = Math.max(y(v) + 4, prev + 15); prev = yy; el('text', {x: xe, y: yy, class: 'lab'}, svg, lab); });
  }
  // crosshair + tooltip
  const cross = el('line', {x1: 0, x2: 0, y1: m.t, y2: m.t + ph, stroke: css('--muted'), 'stroke-width': 1, opacity: 0}, svg);
  const dots = L.map(([d, k, col]) => el('circle', {r: 4, fill: col, stroke: surf, 'stroke-width': 2, opacity: 0}, svg));
  const step = pw / (n - 1);
  R.year.forEach((yr, i) => {
    const r = el('rect', {x: x(yr) - step / 2, y: m.t, width: step, height: ph, fill: 'transparent', tabindex: 0,
      'aria-label': `${yr}: recommended ${f2(R.after[i])}, stress ${f2(R.after_s[i])}; fps only ${f2(S.after[i])}, stress ${f2(S.after_s[i])}`}, svg);
    const show = ev => {
      cross.setAttribute('x1', x(yr)); cross.setAttribute('x2', x(yr)); cross.setAttribute('opacity', 1);
      L.forEach(([d, k], j) => { dots[j].setAttribute('cx', x(yr)); dots[j].setAttribute('cy', y(d[k][i])); dots[j].setAttribute('opacity', 1); });
      const b = card.getBoundingClientRect(), hb = host.getBoundingClientRect();
      const px = ev && ev.clientX ? ev.clientX - b.left : hb.left - b.left + x(yr), py = ev && ev.clientY ? ev.clientY - b.top : hb.top - b.top + y(R.after[i]);
      tipShow(card, tip, `<b>${yr}</b>` + row(fcf, 'Recommended', f2(R.after[i])) + row(fcf, 'Recommended, stress', f2(R.after_s[i]), true)
        + row(ref, 'fps only', f2(S.after[i])) + row(ref, 'fps only, stress', f2(S.after_s[i]), true), px, py);
    };
    const hide = () => { tip.style.display = 'none'; cross.setAttribute('opacity', 0); dots.forEach(c => c.setAttribute('opacity', 0)); };
    r.addEventListener('mousemove', show); r.addEventListener('mouseleave', hide);
    r.addEventListener('focus', () => show()); r.addEventListener('blur', hide);
  });
}

function draw() { drawBars(); drawLines(); }
document.querySelectorAll('.seg button').forEach(b => b.addEventListener('click', () => {
  PLAN = b.dataset.plan;
  document.querySelectorAll('.seg button').forEach(o => o.setAttribute('aria-pressed', o === b ? 'true' : 'false'));
  document.getElementById('k1').textContent = PLAN === 'recommended'
    ? 'Tightest years: 2033-34, when both programmes spend ($7.98B and $8.24B), and 2036, the fps peak ($8.44B).'
    : 'fps only: spend peaks at $8.44B in 2036, against $13.79B of free cash flow ($9.19B in the stress case).';
  drawBars();
}));
let tm; new ResizeObserver(() => { clearTimeout(tm); tm = setTimeout(draw, 60); }).observe(document.querySelector('.wrap'));
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
draw();
"""


def table(rows_html, head):
    return ("<details><summary>Table view</summary><div class='scroll'><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head)
            + "</tr></thead><tbody>" + rows_html + "</tbody></table></div></details>")


t1 = "".join(f"<tr><td>{y}</td><td>{f2(R[y]['items'].get('fps', 0))}</td><td>{f2(R[y]['items'].get('787 Re-engine', 0))}</td>"
             f"<td>{f2(R[y]['items'].get('Overlap cost', 0))}</td><td>{f2(R[y]['spend'])}</td><td>{f2(R[y]['fcf_before'])}</td>"
             f"<td>{f2(R[y]['fcf_before_stress'])}</td></tr>" for y in range(2027, 2046))
t1 += (f"<tr><th>2030-39</th><th>{f2(items['fps'])}</th><th>{f2(items['787 Re-engine'])}</th><th>{f2(items['Overlap cost'])}</th>"
       f"<th>{f2(tot)}</th><th>{f2(sum(R[y]['fcf_before'] for y in dec))}</th><th>{f2(sum(R[y]['fcf_before_stress'] for y in dec))}</th></tr>")
t2 = "".join(f"<tr><td>{y}</td><td>{f2(R[y]['fcf'])}</td><td>{f2(R[y]['fcf_stress'])}</td><td>{f2(S[y]['fcf'])}</td><td>{f2(S[y]['fcf_stress'])}</td>"
             f"<td>{f2(R[y]['profit'])}</td></tr>" for y in range(2027, 2051))

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boeing Cash Profiles</title><style>{CSS}</style></head><body>
<div class="top"><div class="in"><span>Boeing debrief · Cash profiles</span><span>BOEING PROPRIETARY</span></div></div>
<div class="wrap">
<h1>Free cash flow covers the fps and the 787 Re-engine in every year, even in a downturn</h1>
<p class="sub">Recommended plan: the fps on the 10-year plan and the 787 Re-engine, both launched in 2030. Whole-company cash in constant
2026 dollars, from the game master's balance-sheet tracker: the analysts' consensus free cash flow, with a stress case one-third lower.</p>
<div class="stats">
<div class="stat"><b>${f2(tot)}B</b><span>programme cash, 2030-39: fps {f2(items['fps'])}, 787 Re-engine {f2(items['787 Re-engine'])}, overlap cost {f2(items['Overlap cost'])}</span></div>
<div class="stat"><b>${f2(peak[0])}B</b><span>peak year, {peak[1]} (fps alone)</span></div>
<div class="stat"><b>${f2(weak[0])}B / ${f2(weak_s[0])}B</b><span>weakest year after the programmes, {weak[1]} (base / stress)</span></div>
<div class="stat"><b>$0</b><span>new borrowing: net debt is zero from {first0} ({first0_s} in the stress case) and stays there</span></div>
</div>

<section class="card" id="cash">
<h2>Programme cash stays below free cash flow every year, even in the stress case</h2>
<p class="cap">$B a year, 2026 dollars. Bars: programme cash before tax relief. Lines: free cash flow before the programmes.</p>
<div class="ctl"><div class="seg" role="group" aria-label="Plan"><button data-plan="recommended" aria-pressed="true">Recommended: fps + 787 Re-engine</button><button data-plan="played" aria-pressed="false">As played: fps only</button></div>
<div class="legend"><span><i class="sw" style="background:var(--s-fps)"></i>fps</span><span><i class="sw" style="background:var(--s-re)"></i>787 Re-engine</span><span><i class="sw" style="background:var(--s-ovl)"></i>Overlap cost</span><span><i class="ln" style="border-color:var(--s-fcf)"></i>Free cash flow</span><span><i class="ln d" style="border-color:var(--s-fcf)"></i>Stress case</span></div></div>
<div class="chart" id="c1"></div><div class="tip"></div>
<p class="key">Until 2029 free cash flow pays net debt down to zero; from 2030 it funds the programmes, and what is left goes to the owners.</p>
<p class="key" id="k1">Tightest years: 2033-34, when both programmes spend ($7.98B and $8.24B), and 2036, the fps peak ($8.44B).</p>
{table(t1, ['Year', 'fps', '787 Re-engine', 'Overlap cost', 'Programme cash', 'Free cash flow before', 'Stress case'])}
</section>

<section class="card" id="after">
<h2>After the programmes, free cash flow never drops below ${f2(weak[0])}B, or ${f2(weak_s[0])}B in the stress case</h2>
<p class="cap">$B a year, 2026 dollars: free cash flow after programme cash, its tax relief and the programmes' own profit. Recommended plan against fps only.</p>
<div class="legend" style="margin-bottom:6px"><span><i class="ln" style="border-color:var(--s-fcf)"></i>Recommended</span><span><i class="ln d" style="border-color:var(--s-fcf)"></i>Recommended, stress</span><span><i class="ln" style="border-color:var(--ref)"></i>fps only</span><span><i class="ln d" style="border-color:var(--ref)"></i>fps only, stress</span></div>
<div class="chart" id="c2"></div><div class="tip"></div>
<p class="key">The 787 Re-engine costs cash in 2030-34 and pays it back from 2035, when it enters service. From 2040 the fps lifts free cash flow to about $21B a year.</p>
{table(t2, ['Year', 'Recommended', 'Recommended, stress', 'fps only', 'fps only, stress', 'Programmes profit change'])}
</section>

<div class="note">
<p><b>How the numbers work.</b> Free cash flow after the programmes = consensus free cash flow + {100 - tax * 100:.0f}% × (the programmes' profit change
minus programme cash) minus interest on added debt (none here). After tax relief the ${f2(tot)}B costs ${f2(after_tax)}B: {share * 100:.0f}% of the
decade's free cash flow, {share_s * 100:.0f}% in the stress case.</p>
<p><b>Programme cash</b> follows the game master's development curve (5% of the bill in the first year, peaking at 14% in year 7 of 10),
squeezed into five years for the 787 Re-engine. The overlap cost is the board's $3B cost of two developments at once, for the two years they
overlap (2033-34). The value figures in the debrief book each bill at entry into service instead; this page shows cash as it is spent.</p>
<p><b>Not modelled:</b> customer deposits, risk-sharing partners and engine makers' contributions, which would only help.</p>
</div>
<p class="src">Source: war game 2030-2050, game master's balance-sheet tracker (whole company, 2026 dollars; consensus free cash flow from
S&amp;P Capital IQ to 2030, held flat after; stress case one-third lower; 21% tax; net debt first, then owners). Both plans replayed with
every other company's orders as played.</p>
<div class="foot"><span>Copyright © Boeing. All rights reserved.</span><span>BOEING PROPRIETARY</span></div>
</div>
<script>{JS.replace('__DATA__', json.dumps(data))}</script></body></html>"""
open(out, "w").write(html)
print("wrote", out, len(html))
