"""Game-master helper for rounds played by the per-executive agents (workflows/exco_round.js). Not used yet.

  python3 exco.py check                      # the script's order fields match rules.ORDER_FIELDS
  python3 exco.py save N result.json         # ExCo notes to each company's folder; orders file for gm.py adjudicate

`save` writes, for each company, /tmp/wargame-<side>/<run>/exco/rN_<step>.md (its own ExCo and Board only) and
wargame/runs/<run>/orders_exco_rN.json in the shape `gm.py adjudicate` reads, with the whole ExCo record under
`returned.<side>.exco`.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules as R  # noqa: E402

SCRIPT = os.path.join(HERE, "workflows", "exco_round.js")
SEATS = {"cfo": "CFO", "ops": "operating head"}


def check():
    src = open(SCRIPT).read()
    m = re.search(r"// ORDER_FIELDS_BEGIN\nconst ORDER_FIELDS = (\{.*?\n\})\n// ORDER_FIELDS_END", src, re.S)
    js = json.loads(m.group(1))
    ok = js == json.loads(json.dumps(R.ORDER_FIELDS))
    print("order fields match rules.py" if ok else "ORDER FIELDS DIFFER from rules.py")
    return ok


def md(title, obj):
    return "# %s\n\n```json\n%s\n```\n" % (title, json.dumps(obj, indent=1, ensure_ascii=False))


def save(n, path):
    res = json.load(open(path))
    run = res["run"]
    returned = {}
    for side, x in res["sides"].items():
        if not x:
            continue
        d = "/tmp/wargame-%s/%s/exco" % (side, run)
        os.makedirs(d, exist_ok=True)
        notes = [("board_guidance", "Board guidance", x.get("board_guidance")),
                 ("frame", "CEO framing note", x.get("frame")), ("test_cfo", "CFO test memo", x.get("cfo")),
                 ("test_ops", "Operating head test memo", x.get("ops")), ("decision", "CEO decision", x.get("decision"))]
        for seat in ("cfo", "ops"):
            notes.append(("veto_" + seat, "%s veto check" % SEATS[seat], (x.get("veto_checks") or {}).get(seat)))
        if x.get("revision"):
            notes.append(("revision", "CEO revision after a binding veto or a red-line flag", x["revision"]))
        notes += [("board_review", "Board review", x.get("board_review")), ("board_revision", "CEO revision after a Board veto", x.get("board_revision")),
                  ("board_confirm", "Board confirmation", x.get("board_confirm"))]
        for key, title, obj in notes:
            if obj is not None:
                with open(os.path.join(d, "r%d_%s.md" % (n, key)), "w") as f:
                    f.write(md("Round %d: %s" % (n, title), obj))
        fin = dict(x.get("final") or {})
        if x.get("final_orders") is not None:
            fin["orders"] = x["final_orders"]
        fin["exco"] = {k: x.get(k) for k in ("board_guidance", "frame", "cfo", "ops", "decision", "veto_checks", "binding_vetoes",
                                             "red_line_flags", "revision", "board_items", "board_review", "board_vetoed",
                                             "board_revision", "board_confirm", "board_reverted")}
        returned[side] = fin
    out = os.path.join(HERE, "..", "runs", run, "orders_exco_r%d.json" % n)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(returned, f, indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(out, HERE), "and ExCo notes for", ", ".join(returned))


if __name__ == "__main__":
    if sys.argv[1] == "check":
        sys.exit(0 if check() else 1)
    elif sys.argv[1] == "save":
        save(int(sys.argv[2]), sys.argv[3])
