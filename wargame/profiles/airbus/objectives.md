# Airbus: assigned objectives

This brief covers Airbus's assigned mission, how the engine scores it and what it costs. The referee scores attainment alongside delta PV; it never enters the payoff. Engine numbers come from the commands at the end (control-side `whatif`, no suppliers or injects, market multipliers 1.0), in $B of Airbus delta PV. Those numbers, in §2-§8, are the two-player, four-turn game (four-turn game). §9 gives the five-player game (`five-player-2045`: three rounds, three engine makers, NGSA at $20B), from Airbus-side `whatif`. Its three-round check is in §7 and its commands are in the second block.

## 1. Assigned objective

Source: assigned by control for this scenario.

```text
Primary goal:    Defend 60/40 edge; Protect A320 family
Possible moves:  Launch NGSA ($20B)
                 Do Nothing (Milk A320neo family)
                 Delay fps (supply-chain bottleneck)
                 Delay fps (talent poaching)
Enablers:        Existing A320 customer base
                 government incentives
                 cash
                 A220-500 closing the seat-size gap
Constraints:     Engineering capacity (NGSA & A350 share teams)
                 fines if delay tactics are detected
```

The slide is Boeing's reading of our goals, adopted by control (inference).

## 2. Moves to levers

| Briefing move | Game lever and how to order it | Modelled | Notes |
|---|---|---|---|
| Launch NGSA ($20B) | `{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}` in the launch year's turn | yes | 7 development years, capex $25B (not $20B) (four-turn game); **$20B in `five-player-2045`**, as in the briefing. Margin 26.28%, technology-ready year 2035. In `five-player-2045` the engine needs its maker's commitment, or it falls back (§9). |
| Do Nothing (A320neo family) | no orders | yes | Status quo: 60% share at a 13.14% margin. |
| Delay fps (supply-chain bottleneck) | `"delay_tactics": true` in that turn's orders | yes | 1 year of fps slip per turn while fps is in development, 2 at most, $0.5B a turn, exposed after 2 turns of use (in `five-player-2045`, 2 of the 3 rounds; §9.4). A turn before Boeing launches is wasted but counts toward exposure. |
| Delay fps (talent poaching) | `"poaching": true` in that turn's orders | yes | It does not slip fps. Boeing loses $0.75B a turn while developing; we pay $0.25B and save $0.4B while we have a programme in development. Turns 1-3 add $0.36B, no share change. |

Of our other levers, only the NGSA engine moves share (§5.4). An A350 Re-engine in 2033 adds $1.09B and changes no metric (four-turn game; five-player: §9.7).

## 3. Enablers and constraints

| Item | Engine parameter (rules value) | What our evidence says |
|---|---|---|
| Existing A320 customer base | `sq_share.airbus` 0.60; A320neo margin 0.1314 | The most-delivered airliner in history [A-0241]; 607 of 793 deliveries in 2025 [A-0389]; about 60% of the single-aisle backlog [A-0865, AX-0025]. |
| Government incentives | not modelled: NGSA capex fully self-funded, alpha 0.30; a capex override (§5.5) is the nearest proxy | Refundable advances and risk-sharing fund development [A-0348, A-0368]; EU Clean Aviation co-funds technology [A-0445]. Boeing says launch aid lowers our risk [A-0030, A-0127] (outside view). |
| Cash | WACC 0.08, alpha 0.30; no budget limit | Net cash €12.2bn [A-0402]; FCF €4.75bn [A-0404]; a prudent, low-leverage risk appetite [A-0343]. |
| A220-500 closing the seat-size gap | not modelled: one narrowbody segment, no A220 lever | A220 75% owned [A-0265], 25% lower fuel burn per seat [A-0239], backlog 467 [A-0240]. Boeing said it would not answer an A220-500 [A-0579] (rival intelligence). |
| Engineering capacity (NGSA and A350 share teams) | strain $3B × min(1, overlap / 5), alpha-loaded; development years NGSA 7, A350 Re-engine 5 | Talent binds new programmes and the ramp [A-0366, A-0485, A-0423]. The 2-year overlap guardrail is inference [A-0343, A-0401]. |
| Fines if Delay Tactics are detected | not a fine: after 2 turns of use, -1 pp narrowbody share for 5 years from the year after the exposing turn | DPA closed, zero fines [A-0474, A-0478]; integrity heads the 2026 CEO objectives [A-0331]; "abnormal risk" goes to the Board [A-0299]. |

## 4. How attainment is measured

| Metric id | What it measures | Target and years | Status-quo value |
|---|---|---|---|
| `nb_share_60` | Airbus narrowbody share; the worst counted year decides; `gap_pp` = worst minus 60 | at least 60% in 2040, 2045, 2050 | 60.0 each year: met, gap 0.0 |
| `protect_a320` | the same share, counted only before our NGSA enters service (`until_own_eis`) | at least 60% in 2030, 2035, 2040, 2045, 2050 | 60.0 each year: met, gap 0.0 |

- Both read the projection after the orders, with no later moves (`whatif`: `objectives` after, `objectives_now` before).
- The status quo meets both with zero margin, so any Boeing gain in a counted year breaks them.
- With NGSA EIS 2035, `protect_a320` counts 2030 only. With EIS 2036-2037 it also counts 2035.
- The share rule makes `nb_share_60` a race. The first new airplane in service captures 1.5 pp a year from EIS+1, times the engine and market multipliers and, in the wave, a weight of 0.4-1.0. Capture freezes when the follower enters service. If both enter service in the same year, 60/40 holds.

## 5. What it takes (four-turn game)

For `five-player-2045`, see §9.

### 5.1 The reference plan against each fps timing

