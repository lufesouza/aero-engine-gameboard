# Assigned objectives: the referee's cross-player analysis

**Who reads this.** The referee only. Players cannot read `wargame/profiles/overview`. This file covers the five objectives from Boeing PD briefing slide 4. It sets out how they conflict, how many can be met at once, what that costs each player, what the replacement wave changes, and how to score them.

**Basis.** Engine numbers are `whatif --side control` runs of 2026-10-04 on four-player runs (`--suppliers rolls_royce,pratt_whitney`), base and replacement-wave. Two-player runs are used only for the `wave_grid.txt` cells. No injects, market multipliers 1.0, no widebody moves unless stated. Money is delta PV in $B, rounded half up to two decimals from the engine's three. Plan ids P1-P10 and check ids C1-C10 and G1-G5 are defined in the Commands list. Behavioural claims cite each player's own evidence file. (inference) marks my reading.

## 1. The five objectives

```text
Source: Boeing Product Development, 'Players - narrowbody market: Who plays, what they want, and what they can do', Aerospace Game-Theory Briefing (Boeing Strategy), slide 4. BOEING PROPRIETARY.

Boeing           Primary goal:   Hold the 50/50 NB market split; Defend incumbency
                 Possible moves: Launch fps with 7-year ramp-up | Launch fps with 10-year ramp-up | Launch fps via Embraer |
                                 Increase 737 production rate by 2030 | Do Nothing (Milk 737 MAX program)
Airbus           Primary goal:   Defend 60/40 edge; Protect A320 family
                 Possible moves: Launch NGSA ($20B) | Do Nothing (Milk A320neo family) | Delay fps (supply-chain bottleneck) |
                                 Delay fps (talent poaching)
CFM              Primary goal:   Dominate narrowbody engines; Introduce Open Fan
                 Possible moves: Open Fan only | Ducted only | Open + Ducted (both) | Partner with Embraer | Lobby governments on emissions
Pratt & Whitney  Primary goal:   Restore credibility; Capitalize on GTF investment
                 Possible moves: Launch GTF2 solo | Joint Venture with Rolls-Royce | Do Nothing (continue GTF1)
Rolls-Royce      Primary goal:   Enter narrowbody market; Keep Widebody dominance
                 Possible moves: Ultrafan widebody only (no NB entry) | Ultrafan narrowbody solo | Joint Venture with Pratt & Whitney |
                                 Do Nothing (continue Trent only)
```

The engine scores ten metrics. CFM is not a player, but the engine still scores its two metrics from the airframers' engine choices.

| Player | Goal in plain terms | Metric id (short name) | Met when | Status quo (P1) | Decided by |
|---|---|---|---|---|---|
| Boeing | Hold half the market; defend its 40% | `nb_share_50` (B50) | Boeing share at least 50% in 2040, 2045, 2050 | ✗ 40% (−10.0 pp) | Boeing's fps timing, and Airbus waiting |
| | | `defend_incumbency` (Bdef) | Boeing share never below the status-quo path (40%) in 2030-2050 | ✓ 0.0 pp | NGSA timing against fps |
| Airbus | Keep 60/40; protect the A320 family | `nb_share_60` (A60) | Airbus share at least 60% in 2040, 2045, 2050 | ✓ 0.0 pp | fps timing; Boeing's Rate Increase |
| | | `protect_a320` (Aprot) | Airbus at least 60% in 2030-2050, counted only before NGSA enters service | ✓ 0.0 pp | Boeing's Rate Increase and any fps lead |
| Rolls-Royce | Enter the narrowbody market; keep the widebody | `nb_entry` (RRnb) | narrowbody engines above 0.5 a year in 2045 and 2050 | ✗ 0 | an airframer selecting UltraFan |
| | | `wb_dominance` (RRwb) | widebody engines at or above the status quo (184.1 a year) in 2040-2050 | ✓ 184.1 | any rival widebody Re-engine |
| Pratt & Whitney | Restore credibility; keep the GTF base | `gtf_base` (PWbase) | narrowbody engines at or above the status quo (960 a year) in 2040-2050 | ✓ 960 | the NGSA engine, and the fps engine |
| | | `credibility` (PWcred) | GTF upgrade booked by 2031 | ✗ none | Pratt & Whitney alone |
| CFM | Dominate narrowbody engines; fly the open fan | `nb_dominance` (CFMdom) | CFM share of narrowbody engines at or above the status quo (76.0%) in 2040-2050 | ✓ 0.0 pp | both airframers' engines; the GTF upgrade |
| | | `open_fan` (CFMof) | an airframer flies the RISE open fan by 2045 | ✗ none | either airframer |

- **The status quo meets 6 of 10 in both scenarios.** Every one of the six is met with zero margin. Any rival gain in a counted year breaks it.
- **CFM's 76.0%** is Boeing's 40% (LEAP is sole source on the MAX) plus 60% of Airbus's 60% (the GTF holds the rest).

## 2. Conflicts and alignments

### 2.1 Zero-sum pairs

