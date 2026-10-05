#!/usr/bin/env python3
"""Build a timeline page of a five-player war-game run: every launch, entry into service, engine
fallback, cancellation, commitment, tactic, inject and market reaction, by player and year.

Usage: python3 wargame/reports/make_timeline_html.py <run id> <out.html> [--title "<page title>"]

Years and programmes come from the engine's replay of the run, so the page matches the adjudicated
record. It carries public moves only: no private rationales and no assigned objectives.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from wargame import engine as E  # noqa: E402
from wargame import model as M  # noqa: E402

LANES = [("world", "Shocks and market"), ("boeing", "Boeing"), ("airbus", "Airbus"),
         ("pratt_whitney", "Pratt & Whitney"), ("rolls_royce", "Rolls-Royce"), ("cfm", "CFM/GE")]


def build_data(run_id):
    st = E.load_state(run_id)
    cfg = st["config"]
    hist = st["history"]
    w = M.build_world(cfg, hist)
    eng = lambda seg, e: cfg["engine_options"][seg][e]["label"]
    rounds = [{"round": t["turn"], "from": t["years"][0], "to": t["years"][1],
               "inject": ", ".join(cfg["injects"]["deck"][i]["title"] for i in next(r for r in hist if r["turn"] == t["turn"])["injects"])}
              for t in cfg["turns"][:st["turns_total"]]]
    rnd = lambda y: next((r["round"] for r in rounds if r["from"] <= y <= r["to"]), None)
    ev, spans = [], []

    def add(year, lane, kind, title, detail="", **kw):
        fallback_round = kw.pop("round_", None)
        ev.append(dict(year=year, lane=lane, kind=kind, title=title, detail=detail, round=rnd(year) or fallback_round, **kw))

    # Shocks and market
    for r in hist:
        a, _ = M.turn_years(cfg, r["turn"])
        for i in r.get("injects", []):
            d = cfg["injects"]["deck"][i]
            add(a, "world", "inject", d["title"], d["narrative"])
        mk = (r.get("market") or {}).get("capture_mult") or {}
        if mk:
            names = {"ngsa": "NGSA", "fps": "fps", "rea350": "A350 Re-engine"}
            add(a, "world", "market", "Market reaction",
                "Airline and lessor demand multipliers: " + ", ".join(f"{names.get(k, k)} ×{v:.2f}" for k, v in mk.items())
                + (". " + r["market_narrative"] if r.get("market_narrative") else ""))
    wave = cfg["segments"]["nb"].get("replacement_wave", {})
    if wave:
        spans.append(dict(lane="world", key="wave", start=2037, end=2044, kind="wave", label="Replacement wave builds",
                          detail="737 MAX and A320neo replacements rise from about 40 aircraft in 2037 to about 800 a year from 2044."))
    of = cfg["engine_options"]["nb"].get("cfm_open_fan", {}).get("available_eis")
    if of:
        add(of, "world", "milestone", "Open fan could enter service",
            "The first year the RISE open fan can enter service. No airframe flies it: both new single-aisles were committed to the LEAP derivative by 2031.", round_=3)

    # Airframe programmes
    names = {"ngsa": "NGSA", "fps": "fps", "rea350": "A350 Re-engine", "re787": "787 Re-engine"}
    for pid, p in sorted(w.programs.items(), key=lambda kv: kv[1].launch_year):
        pc = cfg["programs"][pid]
        flown = eng(p.segment, p.engine)
        extra = []
        if p.variant:
            extra.append(pc["variants"][p.variant]["label"])
        if p.ramp:
            extra.append(pc["ramp_options"][p.ramp]["label"])
        what = f"{names.get(pid, pid)} launched" + (f" ({', '.join(extra)})" if extra else "")
        if p.engine_requested:
            req_maker = cfg["engine_options"][p.segment][p.engine_requested].get("maker")
            if req_maker in M.active_suppliers(cfg):
                req = M.supplier_requirement(cfg, p.segment, p.engine_requested)
                sp = w.sup_programs.get(req[1]) if req else None
                why = (f"it cancelled that engine in the same round ({sp.cancelled_year})" if sp is not None and sp.cancelled_year == p.launch_year
                       else "it had not launched that engine")
                add(p.launch_year, req_maker, "missed", f"{names.get(pid, pid)} asked for its engine",
                    f"{cfg['players'][p.owner]['label']} named the {eng(p.segment, p.engine_requested)}, but {why}, "
                    f"so {names.get(pid, pid)} went to the {eng(p.segment, p.engine)}.", program=pid)
            add(p.launch_year, p.owner, "launch", what,
                f"Asked for the {eng(p.segment, p.engine_requested)}; flies the {flown}. Planned entry into service {p.eis}.",
                program=pid)
            add(p.launch_year, p.owner, "fallback", f"{names.get(pid, pid)}: engine fell back",
                f"{eng(p.segment, p.engine_requested)} was not committed by its maker in time, so {names.get(pid, pid)} flies the {flown}.",
                program=pid)
        else:
            add(p.launch_year, p.owner, "launch", what, f"Flies the {flown}. Planned entry into service {p.eis}.", program=pid)
        if p.cancelled_year is None:
            add(p.eis, p.owner, "eis", f"{names.get(pid, pid)} enters service", f"On the {flown}.", program=pid, round_=3)
            spans.append(dict(lane=p.owner, key=pid, start=p.launch_year, end=p.eis, kind="dev", label=f"{names.get(pid, pid)} development",
                              detail=f"{p.launch_year}–{p.eis}, on the {flown}"))
            spans.append(dict(lane=p.owner, key=pid, start=p.eis, end=cfg["years"]["end"], kind="service", label=f"{names.get(pid, pid)} in service",
                              detail=f"From {p.eis}"))
            maker = cfg["engine_options"][p.segment][p.engine].get("maker")
            if maker in M.active_suppliers(cfg):
                add(p.launch_year, maker, "win", f"Wins {names.get(pid, pid)}",
                    f"{names.get(pid, pid)} flies the {flown}: every engine on it, with no new engine programme.", program=pid)
                spans.append(dict(lane=maker, key=pid, start=p.eis, end=cfg["years"]["end"], kind="service", label=f"Engines for {names.get(pid, pid)}",
                                  detail=f"{flown}, from {p.eis}"))

    # Engine makers that lose an incumbent fleet when the new airframe flies someone else's engine
    for pid, p in w.programs.items():
        if p.cancelled_year is not None:
            continue
        maker = cfg["engine_options"][p.segment][p.engine].get("maker")
        for sup in M.active_suppliers(cfg):
            fit = cfg["suppliers"][sup]["incumbent_fit"][p.owner][p.segment]
            if sup != maker and fit > 0:
                fleet = {("boeing", "wb"): "787", ("airbus", "nb"): "A320neo", ("airbus", "wb"): "A350", ("boeing", "nb"): "737 MAX"}[(p.owner, p.segment)]
                add(p.launch_year, sup, "loss", f"Loses the {fleet} position",
                    f"{names.get(pid, pid)} flies another maker's engine, so its {fit:.0%} share of {fleet} deliveries goes to zero from {p.eis}.",
                    program=pid)

    # Engine programmes
    for spid, sp in sorted(w.sup_programs.items(), key=lambda kv: kv[1].launch_year):
        spc = cfg["suppliers"][sp.owner]["programs"][spid]
        add(sp.launch_year, sp.owner, "launch", f"{spc['label'][0].upper() + spc['label'][1:]} launched",
            f"{cfg['suppliers'][sp.owner]['terms'][sp.terms]['label'].capitalize()}"
            + (f", {spc['variants'][sp.variant]['label']}" if sp.variant and 'variants' in spc else "")
            + f"; engine ready {sp.launch_year + sp.dev_years + sp.slip_years}.", program=spid)
        if sp.cancelled_year is not None:
            add(sp.cancelled_year, sp.owner, "cancel", f"{spc['label'][0].upper() + spc['label'][1:]} cancelled",
                "No airframe selected it; development spend is sunk.", program=spid)
            spans.append(dict(lane=sp.owner, key=spid, start=sp.launch_year, end=sp.cancelled_year, kind="dev-cancel",
                              label=spc["label"], detail=f"{sp.launch_year}–{sp.cancelled_year}, cancelled"))
        else:
            spans.append(dict(lane=sp.owner, key=spid, start=sp.launch_year, end=sp.ready, kind="dev", label=spc["label"],
                              detail=f"{sp.launch_year}–{sp.ready}"))

    # One-time commitments
    for (sup, flag), yr in sorted(w.commit_years.items(), key=lambda kv: kv[1]):
        c = next(x for x in M.supplier_commitments(cfg, sup) if x["flag"] == flag)
        if c["kind"] == "upgrade":
            src = cfg["suppliers"].get(c.get("from"), {}).get("label")
            frm = f" from {src}" if src else ""
            fleet = {("boeing", "wb"): "787", ("airbus", "nb"): "A320neo", ("airbus", "wb"): "A350", ("boeing", "nb"): "737 MAX"}[(c["fit_side"], c["segment"])]
            add(yr, sup, "commit", c["label"][0].upper() + c["label"][1:],
                f"${c['capex_b']:.2f}B over {c['capex_years']} years; {c['fit_pp']:.0f} points of {fleet} deliveries move to it{frm} from {yr + c['lag_years']}.")
            spans.append(dict(lane=sup, key=flag, start=yr, end=yr + c["capex_years"], kind="commit", label=c["label"],
                              detail=f"Work {yr}–{yr + c['capex_years']}; share effect from {yr + c['lag_years']}"))
        else:
            add(yr, sup, "commit", c["label"][0].upper() + c["label"][1:], "")
    if w.rate_year is not None:
        rt = cfg["tactics"]["rate_increase"]
        add(w.rate_year, "boeing", "commit", "737 rate step committed",
            f"+{rt['share_pp']:.0f} points of narrowbody share from {w.rate_year + rt['lag_years']}; ${rt['capex_b']:.1f}B capex.")
    for t in w.poaching_turns:
        a, _ = M.turn_years(cfg, t)
        hit = any(e["player"] == "boeing" and e["year"] == a and e["label"].startswith("Talent") for e in w.cost_events)
        add(a, "airbus", "tactic", "Poaching (public)",
            "Airbus recruits Boeing engineers." + (" Boeing's fps development costs $0.75B more." if hit else " Boeing has nothing in development to disrupt."))
    for t in w.delay_turns:
        a, _ = M.turn_years(cfg, t)
        add(a, "airbus", "tactic", "Delay Tactics (covert)", "")

    # Public turning points the record shows, in the words of the outcome
    for r in hist:
        a, _ = M.turn_years(cfg, r["turn"])
        for side in M.players(cfg):
            disc = (r.get("statements", {}).get(side, {}) or {}).get("disclose") or []
            if disc:
                add(a, side, "disclose", "Disclosed", " · ".join(disc), public=True)
    ev.sort(key=lambda e: (e["year"], [l for l, _ in LANES].index(e["lane"]),
                           ["inject", "market", "launch", "fallback", "missed", "win", "loss", "commit", "tactic", "cancel", "eis", "milestone", "disclose"].index(e["kind"])))
    totals = {p: round(M.evaluate(cfg, w, with_objectives=False)[p]["delta_pv_b"], 1) for p in M.players(cfg)}
    return {"run": run_id, "scenario": cfg["scenario"]["title"], "years": [cfg["years"]["start"], 2050], "rounds": rounds,
            "lanes": [{"id": l, "label": n} for l, n in LANES], "events": ev, "spans": spans, "totals": totals}


PAGE = r"""<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Layout: a flight-strip board. One swimlane per player on a shared year axis, the three sealed
   rounds as bands, then the same events as a chronological log that the player filters drive. */
