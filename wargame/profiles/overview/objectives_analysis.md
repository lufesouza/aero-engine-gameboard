# Assigned objectives: the referee's cross-player analysis

**Updated 2026-10-04: the open fan is available from 2045 only.**

**Who reads this.** The referee only. Players cannot read `wargame/profiles/overview`. This file covers the five objectives from Boeing PD briefing slide 4. It sets out how they conflict, how many can be met at once, what that costs each player, what the replacement wave changes, and how to score them.

**Basis.** Engine numbers are `whatif --side control` runs of 2026-10-04 on four-player runs (`--suppliers rolls_royce,pratt_whitney`), base and replacement-wave, created after the CFM RISE open fan (`cfm_open_fan`) got its 2045 date (`available_eis`). An airframe on the open fan cannot enter service before 2045. If it would be ready earlier, it waits, and each waiting year costs 10% of programme capex. A 2037 launch enters service in 2045 with no wait. Two-player runs are used only for the `wave_grid.txt` cells. No injects, market multipliers 1.0, no widebody moves unless stated. Money is delta PV in $B, rounded half up to two decimals from the engine's three. Plan ids P1-P13, check ids C1-C14 and G1-G5, and lever ids such as 9-B1 are defined in the Commands list. Behavioural claims cite each player's own evidence file. (inference) marks my reading.

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
| | | `open_fan` (CFMof) | an airframer flies the RISE open fan by 2045. It cannot enter service earlier, so the entry year must be 2045 | ✗ none | either airframer, entering service in 2045 |

- **The status quo meets 6 of 10 in both scenarios.** Every one of the six is met with zero margin. Any rival gain in a counted year breaks it.
- **CFM's 76.0%** is Boeing's 40% (LEAP is sole source on the MAX) plus 60% of Airbus's 60% (the GTF holds the rest).

## 2. Conflicts and alignments

### 2.1 Zero-sum pairs

| Pair | Why | Engine evidence |
|---|---|---|
| B50 and A60 | Shares sum to 100%, and 50 + 60 is more than that | P10 base: Boeing at 51.0% meets B50; Airbus misses A60 by 26.0 pp |
| Bdef and A60 | Both hold only at exactly 40/60 in 2040-2050. In practice that means both enter service in the same year with no Rate Increase | The tie plans (P4, P5, P6, P9, P11) meet both. fps first (P2) breaks A60 by 23.0 pp. NGSA first (P3) breaks Bdef by 20.0 pp |
| CFMof and the open-fan airframer's own share metric | The open fan enters service in 2045 at the earliest, 8 to 10 years after a rival entering in 2035-2037. The airframer that picks it hands its rival the lead | fps on the open fan: Bdef −11.4 pp (P8), −14.25 pp (P13). NGSA on the open fan: A60 −13.5 pp and Aprot −6.0 pp (P7). Only a 2045 tie avoids this, and then both airframers wait (P11) |
| Rate Increase and Airbus's metrics | The +2 pp lands in a counted year | In a 2036 tie, a Turn-1 (C3) or Turn-2 (C4) Rate Increase misses A60 and Aprot by 2.0 pp |
| B50 and Aprot | B50 needs an early fps lead, which shows before NGSA enters service (inference from the share rule) | P10: Aprot −26.0 pp |
| RRnb and CFMdom | An airframer on UltraFan gives CFM none of its deliveries. In a 40/60 tie CFM falls to 60% or 40% | P5 60%, C8 40%, P9 0% (fps also on GTF2). With NGSA leading on UltraFan, 28.6% (P8) and 25.75% (P13) by 2045. C10 meets both in base (+0.5 pp), but only with Airbus at 76.5% and Boeing at 23.5%, and misses in the wave (−6.2 pp) |
| PWbase and CFMdom | The same mechanism: a GTF2 or Joint Venture engine on a new airframe | P6, NGSA on GTF2: CFM 40% (−36.0 pp) |
| PWcred and CFMdom | The GTF upgrade moves 5 pp of A320neo engines to P&W until NGSA enters service | C1: the upgrade alone cuts CFM to 73.0% (−3.0 pp). A CFM-engined NGSA restores it to 100% once in service (P3, P4, P12). An open-fan NGSA enters too late for 2040: CFM is at 73.0% in a 2045 tie (P11) and 75.7% behind an fps lead (P7). Without the upgrade, P11 meets CFMdom (C12). An fps lead on CFM engines restores it in base only (P2 +0.6, P10 +1.95; wave −0.67, −0.13) |

**What the record says about these pairs.**
- **Boeing.** Its record backs Bdef, not B50. Calhoun said 50/50 "is not an objective of ours" [B-1936] and warned that chasing tier rank "gets you in trouble" [B-1980]. In 2012 the red line was not to let Airbus reach 60/40 [B-0602, B-0638].
- **Airbus.** A60 matches its stated aim "to maintain its market-leading position" [A-0200]. But management pay rests on EBIT, FCF and EPS [A-0310, A-0334], so a premium paid for share comes out of what it is paid on (inference).
- **CFM.** Culp says "we're not going for share" [CX-0493] but wants to be "on all the critical platforms" [CX-0587]. CFM's doctrine is closer to being on both airframes than to a 76% share test (inference).

### 2.2 Complementary objectives

- **RRnb and PWbase through the Joint Venture, on NGSA only.** In a 2037 tie with NGSA on the Joint Venture (C8) each partner gets 1,200 engines a year, so both metrics are met. On fps it gives each partner 800 (P5, C6): RR meets its metric, P&W misses its 960. Half of Airbus's 60% clears the bar; half of Boeing's 40% does not.
- **The Joint Venture costs Rolls-Royce.**
  - In P8, RR earns +9.73. Solo on the same NGSA earns +18.92 and leaves P&W at −1.14 with 0 engines (C7). At P13 the gap is 11.55 (13-R1).
  - RR's doctrine takes the Joint Venture only within $3B of Solo (RR profile, reaction triggers). RR wants a partner "to derisk" but "if it doesn't work, we can consider alternatives" [R-1010].
  - For P&W, joining is the best reply at P8 and P13 (premium 0). RTX says "you spread risk, you spread investment through JVs" [P-1233].
