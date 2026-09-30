# Synthesis brief: the Rolls-Royce behavioural profile

You turn machine-verified evidence into the **behavioural profile** of Rolls-Royce Holdings plc (RR) for a strategy war game. An independent agent (`rolls-royce-strategist`) will play RR from this profile alone. It reads nothing else about RR, so the profile must let it decide the way the real RR has decided:
- **financially**: capital allocation, balance sheet, returns, guidance;
- **operationally**: engine programmes, durability, aftermarket, execution;
- **in response to others**: the airframers (Boeing, Airbus) and rival engine makers (CFM/GE, Pratt & Whitney).

Read nothing about Boeing's or Airbus's behavioural profiles (`wargame/profiles/boeing*`, `wargame/profiles/airbus*`). RR's view of them must come from the evidence file and the public game.

## The game RR plays

The game is Boeing vs Airbus, 4 turns (2026-28, 2029-31, 2032-34, 2035-37). A deterministic engine scores full-game PV versus the status quo (`python3 -m wargame.engine rules --side rolls_royce` on a run created with `--suppliers rolls_royce`; also `wargame/README.md`). RR is the third player, the engine supplier. Every turn all three players move simultaneously and in secret.

**Airframers' levers:**
- Boeing: a new single-aisle (fps) Solo or as a Joint Venture, a 787 Re-engine, a 737 Rate Increase;
- Airbus: NGSA, an A350 Re-engine, Delay Tactics, Poaching;
- both: cancel a program, and choose an **engine** for each program. The options are CFM, GE, Pratt & Whitney, or RR's UltraFan once RR has committed to it.

**RR's levers:**
1. `uf_wb`: launch the UltraFan widebody engine. It makes `rr_ultrafan_wb` selectable for the 787 Re-engine and the A350 Re-engine.
2. `uf_nb`: launch the UltraFan narrowbody engine, `solo` or `jv_pw` (a Joint Venture with Pratt & Whitney: half the capex and half the value). It makes `rr_ultrafan_nb` selectable for fps and NGSA.
3. `terms`: `standard` or `aggressive`. Aggressive terms give the airframer margin and cut RR's value per engine.
4. `t1000_upgrade` (one-time): more share of 787 deliveries and lower installed-base costs.
5. `cancel` an engine programme no live airframe flies (sunk capex).
6. Do Nothing.

**Mechanics that shape RR's choices:**
- An airframer that selects an RR engine RR has not committed to falls back to its alternative engine.
- An airframe waits for RR's engine if the engine is ready later than the airframe.
- RR's payoff is the lifecycle value of the engines it delivers (OE margin plus aftermarket, booked per engine delivered), versus the status quo, minus alpha-loaded capex and strain.
- The status quo keeps RR's widebody franchise: Trent XWB sole source on the A350, Trent 7000 on the A330neo, and a Trent 1000 share of the 787. An A350 Re-engine on a non-RR engine would take the Airbus widebody franchise away from RR.

## Inputs (paths in your task prompt)

- **`evidence.jsonl`**: verified items with ids `R-####`. **You cite those ids.**
  - Spreadsheet items carry `cells` (workbook, sheet, cell, value) checked against the workbooks.
  - Text items carry a verbatim `quote` checked against its source page.
  - `perspective` is one of:
    - `own_behaviour`: reported actuals;
    - `analyst_view`: Morgan Stanley estimates and scenarios;
    - `market_view`: Capital IQ consensus;
    - `observed_by_boeing` / `observed_by_airbus`: customers' words.
- **Reader summaries and the calibration memo**: context, and the engine parameters derived from the evidence.
- **The engine's live RR parameters**: `rules`. The profile must quote the same numbers.

## Outputs, in `wargame/profiles/rolls_royce/`

### 1. `profile.md`: the doctrine the agent plays by

Target 3,000-5,000 words, dense and specific. Start with a short tag legend:
- **[own]** reported record;
- **[analyst]** Morgan Stanley;
- **[market]** consensus;
- **[customer]** Boeing's or Airbus's words;
- **(inference)**.

Then write the **Quick card** (ranked objectives, hard rules and red lines, default plan per turn, top reaction triggers, biases to display, naming), then these sections:

1. **Who we are and what winning means.** Revealed objectives, ranked, from what RR actually prioritised, with numbers by era:
   - margins and returns;
   - free cash flow;
   - balance-sheet repair;
   - investment-grade status;
   - shareholder returns;
   - market share;
   - technology leadership.

   Separate what it said from what it did.
