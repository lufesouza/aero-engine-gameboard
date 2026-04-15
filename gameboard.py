import streamlit as st
import numpy as np
import itertools

# ==========================================
# 1. PAGE CONFIGURATION & STRICT THEME
# ==========================================
st.set_page_config(page_title="Aero Engine Game Theory Matrix", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Strict Dark Theme */
.stApp { background-color: #000000; color: #FFFFFF; }
[data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }

/* Tactical Gameboard HTML/CSS */
.board-container { width: 100%; overflow: visible !important; margin-top: 20px; margin-bottom: 50px; background: #050505; border: 2px solid #333; border-radius: 8px; padding: 10px; overflow-x: auto; }
.board-table { border-collapse: separate; border-spacing: 3px; font-family: 'Courier New', Courier, monospace; background-color: #000; width: 100%; min-width: 1200px; }

.board-th-col { background-color: #1a0d00; border: 1px solid #FFA500; border-bottom: 3px solid #FFA500; padding: 8px; text-align: center; font-size: 11px; color: #FFA500; position: sticky; top: 0; z-index: 10; }
.board-th-row { background-color: #001a26; border: 1px solid #00BFFF; border-right: 3px solid #00BFFF; padding: 8px; text-align: left; font-size: 11px; color: #00BFFF; position: sticky; left: 0; z-index: 10; white-space: nowrap; }

.board-td { background-color: #0a0a0a; border: 1px solid #222; padding: 12px 4px; text-align: center; vertical-align: middle; font-size: 11px; transition: all 0.2s ease-in-out; cursor: crosshair; position: relative; }
.board-td:hover { background-color: #1f1f1f; transform: scale(1.05); z-index: 50; border: 1px solid #777; }

/* Nash Equilibrium Styles */
@keyframes pulse-green {
    0% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0.7); }
    70% { box-shadow: 0 0 10px 5px rgba(60, 179, 113, 0); }
    100% { box-shadow: 0 0 0 0 rgba(60, 179, 113, 0); }
}
.nash-pure { border: 2px solid #3cb371 !important; background-color: #002b11 !important; font-weight: bold; animation: pulse-green 2s infinite; }
.nash-near { border: 2px dashed #FFD700 !important; background-color: #2b2400 !important; }

/* Interactive Hover Tooltip */
.board-td .receipt-tooltip { visibility: hidden; width: 380px; background-color: #111; color: #fff; text-align: left; border: 1px solid #555; border-radius: 6px; padding: 12px; position: absolute; z-index: 999; bottom: 120%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.2s; box-shadow: 0px 10px 20px rgba(0,0,0,0.9); font-family: monospace; font-size: 11px; line-height: 1.4; pointer-events: none; }
.board-td .receipt-tooltip::after { content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px; border-width: 5px; border-style: solid; border-color: #555 transparent transparent transparent; }
.board-td:hover .receipt-tooltip { visibility: visible; opacity: 1; }

/* Math Receipt Boxes */
.nash-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 20px; font-family: monospace; }
.nash-title { color: #58a6ff; font-size: 16px; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 15px; }
.nash-title-pure { color: #3cb371; font-size: 16px; font-weight: bold; border-bottom: 1px solid #3cb371; padding-bottom: 10px; margin-bottom: 15px; }
.nash-title-near { color: #FFD700; font-size: 16px; font-weight: bold; border-bottom: 1px solid #FFD700; padding-bottom: 10px; margin-bottom: 15px; }
.delta-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
.delta-col { background: #000; padding: 15px; border-radius: 4px; border-left: 3px solid; }

/* Player Colors */
.player-a { color: #00BFFF; font-weight: bold; } /* CFM/GE */
.player-b { color: #32CD32; font-weight: bold; } /* PW */
.player-c { color: #FFA500; font-weight: bold; } /* RR */
.col-a { border-color: #00BFFF; }
.col-b { border-color: #32CD32; }
.col-c { border-color: #FFA500; }

/* Move Lists */
.move-list-box { background: #111; padding: 15px; border-radius: 6px; border: 1px solid #333; height: 100%; }
.move-item { font-size: 11px; color: #ccc; margin-bottom: 4px; font-family: monospace; }

/* Breakdown Table inside Nash Box */
.math-breakdown-table { width: 100%; font-size: 12px; color: #bbb; margin-bottom: 12px; border-collapse: collapse; }
.math-breakdown-table td { padding: 6px 4px; border-bottom: 1px solid #222; }
.math-breakdown-table .val { text-align: right; color: #fff; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA REGRESSION (ENGINE PRICING)
# ==========================================
thrust_data = np.array([8729, 9220, 12670, 13360, 13630, 18900, 23000, 14200, 20000, 25000])
shipset_price_data = np.array([4.7, 4.7, 5.0, 5.5, 5.5, 6.0, 7.1, 5.2, 7.0, 5.9])

engine_price_data = shipset_price_data / 2.0  # Price per engine
slope, intercept = [float(x) for x in np.polyfit(thrust_data, engine_price_data, 1)]

NB_THRUST = 30000
WB_THRUST = 80000
CPI_RATE = 0.022  

base_price_nb_m = slope * NB_THRUST + intercept
base_price_wb_m = slope * WB_THRUST + intercept
base_price_nb_b = base_price_nb_m / 1000.0  # Billions
base_price_wb_b = base_price_wb_m / 1000.0

ENGINES_PER_AC = 2
NB_AC_PER_YR = 2000  
WB_AC_PER_YR = 170   

# Default Hardcoded Baselines (Prompt)
FIXED_BASE_CFM_NB = 0.60 
FIXED_BASE_PW_NB  = 0.40
FIXED_BASE_RR_NB  = 0.00
FIXED_BASE_CFM_WB = 0.42            
FIXED_BASE_RR_WB  = 0.58   
FIXED_BASE_PW_WB  = 0.00 

# ==========================================
# 3. STRATEGY DICTIONARIES
# ==========================================
a_grp_A = ["0-Do nothing and Milk the LEAP", "1-Launch Only Open Fan", "2- Launch Only Ducted", "3- Launch Open and Ducted"]
a_grp_B = ["", " | 4- Partner with Embraer"]
a_grp_C = ["", " | 5- Lobby Governments"]
a_grp_D = ["", " | 6- Upgrade Genx9", " | 7- Invest In improvements to Genx"]

a_combos_raw = list(itertools.product(a_grp_A, a_grp_B, a_grp_C, a_grp_D))
a_combos_filtered = []
for a, b, c, d in a_combos_raw:
    if "0-Do nothing" in a and "4- Partner" in b: continue
    a_combos_filtered.append(f"{a}{b}{c}{d}")

player_a_16 = []
for base_move in a_grp_A:
    count = 0
    for move in a_combos_filtered:
        if move.startswith(base_move) and count < 4:
            player_a_16.append(move)
            count += 1

c_grp_A = ["0-Do Nothing different from Status Quo", "1- Launch Ultrafan WB only", "3-JV with PW for a new NB Engine", "4-Upgrade T1000"]
c_grp_B = ["", " | 2-Launch Ultra fan for NB solo"]

c_combos_raw = list(itertools.product(c_grp_A, c_grp_B))
c_combos_filtered = []
for a, b in c_combos_raw:
    if "3-JV" in a and "2-Launch" in b: continue
    c_combos_filtered.append(f"{a}{b}")

player_c_16 = c_combos_filtered.copy()
while len(player_c_16) < 16:
    player_c_16.append(player_c_16[len(player_c_16) % len(c_combos_filtered)] + " (Alt)")

pw_grp_A = ["1- Milk GTF", "2- Launch GTF 2 & Go solo", "3- JV with RR to develop a more Efficient GTF"]
pw_grp_B = ["", " | 4-Invest in a new Engine for the WB Market", " | 5-Leverage JV with RR to enter WB Market"]
pw_combos = [f"{a}{b}" for a, b in itertools.product(pw_grp_A, pw_grp_B)]

# ==========================================
# 4. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### ⚙️ Engine Market Parameters")

eps_tolerance = st.sidebar.slider("Epsilon-Nash Tolerance Yield (%)", 0.0, 10.0, 5.0, 0.5)

with st.sidebar.expander("⏳ Timeline Parameter", expanded=False):
    current_year = st.slider("Current Year (>2037)", min_value=2038, max_value=2056, value=2045, step=1)
    n_years = current_year - 2037
    n_years = max(0, min(n_years, 20)) 
    st.caption(f"Calculated N = {n_years} Years")

with st.sidebar.expander("📊 Balance Sheets ($B)", expanded=False):
    ev_a = st.number_input("CFM/GE EV", value=160.0, step=5.0)
    wacc_a = st.slider("CFM/GE WACC (%)", 5.0, 15.0, 8.5, 0.1) / 100
    st.divider()
    ev_b = st.number_input("PW EV", value=110.0, step=5.0)
    wacc_b = st.slider("PW WACC (%)", 5.0, 15.0, 10.0, 0.1) / 100
    st.divider()
    ev_c = st.number_input("RR EV", value=110.0, step=5.0)  
    wacc_c = st.slider("RR WACC (%)", 5.0, 15.0, 10.0, 0.1) / 100

with st.sidebar.expander("💰 Sunk Base Tot Invest ($B)", expanded=False):
    st.caption("Applied to all active states as sunk capital commitments.")
    inv_open_ducted = st.number_input("CFM Open/Ducted R&D", value=5.0)
    inv_gtf2 = st.number_input("PW GTF2 R&D", value=2.0)
    inv_ultrafan = st.number_input("RR Ultrafan R&D", value=4.0)

with st.sidebar.expander("📈 Market Shifts & Disruption", expanded=False):
    open_fan_loss = st.slider("Open Fan Wait Penalty % (Loss to CFM)", 0, 100, 35) / 100.0
    ducted_fan_gain = st.slider("Ducted Fan CFM Gain % (Share Protected)", 0, 100, 10) / 100.0
    strain_penalty = st.number_input("Disruption Op Costs (Strain $B)", value=2.0)

st.sidebar.markdown("#### ♟️ Player B (PW) Move Setting")
selected_pw_move = st.sidebar.selectbox("Set Player B (PW) Static Move:", pw_combos)
move_b_val = selected_pw_move
pw_fights_wb = "WB Market" in move_b_val

# ---------- NEW: SEPARATED TIMELINE SLIDERS ----------
with st.sidebar.expander("📊 Pre-2037 Market (Status Quo Base)", expanded=False):
    st.caption("Defines the historical baseline EV that players are trying to beat. RR is locked to 0% in NB today.")
    st.markdown("**Narrowbody (NB) Status Quo**")
    sq_cfm_nb_pct = st.slider("CFM/GE NB Base (%)", 0, 100, int(FIXED_BASE_CFM_NB*100), key="sq_cfm_nb")
    sq_pw_nb_pct  = st.slider("PW NB Base (%)", 0, 100, int(FIXED_BASE_PW_NB*100), key="sq_pw_nb")
    st.slider("RR NB Base (%)", 0, 100, 0, disabled=True, key="sq_rr_nb_dummy")
    sq_rr_nb_pct = 0.0 # Hardcoded RR to 0 for pre-2037
    
    st.divider()
    st.markdown("**Widebody (WB) Status Quo**")
    sq_cfm_wb_pct = st.slider("CFM/GE WB Base (%)", 0, 100, int(FIXED_BASE_CFM_WB*100), key="sq_cfm_wb")
    sq_rr_wb_pct  = st.slider("RR WB Base (%)", 0, 100, int(FIXED_BASE_RR_WB*100), key="sq_rr_wb")
    st.slider("PW WB Base (%)", 0, 100, 0, disabled=True, key="sq_pw_wb_dummy")
    sq_pw_wb_pct  = 0.0 # Hardcoded PW to 0 for pre-2037

with st.sidebar.expander("🔮 Post-2037 Market (Future Baseline)", expanded=True):
    st.caption("Sets the organic market starting point in 2037 BEFORE game moves apply their modifiers.")
    st.markdown("**Narrowbody (NB) Future Start**")
    fut_cfm_nb_pct = st.slider("CFM/GE NB Start (%)", 0, 100, int(FIXED_BASE_CFM_NB*100), key="fut_cfm_nb")
    fut_pw_nb_pct  = st.slider("PW NB Start (%)", 0, 100, int(FIXED_BASE_PW_NB*100), key="fut_pw_nb")
    fut_rr_nb_pct  = st.slider("RR NB Start (%)", 0, 100, int(FIXED_BASE_RR_NB*100), key="fut_rr_nb")
    
    st.divider()
    st.markdown("**Widebody (WB) Future Start**")
    fut_cfm_wb_pct = st.slider("CFM/GE WB Start (%)", 0, 100, int(FIXED_BASE_CFM_WB*100), key="fut_cfm_wb")
    fut_rr_wb_pct  = st.slider("RR WB Start (%)", 0, 100, int(FIXED_BASE_RR_WB*100), key="fut_rr_wb")
    fut_pw_wb_pct  = st.slider(
        "PW WB Start (%)", 
        min_value=0, max_value=100, value=int(FIXED_BASE_PW_WB*100), 
        disabled=not pw_fights_wb,
        key="fut_pw_wb",
        help="Disabled because PW's selected move does not target the Widebody market." if not pw_fights_wb else "Adjust PW's starting Widebody Share in the state."
    )

# --- Normalization ---
# Pre-2037 Base Normalization
tot_sq_nb = sq_cfm_nb_pct + sq_pw_nb_pct + sq_rr_nb_pct
base_cfm_nb = (sq_cfm_nb_pct / tot_sq_nb) if tot_sq_nb > 0 else 0
base_pw_nb  = (sq_pw_nb_pct / tot_sq_nb) if tot_sq_nb > 0 else 0
base_rr_nb  = (sq_rr_nb_pct / tot_sq_nb) if tot_sq_nb > 0 else 0

tot_sq_wb = sq_cfm_wb_pct + sq_pw_wb_pct + sq_rr_wb_pct
base_cfm_wb = (sq_cfm_wb_pct / tot_sq_wb) if tot_sq_wb > 0 else 0
base_pw_wb  = (sq_pw_wb_pct / tot_sq_wb) if tot_sq_wb > 0 else 0
base_rr_wb  = (sq_rr_wb_pct / tot_sq_wb) if tot_sq_wb > 0 else 0

# Post-2037 Future Normalization
tot_fut_nb = fut_cfm_nb_pct + fut_pw_nb_pct + fut_rr_nb_pct
start_cfm_nb = (fut_cfm_nb_pct / tot_fut_nb) if tot_fut_nb > 0 else 0
start_pw_nb  = (fut_pw_nb_pct / tot_fut_nb) if tot_fut_nb > 0 else 0
start_rr_nb  = (fut_rr_nb_pct / tot_fut_nb) if tot_fut_nb > 0 else 0

raw_future_pw_wb = (fut_pw_wb_pct if pw_fights_wb else 0.0)
tot_fut_wb = fut_cfm_wb_pct + fut_rr_wb_pct + raw_future_pw_wb
start_cfm_wb = (fut_cfm_wb_pct / tot_fut_wb) if tot_fut_wb > 0 else 0
start_pw_wb  = (raw_future_pw_wb / tot_fut_wb) if tot_fut_wb > 0 else 0
start_rr_wb  = (fut_rr_wb_pct / tot_fut_wb) if tot_fut_wb > 0 else 0

# ==========================================
# 5. MATHEMATICAL ENGINE & MATRIX BUILDER
# ==========================================
def calculate_cumulative_npv(planes_per_year, share, base_price_b, wacc, n_years):
    if n_years <= 0 or wacc <= 0.0 or base_price_b <= 0.0: 
        return 0.0
    cumulative_npv = 0.0
    for t in range(1, int(n_years) + 1):
        price_t = base_price_b * ((1 + CPI_RATE) ** t)
        cf_t = planes_per_year * ENGINES_PER_AC * share * price_t
        pv_t = cf_t / ((1 + wacc) ** t)
        cumulative_npv += pv_t
    return float(cumulative_npv)

def simulate_state(move_a, move_b, move_c, n_val):
    
    # 1. Base NPV Calculation uses Pre-2037 Baseline values
    base_a = calculate_cumulative_npv(NB_AC_PER_YR, base_cfm_nb, base_price_nb_b, wacc_a, n_val) + \
             calculate_cumulative_npv(WB_AC_PER_YR, base_cfm_wb, base_price_wb_b, wacc_a, n_val)
    base_b = calculate_cumulative_npv(NB_AC_PER_YR, base_pw_nb, base_price_nb_b, wacc_b, n_val) + \
             calculate_cumulative_npv(WB_AC_PER_YR, base_pw_wb, base_price_wb_b, wacc_b, n_val)
    base_c = calculate_cumulative_npv(NB_AC_PER_YR, base_rr_nb, base_price_nb_b, wacc_c, n_val) + \
             calculate_cumulative_npv(WB_AC_PER_YR, base_rr_wb, base_price_wb_b, wacc_c, n_val)

    # Future active state initializes with Post-2037 values
    a_nb_s, a_wb_s = start_cfm_nb, start_cfm_wb
    b_nb_s, b_wb_s = start_pw_nb, start_pw_wb
    c_nb_s, c_wb_s = start_rr_nb, start_rr_wb
    
    inv_a, strain_a = 0.0, 0.0
    inv_b, strain_b = 0.0, 0.0
    inv_c, strain_c = 0.0, 0.0

    # ---------------------------------------------------------
    # ACTION ENGINE
    # ---------------------------------------------------------
    inv_a += inv_open_ducted 
    inv_b += inv_gtf2 
    inv_c += inv_ultrafan 

    # --- PLAYER A (CFM/GE) ---
    projects_a = 0
    if "1-Launch Only Open Fan" in move_a: projects_a += 1
    if "2- Launch Only Ducted" in move_a: projects_a += 1
    if "3- Launch Open and Ducted" in move_a: projects_a += 2
    if "4- Partner" in move_a: projects_a += 1
    if "6- Upgrade" in move_a: projects_a += 1
    if "7- Invest" in move_a: projects_a += 1
    if projects_a >= 2: strain_a += strain_penalty

    if "1-Launch Only Open Fan" in move_a: 
        a_nb_s -= open_fan_loss
        if "NB solo" in move_c or "JV with PW" in move_c:
            b_nb_s += (open_fan_loss / 2); c_nb_s += (open_fan_loss / 2)
        else:
            b_nb_s += open_fan_loss
    elif "2- Launch Only Ducted" in move_a or "3- Launch Open and Ducted" in move_a:
        a_nb_s += ducted_fan_gain
        if "NB solo" in move_c or "JV with PW" in move_c:
            b_nb_s -= (ducted_fan_gain / 2); c_nb_s -= (ducted_fan_gain / 2)
        else:
            b_nb_s -= ducted_fan_gain

    if "4- Partner with Embraer" in move_a: a_nb_s += 0.05
    if "5- Lobby Governments" in move_a: a_nb_s += 0.05
    if "6- Upgrade Genx9" in move_a or "7- Invest" in move_a: a_wb_s += 0.05

    # --- PLAYER B (PW) ---
    projects_b = 0
    if "2- Launch GTF 2" in move_b: projects_b += 1
    if "3- JV with RR" in move_b: projects_b += 1
    if "4-Invest" in move_b: projects_b += 1
    if "5-Leverage" in move_b: projects_b += 1
    if projects_b >= 2: strain_b += strain_penalty

    if "2- Launch GTF 2" in move_b: 
        b_nb_s += 0.10; a_nb_s -= 0.05; c_nb_s -= 0.05
    if "3- JV with RR" in move_b:
        b_nb_s += 0.05; c_nb_s += 0.05; a_nb_s -= 0.10
    if "4-Invest" in move_b:
        inv_b += 3.0; b_wb_s += 0.05; a_wb_s -= 0.025; c_wb_s -= 0.025
    if "5-Leverage" in move_b:
        b_wb_s += 0.10; a_wb_s -= 0.10

    # --- PLAYER C (RR) ---
    projects_c = 0
    if "1- Launch Ultrafan WB only" in move_c: projects_c += 1
    if "2-Launch Ultra fan for NB" in move_c: projects_c += 1
    if "3-JV with PW" in move_c: projects_c += 1
    if "4-Upgrade T1000" in move_c: projects_c += 1
    if projects_c >= 2: strain_c += strain_penalty

    if "1- Launch Ultrafan WB only" in move_c:
        c_wb_s += 0.10; a_wb_s -= 0.10
    if "2-Launch Ultra fan for NB solo" in move_c:
        c_nb_s += 0.15; a_nb_s -= 0.10; b_nb_s -= 0.05
    if "3-JV with PW" in move_c:
        c_nb_s += 0.05; b_nb_s += 0.05; a_nb_s -= 0.10
    if "4-Upgrade T1000" in move_c:
        inv_c += 2.0; c_wb_s += 0.05; a_wb_s -= 0.05

    # NORMALIZATION (Post-Move)
    a_nb_s, b_nb_s, c_nb_s = max(0, a_nb_s), max(0, b_nb_s), max(0, c_nb_s)
    a_wb_s, b_wb_s, c_wb_s = max(0, a_wb_s), max(0, b_wb_s), max(0, c_wb_s)

    total_nb_post = a_nb_s + b_nb_s + c_nb_s
    if total_nb_post > 0:
        a_nb_s /= total_nb_post; b_nb_s /= total_nb_post; c_nb_s /= total_nb_post
        
    total_wb_post = a_wb_s + b_wb_s + c_wb_s
    if total_wb_post > 0:
        a_wb_s /= total_wb_post; b_wb_s /= total_wb_post; c_wb_s /= total_wb_post

    # YIELD CALCULATIONS
    new_npv_a = calculate_cumulative_npv(NB_AC_PER_YR, a_nb_s, base_price_nb_b, wacc_a, n_val) + \
                calculate_cumulative_npv(WB_AC_PER_YR, a_wb_s, base_price_wb_b, wacc_a, n_val)
    new_npv_b = calculate_cumulative_npv(NB_AC_PER_YR, b_nb_s, base_price_nb_b, wacc_b, n_val) + \
                calculate_cumulative_npv(WB_AC_PER_YR, b_wb_s, base_price_wb_b, wacc_b, n_val)
    new_npv_c = calculate_cumulative_npv(NB_AC_PER_YR, c_nb_s, base_price_nb_b, wacc_c, n_val) + \
                calculate_cumulative_npv(WB_AC_PER_YR, c_wb_s, base_price_wb_b, wacc_c, n_val)

    u_a = float(new_npv_a - base_a - strain_a - inv_a)
    u_b = float(new_npv_b - base_b - strain_b - inv_b)
    u_c = float(new_npv_c - base_c - strain_c - inv_c)

    safe_ev_a = max(0.1, float(ev_a))
    safe_ev_b = max(0.1, float(ev_b))
    safe_ev_c = max(0.1, float(ev_c))

    yield_a = float(100.0 + (u_a / safe_ev_a) * 100)
    yield_b = float(100.0 + (u_b / safe_ev_b) * 100)
    yield_c = float(100.0 + (u_c / safe_ev_c) * 100)

    # Return nb_base/wb_base mapped to the Pre-2037 Status Quo to measure true Strategic Delta in Receipts
    return {
        "A": {"yield_pct": yield_a, "delta_b": u_a, "base_b": base_a, "strain_b": strain_a, "inv_b": inv_a, "nb_base": base_cfm_nb, "nb_final": a_nb_s, "wb_base": base_cfm_wb, "wb_final": a_wb_s},
        "B": {"yield_pct": yield_b, "delta_b": u_b, "base_b": base_b, "strain_b": strain_b, "inv_b": inv_b, "nb_base": base_pw_nb, "nb_final": b_nb_s, "wb_base": base_pw_wb, "wb_final": b_wb_s},
        "C": {"yield_pct": yield_c, "delta_b": u_c, "base_b": base_c, "strain_b": strain_c, "inv_b": inv_c, "nb_base": base_rr_nb, "nb_final": c_nb_s, "wb_base": base_rr_wb, "wb_final": c_wb_s}
    }

matrix_v4 = []
for a_move in player_a_16:
    row = []
    for c_move in player_c_16:
        row.append(simulate_state(a_move, move_b_val, c_move, n_years))
    matrix_v4.append(row)

# NASH EQUILIBRIUM SOLVER
best_a_for_c = []
for c in range(16):
    col_yields = [matrix_v4[a][c]["A"]["yield_pct"] for a in range(16)]
    best_a_for_c.append(col_yields.index(max(col_yields)))
    
best_c_for_a = []
for a in range(16):
    row_yields = [matrix_v4[a][c]["C"]["yield_pct"] for c in range(16)]
    best_c_for_a.append(row_yields.index(max(row_yields)))

nash_pure = []
nash_near = []
for a in range(16):
    for c in range(16):
        y_a = matrix_v4[a][c]["A"]["yield_pct"]
        y_c = matrix_v4[a][c]["C"]["yield_pct"]
        best_y_a = matrix_v4[best_a_for_c[c]][c]["A"]["yield_pct"]
        best_y_c = matrix_v4[a][best_c_for_a[a]]["C"]["yield_pct"]
        
        if (best_y_a - y_a <= 0.01) and (best_y_c - y_c <= 0.01):
            nash_pure.append((a, c))
        elif (best_y_a - y_a <= eps_tolerance) and (best_y_c - y_c <= eps_tolerance):
            nash_near.append((a, c))

# ==========================================
# 6. RENDER THE INTERACTIVE GAMEBOARD
# ==========================================
st.title("🎲 Aerospace Engine Gameboard (3-Player Simulation)")
st.markdown(f"**Board Context:** <span class='player-a'>Player A: CFM/GE (Rows)</span> vs <span class='player-c'>Player C: Rolls-Royce (Columns)</span>. <span class='player-b'>Player B: PW is locked in: [{move_b_val}]</span>.", unsafe_allow_html=True)

html_board = ['<div class="board-container"><table class="board-table"><tr><th style="background:#000; border:none; z-index:20;"></th>']

for c_move in player_c_16:
    display_c_move = c_move.replace(" | ", "<br/>+ ")
    html_board.append(f'<th class="board-th-col" style="min-width: 160px; line-height: 1.4;">{display_c_move}</th>')
html_board.append('</tr>')

for a_idx, a_move in enumerate(player_a_16):
    display_a_move = a_move.replace(" | ", "<br/>+ ")
    html_board.append(f'<tr><th class="board-th-row" style="line-height: 1.4;">{display_a_move}</th>')
    
    for c_idx in range(16):
        cell_class = "board-td"
        icon = ""
        if (a_idx, c_idx) in nash_pure:
            cell_class += " nash-pure"; icon = "⭐<br/>"
        elif (a_idx, c_idx) in nash_near:
            cell_class += " nash-near"; icon = "⚠️<br/>"
            
        data = matrix_v4[a_idx][c_idx]
        a_name_str = player_a_16[a_idx]
        c_name_str = player_c_16[c_idx]
        
        a_y_disp, c_y_disp, b_y_disp = data["A"]["yield_pct"], data["C"]["yield_pct"], data["B"]["yield_pct"]
        a_d_disp, b_d_disp, c_d_disp = data["A"]["delta_b"], data["B"]["delta_b"], data["C"]["delta_b"]
        
        tooltip = [
            f"<div class='receipt-tooltip'>",
            f"<div style='border-bottom: 1px solid #444; margin-bottom: 8px; color:#FFD700; font-weight:bold;'>TACTICAL MATH RECEIPT (N={n_years})</div>",
            f"<div style='margin-bottom: 8px;'><b>CFM:</b> {a_name_str}<br/><b>PW:</b> {move_b_val}<br/><b>RR:</b> {c_name_str}</div>",
            f"<span class='player-a'>[A] CFM/GE Yield: {a_y_disp:.2f}% (Δ ${a_d_disp:+.2f}B)</span><br/>",
            f"<span class='player-b'>[B] PW Yield: {b_y_disp:.2f}% (Δ ${b_d_disp:+.2f}B)</span><br/>",
            f"<span class='player-c'>[C] Rolls-Royce Yield: {c_y_disp:.2f}% (Δ ${c_d_disp:+.2f}B)</span><br/>",
            "</div>"
        ]
        html_board.append(f'<td class="{cell_class}">{icon}<span class="player-a">{a_y_disp:.1f}%</span><br/><span style="color:#555;">vs</span><br/><span class="player-c">{c_y_disp:.1f}%</span>{"".join(tooltip)}</td>')
    html_board.append('</tr>')
html_board.append('</table></div>')
st.markdown("".join(html_board), unsafe_allow_html=True)

# ==========================================
# 7. MATH RECEIPTS & ASSUMPTIONS (NASH BOXES)
# ==========================================
st.markdown("---")
st.title("🧮 Game Math Breakdown & Nash Receipts")

base_a = matrix_v4[0][0]["A"]["base_b"]
base_b = matrix_v4[0][0]["B"]["base_b"]
base_c = matrix_v4[0][0]["C"]["base_b"]

yr1_nb_npv = base_price_nb_m * (1 + CPI_RATE)**1
yrN_nb_npv = base_price_nb_m * (1 + CPI_RATE)**n_years
yr1_wb_npv = base_price_wb_m * (1 + CPI_RATE)**1
yrN_wb_npv = base_price_wb_m * (1 + CPI_RATE)**n_years

base_a_nb = calculate_cumulative_npv(NB_AC_PER_YR, base_cfm_nb, base_price_nb_b, wacc_a, n_years)
base_a_wb = calculate_cumulative_npv(WB_AC_PER_YR, base_cfm_wb, base_price_wb_b, wacc_a, n_years)
base_b_nb = calculate_cumulative_npv(NB_AC_PER_YR, base_pw_nb, base_price_nb_b, wacc_b, n_years)
base_b_wb = calculate_cumulative_npv(WB_AC_PER_YR, base_pw_wb, base_price_wb_b, wacc_b, n_years)
base_c_nb = calculate_cumulative_npv(NB_AC_PER_YR, base_rr_nb, base_price_nb_b, wacc_c, n_years)
base_c_wb = calculate_cumulative_npv(WB_AC_PER_YR, base_rr_wb, base_price_wb_b, wacc_c, n_years)

st.markdown(f"""
<div class="nash-box">
<div class="nash-title-pure" style="color:#58a6ff;">🏛️ Baseline Status Quo Breakdown</div>

<table class="math-breakdown-table" style="font-size:13px; color:#ddd; width:100%; text-align:left; border-collapse: collapse; margin-bottom: 20px;">
    <tr><td colspan="4" style="border-bottom:1px solid #444; color:#58a6ff; font-weight:bold; padding-bottom:5px;">1. PRE-2037 STATUS QUO SHARES (Defines the $EV Target)</td></tr>
    <tr>
        <td style="padding:8px;"><b>NB Market:</b> 40k Total Planes</td>
        <td style="padding:8px;"><span class="player-a"><b>CFM Pre-2037 NB:</b> {base_cfm_nb*100:.0f}%</span></td>
        <td style="padding:8px;"><span class="player-b"><b>PW Pre-2037 NB:</b> {base_pw_nb*100:.0f}%</span></td>
        <td style="padding:8px;"><span class="player-c"><b>RR Pre-2037 NB:</b> {base_rr_nb*100:.0f}%</span></td>
    </tr>
    <tr>
        <td style="padding:8px;"><b>WB Market:</b> 3.4k Total Planes</td>
        <td style="padding:8px;"><span class="player-a"><b>CFM Pre-2037 WB:</b> {base_cfm_wb*100:.0f}%</span></td>
        <td style="padding:8px;"><span class="player-b"><b>PW Pre-2037 WB:</b> {base_pw_wb*100:.0f}%</span></td>
        <td style="padding:8px;"><span class="player-c"><b>RR Pre-2037 WB:</b> {base_rr_wb*100:.0f}%</span></td>
    </tr>
    <tr><td colspan="4" style="border-bottom:1px solid #444; padding-top:15px; padding-bottom:5px; color:#58a6ff; font-weight:bold;">2. EXTRAPOLATED ENGINE PRICING & CPI GROWTH (2 Engines per Plane)</td></tr>
    <tr>
        <td style="padding:8px;"><b>NB Base Price (Year 0):</b> ${base_price_nb_m:.2f}M</td>
        <td style="padding:8px;"><b>NB NPV/Engine (Year 1):</b> ${yr1_nb_npv:.2f}M</td>
        <td colspan="2" style="padding:8px;"><b>NB NPV/Engine (Year {n_years}):</b> ${yrN_nb_npv:.2f}M</td>
    </tr>
    <tr>
        <td style="padding:8px;"><b>WB Base Price (Year 0):</b> ${base_price_wb_m:.2f}M</td>
        <td style="padding:8px;"><b>WB NPV/Engine (Year 1):</b> ${yr1_wb_npv:.2f}M</td>
        <td colspan="2" style="padding:8px;"><b>WB NPV/Engine (Year {n_years}):</b> ${yrN_wb_npv:.2f}M</td>
    </tr>
    <tr><td colspan="4" style="border-bottom:1px solid #444; padding-top:15px; padding-bottom:5px; color:#58a6ff; font-weight:bold;">3. DCF DISCOUNTING VARIABLES</td></tr>
    <tr>
        <td style="padding:8px;"><b>Timeline (N):</b> {n_years} Years</td>
        <td style="padding:8px;"><span class="player-a"><b>CFM WACC:</b> {wacc_a*100:.1f}%</span></td>
        <td style="padding:8px;"><span class="player-b"><b>PW WACC:</b> {wacc_b*100:.1f}%</span></td>
        <td style="padding:8px;"><span class="player-c"><b>RR WACC:</b> {wacc_c*100:.1f}%</span></td>
    </tr>
</table>

<div class="delta-grid" style="border-top:1px solid #30363d; padding-top:20px;">
    <div class="delta-col col-a">
        <span class="player-a">Player A (CFM/GE) EV Base</span><br/>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <table class="math-breakdown-table">
            <tr><td><b>Cumulative NPV (NB):</b></td><td class="val">${base_a_nb:.2f}B</td></tr>
            <tr><td><b>Cumulative NPV (WB):</b></td><td class="val">${base_a_wb:.2f}B</td></tr>
        </table>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <b>Total Cumulative Base NPV:</b> <span class="player-a" style="float:right; font-size:16px;">${base_a:.2f}B</span>
    </div>
    <div class="delta-col col-b">
        <span class="player-b">Player B (PW) EV Base</span><br/>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <table class="math-breakdown-table">
            <tr><td><b>Cumulative NPV (NB):</b></td><td class="val">${base_b_nb:.2f}B</td></tr>
            <tr><td><b>Cumulative NPV (WB):</b></td><td class="val">${base_b_wb:.2f}B</td></tr>
        </table>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <b>Total Cumulative Base NPV:</b> <span class="player-b" style="float:right; font-size:16px;">${base_b:.2f}B</span>
    </div>
    <div class="delta-col col-c">
        <span class="player-c">Player C (RR) EV Base</span><br/>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <table class="math-breakdown-table">
            <tr><td><b>Cumulative NPV (NB):</b></td><td class="val">${base_c_nb:.2f}B</td></tr>
            <tr><td><b>Cumulative NPV (WB):</b></td><td class="val">${base_c_wb:.2f}B</td></tr>
        </table>
        <hr style="border: 1px solid #222; margin: 8px 0;">
        <b>Total Cumulative Base NPV:</b> <span class="player-c" style="float:right; font-size:16px;">${base_c:.2f}B</span>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

def get_diff_str_dollars(old_share_pct, new_share_pct, plane_type, wacc_val):
    old_share = old_share_pct / 100.0
    new_share = new_share_pct / 100.0
    if plane_type == 'NB':
        npv_old = calculate_cumulative_npv(NB_AC_PER_YR, old_share, base_price_nb_b, wacc_val, n_years)
        npv_new = calculate_cumulative_npv(NB_AC_PER_YR, new_share, base_price_nb_b, wacc_val, n_years)
    else:
        npv_old = calculate_cumulative_npv(WB_AC_PER_YR, old_share, base_price_wb_b, wacc_val, n_years)
        npv_new = calculate_cumulative_npv(WB_AC_PER_YR, new_share, base_price_wb_b, wacc_val, n_years)
        
    diff_b = npv_new - npv_old
    color = "#3cb371" if diff_b > 0.005 else ("#ff6666" if diff_b < -0.005 else "#777777")
    sign = "+" if diff_b > 0.005 else ("-" if diff_b < -0.005 else "")
    if abs(diff_b) <= 0.005: val_str = "±$0.00B"
    else: val_str = f"{sign}${abs(diff_b):.2f}B"
    return f"<span style='color:{color}; font-size:11px; margin-left:4px;'>({val_str})</span>"

def render_nash_receipt(idx, a, c, is_pure=True):
    move_a_str = player_a_16[a]
    move_c_str = player_c_16[c]
    
    a_nb_old, a_nb_new = matrix_v4[a][c]["A"]["nb_base"] * 100.0, matrix_v4[a][c]["A"]["nb_final"] * 100.0
    a_wb_old, a_wb_new = matrix_v4[a][c]["A"]["wb_base"] * 100.0, matrix_v4[a][c]["A"]["wb_final"] * 100.0
    a_inv, a_strain, a_delta, a_yield = matrix_v4[a][c]["A"]["inv_b"], matrix_v4[a][c]["A"]["strain_b"], matrix_v4[a][c]["A"]["delta_b"], matrix_v4[a][c]["A"]["yield_pct"]
    a_color = '#3cb371' if a_delta >= 0 else '#ff4444'

    b_nb_old, b_nb_new = matrix_v4[a][c]["B"]["nb_base"] * 100.0, matrix_v4[a][c]["B"]["nb_final"] * 100.0
    b_wb_old, b_wb_new = matrix_v4[a][c]["B"]["wb_base"] * 100.0, matrix_v4[a][c]["B"]["wb_final"] * 100.0
    b_inv, b_strain, b_delta, b_yield = matrix_v4[a][c]["B"]["inv_b"], matrix_v4[a][c]["B"]["strain_b"], matrix_v4[a][c]["B"]["delta_b"], matrix_v4[a][c]["B"]["yield_pct"]
    b_color = '#3cb371' if b_delta >= 0 else '#ff4444'

    c_nb_old, c_nb_new = matrix_v4[a][c]["C"]["nb_base"] * 100.0, matrix_v4[a][c]["C"]["nb_final"] * 100.0
    c_wb_old, c_wb_new = matrix_v4[a][c]["C"]["wb_base"] * 100.0, matrix_v4[a][c]["C"]["wb_final"] * 100.0
    c_inv, c_strain, c_delta, c_yield = matrix_v4[a][c]["C"]["inv_b"], matrix_v4[a][c]["C"]["strain_b"], matrix_v4[a][c]["C"]["delta_b"], matrix_v4[a][c]["C"]["yield_pct"]
    c_color = '#3cb371' if c_delta >= 0 else '#ff4444'
    
    title = f"⭐ Pure Nash Equilibrium #{idx+1}" if is_pure else f"⚠️ Near-Nash Equilibrium #{idx+1}"
    border_color = "#3cb371" if is_pure else "#FFD700"
    title_class = "nash-title-pure" if is_pure else "nash-title-near"

    st.markdown(f"""
<div class="nash-box" style="border-left: 4px solid {border_color};">
<div class="{title_class}">{title}</div>
<div style="color:#ddd; margin-bottom:15px; font-size:13px; font-family: monospace;">
<b>A (CFM/GE):</b> {move_a_str} <br/>
<b>B (PW):</b> {move_b_val} <br/>
<b>C (RR):</b> {move_c_str}
</div>
<div class="delta-grid">

<div class="delta-col col-a">
<span class="player-a" style="font-size:14px; text-transform:uppercase;">Player A (CFM) Delta vs Baseline</span><br/>
<hr style="border: 1px solid #222; margin: 8px 0;">
<table class="math-breakdown-table">
<tr><td><b>NB Share (Base ➔ Final):</b></td><td class="val">{a_nb_old:.0f}% ➔ {a_nb_new:.0f}%</td></tr>
<tr><td><b>WB Share (Base ➔ Final):</b></td><td class="val">{a_wb_old:.0f}% ➔ {a_wb_new:.0f}%</td></tr>
<tr><td><b>R&D / Sunk CAPEX:</b></td><td class="val" style="color:#ff6666;">-${a_inv:.2f}B</td></tr>
<tr><td style="border-bottom:none;"><b>Op Strain Cost:</b></td><td class="val" style="border-bottom:none; color:#ff6666;">-${a_strain:.2f}B</td></tr>
</table>
<hr style="border: 1px solid #222; margin: 8px 0;">
<b>Cumulative Δ EV:</b> <span style="color:{a_color}">${a_delta:+.2f}B</span><br/>
<span style="color:#fff; font-size: 15px;"><b>Final Yield: {a_yield:.2f}%</b></span>
</div>

<div class="delta-col col-b">
<span class="player-b" style="font-size:14px; text-transform:uppercase;">Player B (PW) Delta vs Baseline</span><br/>
<hr style="border: 1px solid #222; margin: 8px 0;">
<table class="math-breakdown-table">
<tr><td><b>NB Share (Base ➔ Final):</b></td><td class="val">{b_nb_old:.0f}% ➔ {b_nb_new:.0f}%</td></tr>
<tr><td><b>WB Share (Base ➔ Final):</b></td><td class="val">{b_wb_old:.0f}% ➔ {b_wb_new:.0f}%</td></tr>
<tr><td><b>R&D / Sunk CAPEX:</b></td><td class="val" style="color:#ff6666;">-${b_inv:.2f}B</td></tr>
<tr><td style="border-bottom:none;"><b>Op Strain Cost:</b></td><td class="val" style="border-bottom:none; color:#ff6666;">-${b_strain:.2f}B</td></tr>
</table>
<hr style="border: 1px solid #222; margin: 8px 0;">
<b>Cumulative Δ EV:</b> <span style="color:{b_color}">${b_delta:+.2f}B</span><br/>
<span style="color:#fff; font-size: 15px;"><b>Final Yield: {b_yield:.2f}%</b></span>
</div>

<div class="delta-col col-c">
<span class="player-c" style="font-size:14px; text-transform:uppercase;">Player C (RR) Delta vs Baseline</span><br/>
<hr style="border: 1px solid #222; margin: 8px 0;">
<table class="math-breakdown-table">
<tr><td><b>NB Share (Base ➔ Final):</b></td><td class="val">{c_nb_old:.0f}% ➔ {c_nb_new:.0f}%</td></tr>
<tr><td><b>WB Share (Base ➔ Final):</b></td><td class="val">{c_wb_old:.0f}% ➔ {c_wb_new:.0f}%</td></tr>
<tr><td><b>R&D / Sunk CAPEX:</b></td><td class="val" style="color:#ff6666;">-${c_inv:.2f}B</td></tr>
<tr><td style="border-bottom:none;"><b>Op Strain Cost:</b></td><td class="val" style="border-bottom:none; color:#ff6666;">-${c_strain:.2f}B</td></tr>
</table>
<hr style="border: 1px solid #222; margin: 8px 0;">
<b>Cumulative Δ EV:</b> <span style="color:{c_color}">${c_delta:+.2f}B</span><br/>
<span style="color:#fff; font-size: 15px;"><b>Final Yield: {c_yield:.2f}%</b></span>
</div>

</div>
</div>
""", unsafe_allow_html=True)

all_nash_states = [(a, c, 'pure') for a, c in nash_pure] + [(a, c, 'near') for a, c in nash_near]
if not all_nash_states:
    st.markdown("<div class='nash-box'><i>No Pure or Near-Nash Equilibriums found. Adjust parameters.</i></div>", unsafe_allow_html=True)
else:
    for idx, (a, c) in enumerate(nash_pure): render_nash_receipt(idx, a, c, is_pure=True)
    for idx, (a, c) in enumerate(nash_near):
        if (a, c) not in nash_pure: render_nash_receipt(idx, a, c, is_pure=False)

# ==========================================
# 8. PLAYER MOVES & ASSUMPTIONS
# ==========================================
st.markdown("---")
st.markdown("### ♟️ Player Move Dictionaries")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("<div class='move-list-box'><span class='player-a'><b>Player A (CFM/GE) Moves:</b></span>", unsafe_allow_html=True)
    for m in player_a_16: st.markdown(f"<div class='move-item'>• {m}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_b:
    st.markdown("<div class='move-list-box'><span class='player-b'><b>Player B (PW) Moves:</b></span>", unsafe_allow_html=True)
    for m in pw_combos: st.markdown(f"<div class='move-item'>• {m}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_c:
    st.markdown("<div class='move-list-box'><span class='player-c'><b>Player C (RR) Moves:</b></span>", unsafe_allow_html=True)
    for m in player_c_16: st.markdown(f"<div class='move-item'>• {m}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 📋 Mathematical Assumptions & Market Details")
st.markdown(f"""
* **Engine Prices Extrapolated via Linear Regression:** Engine Base Price calculated via regression based on thrust requirements. Based on the Prompt Table, Base Price = **${base_price_nb_m:.2f}M** for NB (30k) and **${base_price_wb_m:.2f}M** for WB (80k).
* **Detailed Calculation & CPI:** Analysis projected over 20 years. Current model evaluates `N = {n_years}`. 
    * CPI Growth: 2.2% annually (`NPV_per_engine = Base_Price * (1+CPI)^t`)
    * **Math Implementation:** `NPV_each_Year = [Planes_that_Year * 2 Eng * Share * NPV_per_Engine] / (1+WACC)^t` iteratively summed over N years to accurately calculate true DCF NPV as requested.
* **Hardware Volume:** All aircraft modeled with 2 engines. Total NB Market: 40k planes (2000/yr). Total WB Market: 3.4k planes (170/yr). No operating margins are used.
* **Market Timelines (Pre-2037 vs Post-2037):** The "Status Quo EV target" is strictly defined by the **Pre-2037** sidebar group (where RR is historically excluded from NB). The strategic simulation moves start dynamically from the **Post-2037** future organic baseline. Math Receipts accurately map the Enterprise Value delta between the *Pre-2037 Base* and the *Post-Move Share*.
* **Player Exclusivity:** Handled dynamically via `itertools.product`. Filtered to ensure mutually exclusive plays (e.g. "Milk LEAP" and "Partner Embraer" never overlap). 
* **Sunk Costs (CAPEX):** Base R&D costs are legally defined as sunk costs ("in states they milk they lose this investment"). Consequently, the math deducts the respective baseline R&D from the Enterprise Value in *all* states.
* **CFM Strategic Dynamics (Open vs Ducted Option):** If CFM launches the Ducted Fan in 2037, they retain their dominance and prevent the loss of invested cash, protecting their baseline shares against incoming rivals. If CFM launches *Only Open Fan*, it triggers a massive penalty because airframers struggle to adapt the design and prefer available ducted platforms. Ducted prevents this bleeding and captures share mathematically by forcing the airframers to adopt it.
* **Strain Cost:** Concurrent projects incur an engineering / supply chain penalty calculated discretely against the Net Present EV Delta. (Penalties trigger if 2+ physical engineering projects occur simultaneously).
* **Utility Normalization:** Enterprise Value Yield % = `100% + (Total Delta EV / Total EV) * 100`.
""", unsafe_allow_html=True)