- **Separate airframes also serve both suppliers.** In P9 (fps on GTF2, NGSA on UltraFan Solo) RR delivers 2,400 engines and P&W 1,600. No Joint Venture is needed, and RR earns +17.80.
- **The open fan no longer fits either airframer's share objective.**
  - An airframe launched on it in 2028-2030 waits 7 to 9 years for 2045 (9 in P7, 8 in P8) and pays 10% of capex for each year. NGSA 2028 on the open fan (P7) puts Airbus at −24.26 against +25.59 for the ducted tie (P4), and misses A60 and Aprot. fps 2029 on the open fan (P8) puts Boeing at −25.22 and misses Bdef.
  - Airbus rule 8 (no engine that pushes NGSA past 2037) now rules the open fan out for NGSA. Airbus still names the open fan as a focus [A-0226, A-0444]; in the game that interest can only be served after 2045 (inference).
  - Both on the open fan (P11) keeps the tie and meets CFMof, but both airframers wait until 2045: Boeing +0.13 and Airbus +9.39, against +5.76 and +25.59 in P4.
- **The GTF upgrade is free for P&W and harmless to the airframers.** P&W earns +1.76 from it in Turn 1 and +1.37 in Turn 2 (C1, C2). Its only victim is CFMdom (2.1), also in a 2045 tie (P11 against C12).

### 2.3 Objectives that turn on another player's choice

| Metric | Can the owner secure it alone? | Who decides | Engine evidence |
|---|---|---|---|
| B50 | No | Airbus must wait, and Boeing must break H1 (no Turn-1 fps) | P2: fps 2029 with a Turn-1 Rate Increase misses by 2.0 pp even with Airbus at Do Nothing. P10: fps 2027 + Turn-2 Rate Increase meets it in base (+1.0), misses in the wave (−3.63). An fps on the open fan cannot lead, so it cannot meet B50 |
| Bdef | Mostly: enter no later than NGSA | Airbus's NGSA timing; Boeing's engine | P3 −20.0 pp. fps on the open fan: P8 −11.4 pp, P13 −14.25 pp |
| A60 | Mostly: enter no later than fps | Boeing's fps timing and Rate Increase; Airbus's engine | P2 −23.0 pp; C3 −2.0 pp. NGSA on the open fan: P7 −13.5 pp |
| Aprot | No | Boeing's Rate Increase | C3, C4 −2.0 pp even in a tie |
| RRnb | No | an airframer selecting UltraFan in a turn RR has launched it | met only in P5, P8, P9, P13 |
| RRwb | Yes, unless a rival Re-engine | the engine on a 787 or A350 Re-engine | C5, 787 Re-engine on GE: 119.7, 102.7 and 85.7 engines against 184.1 |
| PWbase | No | the NGSA engine; the fps engine | NGSA on CFM: 0 once it enters service (P3, P4, P12). NGSA on GTF2: 2,400 (P6). fps on GTF2: 1,600 (P9) |
| PWcred | Yes | Pratt & Whitney | C1, C2 |
| CFMdom | No: CFM has no levers | both airframers and P&W | C1; P5, P6, P8, P9, P13 |
| CFMof | No | an airframer entering service in exactly 2045. Within the hard rules only Boeing can (Airbus rule 8) | met only in P7, P8, P11, P12, P13 |

The suppliers know this. RR ties a launch to an airframe programme [R-0994, R-1005]. P&W needs a committed, sole-source airframe [P-0746]. CFM says entry into service is "really not for us to say" [CX-0205].

## 3. Joint feasibility

### 3.1 The plans

All fps launches are Solo; all supplier terms standard. P2-P13 add each supplier's Turn-1 default: the Trent 1000 upgrade (RR) and the GTF upgrade (P&W). P11-P13 are new: open-fan plans that respect the 2045 date.

| Plan | Boeing | Airbus | Rolls-Royce | Pratt & Whitney | Entry into service fps / NGSA |
|---|---|---|---|---|---|
| P1 Status quo | Do Nothing | Do Nothing | Do Nothing | Do Nothing | none / none |
| P2 fps first | Rate Increase T1; fps 2029 ducted | Do Nothing | upgrade | upgrade | 2036 / none |
| P3 NGSA first | Do Nothing | NGSA 2028 ducted | upgrade | upgrade | none / 2035 |
| P4 Same year | fps 2029 ducted | NGSA 2029 ducted | upgrade | upgrade | 2036 / 2036 |
| P5 fps on UltraFan, Joint Venture | fps 2029 UltraFan | NGSA 2029 ducted | upgrade; `uf_nb` Joint Venture 2029 | upgrade; join T2 | 2036 / 2036 |
| P6 NGSA on GTF2 | fps 2029 ducted | NGSA 2029 GTF2 | upgrade | upgrade; `gtf_next` 2029 | 2036 / 2036 |
| P7 NGSA on the open fan | fps 2029 ducted | NGSA 2028 open fan | upgrade | upgrade | 2036 / 2045 |
| P8 Engine split | fps 2029 open fan | NGSA 2030 UltraFan | upgrade; `uf_nb` Joint Venture 2030 | upgrade; join T2 | 2045 / 2037 |
| P9 Two new engines | fps 2029 GTF2 | NGSA 2029 UltraFan | upgrade; `uf_nb` Solo 2029 | upgrade; `gtf_next` 2029 | 2036 / 2036 |
| P10 Boeing chases 50% | fps 2027 ducted; Rate Increase T2 | Do Nothing | upgrade | upgrade | 2034 / none |
| P11 Both on the open fan | fps 2037 open fan | NGSA 2037 open fan | upgrade | upgrade | 2045 / 2045 |
| P12 Open-fan fps against a ducted NGSA | fps 2037 open fan | NGSA 2028 ducted | upgrade | upgrade | 2045 / 2035 |
| P13 Open-fan fps against an UltraFan NGSA | fps 2037 open fan | NGSA 2028 UltraFan | upgrade; `uf_nb` Joint Venture 2028 (Turn 1) | upgrade; join T1 | 2045 / 2035 |