| Pair | Why | Engine evidence |
|---|---|---|
| B50 and A60 | Shares sum to 100%, and 50 + 60 is more than that | P10 base: Boeing at 51.0% meets B50; Airbus misses A60 by 26.0 pp |
| Bdef and A60 | Both hold only at exactly 40/60 in 2040-2050. In practice that means both enter service in the same year with no Rate Increase | The six tie plans (P4-P9) meet both. fps first (P2) breaks A60 by 23.0 pp. NGSA first (P3) breaks Bdef by 20.0 pp |
| Rate Increase and Airbus's metrics | The +2 pp lands in a counted year | In a 2036 tie, a Turn-1 (C3) or Turn-2 (C4) Rate Increase misses A60 and Aprot by 2.0 pp |
| B50 and Aprot | B50 needs an early fps lead, which shows before NGSA enters service (inference from the share rule) | P10: Aprot −26.0 pp |
| RRnb and CFMdom | An airframer on UltraFan gives CFM none of its deliveries. In a 40/60 tie CFM falls to 60% or 40% | P5 60%, P8 40%, P9 0% (fps also on GTF2). C10 meets both in base (+0.5 pp), but only with Airbus at 76.5% and Boeing at 23.5%, and misses in the wave (−6.2 pp) |
| PWbase and CFMdom | The same mechanism: a GTF2 or Joint Venture engine on a new airframe | P6, NGSA on GTF2: CFM 40% (−36.0 pp) |
| PWcred and CFMdom | The GTF upgrade moves 5 pp of A320neo engines to P&W until NGSA enters service | C1: the upgrade alone cuts CFM to 73.0% (−3.0 pp). A CFM-engined NGSA restores it to 100% (P3, P4, P7). An fps lead on CFM engines restores it in base only (P2 +0.6, P10 +1.95; wave −0.67, −0.13) |

**What the record says about these pairs.**
- **Boeing.** Its record backs Bdef, not B50. Calhoun said 50/50 "is not an objective of ours" [B-1936] and warned that chasing tier rank "gets you in trouble" [B-1980]. In 2012 the red line was not to let Airbus reach 60/40 [B-0602, B-0638].
- **Airbus.** A60 matches its stated aim "to maintain its market-leading position" [A-0200]. But management pay rests on EBIT, FCF and EPS [A-0310, A-0334], so a premium paid for share comes out of what it is paid on (inference).
- **CFM.** Culp says "we're not going for share" [CX-0493] but wants to be "on all the critical platforms" [CX-0587]. CFM's doctrine is closer to being on both airframes than to a 76% share test (inference).

### 2.2 Complementary objectives

- **RRnb and PWbase through the Joint Venture, on NGSA only.** In P8 the Joint Venture on NGSA gives each partner 1,200 engines a year, so both metrics are met. On fps it gives each partner 800 (P5, C9): RR meets its metric, P&W misses its 960. Half of Airbus's 60% clears the bar; half of Boeing's 40% does not.
- **The Joint Venture costs Rolls-Royce.**
  - In P8, RR earns +8.27. Solo on the same NGSA earns +15.99 and leaves P&W at −1.14 with 0 engines (C7).
  - RR's doctrine takes the Joint Venture only within $3B of Solo (RR profile, reaction triggers). RR wants a partner "to derisk" but "if it doesn't work, we can consider alternatives" [R-1010].
  - For P&W, joining is the best reply at P8 (premium 0). RTX says "you spread risk, you spread investment through JVs" [P-1233].
- **Separate airframes also serve both suppliers.** In P9 (fps on GTF2, NGSA on UltraFan Solo) RR delivers 2,400 engines and P&W 1,600. No Joint Venture is needed, and RR earns +17.80.
- **The open fan on NGSA fits Airbus and CFM.**
  - P7 (NGSA on the open fan, same entry year as fps) meets both Airbus and both CFM metrics. Airbus earns +27.59 (NGSA 2028 on the open fan) against +25.59 (NGSA 2029 ducted, P4); both enter service in 2036.
  - Airbus names the open fan as a focus [A-0226, A-0444].
- **The GTF upgrade is free for P&W and harmless to the airframers.** P&W earns +1.76 from it in Turn 1 and +1.36 in Turn 2 (C1, C2). Its only victim is CFMdom (2.1).

### 2.3 Objectives that turn on another player's choice

