# ExCo agents: one agent per executive

BOEING PROPRIETARY.

Each company in the dash-2050 war game can now be played by three agents instead of one: the CEO, the CFO and the
operating head of its default 2026 executive committee. Each agent is profiled from that person's own words in the
evidence files under `wargame/profiles/<company>/executives/`. The game has **not** been run with these agents.

| Company | CEO | CFO | Operating head |
|---|---|---|---|
| Boeing | `boeing-ortberg` | `boeing-malave` | `boeing-pope` |
| Airbus | `airbus-faury` | `airbus-toepfer` | `airbus-wagner` |
| CFM/GE | `cfm-culp` | `cfm-ghai` | `cfm-ali` |
| Pratt & Whitney | `pratt-whitney-calio` | `pratt-whitney-mitchill` | `pratt-whitney-eddy` |
| Rolls-Royce | `rolls-royce-erginbilgic` | `rolls-royce-mccabe` | `rolls-royce-watson` |

## Files

- `.claude/agents/<agent>.md`: the fifteen agent definitions (system prompts).
- `data/agents/<agent>.json`: each agent's profile, the data behind the page.
- `data/people.json`: evidence counts, dates and sources per person, taken from the evidence files.
- `check_agents.py`: checks every agent:
  - front matter and the 17 sections, in order;
  - every cited evidence id exists;
  - every quote is word for word from its source item;
  - each quote's date and perspective match the source.
- `make_exco_html.py`, `narrative_exco.py`: build `exco_agents.html`. The builder checks the numbers the text states
  against the data.
- `wargame/dashgame/workflows/exco_round.js`: the round script for the game master (not run). Per company and round it
  runs five steps:
  1. frame (CEO);
  2. test (CFO and operating head, in parallel);
  3. decide (CEO);
  4. veto check;
  5. revise (CEO, only if a binding veto stands).
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

1. `DASH_RUN=<run> python3 wargame/dashgame/gm.py init`, then `gm.py brief N`.
2. Run the Workflow with `{scriptPath: "wargame/dashgame/workflows/exco_round.js"}` and
   `args: {run, round: N, year}`. Save its result to a JSON file.
3. `python3 wargame/dashgame/exco.py save N <result.json>`.
4. `python3 wargame/dashgame/gm.py adjudicate N wargame/runs/<run>/orders_exco_rN.json`.
