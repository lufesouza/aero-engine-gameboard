"""Builds the portable pack for replaying run dash-2050-cons in another LLM: wargame/export/dash-2050-cons-llm/.

  python3 build_llm_pack.py          # engine bundle, reference record, script, personas, zip

Parts:
- engine/: a copy of the game engine (wargame/dashgame: the v3 board combined_dash.py, the supply-and-demand layer,
  rules, briefs, finance) with the run's starting position (runs/dash-2050-cons-start: state_r0, board v3, objective
  set control2, supply and demand on, the run's sd_options), the CLI play.py and a plotly stub. One patch: player
  copies go to runs/<game>/players/<side>/ instead of /tmp/wargame-<side>/<run>/.
- reference/: the game as played (orders, public statements, values each round, briefs, bulletins, ExCo and Board
  decisions), for the self-test and for an LLM without code execution.
- GAME_SCRIPT.md: assembled from src/script/*.md, the run's public rules (rules.md) and personas/*.md, with the
  round protocol's prompts taken from wargame/dashgame/workflows/exco_round.js.
"""
import json
import os
import re
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WG = os.path.normpath(os.path.join(HERE, ".."))
DG = os.path.join(WG, "dashgame")
RUN = os.path.join(WG, "runs", "dash-2050-cons")
REC = os.path.join(WG, "reports", "dash-2050-cons", "record")      # committed copy of the run (runs/ is gitignored)
OUT = os.path.join(HERE, "dash-2050-cons-llm")
SRC = os.path.join(HERE, "src")
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
ENGINE_FILES = ["model.py", "rules.py", "briefs.py", "finance.py", "supply_demand.py", "gm.py", "reports.py",
                "supply_demand.json", "demand_conservative.json", "finance_inputs.json",
                "board/harness.py", "board/combined_dash.py", "board/Game_v3.txt"]
START_FILES = ["board.txt", "objectives.txt", "supply_demand.txt", "sd_options.json", "state_r0.json", "rules.md"]


def rec_path(name):
    p = os.path.join(RUN, name)
    return p if os.path.exists(p) else os.path.join(REC, name)


def jl(name):
    with open(rec_path(name), encoding="utf-8") as f:
        return json.load(f)


