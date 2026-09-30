# Boeing: key financial tables for decisions

These tables are copied from the script-built files, not retyped:
- `evidence/fin_boeing.md` (cited [FIN: §]; sources are Capital IQ, the Goldman Sachs model of 28 Jan 2026 and the Morgan Stanley model);
- the per-10-K tables `evidence/tk1-4.financials.md` (cited [tkN: FYxxxx]).

Amounts are US$ millions unless marked otherwise. A dash (–) means the source has no value. This file adds no new numbers. The behavioural reading of these tables is in `profile.md` §2.

## Decision summary: which table answers which war-game question

| Question you face | Look at | What the table says for the decision |
|---|---|---|
| Can Boeing fund fps now, and when? | §8a (FCF, net debt, forecasts) | FCF is thin in 2026E and strong from 2027E-28E on both banks' paths. Net debt falls toward the pre-crisis level only by 2028E (MS). This supports no fps order in Turn 1 and a launch in Turn 2 |
| How big a development load is "normal"? | §3 (R&D intensity) | The 787 era is the practical ceiling, and the MAX era is the "flat R&D" norm. A Solo fps overlapping a 787 Re-engine would exceed the norm |
| Will cash go to shareholders instead? | §4 (returns vs FCF) | No common returns since 2020. Only GS models buybacks, from 2027E. Deferring them is the historical funding source for programs |
| How fragile is the balance sheet? | §6 (debt build-up), §5 (negative FCF years) | Debt is still far above its FY2004-FY2018 range, and interest expense is several times the 2018 level. Five of the six negative-FCF years since FY1997 fall in FY2019-FY2025 |
| How long do charges and margin damage last? | §7 (BCA margin swings), §9c (charges) | BCA margin has not recovered its FY2018 peak. Charges recur on the same program for years (747, KC-46A, 777X) |
| What do the analysts assume about rates and programs? | §8c, §8d | Both models ramp the 737 and 787. GS puts the first 777X deliveries in 2027E; MS has no 777X line. Neither contains a new airplane |

## 1. P&L and R&D intensity, FY2004-FY2025 [FIN: 1a]

Op income is CapIQ "Operating Income", which excludes unusual items. GAAP EBIT is GS "Earnings from operations". Use GAAP EBIT for what Boeing reported.

**Decision use.** R&D % of revenue peaked in 2009 (787 development). DPS was never cut from 2004 until the 2020 suspension, was raised even in the 2019 grounding year, and is NA from 2021.

| FY | Revenue | Op income (CapIQ) | Op margin | GAAP EBIT (GS) | R&D | R&D % rev | Net income | DPS $ |
|---|---|---|---|---|---|---|---|---|
| 2004 | 51,400 | 1,896 | 3.7% | 2,007 | 1,879 | 3.7% | 1,872 | 0.85 |
| 2005 | 53,621 | 2,204 | 4.1% | 2,812 | 2,205 | 4.1% | 2,572 | 1.05 |
| 2006 | 61,530 | 3,665 | 6.0% | 3,585 | 3,257 | 5.3% | 2,215 | 1.25 |
| 2007 | 66,387 | 5,604 | 8.4% | 5,830 | 3,850 | 5.8% | 4,074 | 1.45 |
| 2008 | 60,909 | 3,705 | 6.1% | 3,950 | 3,768 | 6.2% | 2,672 | 1.62 |
| 2009 | 68,281 | 1,871 | 2.7% | 2,096 | 6,506 | 9.5% | 1,312 | 1.68 |
| 2010 | 64,306 | 4,698 | 7.3% | 4,971 | 4,121 | 6.4% | 3,307 | 1.68 |
| 2011 | 68,735 | 5,521 | 8.0% | 5,844 | 3,918 | 5.7% | 4,018 | 1.68 |
| 2012 | 81,698 | 6,018 | 7.4% | 6,310 | 3,298 | 4.0% | 3,900 | 1.76 |
| 2013 | 86,623 | 6,328 | 7.3% | 6,562 | 3,071 | 3.5% | 4,585 | 1.94 |
| 2014 | 90,762 | 7,196 | 7.9% | 7,473 | 3,047 | 3.4% | 5,446 | 2.92 |
| 2015 | 96,114 | 7,170 | 7.5% | 7,443 | 3,331 | 3.5% | 5,176 | 3.64 |
| 2016 | 93,496 | 6,988 | 7.5% | 5,834 | 3,391 | 3.6% | 5,034 | 4.36 |
| 2017 | 94,005 | 10,113 | 10.8% | 10,344 | 3,179 | 3.4% | 8,458 | 5.68 |
| 2018 | 101,127 | 11,843 | 11.7% | 11,987 | 3,269 | 3.2% | 10,460 | 6.84 |
| 2019 | 76,559 | -2,102 | -2.7% | -1,975 | 3,219 | 4.2% | -636 | 8.22 |
| 2020 | 58,158 | -8,485 | -14.6% | -12,767 | 2,476 | 4.3% | -11,873 | 2.06 |
| 2021 | 62,286 | -473 | -0.8% | -2,902 | 2,249 | 3.6% | -4,202 | NA |
| 2022 | 66,608 | -817 | -1.2% | -3,547 | 2,852 | 4.3% | -4,935 | NA |
| 2023 | 77,794 | 780 | 1.0% | -773 | 3,377 | 4.3% | -2,222 | NA |
| 2024 | 66,517 | -10,019 | -15.1% | -10,707 | 3,812 | 5.7% | -11,817 | NA |
| 2025 | 89,463 | -5,191 | -5.8% | 4,281 | 3,615 | 4.0% | 2,235 | NA |

