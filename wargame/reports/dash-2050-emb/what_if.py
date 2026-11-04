"""What Embraer's choice did, and what would change it, in run dash-2050-emb (Embraer as a sixth player, with political
terms, in the MAX phase-out game). Writes data/what_if.json:

  counterfactual  the whole game replayed with every company's recorded orders, except that Embraer's 2030 order is
                  flipped (launch if it held, hold if it launched); every company's ΔPV and Boeing's market and debt in
                  both worlds (orders no longer legal in the flipped world become hold, as in reports.regret)
  break_even      at the 2030 decision, with the rivals' actual 2030 orders and nobody moving after (the brief's
                  view): Embraer's ΔPV from a launch, and the value of one lever at a time that brings it to zero:
                  partners' share of the bill, operating margin, line peak rate, no US tariff cut
  politics        Boeing's ΔPV in the final state with the political terms off, and each term's size
  played_path     every company's ΔPV and Boeing's bridge after each round on the played-path basis (model.played_path:
                  the political exit cost counts from 2045, the years the path carried with no fps, where the record
                  and the briefs count it from the later of 2045 and the round's year)

The counterfactual worlds and the politics block are valued on the played-path basis too; the break-even and the
co-funding items are decisions in their round, valued as the briefs value them.

  DASH_RUN=dash-2050-emb DASH_BOARD=v3 python3 what_if.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DASH_RUN", "dash-2050-emb")
os.environ.setdefault("DASH_BOARD", "v3")
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
import model as M  # noqa: E402
import rules as R  # noqa: E402
import supply_demand as SD  # noqa: E402
import finance as FIN  # noqa: E402
import reports as RP  # noqa: E402

RUN = os.environ["DASH_RUN"]
RD = os.path.join(HERE, "..", "..", "runs", RUN)
jl = lambda n: json.load(open(os.path.join(RD, n)))
N = RP.rounds_played()
RECS = [jl("record_r%d.json" % n) for n in range(1, N + 1)]
S0 = jl("state_r0.json")
SN = jl("state_r%d.json" % N)


def replay(flip_emb_2030=False):
    s = S0
    trail = []
    for n, rec in enumerate(RECS, 1):
        orders = {}
        for side in M.SIDES:
            o = dict(rec["orders"][side])
            if flip_emb_2030 and side == "embraer" and n == 1:
                o["enb"] = "hold" if rec["orders"]["embraer"]["enb"] == "launch" else "launch"
            orders[side], _ = R.validate(s, side, rec["year"], o)
        s, _ = R.adjudicate(s, rec["year"], orders)
        trail.append(s)
    return s, trail


def world(s, trail):
    with M.played_path():
        v = M.value(s, covert=True, series=True)
    with FIN.history_override(trail):
        debt = FIN.debt_path(s, v, covert=True)
    af = {r["year"]: r for r in v["_af_series"]["years"]}
    em = {r["year"]: r for r in v["_emb_series"]["years"]}
    yrs = range(2026, 2061)
    return {"value": {x: v[x]["pv_delta"] for x in M.SIDES},
            "boeing_bridge": v["boeing"]["bridge"],
            "boeing_nb_units": {y: af[y]["boeing"]["nb_units"] for y in yrs},
            "airbus_nb_units": {y: af[y]["airbus"]["nb_units"] for y in yrs},
            "embraer_units": {y: em[y]["nb_units"] for y in yrs},
            "boeing_share": {y: af[y]["boeing"]["nb_share"] for y in yrs},
            "boeing_board_share": {y: af[y]["boeing"]["board_nb_units"] / M.P_NB for y in yrs},
            "boeing_profit": {y: af[y]["boeing"]["nb_profit"] + af[y]["boeing"]["wb_profit"] for y in yrs},
            "boeing_cut": {y: af[y]["boeing"].get("price_cut", 0.0) for y in yrs},
            "boeing_debt": {r["year"]: r["debt"] for r in debt},
            "embraer_live": bool(M.live(s, "enb"))}


def emb_2030(opts_patch):
    """Embraer's ΔPV in 2030 from a launch against hold, rivals' actual 2030 orders, nobody moving after."""
    base = SD.options()
    o = copy.deepcopy(base)
    o["embraer_player"].update(opts_patch)
    SD.options = lambda: o
    try:
        rec = RECS[0]
        orders = {s: dict(rec["orders"][s]) for s in M.SIDES}
        orders["embraer"] = {"enb": "launch"}
        s1, _ = R.adjudicate(S0, rec["year"], orders)
        return M.value(s1, covert=True, series=True)["embraer"]["pv_delta"]
    finally:
        SD.options = lambda: base


FPS_PLANS = {"fps 10-yr at Renton": {"fps": "launch_10yr", "fps_engine_code": 7, "fps_site": "renton"},
             "fps 10-yr at new sites": {"fps": "launch_10yr", "fps_engine_code": 7, "fps_site": "new_site"}}


def fps_item(n, plan, c):
    """Boeing's fps launch in round n against Do Nothing, everyone else's recorded orders that round, nobody moving
    after (the brief's view), with governments carrying share c of the fps bill."""
    base = SD.options()
    o = copy.deepcopy(base)
    o.setdefault("politics", {})["boeing_cofund"] = c
    SD.options = lambda: o
    try:
        rec, prev = RECS[n - 1], jl("state_r%d.json" % (n - 1))
        orders = {s: dict(rec["orders"][s]) for s in M.SIDES}
        dn, _ = R.adjudicate(prev, rec["year"], orders)
        orders["boeing"] = dict(orders["boeing"], **FPS_PLANS[plan])
        fp, _ = R.adjudicate(prev, rec["year"], orders)
        return M.value(fp, covert=True, series=False)["boeing"]["pv_delta"] - M.value(dn, covert=True, series=False)["boeing"]["pv_delta"]
    finally:
        SD.options = lambda: base


def cofund_needed():
    """Per round and fps plan: the item value with no co-funding, with the game's 2%, and the share of the bill
    governments would have to carry for the item to clear the Board's +$1B business case."""
    out = {}
    for n, rec in enumerate(RECS, 1):
        out[str(rec["year"])] = {}
        for plan in FPS_PLANS:
            f = lambda c: fps_item(n, plan, c) - 1.0
            out[str(rec["year"])][plan] = {"none": fps_item(n, plan, 0.0), "as_played": fps_item(n, plan, SD.options()["politics"]["boeing_cofund"]),
                                           "needed": solve(f, 0.0, 1.0, 1e-5)}
    return out


def solve(f, lo, hi, tol=1e-6):
    """x in [lo, hi] with f(x) = 0 (f increasing), or None if f(hi) < 0."""
    if f(hi) < 0:
        return None
    if f(lo) >= 0:
        return lo
    for _ in range(80):
        m = (lo + hi) / 2
        if f(m) >= 0:
            hi = m
        else:
            lo = m
        if hi - lo < tol:
            break
    return hi


def main():
    played, trail = replay(False)
    assert json.dumps(played, sort_keys=True, default=str) == json.dumps(SN, sort_keys=True, default=str), "replay differs from the record"
    flip, trail_f = replay(True)
    E = SD.embraer()
    out = {"run": RUN, "embraer_2030_order": RECS[0]["orders"]["embraer"]["enb"],
           "played": world(played, trail), "flipped": world(flip, trail_f)}
    base = emb_2030({})
    own = 1 - E["partner_share"] - E["supplier_share"] - E["state_share"]
    be = {"base": base,
          "partner_share": solve(lambda p: emb_2030({"partner_share": p}), E["partner_share"], 1 - E["supplier_share"] - E["state_share"]),
          "margin": solve(lambda m: emb_2030({"margin": m}), E["margin"], 0.60),
          "peak_a_month": solve(lambda r: emb_2030({"peak_a_month": r}), E["peak_a_month"], 40.0, 1e-4),
          "no_tariff": emb_2030({"us_tariff_share_cut": 0.0}),
          "bill_b": None}
    # the whole bill (Embraer's own share scales with it): the largest bill at which a launch breaks even
    lo, hi = 0.0, E["bill_b"]
    if emb_2030({"bill_b": 0.0}) >= 0:
        f = lambda b: -emb_2030({"bill_b": b})
        for _ in range(80):
            m = (lo + hi) / 2
            if emb_2030({"bill_b": m}) >= 0:
                lo = m
            else:
                hi = m
        be["bill_b"] = lo
    be["own_share"] = own
    out["break_even"] = be
    # every round's value on the played-path basis, next to the record's (decision) basis
    pp = []
    for n, rec in enumerate(RECS, 1):
        st = jl("state_r%d.json" % n)
        with M.played_path():
            vp = M.value(st, covert=True, series=False)
        pp.append({"round": n, "year": rec["year"], "value": {x: vp[x]["pv_delta"] for x in M.SIDES},
                   "record_value": {x: rec["value"][x]["pv_delta"] for x in M.SIDES},
                   "bridge": {x: vp[x]["bridge"] for x in ("boeing", "airbus") + (("embraer",) if "embraer" in M.SIDES else ())}})
    out["played_path"] = pp
    # politics: Boeing's final ΔPV without the political terms, and each term (played-path basis)
    with M.played_path():
        v = M.value(played, covert=True, series=True)
    po = copy.deepcopy(SD.options())
    po.pop("politics", None)
    keep = SD.options
    SD.options = lambda: po
    try:
        v0 = M.value(played, covert=True, series=True)
    finally:
        SD.options = keep
    out["politics"] = {"boeing_with": v["boeing"]["pv_delta"], "boeing_without": v0["boeing"]["pv_delta"],
                       "terms": {k: v["boeing"]["bridge"].get(k, 0.0) for k in ("government_cofunding", "political_exit_cost")},
                       "exit_cost_2030": M.exit_cost(v["boeing"]["wacc"], 2030), "exit_cost_2050": M.exit_cost(v["boeing"]["wacc"], 2050),
                       "record_boeing": RECS[-1]["value"]["boeing"]["pv_delta"]}
    out["cofund"] = cofund_needed()
    json.dump(out, open(os.path.join(HERE, "data", "what_if.json"), "w"), indent=1, default=str)
    print("Embraer 2030:", out["embraer_2030_order"], "| flipped values:", {k: round(x, 2) for k, x in out["flipped"]["value"].items()})
    print("played values:", {k: round(x, 2) for k, x in out["played"]["value"].items()})
    print("break-even:", {k: (round(x, 4) if isinstance(x, float) else x) for k, x in be.items()})
    print("politics:", out["politics"])
    print("played path:", [(x["year"], round(x["value"]["boeing"], 4), round(x["record_value"]["boeing"], 4)) for x in pp])


if __name__ == "__main__":
    main()
