# Rolls-Royce Holdings plc Board: sources (`rolls-royce-board`)

Sources for the board profile of Rolls-Royce Holdings plc (`board.md`) and its evidence file (`evidence.jsonl`,
RG-0001 to RG-0070). Research date: 2026-10-10.

## 1. Web sources

Retrieved 2026-10-10 with the WebSearch tool; the container cannot fetch pages. Each web item in `evidence.jsonl`
records the search summary's statement of a fact (`quote`). It is never verbatim page text and never a quote of
anyone's speech. Corroboration (`corroborated_by`) is a second, differently worded search that returned the same
fact, or, where marked "(repo transcript)" or "(repo filing)", a verbatim item already in the repo that passes
`verify_quotes.py`.

- **24 web items (RG-0047 to RG-0070):** 22 corroborated and 2 uncorroborated (RG-0069, RG-0070). The uncorroborated items are
  used only as (inference) and carry no culture score, test, veto ground or reserved matter.

- Where a detail inside a corroborated item came from one search only, the item has a `recheck_note` and that
  detail is used only as (inference): RG-0047 (roster assembled from two searches), RG-0048 (Frew chairs the
  Nominations, Culture & Governance Committee), RG-0049 (that SETT merged the two earlier committees), RG-0050 (no
  2025-2026 re-confirmation of the committee chairs), RG-0053 (dates and backgrounds of the 2022-23 changes),
  RG-0054 (the delegation clause to the Chief Executive), RG-0056 (employee plan page), RG-0058 (bonus weights).

- **History.** An earlier pass on the same date recorded no web item: its queries were refused because the turn's
  search budget was used up, so composition was dated 8 July 2022 (RG-0001). This pass ran with its own budget
  (cap 45 searches) and used all 45: 43 tool calls, two of which (searches 14 and 23) ran two searches each
  (counted as 15 and 24). Composition is now dated 1 September 2026.

- Search summaries sometimes disagreed on small details (the date of the SMR contract signing, job numbers, the
  date of the AGM script). Items keep only what two searches agree on, or say which detail is single-sourced.

### Sources (one line per evidence item)

