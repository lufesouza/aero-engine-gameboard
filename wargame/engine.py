"""Command-line interface for the Boeing vs Airbus war game.

    python3 -m wargame.engine <command> [options]

Every command prints JSON (except `report --format md`). Commands that take
orders read a JSON object on stdin. Only `new`, `inject`, `adjudicate` and
`rollback` change a run; they are the control cell's commands. Everything
else is read-only and safe for the player agents.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys

from . import model as M
from . import solver as S

RUNS_DIR = os.environ.get("WARGAME_RUNS_DIR", os.path.join(M.HERE, "runs"))
VIEWERS = ("boeing", "airbus", "rolls_royce", "pratt_whitney", "market", "control", "analyst")
ORDER_SIDES = M.SIDES + M.SUPPLIERS


class GameError(Exception):
    pass


# ---------------------------------------------------------------------------
# Run state
# ---------------------------------------------------------------------------

def run_dir(run_id):
    if not run_id or "/" in run_id or run_id.startswith("."):
        raise GameError(f"invalid run id {run_id!r}")
    return os.path.join(RUNS_DIR, run_id)


def load_state(run_id):
    path = os.path.join(run_dir(run_id), "state.json")
    if not os.path.exists(path):
        raise GameError(f"run '{run_id}' not found under {RUNS_DIR}")
    with open(path) as f:
        return json.load(f)


def save_state(st):
    d = run_dir(st["run_id"])
    os.makedirs(os.path.join(d, "turns"), exist_ok=True)
    tmp = os.path.join(d, "state.json.tmp")
    with open(tmp, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, os.path.join(d, "state.json"))


def pending_record(st):
    if st["status"] == "complete":
        return []
    return [{"turn": st["current_turn"], "injects": list(st["pending_injects"]), "orders": {}, "market": {}}]


def read_stdin_json():
    raw = sys.stdin.read()
    if not raw.strip():
        raise GameError("expected a JSON object on stdin")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise GameError(f"stdin is not valid JSON: {e}")


def out(obj):
    print(json.dumps(obj, indent=1))


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def public_programs(cfg, world_actual, year):
    dt = cfg["tactics"]["delay_tactics"]
    exposed = world_actual.exposure_year is not None and world_actual.exposure_year <= year
    rows = []
    for pid, p in world_actual.programs.items():
        pc = cfg["programs"][pid]
        rows.append({
            "side": p.owner, "program": pid, "label": pc["label"], "segment": p.segment,
            "launch_year": p.launch_year, "variant": p.variant, "engine": p.engine,
            "engine_label": cfg["engine_options"][p.segment][p.engine]["label"],
            **({"engine_requested": p.engine_requested} if p.engine_requested else {}),
            **({"engine_supplier": p.supplier, "waits_for_engine_years": p.engine_wait} if p.supplier else {}),
            "eis": None if p.cancelled_year is not None else p.eis, "status": p.status(year),
            "cancelled_year": p.cancelled_year,
            "slips": [{"turn": s["turn"], "years": s["years"],
                       "cause": dt["public_cause_unexposed"] if (s["covert"] and not exposed) else s["cause"]}
                      for s in p.slips],
            "market_capture_mult": round(p.capture_mult, 3),
        })
    return rows


def public_supplier_programs(cfg, world_actual):
    """Supplier engine programs: public commitments (launch, terms, readiness, users)."""
    rows = []
    for spid, sp in world_actual.sup_programs.items():
        scfg = cfg["suppliers"][sp.owner]
        rows.append({"supplier": sp.owner, "program": spid, "label": scfg["programs"][spid]["label"],
                     "engine_option": scfg["programs"][spid]["engine_option"], "segment": sp.segment,
                     **({"joint_venture_partner": sp.partner} if sp.partner else {}),
                     "launch_year": sp.launch_year, "variant": sp.variant, "terms": sp.terms,
                     "airframer_margin_pp": scfg["terms"][sp.terms]["airframer_margin_pp"],
                     "ready": sp.ready if sp.live() else None, "cancelled_year": sp.cancelled_year,
                     "selected_by": [p.pid for p in world_actual.programs.values() if p.supplier_program == spid and p.cancelled_year is None],
                     "slips": sp.slips})
    return rows


def engine_dates(cfg, seg):
    """Engines that cannot enter service before a given year (available_eis)."""
    return {eng: (f"cannot enter service before {o['available_eis']}; an airframe ready earlier waits for it "
                  "(extension capex for each waiting year).")
            for eng, o in cfg["engine_options"][seg].items() if o.get("available_eis") is not None}


def engine_availability(cfg, world, seg):
    """For airframers: which engines need a supplier commitment, and its status."""
    out = {}
    for eng in cfg["engine_options"][seg]:
        req = M.supplier_requirement(cfg, seg, eng)
        if not req:
            continue
        sp = world.sup_programs.get(req[1])
        scfg = cfg["suppliers"][req[0]]
        if sp is None or not sp.live():
            out[eng] = (f"needs {scfg['label']} to launch {req[1]}; not committed"
                        f"{' (cancelled)' if sp else ''}. Falls back to {scfg['fallback_engine'][seg]} if it is still "
                        "uncommitted when orders are adjudicated.")
        else:
            out[eng] = (f"committed by {scfg['label']} in {sp.launch_year} on {sp.terms} terms "
                        f"({scfg['terms'][sp.terms]['airframer_margin_pp']:+.1f} pp margin to you); ready {sp.ready}.")
    return out


def supplier_levers(cfg, world, sup, turn):
    a, b = M.turn_years(cfg, turn)
    scfg = cfg["suppliers"][sup]
    lv = {"launch": [], "cancel": [], "flags": [], "terms": scfg["terms"]}
    for spid, spc in scfg["programs"].items():
        sp = world.sup_programs.get(spid)
        if sp is None:
            item = {"program": spid, "label": spc["label"], "segment": spc["segment"], "engine_option": spc["engine_option"],
                    "years": [a, b], "dev_years": spc["dev_years"], "capex_b": spc["capex_b"],
                    "value_m_per_engine": spc["value_m_per_engine"],
                    "airframe_programs_that_can_use_it": [pid for pid, pc in cfg["programs"].items()
                                                          if pc["segment"] == spc["segment"]]}
            if "variants" in spc:
                item["variants"] = list(spc["variants"])
                item["variant_terms"] = {v: {k: x for k, x in vt.items() if k != "label"} for v, vt in spc["variants"].items()}
            lv["launch"].append(item)
        elif sp.live() and sp.ready > a:
            users = [p.pid for p in world.programs.values() if p.supplier_program == spid and p.cancelled_year is None]
            lv["cancel"].append({"program": spid, "label": spc["label"], "ready": sp.ready,
                                 "available": not users, "note": f"flown by {', '.join(users)}: cannot cancel" if users else "no airframe uses it"})
    up = scfg.get("upgrade")
    if up:
        done = world.upgrade_years.get(sup)
        lv["flags"].append({"flag": up["flag"], "label": up["label"], "available": done is None,
                            "note": "one-time commitment" if done is None else f"already committed in {done}"})
    jv = scfg.get("jv")
    if jv:
        owner = jv["partner_of"]
        ok = owner in M.active_suppliers(cfg) and jv["program"] not in world.sup_programs
        ocfg = cfg["suppliers"][owner]
        lv["flags"].append({
            "flag": jv["flag"], "available": ok,
            "label": f"join the {ocfg['label']} {ocfg['programs'][jv['program']]['label']} Joint Venture",
            "note": (f"takes effect only if {ocfg['label']} launches {jv['program']} as '{jv['variant']}' in the same turn; you then pay "
                     f"{M.sparam(cfg, owner, jv['program'], jv['variant'], 'capex_share_partner', 0.0):.0%} of the capex and earn "
                     f"{M.sparam(cfg, owner, jv['program'], jv['variant'], 'value_share_partner', 0.0):.0%} of the engine's value")
                    if ok else (f"{ocfg['label']} is not a player in this run" if owner not in M.active_suppliers(cfg)
                                else "that engine was already launched"),
        })
    tmpl = M.empty_orders(sup)
    tmpl.update({"public_statement": "", "rationale": ""})
    lv["orders_template"] = tmpl
    return lv


def levers(cfg, world, side, turn):
    if side in M.SUPPLIERS:
        return supplier_levers(cfg, world, side, turn)
    a, b = M.turn_years(cfg, turn)
    lv = {"launch": [], "cancel": [], "flags": []}
    for pid in M.programs_of(cfg, side):
        pc = cfg["programs"][pid]
        if pid not in world.programs:
            item = {"program": pid, "label": pc["label"], "years": [a, b], "dev_years": pc.get("dev_years", 0) + world.dev_years_add[side],
                    "engines": list(cfg["engine_options"][pc["segment"]]), "default_engine": pc["default_engine"]}
            avail = engine_availability(cfg, world, pc["segment"])
            if avail:
                item["supplier_engines"] = avail
            dates = engine_dates(cfg, pc["segment"])
            if dates:
                item["engine_dates"] = dates
            if "variants" in pc:
                item["variants"] = list(pc["variants"])
                item["variant_terms"] = {v: {k: x for k, x in vt.items() if k != "label"} for v, vt in pc["variants"].items()}
            lv["launch"].append(item)
        else:
            p = world.programs[pid]
            if p.cancelled_year is None and p.eis > a:
                lv["cancel"].append({"program": pid, "label": pc["label"], "eis": p.eis})
    if side == "boeing":
        if M.tactic_enabled(cfg, "rate_increase"):
            lv["flags"].append({"flag": "rate_increase", "available": world.rate_year is None,
                                "note": "one-time commitment" if world.rate_year is None else f"already committed in {world.rate_year}"})
    else:
        lv["flags"] += [x for x in ({"flag": "delay_tactics", "available": True, "note": "covert; applies to this turn only"},
                                    {"flag": "poaching", "available": True, "note": "public; applies to this turn only"})
                        if M.tactic_enabled(cfg, x["flag"])]
    tmpl = M.empty_orders(side)
    tmpl.update({"public_statement": "", "rationale": ""})
    lv["orders_template"] = tmpl
    return lv


def projection(cfg, history, mask):
    r = M.strip_exact(M.evaluate(cfg, M.build_world(cfg, history, mask)))
    return r


def objectives_view(cfg, objs, viewer):
    """Each player sees only its own objectives; control and the analyst see all; the market view shows none."""
    objs = objs or {}
    if viewer in ("control", "analyst"):
        return objs
    if viewer == "market":
        return {}  # any player may use --side market, so the market view carries no objectives
    return {viewer: objs[viewer]} if viewer in objs else {}


def objective_briefs(cfg, viewer):
    """The assigned objective text (goal, moves mapped to levers, enablers, constraints) visible to a viewer."""
    if not M.objectives_enabled(cfg):
        return {}
    o = cfg["objectives"]
    keep = ("primary_goal", "moves", "enablers", "constraints", "metrics", "label", "non_player")
    out_ = {k: {f: v[f] for f in keep if f in v} for k, v in o["players"].items() if k in objectives_view(cfg, {h: 1 for h in M.objective_holders(cfg)}, viewer)}
    for k, v in out_.items():
        v["source"] = o.get("source") if viewer in ("control", "analyst", "boeing") else "assigned by control for this scenario"
    return out_


def brief(st, viewer):
    if viewer not in VIEWERS:
        raise GameError(f"--side must be one of {', '.join(VIEWERS)}")
    cfg = st["config"]
    if viewer in M.SUPPLIERS and viewer not in M.active_suppliers(cfg):
        raise GameError(f"{viewer} is not a player in this run (create it with --suppliers {viewer})")
    order_sides = M.players(cfg)
    hist = st["history"] + pending_record(st)
    w_actual = M.build_world(cfg, hist)
    turn = st["current_turn"] if st["status"] != "complete" else st["turns_total"]
    year = M.turn_years(cfg, turn)[0] if st["status"] != "complete" else cfg["years"]["end"]
    full = viewer in ("control", "analyst")
    mask = M.belief_mask(cfg, hist, viewer)
    proj = projection(cfg, hist, mask)
    b = {
        "run_id": st["run_id"],
        "viewer": viewer,
        "scenario": cfg["scenario"],
        "status": st["status"],
        "turn": None if st["status"] == "complete" else turn,
        "turns_total": st["turns_total"],
        "turn_years": None if st["status"] == "complete" else list(M.turn_years(cfg, turn)),
        "turn_label": None if st["status"] == "complete" else next(t.get("label") for t in cfg["turns"] if t["turn"] == turn),
        "injects_this_turn": [{"id": i, **{k: cfg["injects"]["deck"][i][k] for k in ("title", "narrative")}}
                              for i in (st["pending_injects"] if st["status"] != "complete" else [])],
        "programs": public_programs(cfg, w_actual, year),
        "rate_increase_committed_year": w_actual.rate_year,
        "delay_tactics_exposed": w_actual.exposure_year is not None,
        "event_log": [e for e in w_actual.events if full or e["visibility"] == "public"
                      or (e["visibility"] == "private" and e["side"] == viewer)],
        "public_statements": [{"turn": r["turn"], "side": s, "text": r.get("statements", {}).get(s, {}).get("public_statement", "")}
                              for r in st["history"] for s in order_sides],
        "disclosures": [{"turn": r["turn"], "side": s, "items": r.get("statements", {}).get(s, {}).get("disclose", []),
                         "referee_note": r.get("referee_notes", {}).get(s, "")}
                        for r in st["history"] for s in order_sides if r.get("statements", {}).get(s, {}).get("disclose")],
        "market_reports": [{"turn": r["turn"], "narrative": r.get("market_narrative", "")} for r in st["history"]],
        "projected_market_shares": proj["shares"],
        **({"your_objectives" if viewer in M.players(cfg) else "objectives": objectives_view(cfg, proj.get("objectives"), viewer),
            "objectives_note": ("Assigned objectives, measured on this projection (no further moves). The referee scores attainment "
                                "alongside delta PV; objectives never change the payoff.")}
           if M.objectives_enabled(cfg) else {}),
        "projection_note": f"Projections assume nobody makes any further move. delta_pv_b is full-game PV ($B, {cfg['years']['pv_base']}) versus the status quo.",
    }
    if M.active_suppliers(cfg):
        b["players"] = list(order_sides)
        b["supplier_programs"] = public_supplier_programs(cfg, w_actual)
        b["supplier_upgrades_committed"] = {s: {"upgrade": cfg["suppliers"][s]["upgrade"]["label"], "year": w_actual.upgrade_years.get(s)}
                                            for s in M.active_suppliers(cfg) if cfg["suppliers"][s].get("upgrade")}
    if viewer in M.SUPPLIERS:
        b["your_projection"] = proj[viewer]
        b["airframer_projection_estimates"] = {s: {"delta_pv_b": proj[s]["delta_pv_b"], "components_pv_b": proj[s]["components_pv_b"]}
                                               for s in M.SIDES}
        b["airframer_projection_note"] = "Your estimate; it cannot include actions you have not observed."
        b["your_past_orders"] = [{"turn": r["turn"], "orders": r["orders"].get(viewer),
                                  "rationale": r.get("statements", {}).get(viewer, {}).get("rationale", "")} for r in st["history"]]
        if st["status"] != "complete":
            b["your_levers_this_turn"] = levers(cfg, M.build_world(cfg, hist, mask), viewer, turn)
    elif viewer in M.SIDES:
        opp = M.other(viewer)
        b["your_projection"] = proj[viewer]
        b["opponent_projection_estimate"] = {"delta_pv_b": proj[opp]["delta_pv_b"], "components_pv_b": proj[opp]["components_pv_b"],
                                             "note": "Your estimate; it cannot include opponent actions you have not observed."}
        b["your_past_orders"] = [{"turn": r["turn"], "orders": r["orders"][viewer],
                                  "rationale": r.get("statements", {}).get(viewer, {}).get("rationale", "")} for r in st["history"]]
        if st["status"] != "complete":
            b["your_levers_this_turn"] = levers(cfg, M.build_world(cfg, hist, mask), viewer, turn)
    elif full:
        b["projection"] = {s: proj[s] for s in order_sides}
        b["history"] = st["history"]
        b["pending_injects"] = st["pending_injects"]
    return b


def rules(cfg, side):
    """Game mechanics; the model is common knowledge, so every viewer gets the same rules."""
    tac = cfg["tactics"]
    return {
        "your_side": side,
        "your_programs": (M.programs_of(cfg, side) if side in M.SIDES else
                          list(cfg["suppliers"][side]["programs"]) if side in M.SUPPLIERS else None),
        "objective": f"Maximise your full-game delta PV ($B, PV to {cfg['years']['pv_base']} at your WACC) versus the status quo in which nobody moves.",
        "turns": cfg["turns"],
        "payoff_formula": ("sum over years and segments of units x share x net price x margin, minus the same for the status quo, "
                           "discounted at your WACC; minus capex x (1 + alpha), minus strain x (1 + alpha), minus tactic costs."),
        "share_rule": ("The first side to put a new product into service in a segment captures capture_pp_per_year of share per "
                       "year from EIS+1 (times engine and market multipliers) up to its leader cap; capture freezes when the "
                       "follower's new product enters service. If the segment sets capture_weight_by_year, each year's "
                       "capture is scaled by that year's weight (demand timing)."),
        "margin_rule": ("A new product earns margin_alone until the rival's new product is also in service, then margin_both; "
                        "minus early_penalty_pp_per_year for each year its EIS precedes tech_ready_year; plus the engine's margin_pp. "
                        "A Joint Venture gives the partner margin_share_partner of the margin and capex_share_partner of the capex."),
        "strain_rule": ("Developing a narrowbody and a widebody program at the same time costs strain.full_overlap_b x "
                        "min(1, overlap_years / strain.norm_years), spread over the overlap and alpha-loaded; a Joint Venture "
                        "relieves strain_relief of it."),
        "delay_rule": ("Extra development years (slips, engine eis_add, injects, waiting for an engine's available_eis or a "
                       "supplier's engine) cost extension_capex_frac_per_year of program capex per year."),
        "players": cfg["players"], "segments": cfg["segments"], "incumbents": cfg["incumbents"],
        "active_suppliers": list(M.active_suppliers(cfg)),
        "programs": cfg["programs"], "engine_options": cfg["engine_options"], "tactics": tac,
        "strain": cfg["strain"], "extension_capex_frac_per_year": cfg["extension_capex_frac_per_year"],
        "market_capture_mult_bounds": [cfg["market"]["capture_mult_min"], cfg["market"]["capture_mult_max"]],
        "inject_deck": {k: {"title": v["title"], "narrative": v["narrative"]} for k, v in cfg["injects"]["deck"].items()
                        if not v.get("requires_supplier") or v["requires_supplier"] in M.active_suppliers(cfg)},
        **({"suppliers": supplier_rules(cfg)} if M.active_suppliers(cfg) else {}),
        **({"assigned_objectives": objective_briefs(cfg, side),
            "assigned_objectives_rule": ("Your assigned objective is a mission set by control. The referee scores its attainment "
                                         "alongside delta PV; it does not change the payoff. Weigh it inside your doctrine.")}
           if M.objectives_enabled(cfg) and objective_briefs(cfg, side) else {}),
    }


def supplier_rules(cfg):
    out = {}
    for sup in M.active_suppliers(cfg):
        scfg = cfg["suppliers"][sup]
        out[sup] = {
            "label": scfg["label"],
            "objective": (f"{scfg['label']} maximises its full-game delta PV ($B, PV to {cfg['years']['pv_base']} at its WACC) versus the "
                          "status quo: the lifecycle value of the engines it delivers, less its alpha-loaded engine capex and strain."),
            "engine_rule": ("An airframer may select a supplier's engine for a program. If the supplier has not launched that engine "
                            "program by the end of the same turn (supplier orders are applied first), the program falls back to "
                            "fallback_engine for its segment. A committed engine is ready launch_year + dev_years (+ slips); the "
                            "airframe's entry into service is the later of its own date and the engine's ready year, and the "
                            "supplier's terms add airframer_margin_pp to the program's margin."),
            "value_rule": ("Engines delivered per year = segment units x airframer share x engines_per_aircraft x fit. Fit is "
                           "incumbent_fit until that airframer's new program in the segment enters service, then 1 minus any "
                           "Joint Venture partner share if it flies the supplier's engine, else 0. Each engine is booked at "
                           "delivery at its lifecycle value ($M): the incumbent value, or the new engine's mature value x a maturity "
                           "ramp (ramp.start_frac at EIS, which can be negative, rising to 1 after ramp.years), less the "
                           "terms' price concession of (1 - value_mult) x the mature value per engine."),
            "upgrade_rule": (f"{scfg['upgrade']['label']} (flag '{scfg['upgrade']['flag']}', one-time): capex_b over capex_years; from "
                             "lag_years later, fit_pp more of fit_side's segment deliveries until that airframer's new program in "
                             "the segment enters service; installed_base_saving_b_per_year for saving_years."
                             if scfg.get("upgrade") else "none"),
            "joint_venture_rule": ("A Joint Venture variant whose partner is another supplier player (partner_player) launches only "
                                   "if that partner sets its join flag in the same turn; the partner then pays capex_share_partner "
                                   "of the capex and earns value_share_partner of the engine's value. If the partner is not a "
                                   "player, the Joint Venture is with an outside partner and always launches."),
            "cancel_rule": "A supplier may cancel an engine program before it is ready only if no live airframe program flies it; capex spent is sunk.",
            "parameters": {k: v for k, v in scfg.items() if k not in ("active", "_about")},
        }
    return out


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_new(args):
    overrides = json.loads(args.override) if args.override else None
    sups = [x.strip() for x in (args.suppliers or "").split(",") if x.strip()]
    for sup in sups:
        if sup not in M.SUPPLIERS:
            raise GameError(f"unknown supplier '{sup}' (available: {', '.join(M.SUPPLIERS)})")
        overrides = M.deep_merge(overrides or {}, {"suppliers": {sup: {"active": True}}})
    cfg = M.load_config(args.scenario, overrides)
    for sup in M.active_suppliers(cfg):
        scfg = cfg["suppliers"][sup]
        for spid, spc in scfg["programs"].items():
            if spc["engine_option"] not in cfg["engine_options"].get(spc["segment"], {}):
                raise GameError(f"scenario '{args.scenario}' has no engine option '{spc['engine_option']}' for {sup} program "
                                f"'{spid}', so {scfg['label']} cannot play it")
        for seg, eng in scfg["fallback_engine"].items():
            if eng not in cfg["engine_options"].get(seg, {}) or M.supplier_requirement(cfg, seg, eng):
                raise GameError(f"{sup} fallback engine '{eng}' for {seg} must be an engine option that needs no supplier")
    n_all = len(cfg["turns"])
    n = args.turns or n_all
    if not 1 <= n <= n_all:
        raise GameError(f"--turns must be between 1 and {n_all}")
    run_id = args.run_id or f"wg-{_dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    d = run_dir(run_id)
    if os.path.exists(os.path.join(d, "state.json")) and not args.force:
        raise GameError(f"run '{run_id}' already exists; pick another --run-id or pass --force")
    st = {"run_id": run_id, "scenario": args.scenario, "overrides": overrides or {}, "seed": args.seed,
          "config": cfg, "turns_total": n, "current_turn": 1, "status": "in_progress",
          "pending_injects": [], "history": []}
    save_state(st)
    out({"run_id": run_id, "dir": d, "scenario": cfg["scenario"], "turns_total": n, "players": list(M.players(cfg)),
         "turns": cfg["turns"][:n], "next": f"python3 -m wargame.engine brief --run {run_id} --side control"})


def cmd_scenarios(args):
    out(M.list_scenarios())


def cmd_status(args):
    st = load_state(args.run)
    out({"run_id": st["run_id"], "dir": run_dir(st["run_id"]), "status": st["status"], "current_turn": st["current_turn"],
         "players": list(M.players(st["config"])),
         "turns_total": st["turns_total"], "pending_injects": st["pending_injects"],
         "adjudicated_turns": [r["turn"] for r in st["history"]]})


def cmd_brief(args):
    out(brief(load_state(args.run), args.side))


def cmd_rules(args):
    if args.run:
        cfg = load_state(args.run)["config"]
    else:
        cfg = M.load_config(args.scenario)
    r = rules(cfg, args.side or "control")
    if not args.side:  # assigned objectives only for a named viewer
        r.pop("assigned_objectives", None)
        r.pop("assigned_objectives_rule", None)
    out(r)


def _require_open(st):
    if st["status"] == "complete":
        raise GameError("the game is complete")


def eligible_injects(st):
    used = {i for r in st["history"] for i in r.get("injects", [])} | set(st["pending_injects"])
    deck = st["config"]["injects"]["deck"]
    sups = M.active_suppliers(st["config"])
    return [k for k in sorted(deck) if (k == "quiet_turn" or k not in used)
            and (not deck[k].get("requires_supplier") or deck[k]["requires_supplier"] in sups)]


def cmd_injects(args):
    st = load_state(args.run)
    deck = st["config"]["injects"]["deck"]
    el = eligible_injects(st)
    out({"turn": st["current_turn"], "pending": st["pending_injects"], "max_per_turn": st["config"]["injects"]["max_per_turn"],
         "eligible": [{"id": k, "title": deck[k]["title"], "narrative": deck[k]["narrative"], "effects": deck[k]["effects"]} for k in el]})


def cmd_inject(args):
    st = load_state(args.run)
    _require_open(st)
    if args.none:
        out({"turn": st["current_turn"], "pending_injects": st["pending_injects"], "applied": None})
        return
    if len(st["pending_injects"]) >= st["config"]["injects"]["max_per_turn"]:
        raise GameError(f"turn {st['current_turn']} already has {len(st['pending_injects'])} inject(s) (max_per_turn)")
    el = eligible_injects(st)
    if args.auto:
        h = hashlib.sha256(f"{st['run_id']}:{st.get('seed', 0)}:{st['current_turn']}".encode()).hexdigest()
        iid = el[int(h, 16) % len(el)]
    else:
        iid = args.id
        if iid not in st["config"]["injects"]["deck"]:
            raise GameError(f"unknown inject '{iid}'")
        req = st["config"]["injects"]["deck"][iid].get("requires_supplier")
        if req and req not in M.active_suppliers(st["config"]):
            raise GameError(f"inject '{iid}' needs {req} as a player in this run")
        if iid not in el:
            raise GameError(f"inject '{iid}' was already used in this game")
    st["pending_injects"].append(iid)
    save_state(st)
    inj = st["config"]["injects"]["deck"][iid]
    out({"turn": st["current_turn"], "applied": {"id": iid, "title": inj["title"], "narrative": inj["narrative"]},
         "pending_injects": st["pending_injects"]})


def _validate_side(st, side, orders, hist_before=None):
    cfg = st["config"]
    hist = (st["history"] if hist_before is None else hist_before) + pending_record(st)
    return M.validate_orders(cfg, hist, st["current_turn"], side, orders)


def cmd_validate(args):
    st = load_state(args.run)
    _require_open(st)
    orders = read_stdin_json()
    canon, errors, warnings = _validate_side(st, args.side, orders)
    out({"ok": not errors, "turn": st["current_turn"], "canonical_orders": canon, "errors": errors, "warnings": warnings,
         "orders_digest": M.orders_digest(args.side, canon) if canon else None})


def cmd_options(args):
    st = load_state(args.run)
    _require_open(st)
    cfg = st["config"]
    viewer = args.side
    mask = M.belief_mask(cfg, st["history"] + pending_record(st), viewer)
    if viewer in M.SUPPLIERS:
        if viewer not in M.active_suppliers(cfg):
            raise GameError(f"{viewer} is not a player in this run")
        rep = S.supplier_stage(cfg, st["history"], st["current_turn"], st["pending_injects"], viewer, mask)
        rep.update({"turn": st["current_turn"], "turn_years": list(M.turn_years(cfg, st["current_turn"]))})
        out(rep)
        return
    sg = S.stage_game(cfg, st["history"], st["current_turn"], st["pending_injects"], mask)
    rep = S.stage_report(cfg, sg, viewer if viewer in M.SIDES else "control", compact=args.compact)
    rep.update({"turn": st["current_turn"], "turn_years": list(M.turn_years(cfg, st["current_turn"]))})
    out(rep)


def _apply_overrides(st, overrides, viewer):
    """History with some turns' orders replaced; validated turn by turn."""
    cfg = st["config"]
    sides = M.players(cfg)
    ov = {s: {int(t): o for t, o in (overrides.get(s) or {}).items()} for s in sides}
    last = st["turns_total"] if st["status"] == "complete" else st["current_turn"]
    horizon = max([last] + [t for s in sides for t in ov[s]])
    if horizon > st["turns_total"]:
        raise GameError(f"this game has {st['turns_total']} turns")
    recorded = {r["turn"]: r for r in st["history"]}
    hist, notes = [], []
    for t in range(1, horizon + 1):
        if t in recorded:
            rec = {k: v for k, v in recorded[t].items() if k in ("turn", "injects", "orders", "market")}
            rec["orders"] = dict(rec["orders"])
        elif t == st["current_turn"] and st["status"] != "complete":
            rec = {"turn": t, "injects": list(st["pending_injects"]), "orders": {}, "market": {}}
        else:
            rec = {"turn": t, "injects": [], "orders": {}, "market": {}}
        # Suppliers first: their orders apply before the airframers' engine selections are resolved.
        for s in M.active_suppliers(cfg) + M.SIDES:
            if t in ov[s]:
                pre = {x: rec["orders"][x] for x in M.active_suppliers(cfg) if s in M.SIDES and x in rec["orders"]}
                canon, errors, warnings = M.validate_orders(cfg, hist + [dict(rec, orders=pre)], t, s, ov[s][t])
                if errors:
                    raise GameError(f"turn {t} {s} orders invalid: {'; '.join(errors)}")
                rec["orders"][s] = canon
                notes += [f"turn {t} {s}: {w}" for w in warnings]
            elif s not in rec["orders"]:
                rec["orders"][s] = M.empty_orders(s)
        hist.append(rec)
    return hist, notes


