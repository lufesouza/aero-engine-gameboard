"""Embraer, with a South Korean partner, as a third single-aisle maker in the MAX phase-out game, and partners who could
carry part of Boeing's fps bill. The evidence is in data/embraer_research.json (five web research tracks, each checked
by an adversarial verifier).

Part 1, the competitor. The game already has an "Embraer-like" new entrant (in service 2040, 20 a month by 2046) that
sells only to customers Boeing and Airbus cannot serve. Here it becomes a real competitor, in two ways:
  share   - it wins a share of each year's new customers (after COMAC's home market), up to its capacity: a larger share
            in the years Boeing has no new narrowbody in service (customers who want a second source to Airbus), a
            smaller one once an fps is in service. This is the engine's own third-party rule (supply_demand.py,
            entrant_share and entrant_share_no_fps), so every plan in every column is re-delivered in that world.
  price   - its campaigns cut the price of every new single-aisle delivered, Boeing's and Airbus's alike, from a few
            years before its entry into service, rising to the full cut over the ramp years. Costs do not change, so
            Boeing's profit falls by the cut times the price on every MAX and fps it delivers, and the status quo (which
            runs the same rules) falls too: only the difference enters a plan's value. The same rule is in the engine
            (supply_demand.py, price_pressure) for the game's re-run; here it is applied to the flows, and a check
            asserts the two give the same value.
Deterred: Embraer launches only if Boeing has not launched an fps by its own launch decision (2030 round only): the
fps plans are valued in the game's own world against the status quo with Embraer, Do Nothing and the Re-engine alone in
the Embraer world.

Part 2, a partner for the bill. A partner (a risk-sharing supplier or a state-backed investor) pays share p of the fps
bill, spent evenly over the development years, and takes back share s of the fps's operating profit (after any price
cut) for as long as the view counts the fps: the counted window in the brief, the fps's 50 years in the franchise view.
s is set where the partner breaks even at its own rate in the CEO's expected columns, so the partner bears the column
risk. Boeing gets the game's own saving on the bill (with the debt penalty, as k = 1 - p) and gives up s of the fps
profit. A partner whose rate equals Boeing's leaves Boeing only the debt-penalty saving; one with a lower rate (state
loans, export credit, a government that values the work) values the fps's late profits more than Boeing does, which is
the only way a partner closes a bill the numbers do not.

Rates: the game's 10.5% on constant-2026 flows, with partner rates applied as stated; and 8.1% (10.5% read as
nominal), with partner rates deflated the same way.

  python3 embraer.py            writes data/embraer.json
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-cons", "analysis"))
import franchise as F  # noqa: E402
import politics as PO  # noqa: E402
import thresholds as T  # noqa: E402

M, SD, P = F.M, F.SD, F.P
M0, PRICE, PRICE_737, MAX_UNIT = F.M0, F.PRICE, P["PRICE_737"], F.MAX_UNIT
RATES = F.RATES
INFL = 0.022
FPS = list(T.SOLO) + list(T.PAIRS)
DEV = {"10yr": 10, "7yr": 7}
VAR = {**{k: v[1] for k, v in T.SOLO.items()}, **{k: v[1] for k, v in T.PAIRS.items()}}

# ─────────────────────────────── Embraer-Korea (low / base / high threat to Boeing) ───────────────────────────────
EMB = {
    "eis": {"low": 2044, "base": 2040, "high": 2037},             # the verifier's correction: no earlier than NGSA (2037)
    "peak_a_month": {"low": 4.0, "base": 8.0, "high": 14.0},       # Embraer's best was 101-108 E-Jets a year
    "years_to_peak": {"low": 12, "base": 8, "high": 5},
    "share_fps": {"low": 0.02, "base": 0.06, "high": 0.10},        # of new customers, once an fps is in service
    "share_no_fps": {"low": 0.05, "base": 0.09, "high": 0.18},     # while Boeing has no new narrowbody in service
    "cut": {"low": 0.02, "base": 0.05, "high": 0.10},              # market-average share of the price, at full effect
    "lead": {"low": -1, "base": 1, "high": 3},                     # deliveries feel it this many years before Embraer's
                                                                   # EIS (deals about 4 years before, deliveries ~3 later)
    "ramp": {"low": 8, "base": 7, "high": 8},                      # years to the full cut (deals: full about 3 years after EIS)
}
P_LAUNCH = {"low": 0.08, "base": 0.20, "high": 0.40}               # chance Embraer-Korea launches (by about 2032): the
                                                                  # research said 35% (15-60%); its verifier, on Embraer's
                                                                  # May 2026 call (segment not chosen), 20% (8-40%)
P_LAUNCH_IF_BOEING = {"base": 0.10}                                # ... if Boeing launches an fps in 2030: Korea's chance of
                                                                  # backing Embraer falls from 25% to 12% (research), so the
                                                                  # chance is about halved
PARTNER_RATES = (0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08)        # partners' own rates, as stated (10.5% reading)
P_MAX = 0.6                                                       # the largest share of the bill searched
PACKAGES = {"Japan and Korea at their past scale": (0.11, 0.06),     # research: Japan about 8% of the bill at about 5.5%,
            "Japan and Korea, high": (0.23, 0.045),                 # Korea about 3% at about 7%; high 15% + 8%
            "787-style work share with state loans": (0.35, 0.04)}  # partners fund their work share (about 35% of the
                                                                  # structure) with state loans for most of it
FIXED = {"repo Joint Venture terms": (0.35, 0.25),                 # wargame/config/default.json: the partner pays 35% of the
                                                                  # capex and takes 25% of the margin
         "777/787-style package, pro rata": (0.20, 0.20),          # research: partners fund about 20% (8-35%) for about a
         "777/787-style package, risk premium": (0.20, 0.24),      # pro-rata share of the profit or more (1.0-1.5x)
         "large state-backed package, pro rata": (0.35, 0.35)}


def emb(level):
    return {k: v[level] for k, v in EMB.items()}


def world_options(level, share=True):
    """The run's engine options with Embraer as the entrant (share on), or the run's own (share off: price only)."""
    o = copy.deepcopy(T.O)
    if share:
        e = emb(level)
        tp = o["third_party"]
        tp["entrant"] = {"eis": e["eis"], "peak_a_month": e["peak_a_month"], "years_to_peak": e["years_to_peak"]}
        tp["entrant_share"] = e["share_fps"]
        tp["entrant_share_no_fps"] = e["share_no_fps"]
    return o


def price_options(level):
    e = emb(level)
    return {"from": e["eis"] - e["lead"], "ramp_years": e["ramp"], "cut": e["cut"]}


def cut_at(pp, y):
    """The engine's own price cut (SD.price_cut without the no-fps variant): pp is a price_pressure option or None."""
    if not pp or y < pp["from"]:
        return 0.0
    return pp["cut"] * min(1.0, (y - pp["from"] + 1) / float(pp["ramp_years"]))


