# Reader brief: Rolls-Royce evidence for the war-game profile

You extract **machine-checkable evidence** about Rolls-Royce Holdings plc (RR) from spreadsheets (and, for one reader, text). A later stage turns the evidence into the behavioural profile an independent agent will use to play Rolls-Royce in a strategy war game. That agent reads nothing else about RR, so the evidence must show how RR has behaved and what its finances allow:
- financially: capital allocation, R&D, balance sheet, guidance;
- operationally: deliveries, engine economics, aftermarket, execution problems;
- in response to others: airframers, competitors, crises.

## The game RR will play

The game is Boeing vs Airbus, 4 turns (2026-28, 2029-31, 2032-34, 2035-37), with a deterministic engine that scores full-game PV versus the status quo. RR joins as the third player: the engine supplier. RR's levers each turn:

1. **Launch UltraFan widebody** (`uf_wb`). Develop the UltraFan-based widebody engine. This makes it selectable for Boeing's 787 Re-engine and Airbus's A350 Re-engine.
2. **Launch UltraFan narrowbody** (`uf_nb`), in one of two variants:
   - `solo`: RR funds all of it. RR has had no narrowbody engine since it left IAE/V2500.
   - `jv_pw`: a Joint Venture with Pratt & Whitney, sharing capex and value 50/50.

   This makes the engine selectable for Boeing's new single-aisle (fps) and Airbus's NGSA.
3. **Terms** on each launch:
   - `standard`;
   - `aggressive`: price concessions that give the airframer margin and cost RR value per engine.
4. **Trent 1000 upgrade** (one-time). Spend on durability and performance to win back share of 787 deliveries and cut installed-base costs.
5. **Cancel** an RR engine program that no airframer uses.
6. **Do Nothing.**

Airframers choose engines. An airframer can select an RR engine only if RR has committed to it. RR's payoff is the lifecycle value of engines delivered: the original-equipment (OE) margin, which is often negative for new engines, plus aftermarket profit, less development capex.

The key RR franchises are:
- A350: Trent XWB, sole source;
- A330neo: Trent 7000, sole source;
- 787: Trent 1000, which competes with the GE GEnx;
- business jets (Pearl), Defence and Power Systems.

## Sources (read the cell dumps, not the workbooks)

Cell dumps are in `RR/cells/`; `RR` is the path given in your task. There is one TSV per sheet. Each line reads:

`ref <TAB> value <TAB> row label <TAB> nearest period header above`

For example, `AS41 21.017 Large engine thrust delivered (Mlbs) 2023`. Always check the period header against the sheet's header row (grep the ref's column in row 1-5 for MS sheets, or the "For the Fiscal Period Ending" / "FY" row for Capital IQ).

| source id | workbook | what it is |
|---|---|---|
| `ms_model` | Morgan Stanley Rolls-Royce model.xlsm | Morgan Stanley equity research model dated 28 Jan 2026 (analyst Ross Law). Historic 2000-2025 and estimates 2H25e-2030e. Sheets: Valuation Summary, Divisional, IS, CFS, BS, Civil, Civil OE, Civil AM, Civil AM bridge, Defence, Power Systems, Bull Bear Base, ImportantDisclosures |
| `ciq_estimates` | Rolls-Royce Holdings plc LSE RR Estimates Report.xls | S&P Capital IQ, as of about spring 2026 (current fiscal year FY2026). Sheets: Consensus, Recent Changes, Guidance, Multiples, Surprise, Trends, Revisions |
| `ciq_segments` | Rolls-Royce Holdings plc LSE RR Financials Segments.xls | S&P Capital IQ segment history, FY2015-FY2025 (GBP m) |

Currency is GBP unless the row says otherwise. Some Capital IQ Surprise rows are for the US ADR (OTCPK:RYCE.Y, USD); say so if you use them. Estimates ("e" columns, consensus) are **forecasts**. Tag them `analyst_view` or `market_view`, never `own_behaviour`.

## Output

Write JSON Lines to `RR/evidence/<your reader id>.jsonl`, one finding per line:

