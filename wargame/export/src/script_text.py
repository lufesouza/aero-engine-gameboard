"""Text of the portable pack (GAME_SCRIPT.md, the company kits, README.md, RESULTS_AS_PLAYED.md), filled from the
game's own sources by build_llm_pack.py. The round protocol mirrors wargame/dashgame/workflows/exco_round.js as it ran
for dash-2050-cons (args: run, round, year, sides, plans; no `objectives` argument, so the step prompts carry no
objective note: Control's objectives reach each company through its brief, section 2)."""
import json

SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAMES = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
SEAT_TITLE = {"ceo": "CEO", "cfo": "CFO", "ops": "operating head", "board": "Board"}
YEARS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}


# ───────────────────────────── output formats ─────────────────────────────
def _skeleton(schema, indent=0):
    """A JSON-like skeleton of a schema: strings as "…", enums as "a | b | c", arrays as [ … ]."""
    pad = " " * indent
    t = schema.get("type")
    if "enum" in schema:
        return " | ".join("null" if v is None else str(v) for v in schema["enum"])
    if t == "string":
        return "text"
    if t == "number":
        return "number"
    if t == "boolean":
        return "true | false"
    if t == "array":
        inner = _skeleton(schema["items"], indent + 2)
        return "[ " + inner + " , … ]" if "\n" not in inner else "[\n" + pad + "  " + inner + "\n" + pad + "  , …\n" + pad + "]"
    if t == "object":
        req = set(schema.get("required", []))
        lines = []
        for k, v in schema.get("properties", {}).items():
            lines.append(pad + "  %s%s: %s" % (k, "" if k in req else " (optional)", _skeleton(v, indent + 2)))
        return "{\n" + "\n".join(lines) + "\n" + pad + "}"
    return "value"


def _generic_orders(sc):
    sc = json.loads(json.dumps(sc))
    for k in ("orders", "recommended_orders"):
        if k in sc.get("properties", {}):
            sc["properties"][k] = {"type": "object", "properties": {"<every order field of your company, section 4>": {"enum": ["one value"]}}, "required": ["<every order field of your company, section 4>"]}
    return sc


def formats(consts, side):
    s = consts["schemas"]
    return [("Board guidance (step 0)", s["guidance"]), ("CEO framing note (step 1)", s["frame"]),
            ("Test memo, CFO and operating head (step 2)", s["test"][side]),
            ("CEO decision (steps 3, 5 and 7)", s["decide"][side]), ("Veto check (step 4)", s["veto"]),
            ("Board review or confirmation (steps 6 and 8)", s["review"])]


def formats_md(consts, side):
    out = []
    fm = formats(consts, side or "boeing")
    if side is None:                      # generic: the orders block is the company's own (section 4)
        fm = [(t, _generic_orders(sc)) for t, sc in fm]
    for title, sc in fm:
        out.append("**%s**\n\n```\n%s\n```" % (title, _skeleton(sc)))
    return "\n\n".join(out)


# ───────────────────────────── protocol ─────────────────────────────
def head_exec(company, name, rule, current):
    return (
        "War game dash-2050-cons, round {N} (decision year {YEAR}). Your step: **{STEP}**.\n\n"
        f"You are {name} of {company}. Follow your persona: \"Your step in each round\", \"Your tests\", "
        "\"Your vetoes and red lines\", \"Your voice\".\n\n"
        "Your materials: this round's brief (the public bulletin followed by your company's private brief) and the public "
        "rules. Round 1: this is the first round, there are no earlier notes or orders. Later rounds: your company's ExCo "
        "and Board notes from earlier rounds and your sealed orders, as the game master kept them.\n\n"
        f"Your ExCo's decision rule: {rule}\n\n"
        "Use only numbers from your brief and your own company's profile. Read nothing of another company; what you know "
        "of the rivals is the public bulletin and your profile."
        + (f"\n\n{current}" if current else ""))