# ─────────────────────────────── worlds ───────────────────────────────
W = {}          # world -> {n: (flows, horizon, terms)}
PRICE_OF = {}   # world -> (plan price_pressure, status quo price_pressure)


def load_world(key, opts, rounds=(1, 2, 3, 4)):
    saved = T.O
    T.O = opts
    try:
        W[key] = {}
        for n in rounds:
            PO.load_round(n, "base" if key == "as played" else key)
            W[key][n] = (PO.FL[n], PO.HOR[n], PO.TT[n])
    finally:
        T.O = saved


def hybrid(base_key, emb_key, n):
    """Deterred: the fps plans' flows from the world without Embraer, with the status quo of the Embraer world (the
    status quo never launches an fps, so Embraer comes); Do Nothing and the Re-engine alone from the Embraer world."""
    fb, hb, _ = W[base_key][n]
    fe, he, _ = W[emb_key][n]
    assert hb == he
    fl = {}
    for name in F.ROWS:
        if name in FPS:
            cols = []
            for f, g in zip(fb[name], fe["Do Nothing"]):
                h = copy.deepcopy(f)
                for y in h["years"]:
                    h["years"][y]["sq"] = g["years"][y]["sq"]
                for kind in h["ext"]:
                    for y in h["ext"][kind]:
                        h["ext"][kind][y]["sq"] = g["ext"][kind][y]["sq"]
                cols.append(h)
            fl[name] = cols
        else:
            fl[name] = fe[name]
    tt = {(lv, rn): F.term_table(fl, hb, r, F.prm_set(lv)) for lv in ("base",) for rn, r in RATES.items()}
    return fl, hb, tt


