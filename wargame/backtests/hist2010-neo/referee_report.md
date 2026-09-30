# Referee's efficiency report: `hist2010-neo`

History backtest, scenario `hist-2010-neo`, 4 turns (2010, 2011, 2012-13, 2014-15). Players: `boeing-2010` and `airbus-2010`. Each read a period-locked profile built only from evidence dated before 1 December 2010 (`wargame/profiles/boeing_2010/`, `wargame/profiles/airbus_2010/`). Market cell: `wargame-market`. Inject policy: umpire. The referee applied the historical inject path from the scenario's `referee_only` field: T1 `quiet_turn`, T2 `major_order_split`, T3 `boeing_787_setbacks`, T4 `order_boom`.

The game is over, so the scorecards and private fields are unsealed in this report. Every figure below is engine output, taken from `scorecard --final`, `report`, or a `whatif --side control` run by the referee (these are labelled). Where a number comes from a player's own `whatif`, the report says so.

---

## 1. Final result

**Final delta PV ($B, PV to 2010).**

| Side | Delta PV | NB operating | Capex | Strain | Program | EIS | Engine | Margin at EIS |
|---|---:|---:|---:|---:|---|---|---|---:|
| Boeing | -2.246 | +2.149 | -3.662 | -0.733 | `b737next` Re-engine, launched 2011 | 2017 (planned 2017, no slips) | PW1000G GTF | 0.135 |
| Airbus | +1.566 | +6.947 | -2.018 | -3.363 | `a320neo`, launched 2010 | 2015 (planned 2015, no slips) | PW1000G GTF | 0.125 |

Narrowbody share, 2030-2040: Boeing 45.4%, Airbus 54.6%. No cancellations. Delay Tactics and Poaching were disabled in this scenario.

**Scorecard (engine output, verbatim: `scorecard --run hist2010-neo --final --format md`).**

| Turn | Side | Orders | Value $B | Best response | Best $B | Regret $B | Capture | Prediction | Expectation error $B |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| T1 | boeing | rate increase | -4.34 | launch b737next (reengine) | -3.37 | 0.97 | 90% | 100% | -0.39 |
| T1 | airbus | launch a320neo | +7.87 | launch a320neo | +7.87 | 0.00 | 100% | 100% | +4.37 |
| T2 | boeing | launch b737next (reengine) | -2.30 | launch b737next (reengine) | -2.30 | 0.00 | 100% | 100% | +0.30 |
| T2 | airbus | no new moves | +1.35 | no new moves | +1.35 | 0.00 | 100% | 100% | -0.85 |
| T3 | boeing | no new moves | -2.30 | no new moves | -2.30 | 0.00 | 100% | 100% | +0.46 |
| T3 | airbus | no new moves | +1.35 | no new moves | +1.35 | 0.00 | 100% | 100% | -0.05 |
| T4 | boeing | no new moves | -2.25 | no new moves | -2.25 | 0.00 | 100% | 100% | +0.36 |
| T4 | airbus | no new moves | +1.57 | no new moves | +1.57 | 0.00 | 100% | 100% | +0.02 |

| Side | Mean capture | Total myopic regret $B | Prediction accuracy | Mean abs expectation error $B | Final delta PV $B | Hindsight regret $B |
|---|---:|---:|---:|---:|---:|---:|
| boeing | 98% | 0.97 | 100% | 0.38 | -2.25 | -0.21 |
| airbus | 100% | 0.00 | 100% | 1.32 | +1.57 | -1.20 |

**Plan-game benchmark (engine, `--final`).**
- Unique pure Nash: Boeing "b737next reengine T2" against Airbus "a320neo T1", payoffs -2.539 and +1.367.
- Best plans against the rival's actual play: Boeing "b737next reengine T2" (-2.455); Airbus "a320neo T1" (+0.37).

The historical path is the plan game's unique pure Nash. Section 4 explains why that matters.

---

## 2. Part A: did the agents behave like the real companies?

The real outcome comes from the scenario's `referee_only` field, plus the referee's knowledge of 2010-2017 history.

