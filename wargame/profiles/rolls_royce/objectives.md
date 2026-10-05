# Rolls-Royce: assigned objectives brief (supplier `rolls_royce`)

Numbers are $B of full-game delta PV for Rolls-Royce (RR) unless named, from `whatif --side control` on runs `rrv-base` and `rrv-wave` (replacement-wave), both engine makers playing. Engine values print to 3 decimals and are rounded half up. "Selected" means an airframer picks our engine and RR launched it by the end of that turn. §2-§8 were written for the four-turn game (four-turn game: turns 2026-28 … 2035-37, P&W the only other engine maker); §9 covers the five-player game (five-player-2045).

## 1. Assigned objective

Source: assigned by control for this scenario.

> **Primary goal:** Enter narrowbody market; Keep Widebody dominance
> **Possible moves:** Ultrafan widebody only (no NB entry) · Ultrafan narrowbody solo · Joint Venture with Pratt & Whitney · Do Nothing (continue Trent only)
> **Enablers:** Free cash from widebody · reputation · airframer support for a 3rd engine maker
> **Constraints:** Engineering resources shared with widebody · no NB MR&O scale · gearbox sizing

Scored beside delta PV, never in the payoff.

## 2. Moves to levers

All checked against `rules --run <run> --side rolls_royce` (same in both scenarios).

| Briefing move | Game lever and how to order it | Modelled | Notes |
|---|---|---|---|
| UltraFan widebody only | `{"launch": [{"program": "uf_wb", "terms": "standard", "year": Y}]}`: 6 years, $3.1B, $8.0M an engine | yes | Earns only if an A350 or 787 Re-engine selects it. An A350 Re-engine falls back to GE unless `uf_wb` is launched that turn. |
| UltraFan narrowbody Solo | `uf_nb`, `"variant": "solo"`: 7 years, $7.5B, $3.1M an engine, value ramp 0.45 to 1 over 6 years | yes | Earns only if fps or NGSA selects `rr_ultrafan_nb`. Unselected it costs -9.18 (2026) to -3.89 (2035). |
| Joint Venture with P&W | `uf_nb`, `"variant": "jv_pw"`: 6 years, capex and value 50/50, strain relief 0.5 | yes | Launches only if P&W sets `join_rr_jv` in the same turn. Without it nothing launches (0.00) and the airframe falls back to CFM. |
| Do Nothing (Trent only) | no orders; `t1000_upgrade` still fits "Trent only" (inference) | yes | Keeps 184.1 widebody engines a year. The upgrade (+10pp of Boeing widebody deliveries after 3 years, $0.8B) lifts that to 204.1 (+0.82). |
| (not on the slide) | `terms` standard or aggressive (+1.2pp airframer margin, value kept 0.86); `cancel` | yes | Terms are our only lever on an airframer's engine choice. |

## 3. Enablers and constraints

| Item | Engine parameter (value from `rules`) | Our evidence |
|---|---|---|
| Free cash from widebody | Not modelled: no cash limit; capex loaded at alpha 0.6. | FCF £3,270m (2025) [R-0220]; net cash £1,972m [R-0032]. The hurdle and engineers bind, not cash (inference). |
| Reputation | Not modelled. Nearest: `rr_ultrafan_nb` capture_mult 0.95 (CFM ducted 1.0). | Airframers want demonstrated engines [R-0383]; Boeing chose LEAP on maturation depth [R-1837]. |
| Airframer support for a third engine maker | Partly: `rr_ultrafan_nb` gives the airframer margin_pp 1.0 (CFM ducted 0, GTF2 0.5, RISE open fan 1.5 but not in service before 2045). | RR sees itself as the only credible third entrant [R-1310]; Airbus names open fan [R-1867]; Boeing wants one engine per narrowbody [R-1830]. |
| Engineering shared with widebody | Strain `full_overlap_b` $1.5B for 5 or more years of overlap, pro rata below (PLACEHOLDER); `jv_pw` strain_relief 0.5. Both UltraFans launched in 2029: 1.44 of strain (four-turn game; five-player, both 2031: 1.19). | Resources for 3 of 4 engines [R-0929]; three parallel programmes "unprecedented" [R-1127]. |
| No narrowbody MRO scale | Partly: narrowbody fit 0.0; $3.1M an engine (widebody $8.0M); ramp start 0.45. | No narrowbody since 2012 [R-0305, R-1826]; weaker buying power [R-1308]. |
| Gearbox sizing | Partly: `uf_nb` dev_years 7 (widebody 6); `ultrafan_test_setback` slips RR programmes 2 years. | Gearbox at full power in 2023 [R-1013]; narrowbody demonstrator about 2 years from build (2025) [R-1024]. |