Rules these plans break:
- **P10** breaks Boeing's H1 (no Turn-1 fps) and H2 (no entry before 2035).
- **P7 and P11** break Airbus rule 8: the open fan pushes NGSA past 2037. P11's 2037 launch is also outside rule 1's 2028-2030 window.
- **fps 2037 (P11-P13)** is the open fan's no-wait launch year, and Boeing's H2 now sets it: with `cfm_open_fan` the H2 year is 2037, and an earlier launch only waits. A Turn-4 launch in 2035 instead waits two years and costs Boeing 3.68 more (13-B3).
- **P13** breaks RR's rule of no Turn-1 launch. A Turn-2 launch comes too late for NGSA 2028, which then falls back to the ducted engine (C14).

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
| P7 | ✗ −4.0 · ✓ 0.0 | ✗ −13.5 · ✗ −6.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✗ −0.3 · ✓ 2045 | 4 | +13.81 | −24.26 | +0.82 | +0.31 |
| P8 | ✗ −21.4 · ✗ −11.4 | ✓ +4.27 · ✓ 0.0 | ✓ 1,428 · ✓ 204.1 | ✓ 1,286 · ✓ 2026 | ✗ −47.4 · ✓ 2045 | 7 | −25.22 | +37.43 | +9.73 | +11.90 |
| P9 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 2,400 · ✓ 204.1 | ✓ 1,600 · ✓ 2026 | ✗ −76.0 · ✗ none | 7 | +6.55 | +29.11 | +17.80 | −1.49 |
| P10 | ✓ +1.0 · ✓ 0.0 | ✗ −26.0 · ✗ −26.0 | ✗ 0 · ✓ 204.1 | ✗ 612 · ✓ 2026 | ✓ +1.95 · ✗ none | 5 | +17.51 | −14.33 | +0.82 | +0.79 |
| P11 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✗ −3.0 · ✓ 2045 | 6 | +0.13 | +9.39 | +0.82 | +0.48 |
| P12 | ✗ −25.0 · ✗ −15.0 | ✓ +7.5 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✓ 2045 | 6 | −6.83 | +43.96 | +0.82 | −1.74 |
| P13 | ✗ −24.25 · ✗ −14.25 | ✓ +7.13 · ✓ 0.0 | ✓ 1,485 · ✓ 204.1 | ✓ 1,342 · ✓ 2026 | ✗ −50.25 · ✓ 2045 | 7 | −6.48 | +47.60 | +12.03 | +14.38 |

**Replacement wave**

| Plan | Boeing: 50% · defend | Airbus: 60% · A320 | RR: NB engines · WB engines | P&W: NB engines · upgrade | CFM: dominance · open fan | Met | ΔPV Boeing | Airbus | RR | P&W |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| P1 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 184.1 | ✓ 960 · ✗ none | ✓ 0.0 · ✗ none | 6 | +0.00 | +0.00 | +0.00 | +0.00 |
| P2 | ✗ −4.83 · ✓ +2.0 | ✗ −18.98 · ✗ −18.98 | ✗ 0 · ✓ 204.1 | ✗ 738 · ✓ 2026 | ✗ −0.67 · ✗ none | 3 | +14.73 | −10.29 | +0.82 | +1.06 |
| P3 | ✗ −27.58 · ✗ −17.58 | ✓ +3.77 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 5 | −2.49 | +42.08 | +0.82 | −1.74 |
| P4 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✗ none | 6 | +5.76 | +25.59 | +0.82 | −1.42 |
| P5 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 800 · ✓ 204.1 | ✗ 800 · ✓ 2026 | ✗ −16.0 · ✗ none | 6 | +7.33 | +25.59 | +5.18 | +5.64 |
| P6 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✓ 2,400 · ✓ 2026 | ✗ −36.0 · ✗ none | 6 | +5.76 | +27.35 | +0.82 | +0.43 |
| P7 | ✗ −6.83 · ✓ 0.0 | ✗ −9.48 · ✗ −3.17 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✗ −1.57 · ✓ 2045 | 4 | +10.96 | −20.51 | +0.82 | +0.39 |
| P8 | ✗ −18.39 · ✗ −8.39 | ✓ +2.4 · ✓ 0.0 | ✓ 1,368 · ✓ 204.1 | ✓ 1,248 · ✓ 2026 | ✗ −44.39 · ✓ 2045 | 7 | −23.81 | +34.05 | +9.29 | +11.30 |
| P9 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✓ 2,400 · ✓ 204.1 | ✓ 1,600 · ✓ 2026 | ✗ −76.0 · ✗ none | 7 | +6.55 | +29.11 | +17.80 | −1.49 |
| P10 | ✗ −3.63 · ✓ 0.0 | ✗ −20.18 · ✗ −20.18 | ✗ 0 · ✓ 204.1 | ✗ 717 · ✓ 2026 | ✗ −0.13 · ✗ none | 3 | +13.13 | −10.57 | +0.82 | +1.04 |
| P11 | ✗ −10.0 · ✓ 0.0 | ✓ 0.0 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✗ −3.0 · ✓ 2045 | 6 | +0.13 | +9.39 | +0.82 | +0.48 |
| P12 | ✗ −20.08 · ✗ −10.08 | ✓ +3.77 · ✓ 0.0 | ✗ 0 · ✓ 204.1 | ✗ 0 · ✓ 2026 | ✓ +24.0 · ✓ 2045 | 6 | −4.35 | +37.94 | +0.82 | −1.74 |
| P13 | ✗ −19.57 · ✗ −9.57 | ✓ +3.58 · ✓ 0.0 | ✓ 1,391 · ✓ 204.1 | ✓ 1,272 · ✓ 2026 | ✗ −45.57 · ✓ 2045 | 7 | −4.13 | +41.66 | +11.23 | +13.32 |

