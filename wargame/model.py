"""Deterministic adjudication model for the Boeing vs Airbus war game.

Agents choose moves; this module decides what those moves are worth. Every
number the war game reports must come from here, never from an agent.

Money is $B in constant 2026 dollars. A player's payoff ("delta PV") is the
present value, to years.pv_base at that player's WACC, of its operating-profit
stream minus the status-quo stream (nobody moves, same injects), less
alpha-loaded capex, alpha-loaded strain, and tactic costs. The components
always sum exactly to the total.

Optional supplier players (the engine makers Rolls-Royce and Pratt & Whitney,
cfg["suppliers"][<id>], each switched on with "active": true) sit on top of the two airframers. The supplier
launches engine programs that airframers can then select; its payoff is the
lifecycle value of the engines it delivers (units x share x engines per aircraft
x its fit on each airframe x value per engine) versus the status quo, less its
own alpha-loaded capex and strain. With no active supplier the game is exactly
the two-player game.
"""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
SIDES = ("boeing", "airbus")
SUPPLIERS = ("rolls_royce", "pratt_whitney", "cfm")
# One-turn boolean levers of each supplier: its one-time commitments (upgrades, CFM/GE's Embraer
# partnership and emissions lobbying) and, for Pratt & Whitney, joining Rolls-Royce's UltraFan
# narrowbody Joint Venture.
SUPPLIER_FLAGS = {"rolls_royce": ("t1000_upgrade",), "pratt_whitney": ("gtf_upgrade", "join_rr_jv"),
                  "cfm": ("leap_upgrade", "genx_upgrade", "embraer_partner", "lobby_emissions")}
SEGMENTS = ("nb", "wb")
NEVER = 10**6  # EIS of a program that does not exist
KEY_YEARS = (2030, 2035, 2040, 2045, 2050, 2060)


def other(side):
    return "airbus" if side == "boeing" else "boeing"


def active_suppliers(cfg):
    return tuple(s for s in SUPPLIERS if cfg.get("suppliers", {}).get(s, {}).get("active"))


def players(cfg):
    """Everyone who submits orders in this game: the two airframers plus active suppliers."""
    return SIDES + active_suppliers(cfg)


def player_label(cfg, side):
    if side in SIDES:
        return cfg["players"][side]["label"]
    return cfg["suppliers"][side]["label"]


def supplier_requirement(cfg, seg, engine):
    """(supplier, supplier program) an airframer engine option depends on, if that supplier plays."""
    for sup in active_suppliers(cfg):
        for spid, spc in cfg["suppliers"][sup]["programs"].items():
            if spc["segment"] == seg and spc["engine_option"] == engine:
                return sup, spid
    return None


def sparam(cfg, sup, spid, variant, key, default=None):
    """A supplier program parameter, overridden by its variant when the variant sets it."""
    spc = cfg["suppliers"][sup]["programs"][spid]
    if variant and key in spc.get("variants", {}).get(variant, {}):
        return spc["variants"][variant][key]
    return spc.get(key, default)


def supplier_commitments(cfg, sup):
    """A supplier's one-time commitment levers, each a dict with 'flag' and 'kind' (upgrade, partner_volume, lobby)."""
    scfg = cfg.get("suppliers", {}).get(sup) or {}
    out = []
    if scfg.get("upgrade"):
        out.append(dict(scfg["upgrade"], kind="upgrade"))
    out += [dict(u, kind="upgrade") for u in scfg.get("upgrades", [])]
    if scfg.get("partner_volume"):
        out.append(dict(scfg["partner_volume"], kind="partner_volume"))
    if scfg.get("lobby"):
        out.append(dict(scfg["lobby"], kind="lobby"))
    return out


def engine_maker(cfg, seg, engine):
    return cfg["engine_options"][seg][engine].get("maker")


def incumbent_fits(cfg, world, y):
    """Each engine maker's fit on each airframer's incumbent fleet in year y: {maker: {(side, seg): fit}}.

    Starts from suppliers.<maker>.incumbent_fit; every committed upgrade of an active supplier then moves
    fit_pp of its fleet from the maker named in 'from' to its owner, from commitment + lag_years."""
    sups = {s: c for s, c in cfg.get("suppliers", {}).items() if isinstance(c, dict) and "incumbent_fit" in c}
    fits = {s: {(side, seg): c["incumbent_fit"][side][seg] for side in SIDES for seg in SEGMENTS} for s, c in sups.items()}
    for s in active_suppliers(cfg):
        for c in supplier_commitments(cfg, s):
            if c["kind"] != "upgrade":
                continue
            yr = world.commit_years.get((s, c["flag"]))
            if yr is None or y < yr + c["lag_years"]:
                continue
            key = (c["fit_side"], c["segment"])
            pp = c["fit_pp"] / 100.0
            src = c.get("from")
            if src in fits:
                pp = min(pp, fits[src][key])
                fits[src][key] -= pp
            fits[s][key] = min(1.0, fits[s][key] + pp)
    return fits


def lobby_effect(cfg, world, engine, y=None):
    """(margin_pp, capture_mult) a supplier's emissions lobbying gives airframes flying `engine`."""
    pp, mult = 0.0, 1.0
    for s in active_suppliers(cfg):
        lb = cfg["suppliers"][s].get("lobby")
        yr = world.commit_years.get((s, lb["flag"])) if lb else None
        if lb and yr is not None and lb["engine"] == engine:
            mult *= lb.get("capture_mult", 1.0)
            if y is None or y >= yr + lb.get("lag_years", 0):
                pp += lb.get("margin_pp", 0.0)
    return pp, mult


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
    ov = sc.get("overrides", {})
    for key in sc.get("replace", []):
        cfg[key] = copy.deepcopy(ov[key])
    cfg = deep_merge(cfg, {k: v for k, v in ov.items() if k not in sc.get("replace", [])})
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


VARIANT_KEYS = ("dev_years", "capex_b", "margin_alone", "margin_both", "tech_ready_year",
                "early_penalty_pp_per_year", "capture_mult", "tech_level")


def pparam(cfg, pid, variant, key, default=None):
    """A program parameter, overridden by the chosen variant when the variant sets it."""
    pc = cfg["programs"][pid]
    if variant and key in pc.get("variants", {}).get(variant, {}):
        return pc["variants"][variant][key]
    return pc.get(key, default)


def vparam(cfg, pid, variant, key):
    """Joint-venture style variant terms (partner shares, strain relief); 0 when absent."""
    if not variant:
        return 0.0
    return cfg["programs"][pid].get("variants", {}).get(variant, {}).get(key, 0.0)


def tactic_enabled(cfg, name):
    return cfg["tactics"].get(name, {}).get("enabled", True)


