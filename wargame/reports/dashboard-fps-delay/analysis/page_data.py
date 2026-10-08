"""Series for the HTML report's charts: fps's equilibrium status by NGSA lead, and yearly share / Airbus delivery paths."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from delay import AROWS, FPS10, DN, cell
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
OUT = {"ngsa_lead": {}, "paths": {}}
for fe in (2041, 2044):
    rows = []
    for ne in range(fe - 9, fe + 1):
        MX, A, B, SS = H.af({"af_fps_eis": fe, "af_ngsa_eis": ne}, H.OVERLAP_PATCH)
        pure, near = H.eq_lists(MX, A, B)
        a = AROWS["NGSA + Re-engine A350"]; s = AROWS["NGSA + Bottleneck + Re-engine A350"]
        rows.append({"ngsa_eis": ne, "lead": fe - ne,
                     "fps_minus_dn": round(cell(MX, A, B, a, FPS10("Milk_787"))["b_total_delta"] - cell(MX, A, B, a, DN("Milk_787"))["b_total_delta"], 3),
                     "fps_minus_dn_vs_delay_tactics": round(cell(MX, A, B, s, FPS10("Milk_787"))["b_total_delta"] - cell(MX, A, B, s, DN("Milk_787"))["b_total_delta"], 3),
                     "pure": len(pure), "near": len(near),
                     "fps_in_pure": sum("fps" in H.lab(b) for _, b, *_ in pure),
                     "fps_in_near": sum("fps" in H.lab(b) for _, b, *_ in near)})
    OUT["ngsa_lead"][str(fe)] = rows
SS = H.af({"af_fps_eis": 2041}, H.OVERLAP_PATCH)[3]; mod = SS["_MOD"]
for name, fe, launch in (("fps 2041", 2041, True), ("fps 2044", 2044, True), ("Boeing Do Nothing", 2044, False)):
    bt, at = fe - 2026, 2037 - 2026
    end = (fe + 19) if launch else 2063
    path = []
    for y in range(2026, end + 1):
        b, a = mod._compute_nb_share_unified(y - 2026, launch, True, bt, at, is_7yr=False)
        path.append([y, round(b, 4), round(a, 4), round(2000 * a)])
    OUT["paths"][name] = path
json.dump(OUT, open(os.path.join(OUTDIR, "page_data.json"), "w"), indent=1)
for fe, rows in OUT["ngsa_lead"].items():
    print("fps", fe); [print("  lead", r["lead"], "NGSA", r["ngsa_eis"], r["fps_minus_dn"], r["fps_minus_dn_vs_delay_tactics"], "pure", r["pure"], "fps_pure", r["fps_in_pure"], "near", r["near"], "fps_near", r["fps_in_near"]) for r in rows]
for k, p in OUT["paths"].items(): print(k, p[0], p[11], p[17], p[-1])
