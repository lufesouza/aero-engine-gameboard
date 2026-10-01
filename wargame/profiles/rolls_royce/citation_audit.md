# Rolls-Royce profile: citation audit

**Audit date:** 2026-10-01.

**Scope.** Three independent audits of the Rolls-Royce (`rolls_royce`) profile were integrated here:
- **citations:** every cited id read in full for the Quick card, §5, §6, §9 and all 12 rows of `reaction_function.json`;
- **numbers:** every figure in `profile.md` and `financials.md` checked against its MS or Capital IQ cells, the calibration memo, live `rules` and read-only `options` / `whatif` on the `calib` run;
- **playability:** turn 1 of `calib` played from the profile alone with `brief`, `rules`, `options`, `whatif` and `validate --side rolls_royce`.

Files fixed: `profile.md`, `reaction_function.json` and `financials.md` in this folder. Evidence: `evidence.jsonl` (R-####) only. No other company's profile, role card or scratch area was read.

Every number added during the fixes was re-run with `whatif --side rolls_royce` on `calib`. The `calib/state.json` md5 is unchanged (67dae2bf…).

---

## Counts before fixes

**What the columns mean.**
- **Pairs** = claim-id pairs: the distinct ids cited in each claim unit (a paragraph, bullet or table row), counted on the pre-fix files.
- **Claims, Supported, Weak and Unsupported** are as each auditor reported them.
- The numbers auditor gave totals only, not a split by section.

| Area | Lens | Claims | Pairs | Supported | Weak | Unsupported |
|---|---|---|---|---|---|---|
| Quick card | citations | 12 | 22 | 11 | 1 | 0 |
| §5 Reaction function | citations | 27 | 75 | 22 | 4 | 1 |
| §6 Lever playbook | citations | 14 | 24 | 9 | 5 | 0 |
| §9 Decision procedure | citations | 2 | 5 | 2 | 0 | 0 |
| `reaction_function.json` (12 rows) | citations | 76 | 95 | 65 | 10 | 1 |
| **Citations lens total** | | **131** | **221** | **109** | **20** | **2** |
| `profile.md` + `financials.md`, numeric claims | numbers | 291 | 833 (467 + 366) | 266 | 22 | 3 |
| Engine-checkable claims (profile, JSON, agent file) | playability | 31 | n/a | 22 | 6 | 3 |

Claim-id pairs in the pre-fix `profile.md`, by section:

| Section | Header | Quick card | §1 | §2 | §3 | §4 | §5 | §6 | §7 | §8 | §9 | §10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pairs | 1 | 22 | 52 | 80 | 82 | 73 | 75 | 24 | 26 | 17 | 5 | 10 |

Pairs in the pre-fix `financials.md`, by section: §1 36, §2 33, §3 43, §4 82, §5 22, §6 26, § Game calibration 124.

**Findings by severity**

| Lens | High | Medium | Low | Fixed in the three files | Not fixed |
|---|---|---|---|---|---|
| Citations | 0 | 4 | 16 | 20 | 0 |
| Numbers | 0 | 2 | 19 | 21 | 0 |
| Playability | 3 | 5 | 7 | 14 | 1 (agent file `whatif` example: outside the three files) |

That is 55 findings addressed. A few appear in two lenses: the $1.4-1.9B strain range, the 2025 Boeing strike and the R-1849 reading.

**After fixes** (cite_check):

| File | Citations | Distinct ids | Missing |
|---|---|---|---|
| `profile.md` | 501 | 279 | 0 |
| `reaction_function.json` | 106 | 95 | 0 |
| `financials.md` | 372 | 242 | 0 |
| All three, union | | 413 | |

`reaction_function.json` is valid JSON with 14 rows. Every row has the six required keys, and every `strength` is one of strong, moderate or weak.

`profile.md` is now 7,047 words (`wc -w`), up from 6,000. That exceeds the brief's 6,000-word target, mainly because of the playability fixes:
- the timing rule;
- the contested-incentive table;
- the upgrade-strain rule;
- two new reaction rows;
- a return template.

---

## Main fixes

**Medium (citations and numbers)**
1. **R-0814** (rf row 8). "One-third of civil fixed cost removed" became "about 9,000 roles cut, including about one-third of civil aerospace management roles", which is what the quote says.
2. **R-1849.** Boeing's 2025 remark is about supply-chain durability work with GE and CFM. In §6, §7 and rf row 3 it now reads "mention only GE and CFM (inference: RR not top of mind; not a selection signal)". The load-bearing evidence moved to R-1830 and R-1831.
3. **Partner as a necessary condition** (§5 row 1, rf row 1). Now reads "a partner is preferred to share risk, but Solo is kept as an option" [R-1010, R-1022].
4. **Joint Venture preference applied to P&W** (§6, §9, rf row 12). Now labelled as an inference. Friction ids R-0318, R-1892, R-1893 and R-1875 were added (see "Playability fixes" for the expected result).
5. **"Double the first stated cost"** (§3). Now reads "(inference) about 1.6x the first full estimate (£1.5bn → £2.4bn) [R-0724, R-0760]; the 2018 figure alone rose 1.3x [R-0697]".
6. **"Six worst contracts"** (§3). Now reads "six most onerous customers, over half of the £1.4bn provision" [R-0433, R-0432]. "All significant onerous airline contracts renegotiated by mid-2025" is now cited to R-0448.

**Low, all applied**
- **Lags.**
  - Technology slip: was "~1 year". Now "~2 years per slip (TEN blade, Nov 2019 to Aug 2021); withdrawal within months (NMA)" [R-1210, R-1251, R-0980].
  - Rows 6 and 7: the lag spans are now inferences anchored to R-1177, R-1239 and R-1023.
- **Trent 1000 cost split.** "Over half of £2.4bn" is now "just over half of the then £1.5bn estimate" [R-0725, R-0724]. Fixed in §3 and rf row 7.
- **Wrong or weak precedents.**
  - F136 and NMA moved to `cancel` precedents "by analogy". The trigger now rests on R-0356, R-1946 and R-0367.
  - R-0359 dropped from row 6.
  - Gulfstream → Pearl now attributed to P&W's claim [R-1881] and an industry report [R-1791], as inference.
  - R-1601 reworded as "pays back within years, not UltraFan's 15".
  - R-0921 relabelled as inference.
  - R-1002 now reads "demonstrator kept alive through COVID … though new-programme capitalisation was cut" [R-0986].
- **Partner shares.** "Goes 50:50 only with GE" became "its one named 50:50 venture is the Engine Alliance with GE (widebody); partners otherwise take 14-50%" [R-1894]. Fixed in §4 and rf row 12.
- **R-1493.** Moved into the 2004-21 era (2019) in §5 row 5 and rf row 5.
- **rf row 1.** R-1017 added (self-funded demonstrator).
- **rf row 11.** "RR held output flat" became "OE deliveries broadly flat in 1H25 under casting and forging constraints, 23 of 122 large engines built as spares" [R-1302, R-1299].
- **Quick card.**
  - Retitled "stated 2023-25, consistent with behaviour".
  - [record] ids added: R-0062, R-0032, R-0075, R-0071.
  - "Never again needs equity" became "from operating cash, not equity".
  - R-0319 added for the A330neo.
  - The strain range $1.4-1.9B became "$1.9B, $1.4B and $1.1B for turns 1, 2 and 3; $0.74B for 2029 then 2032" [whatif].
- **Dates and ids.**
  - Boeing strike 2025 → 2024.
  - Trent 7000 slip cited to R-1132 and R-0254, as inference.
  - "Four issues of ~£200m": marked as the reader's paraphrase. The RR-worded £100m-a-year contingency was added [R-0675].
  - Capex below consensus: now "2021, 2022, 2024 and 2025 (2023 not in evidence)", in §1, §2 and §8.
  - The 8-year ramp downside is now an inference from the memo's range [R-0904, R-1419].
  - Eras: now Rishton 2011-mid-2015 and East mid-2015-22, cited to R-1313, R-0310, R-1083, R-0942 and R-1561.
- **`financials.md`.**
  - Scale-check id: R-0225 → R-0245.
  - MS revision relabelled "27 Apr 2026 via Capital IQ, £3,368m → £3,651m".
  - 29.4p is now marked as a Capital IQ normalised actual.
  - Civil margin: "MS 2025e 22.2%; Capital IQ actual 20.5%, computed". Civil revenue corrected to the cell value £10,380m.
  - 2017 old-GAAP bases flagged: £112m IFRS 15 participation fees; +£4,207m old GAAP.
  - 2019 DPS: 4.6p paid against Capital IQ's 11.7p, flagged.
  - Hedge lines relabelled as "cash flows on other financial assets and liabilities (mainly FX hedge settlements, inference)".
  - Borrowings and book-equity extremes limited to the years each item covers.
  - 2027 targets dated and shown as superseded that day [R-0893].
  - Trent 1000 £2.4bn shown as a revised estimate, not an outturn.
  - `strain.background` and the engine options relabelled n/a, not CALIBRATED or PLACEHOLDER.

## Claims relabelled as inference

**`profile.md`**
- **Quick card and §9:**
  - "never aggressive on the A350" (now consistent with R-0334, not [own]);
  - the turn-2 NGSA window;
  - the no-turn-1-launch consequence of the timing rule;
  - the P(selected) ladder, including the new 0.2 "signal";
  - the §9 step 12 disclosure (now marked "e.g., a script, not an RR quote").
- **§3:**
  - crisis-cost multiplier 1.6x;
  - Trent 7000 ~1-year slip;
  - 8-year ramp downside;
  - "four issues of ~£200m".
- **§5:**
  - row 2 launch strength (derivative and contract precedents applied to a new engine);
  - rows 6 and 7 lags;
  - row 6 "RR answers wins with product";
  - row 8 `wb_demand_boom` Do Nothing;
  - row 10 `engine_maturity_slip` → launches a turn later;
  - row 4 cancel precedents (by analogy);
  - new rows 13 (P&W widebody) and 14 (other injects).
- **§6 and §7:**
  - the Joint Venture preference mapped onto `jv_pw`;
  - the R-1849 reading;
  - TEN as a share defence [R-0921];
  - open fan lowering P.

**`reaction_function.json`**
- Row 6: a P&W setback raises UltraFan's incentive and lowers P&W's appetite to join.
- Row 12: the partnership preference applied to P&W.
- Row 2: launch strength lowered to moderate.

**`financials.md`**
- Hedge-book attribution and hedge settlements.
- Capital IQ's 2019 DPS basis.
- The computed 20.5% Civil margin.

## Playability fixes

1. **Upgrade strain (high).** The engine code (`_evaluate_supplier`) treats the `t1000_upgrade` 3-year window as a strain window against any development. Verified with `whatif`:
   - turn 1: `uf_nb` Solo + upgrade -9.68 against -9.18 alone; `uf_wb` + upgrade -4.46 against -3.96; `jv_pw` + upgrade +0.16 net;
   - turn 2: -0.99 of strain;
   - upgrade 2026 + `uf_nb` 2029 = -6.08 = -6.90 + 0.81, so no overlap.

   Added as a red line in the Quick card, §5 rows 7 and 11, §6, §9 step 9, rf rows 7 and 11, and the `financials.md` `strain.background` note.
2. **Launch timing (high).** Orders are sealed and simultaneous, and disclosures reach players a turn later (`engine.py` `brief`). Added:
   - a Timing rule and a definition of "announced" (an earlier turn's disclosure or statement naming the programme and this turn);
   - every trigger now keys on announcements;
   - turn 1 has no UltraFan launch;
   - an unannounced selection that falls back is handled by row 4;
   - the disclosure now promises launch only "for a turn an airframer announced in advance".
3. **Contested incentive (high).** `airframer_incentive_b` compares UltraFan only with the fallback engine. §6 now carries the `whatif` airframer-PV table against open fan, P&W and GE:
   - NGSA 2026: open fan 43.15 against UltraFan 39.55;
   - fps: P&W aggressive 17.24 against 15.58;
   - A350 Re-engine 2026: P&W -0.12 against -0.29;
   - 787 Re-engine: UltraFan 0.78 / 2.80 against GE -0.08 / 2.47.

   §9 steps 3-4 now use the minimum margin. A new §5 row 13 covers P&W's `pw_wb`. The A350 "never aggressive" rule now has an explicit P&W exception.
4. **Joint Venture in practice (medium).** Solo is declared the expected result once a launch customer announces UltraFan:
   - at P 0.6, Solo beats the Joint Venture by $7.3B on NGSA and $4.3B on fps;
   - at P 0.35, the NGSA Joint Venture (+2.02) is chosen if P&W announced; fps fails the $2B bar.

   The signalling sequence is spelt out: P&W announces in turn t-1.
5. **Concurrency rule (medium).** "Same turn" became "no overlapping development windows" everywhere, with the cross-turn figure ($0.74B).
6. **Setback precedence (medium).** Rows 10 in md and JSON now match:
   - `ultrafan_test_setback`: launch only if a selection is announced for that turn;
   - `engine_maturity_slip`: no order change (it moves the airframers' technology date, not our engines).
7. **"Signalled" (medium).** Defined as a signal with P 0.2. On [T1] numbers it never clears the launch bar alone.
8. **Low:**
   - prediction method: launch-turn PV comparison, R-1867, R-1833;
   - `expected_delta_pv_b` defined as the step-5 expected PV;
   - a full return template;
   - `validate`'s limits stated;
   - perspective → tag map in the profile header;
   - status quo "best except a 787 Re-engine on UltraFan";
   - a turn-4 narrowbody launch allowed;
   - the aggressive trigger rebased on the contested incentive;
   - inject rows for `gtf_next_test_setback`, `fuel_price_spike`, `trade_dispute` and `quiet_turn`.

## Remaining evidence gaps and open items

**Evidence gaps**
- **No airframer text on engine choice for fps, NGSA or either Re-engine,** beyond Airbus's open-fan focus [R-1867, R-1868]. All P(selected) values are doctrine.
- **No P&W widebody precedent.** Row 13 is inference.
- **No closed RR-P&W Joint Venture since 2012,** and why the 2012 agreement lapsed is not in the evidence [R-0916, R-1892].
- **GTF 2023 powder-metal recall:** absent.
- **UltraFan programme cost and schedule:** none beyond the NMA estimate [R-0965, R-0966].
- **Unsourced or incomplete figures:**
  - "four issues of ~£200m" exists only in a reader's finding (R-1220);
  - the mid-term FCF target (£4.2-4.5bn) is not in R-0893's quote;
  - the cancelled 7.1p final is not stated anywhere;
  - 2023 capex consensus (R-1723) is missing;
  - gross borrowings after 2021 (R-0010) are missing;
  - 2021 book equity (R-0028) is missing;
  - the start of the Rose era is evidenced only by 2010 (R-1313).
- **One-sided or dated views.** Customer views are one-sided (Boeing 2010-12, Airbus FY2025 only). The MS model predates FY25. P&W's words end in 2021.

**Placeholders.** `jv_pw` dev_years and strain_relief, `strain.full_overlap_b` and `norm_years`.

**For the engine owner, outside the three files**
- The `rules` strain text names only narrowbody-widebody overlap, but the code charges every pair of windows, upgrade included.
- `validate` ignores `disclose` and `prediction`.
- The `.claude/agents/rolls-royce-strategist.md` `whatif` example orders `jv_pw` in turn 1 without P&W's flag and returns 0.00. Its perspective list names 5 of the evidence's 12 values; the profile header now maps all 12.
- `calibration.md` still cites R-0225 for 2024 deliveries (the correct item is R-0245).
