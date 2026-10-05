# CFM/GE as a supplier player: reconciled calibration

Reconciled 2026-10-05 from two independent calibrations made to the same brief:
- **A**, bottom-up unit economics (shop visits, revenue per visit, margin, cash timing);
- **B**, top-down segment reconciliation (segment profit divided by the effective installed base, reconciled with GE's own statements).

The game master set the reconciled values in `wargame/config/default.json` under `suppliers.cfm` and `engine_options.nb.cfm_leap_plus`. This memo documents them; it does not change them. Cells are cited as `source:Sheet!REF`; GE executives' own words as [CX-nnnn] (`wargame/profiles/cfm/executives/evidence.jsonl`).

## 1. Basis

**What CFM/GE is in the game.**
- It is the third engine-maker player (`--suppliers cfm`), next to Rolls-Royce and Pratt & Whitney.
- It stands for two businesses:
  - CFM International, the 50/50 GE-Safran Joint Venture: LEAP-1A on the A320neo, LEAP-1B sole source on the 737 MAX, and the next narrowbody engine (ducted, or the RISE open fan);
  - GE's own GEnx on the 787.
- **Payoff.** Full-game delta PV against the status quo, at its own WACC:
  - the lifecycle value of the engines it delivers, booked per engine at delivery (OE margin plus PV of aftermarket profit);
  - less alpha-loaded engine capex and strain;
  - less lobbying costs, which are not alpha-loaded.
- **Levers.**
  - `ducted` and `open_fan` (no entry into service before 2045), standard or aggressive terms, cancel;
  - one-time `leap_upgrade`, `genx_upgrade`, `embraer_partner` and `lobby_emissions`.
- **Fallbacks.** An airframe that asks for a CFM engine CFM has not launched flies the LEAP derivative (`cfm_leap_plus`). A widebody falls back to the GEnx upgrade (`ge_genx_next`). The engine books a derivative at fit 1 and the incumbent value per engine, less `derivative_capex_b`.

**100% of CFM, not GE's half.**
- Both Safran models book Safran's half of LEAP (`gs_cfm:Aerospace Propulsion Division!AB57` = 0.5; `ms_cfm:Civil OE!AP120` = 0.5). Both calibrators doubled Safran's LEAP lines.
- Doubling assumes GE's half earns what Safran's does. GE does more of the shop work: in GS's model GE's shops take 30% of CFM aftermarket shop work and Safran's 10% (`gs_cfm:Aerospace Propulsion Division!AB149`, `!AB148`).
  - A cuts the aftermarket margin to allow for GE's labour-heavy share.
  - B checks the doubling against GE's Commercial Engines & Services (CES) profit and finds it conservative. GE's half in 2024 is 3,281 + 0 − 330 + 8 = $2.96B (`ms_cfm:Civil AM!BE44`, `!BE46`; `ms_cfm:Civil OE!Z31`, `!Z30`), about 48% of the $6.0-6.3B CES guide [CX-1292].

**The GE share for GEnx.**
- Safran holds a 7.5% revenue share (`ms_cfm:Civil OE!AP124`; `gs_cfm:Aerospace Propulsion Division!AB59`).
- The other risk-and-revenue-sharing partners are not in the evidence. A assumes 12.5% (GE share 0.80); B assumes 2.5% (0.90).
- The reconciled $5.0M equals both calibrators' programme values (A $5.7M, B about $5.8M) at a GE share of about 0.875.

**Currency and dollars.**
- **EUR/USD.**
  - A uses 1.155, Morgan Stanley's 2026 rate (`ms_cfm:Propulsion!BD114` = 1.1546).
  - B uses 1.1426, Goldman Sachs's 2026E rate (`gs_cfm:Aerospace Propulsion Division!AB52` = 1.1426415).
  - The 1% gap touches only the R&D and capex lines; nearly all unit-economics cells are already in USD. No reconciled value depends on the choice.
- **Constant 2026 $, pre-tax.**
  - A deflates nominal model values at 2.5% a year and inflates historical euros at 2% a year before converting.
  - B lifts 2011-17 euros by ×1.30 to 2026 dollars.
- PV to 2026 at the 8% WACC, over 2026-2060.

**Scale.**
- The game's status-quo CFM flow is 2,000 × 0.4 × 2 × 1.0 + 2,000 × 0.6 × 2 × 0.6 = 3,040 narrowbody engines a year, plus 170 × 0.588 × 2 × 0.78 = 156 GEnx.
- Real LEAP output in 2030 is 2,384 (`ms_cfm:Civil OE!BV50`), so the game runs at about 1.28× real.
- Per-engine values are realistic and not scaled down to compensate.

**Safran's share (context only; the game does not model it).**

| Item | CFM/GE in the game | Safran share |
|---|---|---|
| LEAP value per engine | $3.0M | 50% = $1.5M |
| Ducted / open-fan value per engine | $3.4M / $3.9M | $1.7M / $1.95M |
| Ducted / open-fan capex | $7.0B / $10.0B | $3.5B / $5.0B |
| GEnx | GE share ≈ 0.875 of the programme | 7.5% revenue share |
| WACC | 8% | 7.33% / 7.46% (GS, `gs_cfm:DCF Valuation!D32`, `gs_saf:DCF Valuation!D32`) |

## 2. Parameter table

Value is the reconciled value in the config; A and B are the calibrators' values. The range column gives the span between the two calibrators, with the outer range of their sensitivities in brackets.

| Parameter | Value | A | B | Range | Status | Key evidence |
|---|---|---|---|---|---|---|
| `wacc` | **0.08** | 0.08 | 0.08 | 0.07-0.09 | CALIBRATED | Safran 7.325% / 7.46% (`gs_cfm:DCF Valuation!D32`, `gs_saf:DCF Valuation!D32`; same values at `!D13`); Rf / ERP (`gs_cfm:DCF Valuation!D19`, `!D20`); GE's WACC as a test [CX-0015] |
| `alpha` | **0.45** | 0.60 | 0.30 | 0.30-0.60 (0.19-0.94) | PLACEHOLDER | GE's 15% is an M&A test [CX-0015], [CX-0066]; [CX-0310], [CX-0460]; [CX-0557]; [CX-0645], [CX-0922] |
| `incumbent_fit.boeing.nb` | **1.0** | 1.0 | 1.0 | – | CALIBRATED | Sole source on the MAX [CX-0182], [CX-1098]; `ms_cfm:Civil OE!AP194` = 1 |
| `incumbent_fit.airbus.nb` | **0.60** | 0.60 | 0.60 | 0.55-0.65 | CALIBRATED | 60% life of programme [CX-0182], [CX-1300]; 55-60% of deliveries [CX-0906]; >70% of wins since 2023 [CX-0218]; `gs_cfm:Aerospace Propulsion Division!AB34` 0.54 → `!AF34` 0.62; `gs_saf:Aerospace Propulsion Division!AF34` 0.59; `ms_cfm:Civil OE!AP184` 0.55 |
| `incumbent_fit.boeing.wb` | **0.78** | 0.78 | 0.78 | 0.70-0.80 | CALIBRATED, **flagged** | 70% life-of-programme 787 win rate [CX-0615]; "Genx 60% mkt share on 787 platform, as of April 2022" (`gs_cfm:Aerospace Propulsion Division!AH29`); 1 − Rolls-Royce's 0.22 |
| `incumbent_fit.airbus.wb` | **0** | 0 | 0 | – | CALIBRATED | No GE engine on the A350 or A330neo |
| `incumbent_value_m_per_engine.nb` (LEAP) | **3.0** | 2.6 | 3.3 | 2.6-3.3 (1.9-4.1) | CALIBRATED | §3.4; `ms_cfm:Civil AM!BU135`..`!BU137`, `!BU7`, `!BU44`, `!DA9`; `gs_cfm:Aerospace Propulsion Division!AB38`, `!AB37`; [CX-1298], [CX-0422] |
| `incumbent_value_m_per_engine.wb` (GEnx) | **5.0** | 4.5 | 5.2 | 4.5-5.2 (3.5-6.2) | CALIBRATED (GE share PLACEHOLDER) | §3.5; `ms_cfm:Civil AM!BU48`, `!BU173`, `!BU174`; `ms_cfm:Civil OE!AP113`, `!AP124`; [CX-0951], [CX-0903] |
| `ducted.dev_years` | **7** | 7 | 6 | 6-8 | CALIBRATED | LEAP R&D hump 2011-17 (`ms_cfm:Propulsion!K46`..`!Q46`); [CX-0189], [CX-0147] |
| `ducted.capex_b` | **7.0** | 7.0 | 7.0 | 5.5-9.0 | CALIBRATED | `ms_cfm:Propulsion!K46`..`!Q46`, `!D46`..`!J46`, `!M34`..`!Q34`; [CX-1114] |
| `ducted.value_m_per_engine` | **3.4** | 3.1 | 3.5 | 3.1-3.5 (2.4-4.3) | CALIBRATED | LEAP × 1.125; [CX-0930], [CX-0215], [CX-0183] |
| `open_fan.dev_years` | **9** | 9 | 8 | 8-11 | PLACEHOLDER (the 2045 floor binds) | [CX-0147], [CX-0151], [CX-0211], [CX-0189], [CX-0608], [CX-0152] |
| `open_fan.capex_b` | **10.0** | 10.0 | 9.5 | 7.5-13 | PLACEHOLDER | No RISE cost disclosed; [CX-0181], [CX-0222] |
| `open_fan.value_m_per_engine` | **3.9** | 3.5 | 4.3 | 3.5-4.3 (2.6-5.5) | PLACEHOLDER | ≥20% fuel burn [CX-0217]; [CX-0181] |
| `ramp` | **start_frac −0.30, 10 years** | −0.20, 10 | −0.35, 10 | −0.35 to −0.20 (−0.56 to −0.10); 8-12 years | CALIBRATED | LEAP vintages (`ms_cfm:Civil OE!D129`, `!G129`, `!J129`, `!AP129`, `!BV129`); [CX-0194], [CX-0911], [CX-0956] |
| `terms.aggressive` | **+1.4pp, value_mult 0.88** | +1.1, 0.90 | +1.8, 0.86 | 1.1-1.8 (0.9-3.0); 0.86-0.90 (0.75-0.92) | CALIBRATED | `ms_cfm:Civil OE!B99`, `!E99`, `!F99`, `!J99`, `!Z99`; `gs_cfm:Aerospace Propulsion Division!Y44`, `!AB44`; [CX-1116], [CX-0930], [CX-0207] |
| `leap_upgrade` | **+5pp from Pratt & Whitney, lag 3, $0.75B over 3 years, $0.42B a year for 10 years** | 5, 3, 1.0, 0.40 | 5, 3, 0.5, 0.45 | fit 3-10; capex 0.5-1.5; saving 0.2-0.8 | CALIBRATED (capex low confidence) | [CX-0218], [CX-0209], [CX-0225], [CX-0649]; `gs_cfm:Aerospace Propulsion Division!AF185`, `!AF190`, `!AF199`, `!AF228`, `!AF233`; `ms_cfm:Civil AM!CK9` |
| `genx_upgrade` | **+5pp from Rolls-Royce, lag 3, $0.45B over 3 years, $0.12B a year for 12 years** | 5, 3, 0.5, 0.15 | 5, 3, 0.4, 0.10 | fit 3-8; capex 0.3-0.8; saving 0.05-0.3 | PLACEHOLDER | [CX-0615], [CX-1299], [CX-0951], [CX-1092] |
| `embraer_partner` | **190 engines a year from lag 8, $1.2M each, $1.2B over 4 years** | 200, $1.0M, $1.5B / 5 yr | 180, $1.4M, $1.0B / 3 yr | 120-300; $0.6-1.4M; $0.8-3.0B | PLACEHOLDER | No Embraer evidence; [CX-0587], [CX-0171], [CX-1114] |
| `lobby_emissions` | **$0.15B over 3 years, lag 3; +0.5pp margin, capture ×1.05 on open-fan airframes** | lag 2 | lag 3 | cost 0.05-0.4; +0.2 to +1.0pp; ×1.0-1.1 | PLACEHOLDER | [CX-1014], [CX-1016], [CX-0217], [CX-0856] |
| `strain` | **full_overlap_b 1.75, norm_years 5** | 1.5 | 2.0 | 1.0-3.0 | PLACEHOLDER | [CX-1018], [CX-1021], [CX-1131], [CX-1135], [CX-1293], [CX-1255] |
| `cfm_leap_plus` vs `cfm_ducted` | **margin −1.0pp, eis_add 0, capture 0.92** | −1.0, 0, 0.95 | −1.0, 0, 0.90 | −0.5 to −2.0; 0; 0.85-0.95 | margin and eis CALIBRATED; capture PLACEHOLDER | [CX-1126], [CX-0183], [CX-0162], [CX-1114], [CX-0217] |
| `derivative_capex_b` | **nb $1.0B, wb $0.5B** | – | ≈$1B (note) | nb 0.7-1.5; wb 0.3-0.8 | PLACEHOLDER (new) | [CX-1114]; the `leap_upgrade` and `genx_upgrade` capex |

## 3. Derivations

### 3.1 WACC: 0.08

- **A.**
  - Safran's WACC is 7.325% (`gs_cfm:DCF Valuation!D32`) or 7.46% (`gs_saf:DCF Valuation!D32`).
  - GE has no cell. On GS's own inputs (Rf 3.5% `gs_cfm:DCF Valuation!D19`, ERP 4.5% `!D20`) and an assumed beta of 1.1-1.2, GE's WACC is 8.5-8.9%.
  - Weighted by who owns the value (GE holds about 54% of status-quo value: half of LEAP plus the GEnx): 0.54 × 8.75% + 0.46 × 7.4% = 8.1%.
- **B.** The same Safran cells, a US large-cap WACC of 8.5-9% for GE (which uses its WACC as a test [CX-0015]), and a JV blend of about 8%.
- **Reconciled 0.08.** The two agree. GE's WACC is estimated, not cell-sourced.

### 3.2 Alpha: 0.45 (PLACEHOLDER)

- **A: 0.60, from a 13% hurdle.**
  - GE underwrites at "15% or better" [CX-0015], [CX-0066]. No Safran hurdle is in the evidence; A assumes about WACC + 4pp (11.5%). JV hurdle: (15 + 11.5) / 2 ≈ 13%.
  - Mapping convention: the one that reproduces Rolls-Royce's calibrated pair (10% WACC, 15% hurdle, alpha 0.6). That implies an effective capex-to-value lag of n = ln 1.6 / ln(1.15/1.10) = 10.57 years.
  - (1.13/1.08)^10.57 − 1 = 0.61 → 0.60.
- **B: 0.30, from a 9.5% hurdle.**
  - Take a programme that earns exactly the hurdle h, with 6 development years, the ramp and 30 years of deliveries. Then (1 + α) = PV at 8% of benefits / PV at 8% of capex:

    | Hurdle | 9.0% | 9.5% | 10% | 11% | 15% |
    |---|---|---|---|---|---|
    | Alpha | 0.19 | **0.30** | 0.42 | 0.69 | >1.2 |

  - The hurdle is set about 1.5pp above WACC. The 15% test is old GE's M&A rule. Culp states only a 12-24 month payback on restructuring [CX-0310] and "high single-digit" returns on bolt-ons [CX-0460].
- **Why they differ.** The hurdles differ (13% against 9.5%), and so do the mappings: near 11%, B's formula adds about 0.27 of alpha per point of hurdle, A's convention about 0.13. The two partly offset.
  - Under A's convention, B's 0.30 is a 10.7% hurdle.
  - Under B's formula, A's 0.60 is also about 10.7%.
  - On one convention the gap would be wider: B's 9.5% is 0.16 under A's convention, and A's 13% is well above 1.2 under B's formula.
- **Reconciled 0.45**, the midpoint. A's convention reads it as an 11.9% hurdle and B's formula as 10.1%, so about 11%.
- **Status.** PLACEHOLDER: neither partner discloses a programme hurdle. §5 shows it barely moves CFM/GE's choices.

### 3.3 Incumbent fits

- **Boeing narrowbody 1.0.** LEAP-1B is sole source on the MAX [CX-0182], [CX-1098]; MS share 1 (`ms_cfm:Civil OE!AP194`).
- **Airbus narrowbody 0.60: confirmed by both.**
  - Delivered share:
    - 0.56 in 2022 and 0.50 in 2023 (`ms_cfm:Civil OE!J184` = 0.5601, `!R184` = 0.5026); MS holds 0.55 flat (`!AP184`);
    - GS has 0.54 in 2026E rising to 0.62 in 2030E (`gs_cfm:Aerospace Propulsion Division!AB34`, `!AF34`); GS's November model has 0.59 (`gs_saf:Aerospace Propulsion Division!AF34`).
  - GE's own measures:
    - a 60% life-of-programme win rate [CX-0182], [CX-1300];
    - 55-60% of Airbus deliveries [CX-0906];
    - more than 70% of A320 decisions since 2023 [CX-0218].
  - The PV-weighted 2026-60 share is about 0.60 = 1 − Pratt & Whitney's 0.40. Upside beyond 0.60 sits in `leap_upgrade`.
- **Boeing widebody 0.78: confirmed by both and flagged by both** (§4.1).
- **Airbus widebody 0.** GE has no engine on the A350 or A330neo.

### 3.4 LEAP incumbent value: $3.0M per engine

**A: $2.6M (bottom-up).**
- **OE.** CFM OE revenue per installed engine in 2026 is 2 × 4,762 (`ms_cfm:Civil OE!AP12`) / (1,959 − 110.6 − 81.1 spares) = $5.39M (`!AP50`, `!AP182`, `!AP192`).
  - Margins: −2.5% in 2026 (`!AP129`), 0 in 2027 (`!AX129`), +3% in 2030 (`!BV129`), and an assumed 5% at maturity.
  - Value per installed engine: −$0.14M, 0, +$0.17M and +$0.27M.
- **Lifetime aftermarket revenue: $13.5M (range 11-16).** Three estimates:
  - shop visits: 2 × (3.425 + 2.398 + 1.713) = $15.1M (`ms_cfm:Civil AM!BU135`..`!BU137`, three visits a life [CX-0422]);
  - services at 3.5× the engine sale [CX-1298]: $12.3M in 2026 $;
  - CFM56 fleet: 2 × 6,229 (`!BU7`) / 25,490 installed (`!BU82`) × 25 years = $12.2M.
- **Margin and timing.** Margin 0.42 at maturity (0.38 for the 2026 cohort), after the GE haircut. PV factor 0.44 at 8%, with rate-per-flight-hour cash timing.
- **Result.** Mature aftermarket PV = 0.44 × 0.42 × 13.5 = $2.50M.
  - Cohort values: $2.15M (2026), $2.66M (2030), $2.77M (mature).
  - PV-weighted over 2026-60: $2.63M → **2.6**.

**B: $3.3M (top-down).**
- **The flow identity.** L = P(t) / N_eff(t): segment aftermarket profit divided by the age-weighted installed base.
  - CFM56 benchmark: L = 2 × 4,049 (`ms_cfm:Civil AM!BU44`) / 1,018 = $7.95M of lifetime profit.
  - Lifetime revenue: 2 × 6,229 / 1,018 = $12.2M.
- **Lifetime LEAP aftermarket revenue: $18.5M.** Three estimates:
  - the CFM56's 12.2 × the list-price ratio 16.56 / 11.04 = 1.50 (`gs_cfm:Aerospace Propulsion Division!AB38`, `!AB37`) = $18.3M;
  - 3.5× [CX-1298] applied to realised prices of $4.36-6.29M: $15.3-22.0M;
  - a 2030 cohort check, 2 × 6,349 (`ms_cfm:Civil AM!DA9`) / N_eff 646: $19.7M.
- **Margin and timing.** Mature margin 45%. PV factor 0.401, with shop-visit peaks at 8.5, 15 and 21 years. A 6% haircut for sustaining R&D: half of Safran's R&D ratio, 529.8 / 4,127 = 12.8% (`ms_cfm:Propulsion!BD21` = −529.8, `!BD108` = 4,127).
- **Result.** 18.5 × 0.45 × 0.401 × 0.94 = $3.14M, plus OE of 3% × $5.3M = $0.16M → **3.3**.

**Why they differ.** Almost entirely lifetime aftermarket revenue.
- A's $13.5M is about the CFM56's; B's $18.5M scales the CFM56 by LEAP's higher list price.
- Margin (0.42 against 0.45) and timing (0.44 against 0.401 × 0.94 = 0.377) roughly offset: A gives 13.5 × 0.42 × 0.44 = 2.49; B gives 18.5 × 0.45 × 0.377 = 3.14.

**Reconciled $3.0M** (midpoint 2.95). It implies lifetime aftermarket revenue of about $15-16.5M per LEAP (1.25-1.35× the CFM56) at either calibrator's margin and timing.

**Cross-checks.**
- **A.** $2.6M × 2,100-2,400 installed LEAPs a year = $5.5-6B a year. CFM-level LEAP profit in 2030 is 2 × (2,540 + 200) = $5.5B (`ms_cfm:Civil AM!DA46`, `ms_cfm:Civil OE!BV31`).
- **B.**
  - Its parameters imply LEAP aftermarket profit of $4.8B in 2030, against MS × 2 = $5.1B.
  - GE's claim of profit parity with the CFM56 by about 2030 [CX-0212], [CX-0971] would give about 3.7, and MS's 2030 path about 3.1.

### 3.5 GEnx incumbent value: $5.0M per engine (GE share)

**A: $4.5M.**
- **OE.**
  - Realised price $11.93M: the mean of MS's $11.27M (`ms_cfm:Civil OE!AP113`) and GS's $33.12M × (1 − 0.62) = $12.59M (`gs_cfm:Aerospace Propulsion Division!AB40`, `!AB44`).
  - Spares add 7% at 70% of the $22.55M list (`ms_cfm:Civil OE!AP68`, `!AP85`), giving $13.04M per installed engine.
  - An assumed 5% mature margin gives +$0.65M. MS books 0% on Safran's widebody share (`!AP131`); GEnx margins rose 4× in 10 years [CX-0903].
- **Aftermarket.**
  - Lifetime revenue $35M: the 3.5× rule gives $30.3M in 2026 $; a shop-visit build from GE90's $22.9M per visit (5.429 / 0.237, `ms_cfm:Civil AM!BU173`, `!BU174`), × 0.6, gives about $48M.
  - Margin 0.35, below Safran's 45% on the GE90 (`!BU49`) because over 60% of GEnx is on long-term service agreements [CX-0951].
  - PV $5.05M.
- **Result.** Programme value $5.70M × GE share 0.80 = $4.56M → **4.5**.

**B: $5.2M.**
- **The GE90 analogue.**
  - Programme aftermarket profit = 377.2 / 0.237 = $1.59B (`ms_cfm:Civil AM!BU48`, `!BU174`). This matches 652 shop visits × $5.43M × 45% (`!BU171`, `!BU173`, `!BU49`).
  - N_eff = 135, with pre-2014 deliveries assumed, so L = $11.8M.
- **GEnx lifetime profit: $10.7-15.8M.**
  - 0.9 × the GE90, by list price 22.55 against 24.38 (`ms_cfm:Civil OE!AP85`, `!AP82`);
  - or 3.5× × $11.27M × 40%.
- **Result.** PV factor 0.425 × GE share 0.9 × 0.94 gives $3.8-5.7M; adding OE of $0.51M gives $4.3-6.2M; midpoint **5.2**.

**Reconciled $5.0M.**
- It lies between the two, and equals both programme values at a GE share of about 0.875: A 5.70 × 0.875 = 4.99; B about 5.05.
- Direction: GEnx wins came "not because of price" [CX-0599], and time on wing raises long-term-agreement profit [CX-0951].

### 3.6 New programmes

**Ducted: 7 years, $7.0B, $3.4M per engine (CALIBRATED).**
- **Capex (both partners): both calibrators reach $7.0B, by different routes.**
  - **A.**
    - Safran's self-financed R&D excess over a linear 2010-18 baseline, 2011-17 (`ms_cfm:Propulsion!K46`..`!Q46`; €331M in 2010 `!J46`, €894M peak `!N46`, €537M in 2018 `!S46`): 63 + 266 + 381 + 460 + 415 + 290 + 237 = €2,112M → $3.08B in 2026 $.
    - Less about 15% for Silvercrest = $2.62B; × 2 partners = $5.2B.
    - Industrialisation: capex above 2.2% of revenue over 2013-19 is €1,144M → $1.61B; × 2 = $3.2B, of which half is programme-specific = $1.6B.
    - LEAP analogue $6.8B, which covered three variants; a second application costs about 30% less engineering [CX-1114]. **$7.0B.**
  - **B.**
    - 2011-17 R&D of €5,150M less the 2004-10 run rate (`ms_cfm:Propulsion!D46`..`!J46`, mean 341.6 × 7 = €2,391M) = €2,759M.
    - × 75% LEAP × 1.1426 × 1.30 = $3.07B; × 2 = $6.1B.
    - Industrialisation: 2013-17 capex of €1,850M (`!M34`..`!Q34`) against about €120M a year in 2009-11 (`!I34`..`!K34`). The excess of €1,252M × 60% × 1.1426 × 1.3 × 2 = $2.2B; a successor adds about 40% of that, $0.9B. **$7.0B.**
  - The models' 2026-30 R&D is a flat 4.5% of sales (`ms_cfm:Propulsion!AV47`). It embeds no launch, so a launch is incremental (A).
- **Development years.**
  - A: 7, the length of the LEAP R&D hump (2011-17).
  - B: 6, since RISE technology is already maturing [CX-0147], [CX-0216] and the next CFM engine is "available by the middle of the next decade" [CX-0189].
  - **Reconciled 7.** It is the observed analogue, and it equals fps's and NGSA's 7 development years, so a ducted engine launched with its airframe is ready on time.
- **Value per engine.**
  - A: $3.1M = OE 5% × $5.4M × 1.10 plus aftermarket PV 0.44 × 0.45 × 14.5, i.e. 0.30 + 2.85. Post-launch pricing lifts the aftermarket margin to 0.45 [CX-0930], [CX-0215].
  - B: $3.5M = LEAP × 1.06, for more content and pricing "for the risks we take" [CX-0930], [CX-0188], limited because ducted gets less than half the open fan's fuel gain [CX-0183].
  - The calibrators' ratios to their own LEAP values are 1.19 and 1.06. Their mean (1.125) × the reconciled $3.0M = $3.38M → **3.4**.

**Open fan: 9 years, $10.0B, $3.9M per engine (PLACEHOLDER).**
- **Development years.**
  - A: 9. RISE has been a technology programme since 2021 [CX-0147]. The fly demo slipped from "the middle of this decade" [CX-0151] to "this decade" [CX-0211]. The product is "available by the middle of the next decade" [CX-0189], [CX-0608], and Safran says "by 2035" [CX-0152].
  - B: 8.
  - **Reconciled 9.** The game's 2045 floor binds anyway: any launch up to 2036 is ready in time.
- **Capex.**
  - A: $10.0B = ducted × 1.4 (judgement), for a new architecture: open rotor, pitch change, an Avio gearbox and LPT [CX-0181], and a dust-tested compact core [CX-0222].
  - B: $9.5B = 6.1 × 1.35 + about $1.3B of gearbox and blade lines.
  - **Reconciled $10.0B.** No RISE budget is disclosed.
- **Value per engine.**
  - A: $3.5M (OE price × 1.3, aftermarket content × 1.2).
  - B: $4.3M, about 1.3× LEAP for the ≥20% fuel-burn step [CX-0217] and the gearbox content.
  - **Reconciled $3.9M**, the midpoint: 1.3× LEAP and 1.15× ducted.

### 3.7 Ramp: start_frac −0.30, 10 years

- **A: −0.20.**
  - LEAP cohort values as a fraction of the mature $2.77M:

    | Cohort | 2016 | 2018 | 2023 | 2026 | 2030 |
    |---|---|---|---|---|---|
    | Fraction of mature | −0.19 | −0.05 | 0.65 | 0.78 | 0.96 |
    | OE margin cell | −60% (`ms_cfm:Civil OE!D129`) | −40% (`!F129`) | −5% (`!R129`) | | |

  - A linear −0.20 → 1 over 10 years fits within about ±0.2.
  - GE's milestones are aftermarket profit in year 8, the programme in year 9 and OE in year 10 [CX-0194], [CX-0956].
- **B: −0.35.**
  - Vintage values come from the MS OE path (`ms_cfm:Civil OE!D129`, `!G129`, `!J129`, `!AP129`, `!BV129`) and the MS aftermarket margins (`ms_cfm:Civil AM!BM47`, `!BU47`, `!DA47`):

    | Vintage | 2016 | 2019 | 2022 | 2024 | 2026 |
    |---|---|---|---|---|---|
    | Fraction of mature | −0.60 | −0.02 | 0.47 | 0.77 | 0.89 |

  - The least-squares fit is −0.56 over 9 years. Stripping out launch pricing (the MS discount from list falls from 80% to 70%, `ms_cfm:Civil OE!E99`, `!Z99`) gives −0.11 over 10 years.
  - B takes the midpoint, because the terms lever prices concessions separately. Milestones [CX-0194], [CX-0911].
- **Reconciled −0.30 over 10 years** (midpoint −0.275, rounded).
  - A new CFM engine first books −0.3 × 3.4 = −$1.0M per engine. It passes LEAP's $3.0M only after about 9 years. That is the cannibalisation CFM bore in 2016-24: CFM-level LEAP OE loss in 2019 was 2 × −1,297 = −$2.6B (`ms_cfm:Civil OE!G31`).
  - Durability testing on RISE from day one [CX-0222], [CX-0223] argues against anything worse.

### 3.8 Aggressive terms: +1.4pp airframer margin, value_mult 0.88

- **A: +1.1pp, 0.90.**
  - The MS LEAP discount from list:

    | Years | 2014-17 | 2018-21 | 2022-23 | 2024 on |
    |---|---|---|---|---|
    | Discount | 0.80 | 0.75 | 0.725 | 0.70 |
    | Cells | `ms_cfm:Civil OE!B99`, `!E99` | `!F99` | `!J99` | `!Z99`, `!AP99` |

  - The extra launch discount averages 3.2% of list, $0.47M per engine. Spread over the programme's in-game life, that is $0.30M.
  - Airframer gain: 2 × 0.30 / 55 = 1.09pp. Value kept: 1 − 0.30 / 3.1 = 0.90.
  - Evidence: "the second tranche of customers ... we aren't in those big launch concessions" [CX-1116].
- **B: +1.8pp, 0.86.**
  - The GS discount falls from 65% (2023, `gs_cfm:Aerospace Propulsion Division!Y44`) to 62% (2026, `!AB44`): 3pp × $16.56M = $0.50M per engine. MS's launch-era gap of $1.45M is the upper bound.
  - Airframer gain: 0.5 × 2 / 55 = 1.8pp. Value kept: 1 − 0.5 / 3.5 = 0.86.
  - Evidence: launch-style pricing is "behind us" [CX-0930]; early-life risk is taken under service contracts, priced to win share [CX-0207].
- **Reconciled: the midpoints.**
  - They are consistent as a transfer: (1 − 0.88) × $3.4M = $0.41M per engine; × 2 / $55M = 1.48pp ≈ 1.4pp.
  - The engine confirms it. NGSA on the ducted engine with aggressive rather than standard terms moves Airbus by +$7.3B and CFM by −$7.7B (§5).

### 3.9 Upgrades

**`leap_upgrade` (CALIBRATED): +5pp of A320neo deliveries from Pratt & Whitney, lag 3, $0.75B over 3 years, $0.42B a year for 10 years.**
- **Fit and lag (agreed).**
  - The -1A kit was certified in December 2024 [CX-0225] and is in all -1A deliveries and shop visits [CX-0209]; the -1B kit is due in 1H26 [CX-0656].
  - The win rate is above 70% on recent A320 decisions, against 55-60% over the programme's life [CX-0218].
  - Retrofit comes at natural shop visits, "years, not months" [CX-0649]. Orders take 3-5 years to reach deliveries, and LEAP is sold out to about 2030 [CX-0221].
- **Capex.**
  - A: $1.0B. Safran's R&D rose €187M from 2022 to 2024 (`ms_cfm:Propulsion!X46` = 457 → `!AN46` = 644), partly for LEAP durability [CX-0918]; about a third is LEAP, and GE owns the HPT.
  - B: $0.5B. No cost is disclosed, and the -1A kit is already certified.
  - **Reconciled $0.75B**, the midpoint.
- **Saving.**
  - **A: $0.40B.**
    - 2030 shop-visit cost pool: 1,521 heavy visits × $3.80M + 1,919 quick-turns × $1.27M = $8.2B (`gs_cfm:Aerospace Propulsion Division!AF185`, `!AF190`, `!AF228`, `!AF233`).
    - +25% time on wing → 20% fewer visits = $1.64B. On the 79.2% under rate per flight hour (`!AF199`) that is $1.30B, less $0.23B of lost time-and-materials profit = $1.07B.
    - × 0.7 phase-in × 0.5 pass-through = $0.38B.
  - **B: $0.45B.** 2028 CFM-level LEAP aftermarket revenue of 2 × 4,489 = $9.0B (`ms_cfm:Civil AM!CK9`) × 5pp of margin from fewer visits under service contracts:
    - about 60% of the fleet is under contract, moving toward half [CX-0708], [CX-1286];
    - fewer visits mean more profit [CX-0951].
  - **Reconciled $0.42B.** Ten years matches 10-15-year contracts [CX-0376].

**`genx_upgrade` (PLACEHOLDER): +5pp of 787 deliveries from Rolls-Royce, lag 3, $0.45B over 3 years, $0.12B a year for 12 years.**
- **Fit.** The 787 was won on time on wing, not price [CX-1299], [CX-0615], [CX-0599]. +5pp is agreed.
- **Capex.** A $0.5B, B $0.4B → $0.45B.
- **Saving.**
  - A: about 2,500 engines (assumption), one visit every 5 years, 15% fewer visits = 75 avoided visits × about $10M × 60% under service agreements [CX-0951] × 0.5 pass-through × 0.8 GE share. **A states $0.15B, but its chain multiplies to $0.18B.**
  - B: GE90-like aftermarket of about $3.5B a year × over 60% under agreements × about 5% avoided = $0.10B. Upgrades are absorbed inside the agreements [CX-1092].
  - **Reconciled $0.12B**, the midpoint of the stated values. On A's corrected chain it would be $0.14B, about $0.1B of PV: immaterial within the placeholder range.

### 3.10 Embraer partnership (PLACEHOLDER): 190 engines a year from lag 8, $1.2M each, $1.2B over 4 years

- **A: 200 engines a year from 2034, $1.0M each, $1.5B over 5 years.**
  - Volume: about 100 aircraft a year (assumption).
  - Value: about 0.38× LEAP. An E2-class engine sells at about 0.6× LEAP's price, with about 0.6× the aftermarket content, and entering a Pratt & Whitney-held segment needs concessions.
  - Cost: a scaled derivative of the new core, at 20-30% of a new programme [CX-1114].
- **B: 180 engines a year from 2034, $1.4M each, $1.0B over 3 years.**
  - Volume: about 85 aircraft × 2 plus spares.
  - Value: about 0.42× LEAP for a 20-30k lbf engine. Safran's low-thrust OE margin is 2% (`ms_cfm:Civil OE!AP130`).
  - Cost: adapting a LEAP or RISE core.
- **Reconciled: the midpoints**, with lag 8 (both: about 1 year to launch plus 7 of development).
- **Rationale.** GE wants to be on every important platform [CX-0587], [CX-0171]. No evidence item gives Embraer volumes, pricing or cost.

### 3.11 Lobbying on emissions (PLACEHOLDER): $0.15B over 3 years, lag 3, +0.5pp and ×1.05 on open-fan airframes

- **Agreed by both:** the cost per round, +0.5pp of airframer margin and ×1.05 capture.
- **The margin.**
  - A: 1% of fuel on GE's fleet is worth $2-3B a year to customers [CX-1014], about $60k per narrowbody per point per year. The open fan beats ducted by about 10 points [CX-0217], [CX-0183].
    - A policy that raises the effective fuel or carbon cost by 10% is worth $60k per aircraft a year, or $0.59M of PV over 20 years at 8%.
    - Half captured in price: $0.3M on a $55M aircraft = +0.5pp.
  - B: the game's 1.5pp open-fan premium, scaled for a tighter carbon cost. Fuel is about 20% of airline cost [CX-0856].
- **The capture.** Mandates tilt airline choice mildly. Government co-funding has precedent: governments funded half of GE's ATP [CX-1016], and RISE has EU funding [CX-0181].
- **The lag.** A 2 years (to legislate), B 3 (the CO2-rule cycle). **Reconciled 3.**

### 3.12 Strain (PLACEHOLDER): 1.75 over 5 years

- **A: 1.5**, about 20% of the smaller programme's capex (ducted, $7B).
  - GE ran GEnx, LEAP and GE9X development concurrently [CX-1018].
  - It admits GEnx went poorly and applied the lessons to LEAP [CX-1021].
- **B: 2.0.**
  - Arithmetic: 1.5 scaled by CFM's $16.5B of two-programme capex against about $10.5B for each rival (× 1.57), × 0.8 because two parents share the engineering bench = 1.9 → 2.0.
  - Precedent: GE9X slipped from 2020 to 2021 to 2025/26 [CX-1131], [CX-1135], [CX-1293], and LEAP OE breakeven from 2021 to 2026 [CX-0135], [CX-0194].
  - The 6-8% R&D guardrail caps parallel spending [CX-1255].
- **Reconciled 1.75**, the midpoint: 25% of ducted capex.
- **How the engine applies it.** Any two overlapping developments strain, including upgrade and partner windows. Launching both upgrades in one turn therefore costs about $1.4B of PV (§5).

### 3.13 LEAP derivative (`cfm_leap_plus`) and derivative capex

- **margin_pp −1.0 (agreed).**
  - The game prices the open fan's ~10 extra fuel-burn points at +1.5pp, i.e. 0.15pp per point.
  - A LEAP derivative with RISE technology inserted [CX-0162] gains 3-5%, against about 8-10% for the ducted engine [CX-0183]. Joyce called the NMA engine "a half generation" [CX-1126].
  - Five points short = −0.75pp. A rounds to −1.0 for weaker differentiation; B adds −0.25pp because the airframe misses the ≥20% bar [CX-0217].
- **eis_add 0 (agreed).** A derivative needs about 30% less engineering [CX-1114] and is never on a 7-year airframe's critical path.
- **capture_mult 0.92 (PLACEHOLDER).** A has 0.95 (the fuel-burn deficit is partly offset by mature durability); B has 0.90 (less efficient, but proven). Midpoint 0.925.
- **derivative_capex_b: nb $1.0B, wb $0.5B (new, PLACEHOLDER).**
  - B noted that the engine booked a derivative at the full LEAP value with no capex, while a real derivative costs about $1B for both partners.
  - Cross-checks for $1.0B: it is about 15% of a new ducted programme ($7.0B × 0.15 = $1.05B), and above a durability kit ($0.75B).
  - The widebody $0.5B (the GEnx upgrade as an airframe's engine) mirrors the `genx_upgrade` capex.
  - Both are spread over the airframe's development years and alpha-loaded.

## 4. Disagreements and flags

### 4.1 Boeing widebody fit 0.78 against GE's 70% and GS's 60%

- **The evidence points lower.**
  - GE's own life-of-programme 787 win rate is 70% [CX-0615].
  - Goldman Sachs notes "Genx 60% mkt share on 787 platform, as of April 2022" (`gs_cfm:Aerospace Propulsion Division!AH29`), an installed share.
- **Why 0.78 stands.**
  - It fits only as a forward delivery share, and as the complement of Rolls-Royce's 0.22: fits on a contested airframe must sum to 1.
  - Delivery check: 100 Boeing widebodies × 2 × 0.78 = 156 GEnx a year. MS has 157.5 in 2026 and 189 from 2027 (`ms_cfm:Civil OE!AP57`, `!AX57`); GS has 125 and 138 (`gs_cfm:Aerospace Propulsion Division!AB29`, `!AC29`).
  - Both calibrators flag it. B would use 0.75 if Rolls-Royce's 0.22 were re-cut; A calls it the top of the life-of-programme evidence.
- **Materiality is small.**
  - Each 0.08 of fit is about 16 GEnx a year × $5.0M = $80M a year, under $1B of PV over the game.
  - It matters only when a 787 re-engine changes hands. `genx_upgrade` would take GE to 0.83, further above the evidence.
- **Recommendation.** Keep 0.78 so the 787 split stays coherent. Revisit it together with Rolls-Royce's 0.22.

### 4.2 The LEAP aftermarket margin

There are three readings.
- **GS:** LEAP aftermarket EBITA of €17.3M at an assumed 1% margin in 2026 (`gs_cfm:Aerospace Propulsion Division!AB260`, `!AB261`), and LEAP OE profit of 0 (`!AB86`).
  - GS's own note explains this: "no margin recognition of RPFH contract over 2021-25. Revenues = Cost until 2026" (`!AH257`).
  - It is an accounting artefact, not lifecycle economics. Neither calibrator used it.
- **MS:** 10% in 2025 (`ms_cfm:Civil AM!BM47`), 20% in 2026 (`!BU47`) and 40% in 2030 (`!DA47`), still rising. That compares with 65% for the CFM56 (`!BU45`), a supply-crunch peak; it was 57.8% in 2018 (`!AK45`).
- **GE:**
  - LEAP stays "below the 56" like for like; an analyst reading of the 2024 charts puts it at about half [CX-0175].
  - But LEAP aftermarket profit dollars reach parity with the CFM56 by about 2030, "and continue to improve beyond that" [CX-0212], [CX-0971].
  - New contracts are re-priced upward [CX-0215].

The calibrators' choices:
- A uses 0.42, after the haircut for GE's shop share; B uses 0.45, before a 6% sustaining-R&D haircut.
- The margin is not the main source of the LEAP gap; lifetime revenue is (§3.4). Margin and revenue together span 1.9-4.1 for the LEAP value.
- GE's parity claim implies about 3.7 and MS's 2030 path about 3.1. The reconciled 3.0 sits at the conservative end.

### 4.3 Capex attribution

No LEAP or RISE development cost is disclosed. Both estimates double Safran's R&D and capex humps, and reach $7.0B for ducted by offsetting choices:
- **Doubling** assumes GE spent what Safran did. GE owns the core and HPT, so it probably spent more.
- **LEAP's share of Safran's hump:** A about 85% (less Silvercrest), B 75%.
- **Baseline:** A uses a linear 2010-18 trend, B the 2004-10 run rate.
- **Industrialisation reused by a successor:** A counts half of $3.2B, B about 40% of $2.2B.
- **Capitalised R&D** spiked at €516M and €475M in 2013-14 (`ms_cfm:Propulsion!M51`, `!N51`). The cells do not show whether it is inside the self-financed line.
- **Double counting.**
  - B's 6% haircut keeps sustaining R&D inside the value per engine and charges new-programme R&D as capex.
  - A builds the value from margins, with no separate haircut.
- **The open-fan uplift** is judgement: A × 1.4; B × 1.35 + $1.3B.
- **Derivative capex is new.** The LEAP derivative now costs $1.0B and is no longer free. That makes the fallback slightly less attractive to CFM/GE, but not enough to change its ranking (§5).

### 4.4 The hurdle

- **The 15% figure.** GE's 15% [CX-0015], [CX-0066] is old GE's M&A test, not a programme hurdle. Culp's stated tests are a 12-24 month payback on restructuring [CX-0310] and high-single-digit returns on bolt-ons [CX-0460].
- **Behaviour points both ways.**
  - Lower:
    - GE accepts launch losses as "the price of admission" [CX-0557];
    - it keeps R&D at 6-8% with no "programme dividend" [CX-0174], [CX-1255];
    - it protected RISE through crises [CX-0143], [CX-0553].
  - Higher:
    - it returns at least 70% of free cash flow [CX-0645], more than 100% in 2024 [CX-0953];
    - it holds capex to 2-3% of revenue [CX-0922];
    - it wants "additive" economics [CX-0301], and an airframer plus at least 20% better fuel burn before a launch [CX-0205], [CX-0217];
    - Flannery feared big unstaged bets [CX-0787].
- **Safran.** No Safran hurdle is in the evidence. A's 13% averages GE's 15% with an assumed 11.5%.
- **Convention.** The mapping convention matters too: B's formula loads alpha about twice as fast per point of hurdle as A's convention (§3.2).
- **Reconciled 0.45, PLACEHOLDER.** §5 shows it barely moves CFM/GE's choices.

### 4.5 Other flags

- A's GEnx-upgrade saving chain multiplies to $0.18B, not the $0.15B it states (§3.9).
- B quotes `ms_cfm:Propulsion!BD21` as 529.8; the cell holds −529.8 (R&D booked as a cost). The arithmetic is unaffected.
- GE's WACC, the GE share of GEnx (0.80-0.90) and B's GE90 deliveries before 2014 are assumptions, not cells.

## 5. Sensitivities

**Setup.**
- Scenario `five-player-2045` with all three supplier players and no inject in turn 1.
- `options --side cfm` evaluates CFM/GE's 144 order bundles, launched in 2026, against nine airframer engine-selection scenarios. Other suppliers make no new moves in it.
- Variants: alpha 0.30 or 0.60; LEAP value 2.6 or 3.3.
- For range, each calibrator's full set:
  - A: alpha 0.60, LEAP 2.6, GEnx 4.5, ducted 3.1, open fan 3.5;
  - B: alpha 0.30, LEAP 3.3, GEnx 5.2, ducted 3.5, open fan 4.3.
- `whatif` priced the airframers' engine choices for an NGSA or fps launched in 2026, including Pratt & Whitney launching GTF2.

**Table 5.1: CFM/GE's own moves when no airframe launches (delta PV, $B).**

| Option | Base | α 0.30 | α 0.60 | LEAP 2.6 | LEAP 3.3 | A's set | B's set |
|---|---|---|---|---|---|---|---|
| LEAP upgrade | **4.9** | **5.0** | **4.8** | **4.5** | **5.3** | **4.4** | **5.4** |
| GEnx upgrade | 0.7 | 0.7 | 0.6 | 0.7 | 0.7 | 0.5 | 0.7 |
| Both upgrades, same turn | 4.2 | 4.5 | 3.9 | 3.7 | 4.5 | 3.4 | 4.9 |
| Embraer partnership | −0.1 | +0.1 | −0.3 | −0.1 | −0.1 | −0.3 | +0.1 |
| Lobbying | −0.1 | −0.1 | −0.1 | −0.1 | −0.1 | −0.1 | −0.1 |
| Launch ducted | −8.2 | −7.3 | −9.0 | −8.2 | −8.2 | −9.0 | −7.3 |
| Launch open fan | −10.9 | −9.7 | −12.0 | −10.9 | −10.9 | −12.0 | −9.7 |
| Launch both | −21.1 | −18.9 | −23.2 | −21.1 | −21.1 | −23.2 | −18.9 |

**Table 5.2: CFM/GE's delta PV ($B) when an airframe launches in 2026 on each engine.**

| Airframe flies | Base | α 0.30 | α 0.60 | LEAP 2.6 | LEAP 3.3 | A's set | B's set |
|---|---|---|---|---|---|---|---|
| NGSA: LEAP derivative (CFM no move) | 18.9 | 19.0 | 18.8 | 16.2 | 20.9 | 16.1 | 21.0 |
| NGSA: CFM ducted, standard terms | −8.8 | −8.0 | −9.6 | −3.9 | −12.5 | −7.9 | −10.6 |
| NGSA: CFM ducted, aggressive terms | −16.5 | −15.7 | −17.3 | −11.6 | −20.2 | −15.0 | −18.5 |
| NGSA: GTF2 (P&W launches) | −36.4 | −36.4 | −36.4 | −31.5 | −40.0 | −31.5 | −40.0 |
| fps: LEAP derivative | 1.5 | 1.6 | 1.4 | 1.1 | 1.8 | 1.0 | 1.9 |
| fps: CFM ducted, standard terms | −18.9 | −18.1 | −19.8 | −13.9 | −22.7 | −17.1 | −21.1 |
| fps: GTF2 (P&W launches) | −37.6 | −37.6 | −37.6 | −32.6 | −41.3 | −32.6 | −41.3 |

The airframers' payoffs do not depend on CFM/GE's parameters. In the base run:
- Airbus (NGSA) gets +28.5 on the derivative, +34.4 on ducted at standard terms, +41.6 on ducted at aggressive terms, and +36.5 on GTF2.
- Boeing (fps) gets +5.3, +8.5, +12.1 and +9.4.

**What changes and what does not.**
1. **The ranking never changes.**
   - In every variant, the LEAP durability upgrade alone is CFM/GE's best option in all nine scenarios, on both the worst case (4.4-5.4) and the best case (18.3-23.7).
   - All 16 bundles without a launch rank above all 128 bundles with one, on both measures.
2. **Alpha moves only the capex-heavy options.**
   - From 0.30 to 0.60, launching moves by about $1.7B (ducted), $2.3B (open fan) and $4.3B (both); the upgrades by $0.6B at most.
   - Embraer changes sign (+0.1 at 0.30, −0.3 at 0.60): it is a break-even option. The rival-engine outcomes do not move, since they carry no CFM capex.
3. **The LEAP value matters more than alpha.** Between 2.6 and 3.3:
   - the derivative's gain on NGSA moves from 16.2 to 20.9;
   - the cost of launching ducted for NGSA instead of letting it fly the derivative moves from −20.1 to −33.3;
   - the loss if NGSA flies GTF2 moves from −31.5 to −40.0.

   A richer LEAP makes CFM/GE less willing to launch (it cannibalises more) and raises what it stands to lose.
4. **Why CFM/GE never launches in the options table.**
   - The table assumes rival makers stay still. An airframe that asks for a rival engine then falls back to the LEAP derivative, which the engine books at fit 1 and the incumbent value.
   - A new CFM engine instead starts at −$1.0M per engine, passes LEAP's $3.0M only after about 9 years, and costs $7.0B × 1.45.
   - So committing an engine the airframe would otherwise fly as a derivative costs $15-33B across the variants ($20B for fps and $28B for NGSA in the base). Withholding, as Joyce proposed for the NMA [CX-1126], is the default.
5. **The real decision comes under a rival threat.** With Pratt & Whitney launching GTF2:
   - Both airframers prefer GTF2 to CFM's ducted engine on standard terms (Airbus by $2.2B, Boeing by $0.8B).
   - Both prefer CFM's ducted engine on aggressive terms to GTF2 (by $5.1B and $2.7B).
   - For CFM/GE, ducted on aggressive terms (−16.5) beats losing NGSA to GTF2 (−36.4) by $20B in the base and by $17-21B in every variant. Aggressive terms are close to a pure transfer (Airbus +7.3, CFM −7.7).
6. **Sequencing.**
   - The two upgrades launched in one turn strain each other: overlapping 3-year windows cost 1.75 × 3/5 × 1.45 ≈ $1.5B, about $1.4B of PV. So LEAP + GEnx (4.2) is worth less than the LEAP upgrade alone (4.9); staggered, the GEnx upgrade would add value.
   - Lobbying pays only through the open fan's capture and is never worth its cost on its own. The airframers' disincentive to wait for the open fan ($33-36B in the options table) is far beyond +0.5pp.

<details>
<summary>Commands</summary>

All from `/home/user/aero-engine-gameboard`. The scratch runs were deleted afterwards.

- `python3 -m wargame.engine new --scenario five-player-2045 --suppliers rolls_royce,pratt_whitney,cfm --run-id cfm-calib-scratch --force`, then `inject --run cfm-calib-scratch --none` and `options --run cfm-calib-scratch --side cfm`.
- The same for the variants, with `--override`:
  - `cfm-calib-scratch-a030`: `'{"suppliers": {"cfm": {"alpha": 0.3}}}'`; `-a060` with 0.6;
  - `cfm-calib-scratch-v26`: `'{"suppliers": {"cfm": {"incumbent_value_m_per_engine": {"nb": 2.6}}}}'`; `-v33` with 3.3;
  - `-setA`: `'{"suppliers": {"cfm": {"alpha": 0.6, "incumbent_value_m_per_engine": {"nb": 2.6, "wb": 4.5}, "programs": {"ducted": {"value_m_per_engine": 3.1}, "open_fan": {"value_m_per_engine": 3.5}}}}}'`;
  - `-setB`: `'{"suppliers": {"cfm": {"alpha": 0.3, "incumbent_value_m_per_engine": {"nb": 3.3, "wb": 5.2}, "programs": {"ducted": {"value_m_per_engine": 3.5}, "open_fan": {"value_m_per_engine": 4.3}}}}}'`.

  Each override was confirmed in the run's `state.json`.
- `whatif --run <id> --side control` with, for example:
  - `{"airbus": {"1": {"launch": [{"program": "ngsa", "year": 2026, "engine": "pw_gtf2"}]}}, "pratt_whitney": {"1": {"launch": [{"program": "gtf_next", "year": 2026, "terms": "standard"}]}}}`;
  - the same with `cfm_leap_plus`;
  - or with `cfm_ducted` and `{"cfm": {"1": {"launch": [{"program": "ducted", "year": 2026, "terms": "standard"}]}}}` (or `"aggressive"`);
  - and the fps equivalents for Boeing.
- `python3 wargame/profiles/build/cite_check.py wargame/profiles/cfm/calibration.md wargame/profiles/cfm/executives/evidence.jsonl`.

</details>

## 6. What is PLACEHOLDER, and what would firm it up

| Parameter | Why it is a placeholder | What would firm it up |
|---|---|---|
| `alpha` (0.45) | No programme hurdle from GE or Safran; GE's 15% is an M&A test; the calibrators' mapping conventions differ | A stated programme IRR or approval threshold from either partner (a CMD or investor-day slide); one alpha-to-hurdle convention agreed across all three engine makers |
| `open_fan` (9 yr, $10.0B, $3.9M) | No RISE budget or launch case is disclosed; capex and value are scaled from the ducted engine | A RISE cost line in Safran's or GE's R&D guidance; EU Clean Aviation funding shares [CX-0181]; a launch decision with a fuel-burn and content statement |
| `genx_upgrade` | No GEnx aftermarket cell (the GE90 stands in); upgrade cost and time-on-wing gain are assumed | GEnx shop-visit counts and revenue per visit; the cost of the GEnx durability and performance packages; the GEnx agreement share over time |
| `embraer_partner` | Nothing in the evidence on GE/CFM and Embraer | Embraer's next-aircraft size, thrust class and rate; any engine-selection or co-funding statement |
| `lobby_emissions` | Nothing in the evidence on lobbying spend or effect | Policy proposals that price carbon on new aircraft; precedents for government co-funding of engine programmes beyond [CX-1016] |
| `strain` (1.75 / 5) | Scale only; the concurrent-programme history [CX-1018], [CX-1131] has no cost figure | A disclosed cost of the GE9X or LEAP delays; engineering headcount against programme count |
| `cfm_leap_plus.capture_mult` (0.92) | Airframer and airline reaction to a derivative is not in the evidence | A LEAP derivative proposal for a new airframe and the airframer's response |
| `derivative_capex_b` (nb $1.0B, wb $0.5B) | Ratio evidence only: the -1B cost about 30% less engineering than the -1A [CX-1114] | A disclosed cost of a LEAP thrust or technology derivative; the -1B programme cost |
| GE share of GEnx (≈0.875) | Only Safran's 7.5% is in the cells | GEnx partner list and shares |
| LEAP lifetime aftermarket revenue ($15-16.5M implied) | The main driver of the A/B gap (§3.4) | LEAP revenue per shop visit after the durability kit; a GE split of LEAP services revenue; the first post-kit shop-visit intervals [CX-0655] |

