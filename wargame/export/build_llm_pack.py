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
import sys
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
    patch(os.path.join(e, "dashgame", "gm.py"), '"supply plans (pass as args.plans to workflows/exco_round.js):"',
          '"standing supply plans (the defaults of fps_site and a320_plan this round):"')
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
    for f in ("play.py", "run_game.py"):
        shutil.copy(os.path.join(SRC, f), os.path.join(e, f))
    open(os.path.join(e, "requirements.txt"), "w").write(
        "# The engine was played and tested with these versions; others work, but a different numpy can print a few\n"
        "# +/-0.00 signs or last digits differently (play.py selftest reports it).\nnumpy==2.4.6\npandas>=3.0,<3.2\n")


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
        out[side] = txt          # evidence ids kept: the original seats read them (companies/<side>/ has the evidence)
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

- Never read another company's files or kit, the engine (`engine/`), the original game's record (`engine/reference/`,
  `RESULTS_AS_PLAYED.md`) or any later round's material, and never run the engine.
- Use only numbers from your brief and your own company's profile files.
- What you know of the rivals is the public bulletins plus your profile.
- %s"""
SEE_EXEC = "Inside the ExCo you see only what the game master passes you."
SEE_BOARD = "You see the ExCo only through the package the game master passes you and your company's notes."
FILES_NOTE = ("Your run folder holds `roundN.md` (this round's brief), `rules.md`, `exco/` (earlier rounds' notes) and "
              "`my_orders_rK.json` (earlier sealed orders). Your company's files are in `companies/%s/` (paths below are "
              "relative to it or name it). With the automated runner (`engine/run_game.py`) your file tool reads both; in "
              "a chat game the game master's messages and your chat history carry them.")
RUN_SUBS = [
    (r"Repo root:? `/home/user/aero-engine-gameboard`\.\s*", ""),
    (r"Run folder:? `/tmp/wargame-[a-z_]+/<run>/`,? (?:\(the run the GM names(?:: a fresh run)?\)|where `<run>` is the run the "
     r"GM's prompt names \(a fresh run; the earlier\s+dash-2050 game's files are archived and closed to you\))", "Your run folder"),
    (r"`/tmp/wargame-[a-z_]+/<run>/([^`]*)`", r"`\1`"),
    (r"`<run>/([^`]*)`", r"`\1`"),
    (r"`<run>` is the run id the GM's prompt names: a fresh run\. ", ""),
    (r"The earlier dash-2050 game's files are archived and closed to you\. ", ""),
    (r"(?m)^- The earlier dash-2050 game's files are archived and closed to you\.[ \t]*\n", ""),
    (r"Read only that folder; the earlier dash-2050 game's files are archived and closed to you\.", "Read only your run folder."),
    (r";\s+the earlier dash-2050 game's files are archived and closed to you", ""),
    (r"Use only the run folder the GM names\.", "Use only your run folder."),
    (r"Read only that folder, and in it", "Read only your run folder, and in it"),
]
LEFT = re.compile(r"/tmp/|wargame/|/home/user|<run>|\bhook\b|archived")


def adapt_agent(side, name):
    """The original agent definition, adapted to the pack: no frontmatter; company file paths point into
    companies/<side>/; run-folder paths are relative to the seat's run folder (roundN.md, rules.md, exco/,
    my_orders_rK.json), which the automated runner's file tool serves; the Independence section is the pack's."""
    src = open(os.path.join(AGENT_DIR, name + ".md"), encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", src, re.S)
    front, body = m.group(1), src[m.end():]
    desc = re.search(r"^description: (.*)$", front, re.M).group(1)
    body = body.replace("wargame/profiles/%s/" % side, "companies/%s/" % side)
    for pat, rep in RUN_SUBS:
        body = re.sub(pat, rep, body)
    if "## Your files" in body:
        body = body.replace("## Your files\n", "## Your files\n\n" + FILES_NOTE % side + "\n", 1)
    see = SEE_BOARD if name.endswith("-board") else SEE_EXEC
    body, k = re.subn(r"## Independence\n.*?(?=\n## )", (INDEPENDENCE % see) + "\n", body, flags=re.S)
    assert k == 1, name
    left = [l for l in body.splitlines() if LEFT.search(l)]
    return "> Agent definition used in the original game: %s\n\n%s" % (desc, body.strip()), left


FACTS = r"""
import json, os, sys
sys.path.insert(0, '.')
import model as M, briefs as B, rules as R
st = lambda k: json.load(open(os.path.join('..', 'runs', 'dash-2050-cons', 'state_r%d.json' % k)))
standing = {}
for n in (1, 2, 3, 4):
    s = st(n - 1)
    sd = s.get('sd') or {}
    standing[str(n)] = {}
    for side, f in R.ORDER_FIELDS.items():
        o = {k: v[0] for k, v in f.items()}
        if side == 'boeing':
            o['fps_site'] = sd.get('fps_site', 'new_site')
            if M.live(s, 'fps'): o['fps_engine_code'] = s['codes'].get('fps')
        if side == 'airbus':
            o['a320_plan'] = sd.get('a320_plan', 'base')
            if M.live(s, 'ngsa'): o['ngsa_engine_code'] = s['codes'].get('ngsa')
        standing[str(n)][side] = o
