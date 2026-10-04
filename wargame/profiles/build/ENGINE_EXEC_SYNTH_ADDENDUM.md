# Addendum to EXEC_SYNTH_BRIEF.md: Rolls-Royce and Pratt & Whitney leaders

Use this together with `EXEC_SYNTH_BRIEF.md`. Where the two differ, this file wins.

## What is different for the engine makers

- **Who reads the profiles.** The `rolls-royce-strategist` and `pratt-whitney-strategist` agents play these companies as supplier players. They read the profiles of the team they are given, run an executive-committee deliberation each turn and decide as that team would.
- **Evidence.**
  - Executive evidence: `wargame/profiles/<company>/executives/evidence.jsonl`. Ids are `RX-####` for Rolls-Royce and `PX-####` for Pratt & Whitney.
  - Company evidence: `wargame/profiles/<company>/evidence.jsonl` (`R-####` / `P-####`).
  - Company profile: `wargame/profiles/<company>/profile.md`, with its calibration and `reaction_function.json`. Individual profiles say how the person **differs from or sharpens** that doctrine, and do not repeat it.
- **Pratt & Whitney sits inside RTX.**
  - The CEO seat (Calio) and the CFO (Mitchill) speak for RTX. Profile how they decide across RTX (capital, guidance, crises), but above all what they said and did about Pratt & Whitney, the GTF and engines.
  - The operating seat is the President of Pratt & Whitney (Leduc to about 2019; Eddy later).
  - Say plainly which decisions sit at RTX level (capital allocation, the balance sheet, the dividend and buybacks) and which at Pratt & Whitney level.
- **Rolls-Royce** is a standalone company.
  - The CEO seat is Erginbilgic from January 2023, the CFO seat McCabe from late 2023 and Kakoullis 2021–2023, and the operating seat the President of Civil Aerospace (Schulz in 2016, Cholerton, then Watson).
  - The evidence is thin before 2021: say so and do not extrapolate.
- **Currency.** Rolls-Royce reports in £ and RTX in $. Quote figures in the source currency.

## § 5 "In the game" for engine-maker leaders

The engine rules are `python3 -m wargame.engine rules --scenario five-player-2045 --suppliers rolls_royce,pratt_whitney,cfm --side control`. The game now has three engine-maker players: Rolls-Royce, Pratt & Whitney and CFM/GE. It plays three rounds (2026–2030, 2031–2035, 2036–2045), and the open fan can enter service only from 2045. Cover each lever:

| Lever | Rolls-Royce | Pratt & Whitney |
|---|---|---|
| New narrowbody engine | `uf_nb` UltraFan narrowbody: Solo, or Joint Venture with Pratt & Whitney (`jv_pw`) | `gtf_next`: next-generation GTF |
| New widebody engine | `uf_wb` UltraFan widebody | `pw_wb`: new Pratt & Whitney widebody engine |
| Terms | standard / aggressive | standard / aggressive |
| One-time upgrade | `t1000_upgrade`: Trent 1000 upgrade (takes 787 share from GE) | `gtf_upgrade`: GTF durability upgrade (takes A320neo share from CFM) |
| Joint Venture | proposes `uf_nb` as `jv_pw` | `join_rr_jv` |
| Cancel | before the engine is ready, if no airframe flies it | same |

For each lever, give:
- the person's default stance;
- the conditions that flip it;
- the numbers they would ask for (`options`, `whatif`, capex, strain and the return hurdle);
- what they veto.

Then cover:
- how they react when CFM/GE launches a ducted engine or the RISE open fan;
- how they react when CFM/GE takes share through its own LEAP or GEnx upgrades;
- how they react when an airframer asks for aggressive terms;
- how they argue in the executive-committee deliberation, and what changes their mind.

## Output files in `wargame/profiles/<company>/executives/`

**Rolls-Royce (`rolls_royce`):**
- `erginbilgic.md`: the CEO seat, the deepest profile (2,500–3,000 words);
- `mccabe.md` and `kakoullis.md`: the CFO seat;
- `operations.md`: the Civil Aerospace presidents. One "## <Full name>: <role and dates>" section each for Chris Cholerton, Robert (Rob) Watson and Eric Schulz, then "## What the seat stands for" and "## Gaps";
- `teams.md`, with these teams (check membership dates against the evidence, and change the id where the evidence disagrees):
  - `east-kakoullis-cholerton-2022`: Warren East (CEO to end-2022) is not profiled. Label him context only and build the card from Kakoullis and Cholerton;
  - `erginbilgic-kakoullis-cholerton-2023`;
  - `erginbilgic-mccabe-watson-2026` (**DEFAULT**).
- `README.md`.

**Pratt & Whitney (`pratt_whitney`):**
- `calio.md`: the CEO seat (2,500–3,000 words). Tag his roles by date: President of Pratt & Whitney, RTX President & COO, then RTX CEO;
- `mitchill.md`: the CFO seat;
- `operations.md`: one section each for Bob Leduc and Shane Eddy, then "## What the seat stands for" and "## Gaps";
- `teams.md`, with these teams:
  - `hayes-mitchill-leduc-2019`: Hayes is not profiled; label him as context only;
  - `calio-mitchill-eddy-2023` (Calio as RTX President & COO);
  - `calio-mitchill-eddy-2026` (**DEFAULT**).
- `README.md`.

**`README.md` index columns** must be exactly:

`| Executive (file) | Role(s) and dates | Own words (ids) | Events | Confidence | Teams |`

The Teams column lists only team-id year suffixes, e.g. `2023, 2026`. Then give the team index (with a `Team id` column), how the strategist uses these files, and the gaps.

## Checks

```
cd <repo> && python3 wargame/profiles/build/cite_check.py <file> wargame/profiles/<company>/executives/evidence.jsonl wargame/profiles/<company>/evidence.jsonl
```

The result must show 0 missing. House naming applies: UltraFan, Trent 1000, Trent XWB, Trent 7000, GTF, GTF Advantage, V2500, LEAP, RISE, fps, NGSA, "Joint Venture", "Re-engine", "Do Nothing".

**Isolation:** Rolls-Royce builders read only `wargame/profiles/rolls_royce*`, and Pratt & Whitney builders only `wargame/profiles/pratt_whitney*`. Neither reads the other's profiles or any airframer's or CFM's profiles. `wargame/README.md` and the engine rules are fine.