def cmd_whatif(args):
    st = load_state(args.run)
    cfg = st["config"]
    req = read_stdin_json()
    overrides = req.get("orders", req)
    sides = M.players(cfg)
    bad = [k for k in overrides if k not in sides]
    if bad or not any(k in overrides for k in sides):
        raise GameError('whatif expects {"boeing": {"<turn>": orders}, "airbus": {"<turn>": orders}'
                        + "".join(f', "{x}": {{"<turn>": orders}}' for x in M.active_suppliers(cfg)) + "}; "
                        f"got top-level keys {sorted(overrides)}")
    for s_ in sides:
        for t in (overrides.get(s_) or {}):
            if not str(t).isdigit():
                raise GameError(f'whatif: "{s_}" must map turn numbers to orders, e.g. {{"{s_}": {{"2": {{...}}}}}}; got key {t!r}')
    hist, notes = _apply_overrides(st, overrides, args.side)
    mask = M.belief_mask(cfg, st["history"] + pending_record(st), args.side)
    r = M.strip_exact(M.evaluate(cfg, M.build_world(cfg, hist, mask)))
    base = M.strip_exact(M.evaluate(cfg, M.build_world(cfg, st["history"] + pending_record(st), mask)))
    res = {"assumption": "Turns you did not override keep their recorded orders (past) or no new moves (current/future).",
           "notes": notes, "shares": r["shares"]}
    if M.objectives_enabled(cfg):
        res["objectives"] = objectives_view(cfg, r.get("objectives"), args.side)
        res["objectives_now"] = objectives_view(cfg, base.get("objectives"), args.side)
    for s in sides:
        res[s] = r[s]
        res[s]["change_vs_current_projection_b"] = round(r[s]["delta_pv_b"] - base[s]["delta_pv_b"], 3)
    if args.side in sides:
        for s in sides:
            if s != args.side:
                res[s]["note"] = "Estimate from your information set."
    out(res)


