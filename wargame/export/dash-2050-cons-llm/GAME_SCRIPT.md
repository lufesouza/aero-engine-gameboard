# Boeing vs Airbus, 2030-2050: the war game "dash-2050-cons", scripted for any LLM

This is the full script for replaying, with another LLM, the five-player war game played as run `dash-2050-cons`:
Boeing and Airbus (airframers) and the engine makers CFM/GE, Pratt & Whitney and Rolls-Royce, over four decision rounds
(2030, 2035, 2045, 2050). In the original, each company was four AI agents (the CEO, the CFO, the operating head and
the Board of Directors), each built from the real executives' and directors' public record and run as a separate
agent; a game master ran every round on an economic engine (the narrowbody/widebody game-theory dashboard with a
supply-and-demand layer). This pack carries all of it: the engine and the starting position (`engine/`), an automated
runner that plays every seat through any LLM's API (`engine/run_game.py`), the twenty agent definitions
(`personas_full/`), each company's kit and source files (`kits/`, `companies/`), and this script.

**Spoilers.** `RESULTS_AS_PLAYED.md` and `engine/reference/` hold what the original players did. They are in the full
pack only (`dash-2050-cons-llm.zip`); the players' pack (`dash-2050-cons-llm-players.zip`) leaves them out. Give a
playing LLM the players' pack, and open the results only after the replay.

## Contents

1. Choose how to play
2. Set-up 1: the automated runner
3. Set-ups 2-4: playing in chat apps (the operator and the game master)
4. The game in one page
5. The public rules (every player's text, verbatim)
6. Orders, defaults, Board items and validation
7. The round protocol: what every seat receives, the exact task of each step, missing steps, output formats
8. The five companies' executive committees, and what every seat is told
9. Known inconsistencies in the original material (game master only)
10. Where everything is

---

# 1. Choose how to play

| Set-up | What it needs | Fidelity to the original |
|---|---|---|
| **1. Automated runner** (recommended) | Python 3.9+ with numpy and pandas, and an API key for any OpenAI-compatible endpoint (OpenAI, Google Gemini, Anthropic, Mistral, a local model) | Closest: every seat-step is a fresh call with only what that seat received in the original; formats checked; Board items, reverts and missing steps handled in code, as in the original |
| **2. Six chats + an operator** | A chat app with code execution for the game master (GM), five more chats (one per company), and a person to carry text between them | Good, if the operator runs each test (step 2) and veto check (step 4) in a fresh chat; otherwise the four seats of a company share one context |
| **3. One chat** | A chat with code execution and a very large context | Weakest: one context holds every company's deliberation, so sealed orders are not really sealed; use only to explore |
| **4. No code execution** | This script, the kits and the five round-1 briefs | Round 1 only is exact (its starting position is fixed); later rounds need the engine |

Before any set-up, the operator runs the engine's self-test from the full pack, once, outside any playing chat:
`python3 engine/play.py selftest` (from the pack's top folder). It prints only PASS or FAIL per round.

---

# 2. Set-up 1: the automated runner

From the pack's top folder (the players' pack is enough):

```
export LLM_API_KEY=...                       # the key for your endpoint
python3 engine/run_game.py --game mygame --base-url https://api.openai.com/v1 --model <model>
```

Other endpoints, for example: Google Gemini `--base-url https://generativelanguage.googleapis.com/v1beta/openai`;
Anthropic `--base-url https://api.anthropic.com/v1`; a local Ollama `--base-url http://localhost:11434/v1`; Azure
OpenAI `--auth-header api-key --auth-prefix ''` with your deployment's URL. Options: `--seat-model board=<model>` (a
different model per seat), `--temperature`, `--max-tokens` (`--max-tokens-field max_completion_tokens` for newer
OpenAI models), `--no-tools` (APIs without function calling), `--history full` (every earlier note in each prompt),
`--persona card` (the condensed persona cards instead of the full definitions), `--rounds 1` (one round at a time),
`--companies boeing,airbus` (the others hold). `python3 engine/run_game.py --help` lists them all.

What it does, round by round: writes the briefs; plays the nine steps for the five companies in parallel (each
seat-step one call: the seat's agent definition as the system prompt; the preamble and task of section 7 and 8; the
company's rules, brief and earlier decisions; tools to read its own company's files and earlier notes and to do exact
arithmetic, as the original agents could); applies the merge, revert and missing-step rules; adjudicates; prints the
public events and every value. A stopped run resumes where it stopped. Every call is logged in
`engine/runs/<game>/calls/`, every step's output in `engine/runs/<game>/players/<company>/exco/`.

Size: about 45-55 calls a round (11 per company at most), each with 15-40k tokens of input; a full game is roughly
5-10 million input tokens. Checks without an LLM: `--provider replay` feeds back the original agents' own answers and
must reproduce the original game exactly (full pack only); `--provider mock` makes every seat hold.

---

# 3. Set-ups 2-4: playing in chat apps

## 3.1 Roles

