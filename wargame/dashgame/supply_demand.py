"""Supply and demand: the game master's narrowbody layer for runs that switch it on (runs/<run>/supply_demand.txt).

The board sells a fixed 2,000 narrowbodies a year, split by its share rules, and books every one. This layer keeps
the board's shares as each customer's *preference*, but delivers only what the factories can build:

  total demand     = replacement + growth
  new demand(y)    = (growth(y) + replacement of today's fleets(y)) x 737/A320 class share
                     (replacement: the user's Cirium page, MAX/A320neo/A220 retirements; growth, not in the user's data:
                     the single-aisle fleet grows about 3.95% a year to 2044, Airbus GMF 2025 / Boeing CMO 2025, easing
                     to 3% by 2060)
  firm backlog     = the page's firm orders (MAX 4,769, A320neo family 7,330), delivered first; broadly the older
                     737NG / A320ceo fleets' replacement
  wanted_X(y)      = preference share_X(y) x new demand(y)
  delivered_X(y)   = firm backlog first, then min(capacity left, wanted_X(y) + waiting backlog_X) + spill in
  spill X -> Y     = min(flex x unmet_X, spare_Y)   (flexible customers: airlines flying both types, lessors and
                                                     unannounced customers take the other maker's free slots)
  backlog_X(y+1)   = (unmet_X - spill out) x (1 - lapse)   (a tenth of the waiting customers drop out each year)

Capacity, aircraft a year:
- Airbus: A320 at 85 a month until NGSA enters service, then the Rev. B rundown (base or Alt) and the NGSA ramp to
  100 a month, both read off the user's chart and shifted with the NGSA date. No NGSA: A320 stays at 85.
- Boeing: 737 MAX on Boeing's stated path (42.5, 49.5, 52, 54.5, then 57 a month from 2030); the 737 rate increase
  adds the board's 100 a year from 2032 while the MAX is built. The fps ramps like NGSA (the chart's shape, shifted to
  the fps date). Boeing's single-aisle total is capped at 100 a month (Airbus's Rev. B peak): as the fps fills it the
  MAX gives way, down to the Everett tail of 10 a month. New sites: the MAX carries on at Renton and Everett. Renton
  reassigned to the fps: the Renton MAX lines (47 a month, with the rate increase that rides on them) wind down like the
  A320 base plan and the Everett North Line carries on at up to 15 a month, saving the new-site capex (pro-rated if
  the switch comes late). After 2050 the MAX builds only what the fps cannot yet (it tops Boeing up to the fps's full
  rate while the fps ramps); with no fps the MAX carries on.

Pricing: new-type aircraft (fps, NGSA) are delivered first, up to their line's capacity, at the board's new-type
price and margin; the rest are 737 MAX or A320neo at the legacy price and margin. The status quo (no new programme
anywhere) runs the same rules with today's capacity and the board's 40/60 split. With unlimited capacity and demand
of 2,000 a year the layer changes nothing (test_supply_demand.py).
"""
import functools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "supply_demand.json")
CHART_YEAR = 2037              # NGSA entry-into-service year of the chart (mid-2037)
NB_BOARD = 2000.0
FAL_BUILD_YEARS = 3            # a final assembly site takes about 2-4 years to build (research notes)


