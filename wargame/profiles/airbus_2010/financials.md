# Airbus as of 30 November 2010: financials

## The headline: the evidence holds no Airbus financials for 2010

The evidence file (`evidence.jsonl`, 110 items) contains **no Airbus or EADS financial statement for 2010 or any other year**:
- no revenue, EBIT, margin, cash flow, net cash, R&D or capex;
- no backlog value;
- no program charge.

Every Airbus number below comes from Boeing's calls and 10-Ks, where Boeing executives or analysts describe Airbus. It is an outside view. Nothing here was computed or recalled from memory. Engine placeholders are marked as such and are not history.

## 1. Airbus numbers in the evidence (outside view)

| Item | Value | As of | Evidence |
|---|---|---|---|
| Deliveries supported by export-credit agencies | 45% in 2010 (expected), up from 35% in 2009 | Jul 2010 | A-0026 |
| Narrowbody production rate | "high 30s" a month, against Boeing's "low 30s" | Apr 2009 (describing the pre-downturn ramp) | A-0019, A-0020 |
| Narrowbody rate direction | heading for about 40 a month, against Boeing's 31 | Jan 2008 (analyst) | A-0009 |
| A350 XWB orders | about 250-300 | Jan 2008 (analyst) | A-0009 |
| A350 XWB first delivery | 2013 | Jan 2008 (analyst) | A-0009 |
| Productivity and overhead programme | runs through 2012 | Feb 2009 and Feb 2010 10-Ks | A-0018, A-0024 |
| 787 electrical wiring relative to the A380 | about one fifth (Boeing's claim) | Oct 2006 | A-0007 |

Qualitative financial behaviour with no numbers attached:
- **Launch aid:** the WTO ruled every challenged instance illegal in 2010 [A-0004, A-0006, A-0025].
- **Subsidy-backed risk-taking**, as Boeing argues it [A-0021, A-0022].
- **Pricing:** aggressive pricing of older products [A-0002, A-0003]; announced price increases not realised [A-0010].
- **Weak-dollar response:** cost cuts reinvested in products or price [A-0018, A-0024].

## 2. Engine placeholders for this scenario (not history)

These come from `python3 -m wargame.engine rules --scenario hist-2010-neo`. The engine calls them illustrative 2010-era placeholders.

| Parameter | Airbus | Boeing |
|---|---|---|
| WACC | 8% | 10.5% |
| Capex alpha loading | 0.3 | 0.3 |
| Incumbent narrowbody | A320ceo family, 9% margin | 737NG, 12% margin |
| Status-quo narrowbody share | 52% | 48% |
| New narrowbody program | A320neo: 5 years, $1.8B, 12% margin alone / 11% when both are in service | Re-engine: 6 years, $2.5B, 14% / 13%. Clean sheet: 9 years, $18B, 19% / 18%, capture x1.3 |
| Tech-ready year (early-EIS penalty 2 pp a year; 3 pp for the Boeing clean sheet) | 2015 | 2016 (Re-engine), 2019 (clean sheet) |
| Background widebody development | A350 XWB, 2006-2015 | 787 and 747-8, 2004-2012 |
| Strain from overlapping narrowbody and widebody development | $3.0B at 5 or more overlap years, pro rata below, alpha-loaded | same rule |
| Rate Increase | none | +1.5 pp narrowbody share after 2 years, $1.0B |

Engine terms (Airbus's choice):
- `cfm_leap`: +0 pp margin, capture x1.0.
- `pw_gtf`: +0.5 pp margin, capture x0.95.

Narrowbody market: 1,300 units a year at $45M net price, first-mover capture 2 pp a year up to a 65% cap.

## 3. Boeing numbers Airbus could see in 2010 (rival intel)

| Item | Value | Evidence |
|---|---|---|
| 737 rate plan | 35 a month from early 2012; then 38 a month from 2Q 2013 (the third increase of 2010), on a backlog of over 2,000 | B-0269, B-0284 |
| 787 rate plan | 10 a month by end-2013, 3 of them from Charleston (a 2009 plan had said 10 in 2012) | B-0263, B-0145 |
| 787 orders | 850 | B-0203 |
| 777 rate cut in the downturn | 7 to 5 a month from June 2010 | B-0187 |
| Deferrals absorbed in 1H 2009 | about 60 in 1Q and 70 in 2Q | B-0198 |
| 747 charges | $347M reach-forward loss; $362M tied to deferring a rate increase | B-0249, B-0247 |
| Vought 787 facilities acquired | $592M | B-0211 |
| 2008 buybacks, then cut to minimal | 42,073,885 shares at $69.79 | B-0176 |
| Typical launch threshold | about 100 orders | B-0193 |
| Re-engine threshold | only if a new airplane is 10-15 years away | B-0282 |
| New narrowbody timing | around 2020 | B-0285, B-0289 |
| 737NG fuel gains | 5% so far, 2% more coming | B-0286 |
| 20-year market | 29,000 airplanes, $3.2T; 5% traffic growth on 3% GDP | B-0244 |
| Customer financing lead time | 12-18 months | B-0154 |
| Industrial-participation commitments outstanding | $11B | B-0260 |

## 4. Unknown: what the evidence does not tell us

- **Airbus and EADS results for 2009-2010:**
  - revenue, EBIT, EBIT margin;
  - free cash flow, net cash, liquidity;
  - dividends.
- **Program economics:**
  - A320 family unit margin;
  - A380 unit losses and remaining charges;
  - A350 XWB budget, spend to date and any provision;
  - A400M provisions and the terms of its restructuring.
- **Development capacity:**
  - total R&D spend;
  - engineering headcount;
  - how much capacity the A350 leaves for a re-engine program.
- **Neo funding:**
  - development cost, and whether repayable launch aid or export credit would be sought after the 2010 WTO ruling;
  - engine-maker contributions.
- **Currency:** dollar exposure, the hedge book and its rates. (A-0018 and A-0024 show only that a weak dollar squeezes us.)
- **Commercial position:**
  - order intake, deliveries and backlog in units and value for 2009-2010;
  - the current A320 production rate and plan;
  - net pricing and discount levels.
- **Engine commercial terms** with CFM and Pratt & Whitney: exclusivity, pricing, risk-sharing.
- **Shareholders:** governance and state-shareholder constraints on EADS capital allocation.

Treat any rule that needs these numbers as resting on the engine's placeholders (section 2), not on history.
