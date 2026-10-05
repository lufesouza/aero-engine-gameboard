# Boeing: assigned objectives brief

**What this is.** Control has given Boeing a mission. The referee scores it alongside delta PV; it never changes the payoff. (inference) marks anything beyond the evidence. "Allowed" means within hard rules H1-H8 (`profile.md`). Engine numbers are `whatif` runs of 2026-10-04 (Commands, at the end): no injects, neutral markets, `cfm_ducted`, no widebody moves, unless stated. Sections 1-10 were written for the two-player, four-turn game. Section 11 adds the five-player game (`five-player-2045`; `profile.md` §11); material it replaces is marked **(four-turn game)**.

## 1. Assigned objective

```
Primary goal:   Hold the 50/50 NB market split; Defend incumbency
Possible moves: Launch fps with 7-year ramp-up | Launch fps with 10-year ramp-up | Launch fps via Embraer |
                Increase 737 production rate by 2030 | Do Nothing (Milk 737 MAX program)
Enablers:       Existing 737 customer base | trained workforce | government incentives | cash from 787 program
Constraints:    High debt load | ramp-up speed | engineering capacity | supply-chain bottlenecks
```

Source: Boeing Product Development, 'Players - narrowbody market: Who plays, what they want, and what they can do', Aerospace Game-Theory Briefing (Boeing Strategy), slide 4. BOEING PROPRIETARY.

## 2. Moves to levers

All levers checked against `rules --side control` (base and replacement-wave) and `rules --run <id> --side boeing` (`assigned_objectives`).

| Briefing move | Game lever and order | Modelled | Notes |
|---|---|---|---|
| fps, 7-year ramp-up | `launch` fps, `"variant": "solo"`, year Y | partly (four-turn game) | (four-turn game) 7 development years, $30B. Capture after EIS is fixed: 1.5 pp a year x engine and market multipliers |
| fps, 10-year ramp-up | `launch` fps, Solo; no slower-ramp variant | partly (four-turn game) | (four-turn game) Nearest proxies: a later launch, slips, or a market capture multiplier below 1. Base, Airbus idle, Turn-1 Rate Increase: fps 2029 gives +17.58 (48.0% in 2040); fps 2032 gives +11.86 (43.5%); fps 2029 at the market floor of 0.75 gives +14.85 (46.5%) |
| fps, 7-year ramp-up (five-player) | `launch` fps, `"ramp": "7y"` (the default) | yes | Capture x1.0, capex x1.0. Doctrine plan (Rate Increase in Round 1, fps 2031 Solo): +12.13 with Airbus idle; +2.44 / +3.55 / +4.61 against NGSA 2026 / 2028 / 2030 |
| fps, 10-year ramp-up (five-player) | `launch` fps, `"ramp": "10y"` | yes | Capture x0.7, capex x0.9 (placeholder multipliers). Same plan: +11.85; +4.25 / +5.35 / +6.41. The doctrine choice (`profile.md` §11) |
| fps via Embraer | `"variant": "jv"` | yes | Embraer pays 35% of capex, takes 25% of margin, relieves half the strain. Shares match Solo in every run, so it changes PV, not the metrics |
| 737 rate by 2030 | `"rate_increase": true` | yes | +2 pp two years after commitment; $1.2B; +0.05 alpha for 6 years. Only Turn 1 lands by 2030 (42% in 2030; Turn 2 gives 40%) |
| Do Nothing | no orders | yes | With Airbus idle: 40% share every year; delta PV 0.00 |

**Five-player game.** Both ramp moves are now modelled levers on any fps launch. The 737 rate lands by 2030 only if committed in Round 1 (2026-30): 42% in 2030, against 40% for a Round-2 commitment. "Launch fps via Embraer" is unchanged.

## 3. Enablers and constraints

