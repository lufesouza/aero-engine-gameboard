# Citation audit: CFM International's leaders (GE side)

**Date:** 2026-10-04

## Scope

Two independent audits checked the CFM leadership files in `wargame/profiles/cfm/executives/` against `evidence.jsonl`. They read each cited item's full record (quote, finding, trigger, response, lag and numbers), not only the excerpt that `cite_check.py` prints. Disputed context was checked in the source transcript pages.

- **Audit A, CEO seat and the Joint Venture:** `culp.md`, `flannery.md`, `immelt.md`, `cfm_international.md`.
- **Audit B, CFO seat, operating seat and teams:** `ghai.md`, `dybeck_happe.md`, `miller.md`, `bornstein.md`, `ali.md`, `stokes.md`, `joyce.md`, `historical_ops.md`, `teams.md`.
- **Also edited:** `README.md`, where its referee rule repeated a finding.

**Isolation.** The fixes used only CFM evidence, `wargame/README.md` and the engine's rules and CLI. No Boeing, Airbus, Rolls-Royce or Pratt & Whitney profile was read.

## Counts per audit (before fixes)

| Audit | Load-bearing claims judged | Supported | Weak | Unsupported | Findings (high / medium / low) |
|---|---|---|---|---|---|
| A: CEO seat + `cfm_international` | 284 | 249 | 28 | 7 | 26 (1 / 12 / 13) |
| B: CFO seat, operating seat, teams | about 717 | about 617 | about 88 | about 12 | 35 (3 / 14 / 18) |

Before the fixes, every file passed `cite_check.py` with 0 missing ids. The audits found problems of support, scope and fairness, not missing ids.

**After the fixes**, every file still shows 0 missing:

| File | Citations | Distinct ids | Missing |
|---|---|---|---|
| `culp.md` | 313 | 220 | 0 |
| `flannery.md` | 209 | 115 | 0 |
| `immelt.md` | 206 | 126 | 0 |
| `cfm_international.md` | 156 | 105 | 0 |
| `ghai.md` | 268 | 118 | 0 |
| `dybeck_happe.md` | 252 | 114 | 0 |
| `miller.md` | 251 | 128 | 0 |
| `bornstein.md` | 240 | 115 | 0 |
| `ali.md` | 158 | 42 | 0 |
| `stokes.md` | 239 | 68 | 0 |
| `joyce.md` | 216 | 56 | 0 |
| `historical_ops.md` | 104 | 47 | 0 |
| `teams.md` | 538 | 263 | 0 |
| `README.md` | 68 | 40 | 0 |

**Teams.** No team's membership changed, so every team id and the README index columns stay as they were.

## Main fixes

**Absolute rules contradicted by the evidence.**
- **"GE never speaks for the partner"** (`cfm_international.md`) and **"He never speaks for Safran"** (`culp.md`). Narrowed: GE leaves Safran's own results and its share of supply constraints to Safran [CX-0146] [CX-0157]. It does state joint ramp commitments [CX-0160] [CX-0558], and Culp has named Safran's labour disruption [CX-0220] [CX-0647].
- **Culp, "Never deny-then-reverse".** Replaced. He prefers staged resets and pre-announced charges [CX-0391] [CX-0523]. But he reversed a categorical denial: "no plans to sell GECAS" [CX-0243], then GECAS was combined with AerCap [CX-0434]. He also walked back the 2023 cash commitment [CX-0524].
- **Culp, "No raised target until it has been delivered".** Scoped to the 2021 free-cash-flow margin aspiration [CX-0444]. He does raise once results run ahead: 2019 cash [CX-0317], the 2028 profit target three years early [CX-0597] [CX-0646], and the 2025 LEAP outlook [CX-0654].

**The ramp haircut rule** (`cfm_international.md` rule 3, `teams.md` baseline rule 3, `stokes.md`, `culp.md`, `README.md`).
- The old rule, "haircut by about half", picked +25% for 2023 and dropped Culp's own +38% (1,570 engines) [CX-0590].
- It is restated from the full record: 2023 came in at +38% or +25% against +50% [CX-0590] [CX-0176]; 2024 fell 10% against +20-25% [CX-0954]; the 2025 guide was raised mid-year [CX-0654].
- The new rule, marked (inference): expect a shortfall of a quarter to a half of the promised growth, allow for a 2024-type reversal, and do not haircut a low 2025-style guide.

