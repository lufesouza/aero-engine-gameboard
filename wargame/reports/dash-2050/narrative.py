"""Narrative for the dash-2050 page and report. Every number here is from data/report_data.json, the round grids
(runs/dash-2050/grids_rN.json, as shown to each player) or the players' own returns; make_dash_html.py checks the
headline numbers against the data when it builds (see CHECKS)."""

TITLE = "Five players, four rounds: both new narrowbodies arrive in 2037 and the market ends at 50/50"

LEDE = (
    "Five AI players played four sealed rounds (2030, 2035, 2045 and 2050) on your game-theory dashboard. Boeing, Airbus, "
    "CFM/GE, Pratt &amp; Whitney and Rolls-Royce each decided as its named leadership team, from its own profile and "
    "the PD briefing's objectives, moves, enablers and constraints. The game master alone saw the board. "
    "<b>Boeing launched fps on the 7-year ramp-up in 2030, the same year Airbus launched NGSA, so both enter service in "
    "2037 and the narrowbody market settles at 50/50 from 2047.</b> "
    "Airbus still finishes ahead (+$15.61B). The NGSA's margin and one covert Delay Tactic did that. "
    "Boeing ends at +$1.85B. Nobody re-engined a widebody. "
    "Rolls-Royce enters the narrowbody market (+$15.68B). CFM/GE keeps most narrowbody engines but loses $25.17B "
    "against today's 76% share, and P&amp;W loses $10.64B.")

FINDINGS = [
    ("Boeing's 2030 launch erased NGSA's head start.",
     " fps on the 7-year ramp-up enters service in 2037, alongside NGSA.<ul>"
     "<li>Boeing's narrowbody share climbs from 40% to 54% in 2045, helped by the ramp's 5-point first-mover bonus, "
     "and settles at 50%.</li>"
     "<li>In Boeing's own 2030 grid, against an NGSA launch, this plan scored +$3.79B. The 10-year ramp-up scored "
     "−$1.40B, which would have let NGSA lead by three years. Doing Nothing (with the rate increase) scored −$4.38B.</li>"
     "<li>Matching NGSA's date was worth about $8B to Boeing. This is the opposite of the fps-delay assessment, where a "
     "4-year NGSA lead left fps a knife-edge.</li></ul>"),
    ("Airbus still wins on value, with help from a covert Delay Tactic.",
     "<ul><li>NGSA's 26.3% margin, against 13.1% on the A320neo, adds $29.38B of narrowbody profit (PV).</li>"
     "<li>In 2035 Airbus ordered one Delay Tactic, a supply-chain bottleneck, against an fps already in development. "
     "It cost $0.48B and moved Airbus from +$13.44B to +$15.61B.</li>"
     "<li>It cut Boeing from +$3.79B to +$1.85B and Boeing's 2040 share from 49% to 44%.</li>"
     "<li>It was never exposed. The bulletin reported a 5-point delivery shortfall in 2037-41 without a cause, and "
     "Boeing read it as a supplier problem, as its doctrine says.</li></ul>"),
    ("Nobody re-engined a widebody.",
     " In every round, each pure equilibrium of the board's airframer stage game had exactly one side re-engining: a "
     "game of Chicken. Both held for all four rounds, so the 787 stays at 58.8% of widebody deliveries.<ul>"
     "<li><b>Boeing's reason:</b> one development at a time while fps was in development, then its A330neo "
     "\"no regret\" precedent.</li>"
     "<li><b>Airbus's reason:</b> its one-launch-a-round rule and its peak-spend test, then its $1B launch test.</li>"
     "<li>Measured ex post, re-engining in 2030 would have been worth $2.03B more to Boeing, or $1.77B more to Airbus.</li></ul>"),
    ("Engine selections set the engine makers' fortunes.",
     " Boeing put fps on CFM alone; Airbus opened NGSA to all three makers.<ul>"
     "<li>CFM/GE falls from 76% of narrowbody engines to 57.8% in 2037, then recovers to 63.5% from 2047 as Boeing's "
     "share rises. It keeps a majority throughout.</li>"
     "<li>Rolls-Royce goes from 0% to 20.6-23.5%.</li>"
     "<li>P&amp;W goes from 24% to 14.6-18.7%.</li>"
     "<li>P&amp;W and Rolls-Royce launched only once NGSA selected them (\"launch if selected\"), so no engine was "
     "built without an airframe.</li></ul>"),
    ("Rolls-Royce turned down a Joint Venture that would have paid.",
     " P&amp;W committed publicly to the Joint Venture in 2035. Rolls-Royce held: its rule is to commit only after P&amp;W "
     "is on the record, and the moves were simultaneous.<ul>"
     "<li>On the board, the Joint Venture would have given Rolls-Royce the same narrowbody share for less R&amp;D: "
     "$5.71B including the write-off on UltraFan Solo, against $8B. That makes +$17.97B against +$15.68B.</li>"
     "<li>It would have lifted P&amp;W from −$10.64B to −$5.13B, and taken CFM/GE from −$25.17B to −$32.26B.</li>"
     "<li>By 2045 joining was worth nothing more to Rolls-Royce, and it declined.</li></ul>"),
    ("Objectives: the entrant met both of its own; the airframers met one between them.",
     "<ul><li><b>Boeing</b> held incumbency, but missed 50/50 in 2040 (44%; met in 2045 and 2050).</li>"
     "<li><b>Airbus</b> lost both. Its 60/40 edge became 50/50, and the 737 rate increase broke A320 protection "
     "(55% in 2032-36).</li>"
     "<li><b>CFM/GE</b> kept narrowbody dominance (59.7% at worst) but never launched the Open Fan.</li>"
     "<li><b>P&amp;W</b> restored credibility (GTF2 flies on NGSA) at a loss.</li>"
     "<li><b>Rolls-Royce</b> met both: narrowbody entry and widebody dominance (55%).</li></ul>"),
]