# ─────────────────────────────── one plan in one column ───────────────────────────────
def series(f, view, horizon):
    """{year: (MAX, fps, status-quo MAX units)} for the years the view counts: the brief's counted window, or (franchise
    view) every year to the round's end year on the base demand tail (the counted years after 2060 restated on it)."""
    if view == "game":
        return {y: (x["max"], x["fps"], x["sq"] / MAX_UNIT) for y, x in f["years"].items() if x["in_nb"]}
    ns = F.nb_series(f, F.prm_set("base")["tail"], horizon)
    return {y: (mx, fp, sq / MAX_UNIT) for y, (mx, fp, sq) in ns.items()}


def price_term(f, r, view, horizon, pp_plan, pp_sq):
    """PV (2026) of the price cut on Boeing's deliveries against the status quo's."""
    v = 0.0
    for y, (mx, fp, sq) in series(f, view, horizon).items():
        v -= ((fp * PRICE + mx * PRICE_737) * cut_at(pp_plan, y) - sq * PRICE_737 * cut_at(pp_sq, y)) * F.df(y, r)
    return v


def fps_profit(f, r, view, horizon, pp_plan):
    """PV at rate r of the fps's operating profit after the price cut, over the years the view counts the fps."""
    if not f["fps_eis"]:
        return 0.0
    v = 0.0
    prm = F.prm_set("base")
    for y, (mx, fp, sq) in series(f, view, horizon).items():
        if fp > 0:
            m = M0 if (view == "game" or y <= f["window_end"]) else F.margin_at(y, f, M0, prm)
            v += fp * PRICE * (m - cut_at(pp_plan, y)) * F.df(y, r)
    return v


def spend_pv(f, var, r):
    """PV at rate r of one dollar of the bill spent evenly over the development years (launch to EIS - 1)."""
    eis = f["fps_eis"]
    ys = range(eis - DEV[var], eis)
    return sum(F.df(y, r) for y in ys) / len(ys)


def partner_rate(rp, rname):
    return rp if rname == "10.5%" else (1 + rp) / (1 + INFL) - 1


# ─────────────────────────────── a round's values ───────────────────────────────
VIEWS = {"brief": ("game", False), "franchise": ("full", False), "franchise + politics": ("full", True)}


def split_game_pv(f, r):
    """F.game_pv(f, r, M0, k) as (the part that does not depend on k, a function of k)."""
    v = 0.0
    for y, x in f["years"].items():
        if x["in_nb"]:
            v += (x["fps"] * PRICE * M0 + x["max"] * MAX_UNIT - x["sq"]) * F.df(y, r)
        v += x["wb"] * F.df(y, r)
    if f["renton"]:
        v += f["renton"] * F.df(f["renton_year"], r)

    def inv(k):
        nom, pvc = 0.0, 0.0
        if f["fps_eis"]:
            nom += f["fps_bill"] * k
            pvc += f["fps_bill"] * k * F.df(f["fps_eis"], r)
        if f["re_eis"]:
            nom += f["re_bill"]
            pvc += f["re_bill"] * F.df(f["re_eis"], r)
        if nom <= 0:
            return 0.0
        out = F.tc(nom, pvc)
        if f["strain"]:
            out += f["strain"] / (f["pv_capex"] / f["nom"]) * (pvc / nom)
        return out
    return v, inv


