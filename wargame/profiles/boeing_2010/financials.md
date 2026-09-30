# Boeing financials, 2010 era (locked at 30 November 2010)

**Sources.** Tables 1-4 copy rows verbatim from the script-built historical series in the shared financials file:
- [FIN: 1a], [FIN: 1b], [FIN: 3d] and [FIN: 3a] come from the Capital IQ series;
- GAAP EBIT comes from a broker model's historical column.

Tables 5-6 give values from Boeing's FY2008 and FY2009 10-Ks, cited as [tk2: FY2008] and [tk3: FY2009] with the source page markers. Table 7 gives figures from `evidence.jsonl`, cited by id.

Amounts are US$ millions unless marked otherwise. A dash (–) means the source has no value. This file adds no new numbers.

**Time lock.**
- The rows stop at FY2009, the last full year reported before 30 November 2010.
- FY2010 full-year actuals are left out on purpose: they were published only after the lock date.
- The in-year picture for 2010 comes from the evidence (Table 7).

## 1. P&L and R&D intensity, FY2004-FY2009 [FIN: 1a]

Op income is the CapIQ "Operating Income", which excludes unusual items. GAAP EBIT is reported earnings from operations.

| FY | Revenue | Op income (CapIQ) | Op margin | GAAP EBIT (GS) | R&D | R&D % rev | Net income | DPS $ |
|---|---|---|---|---|---|---|---|---|
| 2004 | 51,400 | 1,896 | 3.7% | 2,007 | 1,879 | 3.7% | 1,872 | 0.85 |
| 2005 | 53,621 | 2,204 | 4.1% | 2,812 | 2,205 | 4.1% | 2,572 | 1.05 |
| 2006 | 61,530 | 3,665 | 6.0% | 3,585 | 3,257 | 5.3% | 2,215 | 1.25 |
| 2007 | 66,387 | 5,604 | 8.4% | 5,830 | 3,850 | 5.8% | 4,074 | 1.45 |
| 2008 | 60,909 | 3,705 | 6.1% | 3,950 | 3,768 | 6.2% | 2,672 | 1.62 |
| 2009 | 68,281 | 1,871 | 2.7% | 2,096 | 6,506 | 9.5% | 1,312 | 1.68 |

**2010-era reading.**
- R&D rose from 3.7% of revenue (2004) to 9.5% (2009) through the 787 and 747-8 developments.
- The 2009 figure includes $2.7B of 787 flight-test aircraft that cannot be sold [B-0236].
- The dividend per share rose every year and was not cut in 2009 [B-0241].

## 2. Commercial Airplanes (BCA) and total capex, FY2004-FY2009 [FIN: 1b]

| FY | BCA revenue | BCA op profit | BCA margin | Total capex | Segment basis | CapIQ flag |
|---|---|---|---|---|---|---|
| 2004 | 19,925 | 745 | 3.7% | 1,246 |  | Reclassified |
| 2005 | 21,365 | 1,431 | 6.7% | 1,547 |  | Reclassified |
| 2006 | 28,465 | 2,733 | 9.6% | 1,681 |  |  |
| 2007 | 33,386 | 3,584 | 10.7% | 1,731 |  |  |
| 2008 | 28,263 | 1,186 | 4.2% | 1,674 |  |  |
| 2009 | 34,051 | -583 | -1.7% | 1,186 |  |  |

**2010-era reading.**
- The BCA margin peaked at 10.7% in 2007 [B-0063].
- It fell to 4.2% in 2008 (strike, 787 and 747-8) [B-0166] and to -1.7% in 2009 (787 test aircraft and 747 losses) [B-0243].
- Capex was cut in 2009 [B-0196].

## 3. Capital returned vs free cash flow, FY2004-FY2009 [FIN: 3d]

| FY | FCF | Buybacks | Dividends | Returned | Returned % FCF | Equity issued |
|---|---|---|---|---|---|---|
| 2004 | 2,480 | 752 | 648 | 1,400 | 56% |  |
| 2005 | 5,504 | 2,877 | 820 | 3,697 | 67% |  |
| 2006 | 6,043 | 1,698 | 956 | 2,654 | 44% |  |
| 2007 | 7,912 | 2,775 | 1,096 | 3,871 | 49% |  |
| 2008 | -2,041 | 2,937 | 1,192 | 4,129 | – |  |
| 2009 | 4,444 | 50 | 1,220 | 1,270 | 29% |  |