- **The operator** is a person. A chat cannot send messages to another chat, so the operator carries text: briefs
  from the GM chat to the company chats, and each company's final orders block back. The operator also keeps the
  files (the saved game, each company's notes) and runs the self-test.
- **The game master (GM)** is the chat that runs the engine (it needs code execution). It is neutral, never advises a
  company, never shows one company another's private material, and never adds anything to a bulletin.
- **A company** is a chat (or, for the most faithful play, one chat per seat-step) that plays the company's four
  seats by the protocol in section 7, from its kit `kits/COMPANY_<company>.md`.

## 3.2 Set-up 2, step by step

1. **GM chat.** Upload the players' pack and say: *"Unzip this. You are the game master of the war game in
   GAME_SCRIPT.md; read sections 3, 4, 6 and 7. Run `python3 engine/play.py new mygame`, then
   `python3 engine/play.py brief mygame 1`, and give me each company's `engine/runs/mygame/players/<company>/round1.md`
   as a file to download."* After every adjudication, ask the GM to run `python3 engine/play.py save mygame` and give
   you `mygame.zip`: chat sandboxes are reset after a while, and `python3 engine/play.py load mygame.zip` restores the
   game.
2. **Company chats.** In each of five chats, paste (or upload, and confirm it was read in full) the company's kit,
   and upload its folder `companies/<company>/` if the app takes files. Then send: *"Round 1 (year 2030). Your brief
   follows. Run steps 0 to 8 by your kit and end with your orders block."* and the whole of its `round1.md`. Let the
   chat give one step per reply if it needs to (say "continue"). Tell it to use code or a calculator for every sum.
3. For the most faithful play, run each **step-2 test and step-4 veto check in a fresh chat** that gets the seat's
   persona (from the kit), the brief, the rules, the company's earlier notes and only that step's inputs (section 7),
   and paste its output back into the company chat.
4. **Back to the GM.** Paste the five orders blocks (or upload them as files). Ask the GM to run
   `python3 engine/play.py check mygame 1 <files>`, then `python3 engine/play.py adjudicate mygame 1 <files>`, then
   `python3 engine/play.py brief mygame 2`. A company with no block holds everything. If an orders block was wrong,
   `python3 engine/play.py undo mygame 1` takes the round back.
5. Carry each company's round-2 brief to its chat (it also says if any of its orders were adjusted), and repeat to
   round 4. Then ask the GM for `python3 engine/play.py status mygame` (values, yields and Control's objectives) and
   `python3 engine/play.py reveal mygame` (covert Delay Tactics), and open `RESULTS_AS_PLAYED.md`.

The GM chat never sees a company's deliberation, so each company chat applies the protocol's own rules (Board items,
the step-7 merge, reverts and missing steps) and outputs only its final orders. The GM applies only the engine's
rules and "no block = hold". The orders template (`play.py orders-template`) is for the GM only: its legal values can
reveal a covert order.

## 3.3 Set-up 3: one chat

Upload the players' pack to one chat with code execution. The chat is the GM and plays every seat. Play one company
at a time, one seat at a time; before each step, restate the seat and what it receives (section 7) and use nothing
else; play each seat from its full definition in its kit. Because one context holds everything, rivals' sealed orders
and private briefs are in view: this set-up cannot reproduce the original's isolation. For a better result, start a
fresh chat for each company-round with this script's sections 5-8, the company's kit, its brief and its earlier notes.

## 3.4 Set-up 4: no code execution

Give the chat (or six chats) this script, the kits and the five round-1 briefs
(`engine/reference/briefs/round1_<company>.md`, from the full pack; the starting position is fixed, so they are the
briefs of any replay). Play round 1 by section 7. The operator, not the chat, then compares the replay's orders with
the original's (`RESULTS_AS_PLAYED.md`, the orders table): if every company's orders change the game in the same way
as the original's (the same launches, cancellations, commitments, supply-plan changes and engine codes), the original
round-2 briefs apply, once the operator replaces their "Public statements (last round)" and "Other moves made public"
sections with the replay's own. Otherwise the replay needs the engine: continue in set-up 2 or 1.

---

# 4. The game in one page

- **Players:** Boeing, Airbus, CFM/GE (CFM International with GE's widebody engines), Pratt & Whitney (RTX), Rolls-Royce.
- **Rounds:** 2030, 2035, 2045, 2050. Sealed, simultaneous orders; a public bulletin after each round.
- **The choices:** Boeing's new narrowbody (fps: 7-year or 10-year ramp, or via Embraer; at new sites or at Renton),
  the 737 Rate Increase (2030 only), the 787 Re-engine; Airbus's NGSA (with its A320 base or Alt production plan), the
  A350 Re-engine, covert Delay Tactics; the engine makers' new engines (CFM Ducted and Open Fan, P&W GTF2, Rolls-Royce
  UltraFan narrowbody and widebody, the P&W-Rolls-Royce Joint Venture), upgrades and partnerships; the engine
  selections on the new narrowbodies; cancellations.
- **This game's settings** (built into the engine and the briefs):
  - board: the combined narrowbody/widebody dashboard, version 3 (fps 7-year $65.00B and 10-year $60.32B at EIS,
    NGSA $35.52B, unlaunched Re-engines at 2042, the EIS-lead share rule);
  - supply and demand on: the narrowbody market is limited by the factories; demand is a conservative case with the
    firm orders as its first slice; Boeing loses 1 point of preference a year from NGSA's entry into service while it
    has no new narrowbody in service, but never below the share Airbus cannot supply; Airbus adds 1% capacity a year
    when it is short;
  - Control's objectives (set "control2"): Boeing must repair its balance sheet and secure a stable engine supply;
    Airbus wants a stable engine supply; Rolls-Royce must protect its widebody cash cow. Each company's brief
    (section 2) measures them; they never change the payoff.
- **Payoffs:** ΔPV against the status quo, $B, discounted to 2026 at each company's cost of capital; each company sees
  its own grid of plans against rival scenarios in its brief.
- **Scoring at the end:** each company's ΔPV and yield, and Control's objectives met or not (`play.py status`);
  then the comparison with the original.

---

# 5. The public rules (verbatim)

## dash-2050: rules of the game (public; every player has the same text)

**Game master.** The game master (GM) runs the game on the narrowbody/widebody game-theory dashboard. Only the GM sees
the whole board. You see the public record and your own position. You never see another player's payoffs, finances,
orders or reasoning.

**Players.** Boeing and Airbus (airframers); CFM/GE, Pratt & Whitney (P&W) and Rolls-Royce (RR) (engine makers).

**Rounds.** Four decision years: 2030, 2035, 2045, 2050. In each round all five players submit sealed orders at the
same time. The GM adjudicates them and publishes a bulletin before the next round.

**Markets.**
- Narrowbody (NB): 2,000 aircraft a year. Status quo: Boeing 40%, Airbus 60%.
- Widebody (WB): 170 aircraft a year. Status quo: Boeing 787 58.8% (100/170), Airbus A350 41.2%.
- NB engines (two per aircraft): status quo CFM 76%, P&W 24%, RR 0%.
- WB engines: status quo CFM/GE (GEnx) 42%, RR (Trent) 58%.
- **Supply and demand is on in this game:** the narrowbody market is limited by what the factories can build; see the
  last section.

### Moves and timing

| Player | Move (the briefing's wording) | Order field and value | Timing |
|---|---|---|---|
| Boeing | Launch fps with 7-year ramp-up | `fps`: `launch_7yr` | enters service (EIS) 7 years after launch |
| Boeing | Launch fps with 10-year ramp-up | `fps`: `launch_10yr` | EIS 10 years after launch |
| Boeing | Launch fps via Embraer | `fps`: `launch_via_embraer` | EIS 10 years after launch |
| Boeing | Increase 737 production rate by 2030 | `rate_737`: `increase` (2030 round only) | rate up in 2032 |
| Boeing | 787 Re-engine (widebody) | `re787`: `launch` | EIS 5 years after launch |
| Boeing | Do Nothing (737 MAX, 787) | `hold` | |
| Airbus | Launch NGSA | `ngsa`: `launch` | EIS 7 years after launch |
| Airbus | A350 Re-engine (widebody) | `rea350`: `launch` | EIS 5 years after launch |
| Airbus | Delay fps (supply-chain bottleneck), Delay fps (talent poaching) | `delay_tactics` | covert; see below |
| Airbus | Do Nothing (A320neo, A350) | `hold` | |
| CFM/GE | Ducted only / Open Fan only / Open + Ducted | `ducted`, `open_fan`: `launch` | ducted ready 6 years after launch; Open Fan ready 10 years after launch and not before 2045 |
| CFM/GE | Partner with Embraer | `partner_embraer`: `launch` (needs a new CFM engine) | counts 7 years after launch |
| CFM/GE | Lobby governments on emissions | `lobby_emissions`: `launch` | immediate |
| CFM/GE | GEnx upgrade or GEnx investment (widebody) | `genx`: `upgrade_genx9` or `invest_genx` | counts 3 years after launch |
| P&W | Launch GTF2 Solo | `gtf2_solo`: `launch` or `launch_if_selected` | ready 6 years after launch |
| P&W | Joint Venture with Rolls-Royce | `jv_with_rr`: `commit` | see Joint Venture |
| P&W | Do Nothing (continue GTF1) | `hold` | |
| RR | UltraFan narrowbody Solo | `ultrafan_nb_solo`: `launch` or `launch_if_selected` | ready 7 years after launch |
| RR | Joint Venture with P&W | `jv_with_pw`: `commit` | see Joint Venture |
| RR | UltraFan widebody | `ultrafan_wb`: `launch` | ready 6 years after launch; counts only once a re-engined 787 or A350 is in service |
| RR | Trent 1000 upgrade (widebody) | `t1000_upgrade`: `launch` (exclusive with UltraFan WB) | counts 3 years after launch |
| RR | Do Nothing (continue Trent only) | `hold` | |

**Other moves.** You may also propose moves your company has historically made that are not on this list (for example
a pricing campaign, an alliance or a derivative aircraft). Put them in `other_moves` and say whether each is public.
The board does not price them. The GM records them, publishes the public ones, and reports them qualitatively; they
do not change any payoff.

**Launch once, cancel before service.** A launched programme can be cancelled in a later round, until it enters
service (airframes) or is ready (engines). A cancelled programme writes off its spend to date: the bill × years
elapsed ÷ development years, booked in the cancel year. A cancelled programme can be relaunched later as a new one.

### Engines on the new narrowbodies

- When Boeing launches fps or Airbus launches NGSA, it selects an engine code. Until the airframe enters service it
  may change the code in any round. The codes are 1 RR, 2 P&W, 3 CFM, 4 RR & P&W Joint Venture, 5 RR and CFM,
  6 P&W and CFM, 7 all three.
- A code is a request. A maker is fitted only if it has a new NB engine ready by the airframe's EIS: for P&W, GTF2 or
  the Joint Venture engine; for RR, UltraFan NB or the Joint Venture engine. CFM is always available (a LEAP
  derivative if it builds nothing new). A maker that is not ready is dropped. If no one is left, the airframe gets CFM.
- Code 4 needs a formed Joint Venture engine ready by EIS.
- Some code pairs are not allowed together: (1,1), (1,4), (2,2), (2,4), (3,3), (4,1), (4,2), (4,4), (5,5), (6,6),
  listed as (fps, NGSA). If both airframers choose such a pair, the later airframe moves to code 7.
- `launch_if_selected` (P&W GTF2, RR UltraFan NB): the engine launches this round only if a live airframe that is
  not yet in service has selected you this round, and your engine would be ready by its EIS. Otherwise nothing
  happens and nothing is spent.
- **Joint Venture.** P&W (`jv_with_rr: commit`) and RR (`jv_with_pw: commit`) each make a public, standing
  commitment. The Joint Venture forms in the first round in which both are committed. Its engine is ready 6 years
  later, or earlier if a partner folds in a solo programme that is further along. A solo programme folds into the
  Joint Venture when it forms; what the maker has spent on it beyond its Joint Venture share is written off in the
  fold year. A commitment can be withdrawn before the Joint Venture forms.
- Before a new airframe enters service, the 737 flies CFM (LEAP-1B) and the A320neo flies P&W and CFM.

### How the board sets market shares

**Narrowbody airframes.**
- Nothing changes until a new airframe enters service.
- **NGSA in service and no fps in service (none launched, or not yet in service):** Boeing loses 1 pp a year
  from 40%, from NGSA EIS (this game's rule; it replaces the board's +3 pp a year for Airbus). Once an fps
  enters service, the rules below apply.
- **Only fps launched:** Boeing gains 1.0 pp a year from fps EIS (cap 80%).
- **Both launched, different EIS years:** the first one to enter service gains 1.0 pp a year while it
  is alone (cap 80%). From the second EIS, shares move toward a long-run split at 1.0 pp a year
  (Boeing gaining) or 1.0 pp a year (Airbus gaining). The long-run split is 50/50 (Boeing/Airbus)
  shifted toward the first one by 1.0 pp for each year of lead (leader cap 80%), and the leader keeps
  that edge for good. Example: NGSA 2037 and fps 2041 give a long-run split of 46/54.
- **Both launched, same EIS year:** Boeing climbs from 40% toward 50% at 1.0 pp a year; no lead edge.
- The three fps moves (7-year, 10-year, via Embraer) follow the same rule: only the two EIS years matter.
- **737 rate increase:** Boeing gets +5 pp in 2032-36, or every year if neither new airframe is ever launched.
- **Delay Tactics:** Boeing loses 5 pp for 5 years from fps EIS.

**Widebody airframes.**
- A lone re-engined 787 gains 1.0 pp a year from its EIS (cap 85%).
- A lone re-engined A350 gains 1.5 pp a year (cap 60%).
- If both re-engine, the first one's gains stop when the second enters service. If both enter service in the same
  year, nothing changes.

**Engines.**
- Nothing changes until the first new narrowbody enters service; on the widebody, until the first re-engine (or 2042).
- From then on, each airframer's share of the NB market is split equally among the makers fitted to its airframe (the
  737 and A320neo slots as above). The engine moves then shift share:

| Engine move | Effect on engine share |
|---|---|
| CFM ducted | CFM +10 pp NB, taken from P&W (or half each from P&W and RR, if RR has an NB engine) |
| CFM Open Fan | Airframers will not wait for it. If the first new narrowbody enters service before Open Fan is ready, CFM loses 35 pp of NB share to the others (20 pp if CFM lobbies on emissions) |
| Partner Embraer | CFM +5 pp NB |
| GEnx upgrade or investment | CFM +5 pp WB |
| GTF2 Solo | P&W +10 pp NB (5 pp each from CFM and RR) |
| Joint Venture | P&W +5 pp and RR +5 pp NB, CFM −10 pp; P&W and RR then hold equal NB shares |
| UltraFan NB Solo | RR +15 pp NB (CFM −10 pp, P&W −5 pp) |
| UltraFan WB | RR +10 pp WB from CFM |
| Trent 1000 upgrade | RR +5 pp WB from CFM |

Shares are floored at zero and re-normalised to 100%.

**Payoffs.**
- Each player's score is the change in its present value (PV, $B at 2026) against the status quo, and its yield:
  100 + ΔPV ÷ enterprise value × 100.
- Airframers: operating profit on NB and WB aircraft, less programme investment (booked at EIS), a debt penalty,
  two-front strain, rate-increase cost, Delay Tactics spend and fines.
- Engine makers: lifetime value of engines delivered (engine price × a 1.6 lifecycle multiplier, with 2.2% a year
  price inflation), less R&D, strain and write-offs.
- Your own numbers are in your private brief.

### What is public

**Public:**
- launches, cancellations, entry-into-service and engine-ready dates;
- engine selections and the engines actually fitted;
- Joint Venture commitments;
- each player's `public_statement`, and any `other_moves` marked public;
- observed market shares and deliveries, year by year, up to the decision year.

**Private:** everything else: your payoffs, finances, orders not yet public, your rationale and your predictions.

**Delay Tactics** are covert: never published, and revealed only when the game ends.
- Each move (supply-chain bottleneck, talent poaching) costs $1B, spent over the years before fps EIS.
- One or both moves give the same 5 pp effect, from fps EIS.
- If Boeing never launches fps, the tactics are "naked" and draw a $48.32B fine.
- They can be ordered in any round before fps enters service.

### Supply and demand

The board's shares are what customers **want**. Aircraft are delivered only if a factory can build them.

**Demand = replacement + growth** (this game's demand curve: a conservative case for the whole single-aisle market, on
the 737/A320 class here, 94.8% of it; aircraft a year).
- **Replacement of old-generation aircraft** (737NG, A320ceo): 697 in 2030, 778 in 2035, 547 in 2040,
  319 in 2045, then none: that fleet is used up by 2046.
- **Replacement of today's 737 MAX, A320neo and A220 fleets:** 133 in 2035, 569 in 2045, 868 in 2051 (the peak),
  531 in 2060.
- **Replacement of aircraft delivered after 2026:** from 2049; 116 in 2055, 544 in 2060, 1,244 in 2065.
- **Growth:** 690 in 2030, 960 in 2040, 1,131 in 2045 (the peak), 1,007 in 2050, 782 in 2055, about
  472 a year from 2060.
- **Total demand:** 724 (2026), 1,406 (2030), 1,724 (2035), 1,801 (2040), 2,019 (2045), 1,914 (2046),
  1,852 (2050), 1,647 (2055), 1,548 (2060), 2,082 (2065); after 2070 it stays at the 2070 level.
- **Firm backlog:** 4,769 737 MAX and 7,330 A320neo-family aircraft on firm order (October 2026). They are **part of this demand, not
  extra to it**: each year's demand is served first from the firm orders still open, split between the makers in
  proportion to what each has left; only the rest is new customers, split by preference. The firm orders last until
  about 2035; from then all demand is new customers. Firm orders never switch maker or lapse.

**Who customers want.** Each year's new demand is split by the board's share rules above: the **preference share**. The
fps, NGSA, the 737 rate increase's +5 pp and Delay Tactics all move preference; they move deliveries only where a
factory has the slots. The share objectives in your brief are measured on preference, as in earlier games.

**Factories (public production plans, aircraft a month).**
- **Airbus (Rev. B plan):** A320 family at 85 a month until NGSA enters service. Then, on the base plan, the A320
  lines wind down (72, 52, 42, then 14 a month, and none about five years after NGSA EIS) while NGSA ramps up
  (rate 50 about four years after EIS, 80 about six, 100 about eight). On the **Alt plan** (`a320_plan: alt`) the A320
  lines are kept longer (82, 62, 52, 42, then 14 a month, about eight years in all): about 1,500 more A320s for
  about $0.75B. Without NGSA the A320 stays at 85 a month.
- **Boeing:** 737 MAX at 42.5, 49.5, 52 and 54.5 a month in 2026-2029, then 57 from 2030
  (Renton's three lines at 47 plus the Everett North Line); the 737 rate increase adds 100 aircraft a year from
  2032 while the MAX is built. The fps ramps on the same shape as NGSA (rate 50 about four years after EIS, 100
  about eight). Boeing's single-aisle total is capped at 100 a month: as the fps fills it, the MAX gives way,
  down to an Everett tail of 10 a month. On the **new-site plan** (`fps_site: new_site`, the default) the fps is
  built at new sites and the MAX carries on at Renton and Everett. On the **Renton plan** (`fps_site: renton`) Renton is
  reassigned to the fps: its MAX lines (with the rate increase that rides on them) wind down as the fps ramps up, like
  the A320 base plan, and only the Everett North Line carries on (up to 15 a month); Boeing avoids about
  $3.0B of new-site capex, in full if Renton is chosen at least three years before the fps enters service
  (pro-rated if later). After 2050 the MAX builds only what the fps cannot yet: it tops Boeing up to the fps's full
  rate while the fps ramps. Without an fps the MAX carries on.

**Deliveries each year.**
- Each maker delivers the firm orders that this year's demand calls on first, then what its new customers want plus its waiting backlog, up to its
  capacity.
- Customers its factories cannot serve: the flexible ones (49%: airlines flying both types, lessors and
  unannounced customers) take the other maker's free slots, this year or in any later year when slots open; the rest
  wait in the backlog for their first choice.
- A tenth of the waiting backlog (not the firm backlog) drops out each year (keeps old aircraft longer, defers growth
  or cancels).
- **Airbus's slack goes to Boeing:** customers Airbus cannot serve buy from Boeing. Boeing's preference share is
  never below the share of the year's new customers that Airbus cannot supply (after its firm orders and its
  waiting customers), so Boeing captures that slack, up to its own capacity.
- **Airbus adds capacity when it is short:** in every year its customers want more than it can build, Airbus raises
  its capacity by 1% (compounding, on top of its production plan, from the next year), until it can meet them.
  The status quo runs the same rules.
- New types are delivered first, up to their line's capacity; the rest are 737 MAX or A320neo, at today's price and
  margin.
- Market share in the observed tables is the share of deliveries. Profit is earned on aircraft delivered, at the
  board's prices and margins for each type.
- The status quo runs the same rules with today's plans (A320 at 85 a month, the MAX path above), the same demand and
  firm backlog, and the 40/60 preference.
- Engine makers sell engines on the aircraft actually delivered (two per aircraft). The 737 MAX keeps CFM (LEAP-1B)
  and the A320neo keeps CFM 60% / P&W 40%; the engine moves in the table above shift share only on the new types (fps
  and NGSA), starting from the makers fitted to each.

**Your supply plan** (`fps_site` for Boeing, `a320_plan` for Airbus) is public. It applies to your new airframe once
launched (you can choose it in the launch round) and can change in any round until that airframe enters service. A
field you leave out keeps your current plan. Supply-plan costs and savings are valued at your cost of capital (no debt
penalty).

---

# 6. Orders, defaults, Board items and validation

| Company | Order fields and values (the first value is the default) |
|---|---|
| Boeing | `fps`: `hold`, `launch_7yr`, `launch_10yr`, `launch_via_embraer`, `cancel`; `fps_engine_code`: `null`, `1`, `2`, `3`, `4`, `5`, `6`, `7`; `rate_737`: `hold`, `increase`; `re787`: `hold`, `launch`, `cancel`; `fps_site`: `new_site`, `renton` |
| Airbus | `ngsa`: `hold`, `launch`, `cancel`; `ngsa_engine_code`: `null`, `1`, `2`, `3`, `4`, `5`, `6`, `7`; `rea350`: `hold`, `launch`, `cancel`; `delay_tactics`: `none`, `bottleneck`, `poaching`, `both`; `a320_plan`: `base`, `alt` |
| CFM/GE | `ducted`: `hold`, `launch`, `cancel`; `open_fan`: `hold`, `launch`, `cancel`; `partner_embraer`: `hold`, `launch`, `cancel`; `lobby_emissions`: `hold`, `launch`; `genx`: `hold`, `upgrade_genx9`, `invest_genx`, `cancel` |
| Pratt & Whitney | `gtf2_solo`: `hold`, `launch`, `launch_if_selected`, `cancel`; `jv_with_rr`: `hold`, `commit`, `withdraw` |
| Rolls-Royce | `ultrafan_nb_solo`: `hold`, `launch`, `launch_if_selected`, `cancel`; `jv_with_pw`: `hold`, `commit`, `withdraw`; `ultrafan_wb`: `hold`, `launch`, `cancel`; `t1000_upgrade`: `hold`, `launch`, `cancel` |

- **Standing supply plans.** Boeing's `fps_site` and Airbus's `a320_plan` are plans, not moves. Their default is the
  company's current plan (at the start `new_site` and `base`; the brief shows it). Keeping it is not a Board item;
  changing it is, and a vetoed change reverts to the current plan.
- **Engine codes** (`fps_engine_code`, `ngsa_engine_code`) are JSON `null` or an integer 1-7. They ride with their
  launch: never a Board item on their own; when a launch reverts, its code reverts with it. The briefs print the "no
  code" option as `None`: it means JSON `null`.
- **Board items** are the order fields, other than engine codes, whose value differs from the default.
- **What the engine does with orders** (rules.py, as in the original): a field left out takes its default (a supply
  plan: the current plan); an illegal value becomes the first legal value, and the company is told so privately in its
  next brief; an fps or NGSA launch without an engine code gets code 7 (all three makers), which can trigger P&W's and
  Rolls-Royce's `launch_if_selected`; Partner Embraer without a new CFM engine (Ducted or Open Fan, on record or
  launched this round) becomes hold; UltraFan WB with the Trent 1000 upgrade sets the upgrade to hold. `play.py check`
  shows every adjustment before you adjudicate, and `play.py adjudicate` refuses unknown fields and malformed blocks.
- **Orders file shape** (one file, or one block per company in its own file):
  `{"boeing": {"orders": {"fps": "hold", "fps_engine_code": null, "rate_737": "hold", "re787": "hold", "fps_site":
  "new_site"}, "public_statement": "...", "other_moves": [{"move": "...", "public": true, "detail": "..."}]}}`

---

# 7. The round protocol

Each company plays the same nine steps; only the names, the decision rule and the veto grounds change (section 8).
Every task below is the text the original game gave the seat, with its inputs in [brackets]. Before its task, each
seat is told the preamble in section 8.

## 7.1 What every seat receives

Every seat, at every step, has: its persona; this round's brief (the public bulletin followed by its
company's private brief); the public rules; its company's own notes and sealed orders from earlier rounds; and its own
company's profile files. On top of that, from this round's deliberation it receives only:

| Step | Who | From this round's deliberation |
|---|---|---|
| 0 Guidance | Board | nothing |
| 1 Frame | CEO | the Board's guidance |
| 2 Test | CFO; operating head (separately) | the CEO's frame, the Board's guidance |
| 3 Decide | CEO | its frame, the Board's guidance, both test memos |
| 4 Veto check | CFO; operating head (separately) | its own test memo, the CEO's decision |
| 5 Revise | CEO (only if a binding veto or a red-line flag) | its decision, the binding vetoes and the flags |
| 6 Review | Board (only if Board items) | its guidance, the ExCo's package (frame, both memos, decision, veto checks, revision), the submitted orders |
| 7 Board revise | CEO (only if a Board veto) | its submitted orders, the Board's review |
| 8 Confirm | Board (only if a vetoed item was revised) | its guidance, the package, its review, the CEO's revision, the merged orders |

Nothing ever crosses between companies: a company sees another only through the public bulletin.

## 7.2 The nine steps

**Step 0. Board guidance** (the Board). Task: *Give the ExCo your guidance for this round: your priorities, your
risk appetite this round, what you expect to see in the package, what you would approve and what you would veto, and
your recommendations. It does not bind; your veto comes at the review.*

**Step 1. Frame** (the CEO). Task: *The Board's guidance for this round (non-binding; its veto
comes after your decision): [the step-0 output]. Write the framing note for your ExCo: the question this round, the
levers in play, the options worth testing, the red lines in force, what you ask of your CFO and of your operating head,
and your initial lean. Your colleagues see only what you return here.*