class Round:
    """One round, rate and case in one world: every row's value in every column, fast in the bill share, the premium
    and the partner's terms."""
    def __init__(self, world, n, rname, case, pp=None):
        self.fl, self.hor, self.tt = W[world][n] if isinstance(world, str) else world
        self.n, self.rname, self.r = n, rname, RATES[rname]
        self.view, self.pol = VIEWS[case]
        self.scen = F.SCENARIOS[self.view]
        self.pp_plan, self.pp_sq = ({name: None for name in F.ROWS}, None) if not pp else pp
        tt = self.tt[("base", rname)]
        self.rows = {}
        for name in F.ROWS:
            row = []
            for f, t in zip(self.fl[name], tt[name]):
                fixed, inv = split_game_pv(f, self.r)
                pt = price_term(f, self.r, self.view, self.hor, self.pp_plan[name], self.pp_sq)
                row.append({"f": f, "fixed": fixed + sum(t[c] for c in self.scen) + pt, "inv": inv, "price": pt,
                            "terms": {c: t[c] for c in self.scen}})
            self.rows[name] = row
        self.X = PO.exit_cost("base", self.r, T.YEARS[n]) if self.pol else 0.0
        self.c_gov = PO.CASH["c_gov"]["base"] if self.pol else 0.0
        self.w = T.CEO_W[n]
        self._fp = {}

    def fp(self, name, j, rate):
        key = (name, j, round(rate, 12))
        if key not in self._fp:
            self._fp[key] = fps_profit(self.rows[name][j]["f"], rate, self.view, self.hor, self.pp_plan[name])
        return self._fp[key]

    def partner_terms(self, name, p, rp, spend="eis"):
        """(s, the partner's money in PV at its rate): s breaks the partner even in the CEO's expected columns."""
        f0 = self.rows[name][0]["f"]
        one = F.df(f0["fps_eis"], rp) if spend == "eis" else spend_pv(f0, VAR[name], rp)
        need = p * f0["fps_bill"] * one
        got = sum(self.fp(name, i, rp) * wt for i, wt in self.w.items())
        return (need / got if got > 0 else float("inf")), need

    def values(self, S=0.0, c_extra=0.0, partner=None, fixed=None):
        """Every row's value in every column; partner = (p, the partner's rate as Boeing's flows read it, spend): the
        partner breaks even; fixed = (p, s): set terms; S on the fps plans (the politics premium); the exit cost on the
        others in the politics case."""
        out, info = {}, {}
        for name in F.ROWS:
            k = 1.0 - self.c_gov - c_extra
            s = 0.0
            if partner and name in FPS:
                p, rp, spend = partner
                k -= p
                s, need = self.partner_terms(name, p, rp, spend)
                info[name] = {"s": s, "partner_money_pv": need}
            elif fixed and name in FPS:
                p, s = fixed
                s = s[name] if isinstance(s, dict) else s
                k -= p
                if not isinstance(fixed[1], dict):
                    info[name] = {"s": s, "implied_rate": self.implied_rate(name, p, s)}
            vals = []
            for j, c in enumerate(self.rows[name]):
                v = c["fixed"] - c["inv"](max(1e-9, k))
                if s:
                    v -= s * self.fp(name, j, self.r)
                v += S if name in FPS else -self.X
                vals.append(v)
            out[name] = vals
        return out, info

    def implied_rate(self, name, p, s, spend="eis"):
        """The partner's own rate at which terms (p, s) break it even in the CEO's expected columns (None if none in
        -5% to 40%)."""
        f = lambda rp: self.partner_terms(name, p, rp, spend)[0] - s
        lo, hi = -0.05, 0.40
        if f(lo) > 0 or f(hi) < 0:
            return None
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
        return (lo + hi) / 2

    def decide(self, **kw):
        V, info = self.values(**kw)
        d = PO.decide2(self.n, V)
        a = PO.decide2(self.n, V, anticipate=True)
        return {**{md: d[md] for md in T.MODES}, "anticipating": a["rule"], "pick": d["pick"], "e": d["e"]}, info

    def launches(self, reading="rule", **kw):
        d, _ = self.decide(**kw)
        return d[reading]


