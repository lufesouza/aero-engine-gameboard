# How each player behaves, and how that behaviour shaped the game

**Games covered:**
- `wg5-2045`: fps on time, in service 2038.
- `wg5-2045d`: fps three years late.

**How this was produced.** For each of the five players, one analyst covered three things, and an independent adversarial verifier then checked the files and re-ran every engine number:
- the evidence-built profile and the agent definition;
- every order, public statement, disclosure and private rationale in both games;
- engine counterfactuals that change one of the player's choices and measure all five payoffs.

A synthesis step resolved the remaining disagreements, all in the verifiers' favour (see Part 2, Appendix A).

**Reading the numbers:**
- $B are PV to 2026 at each player's own WACC.
- "Worth X" means as played minus the rejected alternative, with every other player's recorded orders held fixed.

---

# Part 1. Player by player

## Boeing: a gated, finance-led incumbent

**How the behaviour was built**
- **Sources:** 151 earnings calls, conferences and investor days (2006-2025); 16 10-Ks; the Goldman Sachs and Morgan Stanley Boeing models; Capital IQ. That gives 2,537 evidence items, 2,941 of 2,942 quotes machine-checked.
- **Executives:** 12 profiles with 1,874 items. The default team is Ortberg (CEO, 107 items, Oct 2024 to Oct 2025), Malave (CFO, 11 items from one call: low confidence) and Pope (Boeing Commercial Airplanes, 8 items: very low confidence; played by doctrine).
- **Objectives** come from the Boeing PD briefing: hold 50/50 in narrowbody and defend incumbency. The objective premium is capped at $2B.

**How it behaves**
1. **Readiness gates first.** No fps and no 787 Re-engine in round 1 (H1, H3), and no rate step under the round-1 supply crunch (H6). A new airplane comes "when the market, the technology and we are ready".
2. **The business case must close.** The fps go/no-go test requires beating Do Nothing by more than $1B, and losing no more than $2B to it in Malave's slip test. This makes Boeing a margin player, not a share player.
3. **One major development at a time** (H4). It never cancels (H5), absorbs shocks and never blames anyone.
4. **Commits only to a committed engine.** Its engine requirement is engine-neutral and names no maker.
5. **Treats the widebody as a game of Chicken.** It never follows an A350 Re-engine, and moves first when the field is uncontested.
6. **The rate step is gated on KPIs.** It is deferred under the supply crunch and taken in the first clean round.
7. **Voice:** calm and date-averse ("We're turning it. I don't think it's turned"; "right than fast"). It gives entry into service as ranges and corrects itself the next round.

**How that played and what it did**
- **Game 1:**
  - **Round 1, waited.** The rule's real cost was about $4.7B against an fps launched in 2028. The scorecard's "3.43 regret" is a stage-game number.
  - **Round 2, launched fps 2031 (Solo, 10-year ramp-up) with the rate step.** fps alone was worth **+$7.44B** to Boeing and cost Airbus **$11.31B**. The rate step cost Airbus $3.77B.
  - **Result:** incumbency defended (40.2%), +$3.9B.
- **Game 2:**
  - **Round 2, fps rejected.** The same go/no-go test rejected the delayed fps: −0.73 against Do Nothing, and −4.71 in the slip test. Choosing the 787 Re-engine instead of fps was worth **+$6.25B** to Boeing; refusing fps on its own (keeping the 787 Re-engine) was worth +$3.08B to Boeing and +$8.61B to Airbus.
  - **Round 2, 787 Re-engine on GE in 2031 instead.** Moving first was worth **+$5.03B** to Boeing and **−$3.15B** to Airbus, which then shelved its A350 Re-engine. It cost Rolls-Royce $2.66B and gave CFM/GE +$2.44B.
  - **Result:** narrowbody share fell to 32% in 2045 and widebody share rose to 68%, for +$1.7B. Both share objectives failed, but they would have failed even with fps (37.45% < 40%).
- **Effect on others.** Boeing's engine requirement named no maker, so rivals read it in opposite ways:
  - In game 1, Rolls-Royce built an UltraFan narrowbody that no aircraft took, and Pratt & Whitney cancelled the GTF2 that Boeing then named.
  - In game 2, Boeing's "GTF2 qualifies today" was contradicted the same round. It corrected this in round 3.
- **Thin seats.** Malave's slip-test veto, one of two failed legs behind the game-2 no-fps call (the nominal leg failed too), rests on one earnings call.

## Airbus: a disciplined, rule-bound incumbent that maximises PV inside red lines

**How the behaviour was built**
- **Sources:** 867 evidence items. Airbus's own voice is one document, the FY2025 Board Report (310 items). There are 183 items of Airbus behaviour seen by Boeing and analysts from 2006 to 2025, and 374 items of Airbus intelligence on Boeing.
- **Executives:** 109 items, with one line in Faury's own words. Toepfer has 7 items and Wagner 2.
- **Audit:** hard rules 2, 3 and 7 are inference. For rule 3, the A330neo analogue "cuts the other way".

**How it behaves**
1. **Own technology clock.** It launches NGSA at the technology-ready gate (2028, in service 2035) and never re-times it around Boeing.
2. **Asks for the partner's best new engine but never waits for it.** It launches in the same sealed round and accepts the fallback, since requesting a rival engine costs nothing.
3. **Derivatives come second and in sequence.** No concurrent developments under the supply crunch.
4. **Widebody Chicken discipline.** It pre-empts only when that pays, and stays out once Boeing has re-engined the 787.
5. **Integrity first.** Delay Tactics at most once, only against an fps in development and only if worth at least $1B; it refused them in game 1 round 3 at +$0.72B. It poaches Boeing engineers only while it has a programme of its own in development.
6. **Signals and resets.** It signals to pull suppliers and customers, then resets openly ("subject to Board approval").
7. **Thin seats ratify, they don't decide.** The thin executive seats only confirmed the company default.

**How that played and what it did**
- **NGSA in 2028, both games: top scorer both times.**
  - Against a 2031 NGSA it was worth +$6.4B (game 1) and +$10.9B (game 2).
  - Airbus would still top the table without it, so first place does not depend on 2028.
- **The NGSA engine.** Airbus asked for UltraFan, Rolls-Royce waited, and NGSA flew CFM's LEAP derivative.
- **Game 1:**
  - **A350 Re-engine in round 2, before Boeing could.** It "settles the widebody Chicken"; Boeing's H3 then ruled out a 787 Re-engine.
  - **Cost to Rolls-Royce.** Against Airbus's own deferral path, the same-round launch was worth +$0.37B to Airbus and cost Rolls-Royce $1.60B (the A350 flew GE).
  - **Delay Tactics refused in round 3.** This cost Airbus $0.74B and its 60/40 objective (59.8%), and spared Boeing **$4.07B**.
