# Supply-and-demand inputs: research notes (October 2026)

Three research passes, each checked by an adversarial verifier, for the Boeing and Airbus supply inputs in `supply_demand.json`. Web facts were confirmed through search-result text (page fetches were blocked in the container); repo citations were opened and checked. Estimates are labelled as such.

The Airbus production plan itself is the user's chart "Airbus NGSA Production Assessment, A320 Program and NGSA Transition (Rev. B)"; the demand is the user's page "Single-Aisle Replacement Demand" (Cirium, 5 and 7 Oct 2026). See `make_supply_demand.py`.

## 1. 737 MAX capacity by site

# 737 MAX production capacity by site, 2026–2030 (verified and corrected, 2026-10-13)

**Recommended base path (estimate).** 47 a month at end-2026, 52 from about mid-2027, 57 from about mid-2029, then flat at 57. At 52 a month the split is Renton 47 and Everett North Line 5.

**Method caveat.**
- Page fetches were blocked during this verification as well. The egress proxy refused CONNECT to leehamnews.com and www.boeing.com (HTTP 403). WebFetch also could not resolve airdatanews.com or centreforaviation.com.
- Every web fact below was therefore re-checked through search-result summaries only. Web confidence is one notch lower than it would be from a primary read.
- All repo citations were opened and checked line by line. They are file:line in /home/user/aero-engine-gameboard/wargame/profiles/boeing/.

## 1. Renton: number of lines and the rate they support

