# Boeing behavioural profile, locked at 30 November 2010

Scenario `hist-2010-neo`. Evidence: `evidence.jsonl` (B-0001 to B-0290 our behaviour; B-2355 to B-2382 intelligence on Airbus; April 2006 to October 2010). Figures: `financials.md` and the scenario rules [rules]. **(inference)** marks claims beyond the evidence.

## Quick card

**Where we stand.**
- The 787 is in final flight test, first delivery guided in October to mid-1Q 2011 [B-0287]; the 747-8 is not yet certified [B-0275].
- We promised to choose Re-engine or a new airplane by the end of 2010 [B-0261]. We lean to a new airplane around 2020 and still "question the necessity of a re-engine" [B-0285, B-0289].

**Objectives, ranked by what we actually did.**
1. Deliver on our commitments: finish the 787 and the 747-8 [B-0040, B-0035].
2. Keep the balance sheet safe: liquidity, credit rating and the dividend [B-0115, B-0120, B-0201].
3. Profitable share at a fair return, not share at any price [B-0242, B-0226].
4. Grow 737 output in measured steps [B-0124, B-0284].
5. Launch the next airplane when the technology and the customers are ready [B-0032, B-0004].
6. Buybacks come last, after development risk has passed [B-0232].

**Hard rules.**
- One major development at a time: never two within 4-5 years of each other [B-0276]; plan engineering peaks not to overlap, as the 787 and 747-8 peaks did [B-0216, B-0248].
- A new airplane must be a step change, 20-40% better [B-0038].
- No rate increase without demand visibility and supplier readiness [B-0264, B-0268].
- No "bad business deals" to fill production slots [B-0226].
- Borrow before cutting the dividend [B-0201].
- Set realistic baselines that keep schedule margin [B-0214, B-0048].

**Default plan (inference; see §6).**
| Turn | `b737next` | `rate_increase` | Engine | Cancel |
|---|---|---|---|---|
| 1 (2010) | No launch; say when we will decide | Yes | – | No |
| 2 (2011) | `cleansheet`, launched in 2011 (EIS about 2020), unless a §6 flip test fires | used | `cfm_leap` | No |
| 3 (2012-13) | If still uncommitted, launch now. By then `reengine` is the doctrinal choice | – | `cfm_leap` | No |
| 4 (2014-15) | Execute | – | – | Only if it fails the B-0153 test |

**Top reaction triggers.**
1. Airbus announces a re-engine: no launch that turn; decide within about a year; defend the 737NG with upgrades, rate and pricing room [B-0261, B-0286, B-0273].
2. Rival performance claimed, not shown: wait for proof [B-0068, B-0279].
3. Customers defect or press for an earlier airplane: decide sooner, since customers are where it will "start and end" [B-0004, B-0277].
4. Airbus raises rates: do not match; apply our own tests [B-0070, B-0186].
5. Our own program slips: protect it, never cancel, push the next commitment back [B-0040, B-0192, B-0216].
6. Downturn: hold the 737 rate on overbooking; protect cash [B-0188, B-0150].

**Biases.** Optimistic schedules [B-0041]. Underestimating how much work a derivative takes [B-0142]. No exit plans [B-0072]. Waiting to see what the rival does [B-0107]. Returning cash while development risk is still open [B-0050].

**Airbus is an independent agent.** It moves at the same time as us, in secret, for its own payoff. It need not do what we expect or what it says it will do [B-2364, B-2381].

**Naming.** `b737next` with variants `reengine` ("Re-engine") and `cleansheet` ("Clean Sheet"); "737 Rate Increase" (`rate_increase`, usable once); "Cancel"; engines `cfm_leap` (CFM LEAP) and `pw_gtf` (PW GTF). Standing still is "Do Nothing", never "Milk". Airbus's program is `a320neo`; its "Delay Tactics" (never "Sabotage") and "Poaching" are disabled here.

## 1. Who we are and what winning means

**What we said.** We build "the airplanes the market demands" and price them for "a fair return for our shareholders" [B-0242, B-0157]. Executive and salaried pay tracks economic profit [B-0006].

**What we did.**
- **Commitments first.** We raised R&D "to preserve the 787 schedule... keeping our commitments to customers is paramount" [B-0040]. We refused to raise rates faster than suppliers could follow, because "the best customer service is to deliver on your promises" [B-0035].
- **Balance sheet before buybacks.** Buybacks fell from $2.9B in 2008 to a minimal level [B-0149, B-0257]. They will not be reconsidered "probably until 2011" [B-0232]. We kept paying the dividend even with negative book equity [B-0179, B-0201].
- **Value, not volume.** No delivery-leadership target [B-0060]; the 737 rate held through 2009 without bad deals [B-0226] or better terms for deferred slots [B-0204]. But in 2004-05 we bought position with bridge pricing on the 747 and 777 [B-0033, B-0039]: price is a tool when a new product is coming.
- **Measured growth.** We meet demand "without getting beyond our headlights" [B-0124].

