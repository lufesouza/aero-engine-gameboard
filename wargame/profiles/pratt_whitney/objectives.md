# Pratt & Whitney: assigned objective

Our mission from control, how the engine scores it, what it costs and how it fits our doctrine. Built from our profile, reaction function, calibration memo, evidence file and engine runs with both engine makers playing. Money is P&W delta PV in $B. Commands are listed at the end.

## 1. Assigned objective

Source: assigned by control for this scenario.

> **Primary goal:** Restore credibility; Capitalize on GTF investment
>
> **Possible moves:**
> - Launch GTF2 solo
> - Joint Venture with Rolls-Royce
> - Do Nothing (continue GTF1)
>
> **Enablers:** Mature gearbox technology; RTX leverage; cash from GTF base
>
> **Constraints:** GTF reputation issues; engineering resources

## 2. Moves to levers

Each lever checked against `rules --side pratt_whitney`.

| Briefing move | Game lever and how to order it | Modelled | Notes |
|---|---|---|---|
| Next-generation GTF, Solo | `"launch": [{"program": "gtf_next", "year": Y, "terms": "standard"}]`; Y = 2028 in turn 1, the airframer's year later (§5) | yes | 6 years, $4.5B P&W-net, $1.05M per engine mature, ramp from -0.35 over 10 years. Earns only if fps or NGSA names `pw_gtf2` while it is live. One launch per game: a cancelled one cannot be relaunched. A missing `year` books 2026 (+0.45 against +1.98). |
| Joint Venture with Rolls-Royce | `"join_rr_jv": true` in the turn RR launches `uf_nb` as `jv_pw` | partly | `rules` marks it yes. But it is RR's UltraFan narrowbody (`rr_ultrafan_nb`), **not a GTF-based Joint Venture**; no lever pairs RR with our GTF. RR chooses the variant. We pay 50% of $7.5B, earn 50% of RR's $3.1M per engine on RR's ramp, and cannot leave once it launches. |
| Do Nothing (continue GTF) | no orders | yes | Keeps 40% of A320neo engines: 960 a year. |
| Not on the slide: GTF durability upgrade | `"gtf_upgrade": true` | yes | The `credibility` proxy. $1.0B over 3 years; +5pp of A320neo deliveries from 3 years later until NGSA enters service; saves $0.45B a year for 9 years. Books in the first year of the turn ordered. |
| Not on the slide: terms, `pw_wb`, cancel | `"terms": "aggressive"`; launch `pw_wb`; `"cancel": ["gtf_next"]` | yes | Aggressive: +1.1pp airframer margin, paid for by a price concession of (1 - 0.71) x the $1.05M mature value, about $0.30M per engine. `pw_wb` cannot move a narrowbody metric. |

## 3. Enablers and constraints

| Item | Engine parameter (value from `rules`) | What our evidence says |
|---|---|---|
| Mature gearbox technology | `gtf_next` 6 development years (UltraFan 7 Solo, 6 in the Joint Venture); `pw_gtf2` eis_add 0 (UltraFan +1), margin +0.5pp (UltraFan +1.0pp), capture 0.95 | The next engine stays inside the geared architecture [P-0772][P-0790], sized at 5-6 years [P-0712]. RR claims a favourable geared IP position [P-2004]. It buys a year, not a bigger airframer margin. |
| RTX leverage | WACC 0.085, alpha 0.35; no funding limit | The parent funds programs Pratt alone could not [P-1138][P-0330][P-0378]; GS has RTX free cash flow at $8.14bn (2026E) to $9.80bn (2028E) [P-1964]. Never binds. |
| Cash from the GTF base | Airbus narrowbody fit 0.40 at $0.6M per engine: 960 engines, about $0.58B a year (calibration memo) | 40% of A320neo engines [P-1771][P-0111]; net GTF EBIT breaks even only in 2027E [P-1782]. Not a funding source in the engine. |
| GTF reputation issues | not modelled as a standing parameter. Nearest: `pw_gtf2` capture 0.95; the -0.35 ramp; the `gtf_durability_crisis` inject (incumbent value -50% for 4 years) | Time on wing about half the V2500's in 2023 [P-1014]; a $2.9bn net powder-metal charge [P-1563]; durability doubts cost campaigns [P-0074] and left airlines unhappy [P-0163]. Selection does not respond to reputation. |
| Engineering resources | strain $1.5B at full overlap over 5 years (PLACEHOLDER), on any two overlapping P&W windows; the Joint Venture relieves half | In 2019 we said we were entering a harvest phase after the GTF investment [P-1234], which argues against another large program (inference). Engine (strain component of `whatif`): `gtf_next` 2026 with the upgrade 2026 costs $1.12B of strain; 2028, $0.34B; the Joint Venture, $0.17B. |