def empty_orders(side):
    base = {"launch": [], "cancel": []}
    if side == "boeing":
        base["rate_increase"] = False
    elif side in SUPPLIERS:
        base.update({f: False for f in SUPPLIER_FLAGS[side]})
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
    supplier: str | None = None  # supplier whose engine program this airframe depends on
    supplier_program: str | None = None
    supplier_margin_pp: float = 0.0  # airframer margin from the supplier's terms
    engine_requested: str | None = None  # set when the requested engine was not available
    engine_wait: int = 0  # years the airframe waits for its engine to be ready
    engine_ready_year: int | None = None  # earliest entry into service the engine option allows (available_eis)
    ramp: str | None = None  # production ramp option (e.g. fps "7y" / "10y")

    @property
    def eis(self):
        return self.launch_year + self.base_dev_years + self.extra_dev_years + self.slip_years + self.engine_wait

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
class SupplierProgram:
    """An engine program launched by a supplier player (e.g. Rolls-Royce UltraFan)."""
    pid: str
    owner: str
    segment: str
    launch_year: int
    launch_turn: int
    dev_years: int
    variant: str | None
    terms: str
    slip_years: int = 0
    slips: list = field(default_factory=list)
    cancelled_year: int | None = None
    partner: str | None = None  # a supplier player that co-owns it as a Joint Venture partner

    @property
    def ready(self):
        """First year the engine can enter service on an airframe."""
        return self.launch_year + self.dev_years + self.slip_years

    @property
    def dev_end(self):
        if self.cancelled_year is not None:
            return min(self.cancelled_year, self.ready)
        return self.ready

    def live(self):
        return self.cancelled_year is None


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
    strain_mults: list = field(default_factory=list)  # (from_year, mult, player|"all")
    units_mults: list = field(default_factory=list)  # (seg, y0, y1, mult)
    margin_adds: list = field(default_factory=list)  # (player, seg, kind, y0, y1, pp)
    share_shifts: list = field(default_factory=list)  # (seg, to_player, pp, y0, y1, unless_launched, turn)
    dev_years_add: dict = field(default_factory=lambda: {"boeing": 0, "airbus": 0})
    events: list = field(default_factory=list)  # adjudication log with visibility
    sup_programs: dict = field(default_factory=dict)  # supplier engine programs by id
    upgrade_years: dict = field(default_factory=dict)  # supplier -> year of its first one-time upgrade
    commit_years: dict = field(default_factory=dict)  # (supplier, flag) -> year of a one-time commitment
    supplier_value_mults: list = field(default_factory=list)  # (supplier, kind, y0, y1, mult)

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
            # unless_launched: the shift does not hit the moving world if that program was launched
            # by the end of this turn (e.g. a customer defects unless Boeing commits to an answer).
            w.share_shifts.append((e["segment"], e["to_player"], float(e["pp"]), y0, y1, e.get("unless_launched"), turn))
        elif t == "tech_ready_add":
            segs = SEGMENTS if e.get("segment", "all") == "all" else (e["segment"],)
            for s in segs:
                w.tech_ready_add[s] += int(e["years"])
        elif t == "strain_mult":
            w.strain_mults.append((a, float(e["mult"]), e.get("player", "all")))
        elif t == "supplier_value_mult":
            w.supplier_value_mults.append((e.get("supplier", "rolls_royce"), e.get("kind", "all"), y0, y1, float(e["mult"])))
        elif t == "supplier_slip":
            yrs = int(e["years"])
            for sp in w.sup_programs.values():
                if sp.owner == e.get("supplier", "rolls_royce") and sp.live() and sp.ready > a:
                    sp.slip_years += yrs
                    sp.slips.append({"turn": turn, "years": yrs, "cause": inj["title"]})
                    w.event(turn, f"{player_label(w.cfg, sp.owner)} {w.cfg['suppliers'][sp.owner]['programs'][sp.pid]['label']} "
                                  f"slips {yrs} year(s); ready in {sp.ready}.")
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
    injects (known to both sides before they order), then supplier orders
    (engine commitments are in place before airframers' engine selections are
    resolved), then both sides' orders, then Airbus tactics, then the market
    reaction.

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
        for sup in active_suppliers(cfg):
            _apply_supplier_orders(w, k, a, sup, orders.get(sup), orders)
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
                seg = pc["segment"]
                engine = L["engine"]
                eng = cfg["engine_options"][seg][engine]
                requested, sup, spid, terms_pp, eis_add = None, None, None, 0.0, eng["eis_add"]
                tried = set()
                while True:
                    req = supplier_requirement(cfg, seg, engine)
                    if not req:
                        break
                    sp = w.sup_programs.get(req[1])
                    scfg = cfg["suppliers"][req[0]]
                    if sp is not None and sp.live():
                        # Engine timing comes from the supplier's program, not from eis_add.
                        sup, spid, eis_add = req[0], req[1], 0
                        terms_pp = scfg["terms"][sp.terms]["airframer_margin_pp"]
                        break
                    # The supplier has not committed to this engine: fall back to the segment's alternative
                    # (which may itself need another supplier's commitment, e.g. UltraFan -> CFM ducted -> LEAP derivative).
                    tried.add(engine)
                    fb = scfg["fallback_engine"][seg]
                    if fb in tried:
                        break
                    requested = requested or engine
                    w.event(k, f"{player_label(cfg, req[0])} has not committed to the {cfg['engine_options'][seg][engine]['label']}, "
                               f"so {cfg['players'][side]['label']}'s {pc['label']} falls back to the "
                               f"{cfg['engine_options'][seg][fb]['label']}.")
                    engine = fb
                    eng = cfg["engine_options"][seg][engine]
                    eis_add = eng["eis_add"]
                p = Program(
                    pid=L["program"], owner=side, segment=seg, launch_year=L["year"], launch_turn=k,
                    base_dev_years=pparam(cfg, L["program"], L.get("variant"), "dev_years"),
                    extra_dev_years=w.dev_years_add[side] + eis_add + int(pc.get("delay_years", 0)),
                    variant=L.get("variant"), engine=engine, supplier=sup, supplier_program=spid,
                    supplier_margin_pp=terms_pp, engine_requested=requested,
                    engine_ready_year=eng.get("available_eis"),
                    ramp=(L.get("ramp") or pc.get("default_ramp")) if pc.get("ramp_options") else None,
                )
                w.programs[p.pid] = p
                _update_engine_waits(w)
                vtxt = f" as a {pc['variants'][p.variant]['label']}" if p.variant else ""
                if p.ramp and p.ramp != pc.get("default_ramp"):
                    vtxt += f" with a {pc['ramp_options'][p.ramp]['label']}"
                wtxt = f" (waits {p.engine_wait} year(s) for the engine)" if p.engine_wait else ""
                w.event(k, f"{cfg['players'][side]['label']} launches {pc['label']}{vtxt} in {p.launch_year} "
                           f"with the {eng['label']}; planned entry into service {p.eis}{wtxt}.")
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
                _update_engine_waits(w)
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
        _update_engine_waits(w)
    return w


def _update_engine_waits(w):
    """An airframe cannot enter service before its engine is ready: its supplier's program, or the
    engine option's first available year (available_eis, e.g. the open fan)."""
    for p in w.programs.values():
        own = p.launch_year + p.base_dev_years + p.extra_dev_years + p.slip_years
        wait = 0
        if p.supplier_program:
            wait = max(0, w.sup_programs[p.supplier_program].ready - own)
        if p.engine_ready_year is not None:
            wait = max(wait, p.engine_ready_year - own)
        p.engine_wait = wait


def jv_partner_player(cfg, sup, spid, variant):
    """The active supplier player a Joint Venture variant needs as partner, if any."""
    partner = sparam(cfg, sup, spid, variant, "partner_player") if variant else None
    return partner if partner in active_suppliers(cfg) else None


