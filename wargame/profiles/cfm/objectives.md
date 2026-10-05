# CFM/GE: assigned objective (supplier player)

**Who reads this.** The `cfm-strategist`, when CFM/GE plays (`--suppliers ...,cfm`). The referee reads it to score attainment. When CFM/GE does not play, §9 applies.

**Conventions.**
- Ids are `CX-####` from `executives/evidence.jsonl`.
- Engine numbers are $B of delta PV (CFM/GE at `wacc` 0.08), labelled **(snapshot)**. They come from `whatif --side cfm` on a fresh `five-player-2045` run (suppliers `rolls_royce,pratt_whitney,cfm`), turn 1, no inject, reconciled CFM calibration as configured on 2026-10-05.
- Parameter values are **(provisional)** while `calibration.md` is reconciled. Cite the parameter names and re-run before relying on a number.
- The doctrine is in `profile.md`. This file says what the objective takes and what it costs.

## 1. Assigned objective

Assigned by control for this scenario, from the narrowbody players briefing (`rules --side cfm`, `assigned_objectives`):

> **Primary goal:** Dominate narrowbody engines; introduce the open fan
> **Possible moves:** Open fan only · Ducted only · Open + ducted (both) · Partner with Embraer · Lobby governments on emissions
> **Enablers:** Existing maintenance and overhaul base · Cash · Sustainable aviation fuel capability
> **Constraints:** Open fan certification risk · Airframer reluctance · Raw materials

The objective never changes the payoff. Any PV given up to advance it is an **objective premium**. It counts against the same cap as a doctrine premium: $2.0B in a turn and $4.0B in the game, plus one RISE allowance (`profile.md` §6).

## 2. Moves to levers

All five moves are modelled when CFM/GE plays.

| Briefing move | Lever | How to order it | What it does (provisional) | Snapshot value to CFM/GE |
|---|---|---|---|---|
| Open fan only | `open_fan`, not `ducted` | `{"launch": [{"program": "open_fan", "terms": "standard", "year": 2036}]}` in round 3 | `cfm_open_fan` becomes selectable: 9 years, $10.0B, $3.9M an engine; +1.5pp airframer margin, +1 year, 0.85 capture; no entry into service before 2045. An airframer must still pick it | fps 2037 on RISE: CFM -9.47 (+0.51 on the LEAP derivative). NGSA 2037 on RISE: -6.47 (+6.60) |
| Ducted only | `ducted`, not `open_fan` | `{"launch": [{"program": "ducted", "terms": "standard" or "aggressive", "year": Y}]}` | `cfm_ducted` becomes selectable: 7 years, $7.0B, $3.4M an engine | NGSA 2029: -8.90 standard, -14.87 aggressive (+14.46 on the LEAP derivative) |
| Both | `ducted` and `open_fan` | Both launches; each needs its own year | Both capexes, and strain while they overlap | Ducted and RISE both in 2036, NGSA 2037 on RISE and fps 2037 on ducted: -17.38 |
| Partner with Embraer | `embraer_partner` | `"embraer_partner": true` | $1.2B over 4 years; from 8 years later, 190 engines a year at $1.2M | -0.10 in round 1, -0.14 in round 2, -0.16 in round 3 |
| Lobby governments on emissions | `lobby_emissions` | `"lobby_emissions": true` | $0.15B over 3 years (not alpha-loaded); from 3 years later, airframes on RISE get +0.5pp and 1.05 capture | -0.14 alone in round 1, -0.06 in round 3. It adds +1.08 to Airbus on an NGSA 2037 RISE, +0.45 to Boeing on an fps 2037 |

**Do Nothing.** Without a CFM commitment, an airframe that asks for a CFM narrowbody engine flies the **LEAP derivative** (`cfm_leap_plus`: -1pp margin, 0.92 capture). CFM keeps it at today's $3.0M LEAP value, less `derivative_capex_b` $1.0B. `nb_dominance` counts it as CFM. An airframe that asks for a rival engine whose maker has not launched falls back to `cfm_ducted` if launched, else the LEAP derivative.

