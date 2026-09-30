"""Game-theory helpers over the adjudication model.

stage_game: this turn's simultaneous orders, assuming nobody moves afterwards.
plan_game:  full plans (which program launches in which turn, which tactics)
            from a given turn to the end of the game, in normal form.
Payoffs are full-game delta PV ($B) from model.evaluate.
"""

from __future__ import annotations

import itertools

from .model import (SIDES, SUPPLIERS, active_suppliers, build_world, empty_orders, jv_partner_player, other, payoff,
                    players, programs_of, supplier_requirement, tactic_enabled, turn_years)


def _launch_entry(cfg, pid, year, variant=None):
    pc = cfg["programs"][pid]
    e = {"program": pid, "year": year, "engine": pc["default_engine"]}
    if "variants" in pc:
        e["variant"] = variant or pc["default_variant"]
    return e


def describe_orders(cfg, side, o):
    parts = []
    for L in o.get("launch", []):
        bits = [x for x in (L.get("variant"), L.get("terms") if side in SUPPLIERS else None) if x]
        eng = ""
        if side in SIDES and L.get("engine") and L["engine"] != cfg["programs"][L["program"]]["default_engine"]:
            eng = f" with {L['engine']}"
        parts.append(f"launch {L['program']}{' (' + ', '.join(bits) + ')' if bits else ''}{eng}")
    for pid in o.get("cancel", []):
        parts.append(f"cancel {pid}")
    for flag, label in (("rate_increase", "rate increase"), ("delay_tactics", "Delay Tactics"), ("poaching", "Poaching"),
                        ("t1000_upgrade", "Trent 1000 upgrade"), ("gtf_upgrade", "GTF durability upgrade"),
                        ("join_rr_jv", "join the Rolls-Royce UltraFan Joint Venture")):
        if o.get(flag):
            parts.append(label)
    return " + ".join(parts) if parts else "no new moves"


def _nash(n_rows, n_cols, cell, tol, eps):
    """Pure and eps-near Nash cells of a bimatrix given cell(i, j) -> (row_payoff, col_payoff)."""
    best_row_for_col = [max(cell(i, j)[0] for i in range(n_rows)) for j in range(n_cols)]
    best_col_for_row = [max(cell(i, j)[1] for j in range(n_cols)) for i in range(n_rows)]
    pure, near = [], []
    for i in range(n_rows):
        for j in range(n_cols):
            u = cell(i, j)
            gap_r, gap_c = best_row_for_col[j] - u[0], best_col_for_row[i] - u[1]
            if gap_r <= tol and gap_c <= tol:
                pure.append((i, j, gap_r, gap_c))
            elif gap_r <= eps and gap_c <= eps:
                near.append((i, j, gap_r, gap_c))
    return pure, near, best_row_for_col, best_col_for_row


# ---------------------------------------------------------------------------
# Stage game (this turn only)
# ---------------------------------------------------------------------------

def supplier_candidates(cfg, world, sup, turn):
    """A supplier's orders for this turn: each engine program x variant x terms, cancels, Trent 1000 upgrade."""
    a, _ = turn_years(cfg, turn)
    scfg = cfg["suppliers"][sup]
    per_prog = []
    for spid, spc in scfg["programs"].items():
        opts = [None]
        sp = world.sup_programs.get(spid)
        if sp is None:
            for v in (spc["variants"] if "variants" in spc else [None]):
                opts += [("launch", v, t) for t in scfg["terms"]]
        elif sp.live() and sp.ready > a and not any(p.supplier_program == spid and p.cancelled_year is None
                                                    for p in world.programs.values()):
            opts.append(("cancel", None, None))
        per_prog.append((spid, opts))
    # The one-time upgrade is a candidate while unused. Joining a partner's Joint Venture is left out:
    # alone it does nothing, so the partner's own options model it (see supplier_stage).
    up = scfg.get("upgrade")
    flags = [(up["flag"], [False, True])] if up and sup not in world.upgrade_years else []
    cands = []
    for combo in itertools.product(*[opts for _, opts in per_prog]):
        for fl in itertools.product(*[vals for _, vals in flags]):
            o = empty_orders(sup)
            for (spid, _), act in zip(per_prog, combo):
                if act is None:
                    continue
                if act[0] == "launch":
                    e = {"program": spid, "year": a, "terms": act[2]}
                    if act[1]:
                        e["variant"] = act[1]
                    o["launch"].append(e)
                else:
                    o["cancel"].append(spid)
            for (name, _), v in zip(flags, fl):
                o[name] = v
            cands.append(o)
    return cands