## 2. Commercial Airplanes (BCA) and total capex, FY2004-FY2025 [FIN: 1b]

The segment label includes Boeing Capital from FY2021. The FY2025 row is from GS `SEG`, not CapIQ.

**Decision use.** Capex was protected in the 2024 crisis and rose in 2025. Boeing does not cut investment in future products to save cash in the current era.

| FY | BCA revenue | BCA op profit | BCA margin | Total capex | Segment basis | CapIQ flag |
|---|---|---|---|---|---|---|
| 2004 | 19,925 | 745 | 3.7% | 1,246 |  | Reclassified |
| 2005 | 21,365 | 1,431 | 6.7% | 1,547 |  | Reclassified |
| 2006 | 28,465 | 2,733 | 9.6% | 1,681 |  |  |
| 2007 | 33,386 | 3,584 | 10.7% | 1,731 |  |  |
| 2008 | 28,263 | 1,186 | 4.2% | 1,674 |  |  |
| 2009 | 34,051 | -583 | -1.7% | 1,186 |  |  |
| 2010 | 31,834 | 3,006 | 9.4% | 1,125 |  | Restated |
| 2011 | 36,171 | 3,495 | 9.7% | 1,713 |  | Reclassified |
| 2012 | 49,127 | 4,711 | 9.6% | 1,703 |  | Reclassified |
| 2013 | 52,981 | 5,795 | 10.9% | 2,098 |  |  |
| 2014 | 59,990 | 6,411 | 10.7% | 2,236 |  |  |
| 2015 | 59,399 | 4,284 | 7.2% | 2,450 |  |  |
| 2016 | 59,378 | 1,981 | 3.3% | 2,613 |  | Restated |
| 2017 | 54,612 | 5,285 | 9.7% | 1,739 |  | Restated |
| 2018 | 57,499 | 7,830 | 13.6% | 1,722 |  |  |
| 2019 | 32,255 | -6,657 | -20.6% | 1,834 |  |  |
| 2020 | 16,162 | -13,847 | -85.7% | 1,303 |  | Reclassified |
| 2021 | 19,714 | -6,377 | -32.3% | 980 | incl. BCC | Reclassified |
| 2022 | 26,026 | -2,341 | -9.0% | 1,222 | incl. BCC | Reclassified |
| 2023 | 33,901 | -1,635 | -4.8% | 1,527 | incl. BCC |  |
| 2024 | 22,861 | -7,969 | -34.9% | 2,230 | incl. BCC |  |
| 2025 (GS) | 41,494 | -7,079 | -17.1% | 2,942 | GS SEG / CFLO |  |

## 3. R&D intensity around the 787 and 737 MAX developments [FIN: 3c]

Windows overlap. The aggregate % is total R&D divided by total revenue over the window.

| Program | Phase | Years | Avg R&D $m/yr | Aggregate R&D % rev | Mean of annual % | Range % | Peak R&D year ($m) |
|---|---|---|---|---|---|---|---|
| 787 | before | 1999-2003 | 1,602 | 2.95% | 2.96% | 2.3-3.3 | 2001 (1,936) |
| 787 | during | 2004-2012 | 3,645 | 5.69% | 5.64% | 3.7-9.5 | 2009 (6,506) |
| 787 | after | 2013-2017 | 3,204 | 3.47% | 3.48% | 3.4-3.6 | 2016 (3,391) |
| 737 MAX | before | 2006-2010 | 4,300 | 6.69% | 6.64% | 5.3-9.5 | 2009 (6,506) |
| 737 MAX | during | 2011-2017 | 3,319 | 3.80% | 3.87% | 3.4-5.7 | 2011 (3,918) |
| 737 MAX | after | 2018-2022 | 2,813 | 3.86% | 3.92% | 3.2-4.3 | 2018 (3,269) |
| latest | post-crisis | 2023-2025 | 3,601 | 4.62% | 4.70% | 4.0-5.7 | 2024 (3,812) |
| reference | 1995-2003 (all pre-787) | 1995-2003 | 1,682 | 3.42% | 3.56% | 2.3-5.1 | 2001 (1,936) |

**Decision use.**
- 787-era intensity (5.69%) is the practical ceiling for R&D.
- MAX-era intensity (3.80%) is the "flat R&D" norm.
- The 2023-25 level is 4.62%.

## 4. Capital returned vs free cash flow [FIN: 3d]

A positive "repurchased" value in the banks' models is an equity issuance.

