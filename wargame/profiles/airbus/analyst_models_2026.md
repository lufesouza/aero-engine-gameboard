# Airbus: 2026 analyst-model baseline

This note sums up two bank company models of Airbus: Morgan Stanley (MS, model dated 14 Aug 2026) and Goldman Sachs (GS, published 26 Aug 2026). The source data holds only these two models and no consensus file, so there are no consensus figures here. Money is in EUR millions (m) unless stated; dividends per share (DPS) and price targets are in EUR per share; deliveries are in aircraft and production rates in aircraft per month. The year ends 31 December. "A" means actual, "E" means bank estimate. GS carries no actual/estimate labels, so 2025 and earlier are treated as actual. MS forecasts stop at 2030E and GS at 2031E. Tags read [bank, sheet, row]. **The game's board numbers govern the payoff. This note is real-world context only.**

## Balance sheet and cash

Airbus shows net cash in every year of the MS record (2010A-2030E), from 11,918m in 2010 [MS Valuation Summary r56 'Net Debt / (Cash)'; the model shows net cash as a negative number]. Covid cut it to 4,312m in 2020 [MS CFS r86]. Both banks see it growing fast to 2030E (table below); that the delivery-rate ramp drives this is (inference).

| Year | Net cash, MS | Net cash, GS | Free cash flow, MS | Free cash flow, GS |
|---|---|---|---|---|
| 2019A | 12,534 | 12,534 | 3,509 | 3,509 |
| 2020A | 4,312 | 4,312 | -6,935 | -6,935 |
| 2023A | 10,726 | 10,726 | 4,387 | 4,532 |
| 2024A | 11,753 | 11,753 | 4,463 | 4,463 |
| 2025A | 12,171 | 12,171 | 4,574 | 4,812 |
| 2026E | 14,013 | 14,247 | 4,997 | 4,718 |
| 2027E | 16,441 | 16,271 | 6,600 | 6,642 |
| 2028E | 20,840 | 19,590 | 9,062 | 8,524 |
| 2029E | 25,321 | 26,112 | 9,849 | 10,537 |
| 2030E | 31,830 | 33,062 | 10,717 | 11,565 |
| 2031E | n/a | 38,198 | n/a | 10,476 |