**Other levers that move the metrics.**
- `leap_upgrade` moves 5pp of A320neo deliveries from Pratt & Whitney until the NGSA enters service. It lifts `nb_dominance` from 76% to 79% and is worth +4.94 in round 1 (snapshot).
- `genx_upgrade` and `terms` do not touch the narrowbody metrics directly, but aggressive `terms` decide whether an airframer picks a CFM engine over a rival's.

## 3. Enablers and constraints

| Item | Engine parameter (provisional) | What our evidence says |
|---|---|---|
| Maintenance and overhaul base | `incumbent_value_m_per_engine` (lifecycle value, aftermarket included); `leap_upgrade` saves $0.42B a year for 10 years. `nb_dominance` counts engines on deliveries, not the installed base | A 78,000-engine installed base [CX-0994]; 70% of revenue supports it [CX-0898]; about 70% of LEAP shop visits by CFM by 2030, split equally with Safran [CX-0219] |
| Cash | `wacc` 0.08; `alpha` 0.45 on capex (a placeholder) | More than 70% of deployable cash to shareholders [CX-0923]; capex at 2-3% of revenue [CX-0922]; R&D with no "program dividend" [CX-0174]; 2025 profit about $8.7-8.8B [CX-0989] |
| Sustainable aviation fuel capability | Not modelled; `lobby_emissions` is the nearest lever | Every GE and CFM engine in service runs on approved sustainable aviation fuel [CX-0508]; RISE is fuel-ready and hydrogen-capable [CX-0001] |
| Open fan certification risk | `cfm_open_fan` `eis_add` 1 and `available_eis` 2045; `open_fan` `dev_years` 9; `ramp` from -30% of value over 10 years. `engine_maturity_slip` moves airframe tech-ready to 2037, which leaves every RISE value unchanged. There is no RISE test-setback inject | The fly demo slipped from "by the middle of this decade" to "this decade" [CX-0151] [CX-0211]; earliest-ever dust testing [CX-0222]; an open-fan durability owner [CX-0223]. GE's own window was the mid-2030s [CX-0608] [CX-0152], about ten years earlier than the game's 2045 |
| Airframer reluctance | `capture_mult` 0.85; market multipliers 0.75-1.25; the airframer still chooses the engine | Entry into service is "really not for us to say" [CX-0205]; products follow "as our airframer and airline customers deem appropriate" [CX-0469] |
| Raw materials | `supply_chain_crunch`: strain x1.5 for every player, CFM/GE included (`strain` $1.75B; snapshot: LEAP and GEnx upgrades in the same round fall from +4.31 to +3.61) | 80% of shortages from 9 suppliers [CX-0613]; GE engineers inside suppliers [CX-0993] [CX-0526] |

## 4. How attainment is measured

| Metric | What it measures | Target | Status quo |
|---|---|---|---|
| `nb_dominance` | CFM's share of narrowbody engines: each airframer's share times CFM's fit. Fit is 1 once a new airframe enters service on `cfm_ducted`, `cfm_open_fan` **or the LEAP derivative**, and 0 on `pw_gtf2` or `rr_ultrafan_nb`. Before that, incumbent fit: Boeing 1.0, Airbus 0.60, moved 5pp by `leap_upgrade` or `gtf_upgrade` | At or above the status quo in 2040, 2045 and 2050 | 76% each year; met |
| `open_fan` | The first entry into service of any live airframe on `cfm_open_fan` | By 2045. Nothing on RISE enters service before 2045, so only 2045 meets it. It needs CFM to launch `open_fan` by 2036 and an airframer to fly it | Not met |

`whatif` returns both under `objectives.cfm` (`values`, `gap_pp`, `first_eis`); `brief` shows them as `your_objectives`.

## 5. What it takes: engine runs

All runs use the default upgrades (`leap_upgrade` round 1, `genx_upgrade` round 2) unless marked (snapshot).

