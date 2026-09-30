"""Deterministic adjudication model for the Boeing vs Airbus war game.

Agents choose moves; this module decides what those moves are worth. Every
number the war game reports must come from here, never from an agent.

Money is $B in constant 2026 dollars. A player's payoff ("delta PV") is the
present value, to years.pv_base at that player's WACC, of its operating-profit
stream minus the status-quo stream (nobody moves, same injects), less
alpha-loaded capex, alpha-loaded strain, and tactic costs. The components
always sum exactly to the total.
"""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
SIDES = ("boeing", "airbus")
SEGMENTS = ("nb", "wb")
NEVER = 10**6  # EIS of a program that does not exist
KEY_YEARS = (2030, 2035, 2040, 2045, 2050, 2060)


def other(side):
    return "airbus" if side == "boeing" else "boeing"


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def list_scenarios():
    d = os.path.join(HERE, "scenarios")
    out = {}
    for name in sorted(os.listdir(d)):
        if name.endswith(".json"):
            with open(os.path.join(d, name)) as f:
                sc = json.load(f)
            out[name[:-5]] = {"title": sc.get("title", name[:-5]), "narrative": sc.get("narrative", "")}
    return out


def load_config(scenario="base", overrides=None):
    with open(os.path.join(HERE, "config", "default.json")) as f:
        cfg = json.load(f)
    path = os.path.join(HERE, "scenarios", f"{scenario}.json")
    if not os.path.exists(path):
        raise ValueError(f"unknown scenario '{scenario}'; available: {', '.join(list_scenarios())}")
    with open(path) as f:
        sc = json.load(f)
    cfg = deep_merge(cfg, sc.get("overrides", {}))
    if overrides:
        cfg = deep_merge(cfg, overrides)
    cfg["scenario"] = {"id": scenario, "title": sc.get("title", scenario), "narrative": sc.get("narrative", "")}
    return cfg


def turn_years(cfg, turn):
    for t in cfg["turns"]:
        if t["turn"] == turn:
            return t["years"][0], t["years"][1]
    raise ValueError(f"turn {turn} is not defined in the config")


def programs_of(cfg, side):
    return [pid for pid, p in cfg["programs"].items() if p["owner"] == side]


def program_for(cfg, side, seg):
    for pid, p in cfg["programs"].items():
        if p["owner"] == side and p["segment"] == seg:
            return pid
    return None


def empty_orders(side):
    base = {"launch": [], "cancel": []}
    if side == "boeing":
        base["rate_increase"] = False
    else:
        base["delay_tactics"] = False
        base["poaching"] = False
    return base


# ---------------------------------------------------------------------------
# World state derived from the order history
# ---------------------------------------------------------------------------

@dataclass
class Program:
    pid: str
    owner: str
    segment: str
    launch_year: int
    launch_turn: int
    base_dev_years: int
    extra_dev_years: int  # dev years added at launch (injects, engine choice)
    variant: str | None
    engine: str
    slip_years: int = 0  # slips after launch (Delay Tactics, injects)
    delay_slip_years: int = 0
    slips: list = field(default_factory=list)
    cancelled_year: int | None = None
    capture_mult: float = 1.0  # market-cell reaction

    @property
    def eis(self):
        return self.launch_year + self.base_dev_years + self.extra_dev_years + self.slip_years

    @property
    def dev_end(self):
        """First year the program is no longer in development."""
        if self.cancelled_year is not None:
            return min(self.cancelled_year, self.eis)
        return self.eis

    def in_service(self, y):
        return self.cancelled_year is None and y >= self.eis

    def in_development_during(self, a, b):
        return self.launch_year <= b and self.dev_end > a

    def status(self, year):
        if self.cancelled_year is not None:
            return "cancelled"
        return "in service" if year >= self.eis else "in development"


