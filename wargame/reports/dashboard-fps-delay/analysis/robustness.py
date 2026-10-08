"""Robustness checks requested by the review: (1) lever levels that put fps back into a PURE equilibrium at 2044;
(2) how the fps case depends on when the fps bill is paid (board: one lump at entry into service);
(3) the fps case when Boeing also re-engines the 787."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from delay import AROWS, FPS10, DN, cell
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
OV = H.OVERLAP_PATCH
def eq(over, patch=OV):
    MX, A, B, SS = H.af(over, patch)
    pure, near = H.eq_lists(MX, A, B)
    return {"pure": len(pure), "near": len(near), "fps_in_pure": sum("fps" in H.lab(b) for a, b, *_ in pure),
            "fps_in_near": sum("fps" in H.lab(b) for a, b, *_ in near),
            "pure_cells": [H.lab(a) + " || " + H.lab(b) for a, b, *_ in pure]}
OUT = {"pure_equilibrium_levers_2044": {}}
for name, key, vals in (("fps margin %", "af_m_fps", [31.3, 33.5, 34.0, 34.1, 35.0]),
                        ("fps 10yr bill $B", "af_cx_fps10", [45.0, 41.0, 40.9, 40.7, 38.0]),
                        ("fps price $M", "af_price_fps", [67.0, 71.7, 73.0, 73.1, 75.0]),
                        ("Boeing recovery pp/yr", "af_ramp10_b_pp", [1.9, 2.25, 2.3, 2.5, 3.0])):
    OUT["pure_equilibrium_levers_2044"][name] = {str(v): eq({"af_fps_eis": 2044, key: v}) for v in vals}

# (2) bill timing. Patch only Boeing's NB capex discounting.
LUMP = "        b_pv_nb_invest = b_nom_invest_nb / ((1 + WACC_B) ** b_eis_nb_t)"
def bill_patch(kind):
    if kind == "lump_at_2041":   # slip found after the bill is committed on the 2041 schedule
        new = "        b_pv_nb_invest = b_nom_invest_nb / ((1 + WACC_B) ** 15)"
    elif kind.startswith("spread"):
        n = int(kind[6:])        # spread evenly over n years ending the year before entry into service
        new = f"        b_pv_nb_invest = sum(b_nom_invest_nb / {n} / ((1 + WACC_B) ** _t) for _t in range(b_eis_nb_t - {n}, b_eis_nb_t))"
    elif kind.startswith("slip_spread"):  # spent on the 2041 schedule (n years before 2041), revenue from 2044
        n = int(kind[11:])
        new = f"        b_pv_nb_invest = sum(b_nom_invest_nb / {n} / ((1 + WACC_B) ** _t) for _t in range(15 - {n}, 15))"
    return OV + [(LUMP, new, 1)]
def fpsval(over, patch, ctx="NGSA + Re-engine A350", wb="Milk_787"):
    MX, A, B, SS = H.af(over, patch)
    a = AROWS[ctx]
    return round(cell(MX, A, B, a, FPS10(wb))["b_total_delta"] - cell(MX, A, B, a, DN(wb))["b_total_delta"], 3)
bt = {}
for kind in ("board_lump", "lump_at_2041", "spread9", "spread6", "slip_spread9"):
    p = OV if kind == "board_lump" else bill_patch(kind)
    row = {}
    for y in (2041, 2044):
        if kind in ("lump_at_2041", "slip_spread9") and y == 2041:
            continue
        row[str(y)] = fpsval({"af_fps_eis": y}, p)
        row[f"{y}_vs_delay_tactics"] = fpsval({"af_fps_eis": y}, p, ctx="NGSA + Bottleneck + Re-engine A350")
    bt[kind] = row
# overrun on top of a committed bill: 30% extra paid at the new entry year
bt["lump_at_2041_plus_30pct_at_2044"] = {"2044": fpsval({"af_fps_eis": 2044, "af_cx_fps10": round(55.25 * 1.3, 4)},
    OV + [(LUMP, "        b_pv_nb_invest = (55.25 / ((1 + WACC_B) ** 15)) + ((b_nom_invest_nb - 55.25) / ((1 + WACC_B) ** b_eis_nb_t))", 1)])}
OUT["bill_timing"] = bt
# (3) Boeing re-engines the 787 as well
OUT["with_787_reengine"] = {str(y): {"vs_A350_reengine": fpsval({"af_fps_eis": y}, OV, wb="Re_engine_787"),
                                     "vs_A350_do_nothing": fpsval({"af_fps_eis": y}, OV, ctx="NGSA + Do Nothing A350", wb="Re_engine_787")} for y in (2041, 2044)}
json.dump(OUT, open(os.path.join(OUTDIR, "robustness.json"), "w"), indent=1)
for name, d in OUT["pure_equilibrium_levers_2044"].items():
    print(name, {v: (r["pure"], r["fps_in_pure"], r["near"]) for v, r in d.items()})
print("bill timing:", json.dumps(bt, indent=0))
print("with 787 Re-engine:", OUT["with_787_reengine"])