**2010-era reading.**
- Buybacks were the shock absorber: $2.9B in 2008 despite negative free cash flow [B-0149], then about $50M in 2009 [B-0257].
- No buybacks are expected "probably until 2011" [B-0232].
- Dividends kept rising [B-0200, B-0201].

## 4. BCA margin swings, 2004-2009 [FIN: 3a]

| From | Margin | To | Margin | Change (pp) | Years | Move |
|---|---|---|---|---|---|---|
| 2004 | 3.7% | 2007 | 10.7% | +7.0 | 3 | trough→peak |
| 2007 | 10.7% | 2009 | -1.7% | -12.4 | 2 | peak→trough |

## 5. Commercial Airplanes R&D, $M

| FY | BCA R&D | Source |
|---|---|---|
| 2008 | 2,838 | [tk2: FY2008] p848 |
| 2009 | 5,383 | [tk3: FY2009] p1726 |

## 6. Charges and reach-forward losses, $M

| Year | Item | Amount | Source |
|---|---|---|---|
| 2008 | 747 reach-forward loss | 685 | [tk2: FY2008] p851; [tk3: FY2009] p1729; [B-0143, B-0168] |
| 2009 | 787 flight-test aircraft moved to R&D | 2,693 | [tk3: FY2009] p1730; [B-0243, B-0236] |
| 2009 | 747 reach-forward loss | 1,352 | [tk3: FY2009] p1729; [B-0243] |

## 7. Balance sheet, liquidity and guidance, 2007-2010 (from the evidence)

| As of | Item | Value | Evidence |
|---|---|---|---|
| End 2007 | Cash | $12.1B | B-0065 |
| End 2007 | Pension funding | 110% of projected obligation | B-0064 |
| Jan 2008 | Dividend increase; new buyback authorisation | 14%; $7B | B-0061 |
| 2007 | BCA deliveries; BCA margin; BCA backlog | 441; 10.7%; $255B | B-0063 |
| Oct 2008 | Cash and marketable securities | over $7B | B-0115 |
| 2008 | Operating cash flow | -$401M | B-0175 |
| 2008 | Strike: lost deliveries; revenue lost | 104; about $6.4B | B-0159 |
| 2008 | Buybacks; acquisitions; Boeing Capital debt paid down | $2.9B; about $900M; about $700M | B-0149 |
| End 2008 | Total debt | $7,512M | B-0177 |
| End 2008 | Pension underfunding (GAAP); shareholders' equity | $8,420M; negative | B-0180, B-0179 |
| Jan 2009 | S&P rating | A+, outlook negative | B-0178 |
| Mar 2009 | New debt; cash after issue | $1.8B; $4.7B | B-0190 |
| Apr 2009 | Minimum operating cash | about $2B, plus a safety net | B-0195 |
| 2009 | New borrowings; total debt at year-end | $5,961M; $12,924M | B-0256 |
| 2009 | Operating cash flow | $5.6B | B-0223 |
| Nov 2009 | Company stock contributed to the pension | $1.5B | B-0229 |
| 2009 | Shares repurchased | 1.17M (2008: 42.1M) | B-0257 |
| 2009 | EPS; hit from 787 test aircraft; hit from 747 charges | $1.84; $2.38; $1.20 | B-0227 |
| 2009 | Total R&D (2008; 2007) | $6.5B ($3.8B; $3.9B) | B-0236 |
| Jan 2010 | 2011 R&D guidance | down by more than $500M, keeping a wedge for the 777 and 737 | B-0230 |
| Jul 2010 | 2011 operating cash flow guidance | above $5B | B-0272 |
| Oct 2010 | 737 backlog; planned rate | over 2,000; 38 a month from 2Q 2013 | B-0284 |

## 8. Scenario economics for scale ([rules], `hist-2010-neo`)

| Item | Value |
|---|---|
| Boeing WACC; alpha | 10.5%; 0.3 |
| b737next `reengine` | 6 years, $2.5B capex, margin 14% alone / 13% when both sides have new airplanes, tech-ready 2016 |
| b737next `cleansheet` | 9 years, $18.0B capex, margin 19% / 18%, tech-ready 2019, capture multiplier 1.3 |
| a320neo (Airbus) | 5 years, $1.8B capex, tech-ready 2015 |
| 737 Rate Increase | +1.5 pp narrowbody share after 2 years, $1.0B capex over 2 years, one use |
| Development strain | $3.0B at full overlap over 5 years; 787/747-8 development runs 2004-2012 |
