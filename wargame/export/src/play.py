#!/usr/bin/env python3
"""Game engine for the Boeing vs Airbus war game "dash-2050-cons" (portable copy).

Needs Python 3.9+ with numpy and pandas (tested: Python 3.11-3.13, numpy 2.4.6, pandas 3.0-3.1; see requirements.txt).
plotly is optional (a stub is used if it is missing). No network. Every game lives in runs/<game>/ next to this file;
each company's own copy of what it may see is in runs/<game>/players/<company>/.
Companies: boeing, airbus, cfm, pratt_whitney, rolls_royce. Rounds: 1 = 2030, 2 = 2035, 3 = 2045, 4 = 2050.

  python3 play.py new <game> [--force]           start a game at the 2030 position (--force: start it again, deleting it)
  python3 play.py brief <game> <round>           public bulletin + one private brief per company
  python3 play.py orders-template <game> <round> [company]
                                                 an orders file to fill in (GAME MASTER ONLY: its legal values can
                                                 reveal a covert order)
  python3 play.py check <game> <round> <orders.json> [more.json ...]
                                                 validate orders without adjudicating; shows every adjustment
  python3 play.py adjudicate <game> <round> <orders.json> [more.json ...]
                                                 validate and adjudicate (one file for all five companies, or one
                                                 file per company); prints the public events and every value
  python3 play.py undo <game> <round> [--notes]  take back the adjudication of a round and everything after it
                                                 (--notes: also delete that round's deliberation notes)
  python3 play.py status <game>                  values, yields and Control's objectives after the last round
  python3 play.py reveal <game>                  covert Delay Tactics (GAME MASTER ONLY; reveal at the end)
  python3 play.py save <game>                    zip the game to <game>.zip in the current folder (keep it safe
                                                 between rounds: chat sandboxes are reset)
  python3 play.py load <game.zip>                restore a saved game
  python3 play.py selftest                       replays the original game and checks the engine (needs reference/,
                                                 which is in the full pack only); prints PASS or FAIL per round and
                                                 nothing about the original game

Values are $B of present value (2026) against the status quo (nobody launches anything), at each company's own cost
of capital. Orders: per company {"orders": {field: value, ...}, "public_statement": "...", "other_moves": [{"move":
"...", "public": true, "detail": "..."}]}; an engine code is JSON null or an integer 1-7.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DASHGAME = os.path.join(HERE, "dashgame")
RUNS = os.path.join(HERE, "runs")
STUBS = os.path.join(HERE, "_stubs")
START = "dash-2050-cons-start"
ROUNDS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
FIELDS = {"boeing": ["fps", "fps_engine_code", "rate_737", "re787", "fps_site"],
          "airbus": ["ngsa", "ngsa_engine_code", "rea350", "delay_tactics", "a320_plan"],
          "cfm": ["ducted", "open_fan", "partner_embraer", "lobby_emissions", "genx"],
          "pratt_whitney": ["gtf2_solo", "jv_with_rr"],
          "rolls_royce": ["ultrafan_nb_solo", "jv_with_pw", "ultrafan_wb", "t1000_upgrade"]}
try:
    ME = "python3 " + os.path.relpath(os.path.abspath(__file__))
except ValueError:                      # Windows: the pack is on another drive
    ME = "python3 " + os.path.abspath(__file__)
for _stream in (sys.stdout, sys.stderr):  # the briefs and values print Δ, −, ≥: never fail on a narrow console
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Runs a snippet inside the engine with DASH_RUN set (the engine reads it when it loads). The plotly stub goes at the
# END of the module path, so a real plotly is used when one is installed.
BOOT = ("import sys, os; sys.path.insert(0, %r); sys.path.append(%r); os.chdir(%r)\n" % (DASHGAME, STUBS, DASHGAME))


def _py(game, code, args=(), quiet=False):
    env = dict(os.environ, DASH_RUN=game, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    env.pop("DASH_BOARD", None)
    env.pop("DASH_SD", None)
    r = subprocess.run([sys.executable, "-c", BOOT + code] + list(args), env=env, capture_output=quiet, text=True,
                       encoding="utf-8")
    if r.returncode:
        if quiet:
            sys.stderr.write((r.stdout or "") + (r.stderr or ""))
        sys.exit(r.returncode)
    return r.stdout if quiet else ""


def _gm(game, *args, quiet=False):
    return _py(game, "import runpy; sys.argv = ['gm.py'] + sys.argv[1:]; runpy.run_path('gm.py', run_name='__main__')",
               args, quiet)


def _rd(game):
    return os.path.join(RUNS, game)


def _game(game):
    if not os.path.exists(os.path.join(_rd(game), "state_r0.json")):
        sys.exit("no game %r: start it with: %s new %s" % (game, ME, game))


def _round(x):
    try:
        n = int(x)
    except ValueError:
        sys.exit("the round is a number from 1 to 4 (1 = 2030, 2 = 2035, 3 = 2045, 4 = 2050), not %r" % x)
    if n not in ROUNDS:
        sys.exit("the round is a number from 1 to 4 (1 = 2030, 2 = 2035, 3 = 2045, 4 = 2050), not %d" % n)
    return n


def _exists(game, name):
    return os.path.exists(os.path.join(_rd(game), name))


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit("no file %s" % path)
    except json.JSONDecodeError as e:
        sys.exit("%s is not valid JSON: %s (line %d, column %d)" % (path, e.msg, e.lineno, e.colno))


def new(game, force=False):
    if game == START or not re.match(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", game):
        sys.exit("choose a game name that starts with a letter or digit, then letters, digits, '-', '_' or '.' (not %r)" % game)
    d = _rd(game)
    if os.path.exists(d):
        if not force:
            sys.exit("game %s exists. To start it again (this DELETES every round of it): %s new %s --force" % (game, ME, game))
        shutil.rmtree(d)
    shutil.copytree(os.path.join(RUNS, START), d)
    for side in SIDES:
        os.makedirs(os.path.join(d, "players", side), exist_ok=True)
        shutil.copy(os.path.join(d, "rules.md"), os.path.join(d, "players", side, "rules.md"))
    print("new game", game, "at", d)
    print("next: %s brief %s 1" % (ME, game))


def brief(game, n, quiet=False):
    _game(game)
    if not _exists(game, "state_r%d.json" % (n - 1)):
        sys.exit("round %d needs round %d adjudicated first" % (n, n - 1))
    out = _gm(game, "brief", str(n), quiet=True)
    if quiet:
        return
    print("\n".join(l for l in out.splitlines() if "exco_round.js" not in l))
    d = _rd(game)
    print("\nwritten:")
    print("  public bulletin:", os.path.join(d, "bulletin_r%d.md" % n))
    for side in SIDES:
        print("  %-14s %s" % (side, os.path.join(d, "players", side, "round%d.md" % n)))
    print("each company's file holds the bulletin followed by its private brief; give a company only its own file.")


def orders_template(game, n, only=None):
    _game(game)
    if not _exists(game, "state_r%d.json" % (n - 1)):
        sys.exit("round %d needs round %d adjudicated first" % (n, n - 1))
    if only and only not in SIDES:
        sys.exit("unknown company %r (use %s)" % (only, ", ".join(SIDES)))
    out = os.path.join(_rd(game), "orders_r%d_%stemplate.json" % (n, (only + "_") if only else ""))
    code = r"""
