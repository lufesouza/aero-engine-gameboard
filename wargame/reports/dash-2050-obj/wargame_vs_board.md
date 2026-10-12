# How the war game deviates from the game-theory board

Run `dash-2050-obj`, played on board v3 (`runs/dash-2050-obj/board.txt`). All values are the change in present value against the status quo, in $B at 2026. "The board" means `combined_dash.py` at the Game_v3 snapshot. "The war game" means the `dashgame/` engine plus the player agents. Every number below was computed in python3 by the research passes, and section 7 lists the scripts.

## 1. Answer first

The war game uses your board as its pricing engine. For the airframers the values are exact: Boeing's +0.66 and Airbus's +23.37 are the board's own cell, read at the dates the game produced (`report_data.json` key `board_check`; report 4000–4001).

**(a) How values are computed.** The war game differs in two places:
- Dates come from launch year plus development time, not from sliders. fps entered service in 2040 rather than 2041, which is worth +0.73 to Boeing and −1.68 to Airbus.
- The engine makers are priced by a year-by-year re-implementation. It adds legacy engine slots, a yearly narrowbody split and a Joint Venture the board cannot form. This puts CFM +8.46, P&W −3.59 and RR −5.31 away from the nearest board cell.

**(b) How the game is played and decided.** This differs more:
- four sealed rounds instead of one matrix;
- five players, each seeing only its own payoffs;
- Delay Tactics are covert;
- engine makers can launch conditionally;
- engine codes become a free choice for the airframers;
- every player is an executive committee plus a Board, with doctrine and objectives the board does not price.

**(c) What actually happened.** The played cell was: both airframers launch, nobody re-engines, and nobody uses Delay Tactics. That cell is on none of the board's equilibrium lists. It is also not on the game master's stage-game lists for 2030 or 2035. Airbus gave up 3.30 in 2030 and 3.19 in 2035; Boeing gave up 2.20 and 0.65. Most of that came from the companies' own rules.

On this run, two things matter most: the engine model (the Joint Venture and the legacy slots) and the players' doctrine. The game-master adjustments for cancellations and Delay Tactics never fired.

## 2. Same engine, different bookkeeping

**What the board does here.** The war game runs the board headlessly and stops after each board's equilibrium bookkeeping (`harness.py` 17–25, 96–117).

**What the war game adds.**
- Each game state is mapped to one airframer cell, read at that state's dates (`model.py` 60–65, 321–334).
- The engine makers are not valued with the board's engine simulation. They are valued with a year-by-year copy that uses the board's parameters and share rules (`model.py` 110–118, 565–638; `combined_dash.py` 2774).

