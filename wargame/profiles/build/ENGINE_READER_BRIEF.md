# Reader brief: evidence for the engine-maker agents (Rolls-Royce, Pratt & Whitney)

We are building **independent** strategy agents for the engine makers in a Boeing vs Airbus war game about the next generation of airliners:
- **Rolls-Royce** (`rolls_royce`);
- **Pratt & Whitney** (`pratt_whitney`), part of RTX, formerly United Technologies (UTC).

Each agent must behave the way its company has **actually behaved**:
- **financially**: capital allocation, R&D and capex appetite, balance-sheet risk, pricing of new engines vs the aftermarket, cash;
- **operationally**: engine programmes, deliveries, durability and quality crises, shop visits, supply chain, execution against plan;
- **responsively**: how it reacted to airframer decisions (engine selections, launches, re-engines), to rival engine makers (CFM/GE, RR, PW) and to shocks (COVID, fuel, groundings).

You read one slice of the source material and extract cited evidence.

## The game's engine-maker levers (to judge relevance)

Each turn (2026-28, 2029-31, 2032-34, 2035-37) Boeing and Airbus decide:
- whether and when to launch a new single-aisle (Boeing "fps", Airbus "NGSA");
- whether to re-engine a widebody (787, A350);
- which engine each new aircraft flies.

An engine maker can only be selected once it has committed to the engine. Its payoff is the lifecycle value of the engines it delivers (the OE margin, often negative, plus the aftermarket), minus its development spending.

**Rolls-Royce's levers:**
- launch an UltraFan widebody engine;
- launch an UltraFan narrowbody engine, Solo or as a Joint Venture with Pratt & Whitney;
- standard or aggressive (discounted) terms;
- a Trent 1000 upgrade (787 share, installed-base costs);
- cancel;
- Do Nothing.

**Pratt & Whitney's levers:**
- launch a next-generation geared turbofan for fps or NGSA;
- launch a new widebody engine (P&W has had none since the PW4000);
- standard or aggressive terms;
- a GTF durability upgrade (share of A320neo deliveries, installed-base costs such as the powder-metal groundings and customer compensation);
- join Rolls-Royce's UltraFan narrowbody Joint Venture;
- cancel;
- Do Nothing.

**Anything that reveals how the company decides these things is gold.** For example:
- the returns or thresholds it names for a new engine;
- whether it needs a launch customer;
- sole source vs competing on a platform;
- how it prices OE vs services;
- how it handled crises and who paid;
- partnerships (IAE/V2500, Joint Ventures);
- what it says about rivals and customers.

## Tools

- Text is in `<S>/text/<source>.txt`, with pages marked `=== PAGE N ===`. `<S>` is the path in your task.
- Read pages in batches of 10-15:
  `WARGAME_BUILD_DIR=<S> python3 wargame/profiles/build/pages.py <source> <first> <last>`
- Event indexes (event, date, page, end_page) are in `<S>/text/rr_transcripts_index.json`, `rtx_transcripts_index.json` and `rtx_10k_index.json`.
- Read only your assigned pages. Write only your own output files.

## Output: evidence lines (JSON Lines)

Append one object per line to the file named in your task:

```
{"company": "rolls_royce"|"pratt_whitney"|"cfm_ge"|"boeing"|"airbus"|"other",   // whose behaviour the item describes
 "category": "financial"|"operational"|"competitive_response"|"strategy_principle"|"rival_observation"|"customer_observation"|"game_lever",
 "date": "YYYY-MM-DD",               // date of the event/document (from the index)
 "source": "rr_transcripts"|"rtx_transcripts"|"rtx_10k"|"gtf_news"|"engine_brief_2019"|...,
 "doc": "FY 2019 Earnings Call" | "UTC Form 10-K FY2018" | ...,
 "page": 1234,                       // the === PAGE N === number
 "speaker": "Warren East, CEO" | "analyst (Goldman Sachs)" | "",
 "quote": "verbatim text copied exactly from the page, <= 60 words, use ... to elide",
 "finding": "one sentence: what this reveals about how the company behaves",
 "trigger": "for competitive_response: the rival/customer move or market condition, else ''",
 "response": "what the company did or said it would do, else ''",
 "lag": "time between trigger and response if stated or evident, else ''",
 "numbers": {"key": value},
 "perspective": "own_words"|"analyst_question"|"observed_by_rolls_royce"|"observed_by_pratt_whitney"|"filing"|"press"|"industry_report"}
```

**Rules**
- **Quote verbatim.** Every quote is machine-checked against its cited page (±1 page); items that fail are discarded.
- **The finding must follow from the quote.** No outside knowledge.
- **Prefer decision-revealing statements.** Commitments, reasons, thresholds, trade-offs, reactions and reversals, not boilerplate. One item per distinct behaviour. Keep repeats only when they show persistence or a change of position, and say which in the finding.
- **Keep the numbers:**
  - margins, cash and FCF, R&D and capex, dividends and buybacks;
  - charges, provisions and compensation;
  - deliveries, installed base, shop visits, flying hours;
  - OE losses per engine, aftermarket rates, market shares, order intake;
  - time on wing, durability improvements, guidance.
- **The other engine maker, as described by your company:** set `company` to the company described (e.g. `pratt_whitney` on an RR call) and `perspective` to `observed_by_<speaker's company>`.
- **Customers (Boeing, Airbus) and airlines:** use `customer_observation` for what the company says about them.
- **Analysts' assertions** in questions are `analyst_question`. Keep them only when the executive's answer confirms or rejects them, and put the answer in a separate item.
- **Aim for 40-120 items** depending on how rich the slice is. On RTX calls, only Pratt & Whitney and the engine business (and RTX-level capital allocation that shows how P&W is funded) are relevant, so skip Collins and Raytheon detail.

## Verification (mandatory)

When done, run:

```
cd <repo> && WARGAME_BUILD_DIR=<S> python3 wargame/profiles/build/verify_quotes.py <your file>
```

It writes `.verified.jsonl` and `.rejected.jsonl`. Fix the quote or page of every reject (re-read the page), or delete the item, and re-run until the rejected file is empty.

## Your final reply (structured)

- **summary**: at most 450 words, citing pages. Cover:
  - the period;
  - the key decisions;
  - the financial posture;
  - operational problems;
  - reactions to rivals and customers;
  - anything contradicting earlier behaviour.
- **calibration_candidates**: numbers useful to the game engine, each with its derivation and pages. For example:
  - OE loss or price per engine;
  - aftermarket rates and margins;
  - development spending and years for a new engine;
  - the share of a platform;
  - crisis costs;
  - returns thresholds.
- **gaps**.
