# Airbus executive profiles

These are war-game profiles of the Airbus leaders, and of the team they form, for the `airbus-strategist` player and the referee. They are **profiles of professional conduct only**, built from the sources listed below. **Read the confidence column before leaning on any of them.**

## Sources and their limits

- **`evidence.jsonl` (AX ids):** 109 items.
  - 92 come from the **FY2025 Board Report** (issued 18 February 2026). It is a third-person, Board-approved and positively framed account.
  - 16 are **outside mentions** by Boeing executives, analysts and journalists on Boeing calls (10), and by the CEO of Pratt & Whitney's parent (6).
  - **One** is an Airbus executive's own words: Faury's signed line on safety, quality, integrity, compliance and security [AX-0081].
- **`../evidence.jsonl` (A ids):** Airbus company evidence. These files use it for governance, finance and product context.
- **No Airbus earnings-call, investor-event or interview transcripts are in the corpus.** No Airbus executive can be profiled from the way he speaks and decides. Every behavioural rule here is **(inference)** from incentives, roles and the Board's narrative, unless an id says otherwise.

## Index of executives

| exec_id | Name | Role | Dates shown in the sources | AX items | Own words | Confidence | File |
|---|---|---|---|---|---|---|---|
| `faury` | Guillaume Faury | CEO, Board member | CEO by 2020 (holds the 2020 plan); Board term to 2028; evidence 2021-2026 | 55 (46 Board, 4 Boeing-side, 4 P&W-side, 1 own) | 1 line | Incentives **High**; 2025 actions **Medium**; style and voice **Low** | `faury.md` |
| `toepfer` | Thomas Toepfer | CFO; chairs the Internal Control Committee | FY2025; start date not shown | 7 (all Board) | none | **Low** | `toepfer.md` |
| `wagner` | Lars Wagner | CEO Commercial Aircraft | Joined in November (year cut off); in role from 1 Jan 2026 | 2, plus 2 naming him in the handover and 1 referring only to the role | none | **Very low** (role-derived) | `wagner.md` |
| `enders` | Tom Enders | CEO | Named as CEO in 2017 and 2019 remarks | 3 (2 P&W-side, 1 Board) | none | **Very low**, outside view | `historical.md` |
| `leahy` | John Leahy | Chief commercial officer (sales chief) | Described 2011-2018; retired 2018 | 6 (all Boeing-side) | none | **Low**, outside view | `historical.md` |
| `scherer` | Christian Scherer | Former CEO Commercial Aircraft | Handed over by 1 Jan 2026 | 1 (Board), the only item that names him | none | **Minimal** | `historical.md` |
| `airbus_exco` | Board and Executive Committee (governance) | n/a | FY2025 | 35 (Board) | n/a | **High** for governance facts | `teams.md` |

## Teams

| Team id | Members | Status | File |
|---|---|---|---|
| `faury-toepfer-wagner-2026` | Faury (CEO), Toepfer (CFO), Wagner (CEO Commercial Aircraft) | **DEFAULT for the 2026 game.** The only Airbus team offered. | `teams.md` |

**No historical Airbus team** (for example Enders and Leahy) is offered: the evidence on them before 2025 is eight outside remarks, plus one 2026 Board line on the A220's outcome. A request for one gets the default team plus the labelled `historical.md` modifier.

## How the airbus-strategist uses these files

1. **At game start:**
   - read the `faury-toepfer-wagner-2026` section of `teams.md`;
   - read the **Quick card** of `faury.md`, `toepfer.md` and `wagner.md`.
2. **Every turn:**
   - re-read the team section;
   - run its **ExCo deliberation script**: CEO frames, CFO tests cash, CA CEO tests production, decide by the team rule, Board gate, speak;
   - put 2-4 lines per member in the `rationale`, each citing AX or A ids and the engine numbers asked for.
3. **What is in bounds versus how to decide.** `../profile.md` decides what is in bounds: hard rules, red lines, the default plan. The team decides how options are weighed: the soft vetoes, tie-breaks and timing preferences. If they conflict on what is allowed, the profile wins.
4. **Voice.**
   - `public_statement` and `disclose` use Faury's Voice lines. Only one is his own words; the rest are Board or company phrasing.
   - Financial commitments use Toepfer's register.
   - Never disclose internal long-term-plan targets [AX-0005]. Operating guidance can be a number, as with 2025 delivery guidance [AX-0053]. For EIS and rate, prefer windows and ranges (preference: inference).
5. **Thin profiles are guides, not scripts.** When a Toepfer or Wagner test, which are role-derived, drives a choice, say so in the rationale.
6. **Referee.** Judge fidelity against the Quick cards and the team rule. Do not penalise the player for behaviour the profiles mark as having no evidence.

## What would make these profiles comparable to Boeing's

Boeing's executive profiles rest on executives' own speaking turns in earnings calls and investor events (per `../../build/EXEC_SYNTH_BRIEF.md`). To reach the same footing for Airbus, add these sources, roughly in order of value:

1. **Airbus results-call transcripts:** full-year, H1, Q1 and 9M calls, 2019-2026, Faury and Toepfer in Q&A. These would give:
   - own-words priorities and thresholds (return hurdles, net-cash floor, launch criteria for the next single-aisle);
   - Toepfer's guidance style and a commitment track record (guided vs actual deliveries, EBIT Adjusted and FCF, year by year);
   - Faury's live reactions to Boeing's moves (MAX grounding, 777X slips, Boeing's new-airplane talk);
   - the full sentence naming the engine supplier behind the rate reset.
2. **H1 2026 (July 2026) and 9M 2026 calls, and the Farnborough 2026 briefings.** These would be Wagner's first own words as CEO Commercial Aircraft: rate, quality and supply-chain priorities.
3. **Board Reports or Universal Registration Documents for FY2019-FY2024.** The yearly CEO objectives, weights and scores would turn the single 2025-26 snapshot into a time series of what the Board paid for.
4. **Capital Markets Days, the Airbus Summit and annual results press conferences:** the NGSA technology gates and the widebody strategy in management's own words.
5. **For history:**
   - Enders-era results calls (about 2012-2019), including the February 2019 A380 decision;
   - Leahy's market-forecast and air-show briefings.

   These would make an `enders-leahy` "what if" team possible.

New transcripts should go through the reader pipeline (`../../build/EXEC_READER_BRIEF.md`, `exec_merge_evidence.py`). Each own-words item should be tagged by dimension, so that these profiles can be rebuilt to the same standard as Boeing's.

## Known evidence gaps (summary)

- **Unreadable lines:**
  - the two late-2025 technical issues are not named [AX-0056];
  - the engine supplier the Board names as the cause of the rate slip is cut off [AX-0054];
  - Wagner's arrival year is cut off [AX-0108];
  - the 2026 priority weights are read in printed order [AX-0073].
- **Pay-table conflict:** the table shows a 2025 STI of €1,582k against €2,925k earned for 2025 [AX-0076, AX-0066].
- **Item count:** the reader summary counted 111 items; the merged `evidence.jsonl` holds 109. These files use the file.
- **Reader findings that overreach their quotes** (the evidence files were not edited in this pass):
  - AX-0099 and A-0128 link Leahy's exit to Airbus's ethics issues; neither quote mentions ethics;
  - AX-0038 judges the A220 against a 2,000-aircraft figure that no quote contains;
  - AX-0084 reads the H140 result as a launch criterion.
- **Citation audit:** `citation_audit.md` (2026-10-03) lists the fixes, the claims relabelled as inference and the remaining gaps.