## 4. How attainment is measured

| Metric id | What it measures | Target and years | Status quo |
|---|---|---|---|
| `nb_entry` | RR narrowbody engines delivered a year | above 0.5 in 2045 and 2050 | 0 and 0: **not met** |
| `wb_dominance` | RR widebody engines delivered a year | at or above the status quo (0.5 tolerance) in 2040, 2045, 2050 | 184.1 each year: **met** |

Both are engine counts, so `whatif` gives values and status quo but no `gap_pp`.

## 5. What it takes (four-turn game)

### 5.1 Narrowbody entry needs an airframer

RR cannot meet `nb_entry` alone. It needs fps or NGSA on `rr_ultrafan_nb` in a turn when `uf_nb` is launched. Any launch from 2026 to 2037 works: NGSA or fps launched in 2037 enters service in 2044 and delivers 2,457 or 1,657 engines in 2045.

**Plans that meet both metrics** (standard terms):

| Airframer plan | RR orders | RR delta PV, base / wave | Airframer delta PV on UltraFan (on CFM), base / wave | RR narrowbody engines 2045 |
|---|---|---|---|---|
| NGSA 2029 on UltraFan, no fps | T1 `t1000_upgrade`; T2 `uf_nb` Solo 2029 | +22.19 / +21.23 | Airbus 45.71 (42.05) / 42.20 (38.63) | 2,913 / 2,760 |
| fps 2029 on UltraFan, no NGSA | same | +14.75 / +13.53 | Boeing 18.14 (16.72) / 15.33 (13.87) | 2,113 / 1,960 |
| Both 2029 on UltraFan | `uf_nb` Solo 2029 (T1 upgrade too: +33.72) | +32.91 / +32.91 | Airbus 29.11 (25.59), Boeing 7.33 (5.76) | 4,000 |
| NGSA 2029 on UltraFan, P&W joins | T1 upgrade; `jv_pw` 2029 | +11.35 / +10.87 | Airbus 45.71 / 42.20 | 1,457 / 1,380 |
| NGSA and A350 Re-engine 2029, both on UltraFan | `uf_nb` Solo + `uf_wb` 2029 | +17.19 / +16.23 | Airbus 45.38 / 41.87 | 2,913 / 2,760 |

The lone CFM figures match `wave_grid.txt`. In all 40 selection cells per scenario (NGSA or fps on UltraFan in 2026, 2029, 2032 or 2035; the other airframer idle or on CFM in any of those years), RR's Solo PV is positive. The lowest is fps 2035 against NGSA 2026: +1.50 base, +2.83 wave, still 1,060 and 1,322 engines in 2045.

### 5.2 Widebody dominance is defensive

It holds at the status quo and breaks only when an airframer Re-engines on another engine. Both scenarios, 2029 launches:

| Airframer move | RR orders | RR delta PV | RR widebody engines 2040 / 2045 / 2050 | Met |
|---|---|---|---|---|
| none | `t1000_upgrade` T1 | +0.82 | 204.1 each | yes |
| A350 Re-engine on UltraFan | `uf_wb` 2029 | -2.75 | 197.3 / 210.6 / 223.8 | yes |
| A350 Re-engine, RR does not launch (falls back to GE) | Do Nothing | -5.11 | 39.5 / 35.8 / 32.0 | no |
| A350 Re-engine on P&W | Do Nothing | -4.13 | 41.3 / 37.9 / 34.6 | no |
| 787 Re-engine on GE | Do Nothing | -2.47 | 119.7 / 102.7 / 85.7 | no |
| 787 Re-engine on GE | `uf_wb` 2029, unselected | -5.45 | 119.7 / 102.7 / 85.7 | no |
| 787 Re-engine on UltraFan | `uf_wb` 2029 | +1.38 | 340 each | yes |

