"""Isolation audit for one round of dash-2050: which paths each player agent touched, any hook denials, and any
engine commands. Reads the workflow transcript folder.

  python3 audit.py <round> <workflow transcript dir>   # writes ../runs/dash-2050/audit_rN.json
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.join(HERE, "..", "runs", os.environ.get("DASH_RUN", "dash-2050"))
OWN = {"boeing-strategist": "boeing", "airbus-strategist": "airbus", "cfm-strategist": "cfm",
       "pratt-whitney-strategist": "pratt_whitney", "rolls-royce-strategist": "rolls_royce"}


def audit(tdir):
    out = {}
    for f in sorted(glob.glob(os.path.join(tdir, "agent-*.jsonl"))):
        meta_f = f[:-6] + ".meta.json"
        at = json.load(open(meta_f)).get("agentType", "") if os.path.exists(meta_f) else ""
        side = OWN.get(at, at)
        paths, denied, engine, calls = set(), [], [], 0
        for line in open(f):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message", {})
            if m.get("role") == "assistant":
                for c in m.get("content", []):
                    if c.get("type") == "tool_use":
                        calls += 1
                        s = json.dumps(c["input"])
                        paths.update(re.findall(r"(/tmp/wargame-[a-z_]+|wargame/[a-z_]+(?:/[a-z_]+)?)", s))
                        if "wargame.engine" in s:
                            engine.append(s[:160])
            if m.get("role") == "user" and isinstance(m.get("content"), list):
                for c in m["content"]:
                    if c.get("type") == "tool_result" and "isolation" in json.dumps(c.get("content"))[:400].lower():
                        denied.append(json.dumps(c.get("content"))[:240])
        foreign = sorted(p for p in paths if not (p.endswith("wargame-" + side) or p.startswith("wargame/profiles/" + side)
                                                  or p == "wargame/profiles"))
        out[side] = {"agent_type": at, "tool_calls": calls, "paths": sorted(paths), "foreign_paths": foreign,
                     "denied": denied, "engine_commands": engine, "clean": not (foreign or denied or engine)}
    return out


if __name__ == "__main__":
    n, tdir = int(sys.argv[1]), sys.argv[2]
    res = audit(tdir)
    with open(os.path.join(RUN_DIR, "audit_r%d.json" % n), "w") as f:
        json.dump(res, f, indent=1)
    for s, r in res.items():
        print("%-14s calls %3d  clean=%s  foreign=%s denied=%d engine=%d" % (s, r["tool_calls"], r["clean"], r["foreign_paths"],
                                                                          len(r["denied"]), len(r["engine_commands"])))