s4 = st(4)
v = M.value(s4, covert=True, series=True)
final = {side: [[lab, ok, det] for lab, ok, det in B.objective_status(side, s4, v)] for side in M.SIDES}
print(json.dumps({'standing': standing, 'final_status': final}))
"""


def game_facts():
    """From the original run: each company's standing position before each round, and Control's objectives at the end."""
    import subprocess
    r = subprocess.run([sys.executable, "-c", FACTS], cwd=DG, capture_output=True, text=True, check=True,
                       env=dict(os.environ, DASH_RUN="dash-2050-cons"))
    return json.loads(r.stdout.strip().splitlines()[-1])


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


SPOILERS = ("RESULTS_AS_PLAYED.md", os.path.join("engine", "reference"))


def zip_pack(players=False):
    """The full pack (for the operator), or the players' pack: the same without the original game's record. Games
    played inside the built folder (engine/runs/<game>) are never zipped; the starting position is."""
    z = os.path.join(HERE, "dash-2050-cons-llm%s.zip" % ("-players" if players else ""))
    keep_runs = os.path.join("engine", "runs", "dash-2050-cons-start") + os.sep
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(OUT):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__")
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, OUT)
                if rel.startswith(os.path.join("engine", "runs") + os.sep) and not rel.startswith(keep_runs):
                    continue
                if players and rel.startswith(SPOILERS):
                    continue
                zf.write(p, os.path.join("dash-2050-cons-llm", rel))
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
    shutil.copy(os.path.join(SRC, "protocol.json"), os.path.join(OUT, "engine", "protocol.json"))
    ctx = {"consts": consts, "rules_md": open(rec_path("rules.md"), encoding="utf-8").read(), "doctrine": doctrine(),
           "agents": AGENTS, "played": played,
           "decisions": json.load(open(os.path.join(OUT, "engine", "reference", "played_decisions.json"), encoding="utf-8"))}
    ctx.update(game_facts())
    ctx["cards"], ctx["full"] = {}, {}
    os.makedirs(os.path.join(OUT, "personas"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "personas_full"), exist_ok=True)
    for side, names in AGENTS.items():
        for a in names:
            card = open(os.path.join(SRC, "personas", a + ".md"), encoding="utf-8").read().strip()
            ctx["cards"][a] = card
            ctx["full"][a], left = adapt_agent(side, a)
            assert not left, (a, left)
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
    zp = zip_pack(players=True)
    for f in ("GAME_SCRIPT.md", "README.md", "RESULTS_AS_PLAYED.md"):
        p = os.path.join(OUT, f)
        print("%-24s %7d words" % (f, len(open(p, encoding="utf-8").read().split())))
    for side in SIDES:
        p = os.path.join(OUT, "kits", "COMPANY_%s.md" % side)
        print("kits/COMPANY_%-14s %7d words" % (side + ".md", len(open(p, encoding="utf-8").read().split())))
    for x in (z, zp):
        print("zip", x, os.path.getsize(x) // 1024, "KB")


if __name__ == "__main__":
    main()
