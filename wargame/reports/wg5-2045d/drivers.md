# Key assumptions behind fps value and the Do Nothing state (run `wg5-2045d`)

**The decision:** Boeing's round-2 choice in 2031, with fps three years late (`programs.fps.delay_years = 3`). Everything here was computed with the engine, two ways:
- **first workflow:** four independent ways of breaking down Do Nothing;
- **second workflow:** an inventory of fps assumptions, a breakdown of its value, and a sensitivity sweep with break-evens.

Each result was checked by an independent verifier and then by a critic. Material corrections from those checks are folded in. Scripts are in the session scratchpad (`dn/`, `fpsd/`, `spot.py`).

**Basis:**
- $B, present value (PV) to 2026 at Boeing's 10.5% cost of capital (WACC), over 2026-2060.
- Every figure is a **delta against a status quo in which nobody ever moves**: the 737 keeps 40% of narrowbodies at an 8% margin.
- Round 1 is as played. In rounds 2-3 every other player is held passive, which is the information Boeing had when it decided.

| State | Boeing delta PV | Against Do Nothing | Slip test (Airbus Delay Tactics in rounds 2-3) |
|---|---:|---:|---:|
| Do Nothing | **-2.40** | | -2.35 |
| 737 rate step only | -2.53 | -0.13 | |
| Best fps: Joint Venture, 10-year ramp-up, GTF2, with rate step (in service 2041) | **-3.13** | **-0.73** (needs > +1.00) ❌ | -7.06, gap -4.71 (needs ≥ -2.00) ❌ |
| Same fps with no delay (Solo, in service 2038) | +7.53 | +9.93 ✅ | gap +1.82 ✅ |
| 787 Re-engine 2031 with rate step | +1.03 | +3.43 | |

---

## 1. Do Nothing (-2.40): what it is made of

**One mechanism:** Airbus's NGSA, launched 2028 and in service 2035, takes narrowbody share from a Boeing that never answers.
- All of the -2.40 is narrowbody operating profit. Widebody, capex, strain and tactics are exactly 0.
- Remove the NGSA launch and Boeing's delta is 0.00.

**Formula:** PV = Σ 2,000 aircraft × $55M × 8% × (Boeing share lost) × 1.105^-(year-2026)
- That is $0.088B per point of share per year, undiscounted.
- Airbus's capture speed is 1.5pp × 1.03 (market cell) × 0.92 (LEAP-derivative engine) = **1.42pp per weighted year**, starting 2036. It is scaled by the replacement-wave weights (0.40 in 2036, rising to 1.0 from 2044).

| | 2035 | 2040 | 2045 | 2050 | 2053-2060 |
|---|---:|---:|---:|---:|---:|
| Boeing narrowbody share | 40.0% | 36.4% | 30.5% | 23.3% | 20.0% (Airbus capped at 80%) |

| Period | Aircraft lost | Undiscounted $B | PV $B | Share of PV |
|---|---:|---:|---:|---:|
| 2026-2035 | 0 | 0.00 | 0.00 | 0% |
| 2036-2045 (round 3) | 883 | -3.89 | -0.78 | 33% |
| 2046-2052 | | | -0.93 | 39% |
| 2053-2060 (at the floor, -1.76 a year) | | | -0.69 | 29% |
| **Total** | **6,216** | **-27.35** | **-2.40** | |

**Why a 40% → 20% collapse costs only $2.4B:**
1. **Low margin.** A lost 737 is worth $4.4M (8%), against $14.7M for an NGSA.
2. **Late losses.** Nothing is lost before 2036, and 67% of the PV falls after 2045.
3. **Heavy discounting.** At 10.5%, a 2050 dollar is worth $0.09. The average discount factor is 0.088.
4. **The horizon ends in 2060.** It is 6.7% of Boeing's status-quo narrowbody PV.

The model leaves out:
- aftermarket and services;
- fixed-cost absorption, since the 737 keeps 8% at half the volume (each 1pp of margin erosion would cost about $1.3B);
- any price response;
- volume growth;
- anything after 2060.

**Drivers ranked by swing in the Do Nothing value:**