**Step 2. Test** (the CFO, and the operating head: separately; neither ever sees the other's memo). Task: *Your CEO's
framing note, passed by the game master: [the step-1 output]. The Board's guidance for this round: [the step-0
output]. Test it independently: you do not see your colleague's memo. Apply your own tests with thresholds and the
grid numbers you used, give your recommended orders, and state any veto with its ground and whether the team rule makes
it binding (your veto: [the seat's veto ground]). Memo of at most 250 words, in your voice.*
   - The CFO's veto ground: see section 8.
   - The operating head's veto ground: see section 8.
   - Pratt & Whitney only: the operating head's task ends *Per the team rule you also PROPOSE the engine orders: put them in `recommended_orders` and explain them in `proposal`.*

**Step 3. Decide** (the CEO). Task: *Your framing note: [step 1]. The Board's guidance for this round: [step 0].
[CFO]'s test memo: [step 2, CFO]. [Operating head]'s test memo: [step 2, operating head]. Decide by the team rule.
Return the company's sealed orders (one value per field), other moves, the public statement, the rationale, and how
you weighed each memo. Any override of a colleague's veto goes in `overrides` and must be allowed by the rule. Answer
each of the Board's recommendations in `board_response`: how you took it up, or why not. Every order that differs from
the default goes to the Board, which can veto it.* (The last two sentences only when there was Board guidance.)

**Step 4. Veto check** (the CFO and the operating head, separately). Task: *Your own test memo: [its step-2 memo]. The CEO's
decision: [step 3]. Concur, or invoke a veto only on a ground the team rule gives you: [the seat's veto ground]. Set
`veto.binding` true only if, under the rule, the CEO must revise within it (or record an allowed override).
Separately, if the orders break a company hard rule (a red line), set `red_line_breach` true and name the rule in
`red_line`: that is not a veto, but the CEO must strike the breach.*

**Step 5. Revise** (the CEO). Runs exactly when a veto check returned `concur: false` with `veto.binding: true`, or any
veto check returned `red_line_breach: true`; nobody else judges whether a veto binds. Task: *Your decision: [step 3].
Binding veto(es) from your ExCo: [name: the veto check, for each]. Company red-line breach(es) flagged by your ExCo:
[name: the red line and note, for each]. Revise your orders once. Stay within each binding veto, or override only
where the team rule allows it and record each override in `overrides`. Strike every flagged red-line breach you confirm
(red lines are never traded for PV); if you judge a flag mistaken, keep the order and say why in `rationale`.* The
revision replaces the decision, as returned.

**Step 6. Board review** (the Board). Runs only when there are Board items: the order fields, other than engine codes,
whose value differs from the default (section 6). With none, the review is an automatic approval ("No Board items:
every order is the default"). Task: *Your guidance this round: [step 0]. The ExCo's package, passed by the game master:
[the framing note, both test memos, the decision, both veto checks and the revision, if any]. The orders it submits:
[the orders]. The Board items: [fields]. For each, approve or veto, with the ground and evidence; for a veto you may
name acceptable alternatives (other values of that order field, or the default). Then your recommendations.*

**Step 7. Board revise** (the CEO). Runs only when the Board vetoed an item. Task: *Your orders as submitted: [the
decision or revision, with its orders]. The Board's review: [step 6]. The Board vetoed: [fields]. Revise once, within
the Board's veto: for each vetoed order choose an alternative the Board named, or the default. Keep the approved
orders. Answer the Board's recommendations in `board_response`.* Then the **merge** (done mechanically by whoever runs
the protocol): keep every approved order as submitted; take only the vetoed fields, with their engine code, from the
revision.

**Step 8. Board confirm** (the Board). Runs only when a vetoed field was revised to a value other than its default.
Task: *Your guidance this round: [step 0]. The ExCo's package: [as in step 6]. Your review: [step 6]. The CEO's
revision after your veto: [step 7]. The orders now, after the revision: [the merged orders]. The revised Board items:
[field = value, ...]. Approve or veto each (an alternative you named should pass unless something changed). A
still-vetoed item reverts to the default.* A field still vetoed reverts to its default, with its engine code.

**Result.** The company's sealed orders are the orders after these steps; its `public_statement` and `other_moves`
(and the rest of its decision) come from the CEO's latest output: step 7, else step 5, else step 3.

## 7.3 Missing steps

If a step's output is missing (no reply, or a reply that still does not match its format after two
requests to correct it), the original game's rules apply:

| Missing | What happens |
|---|---|
| Step 0, Board guidance | The CEO frames without it (and the decision need not answer the Board) |
| Step 1, the frame, or step 3, the decision | The company holds everything this round (all defaults) |
| A step-2 test memo | The CEO decides without it; that seat's veto check sees no memo of its own |
| A step-4 veto check | Read as concur: no veto, no red-line flag |
| Step 5, the revision | The decision stands |
| Step 6, the Board review | Every Board item reverts to its default (fail closed) |
| Step 7, the Board revise | The vetoed items revert to their defaults |
| Step 8, the Board confirm | The revised items revert to their defaults |

## 7.4 Output formats

The same for every company; `orders` and `recommended_orders` hold the company's own order fields (section 6), one
value each. `evidence_ids` list the evidence ids the seat relies on (the ids its persona or company files cite); they
may be empty.

**Board guidance (step 0)**

```
{
  priorities: [ text , … ]
  risk_appetite: text
  expect_to_see: text
  would_approve: [ text , … ]
  would_veto: [ text , … ]
  recommendations: [
    {
      text: text
      evidence_ids (optional): [ text , … ]
    }
    , …
  ]
  evidence_ids: [ text , … ]
}
```

**CEO framing note (step 1)**

```
{
  question: text
  situation: text
  levers_in_play: [ text , … ]
  options_to_test: [ text , … ]
  red_lines: [ text , … ]
  asks_cfo: text
  asks_ops: text
  initial_lean: text
  evidence_ids: [ text , … ]
}
```

**Test memo, CFO and operating head (step 2)**

```
{
  tests: [
    {
      name: text
      threshold: text
      result: pass | fail | not applicable
      numbers: text
      evidence_ids (optional): [ text , … ]
    }
    , …
  ]
  recommended_orders: {
    <every order field of your company, section 6>: one value
  }
  proposal (optional): text
  vetoes: [
    {
      plan: text
      ground: text
      binding: true | false
      evidence_ids (optional): [ text , … ]
    }
    , …
  ]
  would_change_mind_if: text
  memo: text
}
```

**CEO decision (steps 3, 5 and 7)**

```
{
  orders: {
    <every order field of your company, section 6>: one value
  }
  other_moves: [
    {
      move: text
      public: true | false
      detail (optional): text
    }
    , …
  ]
  public_statement: text
  rationale: text
  memo_weighing: {
    cfo: text
    ops: text
  }
  overrides (optional): [
    {
      veto: text
      reason: text
      recorded_as (optional): text
    }
    , …
  ]
  board_response (optional): [
    {
      recommendation: text
      response: text
    }
    , …
  ]
  expected_scenario: text
  best_grid_plan_in_expected_scenario: text
  premium_b: number
  premium_reason: text
  objective_note: text
  predictions: text
  expected_pv_b: number
}
```

**Veto check (step 4)**

```
{
  concur: true | false
  veto (optional): {
    ground (optional): text
    evidence_ids (optional): [ text , … ]
    binding (optional): true | false
  }
  red_line_breach: true | false
  red_line (optional): text
  note: text
}
```

**Board review or confirmation (steps 6 and 8)**

```
{
  items: [
    {
      order_field: text
      value: text
      decision: approve | veto
      ground: text
      acceptable_alternatives (optional): [ text , … ]
      evidence_ids (optional): [ text , … ]
    }
    , …
  ]
  recommendations: [
    {
      text: text
      evidence_ids (optional): [ text , … ]
    }
    , …
  ]
  overall: approve | partial | veto
  note: text
}
```

---

# 8. The five companies' executive committees

### Boeing

- **Executive committee:** Kelly Ortberg (CEO), Jay Malave (CFO), Stephanie Pope (operating head). **Board:** the Boeing Board of Directors.
- **Decision rule:** Ortberg proposes and decides. Malave is his independent check on programme estimates: he can veto any plan that fails his buffer test (the slip leg). Rates are KPI-gated: the KPI doctrine (Pope's seat) vetoes a 737 Rate Increase while a quality, FAA or supply-chain problem is live (the game board has no injects, so it binds only if the brief reports one). Ortberg decides everything else. (teams.md §9; both vetoes are inferences from the evidence.)
- **CFO veto ground:** any plan that fails your buffer test (the slip leg).
- **Operating head veto ground:** a 737 Rate Increase while the brief reports a live quality, FAA or supply-chain problem (the KPI doctrine).
- **Board figures (told to every Boeing seat):** Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): fps 7-year $65.00B and 10-year $60.32B at EIS; undiscounted debt penalty 7-year fps $22.0B, 10-year $19.1B, via Embraer $52.5B, 787 Re-engine alone $0.6B. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

**Every executive seat** (CEO, CFO, operating head) is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are <the seat's name> of Boeing. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".
>
> Your company's run folder holds your brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> Your ExCo's decision rule: Ortberg proposes and decides. Malave is his independent check on programme estimates: he can veto any plan that fails his buffer test (the slip leg). Rates are KPI-gated: the KPI doctrine (Pope's seat) vetoes a 737 Rate Increase while a quality, FAA or supply-chain problem is live (the game board has no injects, so it binds only if the brief reports one). Ortberg decides everything else. (teams.md §9; both vetoes are inferences from the evidence.)
>
> Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command.
>
> Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): fps 7-year $65.00B and 10-year $60.32B at EIS; undiscounted debt penalty 7-year fps $22.0B, 10-year $19.1B, via Embraer $52.5B, 787 Re-engine alone $0.6B. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

**The Board** is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are the Boeing Board of Directors. Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".
>
> Your company's run folder holds the brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> The ExCo is Kelly Ortberg (CEO), Jay Malave (CFO) and Stephanie Pope (operating head). Its decision rule: Ortberg proposes and decides. Malave is his independent check on programme estimates: he can veto any plan that fails his buffer test (the slip leg). Rates are KPI-gated: the KPI doctrine (Pope's seat) vetoes a 737 Rate Increase while a quality, FAA or supply-chain problem is live (the game board has no injects, so it binds only if the brief reports one). Ortberg decides everything else. (teams.md §9; both vetoes are inferences from the evidence.)
>
> Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.
>
> Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command.
>
> Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): fps 7-year $65.00B and 10-year $60.32B at EIS; undiscounted debt penalty 7-year fps $22.0B, 10-year $19.1B, via Embraer $52.5B, 787 Re-engine alone $0.6B. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

