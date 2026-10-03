# Citation audit: Airbus executive profiles

**Date:** 2026-10-03

## Scope

- **Files fixed:**
  - `faury.md`;
  - `toepfer.md`;
  - `wagner.md`;
  - `historical.md`;
  - `teams.md`;
  - `README.md`, kept in step with the profile changes.
- **Evidence checked against:**
  - `evidence.jsonl` (109 AX items);
  - `../evidence.jsonl` (A items).
- **Audit.** One independent audit read every load-bearing claim against the quotes of the items it cites, using `cite_check.py --show`. It covered:
  - the Quick cards;
  - the commitment track records;
  - the "In the game" sections;
  - the Enders, Leahy and Scherer cards;
  - in `teams.md`: the decision rule, incentive map, tensions, doctrine-to-decisions table and ExCo script.
- **Isolation.** Airbus only. No Boeing-side profile, digest or summary was read.
- **Not edited.** The evidence files. Reader findings that overreach their quotes are listed under remaining gaps.

## Counts before fixes

**Claims**

| Measure | Count | Share |
|---|---|---|
| Load-bearing claims audited | 182 | 100% |
| Supported | 125 | 69% |
| Weak | 50 | 27% |
| Unsupported | 7 | 4% |

**Citations.** All 404 resolved to existing ids (0 missing):

| File | Citations before | Citations after | Distinct ids after | Missing after |
|---|---|---|---|---|
| `faury.md` | 199 | 213 | 85 | 0 |
| `toepfer.md` | 47 | 47 | 20 | 0 |
| `wagner.md` | 42 | 45 | 24 | 0 |
| `historical.md` | 34 | 41 | 29 | 0 |
| `teams.md` | 82 | 92 | 51 | 0 |
| `README.md` (not audited) | 7 | 13 | 13 | 0 |

**Findings: 35.**
- By severity: 2 high, 15 medium, 18 low.
- By main problem:
  - accuracy 11;
  - perspective 7;
  - fairness 5;
  - unsupported 5;
  - weak 3;
  - game use 3;
  - presentation 1.

**What was already right.** Pay weights and scores, LTI targets and outcomes, deliveries, net cash, FCF, EBIT Adjusted, the dividend and the €300m Board threshold matched their quotes. The game mechanics matched `config/default.json`.

**Outcome.** Every finding was addressed: all 2 high, all 15 medium and all 18 low. One part was not done: the high finding on Leahy also asked for the AX-0099 finding text to be corrected. That text is in the evidence file, which was out of scope, so it is listed under remaining gaps.

## Main fixes

### `faury.md`

- **Quick card, red line.** "No lever ... gets a second turn" is replaced by: no lever a regulator or court could read as misconduct (inference from [AX-0073, AX-0081]). Delay Tactics is in bounds only as `../profile.md` models it, as a legitimate first claim on scarce capacity. Nothing shows him acting against a rival's supply chain.
- **Delay Tactics row.**
  - The Spirit comparison is dropped.
  - The bounds now come from `../profile.md` hard rule 4 (inference, game parameter).
  - The "changes who enters service first" test is now justified by `whatif` PV, not by the integrity pillar.
- **NGSA timing row.**
  - Personal LTI vesting is no longer the reason for the 2028 preference. AX-0048 is the 2022 plan, measured over 2023-25.
  - The preference now rests on three things: the technology-ready year (launch 2028 for EIS 2035), the early-EIS penalty and hard rule 1, and the company EBIT and FCF targets shared by about 5,200 managers [AX-0034].
  - "Technology-ready year (2028 at base)" is corrected to 2035, the EIS year, which is how the engine and `teams.md` define it.
- **Disclosure row.**
  - Was: "never financial targets, never a point".
  - Now: never the internal long-term-plan targets [AX-0005]. Operating guidance can be a number [AX-0053]. Windows and ranges for EIS and rate are a preference (inference).
- **Biases.**
  - "Attribute slips to suppliers" and "blames them publicly" now read as attribution, with the supplier side's corroboration [AX-0044, AX-0045].
  - "Resilience" moved out of the biases into the Voice list, as the Board's words [AX-0050].
  - "Strategy ahead of delivery" is labelled as the Board's scoring, with counter-evidence.
  - "Comfort with the downside" moved to §4 Risk, as a note on the Board's incentive design, beside his 55,880 shares [AX-0087].
