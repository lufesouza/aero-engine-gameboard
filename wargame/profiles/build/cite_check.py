#!/usr/bin/env python3
"""Check a profile's citations against its evidence file.

Usage: cite_check.py <profile.md | reaction_function.json | financials.md> <evidence.jsonl> [--show]

Lists cited ids that do not exist, counts distinct ids cited, and with --show
prints, for every paragraph or table row that cites ids, the finding (and the
first cell or quote) of each cited item, so an auditor can judge support.
"""
import json
import re
import sys

path, ev = sys.argv[1], sys.argv[2]
show = "--show" in sys.argv
items = {}
for line in open(ev):
    if line.strip():
        it = json.loads(line)
        items[it["id"]] = it
text = open(path).read()
pat = re.compile(r"\b([RPAB])-(\d{4})\b")
cited = [m.group(0) for m in pat.finditer(text)]
missing = sorted({c for c in cited if c not in items})
print(f"{path}: {len(cited)} citations, {len(set(cited))} distinct ids, {len(missing)} missing")
if missing:
    print("MISSING:", ", ".join(missing))
if show:
    units = re.split(r"\n\s*\n|\n(?=\|)|\n(?=- )|\n(?=\d+\. )", text)
    for u in units:
        ids = sorted({m.group(0) for m in pat.finditer(u)})
        if not ids:
            continue
        print("\n=== CLAIM:", re.sub(r"\s+", " ", u.strip())[:700])
        for i in ids:
            it = items.get(i)
            if not it:
                print(f"  {i}: MISSING")
                continue
            src = (f"cells {it['cells'][0]['sheet']}!{it['cells'][0]['ref']}={it['cells'][0]['value']}" if it.get("cells")
                   else f"\"{it.get('quote', '')[:220]}\"")
            print(f"  {i} [{it.get('perspective')}, {it.get('date')}]: {it.get('finding', '')[:260]} | {src}")