- **Seven of 10 is the most any plan meets, in both scenarios.** P8, P9 and P13 meet 7. A direct-model search of 1,553 joint plans per scenario agrees: 112 meet 7, 64 of them with the open fan, and none meets 8.
- **The 2045 date moves P7 and P8.** Both used to enter service in 2036-2037.
  - P7's open-fan NGSA now waits until 2045. fps leads by nine years, Airbus falls from +27.59 to −24.26, and P7 drops from 7 to 4.
  - P8's open-fan fps now waits until 2045. NGSA leads by eight years, Boeing falls from +3.57 to −25.22, and P8 drops from 8 to 7: it keeps CFM's `open_fan` and loses Boeing's `defend_incumbency`.
- **P12 is the only plan here that meets both CFM metrics.** A ducted NGSA in 2035 lifts CFM to 100%, and the open-fan fps flies in 2045. Boeing pays for it: −6.83, and Bdef misses by 15.0 pp.
- **Tie plans are the same in both scenarios.** P4, P5, P6, P9 and P11 give identical results because nobody captures share, so the wave weight has nothing to scale.
- **Supplier players leave the airframers' PVs unchanged while the airframers fly CFM engines.** P2 gives Boeing +17.58 and P3 gives Airbus +46.47, the same as the two-player values in the Boeing and Airbus briefs.

### 3.3 Why 7 is the ceiling

This follows from the metric definitions and the engine's dates (inference), and each step is checked by the runs cited.
1. **B50 and A60 cannot both hold**, so at most 9. RRwb and PWcred conflict with nothing.
2. **CFMof needs entry in exactly 2045.** The open fan cannot enter earlier, and the metric needs entry by 2045. No other new airframe enters after 2044 without a delay: the last launch year is 2037, and an UltraFan launched in 2037 is ready by 2044 (C10). So in a 2045 tie NGSA is on the open fan. Only Airbus's Delay Tactics can bring an fps on another engine to 2045 (C6, C9).
3. **A tie (Bdef with A60) meets at most 7.** With no Rate Increase it holds Bdef, A60 and Aprot, and RRwb and PWcred are free: 5.
   - **With CFMdom:** CFMdom needs both airframes on CFM engines, because one other engine leaves CFM at 60% or less. That rules out RRnb and PWbase. With CFMof as well, the tie is in 2045, the current fleets fly until 2044, and the GTF upgrade holds CFM at 73.0% in 2040 (P11). So CFMdom with CFMof costs PWcred (C12). A tie with CFMdom meets at most 6 (P4, C12).
   - **Without CFMdom:** RRnb, PWbase and CFMof cannot all hold. CFMof puts NGSA on the open fan (step 2), so fps carries the other engine with 40% of deliveries. The Joint Venture then gives P&W 800 engines (C6), and GTF2 gives RR none (C9). The ties that meet 7 take two of the three: P9 and C8 (RRnb and PWbase), C6 (RRnb and CFMof), C9 (PWbase and CFMof).
4. **Without a tie, at most 7.**
   - **If Airbus leads,** Bdef and B50 fail. RRnb, CFMdom and PWbase then cannot all hold. CFM would need its airframer at 76% or more once the UltraFan airframe is in service (C10). That leaves the UltraFan airframer 24% or less, and P&W's half of its engines is at most 480 a year, short of 960. P8, P13 and C13 meet 7 this way, with CFMof.
   - **If Boeing leads,** A60 fails, and either B50 fails or the lead it needs breaks Aprot (2.1). RRnb and CFMdom cannot both hold either. Boeing cannot reach 76% by 2040, and Airbus cannot exceed 60% while Boeing leads. C11 meets 7 this way, in base only: B50 and CFMof together, against an open-fan NGSA. It breaks Boeing's H1 and H2, RR's no-Turn-1 rule, and Airbus's rules 1 and 8.
5. **The old route to 8 is closed.** It was P8's structure: fps on the open fan, NGSA on the RR-P&W Joint Venture, the same entry year. That now needs NGSA on UltraFan in 2045, and NGSA on UltraFan enters by 2044 at the latest. Without the open fan the same structure is C8 (fps 2030 ducted, a 2037 tie): 7, with Boeing +4.98, Airbus +26.32, RR +8.27, P&W +9.91.

**Inside every hard rule as written**, P9 reaches 7 without the open fan. With the open fan, C13 (fps 2035 on the open fan, NGSA 2029 on the Joint Venture) and P8 reach 7, with Boeing at −9.34 and −25.22. P13 lifts Boeing to −6.48 by launching in 2037, the no-wait year. It needs RR to launch in Turn 1 so that NGSA 2028 can take UltraFan (C14).

### 3.4 The premium each player pays at P9 and P13

**Definitions.**
- **Premium:** the player's best reply, with the other players' orders held fixed, minus its PV in the plan.
- **"In its hard rules":** the replies kept after the filters the engine can test:
  - Boeing H1-H2: fps only in 2029, 2032 or 2035 (2037 with the open fan, per H2);
  - Airbus rules 1, 4 and 8, and the 2028-2030 window. Rule 8 now excludes every open-fan NGSA;
  - RR: standard terms, no Turn-1 launch;
  - P&W: standard terms.
- **Grids:**
  - Boeing, 388 replies: Rate Increase timing × fps year × engine × Solo or Joint Venture;
  - Airbus, 343: NGSA year × engine × Delay Tactics turns, with Poaching left out because it moves no metric;
  - RR, 98;
  - P&W, 200. The join sits in the turn of the plan's `uf_nb` launch (Turn 1 in P13).
- **Own-objective premium:** the best reply minus the best reply that meets as many of the player's own metrics as any reply can.

P9 is the best plan at the ceiling: it meets 7, sits inside every hard rule, and has the lowest total premium of the plans tested. P13 is the open-fan plan at 7 with the best Boeing PV of those run. Both suppliers' best replies keep their Turn-1 upgrades.

**At P9**

