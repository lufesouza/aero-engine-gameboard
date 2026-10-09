"""Valuation for the dash-2050 war game, built on the user's game-theory board (board/Combined_Game_Board.py).

Airframers (Boeing, Airbus): the board's own evaluate_scenario(), solved at the state's entry-into-service (EIS)
dates, plus game-master (GM) adjustments the board cannot express (cancellation write-offs, Delay Tactics ordered
after the board's spending window). Year-by-year shares, units, revenue and operating profit are traced from inside
evaluate_scenario() and reconcile to its present values (asserted).

Engine makers (CFM/GE, Pratt & Whitney, Rolls-Royce): a year-by-year form of the board's simulate(). It uses the
same share rules, engine prices, CPI, gross multiplier, WACC, R&D and strain. Each engine programme counts from the
year it is ready, and the two airframer slots follow the airframers' year-by-year narrowbody (NB) split. With every
programme ready at the board's EIS and a fixed 50/50 split it reproduces simulate() exactly (see test_model.py).

All values are $B; present values (PV) are discounted to 2026 at each player's board WACC.
"""
import functools
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "board"))
import harness as H  # noqa: E402

Y0 = 2026
REPORT_END = 2060                     # last calendar year shown in the year-by-year tables
DEFAULT_EIS = {"fps": 2041, "ngsa": 2037, "re787": 2035, "rea350": 2035}   # snapshot sliders (unlaunched programmes)
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAMES = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney",
         "rolls_royce": "Rolls-Royce"}

NL = H.NL
_TR_ANCHOR = "                a_scen_wb_pv += (WB_PER_YR * a_sh_wb * PRICE_WB * a_wb_margin_t) * df_a"
_TR_INJ = (_TR_ANCHOR + NL +
           "            _TR = st.session_state.get('_TRACE')" + NL +
           "            if _TR is not None: _TR.append(dict(t=t, b_sh_nb=b_sh_nb, a_sh_nb=a_sh_nb, b_p_nb=b_p_nb, "
           "b_m_nb=b_m_nb, a_p_nb=a_p_nb, a_m_nb=a_m_nb, b_sh_wb=b_sh_wb, a_sh_wb=a_sh_wb, b_m_wb=b_wb_margin_t, "
           "a_m_wb=a_wb_margin_t, b_nb_in=(t <= _b_nb_end_t), a_nb_in=(t <= _a_nb_end_t), b_wb_in=(t <= _b_wb_end_t), "
           "a_wb_in=(t <= _a_wb_end_t), df_b=df_b, df_a=df_a))")
# The per-year loop is extended to 2060 so the tables have shares for every year shown. Every PV accumulation in the
# loop is masked by its programme window, so the extension cannot change a PV (test_model.py checks all 256 cells).
_T_ANCHOR = "        T_dynamic = max(TIMELINE_YRS,"
_T_INJ = "        T_dynamic = max(TIMELINE_YRS, %d," % (REPORT_END - Y0 + 1)
AF_PATCH = H.OVERLAP_PATCH + [(_TR_ANCHOR, _TR_INJ, 1), (_T_ANCHOR, _T_INJ, 1)]


# ─────────────────────────────── airframer board ───────────────────────────────
@functools.lru_cache(maxsize=None)
def af_board(eis):
    """Solve the airframer board at an EIS tuple (fps, ngsa, 787, a350). Cached: each tuple is one board run."""
    over = {"af_fps_eis": eis[0], "af_ngsa_eis": eis[1], "af_787_eis": eis[2], "af_a350_eis": eis[3]}
    MX, A, B, SS = H.af(over, AF_PATCH)
    return SS


@functools.lru_cache(maxsize=None)
def en_board():
    """The engine board's parameters (prices, WACC, EV, base shares, R&D, strain) and its simulate()."""
    return H.en({})


def af_params():
    return af_board((DEFAULT_EIS["fps"], DEFAULT_EIS["ngsa"], DEFAULT_EIS["re787"], DEFAULT_EIS["rea350"]))["_AFLOC"]


def eval_cell(eis, a_strat, b_strat, trace=False):
    SS = af_board(eis)
    if trace:
        SS["_TRACE"] = []
    try:
        cell = dict(SS["_EVAL"](a_strat, b_strat))
        if trace:
            cell["_trace"] = SS["_TRACE"]
    finally:
        SS["_TRACE"] = None
    return cell


def true_cost(nom, pv, debt, ev, alpha):
    """The board's calculate_tc(): PV of spend plus the α debt penalty, PV'd by the spend's own discount factor."""
    if nom <= 0:
        return 0.0
    base_pen = debt * alpha * ((debt / ev) ** 2)
    new_debt = debt + nom
    new_pen = new_debt * alpha * ((new_debt / ev) ** 2)
    return pv + (new_pen - base_pen) * (pv / nom)


def pv_stream(nom, t0, t1, wacc):
    """The board's get_pv_stream(): nominal spread evenly over t0..t1, discounted to 2026."""
    if nom == 0 or t1 < t0:
        return 0.0
    n = t1 - t0 + 1
    return sum((nom / n) / ((1 + wacc) ** t) for t in range(t0, t1 + 1))