TILES = {
    "boeing": "fps 7-year 2030 → EIS 2037; 737 rate up; 50/50 from 2047",
    "airbus": "NGSA 2030 → EIS 2037; one covert Delay Tactic (2035)",
    "cfm": "Ducted engine, Embraer partnership, GEnx upgrade; no Open Fan",
    "pratt_whitney": "GTF2 on NGSA; Joint Venture offer not taken up",
    "rolls_royce": "UltraFan NB on NGSA: 0% → 21% of NB engines",
}

DPV_TITLE = "Each player's ΔPV after each round: the game was decided in 2030 and 2035"

SHARES_LEDE = (
    "<ul><li><b>Narrowbody.</b> Boeing's 737 rate increase lifts its share to 45% in 2032-36. Both new narrowbodies "
    "enter service in 2037. The covert Delay Tactic holds Boeing 5 points down in 2037-41. The 7-year bonus carries it "
    "to 55% in 2046, and the market settles at 50/50.</li>"
    "<li><b>Widebody.</b> Untouched: nobody re-engined.</li>"
    "<li><b>Engines.</b> Rolls-Royce's narrowbody entry and CFM/GE's sole position on fps set the engine split. The "
    "GEnx upgrade moves 2.8 points of widebody engines to CFM/GE from 2035.</li></ul>")
NB_TITLE = "Narrowbody deliveries: Boeing from 40% to 50/50, by way of 45%, 41% and 55%"
BOEING_PATH_TITLE = "Boeing's narrowbody share as projected after each round: the Delay Tactic is the only revision"
WB_TITLE = "Widebody deliveries: unchanged, because neither side re-engined"
ENG_NB_TITLE = "Narrowbody engines: Rolls-Royce enters at 21-24%; CFM/GE keeps a majority throughout"
ENG_WB_TITLE = "Widebody engines: the GEnx upgrade takes 2.8 points from Rolls-Royce in 2035"