| FY | FCF | Buybacks | Dividends | Returned | Returned % FCF | Equity issued |
|---|---|---|---|---|---|---|
| 2004 | 2,480 | 752 | 648 | 1,400 | 56% |  |
| 2005 | 5,504 | 2,877 | 820 | 3,697 | 67% |  |
| 2006 | 6,043 | 1,698 | 956 | 2,654 | 44% |  |
| 2007 | 7,912 | 2,775 | 1,096 | 3,871 | 49% |  |
| 2008 | -2,041 | 2,937 | 1,192 | 4,129 | – |  |
| 2009 | 4,444 | 50 | 1,220 | 1,270 | 29% |  |
| 2010 | 1,890 | 0 | 1,253 | 1,253 | 66% |  |
| 2011 | 2,404 | 0 | 1,244 | 1,244 | 52% |  |
| 2012 | 5,902 | 0 | 1,322 | 1,322 | 22% |  |
| 2013 | 6,081 | 2,801 | 1,467 | 4,268 | 70% |  |
| 2014 | 6,622 | 6,001 | 2,115 | 8,116 | 123% |  |
| 2015 | 6,913 | 6,751 | 2,490 | 9,241 | 134% |  |
| 2016 | 7,886 | 7,001 | 2,756 | 9,757 | 124% |  |
| 2017 | 11,605 | 9,236 | 3,417 | 12,653 | 109% |  |
| 2018 | 13,600 | 9,000 | 3,946 | 12,946 | 95% |  |
| 2019 | -4,280 | 2,651 | 4,630 | 7,281 | – |  |
| 2020 | -19,713 | 0 | 1,158 | 1,158 | – |  |
| 2021 | -4,396 | 0 | 0 | 0 | – |  |
| 2022 | 2,290 | 0 | 0 | 0 | 0% |  |
| 2023 | 4,433 | 0 | 0 | 0 | 0% |  |
| 2024 | -14,310 | 0 | 0 | 0 | – | 23,857 |
| 2025 | -1,877 | 0 | 331 | 331 | – |  |
| 2026E GS | 2,207 | 0 | 0 | 0 | 0% |  |
| 2027E GS | 8,263 | 4,000 | 0 | 4,000 | 48% |  |
| 2028E GS | 14,183 | 10,000 | 0 | 10,000 | 71% |  |
| 2026E MS | 2,171 | 0 | 346 | 346 | 16% |  |
| 2027E MS | 6,809 | 0 | 346 | 346 | 5% |  |
| 2028E MS | 10,287 | 0 | 209 | 209 | 2% |  |
| 2029E MS | 10,796 | 0 | 209 | 209 | 2% |  |
| 2030E MS | 12,690 | 0 | 209 | 209 | 2% |  |

**Decision use.**
- Buybacks are the shock absorber: zero in 2010-12 and from 2020.
- The dividend was suspended only in 2020.
- Returns stay off in both forecasts until at least 2027E, so a program launch competes with debt paydown, not with buybacks.

By era:

| Era | Cum. FCF | Buybacks | Dividends | Returned | Returned % FCF | Equity issued |
|---|---|---|---|---|---|---|
| 2004-2012 | 34,538 | 11,089 | 9,751 | 20,840 | 60% | 0 |
| 2013-2019 | 48,427 | 43,441 | 20,821 | 64,262 | 133% | 0 |
| 2013-2018 | 52,707 | 40,790 | 16,191 | 56,981 | 108% | 0 |
| 2020-2025 | -33,573 | 0 | 1,489 | 1,489 | n/m (FCF ≤ 0) | 23,857 |
| 2026-2028 (GS forecast) | 24,653 | 14,000 | 0 | 14,000 | 57% | 0 |
| 2026-2030 (MS forecast) | 42,753 | 0 | 1,320 | 1,320 | 3% | 0 |

## 5. Negative-FCF years [FIN: 3b]

| FY | FCF |
|---|---|
| 2008 | -2,041 |
| 2019 | -4,280 |
| 2020 | -19,713 |
| 2021 | -4,396 |
| 2024 | -14,310 |
| 2025 | -1,877 |

- 6 of 29 years in FY1997-FY2025 had negative FCF, and 5 of those were in FY2019-FY2025.
- Cumulative FCF was 87,245 over FY2004-FY2018 and -37,853 over FY2019-FY2025.
- Forecasts: GS has no negative years in 2026E-28E, with cumulative FCF of 24,653. MS has no negative years in 2026E-30E, with cumulative FCF of 19,267 over 2026E-28E and 42,753 over 2026E-30E.

## 6. Debt build-up since 2019 [FIN: 3e]

| FY | Debt (GS) | Debt (MS) | Cash+STI | Net debt (GS) | Net debt (MS) | Equity | Interest exp. | New borrowings | Repayments |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | 13,847 | 13,847 | 8,564 | 5,283 | 5,459 | 410 | 475 | 8,548 | 7,183 |
| 2019 | 27,302 | 27,302 | 10,030 | 17,272 | 17,358 | -8,300 | 722 | 25,389 | 12,171 |
| 2020 | 63,583 | 63,583 | 25,590 | 37,993 | 38,076 | -18,075 | 2,156 | 47,248 | 10,998 |
| 2021 | 58,102 | 58,102 | 16,244 | 41,858 | 41,910 | -14,846 | 2,682 | 9,795 | 15,371 |
| 2022 | 57,001 | 57,001 | 17,220 | 39,781 | 39,781 | -15,848 | 2,533 | 34 | 1,310 |
| 2023 | 52,307 | 52,307 | 15,965 | 36,342 | 36,342 | -17,228 | 2,459 | 75 | 5,216 |
| 2024A | 53,864 | 53,864 | 26,282 | 27,582 | 27,582 | -3,914 | 2,725 | 10,161 | 8,673 |
| 2025A | 54,098 | 54,098 | 29,400 | 24,698 | 24,698 | 5,457 | 2,771 | 165 | 3,621 |
| 2026E | 46,148 | 49,648 | 23,637 | 22,511 | 22,840 | 2,521 | 2,512 | 0 | 7,950 |
| 2027E | 41,848 | 41,848 | 23,570 | 18,278 | 16,377 | 7,878 | 2,197 | 0 | 4,300 |
| 2028E | 40,048 | 40,048 | 25,913 | 14,135 | 6,299 | 8,183 | 2,103 | 0 | 1,800 |