| # | Item | Real history | Game | Score |
|---|---|---|---|---|
| 1 | A320neo launch timing | Launched 1 Dec 2010 | Launched T1 (2010). Statement: "Airbus is launching the A320neo today." | **Match** |
| 2 | A320neo entry into service | Airbus's launch target was 2016, later brought forward to late 2015. First delivery (Lufthansa, PW1100G) came in January 2016, after early engine problems. | EIS 2015, disclosed every turn and held with no slips. | **Partial** |
| 3 | Boeing waits, then decides (2010-11) | Promised a choice by end-2010. Leaned towards an all-new airplane into early 2011. Decided mid-2011. | T1: no launch; public decision date "early in 2011"; defended the 737NG. T2 (2011): launch. | **Match** |
| 3a | *(extra)* 737 rate increases in 2010 | Three increases announced in 2010, to 38 a month in 2Q 2013 | T1 Rate Increase; disclosed 38 a month in 2Q 2013 | **Match (in-sample)** |
| 4 | Re-engine vs clean sheet | Re-engine (737 MAX); no clean sheet | Re-engine. Clean Sheet was the profile's T2 default; the §6 flip tests overturned it. | **Match** |
| 5 | Trigger: American Airlines split order, July 2011 | Record order split between Airbus (including the A320neo) and Boeing, conditional on a re-engined 737; Boeing committed at once | T2 inject `major_order_split`. Boeing cited it as "reaction trigger 3" and committed within the turn. | **Match (partly designed in; see Part B)** |
| 6 | MAX launch, Aug 2011 | Board approval, Aug 2011 | Launched 2011 (T2) | **Match** |
| 7 | MAX entry into service, May 2017 | First delivery in May 2017 | Planned EIS 2017; held, no slips | **Match** |
| 8 | Boeing engine choice | CFM LEAP-1B, sole source | PW1000G geared turbofan | **Miss** |
| 8a | *(extra)* Airbus engine choice | Two engines offered from launch (CFM LEAP-1A and PW1100G); the first aircraft delivered was GTF-powered | GTF only; the engine table allows one engine per program | **Partial** |
| 9 | No cancellations | Neither program cancelled | Neither side cancelled in T3-T4 | **Match** |
| 10 | Boeing: "no all-new single-aisle this decade" | The MAX was the 2010s answer; no clean-sheet single-aisle launched in the 2010s | T2: "remains under study for a later date". T3 and T4: "Boeing does not plan to launch an all-new single-aisle airplane this decade." | **Match** |

Tally: 8 of the 10 required items match, 1 is partial (neo EIS) and 1 misses (Boeing engine). Of the two extras, 1 matches in-sample (3a) and 1 is partial (8a).

**Notes on each item.**

1. **Neo launch (match).** Airbus's waiting test in its own `whatif` showed launching in 2010 beating 2011 against every Boeing response. The profile's Quick card default was also "launch in 2010". The engine and the doctrine agreed, so this match says little about behaviour.

2. **Neo EIS (partial).** The 2015 date is set mechanically: 2010 plus 5 development years, which equals the engine's `tech_ready_year`. The Airbus profile's hard rule is "never disclose an EIS before 2015". The one-year gap has two causes:
   - the game counts in whole years, while the real slip was about a quarter;
   - the historical cause, early PW1100G maturity problems, had no counterpart in this scenario's inject deck.

3. **Wait, then decide (match).** This is the most behaviourally informative match (section 4). In the T1 stage game, launching a Re-engine was Boeing's best response: -3.37 against -4.34 for its orders. Boeing still waited, citing trigger 1 ("Airbus announces a re-engine: no launch that turn; decide within about a year"). The real delay was longer: the promised end-2010 decision came in mid-2011. The game's one-year turn cannot resolve that.

3a. **Rate Increase (in-sample match).** The 38-a-month announcement is itself in the evidence (B-0284, Oct 2010), so this reproduces known behaviour rather than forecasting it. It still counts for doctrine, because the engine charges for it (section 5).

4. **Re-engine vs clean sheet (match).** The engine's gap was large. In the referee's control-view `whatif`, Rate Increase plus a 2011 Clean Sheet (LEAP) scores -11.345, against -2.246 for the actual path. The historical debate was closer than the engine makes it. Still, the mechanism matched history: the profile's documented 2010 lean to a new airplane was overturned by customer defection (flip test (b)).