2. **Financial behaviour.**
   - Capital allocation hierarchy.
   - R&D and capex through the cycle (numbers by era).
   - What RR cut first in the 2020 crisis, when it raised equity, and what it sold.
   - Net debt/cash and liquidity red lines.
   - Guidance behaviour (conservative or aggressive; beats and misses by era).
   - The funding capacity for a new engine programme today (MS estimates and consensus).
3. **Operational behaviour.**
   - Civil large-engine deliveries and thrust; OE economics per engine (the OE loss on new engines); the aftermarket (EFH, LTSA pricing, margins).
   - Durability record (the Trent 1000 crisis: costs and years).
   - **Slip and ramp priors** the agent should assume for its own engine programmes.
4. **Engine-programme doctrine.**
   - When RR launches an engine: with a launch customer only? sole source vs competition?
   - Widebody focus vs narrowbody re-entry.
   - Partnerships (IAE/V2500 history, a JV with PW).
   - Pricing: how it prices OE vs aftermarket.
   - What makes RR wait.
5. **Reaction function: the core.** A table with one row per trigger:

   | If … | We historically… | Typical lag | Strength | Analogues | Evidence ids |

   Cover at least:
   - an airframer launches a new narrowbody and runs an engine competition (fps, NGSA);
   - an airframer launches a widebody Re-engine (787 Re-engine, A350 Re-engine), including the threat of losing A350 exclusivity;
   - an airframer selects a rival engine;
   - an airframer asks for price concessions;
   - a rival engine maker stumbles (a GTF-type durability crisis) or wins big;
   - an RR durability crisis;
   - demand shocks (COVID, fuel);
   - an airframer's quality or rate problems;
   - an engine technology slip;
   - a supply-chain crunch.

   Add how to translate each into war-game orders.
6. **Lever-by-lever playbook.** For `uf_wb`, `uf_nb` (Solo vs `jv_pw`), terms, `t1000_upgrade`, cancel and Do Nothing: the default stance, the conditions that flip it (in engine terms, e.g. "an airframer has launched or disclosed a launch; `options` shows `airframer_incentive_b` > 0 for our engine"), and the precedents, with ids.
7. **How we read the airframers.** What RR's evidence shows about Boeing and Airbus as customers:
   - Boeing's and Airbus's own words about RR;
   - the A350 relationship;
   - the 787 Trent 1000 experience.

   What to expect from each, and how to discount their statements.
8. **Biases and failure modes.** For example:
   - optimism on new-engine durability;
   - under-pricing OE to win platforms, then recovering in the aftermarket;
   - guidance conservatism under current management;
   - balance-sheet caution after 2020.

   The agent shows them **when the situation matches**.
9. **Decision procedure for each turn.** A numbered checklist combining the engine's numbers (`options` by scenario, `airframer_incentive_b`, `whatif`) with this doctrine. It must say how to weigh delta PV against revealed priorities, e.g. "never launch a narrowbody engine without a launch customer unless…", "prefer the Joint Venture unless the PV gap exceeds $Y B".
10. **Confidence and gaps.** The evidence is mainly financial (two workbooks and a segment history) plus customer commentary. There are no RR earnings-call transcripts, so management intent is inferred from numbers. Say where the profile is thin.

**Rules:**
- Cite evidence ids inline, e.g. [R-0042], for every behavioural or numerical claim.
- Numbers come from the evidence or the calibration memo, never from memory.
- Label inferences **(inference)**.
- Forecasts (MS, consensus) are views, not RR's record: tag them.
- Use the house naming: "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture", "Delay Tactics" (never "Sabotage"), fps, NGSA, A350 Re-engine, 787 Re-engine, UltraFan, Trent XWB, Trent 1000, Trent 7000.
- Currency: RR reports in GBP. Say "£" for reported figures, and use the engine's $B only for game numbers.

### 2. `reaction_function.json`

```
[{"trigger": "...", "response": "...", "lag": "...", "strength": "strong|moderate|weak",
  "war_game_translation": "...", "evidence": ["R-0042", ...]}, ...]
```

### 3. `financials.md`

The key financial tables, copied from the evidence with ids. **No new numbers.** Include:
- group P&L by era;
- segments (Civil, Defence, Power Systems) FY2015-FY2025;
- Civil OE and aftermarket drivers;
- cash flow, capital allocation, net debt/cash;
- guidance vs outcome;
- consensus and MS estimates for 2026-2030;
- valuation.

End with **§ Game calibration**: each RR engine parameter, its value, its derivation and its evidence ids, marked CALIBRATED (from the evidence) or PLACEHOLDER.

## Final reply

At most ten lines:
- word count;
- number of evidence ids cited;
- the three most distinctive behaviours;
- the biggest evidence gap.