def patch(path, old, new, n=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == n, (path, old, s.count(old))
    open(path, "w", encoding="utf-8").write(s.replace(old, new))


def engine():
    e = os.path.join(OUT, "engine")
    for f in ENGINE_FILES:
        os.makedirs(os.path.dirname(os.path.join(e, "dashgame", f)), exist_ok=True)
        shutil.copy(os.path.join(DG, f), os.path.join(e, "dashgame", f))
    patch(os.path.join(e, "dashgame", "gm.py"), 'return "/tmp/wargame-%s/%s" % (side, RUN)',
          'return os.path.join(RUN_DIR, "players", side)')
    st = os.path.join(e, "runs", "dash-2050-cons-start")
    os.makedirs(st, exist_ok=True)
    for f in START_FILES:
        shutil.copy(rec_path(f), os.path.join(st, f))
    os.makedirs(os.path.join(e, "_stubs", "plotly"), exist_ok=True)
    open(os.path.join(e, "_stubs", "plotly", "__init__.py"), "w").write(
        '"""Stub used only when plotly is not installed: the engine never draws, it only computes."""\n')
    open(os.path.join(e, "_stubs", "plotly", "graph_objects.py"), "w").write(
        "class _Any:\n    def __init__(self, *a, **k): pass\n    def __call__(self, *a, **k): return _Any()\n"
        "    def __getattr__(self, n): return _Any()\n\n\ndef __getattr__(name):\n    return _Any\n")
    shutil.copy(os.path.join(SRC, "play.py"), os.path.join(e, "play.py"))


def reference():
    r = os.path.join(OUT, "engine", "reference")
    os.makedirs(os.path.join(r, "briefs"), exist_ok=True)
    played = {"run": "dash-2050-cons", "rounds": {}}
    decisions = {}
    for n in (1, 2, 3, 4):
        rec = jl("record_r%d.json" % n)
        orders_file = {}
        for side in SIDES:
            ret = rec["returned"].get(side) or {}
            orders_file[side] = {"orders": rec["orders"][side], "public_statement": rec["public_statements"].get(side, ""),
                                 "other_moves": ret.get("other_moves") or []}
        played["rounds"][str(n)] = {"year": rec["year"], "orders_file": orders_file, "log": rec["log"],
                                    "value": {s: rec["value"][s]["pv_delta"] for s in SIDES},
                                    "yield": {s: rec["value"][s]["yield"] for s in SIDES}}
        decisions[str(n)] = {}
        for side in SIDES:
            ret = rec["returned"].get(side) or {}
            ex = ret.get("exco") or {}
            decisions[str(n)][side] = {k: ret.get(k) for k in ("orders", "public_statement", "rationale", "memo_weighing",
                                                                "expected_scenario", "best_grid_plan_in_expected_scenario",
                                                                "premium_b", "premium_reason", "predictions", "expected_pv_b",
                                                                "overrides", "board_response")}
            decisions[str(n)][side]["exco"] = {k: ex.get(k) for k in ("board_guidance", "frame", "cfo", "ops", "decision",
                                                                      "veto_checks", "binding_vetoes", "red_line_flags",
                                                                      "revision", "board_items", "board_review",
                                                                      "board_vetoed", "board_revision", "board_confirm",
                                                                      "board_reverted")}
        shutil.copy(rec_path("bulletin_r%d.md" % n), os.path.join(r, "briefs", "round%d_bulletin.md" % n))
        for side in SIDES:
            shutil.copy(rec_path("brief_r%d_%s.md" % (n, side)), os.path.join(r, "briefs", "round%d_%s.md" % (n, side)))
    json.dump(played, open(os.path.join(r, "played_orders.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(decisions, open(os.path.join(r, "played_decisions.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return played


AGENTS = {"boeing": ["boeing-ortberg", "boeing-malave", "boeing-pope", "boeing-board"],
          "airbus": ["airbus-faury", "airbus-toepfer", "airbus-wagner", "airbus-board"],
          "cfm": ["cfm-culp", "cfm-ghai", "cfm-ali", "cfm-board"],
          "pratt_whitney": ["pratt-whitney-calio", "pratt-whitney-mitchill", "pratt-whitney-eddy", "pratt-whitney-board"],
          "rolls_royce": ["rolls-royce-erginbilgic", "rolls-royce-mccabe", "rolls-royce-watson", "rolls-royce-board"]}
AGENT_DIR = os.path.join(WG, "..", ".claude", "agents")
PROFILES = os.path.join(WG, "profiles")
# evidence ids such as [B-2276, BX-1259] or [AB-0012; inference]: dropped from the doctrine text in the script
EVID = re.compile(r"\s?\[(?:[A-Z]{1,5}-[0-9]{2,5}[a-z]?(?:\s*(?:,|;|and)\s*)?)+\]")


def protocol():
    out = os.path.join(SRC, "protocol.json")
    import subprocess
    subprocess.run(["node", os.path.join(SRC, "extract_protocol.js"), os.path.join(DG, "workflows", "exco_round.js"), out],
                   check=True, stdout=subprocess.DEVNULL)
    c = json.load(open(out))
    # the pack's files, not the repo's
    return c


def section(md, title_prefix):
    """The markdown section whose heading starts with `title_prefix` (up to the next heading of the same level)."""
    lines = md.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("## ") and l[3:].startswith(title_prefix):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            return "\n".join(lines[i:j]).strip()
    raise KeyError(title_prefix)


def doctrine():
    out = {}
    for side in SIDES:
        prof = open(os.path.join(PROFILES, side, "profile.md"), encoding="utf-8").read()
        dg = open(os.path.join(PROFILES, side, "dashboard_game.md"), encoding="utf-8").read()
        qc = section(prof, "Quick card")
        txt = ("#### From the behavioural profile: " + qc.split("\n", 1)[0][3:] + "\n\n" + qc.split("\n", 1)[1].strip() +
               "\n\n#### " + dg.split("\n", 1)[0].lstrip("# ") + "\n\n" + _demote_from(dg.split("\n", 1)[1].strip(), 3))
        out[side] = EVID.sub("", txt)
    return out


def _demote_from(md, level):
    """Headings '## x' become level `level` + 1 (so they nest under a level-`level` heading)."""
    o = []
    fence = False
    for l in md.splitlines():
        if l.startswith("```"):
            fence = not fence
        if not fence and l.startswith("#"):
            k = len(l) - len(l.lstrip("#"))
            l = "#" * (level + k - 1) + l[k:]
        o.append(l)
    return "\n".join(o)


INDEPENDENCE = """## Independence

- Never use another company's material: what you know of the rivals is the public bulletins plus your profile.
- Use only numbers from your brief and your own company's profile files.
- Inside the ExCo you see only what the game master (or this step) passes you."""


def _bullets(text):
    """Split a markdown section body into blocks: each bullet with its continuation lines, or a plain line."""
    blocks = []
    for l in text.splitlines():
        if blocks and l.startswith("  ") and not l.lstrip().startswith("- ") and blocks[-1].lstrip().startswith("- "):
            blocks[-1] += "\n" + l
        elif blocks and l.startswith("  ") and blocks[-1].lstrip().startswith("- ") and l.startswith("   "):
            blocks[-1] += "\n" + l
        else:
            blocks.append(l)
    return blocks


RUN_REF = re.compile(r"/tmp/wargame-|`<run>`|<run>|wargame/runs|wargame/reports|wargame/dashgame|wargame\.engine|"
                     r"A hook enforces|archived and closed|Repo root")


def adapt_agent(side, name):
    """The original agent definition, adapted to the pack: no frontmatter, file paths into companies/<side>/, the
    run-folder and isolation instructions replaced by the pack's (the game master hands each seat its brief, the rules
    and its company's earlier notes)."""
    src = open(os.path.join(AGENT_DIR, name + ".md"), encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", src, re.S)
    front, body = m.group(1), src[m.end():]
    desc = re.search(r"^description: (.*)$", front, re.M).group(1)
    body = body.replace("wargame/profiles/%s/" % side, "companies/%s/" % side)
    # Your files: keep the company-file bullets, drop the run-folder ones
    m = re.search(r"## Your files\n(.*?)(?=\n## )", body, re.S)
    if m:
        keep = []
        for b in _bullets(m.group(1)):
            if RUN_REF.search(b):
                b2 = re.sub(r"Repo root:? `/home/user/aero-engine-gameboard`\.\s*", "", b)
                if RUN_REF.search(b2):
                    continue
                b = b2
            keep.append(b)
        files = ("## Your files\n\nIn this pack your company's files are in `companies/%s/`. The game master gives you the round "
                 "brief, the public rules and your company's earlier notes and sealed orders.\n\n" % side) + "\n".join(keep).strip() + "\n"
        body = body[:m.start()] + files + body[m.end():]
    body = re.sub(r"## Independence\n.*?(?=\n## )", INDEPENDENCE + "\n", body, flags=re.S)
    left = [l for l in body.splitlines() if re.search(r"/tmp/|wargame/|/home/user|<run>|hook", l)]
    return "> Agent definition used in the original game: %s\n\n%s" % (desc, body.strip()), left


COMPANY_SKIP = ("citation_audit.md", "evidence.rejected.jsonl")


def companies():
    for side in SIDES:
        src, dst = os.path.join(PROFILES, side), os.path.join(OUT, "companies", side)
        for root, _, files in os.walk(src):
            for f in files:
                if f in COMPANY_SKIP or f.endswith(".pyc"):
                    continue
                rel = os.path.relpath(os.path.join(root, f), src)
                os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
                shutil.copy(os.path.join(root, f), os.path.join(dst, rel))


def zip_pack():
    z = os.path.join(HERE, "dash-2050-cons-llm.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(OUT):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in sorted(files):
                p = os.path.join(root, f)
                zf.write(p, os.path.join("dash-2050-cons-llm", os.path.relpath(p, OUT)))
    return z


def main():
    import sys
    sys.path.insert(0, SRC)
    import script_text as T
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    engine()
    played = reference()
    print("engine and reference written to", OUT)
    for n, x in played["rounds"].items():
        print(" round", n, x["year"], {s: round(v, 2) for s, v in x["value"].items()})
    consts = protocol()
    ctx = {"consts": consts, "rules_md": open(rec_path("rules.md"), encoding="utf-8").read(), "doctrine": doctrine(),
           "agents": AGENTS, "played": played,
           "decisions": json.load(open(os.path.join(OUT, "engine", "reference", "played_decisions.json"), encoding="utf-8"))}
    ctx["cards"], ctx["full"] = {}, {}
    os.makedirs(os.path.join(OUT, "personas"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "personas_full"), exist_ok=True)
    for side, names in AGENTS.items():
        for a in names:
            card = open(os.path.join(SRC, "personas", a + ".md"), encoding="utf-8").read().strip()
            ctx["cards"][a] = card
            ctx["full"][a], left = adapt_agent(side, a)
            for l in left:
                print("  check %s: %s" % (a, l.strip()[:150]))
            open(os.path.join(OUT, "personas", a + ".md"), "w", encoding="utf-8").write(card + "\n")
            open(os.path.join(OUT, "personas_full", a + ".md"), "w", encoding="utf-8").write(ctx["full"][a] + "\n")
    companies()
    os.makedirs(os.path.join(OUT, "kits"), exist_ok=True)
    for side in SIDES:
        open(os.path.join(OUT, "kits", "COMPANY_%s.md" % side), "w", encoding="utf-8").write(T.company_kit(ctx, side))
    open(os.path.join(OUT, "GAME_SCRIPT.md"), "w", encoding="utf-8").write(T.game_script(ctx))
    open(os.path.join(OUT, "RESULTS_AS_PLAYED.md"), "w", encoding="utf-8").write(T.results_md(ctx))
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(T.readme_md(ctx))
    z = zip_pack()
    for f in ("GAME_SCRIPT.md", "README.md", "RESULTS_AS_PLAYED.md"):
        p = os.path.join(OUT, f)
        print("%-24s %7d words" % (f, len(open(p, encoding="utf-8").read().split())))
    for side in SIDES:
        p = os.path.join(OUT, "kits", "COMPANY_%s.md" % side)
        print("kits/COMPANY_%-14s %7d words" % (side + ".md", len(open(p, encoding="utf-8").read().split())))
    print("zip", z, os.path.getsize(z) // 1024, "KB")


if __name__ == "__main__":
    main()
