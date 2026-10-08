"""Boeing recovery speed (pp/yr after fps entry) needed at fps 2044: bisection on the board (piecewise, so no linear shortcut)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from delay import AROWS, FPS10, DN, cell
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
def val(pp, ctx):
    MX, A, B, SS = H.af({"af_fps_eis": 2044, "af_ramp10_b_pp": pp}, H.OVERLAP_PATCH)
    return cell(MX, A, B, ctx, FPS10("Milk_787"))["b_total_delta"] - cell(MX, A, B, ctx, DN("Milk_787"))["b_total_delta"]
def solve(target, ctx, lo=1.0, hi=4.0):
    for _ in range(30):
        mid = (lo + hi) / 2
        if val(mid, ctx) < target: lo = mid
        else: hi = mid
    return round(hi, 3)
out = {"breakeven_modal": solve(0.0, AROWS["NGSA + Re-engine A350"]), "hurdle_1B_modal": solve(1.0, AROWS["NGSA + Re-engine A350"]),
       "breakeven_delay_tactics": solve(0.0, AROWS["NGSA + Bottleneck + Re-engine A350"])}
json.dump(out, open(os.path.join(OUTDIR, "recovery_threshold.json"), "w"), indent=1); print(out)