## 4. How attainment is measured

| Metric id | What it measures | Target and years | Status quo |
|---|---|---|---|
| `gtf_base` | P&W narrowbody engines delivered a year, all airframers, Joint Venture share included | at or above the status quo (within 0.5 of an engine) in 2040, 2045 and 2050 | 960 a year (2,000 x 60% x 2 x 0.40): **met** |
| `credibility` | the year `gtf_upgrade` is booked | 2031 or earlier | no upgrade: **missed** |

`whatif` shows `gtf_base` as values against `status_quo`, with no `gap_pp`. From the `rules` values: with the upgrade our A320neo engines are 1,800 x Airbus share, so `gtf_base` holds only while Airbus keeps 53.3% (60% without it). A new airframe flying our engine needs only 24% share; a Joint Venture airframe needs 48%. A new airframe on another engine sets our fit on it to zero.

## 5. What it takes

**`credibility`** (base and replacement-wave identical): order `gtf_upgrade` in turn 1 (books 2026, +1.76) or turn 2 (2029, +1.36). Ordered in turn 3 it books 2032 (+1.06) and misses. The PV-best plan already meets it: **objective premium 0**.

**`gtf_base`**, by airframer outcome. P&W orders the upgrade in turn 1 in every row. Base / replacement-wave.

| Airframer outcome | Plan that meets `gtf_base` | ΔPV | Best-PV P&W plan | ΔPV | Premium |
|---|---|---|---|---|---|
| No new narrowbody through 2037 | upgrade only (Do Nothing also meets) | +1.76 / +1.76 | same | same | 0 |
| NGSA 2028 names `pw_gtf2` | `gtf_next` 2028, standard | +1.98 / +1.62 | same | same | 0 |
| NGSA 2028 on UltraFan `jv_pw` | `join_rr_jv` in turn 1 | +14.91 / +14.11 | same | same | 0 |
| fps 2029 names `pw_gtf2` | `gtf_next` 2029 (2031) | +3.04 / +2.79 (+3.07 / +2.90) | same | same | 0 |
| fps 2028 names `pw_gtf2`, NGSA 2028 on CFM | `gtf_next` 2028 | -2.05 / -2.05 | no launch (fps falls back to CFM) | -1.74 / -1.74 | 0.31 / 0.31 |
| fps 2032 names `pw_gtf2`, NGSA 2029 on CFM | `gtf_next` 2034 | -1.96 / -1.79 | no launch | -1.42 / -1.42 | 0.54 / 0.37 |
| NGSA on CFM or Solo UltraFan, any year 2026-2035 | none | | upgrade only | -1.74 / -1.74 (2028) | unreachable |
| fps alone on CFM, any year 2026-2035 | none | | upgrade only | +1.04 / +1.25 (2028) | unreachable |

The last two rows are the trap. Every NGSA launch I ran (2026-2035) on a rival engine leaves us zero engines from its entry into service (NGSA 2035 on CFM: 1,080 / 0 / 0). fps alone on CFM erodes Airbus share: 2050 engines are 621 (fps 2026) to 864 (fps 2035) in the base, 742 to 867 in the wave. All 180 base and wave pairs in the three sweeps agree on met or missed. The wave lowers our payoff from a selected engine (NGSA 2028 ours: +1.62 against +1.98) but changes no verdict.