The upgrade does not save the metric against a rival Re-engine (A350 on GE plus upgrade: 57.4 in 2040).

### 5.3 Best-PV plan and objective premium

- **Once an airframer selects UltraFan, the objective is free.** In all 80 selection cells the PV-best RR plan (Solo in 2026, upgrade plus Solo later) meets both metrics. Premium 0.
- **With no selection, `nb_entry` is out of reach.** The best plan is the upgrade alone (+0.82). A speculative Solo still fails and costs 3.89 to 9.18 (4.69 if launched in 2026 and cancelled in 2029).
- **The premium sits in the decision before selection is certain.** Expected PV of a 2029 Solo at the profile's selection probabilities (profile §9 step 4; selected +21.38 NGSA or +13.93 fps base, +20.42 or +12.72 wave; unselected -6.90 in both):

| P(selected) | NGSA 2029, base / wave | fps 2029, base / wave | Premium against Do Nothing |
|---|---|---|---|
| 0.6 (announced on UltraFan) | +10.07 / +9.49 | +5.60 / +4.87 | 0 |
| 0.35 (announced, engine open) | +3.00 / +2.66 | +0.39 / -0.03 | 0; fps wave 0.03 |
| 0.2 (signal, no announcement) | -1.24 / -1.43 | -2.73 / -2.97 | 1.24 to 2.97 |

Break-even P: NGSA 0.24 (base) and 0.25 (wave); fps 0.33 and 0.35. Launching a turn early, so an unannounced airframer can pick us, costs 1.72 (Solo 2029 for NGSA 2032: +13.38 against +15.10).

### 5.4 The contest decides selection

- UltraFan on standard terms beats CFM ducted in all 40 cells (airframer gain 0.53 to 4.91 base) and P&W GTF2 on standard terms (0.26 to 2.71).
- It loses to P&W GTF2 on aggressive terms in all 40 (-0.32 to -3.25 base).
- It beats CFM's RISE open fan in all 40 (6.72 to 58.93 base, 7.34 to 51.13 wave). The open fan cannot enter service before 2045, and an airframe that would be ready earlier pays 10% of capex for each year it waits. The open fan loses even to CFM ducted in all 40 (NGSA 2026 alone: UltraFan 39.55, CFM ducted 34.65, open fan -15.04). Its best case is a 2037 launch, with no wait: Airbus 14.49 on it, 18.26 on UltraFan, 16.65 on CFM ducted (base).
- Aggressive UltraFan beats every alternative in all 40 (+0.32 to +3.25 base, +0.40 to +3.10 wave); the best alternative is always GTF2 on aggressive terms. It costs RR 0.92 to 6.37 (base) when selected: 4.65 on a lone NGSA 2029 (+16.73 against +21.38), 3.38 on fps 2029.
- P&W's PV on a lone NGSA 2029: GTF2 aggressive -3.48, GTF2 standard +0.72, joining our Joint Venture +12.38 (wave -3.61, +0.45, +11.77). On PV, P&W gains most from the Joint Venture; whether it joins is its own call (inference).

### 5.5 Rival timing

RR Solo PV when the other airframer launches on CFM:

| Other airframer launches | none | 2026 | 2029 | 2032 | 2035 |
|---|---|---|---|---|---|
| NGSA 2029 on UltraFan: base / wave | +21.38 / +20.42 | +15.20 / +16.27 | +16.99 / +16.99 | +18.49 / +17.72 | +19.67 / +18.49 |
| fps 2029 on UltraFan: base / wave | +13.93 / +12.72 | +7.23 / +8.31 | +9.03 / +9.03 | +10.53 / +9.76 | +11.71 / +10.53 |

An early rival answer cuts RR's value by up to 6.7 but never breaks the metric. The wave lowers lone 2029 entries by about 1 and softens early rival answers.

**Plans that pay both ways.** Each airframer gains from UltraFan over CFM ducted and the open fan in every cell, so RR must beat GTF2. The best joint cell is NGSA 2029 on UltraFan: Airbus's best NGSA year in both scenarios (45.71 and 42.20; 2026 gives 39.55 and 33.87) and +22.19 for RR. fps 2029 is Boeing's best year (18.14 and 15.33). NGSA 2026 pays RR most of any lone launch (+29.74, wave +27.80, `options` T1) but cannot be coordinated in turn 1, which has no announcement. `options` T1 fallback incentives at standard: fps 2.083, NGSA 4.909 (wave 2.109, 4.742).

