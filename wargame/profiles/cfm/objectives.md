# CFM International (GE side): assigned objectives

**Who reads this.** CFM is not a player. The referee scores its objective; the market cell may use this brief for CFM/GE reactions; a future CFM supplier player would start here. Ids are `CX-####` from `executives/evidence.jsonl`. Delta PV is in $B. "Wave" is the `replacement-wave` scenario.

## 1. Assigned objective

Source: assigned by control for this scenario (from the Boeing PD players briefing).

> **Primary goal:** Dominate narrowbody engines; Introduce Open Fan
> **Possible moves:** Open Fan only · Ducted only · Open + Ducted (both) · Partner with Embraer · Lobby governments on emissions
> **Enablers:** Existing maintenance & overhaul base · cash · Sustainable Aviation Fuel capability
> **Constraints:** Open Fan certification risk · airframer reluctance · raw materials

## 2. Moves to levers

Checked against `rules --scenario base --side control` and `rules --scenario replacement-wave --side control` (`assigned_objectives.cfm.moves`, the same in both). There is no `--side cfm`.

| Briefing move | Game lever and how to order it | Modelled | Notes |
|---|---|---|---|
| Open fan only | The airframer picks the engine: `{"launch": [{"program": "fps" or "ngsa", "engine": "cfm_open_fan", "year": Y}]}` | Partly | CFM cannot withhold the ducted engine, so "only" cannot be enforced |
| Ducted only | Same, with `"engine": "cfm_ducted"` (the default for fps and NGSA) | Partly | CFM cannot withhold the open fan either |
| Both | Both engines are always on offer to both airframers | Partly | This is the engine's default state |
| Partner with Embraer | None | No | The fps Joint Venture (`"variant": "jv"`) is Boeing-Embraer and leaves the engine choice unchanged. It does make the open fan cheaper for Boeing (§5) |
| Lobby governments on emissions | None | No | Nearest: `tech_ready_year` 2035 and the `fuel_price_spike` inject (+1.5pp to every new product, whatever the engine), so it does not favour the open fan |

## 3. Enablers and constraints

| Item | Engine parameter (value from rules) | What our evidence says |
|---|---|---|
| Maintenance and overhaul base | Not modelled. `nb_dominance` counts engines on deliveries, not the installed base | A 78,000-engine installed base [CX-0994]; 70% of revenue supports it [CX-0898]; about 70% of LEAP shop visits by CFM by 2030 [CX-0219]; CFM powers about 75% of narrowbody flights [CX-0980] |
| Cash | Not modelled: CFM has no capex or payoff | More than 70% of deployable cash goes to shareholders [CX-0923]; capex at 2-3% of revenue [CX-0922]; R&D held, with no "program dividend" [CX-0174] [CX-0962] |
| Sustainable aviation fuel capability | Not modelled | Every GE and CFM engine in service can run on approved sustainable aviation fuel [CX-0508]; RISE is fuel-ready and hydrogen-capable [CX-0001] |
| Open fan certification risk | `cfm_open_fan` `eis_add` +1 year (10% of program capex per extra year); `engine_maturity_slip` moves tech-ready 2 years later | The fly demo slipped from "the middle of this decade" [CX-0151] to "this decade" [CX-0211]; earliest-ever dust testing [CX-0222]; an open-fan Chief Mechanic for durability [CX-0223] |
| Airframer reluctance | `cfm_open_fan` `capture_mult` 0.85; market multipliers 0.75-1.25 | Entry into service is "really not for us to say" [CX-0205]; products launch "as our airframer and airline customers deem appropriate" [CX-0469] |
| Raw materials | Partly: `supply_chain_crunch` raises every player's strain ×1.5 (the airframers and any engine-maker player). CFM has no strain, so it is not hit | 80% of shortages came from 9 suppliers [CX-0613]; castings and forgings [CX-0750]; about 1% of titanium from Russia [CX-1258] |

## 4. How attainment is measured