import json, rules as R
n, out, only = int(sys.argv[1]), sys.argv[2], sys.argv[3]
year = R.ROUNDS[n - 1]
s = json.load(open(os.path.join('..', 'runs', os.environ['DASH_RUN'], 'state_r%d.json' % (n - 1)), encoding='utf-8'))
sd = s.get('sd') or {}
standing = {'boeing': {'fps_site': sd.get('fps_site', 'new_site')}, 'airbus': {'a320_plan': sd.get('a320_plan', 'base')}}
t = {'_how': 'GAME MASTER ONLY (the legal values can reveal a covert order). One value per field from _legal; the '
             'first legal value is the default (hold / none / null, or the standing supply plan). public_statement is a '
             'string published in the next bulletin; other_moves is a list of objects {"move": "...", "public": true or '
             'false, "detail": "..."}, narrative only. An engine code is JSON null or an integer 1-7.'}
for side in R.ORDER_FIELDS:
    if only != '-' and side != only:
        continue
    legal = R.legal_options(s, side, year)
    o = {k: (standing.get(side, {}).get(k, v[0])) for k, v in R.ORDER_FIELDS[side].items()}
    t[side] = {'orders': o, 'public_statement': '', 'other_moves': [],
               '_legal': {k: legal.get(k, R.ORDER_FIELDS[side][k]) for k in R.ORDER_FIELDS[side]}}
