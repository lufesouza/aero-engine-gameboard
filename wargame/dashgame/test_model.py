"""Checks that the game-master valuation is the user's board: run before every game.

1. The trace / 2060 extension patch leaves all 256 airframer cells unchanged at several EIS tuples.
2. A game state that maps onto a board cell reproduces that cell exactly (no GM adjustment fires).
3. The snapshot board still has 0 pure and 17 near-Nash equilibria; the engine board 1 pure and 19 near.
4. The engine start shares equal the board's derive_nb_engine_shares() for every supplier-code pair.
5. The year-by-year engine model, in board mode, reproduces simulate() for every CFM x RR move, PW lock and code
   pair tested; and a game state whose programmes are all ready at the board's EIS reproduces it too.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as M  # noqa: E402

H = M.H
TOL = 1e-9
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


# 1. patch is PV-neutral
for eis in [(2041, 2037, 2035, 2035), (2044, 2037, 2035, 2035), (2037, 2037, 2040, 2035), (2055, 2057, 2050, 2040)]:
    over = {"af_fps_eis": eis[0], "af_ngsa_eis": eis[1], "af_787_eis": eis[2], "af_a350_eis": eis[3]}
    MX0, A, B, _ = H.af(over, H.OVERLAP_PATCH)
    MX1, _, _, _ = H.af(over, M.AF_PATCH)
    for i in range(len(A)):
        for j in range(len(B)):
            for k in ("a_total_delta", "b_total_delta", "a_scen_nb_pv", "b_scen_wb_pv"):
                check(abs(MX0[i][j][k] - MX1[i][j][k]) < TOL, ("patch", eis, i, j, k))
print("1. trace patch PV-neutral on 4 x 256 cells")

# 2. state -> board cell
st = M.new_state()
st["prog"]["fps"] = {"launch": 2031, "eis": 2041, "variant": "10yr", "cancel": None}
st["prog"]["ngsa"] = {"launch": 2030, "eis": 2037, "cancel": None}
st["prog"]["re787"] = {"launch": 2030, "eis": 2035, "cancel": None}
st["prog"]["rea350"] = {"launch": 2030, "eis": 2035, "cancel": None}
st["dt"] = {"bottleneck": 2030, "poaching": 2030}
st["codes"] = {"fps": 7, "ngsa": 6}
v = M.value_airframers(st)
MX, A, B, SS = H.af({}, H.OVERLAP_PATCH)
c = MX[A.index(v["_inputs"]["a"])][B.index(v["_inputs"]["b"])]
check(abs(v["boeing"]["pv_delta"] - c["b_total_delta"]) < TOL, "state->cell boeing")
check(abs(v["airbus"]["pv_delta"] - c["a_total_delta"]) < TOL, "state->cell airbus")
print("2. snapshot-like state = board cell: Boeing %.4f / %.4f, Airbus %.4f / %.4f" % (
    v["boeing"]["pv_delta"], c["b_total_delta"], v["airbus"]["pv_delta"], c["a_total_delta"]))
# never-launched fps with Delay Tactics ordered 2030: naked fine as the board books it
st2 = M.new_state(); st2["dt"] = {"bottleneck": 2030, "poaching": None}
v2 = M.value_airframers(st2)
c2 = MX[A.index(v2["_inputs"]["a"])][B.index(v2["_inputs"]["b"])]
check(abs(v2["airbus"]["pv_delta"] - c2["a_total_delta"]) < TOL, "naked fine = board")
print("   naked Delay Tactics ordered 2030 = board: %.4f / %.4f" % (v2["airbus"]["pv_delta"], c2["a_total_delta"]))

# 3. snapshot equilibria
r = H.check_snapshot(MX, A, B, H.parse_snapshot(os.path.join(M.HERE, "board", "Game.txt")))
check(r["pure"] == 0 and r["near"] == 17 and r["missing"] == 0 and r["extra"] == 0 and not r["bad_round"], ("snapshot", r))
SE = H.en({})
check(len(SE["_EPURE"]) == 1 and len(SE["_ENEAR"]) == 19, "engine snapshot")
print("3. snapshot: airframer", r, "| engine pure", len(SE["_EPURE"]), "near", len(SE["_ENEAR"]))

# 4. start shares = derive_nb_engine_shares
mod = SE["_MOD"]
for bc, ac in itertools.product(range(1, 8), range(1, 8)):
    rr, pw, cfm = mod.derive_nb_engine_shares(bc, ac, 50)
    s = M.start_from_slots([(M.CODE_SETS[bc][0], 0.5), (M.CODE_SETS[ac][0], 0.5)], False)
    check(all(abs(x - y / 100.0) < TOL for x, y in zip(s, (cfm, pw, rr))), ("derive", bc, ac))
print("4. start shares = board derive_nb_engine_shares for 49 code pairs")

# 5. engine model vs simulate
SUP = {v_: k for k, v_ in mod.SUPPLIER_CODE.items()}
n5 = 0
for bc, ac, nb_eis, wb_eis in [(7, 6, 2037, 2035), (4, 6, 2037, 2035), (1, 6, 2041, 2040), (3, 2, 2040, 2035),
                               (5, 4, 2037, 2038), (3, 3, 2037, 2035)]:
    if (bc, ac) in M.FORBIDDEN:
        continue
    rr, pw, cfm = mod.derive_nb_engine_shares(bc, ac, 50)
    jv = (bc == 4 or ac == 4)
    over = {"_b_supplier": SUP[bc], "_a_supplier": SUP[ac], "_last_b_supp_seen": SUP[bc], "_last_a_supp_seen": SUP[ac],
            "_last_boeing_share_seen": 50, "f_cfm_nb": cfm, "f_pw_nb": pw, "f_rr_nb": rr, "f_jv_nb": pw + rr,
            "af_fps_eis": nb_eis, "af_ngsa_eis": nb_eis, "af_787_eis": wb_eis, "af_a350_eis": wb_eis}
    SE = H.en(over)
    sim, EA, EC, PWm = SE["_ESIM"], SE["_EA"], SE["_EC"], SE["_EPW"]
    f = (cfm, (pw + rr) / 2, (pw + rr) / 2) if jv else (cfm, pw, rr)
    P = M.engine_params()
    for ma in EA + ["2-Ducted Only | 4-Partner Embraer | 5-Lobby Govts | 7-Invest GenX", "1-Open Fan Only | 5-Lobby Govts"]:
        for mc in EC:
            res = sim(ma, PWm, mc, 31)
            bm = M.value_engines(None, None, board_mode=(f, nb_eis - 2026, wb_eis - 2026, ma, PWm, mc))
            for i, k in enumerate("ABC"):
                d = bm["new"][i] - bm["old"][i] - res[k]["strain_b"] - res[k]["inv_b"]
                check(abs(d - res[k]["delta_b"]) < 1e-9, ("sim", bc, ac, ma, mc, k, d, res[k]["delta_b"]))
            n5 += 1
print("5. engine board mode = simulate() on %d move combinations" % n5)

# 5b. a game state, all programmes ready at the board's EIS, fixed 50/50 split -> simulate()
st = M.new_state()
st["prog"]["fps"] = {"launch": 2030, "eis": 2037, "variant": "7yr", "cancel": None}
st["prog"]["ngsa"] = {"launch": 2030, "eis": 2037, "cancel": None}
st["prog"]["re787"] = {"launch": 2030, "eis": 2035, "cancel": None}
st["codes"] = {"fps": 7, "ngsa": 6}
for k, l in (("cfm_ducted", 2030), ("pw_solo", 2030), ("rr_solo", 2030), ("cfm_genx", 2030), ("rr_t1000", 2030)):
    st["prog"][k] = {"launch": l, "ready": M.engine_ready(k, l), "cancel": None}
st["prog"]["cfm_genx"]["kind"] = "genx9"
ve = M.value_engines(st, {y: 0.5 for y in range(2026, 2080)})
rr, pw, cfm = mod.derive_nb_engine_shares(7, 6, 50)
over = {"_b_supplier": SUP[7], "_a_supplier": SUP[6], "_last_b_supp_seen": SUP[7], "_last_a_supp_seen": SUP[6],
        "_last_boeing_share_seen": 50, "f_cfm_nb": cfm, "f_pw_nb": pw, "f_rr_nb": rr,
        "af_fps_eis": 2037, "af_ngsa_eis": 2037, "af_787_eis": 2035, "af_a350_eis": 2035}
SE = H.en(over)
res = SE["_ESIM"]("2-Ducted Only | 6-Upgrade GenX9", SE["_EPW"], "2-Ultrafan NB Solo | 4-Upgrade T1000", 31)
for side, k in (("cfm", "A"), ("pratt_whitney", "B"), ("rolls_royce", "C")):
    check(abs(ve[side]["pv_delta"] - res[k]["delta_b"]) < 1e-9, ("state engine", side, ve[side]["pv_delta"], res[k]["delta_b"]))
print("5b. game state = simulate(): CFM %.4f / %.4f, PW %.4f / %.4f, RR %.4f / %.4f" % (
    ve["cfm"]["pv_delta"], res["A"]["delta_b"], ve["pratt_whitney"]["pv_delta"], res["B"]["delta_b"],
    ve["rolls_royce"]["pv_delta"], res["C"]["delta_b"]))

if fails:
    print("FAILURES:", len(fails))
    for f_ in fails[:20]:
        print("  ", f_)
    sys.exit(1)
print("ALL CHECKS PASSED")
