"""What fps margin and/or Boeing investment would have changed Boeing's decision in the MAX phase-out game.

For each round (2030, 2035, 2045, 2050), from the state the round started in (record/state_r{n-1}.json), in the run's
own world (sd_options_phaseout.json), every plan that could compete is valued exactly as Boeing's brief valued it, in
every rival column: Do Nothing, the 787 Re-engine alone, the four Solo fps plans (10-year and 7-year, at Renton and at
new sites) alone, and the 10-year plans beside the Re-engine (the 7-year beside the Re-engine overlaps 5 years and is
struck by the One-development-at-a-time rule, H4; the 737 Rate Increase and via-Embraer plans are checked to stay out of
contention). Then Boeing's process decides, as the round records show it working:

  the CEO      - takes the plan with the most value in the column the CEO expected (2030: S2 alone, as both the CEO and
                 the Board used it; 2035: S1 70% / S3 30%; 2045 and 2050: S1 80% / S2 20%). The 787 Re-engine alone is
                 a candidate only if it adds more than the $1B margin (the CEO's own lever rule; it held the Re-engine
                 on that ground in 2035, 2045 and 2050). Among plans within the $1B margin of the best plan, a tie-break
                 picks: "doing less" (Do Nothing < Re-engine < an fps < an fps with the Re-engine), or the better worst
                 column (the CEO's third tie-breaker in the record).
  the Board    - judges each order as an item: the submitted plan minus the same plan with that order held. It approves
                 an fps launch only if the item adds more than +$1B in the CEO's column (business case), loses no more
                 than $1B in any column (downside), and the plan's risk-case column is no more than $2B below Do
                 Nothing's (rating first). A vetoed order reverts to hold; the CEO cannot add a launch after a veto.
                 (A Re-engine beside an approved fps that fails its own item tests is vetoed and the fps goes ahead
                 alone; rating first is then checked again on that plan.)
  Four readings, which bracket what the record allows:
  "rule"       - doing less among the plans within $1B of the best plan; the fps launches only if the CEO's pick
                 contains it and the Board approves it.
  "pairwise"   - doing less applied again to the pick against each smaller plan, until none is within $1B of it.
  "worst_first"- among the plans within $1B of the best, the better worst column wins (ties: doing less).
  "premium"    - the rule, but the CEO may also give up to $2B of value against the best plan (the H8 cap) to choose
                 an fps for an objective (the 50/50 split).

Levers: the fps operating margin (on every fps delivered, price held at $55M) and Boeing's fps bill (10-year $60.32B,
7-year $65.0B, both scaled by the same share), each alone and together. Exact: each column moves by its discounted fps
deliveries x price x the margin change, and the bill change goes through the dashboard's own joint true-cost formula
(the debt penalty on all of Boeing's programmes together, which is why an fps beside the Re-engine costs more than the
two apart), with the two-front strain of a paired plan priced, as the dashboard prices it, at the PV factor of Boeing's
whole spend. The thresholds of the "rule" reading are re-checked on a re-solved dashboard: every competing row, every
column, against the shortcut. Also: 2045 and 2050 again with the conservative demand curve after 2060
(data/curves/page_n0_game2061.json, tail.py). Writes data/thresholds.json.

  python3 thresholds.py            (about an hour: the re-checks re-solve the dashboard)
  python3 thresholds.py fast       (no re-checks)
"""
import functools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import lib as L  # noqa: E402

