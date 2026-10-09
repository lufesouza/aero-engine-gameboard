#!/usr/bin/env python3
"""PreToolUse hook: keep the war-game agents independent.

Each strategist (Boeing, Airbus, and the optional Rolls-Royce, Pratt & Whitney and CFM/GE suppliers) may not
touch another player's profile, role card or private scratch folder, nor the
build-time work areas that hold every side's material.
No player or market agent may read run state (sealed orders live there) or run
engine commands other than read-only ones from its own side's view; only the Game
Orchestrator sees the full game-theory board (players may not run `equilibria`). The Game
Orchestrator (referee), the analyst and the main session are not restricted.

The per-executive agents (one per member of each company's default ExCo, e.g. boeing-ortberg) carry their company
strategist's restrictions, may not run any engine command, and keep to their company's own folders. Inside an ExCo,
colleagues see each other only through what the game master passes them.
"""
import json
import os
import sys

# The per-executive agents of each company's default ExCo (agent files .claude/agents/<name>.md).
EXECS = {"boeing": ["boeing-ortberg", "boeing-malave", "boeing-pope"],
         "airbus": ["airbus-faury", "airbus-toepfer", "airbus-wagner"],
         "cfm": ["cfm-culp", "cfm-ghai", "cfm-ali"],
         "pratt_whitney": ["pratt-whitney-calio", "pratt-whitney-mitchill", "pratt-whitney-eddy"],
         "rolls_royce": ["rolls-royce-erginbilgic", "rolls-royce-mccabe", "rolls-royce-watson"]}
XF = {side: [n + ".md" for n in names] for side, names in EXECS.items()}
# Build-time work areas (profile drafts, raw evidence, audits) hold both sides' material.
BUILD = ["profiles/build/work", "/scratchpad/profiles", "/scratchpad/evidence", "/scratchpad/integ",
         "/scratchpad/audit", "/scratchpad/ab_synth_work", "/scratchpad/text", "/scratchpad/rr", "/scratchpad/pw",
         "/scratchpad/engines", "/scratchpad/execs", "/scratchpad/cfm", "/scratchpad/rrx", "/scratchpad/pwx"]
RR = ["profiles/rolls_royce", "rolls-royce-strategist.md", "wargame-rolls_royce"] + XF["rolls_royce"]
PW = ["profiles/pratt_whitney", "pratt-whitney-strategist.md", "wargame-pratt_whitney"] + XF["pratt_whitney"]
CFMP = ["profiles/cfm", "cfm-strategist.md", "wargame-cfm"] + XF["cfm"]
# The cross-player overview page summarises every side, the config holds every player's assigned objective,
# and the root gameboard.py holds every engine maker's move table: no player reads them.
SHARED = ["profiles/overview", "wargame/config", "gameboard.py"]
CFM = CFMP + SHARED
AIRFRAMERS = ["profiles/boeing", "profiles/airbus", "boeing-strategist.md", "airbus-strategist.md", "boeing-2010.md",
              "airbus-2010.md", "wargame-boeing", "wargame-airbus"] + XF["boeing"] + XF["airbus"]
# Raw uploads contain every year; the period-locked 2010 players may not read them.
RAW = ["Transcripts from", "Boeing 10ks", "airbus_se_report", "GoldmanSachs", "Morgan Stanley", "NYSE BA Financials",
       "Rolls-Royce Holdings plc", "Transcript Digest", "Filings.pdf", "SEC Fillings", "Durability news", "Global Strategy Brief",
       "Company Profile.pdf", "SAF.PA", "Embraer",
       "wargame/scenarios", "referee_only", "wargame/README.md", "profiles/build"]
# The dashboard war game (dash-2050): only the game master sees the user's board, its snapshot, the
# game-master code and earlier reports (they hold every side's payoffs and private rationale).
DASH = ["Combined_Game_Board", "dashboard-fps-delay", "Game.txt", "wargame/dashgame", "uploads/", "wargame/reports",
        "/scratchpad/dash"]
