# Boeing executives: citation audit

**Date:** 2026-10-03.

## Scope

Two independent audits covered the Boeing executive profiles. The fixes were then applied to all 14 files in this folder:
- **Audit 1, the four CEOs:** `mcnerney.md`, `muilenburg.md`, `calhoun.md` and `ortberg.md`. It covered the Quick card (§2), the commitment track record (§3) and "In the game" (§5).
- **Audit 2, the CFOs, the BCA heads and the teams:** `bell.md`, `smith.md`, `west.md`, `malave.md`, `albaugh.md`, `conner.md`, `deal.md`, `pope.md` and `teams.md`. It covered the same sections, plus every team decision rule and ExCo script.
- **`README.md`** was updated to match the fixes.

Each audit judged every load-bearing claim against the full text of its cited items in `evidence.jsonl` (`BX-`) and `../evidence.jsonl` (`B-`). Both audits re-ran the engine figures in a scratch run outside the repo. The isolation rule held: no Airbus executive or company material was read.

## Counts per audit (before fixes)

| Audit | Files | Claim units | Supported | Weak | Unsupported | Findings: high / medium / low |
|---|---|---|---|---|---|---|
| 1. Boeing CEOs | 4 | 384 | 342 | 38 | 4 | 1 / 8 / 16 |
| 2. CFOs, BCA heads, teams | 9 | ~720 | 668 | 46 | 6 | 0 / 9 / 24 |
| **Total** | 13 | ~1,104 | 1,010 | 84 | 10 | **1 / 17 / 40** |

- **cite_check before the fixes:** 0 missing ids in every file.
- **Engine figures:** both audits reproduced every probe figure they checked, to ±0.01.

## cite_check and length after the fixes

Command, run on each file:

```
cd /home/user/aero-engine-gameboard && python3 wargame/profiles/build/cite_check.py <file> wargame/profiles/boeing/executives/evidence.jsonl wargame/profiles/boeing/evidence.jsonl
```

| File | Citations | Distinct ids | Missing | Words (cap 3,000 for profiles) |
|---|---|---|---|---|
| `mcnerney.md` | 287 | 208 | 0 | 2,995 |
| `muilenburg.md` | 336 | 233 | 0 | 2,994 |
| `calhoun.md` | 266 | 187 | 0 | 2,993 |
| `ortberg.md` | 242 | 141 | 0 | 2,999 |
| `bell.md` | 254 | 132 | 0 | 2,988 |
| `smith.md` | 296 | 216 | 0 | 2,988 |
| `west.md` | 252 | 168 | 0 | 2,991 |
| `malave.md` | 79 | 24 | 0 | 1,378 |
| `albaugh.md` | 229 | 139 | 0 | 2,998 |
| `conner.md` | 237 | 134 | 0 | 2,957 |
| `deal.md` | 101 | 44 | 0 | 1,545 |
| `pope.md` | 33 | 12 | 0 | 739 |
| `teams.md` | 463 | 328 | 0 | 8,360 |
| `README.md` | 64 | 53 | 0 | 1,909 |

Some profiles started within a few words of the 3,000-word cap. To make room for the fixes, duplicate lines were cut. These were mainly repeated voice lines, tempo bullets already covered in §4, and probe tables already given in `teams.md` §1.1. No cut removed a claim that appears nowhere else in the file.

## Main fixes

### High

- **Calhoun's 2030 fps (`calhoun.md` §2 and §5; `teams.md` §6 and §7).**
  - **Problem.** The orders could carry a 2030 launch whenever its premium was $2B or less. That treated a breach of hard rule H2 as a soft premium.
  - **Fix.** The orders now stay at 2029. The preference is logged as "Calhoun 2030 preference: $1.8-2.1B" (re-probed: 2.11 with Airbus idle, 1.80 against NGSA 2026, 2.12 against NGSA 2029). It is voiced in the rationale.
  - **Related change.** `README.md` now names Calhoun's 2030 fps among the team instincts that never reach the orders.

