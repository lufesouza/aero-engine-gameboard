# Spec: one agent per executive for the dash-2050 war game

## Goal

Today each company in the dash-2050 war game is played by ONE agent (`boeing-strategist`, `airbus-strategist`,
`cfm-strategist`, `pratt-whitney-strategist`, `rolls-royce-strategist`). That agent role-plays all three members of its
default executive committee (ExCo) inside one deliberation.

We are replacing that with ONE AGENT PER PERSON: 15 agents, three per company (CEO seat, CFO seat, operating seat). Each
is built from that person's own profile, which was compiled from their own words in earnings-call and investor-day
transcripts (Airbus: mostly the FY2025 Board Report filing).

Nothing is run now. We build the agent definitions and a profile page.

Repo root: /home/user/aero-engine-gameboard

## The 15 agents

The machine-readable list is in `data/people.json` next to this file. Use its evidence counts, date ranges and id ranges;
do not recount by hand.

| Company (side) | Team id (DEFAULT) | CEO seat | CFO seat | Operating seat |
|---|---|---|---|---|
| Boeing (`boeing`) | `ortberg-malave-pope-2026` | `boeing-ortberg` | `boeing-malave` | `boeing-pope` |
| Airbus (`airbus`) | `faury-toepfer-wagner-2026` | `airbus-faury` | `airbus-toepfer` | `airbus-wagner` |
| CFM/GE (`cfm`) | `culp-ghai-ali-2026` | `cfm-culp` | `cfm-ghai` | `cfm-ali` |
| Pratt & Whitney (`pratt_whitney`) | `calio-mitchill-eddy-2026` | `pratt-whitney-calio` | `pratt-whitney-mitchill` | `pratt-whitney-eddy` |
| Rolls-Royce (`rolls_royce`) | `erginbilgic-mccabe-watson-2026` | `rolls-royce-erginbilgic` | `rolls-royce-mccabe` | `rolls-royce-watson` |

Agent definition files will live at `.claude/agents/<agent-name>.md`.

## Sources to read for each person (all under wargame/profiles/<side>/)

- `executives/<file>.md`: the person's own profile. Header, Quick card (§2), commitment track record, sections by
  dimension, "In the game" (§5), and confidence and gaps (§6). For Eddy and Watson the file is `operations.md`; read
  only their section.
- `executives/evidence.jsonl`: the verified items. Use the person's `exec_id` (see `people.json`). For Culp, Ghai and
  Ali, also the `cfm_jv` items where they are the speaker.
- `executives/teams.md`: the default team's section (members, decision rule, tensions, ExCo script, thresholds).
- `executives/roles/<role>.txt`: the plain-text role card for the seat.
- `profile.md` (company doctrine, hard rules and red lines, reaction function), `objectives.md` §1 (the PD-briefing
  objective), `dashboard_game.md` (how the briefing moves map to the dash-2050 board, and how the hard rules apply).
- How the single company agent voiced this seat in the four dash-2050 rounds:
  `wargame/reports/dash-2050/record/record_r1.json` … `record_r4.json`, under `returned.<side>.exco.ceo|cfo|coo`
  and `returned.<side>.exco.decision_rule`. This is the earlier game's ROLE-PLAY, not evidence about the person; use it
  only for the "as voiced in dash-2050" field, and label it so.

## The round protocol the agents will follow (per company, each round)

The game master (GM) runs it. Executives see their own company's material only. Inside the ExCo, they see what the GM
passes them from colleagues. Notes are also stored in `/tmp/wargame-<side>/dash-2050/exco/`.

1. **Frame (CEO).** The CEO reads the round brief (`/tmp/wargame-<side>/dash-2050/roundN.md`) and writes a framing
   note:
   - the question this round;
   - the levers in play;
   - the options worth testing;
   - the red lines in force;
   - specific asks of the CFO and of the operating head;
   - an initial lean.
2. **Test (CFO and operating head, in parallel and independently).** Each reads the brief and the CEO's frame and
   writes a test memo:
   - their tests, each with a threshold, a pass or fail result, and the grid numbers used;
   - their recommended orders;
   - any veto they invoke, with its ground and whether the team rule makes it binding;
   - what would change their mind.
   At Pratt & Whitney the operating head (Eddy) also PROPOSES the engine orders, per the team rule.
3. **Decide (CEO).** The CEO reads both memos and decides by the team's decision rule. The CEO returns the company's
   orders, other moves, public statement and rationale, and records how each memo was weighed.