| Metric | Can the owner secure it alone? | Who decides | Engine evidence |
|---|---|---|---|
| B50 | No | Airbus must wait, and Boeing must break H1 (no Turn-1 fps) | P2: fps 2029 with a Turn-1 Rate Increase misses by 2.0 pp even with Airbus at Do Nothing. P10: fps 2027 + Turn-2 Rate Increase meets it in base (+1.0), misses in the wave (−3.63) |
| Bdef | Mostly: enter no later than NGSA | Airbus's NGSA timing | P3 −20.0 pp |
| A60 | Mostly: enter no later than fps | Boeing's fps timing and Rate Increase | P2 −23.0 pp; C3 −2.0 pp |
| Aprot | No | Boeing's Rate Increase | C3, C4 −2.0 pp even in a tie |
| RRnb | No | an airframer selecting UltraFan in a turn RR has launched it | met only in P5, P8, P9 |
| RRwb | Yes, unless a rival Re-engine | the engine on a 787 or A350 Re-engine | C5, 787 Re-engine on GE: 119.7, 102.7 and 85.7 engines against 184.1 |
| PWbase | No | the NGSA engine; the fps engine | NGSA on CFM: 0 (P3, P4, P7). NGSA on GTF2: 2,400 (P6). fps on GTF2: 1,600 (P9) |
| PWcred | Yes | Pratt & Whitney | C1, C2 |
| CFMdom | No: CFM has no levers | both airframers and P&W | C1; P5, P6, P8, P9 |
| CFMof | No | either airframer | met only in P7, P8 |

The suppliers know this. RR ties a launch to an airframe programme [R-0994, R-1005]. P&W needs a committed, sole-source airframe [P-0746]. CFM says entry into service is "really not for us to say" [CX-0205].

## 3. Joint feasibility

### 3.1 The plans

All fps launches are Solo; all supplier terms standard. P2-P10 add each supplier's Turn-1 default: the Trent 1000 upgrade (RR) and the GTF upgrade (P&W).

| Plan | Boeing | Airbus | Rolls-Royce | Pratt & Whitney | Entry into service fps / NGSA |
|---|---|---|---|---|---|
| P1 Status quo | Do Nothing | Do Nothing | Do Nothing | Do Nothing | none / none |
| P2 fps first | Rate Increase T1; fps 2029 ducted | Do Nothing | upgrade | upgrade | 2036 / none |
| P3 NGSA first | Do Nothing | NGSA 2028 ducted | upgrade | upgrade | none / 2035 |
| P4 Same year | fps 2029 ducted | NGSA 2029 ducted | upgrade | upgrade | 2036 / 2036 |
| P5 fps on UltraFan, Joint Venture | fps 2029 UltraFan | NGSA 2029 ducted | upgrade; `uf_nb` Joint Venture 2029 | upgrade; join T2 | 2036 / 2036 |
| P6 NGSA on GTF2 | fps 2029 ducted | NGSA 2029 GTF2 | upgrade | upgrade; `gtf_next` 2029 | 2036 / 2036 |
| P7 NGSA on the open fan | fps 2029 ducted | NGSA 2028 open fan | upgrade | upgrade | 2036 / 2036 |
| P8 Engine split | fps 2029 open fan | NGSA 2030 UltraFan | upgrade; `uf_nb` Joint Venture 2030 | upgrade; join T2 | 2037 / 2037 |
| P9 Two new engines | fps 2029 GTF2 | NGSA 2029 UltraFan | upgrade; `uf_nb` Solo 2029 | upgrade; `gtf_next` 2029 | 2036 / 2036 |
| P10 Boeing chases 50% | fps 2027 ducted; Rate Increase T2 | Do Nothing | upgrade | upgrade | 2034 / none |

P10 breaks Boeing's H1 (no Turn-1 fps) and H2 (no entry before 2035).

### 3.2 Attainment and delta PV

✓ met, ✗ missed. **Boeing and Airbus cells** give the gap in pp: the worst counted year minus the target, or minus the status-quo path. **RR**: lowest narrowbody engines a year (2045-2050) · lowest widebody engines (2040-2050). **P&W**: lowest narrowbody engines (2040-2050) · upgrade year. **CFM**: dominance gap in pp · first open-fan entry year.

**Base**

| Plan | Boeing: 50% · defend | Airbus: 60% · A320 | RR: NB engines · WB engines | P&W: NB engines · upgrade | CFM: dominance · open fan | Met | ΔPV Boeing | Airbus | RR | P&W |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| P1 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 184.1 | ✓ 960 · ✗ none | ✓ 0.0 · ✗ none | 6 | +0.00 | +0.00 | +0.00 | +0.00 |
| P2 | ✗ −2.0 · ✓ +2.0 | ✗ −23.0 · ✗ −23.0 | ✗ 0 · ✓ 204.1 | ✗ 666 · ✓ 2026 | ✓ +0.6 · ✗ none | 4 | +17.58 | −12.61 | +0.82 | +0.90 |
| P3 | ✗ −30.0 · ✗ −20.0 | ✓ +7.5 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 5 | −3.40 | +46.47 | +0.82 | −1.74 |
| P4 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 6 | +5.76 | +25.59 | +0.82 | −1.42 |
| P5 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 800 · ✓ 204.1 | ✗ 800 · ✓ 2026 | ✗ −16.0 · ✗ none | 6 | +7.33 | +25.59 | +5.18 | +5.64 |
| P6 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✓ 2,400 · ✓ 2026 | ✗ −36.0 · ✗ none | 6 | +5.76 | +27.35 | +0.82 | +0.43 |
| P7 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✓ 2036 | 7 | +5.76 | +27.59 | +0.82 | −1.42 |
| P8 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 1,200 · ✓ 204.1 | ✓ 1,200 · ✓ 2026 | ✗ −36.0 · ✓ 2037 | 8 | +3.57 | +26.32 | +8.27 | +9.91 |
| P9 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 2,400 · ✓ 204.1 | ✓ 1,600 · ✓ 2026 | ✗ −76.0 · ✗ none | 7 | +6.55 | +29.11 | +17.80 | −1.49 |
| P10 | ✓ +1.0 · ✓ 0.0 | ✗ −26.0 · ✗ −26.0 | ✗ 0 · ✓ 204.1 | ✗ 612 · ✓ 2026 | ✓ +1.95 · ✗ none | 5 | +17.51 | −14.33 | +0.82 | +0.79 |