def _orders_and_text(st, side, orders):
    canon, errors, warnings = _validate_side(st, side, orders)
    text = {k: str(orders.get(k, "")) for k in M.TEXT_FIELDS} if isinstance(orders, dict) else {}
    if isinstance(orders, dict):
        disc = orders.get("disclose") or []
        text["disclose"] = [str(d) for d in (disc if isinstance(disc, list) else [disc]) if str(d).strip()]
        if isinstance(orders.get("prediction"), dict):
            text["prediction"] = orders["prediction"]
        if isinstance(orders.get("expected_delta_pv_b"), (int, float)):
            text["expected_delta_pv_b"] = float(orders["expected_delta_pv_b"])
    return canon, errors, warnings, text


def cmd_adjudicate(args):
    st = load_state(args.run)
    _require_open(st)
    cfg = st["config"]
    k = st["current_turn"]
    if args.turn is not None and args.turn != k:
        raise GameError(f"the run is on turn {k}, not turn {args.turn}")
    req = read_stdin_json()
    sides = M.players(cfg)
    extra = [x for x in req if x in ORDER_SIDES and x not in sides]
    if extra:
        raise GameError(f"orders for {', '.join(extra)}, which is not a player in this run")
    canons, texts, errs, warns = {}, {}, {}, {}
    sups = M.active_suppliers(cfg)
    for side in sups + M.SIDES:  # suppliers first: airframers' engine choices are checked against their commitments
        if side not in req:
            errs[side] = [f"missing '{side}' orders"]
            continue
        pre = {x: canons[x] for x in sups if side in M.SIDES and canons.get(x)}
        if pre:
            hist = st["history"] + [dict(pending_record(st)[0], orders=pre)]
            canons[side], errs[side], warns[side] = M.validate_orders(cfg, hist, k, side, req[side])
            texts[side] = _orders_and_text(st, side, req[side])[3]
        else:
            canons[side], errs[side], warns[side], texts[side] = _orders_and_text(st, side, req[side])
    if any(errs.values()):
        out({"status": "invalid", "turn": k, "errors": {s: e for s, e in errs.items() if e}})
        sys.exit(2)
    if args.expect_digest:
        want = dict(part.split("=", 1) for part in args.expect_digest.split(",") if "=" in part)
        got = {s: M.orders_digest(s, canons[s]) for s in sides}
        bad = [s for s in sides if want.get(s) != got[s]]
        if bad:
            raise GameError(f"orders digest mismatch for {', '.join(bad)}: expected {want}, engine computed {got}; "
                            "the orders were altered in transit, so nothing was adjudicated")
    market = req.get("market") or {}
    mult_in = market.get("capture_mult") or {}
    rec = {"turn": k, "years": list(M.turn_years(cfg, k)), "injects": list(st["pending_injects"]),
           "orders": canons, "statements": texts, "market": {}, "market_narrative": str(market.get("narrative", ""))}
    world_after = M.build_world(cfg, st["history"] + [rec])
    lo, hi = cfg["market"]["capture_mult_min"], cfg["market"]["capture_mult_max"]
    applied, market_notes = {}, []
    for pid, m in mult_in.items():
        if pid not in world_after.programs:
            market_notes.append(f"ignored capture_mult for '{pid}': not launched")
            continue
        try:
            v = float(m)
        except (TypeError, ValueError):
            market_notes.append(f"ignored non-numeric capture_mult for '{pid}'")
            continue
        if not lo <= v <= hi:
            market_notes.append(f"clamped capture_mult for '{pid}' from {v} to [{lo}, {hi}]")
        applied[pid] = min(hi, max(lo, v))
    rec["market"] = {"capture_mult": applied}
    full_hist = st["history"] + [rec]
    world = M.build_world(cfg, full_hist)
    proj = M.strip_exact(M.evaluate(cfg, world))
    rec["projection"] = {s: {"delta_pv_b": proj[s]["delta_pv_b"], "components_pv_b": proj[s]["components_pv_b"]} for s in sides}
    st["history"].append(rec)
    st["pending_injects"] = []
    done = k >= st["turns_total"]
    st["status"] = "complete" if done else "in_progress"
    st["current_turn"] = k + 1
    save_state(st)
    result = {
        "status": "ok", "turn": k, "orders_digest": {s: M.orders_digest(s, canons[s]) for s in sides},
        "orders_received": canons, "market_applied": applied, "market_notes": market_notes,
        "warnings": {s: w for s, w in warns.items() if w},
        "events": [e for e in world.events if e["turn"] == k],
        "projection": rec["projection"], "shares": proj["shares"],
        "game_complete": done, "next_turn": None if done else k + 1,
    }
    with open(os.path.join(run_dir(st["run_id"]), "turns", f"T{k}.json"), "w") as f:
        json.dump(result, f, indent=1)
    out(result)