## 6. Fit with our doctrine

**Agrees:**
- Entry needs an airframe; so does our launch rule [R-0994, R-1005].
- RR says it is well placed to re-enter narrowbody through a partnership [R-1009], sees itself as the only credible third entrant [R-1310], and self-funds a demonstrator so as not to wait [R-1017].
- Widebody defence: exclusivity extended against GE [R-0360, R-0361]. `uf_wb` for an announced A350 Re-engine is PV-best and holds the metric (5.2).
- RR aims to win back 787 share [R-1015, R-1021].

**Pulls against:**
- Narrowbody is optional: "we don't need to" [R-1011, R-0952]. The objective makes it a goal.
- Profit over share [R-1582, R-1561]; no "silly pricing" as sole source [R-0334]; prices now cover investment and risk [R-0367]. Winning a contest against aggressive GTF2 needs aggressive terms (5.4).
- The +$2B bar (profile §9 step 6) rejects fps at P 0.35 (+0.39 base). The objective would accept it (inference).
- Maturity over timing [R-0980, R-1934] and engineering rationing [R-0929, R-1127] argue against launching early.
- 787: GE prices hard and won the 777X [R-1946, R-1831]; doctrine wants P > 0.42 before `uf_wb`.

**Weighing rule.** The objective sets what we aim for; the doctrine sets how. Any objective premium counts against the existing doctrine-premium cap of $3B per turn (profile §9 step 11; RR reverses when the business case moves [R-0959, R-1561]). Hard rules still bind: no UltraFan launch without an announcement [R-0994, R-1005]; never compress maturity [R-1476, R-0970]; `jv_pw` only if P&W announced its join; no overlapping `uf_wb` and `uf_nb` Solo developments unless both are selected. In practice (inference):
1. Turn 1 is unchanged: upgrade, no UltraFan.
2. Against an announced fps or NGSA with the engine open, launch Solo if the premium (Do Nothing minus expected PV) fits the cap; this replaces the +$2B bar.
3. (four-turn game) Against an announced 787 Re-engine, `uf_wb` may be offered below P 0.42. The premium is 0.59 at P 0.35 and 1.61 at P 0.2 (2029: +1.38 selected, -5.45 unselected, -2.47 Do Nothing). On these 2029 numbers break-even P is 0.44, so even P 0.42 carries a premium of 0.11.
4. Aggressive terms only by profile §6's test: they are then PV-best, not a premium. A signal without an announcement never justifies a launch.

## 7. Per-turn objective check (four-turn game; add after §9 step 11; five-player: §9.3)

1. Read `your_objectives` in `brief`. Record `nb_entry` (2045 and 2050 engines) and `wb_dominance` (2040-2050 against 184.1).
2. `whatif` the chosen orders and the PV-best alternative, with the airframer selecting UltraFan and not. Read `objectives.rolls_royce` in each.
3. Objective premium = PV-best expected PV minus chosen expected PV. Add it to any doctrine premium and keep the sum within $3B.
4. If an announced Re-engine or narrowbody would fly a rival engine, `whatif` the contested incentive (UltraFan standard and aggressive against GTF2, open fan, CFM, GE).
5. Rationale line: "Objectives: nb_entry before X, after Y (P = p); wb_dominance before X, after Y; objective premium $Z B; ids."

## 8. Gaps and modelling limits

- Airframer selection is outside our control; the referee cannot force it. The P values are doctrine, not evidence.
- `nb_entry` is binary: a Joint Venture or 1,060 engines scores like 4,000.
- `wb_dominance` breaks under any rival Re-engine; RR cannot stop a 787 Re-engine on GE.
- A 2037 launch would miss 2045 if `ultrafan_test_setback` adds its 2 years (inference).
- Not modelled: cash limits, reputation. MRO scale only in part (value per engine, ramp). Gearbox risk is only dev years and the setback inject (`rr_ultrafan_nb` eis_add 1 is ignored when RR plays).
- Placeholders: strain; `jv_pw` dev years, strain relief.
- Airframers and P&W are treated as PV maximisers; in play they follow doctrines.

