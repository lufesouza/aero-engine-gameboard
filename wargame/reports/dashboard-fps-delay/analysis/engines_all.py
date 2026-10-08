"""Engine game with ALL CFM move combinations (the board keeps only the first 4 per base move, which drops Partner Embraer)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTDIR, exist_ok=True)
PATCH = [("            if m.startswith(base) and n < 4:", "            if m.startswith(base) and n < 99:", 1)]
CASES = {"snapshot": {}, "fps 2044 launched, Boeing ~30%": {"_boeing_share_both": 30},
         "Boeing Do Nothing (737 on LEAP at 20%)": {"_b_supplier": "CFM (Ducted)", "_boeing_share_both": 20}}
OUT = {}
for name, ov in CASES.items():
    for label, patch in (("board as built (16 CFM moves)", None), ("all CFM moves", PATCH)):
        SS = H.en(ov, patch)
        MX, EA, EC = SS["_EMX"], SS["_EA"], SS["_EC"]
        pure = [{"cfm": EA[a], "rr": EC[c], "cfm_b": round(MX[a][c]["A"]["delta_b"], 2), "pw_b": round(MX[a][c]["B"]["delta_b"], 2), "rr_b": round(MX[a][c]["C"]["delta_b"], 2)} for a, c in SS["_EPURE"]]
        near_emb = sum(1 for a, c in SS["_ENEAR"] if "Embraer" in EA[a])
        OUT[f"{name} | {label}"] = {"n_cfm_moves": len(EA), "pure": pure, "near": len(SS["_ENEAR"]), "near_with_partner_embraer": near_emb}
json.dump(OUT, open(os.path.join(OUTDIR, "engines_all.json"), "w"), indent=1)
for k, v in OUT.items(): print(k, v)