MONEY_LEDE = (
    "<ul><li>The airframers' ΔPV is narrowbody profit above the status quo, less the new airplane's bill, booked at "
    "entry into service as the board does, and the debt penalty.</li>"
    "<li>Boeing's fps bill ($21.50B in PV for $64.47B booked in 2037), its debt penalty ($7.23B) and the rate "
    "increase ($1.62B) absorb all but $1.85B of its +$32.18B narrowbody gain.</li>"
    "<li>Airbus's smaller bill ($12.90B in PV) and low debt ($0.39B) leave it about half of its +$29.38B.</li>"
    "<li>Engine value is the lifetime value of the engines each maker delivers. Rolls-Royce's narrowbody entry takes its "
    "yearly engine value from $4.2B in 2036 to $11.4B in 2037.</li></ul>")

TIMELINE_LEDE = (
    "Every programme in the game was launched in 2030; after that, nothing was launched or cancelled. Both new "
    "narrowbodies enter service in 2037. P&amp;W's GTF2 (2036), CFM's ducted engine (2036) and Rolls-Royce's UltraFan "
    "NB (2037) were all ready in time for them.")

PLAY_LEDE = (
    "Regret measures what a player gave up against its best alternative in that round, holding everything else in "
    "the game as played. The airframers' regret is all in the widebody, where both held. Rolls-Royce's is all in the "
    "untaken Joint Venture. CFM/GE's and P&amp;W's orders were each the best reply to the round as played. "
    "Rolls-Royce's ex-post regret for 2030 comes from the Joint Venture, which needed P&amp;W's later commitment.")

PLAY_POINTS = [
    ("Calibration.",
     "<ul><li>Airbus expected +$32.09B in 2030. It got +$13.44B, because it put only 10% on Boeing choosing the "
     "7-year ramp-up.</li>"
     "<li>P&amp;W expected +$2.55B and got −$11.37B. It had expected NGSA to name P&amp;W and CFM; NGSA named all "
     "three.</li>"
     "<li>From 2035 on, Airbus and Rolls-Royce were within $0.9B of the board each round, and Boeing within $1.3B. "
     "CFM/GE was up to $4.1B too pessimistic and P&amp;W up to $3.3B too optimistic.</li></ul>"),
    ("Fidelity to doctrine.",
     "<ul><li>Each player declared the premiums its doctrine cost.</li>"
     "<li>Boeing: $0.74B for the Round-1 rate increase and $0.80B for passing on the 787 Re-engine. Both were within "
     "its $1B tie band.</li>"
     "<li>Airbus: $3.35B in 2030, for the A350 Re-engine and Delay Tactics its red lines ruled out. Then $1.57B, "
     "$0.91B and $0.59B for staying out of the A350 Re-engine.</li>"
     "<li>No player cancelled a programme.</li></ul>"),
    ("Information discipline.",
     "<ul><li>Every player stayed inside its own brief and profile; the isolation audit below found no access to "
     "another player's files.</li>"
     "<li>The covert Delay Tactic stayed covert. Airbus never mentioned it in public, and the bulletin reported only "
     "the delivery shortfall.</li></ul>"),
]

FOOTER = ("BOEING PROPRIETARY. Built from the dash-2050 game record (wargame/runs/dash-2050) by wargame/dashgame/reports.py "
          "and wargame/reports/dash-2050/make_dash_html.py. Board: Combined_Game_Board.py at the Game.txt snapshot.")

