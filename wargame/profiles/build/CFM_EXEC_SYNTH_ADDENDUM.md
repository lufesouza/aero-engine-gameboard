# Addendum to EXEC_SYNTH_BRIEF.md: CFM International's leaders

Use this together with `EXEC_SYNTH_BRIEF.md`. Where the two differ, this file wins.

## What is different for CFM

- **Who the profiles cover.** CFM International is a 50/50 joint venture of GE and Safran Aircraft Engines. Its own officers do not speak in any source; the Capital IQ profile names its CEO, Gaël Méheust. The profiles therefore cover the **GE executives who decide GE's half of CFM and speak for it** on GE calls. For each role, say plainly that Safran holds the other half and that its leaders are not in the sources.
- **Evidence.**
  - `wargame/profiles/cfm/executives/evidence.jsonl`: ids `CX-####`. Items for `exec_id` `cfm_jv` are about CFM International itself: the partnership, its governance, LEAP, RISE, and CFM's officers per Capital IQ.
  - There is **no CFM company profile and no company evidence file.** Each profile states the person's own doctrine directly, rather than "how they differ from the company doctrine". Era context comes from their own words and the `cfm_jv` items.
- **Scope of a pre-2024 GE leader.** They ran a conglomerate. Profile how they decided across GE (capital, portfolio, guidance, crises) and, above all, what they said and did about aviation, CFM and engines. Do not pad a profile with Power, Healthcare or Renewables detail.

## CFM in the game today

CFM/GE is **not a player**. Its engines are options the airframers choose (`python3 -m wargame.engine rules --scenario base --side control`):

| Engine | Segment | Use |
|---|---|---|
| `cfm_ducted` | narrowbody | The default for fps and NGSA |
| `cfm_open_fan` | narrowbody | RISE: +1.5pp margin, +1 year to EIS, 0.85 capture |
| `ge_genx_next` | widebody | GE alone, not CFM; the default for the 787 Re-engine |

The market cell sets CFM/GE's reactions without reading profiles. The referee (game-orchestrator) may use these profiles to judge whether a CFM/GE reaction is plausible. A future `cfm` supplier player would read them.

## § 5 "In the game" for CFM leaders

Write two parts:

1. **As the market cell's CFM/GE today.** How this person would steer CFM/GE when:
   - an airframer launches fps or NGSA and picks or tenders the engine;
   - Rolls-Royce launches an UltraFan narrowbody (Solo or Joint Venture with Pratt & Whitney);
   - Pratt & Whitney launches a next-generation GTF;
   - an airframer asks for concessions;
   - a durability or supply-chain inject hits;
   - a 787 or A350 Re-engine opens a widebody tender.

   Cover price, exclusivity, ramp and capacity, and what they would refuse. Back every claim with evidence.

2. **As a supplier player (proposed levers, not in the engine yet).** These mirror the Rolls-Royce and Pratt & Whitney levers (see `wargame/README.md`, "Engine makers"):
   - launch an RISE open fan or an advanced ducted engine for the next single-aisle (`cfm_open_fan` / `cfm_ducted`);
   - a widebody offer (GEnx-next or a GE9X derivative);
   - terms: standard or aggressive;
   - a one-time LEAP durability upgrade;
   - cancel.

   For each lever: the default stance, the conditions that flip it, the numbers they would ask for (`options`, `whatif`, capex and strain), and Safran's consent. Label the levers **proposed**.

## Output files in `wargame/profiles/cfm/executives/`

**Per-person profiles (Output 1 format):**
- CEO seat: `culp.md`, `flannery.md`, `immelt.md`;
- CFO seat: `ghai.md`, `dybeck_happe.md`, `miller.md`, `bornstein.md`;
- operating seat: `stokes.md`, `ali.md`, `joyce.md`;
- `historical_ops.md`: short cards for John Slattery, Bill Fitzgerald and Kevin McAllister, in the style of the Airbus `historical.md`;
- `cfm_international.md`: the joint venture as the institution these people steer. It covers:
  - the 50/50 structure and what the evidence shows about shared decisions with Safran;
  - LEAP, CFM56 and RISE as joint programmes;
  - CFM's own officers per Capital IQ (names and titles only; no evidence of their conduct);
  - what is not known about Safran's side.

**`teams.md`** (Output 2). Check each member's dates against the evidence, and change the id or the members where the evidence disagrees:
- `immelt-bornstein-joyce-2016`;
- `flannery-miller-joyce-2018`;
- `culp-miller-joyce-2019`;
- `culp-dybeckhappe-slattery-2021`;
- `culp-dybeckhappe-stokes-2023`;
- `culp-ghai-stokes-2024`;
- `culp-ghai-ali-2026` (**DEFAULT**; Ali's title as of November 2025 per Capital IQ).

Every team card includes the **Safran gate**: a CFM programme, pricing or capacity decision needs the partner's agreement. Show how this team handled the partner in the evidence; otherwise label it **(inference)**.

**`README.md`** (Output 3). The executive index table must use exactly these columns:

`| Executive (file) | Role(s) and dates | Own words (ids) | Events | Confidence | Teams |`

The Teams column lists only team-id year suffixes, e.g. `2019, 2021`. Also give the team index table (with a `Team id` column), who uses these files (the referee now, a future CFM player), and the gaps: Safran's leaders; CFM's own officers; no CFM financial model has been used yet.

## Checks

```
cd <repo> && python3 wargame/profiles/build/cite_check.py <file> wargame/profiles/cfm/executives/evidence.jsonl
```

The result must show 0 missing. House naming applies: RISE, LEAP, CFM56, GE9X, GEnx, GTF, UltraFan, fps, NGSA, "Joint Venture", "Re-engine", "Do Nothing".
