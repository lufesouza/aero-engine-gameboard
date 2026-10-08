# dash-2050: five-player war game on the game-theory dashboard (BOEING PROPRIETARY)

Four sealed rounds (2030, 2035, 2045, 2050) played by five strategist agents (Boeing, Airbus, CFM/GE, Pratt & Whitney,
Rolls-Royce) on the user's Combined_Game_Board.py, with the game master's code in `wargame/dashgame/`.

| File | What it is |
|---|---|
| `dash_2050_wargame.html` | The report page: summaries, market shares, financials, programme dates, each round in detail, regret, method |
| `dash_2050_report.md` | The full written report, round by round, with every year-by-year table |
| `record/` | The game record: public rules, bulletins, every player's brief (as sent), returned orders, adjudicated records, states, payoff grids, stage-game benchmarks, isolation audits, `report_data.json` |
| `narrative.py` | The written findings; `make_dash_html.py` checks their headline numbers against the data when it builds |
| `make_dash_html.py`, `make_dash_md.py`, `page_kit.py` | Page and report builders |

Rebuild (needs Python 3 with pandas, numpy and plotly, which the board imports):

```
cd wargame/dashgame && python3 test_model.py          # the GM valuation reproduces the board
DASH_RUN=dash-2050 python3 reports.py                  # needs wargame/runs/dash-2050 (copy of record/)
cp ../runs/dash-2050/report_data.json ../reports/dash-2050/data/
cd ../reports/dash-2050 && python3 make_dash_html.py && python3 make_dash_md.py
```