# ─────────────────────────────── engine board ───────────────────────────────
def engine_params():
    L = en_board()["_ELOC"]
    keys = ["CPI", "ENGINES_PER_AC", "NB_AC_PER_YR", "WB_AC_PER_YR", "NB_ENGINE_PRICE_M", "WB_ENGINE_PRICE_M",
            "gross_mult", "wacc_a", "wacc_b", "wacc_c", "ev_a", "ev_b", "ev_c", "base_cfm_nb", "base_pw_nb",
            "base_rr_nb", "base_cfm_wb", "base_pw_wb", "base_rr_wb", "start_cfm_wb", "start_rr_wb", "open_fan_loss",
            "ducted_fan_gain", "lobby_cost", "strain_penalty", "rr_nbwb_strain", "inv_cfm_open_fan_rd",
            "inv_cfm_ducted_rd", "inv_pw_gtf2_solo_rd", "inv_pw_gtf2_jv_rd", "inv_rr_rd_nb", "inv_rr_rd_wb",
            "inv_rr_t1000_rd", "NPV_POST_EIS_YRS", "TIMELINE_YRS"]
    return {k: L[k] for k in keys}


def cfm_move(parts):
    of, du = "open_fan" in parts, "ducted" in parts
    base = "3-Open + Ducted" if (of and du) else "1-Open Fan Only" if of else "2-Ducted Only" if du else "0-Milk LEAP"
    s = base
    if "embraer" in parts:
        s += " | 4-Partner Embraer"
    if "lobby" in parts:
        s += " | 5-Lobby Govts"
    if "genx9" in parts:
        s += " | 6-Upgrade GenX9"
    elif "genx_invest" in parts:
        s += " | 7-Invest GenX"
    return s


def pw_move(parts):
    return "3-JV with RR for GTF" if "jv" in parts else "2-Launch GTF2 Go Solo" if "solo" in parts else "1-Milk GTF"


def rr_move(parts):
    nb = "3-JV with PW for NB" if "jv" in parts else "2-Ultrafan NB Solo" if "solo" in parts else "0-Do Nothing (Milk WB)"
    wb = " | 1-Ultrafan WB" if "uf_wb" in parts else " | 4-Upgrade T1000" if "t1000" in parts else ""
    return (nb.replace(" (Milk WB)", "") + wb) if wb else nb


def post_shares(move_a, move_b, move_c, start_nb, start_wb, P):
    """The share block of the board's simulate(), verbatim in logic: start shares + move effects, floored, normalised.
    start_nb = (cfm, pw, rr) already normalised; start_wb = (cfm, pw, rr)."""
    a_nb, b_nb, c_nb = start_nb
    a_wb, b_wb, c_wb = start_wb
    has_of = ("1-Open Fan" in move_a) or ("3-Open + Ducted" in move_a)
    has_du = ("2-Ducted" in move_a) or ("3-Open + Ducted" in move_a)
    has_lobby = "5-Lobby Govts" in move_a
    rr_nb_active = "Ultrafan NB" in move_c or "JV with PW" in move_c
    if has_of:
        loss = min(P["open_fan_loss"], 0.20) if has_lobby else P["open_fan_loss"]
        a_nb -= loss
        if rr_nb_active:
            b_nb += loss / 2; c_nb += loss / 2
        else:
            b_nb += loss
    if has_du:
        a_nb += P["ducted_fan_gain"]
        if rr_nb_active:
            b_nb -= P["ducted_fan_gain"] / 2; c_nb -= P["ducted_fan_gain"] / 2
        else:
            b_nb -= P["ducted_fan_gain"]
    if "4-Partner Embraer" in move_a:
        a_nb += 0.05
    if "6-Upgrade GenX9" in move_a:
        a_wb += 0.05
    if "7-Invest GenX" in move_a:
        a_wb += 0.05
    jv = False
    if "2-Launch GTF2" in move_b:
        b_nb += 0.10; a_nb -= 0.05; c_nb -= 0.05
    if "3-JV with RR" in move_b:
        jv = True
        a_nb -= 0.10; b_nb += 0.05; c_nb += 0.05
    if "1-Ultrafan WB" in move_c:
        c_wb += 0.10; a_wb -= 0.10
    if "2-Ultrafan NB" in move_c:
        c_nb += 0.15; a_nb -= 0.10; b_nb -= 0.05
    if "3-JV with PW" in move_c:
        jv = True
        c_nb += 0.05; b_nb += 0.05; a_nb -= 0.10
    if "4-Upgrade T1000" in move_c:
        c_wb += 0.05; a_wb -= 0.05
    if jv:
        avg = (b_nb + c_nb) / 2.0
        b_nb = c_nb = avg
    a_nb, b_nb, c_nb = max(0, a_nb), max(0, b_nb), max(0, c_nb)
    a_wb, b_wb, c_wb = max(0, a_wb), max(0, b_wb), max(0, c_wb)
    t = a_nb + b_nb + c_nb
    if t > 0:
        a_nb /= t; b_nb /= t; c_nb /= t
    t = a_wb + b_wb + c_wb
    if t > 0:
        a_wb /= t; b_wb /= t; c_wb /= t
    return (a_nb, b_nb, c_nb), (a_wb, b_wb, c_wb)


def start_from_slots(slots, jv):
    """Engine start shares from the airframer slots: [(maker_set, airframer_share)], each slot split equally among its
    makers (the board's derive_nb_engine_shares). With a Joint Venture the board starts PW and RR at half the JV slider
    each; the GM sets that slider to PW + RR, so PW = RR = (PW + RR) / 2."""
    sh = {"CFM": 0.0, "PW": 0.0, "RR": 0.0}
    for makers, s in slots:
        for m in makers:
            sh[m] += s / len(makers)
    cfm, pw, rr = sh["CFM"], sh["PW"], sh["RR"]
    if jv:
        pw = rr = (pw + rr) / 2.0
    tot = cfm + pw + rr
    return (cfm / tot, pw / tot, rr / tot) if tot > 0 else (0, 0, 0)


