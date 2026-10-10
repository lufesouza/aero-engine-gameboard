# Spec: one Board of Directors agent per company, with veto and recommendation power

## Goal

Each company in the dash-2050 war game is played by its executive committee (ExCo): three agents, the CEO, the CFO and
the operating head (`SPEC.md`). We now add one agent per company for its **Board of Directors**. The Board does not
originate orders. It does two things:

- it **recommends**: before each round it gives the ExCo non-binding guidance (priorities, risk appetite, what it would
  and would not approve);
- it **approves or vetoes** every big decision (a Board item), and its veto binds.

The Board's decision-making must reflect the company's culture, in particular its **risk aversion** and its **time
horizon** (long-term value against short-term results). That culture is profiled from two kinds of evidence:

- the transcripts and filings already in the repo: management's and chairs' words about the board, its approvals,
  authorisations and reserved matters;
- internet information found with web search: composition, committees, governance rules, culture assessments, past
  board decisions, and the pay horizon that the board sets.

Nothing is run now.

Repo root: /home/user/aero-engine-gameboard

## The five boards

| Company (side) | Agent | Board it plays | Notes |
|---|---|---|---|
| Boeing (`boeing`) | `boeing-board` | The Boeing Company Board of Directors | Separate independent chair; Aerospace Safety Committee |
| Airbus (`airbus`) | `airbus-board` | Airbus SE Board of Directors | Reserved matters above €300m and "abnormal" risk; state shareholders |
| CFM/GE (`cfm`) | `cfm-board` | GE Aerospace Board of Directors | Plays GE's board. CFM programmes also need the 50/50 partner Safran: model it as the CFM International parity rule (Safran consent) inside this agent, labelled as such |
| Pratt & Whitney (`pratt_whitney`) | `pratt-whitney-board` | RTX Corporation Board of Directors | P&W is an RTX business; RTX's board approves its big capital decisions |
| Rolls-Royce (`rolls_royce`) | `rolls-royce-board` | Rolls-Royce Holdings plc Board | UK board; capital discipline after the 2020 crisis |

Use the board as it stands at the latest date the sources show (2025-2026). Name the chair, any lead independent
director, the committees that matter for the game (e.g. safety, finance, audit, technology), and the directors whose
background bears on the decisions. Say "as of" the date of the source.

## Sources and evidence

### Repo sources (verbatim, machine-checked)

- Company and executive evidence files: `wargame/profiles/<side>/evidence.jsonl`, `wargame/profiles/<side>/executives/evidence.jsonl`.
  Items that mention the board are citable by their existing ids (B-, BX-, A-, AX-, C-, CX-, P-, PX-, R-, RX-). Search
  them for "board", "chairman", "director", "authoriz", "approv", "governance", "safety committee", "shareholder".
- Extracted full text, with page markers, in `$WARGAME_BUILD_DIR/text/`
  (`WARGAME_BUILD_DIR=/tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad`):
  `transcripts.txt` (Boeing calls), `boeing_10k.txt`, `ge_transcripts.txt`, `rtx_transcripts.txt`, `rtx_10k.txt`,
  `rr_transcripts.txt`, `airbus_fy2025.txt` and `airbus_pages/NNN.txt` (OCR). Grep them for board material that is
  not yet an evidence item (e.g. a chairman's remarks, a board approval, a dividend or buyback decision, reserved
  matters, committee charters in the 10-Ks).
- New items from these sources go into the board evidence file (below) with `source` and `page`, and must pass
  `python3 wargame/profiles/build/verify_quotes.py <file>` (with `WARGAME_BUILD_DIR` set as above).

### Internet sources (web search)

- The container cannot fetch web pages (the network policy blocks them). Use the **WebSearch** tool (load it with
  ToolSearch `select:WebSearch`). It returns result titles, URLs and a summary of what the results say.
