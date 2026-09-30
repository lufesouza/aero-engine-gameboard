#!/usr/bin/env python3
"""Merge verified Rolls-Royce evidence into one citable file with R-#### ids.

Usage: rr_merge_evidence.py <evidence dir> <out evidence.jsonl>

Reads <dir>/*.verified.jsonl (spreadsheet items checked by verify_cells.py, text
items by verify_quotes.py), drops duplicates (same cited cells, or same quote on
the same page), orders items by perspective, category and date, and numbers them
R-0001.... Prints counts by reader, perspective and category.
"""
import collections
import glob
import json
import os
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
items = []
for f in sorted(glob.glob(os.path.join(src, "*.verified.jsonl"))):
    reader = os.path.basename(f).split(".")[0]
    for line in open(f):
        if line.strip():
            it = json.loads(line)
            it["reader"] = it.get("reader") or reader
            items.append(it)


def key(it):
    if it.get("cells"):
        return ("cells",) + tuple(sorted(f"{c['source']}|{c['sheet']}|{str(c['ref']).upper()}" for c in it["cells"]))
    return ("quote", it.get("source"), int(it.get("page", 0)), re.sub(r"\W+", "", it.get("quote", "").lower())[:80])


seen, uniq = set(), []
for it in items:
    k = key(it)
    if k in seen:
        continue
    seen.add(k)
    uniq.append(it)

PERSP = ["own_behaviour", "analyst_view", "market_view", "observed_by_boeing", "observed_by_airbus"]
uniq.sort(key=lambda it: (PERSP.index(it.get("perspective")) if it.get("perspective") in PERSP else 9,
                          it.get("category", ""), it.get("date") or ""))
os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
with open(dst, "w") as out:
    for i, it in enumerate(uniq, 1):
        it = {"id": f"R-{i:04d}", **{k: v for k, v in it.items() if k not in ("id", "cell_errors")}}
        it["company"] = "rolls_royce"
        out.write(json.dumps(it, ensure_ascii=False) + "\n")
print(f"{len(items)} verified items, {len(uniq)} after de-duplication -> {dst}")
for field in ("reader", "perspective", "category"):
    print(field, dict(collections.Counter(it.get(field) for it in uniq).most_common()))