| Id | Date | Publisher | Title | URL | Corroborating search(es) or repo item |
|---|---|---|---|---|---|
| RG-0047 | 2026-04-30 | Rolls-Royce Holdings plc (AGM poll results, RNS) | Rolls-Royce Holdings plc 2026 AGM poll results; 2026 Notice of AGM | https://www.mylearning.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/rr-agm-poll-results.pdf | (search 34) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/2026-notice-of-agm.pdf; (search 1) https://www.fidelity.co.uk/factsheet-data/factsheet/GB00B63H8491-rolls-royce-holdings/profile |
| RG-0048 | 2026-05-01 | Rolls-Royce plc (board page); Fidelity International (factsheet) | Rolls-Royce Holdings PLC (RR.) factsheet: profile; Rolls-Royce board page | https://www.rolls-royce.com/about/leadership/board.aspx | (search 1) https://www.fidelity.co.uk/factsheet-data/factsheet/GB00B63H8491-rolls-royce-holdings/profile; (search 2) https://www.rolls-royce.com/about/leadership/board.aspx; (search 42) https://www.rolls-royce.com/about/leadership/board.aspx; (search 31) https://www.rolls-royce.com/about/leadership/board.aspx; (repo filing) Form F-6 signature page, 8 July 2022: 'George Culmer Senior Independent Director' (RG-0001) |
| RG-0049 | 2023-05-10 | Rolls-Royce Holdings plc (RNS via LSE.co.uk) | Rolls-Royce Holdings plc RNS: Directorate change and withdrawal of AGM resolution (10 May 2023) | https://lse.co.uk/rns/RR./directorate-change-withdrawal-of-agm-resolution-g5e7e1q5ds4vmii.html?page=11 | (search 9) https://www.investegate.co.uk/announcement/7523386; (search 32) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/investors/agm-chair-and-ceo-scripts.pdf; (search 6) https://www.stockopedia.com/share-prices/rolls-royce-holdings-LON:RR./news/rolls-royce-holdings-non-executive-director-appointments-019ef8db-fb14-76b9-b42f-8ef1199046d5/ |
| RG-0050 | 2024-01-01 | Rolls-Royce Holdings plc (AGM scripts) | AGM chair and CEO scripts (2024 AGM; day not given) | https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/investors/agm-chair-and-ceo-scripts.pdf | (search 32) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2023/governance-report.pdf; (search 2) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/investors/agm-chair-and-ceo-scripts.pdf |
| RG-0051 | 2026-06-24 | Rolls-Royce Holdings plc (RNS via Stockopedia) | Rolls-Royce Holdings - Non-Executive Director Appointments (RNS, 24 June 2026) | https://www.stockopedia.com/share-prices/rolls-royce-holdings-LON:RR./news/rolls-royce-holdings-non-executive-director-appointments-019ef8db-fb14-76b9-b42f-8ef1199046d5/ | (search 7) https://www.boerse-express.com/news/articles/rolls-royce-aktie-watkins-und-genco-ins-board-921149; (search 7) https://ground.news/article/rolls-royce-appoints-high-profile-neds |
| RG-0052 | 2023-05-10 | Rolls-Royce Holdings plc (RNS via LSE.co.uk, Investegate) | Rolls-Royce Holdings plc RNS: Directorate change; Result of AGM (May 2023) | https://lse.co.uk/rns/RR./directorate-change-withdrawal-of-agm-resolution-g5e7e1q5ds4vmii.html?page=11 | (search 9) https://www.investegate.co.uk/announcement/7523386; (search 34) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/2026-notice-of-agm.pdf |
| RG-0053 | 2023-09-01 | BoardAgenda; Rolls-Royce Holdings plc (RNS) | Board changes 2022-2023 (Rolls-Royce RNS; BoardAgenda; company listings) | https://boardagenda.com/2023/02/09/rolls-royce-appoints-ned/ | (search 34) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/2026-notice-of-agm.pdf; (search 10) https://www.mylearning.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/rr-agm-poll-results.pdf |
| RG-0054 | 2024-12-10 | Rolls-Royce Holdings plc (governance document) | Board Governance (including matters reserved for the Board and the terms of reference of its committees), amended 10 December 2024 | https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/about/board-governance-inc-matters-reserved-for-the-board-and-its-committees-terms-of-reference-dec-2024.pdf | (search 5) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/about/board-governance-inc-matters-reserved-for-the-board-and-its-committees-terms-of-reference-dec-2024.pdf; (search 43) https://www.rolls-royce.com/about/leadership/corporate-governance.aspx |
| RG-0055 | 2026-04-30 | Rolls-Royce Holdings plc (remuneration policy); City A.M.; interactive investor | Directors' Remuneration Policy 2026 (approved at the 2026 AGM); press coverage | https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/directors-remuneration-policy-2026.pdf | (search 12) https://www.cityam.com/rolls-royce-boss-turbo-tufan-gets-backing-for-18m-pay-packet/; (search 17) https://www.ii.co.uk/analysis-commentary/agm-alert-rolls-royce-bp-relx-ii538449; (search 45) https://data.fca.org.uk/artefacts/NSM/RNS/7636886e-0885-4c3b-8d3b-387d824555da.html |
| RG-0056 | 2026-01-01 | Rolls-Royce plc (share plans website) | LTIP - connecting you to our long-term success (Rolls-Royce share plans; 2026 targets, day not given) | https://shareplans.rolls-royce.com/de-en/shareplans/ltip | (search 14) https://shareplans.rolls-royce.com/es-en/shareplans/ltip; (search 13) https://shareplans.rolls-royce.com/hk-en/shareplans/ltip |
| RG-0057 | 2026-05-01 | Rolls-Royce Holdings plc (RNS, FCA NSM) | Rolls-Royce Holdings plc RNS 8509C: Director/PDMR shareholding (LTIP grants, 1 May 2026) | https://data.fca.org.uk/artefacts/NSM/RNS/7636886e-0885-4c3b-8d3b-387d824555da.html | (search 44) https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/directors-remuneration-policy-2026.pdf; (search 13) https://shareplans.rolls-royce.com/de-en/shareplans/ltip |
| RG-0058 | 2026-03-05 | Rolls-Royce Holdings plc (annual report); interactive investor | Rolls-Royce Holdings plc Annual Report 2025: Directors' remuneration report | https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/rr-plc-annual-report-2025.pdf | (search 17) https://www.ii.co.uk/analysis-commentary/agm-alert-rolls-royce-bp-relx-ii538449; (search 17) https://simplywall.st/stocks/us/capital-goods/otc-ryce.f/rolls-royce-holdings/management |
| RG-0059 | 2026-02-26 | Rolls-Royce Holdings plc (results press release) | Rolls-Royce Holdings plc 2025 full year results (26 February 2026) | https://www.rolls-royce.com/media/press-releases/2026/26-02-2026-rr-holdings-plc-2025-full-year-results | (search 19) https://www.ajbell.co.uk/news/articles/rolls-royce-raises-guidance-and-plans-bumper-buyback-profit-surge; (search 19) https://www.proactiveinvestors.co.uk/companies/news/1087961/rolls-royce-plans-9bn-of-buybacks-and-raises-outlook-after-strong-year-1087961.html |
| RG-0060 | 2026-07-30 | Rolls-Royce Holdings plc (results press release) | Rolls-Royce Holdings plc 2026 half year results (30 July 2026) | https://www.rolls-royce.com/media/press-releases/2026/30-07-2026-rr-holdings-plc-2026-half-year-results.aspx | (search 37) https://www.ajbell.co.uk/news/articles/rolls-royce-shares-climb-lifts-annual-outlook-after-first-half-beat; (search 21) https://www.boerse-express.com/news/articles/rolls-royce-aktie-moodys-und-fitch-stufen-auf-a3a-hoch-900125 |
| RG-0061 | 2024-12-31 | BondBlox | Rolls-Royce returns to IG status on upgrade to Baa3 (BondBlox; 2024, day not given) | https://bondblox.com/news/rolls-royce-returns-to-ig-status-on-upgrade-to-baa3 | (repo transcript) FY2024 results call, 2025-02-27, Erginbilgic: 'We now have a strong balance sheet with an investment-grade rating from all three agencies.' (RX-0102); (search 21) https://www.finanztrends.de/news/rolls-royce-aktie-moodys-stuft-auf-a3-hoch/ |
| RG-0062 | 2023-11-28 | Rolls-Royce plc (press release) | Rolls-Royce targets a step change in mid-term performance (Capital Markets Day press release, 28 November 2023) | https://www.rolls-royce.com/media/press-releases/2023/28-11-2023-capital-markets-day.aspx | (repo transcript) Capital Markets Day 2023-11-28, McCabe: 'In the midterm, which we see as being around 2027, we are targeting between GBP 2.8 billion and GBP 3.1 billion of free cash flow' (RX-0217); (search 28) https://streaming1.www.ajbell.co.uk/articles/latestnews/269028/top-news-rolls-royce-could-exit-electric-lays-out-2027-targets |
| RG-0063 | 2023-01-27 | The Irish Times (Reuters; Financial Times) | Rolls-Royce's new chief warns company is a 'burning platform' (Irish Times, from Reuters and the FT) | https://irishtimes-irishtimes-prod.cdn.arcpublishing.com/business/2023/01/27/rolls-royces-new-chief-warns-company-is-a-burning-platform | (search 41) https://www.morningstar.co.uk/uk/news/AN_1674811089375616200/press-rolls-royce-new-chief-warns-last-chance-to-shake-up-firm.aspx; (search 41) https://fortune.com/europe/2023/10/17/rolls-royce-ceo-tufan-erginbilgic-burning-platform-layoffs-2500-jobs |
| RG-0064 | 2022-07-26 | Rolls-Royce plc (press release) | Rolls-Royce appoints Tufan Erginbilgic as Chief Executive Officer (press release, 26 July 2022) | https://www.rolls-royce.com/media/press-releases/2022/26-07-2022-rr-appoints-tufan-erginbilgic-as-chief-executive-officer.aspx | (repo transcript) Special call 2022-02-24, Frew: 'we're now starting an open and transparent search process for Warren's successor' (RG-0010); (repo transcript) FY2022 results 2023-02-23, Erginbilgic as CEO: 'Rolls-Royce has been underperforming for an extended period.' (RX-0038); (search 27) https://www.peoplematters.in/news/appointments/rolls-royce-appoints-tufan-erginbilgic-as-chief-executive-officer-34716 |
| RG-0065 | 2026-02-26 | Leeham News; Metal AM; American Machinist; ADS Group | Rolls-Royce boosts mid-term targets, CEO dismisses UltraFan loan speculation (Leeham News, 26 February 2026); UltraFan 30 funding reports | https://leehamnews.com/2026/02/26/rolls-royce-boosts-mid-term-targets-ceo-dismisses-ultrafan-loan-speculation/ | (search 23) https://www.metal-am.com/rolls-royce-seeks-uk-funding-for-3b-ultrafan-30-engine-programme/; (search 22) https://www.americanmachinist.com/news/news/55361120/new-narrow-body-jet-engine-proposed-rolls-royce; (search 40) https://www.adsgroup.org.uk/knowledge/industry-member-news/rolls-royce-to-advance-ultrafan-30-demonstrator-through-unified/ |
| RG-0066 | 2026-04-13 | World Nuclear News | Contract signed for delivery of UK's first SMRs (World Nuclear News) | https://world-nuclear-news.org/articles/contract-signed-for-delivery-of-uks-first-smrs | (search 25) https://www.ans.org/news/2026-04-15/article-7937/rollsroyce-gben-contract-kickstarts-uks-smr-plans-for-wylfa-site/; (search 25) https://www.cibsejournal.com/news/government-green-lights-first-uk-small-modular-reactor/ |
| RG-0067 | 2022-05-12 | Rolls-Royce Holdings plc (Articles of Association); IndustryWeek; CMC Markets | Rolls-Royce Holdings plc Articles of Association (as amended 12 May 2022); reports on the special share | https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2022/rr-holdings-plc-articles-of-association.pdf | (search 30) https://www.cmcmarkets.com/en-gb/opto/will-the-uk-government-veto-a-rolls-royce-takeover; (search 29) https://www.industryweek.com/archive/britain-lifts-foreign-ownership-limits-bae-rolls-royce |
| RG-0068 | 2025-06-12 | Rolls-Royce plc (press release); AviTrader; AIN | Rolls-Royce launches Durability Enhancement Package that will double Trent 1000 Time-on-Wing (press release, 12 June 2025) | https://www.rolls-royce.com/media/press-releases/2025/12-06-2025-rr-launches-durability-enhancement-package-that-will-double-trent-1000-time-on-wing.aspx | (repo transcript) H1 2025 results 2025-07-31, Erginbilgic: 'The upgraded Trent 1000 HPT blade was certified in June, which will more than double the time on wing on these engines.' (RX-0129); (repo transcript) 2025-07-31: 'we allocated GBP 1 billion investment in 4 years.' (RX-0123); (search 38) https://avitrader.com/2025/06/13/rolls-royce-launches-trent-1000-durability-enhancement-package |
| RG-0069 | 2026-04-01 | Rolls-Royce Holdings plc | Terms and conditions of non-executive directors (April 2026) | https://www.mylearning.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/about/terms-and-conditions-of-non-executive-directors-april-2026.pdf | **uncorroborated** (single search; inference only) |
| RG-0070 | 2026-04-01 | Rolls-Royce Holdings plc (RNS via Shares Magazine; ticker.app) | Holding(s) in Company (WCM, 16 June 2025); Total Voting Rights (April 2026) | https://sharesmagazine.co.uk/news/market/LSE20250616174500_5698021/holdings-in-company | **uncorroborated** (single search; inference only) |