Reference plan: NGSA 2028 on the CFM ducted engine (EIS 2035), A350 Do Nothing, no tactics. The profile's default adds Poaching (+$0.36B), and its engine rule picks GTF2 (+$1.75B, §5.4). Neither changes a metric. Among NGSA launches from 2026 to 2033, 2028 had the best PV in every row of both scenarios.

| Boeing fps launch (EIS) | Base: ΔPV, `nb_share_60` gap | Wave: ΔPV, gap | `protect_a320` |
|---|---|---|---|
| none | +46.47, +7.5 | +42.08, +3.77 | met |
| 2026 (2033) | +23.09, **-3.0** | +26.20, **-1.2** | met |
| 2027 (2034) | +25.74, **-1.5** | +27.26, **-0.6** | met |
| 2028 (2035) | +28.27, 0.0 | +28.27, 0.0 | met |
| 2029 (2036) | +30.58, +1.5 | +29.19, +0.6 | met |
| 2030 (2037) | +32.70, +3.0 | +30.10, +1.24 | met |
| 2032 (2039) | +36.38, +6.0 | +32.00, +2.8 | met |
| 2035 (2042) | +40.74, +7.5 | +34.87, +3.77 | met |

An fps Joint Venture gives the same Airbus result as Solo (tested for 2026).

### 5.2 When fps launches in 2026 or 2027

| Plan | fps 2026: base | fps 2026: wave | fps 2027: base | fps 2027: wave | Red line broken |
|---|---|---|---|---|---|
| NGSA 2028 | +23.09, -3.0 | +26.20, -1.2 | +25.74, -1.5 | +27.26, -0.6 | none |
| NGSA 2028 + one Delay Tactics turn (turn 3) | +25.42, -1.5 | +26.94, -0.6 | +27.95, met | +27.95, met | none |
| NGSA 2028 + Delay Tactics in turns 2 and 3 | +26.93, met | +26.93, met | | | 4 (exposing second turn) |
| NGSA 2027 + one Delay Tactics turn (turn 3) | +22.43, met | +22.43, met | | | 1 (EIS 2034) |
| NGSA 2027 | | | +22.74, met | +22.74, met | 1 (EIS 2034) |
| NGSA 2026 | +15.90, met | +15.90, met | | | 1 (EIS 2033) |

- **fps 2027.** One Delay Tactics turn slips fps to 2035, tying NGSA, which ends Boeing's lead and should pass the team test below (inference). It adds $2.22B in base, passing the $1B test in profile §6, but only $0.70B in the wave.
- **fps 2026.** No plan inside the red lines meets `nb_share_60`. The best in-bounds plan is NGSA 2028 with one Delay Tactics turn in base, and NGSA 2028 alone in the wave (Delay Tactics adds only $0.74B). In base that turn leaves fps first (2034 against 2035), so it fails the default team's test that Delay Tactics change who enters service first (`teams.md`) and needs an override.
- **Breaking a red line.** A second Delay Tactics turn meets the metric and adds $1.51B in base, but breaks red line 4. Against the best in-bounds plan, NGSA 2027 with Delay Tactics breaks red line 1 and costs $2.995B (base) or $3.77B (wave). NGSA 2026 costs $9.52B or $10.29B.
- **Delay Tactics timing.** Wait until the fps launch is public. Against fps 2029, a turn-1 order costs $0.50B and slips nothing; a turn-2 order adds $1.72B (base) or $0.51B (wave). We already lead fps 2029, so the team test fails there too.

**Objective premium** is the PV of the plan doctrine picks minus that of the best-PV plan that meets both metrics.

| fps launch | Base | Wave |
|---|---|---|
| none, or 2028 and later | 0 | 0 |
| 2027 | 0 (Delay Tactics gains $2.22B) | 0 in PV, but needs Delay Tactics below the $1B test |
| 2026 | not attainable within the red lines | not attainable within the red lines |

### 5.3 Boeing Rate Increase

- **Committed in turn 1.** Our 2030 share falls to 58%, so `protect_a320` fails by 2.0 pp under every Airbus plan. No Airbus capture comes before 2034 (tested with NGSA 2026). NGSA 2028 still meets `nb_share_60`: +5.5 pp at +42.45 (base), +1.77 pp at +37.78 (wave).
- **Committed in turn 2.** NGSA 2028 keeps `protect_a320` (+43.14 base). NGSA 2030 loses it, because 2035 then counts at 58%.
- **Turn-1 Rate Increase plus fps 2029.** NGSA 2028 misses `nb_share_60` by 0.5 pp (base) and 1.4 pp (wave). Turn-3 Delay Tactics fixes base (+1.0 pp; +25.81 to +27.61), not the wave (-0.76 pp).

### 5.4 NGSA engine

- **GTF2** (no added EIS years, capture 0.95) is worth +$1.75B (base) and +$1.74B (wave) over CFM ducted. It met wherever ducted met in every case tested: each fps year in §5.1, a turn-1 Rate Increase, and fps 2027 with Delay Tactics (+29.88, met in both).
- **UltraFan** adds one year. Against fps 2028 it turns a tie into a miss (-1.5 base, -0.6 wave) and costs $4.84B (base) or $3.40B (wave).
- **CFM RISE open fan** cannot enter service before 2045. NGSA 2028 on it would be ready in 2036 and waits 9 years, each costing 10% of capex.
  - Alone it scores -7.67 in both scenarios, $54.13B (base) and $49.74B (wave) below ducted. Both metrics hold only at a zero gap.
  - Against fps 2028 it turns a tie into a miss (-15.0 base, -10.08 wave), fails `protect_a320` (-7.5, -3.77) and costs $54.22B (base) or $49.46B (wave).
  - NGSA 2037 on it enters service in 2045 without waiting: +14.49 alone in both scenarios, still $31.98B (base) and $27.59B (wave) below NGSA 2028 on ducted, and outside the 2028-2030 window.