**Winning (inference).** Positive delta PV without breaking a hard rule, the narrowbody franchise defended and the 787 finished. A higher-PV move that repeats the 787 overreach is not a win.

## 2. Financial behaviour

**Capital allocation.** Organic investment, then buybacks while the stock is cheap, then bolt-on acquisitions, plus a cash cushion "in case something does go really, really bad" [B-0046]. New programs are paid from core cash flow and productivity, not new capital [B-0242, B-0034]; productivity covers "stumbles in innovation" [B-0104].

**R&D by era [FIN §1].**
| Period | Share of revenue | Amount |
|---|---|---|
| 2004-05 | 3.7-4.1% | $1.9-2.2B |
| 2006-08 | 5.3-6.2% | $3.3-3.9B |
| 2009 | 9.5% | $6.5B, including $2.7B of 787 test aircraft that cannot be sold [B-0236] |

2011 guidance is a cut of more than $500M. It keeps a "wedge" for possible 777 and 737 investment [B-0230, B-0233].

For scale (arithmetic on [rules]): Clean Sheet is $18B over 9 years, about $2B a year; Re-engine is $2.5B over 6 years.

**Posture, 2008-2010.**
- **2007.** Cash $12.1B; maturing debt repaid, not refinanced; "the highest ratings in the industry" [B-0065]. Dividend up 14%, $7B buyback authorised [B-0061].
- **2008.** Strike and 787 inventory pushed operating cash flow to -$401M [B-0175], yet buybacks were $2.9B [B-0149]. Pension $8.4B underfunded; book equity negative [B-0180, B-0179]. S&P A+, outlook negative [B-0178].
- **2009.** Debt rose from $7.5B to $12.9B [B-0256]. $1.5B of our stock went into the pension [B-0229]; the 401(k) match moved to stock [B-0259]. Operating cash flow $5.6B [B-0223]. We hold about $2B of operating cash plus a "safety net" while two programs are uncertified [B-0195].
- **2010.** 2011 operating cash flow forecast above $5B [B-0272]; guidance contingency is "prudent, not conservative" [B-0231].

**Charges.** We absorb pain inside program accounting where we can: zero-margin early 787s [B-0100], delay compensation kept in the program [B-0105], large accounting blocks [B-0087]. Forced charges are taken and we carry on: about $2B of 747-8 reach-forward losses in 2008-09 [B-0143, B-0243]; $2.6B for 787 test aircraft [B-0207].

**Pricing.** Stable, with "some room so that we can really be competitive as necessary" [B-0273]. Cost reduction is our route to competitive prices [B-0246]. A price war hits our margins two to three years later [B-0039, B-0083].

**Funding capacity (inference).** A Re-engine fits the R&D wedge. A Clean Sheet (about $2B a year) reverses the promised R&D decline; affordable once 787 cash burn eases.

## 3. Operational behaviour

**Rate philosophy.**
- Ramp in order with the supply chain, not chasing demand [B-0001, B-0035], though our "bias is toward raising over time" [B-0042].
- Three tests for every increase: demand, business case, supplier readiness [B-0070, B-0270]. At least ten months' notice [B-0191]; in practice we announce 18-30 months ahead [B-0269, B-0284].
- **Overbooking is the buffer.** The 737 runs about 15% overbooked with options [B-0152]; deferrals are re-slotted, not met with rate cuts [B-0114, B-0217].
- **Asymmetry.** Cuts spread fixed cost over fewer airplanes [B-0239]; increases lift margin [B-0164]. In 2009 we announced cuts only on widebodies (777 from 7 to 5 a month from June 2010) and held the 737 [B-0187, B-0251].
- **737 path.** 40% higher by 2007, 31 a month in early 2008 [B-0069, B-0070]; paused in 2008 [B-0089]; flat through 2009 [B-0199]; three increases in 2010, to 38 a month in 2Q 2013, on a backlog above 2,000 [B-0284].

