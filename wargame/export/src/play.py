#!/usr/bin/env python3
"""Game engine for the Boeing vs Airbus war game "dash-2050-cons" (portable copy).

Needs Python 3.9+ with numpy and pandas (plotly is optional: a stub is used if it is missing). No network.
Every game lives in runs/<game>/ next to this file; each player's own copy of what it may see is in
runs/<game>/players/<side>/ (sides: boeing, airbus, cfm, pratt_whitney, rolls_royce).

  python3 play.py new <game>                      start a game at the 2030 position (copies the starting state)
  python3 play.py brief <game> <round>            bulletin + one private brief per company for round 1-4
  python3 play.py orders-template <game> <round>  an orders file to fill in (defaults, and the legal values)
  python3 play.py adjudicate <game> <round> <orders.json> [more.json ...]
                                                  validate and adjudicate the round (one file for all five companies,
                                                  or one file per company); prints every company's value
  python3 play.py status <game>                   values after the last adjudicated round, all five companies
  python3 play.py selftest                        replays the game as it was played and checks the engine's numbers

Rounds: 1 = 2030, 2 = 2035, 3 = 2045, 4 = 2050. Values are $B of present value (2026) against the status quo
(nobody launches anything), at each company's own cost of capital.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DASHGAME = os.path.join(HERE, "dashgame")
RUNS = os.path.join(HERE, "runs")
STUBS = os.path.join(HERE, "_stubs")
START = "dash-2050-cons-start"
ROUNDS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]

# Runs a snippet inside the engine with DASH_RUN set (the engine reads it when it loads). The plotly stub goes at the
# END of the module path, so a real plotly is used when one is installed.
BOOT = ("import sys, os; sys.path.insert(0, %r); sys.path.append(%r); os.chdir(%r)\n" % (DASHGAME, STUBS, DASHGAME))


def _py(game, code, args=()):
    env = dict(os.environ, DASH_RUN=game)
    env.pop("DASH_BOARD", None)
    env.pop("DASH_SD", None)
    r = subprocess.run([sys.executable, "-c", BOOT + code] + list(args), env=env)
    if r.returncode:
        sys.exit(r.returncode)


def _gm(game, *args):
    _py(game, "import runpy; sys.argv = ['gm.py'] + sys.argv[1:]; runpy.run_path('gm.py', run_name='__main__')", args)


def _rd(game):
    return os.path.join(RUNS, game)


def _need(game, path, what):
    if not os.path.exists(os.path.join(_rd(game), path)):
        sys.exit("game %s has no %s (%s)" % (game, path, what))


def new(game, force=False):
    if game == START:
        sys.exit("choose another name: %s is the starting position" % START)
    d = _rd(game)
    if os.path.exists(d):
        if not force:
            sys.exit("game %s exists (add --force to start it again)" % game)
        shutil.rmtree(d)
    shutil.copytree(os.path.join(RUNS, START), d)
    for side in SIDES:
        os.makedirs(os.path.join(d, "players", side), exist_ok=True)
        shutil.copy(os.path.join(d, "rules.md"), os.path.join(d, "players", side, "rules.md"))
    print("new game", game, "at", d)
    print("next: python3 play.py brief %s 1" % game)


def brief(game, n):
    _need(game, "state_r%d.json" % (n - 1), "adjudicate the previous round first")
    _gm(game, "brief", str(n))
    d = _rd(game)
    print("\nwritten:")
    print("  public bulletin:", os.path.join(d, "bulletin_r%d.md" % n))
    for side in SIDES:
        print("  %-14s %s" % (side, os.path.join(d, "players", side, "round%d.md" % n)))
    print("each company's file holds the bulletin followed by its private brief; give a company only its own file.")


def orders_template(game, n):
    _need(game, "state_r%d.json" % (n - 1), "adjudicate the previous round first")
    out = os.path.join(_rd(game), "orders_r%d_template.json" % n)
    code = r"""
import json, rules as R
n, out = int(sys.argv[1]), sys.argv[2]
year = R.ROUNDS[n - 1]
s = json.load(open(os.path.join('..', 'runs', os.environ['DASH_RUN'], 'state_r%d.json' % (n - 1))))
sd = s.get('sd') or {}
standing = {'boeing': {'fps_site': sd.get('fps_site', 'new_site')}, 'airbus': {'a320_plan': sd.get('a320_plan', 'base')}}
t = {'_how': 'Fill one value per field from _legal (one company per block). Default = keep: hold / none / null, and the '
             'standing supply plan. public_statement goes to the bulletin; other_moves are narrative only (public true/false).'}
for side in R.ORDER_FIELDS:
    legal = R.legal_options(s, side, year)
    o = {k: (standing.get(side, {}).get(k, v[0])) for k, v in R.ORDER_FIELDS[side].items()}
    t[side] = {'orders': o, 'public_statement': '', 'other_moves': [],
               '_legal': {k: legal.get(k, R.ORDER_FIELDS[side][k]) for k in R.ORDER_FIELDS[side]}}