def stage_candidates(cfg, world, side, turn):
    if side in SUPPLIERS:
        return supplier_candidates(cfg, world, side, turn)
    a, _ = turn_years(cfg, turn)
    per_prog = []
    for pid in programs_of(cfg, side):
        pc = cfg["programs"][pid]
        opts = [None]
        if pid not in world.programs:
            opts += [("launch", v) for v in pc["variants"]] if "variants" in pc else [("launch", None)]
        else:
            p = world.programs[pid]
            if p.cancelled_year is None and p.eis > a:
                opts.append(("cancel", None))
        per_prog.append((pid, opts))
    flags = []
    if side == "boeing":
        if world.rate_year is None and tactic_enabled(cfg, "rate_increase"):
            flags.append(("rate_increase", [False, True]))
    else:
        flags += [(f, [False, True]) for f in ("delay_tactics", "poaching") if tactic_enabled(cfg, f)]
    cands = []
    for combo in itertools.product(*[opts for _, opts in per_prog]):
        for fl in itertools.product(*[vals for _, vals in flags]):
            o = empty_orders(side)
            for (pid, _), act in zip(per_prog, combo):
                if act is None:
                    continue
                if act[0] == "launch":
                    o["launch"].append(_launch_entry(cfg, pid, a, act[1]))
                else:
                    o["cancel"].append(pid)
            for (name, _), v in zip(flags, fl):
                o[name] = v
            cands.append(o)
    return cands


def stage_game(cfg, history, turn, pending_injects, viewer_mask=frozenset(), market=None):
    """Enumerate both sides' orders for `turn`; no moves after this turn."""
    base = history + [{"turn": turn, "injects": list(pending_injects), "orders": {}, "market": {}}]
    world0 = build_world(cfg, base, viewer_mask)
    cands = {s: stage_candidates(cfg, world0, s, turn) for s in SIDES}
    B, A = cands["boeing"], cands["airbus"]
    table = {}
    for i, ob in enumerate(B):
        for j, oa in enumerate(A):
            rec = {"turn": turn, "injects": list(pending_injects), "orders": {"boeing": ob, "airbus": oa},
                   "market": market or {}}
            u = payoff(cfg, history + [rec], viewer_mask)
            table[(i, j)] = (u["boeing"], u["airbus"])
    eq = cfg["equilibrium"]
    pure, near, br_b, br_a = _nash(len(B), len(A), lambda i, j: table[(i, j)], eq["pure_tol_b"], eq["near_eps_b"])
    return {"cands": cands, "table": table, "pure": pure, "near": near, "best_b": br_b, "best_a": br_a}