- A web item records: the claim as the search summary states it (`quote`, which is NOT verbatim page text), the
  result URL(s) that support it, the title and publisher, the source date where known, and `retrieved` (the search
  date). Prefer primary sources: proxy statements (DEF 14A), annual reports, company governance pages, board
  committee charters, regulator reports (e.g. the FAA expert panel report on Boeing's safety culture), then reputable
  press (Reuters, FT, WSJ, Bloomberg, Aviation Week).
- Every web item must be **corroborated** by a second, independently worded search that returns the same fact
  (`corroborated_by`: the second query and its URL). Uncorroborated facts may be used only as (inference) and must
  not carry a test, a veto or a culture score.

### Board evidence file

`wargame/profiles/<side>/board/evidence.jsonl`, one JSON object per line. Ids: Boeing `BG-0001`, Airbus `AG-0001`,
CFM/GE `CG-0001`, P&W/RTX `PG-0001`, Rolls-Royce `RG-0001`.

```json
{"id": "BG-0001", "company": "boeing", "exec_id": "board", "kind": "transcript|filing|web",
 "dimension": "composition|reserved_matters|risk_appetite|time_horizon|capital_allocation|safety_oversight|pay_horizon|shareholders|past_decisions|management_relationship|succession",
 "date": "YYYY-MM-DD (date of the source)", "source": "transcripts|boeing_10k|ge_transcripts|rtx_transcripts|rtx_10k|rr_transcripts|airbus_fy2025|web",
 "doc": "document or page title", "page": 123, "url": "https://... (web only)", "publisher": "(web only)",
 "retrieved": "2026-10-10 (web only)", "corroborated_by": [{"query": "", "url": ""}],
 "speaker": "who said it, or the publisher", "quote": "verbatim for transcript/filing; the search summary's statement for web",
 "finding": "what it tells us about the board, one or two sentences",
 "perspective": "board_own_words|management_on_board|filing|web_official|web_press|web_analysis"}
```

Also write `wargame/profiles/<side>/board/sources.md`: one line per web source (URL, title, publisher, date) and
the queries used.

## The board profile

`wargame/profiles/<side>/board/board.md`, the research synthesis the agent plays from, with these sections:
1. Header: board, as-of date, evidence counts by kind, confidence overall.
2. Composition (chair, lead independent director, size, independence, committees, notable directors, major
   shareholders or state holdings).
3. Governance: matters reserved to the board, thresholds, how votes are taken, delegation to management.
4. Culture: risk aversion and time horizon, each scored 1-5 with the evidence and the trend; capital allocation
   priorities; safety oversight; stakeholder or state influence; how pay horizons (the incentive plans the board sets)
   weight short against long term.
5. Decision record: big decisions the board took or approved (launches, cancellations, CEO changes, capital raises,
   buybacks, dividend cuts), dated, with evidence.
6. Relationship with management: combined or separate chair and CEO; how much the board defers; tensions.
7. How it reads rivals (only with evidence).
8. Confidence and gaps.

## Culture scoring (calibrated across the five boards)

- **Risk aversion**, 1-5: 1 = seeks bold bets and tolerates large programme and balance-sheet risk; 3 = balanced;
  5 = strongly averse (protects the balance sheet, the rating and safety first; demands proof before commitment).
- **Time horizon**, 1-5: 1 = short-term results (quarterly earnings, near-term cash returns, buybacks first);
  3 = balanced; 5 = long-term (multi-decade programmes and technology, accepts near-term cost for long-term position).
- Each score has a rationale, evidence ids, and a trend (how it has moved, e.g. before and after a crisis).
- Scores are judgements from evidence, labelled as such. The final cross-check calibrates them across the five
  boards so that a 4 means the same at every company.

## Board items in the game

On the dash-2050 board every order that differs from the default (`hold`, or `none` for Delay Tactics) is a Board item:
any launch, `launch_if_selected`, Joint Venture `commit` or `withdraw`, cancellation, the 737 Rate Increase, a GEnx
package, lobbying, Delay Tactics. An engine code rides with its airframe launch. The board profile must say how this
maps to the company's real reserved matters (e.g. Airbus: above €300m or "an abnormal level of risk"), and flag any
item that is below the real threshold (it is still reviewed, as part of the round's package).

## The round protocol with the Board (per company, each round)

0. **Board guidance (Board).** Reads the round brief and earlier rounds' notes. Returns non-binding guidance: priorities,
   risk appetite this round, what it expects to see, what it would approve or veto, recommendations.
1. **Frame (CEO)**, reading the Board's guidance.
2. **Test (CFO and operating head)**, as before; their memos go to the Board with the decision.
3. **Decide (CEO)**, as before, plus `board_response`: how each Board recommendation was taken up or why not.
4. **Veto check (CFO and operating head)**, as before.
5. **Revise (CEO)**, as before, if a binding ExCo veto or a red-line flag stands.
6. **Board review (Board).** Sees the ExCo's package (frame, memos, decision, veto checks, revision). For each Board
   item: approve or veto, with the ground and evidence; for a veto it may name acceptable alternatives. Plus
   recommendations (non-binding). The Board does not originate orders.
7. **Board revise (CEO)**, only if the Board vetoed an item: revises once, within the Board's veto (an alternative the
   Board named, or the default).
8. **Board confirm (Board)**, only after a Board revise: approves or vetoes the revised items. A still-vetoed item
   reverts to the default. The Board's recommendations go into the next round's guidance and the ExCo's notes.

## Board agent definition (`.claude/agents/<side>-board.md`)

YAML front matter (`name`, `description`, `tools: Bash, Read, Grep, Glob`; strict YAML: no ": " inside the
description), then a second-person system prompt with these headings, in this order:

1. `# <Board name> (Board of Directors, <company>)`: who you are; that you are the board, not management; that the CEO,
   CFO and operating head are separate agents; that you approve, veto and recommend but never originate orders.
2. `## Who you are`: composition as of the latest source.
3. `## Your record`: evidence counts by kind (transcript, filing, web), dates, confidence by area.
4. `## What you hold management to`: ranked, with ids.
5. `## Your culture`: risk aversion and time horizon (score, rationale, ids, trend); capital allocation; safety
   oversight; stakeholder influence; pay horizon. Say how each shapes your votes.
6. `## Matters reserved to you`: the real reserved matters and how the game's Board items map onto them.
7. `## How you decide`: process (committees, majority), tempo, what you need to see before you approve.
8. `## Your tests`: table | Test | Threshold or rule | Evidence |, computable from the ExCo package and the brief.
9. `## Your veto and its limits`: grounds, that it binds, that you may name acceptable alternatives, that you do not
   originate orders, and what you never veto (e.g. a hold).
10. `## Your recommendations`: style and typical asks; how the ExCo must answer them.
11. `## How you see management`: one line each on the CEO, CFO and operating head (the three agents), with ids.
12. `## How you read the rivals`: evidence only; otherwise say there is none.
13. `## Decisions you have taken`: the decision record, dated, with ids.
14. `## Where your record is thin`: gaps and the fallback (company profile, past decisions, defer to the CEO's case
    unless a test fails). Never invent a view.
15. `## Your voice`: how the board speaks (chair letters, board statements); quotes VERBATIM from transcript or filing
    items only (never from web items), each with its id; if there are none, say so.
16. `## Your files`: own board profile and evidence, company `profile.md`, `objectives.md` §1, `dashboard_game.md`,
    `executives/teams.md`, the round brief `/tmp/wargame-<side>/<run>/roundN.md`, `rules.md`, and the ExCo and
    Board notes folder `/tmp/wargame-<side>/<run>/exco/`.
17. `## Your step in each round`: guidance, review, confirm, with exactly what to produce.
18. `## Independence`: the same rules as the executives (own company only; no engine; numbers from the brief and the
    profile; a hook enforces it).
19. `## What you return`: the fields below.
20. `## Language`: Do Nothing (never Milk), Re-engine, Joint Venture, Delay Tactics (never Sabotage); fps, NGSA.

Return fields:
- **guidance:** `priorities, risk_appetite, expect_to_see, would_approve, would_veto, recommendations[{text, evidence_ids}], evidence_ids`
- **review / confirm:** `items[{order_field, value, decision: approve|veto, ground, acceptable_alternatives, evidence_ids}], recommendations[{text, evidence_ids}], overall: approve|partial|veto, note`

## The executives' new section

Each of the 15 executive agents gets a `## Your Board` section, placed right after `## Your colleagues`:
- who the board is (chair, key committee for your seat), in one or two lines;
- what goes to the board (every non-default order) and its culture (risk aversion, time horizon), so you know what
  will pass;
- your seat's part: CEO reads the guidance, answers each recommendation in `board_response`, and revises within a
  Board veto (`board_revise` step); CFO and operating head write memos that the Board will read;
- evidence ids from the board evidence file and the company files.

Also update each executive's `## Your step in each round` and `## What you return` (CEO: `board_response`; the
`board_revise` step uses the decide fields) and the CEO's description line to mention the board revise step.

