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
            sc["properties"][k] = {"type": "object", "properties": {"<every order field of your company, section 6>": {"enum": ["one value"]}}, "required": ["<every order field of your company, section 6>"]}
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
# ───────────────────────────── what every seat is told ─────────────────────────────
def preamble_md(consts, side):
    """The per-seat preamble of exco_round.js (head / headBoard), chat version, for one company."""
    t = consts["TEAMS"][side]
    cur = consts["CURRENT"].get(side)
    tail = ("\n> " + cur) if cur else ""
    run = ("Your company's run folder (use it instead of any other run folder your agent file names) holds your brief "
           "for this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round: there are no "
           "earlier notes or orders. Later rounds: Earlier rounds (1 to N-1): ExCo notes in `exco/` and sealed orders in "
           "`my_orders_r<k>.json`.")
    run_b = ("Your company's run folder (use it instead of any other run folder your agent file names) holds the brief for "
             "this round (`roundN.md`) and the public rules (`rules.md`). Round 1: This is the first round. Later rounds: "
             "Earlier rounds (1 to N-1): the ExCo's and your notes in `exco/` and the sealed orders in `my_orders_r<k>.json`.")
    ex = ("> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.\n>\n"
          "> You are <the seat's name> of %s. Follow your agent file: \"Your step in each round\", \"Your tests\", "
          "\"Your vetoes and red lines\", \"Your voice\".\n>\n> %s\n>\n> Your ExCo's decision rule: %s\n>\n"
          "> Use only numbers from your brief and your own company's profile files. Read nothing of another company. "
          "Run no wargame.engine command.%s" % (t["company"], run, t["rule"], ("\n>" + tail) if cur else ""))
    bd = ("> War game run `<game>`, round N (decision year YYYY). Your step: **<step>**.\n>\n"
          "> You are %s. Follow your agent file: \"Your step in each round\", \"Your culture\", \"Your tests\", \"Your veto "
          "and its limits\", \"Your recommendations\".\n>\n> %s\n>\n> The ExCo is %s (CEO), %s (CFO) and %s (operating "
          "head). Its decision rule: %s\n>\n> Every order that differs from the default (hold, or none) is a Board item; an "
          "engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, "
          "and you never veto a hold.\n>\n> Use only numbers from your brief and your own company's files. Read nothing of "
          "another company. Run no wargame.engine command.%s" % (
              t["boardName"], run_b, t["names"]["ceo"], t["names"]["cfo"], t["names"]["ops"],
              t["rule"], ("\n>" + tail) if cur else ""))
    return ("**Every executive seat** (CEO, CFO, operating head) is told, before its task:\n\n" + ex +
            "\n\n**The Board** is told, before its task:\n\n" + bd)


def _protocol_text(names, cfo, ops, vc, vo, prop, generic=False):
    cfo_t, ops_t = ("", "") if generic else (", CFO", ", operating head")
    ORDERS_REF = "section 6" if generic else "see \"Your orders\": the first value listed is the default"
    ceo = names["ceo"]
    return f"""**Step 0. Board guidance** (the Board). Task: *Give the ExCo your guidance for this round: your priorities, your
risk appetite this round, what you expect to see in the package, what you would approve and what you would veto, and
your recommendations. It does not bind; your veto comes at the review.*

**Step 1. Frame** ({ceo}{'' if generic else ', CEO'}). Task: *The Board's guidance for this round (non-binding; its veto
comes after your decision): [the step-0 output]. Write the framing note for your ExCo: the question this round, the
levers in play, the options worth testing, the red lines in force, what you ask of your CFO and of your operating head,
and your initial lean. Your colleagues see only what you return here.*

**Step 2. Test** ({cfo}{cfo_t}, and {ops}{ops_t}: separately; neither ever sees the other's memo). Task: *Your CEO's
framing note, passed by the game master: [the step-1 output]. The Board's guidance for this round: [the step-0
output]. Test it independently: you do not see your colleague's memo. Apply your own tests with thresholds and the
grid numbers you used, give your recommended orders, and state any veto with its ground and whether the team rule makes
it binding (your veto: [the seat's veto ground]). Memo of at most 250 words, in your voice.*
   - {cfo[0].upper() + cfo[1:]}'s veto ground: {vc}.
   - {ops[0].upper() + ops[1:]}'s veto ground: {vo}.{prop}

**Step 3. Decide** ({ceo}). Task: *Your framing note: [step 1]. The Board's guidance for this round: [step 0].
[CFO]'s test memo: [step 2, CFO]. [Operating head]'s test memo: [step 2, operating head]. Decide by the team rule.
Return the company's sealed orders (one value per field), other moves, the public statement, the rationale, and how
you weighed each memo. Any override of a colleague's veto goes in `overrides` and must be allowed by the rule. Answer
each of the Board's recommendations in `board_response`: how you took it up, or why not. Every order that differs from
the default goes to the Board, which can veto it.* (The last two sentences only when there was Board guidance.)

**Step 4. Veto check** ({cfo} and {ops}, separately). Task: *Your own test memo: [its step-2 memo]. The CEO's
decision: [step 3]. Concur, or invoke a veto only on a ground the team rule gives you: [the seat's veto ground]. Set
`veto.binding` true only if, under the rule, the CEO must revise within it (or record an allowed override).
Separately, if the orders break a company hard rule (a red line), set `red_line_breach` true and name the rule in
`red_line`: that is not a veto, but the CEO must strike the breach.*

**Step 5. Revise** ({ceo}). Runs exactly when a veto check returned `concur: false` with `veto.binding: true`, or any
veto check returned `red_line_breach: true`; nobody else judges whether a veto binds. Task: *Your decision: [step 3].
Binding veto(es) from your ExCo: [name: the veto check, for each]. Company red-line breach(es) flagged by your ExCo:
[name: the red line and note, for each]. Revise your orders once. Stay within each binding veto, or override only
where the team rule allows it and record each override in `overrides`. Strike every flagged red-line breach you confirm
(red lines are never traded for PV); if you judge a flag mistaken, keep the order and say why in `rationale`.* The
revision replaces the decision, as returned.

**Step 6. Board review** (the Board). Runs only when there are Board items: the order fields, other than engine codes,
whose value differs from the default ({ORDERS_REF}). With none, the review is an automatic approval ("No Board items:
every order is the default"). Task: *Your guidance this round: [step 0]. The ExCo's package, passed by the game master:
[the framing note, both test memos, the decision, both veto checks and the revision, if any]. The orders it submits:
[the orders]. The Board items: [fields]. For each, approve or veto, with the ground and evidence; for a veto you may
name acceptable alternatives (other values of that order field, or the default). Then your recommendations.*

**Step 7. Board revise** ({ceo}). Runs only when the Board vetoed an item. Task: *Your orders as submitted: [the
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
(and the rest of its decision) come from the CEO's latest output: step 7, else step 5, else step 3."""


