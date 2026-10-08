# Rolls-Royce: the dashboard war game (dash-2050)

**What this is.** This addendum covers the dash-2050 game. In it the game master (GM) runs the user's narrowbody/widebody
game-theory dashboard. There is no `wargame.engine` run in this game, so do not run engine commands.
- Your round brief from the GM (`/tmp/wargame-rolls_royce/dash-2050/roundN.md`) replaces `brief`, `options` and
  `whatif`. It gives your position, your objective status and your own payoff grid.
- The public rules are in `/tmp/wargame-rolls_royce/dash-2050/rules.md`, and the public bulletin is at the top of each
  brief.
- Everything else in your profile still applies: doctrine, reaction function, team, ExCo script and voice. This file
  maps your briefing entry onto the dashboard and records what changes.

**Rounds.** 2030, 2035, 2045 and 2050. All dollar figures below are your own board parameters.

## 1. Your briefing entry

```
Primary goal:   Enter narrowbody market; Keep Widebody dominance
Possible moves: Ultrafan widebody only (no NB entry) | Ultrafan narrowbody solo | Joint Venture with Pratt & Whitney | Do Nothing (continue Trent only)
Enablers:       Free cash from widebody | reputation | airframer support for a 3rd engine maker
Constraints:    Engineering resources shared with widebody | no NB MR&O scale | gearbox sizing
```

## 2. Moves on the dashboard

| Briefing move | Order | R&D and timing | What the board does |
|---|---|---|---|
| UltraFan narrowbody Solo | `ultrafan_nb_solo: launch` | $8B; ready 7 years after launch | RR +15 pp of the NB engine market (CFM −10, P&W −5) from the year it is ready, once a new narrowbody is in service. RR can be fitted to fps or NGSA if ready by their EIS |
| UltraFan NB only if an airframer selects RR | `ultrafan_nb_solo: launch_if_selected` | as above, only if triggered | Launches this round only if a live airframe not yet in service selects a code with RR this round, and UltraFan would be ready by its EIS. Otherwise nothing happens and nothing is spent |
| Joint Venture with P&W | `jv_with_pw: commit` (public, standing until withdrawn) | $4B for RR (half the NB R&D); ready 6 years after formation (sooner if a folded solo programme is further along) | Forms when P&W has also committed. RR +5 pp and P&W +5 pp of NB share, CFM −10 pp; then **RR and P&W hold equal NB shares**. A live UltraFan NB Solo folds into it; spend beyond your $4B share is written off |
| UltraFan widebody only | `ultrafan_wb: launch` | $4B; ready 6 years after launch | RR +10 pp of the widebody engine market, from CFM. It counts only once a re-engined 787 or A350 is in service. With no Re-engine, the R&D is spent for nothing |
| Trent 1000 upgrade (not on the slide; exclusive with UltraFan WB) | `t1000_upgrade: launch` | $2B; counts 3 years after launch, not before 2035 | RR +5 pp of the widebody engine market |
| Do Nothing (Trent only) | `hold` | — | Trent keeps 58% of widebody engines; no narrowbody |
| Cancel | `cancel` (before ready) | write-off = R&D × years elapsed ÷ development years | |

**Strain.** $5B if you run a narrowbody project (UltraFan NB or the Joint Venture) and a widebody project (UltraFan WB
or the Trent 1000 upgrade) at the same time.

**Your economics.**
- Enterprise value $110B, debt $40B, WACC 10%.
- Status quo: 58% of widebody engines and 0% of narrowbody.
- A WB engine is worth $11.2M and an NB engine $3.74M, × 1.6 for lifetime aftermarket, rising 2.2% a year.
- 340 WB and 4,000 NB engines are delivered a year.
- R&D is charged in full and undiscounted, as the board does.

**What really drives your number: the airframers' engine selections** (public; in `rules.md`). Once a new narrowbody is
in service, each airframer's share of the NB market is split equally among the makers fitted to its airframe. A
selection that includes RR (codes 1, 5, 7, or 4 with a formed Joint Venture) is the narrowbody entry. Your grid shows
the size.

## 3. Enablers and constraints in this game

| Item | On the board? | How it enters your decision |
|---|---|---|
| Free cash from widebody | yes: 58% of WB engines | What Do Nothing keeps |
| Reputation | no | ExCo judgement; airframer selections |
| Airframer support for a 3rd engine maker | yes: the engine codes airframers choose | Your grid's scenario columns |
| Engineering shared with widebody | yes: $5B NB + WB strain | Red line on overlaps |
| No NB MR&O scale | no | ExCo judgement |
| Gearbox sizing | no | Possible reason for the Joint Venture (P&W's gearbox) |

## 4. How the GM reports your objective

- **Enter the narrowbody market:** RR NB engine share > 0 in 2045 and 2050.
- **Keep widebody dominance:** RR WB engine share ≥ 50% in 2040, 2045 and 2050.

## 5. Profile updates for this game

- **"No UltraFan launch without an announcement of a programme that can fly it"** maps onto `launch_if_selected`. You
  may also `launch` against a selection already on the public record.
- **"`jv_pw` only if P&W announced its join"** maps onto commitments: P&W's commitment is public and standing. Commit
  when P&W has committed, or commit first if your doctrine allows. A commitment is public at once.
- **"No overlapping UltraFan WB and UltraFan NB Solo developments unless both are selected"** and **"no Trent 1000
  upgrade while an UltraFan is in development"** apply. On this board the NB + WB overlap costs $5B of strain.
- **Superseded.** Pricing terms do not exist here. The engine numbers in `profile.md` and `objectives.md` came from the
  earlier engine and do not carry over; the dashboard's numbers replace them. The $3B doctrine-premium cap per round
  still applies.

## 6. Each round

1. Read `rules.md` (Round 1) and your round brief.
2. Re-read `profile.md`: the decision procedure, the reaction function, and the red lines as mapped above.
3. Re-read your team's section in `executives/teams.md` (default `erginbilgic-mccabe-watson-2026`) and the role cards
   in `executives/roles/`.
4. Run the ExCo deliberation script.
5. Pick the scenario you expect from the airframers and P&W. State the best grid plan against it, your choice, and any
   premium.
6. Write the `public_statement` in the CEO's voice, then return the JSON orders.
