"""Re-solve the snapshot board headlessly and compare it with Game.txt (flat strain as built vs overlap-aware strain)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "results"); os.makedirs(OUTDIR, exist_ok=True)
snap = H.parse_snapshot(os.path.join(HERE, "..", "inputs", "Game.txt"))
out = {}
for name, patch in (("flat strain (uploaded build)", None), ("overlap-aware strain", H.OVERLAP_PATCH)):
    MX, A, B, SS = H.af(patch=patch)
    r = H.check_snapshot(MX, A, B, snap)
    out[name] = r
    print(name, {k: v for k, v in r.items() if k != "bad_round"}, "rounding mismatches:", len(r["bad_round"]))
E = H.en()
out["engine"] = {"pure": len(E["_EPURE"]), "near": len(E["_ENEAR"]), "pw_locked": E["_EPW"]}
print("engine board:", out["engine"])
json.dump(out, open(os.path.join(OUTDIR, "check_snapshot.json"), "w"), indent=1)