**Replacement wave**

| Plan | Boeing: 50% · defend | Airbus: 60% · A320 | RR: NB engines · WB engines | P&W: NB engines · upgrade | CFM: dominance · open fan | Met | ΔPV Boeing | Airbus | RR | P&W |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| P1 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 184.1 | ✓ 960 · ✗ none | ✓ 0.0 · ✗ none | 6 | +0.00 | +0.00 | +0.00 | +0.00 |
| P2 | ✗ −4.83 · ✓ +2.0 | ✗ −18.98 · ✗ −18.98 | ✗ 0 · ✓ 204.1 | ✗ 738 · ✓ 2026 | ✗ −0.67 · ✗ none | 3 | +14.73 | −10.29 | +0.82 | +1.06 |
| P3 | ✗ −27.58 · ✗ −17.58 | ✓ +3.77 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 5 | −2.49 | +42.08 | +0.82 | −1.74 |
| P4 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 6 | +5.76 | +25.59 | +0.82 | −1.42 |
| P5 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 800 · ✓ 204.1 | ✗ 800 · ✓ 2026 | ✗ −16.0 · ✗ none | 6 | +7.33 | +25.59 | +5.18 | +5.64 |
| P6 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✓ 2,400 · ✓ 2026 | ✗ −36.0 · ✗ none | 6 | +5.76 | +27.35 | +0.82 | +0.43 |
| P7 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✓ 2036 | 7 | +5.76 | +27.59 | +0.82 | −1.42 |
| P8 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 1,200 · ✓ 204.1 | ✓ 1,200 · ✓ 2026 | ✗ −36.0 · ✓ 2037 | 8 | +3.57 | +26.32 | +8.27 | +9.91 |
| P9 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 2,400 · ✓ 204.1 | ✓ 1,600 · ✓ 2026 | ✗ −76.0 · ✗ none | 7 | +6.55 | +29.11 | +17.80 | −1.49 |
| P10 | ✗ −3.63 · ✓ 0.0 | ✗ −20.18 · ✗ −20.18 | ✗ 0 · ✓ 204.1 | ✗ 717 · ✓ 2026 | ✗ −0.13 · ✗ none | 3 | +13.13 | −10.57 | +0.82 | +1.04 |

- **P8 meets the most objectives: 8 of 10, in both scenarios.** No other plan reaches 8. P7 and P9 meet 7.
- **Tie plans are the same in both scenarios.** P4-P9 give identical results because nobody captures share, so the wave weight has nothing to scale.
- **Supplier players leave the airframers' PVs unchanged while the airframers fly CFM engines.** P2 gives Boeing +17.58 and P3 gives Airbus +46.47, the same as the two-player values in the Boeing and Airbus briefs.

### 3.3 Why 8 is the ceiling

This follows from the metric definitions (inference), and each step is checked by the runs cited.
1. **B50 and A60 cannot both hold**, so at most 9.
2. **Bdef with A60 needs a 40/60 tie** (2.1). In a tie, RRnb rules out CFMdom, because CFM keeps at most 60% (P5, P8, P9). That caps a tie at 8.
3. **Without a tie, at most 7.**
   - **If Airbus leads,** Bdef and B50 fail. RRnb, CFMdom and PWbase then cannot all hold. CFM would need its airframer at 76% or more once the UltraFan airframe is in service (C10). That leaves the UltraFan airframer 24% or less, and P&W's half of its engines is at most 480 a year, short of 960.
   - **If Boeing leads,** A60 fails, and either B50 fails or the lead it needs breaks Aprot (2.1). RRnb and CFMdom cannot both hold either. Boeing cannot reach 76% by 2040, and Airbus cannot exceed 60% while Boeing leads.
4. **In a tie, 8 needs RRnb, PWbase, PWcred, CFMof, Aprot and RRwb all at once.**
   - CFMof needs one airframer on the open fan, and RRnb needs the other on UltraFan.
   - PWbase then needs NGSA on the UltraFan Joint Venture with P&W (1,200 engines, P8). The swap with fps on the Joint Venture gives 800 (C9). NGSA on UltraFan Solo gives 0 (C7).
   - So **P8's structure is the only route to 8**: fps on the open fan, NGSA on the RR-P&W Joint Venture, the same entry year, no Rate Increase, the GTF upgrade by Turn 2, and no rival widebody Re-engine.