- Debt rose from 13,847 in FY2018 to a peak of 63,583 in FY2020. That is +49,736, or 4.6x. It stood at 54,098 at FY2025. For comparison, FY2004-FY2018 debt ranged from 7,512 (FY2008) to 13,847 (FY2018).
- Gross new borrowings over FY2019-FY2025 were 92,867, against repayments of 57,360. The FY2024 equity raise was 23,857.
- Net debt went from 5,283 to 24,698 over FY2018-FY2025. Interest expense went from 475 to 2,771, and shareholders' equity from 410 to 5,457.
- Forecasts: GS has debt at 40,048 and net debt at 14,135 in 2028E. MS has debt at 40,048 and net debt at -16,768 in 2030E.
- **Decision use.** Boeing's stated target is close to, not beyond, the 2017-18 posture. Compare each forecast year's net debt with FY2018 to judge whether the "solidly investment grade" gate for a new airplane has closed. On MS it closes around 2028E-29E; on GS it is still open in 2028E.

## 7. BCA margin swings [FIN: 3a]

A turning point needs a reversal of at least 2 pp (zig-zag rule).

| From | Margin | To | Margin | Change (pp) | Years | Move |
|---|---|---|---|---|---|---|
| 2004 | 3.7% | 2007 | 10.7% | +7.0 | 3 | trough→peak |
| 2007 | 10.7% | 2009 | -1.7% | -12.4 | 2 | peak→trough |
| 2009 | -1.7% | 2013 | 10.9% | +12.7 | 4 | trough→peak |
| 2013 | 10.9% | 2016 | 3.3% | -7.6 | 3 | peak→trough |
| 2016 | 3.3% | 2018 | 13.6% | +10.3 | 2 | trough→peak |
| 2018 | 13.6% | 2020 | -85.7% | -99.3 | 2 | peak→trough |
| 2020 | -85.7% | 2023 | -4.8% | +80.9 | 3 | trough→peak |
| 2023 | -4.8% | 2024 | -34.9% | -30.0 | 1 | peak→trough |
| 2024 | -34.9% | 2025 | -17.1% | +17.8 | 1 | trough→peak |

- **Largest peak-to-trough fall, 2004-2025**: 13.6% in FY2018 to -85.7% in FY2020, a fall of 99.3 pp. By FY2025 the margin had not recovered to the peak.
- **The same test on GS `SEG`, 1997-2025**: 13.6% in FY2018 to -85.7% in FY2020, a fall of 99.3 pp. GS FY1997 BCA margin: -6.8%.
- **Years with a negative BCA margin**: 2009, 2019, 2020, 2021, 2022, 2023, 2024, 2025. The count is 8 of 22 years.
- **Forward recovery against the pre-crisis peak** of 13.6% in FY2018: GS 2028E reaches 11.6%, MS 2028E 9.8% and MS 2030E 9.9%.

## 8. Analyst forward view, 2024A-2030E (GS vs MS)

GS financial statements stop at 2028E. Neither model contains a new-airplane program line [FIN: 2e].

**Decision use.** This is the funding-capacity table for fps. Set the war game's fps capex (from `rules`, Solo or Joint Venture share) against FCF and net debt in the launch year. Nothing here includes that spend.

### 8a. Company totals, cash flow, balance sheet and capital return [FIN: 2d]