def protocol_md(consts, side=None):
    if side is None:
        names = {"ceo": "the CEO"}
        return _protocol_text(names, "the CFO", "the operating head", "see section 8", "see section 8",
                              "\n   - Pratt & Whitney only: the operating head's task ends *Per the team rule you also "
                              "PROPOSE the engine orders: put them in `recommended_orders` and explain them in `proposal`.*",
                              generic=True)
    t = consts["TEAMS"][side]
    prop = ("\n   - %s's task ends: *Per the team rule you also PROPOSE the engine orders: put them in "
            "`recommended_orders` and explain them in `proposal`.*" % t["names"]["ops"]) if t.get("proposes") == "ops" else ""
    return _protocol_text(t["names"], t["names"]["cfo"], t["names"]["ops"], t["veto"]["cfo"]["ground"],
                          t["veto"]["ops"]["ground"], prop)


FAILURES = """If a step's output is missing (no reply, or a reply that still does not match its format after two
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
| Step 8, the Board confirm | The revised items revert to their defaults |"""


def steps_table_md():
    return """Every seat, at every step, has: its persona; this round's brief (the public bulletin followed by its
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

Nothing ever crosses between companies: a company sees another only through the public bulletin."""


def team_md(consts, side):
    t = consts["TEAMS"][side]
    cur = consts["CURRENT"].get(side)
    return (f"- **Executive committee:** {t['names']['ceo']} (CEO), {t['names']['cfo']} (CFO), {t['names']['ops']} "
            f"(operating head). **Board:** {t['boardName']}.\n"
            f"- **Decision rule:** {t['rule']}\n"
            f"- **CFO veto ground:** {t['veto']['cfo']['ground']}.\n"
            f"- **Operating head veto ground:** {t['veto']['ops']['ground']}.\n"
            + (f"- **Proposes the engine orders:** the operating head ({t['names']['ops']}).\n" if t.get("proposes") == "ops" else "")
            + (f"- **Board figures (told to every {NAMES[side]} seat):** {cur}\n" if cur else ""))


def defaults_md(consts):
    rows = []
    for side in SIDES:
        f = consts["ORDER_FIELDS"][side]
        rows.append("| %s | %s |" % (NAMES[side], "; ".join("`%s`: %s" % (k, ", ".join("`%s`" % ("null" if v is None else v) for v in vals))
                                                            for k, vals in f.items())))
    return ("| Company | Order fields and values (the first value is the default) |\n|---|---|\n" + "\n".join(rows) + """

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
  "new_site"}, "public_statement": "...", "other_moves": [{"move": "...", "public": true, "detail": "..."}]}}`""")