### 5.5 NGSA at the briefing's $20B

Separate runs set NGSA capex to $20B. In `five-player-2045`, $20B is the scenario's own value (§9). NGSA 2028 gains $4.48B in both scenarios (+50.94 base, +46.55 wave). No metric changes. Against fps 2026, meeting it with NGSA 2027 plus Delay Tactics now costs $2.64B (base) or $3.41B (wave). NGSA 2026 costs $8.77B or $9.55B.

### 5.6 How the result depends on Boeing's timing

The deciding variable is fps EIS against our 2035.
- **fps EIS 2035 or later** (an fps launched in 2028 or later on a ducted engine): the reference plan meets both metrics at zero premium.
- **An fps on the open fan** cannot enter service before 2045, whatever its launch year. The reference plan meets both metrics with the full no-fps margin (+7.5 base, +3.77 wave) at +43.96 (base) and +37.94 (wave). Delay Tactics only costs money there.
- **fps EIS 2034** (fps 2027, or fps 2026 on UltraFan): one Delay Tactics turn ties it (+27.95, met in both).
- **fps EIS 2033:** nothing inside the red lines closes it.
- **The wave** cuts gaps by 50-60% (60% where capture falls before 2037, at weight 0.4). Within the red lines it changes which plans meet only under a Rate Increase (inference from the share rule): turn-1 Rate Increase, fps 2029 and Delay Tactics meet in base (+1.0 pp), not in the wave (-0.76 pp). It pushes Delay Tactics below $1B and makes an early NGSA dearer.

Our prior is an fps no earlier than turn 2 (profile §7) and an early Rate Increase [A-0820]. Boeing has said "not before '35" [A-0570] and set no date [A-0822, A-0824] (rival intelligence).

## 6. Fit with our doctrine

**Where the objective agrees with revealed behaviour**
- Boeing called the neo campaign "a market share game" [A-0065]. We refine products and add variants "to maintain its market-leading position" [A-0200].
- The A320 family is the core (§3), and commercial aircraft are 72% of revenue [A-0189].
- Our NGSA clock already serves the objective: an expected engine choice around 2027 [A-0182], the generation change "around 2035" [A-0431], and EIS "around 2037" [A-0409]. NGSA 2028 meets both metrics unless fps launches before 2028 or Boeing commits a Rate Increase in turn 1.
- With the neo we moved first and kept a head start [A-0246, A-0032, A-0110].

**Where it pulls against revealed behaviour**
- Pay rests on EBIT, FCF and EPS, not share [A-0310, A-0334, A-0311]. Any objective premium comes out of what management is paid on.
- Technology gates set our timing [A-0225, A-0441], and we wait when the ecosystem is not ready [A-0413, AX-0006]. The objective rewards matching Boeing's EIS, which hard rule 1 and hard rule 2 (itself inference) forbid.
- Integrity comes first [AX-0073] (see §3). With NGSA EIS 2035, the objective rewards a second Delay Tactics turn, because the exposure penalty misses every counted year (four-turn game). In `five-player-2045` the penalty lands in 2040 or 2050, so a second round fails the objective too (§9.4).
- The open fan is a documented focus [A-0226, A-0444], but in the game it cannot enter service before 2045. That breaks hard rule 8 (no NGSA EIS after 2037) and hands the race to any earlier fps (§5.4).
- We hold about 60% of the backlog [AX-0025] and are ramping to rate 75 [A-0431]; that we defend share by ramping rather than launching is inference. The engine has no Airbus rate lever.

**Weighing rule**
1. The objective sets what we aim for. The doctrine sets how we get there.
2. Never break a hard rule or red line for the objective, including rule 1 (NGSA EIS at or after the technology-ready year) and rule 4 (one Delay Tactics turn, never the exposing second). The five pillars cannot be overridden [AX-0073].
3. The objective premium counts against the $3B doctrine-premium cap (profile §9 step 6): on one decision, the two together may not exceed $3B. Overriding a failed team test still needs at least $1B and a Board item, once per game at most (`teams.md`).
4. Among options within $1B of the best survivor, prefer the one meeting more metrics, unless it adds a Board item or a covert lever (inference).
5. The objective does not lower the $1B Delay Tactics test (inference). In the wave against fps 2027, keep Delay Tactics off. Log the -0.6 pp miss and a $0.70B doctrine premium (four-turn game). In `five-player-2045` the miss is -0.55 pp and the premium up to $0.63B (§9.3).

## 7. Per-turn objective check

**Per-turn check (four-turn game).** Insert between profile §9 step 5 (pick the highest-PV survivor) and step 6 (doctrine premium):

1. **Before.** Run `whatif` with no Airbus orders against Boeing's public moves. Log `nb_share_60` and `protect_a320` (met, values, `gap_pp`).
2. **After, plus the threat case.** Run `whatif` for the chosen orders, then against the earliest fps still open to Boeing plus any uncommitted Rate Increase. Log both.
3. **Repair within the red lines.** If a metric fails, try:
   - NGSA 2028, if not yet launched;
   - one Delay Tactics turn, once the fps is public and in development, if it gains at least $1B and (default team) changes who enters service first;
   - a ducted or GTF2 engine, never the open fan. With no entry before 2045, the open fan missed `nb_share_60` in every case tested against a ducted fps (2028-2035) or a turn-1 Rate Increase, including the Rate Increase alone (-2.0 pp) and fps 2032 under it (-11.0 base, -9.28 wave), where ducted met.

   Objective premium = PV of the best survivor minus PV of the best survivor that meets.