- **Game 2:**
  - **A350 signalled for 2037, then shelved after Boeing's 787 Re-engine.** Shelving was itself worth +$0.33B to Airbus and spared Boeing $5.05B.
  - **Rolls-Royce stranded.** Its 2036 UltraFan widebody, committed on that signal, was left with no aircraft (−$1.53B).
- **Poaching:** +$0.32B / +$0.25B to Airbus, −$0.73B / −$0.46B to Boeing.

## Rolls-Royce: cash-first, maturity-first, and structurally late

**How the behaviour was built**
- **Sources:** 1,951 evidence items. 1,335 come from its own earnings calls (2010-2025); the rest are Morgan Stanley model cells, Capital IQ and a 2019 industry engine brief.
- **Executives:** 298 items. Erginbilgic (CEO), McCabe (CFO) and Watson (Civil: 27 items, 26 from one event).
- **Calibration:** two independent calibrations reconciled.

**How it behaves**
1. **"No airframe, no engine."** It launches UltraFan only for an airframe announced in an earlier round. An unannounced selection is valued at probability 0.1.
2. **Time on wing first.** It funds the Trent 1000 upgrade in round 1.
3. **Maturity over timing.** It never compresses entry into service, and launches the widebody engine one year ahead so the aircraft does not wait.
4. **Standard terms in every round.** No discounting.
5. **No overlapping UltraFan developments,** especially under the crunch.
6. **Commit and honour, including stopping.** Its disclosures are few, conditional and binding.

**How that played and what it did**
- **The round-1 rule cost it NGSA in both games.** Launching UltraFan with NGSA would have been worth:
  - to Rolls-Royce: **+$18.2B** (game 1) and **+$21.4B** (game 2);
  - to Airbus: +$7.7B / +$8.9B;
  - to CFM/GE: **−$40.8B / −$45.6B**.
  This single rule is the main reason CFM/GE ended with 100% of narrowbody engines.
- **Game 1, round 2: a bet on Boeing's requirement.** It read Boeing's engine requirement as an announcement and launched UltraFan narrowbody for fps. Boeing named GTF2, and the bet cost $4.44B.
- **Game 1, round 2: the missed widebody launch.** It could have launched the UltraFan widebody and won the A350. On its own, that option was worth +$1.32B.
- **Game 2, round 3: honouring the one-year-ahead promise.** It kept the promise on Airbus's conditional signal, and the engine was stranded (−$1.53B).
- **Result:** last in both games (−$7.0B, then −$3.7B). Both bets were declared and within its premium cap: the game-1 bet was objective-driven, the game-2 one honoured its promise.

## Pratt & Whitney: durability first, then cut what nobody selects

**How the behaviour was built**
- **Sources:** 2,072 evidence items. They include 1,413 RTX/UTC calls, 413 10-Ks, the Goldman Sachs RTX model and GTF reporting.
- **Executives:** 360 items. Calio (110), Mitchill (180) and Eddy (21, from one 2023 event).
- **Calibration:** two calibrations; strain is a placeholder. Every Joint Venture threshold is inference.