| Deviation | Board does | War game does | Size on this run | Where it comes from |
|---|---|---|---|---|
| Entry-into-service dates | Sliders. One fps date for every ramp: fps 2041, NGSA 2037, Re-engines 2042 | Launch year + development time (fps 7 or 10 years, NGSA 7, Re-engines 5). A programme never launched keeps the snapshot date. Dates outside the slider range are allowed | fps 2040, not 2041: **Boeing +0.73, Airbus −1.68** | `model.py` 220, 321–325; `rules.py` 156; `combined_dash.py` 953–956, 986–989; `harness.py` 50–58 |
| Cancellation | No cancel move | Write-off of bill × years elapsed ÷ development years, discounted, plus the debt penalty | 0 (none). Counterfactual, Boeing cancels fps 10-yr in 2035: −18.33, against −3.64 for the board's Do Nothing cell (write-off 30.16 nominal, 12.28 present value, plus 2.41 debt penalty) | `rules.py` 131–139; `model.py` 384–387 |
| Delay Tactics spend and fine | $1B a move over the 9 years before the fps date. $48.32B fine in any cell where Boeing has no fps | Spend starts no earlier than the order year. Fine only if fps is never launched in the whole game; waived if fps is launched and then cancelled | 0 (never ordered). Counterfactuals for Airbus: ordered 2035, +0.08; ordered 2045 against an fps never launched, +4.29; ordered 2030 with fps cancelled in 2035, +15.19 | `combined_dash.py` 1108–1122; `model.py` 337–345, 368–382 |
| Debt penalty, two-front strain | Charged on the board's spend | Same formulas, applied to spend plus write-offs and to the re-timed Delay Tactics | 0 | `model.py` 91–98, 386–388 |
| 737 rate increase | A strategy | Same pricing, but it can be ordered only in 2030 | 0 (not ordered) | `rules.py` 54; `model.py` 393 |
| Covert view | n/a | Payoffs include Delay Tactics; the public view leaves them out | 0. Counterfactual with Delay Tactics in 2030: the public view overstates Boeing by 1.44 and understates Airbus by 1.57 | `model.py` 326; `gm.py` 94–95, 108–109 |
| Legacy engine slots | Code-based start shares from the switch date | 737 flies CFM only, and A320neo flies P&W + CFM, until each new airframe enters service | 2037–2039 at 50/50: **CFM +11.12, P&W −4.72, RR −4.72** | `model.py` 557–562 |
| Narrowbody split between airframers | Fixed 50/50; start shares rounded to whole percent | Boeing's narrowbody share each year from the airframer trace; exact fractions | **CFM −2.66, P&W +1.13, RR +1.13**. Acts only in 2037–2039 | `model.py` 203–215, 597; `combined_dash.py` 733–745, 2411–2420 |
| Joint Venture fold-in | n/a | Solo spend above the maker's Joint Venture share is written off, undiscounted. The Joint Venture inherits the earliest ready date of the solos it absorbs. An absorbed solo still counts as ready when engines are fitted | **RR −1.71**, P&W 0. Joint Venture ready in 2036 instead of 2041 | `rules.py` 222–238; `model.py` 288–297 |
| Engine readiness and fitting | Codes fit as given; moves count from the switch date | Each programme has a ready year. A maker is dropped if it is not ready by entry into service; CFM is the fallback | 0 (all three makers fitted on both airframes) | `model.py` 226, 236–240, 281–317, 504–530 |
| Narrowbody switch year | Earlier of the two slider dates, even if nobody launches | Only once an airframer has launched | 0 (2037 both ways). If nobody launches: war game 0 / 0 / 0, board −51.21 / +20.34 / +19.47 (with P&W also at Do Nothing) | `model.py` 494–495, 599–601 |
| UltraFan widebody | Counts from the widebody date | Counts only once a Re-engine is in service | 0. Counterfactual with a 2035 launch: RR −9.00 in the war game, against −7.06 on the board | `model.py` 528–530 |

**How it adds up on this run.**
- **Airframers.** No game-master term fired, so the whole difference from the snapshot is the fps date.
  - Boeing's value bridges as narrowbody profit +20.30, investment −14.91 and debt penalty −4.73.
  - Airbus's bridges as +39.13, −15.23 and −0.53.
  - Source: the engine research bridge, `model.py` 452–455.
- **Engine makers.** The comparison point is the board at codes 7/7, at the war game's dates, with both Joint Venture moves forced: −78.15 / +12.47 / +37.66.
  - The war game's −69.69 / +8.88 / +32.35 differs from it by +8.46 / −3.59 / −5.31.
  - That gap is the legacy slots, plus the split, plus RR's write-off. Each part is rounded separately.
  - With the legacy slots switched off and no write-off, the war-game engine model at 50/50 gives that board cell exactly.

**Our view: the Joint Venture result hangs on the 2030 "launch if selected" solo programmes.**
- Without the inherited 2036 ready date, the outcome would shift by CFM +8.64, P&W −5.47, RR −1.82.
- Without the solo programmes, the Joint Venture would be fitted to neither airframe: CFM +90.33, P&W −34.95, RR −33.23 (`rules.py` 235–238; `model.py` 288–297).

## 3. A different game