**The decision we actually face.** Orders are simultaneous, so `gtf_base` stays reachable only if `gtf_next` is live when the airframer chooses. The real objective premium is the cost of a hedge nobody selects. Turn 1, NGSA, upgrade 2026, `gtf_next` 2028, cancelled in turn 2 if unselected:

| | Base | Wave |
|---|---|---|
| Gain if NGSA names us (vs falling back to CFM: -1.74) | 3.72 | 3.36 |
| Cost if nobody does (+0.56 vs +1.76; -2.94 vs -1.74) | 1.20 | 1.20 |
| PV break-even odds p* | 0.24 | 0.26 |
| Expected objective premium at p = 0.2 (profile §6, turn 1 with RR in play) | 0.22 | 0.29 |
| Odds at which the premium reaches $1B | 0.04 | 0.04 |

For `join_rr_jv`, given RR launches `jv_pw` in 2028: +14.91 if NGSA takes UltraFan against -1.74 out; -1.95 if nobody does against +1.76. Break-even odds 0.18 (wave 0.19); the premium reaches $1B at 0.13 (wave 0.14). Airbus prefers UltraFan: NGSA 2028 gains it +4.02 against +1.75 for our engine (wave +3.92 / +1.74). Boeing's fps 2028 gains +1.58 against +0.48 (wave +1.63 / +0.60).

Broader cover costs too much. Joining and launching `gtf_next` together meets `gtf_base` whichever P&W engine NGSA picks, but pays +9.61 (UltraFan) or -2.44 (ours): $5.30B or $4.42B below the single lever (wave +8.81 / -2.80, the same gaps). Aggressive terms on a selected NGSA give -2.63 (wave -2.82), below losing it (-1.74).

**How it depends on the rival's timing.**
- Airbus's own timing payoffs point to turn 1: NGSA alone earns it +34.65 in 2026, +46.47 in 2028, +42.05 in 2029 and +30.66 in 2032 (wave +29.13, +42.08, +38.63, +29.38).
- The hedge is one shot and cannot be carried cheaply (base). Launched in 2028 and kept, it is worth +1.45 / +0.51 / +0.09 / -0.98 if NGSA picks it in 2029 / 2031 / 2032 / 2035, against +2.13 / +1.77 / +1.61 / +1.21 for a launch in NGSA's year. Carrying it one more turn with nobody selecting costs $2.20B (-1.64 against +0.56). A cancelled `gtf_next` cannot be relaunched.
- The turn's-last-year rule holds in turn 1 only (base). NGSA 2026 with `gtf_next` 2028: P&W +2.56, Airbus +39.42 (same year: +1.66, +36.85). Later, a last-year launch delays NGSA's entry into service and costs Airbus far more than it gains us: NGSA 2029 with `gtf_next` 2031 gives P&W +2.22 and Airbus +36.36, against +2.13 and +43.64 for 2029. For 2032: +1.69 / +26.06 against +1.61 / +31.84. Both late launches leave Airbus better off on CFM (+42.05 and +30.66), so a late commitment would likely lose the selection (inference).
- Earlier fps launches hurt `gtf_base` more (621 against 864 engines in 2050).

## 6. Fit with our doctrine

**Where the objective agrees with our behaviour.**
- `credibility` is our standard answer to every durability problem: fix forward with an upgrade [P-0786][P-0758][P-1298]; "time on wing ... is the name of the game" [P-1355]. The profile already orders it in turn 1.
- `gtf_base` is franchise defence. Missing a cycle shuts a supplier out for decades [P-1347], and on the A320neo we committed on our own readiness [P-1868].
- It asks only for the status quo, not growth. That fits taking profitable share at 40-50% [P-1292]. Do Nothing meets it if no airframer moves. We welcome a late NGSA [P-1312] and plan on one around the mid-2030s [P-2058].
- The Joint Venture route matches spreading risk and investment through Joint Ventures [P-1233], as with GE [P-1676].

