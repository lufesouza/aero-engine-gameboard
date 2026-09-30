#!/usr/bin/env python3
"""PreToolUse hook: keep the war-game agents independent.

Each strategist may not touch the other side's profile or role card, and no
player or market agent may read run state (sealed orders live there). Calls
from other agents (including the main session) are allowed.
"""
import json
import os
import sys

BLOCK = {
    "boeing-strategist": ["wargame/profiles/airbus", "airbus-strategist.md", "wargame/runs"],
    "airbus-strategist": ["wargame/profiles/boeing", "boeing-strategist.md", "wargame/runs"],
    "wargame-market": ["wargame/profiles/", "wargame/runs"],
}


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
    if hit:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"War-game isolation: {agent} may not access '{hit}'. "
                                        "Use only your own profile and the engine's --side view.",
        }}))


if __name__ == "__main__":
    main()
