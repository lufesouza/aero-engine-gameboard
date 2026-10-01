# Pratt & Whitney: citation audit

**Audit date:** 2026-10-01.

**Scope.** Pratt & Whitney only. Files audited and fixed:
- `wargame/profiles/pratt_whitney/profile.md`
- `wargame/profiles/pratt_whitney/reaction_function.json`
- `wargame/profiles/pratt_whitney/financials.md`

**Checked against:**
- `evidence.jsonl` (2,072 items, ids P-####);
- the synthesis brief (`wargame/profiles/build/ENGINE_SYNTH_BRIEF.md`);
- the reader summaries and the calibration memo;
- the live engine for run `calib` (`rules`, `options`, `whatif` and `validate` with `--side pratt_whitney`).

No other company's profile folder or role card was read. What P&W knows of Rolls-Royce, Boeing and Airbus comes from its own evidence file and the public engine output.

**Method.** Three independent audits, then one integration pass:
- **Citations:** does each cited id support the claim, from the right perspective?
- **Numbers:** does each figure match its cited cells or quote, with the right period, unit and basis, and does each game number match the live engine?
- **Playability:** a full turn 1 played from the profile alone, with the engine.

Every high and medium finding was fixed, and so was every low finding. Engine figures quoted in the fixes were re-run in `whatif`, `options` and `validate` on run `calib`, turn 1.

## Counts before fixes

| Area | Claims judged | Claim-evidence pairs | Supported | Weak | Unsupported |
|---|---|---|---|---|---|
| Citations: profile Quick card, §5 (with 5a), §6 and §9, plus all 14 JSON rows | 77 | 256 (152 in 36 profile units, 104 in JSON rows) | 55 | 20 | 2 |
| Numbers: every figure in profile.md and financials.md, plus engine parameters and payoffs | about 350 | 875 (432 in 87 profile units, 443 in 138 financials units) | 311 | 37 | 2 |
| Playability: turn-1 decision rules and engine reference points, played on run calib | 30 | n/a (tested against the engine, not evidence ids) | 21 | 6 | 3 |

How the pairs were counted: `cite_check.py` split each file into units (paragraphs, table rows and list items). A pair is one cited id within one unit. The numbers count includes only units that hold a figure other than an id.

**Before fixes:**
- profile.md: 466 citations, 284 distinct ids.
- reaction_function.json: 104 citations, 97 distinct ids.
- financials.md: 451 citations, 272 distinct ids.
- 0 missing ids in each file.

**After fixes:**
- profile.md: 483 citations, 282 distinct ids.
- reaction_function.json: 118 citations, 107 distinct ids.
- financials.md: 457 citations, 272 distinct ids.
- 0 missing ids in each file.
- `reaction_function.json` parses as valid JSON: 14 rows, each with the six required keys.

## Main fixes

**High severity.**
- **The IAE red line** (Quick card; §9) was "never back two new engines for one airframer: IAE broke up over exactly that". It misread RR's account [P-1875] and presented a rival's view as P&W doctrine. P&W itself ran the V2500 and the GTF side by side. Fix:
  - The line is now an inference, written as a game constraint: no `gtf_next` and `join_rr_jv` aimed at the same airframer unless `whatif` favours the pair.
  - P-1875 is cited only as RR's view.
  - The line is removed from the §9 red-line list.
- **The turn-1 hedge contradicted the hard rule** "no new engine without a committed airframe", and gave the player no way to estimate the odds. Fixes:
  - Hard rule 1 now carries the franchise-defence exception [P-1868][P-1347].
  - "Committed" is defined in game terms as disclosed for this turn.
  - The hedge is allowed for NGSA only.
  - §6 gives an odds method from the engine: P(launch this turn) from the airframers' `whatif` timing payoffs, times P(names `pw_gtf2`). Naming `pw_gtf2` costs the airframer nothing, and the method weighs our engine against UltraFan.
  - It sets turn-1 defaults: about 0.2 with RR in play, so no launch; about 0.5 without RR.
- **The 1-in-6 break-even** ignored the default upgrade, and the stated numbers did not reproduce it. It is now restated per airframer as cost / (cost + gain), on whatif cases:
  - NGSA with the 2026 upgrade: 1.20 / 4.92 ≈ 0.24.
  - NGSA without the overlap, as from turn 2: 0.86 / (0.86 + 0.96 + 3.11) ≈ 0.17.
  - fps with the upgrade: about 0.38.
- **§9 step 10** (now step 8) conflicted with the §6 Joint Venture premium and had no scenario weighting. It now:
  - scores orders by expected PV under the player's own `prediction` probabilities;
  - lists every red line, held absolutely and with the cost declared;
  - applies a $1B doctrine allowance only to doctrine preferences, and the §6 thresholds already include it (hedge about 0.45; Joint Venture about 0.23);
  - defines the doctrine premium and `expected_delta_pv_b` on the same probabilities.

**Medium severity.**
- **Reaction row 8.**
  - Rate-63 capacity is now cited to P-0091 and P-0092.
  - The 2020 buyback suspension is cited to P-1372, P-1883 and P-1924.
  - "About 20% of staff" now reads "RTX commercial-aero headcount, Collins and P&W" [P-0426].
- **Rows 4 and 9.**
  - PFS 2.0 [P-2017], the walk-away from a non-engine product [P-0148] and the MAX impairment tests [P-1936][P-1937] are labelled "UTC group, not P&W engines (analogy, inference)".
  - Row 4 now rests on P&W items [P-0735][P-1333][P-0273][P-0144][P-1524].
  - Row 9 rests on [P-0079][P-0069][P-2047].
- **Row 5.**
  - P-1974 is tagged [analyst], with "rivals weakened" stated as the analyst's premise.
  - The 43%-to-55% gain is dated to 2019-20, mostly before COVID, and reworded as a stated intent [P-0086].
  - The Gulfstream items move to row 6 as a competitive win.
  - The Falcon 6X stays as the clean analogue.
- **The §6 `join_rr_jv` "For" case.** "Our flag is the gate" now reads: in 2012 RR saw a P&W Joint Venture as its route back [P-1872]; whether that still holds is an inference, and RR now talks to every partner [P-2004].
- **Quick card objective 3** now reads "protect the dividend and repair the rating after shocks" [P-0566][P-0423][P-1362]. The engine-versus-buybacks clause is marked (inference). P-1887 is tagged [record].
- **Engine checks in financials.md** were credited to the wrong memo version. They are now credited to the committed `calibration.md` and the live `whatif` (+0.203, -4.410, -3.105, +1.759). The pre-merge draft's -2.21 and -3.10 are noted as superseded, and -3.105 is reconciled with the -3.11 used elsewhere.
- **The D&A row** is filled for 2020-23 (729, 642, 724, 736) [P-1527][P-1570]. The 2019 basis break is shown: 980 on UTC's basis, 614 restated by RTX.
- **Deliveries against plan.** The 740-against-1,800 pair mixed years and scopes, so it is dropped. The range is now 60-70% (138/200 and 375/600), and the slip prior changes from "halve" to "two-thirds".
- **Block D.** "Reached 90%" now reads "60% by mid-2023; 90% expected in 2-3 years (view)" [P-0758].
- **Playability: the Joint Venture test.**
  - Replaced by an expected-value test on P(UltraFan selected | RR launches `jv_pw`): break-even 3.71 / 20.36 ≈ 0.18, or about 0.23 with the allowance.
  - The always-true "prefers it to ours" clause is dropped.
  - A turn-1 `disclose` rule is added.
- **Playability: no exit.** P&W cannot cancel `uf_nb` (`validate` error), so only RR controls the exit; if RR cancels in turn 2, the case is worth +0.87.
- **Playability: adverse selection.** RR earns +23.90 solo against +11.79 in the Joint Venture when selected, so an offer signals that RR rates its own odds below about 23%.
- **"fps win is pure upside" (§7).** Qualified: fps on ours with NGSA on CFM gives -2.05, against -1.74. The joint-launch cases are in the §6 table, and NGSA is the priority.
- **P-1233.** It moves to the Joint Venture "For" case, since joining RR's engine shares RR's technology, not ours. P-1240 (integrated teams) now carries the "Against" case.
- **Prediction rule.** It is now based on the airframers' `whatif` timing payoffs: NGSA in 2028 gives +46.47, in 2029 +42.05 and in 2026 +34.65. P-2058 and P-1312 only bound the entry into service.
- **Launch timing.** "≤ airframe launch + 1" is replaced by "the turn's last year". With the upgrade in 2026 that year is best even against a 2026 NGSA (+2.56 against +2.46 and +1.66), and the wait costs Airbus nothing (+39.42 against +36.85).

**Low severity (all applied).**
- **Row 7.** "Share held at about 40%" now reads "claimed about 40% in Feb 2024 and aimed to hold it (view)" [P-0111].
- **No widebody.** The red line rests on P-1313, P-1700 and P-1676. P-1125 is cited as a decision P&W later regretted, and "never executed" is labelled (inference).
- **Row 2.** P-2019 is dropped (it concerned narrowbody re-engines).
- **Row 1 lag.** Now "slipped mid-2018 to after early 2019 waiting for Boeing; NMA never launched" [P-0125][P-2020].
- **Row 11.** Reworded to "worked through a castings supplier's shortfall rather than switching". Airbus-first allocation is cited to P-1054 and P-0162, and wider rationing is labelled (inference).
- **Cancel.** P-1342 is labelled a defence-programme analogy (inference). Cancellation rests on the engine rule and on P-1371 and P-1939.
- **The `gtf_next` disclosure** is tagged [engine]. P-0711 and P-1347 now sit on the wait rule and the franchise exception.
- **"About 10%" hurdle.** Marked as an inference from "more close to double-digit". Hard rule 1 carries the franchise exception.
- **Row 3.** Now "claimed 56% Jun 2017-Jun 2018 [own]", set against LEAP's 10:1 in 2017 [press/industry], not reconciled. "After the fixes" is removed from the profile and from the `upgrade.fit_pp` derivation in financials.md.
- **§9 quote.** Now exact: "deliver financial returns, not just bragging rights" [P-0702].
- **GS history columns** (P-1883, P-1887, P-1888) are tagged [record] wherever the profile cites them. `evidence.jsonl` is unchanged, as the audit advised.
- **Rating sequence.** S&P cut RTX to BBB+ in August 2023, and the October ASR then brought negative outlooks [P-1554].
- **Fleet-plan share.** P-1121 is added for "40% historically".
- **IAE price.** "$1.5bn per the 2019 brief; RR reported £1.5bn received" [P-1838][P-1874].
- **Fuel-efficiency claims.** The baselines of "20-25% by 2025" and "1% better" are now stated.
- **2000s margins.** Now "adjusted margins of 16-17% (2006-08)".
- **OE dilution and loss.** OE dilution is now "$0.7-1.05bn", and the OE loss fell "in 3 years (2016-19)".
- **COVID charge.** "$543M of unfavourable contract adjustments (including an impairment)"; job cuts are "about 15,000 RTX commercial-aero jobs (Collins and P&W)".
- **Guidance outcomes.** Now labelled "GS adjusted, our subtraction" [record].
- **Holding cost.** Now "about $0.75B a year nominal, about $1.0B alpha-loaded; -0.86 PV".
- **Labels in financials.md.**
  - The GS scale range is dated: 441-464 in 2019 and 2021-23, 345 in 2020.
  - The GTF breakeven outcome is labelled EBIT, not cash.
  - Three rows are relabelled from PLACEHOLDER to NOT CALIBRATED: the RR `jv_pw` terms, `pw_gtf2` and `pw_wb_new`.
- **§5 lags.** Unsupported lags are tagged (inference), and dated pairs are cited where they exist.
- **Rounding.**
  - 33.8% of RTX revenue (GS mix), with 34.7% of segment sales noted in financials.md.
  - Ex-GTF aftermarket revenue of 10,953 and 13,035.
  - R&D at 4.3% to 3.6% of sales.
- **Row 7 orders.** The JSON "defer, do not cancel" now reads "keep a committed gtf_next (do not cancel)".
- **Strain.** A note says the engine charges strain on narrowbody overlaps although the `rules` text names only narrowbody-plus-widebody. Under a supply-chain crunch, a turn-1 `gtf_next` goes only into a disclosure.
- **Order format.** Always pass `year` and `terms`: `validate` silently sets a missing year to 2026, which moves the case from +1.98 to +0.45.
- **`options`.** Use it only for `airframer_incentive_b`. It has no Joint Venture option, and its worst cases overstate hedge risk (-8.56 against -2.94).
- **Inactive flips.** The `pw_wb` and aggressive-terms flips are labelled inactive at calibration. `gtf_upgrade` counts as a narrowbody programme in the `pw_wb` test.

## Claims relabelled as inference

- The game constraint that replaced the IAE red line: no `gtf_next` and `join_rr_jv` aimed at the same airframer.
- "About 10% all-in": the hurdle, read from "more close to double-digit".
- "A new engine would compete with buybacks, not the dividend."
- "In the game 'committed' means disclosed for this turn": the NGSA hedge as the one exception.
- "Joining RR's UltraFan shares RR's technology, not ours."
- RR's 2012 view of a P&W Joint Venture as its route back: whether it still holds.
- The 2019 widebody plan "never executed".
- UTC-group conduct applied to P&W by analogy:
  - PFS 2.0 and the non-engine walk-away (row 4);
  - Collins MAX impairment tests (row 9).
- RTX's ending of a defence programme as an analogy for cancelling an engine (P-1342).
- Rationing between Airbus, spares and MRO beyond the 2024-25 statements (row 11).
- Every §6 hedge and Joint Venture probability, break-even and default, and the adverse-selection reading of a `jv_pw` offer.
- "Answer NGSA first" when choosing between disclosures.
- Lags for rows 3, 4, 5, 6, 11 (first part), 12, 13 and 14.

## Playability fixes

A player can now produce one set of turn-1 orders from the profile:
- `gtf_upgrade` true;
- no launch (odds about 0.2 with RR in play, below both the 0.24 break-even and the 0.45 doctrine threshold);
- `join_rr_jv` false;
- standard terms;
- conditional disclosures for `gtf_next` and for joining a Joint Venture;
- a prediction built from the airframers' timing payoffs.

These match the playtester's orders, which `validate` accepted with digest dc96eaf0. They are also plausible for the real company.

Other changes:
- **Without RR**, the same method gives about 0.5, so `gtf_next` launches in 2028.
- **Decision rules.** The hedge, Joint Venture and doctrine-premium rules are each stated as a formula with live `whatif` inputs. The §6 reference table adds:
  - the upgrade-aware hedge and cancel cases;
  - the joint fps/NGSA launches;
  - the Joint Venture with the upgrade and with RR cancelling;
  - the `gtf_next` plus join portfolio.
- **Mechanics now stated.** The engine rules the profile previously left out:
  - P&W cannot cancel `uf_nb`;
  - the join flag is free unless RR launches `jv_pw`;
  - a missing `year` defaults to 2026;
  - strain applies to narrowbody overlaps;
  - `options` has limits.

## Evidence gaps that remain

- **The P&W-RR UltraFan Joint Venture.** P&W has said nothing beyond a 2024 non-answer. RR's side comes only from RR's words, and the 2012 Joint Venture's fate is silence [P-1874][P-2004].
- **Selection odds.** Nothing in the evidence shows how an airframer would choose between `pw_gtf2` and UltraFan. Every §6 probability is inferred from engine payoffs.
- **Widebody.** The only widebody plan is in a 2019 industry report [P-1842].
- **The hurdle rate.** It is inferred from 2017-19 statements, and no explicit IRR has been given since 2019 [P-1243][P-0746].
- **Per-engine aftermarket economics.** GS's 35% margin plug is not reconciled to its own segment model [P-1754][P-1789]. Aftermarket margin remains the largest uncertainty in P&W's payoff.
- **Strain.** It is a PLACEHOLDER: no evidence isolates the cost of overlapping programmes [P-0279][P-1234].
- **Two pairs of sources disagree and cannot be reconciled from the file:**
  - LEAP's 10:1 order lead in 2017 [P-1847] against P&W's self-reported 56% of selections [P-0075];
  - the IAE price in $ [P-1838] against £ [P-1874].
- **D&A has a basis break.** The UTC and RTX filings report different 2019 figures [P-1481][P-1527].
- **Not fixed here:**
  - `calibration.md` said the selection gain came "after the 2017-18 durability fixes" in its `upgrade.fit_pp` derivation. That wording, and the P-0075 finding it rested on, have been corrected: the quotes do not tie the gain to the fixes.
  - profile.md is now about 6,700 words, above the brief's 6,000 target. The playability fixes added the hedge arithmetic, the odds method and the Joint Venture mechanics.
