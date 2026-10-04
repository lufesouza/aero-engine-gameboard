# Boeing vs Airbus war game

A multi-turn strategy war game. Three agents sit at the table, five with the engine makers:
- **Boeing** and **Airbus** are independent players, each built from its company's documented record;
- **Rolls-Royce** and **Pratt & Whitney** are optional engine-supplier players, also built from their own records. They decide which engines to build for the airframers, on what terms, and whether to partner;
- the **Game Orchestrator** is the referee. It gives each player its task, relays only what a player chooses to make public, and measures each player's efficiency.

A **market** cell reacts to public moves. A deterministic Python engine adjudicates every move, so no payoff is ever an agent's guess. After the last turn an **analyst** reviews the game against its game-theoretic benchmark. Every claim in that review is checked by three independent agents before it reaches the report.

```
                 ┌──────────── each turn (sealed, simultaneous) ────────────┐
 game-orchestrator ─task─► boeing-strategist ─┐                             │
   (referee)      ─task─► airbus-strategist ──┼─► wargame-market ──► referee │
                                        │   (public moves only)  `adjudicate`│
                                        └────────── wargame engine ◄─────────┘
 after the last turn:  wargame-analyst (AAR) ──► 3 checkers per claim ──► report.md
```

## Three ways to run it

**1. AI vs AI, fully automated.** Ask Claude Code:

> Run the boeing-airbus-wargame workflow

Arguments are all optional. Pass them in the request, e.g. *"run the boeing-airbus-wargame workflow with turns 2, scenario fps-slip, injects auto"*.

| Argument | Default | Meaning |
|---|---|---|
| `turns` | 4 | 1-4 turns (2026-28, 2029-31, 2032-34, 2035-37) |
| `scenario` | `base` | `base`, `fps-slip`, `supply-crunch`, `replacement-wave` (see `scenarios/`) |
| `injects` | `umpire` | `umpire` (the referee picks shocks), `auto` (deterministic from `seed`), `none` |
| `games` | 1 | 1-4 independent plays in parallel, plus a cross-game synthesis |
| `seed` | 0 | seed for `auto` injects (game *i* uses `seed + i - 1`) |
| `run_id` | `wg-<timestamp>` | run name (`-g<i>` appended when `games` > 1) |
| `leadership` | today's teams | executive team per airframer, e.g. `{"boeing": "muilenburg-smith-2017"}`; ids in `profiles/<side>/executives/teams.md` |
| `doctrine` | none | board guidance per side, e.g. `{"boeing": "balance sheet cannot fund two programs at once"}` |
| `fixed_orders` | none | script one side, e.g. `{"boeing": {"1": {"launch": [{"program": "fps", "engine": "cfm_ducted", "variant": "jv"}]}}}` |
| `suppliers` | none | engine makers who play: `["rolls_royce"]`, `["pratt_whitney"]` or both |
| `verify` | true | run the three-checker verification of the after-action review claims |

Output: `wargame/runs/<run_id>/report.md`, plus `state.json` and `turns/T<k>.json`. A 4-turn game spawns roughly 45 agents, most of them in the verification stage. `verify: false` makes it cheaper.

**2. Refereed game, or play a side yourself.** Type `/wargame`.
- Say *"run a refereed game"* and the Game Orchestrator runs Boeing against Airbus.
- Say *"I want to play Boeing"* and Claude referees while you play. You get Boeing's brief each turn and give orders in plain language. The `airbus-strategist` agent plays Airbus without seeing your orders.

You are scored like any player.

**3. Drive the engine directly.** Everything is `python3 -m wargame.engine <command>`, with JSON output and no dependencies beyond Python 3.10+.

```bash
python3 -m wargame.engine new --run-id demo                 # create a run
python3 -m wargame.engine inject --run demo --auto          # this turn's shock
python3 -m wargame.engine brief --run demo --side boeing    # Boeing's fog-of-war view
python3 -m wargame.engine options --run demo --side boeing --compact   # this turn's stage game
python3 -m wargame.engine adjudicate --run demo --turn 1 <<'EOF'
{"boeing": {"launch": [{"program": "fps", "variant": "solo", "engine": "cfm_ducted", "year": 2027}]},
 "airbus": {"launch": [{"program": "ngsa", "engine": "cfm_ducted", "year": 2026}], "delay_tactics": true}}
EOF
python3 -m wargame.engine equilibria --run demo --segment wb   # widebody sub-game
python3 -m wargame.engine report --run demo --format md
```

