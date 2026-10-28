#!/usr/bin/env python3
"""Plays the war game dash-2050-cons end to end with any LLM behind an OpenAI-compatible chat API.

It runs the original round protocol (wargame/dashgame/workflows/exco_round.js) for all five companies: in every
round, for each company, the Board's guidance, the CEO's frame, the CFO's and the operating head's independent tests,
the CEO's decision, the two veto checks, a revision when a binding veto or a red-line flag stands, the Board's review,
the CEO's revision after a Board veto and the Board's confirmation. Every seat-step is one fresh call: the seat's
persona (personas_full/<agent>.md, the agent definition the original game used) as the system prompt, the step's task
text as the original gave it, the company's brief and rules, and its earlier notes. Outputs are checked against the
step's JSON format; Board items, reverts and fail-closed rules are applied in code, as in the original. Then the
engine adjudicates the round and writes the next briefs.

  # any OpenAI-compatible endpoint: OpenAI, Google Gemini, Anthropic, Mistral, Together, Ollama, vLLM, LM Studio ...
  export LLM_API_KEY=...
  python3 run_game.py --game mygame --base-url https://api.openai.com/v1 --model gpt-4.1
  python3 run_game.py --game mygame --base-url https://generativelanguage.googleapis.com/v1beta/openai --model gemini-2.5-pro
  python3 run_game.py --game mygame --base-url http://localhost:11434/v1 --model llama3.1:70b --no-tools

  # checks without an LLM
  python3 run_game.py --game replaycheck --provider replay   # feeds back the original agents' answers: must reproduce
                                                             # the original game exactly (needs reference/)
  python3 run_game.py --game dry --provider mock             # plumbing test: every seat holds

A stopped game resumes where it stopped: finished steps are read back from runs/<game>/players/<company>/exco/ and
finished rounds from the engine's files. Each call's prompt and reply are logged in runs/<game>/calls/.
Python 3.9+, numpy and pandas (the engine's needs); no other package.
"""
import argparse
import ast
import concurrent.futures as cf
import json
import operator
import os
import re
import subprocess
import sys
import time
import threading
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
RUNS = os.path.join(HERE, "runs")
PROTO = json.load(open(os.path.join(HERE, "protocol.json"), encoding="utf-8"))
ORDER_FIELDS, TEAMS, SCHEMAS, CURRENT = PROTO["ORDER_FIELDS"], PROTO["TEAMS"], PROTO["schemas"], PROTO["CURRENT"]
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
YEARS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
SEATS = {"ceo": "CEO", "cfo": "CFO", "ops": "operating head"}
NOTE_TITLES = {"board_guidance": "Board guidance", "frame": "CEO framing note", "test_cfo": "CFO test memo",
               "test_ops": "Operating head test memo", "decision": "CEO decision", "veto_cfo": "CFO veto check",
               "veto_ops": "Operating head veto check", "revision": "CEO revision after a binding veto or a red-line flag",
               "board_review": "Board review", "board_revision": "CEO revision after a Board veto",
               "board_confirm": "Board confirmation"}


_PRINT = threading.Lock()


def say(msg):
    with _PRINT:
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()


def js(x):
    return "```json\n" + json.dumps(x, indent=1, ensure_ascii=False) + "\n```"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ───────────────────────────── JSON formats ─────────────────────────────
def check(schema, v, path="$"):
    """Errors of value v against the step's schema (the subset the protocol uses)."""
    errs = []
    if "enum" in schema:
        if v not in schema["enum"]:
            errs.append("%s: %r is not one of %s" % (path, v, schema["enum"]))
        return errs
    t = schema.get("type")
    if t == "object":
        if not isinstance(v, dict):
            return ["%s: expected an object" % path]
        for k in schema.get("required", []):
            if k not in v:
                errs.append("%s: missing field %r" % (path, k))
        for k, sub in schema.get("properties", {}).items():
            if k in v:
                errs += check(sub, v[k], "%s.%s" % (path, k))
    elif t == "array":
        if not isinstance(v, list):
            return ["%s: expected an array" % path]
        for i, x in enumerate(v):
            errs += check(schema["items"], x, "%s[%d]" % (path, i))
    elif t == "string":
        if not isinstance(v, str):
            errs.append("%s: expected a string" % path)
    elif t == "number":
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            errs.append("%s: expected a number" % path)
    elif t == "boolean":
        if not isinstance(v, bool):
            errs.append("%s: expected true or false" % path)
    return errs


