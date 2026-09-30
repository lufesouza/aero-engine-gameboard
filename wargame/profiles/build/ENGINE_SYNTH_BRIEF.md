# Synthesis brief: an engine maker's behavioural profile

You turn machine-verified evidence into the **behavioural profile** of ONE engine maker for a strategy war game. The company is either:
- **Rolls-Royce Holdings plc**: `rolls_royce`, evidence ids R-####;
- **Pratt & Whitney**, inside RTX (formerly United Technologies): `pratt_whitney`, evidence ids P-####.

An independent agent (`rolls-royce-strategist` or `pratt-whitney-strategist`) will play the company from this profile alone. It reads nothing else about its company, so the profile must let it decide the way the real company has decided:
- **financially**: capital allocation, balance sheet, returns, guidance, pricing;
- **operationally**: engine programmes, durability, the aftermarket, execution;
- **in response to others**: the airframers (Boeing, Airbus) and the rival engine makers (CFM/GE, and the other of RR/PW).

**Isolation.** You work for ONE company. Do not read the other engine maker's profile folder, or `wargame/profiles/boeing*` / `wargame/profiles/airbus*`. What your company knows about others must come from its own evidence file, where rival and customer items are that company's view of them, and from the public game.

## The game

Boeing vs Airbus, 4 turns (2026-28, 2029-31, 2032-34, 2035-37). A deterministic engine scores full-game PV versus the status quo. See `python3 -m wargame.engine rules --side <company>` on a run created with `--suppliers rolls_royce,pratt_whitney`, and `wargame/README.md`.

Every turn all players move simultaneously and in secret:
- **Airframers:** Boeing (a new single-aisle "fps" Solo or as a Joint Venture, a 787 Re-engine, a 737 Rate Increase) and Airbus (NGSA, an A350 Re-engine, Delay Tactics, Poaching). Both can cancel, and both choose an **engine** for each program.
- **Engine-maker players**, with the levers below.

**Rolls-Royce's levers:**
- `uf_wb`: launch the UltraFan widebody engine, selectable for the 787 and A350 Re-engines;
- `uf_nb`: launch the UltraFan narrowbody engine, `solo` or `jv_pw` (a Joint Venture with Pratt & Whitney that halves capex and value; when P&W plays it must join in the same turn), selectable for fps and NGSA;
- `terms`: `standard` or `aggressive`;
- `t1000_upgrade`: a one-time Trent 1000 upgrade (share of 787 deliveries, installed-base cost savings);
- `cancel`; Do Nothing.

**Pratt & Whitney's levers:**
- `gtf_next`: launch a next-generation geared turbofan, selectable for fps and NGSA;
- `pw_wb`: launch a new widebody engine, selectable for the Re-engines;
- `terms`;
- `gtf_upgrade`: a one-time GTF durability upgrade (share of A320neo deliveries, installed-base cost savings);
- `join_rr_jv`: join RR's UltraFan narrowbody Joint Venture;
- `cancel`; Do Nothing.

**Mechanics:**
- An airframer that selects an engine its maker has not committed to falls back to its alternative engine (CFM/GE).
- An airframe waits for a late engine.
- A new airframe program flies one engine (sole source).
- A supplier's payoff is the lifecycle value of the engines it delivers (OE margin plus aftermarket, booked per engine delivered), versus the status quo, minus alpha-loaded capex and strain.

**Status quo:**
- **RR** keeps the A350 (Trent XWB, sole source), the A330neo (Trent 7000) and a Trent 1000 share of the 787. An A350 Re-engine on another maker's engine takes Airbus's widebody franchise away.
- **P&W** keeps its GTF share of A320neo deliveries (the rest are CFM LEAP). An NGSA on another maker's engine takes that away. It has no widebody franchise today.

## Inputs (paths in your task prompt)

- **`evidence.jsonl`**: verified items. **You cite their ids.**
  - Text items carry a verbatim `quote` checked against the source page.
  - Spreadsheet items carry `cells` checked against the workbook.
  - `perspective` tells you whose view each item is:
    - `own_words`: executives on calls;
    - `filing`: 10-K;
    - `own_behaviour`: reported actuals in a model;
    - `analyst_view`: estimates;
    - `market_view`: consensus;
    - `analyst_question`;
    - `press`;
    - `industry_report`;
    - `observed_by_<company>`.
- **The reader summaries and the calibration memo.**
- **The engine's live parameters for your company**, from `rules`. The profile must quote the same numbers.

## Outputs, in `wargame/profiles/<company>/`

### 1. `profile.md`: the doctrine the agent plays by

Target 3,500-6,000 words, dense and specific. Start with a tag legend:
- **[own]**: the company's words or filings;
- **[record]**: reported numbers;
- **[analyst]**;
- **[market]**;
- **[press/industry]**;
- **[customer]**;
- **(inference)**.

Then a **Quick card**:
- ranked objectives;
- hard rules and red lines;
- a default plan per turn;
- top reaction triggers;
- biases to display;
- naming.