# ───────────────────────────── GAME_SCRIPT.md ─────────────────────────────
def game_script(ctx):
    c = ctx["consts"]
    teams = "\n\n".join("## %s\n\n%s\n%s" % (NAMES[s], team_md(c, s), preamble_md(c, s)) for s in SIDES)
    seats = "\n".join("| %s | %s | %s | %s | %s | `kits/COMPANY_%s.md` |" % (
        NAMES[s], *["`%s`" % a for a in ctx["agents"][s]], s) for s in SIDES)
    return f"""# Boeing vs Airbus, 2030-2050: the war game "dash-2050-cons", scripted for any LLM

This is the full script for replaying, with another LLM, the five-player war game played as run `dash-2050-cons`:
Boeing and Airbus (airframers) and the engine makers CFM/GE, Pratt & Whitney and Rolls-Royce, over four decision rounds
(2030, 2035, 2045, 2050). In the original, each company was four AI agents (the CEO, the CFO, the operating head and
the Board of Directors), each built from the real executives' and directors' public record and run as a separate
agent; a game master ran every round on an economic engine (the narrowbody/widebody game-theory dashboard with a
supply-and-demand layer). This pack carries all of it: the engine and the starting position (`engine/`), an automated
runner that plays every seat through any LLM's API (`engine/run_game.py`), the twenty agent definitions
(`personas_full/`), each company's kit and source files (`kits/`, `companies/`), and this script.

**Spoilers.** `RESULTS_AS_PLAYED.md` and `engine/reference/` hold what the original players did. They are in the full
pack only (`dash-2050-cons-llm.zip`). The players' pack (`dash-2050-cons-llm-players.zip`) leaves them out: it is for
the runner, the GM chat and set-up 3. It still holds every company's kit and files, so a company chat gets only its own
kit (and its own `companies/<company>/` folder), never the zip. Open the results only after the replay.

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
| **1. Automated runner** (recommended) | Python 3.9+ with numpy and pandas, and an API key for any OpenAI-compatible endpoint (OpenAI, Google Gemini, Anthropic, Mistral, a local model with a 128k-token context) | Closest: every seat-step is a fresh call with only what that seat had in the original; formats checked; Board items, merges, reverts and missing steps handled in code, as in the original |
| **2. Six chats + an operator** | A chat app with code execution for the game master (GM), five more chats (one per company) with at least about 60k tokens of context, and a person to carry text between them | Good, if the operator runs each test (step 2) and veto check (step 4) in a fresh chat; otherwise the four seats of a company share one context |
| **3. One chat** | A chat with code execution and a very large context | Weakest: one context holds every company's deliberation, so sealed orders are not really sealed; use only to explore |
| **4. No code execution** | The five kits and the five round-1 briefs, one company per chat | Round 1 only is exact (its starting position is fixed); later rounds need the engine |

The operator runs the engine's self-test once, from the full pack, on their own computer:
`python3 engine/play.py selftest`, from the pack's top folder. It prints only PASS or FAIL per round. Operators without
Python can skip it; never open the full pack in a chat app on the account you play with.

---

# 2. Set-up 1: the automated runner

Unzip the **players' pack** into its own folder (not inside the full pack), `cd dash-2050-cons-llm`, install the
engine's needs (`pip install -r engine/requirements.txt`) and run:

```
export LLM_API_KEY=...                       # the key for your endpoint
python3 engine/run_game.py --game mygame --base-url https://api.openai.com/v1 --model <model>
```

- **Endpoints.** Google Gemini `--base-url https://generativelanguage.googleapis.com/v1beta/openai`; Anthropic
  `--base-url https://api.anthropic.com/v1`; Azure OpenAI `--base-url https://<resource>.openai.azure.com/openai/v1
  --auth-header api-key --auth-prefix ''` (or a deployment URL with `--url-query api-version=<version>`); a local
  Ollama `--base-url http://localhost:11434/v1`, after raising its context window (`OLLAMA_CONTEXT_LENGTH=131072`, or
  `num_ctx` in a Modelfile): its default of a few thousand tokens silently cuts every prompt.
- **Model settings.** No temperature is sent unless you give `--temperature` (reasoning models refuse non-default
  values). For reasoning or thinking models give room for the answer: `--max-tokens 32000` (with
  `--max-tokens-field max_completion_tokens` for newer OpenAI models). `--seat-model board=<model>` uses a different
  model for one seat (ceo, cfo, ops or board).
- **Running and resuming.** The command plays rounds 1 to 4; `--rounds 1` plays round 1 only and `--rounds 2-4` the
  rest. To resume after an error, Ctrl-C or a closed laptop, run the same command again: finished steps are kept. A
  round is adjudicated only when all five companies have finished it. When the API still fails after its retries (rate
  limits and network errors are retried with backoff), the runner stops before adjudicating and tells you; fix the
  cause (key, model name, endpoint, quota) and run it again. `--on-api-error missing` instead treats such a step as
  missing (section 7.3), as the original treated an agent that died. `--parallel 1` plays one company at a time (for
  low rate limits).
- **Other options.** `--no-tools` for APIs without function calling (the seats then get their company's doctrine
  inline but cannot read the rest of their company's files, a departure from the original), `--history full` (every
  earlier note in each prompt), `--persona card` (the condensed persona cards), `--companies boeing,airbus` (the
  others hold). `python3 engine/run_game.py --help` lists them all.

What it does, round by round: writes the briefs; plays the nine steps for the five companies in parallel. Each
seat-step is a fresh conversation: the seat's agent definition as the system prompt; the preamble (section 8) and the
step's task (section 7); the company's rules, brief and earlier decisions; and tools to read its own company's files
and its run folder (earlier rounds only) and to do exact arithmetic, as the original agents could. Notes of the round
in progress are closed to the seats, so a CFO never sees the operating head's memo. Then it applies the merge, revert
and missing-step rules, adjudicates, and prints the round's events (covert ones included: the operator sees them) and
every company's value; at the end of the command, `status`. Every request is logged in
`engine/runs/<game>/calls/`, every step's output in `engine/runs/<game>/players/<company>/exco/`.

Size: up to 11 seat-steps per company per round, each one or more requests (a request per tool use, plus up to two
format corrections). Prompts run from about 15k tokens in round 1 to 60-90k in round 4, and each tool use resends
them: count on 400-1,000 requests and 20-60 million input tokens for a full game, depending on how much the model
reads. Checks without an LLM: `--provider replay` feeds back the original agents' own answers and must reproduce the
original game exactly (full pack only); `--provider mock` makes every seat hold.

---

# 3. Set-ups 2-4: playing in chat apps

## 3.1 Roles and isolation

- **The operator** is a person. A chat cannot send messages to another chat, so the operator carries text: briefs
  from the GM chat to the company chats, and each company's final orders block back. The operator also keeps the
  files (the saved game, each company's notes) and runs the self-test.
- **The game master (GM)** is the chat that runs the engine (it needs code execution). It is neutral, never advises a
  company, never shows one company another's private material, and never adds anything to a bulletin.
- **A company** is a chat (or, for the most faithful play, one chat per seat-step) that plays the company's four
  seats by the protocol in section 7, from its kit `kits/COMPANY_<company>.md` and its own `companies/<company>/`
  folder, and nothing else of the pack.
- **Isolation in chat apps.** Turn off saved memory and chat-history reference (or use temporary chats, or a separate
  account or project per company) for the GM and every company chat: otherwise the app can carry one company's chat
  into another. The GM chat is the only chat that holds every kit (inside the players' pack). Never open the full
  pack or `RESULTS_AS_PLAYED.md` in a chat on the account you play with before the replay ends.

## 3.2 Set-up 2, step by step

1. **GM chat.** Upload the players' pack and say: *"Unzip this and cd into dash-2050-cons-llm. You are the game master
   of the war game in GAME_SCRIPT.md; read sections 3, 4, 6, 7 and 9. Run `python3 engine/play.py env`, then
   `python3 engine/play.py new mygame`, then
   `python3 engine/play.py brief mygame 1` and `python3 engine/play.py save mygame`, and give me `mygame.zip` and
   each company's `engine/runs/mygame/players/<company>/round1.md` as files to download."*
2. **Company chats.** In each of five chats, paste the company's kit (or upload it, then check it was read: ask the
   chat to quote the last line of the kit and the first row of "Your orders"), and upload its folder
   `companies/<company>/` if the app takes files. A kit is 35-40k tokens; with a brief and the round's notes a company
   chat needs about 60k tokens of context in round 1 and more later. If the app's context is smaller, start a fresh
   company chat each round with the kit, the new brief and the company's earlier notes (the operator keeps a copy of
   each company's step outputs).
3. **Play the round in each company chat**, in one of two ways:
   - *Plain:* send *"Round 1 (year 2030). Your brief follows. Run steps 0 to 8 by your kit and end with your orders
     block."* and the whole of its `round1.md`. Say "continue" if it stops between steps. Tell it to use code or a
     calculator for every sum.
   - *Most faithful (fresh seats for steps 2 and 4):* send the brief with *"Run steps 0 and 1, then stop."* Open two
     fresh chats, one per tester (CFO, operating head). Give each: the seat's persona (its full definition in the
     kit, under "Your four personas"); "What every seat is told before its task" (the executive block); the step-2
     task with its brackets filled in (the step-1 frame and the step-0 guidance); the seat's veto ground; the step-2
     output format; the brief, the public rules, the company's earlier notes and its `companies/<company>/` folder if
     the company chat has it. Paste both memos back into the company chat, labelled "Step 2: <name>", with
     *"Continue with step 3, then stop."* Then open two more fresh chats for the step-4 veto checks, one per tester:
     each gets the same persona, preamble, brief, rules, notes and files, the step-4 task with its brackets filled in
     (its own step-2 memo and the step-3 decision), its veto ground and the step-4 output format. Paste both back,
     labelled "Step 4: <name>", with *"Continue from step 5 to the end."*
4. **Back to the GM.** Paste the five orders blocks (or upload them as files). Ask the GM to run
   `python3 engine/play.py check mygame 1 <files>`, `python3 engine/play.py adjudicate mygame 1 <files>`,
   `python3 engine/play.py brief mygame 2` and `python3 engine/play.py save mygame`, and give you `mygame.zip` and the
   five round-2 briefs. A company with no block holds everything. Adjustments `check` reports in a company's block
   stand, as in the original (the company is told in its next brief); use `python3 engine/play.py undo mygame 1` only
   for the operator's own copying mistakes.
5. Carry each company's round-2 brief to its chat, and repeat to round 4. Then ask the GM for
   `python3 engine/play.py status mygame` (values, yields and Control's objectives) and
   `python3 engine/play.py reveal mygame` (covert Delay Tactics), and open `RESULTS_AS_PLAYED.md`.
6. **If the GM's sandbox is reset** (files gone): upload the players' pack and the latest `mygame.zip` again, unzip the
   pack, cd into it and run `python3 engine/play.py load <path to mygame.zip>`. Before the first save, just run `new`
   and `brief mygame 1` again: the start is fixed.

The GM chat never sees a company's deliberation, so each company chat applies the protocol's own rules (Board items,
the step-7 merge, reverts and missing steps) and outputs only its final orders. The GM applies only the engine's
rules and "no block = hold". The orders template (`play.py orders-template`) is for the GM only: its legal values can
reveal a covert order.

## 3.3 Set-up 3: one chat

Upload the players' pack to one chat with code execution. The chat is the GM and plays every seat. Play one company
at a time, one seat at a time; before each step, restate the seat and what it receives (section 7) and use nothing
else; play each seat from its full definition in its kit. Because one context holds everything, rivals' sealed orders
and private briefs are in view: this set-up cannot reproduce the original's isolation. For a better result, play each
company-round in a fresh chat given only that company's kit, its brief and its earlier notes (that is set-up 2 without
a separate GM chat).

## 3.4 Set-up 4: no code execution

One chat per company, each given only its own kit and its own round-1 brief (`engine/reference/briefs/round1_<company>.md`,
from the full pack; the starting position is fixed, so these are the briefs of any replay); this script stays with the
operator. Play round 1 by the kit. The operator then compares each company's orders with the original's
(`RESULTS_AS_PLAYED.md`, the orders table), field by field: every order field of section 6 counts, including Boeing's
`rate_737` and Airbus's covert `delay_tactics`. If every company's orders match, the original round-2 briefs apply,
once the operator replaces their "Public statements (last round)" and "Other moves made public" sections with the
replay's own. Otherwise the replay needs the engine: continue in set-up 2 or 1.

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

{_demote(ctx['rules_md'], 1)}

---

# 6. Orders, defaults, Board items and validation

{defaults_md(c)}

---

# 7. The round protocol

Each company plays the same nine steps; only the names, the decision rule and the veto grounds change (section 8).
Every task below is the text the original game gave the seat, with its inputs in [brackets]. Before its task, each
seat is told the preamble in section 8.

## 7.1 What every seat receives

{steps_table_md()}

## 7.2 The nine steps

{protocol_md(c)}

## 7.3 Missing steps

{FAILURES}

## 7.4 Output formats

The same for every company; `orders` and `recommended_orders` hold the company's own order fields (section 6), one
value each. `evidence_ids` list the evidence ids the seat relies on (the ids its persona or company files cite); they
may be empty.

{formats_md(c, None)}

---

# 8. The five companies' executive committees

{teams}

---

# 9. Known inconsistencies in the original material (game master only)

The original players had these too. Do not pass this section to the companies: it explains, it does not change what
they see. Where texts conflict, the public rules and the brief govern, as they did in the original.

- **Doctrine written for an earlier game.** Each company's behavioural-profile quick card (in its kit) was written
  for an earlier version, with turns from 2026, another engine and other share rules. The "dashboard war game"
  mapping that follows it updates much of it, but not all.
- **The NGSA-alone share rule.** Boeing's and Airbus's game mappings still give the board's rule "Only NGSA launched:
  Airbus gains 3 pp a year (cap 80%)". This game replaces it: Boeing loses 1 pp of preference a year from 40% from
  NGSA's entry into service while no fps is in service, never below the share Airbus cannot supply (the public rules).
- **Market size.** Some persona and doctrine texts say the narrowbody market is fixed at 2,000 aircraft (4,000
  engines) a year. In this game supply and demand govern (section 5, last part).
- **Boeing's H4 overlap.** Boeing's game mapping says a Solo fps launched with the 787 Re-engine in the same round
  overlaps by 5 years. That holds for the 7-year fps; a 10-year fps (or via Embraer) overlaps by 2 years (the strain
  overlap counts the fps from EIS minus 7 and the Re-engine from EIS minus 5). Boeing's operating head and Board say so.
- **"fps as a Joint Venture"** (Boeing doctrine H1, H4, H7) has no order on this board.
- **`launch_if_selected`.** The engine launches the engine when, after this round's orders, a live airframe
  (launched this round or earlier, not cancelled, not yet in service) carries an engine code that includes the maker,
  new or standing, and the engine would be ready by that airframe's EIS. The rules' wording ("selected you this
  round") is narrower; the Pratt & Whitney personas describe this behaviour.
- **Engine code 4 without a Joint Venture.** The rules say code 4 needs a formed Joint Venture engine ready by EIS.
  In the engine, code 4 without one behaves like Rolls-Royce and P&W solo: the makers whose solo engine is ready by
  EIS are fitted (CFM if neither is), and it triggers both makers' `launch_if_selected`. The P&W and Rolls-Royce texts
  mostly count code 4 only with a formed Joint Venture (a few partner-alignment rows count it without one).
- **GEnx timing.** Some CFM texts say a GEnx package counts from launch plus 3 years and not before 2035; the rules say
  it counts 3 years after launch, and widebody engine shares move only from the first re-engine (or 2042).
- **Old run folders.** Each company's game mapping names an earlier run's folder (`/tmp/wargame-<company>/dash-2050/`)
  for the brief and rules. The preamble's "use it instead of any other run folder your agent file names" covers it,
  and the runner's file tool maps such paths to the seat's run folder.
- **The Board's confirm step.** The Airbus, CFM/GE and Pratt & Whitney Board definitions say the step-8 prompt does
  not pass the package again (Airbus and Pratt & Whitney: nor the review), and Airbus's adds that this round's notes
  are saved only after the round. The step-8 task (section 7.2) does include the Board's guidance, the package and its review, as the
  Boeing and Rolls-Royce definitions say. The runner saves each step's note as it finishes (so a stopped run
  can resume), but the seats cannot open this round's notes.
- **Engine code `None`.** The briefs print the no-code option as `None`; in orders it is JSON `null`.
- **Pratt & Whitney's round-1 brief** shows its status-quo ΔPV as −0.00 (floating-point noise) and its "ΔPV ≥ 0"
  objective as not met; the original players saw the same. With a numpy other than 2.4.x the same zero can print as
  +0.00 and read "met", in the brief and in `status` (`play.py env` says which you have). The status-quo component tables in round-1 briefs are
  empty because every component is zero.

---

# 10. Where everything is

| Company | CEO | CFO | Operating head | Board | Kit |
|---|---|---|---|---|---|
{seats}

- `personas_full/<agent>.md`: the agent definitions the original game used, adapted only in file paths and the
  Independence section (they are in the kits too). `personas/<agent>.md`: condensed cards of the same, for reference.
- `companies/<company>/`: each company's profile, objectives, game doctrine, 2026 analyst-model baseline, executive
  and Board profiles, role cards and evidence.
- `engine/`: `play.py` (the engine's commands), `run_game.py` (the runner), `protocol.json` (the protocol's teams,
  order fields and formats), `dashgame/` (the engine), `runs/dash-2050-cons-start/` (the 2030 position),
  `requirements.txt`; in the full pack also `reference/` (the original game).
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
    gov = ("Where a figure differs from your brief or from the Board figures above, those govern."
           if side in ("boeing", "airbus") else "Where a figure differs from your brief, your brief governs.")
    return f"""# {NAMES[side]}: company kit for the war game dash-2050-cons

