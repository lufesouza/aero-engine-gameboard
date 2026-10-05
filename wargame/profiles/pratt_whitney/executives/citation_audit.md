# Pratt & Whitney executives: citation audit

**Audit date:** 2026-10-04.

## Scope

Files audited and fixed:
- `wargame/profiles/pratt_whitney/executives/calio.md` (Christopher Calio, the CEO seat)
- `wargame/profiles/pratt_whitney/executives/mitchill.md` (Neil Mitchill, the CFO seat)
- `wargame/profiles/pratt_whitney/executives/operations.md` (the President seat: Bob Leduc and Shane Eddy)

Not touched: `teams.md` and `README.md` in the same folder, which another agent was writing at the same time, and both evidence files.

**Checked against:**
- `executives/evidence.jsonl` (360 own-words items, PX-0001 to PX-0360);
- the company file `evidence.jsonl` (2,072 items, P-####);
- the lever and objective definitions in `objectives.md`;
- the live engine, `five-player-2045` with all three engine makers, on a fresh run (`pw-exec-audit-scratch`, gitignored) and on the existing `pw-5p-scratch`.

No file outside `wargame/profiles/pratt_whitney*` was read, and no Boeing, Airbus, Rolls-Royce or CFM folder.

**Method.**
- `cite_check.py <file> executives/evidence.jsonl evidence.jsonl --show` was run on each file.
- Full quotes were read wherever the tool truncates them at 220 characters.
- Every load-bearing claim in the Quick card, the commitment track record and "In the game" was judged against its cited items: **SUPPORTED**, **WEAK** (partly supported, wrong scope or speaker, a mis-dated or mis-measured outcome, or an outcome taken only from an item's annotation) or **UNSUPPORTED**.
- Four checks were applied: fairness, perspective, accuracy and game use.
- Headers, "By dimension" and "What the seat stands for" were also read. Their findings are fixed and counted under severity, but not in the claim counts below.
- Engine snapshot rows are not evidence claims. They were re-run separately.

## Counts before fixes

| File | Section | Claims | Supported | Weak | Unsupported |
|---|---|---|---|---|---|
| calio.md | Quick card | 42 | 32 | 10 | 0 |
| | Commitment track record (17 rows and the fair reading) | 18 | 7 | 11 | 0 |
| | In the game | 15 | 8 | 7 | 0 |
| | **Total** | **75** | **47** | **28** | **0** |
| mitchill.md | Quick card | 38 | 34 | 4 | 0 |
| | Commitment track record (17 rows and the pattern) | 18 | 11 | 7 | 0 |
| | In the game | 14 | 10 | 4 | 0 |
| | **Total** | **70** | **55** | **15** | **0** |
| operations.md | Quick cards (Leduc 28, Eddy 18) | 46 | 40 | 6 | 0 |
| | Commitments (Leduc 11, Eddy 8) | 19 | 15 | 4 | 0 |
| | In the game (Leduc 12, Eddy 10, the seat 1) | 23 | 19 | 4 | 0 |
| | **Total** | **88** | **74** | **14** | **0** |
| **All three** | | **233** | **176** | **57** | **0** |

**Outside the counted sections:** five cited ids that did not support their claim, all fixed:
- Calio's header said the charge and the ASR were "not his decisions";
- Mitchill's header cited PX-0211 for NEM of $1.2bn;
- operations cited PX-0150 for the #3 seal and combustor problems;
- operations cited PX-0121 for the heat-treat escape;
- operations cited PX-0177 for "narrowbody first".

**Citation checks:**

| File | Before | After |
|---|---|---|
| calio.md | 237 citations, 129 distinct ids, 0 missing | 265 citations, 142 distinct ids, 0 missing |
| mitchill.md | 239 citations, 136 distinct ids, 0 missing | 249 citations, 139 distinct ids, 0 missing |
| operations.md | 199 citations, 88 distinct ids, 0 missing | 224 citations, 97 distinct ids, 0 missing |

## Findings by severity

| File | High | Medium | Low |
|---|---|---|---|
| calio.md | 0 | 13 | 17 |
| mitchill.md | 0 | 7 | 12 |
| operations.md | 1 | 7 | 16 |
| **Total** | **1** | **27** | **45** |

All high and medium findings were fixed, and so were all low findings.

Header counts were checked against the evidence and are correct:
- Calio: 110 items from 20 events, with role tags 14 / 29 / 19 / 27 / 21.
- Mitchill: 180 items from 34 events, plus 193 company-file items.
- Leduc: 49 items plus 105, from 4 events.
- Eddy: 21 items plus 20, from 1 event.

## Main fixes

**High.** Eddy's "there's not a surprise here coming" [PX-0112] was presented three times as a false assurance "weeks before a $5.4B charge": as a bias, as a commitment row and as seat item 6. The remark was about customer support for the existing 10% AOG fleet. The evidence does not show that the powder-metal issue was known in June 2023. See the fairness changes.

**Medium, perspective: RTX-wide or other people's words presented as P&W-specific.**
- **Calio, PX-0109** ("visibility into the long-term demand"). This was said of RTX investment in a defence-capacity context, but it was used as his P&W new-engine rule, as the `gtf_next` default, as an ExCo question and as a mind-changer. It is now labelled RTX-wide. The engine rule rests on PX-0009, and its extension to engines is marked inference.
- **Calio, PX-0071** ("miss a cycle"): labelled as said of RTX's businesses, with P-1304 added.
- **Calio, PX-0075** ("really, really difficult margins"). This is fixed-price defence development, but it was used as a P&W rule and as a `gtf_next` veto. It is now a labelled analogy.
- **Calio, cancel lever.** It rested on a Raytheon contract termination [P-1342][PX-0064] without saying so. It is now labelled, and the read-across is inference.
- **Mitchill, PX-0343.** This was about the Collins outlook, but it was used for "plans below airframers' ramps" and for the in-game Rate Increase stance. It is now labelled, with P&W's own capacity rule [PX-0238] added.

**Medium, re-cited.**
- Calio's "product, not price": PX-0058 and PX-0076 do not show it. It is now cited to PX-0055 (asked whether holding share needs aggressive pricing), P-0768 and PX-0058.
- Operations' era claims:
  - the #3 seal and combustor, now P-0247;
  - the heat-treat escape, now P-1022;
  - entry into service in January 2016, now P-1677;
  - the 10,000-engine backlog in 2019, now P-0080.
- Mitchill's header NEM: about $1.2bn in 2018 is Leduc's figure [PX-0159], with no further headwind from 2019 [P-1238], not PX-0211 for "2018-19".
- Seat item 5 ("narrowbody first") cited Leduc's NMA bid [PX-0177]. That citation is moved to an explicit exception.

**Medium, accuracy.**
- **Calio §3, $9B FCF.** The row said "reset to $7.5B (Jan 2024)". The CFO reset it on 11 September 2023 [PX-0295]; Calio gave the walk in January 2024.
- **Calio §3, capital return.** The row read "$36-37B → $37B". The commitment was the CFO's (February 2024) [PX-0309], and PX-0097 is an expectation ("now expect"). The outturn is now marked as outside the evidence, and the header no longer says "returned".
- **Calio §3, Airbus OE.** The row read "About 20% more Airbus OE → deliveries +14%". It is re-cited to P-0161: about 20% more large-engine deliveries, "the commitment we made to [Airbus]", against +14% on the same measure.
- **Calio §3, margin +700-800 bp.** The outcome cell quoted a same-day statement. It now gives the partial outcomes [PX-0119][PX-0337] and marks the 2025 outturn as outside the evidence.
- **Calio's date heuristic.** "Discount his dates by two quarters to a year" understated the record. The slips run from one quarter (the AOG decline) to about two years (the Advantage entry into service). The heuristic now states that range.
- **Mitchill's tempo.** "Bad news is reset within a quarter" did not fit the R&D-tax reset, made nine months after the guide was built on it. "First read is often 'timing'" rested on one instance. Both are reworded.
- **Mitchill's commitments.** Five outcome cells showed re-forecasts or estimates as outcomes: GTF breakeven, V2500 2025, OE engines 2022, GTF margins 2025 and large-engine units 2025. Each is now labelled as outside the evidence or as an estimate.
- **Leduc's "sole source or no bid".** This was a seat-wide red line, but it was said of the NMA bid, and the GTF itself competes with CFM on the A320neo. It is now scoped. The in-game veto is noted as not binding in the engine, where each airframer names one engine.
- **Eddy's tempo.** "10% AOG, recovery in Q3" ran together the AOG forecast [PX-0115] and the escape's shipment recovery [PX-0121]. The two are now separated.
- **The seat's "refuses `pw_wb`".** This conflicted with Leduc's conditional stance. Both stances are now stated.

**Medium, engine snapshots (game use).** All three files label engine values as snapshots and name the six levers (`gtf_upgrade`, `gtf_next`, terms, `join_rr_jv`, `pw_wb`, cancel). All three cover CFM/GE: ducted, RISE open fan, LEAP upgrade, and GEnx in Mitchill. Re-running them on a fresh run reproduced every value except two:
- The **CFM `leap_upgrade`** pair is -0.67 alone and +1.09 with our upgrade (also on `pw-5p-scratch`), not -0.73 / +1.03. The old pair equals the hedge cost (0.73) and the cancelled-hedge value (+1.03), which looks like a copy error. Calio and Mitchill are corrected. The upgrade's worth whatever CFM does is still +1.76.
- The **open-fan NGSA** is +0.48 if launched in 2028-2033 and +0.62 if launched in 2037. Calio said "+0.48 whatever its launch year", and Mitchill and Eddy quoted only +0.62. All three now give both values.
- All three files now note that a CFM/GE or RR engine counts only if that maker launches it in the same round; otherwise the airframer falls back to another engine.
- Calio's `pw_wb` -3.19 is the value without the upgrade; it is -1.43 with it. It is now labelled.

**Low (all fixed).**
- **Calio:**
  - Pratt-level margin quote presented as the GTF aftermarket objective (P-1354 added);
  - "six weeks" changed to about seven (25 July to 11 September 2023);
  - PX-0062 is about rate guidance;
  - PX-0007 is Pratt Canada;
  - outcomes re-cited from annotations to quotes: V2500 [PX-0340][PX-0359], 3,000 engines [P-1038], 600-700 removals [P-1035], the 4-week stoppage [P-1101];
  - 75% "of the fleet" changed to "of AOGs" [PX-0329];
  - "fee margins" ambiguity noted;
  - fair-reading re-cite (PX-0120 replaces the September item);
  - RTX-wide labels on the $10B envelope, "always paranoid", Boeing rates and fixed price;
  - "loss-making" changed to "not margin contributing";
  - castings "suppliers";
  - an uncited sentence deleted.
- **Mitchill:**
  - F135 "drop-in" labelled as an analogy;
  - aftermarket pricing labelled as inference for OE terms;
  - "often" changed to "in some cases" with partners;
  - the 2021-25 plan dated;
  - the $5B 2021 FCF outturn marked as annotation-only;
  - summits joined "on a quarterly basis, at least";
  - capex "guided";
  - RTX-wide labels on tariffs, 2024 FCF and fixed price;
  - "he kept / he gave / he eased" changed to "he reported / committed".
- **Operations:**
  - the 4.5% E&D target re-cited to Hayes [P-0312];
  - P-0162 re-dated to February 2024;
  - Hayes relayed in PX-0129;
  - Eddy's start date not claimed;
  - EC8's two figures not called one target;
  - LC8, LC10 and EC1 outcomes marked as outside the evidence.

## Fairness changes

No private life, health, family or appearance content was found in any file, and none needed removing. The changes concern one-sided misjudgements and implied motives:
- **Eddy ("not a surprise").** All three places now give the remark's context (customer support for the 10% AOG fleet [PX-0112]; fix costs in the contract base [P-0582]) and the outcome: recall disclosed five weeks later, $5.4B sales charge, about 80% customer support [PX-0290][PX-0303][PX-0300]. They add the counter-evidence: what was known in June is not in the evidence, and the cause was established only after a records review [PX-0039]. The bias is renamed "Reassurance on open exposures".
- **Calio, architecture loyalty.** It now carries counter-evidence: the contaminant entered during the powder-plant ramp [P-1040], and no gear failure in about 3,000 engines [P-1018]. The trigger is marked inference.
- **Calio, optimism on timelines.** Counter-evidence added: the H1 2025 certification date was met [PX-0078][PX-0087].
- **Calio, "value capture over goodwill".** Renamed "value capture on upgrades", with the compensation agreements as counter-evidence [PX-0049][PX-0063].
- **Calio, the charge and the ASR.** The header's exoneration ("not his decisions") and the doctrine line's attribution ("was Hayes's") went beyond the evidence. Both now state who announced the ASR [P-0602] and what Calio, as President & COO, reported [P-0611]. Who decided is marked as not in the evidence.
- **Mitchill, "confidence in estimates before the facts are in".** The April 2023 qualifier is restored ("everything that we know about the engine"). The June 2023 40-engine escape [PX-0287] is distinguished from the powder-metal recall, with its outcome not shown, and PX-0039 is added. The matching commitment row is fixed the same way.
- **Mitchill, recall cash timing.** Now notes that payments follow signed customer agreements [PX-0324].
- **Leduc, "losses attributed to the rival's price".** This implied a self-serving explanation without evidence. It is now his account of IndiGo, which the evidence neither confirms nor refutes.
- **Leduc, time on wing (LC2) and durability optimism.** Counter-evidence added: the cooler-environment three-quarters of the fleet was "better than where we were on V2500 at this stage" [PX-0122].
- **Leduc, fixes by end-2017 (LC4).** Counter-evidence added: production engines carried "the 2 big fixes" by January 2018 [P-0881].
- **Leduc's record.** "Volume met once buffered" is now "missed in 2016, met from 2017".
- **Leduc on the RR Joint Venture.** The scepticism inference from RR's V2500 compressor is replaced by both sides of the IAE history [PX-0150][PX-0143].

## Claims relabelled as inference

- **Calio:**
  - P&W-level decision rights;
  - the RTX demand-visibility test applied to engines (Quick card, `gtf_next` default, ExCo, mind-changer);
  - the defence "difficult margins" rule as an engine veto;
  - the architecture-loyalty trigger;
  - "balance sheet before buybacks" as his own departure;
  - discounting his operating dates;
  - the veto on deferring `gtf_upgrade` to turn 3;
  - extending the MTU/JAEC partnership view to Rolls-Royce;
  - the `gtf_next` and Joint Venture same-airframer veto (company doctrine);
  - the cancel read-across from Raytheon;
  - reading RISE through durability;
  - "committed demand" and "a rival's discount" as mind-changers.
- **Mitchill:**
  - the Rate Increase discount stance;
  - OE terms taken from aftermarket and spare-engine pricing;
  - the upgrade-and-hold-price answer to a LEAP upgrade;
  - refusing aggressive terms;
  - `pw_wb` "never";
  - cancelling from project re-ranking;
  - the F135 "drop-in" upgrade as an analogy for `gtf_upgrade`.
- **Operations:**
  - that the doctrine's rules originate with Leduc;
  - Leduc's `join_rr_jv` OFF and his sole-source `gtf_next` offer against CFM ducted;
  - Eddy's derivatives-over-clean-sheets for large engines;
  - Eddy's OE terms and pass-through pricing taken from aftermarket pricing;
  - the link from the golden rules to the Advantage's testing.

## Remaining gaps

- **Outcomes outside the evidence.** The latest own-words item is October 2025, and the latest press item November 2025. Outside it:
  - 2025 full-year FCF, GTF aftermarket margin, Pratt margin and large-engine growth;
  - the $37B capital return;
  - the 2026 durability kit and the Advantage's entry into service;
  - Eddy's 90% fleet configuration;
  - the Indian fleet's return in April 2018;
  - 2019-20 GTF deliveries;
  - GTF stand-alone breakeven.
- **Annotation-only facts.**
  - The $5B 2021 FCF outturn [PX-0194] has no quote.
  - PX-0053's "fee margins" is probably a transcription of "teen margins", but that cannot be confirmed.
- **No executive evidence** on an UltraFan Joint Venture, the RISE open fan, a new widebody engine (beyond Leduc's NMA bid), cancelling an engine programme, or a hurdle rate. Every stance on these is inference.
- **Eddy:** one event, before the recall; his tenure after June 2023 is not in the evidence, though the `calio-mitchill-eddy-2026` team assumes it.
- **Unverified header shares:** Calio's "about 87" engine items and Mitchill's "about two-thirds" on Pratt. The evidence schema tags dimension, not business.
- **Evidence annotations with errors.** These were left alone; editing the evidence files was out of scope.
  - PX-0025's finding dates the $7.5B reset to January 2024 (it was September 2023 [PX-0295]).
  - PX-0030 says "six weeks" (48 days).
  - PX-0048 says "Airbus OE" where the quote [P-0161] is large-engine deliveries.
  - P-0582's finding treats Eddy's remark as a failed assurance without context.
- **`teams.md` line 382** (not touched) says the LEAP figures in `calio.md` and `mitchill.md` differ (-0.73 / +1.03). After this audit they match `teams.md` (-0.67 / +1.09), so that sentence is now out of date.
- **Engine values** are snapshots of the current rules on turn 1 with no injects. Re-run them each turn.
