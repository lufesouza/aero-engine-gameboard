"""Headless solver for the user's Combined_Game_Board.py (dash-2050 game-master copy: also captures each board's locals as _AFLOC/_ELOC) (mock-streamlit exec; never runs Streamlit).
Adapted from the wb-game-analysis skill harness: picks the board via the radio mock and injects
session-state captures right after each board's equilibrium bookkeeping."""
import sys, types, contextlib
import os
SRC = os.environ.get("BOARD_PY", os.path.join(os.path.dirname(os.path.abspath(__file__)), "Combined_Game_Board.py"))
base_src = open(SRC, newline="").read()
NL = "\r\n" if "\r\n" in base_src else "\n"
AF_ANCHOR = '    st.session_state["_af_near_nash_pairs"] = _near_nash_pairs'
EN_ANCHOR = '    st.session_state["_en_pw_locked_move"] = _forced_pw_move'
assert base_src.count(AF_ANCHOR) == 1 and base_src.count(EN_ANCHOR) == 1
AF_INJ = AF_ANCHOR + NL + '    st.session_state["_AFLOC"] = dict(locals())' + NL + '    st.session_state["_MX"] = matrix_data' + NL + '    st.session_state["_AMOVES"] = A_moves' + NL + '    st.session_state["_BMOVES"] = B_moves' + NL + '    st.session_state["_BASE"] = BASE' + NL + '    st.session_state["_EVAL"] = evaluate_scenario'
EN_INJ = EN_ANCHOR + NL + '    st.session_state["_ELOC"] = dict(locals())' + NL + '    st.session_state["_EMX"] = matrix' + NL + '    st.session_state["_EA"] = player_a_moves' + NL + '    st.session_state["_EC"] = player_c_moves' + NL + '    st.session_state["_EPURE"] = nash_pure' + NL + '    st.session_state["_ENEAR"] = nash_near' + NL + '    st.session_state["_ESIM"] = simulate' + NL + '    st.session_state["_EPW"] = sel_pw'
# Stop execution right after the captured board's math (rendering is not needed): raise a sentinel.
class _Done(Exception):
    pass
SRC_RUN = base_src.replace(AF_ANCHOR, AF_INJ + NL + '    raise _Done()').replace(EN_ANCHOR, EN_INJ + NL + '    raise _Done()')

BOARDS = {"airframer": "Airframer", "engine": "Engine 3-Player"}

def run(overrides, board="airframer", patch=None):
    src = SRC_RUN
    for old, new, n in (patch or []):
        assert src.count(old) == n, (old, src.count(old))
        src = src.replace(old, new)
    st = types.ModuleType("streamlit")
    class _SS(dict):
        def __getattr__(self, k):
            try: return self[k]
            except KeyError: raise AttributeError(k)
        def __setattr__(self, k, v): self[k] = v
    SS = _SS(); st.session_state = SS
    def _noop(*a, **k): return None
    class _Col(contextlib.AbstractContextManager):
        def __exit__(self, *a): return False
        def __enter__(self): return self
        def __getattr__(self, n): return getattr(st, n)
    for n in ["set_page_config", "markdown", "caption", "title", "info", "warning", "success", "error", "plotly_chart",
              "bar_chart", "line_chart", "text_area", "divider", "dataframe", "write", "subheader", "header", "metric",
              "code", "latex", "image", "pyplot", "table", "html", "button", "download_button", "toast"]:
        setattr(st, n, _noop)
    def _val(a, k, pos):
        key = k.get("key")
        if key and key in SS: return SS[key]
        if "value" in k: return k["value"]
        return a[pos] if len(a) > pos else (a[1] if len(a) > 1 else 0)
    def _sl(*a, **k):
        v = _val(a, k, 3)
        if k.get("key"): SS[k["key"]] = v
        return v
    def _ni(*a, **k):
        key = k.get("key")
        v = SS[key] if key and key in SS else k.get("value", a[1] if len(a) > 1 else 0.0)
        if key: SS[key] = v
        return v
    def _sb(*a, **k):
        key = k.get("key")
        opts = k.get("options", a[1] if len(a) > 1 else [None])
        v = SS[key] if key and key in SS else opts[k.get("index", 0) or 0]
        if key: SS[key] = v
        return v
    st.slider = _sl; st.number_input = _ni; st.selectbox = _sb
    want = BOARDS[board]
    st.radio = lambda l, o, **k: next((x for x in o if want in x), o[0])
    st.checkbox = lambda *a, **k: SS.get(k.get("key"), k.get("value", False))
    st.toggle = st.checkbox
    st.columns = lambda n, **k: [_Col() for _ in range(n if isinstance(n, int) else len(n))]
    st.expander = lambda *a, **k: _Col()
    st.tabs = lambda L, **k: [_Col() for _ in L]; st.container = lambda *a, **k: _Col(); st.empty = lambda *a, **k: _Col()
    class _Side:
        def __getattr__(self, n): return _noop
        def expander(self, *a, **k): return _Col()
        slider = staticmethod(_sl); number_input = staticmethod(_ni); selectbox = staticmethod(_sb)
        checkbox = staticmethod(lambda *a, **k: SS.get(k.get("key"), k.get("value", False)))
        def columns(self, n, **k): return [_Col() for _ in range(n if isinstance(n, int) else len(n))]
    st.sidebar = _Side(); sys.modules["streamlit"] = st
    SS.update(overrides)
    mod = types.ModuleType("board_x"); mod.__file__ = SRC
    mod.__dict__["_Done"] = _Done
    try:
        exec(compile(src, SRC, "exec"), mod.__dict__)
    except _Done:
        pass
    SS["_MOD"] = mod
    return SS