| Item | Engine parameter (from `rules`) | Our evidence |
|---|---|---|
| 737 customer base | `sq_share` 0.40; 737 MAX margin 8% | 40% was the red line [B-0638]. The backlog means "no hurry" [B-2305] |
| Trained workforce | not modelled; nearest is Poaching ($0.75B a turn) | 15,000 hired in 2022 [B-2035]; in 2011 half could retire within five years [B-0390] |
| Government incentives | not modelled | Ex-Im export credit [B-1077]; a Washington tax incentive, since repealed after the WTO case [B-1761]; support "on market terms" [B-1825] |
| Cash from 787 | widebody 58.8% share, 20% margin; no funding test | Margins to beat 2018 at target rates [B-2198]; near break-even in 2022 [B-2024] |
| High debt load | alpha 0.30; WACC 10.5%; no debt figure | "Far and away, our priority is debt" [B-2327, BX-1305]. Protect the rating [B-2186] |
| Ramp-up speed | capture 1.5 pp a year; market 0.75-1.25; Rate Increase lag 2 years | KPIs, not dates [B-2221]. Steps of 5 a month, 6+ months apart [B-2351] |
| Engineering capacity | strain $3B x min(1, overlap/5); the Joint Venture halves it | One development at a time [B-0341, B-1526]; the MAX crisis pulled staff off the NMA [B-1593] |
| Supply-chain bottlenecks | Delay Tactics, shown as a "supplier bottleneck" (1 year a turn, at most 2); supply-crunch inject (strain +50%) | Supplier readiness is a hard gate [B-2308]; beyond 47 a month it binds [B-2340] |

**Five-player game.** `profile.md` §11.4 maps each item to doctrine and to the game. Two engine parameters change. Ramp-up speed now has a lever (the 10-year ramp). Supply-chain bottlenecks now include the engine makers: an uncommitted engine falls back to the LEAP derivative, and a late commitment makes the fps wait.

## 4. How attainment is measured

| Metric | Measures | Target and years | Status quo |
|---|---|---|---|
| `nb_share_50` | Boeing narrowbody share in the worst listed year | ≥ 50% in 2040, 2045, 2050 | 40%: not met, gap -10.0 pp |
| `defend_incumbency` | Boeing share minus the status-quo path (40%, moved only by injects) | ≥ 0 in 2030, 2035, 2040, 2045, 2050 | met, gap 0.0 pp |

(four-turn game) 2040 binds `nb_share_50` in 279 of the 375 runs per scenario. A later year binds only when NGSA enters service first and fps is not in service by 2040 (no fps, or a launch in 2034 or later). In five-player-2045, 2040 binds for every plan that comes closest (Section 11).

## 5. What it takes (four-turn game)

**Method.** 375 plans per scenario: Airbus idle or NGSA in 2026, 2029, 2032 or 2035, against Boeing fps none or 2026-2037, Solo or Joint Venture, with the Rate Increase none, Turn 1 or Turn 2. The **doctrine plan** is a Turn-1 Rate Increase plus fps Solo in 2029. Under the default team, the plan against an NGSA launched in 2026-27 is the Joint Venture (`teams.md` §9). Its shares are the same; its PV against NGSA 2026 is +0.34 (base) and +2.47 (wave). **Objective premium** = best PV minus the best PV that meets the metric. Within H1 the doctrine plan is the best-PV plan against every Airbus timing in both scenarios.

**Base scenario** (Boeing $B; Boeing share in 2040)