| Feature | Board | War game | Consequence (our view) | Run example | Where it comes from |
|---|---|---|---|---|---|
| Turn structure | One-shot choice of complete strategies: 256 airframer cells; 16 × 6 or 16 × 9 engine cells | Four sealed, simultaneous rounds (2030, 2035, 2045, 2050); the state carries forward | Development lead times decide the game early | Every Board item fell in 2030 or 2035. In 2045 and 2050 all five companies held every order | `rules.py` 10; `gm.py` 81–93; `record_r3.json`, `record_r4.json` key `log`; `exco_result_r1–4.json` key `board_items` |
| Players | Two separate games. P&W is not a player; the engine codes lock its move | Five players order in the same round. Airframer payoffs still do not depend on engine moves | P&W becomes a decision-maker | P&W ordered GTF2 "launch if selected" in 2030 and a Joint Venture commitment in 2035 | `combined_dash.py` 2389–2398, 2657; `rules.py` 13–30; `record_r1.json`, `record_r2.json` key `orders` |
| Information | The analyst sees every payoff | A bulletin, plus a brief with only the player's own payoffs, set against a few scenario columns chosen by the game master | Players best-respond to beliefs, and the scenario menu bounds what they can expect | 2030 grids: Boeing 16 × 5, Airbus 12 × 6, CFM 22 × 6, P&W 6 × 7, RR 18 × 9. No engine maker's grid had both airframers on code 7, which is what happened. Airbus expected +45.82 and got +23.37 | `briefs.py` 593–695, 863–865; `rules.md` 3–5; `grids_r1.json`; report 285–286 |
| Engine codes | Analyst input (7 and 6) | An airframer order, changeable until entry into service. It costs the airframer nothing | A free lever that swings the engine makers by tens of billions | Boeing moved from code 3 in dash-2050-exco to 7 here. Boeing unchanged; CFM −31.40, P&W +11.81, RR +11.81 | `Game_v3.txt` 17–19; `rules.py` 199–213; `briefs.py` 524–525; report 3796, 3825–3829 |
| Conditional engine launch | None | Launches only if a live airframe selects the maker and the engine is ready in time | Engine makers in effect move after the airframers, at no cost if not selected | Both fired in 2030, on codes 7 and 7 | `rules.py` 239–254; `record_r1.json` key `log` |
| Joint Venture | Only when an airframer picks code 4. That forces P&W in, and only then offers RR the move | Standing commitments; forms once both commit, whatever the codes | Committing was free and weakly dominant on each grid | Both committed in 2035, each putting 0.10 on the other committing. On the grids, committing against Do Nothing was worth up to +5.51 for P&W and +2.28 for RR. P&W expected +0.39 and got +8.88 | `rules.py` 214–238; `exco_result_r2.json` (predictions); `grids_r2.json`; report 287 |
| Delay Tactics | A visible strategy, with the $48.32B fine where Boeing has no fps | Covert until the end of the game; the spend and the fine are re-timed | The board's equilibria lean on a move that Airbus's doctrine keeps off | Never ordered. In 2030, one move was worth −15.74 in the column where Boeing holds | `rules.md` 136–140; `model.py` 368–382; `grids_r1.json` key `airbus`; `state_r4.json` key `dt` |
| Who decides | One payoff-maximiser per side | Board guidance, then the CEO's frame, the finance and operations tests, the CEO's decision and a veto check. The Board then reviews every non-default order | Options with more downside are struck before the CEO chooses | The test memos marked 60 vetoes binding (Airbus 22, CFM 16, RR 11, P&W 8, Boeing 3); none was invoked against a chosen order. 0 Board vetoes in 20 company-rounds | `exco_round.js` 5–15, 37–89, 217–231; `exco_result_r1–4.json` keys `cfo.vetoes`, `ops.vetoes`, `board_vetoed` |
| Doctrine | None | Boeing: −$1B downside limit per item, one development at a time, $2B premium cap. Airbus: rules 4 and 6, plus a stricter Delay Tactics condition. P&W: no engine without a committed airframer | Downside and worst-column tests push both widebody decisions to Do Nothing | See section 4 | `boeing-board.md` 112–114, 198–204; `profiles/airbus/dashboard_game.md` 88–97; `pratt-whitney-board.md` 216 |
| Objectives beyond value | None | Control's objectives are scored separately and never change a payoff. Value given up for them counts against a premium cap | Players give up value only inside their caps | Boeing's 10-year ramp kept its stress-case debt line (premium $0.46B). RR declined the $8.31B it would have cost to keep its $4B line | `objectives.txt`; `briefs.py` 315–340; `finance.py` 3–4; `exco_result_r1.json` |
| Unpriced moves | None | 137 other moves and the public statements are recorded but never priced | Words carry signals at no cost | Boeing's 2030 line "Engine competition with CFM as the baseline" | `gm.py` 97–100; `rules.md` 45–48; `record_r1.json` |
| Equilibrium tolerance | 1 yield point ($1.30B for Boeing, $1.50B for Airbus). 5 points on the engine board ($8.0B for CFM, $5.5B for RR) | Game master's stage game: a flat $1B, engine makers held at their actual orders, never shown to players | A tighter test: 0.77 and 0.67 yield points | See section 4 | `combined_dash.py` 725, 1449, 1456, 2579; `stage_game.py` 17–39 |

