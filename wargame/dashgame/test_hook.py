"""Isolation hook checks: known bypasses are denied, own access is allowed, and every tool call the players made in
dash-2050 (if the transcripts are present) would still be allowed.

  python3 test_hook.py [workflow transcript dirs ...]
"""
import glob
import json
import os
import re
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
    ("boeing-malave", "Read", {"file_path": "/tmp/wargame-boeing/dash-2050-exco/exco/r1_frame.md"}, "allow"),
    ("cfm-ali", "Grep", {"pattern": "\"exec_id\": \"ali\"", "path": REPO + "/wargame/profiles/cfm/executives"}, "allow"),
    ("rolls-royce-mccabe", "Read", {"file_path": REPO + "/.claude/agents/rolls-royce-erginbilgic.md"}, "allow"),
    ("pratt-whitney-calio", "Bash", {"command": "grep -n mitchill " + REPO + "/wargame/profiles/pratt_whitney/executives/teams.md"}, "allow"),
    ("airbus-faury", "Bash", {"command": "ls /tmp/wargame-airbus/dash-2050-exco/exco/"}, "allow"),
    # executives: not the earlier dash-2050 run, the archive, transcripts, game-master modules or the 2010 agents
    ("boeing-malave", "Read", {"file_path": "/tmp/wargame-boeing/dash-2050/my_orders_r1.json"}, "deny"),
    ("cfm-ghai", "Read", {"file_path": "/tmp/wargame-archive/cfm/dash-2050/r2_rationale.txt"}, "deny"),
    ("boeing-strategist", "Read", {"file_path": "/tmp/wargame-archive/boeing/final_r1.json"}, "deny"),
    ("boeing-malave", "Read", {"file_path": "/root/.claude/projects/-home-user-aero-engine-gameboard/abc.jsonl"}, "deny"),
    ("rolls-royce-watson", "Bash", {"command": "tail -c 2000 /root/.claude/projects/p/s.jsonl"}, "deny"),
    ("airbus-toepfer", "Bash", {"command": "python3 -c \"import wargame.dashgame.rules\""}, "deny"),
    ("pratt-whitney-eddy", "Bash", {"command": "python3 -c \"from wargame import engine\""}, "deny"),
    ("boeing-ortberg", "Read", {"file_path": REPO + "/.claude/agents/airbus-2010.md"}, "deny"),
    ("boeing-malave", "Read", {"file_path": "/tmp/wargame-boeing/dash-2050-exco/round2.md"}, "allow"),
    ("boeing-malave", "Read", {"file_path": "/root/.claude/projects/p/s/tool-results/abc123.txt"}, "allow"),
    # boards: their company's limits
    ("boeing-board", "Read", {"file_path": REPO + "/wargame/profiles/airbus/board/board.md"}, "deny"),
    ("airbus-board", "Read", {"file_path": REPO + "/.claude/agents/boeing-board.md"}, "deny"),
    ("rolls-royce-board", "Read", {"file_path": "/tmp/wargame-pratt_whitney/dash-2050-exco/round1.md"}, "deny"),
    ("cfm-board", "Bash", {"command": "python3 -m wargame.engine brief --run x --side cfm"}, "deny"),
    ("pratt-whitney-board", "Grep", {"pattern": "veto", "path": "/tmp"}, "deny"),
    ("boeing-ortberg", "Read", {"file_path": REPO + "/wargame/profiles/airbus/board/evidence.jsonl"}, "deny"),
    ("boeing-board", "Read", {"file_path": REPO + "/wargame/profiles/boeing/board/board.md"}, "allow"),
    ("cfm-board", "Read", {"file_path": "/tmp/wargame-cfm/dash-2050-exco/exco/r1_decision.md"}, "allow"),
    ("rolls-royce-board", "Read", {"file_path": REPO + "/.claude/agents/rolls-royce-erginbilgic.md"}, "allow"),
]
sys.path.insert(0, os.path.dirname(HOOK))
import wargame_isolation as W  # noqa: E402
N_STATIC = len(CASES)                                                  # fixed cases
N_EXEC = sum(1 for c in CASES if any(c[0] in v for v in W.EXECS.values()))   # of which on the executive agents
# Every path an executive agent's own file tells it to read ("## Your files") must be allowed for that agent.
for side, names in W.EXECS.items():
    for n in names:
        f = os.path.join(REPO, ".claude", "agents", n + ".md")
        if not os.path.exists(f):
            continue
        txt = open(f).read()
        sec = txt[txt.find("## Your files"):txt.find("## Your step")]
        for path in sorted(set(re.findall(r"`([^`\s]*/[^`\s]*)`", sec))):
            path = path.replace("roundN", "round1").replace("<run>", "dash-2050-exco")
            if path.endswith("/") and not path.startswith("/tmp"):
                continue
            full = path if path.startswith("/") else os.path.join(REPO, path)
            CASES.append((n, "Read", {"file_path": full.rstrip("/") + ("/x.md" if path.endswith("/") else "")}, "allow"))
N_PATHS = len(CASES) - N_STATIC


def run():
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


if __name__ == "__main__":
    run()