<details>
<summary>Commands</summary>

```bash
cd /home/user/aero-engine-gameboard
export WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/of_update/rr; mkdir -p $WARGAME_RUNS_DIR
python3 -m wargame.engine new --run-id rrv-base --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id rrv-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney
# RUN = rrv-base, rrv-wave:
python3 -m wargame.engine rules --run $RUN --side rolls_royce    # §2-§4: programs, terms, upgrade, strain, assigned_objectives
python3 -m wargame.engine rules --run $RUN --side control        # engine_options (margin_pp, capture_mult, eis_add), inject_deck
python3 -m wargame.engine options --run $RUN --side rolls_royce --compact   # +29.74 / +27.80; fallback incentives
W="python3 -m wargame.engine whatif --run $RUN --side control"   # turn keys: 1 = 2026, 2 = 2029, 3 = 2032, 4 = 2035 and 2037
echo '{"boeing": {}}' | $W                                       # status quo: 184.1 widebody, 0 narrowbody
echo '{"rolls_royce": {"1": {"t1000_upgrade": true}}}' | $W      # +0.82, 204.1
# unselected Solo, Y = 2026, 2029, 2032, 2035, 2037 (turn T): -9.18, -6.90, -5.18, -3.89, -3.22
echo '{"rolls_royce": {"T": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": Y}]}}}' | $W
echo '{"rolls_royce": {"1": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2026}]}, "2": {"cancel": ["uf_nb"]}}}' | $W   # -4.69
echo '{"rolls_royce": {"2": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2029}, {"program": "uf_wb", "terms": "standard", "year": 2029}]}}}' | $W   # strain 1.44
# §5.1 rows, e.g. NGSA 2029 (fps: "boeing" / "fps"; add the other airframer for "Both"; add "uf_wb" + "rea350" for the A350 row):
echo '{"rolls_royce": {"1": {"t1000_upgrade": true}, "2": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2029}]}},
 "airbus": {"2": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2029}]}}}' | $W
# Joint Venture: RR "variant": "jv_pw" plus '"pratt_whitney": {"2": {"join_rr_jv": true}}' (without it: 0.00, NGSA on CFM)
# 2037 cases: RR Solo 2037 and NGSA or fps 2037 on rr_ultrafan_nb, both in turn "4" (open fan: NGSA 2037 on cfm_open_fan, 14.49)
# 80-cell grid: X = NGSA (airbus) or fps (boeing) launched Y in {2026, 2029, 2032, 2035}; the other airframer idle or on
#  cfm_ducted in each of those years. Per cell: RR none, upgrade T1, Solo Y standard / aggressive, upgrade T1 + Solo Y
#  standard / aggressive with X on rr_ultrafan_nb; then X on cfm_ducted, cfm_open_fan, and pw_gtf2 with
#  '"pratt_whitney": {"T": {"launch": [{"program": "gtf_next", "terms": "standard|aggressive", "year": Y}]}}'.
#  Read RR and P&W delta_pv_b, the airframer's delta_pv_b and objectives.rolls_royce. §5.3-§5.5 come from this grid.
echo '{"rolls_royce": {"2": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2029}]}},
 "airbus": {"3": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2032}]}}}' | $W   # +13.38 (Solo 2032 instead: +15.10)
# §5.2: "airbus" rea350 or "boeing" re787 in turn 2 on rr_ultrafan_wb, ge_genx_next or pw_wb_new
#  (P&W: '"pratt_whitney": {"2": {"launch": [{"program": "pw_wb", "terms": "standard", "year": 2029}]}}'), with or without
#  RR '"2": {"launch": [{"program": "uf_wb", "terms": "standard", "year": 2029}]}' and '"1": {"t1000_upgrade": true}'
python3 wargame/profiles/build/cite_check.py wargame/profiles/rolls_royce/objectives.md wargame/profiles/rolls_royce/evidence.jsonl --show
```
</details>

## 9. Five-player game (five-player-2045)