## The cast

Defined in `.claude/agents/`. Each is a Claude Code subagent you can also call on its own.

| Agent | Role | Sees |
|---|---|---|
| `boeing-strategist` | Blue: fps (Solo / Joint Venture), 787 Re-engine, 737 Rate Increase, cancellations, engine choice. Plays from `wargame/profiles/boeing/` | public view + Boeing's own numbers + Boeing's profile |
| `airbus-strategist` | Red: NGSA, A350 Re-engine, Delay Tactics (covert), Poaching, cancellations, engine choice. Plays from `wargame/profiles/airbus/` | public view + Airbus's own numbers + Airbus's profile |
| `rolls-royce-strategist` | Engine supplier (optional): UltraFan widebody, UltraFan narrowbody (Solo / Joint Venture with P&W), terms, Trent 1000 upgrade, cancellations. Plays from `wargame/profiles/rolls_royce/` | public view + RR's own numbers + RR's profile |
| `pratt-whitney-strategist` | Engine supplier (optional): next-generation GTF, a widebody engine, terms, GTF durability upgrade, joining RR's Joint Venture, cancellations. Plays from `wargame/profiles/pratt_whitney/` | public view + P&W's own numbers + P&W's profile |
| `wargame-market` | Green: airlines, lessors, and the engine OEMs that are not players (CFM/GE, and RR/PW unless they play) set bounded capture multipliers | public view only |
| `game-orchestrator` | Referee (White): creates runs, applies injects, gives both players equal sealed tasks, relays public statements and **disclosures** with a public-record note, adjudicates verbatim, and scores efficiency | everything; never computes payoffs, and never leaks private information |
| `wargame-analyst` | after-action review and report | everything |

The orchestration is `.claude/workflows/boeing-airbus-wargame.js`. The interactive mode is `.claude/skills/wargame/SKILL.md`.

## Behavioural agents

The strategists are **independent agents built from each company's record**, not generic optimisers. Each plays from its own folder:

| File | What it holds |
|---|---|
| `profile.md` | A Quick card (ranked objectives, hard rules, default plan, top triggers, biases), then 10 sections: objectives, financial behaviour, operational behaviour and slip priors, product doctrine, **reaction function**, lever-by-lever playbook, how it reads the rival, biases and failure modes, a turn-by-turn decision procedure, and confidence and gaps |
| `reaction_function.json` | "If the rival does X → we historically did Y", with lag, strength, the war-game translation and evidence ids |
| `financials.md` | Decision-relevant financial history and the analysts' forward view |
| `evidence.jsonl` | Every cited item (B-#### / A-#### / R-#### / P-####). Text items carry a verbatim quote, source, page, date, speaker and finding, and each quote was machine-checked against its page. Spreadsheet items cite workbook cells, and each value was checked against the workbook |
| `calibration.md` | Engine makers only: the derivation of every game parameter from the evidence |
| `citation_audit.md` | An independent audit of every load-bearing claim against its cited evidence |

**Where the evidence comes from.** These are the files uploaded to the repository root.
- **Boeing:** 151 earnings calls, conferences and investor days from 2006-2025; 16 10-Ks; the Goldman Sachs and Morgan Stanley models; Capital IQ history.
- **Airbus:** its FY2025 Board Report (OCR'd). Its 2006-2025 behaviour also appears as observed in Boeing's calls and 10-Ks, and every such item is tagged as an outside view.
- **Rolls-Royce:**
  - 54 of its own earnings calls and investor events, 2010-2025;
  - the Morgan Stanley RR model (Jan 2026);
  - Capital IQ consensus, guidance, surprise and segment histories;
  - Boeing's and Airbus's comments on RR;
  - the 2019 engine-makers strategy brief.

  That is 1,951 verified items (R-####).
- **Pratt & Whitney:**
  - 58 UTC/RTX calls and investor events, 2015-2025;
  - the UTC/RTX 10-Ks, FY2016-FY2024;
  - the Goldman Sachs RTX model with its GTF analysis (Oct 2025);
  - FlightGlobal on GTF durability (Nov 2025);
  - the 2019 strategy brief.

  That is 2,072 verified items (P-####).

The Airbus record is thinner. Airbus earnings-call transcripts or older annual reports would improve it most. `wargame/profiles/build/README.md` explains how to rebuild.

**How they decide.** Each turn a strategist:
1. reads its Quick card;
2. matches the situation to its reaction function;
3. uses the engine (`options`, `whatif`) as its finance team;
4. decides by its profile's decision procedure.

When history leads it away from the PV-best option, it reports the **doctrine premium** (the $B it gave up) and the evidence ids behind the choice.

**Independence.** The agents share nothing but the public game.
- Each profile was synthesised by agents that never saw the other side's material.
- The Airbus agent's view of Boeing is limited to Boeing's 2023-25 public statements.
- The Boeing agent's view of Airbus is what Boeing has said about Airbus.
- The PreToolUse hook `.claude/hooks/wargame_isolation.py` enforces this at runtime. Boeing's agent cannot read Airbus's profile or role card, and Airbus's cannot read Boeing's. Neither player, nor the market cell, can read run state, where sealed orders live.

## Leadership teams (executive profiles)

Boeing and Airbus each decide as a **named executive team**: a CEO, a CFO and the head of commercial aircraft. Each person is profiled from their own words. The files are in `wargame/profiles/<side>/executives/`:
- one profile per executive: Quick card, commitment track record, sections by dimension, and "in the game";
- `teams.md`: the teams by era, each with its decision rule, tensions and a per-turn ExCo deliberation script;
- `evidence.jsonl`: verified quotes, BX-#### for Boeing and AX-#### for Airbus;
- `citation_audit.md`.

**Boeing** draws on the executives' own turns on calls and investor days, 2006-2025 (1,874 items). It covers:
- CEOs: McNerney, Muilenburg, Calhoun and Ortberg (Ortberg including his Collins years);
- CFOs: Bell, Smith, West and Malave;
- heads of Commercial Airplanes: Albaugh, Conner, Deal and Pope.

The teams run from `mcnerney-bell-albaugh-2010` to today's **`ortberg-malave-pope-2026`**, the default. A historical team plays "that team running Boeing in 2026".

**Airbus** draws only on the FY2025 Board Report (the CEO's objectives and pay weights, and the executive team) and on mentions by Boeing and RTX executives (109 items). The default team is `faury-toepfer-wagner-2026`, and it is low-confidence. Airbus earnings-call transcripts would make it comparable to Boeing's.

**Use.** Choose the teams with the workflow's `leadership` argument, e.g. `{"boeing": "muilenburg-smith-2017"}`, or tell the referee. Each turn, the strategist runs its team's ExCo deliberation and records it in its rationale. The referee scores leadership fidelity. The isolation hook keeps each company's executive files private, and the period-locked 2010 players cannot read them.

## The referee: information sharing and efficiency scoring

**Sharing.** Orders are sealed. Two things are public automatically: moves the engine makes public (launches, cancellations, Rate Increase, Poaching, slips with their public cause, exposures), and each player's `public_statement`. On top of that, a player can **choose** to make things public through `disclose`: commitments, planned entry-into-service dates, warnings. The Game Orchestrator relays disclosures verbatim to the rival and the market at the start of the next turn, since moves are simultaneous. It adds a note, checked **only against the public record**:
- "consistent with the public record";
- "contradicted by the public record";
- "not publicly verifiable".

The referee never uses private knowledge, so a player can bluff about covert moves without the referee exposing it.

**Scoring.** Run `python3 -m wargame.engine scorecard --run <RUN> [--final] [--format md]`. The scorecard is referee-only until the game ends. The engine computes every metric:

| Metric | Meaning |
|---|---|
| capture / myopic regret | each turn: the value of the player's orders against the rival's **actual** orders, versus the best and worst available responses |
| hindsight regret (`--final`) | the best full plan against the rival's actual play, minus what the player got |
| prediction accuracy | the share of the rival's launches, cancellations and flags the player forecast correctly (from its private `prediction`) |
| calibration | the engine's projection after the turn, minus the player's `expected_delta_pv_b` |
| disclosures | how much the player chose to reveal |

In `wargame/runs/<RUN>/referee_report.md` the referee adds verdicts on information use, discipline and **doctrine fidelity**: whether each player's moves matched its own profile. It separates skill from documented company behaviour, so a declared doctrine premium counts as faithful play, not a blunder.

*Limitation:* the plan-game solver (`equilibria`, hindsight regret) only tries launches in the first year of each turn. The per-turn scorecard always includes the player's actual orders, whatever the launch year.

## Assigned objectives

Each player also has a **mission** set by control: a primary goal, the possible moves mapped to game levers (modelled yes / partly / no), its enablers and constraints, and metrics the engine scores at key years (share targets, engines delivered, upgrades, an engine in service). The missions live in `config/default.json` under `objectives`.

**Who sees what:**
- A player sees only its own mission, through `rules --side <side>` (`assigned_objectives`), `brief` (`your_objectives`) and `whatif` (`objectives`).
- Control and the analyst see every mission. The market view shows none.
- Player agents may not read `config/` (isolation hook).

**Scoring:**
- `report` and `scorecard` tabulate attainment, including a table by turn.
- Objectives **never change the payoff**. A player that gives up delta PV to advance its mission declares an "objective premium", which counts against its doctrine-premium cap.

**Further reading:**
- Each player's brief is `profiles/<player>/objectives.md`.
- The referee's cross-player analysis (conflicts, joint feasibility, how to score) is `profiles/overview/objectives_analysis.md`.

Objectives are off in `hist-2010-neo`.

## How a turn works

1. **The Game Orchestrator** (referee) applies at most one inject from the deck (demand shock, engine maturity slip, supply crunch, FAA scrutiny, fuel spike, quality escape, trade dispute, or a quiet turn). It then writes a public situation report, and includes the rival's disclosures from the previous turn with its public-record notes.
2. **Boeing and Airbus** order in parallel and cannot see each other. Each runs `brief`, `options` (this turn's stage game), `whatif` counterfactuals and `validate` before returning sealed orders, a public statement and a private rationale.
3. **Market** sees only the public half of both sides' orders and sets capture multipliers (0.75-1.25) for launched programs.
4. **The referee** runs `adjudicate` with the exact JSON the workflow built. The workflow stamps each side's orders with an FNV-1a fingerprint. The engine refuses to adjudicate if the orders arrive changed, so an agent retyping JSON cannot corrupt a game. Rejected orders go back to the player with the engine's errors, once. The referee then annotates each side's disclosures against the public record.

## Rules of the engine

Money is $B in constant 2026 dollars. A side's score is **delta PV**: the present value, at its WACC, of its operating profit minus the status-quo profit (nobody moves, same injects), less alpha-loaded capex, alpha-loaded strain and tactic costs. The components (NB operating, WB operating, capex, strain, tactics) always sum exactly to the total.

- **Programs.** Each side has one new narrowbody (fps, NGSA) and one widebody Re-engine (787, A350).
  - Each can be launched once, in any year of a turn. EIS = launch + development years (+ engine `eis_add`, injects and slips).
  - An engine can carry `available_eis`, the first year it can enter service. The CFM RISE open fan (`cfm_open_fan`) is available from **2045** only. An airframe that would be ready earlier waits for it, and each waiting year costs 10% of capex like any other extra year. A launch in 2037 (2037 + 7 + 1) enters service in 2045 without waiting.
  - Capex is spread over the base development years. Each extra year costs 10% of capex.
  - Cancelling stops capex; what was spent is sunk.
- **Share.** The first side to put a new product into service in a segment captures share at `capture_pp_per_year` (× engine × market multipliers). Capture starts at EIS+1, stops at the leader cap, and freezes when the follower's new product enters service.
- **Margins.**
  - A new product earns `margin_alone` until the rival's new product is also in service, then `margin_both`.
  - It loses `early_penalty_pp_per_year` for each year its EIS precedes `tech_ready_year`.
  - It gains the engine's `margin_pp`.
  - A Joint Venture gives Embraer 25% of fps margin, in exchange for 35% of the capex and half the strain.
- **Strain** (overlap-aware). Developing a narrowbody and a widebody program at once costs `$3B × min(1, overlap_years / 5)`, spread over the overlap and alpha-loaded.
- **Boeing Rate Increase.** A one-time commitment: +2 pp narrowbody share from two years after commitment, $1.2B capex, and +0.05 alpha on Boeing capex for six years.
- **Airbus Delay Tactics.** Covert, applies per turn. The fps slips 1 year per turn it is in development, up to 2 years total, at $0.5B per turn. After two turns of use the tactics are **exposed**: the cause becomes public and Airbus loses 1 pp of narrowbody share for five years.
- **Airbus Poaching.** Public, applies per turn. Costs Airbus $0.25B. Costs Boeing $0.75B if Boeing has a program in development. Saves Airbus $0.4B if Airbus has one.
- **Fog of war.** Boeing's brief and tools show an fps slip as "supplier bottleneck (cause not attributed)" until exposure. Boeing's estimate of Airbus's payoff leaves out costs Boeing cannot observe. Sealed orders and rationales are never shown to the other side.

`python3 -m wargame.engine rules` prints all of this, with the live parameters.

### Engine makers (optional supplier players)

Create a run with `--suppliers rolls_royce`, `--suppliers pratt_whitney` or `--suppliers rolls_royce,pratt_whitney`. Without it the game is exactly the two-player game.

- **Engine commitments.** Supplier orders apply first in each turn. An airframer may select an engine maker's new engine (`rr_ultrafan_nb`, `rr_ultrafan_wb`, `pw_gtf2`, `pw_wb_new`) only if its maker has launched that engine program by adjudication. Otherwise the airframe falls back to CFM (narrowbody) or GE (widebody), and the event is public. A committed engine is ready at launch + development years (+ slips). The airframe enters service at the later of its own date and the engine's ready year. The maker's terms add `airframer_margin_pp` to the airframe's margin.
- **Supplier payoff.** Lifecycle value of the engines it delivers, versus the status quo:
  - engines delivered = segment units × airframer share × engines per aircraft × the maker's fit on that airframe;
  - fit is its incumbent share until that airframer's new program in the segment enters service, then 1 (sole source; a Joint Venture splits it) if the program flies its engine, else 0;
  - each engine is booked at delivery at its lifecycle value, meaning OE margin plus PV of aftermarket profit. A new engine starts at `ramp.start_frac` of its value and matures over `ramp.years`.

  Minus the maker's own alpha-loaded engine capex and strain, at its own WACC.
- **What each stands to lose.**
  - Rolls-Royce's status quo is the A350 and A330neo (sole source) and a Trent 1000 share of the 787. An A350 Re-engine on another engine takes the Airbus widebody franchise away.
  - Pratt & Whitney's status quo is its GTF share of A320neo deliveries. An NGSA on another engine takes it away.
- **Levers.**
  - Rolls-Royce: `uf_wb`; `uf_nb` Solo or `jv_pw`; standard or aggressive terms; `t1000_upgrade`; cancel.
  - Pratt & Whitney: `gtf_next`; `pw_wb`; terms; `gtf_upgrade`; `join_rr_jv`; cancel.
  - Each one-time upgrade adds fit on the incumbent airframe and saves installed-base cost.
- **The Joint Venture.** When both play, RR's `uf_nb` as `jv_pw` launches only if P&W sets `join_rr_jv` in the same turn. Each then pays half the capex and earns half the value. When P&W does not play, the Joint Venture is with an outside partner and always launches.
- **Tools.**
  - `options --side <supplier>` ranks the maker's options against airframer engine-selection scenarios, and shows each airframer's incentive to choose its engine.
  - The scorecard scores suppliers on capture, myopic regret, prediction of airframer engine choices and calibration.
  - Plan-game equilibria and hindsight regret cover the airframers, with supplier orders held as played.
- **Injects.** Four injects apply only when their maker plays: an RR durability crisis, an UltraFan test setback, a GTF durability crisis and a next-generation GTF test setback.

### Game-theory tools

- `options`: this turn's stage game. Both sides' candidate orders are evaluated against each other, assuming nobody moves afterwards. It shows best responses, pure and near-Nash cells, worst and best cases.
- `equilibria`: the plan game over the remaining turns (or `--from-turn 1` in hindsight). The output gives:
  - pure Nash and ε-Nash plans (ε = $1.0B);
  - dominant and maximin plans;
  - for a finished game, each side's **regret**: its best plan against what the opponent actually did, minus what it actually got.

  `--segment wb` gives the widebody sub-game on its own. It takes about 15 s for the full game.

## Where the numbers come from

The engine borrows its widebody economics and structural rules from the Boeing/Airbus game-theory dashboard (`combined_dash.py`) landmarks. It is **not** a port of that dashboard, and its payoffs will not match it cell for cell. Everything is in `config/default.json`, and scenario files override it.

| Parameter | Value | Source |
|---|---|---|
| Margins: 737 8%, fps 25.64%, 787 Do Nothing 20% / Re-engine alone 25.21% / both 15.77%, A320 13.14%, NGSA 26.28%, A350 Do Nothing 4.95% / alone 10.76% / both 6.47% | | CALIBRATED |
| Widebody: $180M net, 170 units/yr, status quo 58.8% / 41.2%, caps 787 85% / A350 60%, capture 1.0 pp/yr | | CALIBRATED (capture = slide convention) |
| WACC Boeing 10.5%, Airbus 8.0%; alpha 0.30; ε $1.0B | | CALIBRATED |
| Strain $3B full overlap, NB 7 / WB 5 development years, overlap / 5 | | CALIBRATED (overlap-aware model) |
| Capture from EIS+1, freeze at follower EIS | | CALIBRATED (rule) |
| Narrowbody: 2,000 units/yr, $55M net, status quo 40% / 60%, capture 1.5 pp/yr, caps 80% | | PLACEHOLDER (volume from `gameboard.py`) |
| Capex: fps $30B, NGSA $25B, each Re-engine $4.2B | | PLACEHOLDER (Re-engine sized to the ≈$11B loaded two-ticket landmark) |
| Tech-ready year 2035, early-entry penalties, Joint Venture terms, engine options, 10% extension capex | | PLACEHOLDER |
| Rate Increase, Delay Tactics, Poaching effects, inject deck, 2026-2060 horizon | | PLACEHOLDER |

**Engine makers** (`suppliers.*`; derivations with evidence ids in `profiles/<company>/calibration.md`):

| Parameter | Rolls-Royce | Pratt & Whitney | Source |
|---|---|---|---|
| WACC / alpha | 10% / 0.6 (alpha reproduces RR's 15% hurdle) | 8.5% / 0.35 | CALIBRATED |
| Incumbent fit | Airbus widebody 1.0 (A350, A330neo sole source); Boeing widebody 0.22 (Trent 1000 share of 787) | Airbus narrowbody 0.40 (GTF share of A320neo) | CALIBRATED |
| Lifecycle value per incumbent engine | $7.4M (widebody, incl. spares) | $0.6M (GTF, after OE losses and durability costs) | CALIBRATED |
| New engines: capex / development years / mature value per engine | UltraFan widebody $3.1B / 6 / $8.0M; UltraFan narrowbody $7.5B / 7 / $3.1M | next GTF $4.5B / 6 / $1.05M; widebody engine $6.0B / 7 / $2.9M | CALIBRATED (UltraFan narrowbody industrialisation ±$2B) |
| New-engine ramp (value at EIS → mature after) | 45% → 6 years | -35% → 10 years (GTF-like early losses) | CALIBRATED |
| Aggressive terms (airframer margin / value kept) | +1.2pp / 0.86 | +1.1pp / 0.71 | CALIBRATED |
| One-time upgrade | Trent 1000: +10pp of 787 deliveries, $0.8B over 3 years, saves $0.13B a year for 15 years | GTF durability: +5pp of A320neo deliveries, $1.0B over 3 years, saves $0.45B a year for 9 years | CALIBRATED |
| Joint Venture split; strain | 50/50; $1.5B full overlap over 5 years | same | Joint Venture CALIBRATED (P&W precedent); strain PLACEHOLDER |

The game's aircraft volumes are stylised: 170 widebodies and 2,000 narrowbodies a year. The engine makers' absolute payoffs are therefore off-scale:
- RR's widebody engine flow is about 55-85% of the real one;
- P&W's A320neo flow is about 2x the real one.

Per-engine values were not distorted to compensate, so the incentives are realistic even where the totals are not.

**Landmark check** (`tests/test_engine.py::test_widebody_chicken_landmark`): at the base parameters the widebody sub-game is **Chicken**, as on the calibrated board.
- Both lone Re-engine cells are pure Nash.
- Both Re-engining is not an equilibrium.
- Neither Re-engining is not an equilibrium.

**Differences from the dashboard:**
- Payoffs use one 2026-2060 horizon, not per-program EIS..EIS+19 windows.
- Alpha is per player, with no raise-window doctrine beyond the Rate Increase bump.
- Narrowbody `margin_alone` = `margin_both`.

Treat results as a way to see how incentives interact, not as forecasts. To calibrate further, edit `config/default.json` or add a scenario file with `overrides`.

## History backtests

`scenarios/hist-2010-neo.json` replays 2010-2015: Airbus launches the A320neo, and Boeing chooses between re-engining the 737, a clean sheet, or waiting.
- **Players.** It is played by `boeing-2010` and `airbus-2010`. They use **period-locked profiles** (`profiles/boeing_2010/`, `profiles/airbus_2010/`) built only from evidence dated before 1 Dec 2010, with hindsight annotations scrubbed.
- **Isolation.** The hook blocks these players from today's profiles, the raw sources and the scenario files, which hold the real outcome in a `referee_only` field.
- **Results.** They are in `wargame/backtests/hist2010-neo/`: the referee's report, the scorecard, and the full game record.

Headline: 8 of 10 historical checkpoints match, 1 is partial and 1 misses (Boeing's engine choice, traced to the scenario's engine table). Read the report's validity caveats before relying on the matches.

## Customising

- **Scenarios:** add `scenarios/<name>.json` with `title`, `narrative` and `overrides`. Overrides are deep-merged over `config/default.json`.
- **Demand timing:** `segments.<seg>.capture_weight_by_year` (year → weight, piecewise linear, held flat at the ends) scales how fast a leading new product captures share each year. The default is 1.0 every year.
  - The `replacement-wave` scenario sets it from a curve of 737 MAX and A320neo-family replacements by year: about 40 aircraft in 2037, 330 in 2040 and 800 a year from 2044.
  - The weight is 0.4 + 0.6 × min(1, replacements / 807): 0.4 before 2037 and 1.0 from 2044. The 0.4 floor is an assumption: a new airplane still wins growth orders and older-generation replacements before the wave.
  - The wave never speeds capture beyond the calibrated rate. When both sides enter service in the same year, shares are unchanged.
- **Injects:** add entries to `injects.deck`. Supported effect types: `units_mult`, `margin_add`, `share_shift`, `tech_ready_add`, `strain_mult`, `dev_years_add`.
- **Turns:** edit `turns` in the config. Launch years are validated against them.
- **Personas:** edit the agent files in `.claude/agents/`, or pass `doctrine` to the workflow for a one-off constraint.

## Tests

```bash
python3 -m unittest discover -s wargame/tests -v
```

The tests cover:
- status quo = 0;
- exact waterfalls;
- direction checks: margin, capex, strain, market, rate, Joint Venture, cancellation, Delay Tactics, Poaching;
- the overlap-strain formula;
- share capture and freeze;
- the widebody Chicken landmark;
- order validation;
- fog of war (no Delay Tactics leak before exposure);
- the full command-line turn cycle, including invalid orders, rollback and digest integrity.