def head_board(board_name, names, rule, current):
    return (
        "War game dash-2050-cons, round {N} (decision year {YEAR}). Your step: **{STEP}**.\n\n"
        f"You are {board_name}. Follow your persona: \"Your step in each round\", \"Your culture\", \"Your tests\", "
        "\"Your veto and its limits\", \"Your recommendations\".\n\n"
        "Your materials: this round's brief and the public rules; in later rounds, the ExCo's and your notes from earlier "
        "rounds and the sealed orders.\n\n"
        f"The ExCo is {names['ceo']} (CEO), {names['cfo']} (CFO) and {names['ops']} (operating head). Its decision rule: {rule}\n\n"
        "Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. "
        "You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.\n\n"
        "Use only numbers from your brief and your own company's files. Read nothing of another company."
        + (f"\n\n{current}" if current else ""))


def protocol_md(consts, side=None):
    """The nine steps for one company (or, with side None, for any company: role words instead of names, the veto
    grounds in section 5), with the task text of each step as the original game gave it."""
    if side is None:
        names = {"ceo": "the CEO", "cfo": "the CFO", "ops": "the operating head"}
        cfo, ops = "the CFO", "the operating head"
        vc = vo = "see section 5, company by company"
        prop = ("\n   - Pratt & Whitney only: the operating head also receives *Per the team rule you also PROPOSE the engine "
                "orders: put them in `recommended_orders` and explain them in `proposal`.*")
        return _protocol_text(names, cfo, ops, vc, vo, prop, generic=True)
    t = consts["TEAMS"][side]
    names = t["names"]
    cfo, ops = names["cfo"], names["ops"]
    vc, vo = t["veto"]["cfo"]["ground"], t["veto"]["ops"]["ground"]
    proposes = t.get("proposes")
    prop = ("\n   - " + ops + " also receives: *Per the team rule you also PROPOSE the engine orders: put them in "
            "`recommended_orders` and explain them in `proposal`.*") if proposes == "ops" else ""
    return _protocol_text(names, cfo, ops, vc, vo, prop)


def _protocol_text(names, cfo, ops, vc, vo, prop, generic=False):
    cfo_t, ops_t = ("", "") if generic else (", CFO", ", operating head")
    return f"""**Step 0. Board guidance** (the Board). Task: *Give the ExCo your guidance for this round: your priorities, your
risk appetite this round, what you expect to see in the package, what you would approve and what you would veto, and
your recommendations. It does not bind; your veto comes at the review.*

**Step 1. Frame** ({names['ceo']}{'' if generic else ', CEO'}). Receives the Board's guidance. Task: *The Board's guidance for this round
(non-binding; its veto comes after your decision): [guidance]. Write the framing note for your ExCo: the question this
round, the levers in play, the options worth testing, the red lines in force, what you ask of your CFO and of your
operating head, and your initial lean. Your colleagues see only what you return here.*

**Step 2. Test** ({cfo}{cfo_t}, and {ops}{ops_t}: separately; neither sees the other's memo). Each receives
the CEO's framing note and the Board's guidance. Task: *Test it independently: you do not see your colleague's memo.
Apply your own tests with thresholds and the grid numbers you used, give your recommended orders, and state any veto
with its ground and whether the team rule makes it binding (your veto: [ground]). Memo of at most 250 words, in your
voice.*
   - {cfo[0].upper() + cfo[1:]}'s veto ground: {vc}.
   - {ops[0].upper() + ops[1:]}'s veto ground: {vo}.{prop}

**Step 3. Decide** ({names['ceo']}). Receives the framing note, the Board's guidance and both memos. Task: *Decide by
the team rule. Return the company's sealed orders (one value per field), other moves, the public statement, the
rationale, and how you weighed each memo. Any override of a colleague's veto goes in `overrides` and must be allowed
by the rule. Answer each of the Board's recommendations in `board_response`: how you took it up, or why not. Every
order that differs from the default goes to the Board, which can veto it.*

**Step 4. Veto check** ({cfo} and {ops}, separately). Each receives its own test memo and the CEO's decision. Task:
*Concur, or invoke a veto only on a ground the team rule gives you: [ground]. Set `veto.binding` true only if, under
the rule, the CEO must revise within it (or record an allowed override). Separately, if the orders break a company
hard rule (a red line), set `red_line_breach` true and name the rule in `red_line`: that is not a veto, but the CEO
must strike the breach.*

**Step 5. Revise** ({names['ceo']}; only if a veto check returned `concur: false` with `veto.binding: true`, or any
`red_line_breach: true`). Receives the decision and the binding vetoes and red-line flags. Task: *Revise your orders
once. Stay within each binding veto, or override only where the team rule allows it and record each override in
`overrides`. Strike every flagged red-line breach you confirm (red lines are never traded for PV); if you judge a flag
mistaken, keep the order and say why in `rationale`.* The revision replaces the decision.

**Step 6. Board review** (the Board; only if there are Board items). Board items are the order fields, other than
engine codes, whose value differs from the default (see below). With no Board items the review is an automatic
approval ("No Board items: every order is the default"). Receives its guidance, the ExCo's package (framing note,
both test memos, the decision, the veto checks and any revision) and the submitted orders. Task: *The Board items:
[fields]. For each, approve or veto, with the ground and evidence; for a veto you may name acceptable alternatives
(other values of that order field, or the default). Then your recommendations.* If no review comes back, every Board
item reverts to its default (fail closed).

**Step 7. Board revise** ({names['ceo']}; only if the Board vetoed an item). Receives the submitted orders and the
Board's review. Task: *The Board vetoed: [fields]. Revise once, within the Board's veto: for each vetoed order choose
an alternative the Board named, or the default. Keep the approved orders. Answer the Board's recommendations in
`board_response`.* The game master keeps every approved order as submitted and takes only the vetoed fields (with
their engine code) from the revision.

**Step 8. Board confirm** (the Board; only if a vetoed field was revised to a value other than its default). Receives
its guidance, the package, its review, the CEO's revision and the merged orders. Task: *The revised Board items:
[field = value]. Approve or veto each (an alternative you named should pass unless something changed). A still-vetoed
item reverts to the default.*

**Result.** The company's sealed orders are the merged orders after step 8; its `public_statement` and `other_moves`
come from the CEO's latest output (step 7, else step 5, else step 3)."""