| Item | Value | Date | Source | Type / confidence |
|---|---|---|---|---|
| Renton final assembly lines | 3 | 2025-05-29; 2025-07-29 | Ortberg, "the 3 lines in Renton" (executives/evidence.jsonl:1292, BX-1292); evidence.jsonl:2319 (B-2319); CNBC 2023-01-30 ("still planned to run three lines at Renton") | Fact / high |
| Renton held at 47 | "Renton is stabilizing at Rate 47"; the North Line will "take on the builds needed for Rate 52 and beyond" | July 2026 | Boeing feature (https://www.boeing.com/features/2026/07/everetts-new-north-line-begins-737-production) | Fact (company) / medium-high (seen only via search summary) |
| Renton cap, trade press | "Renton's total output is capped at 47 per month"; 52 needs a working North Line | 2026 | Leeham (via search summary; exact article not identified) | Reported / medium |
| Who sets the 47 cap | The earlier report said the FAA "may" cap Renton at 47. This wording in the Leeham 2025-06-09 article (https://leehamnews.com/2025/06/09/boeings-plans-for-the-737-north-line-and-the-everett-factory-in-transition-now/) **could not be re-confirmed**: the relevant section is cut off in the search result. Leeham's May 2026 account is that Ortberg is unwilling to push Renton back to its earlier ceiling of 57 under current safety and quality processes (https://leehamnews.com/2026/05/27/ortberg-737max-at-47-mo-target-is-63-mo-in-the-future/). | 2025-06 / 2026-05 | Leeham | That the FAA formally caps Renton at 47 is **unverified**. That Boeing's policy holds Renton at 47 is supported / medium. |
| Rate per Renton line | 15.6 a month (Leeham's figure); 47 / 3 = 15.7 (computed) | 2026 | Leeham via search summary: "The North Line's capacity should be similar to that of Renton's lines: 15.6/mo. This would bring total production to 63/mo." | Analyst figure / medium |
| "This (facility) will only go to 47" (Air Data News) | – | – | https://www.airdatanews.com/boeing-struggles-to-stabilize-737-max-production-at-47-jets-per-month/ : the article and the quote could not be found by search | **Unverified; removed as evidence** |
| Current limiter at Renton | Boeing's own Renton wing shop ("all its wings in Renton for the Max line"). Not yet stable at 47. Ortberg said suppliers are in good shape. | 2026-09-16 (Morgan Stanley Laguna conference) | CAPA (https://centreforaviation.com/news/boeing-taking-longer-than-expected-to-stabilise-737-max-production-rate-ceo-1372925); Airways (https://airwaysmag.com/new-post/boeing-737-max-wing-production-rate-47-ortberg); Air Journal 2026-09-19 | Fact / high |
| Recent output signal | 41 737 MAX deliveries in August 2026 | 2026-08 | Cirium data cited by Leeham (search summary) | Reported / medium |
| Peak Renton rate actually achieved | 52 a month from Q2 2018; 57 planned for 2019 | 10-K FY2018 (filed 2019-02-08) | evidence.jsonl:1495 (B-1495); 57 plan also in evidence.jsonl:1106 (B-1106, 10-K FY2015) and :1363 (B-1363, 10-K FY2017). "On 3 lines … gearing up for 57": Aviation Week 2023 (https://m.aviationweek.com/air-transport/aircraft-propulsion/boeing-737-ramp-plan-adds-assembly-line-everett-capacity-renton) | Fact / high (the 3-line detail rests on Aviation Week, not B-1495) |
| Older capacity figures | Renton capacity 63 a month including 2 P-8s, said to be "demonstrated"; 21 a month potential per line. Stated by Beverly Wyse, then 737 VP/GM. | 2011-07-28 (Leeham); about 2012-01 (FlightGlobal; Leeham repost 2012-01-11) | https://leehamnews.com/2011/07/28/737-program-chief-talked-about-renton-production-site/ ; https://www.flightglobal.com/boeing-envisions-third-parallel-line-for-737-max/103629.article | Historical engineering figure, not current / low |

**Conclusion.** Renton's three lines have physically done 52 (2018) and were tooling for 57, so 47 is not a physical limit. Boeing's stated plan holds Renton at 47, and the current binding issue is Renton's wing shop. A formal FAA cap of 47 specific to Renton is not confirmed.

## 2. Everett "North Line" (the fourth 737 line)

| Item | Value | Date | Source | Type / confidence |
|---|---|---|---|---|
| Announced | Fourth 737 line in Everett, to start in 2H 2024. Boeing aimed for about 50 a month in the "2025/2026 timeframe". | 2023-01-30 | CNBC (https://www.cnbc.com/2023/01/30/boeing-new-737-max-production-line.html/); evidence.jsonl:2027 (B-2027), 2056, 2081 (context) | Fact / high |
| Bay | Sources conflict: the former 787 Line 1 space, or the former 747 space | – | Search summaries (CNBC 2023; Air Data News) | Not confirmed / low |
| Why Everett | No land available in Renton | July 2026 | AFP wire (e.g. thepeninsulaqatar.com, 2026-07-11) | Reported / medium |
| Delayed by the FAA | From 2024-01-24 the FAA would not approve "production rate increases or additional production lines" | 10-K FY2023 (filed 2024-01-31) | evidence.jsonl:2103 (B-2103); evidence.jsonl:2236 (B-2236) | Fact / high |
| Opened | Production began on the first airplane on Monday 2026-07-06. Official opening and ribbon cutting on Friday 2026-07-10. *(Corrected: the earlier report had about 07-14.)* | July 2026 | Boeing features (…/2026/07/everetts-new-north-line-begins-737-production; …/2026/07/teammates-mark-north-line-opening-with-renton-to-everett-relay); AFP 2026-07-11 | Fact / high |
| Investment and staff | About $1 billion. Boeing is **training** about 1,000 North Line staff, about half from Renton. *(Corrected: this is not a headcount at start.)* | July 2026 | Boeing feature title "…showing Boeing's $1 billion investment"; Fox13; Reuters-style wire coverage | Fact / medium-high |
| Start-up mode | Low-rate initial production (LRIP) under "regulatory and compliance efforts" (Boeing). The 10-Q says: "The new production line must be production-certified by the FAA prior to first delivery." | July 2026 | Boeing feature; Q2 2026 10-Q (https://www.sec.gov/Archives/edgar/data/0000012927/000162828026050038/ba-20260630.htm, via search summary) | Fact / high |
| | The LRIP period of "several months" is **not confirmed**. Conformity aircraft and the addition to PC700 come from a secondary blog (tygartmedia.com), **not** the 10-Q. PC700 is Boeing Commercial Airplanes' company-wide production certificate (Boeing South Carolina was added in 2012), not a Renton-only certificate. | | Boeing release 2012-06-27 (https://boeing.mediaroom.com/2012-06-27-FAA-Adds-Boeing-South-Carolina-Operations-to-Boeing-Commercial-Airplanes-Production-Certificate) | Secondary / low-medium |
| Certification status of the line | Not found as certified as of Oct 2026 | – | No source found | Unknown |
| Mix | The plan was to activate with 737-8s and -9s ahead of MAX 10 certification, then focus mainly on the -10 so Renton flows faster. Sources conflict on what is built now: Leeham on 2026-08-24 says the line is "currently building one Max 10 per month", and a June 2026 report said the MAX 10 would be the first jet. | 2026-01-20; 2025-05-29; 2026-08-24 | Leeham (https://leehamnews.com/2026/01/20/boeing-planning-to-activate-north-line-with-737-8s-9s-in-advance-of-max-10-certification/); executives/evidence.jsonl:1292; Leeham 2026-08-24 | Fact on intent / high; actual mix / medium |
| MAX 10 / MAX 7 certification | MAX 10 not certified on the latest reports; Bloomberg said it was expected Sept–Oct 2026. The 10-Q expects 737-7 and -10 certification in 2026 and first deliveries in 2027. One AFP timeline says the FAA certified the MAX 7 on 2026-08-03. | 2026 | American Machinist (citing Bloomberg); Q2 2026 10-Q; AFP timeline (fox26medford.com) | Reported / medium (MAX 7 date single-source) |
| Rate now | About 1 a month | As of 2026-08-24 | Leeham, Scott Hamilton (https://leehamnews.com/2026/08/24/second-737-north-line-will-be-needed-as-early-as-2028-analysis/). *(Corrected: the earlier report credited the Everett Post. No Everett Post article could be found.)* | Reported / medium |
| Target rate in 2027 | 5 a month ("target to reach five per month next year") | 2026-08-24 | Leeham, same article. *(Corrected: not "Everett Post quoting Sinclair".)* | Reported target / medium |
| Line ceiling | About 15 a month ("rate capacity of 15 jets per month"); another Leeham piece gives 15.6 | 2026-08-24 | Leeham, same article. The "Sinclair: 15, 16" quote could not be confirmed and is removed. | Analyst estimate / medium |
| Second North Line | "Needed as early as 2028" (Leeham's analysis of the MAX 10 delivery stream). Any rate above about 63 needs it. | 2026-08-24 | Leeham, same article (paywalled after the opening) | Analyst estimate / low-medium |
| Rate step that depends on it | **47 → 52.** Q2 2026 call: LRIP on the North Line "enables us to reach our next planned rate break of 52 per month". Ortberg, Bernstein conference 2026-05-27 (paraphrase): the Everett line is not needed for 47 but matters for 52 and beyond. | 2026-07-28 (Q2 results date confirmed); 2026-05-27 | Q2 2026 transcript (https://s2.q4cdn.com/661678649/files/doc_financials/2026/q2/Transcript.pdf, via search summary); board/evidence.jsonl:68 (BG-0069); Leeham 2026-05-27 | Fact / high. The verbatim "We need to have [the North Line] producing to get to rate 52" was **not found**; use the paraphrase. |

## 3. Boeing's stated rate path, with FAA approvals

| Step | Date | Source | Confidence |
|---|---|---|---|
| FAA freezes rate increases and new lines | 2024-01-24; cap of 38 stated in 10-K FY2024 (filed 2025-02-03) | evidence.jsonl:2103, 2236 | High |
| 38 a month reached | May 2025 (CFO West, FQ2 2025 call, 2025-07-29) | executives/evidence.jsonl:1872 (BX-1872) | High |
| Plan of 38 → 42 → 47 → 52 | 2025-04-23 | evidence.jsonl:2287 (B-2287) | High |
| Cadence policy: steps of 5, "no earlier than six months", and "That doesn't mean it's on six months" | July 2025 | Leeham 2025-07-30 (https://leehamnews.com/2025/07/30/ortberg-becomes-more-cautious-about-737-max-production-ramp-timing/) | Medium-high |
| **FAA approves 42** | 2025-10-17 | AP via Spectrum News 2025-10-18 (board/evidence.jsonl:68, BG-0069; board/sources.md:56, 229); American Machinist; MarketBeat URL dated 2025-10-17. The exact day is now confirmed. | High |
| **FAA capstone review cleared for 47** | 2026-05-27 (Ortberg at the Bernstein conference). Running at 47 from late May or early June. | Bloomberg Law 2026-05-27; Airline Geeks 2026-05-27; Qz 060526; board/sources.md:229 | High |
| Q2 10-Q | "During the first half of 2026, the 737 program **began to transition** from a production rate of 42 to 47 per month with the concurrence of the FAA"; "planning for additional production rate increases beyond 47 per month" | Filed 2026-07 | Q2 2026 10-Q (via search summary) | High |
| Not stable at 47 | Ortberg: "taking us a little bit longer". 52 needs stability at 47 plus FAA certification of the North Line. No new date given. | 2026-09-16 | CAPA 1372925; Airways. *(CAPA 1373245 could not be found and is removed.)* | High |
| 52 target date | "Early 2027" (Reuters, InsideFlyer, others). An end-2026 date appeared only in January 2026 reporting, an earlier plan that has since moved. The airliners.de article cited before could not be found. | 2026 | Search summaries | Medium |
| Ortberg on 52: "that's going to be more of a strain than going to 47 because of the inventory" | Late May 2026 | Qz / Bloomberg (via search summary); CAPA 1360867 headline "cautious of increasing to 52" | High |

Statements about rates above 52:

| Statement | Date | Source | Confidence |
|---|---|---|---|
| Ortberg would like to reach 63 a month "someday". No date given; he ties it to supplier readiness. | Late May 2026 (Leeham URL 2026-05-27; Bernstein conference) | Leeham 2026-05-27 | High that he said it; no schedule. "Right now 63 is our plan" was not re-confirmed. |
| "Ultimate goal" of 57 a month (Ortberg, Q2 2026) | 2026-07-28 | Manufacturing Dive (via search summary only) | Medium-low (single press source) |
| Leeham: Boeing "again aiming to raise the 737 rate to 57 per month"; Ortberg wants 63 | 2026-08-24 | Leeham 2026-08-24 | Medium |
| Boeing is studying about **70** a month: drafting plans and assessing whether suppliers could support it. Ortberg to CNBC: "a study activity right now". | 2026-06-04/05 | The Air Current via Reuters (wdez.com 2026-06-04; marketscreener) | Medium-high that a study exists; no plan |
| ~~Suppliers told to prepare for up to 75 a month~~ | – | Not confirmed as a 2026 statement. In the Leeham 2026-08-24 snippet it sits in a historical background paragraph. | **Removed**; replaced by the 70 study above |
| ~~Leeham reading (Jan 2026): sold out at 52 in 2027, 57 in 2028, possibly 63 in 2029~~ | – | Not found in any search | **Removed (unverified)** |
| Historical ladder: 42 → 47 (2017) → 52 (Q2 2018) → 57 planned for 2019, ended by the 2019 grounding | 2016–2019 | evidence.jsonl:1106, 1363, 1495 | High |

## 4. Analyst production paths in the repo (all re-checked; correct)

| Source | 2026 | 2027 | 2028 | 2029 | 2030 | File:line |
|---|---|---|---|---|---|---|
| MS production, a month | 41.5 | 48.2 | 52.0 | 52.0 | 52.0 (flat after 2028; 498, 579, 624, 624, 624 a year) | financials.md:294; analyst_models_2026.md:61 |
| GS production, a month, by quarter in 2026 | 39.7 / 41.6 / 43.6 / 44.6 | – | – | – | – | financials.md:294 |
| GS "underlying production", a month | 45.04 | 53.39 | – | – | – | financials.md:294 |
| GS delivery "Rate", a month | 45.0 | 53.4 | 57.0 | 60.9 | 64.3 | financials.md:294 |
| 737 deliveries a year, MS / GS | 500 / 522 | – | 624 / 656 | – | 624 / 740 | analyst_models_2026.md:54 |

- The 2025 baseline was 447 deliveries (analyst_models_2026.md:54) and 32.9 a month of production in MS (analyst_models_2026.md:61).
- GS does not agree with itself for 2026: 45.04 a month underlying production against a quarterly average of 42.4 (computed: 169.5 / 4).
- GS's 64.3 a month in 2030 is above Ortberg's stated 63 ambition, and below the 70 now being studied.

## Conclusion (estimates, labelled as such)

### Recommended MAX capacity path (estimate)

The path follows the observed cadence of FAA-gated steps:
- 38 reached (May 2025) to 42 approved (2025-10-17): about 5 months.
- 42 to 47 cleared (2026-05-27): about 7 months.
- Boeing's policy is "no earlier than six months" between steps.
- 47 was not stable at 2026-09-16 and no new date has been given. 52 in "early 2027" is therefore **at risk**; no source yet reports that it has slipped. The base case uses mid-2027.

| Year | Year-end nominal rate (a month) | Nominal average (a month) | Nominal, about a year | Expected actual output (estimate) |
|---|---|---|---|---|
| 2026 | 47 | about 44.9 (computed: 42 for Jan–May, 47 for Jun–Dec) | about 539 | about 42–43 a month, about 505–520 a year (47 not stable; GS quarterly average 42.4; MS 41.5; Aug-2026 deliveries 41) |
| 2027 | 52 (reached about mid-2027) | about 49.5 | about 594 | – |
| 2028 | 52 | 52 | 624 | – |
| 2029 | 57 (step about mid-2029) | about 54.5 | about 654 | – |
| 2030 | 57 | 57 | 684 | – |
| After 2030 | flat 57 (consistent with the reported "ultimate goal 57") | – | about 684 | – |

*Correction:* the earlier "about 42.5 a month, about 510 a year" for 2026 was an actual-output figure presented as a capacity average. The two are now shown separately.

- **Bounds (estimates).**
  - Low case (MS): 52 flat from 2028, which is 624 a year.
  - High case (Ortberg's aspiration, with GS as cross-check): 57 in 2028 and 63 by 2030, then flat at 63 (756 a year). GS itself shows 64.3 in 2030.
  - Upside study: about 70, which needs a second North Line.
- **Ceiling of the current 4-line set-up.** Renton held at 47 plus the North Line at about 15–16 gives about 62–63 a month (computed; Leeham gives 63). This is a planning ceiling, not a physical one: Renton has done 52 and tooled for 57 in the past. Leeham says anything above about 63, including the 70 study, needs a second North Line.
- **Binding limits.**
  - The FAA's gate on each 5-a-month step.
  - FAA production certification of the North Line before its first delivery.
  - Renton wing production (Sept 2026).
  - MAX 10 certification, which affects the North Line mix.
  - Ortberg said in Sept 2026 that suppliers are currently in good shape. Supply capacity at 63–70 is what the June 2026 study is meant to test.
- **Confidence.** Medium for 2026–2028; low-medium for 2029–2030.

### Split of a 52 rate

- **Renton 47** (3 lines at about 15.7 each, computed).
- **Everett North Line 5.**

The split rests on Boeing's July 2026 feature (Renton stabilizes at 47 and the North Line takes the builds for 52 and beyond) and Leeham 2026-08-24 (North Line at about 1 a month now, target 5 a month in 2027). Confidence: high for the structure, medium for the exact 47/5 figures.

### Implication for the game (inference)

- **Wings tie the North Line to Renton.** All MAX wings are built in Renton (Airways, Sept 2026), and about half of the North Line's trained staff came from Renton. The earlier report also claimed a "Renton PC700" link. That was wrong: PC700 is Boeing Commercial Airplanes' company-wide certificate, so certification does not tie Everett to Renton.
- **Where the base path assumes MAX production.** The base path above assumes the MAX stays in Renton through 2050.
- **If Renton is reassigned to fps.** MAX final assembly capacity falls to the Everett lines alone: about 15 a month with one North Line (Leeham) or about 30 with a second (computed estimate). MAX wing production would also have to be moved or replicated. No source shows Boeing plans this (estimate).
- **Siting fps.** Boeing put the fourth line in Everett because Renton has no spare land (AFP, July 2026). This supports modelling fps at new sites rather than expanding at Renton.
## 2. Cost of new single-aisle final assembly capacity (the Renton saving)

**Verifier's note.** I checked every repo citation by opening the file and line. I re-ran web searches for every web fact. WebFetch still cannot open pages from this container (DNS fails: ENOTFOUND), so web facts are confirmed against search-result text only. "Confirmed" below means search text matched the claim. "Not re-verified" means the search turned up nothing either way. Numbers I changed are marked **[corrected]**.

**Recommendation (estimate):** keep `renton_saving_b` at about **$3.0B** in 2025 dollars. This is already the game value (supply_demand.json **l.600** [corrected from l.598]). It is the capex Boeing avoids by putting fps in Renton instead of building a new fps site for the same rate.
- Scenario range: **$1.5B low, $3.0B central, $5.5B high**. That is about **$38M / $60M / $92M** net per unit of monthly rate [corrected from $35M / $60M / $95M: 1.5/40, 3.0/50, 5.5/60].
- The scenario range pairs low gross with low conversion cost. Taking each input's extremes gives a wider bound of about **$0.5B–$6.7B** (2.0−1.5 and 7.2−0.5) [added].

- **Scope of the saving (estimate).** Renton can take over roughly 40–60 a month of fps capacity, not the full 100. Above that, Boeing needs new capacity in either case.
- **What is not saved.** fps product tooling is needed at either site. A composite wing plant is also needed either way. Renton's 737 wing line is aluminium, and Boeing confirms 737 wing production starts in Renton (boeing.com/features/2026/06/new-737-production-line-starts-operations-in-july-ceo-says, via search).
- **Biggest caveat.** If MAX output must be kept to 2050, the MAX capacity Renton gives up has to be rebuilt elsewhere. That removes most of the saving (section 3).

No source was found that gives a cost for "new fps sites". Everything below is built from facility benchmarks, and every derived number is labelled.

**Escalation index (confirmed).** Turner Building Cost Index, annual averages:

| Year | 2009 | 2010 | 2011 | 2012 | 2013 | 2015 | 2019 | 2023 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| Index | 832 | 799 | 812 | 830 | 864 | 943 | 1156 | 1373 | 1485 |

- Sources: turnerconstruction.com/uploads/cost-index-Q4-2025.pdf (2013–2025); turnerconstruction.com/uploads/Q1-2022.pdf (2009–2012).
- KHL (khl.com/news/us-construction-costs-up-212-in-2011/70174.article) independently confirms 2010 = 799 and 2011 = 812. 2012 = 830 also agrees with 864 / 1.041.
- 2025 change: +4.1%. Q1 2026 = 1530.
- Confidence: high for 2013–2025; medium-high for 2009 and 2012.
- Factors to 2025 (computed): 2009 ×1.785, 2012 ×1.789, 2013 ×1.719, 2019 ×1.285, 2023 ×1.082.

## 1. Benchmarks

### Narrowbody final assembly lines

| Benchmark | Reported fact | Per unit of monthly rate (computed) | Confidence |
|---|---|---|---|
| Airbus Mobile, first A320 line | $600M and about 1,000 jobs, announced 2 July 2012 (joc.com; centreforaviation.com/news/...-162384). Groundbreaking 8 Apr 2013. Inaugurated 14 Sept 2015 (businessalabama.com). Plan was "up to four planes per month," upgradable to eight (mottmac.com/article/11548); Team Mobile said 40–50 a year by 2018 [corrected from "4 a month by 2017"]. Airbus announced a move from 4 to 7 a month by early 2021 (avweb.com); I found no confirmation that 7 was reached | $150M at 4 a month (2012$), about $268M in 2025$. About $153M at 7 a month and $134M at 8 a month (2025$) | Cost: high. Rate: medium |
| Airbus Mobile, second A320 line | About $150M. **Only a headline** supports this: fox10tv.com, 18 Oct 2023; the article body seen does not state it. Opened 13 Oct 2025. Adds 350,000 sq ft and about 1,000 jobs; Airbus says it "effectively doubles" Mobile's A320 capacity (airbus.com press release Oct 2025; madeinalabama.com). Mobile city and county gave $20M, partly to offset third-line costs (fox10tv.com 2023-05-16). Announcement date (May 2022) not re-verified | Estimate: about $32–40M in 2025$ if the line adds 4–5 a month; about $23M if it adds 7. This is an add-on line at an existing site | Low-medium; the cost may leave out hangars and paint shops |
| Airbus Mobile, A220 line | $300M and about 400 jobs, announced at groundbreaking (Jan 2019; assemblymag.com/articles/94754; altoday.com). Building is 270,000 sq ft, inaugurated 19 May 2020 (compositesworld.com; ainonline.com). **[added]** The Mobile County incentive deal is tied to a **$210M capital-facilities investment** and 432 hires (apr.org 2019-01-15; thomasnet.com). Target of 4 a month "by mid-decade" (Bloomberg 2020-04-15; alabamawx.com); not confirmed as reached | $75M (2019$) on $300M, about $96M in 2025$. On the $210M facilities figure: $52.5M (2019$), about $67M in 2025$ | Cost: medium-high. Rate: medium (a target) |
| Airbus Mobile, whole campus | **[corrected]** No source reports a campus total; this is my sum. Separately reported: $600M + $300M + $150M + **$82M**. The $82M is 2026 upgrades, a new distribution center due Q1 2027, and solar (fox10tv.com 2026-08-16; thebusinessview.com 2026-08-11); it is not assembly capacity. **An "$18.8M" item could not be found and is removed.** Total about $1.13B nominal. Site is about 2.5M sq ft (madeinalabama.com, Oct 2025); "nearly 200 acres" not re-verified | Estimate: about $1.70B in 2025$. That is about $122–142M per unit if total capacity is 12–14 a month (unsourced assumption). If capacity is about 14 A320 (7 doubled) plus 4 A220, about 18 a month, it is about $95M | Low-medium |
| Airbus Tianjin, first line | 8–10 bn yuan ($1.17–1.47B), a "total estimated investment" reported by China Daily on 9 March 2009 (covid-19.chinadaily.com.cn/china/2009-03/09/content_7557436.htm). **[corrected]** This was reported after the Sept 2008 launch, not a pre-opening estimate. The claim that "Airbus declined to confirm" was not found and is removed. Construction started May 2007; target 4 a month by 2011 (chinadaily.com.cn 2007-05-16). Joint venture is 51% Airbus | $290–370M nominal, about $520–660M in 2025$. Outlier; scope probably wider (joint venture, delivery centre) | Low |
| Airbus Tianjin, second line | **Cost not found.** Inaugurated 22 Oct 2025, "doubles" China A320 assembly capacity (aviationweek.com; global.chinadaily.com.cn). First delivery 16 Sept 2026, to China Eastern (airdatanews.com; year inferred). April 2023 agreement not re-verified. **"308,000 m², 13 buildings" not confirmed by search** | n/a | — |
| Airbus Toulouse (Jean-Luc Lagardère hall) lines | **Cost not disclosed.** Former A380 building. First line opened July 2023; second line 15 June 2026 (airbus.com press release 2026-06; centreforaviation.com/news/...-1363049). **[corrected]** These are A320 Family lines (mainly A321), not A321-only. The "investment cost" site-choice remark was not re-verified | n/a | — |
| Airbus Hamburg fourth line (2018) | Cost not found | n/a | — |
| Airbus line average (derived) | Ten A320 Family lines in 2026 (4 Hamburg, 2 Mobile, 2 Tianjin, 2 Toulouse) for rate 75 by end-2027 (airbus.com, June 2026) | About 7.5 a month per line | Derived, from confirmed inputs |

### Boeing facilities

| Benchmark | Reported fact | Per unit of monthly rate (computed) | Confidence |
|---|---|---|---|
| Everett 737 North Line | **$1B** "to upgrade facilities, expand workforce training and strengthen the production system." This may cover more than the line itself (boeing.com/features/2026/07/new-737-north-line-opens-showing-boeings-1-billion-investment). Fourth 737 final assembly line. **[corrected]** Opening date is **10 or 14 July 2026** (sources differ); first airframe started 6 July. Ortberg called it "a carbon copy of what you see here in Renton" (June 2026; boeing.com feature, via search). **Rate capacity 15 a month**: Leeham, 24 Aug 2026, paywalled; the snippet is confirmed. The line builds about 1 a month now, with a target of 5. Boeing: "With Renton stabilizing at Rate 47, the North Line will … reach Rate 52 and beyond" | About $67M per unit at 15 a month (2026$), in an existing building | Cost: high. Rate: medium (single paywalled source) |
| Charleston 787, first line (widebody) | $750M per AP (manufacturing.net "Boeing breaks ground on $750m S.C. plant"). "Upwards of $870M" per tradeandindustrydev.com (2009 announcement). **[corrected]** Ribbon-cutting was **10 June 2011** (knkx.org 2011-06-10, AP), not 12 Nov 2011. Building 1.2M sq ft (Boeing 2010 release). Other reports give 1.1M sq ft, or 642,720 sq ft "covered space" (militaryaerospace.com), so the floor area is uncertain. Rate 3 a month (evidence.jsonl l.263, B-0263, FQ1 2010 call). Boeing paid $592M for Vought's 787 facilities in South Carolina (l.211, B-0211, FQ3 2009 call). 2011 capex guided at $2.3B for "the 787 final assembly line in Charleston" and rate increases (l.301, B-0301). Actual capex: $1,713M in 2011 vs $1,125M in 2010 (financials.md l.65–66) | $250–290M (2009$), about $446–518M in 2025$. Upper bound for a narrowbody | Medium-high |
| Charleston 2013 expansion | More than $1B over 8 years and 2,000 jobs, about 1,000 of them in an IT centre (heraldnet.com and knkx.org, 9 April 2013) | Not a clean rate benchmark | Medium-high |
| Charleston expansion announced Dec 2024, groundbreaking Nov 2025 | More than $1B. Groundbreaking 7 Nov 2025. New final assembly building of about 1.2M sq ft, plus parts preparation, a vertical-fin paint facility and flight-line stalls. More than 1,000 jobs over 5 years (boeing.mediaroom.com 2025-11-07; scdailygazette.com). Site "slated to reach 10 a month in 2026." Completion early 2027 (Dec 2024 announcement) or 2028 (Post and Courier). Ortberg: "$1 billion here in our Charleston facility" (evidence.jsonl l.2286, B-2286, 2025-04-23) | **[corrected]** Rate increment **unknown**. The building completes after rate 10 is due, so it serves rates above 10. $333M per unit (+3, from 7 to 10) is an upper bound only | Cost: high. Rate increment: low |
| 777X Composite Wing Center | More than $1B. **[corrected]** Groundbreaking 21 Oct 2014 (boeing.mediaroom.com 2014-10-21); opened 20 May 2016 (geekwire.com/2016; compositesworld.com). That is about 19 months; **"14 months of building" removed as unsupported.** Floor area about 1M sq ft planned, about 1.3M sq ft per GeekWire and BRPH. Three autoclaves. Boeing said 777X investment peaked in 2016 (evidence.jsonl l.1225, B-1225). **[corrected]** 2016 capex was *guided* at about $2.8B "driven by the new 777X facilities … [and] Boeing South Carolina" (l.1095, B-1095). Actual 2016 capex was $2,613M (financials.md l.71) | Rate not found | High |
| 777X site request to the states (Dec 2013) | One 4.2M sq ft plant at **$7–10B** (building and equipment). Or a 3.1M sq ft fuselage and final-assembly plant at **$4–6B** plus a 1.1M sq ft wing plant at **$2–4B** (St. Louis Post-Dispatch via mynorthwest.com/local/...24685 and heraldnet.com; confirmed) | In 2025$: $6.9–10.3B for the fuselage and final-assembly plant; $3.4–6.9B for the wing plant. Whole widebody; upper bound | Medium |

### Other reference points

**Wichita and Spirit (existing programmes, not new-airplane capex)**
- Boeing: $1B over 3 years in Wichita, covering factory upgrades, training and manufacturing systems. Announced 11 May 2026 (kwch.com 2026-05-11). Confirmed; high confidence.
- Spirit: $1B over 5 years and 1,000 jobs. Press release dated 6 Dec 2017 (areadevelopment.com 12-7-2017; spiritaero.com). Confirmed; high confidence.
- Boeing closed the Spirit acquisition on 8 Dec 2025: $4.7B per Reuters, or $8.3B including debt per Boeing (board/sources.md l.224, BG-0064).

**JetZero, Greensboro (announced, not built)**
- $4.7B and about 14,500 jobs, announced 12 June 2025 (AP via ksat.com).
- Target of 20 aircraft a month at full production. GlobalAir dates that to the late 2030s.
- Derived: $235M per unit of monthly rate, including structures.
- Confidence: medium for the announcement, low as a cost outcome.

**Renton itself**
- 278 acres and about 4.1M sq ft of buildings (Boeing image-library captions). These are dated Next-Generation-era captions, and they do not say whether wing fabrication is inside the 4.1M sq ft. Confidence medium.
- About 12,000 Renton workers at the Jan 2020 production halt (Dec 2019–Jan 2020 coverage). **[corrected]** The Columbian article was not found, but the figure is confirmed in other outlets.
- Three lines today. The 2016 plan for the 737 programme, then built entirely at Renton, was 42→47→52→57 (evidence.jsonl l.1106, B-1106).
- In 2011 Boeing said 42 a month was "the limit" at its then efficiency and productivity (l.539, B-0539, Albaugh). Going above 42 at Renton would need capex (l.441, B-0441, McNerney).
- **[corrected]** The 63-a-month figure is **from Leeham, 28 July 2011**, not "Leeham (2025)". It reports the 737 programme chief saying each Renton line "can produce 21" a month and that a third line could take Renton to 63 (leehamnews.com/2011/07/28/737-program-chief-talked-about-renton-production-site/).
- The "FlightGlobal 2012, about 21 a month for a third line" citation was **not found**. The 21-a-month-per-line figure comes from the same 2011 Leeham piece.
- Separately, Leeham (24 Aug 2026) says Ortberg wants a 737 *programme* rate of 63, which the 15-a-month North Line "will get Boeing to". That implies Renton at about 48 (derived).
- Boeing's current plan: Renton "stabilizing at Rate 47" (boeing.com feature, July 2026).
- The MAX reused Renton's footprint and tooling (l.557, B-0557).

**Whole-programme cost estimates (context only)**
- **[corrected]** Calhoun put Boeing's next new airplane at about $50B on CNBC in late March 2024, after his retirement was announced. Leeham covered it on 15 April 2024 (leehamnews.com/2024/04/15/...). Confidence medium.
- Leeham (Fehrm, 21 March 2016, paywalled summary) says "about half" of programme cost goes to production tooling. A Cranfield thesis says over a third; its 2005 date was not re-verified. Confidence low-medium.
- Single-aisle programmes historically cost $10–12B (Leeham 2024). Aboulafia attributes the $10–12B estimate to CFO James Bell in 2011.
- **No public analyst estimate was found of facility capex for an NMA or a new single-aisle.** The cost of a second North Line was not found; the Leeham piece of 24 Aug 2026 is paywalled.

**Game and Boeing context**
- The game's fps 7-year solo "Nominal Tot Invest (CAPEX + NRE)" default is $60.69B (board/combined_dash.py l.921).
- Boeing guides 2026 capex at $4.0B (analyst_models_2026.md l.77). The CFO expected 2025 capex "closer to $3 billion", citing St. Louis and Charleston (evidence.jsonl l.2346, B-2346).

## 2. How the recommended figure is built (all estimates)

**What the saving covers.** Buildings, site works, paint, delivery and flight line, and the cost of starting up a workforce. fps tooling and the wing and fuselage plants are excluded, because they are needed in either case.

**Cost per unit of monthly rate at a new site (2025$, estimate):**
- **Low, $50M:** like the North Line, a spare building on an existing Boeing campus.
- **Central, $80M:** between the North Line ($67M) and Mobile A220 ($67–96M), adjusted down because Boeing lines run 15–21 a month against Airbus's 4–8.
- **High, $120M:** a greenfield site. Supported by Mobile's first line at 7–8 a month ($134–153M) and the Mobile campus ($95–142M, a low-confidence sum).

**Capacity Renton can take over (estimate):**
- Low: 40 a month. The game currently implies 42: the 52-a-month MAX rate minus Everett at 10 (supply_demand.json **l.593 and l.598** [corrected from l.590–597]; supply_demand.py **l.116–119** [corrected from l.115–118]). Boeing's current Renton plan is 47.
- Central: 50 a month. Between Renton's 47 plan, its demonstrated 52 and its 57 plan (B-1106).
- High: 60 a month. Close to the 63 theoretical ceiling (3 lines × 21; Leeham 2011). This is above any rate Renton has actually achieved or planned since 2016.

**Gross capex avoided:**
- Low: 40 × $50M = $2.0B
- Central: 50 × $80M = $4.0B
- High: 60 × $120M = $7.2B, rounded to $7.0B

**Cross-check by floor space.**
- Inputs:
  - Assume 2.5–3.5M sq ft of floor space, excluding wing fabrication, at $800–1,100 per sq ft.
  - Charleston 2009: $750M over 1.2M sq ft is $625 per sq ft, about $1,116 in 2025$. The floor area is uncertain (1.1–1.2M sq ft).
  - Charleston 2025: more than $1B over about 1.2M sq ft is about $830 per sq ft or more. **[corrected]** The direction of error is unclear, because the $1B also funds other buildings.
- Then add $0.5–1.0B for paint, delivery, the site and workforce.
- Result: $2.5–4.9B, which is consistent with the central figure.

**Cost of converting Renton (estimate, low confidence).** This covers taking out the 737 lines, re-laying the factory and updating the buildings. It is anchored on one North Line equivalent ($1B):
- Low: $0.5B
- Central: $1.0B
- High: $1.5B

**Net saving: $1.5B / $3.0B / $5.5B** (2025$). With the high case unrounded it is $5.7B. Each input's extremes give $0.5–6.7B.

**Context for a full new-site build (estimate).**
- About $4B for 50 a month (range $2.5–7B).
- About $7B for 100 a month (range $4.5–12B), assuming mild economies of scale.
- Renton avoids roughly the first half of the 100-a-month build.

## 3. Caveats for the game

1. **Keeping MAX output to 2050 erases most of the saving.**
   - If the MAX must keep its volume, Renton's roughly 42 a month of MAX capacity has to move to North-Line-type lines. At $1B per 15 a month, that costs about $2.8B (42 × $67M).
   - This is a floor: the North Line reused an existing Everett building.
   - The central net saving then falls to about $0.2B, and could be negative.
   - The game's Renton option already runs the Renton MAX lines down instead (supply_demand.py l.116–119). So $3.0B is consistent with how the game is built today.
   - Input note: the game's `everett_rate` of 10 (l.598) is an output level. Leeham puts North Line capacity at 15.
2. **Timing and dollars.**
   - **[corrected]** A final assembly line takes about **1.7–3.5 years** from announcement to opening:
     - Charleston: Oct 2009 to June 2011
     - Mobile: July 2012 to Sept 2015
     - Tianjin second line: about April 2023 to Oct 2025
     - North Line: Jan 2023 to July 2026 (ainonline.com 2023-01-30)
   - So the saving lands about 2–4 years before fps entry into service, while the game books it at entry into service (supply_demand.py **l.167–168** [corrected from l.161–162]).
   - For nominal dollars at an entry into service around 2035, escalate at about 4% a year (Turner 2025: +4.1%). That gives about $4.4B central (3.0 × 1.04^10).
   - Keep 2025$ if the game's other capex inputs are not escalated.
3. **Not found or weakly supported:**
   - No cost found for Tianjin's second line, the Toulouse lines, Hamburg's fourth line or a second North Line.
   - No analyst estimate found of facility capex for a new Boeing single-aisle.
   - The Mobile second-line $150M rests only on a headline.
   - The "$18.8M" Mobile item and the Tianjin "308,000 m², 13 buildings" figure were not found.
   - The North Line's 15-a-month capacity rests on one paywalled Leeham article.

Files referenced (line numbers re-checked):
- /home/user/aero-engine-gameboard/wargame/dashgame/supply_demand.json (l.593 `max_rate_after` 52.0; l.598 `everett_rate` 10.0; l.600 `renton_saving_b` 3.0)
- /home/user/aero-engine-gameboard/wargame/dashgame/supply_demand.py (l.116–119 Renton run-down; l.167–168 saving booked at fps EIS)
- /home/user/aero-engine-gameboard/wargame/dashgame/board/combined_dash.py (l.921)
- /home/user/aero-engine-gameboard/wargame/profiles/boeing/evidence.jsonl (lines 211, 263, 301, 441, 539, 557, 1095, 1106, 1225, 2286, 2346; all match)
- /home/user/aero-engine-gameboard/wargame/profiles/boeing/financials.md (l.65–66 capex 2010–11; l.71 capex 2016)
- /home/user/aero-engine-gameboard/wargame/profiles/boeing/analyst_models_2026.md (l.77)
- /home/user/aero-engine-gameboard/wargame/profiles/boeing/board/sources.md (l.224)
## 3. Airbus single-aisle production plan cross-check

Airbus single-aisle cross-check (as of 13 Oct 2026). Adversarially verified version.

VERDICT (unchanged after verification): an A320 family rate of 85 a month from 2026 to mid-2037 is aggressive. As a 2026–2028 number it is contradicted by every public source. As a long-run ceiling from about 2030 it is plausible only as an upside case. Airbus's only stated steady state is rate 75 ("stabilising at rate 75"). The only public figure above 75 is a "rate 83 under study" line in one paywalled Leeham analysis (19 Aug 2026). No Airbus statement puts the A320 family above 75.

HOW THIS WAS VERIFIED (limits):
- WebFetch failed on every host tried (getaddrinfo ENOTFOUND: airbus.com, airwaysmag.com, airdatanews.com). All web facts below come from search-result snippets, not full-page reads.
- The search budget for this turn ran out before these could be re-checked: the June 2024 slip, 2023/2024 deliveries, Faury's "2038", the Tianjin "12 a month" figure and the Q3 2026 results date. These rows are marked "not re-checked".
- Every repo citation was opened and checked line by line.
- Confidence: H = Airbus primary document, or several consistent reports. M = one reputable secondary report, or snippets only. L = single secondary, paywalled, unclear date, or not re-checked.

## 1. A320 family rate targets

| # | Item | Value | Date | Source | Conf. | Type |
|---|---|---|---|---|---|---|
| 1.1 | 2021 target | 64 a month by end-2023, "maybe" 75 by late 2025 | 2021-06-03 | wargame/profiles/airbus/evidence.jsonl:159 (A-0159; Bernstein analyst paraphrase), corroborated by 1.2 | H | reported |
| 1.2 | Pratt & Whitney's view | Hayes: Airbus "pretty aggressive" with "70 to 75 aircraft a month figure out in 2025"; P&W "capacitized to... rate 63". CORRECTED CITE: the AX-0042 quote is truncated and does not contain "63". The full quote is in pratt_whitney/evidence.jsonl:92 (P-0092). Also P-0091 (line 91, 2021-06-08, Mitchill: "capitalized for rate 63 thereabouts"). | 2021-07-27 | profiles/airbus/executives/evidence.jsonl:42 (AX-0042); profiles/pratt_whitney/evidence.jsonl:91-92 | H | reported |
| 1.3 | Going above 75 | CORRECTED. The Aviation Week headline "no plans to go beyond rate 75 for quite a while" (and its "about Feb 2024" date inferred from a "970 days old" tag) could NOT be found by search. Treat it as UNVERIFIED. Verified replacements: Wagner (Airbus Commercial): reach 70–75 by 2027, then hold at 75 before weighing further increases (aerointernational.de, 2026). Faury, 9 Jun 2026 (Aviation Week "Airbus' Planned Growth Inherently Challenging", via Hosteltur): Airbus must absorb this growth before further production jumps. | 2026 | aerointernational.de/?p=316131; aviationweek.com/air-transport/aircraft-propulsion/airbus-planned-growth-inherently-challenging-ceo-says; hosteltur.com/176845_... | M (snippet) | reported |
| 1.4 | Rate 75 moved from 2026 to 2027 (engines, aerostructures, cabins) | 75 in 2027 | Jun 2024 | airdatanews.com/airbus-adjusts-commercial-aircraft-delivery-target-downwards; leehamnews.com/2024/12/12/... NOT re-checked in this pass (search budget). Indirect support: the Airbus release of 27 Dec 2023 still said "75 in 2026", and the Airbus story of Oct 2025 says "75 in 2027". | M | reported |
| 1.5 | Board Report plan | "75 single-aisle aircraft per month by 2027" | Board Report FY2025, p.152 | profiles/airbus/evidence.jsonl:431 (A-0431); financials.md:109 | H | reported |
| 1.6 | Current guidance | "between 70 and 75 aircraft a month by the end of 2027, stabilising at rate 75". Cause: "Pratt & Whitney's failure to commit to the number of engines ordered by Airbus". The repo OCR cuts the name off; the FY2025 release coverage names Pratt & Whitney. | Results 2026-02-19 (Board Report filed 2026-02-18); repeated at Q1 (Apr 2026) and H1 (late Jul 2026) | evidence.jsonl:218 (A-0218); financials.md:108; globalair.com/articles/airbus-reports-2025-financial-results-a320-production-target-revised/11971; airdatanews (870 / engines); aircargoweek H1 | H | reported |
| 1.7 | Q1 2026 release | Pratt & Whitney is "the key pacer" of the A320 ramp, affecting 2026 and 2027 | Apr 2026 (exact day not re-checked) | Airbus Q1 2026 release PDF (mediaassets.airbus.com/pm_38_900_900051-7tq155l0vm.pdf), confirmed via snippet | H | reported |
| 1.8 | Berlin, 9 Jun 2026 | Faury: Airbus may miss 75 by end-2027; P&W has not given certainty on its 2027 schedule | 2026-06-09 | airinsight.com/airbus-could-miss-rate-75-target-in-late-2027/ (citing Aero.de). Single outlet in the results. | M | reported |
| 1.9 | H1 2026 | P&W's agreed volumes shape the 2026–27 ramp; Airbus has no buffer of P&W engines; talks on "foreseeable" volumes continue. The report's specific wording ("support the 2026 guidance and the previously announced mid-term targets") was not confirmed verbatim. | late Jul 2026 | aircargoweek.com/airbus-reports-half-year-2026-results/; airwaysmag.com/new-post/airbus-h1-2026-results-delivery-target; flightglobal.com/.../165925.article (headline) | M | reported |
| 1.10 | Rates above 75 | "Rate 83 has been under study for some time"; 75 needed "sooner rather than later, and potentially even higher". CORRECTED: the article says the rate "is already sold out through 2032". The visible text does not say "at the current rate"; it links overselling to not raising production by end-2027. | 2026-08-19 | leehamnews.com/2026/08/19/airbus-pushing-to-increase-monthly-a320neo-production-rate-sooner-than-later/ (paywalled; opening only) | L–M | analyst report, not an Airbus statement |
| 1.11 | Rate 85 or 100 for the A320 family | None found | — | searches | — | not found |
| 1.12 | Bank models (repo) | MS: 65 in 2027E, 70 in every quarter 1Q28–4Q30; never reaches 75. GS: 65 in 2027E, 75 from 2029. | 2026 analyst files | profiles/airbus/analyst_models_2026.md:83-90 (cite corrected from 84-90) | H (as a file record) | analyst estimate |

**Actual output**

| Item | Value | Source | Conf. |
|---|---|---|---|
| A320 family deliveries, 2025 | 607 (50.6 a month delivered). The banks put the 2025 production rate at 52.8. | financials.md:112 (A-0247); analyst_models_2026.md:74, :85 | H |
| A320 family deliveries, 2023 / 2024 | 571 / 602 | Airbus annual delivery releases. NOT re-checked in this pass; the report's cited 2025 release does not carry the 2023 figure. | M |
| H1 2026 | 351 total (A220 44, A320 family 271, A330 10, A350 26). A320 family is about 45 a month. | Airbus H1 2026 release via aircargoweek and afm.aero snippets. The 351 total is also at analyst_models_2026.md:69. CORRECTED: 271 is not in the repo file. | H |
| September 2026 | 72 total, 59 A320 family (37 A321neo, 21 A320neo, 1 A319neo); 547 in nine months (+7.9%); 323 needed in Q4 for 870, about 108 a month against a nine-month average of about 61 (all types). Outlets disagree on September A220s (6 vs 8). Aviation Week frames the target as "850–870" and says "at least 313" are needed. | airdatanews.com/airbus-delivers-72-jets-in-september-...; aerotime.aero; aviationweek.com/awin-knowledge-center/data-airbus-revs-deliveries-september-new-orders-tumble | H for 72/547; M for detail |
| 2026 guidance | "around 870" | Airbus FY2025, Q1 and H1 releases (multiple reports) | H |
| Meaning of "around" | ±20 (implied 850–890) per Faury on the H1 call | airwaysmag.com (single source) | M (CORRECTED from H) |
| Production run-rate | REMOVED: "analysts estimate about 60 a month" had no named source. The only computed figure is the nine-month delivery average of 547 / 9 ≈ 61 a month, all types, not A320 production. | — | — |
| Rate reporting | Airbus no longer publishes monthly or quarterly A320 production rates | airinsight.com/airbus-no-longer-sharing-quarterly-production-rates/ (search notes AirInsight page dates are unreliable) | L |

## 2. Final assembly line (FAL) footprint

| Item | Value | Date | Source | Conf. |
|---|---|---|---|---|
| Airbus plan | 10 A320 family lines in 2026: Hamburg 4, Toulouse 2 (Lagardère), Mobile 2, Tianjin 2. Faury ties the network to the ramp to 75. | 2026-06-15 | airbus.com/en/newsroom/press-releases/2026-06-airbus-inaugurates-new-a320-family-final-assembly-line-in-toulouse; CAPA; CompositesWorld; air-journal.fr/?p=275743 | H |
| Toulouse Lagardère line 1 | Opened 9 Jul 2023 (former A380 hall); first delivery 27 Dec 2023, an A321neo to Pegasus | 2023 | Airbus release 2023-12 (airbus.com/en/newsroom/press-releases/2023-12-airbus-delivers-first-aircraft-from-new-toulouse-final-assembly); journal-aviation.com 2023-07-10 | H |
| Toulouse Lagardère line 2 | Inaugurated 15 Jun 2026; first aircraft rolls out later in 2026; site staffing to reach nearly 1,500 | 2026-06-15/17 | Airbus release; flightglobal.com/archive/2026/06/airbus-to-end-st-martin-a320neo-assembly-as-second-lagardere-line-opens/ | H |
| Toulouse St Martin support lines | Airbus "has not said when" the St Martin lines will close. Once the two Lagardère lines reach optimum capacity and St Martin closes, the 10-line network above remains. (Wording corrected from "has yet to decide".) | 2026-06-17 | FlightGlobal (above), via snippet | M |
| Toulouse delivery centre (NEW) | New 35,000 m² A320 delivery centre at Lagardère with 16 aircraft positions, to support higher output. NOTE: the report's Airbus URL "2026-09-...new-delivery-centre-0-1" is this release, NOT a Tianjin release. | 2026-09 | avitrader.com/2026/09/17/airbus-opens-toulouse-delivery-centre-to-support-increase-of-a320-output/; abcbourse | M |
| "M91" | No public reference found. The user chart's "Toulouse M91 closure end-2029" is not publicly confirmed. If M91 is a St Martin building, the only public position is that no closure date is set. | — | searches | not found |
| Mobile line 2 | Inaugurated 13 Oct 2025; adds 350,000 sq ft; "effectively doubles" Mobile A320 capacity; tied to 75 in 2027. No site rate found. | 2025-10-13 | Airbus release PDF (airbus.com/.../2025-10/press_release_airbus_inaugurates_second_a320_assembly_line_in_the_us.docx.pdf); fox10tv; evidence.jsonl:263 (A-0263) | H |
| Tianjin line 2 | Inaugurated Oct 2025 (China Daily, 22 Oct 2025). Full operation was targeted for early 2026, but the first delivery came 16 Sep 2026 (A320neo to China Eastern, B-32SW), later than that target. CORRECTED SOURCE: airdatanews / China Daily HK 2026-09-16 / Aviation Week, not the Airbus URL the report gave. | 2025-10 to 2026-09 | airdatanews.com/airbus-delivers-first-a320neo-from-second-chinese-assembly-line/; chinadailyhk.com/article/639657; chinadaily.com.cn/a/202510/22/WS68f866bfa310f735438b6514.html | H (dates); M (detail) |
| Tianjin capacity | "eventually 12 a month" (ajot, 2023); about 20% of global output (Xinhua) | — | NOT re-checked in this pass | L |
| Hamburg | 4 lines | 2026 | Airbus release 2026-06-15 | H |

**My estimate of line capacity (estimate):**
- 75 a month over 10 lines is about 7.5 a month per line.
- 85 a month needs about 8.5 a month per line, or about 11.3 lines at 7.5.
- That means keeping the St Martin support lines that Airbus says will close (date not set), or adding a line. No such plan has been announced.

## 3. Successor aircraft (NGSA): entry into service, ramp, overlap with the A320

| Item | Value | Date | Source | Conf. | Type |
|---|---|---|---|---|---|
| Entry into service | "around 2037" | Board Report FY2025 p.135 (issued 2026-02-18) | evidence.jsonl:409 (A-0409) | H | reported |
| Entry into service | "second half of the next decade" | Board Report p.10 | evidence.jsonl:224 (A-0224) | H | reported |
| Generation transition | Mid-term horizon "around 2035" is "the transition period between the current and next generation" | Board Report p.152 | evidence.jsonl:431 (A-0431) | H | reported |
| Earlier launch window | CORRECTED. The Aviation Week Paris 2025 ShowNews article and the "maybe between 2035 and 2040" quote were NOT found. What was found: an earlier Faury interview (Gulf News, about Feb 2024) put launch in 2027–28 after propulsion selection around 2025–26. At Paris 2025, Airbus's head of future programmes said "By the end of this decade, we want to be launch-ready". | 2024–2025 | gulfnews.com (airbus-wants-to-replace-its-bestselling-a320-family-by-the-mid-2030s); AFP/Reuters 2025 coverage | L–M | reported |
| Launch date (internal name: eAction) | Launch in 2030; entry into service in the second half of the 2030s. CORRECTED: no source found for "possibly outside Toulouse and Hamburg". Coverage says engine and production choices are "still open"; no site is named. "Very committed" appears only in the Simple Flying URL slug. | 2026-06 | aviationweek.com/air-transport/aircraft-propulsion/interview-why-airbus-ceo-bullish-launching-a320-replacement-2030 (paywalled); airlinegeeks.com/2026/06/27/...; aviationnews.eu 2026/06; airdatanews.com/airbus-keeps-2030-target-for-a320-successor-after-hydrogen-rethink/; simpleflying.com/... | M | reported |
| Farnborough 2026 | 2030 launch target maintained. 21 Jul 2026: Airbus announced a three-year Wing of Tomorrow flight-test campaign with wing extensions on an A321neo. The start of test flights is disputed: AFP says "this year", AirInsight says H2 2027. CORRECTED SOURCE: the TechXplore URL could not be found; use the Airbus release and the AFP syndication. | 2026-07-21 | airbus.com/en/newsroom/press-releases/2026-07-airbus-launches-new-flight-test-programme-for-wing-of-tomorrow; deeside.com (21 Jul 2026); omanobserver.om/article/1193398 (AFP); leehamnews.com/2026/07/22/... | H (announcement); M (start date) | reported |
| Faury's own date | Faury has cited 2038; some inside Airbus see the technology arriving in the 2040s | unclear | Leeham via search. NOT re-checked in this pass. | L | reported |
| Production ramp | Airbus is preparing NGSA for about 100 a month | 2026 (exact date unknown) | airdatanews.com/airbus-targets-100-aircraft-per-month-for-a320-successor/ (confirmed via snippet; its Aviation Week attribution not confirmed); hosteltur | L–M | reported, not an Airbus release |
| Production as a design gate | Composite wing must be producible "at the same high industrial rates as current metallic wings"; the production system is matured alongside the aircraft | Board Report p.11, p.157 | evidence.jsonl:225, :441 (A-0225, A-0441) | H | reported |
| A320 production alongside NGSA | Overlap is implied by the "transition period" wording. No public end date for A320 production. "Backlog over 100 months at rate 75" comes from a single unverified secondary report. | various | A-0431; secondary report | H (transition wording); L ("100 months") | reported |
| A320neo family backlog (NEW, repo-derived) | 11,529 firm orders minus 4,372 delivered = about 7,157 at end-2025. That is about 95 months at rate 75 and about 84 months at 85 (my arithmetic; excludes 2026 orders). The Airbus story of Oct 2025 says "over 7,000". | end-2025 | evidence.jsonl:246 (A-0246); financials.md:111; airbus.com/en/newsroom/stories/2025-10-ramping-up-a320-family-production | H (inputs); estimate (months) | reported + estimate |
| Total backlog | 8,754 at end-2025; over 9,000 at Q1 2026; 9,222 at H1 2026 | 2026 | FY2025 release coverage; afm.aero; aircargoweek H1 | H / M / H | reported |

## 4. Slips in the rate 75 date

The target has moved four times, and engines were cited each time from 2024:
- late 2025 (2021 plan; A-0159, P-0092)
- 2026 (Airbus release of 27 Dec 2023)
- 2027 (June 2024; not re-checked)
- "70–75 by end-2027, stabilising at 75" (Feb 2026; A-0218)

That is about a 2–3 year slip in five years.

The repo already records this: wargame/profiles/airbus/profile.md:174 and :368, and wargame/profiles/overview/overview_data.json:1742 (path corrected).

Open risk, as of October 2026:
- 2027 engine volumes with P&W are still not committed (1.8, 1.9).
- Faury said on 9 Jun 2026 that Airbus may miss 75.
- The Q3 2026 results date of 2026-10-28 was NOT re-checked. Nothing from Q3 is included here.

## 5. Is 85 a month from 2026 to mid-2037 aggressive or plausible?

**The user's chart, as stored in the game:** wargame/dashgame/supply_demand.json, airbus.a320_base (verified):
- 64 a month to 2025.61, ramping linearly to 85 at 2025.82.
- Held at 85 to 2037.3, then 72 at 2037.5.
- chart_eis = 2037.45; a320_rate_no_ngsa = 85.

**Evidence that it is aggressive:**
1. **2026–2027 is off by about a third to a half.**
   - 85 a month is 1,020 a year.
   - Actuals: H1 2026 about 45 a month; September 59.
   - Estimate: 2026 A320 total about 665 (607/793 = 76.5% of 870). That is 65% of the plan.
   - Airbus's own end-2027 exit rate is 70–75; both banks model 65 for 2027 (analyst_models_2026.md:85).
2. **85 is above every public ceiling.**
   - Airbus's stated steady state is 75. 85 is 13% above it (85/75).
   - The only figure above 75 is Leeham's "rate 83 under study".
   - MS never reaches 75 through 2030; GS reaches it in 2029.
3. **The line network is sized for 75.** The 10-line network is presented as Airbus's plan for the ramp to 75 (2026-06-15 release). 85 implies about 8.5 a month per line or 1–2 more lines.
4. **Engines are the binding limit through 2027.**
   - P&W is the "key pacer" (Q1 2026 release). Engine commitment is the cause given in A-0218.
   - Inference, not a repo instruction: given a recorded slip of about 2 years (profile.md:174, :368), Airbus rate dates deserve a similar haircut.

**Evidence that parts of it are plausible:**
- **Demand:** Leeham says the planned rate is sold out through 2032, and Airbus should go to 75 sooner "and potentially even higher". The A320neo backlog of about 7,157 at end-2025 is about 8 years at rate 75 (estimate).
- **NGSA ramp:** Airbus is reportedly preparing NGSA for about 100 a month (L–M), which implies it expects single-aisle demand above 75 in the late 2030s.
- **NGSA entry into service** at mid-2037 (2037.45) matches "around 2037". A 2030 launch plus about 7 years of development fits (inference).
- **NGSA ramp to 100 by 2Q45** matches the reported design rate. The ramp speed (50 by 3Q41, about 4 years after entry into service) is my judgement only: fast for a clean sheet on a new production system.

**Cumulative A320 output, 2026.0 to mid-2037 (all estimates; arithmetic re-checked):**

| Path | Build | Total |
|---|---|---|
| User plan | 85 × 12 × 11.3 years, plus the 2037.3–2037.5 ramp from 85 to 72 (about 190) | about 11,700 |
| Public targets | 665 (2026) + 780 (2027, 65 a month) + 75 × 12 × 9.5 years | about 10,000 |
| MS-style | 665 + 780 + 70 × 12 × 3 + 75 × 12 × 6.5 | about 9,800 |
| Upside | 665 + 780 + 75 × 12 × 2 + 83 × 12 × 7.5 | about 10,700 |

The user plan is about 1,700 aircraft (about 17%) above the public-target path and about 1,000 above the upside case.

**Recommendation for the game (inference):**
- Treat 85 as a demand-side or "unconstrained" Airbus plan, not as supply.
- Base supply case: about 55 a month average in 2026, about 65 in 2027 (exit 70–75), 75 from 2028.
- Upside: 83–85 from about 2030, only if engines allow and Airbus keeps St Martin or adds a line.
- Downside: the MS path, 70 a month through 2030.
- The user's base transition dips sharply after mid-2037. At 2040.5 the A320 is at 14 and NGSA at about 25 (interpolated between 24 at 2040.45 and 31 at 2040.8), so the total is about 39–40 a month. The alt plan is at 42 + 25, about 67.

"Toulouse M91 closure end-2029" could not be found in any public source.

**Repo files used (all re-opened):**
- /home/user/aero-engine-gameboard/wargame/profiles/airbus/evidence.jsonl (lines 159, 182, 185, 215, 218, 224, 225, 240, 246, 247, 263, 383, 409, 419, 431, 441)
- /home/user/aero-engine-gameboard/wargame/profiles/airbus/executives/evidence.jsonl (lines 42, 54)
- /home/user/aero-engine-gameboard/wargame/profiles/pratt_whitney/evidence.jsonl (lines 91, 92)
- /home/user/aero-engine-gameboard/wargame/profiles/airbus/analyst_models_2026.md (lines 69, 74, 83-90, 108, 129)
- /home/user/aero-engine-gameboard/wargame/profiles/airbus/financials.md (lines 108-112)
- /home/user/aero-engine-gameboard/wargame/profiles/airbus/profile.md (lines 77, 162, 174, 179, 221, 368)
- /home/user/aero-engine-gameboard/wargame/profiles/overview/overview_data.json (line 1742)
- /home/user/aero-engine-gameboard/wargame/dashgame/supply_demand.json (airbus.a320_base, a320_alt, ngsa, chart_eis, a320_rate_no_ngsa, milestones)

Sources (search-snippet confirmed unless marked):
- [Airbus Toulouse second FAL release](https://www.airbus.com/en/newsroom/press-releases/2026-06-airbus-inaugurates-new-a320-family-final-assembly-line-in-toulouse)
- [FlightGlobal: St Martin assembly to end](https://www.flightglobal.com/archive/2026/06/airbus-to-end-st-martin-a320neo-assembly-as-second-lagardere-line-opens/)
- [Air Journal: 10-line plan](https://www.air-journal.fr/?p=275743)
- [Airbus: first delivery from new Toulouse FAL, Dec 2023](https://airbus.com/en/newsroom/press-releases/2023-12-airbus-delivers-first-aircraft-from-new-toulouse-final-assembly)
- [Airbus Mobile second FAL release (PDF)](https://www.airbus.com/sites/g/files/jlcbta136/files/2025-10/press_release_airbus_inaugurates_second_a320_assembly_line_in_the_us.docx.pdf)
- [Fox10: Mobile line 2, 13 Oct 2025](https://www.fox10tv.com/2025/10/13/airbus-inaugurates-second-a320-final-assembly-line-mobile/)
- [China Daily: second Tianjin FAL](https://global.chinadaily.com.cn/a/202510/22/WS68f866bfa310f735438b6514.html)
- [Air Data News: first A320neo from second Tianjin line](https://www.airdatanews.com/airbus-delivers-first-a320neo-from-second-chinese-assembly-line/)
- [China Daily HK, 16 Sep 2026](https://www.chinadailyhk.com/article/639657)
- [AviTrader: Toulouse delivery centre](https://avitrader.com/2026/09/17/airbus-opens-toulouse-delivery-centre-to-support-increase-of-a320-output/)
- [Air Cargo Week: Airbus H1 2026](https://aircargoweek.com/airbus-reports-half-year-2026-results/)
- [Airways: H1 2026 and ±20](https://airwaysmag.com/new-post/airbus-h1-2026-results-delivery-target)
- [afm.aero: Q1 2026, backlog over 9,000](https://afm.aero/airbus-reports-114-q1-2026-deliveries-while-order-backlog-surpasses-9000-aircraft)
- [GlobalAir: FY2025, A320 target revised](https://www.globalair.com/articles/airbus-reports-2025-financial-results-a320-production-target-revised/11971)
- [Air Data News: 870 and engines](https://www.airdatanews.com/airbus-targets-around-870-deliveries-in-2026-as-engine-issues-slow-a320neo-ramp-up)
- [Air Data News: September 2026](https://www.airdatanews.com/airbus-delivers-72-jets-in-september-as-order-backlog-falls-by-58-aircraft/)
- [Aviation Week: September 2026 deliveries](https://aviationweek.com/awin-knowledge-center/data-airbus-revs-deliveries-september-new-orders-tumble)
- [AeroTime: September 2026](https://www.aerotime.aero/articles/airbus-aircraft-deliveries-september-2026/amp)
- [AirInsight: could miss rate 75 in late 2027](https://airinsight.com/airbus-could-miss-rate-75-target-in-late-2027/)
- [AirInsight: no longer sharing production rates](https://airinsight.com/airbus-no-longer-sharing-quarterly-production-rates/)
- [FlightGlobal: still in talks with P&W](https://www.flightglobal.com/aerospace/airbus-still-in-talks-with-pandw-over-foreseeable-a320neo-engine-supply-volumes/165925.article)
- [Leeham, 19 Aug 2026: pushing A320neo rate (paywalled)](https://leehamnews.com/2026/08/19/airbus-pushing-to-increase-monthly-a320neo-production-rate-sooner-than-later/)
- [Aero International: Wagner, hold at 75](https://www.aerointernational.de/?p=316131)
- [Aviation Week: planned growth inherently challenging](https://aviationweek.com/air-transport/aircraft-propulsion/airbus-planned-growth-inherently-challenging-ceo-says)
- [Hosteltur: 100 aircraft a month](https://www.hosteltur.com/176845_airbus-quiere-llegar-a-los-100-aviones-fabricados-al-mes-sera-en-esta-decada.html)
- [Air Data News: 100 a month for A320 successor](https://www.airdatanews.com/airbus-targets-100-aircraft-per-month-for-a320-successor/)
- [Aviation Week interview: 2030 launch (paywalled)](https://www.aviationweek.com/air-transport/aircraft-propulsion/interview-why-airbus-ceo-bullish-launching-a320-replacement-2030)
- [AirlineGeeks: 2030 launch](https://airlinegeeks.com/2026/06/27/report-airbus-to-launch-a320-replacement-program-in-2030/)
- [Aviation News EU: 2030 launch confirmed](https://aviationnews.eu/news/2026/06/airbus-confirms-2030-launch-for-a320-successor-capitalizing-on-boeings-program-delays/)
- [Air Data News: 2030 target after hydrogen rethink](https://www.airdatanews.com/airbus-keeps-2030-target-for-a320-successor-after-hydrogen-rethink/)
- [Airbus: Wing of Tomorrow flight-test programme](https://www.airbus.com/en/newsroom/press-releases/2026-07-airbus-launches-new-flight-test-programme-for-wing-of-tomorrow)
- [Oman Observer (AFP): Farnborough 2026](https://www.omanobserver.om/article/1193398/business/airbus-boeing-fly-in-different-directions-at-farnborough)
- [Gulf News: replace A320 by mid-2030s](https://gulfnews.com/amp/story/business%2Faviation%2Fairbus-wants-to-replace-its-bestselling-a320-family-by-the-mid-2030s-1.1708002524896)
- [Airbus story, Oct 2025: ramping up A320 production](https://www.airbus.com/en/newsroom/stories/2025-10-ramping-up-a320-family-production)

Not re-checked in this pass (search budget exhausted, WebFetch unavailable):
- [Air Data News: 2024 target cut](https://airdatanews.com/airbus-adjusts-commercial-aircraft-delivery-target-downwards)
- [Leeham, Dec 2024: procurement head](https://leehamnews.com/2024/12/12/airbus-procurement-head-convinced-supply-chain-issues-are-on-right-path/)
- [CNBC: FY2025 results](https://www.cnbc.com/2026/02/19/airbus-earnings-fy-q4-boeing-deliveries-a320-airbus-2026-boeing-recovery.html)
- [Simple Flying: "very committed"](https://simpleflying.com/airbus-very-committed-launching-a320-family-replacement-2030-ceo/)
- [Leeham, 28 Jul 2026](https://leehamnews.com/2026/07/28/airbus-walks-line-between-shareholder-returns-and-clean-sheet-ambitions/)
- [Leeham, 29 Jul 2026](https://leehamnews.com/2026/07/29/airbus-full-year-guidance-back-on-track-after-record-aircraft-delivery-pace-in-q2/)

Not found (treat as unverified):
- aviationweek.com/aerospace/manufacturing-supply-chain/airbus-no-plans-go-beyond-a320neos-rate-75-quite-while
- aviationweek.com/shownews/paris-air-show/airbus-ceo-guillaume-faury-reveals-plans-new-generation-narrowbody
- techxplore.com/news/2026-07-airbus-future-aisle-jet-hydrogen.html