**Where it pulls against it.**
- We wait for a committed airframe and sole source [P-0711][P-0739][P-0737][P-0746]. The objective wants a hedge at odds down to about 0.05 (§5), not only above the profile's 0.45.
- Our plan holds no new centreline engine [P-0745]. Yet every NGSA we ran on a rival engine fails `gtf_base`.
- fps alone on CFM fails `gtf_base`, which pulls toward an fps hedge. We do not launch for "bragging rights" [P-0702], and a launch without a committed airframer breaks our red line.
- Winning a selection on price would meet `gtf_base`, against our no-deep-discount rule [P-0735][P-1333].
- Meeting it through UltraFan scores RR's engine as ours. That pulls against evolving inside the geared architecture [P-0772] and integrated teams [P-1240]. RR's own view is that a Joint Venture holds only while both partners are on the same new engine [P-1875].

**Weighing rule (inference).** The objective sets what we aim for: be on whichever new narrowbody enters service, and book the upgrade by turn 2. The doctrine sets how.
1. Red lines first, never traded for the objective (profile Quick card, §9 step 8): no `gtf_next` aimed at fps without a disclosure; no aggressive terms unless the §6 test holds; no `pw_wb`; no dividend cut; never share our core technology.
2. One cap. The profile keeps a doctrine-favoured order only while it trails the best expected PV by $1B or less (§9 step 8). An objective premium counts against that same $1B in the same turn. Doctrine premium plus objective premium never exceeds $1B.
3. Inside the cap, where the doctrine-favoured order (wait, stay out) and the objective-favoured order (hedge, join) differ, take the objective's. The doctrine then sets the form: NGSA only (the franchise exception [P-1347]); standard terms; 2028 in turn 1 and the airframer's year afterwards; disclose the commitment; cancel in the next turn if unselected; never carry a hedge.
4. Effective thresholds (inference, rounded up to cover both scenarios): hedge NGSA at p ≥ 0.05, in the turn Airbus is likeliest to launch (profile: 0.45); join at P(UltraFan selected | `jv_pw`) ≥ 0.14 (profile: 0.23); fps only on a disclosure.

## 7. Per-turn objective check

Add after §9 step 7 of the decision procedure.
1. **Status now.** Read `your_objectives` in `brief`, or run `whatif` with this turn empty. Log `gtf_base` engines for 2040 / 2045 / 2050 against 960, and the booked upgrade year.
2. **Scenario runs.** For each case in your `prediction` (NGSA on CFM, on `pw_gtf2`, on UltraFan; fps likewise; nobody), run `whatif --side pratt_whitney` on the candidate orders. Record ΔPV and `gtf_base` met for each. Compute P(met) = Σ p x met.
3. **Premium.** Objective premium = best expected PV minus the chosen order's. Add any doctrine premium; the sum stays at or under $1B. Drop any order that breaks a red line.
4. **Credibility guard.** If `gtf_upgrade` is not booked, order it now. Turn 2 is the last turn that books by 2031.
5. **Log in the rationale:** both metrics before and after the chosen orders, P(met), the premium paid and the lever that carries it.

## 8. Gaps and modelling limits

- **The credibility proxy measures spending, not durability.** It reads met once `gtf_upgrade` books by 2031, and nothing revokes it. With `gtf_durability_crisis` applied in turn 1 it still reads met, and the upgrade moves only from +1.76 to +1.73 because the crisis also hits the status quo. It ignores time on wing, removals, compensation and the rating [P-1014][P-1563][P-1554]. It does not raise any airframer's incentive to choose `pw_gtf2`. It says nothing about a new engine's first-time durability, our own GTF lesson [P-1214][P-1095].
- **`gtf_base` counts engines, not value.** It counts half of every UltraFan Joint Venture engine as ours, which is not capitalising on the GTF (inference). It looks only at 2040, 2045 and 2050.
- **New programs are sole source.** Fit is 1 or 0, so a rival engine on NGSA takes the whole base. A dual-sourced NGSA would leave part of it (inference).
- **Selection odds are inference.** Nothing in our evidence shows how an airframer chooses between our engine and UltraFan (profile §10).
- **Scale and asymmetry.** The game's A320neo engine flow is about 2x real installs (calibration memo). Our Joint Venture half is booked at RR's per-engine value and ramp.
- **Not modelled:** RTX leverage and GTF cash as funding limits; reputation as a selection driver. Strain is a PLACEHOLDER.
- **Not run:** market multipliers, Delay Tactics, slips and other injects.

