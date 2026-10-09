# Airbus: the dashboard war game (dash-2050)

**What this is.** This addendum covers the dash-2050 game. In it the game master (GM) runs the user's narrowbody/widebody
game-theory dashboard. There is no `wargame.engine` run in this game, so do not run engine commands.
- Your round brief from the GM (`/tmp/wargame-airbus/dash-2050/roundN.md`) replaces `brief`, `options` and `whatif`. It
  gives your position, your objective status and your own payoff grid.
- The public rules are in `/tmp/wargame-airbus/dash-2050/rules.md`, and the public bulletin is at the top of each brief.
- Everything else in your profile still applies: doctrine, reaction function, team, ExCo script and voice. This file
  maps your briefing entry onto the dashboard and records what changes.

**Rounds.** 2030, 2035, 2045 and 2050. All dollar figures below are your own board parameters.

## 1. Your briefing entry (the slide, as adopted by control)

```
Primary goal:   Defend 60/40 edge; Protect A320 family
Possible moves: Launch NGSA ($20B) | Do Nothing (Milk A320neo family) | Delay fps (supply-chain bottleneck) | Delay fps (talent poaching)
Enablers:       A320 customer base | government incentives | cash | A220-500 closing the seat-size gap
Constraints:    Engineering capacity (NGSA & A350 share teams) | fines if delay tactics are detected
```

## 2. Moves on the dashboard

| Briefing move | Order | Cost and timing | What the board does |
|---|---|---|---|
| Launch NGSA | `ngsa: launch` | **$30.07B** on this board (the slide says $20B), booked at EIS; EIS = launch + 7 | NGSA at $55M and 26.28% margin, against the A320neo at $52M and 13.14%. If NGSA enters service first: +3 pp a year (cap 80%) until fps arrives |
| A350 Re-engine (widebody; not on the slide) | `rea350: launch` | $5B at EIS; EIS = launch + 5 | Alone: A350 gains 1.5 pp a year to 60% and its margin rises from 4.95% to 10.76%. If the 787 also re-engines, the margin is 6.47% and share gains stop at the 787's EIS |
| Delay fps (supply-chain bottleneck) | `delay_tactics: bottleneck` | $1B, spent in the years before fps EIS | **Covert.** Boeing loses 5 pp of NB share for 5 years from fps EIS, and Airbus gains it |
| Delay fps (talent poaching) | `delay_tactics: poaching` | $1B, as above | Same effect. Two moves give the same 5 pp as one: they do not stack |
| Do Nothing | `hold` | — | A320neo and A350 as today |
| Engine choice | `ngsa_engine_code` 1-7 | — | Does not change Airbus's payoff on the board. A maker with no new engine ready by NGSA EIS is dropped; if none is left, NGSA flies CFM |
| Cancel | `ngsa: cancel`, `rea350: cancel` (before EIS) | write-off = bill × years elapsed ÷ development years | |

**Delay Tactics: the fine.**
- Delay Tactics are never published; the GM reveals them only at the end of the game.
- If Boeing never launches fps, they are "naked" and draw a **$48.32B fine**. The board books it at fps's snapshot date
  (2041), or at your order year if that is later.
- If Boeing launched fps and later cancelled it, there is no fine.
- They can be ordered in any round before fps enters service.

**Costs every plan carries.**
- Enterprise value $150B, debt $10B, WACC 8%, α 0.30. Your low debt keeps the penalty small: about $0.8B before
  discounting for NGSA.
- **Two-front strain.** $3B × the overlap between NGSA development (EIS − 7 to EIS) and A350 Re-engine development
  (EIS − 5 to EIS), divided by 5.

**Market rules that drive your number** (public; in `rules.md`).
- If fps enters service first, Boeing gains 1.0 pp a year (cap 80%), and the fps 7-year ramp-up adds 5 pp for 10
  years. When NGSA arrives, Airbus climbs back toward 50% at 1.0 pp a year if below 50%; otherwise shares freeze.
- If both enter service in the same year, Boeing climbs from 40% toward 50%.

## 3. Enablers and constraints in this game

| Item | On the board? | How it enters your decision |
|---|---|---|
| A320 customer base | yes: 60% status quo at 13.14% margin | The share you defend |
| Government incentives | no | ExCo judgement; the board books the full bill |
| Cash | yes: low debt, WACC 8% | CFO test |
| A220-500 closing the seat-size gap | no | A possible `other_moves` entry; the board does not price it |
| Engineering capacity (NGSA and A350 teams) | yes: two-front strain | COO test; hard rule 6 |
| Fines if Delay Tactics are detected | yes: the naked fine (above) | Hard rule 4 |

## 4. How the GM reports your objective

- **Defend the 60/40 edge:** Airbus NB share ≥ 60% in 2040, 2045 and 2050 (the worst year decides).
- **Protect the A320 family:** Airbus NB share ≥ 60% in every listed year (2030-2050) before NGSA enters service.

The objective never changes your payoff.

## 5. Profile updates for this game

- **Rule 1** (NGSA never enters service before the 2035 technology-ready year; launch window 2028-2030). Round 1
  (2030) is the last year of your window. An NGSA launched in 2030 enters service in 2037, which matches "around 2037".
- **Rule 2** (our own clock) and **rule 7** (never cancel NGSA in reaction to Boeing) apply as written.
- **Rule 3** (no A350 Re-engine after Boeing has launched a 787 Re-engine) applies as written.
- **Rule 4** (Delay Tactics at most once, only against an fps in development) reads here as: order Delay Tactics at
  most once, and only after Boeing has launched fps and before it enters service. There is no exposure mechanic in
  this game; the deterrent is the naked fine and your integrity rules.
- **Rule 5** (poaching only while an Airbus programme is in development) applies to the talent-poaching move.
- **Stricter Delay Tactics** (`executives/teams.md`, the 2026 ExCo: the move must change who enters service first).
  On this board Delay Tactics shift share, not entry into service, so read literally the condition keeps Delay Tactics
  off, and that is the default. Setting it aside, with the grid's $1B test standing in for it, is an adaptation the
  CEO must record in the rationale and in the Board item.
- **Rule 6** (at most one new launch per round; NGSA/A350 overlap of 2 years or less unless it pays at least $1B more)
  applies to the grid numbers in your brief.
- **Rule 8** cannot bind: no engine delays NGSA on this board; an engine that is not ready is dropped instead.
- **Superseded.** The engine numbers in `profile.md` and `objectives.md` came from the earlier engine and do not carry
  over. The dashboard's numbers in your brief replace them.

## 6. Each round

1. Read `rules.md` (Round 1) and your round brief.
2. Re-read `profile.md`: the decision procedure, the reaction function, and the hard rules as mapped above.
3. Re-read your team's section in `executives/teams.md` (default `faury-toepfer-wagner-2026`) and the role cards in
   `executives/roles/`.
4. Run the ExCo deliberation script: CEO, CFO, then the head of Commercial Aircraft.
5. Pick the scenario you expect from Boeing. State the best grid plan against it, your choice, and any doctrine or
   objective premium.
6. Write the `public_statement` in the CEO's voice. Never mention Delay Tactics in it. Then return the JSON orders.
