"""Politics, brand and rivals in Boeing's fps decision (MAX phase-out game): the weight of Washington and jobs, Boeing's
identity as an engineering company, and leaving the narrowbody market to Airbus and COMAC, put into Boeing's decision
rule alongside the brief and the franchise terms (franchise.py). The evidence is in data/politics_research.json (six
research sweeps on Boeing's past behaviour, a model design and two adversarial checks).

Two blocks, kept apart:
  cash-like terms, sized from what governments and Boeing have actually done
    government co-funding  - state siting incentives and federal technology money, as a cut in Boeing's share of the fps
                             bill (k = 1 - c in the game's own valuation, so the bill's debt penalty falls with it).
                             US precedent: no direct federal launch funding for an airliner since the SST (cancelled
                             1971); federal help has come as research money (the WTO found NASA and DoD R&D helped the
                             787) and demonstrators (NASA's X-66, $425M, paused 2025); state packages (Washington 2003 and
                             2013, South Carolina 2009) are worth about $1-3B in present value; and Boeing backed "market
                             terms" for all future support in 2021. Base 2% of the bill (0 / 5%).
    political cost of exit - a probability that Washington makes Boeing pay for leaving (defence, export finance, the
                             FAA), times defence profit at risk, for 20 years from 2045, when the MAX phase-out starts
                             (the last MAX is built in 2060), or from the decision year if later. Charged to the plans
                             without an fps in every round, as the brief's Do Nothing never launches (only 2050 is a real
                             exit). It is goodwill, so the cash-rating reading keeps it out of the rating test; as played
                             it is in it. Base p 0.2 x $0.44B a year (0 / 0.5 x $0.66B from 2040).
  a subjective strategic premium S
    the weight Boeing would put on staying in (identity, engineering, standing as the last US airliner maker), added
    to every fps plan in every column; found as the smallest S at which each reading of the CEO's rule launches an fps.

Three ways of applying the rule (thresholds.decide):
  as played    - S counts in every test, as the game's rule is written (premium.py gives the same numbers).
  cash rating  - the Board's rating test (the risk-case column within $2B of Do Nothing) reads cash only (the brief,
                 the franchise terms and co-funding): a brand or political weight does not make spend affordable.
  anticipating - the CEO picks among the outcomes the Board would approve (the Board's tests apply to the 787
                 Re-engine alone too, as it vetoed it in the game's 2030 round), rather than proposing and being vetoed.
S is reported in money of 2026 and of the decision year (today's value carried forward at the rate to the year of the
decision). A sensitivity states the Board's three dollar tests ($1B business case, -$1B downside, -$2B rating buffer) in
decision-year money instead of 2026 money; the CEO's $1B margin and $2B allowance stay as the game has them.

Scenario: COMAC takes all of China's single-aisle demand by 2050 (Boeing's own China outlook: about 360 a year), its
200-a-year target reached in 2032 rather than 2029; COMAC still sells only its own capacity, off the top, so it gains
none of the share Boeing gives up. The political cost of exit is raised (p 0.5, an assumption). The market changes, so
the brief and franchise terms are re-run in that world.

  python3 politics.py           writes data/politics.json
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import franchise as F  # noqa: E402
import thresholds as T  # noqa: E402

M0 = F.M0
RATES = F.RATES
FPS = list(T.SOLO) + list(T.PAIRS)
NON_FPS = ("Do Nothing", "Re-engine")
CASH = {"c_gov": {"low": 0.0, "base": 0.02, "high": 0.05},
        "exit_p": {"low": 0.0, "base": 0.2, "high": 0.5},
        "exit_L": {"low": 0.0, "base": 0.44, "high": 0.66},          # $B a year of defence profit at risk
        "exit_from": {"low": 2045, "base": 2045, "high": 2040}}
COMAC_PLAN = {"2026": 28, "2030": 120, "2032": 200, "2040": 280, "2045": 330, "2050": 360}


def annuity(r, years):
    return sum((1 + r) ** -t for t in range(years))


def exit_cost(level, r, year):
    """PV-2026 of the political cost of leaving: p x L a year for 20 years from max(start of the MAX phase-out, decision year)."""
    p, L, t0 = CASH["exit_p"][level], CASH["exit_L"][level], max(CASH["exit_from"][level], year)
    return p * L * annuity(r, 20) * (1 + r) ** -(t0 - 2026)


def decide2(n, V, RV=None, anticipate=False, scale=1.0):
    """thresholds.decide with three options: the rating test on separate values RV (cash only), the CEO picking among
    the outcomes the Board approves, and the Board's dollar tests scaled (decision-year money: scale = df of the
    year). With RV = V, anticipate False and scale 1 it is thresholds.decide (asserted below)."""
    RV = RV or V
    w = T.CEO_W[n]
    cols = FL[n]["Do Nothing"]
    risk = next(i for i, f in enumerate(cols) if f["label"].startswith("Risk case"))
    EPS, H8 = T.EPS, T.H8                                   # the CEO's margin and allowance stay as the game has them
    BUS, DOWN, BUF = (x * scale for x in (T.BUSINESS, T.DOWNSIDE, T.BUFFER))
    item = lambda a, b: [x - y for x, y in zip(V[a], V[b])]
    E = lambda xs: sum(xs[i] * wt for i, wt in w.items())
    e = {name: E(item(name, "Do Nothing")) for name in V}
    passes = lambda it: E(it) > BUS and min(it) >= DOWN
    rating = lambda name: RV[name][risk] - RV["Do Nothing"][risk] >= BUF

    def board(plan):
        if plan not in T.WITHOUT_FPS:
            return None
        if not (passes(item(plan, T.WITHOUT_FPS[plan])) and rating(plan)):
            return None
        if plan in T.ALONE and not passes(item(plan, T.ALONE[plan])):
            plan = T.ALONE[plan]
            if not rating(plan):
                return None
        return plan

    elig = [p for p in e if not (p == "Re-engine" and e[p] <= EPS)]
    if anticipate:
        out = {"Do Nothing"}
        for p in elig:
            if p == "Re-engine":
                if passes(item(p, "Do Nothing")) and rating(p):
                    out.add(p)
            elif p != "Do Nothing":
                q = board(p)
                if q:
                    out.add(q)
        best = max(out, key=e.get)
        pick = min([p for p in out if e[p] >= e[best] - EPS], key=lambda p: (T.SIZE[p], -e[p]))
        res = pick if pick in T.WITHOUT_FPS else None
        return {md: res for md in T.MODES} | {"pick": pick, "e": e}
    best = max(elig, key=e.get)
    cands = [p for p in elig if e[p] >= e[best] - EPS]
    pick = min(cands, key=lambda p: (T.SIZE[p], -e[p]))
    pick2 = pick
    while True:
        smaller = [p for p in elig if T.SIZE[p] < T.SIZE[pick2] and e[p] >= e[pick2] - EPS]
        if not smaller:
            break
        pick2 = min(smaller, key=lambda p: (T.SIZE[p], -e[p]))
    worst = {p: min(item(p, "Do Nothing")) for p in cands}
    pick3 = max(cands, key=lambda p: (round(worst[p], 9), -T.SIZE[p], e[p]))
    rule = board(pick)
    prem = rule
    if prem is None:
        ok = [p for p in T.WITHOUT_FPS if p in elig and e[p] >= e[best] - H8 and board(p)]
        prem = board(max(ok, key=lambda p: e[p])) if ok else None
    return {"rule": rule, "pairwise": board(pick2), "worst_first": board(pick3), "premium": prem, "pick": pick, "e": e}


FL, HOR, TT, _CACHE = {}, {}, {}, {}


def load_round(n, world="base"):
    if world == "base":
        fl, horizon = F.round_flows(n)                   # asserts the brief, every plan and column, to the cent
    else:                                                 # another world: the same flows, no brief to check against
        st = T.start(n)
        ncol = len(F.B.rival_scenarios(st, "boeing", T.YEARS[n]))
        probe = {name: F.flows(n, name, 0, None) for name in F.ROWS}
        eis_max = max((f["fps_eis"] for f in probe.values() if f["fps_eis"]), default=T.YEARS[n] + 10)
        horizon = eis_max + F.LIFE - 1
        fl = {name: [F.flows(n, name, j, horizon) for j in range(ncol)] for name in F.ROWS}
    FL[n], HOR[n] = fl, horizon
    for k in [k for k in _CACHE if k[0] == n]:
        del _CACHE[k]
    TT[n] = {(lv, rn): F.term_table(fl, horizon, r, F.prm_set(lv)) for lv in ("low", "base", "high") for rn, r in RATES.items()}


def values(n, level, rname, view, c_gov=0.0, S=0.0, X=0.0):
    """(full values, cash values): the brief and the view's terms with co-funding c_gov; S on every fps plan and the
    exit cost X on the plans without an fps in the full values only."""
    key = (n, level, rname, view, round(c_gov, 12))
    if key not in _CACHE:
        _CACHE[key] = F.values_at(FL[n], TT[n][(level, rname)], RATES[rname], M0, 1.0 - c_gov, F.SCENARIOS[view])
    cash = _CACHE[key]
    full = {name: [v + (S if name in FPS else 0.0) - (X if name in NON_FPS else 0.0) for v in vs] for name, vs in cash.items()}
    return full, cash


READINGS = ("as played", "cash rating", "anticipating")


def launches(n, level, rname, view, c_gov, S, X, reading, md, scale=1.0):
    full, cash = values(n, level, rname, view, c_gov, S, X)
    d = decide2(n, full, cash if reading == "cash rating" else None, anticipate=(reading == "anticipating"), scale=scale)
    return d[md]


def s_needed(n, level, rname, view, cash_level, reading, md, scale=1.0):
    c = CASH["c_gov"][cash_level]
    X = exit_cost(cash_level, RATES[rname], T.YEARS[n])
    f = lambda s: launches(n, level, rname, view, c, s, X, reading, md, scale) is not None
    if not f(60.0):
        return None, None
    s, _ = T.first(f, 0.0, 60.0, steps=240, tol=1e-5)
    full, cash = values(n, level, rname, view, c, s + 1e-5, X)
    d = decide2(n, full, cash if reading == "cash rating" else None, anticipate=(reading == "anticipating"), scale=scale)
    return s, d[md]


def cut_needed(n, level, rname, view, cash_level, S=0.0):
    """Share of the fps bill a government would have to carry (with the political cost of exit on and premium S) for
    each reading of the rule, as played, to launch."""
    X = exit_cost(cash_level, RATES[rname], T.YEARS[n])
    out = {}
    for md in T.MODES:
        f = lambda c: launches(n, level, rname, view, c, S, X, "as played", md) is not None
        out[md], _ = T.first(f, 0.0, 0.999, steps=200, tol=1e-6)
    return out


def run_world(world):
    out = {}
    for n in T.YEARS:
        if world != "base" and n not in (1, 2):
            continue
        load_round(n, world)
        year = T.YEARS[n]
        rr = {"year": year, "cases": {}, "items": {}}
        for rname, r in RATES.items():
            dfy = (1 + r) ** -(year - 2026)
            # the plans against Do Nothing in the CEO's columns, brief and full view, base
            for view in ("game", "full"):
                full, cash = values(n, "base", rname, view)
                w = T.CEO_W[n]
                rr["items"]["%s|%s" % (view, rname)] = {name: sum((cash[name][i] - cash["Do Nothing"][i]) * wt for i, wt in w.items()) for name in cash}
            for level, view, cash_level in (("base", "game", "low"), ("base", "full", "low"), ("base", "full", "base"),
                                            ("high", "full", "high"), ("low", "full", "low")):
                key = "%s|%s|cash %s|%s" % (level, view, cash_level, rname)
                case = {"exit_cost_pv": exit_cost(cash_level, r, year), "c_gov": CASH["c_gov"][cash_level], "readings": {}}
                for reading in READINGS:
                    mds = T.MODES if reading != "anticipating" else ("rule",)
                    case["readings"][reading] = {}
                    for md in mds:
                        s, plan = s_needed(n, level, rname, view, cash_level, reading, md)
                        case["readings"][reading][md] = {"S": s, "S_decision_year": None if s is None else s / dfy, "plan": plan}
                if level == "base" and view == "full" and cash_level == "base":
                    s, plan = s_needed(n, level, rname, view, cash_level, "as played", "rule", scale=dfy)
                    case["deflated_tests"] = {"S": s, "S_decision_year": None if s is None else s / dfy, "plan": plan}
                    case["cut_needed_by_reading"] = cut_needed(n, level, rname, view, cash_level)
                    cs = [c for c in case["cut_needed_by_reading"].values() if c is not None]
                    case["cut_needed"] = [min(cs), max(cs)] if len(cs) == len(T.MODES) else None
                rr["cases"][key] = case
                print(world, n, key, {rd: {md: (None if v["S"] is None else round(v["S"], 2), v["plan"]) for md, v in case["readings"][rd].items()} for rd in READINGS},
                      "cut", case.get("cut_needed"), flush=True)
        out[str(n)] = rr
    return out


def main():
    # decide2 is thresholds.decide when the options are off: every stored decision in franchise.json, every case
    FRJ = json.load(open(os.path.join(HERE, "data", "franchise.json")))
    checked = 0
    for n in T.YEARS:
        FL[n] = {"Do Nothing": [{"label": c} for c in FRJ["rounds"][str(n)]["columns"]]}
        for key, t in FRJ["rounds"][str(n)]["thresholds"].items():
            for at, p in t["points"].items():
                d = decide2(n, p["values"])
                assert all(d[md] == p["decision"][md] for md in T.MODES) and d["pick"] == p["decision"]["pick"], (n, key, at)
                checked += 1
    print("decide2 reproduces", checked, "stored decision points")
    # and random values, which reach the veto branches the stored points do not (downside, rating, the solo's rating
    # after the Re-engine beside it is vetoed); with RV = V the cash-rating option changes nothing
    rnd = random.Random(0)
    hits = {"downside": 0, "rating": 0, "solo rating": 0}
    for n in T.YEARS:
        cols = FL[n]["Do Nothing"]
        risk = next(i for i, c in enumerate(cols) if c["label"].startswith("Risk case"))
        rws = {"Do Nothing": {"cols": cols}}
        for _ in range(3000):
            base = rnd.uniform(-8, 8)
            V = {nm: [base + rnd.uniform(-4, 4) for _ in cols] for nm in FPS + list(NON_FPS)}
            V["Do Nothing"] = [0.0] * len(cols)
            a, b2 = decide2(n, V), T.decide(n, rws, vals=V)
            assert all(a[md] == b2[md] for md in T.MODES) and a["pick"] == b2["pick"]
            c = decide2(n, V, RV=V)
            assert all(c[md] == a[md] for md in T.MODES)
            for p in FPS:
                it = [x - y for x, y in zip(V[p], V[T.WITHOUT_FPS[p]])]
                if min(it) < T.DOWNSIDE:
                    hits["downside"] += 1
                if V[p][risk] < T.BUFFER:
                    hits["rating"] += 1
                if p in T.ALONE and V[T.ALONE[p]][risk] < T.BUFFER:
                    hits["solo rating"] += 1
    assert all(v > 1000 for v in hits.values()), hits
    print("decide2 equals thresholds.decide on 12,000 random cases; veto branches reached", hits)
    res = {"cash": CASH, "readings": READINGS, "comac_plan": COMAC_PLAN, "decide2_checked": checked, "worlds": {}}
    res["worlds"]["base"] = run_world("base")
    # COMAC on its own plan: the market changes, so the brief is re-run in that world (rounds 2030 and 2035)
    opts = json.loads(json.dumps(T.O))
    opts["third_party"]["comac"] = COMAC_PLAN
    saved = T.O
    T.O = opts
    F.tail_curve.cache_clear()
    try:
        CASH_SAVED = json.loads(json.dumps(CASH))
        CASH["exit_p"]["base"] = 0.5                       # leaving the market to COMAC raises the political stakes
        res["worlds"]["comac takes china"] = run_world("comac")
    finally:
        T.O = saved
        CASH.clear()
        CASH.update(CASH_SAVED)
    json.dump(res, open(os.path.join(HERE, "data", "politics.json"), "w"), indent=1)
    print("wrote data/politics.json")


if __name__ == "__main__":
    main()
