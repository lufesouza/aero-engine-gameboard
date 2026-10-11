# dash-2050-exco: the war game replayed by ExCo and Board agents (BOEING PROPRIETARY)

Four sealed rounds (2030, 2035, 2045, 2050), as in `../dash-2050/`, but each company decides as four agents: its
CEO, CFO and operating head (profiled from their own public words) and its Board of Directors (with a binding veto).
The board is the user's `combined_dash.py` at the `Game_v3.txt` snapshot (`wargame/dashgame/board/`, board version v3).
The agents are described in `../exco-agents/`.

| File | What it is |
|---|---|
| `dash_2050_exco_wargame.html` | The report page: summary, market shares, financials, programme dates, how each company decided (ExCo and Board), each round in detail with every company's decision chain, equilibria, regret, the comparison with the earlier game, method |
| `dash_2050_exco_report.md` | The full written report, round by round, with every year-by-year table and decision chain |
| `record/` | The game record: public rules, bulletins, every company's brief as sent, the ExCo and Board results (`exco_result_rN.json`, all steps), adjudicated records and states, payoff grids, stage-game benchmarks, isolation audits |
| `data/report_data.json` | Everything the page shows, from `wargame/dashgame/reports.py` |
| `data/crossvalue.json` | Each game's final state valued on both boards (`make_crossvalue.py`) |
| `narrative.py` | The written findings; `make_game_html.py` checks their headline numbers against the data when it builds |
| `make_game_html.py`, `make_game_md.py`, `page_kit.py` | Page and report builders |

## How the game was run (game master)

```
cd wargame/dashgame
DASH_RUN=dash-2050-exco DASH_BOARD=v3 python3 gm.py init          # the run keeps board v3 (runs/<run>/board.txt)
DASH_RUN=dash-2050-exco python3 gm.py brief N
# workflows/exco_round.js, once per company (args {run, round: N, year, sides: [side]}), in parallel
python3 exco.py merge ../runs/dash-2050-exco/exco_result_rN.json <the five workflow outputs>
DASH_RUN=dash-2050-exco python3 exco.py save N ../runs/dash-2050-exco/exco_result_rN.json
DASH_RUN=dash-2050-exco python3 gm.py adjudicate N ../runs/dash-2050-exco/orders_exco_rN.json
DASH_RUN=dash-2050-exco python3 stage_game.py N
DASH_RUN=dash-2050-exco python3 audit.py N <the five workflow transcript folders>
```

## Rebuild (needs Python 3 with pandas, numpy and plotly, which the board imports)

```
cd wargame/dashgame
DASH_BOARD=v3 python3 test_model.py && DASH_BOARD=v2 python3 test_model.py   # the GM valuation reproduces each board
DASH_RUN=dash-2050-exco python3 test_replay.py                               # the record replays exactly (needs runs/dash-2050-exco, a copy of record/)
python3 test_hook.py                                                         # the isolation hook
DASH_RUN=dash-2050-exco python3 reports.py && cp ../runs/dash-2050-exco/report_data.json ../reports/dash-2050-exco/data/
cd ../reports/dash-2050-exco && python3 make_crossvalue.py && python3 make_game_html.py && python3 make_game_md.py
```
