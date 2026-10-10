# The Boeing Company Board of Directors: web sources

Research for the `boeing-board` agent (dash-2050 war game). Retrieved 2026-10-10 with the WebSearch tool. The container cannot fetch pages, so every web item in `evidence.jsonl` records what the search results' summary stated (not verbatim page text), the result URL, and a second, differently worded search that returned the same fact (`corroborated_by`). Items with no corroboration are flagged in their `finding` and may be used only as (inference).

**Verification (2026-10-10).** The verifier's independent re-search of each web item could not run: the session's web
search limit was reached before the first query. Nothing below was re-searched. The 29 corroborated items rest on the
drafter's two searches each; where the repo's own calls and 10-Ks overlap them, they agree (777X launch at Dubai with 259
commitments: FQ4 2013 call, transcripts p. 2030; 737 rate 42 agreed with the FAA in October 2025, Jeppesen closing and
Spirit closing expected in late 2025: FQ3 2025 call, pp. 6-14; six board committees incl. Aerospace Safety, Finance and
Special Programs: 10-K FY2019 Exhibit 10.6, boeing_10k p. 623). Two uncorroborated items were withdrawn and their numbers
are not reused: 0059 (BlackRock's May 2024 vote bulletin, reported vote against the Aerospace Safety chair; a claim about a
named director that no second search confirmed) and 0070 (AInvest analysis claiming a 2025 common-dividend restart; no
release or filing found, and the FY2024 10-K and 2025 calls do not support it). BG-0067 is dated to the month only.

Dates: the source's date where the result gave one; `YYYY-MM` or `YYYY` where only the month or year was known.

## Primary web sources (one line per evidence item)