def team_md(consts, side):
    t = consts["TEAMS"][side]
    cur = consts["CURRENT"].get(side)
    return (f"- **Executive committee:** {t['names']['ceo']} (CEO), {t['names']['cfo']} (CFO), {t['names']['ops']} "
            f"(operating head). **Board:** {t['boardName']}.\n"
            f"- **Decision rule:** {t['rule']}\n"
            f"- **CFO veto ground:** {t['veto']['cfo']['ground']}.\n"
            f"- **Operating head veto ground:** {t['veto']['ops']['ground']}.\n"
            + (f"- **Proposes the engine orders:** the operating head ({t['names']['ops']}).\n" if t.get("proposes") == "ops" else "")
            + (f"- **Board figures (given to every {NAMES[side]} seat):** {cur}\n" if cur else ""))


def defaults_md(consts):
    rows = []
    for side in SIDES:
        f = consts["ORDER_FIELDS"][side]
        rows.append("| %s | %s |" % (NAMES[side], "; ".join("`%s`: %s" % (k, ", ".join("`%s`" % ("null" if v is None else v) for v in vals))
                                                            for k, vals in f.items())))
    return ("| Company | Order fields and values (the first value is the default) |\n|---|---|\n" + "\n".join(rows) +
            "\n\nTwo fields are standing supply plans rather than moves: Boeing's `fps_site` and Airbus's `a320_plan`. "
            "Their default is the company's current plan (at the start: `new_site` and `base`), which the brief and the "
            "engine's orders template show. Keeping the current plan is not a Board item; changing it is, and a vetoed "
            "change reverts to the current plan. Engine codes (`fps_engine_code`, `ngsa_engine_code`) are `null` or "
            "1-7 and ride with their launch: they are never a Board item on their own, and when a launch reverts, its "
            "code reverts with it.")


def steps_table_md():
    return """| Step | Who | Receives (and nothing else from this round) |
|---|---|---|
| 0 Guidance | Board | brief, rules, its earlier notes |
| 1 Frame | CEO | brief, rules, Board guidance, earlier notes |
| 2 Test | CFO; operating head (separately) | brief, rules, CEO's frame, Board guidance |
| 3 Decide | CEO | frame, guidance, both test memos |
| 4 Veto check | CFO; operating head (separately) | own test memo, CEO's decision |
| 5 Revise | CEO (if needed) | decision, binding vetoes, red-line flags |
| 6 Review | Board (if Board items) | guidance, ExCo package, submitted orders |
| 7 Board revise | CEO (if a Board veto) | submitted orders, Board review |
| 8 Confirm | Board (if a revised item) | guidance, package, review, revision, merged orders |"""