def skeleton(schema, ind=0):
    pad = " " * ind
    if "enum" in schema:
        return " | ".join("null" if x is None else json.dumps(x) for x in schema["enum"])
    t = schema.get("type")
    if t == "object":
        req = set(schema.get("required", []))
        lines = ["%s  %s%s: %s" % (pad, json.dumps(k), "" if k in req else " (optional)", skeleton(s, ind + 2))
                 for k, s in schema.get("properties", {}).items()]
        return "{\n" + ",\n".join(lines) + "\n" + pad + "}"
    if t == "array":
        return "[ " + skeleton(schema["items"], ind + 2) + ", ... ]"
    return {"string": "\"text\"", "number": "number", "boolean": "true | false"}.get(t, "value")


def extract_json(text):
    """The first JSON object in a reply (bare, or inside a ```json fence)."""
    if not text:
        return None
    t = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", t, re.S)
    for cand in ([m.group(1)] if m else []) + [t]:
        try:
            x = json.loads(cand)
            if isinstance(x, dict):
                return x
        except ValueError:
            pass
    i = t.find("{")
    while i >= 0:
        depth, instr, esc = 0, False, False
        for j in range(i, len(t)):
            c = t[j]
            if instr:
                esc = (c == "\\" and not esc)
                if c == '"' and not esc:
                    instr = False
                continue
            if c == '"':
                instr = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        x = json.loads(t[i:j + 1])
                        if isinstance(x, dict):
                            return x
                    except ValueError:
                        break
        i = t.find("{", i + 1)
    return None


# ───────────────────────────── tools for the seats ─────────────────────────────
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg, ast.UAdd: operator.pos}
_FUN = {"min": min, "max": max, "sum": sum, "abs": abs, "round": round}


