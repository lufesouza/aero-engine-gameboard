# Rolls-Royce: behavioural profile (supplier `rolls_royce`)

**Tags.** **[own]** RR executives, RR filings, or RR's own view of others · **[record]** reported numbers (MS model actuals, Capital IQ actuals) · **[analyst]** Morgan Stanley estimates, analyst questions · **[market]** Capital IQ consensus and multiples · **[press/industry]** industry reports · **[customer]** Boeing or Airbus · **[rival: P&W]** Pratt & Whitney's or RTX's words and 10-K as held in our evidence · **(inference)** our reading · **(view)** a forecast, not the record.

**Perspective → tag:** `own_words` (RR) and `observed_by_rolls_royce` → [own]; `own_behaviour` → [record]; `analyst_view`, `analyst_question` → [analyst]; `market_view` → [market]; `industry_report`, `press` → [press/industry]; `observed_by_boeing`/`_airbus` → [customer]; `filing`, `observed_by_pratt_whitney`, RTX `own_words` → [rival: P&W].

**Money.** RR figures in £. P&W figures in $. Game numbers in $B (constant 2026 $, PV to 2026 at our WACC); the calibration converts at MS's 1.36 $/£ [analyst] [R-1672]. **Eras** (by the CEO speaking on calls): Rose (to 2011) [R-1313], Rishton (2011-mid-2015) [R-0310, R-1083], East (mid-2015-22) [R-0942], Erginbilgic (2023-) [R-1561].

**[T1]** = `options --side rolls_royce`, base-case calib run, turn 1; **[whatif]** = `whatif` on that run. Snapshots: re-run every turn.

---

## Quick card

**Timing (rules).** Orders are sealed and simultaneous; disclosures reach us a turn later. An airframer selecting UltraFan in turn t falls back to CFM/GE unless we launched by the end of turn t. So we answer only an **announcement**: a disclosure or statement from an earlier turn naming the programme and this turn (§9 step 4). Turn 1 has none.

**Ranked objectives (stated 2023-25, consistent with behaviour)**
1. Quality of profit and cash, ahead of share: "not after market share" [own] [R-1582, R-1561].
2. Repair and keep the balance sheet from operating cash, not equity: investment grade, net cash [own] [R-0865, R-0874, R-0888]; all 2023-24 FCF to net debt, net cash by 2024 [record] [R-0062, R-0032].
3. Defend and harvest the widebody installed base: A350 and A330neo sole source [own] [R-0360, R-0319]; Trent 1000 share regained through durability [own] [R-1601, R-1015].
4. Regular, growing distributions: 30-40% payout plus buybacks [own] [R-0909]; DPS and buyback restored [record] [R-0075, R-0071].
5. UltraFan as an option, launched only on an airframe [own] [R-0994, R-1005].
6. Narrowbody re-entry last, preferably with a partner [own] [R-1011, R-1010].

**Hard rules and red lines**
- No UltraFan launch without an announcement of a programme that can fly it [own] [R-0994, R-1005]; so none in turn 1 (inference).
- Never compress maturity; never disclose an entry into service earlier than launch + `dev_years` [own] [R-1476, R-0970].
- `standard` terms by default; `aggressive` on the A350 Re-engine only if P&W's `pw_wb` beats our standard terms in `whatif` (inference; no "silly pricing" as sole source [own] [R-0334]).
- `jv_pw` only if P&W announced `join_rr_jv` for this turn; otherwise nothing launches and the airframe falls back to CFM (rules).
- No overlapping `uf_wb` and `uf_nb` Solo developments unless both are selected: strain $1.9B, $1.4B, $1.1B launched together in turns 1, 2, 3, and $0.74B for 2029 then 2032 [whatif]; we ration engineering [own] [R-0929, R-1127].
- No `t1000_upgrade` while an UltraFan is in development: its 3-year window draws strain too ($1.31B in turn 1, $0.99B in turn 2) [whatif].
- `cancel` only a programme no live airframe flies (rules).

**Default plan**
- **Turn 1 (2026-28):** `t1000_upgrade` (+$0.81B [T1]); no UltraFan; disclose conditional commitments (§9); predict no airframer launch (each pays its airframer more in 2029 [whatif]).
- **Turn 2 (2029-31):** (inference) the likely NGSA window: entry into service targeted for the second half of the 2030s [customer] [R-1867], about 7 years after launch. Launch only against turn-1 announcements.
- **Turn 3 (2032-34):** launch only against an announcement (NGSA on UltraFan 2032 still +$15.1B [whatif]); cancel unselected programmes.
- **Turn 4 (2035-37):** defend the A350; `uf_nb` only against an announcement (NGSA 2035 +$10.4B [whatif]); else Do Nothing.

**Top reaction triggers (§5):** A350 Re-engine announced → `uf_wb`, standard · fps/NGSA announced → `uf_nb` (Solo if UltraFan announced; Joint Venture only if P&W announced its join and the gap is ≤ $3B) · `rr_durability_crisis` → upgrade unless an UltraFan is in development, hold price · `ultrafan_test_setback` → keep selected, cancel unselected · demand shock → defer.

**Biases to display (§8):** durability optimism; maturity over timing; narrowbody oscillation; price discipline over share-buying; caution after shocks.

**Naming.** Do Nothing, Re-engine, Joint Venture, Delay Tactics; fps, NGSA, A350 Re-engine, 787 Re-engine; UltraFan, Trent XWB, Trent 1000, Trent 7000, GTF, GTF Advantage, V2500, IAE.

---

## 1. Who we are and what winning means

**Revealed objectives today.**
- **Margin and cash.** Civil margin 2.5% (2022) → 16.6% (2024) [record] [R-0295] → mid-20s (1H25) [own] [R-0906]; FCF £1,285m → £3,270m (2023-25) [record] [R-0068, R-0220]. Spare-part prices up about 12% in 2023 and 2024 [own] [R-0880, R-0884], record orders anyway [own] [R-0885]; nothing "silly... on pricing" for 787 share [own] [R-0998].
- **Balance sheet.** "Our first priority is to get to investment grade" (2023) [own] [R-0865]. Net debt of £5,157m (2021, 3.7x EBITDA) became net cash of £475m (2024) [record] [R-0027] and £1,972m (2025) [record] [R-0032]; RR prefers net cash to the 1-1.5x it tolerates [own] [R-0888, R-0902].
- **Installed base.** Over half of widebody deliveries; fleet growing about twice the market [own] [R-0369, R-0368]; sole engine on the A350 and A330neo [customer] [R-1862, R-1860].
- **Distributions.** DPS 6p (2024), 9.5p (2025) [record] [R-0075]; £380m buyback in 1H25, the first since 2015 [record] [R-0071].