@functools.lru_cache(maxsize=None)
def inputs():
    with open(PATH) as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def options():
    """Per-run options, runs/<run>/sd_options.json (absent: the rules above, as played in dash-2050-sd):
      demand_curve      file in this folder with an annual whole-market curve (years, replacements, growth), used
                        instead of supply_demand.json's replacement and growth (the class share still applies)
      firm_backlog      "netted": the firm orders are part of that demand, not extra to it: each year's demand is
                        served first from the firm orders still open (split between the makers in proportion to what
                        each has left), and only the rest is new customers split by preference; new customers start
                        once the firm orders are used up
      boeing_pp_after_ngsa   while NGSA is in service and Boeing has no new narrowbody in service, Boeing's
                        preference falls this many points a year from 40% (instead of the board's rule)
      boeing_takes_airbus_slack   Boeing's preference is never below the share Airbus cannot supply that year
                        (customers Airbus cannot serve buy from Boeing)
      airbus_capacity_response   Airbus raises its capacity by this fraction a year (compounding) in every year its
                        customers want more than it can build, until it can meet them
      max_phaseout      {"start": year, "gone": year}: the 737 MAX (in every plan, and the status quo) builds its full
                        rate to start - 1, then a straight line down to none in `gone` (the MAX is phased out)
      airbus_extra      {"from": year, "step_per_year": a month, "cap": a month}: Airbus adds extra lines on top of its
                        plan (not scaled by the capacity response): step_per_year more a month each year from `from`, up
                        to `cap` a month; the extra builds NGSA once NGSA is in service, else the A320neo family
      third_party       {"comac": {year: aircraft a year, ...}, "comac_first": share, "entrant": {"eis": year,
                        "peak_a_month": rate, "years_to_peak": n}, "entrant_share": share, "willing": share}: COMAC
                        and a new entrant build 737/A320-class aircraft too (capacity: straight lines between COMAC's
                        points; the entrant rises in a straight line to its peak). COMAC sells comac_first of its
                        capacity first, off the top of each year's new customers (its home market), and the entrant
                        wins entrant_share of them, up to its capacity; then Boeing and Airbus split the rest as usual,
                        and of the customers neither can serve (after the overflow between them) `willing` take a free
                        COMAC or entrant slot, split by free capacity. What is left waits, as before.
                        "entrant_share_no_fps": share (optional) - the entrant's share in the years Boeing has no new
                        narrowbody in service (customers who want a second source to Airbus); entrant_share applies
                        once an fps is in service. Absent: entrant_share in every year
      price_pressure    {"from": year, "ramp_years": n, "cut": share, "cut_boeing_no_fps": share (optional)}: a third
                        supplier's campaigns cut the price of every new single-aisle delivered (both makers, every type,
                        the status quo too) by cut x price, from `from`, rising in a straight line over ramp_years; cost
                        is unchanged, so profit falls by the whole cut. cut_boeing_no_fps replaces cut on Boeing's
                        aircraft in the years Boeing has no new narrowbody in service (the status quo in every year)
      embraer_player    Embraer is a player (rules.py order `enb`): its new narrowbody is the entrant, from its own EIS
                        (none in the status quo). {"peak_a_month", "years_to_peak": its line; "share_by_newgen": [share
                        of new customers with 0, 1, 2 new-generation types (fps, NGSA) in service]; "us_tariff_share_cut":
                        share of that lost to US tariffs; "cut", "cut_boeing_no_fps_mult", "lead", "ramp_years": its price
                        pressure, from `lead` years before its EIS (none while no Embraer airliner is launched)} plus its
                        economics (model.value_embraer). The run's generic entrant is not used with it.
      politics          {"boeing_cofund": share of the fps bill governments carry, "exit_p", "exit_loss_b", "exit_from",
                        "exit_years": the political cost of leaving the narrowbody market} (model.value_airframers)"""
    run = os.environ.get("DASH_RUN")
    path = os.path.join(HERE, "..", "runs", run, "sd_options.json") if run else None
    if path and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


@functools.lru_cache(maxsize=None)
def _curve():
    """The annual demand curve named by options()['demand_curve'], or None."""
    name = options().get("demand_curve")
    if not name:
        return None
    with open(os.path.join(HERE, name)) as f:
        c = json.load(f)
    return {y: (r, g) for y, r, g in zip(c["years"], c["replacements"], c["growth"])}


def reload():
    """Forget cached inputs and curves (for in-process sensitivities that edit supply_demand.json)."""
    inputs.cache_clear()
    options.cache_clear()
    _curve.cache_clear()
    _annual.cache_clear()


def _interp(pts, x):
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y1 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


@functools.lru_cache(maxsize=None)
def _annual(curve, shift, year):
    """Aircraft built in calendar `year` on a chart curve (rate a month) moved `shift` years later."""
    pts = inputs()["airbus"][curve]
    n = 48
    return sum(_interp(pts, year - shift + (k + 0.5) / n) for k in range(n)) / n * 12.0


def a320_full():
    return 12.0 * inputs()["airbus"]["a320_rate_no_ngsa"]


def _rundown(curve, shift, year):
    """A320 output on the chart curve, flat at 85 a month before the rundown (the chart's 2025 ramp is not used)."""
    if year < CHART_YEAR - 1 + shift:
        return a320_full()
    return _annual(curve, shift, year)


