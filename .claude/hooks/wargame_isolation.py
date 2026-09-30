#!/usr/bin/env python3
"""PreToolUse hook: keep the war-game agents independent.

Each strategist may not touch the other side's profile, role card or private
scratch folder, nor the build-time work areas that hold both sides' material.
No player or market agent may read run state (sealed orders live there) or run
engine commands other than read-only ones from its own side's view. The Game
Orchestrator (referee), the analyst and the main session are not restricted.
"""
import json
import os
import sys

# Build-time work areas (profile drafts, raw evidence, audits) hold both sides' material.
BUILD = ["profiles/build/work", "/scratchpad/profiles", "/scratchpad/evidence", "/scratchpad/integ",
         "/scratchpad/audit", "/scratchpad/ab_synth_work", "/scratchpad/text"]
# Raw uploads contain every year; the period-locked 2010 players may not read them.
RAW = ["Transcripts from", "Boeing 10ks", "airbus_se_report", "GoldmanSachs", "Morgan Stanley", "NYSE BA Financials",
       "wargame/scenarios", "referee_only", "wargame/README.md", "profiles/build"]
BLOCK = {
    "boeing-2010": ["profiles/airbus", "profiles/boeing/", "airbus-", "boeing-strategist.md", "wargame/runs",
                    "wargame-airbus"] + BUILD + RAW,
    "airbus-2010": ["profiles/boeing", "profiles/airbus/", "boeing-", "airbus-strategist.md", "wargame/runs",
                    "wargame-boeing"] + BUILD + RAW,
    "boeing-strategist": ["profiles/airbus", "airbus-strategist.md", "wargame/runs", "wargame-airbus"] + BUILD,
    "airbus-strategist": ["profiles/boeing", "boeing-strategist.md", "wargame/runs", "wargame-boeing"] + BUILD,
    "wargame-market": ["profiles/", "wargame/runs", "wargame-boeing", "wargame-airbus"] + BUILD,
}


PLAYER_SIDE = {"boeing-strategist": "boeing", "airbus-strategist": "airbus", "wargame-market": "market",
               "boeing-2010": "boeing", "airbus-2010": "airbus"}
READ_ONLY = {"brief", "rules", "options", "whatif", "validate", "equilibria", "scenarios", "status"}


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
        if sub in ("options", "whatif", "equilibria", "brief") and not sides:
            return f"engine '{sub}' without --side {own}"
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
    hit = next((r for r in rules if r in blob), None)
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