# ─────────────────────────────── programme catalogue ───────────────────────────────
# Development times (years from launch to entry into service / engine ready). Board-implied where the board has one.
AF_DEV = {"fps_7yr": 7, "fps_10yr": 10, "fps_embraer": 10, "ngsa": 7, "re787": 5, "rea350": 5}
FPS_STRAT = {"7yr": "Launch_fps_7yr_Solo", "10yr": "Launch_fps_10yr_Solo", "embraer": "Launch_fps_via_Embraer"}
EN_SIDE = {"cfm_ducted": "cfm", "cfm_open_fan": "cfm", "cfm_embraer": "cfm", "cfm_lobby": "cfm", "cfm_genx": "cfm",
           "pw_solo": "pratt_whitney", "rr_solo": "rolls_royce", "jv": "jv", "rr_uf_wb": "rolls_royce",
           "rr_t1000": "rolls_royce"}
AF_SIDE = {"fps": "boeing", "re787": "boeing", "rate737": "boeing", "ngsa": "airbus", "rea350": "airbus"}
OPEN_FAN_EARLIEST = 2045            # the board: "Open Fan not ready until 2045"

PROG_LABEL = {"fps": "fps (Boeing)", "re787": "787 Re-engine (Boeing)", "ngsa": "NGSA (Airbus)",
              "rea350": "A350 Re-engine (Airbus)", "cfm_ducted": "CFM ducted engine", "cfm_open_fan": "CFM Open Fan (RISE)",
              "cfm_embraer": "CFM-Embraer partnership", "cfm_lobby": "CFM emissions lobbying",
              "cfm_genx": "GEnx (CFM/GE)", "pw_solo": "P&W GTF2 (Solo)", "rr_solo": "RR UltraFan NB (Solo)",
              "jv": "P&W-RR Joint Venture NB engine", "rr_uf_wb": "RR UltraFan WB", "rr_t1000": "RR Trent 1000 upgrade"}



def engine_ready(key, launch):
    """Year an engine programme launched in `launch` is ready to enter service."""
    return {"cfm_ducted": launch + 6, "cfm_open_fan": max(OPEN_FAN_EARLIEST, launch + 10), "cfm_embraer": launch + 7,
            "cfm_lobby": launch, "cfm_genx": launch + 3, "pw_solo": launch + 6, "rr_solo": launch + 7,
            "jv": launch + 6, "rr_uf_wb": launch + 6, "rr_t1000": launch + 3}[key]


def af_bill(key, variant=None):
    p = af_params()
    if key == "fps":
        return {"7yr": p["v_capex_fps_7yr"], "10yr": p["v_capex_fps_10yr"], "embraer": p["v_capex_fps_emb"]}[variant]
    return {"ngsa": p["v_capex_angsa"], "re787": p["v_capex_787_reengine"], "rea350": p["v_capex_a350_reengine"]}[key]


def af_dev(key, variant=None):
    return AF_DEV["fps_" + variant] if key == "fps" else AF_DEV[key]


def en_rd(key, maker=None):
    """Board R&D charge ($B, undiscounted) of an engine programme, for one maker (the Joint Venture is split)."""
    P = engine_params()
    if key == "jv":
        return P["inv_pw_gtf2_jv_rd"] if maker == "pratt_whitney" else P["inv_rr_rd_nb"] / 2.0
    return {"cfm_ducted": P["inv_cfm_ducted_rd"], "cfm_open_fan": P["inv_cfm_open_fan_rd"], "cfm_embraer": 0.0,
            "cfm_lobby": P["lobby_cost"], "cfm_genx": 0.0, "pw_solo": P["inv_pw_gtf2_solo_rd"],
            "rr_solo": P["inv_rr_rd_nb"], "rr_uf_wb": P["inv_rr_rd_wb"], "rr_t1000": P["inv_rr_t1000_rd"]}[key]


def new_state():
    return {"year": None, "prog": {}, "rate737": None, "dt": {"bottleneck": None, "poaching": None},
            "dead": [], "jv_commit": {"pratt_whitney": None, "rolls_royce": None}, "codes": {}, "log": []}


def live(state, key):
    r = state["prog"].get(key)
    return r if (r and r.get("cancel") is None) else None


# ─────────────────────────────── engine availability ───────────────────────────────
CODE_SETS = {1: ({"RR"}, False), 2: ({"PW"}, False), 3: ({"CFM"}, False), 4: ({"RR", "PW"}, True),
             5: ({"RR", "CFM"}, False), 6: ({"PW", "CFM"}, False), 7: ({"RR", "PW", "CFM"}, False)}
CODE_LABEL = {1: "RR", 2: "PW", 3: "CFM", 4: "RR & PW (JV)", 5: "RR and CFM", 6: "PW and CFM", 7: "RR, PW and CFM"}
FORBIDDEN = {(1, 1), (1, 4), (2, 2), (2, 4), (3, 3), (4, 1), (4, 2), (4, 4), (5, 5), (6, 6)}


