"""Why the 2030 fps decision differs from the game without supply and demand (dash-2050-obj, where Boeing launched
it): a bridge from the dashboard alone to this game, for the 10-year fps at Renton and at new sites against Do Nothing,
everyone else's 2030 orders as played in this game.

The dashboard alone sells 2,000 narrowbodies a year, split by its share rule, and books every one; the
supply-and-demand layer with every limit switched off (unlimited factories, 2,000 a year, no firm orders, none of the
user's rules) gives back exactly the same values (checked). Then one change at a time, in this order:
  1. Renton's site saving (the layer books it; the dashboard has no site choice)
  2. Boeing's real factories: the fps ramps on the NGSA curve, the 737 MAX path to 57 a month, the 100-a-month cap,
     the Renton wind-down
  3. Airbus's real factories: the Rev. B plan on the Alt plan
  4. the user's conservative demand curve, firm orders on top
  5. firm orders inside demand (option B)
  6. Boeing loses 1 point a year after NGSA
  7. Airbus's slack goes to Boeing
  8. Airbus adds 1% capacity a year when short  (= this game)
Each step reports the fps case, Do Nothing (both against the status quo) and the item (fps minus Do Nothing). The order
matters, so a Shapley split over five groups (Boeing's factories, Airbus's factories, demand, the share rules, the
capacity response) is reported too. Writes bridge.json next to this file.

  python3 bridge.py
"""
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import lib as L  # noqa: E402

M = L.M
OFF = {"demand_curve": None, "firm_backlog": None, "boeing_pp_after_ngsa": None, "boeing_takes_airbus_slack": None,
       "airbus_capacity_response": None}
S = {"dn": L.build({}, "new_site"), "renton": L.build(L.F10, "renton"), "new_site": L.build(L.F10, "new_site")}


def measure(kw=None, sd_on=True):
    M.SD_ON = sd_on
    try:
        with L.patched(**(kw or {})):
            v = {k: M.value(s, covert=True, series=True) for k, s in S.items()}
    finally:
        M.SD_ON = True
    out = {k: v[k]["boeing"]["pv_delta"] for k in v}
    out["item_renton"] = out["renton"] - out["dn"]
    out["item_new_site"] = out["new_site"] - out["dn"]
    # Boeing's deliveries, 2040-2059 (the fps window), and the fps's own
    for k in v:
        rows = [r for r in v[k]["_af_series"]["years"] if 2040 <= r["year"] <= 2059]
        out["dlv_" + k] = sum(r["boeing"]["nb_units"] for r in rows)
        out["fps_" + k] = sum(r["boeing"].get("nb_units_new", 0.0) if sd_on else (r["boeing"]["nb_units"] if r["year"] >= 2040 and k != "dn" else 0.0) for r in rows)
    return out


def opts(**on):
    """The run's options with only the named ones on."""
    o = dict(OFF)
    for k in on:
        o[k] = L.BASE_OPTIONS[k]
    return o


STEPS = [
    ("Dashboard alone (the game without supply and demand)", None, False),
    ("Supply-and-demand layer with every limit off", {"neutral": ("boeing", "airbus", "demand", "firm"), "options": opts()}, True),
    ("+ Boeing's real factories", {"neutral": ("airbus", "demand", "firm"), "options": opts()}, True),
    ("+ Airbus's real factories", {"neutral": ("demand", "firm"), "options": opts()}, True),
    ("+ your conservative demand curve (firm orders on top)", {"options": opts(demand_curve=1)}, True),
    ("+ firm orders inside demand (option B)", {"options": opts(demand_curve=1, firm_backlog=1)}, True),
    ("+ Boeing loses 1 point a year after NGSA", {"options": opts(demand_curve=1, firm_backlog=1, boeing_pp_after_ngsa=1)}, True),
    ("+ Airbus's slack goes to Boeing", {"options": opts(demand_curve=1, firm_backlog=1, boeing_pp_after_ngsa=1, boeing_takes_airbus_slack=1)}, True),
    ("+ Airbus adds 1% capacity a year when short (this game)", {}, True),
]

GROUPS = {"boeing": "Boeing's real factories", "airbus": "Airbus's real factories", "demand": "Your demand (curve and firm orders)",
          "rules": "Your share rules (1 point a year, slack floor)", "response": "Airbus's capacity response"}


