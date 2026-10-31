"""Manual build of the "MAX phase-out" scenario (run dash-2050-cons, Do Nothing), before it goes into the game.

The user's scenario: in Do Nothing the 737 MAX starts to phase out in 2045 and is gone by 2060; the demand it leaves is met
partly by Airbus building more, by COMAC, and by a new entrant (an Embraer-like newcomer). This script builds that world
year by year on the game's own supply-and-demand rules (supply_demand.year_rows, copied here with three switches), so the
numbers can be checked and changed before the engine is changed:

  1. Boeing: the 737 MAX on the game's path (57 a month from 2030), then down in a straight line from 2045 to none in 2060.
  2. Airbus: the game's plan (A320neo family, then NGSA to 100 a month, plus the game's 1%-a-year capacity response when
     short), plus EXTRA lines from 2045: +5 a month each year, up to +20 a month.
  3. A third tier, COMAC and the new entrant: customers Boeing and Airbus cannot serve (after the game's own overflow between
     the two) take a COMAC or entrant aircraft if one is free, up to their capacity, split in proportion to capacity. What is
     left waits a year (a tenth drop out), as in the game.

With every switch off, the copy gives back supply_demand.year_rows exactly (asserted). Demand: the user's page "Single-Aisle
Replacement Story" (chart 4.1), aircraft retiring as chapter 1 sets out, the game's conservative curve before 2038, the
737/A320 class share applied (demand_scenarios/curves/page_N0.json). Case: Airbus launches NGSA (in service 2037), Boeing's
expected case. Writes scenario.json and scenario.png next to this file.

  python3 build_scenario.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "demand_scenarios"))
import demand_scenarios as D  # noqa: E402

L, M, SD = D.L, D.M, D.SD
YEARS = list(range(2026, 2061))

# ─────────────────────────────── the scenario's assumptions (edit here) ───────────────────────────────
MAX_PHASE = {"start": 2045, "gone": 2060}            # full rate to 2044, straight line down, none in 2060
AIRBUS_EXTRA = {"from": 2045, "step_per_year": 5.0, "cap": 20.0}   # extra a month on top of the game's plan
COMAC = {2026: 28, 2030: 93, 2035: 150, 2045: 200, 2050: 250}      # a year, straight lines between (IBA to 2030; COMAC's
#   150-a-year goal reached in 2035; 250 a year, about an eighth of the class market, from 2050)
ENTRANT = {"eis": 2040, "peak_a_month": 20.0, "years_to_peak": 6}  # Embraer-like: in service 2040, 20 a month six years on
WILLING = 1.0                                        # share of unserved customers who take a COMAC or entrant aircraft


def interp(pts, y):
    ks = sorted(pts)
    if y <= ks[0]:
        return float(pts[ks[0]]) if y == ks[0] else 0.0
    if y >= ks[-1]:
        return float(pts[ks[-1]])
    for a, b in zip(ks, ks[1:]):
        if a <= y <= b:
            return pts[a] + (pts[b] - pts[a]) * (y - a) / (b - a)
    return 0.0


def entrant_cap(y):
    e = ENTRANT
    return 0.0 if y < e["eis"] else 12.0 * e["peak_a_month"] * min(1.0, (y - e["eis"] + 1) / e["years_to_peak"])


def max_cap(y, base):
    s, g = MAX_PHASE["start"], MAX_PHASE["gone"]
    if y < s:
        return base
    return base * max(0.0, (g - y) / (g - s + 1))


def airbus_extra(y):
    if y < AIRBUS_EXTRA["from"]:
        return 0.0
    return 12.0 * min(AIRBUS_EXTRA["cap"], AIRBUS_EXTRA["step_per_year"] * (y - AIRBUS_EXTRA["from"] + 1))


def year_rows(state, b_pref_by_year, years, phase=False, extra=False, third=False):
    """supply_demand.year_rows with three switches: the MAX phase-out, Airbus's extra lines, the third tier."""
    o = SD.options()
    out = {}
    fx, lapse = SD.flex(), SD.inputs()["demand"]["lapse_per_year"]
    bb, ba = 0.0, 0.0
    kb, ka = SD.firm_backlog()
    netted = o.get("firm_backlog") == "netted"
    cb, ca = 0.0, 0.0
    resp = float(o.get("airbus_capacity_response") or 0.0)
    m_a = 1.0
    for y in sorted(years):
        mb, fb = SD.boeing_capacity(state, y)
        if phase:
            mb = max_cap(y, mb)
        a3, ng = SD.airbus_capacity(state, y)
        a3, ng = a3 * m_a, ng * m_a
        xa = airbus_extra(y) if extra else 0.0
        gross = SD.demand(y)
        if netted:
            need = min(gross, kb + ka)
            nb_ = need * kb / (kb + ka) if kb + ka > 0 else 0.0
            na_ = need - nb_
            open_b, open_a = kb + cb, ka + ca
            kb, ka = kb - nb_, ka - na_
            fb_in, fa_in = cb + nb_, ca + na_
            d = gross - need
        else:
            fb_in, fa_in, d = kb, ka, gross
        base = SD.boeing_base_pref(state, y, b_pref_by_year[y])
        free_a = max(0.0, a3 + ng + xa - min(fa_in, a3 + ng + xa) - ba)
        pref = base
        if o.get("boeing_takes_airbus_slack") and d > 0:
            pref = min(1.0, max(base, 1.0 - free_a / d))
        r = SD.deliveries(pref, d, mb + fb, a3 + ng + xa, fx, bb, ba, lapse, fb_in, fa_in)
        r.update({"demand_gross": gross, "pref_b": pref, "cap_max": mb, "cap_a320": a3, "cap_ngsa": ng, "cap_extra": xa})
        # third tier: customers still unserved after the overflow between Boeing and Airbus
        cc = interp(COMAC, y) if third else 0.0
        ce = entrant_cap(y) if third else 0.0
        ub, ua = r["backlog_b"] / (1.0 - lapse), r["backlog_a"] / (1.0 - lapse)     # unserved, before the drop-out
        take = min(WILLING * (ub + ua), cc + ce)
        tb = take * ub / (ub + ua) if ub + ua > 0 else 0.0
        ta = take - tb
        r["dlv_comac"] = take * cc / (cc + ce) if cc + ce > 0 else 0.0
        r["dlv_entrant"] = take - r["dlv_comac"]
        r["cap_comac"], r["cap_entrant"] = cc, ce
        r["backlog_b"], r["backlog_a"] = (ub - tb) * (1.0 - lapse), (ua - ta) * (1.0 - lapse)
        r["lost"] = (ub - tb + ua - ta) * lapse
        if netted:
            cb, ca = r["firm_b"], r["firm_a"]
            r["firm_in_b"], r["firm_in_a"] = open_b, open_a
            r["firm_b"], r["firm_a"] = kb + cb, ka + ca
        if resp and (1.0 - base) * d > free_a + 1e-9:
            m_a *= 1.0 + resp
        if not netted:
            kb, ka = r["firm_b"], r["firm_a"]
        r["dlv_max"] = r["delivered_b"] - min(r["delivered_b"], fb)
        r["dlv_airbus"] = r["delivered_a"]
        bb, ba = r["backlog_b"], r["backlog_a"]
        out[y] = r
    return out