### Queries used (2026-10-10)

| # | Query | Items |
|---|---|---|
| 1 | Rolls-Royce Holdings board of directors 2026 chair Anita Frew senior independent director | RG-0047, RG-0048, RG-0069 |
| 2 | Rolls-Royce Annual Report 2025 board of directors Culmer Senior Independent Director committees | RG-0048, RG-0050 |
| 3 | Rolls-Royce "matters reserved for the Board" terms of reference December 2024 Safety Energy Transition Technology Committee | RG-0049, RG-0054 |
| 4 | Rolls-Royce board governance matters reserved approval of major capital projects acquisitions disposals threshold delegated authority Chief Executive | RG-0054 |
| 5 | Rolls-Royce plc board delegated to the Chief Executive powers reserved paragraphs 2.2 strategy capital expenditure contracts value | RG-0054 |
| 6 | Rolls-Royce Holdings appoints non-executive director 2025 directorate change | RG-0049, RG-0051 |
| 7 | Gretchen Watkins Alessandra Genco Rolls-Royce board June 2026 | RG-0051 |
| 8 | Rolls-Royce board members Birgit Behrendt Paulo Cesar Silva Wendy Mars Jitesh Gadhia Nick Luff Paul Adams Angela Strank | RG-0053 |
| 9 | Rolls-Royce directorate change withdrawal of AGM resolution May 2023 non-executive director stepping down | RG-0049, RG-0052 |
| 10 | Rolls-Royce Holdings 2026 Annual General Meeting results re-election of directors poll | RG-0047, RG-0053 |
| 11 | Rolls-Royce 2026 notice of AGM new directors' remuneration policy performance share plan changes | RG-0055 |
| 12 | Erginbilgic pay deal doubled long-term incentive Rolls-Royce shareholders vote 2026 | RG-0055 |
| 13 | Rolls-Royce performance share plan 2025 award measures free cash flow relative TSR operating profit three-year performance period holding period | RG-0056, RG-0057 |
| 14 | Rolls-Royce LTIP targets cumulative free cash flow £13,000m operating margin 18.7% 19.5% relative TSR FTSE 100 S&P Global industrials (ran two searches; also counted as 15) | RG-0056 |
| 16 | Rolls-Royce executive annual bonus 2025 measures underlying operating profit free cash flow weighting deferral remuneration report | RG-0058 |
| 17 | Erginbilgic 2025 total remuneration annual bonus 94% of maximum Rolls-Royce annual report single figure | RG-0055, RG-0058 |
| 18 | Rolls-Royce 2025 full year results February 2026 share buyback dividend new mid-term targets 2028 | RG-0059 |
| 19 | Rolls-Royce £7bn to £9bn buyback 2026-2028 Erginbilgic results reaction Reuters | RG-0059 |
| 20 | Rolls-Royce regains investment grade rating Moody's Baa3 S&P BBB- Fitch 2024 | RG-0061 |
| 21 | Moody's upgrades Rolls-Royce to A3 single-A rating 2026 Fitch A- net cash | RG-0060, RG-0061 |
| 22 | Rolls-Royce narrowbody engine re-entry UltraFan partner decision 2026 Erginbilgic Airbus next-generation single-aisle | RG-0065 |
| 23 | "UltraFan 30" Rolls-Royce government support single-aisle engine (ran two searches; also counted as 24) | RG-0065 |
| 25 | Rolls-Royce SMR selected Great British Energy Nuclear preferred bidder 2025 Wylfa Rolls-Royce investment in SMR | RG-0066 |
| 26 | National Wealth Fund £599 million Rolls-Royce SMR contract Wylfa three reactors signed | nothing usable (see notes) |
| 27 | Rolls-Royce board appoints Tufan Erginbilgic chief executive July 2022 announcement Anita Frew | RG-0064 |
| 28 | Rolls-Royce capital markets day November 2023 mid-term targets 2027 operating profit £2.5bn £2.8bn free cash flow investment grade | RG-0062 |
| 29 | Rolls-Royce Holdings Special Share HM Government articles of association foreign ownership limit | RG-0067 |
| 30 | Rolls-Royce UK government golden share takeover protection nuclear submarines 15% stake limit | RG-0067 |
| 31 | Rolls-Royce chair Anita Frew term extended 2024 three years reappointment letter of appointment | RG-0048 |
| 32 | Rolls-Royce 2025 annual report Wendy Mars chair Safety Energy Transition Tech Committee Jitesh Gadhia Remuneration Committee chair Nick Luff Audit | RG-0049, RG-0050 |
| 33 | Rolls-Royce non-executive directors Paul Adams Mike Manley Lee Hsien Yang step down board 2023 2024 | RG-0053 |
| 34 | Rolls-Royce 2026 notice of AGM resolutions to re-elect Birgit Behrendt Stuart Bradie George Culmer Lord Jitesh Gadhia Nick Luff | RG-0047, RG-0052, RG-0053 |
| 35 | Erginbilgic "burning platform" Rolls-Royce January 2023 staff message last chance | RG-0063 |
| 36 | Rolls-Royce half year results July 2026 raises guidance buyback net cash interim dividend | RG-0060 |
| 37 | Rolls-Royce first-half 2026 profit jumps 46% upgrades full-year profit outlook £4.7bn shares | RG-0060 |
| 38 | Rolls-Royce investment Trent XWB durability time on wing improvement programme 2025 Trent 1000 TEN upgrade cost | RG-0068 |
| 39 | Rolls-Royce Holdings major shareholders 2026 Capital Group BlackRock percentage holding TR-1 notification | RG-0070 |
| 40 | Rolls-Royce UltraFan narrowbody demonstrator UK government funding decision announced 2026 Derby partner | RG-0065 |
| 41 | new Rolls-Royce CEO tells staff "last chance" unsustainable underperforms competitors Derby town hall 2023 shares fall | RG-0063 |
| 42 | Anita Frew chair's statement Rolls-Royce annual report 2025 board transformation capital allocation long-term | RG-0048 |
| 43 | Rolls-Royce Holdings board governance document Board has delegated to the Chief Executive all its powers authorities and discretions excluding reserved matters | RG-0054 |
| 44 | Rolls-Royce directors remuneration policy LTIP awards executive directors two-year holding period post-vesting five years total | RG-0057 |
| 45 | Rolls-Royce PDMR shareholding May 2026 LTIP grant Erginbilgic performance period ending 31 December 2028 holding period | RG-0055, RG-0057 |