### Airbus

- **Executive committee:** Guillaume Faury (CEO), Thomas Toepfer (CFO), Lars Wagner (operating head). **Board:** the Airbus SE Board of Directors.
- **Decision rule:** The CEO leads the ExCo and takes the final call. The CFO and the CEO of Commercial Aircraft hold tests, not formal vetoes: a failed test is a soft veto, which the CEO can override only when the plan is at least $1B better (ΔPV on the brief's grid) than the best option that passes, and the override is recorded as a Board item. The five pillars (safety, quality, integrity, compliance, security) cannot be overridden. NGSA launch, A350 Re-engine, any cancellation and Delay Tactics are Board items; the Board of Directors applies its own tests and may veto. (teams.md; the soft veto is an inference.)
- **CFO veto ground:** a failed financial test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override.
- **Operating head veto ground:** a failed industrial or programme test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override.
- **Board figures (told to every Airbus seat):** Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): NGSA $35.52B at EIS, about $5.07B a year over 7 years in a cash view, so NGSA alone passes a $5.2B peak-cash line narrowly and NGSA with an overlapping A350 Re-engine (about $6.67B a year with strain) does not. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

**Every executive seat** (CEO, CFO, operating head) is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are <the seat's name> of Airbus. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".
>
> Your company's run folder holds your brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> Your ExCo's decision rule: The CEO leads the ExCo and takes the final call. The CFO and the CEO of Commercial Aircraft hold tests, not formal vetoes: a failed test is a soft veto, which the CEO can override only when the plan is at least $1B better (ΔPV on the brief's grid) than the best option that passes, and the override is recorded as a Board item. The five pillars (safety, quality, integrity, compliance, security) cannot be overridden. NGSA launch, A350 Re-engine, any cancellation and Delay Tactics are Board items; the Board of Directors applies its own tests and may veto. (teams.md; the soft veto is an inference.)
>
> Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command.
>
> Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): NGSA $35.52B at EIS, about $5.07B a year over 7 years in a cash view, so NGSA alone passes a $5.2B peak-cash line narrowly and NGSA with an overlapping A350 Re-engine (about $6.67B a year with strain) does not. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