def group_kw(on):
    neutral = tuple(x for x, g in (("boeing", "boeing"), ("airbus", "airbus"), ("demand", "demand"), ("firm", "demand")) if g not in on)
    o = dict(OFF)
    if "demand" in on:
        o.update({"demand_curve": L.BASE_OPTIONS["demand_curve"], "firm_backlog": L.BASE_OPTIONS["firm_backlog"]})
    if "rules" in on:
        o.update({"boeing_pp_after_ngsa": L.BASE_OPTIONS["boeing_pp_after_ngsa"], "boeing_takes_airbus_slack": L.BASE_OPTIONS["boeing_takes_airbus_slack"]})
    if "response" in on:
        o["airbus_capacity_response"] = L.BASE_OPTIONS["airbus_capacity_response"]
    return {"neutral": neutral, "options": o}


def main():
    out = {"steps": []}
    for lab, kw, on in STEPS:
        m = measure(kw, on)
        out["steps"].append({"step": lab, **m})
        print("%-58s DN %+6.2f  fps R %+6.2f N %+6.2f | item R %+6.2f N %+6.2f | Boeing dlv 2040-59 DN %6.0f R %6.0f (fps %5.0f)" % (
            lab, m["dn"], m["renton"], m["new_site"], m["item_renton"], m["item_new_site"], m["dlv_dn"], m["dlv_renton"], m["fps_renton"]))
    st = out["steps"]
    # checks: the layer with every limit off is the dashboard (new sites; Renton adds only its site saving), and the
    # last step is this game
    assert abs(st[1]["item_new_site"] - st[0]["item_new_site"]) < 1e-9, (st[1]["item_new_site"], st[0]["item_new_site"])
    assert abs(st[1]["dn"] - st[0]["dn"]) < 1e-9
    assert abs(st[-1]["item_renton"] - L.played_item(L.F10, "renton")) < 1e-12
    # Shapley over five groups (Renton and new sites)
    keys = list(GROUPS)
    val = {}
    for r in range(len(keys) + 1):
        for on in itertools.combinations(keys, r):
            m = measure(group_kw(set(on)))
            val[frozenset(on)] = m
    full, none = val[frozenset(keys)], val[frozenset()]
    assert abs(full["item_renton"] - st[-1]["item_renton"]) < 1e-9 and abs(none["item_new_site"] - st[0]["item_new_site"]) < 1e-9
    sh = {}
    for site in ("renton", "new_site"):
        k_ = "item_" + site
        sh[site] = {}
        for c in keys:
            tot = 0.0
            for r in range(len(keys)):
                for Sx in itertools.combinations([x for x in keys if x != c], r):
                    Sx = frozenset(Sx)
                    w = math.factorial(len(Sx)) * math.factorial(len(keys) - len(Sx) - 1) / math.factorial(len(keys))
                    tot += w * (val[Sx | {c}][k_] - val[Sx][k_])
            sh[site][c] = tot
        assert abs(sum(sh[site].values()) - (full[k_] - none[k_])) < 1e-9
    out["shapley"] = {"groups": GROUPS, "shares": sh, "none": {k: none[k] for k in ("dn", "renton", "new_site", "item_renton", "item_new_site")},
                      "full": {k: full[k] for k in ("dn", "renton", "new_site", "item_renton", "item_new_site")},
                      "dn_shares": None}
    # the same split for Do Nothing alone (how much better Do Nothing looks once deliveries are real)
    shd = {}
    for c in keys:
        tot = 0.0
        for r in range(len(keys)):
            for Sx in itertools.combinations([x for x in keys if x != c], r):
                Sx = frozenset(Sx)
                w = math.factorial(len(Sx)) * math.factorial(len(keys) - len(Sx) - 1) / math.factorial(len(keys))
                tot += w * (val[Sx | {c}]["dn"] - val[Sx]["dn"])
        shd[c] = tot
    out["shapley"]["dn_shares"] = shd
    for site in sh:
        print(site, {GROUPS[c]: round(x, 2) for c, x in sh[site].items()})
    print("Do Nothing", {GROUPS[c]: round(x, 2) for c, x in shd.items()})
    # the dashboard-only game as played (dash-2050-obj, round 1 brief): the same decision, its six columns
    g = json.load(open(os.path.join(HERE, "..", "..", "..", "dash-2050-obj", "record", "grids_r1.json")))["boeing"]
    rows = {x["plan"]: [c[0] for c in x["cells"]] for x in g["rows"]}
    out["obj_game_brief"] = {"columns": g["scenarios"], "item_10yr": [a - b for a, b in zip(rows["fps 10-yr + 787: hold"], rows["fps: hold + 787: hold"])],
                             "do_nothing": rows["fps: hold + 787: hold"], "fps_10yr": rows["fps 10-yr + 787: hold"]}
    json.dump(out, open(os.path.join(HERE, "bridge.json"), "w"), indent=1)
    print("wrote bridge.json")


if __name__ == "__main__":
    main()