def _apply_supplier_orders(w, k, a, sup, o, all_orders):
    cfg = w.cfg
    scfg = cfg["suppliers"][sup]
    lab = player_label(cfg, sup)
    o = o or {}
    for spid in o.get("cancel", []):
        sp = w.sup_programs[spid]
        sp.cancelled_year = a
        w.event(k, f"{lab} cancels the {scfg['programs'][spid]['label']} (sunk capex lost).")
    for L in o.get("launch", []):
        spid = L["program"]
        spc = scfg["programs"][spid]
        variant = L.get("variant")
        partner = jv_partner_player(cfg, sup, spid, variant)
        if partner:
            flag = cfg["suppliers"][partner]["jv"]["flag"]
            if not (all_orders.get(partner) or {}).get(flag):
                w.event(k, f"{lab} proposes the {spc['label']} as a {spc['variants'][variant]['label']}, but "
                           f"{player_label(cfg, partner)} does not join this turn, so it is not launched.")
                continue
        sp = SupplierProgram(pid=spid, owner=sup, segment=spc["segment"], launch_year=L["year"], launch_turn=k,
                             dev_years=sparam(cfg, sup, spid, variant, "dev_years"), variant=variant,
                             terms=L.get("terms", "standard"), partner=partner)
        w.sup_programs[spid] = sp
        vtxt = f" ({spc['variants'][variant]['label']})" if variant else ""
        w.event(k, f"{lab} launches the {spc['label']}{vtxt} in {sp.launch_year} on {scfg['terms'][sp.terms]['label']}; "
                   f"engine ready for service in {sp.ready}.")
    for c in supplier_commitments(cfg, sup):
        if not o.get(c["flag"]) or (sup, c["flag"]) in w.commit_years:
            continue
        w.commit_years[(sup, c["flag"])] = a
        if c["kind"] == "upgrade":
            w.upgrade_years.setdefault(sup, a)
            w.event(k, f"{lab} commits to the {c['label']} from {a} (more share of {c['segment'].upper()} deliveries at "
                       f"{player_label(cfg, c['fit_side'])} from {a + c['lag_years']}).")
        elif c["kind"] == "partner_volume":
            w.event(k, f"{lab} commits to the {c['label']} from {a} (engines from {a + c['lag_years']}).")
        else:
            w.event(k, f"{lab} starts {c['label']} in {a}.")
    jv = scfg.get("jv")
    if jv and o.get(jv["flag"]):
        owner = jv["partner_of"]
        joined = any(sp.partner == sup and sp.launch_turn == k for sp in w.sup_programs.values())
        if not joined:
            w.event(k, f"{lab} offers to join the {player_label(cfg, owner)} "
                       f"{cfg['suppliers'][owner]['programs'][jv['program']]['label']} Joint Venture, but no Joint Venture is launched this turn.")


# ---------------------------------------------------------------------------
# Payoff evaluation
# ---------------------------------------------------------------------------

def _sum_in_range(items, y):
    return sum(v for (y0, y1, v) in items if y0 <= y <= y1)