| Airbus | Best PV (any) | Doctrine plan | Best plan meeting `nb_share_50` | `defend_incumbency` |
|---|---|---|---|---|
| Idle | fps 2028 + Rate T1: +19.94 (49.5%) | +17.58 (48.0%) | fps 2027 + Rate T2: +17.51 (51.0%); premium 2.42 | doctrine plan; premium 0 |
| NGSA 2026 | +4.06 (39.0%) | +1.95 (37.5%) | none (best 42.0%) | only fps 2026 (with or without Rate) or fps 2027 + Rate; best fps 2027 + Rate T2: +2.76, premium 1.30. Best allowed: doctrine plan, gap -2.5 |
| NGSA 2029 | +8.98 (43.5%) | +6.63 (42.0%) | none (best 46.5%) | doctrine plan; premium 0 |
| NGSA 2032 | +12.62 (48.0%) | +10.27 (46.5%) | fps 2026 + Rate T2: +8.18 (51.0%); premium 4.44 | doctrine plan; premium 0 |
| NGSA 2035 | +15.21 (49.5%) | +12.86 (48.0%) | fps 2027 + Rate T2: +13.16 (51.0%); premium 2.05 | doctrine plan; premium 0 |

**Replacement-wave scenario.**
- **`nb_share_50`:** no plan meets it. The closest is fps 2026 + Rate, at 47.0% in 2040 (gap -3.03), with Airbus idle or NGSA 2035.
- **`defend_incumbency`:** the doctrine plan meets it against every timing, at zero premium. Against NGSA 2026 the margin is thin: 40.2%. Without the Rate Increase it falls to 38.2%.
- **PV:** the doctrine plan gives +14.73 (idle), +4.75, +6.63, +8.39 and +10.09 (NGSA 2026 to 2035). The best plan, fps 2028 + Rate T1, is $1.36-1.45B higher.

**What it means.**
- **`nb_share_50` breaks the hard rules.** It needs fps in 2026-27, which breaks H1 (no Turn-1 fps) and H2 (EIS before the 2035 tech-ready year). The early-entry penalty is 2 pp a year: margin at EIS is 23.64% for fps 2027 and 21.64% for fps 2026, against 25.64% from 2028.
- **`defend_incumbency` is nearly free.** The doctrine plan meets it except against NGSA 2026 (base). There even the H1 exception (fps 2028 Joint Venture + Rate T1) reaches only 39.0% (+1.82), and the default team vetoes that exception (`teams.md` §9).

**Rival timing** (base, Rate Increase in Turn 1).
- **`nb_share_50` needs Airbus to wait.**
  - fps 2026 needs NGSA in 2032 or later; 2031 misses by 0.5 pp.
  - fps 2027 needs NGSA in 2033 or later.
  - fps 2028 misses by at least 0.5 pp whatever Airbus does.
- **Airbus gains by not waiting:** against fps 2027, NGSA 2030 is worth +11.96 to it, NGSA 2033 only +1.65. An analyst expected Airbus to fix the NGSA architecture around 2027 [B-2536], so we expect NGSA in Turn 1 or 2 **(inference)**.
- **`defend_incumbency` lets fps trail NGSA by one year** (Solo, Turn-1 Rate Increase; NGSA 2026-35). In the wave the allowance is wider: three years for NGSA by 2028, two for NGSA 2029-33 (fps 2031 against NGSA 2029 holds 40.66%), one for NGSA 2034-35.
- **Slip test** (Airbus Delay Tactics in Turns 2-3; fps EIS 2038):
  - against NGSA 2029, the doctrine plan drops to 39.0% (PV -4.03) in the base scenario but holds 40.66% (PV -2.67) in the wave;
  - against NGSA 2026 it fails in both (34.5% base, 38.86% wave);
  - against NGSA 2032 it holds in both (42.0%).
- **The market cell can tip `nb_share_50`.** At the maximum fps capture multiplier of 1.25 with Airbus idle:
  - fps 2028 + Rate reaches 51.38% (+22.78);
  - the doctrine plan misses by 0.5 pp (+20.15).

## 6. Fit with our doctrine

**Agrees.**
- **Share has mattered.** "We do not want them to get to 60% and us, 40%" [B-0602, B-0638]. Albaugh aimed at about half the market [BX-0001].
- **Boeing moves when "meaningful market share" is at risk** [B-0422], as in the MAX reversal [B-0413].
- **Lateness cost money:** the MAX came 1-1.5 years behind the NEO [B-0733, B-0804], and being a year late meant more aggressive pricing [B-0733].
- **Boeing benchmarks deliveries against Airbus** [B-2324, B-2537], and the 737 rate drives cash [B-2298].