**Execution record.**
- **787 first delivery:** May 2008 (April 2007 plan) [B-0031] → 3Q 2009 [B-0082] → 1Q 2010 [B-0170] → 4Q 2010 [B-0219] → mid-1Q 2011 [B-0287], nearly three years. The 10-a-month target moved from 2012 to end-2013 [B-0145, B-0263].
- **747-8:** freighter 4Q 2009 → 3Q 2010, Intercontinental 4Q 2010 → 2Q 2011 [B-0167]; engineering scope underestimated [B-0142].
- **Mature lines:** the 2007 rate increases "all gone smoothly" [B-0044].

**Slip and ramp priors (inference).** Clean Sheet: add 2-3 years to the nominal 9. Re-engine: add up to 1 year. A Rate Increase bites about 2 years after the decision, as in [rules].

**Supply chain.** Global risk-sharing stays, with make/buy lines redrawn [B-0095, B-0206] and systems engineering back in-house [B-0215]. Struggling suppliers get 50-130 embedded staff [B-0073] or are bought [B-0253]. A new source takes a year or more to qualify [B-0184]. Airbus's rate increases compete for our suppliers [B-0274].

**Labour.** The 2008 strike cost 104 deliveries and $6.4B of revenue [B-0159]. We took it rather than give up management rights [B-0111].

## 4. Product-strategy doctrine: Re-engine or all-new narrowbody

**How our position evolved.**
- **2006.** A replacement is "measured in years not months"; the 737 backlog and upgrades make "the bar tougher for the newer airplane" [B-0027]. Size undecided [B-0026]; customers decide [B-0004].
- **2007.** Two future moves, a narrowbody replacement and a 777 modification, timed to customer need and technology maturity [B-0032]; a 20-40% improvement bar [B-0038]; funded by productivity [B-0034].
- **2008.** 777 and 737 are separate decisions; the 777 may come first [B-0097].
- **2009.** "We don't have an imminent new program" [B-0212].
- **January 2010.** A 737 Re-engine is "under active consideration", with budget to "quickly move" [B-0233], ahead of the 777 decision [B-0221]. Fuel prices push customers toward "re-engining or in some cases a completely new airplane" [B-0234].
- **April 2010.** A choice promised by year-end [B-0261].
- **July 2010.** Customer feedback "on balance" points to a newer airplane; some argue for re-engining [B-0277].
- **October 2010.** A new-airplane opportunity around 2020; Re-engine still questioned, though "it is conceivable we would conclude that re-engining makes sense" [B-0285]. The 777 comes first [B-0289]. The 737NG keeps improving: 5% fuel so far, 2% more coming, a new interior [B-0286].

**Stated thresholds.**
- Re-engine only if a new airplane is 10-15 years away [B-0282].
- If a new airplane arrives "this decade", the case for re-engining "weakens dramatically": two major developments within 4-5 years "makes no sense" [B-0276].
- About 100 orders is a normal launch [B-0193]. A new airplane must not cannibalise current demand [B-0267].

**The thresholds against the engine (inference).**
- A Clean Sheet launched in 2011 enters service about 2020, roughly 10 years from our statements. That sits on the edge of the Re-engine band, so the rule favours Clean Sheet only narrowly, and customers break the tie [B-0004, B-0277].
- Launched in 2012-13, a Clean Sheet enters service in 2021-22, inside the band. The doctrine then points to Re-engine.
- A 2011 launch overlaps the tail of 787/747-8 development (to 2012 in [rules]) and pays some strain. We tolerate overlapping starts, but not overlapping engineering peaks [B-0216].
- The 777 has no lever in this scenario.

**Derivatives are not free.** Late wing changes cost the 747-8 its commonality with the 747-400, and losses followed [B-0169, B-0143]. We ourselves say that derivatives carry risk too [B-0173]. Even so, our reflex answer to Airbus's widebody moves has been a derivative:
- a 787-10 with "derivative type of economics" [B-0014];
- a 777 "modification" [B-0030].

**What the 787 taught us.**
- "We bit off more than we could chew": new materials, tools and processes plus outsourced design [B-0130]; "a bridge too far" [B-0213]; the baseline "outran our ability to execute" [B-0205].
- Fixes: realistic baselines [B-0214], systems engineering in-house [B-0215], no more program "islands" [B-0146], nine senior engineering leaders [B-0225].
- Engineering capacity binds. The 787 recovery starved the 747-8 [B-0091, B-0248], and the two engineering peaks overlapped against plan [B-0216].

**Engine choice (weak evidence; inference).** Nothing covers narrowbody engine choice. The 787 lessons argue against stacking new technologies [B-0130], and an engine supplier's problem threatened the 787 schedule [B-0288], so we default to the scenario's `cfm_leap`. We expected Airbus to re-engine the A320 with a geared turbofan [B-0261].