json.dump(t, open(out, 'w'), indent=1)
print('wrote', out)
"""
    _py(game, code, [str(n), out])


def adjudicate(game, n, paths):
    _need(game, "state_r%d.json" % (n - 1), "adjudicate the previous round first")
    _need(game, "brief_r%d_boeing.md" % n, "write the round's briefs first: python3 play.py brief %s %d" % (game, n))
    if os.path.exists(os.path.join(_rd(game), "state_r%d.json" % n)):
        sys.exit("round %d of %s is already adjudicated (start again with: python3 play.py new %s --force)" % (n, game, game))
    x = {}
    for path in paths:                     # one file with all five companies, or one block per company
        with open(path) as f:
            part = json.load(f)
        for side, block in part.items():
            if side.startswith("_"):
                continue
            if side not in SIDES:
                sys.exit("%s: unknown company %r (use %s)" % (path, side, ", ".join(SIDES)))
            if side in x:
                sys.exit("%s: orders for %s given twice" % (path, side))
            x[side] = block
    for side in SIDES:
        if side not in x:
            print("note: no orders for %s: it holds everything this round" % side)
    clean = {side: {k: v for k, v in (x.get(side) or {}).items() if not k.startswith("_")} for side in SIDES}
    tmp = os.path.join(_rd(game), "orders_r%d.json" % n)
    with open(tmp, "w") as f:
        json.dump(clean, f, indent=1, ensure_ascii=False)
    _gm(game, "adjudicate", str(n), tmp)
    print("\nnext: python3 play.py brief %s %d" % (game, n + 1) if n < 4 else "\ngame over: python3 play.py status %s" % game)


def status(game):
    last = max([k for k in range(0, 5) if os.path.exists(os.path.join(_rd(game), "state_r%d.json" % k))], default=None)
    if last is None:
        sys.exit("no game %s" % game)
    code = r"""
import json, model as M
k = int(sys.argv[1])
s = json.load(open(os.path.join('..', 'runs', os.environ['DASH_RUN'], 'state_r%d.json' % k)))
v = M.value(s, covert=True, series=False)
print('after round %d (%s)' % (k, {0: 'start, 2026', 1: '2030', 2: '2035', 3: '2045', 4: '2050'}[k]))
for side in M.SIDES:
    print('  %-14s value vs status quo %+8.2f $B   yield %6.2f%%' % (M.NAMES[side], v[side]['pv_delta'], v[side]['yield']))
print('programmes:', json.dumps({k_: p for k_, p in (s.get('prog') or {}).items() if p}, sort_keys=True))
"""
    _py(game, code, [str(last)])


def selftest():
    ref = json.load(open(os.path.join(HERE, "reference", "played_orders.json")))
    game = "selftest"
    new(game, force=True)
    ok = True
    for n in (1, 2, 3, 4):
        brief(game, n)
        for part in SIDES + ["bulletin"]:
            mine = open(os.path.join(_rd(game), ("bulletin_r%d.md" % n) if part == "bulletin" else ("brief_r%d_%s.md" % (n, part))),
                        encoding="utf-8").read()
            want = open(os.path.join(HERE, "reference", "briefs", "round%d_%s.md" % (n, part)), encoding="utf-8").read()
            same = mine == want
            ok &= same
            print("round %d %-14s identical to the one played: %s" % (n, part, same))
        path = os.path.join(_rd(game), "played_r%d.json" % n)
        with open(path, "w") as f:
            json.dump(ref["rounds"][str(n)]["orders_file"], f, indent=1)
        adjudicate(game, n, [path])
        rec = json.load(open(os.path.join(_rd(game), "record_r%d.json" % n)))
        for side in SIDES:
            got, exp = rec["value"][side]["pv_delta"], ref["rounds"][str(n)]["value"][side]
            if abs(got - exp) > 1e-6:
                ok = False
                print("  MISMATCH round %d %s: %.6f expected %.6f" % (n, side, got, exp))
    print("\nSELFTEST", "PASSED: the engine reproduces the game as played" if ok else "FAILED")
    sys.exit(0 if ok else 1)


def main(a):
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "new" and len(a) >= 2:
        new(a[1], force="--force" in a)
    elif cmd == "brief" and len(a) == 3:
        brief(a[1], int(a[2]))
    elif cmd == "orders-template" and len(a) == 3:
        orders_template(a[1], int(a[2]))
    elif cmd == "adjudicate" and len(a) >= 4:
        adjudicate(a[1], int(a[2]), a[3:])
    elif cmd == "status" and len(a) == 2:
        status(a[1])
    elif cmd == "selftest":
        selftest()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