@dataclass
class World:
    cfg: dict
    programs: dict = field(default_factory=dict)
    rate_year: int | None = None
    delay_turns: list = field(default_factory=list)
    poaching_turns: list = field(default_factory=list)
    exposure_year: int | None = None
    exposure_turn: int | None = None
    cost_events: list = field(default_factory=list)
    injects: list = field(default_factory=list)
    tech_ready_add: dict = field(default_factory=lambda: {"nb": 0, "wb": 0})
    strain_mults: list = field(default_factory=list)  # (from_year, mult)
    units_mults: list = field(default_factory=list)  # (seg, y0, y1, mult)
    margin_adds: list = field(default_factory=list)  # (player, seg, kind, y0, y1, pp)
    share_shifts: list = field(default_factory=list)  # (seg, to_player, pp, y0, y1)
    dev_years_add: dict = field(default_factory=lambda: {"boeing": 0, "airbus": 0})
    events: list = field(default_factory=list)  # adjudication log with visibility

    def prog(self, side, seg):
        pid = program_for(self.cfg, side, seg)
        return self.programs.get(pid) if pid else None

    def event(self, turn, text, visibility="public", side=None):
        self.events.append({"turn": turn, "text": text, "visibility": visibility, "side": side})


def _apply_inject(w, turn, a, iid):
    deck = w.cfg["injects"]["deck"]
    if iid not in deck:
        raise ValueError(f"unknown inject '{iid}'")
    inj = deck[iid]
    w.injects.append({"turn": turn, "id": iid, "title": inj["title"], "narrative": inj["narrative"]})
    w.event(turn, f"Inject: {inj['title']} - {inj['narrative']}")
    for e in inj["effects"]:
        t = e["type"]
        rng = e.get("years_from_turn_start", [0, 99])
        y0, y1 = a + rng[0], a + rng[1]
        if t == "units_mult":
            w.units_mults.append((e["segment"], y0, y1, float(e["mult"])))
        elif t == "margin_add":
            w.margin_adds.append((e.get("player", "all"), e.get("segment", "all"), e.get("kind", "all"), y0, y1, float(e["pp"])))
        elif t == "share_shift":
            w.share_shifts.append((e["segment"], e["to_player"], float(e["pp"]), y0, y1))
        elif t == "tech_ready_add":
            segs = SEGMENTS if e.get("segment", "all") == "all" else (e["segment"],)
            for s in segs:
                w.tech_ready_add[s] += int(e["years"])
        elif t == "strain_mult":
            w.strain_mults.append((a, float(e["mult"])))
        elif t == "dev_years_add":
            players = SIDES if e.get("player", "all") == "all" else (e["player"],)
            yrs = int(e["years"])
            for p in players:
                w.dev_years_add[p] += yrs
                if e.get("applies_to", "all") in ("all", "in_development"):
                    for prog in w.programs.values():
                        if prog.owner == p and prog.cancelled_year is None and prog.eis > a:
                            prog.slip_years += yrs
                            prog.slips.append({"turn": turn, "years": yrs, "cause": inj["title"], "covert": False})
        else:
            raise ValueError(f"inject '{iid}' has unknown effect type '{t}'")