**Pulls against.**
- **50/50 was dropped:** "not an objective of ours" [B-1936]. Chasing tier rank "gets you in trouble" [B-1980].
- **Boeing prices for supply scarcity** [B-2331]; that it puts margin ahead of share is **(inference)**.
- **The gates forbid an early fps:** current programs first [B-2276], debt first [B-2327], no dates [B-2313, B-2316], "not before '35" [B-2061], "will not be rushed" [B-2164].
- **One development at a time** [B-0341]; "no hurry" [B-2305].

**Weighing rule (inference: built from Section 5 and the doctrine).**
1. **The objective sets the aim.** Play for `defend_incumbency`. Track `nb_share_50` but do not chase it: it needs a Turn-1 fps and an Airbus that waits until 2032 or later (four-turn game). In five-player-2045 no plan meets it (Section 11).
2. **The doctrine sets how.** Timing, variant, engine and Re-engine follow `profile.md` §6 and §9 and Malave's buffer test (`teams.md` §9).
3. **Tie-breaks.** Within ε, the objective breaks ties toward a Turn-1 Rate Increase and toward `cfm_ducted` (capture 1.0 against 0.95 for `pw_gtf2`).
4. **The premium cap.** An objective premium counts against the H8 cap of $2B for soft choices (profile H8), shared with any doctrine premium **(inference)**.
5. **The red line.** Never break H1-H8 or a red line for the objective.

## 7. Per-turn objective check

Add these steps to the decision procedure (`profile.md` §9).

**Four turns (four-turn game).**

1. **Step 1.** Record `your_objectives` from `brief` (met, `gap_pp`) before any orders.
2. **Step 5.** Read `objectives.boeing` in each `whatif` (doctrine plan, best allowed plan, Do Nothing, slip test). Pick the cheapest allowed plan that meets `defend_incumbency`: usually the doctrine plan with this turn's Rate Increase, if H6 allows.
3. **Step 7.** Compute the objective premium against the best allowed plan. If it plus any doctrine premium exceeds $2B, take the best allowed plan.
4. **If no allowed plan meets a metric,** log "unattainable within hard rules", the gap and the blocking rule. Pay nothing.
5. **Step 10.** Log: "nb_share_50 a → b pp; defend_incumbency c → d pp (slip test e); objective premium $f B; cap used $g B of $2B."

**Three rounds (five-player-2045).** Numbers are the Section 11 snapshots.

1. **Every round, step 1.** Record `your_objectives` from `brief` (met, `gap_pp`). Also record the engines committed so far, with their ready years, from the event log.
2. **Round 1 (2026-30).**
   - Commit the Rate Increase if H6 allows. It is the only move that lifts 2030, the first `defend_incumbency` year (42% against 40%).
   - Order no fps (H1).
   - Log `nb_share_50` as "unattainable in this scenario": no plan reaches 50% in 2040.
3. **Round 2 (2031-35), step 5.** Read `objectives.boeing` in each `whatif`. Check:
   - the doctrine plan: fps 2031, Solo, 10-year ramp, on the committed engine;
   - the 7-year ramp;
   - the Joint Venture;
   - Do Nothing;
   - the slip test (Airbus Delay Tactics in Rounds 2 and 3);
   - the engine-fallback case.

   Pick the cheapest allowed plan that meets `defend_incumbency`. If NGSA launched in 2026 or 2027, no allowed plan meets it. Log "unattainable within hard rules (H1)" and the gap: -1.14 or -0.54 pp.