Notes on searches that added nothing on their own: 5 and 43 did not show the delegation clause or any value
threshold in the reserved-matters schedule; 31 did not confirm the chair's 2024 term extension; 39 found no
Capital Group or BlackRock notification; 42 found no 2025 chair's statement text.

### Earlier refused queries (first pass, 2026-10-10)

Three queries in drafting and one in verification were refused (turn search budget used up): "Rolls-Royce Holdings
plc board of directors 2026 chair Anita Frew senior independent director", "Rolls-Royce annual report 2025 board
committees Safety and Sustainability Committee Science and Technology Committee members", "Rolls-Royce Holdings
matters reserved for the board document" and "Rolls-Royce Holdings board of directors chair 2026".

## 2. Repo sources used (verbatim, machine-checked)

All 46 items pass `wargame/profiles/build/verify_quotes.py` (46/46, 2026-10-10; re-run 46/46 at verification after RG-0030's quote was extended).

| Source key | Document | Pages cited | Items |
|---|---|---|---|
| `rr_sec` | Rolls-Royce Holdings plc Form F-6 (ADR programme), signature pages, 8 July 2022 and 2 February 2021 | 75, 54 | RG-0001, RG-0002 |
| `rr_transcripts` | FH1 2011 Earnings Call (2011-07-28) | 1221 | RG-0013 |
| `rr_transcripts` | Shareholder/Analyst Call, 2014 investor day (2014-06-19) | 1028, 1035 | RG-0045, RG-0036 |
| `rr_transcripts` | Guidance/Update Call (2014-10-17) | 987 | RG-0044 |
| `rr_transcripts` | FY 2014 Earnings Call (2015-02-13) | 892 | RG-0037 |
| `rr_transcripts` | Special Call on the CEO change (2015-04-22) | 876 | RG-0012, RG-0014 |
| `rr_transcripts` | Interim Management Statement Call (2015-11-12) | 817 | RG-0038 |
| `rr_transcripts` | Shareholder/Analyst Call, strategy update (2015-11-24) | 762, 763, 782 | RG-0015, RG-0016, RG-0017, RG-0034 |
| `rr_transcripts` | Analyst/Investor Day (2016-11-16) | 678 | RG-0018 |
| `rr_transcripts` | FY 2016 Earnings Call (2017-02-14) | 669 | RG-0039 |
| `rr_transcripts` | FQ2 2017 Earnings Call (2017-08-01) | 630 | RG-0040 |
| `rr_transcripts` | 2018 AGM (2018-05-03) | 564 | RG-0003, RG-0019, RG-0020, RG-0021, RG-0046 |
| `rr_transcripts` | Special Call, governance and ESG day (2019-04-03) | 457, 461, 462 | RG-0022, RG-0023, RG-0024, RG-0025, RG-0026 |
| `rr_transcripts` | 2019 AGM (2019-05-02) | 441, 442 | RG-0027, RG-0028, RG-0029 |
| `rr_transcripts` | 2020 AGM (2020-05-07) | 367, 368, 377 | RG-0004, RG-0005, RG-0006, RG-0007, RG-0030, RG-0031, RG-0032 |
| `rr_transcripts` | Special Call, recapitalisation (2020-10-01) | 335 | RG-0033 |
| `rr_transcripts` | FY 2020 Earnings Call (2021-03-11) | 306 | RG-0008 |
| `rr_transcripts` | FH1 2021 Earnings Call (2021-08-05) | 252 | RG-0009 |
| `rr_transcripts` | FY 2021 Earnings Call (2022-02-24) | 216 | RG-0010, RG-0011 |
| `rr_transcripts` | FH1 2023 Earnings Call (2023-08-03) | 146 | RG-0035 |
| `rr_transcripts` | FH1 2024 Earnings Call (2024-08-01) | 59 | RG-0041 |
| `rr_transcripts` | FY 2024 Earnings Call (2025-02-27) | 32 | RG-0042, RG-0043 |

The extracted text is in `$WARGAME_BUILD_DIR/text/rr_transcripts.txt` and `rr_sec.txt`, with page markers. The
`rr_sec.txt` file holds the ADR deposit agreements and Form F-6 filings (2015, 2020, 2021, 2022). It has no annual
report, no governance report and no remuneration report.

`board.md` also cites existing company items (R-) and executive items (RX-) from
`wargame/profiles/rolls_royce/evidence.jsonl` and `executives/evidence.jsonl`, unchanged.
