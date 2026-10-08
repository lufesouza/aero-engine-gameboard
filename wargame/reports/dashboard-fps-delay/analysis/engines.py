"""Engine board under three narrowbody outcomes (the engine board itself ignores the fps date)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTDIR, exist_ok=True)
CASES = {
    "snapshot (fps 2041, Boeing 50% of new-NB market, fps engines from all 3 makers)": {},
    "fps 2044 launched, Boeing ~30% of new-NB market": {"_boeing_share_both": 30},
    "Boeing Do Nothing: 737 stays on LEAP at 20%": {"_b_supplier": "CFM (Ducted)", "_boeing_share_both": 20},
}
OUT = {}
for name, ov in CASES.items():
    SS = H.en(ov)
    MX, EA, EC = SS["_EMX"], SS["_EA"], SS["_EC"]
    rec = {"pw_locked": SS["_EPW"], "f_nb": (SS.get("f_cfm_nb"), SS.get("f_pw_nb"), SS.get("f_rr_nb")), "pure": [], "near_count": len(SS["_ENEAR"])}
    for a, c in SS["_EPURE"]:
        m = MX[a][c]
        rec["pure"].append({"cfm": EA[a], "rr": EC[c], "cfm_yield": round(m["A"]["yield_pct"], 1), "pw_yield": round(m["B"]["yield_pct"], 1), "rr_yield": round(m["C"]["yield_pct"], 1),
                            "cfm_b": round(m["A"]["delta_b"], 6), "pw_b": round(m["B"]["delta_b"], 6), "rr_b": round(m["C"]["delta_b"], 6)})
    # Embraer partnership (code path that the board never evaluates): value it directly with the board's simulate()
    sim = SS["_ESIM"]
    base = [x for x in EA if x == "2-Ducted Only"][0]
    rr = rec["pure"][0]["rr"] if rec["pure"] else EC[0]
    r0 = sim("2-Ducted Only", SS["_EPW"], rr, 31); r1 = sim("2-Ducted Only | 4-Partner Embraer", SS["_EPW"], rr, 31)
    rec["cfm_partner_embraer_increment_b"] = round(r1["A"]["delta_b"] - r0["A"]["delta_b"], 6)
    rec["pw_when_cfm_partners_embraer_b"] = round(r1["B"]["delta_b"] - r0["B"]["delta_b"], 6)
    OUT[name] = rec
json.dump(OUT, open(os.path.join(OUTDIR, "engines.json"), "w"), indent=1)
for k, v in OUT.items(): print(k, json.dumps(v, indent=0)[:900])