def calculate(expr):
    """Arithmetic only: numbers, + - * / ** %, parentheses, lists, min max sum abs round."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        if isinstance(n, (ast.List, ast.Tuple)):
            return [ev(e) for e in n.elts]
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUN and not n.keywords:
            return _FUN[n.func.id](*[ev(a) for a in n.args])
        raise ValueError("not allowed: %s" % ast.dump(n)[:60])
    return ev(ast.parse(expr, mode="eval"))


TOOLS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read one of your company's files, or list a folder. Paths: your company's profile files (e.g. "
                       "profile.md, objectives.md, dashboard_game.md, analyst_models_2026.md, executives/teams.md, "
                       "executives/<name>.md, board/board.md, evidence.jsonl), and your run folder: rules.md, roundN.md "
                       "(this round and earlier ones), exco/rK_<step>.md (earlier rounds' notes), my_orders_rK.json. "
                       "Give '' or a folder name to list it. Large files come back in parts: use offset.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}},
                       "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "search_file",
        "description": "Lines of one of your company's files that contain a text (case-insensitive), with line numbers.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "text": {"type": "string"}},
                       "required": ["path", "text"]}}},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Evaluate arithmetic exactly: numbers, + - * / ** %, parentheses, lists, min max sum abs round. "
                       "Example: 0.5*(-4.39) + 0.5*(-4.80) - 1.0",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
]
CHUNK = 60000


class Files:
    """A seat's view of the files: its company's folder and its run folder, nothing else; rounds after the current
    one are closed."""
    def __init__(self, game, side, n):
        self.roots = [os.path.join(RUNS, game, "players", side), os.path.join(PACK, "companies", side)]
        self.side, self.n = side, n

    def _resolve(self, path):
        p = (path or "").strip().lstrip("/")
        for pre in ("companies/%s/" % self.side, "wargame/profiles/%s/" % self.side):
            if p.startswith(pre):
                p = p[len(pre):]
        m = re.match(r"(?:round|exco/r|my_orders_r)(\d+)", p)
        if m and int(m.group(1)) > self.n:
            raise ValueError("a later round's file is closed to you")
        if m and p.startswith(("exco/r", "my_orders_r")) and int(m.group(1)) >= self.n:
            raise ValueError("only earlier rounds' notes and orders are open")
        for root in self.roots:
            full = os.path.realpath(os.path.join(root, p))
            if (full + os.sep).startswith(os.path.realpath(root) + os.sep) or full == os.path.realpath(root):
                if os.path.exists(full):
                    return full
        raise ValueError("no such file in your folders: %s" % path)

    def read(self, path, offset=0):
        full = self._resolve(path)
        if os.path.isdir(full):
            items = sorted(os.listdir(full))
            return "\n".join(x + ("/" if os.path.isdir(os.path.join(full, x)) else "") for x in items)
        txt = read(full)
        off = int(offset or 0)
        part = txt[off:off + CHUNK]
        more = "" if off + CHUNK >= len(txt) else "\n[... %d more characters: read again with offset=%d]" % (len(txt) - off - CHUNK, off + CHUNK)
        return part + more

    def search(self, path, text):
        full = self._resolve(path)
        out = ["%d: %s" % (i + 1, l[:400]) for i, l in enumerate(read(full).splitlines()) if text.lower() in l.lower()]
        return "\n".join(out[:200]) or "no line contains %r" % text

    def root_listing(self):
        return self.read("")


# ───────────────────────────── providers ─────────────────────────────
class OpenAICompatible:
    def __init__(self, a):
        self.url = a.base_url.rstrip("/") + "/chat/completions"
        self.key = os.environ.get(a.api_key_env, "")
        self.a = a
        self.tools_ok = not a.no_tools
        self.json_ok = a.json_mode != "off"
        self.models = dict(x.split("=", 1) for x in (a.seat_model or []))

    def _post(self, body):
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers[self.a.auth_header] = (self.a.auth_prefix + self.key) if self.a.auth_prefix else self.key
        data = json.dumps(body).encode("utf-8")
        for attempt in range(6):
            req = urllib.request.Request(self.url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=self.a.timeout) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")[:600]
                if e.code in (429, 500, 502, 503, 504, 529) and attempt < 5:
                    time.sleep(min(60, 4 * 2 ** attempt))
                    continue
                raise RuntimeError("HTTP %d from the API: %s" % (e.code, msg))
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < 5:
                    time.sleep(min(60, 4 * 2 ** attempt))
                    continue
                raise RuntimeError("cannot reach the API: %s" % e)

    def complete(self, messages, seat, files, want_json):
        """One seat-step: a tool loop, then a JSON reply. Returns (text, transcript)."""
        model = self.models.get(seat, self.a.model)
        msgs = list(messages)
        for _ in range(self.a.max_tool_calls + 1):
            body = {"model": model, "messages": msgs}
            if self.a.temperature is not None:
                body["temperature"] = self.a.temperature
            if self.a.max_tokens:
                body[self.a.max_tokens_field] = self.a.max_tokens
            if self.a.extra_body:
                body.update(json.loads(self.a.extra_body))
            use_tools = self.tools_ok
            if use_tools:
                body["tools"] = TOOLS
            elif want_json and self.json_ok:
                body["response_format"] = {"type": "json_object"}
            try:
                r = self._post(body)
            except RuntimeError as e:
                s = str(e)
                if use_tools and "HTTP 400" in s and "tool" in s.lower():
                    self.tools_ok = False
                    say("  the API rejected tools; continuing without them")
                    continue
                if not use_tools and "HTTP 400" in s and "response_format" in s:
                    self.json_ok = False
                    continue
                raise
            m = r["choices"][0]["message"]
            calls = m.get("tool_calls") or []
            if not calls:
                return m.get("content") or "", msgs + [{"role": "assistant", "content": m.get("content") or ""}]
            msgs.append({"role": "assistant", "content": m.get("content") or "", "tool_calls": calls})
            for c in calls:
                fn = c["function"]["name"]
                try:
                    args = json.loads(c["function"].get("arguments") or "{}")
                    if fn == "read_file":
                        out = files.read(args.get("path", ""), args.get("offset", 0))
                    elif fn == "search_file":
                        out = files.search(args.get("path", ""), args.get("text", ""))
                    elif fn == "calculate":
                        out = repr(calculate(args.get("expression", "")))
                    else:
                        out = "unknown tool %s" % fn
                except Exception as e:      # the seat sees the error and can try again
                    out = "error: %s" % e
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": out})
        msgs.append({"role": "user", "content": "Stop using tools now and return only the JSON object."})
        self.tools_ok, saved = False, self.tools_ok
        try:
            return self.complete(msgs, seat, files, want_json)
        finally:
            self.tools_ok = saved


class Replay:
    """The original agents' answers, step by step (engine/reference/played_decisions.json)."""
    KEYS = {"guidance": ("board_guidance",), "frame": ("frame",), "test_cfo": ("cfo",), "test_ops": ("ops",),
            "decide": ("decision",), "veto_cfo": ("veto_checks", "cfo"), "veto_ops": ("veto_checks", "ops"),
            "revise": ("revision",), "board_review": ("board_review",), "board_revise": ("board_revision",),
            "board_confirm": ("board_confirm",)}

    def __init__(self, a):
        p = os.path.join(HERE, "reference", "played_decisions.json")
        if not os.path.exists(p):
            sys.exit("--provider replay needs engine/reference/ (it is in the full pack, not the players' pack)")
        self.d = json.load(open(p, encoding="utf-8"))

    def answer(self, n, side, step):
        x = self.d[str(n)][side]["exco"]
        for k in self.KEYS[step]:
            x = (x or {}).get(k)
        if step in ("decide", "revise", "board_revise") and x is not None:
            x = dict(x)
        return x


