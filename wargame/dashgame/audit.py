"""Isolation audit for one round of dash-2050, from the workflow transcripts.

For each player agent it lists every path it touched (Read and Grep/Glob paths, and every path-like token in a Bash
command, resolved against a leading `cd`), and flags any path outside the player's own folders:
- wargame/profiles/<own>/ and /tmp/wargame-<own>/;
- the session's tool-results files, but only those the agent's own tool calls produced (their "saved to" path
  appears in the agent's own transcript).
It also scans every tool output the agent received for another player's private material: another player's
private-brief header, or the covert Delay Tactics line in a non-Airbus agent's output. It also records hook denials
and engine commands.

  python3 audit.py <round> <workflow transcript dir>   # writes ../runs/dash-2050/audit_rN.json
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
RUN_DIR = os.path.join(HERE, "..", "runs", os.environ.get("DASH_RUN", "dash-2050"))
OWN = {"boeing-strategist": "boeing", "airbus-strategist": "airbus", "cfm-strategist": "cfm",
       "pratt-whitney-strategist": "pratt_whitney", "rolls-royce-strategist": "rolls_royce"}
NAMES = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}


def _text(content):
    if isinstance(content, str):
        return content
    return " ".join(c.get("text", "") if isinstance(c, dict) else str(c) for c in (content or []))


def bash_paths(cmd, cwd):
    body = cmd.split("\n")[0] if "<<" in cmd else cmd
    quoted = []

    def _q(m):
        quoted.append(m.group(0)[1:-1])
        return " QSTR%d " % (len(quoted) - 1)
    bare = re.sub(r"'[^']*'|\"(?:[^\"\\\\]|\\\\.)*\"", _q, body)
    wd, out = cwd or REPO, []
    for seg in re.split(r"\s*(?:&&|\|\||;|\|)\s*", bare):
        seg = seg.strip()
        m = re.match(r"cd\s+(\S+)$", seg)
        if m:
            d = m.group(1)
            d = quoted[int(d[4:])] if d.startswith("QSTR") else d
            wd = os.path.realpath(d if d.startswith("/") else os.path.join(wd, d))
            out.append(wd)
            continue
        for t in re.split(r"[\s<>]+", seg):
            if t.startswith("QSTR"):
                t = quoted[int(t[4:])]
            if t and not t.startswith("-") and re.fullmatch(r"[\w./~*?\[\]{}+-]+", t) and ("/" in t or t in (".", "..")):
                out.append(os.path.realpath(t if t.startswith("/") else os.path.join(wd, t)))
    return out


def audit(tdir):
    out = {}
    for f in sorted(glob.glob(os.path.join(tdir, "agent-*.jsonl"))):
        meta_f = f[:-6] + ".meta.json"
        at = json.load(open(meta_f)).get("agentType", "") if os.path.exists(meta_f) else ""
        side = OWN.get(at)
        if not side:
            continue
        roots = [os.path.join(REPO, "wargame", "profiles", side), "/tmp/wargame-" + side]
        paths, denied, engine, leaks, own_saved, calls = [], [], [], [], set(), 0
        cwd = None
        lines = [json.loads(x) for x in open(f) if x.strip()]
        for d in lines:                                  # tool-results files produced by this agent's own calls
            m = d.get("message", {})
            if m.get("role") == "user" and isinstance(m.get("content"), list):
                for c in m["content"]:
                    if c.get("type") == "tool_result":
                        own_saved.update(re.findall(r"(/root/\.claude/projects/\S+?/tool-results/\S+?\.txt)", _text(c.get("content"))))
        for d in lines:
            cwd = d.get("cwd", cwd)
            m = d.get("message", {})
            if m.get("role") == "assistant":
                for c in m.get("content", []):
                    if c.get("type") != "tool_use":
                        continue
                    calls += 1
                    ti = c["input"]
                    if c["name"] == "Read":
                        paths.append(os.path.realpath(ti.get("file_path", "")))
                    elif c["name"] in ("Grep", "Glob"):
                        paths.append(os.path.realpath(ti.get("path") or cwd or REPO))
                    elif c["name"] == "Bash":
                        paths += bash_paths(ti.get("command", ""), cwd)
                        if "wargame.engine" in ti.get("command", ""):
                            engine.append(ti["command"][:160])
            if m.get("role") == "user" and isinstance(m.get("content"), list):
                for c in m["content"]:
                    if c.get("type") != "tool_result":
                        continue
                    t = _text(c.get("content"))
                    if "War-game isolation" in t:
                        denied.append(t[:240])
                    for other, nm in NAMES.items():
                        if other != side and ("# %s — private brief" % nm) in t:
                            leaks.append("another player's private brief: " + nm)
                    if side != "airbus" and "Covert (known only to you" in t:
                        leaks.append("covert Delay Tactics line")

        def ok(p):
            return any(p == r or p.startswith(r + "/") for r in roots) or p in own_saved
        uniq = sorted(set(paths))
        foreign = [p for p in uniq if not ok(p)]
        out[side] = {"agent_type": at, "tool_calls": calls, "paths": uniq, "foreign_paths": foreign, "denied": denied,
                     "engine_commands": engine, "leaks_in_outputs": sorted(set(leaks)),
                     "own_tool_results_read": sorted(p for p in uniq if p in own_saved),
                     "clean": not (foreign or denied or engine or leaks)}
    return out


if __name__ == "__main__":
    n, tdir = int(sys.argv[1]), sys.argv[2]
    res = audit(tdir)
    with open(os.path.join(RUN_DIR, "audit_r%d.json" % n), "w") as f:
        json.dump(res, f, indent=1)
    for s, r in res.items():
        print("%-14s calls %3d  paths %3d  clean=%s  foreign=%s denied=%d engine=%d leaks=%s own-tool-results=%d" % (
            s, r["tool_calls"], len(r["paths"]), r["clean"], r["foreign_paths"], len(r["denied"]), len(r["engine_commands"]),
            r["leaks_in_outputs"], len(r["own_tool_results_read"])))
