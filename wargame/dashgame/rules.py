"""Rules of the dash-2050 war game: legal orders, validation and adjudication. Pure functions on a state dict.

Rounds are decision years 2030, 2035, 2045 and 2050. In each round the five players move simultaneously.
A programme launched in round year Y enters service (airframes) or is ready (engines) after its development time.
"""
import copy

import model as M

ROUNDS = [2030, 2035, 2045, 2050]

# ── order vocabulary per side (the JSON each player returns) ──
ORDER_FIELDS = {
    "boeing": {"fps": ["hold", "launch_7yr", "launch_10yr", "launch_via_embraer", "cancel"],
               "fps_engine_code": [None, 1, 2, 3, 4, 5, 6, 7],
               "rate_737": ["hold", "increase"],
               "re787": ["hold", "launch", "cancel"]},
    "airbus": {"ngsa": ["hold", "launch", "cancel"],
               "ngsa_engine_code": [None, 1, 2, 3, 4, 5, 6, 7],
               "rea350": ["hold", "launch", "cancel"],
               "delay_tactics": ["none", "bottleneck", "poaching", "both"]},
    "cfm": {"ducted": ["hold", "launch", "cancel"], "open_fan": ["hold", "launch", "cancel"],
            "partner_embraer": ["hold", "launch", "cancel"], "lobby_emissions": ["hold", "launch"],
            "genx": ["hold", "upgrade_genx9", "invest_genx", "cancel"]},
    "pratt_whitney": {"gtf2_solo": ["hold", "launch", "launch_if_selected", "cancel"],
                      "jv_with_rr": ["hold", "commit", "withdraw"]},
    "rolls_royce": {"ultrafan_nb_solo": ["hold", "launch", "launch_if_selected", "cancel"],
                    "jv_with_pw": ["hold", "commit", "withdraw"],
                    "ultrafan_wb": ["hold", "launch", "cancel"], "t1000_upgrade": ["hold", "launch", "cancel"]},
}
DEFAULT_ORDER = {s: {k: v[0] for k, v in f.items()} for s, f in ORDER_FIELDS.items()}


def in_service(state, key, year):
    r = M.live(state, key)
    return bool(r and r.get("eis", r.get("ready", 9999)) <= year)


def legal_options(state, side, year):
    """Legal values of each order field for `side` in round `year` (what the player's brief lists)."""
    L = {k: list(v) for k, v in ORDER_FIELDS[side].items()}

    def prog_opts(key, launch_vals, field):
        r = M.live(state, key)
        if r is None:
            L[field] = ["hold"] + launch_vals
        elif r.get("eis", r.get("ready")) > year:
            L[field] = ["hold", "cancel"]
        else:
            L[field] = ["hold"]
    if side == "boeing":
        prog_opts("fps", ["launch_7yr", "launch_10yr", "launch_via_embraer"], "fps")
        prog_opts("re787", ["launch"], "re787")
        L["rate_737"] = ["hold", "increase"] if (year == ROUNDS[0] and not state["rate737"]) else ["hold"]
        fps = M.live(state, "fps")
        L["fps_engine_code"] = [None] + list(range(1, 8)) if (fps is None or fps["eis"] > year) else [None]
    elif side == "airbus":
        prog_opts("ngsa", ["launch"], "ngsa")
        prog_opts("rea350", ["launch"], "rea350")
        ngsa = M.live(state, "ngsa")
        L["ngsa_engine_code"] = [None] + list(range(1, 8)) if (ngsa is None or ngsa["eis"] > year) else [None]
        fps = M.live(state, "fps")
        dt = state["dt"]
        if fps and fps["eis"] <= year:
            L["delay_tactics"] = ["none"]                 # nothing left to delay
        else:
            L["delay_tactics"] = ["none"] + [x for x in ("bottleneck", "poaching") if not dt[x]] + \
                (["both"] if not (dt["bottleneck"] or dt["poaching"]) else [])
    elif side == "cfm":
        prog_opts("cfm_ducted", ["launch"], "ducted")
        prog_opts("cfm_open_fan", ["launch"], "open_fan")
        prog_opts("cfm_embraer", ["launch"], "partner_embraer")
        L["lobby_emissions"] = ["hold"] if M.live(state, "cfm_lobby") else ["hold", "launch"]
        g = M.live(state, "cfm_genx")
        L["genx"] = ["hold", "upgrade_genx9", "invest_genx"] if g is None else (["hold", "cancel"] if g["ready"] > year else ["hold"])
    elif side == "pratt_whitney":
        prog_opts("pw_solo", ["launch", "launch_if_selected"], "gtf2_solo")
        if M.live(state, "jv"):
            L["gtf2_solo"] = ["hold"]
            L["jv_with_rr"] = ["hold"]
        else:
            L["jv_with_rr"] = ["hold", "withdraw"] if state["jv_commit"]["pratt_whitney"] else ["hold", "commit"]
    elif side == "rolls_royce":
        prog_opts("rr_solo", ["launch", "launch_if_selected"], "ultrafan_nb_solo")
        prog_opts("rr_uf_wb", ["launch"], "ultrafan_wb")
        prog_opts("rr_t1000", ["launch"], "t1000_upgrade")
        if M.live(state, "rr_t1000"):            # UltraFan WB and the Trent 1000 upgrade are exclusive on the board
            L["ultrafan_wb"] = ["hold"]
        if M.live(state, "rr_uf_wb"):
            L["t1000_upgrade"] = ["hold"]
        if M.live(state, "jv"):
            L["ultrafan_nb_solo"] = ["hold"]
            L["jv_with_pw"] = ["hold"]
        else:
            L["jv_with_pw"] = ["hold", "withdraw"] if state["jv_commit"]["rolls_royce"] else ["hold", "commit"]
    return L


