# Brief: 3-year fps delay on the user's dashboard (Game.txt snapshot)

## What was asked
"Consider this game (attached) - Evaluate what the 3 year fps delay would do with the business case; how Airbus would respond and the
odds of this delay bringing a 3rd player (embraer or comac) to the game. Leverage the war games you have played and just incorporate
these a few changes to evaluate this scenarios."

## Files
- Dashboard (user's code, a Streamlit app; NEVER run streamlit): `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/board/board.py` (copy of the upload). Airframer math: lines ~971-1396; NB share rule lines 102-307; engine board lines 2260-2870.
- Snapshot: `/root/.claude/uploads/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/646296c2-Game.txt`
- Headless solver: `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/dash/harness.py` (`H.af(overrides, patch)`, `H.en(...)`, `H.SNAP` = snapshot values, `H.OVERLAP_PATCH`). Python with pandas/numpy/plotly/xlrd/pdfplumber: `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/deckvenv/bin/python -I`.
- Results: `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/dash/delay.json`, `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/dash/analysis2.json`, `/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/dash/vacuum.json`; scripts `delay.py`, `analysis2.py`, `vacuum.py` in the same folder.
- Repo (cwd /home/user/aero-engine-gameboard): war games `wargame/reports/wg5-2045/` (fps on time) and `wargame/reports/wg5-2045d/` (our fps-3-years-late game: rounds.md, final_report.md, referee_report.md, scorecard.md, state.json, drivers.md); behaviour synthesis `wargame/reports/player_behaviour.md`; profiles `wargame/profiles/<player>/profile.md`, `evidence.jsonl`, `reaction_function.json`, `executives/`; agent definitions `.claude/agents/*.md`; war-game config `wargame/config/default.json`.
- Embraer raw files at repo root: `Embraer S A BOVESPA EMBJ3 Financials.xls`, `... Financials (1).xls`, `... Financials Segments.xls`, `EmbraerSABOVESPAEMBJ3EstimatesReport.xls`, `Embraer Transcripts 2010-2020 (1).pdf`. Evidence mentions of Embraer: boeing 41, pratt_whitney 22, airbus 8 (evidence.jsonl); COMAC/C919: boeing ~5, airbus 1, pratt_whitney 1; CFM executives files mention COMAC.
(SCRATCH = /tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad)

## Board facts established (all from solving the user's board headlessly)
- The uploaded build charges a FLAT $3B two-front strain. The snapshot reproduces EXACTLY (0 pure / 17 near-Nash, all 17 cells, every rounded yield) only with OVERLAP-AWARE strain: strain x clamp((min(nb_eis, wb_eis) - max(nb_eis-7, wb_eis-5))/5, 0, 1). So the snapshot came from the later overlap-strain build; all results use that rule. (Flat strain gives 1 pure / 13 near and misses 4 cells.)
- Yields: 100 + delta/EV x 100; Boeing EV $130B (debt 45), Airbus EV $150B (debt 10). WACC Boeing 10.5%, Airbus 8%. alpha 0.30. NB capex is ONE LUMP AT EIS (PV'd). NB window per program = 2026..EIS+19, baseline uses same window. Capture: NGSA Phase 1 +3pp/yr from 60% to cap 80%; fps Phase 2 recovery 1pp/yr toward 50% (snapshot sliders 1.0); Delay Tactics = flat 5pp for 5 yrs from fps EIS, $1B/move; naked fine $48.32B if Airbus plays Delay Tactics and Boeing doesn't launch.
- "3-year delay" = fps EIS 2041 -> 2044 (NGSA stays 2037; Re-engines 2035).

### Business case (Boeing fps 10-yr Solo minus Do Nothing 737, $B PV-2026; Airbus context NGSA + Re-engine A350; Boeing Do Nothing 787)
| | EIS 2041 (snapshot) | EIS 2044 (delay) | 2044 + 30% capex overrun (war-game 10%/yr extension rule) |
|---|---|---|---|
| fps10 - Do Nothing | +1.06 | -2.53 | -7.00 |
| same, vs Airbus Delay Tactics | -0.24 | -3.49 | -7.97 |
| fps 7-yr - Do Nothing | -0.11 | -3.40 | |
| fps via Embraer ($100B) - Do Nothing | -17.05 | -15.95 | |
Decomposition 2041 -> 2044: NB profit +17.06 -> +9.33 (-7.73: discounting -4.42, share -3.32); capex PV 12.36 -> 9.16 and alpha 3.64 -> 2.70 (+4.14 saved because the lump is later). Whole-project split: pure timing -0.28, share effect -3.32 (Boeing re-enters at 20% instead of 28% after 3 more years of NGSA Phase-1 capture; at 1pp/yr it reaches only 40% by 2063 vs 48% by 2060).
Sweep fps EIS: fps10-DN = 2037 +9.68, 2038 +7.29, 2039 +5.02, 2040 +2.93, 2041 +1.06, 2042 -0.52, 2043 -1.85, 2044 -2.53, 2045 -2.29, 2046 -2.07, 2047 -1.87 (late-years uptick is a board artifact: the evaluation window extends with EIS). fps drops out of every equilibrium from 2043.
Equilibria at 2044: 2 pure Nash, both Boeing Do Nothing on narrowbody (WB Chicken): (Airbus NGSA + Re-engine A350 | Boeing Do Nothing 737 + Do Nothing 787) Airbus 133.41% / Boeing 95.34% ($B +50.12 / -6.05); (Airbus NGSA + Do Nothing A350 | Boeing Do Nothing 737 + Re-engine 787) 131.79% / 99.64% (+47.68 / -0.47). Plus 2 near-Nash with 737 Rate Increase. Snapshot 2041: 0 pure / 17 near (fps 10yr in 12 of 17).
Restoration thresholds at 2044 (modal context; linear levers, confirmed by solve): fps margin break-even 31.2% (base 25.64), +$1B hurdle 33.4%; vs Delay Tactics break-even 34.0%. fps 10yr capex break-even ~$45B (base 55.25), hurdle ~$41B. fps price break-even $66.9M (base $55M). Recovery speed: 1.5pp/yr -0.96, 2.0 +0.37, 3.0 +2.14, 4.0 +3.23 (balance share irrelevant at 1pp/yr). via Embraer break-even capex $52.9B (vs $100B).
### Airbus
- Airbus best response to Boeing fps (2041 and 2044): NGSA + Delay Tactics (Bottleneck) + Re-engine A350. Airbus payoff vs fps10: +39.21 (2041) -> +47.60 (2044); vs Boeing Do Nothing: +50.12 (both). Delay Tactics value vs fps10: +1.45 (2041) -> +1.16 (2044).
- NGSA timing (fps 2044): Airbus payoff vs fps10 by NGSA EIS 2035 +56.2, 2036 +51.7, 2037 +47.6, 2038 +42.7, 2039 +37.4, 2040 +32.4, 2041 +27.7 -> slipping NGSA costs Airbus ~$4-5B/yr; fps re-enters Boeing's equilibrium only if NGSA's lead <= 3 years (NGSA >= 2041 when fps is 2044; snapshot's 4-yr lead is the knife edge).
- In equilibrium after the delay Airbus no longer needs Delay Tactics (Boeing does not launch) and would face the $48.32B naked fine if it used them; the contest moves to the widebody Chicken.
### Engine board
- Engine NB EIS = min(fps, NGSA) = 2037, so the engine game is UNCHANGED by the fps delay (1 pure: CFM Ducted Only + Do Nothing GEnx; PW GTF2 Solo locked; RR UltraFan NB Solo + Do Nothing Trent; 19 near). CFM's "4-Partner Embraer" move exists in code (+5pp CFM NB share, counts as a project for strain) but is never in the 16 CFM moves the board evaluates (it keeps the first 4 combos per base move), so the board cannot value an Embraer partnership.
### Vacuum and entrant (board conventions)
- Board shares imply Airbus builds 2000 x 80% = 1,600 NB/yr from 2043 if fps is 2044 (vs ~1,380-1,440 if fps 2041). Airbus's own FY2025 board report: rate 70-75/month by end-2027, stabilising at 75 (~900/yr).
- Unserved demand 2037-2056 if Airbus capacity = 1,200/yr (100/month): fps 2041 1,920 aircraft (peak 240/yr); fps 2044 5,040 (peak 400/yr); Boeing Do Nothing 6,860. At 900/yr: 7,720 / 11,040 / 12,860.
- Entrant NPV (board conventions: price $48M, margin 12%, WACC 10%, lump capex at EIS, 3-yr ramp, fills only unserved demand at 1,200/yr Airbus capacity): EIS 2038, $15B: fps 2041 -2.78 -> fps 2044 -0.51 -> Boeing Do Nothing +0.42. $20B at 2038 + a 10% fixed slice of the market: -1.35 -> +0.92.

### War-game evidence (our five-player engine, fps 3 years late, run wg5-2045d)
Round 1 identical to the on-time game; Round 2 Boeing chose a 787 Re-engine instead of fps (go/no-go failed: -0.73 vs $1B hurdle, slip test -4.71 vs -$2B floor), P&W cancelled GTF2; Round 3 Airbus shelved the A350 Re-engine while RR committed UltraFan WB. Final (game 2 vs game 1, $B): Boeing +1.68 vs +3.87, Airbus +44.54 vs +36.53, RR -3.68 vs -7.05, P&W -2.77 vs -2.77, CFM +18.99 vs +18.75. Boeing NB share fell to 32% (2045) and 25% (2050). CFM never used its Embraer-partnership lever in either game. Go/no-go by delay (war-game engine): 0y +9.93/+1.82 GO; 1y +5.62/-1.65 GO; 2y +1.70/-4.80 NO-GO; 3y -0.73/-4.71 NO-GO.

## Naming rules for anything user-facing
"Do Nothing" (never "Milk"), "Re-engine", "Delay Tactics" (never "Sabotage"), "Joint Venture"; never expose machine variable names (af_..., Milk_737MAX etc).