4. **Weigh.** Pay the premium only if it plus any doctrine premium is $3B or less. Otherwise accept the miss.
5. **Log** in the rationale: "Objectives: `nb_share_60` before → after (gap); `protect_a320` before → after; objective premium $Z B; doctrine premium $W B; blocking red line N."

**Per-round check (five-player-2045).** Insert it at the same point, once per round. Put the engine makers' public commitments in every `whatif` JSON.

1. **Before.** Run `whatif` with no Airbus orders against the public moves of Boeing and the engine makers. Log both metrics.
2. **After, plus the threat case.** Run the chosen orders twice: once with your NGSA engine committed, once with it fallen back to the LEAP derivative. Then add the round's threat case:
   - **Round 1:** fps 2026 with a 7-year and a 10-year ramp-up, plus a round-1 Rate Increase. Snapshot for NGSA 2028: -1.10 and -0.77, and -3.10 and -2.77 with the Rate Increase, which also fails `protect_a320` by 2.0.
   - **Round 2:** the earliest fps still open (2031, EIS 2038), plus any uncommitted Rate Increase. Snapshot: met at +1.78 to +1.84 alone, -0.16 to -0.22 with a Rate Increase.
   - **Round 3:** fps 2036 (EIS 2043), plus any uncommitted Rate Increase. Both are met. With NGSA EIS 2035, `protect_a320` is settled after round 1 because only 2030 counts, so only `nb_share_60` can still move.
3. **Repair within the red lines.**
   - **Round 1:** NGSA 2028, requesting the best-PV engine whose maker can commit in time (UltraFan by 2028, GTF2 by 2029), never the open fan. No Delay Tactics: the order is blind.
   - **Rounds 2 and 3:** one Delay Tactics round against a public fps in development, if it gains at least $1B and (default team) changes who enters service first. No case tested reached $1B (§9.4), so expect to log the miss.
   - **Never a second Delay Tactics round.** Its exposure now lands in 2040 or 2050 (§9.4).

   The objective premium is defined as in step 3 above.
4. **Weigh** as in step 4 above.
5. **Log** as in step 5 above, adding "engine requested → flown".

## 8. Gaps and modelling limits

- **A220-500, incentives, ramp.** Not modelled (§3, §6). With no Airbus rate lever, `protect_a320` turns on Boeing's Rate Increase timing.
- **"Fines".** A share penalty, not money. From turns 2 and 3 it falls in 2035-2039, which no counted year sees when NGSA EIS is 2035.
- **NGSA capex.** $25B is a placeholder (base narrative); §5.5 tests $20B (four-turn game). `five-player-2045` uses the briefing's $20B.
- **Replacement wave.** It applies one capture weight to both sides. The slide's mix (about 73% Airbus types) is not modelled.
- **Five-year marks.** Dips between counted years are invisible.
- **Untested.** Injects, market multipliers, supplier players (GTF2 or UltraFan may fall back to CFM). Ties have zero capture, so they should survive any multiplier; Rate Increase cases may not (inference) (four-turn game). §9 now tests the supplier players. Injects and market multipliers remain untested, including the UltraFan and next-generation GTF test setbacks. Those would slip a committed NGSA engine by two years: to 2037 for UltraFan committed in 2028 (inference).
- **Evidence.** Our voice is one document; the share framing is mostly Boeing's [A-0065] (profile §10).

## 9. What it takes in the five-player game (five-player-2045)

**Source.** Airbus-side `whatif` on a scratch run of `five-player-2045` with Rolls-Royce, Pratt & Whitney and CFM/GE as players, no injects and market multipliers of 1.0 (second commands block). All numbers are **snapshots** from 2026-10-05, in $B of Airbus delta PV. The run was deleted afterwards.

**Engine states.** Two NGSA engine states run throughout:
- **LEAP**: no maker commits, so the request falls back to `cfm_leap_plus`;
- **UltraFan**: Rolls-Royce commits `uf_nb` in 2028 on standard terms.

Boeing's fps flies the LEAP derivative unless a row says otherwise.

### 9.1 What is different in this scenario

- **Unchanged:** the objective, metrics and counted years (§1, §4).
- **NGSA costs $20B**, as in the briefing (`assigned_objectives`).
- **Rounds:** 2026-2030, 2031-2035 and 2036-2045. The status quo still meets both metrics at zero gap.
- **Capture multipliers:** CFM ducted 1.0, UltraFan and GTF2 0.95, the LEAP derivative 0.92. With no Boeing move, NGSA 2028 therefore leads by +3.77 pp, +3.58 pp or +3.47 pp.
- **Delay Tactics exposure** comes after two rounds of use. It costs -1 pp of share for five years from the year after the exposing round: 2036-2040 after round 2, 2046-2050 after round 3. Both windows contain a counted year.

### 9.2 The reference plan against each fps timing

The reference plan is NGSA 2028, A350 Do Nothing and no tactics. With no Boeing move, 2028 was the best NGSA year from 2026 to 2038 in both engine states: +46.55 with CFM ducted committed, +41.48 on LEAP (profile §11.2).

| Boeing fps launch (EIS) | LEAP: ΔPV, `nb_share_60` gap | UltraFan: ΔPV, gap | `protect_a320` |
|---|---|---|---|
| none | +41.48, +3.47 | +50.47, +3.58 | met |
| 2026 (2033) | +27.05, **-1.10** | +34.62, **-1.10** | met |
| 2027 (2034) | +27.99, **-0.55** | +35.63, **-0.55** | met |
| 2028 (2035) | +28.89, 0.0 | +36.60, 0.0 | met |
| 2029 (2036) | +29.71, +0.55 | +37.51, +0.57 | met |
| 2030 (2037) | +30.51, +1.14 | +38.40, +1.18 | met |
| 2031 (2038) | +31.30, +1.78 | +39.28, +1.84 | met |
| 2033 (2040) | +33.11, +3.47 | +41.30, +3.58 | met |
| 2036 (2043) | +35.67, +3.47 | +44.15, +3.58 | met |