## Profile JSON for the page (`<side>-board.json`)

```json
{"agent_name": "", "company": "", "side": "", "board_name": "", "as_of": "",
 "composition": {"chair": "", "chair_is_ceo": false, "lead_independent_director": "", "size": "", "independence": "",
                 "committees": [{"name": "", "role": ""}], "notable_members": [{"name": "", "background": ""}],
                 "shareholders": "", "ids": [""]},
 "evidence": {"n_items": 0, "n_transcript": 0, "n_filing": 0, "n_web": 0, "first": "", "last": "", "sources_note": "",
              "confidence_overall": "", "confidence_by_area": [{"area": "", "level": ""}]},
 "mandate": "", "holds_management_to": [{"text": "", "ids": [""]}],
 "culture": {"risk_aversion": {"score": 0, "rationale": "", "trend": "", "ids": [""]},
             "time_horizon": {"score": 0, "rationale": "", "trend": "", "ids": [""]},
             "capital_allocation": {"text": "", "ids": [""]}, "safety_oversight": {"text": "", "ids": [""]},
             "stakeholder_influence": {"text": "", "ids": [""]}, "pay_horizon": {"text": "", "ids": [""]}},
 "reserved_matters": [{"matter": "", "threshold": "", "ids": [""], "inference": false}],
 "board_items_in_game": [{"order": "", "rule": "", "ids": [""], "inference": false}],
 "decision_process": [{"text": "", "ids": [""], "inference": false}],
 "tests": [{"test": "", "threshold": "", "ids": [""], "inference": false}],
 "veto": [{"ground": "", "ids": [""], "inference": false}],
 "recommendation_style": {"text": "", "ids": [""]},
 "management_relationship": [{"name": "", "relation": "", "ids": [""]}],
 "rivals": [{"text": "", "ids": [""], "inference": false}],
 "past_decisions": [{"date": "", "decision": "", "ids": [""]}],
 "thin": {"gaps": [""], "fallback": ""},
 "voice": {"style": "", "quotes": [{"id": "", "quote": "", "date": "", "doc": "", "perspective": ""}]},
 "web_sources": [{"id": "", "url": "", "title": "", "publisher": "", "date": ""}],
 "protocol_steps": ["guidance", "review", "confirm"]}
```

## Evidence rules (strict)

- Every claim carries ids or is marked (inference).
- Transcript and filing quotes are verbatim and pass `verify_quotes.py`; web statements are never presented as quotes
  or as someone's speech.
- A culture score, a test, a veto ground or a reserved matter needs at least one transcript/filing item or one
  corroborated web item.
- Keep dates: say "as of" for composition, and do not present a 2019 fact as current without saying so.
- No `wargame.engine` instructions. The board reads only its own company's files.
