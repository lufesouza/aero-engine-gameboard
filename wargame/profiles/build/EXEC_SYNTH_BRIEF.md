# Synthesis brief: executive profiles and leadership teams

You write war-game profiles of **individual executives** and of the **leadership teams** they formed, for Boeing or for Airbus. A company's player agent (`boeing-strategist` or `airbus-strategist`) reads the profiles of the team it is given. It then:
- runs an executive-committee deliberation each turn;
- decides as that team would have decided;
- speaks in the team's voice.

The referee uses the same profiles to judge fidelity.

## Scope and fairness

These are profiles of **professional conduct**, drawn only from what each person said and did as an executive: their priorities, decisions, reasoning, commitments and how they turned out, and their reactions to events.
- No private life, health, family or appearance.
- No speculation about character beyond what the words support.
- Describe misjudgements factually, with dates and outcomes, and give the counter-evidence where it exists.
- Each profile must be something its subject would recognise as a fair, evidence-based account of how they ran the business.

## Inputs (paths in your task)

- **The executive evidence** (ids `BX-####` for Boeing, `AX-####` for Airbus): verbatim quotes from the person's own speaking turns, each tagged with a dimension (priorities, decision_style, risk_appetite, capital_allocation, product_strategy, operations, rival_view, communication, credibility, crisis_response, team).
- **The company evidence** (`B-####` / `A-####`): items whose `speaker` is the person, plus company context.
- **The reader summaries.**
- **The company profile** (`wargame/profiles/<company>/profile.md`): the company's doctrine and reaction function. Individual profiles say how the person **differs from or sharpens** the company doctrine. They do not repeat it.
- **The game rules:** `python3 -m wargame.engine rules` (levers, turns, engine numbers).

## Output 1: one file per executive, `wargame/profiles/<company>/executives/<exec_id>.md`

Target 1,500-3,000 words. Profiles with thin evidence are shorter and say so. Structure:

1. **Header.** Role(s) and dates as shown in the sources. Era context: what they inherited and what happened on their watch. Evidence base (number of items and events), and a confidence level.
2. **Quick card** (what the player reads every turn):
   - **Objective function**: ranked priorities in the person's own terms, with ids.
   - **Decision rules and red lines**, e.g. "no new airplane until…", "no equity", "rates only on KPIs".
   - **Risk appetite**: technology, schedule, balance sheet, fixed-price. Rate each Low / Medium / High with one line of evidence.
   - **Tempo**: how fast they move after a rival's move; deny-then-reverse or act first.
   - **Capital allocation stance.**
   - **Product stance**: clean sheet vs derivative, the business case, Joint Ventures, engines.
   - **How they read Airbus.**
   - **Voice**: 3-6 characteristic phrasings, quoted with ids, to use in public statements.
   - **Biases to display when the situation matches.**
3. **Commitment track record.** A table: date | commitment or forecast | outcome (if the evidence shows it) | ids. Be precise and neutral.
4. **Sections by dimension**, with an era timeline where views shifted:
   - priorities;
   - decision style;
   - risk;
   - capital allocation;
   - product and strategy;
   - operations;
   - rivals;
   - communication;
   - crisis response;
   - team.
5. **In the game: if this person is in the room.** For each war-game lever, what this person pushes for, what they veto, and the evidence. The levers are:
   - fps launch timing, Solo vs Joint Venture;
   - 787 Re-engine / A350 Re-engine;
   - Rate Increase;
   - cancel;
   - engine choice;
   - disclosure;
   - Delay Tactics and Poaching (Airbus).

   Then: how they argue in the executive-committee deliberation (the questions they ask, and the numbers they want from `options` and `whatif`), and what changes their mind.
6. **Confidence and gaps.**

## Output 2: `wargame/profiles/<company>/executives/teams.md`

The leadership teams by era. Each team has an id: Boeing, e.g. `mcnerney-bell-2010`, `muilenburg-smith-2016`, `calhoun-west-2023`, `ortberg-malave-2026`; Airbus, `faury-toepfer-wagner-2026`. For each team give:
- **Members and roles.**
- **The decision rule:** who proposes, who can veto, and on what.
- **Typical tensions**, e.g. CEO ambition against CFO cash.
- **How the team turned the company doctrine into decisions in its era**, with ids.
- **A per-turn ExCo deliberation script** of 4-6 steps: CEO frames → CFO tests cash, debt and hurdle → COO/BCA tests production, quality and supply chain → decide by the team rule. Include tie-breaks and the thresholds each member applies, in engine terms where possible.
- **A short "how this team differs from the company default"** note.

Mark the current team as the default for the 2026 game. Explain that historical teams are "what if this team ran the company today" options.

## Output 3: `wargame/profiles/<company>/executives/README.md`

An index of executives (role, dates, evidence count, confidence) and teams, and how the player uses them.

## Rules

- Cite ids inline for every behavioural or numerical claim: `[BX-0123]`, `[B-0456]`.
- Check with:

  ```
  cd <repo> && python3 wargame/profiles/build/cite_check.py <file> wargame/profiles/<company>/executives/evidence.jsonl wargame/profiles/<company>/evidence.jsonl
  ```

  The result must show 0 missing.
- Label inferences **(inference)**. Analysts' assertions are not the executive's views.
- Use house naming: "Do Nothing" (never "Milk"), "Re-engine", "Joint Venture", "Delay Tactics" (never "Sabotage"), fps, NGSA.
- **Isolation:** Boeing builders never read Airbus executive or company material, and vice versa.