**Said against did, by era**

| Era | What it said | What it did | ids |
|---|---|---|---|
| 2000-09 | Financial strength; self-funded growth [own] | Net debt £690m (2000) → net funds £1,458m (2008); DPS held at 8.18p through 2001-04 [record] | R-0457, R-0002, R-0034 |
| 2010-14 | A- to A+ rating; IRR above a ~9% WACC [own] | Capex + intangibles £599m → £1,144m (2013); payouts above FCF in 2014-15; skipped the A320neo on returns [record] [own] | R-0509, R-1353, R-0043, R-0040, R-0310 |
| 2015-19 | Dividend "essential" (July 2015); A rating a priority [own] | Dividend halved seven months later; R&D cash raised to £1,110m (7.2%); Civil EBIT -£343m (2017); Trent 1000 £2.4bn [own] [record] | R-0555, R-0597, R-0174, R-0294, R-0760 |
| 2020-22 | Investment grade "not as important"; don't spend at the bottom [own] | FCF -£4,185m; £1,972m rights issue (shares 1,931m → 8,368m); capex + intangibles -63%; no dividend 2020-23 [record] | R-1513, R-0839, R-0054, R-0049, R-0060, R-0059 |
| 2023-26 | Profit over share; mid-to-high-teens hurdles [own] | Guidance beaten each year; capex below consensus in each year shown (2021-22, 2024-25); dividend then buyback [record] [market] | R-1561, R-1579, R-0219, R-1723, R-0070 |

**Pattern.** RR says "balance sheet first" every era [own] [R-0509, R-0670, R-0865] but acts on it only after shocks; at cycle tops it over-paid or over-built [record] [R-0040, R-0043]. It admits it "was a market share business" placing engines "at any cost" [own] [R-1554, R-1555], with "too many options open" [own] [R-1560]. **(inference)** Today's team chases share only for a large payoff above the hurdle.

---

## 2. Financial behaviour

**Capital-allocation hierarchy.**
- **Stated (2025):** balance sheet, then growing dividends, then disciplined investment and extra distributions [own] [R-0900]; leverage only "for the right opportunity", never for buybacks [own] [R-0902].
- **Revealed order of cuts:** (1) buybacks, stopped at £500m of £1bn in 2015 [own] [R-0547]; (2) the dividend, halved 2016, cancelled 2020 [own] [R-0597, R-0779]; (3) new-programme spend and Civil capex, deepest: £1,274m → £323m (2019-21) [record] [R-0053], new civil engines first [own] [R-0986]; (4) technology, least: R&D cash -27% [record] [R-0181]; (5) never liquidity: £1-2bn headroom [own] [R-0788], about £2bn net cash "to keep R&D going" [own] [R-1522].
- **Hurdle:** IRR above a ~9% WACC (2014) [own] [R-1353] → 15% cash return, group WACC 10% + 5pp (2018) [own] [R-1459] → mid-to-high teens with CEO and CFO sign-off above £25m (2023-24) [own] [R-1579, R-1591]. Civil's cost of capital is 12.5% [own] [R-1464].
- **Templates:** a new engine is about £1bn of R&D plus £0.5bn of capex, in service about 7 years after launch [own] [R-0931]; a 2,000-engine programme is £1.5-2bn of R&D and capex, about £3.2bn of OE losses and £10bn of aftermarket cash margin over 25 years [own] [R-1461].
- **Engineers, not money, ration programmes:** a constant engineering pool [own] [R-1318]; three of four engines chosen [own] [R-0929]; £1bn of Energy proceeds returned for lack of engineers [own] [R-0511].
- **Others share the bill:** partners take about 30% of LTSA receipts [own] [R-0861]; governments funded about £400m of £1.4bn gross R&D [own] [R-0678].

**R&D and capex through the cycle** (table: financials.md §4). Company-funded R&D cash £371m (6.3%, 2000) → £1,110m (7.2%, 2019) → £775m (4.3%, 2024); PP&E + intangibles £251m (2000) → £1,529m (2018 peak) → £493m (2021) → £876m (2024) [record] [R-0165, R-0035, R-0174, R-0043, R-0060, R-0181]; MS holds R&D at 3.5% of revenue to 2030, no launch step-up (view) [analyst] [R-1679].

**Crisis behaviour**

| Crisis | Cut | Raised / sold | Who paid | ids |
|---|---|---|---|---|
| 2014-16 profit warnings | Buyback halted; dividend halved; R&D and new-product capex protected [own] | ~£1bn debt; RCF to £2bn [own] | Shareholders | R-0547, R-0597, R-0570, R-0575, R-0611 |
| 2017-19 Trent 1000 | "Nice-to-have" projects; 2019 R&D -£100m, capex -£75m [own] | Spares at £4-5m each; disposals [own] [press/industry] | Customers compensated; RR's LTSA margin ~20% → high single digits [own] | R-0682, R-0749, R-0777, R-1788, R-0725, R-0765 |
| 2020-21 COVID | Dividend in ~2 months; 9,000 roles; Civil capex -75%; R&D -27% [own] [record] | £5bn package incl. £2bn rights issue; ~£2bn disposals [own] | Shareholders (4.3x dilution); Civil staff; Defence protected | R-0779, R-0814, R-0053, R-0181, R-0793, R-0825, R-0049, R-0288 |

**Crisis rules (inference from the table):** payouts before investment; programme spend deferred before the technology base; debt before equity, equity only when debt is exhausted [own] [R-1516]; customers compensated to keep fleets flying; Defence and Power Systems are the floor (£649m of EBIT against a Civil loss of £2,535m in 2020) [record] [R-0288]; net cash returns about 3 years after the trough [record] [R-0030].

**Guidance behaviour.**
- 2014-15: optimistic and cut late; FY14 FCF £254m against £350m guided 119 days earlier [record] [R-0208, R-0210].
- 2016-25: guide low, beat. EBIT beat the top of guidance in 2023-25 (£1,590m, £2,464m, £3,462m) [record] [R-0219], FCF too [record] [R-0220]; 2027 targets met two years early [own] [R-0893]; beats against consensus are shrinking (EBIT +15%, +8%, +6%) [market] [R-1758].
- Crisis costs only rise: Trent 1000 £350m → £450m for 2018 [own] [R-0697], then £1.5bn (Feb 2019) and £2.4bn (Nov 2019) [own] [R-0724, R-0760].
- Capex is a ceiling: below final consensus in 2021, 2022, 2024 and 2025 (2023 not in evidence) [market] [R-1723].
- Current targets: FY26 EBIT £4.0-4.2bn, FCF £3.6-3.8bn; FY28 EBIT £4.9-5.2bn, FCF £5.0-5.3bn [record] [R-0222].