def stage_report(cfg, sg, side, compact=False):
    """Render a stage game from `side`'s perspective (side may be 'control')."""
    B, A, T = sg["cands"]["boeing"], sg["cands"]["airbus"], sg["table"]
    ids = {"boeing": [f"B{i + 1}" for i in range(len(B))], "airbus": [f"A{j + 1}" for j in range(len(A))]}
    idle = {"boeing": 0, "airbus": 0}  # index 0 is always "no new moves"

    def u(s, i, j):
        return T[(i, j)][0 if s == "boeing" else 1]

    def opts(s):
        mine, theirs = (B, A) if s == "boeing" else (A, B)
        rows = []
        for i, o in enumerate(mine):
            cells = [(u(s, i, j) if s == "boeing" else u(s, j, i)) for j in range(len(theirs))]
            # opponent's best response to this option
            if s == "boeing":
                br = max(range(len(A)), key=lambda j: T[(i, j)][1])
                vs_br = T[(i, br)][0]
            else:
                br = max(range(len(B)), key=lambda j: T[(j, i)][0])
                vs_br = T[(br, i)][1]
            rows.append({
                "id": ids[s][i], "label": describe_orders(cfg, s, o), "orders": o,
                "vs_opponent_no_new_moves": round(cells[idle[other(s)]], 3),
                "vs_opponent_best_response": round(vs_br, 3),
                "opponent_best_response": ids[other(s)][br],
                "worst_case": round(min(cells), 3), "best_case": round(max(cells), 3),
            })
        rows.sort(key=lambda r: -r["vs_opponent_best_response"])
        return rows

    def label(s, idx):
        return {"id": ids[s][idx], "label": describe_orders(cfg, s, (B if s == "boeing" else A)[idx])}

    sup_txt = (f" Active supplier(s) ({', '.join(active_suppliers(cfg))}) make no new moves this turn, so an engine a supplier "
               "has not yet committed to falls back to the segment's alternative; use whatif with supplier orders to test a commitment."
               if active_suppliers(cfg) else "")
    out = {
        "assumption": "Stage game: both sides choose this turn's orders simultaneously and nobody moves after this turn. "
                      "Payoffs are full-game delta PV ($B, PV to the scenario base year) versus the status quo. Launch year = first year of the turn, "
                      "default engine and variant; use whatif to test other years or engines." + sup_txt,
        "pure_nash": [{"boeing": label("boeing", i), "airbus": label("airbus", j),
                       "payoffs_b": {"boeing": round(T[(i, j)][0], 3), "airbus": round(T[(i, j)][1], 3)}}
                      for (i, j, _, _) in sg["pure"]],
        "near_nash_count": len(sg["near"]),
        "near_nash_eps_b": cfg["equilibrium"]["near_eps_b"],
    }
    near = sorted(sg["near"], key=lambda c: max(c[2], c[3]))[:8]
    out["near_nash_top"] = [{"boeing": label("boeing", i), "airbus": label("airbus", j),
                             "payoffs_b": {"boeing": round(T[(i, j)][0], 3), "airbus": round(T[(i, j)][1], 3)},
                             "max_gap_b": round(max(gr, gc), 3)} for (i, j, gr, gc) in near]
    if side in SIDES:
        out["your_options"] = opts(side)
        out["opponent_options"] = [{"id": ids[other(side)][k], "label": describe_orders(cfg, other(side), o)}
                                   for k, o in enumerate(A if side == "boeing" else B)]
    else:
        out["boeing_options"] = opts("boeing")
        out["airbus_options"] = opts("airbus")
    if not compact:
        out["matrix_b"] = {
            "rows": "boeing options (B*)", "cols": "airbus options (A*)", "cell": "[boeing, airbus]",
            "cells": [[[round(T[(i, j)][0], 2), round(T[(i, j)][1], 2)] for j in range(len(A))] for i in range(len(B))],
        }
    return out


def _non_supplier_engine(cfg, pid, sup):
    pc = cfg["programs"][pid]
    seg = pc["segment"]
    eng = pc["default_engine"]
    req = supplier_requirement(cfg, seg, eng)
    return cfg["suppliers"][sup]["fallback_engine"][seg] if (req and req[0] == sup) else eng


def _supplier_engine(cfg, pid, sup):
    seg = cfg["programs"][pid]["segment"]
    for spid, spc in cfg["suppliers"][sup]["programs"].items():
        if spc["segment"] == seg:
            return spid, spc["engine_option"]
    return None, None