| Line | Src | 2024A | 2025A | 2026E | 2027E | 2028E | 2029E | 2030E | Source (sheet › row label) |
|---|---|---|---|---|---|---|---|---|---|
| Total revenue | GS | 66,517 | 89,463 | 96,650 | 115,342 | 127,690 | – | – | GS `IS` › “Sales” (row 8) |
| Total revenue | MS | 66,517 | 89,463 | 99,715 | 108,378 | 113,112 | 117,045 | 120,345 | MS `Income_Statement_Annual` › “Total Net Sales” (row 10) |
| Total operating income (GAAP) | GS | -10,707 | 4,281 | 2,863 | 9,368 | 14,014 | – | – | GS `IS` › “Earnings from operations” (row 18) |
| Total operating income (GAAP) | MS | -10,707 | 4,281 | 2,112 | 8,682 | 10,865 | 11,359 | 11,817 | MS `Income_Statement_Annual` › “Operating Profit” (row 34) |
| Total R&D expense | GS | 3,812 | 3,615 | 3,245 | 4,037 | 4,469 | – | – | GS `IS` › “Research and development expense, net (sign flipped)” (row 16) |
| Total R&D expense | MS | 3,812 | 3,615 | 3,769 | 4,050 | 4,357 | 4,692 | 5,057 | MS `Income_Statement_Annual` › “Total R&D Expense” (row 115) |
| Net income | GS | -11,867 | 1,890 | 1,277 | 7,103 | 11,187 | – | – | GS `IS` › “Net income reported” (row 26) |
| Net income | MS | -11,829 | 2,238 | 475 | 5,877 | 7,737 | 8,230 | 8,594 | MS `Income_Statement_Annual` › “Net earnings” (row 46) |
| Cash from operations | GS | -12,080 | 1,065 | 6,207 | 11,463 | 16,883 | – | – | GS `CFLO` › “Cash from Operations” (row 32) |
| Cash from operations | MS | -12,080 | 1,065 | 6,230 | 10,060 | 13,680 | 14,307 | 16,300 | MS `Cash_Flow_Annual` › “Net Cash from Operating Activities” (row 29) |
| Capex (PP&E additions) | GS | 2,230 | 2,942 | 4,000 | 3,200 | 2,700 | – | – | GS `CFLO` › “Capex (sign flipped)” (row 55) |
| Capex (PP&E additions) | MS | 2,230 | 2,942 | 4,058 | 3,251 | 3,393 | 3,511 | 3,610 | MS `Cash_Flow_Annual` › “Property, Plant and Equipment Additions (sign flipped)” (row 33) |
| Free cash flow | GS | -14,310 | -1,877 | 2,207 | 8,263 | 14,183 | – | – | GS `CFLO` › “Free cash flow” (row 56) |
| Free cash flow | MS | -14,310 | -1,877 | 2,171 | 6,809 | 10,287 | 10,796 | 12,690 | MS `Cash_Flow_Annual` › “Free Cash Flow” (row 77) |
| Cash and cash equivalents | GS | 13,801 | 10,921 | 12,058 | 11,991 | 14,334 | – | – | GS `BS` › “Cash and cash equivalents” (row 7) |
| Cash and cash equivalents | MS | 13,801 | 10,921 | 8,329 | 6,992 | 15,270 | 25,857 | 38,337 | MS `Balance_Sheet_Annual` › “Cash and Cash Equivalents” (row 5) |
| Cash + short-term investments | GS | 26,282 | 29,400 | 23,637 | 23,570 | 25,913 | – | – | GS `BS` › “Capital structure › Cash” (row 60) |
| Cash + short-term investments | MS | 26,282 | 29,400 | 26,808 | 25,471 | 33,749 | 44,336 | 56,816 | MS `Balance_Sheet_Annual` › “Cash and Cash Equivalents” (row 5) + “Short-Term and Other Investments” (row 7) (sum computed) |
| Total debt | GS | 53,864 | 54,098 | 46,148 | 41,848 | 40,048 | – | – | GS `BS` › “Capital structure › Debt” (row 63) |
| Total debt | MS | 53,864 | 54,098 | 49,648 | 41,848 | 40,048 | 40,048 | 40,048 | MS `Balance_Sheet_Annual` › “Total Debt” (row 82) |
| Net debt | GS | 27,582 | 24,698 | 22,511 | 18,278 | 14,135 | – | – | GS `BS` › “Capital structure › Net debt” (row 64) |
| Net debt | MS | 27,582 | 24,698 | 22,840 | 16,377 | 6,299 | -4,288 | -16,768 | MS `Balance_Sheet_Annual` › “Net Debt” (row 83) |
| Total shareholders' equity | GS | -3,914 | 5,457 | 2,521 | 7,878 | 8,183 | – | – | GS `BS` › “Total shareholder's equity” (row 48) |
| Total shareholders' equity | MS | -3,914 | 5,457 | 6,357 | 12,660 | 20,614 | 29,060 | 37,871 | MS `Balance_Sheet_Annual` › “Total Equity” (row 62) |
| Common shares repurchased (−) / issued (+) | GS | 23,857 | 0 | 0 | -4,000 | -10,000 | – | – | GS `CFLO` › “Common shares repurchased” (row 45) |
| Common shares repurchased (−) / issued (+) | MS | 18,200 | 0 | 0 | 0 | 0 | 0 | 0 | MS `Cash_Flow_Annual` › “Common Shares Repurchased/Issued” (row 51) |
| Preferred stock issued | MS | 5,657 | 0 | 0 | 0 | 0 | 0 | 0 | MS `Cash_Flow_Annual` › “Preferred Stock” (row 53) |
| Dividends paid | GS | 0 | -331 | 0 | 0 | 0 | – | – | GS `CFLO` › “Dividends paid” (row 46) |
| Dividends paid | MS | 0 | -331 | -346 | -346 | -209 | -209 | -209 | MS `Cash_Flow_Annual` › “Dividends Paid” (row 52) |
| Dividend per share ($) | GS | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | – | – | GS `IS` › “Cash Dividend/Share” (row 42) |
| Dividend per share ($) | MS | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | MS `Income_Statement_Annual` › “Dividend Per Share” (row 92) |

### 8b. BCA financials [FIN: 2c]

