# The Boeing Company Board of Directors: web sources

Research for the `boeing-board` agent (dash-2050 war game). Retrieved 2026-10-10 with the WebSearch tool. The container cannot fetch pages, so every web item in `evidence.jsonl` records what the search results' summary stated (not verbatim page text), the result URL, and a second, differently worded search that returned the same fact (`corroborated_by`). Items with no corroboration are flagged in their `finding` and may be used only as (inference).

**Verification (2026-10-10).** The first verifier's re-search could not run (the session's search limit was reached).
A second agent then re-searched the web items independently on 2026-10-10, capped at 30 searches (listed under
"Independent re-search" below). 31 of the 32 web items were re-searched: 26 confirmed (BG-0042 only in part), 5 corrected
(BG-0044, BG-0045, BG-0048, BG-0055, BG-0060), none dropped. BG-0067 is now corroborated. BG-0057 was not re-searched and
stays uncorroborated (inference only). Each item records `verified`, `verification` and a `verification_note`, and its
re-search query and URL are appended to `corroborated_by`. Where the repo's own calls and 10-Ks overlap the web items they
agree (777X launch at Dubai with 259 commitments: FQ4 2013 call, transcripts p. 2030; 737 rate 42 agreed with the FAA in
October 2025, Jeppesen closing and Spirit closing expected in late 2025: FQ3 2025 call, pp. 6-14; six board committees
incl. Aerospace Safety, Finance and Special Programs: 10-K FY2019 Exhibit 10.6, boeing_10k p. 623). Two uncorroborated
items were withdrawn at the first verification and their numbers are not reused: 0059 (BlackRock's May 2024 vote
bulletin, reported vote against the Aerospace Safety chair; a claim about a named director that no second search
confirmed) and 0070 (AInvest analysis claiming a 2025 common-dividend restart; no release or filing found, and the FY2024
10-K and 2025 calls do not support it). BG-0067 is dated to the month only.

Dates: the source's date where the result gave one; `YYYY-MM` or `YYYY` where only the month or year was known.

## Primary web sources (one line per evidence item)