def supplier_stage(cfg, history, turn, pending_injects, sup, viewer_mask=frozenset(), market=None):
    """The supplier's options this turn against a set of airframer engine-selection scenarios.

    Airframer scenarios: nobody launches; each airframe program not yet launched launches
    this turn with the supplier's engine or with the alternative (one program at a time);
    all of them with the supplier's engine; all with the alternative. The airframers'
    other orders are "no new moves". For each supplier launch option the report also
    gives each airframer's incentive: its payoff with the supplier's engine minus with
    the alternative, if it launched that program this turn.
    """
    a, _ = turn_years(cfg, turn)
    base = history + [{"turn": turn, "injects": list(pending_injects), "orders": {}, "market": {}}]
    world0 = build_world(cfg, base, viewer_mask)
    cands = supplier_candidates(cfg, world0, sup, turn)
    open_progs = [pid for pid, pc in cfg["programs"].items() if pid not in world0.programs
                  and _supplier_engine(cfg, pid, sup)[0] is not None]

    def launch(pid, eng):
        pc = cfg["programs"][pid]
        e = {"program": pid, "year": a, "engine": eng}
        if "variants" in pc:
            e["variant"] = pc["default_variant"]
        return e

    scen = [("nobody launches", {})]
    for pid in open_progs:
        scen.append((f"{pid} with {_supplier_engine(cfg, pid, sup)[1]}", {pid: _supplier_engine(cfg, pid, sup)[1]}))
        scen.append((f"{pid} with {_non_supplier_engine(cfg, pid, sup)}", {pid: _non_supplier_engine(cfg, pid, sup)}))
    if len(open_progs) > 1:
        scen.append(("all open programs with your engines", {pid: _supplier_engine(cfg, pid, sup)[1] for pid in open_progs}))
        scen.append(("all open programs with the alternatives", {pid: _non_supplier_engine(cfg, pid, sup) for pid in open_progs}))

    def hist_for(o_sup, picks):
        orders = {s: empty_orders(s) for s in SIDES}
        for pid, eng in picks.items():
            orders[cfg["programs"][pid]["owner"]]["launch"].append(launch(pid, eng))
        orders[sup] = o_sup
        for s in active_suppliers(cfg):
            orders.setdefault(s, empty_orders(s))
        for L in o_sup.get("launch", []):  # a Joint Venture option assumes its partner player joins
            partner = jv_partner_player(cfg, sup, L["program"], L.get("variant"))
            if partner:
                orders[partner] = dict(orders[partner], **{cfg["suppliers"][partner]["jv"]["flag"]: True})
        return history + [{"turn": turn, "injects": list(pending_injects), "orders": orders, "market": market or {}}]

    rows = []
    for i, o in enumerate(cands):
        vals = [payoff(cfg, hist_for(o, picks), viewer_mask)[sup] for _, picks in scen]
        incent = {}
        for pid in open_progs:
            spid, eng = _supplier_engine(cfg, pid, sup)
            if not any(L["program"] == spid for L in o["launch"]) and spid not in world0.sup_programs:
                continue
            owner = cfg["programs"][pid]["owner"]
            u_rr = payoff(cfg, hist_for(o, {pid: eng}), viewer_mask)[owner]
            u_alt = payoff(cfg, hist_for(o, {pid: _non_supplier_engine(cfg, pid, sup)}), viewer_mask)[owner]
            incent[pid] = round(u_rr - u_alt, 3)
        rows.append({"id": f"R{i + 1}", "label": describe_orders(cfg, sup, o), "orders": o,
                     "by_scenario_b": {name: round(v, 3) for (name, _), v in zip(scen, vals)},
                     "worst_case": round(min(vals), 3), "best_case": round(max(vals), 3),
                     "airframer_incentive_b": incent})
    rows.sort(key=lambda r: -r["best_case"])
    return {
        "assumption": ("Your options this turn against airframer engine-selection scenarios (launch in the first year of the "
                       "turn, default variants; airframers' other orders are no new moves; nobody moves after this turn; "
                       "other suppliers make no new moves, except that a Joint Venture option assumes its partner joins). "
                       "Values are your full-game delta PV ($B, PV to the scenario base year at your WACC) versus the status quo. "
                       "airframer_incentive_b: that airframer's payoff with your engine minus with the alternative engine "
                       "(positive = it prefers yours), given your option's terms."),
        "scenarios": [name for name, _ in scen],
        "open_airframe_programs": open_progs,
        "your_options": rows,
    }


# ---------------------------------------------------------------------------
# Plan game (normal form over the rest of the game)
# ---------------------------------------------------------------------------

def plan_space(cfg, side, base_world, turns, segment):
    per_prog = []
    for pid in programs_of(cfg, side):
        pc = cfg["programs"][pid]
        if segment != "all" and pc["segment"] != segment:
            continue
        if pid in base_world.programs:
            continue
        opts = [None]
        for t in turns:
            opts += [(t, v) for v in pc["variants"]] if "variants" in pc else [(t, None)]
        per_prog.append((pid, opts))
    flag_opts = []
    if segment == "all":
        if side == "boeing" and base_world.rate_year is None and tactic_enabled(cfg, "rate_increase"):
            flag_opts.append(("rate_increase", [None] + list(turns)))
        if side == "airbus":
            flag_opts += [(f, [False, True]) for f in ("delay_tactics", "poaching") if tactic_enabled(cfg, f)]
    plans = []
    for combo in itertools.product(*[o for _, o in per_prog]):
        for fl in itertools.product(*[v for _, v in flag_opts]):
            plans.append({
                "launch": {pid: c for (pid, _), c in zip(per_prog, combo) if c is not None},
                "flags": {name: v for (name, _), v in zip(flag_opts, fl)},
            })
    return plans