# Snapshot ('Game.txt') values mapped to the board's session keys
SNAP = {
    "af_eps_tol": 1.0, "af_alpha": 0.3, "_boeing_share_both": 50, "af_fps_7yr_adv": 5.0,
    "af_ramp10_b_pp": 1.0, "af_ramp10_a_pp": 1.0, "af_ramp7_b_pp": 1.0, "af_ramp7_a_pp": 1.0,
    "_b_supplier": "RR, PW, and CFM (all 3)", "_a_supplier": "PW and CFM",
    "af_price_737": 48.0, "af_price_a320": 52.0, "af_price_fps": 55.0, "af_price_ngsa": 55.0, "af_price_wb": 180.0,
    "af_m_a320": 13.14, "af_m_ngsa": 26.28, "af_m_a350": 4.95, "af_m_a350_alone": 10.76, "af_m_a350_both": 6.47,
    "af_m_737": 8.0, "af_m_fps": 25.64, "af_m_787": 20.0, "af_m_787_alone": 25.21, "af_m_787_both": 15.77,
    "af_cx_fps7": 64.47, "af_cx_fps10": 55.25, "af_cx_fpsemb": 100.0, "af_cx_ngsa": 30.07,
    "af_cx_787re": 5.0, "af_cx_a350re": 5.0, "af_cx_737rate": 2.94,
    "af_fps_eis": 2041, "af_ngsa_eis": 2037, "af_787_eis": 2035, "af_a350_eis": 2035,
    "af_nb_milker": 24.8, "af_wb_milker": 15.0, "af_wb_b_pp": 1.0, "af_wb_a_pp": 1.5,
    "af_sab_share": 5.0, "af_sab_cost": 1.0, "af_strain_a": 3.0, "af_strain_b": 3.0, "af_naked_fine": 48.32,
    "en_ev_a": 160.0, "en_debt_a": 35.0, "en_ev_b": 110.0, "en_debt_b": 40.0, "en_ev_c": 110.0, "en_debt_c": 40.0,
    "en_rd_cfm_open_fan": 8.0, "en_rd_cfm_ducted": 4.0, "en_rd_pw_solo": 2.0, "en_rd_pw_jv": 2.0,
    "en_rd_rr_nb": 8.0, "en_rd_rr_wb": 4.0, "en_rd_rr_t1000": 2.0,
    "en_strain_cost": 2.0, "en_rr_nbwb_strain": 5.0, "en_lobby_cost": 1.0, "en_eps_tol": 5.0, "en_gross_mult": 1.6,
}

def af(over=None, patch=None):
    ov = dict(SNAP); ov.update(over or {})
    SS = run(ov, "airframer", patch)
    return SS["_MX"], SS["_AMOVES"], SS["_BMOVES"], SS

def en(over=None, patch=None):
    ov = dict(SNAP); ov.update(over or {})
    return run(ov, "engine", patch)

LBL = {"Launch_NGSA": "Launch NGSA", "Milk_A320neo": "Do Nothing (A320neo)", "Sabotage_Bottleneck": "Delay fps Bottleneck",
       "Sabotage_Poaching": "Delay fps Poaching", "Re_engine_A350": "Re-engine A350", "Milk_A350": "Do Nothing A350",
       "Launch_fps_7yr_Solo": "fps 7yr Solo", "Launch_fps_10yr_Solo": "fps 10yr Solo", "Launch_fps_via_Embraer": "fps via Embraer",
       "Milk_737MAX": "Do Nothing (737 MAX)", "Increase_737_Rate": "737 Rate Increase", "Re_engine_787": "Re-engine 787", "Milk_787": "Do Nothing 787"}