- **When Boeing leads, Boeing's engine sets the gap.**
  - With CFM's ducted engine on both airframes: fps 2026 -1.20, fps 2027 -0.60 (at +30.67 and +31.73).
  - fps 2026 on GTF2 or UltraFan: -1.14.
- **fps with a 10-year ramp-up:** fps 2026 -0.77, fps 2027 -0.39.
- **An fps Joint Venture** gives the same Airbus result as Solo (fps 2026).
- **An fps on the open fan**, with CFM committed, enters service in 2045: +37.45, gap +3.47.

### 9.3 When fps launches in 2026 or 2027

| Plan | fps 2026: LEAP | fps 2026: UltraFan | fps 2027: LEAP | fps 2027: UltraFan | Red line broken |
|---|---|---|---|---|---|
| NGSA 2028 | +27.05, -1.10 | +34.62, -1.10 | +27.99, -0.55 | +35.63, -0.55 | none |
| + Delay Tactics in round 1 | +27.49, -0.55 | +35.13, -0.55 | +28.39, met | +36.10, met | none |
| + Delay Tactics in round 2 | +27.65, -0.55 | +35.29, -0.55 | +28.55, met | +36.26, met | none |
| + Delay Tactics in rounds 1 and 2 | +27.49, -1.00 | +35.16, -1.00 | +28.31, -0.45 | +36.07, -0.43 | 4 (exposing round) |
| NGSA 2027 + Delay Tactics in round 2 | +23.02, met | +31.45, met | | | 1 (EIS 2034) |
| NGSA 2027 | +22.46, -0.55 | +30.81, -0.55 | +23.36, met | +31.79, met | 1 (EIS 2034) |
| NGSA 2026 | +16.53, met | +25.72, met | | | 1 (EIS 2033) |

- **fps 2027.** One Delay Tactics round slips the fps to 2035 and ties NGSA.
  - It adds $0.40B in round 1 or $0.56B in round 2 on LEAP, and $0.47B or $0.63B on UltraFan. Every case is below the profile's $1B test.
  - A round-1 order is also blind, because the fps is not yet public when we order.
  - Weighing rule 5 keeps Delay Tactics off. Log the -0.55 pp miss and a doctrine premium of up to $0.63B.
- **fps 2026.** Nothing inside the red lines meets the metric; one round of Delay Tactics only halves the gap.
  - The cheapest plan that meets is NGSA 2027 with Delay Tactics in round 2. It breaks red line 1 and costs $4.03B (LEAP) or $3.17B (UltraFan) against NGSA 2028, above the $3B cap.
  - NGSA 2026 costs $10.52B or $8.90B.
- **Two rounds of Delay Tactics no longer meet the metric.** The exposure from round 2 lands in 2040 (59.0% against fps 2026). In the four-turn game it missed every counted year (§6).

| fps launch | Objective premium (five-player) |
|---|---|
| none, or 2028 and later | 0 |
| 2027 | 0 in PV, but needs Delay Tactics below the $1B test |
| 2026 | not attainable within the red lines |

### 9.4 Delay Tactics and Poaching across three rounds

Gain from one round of Delay Tactics over NGSA 2028 alone:

| Boeing fps (engine state) | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| 2026 (LEAP) | +0.44 | +0.60 | |
| 2027 (LEAP) | +0.40 | +0.56 | |
| 2029 (LEAP) | +0.30 | +0.46 | -0.23 (fps in service) |
| 2030 (LEAP) | +0.29 | +0.45 | +0.56 |
| 2031 (LEAP) | -0.50 (no fps yet) | +0.56 | +0.66 |
| 2033 (LEAP) | -0.50 (no fps yet) | +0.47 | +0.58 |
| 2036 (UltraFan) | | | +0.82 |
| 2031 plus a Rate Increase (UltraFan) | | +0.65 | +0.76 |

- **One round gains $0.29-0.82B, never $1B.** A round with no fps in development wastes the $0.5B cost and still counts toward exposure.
- **A second round exposes the tactic.**

  | Plan | Against fps 2026 | Against fps 2027 (LEAP) |
  |---|---|---|
  | One round | -0.55 | met |
  | Rounds 1 and 2 (penalty in 2040) | -1.00 | -0.45 |
  | Rounds 2 and 3 (penalty in 2050) | -1.55 | -1.00 |

- **Poaching** adds +0.15 in round 1 and +0.10 in round 2, while NGSA is in development (2028-2034). In round 3 it is about -0.1, unless the A350 Re-engine is in development (+0.07 with a 2035 launch). It never moves share.

### 9.5 Boeing Rate Increase

- **Round 1.** Our 2030 share falls to 58%, so `protect_a320` fails by 2.0 pp under every plan, NGSA 2026 included. NGSA 2028 still meets `nb_share_60`: +1.47 at +37.20 (LEAP), +1.58 at +46.00 (UltraFan).
- **Round 2.** NGSA 2028 keeps `protect_a320` (+38.27 LEAP, +47.07 UltraFan). NGSA 2029 (+34.98) and NGSA 2030 (+31.91) lose it, because 2035 then counts at 58%.
- **Round 3.** Both metrics are met (+1.47 LEAP, +1.58 UltraFan).
- **A Rate Increase plus an fps:**
  - **fps 2029 with a round-1 Rate Increase:** -1.45 (LEAP), -1.43 (UltraFan). Delay Tactics in round 2 leaves -0.86 and -0.82.
  - **fps 2031 with a Rate Increase in round 1 or 2:** -0.22 (LEAP), -0.16 (UltraFan). One Delay Tactics round, in round 2 or 3, meets the metric on UltraFan (+0.66) but adds only $0.65-0.76B.
  - **fps 2032 or 2033 with a round-1 Rate Increase:** met (fps 2032: +0.66 on UltraFan; fps 2033: +1.47 LEAP, +1.58 UltraFan).