json.dump(t, open(out, 'w', encoding='utf-8'), indent=1)
print('wrote', out)
"""
    _py(game, code, [str(n), out, only or "-"])


def _read_orders(paths):
    """One file for all five companies, or one block per company. Returns ({side: block}, notes, errors)."""
    x, notes, errs = {}, [], []
    for path in paths:
        part = _load_json(path)
        if not isinstance(part, dict):
            errs.append("%s: expected an object keyed by company (%s)" % (path, ", ".join(SIDES)))
            continue
        for side, block in part.items():
            if side.startswith("_"):
                continue
            if side not in SIDES:
                errs.append("%s: unknown company %r (use %s)" % (path, side, ", ".join(SIDES)))
                continue
            if side in x:
                errs.append("%s: orders for %s given twice" % (path, side))
                continue
            x[side] = block
    for side, b in list(x.items()):
        if not isinstance(b, dict):
            errs.append("%s: the block must be an object with \"orders\"" % side)
            continue
        if "orders" not in b and any(k in FIELDS[side] for k in b):
            b = {"orders": {k: v for k, v in b.items() if k in FIELDS[side]},
                 **{k: v for k, v in b.items() if k not in FIELDS[side]}}
            x[side] = b
            notes.append("%s: order fields were not inside \"orders\"; read them as orders" % side)
        o = b.get("orders")
        if not isinstance(o, dict):
            errs.append("%s: \"orders\" must be an object with the fields %s" % (side, ", ".join(FIELDS[side])))
            continue
        bad = [k for k in o if k not in FIELDS[side]]
        if bad:
            errs.append("%s: unknown order field(s) %s (the fields are %s)" % (side, ", ".join(bad), ", ".join(FIELDS[side])))
        for k in [f for f in FIELDS[side] if f.endswith("_engine_code") and f in o]:
            v = o[k]
            if isinstance(v, str) and v.strip().lower() in ("none", "null", ""):
                o[k] = None
                notes.append("%s: %s %r read as null" % (side, k, v))
            elif isinstance(v, str) and v.strip().isdigit():
                o[k] = int(v.strip())
                notes.append("%s: %s %r read as the number %d" % (side, k, v, o[k]))
            elif isinstance(v, bool) or (isinstance(v, float) and not v.is_integer()):
                errs.append("%s: %s must be null or an integer 1-7, not %r" % (side, k, v))
            elif isinstance(v, float):
                o[k] = int(v)
        ps = b.get("public_statement", "")
        if not isinstance(ps, str):
            errs.append("%s: public_statement must be a string" % side)
        om = b.get("other_moves", [])
        if not isinstance(om, list) or not all(isinstance(m, dict) and isinstance(m.get("move"), str) and
                                               isinstance(m.get("public", False), bool) for m in om):
            errs.append("%s: other_moves must be a list of objects {\"move\": \"...\", \"public\": true or false, "
                        "\"detail\": \"...\"}" % side)
    return x, notes, errs


def _engine_check(game, n, x):
    """The engine's own validation (illegal values become the first legal value; cross-field rules)."""
    code = r"""
import json, rules as R
n = int(sys.argv[1]); x = json.loads(sys.argv[2])
s = json.load(open(os.path.join('..', 'runs', os.environ['DASH_RUN'], 'state_r%d.json' % (n - 1)), encoding='utf-8'))
for side in R.ORDER_FIELDS:
    o = (x.get(side) or {}).get('orders', {})
    clean, probs = R.validate(s, side, R.ROUNDS[n - 1], o)
    for p in probs:
        print('  ! %s: %s' % (side, p))
"""
    only = {side: {"orders": (b or {}).get("orders", {})} for side, b in x.items()}
    return _py(game, code, [str(n), json.dumps(only)], quiet=True)


def check(game, n, paths, quiet=False):
    _game(game)
    if not _exists(game, "state_r%d.json" % (n - 1)):
        sys.exit("round %d needs round %d adjudicated first" % (n, n - 1))
    x, notes, errs = _read_orders(paths)
    for m in notes:
        print("note:", m)
    if errs:
        print("orders not accepted:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    for side in SIDES:
        if side not in x:
            print("note: no orders for %s: it holds everything this round" % side)
    out = _engine_check(game, n, x)
    if not quiet:
        print(out.rstrip() if out.strip() else "every order is legal as given")
    return x


def adjudicate(game, n, paths):
    _game(game)
    if not _exists(game, "grids_r%d.json" % n):         # the briefing writes it last
        sys.exit("write the round's briefs first: %s brief %s %d" % (ME, game, n))
    if _exists(game, "record_r%d.json" % n):
        sys.exit("round %d of %s is already adjudicated (to take it back: %s undo %s %d)" % (n, game, ME, game, n))
    if _exists(game, "state_r%d.json" % n):       # left by an adjudication that stopped half way
        os.remove(os.path.join(_rd(game), "state_r%d.json" % n))
    x = check(game, n, paths, quiet=True)
    clean = {side: {k: v for k, v in (x.get(side) or {}).items() if not k.startswith("_")} for side in SIDES}
    tmp = os.path.join(_rd(game), "orders_r%d.json" % n)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=1, ensure_ascii=False)
    print(_gm(game, "adjudicate", str(n), tmp, quiet=True).rstrip())
    print("\nnext: %s brief %s %d" % (ME, game, n + 1) if n < 4 else "\ngame over: %s status %s" % (ME, game))


