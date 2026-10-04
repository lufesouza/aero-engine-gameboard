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
| Open fan only | The airframer picks the engine: `{"launch": [{"program": "fps" or "ngsa", "engine": "cfm_open_fan", "year": Y}]}` | Partly | CFM cannot withhold the ducted engine, so "only" cannot be enforced. The open fan cannot enter service before 2045 (`available_eis`): an airframe ordered on it before 2037 waits, and `validate` warns |
| Ducted only | Same, with `"engine": "cfm_ducted"` (the default for fps and NGSA) | Partly | CFM cannot withhold the open fan either |
| Both | Both engines are always on offer to both airframers | Partly | This is the engine's default state |
| Partner with Embraer | None | No | The fps Joint Venture (`"variant": "jv"`) is Boeing-Embraer and leaves the engine choice unchanged. It narrows the open fan's cost for Boeing but does not close it (§5) |
| Lobby governments on emissions | None | No | Nearest: `tech_ready_year` 2035 and the `fuel_price_spike` inject (+1.5pp to every new product, whatever the engine), so it does not favour the open fan |

## 3. Enablers and constraints

| Item | Engine parameter (value from rules) | What our evidence says |
|---|---|---|
| Maintenance and overhaul base | Not modelled. `nb_dominance` counts engines on deliveries, not the installed base | A 78,000-engine installed base [CX-0994]; 70% of revenue supports it [CX-0898]; about 70% of LEAP shop visits by CFM by 2030 [CX-0219]; CFM powers about 75% of narrowbody flights [CX-0980] |
| Cash | Not modelled: CFM has no capex or payoff | More than 70% of deployable cash goes to shareholders [CX-0923]; capex at 2-3% of revenue [CX-0922]; R&D held, with no "program dividend" [CX-0174] [CX-0962] |
| Sustainable aviation fuel capability | Not modelled | Every GE and CFM engine in service can run on approved sustainable aviation fuel [CX-0508]; RISE is fuel-ready and hydrogen-capable [CX-0001] |
| Open fan certification risk | `cfm_open_fan` `eis_add` +1 year, and `available_eis` 2045: no entry into service before 2045. Each extra or waiting year costs 10% of program capex. `engine_maturity_slip` moves tech-ready 2 years later, to 2037, which does not reach a 2045 entry | The fly demo slipped from "the middle of this decade" [CX-0151] to "this decade" [CX-0211]; earliest-ever dust testing [CX-0222]; an open-fan Chief Mechanic for durability [CX-0223]. The partners' own window was earlier: "by 2035" (Safran's CEO) [CX-0152] and "by the middle of the next decade" (Culp) [CX-0608]. The game's 2045 is about ten years later; no leader in the evidence names 2045 |
| Airframer reluctance | `cfm_open_fan` `capture_mult` 0.85; market multipliers 0.75-1.25 | Entry into service is "really not for us to say" [CX-0205]; products launch "as our airframer and airline customers deem appropriate" [CX-0469] |
| Raw materials | Partly: `supply_chain_crunch` raises every player's strain ×1.5 (the airframers and any engine-maker player). CFM has no strain, so it is not hit | 80% of shortages came from 9 suppliers [CX-0613]; castings and forgings [CX-0750]; about 1% of titanium from Russia [CX-1258] |

## 4. How attainment is measured