| Line | Src | 2024A | 2025A | 2026E | 2027E | 2028E | 2029E | 2030E | Source (sheet › row label) |
|---|---|---|---|---|---|---|---|---|---|
| BCA revenue | GS | 22,861 | 41,494 | 45,640 | 60,670 | 70,686 | – | – | GS `SEG` › “Revenue › Commercial Airplanes” (row 35) |
| BCA revenue | MS | 22,861 | 41,494 | 50,763 | 57,203 | 59,684 | 61,238 | 62,839 | MS `BCA_Annual` › “Net Sales” (row 3) |
| BCA operating profit (reported) | GS | -7,969 | -7,079 | -1,032 | 4,429 | 8,200 | – | – | GS `SEG` › “Operating Income › Commercial Airplanes” (row 168) |
| BCA operating profit (reported) | MS | -7,969 | -7,079 | -995 | 4,404 | 5,873 | 6,048 | 6,229 | MS `BCA_Annual` › “Operating Profit” (row 13) |
| BCA operating margin (reported) | GS | -34.9% | -17.1% | -2.3% | 7.3% | 11.6% | – | – | GS `SEG` › “Operating Margin › Commercial Airplanes” (row 221) |
| BCA operating margin (reported) | MS | -34.9% | -17.1% | -2.0% | 7.7% | 9.8% | 9.9% | 9.9% | MS `BCA_Annual` › “% Margin” (row 15) |
| BCA margin ex one-time/abnormal costs | GS | -0.3% | 4.2% | 6.0% | 8.7% | 11.6% | – | – | GS `BCA margin` › “BCA EBIT post-R&D › Margin” (row 85) |
| BCA margin ex one-time/abnormal costs | MS | -15.8% | -5.1% | -2.0% | 7.7% | 9.8% | 9.9% | 9.9% | MS `BCA_Annual` › “Adjusted Margins” (row 42) |
| BCA one-time items / charges | GS | 7,891 | 8,816 | 3,800 | 800 | 0 | – | – | GS `BCA margin` › “One-time items, abnormal cost” (row 87) |
| BCA one-time items / charges | MS | 4,350 | 4,950 | 0 | 0 | 0 | 0 | 0 | MS `BCA_Annual` › “Memo › Charges › Total (sign flipped)” (row 32) |
| BCA R&D | GS | 1,597 | 1,636 | 1,700 | 1,800 | 1,900 | – | – | GS `BCA margin` › “BCA R&D” (row 83) |
| BCA R&D | MS | 2,386 | 2,202 | 2,422 | 2,664 | 2,931 | 3,224 | 3,546 | MS `BCA_Annual` › “R&D Expense, net” (row 6) |

### 8c. Commercial deliveries [FIN: 2a]

| Line | Src | 2024A | 2025A | 2026E | 2027E | 2028E | 2029E | 2030E | Source (sheet › row label) |
|---|---|---|---|---|---|---|---|---|---|
| 737 deliveries | GS | 265 | 447 | 518 | 614 | 656 | 700 | 740 | GS `Commercial` › “737 (units)” (row 32) |
| 737 deliveries | MS | 265 | 447 | 498 | 579 | 624 | 624 | 624 | MS `BCA_Deliveries_Annual` › “737” (row 5) |
| 787 deliveries | GS | 51 | 88 | 110 | 136 | 157 | 174 | 184 | GS `Commercial` › “787 (units)” (row 78) |
| 787 deliveries | MS | 51 | 88 | 101 | 120 | 120 | 120 | 120 | MS `BCA_Deliveries_Annual` › “787” (row 9) |
| 777 family deliveries (777 + 777X) | GS | 14 | 35 | 12 | 31 | 46 | 60 | 65 | GS `Commercial` › “777 (units)” (row 67) |
| 777 family deliveries (777 + 777X) | MS | 14 | 35 | 36 | 48 | 48 | 48 | 48 | MS `BCA_Deliveries_Annual` › “777” (row 8) |
|   of which 777F | GS | 13 | 35 | 12 | 5 | 2 | – | – | GS `Commercial` › “777F” (row 61) |
|   of which 777-8X | GS | 0 | 0 | 0 | 12 | 16 | 18 | 20 | GS `Commercial` › “777-8X” (row 63) |
|   of which 777-9X | GS | 0 | 0 | 0 | 14 | 28 | 42 | 45 | GS `Commercial` › “777-9X” (row 65) |
| 767 deliveries | GS | 18 | 30 | 25 | 27 | 28 | 30 | 30 | GS `Commercial` › “767 (units)” (row 52) |
| 767 deliveries | MS | 18 | 30 | 36 | 0 | 0 | 0 | 0 | MS `BCA_Deliveries_Annual` › “767” (row 7) |
| Total commercial deliveries | GS | 348 | 600 | 665 | 808 | 887 | 964 | 1,019 | GS `Commercial` › “Total Units Delivered” (row 108) |
| Total commercial deliveries | MS | 348 | 600 | 671 | 747 | 792 | 792 | 792 | MS `BCA_Deliveries_Annual` › “Total” (row 14) |

### 8d. Modelled assumptions [FIN: 2e]