## 4. What happened vs what the board predicts

**The board's prediction.** At the snapshot dates the board has 4 pure equilibria with 2 distinct value pairs (`Game_v3.txt` 112–138; `report_data.json` key `board.airframer_pure`):
- In all four, Boeing launches fps 10-yr and Airbus launches NGSA with one Delay Tactics move.
- Exactly one widebody is re-engined. Boeing −2.50 / Airbus +28.24 when Airbus re-engines the A350; −0.79 / +26.13 when Boeing re-engines the 787.

**The played cell on the board's own dates** is worth −0.06 / +25.05:
- Boeing's best deviation, the 787 Re-engine, gains 0.57. That is 0.44 yield points, inside the band.
- Airbus's best deviation, the A350 Re-engine plus one Delay Tactics move, gains 3.19. That is 2.12 points, outside the band.
- So on the board alone, only Airbus breaks equilibrium.

| Round | Game master's stage-game pure equilibria (Boeing / Airbus) | Played | Boeing regret | Airbus regret | Why, from the records |
|---|---|---|---:|---:|---|
| 2030 | Do Nothing on the 787 / A350 Re-engine + one Delay Tactics move: −3.40 / +26.67. Or 787 Re-engine / one Delay Tactics move: +1.42 / +24.08 | +0.66 / +23.37; not even near | 2.20 | 3.30 | **Boeing:** the Board's −$1B downside limit (the Re-engine is −3.58 in the A350 Re-engine columns) and its one-development rule. It also wrongly expected an A350 Re-engine. **Airbus:** Delay Tactics deleted under rule 4 (fps not yet public, so the $48.32B fine applies). The A350 Re-engine was its best plan even in its expected column (+1.75), but red-line rule 6 (two launches with a 5-year overlap) and the peak-cash test struck it |
| 2035 | −2.24 / +26.56, or −0.13 / +24.54 (same two patterns) | hold / hold; not near | 0.65 | 3.19 | **Boeing** forecast correctly and held on its overlap rule (5 years against a 2-year limit). **Airbus:** integrity concerns on the bottleneck move, the cash test on poaching, and the Re-engine's peak cash $1.47B over the line |
| 2045 | +0.34 / +24.26, or +0.96 / +23.26 | hold / hold; the only near-equilibrium | 0.29 | 0.89 | **Boeing:** "+0.30 is inside ε ($1B), so the plan with less to execute wins". **Airbus:** short of its $1B launch test by $0.11B, and no widebody engine ready in time |
| 2050 | +0.57 / +23.94, or +0.71 / +23.33 | hold / hold; the only near-equilibrium | 0.04 | 0.57 | **Airbus:** two binding soft vetoes. **Boeing:** logged a $0.05B premium |

Sources: `stage_r1–4.json` keys `pure`, `near_within_1b`, `played`, and the best-response keys; `exco_result_r1–4.json` keys `decision.rationale` and `board_guidance.would_veto`.

**Whole game against the two 2030 equilibrium paths.** From either 2030 equilibrium, rounds 2–4 have one pure equilibrium, hold / hold (`eqpath.json` key `eq_paths`).

| Player | Played (`state_r4.json`) | Path A: Airbus A350 Re-engine + Delay Tactics | Path B: Boeing 787 Re-engine, Airbus Delay Tactics |
|---|---:|---:|---:|
| Boeing | +0.66 | −3.40 | +1.42 |
| Airbus | +23.37 | +26.67 | +24.08 |
| CFM | −69.69 | −69.29 | −69.29 |
| P&W | +8.88 | +8.88 | +8.88 |
| RR | +32.35 | +31.98 | +31.98 |

The engine makers' shifts of +0.40 and −0.38 come from the Re-engine, not from Delay Tactics (`decomp.json`).

**Engine makers.**
- The board's pure equilibrium at codes 7/6 is CFM Ducted with Do Nothing on GEnx, RR UltraFan NB Solo with Do Nothing on Trent, and P&W locked to GTF2 Solo. It is worth −62.65 / +18.34 / +17.25 (`Game_v3.txt` 204–218).
- What they played:
  - CFM: Ducted + Partner Embraer + the GEnx upgrade. That is +3.43 against Ducted alone.
  - P&W and RR: launch-if-selected solos, then the Joint Venture in 2035. That is +5.51 for P&W and +2.29 for RR against staying solo.