You are **{NAMES[side]}** in a five-player war game (Boeing, Airbus, CFM/GE, Pratt & Whitney, Rolls-Royce) over four
rounds: 2030, 2035, 2045, 2050. In this chat you play your company's four decision-makers, one at a time: the Board
({t['boardName']}), {t['names']['ceo']} (CEO), {t['names']['cfo']} (CFO) and {t['names']['ops']} (operating head). A game
master (GM) runs the game elsewhere; a person (the operator) brings you your brief each round and takes your orders back.
You never see another company's brief, payoffs, deliberation or orders: what you know of the rivals is the public
bulletin and your profile.

## How this chat works

1. Each round the operator pastes your brief: the public bulletin followed by {NAMES[side]}'s private brief.
2. Run the nine steps below in order, one seat at a time. Before each step write a heading "Step k: <seat>"; play
   only that seat, from its full definition below, using only what that seat receives (section "What every seat
   receives") and writing its output in its format. A step may take its own reply: if a reply would be too long, stop
   after a step and continue when the operator says "continue". Do every sum with code or a calculator if you have one.
3. The CFO and the operating head test independently: the second must not use the first's memo. (The operator may run
   these seats in fresh chats and paste their outputs back.)
4. Apply the protocol's rules yourself: Board items, the step-7 merge, reverts, and missing steps.
5. End the round with one block for the operator, with the orders as they stand after step 8:

