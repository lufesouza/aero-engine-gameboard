"""fps 3-year delay on the snapshot board (overlap-aware strain), plus sweeps. Writes delay.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTDIR, exist_ok=True)

AROWS = {
    "NGSA + Re-engine A350": ("Launch_NGSA", "No_Bottleneck", "No_Poaching", "Re_engine_A350"),
    "NGSA + Do Nothing A350": ("Launch_NGSA", "No_Bottleneck", "No_Poaching", "Milk_A350"),
    "NGSA + Bottleneck + Re-engine A350": ("Launch_NGSA", "Sabotage_Bottleneck", "No_Poaching", "Re_engine_A350"),
    "NGSA + Bottleneck + Do Nothing A350": ("Launch_NGSA", "Sabotage_Bottleneck", "No_Poaching", "Milk_A350"),
}
FPS10 = lambda wb: ("Launch_fps_10yr_Solo", "No_Rate_Increase", wb)
FPS7 = lambda wb: ("Launch_fps_7yr_Solo", "No_Rate_Increase", wb)
EMB = lambda wb: ("Launch_fps_via_Embraer", "No_Rate_Increase", wb)
DN = lambda wb: ("Milk_737MAX", "No_Rate_Increase", wb)

def solve(over=None, strain="overlap"):
    patch = H.OVERLAP_PATCH if strain == "overlap" else None
    MX, A, B, SS = H.af(over, patch)
    return MX, A, B, SS

def cell(MX, A, B, a, b):
    return MX[A.index(a)][B.index(b)]

def summary(over=None, strain="overlap"):
    MX, A, B, SS = solve(over, strain)
    pure, near = H.eq_lists(MX, A, B)
    out = {"pure": [], "near": []}
    for k, lst in (("pure", pure), ("near", near)):
        for a, b, ya, yb, da, db in lst:
            out[k].append({"airbus": H.lab(a), "boeing": H.lab(b), "ya": round(ya, 2), "yb": round(yb, 2), "da": round(da, 6), "db": round(db, 6)})
    # Boeing value of fps (vs Do Nothing 737, same WB move) in each Airbus context, both WB moves
    ctx = {}
    for name, a in AROWS.items():
        row = {}
        for wb in ("Re_engine_787", "Milk_787"):
            dn = cell(MX, A, B, a, DN(wb))["b_total_delta"]
            row[wb] = {"do_nothing": round(dn, 6)}
            for vn, f in (("fps10", FPS10), ("fps7", FPS7), ("via_embraer", EMB)):
                c = cell(MX, A, B, a, f(wb))
                row[wb][vn] = round(c["b_total_delta"], 6)
                row[wb][vn + "_vs_dn"] = round(c["b_total_delta"] - dn, 6)
        # Boeing best response in the row
        i = A.index(a)
        j = max(range(len(B)), key=lambda j: MX[i][j]["yield_b"])
        row["best_response"] = H.lab(B[j]); row["best_db"] = round(MX[i][j]["b_total_delta"], 6)
        ctx[name] = row
    out["boeing_by_airbus_ctx"] = ctx
    # Airbus best response to each main Boeing move
    br = {}
    for bn, b in (("fps10 + Do Nothing 787", FPS10("Milk_787")), ("fps10 + Re-engine 787", FPS10("Re_engine_787")),
                  ("fps7 + Do Nothing 787", FPS7("Milk_787")), ("Do Nothing 737 + Do Nothing 787", DN("Milk_787")),
                  ("Do Nothing 737 + Re-engine 787", DN("Re_engine_787")), ("via Embraer + Do Nothing 787", EMB("Milk_787"))):
        j = B.index(b)
        i = max(range(len(A)), key=lambda i: MX[i][j]["yield_a"])
        ranked = sorted(range(len(A)), key=lambda i: -MX[i][j]["yield_a"])[:3]
        br[bn] = {"best": H.lab(A[i]), "da": round(MX[i][j]["a_total_delta"], 6),
                  "top3": [(H.lab(A[k]), round(MX[k][j]["a_total_delta"], 6)) for k in ranked]}
    out["airbus_best_response"] = br
    # Decomposition of fps10 vs Do Nothing in the snapshot's modal context (NGSA + Re-engine A350, Do Nothing 787)
    dec = {}
    for name in ("NGSA + Re-engine A350", "NGSA + Bottleneck + Re-engine A350"):
        a = AROWS[name]
        f = cell(MX, A, B, a, FPS10("Milk_787")); d = cell(MX, A, B, a, DN("Milk_787"))
        dec[name] = {k: round(f[k] - d[k], 6) for k in ("b_delta_nb", "b_delta_wb", "b_delta_tc", "b_strain", "b_total_delta")}
        dec[name]["fps_pv_capex"] = round(f["b_tc_data"]["pv_capex"], 6); dec[name]["fps_alpha_pen"] = round(f["b_tc_data"]["delta_pen"], 6)
        dec[name]["fps_nb_pv"] = round(f["b_scen_nb_pv"], 6); dec[name]["dn_nb_pv"] = round(d["b_scen_nb_pv"], 6)
        dec[name]["base_nb_pv"] = round(SS["_BASE"]["b_base_nb"], 6)
    out["decomp_fps10_vs_dn"] = dec
    return out

if __name__ == "__main__":
    R = {}
    R["snapshot_2041"] = summary()
    R["delay3_2044"] = summary({"af_fps_eis": 2044})
    R["delay3_2044_capex_overrun"] = summary({"af_fps_eis": 2044, "af_cx_fps10": round(55.25 * 1.3, 2), "af_cx_fps7": round(64.47 * 1.3, 2), "af_cx_fpsemb": 130.0})
    R["delay3_2044_flat_strain"] = summary({"af_fps_eis": 2044}, strain="flat")
    R["snapshot_2041_flat_strain"] = summary(strain="flat")
    # Sweep fps EIS 2037..2047: fps10 value vs Do Nothing in the modal and slip contexts, and equilibrium counts
    sweep = []
    for y in range(2037, 2048):
        MX, A, B, SS = solve({"af_fps_eis": y})
        pure, near = H.eq_lists(MX, A, B)
        row = {"fps_eis": y, "pure": len(pure), "near": len(near),
               "fps_in_any_eq": any("fps" in H.lab(b) for a, b, *_ in pure + near),
               "boeing_eq_moves": sorted({H.lab(b) for a, b, *_ in pure + near})}
        for name in ("NGSA + Re-engine A350", "NGSA + Bottleneck + Re-engine A350", "NGSA + Do Nothing A350"):
            a = AROWS[name]
            for wb in ("Milk_787", "Re_engine_787"):
                row[f"{name} | {wb} | fps10-DN"] = round(cell(MX, A, B, a, FPS10(wb))["b_total_delta"] - cell(MX, A, B, a, DN(wb))["b_total_delta"], 6)
                row[f"{name} | {wb} | fps7-DN"] = round(cell(MX, A, B, a, FPS7(wb))["b_total_delta"] - cell(MX, A, B, a, DN(wb))["b_total_delta"], 6)
        # Airbus: value of Delay Tactics (Bottleneck) vs none when Boeing plays fps10 + Do Nothing 787
        for awb in ("Re_engine_A350",):
            j = B.index(FPS10("Milk_787"))
            row["airbus_delay_tactics_value_vs_fps10"] = round(MX[A.index(AROWS["NGSA + Bottleneck + Re-engine A350"])][j]["a_total_delta"] - MX[A.index(AROWS["NGSA + Re-engine A350"])][j]["a_total_delta"], 6)
            row["airbus_ngsa_value_vs_fps10"] = round(MX[A.index(AROWS["NGSA + Re-engine A350"])][j]["a_total_delta"] - MX[A.index(("Milk_A320neo", "No_Bottleneck", "No_Poaching", "Re_engine_A350"))][j]["a_total_delta"], 6)
            jd = B.index(DN("Milk_787"))
            row["airbus_ngsa_value_vs_dn"] = round(MX[A.index(AROWS["NGSA + Re-engine A350"])][jd]["a_total_delta"] - MX[A.index(("Milk_A320neo", "No_Bottleneck", "No_Poaching", "Re_engine_A350"))][jd]["a_total_delta"], 6)
        sweep.append(row)
    R["sweep_fps_eis"] = sweep
    json.dump(R, open(os.path.join(OUTDIR, "delay.json"), "w"), indent=1)
    for k in ("snapshot_2041", "delay3_2044", "delay3_2044_capex_overrun", "delay3_2044_flat_strain", "snapshot_2041_flat_strain"):
        r = R[k]; print(f"== {k}: pure {len(r['pure'])} near {len(r['near'])}")
        for e in r["pure"]: print("   PURE", e["ya"], e["yb"], e["airbus"], "||", e["boeing"], "| $B", e["da"], e["db"])
        for e in r["near"]: print("   near", e["ya"], e["yb"], e["airbus"], "||", e["boeing"])
        for c, v in r["boeing_by_airbus_ctx"].items():
            print(f"   [{c}] DN787: fps10-DN {v['Milk_787']['fps10_vs_dn']:+.2f} fps7-DN {v['Milk_787']['fps7_vs_dn']:+.2f} emb-DN {v['Milk_787']['via_embraer_vs_dn']:+.2f} | Re787: fps10-DN {v['Re_engine_787']['fps10_vs_dn']:+.2f} | BR {v['best_response']} ({v['best_db']:+.2f})")
        for bn, v in r["airbus_best_response"].items(): print(f"   Airbus BR to [{bn}]: {v['best']} ({v['da']:+.2f})")
    print("== sweep")
    for r in sweep:
        print(r["fps_eis"], "pure", r["pure"], "near", r["near"], "fps in eq", r["fps_in_any_eq"],
              "| fps10-DN modal", r["NGSA + Re-engine A350 | Milk_787 | fps10-DN"], "slip", r["NGSA + Bottleneck + Re-engine A350 | Milk_787 | fps10-DN"],
              "| A DelayTactics", r["airbus_delay_tactics_value_vs_fps10"], "A NGSA vs fps10", r["airbus_ngsa_value_vs_fps10"])