Then these sections:

1. **Who we are and what winning means.** Revealed objectives, ranked, with numbers by era, from what the company actually prioritised: margins and cash, returns, balance-sheet repair, investment grade, shareholder returns, installed-base growth, market share, technology leadership. Separate what it said from what it did. For P&W, also cover how RTX (and before 2020 UTC) funds and judges it.
2. **Financial behaviour.**
   - Capital allocation hierarchy.
   - R&D and capex through the cycle (numbers by era).
   - Crisis behaviour: what it cut, what it raised, what it sold, and who paid.
   - Guidance behaviour.
   - The funding capacity for a new engine programme today.
3. **Operational behaviour.**
   - Deliveries and ramp.
   - OE economics per engine (the loss on new engines and how long it lasted).
   - The aftermarket (flying hours, LTSA/PBH pricing, margins, shop visits).
   - Durability record and crises: Trent 1000; GTF early issues and the 2023 powder-metal recall. Give costs and years.
   - **Slip and ramp priors** for its own new engines.
4. **Engine-programme doctrine.**
   - When it launches an engine: a launch customer? sole source vs competition?
   - Technology-readiness gates (UltraFan demonstrator; GTF Advantage).
   - Segments it will and will not enter, and why.
   - Partnerships: IAE/V2500; RR-P&W history; Joint Ventures.
   - Pricing: OE vs aftermarket.
   - What makes it wait.
5. **Reaction function: the core.** A table with one row per trigger:

   | If … | We historically… | Typical lag | Strength | Analogues | Evidence ids |

   Cover at least:
   - an airframer launches a new narrowbody and runs an engine competition;
   - an airframer launches a widebody Re-engine;
   - an airframer selects a rival engine;
   - an airframer asks for price concessions or compensation;
   - a rival engine maker stumbles or wins big;
   - its own durability crisis;
   - demand shocks (COVID);
   - an airframer's quality or rate problems (e.g. 737 MAX grounding);
   - technology slip;
   - supply-chain crunch;
   - a partner proposes a Joint Venture.

   Add how to translate each into war-game orders.
6. **Lever-by-lever playbook.** For each of your company's levers: the default stance, the conditions that flip it in engine terms (e.g. "an airframer launched or disclosed a launch; `options` shows `airframer_incentive_b` > 0 for our engine; `whatif` shows ≥ $X B"), and the precedents, with ids.
7. **How we read the airframers and rivals.** What the evidence shows about Boeing and Airbus as customers, CFM/GE, and the other engine maker. What to expect from each, and how to discount their statements.
8. **Biases and failure modes**, with ids, displayed only when the situation matches. For example:
   - optimism on new-engine durability;
   - buying share with OE concessions and recovering in the aftermarket;
   - guidance habits;
   - balance-sheet caution after a crisis.
9. **Decision procedure for each turn.** A numbered checklist combining the engine's numbers (`options` by scenario, `airframer_incentive_b`, `whatif`) with this doctrine, and saying how to weigh delta PV against revealed priorities. For example:
   - "never launch a narrowbody engine without a committed or disclosed launch customer unless…";
   - "prefer the Joint Venture unless the PV gap exceeds $Y B";
   - "fund the upgrade when…".
10. **Confidence and gaps.** Where the evidence is thin, one-sided or dated.

**Rules:**
- Cite evidence ids inline, e.g. [R-0042] or [P-0042], for every behavioural or numerical claim.
- Numbers come from the evidence or the calibration memo, never from memory.
- Label inferences **(inference)**.
- Forecasts are views, not the record: tag them.
- Use the house naming:
  - "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture", "Delay Tactics" (never "Sabotage");
  - fps, NGSA, A350 Re-engine, 787 Re-engine;
  - UltraFan, Trent XWB, Trent 1000, Trent 7000, GTF, GTF Advantage, V2500, IAE.
- Currency: say £ for Rolls-Royce's reported figures and $ for RTX/P&W. Use the engine's $B only for game numbers.

### 2. `reaction_function.json`

```
[{"trigger": "...", "response": "...", "lag": "...", "strength": "strong|moderate|weak",
  "war_game_translation": "...", "evidence": ["R-0042", ...]}, ...]
```

### 3. `financials.md`

The key financial tables, copied from the evidence with ids. **No new numbers.** Cover:
- P&L by era;
- segments (P&W inside RTX; RR's Civil / Defence / Power Systems);
- OE and aftermarket drivers;
- cash flow and capital allocation;
- guidance vs outcome;
- analysts' estimates.

End with **§ Game calibration**: each of the company's engine parameters, its value, its derivation and evidence ids, marked CALIBRATED or PLACEHOLDER. Take these from the calibration memo and the live `rules`.

## Final reply

At most ten lines:
- word count;
- number of distinct evidence ids cited;
- the three most distinctive behaviours;
- the biggest evidence gap.
