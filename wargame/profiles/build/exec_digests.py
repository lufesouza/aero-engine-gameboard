#!/usr/bin/env python3
"""Write one reading digest per executive from a company's executives/evidence.jsonl.

Usage: exec_digests.py <company: boeing|airbus|cfm> <out dir>

Each digest lists the executive's items by dimension, then date: id, date,
speaker, event and page, the finding, the quote and any numbers. Profile
writers read these instead of the raw JSON Lines file.
"""
import collections
import json
import os
import sys

co, out = sys.argv[1], sys.argv[2]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", co, "executives", "evidence.jsonl")
by = collections.defaultdict(list)
for line in open(root):
    if line.strip():
        it = json.loads(line)
        by[it.get("exec_id", "unknown")].append(it)
os.makedirs(out, exist_ok=True)
for eid, items in sorted(by.items()):
    items.sort(key=lambda i: (i.get("dimension", ""), i.get("date", "")))
    lines = [f"# {eid}: {len(items)} items", ""]
    dim = None
    for it in items:
        if it.get("dimension") != dim:
            dim = it.get("dimension")
            lines += ["", f"## {dim}"]
        lines.append(f"[{it['id']}] {it.get('date')} | {it.get('speaker', '')[:60]} | {it.get('doc', '')} p{it.get('page')} | {it.get('perspective', '')}")
        lines.append(f"  FINDING: {it.get('finding', '')}")
        lines.append(f"  QUOTE: \"{it.get('quote', '')}\"")
        extra = {k: it[k] for k in ("trigger", "response", "lag") if it.get(k)}
        if extra:
            lines.append("  " + " | ".join(f"{k.upper()}: {v}" for k, v in extra.items()))
        if it.get("numbers"):
            lines.append(f"  NUMBERS: {json.dumps(it['numbers'], ensure_ascii=False)}")
    open(os.path.join(out, f"{eid}.txt"), "w").write("\n".join(lines) + "\n")
    print(f"{eid}: {len(items)} items")