def maker_ready_by(state, maker, eis):
    """Can `maker` put a new narrowbody engine on an airframe entering service in `eis`?"""
    if maker == "CFM":
        return True                      # LEAP derivative or a new CFM engine: the board never removes CFM
    keys = ["pw_solo", "jv"] if maker == "PW" else ["rr_solo", "jv"]
    return any(live(state, k) and live(state, k)["ready"] <= eis for k in keys)


def effective_code(state, key):
    """(maker set, jv flag, note) actually fitted to a live new airframe, after removing makers not ready by its EIS."""
    r = live(state, key)
    code = state["codes"].get(key) or 7
    makers, jv = CODE_SETS[code]
    eis = r["eis"]
    if jv:
        j = live(state, "jv")
        if j and j["ready"] <= eis:
            return set(makers), True, ""
        keep = {m for m in makers if maker_ready_by(state, m, eis)}
        note = "Joint Venture not ready by EIS"
        return (keep or {"CFM"}), False, note + ("; fallback to CFM" if not keep else "")
    keep = {m for m in makers if maker_ready_by(state, m, eis)}
    dropped = sorted(set(makers) - keep)
    note = ("not ready by EIS: " + ", ".join(dropped)) if dropped else ""
    if not keep:
        return {"CFM"}, False, note + "; fallback to CFM"
    return keep, False, note


# ─────────────────────────────── airframer valuation ───────────────────────────────
def af_inputs(state, covert=True):
    """Map a game state to the board: EIS tuple and the two strategy tuples."""
    fps, ngsa, b7, a3 = live(state, "fps"), live(state, "ngsa"), live(state, "re787"), live(state, "rea350")
    eis = (fps["eis"] if fps else DEFAULT_EIS["fps"], ngsa["eis"] if ngsa else DEFAULT_EIS["ngsa"],
           b7["eis"] if b7 else DEFAULT_EIS["re787"], a3["eis"] if a3 else DEFAULT_EIS["rea350"])
    dt = state["dt"] if covert else {"bottleneck": None, "poaching": None}
    a = ("Launch_NGSA" if ngsa else "Milk_A320neo",
         "Sabotage_Bottleneck" if dt["bottleneck"] else "No_Bottleneck",
         "Sabotage_Poaching" if dt["poaching"] else "No_Poaching",
         "Re_engine_A350" if a3 else "Milk_A350")
    b = (FPS_STRAT[fps["variant"]] if fps else "Milk_737MAX",
         "Increase_737_Rate" if state["rate737"] else "No_Rate_Increase",
         "Re_engine_787" if b7 else "Milk_787")
    return eis, a, b, dt


def fps_reference_eis(state):
    """The fps date Delay Tactics aim at: the live fps, else a cancelled one's planned date, else the snapshot default."""
    fps = live(state, "fps")
    if fps:
        return fps["eis"], "live"
    dead = [d for d in state["dead"] if d["key"] == "fps"]
    if dead:
        return dead[-1]["eis"], "cancelled"
    return DEFAULT_EIS["fps"], "never"


def value_airframers(state, covert=True, series=True):
    """Board cell at the state's EIS dates plus GM adjustments. Returns {'boeing': {...}, 'airbus': {...}}."""
    p = af_params()
    eis, a, b, dt = af_inputs(state, covert)
    cell = eval_cell(eis, a, b, trace=series)
    out = {}
    for side, pre, wacc, ev, debt in (("boeing", "b", p["WACC_B"], p["v_ev_boeing"], p["v_debt_boeing"]),
                                      ("airbus", "a", p["WACC_A"], p["v_ev_airbus"], p["v_debt_airbus"])):
        tc = cell[pre + "_tc_data"]
        nom, pv = tc.get("nom_capex", 0.0), tc.get("pv_capex", 0.0)
        board_tc = tc["total_tc"]
        strain_pv = -cell[pre + "_strain"]
        strain_nom = strain_pv * (nom / pv) if pv > 0 else strain_pv
        adj = {}
        # Delay Tactics spending window and naked fine (Airbus only)
        sab_pv_board = cell.get("a_pv_sabotage", 0.0) if side == "airbus" else 0.0
        sab_pv_gm = sab_pv_board
        fine_board = -cell.get("a_delta_reg", 0.0) if side == "airbus" else 0.0
        fine_gm = fine_board
        fine_year = None
        if side == "airbus" and (dt["bottleneck"] or dt["poaching"]):
            ref, kind = fps_reference_eis(state)
            rt = ref - Y0
            sab_pv_gm = 0.0
            for yr in (dt["bottleneck"], dt["poaching"]):
                if yr:
                    ty = yr - Y0
                    w0 = max(ty, max(0, rt - 9))
                    w1 = max(w0, rt - 1)
                    sab_pv_gm += pv_stream(p["v_sabotage_cost"], w0, w1, wacc)
            if kind == "never":
                fine_year = max(ref, max(y for y in (dt["bottleneck"], dt["poaching"]) if y))
                fine_gm = p["v_naked_sabotage_fine"] / ((1 + wacc) ** (fine_year - Y0))
            else:
                fine_gm = 0.0
        # cancellation write-offs
        sunk_nom = sum(d["sunk_nom"] for d in state["dead"] if d["side"] == side)
        sunk_pv = sum(d["sunk_nom"] / ((1 + wacc) ** (d["cancel"] - Y0)) for d in state["dead"] if d["side"] == side)
        pv_gm = pv - sab_pv_board + sab_pv_gm
        tc_gm = true_cost(nom + sunk_nom, pv_gm + sunk_pv, debt, ev, p["v_alpha"])
        strain_gm = strain_nom * (pv_gm / nom) if nom > 0 else strain_pv
        board_total = cell[pre + "_total_delta"]
        total = board_total - (tc_gm - board_tc) - (strain_gm - strain_pv) - (fine_gm - fine_board)
        adj = {"true_cost_change": -(tc_gm - board_tc), "strain_change": -(strain_gm - strain_pv),
               "fine_change": -(fine_gm - fine_board)}
        rate_pv = -cell.get("b_pv_rate_hike", 0.0) if side == "boeing" else 0.0
        # bridge: every line in PV $B at 2026; sums exactly to `total`
        inv_pv = cell[pre + "_pv_nb_invest"] + cell[pre + "_pv_wb_invest"]
        alpha_pv = tc_gm - (pv_gm + sunk_pv)
        bridge = {"nb_profit_vs_sq": cell[pre + "_delta_nb"], "wb_profit_vs_sq": cell[pre + "_delta_wb"],
                  "programme_investment": -inv_pv, "rate_hike": -rate_pv,
                  "delay_tactics_spend": -sab_pv_gm, "write_offs": -sunk_pv, "debt_penalty": -alpha_pv,
                  "two_front_strain": -strain_gm, "naked_fine": -fine_gm}
        chk = sum(bridge.values())
        assert abs(chk - total) < 1e-9, (side, chk, total, bridge)
        out[side] = {"pv_delta": total, "yield": 100.0 + total / ev * 100.0, "board_pv_delta": board_total,
                     "board_yield": cell["yield_" + pre], "gm_adjustments": adj, "bridge": bridge, "ev": ev,
                     "wacc": wacc, "fine_year": fine_year if side == "airbus" else None}
    out["_inputs"] = {"eis": eis, "a": a, "b": b}
    if series:
        out["_series"] = af_series(state, cell, eis, dt)
    return out