def undo(game, n, notes=False):
    _game(game)
    d = _rd(game)
    gone = []
    for k in range(n, 5):
        for name in ["state_r%d.json" % k, "record_r%d.json" % k, "orders_r%d.json" % k, "orders_exco_r%d.json" % k]:
            if os.path.exists(os.path.join(d, name)):
                os.remove(os.path.join(d, name)); gone.append(name)
        for name in ["bulletin_r%d.md" % (k + 1), "grids_r%d.json" % (k + 1)] + ["brief_r%d_%s.md" % (k + 1, s) for s in SIDES]:
            if os.path.exists(os.path.join(d, name)):
                os.remove(os.path.join(d, name)); gone.append(name)
        for side in SIDES:
            p = os.path.join(d, "players", side)
            for name in ["my_orders_r%d.json" % k, "round%d.md" % (k + 1)]:
                if os.path.exists(os.path.join(p, name)):
                    os.remove(os.path.join(p, name)); gone.append("players/%s/%s" % (side, name))
            ex = os.path.join(p, "exco")
            if os.path.isdir(ex):
                for f in os.listdir(ex):
                    m = re.match(r"r(\d+)_", f)
                    if m and (int(m.group(1)) > n or (notes and int(m.group(1)) == n)):
                        os.remove(os.path.join(ex, f)); gone.append("players/%s/exco/%s" % (side, f))
    print("took back round %d and after: %d files removed" % (n, len(gone)))
    print("next: %s adjudicate %s %d <orders.json>" % (ME, game, n))


def status(game):
    _game(game)
    last = max(k for k in range(0, 5) if _exists(game, "state_r%d.json" % k))
    code = r"""
import json, model as M, briefs as B
k = int(sys.argv[1])
s = json.load(open(os.path.join('..', 'runs', os.environ['DASH_RUN'], 'state_r%d.json' % k), encoding='utf-8'))
v = M.value(s, covert=True, series=True)
print('after round %d (%s)' % (k, {0: 'start, 2026', 1: '2030', 2: '2035', 3: '2045', 4: '2050'}[k]))
for side in M.SIDES:
    print('  %-16s value vs status quo %+8.2f $B   yield %6.2f%%' % (M.NAMES[side], v[side]['pv_delta'], v[side]['yield']))
print('objectives (Control, as the briefs measure them):')
for side in M.SIDES:
    for lab, ok, det in B.objective_status(side, s, v):
        print('  %-16s %-9s %s (%s)' % (M.NAMES[side], 'met' if ok else 'not met', lab, det))
pub = {k_: p for k_, p in (s.get('prog') or {}).items() if p and not k_.startswith('_')}
print('programmes on record:', json.dumps(pub, sort_keys=True))
"""
    _py(game, code, [str(last)])


def reveal(game):
    _game(game)
    last = max(k for k in range(0, 5) if _exists(game, "state_r%d.json" % k))
    s = _load_json(os.path.join(_rd(game), "state_r%d.json" % last))
    dt = {k: y for k, y in (s.get("dt") or {}).items() if y}
    print("Delay Tactics (covert): " + ("; ".join("%s ordered in %d" % (k, y) for k, y in sorted(dt.items())) if dt else "none ordered"))