def demand(year):
    """New narrowbody demand in `year` (737/A320 class): growth + replacement of today's fleets. The firm backlog
    (firm_backlog) comes on top and is delivered first (with options()['firm_backlog'] == 'netted' it is the first
    part of this demand instead: see new_demand)."""
    d = inputs()["demand"]
    cv = _curve()
    if cv:                                     # a run's own curve; after its last year the last value is held
        r, g = cv[min(max(year, min(cv)), max(cv))]
        return (r + g) * d["class_share"]
    ys, rep = d["years"], d["replacements"]
    y = min(max(year, ys[0]), ys[-1])          # after 2075 the replacement wave is held at its 2075 value
    g = d["growth"].get(str(year), d["growth"][max(d["growth"], key=int)])
    return (g + rep[ys.index(y)]) * d["class_share"]


def growth(year):
    d = inputs()["demand"]
    cv = _curve()
    if cv:
        return cv[min(max(year, min(cv)), max(cv))][1] * d["class_share"]
    return d["growth"].get(str(year), d["growth"][max(d["growth"], key=int)]) * d["class_share"]


def firm_backlog():
    f = inputs()["demand"]["firm_backlog"]
    return float(f["boeing"]), float(f["airbus"])


def flex():
    return inputs()["demand"]["flex_share"]


def _live(state, key):
    r = state["prog"].get(key)
    return r if (r and r.get("cancel") is None) else None


def plans(state):
    sd = state.get("sd") or {}
    return sd.get("a320_plan", "base"), sd.get("fps_site", "new_site")


def max_phase_factor(year):
    """Share of the 737 MAX's capacity left in `year` under options()['max_phaseout'] (1 without it)."""
    ph = options().get("max_phaseout")
    if not ph or year < ph["start"]:
        return 1.0
    return max(0.0, (ph["gone"] - year) / (ph["gone"] - ph["start"] + 1))


def airbus_extra(year):
    """Airbus's extra capacity in `year`, aircraft a year (options()['airbus_extra'])."""
    x = options().get("airbus_extra")
    if not x or year < x["from"]:
        return 0.0
    return 12.0 * min(x["cap"], x["step_per_year"] * (year - x["from"] + 1))