def lab(strat):
    return " + ".join(LBL[m] for m in strat if m in LBL)

def eq_lists(MX, A, B):
    pure, near = [], []
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            c = MX[i][j]
            if c["is_nash"]: pure.append((a, b, c["yield_a"], c["yield_b"], c["a_total_delta"], c["b_total_delta"]))
            elif c["is_near_nash"]: near.append((a, b, c["yield_a"], c["yield_b"], c["a_total_delta"], c["b_total_delta"]))
    return pure, near

# ── Overlap-aware strain (the later "$3B overlap-strain" build described in the skill's model map) ──
_FLAT_B = "        b_strain_penalty_nom = v_capex_strain_b if (b_launches_nb and b_reengines) else 0.0"
_FLAT_A = "        a_strain_penalty_nom = a_strain_penalty_nom_placeholder"
def _ov(nb, wb):
    return ("max(0.0, min(1.0, (min({nb}, {wb}) - max({nb} - 7, {wb} - 5)) / 5.0))").format(nb=nb, wb=wb)
OVERLAP_PATCH = [
    ("        b_strain_penalty_nom = v_capex_strain_b if (b_launches_nb and b_reengines) else 0.0",
     "        b_strain_penalty_nom = (v_capex_strain_b * " + _ov("v_fps_eis_year", "v_787_eis_year") + ") if (b_launches_nb and b_reengines) else 0.0", 1),
    ("        a_strain_penalty_nom = v_capex_strain_a if (a_launches_nb and a_reengines) else 0.0",
     "        a_strain_penalty_nom = (v_capex_strain_a * " + _ov("v_ngsa_eis_year", "v_a350_eis_year") + ") if (a_launches_nb and a_reengines) else 0.0", 1),
]

import re as _re
def parse_snapshot(path):
    """Return the airframer near-Nash list from Game.txt as [(airbus_yield, boeing_yield, A-tuple, B-tuple)]."""
    txt = open(path, encoding="utf-8").read()
    af_part = txt.split("ENGINE GAME")[0]
    out = []
    for blk in _re.split(r"\n  Near-Nash #\d+  ", af_part)[1:]:
        m = _re.match(r"\(Airbus (\d+)% \| Boeing (\d+)%\)", blk)
        ya, yb = int(m.group(1)), int(m.group(2))
        an = _re.search(r"Airbus  NB: (.*)", blk).group(1); aw = _re.search(r"Airbus  WB: (.*)", blk).group(1)
        bn = _re.search(r"Boeing  NB: (.*)", blk).group(1); bw = _re.search(r"Boeing  WB: (.*)", blk).group(1)
        a = ("Launch_NGSA" if "Launch NGSA" in an else "Milk_A320neo",
             "Sabotage_Bottleneck" if "Bottleneck" in an else "No_Bottleneck",
             "Sabotage_Poaching" if "Poaching" in an else "No_Poaching",
             "Re_engine_A350" if "Re-engine" in aw else "Milk_A350")
        bnb = ("Launch_fps_7yr_Solo" if "7yr" in bn else "Launch_fps_10yr_Solo" if "10yr" in bn
               else "Launch_fps_via_Embraer" if "Embraer" in bn else "Milk_737MAX")
        b = (bnb, "Increase_737_Rate" if "Increase 737 Rate" in bn else "No_Rate_Increase",
             "Re_engine_787" if "Re-engine" in bw else "Milk_787")
        out.append((ya, yb, a, b))
    return out

def check_snapshot(MX, A, B, snap):
    """Compare a solved board with the snapshot: equilibrium sets and rounded yields."""
    pure, near = eq_lists(MX, A, B)
    got = {(a, b) for a, b, *_ in near}
    want = {(a, b) for _, _, a, b in snap}
    bad_round = []
    for ya, yb, a, b in snap:
        c = MX[A.index(a)][B.index(b)]
        if round(c["yield_a"]) != ya or round(c["yield_b"]) != yb:
            bad_round.append((ya, yb, round(c["yield_a"], 2), round(c["yield_b"], 2), lab(a), lab(b)))
    return dict(pure=len(pure), near=len(near), missing=len(want - got), extra=len(got - want), bad_round=bad_round)