| Driver | Value used | Range tested → Do Nothing | Swing | Source |
|---|---|---|---:|---|
| Boeing WACC | 10.5% | 6% → -6.34; 12% → -1.77 | 4.57 | Calibrated |
| Narrowbody capture speed | 1.5pp/yr | 0.5 → -0.86; 3.0 → -3.52 | 2.66 | **Placeholder** |
| Airbus share cap | 80% | 60% → 0.00; 90% → -2.57 | 2.57 | **Placeholder** |
| Horizon end | 2060 | 2050 → -1.45; 2080 → -2.88 | 1.43 | **Placeholder** |
| Replacement-wave floor | 0.4 | 0.2 → -2.08; 1.0 (no wave) → -3.29 | 1.21 | Assumption |
| Narrowbody volume (or price) | 2,000/yr, $55M | ±25% → -1.80 / -3.00 | 1.20 | **Placeholder** |
| 737 MAX margin | 8% | 6% → -1.80; 10% → -3.00 | 1.20 | Calibrated |
| Market reaction to NGSA | x1.03 | 0.75 → -1.86; 1.25 → -2.72 | 0.86 | Market-cell judgement |
| LEAP-derivative capture | 0.92 | 0.7 → -1.93; 1.1 → -2.70 | 0.77 | **Placeholder** |
| NGSA launch year | 2028 | 2027 → -2.58; 2031 → -1.94 | 0.64 | As played |

- **No effect on Do Nothing (exactly 0):** every injects, Airbus Poaching (there is no Boeing programme to hit), supplier upgrades, and every fps, rate, alpha and delay parameter.
- **State construction:** the Do Nothing state drops round-2/3 market reactions. Keeping NGSA's as-played x1.05 gives -2.43.

---

## 2. fps value (-0.73 against Do Nothing): what it is made of

fps is launched in 2031 and enters service in 2041. It never takes share, because NGSA leads and shares freeze once both are in service. It freezes Boeing at 37.5% from 2041 instead of sliding to 20%, and lifts the margin from 8% to 20.7%. The 20.7% is (25.64% + 0.5pp GTF2 + 1.5pp fuel spike) × 75%, after the Joint Venture partner's 25% share.

| Component of fps minus Do Nothing | PV $B |
|---|---:|
| Share protected (37.5% vs falling to 20%, at the 737 margin) | +1.35 |
| New-generation margin uplift on Boeing's own volume | +10.69 |
| of which base margin 25.64% vs 8% | +14.81 |
| of which GTF2 engine margin | +0.42 |
| of which fuel spike +1.5pp | +1.26 |
| of which the Joint Venture partner's 25% margin share | -5.80 |
| Rate-step line as booked | -0.43 |
| fps capex, after the partner's 35% | -12.35 |
| of which base ($17.6B nominal over 2031-37) | -8.05 |
| of which three delay years at 10% each ($5.3B nominal, 2038-40) | -1.44 |
| of which alpha loading (+30% on every capex dollar) | -2.85 |
| **Total** | **-0.73** |

**fps's value is a margin bet, not a share bet.** Most of the gain is the new airplane's 25.6% margin. The share it protects is worth only $1.35B, because it arrives in 2041, after NGSA has already taken 4.5 points; the rate step gives 2 of them back, hence 37.5%.

**Cost of each delay year** (like-for-like, Joint Venture): 0→1 year $2.86B; 1→2 $2.61B; 2→3 $2.31B. The three years total $7.78B: $5.90B of operating profit lost and $1.88B more alpha-loaded capex.
- The delay removes fps's first years in service, and no longer horizon gives them back. The model has no product life: fps earns from entry into service to the end of the horizon.

**Drivers ranked by swing in fps minus Do Nothing,** with the break-even for a launch. "Go" means the nominal-best fps passes both legs of Boeing's rule. A more lenient reading, where any variant passing both legs counts, is shown where it differs.