### Medium: game use

- **Gates the engine cannot see.** The 777X and MAX 7/10 certifications and debt appear in no engine output. They were used as gates in `ortberg.md` §5, `west.md` §5, `conner.md` §5, `deal.md` §5, `teams.md` §7 and §9, and the README rationale skeleton.
  - All of these are now labelled not modelled. The programs are assumed certified by Turn 2 (777X 2027 [BX-0550]; MAX 7/10 2026 [BX-1873]) unless a `certification_scrutiny` inject is live.
  - The executable tests are now observable: no live H7 inject, the go/no-go and slip tests, and `components_pv_b.capex`.
  - A "year's wait on a failed gate" is no longer an order, since H2 fixes the year (`ortberg.md`, `teams.md` §8 and §9).
- **H6 applies to every team.** McNerney's "under the [NOW] team, H6 governs" is replaced. H6 binds every team, and his build-through instinct goes into the statement or a logged note.
- **Delay Tactics and Poaching had no order-level translation** in the four CEO files.
  - Each file now gives the orders: on a supplier bottleneck, continue fps (H5), re-baseline once, and launch no overlapping Re-engine; on Poaching, change no orders.
  - Real-world actions are confined to the statement and rationale.
  - The uncited "never blame Airbus" is replaced by the fog-of-war rule: no attribution before exposure.
  - The same structure was applied to the CFO and BCA files.
- **Smith's "Joint Venture under a crisis inject."** The rule appeared in `smith.md` and in three ExCo scripts.
  - It now reads: under a crisis inject, launch only through H7's exception (NGSA in development), and then as a Joint Venture. It is labelled **(inference)**, because BX-1573 concerns seats.
  - In `calhoun-smith-2020`, Calhoun's full stop is stated to override it.
  - Declining an allowed exception is a soft choice under the H8 cap.

### Medium: accuracy

- **Muilenburg, production rate:** "Kept 57+ during the grounding" now reads "kept the long-term 57+ goal while cutting to 42" [BX-1185, BX-1171].
- **McNerney, kill test:** it now says he applied the test to the 747-8 and judged that it passed [BX-0618, B-0192]. He never used it to cancel a launched airplane.
- **Bell, 2009 EPS row:** it now shows each step with its id.
  - Guidance was cut to $5.05-5.35 and then $4.70-5.00 [BX-0120], and then to $1.35-1.55 [BX-0153].
  - The actual was $1.84, after charges of $2.38 and $1.20 a share [B-0227].
  - The auditor's "no item contains $1.84" was checked: the figure is in B-0227's `numbers` field, and the third cut is in BX-0153's. The figure was kept, re-cited.
- **Albaugh, "787 profitable from the beginning":** the row is now judged at program level, as booked, with low-single-digit margins on a 1,100-unit block [BX-0190]. Deferred production is shown as the accounting mechanism: about $25B in 2014 [BX-0477] and $29B in 2016 [BX-1456].
- **West, 737 margins:** the row is now open. Program margins and cash margins are separated [BX-1812, BX-1835], and the 2025-26 outcome is outside the evidence. The tally now reads 5 kept, 13 missed, 1 open.
- **Deal, 800 deliveries around 2026:** the row is open. The "every forecast missed" verdict is limited to the three certification and 777-9 dates. The counter-evidence is stated: regulators set those dates, and his guidance carried a low case [BX-0527].

### Low (all applied)

- **Re-cited.** The outcomes now carry ids that state them:
  - Smith: BX-1008 (787 cash-positive), B-1114 ($835M tanker charge) and B-1093 ($885M 747 charge);
  - Conner: B-1108 and B-1235 (747 reach-forward losses) and BX-1456 ($29B);
  - McNerney: BX-0598 and BX-0669;
  - Calhoun: BX-1842 (equity in the $24B raise);
  - Ortberg: BX-1842 (equity);
  - Muilenburg: B-1135 (deferred balance above $28B, with a new §3 row) and B-0907 (90% reuse).