class Mix:
    """A probability-weighted round: [(round, weight), ...] with weights summing to one (Embraer launches or not, and
    whether a Boeing launch keeps it out). Values are the expected values plan by plan and column by column; a
    partner's terms are set on the expected fps profit, so one contract covers every outcome."""
    def __init__(self, parts):
        self.parts = parts
        assert abs(sum(w for _, w in parts) - 1.0) < 1e-12
        b = parts[-1][0]
        self.n, self.rname, self.r, self.pol, self.c_gov, self.w = b.n, b.rname, b.r, b.pol, b.c_gov, b.w
        assert all((r.n, r.rname, r.view, r.pol) == (b.n, b.rname, b.view, b.pol) for r, _ in parts)

    def partner_terms(self, name, p, rp, spend="eis"):
        need = self.parts[0][0].partner_terms(name, p, rp, spend)[1]
        got = sum(q * r.fp(name, i, rp) * wt for r, q in self.parts for i, wt in self.w.items())
        return (need / got if got > 0 else float("inf")), need

    def implied_rate(self, name, p, s, spend="eis"):
        return Round.implied_rate(self, name, p, s, spend)

    def values(self, S=0.0, c_extra=0.0, partner=None, fixed=None):
        info = {}
        if partner:
            p, rp, spend = partner
            terms = {name: self.partner_terms(name, p, rp, spend) for name in FPS}
            info = {name: {"s": s, "partner_money_pv": need} for name, (s, need) in terms.items()}
            fixed = (p, {name: s for name, (s, _) in terms.items()})
        elif fixed:
            info = {name: {"s": fixed[1], "implied_rate": self.implied_rate(name, fixed[0], fixed[1])} for name in FPS}
        vs = [(r.values(S=S, c_extra=c_extra, fixed=fixed)[0], q) for r, q in self.parts]
        V = {name: [sum(q * v[name][j] for v, q in vs) for j in range(len(vs[0][0][name]))] for name in vs[0][0]}
        return V, info

    decide = Round.decide
    launches = Round.launches


READS = ("rule", "pairwise", "worst_first", "premium", "anticipating")


def summarize(rd, spends=("eis",)):
    d, _ = rd.decide()
    out = {"decision": {k: d[k] for k in T.MODES + ("anticipating", "pick")}, "e": d["e"]}
    if rd.pol:                          # the strategic premium that launches, by reading
        dfy = (1 + rd.r) ** -(T.YEARS[rd.n] - 2026)
        out["S_needed"], out["S_needed_decision_year"] = {}, {}
        for md in READS:
            s, _ = T.first(lambda x: rd.launches(md, S=x) is not None, 0.0, 60.0, steps=120, tol=1e-5)
            out["S_needed"][md] = s
            out["S_needed_decision_year"][md] = None if s is None else s / dfy
    out["free_cut_needed"] = {}         # a free share of the bill (on top of the politics case's co-funding)
    for md in READS:
        c, _ = T.first(lambda x: rd.launches(md, c_extra=x) is not None, 0.0, 0.999 - rd.c_gov, steps=100, tol=1e-6)
        out["free_cut_needed"][md] = c
    out["partner"] = {}                 # the smallest share of the bill a partner must carry to launch, by its rate
    for spend in spends:
        for rp in PARTNER_RATES + (None,):
            key = ("boeing's rate" if rp is None else "%.0f%%" % (100 * rp)) + ("" if spend == "eis" else " | spread")
            rate = rd.r if rp is None else partner_rate(rp, rd.rname)
            res = {}
            for md in READS:
                p, mono = T.first(lambda x: rd.launches(md, partner=(x, rate, spend)) is not None, 0.0, P_MAX, steps=120, tol=1e-5)
                entry = {"p": p, "monotone": mono}
                if p is not None:
                    d2, info = rd.decide(partner=(p + 1e-5, rate, spend))
                    plan = d2[md]
                    entry.update({"plan": plan, "s": info[plan]["s"] if plan else None,
                                  "partner_money_pv": info[plan]["partner_money_pv"] if plan else None,
                                  "boeing_gain_vs_no_partner": (sum((rd.values(partner=(p + 1e-5, rate, spend))[0][plan][i] - rd.values()[0][plan][i]) * wt
                                                                    for i, wt in rd.w.items()) if plan else None)})
                res[md] = entry
            out["partner"][key] = res
    out["packages"] = {}
    for key, (p, rp) in PACKAGES.items():
        d2, info = rd.decide(partner=(p, partner_rate(rp, rd.rname), "eis"))
        out["packages"][key] = {"p": p, "rate": rp, "decision": {k: d2[k] for k in READS + ("pick",)}, "e": d2["e"],
                                "s": {name: info[name]["s"] for name in FPS}}
    out["fixed"] = {}
    for key, (p, s) in FIXED.items():
        d2, info = rd.decide(fixed=(p, s))
        V0, _ = rd.values()
        V1, _ = rd.values(fixed=(p, s))
        out["fixed"][key] = {"p": p, "s": s, "decision": {k: d2[k] for k in READS + ("pick",)}, "e": d2["e"],
                             "implied_rate": {name: info[name]["implied_rate"] for name in FPS},
                             "implied_rate_nominal": {name: (None if info[name]["implied_rate"] is None else
                                                             (info[name]["implied_rate"] if rd.rname == "10.5%" else (1 + info[name]["implied_rate"]) * (1 + INFL) - 1))
                                                      for name in FPS},
                             "boeing_gain": {name: sum((V1[name][i] - V0[name][i]) * wt for i, wt in rd.w.items()) for name in FPS}}
    return out


