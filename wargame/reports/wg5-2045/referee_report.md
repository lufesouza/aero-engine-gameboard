# Referee's efficiency report: run `wg5-2045`

- **Scenario:** `five-player-2045`. Five players: Boeing, Airbus, Rolls-Royce, Pratt & Whitney and CFM/GE. Three rounds: 2026-2030, 2031-2035 and 2036-2045.
- **Injects (umpire's choice):**
  - round 1: supply-chain crunch;
  - round 2: fuel price spike;
  - round 3: widebody demand boom.
- **Leadership teams (all defaults):**
  - `ortberg-malave-pope-2026`
  - `faury-toepfer-wagner-2026`
  - `erginbilgic-mccabe-watson-2026`
  - `calio-mitchill-eddy-2026`
  - `culp-ghai-ali-2026`
- **How it was run:** every player was an independent agent. It read only its own company and executive profiles and its own engine view, under the isolation hook. Only the game master ran `equilibria`, the full game-theory board. Players received the same public situation report each round. Disclosures were relayed verbatim through the brief, with public-record notes.

Supporting files in this folder:
- `rounds.md` / `rounds.json`: round-by-round shares, dates and financials;
- `final_report.md`;
- `scorecard.md`;
- `state.json`: every order, statement, disclosure and private rationale;
- `war_game_2045.html`: summaries and details.

## Final result

| Player | Delta PV $B (full game, PV 2026) | Objectives met |
|---|---:|---|
| Airbus | +36.5 | 1 of 2 (protect A320; 60/40 missed by 0.2pp) |
| CFM/GE | +18.8 | 1 of 2 (narrowbody dominance; open fan missed) |
| Boeing | +3.9 | 1 of 2 (incumbency; 50/50 missed by 9.8pp) |
| Pratt & Whitney | -2.8 | 1 of 2 (credibility; GTF base missed) |
| Rolls-Royce | -7.0 | 0 of 2 |

**Market shares (deliveries) at each round's end:**

| As of | NB Boeing / Airbus | WB Boeing / Airbus | NB engines (RR / P&W / CFM) | WB engines (RR / GE) |
|---|---|---|---|---|
| 2030 | 40.0 / 60.0 | 58.8 / 41.2 | 0 / 24 / 76 | 60 / 40 |
| 2035 | 42.0 / 58.0 | 58.8 / 41.2 | 0 / 0 / 100 | 57 / 43 |
| 2045 | 40.2 / 59.8 | 53.8 / 46.2 | 0 / 0 / 100 | 15 / 85 |

**Programme dates:**

| Programme | Launch | Entry into service / ready | Engine (requested → flown) |
|---|---:|---:|---|
| NGSA | 2028 | 2035 | UltraFan → LEAP derivative |
| fps (Solo, 10-year ramp-up) | 2031 | 2038 | GTF2 → LEAP derivative |
| A350 Re-engine | 2035 | 2040 | UltraFan widebody → GEnx upgrade |
| Next-generation GTF | 2030 | cancelled 2031 | (no airframe) |
| UltraFan narrowbody | 2031 | cancelled 2036 | (no airframe) |
| 737 rate step | 2031 | extra share from 2033 | |

**One-time commitments:**
- 2026: Trent 1000 upgrade, GTF durability upgrade, LEAP durability upgrade;
- 2031: GEnx improvement package.

The engine's scorecard, pasted verbatim, is in `scorecard.md`.

## Efficiency verdicts

**Airbus: the most efficient player.**
- **Value capture and regret.** It captured 94% of available value, with zero myopic regret in rounds 1-2. Its one round-3 regret was $0.7B, from Delay Tactics refused.
- **Hindsight.** Its hindsight regret of -9.7 means it beat every plan in the plan-game benchmark. That benchmark launches in the first year of a round and on default engines, and Airbus did better than any plan built on those assumptions.
- **Doctrine fidelity is high:**
  - NGSA on its own technology clock;
  - no development overlap under the crunch;
  - integrity first, with Delay Tactics never used;
  - the premium declared each round.
- **Leadership fidelity.** Its ExCo script was run every round: Faury frames, Toepfer tests cash, Wagner tests production.
- **Calibration.** Its expected payoffs were off by 6.4 in round 1 and 4.6 in round 2, because it priced Boeing's fps risk conservatively.
- **Disclosures** were consistent with the public record throughout.

**CFM/GE: efficient, by doing the least.**
- **Value capture and regret.** It captured 100% of available value with zero myopic regret.
- **Doctrine.** It followed its doctrine exactly: no new engine without an airframe, durability first, and the Safran gate checked every round. Its defensive ducted engine was tested and correctly rejected; it would have cost at least $5.7B in every state.
- **Calibration.** Its expected payoffs were the most conservative of any player: 9.5 against 16.2 projected in round 1, and 5.0 against 18.4 in round 2. Its doctrine guides low.
- **Open fan.** It was right to call the open fan unattainable once both single-aisles were committed.

**Boeing: disciplined but late.**
- **Value capture and regret.** It captured 86% of available value. Its myopic regret was $3.4B, all of it in round 1, where hard rule H1 ruled out an fps.
- **Calibration.** It was the best calibrated player, with a mean absolute error of 0.41.
- **Prediction.** It was among the most accurate predictors (89%).
- **Doctrine fidelity is high:**
  - the readiness and balance-sheet gates;
  - the rate step only on its KPIs;
  - the 10-year ramp-up chosen on the numbers;
  - no 787 Re-engine.
- **Information use.**
  - Its round-1 engine requirement was strategic but did not name a maker. Two engine makers read it in opposite ways.
  - Its round-2 engine disclosure was contradicted by the public record when Pratt & Whitney cancelled in the same round. Boeing owned that in round 3.

**Pratt & Whitney: sound hedging logic, costly timing.**
- **Value capture and regret.** It captured 92% of available value, with $3.8B of myopic regret, mostly the round-1 GTF2 hedge.
- **The round-2 cancel.** It cancelled the GTF2 in the same sealed round in which Boeing selected it. This was PV-best on its information: keeping the engine needed odds of at least 0.63 that Boeing would name it, against its own estimate of 0.36. Even so, it cost it the fps.
- **Doctrine and objectives.** Its doctrine fidelity is high, with the cancel rule written in advance and no widebody engine. It declared the GTF-base objective unattainable in rounds 2-3 and met the credibility objective.

**Rolls-Royce: least efficient.**
- **Value capture and regret.** It captured 49% of available value, with $26.2B of myopic regret.
  - **Round 1:** $20.2B. Launching UltraFan with Airbus's NGSA would have won it; Rolls-Royce's hard rule required the airframe to be announced in the previous round.
  - **Round 2:** $6.0B. It launched the UltraFan narrowbody for fps, but Boeing named the GTF2. It did not launch the UltraFan widebody, and the A350 Re-engine it would have won went to GE.
- **Doctrine.** Its doctrine fidelity is high (the "no airframe, no engine" red line). It declared a $1.4B objective premium for the 2031 narrowbody launch, inside its cap. It cancelled as it had said it would, and stated the lesson itself: its announce-a-round-ahead rule could not answer launches made in the same round.

## Comparative ranking

1. **Airbus.** Skill and doctrine aligned: the PV-best orders in two of three rounds.
2. **CFM/GE.** Doctrine and position did most of the work: the incumbent's fallback captured everything.
3. **Boeing.** Doctrine cost value (H1 in round 1), but it played the cards it had well afterwards.
4. **Pratt & Whitney.** A good process with unlucky timing, on a misread of Boeing's requirement.
5. **Rolls-Royce.** Its doctrine's red line cost it most of its narrowbody and widebody upside, and it paid as the doctrine predicted.

**Skill and doctrine are separate.** Rolls-Royce's and Boeing's regrets are faithful to their documented doctrines: the premiums were declared or follow from hard rules, so they are not blunders. The structural lesson of the game: sealed, simultaneous moves combined with "no engine without an airframe" rules on both sides hand every contested airframe to the incumbent engine maker.

## Caveats

- Volumes are stylised: 2,000 narrowbodies and 170 widebodies a year.
- Several CFM/GE parameters, and the fps ramp-up multipliers, are placeholders.
- Objectives come from the Boeing Product Development briefing (Boeing proprietary) and never change payoffs.
- This is one game with one seed.