**Funding capacity for a new engine today.**
- FY25 FCF £3,270m [record] [R-0220]; net cash £1,972m [record] [R-0032]; MS net cash £12.5bn (2028e), £22.2bn (2030e) with no launch (view) [analyst] [R-1608]; consensus only £5,503m (2028), implying buybacks (inference) [market] [R-1721, R-1722]; consensus FY30 capex cut from £2.1bn to £926m [market] [R-1730].
- Game capex at 1.36 $/£ (inference): `uf_wb` $3.1B ≈ £2.3bn over 6 years; `uf_nb` Solo $7.5B ≈ £5.5bn over 7 years (≈ 21% of FY26 FCF guidance a year); `jv_pw` half.
- **What binds is not cash** (inference): the hurdle (alpha 0.6 [own] [R-1459, R-1579]), no platform [own] [R-0994], "we don't need to" [own] [R-1011], engineers [own] [R-0929], payouts [own] [R-0909]. RR could absorb a flying-hour shock almost twice 2019's and break even on cash [own] [R-0898].

---

## 3. Operational behaviour

**Deliveries and ramp.**
- Large-engine deliveries: 181 (2000), 308 (2015), 510 (2019 peak), 190 (2022), 278 (2024) [record] [R-0226, R-0245]; MS 312 (2026e), 387 (2030e) (view) [analyst] [R-1686].
- Capacity comes early: Singapore built about 40 engines a year against 250-300 of capacity during 787 delays [own] [R-1083]; delivery before inventory [own] [R-1107]; output follows airframer rates [own] [R-0418].
- The steepest ramp missed: about 550 guided for 2018, 480 delivered [own] [R-1153, R-1182, R-1183]; three parallel programmes were "unprecedented" [own] [R-1127]; RR shared in the A330neo and A350-1000 delays [own] [R-1156].

**OE economics per engine.**
- Model: $10m list, 60% concession, $4m net against $5m cost, recovered through TotalCare [own] [R-0934], sold with over 99% of new engines [own] [R-1451].
- On-wing loss per widebody engine: -£1.6m (2017), -£1.2m (2019), -£1.0m (2024), -£0.85m (1H25) [record] [R-0132]; MS -£0.5m from 2026 (view) [analyst] [R-1653]. On-wing margin -44.4% (2017) → -14.7% (1H25) [record] [R-0133].
- Launch pricing is steepest on new engines [own] [R-1463] and rolls off after 2-3 years of deliveries [own] [R-0646]; 70% of the XWB-84 loss cut was price [own] [R-1468].
- Breakeven drifts: XWB-84 planned about 6 years after entry into service [own] [R-0770]; today only XWB installed deliveries reach breakeven, by 2028 [own] [R-0895, R-0904]; Trent 1000 and Trent 7000 stay below [own] [R-0901].
- Spares carry OE profit: £616m in 2024 at about 60% margin [record] [R-0121, R-0122].

**Aftermarket.**
- 2024: aftermarket gross profit £2,206m against OE £443m [record] [R-0119]. Hours 15.3m (2019), 6.6m (2020), 15.8m (2024) [record] [R-0088, R-0097]. Blended LTSA rate $300/EFH (2019) → $396 (2024) [record] [R-0084, R-0098]. MS's underlying aftermarket gross margin: 32.9% (2019), 40.1% (2024), 53.2% (2030e, view) [analyst] [R-1622, R-1637].
- RR captures about 90% of lifetime services value [own] [R-1549], plans on a 25-year life [own] [R-1371], and catches up profit at the second shop visit [own] [R-1419].
- After COVID it repriced: focus on the six most onerous customers, over half of the £1.4bn onerous-contract provision (2023) [own] [R-0433, R-0432]; all significant onerous airline contracts renegotiated by mid-2025 [own] [R-0448]; first renewals reprice [own] [R-0423]. Temporary rate cuts only to keep RR-powered aircraft flying [own] [R-0359].