4. **Round 3 (2036-45), step 5.** Only an unlaunched fps or a deferred Rate Increase can still move narrowbody share; the 787 Re-engine cannot. If fps is unlaunched, test fps 2036 against Do Nothing and read `defend_incumbency` for 2040-50.
5. **Step 7.** Compute the objective premium as above. It shares the $2B cap with doctrine premiums.
6. **Step 10.** Log: "nb_share_50 a → b pp; defend_incumbency c → d pp (slip test e; engine fallback f); fps engine fitted g; objective premium $h B; cap used $i B of $2B."

## 8. Boeing PD's view of the other players

These are **Boeing Product Development's planning assumptions about rivals and suppliers**, not intelligence on their real intentions.

```
Airbus        | Primary goal: Defend 60/40 edge; Protect A320 family
              | Moves: Launch NGSA ($20B) | Do Nothing (Milk A320neo family) | Delay fps (supply-chain bottleneck) | Delay fps (talent poaching)
              | Enablers: Existing A320 customer base | government incentives | cash | A220-500 closing the seat-size gap
              | Constraints: Engineering capacity (NGSA & A350 share teams) | fines if delay tactics are detected
CFM           | Primary goal: Dominate narrowbody engines; Introduce Open Fan
              | Moves: Open Fan only | Ducted only | Open + Ducted (both) | Partner with Embraer | Lobby governments on emissions
              | Enablers: Existing maintenance & overhaul base | cash | Sustainable Aviation Fuel capability
              | Constraints: Open Fan certification risk | airframer reluctance | raw materials
Pratt&Whitney | Primary goal: Restore credibility; Capitalize on GTF investment
              | Moves: Launch GTF2 solo | Joint Venture with Rolls-Royce | Do Nothing (continue GTF1)
              | Enablers: Mature gearbox technology | RTX leverage | cash from GTF base
              | Constraints: GTF reputation issues | engineering resources
Rolls-Royce   | Primary goal: Enter narrowbody market; Keep Widebody dominance
              | Moves: Ultrafan widebody only (no NB entry) | Ultrafan narrowbody solo | Joint Venture with Pratt & Whitney | Do Nothing (continue Trent only)
              | Enablers: Free cash from widebody | reputation | airframer support for a 3rd engine maker
              | Constraints: Engineering resources shared with widebody | no NB MR&O scale | gearbox sizing
```

- **Airbus (four-turn game).** Its 60% and our 50% are zero-sum. An NGSA by 2031 ends our 50%. Delay Tactics with an NGSA in 2029 break `defend_incumbency` in the base scenario, so keep the slip test as the baseline. The engine prices NGSA at $25B.
- **CFM (four-turn game).** The RISE open fan cannot enter service before 2045. It also adds a year and cuts capture to 0.85. The doctrine plan on it waits until 2045: -17.58 and 42.0% in 2040, against +17.58 and 48.0% on `cfm_ducted`. Against NGSA 2029 it breaks `defend_incumbency` (36.0% in 2040, 28.5% in 2045). A 2037 launch enters service in 2045 without waiting, but still scores $1.95B below a 2037 launch on `cfm_ducted` (Airbus idle). Keep `cfm_ducted`; Boeing sees an open-rotor engine as a long-run option [B-2065, B-2078].
- **Pratt & Whitney.** In the two-player game GTF2 is always on offer, with capture 0.95: the doctrine plan on GTF2 gives +18.06 and 47.7% in 2040, against +17.58 and 48.0% on `cfm_ducted`. When P&W plays, fps gets GTF2 only if P&W launches it by the end of that turn; otherwise fps falls back to `cfm_ducted`. Boeing is wary of new-engine durability [B-2304].
- **Rolls-Royce.** In the two-player game the UltraFan narrowbody adds a year to EIS. Its widebody engine is the default for the A350 Re-engine, whose launch triggers H3.
- **Five-player game.** All three engine makers play, and every new fps engine needs its maker's commitment. Without one, a Rolls-Royce or P&W choice falls back to `cfm_ducted`, and `cfm_ducted` falls back to the LEAP derivative. NGSA costs $20B.
  - The engine moves PV, not share. On the doctrine plan every engine gives 43.2-43.3% in 2040 (Section 11).
  - The open fan still waits for 2045. A 2037 launch scores $1.6B below a 2037 `cfm_ducted` (`profile.md` §11.2).
  - How to read the makers' moves is in `profile.md` §11.3.

