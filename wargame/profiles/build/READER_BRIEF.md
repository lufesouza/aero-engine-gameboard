# Reader brief: evidence for the Boeing and Airbus war-game agents

We are building two **independent** strategy agents, one for Boeing and one for Airbus, for a war game about the next generation of airliners. Each agent must behave the way its company has **actually behaved**:
- financially: capital allocation, balance-sheet risk appetite, R&D and capex appetite, pricing, margins, dividends and buybacks;
- operationally: production rates and ramps, supply chain, quality, program execution, delays and charges;
- **responsively**: how it reacted to the rival's moves and to market shocks.

Your job is to read one slice of the source material and extract cited evidence.

The war game's levers, to judge relevance:
- launching a new narrowbody, and when (Boeing "fps" / new single-aisle, the Airbus NGSA);
- Solo vs Joint Venture (for example Boeing–Embraer);
- re-engining or upgrading a widebody (787, A350, 777X), or Doing Nothing and keeping the current product;
- production rate increases;
- tactics that delay the rival: supplier bottlenecks, poaching talent;
- cancelling programs;
- engine choice (CFM, Pratt & Whitney, Rolls-Royce).

Anything that reveals how a company decides these things is gold: the reasons it gives, the thresholds it names, the trade-offs it makes, and how it responded to the other side.

## Tools

- Text files are in `wargame/profiles/build/work/text/`. Pages are marked `=== PAGE N ===`.
- Read pages in batches of about 10-15 with:
  `python3 wargame/profiles/build/work/pages.py <transcripts|boeing_10k|airbus_fy2025> <first> <last>`
- `transcript_index.json` lists each transcript's event, date and page range.
- Only read the pages assigned to you. Do not modify anything outside your own output files.

## Output 1: evidence lines

Append one JSON object per line to `.../scratchpad/evidence/<your-name>.jsonl`. Fields:

```
{"company": "boeing"|"airbus"|"other",      // whose behaviour the item describes
 "category": "financial"|"operational"|"competitive_response"|"strategy_principle"|"rival_observation"|"game_lever",
 "date": "YYYY-MM-DD",                       // date of the source event/document
 "source": "transcripts"|"boeing_10k"|"airbus_fy2025",
 "doc": "FQ2 2011 Earnings Call" | "10-K FY2015" | "Airbus Board Report FY2025",
 "page": 1234,                               // the === PAGE N === number
 "speaker": "Jim McNerney, CEO" | "analyst (Goldman Sachs)" | "",
 "quote": "verbatim text copied exactly from the page, <= 60 words, use ... to elide",
 "finding": "one sentence: what this reveals about how the company behaves",
 "trigger": "for competitive_response / rival_observation: the rival move or market condition, else ''",
 "response": "for competitive_response: what the company did or said it would do, else ''",
 "lag": "time between trigger and response if stated or evident, else ''",
 "numbers": {"key": value}                   // any figures in the quote, e.g. {"rate_737_per_month": 42}
}
```

Rules:
- **Verbatim quotes.** Copy the words exactly as they appear. We will machine-check every quote against the source, and items that fail are discarded.
- **The finding must follow from the quote.** No outside knowledge, no speculation.
- Prefer decision-revealing statements (commitments, reasons, thresholds, trade-offs, reactions, reversals) over boilerplate. One item per distinct behaviour. Keep repeated statements only when they show persistence or a change of position; say which in the finding.
- Keep numbers: rates, margins, cash, free cash flow, debt, R&D, capex, dividends, buybacks, charges, deliveries, backlog, market share.
- `rival_observation`: what the source says about the other company, for example Boeing describing Airbus pricing or the A320neo launch. Set `company` to the company being described.
- Aim for **40-120 items**, depending on how rich the slice is.

## Output 2: slice summary

Write `.../scratchpad/evidence/<your-name>.summary.md`, at most 400 words, covering:
- the period covered;
- the key decisions;
- how the company responded to its rival;
- its financial posture;
- its operational problems;
- anything that contradicts earlier behaviour.

Cite pages, for example (p. 1234).

## Final reply

Five lines at most: your slice, the item count, and the three most important behavioural patterns you found.
