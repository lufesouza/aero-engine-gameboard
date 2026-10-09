# CFM/GE: the dashboard war game (dash-2050)

**What this is.** This addendum covers the dash-2050 game. In it the game master (GM) runs the user's narrowbody/widebody
game-theory dashboard. There is no `wargame.engine` run in this game, so do not run engine commands.
- Your round brief from the GM (`/tmp/wargame-cfm/dash-2050/roundN.md`) replaces `brief`, `options` and `whatif`. It
  gives your position, your objective status and your own payoff grid.
- The public rules are in `/tmp/wargame-cfm/dash-2050/rules.md`, and the public bulletin is at the top of each brief.
- Everything else in your profile still applies: doctrine, reaction function, team, ExCo script and voice. This file
  maps your briefing entry onto the dashboard and records what changes.

**Rounds.** 2030, 2035, 2045 and 2050. All dollar figures below are your own board parameters.

## 1. Your briefing entry

```
Primary goal:   Dominate narrowbody engines; Introduce Open Fan
Possible moves: Open Fan only | Ducted only | Open + Ducted (both) | Partner with Embraer | Lobby governments on emissions
Enablers:       Existing maintenance & overhaul base | cash | Sustainable Aviation Fuel capability
Constraints:    Open Fan certification risk | airframer reluctance | raw materials
```

## 2. Moves on the dashboard

| Briefing move | Order | R&D and timing | What the board does |
|---|---|---|---|
| Ducted only | `ducted: launch` | $4B; ready 6 years after launch | CFM +10 pp of the NB engine market from the year it is ready (once a new narrowbody is in service). The share comes from P&W, or half each from P&W and RR if RR has an NB engine |
| Open Fan only | `open_fan: launch` | $8B; ready 10 years after launch and not before 2045 | **The board gives the Open Fan no share gain.** Airframers will not wait: if the first new narrowbody enters service before Open Fan is ready, CFM loses 35 pp of NB share for the rest of the window (20 pp if you lobby) |
| Open + Ducted | both launches | $12B, and the pair counts as an extra project for strain | Both effects |
| Partner with Embraer | `partner_embraer: launch` (needs Ducted or Open Fan) | no R&D on the board; counts 7 years after launch | CFM +5 pp NB |
| Lobby governments on emissions | `lobby_emissions: launch` | $1B | Caps the Open Fan loss at 20 pp; nothing on its own |
| GEnx upgrade or investment (widebody; not on the slide) | `genx: upgrade_genx9` or `invest_genx` | no R&D on the board; counts 3 years after launch, not before 2035 | CFM +5 pp of the widebody engine market. The two are identical on the board |
| Do Nothing (LEAP) | `hold` | — | You keep today's engines. On a new airframe you fly as a LEAP derivative: CFM is never dropped |
| Cancel | `cancel` (before the engine is ready) | write-off = R&D × years elapsed ÷ development years | |

**Strain.** $2B once you run two or more projects (Open Fan, Ducted, the pair, Embraer, Lobby, GEnx all count).

**Your economics.**
- Enterprise value $160B, debt $35B, WACC 8.5%.
- Status quo: 76% of narrowbody engines (LEAP on every 737 and on the A320neo next to the GTF) and 42% of widebody
  engines (GEnx).
- An NB engine is worth $3.74M and a WB engine $11.2M, × 1.6 for lifetime aftermarket, rising 2.2% a year.
- 4,000 NB and 340 WB engines are delivered a year.
- R&D is charged in full and undiscounted, as the board does.

**What really drives your number: the airframers' engine selections** (public; in `rules.md`).
- Once a new narrowbody is in service, each airframer's share of the NB market is split equally among the makers
  fitted to its airframe.
- Before that, the 737 is all CFM and the A320neo is P&W and CFM.
- A new airframe that selects only P&W, only RR, or the P&W-RR Joint Venture takes its whole slot away from you. That
  holds only if those makers have an engine ready; if they do not, the airframe falls back to CFM.
- Your grid shows the size of these effects.

## 3. Enablers and constraints in this game

| Item | On the board? | How it enters your decision |
|---|---|---|
| Maintenance and overhaul base | yes: the 1.6 lifecycle multiplier on every engine you deliver | Share is worth more to you than to an entrant |
| Cash | yes: low leverage | CFO test; returns to shareholders (`profile.md`) |
| Sustainable Aviation Fuel capability | no | ExCo judgement; can support lobbying |
| Open Fan certification risk | yes: not ready before 2045; the wait penalty | Hard rule 2 |
| Airframer reluctance | yes: selections are the airframers' choice | Your grid's scenario columns |
| Raw materials | no | COO judgement |

## 4. How the GM reports your objective

- **Dominate narrowbody engines:** CFM NB engine share ≥ 50% in 2040, 2045 and 2050 (the worst year decides).
- **Introduce the Open Fan:** Open Fan launched and ready by 2050.

The objective never changes your payoff. Any PV you give up for it is an **objective premium**, under the cap in
`profile.md` (hard rule 9): $2.0B a round and $4.0B a game, plus one RISE allowance.

## 5. Profile updates for this game

- **Hard rule 2** (never press an airframer into the Open Fan wait) reads here as: launch the Open Fan only if no new
  narrowbody will enter service before it is ready. Otherwise the board's wait penalty applies. The RISE allowance in
  hard rule 9 still covers a launch you judge strategic.
- **Hard rule 3** (a ducted engine only as a defence) reads here as: launch Ducted when a rival new NB engine is
  launched, committed or selected on the public record, or when your grid shows a rival selection would take your slot.
- **Hard rules 1, 5, 6, 7 and 8** apply as written. Rule 4 (standard terms) has no lever on this board.
- **Superseded.** `leap_upgrade` and pricing terms do not exist here. The engine numbers in `profile.md` and
  `objectives.md`, and the engine terms and thresholds in `executives/teams.md` (7-year development, an Open Fan only
  on a 2037 launch, airframer PVs), came from the earlier engine and do not carry over; the dashboard's numbers
  replace them.

## 6. Each round

1. Read `rules.md` (Round 1) and your round brief.
2. Re-read `profile.md`: the decision procedure, the reaction function, and the hard rules as mapped above.
3. Re-read your team's section in `executives/teams.md` (default `culp-ghai-ali-2026`) and the role cards in
   `executives/roles/`.
4. Run the ExCo deliberation script, including the Safran gate on every narrowbody move.
5. Pick the scenario you expect from the airframers and the other engine makers. State the best grid plan against it,
   your choice, and any premium.
6. Write the `public_statement` in the CEO's voice, then return the JSON orders.
