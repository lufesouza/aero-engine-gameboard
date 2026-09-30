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
VIEWERS = ("boeing", "airbus", "market", "control", "analyst")


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
            "eis": None if p.cancelled_year is not None else p.eis, "status": p.status(year),
            "cancelled_year": p.cancelled_year,
            "slips": [{"turn": s["turn"], "years": s["years"],
                       "cause": dt["public_cause_unexposed"] if (s["covert"] and not exposed) else s["cause"]}
                      for s in p.slips],
            "market_capture_mult": round(p.capture_mult, 3),
        })
    return rows


def levers(cfg, world, side, turn):
    a, b = M.turn_years(cfg, turn)
    lv = {"launch": [], "cancel": [], "flags": []}
    for pid in M.programs_of(cfg, side):
        pc = cfg["programs"][pid]
        if pid not in world.programs:
            item = {"program": pid, "label": pc["label"], "years": [a, b], "dev_years": pc.get("dev_years", 0) + world.dev_years_add[side],
                    "engines": list(cfg["engine_options"][pc["segment"]]), "default_engine": pc["default_engine"]}
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


def brief(st, viewer):
    if viewer not in VIEWERS:
        raise GameError(f"--side must be one of {', '.join(VIEWERS)}")
    cfg = st["config"]
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
                              for r in st["history"] for s in M.SIDES],
        "disclosures": [{"turn": r["turn"], "side": s, "items": r.get("statements", {}).get(s, {}).get("disclose", []),
                         "referee_note": r.get("referee_notes", {}).get(s, "")}
                        for r in st["history"] for s in M.SIDES if r.get("statements", {}).get(s, {}).get("disclose")],
        "market_reports": [{"turn": r["turn"], "narrative": r.get("market_narrative", "")} for r in st["history"]],
        "projected_market_shares": proj["shares"],
        "projection_note": f"Projections assume nobody makes any further move. delta_pv_b is full-game PV ($B, {cfg['years']['pv_base']}) versus the status quo.",
    }
    if viewer in M.SIDES:
        opp = M.other(viewer)
        b["your_projection"] = proj[viewer]
        b["opponent_projection_estimate"] = {"delta_pv_b": proj[opp]["delta_pv_b"], "components_pv_b": proj[opp]["components_pv_b"],
                                             "note": "Your estimate; it cannot include opponent actions you have not observed."}
        b["your_past_orders"] = [{"turn": r["turn"], "orders": r["orders"][viewer],
                                  "rationale": r.get("statements", {}).get(viewer, {}).get("rationale", "")} for r in st["history"]]
        if st["status"] != "complete":
            b["your_levers_this_turn"] = levers(cfg, M.build_world(cfg, hist, mask), viewer, turn)
    elif full:
        b["projection"] = {s: proj[s] for s in M.SIDES}
        b["history"] = st["history"]
        b["pending_injects"] = st["pending_injects"]
    return b