# ───────────────────────────── GAME_SCRIPT.md ─────────────────────────────
def game_script(ctx):
    c = ctx["consts"]
    teams = "\n\n".join("### %s\n\n%s" % (NAMES[s], team_md(c, s)) for s in SIDES)
    protocols = ("## The nine steps\n\n" + protocol_md(c) + "\n\n## Output formats\n\nThe same for every company; `orders` and "
                 "`recommended_orders` hold the company's own order fields (section 4), one value each. `evidence_ids` "
                 "list the evidence ids the seat relies on (the ids its persona or company files cite); they may be empty.\n\n" + formats_md(c, None))
    doctrine = "\n\n".join("### %s\n\n%s" % (NAMES[s], ctx["doctrine"][s]) for s in SIDES)
    cards = "\n\n".join("## %s\n\n%s" % (NAMES[s], "\n\n---\n\n".join(_demote(ctx["cards"][a], 2) for a in ctx["agents"][s])) for s in SIDES)
    return f"""# Boeing vs Airbus, 2030-2050: the war game "dash-2050-cons", scripted for any LLM

This script lets an LLM (ChatGPT, Gemini, Claude or another) replay the five-player war game that was played as run
`dash-2050-cons`: Boeing and Airbus (airframers) and the engine makers CFM/GE, Pratt & Whitney and Rolls-Royce, over
four decision rounds (2030, 2035, 2045, 2050). In the original, each company was played by four AI agents (a CEO, a
CFO, an operating head and the Board of Directors), each built from the real executives' and directors' public record,
and a game master ran every round on an economic engine (the narrowbody/widebody game-theory dashboard with a
supply-and-demand layer). This script carries all of it: the rules, the round protocol word for word, the twenty
personas, each company's doctrine, and the engine itself (folder `engine/`, Python).

**Do not open `RESULTS_AS_PLAYED.md` or `engine/reference/` until the game is over** (the game master may use
`engine/reference/` in set-up C below; see 1.6). They hold what the original players did.

## Contents

1. Game master's script: set-ups, round checklist, isolation, adjudication, scoring
2. The game in one page
3. The public rules (every player's text, verbatim)
4. Orders, defaults and Board items
5. The five companies' executive committees: decision rules and veto grounds
6. The round protocol, with the output formats
7. Company doctrine (each company's own rules for this game)
8. The twenty personas

---

# 1. Game master's script

You are the **game master (GM)**. You run the game; you do not play it. You are neutral, you never advise a company,
and you never reveal one company's private material to another.

## 1.1 Choose a set-up

| Set-up | What you need | Fidelity |
|---|---|---|
| **A. Six chats + code** (recommended) | One chat for the GM with code execution (upload `engine/`); one chat per company, each given its kit `kits/COMPANY_<company>.md` (and, if the LLM takes files, the company folder `companies/<company>/`) | Closest to the original: each company sees only its own material |
| **B. One chat + code** | One chat with code execution; upload the whole pack | The engine is exact; isolation is by discipline (1.4) |
| **C. One chat, no code** | This script and `engine/reference/briefs/` | Round 1 is exact; later rounds are exact only while every order matches the original game (1.6) |

The engine needs Python 3.9 or later with numpy and pandas (ChatGPT's and Gemini's code tools have them; plotly is
optional). From the `engine/` folder:

```
python3 play.py selftest                         # first: checks the engine reproduces the original game (about 20 s)
python3 play.py new mygame                       # start a game at the 2030 position
python3 play.py brief mygame 1                   # round 1: public bulletin + one private brief per company
python3 play.py orders-template mygame 1         # an orders file to fill in (defaults and the legal values)
python3 play.py adjudicate mygame 1 orders.json  # adjudicate (or: ... boeing.json airbus.json ...); prints every value
python3 play.py status mygame                    # values after the last round
```

Briefs are written to `engine/runs/mygame/players/<company>/round<N>.md` (the bulletin followed by that company's
private brief). Company keys: `boeing`, `airbus`, `cfm`, `pratt_whitney`, `rolls_royce`.

## 1.2 Each round (N = 1 to 4; years 2030, 2035, 2045, 2050)

1. **Brief.** Run `brief mygame N`. Give each company only its own `players/<company>/roundN.md`. (Round 1 also: the
   public rules, section 3, to every company.)
2. **Play each company's round** by the protocol in section 6: steps 0-8, from Board guidance to Board confirmation.
   The five companies play independently and at the same time: nothing of one company's deliberation reaches another.
   - Set-up A: in the company's chat, send: *"Round N (year YYYY). Your brief follows. Run steps 0 to 8 by your kit
     and end with your orders block."* followed by the whole of its `roundN.md`. In round 2 and later, also tell it
     if the engine adjusted any of its orders (its brief says so too).
   - Set-ups B and C: run the steps yourself, one seat at a time (1.4).
3. **Collect the sealed orders** in the shape of `orders-template` (per company: `orders`, `public_statement`,
   `other_moves`): one file for all five, or each company's final block (`{{"boeing": {{...}}}}`) in its own file. One
   value per order field; an engine code is JSON `null` or an integer 1-7. A company with no block holds everything.
4. **Adjudicate.** Run `adjudicate mygame N orders.json`. The engine validates every order (an illegal value
   becomes hold and is reported to that company privately), applies the moves, and values every company.
5. **Publish.** The next round's bulletin (written by `brief mygame N+1`) carries the public events, every public
   statement and the public other moves. Each company's private brief tells it if its orders were adjusted.
6. **Keep each company's notes** (its nine steps and its sealed orders) and give them back only to that company in
   later rounds.

After round 4, run `status mygame`, then compare with `RESULTS_AS_PLAYED.md` (1.7).

## 1.3 What is public and what is private

Public: launches, cancellations, entry-into-service and engine-ready dates; engine selections and the engines
fitted; Joint Venture commitments; each company's public statement and its other moves marked public; observed
market shares and deliveries up to the decision year. Private: everything else, including each company's payoff grid,
finances, orders not yet public, rationale and predictions. Delay Tactics are covert: never published, revealed only
at the end. The engine's bulletin applies these rules; never add to it.

## 1.4 Playing the seats yourself (set-ups B and C)

Play one seat at a time, in step order, and keep strictly to what that seat receives (table below). Before each step,
state the seat and the step; write the output in that step's format (section 6); then stop being that seat. A CFO
never sees the operating head's memo before the veto check, a Board never sees another company's anything, and no
seat uses a number that is not in its company's brief or profile. When you play a seat, take its persona (section 8)
and its company doctrine (section 7) as binding: its tests, thresholds, vetoes, red lines and voice.

{steps_table_md()}

## 1.5 Adjudication rules you apply yourself

- **Board items and reverts** (section 4): every non-default order field is a Board item; a vetoed item takes the
  CEO's revised value (an alternative the Board named, or the default); a still-vetoed item after step 8 reverts to
  the default, with its engine code.
- **Binding vetoes inside the ExCo** follow each company's decision rule (section 5): Boeing, Pratt & Whitney and
  Rolls-Royce vetoes bind; Airbus's are soft (the CEO may override for a plan at least $1B better on the grid than the
  best option that passes, recorded as a Board item; a five-pillars breach is binding); CFM/GE's tests bind unless the
  CEO answers them with evidence (an inference in the original).
- **A missing or malformed step**: a company with no result for the round holds everything (all defaults).
- **Everything else is the engine's**: legality, timing, engine selection, market shares, deliveries, values.

## 1.6 Set-up C: no code execution

`engine/reference/briefs/round1_<company>.md` are the exact round-1 briefs (the starting position is fixed). Open
nothing else in `engine/reference/` yet: the later briefs and bulletins show what the original players did. After
round 1, compare the sealed orders with `engine/reference/played_orders.json` (GM only, never shown to a company). If
every company's orders match the original round exactly (order fields only; statements may differ), the original's
round-(N+1) briefs in `engine/reference/briefs/` are exact and the values after the round are those in
`played_orders.json`; continue. If any order differs, the original briefs no longer apply: either move to set-up A or
B for the engine, or continue in estimate mode, valuing each company from its own brief's payoff grid (the column
closest to what its rivals did) and saying in every bulletin that the values are estimates.

## 1.7 Scoring and debrief

- Each company's score is its ΔPV ($B, present value at 2026, against the status quo in which nobody launches
  anything) and its yield (100 + ΔPV ÷ enterprise value × 100), as the engine reports after each round.
- At the end, reveal Delay Tactics if any were ordered, then compare with `RESULTS_AS_PLAYED.md`: the original
  players' orders, values and reasons. Useful comparisons: which decisions differ and why; each company's value
  against the original; whether the same tests decided the same way.

---

# 2. The game in one page

- **Players:** Boeing, Airbus, CFM/GE (CFM International with GE's widebody engines), Pratt & Whitney (RTX), Rolls-Royce.
- **Rounds:** 2030, 2035, 2045, 2050. Sealed, simultaneous orders; a bulletin after each round.
- **The big choices:** Boeing's new narrowbody (fps: 7-year or 10-year ramp, or via Embraer; at new sites or at
  Renton), the 737 Rate Increase (2030 only), the 787 Re-engine; Airbus's NGSA (with its A320 base or Alt production
  plan), the A350 Re-engine, covert Delay Tactics; the engine makers' new engines (CFM ducted and Open Fan, P&W GTF2,
  Rolls-Royce UltraFan narrowbody and widebody, the P&W-Rolls-Royce Joint Venture), upgrades and partnerships; and the
  engine selections on the new narrowbodies.
- **This game's settings** (all built into the engine and the briefs):
  - board: the combined narrowbody/widebody dashboard, version 3 (fps 7-year $65.00B and 10-year $60.32B at EIS,
    NGSA $35.52B, unlaunched Re-engines at 2042, the EIS-lead share rule);
  - supply and demand on: the narrowbody market is limited by the factories; demand is a conservative case with the
    firm orders as its first slice; Boeing loses 1 point of preference a year from NGSA's entry into service while it
    has no new narrowbody in service, but never below the share Airbus cannot supply; Airbus adds 1% capacity a year
    when it is short;
  - Control's objectives (set "control2"): Boeing must repair its balance sheet and secure a stable engine supply;
    Airbus wants a stable engine supply; Rolls-Royce must protect its widebody cash cow. They are measured in each
    company's brief (section 2) and never change the payoff.
- **Payoffs:** ΔPV against the status quo, $B, discounted to 2026 at each company's cost of capital; every company
  sees its own grid of plans against rival scenarios in its brief.

---

# 3. The public rules (verbatim)

{_demote(ctx['rules_md'], 1)}

---

# 4. Orders, defaults and Board items

{defaults_md(c)}

---

# 5. The five companies' executive committees

{teams}

---

# 6. The round protocol

Each company plays the same nine steps; only the names, the decision rule and the veto grounds change (section 5). Every seat's
task text below is the one the original game gave it. Each seat is also told: the round and its step; to follow its
persona's "Your step in each round", "Your tests", "Your vetoes and red lines" (Board: "Your culture", "Your veto and
its limits", "Your recommendations") and "Your voice"; its company's decision rule; to use only numbers from its brief
and its own company's profile; and (Boeing and Airbus seats) the Board figures in section 5. Board seats are also told
that every non-default order is a Board item, that they approve or veto each one and recommend, and that they never
originate orders or veto a hold.

{steps_table_md()}

{protocols}

---

# 7. Company doctrine

Each company's doctrine as its players had it: the quick card of its behavioural profile (its hard rules and
reaction function), then its mapping to this game ("the dashboard war game"). The quick cards were written for an
earlier version of the game, with turns from 2026 and another engine; the mapping that follows each one says what
still applies here and governs where they differ. Where a figure differs from the brief or from section 5, the brief
and section 5 govern. Tags such as [NOW], [HIST], [ENGINE] and [RULES] mark the kind of source.

{doctrine}

---

# 8. The twenty personas

Each persona condenses the agent definition the original game used; the full definitions are in `personas_full/`
and each company's source files in `companies/`.

{cards}
"""