def af_series(state, cell, eis, dt):
    """Year-by-year airframer series traced from evaluate_scenario(); PVs reconcile to the board cell."""
    p = af_params()
    base = af_board(eis)["_BASE"]
    tr = cell["_trace"]
    acc = {"b_nb": 0.0, "a_nb": 0.0, "b_wb": 0.0, "a_wb": 0.0, "bb_nb": 0.0, "ab_nb": 0.0, "bb_wb": 0.0, "ab_wb": 0.0}
    rows = []
    for r in tr:
        t = r["t"]
        yr = Y0 + t
        b_nb_u, a_nb_u = p["NB_PER_YR"] * r["b_sh_nb"], p["NB_PER_YR"] * r["a_sh_nb"]
        b_wb_u, a_wb_u = p["WB_PER_YR"] * r["b_sh_wb"], p["WB_PER_YR"] * r["a_sh_wb"]
        row = {"year": yr,
               "boeing": {"nb_share": r["b_sh_nb"], "wb_share": r["b_sh_wb"], "nb_units": b_nb_u, "wb_units": b_wb_u,
                          "nb_price": r["b_p_nb"] * 1000, "nb_margin": r["b_m_nb"], "wb_margin": r["b_m_wb"],
                          "nb_revenue": b_nb_u * r["b_p_nb"], "wb_revenue": b_wb_u * p["PRICE_WB"],
                          "nb_profit": b_nb_u * r["b_p_nb"] * r["b_m_nb"], "wb_profit": b_wb_u * p["PRICE_WB"] * r["b_m_wb"],
                          "nb_in_window": r["b_nb_in"], "wb_in_window": r["b_wb_in"]},
               "airbus": {"nb_share": r["a_sh_nb"], "wb_share": r["a_sh_wb"], "nb_units": a_nb_u, "wb_units": a_wb_u,
                          "nb_price": r["a_p_nb"] * 1000, "nb_margin": r["a_m_nb"], "wb_margin": r["a_m_wb"],
                          "nb_revenue": a_nb_u * r["a_p_nb"], "wb_revenue": a_wb_u * p["PRICE_WB"],
                          "nb_profit": a_nb_u * r["a_p_nb"] * r["a_m_nb"], "wb_profit": a_wb_u * p["PRICE_WB"] * r["a_m_wb"],
                          "nb_in_window": r["a_nb_in"], "wb_in_window": r["a_wb_in"]}}
        # status quo (the board's BASE): 40/60 NB on legacy price and margin, 100/170 vs 70/170 WB on status-quo margins
        sq = {"boeing": {"nb_profit": p["NB_PER_YR"] * 0.40 * p["PRICE_737"] * p["v_margin_737"],
                         "wb_profit": p["WB_PER_YR"] * (100 / 170) * p["PRICE_WB"] * p["v_margin_787"]},
              "airbus": {"nb_profit": p["NB_PER_YR"] * 0.60 * p["PRICE_A320"] * p["v_margin_a320"],
                         "wb_profit": p["WB_PER_YR"] * (70 / 170) * p["PRICE_WB"] * p["v_margin_a350"]}}
        for s in ("boeing", "airbus"):
            row[s]["sq_nb_profit"] = sq[s]["nb_profit"]
            row[s]["sq_wb_profit"] = sq[s]["wb_profit"]
        if r["b_nb_in"]:
            acc["b_nb"] += row["boeing"]["nb_profit"] * r["df_b"]; acc["bb_nb"] += sq["boeing"]["nb_profit"] * r["df_b"]
        if r["a_nb_in"]:
            acc["a_nb"] += row["airbus"]["nb_profit"] * r["df_a"]; acc["ab_nb"] += sq["airbus"]["nb_profit"] * r["df_a"]
        if r["b_wb_in"]:
            acc["b_wb"] += row["boeing"]["wb_profit"] * r["df_b"]; acc["bb_wb"] += sq["boeing"]["wb_profit"] * r["df_b"]
        if r["a_wb_in"]:
            acc["a_wb"] += row["airbus"]["wb_profit"] * r["df_a"]; acc["ab_wb"] += sq["airbus"]["wb_profit"] * r["df_a"]
        rows.append(row)
    for k, ck in (("b_nb", "b_scen_nb_pv"), ("a_nb", "a_scen_nb_pv"), ("b_wb", "b_scen_wb_pv"), ("a_wb", "a_scen_wb_pv")):
        assert abs(acc[k] - cell[ck]) < 1e-9, (k, acc[k], cell[ck])
    for k, bk in (("bb_nb", "b_base_nb"), ("ab_nb", "a_base_nb"), ("bb_wb", "b_base_wb"), ("ab_wb", "a_base_wb")):
        assert abs(acc[k] - base[bk]) < 1e-9, (k, acc[k], base[bk])
    # non-recurring spend as the board books it (nominal $B by calendar year), plus GM items
    nr = {"boeing": {}, "airbus": {}}

    def put(side, yr, item, v):
        if v:
            nr[side].setdefault(yr, {}).setdefault(item, 0.0)
            nr[side][yr][item] += v
    fps, ngsa, b7, a3 = live(state, "fps"), live(state, "ngsa"), live(state, "re787"), live(state, "rea350")
    if fps:
        put("boeing", fps["eis"], "fps (" + fps["variant"] + ")", af_bill("fps", fps["variant"]))
    if b7:
        put("boeing", b7["eis"], "787 Re-engine", af_bill("re787"))
    if state["rate737"]:
        put("boeing", 2032, "737 rate increase", p["v_capex_737_rate_hike"])
    if ngsa:
        put("airbus", ngsa["eis"], "NGSA", af_bill("ngsa"))
    if a3:
        put("airbus", a3["eis"], "A350 Re-engine", af_bill("rea350"))
    if dt["bottleneck"] or dt["poaching"]:
        ref, kind = fps_reference_eis(state)
        rt = ref - Y0
        for yr in (dt["bottleneck"], dt["poaching"]):
            if yr:
                w0 = max(yr - Y0, max(0, rt - 9)); w1 = max(w0, rt - 1)
                for t in range(w0, w1 + 1):
                    put("airbus", Y0 + t, "Delay Tactics", p["v_sabotage_cost"] / (w1 - w0 + 1))
        if kind == "never":
            fy = max(ref, max(y for y in (dt["bottleneck"], dt["poaching"]) if y))
            put("airbus", fy, "naked Delay Tactics fine", p["v_naked_sabotage_fine"])
    for d in state["dead"]:
        if d["side"] in nr:
            put(d["side"], d["cancel"], "write-off: " + d["label"], d["sunk_nom"])
    return {"years": rows, "nonrecurring": nr}