class Mock:
    """Every seat holds: a plumbing test."""
    def __init__(self, a):
        pass

    def answer(self, n, side, step, schema):
        def fill(s):
            if "enum" in s:
                return s["enum"][0]
            t = s.get("type")
            if t == "object":
                return {k: fill(v) for k, v in s.get("properties", {}).items() if k in s.get("required", [])}
            return {"array": [], "string": "mock", "number": 0, "boolean": True}.get(t)
        x = fill(schema)
        if step.startswith("veto"):
            x.update({"concur": True, "red_line_breach": False})
        return x


# ───────────────────────────── the round protocol ─────────────────────────────
class Company:
    def __init__(self, game, n, side, llm, args, plans):
        self.game, self.n, self.year, self.side, self.llm, self.a = game, n, YEARS[n], side, llm, args
        self.t = TEAMS[side]
        self.dir = os.path.join(RUNS, game, "players", side)
        self.notes = os.path.join(self.dir, "exco")
        os.makedirs(self.notes, exist_ok=True)
        os.makedirs(os.path.join(RUNS, game, "calls"), exist_ok=True)
        self.defaults = {k: v[0] for k, v in ORDER_FIELDS[side].items()}
        self.defaults.update(plans.get(side, {}))
        self.files = Files(game, side, n)

    def log(self, msg):
        say("  r%d %-14s %s" % (self.n, self.side, msg))

    # materials and prompt heads, as exco_round.js gave them (the run folder is the seat's file tool)
    def materials(self):
        parts = ["## Your materials\n\n### The public rules (rules.md)\n\n" + read(os.path.join(self.dir, "rules.md")),
                 "### Your brief for round %d (round%d.md)\n\n" % (self.n, self.n) + read(os.path.join(self.dir, "round%d.md" % self.n))]
        if self.n > 1:
            hist = []
            for k in range(1, self.n):
                mo = os.path.join(self.dir, "my_orders_r%d.json" % k)
                if os.path.exists(mo):
                    hist.append("Round %d sealed orders (my_orders_r%d.json):\n%s" % (k, k, js(json.load(open(mo, encoding="utf-8")).get("as_adjudicated"))))
                if self.a.history == "full":
                    for key in NOTE_TITLES:
                        p = os.path.join(self.notes, "r%d_%s.md" % (k, key))
                        if os.path.exists(p):
                            hist.append(read(p))
                elif self.a.history == "decisions":
                    for key in ("board_guidance", "decision", "board_review"):
                        p = os.path.join(self.notes, "r%d_%s.md" % (k, key))
                        if os.path.exists(p):
                            hist.append(read(p))
            if hist:
                parts.append("### Your company's earlier rounds\n\n" + "\n\n".join(hist) +
                             ("\n\nAll earlier notes are in exco/ (your file tool reads them)." if self.llm_tools() else ""))
        return "\n\n".join(parts)

    def llm_tools(self):
        return isinstance(self.llm, OpenAICompatible) and self.llm.tools_ok

    def head(self, seat, step):
        t = self.t
        if seat == "board":
            lines = ["War game run `%s`, round %d (decision year %d). Your step: **%s**." % (self.game, self.n, self.year, step),
                     "You are %s. Follow your agent file: \"Your step in each round\", \"Your culture\", \"Your tests\", \"Your veto and its limits\", \"Your recommendations\"." % t["boardName"],
                     "Your company's run folder holds the brief for this round (`round%d.md`) and the public rules (`rules.md`)." % self.n +
                     (" Earlier rounds (1 to %d): the ExCo's and your notes in `exco/` and the sealed orders in `my_orders_r<k>.json`." % (self.n - 1) if self.n > 1 else " This is the first round."),
                     "The ExCo is %s (CEO), %s (CFO) and %s (operating head). Its decision rule: %s" % (t["names"]["ceo"], t["names"]["cfo"], t["names"]["ops"], t["rule"]),
                     "Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.",
                     "Use only numbers from your brief and your own company's files. Read nothing of another company. Run no wargame.engine command."]
        else:
            lines = ["War game run `%s`, round %d (decision year %d). Your step: **%s**." % (self.game, self.n, self.year, step),
                     "You are %s of %s. Follow your agent file: \"Your step in each round\", \"Your tests\", \"Your vetoes and red lines\", \"Your voice\"." % (t["names"][seat], t["company"]),
                     "Your company's run folder holds your brief for this round (`round%d.md`) and the public rules (`rules.md`)." % self.n +
                     (" Earlier rounds (1 to %d): ExCo notes in `exco/` and sealed orders in `my_orders_r<k>.json`." % (self.n - 1) if self.n > 1 else " This is the first round: there are no earlier notes or orders."),
                     "Your ExCo's decision rule: %s" % t["rule"],
                     "Use only numbers from your brief and your own company's profile files. Read nothing of another company. Run no wargame.engine command."]
        if CURRENT.get(self.side):
            lines.append(CURRENT[self.side])
        if self.llm_tools():
            lines.append("Your file tool reads your company's files and your run folder; your calculate tool does exact arithmetic.")
        return "\n\n".join(lines)

    def persona(self, seat):
        agent = self.t["board"] if seat == "board" else self.t[seat]
        if self.a.persona == "card":
            return read(os.path.join(PACK, "personas", agent + ".md"))
        return read(os.path.join(PACK, "personas_full", agent + ".md"))

    def call(self, key, seat, step, task, schema, note_key):
        """One seat-step, with resume: a saved note is read back instead of calling again."""
        saved = os.path.join(self.notes, "r%d_%s.json" % (self.n, note_key))
        if os.path.exists(saved):
            return json.load(open(saved, encoding="utf-8"))
        if isinstance(self.llm, Replay):
            out = self.llm.answer(self.n, self.side, key)
        elif isinstance(self.llm, Mock):
            out = self.llm.answer(self.n, self.side, key, schema)
        else:
            user = self.head(seat, step) + "\n\n" + self.materials() + "\n\n## Your task\n\n" + task + \
                "\n\n## What you return\n\nReturn only one JSON object in this format (field names exactly as shown; " \
                "text fields are strings; engine codes are JSON null or an integer 1-7):\n\n" + skeleton(schema)
            msgs = [{"role": "system", "content": self.persona(seat)}, {"role": "user", "content": user}]
            out = None
            for attempt in range(self.a.json_retries + 1):
                text, transcript = self.llm.complete(msgs, seat, self.files, True)
                cand = extract_json(text)
                errs = check(schema, cand) if cand is not None else ["the reply holds no JSON object"]
                self._log_call(note_key, attempt, transcript, text, errs)
                if not errs:
                    out = cand
                    break
                msgs = transcript + [{"role": "user", "content": "Your reply does not match the format: " + "; ".join(errs[:12]) +
                                      ". Reply again with only the corrected JSON object."}]
            if out is None:
                self.log("%s: no valid reply after %d tries (treated as missing)" % (note_key, self.a.json_retries + 1))
        if out is not None:
            with open(saved, "w", encoding="utf-8") as f:
                json.dump(out, f, indent=1, ensure_ascii=False)
            with open(os.path.join(self.notes, "r%d_%s.md" % (self.n, note_key)), "w", encoding="utf-8") as f:
                f.write("# Round %d: %s\n\n%s\n" % (self.n, NOTE_TITLES[note_key], js(out)))
        self.log("%-16s %s" % (note_key, "done" if out is not None else "MISSING"))
        return out

    def _log_call(self, note_key, attempt, transcript, text, errs):
        p = os.path.join(RUNS, self.game, "calls", "r%d_%s_%s_%d.json" % (self.n, self.side, note_key, attempt))
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"messages": transcript, "reply": text, "format_errors": errs}, f, indent=1, ensure_ascii=False)

    # Board items: every order field that differs from its default; engine codes ride with their launch
    def board_items(self, orders):
        return [k for k in ORDER_FIELDS[self.side] if not k.endswith("_engine_code") and orders and k in orders
                and orders[k] != self.defaults[k]]

    def revert(self, orders, fields):
        o = dict(orders)
        for k in fields:
            o[k] = self.defaults[k]
            if k + "_engine_code" in o:
                o[k + "_engine_code"] = self.defaults[k + "_engine_code"]
        return o

    def play(self):
        t, s, nm = self.t, self.side, self.t["names"]
        S = SCHEMAS
        # 0 Board guidance
        g = self.call("guidance", "board", "guidance",
                      "Give the ExCo your guidance for this round: your priorities, your risk appetite this round, what you "
                      "expect to see in the package, what you would approve and what you would veto, and your "
                      "recommendations. It does not bind; your veto comes at the review.", S["guidance"], "board_guidance")
        # 1 Frame
        gtxt = ("\n\nThe Board's guidance for this round (non-binding; its veto comes after your decision):\n" + js(g)) if g else ""
        fr = self.call("frame", "ceo", "frame", gtxt.strip() + ("\n\n" if gtxt else "") +
                       "Write the framing note for your ExCo: the question this round, the levers in play, the options worth "
                       "testing, the red lines in force, what you ask of your CFO and of your operating head, and your initial "
                       "lean. Your colleagues see only what you return here.", S["frame"], "frame")
        if fr is None:
            return None
        # 2 Test (independently, in parallel)
        def one_test(seat):
            extra = ("\n\nPer the team rule you also PROPOSE the engine orders: put them in `recommended_orders` and "
                     "explain them in `proposal`.") if t.get("proposes") == seat else ""
            gg = ("\n\nThe Board's guidance for this round:\n" + js(g)) if g else ""
            return self.call("test_" + seat, seat, "test",
                             "Your CEO's framing note, passed by the game master:\n%s%s\n\nTest it independently: you do not "
                             "see your colleague's memo. Apply your own tests with thresholds and the grid numbers you used, give "
                             "your recommended orders, and state any veto with its ground and whether the team rule makes it "
                             "binding (your veto: %s). Memo of at most 250 words, in your voice.%s" % (js(fr), gg, t["veto"][seat]["ground"], extra),
                             S["test"][s], "test_" + seat)
        with cf.ThreadPoolExecutor(2) as ex:
            cfo, ops = ex.map(one_test, ["cfo", "ops"])
        # 3 Decide
        gg = ("\n\nThe Board's guidance for this round:\n" + js(g)) if g else ""
        br = (" Answer each of the Board's recommendations in `board_response`: how you took it up, or why not. Every order "
              "that differs from the default goes to the Board, which can veto it.") if g else ""
        dec = self.call("decide", "ceo", "decide",
                        "Your framing note:\n%s%s\n\n%s's test memo:\n%s\n\n%s's test memo:\n%s\n\nDecide by the team rule. "
                        "Return the company's sealed orders (one value per field), other moves, the public statement, the "
                        "rationale, and how you weighed each memo. Any override of a colleague's veto goes in `overrides` and "
                        "must be allowed by the rule.%s" % (js(fr), gg, nm["cfo"], js(cfo), nm["ops"], js(ops), br),
                        S["decide"][s], "decision")
        if dec is None:
            return None
        # 4 Veto check (independently, in parallel)
        memos = {"cfo": cfo, "ops": ops}

        def one_veto(seat):
            return self.call("veto_" + seat, seat, "veto_check",
                             "Your own test memo:\n%s\n\nThe CEO's decision:\n%s\n\nConcur, or invoke a veto only on a ground the "
                             "team rule gives you: %s. Set `veto.binding` true only if, under the rule, the CEO must revise within "
                             "it (or record an allowed override). Separately, if the orders break a company hard rule (a red line), "
                             "set `red_line_breach` true and name the rule in `red_line`: that is not a veto, but the CEO must "
                             "strike the breach." % (js(memos[seat]), js(dec), t["veto"][seat]["ground"]), S["veto"], "veto_" + seat)
        with cf.ThreadPoolExecutor(2) as ex:
            vcfo, vops = ex.map(one_veto, ["cfo", "ops"])
        vc = {"cfo": vcfo, "ops": vops}
        # 5 Revise
        binding = [x for x in ("cfo", "ops") if vc[x] and not vc[x].get("concur") and (vc[x].get("veto") or {}).get("binding")]
        flags = [x for x in ("cfo", "ops") if vc[x] and vc[x].get("red_line_breach")]
        revision = None
        if binding or flags:
            parts = []
            if binding:
                parts.append("Binding veto(es) from your ExCo:\n\n" + "\n\n".join("%s: %s" % (nm[x], js(vc[x])) for x in binding))
            if flags:
                parts.append("Company red-line breach(es) flagged by your ExCo:\n\n" + "\n\n".join(
                    "%s: %s" % (nm[x], js({"red_line": vc[x].get("red_line"), "note": vc[x].get("note")})) for x in flags))
            revision = self.call("revise", "ceo", "revise",
                                 "Your decision:\n%s\n\n%s\n\nRevise your orders once. Stay within each binding veto, or override "
                                 "only where the team rule allows it and record each override in `overrides`. Strike every flagged "
                                 "red-line breach you confirm (red lines are never traded for PV); if you judge a flag mistaken, keep "
                                 "the order and say why in `rationale`." % (js(dec), "\n\n".join(parts)), S["decide"][s], "revision")
        final = revision or dec
        # 6 Board review
        items = self.board_items(final["orders"])
        exco = {"board_guidance": g, "frame": fr, "cfo": cfo, "ops": ops, "decision": dec, "veto_checks": vc,
                "binding_vetoes": binding, "red_line_flags": flags, "revision": revision, "board_items": items}
        if not items:
            rv = {"items": [], "recommendations": [], "overall": "approve", "note": "No Board items: every order is the default."}
        else:
            pkg = {"frame": fr, "cfo_memo": cfo, "ops_memo": ops, "decision": dec, "veto_checks": vc, "revision": revision}
            rv = self.call("board_review", "board", "review",
                           "Your guidance this round:\n%s\n\nThe ExCo's package, passed by the game master:\n%s\n\nThe orders it "
                           "submits:\n%s\n\nThe Board items: %s. For each, approve or veto, with the ground and evidence; for a veto "
                           "you may name acceptable alternatives (other values of that order field, or the default). Then your "
                           "recommendations." % (js(g), js(pkg), js(final["orders"]), ", ".join(items)), S["review"], "board_review")
            if rv is None:      # fail closed: no Board approval, no Board item
                self.log("no Board review: its items revert to the default: %s" % ", ".join(items))
                orders = self.revert(final["orders"], items)
                exco.update({"board_review": {"failed": True}, "board_vetoed": items, "board_revision": None,
                             "board_confirm": None, "board_reverted": items})
                return dict(final, orders=orders, exco=exco)
        exco["board_review"] = rv
        vetoed = [i["order_field"] for i in rv.get("items", []) if i.get("decision") == "veto" and i.get("order_field") in items]
        if not vetoed:
            exco.update({"board_vetoed": [], "board_revision": None, "board_confirm": None, "board_reverted": []})
            return dict(final, orders=final["orders"], exco=exco)
        # 7 Board revise
        rev = self.call("board_revise", "ceo", "board_revise",
                        "Your orders as submitted:\n%s\n\nThe Board's review:\n%s\n\nThe Board vetoed: %s. Revise once, within the "
                        "Board's veto: for each vetoed order choose an alternative the Board named, or the default. Keep the "
                        "approved orders. Answer the Board's recommendations in `board_response`." % (js(final), js(rv), ", ".join(vetoed)),
                        S["decide"][s], "board_revision")
        if rev:
            orders = dict(final["orders"])
            for k in vetoed:
                orders[k] = rev["orders"][k]
                if k + "_engine_code" in rev["orders"]:
                    orders[k + "_engine_code"] = rev["orders"][k + "_engine_code"]
        else:
            orders = self.revert(final["orders"], vetoed)
        changed = [k for k in vetoed if orders[k] != self.defaults[k]]
        reverted = [k for k in vetoed if orders[k] == self.defaults[k]]
        confirm = None
        if changed:
            pkg = {"frame": fr, "cfo_memo": cfo, "ops_memo": ops, "decision": dec, "veto_checks": vc, "revision": revision}
            confirm = self.call("board_confirm", "board", "confirm",
                                "Your guidance this round:\n%s\n\nThe ExCo's package:\n%s\n\nYour review:\n%s\n\nThe CEO's revision "
                                "after your veto:\n%s\n\nThe orders now, after the revision:\n%s\n\nThe revised Board items: %s. "
                                "Approve or veto each (an alternative you named should pass unless something changed). A still-vetoed "
                                "item reverts to the default." % (js(g), js(pkg), js(rv), js(rev), js(orders),
                                                                 ", ".join("%s = %s" % (k, orders[k]) for k in changed)),
                                S["review"], "board_confirm")
            still = [i["order_field"] for i in confirm.get("items", []) if i.get("decision") == "veto" and i.get("order_field") in changed] if confirm else changed
            orders = self.revert(orders, still)
            reverted += still
        exco.update({"board_vetoed": vetoed, "board_revision": rev, "board_confirm": confirm, "board_reverted": reverted})
        return dict(rev or final, orders=orders, exco=exco)


