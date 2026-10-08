"""Sensitivities quoted in the report that need small board patches:
(1) COMAC taking a slice x of the 2,000-a-year market before Boeing and Airbus split the rest;
(2) the largest flat Boeing strain that still reproduces the snapshot (the uploaded build's flat rule);
(3) the delay's cost to Boeing on a common calendar horizon instead of the board's entry-into-service + 19 window."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from delay import AROWS, FPS10, DN, cell
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "results")
OV = H.OVERLAP_PATCH
MODC = AROWS["NGSA + Re-engine A350"]

def fps_minus_dn(over, patch):
    MX, A, B, SS = H.af(over, patch)
    return cell(MX, A, B, MODC, FPS10("Milk_787"))["b_total_delta"] - cell(MX, A, B, MODC, DN("Milk_787"))["b_total_delta"]

OUT = {}
# (1) market slice
def slice_patch(x):
    return OV + [("    NB_PER_YR    = 2000", f"    NB_PER_YR    = 2000 * (1 - {x})", 1)]
OUT["comac_slice"] = {str(x): {fe: round(fps_minus_dn({"af_fps_eis": fe}, slice_patch(x)), 6) for fe in (2041, 2044)} for x in (0, 0.05, 0.10, 0.15, 0.20)}
lo, hi = 0.0, 0.2
for _ in range(30):
    mid = (lo + hi) / 2
    if fps_minus_dn({"af_fps_eis": 2041}, slice_patch(mid)) > 0: lo = mid
    else: hi = mid
OUT["comac_slice_breakeven_2041"] = round((lo + hi) / 2, 5)

# (2) flat strain bound that reproduces the snapshot exactly
snap = H.parse_snapshot(os.path.join(HERE, "..", "inputs", "Game.txt"))
ok = []
for k in range(0, 61):
    s = round(k * 0.05, 2)
    MX, A, B, SS = H.af({"af_strain_b": s})
    r = H.check_snapshot(MX, A, B, snap)
    if r["pure"] == 0 and r["near"] == 17 and r["missing"] == 0 and r["extra"] == 0 and not r["bad_round"]:
        ok.append(s)
OUT["flat_strain_reproducing_values"] = ok
OUT["flat_strain_max_reproducing"] = max(ok) if ok else None

# (3) common calendar horizon for Boeing's narrowbody window (scenario and baseline alike)
def horizon_patch(end_year):
    t = end_year - 2026
    return OV + [("        _b_nb_end_t = max(0, v_fps_eis_year  - 2026) + NPV_POST_EIS_YRS - 1", f"        _b_nb_end_t = {t}", 1),
                 ("        _b_nb_end_t = b_eis_nb_t + NPV_POST_EIS_YRS - 1", f"        _b_nb_end_t = {t}", 1)]
hz = {}
for end in (2056, 2060, 2063, 2066, 2070, 2080):
    v41 = fps_minus_dn({"af_fps_eis": 2041}, horizon_patch(end)); v44 = fps_minus_dn({"af_fps_eis": 2044}, horizon_patch(end))
    hz[str(end)] = {"fps2041": round(v41, 6), "fps2044": round(v44, 6), "delay_cost": round(v44 - v41, 6)}
OUT["common_horizon"] = hz
lo, hi = 2063, 2120
while hi - lo > 1:
    mid = (lo + hi) // 2
    if fps_minus_dn({"af_fps_eis": 2044}, horizon_patch(mid)) < 0: lo = mid
    else: hi = mid
OUT["fps2044_breakeven_horizon"] = hi
json.dump(OUT, open(os.path.join(OUTDIR, "sensitivities.json"), "w"), indent=1)
print(json.dumps(OUT, indent=1))