- Their regret against the information they had is 0 in every round. RR's hindsight regret, 1.71, is its write-off (`report_data.json` key `regret`).

**Who deviated and why.**
- Airbus deviated most (3.30, then 3.19). Both times it passed up an A350 Re-engine plus one Delay Tactics move.
- Boeing's deviations (2.20, then 0.65) were all about the 787 Re-engine.
- **Our view: 2030 was decided by company rules first and beliefs second.**
  - Airbus's Re-engine was best in its own expected column and died on a red line.
  - Boeing's own grid showed the Re-engine at +2.20 in the column that actually happened. It held on a robustness rule.
- **Our view: the board's Nash prediction is not being tested.** On the widebody, Do Nothing was the plan with the best worst column: for Boeing every round, and for both sides from 2035. That looks like maximin. The exception is Airbus in 2030, where the A350 Re-engine had the better worst column, +19.03 against +17.28.
- **Our view: dropping Delay Tactics is built into the agents, not noise.**
  - The Airbus Board vetoes the bottleneck move and both moves (`airbus-board.md` 194).
  - The Airbus CEO's stricter condition keeps Delay Tactics off by default (`airbus-faury.md` 95).
  - dash-2050-exco played the same cells. The earlier dash-2050 run, on board v2 and before the executive-committee layer, did order the bottleneck move in 2035.
- **The result against the equilibria.** It leaves Boeing 0.76 and Airbus 0.71 short of path B. It is 4.06 better for Boeing than path A.

## 5. The board's snapshot vs the realised world

| Item | Board (Game_v3) | War game | Where it comes from |
|---|---|---|---|
| fps | 2041, one slider for every ramp | 10-yr ramp launched 2030, in service 2040 | `Game_v3.txt` 64; `state_r4.json` key `prog` |
| NGSA | 2037 | Launched 2030, in service 2037 | `Game_v3.txt` 65; `state_r4.json` |
| Re-engines | 2042 | Never launched, so valued at 2042. Reachable dates: 2035, 2040, 2050, 2055 | `Game_v3.txt` 66–67; `model.py` 323–325 |
| Engine codes | 7 / 6 | 7 / 7 | `state_r4.json` key `codes` |
| Long-run narrowbody split, Boeing / Airbus | 46 / 54 | 47 / 53 | `Game_v3.txt` 99 |

**Worked example: the played cell, with fps moved from 2041 to 2040** (NGSA 2037 and Re-engines 2042 in both solves; `variants.json` key `bridge_b`).