- **Mis-scoped citations replaced or narrowed.**
  - McNerney: BX-0711 is now customer financing "when very manageable", with BX-0805 for the backstop.
  - Muilenburg: BX-1030 is replaced by BX-1114 and BX-1115 for balance-sheet risk.
  - Calhoun: BX-0413 is dropped from Poaching.
  - Ortberg: BX-1323 now covers the FAA only, and B-2221 covers rate steps only.
  - Albaugh: B-2331 is no longer cited for the "not at any price" phrase.
  - `teams.md`: BX-1341 is dropped from "cash returns sized to proof".
- **Outcomes stated precisely.**
  - McNerney: "mid-2014" for the 787-9.
  - Muilenburg: the BCA margin shown as Q1 8.5%, Q2 10% and Q3 9.9%. The C-17 is "6 of 10 sold by July 2015; shutdown outside the evidence". The KC-46 flight is "later this summer" (July 2015), from BX-0922's annotation; the auditor had marked it outside the evidence. The 2019 margin row notes the grounding three weeks later.
  - Smith: "five successive assumptions (four moves)". The 100% FCF return reads "$12.9B returned in 2018 [BX-1556]; FCF not in the evidence".
  - West: the $500M capex is "planned". The 777X date was "reset twice on his watch, then by his successor". 2023 deliveries read "guidance cut to 375-400; actual outside the evidence".
  - Ortberg: the 787 rate of 8 is "planned (open)".
- **Engine fields that do not exist.** Margins and early penalties now come from `rules`, and margins at EIS from `whatif` `programs[].margin_at_eis`. "Capex by year" and "year-by-year cash path" now read "`undiscounted_b.capex` across launch years, with `capex_b` and `dev_years` from `rules`". The changes are in Smith, Conner, Muilenburg, Malave and `teams.md` §1, §5 and §9.
- **Deal's ExCo questions** are mapped to observables:
  - no `supply_chain_crunch`, `boeing_quality_escape` or `certification_scrutiny` inject in `injects_this_turn`;
  - the Rate Increase in Turn 1 against Turn 2 in whatif (0.32).
- **"Airbus has partnered"** is dropped as a trigger in `muilenburg.md` and `teams.md` §5. The engine cannot observe it.
- **Consistency in `teams.md` §1.1 and the profiles.**
  - Do Nothing is always compared under the same Airbus orders. In `west.md` the slip-test values 0.07, -4.37 and -3.06 replace the nominal -0.08, -4.52 and -3.21; in `albaugh.md`, -4.32 replaces -4.52.
  - The $0.04B margin by which the 2029 Joint Venture passes the slip leg against NGSA 2026 is flagged as fragile in `teams.md`, `west.md`, `ortberg.md` and `malave.md`.
  - The Turn-3 Rate Increase value (6.67) is added.
- **Ortberg's H1 exception.** The $2.1-2.4B rule cost is no longer quoted as the exception's value. The base probe against NGSA 2026 gives a premium for declining the exception of $1.48B nominal and $0.58B in the slip test, against the 2029 Joint Venture. Above $2B in play, the team takes the exception or logs an explicit H8 override (`ortberg.md`; `teams.md` §8 and §9).
- **Paraphrased ExCo questions.**
  - In every profile and in `teams.md`, constructed questions are now in italics, under "(paraphrased questions)".
  - Quotation marks are kept only for verbatim fragments, for example *Are we "putting meaningful market share at risk by waiting"?* [BX-0715].
  - The convention is stated in `teams.md` §1 and the README.
- **`teams.md` conventions** now define [NOW], list what the engine does not model, and fix the Do Nothing basis.

### Where a fix departs from the auditor's suggestion