def rules(cfg, side):
    """Game mechanics; the model is common knowledge, so every viewer gets the same rules."""
    tac = cfg["tactics"]
    return {
        "your_side": side,
        "your_programs": M.programs_of(cfg, side) if side in M.SIDES else None,
        "objective": f"Maximise your full-game delta PV ($B, PV to {cfg['years']['pv_base']} at your WACC) versus the status quo in which nobody moves.",
        "turns": cfg["turns"],
        "payoff_formula": ("sum over years and segments of units x share x net price x margin, minus the same for the status quo, "
                           "discounted at your WACC; minus capex x (1 + alpha), minus strain x (1 + alpha), minus tactic costs."),
        "share_rule": ("The first side to put a new product into service in a segment captures capture_pp_per_year of share per "
                       "year from EIS+1 (times engine and market multipliers) up to its leader cap; capture freezes when the "
                       "follower's new product enters service."),
        "margin_rule": ("A new product earns margin_alone until the rival's new product is also in service, then margin_both; "
                        "minus early_penalty_pp_per_year for each year its EIS precedes tech_ready_year; plus the engine's margin_pp. "
                        "A Joint Venture gives the partner margin_share_partner of the margin and capex_share_partner of the capex."),
        "strain_rule": ("Developing a narrowbody and a widebody program at the same time costs strain.full_overlap_b x "
                        "min(1, overlap_years / strain.norm_years), spread over the overlap and alpha-loaded; a Joint Venture "
                        "relieves strain_relief of it."),
        "delay_rule": ("Extra development years (slips, engine eis_add, injects) cost extension_capex_frac_per_year of program "
                       "capex per year."),
        "players": cfg["players"], "segments": cfg["segments"], "incumbents": cfg["incumbents"],
        "programs": cfg["programs"], "engine_options": cfg["engine_options"], "tactics": tac,
        "strain": cfg["strain"], "extension_capex_frac_per_year": cfg["extension_capex_frac_per_year"],
        "market_capture_mult_bounds": [cfg["market"]["capture_mult_min"], cfg["market"]["capture_mult_max"]],
        "inject_deck": {k: {"title": v["title"], "narrative": v["narrative"]} for k, v in cfg["injects"]["deck"].items()},
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_new(args):
    overrides = json.loads(args.override) if args.override else None
    cfg = M.load_config(args.scenario, overrides)
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
    out({"run_id": run_id, "dir": d, "scenario": cfg["scenario"], "turns_total": n,
         "turns": cfg["turns"][:n], "next": f"python3 -m wargame.engine brief --run {run_id} --side control"})


def cmd_scenarios(args):
    out(M.list_scenarios())


def cmd_status(args):
    st = load_state(args.run)
    out({"run_id": st["run_id"], "dir": run_dir(st["run_id"]), "status": st["status"], "current_turn": st["current_turn"],
         "turns_total": st["turns_total"], "pending_injects": st["pending_injects"],
         "adjudicated_turns": [r["turn"] for r in st["history"]]})


def cmd_brief(args):
    out(brief(load_state(args.run), args.side))


def cmd_rules(args):
    if args.run:
        cfg = load_state(args.run)["config"]
    else:
        cfg = M.load_config(args.scenario)
    out(rules(cfg, args.side))


def _require_open(st):
    if st["status"] == "complete":
        raise GameError("the game is complete")


def eligible_injects(st):
    used = {i for r in st["history"] for i in r.get("injects", [])} | set(st["pending_injects"])
    return [k for k in sorted(st["config"]["injects"]["deck"]) if k == "quiet_turn" or k not in used]


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
    sg = S.stage_game(cfg, st["history"], st["current_turn"], st["pending_injects"], mask)
    rep = S.stage_report(cfg, sg, viewer if viewer in M.SIDES else "control", compact=args.compact)
    rep.update({"turn": st["current_turn"], "turn_years": list(M.turn_years(cfg, st["current_turn"]))})
    out(rep)


def _apply_overrides(st, overrides, viewer):
    """History with some turns' orders replaced; validated turn by turn."""
    cfg = st["config"]
    ov = {s: {int(t): o for t, o in (overrides.get(s) or {}).items()} for s in M.SIDES}
    last = st["turns_total"] if st["status"] == "complete" else st["current_turn"]
    horizon = max([last] + [t for s in M.SIDES for t in ov[s]])
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
        for s in M.SIDES:
            if t in ov[s]:
                canon, errors, warnings = M.validate_orders(cfg, hist + [dict(rec, orders={})], t, s, ov[s][t])
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
    bad = [k for k in overrides if k not in M.SIDES]
    if bad or not any(k in overrides for k in M.SIDES):
        raise GameError('whatif expects {"boeing": {"<turn>": orders}, "airbus": {"<turn>": orders}}; '
                        f"got top-level keys {sorted(overrides)}")
    for s_ in M.SIDES:
        for t in (overrides.get(s_) or {}):
            if not str(t).isdigit():
                raise GameError(f'whatif: "{s_}" must map turn numbers to orders, e.g. {{"{s_}": {{"2": {{...}}}}}}; got key {t!r}')
    hist, notes = _apply_overrides(st, overrides, args.side)
    mask = M.belief_mask(cfg, st["history"] + pending_record(st), args.side)
    r = M.strip_exact(M.evaluate(cfg, M.build_world(cfg, hist, mask)))
    base = M.strip_exact(M.evaluate(cfg, M.build_world(cfg, st["history"] + pending_record(st), mask)))
    res = {"assumption": "Turns you did not override keep their recorded orders (past) or no new moves (current/future).",
           "notes": notes, "shares": r["shares"]}
    for s in M.SIDES:
        res[s] = r[s]
        res[s]["change_vs_current_projection_b"] = round(r[s]["delta_pv_b"] - base[s]["delta_pv_b"], 3)
    if args.side in M.SIDES:
        opp = M.other(args.side)
        res[opp]["note"] = "Estimate from your information set."
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
    canons, texts, errs, warns = {}, {}, {}, {}
    for side in M.SIDES:
        if side not in req:
            errs[side] = [f"missing '{side}' orders"]
            continue
        canons[side], errs[side], warns[side], texts[side] = _orders_and_text(st, side, req[side])
    if any(errs.values()):
        out({"status": "invalid", "turn": k, "errors": {s: e for s, e in errs.items() if e}})
        sys.exit(2)
    if args.expect_digest:
        want = dict(part.split("=", 1) for part in args.expect_digest.split(",") if "=" in part)
        got = {s: M.orders_digest(s, canons[s]) for s in M.SIDES}
        bad = [s for s in M.SIDES if want.get(s) != got[s]]
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
    rec["projection"] = {s: {"delta_pv_b": proj[s]["delta_pv_b"], "components_pv_b": proj[s]["components_pv_b"]} for s in M.SIDES}
    st["history"].append(rec)
    st["pending_injects"] = []
    done = k >= st["turns_total"]
    st["status"] = "complete" if done else "in_progress"
    st["current_turn"] = k + 1
    save_state(st)
    result = {
        "status": "ok", "turn": k, "orders_digest": {s: M.orders_digest(s, canons[s]) for s in M.SIDES},
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
        "final": {s: ev[s] for s in M.SIDES}, "shares": ev["shares"],
        "trajectory": [{"turn": r["turn"], "projection": r.get("projection")} for r in st["history"]],
        "turns": [{"turn": r["turn"], "years": r.get("years"), "injects": r.get("injects", []), "orders": r["orders"],
                   "statements": r.get("statements", {}), "market": r.get("market", {}),
                   "market_narrative": r.get("market_narrative", "")} for r in st["history"]],
        "events": w.events,
        "delay_tactics_turns": w.delay_turns, "poaching_turns": w.poaching_turns,
        "delay_tactics_exposed_year": w.exposure_year,
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
    L.append("## Projection after each turn")
    L.append("")
    L.append("| Turn | Boeing | Airbus |")
    L.append("|---|---:|---:|")
    for t in rep["trajectory"]:
        p = t["projection"] or {}
        L.append(f"| T{t['turn']} | {p.get('boeing', {}).get('delta_pv_b', 0):+.2f} | {p.get('airbus', {}).get('delta_pv_b', 0):+.2f} |")
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
    L.append("## Market share (Boeing / Airbus)")
    L.append("")
    yrs = list(rep["shares"]["nb"].keys())
    L.append("| Segment | " + " | ".join(yrs) + " |")
    L.append("|---|" + "---:|" * len(yrs))
    for seg in M.SEGMENTS:
        L.append(f"| {cfg['segments'][seg]['label']} | " + " | ".join(
            f"{rep['shares'][seg][y]['boeing'] * 100:.1f} / {rep['shares'][seg][y]['airbus'] * 100:.1f}" for y in yrs) + " |")
    L.append("")
    L.append("## Orders by turn")
    L.append("")
    for t in rep["turns"]:
        inj = ", ".join(cfg["injects"]["deck"][i]["title"] for i in t["injects"]) or "none"
        L.append(f"**Turn {t['turn']} ({t['years'][0]}-{t['years'][1]})**, inject: {inj}")
        L.append("")
        for s in M.SIDES:
            L.append(f"- {cfg['players'][s]['label']}: {S.describe_orders(cfg, s, t['orders'][s])}")
        if t["market"].get("capture_mult"):
            L.append(f"- Market capture multipliers: " + ", ".join(f"{k} x{v:.2f}" for k, v in t["market"]["capture_mult"].items()))
        L.append("")
    L.append(f"Delay Tactics used in turns: {rep['delay_tactics_turns'] or 'none'}; "
             f"exposed: {rep['delay_tactics_exposed_year'] or 'no'}. Poaching used in turns: {rep['poaching_turns'] or 'none'}.")
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
        for s in M.SIDES:
            sc["summary"][s]["final_delta_pv_b"] = eq.get("actual_play", {}).get(s)
            sc["summary"][s]["hindsight_regret_b"] = (eq.get("regret_vs_actual", {}).get(s) or {}).get("regret_b")
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
    ap = argparse.ArgumentParser(prog="python3 -m wargame.engine", description="Boeing vs Airbus war-game engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="create a run (control)")
    p.add_argument("--scenario", default="base")
    p.add_argument("--turns", type=int)
    p.add_argument("--run-id")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--override", help="JSON deep-merged over the scenario config")
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
    p.add_argument("--side", default="control", choices=VIEWERS)
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
    p.add_argument("--side", required=True, choices=M.SIDES)
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("options", help="this turn's stage game")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=VIEWERS)
    p.add_argument("--compact", action="store_true", help="omit the full matrix")
    p.set_defaults(fn=cmd_options)

    p = sub.add_parser("whatif", help="evaluate order overrides from stdin: {\"boeing\": {\"2\": orders}, \"airbus\": {...}}")
    p.add_argument("--run", required=True)
    p.add_argument("--side", required=True, choices=VIEWERS)
    p.set_defaults(fn=cmd_whatif)

    p = sub.add_parser("adjudicate", help="apply both sides' orders and the market reaction from stdin (control)")
    p.add_argument("--run", required=True)
    p.add_argument("--turn", type=int)
    p.add_argument("--expect-digest", help="boeing=<hex>,airbus=<hex>; refuse to adjudicate if the orders differ")
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
    p.add_argument("--side", required=True, choices=M.SIDES)
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