**Dominance.**

| Situation | CFM plan | CFM / Boeing / Airbus | `nb_dominance` 2040/45/50 |
|---|---|---|---|
| Nobody launches | Default | +5.46 / 0 / 0 | 79/79/79%: met |
| fps and NGSA 2029, no rival engine | Default (LEAP derivative on both) | +17.07 / +4.20 / +26.21 | 100%: met |
| Same | Ducted standard 2027 | -18.33 / +5.76 / +29.73 | 100%: met |
| Pratt & Whitney launches `gtf_next` and Airbus picks it **in the same round** (NGSA 2029) | Default | -24.77 / -2.24 / +44.35 | 37/31/24%: missed (-52pp) |
| Pratt & Whitney launched in round 1; Airbus launches NGSA 2031 in round 2 | Default; Airbus on GTF2 | -19.99 / -1.94 / +37.20 | missed (-51pp) |
| Same | `ducted` standard 2031 | -4.46 / -2.02 / +35.90 (Airbus prefers GTF2) | met if Airbus took it |
| Same | `ducted` **aggressive** 2031 | -9.47 / -2.02 / **+40.63** (Airbus prefers CFM) | 100%: met |
| Rolls-Royce `uf_nb` Solo in round 1; Boeing fps 2031 in round 2 | Default; Boeing on UltraFan | -19.12 / +12.40 / -5.99 | missed (-47pp) |
| Same | `ducted` aggressive 2031 | -12.58 / **+13.38** / -6.31 | met |
| Pratt & Whitney `gtf_upgrade` in round 1 | Default | +1.93 | 76%: met |
| Same | `genx_upgrade` only | -3.01 | 73%: missed (-3pp) |

**Reading.**
- With no rival engine, dominance is free: the LEAP derivative keeps it, and is CFM's PV-best plan.
- A rival launch is the only real threat. Aggressive `ducted` defends it and is also PV-better than losing the airframe: +10.5 on the NGSA, +6.5 on the fps (snapshot). So no objective premium is needed there.
- Standard ducted does not win the airframer.
- Two cases cannot be defended by terms. If the rival launches in the same round as the airframer, CFM must have anticipated it. Pre-empting pays only above a probability of about 0.7 (`profile.md` §6). And Pratt & Whitney's aggressive GTF on the NGSA (+48.75 for Airbus) beats CFM's aggressive ducted (+48.40) (snapshot).

**The open fan.**

| Situation | CFM plan | CFM / Boeing / Airbus | `open_fan` |
|---|---|---|---|
| NGSA 2029 on the LEAP derivative; fps 2037 asks for RISE | Default, no RISE (fps gets the LEAP derivative) | +17.49 / -2.66 / +33.11 | missed |
| Same | + `open_fan` 2036 standard + `lobby_emissions` | +8.86 / -3.46 / +33.95 | **met (2045)** |
| Same | + `open_fan` 2036 aggressive + lobbying | +7.56 / -2.85 / +33.95 | met |
| Same, fps asks ducted | + `ducted` 2036 | +9.09 / -2.15 / +33.11 | missed |
| fps 2029 on the LEAP derivative; NGSA 2037 asks for RISE | Default, no RISE | +10.53 / +8.33 / +4.78 | missed |
| Same | + `open_fan` 2036 standard + lobbying | -1.24 / +8.79 / +5.29 | **met (2045)** |
| Same | + `open_fan` 2036 aggressive + lobbying | -3.37 / +8.79 / +7.04 | met |
| Same, NGSA asks ducted | + `ducted` 2036 | -1.02 / +8.33 / +6.21 | missed |