# ─────────────────────────────── engine valuation ───────────────────────────────
def engine_timing(state):
    """Anchors of the engine board's two windows and the year each engine programme starts to count."""
    nb_live = [r["eis"] for k in ("fps", "ngsa") for r in [live(state, k)] if r]
    nb_anchor = min(nb_live) if nb_live else None
    wb_live = [r["eis"] for k in ("re787", "rea350") for r in [live(state, k)] if r]
    # WB window: the board's own anchor, min(787 EIS, A350 EIS) with unlaunched programmes at the snapshot dates.
    # Upgrades to today's engines start counting from the snapshot date (2035) at the earliest, so a re-engine
    # launched later never rewrites years already played.
    wb_anchor = min(live(state, "re787")["eis"] if live(state, "re787") else DEFAULT_EIS["re787"],
                    live(state, "rea350")["eis"] if live(state, "rea350") else DEFAULT_EIS["rea350"])
    wb_upgrade_start = min(DEFAULT_EIS["re787"], DEFAULT_EIS["rea350"])
    start = {}
    for k in ("cfm_ducted", "cfm_embraer", "pw_solo", "rr_solo"):
        r = live(state, k)
        if r and nb_anchor is not None:
            start[k] = max(r["ready"], nb_anchor)
    j = live(state, "jv")
    if j and nb_anchor is not None:
        # a Joint Venture counts from the year it forms at the earliest, even when it inherits an earlier schedule
        start["jv"] = max(j["ready"], nb_anchor, j["launch"])
    for k in ("pw_solo", "rr_solo"):
        f = state["prog"].get("_folded_" + k)
        if f and nb_anchor is not None:
            # a solo programme folded into the Joint Venture keeps counting in the years before the fold
            start[k] = (max(f["ready"], nb_anchor), f["cancel"])
    of = live(state, "cfm_open_fan")
    if of and nb_anchor is not None and nb_anchor < of["ready"]:
        start["cfm_open_fan"] = max(of["launch"], nb_anchor)      # the board's wait penalty
    lob = live(state, "cfm_lobby")
    if lob:
        start["cfm_lobby"] = lob["launch"]
    for k in ("cfm_genx", "rr_t1000"):
        r = live(state, k)
        if r:
            start[k] = max(r["ready"], wb_upgrade_start)
    uf = live(state, "rr_uf_wb")
    if uf and wb_live:
        start["rr_uf_wb"] = max(uf["ready"], min(wb_live))
    return nb_anchor, wb_anchor, start