def evaluate(cfg, world, with_objectives=True, with_series=False):
    """Return per-side payoffs, components, programs and key-year shares.

    with_series adds each player's undiscounted yearly financials ("series": {year: {...}}, $B) for
    round-by-round reporting: airframers' revenue, operating profit, capex, strain and tactics in the
    moving world and the status quo; suppliers' engines delivered, engine value, capex and strain."""
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

    def averted(pid, turn):
        p = world.programs.get(pid) if pid else None
        return p is not None and p.cancelled_year is None and p.launch_turn <= turn

    def world_shift_boeing(seg, y, moving=False):
        d = 0.0
        for (s, to, pp, y0, y1, unless, turn) in world.share_shifts:
            if s == seg and y0 <= y <= y1 and not (moving and averted(unless, turn)):
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

    def ramp_param(p, key):
        ro = cfg["programs"][p.pid].get("ramp_options") or {}
        return ro.get(p.ramp, {}).get(key, 1.0) if p.ramp else 1.0

    def capture_speed(p):
        eng = cfg["engine_options"][p.segment][p.engine]
        vm = pparam(cfg, p.pid, p.variant, "capture_mult", 1.0) or 1.0
        return (seg_cfg[p.segment]["capture_pp_per_year"] * p.capture_mult * eng["capture_mult"] * vm
                * ramp_param(p, "capture_mult") * lobby_effect(cfg, world, p.engine)[1] / 100.0)

    cum_tables = {seg: capture_weight_cumsum(seg_cfg[seg].get("capture_weight_by_year"), y_start, y_end) for seg in SEGMENTS}

    def cum_w(seg, a, b):
        """Sum of capture weights over years a+1..b (zero when b <= a); equals b - a with no weights."""
        if b <= a:
            return 0.0
        tab = cum_tables[seg]
        if tab is None:
            return float(b - a)
        y0, cum = tab
        at = lambda t: cum[min(max(t, y0 - 1), y0 + len(cum) - 2) - y0 + 1]
        return at(b) - at(a)

    def shares(seg, y):
        sq_b = min(1.0, max(0.0, seg_cfg[seg]["sq_share"]["boeing"] + world_shift_boeing(seg, y)))
        s_b = min(1.0, max(0.0, seg_cfg[seg]["sq_share"]["boeing"] + world_shift_boeing(seg, y, moving=True)
                           + move_shift_boeing(seg, y)))
        pb, pa = world.prog("boeing", seg), world.prog("airbus", seg)
        eb, ea = eis_of(pb), eis_of(pa)
        if eb < ea:
            n = cum_w(seg, eb, min(y, ea))
            cap = seg_cfg[seg]["leader_cap"]["boeing"]
            if n and s_b < cap:
                s_b = min(cap, s_b + capture_speed(pb) * n)
        elif ea < eb:
            s_a = 1.0 - s_b
            n = cum_w(seg, ea, min(y, eb))
            cap = seg_cfg[seg]["leader_cap"]["airbus"]
            if n and s_a < cap:
                s_a = min(cap, s_a + capture_speed(pa) * n)
            s_b = 1.0 - s_a
        # Optional technology edge: once both new products are in service, the more advanced one
        # (higher tech_level) keeps taking share. Equal levels (the default) keep the freeze rule.
        if eb < NEVER and ea < NEVER and y > max(eb, ea):
            tb = pparam(cfg, pb.pid, pb.variant, "tech_level", 1.0)
            ta = pparam(cfg, pa.pid, pa.variant, "tech_level", 1.0)
            if tb != ta:
                n2 = cum_w(seg, max(eb, ea), y)
                gain = seg_cfg[seg]["capture_pp_per_year"] / 100.0 * abs(tb - ta) * n2
                if tb > ta:
                    s_b = max(s_b, min(seg_cfg[seg]["leader_cap"]["boeing"], s_b + gain))
                else:
                    s_b = min(s_b, 1.0 - min(seg_cfg[seg]["leader_cap"]["airbus"], (1.0 - s_b) + gain))
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
            both = rival is not None and rival.in_service(y)
            m = pparam(cfg, p.pid, p.variant, "margin_both" if both else "margin_alone")
            ready = pparam(cfg, p.pid, p.variant, "tech_ready_year") + world.tech_ready_add[seg]
            m -= pparam(cfg, p.pid, p.variant, "early_penalty_pp_per_year") / 100.0 * max(0, ready - p.eis)
            m += cfg["engine_options"][seg][p.engine]["margin_pp"] / 100.0
            m += p.supplier_margin_pp / 100.0
            m += lobby_effect(cfg, world, p.engine, y)[0] / 100.0
            m += margin_adds(side, seg, "new", y)
            m *= 1.0 - vparam(cfg, p.pid, p.variant, "margin_share_partner")
            return m, sq_m
        return sq_m, sq_m

    def alpha(side, y):
        a = cfg["players"][side]["alpha"]
        if side == "boeing" and world.rate_year is not None and world.rate_year <= y < world.rate_year + rt["alpha_window_years"]:
            a += rt["alpha_add"]
        return a

    def df(side, y):
        return (1.0 + cfg["players"][side]["wacc"]) ** -(y - pv_base)

    def strain_mult(y, side):
        m = 1.0
        for (y0, mult, who) in world.strain_mults:
            if y >= y0 and who in ("all", side):
                m *= mult
        return m

    # Capex and strain schedules (nominal, before alpha loading).
    capex = {s: {} for s in SIDES}
    strain = {s: {} for s in SIDES}
    for p in world.programs.values():
        pc = cfg["programs"][p.pid]
        c = pparam(cfg, p.pid, p.variant, "capex_b") * (1.0 - vparam(cfg, p.pid, p.variant, "capex_share_partner")) * ramp_param(p, "capex_mult")
        for i, y in enumerate(range(p.launch_year, p.eis)):
            if p.cancelled_year is not None and y >= p.cancelled_year:
                break
            amt = c / p.base_dev_years if i < p.base_dev_years else c * cfg["extension_capex_frac_per_year"]
            capex[p.owner][y] = capex[p.owner].get(y, 0.0) + amt
    if world.rate_year is not None:
        for y in range(world.rate_year, world.rate_year + rt["capex_years"]):
            capex["boeing"][y] = capex["boeing"].get(y, 0.0) + rt["capex_b"] / rt["capex_years"]
    for side in SIDES:
        # (start, end, relief, is_background): the player's new programs plus any background
        # developments the scenario says are already under way (e.g. 787 and 747-8 in 2010).
        wins = [(p.launch_year, p.dev_end, vparam(cfg, p.pid, p.variant, "strain_relief"), False)
                for p in world.programs.values() if p.owner == side]
        wins += [(b["start"], b["end"], 0.0, True) for b in cfg["strain"].get("background", []) if b["owner"] == side]
        for i in range(len(wins)):
            for j in range(i + 1, len(wins)):
                (s1, e1, r1, b1), (s2, e2, r2, b2) = wins[i], wins[j]
                if b1 and b2:
                    continue
                start, end = max(s1, s2), min(e1, e2)
                overlap = end - start
                if overlap <= 0:
                    continue
                nominal = cfg["strain"]["full_overlap_b"] * min(1.0, overlap / cfg["strain"]["norm_years"]) * (1.0 - max(r1, r2))
                for y in range(start, end):
                    strain[side][y] = strain[side].get(y, 0.0) + nominal / overlap * strain_mult(y, side)

    out = {}
    share_paths = {seg: {} for seg in SEGMENTS}
    for y in years:
        for seg in SEGMENTS:
            share_paths[seg][y] = shares(seg, y)
    for side in SIDES:
        comp = {"nb_operating": 0.0, "wb_operating": 0.0, "capex": 0.0, "strain": 0.0, "tactics": 0.0}
        undiscounted = {"nb_operating": 0.0, "wb_operating": 0.0, "capex": 0.0, "strain": 0.0, "tactics": 0.0}
        series = {}
        for y in years:
            d = df(side, y)
            row = {}
            for seg in SEGMENTS:
                sh, sq_sh = share_paths[seg][y]
                m, sq_m = margin(side, seg, y)
                rev_unit = units(seg, y) * seg_cfg[seg]["net_price_m"] / 1000.0
                delta = rev_unit * (sh[side] * m - sq_sh[side] * sq_m)
                comp[f"{seg}_operating"] += delta * d
                undiscounted[f"{seg}_operating"] += delta
                if with_series:
                    row[f"{seg}_aircraft"] = units(seg, y) * sh[side]
                    row[f"{seg}_aircraft_sq"] = units(seg, y) * sq_sh[side]
                    row[f"{seg}_revenue_b"] = rev_unit * sh[side]
                    row[f"{seg}_revenue_sq_b"] = rev_unit * sq_sh[side]
                    row[f"{seg}_op_profit_b"] = rev_unit * sh[side] * m
                    row[f"{seg}_op_profit_sq_b"] = rev_unit * sq_sh[side] * sq_m
            if with_series:
                row["capex_b"] = capex[side].get(y, 0.0)
                row["strain_b"] = strain[side].get(y, 0.0)
                row["tactics_b"] = sum(ev["amount_b"] for ev in world.cost_events if ev["player"] == side and ev["year"] == y)
                series[y] = row
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
                "slips": p.slips, "ramp": p.ramp, "engine_requested": p.engine_requested, "engine_wait": p.engine_wait,
            })
        out[side] = {
            "delta_pv_b": round(total, 3),
            "components_pv_b": {k: round(v, 3) for k, v in comp.items()},
            "undiscounted_b": {k: round(v, 3) for k, v in undiscounted.items()},
            "programs": progs,
        }
        if with_series:
            out[side]["series"] = {str(y): {k: round(v, 4) for k, v in r.items()} for y, r in series.items()}
        out[side]["_exact"] = total
    if active_suppliers(cfg):
        fits = {y: incumbent_fits(cfg, world, y) for y in years}
        for sup in active_suppliers(cfg):
            out[sup] = _evaluate_supplier(cfg, world, sup, share_paths, units, strain_mult, fits, with_series)
    out["shares"] = {
        seg: {str(y): {s: round(share_paths[seg][y][0][s], 4) for s in SIDES} for y in KEY_YEARS if y_start <= y <= y_end}
        for seg in SEGMENTS
    }
    out["objectives"] = objective_status(cfg, world, share_paths, out) if with_objectives else {}
    return out


def capture_weight_points(wy):
    """Valid (year, weight) points of a capture_weight_by_year mapping, sorted; keys that are not years are ignored."""
    pts = []
    for k, v in (wy or {}).items():
        try:
            pts.append((int(float(k)), float(v)))
        except (TypeError, ValueError):
            continue
    return sorted(pts)