5. **The trigger (match, partly designed in).** The referee placed the inject in T2 to follow history. Its text carries a penalty clause ("unless Boeing has committed ... it loses 3 pp of narrowbody share for five years"). The Boeing 2010 profile's §6 also contains a rule keyed to this inject id ("`major_order_split` inject. Commit within that turn"). The response was therefore partly scripted before the game began.

6-7. **MAX launch and EIS (match).** 2011 launch plus 6 development years gives EIS 2017, after the 2016 `tech_ready_year`. The year-level match is again partly parameter-driven.

8. **Boeing engine (miss).** The cause lies in the scenario's engine table, not in any departure from the profile.
   - **The engine table.** `pw_gtf` carries +0.5 pp margin, `eis_add` 0 and a 0.95 capture multiplier. There is no 737 installation constraint. In reality the 737's low ground clearance limits fan diameter: the 737 Classic already needed a flattened CFM56-3 nacelle, and the MAX needed a LEAP-1B with a smaller fan plus a longer nose gear. Under the share rule, the capture multiplier applies only to the first product into service. Boeing entered second (2017 against 2015), so in the model the GTF was pure margin upside with no penalty.
   - **The size of the effect.** In the referee's control-view `whatif`, the historical engine path (Rate Increase 2010 plus Re-engine 2011 with LEAP) scores -2.890, which is -0.644 against the agent's path. The table rewarded the miss.
   - **The profile.** The Boeing 2010 profile records "Gap: engine choice. Nothing covers narrowbody engine selection". It sets `cfm_leap` as the default, with an inferred flip to `pw_gtf` if the GTF adds more than $0.5B and no maturity problem is public. The flip fired at +$0.633B (Boeing's own `whatif`). In Turn 2 the Boeing agent searched its evidence for ground-clearance, landing-gear and fan-diameter terms and found nothing relevant.
   - **The market cell flagged the risk independently.** In its Turn 2 multiplier reasoning, returned to the referee, it wrote: "Fitting a large-fan first-generation GTF under the low-slung 737 carries installation risk". Its public narrative added that the GTF "breaks engine commonality with an all-CFM56 737 fleet". It set `b737next` at 0.95, but noted itself that "under the share rule, this multiplier only matters if the 737 Re-engine enters service before the A320neo". The flag therefore had no effect on payoffs.

8a. **Airbus engine (partial).** The GTF was the historically expected A320 re-engine engine (B-0261) and the first to enter service. Airbus's real policy, however, was two engines. The market cell priced that gap from Turn 1 ("a GTF-only offer ... shuts out CFM-loyal operators").

9. **No cancellations (match).** Both sides' cancel tests showed Keep dominant throughout. Per the players' own `whatif`, Keep beat Cancel in T3-T4 by $3.3-4.3B for Boeing and $8.7-11.0B for Airbus against the rival's actual moves. The tests were not close.

10. **"No all-new single-aisle this decade" (match).** Boeing hardened "under study" into a pledge in T3. Its rationale cites the T2 market report, which said talk of a later all-new jet gave some buyers a reason to wait. The market cell credited the pledge in T3 ("removes the main reason 737 operators had to wait").

---

## 3. Part B: validity caveats

1. **Training-data contamination.**
   - The underlying model knows this history. The profiles were time-locked, and every rationale ends with a declaration that later knowledge was set aside. Contamination still cannot be excluded, so a match is weaker evidence than it looks and a miss is informative.
   - The engine miss is the strongest sign that the agents followed the engine and their profiles rather than recollection. A player importing hindsight would have picked LEAP. The Boeing agent picked the GTF on a +$0.633B figure.
   - The one forecast where hindsight would have helped most was Airbus's T2 prediction of a Boeing Re-engine. It departed from its profile's prior ("a clean sheet somewhat more likely"). Its stated reasons were pre-2010 evidence plus an engine gap of about $8B between Re-engine and Clean Sheet, which makes the call defensible without hindsight. It is still not diagnostic either way.
   - Conversely, the evidence-only rule suppressed a real pre-2010 engineering fact, the 737's ground-clearance limit. The agent looked for it in its evidence and did not use general knowledge when it found none.

2. **Design-level contamination.** The scenario, the inject deck and the profiles were written by people who knew the outcome.
   - The inject deck contains a close analogue of the AA order, with a commit-or-lose-share clause.
   - The referee applied the historical inject path.
   - The Boeing profile has a rule keyed to that inject id and a T3 default of "`reengine` is the doctrinal choice".
   - The engine's plan game has the historical path as its unique pure Nash.

   Together, these mean a PV-maximising agent would reproduce most of the timing and the variant without any behavioural profile. The informative tests are the moves where doctrine pulled against the engine: the T1 wait and the T1 Rate Increase.

3. **The economics are illustrative placeholders.** The scenario's narrowbody volume, price, margins, capex ($2.5B Re-engine, $18B Clean Sheet), strain and engine terms are illustrative, not calibrated to either company.
   - Delta PV is measured against a baseline in which nobody moves. Boeing's -2.246 is not a forecast of value destroyed. It reflects the A320neo's share capture, which Boeing's best available plan could only reduce.
   - The engine resolves time only to the year, so a January 2016 EIS and a 2015 target look a full year apart.

4. **Why hindsight regret comes out negative.**
   - The plan-game grid (`solver.plan_game`) tries only default engines (`cfm_leap`) and launches in the first year of each turn. The per-turn stage game has the same limit (`solver.stage_candidates`).
   - Both players chose the GTF, so each actual play lies outside the grid and beats every plan the grid tried:
     - Boeing: actual -2.246 against the grid's best of -2.455 (LEAP, no Rate Increase), giving -0.21;
     - Airbus: actual +1.566 against the grid's best of +0.37 (LEAP), giving -1.20.
   - A negative value means "better than the grid", not "better than optimal".
   - To test this, the referee ran a supplementary control-view `whatif` sweep over each side's full plan space against the rival's actual play. Boeing had 125 plans: both variants, both engines, every launch year from 2010 to 2015, and the Rate Increase in any turn or never. Airbus had 13 plans: every launch year and both engines.
   - **Airbus:** its actual play was the best of its 13 plans, so its hindsight regret on the extended grid is zero.
   - **Boeing:** the best plan is a 2010 GTF Re-engine with no Rate Increase, at -1.826 (+0.42 against actual). A 2011 GTF Re-engine with no Rate Increase scores -1.832 (+0.414). Boeing's true hindsight regret is therefore about $0.4B. Nearly all of it comes from the Turn 1 Rate Increase; the one-year wait cost almost nothing.

5. **The levers thinned out after Turn 2.**
   - By the end of T2 both programs were launched, with engine and variant locked. Boeing's one-use Rate Increase was spent, Airbus had no rate lever, and Delay Tactics and Poaching were disabled. Turns 3-4 offered only keep or cancel, and cancel was dominated by billions.
   - The T3 787-setback inject prices only new Boeing programs, and Boeing had none left to launch. The T4 order boom moved values but no decisions.
   - T3-T4 capture (100%) and prediction (100%) were near-automatic. Those turns tested statements and disclosures, not decisions.

6. **The calibration metric compares unlike quantities.** Expectation error is the engine's projection after the turn, which assumes nobody moves again, minus the player's expectation. In T1, Airbus reported a path-weighted expectation (+3.5), placing 80% weight on a Boeing launch in 2010-14. The T1 projection (+7.874) assumed Boeing would never launch. Hence the +4.37 error. Airbus's +3.5 lay between that projection and the final +1.566. Boeing's errors (+0.30 to +0.46 in T2-T4) come from a private slip allowance of 0.5-0.6 years that the profile prescribes (§3). The engine rolled no slip.

7. **Process notes.** Two tooling commits landed during the run:
   - `297c9e2` narrowed the isolation-hook patterns during T1;
   - `ea49e23` made `whatif` reject wrongly shaped overrides after T2, a defect the Boeing player found.

   Neither touches payoff code: the diffs are limited to `.claude/hooks/wargame_isolation.py` and input checks in `wargame/engine.py`. All four adjudications returned `status: ok` with no warnings.

---

## 4. Efficiency verdicts

### Boeing (`boeing-2010`)

- **Value capture and regret.** Mean capture 98%, total myopic regret $0.97B, all of it in T1. Against the stage-game best response (a 2010 LEAP Re-engine at -3.37), Boeing's orders (Rate Increase, no launch) scored -4.34. T2-T4: 100% capture, zero regret. The T2 launch (Re-engine, 2011, GTF) was the engine's best response. By Boeing's own `whatif`, it was $2.08B better than Do Nothing and $8.52B better than the Clean Sheet default.
- **Hindsight regret.** -0.21 on the official grid, an artefact of the grid (Part B.4). On the referee's extended sweep, about $0.4B, almost all from the T1 Rate Increase.
- **Situational awareness.** Prediction accuracy 100% in every turn. T1 put a 90% probability on an Airbus launch in 2010 and was right. T2-T4 correctly called no Airbus moves; those were low-difficulty calls once the only rival lever was cancel.
- **Calibration.** Mean absolute error $0.38B. T1 -0.39. T2-T4 +0.30, +0.46, +0.36: a consistent pessimism from the private slip allowance, which is the profile's prescribed prior (§3). The allowance was reasoned and disclosed in the rationale. It was systematically biased only because no slip occurred.
- **Information use.** 14 disclosures across four turns (engine count).
  - Rate figures, decision timetable, launch facts, EIS 2017 held, no all-new single-aisle this decade, engineering ring-fenced from 787 work, staff embedded at Pratt & Whitney, further rate increases under study.
  - Referee notes: launch, EIS and rate facts were "consistent with the public record"; specific rate figures and all intentions were "not publicly verifiable". None was contradicted.
  - The T1 promise to decide "early in 2011" was kept in T2, which built credibility. The T3 no-clean-sheet pledge was strategic: the market cell credited it. The ring-fencing claim was flagged by the market cell as unverifiable. Boeing disclosed no thresholds and no slip allowance.
- **Discipline.**
  - All four order sets passed `validate` on first submission. No referee-side rejection, no retry, no discipline fault.
  - The isolation hook blocked 6 tool calls: 4 were `whatif --help` without `--side`; 1 was a helper script whose text tripped a pattern. The sixth, in T2, was a combined grep of engine source and listing of `wargame/scenarios` and `wargame/config`, described as "Find how order-split inject is modelled". No scenario file was read, and the player then used permitted reads of engine source.
  - The same turn, the player found the silent-override defect in `whatif`.
  - Every rationale carries a time-lock declaration.
- **Doctrine fidelity: high.**
  - T1 matches the Quick card exactly: no launch, a public decision date, Rate Increase.
  - The Rate Increase departed from PV-best, and Boeing declared a doctrine premium of about $0.45-0.70B, citing the $1B override threshold. The extended sweep prices the Rate Increase at about $0.41B in hindsight, so the premium was well sized.
  - T2 applied the §6 flip tests as written: (b) and (c) fired, so Re-engine; the GTF cleared the $0.5B engine flip bar. It committed within the `major_order_split` turn as §6 requires.
  - T3 applied the 787-setback rules (no launch, never cancel). T4 applied the B-0153 cancel test.
  - No hard rule was broken. The one-year overlap with 787/747-8 development was priced ($0.733B strain) and argued as non-overlapping engineering peaks, which the profile allows.

### Airbus (`airbus-2010`)

- **Value capture and regret.** Mean capture 100%, zero myopic regret. T1 launch (2010, GTF) was the stage-game best response. By its own `whatif`, the GTF beat LEAP by $1.04-1.35B in every case, and a 2010 launch beat 2011 against every Boeing response. T2-T4 hold was the best response each turn.
- **Hindsight regret.** -1.20 on the official grid (grid artefact, Part B.4). Zero on the referee's extended sweep: its actual play was its best available plan.
- **Situational awareness.** Prediction accuracy 100% in every turn. The T1 call (Rate Increase, no Boeing launch) followed its profile's prior. The T2 call, a Boeing Re-engine in 2011, departed from that prior with explicit reasons and was right. It was the hardest correct forecast in the game.
- **Calibration.** Mean absolute error $1.32B, driven by T1's +4.37. That error reflects a path-weighted expectation measured against a stage projection (Part B.6). T3 and T4 errors were -0.05 and +0.02. T2's -0.85 came from Airbus keeping 50% weight on a Boeing wait or clean sheet in the very turn Boeing re-engined.
- **Information use.** 14 disclosures (engine count): EIS 2015 each turn; the PW1000G; the split order; self-funding without new launch aid; raising A320-family production; joint engine-maturity work with Pratt & Whitney.
  - Referee notes: EIS, engine and the split order were "consistent with the public record". Self-funding, the production claims and the Pratt & Whitney work were "not publicly verifiable". The production claims were unverifiable because Airbus has no rate lever in this scenario. None was contradicted.
  - The self-funding pledge was strategic: the market cell cited it when it raised the `a320neo` multiplier from 1.05 to 1.08 in T2.
  - Disclosures after T2 largely repeated earlier ones, so they carried little new information. Airbus disclosed no thresholds, prices or rate figures, as its profile directs.
- **Discipline.**
  - All four order sets passed `validate`; T2 was validated twice, both ok. No rejection, retry or fault.
  - The hook blocked 5 calls: 4 were `--help` calls without `--side`, and 1 in T1 was a false positive on a print label (fixed by `297c9e2`). There were no attempts on rival files or run state.
  - In T4 it noticed that `whatif` ignored a `slips` field. It said so in its rationale and used a Turn 1 proxy instead.
  - Every rationale carries a time-lock declaration.
- **Doctrine fidelity: high.**
  - T1 matches the Quick card: launch in 2010, engine by the §9 test, EIS 2015, a bold statement. The GTF lead exceeded the $0.3B tie band, and the share-over-margin bias was weighed against the §9 $1.0B premium cap and correctly set aside.
  - T2-T4 matched the reaction rows: hold, no cancel. The hard rule "never disclose an EIS before 2015" was respected.
  - No doctrine premium was taken or needed.
  - Fidelity here is to rules inferred from 28 Boeing-sourced items, not to documented Airbus behaviour.

---

## 5. Comparative ranking

1. **Airbus: first on efficiency.** It had zero regret on every grid and made the hardest correct prediction. Its decision problem was simpler: one dominant move (launch now with the GTF), then hold.
2. **Boeing: second on the numbers, faithful on doctrine.** Its entire myopic regret ($0.97B) and extended hindsight regret (about $0.4B) trace to the T1 Rate Increase. That move was a declared doctrine premium and the real 2010 behaviour, so it reflects the company, not a blunder. Net of declared doctrine, Boeing's play was PV-optimal in T2-T4, and its launch timing cost almost nothing (a 2011 launch scores -1.832 against -1.826 for 2010).
3. **Skill and doctrine separated.**
   - *Skill:* both players showed clean discipline and zero contradicted disclosures. Boeing's calibration was tighter. Airbus's T2 forecast was sharper.
   - *Doctrine:* both profiles drove the orders. Boeing's T1 wait and Rate Increase are the only doctrine-over-PV moves in the game, and both match history.
4. **Historical fidelity.** Boeing matched history on every item except the engine, and that miss traces to the engine table and the profile's evidence gap. Airbus matched launch and hold. Its EIS and single-engine choice are partial matches, both constrained by the scenario.

---

## 6. What to improve before the next backtest

1. **Add the 737 fit constraint to the engine table.** Make engine options program-specific. Give `pw_gtf` on `b737next` an installation penalty (capex, `eis_add` or ineligibility) and some value for LEAP commonality with the CFM56. Let the engine and market capture multipliers bind for followers too, so installation-risk flags can affect payoffs.
2. **Give Airbus a rate lever** that mirrors Boeing's Rate Increase. Airbus said three times that it was raising production, and each time the note had to read "not publicly verifiable".
3. **Widen the plan grid and the stage-game menu.** Cover non-default engines and every launch year, so hindsight and myopic regret cannot go negative by construction. The referee's 125-plan and 13-plan sweep ran in seconds.
4. **Add Airbus-side evidence.** Use Airbus and EADS annual reports, press releases and air-show statements from 2006-2010, especially on engine sourcing (dual-source policy), rate policy and the neo business case. The current Airbus profile rests on 28 items, all seen through Boeing.
5. **Add Boeing engineering context.** Add pre-2010 evidence on 737 engine integration (ground clearance, the CFM56 incumbency) so the Boeing profile's engine gap closes without hindsight.
6. **Reduce design-level contamination.**
   - Keep inject ids out of profile rules.
   - Pre-register the inject path, or run it with `--auto`.
   - Add a counterfactual run without `major_order_split` to test whether Boeing still re-engines.
7. **Model more of what happened.** Add a GTF-maturity inject and allow two-engine offers. Add a `slips` override to `whatif`. Score calibration against a path-consistent projection. Give Turns 3-4 live levers (rate steps, variants) so they test decisions, not only statements.