| Driver | Value used | Swing over range | Nominal leg passes | **Go needs** | Source |
|---|---|---:|---|---|---|
| Boeing WACC | 10.5% | 15.5 (6-12%) | < 9.5% | **< 7.7%** (lenient < 8.4%) | Calibrated |
| fps margin | 25.64% | 12.6 (15-35%) | > 28.4% | **> 34.7%** (lenient > 31.4%) | Calibrated |
| Joint Venture partner's capex share | 35% | 11.7 (0-60%) | > 43.9% | **> 47.9%** | **Placeholder** |
| Joint Venture partner's margin share | 25% | 11.6 (0-50%) | < 17.5% | **< 9.4%** | **Placeholder** |
| fps development capex | $30B | 10.6 ($15-40B) | < $25.9B | **< $21.8B** (lenient < $24.1B) | **Placeholder** |
| fps delay | 3 years | 7.8 (0-3) | ≤ 2 years | **≤ 1 year** | Scenario premise |
| Narrowbody volume (or price) | 2,000/yr, $55M | 6.5 (1,500-2,500) | > 2,269/yr | slip leg never passes | **Placeholder** |
| Alpha (capex surcharge) | 30% | 5.1 (0-50%) | < 13% | **never** (at 0%, slip gap -2.79) | Calibrated, undefined in config |
| Delay-year cost | 10%/yr | 3.8 (0-20%) | < 0.8% | < 0.5% | **Placeholder** |
| Horizon end | 2060 | 5.6 (2050-2080) | from 2077 | never (slip -2.74 even at 2100) | **Placeholder** |
| fps engine and supplier terms | GTF2 standard | 2.0 | none alone | none alone | **Placeholder** |
| Airbus share cap | 80% | 1.9 (60-90%) | no | no | **Placeholder** |
| Fuel-spike margin add | 1.5pp | 1.9 (0-3pp) | > 4.3pp | > 7.2pp | **Placeholder** |
| Narrowbody capture speed | 1.5pp/yr | 1.3 | no | no | **Placeholder** |

Engine range in detail:
- -1.68 if the engine falls back to the LEAP derivative;
- -0.73 on GTF2 at standard terms;
- -0.04 on GTF2 at aggressive terms;
- +0.34 on a UltraFan committed by Rolls-Royce on aggressive terms (slip gap -3.91).

Lesser drivers:
- fps technology edge over NGSA (not in config): +1.26 at a 1.3 level; the nominal leg needs 1.41.
- NGSA launch year: 0.76.
- Replacement-wave floor: 1.69.

**Zero-effect levers here:**
- the 10-year ramp-up's capture multiplier, because fps follows and never captures. The 10-year ramp-up beats the 7-year only through its 0.9 capex multiplier;
- the Joint Venture's strain relief;
- the supply-chain crunch;
- fps's technology-ready year and early penalty;
- the widebody boom.

**The slip leg rests on placeholder Delay Tactics.** With a maximum total slip of 2 / 1 / 0 years, the slip gap is -4.71 / -2.75 / -0.65. Even with no slip, the nominal leg (-0.73) still fails.

**Combined favourable case.** Every market driver at its best end, NGSA delayed to 2031, and Rolls-Royce UltraFan on aggressive terms:
- the Joint Venture passes both legs (+2.70 / -1.75);
- but the nominal-best version, Solo, fails the slip leg (+3.18 / -3.43).

So it is a Go only on the lenient reading of the rule.

---

## 3. Shared drivers, and what would make the delayed fps a launch

- **Shared by both states:** Boeing WACC, narrowbody volume and price, capture speed, the replacement-wave weights, Airbus's share cap, the horizon, and the NGSA timing, engine and market reaction.
- **fps only:** fps margin, capex, the Joint Venture terms, alpha, the delay and delay-year cost, the engine and supplier terms, and the fuel spike.
- **No single market assumption rescues the delayed fps.** One of these would be needed:
  - a delay of at most 1 year;
  - fps capex under about $21.8B;
  - a margin above about 34.7%;
  - Boeing's cost of capital under about 7.7%;
  - much richer Joint Venture terms (partner pays > 48% of capex, or takes < 9% of margin).
  Short of these, it takes a stack of favourable assumptions plus a supplier price concession.
- **The 787 Re-engine's lead is large.** It is +3.4 over Do Nothing, against fps's -0.7. Sensitivities were not run on the alternatives themselves.

## 4. State-construction caveats

- **Passive rivals and suppliers.** The states hold every other player passive from round 2. Restoring the as-played moves makes fps worse:
  - with Pratt & Whitney's GTF2 cancellation, fps falls back to the LEAP derivative: -1.68 / slip -5.42;
  - with Airbus's round-2 Poaching, which only hits a programme in development: -1.19 / -5.17;
  - with both: -2.13 / -5.88.
- **Fragile Do Nothing.** If Airbus launches an A350 Re-engine against a Boeing that does nothing, Boeing falls to -3.9 (2031) or -3.3 (2035).
- **Alpha.** Alpha (30%) is tagged calibrated in the README but is not defined in the config. It works as a 30% surcharge on every capex dollar, costing -$2.85B on fps.
- **Calibration status.** Calibrated: the 737 margin, WACC, fps margin, 7-year development and the capture rule. Placeholders: volume, price, shares, capture speed, share cap, horizon, fps capex, Joint Venture terms, ramp-up options, engine options, inject deck and tactics.
