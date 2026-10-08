"""Second pass: share/timing split, Airbus NGSA timing response, Boeing restoration thresholds, vacuum sizing."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTDIR, exist_ok=True)
from delay import AROWS, FPS10, FPS7, EMB, DN, cell

OUT = {}
AR = AROWS["NGSA + Re-engine A350"]; AS = AROWS["NGSA + Bottleneck + Re-engine A350"]
def solve(over):
    return H.af(over, H.OVERLAP_PATCH)

# 1) Share paths and per-year fps-minus-Do-Nothing NB profit streams, from the board's own share helper
def streams(fps_eis, ngsa_eis=2037, sab=False):
    MX, A, B, SS = solve({"af_fps_eis": fps_eis, "af_ngsa_eis": ngsa_eis})
    mod = SS["_MOD"]
    bt, at = fps_eis - 2026, ngsa_eis - 2026
    rows = []
    for t in range(0, bt + 20):
        f = mod._compute_nb_share_unified(t, True, True, bt, at, is_7yr=False)
        f = mod._apply_nb_modifiers(f[0], f[1], t, bt, at, True, True, active_sabs=1 if sab else 0, sab_share_pp=5.0)
        d = mod._compute_nb_share_unified(t, False, True, bt, at, is_7yr=False)
        pf = 2000 * f[0] * (0.055 if t >= bt else 0.048) * (0.2564 if t >= bt else 0.08)
        pd_ = 2000 * d[0] * 0.048 * 0.08
        rows.append({"year": 2026 + t, "b_share_fps": round(f[0], 4), "b_share_dn": round(d[0], 4), "diff_b": pf - pd_, "df": 1 / 1.105 ** t})
    return rows
s41, s44 = streams(2041), streams(2044)
npv = lambda rows: sum(r["diff_b"] * r["df"] for r in rows)
nb41, nb44 = npv(s41), npv(s44)
shifted = nb41 / 1.105 ** 3            # same 2041 stream, 3 years later
OUT["nb_split"] = {"nb_2041": round(nb41, 6), "nb_2044": round(nb44, 6), "timing_only": round(shifted - nb41, 6), "share_effect": round(nb44 - shifted, 6)}
OUT["share_paths"] = {"2041": [(r["year"], r["b_share_fps"], r["b_share_dn"]) for r in s41], "2044": [(r["year"], r["b_share_fps"], r["b_share_dn"]) for r in s44]}
# whole-project timing (net of capex/alpha), using solved cells
MX41 = solve({"af_fps_eis": 2041}); MX44 = solve({"af_fps_eis": 2044})
v41 = cell(MX41[0], MX41[1], MX41[2], AR, FPS10("Milk_787"))["b_total_delta"] - cell(MX41[0], MX41[1], MX41[2], AR, DN("Milk_787"))["b_total_delta"]
v44 = cell(MX44[0], MX44[1], MX44[2], AR, FPS10("Milk_787"))["b_total_delta"] - cell(MX44[0], MX44[1], MX44[2], AR, DN("Milk_787"))["b_total_delta"]
OUT["project_split"] = {"v2041": round(v41, 6), "v2044": round(v44, 6), "pure_timing": round(v41 / 1.105 ** 3 - v41, 6), "share_effect": round(v44 - v41 / 1.105 ** 3, 6)}

# 2) Airbus response: NGSA EIS timing with fps at 2044 (and at 2041 for reference)
tim = []
for fe in (2041, 2044):
    for ne in range(2035, 2046):
        MX, A, B, SS = solve({"af_fps_eis": fe, "af_ngsa_eis": ne})
        jf = B.index(FPS10("Milk_787")); jd = B.index(DN("Milk_787"))
        pure, near = H.eq_lists(MX, A, B)
        tim.append({"fps_eis": fe, "ngsa_eis": ne,
                    "airbus_vs_fps10": round(MX[A.index(AS)][jf]["a_total_delta"], 6),
                    "airbus_vs_fps10_noDT": round(MX[A.index(AR)][jf]["a_total_delta"], 6),
                    "airbus_vs_dn": round(MX[A.index(AR)][jd]["a_total_delta"], 6),
                    "boeing_fps10_minus_dn": round(MX[A.index(AR)][jf]["b_total_delta"] - MX[A.index(AR)][jd]["b_total_delta"], 6),
                    "boeing_fps10_minus_dn_DT": round(MX[A.index(AS)][jf]["b_total_delta"] - MX[A.index(AS)][jd]["b_total_delta"], 6),
                    "pure": len(pure), "near": len(near), "eq_boeing_moves": sorted({H.lab(b) for a, b, *_ in pure + near}),
                    "eq_airbus_moves": sorted({H.lab(a) for a, b, *_ in pure + near})})
OUT["ngsa_timing"] = tim

# 3) Boeing restoration thresholds at fps 2044 (linear levers by 2-run linearity + confirmation; nonlinear levers by grid)
def fpsval(over, ctx=AR, wb="Milk_787", var=FPS10):
    o = {"af_fps_eis": 2044}; o.update(over)
    MX, A, B, SS = solve(o)
    return cell(MX, A, B, ctx, var(wb))["b_total_delta"] - cell(MX, A, B, ctx, DN(wb))["b_total_delta"]
thr = {}
for key, base, step, label in (("af_m_fps", 25.64, 1.0, "fps margin (%)"), ("af_cx_fps10", 55.25, -5.0, "fps 10yr capex ($B)"),
                               ("af_price_fps", 55.0, 1.0, "fps price ($M)")):
    for ctxn, ctx in (("modal", AR), ("delay_tactics", AS)):
        g0 = fpsval({}, ctx); g1 = fpsval({key: base + step}, ctx)
        k = (g1 - g0) / step; x = base - g0 / k
        conf = fpsval({key: round(x, 4)}, ctx)
        # +$1B go/no-go hurdle (war-game rule) for the modal context; $-2B slip floor for Delay Tactics
        hurdle = 1.0 if ctxn == "modal" else -2.0
        xh = base + (hurdle - g0) / k
        thr[f"{label} | {ctxn}"] = {"base": base, "g0": round(g0, 6), "k_per_unit": round(k, 4), "breakeven": round(x, 6), "confirm_at_breakeven": round(conf, 4), "hurdle": hurdle, "value_at_hurdle": round(xh, 6)}
# capture speed (Boeing Phase-2 recovery pp/yr) and post-2037 balance share: grid
grid = []
for pp in (1.0, 1.5, 2.0, 3.0, 4.0):
    for bal in (50, 55, 60):
        grid.append({"ramp10_b_pp": pp, "balance_share": bal, "fps10_minus_dn": round(fpsval({"af_ramp10_b_pp": pp, "_boeing_share_both": bal}), 6),
                     "fps10_minus_dn_DT": round(fpsval({"af_ramp10_b_pp": pp, "_boeing_share_both": bal}, AS), 6)})
thr["grid_recovery_speed_x_balance"] = grid
# Airbus Delay Tactics share shift: what if Delay Tactics bite harder (war-game style), 0..10pp
thr["delay_tactics_shift"] = [{"sab_share": s, "fps10_minus_dn_DT": round(fpsval({"af_sab_share": s}, AS), 6)} for s in (0, 2.5, 5, 7.5, 10)]
# fps 7yr variant at 2044 and via-Embraer capex break-even vs Do Nothing
thr["fps7_minus_dn_2044"] = round(fpsval({}, AR, var=FPS7), 6)
thr["via_embraer_minus_dn_2044"] = round(fpsval({}, AR, var=EMB), 6)
thr["note"] = ("margin and price thresholds are exact (payoffs are linear in them); the bill thresholds here are two-run linear "
               "estimates and the debt penalty is cubic in the bill, so use robustness.json lever_thresholds_2044 for exact values")
OUT["thresholds_2044"] = thr

# 4) Vacuum sizing: Airbus NB units/yr implied by the board's shares (2000 NB/yr market)
vac = []
for fe in (2041, 2044):
    rows = streams(fe)
    for r in rows:
        if r["year"] in (2030, 2035, 2037, 2040, 2041, 2043, 2044, 2045, 2050, 2056, 2060, 2063):
            vac.append({"fps_eis": fe, "year": r["year"], "boeing_share_if_fps": r["b_share_fps"], "airbus_units_if_fps": round(2000 * (1 - r["b_share_fps"])),
                        "boeing_share_if_dn": r["b_share_dn"], "airbus_units_if_dn": round(2000 * (1 - r["b_share_dn"]))})
OUT["vacuum"] = vac
# Airbus excess units over 'status-quo 60%' while Boeing lacks a new NB, 2037..fps EIS-1 (cumulative)
for fe in (2041, 2044):
    rows = streams(fe)
    OUT[f"airbus_units_above_60pct_{fe}"] = round(sum(2000 * (1 - r["b_share_fps"] - 0.6) for r in rows if r["year"] < fe and r["year"] >= 2037))
    OUT[f"airbus_units_above_60pct_fps_window_{fe}"] = round(sum(2000 * max(0, (1 - r["b_share_fps"]) - 0.6) for r in rows))

json.dump(OUT, open(os.path.join(OUTDIR, "analysis2.json"), "w"), indent=1)
print("NB split", OUT["nb_split"]); print("project split", OUT["project_split"])
print("NGSA timing:")
for r in tim: print("  ", r["fps_eis"], r["ngsa_eis"], "A vs fps10 (DT)", r["airbus_vs_fps10"], "A vs DN", r["airbus_vs_dn"], "| B fps10-DN", r["boeing_fps10_minus_dn"], "DT", r["boeing_fps10_minus_dn_DT"], "| eq", r["pure"], r["near"], r["eq_boeing_moves"][:3])
print("thresholds:")
for k, v in thr.items():
    if isinstance(v, dict) and "breakeven" in v: print("  ", k, v)
print("  grid:"); [print("    ", g) for g in grid]
print("  DT shift:", thr["delay_tactics_shift"]); print("  fps7-DN 2044:", thr["fps7_minus_dn_2044"], " via Embraer - DN:", thr["via_embraer_minus_dn_2044"])
print("vacuum:"); [print("  ", v) for v in vac]
print({k: v for k, v in OUT.items() if k.startswith("airbus_units")})