def main():
    kw = D.demand_kw("0")
    with L.patched(**kw):
        st, cv = L.grid_states(L.PLAN_DN)[1]                 # Do Nothing, Airbus launches NGSA
        eis, a, b, dt = M.af_inputs(st, cv)
        cell = M.eval_cell(eis, a, b, trace=True)
        ser = M.af_series(st, cell, eis, dt)
        pref = {r["year"]: r["boeing"]["nb_share"] for r in ser["years"]}
        ys = [y for y in sorted(pref) if y >= 2026]
        game = SD.year_rows(st, pref, ys)
        mine = year_rows(st, pref, ys)
        for y in ys:                                          # every switch off: the game's own rows, exactly
            for k in ("delivered_b", "delivered_a", "lost", "backlog_b", "backlog_a", "cap_max"):
                assert abs(game[y][k] - mine[y][k]) < 1e-9, (y, k, game[y][k], mine[y][k])
        new = year_rows(st, pref, ys, phase=True, extra=True, third=True)
        steps = {"Boeing's MAX phase-out only": year_rows(st, pref, ys, phase=True),
                 "+ Airbus extra lines": year_rows(st, pref, ys, phase=True, extra=True)}
    df = {r["year"]: r["df_b"] for r in ser["years"]}
    unit737 = 48.0 * 0.08 / 1000.0                          # $B per 737 (the dashboard's legacy unit)

    def row(r):
        return {"demand": r["demand_gross"], "max": r["dlv_max"], "airbus": r["dlv_airbus"], "comac": r.get("dlv_comac", 0.0),
                "entrant": r.get("dlv_entrant", 0.0), "lost": r["lost"], "cap_max": r["cap_max"],
                "cap_airbus": r["cap_a320"] + r["cap_ngsa"] + r["cap_extra"], "cap_extra": r["cap_extra"],
                "cap_comac": r.get("cap_comac", 0.0), "cap_entrant": r.get("cap_entrant", 0.0)}
    out = {"assumptions": {"max_phase": MAX_PHASE, "airbus_extra_a_month": AIRBUS_EXTRA, "comac_a_year": COMAC,
                           "entrant_a_year": ENTRANT, "willing": WILLING,
                           "demand": "user's page chart 4.1, retiring as chapter 1 sets out (game curve before 2038), class share applied",
                           "case": "Do Nothing, Airbus launches NGSA (in service 2037)"},
           "baseline": {y: row(mine[y]) for y in YEARS}, "scenario": {y: row(new[y]) for y in YEARS},
           "steps": {k: {y: row(v[y]) for y in YEARS} for k, v in steps.items()}}
    # who serves the MAX's customers, 2045-2060
    span = range(2045, 2061)
    tot = lambda rows, k: sum(rows[y][k] for y in span)
    B, S = out["baseline"], out["scenario"]
    out["shift_2045_60"] = {k: tot(S, k) - tot(B, k) for k in ("max", "airbus", "comac", "entrant", "lost")}
    out["max_profit_lost_pv"] = sum((B[y]["max"] - S[y]["max"]) * unit737 * df[y] for y in span if y in df and y <= 2060)
    json.dump(out, open(os.path.join(HERE, "scenario.json"), "w"), indent=1)
    print("2045-60 change vs Do Nothing as played:", {k: round(v) for k, v in out["shift_2045_60"].items()})
    print("737 profit lost, PV at 2026 ($B, indicative): %.2f" % out["max_profit_lost_pv"])
    for y in (2030, 2040, 2045, 2048, 2050, 2052, 2055, 2058, 2060):
        b_, s_ = B[y], S[y]
        print(y, "demand %4.0f | MAX %3.0f -> %3.0f | Airbus %4.0f -> %4.0f | COMAC %3.0f | entrant %3.0f | lost %3.0f -> %3.0f" % (
            s_["demand"], b_["max"], s_["max"], b_["airbus"], s_["airbus"], s_["comac"], s_["entrant"], b_["lost"], s_["lost"]))
    chart(out)