def capture_weight(pts, t):
    """Piecewise-linear weight in year t, held flat before the first and after the last point."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
        if t <= y1:
            return v0 + (v1 - v0) * (t - y0) / (y1 - y0)
    return pts[-1][1]


def capture_weight_cumsum(wy, y_start, y_end):
    """(first year, running totals) for fast sums of capture weights, or None when there are no weights.

    cum[i] is the sum of weights for years y0 .. y0 + i - 1, with y0 a margin before the game start."""
    pts = capture_weight_points(wy)
    if not pts:
        return None
    y0 = min(y_start, pts[0][0]) - 60
    cum = [0.0]
    for t in range(y0, y_end + 61):
        cum.append(cum[-1] + capture_weight(pts, t))
    return y0, cum


def _strain_schedule(windows, full_overlap_b, norm_years, mult):
    """Overlap strain for one player. windows: (start, end, relief, is_background)."""
    sched = {}
    for i in range(len(windows)):
        for j in range(i + 1, len(windows)):
            (s1, e1, r1, b1), (s2, e2, r2, b2) = windows[i], windows[j]
            if b1 and b2:
                continue
            start, end = max(s1, s2), min(e1, e2)
            overlap = end - start
            if overlap <= 0:
                continue
            nominal = full_overlap_b * min(1.0, overlap / norm_years) * (1.0 - max(r1, r2))
            for y in range(start, end):
                sched[y] = sched.get(y, 0.0) + nominal / overlap * mult(y)
    return sched


def _evaluate_supplier(cfg, world, sup, share_paths, units, strain_mult, fits=None, with_series=False):
    """A supplier's delta PV: lifecycle value of engines delivered versus the status quo.

    Engines delivered in a year = aircraft delivered by each airframer in the segment x
    engines per aircraft x the supplier's fit on that airframe. Until the airframer's new
    program enters service the fit is the supplier's incumbent fit (moved by committed
    upgrades: incumbent_fits). Once it is in service the fit is 1 (less any partner share)
    if the program flies the supplier's new engine; 1 at the incumbent value if it flies a
    derivative of the supplier's current engine (an engine option of this maker with no
    supplier program, e.g. CFM's LEAP derivative or GE's GEnx upgrade); else 0. Each engine
    is booked at delivery at its lifecycle value (OE margin plus PV of aftermarket profit,
    $M): the incumbent value, or for a new engine its mature value x a maturity ramp after
    EIS, less the terms' price concession per engine. A Joint Venture partner uses the
    owner's engine values. One-time commitments add their own capex and value: upgrades
    (installed-base savings), partner volume (engines for a partner's aircraft) and lobbying.
    """
    scfg = cfg["suppliers"][sup]
    y_start, y_end, pv_base = cfg["years"]["start"], cfg["years"]["end"], cfg["years"]["pv_base"]
    wacc, alpha = scfg["wacc"], scfg["alpha"]
    epa = scfg["engines_per_aircraft"]
    commits = [(c, world.commit_years[(sup, c["flag"])]) for c in supplier_commitments(cfg, sup)
               if (sup, c["flag"]) in world.commit_years]
    if fits is None:
        fits = {y: incumbent_fits(cfg, world, y) for y in range(y_start, y_end + 1)}

    def df(y):
        return (1.0 + wacc) ** -(y - pv_base)

    def vmult(kind, y):
        m = 1.0
        for (who, k, y0, y1, v) in world.supplier_value_mults:
            if who == sup and k in ("all", kind) and y0 <= y <= y1:
                m *= v
        return m

    def fit_value(side, seg, y):
        """(fit, value $M per engine) in the moving world."""
        p = world.prog(side, seg)
        if p is not None and p.in_service(y):
            sp = world.sup_programs.get(p.supplier_program) if p.supplier_program else None
            if sp is None:
                # A derivative of the maker's current engine: it keeps the whole airframe at incumbent value.
                if engine_maker(cfg, seg, p.engine) == sup:
                    return 1.0, scfg["incumbent_value_m_per_engine"][seg] * vmult("incumbent", y)
                return 0.0, 0.0
            if sup not in (sp.owner, sp.partner):
                return 0.0, 0.0
            # The engine's value per engine uses its owner's parameters; a Joint Venture splits it.
            ocfg = cfg["suppliers"][sp.owner]
            partner_share = sparam(cfg, sp.owner, sp.pid, sp.variant, "value_share_partner", 0.0)
            share = partner_share if sup == sp.partner else 1.0 - partner_share
            age = y - p.eis
            # Maturity ramp (start_frac may be negative: a new engine can destroy value at first);
            # terms are a fixed price concession per engine of (1 - value_mult) x the mature value.
            oramp = ocfg["ramp"]
            r = min(1.0, oramp["start_frac"] + (1.0 - oramp["start_frac"]) * age / max(1, oramp["years"]))
            base = sparam(cfg, sp.owner, sp.pid, sp.variant, "value_m_per_engine")
            v = base * r - base * (1.0 - ocfg["terms"][sp.terms]["value_mult"])
            return share, v * vmult("new", y)
        return fits[y][sup][(side, seg)], scfg["incumbent_value_m_per_engine"][seg] * vmult("incumbent", y)

    capex = {}
    windows = []
    for sp in world.sup_programs.values():
        if sup not in (sp.owner, sp.partner):
            continue
        cs = sparam(cfg, sp.owner, sp.pid, sp.variant, "capex_share_partner", 0.0)
        c = sparam(cfg, sp.owner, sp.pid, sp.variant, "capex_b") * (cs if sup == sp.partner else 1.0 - cs)
        base = sparam(cfg, sp.owner, sp.pid, sp.variant, "dev_years")
        for i, y in enumerate(range(sp.launch_year, sp.ready)):
            if sp.cancelled_year is not None and y >= sp.cancelled_year:
                break
            amt = c / base if i < base else c * cfg["extension_capex_frac_per_year"]
            capex[y] = capex.get(y, 0.0) + amt
        windows.append((sp.launch_year, sp.dev_end, sparam(cfg, sp.owner, sp.pid, sp.variant, "strain_relief", 0.0), False))
    # A derivative of this maker's current engine on a new airframe (no new engine program) still costs it
    # development capex, spread over the airframe's development years.
    for p in world.programs.values():
        if p.supplier_program or engine_maker(cfg, p.segment, p.engine) != sup:
            continue
        dc = (scfg.get("derivative_capex_b") or {}).get(p.segment, 0.0)
        n = max(1, p.base_dev_years)
        for y in range(p.launch_year, p.launch_year + n):
            if p.cancelled_year is not None and y >= p.cancelled_year:
                break
            capex[y] = capex.get(y, 0.0) + dc / n
    lobby = {}
    for c, yr in commits:
        if c["kind"] in ("upgrade", "partner_volume"):
            # Engineering work: capex over capex_years, and it overlaps (strains) with other developments.
            for y in range(yr, yr + c["capex_years"]):
                capex[y] = capex.get(y, 0.0) + c["capex_b"] / c["capex_years"]
            windows.append((yr, yr + c["capex_years"], 0.0, False))
        elif c["kind"] == "lobby":
            for y in range(yr, yr + c["cost_years"]):
                lobby[y] = lobby.get(y, 0.0) + c["cost_b"] / c["cost_years"]
    st = scfg["strain"]
    windows += [(b["start"], b["end"], 0.0, True) for b in st.get("background", [])]
    strain = _strain_schedule(windows, st["full_overlap_b"], st["norm_years"], lambda y: strain_mult(y, sup))

    comp = {"nb_engines": 0.0, "wb_engines": 0.0, "installed_base": 0.0, "capex": 0.0, "strain": 0.0}
    kinds = {c["kind"] for c in supplier_commitments(cfg, sup)}
    if "partner_volume" in kinds:
        comp["partner_engines"] = 0.0
    if "lobby" in kinds:
        comp["lobby"] = 0.0
    und = dict(comp)
    delivered = {}
    series = {}
    for y in range(y_start, y_end + 1):
        d = df(y)
        row = {}
        for seg in SEGMENTS:
            sh, sq_sh = share_paths[seg][y]
            u = units(seg, y)
            eng_now = eng_sq = val_now = val_sq = 0.0
            for side in SIDES:
                f, v = fit_value(side, seg, y)
                n = u * sh[side] * epa[seg] * f
                eng_now += n
                val_now += n * v
                n0 = u * sq_sh[side] * epa[seg] * scfg["incumbent_fit"][side][seg]
                eng_sq += n0
                val_sq += n0 * scfg["incumbent_value_m_per_engine"][seg] * vmult("incumbent", y)
            delta = (val_now - val_sq) / 1000.0
            comp[f"{seg}_engines"] += delta * d
            und[f"{seg}_engines"] += delta
            if y in KEY_YEARS:
                delivered.setdefault(str(y), {})[seg] = {"engines": round(eng_now, 1), "status_quo": round(eng_sq, 1)}
            if with_series:
                row[f"{seg}_engines"] = eng_now
                row[f"{seg}_engines_sq"] = eng_sq
                row[f"{seg}_engine_value_b"] = val_now / 1000.0
                row[f"{seg}_engine_value_sq_b"] = val_sq / 1000.0
        for c, yr in commits:
            if c["kind"] == "upgrade":
                y0 = yr + c["lag_years"]
                if y0 <= y < y0 + c["saving_years"]:
                    comp["installed_base"] += c["installed_base_saving_b_per_year"] * d
                    und["installed_base"] += c["installed_base_saving_b_per_year"]
            elif c["kind"] == "partner_volume" and y >= yr + c["lag_years"]:
                v = c["engines_per_year"] * c["value_m_per_engine"] * vmult("new", y) / 1000.0
                comp["partner_engines"] += v * d
                und["partner_engines"] += v
                if with_series:
                    row["partner_engines"] = row.get("partner_engines", 0.0) + c["engines_per_year"]
                    row["partner_engine_value_b"] = row.get("partner_engine_value_b", 0.0) + v
                if y in KEY_YEARS:
                    delivered.setdefault(str(y), {})["partner"] = {"engines": float(c["engines_per_year"]), "status_quo": 0.0}
        comp["capex"] -= capex.get(y, 0.0) * (1.0 + alpha) * d
        comp["strain"] -= strain.get(y, 0.0) * (1.0 + alpha) * d
        und["capex"] -= capex.get(y, 0.0) * (1.0 + alpha)
        und["strain"] -= strain.get(y, 0.0) * (1.0 + alpha)
        if y in lobby:
            comp["lobby"] -= lobby[y] * d
            und["lobby"] -= lobby[y]
        if with_series:
            row["capex_b"] = capex.get(y, 0.0)
            row["strain_b"] = strain.get(y, 0.0)
            row["lobby_b"] = lobby.get(y, 0.0)
            row["installed_base_b"] = sum(c["installed_base_saving_b_per_year"] for c, yr in commits if c["kind"] == "upgrade"
                                          and yr + c["lag_years"] <= y < yr + c["lag_years"] + c["saving_years"])
            series[str(y)] = {k: round(v, 4) for k, v in row.items()}
    total = sum(comp.values())
    progs = []
    for spid, sp in world.sup_programs.items():
        if sup not in (sp.owner, sp.partner):
            continue
        spc = cfg["suppliers"][sp.owner]["programs"][spid]
        users = [f"{p.owner}:{p.pid}" for p in world.programs.values() if p.supplier_program == spid and p.cancelled_year is None]
        progs.append({"program": spid, "label": spc["label"], "owner": sp.owner, "partner": sp.partner, "segment": sp.segment,
                      "launch_year": sp.launch_year, "ready": sp.ready if sp.live() else None, "cancelled_year": sp.cancelled_year,
                      "variant": sp.variant, "terms": sp.terms, "selected_by": users, "slips": sp.slips})
    return {
        "delta_pv_b": round(total, 3),
        "components_pv_b": {k: round(v, 3) for k, v in comp.items()},
        "undiscounted_b": {k: round(v, 3) for k, v in und.items()},
        "programs": progs,
        "upgrade_year": world.upgrade_years.get(sup),
        "commitments": {c["flag"]: world.commit_years.get((sup, c["flag"])) for c in supplier_commitments(cfg, sup)},
        "engines_delivered": delivered,
        **({"series": series} if with_series else {}),
        "_exact": total,
    }


# ---------------------------------------------------------------------------
# Assigned objectives (mission attainment; never part of the payoff)
# ---------------------------------------------------------------------------

def objectives_enabled(cfg):
    o = cfg.get("objectives")
    return bool(o) and o.get("enabled", True) and bool(o.get("players"))


def objective_holders(cfg):
    """Who has scored objectives in this run: every player with an entry, plus non-player entries (CFM)."""
    if not objectives_enabled(cfg):
        return []
    ps = players(cfg)
    return [k for k, v in cfg["objectives"]["players"].items() if k in ps or v.get("non_player")]


def objective_status(cfg, world, share_paths, out):
    """Attainment of each holder's assigned objectives on this projection: {holder: [metric rows]}.

    Metric kinds: share (a side's segment share >= target at the listed years; with until_own_eis
    only years before that side's new program enters service count), share_vs_sq (share never
    below the status-quo path), supplier_engines (an active supplier's engines delivered, either
    positive or at least the status quo), supplier_upgrade (the one-time upgrade committed by a
    year), maker_nb_share (an engine maker's share of narrowbody engines, from the airframers'
    engine choices and the other makers' fits, versus the status quo), engine_in_service (some
    airframer program flies one of the engines by a year).
    """
    res = {}
    for who in objective_holders(cfg):
        res[who] = [_objective_metric(cfg, world, share_paths, out, m) for m in cfg["objectives"]["players"][who].get("metrics", [])]
    return res


def _objective_metric(cfg, world, share_paths, out, m):
    y0, y1 = cfg["years"]["start"], cfg["years"]["end"]
    years = [y for y in m.get("years", []) if y0 <= y <= y1]
    row = {"id": m["id"], "label": m["label"], "met": None}
    kind = m["kind"]
    if kind in ("share", "share_vs_sq"):
        seg, side = m["segment"], m["side"]
        if m.get("until_own_eis"):
            p = world.prog(side, seg)
            if p is not None and p.cancelled_year is None and p.eis <= y1:
                years = [y for y in years if y < p.eis]
                row["counted_until"] = p.eis
        exact = {y: share_paths[seg][y][0][side] for y in years}
        vals = {str(y): round(v, 4) for y, v in exact.items()}
        row["values"], row["unit"] = vals, "share"
        if kind == "share":
            row["target"] = m["target"]
            if exact:
                worst = min(exact.values())
                row["met"] = worst >= m["target"] - 1e-9
                row["gap_pp"] = round((worst - m["target"]) * 100, 2)
        else:
            sq_exact = {y: share_paths[seg][y][1][side] for y in years}
            row["status_quo"] = {str(y): round(v, 4) for y, v in sq_exact.items()}
            if exact:
                gaps = [exact[y] - sq_exact[y] for y in exact]
                row["met"] = min(gaps) >= -1e-9
                row["gap_pp"] = round(min(gaps) * 100, 2)
        if not vals:
            row["note"] = "no year left to count"
    elif kind == "supplier_engines":
        sup, seg = m["supplier"], m["segment"]
        if sup not in active_suppliers(cfg) or sup not in out:
            row["note"] = "not scored: not a player in this run"
            return row
        dl = out[sup].get("engines_delivered", {})
        off = [y for y in years if str(y) not in dl]
        if off:
            row["note"] = f"not scored: engines are reported only for key years {list(KEY_YEARS)}; got {off}"
            return row
        vals = {str(y): dl.get(str(y), {}).get(seg, {}) for y in years}
        row["values"], row["unit"] = {y: v.get("engines") for y, v in vals.items()}, "engines a year"
        row["status_quo"] = {y: v.get("status_quo") for y, v in vals.items()}
        if vals:
            if m.get("op") == "positive":
                row["met"] = all((v.get("engines") or 0) > 0.5 for v in vals.values())
            else:
                row["met"] = all((v.get("engines") or 0) >= (v.get("status_quo") or 0) - 0.5 for v in vals.values())
    elif kind == "supplier_upgrade":
        sup = m["supplier"]
        if sup not in active_suppliers(cfg):
            row["note"] = "not scored: not a player in this run"
            return row
        yr = world.commit_years.get((sup, m["flag"])) if m.get("flag") else world.upgrade_years.get(sup)
        row["values"] = {"upgrade_year": yr}
        row["target"] = f"by {m['by_year']}"
        row["met"] = yr is not None and yr <= m["by_year"]
    elif kind == "maker_nb_share":
        maker = m.get("maker", "cfm")
        mine = set(m.get("engines") or [e for e, ec in cfg["engine_options"]["nb"].items() if ec.get("maker") == maker])
        base = cfg["suppliers"][maker]["incumbent_fit"]
        vals, sq, gaps = {}, {}, []
        for y in years:
            sh, sq_sh = share_paths["nb"][y]
            now = incumbent_fits(cfg, world, y)[maker]
            v = 0.0
            for side in SIDES:
                p = world.prog(side, "nb")
                fit = (1.0 if p.engine in mine else 0.0) if (p is not None and p.in_service(y)) else now[(side, "nb")]
                v += sh[side] * fit
            q = sum(sq_sh[side] * base[side]["nb"] for side in SIDES)
            vals[str(y)], sq[str(y)] = round(v, 4), round(q, 4)
            gaps.append(v - q)
        row["values"], row["status_quo"], row["unit"] = vals, sq, "share of narrowbody engines"
        if vals:
            row["met"] = min(gaps) >= -1e-9
            row["gap_pp"] = round(min(gaps) * 100, 2)
    elif kind == "engine_in_service":
        eng = set(m["engines"])
        eis = [p.eis for p in world.programs.values() if p.engine in eng and p.cancelled_year is None and p.eis <= y1]
        first = min(eis) if eis else None
        row["values"] = {"first_eis": first}
        row["target"] = f"by {m['by_year']}"
        row["met"] = first is not None and first <= m["by_year"]
    else:
        row["note"] = f"unknown metric kind {kind}"
    return row


def payoff(cfg, history, masked_delay_turns=frozenset()):
    """Exact (unrounded) payoffs for a history: {"boeing": x, "airbus": y, [supplier: z]}."""
    r = evaluate(cfg, build_world(cfg, history, masked_delay_turns), with_objectives=False)
    return {s: r[s]["_exact"] for s in players(cfg)}


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
    for s in SIDES + SUPPLIERS:
        if isinstance(result.get(s), dict):
            result[s].pop("_exact", None)
    return result


# ---------------------------------------------------------------------------
# Order validation
# ---------------------------------------------------------------------------

TEXT_FIELDS = ("public_statement", "rationale")
# Optional player fields kept with the turn record (not mechanical):
#   disclose: statements the player chooses to make public (relayed to the rival and market);
#   prediction: the player's forecast of the rival's orders this turn (scored for awareness);
#   expected_delta_pv_b: the player's own projected payoff when ordering (scored for calibration).
META_FIELDS = ("disclose", "prediction", "expected_delta_pv_b")


def validate_orders(cfg, history, turn, side, orders):
    """Check one side's orders for `turn` against the world built from `history`.

    Returns (canonical_orders, errors, warnings). Canonical orders carry only
    the mechanical fields; text fields are kept separately by the caller.
    """
    errors, warnings = [], []
    if side not in players(cfg):
        return None, [f"unknown side '{side}'" + (" (this game has no active supplier of that name)" if side in SUPPLIERS else "")], []
    if not isinstance(orders, dict):
        return None, ["orders must be a JSON object"], []
    if side in SUPPLIERS:
        return _validate_supplier_orders(cfg, history, turn, side, orders)
    a, b = turn_years(cfg, turn)
    w = build_world(cfg, history)
    canon = empty_orders(side)
    allowed = set(canon) | set(TEXT_FIELDS) | set(META_FIELDS) | {"side"}
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
        avail = cfg["engine_options"][pc["segment"]][engine].get("available_eis")
        if avail is not None:
            own = (year + pparam(cfg, pid, requested_variant(pc, L), "dev_years") + w.dev_years_add[side] + int(pc.get("delay_years", 0))
                   + cfg["engine_options"][pc["segment"]][engine]["eis_add"])
            if own < avail:
                warnings.append(f"'{engine}' cannot enter service before {avail}: '{pid}' would be ready in {own}, so it waits "
                                f"{avail - own} year(s), paying {cfg['extension_capex_frac_per_year']:.0%} of program capex for each. "
                                f"Launch in {year + avail - own} to enter service in {avail} without waiting.")
        req = supplier_requirement(cfg, pc["segment"], engine)
        if req:
            sp = w.sup_programs.get(req[1])
            scfg = cfg["suppliers"][req[0]]
            fb = scfg["fallback_engine"][pc["segment"]]
            if sp is None or not sp.live():
                chain, e2 = [fb], fb
                while True:
                    r2 = supplier_requirement(cfg, pc["segment"], e2)
                    s2 = w.sup_programs.get(r2[1]) if r2 else None
                    if not r2 or (s2 is not None and s2.live()) or len(chain) > 4:
                        break
                    e2 = cfg["suppliers"][r2[0]]["fallback_engine"][pc["segment"]]
                    if e2 in chain:
                        break
                    chain.append(e2)
                warnings.append(f"'{engine}' needs {scfg['label']} to launch its {scfg['programs'][req[1]]['label']} ({req[1]}); "
                                f"it has not{' (it was cancelled)' if sp else ''}. If {scfg['label']} does not launch it this turn, "
                                f"'{pid}' falls back to '{fb}'"
                                + (f" (and, if that engine's maker has not committed either, on to {' -> '.join(chain[1:])})" if len(chain) > 1 else "")
                                + ".")
            else:
                own = year + pparam(cfg, pid, requested_variant(pc, L), "dev_years") + w.dev_years_add[side] + int(pc.get("delay_years", 0))
                wait = max(0, sp.ready - own)
                warnings.append(f"'{engine}': {scfg['label']} committed in {sp.launch_year} on {sp.terms} terms "
                                f"({scfg['terms'][sp.terms]['airframer_margin_pp']:+.1f} pp margin to you); engine ready {sp.ready}"
                                + (f", so '{pid}' waits {wait} year(s) for it" if wait else "") + ".")
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
        ramp = L.get("ramp")
        ro = {k: v for k, v in (pc.get("ramp_options") or {}).items() if not k.startswith("_")}
        if ramp not in (None, ""):
            if ramp not in ro:
                errors.append(f"ramp '{ramp}' is not valid for '{pid}'" + (f" (options: {', '.join(ro)})" if ro else " (it has no ramp options)"))
                continue
            if ramp != pc.get("default_ramp"):
                entry["ramp"] = ramp
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
        elif v and not tactic_enabled(cfg, flag):
            errors.append(f"'{flag}' is not available in this scenario")
        else:
            canon[flag] = v
    if side == "boeing" and canon.get("rate_increase") and w.rate_year is not None:
        warnings.append(f"rate increase already committed in {w.rate_year}; no additional effect")
    canon["launch"].sort(key=lambda e: e["program"])
    canon["cancel"].sort()
    return (canon if not errors else None), errors, warnings


def requested_variant(pc, L):
    v = L.get("variant")
    if v in ("", "none"):
        v = None
    return (v or pc.get("default_variant")) if "variants" in pc else None


def _validate_supplier_orders(cfg, history, turn, side, orders):
    errors, warnings = [], []
    a, b = turn_years(cfg, turn)
    w = build_world(cfg, history)
    scfg = cfg["suppliers"][side]
    canon = empty_orders(side)
    allowed = set(canon) | set(TEXT_FIELDS) | set(META_FIELDS) | {"side"}
    for k in orders:
        if k not in allowed:
            warnings.append(f"ignored unknown field '{k}'")
    if orders.get("side") not in (None, side):
        errors.append(f"orders are labelled for side '{orders.get('side')}' but were submitted for '{side}'")
    launches = orders.get("launch", []) or []
    cancels = orders.get("cancel", []) or []
    if not isinstance(launches, list) or not isinstance(cancels, list):
        return None, ["'launch' and 'cancel' must be lists"], warnings
    mine = list(scfg["programs"])
    seen = set()
    for L in launches:
        if isinstance(L, str):
            L = {"program": L}
        if not isinstance(L, dict) or "program" not in L:
            errors.append(f"launch entry {L!r} must be an object with a 'program'")
            continue
        pid = L["program"]
        if pid not in mine:
            errors.append(f"'{pid}' is not a {scfg['label']} program (yours: {', '.join(mine)})")
            continue
        if pid in seen:
            errors.append(f"'{pid}' is launched twice")
            continue
        seen.add(pid)
        if pid in w.sup_programs:
            errors.append(f"'{pid}' was already launched in turn {w.sup_programs[pid].launch_turn}; a program can be launched once")
            continue
        spc = scfg["programs"][pid]
        year = L.get("year", a)
        if not isinstance(year, int) or not (a <= year <= b):
            errors.append(f"launch year for '{pid}' must be an integer in this turn's years {a}-{b} (got {year!r})")
            continue
        terms = L.get("terms") or "standard"
        if terms not in scfg["terms"]:
            errors.append(f"terms '{terms}' are not valid (options: {', '.join(scfg['terms'])})")
            continue
        entry = {"program": pid, "year": year, "terms": terms}
        requested = L.get("variant")
        if requested in ("", "none"):
            requested = None
        if "variants" in spc:
            variant = requested or spc["default_variant"]
            if variant not in spc["variants"]:
                errors.append(f"variant '{variant}' is not valid for '{pid}' (options: {', '.join(spc['variants'])})")
                continue
            entry["variant"] = variant
        elif requested:
            errors.append(f"'{pid}' has no variants (use \"none\")")
            continue
        canon["launch"].append(entry)
    for pid in cancels:
        sp = w.sup_programs.get(pid)
        users = [p.pid for p in w.programs.values() if p.supplier_program == pid and p.cancelled_year is None]
        if pid not in mine:
            errors.append(f"cannot cancel '{pid}': not a {scfg['label']} program")
        elif sp is None:
            errors.append(f"cannot cancel '{pid}': it has not been launched")
        elif pid in seen:
            errors.append(f"cannot launch and cancel '{pid}' in the same turn")
        elif not sp.live():
            errors.append(f"'{pid}' is already cancelled")
        elif sp.ready <= a:
            errors.append(f"cannot cancel '{pid}': the engine was ready in {sp.ready}")
        elif users:
            errors.append(f"cannot cancel '{pid}': {', '.join(users)} flies it (contractual commitment)")
        elif pid not in canon["cancel"]:
            canon["cancel"].append(pid)
    jv = scfg.get("jv")
    commits = {c["flag"]: c for c in supplier_commitments(cfg, side)}
    for flag in SUPPLIER_FLAGS[side]:
        if flag not in orders:
            continue
        v = orders[flag]
        if not isinstance(v, bool):
            errors.append(f"'{flag}' must be true or false")
            continue
        if not v:
            continue
        if flag in commits:
            canon[flag] = True
            if (side, flag) in w.commit_years:
                warnings.append(f"{commits[flag]['label']} already committed in {w.commit_years[(side, flag)]}; no additional effect")
        elif jv and flag == jv["flag"]:
            owner = jv["partner_of"]
            if owner not in active_suppliers(cfg):
                errors.append(f"'{flag}': {cfg['suppliers'][owner]['label']} is not a player in this run")
            elif jv["program"] in w.sup_programs:
                errors.append(f"'{flag}': the {cfg['suppliers'][owner]['programs'][jv['program']]['label']} was already launched")
            else:
                canon[flag] = True
                warnings.append(f"You join only if {cfg['suppliers'][owner]['label']} launches {jv['program']} as "
                                f"'{jv['variant']}' this turn; you would then pay "
                                f"{sparam(cfg, owner, jv['program'], jv['variant'], 'capex_share_partner', 0.0):.0%} of its capex and earn "
                                f"{sparam(cfg, owner, jv['program'], jv['variant'], 'value_share_partner', 0.0):.0%} of its value.")
        else:
            errors.append(f"'{flag}' is not available in this scenario")
    for L in canon["launch"]:
        partner = jv_partner_player(cfg, side, L["program"], L.get("variant"))
        if partner:
            warnings.append(f"'{L['program']}' as '{L['variant']}' needs {cfg['suppliers'][partner]['label']} to set "
                            f"'{cfg['suppliers'][partner]['jv']['flag']}' this turn; otherwise it is not launched.")
    for flag in ("rate_increase", "delay_tactics", "poaching"):
        if orders.get(flag):
            errors.append(f"'{flag}' is an airframer lever")
    canon["launch"].sort(key=lambda e: e["program"])
    canon["cancel"].sort()
    return (canon if not errors else None), errors, warnings


def canonical_key(side, o):
    """ASCII key of the mechanical content of canonical orders (mirrored in the workflow script)."""
    if side in SUPPLIERS:
        launches = ";".join(f"{L['program']}/{L.get('variant') or '-'}/{L.get('terms', 'standard')}/{L['year']}"
                            for L in sorted(o.get("launch", []), key=lambda e: e["program"]))
        cancels = ",".join(sorted(set(o.get("cancel", []))))
        return f"{side}|L={launches}|C={cancels}|F=" + ",".join(f"{f}:{int(bool(o.get(f)))}" for f in SUPPLIER_FLAGS[side])
    launches = ";".join(f"{L['program']}/{L.get('variant') or '-'}/{L['engine']}/{L['year']}" + (f"/{L['ramp']}" if L.get("ramp") else "")
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