**The Board** is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are the Airbus SE Board of Directors. Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".
>
> Your company's run folder holds the brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> The ExCo is Guillaume Faury (CEO), Thomas Toepfer (CFO) and Lars Wagner (operating head). Its decision rule: The CEO leads the ExCo and takes the final call. The CFO and the CEO of Commercial Aircraft hold tests, not formal vetoes: a failed test is a soft veto, which the CEO can override only when the plan is at least $1B better (ΔPV on the brief's grid) than the best option that passes, and the override is recorded as a Board item. The five pillars (safety, quality, integrity, compliance, security) cannot be overridden. NGSA launch, A350 Re-engine, any cancellation and Delay Tactics are Board items; the Board of Directors applies its own tests and may veto. (teams.md; the soft veto is an inference.)
>
> Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.
>
> Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command.
>
> Board figures: where your agent file quotes an older figure, these govern (they match your brief and dashboard_game.md): NGSA $35.52B at EIS, about $5.07B a year over 7 years in a cash view, so NGSA alone passes a $5.2B peak-cash line narrowly and NGSA with an overlapping A350 Re-engine (about $6.67B a year with strain) does not. The fps 7-year share bonus is gone: every fps move follows the EIS-lead rule in rules.md. An unlaunched Re-engine sits at 2042 on the board.