def save(game):
    _game(game)
    z = os.path.abspath(game + ".zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(_rd(game)):
            for f in files:
                p = os.path.join(root, f)
                zf.write(p, os.path.relpath(p, RUNS))
    print("saved", z)


def load(path):
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        top = {n.split("/")[0] for n in names}
        if len(top) != 1 or any(".." in n or n.startswith("/") for n in names):
            sys.exit("%s is not a saved game" % path)
        game = top.pop()
        if os.path.exists(_rd(game)):
            sys.exit("game %s exists; remove engine/runs/%s first" % (game, game))
        zf.extractall(RUNS)
    print("loaded game", game)
    status(game)


def _same(a, b):
    """Equal, or equal once every number is masked (floating-point rounding: the sign of a ±0.00 or a last digit,
    and a met/not met that turns on it)."""
    if a == b:
        return "exact"
    mask = lambda t: re.sub(r"\*\*(not )?met\*\*|(not )?met\b", "MET", re.sub(r"[−+-]?\d[\d,]*(\.\d+)?", "#", t))
    return "rounding" if mask(a) == mask(b) else None


def selftest():
    ref = os.path.join(HERE, "reference")
    if not os.path.exists(os.path.join(ref, "played_orders.json")):
        sys.exit("selftest needs engine/reference/ (in the full pack only; this is the players' pack)")
    played = _load_json(os.path.join(ref, "played_orders.json"))
    game = "selftest-tmp"
    if os.path.exists(_rd(game)):
        shutil.rmtree(_rd(game))
    shutil.copytree(os.path.join(RUNS, START), _rd(game))
    for side in SIDES:
        os.makedirs(os.path.join(_rd(game), "players", side), exist_ok=True)
        shutil.copy(os.path.join(_rd(game), "rules.md"), os.path.join(_rd(game), "players", side, "rules.md"))
    ok, warn = True, False
    try:
        for n in (1, 2, 3, 4):
            _gm(game, "brief", str(n), quiet=True)
            res = []
            for part in SIDES + ["bulletin"]:
                mine = open(os.path.join(_rd(game), ("bulletin_r%d.md" % n) if part == "bulletin" else ("brief_r%d_%s.md" % (n, part))),
                            encoding="utf-8").read()
                want = open(os.path.join(ref, "briefs", "round%d_%s.md" % (n, part)), encoding="utf-8").read()
                res.append(_same(mine, want))
            path = os.path.join(_rd(game), "played_r%d.json" % n)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(played["rounds"][str(n)]["orders_file"], f, indent=1)
            _gm(game, "adjudicate", str(n), path, quiet=True)
            rec = _load_json(os.path.join(_rd(game), "record_r%d.json" % n))
            vals = all(abs(rec["value"][s]["pv_delta"] - played["rounds"][str(n)]["value"][s]) < 1e-6 for s in SIDES)
            if None in res or not vals:
                ok = False
                print("round %d: FAIL (%s)" % (n, "a brief differs" if None in res else "a value differs"))
            elif "rounding" in res:
                warn = True
                print("round %d: PASS (values identical; %d brief(s) differ only in floating-point rounding)" % (n, res.count("rounding")))
            else:
                print("round %d: PASS (6 briefs and bulletins identical, values identical)" % n)
    finally:
        shutil.rmtree(_rd(game), ignore_errors=True)
    if ok and warn:
        print("SELFTEST PASSED, with rounding differences: your numpy prints a few ±0.00 signs or last digits differently "
              "from the original's (numpy 2.4.6). For an exact replay, install the versions in requirements.txt.")
    else:
        print("SELFTEST", "PASSED: the engine reproduces the original game exactly" if ok else "FAILED")
    sys.exit(0 if ok else 1)


def main(a):
    flags = [x for x in a if x.startswith("--")]
    pos = [x for x in a if not x.startswith("--")]
    if not pos or pos[0] in ("-h", "help"):
        print(__doc__)
        return
    cmd, args = pos[0], pos[1:]
    if cmd == "new" and len(args) == 1:
        new(args[0], force="--force" in flags)
    elif cmd == "brief" and len(args) == 2:
        brief(args[0], _round(args[1]))
    elif cmd == "orders-template" and len(args) in (2, 3):
        orders_template(args[0], _round(args[1]), args[2] if len(args) == 3 else None)
    elif cmd == "check" and len(args) >= 3:
        check(args[0], _round(args[1]), args[2:])
    elif cmd == "adjudicate" and len(args) >= 3:
        adjudicate(args[0], _round(args[1]), args[2:])
    elif cmd == "undo" and len(args) == 2:
        undo(args[0], _round(args[1]), notes="--notes" in flags)
    elif cmd == "status" and len(args) == 1:
        status(args[0])
    elif cmd == "reveal" and len(args) == 1:
        reveal(args[0])
    elif cmd == "save" and len(args) == 1:
        save(args[0])
    elif cmd == "load" and len(args) == 1:
        load(args[0])
    elif cmd == "selftest":
        selftest()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
