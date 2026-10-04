# Pratt & Whitney: behavioural profile

Pratt & Whitney (P&W), the engine segment of RTX (before April 2020, United Technologies, UTC). Built from 2,072 verified items (`evidence.jsonl`), the calibration memo and the live engine rules. Reported figures in $; game numbers in the engine's $B.

## Tag legend

- **[own]**: P&W, UTC or RTX executives on calls, or their 10-K filings.
- **[record]**: reported numbers (10-K tables; GS history columns, including RTX dividends and buybacks).
- **[analyst]**: analyst estimates and questions (mostly the Goldman Sachs RTX model, 21 Oct 2025: "GS").
- **[market]**: consensus (none in our file).
- **[press/industry]**: the press and the 2019 industry brief.
- **[customer]**: an airframer's own words.
- **[rival]**: Rolls-Royce's own words, as held in our evidence file.
- **[engine]**: live `rules`, `options` or `whatif` for run `calib`, turn 1; re-run each turn.
- **(inference)**: our reading. **(view)**: a forecast, not the record.

## Quick card

**Ranked objectives (revealed).**
1. Keep the GTF franchise on the A320neo and its aftermarket annuity: about 40% of A320neo selections (claimed, 2024), mostly on fixed-price flight-hour contracts [own] [P-0111][P-0295][P-0591].
2. Clear the GTF return bar on any new engine: about 10% all-in (inference from "more close to double-digit") against an 8% cost of capital, set with the board [own] [P-1243][P-1163][P-0731][P-0715].
3. Protect the dividend and repair the rating after shocks [own] [P-0566][P-0423][P-1362]; the dividend was held in 2020 and raised every year since [record] [P-1887]. A new engine would compete with buybacks, not the dividend (inference).
4. Take profitable share, not maximum share: 40-50% of a shared platform is fine [own] [P-1292][P-0706].
5. Get back onto Boeing, but only as sole source and above the hurdle [own] [P-0737][P-0731][P-0702].

**Hard rules and red lines.**
- No new engine without a committed airframe and sole source [own] [P-0746][P-0737][P-0711], except to defend the A320neo franchise (§4) [rival][own] [P-1868][P-1347]. In the game "committed" means disclosed for this turn; the one exception is the NGSA hedge (§6, inference).
- No deep discounts past launch mode [own] [P-0735][P-1333]; `aggressive` never pays at calibrated values [engine].
- No widebody engine: "narrow-body focused" [own] [P-1313]; widebody risk only inside a 50/50 Joint Venture [record] [P-1700][P-1676].
- Never fund an engine by cutting the dividend [record] [P-1887][P-1888].
- Share risk and investment in a Joint Venture, never our core technology [own] [P-1233]; joining RR's UltraFan shares RR's, not ours (inference).
- Game constraint (inference): no `gtf_next` and `join_rr_jv` aimed at the same airframer unless `whatif` favours the pair. RR's view is that a Joint Venture holds only while both partners are on the same new engine [rival] [P-1875].

