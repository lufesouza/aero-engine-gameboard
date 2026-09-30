# Boeing vs Airbus war game

A multi-turn strategy war game. Claude agents play **Boeing** and **Airbus**, a **market** cell reacts, and a neutral **control** cell runs the turns. A deterministic Python engine adjudicates every move, so no payoff is ever an agent's guess. After the last turn an **analyst** reviews the game against its game-theoretic benchmark. Every claim in that review is checked by three independent agents before it reaches the report.

```
                 ┌──────────── each turn (sealed, simultaneous) ────────────┐
 control ──inject──► boeing-strategist ─┐                                    │
   (White)          airbus-strategist ──┼─► wargame-market ──► control runs  │
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
| `scenario` | `base` | `base`, `fps-slip`, `supply-crunch` (see `scenarios/`) |
| `injects` | `umpire` | `umpire` (control picks shocks), `auto` (deterministic from `seed`), `none` |
| `games` | 1 | 1-4 independent plays in parallel, plus a cross-game synthesis |
| `seed` | 0 | seed for `auto` injects (game *i* uses `seed + i - 1`) |
| `run_id` | `wg-<timestamp>` | run name (`-g<i>` appended when `games` > 1) |
| `doctrine` | none | board guidance per side, e.g. `{"boeing": "balance sheet cannot fund two programs at once"}` |
| `fixed_orders` | none | script one side, e.g. `{"boeing": {"1": {"launch": [{"program": "fps", "engine": "cfm_ducted", "variant": "jv"}]}}}` |
| `verify` | true | run the three-checker verification of the after-action review claims |

Output: `wargame/runs/<run_id>/report.md`, plus `state.json` and `turns/T<k>.json`. A 4-turn game spawns roughly 45 agents, most of them in the verification stage. `verify: false` makes it cheaper.

**2. Play a side yourself.** Type `/wargame` (or say *"I want to play Boeing in the war game"*). Claude acts as control. You get Boeing's brief each turn and give orders in plain language. The `airbus-strategist` agent plays Airbus without seeing your orders.

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
| `boeing-strategist` | Blue: fps (Solo / Joint Venture), 787 Re-engine, 737 Rate Increase, cancellations, engine choice | public view + Boeing's own numbers |
| `airbus-strategist` | Red: NGSA, A350 Re-engine, Delay Tactics (covert), Poaching, cancellations, engine choice | public view + Airbus's own numbers |
| `wargame-market` | Green: airlines, lessors, engine OEMs (CFM/GE, PW, RR) set bounded capture multipliers | public view only |
| `wargame-control` | White: creates runs, applies injects, runs adjudication verbatim | everything; never computes payoffs |
| `wargame-analyst` | after-action review and report | everything |

The orchestration is `.claude/workflows/boeing-airbus-wargame.js`. The interactive mode is `.claude/skills/wargame/SKILL.md`.

## How a turn works

1. **Control** applies at most one inject from the deck (demand shock, engine maturity slip, supply crunch, FAA scrutiny, fuel spike, quality escape, trade dispute, or a quiet turn). It then writes a public situation report.
2. **Boeing and Airbus** order in parallel and cannot see each other. Each runs `brief`, `options` (this turn's stage game), `whatif` counterfactuals and `validate` before returning sealed orders, a public statement and a private rationale.
3. **Market** sees only the public half of both sides' orders and sets capture multipliers (0.75-1.25) for launched programs.
4. **Control** runs `adjudicate` with the exact JSON the workflow built. The workflow stamps each side's orders with an FNV-1a fingerprint. The engine refuses to adjudicate if the orders arrive changed, so an agent retyping JSON cannot corrupt a game. Rejected orders go back to the player with the engine's errors, once.

## Rules of the engine

Money is $B in constant 2026 dollars. A side's score is **delta PV**: the present value, at its WACC, of its operating profit minus the status-quo profit (nobody moves, same injects), less alpha-loaded capex, alpha-loaded strain and tactic costs. The components (NB operating, WB operating, capex, strain, tactics) always sum exactly to the total.

- **Programs.** Each side has one new narrowbody (fps, NGSA) and one widebody Re-engine (787, A350).
  - Each can be launched once, in any year of a turn. EIS = launch + development years (+ engine `eis_add`, injects and slips).
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

**Landmark check** (`tests/test_engine.py::test_widebody_chicken_landmark`): at the base parameters the widebody sub-game is **Chicken**, as on the calibrated board.
- Both lone Re-engine cells are pure Nash.
- Both Re-engining is not an equilibrium.
- Neither Re-engining is not an equilibrium.

**Differences from the dashboard:**
- Payoffs use one 2026-2060 horizon, not per-program EIS..EIS+19 windows.
- Alpha is per player, with no raise-window doctrine beyond the Rate Increase bump.
- Narrowbody `margin_alone` = `margin_both`.

Treat results as a way to see how incentives interact, not as forecasts. To calibrate further, edit `config/default.json` or add a scenario file with `overrides`.

## Customising

- **Scenarios:** add `scenarios/<name>.json` with `title`, `narrative` and `overrides`. Overrides are deep-merged over `config/default.json`.
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