M, R, B, SD = L.M, L.R, L.B, L.SD
P = M.af_params()
M0, PRICE0 = P["v_margin_fps"], P["PRICE_fps"] * 1000.0
BILL0 = {"10yr": P["v_capex_fps_10yr"], "7yr": P["v_capex_fps_7yr"]}
O = {k: v for k, v in json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json"))).items() if not k.startswith("_")}
GAME_TAIL = dict(O, demand_curve=os.path.abspath(os.path.join(HERE, "data", "curves", "page_n0_game2061.json")))
REC = os.path.join(HERE, "record")
YEARS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
CEO_W = {1: {1: 1.0}, 2: {0: 0.7, 2: 0.3}, 3: {0: 0.8, 1: 0.2}, 4: {0: 0.8, 1: 0.2}}
EPS, H8 = 1.0, 2.0
BUSINESS, DOWNSIDE, BUFFER = 1.0, -1.0, -2.0
DN, RE = "fps: hold + 787: hold", "fps: hold + 787 Re-engine"
SOLO = {"10-year at Renton": ("fps 10-yr at Renton + 787: hold", "10yr"), "10-year, new sites": ("fps 10-yr + 787: hold", "10yr"),
        "7-year at Renton": ("fps 7-yr at Renton + 787: hold", "7yr"), "7-year, new sites": ("fps 7-yr + 787: hold", "7yr")}
PAIRS = {"10-year at Renton + Re-engine": ("fps 10-yr at Renton + 787 Re-engine", "10yr"),
         "10-year, new sites + Re-engine": ("fps 10-yr + 787 Re-engine", "10yr")}
FINE = [k / 20 for k in range(21)]
MODES = ("rule", "pairwise", "worst_first", "premium")
SIZE = {"Do Nothing": 0, "Re-engine": 1}
SIZE.update({k: 2 for k in SOLO})
SIZE.update({k: 3 for k in PAIRS})
WITHOUT_FPS = {k: "Do Nothing" for k in SOLO}
WITHOUT_FPS.update({k: "Re-engine" for k in PAIRS})
ALONE = {"10-year at Renton + Re-engine": "10-year at Renton", "10-year, new sites + Re-engine": "10-year, new sites"}


class board:
    """Re-solve the dashboard with some of its own inputs changed (af_m_fps in %, af_cx_fps10 / af_cx_fps7 in $B)."""
    def __init__(self, **over):
        self.over = over

    def __enter__(self):
        self.saved = M.af_board
        over = self.over

        @functools.lru_cache(maxsize=None)
        def af_board(eis):
            o = {"af_fps_eis": eis[0], "af_ngsa_eis": eis[1], "af_787_eis": eis[2], "af_a350_eis": eis[3]}
            o.update(over)
            return M.H.af(o, M.AF_PATCH)[3]
        M.af_board = af_board

    def __exit__(self, *a):
        M.af_board = self.saved


def tc(nom, pv):
    return M.true_cost(nom, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"])


def start(n):
    return json.load(open(os.path.join(REC, "state_r%d.json" % (n - 1))))


def column_states(n, plan):
    st, year = start(n), YEARS[n]
    scen = B.rival_scenarios(st, "boeing", year)
    own = dict(B.own_options(st, "boeing", year))
    cov = B.sees_covert(st, "boeing", year)
    out = []
    for slab, so in scen:
        orders = {k: dict(v) for k, v in so.items()}
        orders["boeing"] = dict(orders.get("boeing", {}), **own[plan])
        s1, _ = R.adjudicate(st, year, orders)
        out.append((slab, s1, cov or slab.startswith("Risk case")))
    return out


def row(n, plan, var, base=True):
    """One plan's columns: value, discounted fps deliveries in the window (Q), the fps discount factor at entry into
    service, and Boeing's programme spend (nominal and PV) that the joint true cost is charged on."""
    cols = []
    for slab, s, c in column_states(n, plan):
        v = M.value(s, covert=c, series=True)
        Q = 0.0
        for r in v["_af_series"]["years"]:
            x = r["boeing"]
            if x["nb_in_window"]:
                q = x.get("nb_units_new", 0.0)
                if q and base:
                    assert abs(x["nb_price"] - PRICE0) < 1e-9 and abs(x["nb_margin"] - M0) < 1e-12, (r["year"], x["nb_price"], x["nb_margin"])
                Q += q * r["df_b"]
        eis, a, b, dt = M.af_inputs(s, c)
        cell = M.eval_cell(eis, a, b)
        t, strain = cell["b_tc_data"], -cell["b_strain"]
        br = v["boeing"]["bridge"]
        if base:    # the two-front strain is the bridge's own line (Boeing has no Delay Tactics adjustment)
            assert abs(br["two_front_strain"] + strain) < 1e-9, (plan, slab)
        if base:    # the joint true cost is the bridge's own investment and debt penalty lines
            assert not [d for d in s["dead"] if d["side"] == "boeing"] and abs((br["programme_investment"] + br["debt_penalty"]) + tc(t.get("nom_capex", 0.0), t.get("pv_capex", 0.0))) < 1e-6, (plan, slab)
        fps = s["prog"].get("fps")
        cols.append({"label": slab, "v": v["boeing"]["pv_delta"], "Q": Q, "nom": t.get("nom_capex", 0.0), "pv": t.get("pv_capex", 0.0), "strain": strain,
                     "df": (1.0 / (1 + P["WACC_B"]) ** (fps["eis"] - 2026)) if fps else None, "eis": fps["eis"] if fps else None})
    return {"plan": plan, "var": var, "cols": cols}


def rows(n, base=True):
    out = {"Do Nothing": row(n, DN, None, base), "Re-engine": row(n, RE, None, base)}
    for k, (plan, var) in SOLO.items():
        out[k] = row(n, plan, var, base)
    for k, (plan, var) in PAIRS.items():
        out[k] = row(n, plan, var, base)
    return out


def values(rw, m=M0, k=1.0):
    """Each column's value at fps margin m and with Boeing paying share k of its fps bill (exact)."""
    out = []
    for c in rw["cols"]:
        v = c["v"]
        if rw["var"]:
            d = (k - 1.0) * BILL0[rw["var"]]
            v += c["Q"] * PRICE0 * (m - M0) / 1000.0
            nom, pv = c["nom"] + d, c["pv"] + d * c["df"]
            v -= tc(nom, pv) - tc(c["nom"], c["pv"])
            if c["strain"]:     # the dashboard prices the strain at the PV factor of Boeing's whole spend
                v -= c["strain"] * (pv / nom) / (c["pv"] / c["nom"]) - c["strain"]
        out.append(v)
    return out


def decide(n, rws, m=M0, k=1.0, vals=None):
    """Boeing's decision at margin m and bill share k: the launched plan under each reading (None: no launch), the
    CEO's pick, the best plan and each plan's value against Do Nothing in the CEO's column."""
    w = CEO_W[n]
    cols = rws["Do Nothing"]["cols"]
    risk = next(i for i, c in enumerate(cols) if c["label"].startswith("Risk case"))
    V = vals or {name: values(rw, m, k) for name, rw in rws.items()}
    dn = V["Do Nothing"]
    item = lambda a, b: [x - y for x, y in zip(V[a], V[b])]
    E = lambda xs: sum(xs[i] * wt for i, wt in w.items())
    e = {name: E(item(name, "Do Nothing")) for name in V}
    passes = lambda it: E(it) > BUSINESS and min(it) >= DOWNSIDE
    rating = lambda name: V[name][risk] - dn[risk] >= BUFFER

    def board(plan):
        """The launched plan after the Board's review of `plan`, or None."""
        if plan not in WITHOUT_FPS:
            return None
        if not (passes(item(plan, WITHOUT_FPS[plan])) and rating(plan)):
            return None
        if plan in ALONE and not passes(item(plan, ALONE[plan])):      # the Re-engine beside it is vetoed
            plan = ALONE[plan]
            if not rating(plan):
                return None
        return plan

    elig = [p for p in e if not (p == "Re-engine" and e[p] <= EPS)]      # the CEO's lever rule for the Re-engine
    best = max(elig, key=e.get)
    cands = [p for p in elig if e[p] >= e[best] - EPS]
    pick = min(cands, key=lambda p: (SIZE[p], -e[p]))
    pick2 = pick
    while True:                       # the pick weighed again against each smaller plan: within $1B the smaller wins
        smaller = [p for p in elig if SIZE[p] < SIZE[pick2] and e[p] >= e[pick2] - EPS]
        if not smaller:
            break
        pick2 = min(smaller, key=lambda p: (SIZE[p], -e[p]))
    worst = {p: min(item(p, "Do Nothing")) for p in cands}
    pick3 = max(cands, key=lambda p: (round(worst[p], 9), -SIZE[p], e[p]))
    rule = board(pick)
    prem = rule
    if prem is None:
        ok = [p for p in WITHOUT_FPS if p in elig and e[p] >= e[best] - H8 and board(p)]
        prem = board(max(ok, key=lambda p: e[p])) if ok else None
    return {"rule": rule, "pairwise": board(pick2), "worst_first": board(pick3), "premium": prem,
            "pick": pick, "pick_pairwise": pick2, "pick_worst_first": pick3, "best": best, "e": e}


def first(f, lo, hi, steps=400, tol=1e-7):
    """Smallest x in [lo, hi] with f(x) true, scanning then bisecting; and whether f stays true on the scan above it."""
    if f(lo):
        return lo, True
    xs = [lo + (hi - lo) * i / steps for i in range(steps + 1)]
    hit = next((i for i, x in enumerate(xs) if f(x)), None)
    if hit is None:
        return None, True
    a, b = xs[hit - 1], xs[hit]
    while b - a > tol:
        c = (a + b) / 2
        a, b = (a, c) if f(c) else (c, b)
    stays = all(f(x) for x in xs[hit:])
    return b, stays


def solve(n, rws):
    out = {}
    for mode in MODES:
        launched = lambda m, k: decide(n, rws, m, k)[mode] is not None
        m, m_ok = first(lambda x: launched(x, 1.0), M0, 3.0)
        cut, c_ok = first(lambda s: launched(M0, max(1e-9, 1.0 - s)), 0.0, 1.0)     # s: the cut in Boeing's share of the bill
        fine = [first(lambda mm: launched(mm, max(1e-9, frac)), 0.0, 3.0) for frac in FINE]
        plans = [decide(n, rws, x + 1e-7, max(1e-9, frac))[mode] if x is not None else None for (x, _), frac in zip(fine, FINE)]
        # the largest share of the bill Boeing can pay and still launch at a 100% margin
        c100, _ = first(lambda s: launched(1.0, max(1e-9, 1.0 - s)), 0.0, 1.0)
        out[mode] = {"margin": m, "margin_monotone": m_ok, "cut": cut, "cut_monotone": c_ok,
                     "plan_at_margin": decide(n, rws, m + 1e-7, 1.0)[mode] if m is not None else None,
                     "plan_at_cut": decide(n, rws, M0, max(1e-9, 1.0 - cut - 1e-7))[mode] if cut is not None else None,
                     "frontier": {"fractions": FINE, "margin": [x for x, _ in fine], "monotone": [ok for _, ok in fine], "plan": plans},
                     "share_at_100": None if c100 is None else 1.0 - c100}
    base = decide(n, rws)
    out["base"] = {k: base[k] for k in ("pick", "pick_pairwise", "pick_worst_first", "best", "e") + MODES}
    # the range across the readings: the low and high ends, and the plan that launches at each
    lo_hi = {}
    for key in ("margin", "cut"):
        vals = [(out[md][key], md) for md in MODES]
        known = [(v, md) for v, md in vals if v is not None]
        lo_hi[key] = {"low": min(known)[0] if known else None, "low_mode": min(known)[1] if known else None,
                      "high": None if any(v is None for v, _ in vals) else max(vals)[0], "high_mode": None if any(v is None for v, _ in vals) else max(vals)[1]}
    out["range"] = lo_hi
    out["per_point"] = {name: sum(rw["cols"][i]["Q"] * PRICE0 / 1000.0 / 100.0 * wt for i, wt in CEO_W[n].items()) for name, rw in rws.items() if rw["var"]}
    return out


def others_out_of_contention(n):
    """The 737 Rate Increase plans never beat the best of Do Nothing and the Re-engine; the via-Embraer plans trail the
    Solo 10-year at Renton by more than $2B (so neither reaches the CEO's pick or the H8 premium)."""
    st, year = start(n), YEARS[n]
    own = dict(B.own_options(st, "boeing", year))
    w = CEO_W[n]
    val = lambda plan: [M.value(s, covert=c, series=False)["boeing"]["pv_delta"] for _, s, c in column_states(n, plan)]
    dn = val(DN)
    E = lambda plan: sum((val(plan)[i] - dn[i]) * wt for i, wt in w.items())
    e_re = E(RE)
    for plan in own:
        if "737 rate up" in plan and plan.startswith("fps: hold"):
            assert E(plan) <= max(0.0, e_re) + 1e-9, (n, plan)
    e10 = E(SOLO["10-year at Renton"][0])
    for p in own:
        if "Embraer" in p and "rate up" not in p and "Re-engine" not in p:
            assert E(p) < e10 - H8, (n, p)
    return True


def confirm(n, m=None, k=None):
    """Every competing row re-valued on a dashboard re-solved at margin m and/or bill share k, against the shortcut (the
    largest gap), the decision there, and Boeing's stress-case net debt on the launched plan."""
    over = {}
    if m is not None:
        over["af_m_fps"] = 100.0 * m
    if k is not None:
        over["af_cx_fps10"] = BILL0["10yr"] * k
        over["af_cx_fps7"] = BILL0["7yr"] * k
    base = rows(n)
    with board(**over):
        new = rows(n, base=False)
        dec = decide(n, new, vals={name: [c["v"] for c in rw["cols"]] for name, rw in new.items()})
        mets = []
        launched = [dec[md] for md in MODES if dec[md]]
        if launched:
            plan = (SOLO.get(launched[0]) or PAIRS[launched[0]])[0]
            for _, s, c in column_states(n, plan):
                v = M.value(s, covert=c, series=True)
                mt = B.plan_metrics("boeing", s, v, c)
                mets.append({"stress_ok": mt["stress_ok"], "stress_peak": mt["stress_peak"]})
    gap = 0.0
    for name in base:
        a = values(base[name], m if m is not None else M0, k if k is not None else 1.0)
        b = [c["v"] for c in new[name]["cols"]]
        gap = max(gap, max(abs(x - y) for x, y in zip(a, b)))
    return {"gap": gap, "decisions": {md: dec[md] for md in MODES}, "pick": dec["pick"], "metrics": mets}


def run(n, opts, do_confirm):
    with L.patched(options=opts):
        rws = rows(n)
        if opts is O:                      # the run's own world gives back the run's own brief, every plan and column
            rec = json.load(open(os.path.join(REC, "grids_r%d.json" % n)))["boeing"]
            g = {x["plan"]: [c[0] for c in x["cells"]] for x in rec["rows"]}
            for name, rw in rws.items():
                assert max(abs(c["v"] - x) for c, x in zip(rw["cols"], g[rw["plan"]])) < 1e-9, (n, name)
            others_out_of_contention(n)
        dn = values(rws["Do Nothing"])
        out = {"year": YEARS[n], "columns": [c["label"] for c in rws["Do Nothing"]["cols"]], "weights": CEO_W[n],
               "rows": {name: {"plan": rw["plan"], "var": rw["var"], "items": [a - b for a, b in zip(values(rw), dn)],
                               "eis": rw["cols"][0]["eis"]} for name, rw in rws.items()}}
        out.update(solve(n, rws))
        if do_confirm:
            ck = {}
            for end in ("low", "high"):
                m = out["range"]["margin"][end]
                if m is not None and m <= 1.0:
                    ck["margin_" + end] = confirm(n, m=m + 1e-6)
                c = out["range"]["cut"][end]
                if c is not None:
                    ck["cut_" + end] = confirm(n, k=1.0 - c - 1e-6)
            half = out["rule"]["frontier"]["margin"][FINE.index(0.5)]
            if half is not None and half <= 1.0:
                ck["half_rule"] = confirm(n, m=half + 1e-6, k=0.5)
            for key, c in ck.items():
                assert c["gap"] < 1e-5, (n, key, c)
                assert all(x["stress_ok"] for x in c["metrics"]), (n, key)
            out["confirm"] = ck
    return out


def show(r):
    y = r["year"]
    print("%d base: pick %s, best %s, e %s" % (y, r["base"]["pick"], r["base"]["best"], {k: round(v, 2) for k, v in r["base"]["e"].items()}))
    for mode in MODES:
        x = r[mode]
        fm = x["frontier"]["margin"]
        print("%d %-11s margin %s (%s%s) | cut %s (%s%s) | frontier 75/50/25/0: %s" % (
            y, mode, "-" if x["margin"] is None else "%.2f%%" % (100 * x["margin"]), x["plan_at_margin"], "" if x["margin_monotone"] else ", NOT MONOTONE",
            "-" if x["cut"] is None else "%.1f%%" % (100 * x["cut"]), x["plan_at_cut"], "" if x["cut_monotone"] else ", NOT MONOTONE",
            [None if fm[FINE.index(f)] is None else round(100 * fm[FINE.index(f)], 1) for f in (0.75, 0.5, 0.25, 0.0)]))


def main(do_confirm=True):
    res = {"base": {"margin": M0, "price_musd": PRICE0, "bill": BILL0}, "eps": EPS, "h8": H8,
           "tests": {"business_case": BUSINESS, "downside": DOWNSIDE, "buffer": BUFFER}, "rounds": {}, "game_tail": {}}
    for n in YEARS:
        r = run(n, O, do_confirm)
        res["rounds"][str(n)] = r
        show(r)
        if "confirm" in r:
            print("   confirmed", {k: (round(v["gap"], 8), v["decisions"]) for k, v in r["confirm"].items()})
    for n in (3, 4):
        r = run(n, GAME_TAIL, False)
        res["game_tail"][str(n)] = r
        print("conservative tail:", end=" ")
        show(r)
    json.dump(res, open(os.path.join(HERE, "data", "thresholds.json"), "w"), indent=1)
    print("wrote data/thresholds.json")


if __name__ == "__main__":
    main(do_confirm=sys.argv[1:] != ["fast"])