**Reading.**
- **Objective premium for RISE:** 8.63 (fps case) and 11.77 (NGSA case) against the LEAP derivative; only 0.22-0.23 against a ducted twin. RISE costs CFM about what any new engine costs. What is expensive is leaving the LEAP derivative.
- **Will the airframer pick it?**
  - Airbus on an NGSA 2037 prefers RISE with lobbying (+5.29) to the LEAP derivative (+4.78), but not to a ducted engine (+6.21) unless RISE is aggressive (+7.04).
  - Boeing on an fps 2037 prefers the LEAP derivative (-2.66) to RISE with lobbying (-3.46), even aggressive (-2.85).
  - "Open fan only" therefore works for a 2037 NGSA. For a 2037 fps it needs aggressive terms and still trails.
- **Timing.**
  - CFM must launch in 2036: a 2031 launch only adds capex (fps 2037: -11.84 against -9.47), and a 2037 launch is ready in 2046.
  - An airframe on RISE launched before 2036 waits to 2045 and pays for it: NGSA 2029 on RISE leaves Airbus +1.79 against +38.09.
  - An fps 2037 on RISE misses 2045 only if both the FAA certification inject and Delay Tactics hit; an fps 2036 absorbs both; NGSA is never slipped.
- **Who launches late?** Both airframers earn more by launching early on any CFM engine. On the LEAP derivative: Airbus NGSA +38.09 in 2029 against +16.59 in 2037; Boeing fps +11.36 against +3.64. An open-fan customer exists only if an airframer is still unlaunched in round 3. If both launch in rounds 1-2, `open_fan` is unattainable: say so and play for `nb_dominance` and PV.

**Both engines.** Both engines are needed only if two late airframes want different CFM engines. Otherwise "both" is pure cost: ducted and RISE in round 1 with one NGSA on ducted: -20.85 (snapshot).

**Embraer and lobbying.** `embraer_partner` moves neither metric and is PV-negative in every round (snapshot). `lobby_emissions` matters only with RISE: it is what lets RISE beat the LEAP derivative for Airbus.

## 6. Fit with our doctrine

**Where the objective agrees with us.**
- **Dominance is the franchise:** sole source on the MAX, about 60% of A320neo wins [CX-0182], over 70% of recent A320 decisions [CX-0218], "all the critical platforms" [CX-0587].
- **RISE is GE's next engine:** "all in" [CX-0214], at least 20% [CX-0217], kept funded through crises [CX-0553] [CX-0398].

**Where it pulls against us.**
- **Share is not the goal:** "we're not going for share" [CX-0493]; "not the low bid" [CX-0250]; price "regardless of what our competitors may do" [CX-0609]. Aggressive terms are therefore defensive only, and the engine shows they pay as defence.
- **The airframer sets the date** [CX-0205] [CX-0469]: CFM cannot make RISE fly, and must not press an early airframe into a wait.
- **Dates rest on tests** [CX-0009] [CX-0008]. The demo has slipped [CX-0151] [CX-0211]; nothing in the evidence names 2045.
- **The CFO's tests:** price/cost positive [CX-0929], capex within 2-3% [CX-0922], wariness of stacked ramps [CX-0933].
- **The Safran gate:** RISE, narrowbody pricing and capacity are joint [CX-0166] [CX-0184]. Assume consent and say so.

**Weighing rule.**
1. **The objective sets the aim:** both new narrowbodies on CFM engines, and RISE in service in 2045 if an airframer will fly it.
2. **The doctrine sets how:**
   - the LEAP derivative by default;
   - aggressive `ducted` only against a launched or signalled rival;
   - `open_fan` in 2036 only against a committed 2036-2037 airframer (gates G1-G5);
   - never refuse or press an airframer.
3. **Premiums.**
   - Dominance needs none: its defence is PV-positive against the loss.
   - RISE needs the one RISE allowance (snapshot premium 8.6-13.1 against the LEAP derivative).
   - Anything else for the objective must fit $2.0B a turn and $4.0B a game.
4. **Never break for the objective:**
   - the 20% bar [CX-0217];
   - durability [CX-0208];
   - test evidence for dates [CX-0009];
   - price/cost positive [CX-0929];
   - no unmodelled terms risk [CX-0440];
   - no early RISE wait for an airframer [CX-0205].