```json
{{"{side}": {{"orders": {{ one value per order field }}, "public_statement": "...", "other_moves": [ {{"move": "...", "public": true, "detail": "..."}} ]}}}}
```

6. Next round, the operator pastes your new brief, which also tells you if any of your orders were adjusted. Your
   earlier rounds' notes stay in this chat; use them.

7. When the operator says "stop" after a step, stop and wait: the operator may run the CFO's and the operating
   head's steps in fresh chats and paste their outputs ("Step 2: <name>" for the tests, "Step 4: <name>" for the veto
   checks); take those as the seats' outputs and continue from where the operator says.

Your personas cite your company's files (`companies/{side}/...`). If the operator uploaded that folder, read them as
your persona says; if not, follow the rule as your persona states it. Wherever a persona says the game master (GM)
passes something or gives the schema, in this chat that is the operator's message and the Output formats below; your
run folder is this chat (ignore any `/tmp/...` path in your files).

## Your company's decision rule

{team_md(c, side)}

## What every seat is told before its task

{preamble_md(c, side)}

## What every seat receives

{steps_table_md()}

## The nine steps

{protocol_md(c, side)}

## Missing steps

{FAILURES}

## Output formats

{formats_md(c, side)}

## Your orders

{_orders_for(c, side)}

## The public rules (every player has the same text)

