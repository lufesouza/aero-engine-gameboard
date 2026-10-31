"""Build do_nothing_tuner.html: a one-page tool to tune the Do Nothing case by hand (total demand, the 737 MAX's rate and
phase-out, Airbus's rates and extra lines, COMAC and a new entrant) before the scenario goes into the game.

The page runs the game's own supply-and-demand rules for Do Nothing (supply_demand.year_rows: firm orders netted inside
demand, Boeing's preference falling 1 point a year while NGSA flies alone, the slack floor, the overflow between the two
makers, a tenth of the waiting customers dropping out each year, Airbus's capacity response), in JavaScript, plus the
switches of build_scenario.py (MAX phase-out, Airbus extra lines, a COMAC and entrant tier). Presets: the game's Do Nothing
as played (all switches off) and the manual build. test_tuner.py checks both against the Python, year by year.

  python3 make_tuner_html.py            # writes ../../do_nothing_tuner.html
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_scenario as B  # noqa: E402

D, L, M, SD = B.D, B.L, B.M, B.SD
OUT = os.path.join(HERE, "..", "..", "do_nothing_tuner.html")
YEARS = list(range(2026, 2061))


def data():
    page = D.PAGE
    game = {y: (r + g) for y, r, g in zip(D.GAME["years"], D.GAME["replacements"], D.GAME["growth"])}
    curves = {}
    for n in D.NS:                                           # the spliced curves the analysis uses (whole market)
        c = json.load(open(os.path.join(D.HERE, "curves", "page_N%s.json" % n)))
        cv = {y: r + g for y, r, g in zip(c["years"], c["replacements"], c["growth"])}
        curves["N" + n] = [cv[y] for y in YEARS]
    curves["game"] = [game[min(y, max(game))] for y in YEARS]
    with L.patched(**D.demand_kw("0")):
        st, cv = L.grid_states(L.PLAN_DN)[1]
        eis, a, b, dt = M.af_inputs(st, cv)
        cell = M.eval_cell(eis, a, b, trace=True)
        ser = M.af_series(st, cell, eis, dt)
        pref = {r["year"]: r["boeing"]["nb_share"] for r in ser["years"]}
        a320 = [SD.airbus_capacity(st, y)[0] for y in YEARS]
        ngsa = [SD.airbus_capacity(st, y)[1] for y in YEARS]
        ngsa_eis = st["prog"]["ngsa"]["eis"]
        max_path = [SD.max_path(y) / 12.0 for y in YEARS]
    df = {r["year"]: r["df_b"] for r in ser["years"]}
    o = SD.options()
    dem = SD.inputs()["demand"]
    return {"years": YEARS, "curves": curves, "board_pref": [pref[y] for y in YEARS], "a320": a320, "ngsa": ngsa,
            "a320_rate": SD.inputs()["airbus"]["a320_rate_no_ngsa"], "ngsa_peak": max(r for _, r in SD.inputs()["airbus"]["ngsa"]),
            "ngsa_eis": ngsa_eis, "max_path": max_path, "df": [df[y] for y in YEARS],
            "firm": list(SD.firm_backlog()), "flex": SD.flex(), "lapse": dem["lapse_per_year"], "class_share": dem["class_share"],
            "pp_after_ngsa": o["boeing_pp_after_ngsa"], "slack": bool(o["boeing_takes_airbus_slack"]),
            "unit737": 48.0 * 0.08 / 1000.0,
            "build": {"max_phase": B.MAX_PHASE, "airbus_extra": B.AIRBUS_EXTRA, "comac": B.COMAC, "entrant": B.ENTRANT,
                      "willing": B.WILLING}}


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Do Nothing Tuner</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#f4f6f9;--surface:#fff;--sunk:#eef2f7;--line:#d5dce6;--grid:#e3e8ef;--fg:#141c28;--muted:#556275;--faint:#8a95a5;
--boeing:#2a78d6;--airbus:#eb6834;--comac:#c03b5b;--entrant:#17a06f;--demand:#141c28;--ref:#9dc0ea;--r:8px;
--sans:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f141c;--surface:#161d28;--sunk:#1d2633;--line:#2b3646;--grid:#222c3a;
--fg:#e7ecf3;--muted:#a3aebe;--faint:#6f7b8d;--boeing:#3987e5;--airbus:#d95926;--comac:#d0506f;--entrant:#199e70;--demand:#e7ecf3;--ref:#5d8fd0;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f141c;--surface:#161d28;--sunk:#1d2633;--line:#2b3646;--grid:#222c3a;--fg:#e7ecf3;--muted:#a3aebe;--faint:#6f7b8d;
--boeing:#3987e5;--airbus:#d95926;--comac:#d0506f;--entrant:#199e70;--demand:#e7ecf3;--ref:#5d8fd0;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 var(--sans)}
.wrap{max-width:1320px;margin:0 auto;padding:18px 16px 40px}
h1{font:600 1.45rem/1.2 var(--sans);margin:0 0 4px}.sub{color:var(--muted);margin:0 0 14px;max-width:110ch}
.eyebrow{font:500 .7rem/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.layout{display:grid;grid-template-columns:340px 1fr;gap:14px;align-items:start}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px}
.controls{position:sticky;top:10px;max-height:calc(100vh - 20px);overflow:auto}
fieldset{border:0;margin:0 0 10px;padding:0 0 10px;border-bottom:1px solid var(--line)}fieldset:last-of-type{border-bottom:0}
legend{font:600 .78rem/1.3 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:0;margin-bottom:6px}
.ctl{display:grid;grid-template-columns:1fr 64px;gap:2px 8px;align-items:center;margin:6px 0}
.ctl label{font-size:.84rem;grid-column:1/3;display:flex;justify-content:space-between;gap:6px}
.ctl label span.u{color:var(--faint);font-size:.76rem}
.ctl input[type=range]{width:100%;accent-color:var(--boeing)}
select{font:500 .84rem var(--sans)!important}
.ctl input[type=number],select{width:100%;font:500 .84rem var(--mono);color:var(--fg);background:var(--sunk);border:1px solid var(--line);border-radius:5px;padding:3px 5px}
select{grid-column:1/3}
.row5{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}.row5 div{font:500 .7rem var(--mono);color:var(--muted);text-align:center}
.row5 input{width:100%;font:500 .8rem var(--mono);color:var(--fg);background:var(--sunk);border:1px solid var(--line);border-radius:5px;padding:3px 2px;text-align:center}
.chk{display:flex;gap:6px;align-items:center;font-size:.84rem;margin:4px 0}
.btns{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
button{font:500 .8rem var(--sans);color:var(--fg);background:var(--sunk);border:1px solid var(--line);border-radius:6px;padding:5px 9px;cursor:pointer}
button:hover{border-color:var(--faint)}button.primary{background:var(--boeing);border-color:var(--boeing);color:#fff}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-bottom:12px}
.tile .k{font:500 .66rem/1.3 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.tile .v{font:600 1.25rem/1.25 var(--sans);margin-top:3px}.tile .d{font-size:.76rem;color:var(--muted)}
.ctitle{font-weight:600;margin:0 0 4px}.cap{font-size:.8rem;color:var(--muted);margin:6px 0 0}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.8rem;color:var(--muted);margin:2px 0 6px}
.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.legend i.ln{height:2px;width:16px;border-radius:1px;vertical-align:3px}
svg{width:100%;height:auto;display:block}svg text{font:11px var(--mono);fill:var(--muted)}
.gridl{stroke:var(--grid)}.stack{display:grid;gap:12px}
.tip{position:fixed;pointer-events:none;display:none;background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:7px 9px;
font-size:.78rem;box-shadow:0 6px 18px rgba(0,0,0,.18);z-index:9;min-width:180px}
.tip b{font:600 .8rem var(--mono)}.tip .r{display:flex;justify-content:space-between;gap:10px}
table{border-collapse:collapse;width:100%;font-size:.8rem}th,td{padding:4px 6px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th{font:500 .68rem var(--mono);text-transform:uppercase;letter-spacing:.04em;color:var(--muted);background:var(--sunk);position:sticky;top:0}
td:first-child,th:first-child{text-align:left}.scroll{overflow:auto;max-height:420px}
details summary{cursor:pointer;color:var(--muted);font-size:.84rem}
textarea{width:100%;height:110px;font:12px var(--mono);background:var(--sunk);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:6px}
.note{font-size:.78rem;color:var(--muted)}
footer{margin-top:16px;font-size:.76rem;color:var(--muted)}
@media (max-width:900px){.layout{grid-template-columns:1fr}.controls{position:static;max-height:none}}
</style></head><body><div class="wrap">
<p class="eyebrow">Boeing Product Development · dash-2050-cons · BOEING PROPRIETARY</p>
<h1>Do Nothing tuner</h1>
<p class="sub">Set total demand and each maker's rates; the page re-runs the game's own Do Nothing supply-and-demand rules (Airbus launches NGSA in __NGSA__)
with the MAX phase-out, Airbus's extra lines, COMAC and a new entrant. When it looks right, copy the settings and send them back: they go into the game as they are.</p>
<div class="layout">
<div class="panel controls" id="controls">
<div class="btns"><button id="pGame">Game's Do Nothing (as played)</button><button id="pBuild" class="primary">Manual build</button><button id="pProt">COMAC and entrant protected</button></div>
<fieldset><legend>Total demand (737/A320 class)</legend>
<div class="ctl"><label for="curve">Demand curve</label><select id="curve">
<option value="N0">Page: retiring as chapter 1 sets out</option><option value="N1">Page: retiring 1 year later</option><option value="N2">Page: retiring 2 years later</option>
<option value="N3">Page: retiring 3 years later</option><option value="N4">Page: retiring 4 years later</option><option value="game">Game's conservative curve</option></select></div>
<div class="ctl"><label for="dA">Level 2026-2044 <span class="u">% of curve</span></label><input type="range" id="dA" min="50" max="150" step="1"><input type="number" data-for="dA"></div>
<div class="ctl"><label for="dB">Level 2045-2060 <span class="u">% of curve</span></label><input type="range" id="dB" min="50" max="150" step="1"><input type="number" data-for="dB"></div>
</fieldset>
<fieldset><legend>Boeing 737 MAX</legend>
<div class="ctl"><label for="maxRate">Rate from 2030 <span class="u">a month</span></label><input type="range" id="maxRate" min="30" max="75" step="0.5"><input type="number" data-for="maxRate"></div>
<label class="chk"><input type="checkbox" id="phase"> Phase the MAX out</label>
<div class="ctl"><label for="phStart">Phase-out starts <span class="u">year</span></label><input type="range" id="phStart" min="2035" max="2059" step="1"><input type="number" data-for="phStart"></div>
<div class="ctl"><label for="phEnd">None built from <span class="u">year</span></label><input type="range" id="phEnd" min="2036" max="2070" step="1"><input type="number" data-for="phEnd"></div>
</fieldset>
<fieldset><legend>Airbus</legend>
<div class="ctl"><label for="a320Rate">A320neo rate before NGSA <span class="u">a month</span></label><input type="range" id="a320Rate" min="50" max="100" step="1"><input type="number" data-for="a320Rate"></div>
<div class="ctl"><label for="ngsaPeak">NGSA peak rate <span class="u">a month</span></label><input type="range" id="ngsaPeak" min="50" max="140" step="1"><input type="number" data-for="ngsaPeak"></div>
<div class="ctl"><label for="xFrom">Extra lines from <span class="u">year</span></label><input type="range" id="xFrom" min="2030" max="2060" step="1"><input type="number" data-for="xFrom"></div>
<div class="ctl"><label for="xStep">Extra added each year <span class="u">a month</span></label><input type="range" id="xStep" min="0" max="20" step="0.5"><input type="number" data-for="xStep"></div>
<div class="ctl"><label for="xCap">Extra at most <span class="u">a month</span></label><input type="range" id="xCap" min="0" max="60" step="1"><input type="number" data-for="xCap"></div>
<div class="ctl"><label for="resp">Capacity response when short <span class="u">% a year</span></label><input type="range" id="resp" min="0" max="5" step="0.1"><input type="number" data-for="resp"></div>
</fieldset>
<fieldset><legend>COMAC</legend>
<div class="note">Capacity, aircraft a year (straight lines between)</div>
<div class="row5"><div>2026</div><div>2030</div><div>2035</div><div>2045</div><div>2050+</div>
<input type="number" id="c2026"><input type="number" id="c2030"><input type="number" id="c2035"><input type="number" id="c2045"><input type="number" id="c2050"></div>
<div class="ctl"><label for="cProt">Sells first, whoever else has slots <span class="u">% of capacity</span></label><input type="range" id="cProt" min="0" max="100" step="5"><input type="number" data-for="cProt"></div>
</fieldset>
<fieldset><legend>New entrant (Embraer-like)</legend>
<div class="ctl"><label for="eEis">Enters service <span class="u">year</span></label><input type="range" id="eEis" min="2032" max="2055" step="1"><input type="number" data-for="eEis"></div>
<div class="ctl"><label for="ePeak">Peak rate <span class="u">a month</span></label><input type="range" id="ePeak" min="0" max="60" step="1"><input type="number" data-for="ePeak"></div>
<div class="ctl"><label for="eYears">Years to peak <span class="u">years</span></label><input type="range" id="eYears" min="1" max="15" step="1"><input type="number" data-for="eYears"></div>
<div class="ctl"><label for="eShare">Wins of new demand, up to capacity <span class="u">%</span></label><input type="range" id="eShare" min="0" max="30" step="0.5"><input type="number" data-for="eShare"></div>
</fieldset>
<fieldset><legend>Customers nobody else can serve</legend>
<div class="ctl"><label for="willing">Take a free COMAC or entrant slot <span class="u">%</span></label><input type="range" id="willing" min="0" max="100" step="5"><input type="number" data-for="willing"></div>
</fieldset>
<details><summary>Settings to send back</summary><textarea id="settings" readonly></textarea><button id="copy">Copy settings</button></details>
</div>
<div>
<div class="tiles" id="tiles"></div>
<div class="stack">
<div class="panel"><p class="ctitle" id="t1"></p>
<div class="legend"><span><i style="background:var(--boeing)"></i>Boeing 737 MAX</span><span><i style="background:var(--airbus)"></i>Airbus</span>
<span><i style="background:var(--comac)"></i>COMAC</span><span><i style="background:var(--entrant)"></i>New entrant</span><span><i class="ln" style="background:var(--demand)"></i>Demand</span></div>
<div id="c1"></div><p class="cap">Aircraft delivered a year. Demand is new customers in the year (firm orders inside it); deliveries above it in a year serve customers who waited.</p></div>
<div class="panel"><p class="ctitle" id="t2"></p>
<div class="legend"><span><i class="ln" style="background:var(--boeing)"></i>737s sold, this setting</span><span><i class="ln" style="background:var(--ref)"></i>737s sold, the game's Do Nothing as played</span><span><i class="ln" style="background:var(--faint)"></i>737 capacity, this setting</span></div>
<div id="c2"></div></div>
<div class="panel"><details><summary>Year by year</summary><div class="scroll" id="tbl"></div></details></div>
</div></div></div>
<footer>BOEING PROPRIETARY. Built by analysis/max_phaseout/make_tuner_html.py (run dash-2050-cons). The rules are the game's supply_demand.year_rows for Do Nothing,
checked year by year against the Python (test_tuner.py). "737 profit" is indicative: 737s sold against the game's Do Nothing x $3.84M an aircraft, discounted
at 10.5% to 2026; the game run values it properly.</footer>
</div><div class="tip" id="tip"></div>
<script>
const G = __DATA__;
const Y = G.years, N = Y.length, IDX = y => y - Y[0];
const DEF = {curve: "N0", dA: 100, dB: 100, maxRate: 57, phase: false, phStart: 2045, phEnd: 2060, a320Rate: G.a320_rate, ngsaPeak: G.ngsa_peak,
  xFrom: 2045, xStep: 0, xCap: 0, resp: 1.0, c2026: 0, c2030: 0, c2035: 0, c2045: 0, c2050: 0, cProt: 0, eEis: 2040, ePeak: 0, eYears: 6, eShare: 0, willing: 100};
const B = G.build;
const P_BUILD = Object.assign({}, DEF, {phase: true, phStart: B.max_phase.start, phEnd: B.max_phase.gone, xFrom: B.airbus_extra.from,
  xStep: B.airbus_extra.step_per_year, xCap: B.airbus_extra.cap, c2026: B.comac["2026"], c2030: B.comac["2030"], c2035: B.comac["2035"],
  c2045: B.comac["2045"], c2050: B.comac["2050"], eEis: B.entrant.eis, ePeak: B.entrant.peak_a_month, eYears: B.entrant.years_to_peak,
  willing: B.willing * 100});
const P_PROT = Object.assign({}, P_BUILD, {cProt: 100, eShare: 8});
const interp = (pts, y) => { const ks = Object.keys(pts).map(Number).sort((a, b) => a - b);
  if (y < ks[0]) return 0; if (y >= ks[ks.length - 1]) return pts[ks[ks.length - 1]];
  for (let i = 0; i + 1 < ks.length; i++) { const a = ks[i], b = ks[i + 1]; if (y >= a && y <= b) return pts[a] + (pts[b] - pts[a]) * (y - a) / (b - a); } return 0; };

function caps(p) {
  const out = [];
  for (const y of Y) {
    const i = IDX(y);
    let m = (y < 2030 ? Math.min(G.max_path[i], p.maxRate) : p.maxRate) * 12;
    if (p.phase && y >= p.phStart) m = m * Math.max(0, (p.phEnd - y) / (p.phEnd - p.phStart + 1));
    const a3 = G.a320[i] * p.a320Rate / G.a320_rate, ng = G.ngsa[i] * p.ngsaPeak / G.ngsa_peak;
    const xa = y < p.xFrom ? 0 : 12 * Math.min(p.xCap, p.xStep * (y - p.xFrom + 1));
    const cc = interp({2025.999: 0, 2026: p.c2026, 2030: p.c2030, 2035: p.c2035, 2045: p.c2045, 2050: p.c2050}, y);
    const ce = y < p.eEis ? 0 : 12 * p.ePeak * Math.min(1, (y - p.eEis + 1) / p.eYears);
    out.push({m, a3, ng, xa, cc, ce});
  }
  return out;
}

function deliveries(bp, d, capB, capA, fx, backB, backA, lapse, firmB, firmA) {
  const fb = Math.min(firmB, capB), fa = Math.min(firmA, capA);
  const cb = capB - fb, ca = capA - fa;
  const wb = bp * d, wa = (1 - bp) * d;
  const qb = Math.min(wb + backB, cb), qa = Math.min(wa + backA, ca);
  const ub = wb + backB - qb, ua = wa + backA - qa;
  const toB = Math.min(fx * ua, cb - qb), toA = Math.min(fx * ub, ca - qa);
  return {firmLeftB: firmB - fb, firmLeftA: firmA - fa, delB: fb + qb + toB, delA: fa + qa + toA, unB: ub - toA, unA: ua - toB};
}

function run(p) {
  const C = caps(p), dem = G.curves[p.curve];
  let kb = G.firm[0], ka = G.firm[1], cbk = 0, cak = 0, bb = 0, ba = 0, mA = 1;
  const rows = [];
  for (const y of Y) {
    const i = IDX(y), c = C[i];
    const a3 = c.a3 * mA, ng = c.ng * mA, capA = a3 + ng + c.xa;
    const gross = dem[i] * G.class_share * (y < 2045 ? p.dA : p.dB) / 100;
    const need = Math.min(gross, kb + ka);
    const nb = kb + ka > 0 ? need * kb / (kb + ka) : 0, na = need - nb;
    kb -= nb; ka -= na;
    const fbIn = cbk + nb, faIn = cak + na;
    let d = gross - need;
    // COMAC's protected sales and the entrant's won share come off the top of new demand
    const pc = Math.min(c.cc * p.cProt / 100, d); d -= pc;
    const pe = Math.min(c.ce, d * p.eShare / 100); d -= pe;
    const base = y >= G.ngsa_eis ? Math.max(0, 0.40 - G.pp_after_ngsa / 100 * (y - G.ngsa_eis + 1)) : G.board_pref[i];
    const freeA = Math.max(0, capA - Math.min(faIn, capA) - ba);
    let pref = base;
    if (G.slack && d > 0) pref = Math.min(1, Math.max(base, 1 - freeA / d));
    const r = deliveries(pref, d, c.m, capA, G.flex, bb, ba, G.lapse, fbIn, faIn);
    // the third tier: unserved customers take a free COMAC or entrant slot
    const remC = Math.max(0, c.cc - pc), remE = Math.max(0, c.ce - pe);
    const take = Math.min(p.willing / 100 * (r.unB + r.unA), remC + remE);
    const tb = r.unB + r.unA > 0 ? take * r.unB / (r.unB + r.unA) : 0, ta = take - tb;
    const tC = remC + remE > 0 ? take * remC / (remC + remE) : 0, tE = take - tC;
    bb = (r.unB - tb) * (1 - G.lapse); ba = (r.unA - ta) * (1 - G.lapse);
    const lost = (r.unB - tb + r.unA - ta) * G.lapse;
    cbk = r.firmLeftB; cak = r.firmLeftA;
    if (p.resp > 0 && (1 - base) * d > freeA + 1e-9) mA *= 1 + p.resp / 100;
    rows.push({y, demand: gross, capMax: c.m, max: r.delB, capA, airbus: r.delA, comac: pc + tC, entrant: pe + tE, capC: c.cc, capE: c.ce, lost, pref});
  }
  return rows;
}

// ─── state and controls ───
const IDS = Object.keys(DEF);
let P = Object.assign({}, P_BUILD);
function readControls() {
  for (const k of IDS) {
    const el = document.getElementById(k); if (!el) continue;
    if (el.type === "checkbox") P[k] = el.checked; else if (el.tagName === "SELECT") P[k] = el.value; else P[k] = +el.value;
  }
}
function writeControls() {
  for (const k of IDS) {
    const el = document.getElementById(k); if (!el) continue;
    if (el.type === "checkbox") el.checked = !!P[k]; else el.value = P[k];
    const n = document.querySelector(`input[data-for="${k}"]`); if (n) n.value = P[k];
  }
}
document.querySelectorAll('#controls input, #controls select').forEach(el => {
  const ev = el.type === "range" ? "input" : "change";
  el.addEventListener(ev, () => {
    if (el.dataset.for) document.getElementById(el.dataset.for).value = el.value;
    else { const n = document.querySelector(`input[data-for="${el.id}"]`); if (n) n.value = el.value; }
    readControls(); render();
  });
});
document.getElementById("pGame").onclick = () => { P = Object.assign({}, DEF); writeControls(); render(); };
document.getElementById("pBuild").onclick = () => { P = Object.assign({}, P_BUILD); writeControls(); render(); };
document.getElementById("pProt").onclick = () => { P = Object.assign({}, P_PROT); writeControls(); render(); };
document.getElementById("copy").onclick = () => { const t = document.getElementById("settings"); t.select();
  try { navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand && document.execCommand("copy"); } };

// ─── charts ───
const fmt = v => Math.round(v).toLocaleString("en-US");
const tip = document.getElementById("tip");
function showTip(e, html) { tip.innerHTML = html; tip.style.display = "block";
  const w = tip.offsetWidth, h = tip.offsetHeight; let x = e.clientX + 14, yy = e.clientY + 14;
  if (x + w > innerWidth - 8) x = e.clientX - w - 14; if (yy + h > innerHeight - 8) yy = e.clientY - h - 14;
  tip.style.left = x + "px"; tip.style.top = yy + "px"; }
function hideTip() { tip.style.display = "none"; }
function frame(w, h, yMax, step, label) {
  const L = 52, R = 12, T = 12, Bm = 30;
  const sx = y => L + (y - Y[0] + 0.5) / N * (w - L - R), sy = v => T + (1 - v / yMax) * (h - T - Bm);
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}">`;
  for (let v = 0; v <= yMax + 1e-9; v += step) s += `<line class="gridl" x1="${L}" x2="${w - R}" y1="${sy(v)}" y2="${sy(v)}"/><text x="${L - 6}" y="${sy(v) + 4}" text-anchor="end">${fmt(v)}</text>`;
  for (const y of Y) if (y % 5 === 0) s += `<text x="${sx(y)}" y="${h - 10}" text-anchor="middle">${y}</text>`;
  return {s, sx, sy, L, R, T, Bm, bw: (w - L - R) / N};
}
function chart1(rows) {
  const w = 900, h = 360, top = Math.max(...rows.map(r => Math.max(r.demand, r.max + r.airbus + r.comac + r.entrant)));
  const yMax = Math.ceil(top / 500) * 500, f = frame(w, h, yMax, 500, "Deliveries by maker and demand");
  let s = f.s;
  rows.forEach(r => { let acc = 0; const x = f.sx(r.y) - f.bw * 0.4;
    for (const [k, c] of [["max", "boeing"], ["airbus", "airbus"], ["comac", "comac"], ["entrant", "entrant"]]) {
      const v = r[k]; if (v <= 0.01) continue;
      s += `<rect x="${x}" width="${f.bw * 0.8}" y="${f.sy(acc + v)}" height="${Math.max(0, f.sy(acc) - f.sy(acc + v))}" fill="var(--${c})"/>`; acc += v; } });
  s += `<path d="M${rows.map(r => f.sx(r.y) + "," + f.sy(r.demand)).join(" L")}" fill="none" stroke="var(--demand)" stroke-width="1.8"/>`;
  rows.forEach(r => { s += `<rect class="hit" data-y="${r.y}" x="${f.sx(r.y) - f.bw / 2}" width="${f.bw}" y="${f.T}" height="${h - f.T - f.Bm}" fill="transparent"/>`; });
  return s + "</svg>";
}
function chart2(rows, ref) {
  const w = 900, h = 260, f = frame(w, h, 800, 200, "737s sold a year");
  let s = f.s;
  const line = (vals, col, dash, wd) => `<path d="M${vals.map((v, i) => f.sx(Y[i]) + "," + f.sy(v)).join(" L")}" fill="none" stroke="var(--${col})" stroke-width="${wd}" ${dash ? 'stroke-dasharray="5 4"' : ""}/>`;
  s += line(rows.map(r => r.capMax), "faint", true, 1.4) + line(ref.map(r => r.max), "ref", false, 2) + line(rows.map(r => r.max), "boeing", false, 2.4);
  rows.forEach((r, i) => { s += `<rect class="hit2" data-i="${i}" x="${f.sx(r.y) - f.bw / 2}" width="${f.bw}" y="${f.T}" height="${h - f.T - f.Bm}" fill="transparent"/>`; });
  return s + "</svg>";
}
const SUM = (rows, k, a = 2026, b = 2060) => rows.filter(r => r.y >= a && r.y <= b).reduce((s, r) => s + r[k], 0);
let REF = null;
function render() {
  const rows = run(P);
  if (!REF) REF = run(Object.assign({}, DEF));
  const tot = r => r.max + r.airbus + r.comac + r.entrant;
  const share = y => { const r = rows[IDX(y)]; return tot(r) > 0 ? r.max / tot(r) : 0; };
  const dPV = rows.reduce((s, r, i) => s + (r.max - REF[i].max) * G.unit737 * G.df[i], 0);
  const tiles = [
    ["737s sold 2026-60", fmt(SUM(rows, "max")), `game's Do Nothing: ${fmt(SUM(REF, "max"))}`],
    ["737s sold 2045-60", fmt(SUM(rows, "max", 2045)), `game's Do Nothing: ${fmt(SUM(REF, "max", 2045))}`],
    ["Boeing share 2050", Math.round(share(2050) * 100) + "%", `2045 ${Math.round(share(2045) * 100)}% · 2060 ${Math.round(share(2060) * 100)}%`],
    ["Airbus 2045-60", fmt(SUM(rows, "airbus", 2045)), `game's Do Nothing: ${fmt(SUM(REF, "airbus", 2045))}`],
    ["COMAC · entrant 2026-60", fmt(SUM(rows, "comac")) + " · " + fmt(SUM(rows, "entrant")), "aircraft delivered"],
    ["Customers lost 2026-60", fmt(SUM(rows, "lost")), `game's Do Nothing: ${fmt(SUM(REF, "lost"))}`],
    ["737 profit vs game's Do Nothing", (dPV < 0 ? "−$" : "+$") + Math.abs(dPV).toFixed(2) + "B", "PV at 2026, indicative"]];
  document.getElementById("tiles").innerHTML = tiles.map(([k, v, d]) => `<div class="panel tile"><div class="k">${k}</div><div class="v">${v}</div><div class="d">${d}</div></div>`).join("");
  document.getElementById("t1").textContent = `Who builds the 737/A320-class aircraft: Boeing ${fmt(SUM(rows, "max"))}, Airbus ${fmt(SUM(rows, "airbus"))}, COMAC ${fmt(SUM(rows, "comac"))}, entrant ${fmt(SUM(rows, "entrant"))} over 2026-60`;
  document.getElementById("t2").textContent = `737s sold a year: ${fmt(SUM(rows, "max", 2045))} in 2045-60, against ${fmt(SUM(REF, "max", 2045))} in the game's Do Nothing`;
  document.getElementById("c1").innerHTML = chart1(rows);
  document.getElementById("c2").innerHTML = chart2(rows, REF);
  document.querySelectorAll("#c1 .hit").forEach(el => { const r = rows[IDX(+el.dataset.y)];
    el.addEventListener("pointermove", e => showTip(e, `<b>${r.y}</b><div class="r"><span>Demand</span><b>${fmt(r.demand)}</b></div>` +
      [["737 MAX", r.max, r.capMax], ["Airbus", r.airbus, r.capA], ["COMAC", r.comac, r.capC], ["Entrant", r.entrant, r.capE]].map(([n, v, c]) =>
        `<div class="r"><span>${n}</span><b>${fmt(v)} <span style="color:var(--faint)">/ ${fmt(c)}</span></b></div>`).join("") +
      `<div class="r"><span>Lost</span><b>${fmt(r.lost)}</b></div>`)); el.addEventListener("pointerleave", hideTip); });
  document.querySelectorAll("#c2 .hit2").forEach(el => { const i = +el.dataset.i, r = rows[i];
    el.addEventListener("pointermove", e => showTip(e, `<b>${r.y}</b><div class="r"><span>737s sold</span><b>${fmt(r.max)}</b></div><div class="r"><span>Game's Do Nothing</span><b>${fmt(REF[i].max)}</b></div><div class="r"><span>737 capacity</span><b>${fmt(r.capMax)}</b></div>`));
    el.addEventListener("pointerleave", hideTip); });
  document.getElementById("tbl").innerHTML = `<table><thead><tr><th>Year</th><th>Demand</th><th>737 cap</th><th>737 sold</th><th>Airbus cap</th><th>Airbus sold</th><th>COMAC</th><th>Entrant</th><th>Lost</th></tr></thead><tbody>` +
    rows.map(r => `<tr><td>${r.y}</td><td>${fmt(r.demand)}</td><td>${fmt(r.capMax)}</td><td>${fmt(r.max)}</td><td>${fmt(r.capA)}</td><td>${fmt(r.airbus)}</td><td>${fmt(r.comac)}</td><td>${fmt(r.entrant)}</td><td>${fmt(r.lost)}</td></tr>`).join("") + "</tbody></table>";
  const S = Object.assign({}, P);
  document.getElementById("settings").value = JSON.stringify(S, null, 1);
  window.__rows = rows;
}
window.__run = run; window.__presets = {DEF, P_BUILD, P_PROT};
writeControls(); readControls(); render();
</script></body></html>"""


def main():
    g = data()
    page = HTML.replace("__DATA__", json.dumps(g, separators=(",", ":"))).replace("__NGSA__", str(g["ngsa_eis"]))
    with open(OUT, "w") as f:
        f.write(page)
    print("wrote", os.path.abspath(OUT), len(page))


if __name__ == "__main__":
    main()