| Item | Boeing | Airbus |
|---|---:|---:|
| Narrowbody profit | +2.59 | −1.68 (NGSA's lead drops from 4 years to 3) |
| Bill booked a year earlier (the board books it as one lump at entry into service) | −1.42 | none |
| Debt penalty | −0.45 | none |
| **Change** | **+0.73** (−0.06 → +0.66) | **−1.68** (+25.05 → +23.37) |

Components are rounded separately. Moving the fps slider to 2040 on the board gives exactly the war game's values.

**Knock-on effects of the realised dates.**
- **Near-equilibria.** The board's Near-Nash count falls from 12 to 8. With fps a year earlier, Delay Tactics start a year sooner and are worth 1.56–1.57 instead of 1.45, which is 1.04–1.05 yield points instead of 0.96–0.97. That pushes the four cells without Delay Tactics just outside the band.
- **Boeing's Re-engine regret.** A 2030 Re-engine enters service in 2035, not 2042. This raises Boeing's 2030 Re-engine regret to 2.20. It would be 0.63 with only the fps date changed, and 2.40 with only the Re-engine date changed.
- **The two fps ramps swap rank.**
  - On the board, the 7-year ramp is 1.69 worse for Boeing.
  - Launched in 2030 in the war game, it is 0.46 better for Boeing and 6.08 worse for Airbus, because it removes NGSA's lead.
- **Board version.** v3 against v2 (`Game.txt` and `Game_v3.txt` 57–99):
  - fps bills 55.25 / 64.47 → 60.32 / 65.00;
  - NGSA bill 30.07 → 35.52;
  - Re-engine dates 2035 → 2042;
  - the fps 7-yr +5 pp share advantage replaced by a 1.0 pp-a-year lead edge;
  - equilibria 0 Pure / 17 Near → 4 / 12.
- **Our view.**
  - v2's Re-engine date matched the game's earliest reachable date; v3's 2042 does not.
  - At reachable dates (fps 2040, NGSA 2037, Re-engines 2035 or 2040), the board keeps 4 Pure and 8 Near-Nash, the same Chicken on the Re-engines, and Delay Tactics in every pure equilibrium.

## 6. What stays faithful

`test_model.py` passes on v3 for this run:
1. The trace and the extension to 2060 leave every airframer cell unchanged (4 date settings × 256 cells).
2. A snapshot-like state equals its board cell: Boeing −4.9694, Airbus 24.9407. Airbus Delay Tactics in 2030 against an fps never launched also equals the board: −15.7070.
3. The snapshot equilibria are reproduced: 4 pure and 12 near for the airframers, 1 pure and 11 near for the engine makers.
4. At 50/50, the start shares equal the board's unrounded derivation for all 49 code pairs.
5. In board mode, the engine re-implementation equals the board's engine simulation on 648 move combinations. One game state also matches it: CFM −65.3778, P&W 18.4325, RR 10.7416.

Further checks:
- The yearly trace reconciles to the board's present values within 1e-9 (`model.py` 452–455).
- 12 of 13 variant states equal the board cell at their own dates to 4 decimals. The 13th, Delay Tactics ordered in 2035, is +0.08 for Airbus (25.0207 against 24.9391), because of the re-timed spend.

**When the engine equality holds.** It needs all of these: a fixed 50/50 split, exact start shares, both narrowbodies entering service in the same year, every programme ready by its switch date, no Joint Venture outside code 4, no fold-ins or write-offs, and P&W's move equal to the code lock. This run breaks the split, legacy-slot, Joint Venture, P&W-lock and write-off conditions.

**Our view: loose ends.**
- **The published report's "dashboard alone" check uses a cell the board would never offer.** It gives −71.07 / +9.71 / +34.91 by pairing P&W's locked GTF2 Solo with RR's Joint Venture move. The report does bridge the difference. But its closing line claims exactness at 50/50, which is not true here: the legacy slots alone move CFM +11.12 (`reports.py` 223; report 3992–4012).
- **The same spend is phased three ways.**
  - The board books it as a lump at entry into service.
  - Write-offs are linear: fps 10-yr cancelled after 5 of 10 years writes off $30.16B.
  - The balance-sheet tracker uses a curve, on which $24.73B has been spent by then.
- **The debt penalty and the tracker disagree.** The penalty charges Boeing as if it carried $45B of debt (−4.73 here). The tracker has Boeing's net debt at its $0B floor from 2029 (`boeing_fin.json`).
- **Strain keeps a 7-year development window, even for fps 10-yr.** A 2030 787 Re-engine therefore pays −0.31 rather than −0.78. Boeing's 2030 gain would be +1.73, not +2.20 (`combined_dash.py` 1367–1375).

## 7. Where it comes from

- **Board:** `wargame/dashgame/board/combined_dash.py`, `harness.py`, `Game_v3.txt`, `Game.txt`.
- **Engine:** `wargame/dashgame/model.py`, `rules.py`, `gm.py`, `briefs.py`, `finance.py`, `stage_game.py`, `test_model.py`, `reports.py`, `workflows/exco_round.js`.
- **Run files:** `wargame/runs/dash-2050-obj/`: `board.txt`, `rules.md`, `objectives.txt`, `state_r4.json`, `record_r1–4.json`, `grids_r1–4.json`, `stage_r1–4.json`, `exco_result_r1–4.json`, `brief_r1_boeing.md`, `brief_r1_airbus.md`.
- **Report:** `wargame/reports/dash-2050-obj/dash_2050_obj_report.md` (cited as "report" + line), `data/report_data.json`, `data/boeing_fin.json`, `debrief/factpack.json`.
- **Agents and doctrine:** `.claude/agents/airbus-board.md`, `airbus-faury.md`, `boeing-board.md`, `pratt-whitney-board.md`; `wargame/profiles/airbus/dashboard_game.md`.
- **Analysis runs:** the research passes re-solved the board and replayed variant states in scratch scripts (not kept in the repo); every figure can be reproduced with the engine and board files above.
