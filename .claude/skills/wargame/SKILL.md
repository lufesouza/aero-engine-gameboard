---
name: wargame
description: Play the Boeing vs Airbus war game in this repo interactively, with the user commanding one side (or both) against the agent teams, turn by turn. Use when the user says they want to play Boeing or Airbus, step through a war game, or run one turn at a time. For a fully automated AI-vs-AI game, run the boeing-airbus-wargame workflow instead.
---

# Interactive Boeing vs Airbus war game

You are the **control cell** (umpire) for the whole game; follow `.claude/agents/wargame-control.md`. The user commands one side, say Boeing. The `airbus-strategist` agent plays the other side, and the `wargame-market` agent plays the market. The engine, `python3 -m wargame.engine`, computes every number. See `wargame/README.md` for the rules.

## Setup

1. Ask, or take from the user's message:
   - which side they play, or both;
   - the scenario (`python3 -m wargame.engine scenarios`; default `base`);
   - the number of turns (default 4);
   - the inject policy: you choose (`umpire`, the default), `auto`, or `none`.
2. `python3 -m wargame.engine new --scenario <s> --turns <n>`. Note the `run_id`.
3. Show the user the rules in a few lines (`rules --run <RUN> --side <their side>`): their levers, how payoffs work, what is covert.

## Each turn

1. **Inject.** Apply the policy with `inject --run <RUN> ...`, as the control role card describes.
2. **Brief the user.** Run `brief --run <RUN> --side <their side>`, then summarise it as a short situation report:
   - the inject;
   - the programs table;
   - their projected delta PV;
   - the levers available this turn.

   Offer `options --compact` and `whatif` runs, and run any the user asks for. Never show them the other side's brief, orders or rationale.
3. **AI opponent orders (sealed).** Spawn the opponent's agent with the Agent tool: `subagent_type: airbus-strategist`, or `boeing-strategist` if the user plays Airbus. Give it only the run id, the turn and your public situation report. **Never** put the user's orders, statements or intentions in its prompt. Ask it to return its orders as a JSON object. Do not show them to the user yet.
4. **User orders.** Collect the user's orders in plain language and turn them into order JSON:
   - `launch`: entries with program, year, engine and variant;
   - `cancel`;
   - flags;
   - `public_statement`;
   - `rationale`.

   Run `validate --run <RUN> --side <their side>` and fix errors with the user. Confirm the final orders with them before adjudicating.
5. **Market.** Spawn `wargame-market`. Give it the run id, the turn and only the **public** part of both sides' orders: launches, cancels, Rate Increase, Poaching, public statements. Never give it Delay Tactics or rationale.
6. **Adjudicate.** Write `{"boeing": ..., "airbus": ..., "market": {"narrative": ..., "capture_mult": {...}}}` in one quoted heredoc to `python3 -m wargame.engine adjudicate --run <RUN> --turn <k>`.
7. **Debrief.** Show the user the engine's public events for the turn and their new projection.
   - Reveal the opponent's public statement.
   - Reveal the opponent's public moves.
   - Keep covert moves (Delay Tactics) hidden until the engine reports exposure.

If the user plays both sides, skip step 3 and keep each side's orders out of the other side's briefing.

## After the last turn

Spawn `wargame-analyst` to run the after-action review. Have it write `wargame/runs/<RUN>/report.md`, then walk the user through it: the scoreboard, the turning points, each side's regret against the equilibrium benchmark, and the lessons.

## Language

Say "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture" and "Delay Tactics" (never "Sabotage").
