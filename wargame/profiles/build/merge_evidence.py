#!/usr/bin/env python3
"""Merge verified evidence into one citable file per profile.

boeing: everything describing Boeing, plus Boeing-side observations of Airbus (its intel).
airbus: everything describing Airbus (its own report + how others observed it), plus a
        public-intel digest on Boeing (2023+ items from Boeing's own public statements).
"""
import collections, glob, json, os, re, sys
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
side = sys.argv[1]
items = []
for f in sorted(glob.glob(f"{S}/evidence/*.verified.jsonl")):
    reader = os.path.basename(f).split(".")[0]
    for line in open(f):
        it = json.loads(line); it["reader"] = reader; items.append(it)
def key(it): return (it.get("source"), int(it.get("page", 0)), re.sub(r"\W+", "", it.get("quote", "").lower())[:80])
seen, uniq = set(), []
for it in items:
    k = key(it)
    if k in seen: continue
    seen.add(k); uniq.append(it)
def date(it): return it.get("date") or ""
if side == "boeing":
    own = [i for i in uniq if i.get("company") == "boeing"]
    intel = [i for i in uniq if i.get("company") == "airbus" and i.get("source") != "airbus_fy2025"]
    prefix = "B"
else:
    own = [i for i in uniq if i.get("company") == "airbus"]
    intel = [i for i in uniq if i.get("company") == "boeing" and date(i) >= "2023-01-01"]
    prefix = "A"
for i in own: i["perspective"] = "own_behaviour" if not (side == "airbus" and i.get("source") != "airbus_fy2025") else "own_behaviour_observed_by_boeing_or_analysts"
for i in intel: i["perspective"] = "intel_on_rival"
out = sorted(own, key=date) + sorted(intel, key=date)
os.makedirs(f"{S}/profiles/{side}", exist_ok=True)
with open(f"{S}/profiles/{side}/evidence.jsonl", "w") as fh:
    for n, it in enumerate(out, 1):
        it = {"id": f"{prefix}-{n:04d}", **{k: v for k, v in it.items() if k not in ("why",)}}
        fh.write(json.dumps(it, ensure_ascii=False) + "\n")
c = collections.Counter((i["perspective"], i.get("category")) for i in out)
print(side, len(items), "raw ->", len(uniq), "unique ->", len(out), "in profile")
for k, v in sorted(c.items()): print("  ", k, v)
print("  by source:", collections.Counter(i.get("source") for i in out))