**How it behaves**
1. **Fix forward.** It books the GTF durability upgrade first.
2. **Hedged NGSA with a GTF2 for 2030.** Cleared by its objectives file, below the team's bar on its own odds; the profile default was a disclosed offer for 2029.
3. **The CFO cuts an unselected engine at the first chance** (Mitchill's veto). It "reaffirms, then cuts".
4. **No discounts, no widebody engine.** A Joint Venture with Rolls-Royce only after an airframer names UltraFan.
5. **Voice:** dated and disclosure-heavy in Calio's voice ("control what you can control", "time on wing is the name of the game").

**How that played and what it did**
- **The same orders in both games, and the same result: −$2.77B both times.** It met its credibility objective and missed its GTF base objective.
- **The hedge** cost $0.73B in each game. Airbus preferred UltraFan.
- **Its biggest effect: the game-1 round-2 cancel,** made in the same sealed round in which Boeing named GTF2. Keeping the engine would have been worth +$0.22B to P&W and +$1.89B to Boeing, and **−$20.66B to CFM/GE**.
- **Game 2: it broke its round-1 promise** to keep GTF2 "by the end of the next round". It owned the reversal, and it had no effect on others because no airframe had named the engine.
- **The prize it missed: a round-1 UltraFan Joint Venture with Rolls-Royce.** Worth P&W +$13.9B, Rolls-Royce +$13.4B and Airbus +$7.7B, at a cost of $40.8B to CFM/GE. Rolls-Royce's hard rule blocked it, not the disclosures.

## CFM/GE: the incumbent that wins by not moving

**How the behaviour was built**
- **Sources:** 1,300 items from GE earnings calls and investor days (Dec 2015 to Nov 2025). Culp has 474 own-words items.
- **Engine numbers:** from Goldman Sachs and Morgan Stanley CFM/Safran model cells, reconciled across two calibrations.
- **Confidence:** high on guidance, capital and LEAP durability. Medium on engine launches ("no GE leader in the evidence has launched a new CFM product engine"). Low on Safran's side: the Safran gate is "consent with no observed veto".

**How it behaves**
1. **Derivative first.** No new engine without a committed airframe. The LEAP derivative is offered "on the airframer's own schedule".
2. **Durability first, one commitment a turn.** The LEAP upgrade in round 1, the GEnx package in round 2.
3. **Tests its own triggers against PV and its $2B premium cap.** The defensive ducted engine its reaction function calls for fired three times and was rejected each time, because it could not change an airframer's same-round pick.
4. **RISE open fan only with a committed airframe.** It declared the open-fan objective unattainable rather than launch speculatively.
5. **Guides low.** Culp's voice: "Safety, quality, delivery and cost"; "we don't have a birthright on that next order". It never names a rival.

**How that played and what it did**
- **Zero regret in both games: +$18.8B and +$19.0B.**
  - Narrowbody engine share rose from 76% to 100%: NGSA in both games, fps in game 1.
  - GE took the widebody engines in both games: the A350 Re-engine in game 1, the 787 Re-engine in game 2.
- **Rejecting the defensive ducted engine** saved it $18.8B in game 1 round 2, and $34.6B / $25.4B against a round-1 launch. That engine would have given Airbus +$4.1-5.1B and Boeing up to +$3.0B.
- **The engine's fallback rule did most of the work.** Under sealed rounds, every contested airframe defaulted to CFM/GE. If every airframe had got the engine it asked for in game 1, CFM/GE would have lost **$64.6B**.
- **Its forecasting error** came mainly from scenario weights: it never priced Pratt & Whitney's same-round cancel. Guiding low was a small part.

## The market cell (airlines and lessors)

- **Behaviour.** It priced engine certainty and consistent disclosures, with multipliers kept between 0.95 and 1.07.
- **Effect.** It barely moved payoffs: at most about $0.5B, and no decision changed.
  - It priced the same round-1 NGSA facts at x0.97 in game 1 and x1.03 in game 2, citing the fps delay. That alone moved Boeing's Do Nothing value from −$2.30B to −$2.40B.
  - The engine keeps only each programme's last multiplier, and applies it only to the aircraft that is leading.

---

# Part 2. Cross-player synthesis: how the behaviours interacted

**Conventions**
- $B are PV to 2026 at each player's own WACC, so they cannot be added across players.
- "Value of a behaviour" means the as-played result minus the counterfactual the player rejected. Positive means the behaviour helped that player.
- Engine numbers come from `PYTHONPATH=. python3 -m wargame.engine whatif --run <run> --side control` (inputs in Appendix B). Where whatif cannot vary something (market multipliers, injects, the scenario config), I used `wargame.model.evaluate(build_world(cfg, history))` on copies of the recorded history.

## Summary

1. **Every player played its profile.** No player broke a hard rule in either game (all five verified analyses agree). Every departure was declared and stayed inside the player's premium cap.
2. **The outcomes come from how the rules fit together, not from any one player.**
   - The engine makers' "no airframe, no engine" rules met the airframers' "committed engines only" rules in sealed rounds.
   - Within a round the engine resolves supplier orders first (model.py, `build_world` docstring), and an airframe's engine is fixed at launch.
   - Every engine request a rival maker had not committed to fell back to CFM/GE.
   - In game 1, giving every airframe the engine it asked for would have cost CFM/GE **-64.55** and given RR +23.66, Airbus +8.05, Boeing +1.84 and P&W +0.21.
3. **The narrowbody result was set by the order of entry into service.** The model's freeze rule lets the first new airplane in service gain share only until the second one arrives (model.py around line 663). NGSA entered in 2035. The fps followed in 2038 in game 1 and never came in game 2, so Airbus held 59.8% in game 1 against 75% in 2050 in game 2.
4. **The widebody result was set by who moved first in round 2.** That depended on whether Boeing already had an fps in development, because Boeing's H4 rule allows one development at a time.
5. **The fps delay changed no round-1 order.** It changed Boeing's round-2 choice, which reversed the widebody outcome.
   - Applied to Boeing's game-1 plan, the delay would have cost Boeing **-11.06**.
   - The players' changed behaviour won back **+8.86** of that.
6. **The market cell barely mattered** (at most $0.5B), because the engine keeps only the last multiplier and applies it only to the airplane that is leading.

---

## 1. How individual behaviour turned into outcomes

### 1.1 Engine rules that tilt everything toward CFM/GE

- **Fallback chain** (config `suppliers.*.fallback_engine`):
  - Narrowbody: an RR or P&W request falls back to `cfm_ducted`. If CFM has not committed that either, it falls to `cfm_leap_plus`, the LEAP derivative: capture 0.92, margin -1pp.
  - Widebody: everything falls back to `ge_genx_next`. That option needs no supplier programme (no supplier `engine_option` maps to it), so it is always available.
- **Requesting a rival engine costs the airframer nothing.** Three players said so in their own rationales:
  - Airbus, game 1 round 1: UltraFan "shares the same fallback chain, so it weakly dominates".
  - Boeing, game 1 round 2: "it weakly dominates a CFM request".
  - P&W, game 1 round 2: "naming it weakly dominates CFM (same fallback)".
- **Sealed rounds are not the root cause on their own.** The engine honours a supplier commitment made in the same round: if RR launches `uf_nb` in 2028 in round 1, NGSA flies UltraFan (counterfactual below). What failed was the suppliers' own rules: RR waits for an announcement made in an earlier round, and P&W cancels at the first round with no selection.
- **Second-to-market makes the narrowbody contest a timing race.** The follower never gains share at equal technology level, which has three consequences:
  - Boeing's fps variant and ramp choices were private: Joint Venture -2.42 and 7-year ramp -1.85 to Boeing, 0.00 to everyone else.
  - The market's fps multipliers (x0.95, x0.98) had zero effect.
  - Only the timing of entry into service moved rivals.

### 1.2 "No airframe, no engine" on both sides

| Player | Rule as written | Source |
|---|---|---|
| Rolls-Royce | No UltraFan without an airframe announced in an earlier round. An unannounced selection is valued at P 0.1. | Quick card hard rule 1 [R-0994, R-1005]; §9 step 4 |
| P&W | Cancel `gtf_next` in the first round in which no airframe flies it and none has disclosed it will. Mitchill vetoes carrying an unselected engine. One exception: the NGSA hedge. | profile §6; teams.md §4 |
| CFM/GE | No new engine without a committed airframe. A ducted engine is defensive only. | H2, H3; §9 step 8 |
| Boeing | "We will choose among committed engines". In game 2: "A promised engine that has not been committed will not be considered". | wg5-2045 R1 and wg5-2045d R1 disclosures |
| Airbus | Count a supplier commitment only once it is public (§11.3), yet "we expect Rolls-Royce to commit". | G1 R1 rationale; in G2 R1 it put weight 0.60 on "RR on time" |

**Four coordination failures followed.**

**(i) NGSA engine, round 1, both games.**
- Airbus asked for UltraFan. Its own estimate of RR's PV from a 2028 commitment was 22.65.
- RR kept its doctrine's P of 0.1, against an own estimate of about 0.15. Its break-even was 0.25 (G2 R1). In G1 R1 it wrote: "At doctrine P 0.1 for each airframe the expected PV is -2.48".
- NGSA flew the LEAP derivative.
- What holding the rule was worth:
  - RR -18.23 in game 1 and -21.41 in game 2;
  - Airbus -7.74 / -8.86;
  - CFM/GE +40.75 / +45.57.

**(ii) The fps engine, game 1 round 2: both suppliers moved, in opposite directions, and both were wrong.**
- Boeing named GTF2 and priced "a small P&W-cancel risk (-1.9)".
- P&W cancelled. Keeping the engine needed "P ≥ about 0.63" against its estimate of 0.36, even though its own prediction was that Boeing would name GTF2.
- RR launched UltraFan narrowbody Solo for Boeing at P 0.35, reading Boeing's requirement as "an announcement of the programme for this round with the engine left open".
- fps flew the LEAP derivative. Two alternatives:
  - **P&W keeps GTF2:** P&W +0.22, Boeing +1.89, CFM -20.66.
  - **Boeing names UltraFan** (RR's launch kept, no P&W hedge): Boeing +2.52, RR +11.62, CFM -20.66.

**(iii) The A350 Re-engine engine, game 1 round 2.**
- Airbus launched in the same round, asking for UltraFan widebody. It already knew RR's rule ("launches UltraFan only for an airframe announced in the previous round").
- RR's own red lines blocked a launch: "no announcement, and it would overlap with the Solo".
- The A350 flew GE GEnx. Two alternatives:
  - **RR launches `uf_wb` in 2034 instead of `uf_nb`:** RR +5.76, Airbus +0.31, CFM -3.18.
  - **Airbus follows its §11.2 deferral path** (round-3 A350 in 2037, RR `uf_wb` in 2036): RR +1.60, Airbus -0.37, Boeing +0.27, CFM -3.09.

**(iv) The reverse failure, game 2 rounds 2-3.**
- Airbus named a 2037 A350 Re-engine "so that the engine can be committed one year ahead".
- Boeing launched the 787 Re-engine in that same sealed round.
- Airbus shelved the A350 under its rule 3. RR committed `uf_wb` in 2036 anyway, at P 0.6 against a break-even of 0.85.
- Cost to RR: -1.53. Every other player: 0.00.

RR named the problem itself in G1 R3: "The announce-a-round-ahead rule could not answer same-round launches." The referee drew the same lesson: these rules "on both sides hand every contested airframe to the incumbent engine maker".

### 1.3 How each disclosure was read

**Boeing's engine requirement (G1 R1).** Text: "launched program by 2031 ... ready ... by 2038 ... We have not selected an engine maker. This is an engine requirement, not an airplane launch date."
- **RR:** an fps announcement with the engine open (P 0.35). It launched `uf_nb` 2031 to hit exactly 2038. The bet cost RR 4.44 (Do Nothing in R2-R3 gives RR +4.44, others 0.00).
- **P&W:** "Boeing's requirement is not a disclosure on pw_gtf2." It cancelled, which cost P&W 0.22, Boeing 1.89, and gave CFM +20.66.
- **Airbus:** predicted fps 2031 on GTF2 or CFM ducted, which was correct.

**Boeing's re-dated policy (G2 R1), and "GTF2 qualifies today" (G2 R2).**
- **RR:** "a procurement policy, not an fps launch ... a signal (P 0.2 at most)". No narrowbody launch, so zero regret.
- **Airbus:** predicted an fps; prediction accuracy fell to 40% that round.
- **Referee:** "GTF2 qualifies today" was contradicted by P&W's cancellation in the same round. Boeing corrected it in R3.

**P&W's offer and keep promise.** G1 R1: GTF2 "offered ... to Boeing for fps", "reviewed each round". G2 R1: "will keep gtf_next in development for any airframer that names pw_gtf2 by the end of the next round".
- **Boeing, G2 R2:** "an R3 fps may lose its committed engine".
- **CFM, G1 R2:** took the launched GTF2 as its defensive trigger, tested a ducted engine and rejected it.
- **P&W:** cancelled in G2 R2 anyway, which is its own bias 2 ("reaffirm, then cut"), owned publicly. PV effect was zero because no airframer had named GTF2. The referee recorded that P&W "reverses the round-1 disclosure".

**RR's one-year-ahead promise (G1 R1, G2 R1-R2).** Text: launch `uf_wb` "the year before" any announced Re-engine year.
- **Airbus, G2 R2:** used it tactically, "name 2037 publicly so Rolls-Royce commits a year ahead".
- **RR, G2 R3:** honoured it ("when we commit something, we honour it") while noting "Airbus's own PV from the Re-engine is -0.337". Cost: -1.53.

**RR's same-round offer to Boeing (G2 R2).** Text: it would "formally commit ... in that same round" if Boeing launched fps on UltraFan.
- **CFM, G2 R3:** "rival narrowbody engine credibly signalled". It re-tested a defensive ducted engine and rejected it.
- The offer was never tested.

**Airbus's conditional A350 signal (G2 R2).** Text: "2037 ... subject to Board approval and market conditions".
- **RR:** P 0.6, launched `uf_wb` 2036, stranded at -1.53.
- **Boeing, R3:** about 65% on the A350 ("has kept every disclosed date"). This produced its +5.04 expectation miss.
- **Market:** "a reason to wait", then re787 raised to x1.07 after the withdrawal.
- **Referee:** the withdrawal was "consistent with the condition it had stated".

**The mutually conditional Joint Venture offers (P&W and RR).** P&W would join only "in any round for which an airframer names UltraFan"; RR's `jv_pw` needs P&W's join to be announced first.
- **RR, G1 R2:** "No airframer has named it for this round, so `jv_pw` is not open."
- **P&W, G2 R3:** inferred adverse selection ("offers jv_pw only when it doubts the selection").
- The Joint Venture never formed. A round-1 Joint Venture would have been worth P&W +13.88, RR +13.39, Airbus +7.74, CFM -40.75 (G1). It was blocked by RR's hard rule 1, not by the disclosures, because round 1 came before any disclosure.

**CFM's standing offers** ("LEAP derivative ... on the airframer's own schedule").
- Everyone read CFM as passive: Airbus ("CFM to hold back"), Boeing ("CFM's incentive favours the LEAP derivative").
- This did not cause the rival-engine requests. Airbus asked for UltraFan in R1 before any CFM disclosure existed, and requesting a rival engine weakly dominates because of the fallback rule (verifier, accepted).

### 1.4 The widebody "Chicken" game: whoever moves first holds it

**Game 1: Airbus moved first.**
- Boeing had fps in development, so its H4 rule (one development at a time) and the team's no-overlap rule blocked a 787 Re-engine in round 2.
- Airbus launched the A350 Re-engine in 2035 in round 2. Faury said it "settles the widebody Chicken before Boeing moves".
- In round 3 Boeing's H3 rule fired ("A350 Re-engine launched: no re787").
- Following with a 2036 787 Re-engine would have cost Boeing -2.74 and Airbus -3.14, RR -0.90, with CFM +0.61.

**Game 2: Boeing moved first.**
- With no fps, Boeing launched the 787 Re-engine in 2031 in round 2: "Moving first deters it in R3".
- Airbus had deferred, paying a $0.28B premium, because its "§6 pre-emption test fails".
- In round 3: "Boeing does, so rule 3 and row 5 apply: A350 Do Nothing."
- Against the counterfactual in which Airbus does re-engine (no 787 Re-engine, A350 in 2037), the 787 Re-engine was worth Boeing +5.03, Airbus -3.15, RR -2.66, CFM +2.44.

**Both airplanes in the same round would have hurt both airframers.** In game 2 round 2 it gives Boeing -6.29, Airbus -0.41, RR -2.15, CFM +1.78.

**The engine went to GE in both games.** The A350 fell back to GEnx in game 1, and Boeing chose GEnx for the 787 in game 2. Either way GE won the widebody engines and RR's `wb_dominance` objective failed (62/57/52 and 144/123/102 engines a year against 212).

### 1.5 What the fps delay did to behaviour

**Round 1 was identical in both games.** The referee notes "the order digests match".

**From round 2 on, three players changed and two did not.**
- Changed:
  - Boeing: fps became a 787 Re-engine.
  - Airbus: launching the A350 became a 2037 signal, then a shelving.
  - RR: the `uf_nb` bet became Do Nothing, then `uf_wb` on Airbus's signal.
- Unchanged in every round: P&W (hedge, then cancel) and CFM (LEAP upgrade, then GEnx package). Both finished with identical PV in both games.

**Decomposition** (evaluate each order set under each config):

| | Boeing | Airbus | RR | P&W | CFM |
|---|---:|---:|---:|---:|---:|
| G1 as played | +3.87 | +36.53 | -7.05 | -2.77 | +18.75 |
| G1 orders replayed under the delay | -7.19 | +39.36 | -7.05 | -2.77 | +18.84 |
| G2 as played | +1.68 | +44.54 | -3.68 | -2.77 | +18.99 |
| Direct effect of the delay on the G1 plan | **-11.06** | +2.83 | 0 | 0 | +0.09* |
| Effect of the changed behaviour under the delay | **+8.86** | +5.18 | +3.37 | 0 | +0.15 |

\* CFM's +0.09 is not the delay. The two configs differ in `genx_upgrade.installed_base_saving_b_per_year` (0.12 against 0.14). Replaying G2's orders under the on-time config changes only CFM, by -0.09.

What this shows:
- **The delay acted entirely through behaviour.** On G2's own orders it has no direct effect, since there is no fps.
- **The order in which changes are applied matters, because the widebody choices interact.**
  - Boeing's pivot is worth +2.57 to Boeing if Airbus still re-engines, and +7.62 if Airbus shelves.
  - RR's own change is +2.91 regardless of order.
- **Each strategy fitted its own scenario.** Boeing's game-2 orders played in game 1 would have given Boeing -8.48 and Airbus +7.41.

### 1.6 The market cell

**How it behaved** (state.json `market` and `market_narrative`):
- It stayed within 0.95 to 1.07, inside the 0.90-1.10 band its agent file sets as normal.
- Within a game it changed a multiplier only when something new happened.
- It priced engine certainty and consistent disclosures:

| Game | Programme | Multipliers by round | Reasons given in the narrative |
|---|---|---|---|
| 1 | NGSA | 0.97 → 1.0 → 1.02 | R1: launched "without naming a launch customer and without the engine it asked for", buyers waiting "until the engine line-up settles"; R2: "line-up is settled" |
| 1 | fps | 0.95 → 0.98 | R2: "the GTF it named for fps was cancelled the same year"; R3: "disclosure now matches the record" |
| 1 | A350 Re-engine | 0.97 → 1.0 | R2: "Trent XWB fleets want to know the engine is final"; R3: Trent XWB fleets "accept" it |
| 2 | NGSA | 1.03 → 1.03 → 1.05 | R1: "as promised, cash-funded", LEAP-1A commonality, and "fps no earlier than 2041" |
| 2 | 787 Re-engine | 1.04 → 1.07 | After the A350 withdrawal, "buyers no longer have a reason to wait" |

**The same round-1 facts got different prices.** NGSA was x0.97 in game 1 and x1.03 in game 2. The only new public fact was the fps delay, which the cell cited. This is either a reasonable response to that fact or run-to-run variance; one run per scenario cannot tell them apart.

**Effect on payoffs:**
- **Round-1 projection.** The difference is identical under both configs, so it is entirely the market cell (scratch: market.py):

  | NGSA multiplier | Boeing Do Nothing | Airbus |
  |---|---:|---:|
  | x0.97 (game 1) | -2.296 | 41.37 |
  | x1.00 (neutral) | -2.347 | 41.63 |
  | x1.03 (game 2) | -2.397 | 41.87 |

  This is the whole of the round-1 gap between the two scorecards (Boeing T1 -2.30 against -2.40). drivers.md gives the full-range swing for the 0.75-1.25 band as 0.86.
- **Final payoffs.** Only each programme's last multiplier counts, because `build_world` overwrites it.
  - Neutralising every multiplier in game 1: Airbus -0.05, Boeing +0.03.
  - In game 2: Airbus -0.43, Boeing -0.08, RR +0.06, CFM -0.06. NGSA at x1.05 was worth Airbus +0.49; the 787 Re-engine at x1.07 was worth Boeing +0.17.
- **No decision changed.** Boeing's go/no-go test compares fps against Do Nothing, and both sides of that comparison carry the same NGSA multiplier (drivers.md, "Shared by both states").

---

## 2. The behaviour that mattered most for each player, and its measured impact

All values are as played minus the rejected alternative.

| Player | Behaviour (profile basis) | Profile says / agent did | Counterfactual (input in App. B) | Self | Boeing | Airbus | RR | P&W | CFM/GE |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| **Boeing** | fps go/no-go: the business case must clear Do Nothing by more than ε, using Malave's slip test as the baseline (§9 step 6; teams.md §9) | G1: the test passed (+9.93 nominal / +1.88 slip) and it launched fps 2031 Solo 10y + rate. G2: the test failed (-0.73 / -4.71), so no fps and a 787 Re-engine 2031 instead (see departures) | G1: Do Nothing + rate in R2 (B1) | **+7.44** | | -11.31 | 0.00 | 0.00 | -0.79 |
| | | | G2: fps JV GTF2 2031 + rate instead of the 787 Re-engine (B2) | **+6.25** | | +7.79 | -2.66 | 0.00 | +2.94 |
| | | | G2: fps added on top of the 787 Re-engine (isolates the fps refusal) (B3) | +3.08 | | +8.61 | 0.00 | 0.00 | +0.79 |
| **Airbus** | NGSA in 2028 on its own technology clock (hard rules 1, 2, 8; §6 "Earlier: never") | Followed in both games; also PV-best on its own grid | G2: NGSA in 2031 instead (A2) | **+10.94** | -0.48 | | 0.00 | -0.74 | +3.67 |
| | | | G1: NGSA 2031 alone, A350 2038 (rule-consistent version) (A1) | +6.41 | -1.93 | | -18.23† | -0.74 | +34.58† |
| **Rolls-Royce** | No UltraFan without an airframe announced in an earlier round (hard rule 1) | Held in R1 of both games (P 0.1) | G1: `uf_nb` Solo 2028 in R1, then nothing, compared with upgrade then nothing (R1 against R2) | **-18.23** | +0.05 | -7.74 | | 0.00 | +40.75 |
| | | | G2: `uf_nb` Solo 2028 + upgrade in R1 (R3) | **-21.41** | +0.06 | -8.86 | | 0.00 | +45.57 |
| **P&W** | Cancel an unselected GTF2 at the first chance (§6; Mitchill's veto) | Cancelled in R2 of both games. In G2 this broke its R1 keep promise | G1: keep `gtf_next` (P1) | -0.22 | **-1.89** | 0.00 | 0.00 | | **+20.66** |
| | | | G2: keep (P2) | +2.88 | 0.00 | 0.00 | 0.00 | | 0.00 |
| **CFM/GE** | No new engine without an airframe; the defensive ducted engine rejected above the $2B premium cap (H3; §9 step 8) | The ducted reaction row fired in R2 of both games (and G2 R3) and was overridden by §9 step 8 (declared) | G1 R2: aggressive ducted 2031 (C2) | **+18.79** | -3.03 | 0.00 | 0.00 | 0.00 | |
| | | | G1 R1: standard ducted 2028 (C1) | +34.59 | -1.12 | -4.06 | 0.00 | 0.00 | |
| | | | G2 R1: standard ducted 2028 (C3) | +25.41 | +0.15 | -5.11 | 0.00 | 0.00 | |
| **Market cell** | Bounded multipliers 0.95-1.07 | Within band; consistent within each game | All multipliers neutral (scratch: market.py) | n/a | G1 -0.03 / G2 +0.08 | G1 +0.05 / G2 +0.43 | G2 -0.06 | 0 | G2 +0.06 |

† In this version a 2031 NGSA picks up the UltraFan narrowbody RR launched for Boeing in 2031, because whatif holds RR's orders fixed. The RR and CFM swing is an artifact of that.

**Other behaviours with large effects on rivals**

| Behaviour | Self | Boeing | Airbus | RR | P&W | CFM |
|---|---:|---:|---:|---:|---:|---:|
| Boeing's 737 rate step in R2, G1 (vs no rate step) | +0.51 | | -3.77 | 0 | -0.02 | +0.11 |
| Boeing's 737 rate step in R2, G2 (vs no rate step) | -0.24 | | -3.33 | 0 | -0.02 | +0.11 |
| Boeing's H6 rule: rate step deferred from R1 to R2, G1 | -0.43 | | +1.07 | 0 | +0.07 | -0.35 |
| Boeing's 787 Re-engine first, G2 (vs no 787 Re-engine with Airbus's A350 2037) | +5.03 | | -3.15 | -2.66 | 0 | +2.44 |
| Airbus refuses Delay Tactics, G1 R3 | -0.74 | +4.07 | | 0 | 0 | 0 |
| Airbus shelves the A350, G2 R3 (vs launching in 2037) | +0.33 | +5.05 | | -0.16 | 0 | +0.43 |
| Airbus launches the A350 in R2, G1 (vs its own §11.2 deferral path) | +0.37 | -0.27 | | -1.60 | 0 | +3.09 |
| Airbus Poaching, all rounds (verified analysis) | +0.32 G1 / +0.25 G2 | -0.73 / -0.46 | | 0 | 0 | 0 |
| RR's `uf_nb` objective bet, G1 R2 | -4.44 | 0 | 0 | | 0 | 0 |
| RR's `uf_wb` launched on Airbus's signal, G2 R3 | -1.53 | 0 | 0 | | 0 | 0 |
| P&W's R1 GTF2 hedge, both games | -0.73 | 0 | 0 | 0 | | 0 |
| CFM's GEnx package, G1 | +0.45 | 0 | 0 | -0.37 | 0 | |

**Departures from profile that mattered.** No hard rule was broken in either game.

- **Boeing, G2 R2:**
  - It did not follow reaction row 1. The §9 go/no-go test overrode it, which is how the profile resolves that conflict.
  - It launched the 787 Re-engine in 2031. Profile §11.4 and the teams.md decision rule say 2036, and Malave's inferred "no 787 Re-engine in Turns 1-2" says not yet.
  - Its ExCo cited "widebody first" [B-0802], which profile §6 had set aside.
  - Measured value of that choice: +5.03 against the deterrence baseline.
- **Boeing, G1 R2:** chose GTF2 over the profile's default `cfm_ducted` (and over Ortberg's own lever card). Zero effect, because both requests fall back to the LEAP derivative.
- **Airbus, G1 R2:** launched the A350 although `uf_wb` was not public, against §11.2's "defer to round 3". This was declared. It was worth Airbus +0.37 against the deferral path, at a cost of 1.60 to RR.
- **Rolls-Royce, G1 R2:** launched `uf_nb` at P 0.35 with expected PV -0.60, against the team card ("fps never clears") and the §9 step 6 +$2B bar. It declared a $1.41B objective premium; the realised cost was 4.44.
- **Rolls-Royce, G2 R3:** launched `uf_wb` at P 0.6 against a break-even of 0.85, declaring a $0.45B premium; the realised cost was 1.53.
- **P&W, round 1 of both games:** hedged against the profile's §6/§11b default of a disclosed offer only (flip at 0.45).
  - What cleared the hedge was objectives.md (p ≥ 0.10). Its own odds (0.21 and 0.28) were below the team's bar of about 0.3.
  - It chose 2030 against the 2029 timing in objectives.md §9 and profile §11a.
  - Realised cost: 0.73.
- **CFM/GE, R2 of both games and G2 R3:** its defensive ducted reaction row fired but was not executed, under §9 step 8. That saved it 18.79 in game 1.

---

## 3. What drove each outcome: doctrine, engine rules or scenario

| Outcome | Main driver | Evidence |
|---|---|---|
| NGSA first into service (2035) in both games | **Doctrine and PV agreed** | Airbus hard rules 1/2/8; its own grid had 2028 best (+41.48 to +50.47); NGSA in 2031 costs Airbus 6.41-10.94. Airbus would still be top scorer with NGSA 2031 (29.4 in G1, 33.6 in G2), so first place does not depend on 2028. |
| NGSA flies the LEAP derivative (both games) | **Doctrine meeting engine rules** | RR hard rule 1 at P 0.1; Airbus requests UltraFan as a free option; engine fixed at launch with the fallback to CFM. A same-round RR launch would have won it (+21.4 to +22.7 for RR). |
| fps flies the LEAP derivative (game 1) | **Doctrine and engine rules** | P&W's cancel rule and CFO veto; same-round cancels resolve before engine selection; Boeing's committed-engine rule; RR launched for an airframe that did not name it. |
| CFM/GE gets 100% of narrowbody engines; GE takes widebody | **Engine rules (fallback chain)**, given the other players' doctrines | CFM's own PV includes narrowbody engines +16.93. If every airframe got its requested engine, CFM falls 64.55. CFM's own doctrine was to do nothing ("efficient, by doing the least"). |
| Boeing waits in round 1 | **Doctrine (H1)** | Cost about 4.74 in G1 (fps 2028 is the PV-best round-1 move). Cost nothing in G2 (every round-1 fps loses). The scorecard's 3.43 is a stage-game number; its own "best response" would have cost Boeing 0.80. |
| Boeing's 737 rate step deferred to round 2 | **Doctrine (H6), triggered by the crunch** | A round-1 rate step is +0.43 with or without the crunch (crunch.py), so the deferral has no basis in the engine. Its timing was the biggest Boeing-to-Airbus externality (-3.77 and -3.33 for Airbus). |
| No development overlap anywhere | **Doctrine, also PV-best without the crunch** | The crunch's direct payoff effect as played is 0.00 for everyone. Without the crunch, an A350 in 2031 is still -0.49 (crunch: -1.44); CFM stacking both upgrades is still -1.19 (crunch: -1.89). |
| No fps and a 787 Re-engine in game 2 | **Scenario (delay), acting through doctrine** (go/no-go, H4, the §7 Chicken game) | The delay alone costs the G1 plan 11.06; adapting recovers 8.86. drivers.md: no single market assumption rescues a delayed fps. |
| Who wins the widebody | **Scenario, through doctrine** | H4 kept Boeing out while fps was in development (G1); Airbus rule 3 kept Airbus out after the 787 Re-engine (G2). |
| Airbus +8.0 between the games; Boeing objectives 1/2 → 0/2 | **Scenario** | The narrowbody objective was lost either way: with fps launched in G2, Boeing is at 37.45% < 40%. |
| Size of the airframers' gains | **Scenario (injects)** | Fuel spike: Airbus +6.68 / +6.38, Boeing +1.89 / +1.25. Widebody boom rewarded whoever won the widebody: G1 Airbus +0.66, Boeing -0.14; G2 Boeing +0.98, Airbus -0.11. |
| RR last in both games | **Doctrine (hard rule 1, honouring commitments) meeting the engine rules** | Myopic regret 26.15 / 21.84. The rule cost RR about 18-21 (−18.23 / −21.41); the bets cost 4.44 and 1.53. |
| P&W -2.77 in both games | **Doctrine, unchanged by the scenario** | Identical orders in both games; the hedge cost 0.73. |

---

## 4. Caveats

**Thin executive seats drove real decisions.**
- **Boeing:**
  - Malave: Low confidence, 11 items from one call. His buffer-test veto is marked (inference) in teams.md, yet it decided the G2 no-fps call.
  - Pope: Very low confidence, 8 items, so the business-unit seat was played by doctrine.
- **Airbus:**
  - Toepfer: 7 items, none in his own words.
  - Wagner: 2 items.
  - Faury has a single own-words line (AX-0081), and Airbus's whole own-voice evidence is one FY2025 report.
  - Hard rules 2-7 are inference. For rule 3, the audit says the A330neo analogue "cuts the other way".
- **Rolls-Royce:** Watson has 27 items, 26 of them from one event. McCabe has no evidence on launch economics, and she co-signed the G1 R2 bet against her own card.
- **P&W:** Eddy has 21 items from one June 2023 event, and P-1817 shows a different person in that job by Nov 2025. The 2030 timing came from his seat. Every Joint Venture threshold is inference.
- **CFM/GE:** Ali's evidence ends in March 2024. Safran is absent from the sources, and the Safran gate is "consent with no observed veto". Ghai's and Ali's vetoes are inference.

**Placeholder parameters sit on the decisive mechanics.**
- `cfm_leap_plus` capture 0.92 and margin -1pp set how good the fallback engine is.
- Boeing's fps decision depends on placeholders: drivers.md lists fps capex, Joint Venture terms, capture speed, the 80% share cap, the 2060 horizon and volumes. The slip leg rests on placeholder Delay Tactics.
- Strain is a placeholder for RR and P&W. CFM's alpha (0.45) and its open-fan parameters are placeholders.
- The five-player numbers in each profile's §11 come from scratch runs, not evidence.
  - Boeing re-ran its §11 numbers in G2.
  - CFM's objectives.md claim of +8.5 to +13.4 for "defending vs losing" failed in play.
  - RR's citation audit predates §11 and reaction rows 15-20.

**Sample size.**
- One game per scenario and one seed. Round 1 was identical in both games, so effectively one round-1 sample.
- The market priced the same NGSA facts at x0.97 and x1.03, which shows how much LLM agents can vary between runs.

**Method limits.**
- Every counterfactual holds the other players' recorded orders fixed. It does not model their reaction to changed moves or disclosures; for example, Boeing would likely request UltraFan if RR had committed in 2028.
- Scorecard myopic regret uses a stage game with first-year launches on default engines, so it overstates or misstates full-game cost: Boeing's H1, P&W's hedge (3.61 against 0.73 realised) and RR's G1 total (which includes the 4.44 bet).
- PV is at each player's own WACC, so sums across players are not meaningful.
- The configs also differ in GEnx installed-base saving (0.12 against 0.14), so CFM's game-to-game comparison is off by 0.09.
- Volumes are stylised (2,000 narrowbodies and 170 widebodies a year), and objectives never change payoffs.

---

## Appendix A: Disagreements between the per-player analyses and their verifiers, resolved by checking files or re-running

All of these go the verifier's way.

- **Boeing, G2 narrowbody objective:** it was lost even with fps (37.45% < 40%). The go/no-go call cost share, not the objective.
- **Boeing, referee rating:** the referee rated Boeing's doctrine fidelity only; the leadership-fidelity line is about Airbus.
- **Airbus staying out of the A350 in G2 R3:** this gained Airbus +0.33. It was not a sacrifice.
- **Who sent the A350 engine to GE in game 1:** measured against Airbus's §11.2 deferral path, RR lost 1.60, not 3.12. RR's own same-round option (`uf_wb` 2034) was worth +5.76 to it.
- **Value of RR's round-1 rule in game 1:** 18.23, not 22.67. The 4.44 difference is RR's own round-2 bet.
- **Round-1 Joint Venture:** it was blocked by RR's hard rule, not by the mutually conditional disclosures.
- **CFM's forecast error:** it comes mainly from scenario weights (P&W's same-round cancel was never priced), not from its guide-low habit (0.06-0.9).
- **"Every engine maker followed no airframe, no engine":** wrong for P&W, which launched its R1 hedge with no airframe.
- **Boeing's 787 Re-engine:** its value is mostly deterrence. Against the deterrence baseline it was Boeing +5.03 and Airbus -3.15, not Airbus -0.82.