{_demote(ctx['rules_md'], 2)}

## Your company doctrine

The quick card of your behavioural profile, then its mapping to this game ("the dashboard war game"). The quick card
was written for an earlier version of the game, with turns from 2026; the mapping says what still applies here and
governs where they differ. The public rules govern over both. {gov}

{ctx['doctrine'][side]}

## Your four personas (the original agent definitions)

{full}
"""


def _orders_for(c, side):
    f = c["ORDER_FIELDS"][side]
    lines = ["- `%s`: %s" % (k, ", ".join("`%s`" % ("null" if v is None else v) for v in vals)) for k, vals in f.items()]
    return ("One value per field; the first value listed is the default (keep). Your brief lists which values are legal "
            "this round. An engine code is JSON `null` or an integer 1-7 (the brief prints `null` as `None`).\n\n" +
            "\n".join(lines) +
            ("\n\n`fps_site` is your standing supply plan: its default is your current plan." if side == "boeing" else "") +
            ("\n\n`a320_plan` is your standing supply plan: its default is your current plan." if side == "airbus" else "") +
            "\n\nEvery order that differs from its default is a Board item (engine codes ride with their launch).")


# ───────────────────────────── results and README ─────────────────────────────
def results_md(ctx):
    pl, dec, fin = ctx["played"], ctx["decisions"], ctx["final_status"]
    rows = []
    prev = ctx["standing"]                      # {round: {side: {field: value before the round}}}
    for n in ("1", "2", "3", "4"):
        r = pl["rounds"][n]
        for s in SIDES:
            o = r["orders_file"][s]["orders"]
            base = prev[n][s]
            ch = {k: v for k, v in o.items() if v != base.get(k) and not (k.endswith("_engine_code") and v is None)}
            rows.append("| %s (%d) | %s | %s | %+.2f |" % (n, r["year"], NAMES[s],
                                                          ", ".join("`%s`: `%s`" % (k, "null" if v is None else v) for k, v in ch.items()) or "no change",
                                                          r["value"][s]))
    reasons = []
    for n in ("1", "2", "3", "4"):
        reasons.append("### Round %s (%d)\n" % (n, pl["rounds"][n]["year"]))
        reasons.append("Public events: " + ("; ".join(e for e in pl["rounds"][n]["log"] if "[covert]" not in e) or "none") + ".\n")
        for s in SIDES:
            d = dec[n][s]
            ex = d.get("exco") or {}
            br = ex.get("board_review") or {}
            board = ("no Board items" if not (br.get("items") or []) else "%s%s" % (
                br.get("overall", "?"), (", vetoed " + ", ".join(ex.get("board_vetoed") or [])) if ex.get("board_vetoed") else ""))
            reasons.append("**%s.** Expected scenario: %s Best grid plan in it: %s Premium: %s. Board: %s.\n\n"
                           "Public statement: \"%s\"\n" % (
                               NAMES[s], _one(d.get("expected_scenario")), _one(d.get("best_grid_plan_in_expected_scenario")),
                               "$%.2fB" % d["premium_b"] if isinstance(d.get("premium_b"), (int, float)) else "none", board,
                               (d.get("public_statement") or "").strip()))
            om = pl["rounds"][n]["orders_file"][s].get("other_moves") or []
            if om:
                reasons.append("Other moves:\n" + "\n".join("- %s %s%s" % ("(public)" if m.get("public") else "(private)", m.get("move", ""),
                                                                           (": " + m["detail"]) if m.get("detail") else "") for m in om) + "\n")
    v4 = pl["rounds"]["4"]
    obj = "\n".join("| %s | %s | %s | %s |" % (NAMES[s], lab, "met" if ok else "not met", det) for s in SIDES for lab, ok, det in fin[s])
    return f"""# dash-2050-cons as played (spoiler: open only after your replay)