ROUNDS = {
    1: {"title": "2030: both new narrowbodies launch in the same year",
        "lede": ("<ul><li><b>Airbus</b> launched NGSA on its own clock, open to all three engine makers. It "
                 "expected Boeing's fps to take the 10-year ramp-up or go via Embraer.</li>"
                 "<li><b>Boeing</b> lifted its Round-1 hard rule: by its own reading the 777X and MAX 7/10 were done and "
                 "its debt repaired. It launched fps on the 7-year ramp-up on CFM, plus the 737 rate increase.</li>"
                 "<li><b>P&amp;W and Rolls-Royce</b> launched on being selected for NGSA.</li>"
                 "<li><b>CFM/GE</b> committed a ducted engine for both airframers, a partnership with Embraer and the "
                 "GEnx upgrade.</li>"
                 "<li>No player touched the widebody.</li></ul>")},
    2: {"title": "2035: a covert Delay Tactic and an unanswered Joint Venture offer",
        "lede": ("<ul><li><b>Airbus</b> ordered one Delay Tactic (supply-chain bottleneck) against the fps in "
                 "development. It cost Boeing 5 points of share in 2037-41.</li>"
                 "<li><b>P&amp;W</b> committed publicly to a Joint Venture; <b>Rolls-Royce</b> waited for a commitment "
                 "on the record.</li>"
                 "<li><b>Boeing</b> passed on the 787 Re-engine. It would overlap fps by two years, and an A350 "
                 "Re-engine would cancel its gain.</li></ul>")},
    3: {"title": "2045: everyone holds; the delivery shortfall is published without a cause",
        "lede": ("<ul><li>Both new narrowbodies have been in service since 2037. The only live levers were the "
                 "widebody Re-engines and the Joint Venture, and every player held.</li>"
                 "<li><b>Boeing</b> treated the 2037-41 shortfall as a supplier issue.</li>"
                 "<li><b>Airbus</b> re-tested the A350 Re-engine and found it below its $1B launch bar.</li>"
                 "<li><b>Rolls-Royce</b> judged the Joint Venture worthless once UltraFan was flying.</li></ul>")},
    4: {"title": "2050: everyone holds again; the game ends at 50/50",
        "lede": ("A Re-engine ordered in 2050 would enter service only in 2055. Discounted to 2026, its gain was "
                 "below each airframer's launch bar. Every player held, and the final state is the 2035 state.")},
}