Within Boeing's H1 the earliest such tie is 2037: an fps open fan launched in Turn 2 enters service in 2037. Breaking H1 brings it to 2035 (C6: fps 2027, NGSA 2028, all Turn-1 orders). C6 also meets 8 and raises every PV: Boeing +4.96, Airbus +32.12, RR +9.94, P&W +11.59. It also breaks two RR rules: no Turn-1 UltraFan launch (itself an inference in RR's profile) and no Trent 1000 upgrade while an UltraFan is in development.

### 3.4 The premium each player pays at P8

**Definitions.**
- **Premium:** the player's best reply, with the other players' orders held fixed, minus its PV in the plan.
- **"In its hard rules":** the replies kept after the filters the engine can test:
  - Boeing H1-H2: fps only in 2029, 2032 or 2035;
  - Airbus rules 1, 4 and 8, and the 2028-2030 window;
  - RR: standard terms, no Turn-1 launch;
  - P&W: standard terms.
- **Grids:**
  - Boeing, 388 replies: Rate Increase timing × fps year × engine × Solo or Joint Venture;
  - Airbus, 343: NGSA year × engine × Delay Tactics turns, with Poaching left out because it moves no metric;
  - RR, 98;
  - P&W, 200.
- **Own-objective premium:** the best reply minus the best reply that meets as many of the player's own metrics as any reply can.

Both suppliers' best replies keep their Turn-1 upgrades.

| Player | ΔPV in P8 (base / wave) | Best reply in its hard rules | ΔPV (base / wave) | Premium (base / wave) | Best reply, any | Premium (base / wave) | Own-objective premium | Cap |
|---|---:|---|---:|---:|---|---:|---:|---|
| Boeing | +3.57 / +3.57 | Rate Increase T3, fps 2029 UltraFan Solo | +9.64 / +8.88 | 6.07 / 5.31 | Rate Increase T3, fps 2028 ducted Solo | 7.06 / 5.38 | 0.00 | $2B (H8) |
| Airbus | +26.32 / +26.32 | Delay Tactics T4, NGSA 2028 ducted | +34.38 / +30.74 | 8.05 / 4.42 | Delay Tactics T3+4, NGSA 2027 open fan | 10.38 / 6.45 | 0.00 | $3B |
| Rolls-Royce | +8.27 / +8.27 | uf_nb 2030 Solo | +15.99 / +15.99 | 7.73 / 7.73 | uf_nb 2030 Solo | 7.73 / 7.73 | 0.00 | $3B a turn |
| Pratt & Whitney | +9.91 / +9.91 | join T2, no gtf_next | +9.91 / +9.91 | 0.00 / 0.00 | join T2, no gtf_next | 0.00 / 0.00 | 0.00 | $1B |

**Who pays for whose objective at P8**, in hard rules, one lever at a time (base / wave):

| Payer | Concession in P8 | Cost | Objective it protects | Run |
|---|---|---:|---|---|
| Boeing | the open fan instead of UltraFan at the same entry year (2037) | 2.81 / 2.81 | CFM `open_fan` | B1u |
| Boeing | entry in 2037 instead of 2036 (no lead) | 2.28 / 1.52 | Airbus `nb_share_60` | B2u |
| Boeing | no Turn-3 Rate Increase | 0.98 / 0.98 | Airbus `nb_share_60`, `protect_a320` | best reply |
| Airbus | NGSA in 2037 instead of 2036 on UltraFan (no lead) | 4.87 / 3.68 | Boeing `defend_incumbency` | A2 |
| Airbus | UltraFan in 2030 instead of ducted in 2028 plus one Delay Tactics turn | 3.18 / 0.74 | Boeing `defend_incumbency`; RR `nb_entry`; P&W `gtf_base` | best reply |
| Rolls-Royce | the Joint Venture instead of Solo | 7.73 / 7.73 | P&W `gtf_base` | C7 |
| Pratt & Whitney | none | 0 | | |

- **Own objectives are free at P8.** Every player's best reply already meets as many of its own metrics as it can. The whole premium, 21.85 in base and 17.45 in the wave, buys other players' objectives.
- **Three players pay above their caps:** Boeing 6.07 against $2B, Airbus 8.05 against $3B, RR 7.73 against $3B. No doctrine provides for paying toward another player's objective (inference). P8 will not come from doctrine play without a disclosed deal.
- **The engine choice costs Airbus nothing.** UltraFan is worth +3.22 to Airbus over the ducted engine at the same date (A1). Airbus's premium is all about timing: it gives up the lead.
- **Two readings lower the in-rules figures:**
  - **Boeing.** H6 (no Rate Increase as a response to Airbus) may bar the Turn-3 Rate Increase. Without it, fps 2029 on UltraFan (B2u) puts Boeing's premium at 5.09 / 4.33.
  - **Airbus.** Its Turn-4 Delay Tactics leave NGSA first either way. They therefore fail the default team's test that Delay Tactics change who enters service first (Airbus brief §5.2). Without them, NGSA 2028 ducted (A3) puts Airbus's premium at 6.37 / 3.78.

