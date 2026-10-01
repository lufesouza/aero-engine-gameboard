# Pratt & Whitney: financials

Key tables for P&W, the engine segment of UTC (to April 2020) and then RTX. Every figure is copied from `evidence.jsonl` (ids P-####), the calibration memo or the live engine `rules`. No new numbers are introduced.

**Units.** $ for reported figures, $mn or $bn as in the source. $B (the engine's unit) only in § Game calibration.

**Tags.**
- [record]: reported actuals, including the history columns of the Goldman Sachs RTX model of 21 Oct 2025 ("GS").
- [analyst]: GS estimates and plugs (E = estimate).
- [own]: company words or filings.

**Two GS bases.** "Data" is reported segment profit. "SEG" is adjusted profit, before one-time items. GS's GTF Analysis sheet is not reconciled to its segment model after 2023 (2024 revenue $18,845mn against $28,066mn), so use it for unit economics, not totals [P-1789].

## 1. P&L by era (P&W segment)

**GS series** [record]:

| Era | Revenue | Adjusted margin | Reported operating profit | ids |
|---|---|---|---|---|
| 1997-2003, mature | $7,402mn (1997), $7,366mn (2000), $7,484mn (2003) | 11.0% (1997), 8.3% (1999), 17.0% (2001), 14.2% (2003) | $816mn (1997), $634mn (1999), $1,308mn (2001), $1,063mn (2003) | P-0025, P-0027, P-0028 |
| 2004-08, harvest (no new engine) | $8,281mn to $13,849mn | 17.0% (2006), 15.9% (2008) | $1,083mn (2004) to $2,122mn (2008) | P-0026, P-0028 |
| 2009-10, financial crisis | $12,392mn, $12,935mn | 16.3%, 16.4% | $1,835mn, $1,987mn | P-0030, P-0028, P-0034 |
| 2011-14, pre-GTF | $12,711mn to $14,508mn | 14.8% (2011), 12.0% (2012), 14.7% (2014) | $1,867mn, $1,584mn, $1,909mn, $2,066mn | P-0031, P-0034 |
| 2015 | $14,082mn | 13.4% | $839mn, after -$1,052mn of one-time items | P-0033, P-0034, P-0009 |
| 2016-19, GTF ramp | $14,894mn, $16,545mn, $19,397mn, $20,902mn | 11.7%, 9.3%, 8.8%, 9.3% | $1,539mn, $1,345mn, $1,416mn, $1,801mn | P-0034, P-0036, P-0037 |
| 2020-21, COVID | $17,224mn, $18,150mn | 2.5%, 2.7% | -$564mn, $454mn | P-0038, P-0040, P-0041 |
| 2022 | $20,530mn | 6.1% | $1,075mn | P-0041, P-0042 |
| 2023, powder metal | $18,296mn (including a -$5,401mn revenue adjustment) | 7.1% | -$1,455mn, after -$3,143mn of one-time items | P-0042, P-0043 |
| 2024 | $28,066mn (18.4% organic growth) | 8.1% | $2,015mn | P-0044, P-0047 |
| 1Q-3Q25 | $7,366mn, $7,631mn, $8,423mn | 3Q 8.9% | $580mn, $492mn, $751mn | P-0048, P-0049 |

**GS adjusted operating income** [record]:
- 2016-19: $1,745mn, $1,546mn, $1,709mn, $1,934mn [P-0035].
- 2020-21: $426mn, $487mn [P-0040].
- 2022-23: $1,250mn, $1,688mn [P-0042].
- 2024: $2,281mn [P-0044].

GS's adjusted incremental margin was -18.0% (2016), -12.0% (2017), 5.7% (2018) and 14.9% (2019) [P-0036].

**10-K segment series** [record]. 2016-17 were restated in the FY2018 filing.

| $mn | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | ids |
|---|---|---|---|---|---|---|---|
| Sales | 14,508 | 14,082 | 14,894 | 16,160 | 19,397 | 20,892 | P-1408, P-1422, P-1449, P-1469 |
| Operating profit | 2,000 | 861 | 1,545 (restated 1,501) | 1,460 (restated 1,300) | 1,269 | 1,668 | same |
| Margin | 13.8% | 6.1% | 10.4% (10.1%) | 9.0% (8.0%) | 6.5% | 8.0% | same |

On the RTX basis:
- 2019: profit $1,801mn, an 8.6% margin.
- 2020: -$564mn (-3.4%). 2021: $454mn (2.5%). 2022: $1,075mn (5.2%).
- 2023: -$1,455mn (-8.0%). 2024: $2,015mn on $28,066mn of sales (7.2%).

Sources: [P-1504][P-1547][P-1577].

One-time items [record]: -$1,015mn (4Q15), -$194mn (3Q17), -$300mn (3Q18), -$990mn (2020), -$3,143mn (2023), -$266mn (2024), -$116mn (2Q25) [P-0009].

## 2. P&W inside UTC and RTX

| Year | P&W share of group revenue | P&W share of group operating income | ids |
|---|---|---|---|
| 2007 (UTC) | 23.5% ($13,086mn of $55,716mn) | 28.5% ($2,011mn of $7,050mn) | P-0051 |
| 2012 | 28.7% | 27.4% | P-0045 |
| 2019 | 27.2% | 18.5% (UTC basis 18.6%: $1,668mn of $8,966mn) | P-0045, P-0051 |
| 2020 | 24.8% | 8.0% | P-0045 |
| 2024 | 33.8% (GS mix; 34.7% of 2024 segment sales [P-0052]) | 24.0% | P-0045, P-0052 |
| 2025E / 2028E [analyst] | 35.7% / 37.8% | 24.8% / 26.4% | P-1795 |

- **2024 segment profit** [record]: P&W $2,015mn on $28,066mn; Collins $4,135mn on $28,284mn; Raytheon $2,594mn on $26,783mn [P-0052].
- **RTX adjusted operating income** [record]: $11,326mn (2019), $6,451mn (2020), $8,895mn (2023), $10,183mn (2024) [P-1897].
- **Airbus** was P&W's largest customer, before discounts [record]:
  - 34% (2016), 38% (2017), 36% (2018), 31% (2019), 30% (2020);
  - 31% (2021), 33% (2022), 48% (2023), 31% (2024).

  Sources: [P-1927][P-1931][P-1380][P-1386][P-1392].

## 3. OE and aftermarket drivers

### 3a. GTF unit economics ($M per engine; GS GTF Analysis) [analyst]

| Year | GTF deliveries | Net price | Unit cost | OE loss per engine | Total commercial OE impact ($mn) | ids |
|---|---|---|---|---|---|---|
| 2014 | 0 | n/a | n/a | n/a | -250 | P-0011, P-1764 |
| 2015 | n/a | 2.75 | n/a | n/a | -400 | P-1766, P-1764 |
| 2016 | 124 | 2.75 | 6.95 | -4.20 | -691 | P-0011, P-1762, P-1763, P-1764 |
| 2017 | 315 | 2.75 | 5.07 | -2.32 | -832 | same |
| 2018 | 566 | 2.75 | 4.31 | -1.56 | -975 | same |
| 2019 | 738.5 | 2.75 | 3.97 | -1.22 | -936 | same |
| 2020 | 496 | 2.75 | 4.36 | -1.61 | -821 | P-0024, P-1766, P-1768, P-1769, P-1770 |
| 2021 | 623 | 2.78 | 4.28 | -1.50 | -934 | same |
| 2022 | 712 | 2.86 | n/a | -1.29 | -917 | P-0024, P-1767, P-1769, P-1770 |
| 2023 | 900 | 2.95 | n/a | -1.16 | -1,044 | same |
| 2024 | 1,008 | 3.04 | 4.07 | -1.03 | -1,039 | P-0024, P-1767, P-1768, P-1769, P-1770 |
| 2025E | n/a | 3.13 | 4.03 | -0.90 | -979 | P-1767, P-1768, P-1769, P-1770 |
| 2026E | n/a | 3.22 | 3.99 | -0.77 | n/a | same |
| 2028E | n/a | 3.42 | 3.91 | -0.49 | -672 | same |

- **The GS price assumption.** An $11mn list price at a 75% discount gives $2.75mn, flat to 2020 and escalated 3% a year after [P-1766].
- **The V2500.** GS carries a -$0.4mn OE loss per engine. Deliveries ran 621 (2014), 558 (2015), 426.4 (2016), 250.3 (2017), 91 (2019) and 0 (2021) [P-1765].
- **The company's own figures** [own]:
  - negative engine margin of about $650mn (2016), about $1bn (2017) and about $1.2bn on "a little less than 800 engines" (2018) [P-0198][P-0219][P-0308];
  - "over $1.2 billion" (2019) [P-0376];
  - an 87% learning curve [P-0347].
- **GTF installed base** [analyst]: 124 (2016), 1,005 (2018), 2,240 (2020), 4,474 (2023), 5,482 (2024), 7,747 (2026E), 10,390 (2028E) [P-0002][P-1758].
- **Large commercial engine shipments** [record]: 538 (2016), 537 (2017), 779 (2018), 746 (2019), 546 (2020), 623 (2021) [P-0010][P-0015][P-0017]. About 875 in 2023 [own] [P-1064].

### 3b. P&W EBIT build by line ($mn; GS) [analyst; history columns record]

| Line | 2015 | 2019 | 2020 | 2024 | 2028E | ids |
|---|---|---|---|---|---|---|
| Military | 378 | 576 | 660 | 724 | 793 | P-1772, P-1776, P-1777, P-1779, P-1784 |
| Commercial OE | -700 | -1,136 | -896 | -1,039 | -672 | same |
| Commercial aftermarket ex-GTF | 2,222 | 2,497 | 643 | 2,192 | 3,104 | same |
| GTF aftermarket | n/a | 0 | 0.25 | 574 | 981 | same |
| Build total (margin) | 1,899 (13.5%) | 1,938 (9.3%) | 408 (2.4%) | 2,450 (9.3%) | 4,206 (12.6%) | same |
| Main model EBIT | 1,891 | 1,934 | 426 | 2,281 | 3,640 | same |

**Revenue build, 2019 / 2024** ($mn) [P-1790][P-1791]:
- military 5,763 / 6,891;
- commercial OE 2,957 / 3,217;
- commercial aftermarket ex-GTF 12,182 / 14,534;
- GTF aftermarket 0 / 1,641.

**Aftermarket.**
- **Ex-GTF aftermarket revenue** [P-1752]: $8,545mn (2015), $12,182mn (2019), $8,040mn (2020, -34%), $8,728mn (2021), $10,953mn (2022), $13,035mn (2023), $14,534mn (2024).
- **GTF overhaul revenue** [P-1760]: $216mn (2022), $786mn (2023), $1,625mn (2024), $2,479mn (2025E), $2,416mn (2026E), $2,256mn (2027E), $2,772mn (2028E).
- **GTF aftermarket EBIT** [P-1761]: $78mn (2022), $280mn (2023), $574mn (2024), $874mn (2025E), $852mn (2026E), $981mn (2028E).
- **GS plugs** [analyst]:
  - a $3mn overhaul, a 35% aftermarket margin and 3% annual pricing [P-1754];
  - 3,000 flight hours a year [P-1753].
- **Management** [own]:
  - the GTF aftermarket broke even in 2022 [P-0579];
  - about 10% margin in 2024 against a mid-teens target [P-0667];
  - V2500 parity "beyond 2025" [P-0478].

**Quarterly growth** [record]:
- **Commercial aftermarket y/y:**
  - -51% (2Q20 and 3Q20), +56% (3Q21) [P-0001];
  - +28% (1Q25), +5% (3Q25) [P-0003].
- **Commercial OE y/y:**
  - +74% (4Q18) [P-0004];
  - -42% (2Q20), -46% (4Q20) [P-0005];
  - +64% (1Q24), +23% (3Q25) [P-0006].

### 3c. Net GTF impact on P&W EBIT ($mn; GS) [analyst]

| Year | Net GTF (OE + aftermarket) | GTF R&D | P&W EBIT | EBIT ex-GTF | Per RTX share ($) | ids |
|---|---|---|---|---|---|---|
| 2014 | -250 | -400 | 2,129 | 2,379 | n/a | P-1773, P-1774, P-1775 |
| 2015 | -400 | -300 | n/a | n/a | n/a | P-1773, P-1774 |
| 2016 | -691 | -300 | n/a | n/a | n/a | same |
| 2017 | -832 | -300 | n/a | n/a | n/a | same |
| 2018 | -975 | -200 | n/a | n/a | n/a | same |
| 2019 | -936 | -200 | 1,934 | 2,870 | -0.53 | P-1773, P-1774, P-1775, P-1969 |
| 2020 | -820 | -75 | 426 | 1,246 | -0.43 | P-1782, P-1780, P-1778, P-1969 |
| 2021 | -933 | -150 | 487 | 1,420 | -0.52 | same |
| 2022 | -839 | -100 | n/a | n/a | n/a | P-1782, P-1780 |
| 2023 | -765 | -100 | 1,688 | 2,453 | -0.48 | P-1782, P-1780, P-1778, P-1969 |
| 2024 | -465 | 0 | 2,068 | 2,533 | -0.31 | same |
| 2025E | -105 | 0 | 2,655 | 2,761 | -0.07 | P-1782, P-1780, P-1783, P-1969 |
| 2027E | -0.3 | n/a | n/a | n/a | n/a | P-1782 |
| 2028E | +309 | n/a | 3,565 | 3,256 | +0.21 | P-1782, P-1783, P-1969 |

GS's EBIT before GTF effects was $2,779mn (2014) and $3,070mn (2019) [P-1775].

The company's view of the whole GTF bet [own]:
- $10bn of E&D, $6bn of capital and $6-7bn of negative engine margin, with cash payback around 2030 [P-0298];
- more than $7bn of NPV on the 7,000-engine order book (2016) [P-0182];
- an all-in programme return "above cost of capital, but ... more close to double-digit" (2019) [P-1243].

## 4. Cash flow and capital allocation

### 4a. RTX ($bn) [record to 2024; analyst E]

| Year | FCF | Capex | R&D | Dividends | DPS ($) | Buybacks | Net debt (x EBITDA) | ids |
|---|---|---|---|---|---|---|---|---|
| 2018 | 5.08 | 2.54 | 3.25 | 2.50 | 1.71 | 1.33 | n/a | P-1901, P-1886, P-1882, P-1888, P-1887, P-1883 |
| 2019 | 6.70 | 2.88 | 3.19 | 2.88 | 1.90 | 0.80 | 38.3 (2.87x) | same, P-1878 |
| 2020 | 2.54 | 1.80 | 2.69 | 2.73 | 1.90 | 0.05 | 23.0 (2.76x) | same, P-1879 |
| 2021 | 5.01 | 2.13 | 2.73 | 2.96 | 2.005 | 2.33 | 23.7 (2.42x) | same, P-1885 |
| 2022 | 4.88 | 2.29 | 2.71 | 3.13 | 2.16 | 2.80 | 25.7 (2.54x) | same |
| 2023 | 5.47 | 2.42 | 2.81 | 3.24 | 2.32 | 12.87 | 37.2 (3.35x) | same, P-1884 |
| 2024 | 4.53 | 2.63 | 2.93 | 3.22 | 2.48 | 0.44 | 35.7 (2.54x) | same, P-1892 |
| 2025E | 7.52 | 2.61 | 2.81 | 3.58 | 2.67 | n/a | 30.5 (2.24x) | P-1964, P-1955, P-1954, P-1956, P-1952 |
| 2026E | 8.14 | 2.72 | 3.23 | n/a | 2.92 | 3.0 | 29.3 (2.05x) | same, P-1957 |
| 2027E | 9.15 | 2.85 | 3.44 | n/a | 3.22 | 4.0 | 28.5 (1.86x) | same |
| 2028E | 9.80 | 2.88 | 3.65 | 4.71 | 3.54 | 4.5 | 27.9 (1.70x) | same |

- **Balance sheet and payout.** Debt/capital was 50.8% (2019), 30.6% (2020) and 42.3% (2023) [P-1879]. The 2023 payout ratio was 105% [P-1888].
- **2023 buyback and debt.** In 2023 RTX bought back $12.87bn, $10.28bn of it in 4Q23, and issued $12.34bn of net long-term debt [P-1884]. Buybacks were $50mn in 1Q25 and zero in 2Q-3Q25 [P-1892].
- **Net interest**: $1.08bn (2019), $1.28bn (2022), $1.51bn (2023), $1.86bn (2024) [P-1908]. GS has $1.80bn (2025E) and $1.70bn (2028E) [P-1953].
- **1Q-3Q25 FCF**: $792mn, -$72mn, $4,025mn [P-1907].
- **Quarterly dividend**: $0.475 (1Q21) to $0.68 (2Q25), raised 6.8-7.9% each Q2 [P-1891].
- **Platform payments.**
  - Collaboration intangibles: $172mn (2020), $188mn (2021), $218mn (2022), $570mn (2023), $611mn (2024) [P-1890].
  - Exclusivity assets: $2.4bn at end-2021, with $8.9bn committed [P-1720]. $3.3bn at end-2024, with $5.5bn committed net of partners [P-1750].

### 4b. P&W segment capex and D&A ($mn) [record]

| | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | ids |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Capex | 692 | 692 | 725 | 923 | 866 | 822 | 565 | 700 | 949 | 1,025 | 968 | P-1416, P-1463, P-1481, P-1527, P-1570, P-1597 |
| D&A | 390 | 476 | 550 | 672 | 852 | 980 (UTC basis); 614 (RTX restated) | 729 | 642 | 724 | 736 | 784 | P-1416, P-1463, P-1481, P-1527, P-1570, P-1597 |

D&A has a basis break: UTC's filings give 980 for 2019 and RTX's restated filing gives 614 [P-1481][P-1527]. On the RTX basis D&A rose from 614 (2019) to 784 (2024); it did not fall.

### 4c. Who paid in each crisis

| Event | P&L | Cash and response | ids |
|---|---|---|---|
| 2015 | -$1,015mn one-time (4Q15), including the $867mn Pratt Canada royalty settlement | n/a | P-0009, P-1419 |
| GTF teething, 2016-18 | About $100mn (2016) and $196mn (3Q17) of customer charges. GS one-time items -$194mn (3Q17) and -$300mn (3Q18). Knife-edge seal about $50mn | Customer financing for spare engines; UTC warranty issued $246mn → $323mn → $604mn (2016-18) | P-0279, P-0273, P-0009, P-0300, P-1455, P-1418, P-1441, P-1459 |
| COVID, 2020 | -$990mn one-time; adjusted margin 2.5%; $543mn of contract adjustments (3Q20) | FCF $6.70bn → $2.54bn; capex -38%; buybacks $47mn; DPS held at $1.90 | P-0009, P-0040, P-0432, P-1901, P-1886, P-1883, P-1887 |
| Powder metal, 2023-26 | $5.4bn against sales; $2.9bn P&W-net after partners' 49% ($2.5bn); 3Q23 one-time items -$2,895mn | Plan: $0.5bn, $1bn and $1.5bn (2023-25), re-phased to about $1.3bn (2024), $1.5bn (2025) and the rest in 2026. About $1.1bn paid in 2024. GS: $0.3bn, $2.3bn, $1.2bn and $0.7bn (2023-26E). $12.87bn buyback on $12.34bn of new debt | P-1563, P-0021, P-0599, P-0616, P-0652, P-1781, P-1884 |

## 5. Guidance versus outcome

| Item | Guided | Outcome | ids |
|---|---|---|---|
| 2016 GTF deliveries | "Just over 200", reaffirmed to Jul 2016 | Cut to about 150 (Sep). 138 delivered | P-0809, P-0812, P-0814, P-0833 |
| 2016 P&W profit | $1.715-1.775bn (Oct 2016) | GS adjusted $1,745mn | P-0197, P-0035 |
| 2017 P&W profit | Down about $250mn (Feb) → down $150-200mn (Jul) → down $125-175mn (Oct) | Down $90mn (company); GS adjusted $1,745mn → $1,546mn | P-0220, P-0257, P-0277, P-0289, P-0035 |
| 2018 negative engine margin | About $1.0bn (Jan 2017) → about $1.1bn (Sep 2017) → about $1.2bn (Mar 2018) | About $1.2bn on under 800 engines; GS OE impact -$975mn | P-0215, P-0269, P-0300, P-0308, P-1764 |
| 2018 P&W profit | +$25-75mn | +$61mn (company); GS adjusted $1,546mn → $1,709mn | P-0290, P-0336, P-0035 |
| 2019 P&W profit | +$200-250mn → +$225-250mn (Oct) | GS adjusted $1,709mn → $1,934mn | P-0374, P-0385, P-0035 |
| 2021 P&W profit | -$125mn to +$25mn → raised in steps → flat to +$50mn | GS adjusted $426mn → $487mn | P-0447, P-0460, P-0485, P-0493, P-0040 |
| 2022 P&W profit | +$500-600mn → +$550-650mn → +$650-700mn | GS adjusted $487mn → $1,250mn | P-0503, P-0544, P-0040, P-0042 |
| 2023 P&W profit | +$200-275mn | GS adjusted $1,250mn → $1,688mn | P-0559, P-0042 |
| 2024 P&W profit | +$400-475mn, held mid-year as the sales guide rose | GS adjusted $1,688mn → $2,281mn | P-0614, P-0635, P-0042, P-0044 |
| 2025 P&W profit | +$325-400mn → +$200-275mn (tariffs) | 1Q-3Q25 adjusted $590mn, $608mn, $751mn | P-0656, P-0679, P-0048 |
| GTF cash breakeven | "Mid-2020s" (2020) → about 2027 (2022) | No cash outcome in the evidence. GS has net GTF EBIT (not cash) at about 0 in 2027E | P-0425, P-0506, P-1782 |
| GTF aftermarket margin | Teens return on sales by 2025 | About 10% in 2024 | P-0579, P-0667 |
| Powder-metal cash | $0.5bn hit (Jul 2023) → about $3bn (Sep 2023) | GS about $4.5bn over 2023-26E | P-0588, P-0594, P-1781 |
| RTX 2025 FCF | More than $10bn (2021 plan) → $9bn → $7.5bn (Sep 2023) → $7-7.5bn (Jan 2025) | 1Q-3Q25 $0.79bn, -$0.07bn, $4.03bn; GS $7.52bn | P-0463, P-0594, P-0651, P-1907, P-1964 |
| Negative-engine-margin step-ups | +$100-150mn (2022), about +$250mn (2023), about +$125mn (2024), +$150-200mn (2025) | Unit loss never disclosed | P-0504, P-0569, P-0618, P-0663, P-0584 |

## 6. Analysts' estimates (GS, 21 Oct 2025) [analyst]

| Item | 2025E | 2026E | 2027E | 2028E | ids |
|---|---|---|---|---|---|
| P&W revenue | $31.9bn | $34.9bn | n/a | $40.4bn | P-1793 |
| P&W adjusted operating income (margin) | $2,673mn (8.4%) | $3,012mn (8.6%) | n/a | $3,640mn (9.0%) | P-1793, P-1794 |
| P&W organic growth | 13.8% | 9.3% | 8.2% | 7.1% | P-1794 |
| GTF aftermarket EBIT | $874mn | $852mn | $798mn | $981mn | P-1761 |
| RTX net sales | $87.0bn | $92.2bn | $98.3bn | $104.2bn | P-1961 |
| RTX EBIT (margin) | $9.03bn (10.4%) | $10.03bn (10.9%) | $11.04bn (11.2%) | $12.05bn (11.6%) | P-1961, P-1962 |
| RTX adjusted EPS | $6.19 | $6.60 | $7.20 | $7.85 | P-1963 |
| RTX ROIC | 6.5% | n/a | n/a | 8.2% | P-1966 |

**History.**
- RTX adjusted EPS was $6.21 (2019), $3.29 (2020) and $5.73 (2024) [record] [P-1900].
- ROIC was 16.8% (2019), -1.8% (2020) and 4.7% (2024) [record] [P-1903].

**Valuation at GS's $170 share price** [P-1967][P-1968]:
- an FCF yield of 3.3% (2025E) and 4.3% (2028E);
- 27.5x 2025E adjusted EPS.

## § Game calibration

**Sources.**
- **Values** come from the live `rules` (`python3 -m wargame.engine rules --run calib --side pratt_whitney`). They equal the calibrated values in the calibration memo, whose "live" column showed the values before the merge.
- **Derivations and ranges** come from the memo.
- **Status.** CALIBRATED means set from evidence by two independent calibrations that were then reconciled. PLACEHOLDER means the memo found no isolating evidence and kept the live value (P&W's strain leaves only). NOT CALIBRATED means the value is live but outside the P&W memo. Structural means an engine rule.

| Parameter | Value | Range | Status | Derivation | Evidence ids |
|---|---|---|---|---|---|
| `wacc` | 0.085 | 0.08-0.095 | CALIBRATED | UTC's stated cost of capital was about 8%, "not a lowball". The GTF's roughly 10% all-in return was above it. Add about 0.5pp for higher RTX net interest ($1.86bn in 2024) | P-1163, P-0267, P-1165, P-1243, P-1908, P-1878, P-1879, P-1952 |
| `alpha` | 0.35 | 0.17-0.6 | CALIBRATED | The new-engine hurdle is the GTF's "same threshold": about 10-10.5% all-in, against an 8.5% WACC. On the ramped value profile this gives alpha 0.28-0.39. Capital aversion (upgrade preference, buybacks first) is offset by an unstretched parent | P-0715, P-0734, P-0731, P-1243, P-1298, P-0766, P-0745, P-0602, P-1957, P-1964, P-1952, P-0713 |
| `engines_per_aircraft` nb / wb | 2 / 2 | — | CALIBRATED | Twins: the A320neo ("48 aircraft (96 engines)"); the 777X analogue | P-0832, P-1771, P-1981, P-0945 |
| `incumbent_fit` boeing nb / wb | 0 / 0 | — | CALIBRATED | The LEAP-1B is the exclusive 737 MAX engine. "Pratt passed on the 787" | P-1994, P-0697, P-1125, P-1979 |
| `incumbent_fit` airbus nb | 0.4 | 0.35-0.5 | CALIBRATED | GS has "A320neo @ 40%". Management: "on or about 40%". 40-50% is acceptable | P-1771, P-0084, P-0111, P-1292, P-1064, P-0165, P-0085, P-0086 |
| `incumbent_fit` airbus wb | 0 | — | CALIBRATED | No engine on the A350 or A330neo; the GP7000 is out of production | P-1934, P-1700, P-1313 |
| `incumbent_value_m_per_engine` nb | 0.6 | 0.1-1.3 | CALIBRATED | OE of -$0.77M (2026E) plus the PV of about 3 shop visits at about $3.9M. Aftermarket margin (10-35%) is the key uncertainty | P-1769, P-1767, P-1768, P-0308, P-1753, P-1755, P-1754, P-0667, P-0478, P-0705, P-0182 |
| `incumbent_value_m_per_engine` wb | 0 | — | CALIBRATED | No widebody engine on any game airframe | P-0945, P-1125, P-1313 |
| `fallback_engine` nb / wb | cfm_ducted / ge_genx_next | — | structural | Engine rule, not calibrated | n/a |
| `programs.gtf_next.dev_years` | 6 | 5-8 | CALIBRATED | A 40-45k lbf GTF-derived engine takes "5, 6 years". The technology is funded before launch | P-0712, P-0740, P-0750, P-0751, P-0785, P-0757, P-1302, P-1269 |
| `programs.gtf_next.capex_b` | 4.5 | 2-8 | CALIBRATED | $5-7bn gross E&D, about 55% retained ("probably half" partnered; 51% of the PW1100G), plus own tooling | P-0712, P-0713, P-1302, P-0190, P-0298, P-1747, P-1714, P-0183 |
| `programs.gtf_next.value_m_per_engine` | 1.05 | 0.4-1.8 | CALIBRATED | Midpoint of 1.0 (OE -0.5 plus aftermarket) and 1.1 (better sole-source OE terms). A sole-source premium over the incumbent 0.6 | P-1769, P-1754, P-0774, P-0698, P-0478, P-0705, P-0746, P-1345 |
| `programs.pw_wb.dev_years` | 7 | 6-10 | CALIBRATED | The 2019 70-100k lb plan for "the mid-2020s" was never executed; it needs a new large core | P-1842, P-1839, P-1302, P-1269 |
| `programs.pw_wb.capex_b` | 6.0 | 3-9 | CALIBRATED | $8-10bn gross, 55-65% retained | P-1842, P-1302, P-0298, P-1714, P-1744, P-1700 |
| `programs.pw_wb.value_m_per_engine` | 2.9 | 1.1-5.0 | CALIBRATED | 1.05 × the industry widebody/narrowbody engine value ratio of 2.77 | P-1982, P-1981, P-0409, P-1298, P-1313 |
| `ramp.start_frac` | -0.35 | -1.0-0 | CALIBRATED | OE loss from $4.2M to $0.49M on an 87% curve. Early aftermarket at 50-55% of mature. Re-fitted to a 5.9 engine-year PV shortfall. Powder metal is excluded (it is the inject) | P-1763, P-1769, P-0347, P-0364, P-0466, P-0579, P-0478, P-1563 |
| `ramp.years` | 10 | 7-12 | CALIBRATED | Aftermarket breakeven at 7 years, parity at about 10, net GTF EBIT breakeven at 11-12 years, payback about 2030 | P-0579, P-0571, P-0478, P-1769, P-1782, P-0298 |
| `terms.standard` (margin_pp / value_mult) | 0.0 / 1.0 | — | CALIBRATED | Baseline: no deep discounts past launch | P-0735, P-1333 |
| `terms.aggressive` (margin_pp / value_mult) | 1.1 / 0.71 | 0.7-1.6 / 0.6-0.82 | CALIBRATED | A concession of about $0.30M per engine, about 10% of the $3.1M net price. 100 × 2 × 0.30 / 55 = 1.09pp, and 1 - 0.30/1.05 = 0.71 | P-0705, P-1192, P-1243, P-0707, P-0347, P-0466, P-1767 |
| `upgrade.fit_pp` | 5 | 2-12 | CALIBRATED | About 45% of decided selections cumulative (Nov 2016) against 56% of selections in the 12 months to Nov 2016 and again Jun 2017-Jun 2018; 43% to about 55% over 2019-20. The evidence does not tie the gain to the fixes. Diluted through a backlog of about 10,000 engines, about +5pp of deliveries | P-0060, P-0075, P-0086, P-0084, P-0626, P-0111 |
| `upgrade.lag_years` | 3 | 2-5 | CALIBRATED | Block D was introduced in late 2020 and 60% embodied by mid-2023. HS+ reaches MRO in 2026 after 2025 certification | P-1821, P-0758, P-0786, P-0792, P-1817 |
| `upgrade.capex_b` | 1.0 | 0.4-2.5 | CALIBRATED | GTF R&D of $0.43bn (2020-23), plus GTF Advantage and HS+ certification and endurance testing. MRO shop capacity is excluded | P-1780, P-0639, P-1543, P-1575, P-0779, P-1095, P-0786, P-1363 |
| `upgrade.capex_years` | 3 | 2-5 | CALIBRATED | GTF Advantage went from flight test (2022) to certification (2025) | P-0751, P-0785, P-0758 |
| `upgrade.installed_base_saving_b_per_year` | 0.45 | 0.15-1.1 | CALIBRATED | 300-450 shop visits a year avoided on fixed-price contracts at $1.2-1.6M P&W-net | P-1785, P-1758, P-1753, P-1014, P-0752, P-0785, P-1188, P-1754, P-1747, P-0667 |
| `upgrade.saving_years` | 9 | 6-15 | CALIBRATED | Fixed-price contracts run 8-15 years. About 6-10 years are left from 2029 | P-0571, P-1353, P-0311, P-1520 |
| `upgrade` flag / segment / fit_side | gtf_upgrade / nb / airbus | — | structural | One-time A320neo durability upgrade | P-0786 |
| `jv` (join_rr_jv → RR `uf_nb` `jv_pw`) | flag | — | structural | Takes effect only if RR launches `jv_pw` in the same turn | n/a |
| RR `uf_nb.jv_pw` partner terms (capex_share 0.5, value_share 0.5, strain_relief 0.5, dev_years 6) | in RR's parameters | — | NOT CALIBRATED (outside the P&W memo; open issue 9) | Live value. P&W's precedent supports about 50/50: the Engine Alliance; partnering out "probably half" | P-1676, P-1700, P-1870, P-0713 |
| `strain.full_overlap_b` | 1.5 | 0.5-2.5 | PLACEHOLDER | No evidence isolates overlap cost. Context only: 2016-18 ramp charges and supplier support | P-0279, P-0009, P-0269, P-0300, P-0078, P-0854, P-1234 |
| `strain.norm_years` | 5 | — | PLACEHOLDER | The 2013-16 multi-variant overlap lasted about 4-5 years. Not a measurement | P-0190, P-0269, P-0300 |
| `strain.background` | [] | — | PLACEHOLDER | A 2026-27 fleet-recovery window was considered and not added | P-1666, P-1824, P-1826 |
| engine option `pw_gtf2` (margin_pp / eis_add / capture_mult) | 0.5 / 0 / 0.95 | — | NOT CALIBRATED (outside the P&W memo) | Live value; not in the memo | n/a |
| engine option `pw_wb_new` (margin_pp / eis_add / capture_mult) | 0.5 / 1 / 0.9 | — | NOT CALIBRATED (outside the P&W memo) | Live value; not in the memo | n/a |

**Engine checks** (P&W delta PV in $B).

*Calibration memo as committed (`wargame/profiles/pratt_whitney/calibration.md`, "Engine check"), recomputed with the engine after the price-concession change (its open issue 3, resolved); `gtf_next` launched in 2026, NGSA in 2028. All four reproduce in live `whatif` (+0.203, -4.410, -3.105, +1.759). The pre-merge draft of the memo showed in-memory values of -2.21 (aggressive) and -3.10 (CFM) under the old value x value_mult x ramp formula; those are superseded:*
- NGSA on `gtf_next`, standard terms: **+0.20**;
- aggressive terms: **-4.41**;
- NGSA on CFM: **-3.11** (live -3.105; shown as -3.11 here and in the profile);
- `gtf_upgrade` only: **+1.76**.

*Our own `whatif` on run calib, turn 1, airframes launched in 2028:*
- `gtf_next` launched in 2028: **+0.96**;
- with the upgrade in 2026: **+1.98**;
- fps on ours: **+1.65**;
- the Joint Venture joined with NGSA on UltraFan: **+13.71**;
- `pw_wb` on the 787 Re-engine: **-3.65**.

**Engine mechanics that matter for play.**
- Any two overlapping P&W development windows draw strain, including the upgrade's 3-year window, although the `rules` text names only narrowbody-plus-widebody overlaps. The upgrade in 2026 plus `gtf_next` in 2026 costs $1.12B; with `gtf_next` in 2028, $0.34B; with `gtf_next` and the Joint Venture as well, $1.22B.
- The Joint Venture partner books the owner's (RR's) engine value and ramp.

**Scale.** The status quo is 960 A320neo GTFs a year × $0.6M = $0.58B a year, about $6.9B of PV. That is about 2.1x real A320neo installs (GS has about 441-464 a year in 2019 and 2021-23, and 345 in 2020), so P&W's absolute payoffs run about 1.7-2x evidence scale [P-1771][P-0024][P-1788].