### CFM/GE

- **Executive committee:** Larry Culp (CEO), Rahul Ghai (CFO), Mohamed Ali (operating head). **Board:** the GE Aerospace Board of Directors (with Safran's consent on CFM programmes).
- **Decision rule:** Culp proposes and decides. Ghai tests terms and capex: price/cost positive and no number before the airframer's volumes are agreed (veto tests); capex within 2-3% of revenue is advice (an analogy for R&D). Ali tests dates: confidence from real testing, not analysis. Whether either test is a formal veto is not shown; in this game (the script's inference) a failed test binds unless Culp answers it with evidence. Tie-break: "safety, quality, delivery and cost, always in that order". Culp's red lines: a next engine needs at least 20% better fuel burn, and durability is not traded for fuel burn. The Safran gate: narrowbody price, capacity and RISE go to the partner; expect consent (inference).
- **CFO veto ground:** terms or capex that fail your tests (inference: binds unless Culp answers it with evidence).
- **Operating head veto ground:** dates not backed by real testing (inference: binds unless Culp answers it with evidence).

**Every executive seat** (CEO, CFO, operating head) is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are <the seat's name> of CFM/GE. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".
>
> Your company's run folder holds your brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> Your ExCo's decision rule: Culp proposes and decides. Ghai tests terms and capex: price/cost positive and no number before the airframer's volumes are agreed (veto tests); capex within 2-3% of revenue is advice (an analogy for R&D). Ali tests dates: confidence from real testing, not analysis. Whether either test is a formal veto is not shown; in this game (the script's inference) a failed test binds unless Culp answers it with evidence. Tie-break: "safety, quality, delivery and cost, always in that order". Culp's red lines: a next engine needs at least 20% better fuel burn, and durability is not traded for fuel burn. The Safran gate: narrowbody price, capacity and RISE go to the partner; expect consent (inference).
>
> Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command.