def _points(pts, year):
    ks = sorted(int(k) for k in pts)
    v = {int(k): float(x) for k, x in pts.items()}
    if year < ks[0]:
        return 0.0
    if year >= ks[-1]:
        return v[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= year <= b:
            return v[a] + (v[b] - v[a]) * (year - a) / (b - a)
    return 0.0


def embraer():
    """The run's Embraer-player options (options()['embraer_player']), or None."""
    return options().get("embraer_player")


def embraer_line(state):
    """Embraer's live new narrowbody (rules.py `enb`), or None."""
    return _live(state, "enb") if embraer() else None


def third_capacity(year, state=None):
    """(COMAC, entrant) capacity in `year`, aircraft a year (options()['third_party']; zeros without it). With the
    Embraer player the entrant is Embraer's new narrowbody, from its EIS in `state` (none in the status quo)."""
    t = options().get("third_party") or {}
    em = embraer()
    if not t and not em:
        return 0.0, 0.0
    e = t.get("entrant") or {}
    ce = 0.0
    if em:
        r = _live(state, "enb") if state is not None else None
        if r and year >= r["eis"]:
            ce = 12.0 * em["peak_a_month"] * min(1.0, (year - r["eis"] + 1) / em["years_to_peak"])
    elif e and year >= e["eis"]:
        ce = 12.0 * e["peak_a_month"] * min(1.0, (year - e["eis"] + 1) / e["years_to_peak"])
    return _points(t.get("comac") or {"2026": 0}, year), ce


def newgen_in_service(state, year):
    """Number of new-generation narrowbodies (fps, NGSA) in service in `year`."""
    return sum(1 for k in ("fps", "ngsa") if _live(state, k) and year >= _live(state, k)["eis"])


def embraer_share(state, year):
    """Share of the year's new customers Embraer's new narrowbody wins (before its line's capacity)."""
    em = embraer()
    sh = em["share_by_newgen"][min(2, newgen_in_service(state, year))]
    return float(sh) * (1.0 - float(em.get("us_tariff_share_cut", 0.0)))


def airbus_capacity(state, year):
    """(A320, NGSA) aircraft in `year`."""
    ngsa = _live(state, "ngsa")
    if not ngsa:
        return a320_full(), 0.0
    shift = ngsa["eis"] - CHART_YEAR
    plan = plans(state)[0]
    return _rundown("a320_alt" if plan == "alt" else "a320_base", shift, year), _annual("ngsa", shift, year)


def max_path(year):
    b = inputs()["boeing"]
    return 12.0 * b["max_rate"].get(str(year), b["max_rate_after"])


def fps_full():
    b = inputs()["boeing"]
    return 12.0 * max(r for _, r in inputs()["airbus"]["ngsa"]) * b.get("fps_ramp_scale", 1.0)


def boeing_capacity(state, year):
    """(737 MAX, fps) aircraft in `year`."""
    b = inputs()["boeing"]
    k = max_phase_factor(year)                 # the MAX phase-out (a run option), on the path and the rate increase
    m = max_path(year) * k
    hike = (b["rate_increase_per_year"] if (state.get("rate737") and year >= b["rate_increase_from"]) else 0.0) * k
    fps = _live(state, "fps")
    if not fps:
        return m + hike, 0.0
    shift = fps["eis"] - CHART_YEAR
    f = _annual("ngsa", shift, year) * b.get("fps_ramp_scale", 1.0)
    if plans(state)[1] == "renton":
        # Renton's MAX lines (up to renton_rate a month) wind down like the A320 base plan as the fps ramps up there,
        # and the rate increase rides on them; the Everett North Line carries on, up to its own capacity
        keep = _rundown("a320_base", shift, year) / a320_full()
        m = max(min(m, 12.0 * b["everett_rate"]), m - min(m, 12.0 * b["renton_rate"]) * (1.0 - keep))
        hike *= keep
    mx = m + hike
    # Boeing's single-aisle total is capped; the fps fills it first and the MAX keeps at least its Everett tail
    cap = 12.0 * b["total_rate_cap"]
    tail = min(mx, 12.0 * b["max_tail_rate"]) if year <= b["max_last_year"] else 0.0
    f = min(f, max(0.0, cap - tail))
    mx = min(mx, max(0.0, cap - f))
    if year > b["max_last_year"]:
        mx = min(mx, max(0.0, fps_full() - f))        # after 2050 the MAX only tops Boeing up while the fps ramps
    return mx, f


def deliveries(b_pref, d, cap_b, cap_a, fx, back_b=0.0, back_a=0.0, lapse=0.0, firm_b=0.0, firm_a=0.0):
    """One year's market: preference share of Boeing, new demand, capacities, flexible share, the firm backlog
    (delivered first; never lapses or switches) and the waiting backlog of earlier years' unserved new demand ->
    delivered, spill and both backlogs carried into next year (the waiting one after the lapse)."""
    fb_, fa_ = min(firm_b, cap_b), min(firm_a, cap_a)
    cb, ca = cap_b - fb_, cap_a - fa_
    wb, wa = b_pref * d, (1.0 - b_pref) * d
    qb, qa = min(wb + back_b, cb), min(wa + back_a, ca)
    ub, ua = wb + back_b - qb, wa + back_a - qa
    to_b = min(fx * ua, cb - qb)
    to_a = min(fx * ub, ca - qa)
    nb, na = (ub - to_a) * (1.0 - lapse), (ua - to_b) * (1.0 - lapse)
    return {"demand": d, "wanted_b": wb, "wanted_a": wa, "cap_b": cap_b, "cap_a": cap_a,
            "firm_in_b": firm_b, "firm_in_a": firm_a, "firm_b": firm_b - fb_, "firm_a": firm_a - fa_,
            "backlog_in_b": back_b, "backlog_in_a": back_a,
            "delivered_b": fb_ + qb + to_b, "delivered_a": fa_ + qa + to_a, "spill_to_b": to_b, "spill_to_a": to_a,
            "backlog_b": nb, "backlog_a": na, "lost": (ub - to_a + ua - to_b) * lapse}


def sq_state():
    return {"prog": {}, "rate737": None, "sd": {}}


def boeing_base_pref(state, year, board_pref):
    """Boeing's preference share before the slack floor: the board's, or with options()['boeing_pp_after_ngsa'] a
    fall of that many points a year from 40% while NGSA is in service and Boeing has no new narrowbody in service.
    (With both programmes launched and NGSA first, the board already moves 1 point a year, the lead edge.)"""
    pp = options().get("boeing_pp_after_ngsa")
    if pp is None:
        return board_pref
    ngsa, fps = _live(state, "ngsa"), _live(state, "fps")
    if ngsa and year >= ngsa["eis"] and not (fps and year >= fps["eis"]):
        return max(0.0, 0.40 - pp / 100.0 * (year - ngsa["eis"] + 1))
    return board_pref


def year_rows(state, b_pref_by_year, years):
    o = options()
    out = {}
    fx, lapse = flex(), inputs()["demand"]["lapse_per_year"]
    bb, ba = 0.0, 0.0
    kb, ka = firm_backlog()
    netted = o.get("firm_backlog") == "netted"
    cb, ca = 0.0, 0.0                           # netted: firm orders already called by demand but not yet delivered
    resp = float(o.get("airbus_capacity_response") or 0.0)
    m_a = 1.0                                   # Airbus capacity against its plan (capacity response)
    tp = o.get("third_party") or {}
    emb = embraer()
    ngsa_live = _live(state, "ngsa")
    fps_live = _live(state, "fps")
    ys = sorted(years)
    if netted:
        assert ys[0] == 2026, "netting the firm backlog needs every year from 2026"
    for y in ys:
        mb, fb = boeing_capacity(state, y)
        a3, ng = airbus_capacity(state, y)
        a3, ng = a3 * m_a, ng * m_a
        xa = airbus_extra(y)                    # Airbus's extra lines: NGSA once in service, else A320neo family
        if ngsa_live and y >= ngsa_live["eis"]:
            ng += xa
        else:
            a3 += xa
        gross = demand(y)
        if netted:                              # this year's demand is served first from the firm orders still open
            need = min(gross, kb + ka)          # (kb, ka: not yet called by demand)
            nb_ = need * kb / (kb + ka) if kb + ka > 0 else 0.0
            na_ = need - nb_
            open_b, open_a = kb + cb, ka + ca
            kb, ka = kb - nb_, ka - na_
            fb_in, fa_in = cb + nb_, ca + na_   # firm orders to deliver this year: called earlier and called now
            d = gross - need
        else:
            fb_in, fa_in, d = kb, ka, gross
        cc, ce = third_capacity(y, state)       # COMAC's home sales and the entrant's won share come off the top
        pc = min(cc * float(tp.get("comac_first", 0.0)), d)
        d -= pc
        sh_e = float(tp.get("entrant_share", 0.0))
        if "entrant_share_no_fps" in tp and not (fps_live and y >= fps_live["eis"]):
            sh_e = float(tp["entrant_share_no_fps"])       # no new Boeing narrowbody in service: the second-source share
        if emb:
            sh_e = embraer_share(state, y)                 # Embraer the player: by new-generation types in service
        pe = min(ce, d * sh_e)
        d -= pe
        base = boeing_base_pref(state, y, b_pref_by_year[y])
        free_a = max(0.0, a3 + ng - min(fa_in, a3 + ng) - ba)   # Airbus slots left for new customers this year
        pref = base
        if o.get("boeing_takes_airbus_slack") and d > 0:
            pref = min(1.0, max(base, 1.0 - free_a / d))     # customers Airbus cannot serve buy from Boeing
        r = deliveries(pref, d, mb + fb, a3 + ng, fx, bb, ba, lapse, fb_in, fa_in)
        r.update({"demand_gross": gross, "pref_b": pref, "pref_b_base": base, "airbus_capacity_factor": m_a})
        # customers neither maker can serve (after the overflow) take a free COMAC or entrant slot
        rem_c, rem_e = max(0.0, cc - pc), max(0.0, ce - pe)
        tc = te = 0.0
        if rem_c + rem_e > 0:
            ub, ua = r["backlog_b"] / (1.0 - lapse), r["backlog_a"] / (1.0 - lapse)
            take = min(float(tp.get("willing", 1.0)) * (ub + ua), rem_c + rem_e)
            tb = take * ub / (ub + ua) if ub + ua > 0 else 0.0
            ta = take - tb
            tc = take * rem_c / (rem_c + rem_e)
            te = take - tc
            r["backlog_b"], r["backlog_a"] = (ub - tb) * (1.0 - lapse), (ua - ta) * (1.0 - lapse)
            r["lost"] = (ub - tb + ua - ta) * lapse
        r.update({"cap_comac": cc, "cap_entrant": ce, "dlv_comac": pc + tc, "dlv_entrant": pe + te, "cap_airbus_extra": xa,
                  "dlv_embraer": (pe + te) if emb else 0.0, "share_embraer": sh_e if emb else 0.0})
        if netted:                              # called firm orders not delivered wait (never lapse); uncalled stay open
            cb, ca = r["firm_b"], r["firm_a"]
            r["firm_in_b"], r["firm_in_a"] = open_b, open_a
            r["firm_b"], r["firm_a"] = kb + cb, ka + ca
        if resp and (1.0 - base) * d > free_a + 1e-9:          # Airbus short at its customers' own preference
            m_a *= 1.0 + resp
        if not netted:
            kb, ka = r["firm_b"], r["firm_a"]
        r.update({"cap_max": mb, "cap_fps": fb, "cap_a320": a3, "cap_ngsa": ng})
        # new types are delivered first, up to their own line's capacity; the rest are today's types
        r["dlv_fps"] = min(r["delivered_b"], fb)
        r["dlv_max"] = r["delivered_b"] - r["dlv_fps"]
        r["dlv_ngsa"] = min(r["delivered_a"], ng)
        r["dlv_a320"] = r["delivered_a"] - r["dlv_ngsa"]
        bb, ba = r["backlog_b"], r["backlog_a"]
        out[y] = r
    return out


def renton_share(state):
    """Share of the Renton saving Boeing still gets: full if Renton was chosen at least FAL_BUILD_YEARS before the
    fps entry into service (no new site built yet), pro-rated if later."""
    fps = _live(state, "fps")
    if not fps or plans(state)[1] != "renton":
        return 0.0
    since = (state.get("sd") or {}).get("fps_site_year") or fps["launch"]
    return max(0.0, min(1.0, (fps["eis"] - since) / FAL_BUILD_YEARS))


def costs(state):
    """GM costs of the supply plans: [(side, year, item, $B nominal)]. Negative = a saving."""
    b, a = inputs()["boeing"], inputs()["airbus"]
    out = []
    ngsa, fps = _live(state, "ngsa"), _live(state, "fps")
    a320, site = plans(state)
    if ngsa and a320 == "alt":
        out.append(("airbus", ngsa["eis"], "A320 Alt plan (lines kept longer)", a["alt_cost_b"]))
    sh = renton_share(state)
    if sh > 0:
        out.append(("boeing", fps["eis"], "fps at Renton: new-site capex avoided", -b["renton_saving_b"] * sh))
    return out


def price_pressure(state):
    """The price-pressure terms in force for `state`: the run's option, or with the Embraer player the terms its
    launched airliner brings (from `lead` years before its EIS; none while it is not launched or is cancelled)."""
    em = embraer()
    if not em:
        return options().get("price_pressure")
    r = _live(state, "enb")
    if not r:
        return None
    c = float(em["cut"])
    return {"from": r["eis"] - int(em.get("lead", 0)), "ramp_years": em["ramp_years"], "cut": c,
            "cut_boeing_no_fps": c * float(em.get("cut_boeing_no_fps_mult", 1.0))}


def price_cut(state, side, year):
    """Share of the price a third supplier's campaigns take off each new single-aisle `side` delivers in `year`
    (options()['price_pressure'], or the Embraer player's launched airliner; 0 without it)."""
    pp = price_pressure(state)
    if not pp or year < pp["from"]:
        return 0.0
    c = float(pp["cut"])
    if side == "boeing" and "cut_boeing_no_fps" in pp:
        fps = _live(state, "fps")
        if not (fps and year >= fps["eis"]):
            c = float(pp["cut_boeing_no_fps"])
    return c * min(1.0, (year - pp["from"] + 1) / float(pp["ramp_years"]))


def apply(state, rows, waccs):
    """Re-deliver the airframer series rows (from model.af_series) under supply and demand, in place.
    Returns ({side: {"supply_demand": PV $B, "supply_plan": PV $B}}, cost items, scenario rows, status-quo rows)."""
    years = [r["year"] for r in rows]
    pref = {r["year"]: r["boeing"]["nb_share"] for r in rows}
    sc = year_rows(state, pref, years)
    sq = year_rows(sq_state(), {y: 0.40 for y in years}, years)
    adj = {"boeing": 0.0, "airbus": 0.0}
    for r in rows:
        y = r["year"]
        s, q = sc[y], sq[y]
        for side, pre, sq_sh, new, old in (("boeing", "b", 0.40, "fps", "max"), ("airbus", "a", 0.60, "ngsa", "a320")):
            x = r[side]
            sq_unit = x["sq_nb_profit"] / (NB_BOARD * sq_sh)           # legacy (737 MAX / A320neo) profit per aircraft
            new_unit = x["nb_price"] / 1000.0 * x["nb_margin"]         # the board's unit in this year (new type from EIS)
            n_new, n_old = s["dlv_" + new], s["dlv_" + old]
            x["board_nb_units"], x["board_nb_profit"], x["board_sq_nb_profit"] = x["nb_units"], x["nb_profit"], x["sq_nb_profit"]
            x["board_nb_revenue"] = x["nb_revenue"]
            legacy_price = x["legacy_nb_price"]                         # $M per aircraft
            cut, cut_sq = price_cut(state, side, y), price_cut(sq_state(), side, y)
            x["nb_units"] = n_new + n_old
            x["nb_units_new"], x["nb_units_old"] = n_new, n_old
            x["nb_revenue"] = (n_new * x["nb_price"] + n_old * legacy_price) / 1000.0 * (1.0 - cut)
            x["nb_profit"] = n_new * (new_unit - cut * x["nb_price"] / 1000.0) + n_old * (sq_unit - cut * legacy_price / 1000.0)
            sq_dlv = q["delivered_" + pre]
            x["sq_nb_units"] = sq_dlv
            x["sq_nb_profit"] = sq_dlv * (sq_unit - cut_sq * legacy_price / 1000.0)
            x["price_cut"], x["sq_price_cut"] = cut, cut_sq
            x["nb_delivered_share"] = (n_new + n_old) / max(1e-9, s["delivered_a"] + s["delivered_b"] + s["dlv_comac"] + s["dlv_entrant"])
            x["nb_pref_share"] = s["pref_b"] if side == "boeing" else 1.0 - s["pref_b"]   # what customers want
            x["nb_share"] = x["nb_delivered_share"]                   # market share = share of deliveries
            x["sd"] = {"demand": s["demand"], "wanted": s["wanted_" + pre], "capacity": s["cap_" + pre],
                       "backlog_in": s["backlog_in_" + pre], "backlog_out": s["backlog_" + pre],
                       "firm_in": s["firm_in_" + pre], "firm_out": s["firm_" + pre],
                       "spill_in": s["spill_to_" + pre], "sq_delivered": sq_dlv, "sq_capacity": q["cap_" + pre],
                       "new_units": n_new, "old_units": n_old}
            if x["nb_in_window"]:
                adj[side] += ((x["nb_profit"] - x["board_nb_profit"]) - (x["sq_nb_profit"] - x["board_sq_nb_profit"])) * r["df_" + pre]
        r["sd"] = {k: s[k] for k in ("demand", "demand_gross", "pref_b_base", "airbus_capacity_factor", "cap_max", "cap_fps", "cap_a320",
                                     "cap_ngsa", "lost", "backlog_b", "backlog_a", "firm_b", "firm_a",
                                     "dlv_max", "dlv_fps", "dlv_a320", "dlv_ngsa", "dlv_comac", "dlv_entrant", "cap_comac",
                                     "cap_entrant", "cap_airbus_extra", "dlv_embraer", "share_embraer")}
        r["sd_sq"] = {"delivered_b": q["delivered_b"], "delivered_a": q["delivered_a"], "lost": q["lost"],
                      "dlv_max": q["dlv_max"], "dlv_a320": q["dlv_a320"]}
    plan = {"boeing": 0.0, "airbus": 0.0}
    items = []
    for side, y, item, x in costs(state):
        plan[side] -= x / ((1 + waccs[side]) ** (y - 2026))
        items.append((side, y, item, x))
    return {side: {"supply_demand": adj[side], "supply_plan": plan[side]} for side in adj}, items, sc, sq