| Player | ΔPV in P9 (base / wave) | Best reply in its hard rules | ΔPV (base / wave) | Premium (base / wave) | Best reply, any | Premium (base / wave) | Own-objective premium | Cap |
|---|---:|---|---:|---:|---|---:|---:|---|
| Boeing | +6.55 / +6.55 | Rate Increase T3, fps 2029 UltraFan Solo | +8.31 / +8.31 | 1.76 / 1.76 | Rate Increase T3, fps 2028 ducted Solo | 2.74 / 1.83 | 0.00 | $2B (H8) |
| Airbus | +29.11 / +29.11 | Delay Tactics T4, NGSA 2028 ducted | +32.45 / +29.85 | 3.34 / 0.74 | Delay Tactics T3+4, NGSA 2028 ducted | 4.46 / 0.82 | 0.00 | $3B |
| Rolls-Royce | +17.80 / +17.80 | uf_nb 2029 Solo | +17.80 / +17.80 | 0.00 / 0.00 | uf_nb 2029 Solo | 0.00 / 0.00 | 0.00 | $3B a turn |
| Pratt & Whitney | −1.49 / −1.49 | no join, gtf_next 2030 | −1.19 / −1.19 | 0.31 / 0.31 | no join, gtf_next 2030 | 0.31 / 0.31 | 0.00 | $1B |

**Who pays for whose objective at P9**, in hard rules, one lever at a time (base / wave):

| Payer | Concession in P9 | Cost | Objective it protects | Run |
|---|---|---:|---|---|
| Boeing | GTF2 instead of UltraFan at the same entry year (2036) | 0.78 / 0.78 | P&W `gtf_base` | 9-B1 |
| Boeing | no Turn-3 Rate Increase | 0.98 / 0.98 | Airbus `nb_share_60`, `protect_a320` | best reply |
| Airbus | NGSA in 2029 on UltraFan instead of 2028 ducted (no lead) | 1.47 / 0.08 | Boeing `defend_incumbency` | 9-A2 |
| Airbus | no Turn-4 Delay Tactics | 1.87 / 0.66 | Boeing `defend_incumbency` | best reply |
| Rolls-Royce | none | 0 | | |
| Pratt & Whitney | `gtf_next` in 2029 instead of 2030 | 0.31 / 0.31 | none: launch timing only | 9-W1 |

- **Own objectives are free at P9 and P13.** Every player's best reply already meets as many of its own metrics as it can. P9's whole premium, 5.41 in base and 2.81 in the wave, buys other players' objectives.
- **At P9 only Airbus pays above its cap,** 3.34 against $3B in base, by 0.34. In the wave every premium sits inside its cap. I compared five plans and unilateral replies only (inference).
- **The engine choice costs Airbus nothing.** UltraFan is worth +3.52 to Airbus over the ducted engine at the same date in P9 (9-A1), and +3.64 / +3.72 in P13 (13-A2). Airbus's premium is all about timing: it gives up the lead.
- **Two readings lower the in-rules figures at P9:**
  - **Boeing.** H6 (no Rate Increase as a response to Airbus) may bar the Turn-3 Rate Increase. Without it Boeing's premium is 0.78.
  - **Airbus.** Its Turn-4 Delay Tactics leave NGSA first either way. They therefore fail the default team's test that Delay Tactics change who enters service first (Airbus brief §5.2). Without them (9-A2) Airbus's premium is 1.47 / 0.08.

**At P13**

| Player | ΔPV in P13 (base / wave) | Best reply in its hard rules | ΔPV (base / wave) | Premium (base / wave) | Best reply, any | Premium (base / wave) | Own-objective premium | Cap |
|---|---:|---|---:|---:|---|---:|---:|---|
| Boeing | −6.48 / −4.13 | Rate Increase T3, fps 2029 UltraFan Solo | +6.82 / +7.71 | 13.31 / 11.84 | Rate Increase T3, fps 2028 UltraFan Solo | 16.09 / 13.74 | 0.00 | $2B (H8) |
| Airbus | +47.60 / +41.66 | Delay Tactics T4, NGSA 2028 UltraFan | +48.19 / +42.26 | 0.60 / 0.60 | Delay Tactics T4, NGSA 2028 UltraFan | 0.60 / 0.60 | 0.00 | $3B |
| Rolls-Royce | +12.03 / +11.23 | no uf_nb | +0.82 / +0.82 | below the plan* | uf_nb 2028 Solo | 11.55 / 10.75 | 0.00 | $3B a turn |
| Pratt & Whitney | +14.38 / +13.32 | join T1, no gtf_next | +14.38 / +13.32 | 0.00 / 0.00 | join T1, no gtf_next | 0.00 / 0.00 | 0.00 | $1B |

\* P13 breaks RR's no-Turn-1 rule, so every in-rules RR reply is worse than the plan (−11.22 / −10.42). The RR figures below use its best reply of any kind.

**Who pays for whose objective at P13** (base / wave):

| Payer | Concession in P13 | Cost | Objective it protects | Run |
|---|---|---:|---|---|
| Boeing | the open fan, entering in 2045, instead of fps 2029 on UltraFan (2036) | 12.33 / 10.86 | CFM `open_fan` | 13-B2 |
| Boeing | no Turn-3 Rate Increase | 0.98 / 0.98 | Airbus `nb_share_60` | best reply |
| Airbus | no Turn-4 Delay Tactics, which would slip the fps to 2046 | 0.60 / 0.60 | CFM `open_fan` | 13-A1 |
| Rolls-Royce | the Joint Venture instead of Solo, both in Turn 1 | 11.55 / 10.75 | P&W `gtf_base` | 13-R1 |
| Pratt & Whitney | none | 0 | | |

