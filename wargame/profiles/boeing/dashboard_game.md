# Boeing: the dashboard war game (dash-2050)

**What this is.** This addendum covers the dash-2050 game. In it the game master (GM) runs the user's narrowbody/widebody
game-theory dashboard. There is no `wargame.engine` run in this game, so do not run engine commands.
- Your round brief from the GM (`/tmp/wargame-boeing/dash-2050/roundN.md`) replaces `brief`, `options` and `whatif`. It
  gives your position, your objective status and your own payoff grid.
- The public rules are in `/tmp/wargame-boeing/dash-2050/rules.md`, and the public bulletin is at the top of each brief.
- Everything else in your profile still applies: doctrine, reaction function, team, ExCo script and voice. This file
  maps your briefing entry onto the dashboard and records what changes.

**Rounds.** 2030, 2035, 2045 and 2050. All dollar figures below are your own board parameters.

## 1. Your briefing entry (Boeing PD slide, "Who plays, what they want, and what they can do")

```
Primary goal:   Hold the 50/50 NB split; Defend incumbency
Possible moves: fps with 7-year ramp-up | fps with 10-year ramp-up | fps via Embraer | Increase 737 rate by 2030 | Do Nothing (Milk 737 MAX)
Enablers:       737 customer base | trained workforce | government incentives | cash from 787 program
Constraints:    High debt load | ramp-up speed | engineering capacity | supply-chain bottlenecks
```

## 2. Moves on the dashboard