Numbers are $B of full-game delta PV for RR from `whatif --side rolls_royce` on a five-player-2045 scratch run (RR, P&W and CFM/GE playing, no inject), round 1. They are snapshots: re-run them each round. Turn keys: 1 = 2026-30, 2 = 2031-35, 3 = 2036-45. Doctrine and reaction rows: profile §11. The metrics are unchanged (`nb_entry` above 0.5 in 2045 and 2050; `wb_dominance` at or above 184.1 in 2040, 2045, 2050).

### 9.1 What it takes

**Narrowbody entry: an airframer on UltraFan, launched by 2038.** `uf_nb` takes 7 years, so a launch after 2038 delivers nothing in 2045 (NGSA 2040: 0). With `ultrafan_test_setback` (+2 years) only launches by 2036 are safe. Round 1 has no announcements, so the hard rule [R-0994, R-1005] leaves rounds 2 and 3.

Plans that meet both metrics (standard terms; round-1 `t1000_upgrade` in each):

| Airframer plan | RR orders | RR delta PV | Airframer on UltraFan (CFM ducted / LEAP derivative) | RR narrowbody engines 2045 |
|---|---|---|---|---|
| NGSA 2031 on UltraFan | Solo 2031 | +17.32 | Airbus 38.88 (35.90 / 31.93) | 2,709 |
| fps 2031 on UltraFan | Solo 2031 | +11.11 | Boeing 12.40 (11.24 / 9.17) | 1,909 |
| Both 2031 on UltraFan | Solo 2031 | +27.17 | Airbus 27.30, Boeing 5.53 | 4,000 |
| NGSA 2031, P&W joins | `jv_pw` 2031 | +8.94 | Airbus 38.88 | 1,355 |
| NGSA and A350 Re-engine 2033 on UltraFan | Solo 2033, `uf_wb` 2032 (strain 1.03) | +10.77 | Airbus 32.05 | 2,640 |
| NGSA 2036 on UltraFan | Solo 2036 | +9.89 | Airbus 23.24 (21.44 / 18.91) | 2,513 |
| NGSA 2038 on UltraFan | Solo 2038 | +7.64 | Airbus 17.94 (16.51 / 14.46) | 2,400 |
| fps 2038 on UltraFan | Solo 2038 | +4.83 | Boeing 4.30 (3.79 / 2.90) | 1,600 |

CFM/GE's GEnx package in 2026 takes 0.58 off each plan and leaves `wb_dominance` met at 194.1 (NGSA 2031: +16.74).

**Rival timing.** RR's Solo value when the other airframer launches on CFM ducted:

| Other airframer on CFM ducted | none | 2028 | 2031 | 2033 | 2036 |
|---|---|---|---|---|---|
| NGSA 2031 on UltraFan | +16.50 | +12.91 | +13.53 | +14.04 | +14.80 |
| fps 2031 on UltraFan | +10.29 | +6.50 | +7.12 | +7.63 | +8.39 |
| NGSA 2036 on UltraFan | +9.07 | +6.02 | +6.37 | - | +7.30 |

An early rival answer cuts our value by up to 3.8 and never breaks the metric.

**Widebody dominance is defensive** (2040 / 2045 / 2050 engines):

| Move | RR orders | RR delta PV | RR widebody engines | Met |
|---|---|---|---|---|
| none | upgrade 2026 | +0.81 | 204.1 each | yes |
| GEnx package 2026 | none | -0.58 | 174.1 each | no |
| GEnx package 2026 | upgrade 2026 | +0.23 | 194.1 each | yes |
| A350 Re-engine 2033 on UltraFan | `uf_wb` 2032 | -2.11 | 189.4 / 202.6 / 215.9 | yes |
| A350 Re-engine 2033 on GE (we did not launch, or Airbus preferred GE) | none (upgrade) | -3.35 (-2.59) | 42.5 / 38.7 / 35.0 (61.8 / 56.4 / 50.9) | no |
| A350 Re-engine 2031 on UltraFan | `uf_wb` 2031 aggressive | -2.94 | 192.0 / 205.3 / 218.5 | yes |
| 787 Re-engine 2031 on GE | none | -1.98 | 126.5 / 109.5 / 92.5 | no |
| 787 Re-engine 2033 on UltraFan | `uf_wb` 2032 | +0.91 | 340 each | yes |
| 787 Re-engine 2036 on GE | none | -1.10 | 184.1 / 126.5 / 109.5 | no |