- **Track record.**
  - The rate-75 row says the supplier in AX-0054 is illegible, and that Pratt & Whitney's parent is "one of the A320neo engine suppliers".
  - The hydrogen row is marked as a company ambition, not attributed to him.
  - The read-across says that only the 2025 delivery reset is shown to have been met.
  - The 2025 deliveries row adds 766 to 793 and the Board's supply attribution [AX-0009].
- **Smaller corrections:**
  - "record" EBIT is dropped;
  - "delegates portfolio direction" is reversed to "sets portfolio direction from the top" [AX-0078];
  - the LTI design is labelled as the 2022 plan, with the 2025-grant change [AX-0049];
  - the risk table is tagged [outside: P&W];
  - the H140 is a result, not a launch criterion;
  - the guidance reset is attributed to the company.

### `toepfer.md`

- **Peak-cash test.**
  - Now stated in dollars: €4.75bn ≈ $5.2B at an assumed $1.10 per € (a game assumption).
  - Compared on unloaded cash amounts, because the 1.30 alpha loading is already in delta PV.
  - Computed by hand from launch years and `rules`, because `whatif` reports no annual spend.
- **LTI motive.** The 2026-28 LTI window is removed from the NGSA row. His LTI is not in the evidence.
- **Disclosure** is re-worded as in `faury.md`.
- **Biases.** Both are relabelled as company practice that the CFO voices (inference), and reported EBIT (€6,082m) is shown beside EBIT Adjusted.
- **FY2024 dividend.** Moved from the track record to the Era section, as context.

### `wagner.md`

- **NGSA veto.** "A turn-1 launch" is changed to "a launch in 2026-27", which matches the `teams.md` ramp shield. A 2028 launch, the company default, now passes.
- **Game proxies.** Added: no NGSA launch before 2028, and no A350 Re-engine before turn 3.
- **Objectives.** "CEO priorities cascade" is replaced: the business objectives cascade [AX-0071], and applying the CEO's priorities to Wagner is inference.
- **Counts.** The leaked build-prompt sentence is deleted. The item counts are corrected: AX-0093 refers to the role and names nobody.

### `historical.md`

- **Leahy.**
  - The sentence "Boeing linked the change to Airbus's ethics issues" is deleted. Replaced by: "No item links Leahy to any compliance matter."
  - The Heathrow line is re-headed as "Publicly questioned the 787's reliability" (as quoted by a journalist), and McNerney's hedge is quoted in full.
  - "Bullish" is dropped. The "order cycle had probably peaked" phrase is attributed to the journalist.
  - The Delay Tactics line in his card is replaced by: the rules come from `../profile.md`, and nothing in his record bears on it.
- **Enders.**
  - The 2,000-aircraft benchmark and "well short" are removed. The A220 is stated as a programme in production, with 949 delivered or in backlog.
  - "Where Boeing had no dedicated product", "enter a segment cheaply", "dual sourcing" and "confident framing" are removed. The unitemised "upset" remark is removed.
- **Scherer.**
  - His last year now carries the context: deliveries rose from 766 to 793, the Board attributes the slips to supply, and no item attributes these outcomes to him.
  - The item counts are corrected.

### `teams.md`

- **Delay Tactics.** "At most once per game" now cites `../profile.md` hard rule 4 (inference, game parameter), not AX-0073.
- **CFO peak-spend test.** Re-written with an explicit exchange rate, unloaded amounts, a per-year strain formula ($3B × min(1, overlap/5) / overlap) and worked figures:
  - NGSA alone: $3.6B a year, which passes;
  - with an overlapping A350 Re-engine: about $5.0B, which passes narrowly;
  - under a supply crunch, or with Delay Tactics: $5.3-5.5B, which is flagged.
- **LTI motive.** Removed from the incentive map and the timing step. The 2025 grant vests in May 2029 [AX-0047], and its window is not in the evidence.
- **Decision rule.** Was "the CEO proposes and decides". Now: the CEO leads the ExCo, which prepares strategy collectively, and he is accountable for execution [AX-0029]. The final call in the game is inference.
- **Tensions.** Labelled as inference. "Most generously" is corrected, since FCF scored 157%. AX-0042 is tagged [outside: P&W], and "late" is limited to the 3 December delivery reset.
- **Wording.**
  - "A level playing field" is dropped from the statement register.
  - The disclosure rules are aligned with `faury.md`.
  - The Board's stance now carries its "resilience" framing [AX-0050].

### `README.md`

- **Disclosure rule.** Aligned with the profile files.
- **Wagner and Scherer counts.** Corrected.
- **"Nine outside remarks".** Corrected to eight, plus one 2026 Board line. The same correction was made in `teams.md`.
- **Gaps list.** Now includes the reader findings that overreach their quotes.