- **Boeing pays for CFM's open fan.** The open fan costs Boeing 12.33 in base and 10.86 in the wave against an UltraFan fps in 2029, more than five times its $2B cap. No doctrine provides for paying toward another player's objective (inference).
- **RR also pays above its cap,** 11.55 against $3B a turn, for P&W's base. P13 will not come from doctrine play without a disclosed deal.
- **A 2037 launch is exposed to Delay Tactics.** It enters service in 2045 with no slack, so one Turn-4 Delay Tactics turn moves it to 2046 and breaks `open_fan` (13-A1). Airbus gains 0.60 and Boeing loses 1.87 / 2.02. A 2035 launch absorbs that turn and still enters in 2045 (13-B3a), but costs Boeing 3.68 more in waiting years (13-B3).

**Premiums in hard rules at the high-attainment plans** (base / wave):

| Plan | Met (of 10) | Boeing | Airbus | Rolls-Royce | Pratt & Whitney | Total |
|---|---:|---:|---:|---:|---:|---:|
| P4 | 6 | 0.90 / 0.90 | 6.86 / 4.26 | 0.00 / 0.00 | 0.00 / 0.00 | 7.76 / 5.17 |
| P9 | 7 | 1.76 / 1.76 | 3.34 / 0.74 | 0.00 / 0.00 | 0.31 / 0.31 | 5.41 / 2.81 |
| P11 | 6 | 14.58 / 11.73 | 35.18 / 29.16 | 0.00 / 0.00 | 0.00 / 0.00 | 49.76 / 40.89 |
| P13 | 7 | 13.31 / 11.84 | 0.60 / 0.60 | 11.55 / 10.75* | 0.00 / 0.00 | 25.46 / 23.19 |
| P8 | 7 | 34.86 / 32.69 | 6.53 / 3.88 | 9.19 / 8.75 | 0.00 / 0.00 | 50.58 / 45.32 |

\* against RR's best reply of any kind (see above).

- **P9 is the cheapest of these plans.** In the wave every premium sits inside its cap.
- **Adding CFM's open fan costs an objective, not just money.** No plan meets `open_fan` with P9's seven. The open-fan plans at 7 (P13, P8) trade Boeing's `defend_incumbency` for it. P13 costs 20.05 more than P9 in base and 20.38 more in the wave.
- **P11 keeps the tie but costs far more than P4, which also meets 6.** Each airframer would rather enter service around 2035 on a ducted engine: Boeing's premium is 14.58 and Airbus's 35.18 in base.

## 4. What the replacement wave changes

**Mechanism.** The wave scales only the leader's yearly capture. The weight is 0.4 through 2036, 0.428 in 2037, 0.648 in 2040, 1.0 in 2044, 0.981 in 2045 and 1.0 from 2046 (`rules`). The base scenario is unchanged.

| Effect | Base | Wave | Run |
|---|---|---|---|
| Ties (P4, P5, P6, P9, P11): attainment and PV | as in 3.2 | identical | P4-P6, P9, P11 |
| Boeing first: Boeing share in 2040 | 48.0% | 45.17% | P2 |
| Boeing first: Airbus `nb_share_60` gap | −23.0 pp | −18.98 pp | P2 |
| Airbus first: Boeing `defend_incumbency` gap | −20.0 pp | −17.58 pp | P3 |
| Airbus first: Airbus `nb_share_60` margin | +7.5 pp | +3.77 pp | P3 |
| fps on the open fan, NGSA first by ten years: Boeing `defend_incumbency` gap; Boeing PV | −14.25 pp; −6.48 | −9.57 pp; −4.13 | P13 |
| NGSA on the open fan, fps first by nine years: Airbus `nb_share_60` gap; Airbus PV | −13.5 pp; −24.26 | −9.48 pp; −20.51 | P7 |
| Boeing chases 50% (fps 2027 + Rate Increase T2) | met, +1.0 pp | missed, −3.63 pp | P10 |
| Boeing leads against an open-fan NGSA: objectives met | 7 | 6 (`nb_share_50` missed) | C11 |
| fps 2026 against Airbus Do Nothing, two-player: Boeing in 2040, `nb_share_50` | 50.5%, met | 44.97%, missed | G1 |
| fps 2032 against NGSA 2029, two-player: Boeing PV | +0.26 | +1.99 | G4 |
| CFM dominance, fps first with the GTF upgrade | +0.6, +1.95 pp | −0.67, −0.13 pp | P2, P10 |
| Value of entering one year first in the 2036 tie: Boeing / Airbus | 2.37 / 5.00 | 1.47 / 3.61 | 4-B1, 4-A1 |

**Timing.** The wave does not move the best launch years. In both scenarios the best in-rules replies at P4, P8, P9, P11 and P13 are fps 2029 and NGSA 2028; the best replies of any kind are fps 2028 and NGSA 2028. None is on the open fan. The fps 2029 / NGSA 2029 grid cell is +5.76 / +25.59 in both (G3), and Boeing's fps 2026 drops from +13.50 to +8.54 (G1).

**Harder in the wave:**
- **`nb_share_50`.** Even an fps launched in 2026 (G1), or in 2027 with a Rate Increase (P10 and, against an open-fan NGSA, C11), misses.
- **`nb_dominance`** when Boeing leads on CFM engines while the GTF upgrade is in place (P2, P10 flip to missed).
- **The value of leading**, for both airframers.

**Easier in the wave:**
- **The follower's metric.** `defend_incumbency` after an NGSA lead and `nb_share_60` after an fps lead miss by less (P2, P3), but still miss. The same holds for the airframer that picks the open fan (P13, P7).
- **Picking the open fan.** The lead it hands the rival is worth less. Boeing's PV at P13 rises from −6.48 to −4.13, and its premium falls from 13.31 to 11.84.
- **Holding a tie.** A tie is cheaper to hold because the lead it forgoes is worth less. Total in-rules premium at P9 falls from 5.41 to 2.81, and at P11 from 49.76 to 40.89. RR's Joint Venture premium barely moves (P13: 11.55 to 10.75).

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
   - The joint ceiling is 7 (3.3), and the status quo already gives 6.
   - B50 needs a Turn-1 fps and an Airbus that waits.
   - For Boeing, 1 of 2 is a full score unless Airbus waited (inference).
   - RR's `nb_entry` and P&W's `gtf_base` need an airframer's selection.
   - CFM's result reflects other players' choices, not CFM skill.
   - CFM's `open_fan` needs an airframer entering service in exactly 2045. Within the hard rules only Boeing can deliver it (Airbus rule 8), and only by giving up `defend_incumbency`. Treat a missed `open_fan` as the expected result (inference).
