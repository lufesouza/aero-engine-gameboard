"""Isolation hook checks: known bypasses are denied, own access is allowed, and every tool call the players made in
dash-2050 (if the transcripts are present) would still be allowed.

  python3 test_hook.py [workflow transcript dirs ...]
"""
import glob
import json
import os
import subprocess
import sys

REPO = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
HOOK = os.path.join(REPO, ".claude", "hooks", "wargame_isolation.py")


def decide(agent, tool, ti, cwd=REPO):
    out = subprocess.run(["python3", HOOK], input=json.dumps({"agent_type": agent, "tool_name": tool, "tool_input": ti,
                                                               "cwd": cwd}), capture_output=True, text=True).stdout
    return "deny" if "deny" in out else "allow"


B = "boeing-strategist"
CASES = [
    (B, "Bash", {"command": "cat /tmp/wargame-*/dash-2050/round3.md"}, "deny"),
    (B, "Grep", {"pattern": "Covert", "path": "/tmp"}, "deny"),
    (B, "Grep", {"pattern": "delay_tactics"}, "deny"),
    ("cfm-strategist", "Grep", {"pattern": "x", "path": REPO + "/wargame/profiles"}, "deny"),
    (B, "Read", {"file_path": "/tmp/claude-0/x/tasks/a.output"}, "deny"),
    (B, "Read", {"file_path": "/root/.claude/projects/p/s/subagents/workflows/wf/agent-1.jsonl"}, "deny"),
    (B, "Bash", {"command": "grep -rn Covert /tmp"}, "deny"),
    (B, "Bash", {"command": "grep -rn Covert '/tmp'"}, "deny"),
    (B, "Bash", {"command": "cat $(ls /tmp/wargame-a*)"}, "deny"),
    (B, "Bash", {"command": "cat \"$(ls /tmp)\""}, "deny"),
    (B, "Read", {"file_path": "/tmp/wargame-boeing/../wargame-airbus/dash-2050/round1.md"}, "deny"),
    (B, "Bash", {"command": "find /tmp -name round1.md"}, "deny"),
    (B, "Bash", {"command": "cd /tmp && cat wargame-a*/dash-2050/round1.md"}, "deny"),
    (B, "Bash", {"command": "cd " + REPO + "/wargame/profiles && grep -rn delay ."}, "deny"),
    (B, "Bash", {"command": "cd " + REPO + "/wargame/profiles/boeing && cat ../airbus/profile.md"}, "deny"),
    (B, "Bash", {"command": "python3 -c \"import glob;print(glob.glob('/tmp/wargame-*'))\""}, "deny"),
    (B, "Bash", {"command": "grep -r Covert"}, "deny"),
    (B, "Read", {"file_path": REPO + "/wargame/dashgame/board/Game.txt"}, "deny"),
    (B, "Read", {"file_path": "/tmp/wargame-boeing/dash-2050/round1.md"}, "allow"),
    (B, "Bash", {"command": "ls /tmp/wargame-boeing/dash-2050/*.md"}, "allow"),
    (B, "Bash", {"command": "cd " + REPO + "/wargame/profiles/boeing/executives; awk '/^## 9\\. `x`/,/^## 10/' teams.md"}, "allow"),
    (B, "Read", {"file_path": "/root/.claude/projects/p/s/tool-results/brgln74ym.txt"}, "allow"),
    (B, "Bash", {"command": "python3 -m wargame.engine brief --run x --side boeing"}, "allow"),
    ("claude", "Grep", {"pattern": "x"}, "allow"),
    # per-executive agents: their company strategist's limits, no engine at all, colleagues' agent files allowed
    ("boeing-malave", "Read", {"file_path": "/tmp/wargame-airbus/dash-2050/round1.md"}, "deny"),
    ("boeing-malave", "Read", {"file_path": REPO + "/wargame/profiles/airbus/executives/toepfer.md"}, "deny"),
    ("boeing-ortberg", "Read", {"file_path": REPO + "/.claude/agents/airbus-faury.md"}, "deny"),
    ("boeing-strategist", "Read", {"file_path": REPO + "/.claude/agents/airbus-faury.md"}, "deny"),
    ("cfm-ghai", "Read", {"file_path": REPO + "/.claude/agents/rolls-royce-mccabe.md"}, "deny"),
    ("rolls-royce-strategist", "Read", {"file_path": REPO + "/.claude/agents/pratt-whitney-eddy.md"}, "deny"),
    ("wargame-market", "Read", {"file_path": REPO + "/.claude/agents/cfm-culp.md"}, "deny"),
    ("airbus-toepfer", "Bash", {"command": "python3 -m wargame.engine brief --run x --side airbus"}, "deny"),
    ("airbus-wagner", "Read", {"file_path": REPO + "/wargame/reports/dash-2050/record/record_r1.json"}, "deny"),
    ("rolls-royce-watson", "Grep", {"pattern": "Covert", "path": "/tmp"}, "deny"),
    ("pratt-whitney-eddy", "Read", {"file_path": "/tmp/claude-0/s/scratchpad/exco/draft/pratt-whitney-calio.json"}, "deny"),
    ("cfm-ali", "Bash", {"command": "cat /tmp/wargame-*/dash-2050/exco/*.md"}, "deny"),
    ("boeing-pope", "Read", {"file_path": REPO + "/wargame/profiles/boeing/executives/pope.md"}, "allow"),
    ("boeing-malave", "Read", {"file_path": "/tmp/wargame-boeing/dash-2050/exco/r1_frame.md"}, "allow"),
    ("cfm-ali", "Grep", {"pattern": "\"exec_id\": \"ali\"", "path": REPO + "/wargame/profiles/cfm/executives"}, "allow"),
    ("rolls-royce-mccabe", "Read", {"file_path": REPO + "/.claude/agents/rolls-royce-erginbilgic.md"}, "allow"),
    ("pratt-whitney-calio", "Bash", {"command": "grep -n mitchill " + REPO + "/wargame/profiles/pratt_whitney/executives/teams.md"}, "allow"),
    ("airbus-faury", "Bash", {"command": "ls /tmp/wargame-airbus/dash-2050/exco/"}, "allow"),
]
bad = [(c, decide(*c[:3])) for c in CASES if decide(*c[:3]) != c[3]]
print("hook cases: %d of %d as expected" % (len(CASES) - len(bad), len(CASES)))
for c, got in bad:
    print("  UNEXPECTED", got, c)
tot, den = 0, []
for tdir in sys.argv[1:]:
    for f in glob.glob(os.path.join(tdir, "agent-*.jsonl")):
        at = json.load(open(f[:-6] + ".meta.json")).get("agentType")
        cwd = None
        for line in open(f):
            d = json.loads(line)
            cwd = d.get("cwd", cwd)
            m = d.get("message", {})
            if m.get("role") == "assistant":
                for c in m.get("content", []):
                    if c.get("type") == "tool_use" and c["name"] in ("Read", "Bash", "Grep", "Glob"):
                        tot += 1
                        if decide(at, c["name"], c["input"], cwd) == "deny":
                            den.append((at, json.dumps(c["input"])[:200]))
if tot:
    print("game tool calls replayed: %d, would be denied: %d" % (tot, len(den)))
    for x in den:
        print("  ", x)
sys.exit(1 if (bad or den) else 0)