## Fairness changes

1. **Faury.** The Quick card no longer implies he would take one turn of a lever a regulator could read as misconduct. It now says that nothing in the evidence shows him acting against a rival's supply chain.
2. **Faury, Spirit.** His Spirit acquisition, which secured Airbus's own supply [AX-0061], is no longer compared with a covert game lever.
3. **Faury, attribution.** Supply attribution is no longer presented as a personal habit of blaming suppliers. The supplier's own 2021 remarks are shown beside it.
4. **Board wording.** The Board's narrative ("resilience") and the Board's scores ("strategy over delivery") are no longer presented as Faury's personal biases.
5. **Pay as motive.** The timing of a $25B launch is no longer tied to personal vesting, for Faury, Toepfer or the team.
6. **Leahy, ethics.** His name is no longer tied to Airbus's ethics probes. No quote supports that link.
7. **Leahy, motive.** "Exploiting Boeing's weak moments" is removed. McNerney's hedged guess is quoted in full.
8. **Leahy, Delay Tactics.** His card no longer carries the line, which suggested a leaning to covert tactics.
9. **Enders.** The A220 is no longer judged against an unsourced 2,000-aircraft aspiration.
10. **Scherer.** The 2025 misses now carry their context and the Board's own attribution to supply.
11. **Toepfer.** Company reporting practice (EBIT Adjusted) is no longer presented as his personal framing.

## Claims relabelled as inference

- **`faury.md`:**
  - the misconduct red line, inferred from the integrity baseline;
  - the "proven near-term case" launch test (H140);
  - "strategy and European items alongside delivery" (from the Board's scoring);
  - the Disclosure preference for windows and ranges;
  - the Delay Tactics bounds (game parameter, `../profile.md` hard rule 4);
  - that the vesting floor shapes his risk-taking (not shown).
- **`toepfer.md`:**
  - the peak-cash threshold (game guardrail) and the $1.10 per € rate (game assumption);
  - cash conservatism and adjusted-metric framing, now company practice voiced by the CFO;
  - judging programmes on run-rate;
  - the range preference in disclosure.
- **`wagner.md`:** applying the CEO's 2026 priorities to him.
- **`teams.md`:**
  - the CEO's final call in the game;
  - all five tensions (1 and 3 explicitly);
  - Delay Tactics "at most once" (game parameter);
  - the peak-spend test;
  - the later-capex tie-break;
  - the range preference in disclosure;
  - Toepfer's and Wagner's LTI roles.
- **`historical.md`:** both remaining Enders "today's ExCo" lines, marked "inference, weak".

## Remaining gaps

- **No own words.** No Airbus transcripts are in the corpus, and Faury has one own-words line [AX-0081]. Every behavioural rule remains inference from pay design, roles and the Board's narrative.
- **Reader findings that overreach their quotes.** These were not edited here and need the reader pipeline (`exec_merge_evidence.py`):
  - AX-0099 and A-0128 mention Airbus's ethics issues;
  - AX-0038 judges the A220 against "2,000 aircraft";
  - AX-0084 reads the H140 as a launch criterion;
  - AX-0048 states the 2022 design in the present tense;
  - AX-0095 summarises McNerney's reply without quoting it.
- **Game assumptions, not evidence.** The $1.10 per € exchange rate and the peak-spend threshold. No evidence item gives either.
- **Pay terms.**
  - The live LTI's performance period and EPS weight are not in the evidence; AX-0047 gives only vesting in May 2029.
  - The Scope 1&2 weight is illegible [AX-0049].
  - Toepfer's and Wagner's pay terms are absent.
- **Engine supplier.** The supplier named in AX-0054 is illegible. The link to Pratt & Whitney's parent rests on its own 2021 remarks [outside: P&W].
- **Rate reset.** Whether the end-2027 rate is met lies outside the evidence.
- **Dates.**
  - Wagner's arrival year is cut off [AX-0108].
  - Toepfer's start date is absent.
  - Enders's and Scherer's tenure dates are absent.
  - The 2026 priority weights are read in printed order [AX-0073].
- **Weak claims.** The audit rated 50 claims weak but itemised only the 35 findings. Weak claims outside those findings were not re-checked, and no second audit has been run on the fixed files.
- **Pay-table conflict.** The 2025 STI of €1,582k conflicts with the €2,925k earned [AX-0076, AX-0066].