4. **Do not add attainment across players into one score** (inference). The metrics conflict by design.

**What the 2045 date does to the share objectives.** B50 against A60 stays zero-sum. The open fan adds a third leg: the airframer that picks it concedes the lead for 8 to 10 years, so CFM's `open_fan` is paid for in that airframer's own share metric (2.1). Only a 2045 tie avoids it. Against the 2036 ducted tie that cuts Boeing from +5.76 to +0.13 and Airbus from +25.59 to +9.39 (P4, P11). When an airframer picks the open fan, read the rival's share gain as a consequence of that choice, not as the rival's skill.

### 5.2 Premium paid against the doctrine cap

1. **Recompute each declared objective premium** with `whatif` at the decision turn: the best allowed reply minus the chosen orders, with the other players' actual orders held fixed.
2. **Split it into three parts:**
   - own-objective premium, allowed within the cap;
   - doctrine premium;
   - money spent on another player's objective.
   At P9 and P13 the first part is 0 for everyone.
3. **Compare the sum of the first two with the cap:**
   - Boeing $2B (H8, shared with any doctrine premium);
   - Airbus $3B (shared);
   - Rolls-Royce $3B a turn;
   - Pratt & Whitney $1B (shared);
   - CFM none: it has no PV, and its brief proposes $1.0B for a future CFM player (inference).
4. **Flag these cases:**
   - a premium above the cap;
   - money spent on another player's objective without a disclosed deal;
   - an "objective premium" claimed where the best reply already met the objective. That is a mislabelled doctrine premium;
   - a Boeing open-fan fps booked as Boeing's own objective premium. It buys CFM's metric, not Boeing's (12.33 at P13).

### 5.3 Did the player pursue its objective sensibly?

| Player | Sensible | Not sensible |
|---|---|---|
| Boeing | Plays for Bdef: fps enters service no later than NGSA. Tracks B50 without chasing it, since 50/50 "is not an objective of ours" [B-1936]. Ducted engine by default; Boeing chose engines on maturation depth [B-0613] and worries about new-engine durability [B-2304] | A Turn-1 fps to reach 50%: current programmes come first [B-2276], Boeing sets no dates [B-2313] and said "not before '35" [B-2061]. An open-fan fps without a disclosed deal: it gives up Bdef and costs Boeing 12.33 at P13 (13-B2), far above $2B. At P8 Boeing's premium is 34.86 |
| Airbus | NGSA in 2028-2030, matching the expected engine choice around 2027 [A-0182] and entry "around 2037" [A-0409]. At most one Delay Tactics turn: integrity is one of the five pillars in its first 2026 objective [A-0331]. Engine choice by PV: UltraFan costs Airbus nothing at the same date (9-A1, 13-A2) | A second Delay Tactics turn for A60 (red line 4). NGSA entering service before 2035 (rule 1). NGSA on the open fan: it waits until 2045, breaks rule 8 and hands Boeing the lead (P7: −24.26, A60 −13.5 pp) |
| Rolls-Royce | `uf_nb` only against an announced airframe [R-0994, R-1005]. Solo where an airframer has picked UltraFan. The Trent 1000 upgrade in Turn 1 | A speculative launch to reach `nb_entry`; RR says narrowbody is optional, "we don't need to do it" [R-1011], and puts profit before share [R-1582]. A Joint Venture 9.19 (P8) or 11.55 (P13) below Solo booked as RR's own objective premium |
| Pratt & Whitney | The GTF upgrade in Turn 1 or 2, its standard fix [P-0786]; "time on wing ... is the name of the game" [P-1355]. Joining a Joint Venture on NGSA when offered. GTF2 only for a disclosed airframe | `gtf_next` with no committed airframe beyond the $1B cap [P-0746, P-0711]. Discounts past launch mode [P-0735] |
| CFM (not a player) | When the market cell or referee voices CFM, check it against "we're not going for share" [CX-0493], the airframer setting the date [CX-0205], and no trade of durability for fuel burn [CX-0208] | A CFM reaction that cuts price for share, forces an open-fan date, or promises the open fan before 2045 |

A Turn-4 Delay Tactics turn against a 2037 open-fan fps is within Airbus rule 4 and earns +0.60 at P13, but it breaks CFM's `open_fan` (13-A1). Score it as legal play and record the effect on CFM.

### 5.4 Modelling limits to state in the after-action review

- **Unmodelled moves.**
  - **Boeing.** No lever separates the 7-year from the 10-year ramp-up; capture after entry is fixed at 1.5 pp a year times the multipliers. The Embraer route is modelled as the fps Joint Venture.
  - **CFM.** Its choice to offer the open fan, the ducted engine or both is only partly modelled, because CFM cannot withhold an engine. No CFM lever moves the open fan's 2045 date. A CFM partnership with Embraer and emissions lobbying have no lever.
  - **P&W.** Its Joint Venture is RR's UltraFan, not a GTF-based engine.
  - **Enablers with no lever:** government incentives, workforce, the A220-500, MRO scale, and cash or debt limits.
- **The 2045 date is a game parameter** (`engine_options.nb.cfm_open_fan.available_eis`). CFM's partners aimed earlier: Safran's CEO said "by 2035" [CX-0152], and Culp said "by the middle of the next decade" [CX-0189]. A referee testing an earlier open fan can set another date with `--override` when creating a run.
- **NGSA at $20B against the engine's $25B.** At $20B Airbus's PV rises by 4.48 (P3, P13), 4.15 (P4, P9) and 3.84 (P8). No metric and no other player's PV changes.
- **MAX share and margin erosion under Do Nothing is not modelled.** P1 holds Boeing at 40% in every year of both scenarios. Slide 7 expects erosion. Do Nothing is therefore flattered, and `defend_incumbency` under Do Nothing reads met when it may not be (inference).
- **CFM is not a player.** It has no PV, levers or premium. Its attainment is a by-product of others' choices. The GTF upgrade alone breaks `nb_dominance` (C1).
- **Scoring limits.**
  - Metrics are read at five-year marks only. `open_fan` reads entry by 2045, so with the 2045 date it is met only by entry in 2045.
  - The engine counts are binary: 800 engines scores like 2,400.
  - `credibility` measures spending, not durability.
  - New programmes are sole source: a rival engine takes a whole airframe's deliveries.
  - Engine-option values and strain are placeholders.