# ─────────────────────────────── checks ───────────────────────────────
def check_price_rule():
    """The engine's price_pressure gives the same change in Boeing's game value as price_term (brief view, 10.5%)."""
    e = emb("base")
    pp = price_options("base")
    opts = world_options("base")
    worst = 0.0
    for n in (1, 3):
        for name in ("Do Nothing", "10-year at Renton", "7-year, new sites"):
            for j in (0, 1):
                with F.L.patched(options=opts):
                    slab, s, c = T.column_states(n, F.PLAN_OF[name])[j]
                    v0 = M.value(s, covert=c, series=True)["boeing"]["pv_delta"]
                with F.L.patched(options=dict(opts, price_pressure=pp)):
                    slab, s, c = T.column_states(n, F.PLAN_OF[name])[j]
                    v1 = M.value(s, covert=c, series=True)["boeing"]["pv_delta"]
                f = W["Embraer base"][n][0][name][j]
                pt = price_term(f, P["WACC_B"], "game", W["Embraer base"][n][1], pp, pp)
                worst = max(worst, abs((v1 - v0) - pt))
                assert abs((v1 - v0) - pt) < 1e-9, (n, name, j, v1 - v0, pt)
    return worst


def check_no_embraer():
    """With Embraer off the values are politics.py's own: the franchise view's cash values, every row and column."""
    worst = 0.0
    for n in T.YEARS:
        rd = Round("as played", n, "10.5%", "franchise")
        V, _ = rd.values()
        PO.FL[n], PO.HOR[n], PO.TT[n] = W["as played"][n]
        PO._CACHE.clear()
        _, cash = PO.values(n, "base", "10.5%", "full")
        for name in F.ROWS:
            for a, b in zip(V[name], cash[name]):
                worst = max(worst, abs(a - b))
    assert worst < 1e-9, worst
    return worst