```json
{"company": "rolls_royce", "category": "capital_allocation", "date": "2025-12-31",
 "source": "ms_model", "doc": "Morgan Stanley RR model (28 Jan 2026)",
 "cells": [{"source": "ms_model", "sheet": "CFS", "ref": "AA40", "value": -1000, "label": "Share buyback", "period": "2025"}],
 "finding": "RR bought back about £1.0bn of shares in 2025, the first buyback since ...",
 "numbers": {"buyback_2025_gbp_m": 1000},
 "implication": "(inference) With net cash, RR returns surplus cash rather than ...",
 "perspective": "own_behaviour", "reader": "<your reader id>"}
```

**Required fields**
- `company`: always `"rolls_royce"`.
- `category`, one of:
  - `financial`, `segment`, `civil_oe`, `civil_aftermarket`, `capital_allocation`, `balance_sheet`;
  - `guidance`, `surprise`, `consensus`, `valuation`, `scenario`;
  - `defence`, `power_systems`, `operations`, `competitor_view`, `strategy`.
- `date`: the period end (e.g. `2025-12-31` for FY2025, `2025-06-30` for 1H25) or the document date. For a series, use the latest period cited.
- `source`, `doc`, `cells`, `finding`, `numbers`, `perspective`, `reader`.

**`perspective`** is one of:
- `own_behaviour`: reported actuals, i.e. what RR did;
- `analyst_view`: Morgan Stanley estimates and scenarios;
- `market_view`: consensus, revisions, multiples;
- `observed_by_boeing` / `observed_by_airbus`: text readers only.

**`cells`** lists 1-8 cells that establish the finding.
- Include the row label and period so that a reader can see what each cell is.
- Values must be the cell's value. You may round to 3 significant figures, and a percentage cell holding 0.222 may be cited as `"22.2%"`.
- For a time series, cite each year's cell. Several items for long series are fine.

**`finding`** is one factual sentence of what the cells show. No claims beyond them.

**`implication`** (optional) is a behavioural reading. It must start with `(inference)`.

## Verification (mandatory)

When done, run:

```
WARGAME_BUILD_DIR=<S> RR_CELLS_DIR=<RR>/cells python3 wargame/profiles/build/verify_cells.py <RR>/evidence/<id>.jsonl
```

Fix or delete every rejected item and re-run until 100% pass. Leave the `.verified.jsonl` output in place. Text readers use `verify_quotes.py` instead (see their task).

## Coverage expectations

- **Aim for 40-90 items.** Prefer time series across eras over only the latest year. The eras are:
  - pre-2010;
  - 2010-2015 growth;
  - 2016-2019: Trent 1000 durability crisis and restructuring;
  - 2020-2022: COVID, rights issue and disposals;
  - 2023-2025: turnaround and margin expansion;
  - 2026-2030: estimates.
- **Every item must be useful to someone deciding** whether RR should fund a new engine, how aggressively it prices, and how much risk its balance sheet can take.
- **Note the behaviour-revealing patterns:**
  - what RR cut first in the crisis (R&D? capex? dividend?);
  - when it raised equity;
  - what it sold;
  - how its guidance compared with outcomes;
  - how it prices its aftermarket (LTSA).

## Also return (your final message, as structured output)

- A **summary** of up to 700 words: the key numbers with cell refs, and patterns across eras.
- **calibration_candidates**: numbers the engine could use, each with a derivation and cell refs. For example:
  - lifecycle value per widebody engine (OE margin plus PV of aftermarket profit per engine, in $M);
  - OE revenue or cash price per engine;
  - aftermarket revenue per engine flying hour (EFH) and EFH growth;
  - Civil margin;
  - R&D spend per year and share of revenue;
  - capex;
  - WACC or discount rate used by Morgan Stanley;
  - USD/GBP rate implied;
  - net cash;
  - Trent 1000 costs;
  - UltraFan or narrowbody-entry references;
  - engine delivery counts (large engines per year).
- **gaps**: what the data cannot tell.