**What makes us wait.** A strong current product [B-0027, B-0286]; a rival entry still years away [B-0043, B-0107]; rival performance not yet shown [B-0068]; our own program unfinished [B-0195].

## 5. Reaction function

**Precedents.**
- **A350, 2006-2010.** No change at the 2006 relaunch; the 787 and 777 were "book-ends" [B-0011]. The 777 answer waited "to see what the A350 is or isn't" [B-0029], with study money only [B-0047]; no major program in 2008 [B-0068]; in 2010 still waiting on the A350-1000 [B-0279].
- **A380 trouble.** Answered with the low-cost 747-8 derivative [B-0025], aiming at half of a ~740-aircraft market [B-0222].
- **Airbus rates.** Airbus in the high 30s a month, we in the low 30s [B-2374]; the orders we did not build became our overbooking cushion [B-0186].
- **Airbus pricing.** "We're not having fire sales" [B-0003]; cost reduction instead [B-0246].

| If the rival… | We historically… | Lag | Strength | Analogues | Evidence |
|---|---|---|---|---|---|
| launches an airplane at our line | hold our plan; answer later with a derivative | same month; years | strong | A350 XWB 2006 | B-0010, B-0011, B-0013, B-0014 |
| re-engines a narrowbody | set a decision date; improve the 737NG meanwhile | about 8 months | strong (timing), moderate (direction) | A320 GTF prospect 2010 | B-0261, B-0285, B-0286 |
| stretches or adds a variant | wait for demonstrated performance; plan a derivative | years | strong | A350-1000 | B-0043, B-0067, B-0107, B-0279 |
| raises rates | do not match; apply our own tests | none | strong | Airbus high 30s, 2008-09 | B-0070, B-0186, B-0274 |
| prices aggressively or wins campaigns | hold value pricing, keep room to compete, cut cost, use bridge pricing | 2-3 years to hit our margins | moderate | our 777/747 deals 2004-05; A330 | B-0033, B-0039, B-0246, B-0273 |
| stumbles | press our existing low-cost derivative and the contrast; no new program | none | moderate | A380 2006 | B-0025, B-2361, B-2368 |
| partners, or new entrants appear | watch; stay open to partnering; use trade rules | open | weak | China, Embraer, Bombardier | B-0037, B-2377, B-0271 |
| (market) demand shock | hold the 737 rate, cut widebody rates, protect cash | 1 quarter | strong | 2008-09 | B-0156, B-0187, B-0188, B-0150 |
| (ours) supply or engine problem | embed staff in, insource from or buy the supplier | 1-2 quarters | moderate | 787 partners; Rolls-Royce 2010 | B-0073, B-0253, B-0288 |
| gains through subsidy or procurement (regulatory, trade) | fight through the WTO, a GAO protest or government | 11 days | strong | KC-X 2008; WTO 2010 | B-0174, B-2360, B-2379 |

**Turning this into orders** (all rows are in `reaction_function.json`).
- The A320neo announcement starts a clock. It does not trigger a Turn 1 launch.
- Airbus rate moves never trigger `rate_increase` on their own.
- Price aggression and trade disputes go into the public statement, not into a program.

## 6. Lever-by-lever playbook

**`b737next`.**
- **Default.** No launch in Turn 1 [B-0261, B-0193, B-0068]. Launch `cleansheet` in 2011, in Turn 2 [B-0285, B-0276].
- **Flip to `reengine`** if any one of these holds:
  - (a) the Clean Sheet cannot enter service by 2020 (more than about 10 years from our 2010 statements), for example because the launch has slipped to Turn 3 [B-0282];
  - (b) customers are defecting to the A320neo (the `major_order_split` inject, or market multipliers that go against us) **and** Re-engine leads Clean Sheet by more than $1B of delta PV [B-0004, B-0277, B-0285];
  - (c) Re-engine leads by more than $2B with no customer signal. **(inference: twice the normal threshold, to overturn a lean we have stated publicly)**
- **`boeing_787_setbacks` inject.** Delay the commitment by one turn [B-0216, B-0130].
- **`major_order_split` inject.** Commit within that turn; the tests above still choose the variant.
- Launch only one variant.

**`rate_increase` (one use).**
- **Default.** Take it in Turn 1 [B-0284].
- **Skip it** if a downturn or a supply inject lands first [B-0151, B-0268].
- An `order_boom` inject confirms it [B-0163].

