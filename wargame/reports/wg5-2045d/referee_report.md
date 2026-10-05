# Referee's efficiency report: run `wg5-2045d` (fps three years late)

- **Scenario:** `five-player-2045-fps-delay`. It is the five-player game with one public assumption changed: fps entry into service is launch + 10 years instead of 7 (a 2031 launch enters service in 2041), and each of the three extra years costs 10% of fps capex. Every player knew this from round 1.
- **Players and rounds:** Boeing, Airbus, Rolls-Royce, Pratt & Whitney and CFM/GE; three rounds: 2026-2030, 2031-2035 and 2036-2045.
- **Injects (umpire's choice, same as `wg5-2045`):**
  - round 1: supply-chain crunch;
  - round 2: fuel price spike;
  - round 3: widebody demand boom.
- **Leadership teams (all defaults, same as `wg5-2045`):**
  - `ortberg-malave-pope-2026`
  - `faury-toepfer-wagner-2026`
  - `erginbilgic-mccabe-watson-2026`
  - `calio-mitchill-eddy-2026`
  - `culp-ghai-ali-2026`
- **How it was run:** as in `wg5-2045`. Every player was an independent agent, limited by the isolation hook to its own company and executive profiles and its own engine view. Only the game master ran `equilibria`. Each round, every player received the same public situation report, which restated the delay assumption. Disclosures were relayed verbatim through the brief, with public-record notes.

Supporting files in this folder:
- `rounds.md` / `rounds.json`: round-by-round shares, dates and financials;
- `final_report.md`;
- `scorecard.md`;
- `state.json`: every order, statement, disclosure and private rationale;
- `war_game_2045_fps_late.html`: summaries, details and a side-by-side with `wg5-2045`;
- `timeline.html`.

## Final result

| Player | Delta PV $B (full game, PV 2026) | First game (`wg5-2045`) | Objectives met |
|---|---:|---:|---|
| Airbus | +44.5 | +36.5 | 2 of 2 (60/40 edge; A320 protected) |
| CFM/GE | +19.0 | +18.8 | 1 of 2 (narrowbody dominance; open fan missed) |
| Boeing | +1.7 | +3.9 | 0 of 2 (50/50 and incumbency both missed) |
| Pratt & Whitney | -2.8 | -2.8 | 1 of 2 (credibility; GTF base missed) |
| Rolls-Royce | -3.7 | -7.0 | 0 of 2 |

**Market shares (deliveries) at each round's end:**

| As of | NB Boeing / Airbus | WB Boeing / Airbus | NB engines (RR / P&W / CFM) | WB engines (RR / GE) |
|---|---|---|---|---|
| 2030 | 40.0 / 60.0 | 58.8 / 41.2 | 0 / 24 / 76 | 60 / 40 |
| 2035 | 42.0 / 58.0 | 58.8 / 41.2 | 0 / 0 / 100 | 57 / 43 |
| 2045 | 32.3 / 67.7 | 68.4 / 31.6 | 0 / 0 / 100 | 32 / 68 |
| 2050 (projection) | 25.0 / 75.0 | 73.8 / 26.2 | 0 / 0 / 100 | 26 / 74 |

**Programme dates:**

| Programme | Launch | Entry into service / ready | Engine (requested → flown) |
|---|---:|---:|---|
| NGSA | 2028 | 2035 | UltraFan → LEAP derivative |
| 787 Re-engine | 2031 | 2036 | GEnx upgrade |
| fps | not launched | (would be launch + 10) | |
| A350 Re-engine | not launched (signalled for 2037, then shelved) | | |
| Next-generation GTF | 2030 | cancelled 2031 | (no airframe) |
| UltraFan widebody | 2036 | ready 2042 | (no airframe) |
| 737 rate step | 2031 | extra share from 2033 | |

**One-time commitments:**
- 2026: Trent 1000 upgrade, GTF durability upgrade, LEAP durability upgrade;
- 2031: GEnx improvement package.

The engine's scorecard, pasted verbatim, is in `scorecard.md`.

## What the delay changed

- **Round 1 was identical.** All five players gave the same orders as in `wg5-2045` (the order digests match). Boeing's round-1 regret fell from $3.4B to zero: under the delay an early fps was no longer the best response.
- **Round 2 is where the games split.** In `wg5-2045`, Boeing launched fps 2031 (in service 2038), and with the rate step its projection rose from -$2.3B to +$4.3B. Here, Boeing's best fps (Joint Venture, GTF2, 10-year ramp-up, with the rate step) was -$3.1B, against -$2.4B for Do Nothing and +$1.3B for the 787 Re-engine. Boeing's go/no-go test failed on both legs, and its ExCo launched the 787 Re-engine instead.
- **Round 3 confirmed it.** Any fps would enter service in 2046 or later, and the best one was still $1.4-2.5B below Do Nothing. With the 787 Re-engine in service, Airbus's A350 Re-engine was negative on standard terms or the GEnx fallback, and its Board shelved it.
- **Net effect:**
  - Boeing trades narrowbody share (32% in 2045, falling to 20% by 2060) for widebody share (68% in 2045).
  - It saves about $23B of fps capex to 2045, so its delta PV falls by only $2.2B.
  - Airbus gains $8.0B.

## Efficiency verdicts

**Airbus: the most efficient player again.**
- **Value capture and regret.** It captured 100% of available value in every round, with zero myopic regret. Its hindsight regret of -$11.0B means it beat every plan in the plan-game benchmark.
- **Doctrine fidelity is high:**
  - NGSA launched on its own clock;
  - no development overlap under the crunch;
  - the A350 Re-engine tested each round against the "no Chicken crash" rule;
  - no Delay Tactics.
- **Information use.** Its round-2 disclosure of a 2037 A350 Re-engine on UltraFan was labelled "subject to Board approval and market conditions". In round 3 it withdrew it openly, citing a Board review. That withdrawal is consistent with the condition it had stated. Rolls-Royce nevertheless committed the engine in the same sealed round on the strength of the signal.
- **Calibration.** Its expected payoffs were off by 1.7 on average, mainly because it priced a Boeing fps that never came.

**CFM/GE: efficient, by doing the least.**
- **Value capture and regret.** It captured 100% of available value with zero myopic regret.
- **Doctrine.** Its doctrine held: no engine without an airframe, durability first, and the Safran gate checked every round.
- **The defensive ducted engine.** Its doctrine's trigger for a defensive ducted engine (a rival engine launched while fps is open) fired in round 2. CFM/GE re-ran it under the delay and found the defence lost value even when it won. It correctly declined.
- **Calibration.** Its doctrine guides low, so it remains the most conservative forecaster (mean error 4.6).

**Boeing: disciplined, and it pivoted.**
- **Value capture and regret.** It captured 99% of available value. Its only myopic regret was $0.24B, the cost of taking the deferred rate step in round 2 for its objective.
- **Doctrine fidelity is high:**
  - the go/no-go test, nominal and slip legs, run every round;
  - "derivatives first";
  - one development at a time;
  - the rate step only on its KPIs.
- **Strategic effect.** Moving first on the 787 Re-engine deterred the A350 Re-engine, which is the Chicken-game logic in its doctrine.
- **Information use.** Its round-2 disclosure that Pratt & Whitney's GTF2 "qualifies today" was contradicted by Pratt & Whitney's same-round cancellation. Boeing corrected it publicly in round 3.
- **Objectives.** Both share objectives were unattainable once fps lost its business case. Paying for them would have cost $2.1-6.1B, above its $2B cap.

**Pratt & Whitney: same play, same result.**
- **Value capture and regret.** It captured 93% of available value, with $3.6B of myopic regret from the round-1 GTF2 hedge.
- **The round-2 cancel.** It was PV-best in every state, but it broke its round-1 promise to keep the engine "for any airframer that names pw_gtf2 by the end of the next round". The CEO owned this publicly; in this game no airframer had named it.
- **Objectives.** It met its credibility objective with the 2026 durability upgrade. The GTF-base objective was unreachable once NGSA flew the LEAP derivative.

**Rolls-Royce: least efficient, but better than in the first game.**
- **Value capture and regret.** It captured 66% of available value, with $21.8B of myopic regret.
  - **Round 1:** $20.3B. As before, launching UltraFan with Airbus's NGSA would have won it, and its rule required an announcement in the previous round.
  - **Round 3:** $1.5B. It committed the UltraFan widebody one year ahead of Airbus's stated A350 Re-engine, and Airbus shelved the programme in the same round. The engine cannot be cancelled in the final round.
- **Doctrine.** Its doctrine fidelity is high. It honoured a disclosed commitment and declared a $0.45B doctrine premium. It read a conditional signal as an announcement, accepting P = 0.6 against a break-even of 0.85.
- **Why the result improved.** It did not launch a narrowbody engine this time ("signals never justify a launch"), and there was no A350 Re-engine to take its sole-source position. Its result improved from -$7.0B to -$3.7B.

## Comparative ranking

1. **Airbus.** It made the PV-best orders in every round, and the delay removed its only narrowbody competitor.
2. **CFM/GE.** The incumbent's fallback chain again captured every airframe.
3. **Boeing.** It recognised early that fps no longer paid and moved its capital to the widebody, where it won. The narrowbody loss is structural, not a misplay.
4. **Pratt & Whitney.** A good process, an unlucky hedge, and the same outcome as in the first game.
5. **Rolls-Royce.** Its doctrine cost it NGSA again, and its promise to "never make the aircraft wait" made it commit to a programme that was then withdrawn.

**Structural lessons across the two games:**
- **The fps delay decides the shape of the contest.** With a 7-year fps, Boeing fights for the narrowbody and Airbus re-engines the A350. With a 10-year fps, Boeing gives up the narrowbody fight, re-engines the 787, and Airbus shelves the A350 Re-engine.
- **Sealed, simultaneous moves keep producing engine coordination failures, in both directions:**
  - the airframer asks for an engine whose maker waits;
  - the engine maker commits to an airframe that is withdrawn.
- **CFM/GE gains from both.** In both games the incumbent's fallback captures every contested airframe.

## Caveats

- The delay is a public, known assumption from round 1, not a surprise inject. A surprise slip after launch would play differently: fps capex would already be sunk.
- Volumes are stylised: 2,000 narrowbodies and 170 widebodies a year.
- Several CFM/GE parameters, and the fps ramp-up multipliers, are placeholders.
- Objectives come from the Boeing Product Development briefing (Boeing proprietary) and never change payoffs.
- This is one game with one seed, compared with one first game.
