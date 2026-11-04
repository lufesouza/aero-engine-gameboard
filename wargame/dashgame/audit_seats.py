"""Audit, after the fact, the tool calls of seats that ran as general-purpose agents (their agent type could not be
loaded in the session, so the isolation hook did not see them): every Read, Bash, Grep, Glob, Write and Edit call is
replayed through .claude/hooks/wargame_isolation.py as the seat's own agent type, and every write must land in the
seat's own work folder. Seats are recognised by the workflow label "<side>:<step>" (e.g. embraer:frame).

  python3 audit_seats.py <run> <workflow transcript dir> ...     # prints a summary; exit 1 on any denial
"""
import glob
import json
import os
import subprocess
import sys

REPO = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
HOOK = os.path.join(REPO, ".claude", "hooks", "wargame_isolation.py")
SEAT = {"embraer": {"frame": "ceo", "decide": "ceo", "revise": "ceo", "board:revise": "ceo", "test:cfo": "cfo", "veto:cfo": "cfo",
                    "test:ops": "ops", "veto:ops": "ops", "board:guidance": "board", "board:review": "board", "board:confirm": "board"}}
AGENT = {"embraer": {"ceo": "embraer-gomes-neto", "cfo": "embraer-santana", "ops": "embraer-meijer", "board": "embraer-board"}}


def decide(agent, tool, ti, cwd):
    out = subprocess.run(["python3", HOOK], input=json.dumps({"agent_type": agent, "tool_name": tool, "tool_input": ti, "cwd": cwd}),
                         capture_output=True, text=True).stdout
    return "deny" if "deny" in out else "allow"


def main(run, dirs):
    calls = den = 0
    bad_writes, rows = [], []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "agent-*.jsonl"))):
            meta = json.load(open(f[:-6] + ".meta.json"))
            lab = meta.get("description", "")
            side, _, step = lab.partition(":")
            if side not in SEAT or meta.get("agentType") != "general-purpose":
                continue
            seat = SEAT[side].get(step)
            agent = AGENT[side][seat]
            work = "/tmp/wargame-%s/%s/work/" % (side, run)
            cwd, n, dn = None, 0, []
            for line in open(f):
                x = json.loads(line)
                cwd = x.get("cwd", cwd)
                m = x.get("message", {})
                if m.get("role") != "assistant":
                    continue
                for c in m.get("content", []) or []:
                    if c.get("type") != "tool_use":
                        continue
                    name, ti = c["name"], c.get("input", {})
                    if name in ("Write", "Edit", "NotebookEdit"):
                        if not str(ti.get("file_path", "")).startswith(work):
                            bad_writes.append((lab, ti.get("file_path")))
                        continue
                    if name not in ("Read", "Bash", "Grep", "Glob"):
                        continue
                    n += 1
                    if decide(agent, name, ti, cwd) == "deny":
                        dn.append(json.dumps(ti)[:240])
            calls += n
            den += len(dn)
            rows.append({"label": lab, "agent": agent, "calls": n, "denied": dn})
    print("seats audited: %d agents, %d tool calls, %d would be denied, %d writes outside the work folder" % (
        len(rows), calls, den, len(bad_writes)))
    for r in rows:
        print("  %-24s %-20s %3d calls%s" % (r["label"], r["agent"], r["calls"], ("  DENIED: " + " | ".join(r["denied"])) if r["denied"] else ""))
    for w in bad_writes:
        print("  WRITE OUTSIDE WORK:", w)
    return 1 if (den or bad_writes) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