def engine_moves_at(state, start, yr):
    def on(k):
        if k not in start:
            return False
        s0, s1 = start[k] if isinstance(start[k], tuple) else (start[k], None)
        return s0 <= yr and (s1 is None or yr < s1)
    cfm = set()
    if on("cfm_open_fan"): cfm.add("open_fan")
    if on("cfm_ducted"): cfm.add("ducted")
    if on("cfm_embraer"): cfm.add("embraer")
    if on("cfm_lobby"): cfm.add("lobby")
    if on("cfm_genx"): cfm.add(live(state, "cfm_genx")["kind"])
    pw, rr = set(), set()
    if on("jv"):
        pw.add("jv"); rr.add("jv")
    else:
        if on("pw_solo"): pw.add("solo")
        if on("rr_solo"): rr.add("solo")
    if on("rr_uf_wb"): rr.add("uf_wb")
    elif on("rr_t1000"): rr.add("t1000")
    return cfm_move(cfm), pw_move(pw), rr_move(rr)


def nb_slots_at(state, yr, b_share):
    """The two airframer slots of the new-NB engine market in `yr`: (maker set, airframer NB share)."""
    fps, ngsa = live(state, "fps"), live(state, "ngsa")
    bset = effective_code(state, "fps")[0] if (fps and yr >= fps["eis"]) else {"CFM"}           # 737: LEAP-1B
    aset = effective_code(state, "ngsa")[0] if (ngsa and yr >= ngsa["eis"]) else {"PW", "CFM"}  # A320neo
    return [(bset, b_share), (aset, 1.0 - b_share)]


def value_engines(state, b_nb_share, series=True, board_mode=None):
    """Engine makers' PV deltas. b_nb_share: {year: Boeing NB share} from the airframer trace.
    board_mode = (f_nb tuple (cfm, pw, rr), nb_eis_t, wb_eis_t, move_a, move_b, move_c) reproduces simulate()."""
    P = engine_params()
    T_post = P["NPV_POST_EIS_YRS"]
    base_nb = (P["base_cfm_nb"], P["base_pw_nb"], P["base_rr_nb"])
    base_wb = (P["base_cfm_wb"], P["base_pw_wb"], P["base_rr_wb"])
    start_wb = (P["start_cfm_wb"], 0.0, P["start_rr_wb"])
    nb_price, wb_price = P["NB_ENGINE_PRICE_M"], P["WB_ENGINE_PRICE_M"]
    waccs = (P["wacc_a"], P["wacc_b"], P["wacc_c"])
    if board_mode:
        f_nb, nb_t, wb_t, ma, mb, mc = board_mode
        nb_anchor_t, wb_anchor_t = nb_t, wb_t
        tot = sum(f_nb)
        f_norm = tuple(x / tot for x in f_nb)
        post_fixed = post_shares(ma, mb, mc, f_norm, start_wb, P)
    else:
        nb_anchor, wb_anchor, start = engine_timing(state)
        nb_anchor_t = (nb_anchor - Y0) if nb_anchor is not None else None
        wb_anchor_t = wb_anchor - Y0
    nb_end = (nb_anchor_t if nb_anchor_t is not None else min(DEFAULT_EIS["fps"], DEFAULT_EIS["ngsa"]) - Y0) + T_post - 1
    wb_end = wb_anchor_t + T_post - 1
    T = max(P["TIMELINE_YRS"], nb_end + 1, wb_end + 1, REPORT_END - Y0 + 1)
    new = [0.0, 0.0, 0.0]; old = [0.0, 0.0, 0.0]
    rows = []
    for t in range(T):
        yr = Y0 + t
        if board_mode:
            nb_post, wb_post = post_fixed
            moves = (ma, mb, mc)
        else:
            moves = engine_moves_at(state, start, yr)
            bsh = b_nb_share.get(yr, b_nb_share[max(b_nb_share)])
            jv = "3-JV" in moves[1]
            st_nb = start_from_slots(nb_slots_at(state, yr, bsh), jv) if nb_anchor_t is not None else base_nb
            nb_post, wb_post = post_shares(moves[0], moves[1], moves[2], st_nb, start_wb, P)
        nb_sh = base_nb if (nb_anchor_t is None or t < nb_anchor_t) else nb_post
        # board mode switches WB at the board's anchor; in the game each WB move has its own start year (above)
        wb_sh = (base_wb if t < wb_anchor_t else wb_post) if board_mode else wb_post
        g = P["gross_mult"] * ((1 + P["CPI"]) ** t)
        row = {"year": yr, "moves": moves, "nb_in_window": t <= nb_end, "wb_in_window": t <= wb_end}
        for i, side in enumerate(("cfm", "pratt_whitney", "rolls_royce")):
            nb_u = P["NB_AC_PER_YR"] * P["ENGINES_PER_AC"] * nb_sh[i]
            wb_u = P["WB_AC_PER_YR"] * P["ENGINES_PER_AC"] * wb_sh[i]
            nb_v = nb_u * nb_price * g / 1000.0
            wb_v = wb_u * wb_price * g / 1000.0
            nb_b = P["NB_AC_PER_YR"] * P["ENGINES_PER_AC"] * base_nb[i] * nb_price * g / 1000.0
            wb_b = P["WB_AC_PER_YR"] * P["ENGINES_PER_AC"] * base_wb[i] * wb_price * g / 1000.0
            df = (1 + waccs[i]) ** t
            if t <= nb_end:
                new[i] += (nb_v if nb_sh[i] > 0 else 0.0) / df; old[i] += (nb_b if base_nb[i] > 0 else 0.0) / df
            if t <= wb_end:
                new[i] += (wb_v if wb_sh[i] > 0 else 0.0) / df; old[i] += (wb_b if base_wb[i] > 0 else 0.0) / df
            row[side] = {"nb_share": nb_sh[i], "wb_share": wb_sh[i], "nb_units": nb_u, "wb_units": wb_u,
                         "nb_value": nb_v, "wb_value": wb_v, "sq_nb_value": nb_b, "sq_wb_value": wb_b,
                         "nb_share_sq": base_nb[i], "wb_share_sq": base_wb[i]}
        rows.append(row)
    out = {}
    if board_mode:
        return {"new": new, "old": old}
    rd, strain, sunk, nr = engine_costs(state)
    for i, side in enumerate(("cfm", "pratt_whitney", "rolls_royce")):
        ev = (P["ev_a"], P["ev_b"], P["ev_c"])[i]
        mkt = new[i] - old[i]
        total = mkt - rd[side] - strain[side] - sunk[side]
        out[side] = {"pv_delta": total, "yield": 100.0 + total / max(0.1, ev) * 100.0, "ev": ev, "wacc": waccs[i],
                     "bridge": {"engine_value_vs_sq": mkt, "r_and_d": -rd[side], "strain": -strain[side],
                                "write_offs": -sunk[side]},
                     "pv_new": new[i], "pv_sq": old[i]}
    out["_timing"] = {"nb_anchor": None if nb_anchor_t is None else Y0 + nb_anchor_t, "wb_anchor": Y0 + wb_anchor_t,
                      "nb_window_end": Y0 + nb_end, "wb_window_end": Y0 + wb_end}
    if series:
        out["_series"] = {"years": rows, "nonrecurring": nr}
    return out