**Premiums in hard rules at the high-attainment plans** (base / wave):

| Plan | Met (of 10) | Boeing | Airbus | Rolls-Royce | Pratt & Whitney | Total |
|---|---:|---:|---:|---:|---:|---:|
| P4 | 6 | 0.90 / 0.90 | 6.86 / 4.26 | 0.00 / 0.00 | 0.00 / 0.00 | 7.76 / 5.17 |
| P7 | 7 | 0.90 / 0.90 | 4.86 / 2.26 | 0.00 / 0.00 | 0.00 / 0.00 | 5.76 / 3.16 |
| P9 | 7 | 1.76 / 1.76 | 3.34 / 0.74 | 0.00 / 0.00 | 0.31 / 0.31 | 5.41 / 2.81 |
| P8 | 8 | 6.07 / 5.31 | 8.05 / 4.42 | 7.73 / 7.73 | 0.00 / 0.00 | 21.85 / 17.45 |

- **P9 is the cheapest of these plans.** In the wave every premium sits inside its cap. In base only Airbus's 3.34 exceeds its $3B, by 0.34. I compared four plans and unilateral replies only (inference).
- **P9's premiums by payer:**
  - **Boeing** pays 0.78 for P&W's base (GTF2 instead of UltraFan, 9-B1) and 0.98 for Airbus's metrics (no Turn-3 Rate Increase).
  - **Airbus** pays 1.47 / 0.08 for not entering first (9-A2), plus 1.87 / 0.66 for a Turn-4 Delay Tactics turn. Both protect Boeing's `defend_incumbency`.
  - **P&W's 0.31** is launch timing (`gtf_next` 2030 instead of 2029, 9-W1). No objective is at stake.
- **P8 adds CFM's open fan to P9's seven.** It costs 16.44 more in base and 14.65 in the wave. RR's Joint Venture accounts for 7.73. The rest falls on the airframers: Boeing's open fan, and a tie one year later (2037), which raises what each gives up by not leading.

## 4. What the replacement wave changes

**Mechanism.** The wave scales only the leader's yearly capture. The weight is 0.4 through 2036, 0.428 in 2037, 0.648 in 2040, 1.0 in 2044, 0.981 in 2045 and 1.0 from 2046 (`rules`). The base scenario is unchanged.

| Effect | Base | Wave | Run |
|---|---|---|---|
| Ties (P4-P9): attainment and PV | as in 3.2 | identical | P4-P9 |
| Boeing first: Boeing share in 2040 | 48.0% | 45.17% | P2 |
| Boeing first: Airbus `nb_share_60` gap | −23.0 pp | −18.98 pp | P2 |
| Airbus first: Boeing `defend_incumbency` gap | −20.0 pp | −17.58 pp | P3 |
| Airbus first: Airbus `nb_share_60` margin | +7.5 pp | +3.77 pp | P3 |
| Boeing chases 50% (fps 2027 + Rate Increase T2) | met, +1.0 pp | missed, −3.63 pp | P10 |
| fps 2026 against Airbus Do Nothing, two-player: Boeing in 2040, `nb_share_50` | 50.5%, met | 44.97%, missed | G1 |
| fps 2032 against NGSA 2029, two-player: Boeing PV | +0.26 | +1.99 | G4 |
| CFM dominance, fps first with the GTF upgrade | +0.6, +1.95 pp | −0.67, −0.13 pp | P2, P10 |
| Value of entering first at P8: Boeing / Airbus | 2.28 / 4.87 | 1.52 / 3.68 | B2u, A2 |

**Timing.** The wave does not move the best launch years. In both scenarios the best in-rules replies at P4, P7, P8 and P9 are fps 2029 and NGSA 2028; the best replies of any kind are fps 2028 and NGSA 2027. The fps 2029 / NGSA 2029 grid cell is +5.76 / +25.59 in both (G3), and Boeing's fps 2026 drops from +13.50 to +8.54 (G1).

**Harder in the wave:**
- **`nb_share_50`.** Even an fps launched in 2026 (G1) or in 2027 with a Rate Increase (P10) misses.
- **`nb_dominance`** when Boeing leads on CFM engines while the GTF upgrade is in place (P2, P10 flip to missed).
- **The value of leading**, for both airframers.

**Easier in the wave:**
- **The follower's metric.** `defend_incumbency` after an NGSA lead and `nb_share_60` after an fps lead miss by less (P2, P3), but still miss.
- **Holding a tie.** Every high-attainment plan is a tie, and a tie is cheaper to hold because the lead it forgoes is worth less. Total in-rules premium at P8 falls from 21.85 to 17.45; at P9 from 5.41 to 2.81. The RR Joint Venture premium (7.73) does not change.

**Unchanged:**
- `protect_a320` under a Rate Increase (C3, C4);
- `wb_dominance`, `credibility` and `open_fan`;
- the supplier engine counts in ties.

