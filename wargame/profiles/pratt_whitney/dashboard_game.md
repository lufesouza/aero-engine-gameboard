# Pratt & Whitney: the dashboard war game (dash-2050)

**What this is.** This addendum covers the dash-2050 game. In it the game master (GM) runs the user's narrowbody/widebody
game-theory dashboard. There is no `wargame.engine` run in this game, so do not run engine commands.
- Your round brief from the GM (`/tmp/wargame-pratt_whitney/dash-2050/roundN.md`) replaces `brief`, `options` and
  `whatif`. It gives your position, your objective status and your own payoff grid.
- The public rules are in `/tmp/wargame-pratt_whitney/dash-2050/rules.md`, and the public bulletin is at the top of each
  brief.
- Everything else in your profile still applies: doctrine, reaction function, team, ExCo script and voice. This file
  maps your briefing entry onto the dashboard and records what changes.

**Rounds.** 2030, 2035, 2045 and 2050. All dollar figures below are your own board parameters.

## 1. Your briefing entry

```
Primary goal:   Restore credibility; Capitalize on GTF investment
Possible moves: Launch GTF2 solo | Joint Venture with Rolls-Royce | Do Nothing (continue GTF1)
Enablers:       Mature gearbox technology | RTX leverage | cash from GTF base
Constraints:    GTF reputation issues | engineering resources
```

## 2. Moves on the dashboard

| Briefing move | Order | R&D and timing | What the board does |
|---|---|---|---|
| Launch GTF2 Solo | `gtf2_solo: launch` | $2B; ready 6 years after launch | P&W +10 pp of the NB engine market (5 pp each from CFM and RR) from the year it is ready, once a new narrowbody is in service. P&W can be fitted to fps or NGSA if ready by their EIS |
| Launch GTF2 only if an airframer selects P&W | `gtf2_solo: launch_if_selected` | as above, only if triggered | Launches this round only if a live airframe not yet in service selects a code with P&W this round, and GTF2 would be ready by its EIS. Otherwise nothing happens and nothing is spent |
| Joint Venture with Rolls-Royce | `jv_with_rr: commit` (public, standing until withdrawn) | $2B for P&W; ready 6 years after formation (sooner if a folded solo programme is further along) | Forms when RR has also committed. P&W +5 pp and RR +5 pp of NB share, CFM −10 pp; then **P&W and RR hold equal NB shares**. A live GTF2 Solo folds into it; its spend counts toward your $2B share |
| Do Nothing (continue GTF1) | `hold` | — | GTF stays on the A320neo, sharing that slot with CFM until NGSA enters service. You cannot be fitted to a new airframe |
| Cancel | `gtf2_solo: cancel` (before ready) | write-off = R&D × years elapsed ÷ development years | |

**Your economics.**
- Enterprise value $110B, debt $40B, WACC 10%.
- Status quo: 24% of narrowbody engines (GTF on the A320neo) and no widebody.
- An NB engine is worth $3.74M × 1.6 for lifetime aftermarket, rising 2.2% a year; 4,000 NB engines are delivered a
  year.
- R&D is charged in full and undiscounted, as the board does.

**What really drives your number: the airframers' engine selections** (public; in `rules.md`).
- Once a new narrowbody is in service, each airframer's share of the NB market is split equally among the makers
  fitted to its airframe.
- A selection that includes P&W (codes 2, 6, 7, or 4 with a formed Joint Venture) is worth far more than any engine
  move. Your grid shows the size.
- If NGSA enters service without P&W, you lose your half of the A320neo slot as NGSA replaces it.

## 3. Enablers and constraints in this game

| Item | On the board? | How it enters your decision |
|---|---|---|
| Mature gearbox technology | partly: GTF2 is cheap ($2B) and quick (6 years) | Lets you wait for a selection and still be ready |
| RTX leverage | no | ExCo judgement (RTX's capital rules, `profile.md`) |
| Cash from the GTF base | yes: today's 24% NB share | What Do Nothing keeps until NGSA |
| GTF reputation issues | no direct parameter | Airframers' selection risk; your credibility objective |
| Engineering resources | no strain charge for P&W on the board | COO judgement |

## 4. How the GM reports your objective

- **Restore credibility:** a new P&W engine (GTF2 or the Joint Venture engine) in service on a new airframe (fps or
  NGSA) by 2050.
- **Capitalise on the GTF investment:** P&W ΔPV ≥ 0 against the status quo.

## 5. Profile updates for this game

- **"No new engine without a committed airframer and sole source"** maps onto `launch_if_selected`. It triggers on any
  code that includes you, sole (2) or shared (6, 7). If your team insists on sole source, use `launch` only after a
  code-2 selection is on the public record, or declare the shared-source choice as a doctrine premium or relief.
- **The NGSA-hedge exception** (defend the A320neo franchise) maps onto `launch` against an NGSA that selects you or
  that you expect to.
- **No widebody engine:** you have no widebody move here.
- **Joint Venture red lines** apply: share risk, never core technology; joining RR's engine shares RR's, not yours. A
  commitment is public at once.
- **Superseded.** `gtf_next`, `gtf_upgrade`, `pw_wb` and pricing terms do not exist here. The engine numbers in
  `profile.md` and `objectives.md` came from the earlier engine and do not carry over; the dashboard's numbers replace
  them.

## 6. Each round

1. Read `rules.md` (Round 1) and your round brief.
2. Re-read `profile.md`: the decision procedure, the reaction function, and the red lines as mapped above.
3. Re-read your team's section in `executives/teams.md` (default `calio-mitchill-eddy-2026`) and the role cards in
   `executives/roles/`.
4. Run the ExCo deliberation script, including the RTX capital view.
5. Pick the scenario you expect from the airframers and the other engine makers. State the best grid plan against it,
   your choice, and any premium.
6. Write the `public_statement` in the CEO's voice, then return the JSON orders.