| Briefing move | Order | Cost and timing | What the board does |
|---|---|---|---|
| fps, 7-year ramp-up | `fps: launch_7yr` | $64.47B, booked at EIS; EIS = launch + 7 | fps at $55M and 25.64% margin, against the 737 MAX at $48M and 8%. Capture after EIS 1.0 pp a year. Plus a first-mover bonus of +5 pp for 10 years from EIS |
| fps, 10-year ramp-up | `fps: launch_10yr` | $55.25B at EIS; EIS = launch + 10 | Same airplane and capture speed, no bonus, 3 years later |
| fps via Embraer | `fps: launch_via_embraer` | $100B at EIS (Boeing's bill on the board); EIS = launch + 10 | As the 10-year ramp-up; only the cost differs |
| Increase 737 rate by 2030 | `rate_737: increase`; 2030 round only | $2.94B in 2032 | +5 pp NB share in 2032-36, or in every year if neither new narrowbody is ever launched |
| 787 Re-engine (widebody; not on the slide) | `re787: launch` | $5B at EIS; EIS = launch + 5 | Alone: 787 gains 1.0 pp a year to 85% and its margin rises from 20% to 25.21%. If the A350 also re-engines, the margin is 15.77% and share gains stop at the A350's EIS |
| Do Nothing | `hold` | — | 737 MAX and 787 as today |
| Engine choice | `fps_engine_code` 1-7 | — | Does not change Boeing's payoff on the board. A maker with no new engine ready by fps EIS is dropped; if none is left, fps flies CFM |
| Cancel | `fps: cancel`, `re787: cancel` (before EIS) | write-off = bill × years elapsed ÷ development years | The programme is gone; the write-off and its debt penalty stay |

**Costs every plan carries.**
- **Debt penalty (α 0.30).** Enterprise value $130B, debt $45B, WACC 10.5%. New spend adds to debt, and the penalty
  is debt × α × (debt ÷ EV)², so it grows fast. Before discounting, a 10-year fps adds $16.3B of penalty, a 7-year fps
  $21.7B and fps via Embraer $52.5B, against $0.6B for the 787 Re-engine alone. The penalty is discounted like the
  spend itself.
- **Two-front strain.** $3B × the overlap between fps development (EIS − 7 to EIS) and 787 Re-engine development
  (EIS − 5 to EIS), divided by 5. It costs nothing if the two do not overlap.

**Market rules that drive your number** (public; in `rules.md`).
- If NGSA enters service first, Airbus gains 3 pp a year (cap 80%) until fps arrives. Boeing then climbs toward 50% at
  1.0 pp a year.
- If fps enters service first, Boeing gains 1.0 pp a year (cap 80%). When NGSA arrives, shares freeze unless Boeing
  is above 50%.
- Airbus's covert Delay Tactics, if any, cost Boeing 5 pp for 5 years from fps EIS.

## 3. Enablers and constraints in this game

| Item | On the board? | How it enters your decision |
|---|---|---|
| 737 customer base | yes: 40% status quo at 8% margin | The share you defend; Do Nothing keeps it only until NGSA arrives |
| Trained workforce | no | ExCo judgement (COO); Airbus talent poaching is a Delay Tactic you cannot see |
| Government incentives | no | ExCo judgement; the board books the full bill |
| Cash from 787 program | yes: 787 at 20% margin, 58.8% of the widebody | Funds the fps; the 787 Re-engine changes it |
| High debt load | yes: α debt penalty, WACC 10.5% | CFO test in every round |
| Ramp-up speed | yes: 1.0 pp a year capture; 7-year ramp +5 pp | 7-year vs 10-year choice |
| Engineering capacity | yes: two-front strain | COO test; H4 |
| Supply-chain bottlenecks | partly: Delay Tactics (covert) and engine fallback | Use the risk-case column of your grid |

## 4. How the GM reports your objective

- **Hold the 50/50 NB split:** Boeing NB share ≥ 50% in 2040, 2045 and 2050 (the worst year decides).
- **Defend incumbency:** Boeing NB share ≥ 40% (the status quo) in every listed year, 2030-2050.

The objective never changes your payoff. Any PV you give up to advance it is an **objective premium** and counts
against the H8 cap.

## 5. Profile updates for this game

- **H1 (no fps in Round 1) and H3 (no 787 Re-engine in Round 1)** were written for a round sealed at the start of
  2026: the 777X and MAX 7/10 unfinished, debt not yet repaired. Here Round 1 is **2030**. Your ExCo decides whether
  their conditions still hold in 2030 and says why in the rationale, citing evidence. If you lift them, say so.
- **H2** (no EIS before the 2035 technology-ready year) cannot bind: the earliest fps EIS is 2037.
- **H3's second half** still holds: no 787 Re-engine once Airbus has launched the A350 Re-engine.
- **H4.** "At most 2 years of overlap" now refers to the board's strain overlap above. A Solo fps launched with the 787
  Re-engine in the same round overlaps by 5 years (full strain, $3B before discounting).
- **H5** (never cancel a launched fps or 787 Re-engine) and **H6** (no Rate Increase as a response to Airbus) apply as
  written. H7 has no trigger here: there are no crisis injects.
- **H8** (ties within $1B; at most $2B of doctrine plus objective premium) applies to the grid numbers in your brief.
- **Superseded.** The engine numbers in `profile.md` and `objectives.md` came from the earlier engine and do not carry
  over. The dashboard's numbers in your brief replace them.
- **What the board does not price.** Engine durability, customer lock-in from early orders, COMAC and Embraer as
  entrants, and pricing campaigns. Use your doctrine for these; put any such move in `other_moves`.

## 6. Each round

1. Read `rules.md` (Round 1) and your round brief.
2. Re-read `profile.md`: the decision procedure, the reaction function, and the hard rules as mapped above.
3. Re-read your team's section in `executives/teams.md` (default `ortberg-malave-pope-2026`) and the role cards in
   `executives/roles/`.
4. Run the ExCo deliberation:
   - the CEO frames;
   - the CFO tests cash, debt and the hurdle on the grid numbers;
   - the head of Commercial Airplanes tests production, engineering and supply-chain readiness;
   - decide by the team's decision rule.
5. Pick the scenario you expect from Airbus. State the best grid plan against it, your choice, and any doctrine or
   objective premium.
6. Write the `public_statement` in the CEO's voice, then return the JSON orders.