**Wrong or incomplete outcomes.**
- **LEAP 2017 deliveries:** 473 was Joyce's November 2017 projection. The actual is 459 [CX-1168] [CX-0842]. Fixed in `joyce.md` and `historical_ops.md`.
- **Joyce's "back on PO in 3Q 2018":** now scored as missed. LEAP was about 4 weeks late in July 2018 and January 2019, and back on schedule by May 2019 [CX-1180] [CX-1195] [CX-1215] [CX-0299].
- **Fitzgerald's 1,100 LEAPs for 2018:** met, with 1,118 delivered [CX-1195].
- **The GE9X row in `culp.md`:** now shows GE's own share of the slip, a certification delay with added cost [CX-1237], and the 2021 restatement [CX-1135].
- **LEAP table, `cfm_international.md`:** 1,700 is labelled as the cut target. 2023 now shows both records (+38% and +25%). The 2020 actual is marked as not in the evidence.
- **Andries's commitment:** it was March 2022's 2,000-plus [CX-0149], not "the same" as February 2023's +50% [CX-0160].
- **`historical_ops.md`:** no longer says Safran counterparts never speak. Andries speaks once, naming Slattery [CX-0153].
- **Stokes's 2021 shop-visit row:** scored as a beat, +10% against "roughly flat" [CX-0726].
- **Miller's leverage row:** no slip is shown, because the June 2018 quote has no date and the outcome falls outside the slice [CX-1178] [CX-1186] [CX-1246].
- **Dybeck Happe's reset:** no longer "one large reset". It was a large up-front charge followed by smaller true-ups [CX-0679] [CX-0714].
- **Joyce's breakeven row:** marked as not comparable (contribution margin against OE profitability).
- **Ghai's shop-visit row:** shows the 70% as "continue to expect" by July 2025 [CX-0219], not a July raise.
- **Ghai's R&D:** part of a 2-point margin headwind, not all of it [CX-0918].
- **Win rate, not share:** "70% of the 787" is now a 70% life-of-programme win rate [CX-0615] everywhere.
- **"Halved":** LEAP-1B shipments "halved" is now a plan [CX-0333].
- **Immelt's $10B:** now GE-wide technology spend [CX-1060].
- **Bornstein's 2016 LEAP shortfall:** "about 30%" became about a quarter short (77 against about 100).

**Outcomes only in reader notes.** Outcomes found only in an item's finding or numbers fields, not its quote, are now marked "(per reader notes)". Examples:
- Ghai: 20.7%, $6.1B, the 2025 profit ranges, and GE9X "into the 2030s".
- Miller: $9.7B, +158, 1,736, +130 bp, 20.6%, $0.65, the $4B for GE Capital, $55B and the $6.2B charge.
- Bornstein: $20B, $0.65 and $9.7B.
- Dybeck Happe: price/cost and military.
- Stokes: the CFM56 peak.
- Joyce and teams: the NMA shelved.
- Immelt and teams: the megaproject era.

Where another item quotes the figure, that item is now cited: [CX-0324], [CX-0326], [CX-0360], [CX-1136], [CX-1065], [CX-1086], [CX-0417], [CX-0726], [CX-0989].

**Game use.**
- The invalid `options --side cfm` is replaced in `culp.md` and `ghai.md` with `--side boeing` / `--side airbus` (or `control`). Both files now say the side would exist only with the proposed CFM player. `cfm_international.md` gets the same wording.
- `ge_genx_next` is now named in the widebody guidance of `culp.md`, `bornstein.md`, `stokes.md`, `historical_ops.md`, `teams.md` and `README.md`.
- Every team in the cross-team table now has an engine call: `cfm_ducted` / `cfm_open_fan` / `ge_genx_next`.
- `ali.md` and `stokes.md` gain a labelled "The Safran gate" paragraph. Stokes's paragraph rests on his joint-pricing role [CX-0184] [CX-1289].
- `historical_ops.md` maps Slattery's >20% bar to `cfm_open_fan` for EIS from 2035 (inference).
- `immelt.md` drops the contradictory "cut inventory" default for a ramp inject. It now says: in steady state he cut inventory [CX-1056]; in a ramp he carried it [CX-1037].
- `teams.md` keeps one ramp superlative, backed by numbers: the 2024 team's +20-25% against -10%.

## Fairness changes

- **Miller's March 2019 MAX remark** (`miller.md`, `teams.md`). It was presented as a miss against the $1.4B hit. It now quotes her "It is really too early to comment" preface and its scope, services-contract cash. The $1.4B came through engine receivables [CX-1242]. The teams card no longer says Culp quantified the hit "instead": she gave the $300M and $400M per-quarter figures herself [CX-1235] [CX-1236].
- **Flannery.**
  - The "balanced forward outlook" row now describes a transparency pledge, followed by a reset of the inherited $1.60 framework [CX-0794] as cash fell [CX-0806].
  - His July 2018 "on track" is shown as relaying Joyce's account. The CFO's same-day words included the unit range, which was met [CX-1180] [CX-1195].
  - The CFM56-7B "silence" built from a shareholder's question is replaced by: no statement of his is in the sources [CX-0854].
- **Immelt.**
  - The dividend row notes that his successor halved it and that he had flagged a "fresh look" [CX-1102].
  - The LEAP-launch row adds "meeting all our commercial commitments" [CX-0073].
  - "Resets without naming it" now records that he stated misses plainly [CX-1069] [CX-1086] [CX-1082] [CX-1021].
  - "5-ish" moves out of the track record, because it described margins and was not a commitment.