def describe_plan(cfg, plan, restricted):
    parts = []
    for pid, (t, v) in sorted(plan["launch"].items(), key=lambda kv: kv[1][0]):
        parts.append(f"{pid}{' ' + v if v else ''} T{t}")
    fl = plan["flags"]
    if fl.get("rate_increase"):
        parts.append(f"rate increase T{fl['rate_increase']}")
    if fl.get("delay_tactics"):
        parts.append("Delay Tactics every turn")
    if fl.get("poaching"):
        parts.append("Poaching every turn")
    txt = ", ".join(parts) if parts else "no launches"
    return txt + (" (other moves held fixed)" if restricted else "")


def _plan_orders(cfg, side, plan, turn, base_orders, segment):
    """Orders for `side` in `turn` under `plan`.

    base_orders: the orders that side actually gave in this turn (or None). For a
    segment-restricted game the plan only replaces that segment's launches and
    cancels; everything else is kept as played.
    """
    a, _ = turn_years(cfg, turn)
    if segment == "all" or base_orders is None:
        o = empty_orders(side)
    else:
        o = {k: (list(v) if isinstance(v, list) else v) for k, v in base_orders.items()}
        o["launch"] = [L for L in o["launch"] if cfg["programs"][L["program"]]["segment"] != segment]
        o["cancel"] = [p for p in o["cancel"] if cfg["programs"][p]["segment"] != segment]
    for pid, (t, v) in plan["launch"].items():
        if t == turn:
            o["launch"].append(_launch_entry(cfg, pid, a, v))
    fl = plan["flags"]
    if segment == "all":
        if side == "boeing":
            o["rate_increase"] = fl.get("rate_increase") == turn
        else:
            o["delay_tactics"] = bool(fl.get("delay_tactics"))
            o["poaching"] = bool(fl.get("poaching"))
    o["launch"].sort(key=lambda e: e["program"])
    return o


