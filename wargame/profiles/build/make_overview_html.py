#!/usr/bin/env python3
"""Build the one-page overview of the war-game players and their leaders.

Usage: make_overview_html.py <overview_data.json> <out.html>

The data file holds {"players": [...], "compare": {...}} as produced by the
players-overview-data workflow (per-player extraction from the verified
profiles, an adversarial verification pass per player, then a cross-player
comparison). This script adds the game parameters from wargame/config and
writes a self-contained HTML page: inline CSS and JS, data embedded as JSON.
"""
import datetime
import html
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
data = json.load(open(sys.argv[1]))
cfg = json.load(open(os.path.join(ROOT, "wargame", "config", "default.json")))
params = {k: {"wacc": v["wacc"], "alpha": v["alpha"]} for k, v in cfg["players"].items()}
for k in ("rolls_royce", "pratt_whitney"):
    s = cfg["suppliers"][k]
    params[k] = {"wacc": s["wacc"], "alpha": s["alpha"]}
data["params"] = params
data["built"] = datetime.date.today().isoformat()
order = ["boeing", "airbus", "rolls_royce", "pratt_whitney", "cfm"]
data.setdefault("pending", [])
data.setdefault("provisional_caveats", [])
data["players"].sort(key=lambda p: order.index(p["player_id"]) if p["player_id"] in order else 99)
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