## Appendix B: Inputs

Each line is whatif stdin JSON. Runs: G1 = `wg5-2045`, G2 = `wg5-2045d`; all with `--side control`.

- **B1 (G1):** `{"boeing":{"2":{"launch":[],"cancel":[],"rate_increase":true}}}`
- **B2 (G2):** `{"boeing":{"2":{"launch":[{"program":"fps","year":2031,"engine":"pw_gtf2","variant":"jv","ramp":"10y"}],"cancel":[],"rate_increase":true}}}`
- **B3 (G2):** the same with `{"program":"re787","year":2031,"engine":"ge_genx_next"}` added to the launch list.
- **H1 cost (G1):** `{"boeing":{"1":{"launch":[{"program":"fps","year":2028,"engine":"cfm_ducted","variant":"solo","ramp":"10y"}],"cancel":[],"rate_increase":true},"2":{"launch":[],"cancel":[],"rate_increase":false}}}`
- **Rate step (G1):**
  - no rate step: R2 fps with `"rate_increase":false`;
  - rate step in R3 instead: R2 fps with `"rate_increase":false` and R3 `"rate_increase":true`.
- **Rate step (G2):** R2 re787 with `"rate_increase":false`.
- **A1 (G1):** `{"airbus":{"1":{"launch":[],"cancel":[],"delay_tactics":false,"poaching":false},"2":{"launch":[{"program":"ngsa","year":2031,"engine":"rr_ultrafan_nb"}],"cancel":[],"delay_tactics":false,"poaching":true},"3":{"launch":[{"program":"rea350","year":2038,"engine":"rr_ultrafan_wb"}],"cancel":[],"delay_tactics":false,"poaching":true}},"rolls_royce":{"3":{"launch":[],"cancel":[],"t1000_upgrade":false}}}`
- **A2 (G2):** Airbus R1 no launch and no Poaching; R2 NGSA 2031 `rr_ultrafan_nb` with Poaching.
- **Airbus §11.2 deferral path (G1):** `{"airbus":{"2":{"launch":[],...,"poaching":true},"3":{"launch":[{"program":"rea350","year":2037,"engine":"rr_ultrafan_wb"}],...}},"rolls_royce":{"3":{"launch":[{"program":"uf_wb","year":2036,"terms":"standard"}],"cancel":["uf_nb"],"t1000_upgrade":false}}}`
- **Delay Tactics (G1):** `{"airbus":{"3":{"launch":[],"cancel":[],"delay_tactics":true,"poaching":true}}}`
- **A350 2037 (G2):** `{"airbus":{"3":{"launch":[{"program":"rea350","year":2037,"engine":"rr_ultrafan_wb"}],"cancel":[],"delay_tactics":false,"poaching":false}}}`
- **Both widebody airplanes in one round (G2):** `{"airbus":{"2":{"launch":[{"program":"rea350","year":2035,"engine":"rr_ultrafan_wb"}],"cancel":[],"delay_tactics":false,"poaching":true}}}`
- **787 Re-engine following the A350 (G1):** `{"boeing":{"3":{"launch":[{"program":"re787","year":2036,"engine":"ge_genx_next"}],"cancel":[],"rate_increase":false}}}`
- **Deterrence baseline (G2):** Boeing R2 rate step only, plus Airbus R3 rea350 2037 `rr_ultrafan_wb`.
- **R1 (G1):** `{"rolls_royce":{"1":{"launch":[{"program":"uf_nb","variant":"solo","terms":"standard","year":2028}],"cancel":[],"t1000_upgrade":true},"2":{"launch":[],"cancel":[],"t1000_upgrade":false},"3":{"launch":[],"cancel":[],"t1000_upgrade":false}}}`, compared with `{"rolls_royce":{"2":{...empty...},"3":{...empty...}}}`
- **R2 (G1):** R2 `uf_wb` 2034 standard with R3 empty.
- **Full coordination (G1):** R1 `uf_nb` 2028 + upgrade, R2 `uf_wb` 2034, R3 empty. Adding `"pratt_whitney":{"2":{}}` gives the "every airframe gets its requested engine" run.
- **R3 (G2):** `{"rolls_royce":{"1":{"launch":[{"program":"uf_nb","variant":"solo","terms":"standard","year":2028}],"cancel":[],"t1000_upgrade":true}}}`
- **RR's `uf_wb` (G2):** `{"rolls_royce":{"3":{"launch":[],"cancel":[],"t1000_upgrade":false}}}`
- **P1 / P2:** `{"pratt_whitney":{"2":{}}}`
- **P&W hedge:** `{"pratt_whitney":{"1":{"gtf_upgrade":true},"2":{}}}`
- **Round-1 Joint Venture (G1):** `{"rolls_royce":{"1":{"launch":[{"program":"uf_nb","year":2028,"terms":"standard","variant":"jv_pw"}],"t1000_upgrade":true},"2":{},"3":{}},"pratt_whitney":{"1":{"gtf_upgrade":true,"join_rr_jv":true},"2":{}}}`
- **Boeing names UltraFan (G1):** `{"pratt_whitney":{"1":{"gtf_upgrade":true},"2":{}},"boeing":{"2":{"launch":[{"program":"fps","year":2031,"engine":"rr_ultrafan_nb","variant":"solo","ramp":"10y"}],"cancel":[],"rate_increase":true}},"rolls_royce":{"3":{}}}`
- **C1 / C3:** `{"cfm":{"1":{"launch":[{"program":"ducted","terms":"standard","year":2028}],"cancel":[],"leap_upgrade":true}}}`
- **C2:** `{"cfm":{"2":{"launch":[{"program":"ducted","terms":"aggressive","year":2031}],"cancel":[],"genx_upgrade":true}}}`
- **GEnx package:** `{"cfm":{"2":{"launch":[],"cancel":[],"genx_upgrade":false}}}`
- **Model-level runs (not whatif):** market multipliers set to 1.0 (market.py); injects removed by round (scen.py, crunch.py); each game's orders evaluated under the other game's config, and per-player order swaps (scen.py, swap.py).