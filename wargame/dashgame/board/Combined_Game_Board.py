import streamlit as st
import itertools
import warnings   # Py3.14 fix: ensure 'warnings' is in sys.modules so
                  # pandas DataFrame.reset_index (used by st.bar_chart)
                  # doesn't KeyError inside warnings.catch_warnings().
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================
# 0. SINGLE PAGE CONFIG (must run before any other Streamlit call)
# ============================================================
st.set_page_config(page_title="Aerospace Game Theory Boards",
                   layout="wide", initial_sidebar_state="expanded")

# ── Top-of-page tab selector ────────────────────────────────
# Light styling to make the radio look like a row of tabs. This only
# styles the selector itself — neither board's internal CSS is touched.
st.markdown("""
<style>
div[data-testid="stRadio"] > div { flex-direction: row; gap: 6px; }
div[data-testid="stRadio"] label {
    background: #0a0a0a;
    border: 1px solid #333;
    border-radius: 8px 8px 0 0;
    padding: 10px 22px;
    margin: 0;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    color: #ccc !important;
    transition: all 0.15s ease;
}
div[data-testid="stRadio"] label:hover { background: #161616; border-color: #555; }
div[data-testid="stRadio"] label:has(input:checked) {
    background: #1a1a1a;
    border-color: #58a6ff;
    border-bottom: 3px solid #58a6ff;
    color: #58a6ff !important;
    font-weight: bold;
}
div[data-testid="stRadio"] label > div:first-child { display: none; }  /* hide the radio circle */
</style>
""", unsafe_allow_html=True)

_BOARD_SUMMARY   = "📋  Game Summary  —  At a Glance"
_BOARD_AIRFRAMER = "✈️  Airframer Duopoly  —  Airbus vs Boeing"
_BOARD_ENGINE    = "🔧  Engine 3-Player  —  CFM/GE vs PW vs RR"
_BOARD_DASHBOARD = "📊  Dashboard  —  Airframer Charts"

_board_choice = st.radio(
    "Select Board",
    [_BOARD_SUMMARY, _BOARD_AIRFRAMER, _BOARD_ENGINE, _BOARD_DASHBOARD],
    horizontal=True,
    label_visibility="collapsed",
    key="_top_level_board_selector",
)

# ────────────────────────────────────────────────────────────
# WORKAROUND for streamlit/streamlit#6074: keyed widgets lose
# their session_state value when their containing branch isn't
# rendered in a given run. By re-assigning every widget key to
# itself on every script execution, we force Streamlit to retain
# the value across tab switches.
# ────────────────────────────────────────────────────────────
_PERSIST_KEYS = ['_a_supplier', '_b_supplier', '_boeing_share_both', 'af_787_eis', 'af_a350_eis', 'af_alpha', 'af_cx_737rate', 'af_cx_787re', 'af_cx_a350re', 'af_cx_fps10', 'af_cx_fps7', 'af_cx_fpsemb', 'af_cx_ngsa', 'af_debt_airbus', 'af_debt_boeing', 'af_eps_tol', 'af_ev_airbus', 'af_ev_boeing', 'af_fps_7yr_adv', 'af_fps_eis', 'af_m_737', 'af_m_787', 'af_m_787_alone', 'af_m_787_both', 'af_m_a320', 'af_m_a350', 'af_m_a350_alone', 'af_m_a350_both', 'af_m_fps', 'af_m_ngsa', 'af_naked_fine', 'af_nb_milker', 'af_ngsa_eis', 'af_price_737', 'af_price_a320', 'af_price_fps', 'af_price_ngsa', 'af_price_wb', 'af_ramp10_a_pp', 'af_ramp10_b_pp', 'af_ramp7_a_pp', 'af_ramp7_b_pp', 'af_sab_cost', 'af_sab_share', 'af_strain_a', 'af_strain_b', 'af_wb_a_pp', 'af_wb_b_pp', 'af_wb_milker', 'en_debt_a', 'en_debt_b', 'en_debt_c', 'en_ducted_gain', 'en_eps_tol', 'en_ev_a', 'en_ev_b', 'en_ev_c', 'en_gross_mult', 'en_lobby_cost', 'en_openfan_loss', 'en_rd_cfm_open_fan', 'en_rd_cfm_ducted', 'en_rd_pw_solo', 'en_rd_pw_jv', 'en_rd_rr_nb', 'en_rd_rr_wb', 'en_rd_rr_t1000', 'en_rr_nbwb_strain', 'en_strain_cost', 'en_wacc_a', 'en_wacc_b', 'en_wacc_c', 'f_cfm_nb', 'f_cfm_wb', 'f_jv_nb', 'f_pw_nb', 'f_rr_nb', 'f_rr_wb', 'sq_cfm_nb', 'sq_cfm_wb', 'sq_pw_nb', 'sq_rr_wb']
for _k in _PERSIST_KEYS:
    if _k in st.session_state:
        st.session_state[_k] = st.session_state[_k]


# ============================================================
# UNIFIED NB SHARE RULE (v2)
# Single source of truth for the NB market share trajectory.
# Used by:
#   • evaluate_scenario (airframer Nash board)
#   • _boeing_yield / _airbus_yield (tornado simulators)
#   • _compute_aircraft_per_state (Summary tab aircraft delivery chart)
#   • Cash-flow chart per-year share
#
# CASES (year-by-year, t = year - 2026):
#   A. Neither launches            → status quo 40/60 all 31 yrs.
#   B. Both launch, SAME EIS year  → status quo 40/60 until EIS, then Phase 2
#                                    directly: Boeing climbs +4pp/yr toward 50%.
#                                    (Limiting case of "Phase 1 length = 0".)
#   C. NGSA leads (NGSA EIS BEFORE fps EIS, OR Boeing milks 737):
#      • Phase 1 (NGSA EIS onward, or until fps EIS-1 if both launch):
#        Airbus +3pp/yr from 60%, cap 80%.
#      • Phase 2 (only if Boeing also launches, from fps EIS onward):
#        Boeing climbs +4pp/yr toward 50% balance.
#        If Boeing's Phase 1 final share is already >= 50%, frozen (no movement).
#   D. fps leads  (fps EIS BEFORE NGSA EIS, OR Airbus milks A320):
#      • Phase 1 (fps EIS onward, or until NGSA EIS-1 if both launch):
#        Boeing +4pp/yr from 40%, cap 80%.
#      • Phase 2 (only if Airbus also launches, from NGSA EIS onward):
#        Airbus climbs +4pp/yr toward 50% balance.
#        If Airbus's Phase 1 final share is already >= 50%, frozen.
#
# Modifiers (rate hike, 7yr ramp, sabotage) stack additively on top
# via _apply_nb_modifiers().
# NO ANTICIPATION EFFECT.
# ============================================================
def _compute_nb_share_unified(t, b_launches, a_launches, b_eis_t, a_eis_t,
                              boeing_eq_share=None, is_7yr=False):
    """Return (b_share, a_share) at year t under the unified rule.

    `boeing_eq_share` is the post-2037 equilibrium Boeing share when both
    airframers launch (the "balance point" Phase 2 converges toward).
    If None (default), reads from session_state['_boeing_share_both'] / 100.0
    so the slider controls every chart and simulator path automatically.
    Pass an explicit value (0.0–1.0) to override for what-if analysis.

    `is_7yr` selects which share-shift speed sliders apply: True reads the
    7-yr ramp pair (af_ramp7_b_pp / af_ramp7_a_pp), False reads the 10-yr
    pair (af_ramp10_b_pp / af_ramp10_a_pp — also used for via-Embraer).
    Defaults of 4.0 / 4.0 reproduce the original fixed +4pp/yr rule.
    """
    if boeing_eq_share is None:
        try:
            boeing_eq_share = float(st.session_state.get('_boeing_share_both', 50)) / 100.0
        except Exception:
            boeing_eq_share = 0.50
    # Per-variant share-shift speeds (pp/yr → fraction). Sliders live in the
    # airframer sidebar; defaults reproduce the legacy hardcoded +4pp/yr.
    try:
        if is_7yr:
            _bg = float(st.session_state.get('af_ramp7_b_pp', 4.0)) / 100.0
            _ar = float(st.session_state.get('af_ramp7_a_pp', 4.0)) / 100.0
        else:
            _bg = float(st.session_state.get('af_ramp10_b_pp', 4.0)) / 100.0
            _ar = float(st.session_state.get('af_ramp10_a_pp', 4.0)) / 100.0
    except Exception:
        _bg, _ar = 0.04, 0.04
    both = b_launches and a_launches
    xor_b = b_launches and not a_launches
    xor_a = a_launches and not b_launches
    neither = not (b_launches or a_launches)
    same_eis = both and (b_eis_t == a_eis_t)

    b_eq = float(boeing_eq_share)
    a_eq = 1.0 - b_eq

    # Case A → status quo forever
    if neither:
        return 0.40, 0.60

    # Case B → SAME EIS year: pre-EIS status quo, then Phase 2 directly
    # (Boeing climbs from 40% toward b_eq at the variant's capture speed _bg
    #  — slider, default +4pp/yr — from the shared EIS year).
    if same_eis:
        eis = b_eis_t  # = a_eis_t
        if t < eis:
            return 0.40, 0.60
        yrs_p2 = t - eis + 1
        # Direction depends on whether b_eq is above or below status quo (0.40)
        if b_eq >= 0.40:
            b_sh = min(b_eq, 0.40 + _bg * yrs_p2)
        else:
            b_sh = max(b_eq, 0.40 - _bg * yrs_p2)
        return b_sh, 1.0 - b_sh

    ngsa_leads = xor_a or (both and a_eis_t < b_eis_t)
    fps_leads  = xor_b or (both and b_eis_t < a_eis_t)

    if ngsa_leads:
        if t < a_eis_t:
            return 0.40, 0.60
        # Phase 1: NGSA catches up at 3pp/yr toward 80%
        if xor_a or t < b_eis_t:
            yrs_p1 = t - a_eis_t + 1
            a_sh = min(0.80, 0.60 + 0.03 * yrs_p1)
            return 1.0 - a_sh, a_sh
        # Phase 2: Boeing climbs toward b_eq
        p1_len = b_eis_t - a_eis_t
        a_sh_p1 = min(0.80, 0.60 + 0.03 * p1_len)
        b_sh_p1 = 1.0 - a_sh_p1
        if b_sh_p1 >= b_eq:
            return b_sh_p1, a_sh_p1   # already at/above equilibrium → frozen
        yrs_p2 = t - b_eis_t + 1
        b_sh = min(b_eq, b_sh_p1 + _bg * yrs_p2)
        return b_sh, 1.0 - b_sh

    if fps_leads:
        if t < b_eis_t:
            return 0.40, 0.60
        # Phase 1: fps catches up at the variant's capture speed (_bg) toward 80%
        if xor_b or t < a_eis_t:
            yrs_p1 = t - b_eis_t + 1
            b_sh = min(0.80, 0.40 + _bg * yrs_p1)
            return b_sh, 1.0 - b_sh
        # Phase 2: NGSA climbs toward a_eq (= 1 - b_eq)
        p1_len = a_eis_t - b_eis_t
        b_sh_p1 = min(0.80, 0.40 + _bg * p1_len)
        a_sh_p1 = 1.0 - b_sh_p1
        if a_sh_p1 >= a_eq:
            return b_sh_p1, a_sh_p1   # frozen
        yrs_p2 = t - a_eis_t + 1
        a_sh = min(a_eq, a_sh_p1 + _ar * yrs_p2)
        return 1.0 - a_sh, a_sh

    return 0.40, 0.60  # unreachable


def _nb_driver_labels(b_launches, a_launches, b_eis_t, a_eis_t,
                      b_inc_rate=False, is_7yr=False, active_sabs=0,
                      fps_7yr_pp=5.0, sab_share_pp=5.0,
                      b_gain_pp=4.0, a_recover_pp=4.0,
                      b_reengines=False, a_reengines=False,
                      b_wb_eis_t=None, a_wb_eis_t=None):
    """Return a dict {t_offset: 'label_text'} marking the years where an NB
    share driver activates, expires, or fires for the first time.

    Optional WB params: if a player re-engines, the corresponding WB EIS
    year is added as an informational callout (does not affect NB share but
    helps cross-reference the full strategic timeline).
    """
    out = {}

    def _add(t, txt):
        out[t] = (out.get(t, "") + "\n" + txt).lstrip("\n")

    both = b_launches and a_launches
    xor_b = b_launches and not a_launches
    xor_a = a_launches and not b_launches
    neither = not (b_launches or a_launches)
    same_eis = both and (b_eis_t == a_eis_t)
    ngsa_leads = xor_a or (both and a_eis_t < b_eis_t)
    fps_leads  = xor_b or (both and b_eis_t < a_eis_t)

    # Phase 1 / 2 triggers (case-by-case)
    if neither:
        _add(0, "Case A: status quo 40/60")
    elif same_eis:
        _add(b_eis_t, f"Case B: same EIS → Phase 2 directly\nBoeing +{b_gain_pp:g}pp/yr → 50/50")
    elif fps_leads:
        _add(b_eis_t, f"fps EIS — Phase 1 starts\nBoeing +{b_gain_pp:g}pp/yr cap 80%")
        if both:
            _add(a_eis_t, f"NGSA EIS — Phase 2 starts\nAirbus +{a_recover_pp:g}pp/yr → 50 (or freeze)")
    elif ngsa_leads:
        _add(a_eis_t, "NGSA EIS — Phase 1 starts\nAirbus +3pp/yr cap 80%")
        if both:
            _add(b_eis_t, f"fps EIS — Phase 2 starts\nBoeing +{b_gain_pp:g}pp/yr → 50")

    # Modifier windows
    if b_inc_rate:
        if neither:
            _add(0, f"+ Rate Hike: +5pp Boeing (31 yrs)")
        else:
            # FIXED-CALENDAR: rate hike fires 2032-2036 (t=6..10)
            _add(6, "Rate Hike (+5pp Boeing) — starts 2032")
            _add(11, "Rate Hike — expires 2037")
    if b_launches and is_7yr:
        _add(b_eis_t,      f"+ 7yr Ramp: +{fps_7yr_pp:.0f}pp Boeing (10-yr window)")
        _add(b_eis_t + 10, "7yr Ramp — expires (50/50 steady state)")
    if active_sabs > 0 and b_launches:
        _add(b_eis_t, f"Sabotage starts (−{sab_share_pp:.0f}pp Boeing, 5 yrs)")
        _add(b_eis_t + 5, "Sabotage — expires")

    return out


def _apply_nb_modifiers(b_sh, a_sh, t, b_eis_t, a_eis_t,
                        b_launches, a_launches,
                        b_inc_rate=False,
                        is_7yr=False, fps_7yr_pp=5.0,
                        active_sabs=0, sab_share_pp=5.0):
    """Stack modifiers additively on the unified-rule base share.

    Rules:
      • Rate hike (+5pp Boeing):
          - Case A (neither launches): active ALL 31 years.
          - Otherwise: active in the 5 yrs before min(fps, NGSA) EIS.
      • 7yr ramp (+fps_7yr_pp Boeing): FIRST-MOVER WINDOW — active for
        5 years starting at fps EIS, ONLY if Boeing launches fps via 7yr Solo.
        After 5 yrs the advantage decays (NGSA matures) → returns to 50/50.
      • Sabotage (−sab_share_pp × active_sabs Boeing): from fps EIS onward,
        ONLY if Boeing launches fps (otherwise Naked Espionage Fine fires
        instead, handled separately as a cost lever).
    """
    neither = not (b_launches or a_launches)
    # 737 Rate Hike — FIXED CALENDAR YEARS, EIS-independent.
    # Hike fires in 2032 (t=6). In Case A (neither launches) the +5pp boost
    # persists all 31 yrs (no platform ever displaces the rate program).
    # Otherwise it's active only during the ramp window 2032-2036 (t=6..10);
    # afterwards EIS dynamics take over.
    if b_inc_rate:
        if neither:
            apply_rate = True
        else:
            apply_rate = (6 <= t <= 10)   # 2032..2036
        if apply_rate:
            b_sh = min(1.0, b_sh + 0.05)
            a_sh = max(0.0, 1.0 - b_sh)
    # 7yr ramp bonus — FIRST-MOVER WINDOW ONLY (10 yrs from fps EIS)
    # After 10 yrs the share converges to the baseline 50/50 (NGSA matures,
    # the 7yr first-mover advantage decays). Pre-2047 effect (with default 2037 EIS).
    if b_launches and is_7yr and b_eis_t <= t < b_eis_t + 10:
        b_sh = min(1.0, b_sh + fps_7yr_pp / 100.0)
        a_sh = max(0.0, 1.0 - b_sh)
    # Sabotage — FLAT +sab_share_pp Airbus (regardless of how many active sabotage
    # moves: Bottleneck and Poaching no longer stack), active for 5 years starting
    # at fps EIS. Requires Boeing to actually launch fps; otherwise Naked
    # Espionage Fine fires instead (cost lever, handled separately).
    if active_sabs > 0 and b_launches and b_eis_t <= t < b_eis_t + 5:
        shift = sab_share_pp / 100.0
        b_sh = max(0.0, b_sh - shift)
        a_sh = min(1.0, 1.0 - b_sh)
    return b_sh, a_sh


# ============================================================
# UNIFIED WB SHARE RULE
# Mirrors the per-year logic in evaluate_scenario's WB block. Used by
# the WB Market Share Trajectory chart.
#
# Status quo: Boeing 100/170 (~58.8%), Airbus 70/170 (~41.2%). No
# pre-EIS anticipation. CASES:
#   A. Neither re-engines  → status quo all 31 yrs.
#   B. Both, SAME EIS year → status quo all 31 yrs (no first-mover).
#   C. Both, 787 first     → Boeing +3pp/yr (cap 80%) from 787 EIS
#                            until A350 EIS, then FROZEN.
#   D. Both, A350 first    → Airbus +4pp/yr (cap 60%) from A350 EIS
#                            until 787 EIS, then FROZEN.
#   E. Only 787 re-engines → Boeing +3pp/yr (cap 1 − v_wb_milker,
#                            default 85%) from 787 EIS onward.
#   F. Only A350 re-engines → Airbus +4pp/yr (cap 60% — structural
#                             A350 ceiling) from A350 EIS onward.
# No Phase 2 — unlike NB, the WB rule freezes at the leader's Phase 1
# final value when the follower's EIS arrives.
# ============================================================
def _wb_gain_b():
    """Lone-refresh 787 WB share-capture speed (fraction/yr).

    Slider key 'af_wb_b_pp' (pp/yr, default 3.0 -> 0.03/yr). Also the 787's
    leader-phase speed in staggered both-re-engine (Case C)."""
    try:
        return float(st.session_state.get('af_wb_b_pp', 3.0)) / 100.0
    except Exception:
        return 0.03


def _wb_gain_a():
    """Lone-refresh A350 WB share-capture speed (fraction/yr).

    Slider key 'af_wb_a_pp' (pp/yr, default 4.0 -> 0.04/yr). Also the A350's
    leader-phase speed in staggered both-re-engine (Case D)."""
    try:
        return float(st.session_state.get('af_wb_a_pp', 4.0)) / 100.0
    except Exception:
        return 0.04


def _compute_wb_share_unified(t, b_reengines, a_reengines, b_eis_t, a_eis_t,
                               wb_milker_share=0.15):
    """Return (b_share, a_share) WB at year t. wb_milker_share is in
    fraction form (0.15 default → cap at 1−0.15 = 85% in Case E)."""
    sq_b, sq_a = 100/170, 70/170  # status quo
    both = b_reengines and a_reengines
    xor_b = b_reengines and not a_reengines
    xor_a = a_reengines and not b_reengines
    neither = not (b_reengines or a_reengines)
    same_eis = both and (b_eis_t == a_eis_t)

    if neither or same_eis:
        return sq_b, sq_a

    if xor_b:
        # Case E
        if t < b_eis_t:
            return sq_b, sq_a
        yrs_in = t - b_eis_t + 1
        b_sh = min(1.0 - wb_milker_share, sq_b + _wb_gain_b() * yrs_in)
        return b_sh, 1.0 - b_sh

    if xor_a:
        # Case F
        if t < a_eis_t:
            return sq_b, sq_a
        yrs_in = t - a_eis_t + 1
        a_sh = min(0.60, sq_a + _wb_gain_a() * yrs_in)
        return 1.0 - a_sh, a_sh

    # Both re-engine, different EIS years
    if b_eis_t < a_eis_t:
        # Case C: 787 leads
        if t < b_eis_t:
            return sq_b, sq_a
        catch_t = min(t, a_eis_t - 1)
        yrs_in = catch_t - b_eis_t + 1
        b_sh = min(0.80, sq_b + _wb_gain_b() * yrs_in)
        return b_sh, 1.0 - b_sh
    else:
        # Case D: A350 leads
        if t < a_eis_t:
            return sq_b, sq_a
        catch_t = min(t, b_eis_t - 1)
        yrs_in = catch_t - a_eis_t + 1
        a_sh = min(0.60, sq_a + _wb_gain_a() * yrs_in)
        return 1.0 - a_sh, a_sh

    return sq_b, sq_a  # unreachable


def _wb_driver_labels(b_reengines, a_reengines, b_eis_t, a_eis_t,
                      wb_milker_share=0.15):
    """Return {t_offset: 'label_text'} for WB share trigger years.

    Only annotates events that actually fire in the chosen state:
      - Case A (both milk): a single status-quo note at t=0; no EIS markers
        (787 and A350 EIS years have no effect when neither re-engines).
      - Case B (same EIS): one marker at the shared year.
      - Cases C/D (both re-engine, ordered): both EIS markers.
      - Cases E/F (one re-engines): only that player's EIS marker.
    """
    out = {}

    def _add(t, txt):
        out[t] = (out.get(t, "") + "\n" + txt).lstrip("\n")

    both = b_reengines and a_reengines
    xor_b = b_reengines and not a_reengines
    xor_a = a_reengines and not b_reengines
    neither = not (b_reengines or a_reengines)
    same_eis = both and (b_eis_t == a_eis_t)
    cap_e = (1.0 - wb_milker_share) * 100.0
    gain_b = _wb_gain_b() * 100.0
    gain_a = _wb_gain_a() * 100.0

    if neither:
        _add(0, "Case A: status quo 100/170 vs 70/170\n(~58.8 / 41.2%) all 31 yrs")
    elif same_eis:
        _add(b_eis_t, "Case B: same EIS year\nBoth re-engine simultaneously\nStatus quo retained (no first-mover)")
    elif xor_b:
        _add(b_eis_t, f"787 EIS — Case E\nBoeing +{gain_b:.1f}pp/yr toward {cap_e:.0f}% (1−milker)")
    elif xor_a:
        _add(a_eis_t, f"A350 EIS — Case F\nAirbus +{gain_a:.1f}pp/yr cap 60%")
    elif both and b_eis_t < a_eis_t:
        _add(b_eis_t, f"787 EIS — Case C Phase 1 starts\nBoeing +{gain_b:.1f}pp/yr cap 80%")
        _add(a_eis_t, "A350 EIS — Phase 1 ends\nShares FROZEN at this level")
    elif both and a_eis_t < b_eis_t:
        _add(a_eis_t, f"A350 EIS — Case D Phase 1 starts\nAirbus +{gain_a:.1f}pp/yr cap 60%")
        _add(b_eis_t, "787 EIS — Phase 1 ends\nShares FROZEN at this level")

    return out



# ============================================================
# CROSS-BOARD LINK — ENGINE SUPPLIER SELECTION
# Links the Airframer board to the Engine board per the supplier
# matrix.  The user picks a supplier for Boeing's fps and Airbus's
# NGSA on the Airframer sidebar; the Engine board then auto-updates
# its post-2037 NB share sliders and PW lock move accordingly.
# ============================================================
SUPPLIER_OPTIONS = [
    "RR",                       # 1
    "PW",                       # 2
    "CFM (Ducted)",             # 3
    "RR & PW (JV)",             # 4
    "RR and CFM",               # 5  — dual source
    "PW and CFM",               # 6  — dual source
    "RR, PW, and CFM (all 3)",  # 7  — triple source (default for NB)
]
SUPPLIER_CODE = {opt: i + 1 for i, opt in enumerate(SUPPLIER_OPTIONS)}

# Forbidden (Boeing_code, Airbus_code) pairs — the X cells in the matrix.
# Code 7 (triple source) is permitted with anything: when both Boeing and
# Airbus include all 3 makers, each maker simply gets work from both — no
# conflict to forbid.
FORBIDDEN_PAIRS = {
    (1, 1), (1, 4),
    (2, 2), (2, 4),
    (3, 3),
    (4, 1), (4, 2), (4, 4),
    (5, 5),
    (6, 6),
}

def supplier_engines(code):
    """Return the set of engine providers for a supplier code (subset of {RR,PW,CFM})."""
    return {
        1: {"RR"},
        2: {"PW"},
        3: {"CFM"},
        4: {"RR", "PW"},          # JV
        5: {"RR", "CFM"},         # dual source
        6: {"PW", "CFM"},         # dual source
        7: {"RR", "PW", "CFM"},   # triple source — all 3 makers split the slot equally
    }[code]

def is_jv(code):
    return code == 4

def derive_nb_engine_shares(b_code, a_code, boeing_share_pct=50.0):
    """
    Allocate post-2037 NB engine market by airframer × supplier choice.

    The Boeing slot of the new NB market is `boeing_share_pct` (0-100); Airbus
    gets the complement. Within each airframer slot, a single supplier takes
    100% of that slot, and a dual / JV supplier splits the slot 50/50.

    Returns (rr_pct, pw_pct, cfm_pct), each 0-100, summing to 100.
    """
    boeing_share_pct = max(0.0, min(100.0, float(boeing_share_pct)))
    airbus_share_pct = 100.0 - boeing_share_pct
    shares = {"RR": 0.0, "PW": 0.0, "CFM": 0.0}
    for code, slot in ((b_code, boeing_share_pct), (a_code, airbus_share_pct)):
        engines = supplier_engines(code)
        per = slot / len(engines)
        for e in engines:
            shares[e] += per
    return shares["RR"], shares["PW"], shares["CFM"]

# Initialise session-state defaults to triple-source (code 7) for both —
# all 3 engine makers (RR, PW, CFM) on each airframer's NB program.
if "_b_supplier" not in st.session_state:
    st.session_state["_b_supplier"] = "RR, PW, and CFM (all 3)"
if "_a_supplier" not in st.session_state:
    st.session_state["_a_supplier"] = "PW and CFM"
# Boeing/Airbus market-share split for post-2037 "both launch new NB" state
if "_boeing_share_both" not in st.session_state:
    st.session_state["_boeing_share_both"] = 50

# Seed the change-detection trio with the initial defaults so the engine
# board's auto-sync of f_cfm_nb / f_pw_nb / f_rr_nb does NOT fire on the
# very first render — preserves the custom CFM=0 / PW=50 / RR=50 starting
# shares specified as initial conditions. The user can still trigger a
# resync by changing supplier or share, then the matrix-derived values
# overwrite f_*_nb as before.
if "_last_b_supp_seen" not in st.session_state:
    st.session_state["_last_b_supp_seen"] = "RR, PW, and CFM (all 3)"
if "_last_a_supp_seen" not in st.session_state:
    st.session_state["_last_a_supp_seen"] = "RR, PW, and CFM (all 3)"
if "_last_boeing_share_seen" not in st.session_state:
    st.session_state["_last_boeing_share_seen"] = 50

# ============================================================
# BOARD 1 — AIRFRAMER (original Game_Board.py, untouched)
# ============================================================
def run_airframer_board():

    # ============================================================
    # 1. PAGE CONFIGURATION & STRICT DARK THEME  (engine-board look)
    # ============================================================

    st.markdown("""
    <style>
    /* ── Strict Dark Theme ── */
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }

    /* ── Gameboard Table ── */
    .board-container { width: 100%; overflow: visible !important; margin-top: 20px; margin-bottom: 50px; background: #050505; border: 2px solid #333; border-radius: 8px; padding: 10px; overflow-x: auto; }
    .board-table { border-collapse: separate; border-spacing: 3px; font-family: 'Courier New', Courier, monospace; background-color: #000; width: 100%; min-width: 1400px; }

    .board-th-col { vertical-align: top; background-color: #001a0d; border: 2px solid #ffffff; border-bottom: 3px solid #32CD32; outline: 1px solid #ffffff; outline-offset: 0; padding: 8px; text-align: center; font-size: 13px; color: #32CD32; position: sticky; top: 0; z-index: 10; }
    .board-th-row { vertical-align: top; background-color: #001a26; border: 2px solid #ffffff; border-right: 3px solid #00BFFF; border-bottom: 3px solid #00BFFF; outline: 1px solid #ffffff; outline-offset: 0; padding: 8px; text-align: left; font-size: 13px; color: #00BFFF; position: sticky; left: 0; z-index: 10; white-space: nowrap; }

    .board-td { background-color: #0a0a0a; border: 1px solid #222; padding: 3px 6px; text-align: center; vertical-align: middle; font-size: 13px; transition: all 0.2s ease-in-out; cursor: crosshair; position: relative; }
    .board-td:hover { background-color: #1f1f1f; transform: scale(1.05); z-index: 50; border: 1px solid #777; }

    /* ── Nash Equilibrium Styles ── */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0.7); }
        70% { box-shadow: 0 0 10px 5px rgba(60, 179, 113, 0); }
        100% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0); }
    }
    .nash-pure { border: 2px solid #3cb371 !important; background-color: #002b11 !important; font-weight: bold; animation: pulse-green 2s infinite; }
    .nash-near { border: 2px dashed #FFD700 !important; background-color: #2b2400 !important; }

    /* ── Hover Tooltip ── */
    .board-td .receipt-tooltip { visibility: hidden; width: 420px; background-color: #111; color: #fff; text-align: left; border: 1px solid #555; border-radius: 6px; padding: 12px; position: absolute; z-index: 999; bottom: 120%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.2s; box-shadow: 0px 10px 20px rgba(0,0,0,0.9); font-family: monospace; font-size: 11px; line-height: 1.4; pointer-events: none; }
    .board-td .receipt-tooltip::after { content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px; border-width: 5px; border-style: solid; border-color: #555 transparent transparent transparent; }
    .board-td:hover .receipt-tooltip { visibility: visible; opacity: 1; }

    /* ── Math Receipt Boxes ── */
    .nash-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 20px; font-family: monospace; }
    .nash-title { color: #58a6ff; font-size: 16px; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 15px; }
    .nash-title-pure { color: #3cb371; font-size: 16px; font-weight: bold; border-bottom: 1px solid #3cb371; padding-bottom: 10px; margin-bottom: 15px; }
    .nash-title-near { color: #FFD700; font-size: 16px; font-weight: bold; border-bottom: 1px solid #FFD700; padding-bottom: 10px; margin-bottom: 15px; }
    .delta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .delta-col { background: #000; padding: 15px; border-radius: 4px; border-left: 3px solid; }

    /* ── Player Colours ── */
    .player-a { color: #00BFFF; font-weight: bold; }   /* Airbus */
    .player-b { color: #32CD32; font-weight: bold; }   /* Boeing */
    .col-a { border-color: #00BFFF; }
    .col-b { border-color: #32CD32; }

    /* ── Move Lists ── */
    .move-list-box { background: #111; padding: 15px; border-radius: 6px; border: 1px solid #333; height: 100%; }
    .move-item { font-size: 11px; color: #ccc; margin-bottom: 4px; font-family: monospace; }

    /* ── Breakdown Tables ── */
    .math-breakdown-table { width: 100%; font-size: 12px; color: #bbb; margin-bottom: 12px; border-collapse: collapse; }
    .math-breakdown-table td { padding: 6px 4px; border-bottom: 1px solid #222; }
    .math-breakdown-table .val { text-align: right; color: #fff; font-weight: bold; }

    /* ── Price Table ── */
    .price-tbl { width: 100%; border-collapse: collapse; font-size: 12px; color: #ccc; margin: 10px 0 20px 0; }
    .price-tbl th { background: #111; color: #58a6ff; padding: 8px; text-align: left; border-bottom: 2px solid #30363d; }
    .price-tbl td { padding: 6px 8px; border-bottom: 1px solid #222; }

    /* ── Value helpers ── */
    .positive-val { color: #3cb371; font-weight: bold; }
    .negative-val { color: #ff4c4c; font-weight: bold; }
    .math-highlight { color: #FFD700; font-family: monospace; font-size: 14px; background: #1a1a1a; padding: 3px 6px; border-radius: 4px; }
    .math-subtext { color: #888888; font-family: monospace; font-size: 11px; display: block; margin-top: 4px; padding-left: 10px; border-left: 2px solid #444; }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # 2. STRATEGY GROUPS VIA EXCLUSIVITY LETTERS  (UNCHANGED)
    # ============================================================
    Airbus_Exclusivity_Groups = {
        'A':  ["Launch_NGSA", "Milk_A320neo"],
        'B':  ["Sabotage_Bottleneck", "No_Bottleneck"],
        'C':  ["Sabotage_Poaching", "No_Poaching"],
        'WB': ["Re_engine_A350", "Milk_A350"]
    }

    Boeing_Exclusivity_Groups = {
        'A':  ["Launch_fps_7yr_Solo", "Launch_fps_10yr_Solo", "Launch_fps_via_Embraer", "Milk_737MAX"],
        'B':  ["Increase_737_Rate", "No_Rate_Increase"],
        'WB': ["Re_engine_787", "Milk_787"]
    }

    A_moves = list(itertools.product(*Airbus_Exclusivity_Groups.values()))
    B_moves = list(itertools.product(*Boeing_Exclusivity_Groups.values()))

    # --- HARDCODED MARKET ASSUMPTIONS (UNCHANGED) ---
    TIMELINE_YRS = 31   # 2026 to 2056 — outer timeline; per-program windows may extend it
    NPV_POST_EIS_YRS = 20  # Per-program: pre-EIS legacy + 20 yrs post-EIS (inclusive of EIS year)
    NB_PER_YR    = 2000
    WB_PER_YR    = 170

    # Aircraft prices (PRICE_737, PRICE_fps, PRICE_A320, PRICE_NGSA, PRICE_WB)
    # are now defined in the sidebar expander ✈️ Aircraft Prices.

    WACC_B = 0.105
    WACC_A = 0.080

    def get_pv_stream(nominal_total, start_t, end_t, wacc):
        if nominal_total == 0: return 0.0
        years = end_t - start_t + 1
        annual_cf = nominal_total / years
        return sum([annual_cf / ((1 + wacc)**t) for t in range(start_t, end_t + 1)])

    # ============================================================
    # 3. THE CONTROL DESK (SIDEBAR) — UNCHANGED LOGIC
    # ============================================================
    st.sidebar.markdown("### ⚙️ Airframer Market Parameters")

    v_tolerance = st.sidebar.slider('ε-Nash Tolerance Yield (%)', 0.0, 10.0, value=2.0, step=0.5, key='af_eps_tol')
    v_alpha     = st.sidebar.slider('True Cost Penalty — Market Punishment (α)', 0.0, 1.5, value=0.3, step=0.1, key='af_alpha',
                                    help="ΔDebtPenalty = Debt × α × (Debt/EV)². Applied as marginal penalty from new debt load.")

    with st.sidebar.expander("🎯 Airplane Market Share (fps vs NGSA)", expanded=False):
        st.caption("2037+ NB market split — applied in every state where both "
                   "airframers launch a new product (fps and NGSA).")
        boeing_share_pct = st.slider(
            "Boeing fps share of post-2037 NB market (%)",
            0, 100,
            50,
            key="_boeing_share_both",
            help="Sets Boeing's slice of the 2037+ NB market in every state "
                 "where both Boeing (fps) and Airbus (NGSA) launch a new product. "
                 "Airbus gets the complement. Has no effect in milker states "
                 "or pre-2037.",
        )
        st.caption(f"→ Boeing fps: {boeing_share_pct}%   |   "
                   f"Airbus NGSA: {100 - boeing_share_pct}%")

        st.divider()
        # Migration: old default was 7.0, new default is 5.0. If the persisted
        # value is still at the old default (i.e. user never touched it),
        # auto-update so the slider reflects the new convention.
        if st.session_state.get('af_fps_7yr_adv') == 7.0:
            st.session_state['af_fps_7yr_adv'] = 5.0
        v_fps_7yr_advantage = st.slider(
            "fps 7-yr ramp NB share advantage over 10-yr (pp)",
            0.0, 15.0, value=5.0, step=0.5,
            key="af_fps_7yr_adv",
            help="Additive boost to Boeing's post-2037 NB market share when Boeing "
                 "selects the 'Launch fps with 7-year ramp-up' move. Reflects the "
                 "first-mover advantage of the faster development path: customers "
                 "lock in earlier orders, supply-chain commitments harden faster, "
                 "and Airbus's NGSA arrives into a more captured market.\n\n"
                 "Math: applied additively to b_eis_nb_sh whenever Boeing launches "
                 "fps via the 7yr Solo variant — fires in BOTH the 'both launch' "
                 "case AND the 'Boeing launches, Airbus milks' case. The 10yr Solo "
                 "and Via Embraer variants are unaffected. Airbus gets the "
                 "complement (1 - new boeing share). Sabotage shifts apply on top "
                 "of this bonus."
        )

    with st.sidebar.expander("🐢 fps 10-yr Ramp — Share-Shift Speeds", expanded=False):
        st.caption("Speeds (pp/yr) at which the NB market share moves when Boeing "
                   "launches fps via the 10-yr Solo or via-Embraer path. Defaults "
                   "(4.0 / 4.0) reproduce the original fixed +4pp/yr rule.")
        v_ramp10_b_pp = st.slider(
            "Boeing share capture (pp/yr) — 10-yr ramp",
            0.5, 10.0, 4.0, 0.5, key="af_ramp10_b_pp",
            help="How fast Boeing's NB share moves once fps (10-yr Solo or via "
                 "Embraer) is in service. Fires in: Phase 1 when fps leads "
                 "(climb from 40%, cap 80%); the same-EIS climb toward the "
                 "balance point; and Phase 2 when fps follows NGSA (climb back "
                 "toward balance). Does NOT apply to the 7-yr ramp variant.")
        v_ramp10_a_pp = st.slider(
            "Airbus Phase-2 recovery (pp/yr) — vs 10-yr ramp",
            0.5, 10.0, 4.0, 0.5, key="af_ramp10_a_pp",
            help="How fast Airbus claws back share once NGSA enters service "
                 "AFTER a leading 10-yr/Embraer fps (Phase 2 of the fps-leads "
                 "case, climbing toward the 50/50 balance point; freezes if "
                 "Boeing never crossed 50% in Phase 1). NGSA's own Phase-1 "
                 "capture vs a milking Boeing stays fixed at +3pp/yr.")

    with st.sidebar.expander("🐇 fps 7-yr Ramp — Share-Shift Speeds", expanded=False):
        st.caption("Speeds (pp/yr) at which the NB market share moves when Boeing "
                   "launches fps via the 7-yr Solo crash program. Defaults "
                   "(4.0 / 4.0) reproduce the original fixed +4pp/yr rule. The "
                   "+5pp first-mover ramp bonus is separate (Airplane Market "
                   "Share expander) and stacks on top.")
        v_ramp7_b_pp = st.slider(
            "Boeing share capture (pp/yr) — 7-yr ramp",
            0.5, 10.0, 4.0, 0.5, key="af_ramp7_b_pp",
            help="How fast Boeing's NB share moves once fps (7-yr Solo) is in "
                 "service. Fires in: Phase 1 when fps leads (climb from 40%, "
                 "cap 80%); the same-EIS climb toward the balance point; and "
                 "Phase 2 when fps follows NGSA. A faster physical ramp can "
                 "justify a higher capture speed than the 10-yr path.")
        v_ramp7_a_pp = st.slider(
            "Airbus Phase-2 recovery (pp/yr) — vs 7-yr ramp",
            0.5, 10.0, 4.0, 0.5, key="af_ramp7_a_pp",
            help="How fast Airbus claws back share once NGSA enters service "
                 "AFTER a leading 7-yr fps. A lower value models a hardened "
                 "first-mover position (orders locked in before NGSA matures).")

    with st.sidebar.expander("🔌 Engine Supplier Selection", expanded=False):
        st.caption("Pick the engine supplier for Boeing's fps and Airbus's NGSA. "
                   "Forbidden combinations (X) are auto-blocked. Selection "
                   "auto-updates the Engine Board.")

        # Boeing first
        cur_b = st.session_state.get("_b_supplier", "RR")
        if cur_b not in SUPPLIER_OPTIONS:
            cur_b = "RR"
            st.session_state["_b_supplier"] = cur_b
        b_supp = st.selectbox(
            "Boeing fps Supplier",
            SUPPLIER_OPTIONS,
            index=SUPPLIER_OPTIONS.index(cur_b),
            key="_b_supplier",
        )
        b_code = SUPPLIER_CODE[b_supp]

        # Airbus options dynamically filtered to exclude X-combinations
        valid_a_options = [opt for opt in SUPPLIER_OPTIONS
                           if (b_code, SUPPLIER_CODE[opt]) not in FORBIDDEN_PAIRS]

        # If previous value is now invalid, snap to first valid (BEFORE widget renders)
        cur_a = st.session_state.get("_a_supplier", valid_a_options[0])
        if cur_a not in valid_a_options:
            cur_a = valid_a_options[0]
            st.session_state["_a_supplier"] = cur_a

        a_supp = st.selectbox(
            "Airbus NGSA Supplier",
            valid_a_options,
            index=valid_a_options.index(cur_a),
            key="_a_supplier",
        )
        a_code = SUPPLIER_CODE[a_supp]

        excluded = [opt for opt in SUPPLIER_OPTIONS if opt not in valid_a_options]
        if excluded:
            st.caption(f"⛔ Excluded for Airbus (X with Boeing's {b_supp}): "
                       + ", ".join(excluded))

        # Derived NB engine shares preview (uses current airplane share slider value)
        rr_pct, pw_pct, cfm_pct = derive_nb_engine_shares(b_code, a_code, boeing_share_pct)
        st.markdown(
            f"<div style='background:#0d1117;border-left:3px solid #58a6ff;"
            f"padding:8px;font-family:monospace;font-size:11px;color:#ddd;margin-top:8px;'>"
            f"<b>Selection Code:</b> ({b_code},{a_code})<br/>"
            f"<span class='player-b'>Boeing → {b_supp}</span><br/>"
            f"<span class='player-a'>Airbus → {a_supp}</span><br/>"
            f"<hr style='border:1px solid #222;margin:6px 0;'>"
            f"<b>Derived Post-2037 NB Engine Shares:</b><br/>"
            f"&nbsp;&nbsp;RR: {rr_pct:.0f}% | PW: {pw_pct:.0f}% | CFM: {cfm_pct:.0f}%"
            f"</div>",
            unsafe_allow_html=True,
        )

    with st.sidebar.expander("📊 Balance Sheets ($B)", expanded=False):
        v_ev_airbus   = st.number_input('Airbus EV ($B)',   value=150.0, step=5.0, key='af_ev_airbus')
        v_debt_airbus = st.number_input('Airbus Debt ($B)', value=10.0, step=5.0, key='af_debt_airbus')
        st.divider()
        v_ev_boeing   = st.number_input('Boeing EV ($B)',   value=130.0, step=5.0, key='af_ev_boeing')
        v_debt_boeing = st.number_input('Boeing Debt ($B)', value=45.0, step=5.0, key='af_debt_boeing')

    st.sidebar.caption("Build 2026-07-15b · adds WB re-engine capture-speed sliders")
    with st.sidebar.expander("✈️ Aircraft Prices ($M per a/c)", expanded=False):
        st.caption("Narrowbody — Current Generation")
        PRICE_737  = st.number_input('737 MAX ($M)',  value=48.0, min_value=20.0, max_value=100.0, step=1.0, key="af_price_737") / 1000.0
        PRICE_A320 = st.number_input('A320neo ($M)',  value=52.0, min_value=20.0, max_value=100.0, step=1.0, key="af_price_a320") / 1000.0
        st.divider()
        st.caption("Narrowbody — Next Generation (EIS 2037)")
        PRICE_fps  = st.number_input('Boeing fps ($M)',  value=55.0, min_value=30.0, max_value=120.0, step=1.0, key="af_price_fps") / 1000.0
        PRICE_NGSA = st.number_input('Airbus NGSA ($M)',  value=55.0, min_value=30.0, max_value=120.0, step=1.0, key="af_price_ngsa") / 1000.0
        st.divider()
        st.caption("Widebody (787 / A350 class)")
        PRICE_WB   = st.number_input('WB price ($M)', value=180.0, min_value=80.0, max_value=350.0, step=5.0, key="af_price_wb") / 1000.0

    with st.sidebar.expander("⚙️ Operational Margins (%)", expanded=False):
        st.caption("Airbus")
        v_margin_a320  = st.slider('A320neo Margin (%)', 0.0, 30.0, 13.14, key="af_m_a320") / 100.0
        v_margin_angsa = st.slider('NGSA Margin (%)',    0.0, 30.0, 26.28, key="af_m_ngsa") / 100.0
        v_margin_a350  = st.slider('A350 WB Margin (%) — status quo',  0.0, 40.0, 4.95, key="af_m_a350",
            help="Applies in years before A350 re-engines (or if A350 never re-engines).") / 100.0
        v_margin_a350_alone = st.slider('A350 WB Margin (%) with NO 787 Re-engine', 0.0, 40.0, 10.76, key="af_m_a350_alone",
            help="Applies from A350 re-engine EIS onward, when A350 re-engines but 787 does not "
                 "(Airbus captures share at premium pricing → typically a margin uplift vs. status quo).") / 100.0
        v_margin_a350_both  = st.slider('A350 WB Margin (%) WITH 787 Re-engine',    0.0, 40.0, 6.47, key="af_m_a350_both",
            help="Applies from A350 re-engine EIS onward, when both A350 and 787 re-engine "
                 "(competitive pricing pressure → margin closer to status quo).") / 100.0
        st.divider()
        st.caption("Boeing")
        v_margin_737   = st.slider('737 Margin (%)',     0.0, 30.0, 8.0, key="af_m_737") / 100.0
        v_margin_fps   = st.slider('fps Margin (%)',     0.0, 30.0, 25.64, key="af_m_fps") / 100.0
        v_margin_787   = st.slider('787 WB Margin (%) — status quo',  0.0, 40.0, 20.0, key="af_m_787",
            help="Applies in years before 787 re-engines (or if 787 never re-engines).") / 100.0
        v_margin_787_alone = st.slider('787 WB Margin (%) with NO A350 Re-engine', 0.0, 40.0, 25.21, key="af_m_787_alone",
            help="Applies from 787 re-engine EIS onward, when 787 re-engines but A350 does not "
                 "(Boeing captures share at premium pricing → typically a margin uplift vs. status quo).") / 100.0
        v_margin_787_both  = st.slider('787 WB Margin (%) WITH A350 Re-engine',    0.0, 40.0, 15.77, key="af_m_787_both",
            help="Applies from 787 re-engine EIS onward, when both 787 and A350 re-engine "
                 "(competitive pricing pressure → margin closer to status quo).") / 100.0

    with st.sidebar.expander("⚔️ Nominal Tot Invest (CAPEX + NRE) ($B)", expanded=False):
        st.caption("Narrowbody launch programs")
        v_capex_fps_7yr       = st.slider('fps 7yr Solo Tot Invest',       20.0, 100.0, 60.69, key="af_cx_fps7")
        v_capex_fps_10yr      = st.slider('fps 10yr Solo Tot Invest',      20.0, 100.0, 55.25, key="af_cx_fps10")
        v_capex_fps_emb       = st.slider('fps via Emb Tot Invest',        20.0, 100.0, 100.00, key="af_cx_fpsemb")
        v_capex_angsa         = st.slider('NGSA Build Tot Invest',         20.0, 100.0, 30.07, key="af_cx_ngsa")
        st.divider()
        st.caption("Widebody re-engine programs")
        v_capex_787_reengine  = st.slider('Boeing 787 Re-engine Tot Invest', 5.0, 40.0, 5.00, key="af_cx_787re")
        v_capex_a350_reengine = st.slider('Airbus A350 Re-engine Tot Invest', 5.0, 40.0, 5.00, key="af_cx_a350re")
        st.divider()
        st.caption("Production-rate ramp programs")
        v_capex_737_rate_hike = st.slider('Boeing 737 Rate Hike Tot Invest', 0.0, 10.0, 2.94, key="af_cx_737rate",
            help="One-time PV charge for ramping 737 production (new tooling, supply chain expansion). "
                 "Booked at a fixed 2032 calendar date (t=6, decoupled from any EIS), discounted to 2026 at WACC_B.")

    with st.sidebar.expander("📅 WB EISs", expanded=False):
        st.caption("Entry-into-service year for each WB re-engine program. "
                   "Drives both the WB share switch year and the CAPEX spread window "
                   "(6 yrs ending at EIS). Engine board uses min(787, A350) for "
                   "its WB EIS so its WB share dynamics stay synced with the earlier "
                   "WB platform refresh.")
        _wb_rules_help = (
            "WB MARKET SHARE TRANSITION RULES\n\n"
            "Status quo persists until the relevant EIS year (no pre-EIS anticipation). "
            "Starting status quo: Boeing 58.8% / Airbus 41.2%.\n\n"
            "• Neither re-engines → status quo all 31 yrs.\n\n"
            "• Both re-engine, SAME year → status quo all 31 yrs (simultaneous launches cancel any first-mover advantage).\n\n"
            "• Both re-engine, 787 first → from 787 EIS until A350 EIS, Boeing gains at the 787 capture slider (default +3pp/yr) (cap 80%). From A350 EIS onward, share frozen at achieved level.\n\n"
            "• Both re-engine, A350 first → from A350 EIS until 787 EIS, Airbus gains at the A350 capture slider (default +4pp/yr) (cap 60%). From 787 EIS onward, share frozen at achieved level.\n\n"
            "• Only 787 re-engines (Airbus milks A350) → from 787 EIS onward, Boeing gains at the 787 capture slider (default +3pp/yr), cap = 1 − Milker Share (default 85%).\n\n"
            "• Only A350 re-engines (Boeing milks 787) → from A350 EIS onward, Airbus gains at the A350 capture slider (default +4pp/yr), cap 60% (structural A350 ceiling).\n\n"
            "CAPEX is spread over 6 years ending at each player's EIS, then PV-discounted."
        )
        v_787_eis_year  = st.slider('787 Re-engine EIS year',  2031, 2047, 2041, key="af_787_eis",
                                    help=_wb_rules_help)
        v_a350_eis_year = st.slider('A350 Re-engine EIS year', 2031, 2047, 2035, key="af_a350_eis",
                                    help=_wb_rules_help)

    with st.sidebar.expander("📅 NB EISs", expanded=False):
        st.caption("Entry-into-service year for each new NB platform. "
                   "Drives the NB share switch year, the CAPEX spread window "
                   "(9 yrs ending the year before EIS), and the engine board's "
                   "NB_EIS_T (= min(fps, NGSA)).")
        _nb_rules_help = (
            "NB MARKET SHARE TRANSITION RULES (v2)\n\n"
            "Status quo persists until the relevant EIS year (no pre-EIS anticipation). "
            "Starting status quo: Boeing 40% / Airbus 60%.\n\n"
            "• Neither launches → 40/60 for all 31 yrs (or 45/55 if 737 Rate Hike active).\n\n"
            "• Both launch, SAME EIS year → 40/60 until EIS, then Phase 2 fires directly: "
            "Boeing climbs +4pp/yr toward 50% balance (limiting case of Phase 1 length = 0).\n\n"
            "• NGSA leads (NGSA EIS before fps EIS, OR Boeing milks 737):\n"
            "   Phase 1 (NGSA EIS onward): Airbus +3pp/yr, cap 80%.\n"
            "   Phase 2 (fps EIS, only if Boeing also launches): Boeing climbs +4pp/yr to 50/50 balance.\n\n"
            "• fps leads (fps EIS before NGSA EIS, OR Airbus milks A320):\n"
            "   Phase 1 (fps EIS onward): Boeing +4pp/yr, cap 80%.\n"
            "   Phase 2 (NGSA EIS, only if Airbus also launches): Airbus climbs +4pp/yr to 50/50.\n"
            "   Edge case: if Phase 1 was short (≤2 yrs) so fps never crossed 50%, "
            "shares FREEZE at Phase 1 final value when Phase 2 starts.\n\n"
            "MODIFIERS — stack additively on top of catch-up:\n"
            "• 737 Rate Hike: +5pp Boeing. All 31 yrs in Case A (neither). "
            "Otherwise active 2032-2036 only (fixed-calendar, EIS-independent).\n"
            "• fps 7yr Ramp Bonus: +7pp Boeing from fps EIS onward (Launch fps 7yr Solo only).\n"
            "• Sabotage (Bottleneck / Poaching): FLAT −5pp Boeing (no stacking — 1 or 2 moves same effect), "
            "for 5 yrs from fps EIS (the 'fps launch disruption window'). After 5 yrs the shift expires. "
            "Only fires when Boeing launches fps; otherwise Naked Espionage Fine.\n\n"
            "CAPEX (Option B): single lump at each program's EIS year, PV-discounted to 2026.\n\n"
            "NOTE: the +4pp/yr Boeing-capture and Airbus Phase-2 recovery speeds above are "
            "DEFAULTS — both are slider-controlled per fps ramp variant (see the 🐢 10-yr "
            "and 🐇 7-yr Ramp expanders). NGSA's Phase-1 +3pp/yr is fixed."
        )
        v_fps_eis_year  = st.slider('fps EIS year',  2037, 2047, 2037, key="af_fps_eis",
                                    help=_nb_rules_help)
        v_ngsa_eis_year = st.slider('NGSA EIS year', 2037, 2047, 2037, key="af_ngsa_eis",
                                    help=_nb_rules_help)

    with st.sidebar.expander("💥 Market Shifts & Sabotage", expanded=False):
        v_nb_milker_share = st.slider('NB Obsolescence (Milker Share %)', 20.0, 40.0, 30.0, key='af_nb_milker',
            help="When ONE airframer launches a new NB and the other milks, this is the share the milker keeps "
                 "(launcher gets 1 − value). Mirrors the 'anticipation effect': customers shift orders the moment a "
                 "rival announces a launch.\n\n"
                 "Math: applied across ALL 31 years (2026–2056), not just post-EIS. Default 30% means the milker keeps "
                 "30% of NB sales for the full timeline; the launcher takes 70%. At default 30%: ~50% NPV cut for the "
                 "milker vs status quo. At 20%: ~67% NPV cut. Symmetric states (both launch / both milk) ignore this "
                 "slider and use the standard 40/60 status quo or the user-set Boeing-share value."
        ) / 100.0
        v_wb_milker_share = st.slider('WB Obsolescence (Milker Share %)',  5.0, 40.0, 15.0, key='af_wb_milker',
            help="Same mechanic as NB obsolescence, but applied to the WB market when one airframer re-engines and the "
                 "other milks. The milker keeps this share, the re-engineer takes 1 − value.\n\n"
                 "Math: applied across all 31 years. Default 15% reflects the 787's structural WB dominance — even when "
                 "Airbus re-engines A350, Boeing's installed-base loyalty preserves ~15% of WB orders. Symmetric states "
                 "(both re-engine / neither re-engines) ignore this slider and use the 100/170 vs 70/170 baseline split "
                 "for years 0–8 then the EIS shares thereafter."
        ) / 100.0
        v_sabotage_share  = st.slider('Sabotage (delay_fps) Share Shift — FLAT (%)', 0.0, 15.0, 5.0, key='af_sab_share',
            help="NB share Airbus gains from sabotaging Boeing's fps. FLAT magnitude — applies whether Airbus plays "
                 "1 sabotage move (Bottleneck OR Poaching) or both. Bottleneck and Poaching no longer stack.\n\n"
                 "DURATION: applies for 5 years only, starting at fps EIS (the 'fps launch disruption window'). "
                 "After the 5 yrs the shift expires and Boeing's share recovers per the unified rule.\n\n"
                 "Math: from year fps_EIS to fps_EIS+4, b_sh −= value/100, a_sh += value/100. "
                 "CRITICAL: this only fires if Boeing also launches fps — sabotage against a Boeing milker is "
                 "'naked' and triggers the regulatory fine instead."
        )
        v_sabotage_cost   = st.slider('Sabotage (delay_fps) Op Cost per Move ($B)',    0.0,  5.0, 1.0, key='af_sab_cost',
            help="Operational cost charged to Airbus for each active sabotage move (Bottleneck and/or Poaching). "
                 "Independent of whether Boeing launches — the cost is paid even if the sabotage misses.\n\n"
                 "Math: a_nom_sabotage = value × active_sabs ; PV'd evenly across years 2–10 at WACC_A=8%. Default $1B/move "
                 "with 2 active sabs = $2B nominal → ~$1.45B PV. Separate from the $15B regulatory fine (which fires "
                 "only when sabotage is naked, i.e. Boeing isn't launching fps)."
        )

    with st.sidebar.expander("🛫 WB Re-engine — Share-Capture Speed", expanded=False):
        st.caption("How fast a lone re-engined widebody takes WB share from the milked rival "
                   "(also the leader phase when both re-engine at staggered EIS; capture freezes at the rival's EIS).")
        v_wb_b_capture_pp = st.slider('787 Lone Re-engine Capture (pp/yr)', 0.5, 10.0, 3.0, 0.5, key='af_wb_b_pp',
            help="Speed at which a re-engined 787 captures WB share from a milked A350 — pp per year from the 787 "
                 "re-engine EIS toward the cap 100% − Milker Share (default 85%). Also the 787's leader-phase speed "
                 "when both re-engine at staggered EIS (capture freezes at the A350's EIS). Default 3.0 reproduces "
                 "the prior fixed rule.")
        v_wb_a_capture_pp = st.slider('A350 Lone Re-engine Capture (pp/yr)', 0.5, 10.0, 4.0, 0.5, key='af_wb_a_pp',
            help="Speed at which a re-engined A350 captures WB share from a milked 787 — pp per year from the A350 "
                 "re-engine EIS toward the fixed 60% cap. Also the A350's leader-phase speed when both re-engine at "
                 "staggered EIS (capture freezes at the 787's EIS). Default 4.0 reproduces the prior fixed rule.")

    with st.sidebar.expander("⚠️ Strain & Fines ($B)", expanded=False):
        v_capex_strain_a      = st.slider('Airbus Two-Front Strain',      0.0, 50.0, 5.94, key='af_strain_a')
        v_capex_strain_b      = st.slider('Boeing Two-Front Strain',      0.0, 50.0, 5.94, key='af_strain_b')
        v_naked_sabotage_fine = st.slider('Naked Espionage Fine (Airbus)', 0.0, 50.0, 48.32, key='af_naked_fine')

    # ============================================================
    # 4. THE MATH ENGINE — UNCHANGED
    # ============================================================
    def calculate_tc(nominal_capex, pv_capex, debt, ev, alpha):
        if nominal_capex <= 0:
            return {'total_tc': 0.0, 'nom_capex': 0.0, 'pv_capex': 0.0, 'base_pen': 0.0, 'new_pen': 0.0, 'delta_pen': 0.0}
        base_pen      = debt * alpha * ((debt / ev) ** 2)
        new_debt      = debt + nominal_capex
        new_pen       = new_debt * alpha * ((new_debt / ev) ** 2)
        delta_pen_nom = new_pen - base_pen
        # PV-discount the debt penalty by the CAPEX time profile. The penalty
        # is incurred while CAPEX dollars are on the balance sheet, so it should
        # be discounted to 2026 by the same average year as the CAPEX itself.
        # Using (pv_capex / nominal_capex) as the discount factor: when EIS slips
        # out, CAPEX shifts later → both pv_capex AND delta_pen drop in lockstep.
        pv_factor = pv_capex / nominal_capex
        delta_pen = delta_pen_nom * pv_factor
        return {'total_tc': pv_capex + delta_pen, 'nom_capex': nominal_capex, 'pv_capex': pv_capex,
                'base_pen': base_pen, 'new_pen': new_pen, 'delta_pen': delta_pen,
                'delta_pen_nom': delta_pen_nom, 'pv_factor': pv_factor}

    def get_baseline_metrics():
        b_base_nb_pv = 0.0; a_base_nb_pv = 0.0
        b_base_wb_pv = 0.0; a_base_wb_pv = 0.0
        # Per-program NPV windows (Phase A rule): each segment runs from t=0
        # (year 2026) through eis_t + (NPV_POST_EIS_YRS - 1), inclusive of EIS
        # year. Baseline uses the SAME windows as the scenario for apples-to-
        # apples delta comparison (the "status quo will have the same timeline"
        # constraint from the per-program 20-yr spec).
        _b_nb_end_t = max(0, v_fps_eis_year  - 2026) + NPV_POST_EIS_YRS - 1
        _a_nb_end_t = max(0, v_ngsa_eis_year - 2026) + NPV_POST_EIS_YRS - 1
        _b_wb_end_t = max(0, v_787_eis_year  - 2026) + NPV_POST_EIS_YRS - 1
        _a_wb_end_t = max(0, v_a350_eis_year - 2026) + NPV_POST_EIS_YRS - 1
        _T_base = max(TIMELINE_YRS,
                      _b_nb_end_t + 1, _a_nb_end_t + 1,
                      _b_wb_end_t + 1, _a_wb_end_t + 1)
        for t in range(_T_base):
            df_b = 1 / ((1 + WACC_B)**t)
            df_a = 1 / ((1 + WACC_A)**t)
            if t <= _b_nb_end_t:
                b_base_nb_pv += (NB_PER_YR * 0.40 * PRICE_737  * v_margin_737 ) * df_b
            if t <= _a_nb_end_t:
                a_base_nb_pv += (NB_PER_YR * 0.60 * PRICE_A320 * v_margin_a320) * df_a
            if t <= _b_wb_end_t:
                b_base_wb_pv += (WB_PER_YR * (100/170) * PRICE_WB * v_margin_787 ) * df_b
            if t <= _a_wb_end_t:
                a_base_wb_pv += (WB_PER_YR * (70/170)  * PRICE_WB * v_margin_a350) * df_a
        return {'b_base_nb': b_base_nb_pv, 'b_base_wb': b_base_wb_pv,
                'a_base_nb': a_base_nb_pv, 'a_base_wb': a_base_wb_pv}

    BASE = get_baseline_metrics()

    def evaluate_scenario(a_strat, b_strat):
        b_nom_invest_nb = 0.0; a_nom_invest_nb = 0.0
        b_launches_nb    = "Launch_fps"  in b_strat[0]
        a_launches_nb    = "Launch_NGSA" in a_strat[0]
        b_increases_rate = "Increase_737_Rate" in b_strat[1]
        is_10yr_fps      = "10yr" in b_strat[0]
        is_7yr_fps_solo  = (b_strat[0] == "Launch_fps_7yr_Solo")

        active_sabs     = sum([1 for m in a_strat if "Sabotage" in m and "No" not in m])
        a_nom_sabotage  = v_sabotage_cost * active_sabs
        # Sabotage spend is tied to fps's CAPEX window — Airbus's interference
        # operates during fps's development, ending the year before fps EIS.
        _fps_eis_t_tmp  = max(0, v_fps_eis_year - 2026)
        a_pv_sabotage   = get_pv_stream(a_nom_sabotage,
                                        max(0, _fps_eis_t_tmp - 9), _fps_eis_t_tmp - 1, WACC_A)

        a_regulatory_penalty = 0.0
        if active_sabs > 0 and not b_launches_nb:
            # Naked Espionage Fine is levied when Airbus sabotages while Boeing
            # milks fps. PV-discount to fps EIS year (when sabotage typically
            # surfaces / gets litigated). Slides with fps EIS slider.
            _fine_t = max(0, v_fps_eis_year - 2026)
            a_regulatory_penalty = v_naked_sabotage_fine / ((1 + WACC_A) ** _fine_t)

        if b_launches_nb:
            if is_10yr_fps:            b_nom_invest_nb += v_capex_fps_10yr
            elif "Solo" in b_strat[0]: b_nom_invest_nb += v_capex_fps_7yr
            else:                      b_nom_invest_nb += v_capex_fps_emb
        if a_launches_nb:
            a_nom_invest_nb += v_capex_angsa

        # Per-program NB EIS year (slider) → t-offset (year 0 = 2026).
        # Default 2037 → t=11 (matches previous hardcoded behaviour).
        b_eis_nb_t = max(0, v_fps_eis_year  - 2026)
        a_eis_nb_t = max(0, v_ngsa_eis_year - 2026)

        # NB CAPEX — single lump at NB EIS year (Option B). All NRE recognized
        # at certification/EIS, then PV-discounted to 2026 by 1/(1+wacc)^EIS_t.
        b_pv_nb_invest = b_nom_invest_nb / ((1 + WACC_B) ** b_eis_nb_t)
        a_pv_nb_invest = a_nom_invest_nb / ((1 + WACC_A) ** a_eis_nb_t)

        b_pv_rate_hike = 0.0
        if b_increases_rate:
            # 737 Rate Hike is a FIXED-CALENDAR event in 2032 (t=6), regardless
            # of any EIS slider. Boeing's 737 production rate ramp is tied to
            # supply-chain capacity, not to next-gen platform timing.
            _RATE_HIKE_T   = 6   # 2032 = 2026 + 6
            _RATE_HIKE_YR  = 2032
            b_pv_rate_hike = float(v_capex_737_rate_hike) / ((1 + WACC_B) ** _RATE_HIKE_T)

        # ── NB SHARE RULE — UNIFIED ─────────────────────────────────────────
        # Status quo (40/60) persists until the relevant EIS year. From then
        # on, the trajectory depends on which case applies:
        #  A. Neither launches            → status quo all 31 yrs.
        #  B. Both launch, SAME EIS year  → status quo all 31 yrs (each retains
        #                                    the share held just before launch).
        #  C. NGSA leads (NGSA EIS first OR Boeing milks 737)
        #                                  → Airbus +3pp/yr from NGSA EIS, cap 80%.
        #  D. fps leads  (fps EIS first  OR Airbus milks A320)
        #                                  → Boeing +4pp/yr from fps EIS, cap 80%.
        # Modifiers (rate hike, 7yr ramp, sabotage) stack ADDITIVELY on top.
        # NO ANTICIPATION EFFECT.
        #
        # Compute the FINAL achieved shares at end of timeline (year 30 = 2056)
        # for the math-receipt display. Uses _compute_nb_share_unified() and
        # _apply_nb_modifiers() — same helpers the per-year loop uses, so the
        # receipt cannot drift from the simulator.
        END_T = TIMELINE_YRS - 1   # t=30, calendar 2056
        b_eis_nb_sh, a_eis_nb_sh = _compute_nb_share_unified(
            END_T, b_launches_nb, a_launches_nb, b_eis_nb_t, a_eis_nb_t,
            is_7yr=is_7yr_fps_solo)
        b_eis_nb_sh, a_eis_nb_sh = _apply_nb_modifiers(
            b_eis_nb_sh, a_eis_nb_sh, END_T, b_eis_nb_t, a_eis_nb_t,
            b_launches_nb, a_launches_nb,
            b_inc_rate=b_increases_rate,
            is_7yr=is_7yr_fps_solo, fps_7yr_pp=v_fps_7yr_advantage,
            active_sabs=active_sabs, sab_share_pp=v_sabotage_share)
        # Track sabotage shift magnitude for receipt's separate-line display.
        # The shift is now FLAT (5pp regardless of # active moves) and lasts
        # only 5 yrs from fps EIS — the receipt label reflects this transience.
        b_sab_shift = 0.0
        if active_sabs > 0 and b_launches_nb:
            b_sab_shift = v_sabotage_share / 100.0

        b_reengines = "Re_engine_787"  in b_strat[2]
        a_reengines = "Re_engine_A350" in a_strat[3]

        b_nom_invest_wb = 0.0; a_nom_invest_wb = 0.0
        b_eis_wb_sh, a_eis_wb_sh = 100/170, 70/170

        if b_reengines and not a_reengines:
            # XOR Case E: only Boeing re-engines. CAPEX commits; final
            # achieved share computed below from the gradual catch-up.
            b_nom_invest_wb = v_capex_787_reengine
        elif a_reengines and not b_reengines:
            # XOR Case F: only Airbus re-engines.
            a_nom_invest_wb = v_capex_a350_reengine
        elif b_reengines and a_reengines:
            b_nom_invest_wb = v_capex_787_reengine
            a_nom_invest_wb = v_capex_a350_reengine

        # Per-player WB EIS year (slider) → t-offset (year 0 = 2026).
        # Default 2035 → t=9 (matches previous hardcoded behaviour).
        b_eis_wb_t = max(0, v_787_eis_year  - 2026)
        a_eis_wb_t = max(0, v_a350_eis_year - 2026)

        # FINAL achieved WB shares at end of timeline (year 30 = 2056) — for
        # the math-receipt's "X% → Y%" display labels. The simulator's per-
        # year loop uses the trajectory directly; this is purely cosmetic.
        # Caps: 787 alone → 1 − v_wb_milker (default 85%); A350 alone → 60%;
        # both, 787 first → 80%; both, A350 first → 60%.
        END_T = TIMELINE_YRS - 1   # t=30, calendar 2056
        if b_reengines and not a_reengines:
            # Case E: Boeing +3pp/yr from 787 EIS toward (1 − v_wb_milker)
            years_in = max(0, END_T - b_eis_wb_t + 1)
            b_eis_wb_sh = min(1.0 - v_wb_milker_share, 100/170 + _wb_gain_b() * years_in)
            a_eis_wb_sh = 1.0 - b_eis_wb_sh
        elif a_reengines and not b_reengines:
            # Case F: Airbus +4pp/yr from A350 EIS toward 60%
            years_in = max(0, END_T - a_eis_wb_t + 1)
            a_eis_wb_sh = min(0.60, 70/170 + _wb_gain_a() * years_in)
            b_eis_wb_sh = 1.0 - a_eis_wb_sh
        elif b_reengines and a_reengines and b_eis_wb_t != a_eis_wb_t:
            # Cases C/D: catch-up window is between the two EISs; share then frozen
            catch_yrs = abs(b_eis_wb_t - a_eis_wb_t)
            if b_eis_wb_t < a_eis_wb_t:
                # Case C: 787 first
                b_eis_wb_sh = min(0.80, 100/170 + _wb_gain_b() * catch_yrs)
                a_eis_wb_sh = 1.0 - b_eis_wb_sh
            else:
                # Case D: A350 first
                a_eis_wb_sh = min(0.60, 70/170 + _wb_gain_a() * catch_yrs)
                b_eis_wb_sh = 1.0 - a_eis_wb_sh
        # (Cases A/B: status quo — b_eis_wb_sh/a_eis_wb_sh stay at 100/170, 70/170.)

        # WB CAPEX spread: 6 years ending at each player's EIS (preserves the
        # original 5-year-pre-EIS-through-EIS window; slides with the slider).
        # WB CAPEX — single lump at WB EIS year (Option B).
        b_pv_wb_invest = b_nom_invest_wb / ((1 + WACC_B) ** b_eis_wb_t)
        a_pv_wb_invest = a_nom_invest_wb / ((1 + WACC_A) ** a_eis_wb_t)

        b_scen_nb_pv, a_scen_nb_pv = 0.0, 0.0
        b_scen_wb_pv, a_scen_wb_pv = 0.0, 0.0

        # Per-program NPV window end-t offsets (Phase A: per-program 20-yr windows)
        _b_nb_end_t = b_eis_nb_t + NPV_POST_EIS_YRS - 1
        _a_nb_end_t = a_eis_nb_t + NPV_POST_EIS_YRS - 1
        _b_wb_end_t = b_eis_wb_t + NPV_POST_EIS_YRS - 1
        _a_wb_end_t = a_eis_wb_t + NPV_POST_EIS_YRS - 1
        # Outer loop spans the longest program window. Default sliders give
        # T_dynamic == TIMELINE_YRS == 31 (NB end_t=30); late sliders extend it.
        T_dynamic = max(TIMELINE_YRS,
                        _b_nb_end_t + 1, _a_nb_end_t + 1,
                        _b_wb_end_t + 1, _a_wb_end_t + 1)

        for t in range(T_dynamic):
            df_b = 1 / ((1 + WACC_B)**t)
            df_a = 1 / ((1 + WACC_A)**t)

            # NB share — UNIFIED rule v2 (Phase 1 cap 80, Phase 2 to 50/50)
            # See _compute_nb_share_unified() definition at top of file for
            # full case-by-case spec. Modifiers stack additively below.
            b_sh_nb, a_sh_nb = _compute_nb_share_unified(
                t, b_launches_nb, a_launches_nb, b_eis_nb_t, a_eis_nb_t,
                is_7yr=is_7yr_fps_solo)
            b_sh_nb, a_sh_nb = _apply_nb_modifiers(
                b_sh_nb, a_sh_nb, t, b_eis_nb_t, a_eis_nb_t,
                b_launches_nb, a_launches_nb,
                b_inc_rate=b_increases_rate,
                is_7yr=is_7yr_fps_solo, fps_7yr_pp=v_fps_7yr_advantage,
                active_sabs=active_sabs, sab_share_pp=v_sabotage_share)

            # Price / margin per platform (per-program timing):
            # Pre-each-program's EIS, that player still sells legacy product
            # at the legacy price/margin. Once their EIS arrives, they sell
            # the new platform if they launched, else stay on legacy.
            if b_launches_nb and t >= b_eis_nb_t:
                b_p_nb, b_m_nb = PRICE_fps, v_margin_fps
            else:
                b_p_nb, b_m_nb = PRICE_737, v_margin_737
            if a_launches_nb and t >= a_eis_nb_t:
                a_p_nb, a_m_nb = PRICE_NGSA, v_margin_angsa
            else:
                a_p_nb, a_m_nb = PRICE_A320, v_margin_a320

            # Per-program window mask: only count NB revenue while each
            # player's NB program is within its 20-yr-post-EIS window.
            if t <= _b_nb_end_t:
                b_scen_nb_pv += (NB_PER_YR * b_sh_nb * b_p_nb * b_m_nb) * df_b
            if t <= _a_nb_end_t:
                a_scen_nb_pv += (NB_PER_YR * a_sh_nb * a_p_nb * a_m_nb) * df_a

            # WB share allocation rules — UNIFIED:
            # No pre-EIS anticipation effect; status quo persists until the
            # first relevant EIS year. From then on, the trajectory depends
            # on the case:
            #  A. Neither re-engines  → status quo all 31 yrs.
            #  B. Both, same year     → status quo all 31 yrs (no first-mover).
            #  C. Both, 787 first     → Boeing +3pp/yr (cap 80%) until A350
            #                           EIS, then frozen.
            #  D. Both, A350 first    → Airbus +4pp/yr (cap 60%) until 787
            #                           EIS, then frozen.
            #  E. Only 787 re-engines → Boeing +3pp/yr (cap 1 − v_wb_milker,
            #                           default 85%) from 787 EIS onward.
            #  F. Only A350 re-engines→ Airbus +4pp/yr (cap 60% — structural
            #                           A350 ceiling) from A350 EIS onward.
            if b_reengines and not a_reengines:
                # Case E
                if t < b_eis_wb_t:
                    b_sh_wb, a_sh_wb = 100/170, 70/170
                else:
                    years_in = t - b_eis_wb_t + 1
                    b_sh_wb = min(1.0 - v_wb_milker_share, 100/170 + _wb_gain_b() * years_in)
                    a_sh_wb = 1.0 - b_sh_wb
            elif a_reengines and not b_reengines:
                # Case F
                if t < a_eis_wb_t:
                    b_sh_wb, a_sh_wb = 100/170, 70/170
                else:
                    years_in = t - a_eis_wb_t + 1
                    a_sh_wb = min(0.60, 70/170 + _wb_gain_a() * years_in)
                    b_sh_wb = 1.0 - a_sh_wb
            elif b_reengines and a_reengines and b_eis_wb_t != a_eis_wb_t:
                # Cases C / D
                if b_eis_wb_t < a_eis_wb_t:
                    if t < b_eis_wb_t:
                        b_sh_wb, a_sh_wb = 100/170, 70/170
                    else:
                        catch_t = min(t, a_eis_wb_t - 1)
                        years_in = catch_t - b_eis_wb_t + 1
                        b_sh_wb = min(0.80, 100/170 + _wb_gain_b() * years_in)
                        a_sh_wb = 1.0 - b_sh_wb
                else:
                    if t < a_eis_wb_t:
                        b_sh_wb, a_sh_wb = 100/170, 70/170
                    else:
                        catch_t = min(t, b_eis_wb_t - 1)
                        years_in = catch_t - a_eis_wb_t + 1
                        a_sh_wb = min(0.60, 70/170 + _wb_gain_a() * years_in)
                        b_sh_wb = 1.0 - a_sh_wb
            else:
                # Cases A / B
                b_sh_wb, a_sh_wb = 100/170, 70/170

            # Per-player WB margin in year t, conditional on re-engine state:
            # - If the player hasn't re-engined yet (or never re-engines), use status quo.
            # - From their re-engine EIS onward, use the conditional margin based on
            #   whether the other player also re-engines (in their chosen strategy).
            if b_reengines and t >= b_eis_wb_t:
                b_wb_margin_t = v_margin_787_both if a_reengines else v_margin_787_alone
            else:
                b_wb_margin_t = v_margin_787
            if a_reengines and t >= a_eis_wb_t:
                a_wb_margin_t = v_margin_a350_both if b_reengines else v_margin_a350_alone
            else:
                a_wb_margin_t = v_margin_a350

            # Per-program window mask: only count WB revenue while each
            # player's WB program is within its 20-yr-post-EIS window.
            if t <= _b_wb_end_t:
                b_scen_wb_pv += (WB_PER_YR * b_sh_wb * PRICE_WB * b_wb_margin_t) * df_b
            if t <= _a_wb_end_t:
                a_scen_wb_pv += (WB_PER_YR * a_sh_wb * PRICE_WB * a_wb_margin_t) * df_a

        b_strain_penalty_nom = v_capex_strain_b if (b_launches_nb and b_reengines) else 0.0
        a_strain_penalty_nom = v_capex_strain_a if (a_launches_nb and a_reengines) else 0.0

        b_nom_total = b_nom_invest_nb + b_nom_invest_wb
        a_nom_total = a_nom_invest_nb + a_nom_invest_wb + a_nom_sabotage
        b_pv_total  = b_pv_nb_invest + b_pv_wb_invest
        a_pv_total  = a_pv_nb_invest + a_pv_wb_invest + a_pv_sabotage

        # Two-front strain — PV-discounted by the CAPEX time profile (strain
        # accrues during concurrent NB+WB development, same window as CAPEX).
        # Slides with EIS sliders via pv_total/nom_total ratio.
        b_strain_penalty = (b_strain_penalty_nom * (b_pv_total / b_nom_total)
                            if b_nom_total > 0 else b_strain_penalty_nom)
        a_strain_penalty = (a_strain_penalty_nom * (a_pv_total / a_nom_total)
                            if a_nom_total > 0 else a_strain_penalty_nom)

        b_tc_data = calculate_tc(b_nom_total, b_pv_total, v_debt_boeing, v_ev_boeing, v_alpha)
        a_tc_data = calculate_tc(a_nom_total, a_pv_total, v_debt_airbus, v_ev_airbus, v_alpha)

        b_delta_nb = b_scen_nb_pv - BASE['b_base_nb']
        a_delta_nb = a_scen_nb_pv - BASE['a_base_nb']
        b_delta_wb = b_scen_wb_pv - BASE['b_base_wb']
        a_delta_wb = a_scen_wb_pv - BASE['a_base_wb']

        b_delta_tc = -b_tc_data['total_tc'] - b_pv_rate_hike
        a_delta_tc = -a_tc_data['total_tc']

        b_total_delta = b_delta_nb + b_delta_wb + b_delta_tc - b_strain_penalty
        a_total_delta = a_delta_nb + a_delta_wb + a_delta_tc - a_strain_penalty - a_regulatory_penalty

        b_yield = 100.0 + (b_total_delta / v_ev_boeing) * 100.0
        a_yield = 100.0 + (a_total_delta / v_ev_airbus) * 100.0

        return {
            'yield_b': round(b_yield, 2), 'yield_a': round(a_yield, 2),
            'b_total_delta': b_total_delta, 'a_total_delta': a_total_delta,
            'b_delta_nb': b_delta_nb, 'b_delta_wb': b_delta_wb, 'b_delta_tc': b_delta_tc, 'b_strain': -b_strain_penalty,
            'a_delta_nb': a_delta_nb, 'a_delta_wb': a_delta_wb, 'a_delta_tc': a_delta_tc, 'a_strain': -a_strain_penalty,
            'a_delta_reg': -a_regulatory_penalty, 'b_pv_rate_hike': -b_pv_rate_hike,
            'b_tc_data': b_tc_data, 'a_tc_data': a_tc_data,
            # Per-segment non-recurring PVs (NEW — for the receipt's recurring/non-recurring split)
            'a_pv_nb_invest': a_pv_nb_invest, 'a_pv_wb_invest': a_pv_wb_invest, 'a_pv_sabotage': a_pv_sabotage,
            'b_pv_nb_invest': b_pv_nb_invest, 'b_pv_wb_invest': b_pv_wb_invest,
            'b_scen_nb_pv': b_scen_nb_pv, 'a_scen_nb_pv': a_scen_nb_pv,
            'b_scen_wb_pv': b_scen_wb_pv, 'a_scen_wb_pv': a_scen_wb_pv,
            'a_eis_nb_sh': a_eis_nb_sh, 'b_eis_nb_sh': b_eis_nb_sh,
            'a_eis_wb_sh': a_eis_wb_sh, 'b_eis_wb_sh': b_eis_wb_sh,
            'b_sab_shift': b_sab_shift, 'active_sabs': active_sabs,
            'b_launches_nb': b_launches_nb, 'a_launches_nb': a_launches_nb,
            'b_reengines': b_reengines, 'a_reengines': a_reengines,
        }

    # ============================================================
    # 5. BUILD THE MATRIX & FIND EPSILON-NASH — UNCHANGED
    # ============================================================
    matrix_data = []
    nash_equilibria_details = []

    for row_idx, a_strat in enumerate(A_moves):
        row = []
        for col_idx, b_strat in enumerate(B_moves):
            result = evaluate_scenario(a_strat, b_strat)
            result['is_nash']      = False
            result['is_near_nash'] = False
            row.append(result)
        matrix_data.append(row)

    total_rows = len(A_moves)
    total_cols = len(B_moves)

    for col_idx in range(total_cols):
        max_a = max(matrix_data[row_idx][col_idx]['yield_a'] for row_idx in range(total_rows))
        for row_idx in range(total_rows):
            cell = matrix_data[row_idx][col_idx]
            cell['best_a']      = (cell['yield_a'] == max_a)
            cell['near_best_a'] = (cell['yield_a'] >= max_a - v_tolerance)

    for row_idx in range(total_rows):
        max_b = max(cell['yield_b'] for cell in matrix_data[row_idx])
        for col_idx in range(total_cols):
            cell = matrix_data[row_idx][col_idx]
            cell['best_b']      = (cell['yield_b'] == max_b)
            cell['near_best_b'] = (cell['yield_b'] >= max_b - v_tolerance)

    nash_count = 0
    near_nash_count = 0
    _nash_pairs = []
    _near_nash_pairs = []
    for row_idx in range(total_rows):
        for col_idx in range(total_cols):
            cell = matrix_data[row_idx][col_idx]
            if cell['best_a'] and cell['best_b']:
                cell['is_nash'] = True
                nash_count += 1
                nash_equilibria_details.append({
                    'a_strat': A_moves[row_idx],
                    'b_strat': B_moves[col_idx],
                    'row_idx': row_idx, 'col_idx': col_idx,
                    'result': cell
                })
                _nash_pairs.append((A_moves[row_idx], B_moves[col_idx],
                                    cell['yield_a'], cell['yield_b']))
            elif cell['near_best_a'] and cell['near_best_b']:
                cell['is_near_nash'] = True
                near_nash_count += 1
                _near_nash_pairs.append((A_moves[row_idx], B_moves[col_idx],
                                         cell['yield_a'], cell['yield_b']))

    # Persist a snapshot for the Summary tab
    st.session_state["_af_nash_count"] = nash_count
    st.session_state["_af_near_nash_count"] = near_nash_count
    st.session_state["_af_nash_pairs"] = _nash_pairs
    st.session_state["_af_near_nash_pairs"] = _near_nash_pairs

    st.sidebar.markdown("---")
    st.sidebar.write(f"**⭐ Pure Nash Found:** {nash_count}")
    st.sidebar.write(f"**⚠️ Near-Nash Found:** {near_nash_count}")

    # ============================================================
    # 6. RENDER THE INTERACTIVE GAMEBOARD  (engine-board style)
    # ============================================================
    def f_m(m):
        return (m.replace('Launch_', 'L_').replace('Sabotage_', 'Delay_fps_').replace('Re_engine_', 'Re_')
                 .replace('Increase_', 'Inc_').replace('_Rate', '').replace('_Solo', '')
                 .replace('_via_Embraer', '+Emb'))

    def clean_txt(t): return t.replace('_', ' ')

    st.title("🎲 The Duopoly Shall Go On — Airframer Gameboard")

    # ── Supplier Selection Banner (NEW) ──
    _b_sup = st.session_state.get("_b_supplier", "RR")
    _a_sup = st.session_state.get("_a_supplier", "PW")
    _b_share = st.session_state.get("_boeing_share_both", 50)
    _a_share = 100 - _b_share
    _b_c, _a_c = SUPPLIER_CODE[_b_sup], SUPPLIER_CODE[_a_sup]
    _rr, _pw, _cfm = derive_nb_engine_shares(_b_c, _a_c, _b_share)
    st.markdown(
        f"<div style='background:#0d1117;border:1px solid #30363d;border-left:4px solid #58a6ff;"
        f"border-radius:6px;padding:10px 14px;margin-bottom:10px;font-family:monospace;font-size:12px;color:#ddd;'>"
        f"🔌 <b>Engine Supplier:</b> &nbsp;"
        f"<span class='player-b'>Boeing fps → {_b_sup} ({_b_share}%)</span> &nbsp;|&nbsp; "
        f"<span class='player-a'>Airbus NGSA → {_a_sup} ({_a_share}%)</span> &nbsp;|&nbsp; "
        f"<b>Code ({_b_c},{_a_c})</b> &nbsp;|&nbsp; "
        f"Implied post-2037 NB engine market: RR {_rr:.0f}% · PW {_pw:.0f}% · CFM {_cfm:.0f}%"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "**Board Context:** <span class='player-a'>Player A: Airbus (Rows)</span> vs "
        "<span class='player-b'>Player B: Boeing (Columns)</span>. "
        "Yields are normalized as a % of Enterprise Value  [ 100% + (Total Δ EV / Total EV) ].",
        unsafe_allow_html=True)

    # ============================================================
    # EQUILIBRIUM SUMMARY TABLE
    # One unified 6-column table per player. Top header row merges
    # cells: "NB Mkt" spans 3 cols, "WB Mkt" spans 3 cols. Sub-header
    # row has Move | Costs ($B) | Mkt Share Impact (repeated). NB and
    # WB moves are paired row-by-row; shorter list padded with blanks.
    # ============================================================
    def _pp_move(m):
        return (str(m).replace("Launch_", "Launch ")
                .replace("Sabotage_", "Delay fps ")
                .replace("Re_engine_", "Re-engine ")
                .replace("Increase_", "Increase ")
                .replace("_Solo", " Solo").replace("_via_Embraer", " via Embraer")
                .replace("_Rate", " Rate").replace("_", " ").strip())

    def _move_with_eis(s):
        """Append '(EIS - YYYY)' suffix to a pretty-printed move name. Milk
        moves and other status-quo moves return unchanged (no EIS)."""
        if "Milk" in s:
            return s
        if "Launch fps" in s:        return f"{s} (EIS - {v_fps_eis_year})"
        if "Launch NGSA" in s:       return f"{s} (EIS - {v_ngsa_eis_year})"
        if "Increase 737 Rate" in s: return f"{s} (EIS - 2032)"   # fixed-calendar, NOT tied to fps EIS
        if "Delay fps" in s:         return f"{s} (EIS - {v_fps_eis_year})"        # sabotages fire at fps EIS
        if "Re-engine 787" in s:     return f"{s} (EIS - {v_787_eis_year})"
        if "Re-engine A350" in s:    return f"{s} (EIS - {v_a350_eis_year})"
        return s

    def _fmt_a_nb(a):
        parts = [_move_with_eis(_pp_move(a[0]))]
        if "No" not in a[1]: parts.append(_move_with_eis(_pp_move(a[1])))
        if "No" not in a[2]: parts.append(_move_with_eis(_pp_move(a[2])))
        return " + ".join(parts)

    def _fmt_b_nb(b):
        parts = [_move_with_eis(_pp_move(b[0]))]
        if "No" not in b[1]: parts.append(_move_with_eis(_pp_move(b[1])))
        return " + ".join(parts)

    def _fmt_costs(items):
        """items = list of (label, amount). Skip zero amounts. Format:
           '0' if no non-zero items; '38.10' if 1; '20.00 + 1.00 = 21.00' if 2+."""
        nums = [c for _, c in items if c > 0]
        if not nums:
            return "0"
        if len(nums) == 1:
            return f"{nums[0]:.2f}"
        return " + ".join(f"{c:.2f}" for c in nums) + f" = {sum(nums):.2f}"

    # ── Cost / impact extractors ──
    def _b_nb_cost(m):
        items = []
        if   "Embraer"   in m: items.append(("fps via Embraer NRE", v_capex_fps_emb))
        elif "7yr Solo"  in m: items.append(("fps 7yr Solo NRE",    v_capex_fps_7yr))
        elif "10yr Solo" in m: items.append(("fps 10yr Solo NRE",   v_capex_fps_10yr))
        # rate hike — operational, no NRE → 0
        return _fmt_costs(items)

    def _b_nb_impact(m):
        parts = []
        if any(s in m for s in ("Embraer", "7yr Solo", "10yr Solo")):
            parts.append("Phase 2: climbs to 50/50 (if NGSA also launches) or 80% cap (alone)")
            if "7yr" in m: parts.append(f"+{v_fps_7yr_advantage:.1f}pp 7yr-ramp bonus")
        if "Milk 737" in m:
            parts.append("Status quo 40% NB; declines to 20% floor if NGSA launches")
        if "Increase 737 Rate" in m:
            parts.append("+5pp Boeing in 2032-2036 (fixed-calendar rate hike)")
        return "; ".join(parts) if parts else "—"

    def _b_wb_cost(m):
        items = []
        if "Re-engine" in m: items.append(("787 re-engine NRE", v_capex_787_reengine))
        return _fmt_costs(items)

    def _b_wb_impact(m):
        if "Milk" in m:      return "Status quo 100/170 = 58.8% WB share"
        if "Re-engine" in m: return f"Alone (Case E): +{v_wb_b_capture_pp:.1f}pp/yr toward {(1.0 - v_wb_milker_share)*100:.0f}% cap; both re-engine: same EIS → status quo, staggered → leader capture freezes at rival EIS"
        return "—"

    def _a_nb_cost(m):
        items = []
        if "Launch NGSA" in m: items.append(("NGSA NRE", v_capex_angsa))
        sab_count = ("Delay fps Bottleneck" in m) + ("Delay fps Poaching" in m)
        for _ in range(sab_count):
            items.append(("Sabotage op cost", v_sabotage_cost))
        return _fmt_costs(items)

    def _a_nb_impact(m):
        parts = []
        if "Launch NGSA" in m:
            parts.append("Phase 2: climbs to 50/50 (if fps also launches) or 80% cap (alone)")
        if "Delay fps Bottleneck" in m or "Delay fps Poaching" in m:
            parts.append(f"−{v_sabotage_share:.0f}pp Boeing for 5 yrs from fps EIS (flat — 1 or 2 sabotages same effect)")
        if "Milk A320" in m:
            parts.append("Status quo 60% NB; peaks at 80% if fps milks")
        return "; ".join(parts) if parts else "—"

    def _a_wb_cost(m):
        items = []
        if "Re-engine" in m: items.append(("A350 re-engine NRE", v_capex_a350_reengine))
        return _fmt_costs(items)

    def _a_wb_impact(m):
        if "Milk" in m:      return "Status quo 70/170 = 41.2% WB share"
        if "Re-engine" in m: return f"Alone (Case F): +{v_wb_a_capture_pp:.1f}pp/yr toward 60% cap; both re-engine: same EIS → status quo, staggered → leader capture freezes at rival EIS"
        return "—"

    # Collect moves + count appearances in Pure Nash and Near-Nash
    _b_nb_pure = set(); _b_wb_pure = set()
    _a_nb_pure = set(); _a_wb_pure = set()
    # Per-move appearance counts: {move_str: count}
    _b_nb_pn_c = {}; _b_wb_pn_c = {}; _a_nb_pn_c = {}; _a_wb_pn_c = {}
    _b_nb_nn_c = {}; _b_wb_nn_c = {}; _a_nb_nn_c = {}; _a_wb_nn_c = {}
    def _inc(d, k): d[k] = d.get(k, 0) + 1
    for (a, b, _, _) in _nash_pairs:
        ka_nb = _fmt_a_nb(a); ka_wb = _move_with_eis(_pp_move(a[3]))
        kb_nb = _fmt_b_nb(b); kb_wb = _move_with_eis(_pp_move(b[2]))
        _a_nb_pure.add(ka_nb); _a_wb_pure.add(ka_wb)
        _b_nb_pure.add(kb_nb); _b_wb_pure.add(kb_wb)
        _inc(_a_nb_pn_c, ka_nb); _inc(_a_wb_pn_c, ka_wb)
        _inc(_b_nb_pn_c, kb_nb); _inc(_b_wb_pn_c, kb_wb)
    _b_nb_all = set(_b_nb_pure); _b_wb_all = set(_b_wb_pure)
    _a_nb_all = set(_a_nb_pure); _a_wb_all = set(_a_wb_pure)
    for (a, b, _, _) in _near_nash_pairs:
        ka_nb = _fmt_a_nb(a); ka_wb = _move_with_eis(_pp_move(a[3]))
        kb_nb = _fmt_b_nb(b); kb_wb = _move_with_eis(_pp_move(b[2]))
        _a_nb_all.add(ka_nb); _a_wb_all.add(ka_wb)
        _b_nb_all.add(kb_nb); _b_wb_all.add(kb_wb)
        _inc(_a_nb_nn_c, ka_nb); _inc(_a_wb_nn_c, ka_wb)
        _inc(_b_nb_nn_c, kb_nb); _inc(_b_wb_nn_c, kb_wb)

    def _combined_af_table(players_data):
        """Render multiple airframer players in ONE table with merged Player column.
        Each player dict: name, klass, nb_set, nb_pure, nb_pn_c, nb_nn_c, nb_cost_fn,
        nb_impact_fn, wb_set, wb_pure, wb_pn_c, wb_nn_c, wb_cost_fn, wb_impact_fn.
        """
        def _badge(m, pn_c, nn_c):
            pn = pn_c.get(m, 0); nn = nn_c.get(m, 0)
            parts = []
            if pn > 0: parts.append(f"<span style='color:#3cb371;font-weight:bold;'>⭐{pn}</span>")
            if nn > 0: parts.append(f"<span style='color:#FFD700;font-weight:bold;'>⚠️{nn}</span>")
            return ("&nbsp;" + " ".join(parts)) if parts else ""
        rows_html = []
        for idx, pd in enumerate(players_data):
            nb_list = sorted(pd['nb_set'])
            wb_list = sorted(pd['wb_set'])
            n = max(len(nb_list), len(wb_list), 1)
            # Thicker top border on the FIRST row of each player except the first
            top_border = "border-top:2px solid #58a6ff;" if idx > 0 else ""
            for i in range(n):
                row_cells = []
                # Player cell — only on first row, with rowspan
                if i == 0:
                    row_cells.append(
                        f"<td rowspan='{n}' class='{pd['klass']}' "
                        f"style='vertical-align:middle;padding:8px 10px;border:1px solid #30363d;"
                        f"{top_border}font-weight:bold;text-align:center;background:#161b22;"
                        f"font-size:13px;writing-mode:horizontal-tb;'>{pd['name']}</td>"
                    )
                row_top = top_border if i == 0 else ""
                # NB cells
                if i < len(nb_list):
                    m = nb_list[i]
                    lbl = (f"<b>{m}</b>" if m in pd['nb_pure'] else m) + _badge(m, pd['nb_pn_c'], pd['nb_nn_c'])
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;{row_top}'>{lbl}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;text-align:right;font-family:monospace;white-space:nowrap;{row_top}'>{pd['nb_cost_fn'](m)}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;max-width:240px;word-wrap:break-word;white-space:normal;line-height:1.35;{row_top}'>{pd['nb_impact_fn'](m)}</td>")
                else:
                    row_cells.extend([f"<td style='border:1px solid #30363d;{row_top}'></td>"] * 3)
                # WB cells
                if i < len(wb_list):
                    m = wb_list[i]
                    lbl = (f"<b>{m}</b>" if m in pd['wb_pure'] else m) + _badge(m, pd['wb_pn_c'], pd['wb_nn_c'])
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;{row_top}'>{lbl}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;text-align:right;font-family:monospace;white-space:nowrap;{row_top}'>{pd['wb_cost_fn'](m)}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;max-width:240px;word-wrap:break-word;white-space:normal;line-height:1.35;{row_top}'>{pd['wb_impact_fn'](m)}</td>")
                else:
                    row_cells.extend([f"<td style='border:1px solid #30363d;{row_top}'></td>"] * 3)
                rows_html.append("<tr>" + "".join(row_cells) + "</tr>")
        return f"""
<div style="margin-top:12px;">
  <table style="border-collapse:collapse;font-size:12px;color:#ddd;">
    <thead>
      <tr style="background:#161b22;">
        <th rowspan="2" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#1a1f36;text-align:center;min-width:80px;">Player</th>
        <th colspan="3" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#1a2332;text-align:center;">NB Mkt</th>
        <th colspan="3" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#2a1a1a;text-align:center;">WB Mkt</th>
      </tr>
      <tr style="background:#0d1117;">
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Move</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Costs ($B)</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Mkt Share Impact</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Move</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Costs ($B)</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Mkt Share Impact</th>
      </tr>
    </thead>
    <tbody>{"".join(rows_html)}</tbody>
  </table>
</div>"""

    _af_summary_header_html = (
        f"#### 📋 Equilibrium summary — mutually exclusive moves "
        f"({len(_nash_pairs)} Pure Nash · {len(_near_nash_pairs)} Near-Nash) "
        f"&nbsp;·&nbsp; <i style='font-size:11px;'>each move shows "
        f"<span style='color:#3cb371;font-weight:bold;'>⭐N</span> Pure Nash and "
        f"<span style='color:#FFD700;font-weight:bold;'>⚠️N</span> Near-Nash appearance count</i>"
    )
    _af_combined_table_html = _combined_af_table([
        {'name': '🟢 Boeing', 'klass': 'player-b',
         'nb_set': _b_nb_all, 'nb_pure': _b_nb_pure,
         'nb_pn_c': _b_nb_pn_c, 'nb_nn_c': _b_nb_nn_c,
         'nb_cost_fn': _b_nb_cost, 'nb_impact_fn': _b_nb_impact,
         'wb_set': _b_wb_all, 'wb_pure': _b_wb_pure,
         'wb_pn_c': _b_wb_pn_c, 'wb_nn_c': _b_wb_nn_c,
         'wb_cost_fn': _b_wb_cost, 'wb_impact_fn': _b_wb_impact},
        {'name': '🔵 Airbus', 'klass': 'player-a',
         'nb_set': _a_nb_all, 'nb_pure': _a_nb_pure,
         'nb_pn_c': _a_nb_pn_c, 'nb_nn_c': _a_nb_nn_c,
         'nb_cost_fn': _a_nb_cost, 'nb_impact_fn': _a_nb_impact,
         'wb_set': _a_wb_all, 'wb_pure': _a_wb_pure,
         'wb_pn_c': _a_wb_pn_c, 'wb_nn_c': _a_wb_nn_c,
         'wb_cost_fn': _a_wb_cost, 'wb_impact_fn': _a_wb_impact},
    ])
    # Persist for the Summary tab to mirror at the top.
    st.session_state["_af_summary_header_html"] = _af_summary_header_html
    st.session_state["_af_combined_table_html"] = _af_combined_table_html

    st.markdown(_af_summary_header_html, unsafe_allow_html=True)
    st.markdown(_af_combined_table_html, unsafe_allow_html=True)

    # ── Diverging bar chart: 100% line in center, bars grow up/down from it ──
    # Same structure as the Engine tab. PX_PER is computed dynamically from
    # the global max |delta| across BOTH Airbus (blue) and Boeing (green)
    # yields → both colours share a single common scale, the largest |delta|
    # in the matrix exactly fills LINE_Y, and small deltas remain visibly
    # proportional instead of being clamped to the ceiling.
    BAR_H  = 80
    LINE_Y = 40
    _max_abs_delta = 0.5    # floor — avoid divide-by-zero / over-stretch
    for _row in matrix_data:
        for _cell in _row:
            _max_abs_delta = max(_max_abs_delta,
                                 abs(_cell['yield_a'] - 100.0),
                                 abs(_cell['yield_b'] - 100.0))
    PX_PER = LINE_Y / _max_abs_delta

    def bar_div(val):
        delta = val - 100.0
        px = max(2, min(LINE_Y, int(round(abs(delta) * PX_PER))))
        return px, (delta >= 0)

    def _nb_wb_split_html(nb_lines, wb_lines):
        """Render a th's content as a 2-row inner table: NB label on the left,
        NB moves right-aligned; WB label on the left, WB moves right-aligned."""
        nb_html = "<br/>".join(nb_lines) if nb_lines else "—"
        wb_html = "<br/>".join(wb_lines) if wb_lines else "—"
        return (
            "<table style='border:none;border-collapse:collapse;width:100%;font-size:inherit;line-height:1.2;margin:0;'>"
            "<tr>"
            "<td style='border:none;padding:0 4px 0 0;text-align:left;font-weight:bold;font-size:16px;color:#58a6ff;width:32px;vertical-align:top;'>NB</td>"
            f"<td style='border:none;padding:0 0 0 4px;text-align:right;vertical-align:middle;'>{nb_html}</td>"
            "</tr>"
            "<tr>"
            "<td style='border:none;border-top:1px solid #555;padding:0 4px 0 0;text-align:left;font-weight:bold;font-size:16px;color:#ff7b72;width:32px;vertical-align:top;'>WB</td>"
            f"<td style='border:none;border-top:1px solid #555;padding:0 0 0 4px;text-align:right;vertical-align:middle;'>{wb_html}</td>"
            "</tr>"
            "</table>"
        )

    # ── Grouped-header CSS (scoped; added on top, existing styles untouched) ──
    st.markdown("""
    <style>
    .bh-grp { background:#001a0d; border:1px solid #1f6f3f; color:#9be8b0; font-weight:bold;
              text-align:center !important; vertical-align:middle !important; padding:7px 8px; line-height:1.25;
              font-family:'Courier New',Courier,monospace; font-size:13px; }
    .bh-grp-top { background:#04230f; color:#46e06e; font-size:16px; letter-spacing:1px;
                  border-bottom:2px solid #32CD32; }
    .rh-grp { background:#001a26; border:1px solid #1f5f7f; color:#9bd8ff; font-weight:bold;
              text-align:center !important; vertical-align:middle !important; padding:7px 9px; line-height:1.25;
              font-family:'Courier New',Courier,monospace; font-size:13px; }
    .rh-grp-prog { background:#04202e; color:#4cc6ff; font-size:16px; letter-spacing:1px;
                   border-right:2px solid #00BFFF; }
    </style>
    """, unsafe_allow_html=True)

    # ── Gameboard with MERGED / GROUPED headers ──
    # Boeing columns nest in 4 bands: umbrella (Launch fps | Do Nothing) > fps variant
    #   > 737 rate > 787 WB leaf. Airbus rows nest with rowspan in 4 levels:
    #   program (NGSA/Do Nothing) > bottleneck > poaching > A350 WB.
    # Index maps: B_moves[c] -> a=c//4, b=(c%4)//2, wb=c%2 (product A,B,WB)
    #             A_moves[r] -> a=r//8, b=(r%8)//4, c=(r%4)//2, wb=r%2 (product A,B,C,WB)
    html = ['<div class="board-container"><table class="board-table">']

    # Band 0 — corner (spans 4 header rows x 4 row-header cols) + umbrella
    html.append('<tr>')
    html.append(
        '<th rowspan="4" colspan="4" style="background: linear-gradient(to top right, #001a26 49%, #ffffff 49%, #ffffff 51%, #001a0d 51%); '
        'border: 2px solid #ffffff; position: relative; z-index: 20; min-width: 430px; height: 90px; padding: 0;">'
        '<span style="position: absolute; top: 8px; right: 10px; color: #32CD32; font-weight: bold; font-size: 14px; text-align: right; line-height: 1.15;">'
        '🟢 Boeing<br/><span style="font-size: 10px; font-weight: normal; color: #32CD32;">(columns →)</span></span>'
        '<span style="position: absolute; bottom: 8px; left: 10px; color: #00BFFF; font-weight: bold; font-size: 14px; text-align: left; line-height: 1.15;">'
        '🔵 Airbus<br/><span style="font-size: 10px; font-weight: normal; color: #00BFFF;">(↓ rows)</span></span>'
        '</th>'
    )
    html.append('<th class="bh-grp bh-grp-top" colspan="12" style="text-align:center;vertical-align:middle;">Launch fps</th>')
    html.append('<th class="bh-grp bh-grp-top" colspan="4" rowspan="2" style="text-align:center;vertical-align:middle;">Do Nothing'
                '<br/><span style="font-size:11px;font-weight:normal;color:#9be8b0;">(milk 737)</span></th>')
    html.append('</tr>')

    # Band 1 — fps variant
    html.append('<tr>')
    html.append('<th class="bh-grp" colspan="4">7-yr ramp</th>')
    html.append('<th class="bh-grp" colspan="4">10-yr ramp</th>')
    html.append('<th class="bh-grp" colspan="4">via Embraer</th>')
    html.append('</tr>')

    # Band 2 — 737 rate (per fps/milk block: Increase | No Increase)
    html.append('<tr>')
    for _a_blk in range(4):
        html.append('<th class="bh-grp" colspan="2">Inc. 737 rate</th>')
        html.append('<th class="bh-grp" colspan="2">no rate hike</th>')
    html.append('</tr>')

    # Band 3 — 787 WB leaf (one cell per data column; sets column width)
    html.append('<tr>')
    for _c in range(total_cols):
        _wb_lbl = "Re-engine 787" if (_c % 2 == 0) else "milk 787"
        html.append(f'<th class="bh-grp" style="min-width:94px;">{_wb_lbl}</th>')
    html.append('</tr>')

    # ── Data rows with nested (rowspan) Airbus row headers ──
    for ai, a_strat in enumerate(A_moves):
        html.append('<tr>')
        # Level 0 — program (rowspan 8)
        if ai % 8 == 0:
            _prog = ("Launch NGSA" if ai // 8 == 0
                     else 'Do Nothing<br/><span style="font-size:11px;font-weight:normal;color:#9bd8ff;">(milk A320)</span>')
            html.append(f'<th class="rh-grp rh-grp-prog" rowspan="8" style="min-width:120px;">{_prog}</th>')
        # Level 1 — bottleneck (rowspan 4)
        if ai % 4 == 0:
            _btl = "Delay fps:<br/>Bottleneck" if (ai % 8) // 4 == 0 else "No<br/>bottleneck"
            html.append(f'<th class="rh-grp" rowspan="4" style="min-width:104px;">{_btl}</th>')
        # Level 2 — poaching (rowspan 2)
        if ai % 2 == 0:
            _poach = "Delay fps:<br/>Poaching" if (ai % 4) // 2 == 0 else "No<br/>poaching"
            html.append(f'<th class="rh-grp" rowspan="2" style="min-width:104px;">{_poach}</th>')
        # Level 3 — A350 WB leaf (rowspan 1)
        _awb = "Re-engine A350" if (ai % 2 == 0) else "milk A350"
        html.append(f'<th class="rh-grp" style="min-width:104px;">{_awb}</th>')
        for ci in range(total_cols):
            b_strat = B_moves[ci]
            cell = matrix_data[ai][ci]
            cls, icon = "board-td", ""
            if cell['is_nash']:        cls += " nash-pure"; icon = "⭐ "
            elif cell['is_near_nash']: cls += " nash-near"; icon = "⚠️ "

            ay = cell['yield_a']; by = cell['yield_b']
            ad = cell['a_total_delta']; bd = cell['b_total_delta']

            px_a, up_a = bar_div(ay)
            px_b, up_b = bar_div(by)

            # Bright above 100% (value created), dim below (value destroyed)
            col_a = "#00BFFF" if up_a else "#006080"
            col_b = "#32CD32" if up_b else "#1a6611"

            # Position: above line → bottom of bar touches line; below → top touches line
            if up_a:
                style_a = f"position:absolute;bottom:{BAR_H - LINE_Y}px;width:28px;height:{px_a}px;background:{col_a};border-radius:2px 2px 0 0;"
            else:
                style_a = f"position:absolute;top:{LINE_Y}px;width:28px;height:{px_a}px;background:{col_a};border-radius:0 0 2px 2px;"

            if up_b:
                style_b = f"position:absolute;bottom:{BAR_H - LINE_Y}px;width:28px;height:{px_b}px;background:{col_b};border-radius:2px 2px 0 0;"
            else:
                style_b = f"position:absolute;top:{LINE_Y}px;width:28px;height:{px_b}px;background:{col_b};border-radius:0 0 2px 2px;"

            bars = (
                f'<div style="position:relative;height:{BAR_H}px;margin:0 auto;width:80px;">'
                # 100% reference line
                f'<div style="position:absolute;top:{LINE_Y}px;left:0;right:0;'
                f'border-top:1px solid rgba(255,255,255,0.35);z-index:2;"></div>'
                # Airbus bar (left)
                f'<div style="{style_a}left:8px;" title="Airbus: {ay:.0f}%"></div>'
                # Boeing bar (right)
                f'<div style="{style_b}right:8px;" title="Boeing: {by:.0f}%"></div>'
                f'</div>'
                # Numbers below
                f'<div style="font-size:16px;line-height:1.0;margin-top:2px;text-align:center;font-weight:bold;">'
                f'<span class="player-a">{ay:.0f}</span>'
                f' '
                f'<span class="player-b">{by:.0f}</span></div>'
            )

            tip = (
                f"<div class='receipt-tooltip'>"
                f"<div style='border-bottom:1px solid #444;margin-bottom:8px;color:#FFD700;font-weight:bold;'>"
                f"TACTICAL MATH RECEIPT (T={TIMELINE_YRS}yrs)</div>"
                f"<div style='margin-bottom:8px;'>"
                f"<b>Airbus:</b> {clean_txt(a_strat[0])} | {clean_txt(a_strat[1])} | {clean_txt(a_strat[2])} | {clean_txt(a_strat[3])}<br/>"
                f"<b>Boeing:</b> {clean_txt(b_strat[0])} | {clean_txt(b_strat[1])} | {clean_txt(b_strat[2])}"
                f"</div>"
                f"<span class='player-a'>[A] Airbus Yield: {ay:.0f}% (Δ ${ad:+.2f}B, 2026–2056)</span><br/>"
                f"<span class='player-b'>[B] Boeing Yield: {by:.0f}% (Δ ${bd:+.2f}B, 2026–2056)</span>"
                f"</div>"
            )
            html.append(f'<td class="{cls}"><span style="position:absolute;top:2px;left:3px;font-size:13px;line-height:1;z-index:5;">{icon}</span>{bars}{tip}</td>')
        html.append('</tr>')
    html.append('</table></div>')
    st.markdown("".join(html), unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style='background: #111; padding: 10px; border-radius: 5px; margin-top: -20px; margin-bottom: 20px; font-size: 13px;'>
        <b>Legend:</b> &nbsp;&nbsp;
        <span style='color:#3cb371'>⭐ Pure Nash Equilibrium</span> (mathematically optimal for both) &nbsp; | &nbsp;
        <span style='color:#FFD700'>⚠️ Near-Nash State</span> (within ±{t}% Yield tolerance) &nbsp; | &nbsp;
        Bars diverge from the 100 % EV line — up = value created, down = value destroyed.
    </div>
    """.format(t=v_tolerance), unsafe_allow_html=True)

    # ============================================================
    # 7. GAME MATH BREAKDOWN  (engine-board nash-box style)
    # ============================================================
    st.markdown("---")
    st.title("🧮 Game Math Breakdown & Nash Receipts")

    # ── Baseline Status Quo Box ──
    st.markdown(f"""
    <div class="nash-box">
    <div class="nash-title" style="color:#58a6ff;">⚓ Baseline Status Quo Breakdown (Anchor for Deltas)</div>

    <table class="math-breakdown-table" style="font-size:13px;color:#ddd;width:100%;">
        <tr><td colspan="3" style="border-bottom:1px solid #444;color:#58a6ff;font-weight:bold;padding-bottom:5px;">
            1. PRE-MOVE STATUS QUO SHARES</td></tr>
        <tr>
            <td style="padding:8px;"><b>NB Market:</b> 2,000 a/c / yr</td>
            <td style="padding:8px;"><span class="player-a">Airbus: 60%</span></td>
            <td style="padding:8px;"><span class="player-b">Boeing: 40%</span></td>
        </tr>
        <tr>
            <td style="padding:8px;"><b>WB Market:</b> 170 a/c / yr</td>
            <td style="padding:8px;"><span class="player-a">Airbus: {70/170*100:.1f}%</span></td>
            <td style="padding:8px;"><span class="player-b">Boeing: {100/170*100:.1f}%</span></td>
        </tr>
        <tr><td colspan="3" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            2. PRICING & MARGINS</td></tr>
        <tr>
            <td style="padding:8px;"><b>NB Prices:</b> 737=${PRICE_737*1000:.0f}M | A320=${PRICE_A320*1000:.0f}M | fps=${PRICE_fps*1000:.0f}M | NGSA=${PRICE_NGSA*1000:.0f}M</td>
            <td colspan="2" style="padding:8px;"><b>WB Price:</b> ${PRICE_WB*1000:.0f}M</td>
        </tr>
        <tr>
            <td colspan="3" style="padding:8px;">
            <span class="player-a">Airbus Margins → A320: {v_margin_a320*100:.0f}% | NGSA: {v_margin_angsa*100:.0f}% | A350: {v_margin_a350*100:.0f}%</span><br/>
            <span class="player-b">Boeing Margins → 737: {v_margin_737*100:.0f}% | fps: {v_margin_fps*100:.0f}% | 787: {v_margin_787*100:.0f}%</span>
            </td>
        </tr>
        <tr><td colspan="3" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            3. DCF DISCOUNTING PARAMETERS</td></tr>
        <tr>
            <td style="padding:8px;"><b>T:</b> {TIMELINE_YRS} yrs (2026–2056)</td>
            <td style="padding:8px;"><span class="player-a">WACC: {WACC_A*100:.1f}%</span></td>
            <td style="padding:8px;"><span class="player-b">WACC: {WACC_B*100:.1f}%</span></td>
        </tr>
        <tr>
            <td colspan="3" style="padding:8px;color:#aaa;font-size:11px;">
                <b>Formula (Time-Series DCF, 2026–2056):</b><br/>
                Annual CF(t) = Planes/yr × Share(t) × Price(t) × Margin(t) &nbsp;|&nbsp;
                NPV = Σ(t=0..30) Annual CF(t) / (1+WACC)^t &nbsp;|&nbsp;
                Δ EV = NPV_scenario − NPV_baseline − PV_Invest − ΔDebtPenalty − Strain
            </td>
        </tr>
        <tr><td colspan="3" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            4. BALANCE SHEETS</td></tr>
        <tr>
            <td style="padding:8px;"></td>
            <td style="padding:8px;"><span class="player-a">EV: ${v_ev_airbus:.0f}B | Debt: ${v_debt_airbus:.0f}B</span></td>
            <td style="padding:8px;"><span class="player-b">EV: ${v_ev_boeing:.0f}B | Debt: ${v_debt_boeing:.0f}B</span></td>
        </tr>
    </table>

    <div class="delta-grid" style="border-top:1px solid #30363d;padding-top:20px;">
        <div class="delta-col col-a">
            <span class="player-a">Airbus Baseline NPV</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
                <tr><td><b>NB NPV (A320neo):</b></td><td class="val">${BASE['a_base_nb']:.2f}B</td></tr>
                <tr><td><b>WB NPV (A350):</b></td><td class="val">${BASE['a_base_wb']:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Total Base NPV:</b> <span class="player-a" style="float:right;font-size:16px;">${BASE['a_base_nb']+BASE['a_base_wb']:.2f}B</span>
        </div>
        <div class="delta-col col-b">
            <span class="player-b">Boeing Baseline NPV</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
                <tr><td><b>NB NPV (737 MAX):</b></td><td class="val">${BASE['b_base_nb']:.2f}B</td></tr>
                <tr><td><b>WB NPV (787):</b></td><td class="val">${BASE['b_base_wb']:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Total Base NPV:</b> <span class="player-b" style="float:right;font-size:16px;">${BASE['b_base_nb']+BASE['b_base_wb']:.2f}B</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nash Equilibrium Receipt Renderer ──
    def format_val(val):
        if   val > 0:  return f"<span class='positive-val'>+${val:.2f}B</span>"
        elif val < 0:  return f"<span class='negative-val'>-${abs(val):.2f}B</span>"
        else:          return f"<span style='color:#777'>$0.00B</span>"

    def render_receipt(idx, ne, is_pure):
        r  = ne['result']
        a_m = ne['a_strat']; b_m = ne['b_strat']
        title = f"⭐ Pure Nash #{idx+1}" if is_pure else f"⚠️ Near-Nash #{idx+1}"
        bc    = "#3cb371" if is_pure else "#FFD700"
        tc    = "nash-title-pure" if is_pure else "nash-title-near"

        # ----- Airbus column -----
        a_blocks = []
        a_blocks.append(f"<table class='math-breakdown-table'>")
        # When one player launches and the other milks (XOR), the milker share
        # applies across the FULL timeline — show "Full timeline" instead of
        # "(2037+)" so the label matches the math.
        _nb_milker_active = (r['b_launches_nb'] != r['a_launches_nb'])
        _wb_milker_active = (r['b_reengines'] != r['a_reengines'])
        _a_nb_label = f"NB Share ({v_ngsa_eis_year}+):"
        _a_wb_label = "WB Share (Full timeline):" if _wb_milker_active else f"WB Share ({v_a350_eis_year}+):"
        a_blocks.append(f"<tr><td><b>{_a_nb_label}</b></td><td class='val'>60% ➔ {r['a_eis_nb_sh']*100:.1f}%</td></tr>")
        a_blocks.append(f"<tr><td><b>{_a_wb_label}</b></td><td class='val'>{70/170*100:.1f}% ➔ {r['a_eis_wb_sh']*100:.1f}%</td></tr>")

        # ── RECURRING (Sales NPV deltas) ──
        a_blocks.append("<tr><td colspan='2' style='color:#58a6ff;font-size:10px;letter-spacing:1px;"
                        "padding:10px 0 4px 0;border-top:1px solid #222;'>"
                        "<b>RECURRING — Sales NPV Δ</b></td></tr>")
        a_blocks.append(f"<tr>"
                        f"<td style='border-bottom:none;'>NB Δ NPV (sales):</td>"
                        f"<td class='val' style='border-bottom:none;'>{format_val(r['a_delta_nb'])}</td></tr>")
        a_blocks.append(f"<tr><td colspan='2' style='padding:0 0 6px 24px;font-size:10px;"
                        f"color:#888;font-style:italic;border-bottom:1px solid #222;'>"
                        f"= ${r['a_scen_nb_pv']:.2f}B (scenario NPV) − ${BASE['a_base_nb']:.2f}B (baseline NPV)"
                        f"</td></tr>")
        a_blocks.append(f"<tr>"
                        f"<td style='border-bottom:none;'>WB Δ NPV (sales):</td>"
                        f"<td class='val' style='border-bottom:none;'>{format_val(r['a_delta_wb'])}</td></tr>")
        a_blocks.append(f"<tr><td colspan='2' style='padding:0 0 6px 24px;font-size:10px;"
                        f"color:#888;font-style:italic;border-bottom:1px solid #222;'>"
                        f"= ${r['a_scen_wb_pv']:.2f}B (scenario NPV) − ${BASE['a_base_wb']:.2f}B (baseline NPV)"
                        f"</td></tr>")

        # ── NON-RECURRING (NRE / CAPEX / debt / strain / fines) ──
        _nrec_a = (r['a_pv_nb_invest'] > 0 or r['a_pv_wb_invest'] > 0 or
                   r['a_pv_sabotage'] > 0 or r['a_tc_data']['delta_pen'] > 0 or
                   r['a_strain'] < 0 or r['a_delta_reg'] < 0)
        if _nrec_a:
            a_blocks.append("<tr><td colspan='2' style='color:#58a6ff;font-size:10px;letter-spacing:1px;"
                            "padding:10px 0 4px 0;border-top:1px solid #222;'>"
                            "<b>NON-RECURRING — Invest / Debt / Strain</b></td></tr>")
            if r['a_pv_nb_invest'] > 0:
                a_blocks.append(f"<tr><td>NB NRE + CAPEX (PV):</td><td class='val'>{format_val(-r['a_pv_nb_invest'])}</td></tr>")
            if r['a_pv_wb_invest'] > 0:
                a_blocks.append(f"<tr><td>WB NRE + CAPEX (PV):</td><td class='val'>{format_val(-r['a_pv_wb_invest'])}</td></tr>")
            if r['a_pv_sabotage'] > 0:
                _sab_lbl = "Sabotage Op (fps blunted)" if r['b_launches_nb'] else "Sabotage Op (naked — caught)"
                a_blocks.append(f"<tr><td>{_sab_lbl} (PV):</td><td class='val'>{format_val(-r['a_pv_sabotage'])}</td></tr>")
            if r['a_tc_data']['delta_pen'] > 0:
                a_blocks.append(f"<tr><td>Debt Penalty (Δ from new debt):</td>"
                                f"<td class='val'>{format_val(-r['a_tc_data']['delta_pen'])}</td></tr>")
            if r['a_delta_reg'] < 0:
                a_blocks.append(f"<tr><td>Regulatory Fine:</td><td class='val'>{format_val(r['a_delta_reg'])}</td></tr>")
            if r['a_strain'] < 0:
                a_blocks.append(f"<tr><td>Two-Front Strain:</td><td class='val'>{format_val(r['a_strain'])}</td></tr>")
        a_blocks.append(f"</table>")
        a_blocks.append(f"<hr style='border:1px solid #222;margin:8px 0;'>")
        a_col = '#3cb371' if r['a_total_delta'] >= 0 else '#ff4444'
        a_blocks.append(f"<b>Δ EV:</b> <span style='color:{a_col}'>${r['a_total_delta']:+.2f}B</span><br/>")
        a_blocks.append(f"<span style='color:#fff;font-size:15px;'><b>Yield: {r['yield_a']:.0f}%</b></span>")
        a_html = (
            f"<div class='delta-col col-a'>"
            f"<span class='player-a' style='font-size:14px;text-transform:uppercase;'>Airbus Strategic Deltas</span><br/>"
            f"<hr style='border:1px solid #222;margin:8px 0;'>"
            + "".join(a_blocks) +
            f"</div>"
        )

        # ----- Boeing column -----
        b_blocks = []
        b_blocks.append(f"<table class='math-breakdown-table'>")
        _b_nb_label = f"NB Share ({v_fps_eis_year}+):"
        _b_wb_label = "WB Share (Full timeline):" if _wb_milker_active else f"WB Share ({v_787_eis_year}+):"
        b_blocks.append(f"<tr><td><b>{_b_nb_label}</b></td><td class='val'>40% ➔ {r['b_eis_nb_sh']*100:.1f}%</td></tr>")
        b_blocks.append(f"<tr><td><b>{_b_wb_label}</b></td><td class='val'>{100/170*100:.1f}% ➔ {r['b_eis_wb_sh']*100:.1f}%</td></tr>")

        # ── RECURRING (Sales NPV deltas) ──
        b_blocks.append("<tr><td colspan='2' style='color:#58a6ff;font-size:10px;letter-spacing:1px;"
                        "padding:10px 0 4px 0;border-top:1px solid #222;'>"
                        "<b>RECURRING — Sales NPV Δ</b></td></tr>")
        b_blocks.append(f"<tr>"
                        f"<td style='border-bottom:none;'>NB Δ NPV (sales):</td>"
                        f"<td class='val' style='border-bottom:none;'>{format_val(r['b_delta_nb'])}</td></tr>")
        b_blocks.append(f"<tr><td colspan='2' style='padding:0 0 6px 24px;font-size:10px;"
                        f"color:#888;font-style:italic;border-bottom:1px solid #222;'>"
                        f"= ${r['b_scen_nb_pv']:.2f}B (scenario NPV) − ${BASE['b_base_nb']:.2f}B (baseline NPV)"
                        f"</td></tr>")
        b_blocks.append(f"<tr>"
                        f"<td style='border-bottom:none;'>WB Δ NPV (sales):</td>"
                        f"<td class='val' style='border-bottom:none;'>{format_val(r['b_delta_wb'])}</td></tr>")
        b_blocks.append(f"<tr><td colspan='2' style='padding:0 0 6px 24px;font-size:10px;"
                        f"color:#888;font-style:italic;border-bottom:1px solid #222;'>"
                        f"= ${r['b_scen_wb_pv']:.2f}B (scenario NPV) − ${BASE['b_base_wb']:.2f}B (baseline NPV)"
                        f"</td></tr>")

        # ── NON-RECURRING (NRE / CAPEX / debt / rate hike / strain) ──
        _nrec_b = (r['b_pv_nb_invest'] > 0 or r['b_pv_wb_invest'] > 0 or
                   r['b_tc_data']['delta_pen'] > 0 or r['b_pv_rate_hike'] < 0 or
                   r['b_strain'] < 0)
        if _nrec_b:
            b_blocks.append("<tr><td colspan='2' style='color:#58a6ff;font-size:10px;letter-spacing:1px;"
                            "padding:10px 0 4px 0;border-top:1px solid #222;'>"
                            "<b>NON-RECURRING — Invest / Debt / Strain</b></td></tr>")
            if r['b_pv_nb_invest'] > 0:
                b_blocks.append(f"<tr><td>NB NRE + CAPEX (PV):</td><td class='val'>{format_val(-r['b_pv_nb_invest'])}</td></tr>")
            if r['b_pv_wb_invest'] > 0:
                b_blocks.append(f"<tr><td>WB NRE + CAPEX (PV):</td><td class='val'>{format_val(-r['b_pv_wb_invest'])}</td></tr>")
            if r['b_pv_rate_hike'] < 0:
                b_blocks.append(f"<tr><td>737 Rate Hike (2032 PV):</td><td class='val'>{format_val(r['b_pv_rate_hike'])}</td></tr>")
            if r['b_tc_data']['delta_pen'] > 0:
                b_blocks.append(f"<tr><td>Debt Penalty (Δ from new debt):</td>"
                                f"<td class='val'>{format_val(-r['b_tc_data']['delta_pen'])}</td></tr>")
            if r['active_sabs'] > 0 and r['b_launches_nb']:
                b_blocks.append(f"<tr><td>Sabotage Damage (NB share, 5 yrs only):</td>"
                                f"<td class='val'>-{r['b_sab_shift']*100:.1f}%</td></tr>")
            if r['b_strain'] < 0:
                b_blocks.append(f"<tr><td>Two-Front Strain:</td><td class='val'>{format_val(r['b_strain'])}</td></tr>")
        b_blocks.append(f"</table>")
        b_blocks.append(f"<hr style='border:1px solid #222;margin:8px 0;'>")
        b_col = '#3cb371' if r['b_total_delta'] >= 0 else '#ff4444'
        b_blocks.append(f"<b>Δ EV:</b> <span style='color:{b_col}'>${r['b_total_delta']:+.2f}B</span><br/>")
        b_blocks.append(f"<span style='color:#fff;font-size:15px;'><b>Yield: {r['yield_b']:.0f}%</b></span>")
        b_html = (
            f"<div class='delta-col col-b'>"
            f"<span class='player-b' style='font-size:14px;text-transform:uppercase;'>Boeing Strategic Deltas</span><br/>"
            f"<hr style='border:1px solid #222;margin:8px 0;'>"
            + "".join(b_blocks) +
            f"</div>"
        )

        st.markdown(f"""
        <div class="nash-box" style="border-left:4px solid {bc};">
        <div class="{tc}">{title}</div>
        <div style="color:#ddd;margin-bottom:15px;font-size:13px;font-family:monospace;">
        <b>Airbus (A):</b> {clean_txt(a_m[0])} | {clean_txt(a_m[1])} | {clean_txt(a_m[2])} | {clean_txt(a_m[3])}<br/>
        <b>Boeing (B):</b> {clean_txt(b_m[0])} | {clean_txt(b_m[1])} | {clean_txt(b_m[2])}
        </div>
        <div class="delta-grid">{a_html}{b_html}</div>
        </div>""", unsafe_allow_html=True)

    # ── Collect & render ──
    near_nash_details = []
    for ai in range(total_rows):
        for ci in range(total_cols):
            cell = matrix_data[ai][ci]
            if cell['is_near_nash']:
                near_nash_details.append({
                    'a_strat': A_moves[ai], 'b_strat': B_moves[ci],
                    'row_idx': ai, 'col_idx': ci, 'result': cell
                })

    if not nash_equilibria_details and not near_nash_details:
        st.markdown("<div class='nash-box'><i>No Pure or Near-Nash Equilibria found. Adjust parameters.</i></div>",
                    unsafe_allow_html=True)
    else:
        for i, ne in enumerate(nash_equilibria_details):
            render_receipt(i, ne, True)
        for i, ne in enumerate(near_nash_details[:5]):   # cap near-nash at 5 to stay readable
            render_receipt(i, ne, False)

    # ============================================================
    # 8. PLAYER MOVE DICTIONARIES + ASSUMPTIONS
    # ============================================================
    st.markdown("---")
    st.markdown("### ♟️ Player Move Dictionaries")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='move-list-box'><span class='player-a'><b>Player A (Airbus)</b></span>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group A — NB Focus</b></div>", unsafe_allow_html=True)
        for i, m in enumerate(Airbus_Exclusivity_Groups['A']):
            st.markdown(f"<div class='move-item'>A{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group B/C — Sabotage (Delay fps)</b></div>", unsafe_allow_html=True)
        sab_moves = Airbus_Exclusivity_Groups['B'] + Airbus_Exclusivity_Groups['C']
        for i, m in enumerate(sab_moves):
            st.markdown(f"<div class='move-item'>S{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group WB — WB Focus</b></div>", unsafe_allow_html=True)
        for i, m in enumerate(Airbus_Exclusivity_Groups['WB']):
            st.markdown(f"<div class='move-item'>W{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='move-list-box'><span class='player-b'><b>Player B (Boeing)</b></span>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group A — NB Focus</b></div>", unsafe_allow_html=True)
        for i, m in enumerate(Boeing_Exclusivity_Groups['A']):
            st.markdown(f"<div class='move-item'>A{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group B — Production</b></div>", unsafe_allow_html=True)
        for i, m in enumerate(Boeing_Exclusivity_Groups['B']):
            st.markdown(f"<div class='move-item'>P{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='move-item' style='color:#58a6ff;margin-top:8px;'><b>Group WB — WB Focus</b></div>", unsafe_allow_html=True)
        for i, m in enumerate(Boeing_Exclusivity_Groups['WB']):
            st.markdown(f"<div class='move-item'>W{i+1}. {clean_txt(m)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Assumptions Box ──
    st.markdown("### 📋 Assumptions")
    st.markdown(f"""
    <div class="nash-box" style="font-size:13px;color:#ccc;">
    <b>1. Timeline:</b> 31-year dynamic DCF from 2026 → 2056. Narrowbody EIS: fps {v_fps_eis_year} / NGSA {v_ngsa_eis_year}. Widebody re-engine EIS: 787 {v_787_eis_year} / A350 {v_a350_eis_year}.<br/><br/>

    <b>2. Market Volumes (Annual):</b> 2,000 narrowbody a/c, 170 widebody a/c.<br/><br/>

    <b>3. Pricing ($B per a/c):</b> 737=${PRICE_737} | A320neo=${PRICE_A320} | fps=${PRICE_fps} | NGSA=${PRICE_NGSA} | Widebody=${PRICE_WB}<br/><br/>

    <b>4. Margins:</b>
    &nbsp;&nbsp;<span class='player-a'>Airbus: A320={v_margin_a320*100:.0f}% | NGSA={v_margin_angsa*100:.0f}% | A350={v_margin_a350*100:.0f}%</span><br/>
    &nbsp;&nbsp;<span class='player-b'>Boeing: 737={v_margin_737*100:.0f}% | fps={v_margin_fps*100:.0f}% | 787={v_margin_787*100:.0f}%</span><br/><br/>

    <b>5. WACC:</b> <span class='player-a'>Airbus {WACC_A*100:.1f}%</span> | <span class='player-b'>Boeing {WACC_B*100:.1f}%</span><br/><br/>

    <b>6. Status Quo Shares (Pre-EIS):</b>
    &nbsp;&nbsp;NB: Airbus 60% / Boeing 40%  |  WB: Airbus {70/170*100:.1f}% / Boeing {100/170*100:.1f}%<br/><br/>

    <b>7. Balance Sheets:</b>
    &nbsp;&nbsp;<span class='player-a'>Airbus EV=${v_ev_airbus:.0f}B | Debt=${v_debt_airbus:.0f}B</span><br/>
    &nbsp;&nbsp;<span class='player-b'>Boeing EV=${v_ev_boeing:.0f}B | Debt=${v_debt_boeing:.0f}B</span><br/><br/>

    <b>8. True Cost Penalty (α = {v_alpha}):</b> Δ Debt Penalty = Debt × α × (Debt/EV)². Applied as <i>marginal</i> penalty from new debt load.<br/><br/>

    <b>9. Nominal Tot Invest (CAPEX + NRE):</b>
    &nbsp;&nbsp;fps 7yr = ${v_capex_fps_7yr}B | fps 10yr = ${v_capex_fps_10yr}B | fps+Emb = ${v_capex_fps_emb}B | NGSA = ${v_capex_angsa}B<br/>
    &nbsp;&nbsp;787 Re-engine = ${v_capex_787_reengine}B | A350 Re-engine = ${v_capex_a350_reengine}B<br/>
    &nbsp;&nbsp;<b>Option B convention:</b> all CAPEX/NRE recognized as a single lump at each program's EIS year, then PV-discounted to 2026.
    NB lumps at <b>{v_fps_eis_year}</b> (fps) / <b>{v_ngsa_eis_year}</b> (NGSA);
    WB lumps at <b>{v_787_eis_year}</b> (787) / <b>{v_a350_eis_year}</b> (A350).<br/><br/>

    <b>10. Strain Cost:</b> <span class='player-a'>Airbus ${v_capex_strain_a}B</span> / <span class='player-b'>Boeing ${v_capex_strain_b}B</span>
    penalty when a player runs concurrent NB + WB development projects. PV-discounted to 2026 by the same time profile as the player's CAPEX.<br/><br/>

    <b>11. Sabotage Mechanics:</b>
    &nbsp;&nbsp;Each active sabotage move costs ${v_sabotage_cost}B (operational op cost, spread {max(2026, v_fps_eis_year-9)}–{v_fps_eis_year-1} — fps's build window).<br/>
    &nbsp;&nbsp;<b>If Boeing launches fps:</b> shifts {v_sabotage_share:.1f}% NB share per move to Airbus for 5 yrs from fps EIS ({v_fps_eis_year}).<br/>
    &nbsp;&nbsp;<b>If Boeing milks:</b> sabotage is <i>naked</i> → Airbus pays ${v_naked_sabotage_fine}B Regulatory Fine, PV-discounted to fps EIS year ({v_fps_eis_year}).<br/><br/>

    <b>12. 737 Rate Hike:</b> $2B cost in <b>2032</b> (fixed calendar year, EIS-independent) → +5% bonus NB share active <b>2032-2036</b> (5-yr ramp window). In Case A (neither launches) the +5pp persists all 31 yrs. Otherwise the boost expires in 2037 as EIS dynamics take over.<br/><br/>

    <b>13. fps 7-yr Ramp First-Mover Bonus:</b> the 7yr Solo variant captures
    +{v_fps_7yr_advantage:.1f}pp of NB share <b>for 10 years from fps EIS</b>
    ({v_fps_eis_year}-{v_fps_eis_year+9}) vs the 10yr Solo / via-Embraer
    variants. Reflects faster time-to-market locking in early customer
    commitments before NGSA matures. After the 10-yr first-mover window, fps and
    NGSA converge to the unified-rule baseline (50/50 in Both-Launch). The 10yr
    and Embraer variants pay a lower CAPEX but get baseline share only. Sabotage
    is applied <i>after</i> the bonus, so the 7yr variant is no more or less
    exposed to delay tactics than the 10yr variant in absolute pp terms.<br/><br/>

    <b>14. WB Re-engine — Status Quo Until EIS, then Catch-up:</b><br/>
    &nbsp;&nbsp;<b>Status quo persists until the first relevant EIS year.</b> No pre-EIS anticipation effect on shares (CAPEX still spends pre-EIS).<br/>
    &nbsp;&nbsp;<b>Only 787 re-engines (Airbus milks):</b> from {v_787_eis_year} (787 EIS) onward, Boeing gains <b>+{v_wb_b_capture_pp:.1f}pp/yr</b>, capped at <b>{(1-v_wb_milker_share)*100:.0f}%</b> (= 1 − Milker Share).<br/>
    &nbsp;&nbsp;<b>Only A350 re-engines (Boeing milks):</b> from {v_a350_eis_year} (A350 EIS) onward, Airbus gains <b>+{v_wb_a_capture_pp:.1f}pp/yr</b>, capped at <b>60%</b> (structural A350 ceiling — applies in both XOR and asymmetric cases).<br/>
    &nbsp;&nbsp;<b>Both re-engine, SAME year:</b> simultaneous launches cancel any first-mover advantage; status quo persists for all 31 years.<br/>
    &nbsp;&nbsp;<b>Both re-engine, 787 first:</b> from {v_787_eis_year} until {v_a350_eis_year}, Boeing gains <b>+{v_wb_b_capture_pp:.1f}pp/yr</b>, capped at <b>80%</b>. From {v_a350_eis_year} onward, share is frozen at the achieved level.<br/>
    &nbsp;&nbsp;<b>Both re-engine, A350 first:</b> from {v_a350_eis_year} until {v_787_eis_year}, Airbus gains <b>+{v_wb_a_capture_pp:.1f}pp/yr</b>, capped at <b>60%</b>. From {v_787_eis_year} onward, share is frozen.<br/>
    &nbsp;&nbsp;<b>Neither re-engines:</b> status quo persists for all 31 years.<br/><br/>

    <b>15. NB Launch — Status Quo → Phase 1 (cap 80%) → Phase 2 (balance 50/50):</b><br/>
    &nbsp;&nbsp;<b>Status quo persists until the relevant EIS year.</b> Starting status quo: Boeing 40% / Airbus 60%. <b>NO ANTICIPATION EFFECT.</b><br/>
    &nbsp;&nbsp;<b>Share-shift speeds (sliders):</b> Boeing capture <b>+{v_ramp7_b_pp:g}pp/yr</b> (7-yr ramp) / <b>+{v_ramp10_b_pp:g}pp/yr</b> (10-yr &amp; Embraer); Airbus Phase-2 recovery <b>+{v_ramp7_a_pp:g}</b> / <b>+{v_ramp10_a_pp:g}pp/yr</b>. The +4pp/+3pp figures below are the defaults; NGSA Phase-1 +3pp/yr is fixed.<br/>
    &nbsp;&nbsp;<b>Neither launches:</b> 40/60 for all 31 yrs (or <b>45/55 if 737 Rate Hike is active</b> — applies all 31 yrs in this case).<br/>
    &nbsp;&nbsp;<b>Both launch, SAME EIS year:</b> pre-EIS 40/60; from the shared EIS year, Phase 2 fires directly — Boeing climbs <b>+4pp/yr toward 50% balance</b> (treated as the limiting case of "Phase 1 length = 0", removes discontinuity with Cases C/D-both).<br/>
    &nbsp;&nbsp;<b>NGSA leads</b> (NGSA EIS before fps EIS, OR Boeing milks 737):<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Phase 1</b> from {v_ngsa_eis_year} (NGSA EIS): Airbus gains <b>+3pp/yr</b>, cap <b>80%</b>.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Phase 2</b> from {v_fps_eis_year} (fps EIS, only if Boeing also launches): Boeing climbs <b>+4pp/yr toward 50%</b>. Equilibrium balance is 50/50.<br/>
    &nbsp;&nbsp;<b>fps leads</b> (fps EIS before NGSA EIS, OR Airbus milks A320):<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Phase 1</b> from {v_fps_eis_year} (fps EIS): Boeing gains <b>+4pp/yr</b>, cap <b>80%</b>.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Phase 2</b> from {v_ngsa_eis_year} (NGSA EIS, only if Airbus also launches): Airbus climbs <b>+4pp/yr toward 50%</b>. <i>Edge case:</i> if Phase 1 was too short for fps to cross 50% (Airbus still above 50% at Phase 2 start), shares <b>freeze</b> at the Phase 1 final value.<br/>
    &nbsp;&nbsp;<b>Modifiers (stack additively on top of the catch-up share):</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>737 Rate Hike</b>: +5pp Boeing. In Case A (neither launches): all 31 yrs. Otherwise: <b>2032-2036 only</b> (fixed-calendar 5-yr ramp).<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>fps 7yr Ramp Bonus</b>: +{v_fps_7yr_advantage:.1f}pp Boeing, active <b>10 yrs from fps EIS only</b> ({v_fps_eis_year}-{v_fps_eis_year+9}); fades to 50/50 baseline afterward.<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• <b>Sabotage (Bottleneck / Poaching)</b>: FLAT −{v_sabotage_share:.1f}pp Boeing (1 OR 2 moves give the same effect — no stacking), active for <b>5 years from fps EIS</b> only. After the 5-yr disruption window, the shift expires and Boeing's share recovers per the unified rule. Only fires when Boeing launches fps; otherwise Naked Espionage Fine.<br/>
    &nbsp;&nbsp;<b>NB CAPEX (Option B):</b> recognized as a single lump at each program's EIS year ({v_fps_eis_year} for fps, {v_ngsa_eis_year} for NGSA), PV-discounted to 2026. Engine board's NB_EIS_T = min(fps, NGSA) − 2026 = {min(v_fps_eis_year, v_ngsa_eis_year) - 2026}.<br/><br/>

    <b>16. Player Exclusivity:</b> Moves with the same letter group are mutually exclusive (itertools.product).
    Airbus Group A: NGSA OR Milk. Group B: Bottleneck OR No. Group C: Poach OR No. Group WB: Re-engine OR Milk.
    Boeing Group A: fps variants OR Milk. Group B: Rate Hike OR No. Group WB: Re-engine OR Milk.<br/><br/>

    <b>17. Utility / Yield:</b> EV Yield % = 100 + (Total Δ EV / EV) × 100.
    ε-Near-Nash Tolerance: {v_tolerance:.1f}%.
    </div>
    """, unsafe_allow_html=True)

    # ── Strategic Impact Table (native streamlit to stay bug-free) ──
    st.markdown("### 📊 Move Assumptions & Mathematical Impact (2026 – 2056)")
    assumptions_data = [
        ["Airbus", "Launch NGSA", f"Lump at EIS ({v_ngsa_eis_year}), PV-discounted to 2026", "Dynamic", f"EIS {v_ngsa_eis_year}. NB Share dynamics depend on case: (NGSA leads, same EIS, NGSA follows). NGSA-leads: Phase 1 Airbus +3pp/yr cap 80% until fps EIS, then Phase 2 Boeing climbs +4pp/yr to 50/50 balance. SAME EIS year: Phase 2 from EIS directly (Boeing 40→50% at +4pp/yr — no Phase 1). NGSA-follows: enters as catcher in Phase 2 climbing +4pp/yr to 50% (frozen if Boeing was still below 50% at NGSA EIS)."],
        ["Airbus", "Milk A320neo", "$0.0B", "Dynamic", f"NB Share stays 60% unless Boeing launches fps. If Boeing launches → Phase 1 only: Boeing +4pp/yr cap 80% from fps EIS, Airbus drops toward 20%. No Phase 2 (NGSA never launches)."],
        ["Airbus", "Sabotage (Poach/Bottleneck)", f"${v_sabotage_cost}B per move spread {max(2026, v_fps_eis_year-9)}-{v_fps_eis_year-1} (op cost)", "N/A", f"FLAT {v_sabotage_share:.0f}pp NB share transferred from Boeing to Airbus (1 OR 2 sabotage moves give same effect — no stacking), active for 5 yrs from fps EIS only. Cost is still per-move (${v_sabotage_cost}B each). After 5 yrs the shift expires. ONLY IF Boeing launches fps. If Boeing milks → ${v_naked_sabotage_fine}B Naked Espionage Fine (PV-discounted to {v_fps_eis_year})."],
        ["Airbus", "Re-engine A350", f"Lump at EIS ({v_a350_eis_year}), PV-discounted to 2026", "Dynamic", f"EIS {v_a350_eis_year}. WB Share: status quo until A350 EIS, then Airbus +{v_wb_a_capture_pp:.1f}pp/yr (cap 60%). If Boeing also re-engines: same year → status quo; A350 EIS first → catch-up to 60% until 787 EIS; 787 EIS first → Boeing catches up first (+{v_wb_b_capture_pp:.1f}pp/yr cap 80%)."],
        ["Airbus", "Milk A350", "$0.0B", "Dynamic", f"WB Share: stays ~41% if Boeing also milks. If Boeing re-engines: status quo until {v_787_eis_year} (787 EIS), then Airbus loses share gradually as Boeing gains +{v_wb_b_capture_pp:.1f}pp/yr toward {(1-v_wb_milker_share)*100:.0f}%."],
        ["Boeing", "Launch fps 7yr Solo", f"Lump at EIS ({v_fps_eis_year}), PV-discounted to 2026", "Dynamic", f"EIS {v_fps_eis_year}. NB Share dynamics: fps-leads → Phase 1 Boeing +4pp/yr cap 80% until NGSA EIS, then Phase 2 Airbus climbs +4pp/yr to 50/50 (frozen if Phase 1 too short). Plus +{v_fps_7yr_advantage:.1f}pp 7yr ramp stacked for 10 yrs from fps EIS only ({v_fps_eis_year}-{v_fps_eis_year+9}); fades to baseline 50/50 afterward. Capture speed +{v_ramp7_b_pp:g}pp/yr / Airbus recovery +{v_ramp7_a_pp:g}pp/yr (7-yr ramp sliders). Fully exposed to Sabotage."],
        ["Boeing", "Launch fps 10yr Solo", f"Lump at EIS ({v_fps_eis_year}), PV-discounted to 2026", "Dynamic", f"EIS {v_fps_eis_year}. NB Share dynamics same as 7yr Solo but no ramp bonus. Phase 1 Boeing +4pp/yr cap 80% if fps leads, Phase 2 NGSA climbs to 50/50 if both launch. Capture speed +{v_ramp10_b_pp:g}pp/yr / Airbus recovery +{v_ramp10_a_pp:g}pp/yr (10-yr ramp sliders). Fully exposed to Sabotage."],
        ["Boeing", "Milk 737MAX", "$0.0B", "Dynamic", f"NB Share stays 40% unless Airbus launches NGSA. If Airbus launches → Phase 1 only: Airbus +3pp/yr cap 80% from NGSA EIS, Boeing drops toward 20%. No Phase 2 (fps never launches). 100% immune to Sabotage (Naked Espionage Fine fires instead)."],
        ["Boeing", "Increase 737 Rate", "$2.0B Cost applied in 2032 (fixed calendar)", "N/A", "+5pp Boeing NB share modifier. Case A (neither launches): active all 31 yrs (45/55). Otherwise: active 2032-2036 only (fixed-calendar 5-yr ramp, EIS-independent). Stacks additively on top of the catch-up trajectory."],
        ["Boeing", "Re-engine 787", f"Lump at EIS ({v_787_eis_year}), PV-discounted to 2026", "Dynamic", f"EIS {v_787_eis_year}. WB Share: status quo until 787 EIS, then Boeing +{v_wb_b_capture_pp:.1f}pp/yr (cap {(1-v_wb_milker_share)*100:.0f}% if Airbus milks; cap 80% if Airbus also re-engines and 787 EIS is first). Triggers Strain if paired with fps."],
    ]
    df_assumptions = pd.DataFrame(assumptions_data,
        columns=["Player", "Move", "Tot Invest (CAPEX + NRE)", "Price / Margin", "Strategic Impact Rule"])
    st.dataframe(df_assumptions, use_container_width=True, hide_index=True)


# ============================================================
# BOARD 2 — ENGINES (original Game_Board_Engines.py, untouched)
# ============================================================
def run_engine_board():

    # ============================================================
    # 0. AIRFRAMER → ENGINE BOARD LINK (NEW)
    # When the Airframer board's supplier choice changes, force-update
    # the Engine board's post-2037 NB share sliders and PW lock move.
    # ============================================================
    _b_sup = st.session_state.get("_b_supplier", "RR")
    _a_sup = st.session_state.get("_a_supplier", "PW")
    _b_code = SUPPLIER_CODE[_b_sup]
    _a_code = SUPPLIER_CODE[_a_sup]
    _b_share = st.session_state.get("_boeing_share_both", 50)
    _a_share = 100 - _b_share

    # Determine forced engine-player postures from the supplier matrix
    _all_engines = supplier_engines(_b_code) | supplier_engines(_a_code)
    _jv_active   = is_jv(_b_code) or is_jv(_a_code)

    if _jv_active:
        _forced_pw_move = "3-JV with RR for GTF"
    elif "PW" in _all_engines:
        _forced_pw_move = "2-Launch GTF2 Go Solo"
    else:
        _forced_pw_move = "1-Milk GTF"

    if "RR" not in _all_engines:
        _rr_posture = "Do Nothing (no airframer)"
    elif _jv_active:
        _rr_posture = "JV with PW for NB"
    else:
        _rr_posture = "Solo or Do Nothing"

    # Derived NB engine shares (user-set Boeing/Airbus split)
    _rr_pct, _pw_pct, _cfm_pct = derive_nb_engine_shares(_b_code, _a_code, _b_share)

    # Detect supplier or share change and force-update widget state BEFORE widgets render
    _seen = (st.session_state.get("_last_b_supp_seen"),
             st.session_state.get("_last_a_supp_seen"),
             st.session_state.get("_last_boeing_share_seen"))
    if _seen != (_b_sup, _a_sup, _b_share):
        st.session_state["f_cfm_nb"]      = int(round(_cfm_pct))
        st.session_state["f_pw_nb"]       = int(round(_pw_pct))
        st.session_state["f_rr_nb"]       = int(round(_rr_pct))
        st.session_state["_last_b_supp_seen"] = _b_sup
        st.session_state["_last_a_supp_seen"] = _a_sup
        st.session_state["_last_boeing_share_seen"] = _b_share

    # ============================================================
    # 1. PAGE CONFIGURATION & STRICT DARK THEME
    # ============================================================

    st.markdown("""
    <style>
    /* ── Strict Dark Theme ── */
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }

    /* ── Gameboard Table ── */
    .board-container { width: 100%; overflow: visible !important; margin-top: 20px; margin-bottom: 50px; background: #050505; border: 2px solid #333; border-radius: 8px; padding: 10px; overflow-x: auto; }
    .board-table { border-collapse: separate; border-spacing: 3px; font-family: 'Courier New', Courier, monospace; background-color: #000; width: 100%; min-width: 1200px; }

    .board-th-col { vertical-align: top; background-color: #1a0d00; border: 2px solid #ffffff; border-bottom: 3px solid #FFA500; outline: 1px solid #ffffff; outline-offset: 0; padding: 8px; text-align: center; font-size: 13px; color: #FFA500; position: sticky; top: 0; z-index: 10; }
    .board-th-row { vertical-align: top; background-color: #001a26; border: 2px solid #ffffff; border-right: 3px solid #00BFFF; border-bottom: 3px solid #00BFFF; outline: 1px solid #ffffff; outline-offset: 0; padding: 8px; text-align: left; font-size: 13px; color: #00BFFF; position: sticky; left: 0; z-index: 10; white-space: nowrap; }

    .board-td { background-color: #0a0a0a; border: 1px solid #222; padding: 3px 6px; text-align: center; vertical-align: middle; font-size: 13px; transition: all 0.2s ease-in-out; cursor: crosshair; position: relative; }
    .board-td:hover { background-color: #1f1f1f; transform: scale(1.05); z-index: 50; border: 1px solid #777; }

    /* ── Nash Equilibrium Styles ── */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0.7); }
        70% { box-shadow: 0 0 10px 5px rgba(60, 179, 113, 0); }
        100% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0); }
    }
    .nash-pure { border: 2px solid #3cb371 !important; background-color: #002b11 !important; font-weight: bold; animation: pulse-green 2s infinite; }
    .nash-near { border: 2px dashed #FFD700 !important; background-color: #2b2400 !important; }

    /* ── Hover Tooltip ── */
    .board-td .receipt-tooltip { visibility: hidden; width: 400px; background-color: #111; color: #fff; text-align: left; border: 1px solid #555; border-radius: 6px; padding: 12px; position: absolute; z-index: 999; bottom: 120%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.2s; box-shadow: 0px 10px 20px rgba(0,0,0,0.9); font-family: monospace; font-size: 11px; line-height: 1.4; pointer-events: none; }
    .board-td .receipt-tooltip::after { content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px; border-width: 5px; border-style: solid; border-color: #555 transparent transparent transparent; }
    .board-td:hover .receipt-tooltip { visibility: visible; opacity: 1; }

    /* ── Math Receipt Boxes ── */
    .nash-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 20px; font-family: monospace; }
    .nash-title { color: #58a6ff; font-size: 16px; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 15px; }
    .nash-title-pure { color: #3cb371; font-size: 16px; font-weight: bold; border-bottom: 1px solid #3cb371; padding-bottom: 10px; margin-bottom: 15px; }
    .nash-title-near { color: #FFD700; font-size: 16px; font-weight: bold; border-bottom: 1px solid #FFD700; padding-bottom: 10px; margin-bottom: 15px; }
    .delta-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
    .delta-col { background: #000; padding: 15px; border-radius: 4px; border-left: 3px solid; }

    /* ── Player Colours ── */
    .player-a { color: #00BFFF; font-weight: bold; }
    .player-b { color: #32CD32; font-weight: bold; }
    .player-c { color: #FFA500; font-weight: bold; }
    .col-a { border-color: #00BFFF; }
    .col-b { border-color: #32CD32; }
    .col-c { border-color: #FFA500; }

    /* ── Move Lists ── */
    .move-list-box { background: #111; padding: 15px; border-radius: 6px; border: 1px solid #333; height: 100%; }
    .move-item { font-size: 11px; color: #ccc; margin-bottom: 4px; font-family: monospace; }

    /* ── Breakdown Tables ── */
    .math-breakdown-table { width: 100%; font-size: 12px; color: #bbb; margin-bottom: 12px; border-collapse: collapse; }
    .math-breakdown-table td { padding: 6px 4px; border-bottom: 1px solid #222; }
    .math-breakdown-table .val { text-align: right; color: #fff; font-weight: bold; }

    /* ── Price Table ── */
    .price-tbl { width: 100%; border-collapse: collapse; font-size: 12px; color: #ccc; margin: 10px 0 20px 0; }
    .price-tbl th { background: #111; color: #58a6ff; padding: 8px; text-align: left; border-bottom: 2px solid #30363d; }
    .price-tbl td { padding: 6px 8px; border-bottom: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # 2. ENGINE PRICING — Regression (NB) + $140/lb Rule (WB)
    # ============================================================
    # Historical shipset (2-engine) price table for regression
    thrust_data    = np.array([8729, 9220, 12670, 13360, 13630, 18900, 23000, 14200, 20000, 25000], dtype=float)
    shipset_price  = np.array([4.7,  4.7,  5.0,   5.5,   5.5,   6.0,   7.1,   5.2,   7.0,   5.9],  dtype=float)
    engine_price_data = shipset_price / 2.0          # per-engine $M

    reg_slope, reg_intercept = np.polyfit(thrust_data, engine_price_data, 1)

    NB_THRUST = 30000       # NGSA / FPS next-gen narrowbody
    WB_THRUST = 80000       # Widebody class (GenX / Ultrafan)
    CPI       = 0.022       # 2.2 %

    # NB engine price from linear regression on historical thrust-price data
    NB_ENGINE_PRICE_M = float(reg_slope * NB_THRUST + reg_intercept)   # $M per engine

    # WB engine price from $140/lb-of-thrust industry rule
    # Regression data only covers up to 25k thrust — use $140/lb rule for 80k WB class
    WB_ENGINE_PRICE_M = float(WB_THRUST * 140 / 1_000_000)            # $M per engine

    ENGINES_PER_AC = 2
    NB_AC_PER_YR   = 2000   # 40 000 total / 20 yr
    WB_AC_PER_YR   = 170    # 3 400 total  / 20 yr

    # ── Default Market Shares (Pre-2037 Status Quo) ──
    # NB: 737 = LEAP-1B (CFM 100%) at 40% market = 40% CFM
    #     A320 = LEAP-1A (CFM 60%) + GTF (PW 40%) at 60% market
    #          = 36% CFM + 24% PW
    #     Total: CFM 76%, PW 24%, RR 0%
    # WB: GE 70% of 787 (60% mkt) + 0% of A350 (40% mkt) = 42% total ; RR = 58%
    DEF_CFM_NB, DEF_PW_NB, DEF_RR_NB = 0.76, 0.24, 0.00
    DEF_CFM_WB, DEF_PW_WB, DEF_RR_WB = 0.42, 0.00, 0.58

    # ============================================================
    # 3. STRATEGY DICTIONARIES (itertools.product + exclusivity)
    # ============================================================

    # ── Player A (CFM / GE) ─────────────────────────────────────
    #   Group A (mut-excl): 0-Do Nothing, 1-Open Fan, 2-Ducted, 3-Open+Ducted
    #   Group B: ∅, 4-Partner Embraer
    #   Group C: ∅, 5-Lobby Govts
    #   Group D: ∅, 6-Upgrade GenX9, 7-Invest GenX
    a_A = ["0-Milk LEAP", "1-Open Fan Only", "2-Ducted Only", "3-Open + Ducted"]
    a_B = ["", " | 4-Partner Embraer"]
    a_C = ["", " | 5-Lobby Govts"]
    a_D = ["", " | 6-Upgrade GenX9", " | 7-Invest GenX"]

    _a_all = list(itertools.product(a_A, a_B, a_C, a_D))
    _a_filt = []
    for ga, gb, gc, gd in _a_all:
        # Constraint: "0-Milk" cannot combine with "4-Partner Embraer"
        if "0-Milk" in ga and "4-Partner" in gb:
            continue
        _a_filt.append(f"{ga}{gb}{gc}{gd}")

    # Select 16 representative combos: 4 per base move
    player_a_moves = []
    for base in a_A:
        n = 0
        for m in _a_filt:
            if m.startswith(base) and n < 4:
                player_a_moves.append(m)
                n += 1
    N_A = len(player_a_moves)    # should be 16

    # ── Player C (Rolls-Royce) — base combo generation ──────────
    #   Group A (mut-excl NB strategy): 0-Do Nothing, 2-Ultrafan NB Solo, 3-JV PW NB
    #   Group B (mut-excl WB tech):     ∅, 1-Ultrafan WB, 4-Upgrade T1000
    c_A = ["0-Do Nothing (Milk WB)", "2-Ultrafan NB Solo", "3-JV with PW for NB"]
    c_B = ["", " | 1-Ultrafan WB", " | 4-Upgrade T1000"]

    # Strip the "(Milk WB)" editorial from the Group A label when a real
    # Group B WB action is appended — otherwise the concatenated header reads
    # like "Milk WB + Launch Ultrafan WB" which is self-contradictory.
    # The (Milk WB) annotation only stays when Group B is empty, where it is
    # actually accurate (RR sits out NB and sits out WB → milks legacy WB).
    _c_all_combos = [
        f"{ca if cb == '' else ca.replace(' (Milk WB)', '')}{cb}"
        for ca, cb in itertools.product(c_A, c_B)
    ]

    # ── Player B (Pratt & Whitney) — sidebar-selected ───────────
    #   All 3 moves are Group A (mutually exclusive — pick one)
    pw_combos = ["1-Milk GTF", "2-Launch GTF2 Go Solo", "3-JV with RR for GTF"]

    # ============================================================
    # 4. SIDEBAR CONTROLS
    # ============================================================
    st.sidebar.markdown("### ⚙️ Engine Market Parameters")

    eps_tol = st.sidebar.slider("ε-Nash Tolerance Yield (%)", 0.0, 10.0, value=2.0, step=0.5, key="en_eps_tol")
    gross_mult = st.sidebar.slider("Gross Multiplier (Engine Lifecycle NPV)", 1.0, 3.0, value=1.6, step=0.1, key="en_gross_mult",
                                    help="NPV_per_engine = (Price × Gross_Multiplier) × (1+CPI)^t")

    # Timeline is fixed at airframer-board cadence (2026-2056, T=31 years).
    # NB EIS is read from the airframer board's per-program sliders (default
    # 2037 each → t=11); we use min(fps, NGSA) so the engine NB share switch
    # syncs with the earlier NB platform launch. WB EIS likewise via min.
    TIMELINE_YRS = 31      # 2026..2056
    NPV_POST_EIS_YRS = 20   # Per-program window — pre-EIS legacy + 20 yrs post-EIS (Phase A)
    _b_nb_eis_yr = int(st.session_state.get('af_fps_eis',  2037))
    _a_nb_eis_yr = int(st.session_state.get('af_ngsa_eis', 2037))
    NB_EIS_T     = max(0, min(_b_nb_eis_yr, _a_nb_eis_yr) - 2026)
    _b_wb_eis_yr = int(st.session_state.get('af_787_eis',  2041))
    _a_wb_eis_yr = int(st.session_state.get('af_a350_eis', 2035))
    WB_EIS_T     = max(0, min(_b_wb_eis_yr, _a_wb_eis_yr) - 2026)
    N_YRS        = TIMELINE_YRS   # for backward-compat refs further down

    with st.sidebar.expander("📊 Balance Sheets ($B)", expanded=False):
        ev_a   = st.number_input("CFM/GE EV ($B)", value=160.0, step=5.0, key="en_ev_a")
        debt_a = st.number_input("CFM/GE Debt ($B)", value=35.0, step=5.0, key="en_debt_a")
        wacc_a = st.slider("CFM/GE WACC (%)", 5.0, 15.0, value=8.5, step=0.1, key="en_wacc_a") / 100
        st.divider()
        ev_b   = st.number_input("PW EV ($B)", value=110.0, step=5.0, key="en_ev_b")
        debt_b = st.number_input("PW Debt ($B)", value=40.0, step=5.0, key="en_debt_b")
        wacc_b = st.slider("PW WACC (%)", 5.0, 15.0, value=10.0, step=0.1, key="en_wacc_b") / 100
        st.divider()
        ev_c   = st.number_input("RR EV ($B)", value=110.0, step=5.0, key="en_ev_c")
        debt_c = st.number_input("RR Debt ($B)", value=40.0, step=5.0, key="en_debt_c")
        wacc_c = st.slider("RR WACC (%)", 5.0, 15.0, value=10.0, step=0.1, key="en_wacc_c") / 100

    with st.sidebar.expander("💰 Engine R&D ($B)", expanded=False):
        st.caption("R&D is CONDITIONAL — charged only when the corresponding "
                   "program is actually launched. Milk = no R&D charge.")
        st.caption("**CFM** (NB technology choice)")
        inv_cfm_open_fan_rd = st.number_input("CFM Open Fan R&D",  value=8.0, step=0.5, key="en_rd_cfm_open_fan",
            help="Charged only when CFM plays Open Fan Only or Open + Ducted. Milk LEAP → no charge.")
        inv_cfm_ducted_rd   = st.number_input("CFM Ducted Fan R&D", value=4.0, step=0.5, key="en_rd_cfm_ducted",
            help="Charged only when CFM plays Ducted Only or Open + Ducted. Milk LEAP → no charge.")
        st.divider()
        st.caption("**PW** (locked to one of Solo/JV/Milk by airframer supplier matrix)")
        inv_pw_gtf2_solo_rd = st.number_input("PW GTF2 Solo R&D",   value=2.0, step=0.5, key="en_rd_pw_solo",
            help="Charged only when PW is locked to Launch GTF2 Go Solo "
                 "(triggered when both airframers select PW solo).")
        inv_pw_gtf2_jv_rd   = st.number_input("PW GTF2 JV R&D",     value=2.0, step=0.5, key="en_rd_pw_jv",
            help="Charged only when PW is locked to JV with RR for GTF "
                 "(triggered when at least one airframer selects the JV supplier code).")
        st.divider()
        st.caption("**RR** (conditional per program)")
        inv_rr_rd_nb    = st.number_input("RR Ultrafan R&D — NB",  value=8.0, step=0.5, key="en_rd_rr_nb",
            help="Charged only when RR launches Ultrafan NB (Solo or JV with PW). "
                 "Do Nothing on NB → no charge.")
        inv_rr_rd_wb    = st.number_input("RR Ultrafan R&D — WB",  value=4.0, step=0.5, key="en_rd_rr_wb",
            help="Charged only when RR launches Ultrafan WB. "
                 "Milk Trent (no WB launch) → no charge.")
        inv_rr_t1000_rd = st.number_input("RR T1000 Upgrade R&D",  value=2.0, step=0.5, key="en_rd_rr_t1000",
            help="Charged only when RR selects Upgrade T1000 for the WB market.")

    with st.sidebar.expander("📈 Market Shifts & Costs", expanded=False):
        open_fan_loss  = st.slider("Open Fan Wait Penalty (CFM NB loss %)", 0, 100, 35, key="en_openfan_loss") / 100.0
        ducted_fan_gain = st.slider("Ducted Fan CFM NB Gain %", 0, 100, 10, key="en_ducted_gain") / 100.0
        lobby_cost     = st.number_input("Lobby Cost ($B) — Open Fan defensive move (caps loss at 20%)", value=2.0, step=0.5, key="en_lobby_cost")
        strain_penalty = st.number_input("Strain Cost ($B) — 2+ concurrent projects", value=2.0, step=0.5, key="en_strain_cost")
        rr_nbwb_strain = st.slider(
            "RR NB + WB Concurrent Strain ($B)",
            2.0, 10.0, 5.0, 0.5,
            key="en_rr_nbwb_strain",
            help="Additional strain charged to Rolls-Royce when its strategy "
                 "includes BOTH a narrowbody project (Ultrafan NB Solo or JV "
                 "with PW) AND a widebody project (Ultrafan WB or Upgrade "
                 "T1000) in the same scenario. Replaces the generic strain "
                 "penalty for RR's specific NB+WB concurrent case.",
        )

    # ── Player B (PW) is fully determined by Boeing's & Airbus's supplier choice
    # on the Airframer board; no user override is offered. The forced move is
    # computed at the top of this function (_forced_pw_move) and surfaced both
    # in the page banner and as `sel_pw` for downstream code paths.
    sel_pw = _forced_pw_move
    pw_jv_nb = ("3-JV with RR" in sel_pw)

    # ── Filter RR moves: remove JV option if PW didn't pick JV ──
    if pw_jv_nb:
        player_c_moves = _c_all_combos  # all 9 combos available
    else:
        player_c_moves = [m for m in _c_all_combos if "3-JV with PW" not in m]  # 6 combos
    N_C = len(player_c_moves)

    # ── Pre-2037 Status Quo Shares ──
    with st.sidebar.expander("📊 Pre-2037 Market (Status Quo)", expanded=False):
        st.caption("Baseline EV target — RR locked to 0% NB, PW locked to 0% WB.")
        st.markdown("**Narrowbody**")
        sq_cfm_nb = st.slider("CFM NB Base %", 0, 100, 76, key="sq_cfm_nb")
        sq_pw_nb  = st.slider("PW NB Base %",  0, 100, 24, key="sq_pw_nb")
        sq_rr_nb  = 0
        st.divider()
        st.markdown("**Widebody**")
        sq_cfm_wb = st.slider("CFM WB Base %", 0, 100, 42, key="sq_cfm_wb")
        sq_rr_wb  = st.slider("RR WB Base %",  0, 100, 58, key="sq_rr_wb")
        sq_pw_wb  = 0

    # ── Post-2037 Future Organic Start ──
    with st.sidebar.expander("🔮 Post-2037 Future Baseline", expanded=True):
        st.caption("Organic starting shares BEFORE game moves apply.")

        st.markdown("**Narrowbody**")
        fut_cfm_nb = st.slider("CFM NB Start %", 0, 100, 53, key="f_cfm_nb")
        if pw_jv_nb:
            # JV active → single combined slider, split 50/50
            jv_nb_default = 100  # default = PW+RR combined NB
            jv_nb_pct = st.slider("🤝 JV (PW+RR) NB Combined %", 0, 100, 100, key="f_jv_nb",
                                   help="PW and RR share this equally (50/50 split).")
            fut_pw_nb = jv_nb_pct / 2.0
            fut_rr_nb = jv_nb_pct / 2.0
            st.caption(f"→ PW: {fut_pw_nb:.0f}%  |  RR: {fut_rr_nb:.0f}%")
        else:
            fut_pw_nb  = st.slider("PW NB Start %",  0, 100, 50, key="f_pw_nb")
            fut_rr_nb  = st.slider("RR NB Start %",  0, 100, 50, key="f_rr_nb")

        st.divider()
        st.markdown("**Widebody**")
        fut_cfm_wb = st.slider("CFM WB Start %", 0, 100, 42, key="f_cfm_wb")
        fut_rr_wb  = st.slider("RR WB Start %",  0, 100, 58, key="f_rr_wb")
        fut_pw_wb  = 0  # PW has no WB moves

    # ── Normalise shares ──
    def norm3(a, b, c):
        t = a + b + c
        return (a/t, b/t, c/t) if t > 0 else (0, 0, 0)

    base_cfm_nb, base_pw_nb, base_rr_nb = norm3(sq_cfm_nb, sq_pw_nb, sq_rr_nb)
    base_cfm_wb, base_pw_wb, base_rr_wb = norm3(sq_cfm_wb, sq_pw_wb, sq_rr_wb)

    start_cfm_nb, start_pw_nb, start_rr_nb = norm3(fut_cfm_nb, fut_pw_nb, fut_rr_nb)
    start_cfm_wb, start_pw_wb, start_rr_wb = norm3(fut_cfm_wb, 0, fut_rr_wb)

    # ============================================================
    # 5. MATHEMATICAL ENGINE — NPV FORMULA (WITH Gross Multiplier)
    # ============================================================
    #   NPV_per_engine(t) = (Price × Gross_Multiplier) × (1+CPI)^t
    #   NPV_each_Year(t)  = Planes/yr × 2 Eng × Share × NPV_per_engine(t)
    #   NPV_Total         = Σ(t=0..N−1) NPV_each_Year(t) / (1+WACC)^t
    #   Straight DCF — no annuity factor
    # ============================================================
    def calc_npv(planes_yr, pre_eis_share, post_eis_share, eng_price_m, wacc, eis_t,
                 T=TIMELINE_YRS, cpi=CPI, apply_post_eis_window=True):
        """Return cumulative NPV in $B over the per-program 20-yr window.
        Shares switch from `pre_eis_share` to `post_eis_share` at year t = eis_t.
        Phase A rule: revenue is counted from t=0 through t = eis_t + 19
        (inclusive of EIS year, 20 yrs post-EIS). Pre-EIS legacy years are
        all included. Years beyond eis_t + 19 contribute zero.
        `apply_post_eis_window=False` disables the mask (used by legacy
        backward-compat wrappers that need the full T-year run).
        """
        if wacc <= 0 or eng_price_m <= 0:
            return 0.0
        if apply_post_eis_window:
            end_t = eis_t + NPV_POST_EIS_YRS - 1
            T_dyn = max(T, end_t + 1)  # ensures we cover late-EIS windows
        else:
            end_t = T - 1
            T_dyn = T
        total = 0.0
        for t in range(T_dyn):
            if t > end_t:
                continue
            share = pre_eis_share if t < eis_t else post_eis_share
            if share <= 0:
                continue
            npv_per_eng_t = (eng_price_m * gross_mult) * ((1 + cpi) ** t)
            cf_t = planes_yr * ENGINES_PER_AC * share * npv_per_eng_t
            pv_t = cf_t / ((1 + wacc) ** t)
            total += pv_t
        return total / 1000.0   # $M → $B

    def npv_player(pre_nb, post_nb, pre_wb, post_wb, wacc, T=TIMELINE_YRS):
        """Total NPV for one engine maker. NB runs 2026 through NB_EIS_T+19;
        WB runs 2026 through WB_EIS_T+19. Per-program 20-yr post-EIS windows."""
        return (calc_npv(NB_AC_PER_YR, pre_nb, post_nb, NB_ENGINE_PRICE_M, wacc, NB_EIS_T, T)
              + calc_npv(WB_AC_PER_YR, pre_wb, post_wb, WB_ENGINE_PRICE_M, wacc, WB_EIS_T, T))

    # Backward-compat wrappers retained for the Math Breakdown section's
    # legacy calls (one-share form, no EIS switching, no per-program window).
    def calc_npv_flat(planes_yr, share, eng_price_m, wacc, n, cpi=CPI):
        return calc_npv(planes_yr, share, share, eng_price_m, wacc,
                        eis_t=0, T=n, cpi=cpi, apply_post_eis_window=False)

    def base_npv_player(nb_share, wb_share, wacc, n):
        """Legacy single-share NPV (no EIS switching). Used by Math Breakdown."""
        return (calc_npv_flat(NB_AC_PER_YR, nb_share, NB_ENGINE_PRICE_M, wacc, n)
              + calc_npv_flat(WB_AC_PER_YR, wb_share, WB_ENGINE_PRICE_M, wacc, n))

    # ============================================================
    # 6. STATE SIMULATION
    # ============================================================
    def simulate(move_a, move_b, move_c, n):
        # ── Starting shares (post-2037 organic baseline) ──
        a_nb, a_wb = start_cfm_nb, start_cfm_wb
        b_nb, b_wb = start_pw_nb,  start_pw_wb
        c_nb, c_wb = start_rr_nb,  start_rr_wb

        inv_a, inv_b, inv_c = 0.0, 0.0, 0.0   # All R&D is conditional now
        str_a, str_b, str_c = 0.0, 0.0, 0.0

        # ── PLAYER A (CFM / GE) ──────────────────────────────────
        pa = 0  # project counter
        # Detect Open Fan / Ducted / Lobby (Lobby is Open Fan's defensive move)
        _has_open_fan = ("1-Open Fan" in move_a) or ("3-Open + Ducted" in move_a)
        _has_ducted   = ("2-Ducted"   in move_a) or ("3-Open + Ducted" in move_a)
        _has_lobby    = "5-Lobby Govts" in move_a
        _rr_nb_active = "Ultrafan NB" in move_c or "JV with PW" in move_c

        if _has_open_fan:
            pa += 1
            inv_a += inv_cfm_open_fan_rd   # Open Fan R&D — charged only on Open Fan launch
            # Open Fan not ready until 2045 → CFM loses NB share.
            # Lobby Govts caps the loss at 20% (defensive regulatory action).
            _of_loss = min(open_fan_loss, 0.20) if _has_lobby else open_fan_loss
            a_nb -= _of_loss
            if _rr_nb_active:
                b_nb += _of_loss / 2; c_nb += _of_loss / 2
            else:
                b_nb += _of_loss

        if _has_ducted:
            pa += 1
            inv_a += inv_cfm_ducted_rd     # Ducted Fan R&D — charged only on Ducted launch
            a_nb += ducted_fan_gain
            if _rr_nb_active:
                b_nb -= ducted_fan_gain / 2; c_nb -= ducted_fan_gain / 2
            else:
                b_nb -= ducted_fan_gain

        if "3-Open + Ducted" in move_a:
            pa += 1  # second project (Open Fan + Ducted is a 2-program portfolio)

        if "4-Partner Embraer" in move_a:
            pa += 1
            a_nb += 0.05  # new platform share gain

        if _has_lobby:
            pa += 1
            inv_a += lobby_cost  # $2B default — Open Fan defensive program
            # No standalone share effect: Lobby ONLY caps the Open Fan loss above.
            # If selected without Open Fan, Lobby is wasted spend (strictly dominated).

        if "6-Upgrade GenX9" in move_a:
            pa += 1
            a_wb += 0.05  # GenX stays competitive with Ultrafan

        if "7-Invest GenX" in move_a:
            pa += 1
            a_wb += 0.05

        if pa >= 2:
            str_a += strain_penalty

        # ── PLAYER B (PW) — 3 mutually exclusive NB moves ────────
        # PW's move is auto-locked by the airframer supplier matrix:
        # both airframers selecting PW solo → "2-Launch GTF2 Go Solo"; at
        # least one selecting the JV code → "3-JV with RR for GTF"; otherwise
        # "1-Milk GTF" (no R&D charge).
        pb = 0
        jv_nb_active = False   # Track if NB JV between PW & RR is active

        if "2-Launch GTF2" in move_b:
            pb += 1
            inv_b += inv_pw_gtf2_solo_rd   # Solo R&D — only on Solo launch
            b_nb += 0.10; a_nb -= 0.05; c_nb -= 0.05

        if "3-JV with RR" in move_b:
            pb += 1
            inv_b += inv_pw_gtf2_jv_rd     # JV R&D — only on JV launch
            jv_nb_active = True
            a_nb -= 0.10; b_nb += 0.05; c_nb += 0.05

        # (Move 1-Milk GTF has no effect — status quo, no R&D charge)

        if pb >= 2:
            str_b += strain_penalty

        # ── PLAYER C (RR) ────────────────────────────────────────
        pc = 0
        rr_has_nb_project = False
        rr_has_wb_project = False
        if "1-Ultrafan WB" in move_c:
            pc += 1
            rr_has_wb_project = True
            inv_c += inv_rr_rd_wb   # Ultrafan WB R&D — charged only on WB launch
            c_wb += 0.10; a_wb -= 0.10

        if "2-Ultrafan NB" in move_c:
            pc += 1
            rr_has_nb_project = True
            inv_c += inv_rr_rd_nb   # Ultrafan NB R&D — charged only on NB launch
            c_nb += 0.15; a_nb -= 0.10; b_nb -= 0.05

        if "3-JV with PW" in move_c:
            pc += 1
            rr_has_nb_project = True
            inv_c += inv_rr_rd_nb / 2.0   # RR's half of the JV NB R&D
            jv_nb_active = True     # RR side of NB JV
            c_nb += 0.05; b_nb += 0.05; a_nb -= 0.10

        if "4-Upgrade T1000" in move_c:
            pc += 1
            rr_has_wb_project = True
            inv_c += inv_rr_t1000_rd   # T1000 upgrade R&D (was hardcoded $2B)
            c_wb += 0.05; a_wb -= 0.05

        # RR strain: dedicated charge when RR runs concurrent NB + WB projects.
        # This replaces the generic strain_penalty for RR's specific case.
        # (For CFM and PW, the generic strain_penalty above continues to apply.)
        if rr_has_nb_project and rr_has_wb_project:
            str_c += rr_nbwb_strain

        # ── JV EQUALIZATION: force PW = RR NB share when JV is active ──
        if jv_nb_active:
            avg_nb = (b_nb + c_nb) / 2.0
            b_nb = avg_nb
            c_nb = avg_nb

        # ── Post-move share normalisation (floor at 0) ───────────
        a_nb, b_nb, c_nb = max(0, a_nb), max(0, b_nb), max(0, c_nb)
        a_wb, b_wb, c_wb = max(0, a_wb), max(0, b_wb), max(0, c_wb)
        t_nb = a_nb + b_nb + c_nb
        if t_nb > 0: a_nb /= t_nb; b_nb /= t_nb; c_nb /= t_nb
        t_wb = a_wb + b_wb + c_wb
        if t_wb > 0: a_wb /= t_wb; b_wb /= t_wb; c_wb /= t_wb

        # ── Base NPVs (Pre-2037 status-quo baseline — applies for ALL 31 yrs).
        # Same share both pre-EIS and post-EIS: "if nobody played any moves,
        # the status quo persists forever" — mirrors the airframer's BASE.
        base_a = npv_player(base_cfm_nb, base_cfm_nb, base_cfm_wb, base_cfm_wb, wacc_a)
        base_b = npv_player(base_pw_nb,  base_pw_nb,  base_pw_wb,  base_pw_wb,  wacc_b)
        base_c = npv_player(base_rr_nb,  base_rr_nb,  base_rr_wb,  base_rr_wb,  wacc_c)

        # ── New NPVs (post-move). Pre-EIS shares = status quo (sq_*); post-EIS
        # shares = the move-shifted (a_nb, b_nb, c_nb) / (a_wb, b_wb, c_wb).
        # Engine moves (Open Fan, Ultrafan NB, etc.) represent NEW PRODUCTS
        # that only enter at EIS, so pre-EIS the legacy market persists.
        new_a = npv_player(base_cfm_nb, a_nb, base_cfm_wb, a_wb, wacc_a)
        new_b = npv_player(base_pw_nb,  b_nb, base_pw_wb,  b_wb, wacc_b)
        new_c = npv_player(base_rr_nb,  c_nb, base_rr_wb,  c_wb, wacc_c)

        # ── Utility = (New − Base) − Strain − Investment ─────────
        u_a = new_a - base_a - str_a - inv_a
        u_b = new_b - base_b - str_b - inv_b
        u_c = new_c - base_c - str_c - inv_c

        # ── Enterprise Value Yield % = 100 + (ΔEV / EV) × 100 ───
        y_a = 100.0 + (u_a / max(0.1, ev_a)) * 100
        y_b = 100.0 + (u_b / max(0.1, ev_b)) * 100
        y_c = 100.0 + (u_c / max(0.1, ev_c)) * 100

        return {
            "A": dict(yield_pct=y_a, delta_b=u_a, base_b=base_a, strain_b=str_a, inv_b=inv_a,
                      nb_base=base_cfm_nb, nb_final=a_nb, wb_base=base_cfm_wb, wb_final=a_wb),
            "B": dict(yield_pct=y_b, delta_b=u_b, base_b=base_b, strain_b=str_b, inv_b=inv_b,
                      nb_base=base_pw_nb, nb_final=b_nb, wb_base=base_pw_wb, wb_final=b_wb),
            "C": dict(yield_pct=y_c, delta_b=u_c, base_b=base_c, strain_b=str_c, inv_b=inv_c,
                      nb_base=base_rr_nb, nb_final=c_nb, wb_base=base_rr_wb, wb_final=c_wb),
        }

    # ── Build 16×16 payoff matrix ──
    matrix = [[simulate(player_a_moves[a], sel_pw, player_c_moves[c], N_YRS)
               for c in range(N_C)] for a in range(N_A)]

    # ============================================================
    # 7. NASH EQUILIBRIUM SOLVER
    # ============================================================
    best_a_for_c = []
    for c in range(N_C):
        yields = [matrix[a][c]["A"]["yield_pct"] for a in range(N_A)]
        best_a_for_c.append(int(np.argmax(yields)))

    best_c_for_a = []
    for a in range(N_A):
        yields = [matrix[a][c]["C"]["yield_pct"] for c in range(N_C)]
        best_c_for_a.append(int(np.argmax(yields)))

    nash_pure, nash_near = [], []
    for a in range(N_A):
        for c in range(N_C):
            ya = matrix[a][c]["A"]["yield_pct"]
            yc = matrix[a][c]["C"]["yield_pct"]
            best_ya = matrix[best_a_for_c[c]][c]["A"]["yield_pct"]
            best_yc = matrix[a][best_c_for_a[a]]["C"]["yield_pct"]
            gap_a = best_ya - ya
            gap_c = best_yc - yc
            if gap_a <= 0.01 and gap_c <= 0.01:
                nash_pure.append((a, c))
            elif gap_a <= eps_tol and gap_c <= eps_tol:
                nash_near.append((a, c))

    # Persist a snapshot for the Summary tab
    _eng_nash_pairs = [(player_a_moves[a], player_c_moves[c],
                        matrix[a][c]["A"]["yield_pct"], matrix[a][c]["C"]["yield_pct"])
                       for (a, c) in nash_pure]
    _eng_near_nash_pairs = [(player_a_moves[a], player_c_moves[c],
                             matrix[a][c]["A"]["yield_pct"], matrix[a][c]["C"]["yield_pct"])
                            for (a, c) in nash_near]
    st.session_state["_en_nash_count"] = len(nash_pure)
    st.session_state["_en_near_nash_count"] = len(nash_near)
    st.session_state["_en_nash_pairs"] = _eng_nash_pairs
    st.session_state["_en_near_nash_pairs"] = _eng_near_nash_pairs
    st.session_state["_en_pw_locked_move"] = _forced_pw_move

    # ============================================================
    # 8. RENDER THE INTERACTIVE GAMEBOARD
    # ============================================================
    st.title("🎲 Aerospace Engine Gameboard — 3-Player Simulation")

    # ── Airframer-Linked Banner (NEW) ──
    # Reason text explaining WHY PW is locked to this move
    if _jv_active:
        _pw_reason = ("an airframer chose <b>RR & PW (JV)</b> — the JV is the "
                      "only viable PW posture")
    elif "PW" in _all_engines:
        _pw_reason = ("an airframer chose PW (solo, not JV) — PW must launch "
                      "GTF2 to fulfil the contract")
    else:
        _pw_reason = ("neither airframer selected PW — PW has no NB platform "
                      "to launch, only the existing GTF to milk")

    st.markdown(
        f"<div style='background:#0d1117;border:1px solid #30363d;border-left:4px solid #58a6ff;"
        f"border-radius:6px;padding:10px 14px;margin-bottom:10px;font-family:monospace;font-size:12px;color:#ddd;'>"
        f"🔌 <b>Auto-set from Airframer Board:</b> &nbsp;"
        f"<span class='player-a'>Boeing fps → {_b_sup} ({_b_share}%)</span> &nbsp;|&nbsp; "
        f"<span class='player-c'>Airbus NGSA → {_a_sup} ({_a_share}%)</span> &nbsp;|&nbsp; "
        f"<b>Code ({_b_code},{_a_code})</b><br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;Post-2037 NB shares synced → "
        f"<span class='player-a'>CFM {_cfm_pct:.0f}%</span> · "
        f"<span class='player-b'>PW {_pw_pct:.0f}%</span> · "
        f"<span class='player-c'>RR {_rr_pct:.0f}%</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── PW posture banner — replaces the former PW Lock selectbox ──
    st.markdown(
        f"<div style='background:#1a1100;border:1px solid #5a4a00;border-left:4px solid #FFD700;"
        f"border-radius:6px;padding:10px 14px;margin-bottom:10px;font-family:monospace;font-size:12px;color:#ddd;'>"
        f"♟️ <b><span class='player-b'>Player B (PW)</span> — locked move:</b> "
        f"<span style='color:#FFD700;font-weight:bold;'>{_forced_pw_move}</span><br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#888;font-style:italic;'>"
        f"Rationale: {_pw_reason}.</span><br/>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#888;font-style:italic;'>"
        f"<b><span class='player-c'>Player C (RR) posture:</span></b> {_rr_posture}.</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"**Board Context:** <span class='player-a'>Player A: CFM/GE (Rows)</span> vs "
        f"<span class='player-c'>Player C: Rolls-Royce (Columns)</span>.",
        unsafe_allow_html=True)

    # ============================================================
    # EQUILIBRIUM SUMMARY TABLE — unified 6-col table per player
    # ============================================================
    def _en_split_pipe(s):
        """Split an engine move string into (NB-side, WB-side) components.

        Engine players have multiple mutually-exclusive move groups:
          CFM (4 groups): NB tech (0-3) + NB partnership (4) + NB regulatory (5)
                          + WB tech (6-7). Only Group D is widebody.
          RR  (2 groups): NB launch (0,2,3) + WB tech (1,4). Group B is WB.

        Splitting on the first ' | ' is WRONG for CFM because it lumps all
        non-tech NB moves (partnerships, lobbying) into the WB column.

        This implementation classifies each pipe-separated piece by NAME,
        matching the four widebody move identifiers explicitly.
        """
        s = str(s).strip()
        if not s:
            return "", ""
        pieces = [p.strip() for p in s.split(" | ")]
        nb_pieces, wb_pieces = [], []
        # WB move identifiers across both engine players
        WB_NAMES = ("Upgrade GenX9", "Invest GenX",        # CFM Group D
                    "Ultrafan WB",   "Upgrade T1000")      # RR  Group B
        for p in pieces:
            if any(name in p for name in WB_NAMES):
                wb_pieces.append(p)
            else:
                nb_pieces.append(p)
        return " | ".join(nb_pieces), " | ".join(wb_pieces)

    def _en_move_with_eis(s):
        """Append '(EIS - YYYY)' suffix to an engine move label.
        NB engine moves use the earliest NB EIS (min fps/NGSA); WB engine
        moves use the earliest WB EIS (min 787/A350). Milk / Do Nothing
        returns unchanged."""
        if not s or "Milk" in s or "Do Nothing" in s:
            return s
        # WB engine moves
        if any(k in s for k in ("Upgrade GenX", "Ultrafan WB", "Upgrade T1000")):
            return f"{s} (EIS - {_en_wb_eis})"
        # NB engine moves (Open Fan / Ducted / Lobby / Sue PW / CFM Block /
        #                  Ultrafan NB Solo / JV with PW / GTF2 / Launch GTF)
        if any(k in s for k in ("Open Fan", "Ducted", "Lobby", "Sue PW",
                                  "CFM Block", "Ultrafan NB Solo", "JV with PW",
                                  "GTF2", "Launch")):
            return f"{s} (EIS - {_en_nb_eis})"
        return s

    # Earliest NB / WB EIS years across both airframer programs (governs
    # when an engine maker's product first ships).
    _en_nb_eis = min(_b_nb_eis_yr, _a_nb_eis_yr)
    _en_wb_eis = min(_b_wb_eis_yr, _a_wb_eis_yr)

    def _en_fmt_costs(items):
        nums = [c for _, c in items if c > 0]
        if not nums:
            return "0"
        if len(nums) == 1:
            return f"{nums[0]:.2f}"
        return " + ".join(f"{c:.2f}" for c in nums) + f" = {sum(nums):.2f}"

    # CFM
    def _cfm_nb_cost(m):
        items = []
        if "Open Fan" in m or "Open + Ducted" in m:
            items.append(("CFM Open Fan R&D", inv_cfm_open_fan_rd))
        if "Ducted" in m:  # matches "2-Ducted Only" and "3-Open + Ducted"
            items.append(("CFM Ducted Fan R&D", inv_cfm_ducted_rd))
        if "Lobby" in m:
            items.append(("Lobby cost", lobby_cost))
        return _en_fmt_costs(items)

    def _cfm_nb_impact(m):
        # Open Fan + Lobby caps the loss at 20%; otherwise full slider value.
        if "Open Fan" in m or "Open + Ducted" in m:
            _eff_loss = min(open_fan_loss, 0.20) if "Lobby" in m else open_fan_loss
            _lobby_note = " (Lobby caps loss at 20%)" if "Lobby" in m else ""
            base = f"−{_eff_loss*100:.0f}% NB share (Open Fan wait penalty){_lobby_note}"
            if "Open + Ducted" in m:
                base += f"; +{ducted_fan_gain*100:.0f}% Ducted gain (net {(ducted_fan_gain - _eff_loss)*100:+.0f}%)"
            return base
        if "Ducted" in m:      return f"+{ducted_fan_gain*100:.0f}% NB share (Ducted gain)"
        if "Sue PW" in m or "CFM Block" in m: return "Blocks PW entry → CFM captures PW's NB slot"
        if "Lobby" in m:       return f"WASTED ${lobby_cost:.0f}B (Lobby has no effect without Open Fan)"
        if "Milk LEAP" in m or "0-Milk" in m: return "Status quo NB engine share (no R&D charge)"
        if "Do Nothing" in m or "Milk" in m:  return "Status quo NB engine share"
        return "—"

    def _cfm_wb_cost(m):
        return _en_fmt_costs([])  # No explicit slider for CFM WB moves

    def _cfm_wb_impact(m):
        if "Milk" in m or "GenX" in m:   return "Legacy GenX share if Boeing milks 787"
        if "Upgrade GenX" in m:          return "Re-engined 787 captures CFM's WB slot"
        return "—"

    # PW (NB only — no WB platform)
    def _pw_nb_cost(m):
        items = []
        if "Launch GTF2 Go Solo" in m: items.append(("PW GTF2 Solo R&D", inv_pw_gtf2_solo_rd))
        if "JV with RR" in m:          items.append(("PW GTF2 JV R&D", inv_pw_gtf2_jv_rd))
        return _en_fmt_costs(items)

    def _pw_nb_impact(m):
        if "GTF2" in m or "Launch" in m: return "Captures PW's NB slot in post-EIS market"
        if "Milk" in m:                  return "Legacy GTF share — no new product"
        return "—"

    # RR
    def _rr_nb_cost(m):
        items = []
        if "Ultrafan NB Solo" in m: items.append(("RR Ultrafan R&D — NB", inv_rr_rd_nb))
        if "JV with PW" in m:       items.append(("RR share of NB JV R&D", inv_rr_rd_nb / 2.0))
        return _en_fmt_costs(items)

    def _rr_nb_impact(m):
        if "Ultrafan NB Solo" in m: return "Captures RR's NB slot from supplier matrix"
        if "JV with PW" in m:       return "RR + PW share NB slot 50/50 per JV terms"
        if "Do Nothing" in m:       return "No new NB product — RR sits out NB market (no NB R&D charge)"
        return "—"

    def _rr_wb_cost(m):
        items = []
        if "Ultrafan WB" in m:
            items.append(("RR Ultrafan R&D — WB", inv_rr_rd_wb))
            # Concurrent NB+WB strain when RR runs Ultrafan on both
            items.append(("Concurrent NB+WB strain", rr_nbwb_strain))
        if "Upgrade T1000" in m:
            items.append(("T1000 Upgrade R&D", inv_rr_t1000_rd))
        return _en_fmt_costs(items)

    def _rr_wb_impact(m):
        if "Ultrafan WB" in m:        return "Captures re-engined 787 WB engine slot"
        if "Upgrade T1000" in m:      return "Captures re-engined 787 via T1000 upgrade"
        if "Milk" in m or "Trent" in m: return "Status quo Trent share (A350 sole-source + 787 legacy)"
        return "—"

    # Collect moves from equilibria + count appearances
    _cfm_nb_pure = set(); _cfm_wb_pure = set()
    _rr_nb_pure  = set(); _rr_wb_pure  = set()
    _cfm_nb_pn_c = {}; _cfm_wb_pn_c = {}; _rr_nb_pn_c = {}; _rr_wb_pn_c = {}
    _cfm_nb_nn_c = {}; _cfm_wb_nn_c = {}; _rr_nb_nn_c = {}; _rr_wb_nn_c = {}
    def _e_inc(d, k): d[k] = d.get(k, 0) + 1
    for (a_str, c_str, _, _) in _eng_nash_pairs:
        cnb, cwb = _en_split_pipe(a_str)
        rnb, rwb = _en_split_pipe(c_str)
        k_cnb = _en_move_with_eis(cnb); k_cwb = _en_move_with_eis(cwb or "Milk GEnx")
        k_rnb = _en_move_with_eis(rnb or "Do Nothing"); k_rwb = _en_move_with_eis(rwb or "Milk Trent")
        _cfm_nb_pure.add(k_cnb); _cfm_wb_pure.add(k_cwb)
        _rr_nb_pure.add(k_rnb);  _rr_wb_pure.add(k_rwb)
        _e_inc(_cfm_nb_pn_c, k_cnb); _e_inc(_cfm_wb_pn_c, k_cwb)
        _e_inc(_rr_nb_pn_c, k_rnb);  _e_inc(_rr_wb_pn_c, k_rwb)
    _cfm_nb_all = set(_cfm_nb_pure); _cfm_wb_all = set(_cfm_wb_pure)
    _rr_nb_all  = set(_rr_nb_pure);  _rr_wb_all  = set(_rr_wb_pure)
    for (a_str, c_str, _, _) in _eng_near_nash_pairs:
        cnb, cwb = _en_split_pipe(a_str)
        rnb, rwb = _en_split_pipe(c_str)
        k_cnb = _en_move_with_eis(cnb); k_cwb = _en_move_with_eis(cwb or "Milk GEnx")
        k_rnb = _en_move_with_eis(rnb or "Do Nothing"); k_rwb = _en_move_with_eis(rwb or "Milk Trent")
        _cfm_nb_all.add(k_cnb); _cfm_wb_all.add(k_cwb)
        _rr_nb_all.add(k_rnb);  _rr_wb_all.add(k_rwb)
        _e_inc(_cfm_nb_nn_c, k_cnb); _e_inc(_cfm_wb_nn_c, k_cwb)
        _e_inc(_rr_nb_nn_c, k_rnb);  _e_inc(_rr_wb_nn_c, k_rwb)

    def _combined_en_table(players_data):
        """Render all engine players in ONE table with merged Player column.
        Each dict: name, klass, nb_set, nb_pure, nb_pn_c, nb_nn_c, nb_cost_fn,
        nb_impact_fn, wb_set, wb_pure, wb_pn_c, wb_nn_c, wb_cost_fn, wb_impact_fn,
        no_wb (bool)."""
        def _badge(m, pn_c, nn_c):
            pn = pn_c.get(m, 0); nn = nn_c.get(m, 0)
            parts = []
            if pn > 0: parts.append(f"<span style='color:#3cb371;font-weight:bold;'>⭐{pn}</span>")
            if nn > 0: parts.append(f"<span style='color:#FFD700;font-weight:bold;'>⚠️{nn}</span>")
            return ("&nbsp;" + " ".join(parts)) if parts else ""
        rows_html = []
        for idx, pd in enumerate(players_data):
            nb_list = sorted(pd['nb_set'])
            no_wb   = pd.get('no_wb', False)
            wb_list = sorted(pd['wb_set']) if not no_wb else []
            n = max(len(nb_list), len(wb_list), 1)
            top_border = "border-top:2px solid #58a6ff;" if idx > 0 else ""
            for i in range(n):
                row_cells = []
                if i == 0:
                    row_cells.append(
                        f"<td rowspan='{n}' class='{pd['klass']}' "
                        f"style='vertical-align:middle;padding:8px 10px;border:1px solid #30363d;"
                        f"{top_border}font-weight:bold;text-align:center;background:#161b22;"
                        f"font-size:13px;'>{pd['name']}</td>"
                    )
                row_top = top_border if i == 0 else ""
                # NB cells
                if i < len(nb_list):
                    m = nb_list[i]
                    lbl = (f"<b>{m}</b>" if m in pd['nb_pure'] else m) + _badge(m, pd['nb_pn_c'], pd['nb_nn_c'])
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;{row_top}'>{lbl}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;text-align:right;font-family:monospace;white-space:nowrap;{row_top}'>{pd['nb_cost_fn'](m)}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;max-width:240px;word-wrap:break-word;white-space:normal;line-height:1.35;{row_top}'>{pd['nb_impact_fn'](m)}</td>")
                else:
                    row_cells.extend([f"<td style='border:1px solid #30363d;{row_top}'></td>"] * 3)
                # WB cells
                if no_wb:
                    if i == 0:
                        row_cells.append(
                            f"<td colspan='3' rowspan='{n}' "
                            f"style='vertical-align:middle;padding:6px;border:1px solid #30363d;"
                            f"{top_border}color:#888;font-style:italic;text-align:center;'>(no WB platform)</td>"
                        )
                elif i < len(wb_list):
                    m = wb_list[i]
                    lbl = (f"<b>{m}</b>" if m in pd['wb_pure'] else m) + _badge(m, pd['wb_pn_c'], pd['wb_nn_c'])
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;{row_top}'>{lbl}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;text-align:right;font-family:monospace;white-space:nowrap;{row_top}'>{pd['wb_cost_fn'](m)}</td>")
                    row_cells.append(f"<td style='vertical-align:top;padding:6px 10px;border:1px solid #30363d;max-width:240px;word-wrap:break-word;white-space:normal;line-height:1.35;{row_top}'>{pd['wb_impact_fn'](m)}</td>")
                else:
                    row_cells.extend([f"<td style='border:1px solid #30363d;{row_top}'></td>"] * 3)
                rows_html.append("<tr>" + "".join(row_cells) + "</tr>")
        return f"""
<div style="margin-top:12px;">
  <table style="border-collapse:collapse;font-size:12px;color:#ddd;">
    <thead>
      <tr style="background:#161b22;">
        <th rowspan="2" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#1a1f36;text-align:center;min-width:100px;">Player</th>
        <th colspan="3" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#1a2332;text-align:center;">NB Mkt</th>
        <th colspan="3" style="border:1px solid #30363d;padding:6px;font-weight:bold;background:#2a1a1a;text-align:center;">WB Mkt</th>
      </tr>
      <tr style="background:#0d1117;">
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Move</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Costs ($B)</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Mkt Share Impact</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Move</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Costs ($B)</th>
        <th style="border:1px solid #30363d;padding:5px;text-align:center;">Mkt Share Impact</th>
      </tr>
    </thead>
    <tbody>{"".join(rows_html)}</tbody>
  </table>
</div>"""

    # PW (locked single move, NB only)
    _pw_set_all = {_en_move_with_eis(_forced_pw_move)} if (_eng_near_nash_pairs or _eng_nash_pairs) else set()
    _pw_set_pure = {_en_move_with_eis(_forced_pw_move)} if _eng_nash_pairs else set()

    # PW counts: PW plays the locked move in every equilibrium that exists
    _pw_key = _en_move_with_eis(_forced_pw_move)
    _pw_nb_pn_c = {_pw_key: len(_eng_nash_pairs)}      if _eng_nash_pairs      else {}
    _pw_nb_nn_c = {_pw_key: len(_eng_near_nash_pairs)} if _eng_near_nash_pairs else {}

    _en_summary_header_html = (
        f"#### 📋 Equilibrium summary — mutually exclusive moves "
        f"({len(_eng_nash_pairs)} Pure Nash · {len(_eng_near_nash_pairs)} Near-Nash) "
        f"&nbsp;·&nbsp; <i style='font-size:11px;'>each move shows "
        f"<span style='color:#3cb371;font-weight:bold;'>⭐N</span> Pure Nash and "
        f"<span style='color:#FFD700;font-weight:bold;'>⚠️N</span> Near-Nash appearance count</i>"
    )
    _en_combined_table_html = _combined_en_table([
        {'name': '🔵 CFM/GE', 'klass': 'player-a',
         'nb_set': _cfm_nb_all, 'nb_pure': _cfm_nb_pure,
         'nb_pn_c': _cfm_nb_pn_c, 'nb_nn_c': _cfm_nb_nn_c,
         'nb_cost_fn': _cfm_nb_cost, 'nb_impact_fn': _cfm_nb_impact,
         'wb_set': _cfm_wb_all, 'wb_pure': _cfm_wb_pure,
         'wb_pn_c': _cfm_wb_pn_c, 'wb_nn_c': _cfm_wb_nn_c,
         'wb_cost_fn': _cfm_wb_cost, 'wb_impact_fn': _cfm_wb_impact},
        {'name': '🟢 PW<br/><i style="font-size:10px;font-weight:normal;">(locked by airframer supplier matrix)</i>',
         'klass': 'player-b',
         'nb_set': _pw_set_all, 'nb_pure': _pw_set_pure,
         'nb_pn_c': _pw_nb_pn_c, 'nb_nn_c': _pw_nb_nn_c,
         'nb_cost_fn': _pw_nb_cost, 'nb_impact_fn': _pw_nb_impact,
         'wb_set': set(), 'wb_pure': set(),
         'wb_pn_c': {}, 'wb_nn_c': {},
         'wb_cost_fn': lambda m: "", 'wb_impact_fn': lambda m: "",
         'no_wb': True},
        {'name': '🟠 Rolls-Royce', 'klass': 'player-c',
         'nb_set': _rr_nb_all, 'nb_pure': _rr_nb_pure,
         'nb_pn_c': _rr_nb_pn_c, 'nb_nn_c': _rr_nb_nn_c,
         'nb_cost_fn': _rr_nb_cost, 'nb_impact_fn': _rr_nb_impact,
         'wb_set': _rr_wb_all, 'wb_pure': _rr_wb_pure,
         'wb_pn_c': _rr_wb_pn_c, 'wb_nn_c': _rr_wb_nn_c,
         'wb_cost_fn': _rr_wb_cost, 'wb_impact_fn': _rr_wb_impact},
    ])
    # Persist for the Summary tab to mirror at the top.
    st.session_state["_en_summary_header_html"] = _en_summary_header_html
    st.session_state["_en_combined_table_html"] = _en_combined_table_html

    st.markdown(_en_summary_header_html, unsafe_allow_html=True)
    st.markdown(_en_combined_table_html, unsafe_allow_html=True)

    # ── Diverging bar chart: 100% line in center, bars grow up/down from it ──
    # PX_PER computed dynamically from the global max |delta| across BOTH
    # CFM (blue) and RR (orange) yields → both colours share a single scale,
    # the largest |delta| exactly fills LINE_Y, and small deltas remain
    # visibly proportional instead of being clamped to the ceiling.
    BAR_H   = 80   # total container height in px
    LINE_Y  = 40   # 100% line position from top (center)
    _max_abs_delta = 0.5
    for _ai in range(N_A):
        for _ci in range(N_C):
            _d = matrix[_ai][_ci]
            _max_abs_delta = max(_max_abs_delta,
                                 abs(_d["A"]["yield_pct"] - 100.0),
                                 abs(_d["C"]["yield_pct"] - 100.0))
    PX_PER  = LINE_Y / _max_abs_delta

    def bar_div(val):
        """Return (height_px, is_above) for a diverging bar from 100%."""
        delta = val - 100.0
        px = max(2, min(LINE_Y, int(abs(delta) * PX_PER)))
        return px, (delta >= 0)

    def _en_nb_wb_split_html(move_str):
        """Render an engine player's move string as NB/WB sub-rows.
        Uses the same name-based split as _en_split_pipe."""
        s = str(move_str).strip()
        pieces = [p.strip() for p in s.split(" | ")] if s else []
        WB_NAMES = ("Upgrade GenX9", "Invest GenX", "Ultrafan WB", "Upgrade T1000")
        nb_pieces = [p for p in pieces if not any(n in p for n in WB_NAMES)]
        wb_pieces = [p for p in pieces if     any(n in p for n in WB_NAMES)]
        nb_html = "<br/>".join(nb_pieces) if nb_pieces else "—"
        wb_html = "<br/>".join(wb_pieces) if wb_pieces else "—"
        return (
            "<table style='border:none;border-collapse:collapse;width:100%;font-size:inherit;line-height:1.2;margin:0;'>"
            "<tr>"
            "<td style='border:none;padding:0 4px 0 0;text-align:left;font-weight:bold;font-size:16px;color:#58a6ff;width:32px;vertical-align:top;'>NB</td>"
            f"<td style='border:none;padding:0 0 0 4px;text-align:right;vertical-align:middle;'>{nb_html}</td>"
            "</tr>"
            "<tr>"
            "<td style='border:none;border-top:1px solid #555;padding:0 4px 0 0;text-align:left;font-weight:bold;font-size:16px;color:#ff7b72;width:32px;vertical-align:top;'>WB</td>"
            f"<td style='border:none;border-top:1px solid #555;padding:0 0 0 4px;text-align:right;vertical-align:middle;'>{wb_html}</td>"
            "</tr>"
            "</table>"
        )

    # ── Grouped-header CSS (engine board; scoped, existing styles untouched) ──
    st.markdown("""
    <style>
    .ehg { background:#1a0d00; border:1px solid #7f5a1f; color:#ffd9a0; font-weight:bold;
           text-align:center !important; vertical-align:middle !important; padding:7px 8px; line-height:1.25;
           font-family:'Courier New',Courier,monospace; font-size:13px; }
    .ehg-top { background:#23120a; color:#FFA500; font-size:16px; letter-spacing:1px;
               border-bottom:2px solid #FFA500; }
    .erg { background:#001a26; border:1px solid #1f5f7f; color:#9bd8ff; font-weight:bold;
           text-align:center !important; vertical-align:middle !important; padding:7px 9px; line-height:1.25;
           font-family:'Courier New',Courier,monospace; font-size:13px; }
    .erg-base { background:#04202e; color:#4cc6ff; font-size:16px; letter-spacing:1px;
                border-right:2px solid #00BFFF; }
    </style>
    """, unsafe_allow_html=True)

    # ── Gameboard with MERGED / GROUPED headers (mirrors the airframer board) ──
    # RR columns nest in 2 bands: NB strategy (Do Nothing / Ultrafan NB Solo /
    #   JV with PW) spanning its WB variants > WB tech leaf (milk / Ultrafan WB /
    #   Upgrade T1000). CFM rows nest in 2 levels: NB base tech (rowspan per
    #   group) > add-on leaf (— / Upgrade GenX9 / Invest GenX / Lobby Govts).
    # Grouping is derived from the move strings so it adapts to the 6-column
    #   (no JV) and 9-column (JV active) RR layouts automatically.

    def _en_base_of(m):
        """NB base of a move string: text before the first ' | ', numeric prefix stripped."""
        base = str(m).split(" | ")[0].strip()
        if len(base) > 2 and base[1] == "-" and base[0].isdigit():
            base = base[2:]
        return base

    def _en_addons_of(m):
        """Add-on pieces of a move string (everything after the base), prefixes stripped."""
        parts = [p.strip() for p in str(m).split(" | ")[1:]]
        out = []
        for p in parts:
            if len(p) > 2 and p[1] == "-" and p[0].isdigit():
                p = p[2:]
            out.append(p)
        return out

    # Group RR columns by consecutive equal NB base
    _rr_groups = []   # (base_label, n_cols)
    for cm in player_c_moves:
        _b = _en_base_of(cm).replace(" (Milk WB)", "")
        if _rr_groups and _rr_groups[-1][0] == _b:
            _rr_groups[-1][1] += 1
        else:
            _rr_groups.append([_b, 1])

    def _en_rr_wb_leaf(cm):
        adds = _en_addons_of(cm)
        for a in adds:
            if "Ultrafan WB" in a:  return "Ultrafan WB"
            if "Upgrade T1000" in a: return "Upgrade T1000"
        return "milk WB"

    def _en_cfm_leaf(am):
        adds = _en_addons_of(am)
        labs = []
        for a in adds:
            if "Upgrade GenX9" in a:   labs.append("Upgrade GenX9 (WB)")
            elif "Invest GenX" in a:   labs.append("Invest GenX (WB)")
            elif "Lobby Govts" in a:   labs.append("Lobby Govts")
            elif "Partner Embraer" in a: labs.append("Partner Embraer")
            else:                      labs.append(a)
        return "<br/>".join(labs) if labs else "—"

    html = ['<div class="board-container"><table class="board-table">']

    # Band 0 — corner (spans 2 header rows x 2 row-header cols) + RR NB strategy
    html.append('<tr>')
    html.append(
        '<th rowspan="2" colspan="2" style="background: linear-gradient(to top right, #001a26 49%, #ffffff 49%, #ffffff 51%, #1a0d00 51%); '
        'border: 2px solid #ffffff; position: relative; z-index: 20; min-width: 280px; height: 90px; padding: 0;">'
        '<span style="position: absolute; top: 8px; right: 10px; color: #FFA500; font-weight: bold; font-size: 14px; text-align: right; line-height: 1.15;">'
        '🟠 RR<br/><span style="font-size: 10px; font-weight: normal; color: #FFA500;">(columns →)</span></span>'
        '<span style="position: absolute; bottom: 8px; left: 10px; color: #00BFFF; font-weight: bold; font-size: 14px; text-align: left; line-height: 1.15;">'
        '🔵 CFM/GE<br/><span style="font-size: 10px; font-weight: normal; color: #00BFFF;">(↓ rows)</span></span>'
        '</th>'
    )
    for _gb, _gn in _rr_groups:
        html.append(f'<th class="ehg ehg-top" colspan="{_gn}" style="text-align:center;vertical-align:middle;">{_gb}</th>')
    html.append('</tr>')

    # Band 1 — WB tech leaf (one cell per data column; sets column width)
    html.append('<tr>')
    for cm in player_c_moves:
        html.append(f'<th class="ehg" style="min-width:94px;">{_en_rr_wb_leaf(cm)}</th>')
    html.append('</tr>')

    # ── Data rows with nested (rowspan) CFM row headers ──
    # player_a_moves is built as 4 consecutive variants per NB base, so a new
    # base group starts whenever the base label changes.
    for ai, am in enumerate(player_a_moves):
        html.append('<tr>')
        _base = _en_base_of(am)
        if ai == 0 or _en_base_of(player_a_moves[ai - 1]) != _base:
            _span = 1
            for _j in range(ai + 1, N_A):
                if _en_base_of(player_a_moves[_j]) == _base:
                    _span += 1
                else:
                    break
            html.append(f'<th class="erg erg-base" rowspan="{_span}" style="min-width:130px;">{_base}</th>')
        html.append(f'<th class="erg" style="min-width:150px;">{_en_cfm_leaf(am)}</th>')
        for ci in range(N_C):
            cls = "board-td"
            icon = ""
            if (ai, ci) in nash_pure:   cls += " nash-pure"; icon = "⭐ "
            elif (ai, ci) in nash_near:  cls += " nash-near"; icon = "⚠️ "

            d = matrix[ai][ci]
            ay, cy, by_ = d["A"]["yield_pct"], d["C"]["yield_pct"], d["B"]["yield_pct"]
            ad, bd, cd  = d["A"]["delta_b"],   d["B"]["delta_b"],   d["C"]["delta_b"]

            px_a, up_a = bar_div(ay)
            px_c, up_c = bar_div(cy)

            # Bright above 100%, dim below
            col_a = "#00BFFF" if up_a else "#006080"
            col_c = "#FFA500" if up_c else "#805300"

            # Position: above line → bottom of bar touches line; below → top touches line
            if up_a:
                style_a = f"position:absolute;bottom:{BAR_H - LINE_Y}px;width:28px;height:{px_a}px;background:{col_a};border-radius:2px 2px 0 0;"
            else:
                style_a = f"position:absolute;top:{LINE_Y}px;width:28px;height:{px_a}px;background:{col_a};border-radius:0 0 2px 2px;"

            if up_c:
                style_c = f"position:absolute;bottom:{BAR_H - LINE_Y}px;width:28px;height:{px_c}px;background:{col_c};border-radius:2px 2px 0 0;"
            else:
                style_c = f"position:absolute;top:{LINE_Y}px;width:28px;height:{px_c}px;background:{col_c};border-radius:0 0 2px 2px;"

            bars = (
                f'<div style="position:relative;height:{BAR_H}px;margin:0 auto;width:80px;">'
                # 100% reference line
                f'<div style="position:absolute;top:{LINE_Y}px;left:0;right:0;'
                f'border-top:1px solid rgba(255,255,255,0.35);z-index:2;"></div>'
                # Bar A (left)
                f'<div style="{style_a}left:8px;" title="CFM: {ay:.0f}%"></div>'
                # Bar C (right)
                f'<div style="{style_c}right:8px;" title="RR: {cy:.0f}%"></div>'
                f'</div>'
                # Numbers below
                f'<div style="font-size:16px;line-height:1.0;margin-top:2px;text-align:center;font-weight:bold;">'
                f'<span class="player-a">{ay:.0f}</span>'
                f' '
                f'<span class="player-c">{cy:.0f}</span></div>'
            )

            # NPV revenue window — engine NPV now synced to the airframer
            # board's 2026-2056 timeline (T=31 yrs), with NB EIS at 2037
            # and WB re-engine EIS at 2035.
            _yr_range = "2026–2056"

            tip = (
                f"<div class='receipt-tooltip'>"
                f"<div style='border-bottom:1px solid #444;margin-bottom:8px;color:#FFD700;font-weight:bold;'>"
                f"TACTICAL MATH RECEIPT (T={TIMELINE_YRS}yrs)</div>"
                f"<div style='margin-bottom:8px;'><b>CFM:</b> {am}<br/>"
                f"<b>PW:</b> {sel_pw}<br/><b>RR:</b> {player_c_moves[ci]}</div>"
                f"<span class='player-a'>[A] CFM Yield: {ay:.0f}% (Δ ${ad:+.2f}B, {_yr_range})</span><br/>"
                f"<span class='player-b'>[B] PW  Yield: {by_:.0f}% (Δ ${bd:+.2f}B, {_yr_range})</span><br/>"
                f"<span class='player-c'>[C] RR  Yield: {cy:.0f}% (Δ ${cd:+.2f}B, {_yr_range})</span>"
                f"</div>"
            )
            html.append(f'<td class="{cls}"><span style="position:absolute;top:2px;left:3px;font-size:13px;line-height:1;z-index:5;">{icon}</span>{bars}{tip}</td>')
        html.append('</tr>')
    html.append('</table></div>')
    st.markdown("".join(html), unsafe_allow_html=True)

    # ============================================================
    # 9. GAME MATH BREAKDOWN — Baseline & Nash Receipts
    # ============================================================
    st.markdown("---")
    st.title("🧮 Game Math Breakdown & Nash Receipts")

    # ── Baseline Status Quo Box ──
    bA = base_npv_player(base_cfm_nb, base_cfm_wb, wacc_a, N_YRS)
    bB = base_npv_player(base_pw_nb,  base_pw_wb,  wacc_b, N_YRS)
    bC = base_npv_player(base_rr_nb,  base_rr_wb,  wacc_c, N_YRS)

    bA_nb = calc_npv_flat(NB_AC_PER_YR, base_cfm_nb, NB_ENGINE_PRICE_M, wacc_a, N_YRS)
    bA_wb = calc_npv_flat(WB_AC_PER_YR, base_cfm_wb, WB_ENGINE_PRICE_M, wacc_a, N_YRS)
    bB_nb = calc_npv_flat(NB_AC_PER_YR, base_pw_nb,  NB_ENGINE_PRICE_M, wacc_b, N_YRS)
    bB_wb = calc_npv_flat(WB_AC_PER_YR, base_pw_wb,  WB_ENGINE_PRICE_M, wacc_b, N_YRS)
    bC_nb = calc_npv_flat(NB_AC_PER_YR, base_rr_nb,  NB_ENGINE_PRICE_M, wacc_c, N_YRS)
    bC_wb = calc_npv_flat(WB_AC_PER_YR, base_rr_wb,  WB_ENGINE_PRICE_M, wacc_c, N_YRS)

    npv_eng_nb_0 = NB_ENGINE_PRICE_M * gross_mult                                      # Year 0
    npv_eng_nb_N = (NB_ENGINE_PRICE_M * gross_mult) * ((1+CPI)**(max(1,N_YRS)-1))      # Last year
    npv_eng_wb_0 = WB_ENGINE_PRICE_M * gross_mult
    npv_eng_wb_N = (WB_ENGINE_PRICE_M * gross_mult) * ((1+CPI)**(max(1,N_YRS)-1))

    st.markdown(f"""
    <div class="nash-box">
    <div class="nash-title" style="color:#58a6ff;">🏛️ Baseline Status Quo Breakdown</div>

    <table class="math-breakdown-table" style="font-size:13px;color:#ddd;width:100%;">
        <tr><td colspan="4" style="border-bottom:1px solid #444;color:#58a6ff;font-weight:bold;padding-bottom:5px;">
            1. PRE-2037 STATUS QUO SHARES</td></tr>
        <tr>
            <td style="padding:8px;"><b>NB Market:</b> 40k planes</td>
            <td style="padding:8px;"><span class="player-a">CFM: {base_cfm_nb*100:.0f}%</span></td>
            <td style="padding:8px;"><span class="player-b">PW: {base_pw_nb*100:.0f}%</span></td>
            <td style="padding:8px;"><span class="player-c">RR: {base_rr_nb*100:.0f}%</span></td>
        </tr>
        <tr>
            <td style="padding:8px;"><b>WB Market:</b> 3.4k planes</td>
            <td style="padding:8px;"><span class="player-a">CFM: {base_cfm_wb*100:.0f}%</span></td>
            <td style="padding:8px;"><span class="player-b">PW: {base_pw_wb*100:.0f}%</span></td>
            <td style="padding:8px;"><span class="player-c">RR: {base_rr_wb*100:.0f}%</span></td>
        </tr>
        <tr><td colspan="4" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            2. ENGINE PRICING & gross_mult NPV (×{gross_mult})</td></tr>
        <tr>
            <td colspan="2" style="padding:8px;"><b>NB Price (Regression):</b> ${NB_ENGINE_PRICE_M:.2f}M &nbsp;→&nbsp; <b>×{gross_mult} =</b> ${NB_ENGINE_PRICE_M*gross_mult:.2f}M</td>
            <td colspan="2" style="padding:8px;"><b>WB Price ($140/lb):</b> ${WB_ENGINE_PRICE_M:.2f}M &nbsp;→&nbsp; <b>×{gross_mult} =</b> ${WB_ENGINE_PRICE_M*gross_mult:.2f}M</td>
        </tr>
        <tr>
            <td colspan="2" style="padding:8px;"><b>NB NPV/Eng (t=0):</b> ${npv_eng_nb_0:.2f}M &nbsp;→&nbsp; <b>(t={max(1,N_YRS)-1}):</b> ${npv_eng_nb_N:.2f}M</td>
            <td colspan="2" style="padding:8px;"><b>WB NPV/Eng (t=0):</b> ${npv_eng_wb_0:.2f}M &nbsp;→&nbsp; <b>(t={max(1,N_YRS)-1}):</b> ${npv_eng_wb_N:.2f}M</td>
        </tr>
        <tr><td colspan="4" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            3. DCF DISCOUNTING PARAMETERS</td></tr>
        <tr>
            <td style="padding:8px;"><b>N:</b> {N_YRS} yrs</td>
            <td style="padding:8px;"><span class="player-a">WACC: {wacc_a*100:.1f}%</span></td>
            <td style="padding:8px;"><span class="player-b">WACC: {wacc_b*100:.1f}%</span></td>
            <td style="padding:8px;"><span class="player-c">WACC: {wacc_c*100:.1f}%</span></td>
        </tr>
        <tr>
            <td colspan="4" style="padding:8px;color:#aaa;font-size:11px;">
                <b>Formula (×{gross_mult:.1f} Gross Multiplier — Straight DCF):</b><br/>
                NPV_per_engine(t) = (Price × {gross_mult:.1f}) × (1+CPI)^t &nbsp;|&nbsp;
                NPV_each_Year(t) = Planes × 2 × Share × NPV_per_engine(t) &nbsp;|&nbsp;
                NPV_Total = Σ(t=0..N−1) NPV_each_Year(t) / (1+WACC)^t
            </td>
        </tr>
        <tr><td colspan="4" style="border-bottom:1px solid #444;padding-top:15px;color:#58a6ff;font-weight:bold;">
            4. BALANCE SHEETS</td></tr>
        <tr>
            <td style="padding:8px;"></td>
            <td style="padding:8px;"><span class="player-a">EV: ${ev_a:.0f}B | Debt: ${debt_a:.0f}B</span></td>
            <td style="padding:8px;"><span class="player-b">EV: ${ev_b:.0f}B | Debt: ${debt_b:.0f}B</span></td>
            <td style="padding:8px;"><span class="player-c">EV: ${ev_c:.0f}B | Debt: ${debt_c:.0f}B</span></td>
        </tr>
    </table>

    <div class="delta-grid" style="border-top:1px solid #30363d;padding-top:20px;">
        <div class="delta-col col-a">
            <span class="player-a">Player A (CFM/GE) Base</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
                <tr><td><b>NB NPV:</b></td><td class="val">${bA_nb:.2f}B</td></tr>
                <tr><td><b>WB NPV:</b></td><td class="val">${bA_wb:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Total Base NPV:</b> <span class="player-a" style="float:right;font-size:16px;">${bA:.2f}B</span>
        </div>
        <div class="delta-col col-b">
            <span class="player-b">Player B (PW) Base</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
                <tr><td><b>NB NPV:</b></td><td class="val">${bB_nb:.2f}B</td></tr>
                <tr><td><b>WB NPV:</b></td><td class="val">${bB_wb:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Total Base NPV:</b> <span class="player-b" style="float:right;font-size:16px;">${bB:.2f}B</span>
        </div>
        <div class="delta-col col-c">
            <span class="player-c">Player C (RR) Base</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
                <tr><td><b>NB NPV:</b></td><td class="val">${bC_nb:.2f}B</td></tr>
                <tr><td><b>WB NPV:</b></td><td class="val">${bC_wb:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Total Base NPV:</b> <span class="player-c" style="float:right;font-size:16px;">${bC:.2f}B</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nash Equilibrium Receipt Renderer ──
    def render_receipt(idx, a, c, is_pure):
        d = matrix[a][c]
        title = f"⭐ Pure Nash #{idx+1}" if is_pure else f"⚠️ Near-Nash #{idx+1}"
        bc = "#3cb371" if is_pure else "#FFD700"
        tc = "nash-title-pure" if is_pure else "nash-title-near"

        blocks = []
        for key, label, pclass, cclass in [("A","CFM/GE","player-a","col-a"),
                                            ("B","PW","player-b","col-b"),
                                            ("C","RR","player-c","col-c")]:
            p = d[key]
            col = '#3cb371' if p['delta_b'] >= 0 else '#ff4444'
            blocks.append(f"""
            <div class="delta-col {cclass}">
            <span class="{pclass}" style="font-size:14px;text-transform:uppercase;">Player {key} ({label}) Delta</span><br/>
            <hr style="border:1px solid #222;margin:8px 0;">
            <table class="math-breakdown-table">
            <tr><td><b>NB Share:</b></td><td class="val">{p['nb_base']*100:.0f}% ➔ {p['nb_final']*100:.0f}%</td></tr>
            <tr><td><b>WB Share:</b></td><td class="val">{p['wb_base']*100:.0f}% ➔ {p['wb_final']*100:.0f}%</td></tr>
            <tr><td><b>R&D / Sunk CAPEX:</b></td><td class="val" style="color:#ff6666;">-${p['inv_b']:.2f}B</td></tr>
            <tr><td style="border-bottom:none;"><b>Strain Cost:</b></td>
                <td class="val" style="border-bottom:none;color:#ff6666;">-${p['strain_b']:.2f}B</td></tr>
            </table>
            <hr style="border:1px solid #222;margin:8px 0;">
            <b>Δ EV:</b> <span style="color:{col}">${p['delta_b']:+.2f}B</span><br/>
            <span style="color:#fff;font-size:15px;"><b>Yield: {p['yield_pct']:.0f}%</b></span>
            </div>""")

        st.markdown(f"""
        <div class="nash-box" style="border-left:4px solid {bc};">
        <div class="{tc}">{title}</div>
        <div style="color:#ddd;margin-bottom:15px;font-size:13px;font-family:monospace;">
        <b>A (CFM/GE):</b> {player_a_moves[a]}<br/>
        <b>B (PW):</b> {sel_pw}<br/>
        <b>C (RR):</b> {player_c_moves[c]}
        </div>
        <div class="delta-grid">{"".join(blocks)}</div>
        </div>""", unsafe_allow_html=True)

    if not nash_pure and not nash_near:
        st.markdown("<div class='nash-box'><i>No Pure or Near-Nash Equilibria found. Adjust parameters.</i></div>",
                    unsafe_allow_html=True)
    else:
        for i, (a, c) in enumerate(nash_pure):
            render_receipt(i, a, c, True)
        for i, (a, c) in enumerate(nash_near):
            if (a, c) not in nash_pure:
                render_receipt(i, a, c, False)

    # ============================================================
    # 10. PLAYER MOVES, ASSUMPTIONS, ENGINE PRICES
    # ============================================================
    st.markdown("---")
    st.markdown("### ♟️ Player Move Dictionaries")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='move-list-box'><span class='player-a'><b>Player A (CFM/GE)</b></span>", unsafe_allow_html=True)
        for i, m in enumerate(player_a_moves):
            st.markdown(f"<div class='move-item'>{i}. {m}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='move-list-box'><span class='player-b'><b>Player B (PW)</b></span>", unsafe_allow_html=True)
        for i, m in enumerate(pw_combos):
            st.markdown(f"<div class='move-item'>{i}. {m}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='move-list-box'><span class='player-c'><b>Player C (RR)</b></span>", unsafe_allow_html=True)
        for i, m in enumerate(player_c_moves):
            st.markdown(f"<div class='move-item'>{i}. {m}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Assumptions ──
    st.markdown("### 📋 Assumptions")
    st.markdown(f"""
    <div class="nash-box" style="font-size:13px;color:#ccc;">
    <b>1. NPV Formula (No Margins, ×{gross_mult:.1f} Gross Multiplier, Straight DCF):</b><br/>
    &nbsp;&nbsp;NPV_per_engine(t) = (Engine_Price × {gross_mult:.1f}) × (1 + CPI)^t &nbsp;&nbsp;(gross-adjusted, escalated to year t)<br/>
    &nbsp;&nbsp;NPV_each_Year(t)  = Planes/yr × 2 engines × Share × NPV_per_engine(t)<br/>
    &nbsp;&nbsp;NPV_Total          = Σ(t=0 to N−1) NPV_each_Year(t) / (1+WACC)^t &nbsp;&nbsp;(straight DCF)<br/><br/>

    <b>2. Engine Pricing:</b><br/>
    &nbsp;&nbsp;NB (30k lbs thrust): Linear regression on historical data → <b>${NB_ENGINE_PRICE_M:.2f}M</b> per engine<br/>
    &nbsp;&nbsp;WB (80k lbs thrust): $140/lb-of-thrust rule → <b>${WB_ENGINE_PRICE_M:.2f}M</b> per engine<br/>
    &nbsp;&nbsp;CPI = {CPI*100:.1f}% annually<br/><br/>

    <b>3. Market Volumes:</b><br/>
    &nbsp;&nbsp;All aircraft have 2 engines. NB: 40,000 total (2,000/yr). WB: 3,400 total (170/yr).<br/>
    &nbsp;&nbsp;EIS 2037 for next-gen NB and re-engined WB platforms.<br/><br/>

    <b>4. Status Quo Shares:</b><br/>
    &nbsp;&nbsp;NB: CFM 76% (LEAP-1B + LEAP-1A), PW 24% (GTF), RR 0% — derived from 737 → 100% LEAP-1B, A320 → 60% LEAP-1A + 40% GTF. &nbsp;|&nbsp; WB: GE 42% (787 70% of 60% mkt), RR 58%.<br/><br/>

    <b>5. R&D Charges (all conditional — no R&D charge if player milks):</b><br/>
    &nbsp;&nbsp;<b>CFM</b>: Open Fan R&D ${inv_cfm_open_fan_rd:.1f}B (only on Open Fan / Open + Ducted), Ducted Fan R&D ${inv_cfm_ducted_rd:.1f}B (only on Ducted Only / Open + Ducted). Milk LEAP → no charge.<br/>
    &nbsp;&nbsp;<b>PW</b> (auto-locked by airframer supplier matrix): GTF2 Solo R&D ${inv_pw_gtf2_solo_rd:.1f}B (if Solo) or GTF2 JV R&D ${inv_pw_gtf2_jv_rd:.1f}B (if JV with RR). Milk GTF → no charge.<br/>
    &nbsp;&nbsp;<b>RR</b>: Ultrafan NB R&D ${inv_rr_rd_nb:.1f}B (only on Ultrafan NB Solo / JV with PW), Ultrafan WB R&D ${inv_rr_rd_wb:.1f}B (only on Ultrafan WB), T1000 Upgrade R&D ${inv_rr_t1000_rd:.1f}B (only on Upgrade T1000). Do Nothing on both → no charge.<br/><br/>

    <b>6. Lobby Govts (Move 5):</b> ${lobby_cost:.1f}B regulatory campaign — Open Fan's <b>defensive companion</b>.
    When paired with Open Fan, caps CFM's NB share loss at <b>20%</b> (instead of the full {open_fan_loss*100:.0f}% wait penalty).
    Has NO standalone effect if Open Fan is not active.<br/><br/>

    <b>7. Strain Cost:</b> ${strain_penalty:.1f}B penalty when a player runs 2+ concurrent engineering projects.<br/><br/>

    <b>8. Open Fan Timing:</b> Open Fan not ready until ~2045 → CFM loses {open_fan_loss*100:.0f}% NB share if launched alone.
    Paired with Lobby Govts (+${lobby_cost:.1f}B), the loss is capped at <b>20%</b>.<br/>
    &nbsp;&nbsp;Ducted Fan ready by 2035 → CFM gains {ducted_fan_gain*100:.0f}% NB share advantage.
    "3-Open + Ducted" runs BOTH simultaneously: net share effect = −{open_fan_loss*100:.0f}% + {ducted_fan_gain*100:.0f}% = {(ducted_fan_gain - open_fan_loss)*100:+.0f}% (or −20% + {ducted_fan_gain*100:.0f}% = {(ducted_fan_gain - 0.20)*100:+.0f}% with Lobby).<br/><br/>

    <b>9. Utility / Yield:</b> Enterprise Value Yield % = 100% + (Total Δ EV / EV) × 100.<br/>
    &nbsp;&nbsp;ε-Nash Tolerance: {eps_tol:.1f}%.<br/><br/>

    <b>10. Player Exclusivity:</b> Moves with the same letter group are mutually exclusive per player.
    Filtered via itertools.product. "Milk LEAP" + "Partner Embraer" cannot co-occur (CFM Group A).
    RR Group A (NB strategy): Do Nothing / Ultrafan NB Solo / JV with PW — mutually exclusive.
    RR Group B (WB tech): ∅ / Ultrafan WB / Upgrade T1000 — mutually exclusive.<br/><br/>

    <b>11. Balance Sheets:</b> CFM EV=${ev_a:.0f}B Debt=${debt_a:.0f}B | PW EV=${ev_b:.0f}B Debt=${debt_b:.0f}B | RR EV=${ev_c:.0f}B Debt=${debt_c:.0f}B
    </div>
    """, unsafe_allow_html=True)

    # ── Engine Prices Used ──
    st.markdown("### 💲 Engine Prices Used in Calculation")
    reg_prices_html = "".join(
        f"<tr><td>{int(t)}</td><td>${p:.2f}M</td><td>${(reg_slope*t + reg_intercept):.2f}M</td><td>${(reg_slope*t + reg_intercept)*gross_mult:.2f}M</td></tr>"
        for t, p in zip(thrust_data, engine_price_data)
    )
    st.markdown(f"""
    <div class="nash-box">
    <div class="nash-title" style="color:#58a6ff;">Regression: Per-Engine Price = {reg_slope:.6f} × Thrust + {reg_intercept:.4f} &nbsp;|&nbsp; Gross Multiplier: ×{gross_mult}</div>
    <table class="price-tbl">
    <tr><th>Thrust (lbs)</th><th>Actual $/Engine</th><th>Regression Fit</th><th>×{gross_mult} Gross Multiplier NPV</th></tr>
    {reg_prices_html}
    <tr style="border-top:2px solid #58a6ff;">
        <td><b>{NB_THRUST} (NB — extrapolated)</b></td>
        <td>—</td>
        <td><b>${NB_ENGINE_PRICE_M:.2f}M</b></td>
        <td><b>${NB_ENGINE_PRICE_M*gross_mult:.2f}M</b></td>
    </tr>
    <tr>
        <td><b>{WB_THRUST} (WB — $140/lb rule)</b></td>
        <td>—</td>
        <td><b>${WB_ENGINE_PRICE_M:.2f}M</b></td>
        <td><b>${WB_ENGINE_PRICE_M*gross_mult:.2f}M</b></td>
    </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # ── Detailed Math for each Nash Equilibrium ──
    if nash_pure or nash_near:
        st.markdown("### 🔬 Detailed Nash Math Walkthrough")
        all_nash = [(a, c, True) for a, c in nash_pure] + [(a, c, False) for a, c in nash_near if (a, c) not in nash_pure]

        for seq, (ai, ci, is_p) in enumerate(all_nash[:5]):  # cap at 5 for readability
            d = matrix[ai][ci]
            tag = "Pure" if is_p else "Near"
            st.markdown(f"""
    <div class="nash-box" style="border-left:4px solid {'#3cb371' if is_p else '#FFD700'};">
    <div class="{'nash-title-pure' if is_p else 'nash-title-near'}">{tag} Nash #{seq+1} — Step-by-Step</div>
    <div style="color:#ddd;font-size:12px;margin-bottom:12px;">
    <b>A:</b> {player_a_moves[ai]}<br/><b>B:</b> {sel_pw}<br/><b>C:</b> {player_c_moves[ci]}
    </div>

    <table class="math-breakdown-table" style="color:#ccc;">
    <tr><td colspan="4" style="color:#58a6ff;font-weight:bold;border-bottom:1px solid #444;">Step 1 — NPV per Engine = (Price × {gross_mult:.1f}) × (1+CPI)^t, N={N_YRS}</td></tr>
    <tr><td>NB (t=0):</td><td class="val">${NB_ENGINE_PRICE_M:.2f}M</td>
        <td>NB (t={max(1,N_YRS)-1}):</td><td class="val">${npv_eng_nb_N:.2f}M</td></tr>
    <tr><td>WB (t=0):</td><td class="val">${WB_ENGINE_PRICE_M:.2f}M</td>
        <td>WB (t={max(1,N_YRS)-1}):</td><td class="val">${npv_eng_wb_N:.2f}M</td></tr>

    <tr><td colspan="4" style="color:#58a6ff;font-weight:bold;border-bottom:1px solid #444;padding-top:10px;">Step 2 — Post-Move Shares</td></tr>
    <tr><td><span class="player-a">A NB:</span></td><td class="val">{d['A']['nb_final']*100:.1f}%</td>
        <td><span class="player-a">A WB:</span></td><td class="val">{d['A']['wb_final']*100:.1f}%</td></tr>
    <tr><td><span class="player-b">B NB:</span></td><td class="val">{d['B']['nb_final']*100:.1f}%</td>
        <td><span class="player-b">B WB:</span></td><td class="val">{d['B']['wb_final']*100:.1f}%</td></tr>
    <tr><td><span class="player-c">C NB:</span></td><td class="val">{d['C']['nb_final']*100:.1f}%</td>
        <td><span class="player-c">C WB:</span></td><td class="val">{d['C']['wb_final']*100:.1f}%</td></tr>

    <tr><td colspan="4" style="color:#58a6ff;font-weight:bold;border-bottom:1px solid #444;padding-top:10px;">Step 3 — Utility = (New NPV − Base NPV) − Strain − Investment</td></tr>
    <tr><td><span class="player-a">A:</span></td><td colspan="3" class="val">
        New ${d['A']['delta_b']+d['A']['base_b']+d['A']['strain_b']+d['A']['inv_b']:.2f}B − Base ${d['A']['base_b']:.2f}B − Strain ${d['A']['strain_b']:.2f}B − Inv ${d['A']['inv_b']:.2f}B = <span style="color:{'#3cb371' if d['A']['delta_b']>=0 else '#ff4444'}">${d['A']['delta_b']:+.2f}B</span></td></tr>
    <tr><td><span class="player-b">B:</span></td><td colspan="3" class="val">
        New ${d['B']['delta_b']+d['B']['base_b']+d['B']['strain_b']+d['B']['inv_b']:.2f}B − Base ${d['B']['base_b']:.2f}B − Strain ${d['B']['strain_b']:.2f}B − Inv ${d['B']['inv_b']:.2f}B = <span style="color:{'#3cb371' if d['B']['delta_b']>=0 else '#ff4444'}">${d['B']['delta_b']:+.2f}B</span></td></tr>
    <tr><td><span class="player-c">C:</span></td><td colspan="3" class="val">
        New ${d['C']['delta_b']+d['C']['base_b']+d['C']['strain_b']+d['C']['inv_b']:.2f}B − Base ${d['C']['base_b']:.2f}B − Strain ${d['C']['strain_b']:.2f}B − Inv ${d['C']['inv_b']:.2f}B = <span style="color:{'#3cb371' if d['C']['delta_b']>=0 else '#ff4444'}">${d['C']['delta_b']:+.2f}B</span></td></tr>

    <tr><td colspan="4" style="color:#58a6ff;font-weight:bold;border-bottom:1px solid #444;padding-top:10px;">Step 4 — EV Yield = 100 + (ΔEV / EV) × 100</td></tr>
    <tr><td><span class="player-a">A:</span></td><td class="val">100 + ({d['A']['delta_b']:+.2f} / {ev_a:.0f}) × 100 = <b>{d['A']['yield_pct']:.0f}%</b></td>
        <td><span class="player-b">B:</span></td><td class="val">100 + ({d['B']['delta_b']:+.2f} / {ev_b:.0f}) × 100 = <b>{d['B']['yield_pct']:.0f}%</b></td></tr>
    <tr><td><span class="player-c">C:</span></td><td class="val" colspan="3">100 + ({d['C']['delta_b']:+.2f} / {ev_c:.0f}) × 100 = <b>{d['C']['yield_pct']:.0f}%</b></td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)




# ============================================================
# BOARD 3 — GAME SUMMARY TAB (NEW — at-a-glance dashboard)
# Reads everything from st.session_state. Defaults match the
# widget defaults so the tab is meaningful on first load even
# if the user hasn't visited the Airframer / Engine tabs yet.
# ============================================================
# ============================================================
# CHART RENDERING — extracted from Summary tab so the Dashboard
# tab can call the SAME charts. Each function reads from
# session_state directly and renders to streamlit.
# ============================================================
def _render_nb_share_trajectory_block(a_strat, b_strat):
    """Module-level NB share trajectory chart, called by both Summary and Dashboard tabs."""
    import plotly.graph_objects as go
    _ac_a_strat = a_strat
    _ac_b_strat = b_strat
    _ac_fps_eis  = int(st.session_state.get('af_fps_eis',  2037))
    _ac_ngsa_eis = int(st.session_state.get('af_ngsa_eis', 2037))
    _CHT_787_EIS_YEAR  = int(st.session_state.get('af_787_eis',  2041))
    _CHT_A350_EIS_YEAR = int(st.session_state.get('af_a350_eis', 2035))

    # ============================================================
    # PART 1a-2 — NB SHARE TRAJECTORY w/ DRIVER ANNOTATIONS
    # Companion chart to the aircraft delivery chart. Shows Boeing
    # vs Airbus NB market share % year-by-year, with vertical
    # dashed lines and text labels at every TRIGGER year where a
    # driver activates, expires, or fires for the first time.
    # Uses the unified rule helpers — math cannot drift from
    # evaluate_scenario.
    # ============================================================
    _trj_b_nb_move, _trj_b_rate, _ = _ac_b_strat
    _trj_a_nb_move, _trj_a_btl, _trj_a_poach, _ = _ac_a_strat
    _trj_b_launches = "Launch_fps" in _trj_b_nb_move
    _trj_a_launches = "Launch_NGSA" in _trj_a_nb_move
    _trj_b_inc_rate = "Increase_737_Rate" in _trj_b_rate
    _trj_is_7yr = (_trj_b_nb_move == "Launch_fps_7yr_Solo")
    _trj_active_sabs = sum(1 for m in (_trj_a_btl, _trj_a_poach)
                           if "Sabotage" in m and "No" not in m)
    _trj_fps_7yr_adv = float(st.session_state.get('af_fps_7yr_adv', 5.0))
    _trj_sab_share   = float(st.session_state.get('af_sab_share',   5.0))
    _trj_b_eis_t = max(0, _ac_fps_eis  - 2026)
    _trj_a_eis_t = max(0, _ac_ngsa_eis - 2026)
    # WB context (for EIS-reference annotations on the NB chart)
    _trj_b_wb_eis_t = max(0, _CHT_787_EIS_YEAR  - 2026)
    _trj_a_wb_eis_t = max(0, _CHT_A350_EIS_YEAR - 2026)
    _trj_b_reengines = "Re-engine_787"  in _ac_b_strat[2]
    _trj_a_reengines = "Re-engine_A350" in _ac_a_strat[3]

    # Compute share trajectory year-by-year using the unified helpers
    _trj_years = list(range(2026, 2057))   # 2026..2056 inclusive
    _trj_b_shares = []
    _trj_a_shares = []
    for _ty in _trj_years:
        _tt = _ty - 2026
        _bsh, _ash = _compute_nb_share_unified(
            _tt, _trj_b_launches, _trj_a_launches,
            _trj_b_eis_t, _trj_a_eis_t, is_7yr=_trj_is_7yr)
        _bsh, _ash = _apply_nb_modifiers(
            _bsh, _ash, _tt, _trj_b_eis_t, _trj_a_eis_t,
            _trj_b_launches, _trj_a_launches,
            b_inc_rate=_trj_b_inc_rate,
            is_7yr=_trj_is_7yr, fps_7yr_pp=_trj_fps_7yr_adv,
            active_sabs=_trj_active_sabs, sab_share_pp=_trj_sab_share)
        _trj_b_shares.append(_bsh * 100)
        _trj_a_shares.append(_ash * 100)

    # Compute trigger-year driver labels (NB only — WB events excluded)
    if _trj_is_7yr:
        _trj_bg_pp = float(st.session_state.get('af_ramp7_b_pp', 4.0))
        _trj_ar_pp = float(st.session_state.get('af_ramp7_a_pp', 4.0))
    else:
        _trj_bg_pp = float(st.session_state.get('af_ramp10_b_pp', 4.0))
        _trj_ar_pp = float(st.session_state.get('af_ramp10_a_pp', 4.0))
    _trj_drivers = _nb_driver_labels(
        _trj_b_launches, _trj_a_launches, _trj_b_eis_t, _trj_a_eis_t,
        b_inc_rate=_trj_b_inc_rate, is_7yr=_trj_is_7yr,
        active_sabs=_trj_active_sabs,
        fps_7yr_pp=_trj_fps_7yr_adv, sab_share_pp=_trj_sab_share,
        b_gain_pp=_trj_bg_pp, a_recover_pp=_trj_ar_pp)

    # Build the plotly figure
    _trj_fig = go.Figure()
    _trj_fig.add_trace(go.Scatter(
        x=_trj_years, y=_trj_b_shares, mode='lines+markers',
        name='Boeing NB share', line=dict(color='#1f77b4', width=3),
        marker=dict(size=6), hovertemplate='%{x}: %{y:.1f}%<extra>Boeing</extra>'))
    _trj_fig.add_trace(go.Scatter(
        x=_trj_years, y=_trj_a_shares, mode='lines+markers',
        name='Airbus NB share', line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6), hovertemplate='%{x}: %{y:.1f}%<extra>Airbus</extra>'))

    # 50/50 balance line for reference
    _trj_fig.add_hline(y=50, line_dash='dot', line_color='rgba(200,200,200,0.55)',
                       line_width=1, opacity=0.8,
                       annotation_text='50/50 balance',
                       annotation_position='right',
                       annotation_font=dict(size=10, color='#bbb'))

    # Vertical dashed lines + driver text annotations at each trigger year
    # Place labels alternating above/below to reduce overlap
    _trj_label_y_high = 92
    _trj_label_y_low  = 8
    _trj_alternate = True
    for _t_off in sorted(_trj_drivers.keys()):
        if _t_off < 0 or _t_off > 30:
            continue
        _yr_lbl = 2026 + _t_off
        _label = _trj_drivers[_t_off]
        _trj_fig.add_vline(x=_yr_lbl, line_dash='dot',
                           line_color='rgba(200,200,200,0.65)',
                           line_width=1.2)
        _y_pos = _trj_label_y_high if _trj_alternate else _trj_label_y_low
        _trj_alternate = not _trj_alternate
        _trj_fig.add_annotation(
            x=_yr_lbl, y=_y_pos,
            text=f"<b>{_yr_lbl}</b><br>{_label.replace(chr(10), '<br>')}",
            showarrow=False, font=dict(size=11, color='#222'),
            align='left', bgcolor='rgba(255,255,255,0.93)',
            bordercolor='rgba(180,180,180,0.7)', borderwidth=1,
            borderpad=4, xanchor='left', xshift=2)

    _trj_fig.update_layout(
        title=dict(text='NB Market Share Trajectory — with Driver Annotations',
                   font=dict(size=14, color='#eee')),
        xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                   title_font=dict(color='#eee'),
                   tickfont=dict(color='#ddd'),
                   gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.15)'),
        yaxis=dict(title='NB share (%)', range=[0, 100], dtick=10,
                   title_font=dict(color='#eee'),
                   tickfont=dict(color='#ddd'),
                   gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.15)'),
        height=460, margin=dict(l=50, r=20, t=50, b=40),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02,
                    xanchor='right', x=1,
                    font=dict(color='#eee'),
                    bgcolor='rgba(0,0,0,0)'),
        plot_bgcolor='#000',
        paper_bgcolor='#000'
    )
    st.plotly_chart(_trj_fig, use_container_width=True)
    st.caption(
        "Vertical dashed lines mark **trigger years** where a driver "
        "activates, expires, or fires for the first time. Years with no "
        "label have no new driver event (shares evolve under whatever "
        "rule is currently active). Boeing's line + Airbus's line sum to "
        "100% in every year. The 50/50 dotted line marks the Phase 2 "
        "equilibrium balance point."
    )

def _render_wb_share_trajectory_block(a_strat, b_strat):
    """Module-level WB share trajectory chart, called by both Summary and Dashboard tabs."""
    import plotly.graph_objects as go
    _ac_a_strat = a_strat
    _ac_b_strat = b_strat
    _ac_fps_eis  = int(st.session_state.get('af_fps_eis',  2037))
    _ac_ngsa_eis = int(st.session_state.get('af_ngsa_eis', 2037))
    _CHT_787_EIS_YEAR  = int(st.session_state.get('af_787_eis',  2041))
    _CHT_A350_EIS_YEAR = int(st.session_state.get('af_a350_eis', 2035))

    # ============================================================
    # PART 1a-3 — WB SHARE TRAJECTORY w/ DRIVER ANNOTATIONS
    # Companion chart for the WB (widebody) market. Uses the unified
    # WB-rule helper (mirrors evaluate_scenario's per-year math).
    # Status quo: 787 100/170 (~58.8%), A350 70/170 (~41.2%). No
    # Phase 2 — leader's catch-up freezes when follower's EIS hits.
    # ============================================================
    _wb_b_reengines = "Re_engine_787"  in _ac_b_strat[2]
    _wb_a_reengines = "Re_engine_A350" in _ac_a_strat[3]
    _wb_b_eis_yr = int(st.session_state.get('af_787_eis',  2041))
    _wb_a_eis_yr = int(st.session_state.get('af_a350_eis', 2035))
    _wb_milker_share = float(st.session_state.get('af_wb_milker', 15.0)) / 100.0
    _wb_b_eis_t = max(0, _wb_b_eis_yr - 2026)
    _wb_a_eis_t = max(0, _wb_a_eis_yr - 2026)

    # Compute year-by-year WB share via unified helper
    _wb_years = list(range(2026, 2057))
    _wb_b_shares = []
    _wb_a_shares = []
    for _ty in _wb_years:
        _tt = _ty - 2026
        _bsh, _ash = _compute_wb_share_unified(
            _tt, _wb_b_reengines, _wb_a_reengines,
            _wb_b_eis_t, _wb_a_eis_t,
            wb_milker_share=_wb_milker_share)
        _wb_b_shares.append(_bsh * 100)
        _wb_a_shares.append(_ash * 100)

    _wb_drivers = _wb_driver_labels(
        _wb_b_reengines, _wb_a_reengines, _wb_b_eis_t, _wb_a_eis_t,
        wb_milker_share=_wb_milker_share)

    # Build plotly figure (mirrors NB chart styling)
    _wb_fig = go.Figure()
    _wb_fig.add_trace(go.Scatter(
        x=_wb_years, y=_wb_b_shares, mode='lines+markers',
        name='Boeing 787 share', line=dict(color='#1f77b4', width=3),
        marker=dict(size=6), hovertemplate='%{x}: %{y:.1f}%<extra>Boeing 787</extra>'))
    _wb_fig.add_trace(go.Scatter(
        x=_wb_years, y=_wb_a_shares, mode='lines+markers',
        name='Airbus A350 share', line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6), hovertemplate='%{x}: %{y:.1f}%<extra>Airbus A350</extra>'))

    # Status-quo reference line at ~58.8% Boeing (100/170)
    _wb_sq_b = 100.0 * (100/170)
    _wb_fig.add_hline(y=_wb_sq_b, line_dash='dot',
                      line_color='rgba(200,200,200,0.55)',
                      line_width=1, opacity=0.8,
                      annotation_text=f'Status quo: {_wb_sq_b:.1f}% Boeing',
                      annotation_position='right',
                      annotation_font=dict(size=10, color='#bbb'))

    # Annotations + dotted vertical lines at trigger years
    _wb_label_high = 92
    _wb_label_low  = 8
    _wb_alt = True
    for _t_off in sorted(_wb_drivers.keys()):
        if _t_off < 0 or _t_off > 30:
            continue
        _yr_lbl = 2026 + _t_off
        _label = _wb_drivers[_t_off]
        _wb_fig.add_vline(x=_yr_lbl, line_dash='dot',
                          line_color='rgba(200,200,200,0.65)',
                          line_width=1.2)
        _y_pos = _wb_label_high if _wb_alt else _wb_label_low
        _wb_alt = not _wb_alt
        _wb_fig.add_annotation(
            x=_yr_lbl, y=_y_pos,
            text=f"<b>{_yr_lbl}</b><br>{_label.replace(chr(10), '<br>')}",
            showarrow=False, font=dict(size=11, color='#222'),
            align='left', bgcolor='rgba(255,255,255,0.93)',
            bordercolor='rgba(180,180,180,0.7)', borderwidth=1,
            borderpad=4, xanchor='left', xshift=2)

    _wb_fig.update_layout(
        title=dict(text='WB Market Share Trajectory — with Driver Annotations',
                   font=dict(size=14, color='#eee')),
        xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                   title_font=dict(color='#eee'),
                   tickfont=dict(color='#ddd'),
                   gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.15)'),
        yaxis=dict(title='WB share (%)', range=[0, 100], dtick=10,
                   title_font=dict(color='#eee'),
                   tickfont=dict(color='#ddd'),
                   gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.15)'),
        height=460, margin=dict(l=50, r=20, t=50, b=40),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02,
                    xanchor='right', x=1,
                    font=dict(color='#eee'),
                    bgcolor='rgba(0,0,0,0)'),
        plot_bgcolor='#000',
        paper_bgcolor='#000'
    )
    st.plotly_chart(_wb_fig, use_container_width=True)
    st.caption(
        "WB market share % per year for the selected airframer "
        "equilibrium. Status quo is Boeing 100/170 (~58.8%) and "
        "Airbus 70/170 (~41.2%) — drawn as a dotted reference line. "
        "Unlike NB, WB shares have no Phase 2 convergence — when the "
        "follower's EIS arrives in 'both re-engine' cases, shares "
        "FREEZE at the leader's Phase 1 final value. Boeing's cap "
        "depends on case: 80% (both re-engine, 787 leads), or "
        f"{(1-_wb_milker_share)*100:.0f}% (Boeing solo). Airbus is "
        "always capped at 60% (structural A350 ceiling). Dotted "
        "vertical lines mark 787 EIS / A350 EIS trigger years; 'Same "
        "EIS' or 'Neither re-engines' shows a single Case A/B label."
    )

def _render_player_cash_flow_block(a_strat, b_strat):
    """Module-level cash flow bar chart (with internal player picker), called by both Summary and Dashboard tabs."""
    import plotly.graph_objects as go
    import numpy as np
    _ac_a_strat = a_strat
    _ac_b_strat = b_strat
    # Summary-tab constants the original block expected from outer scope
    _CHT_YEARS = list(range(2026, 2069))   # 2026..2068 inclusive
    NPV_POST_EIS_YRS_AC = 20

    # ============================================================
    # PART 1b — PLAYER CASH-FLOW BAR CHART (airframer NPV breakdown)
    # Year-by-year decomposition of the airframer board's Δ EV ($B)
    # for the selected airframer equilibrium. Shows the same NPV math
    # that evaluate_scenario() inside run_airframer_board computes:
    #   • Per-year positive/negative stacks: Δ NB-PV and Δ WB-PV
    #     (scenario revenue minus pre-2037 status-quo baseline,
    #     discounted at the player's WACC). Years 2026-2056 only.
    #   • One segmented negative stack at 2037 for the lump-sum costs
    #     deducted in the NPV: CAPEX (PV-discounted), Two-Front Strain,
    #     Debt penalty (α-quadratic), Naked Espionage Fine (Airbus),
    #     Rate-hike PV cost (Boeing), Sabotage Op cost PV (Airbus).
    # Summing every bar in the chart = the player's Δ EV in $B
    # (the same number shown in the airframer math receipt).
    # ============================================================
    st.markdown("**1️⃣b Player cash flows — Δ vs status quo baseline (same airframer equilibrium)**")

    _cf_af_player = st.selectbox(
        "Pick a player to inspect",
        options=["Boeing", "Airbus"],
        index=0,
        key="_cf_af_player_pick",
        help=("Year-by-year discounted PV cash flows that feed the airframer "
              "board's NPV calculation for the selected player. CAPEX, "
              "strain, fines, rate-hike PV, and debt penalty appear as a "
              "segmented stack at 2037. Sum of all bars = the player's "
              "Δ EV in $B (same as the (Δ $X.XXB) figure in the math receipt)."),
    )
    _cfa_player_is_b = (_cf_af_player == "Boeing")

    # ── Airframer constants (identical to run_airframer_board) ──
    _CFA_TIMELINE_YRS = 31    # 2026..2056 — base; per-program windows may extend
    _CFA_NPV_POST_EIS_YRS = 20  # Phase A per-program window (matches simulator)
    _CFA_NB_PER_YR    = 2000
    _CFA_WB_PER_YR    = 170
    _CFA_WACC_B       = 0.105
    _CFA_WACC_A       = 0.080

    # ── Airframer parameters from session state ──
    _CFA_PRICE_737  = float(st.session_state.get('af_price_737',  48.0)) / 1000.0
    _CFA_PRICE_A320 = float(st.session_state.get('af_price_a320', 52.0)) / 1000.0
    _CFA_PRICE_FPS  = float(st.session_state.get('af_price_fps',  55.0)) / 1000.0
    _CFA_PRICE_NGSA = float(st.session_state.get('af_price_ngsa', 55.0)) / 1000.0
    _CFA_PRICE_WB   = float(st.session_state.get('af_price_wb',  180.0)) / 1000.0
    _CFA_M_737   = float(st.session_state.get('af_m_737',    8.00)) / 100.0
    _CFA_M_A320  = float(st.session_state.get('af_m_a320',  13.14)) / 100.0
    _CFA_M_FPS   = float(st.session_state.get('af_m_fps',   25.64)) / 100.0
    _CFA_M_NGSA  = float(st.session_state.get('af_m_ngsa',  26.28)) / 100.0
    _CFA_M_787   = float(st.session_state.get('af_m_787',   20.00)) / 100.0
    _CFA_M_A350  = float(st.session_state.get('af_m_a350',   4.95)) / 100.0
    _CFA_CX_FPS7      = float(st.session_state.get('af_cx_fps7',   60.69))
    _CFA_CX_FPS10     = float(st.session_state.get('af_cx_fps10',  55.25))
    _CFA_CX_FPSEMB    = float(st.session_state.get('af_cx_fpsemb', 100.00))
    _CFA_CX_NGSA      = float(st.session_state.get('af_cx_ngsa',   30.07))
    _CFA_CX_787RE     = float(st.session_state.get('af_cx_787re',   5.00))
    _CFA_CX_A350RE    = float(st.session_state.get('af_cx_a350re',  5.00))
    _CFA_CX_737RATE   = float(st.session_state.get('af_cx_737rate', 2.94))
    _CFA_EV_BOEING    = float(st.session_state.get('af_ev_boeing',  130.0))
    _CFA_DEBT_BOEING  = float(st.session_state.get('af_debt_boeing', 45.0))
    _CFA_EV_AIRBUS    = float(st.session_state.get('af_ev_airbus',  150.0))
    _CFA_DEBT_AIRBUS  = float(st.session_state.get('af_debt_airbus', 10.0))
    _CFA_STRAIN_B     = float(st.session_state.get('af_strain_b',    5.94))
    _CFA_STRAIN_A     = float(st.session_state.get('af_strain_a',    5.94))
    _CFA_NAKED_FINE   = float(st.session_state.get('af_naked_fine', 48.32))
    _CFA_NB_MILKER    = float(st.session_state.get('af_nb_milker', 30.0)) / 100.0
    _CFA_WB_MILKER    = float(st.session_state.get('af_wb_milker', 15.0)) / 100.0
    _CFA_SAB_SHARE    = float(st.session_state.get('af_sab_share',  5.0))
    _CFA_SAB_COST     = float(st.session_state.get('af_sab_cost',   1.0))
    _CFA_FPS_7YR_ADV  = float(st.session_state.get('af_fps_7yr_adv', 7.0))
    _CFA_ALPHA        = float(st.session_state.get('af_alpha',       0.3))
    _CFA_B_SHARE_PCT  = float(st.session_state.get('_boeing_share_both', 50.0))
    # WB EIS years (per-platform sliders) → t-offsets (year 0 = 2026)
    _CFA_B_WB_EIS_T   = max(0, int(st.session_state.get('af_787_eis',  2041)) - 2026)
    _CFA_A_WB_EIS_T   = max(0, int(st.session_state.get('af_a350_eis', 2035)) - 2026)
    # NB EIS years (per-program sliders)
    _CFA_B_NB_EIS_T   = max(0, int(st.session_state.get('af_fps_eis',  2037)) - 2026)
    _CFA_A_NB_EIS_T   = max(0, int(st.session_state.get('af_ngsa_eis', 2037)) - 2026)

    # ── Decode the selected airframer equilibrium ──
    _cfa_a_strat = _ac_a_strat
    _cfa_b_strat = _ac_b_strat
    _cfa_b_launches = "Launch_fps" in _cfa_b_strat[0]
    _cfa_a_launches = "Launch_NGSA" in _cfa_a_strat[0]
    _cfa_b_inc_rate = "Increase_737_Rate" in _cfa_b_strat[1]
    _cfa_is_7yr_solo = (_cfa_b_strat[0] == "Launch_fps_7yr_Solo")
    _cfa_is_10yr = "10yr" in _cfa_b_strat[0]
    _cfa_b_reengines = "Re_engine_787" in _cfa_b_strat[2]
    _cfa_a_reengines = "Re_engine_A350" in _cfa_a_strat[3]
    _cfa_active_sabs = sum(1 for m in _cfa_a_strat if "Sabotage" in m and "No" not in m)

    # ── Post-EIS NB / WB shares (mirror evaluate_scenario) ──
    if _cfa_b_launches and not _cfa_a_launches:
        _cfa_b_eis_nb = 1.0 - _CFA_NB_MILKER
        _cfa_a_eis_nb = _CFA_NB_MILKER
    elif _cfa_a_launches and not _cfa_b_launches:
        _cfa_a_eis_nb = 1.0 - _CFA_NB_MILKER
        _cfa_b_eis_nb = _CFA_NB_MILKER
    elif _cfa_b_launches and _cfa_a_launches:
        _cfa_b_eis_nb = _CFA_B_SHARE_PCT / 100.0
        _cfa_a_eis_nb = 1.0 - _cfa_b_eis_nb
    else:
        _cfa_b_eis_nb, _cfa_a_eis_nb = 0.40, 0.60
    if _cfa_b_launches and _cfa_is_7yr_solo:
        _cfa_b_eis_nb = min(1.0, _cfa_b_eis_nb + _CFA_FPS_7YR_ADV / 100.0)
        _cfa_a_eis_nb = max(0.0, 1.0 - _cfa_b_eis_nb)
    if _cfa_active_sabs > 0 and _cfa_b_launches:
        _shift = _CFA_SAB_SHARE / 100.0 * _cfa_active_sabs
        _cfa_b_eis_nb -= _shift
        _cfa_a_eis_nb += _shift

    if _cfa_b_reengines and not _cfa_a_reengines:
        _cfa_b_eis_wb = 1.0 - _CFA_WB_MILKER
        _cfa_a_eis_wb = _CFA_WB_MILKER
    elif _cfa_a_reengines and not _cfa_b_reengines:
        _cfa_a_eis_wb = 1.0 - _CFA_WB_MILKER
        _cfa_b_eis_wb = _CFA_WB_MILKER
    else:
        _cfa_b_eis_wb, _cfa_a_eis_wb = 100/170, 70/170

    _cfa_nb_milker_active = (_cfa_b_launches != _cfa_a_launches)
    _cfa_wb_milker_active = (_cfa_b_reengines != _cfa_a_reengines)

    # ── CPI for nominal cash-flow escalation (same as engine board) ──
    _CFA_CPI = 0.022   # 2.2% annual price escalation

    # ── Per-year scenario and base revenue (NOMINAL cash flow, with CPI
    #    escalation — what the player actually earns each year).
    #    A parallel PV pass below produces the NPV equivalent for the
    #    caption, mirroring evaluate_scenario's WACC-discounted math. ──
    _cfa_delta_nb_pv = [0.0] * len(_CHT_YEARS)  # nominal Δ NB cash flow / yr
    _cfa_delta_wb_pv = [0.0] * len(_CHT_YEARS)  # nominal Δ WB cash flow / yr
    _cfa_delta_nb_pv_npv = 0.0   # PV-equivalent sum for caption
    _cfa_delta_wb_pv_npv = 0.0

    # Per-program end-t offsets for the selected player (Phase A: 20 yrs
    # post-EIS inclusive of EIS year, plus full pre-EIS legacy).
    if _cfa_player_is_b:
        _cfa_my_nb_end_t = _CFA_B_NB_EIS_T + _CFA_NPV_POST_EIS_YRS - 1
        _cfa_my_wb_end_t = _CFA_B_WB_EIS_T + _CFA_NPV_POST_EIS_YRS - 1
    else:
        _cfa_my_nb_end_t = _CFA_A_NB_EIS_T + _CFA_NPV_POST_EIS_YRS - 1
        _cfa_my_wb_end_t = _CFA_A_WB_EIS_T + _CFA_NPV_POST_EIS_YRS - 1

    for idx, yr in enumerate(_CHT_YEARS):
        t = yr - 2026
        # Outer bound: extend beyond _CFA_TIMELINE_YRS only if a program's
        # window requires it (late EIS). Otherwise skip year.
        if t > max(_cfa_my_nb_end_t, _cfa_my_wb_end_t):
            continue
        wacc = _CFA_WACC_B if _cfa_player_is_b else _CFA_WACC_A
        df = 1.0 / ((1 + wacc) ** t)             # for caption-NPV math only
        cpi_factor = (1 + _CFA_CPI) ** t          # nominal escalation for bars

        # NB share — UNIFIED rule v2 via module helpers
        b_sh_nb, a_sh_nb = _compute_nb_share_unified(
            t, _cfa_b_launches, _cfa_a_launches, _CFA_B_NB_EIS_T, _CFA_A_NB_EIS_T,
            is_7yr=_cfa_is_7yr_solo)
        b_sh_nb, a_sh_nb = _apply_nb_modifiers(
            b_sh_nb, a_sh_nb, t, _CFA_B_NB_EIS_T, _CFA_A_NB_EIS_T,
            _cfa_b_launches, _cfa_a_launches,
            b_inc_rate=_cfa_b_inc_rate,
            is_7yr=_cfa_is_7yr_solo, fps_7yr_pp=_CFA_FPS_7YR_ADV,
            active_sabs=_cfa_active_sabs, sab_share_pp=_CFA_SAB_SHARE)

        # Price / margin per-program timing
        if _cfa_b_launches and t >= _CFA_B_NB_EIS_T:
            b_p, b_m = _CFA_PRICE_FPS, _CFA_M_FPS
        else:
            b_p, b_m = _CFA_PRICE_737, _CFA_M_737
        if _cfa_a_launches and t >= _CFA_A_NB_EIS_T:
            a_p, a_m = _CFA_PRICE_NGSA, _CFA_M_NGSA
        else:
            a_p, a_m = _CFA_PRICE_A320, _CFA_M_A320

        # NB cashflow — only within selected player's NB program window
        if t <= _cfa_my_nb_end_t:
            # NOMINAL cash flow for the bar (price × units × share × margin × CPI factor)
            scen_nb_nom = (_CFA_NB_PER_YR * b_sh_nb * b_p * b_m * cpi_factor) if _cfa_player_is_b \
                          else (_CFA_NB_PER_YR * a_sh_nb * a_p * a_m * cpi_factor)
            # NB base (status quo: 40/60 split, 737/A320) — same CPI escalation
            if _cfa_player_is_b:
                base_nb_nom = _CFA_NB_PER_YR * 0.40 * _CFA_PRICE_737 * _CFA_M_737 * cpi_factor
            else:
                base_nb_nom = _CFA_NB_PER_YR * 0.60 * _CFA_PRICE_A320 * _CFA_M_A320 * cpi_factor
            _cfa_delta_nb_pv[idx] = scen_nb_nom - base_nb_nom

            # Parallel PV pass for caption — mirrors evaluate_scenario exactly
            # (WACC discount, NO CPI in revenue — that's the dashboard's math).
            scen_nb_pv_for_npv = (_CFA_NB_PER_YR * b_sh_nb * b_p * b_m * df) if _cfa_player_is_b \
                                 else (_CFA_NB_PER_YR * a_sh_nb * a_p * a_m * df)
            if _cfa_player_is_b:
                base_nb_pv_for_npv = _CFA_NB_PER_YR * 0.40 * _CFA_PRICE_737 * _CFA_M_737 * df
            else:
                base_nb_pv_for_npv = _CFA_NB_PER_YR * 0.60 * _CFA_PRICE_A320 * _CFA_M_A320 * df
            _cfa_delta_nb_pv_npv += scen_nb_pv_for_npv - base_nb_pv_for_npv

        # ── WB scenario revenue this year ──
        # UNIFIED WB share rule (mirrors evaluate_scenario):
        # No pre-EIS anticipation. Status quo until first relevant EIS,
        # then per-case catch-up.
        if _cfa_b_reengines and not _cfa_a_reengines:
            # XOR Case E: only Boeing re-engines
            if t < _CFA_B_WB_EIS_T:
                b_sh_wb, a_sh_wb = 100/170, 70/170
            else:
                years_in = t - _CFA_B_WB_EIS_T + 1
                b_sh_wb = min(1.0 - _CFA_WB_MILKER, 100/170 + _wb_gain_b() * years_in)
                a_sh_wb = 1.0 - b_sh_wb
        elif _cfa_a_reengines and not _cfa_b_reengines:
            # XOR Case F: only Airbus re-engines
            if t < _CFA_A_WB_EIS_T:
                b_sh_wb, a_sh_wb = 100/170, 70/170
            else:
                years_in = t - _CFA_A_WB_EIS_T + 1
                a_sh_wb = min(0.60, 70/170 + _wb_gain_a() * years_in)
                b_sh_wb = 1.0 - a_sh_wb
        elif _cfa_b_reengines and _cfa_a_reengines and _CFA_B_WB_EIS_T != _CFA_A_WB_EIS_T:
            if _CFA_B_WB_EIS_T < _CFA_A_WB_EIS_T:
                if t < _CFA_B_WB_EIS_T:
                    b_sh_wb, a_sh_wb = 100/170, 70/170
                else:
                    catch_t = min(t, _CFA_A_WB_EIS_T - 1)
                    years_in = catch_t - _CFA_B_WB_EIS_T + 1
                    b_sh_wb = min(0.80, 100/170 + _wb_gain_b() * years_in)
                    a_sh_wb = 1.0 - b_sh_wb
            else:
                if t < _CFA_A_WB_EIS_T:
                    b_sh_wb, a_sh_wb = 100/170, 70/170
                else:
                    catch_t = min(t, _CFA_B_WB_EIS_T - 1)
                    years_in = catch_t - _CFA_A_WB_EIS_T + 1
                    a_sh_wb = min(0.60, 70/170 + _wb_gain_a() * years_in)
                    b_sh_wb = 1.0 - a_sh_wb
        else:
            b_sh_wb, a_sh_wb = 100/170, 70/170

        scen_wb_nom = (_CFA_WB_PER_YR * b_sh_wb * _CFA_PRICE_WB * _CFA_M_787 * cpi_factor) if _cfa_player_is_b \
                      else (_CFA_WB_PER_YR * a_sh_wb * _CFA_PRICE_WB * _CFA_M_A350 * cpi_factor)
        base_wb_nom = (_CFA_WB_PER_YR * (100/170) * _CFA_PRICE_WB * _CFA_M_787 * cpi_factor) if _cfa_player_is_b \
                      else (_CFA_WB_PER_YR * (70/170)  * _CFA_PRICE_WB * _CFA_M_A350 * cpi_factor)
        # WB cashflow — only within selected player's WB program window
        if t <= _cfa_my_wb_end_t:
            _cfa_delta_wb_pv[idx] = scen_wb_nom - base_wb_nom

            # Parallel PV pass for caption (no CPI in revenue, WACC discount only)
            scen_wb_pv_for_npv = (_CFA_WB_PER_YR * b_sh_wb * _CFA_PRICE_WB * _CFA_M_787 * df) if _cfa_player_is_b \
                                 else (_CFA_WB_PER_YR * a_sh_wb * _CFA_PRICE_WB * _CFA_M_A350 * df)
            base_wb_pv_for_npv = (_CFA_WB_PER_YR * (100/170) * _CFA_PRICE_WB * _CFA_M_787 * df) if _cfa_player_is_b \
                                 else (_CFA_WB_PER_YR * (70/170)  * _CFA_PRICE_WB * _CFA_M_A350 * df)
            _cfa_delta_wb_pv_npv += scen_wb_pv_for_npv - base_wb_pv_for_npv

    # ── Lump-sum costs ──
    # Bars show NOMINAL totals at 2037 (what the player actually commits).
    # Parallel PV values are kept for the caption's NPV-equivalent (matches
    # the dashboard's receipt math: WACC discount, CAPEX spread t=2..10 NB,
    # t=4..9 WB; strain/fine/debt-penalty lump nominal).
    def _cfa_pv_stream(nominal, t0, t1, wacc):
        if nominal == 0: return 0.0
        annual = nominal / (t1 - t0 + 1)
        return sum(annual / ((1 + wacc) ** t) for t in range(t0, t1 + 1))

    if _cfa_player_is_b:
        wacc = _CFA_WACC_B
        nom_invest_nb = 0.0
        if _cfa_b_launches:
            if _cfa_is_10yr:
                nom_invest_nb = _CFA_CX_FPS10
            elif "Solo" in _cfa_b_strat[0]:
                nom_invest_nb = _CFA_CX_FPS7
            else:
                nom_invest_nb = _CFA_CX_FPSEMB
        nom_invest_wb = _CFA_CX_787RE if _cfa_b_reengines else 0.0
        # Option B: lump CAPEX at EIS year
        pv_nb_invest = nom_invest_nb / ((1 + wacc) ** _CFA_B_NB_EIS_T)
        pv_wb_invest = nom_invest_wb / ((1 + wacc) ** _CFA_B_WB_EIS_T)
        nom_total = nom_invest_nb + nom_invest_wb
        pv_total  = pv_nb_invest  + pv_wb_invest
        # Debt penalty — PV-discounted by the CAPEX time profile so it
        # slides with EIS, consistent with the simulator's calculate_tc.
        if nom_total > 0:
            debt = _CFA_DEBT_BOEING; ev = _CFA_EV_BOEING; alpha = _CFA_ALPHA
            base_pen = debt * alpha * (debt / ev) ** 2
            new_d    = debt + nom_total
            new_pen  = new_d * alpha * (new_d / ev) ** 2
            delta_pen = (new_pen - base_pen) * (pv_total / nom_total)
        else:
            delta_pen = 0.0
        # Two-front strain — nominal lump in both views
        strain = _CFA_STRAIN_B if (_cfa_b_launches and _cfa_b_reengines) else 0.0
        # Rate hike: bar shows the nominal capex incurred at fps_EIS−5 (default 2032);
        # caption uses the PV that the dashboard actually deducts.
        rate_hike_nominal = _CFA_CX_737RATE if _cfa_b_inc_rate else 0.0
        # 737 Rate Hike fires in 2032 (t=6), fixed-calendar, EIS-independent.
        _cfa_rate_hike_t  = 6
        rate_hike_pv      = (_CFA_CX_737RATE / ((1 + wacc) ** _cfa_rate_hike_t)) if _cfa_b_inc_rate else 0.0
        # Sabotage and naked-fine are Airbus-only
        nom_sabotage = 0.0
        sabotage_pv  = 0.0
        naked_fine   = 0.0
    else:
        wacc = _CFA_WACC_A
        nom_invest_nb = _CFA_CX_NGSA if _cfa_a_launches else 0.0
        nom_invest_wb = _CFA_CX_A350RE if _cfa_a_reengines else 0.0
        # Option B: lump CAPEX at EIS year
        pv_nb_invest = nom_invest_nb / ((1 + wacc) ** _CFA_A_NB_EIS_T)
        pv_wb_invest = nom_invest_wb / ((1 + wacc) ** _CFA_A_WB_EIS_T)
        # Sabotage cost — tied to fps's CAPEX window (Airbus interferes during fps dev)
        nom_sabotage = _CFA_SAB_COST * _cfa_active_sabs
        sabotage_pv  = _cfa_pv_stream(nom_sabotage,
                                      max(0, _CFA_B_NB_EIS_T - 9),
                                      _CFA_B_NB_EIS_T - 1, wacc)
        nom_total = nom_invest_nb + nom_invest_wb + nom_sabotage
        pv_total  = pv_nb_invest  + pv_wb_invest  + sabotage_pv
        if nom_total > 0:
            debt = _CFA_DEBT_AIRBUS; ev = _CFA_EV_AIRBUS; alpha = _CFA_ALPHA
            base_pen = debt * alpha * (debt / ev) ** 2
            new_d    = debt + nom_total
            new_pen  = new_d * alpha * (new_d / ev) ** 2
            delta_pen = (new_pen - base_pen) * (pv_total / nom_total)
        else:
            delta_pen = 0.0
        strain = _CFA_STRAIN_A if (_cfa_a_launches and _cfa_a_reengines) else 0.0
        naked_fine = _CFA_NAKED_FINE if (_cfa_active_sabs > 0 and not _cfa_b_launches) else 0.0
        rate_hike_nominal = 0.0  # Airbus has no rate-hike
        rate_hike_pv      = 0.0

    # ── Build per-segment cost lists with Option B semantics ──
    # CAPEX / NRE is a single lump at the program's EIS year. Sabotage
    # remains a multi-year operational spread (it's not CAPEX).
    def _spread(total_nom, t_start, t_end):
        """Spread a nominal total evenly across t_start..t_end (inclusive)
        into a per-year list aligned with _CHT_YEARS. Negative (cost)."""
        arr = [0.0] * len(_CHT_YEARS)
        if total_nom <= 0 or t_end < t_start:
            return arr
        n_yrs = t_end - t_start + 1
        per_yr = total_nom / n_yrs
        for t in range(t_start, t_end + 1):
            yr = 2026 + t
            if 2026 <= yr <= _CHT_YEARS[-1]:
                arr[_CHT_YEARS.index(yr)] = -per_yr
        return arr

    def _at_year(t_year, value):
        """Place a single nominal value at year 2026 + t_year. Negative."""
        arr = [0.0] * len(_CHT_YEARS)
        if value <= 0:
            return arr
        yr = 2026 + t_year
        if 2026 <= yr <= _CHT_YEARS[-1]:
            arr[_CHT_YEARS.index(yr)] = -value
        return arr

    # EIS years for the selected player
    if _cfa_player_is_b:
        _nb_eis_t      = _CFA_B_NB_EIS_T
        _wb_eis_t      = _CFA_B_WB_EIS_T
        _rate_hike_t   = 6   # FIXED-CALENDAR 2032, EIS-independent
    else:
        _nb_eis_t      = _CFA_A_NB_EIS_T
        _wb_eis_t      = _CFA_A_WB_EIS_T
        _rate_hike_t   = 0   # Airbus has no rate hike
    # Sabotage stays as spread (it's a multi-year op cost, not CAPEX)
    _sab_t0, _sab_t1 = max(0, _CFA_B_NB_EIS_T - 9), _CFA_B_NB_EIS_T - 1
    _fine_t          = _CFA_B_NB_EIS_T

    # Bars: CAPEX = single lump at EIS year (Option B)
    _cfa_cap_nb    = _at_year(_nb_eis_t, nom_invest_nb)
    _cfa_cap_wb    = _at_year(_wb_eis_t, nom_invest_wb)
    # Debt penalty: charged at the same year(s) as CAPEX, weighted
    # proportionally so each segment's penalty contribution lands at its
    # own EIS year.
    _cfa_debt_pen = [0.0] * len(_CHT_YEARS)
    if delta_pen > 0 and nom_total > 0:
        _nb_pen = delta_pen * (nom_invest_nb / nom_total)
        _wb_pen = delta_pen * (nom_invest_wb / nom_total)
        for t, v in ((_nb_eis_t, _nb_pen), (_wb_eis_t, _wb_pen)):
            if v > 0:
                yr = 2026 + t
                if 2026 <= yr <= _CHT_YEARS[-1]:
                    _cfa_debt_pen[_CHT_YEARS.index(yr)] -= v
    # Strain: same treatment — split across the two CAPEX-year lumps
    _cfa_strain = [0.0] * len(_CHT_YEARS)
    if strain > 0 and nom_total > 0:
        _nb_str = strain * (nom_invest_nb / nom_total)
        _wb_str = strain * (nom_invest_wb / nom_total)
        for t, v in ((_nb_eis_t, _nb_str), (_wb_eis_t, _wb_str)):
            if v > 0:
                yr = 2026 + t
                if 2026 <= yr <= _CHT_YEARS[-1]:
                    _cfa_strain[_CHT_YEARS.index(yr)] -= v
    _cfa_rate_hike = _at_year(_rate_hike_t, rate_hike_nominal)
    _cfa_sab       = _spread(nom_sabotage, _sab_t0, _sab_t1)
    _cfa_naked     = _at_year(_fine_t, naked_fine)

    # ── Build chart DataFrame ──
    # All bar values are NOMINAL ($B). Per-year revenue bars include CPI
    # escalation; cost stack at 2037 holds the full nominal totals.
    _cfa_label_nb = ("fps R&D + CAPEX (nominal)" if (_cfa_player_is_b and _cfa_b_launches)
                     else ("NGSA Build (nominal)" if (not _cfa_player_is_b and _cfa_a_launches)
                           else "NB CAPEX (nominal)"))
    _cfa_label_wb = ("787 Re-engine (nominal)" if (_cfa_player_is_b and _cfa_b_reengines)
                     else ("A350 Re-engine (nominal)" if (not _cfa_player_is_b and _cfa_a_reengines)
                           else "WB CAPEX (nominal)"))

    _cfa_chart_dict = {
        "Δ NB revenue (nominal)": _cfa_delta_nb_pv,
        "Δ WB revenue (nominal)": _cfa_delta_wb_pv,
        _cfa_label_nb:            _cfa_cap_nb,
        _cfa_label_wb:            _cfa_cap_wb,
        "Two-Front Strain":       _cfa_strain,
        "Debt Penalty (Δ α-quadratic)": _cfa_debt_pen,
    }
    if _cfa_player_is_b:
        _cfa_chart_dict["Rate-Hike Cost (nominal)"] = _cfa_rate_hike
    else:
        _cfa_chart_dict["Sabotage Op (nominal)"] = _cfa_sab
        _cfa_chart_dict["Naked Espionage Fine"]  = _cfa_naked

    # Drop columns that are entirely zero
    _cfa_chart_dict = {k: v for k, v in _cfa_chart_dict.items()
                       if any(abs(x) > 1e-6 for x in v)}

    _cfa_df = pd.DataFrame(_cfa_chart_dict, index=pd.Index(_CHT_YEARS, name="Year"))
    st.bar_chart(_cfa_df, height=340, use_container_width=True, stack=True)

    # ── Caption: sum of bars (nominal) + NPV equivalent (dashboard math) ──
    _cfa_nominal_total = sum(sum(v) for v in _cfa_chart_dict.values())

    # NPV equivalent = the same Δ EV the airframer math receipt reports.
    # Revenue side: WACC-discounted, no CPI (mirrors evaluate_scenario).
    # Cost side: PV-discounted CAPEX, plus nominal strain / debt penalty
    # / rate-hike-PV / sabotage-PV / naked-fine (matches the receipt).
    # PV-discount strain (same time profile as CAPEX) and naked fine (to
    # fps EIS year) so the caption's NPV matches the simulator's math.
    wacc_self = _CFA_WACC_B if _cfa_player_is_b else _CFA_WACC_A
    strain_pv = strain * (pv_total / nom_total) if nom_total > 0 else strain
    naked_pv  = naked_fine / ((1.0 + wacc_self) ** _CFA_B_NB_EIS_T) if naked_fine > 0 else 0.0

    _cfa_npv_total = (
        _cfa_delta_nb_pv_npv + _cfa_delta_wb_pv_npv
        - pv_nb_invest - pv_wb_invest
        - delta_pen - strain_pv
        - (rate_hike_pv if _cfa_player_is_b else 0.0)
        - (sabotage_pv if not _cfa_player_is_b else 0.0)
        - (naked_pv    if not _cfa_player_is_b else 0.0)
    )

    _cfa_ev = _CFA_EV_BOEING if _cfa_player_is_b else _CFA_EV_AIRBUS
    _cfa_implied_yield = 100.0 + (_cfa_npv_total / _cfa_ev) * 100.0

    st.caption(
        f"**{_cf_af_player}** — bars show NOMINAL cash flow per year "
        f"(price × units × share × margin × (1+CPI)^t, CPI = {_CFA_CPI*100:.1f}%). "
        f"**Option B convention**: all CAPEX/NRE recognized as a single lump at "
        f"each program's EIS year (NB at {2026+_nb_eis_t}, WB at {2026+_wb_eis_t}). "
        f"Sabotage is a multi-year op cost (spread {2026+_sab_t0}-{2026+_sab_t1}). "
        f"Rate hike at {2026+_rate_hike_t}; naked fine at {2026+_fine_t}. "
        f"Debt penalty + strain are split between the two CAPEX-year lumps. "
        f"**Per-program NPV windows (Phase A, 20 yrs post-EIS inclusive):** "
        f"NB = 2026 → **{2026 + _cfa_my_nb_end_t}**; "
        f"WB = 2026 → **{2026 + _cfa_my_wb_end_t}**.  \n"
        f"**Sum of all bars = ${_cfa_nominal_total:+.2f}B (nominal Δ).** "
        f" \n"
        f"**NPV equivalent (dashboard math): ${_cfa_npv_total:+.2f}B Δ EV** "
        f"→ implied yield {_cfa_implied_yield:.0f}% "
        f"(uses WACC_{'B' if _cfa_player_is_b else 'A'} = "
        f"{(_CFA_WACC_B if _cfa_player_is_b else _CFA_WACC_A)*100:.1f}%; "
        f"all costs PV-discounted to 2026)."
    )

def run_summary_tab():

    st.markdown("""
    <style>
    .sum-card {
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px;
        padding: 18px 22px; margin-bottom: 14px;
    }
    .sum-title {
        color: #58a6ff; font-size: 14px; font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
        border-bottom: 1px solid #30363d; padding-bottom: 6px; margin-bottom: 12px;
        letter-spacing: 1px; text-transform: uppercase;
    }
    .sum-section {
        font-family: 'Courier New', Courier, monospace;
        color: #58a6ff; font-size: 16px; font-weight: bold;
        letter-spacing: 2px; margin: 18px 0 12px 0;
        padding-bottom: 6px; border-bottom: 2px solid #1f6feb;
    }
    .sum-kv { font-family: 'Courier New', Courier, monospace; font-size: 12px;
              color: #ddd; line-height: 1.7; }
    .sum-kv .lbl { color: #888; }
    .sum-kv .val { color: #fff; font-weight: bold; }
    .sum-kv .hi  { color: #58a6ff; font-weight: bold; }
    .player-a-s  { color: #00BFFF; font-weight: bold; }
    .player-b-s  { color: #32CD32; font-weight: bold; }
    .player-c-s  { color: #FFA500; font-weight: bold; }
    .pw-locked   { color: #FFD700; font-weight: bold; }
    .stale-warn { background:#2a1a00;border:1px solid #5a4400;border-left:3px solid #d29922;
                  border-radius:4px; padding:8px 12px; font-size:11px; color:#d29922;
                  font-family: 'Courier New', Courier, monospace; margin-top: 8px; }

    /* Equilibrium tables (rows = players, cols = NB/WB) */
    .eq-wrap {
        background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
        padding: 14px 16px; margin-bottom: 12px;
    }
    .eq-wrap.pure  { border-left: 4px solid #3cb371; }
    .eq-wrap.near  { border-left: 4px solid #FFD700; }
    .eq-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 10px; font-family: 'Courier New', Courier, monospace;
    }
    .eq-tag {
        font-size: 10px; font-weight: bold; padding: 2px 8px;
        border-radius: 3px; letter-spacing: 2px;
    }
    .eq-tag.pure { background: #1a4a1a; color: #3cb371; }
    .eq-tag.near { background: #4a3a1a; color: #FFD700; }
    .eq-yields { font-size: 12px; color: #aaa; }
    .eq-table {
        width: 100%; border-collapse: collapse;
        font-family: 'Courier New', Courier, monospace; font-size: 12px;
    }
    .eq-table th {
        background: #1a1f36; color: #58a6ff; padding: 6px 10px;
        text-align: left; font-weight: bold; font-size: 11px;
        letter-spacing: 1px; border-bottom: 1px solid #30363d;
    }
    .eq-table th.market { text-align: center; width: 40%; }
    .eq-table th.player { width: 20%; }
    .eq-table td {
        padding: 8px 10px; border-bottom: 1px solid #1a1a1a;
        color: #ddd; vertical-align: middle;
    }
    .eq-table td.player {
        font-weight: bold; background: #0a0e1a; font-size: 11px;
        letter-spacing: 1px;
    }
    .eq-table td.market { color: #fff; }
    .eq-table td.muted { color: #555; font-style: italic; }
    .eq-table .yield-pill {
        display: inline-block; padding: 1px 8px; border-radius: 10px;
        background: #1a1f36; font-weight: bold; font-size: 11px;
    }
    .none-msg { color: #666; font-style: italic; padding: 6px 0;
                font-family: 'Courier New', monospace; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

    st.title("📋 Game Summary — At a Glance")
    st.caption("Equilibria first; assumptions below. "
               "Visit the Airframer and Engine tabs at least once to populate Nash results.")

    ss = st.session_state

    # ============================================================
    # EQUILIBRIUM SUMMARY TABLES (mirrored from Airframer / Engine tabs)
    # ============================================================
    _af_hdr = ss.get("_af_summary_header_html")
    _en_hdr = ss.get("_en_summary_header_html")
    if _af_hdr or _en_hdr:
        # Airframers block
        if _af_hdr:
            st.markdown(
                "<div style='font-family:\"Courier New\",monospace;color:#58a6ff;"
                "font-size:16px;font-weight:bold;letter-spacing:2px;margin:6px 0 6px 0;"
                "padding-bottom:4px;border-bottom:2px solid #1f6feb;'>✈️ AIRFRAMERS</div>",
                unsafe_allow_html=True)
            st.markdown(_af_hdr, unsafe_allow_html=True)
            st.markdown(ss.get("_af_combined_table_html", ""), unsafe_allow_html=True)
        else:
            st.info("Visit the Airframer tab to populate its equilibrium summary.")

        # Engines block
        if _en_hdr:
            st.markdown(
                "<div style='font-family:\"Courier New\",monospace;color:#58a6ff;"
                "font-size:16px;font-weight:bold;letter-spacing:2px;margin:18px 0 6px 0;"
                "padding-bottom:4px;border-bottom:2px solid #1f6feb;'>🔧 ENGINES</div>",
                unsafe_allow_html=True)
            st.markdown(_en_hdr, unsafe_allow_html=True)
            st.markdown(ss.get("_en_combined_table_html", ""), unsafe_allow_html=True)
        else:
            st.info("Visit the Engine tab to populate its equilibrium summary.")
        st.markdown("<hr style='border:0;border-top:1px solid #30363d;margin:20px 0;'>",
                    unsafe_allow_html=True)
    else:
        st.warning("⚠️ Visit the Airframer and Engine tabs to populate the equilibrium summaries above.")

    # ── Read controls (with defaults matching the widget defaults) ──
    b_sup       = ss.get("_b_supplier", "RR")
    a_sup       = ss.get("_a_supplier", "PW")
    b_code      = SUPPLIER_CODE.get(b_sup, 1)
    a_code      = SUPPLIER_CODE.get(a_sup, 2)
    boeing_share = int(ss.get("_boeing_share_both", 50))
    airbus_share = 100 - boeing_share

    # Aircraft prices ($M)
    p_737  = float(ss.get("af_price_737",  48.0))
    p_a320 = float(ss.get("af_price_a320", 52.0))
    p_fps  = float(ss.get("af_price_fps",  55.0))
    p_ngsa = float(ss.get("af_price_ngsa", 55.0))
    p_wb   = float(ss.get("af_price_wb",  180.0))

    # Operational margins
    m_a320 = float(ss.get("af_m_a320", 13.14))
    m_ngsa = float(ss.get("af_m_ngsa", 26.28))
    m_a350 = float(ss.get("af_m_a350",  4.95))
    m_737  = float(ss.get("af_m_737",   8.0))
    m_fps  = float(ss.get("af_m_fps",  25.64))
    m_787  = float(ss.get("af_m_787",  20.0))
    # Conditional WB margins (apply post-re-engine EIS)
    m_a350_alone = float(ss.get("af_m_a350_alone",  10.76))
    m_a350_both  = float(ss.get("af_m_a350_both",   6.47))
    m_787_alone  = float(ss.get("af_m_787_alone",  25.21))
    m_787_both   = float(ss.get("af_m_787_both",   15.77))

    # CAPEX / NRE
    cx_fps7   = float(ss.get("af_cx_fps7",   60.69))
    cx_fps10  = float(ss.get("af_cx_fps10",  55.25))
    cx_fpsemb = float(ss.get("af_cx_fpsemb", 100.00))
    cx_ngsa   = float(ss.get("af_cx_ngsa",   30.07))
    cx_787re  = float(ss.get("af_cx_787re",   5.00))
    cx_a350re = float(ss.get("af_cx_a350re",  5.00))
    cx_737rate = float(ss.get("af_cx_737rate", 2.94))

    # Engine balance sheets
    ev_a = float(ss.get("en_ev_a", 160.0)); debt_a = float(ss.get("en_debt_a", 35.0))
    ev_b = float(ss.get("en_ev_b", 110.0)); debt_b = float(ss.get("en_debt_b", 40.0))
    ev_c = float(ss.get("en_ev_c", 110.0)); debt_c = float(ss.get("en_debt_c", 40.0))

    # R&D
    rd_cfm_open_fan = float(ss.get("en_rd_cfm_open_fan", 8.0))
    rd_cfm_ducted   = float(ss.get("en_rd_cfm_ducted",   4.0))
    rd_pw_solo      = float(ss.get("en_rd_pw_solo",      2.0))
    rd_pw_jv        = float(ss.get("en_rd_pw_jv",        2.0))
    rd_rr_nb    = float(ss.get("en_rd_rr_nb",    8.0))
    rd_rr_wb    = float(ss.get("en_rd_rr_wb",    4.0))
    rd_rr_t1000 = float(ss.get("en_rd_rr_t1000", 2.0))

    # Derived engine NB shares (post-2037)
    rr_pct, pw_pct, cfm_pct = derive_nb_engine_shares(b_code, a_code, boeing_share)

    # PW locked move + RR posture
    _all_engines = supplier_engines(b_code) | supplier_engines(a_code)
    if is_jv(b_code) or is_jv(a_code):
        pw_lock = "3-JV with RR for GTF"
        pw_why  = "an airframer chose RR & PW (JV)"
    elif "PW" in _all_engines:
        pw_lock = "2-Launch GTF2 Go Solo"
        pw_why  = "an airframer chose PW (solo)"
    else:
        pw_lock = "1-Milk GTF"
        pw_why  = "neither airframer selected PW"

    if "RR" not in _all_engines:           rr_posture = "Do Nothing (no airframer)"
    elif is_jv(b_code) or is_jv(a_code):   rr_posture = "JV with PW for NB"
    else:                                   rr_posture = "Solo or Do Nothing"

    # ============================================================
    # Top context strip — supplier / share / PW lock at a glance
    # ============================================================
    st.markdown(
        f"<div style='background:#0d1117;border:1px solid #30363d;border-left:4px solid #58a6ff;"
        f"border-radius:6px;padding:10px 14px;margin-bottom:12px;font-family:monospace;font-size:12px;color:#ddd;'>"
        f"🔌 <span class='player-b-s'>Boeing fps → {b_sup} ({boeing_share}%)</span> &nbsp;|&nbsp; "
        f"<span class='player-a-s'>Airbus NGSA → {a_sup} ({airbus_share}%)</span> &nbsp;|&nbsp; "
        f"<b>NB engines:</b> CFM {cfm_pct:.0f}% · PW {pw_pct:.0f}% · RR {rr_pct:.0f}% &nbsp;|&nbsp; "
        f"<b>PW lock:</b> <span class='pw-locked'>{pw_lock}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ============================================================
    # STRATEGY DECODERS — turn raw move tuples into NB/WB cell text
    # ============================================================
    def af_decode(a_strat, b_strat):
        """
        Airbus tuple: (NGSA-move, Bottleneck, Poaching, A350-move)
        Boeing tuple: (fps-move, 737-rate, 787-move)
        Returns dict {player: {"NB": str, "WB": str}}
        """
        # Pretty-printers
        def pp(m):
            return (str(m).replace("Launch_", "Launch ").replace("Sabotage_", "Delay fps ")
                          .replace("Re_engine_", "Re-engine ").replace("Increase_", "Increase ")
                          .replace("_Solo", " Solo").replace("_via_Embraer", " via Embraer")
                          .replace("_Rate", " Rate").replace("_", " ").strip())
        # Airbus
        ngsa, btl, poach, a350 = a_strat
        a_nb_parts = [pp(ngsa)]
        if "No" not in btl:   a_nb_parts.append(f"+ {pp(btl)}")
        if "No" not in poach: a_nb_parts.append(f"+ {pp(poach)}")
        a_nb = "  ".join(a_nb_parts)
        a_wb = pp(a350)
        # Boeing
        fps, rate, b787 = b_strat
        b_nb_parts = [pp(fps)]
        if "No" not in rate: b_nb_parts.append(f"+ {pp(rate)}")
        b_nb = "  ".join(b_nb_parts)
        b_wb = pp(b787)
        return {
            "Airbus": {"NB": a_nb, "WB": a_wb, "color": "00BFFF", "klass": "player-a-s"},
            "Boeing": {"NB": b_nb, "WB": b_wb, "color": "32CD32", "klass": "player-b-s"},
        }

    def en_decode(a_str, c_str, pw_locked):
        """
        Engine player A (CFM): single string from a_filt — has both NB and possibly WB tag
        Engine player C (RR):  string of form "<NB-piece> | <WB-piece>" or "<NB-piece>"
        PW: locked move string (NB only — PW has no WB)
        """
        # CFM strings encode multiple groups separated by " | ":
        # NB tech / NB partnership / NB regulatory / WB tech. Classify each
        # piece by its move name (mirrors _en_split_pipe in run_engine_board).
        def split_pipe(s):
            s = str(s).strip()
            if not s:
                return "", ""
            pieces = [p.strip() for p in s.split(" | ")]
            nb_pieces, wb_pieces = [], []
            WB_NAMES = ("Upgrade GenX9", "Invest GenX",        # CFM Group D
                        "Ultrafan WB",   "Upgrade T1000")      # RR  Group B
            for p in pieces:
                if any(name in p for name in WB_NAMES):
                    wb_pieces.append(p)
                else:
                    nb_pieces.append(p)
            return " | ".join(nb_pieces), " | ".join(wb_pieces)

        cfm_nb, cfm_wb = split_pipe(str(a_str))
        rr_nb,  rr_wb  = split_pipe(str(c_str))

        return {
            "CFM/GE": {"NB": cfm_nb or "—", "WB": cfm_wb or "Milk GEnx",
                       "color": "00BFFF", "klass": "player-a-s"},
            "PW":     {"NB": pw_locked,    "WB": "(no WB platform)",
                       "color": "32CD32", "klass": "player-b-s"},
            "RR":     {"NB": rr_nb or "Do Nothing", "WB": rr_wb or "Milk Trent",
                       "color": "FFA500", "klass": "player-c-s"},
        }

    def render_eq_table(idx, kind, decoded, yields, game_label):
        """Render one equilibrium as a player-rows × {NB,WB}-cols table."""
        klass = "pure" if kind == "pure" else "near"
        tag_text = "PURE NASH" if kind == "pure" else "NEAR-NASH"
        yield_html = " &nbsp;·&nbsp; ".join(
            f"<span class='{decoded[p]['klass']}'>{p}: {y:.1f}%</span>"
            for p, y in yields.items()
        )

        rows_html = []
        for player, info in decoded.items():
            rows_html.append(
                f"<tr>"
                f"<td class='player {info['klass']}'>{player}</td>"
                f"<td class='market'>{info['NB']}</td>"
                f"<td class='market'>{info['WB']}</td>"
                f"</tr>"
            )

        st.markdown(
            f"<div class='eq-wrap {klass}'>"
            f"<div class='eq-header'>"
            f"<span><span class='eq-tag {klass}'>{tag_text}</span> "
            f"&nbsp;<b style='color:#fff;'>#{idx+1}</b> "
            f"<span style='color:#888;'>· {game_label}</span></span>"
            f"<span class='eq-yields'>{yield_html}</span>"
            f"</div>"
            f"<table class='eq-table'>"
            f"<tr><th class='player'>Player</th>"
            f"<th class='market'>Narrowbody</th>"
            f"<th class='market'>Widebody</th></tr>"
            f"{''.join(rows_html)}"
            f"</table>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ============================================================
    # SECTION C — KEY ASSUMPTIONS
    # ============================================================
    st.markdown("<div class='sum-section'>📐 KEY ASSUMPTIONS</div>",
                unsafe_allow_html=True)

    # Row 1: Suppliers + Market split + Postures
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>🔌 Engine Supplier Selection</div>
            <div class='sum-kv'>
                <span class='lbl'>Boeing fps supplier:</span>
                &nbsp;<span class='player-b-s'>{b_sup}</span><br/>
                <span class='lbl'>Airbus NGSA supplier:</span>
                &nbsp;<span class='player-a-s'>{a_sup}</span><br/>
                <span class='lbl'>Selection code:</span>
                &nbsp;<span class='hi'>({b_code}, {a_code})</span><br/>
                <span class='lbl'>Engines in play:</span>
                &nbsp;<span class='val'>{', '.join(sorted(_all_engines))}</span>
            </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>📊 Post-2037 NB Market Share (when both launch)</div>
            <div class='sum-kv'>
                <span class='lbl'>Boeing fps:</span>
                &nbsp;<span class='player-b-s'>{boeing_share}%</span> &nbsp;
                <span class='lbl'>|</span> &nbsp;
                <span class='lbl'>Airbus NGSA:</span>
                &nbsp;<span class='player-a-s'>{airbus_share}%</span><br/>
                <hr style='border:0;border-top:1px solid #222;margin:8px 0;'/>
                <span class='lbl'>Derived engine market:</span><br/>
                &nbsp;&nbsp;CFM: <span class='val'>{cfm_pct:.0f}%</span> &nbsp;·&nbsp;
                PW: <span class='val'>{pw_pct:.0f}%</span> &nbsp;·&nbsp;
                RR: <span class='val'>{rr_pct:.0f}%</span>
            </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Row 2: Postures
    st.markdown(
        f"""<div class='sum-card' style='border-left:4px solid #FFD700;'>
        <div class='sum-title'>♟️ Engine-Player Postures (Derived)</div>
        <div class='sum-kv'>
            <b>Player B (PW)</b> — locked move:
            &nbsp;<span class='pw-locked'>{pw_lock}</span><br/>
            &nbsp;&nbsp;<span style='color:#888;font-style:italic;'>Rationale: {pw_why}.</span><br/><br/>
            <b>Player C (RR)</b> — posture:
            &nbsp;<span class='player-c-s'>{rr_posture}</span>
        </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # Row 3: Prices + Margins
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>✈️ Aircraft Prices ($M / a/c)</div>
            <div class='sum-kv'>
                <span class='lbl'>Current-gen NB:</span><br/>
                &nbsp;&nbsp;737 MAX: <span class='val'>${p_737:.0f}M</span> &nbsp;|&nbsp;
                A320neo: <span class='val'>${p_a320:.0f}M</span><br/>
                <span class='lbl'>Next-gen NB (EIS 2037):</span><br/>
                &nbsp;&nbsp;Boeing fps: <span class='player-b-s'>${p_fps:.0f}M</span> &nbsp;|&nbsp;
                Airbus NGSA: <span class='player-a-s'>${p_ngsa:.0f}M</span><br/>
                <span class='lbl'>Widebody (787 / A350):</span>
                &nbsp;<span class='val'>${p_wb:.0f}M</span>
            </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>⚙️ Operational Margins (%)</div>
            <div class='sum-kv'>
                <span class='lbl'>Airbus:</span><br/>
                &nbsp;&nbsp;A320: <span class='val'>{m_a320:.1f}%</span> &nbsp;|&nbsp;
                NGSA: <span class='val'>{m_ngsa:.1f}%</span> &nbsp;|&nbsp;
                A350 WB: <span class='val'>{m_a350:.1f}%</span><br/>
                <span class='lbl'>Boeing:</span><br/>
                &nbsp;&nbsp;737: <span class='val'>{m_737:.1f}%</span> &nbsp;|&nbsp;
                fps: <span class='val'>{m_fps:.1f}%</span> &nbsp;|&nbsp;
                787 WB: <span class='val'>{m_787:.1f}%</span>
            </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Row 4: NRE/CAPEX + Engine R&D
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>⚔️ Airframer Non-Recurring Spend ($B)</div>
            <div class='sum-kv'>
                <span class='lbl'>NB launch programs:</span><br/>
                &nbsp;&nbsp;fps 7yr Solo: <span class='val'>${cx_fps7:.2f}B</span><br/>
                &nbsp;&nbsp;fps 10yr Solo: <span class='val'>${cx_fps10:.2f}B</span><br/>
                &nbsp;&nbsp;fps via Embraer: <span class='val'>${cx_fpsemb:.2f}B</span><br/>
                &nbsp;&nbsp;NGSA Build: <span class='val'>${cx_ngsa:.2f}B</span><br/>
                <span class='lbl'>WB re-engine:</span><br/>
                &nbsp;&nbsp;787 Re-engine: <span class='val'>${cx_787re:.2f}B</span><br/>
                &nbsp;&nbsp;A350 Re-engine: <span class='val'>${cx_a350re:.2f}B</span><br/>
                <span class='lbl'>Production-rate ramp:</span><br/>
                &nbsp;&nbsp;737 Rate Hike (2032 PV): <span class='val'>${cx_737rate:.2f}B</span>
            </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class='sum-card'>
            <div class='sum-title'>💰 Engine R&D ($B) + Balance Sheets</div>
            <div class='sum-kv'>
                <span class='lbl'>R&amp;D (all conditional — milk = no charge):</span><br/>
                &nbsp;&nbsp;CFM Open Fan: <span class='val'>${rd_cfm_open_fan:.1f}B</span><br/>
                &nbsp;&nbsp;CFM Ducted: <span class='val'>${rd_cfm_ducted:.1f}B</span><br/>
                &nbsp;&nbsp;PW GTF2 Solo: <span class='val'>${rd_pw_solo:.1f}B</span><br/>
                &nbsp;&nbsp;PW GTF2 JV: <span class='val'>${rd_pw_jv:.1f}B</span><br/>
                &nbsp;&nbsp;RR Ultrafan — NB: <span class='val'>${rd_rr_nb:.1f}B</span><br/>
                &nbsp;&nbsp;RR Ultrafan — WB: <span class='val'>${rd_rr_wb:.1f}B</span><br/>
                &nbsp;&nbsp;RR T1000 Upgrade: <span class='val'>${rd_rr_t1000:.1f}B</span><br/>
                <hr style='border:0;border-top:1px solid #222;margin:6px 0;'/>
                <span class='lbl'>Engine balance sheets (EV / Debt):</span><br/>
                &nbsp;&nbsp;<span class='player-a-s'>CFM/GE</span>: ${ev_a:.0f}B / ${debt_a:.0f}B<br/>
                &nbsp;&nbsp;<span class='player-b-s'>PW</span>: ${ev_b:.0f}B / ${debt_b:.0f}B<br/>
                &nbsp;&nbsp;<span class='player-c-s'>RR</span>: ${ev_c:.0f}B / ${debt_c:.0f}B
            </div>
            </div>""",
            unsafe_allow_html=True,
        )

    # ============================================================
    # SECTION C2 — fps LAUNCH SENSITIVITY (LIVE TORNADO)
    # Self-contained tornado chart that mirrors the static
    # /fps-tornado-chart skill, but reads its inputs from the
    # current dashboard session_state. The math is a copy of
    # the airframer evaluate_scenario(), specialised to the two
    # cells that matter for this analysis:
    #   Base case  : Boeing Launch fps (10-yr) + Re-engine 787,
    #                Airbus best response.
    #   Benchmark  : Boeing Do Nothing (Milk 737) + Re-engine 787,
    #                Airbus best response.
    # No existing dashboard logic is touched.
    # ============================================================
    st.markdown("<div class='sum-section'>📊 fps LAUNCH SENSITIVITY (LIVE TORNADO)</div>",
                unsafe_allow_html=True)
    st.caption("How robust is Boeing's fps launch upside? Each factor is swept across "
               "a realistic real-world range, holding everything else at the current "
               "dashboard values. Updates live as you adjust the sidebar parameters.")

    # ---- Read every parameter the calculation needs from session_state ----
    _TIMELINE_YRS    = 31
    _NPV_POST_EIS_YRS = 20   # Per-program window — pre-EIS legacy + 20 yrs post-EIS
    _NB_PER_YR    = 2000
    _WB_PER_YR    = 170
    _WACC_B       = 0.105
    _WACC_A       = 0.080

    # Prices ($M -> $B by /1000, mirroring run_airframer_board's wiring)
    _PRICE_737  = float(ss.get('af_price_737',  48.0))  / 1000.0
    _PRICE_A320 = float(ss.get('af_price_a320', 52.0))  / 1000.0
    _PRICE_fps  = float(ss.get('af_price_fps',  55.0))  / 1000.0
    _PRICE_NGSA = float(ss.get('af_price_ngsa', 55.0))  / 1000.0
    _PRICE_WB   = float(ss.get('af_price_wb',  180.0))  / 1000.0
    # Margins (% -> fraction)
    _M_737   = float(ss.get('af_m_737',   8.00))  / 100.0
    _M_A320  = float(ss.get('af_m_a320', 13.14))  / 100.0
    _M_FPS   = float(ss.get('af_m_fps',  25.64))  / 100.0
    _M_NGSA  = float(ss.get('af_m_ngsa', 26.28))  / 100.0
    _M_787   = float(ss.get('af_m_787',  20.00))  / 100.0
    _M_A350  = float(ss.get('af_m_a350',  4.95))  / 100.0
    # Conditional WB margins (apply post-re-engine; default to status quo)
    _M_787_ALONE  = float(ss.get('af_m_787_alone',  25.21))  / 100.0
    _M_787_BOTH   = float(ss.get('af_m_787_both',   15.77))  / 100.0
    _M_A350_ALONE = float(ss.get('af_m_a350_alone',  10.76))  / 100.0
    _M_A350_BOTH  = float(ss.get('af_m_a350_both',   6.47))  / 100.0
    # CAPEX ($B)
    _CX_FPS_10YR  = float(ss.get('af_cx_fps10', 55.25))
    _CX_NGSA      = float(ss.get('af_cx_ngsa',  30.07))
    _CX_787RE     = float(ss.get('af_cx_787re',  5.00))
    _CX_A350RE    = float(ss.get('af_cx_a350re', 5.00))
    # Balance sheets
    _EV_BOEING    = float(ss.get('af_ev_boeing',  130.0))
    _DEBT_BOEING  = float(ss.get('af_debt_boeing', 45.0))
    # Strain & shares
    _STRAIN_B     = float(ss.get('af_strain_b',    5.94))
    _NAKED_FINE   = float(ss.get('af_naked_fine', 48.32))
    _NB_MILKER    = float(ss.get('af_nb_milker',  30.0))  / 100.0
    _WB_MILKER    = float(ss.get('af_wb_milker',  15.0))  / 100.0
    _SAB_SHARE    = float(ss.get('af_sab_share',   5.0))  # in % per move
    _SAB_COST     = float(ss.get('af_sab_cost',    1.0))  # $B per move
    _ALPHA        = float(ss.get('af_alpha',       0.3))
    _B_SHARE_PCT  = float(ss.get('_boeing_share_both', 50.0))
    _FPS_7YR_ADV  = float(ss.get('af_fps_7yr_adv', 5.0))  # 7yr ramp bonus pp
    # WB EIS years (per-platform sliders)
    _B_WB_EIS_T   = max(0, int(ss.get('af_787_eis',  2041)) - 2026)
    _A_WB_EIS_T   = max(0, int(ss.get('af_a350_eis', 2035)) - 2026)
    # NB EIS years (per-program sliders)
    _B_NB_EIS_T   = max(0, int(ss.get('af_fps_eis',  2037)) - 2026)
    _A_NB_EIS_T   = max(0, int(ss.get('af_ngsa_eis', 2037)) - 2026)

    # ---- Helper: PV stream, debt-aware true-cost penalty, status-quo baseline ----
    def _pv_stream(nominal, t0, t1, wacc):
        if nominal == 0:
            return 0.0
        annual = nominal / (t1 - t0 + 1)
        return sum(annual / ((1.0 + wacc) ** t) for t in range(t0, t1 + 1))

    def _true_cost(nominal_capex, pv_capex, debt, ev, alpha):
        if nominal_capex <= 0:
            return 0.0
        base_pen      = debt * alpha * (debt / ev) ** 2
        new_d         = debt + nominal_capex
        new_pen       = new_d * alpha * (new_d / ev) ** 2
        delta_pen_nom = new_pen - base_pen
        # Same PV-discount logic as the airframer board's calculate_tc:
        # debt penalty slides with EIS via the CAPEX time profile.
        pv_factor     = pv_capex / nominal_capex
        return pv_capex + delta_pen_nom * pv_factor

    def _baseline_npv(price_737, m_737, price_wb, m_787):
        b_nb = b_wb = 0.0
        # Per-program windows (Phase A)
        _b_nb_end = _B_NB_EIS_T + _NPV_POST_EIS_YRS - 1
        _b_wb_end = _B_WB_EIS_T + _NPV_POST_EIS_YRS - 1
        _T_base = max(_TIMELINE_YRS, _b_nb_end + 1, _b_wb_end + 1)
        for t in range(_T_base):
            df = 1.0 / ((1.0 + _WACC_B) ** t)
            if t <= _b_nb_end:
                b_nb += _NB_PER_YR * 0.40 * price_737 * m_737 * df
            if t <= _b_wb_end:
                b_wb += _WB_PER_YR * (100.0 / 170.0) * price_wb * m_787 * df
        return b_nb, b_wb

    # ---- Boeing yield calculator for one cell (mirrors evaluate_scenario) ----
    def _boeing_yield(p):
        b_l, a_l   = p['b_launches'], p['a_launches']
        b_r, a_r   = p['b_reengines'], p['a_reengines']
        sabs       = p['active_sabs']

        b_inv_nb = p['cx_fps_10yr'] if b_l else 0.0
        a_inv_nb = p['cx_ngsa']     if a_l else 0.0
        # Option B: lump at EIS year
        b_pv_nb  = b_inv_nb / ((1.0 + _WACC_B) ** _B_NB_EIS_T)

        b_inv_wb = p['cx_787re']  if b_r else 0.0
        a_inv_wb = p['cx_a350re'] if a_r else 0.0
        b_pv_wb  = b_inv_wb / ((1.0 + _WACC_B) ** _B_WB_EIS_T)

        # NB / WB share rules are computed per-year below (no need for the
        # legacy "post-EIS share" precomputation under the unified rule).

        nb_milker_active = (b_l != a_l)
        wb_milker_active = (b_r != a_r)

        # Per-program end-t offsets for Boeing's segments
        _b_nb_end = _B_NB_EIS_T + _NPV_POST_EIS_YRS - 1
        _b_wb_end = _B_WB_EIS_T + _NPV_POST_EIS_YRS - 1
        # Outer loop extends to whichever window is longest (default sliders
        # give 31; late sliders extend).
        _T_dyn = max(_TIMELINE_YRS, _b_nb_end + 1, _b_wb_end + 1)

        b_nb_pv = b_wb_pv = 0.0
        for t in range(_T_dyn):
            df = 1.0 / ((1.0 + _WACC_B) ** t)
            # NB share — UNIFIED rule v2 (see _compute_nb_share_unified at top)
            sh, _ = _compute_nb_share_unified(t, b_l, a_l, _B_NB_EIS_T, _A_NB_EIS_T,
                                              is_7yr=p.get('is_7yr', False))
            _ash = 1.0 - sh
            sh, _ash = _apply_nb_modifiers(
                sh, _ash, t, _B_NB_EIS_T, _A_NB_EIS_T, b_l, a_l,
                b_inc_rate=p.get('inc_rate', False),
                is_7yr=p.get('is_7yr', False),
                fps_7yr_pp=p.get('fps_7yr_adv', 7.0),
                active_sabs=sabs, sab_share_pp=p['sab_share'])

            # Price / margin per program (per-program timing)
            if b_l and t >= _B_NB_EIS_T:
                pp, mm = p['price_fps'], p['m_fps']
            else:
                pp, mm = p['price_737'], p['m_737']
            if t <= _b_nb_end:
                b_nb_pv += _NB_PER_YR * sh * pp * mm * df

            # WB share — UNIFIED rule (mirrors evaluate_scenario):
            # No pre-EIS anticipation; per-case catch-up from EIS.
            if b_r and not a_r:
                # XOR Case E: Boeing alone re-engines
                if t < _B_WB_EIS_T:
                    sh_w = 100.0 / 170.0
                else:
                    years_in = t - _B_WB_EIS_T + 1
                    sh_w = min(1.0 - p['wb_milker'], 100/170 + _wb_gain_b() * years_in)
            elif a_r and not b_r:
                # XOR Case F: Airbus alone re-engines (Boeing's share = 1 - Airbus)
                if t < _A_WB_EIS_T:
                    sh_w = 100.0 / 170.0
                else:
                    years_in = t - _A_WB_EIS_T + 1
                    a_sh = min(0.60, 70/170 + _wb_gain_a() * years_in)
                    sh_w = 1.0 - a_sh
            elif b_r and a_r and _B_WB_EIS_T != _A_WB_EIS_T:
                if _B_WB_EIS_T < _A_WB_EIS_T:
                    if t < _B_WB_EIS_T:
                        sh_w = 100.0 / 170.0
                    else:
                        catch_t = min(t, _A_WB_EIS_T - 1)
                        years_in = catch_t - _B_WB_EIS_T + 1
                        sh_w = min(0.80, 100/170 + _wb_gain_b() * years_in)
                else:
                    if t < _A_WB_EIS_T:
                        sh_w = 100.0 / 170.0
                    else:
                        catch_t = min(t, _B_WB_EIS_T - 1)
                        years_in = catch_t - _A_WB_EIS_T + 1
                        a_sh = min(0.60, 70/170 + _wb_gain_a() * years_in)
                        sh_w = 1.0 - a_sh
            else:
                sh_w = 100.0 / 170.0
            if t <= _b_wb_end:
                # Conditional 787 margin: status quo until re-engine EIS, then
                # branch on whether A350 also re-engines.
                if b_r and t >= _B_WB_EIS_T:
                    m_787_t = p['m_787_both'] if a_r else p['m_787_alone']
                else:
                    m_787_t = p['m_787']
                b_wb_pv += _WB_PER_YR * sh_w * p['price_wb'] * m_787_t * df

        b_strain_nom = p['strain_b'] if (b_l and b_r) else 0.0
        b_nom    = b_inv_nb + b_inv_wb
        b_pv     = b_pv_nb + b_pv_wb
        b_strain = (b_strain_nom * (b_pv / b_nom) if b_nom > 0 else b_strain_nom)
        b_tc     = _true_cost(b_nom, b_pv, p['debt_boeing'],
                              _EV_BOEING, p['alpha'])

        b_base_nb, b_base_wb = _baseline_npv(p['price_737'], p['m_737'],
                                              p['price_wb'], p['m_787'])
        delta = (b_nb_pv - b_base_nb) + (b_wb_pv - b_base_wb) - b_tc - b_strain
        return 100.0 + (delta / _EV_BOEING) * 100.0

    # ---- Pack live parameters into one dict for the calculator ----
    def _make_params(**overrides):
        p = dict(
            price_737=_PRICE_737, price_a320=_PRICE_A320,
            price_fps=_PRICE_fps, price_ngsa=_PRICE_NGSA, price_wb=_PRICE_WB,
            m_737=_M_737, m_a320=_M_A320, m_fps=_M_FPS, m_ngsa=_M_NGSA,
            m_787=_M_787, m_a350=_M_A350,
            m_787_alone=_M_787_ALONE, m_787_both=_M_787_BOTH,
            m_a350_alone=_M_A350_ALONE, m_a350_both=_M_A350_BOTH,
            cx_fps_10yr=_CX_FPS_10YR, cx_ngsa=_CX_NGSA,
            cx_787re=_CX_787RE, cx_a350re=_CX_A350RE,
            debt_boeing=_DEBT_BOEING, strain_b=_STRAIN_B,
            nb_milker=_NB_MILKER, wb_milker=_WB_MILKER,
            sab_share=_SAB_SHARE, alpha=_ALPHA,
            boeing_share_pct=_B_SHARE_PCT,
            fps_7yr_adv=_FPS_7YR_ADV,
            inc_rate=False, is_7yr=False,
            b_launches=True, a_launches=True,
            b_reengines=True, a_reengines=False, active_sabs=2,
        )
        p.update(overrides)
        return p

    # Sweep Airbus's response (sabs ∈ {0,2}, a_reengines ∈ {True,False})
    # and pick Boeing's yield in the cell where Airbus best-responds.
    # We use a simplified Airbus-yield proxy here: when Boeing launches,
    # Airbus is known to prefer sabs=2 + Hold A350 (matches snapshot
    # Near-Nash #4 in the calibrated game). When Boeing holds, Airbus
    # prefers sabs=0 (no naked-fine risk) + the WB option that maximises
    # its NB+WB outcome — typically Hold A350 in current parameters.
    base_params = _make_params(
        b_launches=True, a_launches=True,
        b_reengines=True, a_reengines=False, active_sabs=2,
    )
    base_y = _boeing_yield(base_params)

    bench_params = _make_params(
        b_launches=False, a_launches=True,
        b_reengines=True, a_reengines=False, active_sabs=0,
    )
    bench_y = _boeing_yield(bench_params)

    # ---- Tornado factor sweep ----
    factors_def = [
        dict(name="Boeing debt level",
             param="debt_boeing",
             low=65.0, high=25.0,
             lo_lbl="$65B", hi_lbl="$25B",
             base_lbl=f"${_DEBT_BOEING:.0f}B"),
        dict(name="fps program CAPEX (10-yr)",
             param="cx_fps_10yr",
             low=48.0, high=25.0,
             lo_lbl="$48B", hi_lbl="$25B",
             base_lbl=f"${_CX_FPS_10YR:.1f}B"),
        dict(name="fps operating margin",
             param="m_fps",
             low=0.22, high=0.32,
             lo_lbl="22%", hi_lbl="32%",
             base_lbl=f"{_M_FPS*100:.2f}%"),
        dict(name="fps NB share post-launch",
             param="boeing_share_pct",
             low=42.0, high=60.0,
             lo_lbl="42%", hi_lbl="60%",
             base_lbl=f"{_B_SHARE_PCT:.0f}%"),
        dict(name="Airbus delay-tactic effectiveness",
             param="sab_share",
             low=10.0, high=0.0,
             lo_lbl="10%", hi_lbl="0%",
             base_lbl=f"{_SAB_SHARE:.0f}%"),
        dict(name="Two-front execution strain",
             param="strain_b",
             low=5.0, high=1.5,
             lo_lbl="$5B", hi_lbl="$1.5B",
             base_lbl=f"${_STRAIN_B:.2f}B"),
    ]

    factor_rows = []
    for f in factors_def:
        y_lo = _boeing_yield(_make_params(**{f['param']: f['low']},
                                          b_launches=True, a_launches=True,
                                          b_reengines=True, a_reengines=False,
                                          active_sabs=2))
        y_hi = _boeing_yield(_make_params(**{f['param']: f['high']},
                                          b_launches=True, a_launches=True,
                                          b_reengines=True, a_reengines=False,
                                          active_sabs=2))
        factor_rows.append(dict(
            name=f['name'],
            lo=round(y_lo - base_y, 2), hi=round(y_hi - base_y, 2),
            lo_lbl=f['lo_lbl'], hi_lbl=f['hi_lbl'], base_lbl=f['base_lbl'],
        ))

    # Sort by total impact (largest range at top — true tornado layout)
    factor_rows.sort(key=lambda r: abs(r['hi'] - r['lo']), reverse=True)

    # Persist for the Dashboard tab to consume
    st.session_state['_af_b_tornado_rows'] = factor_rows
    st.session_state['_af_b_base_y']  = float(base_y)
    st.session_state['_af_b_bench_y'] = float(bench_y)

    # ---- Render the tornado as HTML ----
    # Choose a symmetric x-axis range that fits both bars and the benchmark
    _max_abs = max(
        max(abs(r['lo']), abs(r['hi'])) for r in factor_rows
    )
    _bench_pp = bench_y - base_y
    _x_max = max(5 * round((max(_max_abs, abs(_bench_pp)) + 4) / 5), 5)

    # px width per percentage point (each side of the bar track)
    _track_w_px = 460   # half-width of the bar track in pixels
    _px_per_pp  = _track_w_px / _x_max

    # CSS for the tornado
    st.markdown("""
    <style>
    .torn-wrap {
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px;
        padding: 22px 24px 18px 24px; margin-bottom: 16px;
        font-family: 'Courier New', Courier, monospace;
    }
    .torn-subtitle { font-size: 13px; color: #ddd; margin-bottom: 18px; line-height: 1.6; }
    .torn-subtitle .lbl  { color: #888; }
    .torn-subtitle .base { color: #3cb371; font-weight: bold; }
    .torn-subtitle .bench { color: #d29922; font-weight: bold; }
    .torn-row {
        display: flex; align-items: center; gap: 14px;
        height: 56px; border-bottom: 1px solid #1a1a1a;
    }
    .torn-row:last-child { border-bottom: none; }
    .torn-name {
        flex: 0 0 220px; text-align: right; padding-right: 10px;
        font-size: 12px; color: #cfd9e7; font-weight: bold;
    }
    .torn-track {
        flex: 0 0 auto; position: relative;
        height: 36px;
    }
    .torn-axis-line {
        position: absolute; top: 2px; bottom: 2px; width: 0;
        border-left: 2px solid #58a6ff;
    }
    .torn-bench-line {
        position: absolute; top: 0; bottom: 0; width: 0;
        border-left: 1.5px dashed #d29922;
    }
    .torn-bar-down {
        position: absolute; top: 6px; height: 24px;
        background: #d29922; border: 1px solid #b07a16;
    }
    .torn-bar-up {
        position: absolute; top: 6px; height: 24px;
        background: #2f81f7; border: 1px solid #1f6feb;
    }
    .torn-val {
        position: absolute; top: 8px; height: 22px; line-height: 22px;
        font-size: 11px; font-weight: bold;
    }
    .torn-val-down { color: #d29922; }
    .torn-val-up   { color: #2f81f7; }
    .torn-val-down-inside, .torn-val-up-inside { color: #fff; }
    .torn-range {
        flex: 0 0 200px; padding-left: 10px;
        font-size: 11px; color: #888; font-style: italic;
    }
    .torn-range .basev { color: #fff; font-weight: bold; font-style: normal; }
    .torn-axis {
        display: flex; gap: 14px; align-items: center;
        margin-top: 10px; height: 22px;
    }
    .torn-axis-spacer-left  { flex: 0 0 220px; }
    .torn-axis-spacer-right { flex: 0 0 200px; }
    .torn-axis-track {
        flex: 0 0 auto; position: relative; height: 18px;
        border-top: 1px solid #444;
    }
    .torn-tick {
        position: absolute; top: -1px;
        font-size: 10px; color: #888; line-height: 1;
        transform: translateX(-50%);
    }
    .torn-tick-mark {
        position: absolute; top: -5px; height: 5px; width: 0;
        border-left: 1px solid #444; transform: translateX(-50%);
    }
    .torn-tick-label {
        position: absolute; top: 6px;
        font-size: 10px; color: #888;
        transform: translateX(-50%);
    }
    .torn-axis-title {
        text-align: center; margin: 8px 0 4px 234px;
        font-size: 11px; color: #888; font-style: italic;
    }
    .torn-bench-annot {
        text-align: left; margin: 2px 0 8px 234px;
        font-size: 11px; color: #d29922; font-weight: bold; font-style: italic;
    }
    .torn-foot {
        display: flex; gap: 14px; margin-top: 10px;
        font-size: 10px; letter-spacing: 2px; font-weight: bold;
    }
    .torn-foot-spacer-left  { flex: 0 0 220px; }
    .torn-foot-spacer-right { flex: 0 0 200px; }
    .torn-foot-track { flex: 0 0 auto; position: relative; height: 16px; }
    .torn-foot-down { position: absolute; left: 0; right: 50%; text-align: center;
                       color: #d29922; padding-right: 14px; }
    .torn-foot-base { position: absolute; left: 50%; transform: translateX(-50%);
                       color: #58a6ff; }
    .torn-foot-up   { position: absolute; left: 50%; right: 0; text-align: center;
                       color: #2f81f7; padding-left: 14px; }
    .torn-takeaway {
        background: #1a1f36; border: 1px solid #1f6feb;
        border-left: 4px solid #d29922; border-radius: 4px;
        padding: 10px 14px; margin-top: 18px;
        font-size: 12px; color: #ddd; line-height: 1.6;
    }
    .torn-takeaway .tag { color: #d29922; font-weight: bold;
                           letter-spacing: 3px; font-size: 10px; margin-right: 6px; }
    .torn-takeaway .em { color: #d29922; font-weight: bold; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

    # Helper: position (centre 50%) + offset in px for a Δpp value
    def _x_for(pp):
        # returns CSS calc string so px values stay crisp
        return f"calc(50% + {pp * _px_per_pp:.2f}px)"

    # Decide where to put the benchmark annotation (left vs right of line)
    _bench_x = _bench_pp * _px_per_pp
    _bench_annot_align_left = (_bench_pp <= 0)

    # ---- Build the HTML ----
    # FIX: use single-line concatenated f-strings (no leading whitespace) so
    # CommonMark does NOT treat indented lines as <pre><code> code blocks
    # when st.markdown(..., unsafe_allow_html=True) parses the string.
    rows_html = []
    for r in factor_rows:
        bar_down_html = ""
        bar_up_html   = ""
        if r['lo'] < 0:
            w_lo = abs(r['lo']) * _px_per_pp
            bar_down_html = (
                f'<div class="torn-bar-down" '
                f'style="right: 50%; width: {w_lo:.2f}px;"></div>'
            )
            # Place value: outside if room, inside if bar is large
            if w_lo < (_track_w_px - 50):  # outside
                bar_down_html += (
                    f'<div class="torn-val torn-val-down" '
                    f'style="right: calc(50% + {w_lo + 4:.2f}px); '
                    f'text-align: right; width: 60px;">'
                    f'{r["lo"]:.1f}pp</div>'
                )
            else:  # inside
                bar_down_html += (
                    f'<div class="torn-val torn-val-down-inside" '
                    f'style="right: calc(50% + 6px); '
                    f'text-align: left; width: 60px;">'
                    f'{r["lo"]:.1f}pp</div>'
                )
        if r['hi'] > 0:
            w_hi = r['hi'] * _px_per_pp
            bar_up_html = (
                f'<div class="torn-bar-up" '
                f'style="left: 50%; width: {w_hi:.2f}px;"></div>'
                f'<div class="torn-val torn-val-up" '
                f'style="left: calc(50% + {w_hi + 4:.2f}px); width: 60px;">'
                f'+{r["hi"]:.1f}pp</div>'
            )

        # Range cell: low → BASE → high
        rng_html = (
            f'{r["lo_lbl"]} → '
            f'<span class="basev">{r["base_lbl"]}</span> → '
            f'{r["hi_lbl"]}'
        )

        # FIX: build the row as a single-line concatenated f-string with no
        # leading indentation on any line so CommonMark won't treat it as a
        # code block. Whitespace-only differences from the original block;
        # the rendered DOM is identical.
        rows_html.append(
            f'<div class="torn-row">'
            f'<div class="torn-name">{r["name"]}</div>'
            f'<div class="torn-track" style="width: {2 * _track_w_px}px;">'
            f'<div class="torn-axis-line" style="left: 50%;"></div>'
            f'<div class="torn-bench-line" style="left: {_x_for(_bench_pp)};"></div>'
            f'{bar_down_html}'
            f'{bar_up_html}'
            f'</div>'
            f'<div class="torn-range">{rng_html}</div>'
            f'</div>'
        )

    # Top axis ticks
    ticks = [-_x_max, -_x_max // 2, 0, _x_max // 2, _x_max]
    tick_html = []
    for t in ticks:
        sign = "+" if t > 0 else ""
        tick_html.append(
            f'<div class="torn-tick-mark" style="left: {_x_for(t)};"></div>'
            f'<div class="torn-tick-label" style="left: {_x_for(t)};">{sign}{t}pp</div>'
        )
    tick_track_html = "".join(tick_html)

    # Benchmark annotation (above the chart, near the dashed line)
    bench_annot_offset_px = _bench_pp * _px_per_pp
    bench_annot_align = "left" if _bench_annot_align_left else "right"
    if _bench_annot_align_left:
        bench_annot_style = f"margin-left: calc(234px + {_track_w_px}px + {bench_annot_offset_px:.2f}px + 6px);"
    else:
        bench_annot_style = f"margin-left: calc(234px + {_track_w_px}px + {bench_annot_offset_px:.2f}px - 280px); text-align: right; width: 280px;"

    # Build subtitle
    subtitle_html = (
        f'<span class="lbl">Base case</span>: Boeing yield with '
        f'<b>Launch fps (10-yr ramp) + Re-engine 787</b> = '
        f'<span class="base">{base_y:.1f}%</span> &nbsp;•&nbsp; '
        f'<span class="lbl">Benchmark</span>: Boeing yield with '
        f'<b>Do Nothing (Milk 737) + Re-engine 787</b> = '
        f'<span class="bench">{bench_y:.1f}%</span> &nbsp;•&nbsp; '
        f'<span class="lbl">fps advantage</span> = '
        f'<b>{base_y - bench_y:+.2f}pp</b>'
    )

    # Decide takeaway tone
    _adv = base_y - bench_y
    _top = factor_rows[0]
    _next = factor_rows[1] if len(factor_rows) > 1 else _top
    if _adv > 2.0:
        _takeaway = (
            f'Launching fps wins by {_adv:.1f}pp at the base case. '
            f'Only <span class="em">{_top["name"]}</span> and '
            f'<span class="em">{_next["name"]}</span> can singlehandedly '
            f'push fps below the Do Nothing benchmark — both require '
            f'materially adverse scenarios.'
        )
    elif _adv > -2.0:
        _takeaway = (
            f'fps and Do Nothing are nearly tied at the base case '
            f'({abs(_adv):.1f}pp apart). The decision pivots on '
            f'<span class="em">{_top["name"]}</span> and '
            f'<span class="em">{_next["name"]}</span> — the two factors '
            f'that move yield ±10pp single-handedly.'
        )
    else:
        _takeaway = (
            f'Do Nothing dominates fps by {abs(_adv):.1f}pp at the base '
            f'case. fps becomes preferable only if '
            f'<span class="em">{_top["name"]}</span> and '
            f'<span class="em">{_next["name"]}</span> move materially '
            f'in Boeing\'s favour.'
        )

    # Top axis title and benchmark annotation
    bench_text_html = (
        f'<div class="torn-bench-annot" style="{bench_annot_style}">'
        f'← Do Nothing (Milk 737) benchmark ≈ {bench_y:.0f}%'
        f'</div>'
    )

    # FIX: build the wrapper as a single-line concatenated f-string with NO
    # leading indentation on any line. Streamlit's st.markdown(..., unsafe_
    # allow_html=True) runs content through CommonMark BEFORE rendering HTML,
    # and CommonMark treats lines indented 4+ spaces as <pre><code> code
    # blocks — which is what produced the raw-HTML rendering bug.
    full_html = (
        f'<div class="torn-wrap">'
        f'<div class="torn-subtitle">{subtitle_html}</div>'
        f'<div class="torn-axis-title">Δ Boeing yield (percentage points vs base case)</div>'
        f'{bench_text_html}'
        f'<div class="torn-axis">'
        f'<div class="torn-axis-spacer-left"></div>'
        f'<div class="torn-axis-track" style="width: {2 * _track_w_px}px;">'
        f'{tick_track_html}'
        f'</div>'
        f'<div class="torn-axis-spacer-right"></div>'
        f'</div>'
        f'{"".join(rows_html)}'
        f'<div class="torn-foot">'
        f'<div class="torn-foot-spacer-left"></div>'
        f'<div class="torn-foot-track" style="width: {2 * _track_w_px}px;">'
        f'<div class="torn-foot-down">DOWNSIDE SCENARIOS</div>'
        f'<div class="torn-foot-base">BASE = {base_y:.1f}%</div>'
        f'<div class="torn-foot-up">UPSIDE SCENARIOS</div>'
        f'</div>'
        f'<div class="torn-foot-spacer-right"></div>'
        f'</div>'
        f'<div class="torn-takeaway">'
        f'<span class="tag">TAKEAWAY</span>{_takeaway}'
        f'</div>'
        f'</div>'
    )
    st.markdown(full_html, unsafe_allow_html=True)

    # ============================================================
    # SECTION C3 — NGSA LAUNCH SENSITIVITY (LIVE TORNADO)
    # Mirror of the Boeing fps tornado, computed from Airbus's
    # perspective. Self-contained — does not modify any existing
    # dashboard logic. Reuses the same .torn-* CSS already loaded
    # by the Boeing section above.
    #   Base case  : Airbus Launch NGSA + Hold A350 (sabs = 2),
    #                with Boeing Launch fps (10-yr) + Re-engine 787
    #   Benchmark  : Airbus Do Nothing (Milk A320) + Hold A350
    #                (sabs = 0), with Boeing Launch fps (10-yr) +
    #                Re-engine 787
    # Five factors (strain omitted because Airbus's optimal holds
    # A350 — no two-front strain fires in the base case).
    # ============================================================
    st.markdown("<div class='sum-section'>📊 NGSA LAUNCH SENSITIVITY (LIVE TORNADO)</div>",
                unsafe_allow_html=True)
    st.caption("How robust is Airbus's NGSA launch upside? Each factor is swept across "
               "a realistic real-world range, holding everything else at the current "
               "dashboard values. Updates live as you adjust the sidebar parameters.")

    # ---- Airbus-specific parameters from session_state ----
    _EV_AIRBUS    = float(ss.get('af_ev_airbus',   190.0))
    _DEBT_AIRBUS  = float(ss.get('af_debt_airbus',  10.0))
    _STRAIN_A     = float(ss.get('af_strain_a',     5.94))
    _SAB_COST_A   = float(ss.get('af_sab_cost',     1.0))
    _NAKED_FINE_A = float(ss.get('af_naked_fine',  48.32))

    # ---- Airbus status-quo baseline (60% NB at A320, 70/170 WB at A350) ----
    def _airbus_baseline_npv(price_a320, m_a320, price_wb, m_a350):
        a_nb = a_wb = 0.0
        _a_nb_end = _A_NB_EIS_T + _NPV_POST_EIS_YRS - 1
        _a_wb_end = _A_WB_EIS_T + _NPV_POST_EIS_YRS - 1
        _T_base = max(_TIMELINE_YRS, _a_nb_end + 1, _a_wb_end + 1)
        for t in range(_T_base):
            df = 1.0 / ((1.0 + _WACC_A) ** t)
            if t <= _a_nb_end:
                a_nb += _NB_PER_YR * 0.60 * price_a320 * m_a320 * df
            if t <= _a_wb_end:
                a_wb += _WB_PER_YR * (70.0 / 170.0) * price_wb * m_a350 * df
        return a_nb, a_wb

    # ---- Airbus yield calculator (mirrors evaluate_scenario for Airbus) ----
    def _airbus_yield(p):
        b_l, a_l   = p['b_launches'], p['a_launches']
        b_r, a_r   = p['b_reengines'], p['a_reengines']
        sabs       = p['active_sabs']

        a_inv_nb = p['cx_ngsa']     if a_l else 0.0
        a_inv_wb = p['cx_a350re']   if a_r else 0.0
        # Option B: lump at EIS year
        a_pv_nb  = a_inv_nb / ((1.0 + _WACC_A) ** _A_NB_EIS_T)
        a_pv_wb  = a_inv_wb / ((1.0 + _WACC_A) ** _A_WB_EIS_T)

        # Sabotage operational cost — tied to fps's CAPEX window
        a_sab_nom = p['sab_cost'] * sabs
        a_pv_sab  = _pv_stream(a_sab_nom,
                               max(0, _B_NB_EIS_T - 9), _B_NB_EIS_T - 1, _WACC_A)

        # Naked Espionage Fine (Airbus sabotages while Boeing milks) — PV-discount
        # to fps EIS (year fine is realistically levied). Slides with fps EIS.
        if (sabs > 0 and not b_l):
            _fine_t = _B_NB_EIS_T
            a_naked = p['naked_fine'] / ((1.0 + _WACC_A) ** _fine_t)
        else:
            a_naked = 0.0

        # NB / WB share rules computed per-year (no legacy precomputation needed)

        nb_milker_active = (b_l != a_l)
        wb_milker_active = (b_r != a_r)

        # Per-program end-t offsets for Airbus's segments (Phase A)
        _a_nb_end = _A_NB_EIS_T + _NPV_POST_EIS_YRS - 1
        _a_wb_end = _A_WB_EIS_T + _NPV_POST_EIS_YRS - 1
        _T_dyn = max(_TIMELINE_YRS, _a_nb_end + 1, _a_wb_end + 1)

        a_nb_pv = a_wb_pv = 0.0
        for t in range(_T_dyn):
            df = 1.0 / ((1.0 + _WACC_A) ** t)
            # NB share — UNIFIED rule v2 (see _compute_nb_share_unified at top)
            b_sh_nb, a_sh_nb_local = _compute_nb_share_unified(
                t, b_l, a_l, _B_NB_EIS_T, _A_NB_EIS_T, is_7yr=p.get('is_7yr', False))
            b_sh_nb, a_sh_nb_local = _apply_nb_modifiers(
                b_sh_nb, a_sh_nb_local, t, _B_NB_EIS_T, _A_NB_EIS_T, b_l, a_l,
                b_inc_rate=p.get('inc_rate', False),
                is_7yr=p.get('is_7yr', False),
                fps_7yr_pp=p.get('fps_7yr_adv', 7.0),
                active_sabs=sabs, sab_share_pp=p['sab_share'])
            sh = a_sh_nb_local

            # Airbus price / margin per program timing
            if a_l and t >= _A_NB_EIS_T:
                pp, mm = p['price_ngsa'], p['m_ngsa']
            else:
                pp, mm = p['price_a320'], p['m_a320']
            if t <= _a_nb_end:
                a_nb_pv += _NB_PER_YR * sh * pp * mm * df

            # WB share (Airbus side) — UNIFIED rule (mirrors evaluate_scenario):
            # No pre-EIS anticipation; per-case catch-up from EIS.
            if b_r and not a_r:
                # XOR Case E: Boeing alone re-engines (Airbus's share = 1 - Boeing)
                if t < _B_WB_EIS_T:
                    sh_w = 70.0 / 170.0
                else:
                    years_in = t - _B_WB_EIS_T + 1
                    b_sh = min(1.0 - p['wb_milker'], 100/170 + _wb_gain_b() * years_in)
                    sh_w = 1.0 - b_sh
            elif a_r and not b_r:
                # XOR Case F: Airbus alone re-engines
                if t < _A_WB_EIS_T:
                    sh_w = 70.0 / 170.0
                else:
                    years_in = t - _A_WB_EIS_T + 1
                    sh_w = min(0.60, 70/170 + _wb_gain_a() * years_in)
            elif b_r and a_r and _B_WB_EIS_T != _A_WB_EIS_T:
                if _B_WB_EIS_T < _A_WB_EIS_T:
                    if t < _B_WB_EIS_T:
                        sh_w = 70.0 / 170.0
                    else:
                        catch_t = min(t, _A_WB_EIS_T - 1)
                        years_in = catch_t - _B_WB_EIS_T + 1
                        b_sh = min(0.80, 100/170 + _wb_gain_b() * years_in)
                        sh_w = 1.0 - b_sh
                else:
                    if t < _A_WB_EIS_T:
                        sh_w = 70.0 / 170.0
                    else:
                        catch_t = min(t, _B_WB_EIS_T - 1)
                        years_in = catch_t - _A_WB_EIS_T + 1
                        sh_w = min(0.60, 70/170 + _wb_gain_a() * years_in)
            else:
                sh_w = 70.0 / 170.0
            if t <= _a_wb_end:
                # Conditional A350 margin: status quo until re-engine EIS, then
                # branch on whether 787 also re-engines.
                if a_r and t >= _A_WB_EIS_T:
                    m_a350_t = p['m_a350_both'] if b_r else p['m_a350_alone']
                else:
                    m_a350_t = p['m_a350']
                a_wb_pv += _WB_PER_YR * sh_w * p['price_wb'] * m_a350_t * df

        a_strain_nom = p['strain_a'] if (a_l and a_r) else 0.0
        a_nom    = a_inv_nb + a_inv_wb + a_sab_nom
        a_pv     = a_pv_nb + a_pv_wb + a_pv_sab
        a_strain = (a_strain_nom * (a_pv / a_nom) if a_nom > 0 else a_strain_nom)
        a_tc     = _true_cost(a_nom, a_pv, p['debt_airbus'],
                              _EV_AIRBUS, p['alpha'])

        a_base_nb, a_base_wb = _airbus_baseline_npv(p['price_a320'], p['m_a320'],
                                                     p['price_wb'], p['m_a350'])
        delta = (a_nb_pv - a_base_nb) + (a_wb_pv - a_base_wb) \
                - a_tc - a_strain - a_pv_sab - a_naked
        return 100.0 + (delta / _EV_AIRBUS) * 100.0

    # ---- Pack live parameters for Airbus calc ----
    def _make_a_params(**overrides):
        p = dict(
            price_737=_PRICE_737, price_a320=_PRICE_A320,
            price_fps=_PRICE_fps, price_ngsa=_PRICE_NGSA, price_wb=_PRICE_WB,
            m_737=_M_737, m_a320=_M_A320, m_fps=_M_FPS, m_ngsa=_M_NGSA,
            m_787=_M_787, m_a350=_M_A350,
            m_787_alone=_M_787_ALONE, m_787_both=_M_787_BOTH,
            m_a350_alone=_M_A350_ALONE, m_a350_both=_M_A350_BOTH,
            cx_fps_10yr=_CX_FPS_10YR, cx_ngsa=_CX_NGSA,
            cx_787re=_CX_787RE, cx_a350re=_CX_A350RE,
            debt_boeing=_DEBT_BOEING, debt_airbus=_DEBT_AIRBUS,
            strain_b=_STRAIN_B, strain_a=_STRAIN_A,
            nb_milker=_NB_MILKER, wb_milker=_WB_MILKER,
            sab_share=_SAB_SHARE, sab_cost=_SAB_COST_A,
            naked_fine=_NAKED_FINE_A, alpha=_ALPHA,
            boeing_share_pct=_B_SHARE_PCT,
            fps_7yr_adv=_FPS_7YR_ADV,
            inc_rate=False, is_7yr=False,
            b_launches=True, a_launches=True,
            b_reengines=True, a_reengines=False, active_sabs=2,
        )
        p.update(overrides)
        return p

    # Airbus base case & benchmark
    a_base_params = _make_a_params(
        b_launches=True, a_launches=True,
        b_reengines=True, a_reengines=False, active_sabs=2,
    )
    a_base_y = _airbus_yield(a_base_params)

    a_bench_params = _make_a_params(
        b_launches=True, a_launches=False,
        b_reengines=True, a_reengines=False, active_sabs=0,
    )
    a_bench_y = _airbus_yield(a_bench_params)

    # ---- Airbus tornado factor sweep ----
    a_factors_def = [
        dict(name="Airbus debt level",
             param="debt_airbus",
             low=30.0, high=5.0,
             lo_lbl="$30B", hi_lbl="$5B",
             base_lbl=f"${_DEBT_AIRBUS:.0f}B"),
        dict(name="NGSA program CAPEX",
             param="cx_ngsa",
             low=30.0, high=10.0,
             lo_lbl="$30B", hi_lbl="$10B",
             base_lbl=f"${_CX_NGSA:.1f}B"),
        dict(name="NGSA operating margin",
             param="m_ngsa",
             low=0.20, high=0.32,
             lo_lbl="20%", hi_lbl="32%",
             base_lbl=f"{_M_NGSA*100:.2f}%"),
        # NGSA NB share is the inverse of boeing_share_pct: when boeing_share_pct=70
        # NGSA gets 30% (bad for Airbus); when boeing_share_pct=30 NGSA gets 70%.
        dict(name="NGSA NB share post-launch",
             param="boeing_share_pct",
             low=70.0, high=30.0,
             lo_lbl="30%", hi_lbl="70%",
             base_lbl=f"{100 - _B_SHARE_PCT:.0f}%"),
        dict(name="Delay-tactic effectiveness",
             param="sab_share",
             low=0.0, high=10.0,
             lo_lbl="0%", hi_lbl="10%",
             base_lbl=f"{_SAB_SHARE:.0f}%"),
    ]

    a_factor_rows = []
    for f in a_factors_def:
        y_lo = _airbus_yield(_make_a_params(**{f['param']: f['low']},
                                            b_launches=True, a_launches=True,
                                            b_reengines=True, a_reengines=False,
                                            active_sabs=2))
        y_hi = _airbus_yield(_make_a_params(**{f['param']: f['high']},
                                            b_launches=True, a_launches=True,
                                            b_reengines=True, a_reengines=False,
                                            active_sabs=2))
        a_factor_rows.append(dict(
            name=f['name'],
            lo=round(y_lo - a_base_y, 2), hi=round(y_hi - a_base_y, 2),
            lo_lbl=f['lo_lbl'], hi_lbl=f['hi_lbl'], base_lbl=f['base_lbl'],
        ))

    # Sort by total impact (largest range at top)
    a_factor_rows.sort(key=lambda r: abs(r['hi'] - r['lo']), reverse=True)

    # Persist for the Dashboard tab to consume
    st.session_state['_af_a_tornado_rows'] = a_factor_rows
    st.session_state['_af_a_base_y']  = float(a_base_y)
    st.session_state['_af_a_bench_y'] = float(a_bench_y)

    # X-axis range (symmetric, big enough to cover both bars and benchmark)
    _a_max_abs  = max(max(abs(r['lo']), abs(r['hi'])) for r in a_factor_rows)
    _a_bench_pp = a_bench_y - a_base_y
    _a_x_max    = max(5 * round((max(_a_max_abs, abs(_a_bench_pp)) + 4) / 5), 5)
    _a_track_w_px = 460
    _a_px_per_pp  = _a_track_w_px / _a_x_max

    def _a_x_for(pp):
        return f"calc(50% + {pp * _a_px_per_pp:.2f}px)"

    _a_bench_annot_align_left = (_a_bench_pp <= 0)

    # Build rows HTML (reuses .torn-* CSS already injected by Boeing section)
    a_rows_html = []
    for r in a_factor_rows:
        bar_down_html = ""
        bar_up_html   = ""
        if r['lo'] < 0:
            w_lo = abs(r['lo']) * _a_px_per_pp
            bar_down_html = (
                f'<div class="torn-bar-down" '
                f'style="right: 50%; width: {w_lo:.2f}px;"></div>'
            )
            if w_lo < (_a_track_w_px - 50):
                bar_down_html += (
                    f'<div class="torn-val torn-val-down" '
                    f'style="right: calc(50% + {w_lo + 4:.2f}px); '
                    f'text-align: right; width: 60px;">'
                    f'{r["lo"]:.1f}pp</div>'
                )
            else:
                bar_down_html += (
                    f'<div class="torn-val torn-val-down-inside" '
                    f'style="right: calc(50% + 6px); '
                    f'text-align: left; width: 60px;">'
                    f'{r["lo"]:.1f}pp</div>'
                )
        if r['hi'] > 0:
            w_hi = r['hi'] * _a_px_per_pp
            bar_up_html = (
                f'<div class="torn-bar-up" '
                f'style="left: 50%; width: {w_hi:.2f}px;"></div>'
                f'<div class="torn-val torn-val-up" '
                f'style="left: calc(50% + {w_hi + 4:.2f}px); width: 60px;">'
                f'+{r["hi"]:.1f}pp</div>'
            )
        rng_html = (
            f'{r["lo_lbl"]} → '
            f'<span class="basev">{r["base_lbl"]}</span> → '
            f'{r["hi_lbl"]}'
        )
        a_rows_html.append(
            f'<div class="torn-row">'
            f'<div class="torn-name">{r["name"]}</div>'
            f'<div class="torn-track" style="width: {2 * _a_track_w_px}px;">'
            f'<div class="torn-axis-line" style="left: 50%;"></div>'
            f'<div class="torn-bench-line" style="left: {_a_x_for(_a_bench_pp)};"></div>'
            f'{bar_down_html}'
            f'{bar_up_html}'
            f'</div>'
            f'<div class="torn-range">{rng_html}</div>'
            f'</div>'
        )

    # Top axis ticks
    a_ticks = [-_a_x_max, -_a_x_max // 2, 0, _a_x_max // 2, _a_x_max]
    a_tick_html = []
    for t in a_ticks:
        sign = "+" if t > 0 else ""
        a_tick_html.append(
            f'<div class="torn-tick-mark" style="left: {_a_x_for(t)};"></div>'
            f'<div class="torn-tick-label" style="left: {_a_x_for(t)};">{sign}{t}pp</div>'
        )
    a_tick_track_html = "".join(a_tick_html)

    # Benchmark annotation placement
    a_bench_annot_offset_px = _a_bench_pp * _a_px_per_pp
    if _a_bench_annot_align_left:
        a_bench_annot_style = f"margin-left: calc(234px + {_a_track_w_px}px + {a_bench_annot_offset_px:.2f}px + 6px);"
    else:
        a_bench_annot_style = f"margin-left: calc(234px + {_a_track_w_px}px + {a_bench_annot_offset_px:.2f}px - 280px); text-align: right; width: 280px;"

    a_subtitle_html = (
        f'<span class="lbl">Base case</span>: Airbus yield with '
        f'<b>Launch NGSA + Hold A350</b> = '
        f'<span class="base">{a_base_y:.1f}%</span> &nbsp;•&nbsp; '
        f'<span class="lbl">Benchmark</span>: Airbus yield with '
        f'<b>Do Nothing (Milk A320) + Hold A350</b> = '
        f'<span class="bench">{a_bench_y:.1f}%</span> &nbsp;•&nbsp; '
        f'<span class="lbl">NGSA advantage</span> = '
        f'<b>{a_base_y - a_bench_y:+.2f}pp</b>'
    )

    # Takeaway tone (mirrors Boeing version)
    _a_adv = a_base_y - a_bench_y
    _a_top  = a_factor_rows[0]
    _a_next = a_factor_rows[1] if len(a_factor_rows) > 1 else _a_top
    if _a_adv > 2.0:
        _a_takeaway = (
            f'Launching NGSA wins by {_a_adv:.1f}pp at the base case. '
            f'Only <span class="em">{_a_top["name"]}</span> and '
            f'<span class="em">{_a_next["name"]}</span> can singlehandedly '
            f'push NGSA below the Do Nothing benchmark — both require '
            f'materially adverse scenarios.'
        )
    elif _a_adv > -2.0:
        _a_takeaway = (
            f'NGSA and Do Nothing are nearly tied at the base case '
            f'({abs(_a_adv):.1f}pp apart). The decision pivots on '
            f'<span class="em">{_a_top["name"]}</span> and '
            f'<span class="em">{_a_next["name"]}</span> — the two factors '
            f'that move yield ±10pp single-handedly.'
        )
    else:
        _a_takeaway = (
            f'Do Nothing dominates NGSA by {abs(_a_adv):.1f}pp at the base '
            f'case. NGSA becomes preferable only if '
            f'<span class="em">{_a_top["name"]}</span> and '
            f'<span class="em">{_a_next["name"]}</span> move materially '
            f'in Airbus\'s favour.'
        )

    a_bench_text_html = (
        f'<div class="torn-bench-annot" style="{a_bench_annot_style}">'
        f'← Do Nothing (Milk A320) benchmark ≈ {a_bench_y:.0f}%'
        f'</div>'
    )

    a_full_html = (
        f'<div class="torn-wrap">'
        f'<div class="torn-subtitle">{a_subtitle_html}</div>'
        f'<div class="torn-axis-title">Δ Airbus yield (percentage points vs base case)</div>'
        f'{a_bench_text_html}'
        f'<div class="torn-axis">'
        f'<div class="torn-axis-spacer-left"></div>'
        f'<div class="torn-axis-track" style="width: {2 * _a_track_w_px}px;">'
        f'{a_tick_track_html}'
        f'</div>'
        f'<div class="torn-axis-spacer-right"></div>'
        f'</div>'
        f'{"".join(a_rows_html)}'
        f'<div class="torn-foot">'
        f'<div class="torn-foot-spacer-left"></div>'
        f'<div class="torn-foot-track" style="width: {2 * _a_track_w_px}px;">'
        f'<div class="torn-foot-down">DOWNSIDE SCENARIOS</div>'
        f'<div class="torn-foot-base">BASE = {a_base_y:.1f}%</div>'
        f'<div class="torn-foot-up">UPSIDE SCENARIOS</div>'
        f'</div>'
        f'<div class="torn-foot-spacer-right"></div>'
        f'</div>'
        f'<div class="torn-takeaway">'
        f'<span class="tag">TAKEAWAY</span>{_a_takeaway}'
        f'</div>'
        f'</div>'
    )
    st.markdown(a_full_html, unsafe_allow_html=True)

    # ============================================================
    # SECTION C4 — ENGINE-PLAYER LAUNCH SENSITIVITY (LIVE TORNADOS)
    # Three live tornados — one per engine player — mirroring the
    # idea used for Boeing fps and Airbus NGSA above:
    #   • Base case   : that player chooses an "active launch" posture
    #   • Benchmark   : that player chooses a "do nothing" posture
    #   • Other two   : held fixed at their plausible best-response
    # The tornado answers: "given the rest of the engine board, how
    # robust is this player's launch upside?"
    #
    # Each chart sweeps 5 realistic factors. Math is a self-contained
    # copy of run_engine_board()'s simulate() — does not touch any
    # existing dashboard state. Reuses the .torn-* CSS already loaded
    # by the Boeing section above.
    # ============================================================

    # ---- Engine constants (identical to run_engine_board()) ----
    _EN_NB_THRUST = 30000
    _EN_WB_THRUST = 80000
    _EN_CPI       = 0.022
    _EN_ENGINES_PER_AC = 2
    _EN_NB_AC_PER_YR   = 2000
    _EN_WB_AC_PER_YR   = 170
    # NB engine price from the same historical-thrust regression run_engine_board uses
    _EN_thrust_data    = np.array([8729, 9220, 12670, 13360, 13630, 18900, 23000, 14200, 20000, 25000], dtype=float)
    _EN_shipset_price  = np.array([4.7,  4.7,  5.0,   5.5,   5.5,   6.0,   7.1,   5.2,   7.0,   5.9],  dtype=float)
    _EN_engine_price_data = _EN_shipset_price / 2.0
    _EN_reg_slope, _EN_reg_intercept = np.polyfit(_EN_thrust_data, _EN_engine_price_data, 1)
    _EN_NB_PRICE_M = float(_EN_reg_slope * _EN_NB_THRUST + _EN_reg_intercept)
    _EN_WB_PRICE_M = float(_EN_WB_THRUST * 140 / 1_000_000)

    # ---- Read every engine parameter the calculation needs ----
    _EN_EV_A   = float(ss.get('en_ev_a',   160.0))
    _EN_DEBT_A = float(ss.get('en_debt_a',  35.0))
    _EN_WACC_A = float(ss.get('en_wacc_a',   8.5)) / 100.0
    _EN_EV_B   = float(ss.get('en_ev_b',   110.0))
    _EN_DEBT_B = float(ss.get('en_debt_b',  40.0))
    _EN_WACC_B = float(ss.get('en_wacc_b',  10.0)) / 100.0
    _EN_EV_C   = float(ss.get('en_ev_c',   110.0))
    _EN_DEBT_C = float(ss.get('en_debt_c',  40.0))
    _EN_WACC_C = float(ss.get('en_wacc_c',  10.0)) / 100.0
    _EN_RD_CFM_OF  = float(ss.get('en_rd_cfm_open_fan', 8.0))
    _EN_RD_CFM_DUC = float(ss.get('en_rd_cfm_ducted',   4.0))
    _EN_RD_PW_SOLO = float(ss.get('en_rd_pw_solo',      2.0))
    _EN_RD_PW_JV   = float(ss.get('en_rd_pw_jv',        2.0))
    _EN_RD_RR_NB    = float(ss.get('en_rd_rr_nb',    8.0))
    _EN_RD_RR_WB    = float(ss.get('en_rd_rr_wb',    4.0))
    _EN_RD_RR_T1000 = float(ss.get('en_rd_rr_t1000', 2.0))
    _EN_OPEN_FAN_LOSS = float(ss.get('en_openfan_loss', 35)) / 100.0
    _EN_DUCTED_GAIN   = float(ss.get('en_ducted_gain',  10)) / 100.0
    _EN_LOBBY_COST    = float(ss.get('en_lobby_cost',    1.0))
    _EN_STRAIN        = float(ss.get('en_strain_cost',   2.0))
    _EN_RR_NBWB_STRAIN = float(ss.get('en_rr_nbwb_strain', 5.0))
    _EN_GROSS_MULT    = float(ss.get('en_gross_mult',    1.6))
    # Engine NPV timeline synced to airframer (2026-2056, T=31).
    # Both NB and WB EIS read from airframer per-program sliders; we use
    # min() so the engine board's share switch syncs with the earlier
    # platform launch in each segment.
    _EN_TIMELINE_YRS  = 31
    _EN_NPV_POST_EIS_YRS = 20   # Phase A per-program window
    _en_fps_yr        = int(ss.get('af_fps_eis',  2037))
    _en_ngsa_yr       = int(ss.get('af_ngsa_eis', 2037))
    _EN_NB_EIS_T      = max(0, min(_en_fps_yr, _en_ngsa_yr) - 2026)
    _en_787_yr        = int(ss.get('af_787_eis',  2041))
    _en_a350_yr       = int(ss.get('af_a350_eis', 2035))
    _EN_WB_EIS_T      = max(0, min(_en_787_yr, _en_a350_yr) - 2026)
    _EN_FUT_CFM_NB    = float(ss.get('f_cfm_nb', 53))
    _EN_FUT_PW_NB     = float(ss.get('f_pw_nb',  50))
    _EN_FUT_RR_NB     = float(ss.get('f_rr_nb',  50))
    _EN_FUT_CFM_WB    = float(ss.get('f_cfm_wb', 42))
    _EN_FUT_RR_WB     = float(ss.get('f_rr_wb',  58))
    _EN_SQ_CFM_NB     = float(ss.get('sq_cfm_nb', 76))
    _EN_SQ_PW_NB      = float(ss.get('sq_pw_nb',  24))
    _EN_SQ_CFM_WB     = float(ss.get('sq_cfm_wb', 42))
    _EN_SQ_RR_WB      = float(ss.get('sq_rr_wb',  58))

    # PW lock state (forced by airframer supplier choice)
    _EN_PW_LOCK = ss.get("_en_pw_locked_move", "2-Launch GTF2 Go Solo")

    # ---- Helpers (self-contained copies of run_engine_board's math) ----
    def _en_norm3(a, b, c):
        t = a + b + c
        return (a/t, b/t, c/t) if t > 0 else (0.0, 0.0, 0.0)

    def _en_calc_npv(planes_yr, pre_share, post_share, eng_price_m, wacc, eis_t, gross_mult,
                     T=_EN_TIMELINE_YRS, apply_post_eis_window=True):
        # Mirror of run_engine_board's calc_npv with pre/post-EIS share switching.
        # Phase A: per-program window — count cashflows only through eis_t + 19.
        if wacc <= 0 or eng_price_m <= 0:
            return 0.0
        if apply_post_eis_window:
            end_t = eis_t + _EN_NPV_POST_EIS_YRS - 1
            T_dyn = max(T, end_t + 1)
        else:
            end_t = T - 1
            T_dyn = T
        total = 0.0
        for t in range(T_dyn):
            if t > end_t:
                continue
            share = pre_share if t < eis_t else post_share
            if share <= 0:
                continue
            npv_per = (eng_price_m * gross_mult) * ((1.0 + _EN_CPI) ** t)
            cf_t    = planes_yr * _EN_ENGINES_PER_AC * share * npv_per
            pv_t    = cf_t / ((1.0 + wacc) ** t)
            total  += pv_t
        return total / 1000.0  # $M → $B

    def _en_npv_player(pre_nb, post_nb, pre_wb, post_wb, wacc, gross_mult, T=_EN_TIMELINE_YRS):
        return (_en_calc_npv(_EN_NB_AC_PER_YR, pre_nb, post_nb, _EN_NB_PRICE_M, wacc, _EN_NB_EIS_T, gross_mult, T)
              + _en_calc_npv(_EN_WB_AC_PER_YR, pre_wb, post_wb, _EN_WB_PRICE_M, wacc, _EN_WB_EIS_T, gross_mult, T))

    def _en_simulate(move_a, move_b, move_c, p):
        """Compact mirror of run_engine_board's simulate(). Returns dict with
        yields for all three players. `p` carries every tunable parameter so
        we can sweep them for tornado factors."""
        # Pre-2037 status-quo baselines (constant across calibrations)
        base_cfm_nb, base_pw_nb, base_rr_nb = _en_norm3(p['sq_cfm_nb'], p['sq_pw_nb'], 0.0)
        base_cfm_wb, base_pw_wb, base_rr_wb = _en_norm3(p['sq_cfm_wb'], 0.0, p['sq_rr_wb'])

        # Post-2037 organic starting shares (subject to game moves below)
        start_cfm_nb, start_pw_nb, start_rr_nb = _en_norm3(p['fut_cfm_nb'], p['fut_pw_nb'], p['fut_rr_nb'])
        start_cfm_wb, start_pw_wb, start_rr_wb = _en_norm3(p['fut_cfm_wb'], 0.0, p['fut_rr_wb'])

        a_nb, a_wb = start_cfm_nb, start_cfm_wb
        b_nb, b_wb = start_pw_nb,  start_pw_wb
        c_nb, c_wb = start_rr_nb,  start_rr_wb

        inv_a = inv_b = inv_c = 0.0   # All R&D conditional
        str_a = str_b = str_c = 0.0
        jv_nb_active = False

        # Player A (CFM)
        pa = 0
        # Detect Open Fan / Ducted / Lobby (mirrors run_engine_board simulator)
        _has_open_fan = ("1-Open Fan" in move_a) or ("3-Open + Ducted" in move_a)
        _has_ducted   = ("2-Ducted"   in move_a) or ("3-Open + Ducted" in move_a)
        _has_lobby    = "5-Lobby Govts" in move_a
        _rr_nb_active = "Ultrafan NB" in move_c or "JV with PW" in move_c

        if _has_open_fan:
            pa += 1; inv_a += p['rd_cfm_open_fan']
            _of_loss = min(p['open_fan_loss'], 0.20) if _has_lobby else p['open_fan_loss']
            a_nb -= _of_loss
            if _rr_nb_active:
                b_nb += _of_loss / 2; c_nb += _of_loss / 2
            else:
                b_nb += _of_loss
        if _has_ducted:
            pa += 1; inv_a += p['rd_cfm_ducted']
            a_nb += p['ducted_gain']
            if _rr_nb_active:
                b_nb -= p['ducted_gain']/2; c_nb -= p['ducted_gain']/2
            else:
                b_nb -= p['ducted_gain']
        if "3-Open + Ducted" in move_a:
            pa += 1
        if "4-Partner Embraer" in move_a:
            pa += 1; a_nb += 0.05
        if _has_lobby:
            pa += 1; inv_a += p['lobby_cost']  # $2B default — Open Fan defensive
            # No standalone share effect
        if "6-Upgrade GenX9" in move_a:
            pa += 1; a_wb += 0.05
        if "7-Invest GenX" in move_a:
            pa += 1; a_wb += 0.05
        if pa >= 2: str_a += p['strain']

        # Player B (PW)
        pb = 0
        if "2-Launch GTF2" in move_b:
            pb += 1; inv_b += p['rd_pw_solo']
            b_nb += 0.10; a_nb -= 0.05; c_nb -= 0.05
        if "3-JV with RR" in move_b:
            pb += 1; jv_nb_active = True; inv_b += p['rd_pw_jv']
            a_nb -= 0.10; b_nb += 0.05; c_nb += 0.05
        if pb >= 2: str_b += p['strain']

        # Player C (RR)
        pc = 0; rr_nb = False; rr_wb = False
        if "1-Ultrafan WB" in move_c:
            pc += 1; rr_wb = True; inv_c += p['rd_rr_wb']
            c_wb += 0.10; a_wb -= 0.10
        if "2-Ultrafan NB" in move_c:
            pc += 1; rr_nb = True; inv_c += p['rd_rr_nb']
            c_nb += 0.15; a_nb -= 0.10; b_nb -= 0.05
        if "3-JV with PW" in move_c:
            pc += 1; rr_nb = True; jv_nb_active = True
            inv_c += p['rd_rr_nb'] / 2.0
            c_nb += 0.05; b_nb += 0.05; a_nb -= 0.10
        if "4-Upgrade T1000" in move_c:
            pc += 1; rr_wb = True; inv_c += p['rd_rr_t1000']
            c_wb += 0.05; a_wb -= 0.05
        if rr_nb and rr_wb: str_c += p['rr_nbwb_strain']

        # JV equalization, floor at 0, renormalize
        if jv_nb_active:
            avg = (b_nb + c_nb) / 2.0
            b_nb = avg; c_nb = avg
        a_nb, b_nb, c_nb = max(0, a_nb), max(0, b_nb), max(0, c_nb)
        a_wb, b_wb, c_wb = max(0, a_wb), max(0, b_wb), max(0, c_wb)
        t_nb = a_nb + b_nb + c_nb
        if t_nb > 0: a_nb /= t_nb; b_nb /= t_nb; c_nb /= t_nb
        t_wb = a_wb + b_wb + c_wb
        if t_wb > 0: a_wb /= t_wb; b_wb /= t_wb; c_wb /= t_wb

        # NPVs — use pre/post-EIS share switching (sync to airframer timeline).
        gm = p['gross_mult']
        # Base = status quo persists for all 31 years (pre = post = base shares)
        ba = _en_npv_player(base_cfm_nb, base_cfm_nb, base_cfm_wb, base_cfm_wb, p['wacc_a'], gm)
        bb = _en_npv_player(base_pw_nb,  base_pw_nb,  base_pw_wb,  base_pw_wb,  p['wacc_b'], gm)
        bc = _en_npv_player(base_rr_nb,  base_rr_nb,  base_rr_wb,  base_rr_wb,  p['wacc_c'], gm)
        # Scenario = status-quo pre-EIS, move-shifted shares post-EIS
        na  = _en_npv_player(base_cfm_nb, a_nb, base_cfm_wb, a_wb, p['wacc_a'], gm)
        nb_ = _en_npv_player(base_pw_nb,  b_nb, base_pw_wb,  b_wb, p['wacc_b'], gm)
        nc  = _en_npv_player(base_rr_nb,  c_nb, base_rr_wb,  c_wb, p['wacc_c'], gm)

        u_a = na - ba - str_a - inv_a
        u_b = nb_ - bb - str_b - inv_b
        u_c = nc - bc - str_c - inv_c

        ya = 100.0 + (u_a / max(0.1, p['ev_a'])) * 100.0
        yb = 100.0 + (u_b / max(0.1, p['ev_b'])) * 100.0
        yc = 100.0 + (u_c / max(0.1, p['ev_c'])) * 100.0
        return {'A': ya, 'B': yb, 'C': yc}

    def _en_make_params(**overrides):
        """Pack the live engine parameters into a dict for _en_simulate."""
        p = dict(
            ev_a=_EN_EV_A, ev_b=_EN_EV_B, ev_c=_EN_EV_C,
            wacc_a=_EN_WACC_A, wacc_b=_EN_WACC_B, wacc_c=_EN_WACC_C,
            rd_cfm_open_fan=_EN_RD_CFM_OF, rd_cfm_ducted=_EN_RD_CFM_DUC,
            rd_pw_solo=_EN_RD_PW_SOLO, rd_pw_jv=_EN_RD_PW_JV,
            rd_rr_nb=_EN_RD_RR_NB, rd_rr_wb=_EN_RD_RR_WB, rd_rr_t1000=_EN_RD_RR_T1000,
            open_fan_loss=_EN_OPEN_FAN_LOSS, ducted_gain=_EN_DUCTED_GAIN,
            lobby_cost=_EN_LOBBY_COST, strain=_EN_STRAIN,
            rr_nbwb_strain=_EN_RR_NBWB_STRAIN,
            gross_mult=_EN_GROSS_MULT,
            sq_cfm_nb=_EN_SQ_CFM_NB, sq_pw_nb=_EN_SQ_PW_NB,
            sq_cfm_wb=_EN_SQ_CFM_WB, sq_rr_wb=_EN_SQ_RR_WB,
            fut_cfm_nb=_EN_FUT_CFM_NB, fut_pw_nb=_EN_FUT_PW_NB, fut_rr_nb=_EN_FUT_RR_NB,
            fut_cfm_wb=_EN_FUT_CFM_WB, fut_rr_wb=_EN_FUT_RR_WB,
        )
        p.update(overrides)
        return p

    # ---- Shared tornado renderer ----
    # Reuses .torn-* CSS already injected by the Boeing section above.
    def _en_render_tornado(container_id, title, caption,
                            base_y, bench_y, factor_rows,
                            base_label, bench_label, product_label,
                            advantage_word):
        """Render a single engine tornado. Mirrors the layout of the Boeing
        and Airbus tornados above. `factor_rows` is a list of dicts with
        keys: name, lo, hi, lo_lbl, hi_lbl, base_lbl."""
        # Sort by total impact, top = biggest mover
        factor_rows.sort(key=lambda r: abs(r['hi'] - r['lo']), reverse=True)

        max_abs = max(max(abs(r['lo']), abs(r['hi'])) for r in factor_rows)
        bench_pp = bench_y - base_y
        x_max    = max(5 * round((max(max_abs, abs(bench_pp)) + 4) / 5), 5)
        track_w_px = 460
        px_per_pp  = track_w_px / x_max

        def x_for(pp):
            return f"calc(50% + {pp * px_per_pp:.2f}px)"

        bench_annot_align_left = (bench_pp <= 0)

        rows_html = []
        for r in factor_rows:
            bar_down_html = ""
            bar_up_html   = ""
            if r['lo'] < 0:
                w_lo = abs(r['lo']) * px_per_pp
                bar_down_html = (
                    f'<div class="torn-bar-down" '
                    f'style="right: 50%; width: {w_lo:.2f}px;"></div>'
                )
                if w_lo < (track_w_px - 50):
                    bar_down_html += (
                        f'<div class="torn-val torn-val-down" '
                        f'style="right: calc(50% + {w_lo + 4:.2f}px); '
                        f'text-align: right; width: 60px;">'
                        f'{r["lo"]:.1f}pp</div>'
                    )
                else:
                    bar_down_html += (
                        f'<div class="torn-val torn-val-down-inside" '
                        f'style="right: calc(50% + 6px); '
                        f'text-align: left; width: 60px;">'
                        f'{r["lo"]:.1f}pp</div>'
                    )
            if r['hi'] > 0:
                w_hi = r['hi'] * px_per_pp
                bar_up_html = (
                    f'<div class="torn-bar-up" '
                    f'style="left: 50%; width: {w_hi:.2f}px;"></div>'
                    f'<div class="torn-val torn-val-up" '
                    f'style="left: calc(50% + {w_hi + 4:.2f}px); width: 60px;">'
                    f'+{r["hi"]:.1f}pp</div>'
                )
            rng_html = (
                f'{r["lo_lbl"]} → '
                f'<span class="basev">{r["base_lbl"]}</span> → '
                f'{r["hi_lbl"]}'
            )
            rows_html.append(
                f'<div class="torn-row">'
                f'<div class="torn-name">{r["name"]}</div>'
                f'<div class="torn-track" style="width: {2 * track_w_px}px;">'
                f'<div class="torn-axis-line" style="left: 50%;"></div>'
                f'<div class="torn-bench-line" style="left: {x_for(bench_pp)};"></div>'
                f'{bar_down_html}'
                f'{bar_up_html}'
                f'</div>'
                f'<div class="torn-range">{rng_html}</div>'
                f'</div>'
            )

        ticks = [-x_max, -x_max // 2, 0, x_max // 2, x_max]
        tick_html = []
        for t in ticks:
            sign = "+" if t > 0 else ""
            tick_html.append(
                f'<div class="torn-tick-mark" style="left: {x_for(t)};"></div>'
                f'<div class="torn-tick-label" style="left: {x_for(t)};">{sign}{t}pp</div>'
            )
        tick_track_html = "".join(tick_html)

        bench_annot_offset_px = bench_pp * px_per_pp
        if bench_annot_align_left:
            bench_annot_style = f"margin-left: calc(234px + {track_w_px}px + {bench_annot_offset_px:.2f}px + 6px);"
        else:
            bench_annot_style = f"margin-left: calc(234px + {track_w_px}px + {bench_annot_offset_px:.2f}px - 280px); text-align: right; width: 280px;"

        subtitle_html = (
            f'<span class="lbl">Base case</span>: '
            f'<b>{base_label}</b> = '
            f'<span class="base">{base_y:.1f}%</span> &nbsp;•&nbsp; '
            f'<span class="lbl">Benchmark</span>: '
            f'<b>{bench_label}</b> = '
            f'<span class="bench">{bench_y:.1f}%</span> &nbsp;•&nbsp; '
            f'<span class="lbl">{advantage_word}</span> = '
            f'<b>{base_y - bench_y:+.2f}pp</b>'
        )

        adv = base_y - bench_y
        top  = factor_rows[0]
        nxt = factor_rows[1] if len(factor_rows) > 1 else top
        if adv > 2.0:
            takeaway = (
                f'Launching {product_label} wins by {adv:.1f}pp at the base case. '
                f'Only <span class="em">{top["name"]}</span> and '
                f'<span class="em">{nxt["name"]}</span> can singlehandedly '
                f'push {product_label} below the Do Nothing benchmark — both '
                f'require materially adverse scenarios.'
            )
        elif adv > -2.0:
            takeaway = (
                f'{product_label} and Do Nothing are nearly tied at the base case '
                f'({abs(adv):.1f}pp apart). The decision pivots on '
                f'<span class="em">{top["name"]}</span> and '
                f'<span class="em">{nxt["name"]}</span> — the two factors that '
                f'move yield ±{abs(top["hi"] - top["lo"]):.0f}pp single-handedly.'
            )
        else:
            takeaway = (
                f'Do Nothing dominates {product_label} by {abs(adv):.1f}pp at the '
                f'base case. {product_label} becomes preferable only if '
                f'<span class="em">{top["name"]}</span> and '
                f'<span class="em">{nxt["name"]}</span> move materially in the '
                f'launcher\'s favour.'
            )

        bench_text_html = (
            f'<div class="torn-bench-annot" style="{bench_annot_style}">'
            f'← Do Nothing benchmark ≈ {bench_y:.0f}%'
            f'</div>'
        )

        st.markdown(f"<div class='sum-section'>{title}</div>", unsafe_allow_html=True)
        st.caption(caption)
        full_html = (
            f'<div class="torn-wrap">'
            f'<div class="torn-subtitle">{subtitle_html}</div>'
            f'<div class="torn-axis-title">Δ yield (percentage points vs base case)</div>'
            f'{bench_text_html}'
            f'<div class="torn-axis">'
            f'<div class="torn-axis-spacer-left"></div>'
            f'<div class="torn-axis-track" style="width: {2 * track_w_px}px;">'
            f'{tick_track_html}'
            f'</div>'
            f'<div class="torn-axis-spacer-right"></div>'
            f'</div>'
            f'{"".join(rows_html)}'
            f'<div class="torn-foot">'
            f'<div class="torn-foot-spacer-left"></div>'
            f'<div class="torn-foot-track" style="width: {2 * track_w_px}px;">'
            f'<div class="torn-foot-down">DOWNSIDE SCENARIOS</div>'
            f'<div class="torn-foot-base">BASE = {base_y:.1f}%</div>'
            f'<div class="torn-foot-up">UPSIDE SCENARIOS</div>'
            f'</div>'
            f'<div class="torn-foot-spacer-right"></div>'
            f'</div>'
            f'<div class="torn-takeaway">'
            f'<span class="tag">TAKEAWAY</span>{takeaway}'
            f'</div>'
            f'</div>'
        )
        st.markdown(full_html, unsafe_allow_html=True)

    # ============================================================
    # CFM/GE TORNADO
    #   Base case   : CFM "3-Open + Ducted | 6-Upgrade GenX9"
    #                 (full NB + WB launch posture)
    #   Benchmark   : CFM "0-Milk LEAP" (do nothing on NB, no GenX9)
    #   PW (locked) : its current locked move (default GTF2 Solo)
    #   RR          : "2-Ultrafan NB Solo | 1-Ultrafan WB" (active)
    # ============================================================
    _CFM_BASE_MOVE  = "3-Open + Ducted | 6-Upgrade GenX9"
    _CFM_BENCH_MOVE = "0-Milk LEAP"
    _RR_FIXED_ACTIVE = "2-Ultrafan NB Solo | 1-Ultrafan WB"

    _cfm_base_y  = _en_simulate(_CFM_BASE_MOVE,  _EN_PW_LOCK, _RR_FIXED_ACTIVE,
                                  _en_make_params())['A']
    _cfm_bench_y = _en_simulate(_CFM_BENCH_MOVE, _EN_PW_LOCK, _RR_FIXED_ACTIVE,
                                  _en_make_params())['A']

    _cfm_factors_def = [
        dict(name="CFM NB starting share",
             param="fut_cfm_nb", low=20.0, high=80.0,
             lo_lbl="20%", hi_lbl="80%", base_lbl=f"{_EN_FUT_CFM_NB:.0f}%"),
        dict(name="CFM WB starting share",
             param="fut_cfm_wb", low=20.0, high=70.0,
             lo_lbl="20%", hi_lbl="70%", base_lbl=f"{_EN_FUT_CFM_WB:.0f}%"),
        dict(name="Ducted Fan NB share gain",
             param="ducted_gain", low=0.05, high=0.25,
             lo_lbl="5%", hi_lbl="25%", base_lbl=f"{_EN_DUCTED_GAIN*100:.0f}%"),
        dict(name="CFM Open Fan R&D (conditional)",
             param="rd_cfm_open_fan", low=6.0, high=1.0,
             lo_lbl="$6B", hi_lbl="$1B", base_lbl=f"${_EN_RD_CFM_OF:.1f}B"),
        dict(name="Two-project strain ($B)",
             param="strain", low=5.0, high=0.5,
             lo_lbl="$5B", hi_lbl="$0.5B", base_lbl=f"${_EN_STRAIN:.1f}B"),
    ]
    _cfm_factor_rows = []
    for f in _cfm_factors_def:
        y_lo = _en_simulate(_CFM_BASE_MOVE, _EN_PW_LOCK, _RR_FIXED_ACTIVE,
                              _en_make_params(**{f['param']: f['low']}))['A']
        y_hi = _en_simulate(_CFM_BASE_MOVE, _EN_PW_LOCK, _RR_FIXED_ACTIVE,
                              _en_make_params(**{f['param']: f['high']}))['A']
        _cfm_factor_rows.append(dict(
            name=f['name'],
            lo=round(y_lo - _cfm_base_y, 2),
            hi=round(y_hi - _cfm_base_y, 2),
            lo_lbl=f['lo_lbl'], hi_lbl=f['hi_lbl'], base_lbl=f['base_lbl'],
        ))

    _cfm_factor_rows.sort(key=lambda r: abs(r['hi'] - r['lo']), reverse=True) if False else None  # already sorted by build order — left as-is

    # Persist CFM tornado for Dashboard tab consumption
    st.session_state['_en_cfm_tornado_rows'] = _cfm_factor_rows
    st.session_state['_en_cfm_base_y']  = float(_cfm_base_y)
    st.session_state['_en_cfm_bench_y'] = float(_cfm_bench_y)

    _en_render_tornado(
        container_id="cfm-tornado",
        title="📊 CFM/GE LAUNCH SENSITIVITY (LIVE TORNADO)",
        caption=(
            "How robust is CFM's full-launch posture (3-Open + Ducted + Upgrade GenX9) "
            "vs going passive (0-Milk LEAP)? Other engine players held at active stances. "
            "Updates live as you adjust sidebar parameters."
        ),
        base_y=_cfm_base_y, bench_y=_cfm_bench_y,
        factor_rows=_cfm_factor_rows,
        base_label="CFM yield with Open + Ducted + Upgrade GenX9",
        bench_label="CFM yield with Milk LEAP (do nothing)",
        product_label="CFM Launch",
        advantage_word="CFM launch advantage",
    )

    # ============================================================
    # PW TORNADO
    #   Base case   : PW "2-Launch GTF2 Go Solo"
    #   Benchmark   : PW "1-Milk GTF" (do nothing)
    #   CFM         : "0-Milk LEAP" (passive — keeps tornado about PW only)
    #   RR          : "2-Ultrafan NB Solo | 1-Ultrafan WB" (active)
    # NOTE: PW's actual move is locked by the airframer matrix. This
    # tornado answers the counterfactual: "what if PW WERE free to
    # choose between Launch GTF2 vs Milk GTF, given the rest of the
    # board is fixed?"
    # ============================================================
    _PW_BASE_MOVE  = "2-Launch GTF2 Go Solo"
    _PW_BENCH_MOVE = "1-Milk GTF"
    # For PW's tornado we want CFM active so that share-dynamic factors
    # (Ducted gain) actually fire. CFM doing Open+Ducted is the realistic
    # Nash response when RR is also pushing Ultrafan NB.
    _CFM_ACTIVE_FOR_PW = "3-Open + Ducted | 6-Upgrade GenX9"
    # For the RR tornado we keep CFM milking so the chart is about RR vs.
    # an unchallenged baseline (the user's deck framing).
    _CFM_FIXED_PASSIVE = "0-Milk LEAP"

    _pw_base_y  = _en_simulate(_CFM_ACTIVE_FOR_PW, _PW_BASE_MOVE,  _RR_FIXED_ACTIVE,
                                 _en_make_params())['B']
    _pw_bench_y = _en_simulate(_CFM_ACTIVE_FOR_PW, _PW_BENCH_MOVE, _RR_FIXED_ACTIVE,
                                 _en_make_params())['B']

    _pw_factors_def = [
        dict(name="PW NB starting share",
             param="fut_pw_nb", low=20.0, high=80.0,
             lo_lbl="20%", hi_lbl="80%", base_lbl=f"{_EN_FUT_PW_NB:.0f}%"),
        dict(name="CFM NB starting share",
             param="fut_cfm_nb", low=80.0, high=20.0,
             lo_lbl="80%", hi_lbl="20%", base_lbl=f"{_EN_FUT_CFM_NB:.0f}%"),
        dict(name="RR NB starting share",
             param="fut_rr_nb", low=80.0, high=20.0,
             lo_lbl="80%", hi_lbl="20%", base_lbl=f"{_EN_FUT_RR_NB:.0f}%"),
        dict(name="PW GTF2 Solo R&D (conditional)",
             param="rd_pw_solo", low=6.0, high=0.5,
             lo_lbl="$6B", hi_lbl="$0.5B", base_lbl=f"${_EN_RD_PW_SOLO:.1f}B"),
        dict(name="CFM Ducted Fan NB share gain",
             param="ducted_gain", low=0.25, high=0.05,
             lo_lbl="25%", hi_lbl="5%", base_lbl=f"{_EN_DUCTED_GAIN*100:.0f}%"),
    ]
    _pw_factor_rows = []
    for f in _pw_factors_def:
        y_lo = _en_simulate(_CFM_ACTIVE_FOR_PW, _PW_BASE_MOVE, _RR_FIXED_ACTIVE,
                              _en_make_params(**{f['param']: f['low']}))['B']
        y_hi = _en_simulate(_CFM_ACTIVE_FOR_PW, _PW_BASE_MOVE, _RR_FIXED_ACTIVE,
                              _en_make_params(**{f['param']: f['high']}))['B']
        _pw_factor_rows.append(dict(
            name=f['name'],
            lo=round(y_lo - _pw_base_y, 2),
            hi=round(y_hi - _pw_base_y, 2),
            lo_lbl=f['lo_lbl'], hi_lbl=f['hi_lbl'], base_lbl=f['base_lbl'],
        ))

    # Persist PW tornado for Dashboard tab consumption
    st.session_state['_en_pw_tornado_rows'] = _pw_factor_rows
    st.session_state['_en_pw_base_y']  = float(_pw_base_y)
    st.session_state['_en_pw_bench_y'] = float(_pw_bench_y)

    _en_render_tornado(
        container_id="pw-tornado",
        title="📊 PW (Pratt) LAUNCH SENSITIVITY (LIVE TORNADO)",
        caption=(
            "How robust is PW's GTF2 launch upside vs milking GTF? Note PW's actual "
            "move is forced by the airframer supplier matrix; this tornado is the "
            "counterfactual analysis. Other engine players held fixed."
        ),
        base_y=_pw_base_y, bench_y=_pw_bench_y,
        factor_rows=_pw_factor_rows,
        base_label="PW yield with Launch GTF2 Go Solo",
        bench_label="PW yield with Milk GTF (do nothing)",
        product_label="GTF2",
        advantage_word="GTF2 advantage",
    )

    # ============================================================
    # RR TORNADO
    #   Base case   : RR "2-Ultrafan NB Solo | 1-Ultrafan WB"
    #                 (full NB + WB launch — fires the NB+WB strain)
    #   Benchmark   : RR "0-Do Nothing (Milk WB)" (do nothing)
    #   CFM         : "0-Milk LEAP" (passive)
    #   PW (locked) : its current locked move
    # ============================================================
    _RR_BASE_MOVE  = "2-Ultrafan NB Solo | 1-Ultrafan WB"
    _RR_BENCH_MOVE = "0-Do Nothing (Milk WB)"

    _rr_base_y  = _en_simulate(_CFM_FIXED_PASSIVE, _EN_PW_LOCK, _RR_BASE_MOVE,
                                 _en_make_params())['C']
    _rr_bench_y = _en_simulate(_CFM_FIXED_PASSIVE, _EN_PW_LOCK, _RR_BENCH_MOVE,
                                 _en_make_params())['C']

    _rr_factors_def = [
        dict(name="RR NB starting share",
             param="fut_rr_nb", low=20.0, high=80.0,
             lo_lbl="20%", hi_lbl="80%", base_lbl=f"{_EN_FUT_RR_NB:.0f}%"),
        dict(name="RR WB starting share",
             param="fut_rr_wb", low=30.0, high=80.0,
             lo_lbl="30%", hi_lbl="80%", base_lbl=f"{_EN_FUT_RR_WB:.0f}%"),
        dict(name="CFM WB starting share",
             param="fut_cfm_wb", low=70.0, high=20.0,
             lo_lbl="70%", hi_lbl="20%", base_lbl=f"{_EN_FUT_CFM_WB:.0f}%"),
        dict(name="RR Ultrafan R&D — NB (conditional)",
             param="rd_rr_nb", low=8.0, high=1.0,
             lo_lbl="$8B", hi_lbl="$1B", base_lbl=f"${_EN_RD_RR_NB:.1f}B"),
        dict(name="RR NB+WB concurrent strain",
             param="rr_nbwb_strain", low=10.0, high=1.0,
             lo_lbl="$10B", hi_lbl="$1B", base_lbl=f"${_EN_RR_NBWB_STRAIN:.1f}B"),
    ]
    _rr_factor_rows = []
    for f in _rr_factors_def:
        y_lo = _en_simulate(_CFM_FIXED_PASSIVE, _EN_PW_LOCK, _RR_BASE_MOVE,
                              _en_make_params(**{f['param']: f['low']}))['C']
        y_hi = _en_simulate(_CFM_FIXED_PASSIVE, _EN_PW_LOCK, _RR_BASE_MOVE,
                              _en_make_params(**{f['param']: f['high']}))['C']
        _rr_factor_rows.append(dict(
            name=f['name'],
            lo=round(y_lo - _rr_base_y, 2),
            hi=round(y_hi - _rr_base_y, 2),
            lo_lbl=f['lo_lbl'], hi_lbl=f['hi_lbl'], base_lbl=f['base_lbl'],
        ))

    # Persist RR tornado for Dashboard tab consumption
    st.session_state['_en_rr_tornado_rows'] = _rr_factor_rows
    st.session_state['_en_rr_base_y']  = float(_rr_base_y)
    st.session_state['_en_rr_bench_y'] = float(_rr_bench_y)

    _en_render_tornado(
        container_id="rr-tornado",
        title="📊 RR (Rolls-Royce) LAUNCH SENSITIVITY (LIVE TORNADO)",
        caption=(
            "How robust is RR's full-launch posture (Ultrafan NB Solo + Ultrafan WB) "
            "vs holding back? Note: this scenario fires the NB+WB concurrent strain. "
            "Other engine players held fixed."
        ),
        base_y=_rr_base_y, bench_y=_rr_bench_y,
        factor_rows=_rr_factor_rows,
        base_label="RR yield with Ultrafan NB Solo + Ultrafan WB",
        bench_label="RR yield with Do Nothing (Milk WB)",
        product_label="Ultrafan launch",
        advantage_word="Ultrafan advantage",
    )

    # ============================================================
    # SECTION C5 — DELIVERY PROJECTIONS (LIVE LINE CHARTS)
    # Two INDEPENDENT charts, each with its own dropdown:
    #   • Aircraft deliveries — driven by Airframer-board equilibria
    #   • Engine deliveries   — driven by Engine-board equilibria
    #
    # Aircraft chart: one line per AIRCRAFT VARIANT (737 / fps / A320 /
    # NGSA / 787 / A350). The 737↔fps and A320↔NGSA transitions reflect
    # post-2037 EIS, with the same time-segmented logic that
    # evaluate_scenario() uses inside run_airframer_board().
    #
    # Engine chart: one line per ENGINE PRODUCT × MAKER, with the engine
    # count = aircraft × 2 (two engines per aircraft). The engine
    # equilibrium's share-modifying moves are applied per the engine
    # simulate() at lines ~1580-1684 of run_engine_board(), and aircraft
    # deliveries assume the "both launch" baseline that the engine board
    # itself is computed under.
    #
    # We deliberately do NOT modify any simulator logic — this is purely
    # an additive visualisation.
    # ============================================================
    st.markdown("<div class='sum-section'>📈 DELIVERY PROJECTIONS — AIRCRAFT &amp; ENGINES (LIVE)</div>",
                unsafe_allow_html=True)
    st.caption(
        "Two charts, each independently driven by its own gameboard. "
        "Year-by-year deliveries 2026-2068. Aircraft chart uses the airframer "
        "equilibria (each Nash determines 737↔fps and A320↔NGSA transitions, "
        "plus 787/A350 re-engine effects). Engine chart uses the engine "
        "equilibria (each Nash determines CFM/PW/RR engine share splits) and "
        "multiplies aircraft deliveries by 2 (two engines per aircraft)."
    )

    # Shared per-year setup (used by both charts)
    _CHT_NB_RATE     = 2000.0   # aircraft per year, NB market
    _CHT_WB_RATE     = 170.0    # aircraft per year, WB market
    NPV_POST_EIS_YRS_AC = 20    # Phase A: per-program window for delivery counting
    _CHT_YEAR_START  = 2026
    _CHT_YEAR_END    = 2068
    _CHT_YEARS       = list(range(_CHT_YEAR_START, _CHT_YEAR_END + 1))
    _CHT_NB_EIS_YEAR = min(int(st.session_state.get('af_fps_eis',  2037)),
                           int(st.session_state.get('af_ngsa_eis', 2037)))  # legacy ref
    # Per-platform WB EIS years (read from airframer sliders so the chart's
    # share-switch year stays synced with evaluate_scenario).
    _CHT_787_EIS_YEAR  = int(st.session_state.get('af_787_eis',  2041))
    _CHT_A350_EIS_YEAR = int(st.session_state.get('af_a350_eis', 2035))

    def _compute_aircraft_per_state(a_strat, b_strat):
        """Replicate evaluate_scenario's per-year share logic to produce 6
        per-aircraft delivery lists (737, fps, A320, NGSA, 787, A350) covering
        2026-2068. Both charts use this so they stay numerically consistent.

        Returns (lst_737, lst_fps, lst_a320, lst_ngsa, lst_787, lst_a350).
        """
        v_nb_milker   = float(st.session_state.get('af_nb_milker', 30.0)) / 100.0
        v_wb_milker   = float(st.session_state.get('af_wb_milker', 15.0)) / 100.0
        v_fps_7yr_adv = float(st.session_state.get('af_fps_7yr_adv', 7.0))
        v_sab_share   = float(st.session_state.get('af_sab_share', 5.0))
        boeing_share  = float(st.session_state.get('_boeing_share_both', 50))
        # Per-program NB EIS years
        v_fps_eis_yr  = int(st.session_state.get('af_fps_eis',  2037))
        v_ngsa_eis_yr = int(st.session_state.get('af_ngsa_eis', 2037))

        b_nb_move, b_rate, b_wb_move = b_strat
        a_nb_move, a_btl, a_poach, a_wb_move = a_strat

        b_launches_nb = "Launch_fps" in b_nb_move
        a_launches_nb = "Launch_NGSA" in a_nb_move
        b_inc_rate    = "Increase_737_Rate" in b_rate
        is_7yr_fps    = (b_nb_move == "Launch_fps_7yr_Solo")
        b_reengines   = "Re_engine_787"  in b_wb_move
        a_reengines   = "Re_engine_A350" in a_wb_move
        active_sabs   = sum(1 for m in (a_btl, a_poach)
                            if "Sabotage" in m and "No" not in m)

        # Post-EIS WB share (still uses milker-share for receipt convenience)
        b_eis_wb_base, a_eis_wb_base = 100/170, 70/170
        if b_reengines and not a_reengines:
            b_eis_wb, a_eis_wb = 1.0 - v_wb_milker, v_wb_milker
        elif a_reengines and not b_reengines:
            a_eis_wb, b_eis_wb = 1.0 - v_wb_milker, v_wb_milker
        else:
            b_eis_wb, a_eis_wb = b_eis_wb_base, a_eis_wb_base

        wb_milker_active = (b_reengines   != a_reengines)

        lst_737, lst_fps   = [], []
        lst_a320, lst_ngsa = [], []
        lst_787, lst_a350  = [], []

        min_nb_eis = min(v_fps_eis_yr, v_ngsa_eis_yr)
        for yr in _CHT_YEARS:
            # NB share for the year — UNIFIED rule v2 via module helpers.
            # Helpers work in t-offset (year - 2026); convert yr ↔ t.
            t = yr - 2026
            b_eis_nb_t_h = v_fps_eis_yr  - 2026
            a_eis_nb_t_h = v_ngsa_eis_yr - 2026
            b_sh_nb, a_sh_nb = _compute_nb_share_unified(
                t, b_launches_nb, a_launches_nb, b_eis_nb_t_h, a_eis_nb_t_h,
                is_7yr=is_7yr_fps)
            b_sh_nb, a_sh_nb = _apply_nb_modifiers(
                b_sh_nb, a_sh_nb, t, b_eis_nb_t_h, a_eis_nb_t_h,
                b_launches_nb, a_launches_nb,
                b_inc_rate=b_inc_rate,
                is_7yr=is_7yr_fps, fps_7yr_pp=v_fps_7yr_adv,
                active_sabs=active_sabs, sab_share_pp=v_sab_share)

            b_nb_total = _CHT_NB_RATE * b_sh_nb
            a_nb_total = _CHT_NB_RATE * a_sh_nb

            # Aircraft variant transitions per-program: 737↔fps at fps EIS,
            # A320↔NGSA at NGSA EIS. Each player flips at their own EIS year.
            if b_launches_nb and yr >= v_fps_eis_yr:
                lst_737.append(0.0);        lst_fps.append(b_nb_total)
            else:
                lst_737.append(b_nb_total); lst_fps.append(0.0)
            if a_launches_nb and yr >= v_ngsa_eis_yr:
                lst_a320.append(0.0);       lst_ngsa.append(a_nb_total)
            else:
                lst_a320.append(a_nb_total); lst_ngsa.append(0.0)

            # Phase A per-program window mask: deliveries are zero outside
            # each program's 20-yr-post-EIS NPV window. For NB, the program
            # window is 2026 → fps_EIS+19 (Boeing's program) / NGSA_EIS+19
            # (Airbus's program). 737/fps share the Boeing NB window; A320/
            # NGSA share the Airbus NB window. Same logic applies to WB
            # below.
            _b_nb_end_yr = v_fps_eis_yr  + NPV_POST_EIS_YRS_AC - 1
            _a_nb_end_yr = v_ngsa_eis_yr + NPV_POST_EIS_YRS_AC - 1
            if yr > _b_nb_end_yr:
                lst_737[-1] = 0.0
                lst_fps[-1] = 0.0
            if yr > _a_nb_end_yr:
                lst_a320[-1] = 0.0
                lst_ngsa[-1] = 0.0

            # WB share for the year — UNIFIED rule (mirrors evaluate_scenario):
            # No pre-EIS anticipation. Status quo persists until the first
            # relevant EIS. Then per-case catch-up.
            if b_reengines and not a_reengines:
                # XOR Case E: only Boeing re-engines
                if yr < _CHT_787_EIS_YEAR:
                    b_sh_wb, a_sh_wb = b_eis_wb_base, a_eis_wb_base
                else:
                    years_in = yr - _CHT_787_EIS_YEAR + 1
                    b_sh_wb = min(1.0 - v_wb_milker, b_eis_wb_base + 0.03 * years_in)
                    a_sh_wb = 1.0 - b_sh_wb
            elif a_reengines and not b_reengines:
                # XOR Case F: only Airbus re-engines
                if yr < _CHT_A350_EIS_YEAR:
                    b_sh_wb, a_sh_wb = b_eis_wb_base, a_eis_wb_base
                else:
                    years_in = yr - _CHT_A350_EIS_YEAR + 1
                    a_sh_wb = min(0.60, a_eis_wb_base + 0.04 * years_in)
                    b_sh_wb = 1.0 - a_sh_wb
            elif b_reengines and a_reengines and _CHT_787_EIS_YEAR != _CHT_A350_EIS_YEAR:
                if _CHT_787_EIS_YEAR < _CHT_A350_EIS_YEAR:
                    if yr < _CHT_787_EIS_YEAR:
                        b_sh_wb, a_sh_wb = b_eis_wb_base, a_eis_wb_base
                    else:
                        catch_yr = min(yr, _CHT_A350_EIS_YEAR - 1)
                        years_in = catch_yr - _CHT_787_EIS_YEAR + 1
                        b_sh_wb = min(0.80, b_eis_wb_base + 0.03 * years_in)
                        a_sh_wb = 1.0 - b_sh_wb
                else:
                    if yr < _CHT_A350_EIS_YEAR:
                        b_sh_wb, a_sh_wb = b_eis_wb_base, a_eis_wb_base
                    else:
                        catch_yr = min(yr, _CHT_787_EIS_YEAR - 1)
                        years_in = catch_yr - _CHT_A350_EIS_YEAR + 1
                        a_sh_wb = min(0.60, a_eis_wb_base + 0.04 * years_in)
                        b_sh_wb = 1.0 - a_sh_wb
            else:
                b_sh_wb, a_sh_wb = b_eis_wb_base, a_eis_wb_base
            lst_787.append(_CHT_WB_RATE * b_sh_wb)
            lst_a350.append(_CHT_WB_RATE * a_sh_wb)

            # Phase A per-program window mask (WB)
            _b_wb_end_yr = _CHT_787_EIS_YEAR  + NPV_POST_EIS_YRS_AC - 1
            _a_wb_end_yr = _CHT_A350_EIS_YEAR + NPV_POST_EIS_YRS_AC - 1
            if yr > _b_wb_end_yr:
                lst_787[-1] = 0.0
            if yr > _a_wb_end_yr:
                lst_a350[-1] = 0.0

        return lst_737, lst_fps, lst_a320, lst_ngsa, lst_787, lst_a350

    # ============================================================
    # PART 1 — AIRCRAFT DELIVERIES CHART
    # ============================================================
    st.markdown("**1️⃣ Aircraft deliveries — by airframer equilibrium**")

    _ac_pure  = st.session_state.get("_af_nash_pairs", [])
    _ac_near  = st.session_state.get("_af_near_nash_pairs", [])

    if not _ac_pure and not _ac_near:
        st.info("No airframer equilibria computed yet. Visit the Airframer tab first.")
    else:
        # Build dropdown for airframer equilibria
        _ac_options = []  # (label, a_strat, b_strat)
        for i, (a_strat, b_strat, ya, yb) in enumerate(_ac_pure, start=1):
            d = af_decode(a_strat, b_strat)
            label = (f"★ Pure Nash #{i}  |  Boeing {yb:.0f}%  |  Airbus {ya:.0f}%  |  "
                     f"B: {d['Boeing']['NB']} / {d['Boeing']['WB']}  |  "
                     f"A: {d['Airbus']['NB']} / {d['Airbus']['WB']}")
            _ac_options.append((label, a_strat, b_strat))
        for i, (a_strat, b_strat, ya, yb) in enumerate(_ac_near, start=1):
            d = af_decode(a_strat, b_strat)
            label = (f"Near-Nash #{i}  |  Boeing {yb:.0f}%  |  Airbus {ya:.0f}%  |  "
                     f"B: {d['Boeing']['NB']} / {d['Boeing']['WB']}  |  "
                     f"A: {d['Airbus']['NB']} / {d['Airbus']['WB']}")
            _ac_options.append((label, a_strat, b_strat))

        _ac_labels = [opt[0] for opt in _ac_options]
        _ac_pick = st.selectbox(
            "Pick an airframer equilibrium",
            options=_ac_labels,
            index=0,
            key="_ac_eq_pick",
            help="Selecting an equilibrium determines launch/milk choices, "
                 "which set the 737↔fps and A320↔NGSA transitions and the WB shares.",
        )
        _ac_idx = _ac_labels.index(_ac_pick)
        _ac_a_strat, _ac_b_strat = _ac_options[_ac_idx][1], _ac_options[_ac_idx][2]

        # Pull airframer-board parameters (also used by helper for caption)
        _b_nb_move, _b_rate, _b_wb_move = _ac_b_strat
        _b_inc_rate    = "Increase_737_Rate" in _b_rate

        # Compute the 6 per-aircraft delivery lists for this airframer state
        (_ac_737, _ac_fps, _ac_a320, _ac_ngsa,
         _ac_787, _ac_a350) = _compute_aircraft_per_state(_ac_a_strat, _ac_b_strat)

        # Compute cumulative totals (2026-2056) for each platform so the user
        # can see at a glance how many of each model are delivered across the
        # full timeline. Appended to each line's legend label.
        _ac_t737   = int(round(sum(_ac_737)))
        _ac_tfps   = int(round(sum(_ac_fps)))
        _ac_ta320  = int(round(sum(_ac_a320)))
        _ac_tngsa  = int(round(sum(_ac_ngsa)))
        _ac_t787   = int(round(sum(_ac_787)))
        _ac_ta350  = int(round(sum(_ac_a350)))

        _ac_df = pd.DataFrame({
            "737 MAX (Boeing NB)":    _ac_737,
            "Boeing fps (new NB)":    _ac_fps,
            "A320neo (Airbus NB)":    _ac_a320,
            "Airbus NGSA (new NB)":   _ac_ngsa,
            "787 (Boeing WB)":        _ac_787,
            "A350 (Airbus WB)":       _ac_a350,
        }, index=pd.Index(_CHT_YEARS, name="Year"))
        st.line_chart(_ac_df, height=320, use_container_width=True)
        _ac_fps_eis  = int(st.session_state.get('af_fps_eis',  2037))
        _ac_ngsa_eis = int(st.session_state.get('af_ngsa_eis', 2037))
        # Per-program window end-years (Phase A: 20 yrs post-EIS inclusive)
        _ac_b_nb_end_yr = _ac_fps_eis  + NPV_POST_EIS_YRS_AC - 1
        _ac_a_nb_end_yr = _ac_ngsa_eis + NPV_POST_EIS_YRS_AC - 1
        _ac_b_wb_end_yr = _CHT_787_EIS_YEAR  + NPV_POST_EIS_YRS_AC - 1
        _ac_a_wb_end_yr = _CHT_A350_EIS_YEAR + NPV_POST_EIS_YRS_AC - 1

        # Per-period delivery subtotals (pre-EIS legacy vs post-EIS 20-yr window)
        def _sum_in(lst, start_yr, end_yr):
            return int(round(sum(
                lst[i] for i, yr in enumerate(_CHT_YEARS)
                if start_yr <= yr <= end_yr
            )))
        # Boeing NB: 737 pre/post + fps post
        _t_737_pre  = _sum_in(_ac_737, 2026, _ac_fps_eis - 1)
        _t_737_post = _sum_in(_ac_737, _ac_fps_eis, _ac_b_nb_end_yr)
        _t_fps_post = _sum_in(_ac_fps, _ac_fps_eis, _ac_b_nb_end_yr)
        # Airbus NB: A320 pre/post + NGSA post
        _t_a320_pre  = _sum_in(_ac_a320, 2026, _ac_ngsa_eis - 1)
        _t_a320_post = _sum_in(_ac_a320, _ac_ngsa_eis, _ac_a_nb_end_yr)
        _t_ngsa_post = _sum_in(_ac_ngsa, _ac_ngsa_eis, _ac_a_nb_end_yr)
        # Boeing WB: 787 pre/post (one platform, label changes per re-engine choice)
        _t_787_pre  = _sum_in(_ac_787, 2026, _CHT_787_EIS_YEAR - 1)
        _t_787_post = _sum_in(_ac_787, _CHT_787_EIS_YEAR, _ac_b_wb_end_yr)
        # Airbus WB: A350 pre/post
        _t_a350_pre  = _sum_in(_ac_a350, 2026, _CHT_A350_EIS_YEAR - 1)
        _t_a350_post = _sum_in(_ac_a350, _CHT_A350_EIS_YEAR, _ac_a_wb_end_yr)
        # Pre-EIS year counts
        _yrs_b_nb_pre = _ac_fps_eis  - 2026
        _yrs_a_nb_pre = _ac_ngsa_eis - 2026
        _yrs_b_wb_pre = _CHT_787_EIS_YEAR  - 2026
        _yrs_a_wb_pre = _CHT_A350_EIS_YEAR - 2026
        # Decode re-engine choices for table annotation
        _b_reengines_787  = "Re_engine_787"  in _ac_b_strat[2]
        _a_reengines_a350 = "Re_engine_A350" in _ac_a_strat[3]
        _787_post_lbl = "re-engined 787" if _b_reengines_787  else "787 (legacy, milked)"
        _a350_post_lbl = "re-engined A350" if _a_reengines_a350 else "A350 (legacy, milked)"

        st.markdown(
            f"**Aircraft deliveries — per-program windows (Phase A: pre-EIS legacy + 20-yr post-EIS):**"
        )
        # Boeing NB sub-table
        st.markdown(
            f"#### Boeing NB program (fps EIS {_ac_fps_eis} · window 2026–{_ac_b_nb_end_yr})\n\n"
            f"| Period | Year range | Yrs | 737 MAX | Boeing fps | Period total |\n"
            f"|---|---|---:|---:|---:|---:|\n"
            f"| Pre-fps-EIS legacy | 2026–{_ac_fps_eis-1} | {_yrs_b_nb_pre} | "
            f"{_t_737_pre:,} | — | {_t_737_pre:,} |\n"
            f"| Post-fps-EIS (20-yr Phase A window) | {_ac_fps_eis}–{_ac_b_nb_end_yr} | 20 | "
            f"{_t_737_post:,} | {_t_fps_post:,} | {_t_737_post+_t_fps_post:,} |\n"
            f"| **Total Boeing NB** | 2026–{_ac_b_nb_end_yr} | {_yrs_b_nb_pre+20} | "
            f"**{_t_737_pre+_t_737_post:,}** | **{_t_fps_post:,}** | "
            f"**{_t_737_pre+_t_737_post+_t_fps_post:,}** |\n"
        )
        # Airbus NB sub-table
        st.markdown(
            f"#### Airbus NB program (NGSA EIS {_ac_ngsa_eis} · window 2026–{_ac_a_nb_end_yr})\n\n"
            f"| Period | Year range | Yrs | A320neo | Airbus NGSA | Period total |\n"
            f"|---|---|---:|---:|---:|---:|\n"
            f"| Pre-NGSA-EIS legacy | 2026–{_ac_ngsa_eis-1} | {_yrs_a_nb_pre} | "
            f"{_t_a320_pre:,} | — | {_t_a320_pre:,} |\n"
            f"| Post-NGSA-EIS (20-yr Phase A window) | {_ac_ngsa_eis}–{_ac_a_nb_end_yr} | 20 | "
            f"{_t_a320_post:,} | {_t_ngsa_post:,} | {_t_a320_post+_t_ngsa_post:,} |\n"
            f"| **Total Airbus NB** | 2026–{_ac_a_nb_end_yr} | {_yrs_a_nb_pre+20} | "
            f"**{_t_a320_pre+_t_a320_post:,}** | **{_t_ngsa_post:,}** | "
            f"**{_t_a320_pre+_t_a320_post+_t_ngsa_post:,}** |\n"
        )
        # Boeing WB sub-table
        st.markdown(
            f"#### Boeing WB program (787 EIS {_CHT_787_EIS_YEAR} · window 2026–{_ac_b_wb_end_yr})\n\n"
            f"| Period | Year range | Yrs | 787 (legacy) | 787 ({_787_post_lbl}) | Period total |\n"
            f"|---|---|---:|---:|---:|---:|\n"
            f"| Pre-787-EIS legacy | 2026–{_CHT_787_EIS_YEAR-1} | {_yrs_b_wb_pre} | "
            f"{_t_787_pre:,} | — | {_t_787_pre:,} |\n"
            f"| Post-787-EIS (20-yr Phase A window) | {_CHT_787_EIS_YEAR}–{_ac_b_wb_end_yr} | 20 | "
            f"{'—' if _b_reengines_787 else f'{_t_787_post:,}'} | "
            f"{f'{_t_787_post:,}' if _b_reengines_787 else '—'} | {_t_787_post:,} |\n"
            f"| **Total Boeing WB** | 2026–{_ac_b_wb_end_yr} | {_yrs_b_wb_pre+20} | "
            f"**{_t_787_pre + (0 if _b_reengines_787 else _t_787_post):,}** | "
            f"**{(_t_787_post if _b_reengines_787 else 0):,}** | "
            f"**{_t_787_pre+_t_787_post:,}** |\n"
        )
        # Airbus WB sub-table
        st.markdown(
            f"#### Airbus WB program (A350 EIS {_CHT_A350_EIS_YEAR} · window 2026–{_ac_a_wb_end_yr})\n\n"
            f"| Period | Year range | Yrs | A350 (legacy) | A350 ({_a350_post_lbl}) | Period total |\n"
            f"|---|---|---:|---:|---:|---:|\n"
            f"| Pre-A350-EIS legacy | 2026–{_CHT_A350_EIS_YEAR-1} | {_yrs_a_wb_pre} | "
            f"{_t_a350_pre:,} | — | {_t_a350_pre:,} |\n"
            f"| Post-A350-EIS (20-yr Phase A window) | {_CHT_A350_EIS_YEAR}–{_ac_a_wb_end_yr} | 20 | "
            f"{'—' if _a_reengines_a350 else f'{_t_a350_post:,}'} | "
            f"{f'{_t_a350_post:,}' if _a_reengines_a350 else '—'} | {_t_a350_post:,} |\n"
            f"| **Total Airbus WB** | 2026–{_ac_a_wb_end_yr} | {_yrs_a_wb_pre+20} | "
            f"**{_t_a350_pre + (0 if _a_reengines_a350 else _t_a350_post):,}** | "
            f"**{(_t_a350_post if _a_reengines_a350 else 0):,}** | "
            f"**{_t_a350_pre+_t_a350_post:,}** |\n"
        )
        # Grand total
        _ac_grand_nb_v2 = _t_737_pre + _t_737_post + _t_fps_post + _t_a320_pre + _t_a320_post + _t_ngsa_post
        _ac_grand_wb_v2 = _t_787_pre + _t_787_post + _t_a350_pre + _t_a350_post
        st.markdown(
            f"#### Total fleet\n\n"
            f"| Player | NB | WB | Total |\n"
            f"|---|---:|---:|---:|\n"
            f"| Boeing | {_t_737_pre+_t_737_post+_t_fps_post:,} | {_t_787_pre+_t_787_post:,} | "
            f"{_t_737_pre+_t_737_post+_t_fps_post+_t_787_pre+_t_787_post:,} |\n"
            f"| Airbus | {_t_a320_pre+_t_a320_post+_t_ngsa_post:,} | {_t_a350_pre+_t_a350_post:,} | "
            f"{_t_a320_pre+_t_a320_post+_t_ngsa_post+_t_a350_pre+_t_a350_post:,} |\n"
            f"| **Total** | **{_ac_grand_nb_v2:,}** | **{_ac_grand_wb_v2:,}** | "
            f"**{_ac_grand_nb_v2 + _ac_grand_wb_v2:,}** |\n"
        )
        st.caption(
            f"Selected: **{_ac_pick.split('|')[0].strip()}**. "
            f"NB market = 2,000 a/c/yr, WB = 170 a/c/yr. "
            f"Each program's deliveries are counted only within its own 20-yr "
            f"post-EIS Phase A window (plus pre-EIS legacy). "
            f"NB EIS: fps = {_ac_fps_eis}, NGSA = {_ac_ngsa_eis}. "
            f"WB re-engine EIS: 787 = {_CHT_787_EIS_YEAR}, A350 = {_CHT_A350_EIS_YEAR}."
        )

        _render_nb_share_trajectory_block(_ac_a_strat, _ac_b_strat)


        _render_wb_share_trajectory_block(_ac_a_strat, _ac_b_strat)


        _render_player_cash_flow_block(_ac_a_strat, _ac_b_strat)

    st.markdown("---")

    # ============================================================
    # PART 2 — ENGINE DELIVERIES CHART
    # ============================================================
    st.markdown("**2️⃣ Engine deliveries — by engine equilibrium**  "
                "*(aircraft × 2 engines)*")

    _en_pure  = st.session_state.get("_en_nash_pairs", [])
    _en_near  = st.session_state.get("_en_near_nash_pairs", [])
    _en_pw_locked = st.session_state.get("_en_pw_locked_move", "1-Milk GTF")

    if not _en_pure and not _en_near:
        st.info("No engine equilibria computed yet. Visit the Engine tab first.")
    else:
        # Build dropdown for engine equilibria
        # Each entry: (move_a_combo, move_c_combo, yield_a, yield_c)
        # PW move is locked separately (_en_pw_locked).
        _en_options = []  # (label, move_a, move_b, move_c)
        for i, (move_a, move_c, ya, yc) in enumerate(_en_pure, start=1):
            label = (f"★ Pure Nash #{i}  |  CFM {ya:.0f}%  |  RR {yc:.0f}%  |  "
                     f"CFM: {move_a}  |  RR: {move_c}")
            _en_options.append((label, move_a, _en_pw_locked, move_c))
        for i, (move_a, move_c, ya, yc) in enumerate(_en_near, start=1):
            label = (f"Near-Nash #{i}  |  CFM {ya:.0f}%  |  RR {yc:.0f}%  |  "
                     f"CFM: {move_a}  |  RR: {move_c}")
            _en_options.append((label, move_a, _en_pw_locked, move_c))

        _en_labels = [opt[0] for opt in _en_options]
        _en_pick = st.selectbox(
            "Pick an engine equilibrium",
            options=_en_labels,
            index=0,
            key="_en_eq_pick",
            help="Selecting an engine equilibrium applies CFM/PW/RR moves to the "
                 "post-2037 supplier-matrix-derived shares. Aircraft deliveries "
                 "assume the engine-board baseline (both airframers launch).",
        )
        _en_idx = _en_labels.index(_en_pick)
        _en_move_a = _en_options[_en_idx][1]
        _en_move_b = _en_options[_en_idx][2]
        _en_move_c = _en_options[_en_idx][3]

        # Pull engine-board parameters (mirror engine simulate).
        # NOTE: the sliders for en_openfan_loss and en_ducted_gain store values
        # in PERCENT (e.g., 35 and 10), and the engine board divides by 100
        # at the slider definition (line ~1467-1468). We replicate that here.
        _open_fan_loss  = float(st.session_state.get('en_openfan_loss', 35)) / 100.0
        _ducted_gain    = float(st.session_state.get('en_ducted_gain',  10)) / 100.0

        # Pull supplier-matrix codes (used to map post-2037 NB engines to makers)
        _b_supplier_str = st.session_state.get("_b_supplier", "RR and CFM")
        _a_supplier_str = st.session_state.get("_a_supplier", "PW and CFM")
        _b_sup_code = SUPPLIER_CODE.get(_b_supplier_str, 5)
        _a_sup_code = SUPPLIER_CODE.get(_a_supplier_str, 6)
        _b_sup_engines = supplier_engines(_b_sup_code)
        _a_sup_engines = supplier_engines(_a_sup_code)
        _b_per_eng = 1.0 / max(1, len(_b_sup_engines))
        _a_per_eng = 1.0 / max(1, len(_a_sup_engines))

        # Boeing/Airbus market-share split (independent of aircraft section
        # — re-fetched in case that section's `else` branch didn't execute)
        _boeing_share = float(st.session_state.get('_boeing_share_both', 50))

        # Compute post-2037 maker shares by applying engine moves to the
        # SAME starting shares the engine board uses. The engine board reads
        # `f_cfm_nb`, `f_pw_nb`, `f_rr_nb`, `f_cfm_wb`, `f_rr_wb` from session
        # state and normalises (see run_engine_board lines 1541-1542). These
        # slider values auto-track the supplier matrix unless the user
        # manually overrides them, so reading them directly is the source
        # of truth for "what shares the engine board sees".
        def _norm3(a, b, c):
            t = a + b + c
            return (a/t, b/t, c/t) if t > 0 else (0.0, 0.0, 0.0)

        _fut_cfm_nb = float(st.session_state.get('f_cfm_nb', 53))
        _fut_pw_nb  = float(st.session_state.get('f_pw_nb',  50))
        _fut_rr_nb  = float(st.session_state.get('f_rr_nb',  50))
        _fut_cfm_wb = float(st.session_state.get('f_cfm_wb', 42))
        _fut_rr_wb  = float(st.session_state.get('f_rr_wb',  58))
        a_nb, b_nb, c_nb = _norm3(_fut_cfm_nb, _fut_pw_nb,  _fut_rr_nb)
        a_wb, b_wb, c_wb = _norm3(_fut_cfm_wb, 0.0,         _fut_rr_wb)

        jv_nb_active = False

        # ── PLAYER A (CFM) — mirrors simulate() lines ~1580-1620 ─
        if "1-Open Fan" in _en_move_a:
            a_nb -= _open_fan_loss
            if "Ultrafan NB" in _en_move_c or "JV with PW" in _en_move_c:
                b_nb += _open_fan_loss/2; c_nb += _open_fan_loss/2
            else:
                b_nb += _open_fan_loss
        if "2-Ducted" in _en_move_a or "3-Open + Ducted" in _en_move_a:
            a_nb += _ducted_gain
            if "Ultrafan NB" in _en_move_c or "JV with PW" in _en_move_c:
                b_nb -= _ducted_gain/2; c_nb -= _ducted_gain/2
            else:
                b_nb -= _ducted_gain
        if "4-Partner Embraer" in _en_move_a:
            a_nb += 0.05
        if "5-Lobby Govts" in _en_move_a:
            a_nb += 0.05
        if "6-Upgrade GenX9" in _en_move_a: a_wb += 0.05
        if "7-Invest GenX"   in _en_move_a: a_wb += 0.05

        # ── PLAYER B (PW) ───────────────────────────────────────
        if "2-Launch GTF2" in _en_move_b:
            b_nb += 0.10; a_nb -= 0.05; c_nb -= 0.05
        if "3-JV with RR" in _en_move_b:
            jv_nb_active = True
            a_nb -= 0.10; b_nb += 0.05; c_nb += 0.05

        # ── PLAYER C (RR) ───────────────────────────────────────
        if "1-Ultrafan WB"  in _en_move_c: c_wb += 0.10; a_wb -= 0.10
        if "2-Ultrafan NB"  in _en_move_c:
            c_nb += 0.15; a_nb -= 0.10; b_nb -= 0.05
        if "3-JV with PW"   in _en_move_c:
            jv_nb_active = True
            c_nb += 0.05; b_nb += 0.05; a_nb -= 0.10
        if "4-Upgrade T1000" in _en_move_c:
            c_wb += 0.05; a_wb -= 0.05

        if jv_nb_active:
            avg_nb = (b_nb + c_nb) / 2.0
            b_nb = avg_nb; c_nb = avg_nb

        # Floor + normalize
        a_nb = max(0.0, a_nb); b_nb = max(0.0, b_nb); c_nb = max(0.0, c_nb)
        a_wb = max(0.0, a_wb); b_wb = max(0.0, b_wb); c_wb = max(0.0, c_wb)
        t_nb = a_nb + b_nb + c_nb
        if t_nb > 0: a_nb/=t_nb; b_nb/=t_nb; c_nb/=t_nb
        t_wb = a_wb + b_wb + c_wb
        if t_wb > 0: a_wb/=t_wb; b_wb/=t_wb; c_wb/=t_wb

        # The aircraft deliveries that feed the engine chart should match the
        # aircraft chart for the SAME airframer equilibrium. We re-resolve the
        # airframer equilibrium picked in the aircraft chart's dropdown
        # (_ac_eq_pick) and call the shared helper. If no airframer equilibria
        # are loaded yet, we fall back to a neutral both-launch baseline so
        # the engine chart still renders.
        _af_pure_for_eng  = st.session_state.get("_af_nash_pairs", [])
        _af_near_for_eng  = st.session_state.get("_af_near_nash_pairs", [])

        _ac_aircraft = None  # (lst_737, lst_fps, lst_a320, lst_ngsa, lst_787, lst_a350)
        _af_state_for_caption = "neutral both-launch baseline"
        _af_inc_rate_for_caption = False
        if _af_pure_for_eng or _af_near_for_eng:
            # Re-build option list to look up the current selection
            _af_opts = []
            for i, (a_strat, b_strat, ya, yb) in enumerate(_af_pure_for_eng, start=1):
                d = af_decode(a_strat, b_strat)
                lbl = (f"★ Pure Nash #{i}  |  Boeing {yb:.0f}%  |  Airbus {ya:.0f}%  |  "
                       f"B: {d['Boeing']['NB']} / {d['Boeing']['WB']}  |  "
                       f"A: {d['Airbus']['NB']} / {d['Airbus']['WB']}")
                _af_opts.append((lbl, a_strat, b_strat))
            for i, (a_strat, b_strat, ya, yb) in enumerate(_af_near_for_eng, start=1):
                d = af_decode(a_strat, b_strat)
                lbl = (f"Near-Nash #{i}  |  Boeing {yb:.0f}%  |  Airbus {ya:.0f}%  |  "
                       f"B: {d['Boeing']['NB']} / {d['Boeing']['WB']}  |  "
                       f"A: {d['Airbus']['NB']} / {d['Airbus']['WB']}")
                _af_opts.append((lbl, a_strat, b_strat))

            _af_labels_for_eng = [opt[0] for opt in _af_opts]
            # Read the aircraft chart's selection from session state, falling
            # back to the first available equilibrium if not yet set.
            _ac_pick_for_eng = st.session_state.get("_ac_eq_pick", _af_labels_for_eng[0])
            if _ac_pick_for_eng in _af_labels_for_eng:
                _ac_idx_for_eng = _af_labels_for_eng.index(_ac_pick_for_eng)
            else:
                _ac_idx_for_eng = 0
            _af_a_strat_for_eng = _af_opts[_ac_idx_for_eng][1]
            _af_b_strat_for_eng = _af_opts[_ac_idx_for_eng][2]
            _ac_aircraft = _compute_aircraft_per_state(_af_a_strat_for_eng,
                                                       _af_b_strat_for_eng)
            _af_state_for_caption = _af_opts[_ac_idx_for_eng][0].split("|")[0].strip()
            _af_inc_rate_for_caption = "Increase_737_Rate" in _af_b_strat_for_eng[1]

        if _ac_aircraft is None:
            # Fallback: simulate a neutral "both launch, no milking, no rate hike"
            # state so the engine chart still has consistent aircraft volumes.
            _fb_a = ("Launch_NGSA", "No_Bottleneck", "No_Poaching", "Milk_A350")
            _fb_b = ("Launch_fps_10yr_Solo", "No_Rate_Increase", "Re_engine_787")
            _ac_aircraft = _compute_aircraft_per_state(_fb_a, _fb_b)
        _ac_737_eng, _ac_fps_eng, _ac_a320_eng, _ac_ngsa_eng, \
        _ac_787_eng, _ac_a350_eng = _ac_aircraft

        # Per-year engine deliveries — one line per engine product
        leap1b   = []   # CFM on 737
        leap1a   = []   # CFM on A320
        gtf      = []   # PW on A320
        fps_rr   = []   # RR engines on fps (post-2037)
        fps_cfm  = []   # CFM engines on fps (post-2037)
        fps_pw   = []   # PW engines on fps (only if supplier matrix has PW for fps)
        ngsa_pw  = []   # PW engines on NGSA
        ngsa_cfm = []   # CFM engines on NGSA
        ngsa_rr  = []   # RR engines on NGSA (only if matrix has RR for NGSA)
        # WB legacy products
        genx     = []   # CFM/GE GenX on 787 (legacy)
        trent1k  = []   # RR Trent 1000 on 787 (legacy)
        trent_xwb= []   # RR Trent XWB on A350 (legacy)
        # WB next-gen products — populated only when the platform re-engines
        # AND the engine maker has a qualifying next-gen move. If a re-engined
        # platform has no eligible maker, those engines vanish from the chart
        # (visible model gap; matches the Q3 rule "RR loses ALL WB deliveries
        # on a re-engined platform if no Ultrafan WB").
        genx9_787       = []   # CFM/GE GenX9 on re-engined 787
        ultrafan_787    = []   # RR Ultrafan WB on re-engined 787
        ultrafan_a350   = []   # RR Ultrafan WB on re-engined A350

        # Year-independent capability detection (from engine moves & airframer state)
        _b_787_re   = "Re_engine_787"  in _af_b_strat_for_eng[2]
        _a_a350_re  = "Re_engine_A350" in _af_a_strat_for_eng[3]
        _cfm_has_787_ng = ("6-Upgrade GenX9" in _en_move_a or
                           "7-Invest GenX"   in _en_move_a)
        _rr_has_uf_wb   = ("1-Ultrafan WB"   in _en_move_c)

        def _allocate_to_slots(maker_totals, slot_capacities, slot_eligibility):
            """Assign each maker's total engine output across the slots they
            can supply, such that BOTH (1) each maker's total is preserved
            (= the engine board's aggregate maker share × total engines) AND
            (2) each slot's capacity is exactly filled.

            This is the supply-constrained transportation that fixes the
            "double-counting CFM in both fps and NGSA" bug that the previous
            within-slot proportional allocator produced.

            Strategy: makers eligible for exactly one slot take their full
            total from that slot; multi-slot makers then fill remaining
            capacity proportionally.

            maker_totals      = {"CFM": float, "PW": float, "RR": float}
            slot_capacities   = {"fps": float, "NGSA": float, ...}
            slot_eligibility  = {"fps": {"RR","CFM"}, ...}

            Returns: {slot: {maker: engines}}
            """
            # Index each maker → set of eligible slots
            maker_eligible = {}
            for slot, makers in slot_eligibility.items():
                for m in makers:
                    maker_eligible.setdefault(m, set()).add(slot)

            allocation = {slot: {} for slot in slot_capacities}
            remaining_capacity = dict(slot_capacities)
            remaining_total = dict(maker_totals)

            # Pass 1: exclusive (single-slot) makers
            for maker, slots in maker_eligible.items():
                if len(slots) == 1:
                    slot = next(iter(slots))
                    qty = min(remaining_total.get(maker, 0.0),
                              remaining_capacity[slot])
                    if qty > 0:
                        allocation[slot][maker] = qty
                    remaining_total[maker] = remaining_total.get(maker, 0.0) - qty
                    remaining_capacity[slot] -= qty

            # Pass 2: multi-slot makers — fill remaining capacity proportionally
            for maker, slots in maker_eligible.items():
                if len(slots) > 1:
                    maker_left = remaining_total.get(maker, 0.0)
                    if maker_left <= 0:
                        continue
                    cap_tot = sum(remaining_capacity[s] for s in slots)
                    if cap_tot <= 0:
                        continue
                    for slot in slots:
                        share = remaining_capacity[slot] / cap_tot
                        qty = maker_left * share
                        allocation[slot][maker] = allocation[slot].get(maker, 0.0) + qty
                        remaining_capacity[slot] -= qty
                    remaining_total[maker] = 0.0

            return allocation

        # Engine delivery chart's WB share switch tracks the engine board's
        # WB_EIS_T = min(787, A350) year — same sync rule the engine NPV uses.
        _en_wb_eis_year = min(_CHT_787_EIS_YEAR, _CHT_A350_EIS_YEAR)
        for idx, yr in enumerate(_CHT_YEARS):
            is_post_wb = (yr >= _en_wb_eis_year)

            # Aircraft deliveries — taken from helper output (matches aircraft
            # chart for the same airframer equilibrium).
            ac_737  = _ac_737_eng [idx]
            ac_fps  = _ac_fps_eng [idx]
            ac_a320 = _ac_a320_eng[idx]
            ac_ngsa = _ac_ngsa_eng[idx]
            ac_787  = _ac_787_eng [idx]
            ac_a350 = _ac_a350_eng[idx]

            # Legacy NB aircraft → fixed engine mappings (regardless of year):
            # 737 → CFM LEAP-1B; A320 → CFM LEAP-1A (60%) + PW GTF (40%).
            leap1b.append (ac_737  * 2.0 * 1.00)
            leap1a.append (ac_a320 * 2.0 * 0.60)
            gtf.append    (ac_a320 * 2.0 * 0.40)

            # New NB aircraft (post-2037 if launched) → engine equilibrium's
            # NB share modifications, allocated supply-constrained so the
            # chart's per-maker totals = engine board's aggregate maker shares.
            fps_eng_total  = ac_fps  * 2.0
            ngsa_eng_total = ac_ngsa * 2.0
            total_new_nb_engines = fps_eng_total + ngsa_eng_total

            if total_new_nb_engines > 0:
                nb_maker_totals = {
                    "CFM": a_nb * total_new_nb_engines,
                    "PW":  b_nb * total_new_nb_engines,
                    "RR":  c_nb * total_new_nb_engines,
                }
                nb_slot_caps = {"fps": fps_eng_total, "NGSA": ngsa_eng_total}
                nb_slot_elig = {"fps": _b_sup_engines, "NGSA": _a_sup_engines}
                nb_alloc = _allocate_to_slots(nb_maker_totals, nb_slot_caps, nb_slot_elig)
            else:
                nb_alloc = {"fps": {}, "NGSA": {}}

            fps_rr .append(nb_alloc["fps"].get("RR",  0.0))
            fps_cfm.append(nb_alloc["fps"].get("CFM", 0.0))
            fps_pw .append(nb_alloc["fps"].get("PW",  0.0))
            ngsa_pw .append(nb_alloc["NGSA"].get("PW",  0.0))
            ngsa_cfm.append(nb_alloc["NGSA"].get("CFM", 0.0))
            ngsa_rr .append(nb_alloc["NGSA"].get("RR",  0.0))

            # WB engines: product identity depends on (a) each platform's
            # EIS year, (b) whether the airframer re-engined it, (c) whether
            # the engine maker has a qualifying next-gen product. Each platform
            # is in either LEGACY mode (pre-EIS OR not re-engined) or NEXT-GEN
            # mode (post-EIS AND re-engined). Maker eligibility per slot:
            #   787-legacy   → {CFM via GenX,   RR via Trent 1000}
            #   787-nextgen  → {CFM via GenX9 if Upgrade/Invest, RR via Ultrafan WB}
            #   A350-legacy  → {RR via Trent XWB}
            #   A350-nextgen → {RR via Ultrafan WB}
            wb_787_total = ac_787 * 2.0
            wb_a350_total = ac_a350 * 2.0
            total_wb_engines = wb_787_total + wb_a350_total

            # 787 state for this year
            _787_is_ng = (yr >= _CHT_787_EIS_YEAR) and _b_787_re
            if _787_is_ng:
                cap_787_leg, cap_787_ng = 0.0, wb_787_total
                elig_787_leg = set()
                elig_787_ng = set()
                if _cfm_has_787_ng: elig_787_ng.add("CFM")
                if _rr_has_uf_wb:   elig_787_ng.add("RR")
            else:
                cap_787_leg, cap_787_ng = wb_787_total, 0.0
                elig_787_leg = {"CFM", "RR"}
                elig_787_ng = set()

            # A350 state for this year
            _a350_is_ng = (yr >= _CHT_A350_EIS_YEAR) and _a_a350_re
            if _a350_is_ng:
                cap_a350_leg, cap_a350_ng = 0.0, wb_a350_total
                elig_a350_leg = set()
                elig_a350_ng = set()
                if _rr_has_uf_wb: elig_a350_ng.add("RR")
            else:
                cap_a350_leg, cap_a350_ng = wb_a350_total, 0.0
                elig_a350_leg = {"RR"}
                elig_a350_ng = set()

            if is_post_wb and total_wb_engines > 0:
                wb_maker_totals = {
                    "CFM": a_wb * total_wb_engines,
                    "RR":  c_wb * total_wb_engines,
                }
                wb_slot_caps = {
                    "787-legacy":   cap_787_leg,
                    "787-nextgen":  cap_787_ng,
                    "A350-legacy":  cap_a350_leg,
                    "A350-nextgen": cap_a350_ng,
                }
                wb_slot_elig = {
                    "787-legacy":   elig_787_leg,
                    "787-nextgen":  elig_787_ng,
                    "A350-legacy":  elig_a350_leg,
                    "A350-nextgen": elig_a350_ng,
                }
                wb_alloc = _allocate_to_slots(wb_maker_totals, wb_slot_caps, wb_slot_elig)
                cfm_787_leg = wb_alloc["787-legacy"].get("CFM", 0.0)
                rr_787_leg  = wb_alloc["787-legacy"].get("RR",  0.0)
                cfm_787_ng  = wb_alloc["787-nextgen"].get("CFM", 0.0)
                rr_787_ng   = wb_alloc["787-nextgen"].get("RR",  0.0)
                rr_a350_leg = wb_alloc["A350-legacy"].get("RR", 0.0)
                rr_a350_ng  = wb_alloc["A350-nextgen"].get("RR", 0.0)
            else:
                # Pre-WB-EIS: historical 70/30 split on 787, RR on A350.
                # All platforms necessarily in legacy mode here.
                cfm_787_leg = wb_787_total * 0.70
                rr_787_leg  = wb_787_total * 0.30
                rr_a350_leg = wb_a350_total
                cfm_787_ng  = 0.0
                rr_787_ng   = 0.0
                rr_a350_ng  = 0.0

            genx          .append(cfm_787_leg)
            trent1k       .append(rr_787_leg)
            trent_xwb     .append(rr_a350_leg)
            genx9_787     .append(cfm_787_ng)
            ultrafan_787  .append(rr_787_ng)
            ultrafan_a350 .append(rr_a350_ng)

        # Build the engine deliveries dataframe — one line per product × maker.
        # Only include lines that have any non-zero data (avoid useless 0-lines).
        _en_data = {
            "LEAP-1B  (CFM/GE — 737)":           leap1b,
            "LEAP-1A  (CFM/GE — A320)":          leap1a,
            "GTF  (Pratt & Whitney — A320)":     gtf,
            "fps engine  (RR — fps)":            fps_rr,
            "fps engine  (CFM/GE — fps)":        fps_cfm,
            "fps engine  (PW — fps)":            fps_pw,
            "NGSA engine  (PW — NGSA)":          ngsa_pw,
            "NGSA engine  (CFM/GE — NGSA)":      ngsa_cfm,
            "NGSA engine  (RR — NGSA)":          ngsa_rr,
            "GenX  (CFM/GE — 787)":              genx,
            "GenX9  (CFM/GE — 787 re-engined)":  genx9_787,
            "Trent 1000  (RR — 787)":            trent1k,
            "Ultrafan WB  (RR — 787 re-engined)": ultrafan_787,
            "Trent XWB  (RR — A350)":            trent_xwb,
            "Ultrafan WB  (RR — A350 re-engined)": ultrafan_a350,
        }
        # Drop lines that are all zero (no engines of that type ever delivered)
        _en_data = {k: v for k, v in _en_data.items() if max(v) > 1e-6}

        # Compute cumulative totals (31-yr) per engine type for the per-model
        # table below the chart (NOT for legend labels — the labels stay clean
        # to avoid overlap on the chart itself).
        _en_totals = {k: int(round(sum(v))) for k, v in _en_data.items()}

        _en_df = pd.DataFrame(_en_data, index=pd.Index(_CHT_YEARS, name="Year"))
        st.line_chart(_en_df, height=360, use_container_width=True)
        _en_nb_eis_year = min(int(st.session_state.get('af_fps_eis',  2037)),
                              int(st.session_state.get('af_ngsa_eis', 2037)))

        # 31-yr totals — per-engine model + by-maker summary, displayed below
        # the chart in two grouped tables
        _en_wb_markers_cap = ['GenX', 'Trent 1000', 'Ultrafan WB', 'Trent XWB']

        def _en_maker(k):
            if 'CFM/GE' in k:
                return 'CFM/GE'
            if 'Pratt & Whitney' in k or '(PW —' in k:
                return 'PW'
            if 'RR —' in k:
                return 'RR'
            return '?'

        def _en_is_wb(k):
            return any(m in k for m in _en_wb_markers_cap)

        _en_cfm_nb = sum(t for k, t in _en_totals.items()
                         if _en_maker(k) == 'CFM/GE' and not _en_is_wb(k))
        _en_pw_nb  = sum(t for k, t in _en_totals.items()
                         if _en_maker(k) == 'PW' and not _en_is_wb(k))
        _en_rr_nb  = sum(t for k, t in _en_totals.items()
                         if _en_maker(k) == 'RR' and not _en_is_wb(k))
        _en_cfm_wb = sum(t for k, t in _en_totals.items()
                         if _en_maker(k) == 'CFM/GE' and _en_is_wb(k))
        _en_rr_wb  = sum(t for k, t in _en_totals.items()
                         if _en_maker(k) == 'RR' and _en_is_wb(k))
        _en_grand_nb = _en_cfm_nb + _en_pw_nb + _en_rr_nb
        _en_grand_wb = _en_cfm_wb + _en_rr_wb

        # Per-engine table — show the actual delivery period for each engine
        # (first non-zero year → last non-zero year) so the engine table
        # is 100% consistent with the per-program aircraft table.
        def _engine_period(lst):
            non_zero = [yr for i, yr in enumerate(_CHT_YEARS) if lst[i] > 1e-6]
            if not non_zero:
                return None
            return (min(non_zero), max(non_zero))

        _en_rows = []
        for _k in sorted(_en_totals.keys(), key=lambda x: (-_en_totals[x], x)):
            _lst = _en_data[_k]
            _per = _engine_period(_lst)
            if _per is None:
                _per_str = "—"; _per_yrs = 0
            else:
                _per_str = f"{_per[0]}–{_per[1]}"
                _per_yrs = _per[1] - _per[0] + 1
            _en_rows.append(
                f"| {_k} | {_per_str} | {_per_yrs} | {_en_totals[_k]:,} | "
                f"{_en_maker(_k)} {'WB' if _en_is_wb(_k) else 'NB'} |"
            )
        st.markdown(
            f"**Engine deliveries — per actual delivery period (consistent with aircraft table):**\n\n"
            f"| Engine | Period | Yrs | Total | Maker / Market |\n"
            f"|---|---|---:|---:|---|\n"
            + "\n".join(_en_rows) + "\n"
            f"\n*Each engine = the 2 engines per aircraft × the aircraft "
            f"platform's deliveries, so periods mirror the per-program window "
            f"masks in the aircraft table. Cross-check: any engine's total = "
            f"(corresponding aircraft total) × 2 × (maker's share of that "
            f"platform's engine supply).*"
        )
        st.markdown(
            f"**By maker (per-program windows):**\n\n"
            f"| Maker | NB engines | WB engines | Total |\n"
            f"|---|---:|---:|---:|\n"
            f"| CFM/GE | {_en_cfm_nb:,} | {_en_cfm_wb:,} | {_en_cfm_nb + _en_cfm_wb:,} |\n"
            f"| PW | {_en_pw_nb:,} | 0 | {_en_pw_nb:,} |\n"
            f"| RR | {_en_rr_nb:,} | {_en_rr_wb:,} | {_en_rr_nb + _en_rr_wb:,} |\n"
            f"| **Total** | **{_en_grand_nb:,}** | **{_en_grand_wb:,}** "
            f"| **{_en_grand_nb + _en_grand_wb:,}** |\n"
        )
        st.caption(
            f"Engine equilibrium: **{_en_pick.split('|')[0].strip()}**  ·  "
            f"Aircraft volumes from airframer state: **{_af_state_for_caption}** "
            f"({'rate hike active' if _af_inc_rate_for_caption else 'no rate hike'}).  "
            f"Engines = aircraft × 2.  "
            f"Legacy: 737 → CFM LEAP-1B; A320 → CFM LEAP-1A (60%) + PW GTF (40%); "
            f"787 → CFM/GE GenX (70%) + RR Trent 1000 (30%); A350 → RR Trent XWB. "
            f"fps engines from {sorted(_b_sup_engines)} from fps EIS, NGSA engines from "
            f"{sorted(_a_sup_engines)} from NGSA EIS, allocated per engine-equilibrium "
            f"maker shares (CFM {a_nb*100:.0f}% / PW {b_nb*100:.0f}% / RR {c_nb*100:.0f}% "
            f"NB after moves). "
            f"NB engine maker share switches at **{_en_nb_eis_year}** (= min(fps EIS, "
            f"NGSA EIS)). "
            f"WB engine maker share switches at **{_en_wb_eis_year}** (= min(787 EIS "
            f"{_CHT_787_EIS_YEAR}, A350 EIS {_CHT_A350_EIS_YEAR})). "
            f"**WB product identity is per-platform:** each platform flips from "
            f"legacy (GenX/Trent 1000 on 787, Trent XWB on A350) to next-gen "
            f"(GenX9 on re-engined 787, Ultrafan WB on re-engined platform) at "
            f"its own EIS year — but ONLY if the airframer re-engined AND the "
            f"engine maker has a qualifying next-gen move (CFM: Upgrade GenX9 or "
            f"Invest GenX; RR: Ultrafan WB). If a maker has no qualifying product, "
            f"those deliveries vanish from the chart (visible model gap)."
        )

        # ============================================================
        # NB ENGINE MAKER SHARE TRAJECTORY w/ DRIVER ANNOTATIONS
        # Companion chart to the engine delivery chart. Aggregates the
        # NB engine deliveries (filtered out of _en_data) by maker
        # (CFM/GE, PW, RR) and shows % share of total NB engines/year.
        # Annotates at fps EIS and NGSA EIS trigger years.
        # ============================================================
        _eng_wb_markers = ['GenX', 'Trent 1000', 'Ultrafan WB', 'Trent XWB']
        _eng_nb_keys = [k for k in _en_data
                        if not any(m in k for m in _eng_wb_markers)]
        _eng_cfm_keys = [k for k in _eng_nb_keys if 'CFM/GE' in k]
        _eng_pw_keys  = [k for k in _eng_nb_keys
                         if 'Pratt & Whitney' in k or '(PW —' in k]
        _eng_rr_keys  = [k for k in _eng_nb_keys if 'RR —' in k]

        _eng_n = len(_CHT_YEARS)
        _eng_cfm_tot = [sum(_en_data[k][i] for k in _eng_cfm_keys) for i in range(_eng_n)]
        _eng_pw_tot  = [sum(_en_data[k][i] for k in _eng_pw_keys)  for i in range(_eng_n)]
        _eng_rr_tot  = [sum(_en_data[k][i] for k in _eng_rr_keys)  for i in range(_eng_n)]

        _eng_cfm_sh, _eng_pw_sh, _eng_rr_sh = [], [], []
        for _i in range(_eng_n):
            _tot = _eng_cfm_tot[_i] + _eng_pw_tot[_i] + _eng_rr_tot[_i]
            if _tot > 1e-6:
                _eng_cfm_sh.append(100.0 * _eng_cfm_tot[_i] / _tot)
                _eng_pw_sh.append (100.0 * _eng_pw_tot[_i]  / _tot)
                _eng_rr_sh.append (100.0 * _eng_rr_tot[_i]  / _tot)
            else:
                # No deliveries this year (rare) — pad with 0s so the chart
                # has continuous lines
                _eng_cfm_sh.append(0.0)
                _eng_pw_sh.append(0.0)
                _eng_rr_sh.append(0.0)

        # Driver annotations for engines — limited to fps/NGSA EIS triggers
        # (engine-maker move choices don't have a year-trigger; they're
        # baked into the supplier matrix and apply at fps/NGSA EIS).
        _eng_b_launches = "Launch_fps"  in _af_b_strat_for_eng[0]
        _eng_a_launches = "Launch_NGSA" in _af_a_strat_for_eng[0]
        _eng_fps_eis_yr  = int(st.session_state.get('af_fps_eis',  2037))
        _eng_ngsa_eis_yr = int(st.session_state.get('af_ngsa_eis', 2037))

        _eng_drivers = {}
        if _eng_b_launches and _eng_a_launches and _eng_fps_eis_yr == _eng_ngsa_eis_yr:
            _eng_drivers[_eng_fps_eis_yr] = (
                f"fps + NGSA EIS\n737 → fps ({'+'.join(sorted(_b_sup_engines))})\n"
                f"A320 → NGSA ({'+'.join(sorted(_a_sup_engines))})")
        else:
            if _eng_b_launches:
                _eng_drivers[_eng_fps_eis_yr] = (
                    f"fps EIS\n737 (CFM-only) → fps ({'+'.join(sorted(_b_sup_engines))})")
            if _eng_a_launches:
                _eng_drivers[_eng_ngsa_eis_yr] = (
                    f"NGSA EIS\nA320 (CFM 60% / PW 40%) → NGSA ({'+'.join(sorted(_a_sup_engines))})")

        # Build plotly figure — 3 lines (CFM, PW, RR) over 2026-2056
        _eng_fig = go.Figure()
        _eng_fig.add_trace(go.Scatter(
            x=list(_CHT_YEARS), y=_eng_cfm_sh, mode='lines+markers',
            name='CFM/GE', line=dict(color='#2ca02c', width=3),
            marker=dict(size=5),
            hovertemplate='%{x}: %{y:.1f}%<extra>CFM/GE</extra>'))
        _eng_fig.add_trace(go.Scatter(
            x=list(_CHT_YEARS), y=_eng_pw_sh, mode='lines+markers',
            name='PW', line=dict(color='#d62728', width=3),
            marker=dict(size=5),
            hovertemplate='%{x}: %{y:.1f}%<extra>PW</extra>'))
        _eng_fig.add_trace(go.Scatter(
            x=list(_CHT_YEARS), y=_eng_rr_sh, mode='lines+markers',
            name='RR', line=dict(color='#9467bd', width=3),
            marker=dict(size=5),
            hovertemplate='%{x}: %{y:.1f}%<extra>RR</extra>'))

        # Annotations + dotted vertical lines at trigger years
        _eng_label_high = 92
        _eng_label_low  = 8
        _eng_alt = True
        for _yr_lbl in sorted(_eng_drivers.keys()):
            if _yr_lbl < 2026 or _yr_lbl > 2056:
                continue
            _label = _eng_drivers[_yr_lbl]
            _eng_fig.add_vline(x=_yr_lbl, line_dash='dot',
                               line_color='rgba(200,200,200,0.65)',
                               line_width=1.2)
            _y_pos = _eng_label_high if _eng_alt else _eng_label_low
            _eng_alt = not _eng_alt
            _eng_fig.add_annotation(
                x=_yr_lbl, y=_y_pos,
                text=f"<b>{_yr_lbl}</b><br>{_label.replace(chr(10), '<br>')}",
                showarrow=False, font=dict(size=11, color='#222'),
                align='left', bgcolor='rgba(255,255,255,0.93)',
                bordercolor='rgba(180,180,180,0.7)', borderwidth=1,
                borderpad=4, xanchor='left', xshift=2)

        _eng_fig.update_layout(
            title=dict(text='NB Engine Maker Share Trajectory — with Driver Annotations',
                       font=dict(size=14, color='#eee')),
            xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                       title_font=dict(color='#eee'),
                       tickfont=dict(color='#ddd'),
                       gridcolor='rgba(255,255,255,0.08)',
                       zerolinecolor='rgba(255,255,255,0.15)'),
            yaxis=dict(title='NB engine share (%)', range=[0, 100], dtick=10,
                       title_font=dict(color='#eee'),
                       tickfont=dict(color='#ddd'),
                       gridcolor='rgba(255,255,255,0.08)',
                       zerolinecolor='rgba(255,255,255,0.15)'),
            height=460, margin=dict(l=50, r=20, t=50, b=40),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02,
                        xanchor='right', x=1,
                        font=dict(color='#eee'),
                        bgcolor='rgba(0,0,0,0)'),
            plot_bgcolor='#000',
            paper_bgcolor='#000'
        )
        st.plotly_chart(_eng_fig, use_container_width=True)
        st.caption(
            "NB engine maker share % per year, computed from the engine "
            "delivery chart above by aggregating CFM/GE, PW, and RR lines "
            "(excluding WB engines). Three lines sum to 100% in every "
            "year. Vertical dotted lines mark fps EIS and NGSA EIS — the "
            "trigger years where Boeing's and Airbus's NB platforms flip "
            "and the supplier matrix re-routes deliveries. Pre-EIS "
            "structure: CFM owns 737 (LEAP-1B sole-source) and 60% of "
            "A320 (LEAP-1A); PW has 40% of A320 (GTF); RR has 0% NB. "
            "Post-EIS: shares depend on supplier matrix × engine-equilibrium "
            "maker shares (if a maker lacks a qualifying next-gen product, "
            "they vanish from their slot — model gap visible)."
        )

        # ============================================================
        # WB ENGINE MAKER SHARE TRAJECTORY w/ DRIVER ANNOTATIONS
        # Companion chart for the WB engine market. Filters _en_data to
        # WB engines only (GenX, GenX9, Trent 1000, Trent XWB, Ultrafan WB)
        # and aggregates by maker (CFM/GE, RR — PW has no WB engines).
        # Annotates at 787 EIS / A350 EIS trigger years.
        # ============================================================
        _eng_wb_keys = [k for k in _en_data
                        if any(m in k for m in
                               ['GenX', 'Trent 1000', 'Ultrafan WB', 'Trent XWB'])]
        _eng_wb_cfm_keys = [k for k in _eng_wb_keys if 'CFM/GE' in k]
        _eng_wb_rr_keys  = [k for k in _eng_wb_keys if 'RR —' in k]

        _eng_n = len(_CHT_YEARS)
        _eng_wb_cfm_tot = [sum(_en_data[k][i] for k in _eng_wb_cfm_keys)
                           for i in range(_eng_n)]
        _eng_wb_rr_tot  = [sum(_en_data[k][i] for k in _eng_wb_rr_keys)
                           for i in range(_eng_n)]

        _eng_wb_cfm_sh, _eng_wb_rr_sh = [], []
        for _i in range(_eng_n):
            _tot = _eng_wb_cfm_tot[_i] + _eng_wb_rr_tot[_i]
            if _tot > 1e-6:
                _eng_wb_cfm_sh.append(100.0 * _eng_wb_cfm_tot[_i] / _tot)
                _eng_wb_rr_sh.append (100.0 * _eng_wb_rr_tot[_i]  / _tot)
            else:
                _eng_wb_cfm_sh.append(0.0)
                _eng_wb_rr_sh.append(0.0)

        # Driver labels — 787 EIS and A350 EIS (only when re-engined)
        _eng_wb_b_reengines = "Re_engine_787"  in _af_b_strat_for_eng[2]
        _eng_wb_a_reengines = "Re_engine_A350" in _af_a_strat_for_eng[3]
        _eng_wb_787_eis  = int(st.session_state.get('af_787_eis',  2041))
        _eng_wb_a350_eis = int(st.session_state.get('af_a350_eis', 2035))

        _eng_wb_drivers = {}
        # Determine CFM and RR's qualifying next-gen WB products from moves
        _en_cfm_wb_move = _en_move_a  # CFM's move (a-player)
        _en_rr_wb_move  = _en_move_c  # RR's move (c-player)
        _cfm_wb_next = ("Upgrade GenX9" if "GenX9" in _en_cfm_wb_move else
                        "Invest GenX"   if "Invest GenX" in _en_cfm_wb_move else
                        "Milk (no qualifying next-gen)")
        _rr_wb_next  = ("Ultrafan WB" if "Ultrafan WB" in _en_rr_wb_move else
                        "Milk Trent (no qualifying next-gen)")

        if _eng_wb_b_reengines and _eng_wb_a_reengines and \
           _eng_wb_787_eis == _eng_wb_a350_eis:
            _eng_wb_drivers[_eng_wb_787_eis] = (
                f"787 + A350 re-engined EIS\n"
                f"787: GenX/Trent 1000 → CFM {_cfm_wb_next} / RR {_rr_wb_next}\n"
                f"A350: Trent XWB → RR {_rr_wb_next}")
        else:
            if _eng_wb_b_reengines:
                _eng_wb_drivers[_eng_wb_787_eis] = (
                    f"787 EIS — re-engine\n"
                    f"GenX/Trent 1000 → CFM {_cfm_wb_next} / RR {_rr_wb_next}")
            if _eng_wb_a_reengines:
                _eng_wb_drivers[_eng_wb_a350_eis] = (
                    f"A350 EIS — re-engine\n"
                    f"Trent XWB → RR {_rr_wb_next}")

        # Build plotly figure — 2 lines (CFM, RR) over 2026-2056
        _eng_wb_fig = go.Figure()
        _eng_wb_fig.add_trace(go.Scatter(
            x=list(_CHT_YEARS), y=_eng_wb_cfm_sh, mode='lines+markers',
            name='CFM/GE', line=dict(color='#2ca02c', width=3),
            marker=dict(size=5),
            hovertemplate='%{x}: %{y:.1f}%<extra>CFM/GE</extra>'))
        _eng_wb_fig.add_trace(go.Scatter(
            x=list(_CHT_YEARS), y=_eng_wb_rr_sh, mode='lines+markers',
            name='RR', line=dict(color='#9467bd', width=3),
            marker=dict(size=5),
            hovertemplate='%{x}: %{y:.1f}%<extra>RR</extra>'))

        # Annotations + dotted vertical lines at trigger years
        _eng_wb_label_high = 92
        _eng_wb_label_low  = 8
        _eng_wb_alt = True
        for _yr_lbl in sorted(_eng_wb_drivers.keys()):
            if _yr_lbl < 2026 or _yr_lbl > 2056:
                continue
            _label = _eng_wb_drivers[_yr_lbl]
            _eng_wb_fig.add_vline(x=_yr_lbl, line_dash='dot',
                                  line_color='rgba(200,200,200,0.65)',
                                  line_width=1.2)
            _y_pos = _eng_wb_label_high if _eng_wb_alt else _eng_wb_label_low
            _eng_wb_alt = not _eng_wb_alt
            _eng_wb_fig.add_annotation(
                x=_yr_lbl, y=_y_pos,
                text=f"<b>{_yr_lbl}</b><br>{_label.replace(chr(10), '<br>')}",
                showarrow=False, font=dict(size=11, color='#222'),
                align='left', bgcolor='rgba(255,255,255,0.93)',
                bordercolor='rgba(180,180,180,0.7)', borderwidth=1,
                borderpad=4, xanchor='left', xshift=2)

        _eng_wb_fig.update_layout(
            title=dict(text='WB Engine Maker Share Trajectory — with Driver Annotations',
                       font=dict(size=14, color='#eee')),
            xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                       title_font=dict(color='#eee'),
                       tickfont=dict(color='#ddd'),
                       gridcolor='rgba(255,255,255,0.08)',
                       zerolinecolor='rgba(255,255,255,0.15)'),
            yaxis=dict(title='WB engine share (%)', range=[0, 100], dtick=10,
                       title_font=dict(color='#eee'),
                       tickfont=dict(color='#ddd'),
                       gridcolor='rgba(255,255,255,0.08)',
                       zerolinecolor='rgba(255,255,255,0.15)'),
            height=460, margin=dict(l=50, r=20, t=50, b=40),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02,
                        xanchor='right', x=1,
                        font=dict(color='#eee'),
                        bgcolor='rgba(0,0,0,0)'),
            plot_bgcolor='#000',
            paper_bgcolor='#000'
        )
        st.plotly_chart(_eng_wb_fig, use_container_width=True)
        st.caption(
            "WB engine maker share % per year (CFM/GE + RR sum to 100%; "
            "PW has no WB engines so is omitted). Pre-EIS structure: "
            "787 uses CFM GenX (70%) + RR Trent 1000 (30%); A350 uses "
            "RR Trent XWB (sole-source). Post-EIS: shares depend on each "
            "airframer's re-engine choice AND each engine maker's "
            "qualifying next-gen product. Vertical dotted lines mark "
            "787 EIS / A350 EIS trigger years (only shown when the "
            "airframer actually re-engines). If an engine maker lacks a "
            "qualifying next-gen product when the airframer re-engines, "
            "those deliveries vanish — visible as a depressed line "
            "(model gap)."
        )

    # ============================================================
    # SECTION D — FULL GAME-STATE SNAPSHOT
    # Plain-text export of the entire game state for further analysis.
    # ============================================================
    st.markdown("<div class='sum-section'>📋 FULL GAME-STATE SNAPSHOT</div>",
                unsafe_allow_html=True)
    st.caption("Plain-text snapshot of every assumption and every equilibrium "
               "currently loaded. Select all and copy for further analysis.")

    # Read the new RR NB+WB strain value (with fallback default)
    rr_nbwb_strain_val = float(ss.get("en_rr_nbwb_strain", 5.0))

    # Read additional global controls
    af_eps   = float(ss.get("af_eps_tol",  2.0))
    af_alpha = float(ss.get("af_alpha",    0.3))
    en_eps   = float(ss.get("en_eps_tol",  5.0))
    en_gross = float(ss.get("en_gross_mult", 1.6))
    en_lobby = float(ss.get("en_lobby_cost", 1.0))
    en_strain_general = float(ss.get("en_strain_cost", 2.0))
    af_milker = float(ss.get("af_nb_milker", 30.0))
    af_wb_milker_v = float(ss.get("af_wb_milker", 15.0))
    af_sab_sh = float(ss.get("af_sab_share", 5.0))
    af_sab_co = float(ss.get("af_sab_cost", 1.0))
    af_str_a  = float(ss.get("af_strain_a", 5.94))
    af_str_b  = float(ss.get("af_strain_b", 5.94))
    af_naked  = float(ss.get("af_naked_fine", 48.32))
    af_fps_7yr_adv = float(ss.get("af_fps_7yr_adv", 7.0))

    # Plain-text strategy decoders (no HTML / color classes)
    def _af_decode_text(a_strat, b_strat):
        d = af_decode(a_strat, b_strat)
        return {p: {"NB": d[p]["NB"], "WB": d[p]["WB"]} for p in d}

    def _en_decode_text(a_str, c_str, pw_locked):
        d = en_decode(a_str, c_str, pw_locked)
        return {p: {"NB": d[p]["NB"], "WB": d[p]["WB"]} for p in d}

    # Build the summary text block
    lines = []
    lines.append("=" * 70)
    lines.append("AEROSPACE GAME-THEORY DASHBOARD — FULL STATE SNAPSHOT")
    lines.append("=" * 70)
    lines.append("")
    lines.append("CONTEXT")
    lines.append("-------")
    lines.append("This is a coupled non-cooperative game over the post-2037")
    lines.append("narrowbody (NB) and widebody (WB) commercial-aircraft markets.")
    lines.append("Two airframers (Airbus, Boeing) and three engine makers")
    lines.append("(CFM/GE, Pratt & Whitney, Rolls-Royce) make simultaneous")
    lines.append("strategy choices. Payoffs are EV-normalised yields (100% = no")
    lines.append("change vs status quo). Equilibria are computed as Pure Nash")
    lines.append("(no unilateral improvement) and Near-Nash (within an ε-band).")
    lines.append("")

    # ── Critical user selections ──
    lines.append("1. ENGINE SUPPLIER SELECTION")
    lines.append("-" * 30)
    lines.append(f"  Boeing fps supplier      : {b_sup}")
    lines.append(f"  Airbus NGSA supplier     : {a_sup}")
    lines.append(f"  Selection code           : ({b_code}, {a_code})")
    lines.append(f"  Engines in play          : {', '.join(sorted(_all_engines))}")
    lines.append("")

    lines.append("2. POST-2037 NB MARKET SHARE (when both airframers launch)")
    lines.append("-" * 30)
    lines.append(f"  Boeing fps               : {boeing_share}%")
    lines.append(f"  Airbus NGSA              : {airbus_share}%")
    lines.append(f"  Derived NB engine share  : CFM {cfm_pct:.0f}% | "
                 f"PW {pw_pct:.0f}% | RR {rr_pct:.0f}%")
    lines.append("")

    lines.append("3. ENGINE-PLAYER POSTURES (DERIVED FROM SUPPLIER MATRIX)")
    lines.append("-" * 30)
    lines.append(f"  PW locked move           : {pw_lock}")
    lines.append(f"  PW lock rationale        : {pw_why}")
    lines.append(f"  RR posture               : {rr_posture}")
    lines.append("")

    # ── Aircraft prices ──
    lines.append("4. AIRCRAFT PRICES ($M PER AIRCRAFT)")
    lines.append("-" * 30)
    lines.append(f"  737 MAX                  : ${p_737:.0f}M")
    lines.append(f"  A320neo                  : ${p_a320:.0f}M")
    lines.append(f"  Boeing fps (next-gen NB) : ${p_fps:.0f}M")
    lines.append(f"  Airbus NGSA (next-gen NB): ${p_ngsa:.0f}M")
    lines.append(f"  Widebody (787 / A350)    : ${p_wb:.0f}M")
    lines.append("")

    # ── Operational margins ──
    lines.append("5. OPERATIONAL MARGINS (%)")
    lines.append("-" * 30)
    lines.append(f"  Airbus A320neo                                : {m_a320:.2f}%")
    lines.append(f"  Airbus NGSA                                   : {m_ngsa:.2f}%")
    lines.append(f"  Airbus A350 (WB) — status quo                 : {m_a350:.2f}%")
    lines.append(f"  Airbus A350 (WB) NO 787 re-engine (post-EIS)  : {m_a350_alone:.2f}%")
    lines.append(f"  Airbus A350 (WB) WITH 787 re-engine (post-EIS): {m_a350_both:.2f}%")
    lines.append(f"  Boeing 737                                    : {m_737:.2f}%")
    lines.append(f"  Boeing fps                                    : {m_fps:.2f}%")
    lines.append(f"  Boeing 787 (WB) — status quo                  : {m_787:.2f}%")
    lines.append(f"  Boeing 787 (WB) NO A350 re-engine (post-EIS)  : {m_787_alone:.2f}%")
    lines.append(f"  Boeing 787 (WB) WITH A350 re-engine (post-EIS): {m_787_both:.2f}%")
    lines.append("")

    # ── Airframer non-recurring spend ──
    lines.append("6. AIRFRAMER NON-RECURRING SPEND ($B, CAPEX + NRE)")
    lines.append("-" * 30)
    lines.append(f"  fps 7yr Solo             : ${cx_fps7:.2f}B")
    lines.append(f"  fps 10yr Solo            : ${cx_fps10:.2f}B")
    lines.append(f"  fps via Embraer          : ${cx_fpsemb:.2f}B")
    lines.append(f"  NGSA Build               : ${cx_ngsa:.2f}B")
    lines.append(f"  Boeing 787 Re-engine     : ${cx_787re:.2f}B")
    lines.append(f"  Airbus A350 Re-engine    : ${cx_a350re:.2f}B")
    lines.append(f"  Boeing 737 Rate Hike     : ${cx_737rate:.2f}B (nominal at 2032 fixed-calendar)")
    lines.append(f"  fps EIS year             : {int(ss.get('af_fps_eis',  2037))}")
    lines.append(f"  NGSA EIS year            : {int(ss.get('af_ngsa_eis', 2037))}")
    lines.append(f"  787 Re-engine EIS year   : {int(ss.get('af_787_eis',  2041))}")
    lines.append(f"  A350 Re-engine EIS year  : {int(ss.get('af_a350_eis', 2035))}")
    lines.append("")

    # ── Engine balance sheets + R&D ──
    lines.append("7. ENGINE-MAKER BALANCE SHEETS ($B)")
    lines.append("-" * 30)
    lines.append(f"  CFM/GE                   : EV ${ev_a:.0f}B / Debt ${debt_a:.0f}B")
    lines.append(f"  PW                       : EV ${ev_b:.0f}B / Debt ${debt_b:.0f}B")
    lines.append(f"  RR                       : EV ${ev_c:.0f}B / Debt ${debt_c:.0f}B")
    lines.append("")

    lines.append("8. ENGINE R&D ($B) — all conditional on actual program launch")
    lines.append("-" * 30)
    lines.append(f"  CFM Open Fan R&D (only on Open Fan / Open + Ducted) : ${rd_cfm_open_fan:.1f}B")
    lines.append(f"  CFM Ducted Fan R&D (only on Ducted / Open + Ducted) : ${rd_cfm_ducted:.1f}B")
    lines.append(f"  PW GTF2 Solo R&D (only when PW locked to Solo)      : ${rd_pw_solo:.1f}B")
    lines.append(f"  PW GTF2 JV R&D (only when PW locked to JV with RR)  : ${rd_pw_jv:.1f}B")
    lines.append(f"  RR Ultrafan R&D — NB (only if RR launches NB)       : ${rd_rr_nb:.1f}B")
    lines.append(f"  RR Ultrafan R&D — WB (only if RR launches WB)       : ${rd_rr_wb:.1f}B")
    lines.append(f"  RR T1000 Upgrade R&D (only if RR plays T1000)       : ${rd_rr_t1000:.1f}B")
    lines.append("")

    # ── Strain, fines, and other airframer-game costs ──
    lines.append("9. STRAIN, FINES & OTHER COSTS")
    lines.append("-" * 30)
    lines.append(f"  Airbus Two-Front Strain  : ${af_str_a:.2f}B")
    lines.append(f"  Boeing Two-Front Strain  : ${af_str_b:.2f}B")
    lines.append(f"  Naked Espionage Fine     : ${af_naked:.2f}B")
    lines.append(f"  NB Obsolescence (milker) : {af_milker:.1f}%")
    lines.append(f"  WB Obsolescence (milker) : {af_wb_milker_v:.1f}%")
    lines.append(f"  WB lone-refresh capture  : 787 +{float(st.session_state.get('af_wb_b_pp', 3.0)):.1f}pp/yr (cap {100.0 - af_wb_milker_v:.1f}%) | A350 +{float(st.session_state.get('af_wb_a_pp', 4.0)):.1f}pp/yr (cap 60%)")
    lines.append(f"  Sabotage Share Shift     : {af_sab_sh:.1f}% (FLAT, 5 yrs from fps EIS)")
    lines.append(f"  Sabotage Op Cost / Move  : ${af_sab_co:.2f}B")
    lines.append(f"  Generic engine strain    : ${en_strain_general:.2f}B")
    lines.append(f"  RR NB+WB concurrent strn : ${rr_nbwb_strain_val:.2f}B "
                 f"(triggers when RR has both NB and WB project)")
    lines.append(f"  CFM Lobby Cost (Move 5)  : ${en_lobby:.2f}B")
    lines.append(f"  fps 7yr ramp NB share +  : {af_fps_7yr_adv:.1f}pp "
                 f"(first-mover bonus over 10yr / Embraer)")
    _r7b  = float(ss.get('af_ramp7_b_pp',  4.0)); _r7a  = float(ss.get('af_ramp7_a_pp',  4.0))
    _r10b = float(ss.get('af_ramp10_b_pp', 4.0)); _r10a = float(ss.get('af_ramp10_a_pp', 4.0))
    lines.append(f"  fps capture speed        : 7yr {_r7b:.1f}pp/yr | 10yr/Embraer {_r10b:.1f}pp/yr")
    lines.append(f"  NGSA Phase-2 recovery    : vs 7yr {_r7a:.1f}pp/yr | vs 10yr {_r10a:.1f}pp/yr "
                 f"(NGSA Phase-1 capture fixed at +3pp/yr)")
    lines.append("")

    # ── Game-theory parameters ──
    lines.append("10. GAME-THEORY PARAMETERS")
    lines.append("-" * 30)
    lines.append(f"  Airframer ε-Nash tol     : {af_eps:.2f}%")
    lines.append(f"  Engine ε-Nash tol        : {en_eps:.2f}%")
    lines.append(f"  True Cost Penalty α      : {af_alpha:.2f}")
    lines.append(f"  Engine Gross Multiplier  : {en_gross:.2f}x")
    _nb_eis_min = min(int(ss.get('af_fps_eis', 2037)), int(ss.get('af_ngsa_eis', 2037)))
    _wb_eis_min = min(int(ss.get('af_787_eis', 2041)), int(ss.get('af_a350_eis', 2035)))
    lines.append(f"  Engine timeline (synced) : 2026-2056 (T=31 yrs; NB EIS {_nb_eis_min} = min(fps, NGSA), WB EIS {_wb_eis_min} = min(787, A350))")
    lines.append("")

    # ── Airframer equilibria ──
    lines.append("=" * 70)
    lines.append("AIRFRAMER GAME — EQUILIBRIA")
    lines.append("=" * 70)
    af_nash_n      = ss.get("_af_nash_count", None)
    af_near_n      = ss.get("_af_near_nash_count", None)
    af_nash_pairs  = ss.get("_af_nash_pairs",  [])
    af_near_pairs  = ss.get("_af_near_nash_pairs", [])
    if af_nash_n is None and af_near_n is None:
        lines.append("(Not yet computed — visit the Airframer tab to populate.)")
    else:
        lines.append(f"Pure Nash count     : {af_nash_n}")
        lines.append(f"Near-Nash count (ε) : {af_near_n}")
        lines.append("")
        if af_nash_pairs:
            lines.append("PURE NASH EQUILIBRIA")
            lines.append("-" * 30)
            for i, (a_strat, b_strat, ya, yb) in enumerate(af_nash_pairs):
                d = _af_decode_text(a_strat, b_strat)
                lines.append(f"  Pure Nash #{i+1}  "
                             f"(Airbus {ya:.0f}% | Boeing {yb:.0f}%)")
                lines.append(f"    Airbus  NB: {d['Airbus']['NB']}")
                lines.append(f"    Airbus  WB: {d['Airbus']['WB']}")
                lines.append(f"    Boeing  NB: {d['Boeing']['NB']}")
                lines.append(f"    Boeing  WB: {d['Boeing']['WB']}")
            lines.append("")
        else:
            lines.append("PURE NASH: none at current parameters.")
            lines.append("")
        if af_near_pairs:
            lines.append("NEAR-NASH EQUILIBRIA (within ε)")
            lines.append("-" * 30)
            for i, (a_strat, b_strat, ya, yb) in enumerate(af_near_pairs):
                d = _af_decode_text(a_strat, b_strat)
                lines.append(f"  Near-Nash #{i+1}  "
                             f"(Airbus {ya:.0f}% | Boeing {yb:.0f}%)")
                lines.append(f"    Airbus  NB: {d['Airbus']['NB']}")
                lines.append(f"    Airbus  WB: {d['Airbus']['WB']}")
                lines.append(f"    Boeing  NB: {d['Boeing']['NB']}")
                lines.append(f"    Boeing  WB: {d['Boeing']['WB']}")
            lines.append("")
        else:
            lines.append("NEAR-NASH: none at current parameters.")
            lines.append("")

    # ── Engine equilibria ──
    lines.append("=" * 70)
    lines.append("ENGINE GAME — EQUILIBRIA")
    lines.append("=" * 70)
    en_nash_n      = ss.get("_en_nash_count", None)
    en_near_n      = ss.get("_en_near_nash_count", None)
    en_nash_pairs  = ss.get("_en_nash_pairs",  [])
    en_near_pairs  = ss.get("_en_near_nash_pairs", [])
    pw_locked_move = ss.get("_en_pw_locked_move", "1-Milk GTF")
    if en_nash_n is None and en_near_n is None:
        lines.append("(Not yet computed — visit the Engine tab to populate.)")
    else:
        lines.append(f"Pure Nash count     : {en_nash_n}")
        lines.append(f"Near-Nash count (ε) : {en_near_n}")
        lines.append(f"PW locked move      : {pw_locked_move}")
        lines.append("")
        if en_nash_pairs:
            lines.append("PURE NASH EQUILIBRIA")
            lines.append("-" * 30)
            for i, (a_str, c_str, ya, yc) in enumerate(en_nash_pairs):
                d = _en_decode_text(a_str, c_str, pw_locked_move)
                lines.append(f"  Pure Nash #{i+1}  "
                             f"(CFM {ya:.0f}% | RR {yc:.0f}%)")
                lines.append(f"    CFM/GE  NB: {d['CFM/GE']['NB']}")
                lines.append(f"    CFM/GE  WB: {d['CFM/GE']['WB']}")
                lines.append(f"    PW      NB: {d['PW']['NB']}")
                lines.append(f"    PW      WB: {d['PW']['WB']}")
                lines.append(f"    RR      NB: {d['RR']['NB']}")
                lines.append(f"    RR      WB: {d['RR']['WB']}")
            lines.append("")
        else:
            lines.append("PURE NASH: none at current parameters.")
            lines.append("")
        if en_near_pairs:
            lines.append("NEAR-NASH EQUILIBRIA (within ε)")
            lines.append("-" * 30)
            for i, (a_str, c_str, ya, yc) in enumerate(en_near_pairs):
                d = _en_decode_text(a_str, c_str, pw_locked_move)
                lines.append(f"  Near-Nash #{i+1}  "
                             f"(CFM {ya:.0f}% | RR {yc:.0f}%)")
                lines.append(f"    CFM/GE  NB: {d['CFM/GE']['NB']}")
                lines.append(f"    CFM/GE  WB: {d['CFM/GE']['WB']}")
                lines.append(f"    PW      NB: {d['PW']['NB']}")
                lines.append(f"    PW      WB: {d['PW']['WB']}")
                lines.append(f"    RR      NB: {d['RR']['NB']}")
                lines.append(f"    RR      WB: {d['RR']['WB']}")
            lines.append("")
        else:
            lines.append("NEAR-NASH: none at current parameters.")
            lines.append("")

    lines.append("=" * 70)
    lines.append("END OF SNAPSHOT")
    lines.append("=" * 70)

    ai_text = "\n".join(lines)

    # Render the text in a copyable text area. We deliberately omit a `key=`
    # so Streamlit treats the `value=` argument as authoritative on every
    # rerun — the text always reflects the current game state. (If we had
    # a key, session_state would lock the old text and stale-out on edits.)
    st.text_area(
        "Game state (plain text — select all and copy for further analysis):",
        value=ai_text,
        height=420,
        help="Contains every assumption currently loaded plus every Pure Nash "
             "and Near-Nash equilibrium with full per-player NB and WB "
             "strategy decoding.",
    )

    # Footnote
    st.markdown(
        "<div style='font-family:monospace;font-size:11px;color:#666;"
        "padding:10px 14px;border-left:3px solid #30363d;background:#0a0a0a;"
        "border-radius:0 4px 4px 0;'>"
        "All values reflect the current state of the Airframer and Engine sidebars. "
        "Equilibrium results recompute on each visit to those tabs. "
        "If sidebar parameters changed since the last visit, re-open the relevant "
        "board to refresh."
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD TAB — consolidated view of the airframer-game charts.
# Leverages the SAME chart functions as the Summary tab so the
# math + visuals are identical. NB / WB / cash-flow share the
# state picker; tornado has its own player picker.
# ============================================================
def run_oem_dashboard_tab():
    import plotly.graph_objects as go
    st.markdown("## 📊 Game Dashboard")

    # ─── Toggle: Airframer vs Engine board ───
    _board = st.radio(
        "Game board",
        ["✈️ Airframer Game (Boeing vs Airbus)", "🔧 Engine Game (CFM vs PW vs RR)"],
        horizontal=True,
        key="_dash_board_toggle",
    )
    _is_engine = _board.startswith("🔧")

    if not _is_engine:
        _run_dashboard_airframer()
    else:
        _run_dashboard_engine()


def _run_dashboard_airframer():
    import plotly.graph_objects as go
    _pure = st.session_state.get("_af_nash_pairs", [])
    _near = st.session_state.get("_af_near_nash_pairs", [])

    if not _pure and not _near:
        st.info("No airframer equilibria computed yet. Visit the **✈️ Airframer Duopoly** tab first to populate this dashboard.")
        return

    # ── State picker (shared by NB / WB / cash-flow charts) ──
    def _clean(m): return m.replace('Re_engine', 'Re-engine').replace('_', ' ')
    def _fmt_b(b_strat):
        b_nb, b_rate, b_wb = b_strat
        parts = [_clean(b_nb)]
        if "Increase" in b_rate:
            parts.append(_clean(b_rate))
        parts.append(_clean(b_wb))
        return " + ".join(parts)
    def _fmt_a(a_strat):
        a_nb, a_btl, a_poach, a_wb = a_strat
        parts = [_clean(a_nb)]
        if "Sabotage" in a_btl and "No" not in a_btl:
            parts.append(_clean(a_btl))
        if "Sabotage" in a_poach and "No" not in a_poach:
            parts.append(_clean(a_poach))
        parts.append(_clean(a_wb))
        return " + ".join(parts)

    _options = []
    for i, (a_strat, b_strat, ya, yb) in enumerate(_pure, start=1):
        _options.append((f"★ Pure Nash #{i}  |  B: {_fmt_b(b_strat)}  |  A: {_fmt_a(a_strat)}", a_strat, b_strat))
    for i, (a_strat, b_strat, ya, yb) in enumerate(_near, start=1):
        _options.append((f"Near-Nash #{i}  |  B: {_fmt_b(b_strat)}  |  A: {_fmt_a(a_strat)}", a_strat, b_strat))
    _labels = [o[0] for o in _options]

    # Clear stale state-picker value from earlier format runs.
    if '_dash_state_pick' in st.session_state and st.session_state['_dash_state_pick'] not in _labels:
        del st.session_state['_dash_state_pick']

    st.markdown("### Equilibrium state (applies to charts 1–3)")
    _pick = st.selectbox(
        "Pick state", options=_labels, index=0,
        key="_dash_state_pick", label_visibility="collapsed",
    )
    _idx = _labels.index(_pick)
    _a_strat, _b_strat = _options[_idx][1], _options[_idx][2]

    _row1_c1, _row1_c2 = st.columns(2)
    with _row1_c1:
        st.markdown("**1️⃣ NB Market Share**")
        _render_nb_share_trajectory_block(_a_strat, _b_strat)
    with _row1_c2:
        st.markdown("**2️⃣ WB Market Share**")
        _render_wb_share_trajectory_block(_a_strat, _b_strat)

    _row2_c1, _row2_c2 = st.columns(2)
    with _row2_c1:
        st.markdown("**3️⃣ Player Cash Flow**")
        _render_player_cash_flow_block(_a_strat, _b_strat)
    with _row2_c2:
        st.markdown("**4️⃣ Launch Sensitivity Tornado**")
        _player = st.selectbox(
            "Tornado player", options=["Boeing", "Airbus"], index=0,
            key="_dash_tornado_player",
        )
        if _player == "Boeing":
            _rows  = st.session_state.get('_af_b_tornado_rows', [])
            _base  = st.session_state.get('_af_b_base_y', None)
            _bench = st.session_state.get('_af_b_bench_y', None)
        else:
            _rows  = st.session_state.get('_af_a_tornado_rows', [])
            _base  = st.session_state.get('_af_a_base_y', None)
            _bench = st.session_state.get('_af_a_bench_y', None)

        if not _rows:
            st.info("Tornado data not yet computed. Open the **✈️ Airframer Duopoly** tab first.")
        else:
            _render_dashboard_tornado_chart(_rows, _base, _bench, _player)


def _run_dashboard_engine():
    """Engine-side dashboard: 4 charts mirroring the airframer dashboard."""
    import plotly.graph_objects as go
    _pure = st.session_state.get("_en_nash_pairs", [])
    _near = st.session_state.get("_en_near_nash_pairs", [])
    _pw_locked = st.session_state.get("_en_pw_locked_move", "2-Launch GTF2 Go Solo")

    if not _pure and not _near:
        st.info("No engine equilibria computed yet. Visit the **🔧 Engine 3-Player** tab first to populate this dashboard.")
        return

    # ── Engine state picker — labels show moves ──
    _options = []
    for i, (mv_a, mv_c, ya, yc) in enumerate(_pure, start=1):
        _options.append((f"★ Pure Nash #{i}  |  CFM: {mv_a}  |  RR: {mv_c}", mv_a, _pw_locked, mv_c))
    for i, (mv_a, mv_c, ya, yc) in enumerate(_near, start=1):
        _options.append((f"Near-Nash #{i}  |  CFM: {mv_a}  |  RR: {mv_c}", mv_a, _pw_locked, mv_c))
    _labels = [o[0] for o in _options]

    if '_dash_en_state_pick' in st.session_state and st.session_state['_dash_en_state_pick'] not in _labels:
        del st.session_state['_dash_en_state_pick']

    st.markdown(f"### Engine equilibrium state (PW locked to: **{_pw_locked}**)")
    _pick = st.selectbox(
        "Pick engine state", options=_labels, index=0,
        key="_dash_en_state_pick", label_visibility="collapsed",
    )
    _idx = _labels.index(_pick)
    _move_a = _options[_idx][1]
    _move_b = _options[_idx][2]
    _move_c = _options[_idx][3]

    # ── Compute post-EIS shares by applying moves ──
    _shares = _en_dash_apply_moves(_move_a, _move_b, _move_c)

    # ── 2×2 grid layout ──
    _row1_c1, _row1_c2 = st.columns(2)
    with _row1_c1:
        st.markdown("**1️⃣ NB Engine Maker Share**")
        _render_engine_nb_share_chart(_shares)
    with _row1_c2:
        st.markdown("**2️⃣ WB Engine Maker Share**")
        _render_engine_wb_share_chart(_shares)

    _row2_c1, _row2_c2 = st.columns(2)
    with _row2_c1:
        st.markdown("**3️⃣ Engine Player Cash Flow**")
        _render_engine_cash_flow_chart(_shares, _move_a, _move_b, _move_c)
    with _row2_c2:
        st.markdown("**4️⃣ Launch Sensitivity Tornado**")
        _player = st.selectbox(
            "Tornado player", options=["CFM/GE", "PW", "RR"], index=0,
            key="_dash_en_tornado_player",
        )
        if _player == "CFM/GE":
            _rows  = st.session_state.get('_en_cfm_tornado_rows', [])
            _base  = st.session_state.get('_en_cfm_base_y', None)
            _bench = st.session_state.get('_en_cfm_bench_y', None)
        elif _player == "PW":
            _rows  = st.session_state.get('_en_pw_tornado_rows', [])
            _base  = st.session_state.get('_en_pw_base_y', None)
            _bench = st.session_state.get('_en_pw_bench_y', None)
        else:
            _rows  = st.session_state.get('_en_rr_tornado_rows', [])
            _base  = st.session_state.get('_en_rr_base_y', None)
            _bench = st.session_state.get('_en_rr_bench_y', None)

        if not _rows:
            st.info("Tornado data not yet computed. Open the **📋 Game Summary** tab to refresh.")
        else:
            _render_dashboard_tornado_chart(_rows, _base, _bench, _player)


def _render_dashboard_tornado_chart(rows, base, bench, player_label):
    """Common tornado chart renderer for the dashboard tab."""
    import plotly.graph_objects as go
    _rows_sorted = sorted(rows, key=lambda r: abs(r['hi'] - r['lo']))
    # Two-line y-axis labels: variable name on top, swept range below in a
    # smaller dimmer font. Plotly tick labels support HTML.
    _names = [
        f"{r['name']}<br><span style='font-size:9px;color:#888'>"
        f"{r['lo_lbl']} ↔ {r['hi_lbl']}  (base {r['base_lbl']})</span>"
        for r in _rows_sorted
    ]
    _lo_vals = [r['lo']   for r in _rows_sorted]
    _hi_vals = [r['hi']   for r in _rows_sorted]
    _hover   = [f"low {r['lo_lbl']}: {r['lo']:+.1f}pp<br>high {r['hi_lbl']}: {r['hi']:+.1f}pp<br>base {r['base_lbl']}"
                for r in _rows_sorted]
    _fig = go.Figure()
    _fig.add_trace(go.Bar(
        y=_names, x=_lo_vals, orientation='h',
        marker=dict(color='#d29922', line=dict(color='#b07a16', width=1)),
        name='Low → yield Δ', hovertext=_hover, hoverinfo='text', base=0,
    ))
    _fig.add_trace(go.Bar(
        y=_names, x=_hi_vals, orientation='h',
        marker=dict(color='#2f81f7', line=dict(color='#1f6feb', width=1)),
        name='High → yield Δ', hovertext=_hover, hoverinfo='text', base=0,
    ))
    if bench is not None and base is not None:
        _bench_pp = bench - base
        _fig.add_vline(x=_bench_pp, line_dash='dash', line_color='#d29922', line_width=2,
                       annotation_text=f"Do Nothing: {_bench_pp:+.1f}pp",
                       annotation_position='top right',
                       annotation_font_color='#d29922')
    _fig.add_vline(x=0, line_color='#58a6ff', line_width=2)
    _fig.update_layout(
        title=f'{player_label} Tornado — yield sensitivity (pp)',
        height=520, margin=dict(l=200, r=20, t=50, b=40),
        paper_bgcolor='#0d1117', plot_bgcolor='#000',
        font=dict(color='#ddd', size=10),
        barmode='overlay', bargap=0.35,
        xaxis=dict(title='Yield Δ vs base (pp)',
                   gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.15)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', automargin=True),
        showlegend=False,
    )
    st.plotly_chart(_fig, use_container_width=True)
    if base is not None:
        st.caption(f"Base yield ({player_label}): **{base:.1f}%** · "
                   f"Do Nothing benchmark: **{bench:.1f}%** · "
                   f"bars show yield delta (pp) when each factor sweeps low→high.")


def _en_dash_apply_moves(move_a, move_b, move_c):
    """Apply engine moves to starting shares; return a dict with all the
    shares, R&D charges, strain, EIS years, and other constants the engine
    dashboard charts need. Mirrors the engine simulator's logic exactly."""
    import numpy as np
    # Constants
    _CPI = 0.022; _ENG_PER_AC = 2
    _NB_AC = 2000; _WB_AC = 170
    _NB_THRUST = 30000; _WB_THRUST = 80000
    _thrust = np.array([8729, 9220, 12670, 13360, 13630, 18900, 23000, 14200, 20000, 25000], dtype=float)
    _shipset = np.array([4.7, 4.7, 5.0, 5.5, 5.5, 6.0, 7.1, 5.2, 7.0, 5.9], dtype=float) / 2.0
    _slope, _icpt = np.polyfit(_thrust, _shipset, 1)
    _NB_PRICE_M = float(_slope * _NB_THRUST + _icpt)
    _WB_PRICE_M = float(_WB_THRUST * 140 / 1_000_000)
    _GM = float(st.session_state.get('en_gross_mult', 1.6))

    # WACCs and EVs
    _wacc_a = float(st.session_state.get('en_wacc_a', 8.5)) / 100.0
    _wacc_b = float(st.session_state.get('en_wacc_b', 10.0)) / 100.0
    _wacc_c = float(st.session_state.get('en_wacc_c', 10.0)) / 100.0
    _ev_a   = float(st.session_state.get('en_ev_a', 160.0))
    _ev_b   = float(st.session_state.get('en_ev_b', 110.0))
    _ev_c   = float(st.session_state.get('en_ev_c', 110.0))

    # R&D
    _rd_cfm_of  = float(st.session_state.get('en_rd_cfm_open_fan', 8.0))
    _rd_cfm_duc = float(st.session_state.get('en_rd_cfm_ducted', 4.0))
    _rd_pw_solo = float(st.session_state.get('en_rd_pw_solo', 2.0))
    _rd_pw_jv   = float(st.session_state.get('en_rd_pw_jv', 2.0))
    _rd_rr_nb   = float(st.session_state.get('en_rd_rr_nb', 8.0))
    _rd_rr_wb   = float(st.session_state.get('en_rd_rr_wb', 4.0))
    _rd_rr_t1k  = float(st.session_state.get('en_rd_rr_t1000', 2.0))
    _lobby_cost = float(st.session_state.get('en_lobby_cost', 2.0))
    _strain     = float(st.session_state.get('en_strain_cost', 2.0))
    _rr_nbwb_strain = float(st.session_state.get('en_rr_nbwb_strain', 5.0))
    _of_loss    = float(st.session_state.get('en_openfan_loss', 35)) / 100.0
    _duc_gain   = float(st.session_state.get('en_ducted_gain', 10)) / 100.0

    # EIS years
    _fps  = int(st.session_state.get('af_fps_eis',  2037))
    _ngsa = int(st.session_state.get('af_ngsa_eis', 2037))
    _787  = int(st.session_state.get('af_787_eis',  2041))
    _a350 = int(st.session_state.get('af_a350_eis', 2035))
    _nb_eis_t = max(0, min(_fps, _ngsa) - 2026)
    _wb_eis_t = max(0, min(_787, _a350) - 2026)
    _nb_eis_yr = 2026 + _nb_eis_t
    _wb_eis_yr = 2026 + _wb_eis_t

    # Status-quo and starting shares (normalized)
    def _norm3(a, b, c):
        t = a + b + c
        return (a/t, b/t, c/t) if t > 0 else (0.0, 0.0, 0.0)
    _sq_cfm_nb = float(st.session_state.get('sq_cfm_nb', 76))
    _sq_pw_nb  = float(st.session_state.get('sq_pw_nb',  24))
    _sq_cfm_wb = float(st.session_state.get('sq_cfm_wb', 42))
    _sq_rr_wb  = float(st.session_state.get('sq_rr_wb',  58))
    sq_cfm_nb, sq_pw_nb, sq_rr_nb = _norm3(_sq_cfm_nb, _sq_pw_nb, 0.0)
    sq_cfm_wb, _, sq_rr_wb = _norm3(_sq_cfm_wb, 0.0, _sq_rr_wb)

    _fut_cfm_nb = float(st.session_state.get('f_cfm_nb', 53))
    _fut_pw_nb  = float(st.session_state.get('f_pw_nb',  50))
    _fut_rr_nb  = float(st.session_state.get('f_rr_nb',  50))
    _fut_cfm_wb = float(st.session_state.get('f_cfm_wb', 42))
    _fut_rr_wb  = float(st.session_state.get('f_rr_wb',  58))
    a_nb, b_nb, c_nb = _norm3(_fut_cfm_nb, _fut_pw_nb, _fut_rr_nb)
    a_wb, b_wb, c_wb = _norm3(_fut_cfm_wb, 0.0, _fut_rr_wb)

    # ── Apply moves (mirrors _en_simulate exactly) ──
    inv_a = inv_b = inv_c = 0.0
    str_a = str_b = str_c = 0.0
    jv_nb = False
    _has_open = ("1-Open Fan" in move_a) or ("3-Open + Ducted" in move_a)
    _has_duc  = ("2-Ducted" in move_a) or ("3-Open + Ducted" in move_a)
    _has_lobby = "5-Lobby Govts" in move_a
    _rr_nb_act = "Ultrafan NB" in move_c or "JV with PW" in move_c
    pa = 0
    if _has_open:
        pa += 1; inv_a += _rd_cfm_of
        _eff = min(_of_loss, 0.20) if _has_lobby else _of_loss
        a_nb -= _eff
        if _rr_nb_act: b_nb += _eff/2; c_nb += _eff/2
        else: b_nb += _eff
    if _has_duc:
        pa += 1; inv_a += _rd_cfm_duc
        a_nb += _duc_gain
        if _rr_nb_act: b_nb -= _duc_gain/2; c_nb -= _duc_gain/2
        else: b_nb -= _duc_gain
    if "3-Open + Ducted" in move_a: pa += 1
    if "4-Partner Embraer" in move_a: pa += 1; a_nb += 0.05
    if _has_lobby:    pa += 1; inv_a += _lobby_cost
    if "6-Upgrade GenX9" in move_a: pa += 1; a_wb += 0.05
    if "7-Invest GenX"   in move_a: pa += 1; a_wb += 0.05
    if pa >= 2: str_a += _strain

    pb = 0
    if "2-Launch GTF2" in move_b:
        pb += 1; inv_b += _rd_pw_solo
        b_nb += 0.10; a_nb -= 0.05; c_nb -= 0.05
    if "3-JV with RR" in move_b:
        pb += 1; jv_nb = True; inv_b += _rd_pw_jv
        a_nb -= 0.10; b_nb += 0.05; c_nb += 0.05
    if pb >= 2: str_b += _strain

    pc = 0; rr_nb = rr_wb = False
    if "1-Ultrafan WB" in move_c:
        pc += 1; rr_wb = True; inv_c += _rd_rr_wb
        c_wb += 0.10; a_wb -= 0.10
    if "2-Ultrafan NB" in move_c:
        pc += 1; rr_nb = True; inv_c += _rd_rr_nb
        c_nb += 0.15; a_nb -= 0.10; b_nb -= 0.05
    if "3-JV with PW" in move_c:
        pc += 1; rr_nb = True; jv_nb = True; inv_c += _rd_rr_nb / 2.0
        c_nb += 0.05; b_nb += 0.05; a_nb -= 0.10
    if "4-Upgrade T1000" in move_c:
        pc += 1; rr_wb = True; inv_c += _rd_rr_t1k
        c_wb += 0.05; a_wb -= 0.05
    if rr_nb and rr_wb: str_c += _rr_nbwb_strain

    # JV equalization, floor at 0, renormalize
    if jv_nb:
        avg = (b_nb + c_nb) / 2.0
        b_nb = avg; c_nb = avg
    a_nb, b_nb, c_nb = max(0, a_nb), max(0, b_nb), max(0, c_nb)
    a_wb, b_wb, c_wb = max(0, a_wb), max(0, b_wb), max(0, c_wb)
    _t = a_nb + b_nb + c_nb
    if _t > 0: a_nb /= _t; b_nb /= _t; c_nb /= _t
    _t = a_wb + b_wb + c_wb
    if _t > 0: a_wb /= _t; b_wb /= _t; c_wb /= _t

    return dict(
        # post-EIS shares
        post_cfm_nb=a_nb, post_pw_nb=b_nb, post_rr_nb=c_nb,
        post_cfm_wb=a_wb, post_pw_wb=b_wb, post_rr_wb=c_wb,
        # pre-EIS (status quo) shares
        sq_cfm_nb=sq_cfm_nb, sq_pw_nb=sq_pw_nb, sq_rr_nb=sq_rr_nb,
        sq_cfm_wb=sq_cfm_wb, sq_pw_wb=0.0, sq_rr_wb=sq_rr_wb,
        # EIS years (as year ints and t-offsets)
        nb_eis_yr=_nb_eis_yr, wb_eis_yr=_wb_eis_yr,
        nb_eis_t=_nb_eis_t, wb_eis_t=_wb_eis_t,
        # Costs
        inv_a=inv_a, inv_b=inv_b, inv_c=inv_c,
        str_a=str_a, str_b=str_b, str_c=str_c,
        # Economic constants
        nb_ac=_NB_AC, wb_ac=_WB_AC, eng_per_ac=_ENG_PER_AC,
        nb_price_m=_NB_PRICE_M, wb_price_m=_WB_PRICE_M,
        cpi=_CPI, gross_mult=_GM,
        wacc_a=_wacc_a, wacc_b=_wacc_b, wacc_c=_wacc_c,
        ev_a=_ev_a, ev_b=_ev_b, ev_c=_ev_c,
    )


def _render_engine_nb_share_chart(sh):
    """NB engine maker share trajectory chart."""
    import plotly.graph_objects as go
    _years = list(range(2026, 2057))
    _cfm_sh, _pw_sh, _rr_sh = [], [], []
    for _y in _years:
        _t = _y - 2026
        if _t < sh['nb_eis_t']:
            _cfm_sh.append(sh['sq_cfm_nb'] * 100)
            _pw_sh.append(sh['sq_pw_nb'] * 100)
            _rr_sh.append(sh['sq_rr_nb'] * 100)
        else:
            _cfm_sh.append(sh['post_cfm_nb'] * 100)
            _pw_sh.append(sh['post_pw_nb'] * 100)
            _rr_sh.append(sh['post_rr_nb'] * 100)
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_years, y=_cfm_sh, mode='lines+markers',
                              name='CFM/GE', line=dict(color='#2ca02c', width=2.5)))
    _fig.add_trace(go.Scatter(x=_years, y=_pw_sh, mode='lines+markers',
                              name='Pratt & Whitney', line=dict(color='#9467bd', width=2.5)))
    _fig.add_trace(go.Scatter(x=_years, y=_rr_sh, mode='lines+markers',
                              name='Rolls-Royce', line=dict(color='#d62728', width=2.5)))
    _fig.add_vline(x=sh['nb_eis_yr'], line_dash='dot', line_color='rgba(200,200,200,0.7)',
                   annotation_text=f"NB EIS {sh['nb_eis_yr']}",
                   annotation_position='top', annotation_font_color='#ccc')
    _fig.update_layout(
        title=dict(text='NB Engine Maker Share Trajectory', font=dict(size=14, color='#eee')),
        height=460, margin=dict(l=50, r=20, t=50, b=40),
        paper_bgcolor='#0d1117', plot_bgcolor='#000', font=dict(color='#ddd'),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                   gridcolor='rgba(255,255,255,0.08)'),
        yaxis=dict(title='NB engine share (%)', range=[0, 100], dtick=10,
                   gridcolor='rgba(255,255,255,0.08)'),
    )
    st.plotly_chart(_fig, use_container_width=True)
    st.caption(f"Pre-{sh['nb_eis_yr']}: status quo (CFM ~76%, PW ~24%, RR ~0%). "
               f"Post-EIS: shares shift per the selected engine moves. Lines sum to 100%.")


def _render_engine_wb_share_chart(sh):
    """WB engine maker share trajectory chart (CFM + RR, PW has no WB)."""
    import plotly.graph_objects as go
    _years = list(range(2026, 2057))
    _cfm_sh, _rr_sh = [], []
    for _y in _years:
        _t = _y - 2026
        if _t < sh['wb_eis_t']:
            _cfm_sh.append(sh['sq_cfm_wb'] * 100)
            _rr_sh.append(sh['sq_rr_wb'] * 100)
        else:
            _cfm_sh.append(sh['post_cfm_wb'] * 100)
            _rr_sh.append(sh['post_rr_wb'] * 100)
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_years, y=_cfm_sh, mode='lines+markers',
                              name='CFM/GE (GenX)', line=dict(color='#2ca02c', width=2.5)))
    _fig.add_trace(go.Scatter(x=_years, y=_rr_sh, mode='lines+markers',
                              name='Rolls-Royce (Trent / Ultrafan WB)',
                              line=dict(color='#d62728', width=2.5)))
    _fig.add_vline(x=sh['wb_eis_yr'], line_dash='dot', line_color='rgba(200,200,200,0.7)',
                   annotation_text=f"WB EIS {sh['wb_eis_yr']}",
                   annotation_position='top', annotation_font_color='#ccc')
    _fig.update_layout(
        title=dict(text='WB Engine Maker Share Trajectory', font=dict(size=14, color='#eee')),
        height=460, margin=dict(l=50, r=20, t=50, b=40),
        paper_bgcolor='#0d1117', plot_bgcolor='#000', font=dict(color='#ddd'),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(title='Year', dtick=2, range=[2025.5, 2057],
                   gridcolor='rgba(255,255,255,0.08)'),
        yaxis=dict(title='WB engine share (%)', range=[0, 100], dtick=10,
                   gridcolor='rgba(255,255,255,0.08)'),
    )
    st.plotly_chart(_fig, use_container_width=True)
    st.caption(f"Pre-{sh['wb_eis_yr']}: status quo (CFM ~42% via GenX, RR ~58% via Trent). "
               f"Post-EIS: shares shift per selected moves. PW has no WB platform.")


def _render_engine_cash_flow_chart(sh, move_a, move_b, move_c):
    """Engine cash flow chart per player. Implied from year-by-year revenue
    delta vs status-quo baseline, discounted to PV. Sum of all bars = the
    player's NPV in $B EV delta, mapping back to yield = 100 + (NPV/EV)*100."""
    import plotly.graph_objects as go
    _player = st.selectbox(
        "Pick engine player",
        options=["CFM/GE", "PW", "RR"], index=0,
        key="_dash_en_cf_player",
    )
    if _player == "CFM/GE":
        post_nb, post_wb = sh['post_cfm_nb'], sh['post_cfm_wb']
        sq_nb,   sq_wb   = sh['sq_cfm_nb'],   sh['sq_cfm_wb']
        wacc, ev = sh['wacc_a'], sh['ev_a']
        inv, strain = sh['inv_a'], sh['str_a']
        color = '#2ca02c'
    elif _player == "PW":
        post_nb, post_wb = sh['post_pw_nb'], sh['post_pw_wb']
        sq_nb,   sq_wb   = sh['sq_pw_nb'],   sh['sq_pw_wb']
        wacc, ev = sh['wacc_b'], sh['ev_b']
        inv, strain = sh['inv_b'], sh['str_b']
        color = '#9467bd'
    else:  # RR
        post_nb, post_wb = sh['post_rr_nb'], sh['post_rr_wb']
        sq_nb,   sq_wb   = sh['sq_rr_nb'],   sh['sq_rr_wb']
        wacc, ev = sh['wacc_c'], sh['ev_c']
        inv, strain = sh['inv_c'], sh['str_c']
        color = '#d62728'

    _years = list(range(2026, 2057))
    _NPV_WIN = 20   # post-EIS Phase A window

    _delta_nb = [0.0] * len(_years)   # nominal Δ cash flow per year (chart bars)
    _delta_wb = [0.0] * len(_years)
    _pv_delta_total = 0.0             # PV-discounted total (for implied yield)
    _nominal_delta_total = 0.0        # nominal sum (caption only)

    for i, yr in enumerate(_years):
        t = yr - 2026
        # NB cashflow within program window (eis_t .. eis_t+19)
        if t <= sh['nb_eis_t'] + _NPV_WIN - 1:
            nb_share    = sq_nb if t < sh['nb_eis_t'] else post_nb
            cpi_factor  = (1.0 + sh['cpi']) ** t
            scen_nom = sh['nb_ac'] * sh['eng_per_ac'] * nb_share * sh['nb_price_m'] * sh['gross_mult'] * cpi_factor / 1000.0
            base_nom = sh['nb_ac'] * sh['eng_per_ac'] * sq_nb    * sh['nb_price_m'] * sh['gross_mult'] * cpi_factor / 1000.0
            _delta_nb[i] = scen_nom - base_nom   # NOMINAL bar height
            _nominal_delta_total += _delta_nb[i]
            _pv_delta_total += _delta_nb[i] / ((1.0 + wacc) ** t)
        # WB cashflow within program window
        if t <= sh['wb_eis_t'] + _NPV_WIN - 1:
            wb_share    = sq_wb if t < sh['wb_eis_t'] else post_wb
            cpi_factor  = (1.0 + sh['cpi']) ** t
            scen_nom = sh['wb_ac'] * sh['eng_per_ac'] * wb_share * sh['wb_price_m'] * sh['gross_mult'] * cpi_factor / 1000.0
            base_nom = sh['wb_ac'] * sh['eng_per_ac'] * sq_wb    * sh['wb_price_m'] * sh['gross_mult'] * cpi_factor / 1000.0
            _delta_wb[i] = scen_nom - base_nom
            _nominal_delta_total += _delta_wb[i]
            _pv_delta_total += _delta_wb[i] / ((1.0 + wacc) ** t)

    # R&D and strain charged as lump-sum negatives at min EIS year (nominal)
    _lump_yr = min(sh['nb_eis_yr'], sh['wb_eis_yr'])
    _lump_idx = _years.index(_lump_yr) if _lump_yr in _years else 0
    _rd_arr = [0.0] * len(_years)
    _str_arr = [0.0] * len(_years)
    _rd_arr[_lump_idx] = -inv
    _str_arr[_lump_idx] = -strain
    _nominal_delta_total += (-inv) + (-strain)
    # PV for the implied yield — R&D/strain are charged at EIS year, discount accordingly
    _pv_delta_total += (-inv) / ((1.0 + wacc) ** (_lump_yr - 2026))
    _pv_delta_total += (-strain) / ((1.0 + wacc) ** (_lump_yr - 2026))

    _implied_yield = 100.0 + (_pv_delta_total / max(0.1, ev)) * 100.0

    _fig = go.Figure()
    _fig.add_trace(go.Bar(x=_years, y=_delta_nb, name='Δ NB engine revenue (nominal)',
                          marker=dict(color=color)))
    _fig.add_trace(go.Bar(x=_years, y=_delta_wb, name='Δ WB engine revenue (nominal)',
                          marker=dict(color=color, opacity=0.5)))
    _fig.add_trace(go.Bar(x=_years, y=_rd_arr, name='R&D charge',
                          marker=dict(color='#d29922')))
    _fig.add_trace(go.Bar(x=_years, y=_str_arr, name='Strain charge',
                          marker=dict(color='#c4341c')))
    _fig.update_layout(
        title=dict(text=f'{_player} Cash Flow — Δ nominal vs status quo ($B)',
                   font=dict(size=14, color='#eee')),
        barmode='relative',
        height=460, margin=dict(l=50, r=20, t=50, b=40),
        paper_bgcolor='#0d1117', plot_bgcolor='#000', font=dict(color='#ddd'),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(title='Year', dtick=2, gridcolor='rgba(255,255,255,0.08)'),
        yaxis=dict(title='Δ PV ($B)', gridcolor='rgba(255,255,255,0.08)',
                   zerolinecolor='rgba(255,255,255,0.4)'),
    )
    st.plotly_chart(_fig, use_container_width=True)
    st.caption(
        f"Bars show **nominal annual Δ cash flows** (CPI-escalated, no WACC discounting) — "
        f"this is what gets booked on the P&L each year. "
        f"Nominal cumulative Δ = **${_nominal_delta_total:+.2f}B**. "
        f"NB revenue bars run {sh['nb_eis_yr']}–{sh['nb_eis_yr']+19}; "
        f"WB bars run {sh['wb_eis_yr']}–{sh['wb_eis_yr']+19}. "
        f"R&D (${inv:.1f}B) + strain (${strain:.1f}B) are lump-sum negatives at {_lump_yr}. "
        f"&nbsp;&nbsp;**Implied yield: {_implied_yield:.0f}%** "
        f"— this is the same nominal stream PV-discounted at WACC={wacc*100:.1f}% (EV=${ev:.0f}B), "
        f"which reconciles to the equilibrium yield."
    )


# ── Dispatch to the chosen board ───────────────────────────
if _board_choice == _BOARD_SUMMARY:
    run_summary_tab()
elif _board_choice == _BOARD_AIRFRAMER:
    run_airframer_board()
elif _board_choice == _BOARD_ENGINE:
    run_engine_board()
else:
    run_oem_dashboard_tab()