def cmd_rollback(args):
    st = load_state(args.run)
    t = args.to_turn
    if not 1 <= t <= len(st["history"]) + 1:
        raise GameError(f"--to-turn must be between 1 and {len(st['history']) + 1}")
    dropped = [r for r in st["history"] if r["turn"] >= t]
    st["history"] = [r for r in st["history"] if r["turn"] < t]
    st["pending_injects"] = list(dropped[0]["injects"]) if dropped else st["pending_injects"]
    st["current_turn"] = t
    st["status"] = "in_progress"
    save_state(st)
    for r in dropped:
        p = os.path.join(run_dir(st["run_id"]), "turns", f"T{r['turn']}.json")
        if os.path.exists(p):
            os.remove(p)
    out({"run_id": st["run_id"], "current_turn": t, "pending_injects": st["pending_injects"],
         "dropped_turns": [r["turn"] for r in dropped]})


def cmd_equilibria(args):
    st = load_state(args.run)
    cfg = st["config"]
    complete = st["status"] == "complete"
    from_turn = args.from_turn or (1 if complete else st["current_turn"])
    if not 1 <= from_turn <= st["turns_total"]:
        raise GameError(f"--from-turn must be between 1 and {st['turns_total']}")
    if not complete and from_turn > st["current_turn"]:
        raise GameError("--from-turn cannot be later than the current turn")
    viewer = args.side or "control"
    mask = M.belief_mask(cfg, st["history"] + pending_record(st), viewer)
    res = S.plan_game(cfg, st["history"], from_turn, st["turns_total"], None if complete else st["current_turn"],
                      st["pending_injects"], args.segment, mask)
    res["viewer"] = viewer
    out(res)