**The Board** is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are the GE Aerospace Board of Directors (with Safran's consent on CFM programmes). Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".
>
> Your company's run folder holds the brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> The ExCo is Larry Culp (CEO), Rahul Ghai (CFO) and Mohamed Ali (operating head). Its decision rule: Culp proposes and decides. Ghai tests terms and capex: price/cost positive and no number before the airframer's volumes are agreed (veto tests); capex within 2-3% of revenue is advice (an analogy for R&D). Ali tests dates: confidence from real testing, not analysis. Whether either test is a formal veto is not shown; in this game (the script's inference) a failed test binds unless Culp answers it with evidence. Tie-break: "safety, quality, delivery and cost, always in that order". Culp's red lines: a next engine needs at least 20% better fuel burn, and durability is not traded for fuel burn. The Safran gate: narrowbody price, capacity and RISE go to the partner; expect consent (inference).
>
> Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.
>
> Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command.

### Pratt & Whitney

- **Executive committee:** Chris Calio (CEO), Neil Mitchill (CFO), Shane Eddy (operating head). **Board:** the RTX Board of Directors.
- **Decision rule:** Eddy proposes the engine orders (on this board GTF2 and the Joint Venture with Rolls-Royce; an inference from the evidence); Calio frames the turn and proposes the disclosure. Every capital order passes Mitchill's payback and return gate; he can veto on four grounds: the dividend or the debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven. Eddy can veto on technical grounds: durability not proven before entry into service, parts and capacity short of the fleet's needs. Calio decides, setting the safety and durability constraint first. Tie-breaks: the fleet beats a new engine; "if you miss a cycle" beats "we'll cross that bridge" only on visible demand; a rival's discount never moves the answer.
- **CFO veto ground:** one of your four grounds: the dividend or debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven.
- **Operating head veto ground:** durability not proven before entry into service, or parts and capacity short of the fleet's needs.
- **Proposes the engine orders:** the operating head (Shane Eddy).

**Every executive seat** (CEO, CFO, operating head) is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are <the seat's name> of Pratt & Whitney. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".
>
> Your company's run folder holds your brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> Your ExCo's decision rule: Eddy proposes the engine orders (on this board GTF2 and the Joint Venture with Rolls-Royce; an inference from the evidence); Calio frames the turn and proposes the disclosure. Every capital order passes Mitchill's payback and return gate; he can veto on four grounds: the dividend or the debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven. Eddy can veto on technical grounds: durability not proven before entry into service, parts and capacity short of the fleet's needs. Calio decides, setting the safety and durability constraint first. Tie-breaks: the fleet beats a new engine; "if you miss a cycle" beats "we'll cross that bridge" only on visible demand; a rival's discount never moves the answer.
>
> Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command.

**The Board** is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are the RTX Board of Directors. Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".
>
> Your company's run folder holds the brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> The ExCo is Chris Calio (CEO), Neil Mitchill (CFO) and Shane Eddy (operating head). Its decision rule: Eddy proposes the engine orders (on this board GTF2 and the Joint Venture with Rolls-Royce; an inference from the evidence); Calio frames the turn and proposes the disclosure. Every capital order passes Mitchill's payback and return gate; he can veto on four grounds: the dividend or the debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven. Eddy can veto on technical grounds: durability not proven before entry into service, parts and capacity short of the fleet's needs. Calio decides, setting the safety and durability constraint first. Tie-breaks: the fleet beats a new engine; "if you miss a cycle" beats "we'll cross that bridge" only on visible demand; a rival's discount never moves the answer.
>
> Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.
>
> Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command.

### Rolls-Royce

- **Executive committee:** Tufan Erginbilgic (CEO), Helen McCabe (CFO), Rob Watson (operating head). **Board:** the Rolls-Royce Holdings plc Board.
- **Decision rule:** The CEO proposes and decides. Any launch and any aggressive terms need joint CEO-CFO sign-off against mid-to-high-teens hurdles. CFO vetoes: an equity raise, leverage above about 1.5x net debt to EBITDA, levering up for buybacks; in the game her real check is the hurdle and the unselected downside (inference). Civil veto: any compressed maturity, or a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service. Tie-break: the CEO.
- **CFO veto ground:** withholding your joint sign-off on a launch or aggressive terms (hurdle, unselected downside), or a balance-sheet veto.
- **Operating head veto ground:** compressed maturity, a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service.

**Every executive seat** (CEO, CFO, operating head) is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are <the seat's name> of Rolls-Royce. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".
>
> Your company's run folder holds your brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> Your ExCo's decision rule: The CEO proposes and decides. Any launch and any aggressive terms need joint CEO-CFO sign-off against mid-to-high-teens hurdles. CFO vetoes: an equity raise, leverage above about 1.5x net debt to EBITDA, levering up for buybacks; in the game her real check is the hurdle and the unselected downside (inference). Civil veto: any compressed maturity, or a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service. Tie-break: the CEO.
>
> Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command.

**The Board** is told, before its task:

> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.
>
> You are the Rolls-Royce Holdings plc Board. Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".
>
> Your company's run folder holds the brief for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`.
>
> The ExCo is Tufan Erginbilgic (CEO), Helen McCabe (CFO) and Rob Watson (operating head). Its decision rule: The CEO proposes and decides. Any launch and any aggressive terms need joint CEO-CFO sign-off against mid-to-high-teens hurdles. CFO vetoes: an equity raise, leverage above about 1.5x net debt to EBITDA, levering up for buybacks; in the game her real check is the hurdle and the unselected downside (inference). Civil veto: any compressed maturity, or a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service. Tie-break: the CEO.
>
> Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.
>
> Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command.

---

# 9. Known inconsistencies in the original material (game master only)

The original players had these too. Do not pass this section to the companies: it explains, it does not change what
they see. Where texts conflict, the public rules and the brief govern, as they did in the original.

- **Doctrine written for an earlier game.** Each company's behavioural-profile quick card (in its kit) was written
  for an earlier version, with turns from 2026, another engine and other share rules; the "dashboard war game" mapping
  that follows it says what still applies. Where a quick card's share rule, figures or turn plan differ from the public
  rules or the brief, those govern.
- **Market size.** Some persona and doctrine texts say the narrowbody market is fixed at 2,000 aircraft (4,000
  engines) a year. In this game supply and demand govern (section 5, last part).
- **Boeing's H4 overlap.** Boeing's game mapping says a Solo fps launched with the 787 Re-engine in the same round
  overlaps by 5 years. That holds for the 7-year fps; a 10-year fps (or via Embraer) overlaps by 2 years (the strain
  overlap counts the fps from EIS minus 7 and the Re-engine from EIS minus 5). Boeing's operating head and Board say so.
- **"fps as a Joint Venture"** (Boeing doctrine H1, H4, H7) has no order on this board.
- **`launch_if_selected`.** The engine launches the engine when, after this round's orders, a live airframe
  (launched this round or earlier, not cancelled, not yet in service) carries an engine code that includes the maker,
  new or standing, and the engine would be ready by that airframe's EIS. The rules' wording ("selected you this
  round") is narrower; the Pratt & Whitney personas describe the engine's behaviour.
- **GEnx timing.** Some CFM texts say a GEnx package counts from launch plus 3 years and not before 2035; the rules say
  it counts 3 years after launch, and widebody engine shares move only from the first re-engine (or 2042).
- **Engine code `None`.** The briefs print the no-code option as `None`; in orders it is JSON `null`.
- **Pratt & Whitney's round-1 brief** shows its status-quo ΔPV as −0.00 (floating-point noise) and its "ΔPV ≥ 0"
  objective as not met; the original players saw the same. The status-quo component tables in round-1 briefs are
  empty because every component is zero.

---

# 10. Where everything is

| Company | CEO | CFO | Operating head | Board | Kit |
|---|---|---|---|---|---|
| Boeing | `boeing-ortberg` | `boeing-malave` | `boeing-pope` | `boeing-board` | `kits/COMPANY_boeing.md` |
| Airbus | `airbus-faury` | `airbus-toepfer` | `airbus-wagner` | `airbus-board` | `kits/COMPANY_airbus.md` |
| CFM/GE | `cfm-culp` | `cfm-ghai` | `cfm-ali` | `cfm-board` | `kits/COMPANY_cfm.md` |
| Pratt & Whitney | `pratt-whitney-calio` | `pratt-whitney-mitchill` | `pratt-whitney-eddy` | `pratt-whitney-board` | `kits/COMPANY_pratt_whitney.md` |
| Rolls-Royce | `rolls-royce-erginbilgic` | `rolls-royce-mccabe` | `rolls-royce-watson` | `rolls-royce-board` | `kits/COMPANY_rolls_royce.md` |

- `personas_full/<agent>.md`: the agent definitions the original game used, adapted only in file paths and the
  Independence section (they are in the kits too). `personas/<agent>.md`: condensed cards of the same, for reference.
- `companies/<company>/`: each company's profile, objectives, game doctrine, 2026 analyst-model baseline, executive
  and Board profiles, role cards and evidence.
- `engine/`: `play.py` (the engine's commands), `run_game.py` (the runner), `protocol.json` (the protocol's teams,
  order fields and formats), `dashgame/` (the engine), `runs/dash-2050-cons-start/` (the 2030 position),
  `requirements.txt`; in the full pack also `reference/` (the original game).