def _demote(md, by=1):
    """Push every markdown heading down `by` levels so a document nests under this script's headings."""
    out = []
    fence = False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("#"):
            line = "#" * by + line
        out.append(line)
    return "\n".join(out)


# ───────────────────────────── company kits ─────────────────────────────
def company_kit(ctx, side):
    c = ctx["consts"]
    t = c["TEAMS"][side]
    full = "\n\n---\n\n".join(_demote(ctx["full"][a], 2) for a in ctx["agents"][side])
    return f"""# {NAMES[side]}: company kit for the war game dash-2050-cons

You are **{NAMES[side]}** in a five-player war game (Boeing, Airbus, CFM/GE, Pratt & Whitney, Rolls-Royce) over
four rounds: 2030, 2035, 2045, 2050. In this chat you play your company's four decision-makers in turn: the Board
({t['boardName']}), {t['names']['ceo']} (CEO), {t['names']['cfo']} (CFO) and {t['names']['ops']} (operating head).
A game master (GM) runs the game in another chat. You never see another company's brief, payoffs, deliberation or
orders; what you know of the rivals is the public bulletin and your profile.

## How this chat works

1. Each round the GM pastes your brief: the public bulletin followed by {NAMES[side]}'s private brief.
2. Run the nine steps below in order, one seat at a time. Before each step write a heading "Step k: <seat>", play
   only that seat, using only what that seat receives (the table), and write the step's output in its format. A CFO
   or operating head tests independently of the other.
3. End the round with one block for the GM:

```json
{{"{side}": {{"orders": {{ one value per order field }}, "public_statement": "...", "other_moves": [ {{"move": "...", "public": true, "detail": "..."}} ]}}}}
```

4. The GM adjudicates all five companies and pastes the next round's brief, which also tells you if any of your
   orders were adjusted. Keep your earlier rounds' notes in this chat: later rounds may use them.

If your LLM accepts files, the GM may also give you the folder `companies/{side}/` (your company's profile, objectives,
doctrine, analyst-model baseline, executive and Board profiles and evidence). Your personas cite those files; where a
persona points to a file you do not have, follow its card's own statement of the rule.

## Your company's decision rule

{team_md(c, side)}

## The nine steps

{steps_table_md()}

{protocol_md(c, side)}

## Output formats

{formats_md(c, side)}

## Your orders

{_orders_for(c, side)}

## The public rules (every player has the same text)

{_demote(ctx['rules_md'], 2)}

## Your company doctrine

The quick card of your behavioural profile, then its mapping to this game ("the dashboard war game"). The quick card
was written for an earlier version of the game, with turns from 2026; the mapping says what still applies here and
governs where they differ. Where a figure differs from your brief{' or from the Board figures above' if side in ('boeing', 'airbus') else ''}, {'those govern' if side in ('boeing', 'airbus') else 'your brief governs'}.

{ctx['doctrine'][side]}

## Your four personas (the original agent definitions)

{full}
"""