| Metric id | What it measures | Target and years | Status quo |
|---|---|---|---|
| `nb_dominance` | CFM's share of narrowbody engines: each airframer's share × CFM fit. Fit is 1 once its new program enters service on `cfm_ducted` or `cfm_open_fan`, and 0 if it enters service on `pw_gtf2` or `rr_ultrafan_nb`. Before that, the incumbent fit applies: Boeing 1.0 (LEAP sole source), Airbus 0.60 (1 minus the GTF's 0.40). When P&W plays, Airbus's fit falls 5pp from three years after its GTF upgrade | At or above the status quo in 2040, 2045 and 2050 | 76.0% each year; met (gap 0.0pp) |
| `open_fan` | The first entry into service of any live program on `cfm_open_fan` | 2045 or earlier. Nothing on the open fan can enter service before 2045, so only 2045 meets it | None; not met |

## 5. What it takes

**The open fan metric.** The open fan cannot enter service before 2045. An airframe that would be ready earlier waits for it, so every open-fan launch from 2026 to 2037 enters service in exactly 2045 and meets the metric. That held in all 720 open-fan plans of my four sweeps, and in all 4,104 open-fan pairs of the full base and wave pair grids. A launch in year Y waits 2037 - Y years. A slip is absorbed while the airframe waits, so only late launches can miss:

| Open-fan fps launch | Delay Tactics or FAA certification inject | First entry into service | Met |
|---|---|---|---|
| 2026-2035 | Any: Delay Tactics in two turns, the certification inject, or both | 2045 | Yes |
| 2036 | Delay Tactics in turn 4, or the certification inject | 2045 | Yes |
| 2036 | Both | 2046 | **No** |
| 2037 | Either | 2046 (2047 with both) | **No** |

Neither touches NGSA: an NGSA open fan enters service in 2045 whatever its launch year.

**The dominance metric.** Every plan in which no airframer flies another maker's engine meets it. There were 0 failures in 1,440 such sweep runs (base, wave and both maturity-slip runs) and in 2,450 such pairs of the full base and wave grids. It fails only on another maker's engine:
- NGSA 2028 on `pw_gtf2`: CFM falls to 32.9/25.8/20.0% (gap -56.0pp, base);
- fps 2028 on `rr_ultrafan_nb`: gap -52.8pp (base, with suppliers, Rolls-Royce launching `uf_nb` in turn 1);
- with suppliers, P&W's GTF upgrade alone cuts CFM to 73.0% (-3.0pp). An NGSA on `cfm_ducted` (2029 or 2032) restores 100%. An fps 2028 ducted restores it in base (+0.37pp), not in wave (-1.3pp). An fps 2027 open fan fails in both (-3.0pp): it enters service only in 2045, so CFM stays at 73.0% to 2045.

**This is a live risk even without suppliers.** In two-player runs both airframers may order `pw_gtf2`, and it beats `cfm_ducted` by +0.3 to +2.2 at every launch year from 2026 to 2033 (rival at Do Nothing or a 2029 ducted launch). It stays ahead at every launch year to 2037, against every rival timing in the sweeps (+0.1 to +2.3).

**What the open fan costs the airframer.** The table compares the same launch year, with the rival at Do Nothing (fps Solo):

| Launch | Boeing fps, base: ducted / open / diff | wave diff | Airbus NGSA, base: ducted / open / diff | wave diff |
|---|---|---|---|---|
| 2026 | +13.50 / -30.51 / -44.01 | -39.05 | +34.64 / -15.04 / -49.69 | -44.17 |
| 2027 | +16.73 / -25.77 / -42.50 | -38.11 | +41.29 / -11.21 / -52.50 | -47.50 |
| 2028 | +19.09 / -21.48 / -40.57 | -36.81 | +46.47 / -7.67 / -54.13 | -49.74 |
| 2029 | +16.72 / -17.60 / -34.31 | -31.46 | +42.05 / -4.38 / -46.43 | -43.01 |
| 2032 | +10.95 / -8.03 / -18.97 | -18.00 | +30.66 / +4.08 / -26.58 | -25.30 |
| 2035 | +6.77 / -0.93 / -7.71 | -7.62 | +21.62 / +10.80 / -10.82 | -10.70 |
| 2037 | +4.67 / +2.74 / -1.93 | -1.92 | +16.65 / +14.49 / -2.16 | -2.14 |

The mechanism (rules, `margin_at_eis` and `validate`): most of the cost is the wait. A launch in year Y carries 2038 - Y extra development years (the +1 year plus the wait), each at 10% of program capex: 12 years (+120% capex) for a 2026 launch, 1 for a 2037 launch. Its ducted twin enters service in Y + 7 and starts capturing share up to twelve years earlier. The open fan's margin no longer depends on the launch year (27.1% at entry into service on fps, against 21.6-25.6% for ducted launches in 2026-2028): 2045 is after tech-ready 2035, so there is no early penalty to avoid. Only a 2037 launch does not wait, and even then the +1.5pp does not pay for a year's delay, 10% more capex and 15% less capture.

**Best plans and the objective premium** (premium = best PV minus best open-fan PV; rival on `cfm_ducted`):

| Scenario | Airframer vs rival | Best overall | Best on CFM | Best open fan | Premium vs best on CFM / overall |
|---|---|---|---|---|---|
| Base | Boeing vs Do Nothing | fps 2028 `pw_gtf2` +19.57 | fps 2028 ducted +19.09 | fps 2037 Solo +2.74 | 16.34 / 16.82 |
| Base | Boeing vs NGSA 2029 | fps 2028 `pw_gtf2` +8.96 | fps 2028 ducted +8.13 | fps 2037 Joint Venture -4.79 | 12.92 / 13.74 |
| Base | Airbus vs Do Nothing | NGSA 2028 `pw_gtf2` +48.22 | NGSA 2028 ducted +46.47 | NGSA 2037 +14.49 | 31.98 / 33.73 |
| Base | Airbus vs fps 2029 | NGSA 2028 `pw_gtf2` +32.44 | NGSA 2028 ducted +30.58 | NGSA 2037 -2.11 | 32.69 / 34.55 |
| Wave | Boeing vs Do Nothing | fps 2028 `pw_gtf2` +15.93 | fps 2028 ducted +15.33 | fps 2037 Solo +2.74 | 12.59 / 13.19 |
| Wave | Boeing vs NGSA 2029 | fps 2028 `pw_gtf2` +8.08 | fps 2028 ducted +7.23 | fps 2037 Joint Venture -3.21 | 10.44 / 11.29 |
| Wave | Airbus vs Do Nothing | NGSA 2028 `pw_gtf2` +43.81 | NGSA 2028 ducted +42.08 | NGSA 2037 +14.49 | 27.59 / 29.33 |
| Wave | Airbus vs fps 2029 | NGSA 2028 `pw_gtf2` +31.09 | NGSA 2028 ducted +29.19 | NGSA 2037 +1.64 | 27.55 / 29.45 |

**Rival timing.**
- **Boeing.** Its open-fan premium against its best CFM plan, with Airbus at Do Nothing or NGSA 2026/2029/2032/2035: base 16.34/10.35/12.92/14.65/15.67; wave 12.59/9.41/10.44/11.27/11.93. Its best open-fan plan is always fps 2037: Solo against Do Nothing, Joint Venture against a launched NGSA.
- **Airbus.** Its premium against its best CFM plan, with Boeing at Do Nothing or fps 2026/2029/2032/2035: base 31.98/30.61/32.69/33.99/34.56; wave 27.59/26.72/27.55/28.17/28.55. Its best open-fan plan is always NGSA 2037. NGSA 2028 on `pw_gtf2` beats its best CFM plan (NGSA 2028 ducted) by a further 1.5 to 1.9.
- **Never a best reply.** In the full pair grids the open fan is never either airframer's best reply, in either scenario: not for Boeing against any of 49 Airbus plans, not for Airbus against any of 97 Boeing plans.
- **Maturity slip.** With `engine_maturity_slip` no open-fan PV changes (2045 is after the slipped tech-ready year, 2037), while the best ducted plans move to 2030 and lose value. Boeing's premium against its best CFM plan falls to 6.4-11.8 in base and 6.8-9.8 in wave; Airbus's to 21.5-25.0 and 19.9-21.6. The best open-fan year stays 2037.
- **Spillover** (base, against the ducted twin). An fps open fan raises Airbus's PV by +0.8 to +20.7, because Boeing enters service later and captures share more slowly; the earlier the launch, the larger the gain. An NGSA open fan raises Boeing's by +0.3 to +12.7.
- **Joint Venture.** Embraer's share narrows the gap but never closes it. The Joint Venture open fan loses to its ducted twin at every launch year and rival timing: by 0.96 to 28.68 in base, against 1.48 to 44.40 Solo. Against Do Nothing the fps 2026 Joint Venture open fan loses 28.37 (base) and 24.65 (wave), against 44.01 and 39.05 Solo.

**The cheapest plan that meets both metrics** is fps 2037 Joint Venture on the open fan with NGSA 2028 on `cfm_ducted`: Boeing -5.51, Airbus +43.96 in base; Boeing -3.50, Airbus +37.94 in wave. NGSA enters service in 2035 and fps in 2045, so Airbus captures share for ten years. "Cheapest" means the smallest total gap to each side's best reply, over the full pair grid (4,753 pairs per scenario): 14.44 in base, 12.62 in wave.
- **Boeing carries most of it.** Its best reply to that NGSA is fps 2028 on `pw_gtf2` (+7.50), and its best CFM reply is fps 2028 ducted (+6.63). Flying the open fan instead costs it 12.14 in base and 10.13 in wave.
- **Airbus.** Its best reply to that fps is NGSA 2028 on `pw_gtf2` (+45.38 base, +39.56 wave). That breaks `nb_dominance`, so keeping Airbus on CFM costs it 1.43 (1.62 in wave).
- **With Airbus on the open fan,** the cheapest pair is fps 2028 ducted against the NGSA 2037 open fan: Boeing +16.18, Airbus -3.80 in base, a total gap of 34.57 (29.92 in wave).
- **The equilibrium misses both metrics.** In that grid the only pure Nash pair, in both scenarios, is fps 2028 on `pw_gtf2` against NGSA 2028 on `pw_gtf2` (Boeing +7.50, Airbus +30.19). CFM falls to 0% in 2040, 2045 and 2050 (-76.0pp) and no open fan flies. The grid covers narrowbody launches only: no widebody moves, Rate Increase or tactics.

Check: I reproduced the briefing grid's fps 2029 / NGSA 2029 cell in both scenarios (Boeing +5.76, Airbus +25.59). The grid is all ducted, so no row meets `open_fan`.

**Supplier levers CFM would need** (proposed, not in the engine) **(inference)**:
1. **Launch levers for `cfm_open_fan` and `cfm_ducted`**, with capex, development years and a fallback rule, as Rolls-Royce and Pratt & Whitney have. Only then can CFM offer one engine, the other, or both, and own the open fan's date instead of a fixed 2045.
2. **Standard or aggressive terms** to offset the 0.87 Boeing gains from `pw_gtf2` against an NGSA 2028 ducted, and Airbus's 1.5-1.9 from `pw_gtf2`. Terms cannot offset the open fan's premium (9.4-16.3 on fps, 26.7-34.6 on NGSA), which comes from the 2045 date.
3. **A one-time LEAP durability upgrade**, to counter the GTF upgrade.
4. **Two new levers:** a CFM-Embraer engine commitment and an emissions-lobbying lever, priced as a margin or tech-ready effect.

## 6. Fit with our doctrine

**Where the objective agrees with us.**
- **The open fan.** Culp is "all in" [CX-0214], calls it the most promising path to at least 20% [CX-0217], and keeps RISE funded [CX-0553] [CX-0174]. Ali argues it on physics [CX-0180] [CX-0183]. Safran's CEO set "by 2035" [CX-0152]; Culp says "by the middle of the next decade" [CX-0608]. The game does not use those dates: the open fan cannot enter service before 2045, about ten years later, and no leader in the evidence names 2045. The PV-best open-fan plan is NGSA 2037, in service 2045.
- **Dominance.** LEAP is sole source on the MAX [CX-0182], with a win rate above 70% on the A320 family since 2023 [CX-0218]. Culp wants "all the critical platforms" [CX-0587] and co-plans with the airframers [CX-0185] [CX-0193].

**Where it pulls against us.**
- **Share is not the goal:** "we're not going for share" [CX-0493]; "not the low bid" [CX-0250]; profitability over share (Ghai, of GE Power) [CX-0912]; pricing regardless of competitors [CX-0609]; no relative yardstick [CX-0600]. Yet `nb_dominance` is a relative share.
- **The airframer sets the date** [CX-0205]. CFM can offer the open fan but cannot make it fly.
- **Dates rest on tests:** "turn on and turn off" [CX-0009]; "not on the back of a theory" [CX-0008]. In the game no open fan can run ahead of GE's own words: 2045 is later than "by the middle of the next decade" [CX-0608]. The fly demo has slipped [CX-0151] [CX-0211]; whether the product date slips as far as 2045 is not in the evidence.
- **The open fan is never the airframer's best reply** in the game (§5). An airframer that orders it before 2037 pays 10% of program capex for each year it waits. Pressing an airframer into that wait would break the rule that the airframer sets the date [CX-0205] **(inference)**.
- **Durability comes first.** It is not traded for fuel burn [CX-0208]: "safety, quality, delivery and cost, always in that order" [CX-0658].
- **The CFO is wary of new-engine ramps** [CX-0933] [CX-0995] and is committed to cash returns [CX-0923].
- **The Safran gate.** RISE and narrowbody pricing need the partner [CX-0166] [CX-0184]. Consent is assumed **(inference)**.

**Weighing rule.**
1. **The objective sets the aim:** an open fan in service by 2045 (in the game, in 2045 exactly), and both new narrowbodies on CFM engines.
2. **The doctrine sets how:**
   - offer both engines to both airframers [CX-0185] [CX-0193];
   - never force the open fan or refuse an airframer [CX-0205] [CX-0587];
   - compete on durability, not price [CX-0218] [CX-0609];
   - early-life risk may be taken to win share [CX-0207], then re-priced after launch [CX-0215].
3. **The premium cap.** The CFM profile has no doctrine-premium cap: CFM has no payoff, and no CFM financial model exists. **Proposed cap (inference):** a future CFM player may give up at most $1.0B of PV per game (GE's half) for the objective. That is the engine's ε (README), so the objective only breaks near-ties. The airframers' open-fan premiums (9.4-16.3 on fps, 26.7-34.6 on NGSA; 6.4-25.0 with the maturity slip) are paid by the airframers, not by CFM. None is a near-tie, so in this game the cap never decides for the open fan.
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
3. **Check the wait and the slack.** An open fan meets the metric only with `first_eis` 2045. For each open-fan launch, log its wait (`eis` minus `planned_eis_at_launch`, or the `validate` warning): 2037 minus the launch year, at 10% of program capex a year. In turns 1-3 every open-fan launch waits; in turn 4 only a 2037 launch does not. The wait absorbs slips, so only late fps launches are at risk: a 2036 launch has one year of slack and a 2037 launch none. Re-test those with Delay Tactics and the certification inject, alone and together.
4. **Check the suppliers.** If Pratt & Whitney plays, log `gtf_upgrade` and any `pw_gtf2` selection. If Rolls-Royce plays, log any `rr_ultrafan_nb` selection. Record the `nb_dominance` gap.
5. **Check the doctrine.** Note whether any CFM reaction implied a price cut, a forced date or a refused airframer. Cite the id, and record any premium against the proposed $1.0B cap.

## 8. Gaps and modelling limits

- **CFM has no payoff, capex or levers.**
- **Rival engines are open in two-player runs.** `pw_gtf2` is PV-better than `cfm_ducted` for both airframers at every launch year, so `nb_dominance` rests on the airframers keeping the default **(inference)**.
- **Not modelled:** the installed base, aftermarket and fuel capability. Embraer and lobbying have no lever and no evidence item.
- **Open-fan timing is fixed:** +1 year, and no entry into service before 2045. Nothing models certification failure or an earlier RISE. The `engine_maturity_slip` inject leaves every open-fan PV unchanged and lowers the ducted plans, so it narrows the open fan's cost.
- **The 2045 date is a control assumption.** It is about ten years after the partners' stated window: "by 2035" [CX-0152] and "by the middle of the next decade" [CX-0608].
- **The `equilibria` solver tries first-year launches only** (2026, 2029, 2032, 2035; README). It misses 2037, the only open-fan launch year without a wait, the PV-best fps 2028 and NGSA 2028 plans, and the pure Nash pair in §5.
- **The engine-option values are placeholders** (README): +1.5pp, 0.85 capture, +1 year, 2045.
- **The evidence has limits.** Safran's side is unknown, and Ali's own words end in March 2024 [CX-0013].

<details>
<summary>Commands</summary>

All from `/home/user/aero-engine-gameboard`, with `WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/of_update/cfm`. All runs were made fresh after the open fan's 2045 date was committed (runs keep the config they were made with). Scripts are in its `py/` folder and outputs in `out/`; each `whatif` call is `python3 -m wargame.engine whatif --run <id> --side control` with the plan on stdin (`py/wi.py`).

- `python3 -m wargame.engine rules --scenario base --side control` (`engine_options.nb.cfm_open_fan.available_eis` 2045); `rules --scenario replacement-wave --side control`; `rules --run v-base-sup --side control`; `injects --run v-base`; `rules --scenario base --side cfm` (rejected: no such side)
- `python3 -m wargame.engine new --run-id v-base --scenario base`; the same for `v-wave` (`replacement-wave`), `v-base-sup` and `v-wave-sup` (`--suppliers rolls_royce,pratt_whitney`), `v-base-slip`, `v-wave-slip`, `v-base-cert` and `v-wave-cert`
- `python3 -m wargame.engine inject --run v-base-slip --id engine_maturity_slip` (and `v-wave-slip`); `inject --run v-base-cert --id certification_scrutiny` (and `v-wave-cert`)
- `echo '{"boeing": {}, "airbus": {}}' | python3 -m wargame.engine whatif --run v-base --side control` (status quo: 76.0%, `open_fan` not met)
- `python3 py/sweep.py <run> sweep_<run>.jsonl` for `v-base`, `v-wave`, `v-base-slip`, `v-wave-slip` (720 runs each): fps (Solo, Joint Venture) × 2026-2037 × all four engines against Airbus Do Nothing or NGSA 2026/29/32/35 ducted, and NGSA × 2026-2037 × all four engines against Boeing Do Nothing or fps 2026/29/32/35 Solo ducted. Read by `py/analyse.py` (metric counts, entry years), `py/analyse2.py` (cost table, best plans, premiums, maturity slip), `py/spill.py` (spillover, Joint Venture) and `py/pwrange.py` (`pw_gtf2` against `cfm_ducted`)
- `python3 py/pairs.py v-base pairs_v-base.jsonl` (and `v-wave`): every Boeing plan (Do Nothing, or fps Solo/Joint Venture × 2026-2037 × four engines) against every Airbus plan (Do Nothing, or NGSA × 2026-2037 × four engines), 4,753 pairs each. Read by `py/pairs_an.py` (cheapest plan meeting both metrics, best replies, pure Nash, metric counts, the fps 2029 / NGSA 2029 grid cell) and `py/pairs_an2.py` (best replies to the cheapest pair, the cheapest pair with an NGSA open fan, the open fan as a best reply)
- `python3 py/exact.py`, `py/exact_best.py` and `py/exact_slip.py`: the cost table, best plans and maturity-slip premiums recomputed from unrounded model values (`wargame.model`, the same config), to fix the second decimal
- `python3 py/checks.py` (`out/checks.txt`): `gtf_upgrade` alone and with NGSA 2029/2032 ducted, fps 2028 ducted or fps 2027 open fan; Rolls-Royce `uf_nb` with fps 2028 on `rr_ultrafan_nb`; Delay Tactics and the certification inject on fps open fans launched 2032-2037; `margin_at_eis` for fps 2026-2028 on both CFM engines. `python3 py/slips2.py` (`out/slips2.txt`): the certification inject with two turns of Delay Tactics on fps open fans launched 2026-2037
- `echo '{"launch": [{"program": "ngsa", "engine": "cfm_open_fan", "year": 2028}]}' | python3 -m wargame.engine validate --run v-base --side airbus` (warns: ready in 2036, waits 9 years; launch in 2037); the same for `pw_gtf2`, for fps on `rr_ultrafan_nb` and for fps Joint Venture 2026 on `cfm_open_fan` with `--side boeing` (waits 11 years)
- `python3 wargame/profiles/build/cite_check.py wargame/profiles/cfm/objectives.md wargame/profiles/cfm/executives/evidence.jsonl --show`

</details>
