"""Size the narrowbody 'vacuum' implied by the board's share paths, against Airbus's physical capacity,
and value a third entrant that fills it, using the board's own conventions (2,000 NB/yr, lump capex at EIS,
alpha debt penalty) so the numbers are comparable with the fps business case."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUTDIR, exist_ok=True)

def paths(fps_eis, launch=True):
    SS = H.af({"af_fps_eis": fps_eis}, H.OVERLAP_PATCH)[3]; mod = SS["_MOD"]
    bt, at = fps_eis - 2026, 2037 - 2026
    out = {}
    for t in range(0, 38):
        b, a = mod._compute_nb_share_unified(t, launch, True, bt, at, is_7yr=False)
        out[2026 + t] = a
    return out
OUT = {"cases": {}}
for name, fe, launch in (("fps 2041", 2041, True), ("fps 2044", 2044, True), ("Boeing Do Nothing", 2044, False)):
    ap = paths(fe, launch)
    case = {"airbus_share": {y: round(ap[y], 3) for y in (2037, 2040, 2041, 2043, 2044, 2046, 2050, 2056)}}
    for cap in (900, 1080, 1200, 1320):
        uns = {y: max(0.0, 2000 * ap[y] - cap) for y in range(2037, 2057)}
        case[f"unserved_cap{cap}"] = {"cum_2037_2056": round(sum(uns.values())), "peak_per_yr": round(max(uns.values())),
                                      "years_with_gap": sum(1 for v in uns.values() if v > 0)}
    OUT["cases"][name] = case

# Entrant value with board conventions: units/yr = unserved units at an Airbus capacity of 1,200/yr (100 a month),
# captured from the entrant's EIS with a 3-year ramp; price/margin/capex/WACC as stated; lump capex at EIS (board rule)
def entrant(case, eis, capex, price_m=48.0, margin=0.12, wacc=0.10, cap=1200, take=1.0, ev=None, debt=None, alpha=0.3, end=2056):
    ap = paths({"fps 2041": 2041, "fps 2044": 2044, "Boeing Do Nothing": 2044}[case], case != "Boeing Do Nothing")
    v = 0.0; units = 0
    for y in range(eis, end + 1):
        ramp = min(1.0, (y - eis + 1) / 3.0)
        u = take * ramp * max(0.0, 2000 * ap.get(y, ap[2063 if y > 2063 else y]) - cap)
        units += u
        v += u * price_m / 1000.0 * margin / (1 + wacc) ** (y - 2026)
    pv_capex = capex / (1 + wacc) ** (eis - 2026)
    pen = 0.0
    if ev and debt is not None:
        pen = ((debt + capex) * alpha * ((debt + capex) / ev) ** 2 - debt * alpha * (debt / ev) ** 2) / (1 + wacc) ** (eis - 2026)
    return {"case": case, "eis": eis, "capex_b": capex, "units_2037_2056": round(units), "pv_margin": round(v, 2), "pv_capex": round(pv_capex, 2), "alpha_pen": round(pen, 2), "npv": round(v - pv_capex - pen, 2)}
ent = []
for case in ("fps 2041", "fps 2044", "Boeing Do Nothing"):
    for eis in (2036, 2038, 2040):
        for capex in (15.0, 25.0):
            ent.append(entrant(case, eis, capex))
OUT["entrant_unserved_only"] = ent
# Entrant that also wins a fixed slice of the whole market (dual-source / national demand), e.g. 5% and 10%
def entrant_slice(case, eis, capex, slice_, price_m=48.0, margin=0.12, wacc=0.10, cap=1200):
    base = entrant(case, eis, capex, price_m, margin, wacc, cap)
    extra = sum(min(1.0, (y - eis + 1) / 3.0) * 2000 * slice_ * price_m / 1000.0 * margin / (1 + wacc) ** (y - 2026) for y in range(eis, 2057))
    base["slice"] = slice_; base["npv_with_slice"] = round(base["npv"] + extra, 2); return base
OUT["entrant_with_slice"] = [entrant_slice(c, 2038, 20.0, s) for c in ("fps 2041", "fps 2044") for s in (0.05, 0.10)]
json.dump(OUT, open(os.path.join(OUTDIR, "vacuum.json"), "w"), indent=1)
for k, v in OUT["cases"].items(): print(k, v)
for e in ent: print(e)
for e in OUT["entrant_with_slice"]: print(e)


# ── Entrant sensitivities used in the report (added after review) ──────────────────────────────────────────────
def entrant2(case, eis=2038, capex=15.0, cap=1200, price_m=48.0, margin=0.12, wacc=0.10, spread=None, boeing_cap=None, end=2056):
    """Entrant serving demand the board gives Airbus beyond Airbus's capacity.
    spread=(first, last): bill paid evenly over those calendar years instead of one lump at entry into service.
    boeing_cap: aircraft/yr the 737 line can build; its slack above the board's Boeing demand absorbs overflow first."""
    fe, launch = {"fps 2041": (2041, True), "fps 2044": (2044, True), "Boeing Do Nothing": (2044, False)}[case]
    SS = H.af({"af_fps_eis": fe}, H.OVERLAP_PATCH)[3]; mod = SS["_MOD"]
    v = 0.0
    for y in range(eis, end + 1):
        b, a = mod._compute_nb_share_unified(y - 2026, launch, True, fe - 2026, 2037 - 2026, is_7yr=False)
        over = max(0.0, 2000 * a - cap)
        if boeing_cap is not None:
            over = max(0.0, over - max(0.0, boeing_cap - 2000 * b))
        v += min(1.0, (y - eis + 1) / 3.0) * over * price_m / 1000.0 * margin / (1 + wacc) ** (y - 2026)
    if spread:
        n = spread[1] - spread[0] + 1
        pv_capex = sum(capex / n / (1 + wacc) ** (y - 2026) for y in range(spread[0], spread[1] + 1))
    else:
        pv_capex = capex / (1 + wacc) ** (eis - 2026)
    return round(v - pv_capex, 6)

if __name__ == "__main__":
    CASES = ("fps 2041", "fps 2044", "Boeing Do Nothing")
    S = {
        "lump_eis2038_cap1200": {c: entrant2(c) for c in CASES},
        "lump_eis2042_cap1200": {c: entrant2(c, eis=2042) for c in CASES},
        "spread2034_41_eis2042_cap1200": {c: entrant2(c, eis=2042, spread=(2034, 2041)) for c in CASES},
        "lump_eis2038_cap1200_737_rate47": {c: entrant2(c, boeing_cap=564) for c in CASES},
        "lump_eis2038_cap900": {c: entrant2(c, cap=900) for c in CASES},
    }
    OUT["entrant_sensitivities"] = S
    json.dump(OUT, open(os.path.join(OUTDIR, "vacuum.json"), "w"), indent=1)
    for k, v in S.items(): print(k, v)