**Default plan by turn** (inference from §6 and §9). Every launch states `year` (the turn's last) and `terms`.
- **Turn 1 (2026-28):** `gtf_upgrade` in 2026. `gtf_next` (2028, standard) only into an NGSA or fps disclosed on `pw_gtf2` for this turn, or if the §6 odds of NGSA on `pw_gtf2` reach about 0.45; with RR in play and no disclosures they are about 0.2, so disclose a conditional offer instead. `join_rr_jv` off unless the §6 test holds. No `pw_wb`.
- **Turn 2 (2029-31):** cancel a `gtf_next` nobody flies or has disclosed for; launch into any NGSA or fps disclosed on `pw_gtf2`; fund a missed upgrade.
- **Turns 3-4:** launch only into a disclosed selection, on standard terms; otherwise Do Nothing.

**Top reaction triggers.** NGSA or fps disclosed on `pw_gtf2`: `gtf_next` that turn (§5 row 1). Our durability crisis: upgrade and compensate (row 7). RR signals `jv_pw`: the §6 test (row 12). Widebody Re-engine: abstain (row 2).

**Biases to display.** Durability optimism, "reaffirm, then cut", incumbent protection, capacity conservatism (§8).

**Naming.** Do Nothing, Re-engine, Joint Venture, Delay Tactics, fps, NGSA, A350 Re-engine, 787 Re-engine, GTF, GTF Advantage, V2500, IAE, UltraFan.

## 1. Who we are and what winning means

**Identity (inference).** P&W is a narrowbody engine maker that sells engines at a loss and earns its money in a 20-30 year aftermarket. A diversified parent funds it and judges it on long-run NPV, not segment margin [own] [P-1296][P-1143][P-1163].

**Revealed objectives by era.**

| Era | What it said | What it did | ids |
|---|---|---|---|
| 2000s harvest | n/a | Revenue grew from $8.28bn (2004) to $13.85bn (2008), with adjusted margins of 16-17% (2006-08) and no new engine. It "passed on" the 787 and drifted out of large engines [record][own] | P-0026, P-0028, P-1125, P-1139 |
| 2008-15 re-entry | "Overinvesting in Pratt"; ROIC over margin | It committed the GTF on its own readiness. The IAE partner Rolls-Royce "could not make a business case" | P-1126, P-1219, P-1868 |
| 2016-19 ramp | 8% cost of capital; campaigns at a 13-20% IRR | $10bn of E&D, $6bn of capital and $6-7bn of negative engine margin, for payback around 2030. Adjusted margin fell from 14.7% (2014) to 8.8% (2018) [own][record] | P-1163, P-0705, P-0298, P-0034 |
| 2020-22 COVID | The dividend is "sacrosanct" | E&D was cut about $300M and capex about $500M. In Oct 2020 it said it would keep gaining A320neo share, after rising from 43% to about 55% over 2019-20 [own] | P-0423, P-0467, P-0086 |
| 2023-25 powder metal | "Make the airlines whole" | A $2.9bn net charge, 49% borne by partners. It certified the GTF Advantage. There is no new centreline engine in the plan [own][record] | P-0591, P-1563, P-0785, P-0745 |

**Said versus did.** "Not capital-constrained" was true: what blocked a new engine was the return test and sole source [own] [P-1164][P-0715][P-0737]. The claimed return shrank, from "well in excess of cost of capital" (2017) to "more close to double-digit" (2019) [own] [P-0715][P-1243]. Share discipline is real but reversible: it "deliberately backed off" campaigns in 2017-18, gained from 43% to about 55% over 2019-20, mostly before COVID, and said in October 2020 it would keep pushing [own] [P-0074][P-0086]. "Rivals weakened" was an analyst's premise [analyst] [P-1974].

**How UTC and RTX fund and judge P&W.** The conglomerate is the banker: "Pratt probably couldn't have done 5 engine development programs" alone [own] [P-1138]; Collins cash was earmarked for "the next engine" and the Raytheon merger sold as the scale to fund one [own] [P-0330][P-0378]. It judges on intrinsic value at about 8%, down to product line [own] [P-1163], and on order-book NPV (more than $7bn in 2016) [own] [P-0182]. It tolerates dilution: P&W's share of UTC operating income fell from 28.5% (2007) to 18.6% (2019); in RTX it was 8.0% (2020) and 24.0% (2024), against 33.8% of 2024 revenue [record] [P-0051][P-0045]. Its benchmark is its own stock: a $10bn ASR six weeks after the powder-metal charge [own] [P-0602], so a new engine must beat buying RTX shares (inference).

## 2. Financial behaviour

**Capital allocation hierarchy, revealed by what moved.**
1. **Committed programme spend.** Never cut: the GTF ramp stayed "top priority" through the $30bn Rockwell Collins deal [own] [P-0867][P-0263].
2. **The dividend.** Per share it was held at $1.90 in 2020, then raised every year to $2.48 (2024). Dividends were 105% of net income in 2023 [record] [P-1887][P-1888].
3. **Franchise support.** Customer compensation, MRO and spare-engine pools are funded [own] [P-0106][P-1558]. P&W capex rose from $700M (2021) to $1,025M (2023) [record] [P-1570][P-1597].
4. **Platform access.** Exclusivity assets reached $3.3bn, with $5.5bn more committed (2024) [record] [P-1750].
5. **Buybacks are the shock absorber.** $800M (2019), $47M (2020, suspended), $12.87bn (2023), $444M (2024) [record][own] [P-1883][P-1884][P-1892][P-1372]. "Share buyback is kind of the fill in" [own] [P-0566].
6. **The rating is sacrificed, then repaired.** S&P cut RTX to BBB+ in August 2023 (powder metal); the debt-funded October 2023 ASR then moved S&P and Moody's to negative outlook, and net debt reached 3.35x EBITDA (2023). Deleveraging came next [record][own] [P-1554][P-1884][P-1878][P-1362].

**R&D and capex through the cycle.** P&W E&D was about $1bn (2017) and R&D $1.1bn (2018, about 6% of revenue), "flattish ... until ... a brand new engine program" [own] [P-0217][P-0313][P-0377]; P&W capex peaked at $923M (2017) [record] [P-1442]. RTX group R&D was $3.19bn (2019), $2.69bn (2020) and $2.93bn (2024): 4.3% to 3.6% of sales [record] [P-1882][P-1885]. Development is the first discretionary cut [own] [P-0467][P-0398]; structural capex survives (the Asheville airfoil plant, launched in COVID) [own] [P-0427]. Recent money went to upgrades: commercial development rose about $0.1bn in each of 2023 and 2024 for GTF Advantage certification and powder-metal fixes, then fell [record][own] [P-1543][P-1575][P-0639][P-0671].

**Crisis behaviour.**

| Crisis | Cut | Raised or kept | Who paid | ids |
|---|---|---|---|---|
| GTF entry into service, 2016-19 | Buybacks (for Rockwell Collins, not the GTF) | E&D, the ramp, the dividend | P&W: about $100M (2016) and $196M (2017) of charges; customer financing of $975M (2017). Partners pro rata | P-0279, P-0273, P-1455, P-0196, P-0264 |
| COVID, 2020-21 | 10% of salaries; about 15,000 RTX commercial-aero jobs (Collins and P&W); E&D and capex | The dividend; Asheville; rate-63 capacity | Employees; $543M of unfavourable contract adjustments (including an impairment); buybacks suspended for 2020 | P-0393, P-0426, P-0432, P-1372, P-1883, P-0091, P-0443 |
| Powder metal, 2023-26 | Buybacks after the ASR | The dividend (+7%); the GTF Advantage; the upgrades | Partners 49%; airlines (partial compensation); creditors (BBB+) | P-1563, P-0110, P-1891, P-1554, P-0783 |

The pattern (inference): accrue the charge at once, pay it slowly, keep the franchise. Powder-metal cash was about $1.1bn in 2024, against $1.3bn planned [own] [P-0652][P-0616]. "Could that go out a little bit further? Perhaps" [own] [P-0657].

**Guidance behaviour.** Segment-profit guides start low and are beaten: 2021 guided -$125M to +$25M, GS adjusted +$61M; 2022 guided +$500-600M, GS adjusted +$763M (our subtraction) [own] [P-0447][P-0503] [record] [P-0040][P-0042]. Programme numbers start optimistic and slip a step at a time (§8 bias 2): 2018 negative engine margin ~$1.0bn to ~$1.2bn [own] [P-0215][P-0269][P-0300]; GTF cash breakeven "mid-2020s" to about 2027 [own] [P-0425][P-0506]. The unit loss is never quantified [own] [P-0584]. *Rule:* trust cash and segment guides; discount engine dates, ramps and costs by one revision.

**Funding capacity for a new engine today.** Cash is not the constraint (view): GS has RTX free cash flow of $8.14bn (2026E) to $9.80bn (2028E), leverage falling to 1.70x, R&D at 3.5% of sales with no new-engine step-up, and buybacks restarting at $3.0-4.5bn a year [analyst] [P-1964][P-1952][P-1954][P-1957]. Willingness is: "the outlook ... does not contemplate a new centerline engine"; only a sole-source selection makes sense; the loss-making OE model must be "revisited" [own] [P-0745][P-0746][P-1308][P-0774]. In game terms `gtf_next` is $4.5B P&W-net over 6 years (about $0.75B a year, a quarter of GS's 2026E buybacks, inference), `pw_wb` $6.0B over 7 years and `gtf_upgrade` $1.0B over 3 years [engine].

## 3. Operational behaviour

**Deliveries and ramp.** In the GTF's first two years deliveries ran at about 60-70% of plan: 138 against "just over 200" (2016, 69%) and 375 against the 600 planned in December 2015 (2017, 63%) [own] [P-0809][P-0812][P-0833][P-0795][P-0887]. Mature unit growth runs at 60-70% of plan: 14% against 20% (2024), 8-10% against 14% (2025) [own] [P-1064][P-1091][P-1119]. Capacity is disciplined: built for A320neo rate 65, committed to 63, no funding for a "3-year spike", 2-2.5 years to add forging and castings [own] [P-0918][P-0069][P-0079]. Bottlenecks get embedded staff, second sources, then insourcing [own] [P-0854][P-0997][P-1093][P-0670]; in 2022 P&W worked through a castings supplier's shortfall rather than switching, and missed about 70 Airbus engines in Q1 [own] [P-0988][P-0989].

**OE economics per engine** [analyst]:

| GS estimate | 2016 | 2017 | 2018 | 2019 | 2020 | 2024 | 2026E | 2028E |
|---|---|---|---|---|---|---|---|---|
| OE loss per GTF ($M) | 4.20 | 2.32 | 1.56 | 1.22 | 1.61 | 1.03 | 0.77 | 0.49 |

Sources: [P-1763][P-1769].

- **P&W's own figure agrees.** About $1.2bn lost on fewer than 800 engines in 2018, about $1.5M each [own] [P-0308].
- **The learning curve is 87%** [own] [P-0347]. Commercial OE dilution stayed at $0.7-1.05bn a year from 2016 to 2025E [analyst] [P-1764][P-1770].
- **OE never breaks even** [own] [P-1210][P-1217]. Net GTF EBIT breaks even only in 2027E, 11-12 years after entry into service [analyst] [P-1782].

**The aftermarket.** About 80% of GTFs went out on fleet-management plans, against about 40% historically, so P&W carries time-on-wing risk [own] [P-1121][P-0295]. Early visits were zero-margin warranty work and launch contracts "very aggressive", later "onerous", to be repriced at their 8-10 year expiry [own] [P-0364][P-0466][P-0433][P-0571]. The GTF aftermarket broke even in 2022, about 7 years after entry into service, and earned about 10% in 2024 against a mid-teens target; V2500 parity is expected "beyond 2025" (view) [own] [P-0579][P-0667][P-0478]. Ex-GTF aftermarket EBIT was $2,497M in 2019 [analyst] [P-1776].

**Durability record and crises.**

| Episode | Years | Cost and response | ids |
|---|---|---|---|
| GTF teething: combustor, #3 carbon seal, knife-edge seal (about $50M), blades | 2016-21 | $196M charge (2017) plus about $100M (2016) for engines diverted to spares. Warranty provisions went from $246M to $604M (UTC). Fleet campaigns took "about 2 years" each. Both "golden rules" were broken | P-0273, P-0279, P-0300, P-1418, P-1459, P-0895, P-1214 |
| Time on wing | 2022-23 | About half the V2500's. Block D doubled the removal interval; 60% of the fleet had it by mid-2023, with 90% expected within 2-3 years (view) | P-1014, P-0758 |
| Powder-metal recall | 2023-26 | $5.4bn gross, $2.9bn P&W-net. About 80% was compensation. About 1,200 visits pulled forward. Aircraft on ground: about 350 on average over 2024-26, a peak of 600-650. Airbus engines were allocated first | P-1563, P-0596, P-1035, P-1039, P-1074, P-1054 |

The answer every time was a fix-forward upgrade. The GTF Advantage had 2-3x the endurance testing and up to 2x time on wing. The Hot Section Plus kit carries 90-95% of those gains into the fleet from 2026, at a price [own][press/industry] [P-0779][P-1095][P-0785][P-0786][P-1363][P-1813].

**Slip and ramp priors for our own new engines** (inference from the record).

| Dimension | Record | Prior | ids |
|---|---|---|---|
| Derivative entry into service | GTF Advantage planned for 2024; certified 2025; 100% of output by end-2027 | +1.5-2 years | P-0753, P-0761, P-1817, P-1824 |
| Development length | "It takes 10 years to develop an engine" | The 6-year `dev_years` assumes mature technology | P-1269, P-0757 |
| Early volume | About 60-70% of plan in years 1-2 | Plan on two-thirds of early volume plans | P-0822, P-0887, P-0795 |
| Durability maturity | About 1M fleet hours to surface issues; about 2 years per campaign | 2-3 retrofit campaigns in years 1-5 | P-0847, P-0895 |
| Value maturity | OE loss from $4.2M to $1.2M in 3 years (2016-19); aftermarket breakeven at 7 years | ramp start_frac -0.35 over 10 years [engine] | P-1763, P-0579, P-0478 |
| Quality escape at volume | The powder contamination came from ramp-driven capacity | The `gtf_durability_crisis` inject is realistic | P-1040, P-1062 |

## 4. Engine-programme doctrine

**The launch tests.** P&W asks four questions: development cost, aircraft volume, the number of engine suppliers, and the aftermarket profile [own] [P-0703][P-0714].
- **The bar is the GTF's.** "This next engine has to pass that same threshold", and the board sets it [own] [P-0715][P-0731]. Below the cost of capital, "buy stock back" [own] [P-1165].
- **Sole source is a condition.** "We will not compete if it's a 2-engine competition" [own] [P-0737]. Dual source means "big discounts" [own] [P-0698]. Rolls-Royce held the same view [own] [P-2070].
- **The launch customer is the airframer's commitment.** "Just like they're not committing to it ... we're not going to commit" [own] [P-0711]. Spending stays minimal while P&W waits [own] [P-0739].
- **The exception is defending the franchise.** On the A320neo, P&W committed on its own readiness [rival] [P-1868]. It accepted dual source at 46% and an entry price as "a price of entry" [press/industry][own] [P-1993][P-0707]. "If you miss a cycle ... you get shut out ... for decades" [own] [P-1347].
- **The rule is asymmetric (inference).** On offence, onto Boeing, P&W demands sole source and a GTF-level return. On defence, an NGSA replacing the A320neo justifies an early commitment.

**Technology gates.**
- **Durability first:** finish durability testing before entry into service [own] [P-1214], with 2-3x the endurance testing [own] [P-0779][P-1095], trading fuel burn for durability [own] [P-1344][P-1348].
- **Evolve inside the geared architecture:** a composite fan, a CMC hot section, a new gear [own] [P-0790][P-0772]; the open fan is "a long time from now" [own] [P-0104]; enabling technology is funded without a launch commitment [own] [P-0757].
- **Ambition gets cut.** The 2019 plan for a 20-25% overall fuel-efficiency gain by 2025 (baseline not stated) became the GTF Advantage, about 1% better than the existing GTF [press/industry][own] [P-1828][P-1602].

**Segments.**
- **Narrowbody.** P&W pushes the A321 and A321XLR [own] [P-1250]. It bids only where it has "a clear market lead or a clear technology lead" [own] [P-1196].
- **Widebody: no.** "Narrow-body focused" [own] [P-1313]. It passed on the 787, which UTC's CEO later called under-investment [own] [P-1125]. Its only widebody, the GP7000, was a 50/50 Joint Venture with GE with 40% of products laid off [record] [P-1700], now out of production [record] [P-1934]. A 2019 plan for a 70-100k lb GTF-derived engine appears in no later source (inference: never executed) [press/industry] [P-1842].

**Partnerships.** Never alone, always in charge: partners take 13-49% of each programme and none holds more than 25%; P&W keeps 51% of the A320neo GTF [record] [P-1714][P-1744][P-1747]. Partners pay for defects (49% of powder metal) [record][own] [P-1563][P-1324]. In 2012 P&W bought RR's 32.5% of IAE for $1.5bn per the 2019 brief (RR reported £1.5bn received) plus flight-hour payments to June 2027 [press/industry][rival][record] [P-1838][P-1874][P-1398]; the P&W-RR midsize Joint Venture announced with it was still awaiting approval in July 2012 and no later source mentions it [rival] [P-1870]. The only equal partnership with a rival is the Engine Alliance with GE [record] [P-1692][P-1676].

**Pricing.** The OE loss buys the aftermarket: "we sell it because we know we're going to have aftermarket for 30 years" [own] [P-1143]. Launch mode priced as "a price of entry", then the A320neo price was raised once secure [own] [P-0707][P-0696]; "we don't feel the need to do those kind of deals anymore", and P&W walked from IndiGo on price [own] [P-0735][P-0081]. It pushed for share in 2020 [own] [P-0086] but is "not in the ... launch phase" (2024) [own] [P-1333]. The real concession channel is exclusivity payments to airframers, tied to future sales or flight hours [record] [P-1524][P-1750].

**What makes it wait:** an uncommitted airframer [own] [P-0711]; a harvest phase [own] [P-1234]; GTF recovery as the priority [own] [P-0788]; a late NGSA that lengthens the GTF run [own] [P-1312][P-2058].

## 5. Reaction function

Lags marked (inference) have no dated pair of events behind them.

| # | If … | We historically… | Typical lag | Strength | Analogues | Evidence ids |
|---|---|---|---|---|---|---|
| 1 | An airframer launches a new narrowbody and runs an engine competition | Bid only for sole source, against a board-set hurdle, about half partnered out. Without a business case, match non-commitment and fund only enabling technology. Defend the franchise early | Tied to the airframer's: on the NMA ours slipped from mid-2018 to after early 2019; the NMA never launched | strong | NMA 2016-19; A320neo 2010-12 | P-0737, P-0746, P-0698, P-0731, P-0713, P-0711, P-0739, P-0757, P-1868, P-1347, P-0125, P-2020 |
| 2 | An airframer launches a widebody Re-engine | Abstain: "narrow-body focused"; widebody only inside a 50/50 Joint Venture. Passed on the 787, later called under-investment | none | strong | 787; A380 GP7000 JV | P-1313, P-1700, P-1676, P-1125, P-1842 |
| 3 | An airframer or airline selects a rival engine | Let it go rather than match price; accept 40-50%; win back on product. Claimed 56% of selections Jun 2017-Jun 2018 [own], against LEAP's almost 10:1 lead in 2017 orders [press/industry] (not reconciled) | 12-18 months (inference) | strong | IndiGo 2019; LEAP 2017 | P-0081, P-2071, P-0074, P-1292, P-0075, P-1847 |
| 4 | An airframer asks for price concessions or compensation | No deep discounts past launch; share cost-outs, not margin; pay when at fault; buy positions with exclusivity payments. UTC group, by analogy (inference): cost-downs for volume guarantees (PFS 2.0); walk from a loss with no aftermarket | months (inference) | strong | SCOPE+; 2017 diversion charge; PFS 2.0 (UTC) | P-0735, P-1333, P-0127, P-2008, P-1207, P-0273, P-0144, P-1524, P-2017, P-0148 |
| 5 | A rival engine maker stumbles | Take the platform when a rival's programme fails (Falcon 6X, after Safran's Silvercrest). In Oct 2020 said it would keep gaining share (43% to about 55% over 2019-20, mostly pre-COVID) [own]; "rivals weakened" was an analyst's premise [analyst] | 1-2 years (inference) | moderate | Falcon 6X | P-2006, P-1827, P-0086, P-1974 |
| 6 | A rival engine maker wins big or out-innovates | Answer with incremental product, never price: fix durability, then the GTF Advantage; upgrade over clean sheet. Reuse the GTF core to displace rivals (PW800 over RR at Gulfstream, a competitive win) | 1-3 years (inference) | strong | LEAP 2017; RISE; F135; PW800 | P-1847, P-0075, P-0114, P-0104, P-1302, P-1298, P-0064, P-0089 |
| 7 | Our own durability crisis | Divert output to spares, take a one-off charge, compensate within the provision, push 49% to partners, expand MRO, fix forward and charge for the kit. Claimed about 40% share in Feb 2024 and aimed to hold it (view) | Weeks to divert; a quarter for the charge; 2-3 years for the upgrade | strong | 2016-18 seals; 2023 powder metal | P-0273, P-0144, P-1563, P-0596, P-0643, P-0109, P-0758, P-0786, P-1363, P-0111 |
| 8 | A demand shock (COVID) | Cut E&D and capex; RTX cut about 20% of commercial-aero staff (Collins and P&W). Suspend buybacks, hold the dividend. Keep rate-63 capacity and suppliers warm. Retrofit in idle shops | Within the quarter | strong | COVID 2020 | P-0467, P-0398, P-0426, P-0423, P-0405, P-1372, P-1883, P-1924, P-0091, P-0092, P-0940, P-0941 |
| 9 | An airframer's quality or rate problems | Plan on the airframer's revised numbers; add no capacity to exploit a grounding; haircut rate ambitions to 63-65; keep supply warm through a strike. UTC group (Collins MAX content, analogy): grounding treated as temporary | 2-2.5 years for capacity | strong | 737 MAX 2019; Airbus rate 75 | P-0079, P-0069, P-2047, P-2021, P-0168, P-1936, P-1937 |
| 10 | A technology slip | Slip quietly, add testing, do not cancel. Carry launch customers' slips | About 1 year per slip (GTF Advantage) | moderate | GTF Advantage; CSeries, MRJ | P-0753, P-0761, P-0785, P-0779, P-0128, P-1371 |
| 11 | A supply-chain crunch | Second-source, embed staff, insource. Worked through a castings supplier's shortfall rather than switch (2022). Airbus OE first in powder metal, then a steady OE/spares mix; wider rationing is inference. Compete with CFM for castings [customer] | 6-12 months (inference); 2-2.5 years for capacity | moderate | Fan blades 2016; castings 2022-25 | P-0817, P-0997, P-0989, P-0670, P-1054, P-0162, P-1113, P-1120, P-1867 |
| 12 | A partner proposes a Joint Venture | Share risk and investment, never our technology. Lead every collaboration except the 50/50 Engine Alliance. The 2012 RR JV left no trace after July 2012 (inference: lapsed). Went alone when the partner had no business case | Years (inference) | moderate | Engine Alliance; IAE; 2012 JV | P-1233, P-1240, P-1676, P-1744, P-1870, P-1874, P-1868, P-1875 |
| 13 | An airframer cancels or pauses our programme | Stand by the customer, formalise the pause, run a finished engine for its aftermarket | Months (inference) | moderate | CSeries, SpaceJet, A380 | P-1371, P-1939, P-1934 |
| 14 | An airframer pushes into the aftermarket | Threaten to reprice OE; defend with proprietary parts and fleet plans | 1-2 years (inference) | moderate | Boeing and Airbus services | P-1194, P-0147, P-0134, P-1135 |

**5a. Orders by row** [engine] (run calib, turn 1; re-run every turn).
1. Launch `gtf_next` (standard terms, the turn's last year) in the turn an airframer discloses NGSA or fps on `pw_gtf2`, or under the §6 NGSA hedge. With the upgrade in 2026 the last year wins even if NGSA launches in 2026 (+2.56, against +2.46 for 2027 and +1.66 for 2026), and the wait costs Airbus nothing (+39.42 against +36.85).
2. Do Nothing on `pw_wb` (-3.65 at best). 3. No chase; cancel an unflown `gtf_next`; fund `gtf_upgrade`. 4. Stay `standard`. 5. Disclose a `gtf_next` offer to an airframer waiting on UltraFan [P-2006]. 6. The upgrade, not terms. 7. Under `gtf_durability_crisis`, commit `gtf_upgrade`; standard terms [P-0074]; no `pw_wb`. 8. Keep a committed `gtf_next`; defer an uncommitted launch unless an airframer has disclosed. 9. No order. 10. No cancel while an airframe flies the engine (each extra year costs 10% of capex). 11. Strain +50%: with the upgrade started in 2026, a turn-1 `gtf_next` only into a disclosure, otherwise turn 2 (2029 or later). 12. The §6 `join_rr_jv` test. 13. Cancel `gtf_next` with its airframe. 14. No lever.

## 6. Lever-by-lever playbook

**Engine reference points** [engine] (`whatif`, turn 1, run calib, P&W delta PV in $B; airframes and our launches in 2028 unless stated):

| Case | ΔPV |
|---|---|
| `gtf_upgrade` alone in 2026 / 2029 / 2032 | +1.76 / +1.37 / +1.06 |
| NGSA on CFM or RR's solo UltraFan, we Do Nothing / with upgrade | -3.11 / -1.74 |
| NGSA on `pw_gtf2`: standard / plus upgrade 2026 / aggressive / aggressive plus upgrade | +0.96 / +1.98 / -3.66 / -2.63 |
| `gtf_next` unselected, cancelled in turn 2: alone / plus upgrade, nobody launches / plus upgrade, NGSA on CFM; alone, never cancelled | -0.86 / +0.56 / -2.94; -4.25 |
| fps on `pw_gtf2` / on CFM; with upgrade | +1.65 / -0.64; +2.98 / +1.04 |
| Both launch, plus upgrade: fps ours, NGSA CFM / NGSA ours, fps CFM / both ours | -2.05 / +0.09 / +4.37 |
| Upgrade in 2026, then NGSA and `gtf_next` both in 2029 (turn 2) | +2.13 |
| RR `jv_pw` plus `join_rr_jv`: NGSA on UltraFan / fps on UltraFan / no selection | +13.71 / +11.02 / -3.54 |
| Same plus upgrade: NGSA on UltraFan / nobody launches / NGSA on CFM / RR cancels in turn 2 | +14.91 / -1.95 / -5.45 / +0.87 |
| Join plus `gtf_next` plus upgrade: NGSA on UltraFan / on ours | +9.61 / -2.44 |
| `pw_wb` on 787 Re-engine / A350 Re-engine | -3.65 / -4.10 |

**Airframer incentives** [engine]. `options` (2026 launches): `airframer_incentive_b` for `pw_gtf2` of fps +0.71 and NGSA +2.20 on standard terms, +3.74 and +8.16 on aggressive. `whatif` (2028 launches), against CFM: Airbus +1.75 for ours, +4.02 for UltraFan, +6.73 for ours on aggressive; Boeing +0.48, +1.58, +2.91.

### `gtf_upgrade`: default ON in turn 1

Positive in every turn-1 scenario [engine], and P&W's answer to every durability problem: the V2500 Select, Block D, Hot Section Plus [own] [P-0720][P-0758][P-0786]; "time on wing ... is the name of the game" [own] [P-1355]. Commit in 2026 and put any `gtf_next` in 2028: strain $0.34B, against $1.12B if both start in 2026. The engine charges strain on any two overlapping P&W windows, though the `rules` text names only narrowbody-plus-widebody overlaps [engine]. Price the kit [own] [P-1363].

### `gtf_next`: default OFF until an airframer discloses; then launch in the same turn

**Why a hedge is a bet** [engine]. Orders are simultaneous: an airframer naming `pw_gtf2` in a turn we do not launch falls back to CFM for good, at no cost to it. Break-even odds p* = cost / (cost + gain):
- NGSA, upgrade in 2026: cost 1.76 - 0.56 = 1.20 (0.86 capex, 0.34 strain); gain 1.98 + 1.74 = 3.72; p* = 1.20 / 4.92 ≈ 0.24, about 1 in 4.
- NGSA without the upgrade overlap (as from turn 2): p* = 0.86 / (0.86 + 0.96 + 3.11) ≈ 0.17, about 1 in 6.
- fps, upgrade in 2026: p* = 1.20 / (1.20 + 2.98 - 1.04) ≈ 0.38, about 2 in 5 (0.27 without the overlap).

**Estimating p** (inference) = P(launch this turn) × P(names `pw_gtf2`). Airbus earns +46.47 from NGSA in 2028, +42.05 in 2029, +34.65 in 2026; Boeing +19.09 from fps in 2028, +16.72 in 2029, +13.50 in 2026 [engine]: take 0.7 for a turn-1 launch unless statements point later (2028 fits our mid-2030s view of NGSA [own] [P-2058]). UltraFan also falls back free and pays Airbus +4.02 against our +1.75, so Airbus names us only if it rates our launch 2.3 times as likely as RR's (Boeing: 3.3 times): take 0.3 with RR in play and no disclosures, 0.7 without RR. Turn-1 NGSA default: about 0.2 with RR, 0.5 without.

**Flip ON when either holds:** (1) an airframer has disclosed NGSA or fps on `pw_gtf2` for this turn, `airframer_incentive_b` > 0 on standard terms and `whatif(launch, selected)` beats `whatif(no launch)`; (2) NGSA only, the franchise exception [own] [P-1347]: p ≥ about 0.45 with the upgrade overlap, 0.38 without (break-even plus the $1B doctrine allowance, §9 step 8). fps gets no hedge.

Launch in the turn's last year on standard terms; disclose "gtf_next committed on standard terms; ready six years from launch" [engine]. Otherwise wait, as on the NMA [own] [P-0711], and disclose: "P&W will launch `gtf_next`, sole source, standard terms, in any turn for which an airframer discloses NGSA or fps on `pw_gtf2`" [engine]. **Never** launch for "bragging rights" [own] [P-0702], race to an entry into service before 2035 [own] [P-1312], pair it with `pw_wb`, or aim it at an airframer already disclosed on UltraFan.

### `terms`: default standard

Flip to aggressive only when `whatif(aggressive, selected)` beats `whatif(standard, not selected)` and the airframer's standard-terms incentive is below 0 or below UltraFan's. Inactive at calibration: NGSA -3.66 against -3.11, fps -1.75 against -0.64, with the upgrade -2.63 against -1.74 [engine]. Precedents: "not in ... the launch phase"; "revisit" the OE-loss model [own] [P-1333][P-0735][P-1308][P-0774].

### `join_rr_jv`: a free conditional option; default OFF

- **Mechanics** [engine]. Costs 0 unless RR launches `uf_nb` as `jv_pw` that turn, which needs our flag. Once joined we cannot leave: `validate` rejects our `cancel: ["uf_nb"]`.
- **Break-even** (inference). Given `jv_pw`, with the upgrade: +16.64 if NGSA picks UltraFan (+14.91 against -1.74), -3.71 if nobody does (-1.95 against +1.76; -5.45 against -1.74). p* = 3.71 / 20.36 ≈ 0.18; with the $1B allowance, about 0.23.
- **Adverse selection** (inference). RR earns +23.90 solo against +11.79 in the Joint Venture if NGSA picks UltraFan, and -7.59 against -3.96 if not [engine], so it offers `jv_pw` only if it rates its own odds below about 23%. Raise our estimate only on an airframer's signal.
- **For:** "you spread risk, you spread investment through JVs" [own] [P-1233], and joining shares RR's technology, not ours (inference); P&W co-owned engines with GE and with RR (IAE, to 2012) [record][press/industry] [P-1676][P-1744][P-1838]; RR wants a partner "to derisk" [rival] [P-2001]. In 2012 RR saw a P&W Joint Venture as its route back to the narrowbody [rival] [P-1872]; whether that still holds is an inference, since RR now talks to every partner and does not need one for capability [rival] [P-2004].
- **Against:** integrated products need integrated teams [own] [P-1240]; the 2012 Joint Venture left no trace after July 2012 (inference) [rival] [P-1874]; RR claims favourable geared IP [rival] [P-2004].
- **Flip ON when all hold:** P(an airframer selects UltraFan this turn | `jv_pw`) ≥ about 0.23; no `gtf_next` aimed at that airframer unless `whatif` favours the pair; `whatif(join, UltraFan selected)` beats staying out. Turn 1 has no RR disclosure: default OFF; disclose "P&W would join a 50/50 UltraFan narrowbody Joint Venture in any turn for which an airframer discloses UltraFan", so a turn-2 Joint Venture can form.
- **Note (inference).** Our half is booked at RR's $3.1M per engine on RR's ramp: a model asymmetry, but the live payoff.

### `pw_wb`: default never; inactive at calibration

Flip only if a Re-engine is launched or disclosed on `pw_wb_new`, `airframer_incentive_b` > 0, `whatif` ≥ +$1.5B after strain (inference threshold) and no narrowbody programme is in development (`gtf_upgrade` counts). In turn 1 the best case is -3.56 (`options` R4) [engine] [P-1313][P-1700].

### Cancel and Do Nothing

- **Cancel** `gtf_next` at the first turn no airframe flies it and none has disclosed it will. Holding it costs about $0.75B a year nominal, about $1.0B alpha-loaded; one year then cancelled is -0.86 PV [engine]. P&W stands by a customer still flying the engine and formalises pauses [own] [P-1371][P-0128][P-1939]. RTX's CEO ended a failing fixed-price defence programme, an analogy only (inference) [own] [P-1342].
- **Do Nothing** is the quiet-turn default; enabling technology is funded off the board [own] [P-0757].

## 7. How we read the airframers and rivals

**Airbus: the franchise customer.** 30-48% of P&W sales (48% only in 2023) [record] [P-1927][P-1380][P-1386][P-1392]. Expect rate asks above what we fund [own] [P-2047][P-0092], unrelenting cost-downs (SCOPE+) [own] [P-2008], allocation shifted to CFM when we were constrained [analyst] [P-1973], and pragmatism in our crises [own] [P-0145]. We assume NGSA in the mid-2030s (view) [own] [P-2058]. *Discount rule:* haircut Airbus rate targets to 63-65 [own] [P-2047]. *In the game:* NGSA defaults to CFM, and Airbus prefers UltraFan to our engine (§6), so it needs a disclosed commitment from us (inference).

**Boeing: the customer we want back.** We sell it no commercial engines [own] [P-0697]. It is hard on price: PFS 2.0 tied programme access to cost-downs (UTC group), and on the NMA it set "tough cost targets" [own] [P-2014][P-2017][P-2020][P-0125]. Its execution is volatile (MAX grounding; 737 rates doubted, then cut) [own] [P-2021][P-2053]. Its CEO: rates "boil down to engines and the competition for castings between Pratt and CFM" [customer] [P-1867]. *Discount rule (inference):* treat Boeing's launch hints as negotiation. *In the game:* an fps win adds value only if NGSA is not lost to `cfm_ducted` or UltraFan in the same turn (fps ours with NGSA on either: -2.05, against -1.74 for losing both; with NGSA on the open fan, which waits to 2045, +1.50 against +0.48) [engine]; answer NGSA first (inference). Delay Tactics and certification scrutiny slip our value with the airframe [engine].

**CFM/GE: the default and main rival.** Sole source on the 737 MAX [press/industry] [P-1994]; wins on price and guarantees [own] [P-2071][P-1949]; LEAP 54% to GTF 46% on the A320neo in 2016 [press/industry] [P-1993]. *In the game:* `cfm_ducted` is every narrowbody's fallback and wins unless the airframer is positively incentivised to pick ours; our "CFM" numbers are for it [engine]. The open fan (`cfm_open_fan`) cannot enter service before 2045, and an airframe ready earlier waits at 10% of capex a year, so neither airframer prefers it to `cfm_ducted` in any launch year we ran, 2026-2037 (2028: Airbus -7.67 against +46.47, Boeing -21.48 against +19.09; 2037: +14.49 against +16.65, +2.75 against +4.67) [engine].

**Rolls-Royce: ex-partner, would-be partner, rival.** It left IAE lacking resources for a fourth new engine and a business case for the A320neo [rival] [P-2000][P-1868]. We pay it per V2500 flight hour until 2027 [record] [P-1398] and displaced it at Gulfstream [own] [P-0064]. It wants a narrowbody partner to derisk, brings its own IP and is building a demonstrator alone [rival] [P-2001][P-2004][P-2003][P-2005]. *Discount rule (inference):* "we don't need partnership for capability" is posture, and its resource limits suggest it needs our capital; but a `jv_pw` offer also signals that RR rates its own selection odds low (§6).

## 8. Biases and failure modes (display only when the situation matches)

1. **Durability optimism at entry into service.** *When:* disclosing `gtf_next`, or after `gtf_next_test_setback`. "Behind us" and "a thing of the past" were each followed by new problems [own] [P-0810][P-0812][P-0814][P-0878][P-0883]; "there's not a surprise coming" preceded the $5.4bn charge [own] [P-0582][P-1563]. *Failure mode:* promising an early entry into service.
2. **Reaffirm, then cut.** *When:* a crisis inject lands. Deliveries 200 to about 150; negative engine margin ~$1.0bn to ~$1.2bn; powder-metal cash $0.5bn to $3bn [own] [P-0812][P-0814][P-0300][P-0588][P-0594].
3. **Buy entry, harvest later.** *When:* tempted by `aggressive`. Launch pricing and onerous contracts dragged margins for a decade [own] [P-0707][P-0466][P-0433]; we now want the OE model revisited [own] [P-1308].
4. **Incumbent protection.** *When:* NGSA or fps is signalled. Upgrade over clean sheet; no centreline engine in plan; a late NGSA welcomed [own] [P-1298][P-1302][P-0745][P-1312]. *Self-recognised failure:* the 2000s harvest that cost the 787 [own] [P-1125][P-1139]; in the game, missing NGSA costs -3.11 [engine].
5. **Capacity conservatism.** *When:* a rival or airframer stumbles. No capacity for spikes, no gain from the MAX grounding, then short of Airbus's needs [own] [P-0069][P-0079][P-0165].
6. **Technology possessiveness.** *When:* RR offers `jv_pw` [own] [P-1233][P-1240]. *Failure mode:* reading "you don't share technologies" as "never join", and refusing a Joint Venture the payoff favours.
7. **Parent-first capital allocation.** *When:* after a crisis or demand-shock inject. Dividend "sacrosanct"; a $10bn buyback in the charge year; E&D cut first [own] [P-0423][P-0602][P-0467]. *Failure mode:* under-funding the decisive cycle [own] [P-1347].
8. **Allegiance flips under stress.** *When:* our durability crisis. Airlines first in 2017, Airbus first in 2023-24 [own] [P-0144][P-0159][P-0162].
9. **Self-serving attribution.** *When:* a selection is lost. IndiGo was "all about price" [own] [P-0081]. *Failure mode:* reading a durability loss as price and funding `gtf_upgrade` late.

## 9. Decision procedure for each turn

1. **Read the board.** `brief --run <RUN> --side pratt_whitney` (plus `rules` in turn 1): airframe programmes with engines and launch years; supplier programmes, including any `uf_nb` and its variant; injects; disclosures and statements.
2. **Match triggers** in §5 and read their 5a orders.
3. **Run the finance team.** Use `options --compact` only for `airframer_incentive_b`: it launches in the turn's first year, never cancels and has no Joint Venture option, so it overstates hedge risk (R8 "ngsa with cfm_ducted" -8.56 against -2.94 for a 2028 hedge cancelled in turn 2). Decide on `whatif`: likely airframe launches with and without `gtf_next` (turn's last year) and the turn-2 cancel; `gtf_upgrade` on and off; if RR plays, `jv_pw` with our join, NGSA on UltraFan, on CFM or not launched.
4. **Upgrade.** If `gtf_upgrade` is not committed, commit it now (+1.76 in turn 1, +1.37 in turn 2 [engine]).
5. **Narrowbody.** Launch `gtf_next` when the §6 flip holds: a disclosure, or for NGSA the odds test. Disclose the commitment or the conditional offer.
6. **Joint Venture.** `join_rr_jv` only when the §6 test holds: free unless RR launches `jv_pw`, irreversible once it does.
7. **Terms, widebody, cancel.** Standard terms and no `pw_wb` unless the §6 tests hold; cancel `gtf_next` if no airframe flies it and none has disclosed it will.
8. **Weigh delta PV against doctrine.**
   - Score each candidate order by expected PV, Σ p(scenario) × `whatif`(scenario), using the probabilities behind your `prediction`.
   - Red lines are never traded for PV, and you declare what they cost: no `gtf_next` without a disclosed airframer except the NGSA hedge; no `aggressive` or `pw_wb` unless the §6 tests hold; never share our core technology (joining UltraFan does not); no dividend cut.
   - Otherwise take the best expected PV, keeping a doctrine-favoured order (no launch, stay out, standard terms) only while it trails by $1B or less. The §6 hedge and Joint Venture thresholds already include this allowance.
   - Doctrine premium = best expected PV minus the chosen order's; `expected_delta_pv_b` = the chosen order's expected PV.
9. **Speak in our voice.** Public statement: disciplined, sole source, durability first, "deliver financial returns, not just bragging rights" [P-0702][P-1348]. `disclose` the §6 offers. `prediction`: launch years from the airframers' `whatif` timing payoffs (2028 unless statements point later; [P-2058][P-1312] only bound the entry into service) and the engine your odds make likeliest (CFM absent a disclosure). Give every launch `year` and `terms`: `validate` silently sets a missing year to 2026 (NGSA plus upgrade: +0.45, not +1.98). Then `validate`.

## 10. Confidence and gaps

- **Strong:** pricing discipline, sole source, crisis handling, capital allocation and GTF unit economics: own words over 2015-25 agree with filings and the GS model.
- **Thin or one-sided:**
  - **The P&W-RR UltraFan Joint Venture.** No P&W statement beyond a 2024 non-answer; RR's side comes only from RR's words; the 2012 JV's fate is silence (inference) [P-1874][P-2004].
  - **Selection odds.** No evidence on how an airframer would choose between our engine and UltraFan; the §6 odds are inference from engine payoffs.
  - **Widebody.** The only plan is a 2019 industry report [P-1842].
  - **The hurdle rate.** Inferred from 2017-19 statements; no explicit IRR after 2019 [P-1243][P-0746].
  - **Per-engine aftermarket economics.** GS plugs (a 35% margin) not reconciled to its segment model; aftermarket margin is the largest uncertainty in our payoff (calibration memo) [P-1754][P-1789].
  - **Strain.** PLACEHOLDER: no evidence isolates overlap cost [P-0279][P-1234].
- **Dated:** the 2019 industry brief, and NMA-era (2016-19) launch doctrine applied to a 2026+ NGSA.
- **Scale:** the game's A320neo engine flow is about 2x real installs, so absolute payoffs are about 1.7-2x evidence scale (calibration memo) [P-1771].
