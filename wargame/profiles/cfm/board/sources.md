# GE Aerospace Board of Directors (`cfm-board`): web sources

Retrieved 2026-10-10 with the WebSearch tool; the container cannot fetch pages. Each web item in `evidence.jsonl`
records the search summary's statement of a fact. It is never verbatim page text and never a quote. Corroboration is a
second, differently worded search that returned the same fact (`corroborated_by`). Where the second source is a
verbatim transcript or filing item already in the repo, the entry names that item ("(repo transcript)" or "(repo
filing)") and has no URL; those items pass `verify_quotes.py`.

- **29 web items:** 25 corroborated and 4 uncorroborated (CG-0052, CG-0067, CG-0068, CG-0069). CG-0051 was corroborated at the 2026-10-10 re-check.
- The uncorroborated items are used only as (inference). They carry no culture score, test, veto ground or reserved matter.
- **Verification pass (2026-10-10).** The verifier could not run its own, differently worded searches: the session's
  web-search budget was exhausted before it started. No web item was dropped or changed for that reason; the items
  stand on the drafter's searches below. Two were re-corroborated against verbatim repo transcripts (CG-0060 with
  CX-0530; CG-0063 with ge_transcripts pp. 38-39), and all were checked for consistency with the transcripts and the
  Capital IQ profile (no conflict found). A later pass with search budget should re-run one new query per item.
- **Re-check (2026-10-10).** A second agent re-ran its own queries (28 searches, listed at the end). It confirmed 25
  items in substance (CG-0041 to CG-0051, CG-0053 to CG-0066); none was contradicted, corrected or dropped. Each
  confirmed item has `"verified": "2026-10-10"`, the re-check query and URL appended to `corroborated_by`, and,
  where a detail was not confirmed, a `recheck_note`. CG-0052, CG-0067, CG-0068 and CG-0069 were not re-searched
  (`"verified": "not re-searched"`) and stay inference only.
- Search summaries were sometimes garbled when they parsed proxy tables. The committee rosters (CG-0045) are taken
  from three searches that agree; one summary flagged the table layout as ambiguous.

## Sources (one line per evidence item)