def final_report(st):
    cfg = st["config"]
    w = M.build_world(cfg, st["history"])
    ev = M.strip_exact(M.evaluate(cfg, w))
    return {
        "run_id": st["run_id"], "status": st["status"], "scenario": cfg["scenario"], "turns_total": st["turns_total"],
        "players": list(M.players(cfg)),
        "final": {s: ev[s] for s in M.players(cfg)}, "shares": ev["shares"],
        "objectives": ev.get("objectives", {}),
        "trajectory": [{"turn": r["turn"], "projection": r.get("projection")} for r in st["history"]],
        "turns": [{"turn": r["turn"], "years": r.get("years"), "injects": r.get("injects", []), "orders": r["orders"],
                   "statements": r.get("statements", {}), "market": r.get("market", {}),
                   "market_narrative": r.get("market_narrative", "")} for r in st["history"]],
        "events": w.events,
        "delay_tactics_turns": w.delay_turns, "poaching_turns": w.poaching_turns,
        "delay_tactics_exposed_year": w.exposure_year,
        **({"supplier_programs": public_supplier_programs(cfg, w),
            "supplier_upgrades": {s: w.upgrade_years.get(s) for s in M.active_suppliers(cfg) if cfg["suppliers"][s].get("upgrade")}}
           if M.active_suppliers(cfg) else {}),
    }


