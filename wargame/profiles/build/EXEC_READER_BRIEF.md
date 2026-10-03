# Reader brief: evidence for executive profiles (Boeing and Airbus leaders)

We are building **profiles of individual executives** for a strategy war game:
- **CEOs:** at Boeing, McNerney, Muilenburg, Calhoun and Ortberg; at Airbus, Faury.
- **CFOs:** at Boeing, Bell, Smith, West and Malave; at Airbus, Toepfer.
- **Operating heads:** at Boeing, the presidents of Commercial Airplanes (BCA), i.e. Albaugh, Conner, Deal and Pope, and Muilenburg in his COO years; at Airbus, the CEO of Commercial Aircraft.

In the game, a company's leadership team decides each turn whether and when to launch a new airplane, re-engine, change production rate, cancel, choose engines and partner. The agents must decide **the way each person decided**, in their professional role, as shown by their own words on earnings calls and investor events.

**Scope: professional conduct only.** Record what the executive said and did as an executive: priorities, decisions, reasoning, commitments and how they turned out, reactions to events. Do **not** record anything about private life, health, family or appearance, and do not speculate about motives beyond what the words support.

## Your input

Your input is a slice file holding ONE executive's own speaking turns. Each turn is headed:

`##### <date> | <event> | page <n> | <title> | prepared|Q&A`

Long turns contain `[page n]` markers. The `######## FILE ... (source id for citations: <src>) ########` line gives the `source` value for your items. Read the whole slice. When you need the analyst's question, read the transcript page:

`WARGAME_BUILD_DIR=<S> python3 wargame/profiles/build/pages.py <src> <page> <page>`

## What to extract (one item per distinct, decision-revealing behaviour)

Tag each item with one `dimension`:
- `priorities`: what they say they optimise, and how the ranking shifts over time.
- `decision_style`: speed, data vs conviction, centralised vs delegated, reversals, appetite for bold moves, "wait until it's real".
- `risk_appetite`: technology, schedule, balance-sheet and fixed-price risk; quotes that give thresholds.
- `capital_allocation`: R&D, capex, buybacks, dividends, debt, M&A, equity raises, cash vs share.
- `product_strategy`: clean sheet vs derivative, timing, the business case for a new airplane, partnerships and Joint Ventures, engines, the middle of the market.
- `operations`: production rates, supply chain, quality, the factory, labour, regulators.
- `rival_view`: how they describe Airbus, Embraer, COMAC and the engine makers, and their competitive moves.
- `communication`: guidance style, how they deliver bad news (deny, minimise, reset, own it), confidence language, signature phrases.
- `credibility`: a dated **commitment or forecast** (EIS, rate, cash, margin, "no equity", "the worst is behind us") and, if the slice shows it, what happened. Use the `numbers` field.
- `crisis_response`: the 787 battery (2013), the MAX accidents and grounding (2019-20), COVID, the door plug (2024), strikes, the 777X slips.
- `team`: how they describe the CEO-CFO-BCA relationship, decision rights, culture and accountability.

Aim for **40-110 items** per slice, spread across dimensions and years. Cover every year in the slice.

## Output (JSON Lines) to the file named in your task

```
{"company": "boeing", "exec_id": "<id from your task>", "dimension": "<one of the above>",
 "date": "YYYY-MM-DD", "source": "transcripts"|"rtx_transcripts", "doc": "<event>", "page": 1234,
 "speaker": "<Name, title as printed>", "role_at_time": "CEO"|"CFO"|"COO"|"BCA CEO"|...,
 "quote": "verbatim text copied exactly, <= 60 words, ... to elide",
 "finding": "one sentence: what this shows about how this executive decides or behaves",
 "trigger": "", "response": "", "lag": "", "numbers": {}, "perspective": "own_words"}
```

**Quote verbatim.** Copy exactly from the slice. Join lines with single spaces and drop `[page n]` markers. The page is the turn's page, or the `[page n]` marker before the quoted text.

**Verify:** `cd <repo> && WARGAME_BUILD_DIR=<S> python3 wargame/profiles/build/verify_quotes.py <your file>`. Fix or drop rejects until the rejected file is empty.

## Return (structured)

- **summary** (at most 500 words):
  - the person's stated priorities and how they shifted;
  - decision style;
  - risk appetite;
  - how they handle bad news;
  - a commitment track record with dates;
  - their view of Airbus;
  - their signature phrases.
- **calibration_candidates**: leave empty unless you find numeric thresholds (for example a return hurdle or a debt ceiling).
- **gaps**.