def _orders_for(c, side):
    f = c["ORDER_FIELDS"][side]
    lines = ["- `%s`: %s" % (k, ", ".join("`%s`" % ("null" if v is None else v) for v in vals)) for k, vals in f.items()]
    return ("One value per field; the first value listed is the default (keep). Your brief lists which values are legal "
            "this round.\n\n" + "\n".join(lines) +
            ("\n\n`fps_site` is your standing supply plan: its default is your current plan." if side == "boeing" else "") +
            ("\n\n`a320_plan` is your standing supply plan: its default is your current plan." if side == "airbus" else "") +
            "\n\nEvery order that differs from its default is a Board item (engine codes ride with their launch).")


# ───────────────────────────── results and README ─────────────────────────────
def results_md(ctx):
    pl, dec = ctx["played"], ctx["decisions"]
    rows = []
    for n in ("1", "2", "3", "4"):
        r = pl["rounds"][n]
        for s in SIDES:
            o = r["orders_file"][s]["orders"]
            nd = {k: v for k, v in o.items() if v not in ("hold", "none", None) and not (k == "fps_site" and v == "new_site")}
            rows.append("| %s (%d) | %s | %s | %+.2f |" % (n, r["year"], NAMES[s], ", ".join("`%s`: `%s`" % kv for kv in nd.items()) or "hold everything",
                                                          r["value"][s]))
    reasons = []
    for n in ("1", "2", "3", "4"):
        reasons.append("### Round %s (%d)\n" % (n, pl["rounds"][n]["year"]))
        reasons.append("Events: " + ("; ".join(pl["rounds"][n]["log"]) or "none") + ".\n")
        for s in SIDES:
            d = dec[n][s]
            ex = d.get("exco") or {}
            br = ex.get("board_review") or {}
            reasons.append("**%s.** Expected scenario: %s Best grid plan in it: %s Premium: %s. Board: %s%s.\n\n"
                           "Public statement: \"%s\"\n" % (
                               NAMES[s], _one(d.get("expected_scenario")), _one(d.get("best_grid_plan_in_expected_scenario")),
                               "$%.2fB" % d["premium_b"] if isinstance(d.get("premium_b"), (int, float)) else "none",
                               br.get("overall", "no review"),
                               (", vetoed " + ", ".join(ex.get("board_vetoed") or [])) if ex.get("board_vetoed") else "",
                               (d.get("public_statement") or "").strip()))
    fin = pl["rounds"]["4"]["value"]
    return f"""# dash-2050-cons as played (spoiler: open only after your replay)

The original game, played on 14 October 2026 by twenty AI agents (an executive committee and a Board for each
company) with the game master's engine. Values are ΔPV against the status quo, $B, present value at 2026.

## Final values (after round 4, 2050)

| Company | ΔPV ($B) |
|---|---|
""" + "\n".join("| %s | %+.2f |" % (NAMES[s], fin[s]) for s in SIDES) + f"""

## Orders each round (non-default fields) and value after the round

| Round | Company | Orders | ΔPV after the round |
|---|---|---|---|
""" + "\n".join(rows) + """

## What each company expected and said

""" + "\n".join(reasons) + """
The full record of every step (Board guidance, frames, test memos, decisions, veto checks, Board reviews) is in
`engine/reference/played_decisions.json`; the briefs and bulletins the players saw are in `engine/reference/briefs/`.
"""