PAGE = r"""<title>Aero War Game Players</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a wayfinding-style briefing book. Summary first, then a topic-by-player matrix,
   then explorers for topics and leaders. Player colours follow the game's own sides:
   Blue = Boeing, Red = Airbus; the engine makers get amber, violet and the market-cell green. */
:root {
  --bg: #f3f5f8; --surface: #ffffff; --sunk: #e8ecf2; --line: #d3dae4;
  --fg: #16202e; --muted: #556275; --faint: #7d8899;
  --accent: #1d4ed8;
  --boeing: #1f5fbf; --airbus: #c2352b; --rolls_royce: #a16207; --pratt_whitney: #7c3aed; --cfm: #15803d;
  --r1: #e3ecf8; --r2: #c4d6ef; --r3: #8fb0dd; --r4: #4f7fc2; --r5: #1f4f94; --rtext-hi: #ffffff; --rtext-lo: #16202e;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
  --radius: 6px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0d131c; --surface: #141c28; --sunk: #1b2533; --line: #2a3647;
  --fg: #e6ebf2; --muted: #a2adbd; --faint: #7a8597; --accent: #7aa7ff;
  --boeing: #6ea2f2; --airbus: #f07a70; --rolls_royce: #e0a93a; --pratt_whitney: #b394ff; --cfm: #4cc27a;
  --r1: #1c2a3f; --r2: #24406a; --r3: #2f5b98; --r4: #4b7fd0; --r5: #8db3f5; --rtext-hi: #0d131c; --rtext-lo: #e6ebf2;
  color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0d131c; --surface: #141c28; --sunk: #1b2533; --line: #2a3647;
  --fg: #e6ebf2; --muted: #a2adbd; --faint: #7a8597; --accent: #7aa7ff;
  --boeing: #6ea2f2; --airbus: #f07a70; --rolls_royce: #e0a93a; --pratt_whitney: #b394ff; --cfm: #4cc27a;
  --r1: #1c2a3f; --r2: #24406a; --r3: #2f5b98; --r4: #4b7fd0; --r5: #8db3f5; --rtext-hi: #0d131c; --rtext-lo: #e6ebf2;
  color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
.wrap { max-width: 1240px; margin: 0 auto; padding-inline: 20px; padding-block: 0 64px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; letter-spacing: .01em; line-height: 1.1; text-wrap: balance; margin: 0; }
h1 { font-size: clamp(2.4rem, 5vw, 3.6rem); font-weight: 700; }
h2 { font-size: 1.9rem; }
h3 { font-size: 1.3rem; }
p { margin: 0; }
.eyebrow { font: 600 .74rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.muted { color: var(--muted); }
.mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
a { color: var(--accent); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* top bar */
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); border-bottom: 1px solid var(--line); }
.bar .wrap { display: flex; gap: 18px; align-items: center; padding-block: 10px; overflow-x: auto; }
.bar .brand { font: 700 1.05rem/1 var(--font-display); letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; }
.bar nav { display: flex; gap: 14px; }
.bar nav a { font: 500 .82rem/1 var(--font-body); color: var(--muted); text-decoration: none; white-space: nowrap; }
.bar nav a:hover { color: var(--fg); }

section { padding-top: 48px; display: grid; gap: 18px; scroll-margin-top: 56px; }
.lede { font-size: 1.12rem; max-width: 70ch; }
.intro { display: grid; gap: 14px; padding-top: 36px; }

/* player chips & cards */
.dot { display: inline-block; width: .7em; height: .7em; border-radius: 50%; background: var(--pc, var(--faint)); flex: none; }
.pname { font-family: var(--font-display); font-weight: 600; font-size: 1.05rem; letter-spacing: .02em; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px; display: grid; gap: 10px; align-content: start; min-width: 0; border-top: 4px solid var(--pc); }
.card .role { font: 500 .72rem/1.3 var(--font-mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.card dl { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; margin: 0; font-size: .82rem; }
.card dt { color: var(--muted); }
.card dd { margin: 0; font-family: var(--font-mono); font-variant-numeric: tabular-nums; overflow-wrap: anywhere; min-width: 0; }

/* tables */
.scroll { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: .86rem; }
th, td { text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }
thead th { font: 600 .95rem/1.2 var(--font-display); letter-spacing: .03em; background: var(--sunk); position: sticky; top: 0; }
tbody th { font: 600 .78rem/1.3 var(--font-mono); text-transform: uppercase; letter-spacing: .05em; color: var(--muted); white-space: nowrap; }
.matrix td { min-width: 190px; }
.matrix td button { all: unset; cursor: pointer; display: block; }
.matrix td button:hover .hl, .matrix td button:focus-visible .hl { text-decoration: underline; text-decoration-color: var(--pc); text-underline-offset: 3px; }
.hl { font-weight: 500; }

/* risk chips */
.rating { display: inline-block; font: 500 .74rem/1 var(--font-mono); padding: 5px 8px; border-radius: 3px; white-space: nowrap; }
.rating[data-r="Low"] { background: var(--r1); color: var(--rtext-lo); }
.rating[data-r="Low-Medium"] { background: var(--r2); color: var(--rtext-lo); }
.rating[data-r="Medium"] { background: var(--r3); color: var(--rtext-lo); }
.rating[data-r="Medium-High"] { background: var(--r4); color: var(--rtext-hi); }
.rating[data-r="High"] { background: var(--r5); color: var(--rtext-hi); }
.legend { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: .8rem; color: var(--muted); }
.risk td { min-width: 170px; }
.risk .note { font-size: .8rem; color: var(--muted); margin-top: 6px; }

/* contrasts */
.contrasts { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.contrast { padding: 14px 16px; border-left: 3px solid var(--line); display: grid; gap: 6px; background: var(--surface); border-radius: 0 var(--radius) var(--radius) 0; }
.contrast .who { display: flex; gap: 6px; flex-wrap: wrap; }

/* tabs & filters */
.tabs { display: flex; flex-wrap: wrap; gap: 6px; }
.tab, .chip { font: 500 .82rem/1 var(--font-body); padding: 8px 12px; border-radius: 999px; border: 1px solid var(--line); background: var(--surface); color: var(--fg); cursor: pointer; }
.tab[aria-selected="true"], .chip[aria-pressed="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.filters { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; }
.filters .group { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.filters .label { font: 600 .7rem/1 var(--font-mono); text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.panel { display: grid; gap: 18px; }
.compare-box { background: var(--sunk); border-radius: var(--radius); padding: 16px 18px; display: grid; gap: 10px; }
.standouts { display: grid; gap: 6px; margin: 0; padding: 0; list-style: none; }
.standouts li { display: flex; gap: 8px; align-items: baseline; font-size: .9rem; }
.pgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }
.entry { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px; display: grid; gap: 8px; align-content: start; min-width: 0; }
.entry .head { display: flex; gap: 8px; align-items: center; }
.ids { display: flex; flex-wrap: wrap; gap: 4px; }
.id { font: 400 .68rem/1 var(--font-mono); padding: 3px 5px; border-radius: 3px; background: var(--sunk); color: var(--muted); }
.people-list { display: grid; gap: 8px; }
.prow { display: grid; grid-template-columns: minmax(150px, 220px) 1fr; gap: 6px 16px; padding: 12px 14px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); }
.prow .who { display: grid; gap: 3px; align-content: start; }
.prow .meta { font: 400 .72rem/1.3 var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
.prow .txt { display: grid; gap: 6px; min-width: 0; }
.empty { color: var(--muted); font-style: italic; }

/* leaders directory */
.company { display: grid; gap: 12px; }
.company > header { display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }
.seats { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
.seat { display: grid; gap: 10px; align-content: start; min-width: 0; }
.seat > .eyebrow { padding-bottom: 4px; border-bottom: 1px solid var(--line); }
.person { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px; display: grid; gap: 8px; }
.person.current { border-color: var(--pc); box-shadow: inset 3px 0 0 var(--pc); }
.person .badge { font: 500 .66rem/1 var(--font-mono); text-transform: uppercase; letter-spacing: .08em; padding: 4px 6px; border-radius: 3px; background: var(--sunk); color: var(--muted); justify-self: start; }
.person.current .badge { background: var(--pc); color: var(--surface); }
.person .name { font: 600 1.15rem/1.15 var(--font-display); letter-spacing: .02em; }
.person .td { font-size: .8rem; color: var(--muted); }
.person blockquote { margin: 0; padding-left: 10px; border-left: 2px solid var(--line); font-style: italic; font-size: .88rem; }
.person details summary { cursor: pointer; font-size: .82rem; color: var(--accent); }
.person details dl { margin: 8px 0 0; display: grid; gap: 8px; font-size: .85rem; }
.person details dt { font: 600 .68rem/1 var(--font-mono); text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.person details dd { margin: 2px 0 0; }
.seatcmp { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.seatcmp > div { background: var(--sunk); border-radius: var(--radius); padding: 14px 16px; display: grid; gap: 8px; }
.teams { display: grid; gap: 6px; margin: 0; padding: 0; list-style: none; }
.teams li { display: grid; grid-template-columns: minmax(170px, 260px) 1fr; gap: 4px 14px; padding: 10px 12px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); font-size: .88rem; }
.teams li.default { border-color: var(--pc); }
.teams code { font: 500 .78rem/1.3 var(--font-mono); }
.levers { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.levers ul { margin: 0; padding-left: 18px; display: grid; gap: 6px; font-size: .88rem; }
.notes { display: grid; gap: 8px; font-size: .88rem; max-width: 80ch; }
.notes ul { margin: 0; padding-left: 18px; display: grid; gap: 6px; }
.status { margin-top: 18px; padding: 12px 16px; border: 1px dashed var(--line); border-radius: var(--radius); background: var(--surface); display: grid; gap: 6px; font-size: .88rem; max-width: 90ch; }
.status b { font-family: var(--font-display); font-size: 1.05rem; letter-spacing: .03em; }
.pill { justify-self: start; font: 500 .66rem/1 var(--font-mono); text-transform: uppercase; letter-spacing: .08em; padding: 4px 6px; border-radius: 3px; background: var(--sunk); color: var(--muted); }
.pill.ok { background: var(--pc); color: var(--surface); }
.card.pending { border-style: dashed; border-top-style: solid; }
footer.src { padding-top: 40px; font-size: .8rem; color: var(--muted); display: grid; gap: 6px; max-width: 90ch; }
@media (max-width: 640px) {
  .prow, .teams li { grid-template-columns: 1fr; }
  section { padding-top: 36px; }
}
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
</style>

<div class="bar"><div class="wrap">
  <span class="brand">Aero War Game Players</span>
  <nav aria-label="Sections">
    <a href="#summary">Summary</a><a href="#matrix">Comparison</a><a href="#risk">Risk</a><a href="#contrasts">Contrasts</a>
    <a href="#topics">By topic</a><a href="#leaders">Leaders</a><a href="#teams">Teams</a><a href="#levers">Game levers</a><a href="#notes">Notes</a>
  </nav>
</div></div>

<main class="wrap">
  <div class="intro" id="summary">
    <span class="eyebrow">Boeing vs Airbus war game · players, leaders and how they decide</span>
    <h1 id="headline"></h1>
    <p class="lede" id="summary-text"></p>
    <p class="muted" id="built"></p>
    <div class="status" id="status" hidden></div>
  </div>
  <section aria-labelledby="h-players"><h2 id="h-players" class="eyebrow">The five players</h2><div class="cards" id="player-cards"></div></section>
  <section id="matrix" aria-labelledby="h-matrix">
    <h2 id="h-matrix">Comparison by topic</h2>
    <p class="muted">Each cell is the player's own doctrine on that topic. Select a cell to open the topic with every player's full entry and what its leaders say.</p>
    <div class="scroll"><table class="matrix" id="matrix-table"></table></div>
  </section>
  <section id="risk" aria-labelledby="h-risk">
    <h2 id="h-risk">Risk appetite</h2>
    <div class="legend" id="risk-legend"></div>
    <div class="scroll"><table class="risk" id="risk-table"></table></div>
  </section>
  <section id="contrasts" aria-labelledby="h-contrasts"><h2 id="h-contrasts">Sharpest contrasts</h2><div class="contrasts" id="contrast-list"></div></section>
  <section id="topics" aria-labelledby="h-topics">
    <h2 id="h-topics">Players and leaders by topic</h2>
    <div class="tabs" role="tablist" id="topic-tabs"></div>
    <div class="panel" id="topic-panel"></div>
  </section>
  <section id="leaders" aria-labelledby="h-leaders">
    <h2 id="h-leaders">Leaders by seat</h2>
    <p class="muted">Boeing, Airbus and CFM have executive profiles. Rolls-Royce and Pratt &amp; Whitney are profiled as companies only. CFM's seats are held by GE executives, who decide GE's half of the GE-Safran joint venture.</p>
    <div class="seatcmp" id="seat-compare"></div>
    <div id="directory" class="panel"></div>
  </section>
  <section id="teams" aria-labelledby="h-teams"><h2 id="h-teams">Leadership teams</h2><div id="team-list" class="panel"></div></section>
  <section id="levers" aria-labelledby="h-levers"><h2 id="h-levers">Game levers and default stances</h2><div class="levers" id="lever-list"></div></section>
  <section id="notes" aria-labelledby="h-notes"><h2 id="h-notes">Caveats and method</h2><div class="notes" id="notes-body"></div></section>
  <footer class="src" id="sources"></footer>
</main>

<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  const D = JSON.parse(document.getElementById('data').textContent);
  const TOPICS = [
    ['objectives', 'Objectives'], ['capital', 'Capital and balance sheet'], ['product', 'Product and technology'],
    ['risk', 'Risk appetite'], ['operations', 'Operations and execution'], ['rivals', 'Rivals, customers, partners'],
    ['credibility', 'Guidance and credibility'], ['crisis', 'Crisis response'], ['game', 'In the war game'], ['biases', 'Biases']];
  const TL = Object.fromEntries(TOPICS);
  const RISK = [['technology', 'Technology'], ['schedule', 'Schedule'], ['balance_sheet', 'Balance sheet'], ['pricing', 'Pricing / fixed price']];
  const RATINGS = ['Low', 'Low-Medium', 'Medium', 'Medium-High', 'High'];
  const SEATS = [['CEO', 'CEO seat'], ['CFO', 'CFO seat'], ['COO', 'Operating (COO) seat']];
  const P = D.players, byId = Object.fromEntries(P.map(p => [p.player_id, p]));
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const pc = id => `--pc: var(--${id})`;
  const ids = a => a && a.length ? `<div class="ids">${a.map(i => `<span class="id">${esc(i)}</span>`).join('')}</div>` : '';
  const short = p => ({ boeing: 'Boeing', airbus: 'Airbus', rolls_royce: 'Rolls-Royce', pratt_whitney: 'Pratt & Whitney', cfm: 'CFM (GE side)' }[p.player_id] || p.name);
  const tag = id => byId[id] ? `<span class="dot" style="${pc(id)}"></span>&nbsp;<b>${esc(short(byId[id]))}</b>` : esc(id);
  const topicOf = (obj, key) => (obj.topics || []).find(t => t.key === key);

  const C = D.compare || null;
  const NAMES = { boeing: ['Boeing', 'Airframer player (Blue)'], airbus: ['Airbus', 'Airframer player (Red)'], rolls_royce: ['Rolls-Royce', 'Engine-supplier player (optional)'], pratt_whitney: ['Pratt & Whitney', 'Engine-supplier player (optional, inside RTX)'], cfm: ['CFM International (GE side)', 'Engine maker, not a player'] };
  document.getElementById('headline').textContent = C ? C.headline : 'How the war-game players decide';
  document.getElementById('summary-text').textContent = C ? C.summary : 'What each player optimises and how its leaders decide, topic by topic: objectives, capital, products, risk, operations, rivals, credibility, crises, game stance and biases.';
  const drafts = P.filter(p => p.status === 'draft'), pend = D.pending || [];
  if (drafts.length || pend.length || !C) {
    const st = document.getElementById('status'); st.hidden = false;
    const cit = P.reduce((a, p) => a + (p.id_check?.cited || 0), 0);
    const todo = [];
    const SN = { boeing: 'Boeing', airbus: 'Airbus', rolls_royce: 'Rolls-Royce', pratt_whitney: 'Pratt & Whitney', cfm: 'CFM' };
    if (pend.length) todo.push(pend.map(x => SN[x]).join(' and ') + (pend.length > 1 ? ' are' : ' is') + ' being extracted');
    if (drafts.length) todo.push('the independent fact-check of ' + drafts.map(p => short(p)).join(', '));
    if (!C) todo.push('the cross-player comparison and contrasts');
    st.innerHTML = `<b>Early version · ${P.length} of 5 players</b>
      <span>Still in progress: ${esc(todo.join('; '))}. This page will be updated at the same link.</span>
      <span class="muted">Checks already run on what is shown: all <span class="mono">${cit.toLocaleString('en-US')}</span> evidence citations resolve to verified items, and every leader quote was found word for word in the sources.</span>`;
  }
  const nItems = P.reduce((a, p) => a + (p.evidence?.items || 0), 0);
  const nPeople = P.reduce((a, p) => a + (p.people?.length || 0), 0);
  document.getElementById('built').innerHTML = `<span class="mono">${nItems.toLocaleString('en-US')}</span> verified evidence items · <span class="mono">${nPeople}</span> leaders profiled · built <span class="mono">${esc(D.built)}</span>`;

  // player cards
  document.getElementById('player-cards').innerHTML = P.map(p => {
    const prm = D.params[p.player_id];
    const def = (p.teams || []).find(t => t.is_default);
    return `<article class="card" style="${pc(p.player_id)}">
      <div style="display:flex;gap:8px;align-items:center"><span class="dot"></span><span class="pname">${esc(p.name)}</span></div>
      <span class="role">${esc(p.game_role)}</span>
      ${p.status === 'draft' ? '<span class="pill">Not yet fact-checked</span>' : p.status === 'checked' ? '<span class="pill ok">Fact-checked</span>' : ''}
      <p>${esc(p.tagline)}</p>
      <dl>
        <dt>Evidence items</dt><dd>${(p.evidence?.items || 0).toLocaleString('en-US')}</dd>
        <dt>Leaders</dt><dd>${p.people?.length || 'none'}</dd>
        ${prm ? `<dt>WACC (game)</dt><dd>${(prm.wacc * 100).toFixed(1)}%</dd><dt>Capex weight α</dt><dd>${prm.alpha}</dd>` : `<dt>In the game</dt><dd>not a player</dd>`}
        ${def ? `<dt>Default team</dt><dd>${esc(def.id)}</dd>` : ''}
      </dl>
      <details><summary class="muted" style="cursor:pointer;font-size:.82rem">Summary and confidence</summary>
        <p style="margin-top:8px;font-size:.88rem">${esc(p.summary)}</p>
        <p class="muted" style="margin-top:6px;font-size:.8rem">${esc(p.evidence?.sources)}. ${esc(p.evidence?.confidence)}</p></details>
    </article>`;
  }).join('') + (D.pending || []).map(id => `<article class="card pending" style="${pc(id)}">
      <div style="display:flex;gap:8px;align-items:center"><span class="dot"></span><span class="pname">${esc(NAMES[id][0])}</span></div>
      <span class="role">${esc(NAMES[id][1])}</span><span class="pill">In progress</span>
      <p class="muted">Being extracted from its verified profiles. It joins the comparison in the next update.</p></article>`).join('');

  // matrix
  const mt = document.getElementById('matrix-table');
  mt.innerHTML = `<thead><tr><th scope="col">Topic</th>${P.map(p => `<th scope="col" style="${pc(p.player_id)}"><span class="dot"></span> ${esc(short(p))}</th>`).join('')}</tr></thead>
    <tbody>${TOPICS.map(([k, l]) => `<tr><th scope="row">${esc(l)}</th>${P.map(p => {
      const t = topicOf(p, k);
      return `<td style="${pc(p.player_id)}">${t ? `<button data-topic="${k}" data-player="${p.player_id}"><span class="hl">${esc(t.headline)}</span></button>` : '<span class="empty">no entry</span>'}</td>`;
    }).join('')}</tr>`).join('')}</tbody>`;
  mt.addEventListener('click', e => { const b = e.target.closest('button[data-topic]'); if (!b) return; selectTopic(b.dataset.topic, b.dataset.player); document.getElementById('topics').scrollIntoView(); });

  // risk
  document.getElementById('risk-legend').innerHTML = 'Rating scale: ' + RATINGS.map(r => `<span class="rating" data-r="${r}">${r}</span>`).join('');
  document.getElementById('risk-table').innerHTML = `<thead><tr><th scope="col">Risk</th>${P.map(p => `<th scope="col" style="${pc(p.player_id)}"><span class="dot"></span> ${esc(short(p))}</th>`).join('')}</tr></thead>
    <tbody>${RISK.map(([k, l]) => `<tr><th scope="row">${esc(l)}</th>${P.map(p => {
      const r = (p.risk_ratings || []).find(x => x.dimension === k);
      return `<td>${r ? `<span class="rating" data-r="${esc(r.rating)}">${esc(r.rating)}</span><div class="note">${esc(r.note)}</div>${ids(r.ids)}` : '<span class="empty">not rated</span>'}</td>`;
    }).join('')}</tr>`).join('')}</tbody>`;

  // contrasts
  document.getElementById('contrast-list').innerHTML = C ? (C.contrasts || []).map(c => `<article class="contrast">
    <h3>${esc(c.title)}</h3><div class="who">${(c.players || []).map(tag).join(' · ')}</div><p>${esc(c.text)}</p></article>`).join('')
    : '<p class="muted">The sharpest contrasts arrive with the cross-player comparison, once all five players are in.</p>';

  // topic explorer
  const tabs = document.getElementById('topic-tabs'), panel = document.getElementById('topic-panel');
  const state = { topic: 'objectives', co: 'all', seat: 'all', status: 'current', focus: null };
  tabs.innerHTML = TOPICS.map(([k, l]) => `<button class="tab" role="tab" id="tab-${k}" data-k="${k}" aria-selected="false">${esc(l)}</button>`).join('');
  tabs.addEventListener('click', e => { const b = e.target.closest('.tab'); if (b) selectTopic(b.dataset.k, null); });
  function selectTopic(k, focus) {
    state.topic = k; state.focus = focus;
    tabs.querySelectorAll('.tab').forEach(t => t.setAttribute('aria-selected', String(t.dataset.k === k)));
    renderTopic();
  }
  function people() {
    const out = [];
    P.forEach(p => (p.people || []).forEach(x => out.push(Object.assign({ pid: p.player_id }, x))));
    return out;
  }
  const ALL = people();
  function chipGroup(label, key, opts) {
    return `<div class="group" role="group" aria-label="${esc(label)}"><span class="label">${esc(label)}</span>${opts.map(([v, l]) => `<button class="chip" data-f="${key}" data-v="${v}" aria-pressed="${state[key] === v}">${esc(l)}</button>`).join('')}</div>`;
  }
  function renderTopic() {
    const k = state.topic, cmp = C ? (C.per_topic || []).find(t => t.key === k) : null;
    const ents = P.map(p => { const t = topicOf(p, k); return `<article class="entry" style="${pc(p.player_id)}${state.focus === p.player_id ? ';outline:2px solid var(--pc)' : ''}">
      <div class="head"><span class="dot"></span><span class="pname">${esc(short(p))}</span></div>
      ${t ? `<b>${esc(t.headline)}</b><p>${esc(t.text)}</p>${ids(t.ids)}` : '<p class="empty">No entry.</p>'}</article>`; }).join('');
    const rows = ALL.filter(x => (state.co === 'all' || x.pid === state.co) && (state.seat === 'all' || x.seat === state.seat) && (state.status === 'all' || x.status === state.status))
      .map(x => ({ x, t: topicOf(x, k) })).filter(r => r.t)
      .sort((a, b) => ['boeing', 'airbus', 'cfm'].indexOf(a.x.pid) - ['boeing', 'airbus', 'cfm'].indexOf(b.x.pid) || ['CEO', 'CFO', 'COO'].indexOf(a.x.seat) - ['CEO', 'CFO', 'COO'].indexOf(b.x.seat) || (a.x.status === 'current' ? -1 : 1) - (b.x.status === 'current' ? -1 : 1));
    panel.innerHTML = `
      ${cmp ? `<div class="compare-box"><span class="eyebrow">How the players compare</span><p>${esc(cmp.comparison)}</p>
        <ul class="standouts">${(cmp.standouts || []).map(s => `<li>${tag(s.player_id)}<span>${esc(s.note)}</span></li>`).join('')}</ul></div>` : ''}
      <div class="pgrid">${ents}</div>
      <div style="display:grid;gap:12px">
        <h3>What the leaders say on ${esc(TL[k].toLowerCase())}</h3>
        <div class="filters">
          ${chipGroup('Company', 'co', [['all', 'All'], ['boeing', 'Boeing'], ['airbus', 'Airbus'], ['cfm', 'CFM']])}
          ${chipGroup('Seat', 'seat', [['all', 'All'], ['CEO', 'CEO'], ['CFO', 'CFO'], ['COO', 'COO']])}
          ${chipGroup('Holders', 'status', [['current', 'Current'], ['all', 'Current and past']])}
        </div>
        <div class="people-list">${rows.length ? rows.map(({ x, t }) => `<div class="prow" style="${pc(x.pid)}">
          <div class="who"><span style="display:flex;gap:6px;align-items:center"><span class="dot"></span><b>${esc(x.name)}</b></span>
            <span class="meta">${esc(short(byId[x.pid]))} · ${esc(x.seat)} · ${x.status === 'current' ? 'current' : 'past'}</span></div>
          <div class="txt"><p>${esc(t.text)}</p>${ids(t.ids)}</div></div>`).join('') : '<p class="empty">No leader entry on this topic for the selected filters.</p>'}</div>
      </div>`;
  }
  panel.addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; state[b.dataset.f] = b.dataset.v; renderTopic(); });
  selectTopic('objectives', null);

  // seats + directory
  document.getElementById('seat-compare').innerHTML = ((C && C.seats) || []).map(s => `<div><span class="eyebrow">${esc(s.seat)} seat compared</span><p>${esc(s.comparison)}</p></div>`).join('');
  document.getElementById('directory').innerHTML = P.filter(p => (p.people || []).length).map(p => `<div class="company" style="${pc(p.player_id)}">
    <header><span class="dot"></span><h3>${esc(p.name)}</h3><span class="muted">${p.people.length} leaders</span></header>
    <div class="seats">${SEATS.map(([s, l]) => { const ps = p.people.filter(x => x.seat === s).sort((a, b) => (a.status === 'current' ? -1 : 1) - (b.status === 'current' ? -1 : 1));
      return `<div class="seat"><span class="eyebrow">${esc(l)}</span>${ps.map(x => `<article class="person${x.status === 'current' ? ' current' : ''}">
        <span class="badge">${x.status === 'current' ? 'Current' : 'Past'}</span>
        <span class="name">${esc(x.name)}</span><span class="td">${esc(x.title_dates)}</span>
        <p>${esc(x.tagline)}</p>
        ${(x.voice || []).map(v => `<blockquote>“${esc(v.quote)}” <span class="id">${esc(v.id)}</span></blockquote>`).join('')}
        <span class="td">Confidence: ${esc(x.confidence)}</span>
        ${(x.teams || []).length ? `<span class="td">Teams: <span class="mono">${x.teams.map(esc).join(', ')}</span></span>` : ''}
        <details><summary>All topics (${(x.topics || []).length})</summary><dl>${TOPICS.map(([k, l]) => { const t = topicOf(x, k); return t ? `<div><dt>${esc(l)}</dt><dd>${esc(t.text)} ${ids(t.ids)}</dd></div>` : ''; }).join('')}</dl></details>
      </article>`).join('') || '<p class="empty">No profile.</p>'}</div>`; }).join('')}</div></div>`).join('');

  // teams
  document.getElementById('team-list').innerHTML = P.filter(p => (p.teams || []).length).map(p => `<div class="company" style="${pc(p.player_id)}">
    <header><span class="dot"></span><h3>${esc(p.name)}</h3></header>
    <ul class="teams">${p.teams.map(t => `<li class="${t.is_default ? 'default' : ''}"><div><code>${esc(t.id)}</code>${t.is_default ? ' <span class="rating" data-r="Medium-High">default</span>' : ''}<div class="muted" style="font-size:.8rem">${esc(t.members)}</div></div><p>${esc(t.one_line)}</p></li>`).join('')}</ul></div>`).join('');

  // levers
  document.getElementById('lever-list').innerHTML = P.map(p => `<div class="entry" style="${pc(p.player_id)}"><div class="head"><span class="dot"></span><span class="pname">${esc(p.name)}</span></div>
    <ul>${(p.levers || []).map(l => `<li><b>${esc(l.lever)}</b>: ${esc(l.stance)}</li>`).join('')}</ul></div>`).join('');

  // notes
  const vcount = P.filter(p => p.status === 'checked').map(p => { const last = (p.verifier_notes || []).slice(-1)[0] || ''; return `${short(p)}: ${last}`; });
  const cav = (C && C.caveats) || D.provisional_caveats || [];
  document.getElementById('notes-body').innerHTML = `<ul>${cav.map(c => `<li>${esc(c)}</li>`).join('')}</ul>
    <p class="muted">Every entry cites the evidence ids behind it (B-, BX-, A-, AX-, R-, P-, CX-). Each id is a verified quote or spreadsheet cell in the profile folders under <span class="mono">wargame/profiles/</span>. Each player's section was extracted from its profiles and then checked by an independent fact-checker. ${vcount.length ? 'Fact-check results: ' + vcount.map(esc).join('; ') + '.' : 'The independent fact-check is still running.'}</p>`;
  document.getElementById('sources').innerHTML = `<span>Sources: Boeing earnings calls 2006-2025, 10-Ks and analyst models; the Airbus FY2025 Board Report and Boeing-side observations; Rolls-Royce calls 2010-2025, Morgan Stanley model and Capital IQ data; UTC/RTX calls and 10-Ks 2015-2025 and the Goldman Sachs RTX/GTF model; GE / GE Aerospace calls 2015-2025 and Capital IQ profiles. Professional conduct only.</span>
    <span>Game parameters (WACC, capex weight α) come from <span class="mono">wargame/config/default.json</span>.</span>`;
})();
</script>
"""

out = PAGE.replace("__DATA__", payload)
open(sys.argv[2], "w").write(out)
print(sys.argv[2], f"{len(out) / 1024:.0f} KB")