def build_world(cfg, history, masked_delay_turns=frozenset()):
    """Replay a history of turn records into a World.

    A turn record is {"turn": k, "injects": [ids], "orders": {side: canonical},
    "market": {"capture_mult": {program: mult}}}. Order within a turn:
    injects (known to both sides before they order), then both sides' orders,
    then Airbus tactics, then the market reaction.

    masked_delay_turns renders Boeing's (or the public's) belief: Delay Tactics
    in those turns keep their observable effect (the fps slip) but their cost
    and their count toward exposure are unknown to the viewer.
    """
    w = World(cfg=cfg)
    tac = cfg["tactics"]
    for rec in history:
        k = rec["turn"]
        a, b = turn_years(cfg, k)
        for iid in rec.get("injects", []):
            _apply_inject(w, k, a, iid)
        orders = rec.get("orders") or {}
        for side in SIDES:
            o = orders.get(side)
            if not o:
                continue
            for pid in o.get("cancel", []):
                p = w.programs[pid]
                p.cancelled_year = a
                w.event(k, f"{cfg['players'][side]['label']} cancels {cfg['programs'][pid]['label']} (sunk capex lost).")
            for L in o.get("launch", []):
                pc = cfg["programs"][L["program"]]
                eng = cfg["engine_options"][pc["segment"]][L["engine"]]
                p = Program(
                    pid=L["program"], owner=side, segment=pc["segment"], launch_year=L["year"], launch_turn=k,
                    base_dev_years=pc["dev_years"], extra_dev_years=w.dev_years_add[side] + eng["eis_add"],
                    variant=L.get("variant"), engine=L["engine"],
                )
                w.programs[p.pid] = p
                vtxt = f" as a {pc['variants'][p.variant]['label']}" if p.variant else ""
                w.event(k, f"{cfg['players'][side]['label']} launches {pc['label']}{vtxt} in {p.launch_year} "
                           f"with the {eng['label']}; planned entry into service {p.eis}.")
            if side == "boeing" and o.get("rate_increase") and w.rate_year is None:
                w.rate_year = a
                w.event(k, f"Boeing commits to a 737 rate increase from {a} (extra share from {a + tac['rate_increase']['lag_years']}).")
        ao = orders.get("airbus") or {}
        if ao.get("delay_tactics"):
            dt = tac["delay_tactics"]
            if k not in masked_delay_turns:
                w.delay_turns.append(k)
                w.cost_events.append({"player": "airbus", "year": a, "amount_b": dt["cost_b_per_turn"], "kind": "tactics",
                                      "label": "Delay Tactics", "covert": True})
                w.event(k, "Airbus runs Delay Tactics against fps.", visibility="private", side="airbus")
            tgt = w.programs.get(dt["target_program"])
            if tgt and tgt.in_development_during(a, b) and tgt.delay_slip_years < dt["max_total_slip"]:
                s = min(dt["slip_years_per_turn"], dt["max_total_slip"] - tgt.delay_slip_years)
                tgt.slip_years += s
                tgt.delay_slip_years += s
                cause = dt["public_cause_unexposed"] if k in masked_delay_turns else "Delay Tactics"
                tgt.slips.append({"turn": k, "years": s, "cause": cause, "covert": True})
                w.event(k, f"fps entry into service slips {s} year(s) to {tgt.eis}: {dt['public_cause_unexposed']}.")
            if w.exposure_year is None and len(w.delay_turns) >= dt["exposure_after_turns"]:
                w.exposure_year = b + 1
                w.exposure_turn = k
                w.event(k, f"Airbus Delay Tactics are exposed (used in turns {w.delay_turns}); "
                           f"reputational penalty of {dt['exposure_share_pp']} pp narrowbody share for {dt['exposure_years']} years.")
        if ao.get("poaching"):
            pt = tac["poaching"]
            w.poaching_turns.append(k)
            w.cost_events.append({"player": "airbus", "year": a, "amount_b": pt["cost_b_per_turn"], "kind": "tactics",
                                  "label": "Poaching", "covert": False})
            hit = [p for p in w.programs.values() if p.owner == "boeing" and p.in_development_during(a, b)]
            if hit:
                w.cost_events.append({"player": "boeing", "year": a, "amount_b": pt["victim_cost_b_per_turn"],
                                      "kind": "tactics", "label": "Talent lost to Airbus poaching", "covert": False})
                w.event(k, f"Airbus poaches Boeing engineers; Boeing programs in development ({', '.join(p.pid for p in hit)}) "
                           f"cost ${pt['victim_cost_b_per_turn']}B more.")
            else:
                w.event(k, "Airbus poaches Boeing engineers, but Boeing has no program in development to disrupt.")
            own = [p for p in w.programs.values() if p.owner == "airbus" and p.in_development_during(a, b)]
            if own:
                w.cost_events.append({"player": "airbus", "year": a, "amount_b": -pt["beneficiary_saving_b_per_turn"],
                                      "kind": "tactics", "label": "Poached talent speeds Airbus programs", "covert": False})
        mk = (rec.get("market") or {}).get("capture_mult", {}) or {}
        lo, hi = cfg["market"]["capture_mult_min"], cfg["market"]["capture_mult_max"]
        for pid, m in mk.items():
            if pid in w.programs:
                w.programs[pid].capture_mult = min(hi, max(lo, float(m)))
    return w