## 9. The replacement wave and fps timing

Source: Boeing Product Development, draft slide 7 on the drivers of a late-2030s entry into service (BOEING PROPRIETARY). Paraphrased below; the digitised curve is in `rules --scenario replacement-wave` (`segments.nb.replacement_wave`).

**Slide 7's four drivers.**
1. **Retirement timing:** MAX and neo fleets age out in the mid-2030s, and orders need 5+ years of lead time.
2. **Product lifecycle:** limits on further MAX enhancements cap its competitiveness.
3. **Eroding share and margin:** A320-family gains and price pressure.
4. **Competition:** COMAC and others, and the risk of being leapfrogged.

Replacements: about 38 in 2037, 334 in 2040, 825 in 2044; about 27% are 737 MAX.

**What the scenario does.** It scales a leading product's yearly capture by 0.4 + 0.6 x min(1, replacements/807): 0.4 before 2037, 0.648 in 2040, 1.0 in 2044, 0.981 in 2045, then 1.0 from 2046. The base scenario is unchanged.

**What the grid shows** (reproduced; Solo, no Rate Increase).
- **The best launch year does not move.**
  - Grid years: 2029 is best in both, +16.72 base (2026: +13.50) and +13.87 wave (2026: +8.54).
  - Every year: 2028 (EIS 2035) is best in both, +19.09 and +15.34.
- **The wave hits early entry hardest:** -$4.96B for a 2026 launch, -$0.08B for 2035.
- **It softens a late answer to NGSA.**
  - Do Nothing against NGSA 2026: -4.28 base (29.5% in 2040), -2.88 wave (35.0%).
  - fps 2032 against NGSA 2029: +0.26 base, +1.99 wave.
  - Entering service in the same year is unchanged: +5.76 in both.
- **Net:** the wave helps `defend_incumbency` and rules out `nb_share_50`.

**Driver 3 is not modelled.** Under Do Nothing, with Airbus idle, the engine holds the 737 MAX at 40% and an 8% margin in both scenarios. The slide expects erosion, so Do Nothing is flattered in both (inference, unmodelled). The record shows the late MAX 10 weakening the top of the line [B-2249] while Boeing calls the family competitive [B-2033].

## 10. Gaps and modelling limits

- **No ramp-up lever** for the 7-year and 10-year moves (four-turn game). In five-player-2045 the ramp is a lever, but its multipliers (capture x0.7, capex x0.9) are placeholders.
- **Market multipliers** decide `nb_share_50` at the margin; Boeing does not set them.
- **Not modelled:** debt (only alpha), workforce, incentives, the A220-500, COMAC, MAX erosion.
- **Fixed NGSA dates;** no injects or widebody moves.
- **The wave** is digitised to ±20 aircraft a year, and its 0.4 floor is assumed.
- **Supplier players** are not in these runs. With Rolls-Royce or Pratt & Whitney playing, their engines depend on their launches.

<details>
<summary>Commands</summary>