The original game, played on 14 October 2026 by twenty AI agents (an executive committee and a Board for each
company) with the game master's engine. Values are ΔPV against the status quo, $B, present value at 2026.

## Final values (after round 4, 2050)

| Company | ΔPV ($B) | Yield |
|---|---|---|
""" + "\n".join("| %s | %+.2f | %.2f%% |" % (NAMES[s], v4["value"][s], v4["yield"][s]) for s in SIDES) + f"""

## Control's objectives at the end (as the briefs measure them)

| Company | Objective | Status | Detail |
|---|---|---|---|
{obj}

## Orders each round (changes from the standing position) and value after the round

"No change" means every order kept the company's standing position (holds, its current supply plan, the engine code
already on record). Delay Tactics were never ordered.

| Round | Company | Orders that changed something | ΔPV after the round |
|---|---|---|---|
""" + "\n".join(rows) + """

## What each company expected, said and did besides

""" + "\n".join(reasons) + """
The full record of every step (Board guidance, frames, test memos, decisions, veto checks, Board reviews) is in
`engine/reference/played_decisions.json`; the briefs and bulletins the players saw are in `engine/reference/briefs/`.
"""


def _one(x):
    s = (x or "").strip().replace("\n", " ")
    return s if s.endswith(".") else s + "."


def readme_md(ctx):
    return """# dash-2050-cons: the Boeing vs Airbus war game, packed for any LLM

