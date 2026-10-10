"""Check the per-executive agents: python3 check_agents.py [--md DIR] [--json DIR] [agent-name ...]

Defaults: the agent definitions in .claude/agents/<agent>.md and the profiles in data/agents/<agent>.json (the HTML
page's data). For each agent it checks:
- front matter: name equals the agent name; description and tools present;
- the required headings, in order (executives: 18 with "## Your Board"; boards: the 20 of BOARD_SPEC.md);
- every evidence id cited, in the .md or the .json, exists in the evidence files;
- every quote in the .md "Your voice" section, and every profile voice quote, is verbatim from its id's quote
  ("..." or "…" may join verbatim fragments that appear in order);
- profile quotes' date, doc and perspective match the evidence item;
- the profile JSON has the required keys.
Exit status 1 if any error is found.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
EV = {}
for f in (glob.glob(REPO + "/wargame/profiles/*/evidence.jsonl") + glob.glob(REPO + "/wargame/profiles/*/executives/evidence.jsonl")
          + glob.glob(REPO + "/wargame/profiles/*/board/evidence.jsonl")):
    if "_2010" in f:
        continue
    for line in open(f):
        if line.strip():
            d = json.loads(line)
            EV.setdefault(d["id"], d)

HEADINGS = ["## Your record", "## What you are paid to protect", "## How you decide", "## Your tests",
            "## Your vetoes and red lines", "## Your positions on the game's levers", "## How you read the rivals",
            "## Your colleagues", "## Your Board", "## Biases to display", "## Your voice", "## Where your record is thin",
            "## Your files", "## Your step in each round", "## Independence", "## What you return", "## Language"]
BOARD_HEADINGS = ["## Who you are", "## Your record", "## What you hold management to", "## Your culture",
                  "## Matters reserved to you", "## How you decide", "## Your tests", "## Your veto and its limits",
                  "## Your recommendations", "## How you see management", "## How you read the rivals",
                  "## Decisions you have taken", "## Where your record is thin", "## Your voice", "## Your files",
                  "## Your step in each round", "## Independence", "## What you return", "## Language"]
BOARD_KEYS = ["agent_name", "company", "side", "board_name", "as_of", "composition", "evidence", "mandate",
              "holds_management_to", "culture", "reserved_matters", "board_items_in_game", "decision_process", "tests",
              "veto", "recommendation_style", "management_relationship", "rivals", "past_decisions", "thin", "voice",
              "web_sources", "protocol_steps"]
KEYS = ["agent_name", "name", "side", "company", "seat", "title", "team_id", "role_dates", "evidence", "mandate",
        "objective_ranked", "decision_style", "tests", "vetoes", "lever_positions", "rivals", "colleagues", "biases",
        "voice", "thin", "dash2050_voiced", "protocol_steps", "veto_holder"]
IDRE = re.compile(r"\b((?:BX|AX|CX|PX|RX|BG|AG|CG|PG|RG|B|A|C|P|R)-\d{4})\b")


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def verbatim(q, src):
    frags = [f.strip(" ,;:") for f in re.split(r"\.\.\.|…", q) if f.strip(" ,;:.")]
    pos = 0
    for fr in frags:
        i = src.find(fr, pos)
        if i < 0:
            i = norm(src).find(norm(fr), pos)
        if i < 0:
            return False
        pos = i + len(fr)
    return bool(frags)


def check(md_dir, js_dir, name):
    errs, warns = [], []
    md_p, js_p = os.path.join(md_dir, name + ".md"), os.path.join(js_dir, name + ".json")
    if not os.path.exists(md_p) or not os.path.exists(js_p):
        return ["missing file(s)"], []
    md = open(md_p).read()
    fm = re.match(r"---\n(.*?)\n---\n", md, re.S)
    if not fm:
        errs.append("no front matter")
    else:
        if not re.search(r"^name:\s*%s\s*$" % re.escape(name), fm.group(1), re.M):
            errs.append("front matter name != %s" % name)
        for k in ("description:", "tools:"):
            if k not in fm.group(1):
                errs.append("front matter missing " + k)
    board = name.endswith("-board")
    pos = 0
    for h in (BOARD_HEADINGS if board else HEADINGS):
        i = md.find("\n" + h, pos)
        if i < 0:
            errs.append("heading missing or out of order: " + h)
        else:
            pos = i
    for i in set(IDRE.findall(md)):
        if i not in EV:
            errs.append("md cites unknown id " + i)
    v0 = md.find("\n## Your voice")
    v1 = md.find("\n## ", v0 + 5)
    voice = md[v0:v1] if v0 >= 0 else ""
    nq = 0
    for m in re.finditer(r'["“]([^"”]{6,}?)["”][^\[\n]{0,80}?\[((?:BX|AX|CX|PX|RX|BG|AG|CG|PG|RG|B|A|C|P|R)-\d{4})', voice):
        q, i = m.group(1), m.group(2)
        nq += 1
        if EV.get(i, {}).get("kind") == "web":
            errs.append("md voice quote from a web item [%s]" % i)
        if i in EV and not verbatim(q, EV[i]["quote"]):
            errs.append("md voice quote not verbatim [%s]: %s" % (i, q[:80]))
    if nq < 3:
        warns.append("md voice section has only %d checkable quotes" % nq)
    try:
        p = json.load(open(js_p))
    except Exception as e:
        return errs + ["profile json invalid: %s" % e], warns
    for k in (BOARD_KEYS if board else KEYS):
        if k not in p:
            errs.append("profile missing key " + k)
    if board:   # web items behind a score, test, veto or reserved matter must be corroborated
        hard = json.dumps([p.get("culture"), p.get("tests"), p.get("veto"), p.get("reserved_matters")])
        for i in set(IDRE.findall(hard)):
            e = EV.get(i, {})
            if e.get("kind") == "web" and not e.get("corroborated_by"):
                errs.append("uncorroborated web item behind a score, test, veto or reserved matter: " + i)
    if p.get("agent_name") != name:
        errs.append("profile agent_name mismatch")
    for qq in (p.get("voice") or {}).get("quotes", []):
        i = qq.get("id")
        if i not in EV:
            errs.append("profile quote unknown id %s" % i)
            continue
        e = EV[i]
        if e.get("kind") == "web":
            errs.append("profile voice quote from a web item [%s]" % i)
        if not verbatim(qq.get("quote", ""), e.get("quote", "")):
            errs.append("profile quote not verbatim [%s]: %s" % (i, qq.get("quote", "")[:80]))
        if qq.get("date") != e.get("date"):
            errs.append("profile quote date mismatch [%s]: %s vs %s" % (i, qq.get("date"), e.get("date")))
        if qq.get("perspective") != e.get("perspective"):
            errs.append("profile quote perspective mismatch [%s]: %s vs %s" % (i, qq.get("perspective"), e.get("perspective")))
        if (qq.get("doc") or "")[:25] != (e.get("doc") or "")[:25]:
            warns.append("profile quote doc differs [%s]" % i)
    for i in set(IDRE.findall(json.dumps(p))):
        if i not in EV:
            errs.append("profile cites unknown id " + i)
    return errs, warns


def main(argv):
    md_dir, js_dir, names = os.path.join(REPO, ".claude", "agents"), os.path.join(HERE, "data", "agents"), []
    while argv:
        a = argv.pop(0)
        if a == "--md":
            md_dir = argv.pop(0)
        elif a == "--json":
            js_dir = argv.pop(0)
        else:
            names.append(a)
    names = names or sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(js_dir, "*.json")))
    if not os.path.isdir(md_dir):
        sys.exit("no such folder: " + md_dir)
    bad = 0
    for n in names:
        e, w = check(md_dir, js_dir, n)
        bad += len(e)
        print("%-26s %s" % (n, "OK" if not e else "%d ERRORS" % len(e)) + ("" if not w else "  (%d warnings)" % len(w)))
        for x in e:
            print("   ERROR", x)
        for x in w:
            print("   warn ", x)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