def plan_game(cfg, state_history, from_turn, turns_total, current_turn, pending_injects,
              segment="all", viewer_mask=frozenset()):
    """Normal-form game over plans for turns from_turn..turns_total.

    Turns already adjudicated keep their recorded injects and market reactions;
    the current turn uses its pending injects; later turns have none.
    """
    before = [r for r in state_history if r["turn"] < from_turn]
    recorded = {r["turn"]: r for r in state_history}
    turns = list(range(from_turn, turns_total + 1))
    frame = []
    for t in turns:
        if t in recorded:
            frame.append({"turn": t, "injects": list(recorded[t].get("injects", [])), "market": recorded[t].get("market", {}),
                          "actual": recorded[t]["orders"]})
        elif t == current_turn:
            frame.append({"turn": t, "injects": list(pending_injects), "market": {}, "actual": None})
        else:
            frame.append({"turn": t, "injects": [], "market": {}, "actual": None})
    base_world = build_world(cfg, before, viewer_mask)
    plans = {s: plan_space(cfg, s, base_world, turns, segment) for s in SIDES}

    def history_for(plan_b, plan_a):
        h = list(before)
        for f in frame:
            act = f["actual"] or {}
            ob = act.get("boeing") if plan_b is None else _plan_orders(cfg, "boeing", plan_b, f["turn"], act.get("boeing"), segment)
            oa = act.get("airbus") if plan_a is None else _plan_orders(cfg, "airbus", plan_a, f["turn"], act.get("airbus"), segment)
            orders = {"boeing": ob or empty_orders("boeing"), "airbus": oa or empty_orders("airbus")}
            for sup in active_suppliers(cfg):  # suppliers keep their recorded orders; none in unplayed turns
                orders[sup] = act.get(sup) or empty_orders(sup)
            h.append({"turn": f["turn"], "injects": f["injects"], "market": f["market"], "orders": orders})
        return h

    PB, PA = plans["boeing"], plans["airbus"]
    table = {}
    for i, pb in enumerate(PB):
        for j, pa in enumerate(PA):
            u = payoff(cfg, history_for(pb, pa), viewer_mask)
            table[(i, j)] = (u["boeing"], u["airbus"])
    eq = cfg["equilibrium"]
    pure, near, br_b, br_a = _nash(len(PB), len(PA), lambda i, j: table[(i, j)], eq["pure_tol_b"], eq["near_eps_b"])
    restricted = segment != "all"

    def lab(s, idx):
        return describe_plan(cfg, (PB if s == "boeing" else PA)[idx], restricted)

    def cell(i, j):
        return {"boeing_plan": lab("boeing", i), "airbus_plan": lab("airbus", j),
                "payoffs_b": {"boeing": round(table[(i, j)][0], 3), "airbus": round(table[(i, j)][1], 3)}}

    maximin = {}
    dominant = {}
    for s, n_own, n_opp in (("boeing", len(PB), len(PA)), ("airbus", len(PA), len(PB))):
        def val(own, opp, s=s):
            return table[(own, opp)][0] if s == "boeing" else table[(opp, own)][1]
        mm = max(range(n_own), key=lambda k: min(val(k, o) for o in range(n_opp)))
        maximin[s] = {"plan": lab(s, mm), "guaranteed_b": round(min(val(mm, o) for o in range(n_opp)), 3)}
        dom = [k for k in range(n_own) if all(val(k, o) >= max(val(x, o) for x in range(n_own)) - eq["pure_tol_b"] for o in range(n_opp))]
        dominant[s] = [lab(s, k) for k in dom]

    out = {
        "from_turn": from_turn, "turns": turns, "segment": segment,
        "plan_counts": {"boeing": len(PB), "airbus": len(PA)},
        "assumption": ("Normal-form game over plans for the remaining turns (launch turn per program, tactics on/off for "
                       "every remaining turn, default engines, launch in the first year of a turn). Adjudicated turns keep "
                       "their recorded injects and market reactions. Payoffs: full-game delta PV ($B, PV to the scenario base year)."
                       + (" Supplier orders are held at their recorded values (no new supplier moves in unplayed turns)."
                          if active_suppliers(cfg) else "")),
        "pure_nash": [cell(i, j) for (i, j, _, _) in pure],
        "near_nash_count": len(near),
        "near_nash_eps_b": eq["near_eps_b"],
        "near_nash_top": [dict(cell(i, j), max_gap_b=round(max(gr, gc), 3))
                          for (i, j, gr, gc) in sorted(near, key=lambda c: max(c[2], c[3]))[:10]],
        "dominant_plans": dominant,
        "maximin": maximin,
    }
    if segment != "all" and len(PB) * len(PA) <= 100:
        out["matrix"] = {"rows": [lab("boeing", i) for i in range(len(PB))],
                         "cols": [lab("airbus", j) for j in range(len(PA))],
                         "cells_b": [[[round(table[(i, j)][0], 3), round(table[(i, j)][1], 3)] for j in range(len(PA))]
                                     for i in range(len(PB))]}
    if all(f["actual"] is not None for f in frame):
        act = payoff(cfg, history_for(None, None), viewer_mask)
        out["actual_play"] = {s: round(act[s], 3) for s in SIDES}
        regret = {}
        for s in SIDES:
            own = PB if s == "boeing" else PA
            best_k, best_v = None, None
            for k, p in enumerate(own):
                u = payoff(cfg, history_for(p, None) if s == "boeing" else history_for(None, p), viewer_mask)[s]
                if best_v is None or u > best_v:
                    best_k, best_v = k, u
            regret[s] = {"best_response_to_opponents_actual_play": lab(s, best_k),
                         "best_response_payoff_b": round(best_v, 3),
                         "regret_b": round(best_v - act[s], 3)}
        out["regret_vs_actual"] = regret
    return out


# ---------------------------------------------------------------------------
# Referee scorecard (player efficiency)
# ---------------------------------------------------------------------------

def _supplier_prediction_score(cfg, prediction, actual_orders):
    """A supplier's forecast of both airframers: launch yes/no and, for launches, which engine."""
    if not isinstance(prediction, dict):
        return None
    hits = total = 0
    for side in SIDES:
        pred = prediction.get(side)
        if not isinstance(pred, dict):
            continue
        act = actual_orders.get(side) or {}
        pl = {}
        for L in pred.get("launch", []) or []:
            if isinstance(L, str):
                pl[L] = None
            elif isinstance(L, dict) and L.get("program"):
                pl[L["program"]] = L.get("engine")
        al = {L["program"]: L.get("engine") for L in act.get("launch", [])}
        for pid in programs_of(cfg, side):
            total += 1
            hits += (pid in pl) == (pid in al)
            if pid in pl and pid in al and pl[pid]:
                total += 1
                hits += pl[pid] == al[pid]
    return round(hits / total, 3) if total else None