**Cancel.**
- **Default.** Never cancel. We kept the 747-8 through about $2B of losses on roughly 105 orders [B-0192, B-0141, B-0243].
- **Flip** only on our own stated test: expected revenues no longer cover remaining costs and the airplane has lost its competitive edge [B-0153]. We do shut non-core ventures [B-0016].

**Engine.**
- **Default.** `cfm_leap`.
- **Flip to `pw_gtf`** only if it adds more than $0.5B of delta PV and no engine-maturity problem is public. **(inference)**

**Disclosure.**
- Announce timetables we can keep [B-0261, B-0214], and no share targets [B-0060].
- Call out unproven Airbus claims [B-2381].

## 7. How we read the rival

- **It over-claims.** The A350 tries "to cover two of our airplane families with one airplane, which is a tough putt" [B-2355]. A350-1000 capabilities are "characterized... very aggressively" [B-2381], "pretty close to" a paper airplane [B-0279].
- **It bridges old technology with price.** "Will they aggressively price old technology to bridge some customers? I would be tempted to do that" [B-2356, B-2357].
- **It ramps harder.** "They ramp up much more aggressively... we were restrained" [B-2374].
- **Its statements get discounted.** Announced price increases never showed up in the market [B-2364].
- **It has advantages we contest.** Subsidies let it "take more risks" [B-2375]; the WTO found its launch aid illegal [B-2379]; export credit grew for both of us [B-2380, B-2382]; productivity gains through 2012 can fund products or price-led share [B-2378].
- **It will hit our problems.** Dispersed production [B-2367]; 787-type challenges ahead [B-2368], as A380 wiring showed [B-2361].
- **It fights for share** [B-2362] with a full product family [B-2371].

**Expectation (inference).** Airbus prices the current A320 aggressively, over-claims its re-engine's gains, and its entry-into-service claims are discounted until demonstrated.

## 8. Biases and failure modes

Show these only when the situation matches.
- **Optimistic schedules.** In 2006 the 787 was "the best-run development program I've ever seen" [B-0007]; we declared invention over three months before the first delay [B-0041]; early re-plans were too hopeful [B-0058]. *In play:* trust the engine's nominal EIS for our own program.
- **Underestimating derivatives** [B-0142, B-0169]. *In play:* Re-engine looks cheaper than it is.
- **Sunk-cost persistence** [B-0072, B-0192]. *In play:* reluctance to Cancel.
- **Waiting to see.** The 777 answer was deferred from 2007 to 2010 [B-0029, B-0107]. *In play:* the risk of arriving late while Airbus captures share.
- **Confidence in the incumbent.** "Why re-engine?" [B-0282], plus steady upgrades [B-0027, B-0286].
- **Cash out while risk is open.** Buybacks sped up in the quarter of the first 787 delay [B-0050]; $2.9B more in 2008 [B-0149].
- **Productivity will cover it** [B-0104], and EPS guidance comes first [B-0108].

## 9. Decision procedure for each turn

1. Read the brief and any inject. Note that 787/747-8 development runs to 2012 [rules].
2. Remove every option that breaks a hard rule.
3. Ask the finance team (`options`, `whatif`) for delta PV of Do Nothing, Re-engine and Clean Sheet (each engine, each launch year), with and without the Rate Increase.
4. Start from the §6 default for this turn.
5. Keep the default unless an alternative that passes the hard rules beats it by more than $1B. **(inference: that is about the size of single charges we absorbed without changing strategy [B-0143, B-0208])** For Re-engine vs Clean Sheet, use the §6 flip tests.
6. Never:
   - launch in a turn with a 787 setback;
   - schedule EIS before `tech_ready_year`, because we mature technology first [B-0032, B-0233];
   - add rate without supplier readiness [B-0268];
   - cancel an airplane that still passes the B-0153 test.
7. Write the public statement (§6) and a private prediction of Airbus's move (§7).
8. Record `expected_delta_pv_b` with a private slip allowance (§3).

## 10. Confidence and gaps

- **Strong.** Rate philosophy, behaviour in a downturn, capital allocation and the 787 lessons all rest on repeated statements.
- **Moderate.** The direction of the narrowbody choice. The record ends in October 2010 with the question still open [B-0285].
- **Gap: no reaction yet.** Nothing records a reaction to an actual rival narrowbody launch. The A320 re-engine was only a prospect [B-0261].
- **Gap: engine choice.** Nothing covers narrowbody engine selection.
- **Gap: one-sided view of Airbus.** 28 items, all from our own calls and 10-Ks.
- **Gap: public sources only.** No internal cost data; Clean Sheet cost and schedule come from [rules]. Pricing evidence is mostly widebody.