# ---------------------------------------------------------------------------
# Payoff evaluation
# ---------------------------------------------------------------------------

def _sum_in_range(items, y):
    return sum(v for (y0, y1, v) in items if y0 <= y <= y1)


def evaluate(cfg, world):
    """Return per-side payoffs, components, programs and key-year shares."""
    y_start, y_end = cfg["years"]["start"], cfg["years"]["end"]
    pv_base = cfg["years"]["pv_base"]
    years = range(y_start, y_end + 1)
    seg_cfg = cfg["segments"]
    tac = cfg["tactics"]
    rt = tac["rate_increase"]
    dt = tac["delay_tactics"]

    def units(seg, y):
        u = seg_cfg[seg]["units_per_year"]
        for (s, y0, y1, m) in world.units_mults:
            if s == seg and y0 <= y <= y1:
                u *= m
        return u

    def world_shift_boeing(seg, y):
        d = 0.0
        for (s, to, pp, y0, y1) in world.share_shifts:
            if s == seg and y0 <= y <= y1:
                d += pp if to == "boeing" else -pp
        return d / 100.0

    def move_shift_boeing(seg, y):
        d = 0.0
        if seg == "nb" and world.rate_year is not None and y >= world.rate_year + rt["lag_years"]:
            d += rt["share_pp"]
        if seg == "nb" and world.exposure_year is not None and world.exposure_year <= y < world.exposure_year + dt["exposure_years"]:
            d += dt["exposure_share_pp"]
        return d / 100.0

    def eis_of(p):
        return p.eis if (p is not None and p.cancelled_year is None) else NEVER

    def capture_speed(p):
        eng = cfg["engine_options"][p.segment][p.engine]
        return seg_cfg[p.segment]["capture_pp_per_year"] * p.capture_mult * eng["capture_mult"] / 100.0

    def shares(seg, y):
        sq_b = min(1.0, max(0.0, seg_cfg[seg]["sq_share"]["boeing"] + world_shift_boeing(seg, y)))
        s_b = min(1.0, max(0.0, sq_b + move_shift_boeing(seg, y)))
        pb, pa = world.prog("boeing", seg), world.prog("airbus", seg)
        eb, ea = eis_of(pb), eis_of(pa)
        if eb < ea:
            n = max(0, min(y, ea) - eb)
            cap = seg_cfg[seg]["leader_cap"]["boeing"]
            if n and s_b < cap:
                s_b = min(cap, s_b + capture_speed(pb) * n)
        elif ea < eb:
            s_a = 1.0 - s_b
            n = max(0, min(y, eb) - ea)
            cap = seg_cfg[seg]["leader_cap"]["airbus"]
            if n and s_a < cap:
                s_a = min(cap, s_a + capture_speed(pa) * n)
            s_b = 1.0 - s_a
        return {"boeing": s_b, "airbus": 1.0 - s_b}, {"boeing": sq_b, "airbus": 1.0 - sq_b}

    def margin_adds(side, seg, kind, y):
        pp = 0.0
        for (pl, s, k, y0, y1, v) in world.margin_adds:
            if pl in ("all", side) and s in ("all", seg) and k in ("all", kind) and y0 <= y <= y1:
                pp += v
        return pp / 100.0

    def margin(side, seg, y):
        p = world.prog(side, seg)
        inc = cfg["incumbents"][side][seg]["margin"]
        sq_m = inc + margin_adds(side, seg, "incumbent", y)
        if p is not None and p.in_service(y):
            pc = cfg["programs"][p.pid]
            rival = world.prog(other(side), seg)
            m = pc["margin_both"] if (rival is not None and rival.in_service(y)) else pc["margin_alone"]
            ready = pc["tech_ready_year"] + world.tech_ready_add[seg]
            m -= pc["early_penalty_pp_per_year"] / 100.0 * max(0, ready - p.eis)
            m += cfg["engine_options"][seg][p.engine]["margin_pp"] / 100.0
            m += margin_adds(side, seg, "new", y)
            if p.variant:
                m *= 1.0 - pc["variants"][p.variant]["margin_share_partner"]
            return m, sq_m
        return sq_m, sq_m

    def alpha(side, y):
        a = cfg["players"][side]["alpha"]
        if side == "boeing" and world.rate_year is not None and world.rate_year <= y < world.rate_year + rt["alpha_window_years"]:
            a += rt["alpha_add"]
        return a

    def df(side, y):
        return (1.0 + cfg["players"][side]["wacc"]) ** -(y - pv_base)

    def strain_mult(y):
        m = 1.0
        for (y0, mult) in world.strain_mults:
            if y >= y0:
                m *= mult
        return m

    # Capex and strain schedules (nominal, before alpha loading).
    capex = {s: {} for s in SIDES}
    strain = {s: {} for s in SIDES}
    for p in world.programs.values():
        pc = cfg["programs"][p.pid]
        share = pc["variants"][p.variant]["capex_share_partner"] if p.variant else 0.0
        c = pc["capex_b"] * (1.0 - share)
        for i, y in enumerate(range(p.launch_year, p.eis)):
            if p.cancelled_year is not None and y >= p.cancelled_year:
                break
            amt = c / p.base_dev_years if i < p.base_dev_years else c * cfg["extension_capex_frac_per_year"]
            capex[p.owner][y] = capex[p.owner].get(y, 0.0) + amt
    if world.rate_year is not None:
        for y in range(world.rate_year, world.rate_year + rt["capex_years"]):
            capex["boeing"][y] = capex["boeing"].get(y, 0.0) + rt["capex_b"] / rt["capex_years"]
    for side in SIDES:
        nb, wb = world.prog(side, "nb"), world.prog(side, "wb")
        if nb is None or wb is None:
            continue
        start, end = max(nb.launch_year, wb.launch_year), min(nb.dev_end, wb.dev_end)
        overlap = end - start
        if overlap <= 0:
            continue
        relief = max(cfg["programs"][p.pid]["variants"][p.variant]["strain_relief"] if p.variant else 0.0 for p in (nb, wb))
        nominal = cfg["strain"]["full_overlap_b"] * min(1.0, overlap / cfg["strain"]["norm_years"]) * (1.0 - relief)
        for y in range(start, end):
            strain[side][y] = strain[side].get(y, 0.0) + nominal / overlap * strain_mult(y)

    out = {}
    share_paths = {seg: {} for seg in SEGMENTS}
    for y in years:
        for seg in SEGMENTS:
            share_paths[seg][y] = shares(seg, y)
    for side in SIDES:
        comp = {"nb_operating": 0.0, "wb_operating": 0.0, "capex": 0.0, "strain": 0.0, "tactics": 0.0}
        undiscounted = {"nb_operating": 0.0, "wb_operating": 0.0, "capex": 0.0, "strain": 0.0, "tactics": 0.0}
        for y in years:
            d = df(side, y)
            for seg in SEGMENTS:
                sh, sq_sh = share_paths[seg][y]
                m, sq_m = margin(side, seg, y)
                rev_unit = units(seg, y) * seg_cfg[seg]["net_price_m"] / 1000.0
                delta = rev_unit * (sh[side] * m - sq_sh[side] * sq_m)
                comp[f"{seg}_operating"] += delta * d
                undiscounted[f"{seg}_operating"] += delta
            ld = capex[side].get(y, 0.0) * (1.0 + alpha(side, y))
            ls = strain[side].get(y, 0.0) * (1.0 + alpha(side, y))
            comp["capex"] -= ld * d
            comp["strain"] -= ls * d
            undiscounted["capex"] -= ld
            undiscounted["strain"] -= ls
        for ev in world.cost_events:
            if ev["player"] != side:
                continue
            comp["tactics"] -= ev["amount_b"] * df(side, ev["year"])
            undiscounted["tactics"] -= ev["amount_b"]
        total = sum(comp.values())
        progs = []
        for pid in programs_of(cfg, side):
            p = world.programs.get(pid)
            if p is None:
                continue
            pc = cfg["programs"][pid]
            m_now, _ = margin(side, p.segment, max(p.eis, y_start)) if p.cancelled_year is None else (None, None)
            progs.append({
                "program": pid, "label": pc["label"], "segment": p.segment, "launch_year": p.launch_year,
                "eis": p.eis if p.cancelled_year is None else None, "planned_eis_at_launch": p.launch_year + p.base_dev_years + p.extra_dev_years,
                "cancelled_year": p.cancelled_year, "variant": p.variant, "engine": p.engine,
                "engine_label": cfg["engine_options"][p.segment][p.engine]["label"],
                "capture_mult": round(p.capture_mult, 3), "margin_at_eis": None if m_now is None else round(m_now, 4),
                "slips": p.slips,
            })
        out[side] = {
            "delta_pv_b": round(total, 3),
            "components_pv_b": {k: round(v, 3) for k, v in comp.items()},
            "undiscounted_b": {k: round(v, 3) for k, v in undiscounted.items()},
            "programs": progs,
        }
        out[side]["_exact"] = total
    out["shares"] = {
        seg: {str(y): {s: round(share_paths[seg][y][0][s], 4) for s in SIDES} for y in KEY_YEARS if y_start <= y <= y_end}
        for seg in SEGMENTS
    }
    return out