def chart(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    S, B = out["scenario"], out["baseline"]
    ys = YEARS
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=150, gridspec_kw={"width_ratios": [1.55, 1]})
    ax = axes[0]
    cols = [("max", "Boeing 737 MAX", "#2a78d6"), ("airbus", "Airbus (A320neo, NGSA, extra lines)", "#eb6834"),
            ("comac", "COMAC", "#c03b5b"), ("entrant", "New entrant", "#17a06f")]
    bottom = [0.0] * len(ys)
    for k, lab, c in cols:
        v = [S[y][k] for y in ys]
        ax.bar(ys, v, bottom=bottom, width=0.8, color=c, label=lab, edgecolor="white", linewidth=0.5)
        bottom = [a + b for a, b in zip(bottom, v)]
    ax.plot(ys, [S[y]["demand"] for y in ys], color="#141c28", lw=1.6, label="Demand (737/A320 class)")
    ax.axvline(2044.5, color="#556275", lw=1, ls=(0, (4, 3)))
    ax.text(2044.7, 2330, "MAX phase-out starts", fontsize=8.5, color="#556275")
    ax.set_xlim(2025.4, 2060.6)
    ax.set_ylim(0, 2450)
    ax.set_ylabel("Aircraft delivered a year")
    ax.set_title("Who builds the 737/A320-class aircraft, Do Nothing with the MAX phased out", loc="left", fontsize=10.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    ax2 = axes[1]
    ax2.plot(ys, [B[y]["max"] for y in ys], color="#9dc0ea", lw=2, label="737s sold, Do Nothing as played")
    ax2.plot(ys, [S[y]["max"] for y in ys], color="#2a78d6", lw=2.2, label="737s sold, MAX phased out")
    ax2.plot(ys, [S[y]["cap_max"] for y in ys], color="#8a95a5", lw=1.3, ls=(0, (5, 4)), label="737 capacity, phased out")
    ax2.set_xlim(2026, 2060)
    ax2.set_ylim(0, 800)
    ax2.set_title("The 737 alone", loc="left", fontsize=10.5, fontweight="bold")
    ax2.legend(frameon=False, fontsize=8, loc="lower left")
    for a in axes:
        a.grid(axis="y", color="#e3e8ef")
        a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    fig.text(0.01, 0.01, "Manual build before the game run. Demand: your page (retiring as chapter 1 sets out), game curve before 2038, "
             "class share applied. Airbus launches NGSA in 2037. BOEING PROPRIETARY.", fontsize=7.5, color="#556275")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(HERE, "scenario.png"))


if __name__ == "__main__":
    main()