def engine_costs(state):
    """Board R&D (undiscounted, charged in full when a programme is live), board strain, and GM write-offs."""
    P = engine_params()
    rd = {"cfm": 0.0, "pratt_whitney": 0.0, "rolls_royce": 0.0}
    nr = {"cfm": {}, "pratt_whitney": {}, "rolls_royce": {}}

    def put(side, yr, item, v):
        if v:
            nr[side].setdefault(yr, {}).setdefault(item, 0.0)
            nr[side][yr][item] += v
    labels = {"cfm_ducted": "Ducted engine R&D", "cfm_open_fan": "Open Fan R&D", "cfm_lobby": "Emissions lobbying",
              "pw_solo": "GTF2 R&D", "rr_solo": "UltraFan NB R&D", "rr_uf_wb": "UltraFan WB R&D",
              "rr_t1000": "Trent 1000 upgrade R&D", "jv": "Joint Venture NB R&D"}
    for k, side in EN_SIDE.items():
        r = live(state, k)
        if not r:
            continue
        if k == "jv":
            for s in ("pratt_whitney", "rolls_royce"):
                rd[s] += en_rd(k, s); put(s, r["launch"], labels[k], en_rd(k, s))
        else:
            rd[side] += en_rd(k); put(side, r["launch"], labels.get(k, k), en_rd(k))
    # board strain rules
    cfm_pa = sum(1 for k in ("cfm_open_fan", "cfm_ducted", "cfm_embraer", "cfm_lobby", "cfm_genx") if live(state, k))
    if live(state, "cfm_open_fan") and live(state, "cfm_ducted"):
        cfm_pa += 1
    rr_nb = bool(live(state, "rr_solo") or live(state, "jv"))
    rr_wb = bool(live(state, "rr_uf_wb") or live(state, "rr_t1000"))
    strain = {"cfm": P["strain_penalty"] if cfm_pa >= 2 else 0.0, "pratt_whitney": 0.0,
              "rolls_royce": P["rr_nbwb_strain"] if (rr_nb and rr_wb) else 0.0}
    sunk = {"cfm": 0.0, "pratt_whitney": 0.0, "rolls_royce": 0.0}
    for d in state["dead"]:
        if d["side"] in sunk:
            sunk[d["side"]] += d["sunk_nom"]; put(d["side"], d["cancel"], "write-off: " + d["label"], d["sunk_nom"])
    return rd, strain, sunk, nr


def value(state, covert=True, series=True):
    """Full valuation of a state for all five players."""
    af = value_airframers(state, covert=covert, series=True)
    bshare = {r["year"]: r["boeing"]["nb_share"] for r in af["_series"]["years"]}
    en = value_engines(state, bshare, series=series)
    out = {"boeing": af["boeing"], "airbus": af["airbus"], "cfm": en["cfm"], "pratt_whitney": en["pratt_whitney"],
           "rolls_royce": en["rolls_royce"], "_af_inputs": af["_inputs"], "_engine_timing": en["_timing"]}
    if series:
        out["_af_series"] = af["_series"]
        out["_en_series"] = en["_series"]
    return out