| Assumption | GS | MS | Where |
|---|---|---|---|
| 737 rate path | Production of 39.7, 41.6, 43.6, 44.6 per month in 1Q-4Q26E. Underlying monthly production of 45.04 in FY26E and 53.39 in FY27E. Delivery “Rate” of 45.0, 53.4, 57.0, 60.9, 64.3 per month over 2026E-30E | Production of 41.5, 48.2, 52.0, 52.0, 52.0 per month over 2026E-30E (498, 579, 624, 624, 624 units a year), flat after 2028E | GS `FCF build`, `Commercial`; MS `Inventory` |
| 787 rate path | Production of 20.30, 23.20, 24.65, 29.00 units a quarter in 1Q-4Q26E. Underlying monthly production of 9.57 in FY26E and 11.83 in FY27E. Delivery “Rate” of 9.6, 11.8, 13.7, 15.1, 16.0 per month over 2026E-30E | Production of 8.0, 10.0, 10.0, 10.0, 10.0 per month over 2026E-30E (96, 120, 120, 120, 120 units a year) | GS `FCF build`, `Commercial`; MS `Inventory` |
| 777X entry into service | Neither model states an EIS date. GS's first 777X deliveries are in 2027E: 14 777-9X and 12 777-8X. The 777-9X ramps to 14, 28, 42, 45 over 2027E-2030E. The 777F runs down (12, 5, 2 over 2026E-28E). `FCF build` “777X deferred” units: 2027E 14, 2028E 28 | No 777X line. 777 family deliveries are 36, 48, 48, 48, 48 over 2026E-30E, at a flat price of 160 $m | GS `Commercial` rows 63/65; MS `BCA_Deliveries_Annual`, `Inventory` |
| 737-7 / 737-10 certification (implied) | First deliveries in 2026E: 737-7 at 13 and 737-10 at 19. The 737-10 reaches 115 in 2030E | Not split | GS `Commercial` |
| 767 line | Continues at 25, 27, 28, 30, 30 over 2026E-30E | 36 in 2026E, then 0 from 2027E (production ends) | GS `Commercial`; MS `BCA_Deliveries_Annual` |
| R&D for a new airplane | Neither model has an explicit new-airplane program line. GS BCA R&D is 1,636, 1,700, 1,800, 1,900 over 2025A-28E, and total R&D is 3,615 → 4,469 | BCA R&D grows 10% a year, 2,202 → 3,546 over 2025A-30E. Total R&D goes 3,615 → 5,057 | GS `BCA margin` “BCA R&D”, `IS`; MS `BCA_Annual`, `Income_Statement_Annual` |
| Capital return | Buybacks resume at 4,000 in 2027E and 10,000 in 2028E. DPS is 0 through 2028E | No buybacks. DPS is reinstated at $0.25 in 2028E. Preferred dividends are 346 in 2026E-27E | GS `CFLO`, `IS`; MS `Cash_Flow_Annual`, `Income_Statement_Annual` |
| Deleveraging | Debt goes 54,098 → 40,048 by 2028E, and net debt goes 24,698 → 14,135 | Debt goes 54,098 → 40,048 by 2030E, and net debt goes 24,698 → -16,768 | GS `BS`; MS `Balance_Sheet_Annual` |

## 9. 10-K cross-checks (tk1-tk4)

Values as originally reported in each 10-K. Page numbers are `boeing_10k.txt` markers. FCF in the tk files is operating cash flow minus capex, **derived** by those files.

**Decision use.** These tables document how long program costs linger:
- 787 deferred production built up for years before it unwound;
- the 747, KC-46A and 777X took charges year after year;
- the capital-return log shows how buybacks paused and restarted.

Use them to size private slip and charge budgets, not to forecast.

### 9a. Commercial Airplanes (BCA) R&D, $M

| FY | BCA R&D | Source |
|---|---|---|
| 2008 | 2,838 | [tk2: FY2008] p848 |
| 2009 | 5,383 | [tk2: FY2011] p1214; [tk3: FY2009] p1726 |
| 2010 | 2,975 | [tk2: FY2011] p1214; [tk3: FY2010] p1889 |
| 2011 | 2,715 | [tk2: FY2011] p1214 |
| 2012 | 2,049 | [tk1: FY2012] p29 |
| 2013 | 1,807 | [tk4: FY2013] p.2664 |
| 2014 | 1,881 | [tk4: FY2014] p.2045 |
| 2015 | 2,340 | [tk2: FY2015] p656, p660 |
| 2016 | 3,755 (3,706 as shown in the FY2018 10-K) | [tk2: FY2016] p994, p997; [tk4: FY2018] p.2501 |
| 2017 | 2,247 | [tk1: FY2017] p170 |
| 2018 | 2,188 | [tk4: FY2018] p.2501 |
| 2019 | 1,956 | [tk1: FY2019] p496 |
| 2020 | 1,385 | [tk3: FY2020] p1368 |
| 2021 | 1,140 | [tk3: FY2022] p1533 (comparative) |
| 2022 | 1,510 | [tk3: FY2022] p1533 |
| 2023 | 2,036 | [tk1: FY2023] p320 |
| 2024 | 2,386 | [tk4: FY2024] p.2195, p.2198 |

### 9b. 787 (and 737) deferred production costs, $M

| Year-end | 787 deferred production | 737 deferred production | Source |
|---|---|---|---|
| 2011 | 10,753 | – | [tk2: FY2011] p1264 |
| 2012 | 15,929 | – | [tk4: FY2013] p.2715; [tk1: FY2012] p80 ($15.9bn) |
| 2013 | 21,620 | – | [tk4: FY2013] p.2715 |
| 2014 | 26,149 | – | [tk4: FY2014] p.2097; [tk2: FY2015] p710 |
| 2015 | 28,510 | – | [tk2: FY2015] p710 |
| 2016 | 27,308 | – | [tk2: FY2016] p1048 |
| 2017 | 25,358 | – | [tk4: FY2018] p.2565; [tk1: FY2017] p224 ($25.4bn) |
| 2018 | 22,967 | – | [tk4: FY2018] p.2565 |
| 2019 | 18,716 | – | [tk3: FY2020] p1431; [tk1: FY2019] p551 ($18.7bn) |
| 2020 | 14,976 | – | [tk3: FY2020] p1431 |
| 2022 | 12,689 | – | [tk3: FY2022] p1586 |
| 2023 | $12.4bn | $6.0bn | [tk1: FY2023] p371 |
| 2024 | 13,178 | 9,679 | [tk4: FY2024] p.2246, p.2247 |