| Metric id | What it measures | Target and years | Status quo |
|---|---|---|---|
| `nb_dominance` | CFM's share of narrowbody engines: each airframer's share × CFM fit. Fit is 1 once its new program enters service on `cfm_ducted` or `cfm_open_fan`, and 0 if it enters service on `pw_gtf2` or `rr_ultrafan_nb`. Before that, the incumbent fit applies: Boeing 1.0 (LEAP sole source), Airbus 0.60 (1 minus the GTF's 0.40). When P&W plays, Airbus's fit falls 5pp from three years after its GTF upgrade | At or above the status quo in 2040, 2045 and 2050 | 76.0% each year; met (gap 0.0pp) |
| `open_fan` | The first entry into service of any live program on `cfm_open_fan` | 2045 or earlier | None; not met |

## 5. What it takes

**The open fan metric.** Every open-fan launch from 2026 to 2037 meets it, because entry into service is the launch year + 8. That held in all 720 open-fan plans of my four sweeps, and in all 4,104 open-fan pairs of the full base and wave pair grids. It also survives slips:

| Open-fan fps launch | Delay Tactics or FAA certification inject | First entry into service | Met |
|---|---|---|---|
| 2032-2034 | Delay Tactics in turns 3 and 4 (2 years) | 2042-2044 | Yes |
| 2035 | Delay Tactics in turn 4, or the certification inject | 2044 | Yes |
| 2036 | Same | 2045 | Yes |
| 2037 | Same | 2046 | **No** |

The two slips stack: the certification inject plus Delay Tactics in turn 4 push an fps 2036 open fan to 2046, a miss. Neither touches NGSA.

**The dominance metric.** Every plan in which no airframer flies another maker's engine meets it. There were 0 failures in 1,440 such sweep runs (base, wave and both maturity-slip runs) and in 2,450 such pairs of the full base and wave grids. It fails only on another maker's engine:
- NGSA 2028 on `pw_gtf2`: CFM falls to 32.9/25.8/20.0% (gap -56.0pp, base);
- fps 2028 on `rr_ultrafan_nb`: gap -52.8pp (base, with suppliers, Rolls-Royce launching `uf_nb` in turn 1);
- with suppliers, P&W's GTF upgrade alone cuts CFM to 73.0% (-3.0pp). An NGSA on `cfm_ducted` (2029 or 2032) restores 100%. An fps 2028 ducted restores it in base (+0.37pp), not in wave (-1.3pp). An fps 2027 open fan fails in both (-0.13pp, -1.56pp): its 0.85 capture slows Boeing's share gain.

**This is a live risk even without suppliers.** In two-player runs both airframers may order `pw_gtf2`, and it beats `cfm_ducted` by +0.3 to +2.2 at every launch year from 2026 to 2033 (rival at Do Nothing or a 2029 ducted launch). It stays ahead at every launch year to 2037, against every rival timing in the sweeps (+0.1 to +2.3).

**What the open fan costs the airframer.** The table compares the same launch year, with the rival at Do Nothing (fps Solo):

| Launch | Boeing fps, base: ducted / open / diff | wave diff | Airbus NGSA, base: ducted / open / diff | wave diff |
|---|---|---|---|---|
| 2026 | +13.50 / +13.66 / +0.16 | +1.15 | +34.65 / +43.15 / +8.50 | +9.00 |
| 2027 | +16.73 / +16.17 / -0.57 | +0.44 | +41.29 / +47.97 / +6.68 | +7.31 |
| 2028 | +19.09 / +14.09 / -5.00 | -3.82 | +46.47 / +43.35 / -3.12 | -2.14 |
| 2029 | +16.72 / +12.21 / -4.51 | -3.52 | +42.05 / +39.07 / -2.97 | -2.11 |
| 2032 | +10.95 / +7.67 / -3.28 | -2.88 | +30.66 / +28.05 / -2.61 | -2.18 |
| 2035 | +6.77 / +4.39 / -2.38 | -2.31 | +21.62 / +19.30 / -2.32 | -2.21 |
| 2037 | +4.67 / +2.75 / -1.93 | -1.92 | +16.65 / +14.49 / -2.16 | -2.14 |

The mechanism (rules and `margin_at_eis`): for a 2026 or 2027 launch, the open fan's extra year moves entry into service one year closer to tech-ready 2035 (2034 instead of 2033, or 2035 instead of 2034). That removes 2pp of early penalty, and the engine adds +1.5pp. From 2028 on there is no penalty left to remove, so the open fan's +1.5pp does not pay for a year's delay, 10% more capex and 15% less capture.

**Best plans and the objective premium** (premium = best PV minus best open-fan PV; rival on `cfm_ducted`):

| Scenario | Airframer vs rival | Best overall | Best on CFM | Best open fan | Premium vs best on CFM / overall |
|---|---|---|---|---|---|
| Base | Boeing vs Do Nothing | fps 2028 `pw_gtf2` +19.57 | fps 2028 ducted +19.09 | fps 2027 Solo +16.17 | 2.92 / 3.40 |
| Base | Boeing vs NGSA 2029 | fps 2028 `pw_gtf2` +8.96 | fps 2028 ducted +8.13 | fps 2027 Solo +6.31 | 1.82 / 2.65 |
| Base | Airbus vs Do Nothing | NGSA 2028 `pw_gtf2` +48.22 | NGSA 2027 open fan +47.97 | the same | 0 / 0.25 |
| Base | Airbus vs fps 2029 | NGSA 2027 open fan +32.58 | the same | the same | 0 / 0 |
| Wave | Boeing vs Do Nothing | fps 2028 `pw_gtf2` +15.93 | fps 2028 ducted +15.34 | fps 2027 Solo +12.79 | 2.55 / 3.14 |
| Wave | Boeing vs NGSA 2029 | fps 2028 `pw_gtf2` +8.08 | fps 2028 ducted +7.23 | fps 2027 Solo +5.50 | 1.73 / 2.59 |
| Wave | Airbus vs Do Nothing | NGSA 2028 `pw_gtf2` +43.81 | NGSA 2027 open fan +43.60 | the same | 0 / 0.22 |
| Wave | Airbus vs fps 2029 | NGSA 2027 open fan +31.34 | the same | the same | 0 / 0 |

**Rival timing.**
- **Boeing.** Its open-fan premium against its best CFM plan, with Airbus at Do Nothing or NGSA 2026/2029/2032/2035: base 2.92/1.87/1.82/2.19/2.45; wave 2.55/1.75/1.73/1.91/2.08.
- **Airbus.** Its premium against its best CFM plan is 0 against Boeing at Do Nothing and against fps 2026, 2029, 2032 and 2035, in both scenarios. Against its best plan overall it is 0 to 0.56 in base and 0 to 0.22 in wave: NGSA 2028 on `pw_gtf2` is the only better plan.
- **Maturity slip.** With `engine_maturity_slip` the best open-fan year moves to 2029 (entry into service 2037). The NGSA 2029 open fan stays Airbus's best CFM plan (+39.07 base, Boeing at Do Nothing); NGSA 2030 on `pw_gtf2` beats it by 0.33. Boeing's premium against its best CFM plan is 1.49-2.37 in base and 1.44-2.16 in wave.
- **Spillover** (base, against the ducted twin). An fps open fan raises Airbus's PV by +0.8 to +4.0, because Boeing captures share more slowly. An NGSA open fan raises Boeing's by +0.3 to +2.2.
- **Joint Venture.** Embraer's share narrows the gap: the fps 2026 Joint Venture open fan beats its ducted twin by +0.75 (base) and +1.49 (wave). But the best Joint Venture open-fan plan (fps 2027, +11.48 base) is far below the best Solo plan.

**The cheapest plan that meets both metrics** is NGSA 2027 on the open fan with fps 2028 on `cfm_ducted`: Boeing +6.63, Airbus +30.50 in both scenarios (both enter service in 2035, so shares do not move). "Cheapest" means the smallest total gap to each side's best reply, over the full pair grid (4,753 pairs per scenario).
- **Airbus.** The NGSA 2027 open fan is its best reply to that fps over all four engines and every launch year.
- **Boeing.** Its best reply to that NGSA is fps 2028 on `pw_gtf2` (+7.50). That breaks `nb_dominance`, so keeping Boeing on CFM costs it 0.87.
- **The equilibrium misses dominance.** In that grid the only pure Nash pair, in both scenarios, is fps 2028 on `pw_gtf2` against the NGSA 2027 open fan (Boeing +7.50, Airbus +30.50). It meets `open_fan` (2035) but leaves CFM at 60.0% (-16.0pp). The grid covers narrowbody launches only: no widebody moves, Rate Increase or tactics.

Check: I reproduced the briefing grid's fps 2029 / NGSA 2029 cell in both scenarios (Boeing +5.76, Airbus +25.59). The grid is all ducted, so no row meets `open_fan`.

**Supplier levers CFM would need** (proposed, not in the engine) **(inference)**:
1. **Launch levers for `cfm_open_fan` and `cfm_ducted`**, with capex, development years and a fallback rule, as Rolls-Royce and Pratt & Whitney have. Only then can CFM offer one engine, the other, or both.
2. **Standard or aggressive terms** to offset Boeing's 1.7-2.9 open-fan premium, and the 0.87 it gains from `pw_gtf2` against the NGSA 2027 open fan.
3. **A one-time LEAP durability upgrade**, to counter the GTF upgrade.
4. **Two new levers:** a CFM-Embraer engine commitment and an emissions-lobbying lever, priced as a margin or tech-ready effect.

## 6. Fit with our doctrine

**Where the objective agrees with us.**
- **The open fan.** Culp is "all in" [CX-0214], calls it the most promising path to at least 20% [CX-0217], and keeps RISE funded [CX-0553] [CX-0174]. Ali argues it on physics [CX-0180] [CX-0183]. Safran's CEO set "by 2035" [CX-0152]; Culp says "by the middle of the next decade" [CX-0608]. The PV-best open-fan plan (NGSA 2027, in service 2035) fits those dates.
- **Dominance.** LEAP is sole source on the MAX [CX-0182], with a win rate above 70% on the A320 family since 2023 [CX-0218]. Culp wants "all the critical platforms" [CX-0587] and co-plans with the airframers [CX-0185] [CX-0193].

**Where it pulls against us.**
- **Share is not the goal:** "we're not going for share" [CX-0493]; "not the low bid" [CX-0250]; profitability over share (Ghai, of GE Power) [CX-0912]; pricing regardless of competitors [CX-0609]; no relative yardstick [CX-0600]. Yet `nb_dominance` is a relative share.
- **The airframer sets the date** [CX-0205]. CFM can offer the open fan but cannot make it fly.
- **Dates rest on tests:** "turn on and turn off" [CX-0009]; "not on the back of a theory" [CX-0008]. An fps 2026 open fan (in service 2034) runs ahead of GE's own words **(inference** from [CX-0608]**)**.
- **Durability comes first.** It is not traded for fuel burn [CX-0208]: "safety, quality, delivery and cost, always in that order" [CX-0658].
- **The CFO is wary of new-engine ramps** [CX-0933] [CX-0995] and is committed to cash returns [CX-0923].
- **The Safran gate.** RISE and narrowbody pricing need the partner [CX-0166] [CX-0184]. Consent is assumed **(inference)**.

**Weighing rule.**
1. **The objective sets the aim:** an open fan in service by 2045, and both new narrowbodies on CFM engines.
2. **The doctrine sets how:**
   - offer both engines to both airframers [CX-0185] [CX-0193];
   - never force the open fan or refuse an airframer [CX-0205] [CX-0587];
   - compete on durability, not price [CX-0218] [CX-0609];
   - early-life risk may be taken to win share [CX-0207], then re-priced after launch [CX-0215].
3. **The premium cap.** The CFM profile has no doctrine-premium cap: CFM has no payoff, and no CFM financial model exists. **Proposed cap (inference):** a future CFM player may give up at most $1.0B of PV per game (GE's half) for the objective. That is the engine's ε (README), so the objective only breaks near-ties. The airframers' open-fan premiums (1.7-2.9 on fps, 0 on NGSA) are paid by the airframers, not by CFM.
4. **Never break these for the objective:**
   - at least 20% better fuel burn [CX-0217];
   - durability [CX-0208];
   - test evidence for every date [CX-0009];
   - price/cost positive [CX-0929];
   - no launch-era pricing [CX-0930];
   - no unmodelled terms risk [CX-0440].

## 7. Per-turn objective check

Add to the referee's turn procedure (and the market cell's, for CFM reactions):
1. **Measure.** Run `whatif --run <RUN> --side control` on both airframers' sealed orders. Log `objectives.cfm` before and after: `nb_dominance` values and `gap_pp`, and `open_fan.first_eis`.
2. **Swap the engine.** Re-run each new launch on the other CFM engine, and on `cfm_ducted` if a rival maker's engine was chosen. Log the airframer's `delta_pv_b` change as the premium it paid or avoided.
3. **Check the slack.** Log 2045 minus `first_eis`. fps open-fan launches after 2035 have at most one year of slack, so re-test them with Delay Tactics and the certification inject, alone and together.
4. **Check the suppliers.** If Pratt & Whitney plays, log `gtf_upgrade` and any `pw_gtf2` selection. If Rolls-Royce plays, log any `rr_ultrafan_nb` selection. Record the `nb_dominance` gap.
5. **Check the doctrine.** Note whether any CFM reaction implied a price cut, a forced date or a refused airframer. Cite the id, and record any premium against the proposed $1.0B cap.

## 8. Gaps and modelling limits

- **CFM has no payoff, capex or levers.**
- **Rival engines are open in two-player runs.** `pw_gtf2` is PV-better than `cfm_ducted` for both airframers at every launch year, so `nb_dominance` rests on the airframers keeping the default **(inference)**.
- **Not modelled:** the installed base, aftermarket and fuel capability. Embraer and lobbying have no lever and no evidence item.
- **Open-fan risk is a fixed +1 year.** Nothing models certification failure. The `engine_maturity_slip` inject even narrows the open fan's cost.
- **The `equilibria` solver tries first-year launches only** (2026, 2029, 2032, 2035; README). It misses the PV-best NGSA 2027 open fan and fps 2028 ducted plans, and the pure Nash pair in §5.
- **The engine-option values are placeholders** (README): +1.5pp, 0.85 capture, +1 year.
- **The evidence has limits.** Safran's side is unknown, and Ali's own words end in March 2024 [CX-0013].

<details>
<summary>Commands</summary>

All from `/home/user/aero-engine-gameboard`, with `WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/runs_cfm_verify`. Scripts are in its `py/` folder; each `whatif` call is `python3 -m wargame.engine whatif --run <id> --side control` with the plan on stdin (`py/wi.py`).

- `python3 -m wargame.engine rules --scenario base --side control`; `rules --scenario replacement-wave --side control`; `rules --run v-base-sup --side control`; `injects --run v-base`; `rules --scenario base --side cfm` (rejected: no such side)
- `python3 -m wargame.engine new --run-id v-base --scenario base`; the same for `v-wave` (`replacement-wave`), `v-base-sup` and `v-wave-sup` (`--suppliers rolls_royce,pratt_whitney`), `v-base-slip`, `v-wave-slip`, `v-base-cert` and `v-wave-cert`
- `python3 -m wargame.engine inject --run v-base-slip --id engine_maturity_slip` (and `v-wave-slip`); `inject --run v-base-cert --id certification_scrutiny` (and `v-wave-cert`)
- `echo '{"boeing": {}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control` (status quo: 76.0%, `open_fan` not met)
- `python3 py/sweep.py <run> sweep_<run>.jsonl` for `v-base`, `v-wave`, `v-base-slip`, `v-wave-slip` (720 runs each): fps (Solo, Joint Venture) × 2026-2037 × all four engines against Airbus Do Nothing or NGSA 2026/29/32/35 ducted, and NGSA × 2026-2037 × all four engines against Boeing Do Nothing or fps 2026/29/32/35 Solo ducted. Read by `py/analyse.py` (metric counts), `py/analyse2.py` (cost table, best plans, premiums, maturity slip), `py/spill.py` (spillover, Joint Venture) and `py/pwrange.py` (`pw_gtf2` against `cfm_ducted`)
- `python3 py/pairs.py v-base pairs_v-base.jsonl` (and `v-wave`): every Boeing plan (Do Nothing, or fps Solo/Joint Venture × 2026-2037 × four engines) against every Airbus plan (Do Nothing, or NGSA × 2026-2037 × four engines), 4,753 pairs each. Read by `py/pairs_an.py` (cheapest plan meeting both metrics, best replies, pure Nash, metric counts, the fps 2029 / NGSA 2029 grid cell)
- `python3 py/checks.py` (output in `checks.txt`): `gtf_upgrade` alone and with NGSA 2029/2032 ducted, fps 2028 ducted or fps 2027 open fan; Rolls-Royce `uf_nb` with fps 2028 on `rr_ultrafan_nb`; Delay Tactics and the certification inject on fps open fans launched 2032-2037; `margin_at_eis` for fps 2026-2028 on both CFM engines
- `echo '{"launch": [{"program": "ngsa", "engine": "pw_gtf2", "year": 2028}]}' | python3 -m wargame.engine validate --run v-base --side airbus`; the same for fps on `rr_ultrafan_nb` and fps Joint Venture on `cfm_open_fan` with `--side boeing`
- `python3 wargame/profiles/build/cite_check.py wargame/profiles/cfm/objectives.md wargame/profiles/cfm/executives/evidence.jsonl --show`

</details>
