"""What fps margin and/or Boeing investment would have changed Boeing's decision in the MAX phase-out game.

For each round (2030, 2035, 2045, 2050), from the state the round started in (record/state_r{n-1}.json), with the
run's own world (sd_options_phaseout.json), each Solo fps plan is valued exactly as Boeing's brief valued it: the plan
against Do Nothing in every rival column. It is then held to the Board's three value tests, the same in every round's
guidance (record/exco_result_rN.json, board_guidance):
  business case - more than +$1B in the expected column (the CEO's own weighting of Airbus's options that round);
  downside      - no worse than -$1B in any column (the Board treats every column as plausible in every round);
  rating first  - the plan's risk-case column no more than $2B below Do Nothing's (item >= -$2B there).
The CEO's own rule (lead Do Nothing by more than the $1B margin in the expected column) is the business-case test.

Levers, each alone and together:
  margin     - the fps operating margin on every fps delivered (price held at $55M): exact, because each column's value
               moves by its discounted fps deliveries x price x the margin change;
  investment - Boeing's fps bill (10-year $60.32B, 7-year $65.0B), booked as a lump at entry into service with the
               dashboard's debt penalty, as the brief books it: exact, the bill and penalty lines are the dashboard's own
               formula (checked column by column).
Every threshold of the best plan in each round is re-checked on a re-solved dashboard (margin, investment and the
combined frontier's 50% point), with Boeing's stress-case net debt at that point. Also: 2045 and 2050 again with the
conservative demand curve after 2060 (data/curves/page_n0_game2061.json, tail.py). Writes data/thresholds.json.

  python3 thresholds.py            (about 30 minutes: the re-checks re-solve the dashboard)
  python3 thresholds.py frontier   (only the fine frontier, from data/thresholds.json)
  python3 thresholds.py confirm10  (only the 10-year at Renton's re-checks)
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
CX_KEY = {"10yr": "af_cx_fps10", "7yr": "af_cx_fps7"}
O = {k: v for k, v in json.load(open(os.path.join(HERE, "..", "..", "dashgame", "sd_options_phaseout.json"))).items() if not k.startswith("_")}
GAME_TAIL = dict(O, demand_curve=os.path.abspath(os.path.join(HERE, "data", "curves", "page_n0_game2061.json")))
REC = os.path.join(HERE, "record")
YEARS = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
CEO_W = {1: {1: 2 / 3, 4: 1 / 3}, 2: {0: 0.7, 2: 0.3}, 3: {0: 0.8, 1: 0.2}, 4: {0: 0.8, 1: 0.2}}
BUSINESS, DOWNSIDE, BUFFER = 1.0, -1.0, -2.0
DN = "fps: hold + 787: hold"
PLANS = {"10-year at Renton": ("fps 10-yr at Renton + 787: hold", "10yr"), "10-year, new sites": ("fps 10-yr + 787: hold", "10yr"),
         "7-year at Renton": ("fps 7-yr at Renton + 787: hold", "7yr"), "7-year, new sites": ("fps 7-yr + 787: hold", "7yr")}
FRACTIONS = (1.0, 0.75, 0.5, 0.25, 0.0)


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


def pen_pv(bill, df):
    pv = bill * df
    return M.true_cost(bill, pv, P["v_debt_boeing"], P["v_ev_boeing"], P["v_alpha"]) - pv


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


def grid(n, plans, check=True):
    """Items (plan minus Do Nothing) per column, with each column's fps terms: Q (discounted fps deliveries in the
    window), df (discount factor at entry into service), and the fps entry into service."""
    dn = [M.value(s, covert=c, series=False)["boeing"]["pv_delta"] for _, s, c in column_states(n, DN)]
    res = {}
    for name in plans:
        plan, var = PLANS[name]
        items, terms, labels = [], [], []
        for (slab, s, c), d in zip(column_states(n, plan), dn):
            v = M.value(s, covert=c, series=True)
            Q = 0.0
            for r in v["_af_series"]["years"]:
                x = r["boeing"]
                if x["nb_in_window"]:
                    q = x.get("nb_units_new", 0.0)
                    if q and check:
                        assert abs(x["nb_price"] - PRICE0) < 1e-9 and abs(x["nb_margin"] - M0) < 1e-12, (r["year"], x["nb_price"], x["nb_margin"])
                    Q += q * r["df_b"]
            eis = s["prog"]["fps"]["eis"]
            df = 1.0 / (1 + P["WACC_B"]) ** (eis - 2026)
            br = v["boeing"]["bridge"]
            if check:
                assert abs(br["programme_investment"] + BILL0[var] * df) < 1e-6, (br["programme_investment"], BILL0[var] * df)
                assert abs(br["debt_penalty"] + pen_pv(BILL0[var], df)) < 1e-6, (br["debt_penalty"], pen_pv(BILL0[var], df))
            items.append(v["boeing"]["pv_delta"] - d)
            terms.append({"Q": Q, "df": df, "eis": eis})
            labels.append(slab)
        res[name] = {"items": items, "terms": terms, "columns": labels, "dn": dn, "var": var}
    return res


def shifted(g, margin=M0, bill=None):
    b0 = BILL0[g["var"]]
    bill = b0 if bill is None else bill
    out = []
    for it, t in zip(g["items"], g["terms"]):
        dv = t["Q"] * PRICE0 * (margin - M0) / 1000.0
        dv -= (bill - b0) * t["df"] + (pen_pv(bill, t["df"]) - pen_pv(b0, t["df"]))
        out.append(it + dv)
    return out


def tests(n, items, columns):
    risk = next(i for i, s in enumerate(columns) if s.startswith("Risk case"))
    e = sum(items[i] * w for i, w in CEO_W[n].items())
    parts = {"business case": e - BUSINESS, "downside": min(items) - DOWNSIDE, "rating first": items[risk] - BUFFER}
    return {"expected": e, "worst": min(items), "risk_case": items[risk], "slack": min(parts.values()),
            "binding": min(parts, key=parts.get), "passes": e > BUSINESS and min(items) >= DOWNSIDE and items[risk] >= BUFFER}


def solve(n, g):
    f = lambda **kw: tests(n, shifted(g, **kw), g["columns"])["slack"]
    m = L.bisect(lambda x: f(margin=x), M0, 3.0, 0.0, tol=1e-7)
    b0 = BILL0[g["var"]]
    bl = L.bisect(lambda x: f(bill=x), b0, 0.0, 0.0, tol=1e-6) if f(bill=1e-9) >= 0 else None
    front = {}
    for k in FRACTIONS:
        x = b0 * k if k > 0 else 1e-9
        front[str(k)] = L.bisect(lambda mm: f(margin=mm, bill=x), 0.0, 3.0, 0.0, tol=1e-7)
    base = tests(n, g["items"], g["columns"])
    return {"base": base, "margin": m, "bill": bl, "at_zero_bill": tests(n, shifted(g, bill=1e-9), g["columns"]),
            "frontier": front, "per_point": sum(t["Q"] * PRICE0 / 1000.0 / 100.0 * CEO_W[n].get(i, 0.0) for i, t in enumerate(g["terms"])),
            "per_10b": None, "eis": g["terms"][0]["eis"], "Q_expected": sum(t["Q"] * CEO_W[n].get(i, 0.0) for i, t in enumerate(g["terms"])),
            "margin_tests": tests(n, shifted(g, margin=m), g["columns"]) if m else None,
            "bill_tests": tests(n, shifted(g, bill=bl), g["columns"]) if bl is not None else None}


def confirm(n, name, margin=None, bill=None):
    """Boeing's test slack for one plan on a dashboard re-solved at the given margin and/or bill (0 at a pass line), and
    the stress-case net debt there."""
    var = PLANS[name][1]
    over = {}
    if margin is not None:
        over["af_m_fps"] = 100.0 * margin
    if bill is not None:
        over[CX_KEY[var]] = bill
    with board(**over):
        g = grid(n, [name], check=False)[name]
        st = column_states(n, PLANS[name][0])
        mets = []
        for _, s, c in st:
            v = M.value(s, covert=c, series=True)
            m = B.plan_metrics("boeing", s, v, c)
            mets.append({"stress_ok": m["stress_ok"], "stress_peak": m["stress_peak"]})
    return tests(n, g["items"], g["columns"])["slack"], mets


def run(n, opts, do_confirm):
    with L.patched(options=opts):
        g = grid(n, list(PLANS))
        if opts is O:                      # the run's own world gives back the run's own brief, every plan and column
            rec = json.load(open(os.path.join(REC, "grids_r%d.json" % n)))["boeing"]
            rows = {x["plan"]: [c[0] for c in x["cells"]] for x in rec["rows"]}
            for name, (plan, _) in PLANS.items():
                want = [a - b for a, b in zip(rows[plan], rows[DN])]
                assert max(abs(a - b) for a, b in zip(want, g[name]["items"])) < 1e-9, (n, name)
        out = {"year": YEARS[n], "columns": g[next(iter(PLANS))]["columns"], "weights": CEO_W[n], "plans": {}}
        for name in PLANS:
            out["plans"][name] = dict(solve(n, g[name]), items=g[name]["items"], terms=g[name]["terms"])
        # the plan that needs the least margin (and, separately, the least investment cut)
        ms = {k: v["margin"] for k, v in out["plans"].items() if v["margin"] is not None}
        out["best_margin_plan"] = min(ms, key=ms.get) if ms else max(out["plans"], key=lambda k: out["plans"][k]["at_zero_bill"]["slack"])
        bs = {k: v["bill"] / BILL0[PLANS[k][1]] for k, v in out["plans"].items() if v["bill"] is not None}
        out["best_bill_plan"] = max(bs, key=bs.get) if bs else None
        if do_confirm:
            name = out["best_margin_plan"]
            p = out["plans"][name]
            ck = {}
            if p["margin"] is not None:
                ck["margin"] = confirm(n, name, margin=p["margin"])
            if p["bill"] is not None:
                ck["bill"] = confirm(n, name, bill=p["bill"])
            if p["frontier"]["0.5"] is not None:
                ck["half_bill"] = confirm(n, name, margin=p["frontier"]["0.5"], bill=BILL0[PLANS[name][1]] * 0.5)
            for k, (slack, mets) in ck.items():
                assert abs(slack) < 1e-4, (n, name, k, slack)
            out["confirm"] = {k: {"slack": s, "metrics": m} for k, (s, m) in ck.items()}
    return out


def main():
    res = {"base": {"margin": M0, "price_musd": PRICE0, "bill": BILL0}, "tests": {"business_case": BUSINESS, "downside": DOWNSIDE, "buffer": BUFFER},
           "rounds": {}, "game_tail": {}}
    for n in YEARS:
        r = run(n, O, do_confirm=True)
        res["rounds"][str(n)] = r
        for name, p in r["plans"].items():
            print("%d %-20s base exp %+6.2f worst %+6.2f | margin %s | bill %s | at zero bill slack %+.2f | frontier %s" % (
                YEARS[n], name, p["base"]["expected"], p["base"]["worst"],
                "-" if p["margin"] is None else "%.1f%%" % (100 * p["margin"]), "-" if p["bill"] is None else "%.1f" % p["bill"],
                p["at_zero_bill"]["slack"], {k: (None if v is None else round(100 * v, 1)) for k, v in p["frontier"].items()}))
        print("   confirmed", {k: round(v["slack"], 6) for k, v in r.get("confirm", {}).items()})
    for n in (3, 4):
        r = run(n, GAME_TAIL, do_confirm=False)
        res["game_tail"][str(n)] = r
        p = r["plans"][r["best_margin_plan"]]
        print("%d conservative tail: %s margin %s bill %s frontier %s" % (YEARS[n], r["best_margin_plan"], p["margin"],
              p["bill"], {k: (None if v is None else round(100 * v, 1)) for k, v in p["frontier"].items()}))
    json.dump(res, open(os.path.join(HERE, "data", "thresholds.json"), "w"), indent=1)
    print("wrote data/thresholds.json")


FINE = [k / 20 for k in range(21)]          # Boeing's investment, 0% to 100% of today's bill in 5% steps


def add_fine_frontier():
    """From data/thresholds.json alone (no re-solve): the margin needed at every 5% of today's bill, for every plan,
    round and tail, with the same exact shortcut (the stored items and per-column terms)."""
    path = os.path.join(HERE, "data", "thresholds.json")
    res = json.load(open(path))
    for key in ("rounds", "game_tail"):
        for n, r in res[key].items():
            for name, p in r["plans"].items():
                g = {"items": p["items"], "terms": p["terms"], "var": PLANS[name][1], "columns": r["columns"]}
                f = lambda **kw: tests(int(n), shifted(g, **kw), g["columns"])["slack"]
                b0 = BILL0[g["var"]]
                fine = []
                for k in FINE:
                    x = b0 * k if k > 0 else 1e-9
                    fine.append(L.bisect(lambda mm: f(margin=mm, bill=x), 0.0, 3.0, 0.0, tol=1e-7))
                for k in FRACTIONS:                 # agrees with the coarse frontier
                    a, c = fine[FINE.index(k)], p["frontier"][str(k)]
                    assert (a is None and c is None) or abs(a - c) < 1e-6, (key, n, name, k, a, c)
                p["fine_frontier"] = {"fractions": FINE, "margin": fine}
    json.dump(res, open(path, "w"), indent=1)
    print("added fine frontiers to data/thresholds.json")


def confirm_ten():
    """Re-check the 10-year at Renton's margin and investment thresholds (2030-45, where they exist) on a re-solved
    dashboard, with the stress-case net debt there, and store them under confirm_10yr in data/thresholds.json."""
    path = os.path.join(HERE, "data", "thresholds.json")
    res = json.load(open(path))
    name = "10-year at Renton"
    with L.patched(options=O):
        for n in (1, 2, 3):
            p = res["rounds"][str(n)]["plans"][name]
            ck = {}
            if p["margin"] is not None and p["margin"] <= 1.0:
                ck["margin"] = confirm(n, name, margin=p["margin"])
            if p["bill"] is not None:
                ck["bill"] = confirm(n, name, bill=p["bill"])
            for k, (slack, mets) in ck.items():
                assert abs(slack) < 1e-4, (n, k, slack)
                print(YEARS[n], name, k, "slack %.2e" % slack, "stress ok" if all(m["stress_ok"] for m in mets) else "STRESS FAILS")
            res["rounds"][str(n)]["confirm_10yr"] = {k: {"slack": sl, "metrics": m} for k, (sl, m) in ck.items()}
    json.dump(res, open(path, "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1:] == ["frontier"]:
        add_fine_frontier()
    elif sys.argv[1:] == ["confirm10"]:
        confirm_ten()
    else:
        main()
        add_fine_frontier()
        confirm_ten()
