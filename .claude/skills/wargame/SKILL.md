---
name: wargame
description: Run or play the Boeing vs Airbus war game in this repo, optionally with Rolls-Royce as a third player (the engine supplier). Use when the user wants to start a game, play Boeing, Airbus or Rolls-Royce themselves, step through turns, or get a referee's efficiency scorecard. The Game Orchestrator agent referees. For a fully automated game with a verified after-action review, run the boeing-airbus-wargame workflow instead.
---

# Boeing vs Airbus war game

Three agents sit at the table, four with Rolls-Royce. `wargame/README.md` has the rules.

| Seat | Agent | Plays from |
|---|---|---|
| Boeing (Blue) | `boeing-strategist` | `wargame/profiles/boeing/`, Boeing's documented behaviour |
| Airbus (Red) | `airbus-strategist` | `wargame/profiles/airbus/`, Airbus's documented behaviour |
| Rolls-Royce (optional, engine supplier) | `rolls-royce-strategist` | `wargame/profiles/rolls_royce/`, Rolls-Royce's documented financial and operational behaviour |
| Referee | `game-orchestrator` | runs the game, relays public information, scores efficiency |

Rolls-Royce plays only in runs created with `new --suppliers rolls_royce`. It decides whether to build UltraFan engines for the airframers (widebody; narrowbody Solo or as a Joint Venture with Pratt & Whitney), on what terms, and whether to upgrade the Trent 1000. The market cell (`wargame-market`) reacts to public moves. `wargame-analyst` writes the after-action review. An isolation hook keeps the players apart.

## AI vs AI, refereed

Spawn the referee with the Agent tool: `subagent_type: game-orchestrator`. Give it:
- the scenario (`python3 -m wargame.engine scenarios`; default `base`);
- the number of turns (default 4);
- the inject policy (`umpire` by default, or `auto` or `none`);
- whether Rolls-Royce plays (`--suppliers rolls_royce`);
- whether you want the after-action review.

It dispatches every player each turn, relays disclosures, adjudicates, and writes `wargame/runs/<RUN>/referee_report.md` with the efficiency scorecard. When it's done, show the user the scorecard and the verdicts.

## The user plays one side

When the user takes a seat, **you** (the main session) are the Game Orchestrator: read `.claude/agents/game-orchestrator.md` and follow it. The one difference is that the user plays their side. Each turn:
1. Apply the inject. Show the user their side's brief (`brief --side <their side>`) as a short situation report: the inject, the programs, the rival's public statements and disclosures with your referee notes, their projection and their levers. Run `options --compact` or `whatif` on request. Never show them the rival's brief, orders, rationale or prediction.
2. Spawn the AI players (`boeing-strategist`, `airbus-strategist`, and `rolls-royce-strategist` if Rolls-Royce plays; all except the user's seat, in parallel) with only the run id, the turn, your public situation report and the user's *public* statements and disclosures from earlier turns. Never pass them the user's current orders or intentions. Keep their orders sealed until adjudication.
3. Collect the user's orders in plain language. Turn them into order JSON:
   - `launch`: {program, year, engine, variant}. For Rolls-Royce it is {program: uf_wb|uf_nb, year, variant: solo|jv_pw, terms: standard|aggressive}, with `t1000_upgrade` as its flag;
   - `cancel`;
   - flags;
   - `public_statement`;
   - `disclose`: what they choose to make public;
   - optional `prediction` and `expected_delta_pv_b`.

   Run `validate` and confirm the orders with the user.
4. Spawn `wargame-market` with the public part of every player's orders. Then adjudicate, annotate disclosures against the public record, and debrief the user on the public events and their new projection.

After the last turn, run `scorecard --final --format md` and write the referee report. The user is scored like any player, which makes their efficiency comparable with the AI's.

## Language

Say "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture" and "Delay Tactics" (never "Sabotage").