4. **Veto check (only the members the team rule gives a veto or sign-off).** Each reviews the CEO's orders and either
   concurs or invokes a veto on a ground the rule allows. The veto holders by team:
   - **Boeing.** Malave: his buffer test (the slip leg) on any plan. Pope's seat: the KPI doctrine against a Rate
     Increase under an inject (operations).
   - **Airbus.** Toepfer and Wagner hold soft vetoes: a failed test can be overridden only when the plan is at least
     $1B better than the best option that passes, and the override is recorded as a Board item. The five pillars
     cannot be overridden.
   - **CFM/GE.** Ghai on terms and capex; Ali on dates (test evidence). Both are vetoes only by inference.
   - **Pratt & Whitney.** Mitchill's payback and return gate on capital orders (four grounds). Eddy's technical vetoes:
     durability not proven before entry into service; parts and capacity short.
   - **Rolls-Royce.** McCabe's joint sign-off on any launch or aggressive terms, plus her balance-sheet vetoes. Watson's
     civil veto: compressed maturity, or an entry into service earlier than launch plus development time.
5. **Revise (CEO, only if a binding veto stands).** The CEO revises the orders once, within the veto, or overrides
   only where the team rule allows it, recording the override.

## Agent definition template (`agent_md`)

Write the WHOLE file: YAML front matter, then a system prompt in the second person. Plain, concrete English. Keep the
person's own wording in quotes with ids. Mark anything beyond the evidence as **(inference)**. Target length 160-260
lines.

```
---
name: <agent-name>
description: <Full name>, <title> at <company>: the <CEO|CFO|operating> seat of the `<team id>` executive committee in the Boeing vs Airbus war game (dash-2050 board). One of three per-executive agents for <company>; profiled from <N> items of <their own words in earnings-call and investor-day transcripts | the FY2025 Board Report and outside remarks>, <first>-<last>. Use it for <company>'s <frame and decide | test and veto-check> step of a dash-2050 round. Give it the run id, the round and the step.
tools: Bash, Read, Grep, Glob
---
```

Sections, in this order, using these exact headings:

1. `# <Full name> (<seat>, <company>)`. Two or three sentences:
   - who you are;
   - that you are one member of the ExCo, not the company;
   - that colleagues X and Y are separate agents;
   - that you decide and speak only as this person would.
2. `## Your record`. Role and dates as the sources show them. The evidence base: counts, date range, source types.
   Confidence overall and by area, as the profile states it.
3. `## What you are paid to protect`. The objective function, ranked, with ids.
4. `## How you decide`. Decision style, tempo, risk appetite, decision rules, with ids.
5. `## Your tests`. A table: | Test | Threshold or rule | Evidence |. These are the checks you apply every round, in
   dash-2050 terms where the profile or `dashboard_game.md` supports it.
6. `## Your vetoes and red lines`. What the team decision rule lets you block, how binding it is, and the company hard
   rules you personally enforce.
7. `## Your positions on the game's levers`. A table: | Lever | Your position | Evidence |. Cover the levers your seat
   touches on the dash-2050 board:
   - Boeing: fps 7- or 10-year, via Embraer, 737 rate, 787 Re-engine, engine code, cancel.
   - Airbus: NGSA, A350 Re-engine, Delay Tactics, engine code, cancel.
   - CFM/GE: ducted, Open Fan, Partner Embraer, lobbying, GEnx.
   - Pratt & Whitney: GTF2 solo or launch_if_selected, Joint Venture with RR.
   - Rolls-Royce: UltraFan NB solo or launch_if_selected, Joint Venture with P&W, UltraFan WB, Trent 1000 upgrade.
   Where the person has no evidence, say "No evidence: follow <colleague or company doctrine>".
8. `## How you read the rivals`. Only what the evidence supports; otherwise say there is none.
9. `## Your colleagues`. One line each on the other two members: the typical tensions from `teams.md`, and what you
   expect from them.
