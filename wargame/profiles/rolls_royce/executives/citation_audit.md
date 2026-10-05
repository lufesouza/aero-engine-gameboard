# Rolls-Royce executive profiles: citation audit

**Audit date:** 2026-10-04.

## Scope

**Files audited and fixed** (in this folder):
- `erginbilgic.md` (CEO);
- `mccabe.md` and `kakoullis.md` (CFO);
- `operations.md` (Civil Aerospace presidents: Cholerton, Watson, Schulz).

`teams.md`, `README.md` and `../profile.md` were being written by other agents. They were not edited, and they were not audited.

**Evidence.** `executives/evidence.jsonl` (RX-####, 298 items) and `../evidence.jsonl` (R-####). The only other file read was `../profile.md`, to check one doctrine claim. No Boeing, Airbus, Pratt & Whitney or CFM profile was read.

**Method.**
- `cite_check.py <file> executives/evidence.jsonl evidence.jsonl --show` was run on each file. Every cited item was then read in full: speaker, role, quote, finding and numbers.
- Every load-bearing claim in three sections was judged SUPPORTED, WEAK or UNSUPPORTED against its cited items:
  - the Quick card;
  - the commitment track record;
  - "In the game", including the CFM/GE and ExCo parts. For `operations.md` this also covers "What the seat stands for".
- A claim is one bullet, sub-bullet, table row or paragraph that cites ids. Outcomes that appear only in an item's reader note or numbers field, and not in its quote or data cells, were judged WEAK.
- Header, "By dimension" and gaps sections were read for fairness, perspective and accuracy. Findings there are listed with the others.
- Every engine figure was re-run on a scratch `five-player-2045` run with all three engine makers, using `options --side rolls_royce` and `whatif`. All of them reproduced, including the 2040 widebody engine counts (41 against 192) and the GEnx loss of 10 engines a year. The scratch run was then deleted.

## Counts before fixes

| File | Section | Claims | Claim-id pairs | Supported | Weak | Unsupported |
|---|---|---|---|---|---|---|
| `erginbilgic.md` | Quick card | 39 | 64 | 30 | 8 | 1 |
| | Commitment track record | 11 | 38 | 9 | 2 | 0 |
| | In the game | 19 | 37 | 12 | 7 | 0 |
| `mccabe.md` | Quick card | 28 | 53 | 19 | 9 | 0 |
| | Commitment track record | 13 | 27 | 7 | 6 | 0 |
| | In the game | 12 | 22 | 8 | 4 | 0 |
| `kakoullis.md` | Quick card | 36 | 59 | 26 | 10 | 0 |
| | Commitment track record | 15 | 23 | 3 | 12 | 0 |
| | In the game | 16 | 26 | 11 | 5 | 0 |
| `operations.md` | Quick cards (3 people) | 49 | 67 | 36 | 12 | 1 |
| | Commitment tables | 15 | 34 | 11 | 4 | 0 |
| | In the game, reactions, seat | 33 | 59 | 18 | 15 | 0 |
| **Total** | | **286** | **509** | **190** | **94** | **2** |

**Weak claims by cause:**
- **Kakoullis track record (12 weak):** most outcomes (1,044 shop visits, 88%, 1,227, £792m, £29m, H1 £405m, "two agencies", 101%) were in reader notes rather than quotes. £505m conflicted with the data cells.
- **`operations.md`:** the "In the game" weak claims were mostly unlabelled inference, plus ten Unknown Executive citations without a flag.

**cite_check before fixes:**

| File | Citations | Distinct ids | Missing |
|---|---|---|---|
| `erginbilgic.md` | 221 | 126 | 0 |
| `mccabe.md` | 148 | 74 | 0 |
| `kakoullis.md` | 162 | 66 | 0 |
| `operations.md` | 178 | 84 | 0 |

**Findings by severity**

| File | High | Medium | Low | Fixed |
|---|---|---|---|---|
| `erginbilgic.md` | 1 | 9 | 15 | all |
| `mccabe.md` | 0 | 5 | 17 | all |
| `kakoullis.md` | 0 | 5 | 16 | all |
| `operations.md` | 0 | 5 | 16 | all |
| **Total** | **1** | **24** | **64** | **89** |

**cite_check after fixes:**

| File | Citations | Distinct ids | Missing |
|---|---|---|---|
| `erginbilgic.md` | 226 | 127 | 0 |
| `mccabe.md` | 158 | 75 | 0 |
| `kakoullis.md` | 189 | 82 | 0 |
| `operations.md` | 186 | 83 | 0 |

## Main fixes

**High**

1. **Erginbilgic, `uf_nb` row.** The row made Solo his default once a launch customer names UltraFan, and cited RX-0118 for it. The main point of RX-0118 is "our preference is partnership". The row now reads:
   - partner first: `jv_pw` if P&W has announced `join_rr_jv` [RX-0118, RX-0138];
   - Solo as the fallback, "If it doesn't work, we can consider alternatives" [RX-0072];
   - the engine comparison (Solo +16.50 against Joint Venture +8.13 once selected) is labelled inference.

**Medium: Erginbilgic**

2. "Very aligned with Airbus ... even after Airbus called it challenging" [RX-0084]. The Airbus remark is in no quote, only in the reader note on R-0442. It was deleted and replaced with his own words.
3. "When British Airways chose GE" is not in the evidence. It was deleted.
4. "The GTF went to Watson" (gaps) is not in the evidence. It was deleted. No RR turn in either evidence file mentions the GTF.
5. An analyst's complaint ("airline and lessor complaints that RR had become less accommodating") was presented from RX-0133, whose quote has only his answer. It was replaced with his words: some customers were "disappointed", and relations had improved.
6. The bias "Guide low ... understate dates and upside" contradicted the evidence that his dates were optimistic. It now reads: guide low on profit and cash; engineering and supply dates run the other way.
7. R-1579 (McCabe's CMD words on the £25m sign-off and hurdle) sat in his decision rules without attribution. It is now attributed.
8. RX-0120 was presented as UltraFan being "superior to both incumbents' routes". That is the reader's interpretation. It was replaced with the quote; he names no rival design.
9. "A self-funded demonstrator" contradicted RX-0086 ("some additional funding"). It was corrected.
10. Fairness: see "Fairness changes" (slips).

**Medium: McCabe**

11. The investment-grade outcome was cited to RX-0171, which is Kakoullis's 2022 commitment. It was re-cited to RX-0102 and RX-0261.
12. The quoted phrase "for the right opportunity" is not in RX-0261. It was replaced with her words: "we could go up to that point" and "we don't have any intent of levering up for buybacks".
13. "Accepted about £800m of legacy concession outflows rather than keep deferring them" imputed a choice. It now states the outflow and the age of the deals [RX-0231].
14. ExCo: "mid-to-high-teens hurdle ... that is alpha 0.6 on capex (rules)". The engine has no hurdle input, and alpha loads both capex and strain. This is now labelled as a proxy (RR's 10% WACC and 0.6 alpha; inference).
15. Track-record outcomes from reader notes were unlabelled: 109%, £0.4bn and £280m, the bond repayment dates, £181m. They are now marked †. The FY2025 FCF of £3,270m [R-0220] was added to the 2027 FCF row.

**Medium: Kakoullis**

16. Fairness: see "Fairness changes" (the 2023 guide).
17. The 2022 FCF of £505m came from a reader note. The CIQ and MS data cells give £491m [R-0217, R-0057], and the figure was corrected in three places. 2021 FCF is now -£1,442m [R-0217].
18. The investors' words he relayed ("set achievable targets ... then achieve them or even beat them" [RX-0165]) were shown as his own objective. They are now labelled as investor feedback; his own words are "deliver on our commitments" [RX-0182].
19. "Long-dated bets need a higher risk-adjusted IRR" is in the reader note on RX-0181, not the quote, and the game section used it three times. It is now relabelled: "scenario-tested IRR" from the quote, and the long-dated hurdle as inference.
20. Track-record outcomes from reader notes were re-cited to quotes or data cells where they exist:
   - flying hours: R-0088, R-0878;
   - LTSA and Civil profit: R-0090, R-0879;
   - other outcomes: R-1281, R-0245, R-0295, R-0862, RX-0102.

   The rest are marked †: 1,044 shop visits, the £29m catch-up charge, H1 £405m, "two agencies by August 2024" and the bond repayment.

**Medium: operations.md**

21. Unknown Executive items were cited without (attr.) or (prob.) at ten places: RX-0009, RX-0023, RX-0024, RX-0025, RX-0026 (×2), RX-0284 and RX-0296 (×3). All are now flagged.
22. Watson: "Asked about the Trent 1000 and the GTF problems". The GTF is not in the evidence. The sentence now reads: his lesson is about RR's own maturity testing, and he names no rival (attr.).
23. Fairness: see "Fairness changes" (Cholerton).
24. In Watson's commitments, the 80% time-on-wing raise was cited to R-1274, the 40% target. It was re-cited to RX-0110 (February 2025). The "40% by 2025 in May 2022" version is now labelled as a reader note about another speaker.
25. Cholerton's reaction, "no launch until the market is 'real'" [RX-0002], quoted a word that is not in the quote and came from a 2016 Defence turn. It was replaced with "depending on the actual reality of any market opportunity" (attr.) [RX-0009] and labelled inference.

**Team ids (game master's note, applied during the audit)**
- `erginbilgic.md` header: `erginbilgic-kakoullis-cholerton-2023` → `erginbilgic-kakoullis-watson-2023`.
- `operations.md`:
  - Cholerton is in the 2022 team only;
  - Watson is in the 2023 and 2026 teams;
  - Cholerton's dates are now "2018 to at least May 2022" (his last item is 13 May 2022 [RX-0004]; Watson is first printed as president on 28 November 2023 [RX-0277]).

**Low (all fixed)**
- **Missing ids added:** RX-0077 for the end-2023 Trent 1000 target; R-0862 for the £150m fire cost; RX-0106, RX-0224, RX-0239, RX-0085, R-0075, R-0855 and R-0027 for figures already stated.
- **Wording brought back to the quote:**
  - McCabe: "no commitment to annual buybacks"; the UltraFan "midterm and beyond" quote; "a named drag" for "largest drag";
  - Erginbilgic: "expected to reach" the 2027 targets (not "had reached"), and the margin outcome is shown as not in the evidence;
  - Watson: the full list of six levers, and "Director, Rolls-Royce Electrical" as printed.
- **Engine figures:**
  - every [T1], [whatif] and [5p] tag now says "engine snapshot, not evidence, re-checked 2026-10-04; re-run every turn";
  - the -2.46 unselected `uf_wb` value now names its 2031 launch;
  - -4.14 is harmonised to -4.15.
- **Transcript and evidence notes:** RX-0130's transcript reading "not delivered" is noted. The SMR outcome is labelled reader-note only. Schulz's 50% share target is marked as having no 2019-20 outcome in the evidence.

## Fairness changes

- **Kakoullis, 2023 guide.** The £0.8-1.0bn guide was attributed to him alone, "overtaken once the new CEO's transformation took hold", and called "far too low". The evidence shows a different picture:
  - the CEO gave the same guide on the same call [RX-0034, RX-0202];
  - it was raised in August 2023 while Kakoullis was still CFO [RX-0047].

  The header, bias, track-record row and pattern now say this, and the causal claim was removed.
- **Erginbilgic, slips.** "Playing down or externalising slips" became a factual line: the Boeing strike explanation [RX-0107] and the "1 engine" Trent 7000 remark [RX-0088], next to his plain admission of the missed date [RX-0077].
- **Erginbilgic, customer relations.** The analyst's "less accommodating" charge was replaced with his own acknowledgement of disappointed customers and his counter-claim [RX-0133].
- **Cholerton, "durability optimism".** It became factual. "That disruption is now behind us" (May 2022) [RX-0006] now sits next to the counter-evidence:
  - aircraft on ground had reached zero [R-1239];
  - intense check-and-repair was to run to the end of the medium-term plan [RX-0282];
  - the blade was certified in June 2025 [R-1023].
- **McCabe.**
  - "She seldom acts as a counterweight" became "no evidenced turn shows her disagreeing with him (inference)".
  - The imputed choice on the £800m concessions was removed.
- **Schulz.** "Share-led optimism" became "share-led targets (the outcome is not in the evidence)".
- **Checked.** No file contains private life, health, family or appearance. No speculation about motives remains.

## Claims relabelled as inference

**Erginbilgic**
- Fast payback ranks first.
- Partnership used as leverage.
- `t1000_upgrade`, `uf_wb` and terms flip conditions. A table-level note now says that flips and vetoes are inference unless an id is given.
- Solo against Joint Venture reasoning from engine values.
- "He holds price and sells efficiency" against CFM ducted.
- "He does not launch early" against the open fan.
- An aggressive-terms request framed as a partnership test.

**McCabe**
- New-engine money redeployed, not added.
- `uf_wb` "protects the base".
- Standard terms as her engine-terms default; she holds standard terms when an airframer asks.
- The open fan as a signal.
- Hurdle → WACC and alpha proxy.
- CEO alignment.

**Kakoullis**
- Civil in "harvest mode".
- Enforcement extended to airframers.
- A higher hurdle for a 2038 payoff.
- The long-dated risk-adjusted IRR question.
- Durability as his answer to rival upgrades.

**operations.md**
- Cholerton:
  - cost-led defence carried into Civil;
  - `uf_nb` flips and `t1000_upgrade` deferral;
  - reactions to CFM/GE launches, upgrades and aggressive terms;
  - his ExCo asks.
- Watson:
  - "executes inside the CEO's frame";
  - "tolerates customer friction";
  - `uf_nb` flips, the terms veto and `t1000_upgrade` deferral;
  - the GEnx answer and the aggressive-terms reaction;
  - "asks for strain".
- Schulz meets a CFM/GE launch head on.
- The seat's veto of compressed schedules and its push for `t1000_upgrade`.

## Remaining gaps

- **Reader-note outcomes (marked †).** These still rest on the reader's summary of turns that are not quoted in the evidence:
  - McCabe: 109% flying hours, working capital £0.4bn and £280m, bond repayments, £181m;
  - Kakoullis: 1,044 shop visits, the £29m charge, H1 £405m, "two agencies";
  - Erginbilgic: the SMR stake;
  - Watson: 430 refurbishments.

  Adding those turns to `executives/evidence.jsonl` would close the gap.
- **Interpretations in reader notes.** Some reader notes go beyond their quotes:
  - R-0442: "Airbus called pricing challenging";
  - RX-0120: open fan and GTF;
  - RX-0181: the long-dated IRR;
  - RX-0176: £505m.

  The profiles no longer rely on them. The evidence file itself is unchanged.
- **No evidence:**
  - Joint Venture terms with P&W, CFM/GE moves, or a hurdle for UltraFan. All of those rows remain inference.
  - Tenure: who held the Civil seat between May 2022 and November 2023; whether McCabe and Watson still hold their seats in 2026.
  - Reconciled shop-visit definitions (Watson 1,100-1,200 against McCabe 1,400-1,500 at the same event).
- **Length.** `erginbilgic.md` is 3,142 words (`wc -w`), about 5% above the brief's 2,500-3,000. Labels and attributions added 289 words; trims recovered 145.
- **Consistency to check in `teams.md` and `README.md`** (not edited here):
  - the CEO's `uf_nb` default is now partner first (`jv_pw` when P&W announces its join), with Solo as the fallback;
  - the 2023 team id is now `erginbilgic-kakoullis-watson-2023` in the profiles.