- **Bornstein.**
  - The launch-year shortfall carries his stated reason, coordination with the airframers [CX-0073].
  - "Categorical denials" is restated neutrally; the evidence does not show the denial was wrong [CX-0113].
  - The spares-metric change carries its stated basis [CX-0090].
- **Ali.** The "small-fix framing" bias no longer sets his words beside Ghai's all-events reserve figure [CX-0905]. It now records that the fixes he named were delivered [CX-0007] [CX-0225] [CX-0996].
- **Joyce.**
  - The 2,200-to-1,400 cut is attributed to the MAX grounding, not called ramp optimism. The same change is made in `teams.md`.
  - "77 delivered" becomes 77 revenue-recognised, plus 8 shipped [CX-0770].
  - The salary-sacrifice line is removed as personal pay detail.
- **Fitzgerald.** "Explained away the 2016 miss" becomes "attributed the 2016 shortfall to revenue recognition".
- **Stokes.** "Spares held back" becomes output that includes spares for fleet stability [CX-1278]. "Pratt & Whitney: game on" now notes that the GTF context came from the analyst.

## Claims relabelled as inference or scoped to their source

- **Healthcare-era rules (Flannery).** These were said as GE Healthcare CEO, 2016-17: stage gates [CX-0787], test then "double down" [CX-0783], price pressure "indefinitely" [CX-0788], outcome guarantees [CX-0786], 6-24 month paybacks [CX-0779] and the single-source target [CX-0785]. They are tagged in `flannery.md` and `teams.md`, and every CFM use of them is marked (inference).
- **GE Power or other non-aviation statements**, now labelled:
  - Miller: "no longer comping on share" [CX-1217], about Power's underwriting; "too optimistic for the market" [CX-1158].
  - Bornstein: the 20% services rule [CX-0014], about Power Generation Services; slot pricing [CX-0024], about the H turbine.
  - Ghai: "profitability is more important than share" [CX-0912].
  - Dybeck Happe: the turnkey cut [CX-0721].
  - Flannery: the H-turbine delivery-date lesson [CX-0830].
  - Immelt: GE-wide equipment margins [CX-1082] and technology spend [CX-1060].
  - Culp: "if it takes a while, it takes a while" [CX-0489], said of GE military engines.
- **Inferences now marked as such:**
  - Immelt's launch-customer and government-funding rule, from the Advanced Turboprop [CX-1016].
  - The "even split" of MAX losses [CX-0136] [CX-0279].
  - Safran's consent to a LEAP durability upgrade [CX-0186] [CX-0210].
  - Applying Ali's ducted-engine physics to UltraFan [CX-0183].
  - Joyce's NMA-only red lines (no geared product; no three-supplier airframe) when applied to fps, NGSA or a GTF response [CX-1127] [CX-1128].
- **Decision rights in `teams.md`.** Every "veto" is now a red line or test, (inference). The evidence shows each member's test, not a formal decision right. Ali's "turn on and turn off" [CX-0009] is dated to his VP of Engineering role in 2024.
- **Other relabels:**
  - The 2,500-LEAP target is shown as Safran's first "per an analyst's question" [CX-0195].
  - Tom Levin "facilitates" the MRO deals; the speaker is uncertain [CX-0170].
  - Flannery's "Safran gate" no longer claims Fitzgerald's February 2017 words [CX-0127] [CX-0128] as Flannery's era.
  - Joyce's and Miller's later or earlier statements used on a team card are dated as such: the payment-terms deal [CX-0142] came after Miller's tenure, and Joyce's NMA tests were stated in March 2018.

## Remaining gaps

- **No new evidence items were added.** This pass wrote only the profile files, so some outcomes stay marked "(per reader notes)". Adding quote-bearing items from the source pages would close them. Examples: Ghai's 20.7% and $6.1B; Miller's $9.7B, 1,736 and 20.6%; the NMA's shelving; and the CFM56 peak moving to 2027-28.
- **Two records conflict.** 2023 LEAP growth appears as +38% [CX-0590] and +25% [CX-0176]. The files show both and do not pick one.
- **Safran's side.** No Safran evidence beyond one investor day [CX-0149] [CX-0152] [CX-0153]. Every Safran gate is GE's account, and consent is assumed.
- **Decision rights inside GE's trio** are not shown for any team, so all vetoes are inferences.
- **The 2025 LEAP full-year outcome** and all outcomes after November 2025 are outside the evidence: the 1B kit, 777X entry into service and the 2028 targets.
- **The engine has no CFM side**, so the proposed CFM levers cannot yet be run. `options` and `whatif` are read through the airframers' sides.
- **Low findings.** All high and medium findings were fixed. The low findings were fixed where cheap, which covered all of them in substance; some minor phrasing outside the cited lines was left as it was.
