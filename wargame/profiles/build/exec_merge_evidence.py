#!/usr/bin/env python3
"""Merge verified executive evidence into each company's executives/evidence.jsonl.

Usage: exec_merge_evidence.py <evidence dir> <repo root>

Reads <dir>/*.verified.jsonl, drops duplicate quotes (same source, page and text),
orders items by company, executive, date and dimension, and numbers them BX-####
(Boeing, wargame/profiles/boeing/executives/evidence.jsonl), AX-#### (Airbus,
wargame/profiles/airbus/executives/evidence.jsonl) or CX-#### (CFM International's
parent-side leaders, wargame/profiles/cfm/executives/evidence.jsonl). A company with
no items in the input is left untouched. Prints counts per executive
and dimension.
"""
import collections
import glob
import json
import os
import re
import sys

src, root = sys.argv[1], sys.argv[2]
items = []
for f in sorted(glob.glob(os.path.join(src, "*.verified.jsonl"))):
    reader = os.path.basename(f).split(".")[0]
    for line in open(f):
        if line.strip():
            it = json.loads(line)
            it["reader"] = reader
            items.append(it)
seen, uniq = set(), []
for it in items:
    k = (it.get("source"), int(it.get("page", 0)), re.sub(r"\W+", "", it.get("quote", "").lower())[:100])
    if k not in seen:
        seen.add(k)
        uniq.append(it)
for co, prefix in (("boeing", "BX"), ("airbus", "AX"), ("cfm", "CX"), ("rolls_royce", "RX"), ("pratt_whitney", "PX")):
    rows = sorted([i for i in uniq if i.get("company") == co],
                  key=lambda i: (i.get("exec_id", ""), i.get("date", ""), i.get("dimension", "")))
    if not rows:  # never overwrite a company's evidence from a run that did not cover it
        continue
    dst = os.path.join(root, "wargame", "profiles", co, "executives", "evidence.jsonl")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as out:
        for n, it in enumerate(rows, 1):
            out.write(json.dumps({"id": f"{prefix}-{n:04d}", **{k: v for k, v in it.items() if k != "id"}}, ensure_ascii=False) + "\n")
    print(f"{co}: {len(rows)} items -> {dst}")
    print("  by exec:", dict(collections.Counter(i.get("exec_id") for i in rows).most_common()))
    print("  by dimension:", dict(collections.Counter(i.get("dimension") for i in rows).most_common()))