def validate(state, side, year, orders):
    """Return (clean_orders, problems). Illegal or missing fields become 'hold' (logged)."""
    L = legal_options(state, side, year)
    clean, probs = {}, []
    for k, opts in L.items():
        v = orders.get(k, DEFAULT_ORDER[side][k])
        if k.endswith("engine_code") and v is not None:
            try:
                v = int(v)
            except (TypeError, ValueError):
                v = "bad"
        if v not in opts:
            probs.append("%s=%r not legal (legal: %s); set to %r" % (k, v, opts, opts[0]))
            v = opts[0]
        clean[k] = v
    # cross-field rules
    if side == "rolls_royce" and clean.get("ultrafan_wb") == "launch" and clean.get("t1000_upgrade") == "launch":
        probs.append("UltraFan WB and the Trent 1000 upgrade are exclusive on the board; t1000_upgrade set to hold")
        clean["t1000_upgrade"] = "hold"
    if side == "cfm" and clean.get("partner_embraer") == "launch":
        has_new = any(M.live(state, k) for k in ("cfm_ducted", "cfm_open_fan")) or \
            clean.get("ducted") == "launch" or clean.get("open_fan") == "launch"
        if not has_new:
            clean["partner_embraer"] = "hold"
            probs.append("Partner Embraer needs a new CFM engine (Ducted or Open Fan) on the board; set to hold")
    if side == "boeing" and clean["fps"].startswith("launch") and clean.get("fps_engine_code") is None:
        clean["fps_engine_code"] = 7; probs.append("fps launched without an engine code; set to 7 (all three)")
    if side == "airbus" and clean["ngsa"] == "launch" and clean.get("ngsa_engine_code") is None:
        clean["ngsa_engine_code"] = 7; probs.append("NGSA launched without an engine code; set to 7 (all three)")
    return clean, probs


def _cancel(state, key, year, log):
    r = state["prog"][key]
    if key in M.AF_SIDE:
        bill, dev = M.af_bill(key, r.get("variant")), M.af_dev(key, r.get("variant"))
        frac = min(1.0, max(0.0, (year - r["launch"]) / dev))
        side = M.AF_SIDE[key]
        rec = {"key": key, "side": side, "launch": r["launch"], "cancel": year, "eis": r["eis"],
               "sunk_nom": bill * frac, "label": key + (" " + r["variant"] if r.get("variant") else "")}
        state["dead"].append(rec)
    else:
        dev = r["ready"] - r["launch"]
        frac = min(1.0, max(0.0, (year - r["launch"]) / dev)) if dev > 0 else 1.0
        for side in (["pratt_whitney", "rolls_royce"] if key == "jv" else [M.EN_SIDE[key]]):
            rd = M.en_rd(key, side)
            state["dead"].append({"key": key, "side": side, "launch": r["launch"], "cancel": year,
                                  "sunk_nom": rd * frac, "label": key})
    r["cancel"] = year
    log.append("%s cancelled in %d" % (M.PROG_LABEL.get(key, key), year))
    state["prog"]["_cancelled_" + key + "_%d" % year] = state["prog"].pop(key)