| Id | Date | Publisher | Title | URL | Corroborated by |
|---|---|---|---|---|---|
| BG-0037 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://www.sec.gov/Archives/edgar/data/12927/000162828026025684/ba-20260417.htm |
| BG-0038 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://investors.boeing.com/investors/news/press-release-details/2024/Boeing-Announces-Board-and-Management-Changes/default.aspx |
| BG-0039 | 2025-12-03 | The Boeing Company (investor relations) | Boeing Elects Bradley D. Tilden to Board of Directors | https://investors.boeing.com/investors/news/press-release-details/2025/Boeing-Elects-Bradley-D--Tilden-to-Board-of-Directors/default.aspx | https://www.sec.gov/Archives/edgar/data/0000012927/000162828025055122/a202512dec018kprex991.htm |
| BG-0040 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://www.boeing.com/company/general-info/corporate-governance |
| BG-0041 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form ARS - FY2025 (annual report to shareholders) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096681/d23314dars.pdf | https://www.boeing.com/company/bios/david-l-joyce-bio |
| BG-0042 | 2026 | MarketScreener | Executive Committee: Boeing (company governance) | https://www.marketscreener.com/quote/stock/BOEING-4816/company-governance/ | none (inference only) |
| BG-0043 | 2025-12-17 | The Boeing Company | Aerospace Safety Committee Charter (as amended December 17, 2025) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/charter_aerospace_safety.pdf | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm |
| BG-0044 | 2025-12-17 | The Boeing Company | Finance Committee Charter (as amended December 17, 2025) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/charter_finance.pdf | https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/charter_finance.pdf |
| BG-0045 | 2026-06-23 | The Boeing Company | Corporate Governance Principles (latest version found, June 23, 2026) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/corporate-governance-principles.pdf | https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/corporate-governance-principles-08-19.pdf |
| BG-0046 | 2020-04-29 | ValueEdge Advisors | Independent chair proposal gets majority support at Boeing | https://valueedgeadvisors.com/2020/04/29/independent-chair-proposal-gets-majority-support-at-boeing/ | https://sec.gov/Archives/edgar/data/12927/000119312521071321/d922634ddef14a.htm |
| BG-0047 | 2019-10-11 | The Boeing Company (SEC EDGAR) | BOEING CO - Form 8-K - FY2019 (Exhibit 99.1) | https://www.sec.gov/Archives/edgar/data/12927/000001292719000067/exhibit991.htm | https://onmanorama.com/news/business/2019/12/23/boeing-ousts-muilenburg--names-chair-david-calhoun-as-ceo.html |
| BG-0048 | 2019-12-23 | Bloomberg | Boeing Ousts CEO, Picks Chairman to Map Exit From Max Crisis | https://www.bloomberg.com/news/articles/2019-12-23/boeing-ceo-dennis-muilenburg-resigns-david-calhoun-named-president-and-ceo | https://www.satellitetoday.com/business/2019/12/23/boeing-ceo-dennis-muilenburg-resigns/ |
| BG-0049 | 2019-09-25 | The Boeing Company (news release) | Boeing Chairman, President and CEO Dennis Muilenburg and Boeing Board of Directors Reaffirm Company's Commitment to Safety | https://boeing.mediaroom.com/2019-09-25-Boeing-Chairman-President-and-CEO-Dennis-Muilenburg-and-Boeing-Board-of-Directors-Reaffirm-Companys-Commitment-to-Safety | https://www.militaryaerospace.com/commercial-aerospace/article/14230658/boeing-board-establishes-permanent-aerospace-safety-committee |
| BG-0050 | 2024-02-26 | Federal Aviation Administration | Section 103 Organization Designation Authorizations (ODA) for Transport Airplanes Expert Panel Review Report | https://www.faa.gov/newsroom/Sec103_ExpertPanelReview_Report_Final.pdf | https://www.nbcnews.com/news/us-news/boeings-safety-culture-inadequate-confusing-new-faa-report-finds-rcna140647; https://flightplan.forecastinternational.com/2024/02/27/oda-review-panel-issues-report-on-boeings-safety-culture/ |
| BG-0051 | 2021-09-30 | Holland & Knight | Recent Delaware Decision Highlights Heightened Board Oversight | https://www.hklaw.com/en/insights/publications/2021/09/recent-delaware-decision-highlights-heightened-board-oversight | https://lieffcabraser.com/securities/boeing/ |
| BG-0052 | 2021-11 | The D&O Diary | Boeing Air Crash Derivative Lawsuit Settles for $237.5 Million | https://www.dandodiary.com/2021/11/articles/shareholders-derivative-litigation/boeing-air-crash-derivative-lawsuit-settles-for-237-5-million/ | https://www.bordermail.com.au/story/7499825/boeing-settles-737-max-safety-lawsuit/ |
| BG-0053 | 2021-09-06 | Leeham News and Analysis | Pontifications: David Joyce fills key void on Boeing's Board | https://leehamnews.com/2021/09/06/pontifications-david-joyce-fills-key-void-on-boeings-board/ | https://leehamnews.com/2021/04/12/pontifications-more-of-the-same-expected-at-boeings-annual-meeting/ |
| BG-0054 | 2019-05-31 | The American Prospect | To Make Passengers Safer? Boeing Just Made Shareholders Richer | https://prospect.org/2019/05/31/make-passengers-safer-boeing-just-made-shareholders-richer/ | https://fortune.com/longform/boeing-737-max-crisis-shareholder-first-culture/ |
| BG-0055 | 2024-04 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2024 (2024 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312524088568/d550077ddef14a.htm | https://wjla.com/news/nation-world/boeings-ceo-got-compensation-worth-nearly-33m-last-year-but-lost-3m-bonus-david-calhoun-jetliner-max-737-panel-door-plug-blowout-mid-flight-travel-plane-manufacturer-faa-federal-aviation-administration |
| BG-0056 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://finance.yahoo.com/news/boeing-ties-employee-incentive-plan-221537944.html |
| BG-0057 | 2024-07-30 | The Boeing Company (SEC EDGAR) | BOEING CO - Form 8-K (Ortberg appointment and compensation) | https://www.sec.gov/Archives/edgar/data/12927/000001292724000058/ba-20240730.htm | none (inference only) |
| BG-0058 | 2024-04-30 | CNBC | Glass Lewis recommends investors vote against three Boeing directors, including CEO Calhoun | https://www.cnbc.com/2024/04/30/glass-lewis-recommends-investors-vote-against-three-boeing-directors-including-ceo-calhoun.html | https://news.bloomberglaw.com/esg/boeing-safety-woes-fuel-opposition-to-ceos-pay-board-make-up |
| BG-0060 | 2026-04 | Simply Wall St | The Boeing Company ownership | https://simplywall.st/stocks/us/capital-goods/nyse-ba/boeing/ownership | https://finance.yahoo.com/markets/stocks/articles/boeing-stock-ownership-institutional-executive-143900060.html |
| BG-0061 | 2024-03-25 | The Boeing Company (investor relations) | Boeing Announces Board and Management Changes | https://investors.boeing.com/investors/news/press-release-details/2024/Boeing-Announces-Board-and-Management-Changes/default.aspx | https://assemblymag.com/articles/98423-boeing-is-searching-for-a-new-ceo-amid-massive-leadership-changes |
| BG-0062 | 2024-11 | Kirkland & Ellis | Boeing Closes $24.25 Billion Equity Offering, Marking Largest Follow-On in History | https://www.kirkland.com/news/press-release/2024/11/boeing-closes-24-25-billion-equity-offering-marking-largest-follow-on-in-history | https://www.bloomberg.com/news/articles/2024-10-29/boeing-raises-21-billion-in-capital-hike-to-boost-liquidity |
| BG-0063 | 2025-04-22 | Bloomberg | Boeing Sells Jeppesen Unit to Thoma Bravo for $10.6 Billion | https://www.bloomberg.com/news/articles/2025-04-22/boeing-sells-jeppesen-unit-to-thoma-bravo-for-10-6-billion | https://www.thomabravo.com/press-releases/jeppesen-foreflight-launches-as-a-standalone-company-to-redefine-the-future-of-aviation-software |
| BG-0064 | 2025-12-08 | AP via ABC News | Boeing finalizes $4.7B acquisition of key 737 Max supplier Spirit AeroSystems | https://abcnews.go.com/Business/wireStory/boeing-finalizes-47b-acquisition-key-737-max-supplier-128218277 | https://centreforaviation.com/news/boeing-completes-acquisition-of-spirit-aerosystems-1341750 |
| BG-0065 | 2025-05-23 | Al Jazeera | Boeing reaches deal with US DOJ to avoid prosecution over 737 Max crashes | https://www.aljazeera.com/economy/2025/5/23/boeing-reaches-deal-with-us-doj-to-avoid-prosecution-over-737-max-crashes | https://www.aljazeera.com/economy/2025/11/6/us-judge-approves-doj-decision-to-drop-boeing-criminal-case |
| BG-0066 | 2011-08-30 | The Boeing Company (news release) | Boeing Launches 737 New Engine Family with Commitments for 496 Airplanes from Five Airlines | https://boeing.mediaroom.com/2011-08-30-Boeing-Launches-737-New-Engine-Family-with-Commitments-for-496-Airplanes-from-Five-Airlines | https://centreforaviation.com/news/boeing-launches-737-max-with-496-commitments-117931 |
| BG-0067 | 2013-11 | The Boeing Company (news release) | Boeing Launches 777X with Record-Breaking Orders | https://boeing.mediaroom.com/Boeing-Launches-777X-with-Record-Breaking-Orders-Strengthens-Partnerships-in-the-Middle-East-at-the-2013-Dubai-Airshow | none (inference only) |
| BG-0068 | 2026-07-20 | Airguide (reporting a CNBC interview) | Boeing CEO: New Jet Still Years Away as Company Rebuilds Finances | https://airguide.info/?p=419429 | https://news.bloomberglaw.com/international-trade/boeing-says-next-generation-jet-likely-coming-end-of-next-decade |
| BG-0069 | 2025-10-18 | Spectrum News | FAA approval for Boeing to increase 737 MAX production | https://spectrumlocalnews.com/us/snplus/business/2025/10/18/faa-approval-boeing-increase-737-max-production | https://centreforaviation.com/news/boeing-testing-production-rate-of-47-aircraft-per-month-cautious-of-increasing-to-52-ceo-1360867 |

## Corroborating sources

- https://www.sec.gov/Archives/edgar/data/12927/000162828026025684/ba-20260417.htm (for BG-0037; query: `Boeing 2026 annual meeting results directors elected April 17 2026`)
- https://investors.boeing.com/investors/news/press-release-details/2024/Boeing-Announces-Board-and-Management-Changes/default.aspx (for BG-0038; query: `Boeing March 25 2024 Calhoun to step down end of year Kellner not stand for reelection Mollenkopf chair Stan Deal retire`)
- https://www.sec.gov/Archives/edgar/data/0000012927/000162828025055122/a202512dec018kprex991.htm (for BG-0039; query: `Boeing board refreshment ten new directors since 2019 aviation safety engineering expertise Tilden 12 members`)
- https://www.boeing.com/company/general-info/corporate-governance (for BG-0040; query: `Boeing board Compensation Committee chair and Governance & Public Policy Committee chair 2025 2026 Bradway Good Williams`)
- https://www.boeing.com/company/bios/david-l-joyce-bio (for BG-0041; query: `David Joyce chair Boeing Aerospace Safety Committee Akhil Johri chair Finance Committee Lynne Doughtie Audit chair`)
- https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm (for BG-0043; query: `Boeing board six standing committees Audit Compensation Finance Governance Public Policy Special Programs Aerospace Safety`)
- https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/charter_finance.pdf (for BG-0044; query: `"Boeing" finance committee purpose capital structure financing investment recommendations to the board significant capital projects`)
- https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/corporate-governance-principles-08-19.pdf (for BG-0045; query: `Boeing corporate governance principles "Board selects the CEO" oversight business conducted by employees managers officers`)
- https://sec.gov/Archives/edgar/data/12927/000119312521071321/d922634ddef14a.htm (for BG-0046; query: `Boeing corporate governance principles board responsibilities strategic plan approve major decisions independent chair 75% independent`)
- https://onmanorama.com/news/business/2019/12/23/boeing-ousts-muilenburg--names-chair-david-calhoun-as-ceo.html (for BG-0047; query: `Boeing board ousts Muilenburg December 2019 Calhoun named CEO restore confidence`)
- https://www.satellitetoday.com/business/2019/12/23/boeing-ceo-dennis-muilenburg-resigns/ (for BG-0048; query: `Boeing CEO Dennis Muilenburg resigns board statement "change in leadership was necessary to restore confidence"`)
- https://www.militaryaerospace.com/commercial-aerospace/article/14230658/boeing-board-establishes-permanent-aerospace-safety-committee (for BG-0049; query: `Boeing Aerospace Safety Committee charter responsibilities oversight design manufacture`)
- https://www.nbcnews.com/news/us-news/boeings-safety-culture-inadequate-confusing-new-faa-report-finds-rcna140647 (for BG-0050; query: `FAA Section 103 expert review panel report Boeing safety culture February 2024 findings disconnect senior management`)
- https://flightplan.forecastinternational.com/2024/02/27/oda-review-panel-issues-report-on-boeings-safety-culture/ (for BG-0050; query: `expert panel Boeing safety management system inadequate 53 recommendations ACSAA report employees fear retaliation`)
- https://lieffcabraser.com/securities/boeing/ (for BG-0051; query: `Boeing directors settle Delaware derivative lawsuit 737 MAX $237.5 million board failed oversee safety governance reforms`)
- https://www.bordermail.com.au/story/7499825/boeing-settles-737-max-safety-lawsuit/ (for BG-0052; query: `Boeing board lacked engineering and safety expertise before 737 MAX crashes directors backgrounds criticism 2019`)
- https://leehamnews.com/2021/04/12/pontifications-more-of-the-same-expected-at-boeings-annual-meeting/ (for BG-0053; query: `Boeing board lacked engineering and safety expertise before 737 MAX crashes directors backgrounds criticism 2019`)
- https://fortune.com/longform/boeing-737-max-crisis-shareholder-first-culture/ (for BG-0054; query: `Boeing share buybacks 2013-2019 $43 billion instead of new airplane investment criticism`)
- https://wjla.com/news/nation-world/boeings-ceo-got-compensation-worth-nearly-33m-last-year-but-lost-3m-bonus-david-calhoun-jetliner-max-737-panel-door-plug-blowout-mid-flight-travel-plane-manufacturer-faa-federal-aviation-administration (for BG-0055; query: `Calhoun declined 2023 annual bonus Boeing compensation committee product safety primary weight Mollenkopf proxy 2024`)
- https://finance.yahoo.com/news/boeing-ties-employee-incentive-plan-221537944.html (for BG-0056; query: `Boeing ties employee incentive plan to company-wide performance 2025 safety quality program execution 20 percent`)
- https://news.bloomberglaw.com/esg/boeing-safety-woes-fuel-opposition-to-ceos-pay-board-make-up (for BG-0058; query: `Boeing 2024 annual shareholder meeting Glass Lewis ISS recommend against directors say on pay support 62%`)
- https://finance.yahoo.com/markets/stocks/articles/boeing-stock-ownership-institutional-executive-143900060.html (for BG-0060; query: `Boeing largest shareholders institutional ownership Vanguard BlackRock Capital Research 2025`)
- https://assemblymag.com/articles/98423-boeing-is-searching-for-a-new-ceo-amid-massive-leadership-changes (for BG-0061; query: `Boeing shakeup 2024 Kellner steps aside as chairman Mollenkopf leads CEO search Alaska door plug`)
- https://www.bloomberg.com/news/articles/2024-10-29/boeing-raises-21-billion-in-capital-hike-to-boost-liquidity (for BG-0062; query: `Boeing raises $21 billion share sale upsized October 28 2024 common stock depositary shares priced $143`)
- https://www.thomabravo.com/press-releases/jeppesen-foreflight-launches-as-a-standalone-company-to-redefine-the-future-of-aviation-software (for BG-0063; query: `Boeing Jeppesen digital aviation sale Thoma Bravo $10.55 billion completed debt reduction`)
- https://centreforaviation.com/news/boeing-completes-acquisition-of-spirit-aerosystems-1341750 (for BG-0064; query: `Boeing completes acquisition of Spirit AeroSystems closing date 2025`)
- https://www.aljazeera.com/economy/2025/11/6/us-judge-approves-doj-decision-to-drop-boeing-criminal-case (for BG-0065; query: `judge approves dismissal Boeing criminal case 737 MAX fraud non-prosecution deal families object`)
- https://centreforaviation.com/news/boeing-launches-737-max-with-496-commitments-117931 (for BG-0066; query: `Boeing board approves launch of 737 MAX August 30 2011 re-engined 737`)
- https://news.bloomberglaw.com/international-trade/boeing-says-next-generation-jet-likely-coming-end-of-next-decade (for BG-0068; query: `Boeing 2026 new single-aisle airplane launch decision Ortberg timing next-generation narrowbody`)
- https://centreforaviation.com/news/boeing-testing-production-rate-of-47-aircraft-per-month-cautious-of-increasing-to-52-ceo-1360867 (for BG-0069; query: `Boeing 737 MAX production 47 per month FAA capstone review approval 2026`)

## Queries used (in order, 58 searches)

1. `Boeing board of directors 2026 chair Mollenkopf directors list`
2. `Boeing 2026 proxy statement director nominees annual meeting`
3. `Boeing names Brad Tilden to board of directors`
4. `Boeing 2026 annual meeting results directors elected April 17 2026`
5. `Sabrina Soussan Boeing board leaves not standing for re-election`
6. `Boeing board committees Aerospace Safety Committee chair Joyce Finance Committee chair 2025`
7. `Boeing board six standing committees Audit Compensation Finance Governance Public Policy Special Programs Aerospace Safety`
8. `Boeing Aerospace Safety Committee charter responsibilities oversight design manufacture`
9. `Boeing Finance Committee charter reviews capital expenditures dividends share repurchase new commercial airplane program`
10. `Boeing corporate governance principles board responsibilities strategic plan approve major decisions independent chair 75% independent`
11. `"Boeing" finance committee purpose capital structure financing investment recommendations to the board significant capital projects`
12. `Boeing independent chairman requirement adopted 2020 shareholder vote governance principles split chair CEO`
13. `Boeing board ousts Muilenburg December 2019 Calhoun named CEO restore confidence`
14. `Boeing March 25 2024 Calhoun to step down end of year Kellner not stand for reelection Mollenkopf chair Stan Deal retire`
15. `Boeing CEO Dennis Muilenburg resigns board statement "change in leadership was necessary to restore confidence"`
16. `Boeing shakeup 2024 Kellner steps aside as chairman Mollenkopf leads CEO search Alaska door plug`
17. `FAA Section 103 expert review panel report Boeing safety culture February 2024 findings disconnect senior management`
18. `expert panel Boeing safety management system inadequate 53 recommendations ACSAA report employees fear retaliation`
19. `Boeing directors settle Delaware derivative lawsuit 737 MAX $237.5 million board failed oversee safety governance reforms`
20. `Delaware Chancery Boeing Caremark ruling 2021 board no safety reporting system judge Zurn shareholders claim directors`
21. `Boeing share buybacks 2013-2019 $43 billion instead of new airplane investment criticism`
22. `how much stock did Boeing repurchase before 737 MAX grounding buybacks total 2014 to 2019 analysis`
23. `Boeing 2025 annual incentive plan metrics safety quality weighting executive compensation proxy 2026`
24. `Boeing executive pay 2024 annual bonus 60% safety quality operational metrics compensation committee changes after Alaska`
25. `Boeing "One Company Score" bonus free cash flow core EPS revenue 80% operational 20%`
26. `Ortberg pay package 2025 long-term incentive performance stock units three-year metrics Boeing proxy`
27. `Boeing ties employee incentive plan to company-wide performance 2025 safety quality program execution 20 percent`
28. `Boeing largest shareholders institutional ownership Vanguard BlackRock Capital Research 2025`
29. `who owns the most Boeing stock 2026 top holders percent no government stake`
30. `Boeing completes acquisition of Spirit AeroSystems closing date 2025`
31. `Boeing Jeppesen digital aviation sale Thoma Bravo $10.55 billion completed debt reduction`
32. `Boeing sells Jeppesen ForeFlight to Thoma Bravo closes portfolio streamlining Ortberg`
33. `Boeing 2026 new single-aisle airplane launch decision Ortberg timing next-generation narrowbody`
34. `Boeing dividend reinstatement share buyback 2026 Ortberg capital allocation debt paydown priority`
35. `"Boeing" reinstates quarterly dividend board declares common stock dividend first since 2020`
36. `Farnborough 2026 Ortberg not financially ready new airplane launch balance sheet`
37. `Boeing board committee on airplane policies and processes September 2019 recommendations permanent aerospace safety committee product and services safety organization`
38. `Boeing board strips Muilenburg of chairman title October 2019 Calhoun non-executive chairman`
39. `Boeing DOJ non-prosecution agreement 2025 independent compliance consultant board obligations $1.1 billion`
40. `judge approves dismissal Boeing criminal case 737 MAX fraud non-prosecution deal families object`
41. `Boeing board approves launch of 737 MAX August 30 2011 re-engined 737`
42. `Boeing board of directors authorized 777X offer to customers May 2013 launch November 2013 Dubai`
43. `"Boeing Launches 737 New Engine Family" board of directors approval 496 commitments five airlines`
44. `Boeing $24 billion stock offering October 2024 largest ever equity raise mandatory convertible preferred protect investment grade`
45. `Boeing 2024 annual shareholder meeting Glass Lewis ISS recommend against directors say on pay support 62%`
46. `Boeing board refreshment ten new directors since 2019 aviation safety engineering expertise Tilden 12 members`
47. `Mollenkopf letter to shareholders 2026 proxy Boeing board priorities safety quality stability long-term`
48. `David Joyce chair Boeing Aerospace Safety Committee Akhil Johri chair Finance Committee Lynne Doughtie Audit chair`
49. `Boeing board Compensation Committee chair and Governance & Public Policy Committee chair 2025 2026 Bradway Good Williams`
50. `Boeing board lacked engineering and safety expertise before 737 MAX crashes directors backgrounds criticism 2019`
51. `Calhoun declined 2023 annual bonus Boeing compensation committee product safety primary weight Mollenkopf proxy 2024`
52. `FAA approves Boeing 737 MAX production increase to 42 per month October 2025 then 47 2026`
53. `Boeing corporate governance principles "Board selects the CEO" oversight business conducted by employees managers officers`
54. `Boeing finalizes Spirit AeroSystems deal December 2025 Wichita fuselage supplier back in-house`
55. `Boeing raises $21 billion share sale upsized October 28 2024 common stock depositary shares priced $143`
56. `Boeing 737 MAX production 47 per month FAA capstone review approval 2026`
57. `Boeing directors no aviation engineers or pilots on board 2019 Leeham David Joyce fills key void`
58. `BlackRock voted against Boeing director David Joyce 2024 Aerospace Safety Committee chair vote bulletin`

## Searches that did not yield a usable fact

- Query 5 (Sabrina Soussan): she did not stand for re-election in 2025 and the board shrank; only one search, so not an item. The 2026 slate (BG-0037) no longer lists her.
- Query 25 (One Company Score): no result; the 2025 bonus design is corroborated by queries 23 and 27 instead.
- Queries 34-35 (dividend reinstatement): no Boeing release or filing found; one analysis claimed a 2025 restart (former 0070, withdrawn at verification).
- Query 42 (777X board authorization date): launch found, board date not found (BG-0067, uncorroborated; launch day not confirmed, dated 2013-11).
- Query 47 (2026 chair letter): the letter's text was not reached; only vote results.
- Query 58 (BlackRock vote on Joyce): not confirmed by a second search; the item (former 0059) was withdrawn at verification. The query did return the CNBC Glass Lewis item (BG-0058).

## Repo sources (verbatim, machine-checked)

- `transcripts.txt` (Boeing calls 2006-2025): 23 items, BG-0001 to BG-0023, including Chairman Lawrence Kellner at the 2021 Annual Meeting of Shareholders (pages 742-755).
- `boeing_10k.txt`: 13 items, BG-0024 to BG-0036 (10-K FY2024, FY2020, FY2018).
- All 36 pass `wargame/profiles/build/verify_quotes.py` (36/36).