- **Boeing's round-1 best response in `options`** is fps 2026 Solo with a 10-year ramp-up, plus a Rate Increase.
  - NGSA 2028 scores +22.96 (LEAP) or +30.32 (UltraFan), with `nb_share_60` at -2.77 and `protect_a320` at -2.0.
  - Delay Tactics in round 2 leaves -2.39 (+0.36).

### 9.6 NGSA engine

| NGSA 2028 request | Committed on time (standard / aggressive) | Late commitment | No commitment |
|---|---|---|---|
| UltraFan (Rolls-Royce by 2028, or its Joint Venture by 2029) | +50.47 / +55.71 | 2029: +43.72 (EIS 2036); 2030: +37.44 (EIS 2037) | CFM ducted if CFM committed (+46.55), else LEAP (+41.48) |
| GTF2 (Pratt & Whitney by 2029) | +48.29 / +53.09 | 2030: +41.72 (EIS 2036) | same chain |
| CFM ducted (by 2028) | +46.55 / +52.69 | 2029: +40.15; 2030: +34.16 | LEAP +41.48 |
| Open fan (CFM/GE) | -0.83 (EIS 2045) | | LEAP +41.48 |

- **The engine moves PV more than the metrics.**
  - It changes the gap only where we lead (+3.47 to +3.77). It turned no miss into a met in the cases tested.
  - A late commitment that moves EIS past 2035 also brings 2035 into `protect_a320`. That is harmless alone, but under a round-2 Rate Increase it would fail like NGSA 2029 (inference; not run).