`gtf_base` still fails when fps leads (P2 738, P10 717 engines in 2050).

**Not modelled from slide 7.**
- **Retirement timing** enters only as the capture weight. The weight is the same for both sides, although about 73% of the replacements are Airbus types.
- **Product lifecycle, eroding MAX share and margin, and new competitors** are not modelled.

## 5. Guidance for the referee

### 5.1 Scoring attainment

1. **Score each metric met or missed** on the final projection (`scorecard --final` or `report`), and keep the by-turn table.
2. **Report the gap:**
   - pp for B50, Bdef, A60, Aprot and CFMdom;
   - engines short of the bar for RRnb (0.5 a year), RRwb (184.1) and PWbase (960);
   - the booked year for PWcred and the first open-fan year for CFMof.
3. **Score against what was attainable, not against 10.**
   - The joint ceiling is 8 (3.3), and the status quo already gives 6.
   - B50 needs a Turn-1 fps and an Airbus that waits.
   - For Boeing, 1 of 2 is a full score unless Airbus waited (inference).
   - RR's `nb_entry` and P&W's `gtf_base` need an airframer's selection.
   - CFM's result reflects other players' choices, not CFM skill.
4. **Do not add attainment across players into one score** (inference). The metrics conflict by design.

### 5.2 Premium paid against the doctrine cap

1. **Recompute each declared objective premium** with `whatif` at the decision turn: the best allowed reply minus the chosen orders, with the other players' actual orders held fixed.
2. **Split it into three parts:**
   - own-objective premium, allowed within the cap;
   - doctrine premium;
   - money spent on another player's objective.
   At P8 the first part is 0 for everyone.
3. **Compare the sum of the first two with the cap:**
   - Boeing $2B (H8, shared with any doctrine premium);
   - Airbus $3B (shared);
   - Rolls-Royce $3B a turn;
   - Pratt & Whitney $1B (shared);
   - CFM none: it has no PV, and its brief proposes $1.0B for a future CFM player (inference).
4. **Flag these cases:**
   - a premium above the cap;
   - money spent on another player's objective without a disclosed deal;
   - an "objective premium" claimed where the best reply already met the objective. That is a mislabelled doctrine premium.

### 5.3 Did the player pursue its objective sensibly?

| Player | Sensible | Not sensible |
|---|---|---|
| Boeing | Plays for Bdef: fps enters service no later than NGSA. Tracks B50 without chasing it, since 50/50 "is not an objective of ours" [B-1936]. Ducted engine by default; Boeing chose engines on maturation depth [B-0613] and worries about new-engine durability [B-2304] | A Turn-1 fps to reach 50%: current programmes come first [B-2276], Boeing sets no dates [B-2313] and said "not before '35" [B-2061]. Paying above $2B for another player's objective, such as 2.81 for the open fan at P8 |
| Airbus | NGSA in 2028-2030, matching the expected engine choice around 2027 [A-0182] and entry "around 2037" [A-0409]. At most one Delay Tactics turn: integrity is one of the five pillars in its first 2026 objective [A-0331]. Engine choice by PV: UltraFan or the open fan costs Airbus nothing at the same date (A1; P7 against P4) | A second Delay Tactics turn for A60 (red line 4). NGSA entering service before 2035 (rule 1) |
| Rolls-Royce | `uf_nb` only against an announced airframe [R-0994, R-1005]. Solo where an airframer has picked UltraFan. The Trent 1000 upgrade in Turn 1 | A speculative launch to reach `nb_entry`; RR says narrowbody is optional, "we don't need to do it" [R-1011], and puts profit before share [R-1582]. A Joint Venture 7.73 below Solo booked as RR's own objective premium |
| Pratt & Whitney | The GTF upgrade in Turn 1 or 2, its standard fix [P-0786]; "time on wing ... is the name of the game" [P-1355]. Joining a Joint Venture on NGSA when offered. GTF2 only for a disclosed airframe | `gtf_next` with no committed airframe beyond the $1B cap [P-0746, P-0711]. Discounts past launch mode [P-0735] |
| CFM (not a player) | When the market cell or referee voices CFM, check it against "we're not going for share" [CX-0493], the airframer setting the date [CX-0205], and no trade of durability for fuel burn [CX-0208] | A CFM reaction that cuts price for share or forces an open-fan date |

### 5.4 Modelling limits to state in the after-action review

- **Unmodelled moves.**
  - **Boeing.** No lever separates the 7-year from the 10-year ramp-up; capture after entry is fixed at 1.5 pp a year times the multipliers. The Embraer route is modelled as the fps Joint Venture.
  - **CFM.** Its choice to offer the open fan, the ducted engine or both is only partly modelled, because CFM cannot withhold an engine. A CFM partnership with Embraer and emissions lobbying have no lever.
  - **P&W.** Its Joint Venture is RR's UltraFan, not a GTF-based engine.
  - **Enablers with no lever:** government incentives, workforce, the A220-500, MRO scale, and cash or debt limits.