def check_partner_at_boeing_rate():
    """A partner at Boeing's own rate who spends at entry into service (the game's booking of the bill) leaves Boeing, in
    the CEO's column, exactly the debt-penalty saving on the share it carries; and split_game_pv is F.game_pv."""
    out = {}
    for n in (1, 2):
        rd = Round("as played", n, "10.5%", "brief")
        for name in ("10-year at Renton", "7-year, new sites", "10-year at Renton + Re-engine"):
            for j, c in enumerate(rd.rows[name]):
                for k in (1.0, 0.7, 0.35):
                    assert abs(c["fixed"] - c["inv"](k) - F.game_pv(c["f"], rd.r, M0, k)) < 1e-9
            p = 0.3
            V0, _ = rd.values()
            V1, _ = rd.values(partner=(p, rd.r, "eis"))
            gain = sum((V1[name][i] - V0[name][i]) * wt for i, wt in rd.w.items())
            f = rd.rows[name][0]["f"]
            nom0 = f["fps_bill"] + f["re_bill"]
            pv0 = f["fps_bill"] * F.df(f["fps_eis"], rd.r) + (f["re_bill"] * F.df(f["re_eis"], rd.r) if f["re_eis"] else 0.0)
            nom1 = f["fps_bill"] * (1 - p) + f["re_bill"]
            pv1 = f["fps_bill"] * (1 - p) * F.df(f["fps_eis"], rd.r) + (f["re_bill"] * F.df(f["re_eis"], rd.r) if f["re_eis"] else 0.0)
            debt = (F.tc(nom0, pv0) - pv0) - (F.tc(nom1, pv1) - pv1)
            strain = sum((rd.rows[name][i]["inv"](1.0) - F.tc(nom0, pv0)) - (rd.rows[name][i]["inv"](1 - p) - F.tc(nom1, pv1)) for i in rd.w) / len(rd.w)
            assert abs(gain - debt - strain) < 1e-9, (n, name, gain, debt, strain)
            out["%d|%s" % (n, name)] = {"gain": gain, "debt_penalty_saving": debt, "strain_change": strain}
    return out


# ─────────────────────────────── main ───────────────────────────────
WORLDS = ("as played", "Embraer low", "Embraer base", "Embraer high", "share only", "price only", "deterred",
          "expected", "expected, deterred", "expected, partly deterred")
ROUND1_ONLY = ("deterred", "expected", "expected, deterred", "expected, partly deterred")      # Boeing decides in 2030 before Embraer does; by 2035
                                                                  # it knows whether Embraer launched


def make_round(world, n, rname, case):
    q, qf = P_LAUNCH["base"], P_LAUNCH_IF_BOEING["base"]
    if world == "expected":
        return Mix([(make_round("Embraer base", n, rname, case), q), (make_round("as played", n, rname, case), 1 - q)])
    if world == "expected, deterred":
        return Mix([(make_round("deterred", n, rname, case), q), (make_round("as played", n, rname, case), 1 - q)])
    if world == "expected, partly deterred":
        # Embraer launches with chance qf if Boeing launches an fps in 2030, q if not: the fps plans see Embraer with
        # chance qf, Do Nothing and the status quo with chance q (weights: Embraer world qf, deterred q - qf, none 1 - q)
        return Mix([(make_round("Embraer base", n, rname, case), qf), (make_round("deterred", n, rname, case), q - qf),
                    (make_round("as played", n, rname, case), 1 - q)])
    if world == "deterred":
        if ("deterred", n) not in W:
            W[("deterred", n)] = hybrid("as played", "Embraer base", n)
        pp = price_options("base")
        return Round(W[("deterred", n)], n, rname, case, ({name: (None if name in FPS else pp) for name in F.ROWS}, pp))
    lv = world.split()[-1] if world.startswith("Embraer") else ("base" if world == "price only" else None)
    pp = price_options(lv) if lv else None
    return Round(world, n, rname, case, ({name: pp for name in F.ROWS}, pp) if pp else None)