BLOCK = {
    "boeing-2010": ["profiles/airbus", "profiles/boeing/", "airbus-2010.md", "airbus-strategist.md", "boeing-strategist.md",
                    "wargame/runs",
                    "wargame-airbus"] + XF["boeing"] + XF["airbus"] + RR + PW + CFM + BUILD + RAW,
    "airbus-2010": ["profiles/boeing", "profiles/airbus/", "boeing-2010.md", "boeing-strategist.md", "airbus-strategist.md",
                    "wargame/runs",
                    "wargame-boeing"] + XF["boeing"] + XF["airbus"] + RR + PW + CFM + BUILD + RAW,
    "boeing-strategist": ["profiles/airbus", "airbus-strategist.md", "wargame/runs", "wargame-airbus"] + XF["airbus"] + RR + PW + CFM + BUILD + DASH,
    "airbus-strategist": ["profiles/boeing", "boeing-strategist.md", "wargame/runs", "wargame-boeing"] + XF["boeing"] + RR + PW + CFM + BUILD + DASH,
    "rolls-royce-strategist": AIRFRAMERS + PW + CFM + ["wargame/runs"] + BUILD + DASH,
    "pratt-whitney-strategist": AIRFRAMERS + RR + CFM + ["wargame/runs"] + BUILD + DASH,
    "cfm-strategist": AIRFRAMERS + RR + PW + SHARED + ["wargame/runs"] + BUILD + DASH,
    "wargame-market": ["profiles/", "wargame/runs", "wargame/config", "gameboard.py", "wargame-boeing", "wargame-airbus",
                       "wargame-rolls_royce", "wargame-pratt_whitney", "wargame-cfm"] + sum(XF.values(), []) + BUILD + DASH,
}


PLAYER_SIDE = {"boeing-strategist": "boeing", "airbus-strategist": "airbus", "wargame-market": "market",
               "boeing-2010": "boeing", "airbus-2010": "airbus", "rolls-royce-strategist": "rolls_royce",
               "pratt-whitney-strategist": "pratt_whitney", "cfm-strategist": "cfm"}
# `equilibria` (the game-theory board) is for the Game Orchestrator only.
READ_ONLY = {"brief", "rules", "options", "whatif", "validate", "scenarios", "status"}


def engine_violation(agent, command):
    """Players may only run read-only engine commands, from their own side's point of view."""
    import re
    own = PLAYER_SIDE.get(agent)
    for m in re.finditer(r"wargame\.engine\s+(\S+)([^;&|]*)", command):
        sub, rest = m.group(1), m.group(2)
        if sub not in READ_ONLY:
            return f"engine command '{sub}'"
        sides = re.findall(r"--side[ =](\S+)", rest)
        allowed = {own, "market"} if own != "market" else {"market"}
        if any(x.strip("'\"") not in allowed for x in sides):
            return f"engine view --side {sides[0]}"
        if sub in ("options", "whatif", "brief", "rules") and not sides:
            return f"engine '{sub}' without --side {own}"
    return None


# The game master's private areas: its scratchpad and task outputs, and every agent transcript. Players' own
# persisted tool outputs live in the session's tool-results folder, which stays readable.
GM_PRIVATE = ["/tmp/claude-0/", "/subagents/", "/workflows/"]
OWN_ROOTS = {"boeing-strategist": ["wargame/profiles/boeing/", "/tmp/wargame-boeing"],
             "airbus-strategist": ["wargame/profiles/airbus/", "/tmp/wargame-airbus"],
             "cfm-strategist": ["wargame/profiles/cfm/", "/tmp/wargame-cfm"],
             "pratt-whitney-strategist": ["wargame/profiles/pratt_whitney/", "/tmp/wargame-pratt_whitney"],
             "rolls-royce-strategist": ["wargame/profiles/rolls_royce/", "/tmp/wargame-rolls_royce"],
             "boeing-2010": ["wargame/profiles/boeing_2010/", "/tmp/wargame-boeing"],
             "airbus-2010": ["wargame/profiles/airbus_2010/", "/tmp/wargame-airbus"]}
REPO = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# Each executive inherits its company strategist's blocks and folders; no engine commands at all (dash-2050 has none).
COMPANY_AGENT = {"boeing": "boeing-strategist", "airbus": "airbus-strategist", "cfm": "cfm-strategist",
                 "pratt_whitney": "pratt-whitney-strategist", "rolls_royce": "rolls-royce-strategist"}
for _side, _names in EXECS.items():
    for _n in _names:
        BLOCK[_n] = BLOCK[COMPANY_AGENT[_side]] + ["wargame.engine"]
        PLAYER_SIDE[_n] = _side
        OWN_ROOTS[_n] = OWN_ROOTS[COMPANY_AGENT[_side]]