- **NGSA at $20B against the engine's $25B.** At $20B Airbus's PV rises by 4.48 (P3), 4.15 (P4, P9) and 3.84 (P8). No metric and no other player's PV changes.
- **MAX share and margin erosion under Do Nothing is not modelled.** P1 holds Boeing at 40% in every year of both scenarios. Slide 7 expects erosion. Do Nothing is therefore flattered, and `defend_incumbency` under Do Nothing reads met when it may not be (inference).
- **CFM is not a player.** It has no PV, levers or premium. Its attainment is a by-product of others' choices. The GTF upgrade alone breaks `nb_dominance` (C1).
- **Scoring limits.**
  - Metrics are read at five-year marks only.
  - The engine counts are binary: 800 engines scores like 2,400.
  - `credibility` measures spending, not durability.
  - New programmes are sole source: a rival engine takes a whole airframe's deliveries.
  - Engine-option values and strain are placeholders.
- **Limits of this analysis.**
  - Replies are unilateral and the grids are finite. No four-player equilibrium was computed.
  - No injects or market multipliers.
  - Engine selection has no maturity or reputation test once a supplier has launched. Real airframers weigh maturity: Boeing chose LEAP on its maturation depth [B-0613].

<details>
<summary>Commands</summary>

```bash
cd /home/user/aero-engine-gameboard
export WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/runs_conflicts
mkdir -p $WARGAME_RUNS_DIR
python3 -m wargame.engine new --run-id oc-base --scenario base --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id oc-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id oc2-base --scenario base                 # two-player, wave_grid.txt cells
python3 -m wargame.engine new --run-id oc2-wave --scenario replacement-wave
python3 -m wargame.engine new --run-id oc20-base --scenario base --suppliers rolls_royce,pratt_whitney --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
python3 -m wargame.engine new --run-id oc20-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
for s in boeing airbus rolls_royce pratt_whitney; do python3 -m wargame.engine rules --run oc-base --side $s; done   # assigned_objectives (Section 1)
python3 -m wargame.engine rules --run oc-base --side control    # engine options, share rule, leader cap 0.8, CFM metrics
python3 -m wargame.engine rules --run oc-wave --side control    # capture_weight_by_year (Section 4)

# Every plan and check is one whatif with the plan on stdin. Turn keys: 1 = 2026-28, 2 = 2029-31, 3 = 2032-34, 4 = 2035-37. P8:
echo '{"boeing": {"2": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_open_fan", "year": 2029}]}},
 "airbus": {"2": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2030}]}},
 "rolls_royce": {"1": {"t1000_upgrade": true}, "2": {"launch": [{"program": "uf_nb", "variant": "jv_pw", "terms": "standard", "year": 2030}]}},
 "pratt_whitney": {"1": {"gtf_upgrade": true}, "2": {"join_rr_jv": true}}}' | python3 -m wargame.engine whatif --run oc-base --side control   # and --run oc-wave

# Scripts in /tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/objectives/oc/
# (run from that folder with the same WARGAME_RUNS_DIR; each calls the whatif above through subprocess):
python3 plans.py --json plans_out.json   # P1-P10 orders (PLANS) on oc-base and oc-wave: Sections 1, 2, 3.2, 4
python3 br.py P8 P7 P9 P4                # best replies: Boeing 388, Airbus 343, RR 98, P&W 200 per plan and run (3.4, 4)
python3 make_tables.py > tables.md       # re-runs P1-P10 and the best-reply grids; prints the tables of 3.2 and 3.4
python3 decomp.py                        # one-lever swaps at P8 (B1, B1u, B2, B2u, B3-B5, A1-A5, R1, R2, W1, W2) and P9 (9-B1, 9-B2, 9-A1, 9-A2, 9-W1)
python3 checks.py                        # C1 upgrades only; C2 GTF upgrade T2; C3, C4 Rate Increase T1, T2 in P4; C5 787 Re-engine on GE;
                                         # C6 P8 at 2035 (Turn-1 orders); C7 P8 with RR Solo; C8 P8 with fps ducted; C9 Joint Venture on fps,
                                         # open fan on NGSA 2028; G1-G5 two-player cells (fps 2026 / none; none / NGSA 2026; 2029 / 2029;
                                         # 2032 / 2029; 2029 / none; Solo, ducted)
python3 checks2.py                       # C10 NGSA 2026 ducted, fps 2037 on UltraFan Solo (RR uf_nb 2037); NGSA at $20B for P3, P4, P8, P9
python3 verify_prose.py                  # checks every engine number in the prose against the outputs above (52 checks)
# Citations
python3 wargame/profiles/build/cite_check.py wargame/profiles/overview/objectives_analysis.md wargame/profiles/boeing/evidence.jsonl \
  wargame/profiles/airbus/evidence.jsonl wargame/profiles/rolls_royce/evidence.jsonl wargame/profiles/pratt_whitney/evidence.jsonl \
  wargame/profiles/cfm/executives/evidence.jsonl --show
```

</details>