**Start with `GAME_SCRIPT.md`.** It explains the four ways to play, the game, its rules and its round protocol.

| File or folder | What it is | Who gets it |
|---|---|---|
| `GAME_SCRIPT.md` | The full script: set-ups, the runner, the operator's and game master's steps, rules, protocol, known inconsistencies | The operator and the game master |
| `engine/run_game.py` | The automated runner: plays all twenty seats through any OpenAI-compatible API | The operator (set-up 1) |
| `engine/play.py` | The engine's commands: new, brief, orders-template, check, adjudicate, undo, status, reveal, save, load, env, selftest | The game master |
| `kits/COMPANY_<company>.md` | One company's kit: how its chat works, its decision rule, what each seat is told and receives, the nine steps, formats, orders, rules, doctrine and its four full agent definitions | That company only |
| `companies/<company>/` | That company's source files: behavioural profile, objectives, game doctrine, 2026 analyst-model baseline, executive and Board profiles, role cards, evidence | That company only |
| `personas_full/`, `personas/` | All twenty agent definitions (full, and condensed cards) | Never a company (each company's four are in its kit); the runner uses them |
| `RESULTS_AS_PLAYED.md`, `engine/reference/` | The original game: orders, values, statements, every step's notes, the briefs and bulletins (full pack only) | Nobody until the replay ends; the operator for the self-test and set-up 4 |

Two zips: `dash-2050-cons-llm.zip` (everything, for the operator) and `dash-2050-cons-llm-players.zip` (the same
without the original game's record: for the runner, the GM chat and set-up 3; a company chat gets only its own kit and
its own `companies/<company>/` folder, never a zip). Each unzips to a folder `dash-2050-cons-llm/`: unzip them into
separate folders, and run every command from inside one.

## Quick start

1. Unzip the full pack into its own folder, `cd dash-2050-cons-llm`, install the engine's needs
   (`pip install -r engine/requirements.txt`) and run `python3 engine/play.py selftest`. It prints PASS or FAIL per
   round and nothing about the original game.
2. **Automated (recommended):** unzip the players' pack into another folder and, with an API key,
   `python3 engine/run_game.py --game mygame --base-url <endpoint> --model <model>` (GAME_SCRIPT.md section 2).
3. **In chat apps:** follow GAME_SCRIPT.md section 3 (six chats and an operator; one chat; or no code execution).

## Notes

- The pack contains extracts from company filings, earnings-call transcripts and analyst models (Goldman Sachs,
  Morgan Stanley, S&P Capital IQ) in `companies/`, the kits and the briefs. Check that your licences and your
  organisation's rules allow sharing them with the LLM provider you use.
- Sizes: `GAME_SCRIPT.md` is about 20k tokens; a company kit about 35-40k; a brief 4-9k. A full automated game is
  roughly 400-1,000 API requests and 20-60 million input tokens.
- Built by `wargame/export/build_llm_pack.py` from the repository's game files.
"""