def proposed_options():
    """The engine options this page proposes for the game's re-run (Embraer base): the run's own options with Embraer as
    the entrant, its second-source share, and the price pressure. Not played."""
    o = world_options("base")
    o["price_pressure"] = price_options("base")
    o["_note"] = ("Proposed for a re-run of the MAX phase-out game with Embraer-Korea as a third single-aisle maker (embraer.py, "
                  "base case; not played): Embraer-Korea in service %d, %.0f a month %d years later; it wins %.0f%% of new customers "
                  "once an fps is in service and %.0f%% while Boeing has no new narrowbody in service; its campaigns cut single-aisle "
                  "prices by up to %.1f%% from %d over %d years. Otherwise the run's own options (sd_options_phaseout.json)."
                  % (EMB["eis"]["base"], EMB["peak_a_month"]["base"], EMB["years_to_peak"]["base"], 100 * EMB["share_fps"]["base"],
                     100 * EMB["share_no_fps"]["base"], 100 * EMB["cut"]["base"], o["price_pressure"]["from"], o["price_pressure"]["ramp_years"]))
    return o


def main():
    load_world("as played", T.O)
    for lv in ("low", "base", "high"):
        load_world("Embraer " + lv, world_options(lv))
    W["share only"] = W["Embraer base"]
    W["price only"] = W["as played"]
    res = {"embraer": EMB, "p_launch": P_LAUNCH, "p_launch_if_boeing": P_LAUNCH_IF_BOEING, "partner_rates": PARTNER_RATES,
           "p_max": P_MAX, "fixed": FIXED, "packages": PACKAGES,
           "price_options": {lv: price_options(lv) for lv in ("low", "base", "high")}, "checks": {}, "worlds": {}}
    res["checks"]["no_embraer_equals_politics"] = check_no_embraer()
    res["checks"]["price_rule_engine_vs_overlay"] = check_price_rule()
    res["checks"]["partner_at_boeing_rate"] = check_partner_at_boeing_rate()
    print("checks", res["checks"], flush=True)
    res["units"] = units()
    for world in WORLDS:
        res["worlds"][world] = {}
        for n in T.YEARS:
            if world in ROUND1_ONLY and n != 1:
                continue
            rr = {"year": T.YEARS[n]}
            for rname in RATES:
                for case in VIEWS:
                    rd = make_round(world, n, rname, case)
                    d = summarize(rd, ("eis", "spread") if world in ("as played", "Embraer base", "expected") else ("eis",))
                    rr["%s|%s" % (case, rname)] = d
                    print(world, n, case, rname, d["decision"]["rule"], d["decision"]["pick"],
                          {k: round(v, 2) for k, v in d["e"].items()},
                          "S", None if not rd.pol else {k: (None if v is None else round(v, 2)) for k, v in d["S_needed"].items()},
                          "p", {k: (None if v["rule"]["p"] is None else round(v["rule"]["p"], 3)) for k, v in d["partner"].items()}, flush=True)
            res["worlds"][world][str(n)] = rr
    json.dump(res, open(os.path.join(HERE, "data", "embraer.json"), "w"), indent=1)
    json.dump(proposed_options(), open(os.path.join(HERE, "data", "sd_options_embraer_proposed.json"), "w"), indent=1)
    print("wrote data/embraer.json, data/sd_options_embraer_proposed.json")


def units():
    """Aircraft a year: Embraer's deliveries and Boeing's and Airbus's, with and without Embraer (base), Do Nothing and
    the 10-year fps at Renton launched in 2030, in the CEO's 2030 column, and the status quo."""
    out = {}
    for name in ("Do Nothing", "10-year at Renton"):
        for tag, opts in (("as played", T.O), ("Embraer base", world_options("base"))):
            with F.L.patched(options=opts):
                slab, s, c = T.column_states(1, F.PLAN_OF[name])[1]
                v = M.value(s, covert=c, series=True)
            out["%s|%s" % (name, tag)] = {r["year"]: {"embraer": r["sd"]["dlv_entrant"], "boeing": r["boeing"]["nb_units"],
                                                       "airbus": r["airbus"]["nb_units"], "comac": r["sd"]["dlv_comac"],
                                                       "sq_boeing": r["sd_sq"]["delivered_b"]}
                                         for r in v["_af_series"]["years"]}
            out["%s|%s" % (name, tag)]["column"] = slab
    return out


if __name__ == "__main__":
    main()
