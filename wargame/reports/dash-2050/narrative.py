"""Narrative for the dash-2050 page (placeholder until the game is played)."""
TITLE = "dash-2050 war game"
LEDE = "Placeholder."
FINDINGS = [("Placeholder", "Text.")]
TILES = {}
DPV_TITLE = "Each player's ΔPV after each round"
SHARES_LEDE = ""
NB_TITLE = "Narrowbody"
BOEING_PATH_TITLE = "Boeing path"
WB_TITLE = "Widebody"
ENG_NB_TITLE = "NB engines"
ENG_WB_TITLE = "WB engines"
MONEY_LEDE = ""
TIMELINE_LEDE = ""
PLAY_LEDE = ""
PLAY_POINTS = []
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
<li>The audit below lists every file path each agent touched.</li>
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
</ul>
"""
FOOTER = "Placeholder."
ROUNDS = {}
