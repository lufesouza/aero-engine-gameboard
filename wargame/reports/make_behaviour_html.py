#!/usr/bin/env python3
"""Build the player-behaviour page: how each player's evidence-built profile makes it behave, what it did in
the two five-player games (wg5-2045, fps on time; wg5-2045d, fps three years late), and what that behaviour
was worth to every player.

Usage: python3 wargame/reports/make_behaviour_html.py <out.html>

All figures come from wargame/reports/player_behaviour.md (verified per-player analyses and the cross-player
synthesis); full-game delta PV is read from the two runs' saved state so the headline chart matches the record.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from wargame import engine as E  # noqa: E402
from wargame import model as M  # noqa: E402

PLAYERS = [("boeing", "Boeing"), ("airbus", "Airbus"), ("rolls_royce", "Rolls-Royce"), ("pratt_whitney", "Pratt & Whitney"), ("cfm", "CFM/GE")]
NAME = dict(PLAYERS)
esc = html.escape


def final_pv(run):
    st = E.load_state(run)
    cfg = st["config"]
    ev = M.evaluate(cfg, M.build_world(cfg, st["history"]), with_objectives=False)
    return {p: ev[p]["delta_pv_b"] for p, _ in PLAYERS}


# ------------------------------------------------------------------ content
CARDS = {
    "boeing": dict(
        tag="A gated, finance-led incumbent",
        built=["151 calls, conferences and investor days, 2006-2025", "16 10-Ks; GS and MS models", "2,537 evidence items",
               "Team: Ortberg (107 items), Malave (11, one call), Pope (8)"],
        behaves=["Readiness gates first: no fps and no 787 Re-engine in round 1, and no rate step under the round-1 supply crunch",
                 "Launch only if the business case closes: beat Do Nothing by >$1B, and lose ≤$2B to it in the slip test",
                 "One major development at a time; never cancel; never blame",
                 "Commit only to a committed engine; the engine requirement names no maker",
                 "Widebody as Chicken: never follow an A350 Re-engine, move first when uncontested",
                 "Calm, date-averse voice: “We're turning it. I don't think it's turned”"],
        g1="Waited in round 1. Launched fps in 2031 (Solo, 10-year ramp-up) with the 737 rate step. Held incumbency at 40.2%.",
        g2="The same test rejected the late fps (−0.73 vs Do Nothing; −4.71 in the slip test). Launched a 787 Re-engine on GE in 2031 instead.",
        impact=[("+7.44", "fps launch worth to Boeing (game 1); −11.31 to Airbus"),
                ("+6.25", "787 Re-engine instead of the late fps (game 2); +3.08 for the refusal alone"),
                ("+5.03", "787 Re-engine first; Airbus −3.15, as it shelved its A350 Re-engine"),
                ("−4.7", "cost of waiting in round 1, against an fps launched in 2028 (game 1)")],
        note="Its engine requirement named no maker, so rivals read it in opposite ways. Malave's slip-test veto, one of two failed legs behind the game-2 no-fps call, rests on one call."),
    "airbus": dict(
        tag="Disciplined and rule-bound; maximises PV inside red lines",
        built=["Own voice: the FY2025 Board Report (310 items)", "183 items of Airbus behaviour seen by Boeing and analysts, 2006-2025",
               "867 evidence items", "Faury: one own-words line; Toepfer 7 items; Wagner 2"],
        behaves=["Own technology clock: NGSA in 2028, never re-timed around Boeing",
                 "Asks for the partner's best engine but never waits for it",
                 "No concurrent developments under the supply crunch",
                 "Widebody Chicken: stays out once Boeing has re-engined the 787",
                 "Delay Tactics at most once, only against an fps in development and only if worth ≥$1B (refused in game 1 at +0.72); poaches only while developing",
                 "Signals to pull suppliers, then resets openly (“subject to Board approval”)"],
        g1="NGSA 2028, then the A350 Re-engine in round 2 before Boeing could move. Refused Delay Tactics in round 3.",
        g2="NGSA 2028. Signalled an A350 Re-engine for 2037, then shelved it after Boeing's 787 Re-engine.",
        impact=[("+36.5 / +44.5", "final ΔPV: top scorer in both games"),
                ("+10.9", "NGSA 2028 vs 2031 (game 2); +6.4 in game 1"),
                ("+4.07", "to Boeing from refusing Delay Tactics; it cost Airbus 0.74 and the 60/40 objective (59.8%)"),
                ("+0.33", "shelving the A350 Re-engine after Boeing moved (game 2); it spared Boeing 5.05")],
        note="The thin seats only ratified the company default. Hard rules 2-7 are inference. Its conditional 2037 A350 signal led Rolls-Royce to commit an engine that was stranded (an RR choice, −1.53 to RR)."),
    "rolls_royce": dict(
        tag="Cash-first and maturity-first, and structurally a round late",
        built=["1,335 items from its own calls, 2010-2025", "MS model, Capital IQ, 2019 engine brief", "1,951 evidence items",
               "Team: Erginbilgic, McCabe, Watson (27 items, 26 from one event)"],
        behaves=["“No airframe, no engine”: UltraFan only for an aircraft announced in an earlier round (unannounced = P 0.1)",
                 "Time on wing first: the Trent 1000 upgrade in round 1",
                 "Never compresses maturity; launches the widebody engine a year ahead",
                 "Standard terms in every round; no overlapping UltraFan programmes",
                 "Commit and honour, including the commitment to stop"],
        g1="Held the rule in round 1. Launched UltraFan narrowbody on Boeing's engine requirement in round 2; Boeing named GTF2. Cancelled it in round 3.",
        g2="Held the rule in round 1 and waited in round 2. Committed the UltraFan widebody in 2036 on Airbus's 2037 signal; Airbus shelved the A350 the same round.",
        impact=[("−18.2 / −21.4", "the round-1 rule, to itself (games 1 / 2)"),
                ("+40.8 / +45.6", "the same rule, to CFM/GE"),
                ("−4.44", "the game-1 narrowbody bet"),
                ("−1.53", "the game-2 widebody commitment")],
        note="Last in both games (−7.0, then −3.7). Both bets were declared and within its premium cap: the game-1 bet was objective-driven, the game-2 one honoured its promise."),
    "pratt_whitney": dict(
        tag="Durability first, then cut what nobody selected",
        built=["1,413 items from RTX/UTC calls; 413 from 10-Ks", "GS RTX model and GTF reporting", "2,072 evidence items",
               "Team: Calio (110), Mitchill (180), Eddy (21, one event)"],
        behaves=["Fix forward: books the GTF durability upgrade first",
                 "Hedged NGSA with a GTF2 for 2030, cleared by its objectives (profile default: a disclosed offer, 2029)",
                 "CFO cuts an engine nobody selected at the first chance: “reaffirm, then cut”",
                 "No discounts; no widebody engine",
                 "Joint Venture only after an airframer names UltraFan"],
        g1="Upgrade plus a 2030 GTF2 hedge. Cancelled GTF2 in round 2, the same sealed round Boeing named it.",
        g2="The same orders. Cancelled GTF2 in round 2, breaking its round-1 promise to keep it to the end of that round.",
        impact=[("−2.77", "final ΔPV in both games"),
                ("+20.66", "to CFM/GE from the game-1 cancel; −1.89 to Boeing, −0.22 to itself"),
                ("−0.73", "realised cost of the hedge, each game"),
                ("+13.9", "what a round-1 Joint Venture with Rolls-Royce would have given P&W; blocked by RR's rule")],
        note="Eddy, whose seat set the 2030 timing, rests on one 2023 event. Every Joint Venture threshold is inference."),
    "cfm": dict(
        tag="The incumbent that wins by not moving",
        built=["1,300 items from GE calls and investor days, 2015-2025", "GS and MS CFM/Safran model cells", "Culp: 474 own-words items",
               "Safran side thin: the Safran gate is consent with no observed veto"],
        behaves=["Derivative first: no new engine without a committed airframe",
                 "Durability first, one commitment a turn: LEAP upgrade, then the GEnx package",
                 "Tests its own defensive-engine trigger against PV and a $2B cap, and rejects it",
                 "RISE open fan only with a committed airframe",
                 "Guides low; never names a rival (“we don't have a birthright on that next order”)"],
        g1="LEAP upgrade, then GEnx package, then nothing. NGSA, fps and the A350 Re-engine all fell back to its engines.",
        g2="The same. NGSA flew the LEAP derivative; Boeing chose the GE GEnx upgrade for the 787 Re-engine.",
        impact=[("+18.8 / +19.0", "final ΔPV, with zero regret; narrowbody engine share 76% → 100%"),
                ("+18.79", "saved by rejecting the defensive ducted engine (game 1, round 2)"),
                ("−64.6", "what CFM/GE would lose if every aircraft got the engine it asked for (game 1)"),
                ("+4.1 to +5.1", "what a round-1 CFM ducted engine would have given Airbus")],
        note="Its forecasting error came mainly from never pricing P&W's same-round cancel."),
}

# Behaviour -> effect on every player (as played minus the rejected alternative, $B PV at each player's WACC)
MATRIX = [
    ("boeing", "Launches fps in 2031", "G1", {"boeing": 7.44, "airbus": -11.31, "rolls_royce": 0, "pratt_whitney": 0, "cfm": -0.79}),
    ("boeing", "Rejects the late fps (with the 787 Re-engine kept)", "G2", {"boeing": 3.08, "airbus": 8.61, "rolls_royce": 0, "pratt_whitney": 0, "cfm": 0.79}),
    ("boeing", "Moves first with a 787 Re-engine*", "G2", {"boeing": 5.03, "airbus": -3.15, "rolls_royce": -2.66, "pratt_whitney": 0, "cfm": 2.44}),
    ("boeing", "Takes the 737 rate step in round 2", "G1", {"boeing": 0.51, "airbus": -3.77, "rolls_royce": 0, "pratt_whitney": -0.02, "cfm": 0.11}),
    ("airbus", "Launches NGSA in 2028, not 2031*", "G2", {"boeing": -0.48, "airbus": 10.94, "rolls_royce": 0, "pratt_whitney": -0.74, "cfm": 3.67}),
    ("airbus", "Refuses Delay Tactics", "G1", {"boeing": 4.07, "airbus": -0.74, "rolls_royce": 0, "pratt_whitney": 0, "cfm": 0}),
    ("airbus", "Shelves the A350 Re-engine", "G2", {"boeing": 5.05, "airbus": 0.33, "rolls_royce": -0.16, "pratt_whitney": 0, "cfm": 0.43}),
    ("rolls_royce", "No UltraFan for NGSA in round 1*", "G1", {"boeing": 0.05, "airbus": -7.74, "rolls_royce": -18.23, "pratt_whitney": 0, "cfm": 40.75}),
    ("rolls_royce", "No UltraFan for NGSA in round 1", "G2", {"boeing": 0.06, "airbus": -8.86, "rolls_royce": -21.41, "pratt_whitney": 0, "cfm": 45.57}),
    ("rolls_royce", "UltraFan narrowbody bet on Boeing's requirement", "G1", {"boeing": 0, "airbus": 0, "rolls_royce": -4.44, "pratt_whitney": 0, "cfm": 0}),
    ("pratt_whitney", "Cancels GTF2 the round Boeing named it", "G1", {"boeing": -1.89, "airbus": 0, "rolls_royce": 0, "pratt_whitney": -0.22, "cfm": 20.66}),
    ("pratt_whitney", "Hedges NGSA with a 2030 GTF2", "G1+G2", {"boeing": 0, "airbus": 0, "rolls_royce": 0, "pratt_whitney": -0.73, "cfm": 0}),
    ("cfm", "Rejects a round-1 ducted engine", "G1", {"boeing": -1.12, "airbus": -4.06, "rolls_royce": 0, "pratt_whitney": 0, "cfm": 34.59}),
    ("cfm", "Rejects the defensive ducted engine in round 2", "G1", {"boeing": -3.03, "airbus": 0, "rolls_royce": 0, "pratt_whitney": 0, "cfm": 18.79}),
]

MECHANISMS = [
    ("“No airframe, no engine” rules under sealed moves",
     "Rolls-Royce waited for an aircraft announced in an earlier round; P&W cut an engine nobody had selected; CFM/GE launched nothing "
     "without a committed airframe. The airframers counted only committed engines but requested rivals' engines anyway, because a request "
     "falls back to CFM/GE at no cost. Four engine coordination failures followed, and every contested aircraft went to CFM/GE."),
    ("Order of entry into service decides the narrowbody",
     "The first new aircraft in service gains share only until the second arrives, then shares freeze. NGSA entered in 2035; fps followed "
     "in 2038 in game 1 and never in game 2. Airbus held 59.8% in game 1 and reached 75% in 2050 in game 2."),
    ("In widebody, whoever moves first wins",
     "Boeing's one-development rule decided who moved first. In game 1 fps was in development, so Airbus re-engined the A350 first. "
     "In game 2 there was no fps, so Boeing re-engined the 787 first and Airbus stayed out. The engine went to GE both times."),
    ("Disclosures were read in opposite ways",
     "Boeing's engine-neutral requirement led Rolls-Royce to launch and Pratt & Whitney to cancel. Airbus's conditional 2037 A350 signal "
     "led Rolls-Royce to commit, in the round Airbus shelved it. P&W's “keep it until” promise was broken the next round."),
    ("The fps delay worked entirely through behaviour",
     "Round 1 was identical in both games, and on the orders actually played in game 2 the delay had no direct effect. "
     "Applied to Boeing's game-1 plan, it would have cost Boeing $11.1B; "
     "the players' changed choices won back $8.9B of it."),
]

DRIVERS = [
    ("NGSA first into service (2035)", "Doctrine", "Airbus's own technology clock; also PV-best on its own grid"),
    ("NGSA flies the LEAP derivative", "Doctrine + engine rules", "Rolls-Royce's round-1 rule; an airframe's engine is fixed at launch, with fallback to CFM"),
    ("fps flies the LEAP derivative (game 1)", "Doctrine + engine rules", "P&W's cancel rule in the same sealed round Boeing named GTF2"),
    ("CFM/GE takes 100% of narrowbody engines", "Engine rules", "The fallback chain, given the others' doctrines; CFM's own doctrine was to do nothing"),
    ("Boeing waits in round 1", "Doctrine", "Hard rule H1: about $4.7B in game 1, nothing in game 2"),
    ("No fps and a 787 Re-engine (game 2)", "Scenario, through doctrine", "The delay fails the go/no-go test; H4 frees capacity for the 787"),
    ("Who wins the widebody", "Scenario, through doctrine", "Boeing's H4 in game 1, Airbus's rule 3 in game 2"),
    ("Rolls-Royce last in both games", "Doctrine + engine rules", "Its round-1 rule cost it 18-21 (−18.2 / −21.4); its two bets cost 4.44 and 1.53"),
    ("P&W −2.77 in both games", "Doctrine", "Identical orders in both games"),
    ("Market cell effect", "Minor", "At most about $0.5B; NGSA x0.97 vs x1.03 for the same round-1 facts"),
]

CAVEATS = [
    "Thin seats decided some real moves: Boeing's CFO (one call; the game-2 slip-leg veto), P&W's operating head (one event; the 2030 hedge timing), and Rolls-Royce's CFO co-signed the game-1 bet. Airbus's thin seats only ratified the default; Boeing's Commercial Airplanes seat was played by doctrine; Rolls-Royce's Civil head rests on one event; CFM/GE's operating-head evidence ends March 2024.",
    "Placeholder parameters sit on the decisive mechanics: the LEAP-derivative capture (0.92) and margin, fps capex, Joint Venture terms, capture speed, the 80% share cap and the 2060 horizon.",
    "One game per scenario and one seed; round 1 was identical in both, so it is effectively one round-1 sample.",
    "Counterfactuals hold the other players' recorded orders fixed, so they do not capture rivals' reactions.",
    "PV is at each player's own WACC, so values cannot be added across players.",
]


# ------------------------------------------------------------------ charts
def num(v, f):
    """Format with a true minus sign."""
    return format(v, f).replace("-", "\u2212")


def dumbbell(pv1, pv2):
    w, rowh, top, left, right = 760, 46, 14, 150, 70
    h = top + rowh * len(PLAYERS) + 50
    lo, hi = -10, 50
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Full-game delta PV by player, game 1 and game 2">']
    for t in range(lo, hi + 1, 10):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - 44}" class="{"zero" if t == 0 else "grid"}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 27}" text-anchor="middle" class="tick">{"0" if t == 0 else num(t, "+d")}</text>')
    for i, (p, n) in enumerate(PLAYERS):
        y = top + i * rowh + rowh / 2 - 6
        a, b = pv1[p], pv2[p]
        out.append(f'<text x="{left - 14}" y="{y + 5:.1f}" text-anchor="end" class="rowlab">{esc(n)}</text>')
        x1, x2 = sx(min(a, b)), sx(max(a, b))
        if x2 - x1 > 16:
            out.append(f'<line x1="{x1 + 8:.1f}" x2="{x2 - 8:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--{p})" stroke-width="3" opacity=".55"/>')
        out.append(f'<g class="pt" tabindex="0"><circle cx="{sx(b):.1f}" cy="{y:.1f}" r="6.5" fill="var(--{p})"/>'
                   f'<title>{esc(n)}, game 2 (fps late): {num(b, "+.1f")} $B</title></g>')
        out.append(f'<g class="pt" tabindex="0"><circle cx="{sx(a):.1f}" cy="{y:.1f}" r="9" fill="none" stroke="var(--{p})" stroke-width="2.5"/>'
                   f'<title>{esc(n)}, game 1 (fps on time): {num(a, "+.1f")} $B</title></g>')
        lx = max(sx(max(a, b)) + 14, sx(0) + 10)  # keep labels clear of the zero line
        lab = f"{num(a, '+.1f')} → {num(b, '+.1f')}" if abs(a - b) >= 0.05 else f"{num(b, '+.1f')} both"
        out.append(f'<text x="{lx:.1f}" y="{y + 4:.1f}" class="val">{lab}</text>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{h - 6}" text-anchor="middle" class="tick">$B PV, each player at its own WACC</text>')
    out.append("</svg>")
    return "".join(out)


def matrix_html():
    cap = 46.0
    head = "".join(f'<th class="mcol" scope="col"><span class="sw" style="--pc:var(--{p})"></span>{esc(n)}</th>' for p, n in PLAYERS)
    rows = []
    for actor, label, game, vals in MATRIX:
        cells = []
        for p, n in PLAYERS:
            v = vals[p]
            pct = min(abs(v), cap) / cap * 50
            side = "pos" if v > 0 else ("neg" if v < 0 else "nil")
            bar = (f'<span class="bar {side}" style="width:{pct:.1f}%"></span>' if v else "")
            own = " own" if p == actor else ""
            txt = "0" if v == 0 else num(v, "+.2f")
            cells.append(f'<td class="mcell{own}" data-l="{esc(n)}"><span class="track" aria-hidden="true">{bar}</span><span class="mv" aria-hidden="true">{txt}</span>'
                         f'<span class="sr">{esc(n)}: {txt} $B</span></td>')
        rows.append(f'<tr><th class="mrow" scope="row"><span class="sw" style="--pc:var(--{actor})"></span><b>{esc(NAME[actor])}</b> '
                    f'{esc(label)} <span class="gtag">{game}</span></th>{"".join(cells)}</tr>')
    return (f'<div class="scroll"><table class="matrix"><thead><tr><th class="mrow" scope="col">Behaviour (actor, game)</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="muted small">* Constructed baselines: the 787 Re-engine row compares with no 787 Re-engine and Airbus launching its A350 '
            'Re-engine in 2037; the Rolls-Royce game-1 row also removes its later narrowbody bet from the baseline; the Airbus NGSA row also turns off '
            'round-1 Poaching. Every other row changes one choice and holds all other recorded orders fixed.</p>')


def fallback_diagram():
    steps = [("Airframer asks for a rival engine", "UltraFan (Rolls-Royce) or GTF2 (P&W)", "req"),
             ("Its maker has no live programme for it", "never launched, or cancelled (even in the same sealed round)", "gate"),
             ("Falls back to CFM's advanced ducted engine", "only if CFM has committed it", "gate"),
             ("Lands on CFM's LEAP derivative", "no new engine; capture 0.92, margin −1pp", "end")]
    parts = []
    for i, (h, s, k) in enumerate(steps):
        parts.append(f'<div class="fb {k}" role="listitem"><b>{esc(h)}</b><span>{esc(s)}</span></div>')
        if i < len(steps) - 1:
            parts.append('<div class="fbarrow" aria-hidden="true">→</div>')
    return ('<div class="fbflow" role="list" aria-label="Narrowbody engine fallback chain">' + "".join(parts) + "</div>"
            '<p class="muted small">Widebody requests fall back to the GE GEnx upgrade, which needs no new programme and is always available. '
            'Because a request costs the airframer nothing, every contested aircraft in both games ended on CFM/GE engines.</p>')


# ------------------------------------------------------------------ page
CSS = r"""
:root {
  --bg: #f4f6f9; --surface: #ffffff; --sunk: #eef2f7; --line: #d5dce6; --grid: #e3e8ef;
  --fg: #141c28; --muted: #556275; --faint: #8a95a5;
  --boeing: #2a78d6; --airbus: #e34948; --pratt_whitney: #4a3aa7; --rolls_royce: #eda100; --cfm: #008300;
  --pos: #3b4a5e; --neg: #9aa6b6;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --font-body: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --r: 8px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #22a32a;
  --pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #0f141c; --surface: #161d28; --sunk: #1d2633; --line: #2b3646; --grid: #222c3a;
  --fg: #e7ecf3; --muted: #a3aebe; --faint: #6f7b8d;
  --boeing: #3987e5; --airbus: #e66767; --pratt_whitney: #9085e9; --rolls_royce: #c98500; --cfm: #22a32a;
  --pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--font-body); }