- **Calhoun's "not … this decade."** The auditor suggested voicing it in `public_statement`. Beside a 2029 launch it would contradict the orders. The statement therefore uses EIS "not before '35" [BX-0376], and "this decade" stays in the rationale.
- **`teams.md` §6, the Re-engine with a 2030 fps** (the auditor suggested 2037, +1.06). With 2030 out of the orders the case no longer arises. The premium is now $1.24B, against the 2029 fps. The re-probe confirmed +0.96 for 2036 and +1.06 for 2037 against a 2030 fps.
- **Bell's $1.84 and the KC-46 flight date.** Both were kept and re-cited from the items' `numbers` and annotation fields, rather than deleted.

## Fairness changes

Wording a fair-minded subject could call a caricature was replaced with neutral, dated statements, and counter-evidence now sits beside the bias it qualifies.

- **Muilenburg.**
  - "Blame suppliers or regulators" now reads "attributes slips to external dependencies (GE's engine, regulator approvals) while holding the end date". The counter-evidence is placed beside it: the FAA requirement accepted [BX-1189] and "We own it" [BX-1167].
  - "Safety first in words" now reads "states safety first" [BX-0915].
  - "Deny, then partner" now reads "hold course in words, then partner" **(inference)**, with his own account [BX-1120].
  - "Perpetual deferral" now reads "repeated deferral of the NMA decision, May 2018 to October 2019".
- **Smith.**
  - "Perpetual new-airplane deferral" now reads "decisions slip while gates are open", with the dated NMA sequence and the MAX-crisis context.
  - "Flatly denied any safety-versus-cost trade-off" now reads that he rejected the suggestion, with his words [BX-1599].
- **Deal.** "Minimising a quality escape" now reads "frames escapes as caught and recoverable; the recovery is not in the evidence". The 2026 forecast is no longer counted as missed.
- **Conner.** "Anchoring on the heart of the market" now reads "holds that the heart of the market is MAX 8-sized", with his A321 concession as counter-evidence [BX-0521].
- **Calhoun.**
  - Both biases ("recasts setbacks", "points to Airbus's troubles") now carry the counter-evidence of plain ownership [BX-0399, BX-0398]. The second is marked as one instance and notes his promise to improve.
  - The $24B raise is placed under the successor team, after the 2024 strike.
- **McNerney.**
  - "Yet he committed the MAX…" is dropped. Albaugh's remark about the board is shown as Albaugh's account [BX-0043].
  - The 2014 tanker row quotes his caveat "it doesn't mean that something can't crop up" [BX-0843].
- **Albaugh.** The 787 row no longer treats deferred production as proof of a failed commitment.
- **Malave.** "Would not endorse the $10B target" now reads "said it was 'a little early' to comment" [B-2337], in `malave.md`, `teams.md`, `calhoun.md` and `west.md`. The "conservative baseline, then a beat" bias is relabelled as an untested inference, since the beat improved West's number.
- **West.** "Walked back within ten weeks" is removed: the cash-margin forecast was not shown to be walked back.
- **Bell.** The 10-15% re-engine R&D estimate is attributed to the analyst; Bell agreed with it [B-0432].

## Claims relabelled as inference

- **McNerney:**
  - NGSA read as "meaningful market share at risk" (the 2011 override was to re-engine);
  - the veto of an EIS before tech_ready_year [BX-0654];
  - keeping a Rate Increase through a demand shock [B-0199, BX-0621];
  - `ge_genx_next` as fitting his 777X choice of GE [BX-0791].
- **Muilenburg:**
  - Embraer as a counter to the C Series deal;
  - "hold course in words, then partner";
  - not accelerating for NGSA;
  - the Joint Venture once NGSA is in development;
  - the veto on following an A350 Re-engine (H3 governs).
- **Calhoun:**
  - Solo by default (no statement on a development Joint Venture);
  - extending "narrow" propulsion gains [B-1900] to a Re-engine.
- **Ortberg:**
  - the 737-7/-10, 777-9 and debt gates (not modelled, assumed closed);
  - vetoing overlap from "doing less and doing it better" [BX-1239].
- **Bell:**
  - "follows the CEO's line, then supplies the numbers";
  - the design-control limit;
  - the Rate Increase veto in a supply-crunch turn [BX-0087].
  - Design control on the 787-9 now rests on the item's finding, not the quote.