**Durability record.**
- **Trent 1000 (2016-25):** entry into service 2011 [own] [R-0465]; 380-500 engines affected, issues from 2016-17 [own] [R-1160, R-1145, R-1177]; just under 50 aircraft on ground at peak (2018) [own] [R-1171]; zero by early 2021 [own] [R-1239]; HPT blade certified June 2025, BoM C by end-2025 [own] [R-1023, R-1306]. Just over half of the then £1.5bn cash-cost estimate (Feb 2019) was customer disruption [own] [R-0725, R-0724], paid mostly as credit notes [own] [R-1238]; the total later rose to £2.4bn over 2017-23 [own] [R-0760]. LTSA margin ~20% → high single digits; 3 of 20 contracts loss-making; one extra shop visit per life [own] [R-0765, R-0758, R-0757]. 787 share 50% (2012), 45% (2016), 14% (2021), 27% (2024) [record] [R-0135].
- **Optimism ladder:** "fully scoped" (2018) [own] [R-1178], "solved" (Feb 2019) [own] [R-1186]; then the blade failed testing (Nov 2019) [own] [R-1210] and certification slipped to 2021 [own] [R-1251].
- **Smaller issues:** about £100m a year of cash contingency for engine issues [own] [R-0675]; the Trent 1000 was "unprecedented" [own] [R-1220] ("four issues of ~£200m are normal" is a reader's paraphrase, inference). XWB-84 blade wear (2020) [own] [R-1224]; XWB-97 harsh-environment fix to 2027 [own] [R-1305].
- **How RR fixes:** capacity, spares, credit notes, retrofit at natural overhauls, not recall [own] [R-1212, R-0777]; £1bn of time-on-wing spend over four years [own] [R-1601].
- **GTF:** we hold only P&W's early gearbox problems [own] [R-1944] (§10).

**Slip and ramp priors for our new engines (inference unless tagged).**
1. Development: about 7 years launch to entry into service [own] [R-0931]; 6-7 on UltraFan architecture [own] [R-0965]. Live: `uf_wb` 6, `uf_nb` 7, `jv_pw` 6 (rules).
2. Base slip risk +1 year: TEN about 1.5 years [own] [R-0921, R-1146]; Trent 7000 about 1 year (inference: readied for 2017, first 8 deliveries 2018) [own] [R-1132] [record] [R-0254]. UltraFan was "preparing the 2025 deliveries" (2016), then "well into the 2030s" (2022) [own] [R-0955, R-1000]: `ultrafan_test_setback` (+2 years) is a live tail.
3. Value ramp: live `ramp.start_frac` 0.45 rising to 1 over `ramp.years` 6 (rules), consistent with launch pricing rolling off [own] [R-0646] and the XWB breakeven plan [own] [R-0770]. Downside about 8 years (inference, memo range 5-8): XWB breakeven slipped to 2028 [own] [R-0904]; catch-up at the second shop visit [own] [R-1419].
4. Durability unproven for 4-6 years: no claim before 20-30 engines reach a first shop visit [own] [R-1169]; recent engines each had a blade or hot-section issue 2-6 years in [own] [R-1177, R-1189, R-1224].
5. (inference) Assume a crisis ends about 1.6x its first full estimate (£1.5bn → £2.4bn) [own] [R-0724, R-0760]; the 2018 figure alone rose 1.3x [own] [R-0697].

---

## 4. Engine-programme doctrine

**Rules.**
1. **No airframe, no engine.** Demonstrate first; whether to "go ahead" or "pause" depends "on the timing of new aircraft programs" [own] [R-0994]; "we need airframers, obviously, to go there first" [own] [R-1005].
2. **Sole source.** RR calls exclusive positions positive [own] [R-1393]; P&W heard RR wanted only a sole-source NMA slot [rival: P&W] [R-1876]. Boeing wants one engine on a narrowbody [customer] [R-1830], so fps and NGSA are all or nothing.
3. **Maturity before the airframer's date.** RR left NMA as "simply too aggressive" for UltraFan [own] [R-1934, R-0980]; it withdraws early rather than miss by a year [own] [R-0970]. Airframers demand demonstrated technology [own] [R-0383].
4. **Hurdle:** mid-to-high teens [own] [R-1579].
5. **Widebody is the franchise; narrowbody optional** [own] [R-1574, R-1011].

**Launch history.**
- 2006-13: three widebody engines, no A320neo "from a simple financial basis" [own] [R-0929, R-0310].
- 2013: "very competitive" 777X bid; GE won sole source [own] [R-0317] [customer] [R-1831].
- 2014: Trent 7000 exclusive on the A330neo at launch, 127 commitments, £200-300m of derivative R&D [own] [R-0319, R-0937].
- 2018: NMA pursued, costed £1-2bn over 5-7 years [own] [R-0960, R-0965], then dropped [own] [R-0968].
- 2021: A350-900 exclusivity extended to 2030 against GE, timed to UltraFan [own] [R-0360, R-0361, R-0990].
- 2024-25: self-funded narrowbody demonstrator, about 2 years from build [own] [R-1017, R-1024].

**Technology gates.** UltraFan core at full power 2018-19 [own] [R-0979]; demonstrator at full power with a 64 MW gearbox in 2023 [own] [R-1013, R-1007]; +10% on the Trent XWB; scalable 25,000-110,000 lbf [own] [R-0974, R-1007]. RR admits the Trent 1000 chased performance past durability limits [own] [R-1436].

**Segments.**
- Widebody: from under 10% to over 50% of widebody engines on order took 30 years [own] [R-1387, R-1392].
- Narrowbody: "unfinished business", then "we don't have to be in narrow-body" seven months later (2015) [own] [R-0942, R-0952]; "if it is not profitable, we won't do it" (2023) [own] [R-1011]; "probably" the only entrant into a CFM-P&W duopoly [own] [R-1310]. The V2500 flight-hour payment ends June 2027 [rival: P&W 10-K] [R-1891].
- Won't: "custom engines for every airplane" (A380neo only with a business case) [own] [R-1396, R-0943]; programmes whose funder walks away (F136) [own] [R-0309].

**Partnerships.**
- Risk-and-revenue sharing is the default [own] [R-1394]; UltraFan with "the usual suspects" [own] [R-0973]; gearbox 50:50 with Liebherr [press/industry] [R-1821].
- Narrowbody partner preferred, financially "to derisk things"; "we don't need partnership for capability", and "if it doesn't work, we can consider alternatives" [own] [R-1010, R-1022]; talking to "almost all the parties", none named [own] [R-1025].
- IAE: RR exited because partners on old and new engines were no longer aligned [own] [R-0318]; it sold the 32.5% stake for $1.5bn plus flight-hour payments [press/industry] [R-1826]; the 2012 P&W midsize Joint Venture was announced [own] [R-0916], but P&W formed IAE LLC without RR [rival: P&W 10-K] [R-1892]. P&W keeps 59-61% of its narrowbody collaborations [rival: P&W 10-K] [R-1893]; its one named 50:50 venture is the Engine Alliance with GE (widebody), and partners otherwise take 14-50% [rival: P&W 10-K] [R-1894]. P&W still recalls RR's compressor halting V2500 deliveries [rival: P&W] [R-1875]. Joint Ventures must beat WACC within 3 years [own] [R-1356]; "pain and grief" of Tognum [own] [R-1377].

**Pricing: OE against aftermarket.**
- 2004-17: buy share. Deeper launch discounts [own] [R-0484]; capitalised concessions (CARs) £21m (2004) → £286m (2017), book value £873m [record] [R-0113]; Trent 700 cut to cash-loss prices for the A330ceo run-out, a £250m hit [own] [R-0343, R-0588].
- 2019: meets aggression only within "commercial common sense", priced on a portfolio basis [own] [R-1493, R-1494]; Trent 7000 aftermarket concessions against Boeing's 787 pricing [own] [R-0753, R-1935].
- 2023-: Investment Committee reviews every contract [own] [R-1571]; RR denies price loses campaigns [own] [R-0367]; as sole source, no reason for "silly pricing" [own] [R-0334].

**Waits on:** no airframe; a timeline shorter than maturity; sub-hurdle returns; loaded engineering; a cash crisis; an in-service problem [own] [R-0994, R-0968, R-0310, R-0929, R-0986, R-1601]. **Moves on:** an airframer launch it can serve, or a threat to a sole-source franchise [own] [R-0361].

---

## 5. Reaction function

Rules (live): supplier orders apply first; an unlaunched UltraFan falls back to `cfm_ducted` / `ge_genx_next`; new airframes are sole source; defaults: A350 Re-engine `rr_ultrafan_wb`, 787 Re-engine `ge_genx_next`, fps and NGSA `cfm_ducted`. "Announced" = disclosed or stated in an earlier turn for this turn.

| # | If … | We historically… | Typical lag | Strength | Analogues | War-game orders | Evidence ids |
|---|---|---|---|---|---|---|---|
| 1 | Airframer launches a new narrowbody with an engine competition (fps, NGSA) | Skip unless returns clear the hurdle and capacity allows; a partner preferred for risk, Solo kept as an option; "we don't need to" [own] | At the airframer launch; ~7 years to entry into service [own] | Strong for "no launch without a programme"; moderate for launching (untested since 2011) | A320neo 2011 skipped; NMA 2019 withdrew | `uf_nb` only for an announced fps/NGSA: Solo if UltraFan announced (P 0.6); engine open (P 0.35): NGSA `jv_pw` if P&W announced its join, else Solo; fps fails the $2B bar. [T1] Solo -9.18 / +19.78 fps / +29.74 NGSA; `jv_pw` -4.79 / +9.69 / +14.67 | R-0310, R-0929, R-0952, R-1009, R-1010, R-1011, R-1017, R-1022, R-1024, R-0994, R-0931 |
| 2 | Airbus launches an A350 Re-engine or courts a rival engine | Commit at once with a derivative; lock exclusivity [own] | The announced turn; ~12 months for exclusivity | Strong for exclusivity; moderate for a new-engine launch (inference: derivative and contract precedents applied to a $3.1B new architecture) | A330neo 2014; A350 2020-21 | `uf_wb`, standard, in the announced turn; unannounced, it falls back to GE (row 4). [whatif] 2029: -2.75 with `uf_wb`, -5.11 without; pre-launched 2026: -3.69 | R-0319, R-0937, R-0360, R-0361, R-0990, R-0991 |
| 3 | Boeing launches a 787 Re-engine | Bid hard, often lose to GE [own] [customer] | Within the campaign | Moderate bid, weak win | 777X 2013 | Not `uf_wb` for `re787` alone unless P(UltraFan) > 0.42 (inference). [T1] +2.01 selected, -7.38 GE, Do Nothing -3.41. Boeing's own PV favours UltraFan (§6): check `whatif` | R-0317, R-1831, R-1946 |
| 4 | Rival engine selected, or UltraFan selected unannounced (falls back) | Accept, do not chase on price, support the fleet [own] | Immediate | Strong | ANA 2020; Air NZ 2019 | No retroactive `aggressive`; `cancel` an unselected programme (by analogy: F136, funder walked away; NMA, own withdrawal [own] [R-0309, R-0980]) | R-0356, R-1946, R-0367 |
| 5 | Airframer asks for price concessions | 2004-21 concede (CARs to £286m; "commercial common sense" limits, 2019); 2022- hold price [record] [own] | Within the campaign | Strong (standard today) | A330ceo 2015; Trent 7000 2019 | `standard`; `aggressive` (+1.2pp, value_mult 0.86) only per §6 | R-0484, R-0113, R-0588, R-1935, R-1555, R-1582, R-1571, R-1493 |
| 6 | Rival stumbles or wins (`gtf_durability_crisis`, `gtf_next_test_setback`) | Stay quiet and learn [own]; P&W's GTF core displaced RR at Gulfstream [rival: P&W]; an industry report reads RR's Pearl as the answer [press/industry] (inference: RR answers wins with product) | 1-4 years (inference) | Moderate | GTF 2017; Gulfstream/Pearl | No lever change; re-run `options` and the rival comparison (§6). If CFM wins fps, NGSA is the last narrowbody prize (inference) | R-1944, R-1945, R-1881, R-1791 |
| 7 | Own durability crisis (`rr_durability_crisis`) | Fix, fund spares, compensate; rebuild share without price cuts [own] | (inference) ~4 years to zero aircraft on ground, ~8 to the final blade; share slower | Strong | Trent 1000 2016-25 | `t1000_upgrade` if unfunded and no UltraFan in development; standard; defer launches unless announced | R-0760, R-0725, R-1238, R-0777, R-0765, R-0135, R-1601, R-0998, R-1177, R-1239, R-1023 |
| 8 | Demand shock (COVID; `nb_demand_shock`) | Cut payouts and new-programme spend within months; protect liquidity [own] [record] | 2-3 months to cut; ~3 years to net cash | Strong | COVID; 2014-16 | Postpone `uf_nb` a turn unless announced. `wb_demand_boom`: Do Nothing (inference) | R-0779, R-0986, R-0060, R-0181, R-0793, R-1513, R-0030 |
| 9 | Airframer quality or rate problems (`boeing_quality_escape`, `certification_scrutiny`) | Follow the airframer; "at the mercy of Boeing's production plans" [own] | Same quarter | Strong (passive) | 787 grounding 2013; Boeing strike 2024 | No order change | R-0315, R-0421, R-0422, R-0446, R-0418 |
| 10 | Technology slips (`ultrafan_test_setback`, `engine_maturity_slip`) | Protect maturity even at the cost of a slot [own] | ~2 years per slip (TEN blade, Nov 2019 to Aug 2021 still uncertified); withdrawal within months of judging a timeline too tight (NMA) | Strong | NMA 2019; TEN fix 2019-21 | Setback (our launched engines +2 years): keep programmes an airframe flies (10% of capex a year); cancel the rest; no new launch unless one is announced for this turn, then launch (slots are one-shot). `engine_maturity_slip` (airframers' technology 2 years later): no change; expect launches a turn later (inference) | R-0955, R-1000, R-1013, R-1934, R-1476, R-0994, R-1210, R-1251, R-0980 |
| 11 | Supply-chain crunch (`supply_chain_crunch`) | Output broadly flat under casting and forging limits; spares built; programmes rationed [own] | Ongoing | Moderate-strong | 2022-26 | No overlapping `uf_wb` / `uf_nb` Solo developments (6-7 years each, so different launch turns can overlap) and no upgrade during either; sequence or `jv_pw` (`strain_relief` 0.5). Strain +50% | R-1299, R-0862, R-1302, R-0929, R-1127 |
| 12 | Partner proposes a Joint Venture (P&W `join_rr_jv`) | Partnership preferred, no partner named; friction: IAE exit on misalignment, IAE LLC without RR, P&W keeps 59-61% [own] [rival: P&W 10-K] | Years | Moderate | IAE; Liebherr 50:50 | `jv_pw` only in a turn for which P&W announced its join; halves capex ($7.5B → $3.75B) and value; in practice only at P 0.35 on NGSA (§6) | R-1010, R-1022, R-1025, R-0916, R-0318, R-1892, R-1893, R-1875, R-1821 |
| 13 | P&W launches or announces `pw_wb` | Defend exclusivity, as against GE in 2020 [own] | Same turn as an announced A350 Re-engine | Moderate (inference: no P&W widebody precedent) | A350 2020-21 | Compare Airbus's PV on `pw_wb_new` and UltraFan (§6). If P&W wins at our standard terms, `aggressive` `uf_wb` is allowed while our selected PV beats the P&W-selected case | R-0361, R-0360, R-0991, R-1880 |
| 14 | `fuel_price_spike`, `trade_dispute`, `quiet_turn` | "We sell fuel burn" [own] | - | Weak (inference) | - | No change by itself; re-run `options`. A fuel spike (+1.5pp for new products) raises launch odds; a trade dispute (-1pp, 5 years) lowers them | R-0955 |

---

## 6. Lever-by-lever playbook

**[T1] stage game** ($B, full-game delta PV; columns are an airframer launching in 2026 with that engine; * = falls back because we did not launch):

| Our order | Nobody | A350 RE UltraFan | A350 RE GE | 787 RE UltraFan | 787 RE GE | fps UltraFan | NGSA UltraFan | Airframer incentive |
|---|---|---|---|---|---|---|---|---|
| Do Nothing | 0.00 | -6.95* | -6.95 | -3.41* | -3.41 | 0.00* | 0.00* | - |
| `t1000_upgrade` | +0.81 | -6.26* | -6.26 | -3.55* | -3.55 | +0.81* | +0.81* | - |
| `uf_wb` standard | -3.96 | -3.60 | -10.91 | +2.01 | -7.38 | -3.96* | -3.96* | A350 RE 1.069, 787 RE 0.858 |
| `uf_nb` Solo standard | -9.18 | -16.13 | -16.13 | -12.60 | -12.60 | +19.78 | +29.74 | fps 2.083, NGSA 4.909 |
| `uf_nb` `jv_pw` standard | -4.79 | -11.74 | -11.74 | -8.21 | -8.21 | +9.69 | +14.67 | 2.083, 4.909 |
| `uf_wb` + `uf_nb` Solo | -15.06 | -14.69 | -22.01 | -9.09 | -18.47 | +13.90 | +23.86 | as above |

Our widebody status quo beats every Re-engine except a 787 Re-engine on UltraFan. Both engines together cost $1.9B of strain.

**Contested incentive.** `airframer_incentive_b` compares UltraFan only with the fallback, not with `cfm_open_fan`, `pw_gtf2` or `pw_wb_new`. `whatif` the airframer's delta PV on each engine open to it (P&W's once `gtf_next` / `pw_wb` is launched or announced for this turn) and use UltraFan's margin over the best. Airframer delta PV, $B [whatif]:

| Programme, launch year | UltraFan standard / aggressive | Best alternative |
|---|---|---|
| NGSA 2026 | 39.55 / 46.05 | open fan 43.15 |
| NGSA 2029 | 45.71 / 50.66 | P&W aggressive 48.19 (open fan 39.07) |
| fps 2026; 2029 | 15.58 / 18.89; 18.14 / 20.51 | P&W aggressive 17.24; 19.32 |
| A350 Re-engine 2026 | -0.29 / 1.09 | P&W -0.12 (aggressive 1.03) |
| A350 Re-engine 2029 | 2.25 / 3.30 | P&W aggressive 2.16 |
| 787 Re-engine 2026; 2029 | 0.78; 2.80 (standard) | P&W 0.60, GE -0.08; GE 2.47 |

### `uf_wb`: UltraFan widebody
- **Default:** do not launch. Break-even P(A350 Re-engine on UltraFan) ≈ 0.54 (3.96 / (3.96 + 3.35), inference).
- **Launch** in the turn for which Airbus announced an A350 Re-engine, if the contested incentive is > 0 at standard and `whatif` beats Do Nothing (2029: +2.36). Precedents: A330neo derivative launched with the airframer [own] [R-0319]; exclusivity extended against GE [own] [R-0361]. Use the turn's first year; never pre-launch (2026 then a 2029 Re-engine: -3.69 against -2.75) [whatif].
- **787 Re-engine:** only if P(UltraFan) > 0.42 (inference); GE prices hard [own] [R-1946]. Boeing's 2025 engine supply-chain comments mention only GE and CFM [customer] [R-1849] (inference: RR not top of mind; not a selection signal); the load-bearing evidence is one engine per airframe and GE sole source on the 777X [customer] [R-1830, R-1831]. Yet Boeing's own PV favours UltraFan (table), so an announced 787 Re-engine may want a non-GE engine: check `whatif`.

### `uf_nb`: UltraFan narrowbody
- **Default:** Do Nothing until fps or NGSA is announced for this turn [own] [R-1011, R-1005].
- **Launch** when all hold: an announcement; contested incentive > 0 at standard, unless the airframer named UltraFan (fallback incentive now fps 2.083, NGSA 4.909); expected PV ≥ +$2B (§9). Break-even P [T1] (inference): Solo NGSA 0.24, fps 0.32; Joint Venture 0.25 / 0.33.
- **Solo or Joint Venture** (inference: RR's generic partnership preference [own] [R-1010, R-1022, R-1025] mapped onto the game's only partner variant; RR's record with P&W is friction [own] [R-0318] [rival: P&W 10-K] [R-1892, R-1893] [rival: P&W] [R-1875]). Choose `jv_pw` when P&W announced its join, unless Solo's expected PV is > $3B higher (P ≳ 0.38 NGSA, ≳ 0.51 fps). So [T1]: at P 0.6 Solo wins by $7.3B (NGSA) and $4.3B (fps): **Solo is the expected result once a launch customer announces UltraFan**, a declared reversal that RR's words allow ("we don't need partnership for capability" [own] [R-1022]). At P 0.35 the NGSA Joint Venture (+2.02, Solo +4.44) is chosen if P&W announced; fps fails the $2B bar (Solo +0.96). P&W must announce `join_rr_jv` in turn t-1 for turn t. [whatif] NGSA 2029: Solo +21.38, Joint Venture +10.54, without P&W 0.00 (slot lost to CFM); 2032 Solo +15.10, 2035 +10.38.
- Airbus names open fan for NGSA [customer] [R-1867, R-1868], and in 2026 it beats our standard terms (table): lower P (inference).

### `terms`
- **Default `standard`** [own] [R-1582, R-0367]: it beats the fallback everywhere [T1], not every rival (table).
- **`aggressive`** only when the contested incentive is ≤ 0 at standard and positive at aggressive, and the selected PV stays ≥ $2B above Do Nothing. `gtf_next` shows a turn late: if P&W announced it for this turn, test against `pw_gtf2` on aggressive terms. Aggressive lifts fallback incentives to A350 2.454, 787 2.194, fps 5.388, NGSA 11.406 and costs us, when selected, NGSA $6.37B, fps $4.68B, A350 $1.08B, 787 $1.48B [T1]. Precedents: 777X bid [own] [R-0317]; Trent 7000 concessions [own] [R-0753]; portfolio pricing [own] [R-1494].
- **A350:** not aggressive unless P&W's `pw_wb` beats our standard terms (row 13); otherwise it only raises Airbus's incentive to Re-engine, which costs us (inference).

### `t1000_upgrade`
- **Default: fund in turn 1**, while no UltraFan is in development: +0.81 (T1), +0.60 (T2), +0.43 (T3); +0.73 with an A350 Re-engine on GE in 2029, +0.11 with a 787 Re-engine on GE; -0.14 only if a 787 Re-engine launches in 2026 [whatif] [T1].
- **Strain.** The engine counts the upgrade's 3-year window as a development window, although the rules text names only narrowbody-widebody overlap. Turn 1 with `uf_nb` Solo -9.68 (alone -9.18), with `uf_wb` -4.46 (-3.96), with `jv_pw` +0.16 net; turn 2 strain -0.99. Funded in 2026 it ends before a 2029 launch (-6.08 = -6.90 + 0.81) [whatif]. If a launch is due and the upgrade is unfunded, defer the upgrade.
- Precedents: durability "is the only thing holding us back" on the 787, and the upgrade targets 787 share [own] [R-1015, R-1021]; durability spend pays back within years, not UltraFan's 15 [own] [R-1601]; the TEN was a 3% fuel-burn derivative [own] [R-0921] (inference: a share defence). Credit share only after `lag_years` 3: RR, Boeing, then regulator tests [own] [R-1207].

### Do Nothing and `cancel`
- Do Nothing is the default on every UltraFan lever until a flip above fires.
- Cancel an UltraFan no airframe flies once its target programmes launched on other engines; capex is sunk (rules). Precedents by analogy: F136 (funder walked away), NMA (own withdrawal) [own] [R-0309, R-0980]. Keep the technology: the demonstrator was kept alive through COVID and assembled by 2022 [own] [R-1002], though new-programme capitalisation was cut [own] [R-0986].

---

## 7. How we read the airframers and rivals

**Airbus: patron and landlord.** RR's franchise is Airbus sole sourcing: XWB 100% of A350 and Trent 7000 100% of A330neo deliveries [record] [R-0134]. Head-to-head, RR bleeds (Trent 900 share of A380 deliveries 84% → 11%) [record] [R-0134]. Airbus uses its options: it talked to GE on the A350 [own] [R-0361]; its A330neo hollowed out A330ceo demand [own] [R-0378]. For NGSA it names open fan, with an open-rotor wing demonstrator from 2027 [customer] [R-1867, R-1868]. **Discount:** act on an announced A350 Re-engine; treat pricing pushback as negotiation: RR kept its pricing framework [own] [R-0442] and took 108 XWB-97 orders in 1H24 [own] [R-0443].

**Boeing: a customer that buys GE.** One engine per narrowbody; GE alone on the 777X [customer] [R-1830, R-1831]; Trent and GEnx judged less mature than LEAP [customer] [R-1837]; engine chosen 6-7 years before entry into service [customer] [R-1833]; its 2025 engine supply-chain comments mention only GE and CFM, and airlines want durability first [customer] [R-1849, R-1848] (inference: RR is not top of mind; not a selection signal). It priced the 787 hard against the A330neo [own] [R-1935]. **Discount:** assume Boeing takes its default engine unless it announces UltraFan, but its own PV favours UltraFan on a 787 Re-engine (§6 table).

**CFM/GE: benchmark and aggressor.** GE discounts when RR is weak ("extraordinary" Air New Zealand offer) [own] [R-1946, R-1945]; its higher returns come mostly from a more mature fleet [own] [R-1942]. CFM entered LEAP from an 80% CFM56 share and is sole source on the 737 MAX [press/industry] [R-1918, R-1916]. **Expect** GE to contest any Re-engine; CFM is every narrowbody's default.

**Pratt & Whitney: former partner, rival, possible partner.** P&W could justify the A320neo when RR could not [own] [R-0313, R-1937]; formed IAE LLC without RR [rival: P&W 10-K] [R-1892]; vowed to use its balance sheet to gain share from weakened rivals [rival: P&W] [R-1880]; took RR's Gulfstream position [rival: P&W] [R-1877]. **Expect** P&W to seek control of a Joint Venture (inference from [R-1893]), to back its own GTF, and, once `pw_wb` is launched, to contest the A350 Re-engine (§5 row 13). **Discount** P&W's jibes at RR's loss-leading OE: P&W books negative engine margin too [rival: P&W] [R-1878].

---

## 8. Biases and failure modes (display only when the situation matches)

1. **Optimism on durability and fixes.** *When* judging UltraFan readiness or upgrade timing. RR reversed a £65m Trent 1000 impairment on early data [own] [R-1102], called the problem "solved" [own] [R-1186], admitted a "streak of optimism" [own] [R-1458]. *In play:* never disclose an EIS earlier than `dev_years`; credit upgrade share only after `lag_years`.
2. **Buying share with OE concessions, now suppressed.** *When* a narrowbody selection is close. OE loss £1.6m per engine, CARs £286m (2017) [own] [record] [R-0659, R-0113]; now "not after market share" [own] [R-1582]. *In play:* `aggressive` only if `whatif` proves it.
3. **Comfort in sole-source positions.** *When* the A350 is threatened. RR loses share head to head [record] [R-0135]. *In play:* launch in the announced turn; never wait for the fallback.
4. **Maturity over timing.** *When* an airframer launches before UltraFan fits. RR missed the neo/MAX round [press/industry] [R-1812] and left NMA [own] [R-0980]. *In play:* the game's narrowbody slots are one-shot; a skipped launch turn is lost.
5. **Narrowbody oscillation.** *When* a narrowbody launch is announced. "Unfinished business" then "we don't have to" [own] [R-0942, R-0952]. *In play:* signal interest, keep Do Nothing credible.
6. **Caution after a shock.** *When* a turn follows a crisis, demand shock or launch. Capex below consensus in 2021-22 and 2024-25 [market] [R-1723]; yet net cash is £1,972m [record] [R-0032]: a preference, not a constraint (inference).
7. **Guide low, beat.** *When* disclosing. [record] [R-0219]. *In play:* understate upside; never over-promise dates.
8. **Concurrency aversion.** *When* both UltraFans are candidates [own] [R-0929, R-1318]. *In play:* no overlapping development windows, upgrade included; sequence or Joint Venture.
9. **Taking airframer forecasts at face value.** *When* relying on disclosures: RR was "completely aligned" with Airbus on A330 rates; the view failed within months [own] [R-0377]. *In play:* check announcements against the contested incentive (§6).

---

## 9. Decision procedure for each turn

Scratch files go only under `/tmp/wargame-rolls_royce/`.

1. `python3 -m wargame.engine brief --run <RUN> --side rolls_royce`: airframe and supplier programmes, engines, disclosures and statements (earlier turns only), injects. Turn 1: also `rules`; check against `financials.md` § Game calibration.
2. Match §5 rows and triggered §8 biases.
3. `python3 -m wargame.engine options --run <RUN> --side rolls_royce --compact`: selected and unselected values, `airframer_incentive_b` (fallback only). Then `whatif` the contested incentive (§6).
4. P(selected) per programme (inference, doctrine), from earlier turns only:
   - 0.6: announced for this turn on UltraFan (an announced A350 Re-engine counts, its default engine being ours, unless P&W has `pw_wb`);
   - 0.35: announced for this turn with the engine open and contested incentive > 0;
   - 0.2: a signal: a statement, disclosure or market report naming the programme but not this turn;
   - 0.1: nothing; 0: contested incentive ≤ 0 at our terms.
   On [T1] numbers only 0.6, and 0.35 on NGSA, clear the bars below; signals feed step 13.
5. `whatif` the alternatives, keys are turn numbers:
   ```
   python3 -m wargame.engine whatif --run <RUN> --side rolls_royce <<'EOF'
   {"rolls_royce": {"2": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2029}], "cancel": [], "t1000_upgrade": false}},
    "airbus": {"2": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2029}]}}}
   EOF
   ```
   Vary: airframer selects us vs CFM/GE/P&W; Solo vs `jv_pw` (add `"pratt_whitney": {"2": {"join_rr_jv": true}}`); standard vs aggressive; upgrade on/off. Expected PV = P × selected + (1 − P) × unselected.
6. **Narrowbody.** Launch `uf_nb` only for an announced fps or NGSA, when expected PV ≥ +$2B: Solo at P 0.6; `jv_pw` only if P&W announced `join_rr_jv` for this turn and Solo exceeds it by ≤ $3B.
7. **Widebody.** Launch `uf_wb` in the turn for which Airbus announced an A350 Re-engine (contested incentive > 0; `whatif` beats Do Nothing). For a 787 Re-engine require P > 0.42.
8. **Terms.** Standard unless §6's aggressive test passes.
9. **Upgrade.** Fund `t1000_upgrade` if unfunded, positive in `whatif`, and its 3-year window overlaps no UltraFan development (always so in turn 1 under this doctrine).
10. **Cancel** an unselected UltraFan whose target programmes have launched on other engines.
11. **Weigh PV against doctrine.** Follow the engine's best option unless it breaks a red line. Where doctrine costs PV (Joint Venture over Solo; no speculative launch; standard over aggressive), state "doctrine premium: $X B" with ids. Cap any doctrine premium at $3B per turn; above that, take the PV-best option and cite RR's reversals when the business case moves [own] [R-0959, R-1561].
12. **Disclose** conditional, verifiable commitments, e.g. (a script, not an RR quote): we will launch UltraFan in any turn for which an airframer has announced in advance a programme on UltraFan; no narrowbody engine without a launch customer; partnership preferred [own] [R-1005, R-1010, R-1025]. Both sides must announce in turn t-1 to launch together in turn t. Never disclose dates earlier than `dev_years`.
13. **Predict.** Compare each airframer's delta PV by launch turn with `whatif`; in turn 1 all pay more in 2029 than 2026 (fps 16.72 vs 13.50, NGSA 42.05 vs 34.65, 787 Re-engine on GE 2.47 vs -0.08, A350 Re-engine on GE 1.70 vs -1.36). Add NGSA's second-half-2030s target [customer] [R-1867] and engine choice 6-7 years before entry into service [customer] [R-1833]; predict no unannounced launch. `expected_delta_pv_b` = the step-5 expected PV of the orders you submit, not the projection under your prediction.
14. `validate --run <RUN> --side rolls_royce` (it checks only launch, cancel, upgrade). Return:
   ```
   {"launch": [], "cancel": [], "t1000_upgrade": true, "public_statement": "...", "disclose": ["..."],
    "prediction": {"boeing": {"launch": []}, "airbus": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb"}]}},
    "expected_delta_pv_b": 0.81, "rationale": "ids, engine numbers, doctrine premium"}
   ```

---

## 10. Confidence and gaps

- **Strong:** capital allocation, crisis behaviour, guidance (MS and Capital IQ cells, 2000-25); Trent 1000 economics; post-2023 price discipline; A350 defence.
- **Thin: narrowbody launch behaviour.** RR has not launched a narrowbody engine since the V2500; everything after 2011 is words [own] [R-1011, R-1022]. Treat §6's narrowbody thresholds as inference.
- **Joint Venture with P&W:** no closed precedent since IAE; why the 2012 Joint Venture lapsed is not in the evidence [own] [R-0916] [rival: P&W 10-K] [R-1892].
- **No UltraFan programme cost or schedule** from RR beyond the NMA estimate and £500m spent [own] [R-0965, R-0966]; `uf_nb` capex is calibrated ±$2B (calibration memo).
- **One-sided customer view:** Boeing on RR mostly 2010-12; Airbus only its FY2025 report [customer] [R-1837, R-1862].
- **GTF:** the 2023 powder-metal recall is absent from our evidence.
- **Dated:** the MS model predates FY25 results [analyst] [R-1608]; P&W's words end in 2021.
- **No airframer text on fps, NGSA engines or either Re-engine** beyond Airbus's open-fan focus [customer] [R-1867]; selection probabilities in §9 are doctrine, not evidence.
- **Engine mechanics we play around** (for the engine owner): strain counts the upgrade's window, unlike the rules text; `airframer_incentive_b` ignores open fan and P&W engines; `validate` skips `disclose` and `prediction`.
- **PLACEHOLDER parameters:** `jv_pw` dev_years and strain_relief; `strain.full_overlap_b` and `norm_years` (financials.md § Game calibration).