10. `## Biases to display`. With ids or **(inference)**.
11. `## Your voice`. Two or three sentences on how you speak. Then 4-8 signature lines, VERBATIM from
    `evidence.jsonl` (an exact substring of the item's `quote`), each with its id.
12. `## Where your record is thin`. The gaps from §6 of the profile. What to do when the evidence is silent: fall back
    to the company profile, or defer to a named colleague. Never invent a view.
13. `## Your files`. Exact repo paths:
    - own profile, role card, team section, company `profile.md`, `objectives.md` §1, `dashboard_game.md`,
      `evidence.jsonl` (grep by your exec_id);
    - the round brief at `/tmp/wargame-<side>/dash-2050/roundN.md` and `rules.md`;
    - the ExCo notes folder `/tmp/wargame-<side>/dash-2050/exco/`.
14. `## Your step in each round`. Your step(s) from the protocol above, with exactly what to produce.
15. `## Independence`. Rules:
    - Never read another company's files, wargame/runs, wargame/reports, wargame/dashgame or the board.
    - No `python3 -m wargame.engine` commands in dash-2050.
    - Use only numbers from your brief and your own profile.
    - What you know of the rivals is public bulletins plus your profile.
    - Inside the ExCo you see only what the GM passes you.
    - A hook enforces this.
16. `## What you return`. The JSON fields for your step(s), using the field lists below.
17. `## Language`. Say Do Nothing (never Milk), Re-engine, Joint Venture, Delay Tactics; fps, NGSA.

Return fields by step (the GM gives the JSON schema at run time; list the fields in the agent file):
- **frame:** `question, situation, levers_in_play, options_to_test, red_lines, asks_cfo, asks_ops, initial_lean, evidence_ids`
- **test:** `tests[{name, threshold, result, numbers, evidence_ids}], recommended_orders, proposal (only where the team rule names a separate proposer: P&W's operating head), vetoes[{plan, ground, binding, evidence_ids}], would_change_mind_if, memo` (memo of at most 250 words, in your voice)
- **decide / revise:**
  - `orders` (the company's order fields, as in the brief);
  - `other_moves[{move, public, detail}], public_statement, rationale, memo_weighing{cfo, ops};`
  - `expected_scenario, best_grid_plan_in_expected_scenario, premium_b, premium_reason, objective_note, predictions, expected_pv_b`
- **veto_check:** `concur, veto{ground, evidence_ids, binding}, red_line_breach, red_line, note` (a red-line flag is not a veto, but the CEO must strike the breach)

## Profile JSON (`profile`) for the HTML page

Exact keys:

```json
{
 "agent_name": "", "name": "", "side": "", "company": "", "seat": "CEO|CFO|Operating head", "title": "", "team_id": "",
 "role_dates": "as the sources show them, one sentence",
 "evidence": {"n_items": 0, "n_own_words": 0, "first": "", "last": "", "sources_note": "", "confidence_overall": "",
              "confidence_by_area": [{"area": "", "level": ""}]},
 "mandate": "one sentence: what this seat does in the ExCo",
 "objective_ranked": [{"text": "", "ids": [""]}],
 "decision_style": [{"text": "", "ids": [""], "inference": false}],
 "tests": [{"test": "", "threshold": "", "ids": [""], "inference": false}],
 "vetoes": [{"ground": "", "binding": "formal|soft|inference|none", "ids": [""]}],
 "lever_positions": [{"lever": "", "position": "", "ids": [""], "inference": false}],
 "rivals": [{"text": "", "ids": [""], "inference": false}],
 "colleagues": [{"name": "", "relation": ""}],
 "biases": [{"text": "", "ids": [""], "inference": false}],
 "voice": {"style": "", "quotes": [{"id": "", "quote": "", "date": "", "doc": "", "perspective": "own_words|filing|observed_by_boeing|observed_by_pratt_whitney"}]},
 "thin": {"gaps": [""], "fallback": ""},
 "dash2050_voiced": {"summary": "", "by_round": [{"round": 1, "line": ""}]},
 "protocol_steps": ["frame", "decide"],
 "veto_holder": true
}
```

- `ids` hold evidence ids (BX-, B-, AX-, A-, CX-, C-, PX-, P-, RX-, R-) as they appear in the profile files.
- `voice.quotes[].quote` MUST be an exact substring of that id's `quote` in `evidence.jsonl`. Copy `date`, `doc` and
  `perspective` from the item.
- Prefer `own_words` items. For Airbus, where few or none exist, you may use `filing` or `observed_by_*` items, but the
  `perspective` field must say so. In the agent file, label such lines "(Board Report, not his speech)" or "(as quoted
  by Boeing)".
- `dash2050_voiced.by_round` lines are short paraphrases (at most 30 words) of the earlier role-play for this seat,
  rounds 1-4.

## Evidence rules (strict)

- Use only the repo files listed. No web, no memory of these people beyond the files.
- Every factual claim about the person carries ids, or is marked as inference.
- Quotes are verbatim, character for character, from `evidence.jsonl`. Do not "clean up" quotes.
- Keep the profile's own confidence labels. Where a profile says Low or Very low, say so prominently, and make the
  fallback rule explicit.
- Airbus: the evidence is mostly Board Report filings, not transcripts. Faury has 1 own-words line, Toepfer and Wagner
  none. Say so, and never present filing text as the person's speech: those items have perspective `filing`.
- Do not copy the single-agent strategist instructions about `wargame.engine`.