METHOD = """
<h3>How the game was run</h3>
<ul class="cav">
<li><b>Board.</b> Your Combined_Game_Board.py, run headless (never in Streamlit) at the snapshot settings in Game.txt.
The overlap-aware two-front strain from the earlier analysis is used. Every airframer number is the board's own
<code>evaluate_scenario()</code> at the game's entry-into-service dates. The year-by-year figures are traced from inside it
and reconcile to its present values to 10<sup>−9</sup>.</li>
<li><b>Players.</b> Five agents, one per company. Each decided as its named leadership team: CEO frames, CFO tests,
operating head tests, then the team's decision rule. Each used its company profile, its executive and role profiles,
and a dashboard addendum that maps the briefing slide's goals, moves, enablers and constraints onto the board.</li>
<li><b>Information.</b> Only the game master (GM) saw the full board.
<ul>
<li>Each player received the public bulletin plus a private brief: its own position, its own year-by-year projection,
its objective status, and its own payoff for each of its plans against a few public scenarios of rival moves.</li>
<li>A hook blocked every player from other players' profiles and briefs, from the run record, from the board file, the
snapshot, the GM code and earlier reports.</li>
<li>The audit below lists what each agent touched.</li>
</ul></li>
<li><b>Rounds.</b> Four sealed, simultaneous rounds: 2030, 2035, 2045, 2050. Each round's value is the board's valuation of
the state after that round, assuming nobody moves again. The final round's value is the game outcome.</li>
</ul>
<h3>Rules the GM added to the static board</h3>
<ul class="cav">
<li><b>Time.</b>
<ul>
<li>A programme enters service (or an engine is ready) after its development time from the decision year: fps 7 or 10
years, fps via Embraer 10, NGSA 7, Re-engines 5; ducted engine 6, GTF2 6, UltraFan NB 7, UltraFan WB 6, Trent and GEnx
upgrades 3; Open Fan 10 and never before 2045.</li>
<li>Unlaunched programmes keep the snapshot dates (fps 2041, NGSA 2037, Re-engines 2035) for the board's valuation
windows.</li>
<li>The 737 rate increase could only be ordered in 2030 (the board dates it 2032).</li>
</ul></li>
<li><b>Cancellations</b> write off the bill × years elapsed ÷ development years, booked in the cancel year, with the board's
debt penalty.</li>
<li><b>Delay Tactics</b> are covert.
<ul>
<li>Their spend falls in the years before fps entry into service, never before the order year.</li>
<li>The naked fine applies only if Boeing never launches fps.</li>
<li>Their share effect enters another player's valuation only once it is fully in the past. The bulletin then reports
the shortfall in Boeing's deliveries without a cause.</li>
</ul></li>
<li><b>Engines.</b> The engine board is applied year by year.
<ul>
<li>Each airframer's narrowbody share is split equally among the engines actually fitted to its airframe. The board uses a
fixed 50/50 split; here the split follows the airframers' year-by-year shares.</li>
<li>Each engine move counts from the year it is ready. An engine not ready by an airframe's entry into service is dropped
from it; CFM is always available.</li>
<li>The Joint Venture forms when both makers have committed.</li>
<li>Open Fan's wait penalty applies only if a new narrowbody enters service before it is ready.</li>
<li>UltraFan WB counts only once a re-engined widebody is in service.</li>
<li>With every engine ready at the board's entry into service and a 50/50 split, this reproduces the board's
<code>simulate()</code> exactly; tested on 648 move combinations.</li>
</ul></li>
<li><b>Other moves</b> (pricing campaigns, partnerships, derivatives) were recorded and published when public, but the board
does not price them.</li>
</ul>
<h3>What the numbers are</h3>
<ul class="cav">
<li><b>ΔPV and yield.</b> ΔPV is the change in present value at 2026 against the status quo (nobody launches anything), at
each player's board WACC: Boeing 10.5%, Airbus 8%, CFM/GE 8.5%, P&amp;W and RR 10%. Yield = 100 + ΔPV ÷ enterprise value.</li>
<li><b>Board conventions.</b>
<ul>
<li>Airframe programme spend is booked in full at entry into service.</li>
<li>Engine R&amp;D is undiscounted.</li>
<li>Each programme's market counts for 20 years from its entry into service.</li>
<li>Engine value is lifetime value per engine delivered: price × 1.6, rising 2.2% a year.</li>
</ul></li>
<li><b>Regret.</b> The final ΔPV a player would have had with its best alternative orders in that round, holding every other
order in the game as played (later rounds re-run), minus its actual final ΔPV.</li>
<li><b>What the board does not price.</b> Engine durability, customer lock-in, COMAC or Embraer as entrants, the
A220-500, pricing campaigns and government support. Players' moves on these are recorded in each round's detail.</li>
</ul>
"""

# Headline numbers the builder checks against data/report_data.json: (description, round index, player, field, value)
CHECKS = [
    ("final ΔPV", -1, "boeing", "pv_delta", 1.85), ("final ΔPV", -1, "airbus", "pv_delta", 15.61),
    ("final ΔPV", -1, "cfm", "pv_delta", -25.17), ("final ΔPV", -1, "pratt_whitney", "pv_delta", -10.64),
    ("final ΔPV", -1, "rolls_royce", "pv_delta", 15.68), ("round-1 ΔPV", 0, "boeing", "pv_delta", 3.79),
    ("round-1 ΔPV", 0, "airbus", "pv_delta", 13.44),
]
SHARE_CHECKS = [("cfm", "nb_share", 2037, .578), ("cfm", "nb_share", 2047, .635), ("rolls_royce", "nb_share", 2037, .235), ("rolls_royce", "nb_share", 2050, .206), ("pratt_whitney", "nb_share", 2037, .187), ("pratt_whitney", "nb_share", 2045, .146), ("boeing", "nb_share", 2040, .44), ("boeing", "nb_share", 2045, .54), ("boeing", "nb_share", 2050, .50),
                ("boeing", "nb_share", 2032, .45), ("boeing", "nb_share", 2046, .55), ("airbus", "nb_share", 2045, .46),
                ("cfm", "nb_share", 2040, .597), ("rolls_royce", "wb_share", 2040, .552)]