| Id | Date | Publisher | Title | URL | Corroborating URL(s) or repo item |
|---|---|---|---|---|---|
| CG-0041 | 2026-09-22 | GE Aerospace (press release) | GE Aerospace Board of Directors appoints Wes Bush independent Lead Director | https://www.geaerospace.com/news/press-releases/ge-aerospace-board-directors-appoints-wes-bush-independent-lead-director | https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000059/ex990120260922.htm; https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000059/ge-20260921.htm |
| CG-0042 | 2025-10-01 | GE Aerospace (press release); Form 8-K of 29 September 2025 | Wesley G. Bush joining GE Aerospace Board of Directors | https://www.geaerospace.com/news/press-releases/wesley-g-bush-joining-ge-aerospace-board-directors | https://www.sec.gov/Archives/edgar/data/40545/000004054525000126/ge-20250929.htm; https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf |
| CG-0043 | 2026-06-11 | GE Aerospace (press release) | Judson Althoff joins GE Aerospace Board of Directors | https://www.geaerospace.com/news/press-releases/judson-althoff-joins-ge-aerospace-board-directors | https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000059/ge-20260921.htm; https://www.geaerospace.com/investor-relations/governance |
| CG-0044 | 2026-05-05 | GE Aerospace (SEC EDGAR, DEF 14A filed March 2026; results 8-K) | GE Aerospace 2026 Notice of Annual Meeting and Proxy Statement; 2026 Annual Meeting results | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm | https://www.geaerospace.com/sites/default/files/2026-geaerospace-annual-meeting-results.pdf; https://www.geaerospace.com/investor-relations/governance |
| CG-0045 | 2026-03-12 | GE Aerospace (SEC EDGAR, DEF 14A) | GE Aerospace 2026 proxy statement: Board Committees | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm; https://www.sec.gov/Archives/edgar/data/40545/000004054525000126/ge-20250929.htm; https://www.geaerospace.com/sites/default/files/geaerospace_proxy_2026.pdf |
| CG-0046 | 2026-03-12 | GE Aerospace (committee charter; DEF 14A) | GE Aerospace Classified Programs Committee Charter; 2026 proxy statement | https://www.geaerospace.com/sites/default/files/ClassifiedProgramsCommitteeCharter.pdf | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm |
| CG-0047 | 2025-01-01 | GE Aerospace (governance principles) | GE Aerospace Governance Principles (2025 version; day not given) | https://www.geaerospace.com/sites/default/files/GEAerospaceGovernancePrinciples_0.pdf | https://www.ge.com/sites/default/files/Governance_Principles_2021.pdf |
| CG-0048 | 2026-03-12 | GE Aerospace (SEC EDGAR, DEF 14A) | GE Aerospace 2026 proxy statement: Board's role in risk oversight | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm; https://www.geaerospace.com/sites/default/files/geaerospace_proxy2025.pdf |
| CG-0049 | 2026-03-12 | GE Aerospace (DEF 14A) | GE Aerospace 2026 proxy statement: letter from the Lead Director | https://www.geaerospace.com/sites/default/files/geaerospace_proxy_2026.pdf | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf |
| CG-0050 | 2024-07-01 | GE Aerospace (SEC EDGAR, 8-K) | GE Aerospace Form 8-K: new employment agreement with H. Lawrence Culp, Jr. | https://www.sec.gov/Archives/edgar/data/40545/000095014224001825/eh240502380_8k.htm | https://www.tipranks.com/news/company-announcements/ge-aerospace-confirms-ceos-extension-and-new-compensation-plan; https://www.aol.com/ge-aerospace-signs-larry-culp-125840105.html |
| CG-0051 | 2025-03-13 | GE Aerospace (SEC EDGAR, DEF 14A) | GE Aerospace 2025 proxy statement: PSU design | https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge4356871-def14a.htm | https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge_courtesy-pdf.pdf (re-check 2026-10-10, search 28) |
| CG-0052 | 2026-03-12 | GE Aerospace (SEC EDGAR, DEF 14A) | GE Aerospace 2026 proxy statement: Annual Executive Incentive Plan | https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm | **uncorroborated** (single search; inference only) |
| CG-0053 | 2025-05-06 | GE Aerospace (annual meeting results); 8-K of 6 May 2025 | GE Aerospace 2025 Annual Meeting results | https://www.geaerospace.com/sites/default/files/2025-geaerospace-annual-meeting-results.pdf | https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge4356871-def14a.htm |
| CG-0054 | 2021-05-04 | Bloomberg | GE CEO's $232 Million Pay Deal Draws Shareholder Rebuke | https://www.bloomberg.com/news/articles/2021-05-04/ge-ceo-s-232-million-pay-deal-draws-rebuke-from-shareholders | https://www.bostonglobe.com/2021/05/03/business/ge-chief-executive-larry-culps-compensation-faces-scrutiny-shareholder-vote |
| CG-0055 | 2018-10-01 | Bloomberg | GE Ousts Flannery After Slump, Names Lawrence Culp CEO | https://www.bloomberg.com/news/articles/2018-10-01/ge-taps-culp-to-replace-ceo-flannery-will-miss-profit-guidance | https://www.cnbc.com/2018/10/01/ge-removes-flannery-as-ceo-takes-23-billion-non-cash-charge-for-power-business-problems-and-withdraws-guidance.html |
| CG-0056 | 2017-11-13 | CNN Money | GE cuts dividend for second time since Great Depression | https://money.cnn.com/2017/11/13/investing/ge-dividend-cut/index.html | (repo transcript) GE investor conference 2017-11-14, Jamie Miller: 'you saw that we cut the dividend yesterday by 50%' (CX-1154) |
| CG-0057 | 2018-10-30 | AP via WTOP | GE Cuts Quarterly Dividend to 1 Cent | https://wtop.com/news/2018/10/ge-cuts-quarterly-dividend-to-1-cent/ | https://www.fortune.com/2018/10/30/ge-culp-dividend-power; (repo transcript) CX-0234, ge_transcripts p1662 |
| CG-0058 | 2017-06-19 | Treasury & Risk; Bloomberg Opinion; Fox Business; IndustryWeek | GE's Immelt leaves behind $31B pension deficit (buyback data); related coverage of GE buybacks and the Trian stake | https://www.treasuryandrisk.com/2017/06/19/ges-immelt-leaves-behind-31b-pension-deficit | https://www.industryweek.com/global-economy/ge-shares-jump-activist-peltz-reports-stake |
| CG-0059 | 2024-02-29 | GE (press release); 8-K | GE Board of Directors approves spin-off of GE Vernova; GE Vernova and GE Aerospace to launch | https://www.ge.com/news/press-releases/ge-board-of-directors-approves-spin-off-of-ge-vernova-ge-vernova-and-ge-aerospace-to | (repo transcript) 2024 AGM, ge_transcripts p157: directors departed 'with the spin- off of GE Vernova on the 2nd of April' (CG-0004 context); https://ainonline.com/aviation-news/aerospace/2024-04-02/ge-aerospace-marks-independence-spinoff-ge-vernova |
| CG-0060 | 2022-06-27 | Reuters via Boston Globe | GE CEO Culp takes reins of aviation unit as Slattery loses top post | https://www.bostonglobe.com/2022/06/27/business/ge-ceo-culp-takes-reins-aviation-unit-slattery-loses-top-post | (repo transcript) CX-0530, ge_transcripts p643 (2022-07-26); replaced at verification a proxy search that did not state the 2022 change |
| CG-0061 | 2025-12-31 | GE Aerospace (SEC EDGAR, 10-Q Q1 2026) | GE Aerospace 10-Q: $20 billion share repurchase authorization | https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000027/ge-20260331.htm | https://www.nasdaq.com/articles/ge-aerospaces-robust-capital-position-fuels-higher-shareholder-returns |
| CG-0062 | 2026-02-06 | GE Aerospace (press release) | GE Aerospace Board of Directors authorizes quarterly dividend | https://www.geaerospace.com/news/press-releases/ge-aerospace-board-directors-authorizes-quarterly-dividend | https://www.marketbeat.com/instant-alerts/ge-aerospace-nysege-raises-dividend-to-047-per-share-2026-03-07/ |
| CG-0063 | 2025-07-17 | GE Aerospace (SEC EDGAR, 8-K earnings release) | GE Aerospace reports second quarter 2025 results; raises 2025 guidance and 2028 outlook | https://www.sec.gov/Archives/edgar/data/40545/000004054525000108/ge2q2025earningsrelease.htm | (repo transcript) ge_transcripts p38-39 (2025-07-17: 2028 outlook, RISE tests), added at verification; CX-0644 and CX-0645, ge_transcripts p42 |
| CG-0064 | 2026-02-02 | GE Aerospace (SEC EDGAR, 10-Q) | GE Aerospace 10-Q Q2 2026: credit ratings (Moody's upgrade to A2) | https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000049/ge-20260630.htm | https://ts2.tech/en/ge-aerospace-stock-price-today-moodys-upgrade-and-singapore-tech-deals-lift-ge-shares/; (repo filing) CG-0002, ge_ciq p3: S&P A- stable, Mar-25-2025 |
| CG-0065 | 2021-06-14 | GE Aviation and Safran (joint press release, Business Wire) | GE Aviation and Safran Launch Advanced Technology Demonstration Program for Sustainable Engines, Extend CFM Partnership to 2050 | https://www.businesswire.com/news/home/20210614005533/en/GE-Aviation-and-Safran-Launch-Advanced-Technology-Demonstration-Program-for-Sustainable-Engines-Extend-CFM-Partnership-to-2050 | https://www.airdatanews.com/ge-and-safran-launch-cfm-rise-program-which-forecasts-new-engine-20-more-efficient/; https://www.cfmaeroengines.com/press-articles/ge-safran-renew-cfm-partnership-until-2040/ |
| CG-0066 | 2024-02-02 | GE (SEC EDGAR, 10-K); GE Aerospace; CNBC | GE 10-K FY2023: CFM International collaborative arrangement | https://www.sec.gov/Archives/edgar/data/40545/000004054524000027/ge-20231231.htm | https://www.geaerospace.com/news/articles/technology/ge-aviation-and-safran-launch-advanced-technology-demonstration-program |
| CG-0067 | 2008-07-13 | CFM International / GE Aerospace (press release) | GE, Safran renew CFM partnership until 2040 | https://www.cfmaeroengines.com/press-articles/ge-safran-renew-cfm-partnership-until-2040/ | **uncorroborated** (single search; inference only) |
| CG-0068 | 2017-02-01 | CFM International | CFM International president and CEO Gael Meheust | https://www.cfmaeroengines.com/about/gael-meheust/ | **uncorroborated** (single search; inference only) |
| CG-0069 | 2025-03-05 | Manufacturing Dive; Reuters via Yahoo Finance | GE Aerospace to invest nearly $1 billion in U.S. manufacturing and supply chain | https://www.manufacturingdive.com/news/ge-aerospace-nearly-1-billion-investment-u-s-engine-suppliers/742313/ | **uncorroborated** (single search; inference only) |

## Other primary documents seen in results (not cited as items)

- GE Aerospace 2026 proxy (PDF): https://www.geaerospace.com/sites/default/files/geaerospace_proxy_2026.pdf
- GE Aerospace 2025 proxy (PDF): https://www.geaerospace.com/sites/default/files/geaerospace_proxy2025.pdf
- GE Aerospace governance page: https://www.geaerospace.com/investor-relations/governance
- Management Development and Compensation Committee charter: https://www.geaerospace.com/sites/default/files/ge-aerospace-management-development-and-compensation-committee-charter.pdf
- Audit Committee charter: https://www.geaerospace.com/sites/default/files/ge-aerospace-audit-committee-charter.pdf
- Governance and Public Affairs Committee charter (2024): https://www.geaerospace.com:443/sites/default/files/gpac-charter-04-05-24_0.pdf
- GE Aerospace product safety and SMS material: https://www.geaerospace.com/sites/default/files/product-safety-2024.pdf

## Queries used (in order; 50 run)

1. GE Aerospace 2026 proxy statement board of directors nominees
2. GE Aerospace board of directors lead independent director 2025
3. Wes Bush elected lead director GE Aerospace September 2026
4. GE Aerospace 8-K September 22 2026 board announcement
5. Althoff joins GE Aerospace board of directors June 2026
6. GE Aerospace 2026 annual meeting results directors elected Garden Bazin not standing
7. GE Aerospace proxy 2026 nominees Angel Bazin Billson Bush Enders Goren Horton Lesjak McDew Culp (extended mode)
8. Wesley G. Bush joining GE Aerospace Board of Directors Steve Angel step down
9. GE Aerospace Management Development and Compensation Committee chair 2026 committee membership
10. GE Aerospace Governance and Public Affairs Committee chair 2026 proxy Billson Horton
11. "Lesjak" GE Aerospace compensation committee chair Angel CSX
12. GE Aerospace governance principles board responsibilities review approve strategy major risks capital allocation
13. GE governance principles "board" functions "review and, where appropriate, approve" major strategic financial and business objectives
14. GE board approval threshold acquisitions capital expenditures delegation of authority CEO limit (no GE-specific result)
15. GE Aerospace 2025 performance stock units metrics EPS free cash flow relative TSR three-year proxy
16. GE Aerospace annual bonus plan metrics operating profit free cash flow safety quality delivery 2025 executive compensation
17. GE Aerospace Culp employment agreement extension 2028 one-time performance award
18. GE Aerospace board oversight of product safety flight safety committee proxy risk oversight
19. Horton letter from lead director GE Aerospace 2026 proxy deep dive next generation propulsion
20. GE board ousts Flannery names Culp CEO October 2018 first outsider
21. Larry Culp replaces John Flannery General Electric board unanimously October 1 2018 goodwill charge
22. GE cuts dividend in half November 2017 second cut since Great Depression
23. General Electric slashes dividend to 1 cent October 2018 Culp
24. GE share buybacks 2015 2016 2017 Immelt billions at high prices capital allocation mistake
25. Trian Peltz GE 2015 stake pushed buybacks $50 billion repurchase plan
26. CFM International 50/50 joint venture GE Safran governance equal partnership extended to 2050
27. CFM International board of directors composition GE Safran representatives president CEO rotation
28. Safran universal registration document CFM International joint control GE Aerospace revenue sharing workshare 50/50 decisions (no governance detail found)
29. GE Aerospace 10-K CFM International collaborative arrangement Safran "jointly" engine program revenue sharing
30. GE Aerospace board authorizes quarterly dividend 2026 increase share repurchase authorization
31. GE Aerospace new $20 billion buyback program December 2025 dividend raised to 47 cents
32. "GE Aerospace" "$0.47 per share" dividend February 2026
33. GE Aerospace R&D spending 2025 total research and development billion RISE open fan investment (no total R&D figure found)
34. CFM RISE open fan engine entry into service mid-2030s Safran GE launch decision next narrowbody
35. GE Aerospace launches independent company April 2 2024 GE Vernova spin Culp chairman CEO
36. Culp took over as CEO of GE Aerospace business July 2022 Slattery leaves
37. GE Aerospace 2025 annual meeting say on pay support percent shareholder proposals results
38. GE Aerospace Culp pay ISS Glass Lewis recommendation 2025 say-on-pay vote opposition
39. GE shareholders reject executive pay vote May 2021 Culp $230 million award
40. GE Aerospace first engine manufacturer FAA accepted safety management system SMS (fact used through transcript item CG-0018 instead)
41. GE Aerospace proxy statement "safety" board oversight "risk" committee responsibilities aviation safety quality enterprise risk (extended mode)
42. GE Aerospace Audit Committee oversees enterprise risk management framework Board focuses on most significant risks
43. GE Aerospace board "Classified Programs Committee" members purpose
44. GE Aerospace classified programs committee formed 2025 national security oversight board (no relevant results)
45. S&P upgrades GE Aerospace rating A- 2025 Moody's A3 credit rating
46. GE Aerospace July 2025 investor update 2028 outlook capital allocation $24 billion returns R&D
47. GE Aerospace committee assignments 2026 Audit Compensation Governance Classified Programs McDew Bush Culp
48. Moody's upgrades General Electric GE Aerospace senior unsecured to A2 outlook
49. GE Aerospace invest nearly $1 billion US manufacturing 2025 2026 plants supply chain announcement
50. GE Safran renew CFM partnership until 2040 LEAP launch 2008 agreement
51. LEAP engine launched 2008 without aircraft application first customer COMAC C919 December 2009 CFM (not run: the session's web-search budget was exhausted, so CG-0067 stays uncorroborated)

## Re-check queries (2026-10-10; 28 run, the cap)

1. GE Aerospace Wes Bush independent Lead Director Tom Horton September 2026 -> CG-0041: https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000059/ex990120260922.htm
2. Wesley G. Bush joining GE Aerospace Board of Directors Stephen Angel CSX -> CG-0042: https://intelligencecommunitynews.com/wesley-bush-joins-ge-aerospace-board/
3. Judson Althoff joins GE Aerospace Board of Directors -> CG-0043: https://www.geaerospace.com/news/investor-relations/ir-updates/welcoming-microsofts-judson-althoff
4. GE Aerospace 2026 annual meeting results directors elected Ed Garden not standing for re-election -> CG-0044: https://www.geaerospace.com/sites/default/files/2026-geaerospace-annual-meeting-results.pdf
5. GE Aerospace 2026 proxy committee chairs Goren Audit Lesjak Compensation Horton Governance McDew Classified Programs -> CG-0044, CG-0045, CG-0046 (four committees, Classified Programs formed June 2025; chairs not shown (resolved by search 7)): https://www.geaerospace.com/investor-relations/governance; https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm
6. GE Aerospace Classified Programs Committee established June 2025 charter -> CG-0046 (charter content; date conflict noted, unverified): https://www.geaerospace.com/sites/default/files/ClassifiedProgramsCommitteeCharter.pdf
7. GE Aerospace board committee assignments chair Audit Committee Goren Management Development Compensation Committee chair Lesjak -> CG-0042, CG-0045: https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf; https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge4356871-def14a.htm
8. GE Aerospace Governance Principles board functions "fundamental financial and business strategies and major corporate actions" -> CG-0047: https://www.geaerospace.com/sites/default/files/GEAerospaceGovernancePrinciples_0.pdf
9. GE Aerospace proxy 2026 board risk oversight Audit Committee enterprise risk management Governance and Public Affairs health and safety risks -> CG-0048 (Audit ERM and executive risk committee; Governance health-and-safety not found): https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-courtesy.pdf
10. GE Aerospace 2026 proxy letter from Lead Director Horton board dedicated reviews strategic topics each core business -> letter found, deep-dive wording not seen (resolved by search 27)
11. GE Culp new employment agreement June 2024 through 2027 base salary $2 million one-time performance stock units EPS -> CG-0050: https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge4356871-def14a.htm
12. GE Aerospace 2025 say on pay vote 71% support Culp compensation -> CG-0050, CG-0053: https://fintool.com/app/research/companies/GE/people/larry-culp; https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm
13. GE shareholders reject executive pay 2021 vote 58% against Culp $232 million -> CG-0054: https://www.cfo.com/news/ge-shareholders-reject-pay-plan-for-ceo-culp/655649/
14. GE board names Larry Culp chairman CEO replaces Flannery October 1 2018 Horton lead director unanimous -> CG-0055: https://www.ge.com/news/press-releases/h-lawrence-culp-jr-named-chairman-and-ceo-ge
15. GE cuts dividend in half November 2017 24 cents to 12 cents, then October 2018 cuts to one cent -> CG-0056 (November 2017 cut only; October 2018 not covered (resolved by search 25)): https://fortune.com/2017/11/13/ge-dividends-general-electric-stock
16. GE share buybacks 2015 2016 $22 billion Trian Peltz stake $2.5 billion recommended debt-funded buyback -> CG-0058 (Trian stake and debt-funded buyback thesis; $22-24bn yearly figure not found): https://foxbusiness.com/features/ges-performance-under-scrutiny; https://www.industryweek.com/the-economy/article/21966049/ge-shares-jump-as-activist-peltz-reports-stake
17. GE board approves spin-off of GE Vernova February 29 2024 distribution April 2 one share for every four -> CG-0059: https://www.gevernova.com/news/press-releases/ge-board-of-directors-approves-spin-off-of-ge-vernova-ge-vernova-and-ge-aerospace-to
18. Culp becomes CEO of GE Aviation June 2022 Slattery chief commercial officer -> CG-0060: https://www.ge.com/news/press-releases/ge-announces-changes-to-ge-aviation-senior-leadership-team
19. GE Aerospace board approves new $20 billion share repurchase authorization December 2025 dividend $0.47 -> CG-0062 ($0.47 dividends; $20B buyback not surfaced (resolved by search 23)): https://www.placera.se/pressmeddelanden/ge-aerospace-board-of-directors-authorizes-quarterly-dividend-20260206
20. GE Aerospace July 2025 raises 2028 outlook operating profit $11.5 billion free cash flow $8.5 billion $24 billion shareholder returns 70% -> CG-0063: https://www.geaerospace.com/news/press-releases/ge-aerospace-announces-second-quarter-2025-results
21. Moody's upgrades GE Aerospace to A2 February 2026 P-1 positive outlook -> CG-0064: https://www.kapitalmarktexperten.de/ge-aerospace-aktie-erstaunlicher-umsatzzuwachs/
22. GE Aviation Safran extend CFM International partnership to 2050 launch CFM RISE June 2021 -> CG-0065: https://www.ge.com/news/press-releases/ge-aviation-and-safran-launch-advanced-technology-demonstration-program-for
23. "GE Aerospace" "$20 billion" share repurchase program authorized December 2025 -> CG-0061: https://www.zacks.com/stock/news/2978532/ge-aerospace-s-robust-capital-position-fuels-higher-shareholder-returns
24. GE 10-K CFM International collaborative arrangement Safran Aircraft Engines jointly owned non-consolidated sells LEAP CFM56 engines -> CG-0066 (50/50 ownership, CFM56 and LEAP; 10-K wording not reached): https://www.safran-group.com/companies/cfm-international
25. General Electric slashes quarterly dividend to 1 cent October 30 2018 Culp first move -> CG-0057: https://www.business-standard.com/amp/article/reuters/ge-cuts-dividend-splits-power-business-118103000811_1.html
26. GE Aerospace Governance and Public Affairs Committee charter oversees risks health and safety political activities lobbying -> CG-0048 (political spending and lobbying, ESG and climate risk; health and safety not found): https://www.geaerospace.com:443/sites/default/files/gpac-charter-04-05-24_0.pdf
27. GE Aerospace 2026 proxy statement Lead Director letter engine deliveries up 26% board deep dives strategy -> CG-0049: https://www.sec.gov/Archives/edgar/data/40545/000004054526000018/ge-20260312.htm
28. GE Aerospace performance stock units 2025 adjusted EPS free cash flow three-year relative TSR modifier S&P 500 Industrials -> CG-0051: https://www.sec.gov/Archives/edgar/data/40545/000130817925000114/ge_courtesy-pdf.pdf