- **Limits of this analysis.**
  - Replies are unilateral and the grids are finite. No four-player equilibrium was computed.
  - The direct-model search covers launch years 2026, 2028, 2029, 2031, 2032, 2034, 2035 and 2037, all four engines, and Solo or Joint Venture UltraFan, with no Rate Increase or Delay Tactics. The argument in 3.3 covers the rest (inference).
  - No injects or market multipliers.
  - Engine selection has no maturity or reputation test once a supplier has launched. Real airframers weigh maturity: Boeing chose LEAP on its maturation depth [B-0613].

<details>
<summary>Commands</summary>

```bash
cd /home/user/aero-engine-gameboard
export WARGAME_RUNS_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/of_update/overview
mkdir -p $WARGAME_RUNS_DIR
python3 -m wargame.engine new --run-id oc-base --scenario base --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id oc-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney
python3 -m wargame.engine new --run-id oc2-base --scenario base                 # two-player, wave_grid.txt cells
python3 -m wargame.engine new --run-id oc2-wave --scenario replacement-wave
python3 -m wargame.engine new --run-id oc20-base --scenario base --suppliers rolls_royce,pratt_whitney --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
python3 -m wargame.engine new --run-id oc20-wave --scenario replacement-wave --suppliers rolls_royce,pratt_whitney --override '{"programs":{"ngsa":{"capex_b":20.0}}}'
for s in boeing airbus rolls_royce pratt_whitney; do python3 -m wargame.engine rules --run oc-base --side $s; done   # assigned_objectives (Section 1)
python3 -m wargame.engine rules --run oc-base --side control    # engine options (open fan available_eis 2045), share rule, leader cap 0.8, CFM metrics
python3 -m wargame.engine rules --run oc-wave --side control    # capture_weight_by_year (Section 4)

# Every plan and check is one whatif with the plan on stdin. Turn keys: 1 = 2026-28, 2 = 2029-31, 3 = 2032-34, 4 = 2035-37. P13:
echo '{"boeing": {"4": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_open_fan", "year": 2037}]}},
 "airbus": {"1": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb", "year": 2028}]}},
 "rolls_royce": {"1": {"t1000_upgrade": true, "launch": [{"program": "uf_nb", "variant": "jv_pw", "terms": "standard", "year": 2028}]}},
 "pratt_whitney": {"1": {"gtf_upgrade": true, "join_rr_jv": true}}}' | python3 -m wargame.engine whatif --run oc-base --side control   # and --run oc-wave

# Scripts in /tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad/of_update/oc/
# (run from that folder with the same WARGAME_RUNS_DIR; each calls the whatif above through subprocess, except of_search.py):
python3 plans.py --json plans_out.json   # P1-P13 orders (PLANS) on oc-base and oc-wave: Sections 1, 2, 3.2, 4
python3 br.py P9 P13 P8 P4 P11           # best replies: Boeing 388, Airbus 343, RR 98, P&W 200 per plan and run (3.4, 4)
python3 make_tables.py > tables.md       # re-runs P1-P13 and the best-reply grids; prints the tables of 3.2 and 3.4
python3 decomp.py                        # one-lever swaps at P9 (9-B1, 9-B2, 9-A1, 9-A2, 9-W1), P13 (13-B1, 13-B2, 13-B3, 13-B3a,
                                         # 13-A1, 13-A2, 13-R1, 13-W1) and P4 (4-B1, 4-A1: fps or NGSA 2028 ducted, entering first)
python3 checks.py                        # C1 upgrades only; C2 GTF upgrade T2; C3, C4 Rate Increase T1, T2 in P4; C5 787 Re-engine on GE;
                                         # C6 2045 tie: fps 2037 on UltraFan Joint Venture + Airbus Delay Tactics T4, NGSA 2037 open fan;
                                         # C7 P8 with RR Solo; C8 P8 with fps 2030 ducted (2037 tie); C9 as C6 with fps on GTF2;
                                         # C11 fps 2027 on UltraFan Joint Venture (uf_nb 2026) + Rate Increase T2, NGSA 2037 open fan;
                                         # C12 P11 without the GTF upgrade; C13 fps 2035 open fan, NGSA 2029 on UltraFan Joint Venture 2029;
                                         # C14 P13 with RR's Joint Venture in Turn 2; G1-G5 two-player cells (fps 2026 / none;
                                         # none / NGSA 2026; 2029 / 2029; 2032 / 2029; 2029 / none; Solo, ducted)
python3 checks2.py                       # C10 NGSA 2026 ducted, fps 2037 on UltraFan Solo (RR uf_nb 2037); NGSA at $20B for P3, P4, P8, P9, P13
python3 of_search.py                     # direct-model search, 1,553 joint plans per scenario: maximum met, plans with open_fan (3.2)
python3 verify_prose.py                  # checks every engine number in the prose against the outputs above
# Citations
python3 wargame/profiles/build/cite_check.py wargame/profiles/overview/objectives_analysis.md wargame/profiles/boeing/evidence.jsonl \
  wargame/profiles/boeing/executives/evidence.jsonl wargame/profiles/airbus/evidence.jsonl wargame/profiles/airbus/executives/evidence.jsonl \
  wargame/profiles/rolls_royce/evidence.jsonl wargame/profiles/pratt_whitney/evidence.jsonl wargame/profiles/cfm/executives/evidence.jsonl
```

</details>