- **The open fan** misses wherever Boeing moves first:
  - NGSA 2028 on it, with CFM committed, meets only at zero gap with no Boeing move.
  - Against fps 2028 it scores -9.27 with `protect_a320` at -3.47 (ΔPV -13.68). Against fps 2032 it scores -6.69.
  - Against a round-1 Rate Increase both metrics fail by 2.0.
  - NGSA 2037 on it scores +16.89 (+17.97 with CFM's emissions lobbying), and -6.69 against fps 2032.

### 9.7 A350 Re-engine and the whole plan

- **The A350 Re-engine changes no metric.** Gains over NGSA 2028 alone (LEAP, +41.48):
  - **On UltraFan, with Rolls-Royce committed a year earlier:** 2033 +1.08, 2034 +1.30, 2035 +1.49 (+2.15 on aggressive terms), 2036 +1.28, 2037 +1.09.
  - **On the GEnx upgrade (no commitment):** 2033 +0.75, 2035 +1.22, 2036 +1.04, 2038 +0.71.
  - **Rolls-Royce committing in our launch year** forces a one-year wait: 2033 +0.42, 2035 +0.92.
  - **After a 787 Re-engine:** -0.81 to -2.17.
- **The whole plan** (NGSA 2028 on UltraFan, Poaching in rounds 1-2, A350 Re-engine 2035) scores +52.22 and meets both metrics (+3.58). If every engine request falls back, it scores +42.95 (+3.47).

### 9.8 How the result depends on Boeing and the engine makers

- **The deciding variable is still fps EIS against our 2035.**
  - fps 2028 or later: the reference plan meets both metrics at zero premium.
  - fps 2027: one Delay Tactics round ties it, below $1B.
  - fps 2026: nothing inside the red lines closes the gap.
  - The open fan cannot enter service before 2045, so an fps on it leaves us the full lead.
- **A Rate Increase stretches the threat into round 2.** fps 2031 then misses by 0.16-0.22 pp, against a +1.78-1.84 lead without it.
- **The engine makers move PV, not the metrics.**
  - UltraFan committed is worth $8.99B more than no commitment.
  - Aggressive terms add $4.8-6.1B.
  - A 2030 commitment is worth less than none.

<details>
<summary>Commands (four-turn game)</summary>

```bash
cd /home/user/aero-engine-gameboard
# runs snapshot their config at `new`; the open fan numbers (5.4, 5.6, 6, 7) come from runs created after its 2045 date
export WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/of_update/airbus
mkdir -p $WARGAME_RUNS_DIR
python3 -m wargame.engine new --run-id ab-base --scenario base
python3 -m wargame.engine new --run-id ab-wave --scenario replacement-wave
python3 -m wargame.engine new --run-id ab-ngsa20 --scenario base --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
python3 -m wargame.engine new --run-id ab-wave-ngsa20 --scenario replacement-wave --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
python3 -m wargame.engine rules --run ab-base --side airbus
python3 -m wargame.engine rules --run ab-wave --side airbus
python3 -m wargame.engine rules --run ab-ngsa20 --side airbus
python3 -m wargame.engine rules --scenario base --side control
python3 -m wargame.engine rules --scenario replacement-wave --side control
python3 -m wargame.engine scenarios   # base narrative: placeholder programme costs (8)

# best NGSA year per fps year (5.1). The wave_grid.txt row used (fps 2026 / NGSA 2026: +15.90 in both scenarios) is reproduced below.
t() { if [ $1 -le 2028 ]; then echo 1; elif [ $1 -le 2031 ]; then echo 2; elif [ $1 -le 2034 ]; then echo 3; else echo 4; fi; }
for r in ab-base ab-wave; do for f in none 2026 2027 2028 2029 2030 2032 2035; do for n in 2026 2027 2028 2029 2030 2031 2032 2033; do
  B=""; [ $f != none ] && B="\"boeing\":{\"$(t $f)\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"year\":$f}]}},"
  echo "{$B\"airbus\":{\"$(t $n)\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"cfm_ducted\",\"year\":$n}]}}}" \
  | python3 -m wargame.engine whatif --run $r --side control \
  | python3 -c "import json,sys; o=json.load(sys.stdin); print('$r','$f','$n',o['airbus']['delta_pv_b'])"
done; done; done | sort -k1,1 -k2,2 -k4,4gr | awk '!seen[$1" "$2]++'

# single plans (runs: base and wave unless stated)
wi() { for r in $1; do echo "$2" | python3 -m wargame.engine whatif --run $r --side control; done; }
W="ab-base ab-wave"; W20="ab-ngsa20 ab-wave-ngsa20"
wi "$W" '{"airbus":{"1":{"launch":[]}}}'
wi "$W $W20" '{"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
for f in 2026:1 2027:1 2028:1 2029:2 2030:2 2032:3 2035:4; do wi "$W" "{\"boeing\":{\"${f#*:}\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"year\":${f%:*}}]}},\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"cfm_ducted\",\"year\":2028}]}}}"; done
wi "$W20" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}],"delay_tactics":true}}}'
wi "$W $W20" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"delay_tactics":true}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"2":{"delay_tactics":true},"3":{"delay_tactics":true}}}'
wi "$W $W20" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2027}]},"3":{"delay_tactics":true}}}'
wi "$W $W20" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2026}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2027}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"delay_tactics":true}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2027}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2027}]}}}'
wi "$W" '{"boeing":{"2":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2029}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}],"delay_tactics":true}}}'
wi "$W" '{"boeing":{"2":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2029}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"2":{"delay_tactics":true}}}'
wi "$W" '{"boeing":{"1":{"rate_increase":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"boeing":{"2":{"rate_increase":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"boeing":{"2":{"rate_increase":true}},"airbus":{"2":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2030}]}}}'
wi "$W" '{"boeing":{"2":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2029}]},"1":{"rate_increase":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"boeing":{"2":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2029}]},"1":{"rate_increase":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"delay_tactics":true}}}'
wi "$W" '{"airbus":{"1":{"launch":[{"program":"ngsa","engine":"pw_gtf2","year":2028}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2027}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"pw_gtf2","year":2028}]},"3":{"delay_tactics":true}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2028}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_open_fan","year":2028}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2028}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"rr_ultrafan_nb","year":2028}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_open_fan","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"delay_tactics":true}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"jv","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}],"poaching":true},"2":{"poaching":true},"3":{"poaching":true}}}'
wi "$W" '{"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"launch":[{"program":"rea350","engine":"rr_ultrafan_wb","year":2033}]}}}'
# added in fact-check: Rate Increase with NGSA 2026 (5.3); GTF2 against each fps year and with a Rate Increase (5.4); engine choice under a Rate Increase (7)
wi "$W" '{"boeing":{"1":{"rate_increase":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2026}]}}}'
for f in 2026:1 2027:1 2028:1 2029:2 2030:2 2032:3 2035:4; do wi "$W" "{\"boeing\":{\"${f#*:}\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"year\":${f%:*}}]}},\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"pw_gtf2\",\"year\":2028}]}}}"; done
for e in cfm_ducted pw_gtf2 cfm_open_fan; do
  wi "$W" "{\"boeing\":{\"1\":{\"rate_increase\":true}},\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"$e\",\"year\":2028}]}}}"
  for f in 2030:2 2032:3; do wi "$W" "{\"boeing\":{\"1\":{\"rate_increase\":true},\"${f#*:}\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"year\":${f%:*}}]}},\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"$e\",\"year\":2028}]}}}"; done
done
# added for the open fan's 2045 date: the open fan alone, at 2028 and 2037, against later ducted fps years; an fps on the open fan or UltraFan (5.4, 5.6)
for e in cfm_ducted pw_gtf2 cfm_open_fan rr_ultrafan_nb; do wi "$W" "{\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"$e\",\"year\":2028}]}}}"; done
wi "$W" '{"airbus":{"4":{"launch":[{"program":"ngsa","engine":"cfm_open_fan","year":2037}]}}}'
for f in 2029:2 2032:3 2035:4; do for n in 1:2028 4:2037; do wi "$W" "{\"boeing\":{\"${f#*:}\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"year\":${f%:*}}]}},\"airbus\":{\"${n%:*}\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"cfm_open_fan\",\"year\":${n#*:}}]}}}"; done; done
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_open_fan","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}}}'
wi "$W" '{"boeing":{"1":{"launch":[{"program":"fps","engine":"rr_ultrafan_nb","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"3":{"delay_tactics":true}}}'
```

</details>

<details>
<summary>Commands (five-player-2045, §9 and profile §11)</summary>

```bash
cd /home/user/aero-engine-gameboard
python3 -m wargame.engine new --scenario five-player-2045 --suppliers rolls_royce,pratt_whitney,cfm --run-id airbus-5p-scratch --force
python3 -m wargame.engine inject --run airbus-5p-scratch --none
python3 -m wargame.engine rules --scenario five-player-2045 --suppliers rolls_royce,pratt_whitney,cfm --side airbus
python3 -m wargame.engine options --run airbus-5p-scratch --side airbus --compact   # Boeing's best response B14 (9.5)
# whatif keys are rounds (1 = 2026-30, 2 = 2031-35, 3 = 2036-45); engine makers' orders go in the same JSON
r() { if [ $1 -le 2030 ]; then echo 1; elif [ $1 -le 2035 ]; then echo 2; else echo 3; fi; }
wi() { echo "$1" | python3 -m wargame.engine whatif --run airbus-5p-scratch --side airbus; }
NG='"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]'        # LEAP state: nobody commits
UF='"launch":[{"program":"ngsa","engine":"rr_ultrafan_nb","year":2028}]'
RR='"rolls_royce":{"1":{"launch":[{"program":"uf_nb","variant":"solo","year":2028}]}}'
# NGSA year with and without CFM committing in the same year (9.2; profile 11.2)
for n in $(seq 2026 2038); do L="\"launch\":[{\"program\":\"ngsa\",\"engine\":\"cfm_ducted\",\"year\":$n}]"
  wi "{\"airbus\":{\"$(r $n)\":{$L}}}"
  wi "{\"cfm\":{\"$(r $n)\":{\"launch\":[{\"program\":\"ducted\",\"year\":$n}]}},\"airbus\":{\"$(r $n)\":{$L}}}"; done
# fps years against both engine states (9.2); variants: "ramp":"10y", "variant":"jv", "engine":"pw_gtf2" (+ PW gtf_next), "cfm_open_fan" (+ CFM open_fan)
for f in 2026 2027 2028 2029 2030 2031 2033 2036; do
  B="\"boeing\":{\"$(r $f)\":{\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"ramp\":\"7y\",\"year\":$f}]}}"
  wi "{$B,\"airbus\":{\"1\":{$NG}}}"; wi "{$B,$RR,\"airbus\":{\"1\":{$UF}}}"
  # Delay Tactics in round k (9.3, 9.4): add ,"k":{"delay_tactics":true} to "airbus"; rounds 1+2 and 2+3 for exposure
  for k in 1 2 3; do wi "{$B,\"airbus\":{\"1\":{$NG},\"$k\":{\"delay_tactics\":true}}}"; done; done
# NGSA 2027 / 2026 against fps 2026-2027 (9.3), e.g.
wi '{"boeing":{"1":{"launch":[{"program":"fps","engine":"cfm_ducted","variant":"solo","year":2026}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2027}]},"2":{"delay_tactics":true}}}'
# engine requests and commitment years (9.6): uf_nb solo/jv_pw (+ PW join_rr_jv), gtf_next, ducted, open_fan; "terms":"aggressive"
for y in 2026 2027 2028 2029 2030; do
  wi "{\"rolls_royce\":{\"1\":{\"launch\":[{\"program\":\"uf_nb\",\"variant\":\"solo\",\"year\":$y}]}},\"airbus\":{\"1\":{$UF}}}"
  wi "{\"pratt_whitney\":{\"1\":{\"launch\":[{\"program\":\"gtf_next\",\"year\":$y}]}},\"airbus\":{\"1\":{\"launch\":[{\"program\":\"ngsa\",\"engine\":\"pw_gtf2\",\"year\":2028}]}}}"
  wi "{\"cfm\":{\"1\":{\"launch\":[{\"program\":\"ducted\",\"year\":$y}]}},\"airbus\":{\"1\":{$NG}}}"; done
wi '{"rolls_royce":{"1":{"launch":[{"program":"uf_nb","variant":"jv_pw","year":2029}]}},"pratt_whitney":{"1":{"join_rr_jv":true}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"rr_ultrafan_nb","year":2028}]}}}'
wi '{"cfm":{"1":{"launch":[{"program":"open_fan","year":2028}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_open_fan","year":2028}]}}}'
wi '{"cfm":{"3":{"launch":[{"program":"open_fan","year":2036}],"lobby_emissions":true}},"airbus":{"3":{"launch":[{"program":"ngsa","engine":"cfm_open_fan","year":2037}]}}}'
# Rate Increase (9.5): "boeing":{"<round>":{"rate_increase":true}}, alone, with NGSA 2026/2028/2029/2030, with fps 2029/2031/2032/2033, with "2" or "3" Delay Tactics
wi "{\"boeing\":{\"1\":{\"rate_increase\":true,\"launch\":[{\"program\":\"fps\",\"engine\":\"cfm_ducted\",\"variant\":\"solo\",\"ramp\":\"10y\",\"year\":2026}]}},$RR,\"airbus\":{\"1\":{$UF}}}"
# A350 Re-engine (9.7): year Y on rr_ultrafan_wb with Rolls-Royce uf_wb in year C (C = Y-1, Y, none), or ge_genx_next; with Boeing re787
wi "{\"airbus\":{\"1\":{$UF,\"poaching\":true},\"2\":{\"poaching\":true,\"launch\":[{\"program\":\"rea350\",\"engine\":\"rr_ultrafan_wb\",\"year\":2035}]}},\"rolls_royce\":{\"1\":{\"launch\":[{\"program\":\"uf_nb\",\"variant\":\"solo\",\"year\":2028}]},\"2\":{\"launch\":[{\"program\":\"uf_wb\",\"year\":2034}]}}}"
wi '{"boeing":{"1":{"launch":[{"program":"re787","engine":"ge_genx_next","year":2028}]}},"airbus":{"1":{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]},"2":{"launch":[{"program":"rea350","engine":"rr_ultrafan_wb","year":2033}]}},"rolls_royce":{"2":{"launch":[{"program":"uf_wb","year":2032}]}}}'
# engine-maker moves with no Airbus effect (profile 11.3): t1000_upgrade, gtf_upgrade, leap_upgrade, genx_upgrade, embraer_partner, lobby_emissions
rm -rf wargame/runs/airbus-5p-scratch
```

</details>