def report_markdown(rep, cfg):
    L = []
    fin = rep["final"]
    L.append(f"## Scoreboard ({rep['status']})")
    L.append("")
    L.append("Full-game delta PV versus the status quo, $B PV 2026 (Boeing at "
             f"{cfg['players']['boeing']['wacc'] * 100:.1f}% WACC, Airbus at {cfg['players']['airbus']['wacc'] * 100:.1f}%).")
    L.append("")
    L.append("| Component | Boeing | Airbus |")
    L.append("|---|---:|---:|")
    for k in ("nb_operating", "wb_operating", "capex", "strain", "tactics"):
        L.append(f"| {k.replace('_', ' ')} | {fin['boeing']['components_pv_b'][k]:+.2f} | {fin['airbus']['components_pv_b'][k]:+.2f} |")
    L.append(f"| **Total** | **{fin['boeing']['delta_pv_b']:+.2f}** | **{fin['airbus']['delta_pv_b']:+.2f}** |")
    L.append("")
    sups = [s for s in M.SUPPLIERS if s in fin]
    for sup in sups:
        scfg = cfg["suppliers"][sup]
        L.append(f"{scfg['label']} (supplier, {scfg['wacc'] * 100:.1f}% WACC):")
        L.append("")
        L.append(f"| Component | {scfg['label']} |")
        L.append("|---|---:|")
        for k, v in fin[sup]["components_pv_b"].items():
            L.append(f"| {k.replace('_', ' ')} | {v:+.2f} |")
        L.append(f"| **Total** | **{fin[sup]['delta_pv_b']:+.2f}** |")
        L.append("")
    L.append("## Projection after each turn")
    L.append("")
    L.append("| Turn | Boeing | Airbus |" + "".join(f" {cfg['suppliers'][x]['label']} |" for x in sups))
    L.append("|---|---:|---:|" + "---:|" * len(sups))
    for t in rep["trajectory"]:
        p = t["projection"] or {}
        L.append(f"| T{t['turn']} | {p.get('boeing', {}).get('delta_pv_b', 0):+.2f} | {p.get('airbus', {}).get('delta_pv_b', 0):+.2f} |"
                 + "".join(f" {p.get(x, {}).get('delta_pv_b', 0):+.2f} |" for x in sups))
    L.append("")
    L.append("## Programs")
    L.append("")
    L.append("| Side | Program | Launch | EIS | Engine | Variant | Slips |")
    L.append("|---|---|---:|---:|---|---|---|")
    for s in M.SIDES:
        for p in fin[s]["programs"]:
            slips = "; ".join(f"T{x['turn']} +{x['years']}y {x['cause']}" for x in p["slips"]) or "-"
            eis = p["eis"] if p["eis"] is not None else f"cancelled {p['cancelled_year']}"
            L.append(f"| {cfg['players'][s]['label']} | {p['label']} | {p['launch_year']} | {eis} | {p['engine_label']} | {p['variant'] or '-'} | {slips} |")
    L.append("")
    if rep.get("supplier_programs") is not None:
        L.append("## Supplier engine programs")
        L.append("")
        L.append("| Supplier | Program | Launch | Ready | Variant | Terms | Flown by |")
        L.append("|---|---|---:|---:|---|---|---|")
        for sp in rep["supplier_programs"]:
            ready = sp["ready"] if sp["ready"] is not None else f"cancelled {sp['cancelled_year']}"
            jv = f" + {cfg['suppliers'][sp['joint_venture_partner']]['label']}" if sp.get("joint_venture_partner") else ""
            L.append(f"| {cfg['suppliers'][sp['supplier']]['label']}{jv} | {sp['label']} | {sp['launch_year']} | {ready} | "
                     f"{sp['variant'] or '-'} | {sp['terms']} | {', '.join(sp['selected_by']) or '-'} |")
        if not rep["supplier_programs"]:
            L.append("| - | none launched | | | | | |")
        L.append("")
        L.append("Upgrades: " + "; ".join(f"{cfg['suppliers'][s]['label']} {cfg['suppliers'][s]['upgrade']['label']}: {y or 'not committed'}"
                                          for s, y in rep.get("supplier_upgrades", {}).items()) + ".")
        L.append("")
    L.append("## Market share (Boeing / Airbus)")
    L.append("")
    yrs = list(rep["shares"]["nb"].keys())
    L.append("| Segment | " + " | ".join(yrs) + " |")
    L.append("|---|" + "---:|" * len(yrs))
    for seg in M.SEGMENTS:
        L.append(f"| {cfg['segments'][seg]['label']} | " + " | ".join(
            f"{rep['shares'][seg][y]['boeing'] * 100:.1f} / {rep['shares'][seg][y]['airbus'] * 100:.1f}" for y in yrs) + " |")
    L.append("")
    if rep.get("objectives"):
        L.append("## Assigned objectives (attainment on the " + ("final" if rep["status"] == "complete" else "current") + " projection)")
        L.append("")
        L.append(objectives_markdown(rep["objectives"], cfg))
        L.append("")
    L.append("## Orders by turn")
    L.append("")
    for t in rep["turns"]:
        inj = ", ".join(cfg["injects"]["deck"][i]["title"] for i in t["injects"]) or "none"
        L.append(f"**Turn {t['turn']} ({t['years'][0]}-{t['years'][1]})**, inject: {inj}")
        L.append("")
        for s in M.players(cfg):
            if s in t["orders"]:
                L.append(f"- {M.player_label(cfg, s)}: {S.describe_orders(cfg, s, t['orders'][s])}")
        if t["market"].get("capture_mult"):
            L.append(f"- Market capture multipliers: " + ", ".join(f"{k} x{v:.2f}" for k, v in t["market"]["capture_mult"].items()))
        L.append("")
    L.append(f"Delay Tactics used in turns: {rep['delay_tactics_turns'] or 'none'}; "
             f"exposed: {rep['delay_tactics_exposed_year'] or 'no'}. Poaching used in turns: {rep['poaching_turns'] or 'none'}.")
    return "\n".join(L)