GE's GEnx fallback needs no wait; our 6-year engine makes a 5-year Re-engine wait a year unless `uf_wb` launches a year before the airframer. A same-year launch from 2030 loses the contest at standard terms (A350 2031: Airbus 1.74 on us, 2.11 on GE; A350 2036: 0.76 against 1.04), so the year-early launch, or aggressive terms when the announced year opens a round, is what keeps the A350.

### 9.2 Objective premium and the contest

Expected PV of a Solo launch at the profile's selection probabilities (selected / unselected: NGSA 2031 +16.50 / -5.70, fps 2031 +10.29 / -5.70, NGSA 2036 +9.07 / -3.54, fps 2036 +5.51 / -3.54, NGSA 2038 +6.83 / -2.92):

| P(selected) | NGSA 2031 | fps 2031 | NGSA 2036 | fps 2036 | NGSA 2038 | Premium against Do Nothing |
|---|---|---|---|---|---|---|
| 0.6 (announced on UltraFan) | +7.62 | +3.89 | +4.03 | +1.89 | +2.93 | 0 |
| 0.35 (announced, engine open) | +2.07 | -0.10 | +0.87 | -0.37 | +0.49 | 0; fps 0.10 and 0.37 |
| 0.2 (signal only) | -1.26 | -2.50 | -1.02 | -1.73 | -0.97 | 0.97 to 2.50 |

