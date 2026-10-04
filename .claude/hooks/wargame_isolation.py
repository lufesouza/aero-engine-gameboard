#!/usr/bin/env python3
"""PreToolUse hook: keep the war-game agents independent.

Each strategist (Boeing, Airbus, and the optional Rolls-Royce and Pratt & Whitney suppliers) may not
touch another player's profile, role card or private scratch folder, nor the
build-time work areas that hold every side's material.
No player or market agent may read run state (sealed orders live there) or run
engine commands other than read-only ones from its own side's view. The Game
Orchestrator (referee), the analyst and the main session are not restricted.
"""
import json
import os
import sys

# Build-time work areas (profile drafts, raw evidence, audits) hold both sides' material.
BUILD = ["profiles/build/work", "/scratchpad/profiles", "/scratchpad/evidence", "/scratchpad/integ",
         "/scratchpad/audit", "/scratchpad/ab_synth_work", "/scratchpad/text", "/scratchpad/rr", "/scratchpad/pw",
         "/scratchpad/engines", "/scratchpad/execs", "/scratchpad/cfm"]
RR = ["profiles/rolls_royce", "rolls-royce-strategist.md", "wargame-rolls_royce"]
PW = ["profiles/pratt_whitney", "pratt-whitney-strategist.md", "wargame-pratt_whitney"]
# CFM International's leaders (GE side): not a player yet; no player reads them. The cross-player
# overview page summarises every side, so no player reads it either.
CFM = ["profiles/cfm", "profiles/overview", "wargame/config"]  # the config holds every player's assigned objective
AIRFRAMERS = ["profiles/boeing", "profiles/airbus", "boeing-strategist.md", "airbus-strategist.md", "boeing-2010.md",
              "airbus-2010.md", "wargame-boeing", "wargame-airbus"]
# Raw uploads contain every year; the period-locked 2010 players may not read them.
RAW = ["Transcripts from", "Boeing 10ks", "airbus_se_report", "GoldmanSachs", "Morgan Stanley", "NYSE BA Financials",
       "Rolls-Royce Holdings plc", "Transcript Digest", "Filings.pdf", "SEC Fillings", "Durability news", "Global Strategy Brief",
       "Company Profile.pdf", "SAF.PA", "Embraer",
       "wargame/scenarios", "referee_only", "wargame/README.md", "profiles/build"]
BLOCK = {
    "boeing-2010": ["profiles/airbus", "profiles/boeing/", "airbus-2010.md", "airbus-strategist.md", "boeing-strategist.md",
                    "wargame/runs",
                    "wargame-airbus"] + RR + PW + CFM + BUILD + RAW,
    "airbus-2010": ["profiles/boeing", "profiles/airbus/", "boeing-2010.md", "boeing-strategist.md", "airbus-strategist.md",
                    "wargame/runs",
                    "wargame-boeing"] + RR + PW + CFM + BUILD + RAW,
    "boeing-strategist": ["profiles/airbus", "airbus-strategist.md", "wargame/runs", "wargame-airbus"] + RR + PW + CFM + BUILD,
    "airbus-strategist": ["profiles/boeing", "boeing-strategist.md", "wargame/runs", "wargame-boeing"] + RR + PW + CFM + BUILD,
    "rolls-royce-strategist": AIRFRAMERS + PW + CFM + ["wargame/runs"] + BUILD,
    "pratt-whitney-strategist": AIRFRAMERS + RR + CFM + ["wargame/runs"] + BUILD,
    "wargame-market": ["profiles/", "wargame/runs", "wargame/config", "wargame-boeing", "wargame-airbus", "wargame-rolls_royce",
                       "wargame-pratt_whitney"] + BUILD,
}


PLAYER_SIDE = {"boeing-strategist": "boeing", "airbus-strategist": "airbus", "wargame-market": "market",
               "boeing-2010": "boeing", "airbus-2010": "airbus", "rolls-royce-strategist": "rolls_royce",
               "pratt-whitney-strategist": "pratt_whitney"}
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
        if sub in ("options", "whatif", "equilibria", "brief", "rules") and not sides:
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