<details>
<summary>Commands</summary>

From `/home/user/aero-engine-gameboard`, with `WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/runs_pratt_whitney`:

```
python3 -m wargame.engine new --run-id pw-base --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id pw-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id pw-crisis --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine inject --run pw-crisis --id gtf_durability_crisis
python3 -m wargame.engine rules --run pw-base --side pratt_whitney   # also pw-wave
echo '<stdin>' | python3 -m wargame.engine whatif --run pw-base --side control   # also pw-wave, pw-crisis
echo '{"cancel": ["uf_nb"]}' | python3 -m wargame.engine validate --run pw-base --side pratt_whitney   # rejected
```

Stdin per case (U = `"gtf_upgrade": true`; G(y) = `"launch": [{"program": "gtf_next", "year": y, "terms": "standard"}]`; turn keys "1"-"4" = 2026-28, 2029-31, 2032-34, 2035-37):
- Upgrade: `{"pratt_whitney": {"1": {U}}}`, keys "2", "3"; Do Nothing `{"pratt_whitney": {"1": {}}}`.
- NGSA: `{"airbus": {"1": {"launch": [{"program": "ngsa", "engine": "cfm_ducted", "year": 2028}]}}, "pratt_whitney": {"1": {U}}}`. Years 2026-2035 (matching key), with and without U. `pw_gtf2` with G(NGSA year or turn's last year) in NGSA's turn; G(2028) with `"terms": "aggressive"`; G(2026); G with no `year`. Strain is the `strain` entry of `components_pv_b`.
- UltraFan: NGSA on `rr_ultrafan_nb` plus `"rolls_royce": {"1": {"launch": [{"program": "uf_nb", "variant": "jv_pw", "year": 2028, "terms": "standard"}]}}` and `"pratt_whitney": {"1": {U, "join_rr_jv": true}}`; also unselected (NGSA on CFM or none), with G(2028) added, and RR `"variant": "solo"` without the join.
- Hedge: `"pratt_whitney": {"1": {U, G(2028)}, "2": {"cancel": ["gtf_next"]}}` with NGSA on CFM or none; carried: cancel in "3"; held: NGSA 2029-2035 on `pw_gtf2` or CFM, no cancel.
- fps: `{"boeing": {"1": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2028}]}}, "pratt_whitney": {"1": {U}}}`, years 2026-2035, and `pw_gtf2` / `rr_ultrafan_nb` with G or the join as above.
- Both: (fps, NGSA) = (2026, 2026), (2028, 2028), (2029, 2029), (2026, 2029), (2029, 2032), (2032, 2029); engines CFM/CFM, CFM/`pw_gtf2`, `pw_gtf2`/CFM, both ours, CFM/UltraFan `jv_pw`.
- Relaunch: U and G(2028) in "1", cancel in "2", G(2032) in "3" with NGSA 2032 on `pw_gtf2`: refused.

Generated by `pw_sweep.py`, `pw_sweep2.py`, `pw_sweep3.py` in the runs directory; results in `sweep1.jsonl` (236 cases), `sweep2.jsonl` (165), `sweep3.jsonl` (14). The sweeps hold 180 base and wave pairs (118, 55 and 7); the other 55 rows are `pw-crisis`.

Fact-check re-run: the same `new` and `inject` commands as runs `v-base`, `v-wave` and `v-crisis` in `WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/runs_pratt_whitney_verify`. Copies of the three sweeps (`rep_pw_sweep*.py` in `.../scratchpad/objectives/pwv/`) reproduce all 415 rows exactly. Targeted checks `c1.py` to `c5.py` in the same folder re-run every number in §2-§8, including NGSA and fps on CFM for each launch year 2026-2035 and Solo UltraFan for each NGSA year.

</details>