def _fmt_obj_values(r):
    v = r.get("values") or {}
    if "upgrade_year" in v:
        return f"upgrade {v['upgrade_year'] or 'not committed'}"
    if "first_eis" in v:
        return f"first EIS {v['first_eis'] or 'none'}"
    pct = str(r.get("unit", "")).startswith("share")
    cells = []
    for y, x in v.items():
        if x is None:
            continue
        sq = (r.get("status_quo") or {}).get(y)
        if pct:
            cells.append(f"{y}: {x * 100:.1f}%" + (f" (sq {sq * 100:.1f}%)" if sq is not None else ""))
        else:
            cells.append(f"{y}: {x:,.0f}" + (f" (sq {sq:,.0f})" if sq is not None else ""))
    return "; ".join(cells) or "-"


def objectives_markdown(objs, cfg):
    L = ["| Player | Objective | Measured | Met |", "|---|---|---|---|"]
    for who, rows in objs.items():
        name = cfg["objectives"]["players"].get(who, {}).get("label") or M.player_label(cfg, who)
        for r in rows:
            met = "n/a" if r.get("met") is None else ("yes" if r["met"] else "no")
            extra = f" ({r['note']})" if r.get("note") else (f", gap {r['gap_pp']:+.1f}pp" if r.get("gap_pp") is not None and not r.get("met") else "")
            L.append(f"| {name} | {r['label']} | {_fmt_obj_values(r)}{extra} | {met} |")
    return "\n".join(L)