| Id | Date | Publisher | Title | URL | Corroborated by |
|---|---|---|---|---|---|
| BG-0037 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://www.sec.gov/Archives/edgar/data/12927/000162828026025684/ba-20260417.htm |
| BG-0038 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://investors.boeing.com/investors/news/press-release-details/2024/Boeing-Announces-Board-and-Management-Changes/default.aspx |
| BG-0039 | 2025-12-03 | The Boeing Company (investor relations) | Boeing Elects Bradley D. Tilden to Board of Directors | https://investors.boeing.com/investors/news/press-release-details/2025/Boeing-Elects-Bradley-D--Tilden-to-Board-of-Directors/default.aspx | https://www.sec.gov/Archives/edgar/data/0000012927/000162828025055122/a202512dec018kprex991.htm |
| BG-0040 | 2026-03-06 | The Boeing Company (SEC EDGAR) | BOEING CO - Form DEF 14A - FY2026 (2026 proxy statement) | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm | https://www.boeing.com/company/general-info/corporate-governance |
| BG-0041 | 2026 | VectorShift (third-party profile); for Joyce also CNBC (2024) | Boeing board committee chairs, 2026 (third-party profile; relabelled at the fix pass: the drafter's result linked the FY2025 Form ARS, https://www.sec.gov/Archives/edgar/data/12927/000119312526096681/d23314dars.pdf, which the re-search did not reach) | https://vectorshift.ai/research/companies/boeing-co/people | https://www.cnbc.com/2024/04/30/glass-lewis-recommends-investors-vote-against-three-boeing-directors-including-ceo-calhoun.html |
| BG-0042 | 2026 | MarketScreener | Executive Committee: Boeing (company governance) | https://www.marketscreener.com/quote/stock/BOEING-4816/company-governance/ | https://vectorshift.ai/research/companies/boeing-co/people (re-search; Bradway's chair only, Good's stays inference only) |
| BG-0043 | 2025-12-17 | The Boeing Company | Aerospace Safety Committee Charter (as amended December 17, 2025) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/charter_aerospace_safety.pdf | https://www.sec.gov/Archives/edgar/data/12927/000119312526096787/d39411ddef14a.htm |
| BG-0044 | 2025-12-17 | The Boeing Company | Finance Committee Charter (as amended December 17, 2025) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/charter_finance.pdf | https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/charter_finance.pdf |
| BG-0045 | 2026-06-23 | The Boeing Company | Corporate Governance Principles (current boeing.com version) and Director Independence Standards (affirmed June 23, 2026) | https://www.boeing.com/content/dam/boeing/v2/company/corporate-governance/corporate-governance-principles.pdf | https://www.boeing.com/resources/boeingdotcom/company/general_info/pdf/corporate-governance-principles-08-19.pdf |
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
| BG-0057 | 2024-07-30 | The Boeing Company (SEC EDGAR) | BOEING CO - Form 8-K (Ortberg appointment and compensation) | https://www.sec.gov/Archives/edgar/data/12927/000001292724000058/ba-20240730.htm | none (inference only; not re-searched 2026-10-10) |
| BG-0058 | 2024-04-30 | CNBC | Glass Lewis recommends investors vote against three Boeing directors, including CEO Calhoun | https://www.cnbc.com/2024/04/30/glass-lewis-recommends-investors-vote-against-three-boeing-directors-including-ceo-calhoun.html | https://news.bloomberglaw.com/esg/boeing-safety-woes-fuel-opposition-to-ceos-pay-board-make-up |
| BG-0060 | 2026-04 | Simply Wall St | The Boeing Company ownership | https://simplywall.st/stocks/us/capital-goods/nyse-ba/boeing/ownership | https://finance.yahoo.com/markets/stocks/articles/boeing-stock-ownership-institutional-executive-143900060.html |
| BG-0061 | 2024-03-25 | The Boeing Company (investor relations) | Boeing Announces Board and Management Changes | https://investors.boeing.com/investors/news/press-release-details/2024/Boeing-Announces-Board-and-Management-Changes/default.aspx | https://assemblymag.com/articles/98423-boeing-is-searching-for-a-new-ceo-amid-massive-leadership-changes |
| BG-0062 | 2024-11 | Kirkland & Ellis | Boeing Closes $24.25 Billion Equity Offering, Marking Largest Follow-On in History | https://www.kirkland.com/news/press-release/2024/11/boeing-closes-24-25-billion-equity-offering-marking-largest-follow-on-in-history | https://www.bloomberg.com/news/articles/2024-10-29/boeing-raises-21-billion-in-capital-hike-to-boost-liquidity |
| BG-0063 | 2025-04-22 | Bloomberg | Boeing Sells Jeppesen Unit to Thoma Bravo for $10.6 Billion | https://www.bloomberg.com/news/articles/2025-04-22/boeing-sells-jeppesen-unit-to-thoma-bravo-for-10-6-billion | https://www.thomabravo.com/press-releases/jeppesen-foreflight-launches-as-a-standalone-company-to-redefine-the-future-of-aviation-software |
| BG-0064 | 2025-12-08 | AP via ABC News | Boeing finalizes $4.7B acquisition of key 737 Max supplier Spirit AeroSystems | https://abcnews.go.com/Business/wireStory/boeing-finalizes-47b-acquisition-key-737-max-supplier-128218277 | https://centreforaviation.com/news/boeing-completes-acquisition-of-spirit-aerosystems-1341750 |
| BG-0065 | 2025-05-23 | Al Jazeera | Boeing reaches deal with US DOJ to avoid prosecution over 737 Max crashes | https://www.aljazeera.com/economy/2025/5/23/boeing-reaches-deal-with-us-doj-to-avoid-prosecution-over-737-max-crashes | https://www.aljazeera.com/economy/2025/11/6/us-judge-approves-doj-decision-to-drop-boeing-criminal-case |
| BG-0066 | 2011-08-30 | The Boeing Company (news release) | Boeing Launches 737 New Engine Family with Commitments for 496 Airplanes from Five Airlines | https://boeing.mediaroom.com/2011-08-30-Boeing-Launches-737-New-Engine-Family-with-Commitments-for-496-Airplanes-from-Five-Airlines | https://centreforaviation.com/news/boeing-launches-737-max-with-496-commitments-117931 |
| BG-0067 | 2013-11 | The Boeing Company (news release) | Boeing Launches 777X with Record-Breaking Orders | https://boeing.mediaroom.com/Boeing-Launches-777X-with-Record-Breaking-Orders-Strengthens-Partnerships-in-the-Middle-East-at-the-2013-Dubai-Airshow | https://oldain.ainonline.com/aviation-news/air-transport/2013-11-18/new-orders-kick-launch-boeing-777x (re-search) |
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
- Query 42 (777X board authorization date): launch found, board date not found (BG-0067; launch day not confirmed, dated 2013-11). The launch month and orders were corroborated at the 2026-10-10 re-search (re-search 25).
- Query 47 (2026 chair letter): the letter's text was not reached; only vote results.
- Query 58 (BlackRock vote on Joyce): not confirmed by a second search; the item (former 0059) was withdrawn at verification. The query did return the CNBC Glass Lewis item (BG-0058).

## Independent re-search (2026-10-10, 30 searches)

Run by a second agent with the WebSearch tool; the query, the items it checked and the outcome. Each item's URL is in
its `corroborated_by`.

1. `Boeing 2026 proxy statement director nominees Mollenkopf Bradway Buckley Doughtie Gitlin Good Harris Johri Joyce Richardson Tilden` -> BG-0037 kept; BG-0039 kept
2. `Boeing April 17 2026 annual meeting voting results all directors re-elected say on pay approved 8-K` -> BG-0037 kept
3. `Boeing board committee chairs 2026: Joyce Aerospace Safety Committee chair, Johri Finance Committee chair, Doughtie Audit Committee chair, Good Compensation chair, Bradway Governance chair` -> BG-0039 kept; BG-0040 kept; BG-0041 kept; BG-0042 kept (partial)
4. `"Joyce" chairs Boeing "Aerospace Safety Committee" and "Johri" chairs Boeing "Finance Committee"` -> BG-0041 kept
5. `Steve Mollenkopf Boeing independent board chair engineering background former Qualcomm CEO director since 2020 led CEO search` -> BG-0038 kept; BG-0061 kept
6. `Boeing Aerospace Safety Committee charter purpose safe design development certification production maintenance operation at least three independent directors` -> BG-0043 kept; BG-0049 kept
7. `Boeing Finance Committee charter December 2025 significant investments capital projects mergers acquisitions joint ventures dividends repurchases recommendations to the Board` -> BG-0044 corrected
8. `Boeing Corporate Governance Principles 2026 "Board selects the CEO" long-term interests of the Company and its shareholders independent directors percentage` -> BG-0045 corrected
9. `Boeing 2020 annual meeting independent board chair shareholder proposal majority support percent; board amends governance principles require independent chair` -> BG-0046 kept
10. `Boeing board October 11 2019 separates chairman and CEO roles Calhoun non-executive chairman; December 23 2019 Muilenburg resigns Calhoun CEO January 13 Kellner chairman` -> BG-0047 kept; BG-0048 corrected
11. `Boeing board strips Muilenburg of chairman title October 2019 Calhoun lead director becomes non-executive chairman; shareholders April 2019 rejected proposal to split roles` -> BG-0047 kept
12. `Boeing September 2019 Committee on Airplane Policies and Processes recommendations Product and Services Safety organization Aerospace Safety Committee chaired Giambastiani` -> BG-0049 kept
13. `FAA Section 103 ODA expert panel report Boeing February 26 2024 27 findings 53 recommendations disconnect senior management` -> BG-0050 kept
14. `Boeing directors Caremark derivative suit Vice Chancellor Zurn September 2021 ruling; $237.5 million settlement approved February 2022 governance reforms director with aviation safety expertise` -> BG-0051 kept; BG-0052 kept
15. `Boeing elects David Joyce former GE Aviation CEO to board August 2021 aviation engineering expertise` -> BG-0053 kept
16. `Boeing stock buybacks 2013 to 2019 $43 billion versus commercial airplane R&D Fortune 737 MAX shareholder-first culture` -> BG-0054 kept
17. `Boeing 2024 proxy Commercial Airplanes annual incentive 60% safety quality 40% financial; long-term incentive awards reduced about 22%; Calhoun declined 2023 bonus` -> BG-0055 corrected
18. `Boeing 2026 proxy 2025 annual incentive plan company-wide score free cash flow 40% core EPS revenue 20% Safety & Execution scorecard 20% payout 131%` -> BG-0056 kept
19. `Boeing May 17 2024 annual meeting vote results Calhoun opposed percent say on pay support; Glass Lewis against Calhoun Joyce Johri` -> BG-0058 kept
20. `Boeing institutional ownership percentage 2026 largest shareholders Vanguard BlackRock Fidelity Capital Research employee savings plan` -> BG-0060 corrected
21. `Boeing October 2024 equity offering closes $24.25 billion including overallotment common stock $143 mandatory convertible preferred 6% largest follow-on` -> BG-0062 kept
22. `Boeing completes sale of Jeppesen ForeFlight to Thoma Bravo $10.55 billion November 2025; Boeing completes Spirit AeroSystems acquisition December 8 2025` -> BG-0063 kept (the Spirit close was not found; see 23)
23. `Boeing closes Spirit AeroSystems acquisition December 2025 all-stock $4.7 billion $8.3 billion including debt Airbus work divested` -> BG-0064 kept
24. `Boeing DOJ non-prosecution agreement May 2025 $1.1 billion $444.5 million families $455 million compliance; Judge O'Connor grants dismissal November 2025` -> BG-0065 kept
25. `Boeing board approves 737 MAX launch August 30 2011 496 commitments five airlines; Boeing 777X launch Dubai Airshow November 17 2013 259 orders commitments` -> BG-0067 kept (nothing on the 737 MAX launch; see 26)
26. `"Boeing Launches 737 New Engine Family" 496 airplanes five airlines board of directors approved launch August 2011` -> BG-0066 kept
27. `Ortberg Farnborough July 2026 Boeing not financially ready to launch new airplane two years rebuild balance sheet next single-aisle` -> BG-0068 kept
28. `FAA approves Boeing 737 MAX production increase to 42 per month October 17 2025; Boeing 47 per month FAA approval 2026` -> BG-0069 kept
29. `Boeing Finance Committee charter as affirmed December 12 2024 responsibilities list "capital projects" before December 2025 amendment` -> BG-0044 corrected
30. `Boeing Commercial Airplanes 2024 annual incentive plan 60% quality and safety metrics 40% financial weighting` -> BG-0055 corrected

Outcomes by item:

- BG-0037 (kept): Re-search confirms 12 nominees at the virtual meeting of April 17, 2026 (10 of 12 joined since 2019; 11 of 12 independent; independent chair) and the 8-K: all 12 named, each with more votes for than against; say-on-pay 484,097,165 for, 55,595,642 against.
- BG-0038 (kept): Boeing bio: director since 2020, Independent Board Chair 2024-present, Qualcomm CEO 2014-2021; chosen for his engineering background and record of independent leadership; succeeded Kellner and led the CEO selection.
- BG-0039 (kept): Re-search confirms the December 3, 2025 election and the Aerospace Safety and Finance assignments; the 2026 proxy says 10 of the 12 nominees joined since 2019.
- BG-0040 (kept): The 2026 proxy lists six standing committees: Aerospace Safety, Audit, Compensation, Finance, Governance & Public Policy and Special Programs.
- BG-0041 (kept): Re-search: Joyce chairs Aerospace Safety (third-party profile and CNBC 2024); Johri chairs Finance and sits on Audit, and Doughtie chairs Audit (third-party profile). CNBC and a 2021 Boeing release show Johri chaired Audit until at least 2024, so the Finance chair is a later change; no Boeing document naming the 2026 chairs was reached. Relabelled at the fix pass (2026-10-10) to the sources that support it (VectorShift third-party profile, 2026; CNBC 2024 for Joyce), perspective web_analysis.
- BG-0042 (kept (partial)): Partial: a second third-party profile confirms Bradway as Governance & Public Policy chair (also on Compensation); no result named Lynn Good as Compensation chair. Good's role stays (inference).
- BG-0043 (kept): Charter as amended December 17, 2025: purpose, at least three independent directors, SMS, QMS, product cyber-safety and regulator dealings (FAA, NTSB, DoD, NASA; ODA) all confirmed.
- BG-0044 (corrected): Corrected: the December 17, 2025 charter's purpose and its three areas (transactions; capital structure; significant investments and capital projects) are confirmed, but two searches could not confirm that the capital-projects item was added in 2025 (the December 12, 2024 version was 'affirmed', its list not visible). The 'added in 2025' claim is withdrawn and any 'since December 2025' wording is relabelled.
- BG-0045 (corrected): Corrected: CEO selection, long-term interests and the 75% independence floor are confirmed in the Principles; the June 23, 2026 date belongs to the Director Independence Standards, and the Principles' own current date was not confirmed. The 2026 proxy also says the By-Laws and Principles require an independent Board Chair.
- BG-0046 (kept): Re-search: 52% support (Manhattan Institute), listed by Georgeson as one of two such proposals passed in 2020; adoption in June 2020 on one third-party page (UN PRI); the 2026 proxy confirms the independent-chair requirement.
- BG-0047 (kept): Re-search: split announced late Friday October 11, 2019; Calhoun, the lead director, became non-executive chair; the board had opposed the April 2019 proposal, which failed by about 2 to 1.
- BG-0048 (corrected): Corrected date detail: announced December 23, 2019, but the 8-K gives December 22, 2019 as the effective date of Muilenburg's resignation and Kellner's chairmanship; CFO Greg Smith was interim CEO until Calhoun started on January 13, 2020.
- BG-0049 (kept): Re-search confirms the April 2019 special committee (chaired by Giambastiani), the September 25, 2019 adoption of its recommendations, the permanent committee created in August 2019 and the Product and Services Safety organization; Giambastiani's chairing of the permanent committee was not separately confirmed (he retired from the board at the end of 2021).
- BG-0050 (kept): Re-search confirms February 26, 2024, 27 findings, 53 recommendations, the management disconnect, retaliation doubts and the SMS finding; the six-month action plan was not re-confirmed.
- BG-0051 (kept): Re-search: Vice Chancellor Zurn denied dismissal on September 7, 2021, finding both a failure to set up a safety reporting system and ignored red flags adequately pleaded.
- BG-0052 (kept): Re-search: $237.5 million paid to Boeing by the directors' insurers; final approval hearing February 23, 2022; reforms include an added director with aviation, engineering or product-safety experience and an ombudsman channel (the 'within one year' detail was not re-confirmed).
- BG-0053 (kept): Re-search: Joyce elected August 31, 2021 (Aerospace Safety and Compensation committees), GE Aviation CEO 2008-2020, a former GE engine designer; the chairman cited his safety and engineering expertise.
- BG-0054 (kept): Re-search: $43.1 billion (American Prospect) and $43.5 billion (Leeham) for 2013-2019; Fortune's shareholder-first account confirmed; the R&D comparison ($15.7 billion) was not re-confirmed.
- BG-0055 (corrected): Corrected number: Calhoun's declined 2023 annual incentive target was $2.8 million (not 'about $3 million'). Confirmed: the 22% cut to long-term awards and the 60% operational (quality and safety) / 40% financial weighting for Commercial Airplanes in 2024 (from 75/25 before).
- BG-0056 (kept): Re-search confirms the One Company Score, the 80% financial / 20% safety-quality-execution split and the 131% payout for 2025; the 40/20/20 split inside the financial 80% was not re-confirmed (it rests on the drafter's searches).
- BG-0058 (kept): Re-search: Glass Lewis opposed Calhoun, Joyce (Aerospace Safety chair) and Johri (then Audit chair); all 11 re-elected; about 22% against Calhoun and 36% against the pay package.
- BG-0060 (corrected): Corrected: institutions 71-75% confirmed; Vanguard, BlackRock and FMR each hold roughly 9-10% and their order varies by date (a June 30, 2026 13F tally puts BlackRock first at 10.2%); the other large holder is Capital World Investors (Capital Group), not 'Capital Research'; the 4% savings-plan and 0.1% government figures were not re-confirmed.
- BG-0061 (kept): Re-search confirms Calhoun's announced departure, Kellner not standing for re-election and Mollenkopf as chair leading the CEO selection (March 25, 2024 release); Pope's appointment is in the same release but was not restated by the search summary.
- BG-0062 (kept): Re-search confirms $24.25 billion ($18.5 billion common, 129,375,000 shares; $5.75 billion 6.00% mandatory convertible depositary shares), largest US follow-on on record; priced in late October, closed in early November 2024.
- BG-0063 (kept): Re-search confirms the all-cash $10.55 billion sale of Jeppesen, ForeFlight, AerData and OzRunways to Thoma Bravo, completed in November 2025 (closing reported for November 3).
- BG-0064 (kept): Re-search confirms the December 8, 2025 close, $4.7 billion (Reuters) or $8.3 billion including debt (Boeing), and the required divestiture of Spirit's Airbus work.
- BG-0065 (kept): Re-search confirms the late-May 2025 agreement, over $1.1 billion including $444.5 million for families and over $455 million for compliance, safety and quality, and dismissal on November 6, 2025 over the families' objections (reports differ on the fine itself).
- BG-0066 (kept): Re-search confirms the board's approval on August 30, 2011 on commitments for 496 airplanes from five airlines and a strong business case; LEAP-1B; deliveries from 2017.
- BG-0067 (kept): Now corroborated: launched by McNerney at the November 2013 Dubai Airshow with 259 orders and commitments (Emirates 150, Qatar 50, Etihad 25, Lufthansa 34) worth more than $95 billion. The board's authorisation date is still not found.
- BG-0068 (kept): Re-search confirms Ortberg's Farnborough remarks of July 2026: the financial house needs 'another couple years', the market is not quite ready, and Boeing expects to be able to fund a new programme by about 2030 with the next single-aisle by the end of the next decade; 'evolutionary 737 MAX successor' was not re-confirmed.
- BG-0069 (kept): Re-search confirms the FAA lifting the 38 cap to 42 in October 2025 (the exact day was not re-confirmed) and the capstone review for 47 a month on May 27, 2026, with 52 tied to a new Everett line.
- BG-0057 (not re-searched): the 30-search cap was reached; it stays uncorroborated and is used only as (inference).

## Repo sources (verbatim, machine-checked)

- `transcripts.txt` (Boeing calls 2006-2025): 23 items, BG-0001 to BG-0023, including Chairman Lawrence Kellner at the 2021 Annual Meeting of Shareholders (pages 742-755).
- `boeing_10k.txt`: 13 items, BG-0024 to BG-0036 (10-K FY2024, FY2020, FY2018).
- All 36 pass `wargame/profiles/build/verify_quotes.py` (36/36).