## 7. Per-turn objective check

Run each turn, before deciding, and report it in the rationale.
1. **Measure now.** From `brief` (`your_objectives`) log `nb_dominance` (values, `gap_pp`) and `open_fan.first_eis`.
2. **Measure each candidate.** For every plan you test in `whatif`, log `objectives.cfm`. Include the likely airframer and rival orders; `options` assumes they do nothing.
3. **Threat scan.**
   - Is any rival narrowbody engine launched or signalled (`gtf_next`, `uf_nb`)?
   - Which airframes are still unlaunched?
   - Would each prefer the rival engine to our best offer (compare the airframer's delta PV in `whatif`)?
   - If yes, and a CFM aggressive `ducted` flips it, that is the dominance move.
4. **Upgrade scan.** Has Pratt & Whitney ordered `gtf_upgrade`? If `leap_upgrade` is not done, do it (73% back to 76%).
5. **Open-fan window.**
   - Rounds 1-2: no launch; disclose RISE readiness for 2045.
   - Round 3: is an airframer unlaunched and committed, or predicted at about 0.7, to a 2036-2037 RISE launch? Check G1-G5, then compute the RISE premium against the LEAP derivative and against a ducted twin.
   - If no airframer is left, record "open_fan unattainable".
6. **Record** for each metric: met or missed before and after your orders, the gap, and any objective premium with its share of the cap.

## 8. A plan that meets both metrics, and what it needs from others

The cheapest plan that meets both, in the snapshot, is "NGSA 2029 on the LEAP derivative, fps 2037 on RISE". It costs CFM 8.63 against the default (+8.86 against +17.49), and Boeing 0.80 (-3.46 against -2.66) unless CFM goes aggressive.

With "fps 2029, NGSA 2037 on RISE" Airbus gains (+5.29 against +4.78), but CFM pays 11.77.

Neither happens unless an airframer chooses to wait to round 3: CFM cannot cause it.

## 9. When CFM/GE does not play (the old rules)

Without `cfm` in `--suppliers`, the old rules apply:
- CFM/GE has no payoff, no capex and no levers. The briefing's moves are not orders.
- Both CFM engines are always on offer to both airframers, with no commitment. The default is `cfm_ducted` for fps and NGSA; there is no LEAP-derivative fallback. A Rolls-Royce or Pratt & Whitney engine whose maker has not launched falls back to `cfm_ducted`.
- The referee measures the same two metrics with `whatif --side control`. In the five-player scenario without CFM:
  - NGSA 2029 on `cfm_ducted`: 100% (met);
  - NGSA 2037 on `cfm_open_fan`: entry 2045 (met);
  - NGSA 2029 on `pw_gtf2` with `gtf_next` launched: 37/31/24% (missed, -52pp).
- The market cell and referee use `profile.md` and `executives/` only to judge whether a CFM/GE reaction is plausible.

Earlier analysis under the two-player rules found:
- the open fan was never an airframer's best reply;
- `pw_gtf2` beat `cfm_ducted` for both airframers at every launch year;
- the only pure Nash pair put both new narrowbodies on `pw_gtf2`, so CFM lost dominance.

That analysis used an older config; re-run it before relying on it.

## 10. Gaps

- **Provisional values.** Open-fan capex and value, `alpha`, `embraer_partner`, `lobby_emissions`, strain and derivative capex are placeholders. The finding that a new CFM engine is worth less to CFM than the LEAP derivative rests mainly on `ramp` (-30% start, 10 years) and the new engines' capex.
- **The 2045 date is a control assumption,** about ten years after GE's and Safran's windows [CX-0608] [CX-0152].
- **Missing evidence.** There is none on Embraer or emissions lobbying, and Safran's side is unknown beyond one investor day [CX-0153].
- **The solver.** `equilibria` is the referee's and tries first-year launches only. The players' late-launch choices that decide `open_fan` are not covered by it.