def cmd_scorecard(args):
    st = load_state(args.run)
    cfg = st["config"]
    sc = S.turn_scorecard(cfg, st["history"])
    if args.final:
        if st["status"] != "complete":
            raise GameError("--final needs a completed game")
        eq = S.plan_game(cfg, st["history"], 1, st["turns_total"], None, [], "all")
        sc["hindsight"] = {"actual_play_b": eq.get("actual_play"), "regret_vs_actual": eq.get("regret_vs_actual"),
                           "pure_nash": eq.get("pure_nash")}
        if M.active_suppliers(cfg):
            sc["hindsight"]["note"] = "Hindsight regret is for the airframers only; supplier orders are held as played."
        for s in M.SIDES:
            sc["summary"][s]["final_delta_pv_b"] = eq.get("actual_play", {}).get(s)
            sc["summary"][s]["hindsight_regret_b"] = (eq.get("regret_vs_actual", {}).get(s) or {}).get("regret_b")
    if M.objectives_enabled(cfg):
        hist = st["history"]
        sc["objectives"] = M.evaluate(cfg, M.build_world(cfg, hist)).get("objectives", {})
        sc["objectives_by_turn"] = [{"turn": r["turn"], "objectives": {w: {x["id"]: x["met"] for x in rows} for w, rows in
                                     M.evaluate(cfg, M.build_world(cfg, hist[:i + 1])).get("objectives", {}).items()}}
                                    for i, r in enumerate(hist)]
    sc["run_id"] = st["run_id"]
    sc["visibility"] = "control only: rows reveal each side's actual orders, including covert ones"
    if args.format == "md":
        L = [f"| Turn | Side | Orders | Value $B | Best response | Best $B | Regret $B | Capture | Prediction | Expectation error $B |",
             "|---|---|---|---:|---|---:|---:|---:|---:|---:|"]
        for r in sc["rows"]:
            L.append(f"| T{r['turn']} | {r['side']} | {r['orders']} | {r['myopic_value_b']:+.2f} | {r['best_response']} | "
                     f"{r['best_response_value_b']:+.2f} | {r['regret_b']:.2f} | {r['capture']:.0%} | "
                     f"{'-' if r['prediction_accuracy'] is None else format(r['prediction_accuracy'], '.0%')} | "
                     f"{'-' if r['expectation_error_b'] is None else format(r['expectation_error_b'], '+.2f')} |")
        L += ["", "| Side | Mean capture | Total myopic regret $B | Prediction accuracy | Mean abs expectation error $B | Final delta PV $B | Hindsight regret $B |",
              "|---|---:|---:|---:|---:|---:|---:|"]
        for s, v in sc["summary"].items():
            f = lambda x, fmt: "-" if x is None else format(x, fmt)
            L.append(f"| {s} | {f(v['mean_capture'], '.0%')} | {v['total_myopic_regret_b']:.2f} | {f(v['mean_prediction_accuracy'], '.0%')} | "
                     f"{f(v['mean_abs_expectation_error_b'], '.2f')} | {f(v.get('final_delta_pv_b'), '+.2f')} | {f(v.get('hindsight_regret_b'), '.2f')} |")
        if sc.get("objectives"):
            L += ["", "Assigned objectives (attainment on the " + ("final" if st["status"] == "complete" else "current") + " projection):", "",
                  objectives_markdown(sc["objectives"], cfg)]
            if sc.get("objectives_by_turn"):
                ids = [(w, x["id"]) for w, rows in sc["objectives"].items() for x in rows]
                L += ["", "| Turn | " + " | ".join(f"{w}:{i}" for w, i in ids) + " |", "|---|" + "---|" * len(ids)]
                for t in sc["objectives_by_turn"]:
                    L.append(f"| T{t['turn']} | " + " | ".join({True: "yes", False: "no", None: "n/a"}[t["objectives"].get(w, {}).get(i)] for w, i in ids) + " |")
        print("\n".join(L))
    else:
        out(sc)


def cmd_annotate(args):
    st = load_state(args.run)
    rec = next((r for r in st["history"] if r["turn"] == args.turn), None)
    if rec is None:
        raise GameError(f"turn {args.turn} has not been adjudicated")
    rec.setdefault("referee_notes", {})[args.side] = args.note
    save_state(st)
    out({"run_id": st["run_id"], "turn": args.turn, "side": args.side, "referee_note": args.note})


def cmd_report(args):
    st = load_state(args.run)
    rep = final_report(st)
    if args.format == "md":
        print(report_markdown(rep, st["config"]))
    else:
        out(rep)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python3 -m wargame.engine",
                                 description="Boeing vs Airbus war-game engine (optionally with Rolls-Royce and Pratt & Whitney as engine-supplier players)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="create a run (control)")
    p.add_argument("--scenario", default="base")
    p.add_argument("--turns", type=int)
    p.add_argument("--run-id")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--override", help="JSON deep-merged over the scenario config")
    p.add_argument("--suppliers", help="comma list of supplier players to add: rolls_royce, pratt_whitney")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_new)

    sub.add_parser("scenarios", help="list scenarios").set_defaults(fn=cmd_scenarios)

    p = sub.add_parser("status")
    p.add_argument("--run", required=True)
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("brief", help="situation brief with fog of war")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=VIEWERS)
    p.set_defaults(fn=cmd_brief)

    p = sub.add_parser("rules", help="game mechanics and parameters")
    p.add_argument("--run")
    p.add_argument("--scenario", default="base")
    p.add_argument("--side", default=None, choices=VIEWERS)
    p.set_defaults(fn=cmd_rules)

    p = sub.add_parser("injects", help="list injects still available (control)")
    p.add_argument("--run", required=True)
    p.set_defaults(fn=cmd_injects)

    p = sub.add_parser("inject", help="apply an inject to the current turn (control)")
    p.add_argument("--run", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--auto", action="store_true")
    g.add_argument("--none", action="store_true")
    p.set_defaults(fn=cmd_inject)

    p = sub.add_parser("validate", help="check orders from stdin")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=ORDER_SIDES)
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("options", help="this turn's stage game")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=VIEWERS)
    p.add_argument("--compact", action="store_true", help="omit the full matrix")
    p.set_defaults(fn=cmd_options)

    p = sub.add_parser("whatif", help="evaluate order overrides from stdin: {\"boeing\": {\"2\": orders}, \"airbus\": {...}, \"rolls_royce\"|\"pratt_whitney\": {...}}")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=VIEWERS)
    p.set_defaults(fn=cmd_whatif)

    p = sub.add_parser("adjudicate", help="apply all players' orders and the market reaction from stdin (control)")
    p.add_argument("--run", required=True)
    p.add_argument("--turn", type=int)
    p.add_argument("--expect-digest", help="boeing=<hex>,airbus=<hex>[,rolls_royce=<hex>][,pratt_whitney=<hex>]; refuse to adjudicate if the orders differ")
    p.set_defaults(fn=cmd_adjudicate)

    p = sub.add_parser("rollback", help="undo turns from --to-turn onward (control)")
    p.add_argument("--run", required=True)
    p.add_argument("--to-turn", type=int, required=True)
    p.set_defaults(fn=cmd_rollback)

    p = sub.add_parser("equilibria", help="normal-form plan game for the remaining (or all) turns")
    p.add_argument("--run", required=True)
    p.add_argument("--from-turn", type=int)
    p.add_argument("--segment", default="all", choices=("all", "nb", "wb"))
    p.add_argument("--side", choices=VIEWERS)
    p.set_defaults(fn=cmd_equilibria)

    p = sub.add_parser("scorecard", help="referee's efficiency scorecard per player (control only)")
    p.add_argument("--run", required=True)
    p.add_argument("--final", action="store_true", help="add hindsight regret from the plan game (~15 s)")
    p.add_argument("--format", default="json", choices=("json", "md"))
    p.set_defaults(fn=cmd_scorecard)

    p = sub.add_parser("annotate", help="attach the referee's public note to a side's disclosures (control)")
    p.add_argument("--run", required=True)
    p.add_argument("--turn", type=int, required=True)
    p.add_argument("--side", required=True, choices=ORDER_SIDES)
    p.add_argument("--note", required=True)
    p.set_defaults(fn=cmd_annotate)

    p = sub.add_parser("report", help="full results (control/analyst)")
    p.add_argument("--run", required=True)
    p.add_argument("--format", default="json", choices=("json", "md"))
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args(argv)
    try:
        args.fn(args)
    except GameError as e:
        out({"status": "error", "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