:root {
  --bg: #f4f6f9; --surface: #ffffff; --sunk: #e9edf3; --line: #d5dce6; --grid: #e3e8ef;
  --fg: #141c28; --muted: #556275; --faint: #8a95a5;
  --band: #eef2f7; --band-alt: #f8fafc;
  --boeing: #2a78d6; --airbus: #e34948; --pratt_whitney: #4a3aa7; --rolls_royce: #eda100; --cfm: #008300; --world: #556275;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --r: 6px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d; --band: #19212d; --band-alt: #131a24;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #008300; --world: #a3aebe;
  color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d; --band: #19212d; --band-alt: #131a24;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #008300; --world: #a3aebe;
  color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
.wrap { max-width: 1200px; margin: 0 auto; padding-inline: 16px; padding-block: 28px 64px; display: grid; gap: 28px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; line-height: 1.08; letter-spacing: .01em; margin: 0; text-wrap: balance; }
h1 { font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 700; }
h2 { font-size: 1.7rem; }
p { margin: 0; max-width: 72ch; }
.eyebrow { font: 500 .72rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.muted { color: var(--muted); } .small { font-size: .84rem; }
.head { display: grid; gap: 10px; }
.rounds { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
.rcard { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 12px 14px; display: grid; gap: 4px; min-width: 0; }
.rcard b { font: 600 1.15rem/1.1 var(--font-display); letter-spacing: .02em; }
.rcard span { font-size: .85rem; color: var(--muted); }
.scores { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: .9rem; }
.score { display: inline-flex; align-items: baseline; gap: 6px; white-space: nowrap; }
.score .v { font: 500 .9rem var(--font-mono); font-variant-numeric: tabular-nums; }
.dot { width: 10px; height: 10px; border-radius: 50%; background: var(--pc); display: inline-block; flex: none; align-self: center; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: .8rem; color: var(--muted); align-items: center; }
.legend svg { vertical-align: middle; margin-right: 5px; }
.board { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); overflow-x: auto; }
.board svg { display: block; min-width: 860px; width: 100%; height: auto; }
.board .tick { fill: var(--muted); font: 11px var(--font-mono); }
.board .lane-label { fill: var(--fg); font: 600 15px var(--font-display); letter-spacing: .02em; }
.board .band-label { fill: var(--muted); font: 500 10.5px var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
.board .mark { cursor: pointer; }
.board .mark:focus { outline: none; }
.board .mark:focus-visible .hit, .board .mark:hover .hit { stroke: var(--fg); stroke-width: 1.5; }
.board .dim { opacity: .18; }
.board .span-label { fill: var(--fg); font: 500 11px var(--font-body); pointer-events: none; }
.tip { position: fixed; z-index: 20; max-width: 320px; background: var(--fg); color: var(--bg); border-radius: var(--r); padding: 9px 11px;
       font-size: .82rem; line-height: 1.45; pointer-events: none; box-shadow: 0 6px 22px rgb(0 0 0 / .22); }
.tip b { display: block; font-weight: 600; margin-bottom: 2px; }
.tip .y { font: 500 .72rem var(--font-mono); opacity: .75; letter-spacing: .06em; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.chip { display: inline-flex; align-items: center; gap: 7px; font: 500 .85rem var(--font-body); padding: 7px 12px; border-radius: 999px;
        border: 1px solid var(--line); background: var(--surface); color: var(--fg); cursor: pointer; }
.chip[aria-pressed="false"] { color: var(--faint); background: transparent; }
.chip[aria-pressed="false"] .dot { background: var(--line); }
.chip:focus-visible { outline: 2px solid var(--fg); outline-offset: 2px; }
.toggle { display: inline-flex; align-items: center; gap: 6px; font-size: .85rem; color: var(--muted); margin-left: auto; }
.log { display: grid; gap: 22px; }
.round-block { display: grid; gap: 8px; }
.round-block h3 { font-size: 1.3rem; display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }
.round-block h3 small { font: 500 .78rem var(--font-mono); color: var(--muted); letter-spacing: .06em; }
.ev { display: grid; grid-template-columns: 52px 150px minmax(0, 1fr); gap: 4px 14px; padding: 10px 14px; background: var(--surface);
      border: 1px solid var(--line); border-radius: var(--r); align-items: baseline; }
.ev .yr { font: 500 .95rem var(--font-mono); font-variant-numeric: tabular-nums; }
.ev .who { display: inline-flex; gap: 7px; align-items: baseline; font-weight: 500; font-size: .9rem; min-width: 0; }
.ev .what { min-width: 0; display: grid; gap: 2px; }
.ev .what b { font-weight: 600; }
.ev .what span { color: var(--muted); font-size: .88rem; }
.kind { font: 500 .66rem/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted);
        border: 1px solid var(--line); border-radius: 3px; padding: 3px 5px; margin-right: 6px; white-space: nowrap; }
.ev.disclose { background: transparent; border-style: dashed; }
.foot { font-size: .82rem; color: var(--muted); display: grid; gap: 6px; }
@media (max-width: 640px) {
  .ev { grid-template-columns: 46px minmax(0, 1fr); }
  .ev .what { grid-column: 1 / -1; }
  .toggle { margin-left: 0; }
}
@media (prefers-reduced-motion: no-preference) { .tip { transition: opacity .12s; } }
</style>

<div class="wrap">
  <header class="head">
    <span class="eyebrow" id="eyebrow"></span>
    <h1>__TITLE__</h1>
    <p class="muted">Every public move and its consequence in the five-player game, 2026–2045, with the projection to 2050. Each round's orders were sealed and simultaneous, and engine makers' orders applied first, so an airframe that named an uncommitted engine fell back down the chain in the same year.</p>
    <div class="scores" id="scores" aria-label="Final delta PV by player"></div>
  </header>

  <section class="rounds" id="rounds" aria-label="Rounds"></section>

  <section style="display:grid;gap:10px" aria-label="Swimlane timeline">
    <h2>By player</h2>
    <div class="legend" id="legend"></div>
    <div class="board" id="board"></div>
    <p class="small muted">Hover or tab to a mark for details. Shaded bands are the three rounds; years after 2045 are the engine's projection with no further moves.</p>
  </section>

  <section style="display:grid;gap:14px" aria-label="Chronological log">
    <h2>Chronological log</h2>
    <div class="filters" id="filters">
      <label class="toggle"><input type="checkbox" id="showDisc"> Show disclosures</label>
    </div>
    <div class="log" id="log"></div>
  </section>

  <footer class="foot">
    <p>Source: the war-game engine's replay of run <span id="runid"></span>. Years, engines and fallbacks are the adjudicated record. Values are full-game delta PV in $B, at each player's own cost of capital, against a status quo in which nobody moves; volumes are stylised.</p>
  </footer>
</div>
<div class="tip" id="tip" hidden></div>

<script>
const DATA = __DATA__;
const LANE = Object.fromEntries(DATA.lanes.map(l => [l.id, l]));
const KIND = { inject: "Shock", market: "Market", launch: "Launch", fallback: "Engine fallback", win: "Engine win", missed: "Engine not committed", loss: "Fleet lost", commit: "Commitment",
               tactic: "Tactic", cancel: "Cancelled", eis: "Entry into service", milestone: "Milestone", disclose: "Disclosure" };
const col = id => `var(--${id})`;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
let active = new Set(DATA.lanes.map(l => l.id));
let showDisc = false;
try { const s = JSON.parse(localStorage.getItem("wg-timeline") || "null"); if (s) { active = new Set(s.active); showDisc = !!s.showDisc; } } catch (e) {}
const save = () => { try { localStorage.setItem("wg-timeline", JSON.stringify({ active: [...active], showDisc })); } catch (e) {} };

$("#eyebrow").textContent = `Run ${DATA.run} · five players · three sealed rounds`;
$("#runid").textContent = DATA.run;
$("#scores").innerHTML = DATA.lanes.filter(l => l.id in DATA.totals).map(l =>
  `<span class="score"><span class="dot" style="--pc:${col(l.id)}"></span>${esc(l.label)} <span class="v">${DATA.totals[l.id] >= 0 ? "+" : ""}${DATA.totals[l.id].toFixed(1)}</span></span>`).join("")
  + `<span class="score muted small">final delta PV, $B</span>`;
$("#rounds").innerHTML = DATA.rounds.map(r => `<div class="rcard"><span class="eyebrow">Round ${r.round}</span><b>${r.from}–${r.to}</b><span>Shock: ${esc(r.inject)}</span></div>`).join("");

// ---- swimlane board -------------------------------------------------------
const W = 1180, LW = 178, PADR = 18, TOP = 34, BOT = 28;
const ROWS = {}; DATA.spans.forEach(s => { const r = ROWS[s.lane] = ROWS[s.lane] || []; if (!r.includes(s.key)) r.push(s.key); });
const laneH = id => Math.max(60, 46 + 11 * (ROWS[id] || []).length);
const LANE_TOP = {}; { let y = TOP; DATA.lanes.forEach(l => { LANE_TOP[l.id] = y; y += laneH(l.id); }); }
const LANES_H = DATA.lanes.reduce((a, l) => a + laneH(l.id), 0);
const rowY = s => laneY(s.lane) + 36 + ROWS[s.lane].indexOf(s.key) * 11;
const [Y0, Y1] = DATA.years;
const H = TOP + LANES_H + BOT;
const sx = y => LW + (y - Y0) / (Y1 + 1 - Y0) * (W - LW - PADR);
const laneY = id => LANE_TOP[id];

function shape(kind, x, y, c) {
  const s = 7;
  switch (kind) {
    case "launch": return `<circle class="hit" cx="${x}" cy="${y}" r="${s}" fill="${c}"/>`;
    case "eis": return `<path class="hit" d="M${x} ${y - s - 2}L${x + s + 2} ${y}L${x} ${y + s + 2}L${x - s - 2} ${y}Z" fill="${c}"/>`;
    case "cancel": return `<g class="hit" stroke="${c}" stroke-width="3" stroke-linecap="round"><path d="M${x - s} ${y - s}L${x + s} ${y + s}M${x + s} ${y - s}L${x - s} ${y + s}"/></g><circle class="hit" cx="${x}" cy="${y}" r="${s + 3}" fill="transparent"/>`;
    case "fallback": return `<path class="hit" d="M${x} ${y + s + 1}L${x + s + 1} ${y - s}L${x - s - 1} ${y - s}Z" fill="var(--surface)" stroke="${c}" stroke-width="2.2"/>`;
    case "win": return `<path class="hit" d="M${x} ${y - s - 1}L${x + s + 1} ${y + s}L${x - s - 1} ${y + s}Z" fill="${c}"/>`;
    case "commit": return `<rect class="hit" x="${x - 3}" y="${y - s - 2}" width="6" height="${2 * s + 4}" rx="2" fill="${c}"/>`;
    case "tactic": return `<rect class="hit" x="${x - s + 1}" y="${y - s + 1}" width="${2 * s - 2}" height="${2 * s - 2}" rx="2" fill="var(--surface)" stroke="${c}" stroke-width="2.2" transform="rotate(45 ${x} ${y})"/>`;
    case "missed": return `<path class="hit" d="M${x} ${y + s + 1}L${x + s + 1} ${y - s}L${x - s - 1} ${y - s}Z" fill="var(--surface)" stroke="${c}" stroke-width="2.2" stroke-dasharray="3 2"/>`;
    case "loss": return `<circle class="hit" cx="${x}" cy="${y}" r="${s}" fill="var(--surface)" stroke="${c}" stroke-width="2.2"/><path d="M${x - 4} ${y}L${x + 4} ${y}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/>`;
    case "market": return `<rect class="hit" x="${x - s + 1}" y="${y - s + 1}" width="${2 * s - 2}" height="${2 * s - 2}" rx="3" fill="var(--surface)" stroke="${c}" stroke-width="2.2"/>`;
    case "inject": return `<circle class="hit" cx="${x}" cy="${y}" r="${s}" fill="${c}"/><path d="M${x + 1} ${y - 5}L${x - 3} ${y + 1}L${x + 1} ${y + 1}L${x - 1} ${y + 5}" stroke="var(--surface)" stroke-width="1.6" fill="none" stroke-linejoin="round"/>`;
    case "milestone": return `<circle class="hit" cx="${x}" cy="${y}" r="${s}" fill="var(--surface)" stroke="${c}" stroke-width="2.2" stroke-dasharray="3 2"/>`;
    default: return `<circle class="hit" cx="${x}" cy="${y}" r="${s - 1}" fill="var(--surface)" stroke="${c}" stroke-width="2.2"/>`;
  }
}

function drawBoard() {
  const g = [];
  // round bands
  DATA.rounds.forEach((r, i) => {
    g.push(`<rect x="${sx(r.from)}" y="${TOP - 8}" width="${sx(r.to + 1) - sx(r.from)}" height="${LANES_H + 8}" fill="${i % 2 ? "var(--band-alt)" : "var(--band)"}"/>`);
    g.push(`<text class="band-label" x="${sx(r.from) + 6}" y="${TOP - 14}">Round ${r.round} · ${r.from}–${r.to}</text>`);
  });
  const last = DATA.rounds[DATA.rounds.length - 1].to + 1;
  g.push(`<text class="band-label" x="${sx(last) + 6}" y="${TOP - 14}">Projection</text>`);
  // grid + axis
  for (let y = Y0; y <= Y1; y++) {
    const x = sx(y), major = y % 5 === 0 || y === Y0;
    g.push(`<line x1="${x}" x2="${x}" y1="${TOP - 8}" y2="${H - BOT}" stroke="var(--grid)" stroke-width="${major ? 1 : 0.5}"/>`);
    if (major) g.push(`<text class="tick" x="${x + 3}" y="${H - 10}">${y}</text>`);
  }
  // lanes
  DATA.lanes.forEach((l, i) => {
    const y = laneY(l.id), h = laneH(l.id), dim = active.has(l.id) ? "" : "dim";
    g.push(`<line x1="0" x2="${W}" y1="${y + h}" y2="${y + h}" stroke="var(--line)" stroke-width="1"/>`);
    g.push(`<g class="${dim}"><rect x="12" y="${y + 9}" width="5" height="18" rx="2" fill="${col(l.id)}"/>`
         + `<text class="lane-label" x="24" y="${y + 23}">${esc(l.label)}</text></g>`);
  });
  // spans
  const tips = [];
  DATA.spans.forEach((s, i) => {
    const y = rowY(s), c = col(s.lane), dim = active.has(s.lane) ? "" : "dim";
    const x0 = sx(s.start), x1 = Math.max(sx(Math.min(s.end, Y1 + 1)), x0 + 4);
    let el;
    if (s.kind === "dev" || s.kind === "dev-cancel")
      el = `<rect class="hit" x="${x0}" y="${y}" width="${x1 - x0}" height="8" rx="4" fill="${c}" opacity="${s.kind === "dev" ? 0.95 : 0.5}"/>`
         + (s.kind === "dev-cancel" ? `<path d="M${x1 - 1} ${y - 2}L${x1 - 1} ${y + 10}" stroke="${c}" stroke-width="2"/>` : "");
    else if (s.kind === "service")
      el = `<rect class="hit" x="${x0}" y="${y + 1}" width="${x1 - x0}" height="6" rx="3" fill="${c}" opacity=".42"/>`;
    else if (s.kind === "commit")
      el = `<rect class="hit" x="${x0}" y="${y + 2}" width="${x1 - x0}" height="4" rx="2" fill="${c}" opacity=".6"/>`;
    else
      el = `<rect class="hit" x="${x0}" y="${y - 6}" width="${x1 - x0}" height="18" rx="4" fill="var(--sunk)" stroke="var(--line)"/>`
         + `<text class="span-label" x="${x0 + 6}" y="${y + 7}">${esc(s.label)}</text>`;
    tips.push({ title: s.label, detail: s.detail, year: s.kind === "service" ? `from ${s.start}` : `${s.start}–${s.end}` });
    g.push(`<g class="mark ${dim}" tabindex="0" data-tip="s${i}" aria-label="${esc(s.label)}: ${esc(s.detail)}">${el}</g>`);
  });
  // events (stack marks sharing a lane and year)
  const count = {}, seen = {};
  DATA.events.forEach(e => { if (e.kind !== "disclose") count[e.lane + e.year] = (count[e.lane + e.year] || 0) + 1; });
  const cell = sx(Y0 + 1) - sx(Y0);
  DATA.events.forEach((e, i) => {
    if (e.kind === "disclose") return;
    const key = e.lane + e.year, n = (seen[key] = (seen[key] || 0) + 1) - 1, k = count[key];
    const step = Math.min(15, (cell - 4) / Math.max(1, k - 1));
    const x = sx(e.year) + cell / 2 + (n - (k - 1) / 2) * (k > 1 ? step : 0), y = laneY(e.lane) + 18;
    const dim = active.has(e.lane) ? "" : "dim";
    g.push(`<g class="mark ${dim}" tabindex="0" data-tip="e${i}" aria-label="${e.year} ${esc(LANE[e.lane].label)}: ${esc(e.title)}">${shape(e.kind, x, y, col(e.lane))}</g>`);
  });
  $("#board").innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Swimlane timeline of the war game by player, ${Y0} to ${Y1}">${g.join("")}</svg>`;
  window.__spanTips = tips;
}

// legend
const LEG = [["launch", "Launch"], ["fallback", "Engine fell back"], ["missed", "Asked-for engine not committed"], ["win", "Engine maker wins an airframe"],
             ["loss", "Engine maker loses a fleet"], ["eis", "Entry into service"],
             ["cancel", "Cancelled"], ["commit", "One-time commitment"], ["tactic", "Poaching"], ["inject", "Shock"], ["market", "Market reaction"], ["milestone", "Milestone"]];
$("#legend").innerHTML = LEG.map(([k, t]) => `<span><svg width="20" height="20" viewBox="-10 -10 20 20" aria-hidden="true">${shape(k, 0, 0, "var(--muted)")}</svg>${t}</span>`).join("")
  + `<span><svg width="28" height="12" aria-hidden="true"><rect x="1" y="1" width="26" height="10" rx="3" fill="var(--muted)" opacity=".9"/></svg>Development</span>`
  + `<span><svg width="28" height="12" aria-hidden="true"><rect x="1" y="3" width="26" height="6" rx="3" fill="var(--muted)" opacity=".32"/></svg>In service</span>`;

// tooltip
const tip = $("#tip");
function showTip(el, cx, cy) {
  const id = el.dataset.tip;
  const d = id[0] === "e" ? DATA.events[+id.slice(1)] : window.__spanTips[+id.slice(1)];
  const year = id[0] === "e" ? d.year : d.year;
  tip.innerHTML = `<span class="y">${year}${id[0] === "e" ? " · " + esc(LANE[d.lane].label) + " · " + esc(KIND[d.kind] || d.kind) : ""}</span><b>${esc(d.title)}</b>${esc(d.detail || "")}`;
  tip.hidden = false;
  const r = tip.getBoundingClientRect();
  let x = cx + 14, y = cy + 14;
  if (x + r.width > innerWidth - 8) x = cx - r.width - 14;
  if (y + r.height > innerHeight - 8) y = cy - r.height - 14;
  tip.style.left = Math.max(8, x) + "px"; tip.style.top = Math.max(8, y) + "px";
}
$("#board").addEventListener("mousemove", ev => { const m = ev.target.closest(".mark"); if (m) showTip(m, ev.clientX, ev.clientY); else tip.hidden = true; });
$("#board").addEventListener("mouseleave", () => tip.hidden = true);
$("#board").addEventListener("focusin", ev => { const m = ev.target.closest(".mark"); if (m) { const r = m.getBoundingClientRect(); showTip(m, r.right, r.top); } });
$("#board").addEventListener("focusout", () => tip.hidden = true);

// filters + log
function drawFilters() {
  const chips = DATA.lanes.map(l => `<button class="chip" type="button" id="f-${l.id}" aria-pressed="${active.has(l.id)}" data-lane="${l.id}"><span class="dot" style="--pc:${col(l.id)}"></span>${esc(l.label)}</button>`).join("");
  const tog = $("#filters .toggle");
  $("#filters").innerHTML = chips;
  $("#filters").appendChild(tog);
  $("#showDisc").checked = showDisc;
}
function drawLog() {
  $("#log").innerHTML = DATA.rounds.map(r => {
    const items = DATA.events.filter(e => e.round === r.round && active.has(e.lane) && (showDisc || e.kind !== "disclose"));
    const rows = items.map(e => `<div class="ev ${e.kind}"><span class="yr">${e.year}</span>`
      + `<span class="who"><span class="dot" style="--pc:${col(e.lane)}"></span>${esc(LANE[e.lane].label)}</span>`
      + `<span class="what"><b><span class="kind">${esc(KIND[e.kind] || e.kind)}</span>${esc(e.title)}</b>${e.detail ? `<span>${esc(e.detail)}</span>` : ""}</span></div>`).join("");
    return `<div class="round-block"><h3>Round ${r.round} <small>${r.from}–${r.to} · ${esc(r.inject)}</small></h3>${rows || '<p class="muted small">No events for the selected players.</p>'}</div>`;
  }).join("");
}
$("#filters").addEventListener("click", ev => {
  const b = ev.target.closest(".chip"); if (!b) return;
  const id = b.dataset.lane;
  if (active.has(id) && active.size > 1) active.delete(id); else active.add(id);
  save(); drawFilters(); drawBoard(); drawLog();
});
$("#filters").addEventListener("change", ev => { if (ev.target.id === "showDisc") { showDisc = ev.target.checked; save(); drawLog(); } });
drawFilters(); drawBoard(); drawLog();
</script>
"""


def main():
    run_id, out = sys.argv[1], sys.argv[2]
    title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else "War Game 2045 Timeline"
    data = build_data(run_id)
    page = PAGE.replace("__TITLE__", html.escape(title)).replace(
        "__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    with open(out, "w") as f:
        f.write(page)
    print(out, len(page), len(data["events"]), "events", len(data["spans"]), "spans")


if __name__ == "__main__":
    main()