### 9c. Charges, reach-forward losses and abnormal costs, $M

| Year | Item | Amount | Source |
|---|---|---|---|
| 2008 | 747 reach-forward loss | 685 | [tk2: FY2008] p851; [tk3] p1729 |
| 2009 | 787 flight-test aircraft moved to R&D | 2,693 | [tk2: FY2011] p1215; [tk3] p1730 |
| 2009 | 747 reach-forward loss | 1,352 | [tk2: FY2011] p1215; [tk3] p1729 |
| 2014 | KC-46A reach-forward loss | 425 (238 at BCA) | [tk4: FY2014] p.2046 |
| 2015 | 747 reach-forward loss; KC-46A loss | 885; 835 (513 at BCA) | [tk2: FY2015] p653, p654, p662 |
| 2016 | 747 losses; KC-46A losses; 787 flight-test reclassification | 1,258 (70 Q1 + 1,188 Q2); 1,128 (772 at BCA); 1,235 | [tk2: FY2016] p991, p995, p1000 |
| 2017 | KC-46A reach-forward loss | 471 (restated 445 in the FY2019 10-K) | [tk1: FY2017] p166; [tk1: FY2019] p489 |
| 2018 | KC-46A reach-forward loss | 736 | [tk4: FY2018] p.2496 |
| 2019 | 737 MAX customer concessions (net of $500m insurance) | 8,259 | [tk1: FY2019] p473; [tk3] p1345 |
| 2019 | 737 MAX program cost increase; abnormal costs expected 2020-21 | $6.3bn; $4.0bn | [tk1: FY2019] p517 |
| Q4 2020 | 777X reach-forward loss; DOJ DPA | 6,493; 744 | [tk3: FY2020] p1364, p1344 |
| Q4 2021 | 787 reach-forward loss | 3,460 | [tk3: FY2022] p1530; [tk1: FY2023] p324 |
| 2022 | Abnormal production costs | 1,753 | [tk3: FY2022] p1536 |
| 2023 | Abnormal production costs (787 1,014; 777X 513) | 1,527 | [tk1: FY2023] p324 |
| 2024 | 777X reach-forward losses (2,608 + 891); 767 (398 + 182); BDS fixed-price | 3,499; 580; $5.0bn | [tk4: FY2024] p.2202, p.2201, p.2177-2178 |

MAX concessions paid in cash: $2.5bn (2021), $1.0bn (2022), $0.4bn (2023) [tk1: FY2023] p333.

### 9d. Capital-return actions and balance-sheet events

| Date / FY | Action | Source |
|---|---|---|
| Feb 2009 | Buybacks suspended | [tk1: FY2012] p20 |
| Dec 2012 | Buyback restart announced, $1.5-2.0bn for 2013 | [tk1: FY2012] p20, p43 |
| Dec 2013 | New $10bn buyback plan; quarterly dividend raised to $0.73 | [tk4: FY2013] p.2654, p.2759 |
| Dec 2014 | New $12bn buyback plan | [tk4: FY2014] p.2061 |
| Dec 2015 | New $14bn buyback authorization | [tk2: FY2015] p673 |
| Dec 2016 | New $14bn buyback authorization | [tk2: FY2016] p1010 |
| FY2017 | New $18bn buyback authorization | [tk1: FY2017] p184 |
| Dec 2018 | New $20bn buyback plan; Embraer JV terms: 80% for $4.2bn | [tk4: FY2018] p.2518, p.2557 |
| Apr 2019 | Buybacks suspended | [tk3: FY2020] p1384; [tk1: FY2019] p509 |
| Jan 2020 | $12bn term loan committed | [tk1: FY2019] p510 |
| Mar 2020 | Dividend suspended | [tk3: FY2020] p1384 |
| FY2020 | $3bn of stock contributed to the pension | [tk3: FY2020] p1385 |
| FY2023 | Net debt repayment of $5.1bn | [tk1: FY2023] p334 |
| Q4 2024 | Common 18,200 + mandatory convertible preferred 5,657; plus $10.0bn senior notes; preferred dividend up to $345m a year | [tk4: FY2024] p.2224, p.2208, p.2181 |
| FY2024 | Spirit acquisition, all-stock, equity value about 4,700 plus net debt | [tk4: FY2024] p.2239 |

### 9e. Dividends declared per share, $

| FY | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DPS | 1.62 | 1.68 | 1.68 | 1.70 | 1.81 | 2.185 | 3.10 | 3.82 | 4.69 | 5.97 | 7.19 | 8.22 |

Sources: [tk2: FY2008] p841; [tk2: FY2011] p1208; [tk1: FY2012] p21; [tk4: FY2013] p.2655; [tk4: FY2014] p.2038; [tk2: FY2015] p650; [tk2: FY2016] p987; [tk1: FY2017] p163; [tk4: FY2018] p.2493; [tk1: FY2019] p485. There were no common dividends after the 2020 suspension [tk4: FY2024] p.2208.