.wrap { max-width: 1140px; margin: 0 auto; padding: 0 20px 56px; }
header.top { padding: 34px 0 10px; }
.eyebrow { font: 500 .74rem/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
h1 { font: 700 clamp(2.1rem, 5vw, 3.2rem)/1.02 var(--font-display); margin: 10px 0 12px; letter-spacing: .01em; }
h2 { font: 700 1.9rem/1.1 var(--font-display); margin: 0 0 8px; }
h3 { font: 600 1.25rem/1.2 var(--font-display); margin: 0 0 8px; letter-spacing: .02em; }
.lede { font-size: 1.08rem; max-width: 76ch; color: var(--fg); }
.muted { color: var(--muted); } .small { font-size: .85rem; }
nav.toc { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 14px 0 6px; font-size: .9rem; }
nav.toc a { color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--line); }
nav.toc a:hover { color: var(--fg); }
section { margin-top: 38px; }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 18px 20px; }
.takeaways { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 16px; }
.takeaways .panel b { display: block; font: 600 1.05rem/1.25 var(--font-display); letter-spacing: .02em; margin-bottom: 4px; }
.chart { width: 100%; height: auto; display: block; }
.chart .grid { stroke: var(--grid); } .chart .zero { stroke: var(--muted); }
.chart .tick { fill: var(--muted); font: 11px var(--font-mono); }
.chart .rowlab { fill: var(--fg); font: 600 14px var(--font-body); }
.chart .val { fill: var(--fg); font: 500 12.5px var(--font-mono); paint-order: stroke; stroke: var(--surface); stroke-width: 5px; stroke-linejoin: round; }
.chart .pt:focus { outline: none; } .chart .pt:focus circle, .chart .pt:hover circle { stroke-width: 4; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: .85rem; color: var(--muted); margin-top: 6px; }
.legend i { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 6px; vertical-align: -2px; border: 2px solid var(--muted); }
.legend i.f { background: var(--muted); }
.player { border-left: 5px solid var(--pc); }
.player .head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 14px; margin-bottom: 12px; }
.player .head h3 { font-size: 1.7rem; margin: 0; }
.player .head .tagline { color: var(--muted); font-size: .98rem; }
.pgrid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 18px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 12px; padding: 0; list-style: none; }
.chips li { background: var(--sunk); border-radius: 12px; padding: 3px 10px; font-size: .8rem; color: var(--muted); }
.label { font: 500 .72rem/1 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
ol.rules { margin: 0; padding-left: 20px; } ol.rules li { margin: 0 0 5px; }
.games { display: grid; gap: 8px; margin-bottom: 14px; }
.game { background: var(--sunk); border-radius: 6px; padding: 9px 12px; font-size: .93rem; }
.game b { font: 600 .78rem/1 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); display: block; margin-bottom: 4px; }
.stats { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.stat { border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; }
.stat .n { font: 700 1.45rem/1.1 var(--font-display); color: var(--fg); letter-spacing: .01em; }
.stat .d { font-size: .82rem; color: var(--muted); line-height: 1.35; }
.note { margin-top: 12px; font-size: .86rem; color: var(--muted); border-top: 1px dashed var(--line); padding-top: 8px; }
.players { display: grid; gap: 16px; }
.mech { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin-top: 14px; }
.mech .panel b { display: block; font: 600 1.12rem/1.2 var(--font-display); letter-spacing: .02em; margin-bottom: 6px; }
.mech .panel .num { font: 700 1rem/1 var(--font-mono); color: var(--muted); margin-right: 6px; }
.fbflow { display: flex; align-items: stretch; gap: 6px; margin: 14px 0 6px; flex-wrap: wrap; }
.fb { flex: 1 1 180px; border: 1px solid var(--line); border-radius: 6px; padding: 10px 12px; background: var(--surface); }
.fb b { display: block; font-size: .95rem; } .fb span { font-size: .82rem; color: var(--muted); }
.fb.req { border-left: 4px solid var(--rolls_royce); } .fb.gate { border-left: 4px solid var(--faint); } .fb.end { border-left: 4px solid var(--cfm); }
.fbarrow { align-self: center; color: var(--muted); font-size: 1.3rem; }
.scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { border-collapse: separate; border-spacing: 0; overflow: hidden; width: 100%; background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); }
th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: middle; }
thead th { font: 500 .74rem/1.2 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); background: var(--sunk); }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 3px; background: var(--pc); margin-right: 6px; vertical-align: 0; }
.matrix { table-layout: fixed; }
.matrix .mrow { font-weight: 400; font-size: .9rem; width: 31%; }
.matrix .mcol { text-align: center; white-space: nowrap; }
.gtag { font: 500 .7rem/1 var(--font-mono); color: var(--muted); background: var(--sunk); border-radius: 4px; padding: 2px 5px; margin-left: 4px; }
.mcell { position: relative; text-align: center; }
.mcell.own { background: var(--sunk); }
.track { position: relative; display: block; height: 10px; margin: 0 2px 5px; }
.track::before { content: ""; position: absolute; left: 50%; top: -3px; bottom: -3px; width: 1px; background: var(--faint); }
.bar { position: absolute; top: 0; height: 10px; border-radius: 2px; }
.bar.pos { left: 50%; background: var(--pos); } .bar.neg { right: 50%; background: var(--neg); }
.mv { font: 500 .85rem/1 var(--font-mono); }
.mcell.own .mv { font-weight: 600; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.drivers td:nth-child(2) { white-space: nowrap; }
.pill { display: inline-block; font: 500 .74rem/1 var(--font-mono); padding: 4px 7px; border-radius: 4px; background: var(--sunk); color: var(--fg); }
tbody tr:last-child > * { border-bottom: 0; }
ol.rules li, .game, .stat .d, .lede, .takeaways .panel { text-wrap: pretty; }
ul.cav { margin: 0; padding-left: 18px; } ul.cav li { margin-bottom: 6px; }
footer { margin-top: 40px; font-size: .82rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 12px; }
@media (max-width: 760px) {
  .pgrid { grid-template-columns: 1fr; }
  .fbarrow { transform: rotate(90deg); flex-basis: 100%; text-align: center; }
  .matrix thead { display: none; }
  .matrix, .matrix tbody, .matrix tr { display: block; width: 100%; }
  .matrix tr { border-bottom: 1px solid var(--line); padding: 6px 0; }
  .matrix th.mrow { display: block; border: 0; min-width: 0; width: auto; }
  .matrix { table-layout: auto; }
  .matrix td.mcell { display: grid; grid-template-columns: 9.5em 1fr 4.6em; align-items: center; gap: 8px; border: 0; padding: 3px 10px; text-align: right; min-width: 0; }
  .matrix td.mcell::before { content: attr(data-l); text-align: left; font-size: .82rem; color: var(--muted); }
  .matrix td.mcell .track { margin: 0; order: 0; }
  .drivers thead { display: none; }
  .drivers, .drivers tbody, .drivers tr, .drivers td { display: block; width: 100%; }
  .drivers tr { border-bottom: 1px solid var(--line); padding: 6px 0; }
  .drivers td { border: 0; padding: 3px 10px; }
}
@media (prefers-reduced-motion: no-preference) { a { transition: color .15s; } }
"""


def player_section(p, n, c):
    built = "".join(f"<li>{esc(x)}</li>" for x in c["built"])
    rules = "".join(f"<li>{esc(x)}</li>" for x in c["behaves"])
    stats = "".join(f'<div class="stat"><div class="n">{esc(a)}</div><div class="d">{esc(b)}</div></div>' for a, b in c["impact"])
    return (f'<article class="panel player" id="p-{p}" style="--pc:var(--{p})"><div class="head"><h3>{esc(n)}</h3>'
            f'<span class="tagline">{esc(c["tag"])}</span></div>'
            f'<div class="pgrid"><div><p class="label">How it was built</p><ul class="chips">{built}</ul>'
            f'<p class="label">How it behaves</p><ol class="rules">{rules}</ol></div>'
            f'<div><p class="label">What it did</p><div class="games"><div class="game"><b>Game 1 · fps on time</b>{esc(c["g1"])}</div>'
            f'<div class="game"><b>Game 2 · fps three years late</b>{esc(c["g2"])}</div></div>'
            f'<p class="label">Key numbers ($B PV)</p><div class="stats">{stats}</div></div></div>'
            f'<div class="note">{esc(c["note"])}</div></article>')


def build():
    pv1, pv2 = final_pv("wg5-2045"), final_pv("wg5-2045d")
    take = [
        ("Every player played its profile", "No player broke a hard rule in either game; every departure was declared and stayed inside its premium cap."),
        ("Rules collided, not players", "“No airframe, no engine” on both sides under sealed moves handed every contested aircraft to CFM/GE's existing engines."),
        ("Timing decided the narrowbody", "The first new aircraft in service takes share until the second arrives. Airbus's NGSA came first in both games."),
        ("First mover took the widebody", "Airbus in game 1, Boeing in game 2: decided by whether Boeing had an fps in development (its one-development rule), which the delay changed."),
    ]
    tk = "".join(f'<div class="panel"><b>{esc(a)}</b><span class="muted">{esc(b)}</span></div>' for a, b in take)
    mech = "".join(f'<div class="panel"><b><span class="num">{i + 1}</span>{esc(a)}</b>{esc(b)}</div>' for i, (a, b) in enumerate(MECHANISMS))
    drv = "".join(f'<tr><td>{esc(a)}</td><td><span class="pill">{esc(b)}</span></td><td class="muted">{esc(c)}</td></tr>' for a, b, c in DRIVERS)
    cav = "".join(f"<li>{esc(x)}</li>" for x in CAVEATS)
    cards = "".join(player_section(p, n, CARDS[p]) for p, n in PLAYERS)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Player Behaviour</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="top"><span class="eyebrow">Five-player war game · <span style="white-space:nowrap">wg5-2045</span> and <span style="white-space:nowrap">wg5-2045d</span></span>
<h1>Player Behaviour</h1>
<p class="lede">Each player is an AI agent working from a profile built from its own evidence (earnings calls, annual reports, analyst models) and deciding as its named executive team. This page shows how each one behaves, what it did in the two games, and what that behaviour was worth to every player, measured by changing one of its choices in the engine.</p>
<nav class="toc"><a href="#overview">Overview</a><a href="#players">Players</a><a href="#interactions">How behaviours combined</a><a href="#matrix">Who it helped and hurt</a><a href="#drivers">Doctrine, rules or scenario</a><a href="#caveats">Caveats</a></nav>
</header>

<main>
<section id="overview"><h2>Every player played its profile; the outcome came from how the rules collided</h2>
<div class="panel"><p class="label">Full-game delta PV, game 1 (fps on time) vs game 2 (fps three years late)</p>
<div class="legend"><span><i></i>Game 1 · fps on time</span><span><i class="f"></i>Game 2 · fps three years late</span></div>{dumbbell(pv1, pv2)}</div>
<div class="takeaways">{tk}</div></section>

<section id="players"><h2>Player by player</h2>
<p class="muted">Tiles give either a final result (“final ΔPV”) or the value of a specific alternative, as labelled; a behaviour's value is the as-played result minus the alternative it rejected. $B PV at each player's own WACC.</p>
<div class="players">{cards}
<article class="panel player" id="p-market" style="--pc:var(--faint)"><div class="head"><h3>Market cell</h3><span class="tagline">Airlines and lessors</span></div>
<p>Priced engine certainty and consistent disclosures, keeping multipliers between 0.95 and 1.07. It priced the same round-1 NGSA facts at x0.97 in game 1 and x1.03 in game 2, citing the fps delay; that alone moved Boeing's Do Nothing value from −2.30 to −2.40. Its total effect on payoffs was at most about $0.5B, and it changed no decision.</p></article>
</div></section>

<section id="interactions"><h2>How the behaviours combined</h2>
<div class="panel"><p class="label">The narrowbody engine fallback chain</p>{fallback_diagram()}</div>
<div class="mech">{mech}</div></section>

<section id="matrix"><h2>Who each behaviour helped and hurt</h2>
<p class="muted">Each row changes one of the actor's choices in the engine. Bars run right for a gain and left for a loss, on one scale ($B PV); the shaded cell is the actor itself. In game 1, giving every aircraft the engine it asked for would have cost CFM/GE $64.6B and given Rolls-Royce +23.7, Airbus +8.1, Boeing +1.8 and P&amp;W +0.2.</p>
{matrix_html()}</section>

<section id="drivers"><h2>What drove each outcome: doctrine, engine rules or scenario</h2>
<div class="scroll"><table class="drivers"><thead><tr><th>Outcome</th><th>Main driver</th><th>Evidence</th></tr></thead><tbody>{drv}</tbody></table></div></section>

<section id="caveats"><h2>Caveats</h2><div class="panel"><ul class="cav">{cav}</ul></div></section>

</main>
<footer>Source: five-player war-game engine, runs wg5-2045 (fps on time) and wg5-2045d (fps three years late); per-player analyses verified by independent re-runs (wargame/reports/player_behaviour.md). Assigned objectives come from the Boeing PD briefing (Boeing proprietary) and never change payoffs.</footer>
</div></body></html>"""


if __name__ == "__main__":
    out = sys.argv[1]
    page = build()
    with open(out, "w") as f:
        f.write(page)
    print(out, len(page))
