# Synthesis brief: build one company's behavioural profile

You turn machine-verified evidence into the **behavioural profile** of ONE company for a Boeing vs Airbus strategy war game. An independent agent will play the company from this profile alone. It will read nothing else about its own company, so the profile must let it decide the way the real company has decided:
- financially;
- operationally;
- in response to the rival's moves.

You work for ONE side only. Do not read the other company's profile folder, if one exists.

## The war game you are profiling for

Four turns (2026-28, 2029-31, 2032-34, 2035-37). Each turn both sides move simultaneously and in secret; a deterministic engine scores full-game PV versus the status quo.

Boeing's levers:
- launch the new single-aisle "fps", Solo or as a Joint Venture with Embraer;
- 787 Re-engine;
- 737 Rate Increase;
- cancel a program;
- engine choice.

Airbus's levers:
- launch the NGSA new single-aisle;
- A350 Re-engine;
- Delay Tactics (a covert supplier bottleneck that slips the rival's program);
- Poaching (hiring the rival's engineering talent);
- cancel a program;
- engine choice.

The rules are in `wargame/README.md` and `python3 -m wargame.engine rules`.

## Inputs (paths are given in your task prompt)

- `evidence.jsonl`: verified evidence items. Every quote has been machine-checked against its source page. Each item has an `id`, and **you cite those ids**.
- Slice summaries: narrative context per period.
- Financial tables: numbers extracted by script, to be copied, not retyped from memory.

## Outputs, in your company's folder

### 1. `profile.md`: the doctrine the agent plays by

Target 2,500-4,500 words, dense and specific. Sections:

1. **Who we are and what winning means.** Revealed objectives, ranked, from what the company actually prioritised (FCF, market share, margin, dividends and buybacks, balance-sheet repair, rate, safety or quality). Separate what they said from what they did.
2. **Financial behaviour.** Capital allocation hierarchy; appetite for R&D and capex through the cycle (numbers by era); balance-sheet red lines and how they have moved; pricing discipline vs share defence; how charges and reach-forward losses were handled; the funding capacity for a new program today.
3. **Operational behaviour.** Rate philosophy (how fast they ramp, how they treat rate breaks); execution record (schedule slips vs plan, per program, with years); supply-chain posture; quality and regulatory constraints today. Include **realistic slip and ramp priors** the agent should assume for its own programs.
4. **Product-strategy doctrine.**
   - clean-sheet vs derivative;
   - stated technology or economic thresholds for a new airplane;
   - timing logic;
   - partnerships and Joint Ventures;
   - engine choices;
   - what makes them wait.
5. **Reaction function: the core of the profile.** A table with one row per trigger:

   | If the rival… | We historically… | Typical lag | Strength (strong/moderate/weak) | Analogues | Evidence ids |

   Cover at least these triggers:
   - the rival launches a new narrowbody;
   - the rival re-engines a narrowbody or widebody;
   - the rival stretches or adds a variant;
   - the rival raises production rates;
   - rival price aggression and order-campaign losses;
   - the rival acquires or partners (for example CSeries);
   - the rival stumbles (crisis, grounding, quality);
   - demand shocks and downturns;
   - supply-chain or engine problems;
   - regulatory or trade action.

   Then add a column-style note: **how to translate each into war-game orders.**
6. **Lever-by-lever playbook.** For each war-game lever: the default stance, the conditions that would flip it, and the historical precedent, with ids.
7. **How we read the rival.** What this company has believed about its competitor's behaviour, with evidence. What it expects the rival to do and how it discounts rival statements.
8. **Biases and failure modes.** Documented tendencies, such as optimistic schedules, under-investing, over-returning cash, or share-at-any-price. They make the agent realistic. The agent should exhibit them **when the situation matches**, not blindly.
9. **Decision procedure for each turn.** A numbered checklist the agent follows, combining the engine numbers from its finance team with this doctrine. It must say how to weigh the engine's delta PV against the company's revealed priorities, for example "never choose an option that…", "prefer X unless the PV gap exceeds $Y B".
10. **Confidence and gaps.** Where the evidence is thin or one-sided, for example Airbus behaviour seen only through Boeing's commentary.

Rules:
- Cite evidence ids inline, like [B-0042] or [A-0017], for every behavioural claim.
- Numbers must come from the evidence or the financial tables.
- If you infer something beyond the evidence, label it **(inference)**.
- Use the house naming: "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture", "Delay Tactics" (never "Sabotage"), fps, NGSA.

### 2. `reaction_function.json`: machine-readable reaction rows

```
[{"trigger": "...", "response": "...", "lag": "...", "strength": "strong|moderate|weak",
  "war_game_translation": "...", "evidence": ["B-0042", ...]}, ...]
```

### 3. `financials.md`

The key financial tables relevant to decisions, copied from the provided financial files and cited. No new numbers.

## Final reply

At most ten lines: word count, number of evidence ids cited, the three most distinctive behaviours, and the biggest evidence gap.