```bash
cd /home/user/aero-engine-gameboard
export WARGAME_RUNS_DIR=<scratchpad>/objectives/runs_boeing_verify
python3 -m wargame.engine rules --scenario base --side control                # levers, parameters, metrics (Sections 2-4)
python3 -m wargame.engine rules --scenario replacement-wave --side control    # capture weights, replacement curve (Section 9)
python3 -m wargame.engine new --run-id v-base --scenario base
python3 -m wargame.engine new --run-id v-wave --scenario replacement-wave
python3 -m wargame.engine rules --run v-base --side boeing                    # assigned_objectives
# Template (doctrine plan against NGSA 2029; Section 5):
echo '{"boeing": {"1": {"rate_increase": true}, "2": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2029}]}},
 "airbus": {"2": {"launch": [{"program": "ngsa", "engine": "cfm_ducted", "year": 2029}]}}}' | python3 -m wargame.engine whatif --run v-base --side control
# Sweep, 375 plans per run (Sections 4, 5, 9 and the grid): the template looped over Airbus idle / NGSA 2026, 2029, 2032, 2035,
#   fps none / 2026-2037 x solo, jv, Rate none / T1 / T2; launch in the turn holding the year. Script: <scratchpad>/objectives/sweep_boeing.py
python3 <scratchpad>/objectives/sweep_boeing.py v-base vsweep_base.jsonl; python3 <scratchpad>/objectives/sweep_boeing.py v-wave vsweep_wave.jsonl
python3 <scratchpad>/objectives/analyse_sweep.py vsweep_base.jsonl vsweep_wave.jsonl
# Same template, looped on v-base and v-wave:
#   rival timing: fps 2026, 2027, 2028 Solo + Rate T1 against Airbus idle and NGSA 2026-2037;
#   lag test: Rate T1 + fps Solo in NGSA year + 0..3, NGSA 2026-2035;
#   slip test: Rate T1 + fps 2029 Solo or jv, Airbus idle / NGSA 2026, 2029, 2032, plus "delay_tactics": true in turns "2" and "3".
# Margin at EIS (boeing.programs[].margin_at_eis), Do Nothing, Rate Increase timing:
echo '{"boeing": {"1": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2027}]}}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control   # and 2026, 2028
echo '{"boeing": {}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control
echo '{"boeing": {"1": {"rate_increase": true}}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control   # and "2", "3"
# Market cell (Sections 2 and 5): v-mkt28 at 1.25; v-mkt29 at 1.25 and v-mkt29lo at 0.75 (Rate in T1, fps 2029 + market in T2)
python3 -m wargame.engine new --run-id v-mkt28 --scenario base
echo '{"boeing": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2028}], "rate_increase": true},
 "airbus": {}, "market": {"capture_mult": {"fps": 1.25}}}' | python3 -m wargame.engine adjudicate --run v-mkt28 --turn 1
echo '{"boeing": {}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-mkt28 --side control
python3 -m wargame.engine new --run-id v-mkt29 --scenario base
echo '{"boeing": {"rate_increase": true}, "airbus": {}}' | python3 -m wargame.engine adjudicate --run v-mkt29 --turn 1
echo '{"boeing": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2029}]}, "airbus": {},
 "market": {"capture_mult": {"fps": 1.25}}}' | python3 -m wargame.engine adjudicate --run v-mkt29 --turn 2
echo '{"boeing": {}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-mkt29 --side control
# GTF2 (Section 8): the doctrine plan with "engine": "pw_gtf2" on v-base and on a run with P&W playing
python3 -m wargame.engine new --run-id v-pw --scenario base --suppliers pratt_whitney
echo '{"boeing": {"1": {"rate_increase": true}, "2": {"launch": [{"program": "fps", "variant": "solo", "engine": "pw_gtf2", "year": 2029}]}},
 "airbus": {}}' | python3 -m wargame.engine whatif --run v-pw --side control   # and --run v-base
# Open fan (Section 8): the doctrine plan with "engine": "cfm_open_fan" (Airbus idle and NGSA 2029), then fps 2037 in turn "4" on each engine
echo '{"boeing": {"1": {"rate_increase": true}, "4": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_open_fan", "year": 2037}]}},
 "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control   # and "engine": "cfm_ducted"
# Citations
python3 wargame/profiles/build/cite_check.py wargame/profiles/boeing/objectives.md wargame/profiles/boeing/evidence.jsonl wargame/profiles/boeing/executives/evidence.jsonl --show
```

</details>
