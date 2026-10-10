# ExCo and Board agents: one agent per executive, one per Board

BOEING PROPRIETARY.

Each company in the dash-2050 war game can now be played by four agents instead of one: the CEO, the CFO and the
operating head of its default 2026 executive committee (ExCo), each profiled from that person's own words in the evidence
files under `wargame/profiles/<company>/executives/`, and its Board of Directors, profiled from the transcripts, filings
and web search under `wargame/profiles/<company>/board/` (spec: `BOARD_SPEC.md`). The Board recommends before each round
and approves or vetoes every order that differs from the default; its veto binds, and its culture (risk aversion, time
horizon) sets its tests. The game has **not** been run with these agents.

| Company | CEO | CFO | Operating head | Board |
|---|---|---|---|---|
| Boeing | `boeing-ortberg` | `boeing-malave` | `boeing-pope` | `boeing-board` |
| Airbus | `airbus-faury` | `airbus-toepfer` | `airbus-wagner` | `airbus-board` |
| CFM/GE | `cfm-culp` | `cfm-ghai` | `cfm-ali` | `cfm-board` (GE Aerospace, with Safran's consent on CFM) |
| Pratt & Whitney | `pratt-whitney-calio` | `pratt-whitney-mitchill` | `pratt-whitney-eddy` | `pratt-whitney-board` (RTX) |
| Rolls-Royce | `rolls-royce-erginbilgic` | `rolls-royce-mccabe` | `rolls-royce-watson` | `rolls-royce-board` |

## Files

- `.claude/agents/<agent>.md`: the twenty agent definitions (system prompts).
- `wargame/profiles/<company>/board/`: each Board's profile (`board.md`), evidence (`evidence.jsonl`, ids BG/AG/CG/PG/RG) and web
  sources (`sources.md`). Web facts come from web search (page fetches are blocked in this environment) and are never
  shown as quotes.
- `data/agents/<agent>.json`: each agent's profile, the data behind the page.
- `data/people.json`: evidence counts, dates and sources per person, taken from the evidence files.
- `SPEC.md`: the specification the agents were drafted to (template, sections, return fields, evidence rules).
- `check_agents.py`: checks every agent:
  - front matter and the 17 sections, in order;
  - every cited evidence id exists;
  - every quote is word for word from its source item;
  - each quote's date and perspective match the source.
- `make_exco_html.py`, `narrative_exco.py`: build `exco_agents.html`. The builder checks the numbers the text states
  against the data.
- `wargame/dashgame/workflows/exco_round.js`: the round script for the game master (not run). Per company and round it
  runs up to nine steps:
  0. Board guidance (recommendations);
  1. frame (CEO);
  2. test (CFO and operating head, in parallel);
  3. decide (CEO);
  4. veto check;
  5. revise (CEO, only if a binding veto or a red-line flag stands);
  6. Board review (approve or veto each Board item);
  7. board revise (CEO, only after a Board veto);
  8. Board confirm (a still-vetoed item reverts to the default; a failed review fails closed).
- `wargame/dashgame/workflows/dry_run.js`: runs the round script with stub agents, to check its flow.
- `wargame/dashgame/exco.py`:
  - `check` compares the script's order fields with `rules.py`;
  - `save` writes each company's ExCo notes and the orders file for `gm.py adjudicate`.
- `.claude/hooks/wargame_isolation.py`, tested by `wargame/dashgame/test_hook.py`: keeps each executive inside its own
  company's files, with no engine commands.

## Rebuild and check

```
python3 wargame/reports/exco-agents/check_agents.py
python3 wargame/reports/exco-agents/make_exco_html.py
python3 wargame/dashgame/test_hook.py
python3 wargame/dashgame/exco.py check
node wargame/dashgame/workflows/dry_run.js wargame/dashgame/workflows/exco_round.js
```

## Playing a round later (game master)

Use a fresh run id (the script refuses `dash-2050`, which holds the earlier game) and the same id in every command. The
earlier games' player folders were moved to `/tmp/wargame-archive/`, which no player can read, and the executives are
also blocked from any `/dash-2050/` path, so a replay cannot see the earlier orders.

1. `DASH_RUN=<run> python3 wargame/dashgame/gm.py init`, then `DASH_RUN=<run> python3 wargame/dashgame/gm.py brief N`.
2. Run the Workflow with `{scriptPath: "wargame/dashgame/workflows/exco_round.js"}` and
   `args: {run: "<run>", round: N, year}`. Save its result to a JSON file.
3. `python3 wargame/dashgame/exco.py save N <result.json>`.
4. `DASH_RUN=<run> python3 wargame/dashgame/gm.py adjudicate N wargame/runs/<run>/orders_exco_rN.json`.

The revise step runs when a colleague's binding veto stands or a colleague flags a company red-line breach.