# ───────────────────────────── the game ─────────────────────────────
def engine(game, *args, quiet=False):
    r = subprocess.run([sys.executable, os.path.join(HERE, "play.py")] + list(args), capture_output=quiet, text=True,
                       env=dict(os.environ, PYTHONUTF8="1"))
    if r.returncode:
        if quiet:
            sys.stdout.write(r.stdout or "")
            sys.stderr.write(r.stderr or "")
        sys.exit("engine command failed: play.py %s" % " ".join(args))
    return r.stdout


def standing_plans(game, n):
    s = json.load(open(os.path.join(RUNS, game, "state_r%d.json" % (n - 1)), encoding="utf-8"))
    sd = s.get("sd") or {}
    return {"boeing": {"fps_site": sd.get("fps_site", "new_site")}, "airbus": {"a320_plan": sd.get("a320_plan", "base")}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", required=True, help="game name (a folder under engine/runs/)")
    ap.add_argument("--provider", choices=["api", "replay", "mock"], default="api")
    ap.add_argument("--base-url", help="OpenAI-compatible API base, e.g. https://api.openai.com/v1")
    ap.add_argument("--model", help="model name")
    ap.add_argument("--seat-model", action="append", help="a different model for one seat: ceo=..., cfo=..., ops=..., board=...")
    ap.add_argument("--api-key-env", default="LLM_API_KEY", help="environment variable holding the API key (default LLM_API_KEY)")
    ap.add_argument("--auth-header", default="Authorization", help="header for the key (Azure: api-key)")
    ap.add_argument("--auth-prefix", default="Bearer ", help="prefix before the key ('' for none)")
    ap.add_argument("--extra-body", help="JSON merged into every request body")
    ap.add_argument("--temperature", type=float, default=None)
    ap.add_argument("--max-tokens", type=int, default=None)
    ap.add_argument("--max-tokens-field", default="max_tokens", help="or max_completion_tokens (newer OpenAI models)")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--no-tools", action="store_true", help="no file and calculator tools (for APIs without function calling)")
    ap.add_argument("--max-tool-calls", type=int, default=24)
    ap.add_argument("--json-mode", choices=["auto", "off"], default="auto")
    ap.add_argument("--json-retries", type=int, default=2)
    ap.add_argument("--history", choices=["decisions", "full", "none"], default="decisions",
                    help="earlier rounds put in each prompt: sealed orders plus the Board guidance, the decision and the Board "
                         "review (decisions, default), every note (full) or only the sealed orders (none); with tools a seat "
                         "can read every earlier note itself")
    ap.add_argument("--persona", choices=["full", "card"], default="full", help="the original agent definitions (full) or the condensed cards")
    ap.add_argument("--rounds", default="1-4", help="e.g. 1-4, or 1")
    ap.add_argument("--companies", default=",".join(SIDES), help="companies the LLM plays; the others hold")
    ap.add_argument("--parallel", type=int, default=5, help="companies played at the same time")
    a = ap.parse_args()
    if a.provider == "api" and not (a.base_url and a.model):
        ap.error("--base-url and --model are needed with the api provider")
    if a.provider == "api" and not os.environ.get(a.api_key_env):
        print("note: %s is not set; calling the API without a key" % a.api_key_env)
    llm = {"api": OpenAICompatible, "replay": Replay, "mock": Mock}[a.provider](a)
    lo, hi = (int(x) for x in (a.rounds.split("-") + a.rounds.split("-"))[:2]) if "-" in a.rounds else (int(a.rounds), int(a.rounds))
    playing = [x.strip() for x in a.companies.split(",") if x.strip()]
    gdir = os.path.join(RUNS, a.game)
    if not os.path.exists(os.path.join(gdir, "state_r0.json")):
        engine(a.game, "new", a.game, quiet=True)
    print("game %s: %s, rounds %d-%d" % (a.game, a.provider if a.provider != "api" else "%s at %s" % (a.model, a.base_url), lo, hi))
    for n in range(lo, hi + 1):
        if os.path.exists(os.path.join(gdir, "record_r%d.json" % n)):
            print("round %d already adjudicated" % n)
            continue
        if not os.path.exists(os.path.join(gdir, "state_r%d.json" % (n - 1))):
            sys.exit("round %d needs round %d first" % (n, n - 1))
        if not os.path.exists(os.path.join(gdir, "brief_r%d_boeing.md" % n)):
            engine(a.game, "brief", a.game, str(n), quiet=True)
        plans = standing_plans(a.game, n)
        print("round %d (%d): playing %s" % (n, YEARS[n], ", ".join(playing)), flush=True)
        comps = {s: Company(a.game, n, s, llm, a, plans) for s in playing}
        with cf.ThreadPoolExecutor(max(1, a.parallel)) as ex:
            futs = {s: ex.submit(comps[s].play) for s in playing}
            results = {}
            for s, f in futs.items():
                try:
                    results[s] = f.result()
                except Exception as e:      # a company whose round fails holds, as in the original
                    say("  r%d %-14s FAILED: %s (it holds this round)" % (n, s, e))
                    results[s] = None
        orders = {}
        for s in SIDES:
            r = results.get(s)
            if r:
                orders[s] = {"orders": r["orders"], "public_statement": r.get("public_statement", ""),
                             "other_moves": r.get("other_moves") or [],
                             **{k: v for k, v in r.items() if k not in ("orders", "public_statement", "other_moves")}}
        path = os.path.join(gdir, "orders_exco_r%d.json" % n)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(orders, f, indent=1, ensure_ascii=False)
        out = engine(a.game, "adjudicate", a.game, str(n), path, quiet=True)
        print("\n".join(l for l in out.splitlines() if l.startswith(("round", "  -", "  !", "note"))))
        if n < 4:
            engine(a.game, "brief", a.game, str(n + 1), quiet=True)
    if os.path.exists(os.path.join(gdir, "record_r%d.json" % hi)):
        print(engine(a.game, "status", a.game, quiet=True))


if __name__ == "__main__":
    main()
