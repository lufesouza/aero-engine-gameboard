# Airbus: assigned objectives

This brief covers Airbus's assigned mission, how the engine scores it and what it costs. The referee scores attainment alongside delta PV; it never enters the payoff. Engine numbers come from the commands at the end (control-side `whatif`, no suppliers or injects, market multipliers 1.0), in $B of Airbus delta PV.

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
| Launch NGSA ($20B) | `{"launch":[{"program":"ngsa","engine":"cfm_ducted","year":2028}]}` in the launch year's turn | yes | 7 development years, capex $25B (not $20B), margin 26.28%, technology-ready year 2035. |
| Do Nothing (A320neo family) | no orders | yes | Status quo: 60% share at a 13.14% margin. |
| Delay fps (supply-chain bottleneck) | `"delay_tactics": true` in that turn's orders | yes | 1 year of fps slip per turn while fps is in development, 2 at most, $0.5B a turn, exposed after 2 turns of use. A turn before Boeing launches is wasted but counts toward exposure. |
| Delay fps (talent poaching) | `"poaching": true` in that turn's orders | yes | It does not slip fps. Boeing loses $0.75B a turn while developing; we pay $0.25B and save $0.4B while we have a programme in development. Turns 1-3 add $0.36B, no share change. |

Of our other levers, only the NGSA engine moves share (§5.4). An A350 Re-engine in 2033 adds $1.09B and changes no metric.

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

## 5. What it takes

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
- **CFM RISE open fan and UltraFan** add one year each. Against fps 2028 they turn a tie into a miss (-1.5 base, -0.6 wave) and cost $3.13B or $4.84B (base) and $1.66B or $3.40B (wave).

### 5.5 NGSA at the briefing's $20B

Separate runs set NGSA capex to $20B. NGSA 2028 gains $4.48B in both scenarios (+50.94 base, +46.55 wave). No metric changes. Against fps 2026, meeting it with NGSA 2027 plus Delay Tactics now costs $2.64B (base) or $3.41B (wave). NGSA 2026 costs $8.77B or $9.55B.

### 5.6 How the result depends on Boeing's timing

The deciding variable is fps EIS against our 2035.
- **fps EIS 2035 or later** (an fps launched in 2028 or later on a ducted engine): the reference plan meets both metrics at zero premium.
- **fps EIS 2034** (fps 2027, or fps 2026 on an open fan): one Delay Tactics turn ties it (+27.95, met in both).
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
- Integrity comes first [AX-0073] (see §3). With NGSA EIS 2035, the objective rewards a second Delay Tactics turn, because the exposure penalty misses every counted year.
- The open fan is a documented focus [A-0226, A-0444], but its extra EIS year can lose a tie.
- We hold about 60% of the backlog [AX-0025] and are ramping to rate 75 [A-0431]; that we defend share by ramping rather than launching is inference. The engine has no Airbus rate lever.

**Weighing rule**
1. The objective sets what we aim for. The doctrine sets how we get there.
2. Never break a hard rule or red line for the objective, including rule 1 (NGSA EIS at or after the technology-ready year) and rule 4 (one Delay Tactics turn, never the exposing second). The five pillars cannot be overridden [AX-0073].
3. The objective premium counts against the $3B doctrine-premium cap (profile §9 step 6): on one decision, the two together may not exceed $3B. Overriding a failed team test still needs at least $1B and a Board item, once per game at most (`teams.md`).
4. Among options within $1B of the best survivor, prefer the one meeting more metrics, unless it adds a Board item or a covert lever (inference).
5. The objective does not lower the $1B Delay Tactics test (inference). In the wave against fps 2027, keep Delay Tactics off. Log the -0.6 pp miss and a $0.70B doctrine premium.

## 7. Per-turn objective check

Insert between profile §9 step 5 (pick the highest-PV survivor) and step 6 (doctrine premium):

1. **Before.** Run `whatif` with no Airbus orders against Boeing's public moves. Log `nb_share_60` and `protect_a320` (met, values, `gap_pp`).
2. **After, plus the threat case.** Run `whatif` for the chosen orders, then against the earliest fps still open to Boeing plus any uncommitted Rate Increase. Log both.
3. **Repair within the red lines.** If a metric fails, try:
   - NGSA 2028, if not yet launched;
   - one Delay Tactics turn, once the fps is public and in development, if it gains at least $1B and (default team) changes who enters service first;
   - a ducted or GTF2 engine while fps EIS could be 2035, or later under a turn-1 Rate Increase (then an open fan missed where ducted met: fps 2030 base, fps 2032 wave).

   Objective premium = PV of the best survivor minus PV of the best survivor that meets.
4. **Weigh.** Pay the premium only if it plus any doctrine premium is $3B or less. Otherwise accept the miss.
5. **Log** in the rationale: "Objectives: `nb_share_60` before → after (gap); `protect_a320` before → after; objective premium $Z B; doctrine premium $W B; blocking red line N."

## 8. Gaps and modelling limits

- **A220-500, incentives, ramp.** Not modelled (§3, §6). With no Airbus rate lever, `protect_a320` turns on Boeing's Rate Increase timing.
- **"Fines".** A share penalty, not money. From turns 2 and 3 it falls in 2035-2039, which no counted year sees when NGSA EIS is 2035.
- **NGSA capex.** $25B is a placeholder (base narrative); §5.5 tests $20B.
- **Replacement wave.** It applies one capture weight to both sides. The slide's mix (about 73% Airbus types) is not modelled.
- **Five-year marks.** Dips between counted years are invisible.
- **Untested.** Injects, market multipliers, supplier players (GTF2 or UltraFan may fall back to CFM). Ties have zero capture, so they should survive any multiplier; Rate Increase cases may not (inference).
- **Evidence.** Our voice is one document; the share framing is mostly Boeing's [A-0065] (profile §10).

<details>
<summary>Commands</summary>

```bash
cd /home/user/aero-engine-gameboard
export WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/runs_airbus_verify
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
```

</details>