def payoff(cfg, history, masked_delay_turns=frozenset()):
    """Exact (unrounded) payoffs for a history: {"boeing": x, "airbus": y}."""
    r = evaluate(cfg, build_world(cfg, history, masked_delay_turns))
    return {s: r[s]["_exact"] for s in SIDES}


def belief_mask(cfg, history, viewer):
    """Delay-Tactics turns hidden from `viewer` ("boeing", "market", or "public").

    Airbus, control and analyst see everything. Everyone else sees the fps
    slips but not their cause, cost or exposure count until exposure.
    """
    if viewer in ("airbus", "control", "analyst"):
        return frozenset()
    w = build_world(cfg, history)
    if w.exposure_year is not None:
        return frozenset()
    return frozenset(w.delay_turns)


def strip_exact(result):
    for s in SIDES:
        result.get(s, {}).pop("_exact", None)
    return result


# ---------------------------------------------------------------------------
# Order validation
# ---------------------------------------------------------------------------

TEXT_FIELDS = ("public_statement", "rationale")


def validate_orders(cfg, history, turn, side, orders):
    """Check one side's orders for `turn` against the world built from `history`.

    Returns (canonical_orders, errors, warnings). Canonical orders carry only
    the mechanical fields; text fields are kept separately by the caller.
    """
    errors, warnings = [], []
    if side not in SIDES:
        return None, [f"unknown side '{side}'"], []
    if not isinstance(orders, dict):
        return None, ["orders must be a JSON object"], []
    a, b = turn_years(cfg, turn)
    w = build_world(cfg, history)
    canon = empty_orders(side)
    allowed = set(canon) | set(TEXT_FIELDS) | {"side"}
    for k in orders:
        if k not in allowed:
            warnings.append(f"ignored unknown field '{k}'")
    if orders.get("side") not in (None, side):
        errors.append(f"orders are labelled for side '{orders.get('side')}' but were submitted for '{side}'")

    launches = orders.get("launch", []) or []
    cancels = orders.get("cancel", []) or []
    if not isinstance(launches, list) or not isinstance(cancels, list):
        return None, ["'launch' and 'cancel' must be lists"], warnings
    mine = programs_of(cfg, side)
    seen = set()
    for L in launches:
        if isinstance(L, str):
            L = {"program": L}
        if not isinstance(L, dict) or "program" not in L:
            errors.append(f"launch entry {L!r} must be an object with a 'program'")
            continue
        pid = L["program"]
        if pid not in mine:
            errors.append(f"'{pid}' is not a {side} program (yours: {', '.join(mine)})")
            continue
        if pid in seen:
            errors.append(f"'{pid}' is launched twice")
            continue
        seen.add(pid)
        if pid in w.programs:
            errors.append(f"'{pid}' was already launched in turn {w.programs[pid].launch_turn}; a program can be launched once")
            continue
        pc = cfg["programs"][pid]
        year = L.get("year", a)
        if not isinstance(year, int) or not (a <= year <= b):
            errors.append(f"launch year for '{pid}' must be an integer in this turn's years {a}-{b} (got {year!r})")
            continue
        engine = L.get("engine") or pc["default_engine"]
        if engine not in cfg["engine_options"][pc["segment"]]:
            errors.append(f"engine '{engine}' is not available for {pc['segment'].upper()} "
                          f"(options: {', '.join(cfg['engine_options'][pc['segment']])})")
            continue
        entry = {"program": pid, "year": year, "engine": engine}
        requested = L.get("variant")
        if requested in ("", "none"):
            requested = None
        if "variants" in pc:
            variant = requested or pc["default_variant"]
            if variant not in pc["variants"]:
                errors.append(f"variant '{variant}' is not valid for '{pid}' (options: {', '.join(pc['variants'])})")
                continue
            entry["variant"] = variant
        elif requested:
            errors.append(f"'{pid}' has no variants (use \"none\")")
            continue
        canon["launch"].append(entry)
    for pid in cancels:
        if pid not in mine:
            errors.append(f"cannot cancel '{pid}': not a {side} program")
        elif pid not in w.programs:
            errors.append(f"cannot cancel '{pid}': it has not been launched")
        elif pid in seen:
            errors.append(f"cannot launch and cancel '{pid}' in the same turn")
        elif w.programs[pid].cancelled_year is not None:
            errors.append(f"'{pid}' is already cancelled")
        elif w.programs[pid].eis <= a:
            errors.append(f"cannot cancel '{pid}': it entered service in {w.programs[pid].eis}")
        elif pid not in canon["cancel"]:
            canon["cancel"].append(pid)
    for flag, owner in (("rate_increase", "boeing"), ("delay_tactics", "airbus"), ("poaching", "airbus")):
        if flag not in orders:
            continue
        v = orders[flag]
        if not isinstance(v, bool):
            errors.append(f"'{flag}' must be true or false")
        elif owner != side:
            if v:
                errors.append(f"'{flag}' is an {owner} lever")
        else:
            canon[flag] = v
    if side == "boeing" and canon.get("rate_increase") and w.rate_year is not None:
        warnings.append(f"rate increase already committed in {w.rate_year}; no additional effect")
    canon["launch"].sort(key=lambda e: e["program"])
    canon["cancel"].sort()
    return (canon if not errors else None), errors, warnings


def canonical_key(side, o):
    """ASCII key of the mechanical content of canonical orders (mirrored in the workflow script)."""
    launches = ";".join(f"{L['program']}/{L.get('variant') or '-'}/{L['engine']}/{L['year']}"
                        for L in sorted(o.get("launch", []), key=lambda e: e["program"]))
    cancels = ",".join(sorted(set(o.get("cancel", []))))
    flags = ("rate_increase",) if side == "boeing" else ("delay_tactics", "poaching")
    fl = ",".join(f"{f}:{int(bool(o.get(f)))}" for f in flags)
    return f"{side}|L={launches}|C={cancels}|F={fl}"


def orders_digest(side, o):
    """32-bit FNV-1a of canonical_key, as 8 hex digits."""
    h = 0x811C9DC5
    for ch in canonical_key(side, o).encode("ascii", "replace"):
        h ^= ch
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"