- Break-even P: NGSA 0.26 (2031) to 0.30 (2038); fps 0.36 to 0.42. Joint Venture at P 0.6: NGSA 2031 +3.69, 2036 +1.94; Solo leads by 3.93 and 2.09.
- Round 1: a speculative Solo 2028 pays +22.65 (NGSA) or +14.08 (fps) if selected and -7.59 if not; at P 0.1 it is -4.56 and -5.42. The premium of holding the hard rule is 0 at that P. The risk is structural: both airframers' PV peaks at a 2028 launch (NGSA 50.47 on UltraFan, 46.55 CFM ducted, 41.48 LEAP derivative; fps 16.97 / 15.34 / 12.58), so a round-1 launch on CFM can close `nb_entry` before we may act (inference).
- The fallback chain: an airframer naming UltraFan when we have not launched gets CFM ducted if CFM committed, else the LEAP derivative. Naming us therefore costs it nothing (inference).
- Contest (airframer gain from UltraFan standard): against CFM ducted standard NGSA +4.74 (2026) to +1.11 (2040), fps +2.11 to +0.40; against GTF2 standard NGSA +2.58 to +0.65. UltraFan standard loses to CFM ducted aggressive (2031: NGSA -1.75, fps -0.98) and GTF2 aggressive (NGSA -2.02, fps -0.91). Aggressive UltraFan beats all of them (2031: NGSA +2.01, fps +0.84; 2036: +1.25, +0.48) and costs RR 3.67 (NGSA) and 2.62 (fps) in 2031, 2.11 and 1.51 in 2036.
- The open fan loses everywhere: NGSA 2036 on it 15.47, lobbied 16.55, lobbied and aggressive 18.87, against UltraFan 23.24.
- P&W gains most from our Joint Venture: NGSA 2031 +9.71 (+9.34 after CFM's LEAP upgrade) against GTF2 standard +0.17 and aggressive -3.21 (inference: whether it joins is its own call).

### 9.3 Three-round objective check (add after profile §9 step 11)

**Every round.** Read `your_objectives` in `brief`; record `nb_entry` (2045 and 2050 engines) and `wb_dominance` (2040-2050 against 184.1). `whatif` the chosen orders and the PV-best alternative, with the airframer selecting UltraFan and not, and read `objectives.rolls_royce`. Objective premium = PV-best expected PV minus chosen expected PV; with any doctrine premium it stays within $3B per round. Rationale line: "Objectives: nb_entry before X, after Y (P = p); wb_dominance before X, after Y; objective premium $Z B; ids."

**Round 1 (2026-30).**
1. No announcements, so no UltraFan (premium 0 at P 0.1; speculative Solo 2028 -4.56).
2. Fund `t1000_upgrade` (+0.81): it keeps `wb_dominance` even if CFM/GE funds the GEnx package (194.1 against 174.1).
3. Disclose year-specific conditions: we launch `uf_nb` in the year an airframer announces on UltraFan, and `uf_wb` a year before an announced Re-engine year. A round-2 announcement is the only route to `nb_entry` (inference).
4. Record whether NGSA or fps launched on CFM in round 1. If both did, `nb_entry` is out of reach; score PV only.

**Round 2 (2031-35).**
1. For each round-1 announcement, `whatif` our launch in the announced year (narrowbody) or a year earlier (widebody).
2. Set P from the profile §9 step 4. Check the contest against CFM ducted if CFM committed one (else the LEAP derivative), GTF2 and the open fan, at both terms.
3. Launch Solo at P 0.6. Choose `jv_pw` only if P&W announced its join and Solo leads by $3B or less (NGSA 2035: 2.41). At P 0.35, NGSA 2031 Solo (+2.07) clears the +$2B bar; later NGSA launches are positive but below it (+1.54 in 2033), and fps costs a premium of 0.10 to 0.31 (2031-35). Under §6 item 2 launch while the premium fits the cap.
4. A350 Re-engine announced for 2031: standard loses to GE, so aggressive (-2.94 against -4.14 on GE; `wb_dominance` met). For a later year: `uf_wb` a year earlier, standard.
5. GEnx package announced and our upgrade unfunded: fund it only if no UltraFan development overlaps (+0.48); otherwise the red line holds.

**Round 3 (2036-45).**
1. If `nb_entry` is unmet, this is the last window: `uf_nb` by 2038 (2036 to stay safe against a setback). At P 0.6, NGSA Solo +4.03 (2036) to +2.93 (2038) and fps +1.89 to +1.24 are positive, so launch; the objective replaces the +$2B bar (§6).
2. After 2038 `nb_entry` cannot be met; PV only.
3. A350 Re-engine announced for 2036: aggressive `uf_wb` 2036 (-1.87 against -2.40 on GE). For a later year: a year earlier, standard (2037: -1.50 against -2.15).
4. Upgrade, if still unfunded and no overlap: +0.28.

<details>
<summary>Commands (five-player-2045)</summary>

```bash
cd /home/user/aero-engine-gameboard
python3 -m wargame.engine new --scenario five-player-2045 --suppliers rolls_royce,pratt_whitney,cfm --run-id rr-5p-scratch --force
python3 -m wargame.engine inject --run rr-5p-scratch --none
python3 -m wargame.engine options --run rr-5p-scratch --side rolls_royce   # fallback incentives fps 5.317, NGSA 10.593
W="python3 -m wargame.engine whatif --run rr-5p-scratch --side rolls_royce"  # turn keys 1 = 2026-30, 2 = 2031-35, 3 = 2036-45
# Narrowbody grid, Y in 2026, 2028, 2030, 2031, 2033, 2035-2038, 2040 (turn T): RR Solo / jv_pw (+ '"pratt_whitney": {"T": {"join_rr_jv": true}}')
#  in Y with ngsa (airbus) or fps (boeing) on rr_ultrafan_nb; unselected; the airframer on cfm_ducted
#  ('"cfm": {"T": {"launch": [{"program": "ducted", "terms": "standard|aggressive", "year": Y}]}}'), cfm_leap_plus, pw_gtf2
#  (P&W gtf_next standard|aggressive), cfm_open_fan (CFM open_fan, with or without '"cfm": {"1": {"lobby_emissions": true}}').
echo '{"rolls_royce": {"1": {"t1000_upgrade": true}, "2": {"launch": [{"program": "uf_nb", "variant": "solo", "terms": "standard", "year": 2031}]}},
 "airbus": {"2": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2031}]}}}' | $W     # +17.32
# Widebody: rea350 / re787 in year Y on rr_ultrafan_wb with uf_wb in Y or Y-1 (standard|aggressive), or on ge_genx_next.
# Upgrade: '"rolls_royce": {"T": {"t1000_upgrade": true}}' with and without '"cfm": {"T": {"genx_upgrade": true}}'.
rm -rf wargame/runs/rr-5p-scratch
```
</details>