Sources: [MS CFS r86 'Reported net cash'], [GS Balance Sheet r65 '(Net Debt)/Net cash'], [MS CFS r61 'FCF before M&A and Customer Financing'], [GS Cash Flow Statement r89 'FCF excluding the impact of customer financing']. Free cash flow is before customer financing; the MS line is also before M&A and is labelled "old def" in the model (Airbus's headline definition, equal to the new definition before customer financing from 2024). Caveat: the two banks report different actuals for the same definition family in 2023 (4,387 vs 4,532m) and 2025 (4,574 vs 4,812m).

- **Leverage.** Net cash runs at 1.18x adjusted EBITDA in 2025A and 1.74x in 2030E [MS Valuation Summary r57].
- **Gross debt is held flat.** MS keeps total debt at 14,249m from 2025A to 2030E; the 2020 peak was 17,095m [MS BS r211]. GS keeps short-term debt at 5,186m and pays long-term debt down from 9,063m (2025A) to 7,253m (2031E) [GS Balance Sheet r63-64]. Government launch aid (refundable advances, 3,620m in 2025A) is not counted as debt [MS BS r212].
- **Liquidity.** Gross cash and securities rise from 27,218m (2025A) to 46,879m (2030E) [MS CFS r82].
- **Cash is seasonal.** Net cash falls mid-year: 6,953m at 1H25, 9,849m at 1Q26, 8,360m at 1H26 [MS CFS r86, quarterly]. Free cash flow was -1,166m in H1 2026 (Q1 -2,485m, Q2 +1,319m) [MS CFS r61; GS Interims r154]. Caveat: MS does not label its 2026 quarters; they are treated as actual because they match GS actuals.
- **2026 is back-loaded.** The full-year forecast needs H2 2026 free cash flow of 6,163m [MS CFS r61, second-half 2026 estimate column] or 5,884m [GS Interims r154].

**Shareholder returns.**

| | 2025A | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|---|
| DPS, MS (EUR) [MS BS r261] | 3.20 | 3.07 | 3.72 | 4.66 | 5.12 | 5.47 |
| DPS, GS (EUR) [GS Income Statement r117] | 3.20 | 3.45 | 4.27 | 5.40 | 6.19 | 7.15 |
| Buybacks, MS [MS IS r75] | n/a | 500 | 1,500 | 1,500 | 1,500 | 0 |
| Buybacks, GS [GS Cash Flow Statement r101] | 0 | 1,000 | 2,000 | 2,000 | 0 | 0 |
| Total cash to shareholders, MS [MS CFS r34] | 2,372 | 3,015 | 3,897 | 4,388 | 5,093 | 3,934 |
| Dividends paid, GS [GS Cash Flow Statement r100] | 2,374 | 2,527 | 2,703 | 3,301 | 4,119 | 4,726 |

MS assumes a 40% payout of clean earnings per share [MS BS r262]. GS assumes 47%, rising to 50% from 2030 [GS Income Statement r118]. Airbus paid no dividend for 2019 and 2020 (Covid) [MS BS r261]. GS DPS for 2018-2020 looks shifted by a year, so only 2021 onward is used [GS Income Statement r117]. Caveat: the MS "total cash to shareholders" row is dividends plus buybacks paid in the year, while the GS row is dividends only, so the two rows are not like for like [MS CFS r34; GS Cash Flow Statement r100].

## The business

**Airbus Commercial (the aircraft business).** Margins are adjusted EBIT over revenue.

| Year | Revenue, MS | Adj. EBIT, MS (margin) | Revenue, GS | Adj. EBIT, GS (margin) |
|---|---|---|---|---|
| 2019A | 54,775 | 6,358 (11.6%) | 54,775 | 6,358 |
| 2020A | 34,250 | 618 (1.8%) | 34,250 | 618 |
| 2025A | 52,577 | 5,470 (10.4%) | 52,577 | 5,470 |
| 2026E | 58,339 | 5,918 (10.1%) | 57,946 | 5,758 (9.9%) |
| 2027E | 66,233 | 7,313 (11.0%) | 67,785 | 7,168 (10.6%) |
| 2028E | 73,145 | 9,368 (12.8%) | 77,836 | 9,292 (11.9%) |
| 2029E | 76,371 | 10,186 (13.3%) | 84,850 | 10,716 (12.6%) |
| 2030E | 78,629 | 10,793 (13.7%) | 88,711 | 11,317 (12.8%) |
| 2031E | n/a | n/a | 91,335 | 11,677 |

Sources: [MS Airbus r11, r45, r46], [GS Airbus Commercial r2, r4, r5]. The GS EBIT row is labelled 'Company defined EBIT' and equals its underlying EBIT before one-offs.

- **Group.** Revenue goes from 73,420m (2025A) to 105,534m (2030E) [MS IS r8]. Adjusted EBIT goes from 7,128m to 13,574m [MS Valuation Summary r17].
- **2026 started weak.** Commercial adjusted EBIT was only 81m in Q1 2026 (about 1% margin) and 1,987m for H1 [GS Interims r116].
- **MS range for 2028E (bear / base / bull).** Commercial revenue 69,980 / 73,145 / 77,895m; adjusted EBIT 7,698 / 9,368 / 11,684m; margin 11.0% / 12.8% / 15.0% [MS Bull Bear Base r4, r15, r16].
- **Narrowbody carries the business.** New-aircraft narrowbody revenue (A220 plus A320neo family) was 34,377m in 2025A, 65% of Commercial revenue. Widebody (A330 plus A350) was 12,417m, 24%. By 2030E it is 48,814m vs 21,839m (62% vs 28%) as A350 rates climb [MS Airbus r311-312, r315-316].
- **Aftermarket vs new aircraft.** The extract has no services or aftermarket revenue line, so this split cannot be given.
- **A220 is still loss-making.** GS EBIT: -232m (2025A), -161m (2026E), -54m (2027E), then +99m (2028E) and +511m (2030E) [GS Airbus Commercial r157]. MS takes A220 gross margin from -12.5% (2025) to 0% (2030E) [MS Airbus r323].

**Deliveries.** 793 in 2025A; H1 2026 was 351 (Q1 114, Q2 237) against 306 in H1 2025, leaving 519 for H2 2026 in the MS plan [MS Airbus r143; GS Interims r70].

| Family | 2025A | 2030E, MS | 2030E, GS |
|---|---|---|---|
| A220 | 93 | 115 | 161 |
| A320 family (of which A321neo) | 607 (387) | 805 (604) | 862.5 (n/a) |
| A330 | 36 | 41.5 | 55 |
| A350 | 57 | 110 | 137.5 |
| **Total** | **793** | **1,072** | **1,216** |

Sources: [MS Airbus r104, r116, r119, r129, r139, r143], [GS Airbus Commercial r56+r57, r61, r65, r68, r69]. GS has no A220 total row; its figure adds the A220-100 and -300 rows. Total path: MS 870 / 975 / 1,041 / 1,066 / 1,072 for 2026E-2030E; GS 870 / 1,007 / 1,130 / 1,194 / 1,216, then 1,218 in 2031E.

**Production rates, the main split between the banks.**

| Programme | 2025A (MS / GS) | 2027E MS / GS | 2030E MS / GS |
|---|---|---|---|
| A320 family (MS row: A320neo) | 52.8 / 52.8 | 65 / 65 | 70 / 75 |
| A350 | 5.2 / 4.75 | 8.5 / 8 | 10 / 12.5 |
| A220 | 8.1 / 8.1 | 10 / 11 | 10 / 14 |
| A330neo | 3.1 / 2.8 | 3 / 4.1 | 4 / 5 |

Sources: [MS Airbus r85-89 'Monthly'], [GS Airbus Commercial r74-77]. MS never reaches A320 rate 75: it holds 70 in every quarter from 1Q28 to 4Q30. GS reaches 75 in 2029. Caveats: the banks compute past rates differently (MS divides A350 deliveries by 11 months, GS by 12). MS labels its block production forecasts with actuals based on deliveries; the GS rows are monthly delivery rates. The MS figures are annual averages of its quarterly rates.

## Engines and supply

- **Public structure, not from the models.** The A320neo family is offered with two engines, the CFM LEAP-1A and the Pratt & Whitney GTF. Neither model splits deliveries, cost or risk by engine.
- **No engine data at all.** Neither workbook has a row, note or cell comment on engines, engine shortages or "gliders" (finished airframes waiting for engines).
- **One supply-chain line.** GS books a 'Spirit Aerosystems Impact' of -250m on Airbus Commercial EBIT in each of 2026E and 2027E in its EBITA bridge, with no explanation, plus 'LEAD Savings' of +150m in 2026E [GS Airbus Commercial r132, r134].
- **Constraints are only implicit.** In 2030E GS has 57.5 more A320-family deliveries than MS (862.5 vs 805), in line with its rate of 75 a month against 70 [MS Airbus r119, r86; GS Airbus Commercial r61, r75]. The files do not say whether engines, structures or something else drive the MS caution.
- **Durability.** Nothing on engine time-on-wing, groundings, inspections or airline compensation. Neither model tests deliveries against a supplier shortfall.

## Investment capacity and programme risk

| Self-financed R&D, Airbus Commercial | 2025A | 2026E | 2027E | 2028E | 2029E | 2030E | 2031E |
|---|---|---|---|---|---|---|---|
| MS [MS Airbus r42] | 2,537 | 2,771 | 3,146 | 3,474 | 3,628 | 3,735 | n/a |
| GS [GS Airbus Commercial r179] | 2,537 | 2,800 | 3,000 | 3,200 | 3,200 | 3,100 | 3,100 |

- **R&D is set as a share of revenue on existing programmes.** MS holds R&D at 4.75% of revenue [MS Airbus r43]; GS lets it fall to 3.5% of sales [GS Airbus Commercial r180]. GS's A320 programme R&D peaks at 1.2bn in 2028-2029E and A350 R&D is 1.0bn from 2028E [GS Airbus Commercial r170, r175]. Group expensed R&D rises from 3,153m (2025A) to 4,989m (2030E) [MS Divisional r124].
- **No A320 successor is modelled.** The MS row 'Next generation SA dev.' (next-generation single aisle) has 100m (2010) and 250m (2011) and is empty for every forecast year [MS Airbus r38]. GS's R&D by programme has no new-programme line [GS Airbus Commercial r169-175].
- **Cash capacity.** Free cash flow adds up to 41,225m over 2026E-2030E in MS and 41,985m in GS [MS CFS r61; GS Cash Flow Statement r89, sums]. MS returns 20,327m of that to shareholders [MS CFS r34, sum]. Net cash of 31,830m in 2030E is about three years of 2030E free cash flow [MS CFS r86, r61] (inference).
- **Precedents of programme pain.** The files hold no engine or durability charges. Two precedents remain. Covid in 2020: Commercial EBIT fell to 618m, free cash flow to -6,935m and the dividend was cancelled [MS Airbus r45; MS CFS r61; MS BS r261]. The A220: losses every year from 2019A (-200m, worst -486m in 2021A) to 2027E, profit only from 2028E [GS Airbus Commercial r157].
- **Market view.** Share price 212.90 EUR on 14 Aug 2026; MS rates Overweight with a 255 EUR target (bear 157, bull 376) [MS Cover; MS Bull Bear Base r44]. GS's rating is suspended; its DCF gives 240 EUR per share and runs group adjusted EBIT out to 18,820m in 2036E by formula (7% growth tapering to 3%, 9% discount rate) [GS Cover Page; GS DCF Valuation r7, r21, r38, r39, r51].

## What this means for your decisions

All bullets are (inference): they read the bank numbers above against the game. The numbers they quote carry their source tags.

- **Money is not the binding limit on a launch at the 2030 round (inference).** In 2030E both banks show net cash above 31bn (31,830m MS, 33,062m GS) and free cash flow above 10bn (10,717m MS, 11,565m GS) [MS CFS r86, r61; GS Balance Sheet r65; GS Cash Flow Statement r89]. A new narrowbody launch looks affordable on these numbers; the board's own launch cost and payoff numbers still decide.
- **A launch competes with the payout the market is pricing (inference).** Neither model includes an A320 successor [MS Airbus r38], and both plan rising dividends plus buybacks [MS BS r261; MS IS r75; GS Income Statement r117; GS Cash Flow Statement r101]. A launch in 2030 or 2035 would lift R&D above the 3.5-4.75% of revenue the banks assume [GS Airbus Commercial r180; MS Airbus r43]. Expect investors to treat that as a cut to returns.
- **"Do Nothing" through 2030 is what the valuation rests on (inference).** The A320 family (805-862.5 deliveries in 2030E) [MS Airbus r119; GS Airbus Commercial r61] and Commercial margins rising to 12.8-13.7% in 2030E [GS Airbus Commercial r2, r4; MS Airbus r46] are the base case. An early launch risks the A321neo cash flows before they peak. A later launch keeps them but cedes timing to the rival.
- **Delivering the rate ramp matters more than launch timing before 2030 (inference).** Commercial margin was about 1% in Q1 2026 and H1 2026 free cash flow was negative (-1,166m) [GS Interims r116, r154]. The 57.5-aircraft A320-family gap between the banks in 2030E [MS Airbus r119; GS Airbus Commercial r61] is a measure of the execution risk. Engine supply may be one cause, but the files do not show it.
- **Engine selection: keep two sources if the board allows it (inference).** The A320neo already has two engines (public structure). Keeping two engine makers in the race for the next narrowbody limits dependence on one supplier's durability record, which the models do not measure. A Joint Venture or single-source engine offer should be judged on board numbers for delay and durability risk.
- **Budget for a long loss tail (inference).** The A220 lost money in every year of the GS record from 2019A to 2027E, nine years [GS Airbus Commercial r157]. A new narrowbody with an unproven engine could do the same. Treat "Delay Tactics" or a slip by an engine maker as a real cost, not a free option.
- **The widebody leg is growing (inference).** A350 rates rise to 10 (MS) or 12.5 (GS) a month by 2030E [MS Airbus r89; GS Airbus Commercial r77] and MS puts widebody revenue at 28% of Commercial revenue in 2030E [MS Airbus r312, r316]. Widebody engine upgrades offered by engine makers would matter to that growth; "Re-engine" of a widebody is likely a cheaper lever than a clean-sheet aircraft.

## What the models do not cover

- **The game's horizon.** MS ends at 2030E and GS at 2031E. The GS DCF extends group EBIT and free cash flow to 2036E by formula only, at fixed growth rates [GS DCF Valuation r7, r14]; that formula path is the only number in either file for the 2035 round, and nothing covers the 2045 or 2050 rounds.
- **Engines.** No engine split by family, no LEAP or GTF supply, no gliders, no durability or compensation costs.
- **The next aircraft.** No A320-successor cost, timing or engine choice in either model.
- **Scenarios.** MS bear/base/bull covers only 2028E profit-and-loss items (revenue, EBIT, EPS) and the price target [MS Bull Bear Base r4, r15, r16, r23, r44]; nothing for deliveries, rates, cash flow or net cash. GS has no scenarios. Neither model tests supplier shortfalls beyond the Spirit line.
- **Order book.** Neither model forecasts it: MS holds the order book flat at 539.7bn EUR and GS stops at 2025A [MS and GS order-book rows; row numbers not given in the extract].
- **Mix detail.** The extract has no aftermarket split, no A321XLR, A350 freighter or A330neo tanker split, and no customer-financing exposure beyond small residual values.
- **Data caveats.** GS actual vs estimate is inferred from its publication date. MS 2026 quarters are treated as actual by inference. GS DPS for 2018-2020 is shifted, and its 'Adj. EBIT margin (%)' row is inconsistent with its own EBIT and sales rows, so neither is used [GS Income Statement r117; GS r85].