- **Smith:**
  - the crisis-inject Joint Venture rule;
  - the veto of `cfm_open_fan` from "No big leaps" [BX-1535].
- **West:**
  - staying with CFM [BX-1710];
  - the gates closing by Turn 2.
- **Malave:**
  - buffer in every baseline (the evidence covers the 777X baseline only);
  - baselines he can beat (untested);
  - Cancel follows doctrine H5;
  - B-2336 attributed to Ortberg.
- **Pope:**
  - the 2012 role read as investor relations;
  - "capacity follows visible demand" (one converted-freighter remark).
- **`teams.md`:**
  - Muilenburg's COO-era slip test (his 2016 CEO-era items are marked as such);
  - "cash and readiness" recast as one selective supplier policy, not a CEO-CFO tension;
  - publishing ranges, now only at launch and as doctrine;
  - Malave's buffer rule.

## Engine re-probes for the fixes (base scenario, scratch run, 2026-10-03)

| Case | Result |
|---|---|
| fps Solo 2029 / 2030 (idle; NGSA 2026; NGSA 2029) | 17.58 / 15.47; 1.95 / 0.15; 6.63 / 4.51 |
| H1 exception against NGSA 2026: 2028 Joint Venture vs 2029 Joint Venture, nominal | 1.82 vs 0.34 |
| Same comparison, slip test | -5.75 (Delay Tactics Turns 1-3) vs -6.33 (Turns 2-3) |
| Do Nothing, nominal / slip (Turns 2-3) / slip (Turns 1-3), NGSA 2026 | -4.52 / -4.37 / -4.32 |
| Do Nothing, nominal / slip, NGSA 2029; Airbus idle | -3.21 / -3.06; -0.08 / 0.07 |
| 787 Re-engine added to a 2030 fps (NGSA 2029): 2036 / 2037 | +0.96 / +1.06 |
| Rate Increase timing (NGSA 2029, fps 2029): Turn 1 / 2 / 3 / never | 6.63 / 6.31 / 6.67 / 5.76 |

## Remaining gaps

- **What the engine does not model.** Certification status and debt are absent from the engine. The gates of the default team (Ortberg, Malave) and of West, Conner and Deal therefore rest on an assumption: closed by Turn 2 unless a `certification_scrutiny` inject is live.
- **Fragile margins.**
  - The default team's choice against NGSA 2026 turns on a $0.04B slip-leg margin. A small change in play can flip it between the Joint Venture and the go/no-go test.
  - The calhoun-smith-2020 "full stop" under a crisis inject was not probed with NGSA already in development. Its cost against H7's exception has to be measured in play against the $2B cap.
- **The H1 cost in `profile.md`.** `profile.md` (outside this scope) still quotes H1's unconditional cost of $2.1-2.4B. The team files now measure the exception's own value, so the two numbers answer different questions.
- **Thin seats.** These are unchanged by the audit:
  - Deal: one event.
  - Malave: one call.
  - Pope: no airplane-business evidence.
  - `muilenburg-smith-2017`: no BCA head.
  Their positions remain mostly **(inference)** or doctrine.
- **Annotations and findings.** Several outcomes rest on the evidence readers' annotations or findings rather than quotes: the C-17 sales, the KC-46 flight date, the 787-9 design control and Bell's EPS steps. They are cited, but they are not the executives' words.
- **Not re-audited.**
  - §4 (sections by dimension) was outside both audits' scope and was not re-audited, apart from lines that duplicated a fixed claim.
  - Two related claims kept their wording: Muilenburg's "never matches Airbus rates" [B-1428, B-1400] and McNerney's "rejected Pratt & Whitney" [B-0600], an exclusive-CFM statement.
- **Lines cut for length.** Duplicate lines removed to respect the 3,000-word cap reduced the distinct-id counts slightly in some profiles (for example McNerney 211 → 208, West 173 → 168). No unique claim was lost.