def _inside_own(agent, path, cwd):
    """True if `path` (made absolute and normalised) lies inside one of the agent's own folders."""
    roots = [os.path.realpath(r if r.startswith("/") else os.path.join(REPO, r)) for r in OWN_ROOTS.get(agent, [])]
    p = os.path.realpath(path if path.startswith("/") else os.path.join(cwd or REPO, path))
    return any(p == r or p.startswith(r.rstrip("/") + "/") for r in roots)


def scope_violation(agent, tool, ti, cwd):
    """Searches and wildcard or recursive reads must stay inside the player's own folders."""
    import re
    if agent not in OWN_ROOTS:
        return None
    if tool in ("Grep", "Glob"):
        root = ti.get("path") or cwd or REPO
        if not _inside_own(agent, root, cwd):
            return f"{tool} outside your own folders ({root})"
        pat = ti.get("pattern", "") if tool == "Glob" else ""
        if pat.startswith("/") or ".." in pat:
            return f"Glob pattern outside your own folders ({pat})"
    if tool == "Read":
        fp = ti.get("file_path", "")
        if os.path.normpath(fp) != fp and ".." in fp:
            if not _inside_own(agent, fp, cwd):
                return f"normalised path outside your own folders ({fp})"
    if tool == "Bash":
        cmd = ti.get("command", "")
        body = cmd.split("\n")[0] if "<<" in cmd else cmd      # heredoc bodies are data, not paths
        quoted = []

        def _q(m):                                              # quoted text is literal: no globbing, no splitting
            quoted.append((m.group(0)[0], m.group(0)[1:-1]))
            return " QSTR%d " % (len(quoted) - 1)
        bare = re.sub(r"'[^']*'|\"(?:[^\"\\\\]|\\\\.)*\"", _q, body)
        dq = " ".join(t for k, t in quoted if k == '"')
        if "$(" in bare or "`" in bare or "$(" in dq or "`" in dq:
            return "command substitution"
        if re.search(r"\b(glob|os\.walk|listdir|scandir|subprocess|os\.system|popen)\b", cmd):
            return "file discovery or shell calls from a script"
        wd = cwd or REPO
        for seg in re.split(r"\s*(?:&&|\|\||;|\|)\s*", bare):
            seg = seg.strip()
            m = re.match(r"cd\s+(\S+)$", seg)
            if m:
                d = m.group(1)
                if d.startswith("QSTR"):
                    d = quoted[int(d[4:])][1]
                wd = os.path.realpath(d if d.startswith("/") else os.path.join(wd, d))
                continue
            toks = [t for t in re.split(r"[\s<>]+", seg) if t]
            recursive = bool(re.search(r"(^|\s)(-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)(\s|$)", seg) and
                             re.match(r"(grep|egrep|fgrep|rg|ls|cp|du)\b", seg)) or \
                bool(re.match(r"(find|tree|rg)\b", seg))
            npaths = 0
            for t in toks:
                lit = t.startswith("QSTR")
                if lit:
                    t = quoted[int(t[4:])][1]
                if t.startswith("-") or not re.fullmatch(r"[\w./~*?\[\]{}+-]+", t):
                    continue
                globbing = (not lit) and bool(re.search(r"[*?\[{]", t))
                if not ("/" in t or globbing or t in (".", "..")):
                    continue
                npaths += 1
                static = (re.split(r"[*?\[{]", t)[0] or ".") if globbing else t
                if (globbing or recursive or ".." in t) and not _inside_own(agent, static, wd):
                    return f"wildcard, recursive or relative access outside your own folders ({t})"
            if recursive and not npaths and not _inside_own(agent, ".", wd):
                return "recursive search outside your own folders"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if os.environ.get("WARGAME_HOOK_DEBUG"):
        with open(os.environ["WARGAME_HOOK_DEBUG"], "a") as f:
            f.write(json.dumps({k: data.get(k) for k in ("agent_type", "agent_id", "tool_name")}) + "\n")
    agent = data.get("agent_type") or ""
    rules = BLOCK.get(agent)
    if not rules:
        return
    blob = json.dumps(data.get("tool_input", {}))
    hit = next((r for r in rules + (GM_PRIVATE if agent in OWN_ROOTS else []) if r in blob), None)
    if not hit:
        hit = scope_violation(agent, data.get("tool_name", ""), data.get("tool_input", {}) or {}, data.get("cwd"))
    if not hit and "wargame.engine" in blob:
        hit = engine_violation(agent, str((data.get("tool_input") or {}).get("command", "")))
    if hit:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"War-game isolation: {agent} may not access '{hit}'. "
                                        "Use only your own profile and the engine's --side view.",
        }}))


if __name__ == "__main__":
    main()