def _launch(state, key, year, log, **extra):
    rec = {"launch": year, "cancel": None}
    rec.update(extra)
    if key in M.AF_SIDE and key != "rate737":
        rec["eis"] = year + M.af_dev(key, extra.get("variant"))
    elif key in M.EN_SIDE:
        rec["ready"] = M.engine_ready(key, year)
    state["prog"][key] = rec
    log.append("%s launched in %d" % (M.PROG_LABEL.get(key, key), year))


def adjudicate(state, year, orders):
    """Apply one round of validated orders (all five sides) and return (new_state, log)."""
    s = copy.deepcopy(state)
    log = []
    o = {side: dict(DEFAULT_ORDER[side], **orders.get(side, {})) for side in M.SIDES}
    # cancellations first (they free the slot)
    for side, field, key in (("boeing", "fps", "fps"), ("boeing", "re787", "re787"), ("airbus", "ngsa", "ngsa"),
                             ("airbus", "rea350", "rea350"), ("cfm", "ducted", "cfm_ducted"),
                             ("cfm", "open_fan", "cfm_open_fan"), ("cfm", "partner_embraer", "cfm_embraer"),
                             ("cfm", "genx", "cfm_genx"), ("pratt_whitney", "gtf2_solo", "pw_solo"),
                             ("rolls_royce", "ultrafan_nb_solo", "rr_solo"), ("rolls_royce", "ultrafan_wb", "rr_uf_wb"),
                             ("rolls_royce", "t1000_upgrade", "rr_t1000")):
        if o[side][field] == "cancel" and M.live(s, key):
            _cancel(s, key, year, log)
    # Embraer partnership lapses if CFM is left with no new engine programme
    if M.live(s, "cfm_embraer") and not (M.live(s, "cfm_ducted") or M.live(s, "cfm_open_fan")) and \
            o["cfm"]["ducted"] != "launch" and o["cfm"]["open_fan"] != "launch":
        _cancel(s, "cfm_embraer", year, log)
    # airframer launches and engine codes
    b = o["boeing"]
    if b["fps"].startswith("launch"):
        _launch(s, "fps", year, log, variant={"launch_7yr": "7yr", "launch_10yr": "10yr",
                                              "launch_via_embraer": "embraer"}[b["fps"]])
    if b["re787"] == "launch":
        _launch(s, "re787", year, log)
    if b.get("rate_737") == "increase" and not s["rate737"]:
        s["rate737"] = {"launch": year}; log.append("Boeing 737 production-rate increase ordered in %d (rate up from 2032)" % year)
    a = o["airbus"]
    if a["ngsa"] == "launch":
        _launch(s, "ngsa", year, log)
    if a["rea350"] == "launch":
        _launch(s, "rea350", year, log)
    dt = a.get("delay_tactics", "none")
    for x in ("bottleneck", "poaching"):
        if dt in (x, "both") and not s["dt"][x]:
            s["dt"][x] = year; log.append("Delay Tactics (%s) ordered in %d [covert]" % (x, year))
    for side, key, field in (("boeing", "fps", "fps_engine_code"), ("airbus", "ngsa", "ngsa_engine_code")):
        r = M.live(s, key)
        if r and r["eis"] > year and o[side].get(field):
            if s["codes"].get(key) != o[side][field]:
                log.append("%s engine selection: %s" % ("fps" if key == "fps" else "NGSA", M.CODE_LABEL[o[side][field]]))
            s["codes"][key] = o[side][field]
    # forbidden pairs between the two new programmes: the later-EIS one (Airbus on a tie) goes to code 7
    if M.live(s, "fps") and M.live(s, "ngsa"):
        bc, ac = s["codes"].get("fps", 7), s["codes"].get("ngsa", 7)
        if (bc, ac) in M.FORBIDDEN:
            later = "fps" if s["prog"]["fps"]["eis"] > s["prog"]["ngsa"]["eis"] else "ngsa"
            if s["prog"][later]["eis"] <= year:
                later = "ngsa" if later == "fps" else "fps"
            log.append("engine codes (%d,%d) are not allowed together: %s moved to code 7 (all three)" % (bc, ac, "fps" if later == "fps" else "NGSA"))
            s["codes"][later] = 7
    # Joint Venture: forms when both makers have a standing commitment
    for side, field in (("pratt_whitney", "jv_with_rr"), ("rolls_royce", "jv_with_pw")):
        if o[side][field] == "commit" and not s["jv_commit"][side]:
            s["jv_commit"][side] = year; log.append("%s commits to the Joint Venture" % M.NAMES[side])
        elif o[side][field] == "withdraw" and s["jv_commit"][side]:
            s["jv_commit"][side] = None; log.append("%s withdraws its Joint Venture commitment" % M.NAMES[side])
    jv_now = (not M.live(s, "jv")) and s["jv_commit"]["pratt_whitney"] and s["jv_commit"]["rolls_royce"]
    if jv_now:
        folded_ready = []
        for key, side in (("pw_solo", "pratt_whitney"), ("rr_solo", "rolls_royce")):
            r = M.live(s, key)
            if r:   # a solo programme folds into the Joint Venture; spend beyond the maker's JV share is written off
                folded_ready.append(r["ready"])
                dev = r["ready"] - r["launch"]
                spent = M.en_rd(key) * min(1.0, (year - r["launch"]) / dev)
                s["dead"].append({"key": key, "side": side, "launch": r["launch"], "cancel": year,
                                  "sunk_nom": max(0.0, spent - M.en_rd("jv", side)), "label": key + " (folded into JV)"})
                r["cancel"] = year
                s["prog"]["_folded_" + key] = s["prog"].pop(key)
                log.append("%s folded into the Joint Venture" % M.PROG_LABEL.get(key, key))
        _launch(s, "jv", year, log)
        if folded_ready and min(folded_ready) < s["prog"]["jv"]["ready"]:
            # the Joint Venture inherits the most advanced folded programme's schedule
            s["prog"]["jv"]["ready"] = min(folded_ready)
            log.append("Joint Venture engine ready %d (inherits a folded solo programme's schedule)" % min(folded_ready))
    # conditional engine launches: launch if a live, not-yet-in-service airframe selects you and you'd be ready in time
    for side, field, key, maker in (("pratt_whitney", "gtf2_solo", "pw_solo", "PW"),
                                    ("rolls_royce", "ultrafan_nb_solo", "rr_solo", "RR")):
        v = o[side][field]
        if M.live(s, key) or M.live(s, "jv"):
            continue
        if v == "launch":
            _launch(s, key, year, log)
        elif v == "launch_if_selected":
            ready = M.engine_ready(key, year)
            sel = [k for k in ("fps", "ngsa") if M.live(s, k) and s["prog"][k]["eis"] > year
                   and maker in M.CODE_SETS[s["codes"].get(k, 7)][0] and ready <= s["prog"][k]["eis"]]
            if sel:
                _launch(s, key, year, log); log.append("%s: conditional launch triggered by %s" % (key, ", ".join(sel)))
            else:
                log.append("%s: conditional launch not triggered (not selected on an airframe it could meet)" % key)
    c = o["cfm"]
    for field, key in (("ducted", "cfm_ducted"), ("open_fan", "cfm_open_fan")):
        if c[field] == "launch" and not M.live(s, key):
            _launch(s, key, year, log)
    if c["partner_embraer"] == "launch" and not M.live(s, "cfm_embraer"):
        _launch(s, "cfm_embraer", year, log)
    if c["lobby_emissions"] == "launch" and not M.live(s, "cfm_lobby"):
        _launch(s, "cfm_lobby", year, log)
    if c["genx"] in ("upgrade_genx9", "invest_genx") and not M.live(s, "cfm_genx"):
        _launch(s, "cfm_genx", year, log, kind={"upgrade_genx9": "genx9", "invest_genx": "genx_invest"}[c["genx"]])
    r_ = o["rolls_royce"]
    if r_["ultrafan_wb"] == "launch" and not M.live(s, "rr_uf_wb") and not M.live(s, "rr_t1000"):
        _launch(s, "rr_uf_wb", year, log)
    if r_["t1000_upgrade"] == "launch" and not M.live(s, "rr_t1000") and not M.live(s, "rr_uf_wb"):
        _launch(s, "rr_t1000", year, log)
    s["year"] = year
    s["log"].append({"year": year, "events": log})
    return s, log


def engine_fit(state):
    """Public view of each live new airframe's engines: requested code, what is actually fitted, and why."""
    out = {}
    for key in ("fps", "ngsa"):
        r = M.live(state, key)
        if r:
            makers, jv, note = M.effective_code(state, key)
            out[key] = {"requested": M.CODE_LABEL[state["codes"].get(key, 7)],
                        "fitted_if_no_change": " + ".join(sorted(makers)) + (" (JV)" if jv else ""), "note": note}
    return out