def _one(x):
    s = (x or "").strip().replace("\n", " ")
    return s if s.endswith(".") else s + "."


def readme_md(ctx):
    return """# dash-2050-cons: the Boeing vs Airbus war game, packed for any LLM

**Start with `GAME_SCRIPT.md`.** It is the whole game as one script: the game master's instructions, the rules, the
round protocol, each company's doctrine and the twenty personas.

| File or folder | What it is | Who gets it |
|---|---|---|
| `GAME_SCRIPT.md` | The full script (sections 1-8) | The game master; in a one-chat game, the one chat |
| `kits/COMPANY_<company>.md` | One company's kit: how its chat works, its decision rule, the nine steps, output formats, rules, doctrine and its four full persona definitions | That company's chat only (six-chat set-up) |
| `engine/` | The game engine (Python 3.9+, numpy, pandas) with the 2030 starting position and `play.py` | The game master (needs code execution) |
| `engine/reference/` | The original game: briefs, bulletins, orders, every step's notes | The game master only, and only as section 1.6 of the script allows |
| `personas/` | The twenty persona cards (also in the script, section 8) | |
| `personas_full/` | The twenty original agent definitions, adapted to this pack (file paths point into `companies/`) | |
| `companies/<company>/` | Each company's source files: behavioural profile, objectives, game doctrine, 2026 analyst-model baseline, executive and Board profiles, evidence | That company only |
| `RESULTS_AS_PLAYED.md` | What the original players did (spoiler) | Nobody until the replay ends |

## Quick start

**One chat with code execution** (ChatGPT, Gemini or Claude with file upload and code): upload the zip and say:

> Unzip this pack. Read GAME_SCRIPT.md in full: you are the game master and you will also play every seat by section
> 1.4. Run `python3 engine/play.py selftest`, then start a game and play round 1 by the script.

**Six chats (closest to the original):** in one chat, upload the pack and say "You are the game master: read
GAME_SCRIPT.md section 1 and run the engine". In five more chats, give each company its kit
(`kits/COMPANY_boeing.md` etc.) and say "Read this kit; you are this company. Wait for the game master's brief." Then
carry each round's brief from the GM chat to each company chat, and each company's final orders block back.

**No code execution:** give the one chat `GAME_SCRIPT.md` and the five round-1 briefs
(`engine/reference/briefs/round1_*.md`) only, and follow section 1.6 of the script. Later rounds' original briefs
show what the original players did: give them to the chat only when section 1.6 says they apply.

## Notes

- The engine's self-test replays the original orders and checks that every brief and every value comes out exactly as
  played (`python3 play.py selftest`).
- The company folders and the original briefs contain extracts from company filings, earnings-call transcripts and
  analyst models (Goldman Sachs, Morgan Stanley, S&P Capital IQ). Check that your licences and your organisation's
  rules allow sharing them with the LLM provider you use.
- Built by `wargame/export/build_llm_pack.py` from the repository's game files.
"""
