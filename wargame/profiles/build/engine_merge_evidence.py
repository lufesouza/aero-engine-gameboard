#!/usr/bin/env python3
"""Merge an engine maker's verified evidence into one citable file.

Usage: engine_merge_evidence.py <rolls_royce|pratt_whitney> <evidence dir> <out evidence.jsonl>

Reads <dir>/*.verified.jsonl (spreadsheet items checked by verify_cells.py, text
items by verify_quotes.py), drops duplicates (same cited cells, or same quote on
the same page), orders items by perspective, category and date, and numbers them
R-#### (Rolls-Royce) or P-#### (Pratt & Whitney). Items about other companies
(rivals, customers) stay in: they are that company's view of them. Prints counts
by reader, company, perspective and category.
"""
import collections
import glob
import json
import os
import re
import sys

company, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
PREFIX = {"rolls_royce": "R", "pratt_whitney": "P"}[company]
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

PERSP = ["own_behaviour", "own_words", "filing", "analyst_view", "market_view", "analyst_question", "press", "industry_report",
         "observed_by_boeing", "observed_by_airbus", "observed_by_rolls_royce", "observed_by_pratt_whitney"]
uniq.sort(key=lambda it: (it.get("company") != company, PERSP.index(it.get("perspective")) if it.get("perspective") in PERSP else 99,
                          it.get("category", ""), it.get("date") or ""))
os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
with open(dst, "w") as out:
    for i, it in enumerate(uniq, 1):
        it = {"id": f"{PREFIX}-{i:04d}", **{k: v for k, v in it.items() if k not in ("id", "cell_errors")}}
        it["company"] = it.get("company") or company
        out.write(json.dumps(it, ensure_ascii=False) + "\n")
print(f"{len(items)} verified items, {len(uniq)} after de-duplication -> {dst}")
for field in ("reader", "company", "perspective", "category"):
    print(field, dict(collections.Counter(it.get(field) for it in uniq).most_common()))