def _prediction_score(cfg, predictor, prediction, actual):
    """Share of the rival's decisions this turn that the predictor called right.

    Decisions scored: launch yes/no for each rival program not launched before,
    cancel yes/no for each rival program, and each rival flag.
    """
    rival = other(predictor)
    if not isinstance(prediction, dict):
        return None
    pl = {(L if isinstance(L, str) else L.get("program")) for L in prediction.get("launch", []) or []}
    al = {L["program"] for L in actual.get("launch", [])}
    pc, ac = set(prediction.get("cancel", []) or []), set(actual.get("cancel", []))
    flags = ("rate_increase",) if rival == "boeing" else ("delay_tactics", "poaching")
    hits = total = 0
    for pid in programs_of(cfg, rival):
        total += 2
        hits += (pid in pl) == (pid in al)
        hits += (pid in pc) == (pid in ac)
    for f in flags:
        if f in prediction:
            total += 1
            hits += bool(prediction.get(f)) == bool(actual.get(f))
    return round(hits / total, 3) if total else None


def turn_scorecard(cfg, history):
    """Per turn and side: value captured against the rival's ACTUAL orders that turn.

    Myopic by construction (no moves after the scored turn), like the stage game the
    players see. capture = (actual - worst) / (best - worst) over the stage candidates
    plus the actual orders; regret = best - actual.
    """
    rows = []
    for idx, rec in enumerate(history):
        k = rec["turn"]
        before = history[:idx]
        w0 = build_world(cfg, before + [{"turn": k, "injects": rec.get("injects", []), "orders": {}, "market": {}}])
        proj = rec.get("projection") or {}
        stm = rec.get("statements") or {}
        for side in players(cfg):
            def val(o, side=side):
                r = {"turn": k, "injects": rec.get("injects", []), "market": rec.get("market", {}),
                     "orders": dict(rec["orders"], **{side: o})}
                return payoff(cfg, before + [r])[side]

            cands = stage_candidates(cfg, w0, side, k)
            vals = [(val(o), o) for o in cands]
            actual = val(rec["orders"][side])
            best_v, best_o = max(vals, key=lambda x: x[0])
            if actual > best_v:
                best_v, best_o = actual, rec["orders"][side]
            worst = min([v for v, _ in vals] + [actual])
            exp = stm.get(side, {}).get("expected_delta_pv_b")
            realised = (proj.get(side) or {}).get("delta_pv_b")
            rows.append({
                "turn": k, "side": side,
                "orders": describe_orders(cfg, side, rec["orders"][side]),
                "myopic_value_b": round(actual, 3),
                "best_response": describe_orders(cfg, side, best_o),
                "best_response_value_b": round(best_v, 3),
                "regret_b": round(best_v - actual, 3),
                "capture": round((actual - worst) / (best_v - worst), 3) if best_v > worst else 1.0,
                "prediction_accuracy": (_supplier_prediction_score(cfg, stm.get(side, {}).get("prediction"), rec["orders"])
                                        if side in SUPPLIERS else
                                        _prediction_score(cfg, side, stm.get(side, {}).get("prediction"), rec["orders"][other(side)])),
                "expected_delta_pv_b": exp,
                "projection_after_turn_b": realised,
                "expectation_error_b": round(realised - exp, 3) if (exp is not None and realised is not None) else None,
                "disclosures": len(stm.get(side, {}).get("disclose", []) or []),
            })
    summary = {}
    for side in players(cfg):
        rs = [r for r in rows if r["side"] == side]
        preds = [r["prediction_accuracy"] for r in rs if r["prediction_accuracy"] is not None]
        errs = [abs(r["expectation_error_b"]) for r in rs if r["expectation_error_b"] is not None]
        summary[side] = {
            "turns": len(rs),
            "mean_capture": round(sum(r["capture"] for r in rs) / len(rs), 3) if rs else None,
            "total_myopic_regret_b": round(sum(r["regret_b"] for r in rs), 3),
            "mean_prediction_accuracy": round(sum(preds) / len(preds), 3) if preds else None,
            "mean_abs_expectation_error_b": round(sum(errs) / len(errs), 3) if errs else None,
            "disclosures": sum(r["disclosures"] for r in rs),
        }
    return {"rows": rows, "summary": summary,
            "method": ("capture and regret score each turn's orders against the other players' actual orders that turn, "
                       "assuming no later moves (the players' stage-game view). prediction_accuracy scores the "
                       "player's forecast of the rival's launches, cancels and flags (a supplier: each airframer's "
                       "launches and engine choices). expectation_error = engine projection after adjudication minus "
                       "the player's expected_delta_pv_b.")}
