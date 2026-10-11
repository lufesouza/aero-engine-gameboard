"""Narrative for the dash-2050-obj page and report: the ExCo-and-Board game replayed with Control's added objectives and
the July-August 2026 analyst models. Every number here is from data/report_data.json, data/compare_prev.json, the
previous game's data (../dash-2050-exco/data/report_data.json), the round grids and briefs (record/grids_rN.json,
record/brief_rN_<side>.md, as shown to each company), the companies' own decision chains (record/exco_result_rN.json)
or the analyst notes (wargame/profiles/<side>/analyst_models_2026.md); make_game_html.py checks the headline numbers
against the data when it builds (see CHECKS and SHARE_CHECKS). Titles, tiles and chart titles are plain text (the
builders escape them); the other strings are HTML. "The dashboard" is the game-theory model (combined_dash.py);
"Board" is always a company's Board; "Control" is the game's control cell, which set the objectives."""

TITLE = ("One order changes: Boeing opens fps to all three engine makers. Both new narrowbodies fly two engine sources and "
         "Boeing's balance sheet stays repaired; CFM/GE falls to 27% of narrowbody engines")

LEDE = (
    "<b>One order changed against the previous game: Boeing opened fps to all three engine makers instead of CFM alone, "
    "for Control's supply enabler. Every other order in the four rounds was the same.</b> "
    "So the airframers' values did not move (Airbus ΔPV +$23.37B, Boeing +$0.66B), and the engine makers' did: "
    "Rolls-Royce +$32.35B (was +$20.55B), P&amp;W +$8.88B (was −$2.93B), CFM/GE −$69.69B (was −$38.29B). From 2040 the "
    "P&amp;W-Rolls-Royce Joint Venture engine flies on both new narrowbodies and its partners hold 36.5% of narrowbody "
    "engines each; CFM/GE holds 27%, against 76% today. "
    "On Control's objectives: Boeing's net debt is at its historical level from 2029 and stays there through the fps "
    "spending peak, in the stress case too. Both new narrowbodies fly two engine sources, CFM and the Joint Venture "
    "engine, with three engine makers in the market. Rolls-Royce's widebody was never starved, but its own narrowbody "
    "money reached $5.71B against the $4B bound, a breach it stated before ordering. Thirteen of nineteen objectives "
    "were met, against twelve for the previous game's orders scored the same way. "
    "Twenty AI agents played four sealed rounds (2030, 2035, 2045 and 2050), as before: each company an executive "
    "committee (ExCo) of CEO, CFO and operating head under a Board agent, now with Control's objectives and the 2026 "
    "analyst models in their files. No Board vetoed anything.")

FINDINGS = [
    ("Control's supply enabler changed one order: Boeing opened fps to all three engine makers.",
     " The engine code does not enter Boeing's value on the dashboard, so the change cost Boeing nothing.<ul>"
     "<li>Ortberg's own record: \"Doctrine and my Low-confidence lean were code 3; code 7 keeps CFM as the fallback and "
     "serves the supply-stability enabler.\" His Board had asked for code 7 \"at no cost to Boeing's payoff\".</li>"
     "<li>In the previous game, with no enabler in its brief, Boeing put fps on CFM alone (code 3).</li>"
     "<li>Boeing published an engine competition: CFM the baseline engine, certifying first; a P&amp;W or Rolls-Royce "
     "engine to follow \"once it shows maturity and durability\". Goal: \"two or three engine sources on our narrowbody "
     "and three narrowbody engine makers in the market.\"</li>"
     "<li>P&amp;W and Rolls-Royce had each ordered a launch conditional on selection, so both triggered on both "
     "airframes. After 2030 each new narrowbody had three engine sources.</li></ul>"),
    ("The Joint Venture turned three engine sources into two.",
     "<ul><li>P&amp;W and Rolls-Royce committed on sealed orders in 2035, as in the previous game, and their two solo "
     "engines folded into one. Control counts the Joint Venture engine as one source, so fps and NGSA each fly two: "
     "CFM and the Joint Venture engine. The enabler's \"two or three\" is met at two.</li>"
     "<li>The Boeing Board in 2045: \"The enabler is met at two sources, not the three we planned in 2035: the Joint "
     "Venture folded both solo engines into one source.\" Boeing then said in public: \"If the Joint Venture engine "
     "stumbles, the fps is back on CFM alone.\"</li>"
     "<li>The Joint Venture was worth +$5.51B to P&amp;W and +$2.29B to Rolls-Royce, as before, and moved 4.8 points of "
     "narrowbody engines from CFM/GE to P&amp;W.</li>"
     "<li>Two of Control's aims pull apart here (inference): Rolls-Royce's $4B bound points to the Joint Venture (a $4B "
     "share against $8B alone), and the Joint Venture removes the third independent source the airframers' enabler "
     "prefers.</li></ul>"),
    ("Boeing's balance sheet stays repaired on the 10-year ramp, stress case included. The objective gave the ramp a "
     "second reason, not a new answer.",
     "<ul><li>The analysts' consensus cash flow takes Boeing's net debt from $22.53B at end-2026 to zero in 2029, before "
     "any game spend. The 10-year fps then spends $3.02B in 2030, peaking at $8.44B in 2036, and free cash flow stays "
     "positive every year: at least $2.52B in the stress case.</li>"
     "<li>The stress case separated the ramps. On the 7-year, net debt goes back above zero ($0.71B at end-2034, "
     "$0.47B at end-2035); via Embraer, up to $3.31B in 2037.</li>"
     "<li>The Board still preferred the 7-year by its worst-column rule (−$1.50B against −$1.96B), as in the previous "
     "game. This time it said it would approve the 10-year if the $0.46B given up was logged as objective premium. "
     "Ortberg logged it: \"Objective part: it keeps the stress-case debt line.\" Malave's balance-sheet test broke the "
     "tie.</li>"
     "<li>The share cost is unchanged: Boeing at 37% of narrowbodies in 2039 and 38% in 2040, missing incumbency, and "
     "47% from 2049.</li></ul>"),
    ("Rolls-Royce stated its breach of the $4B risk bound before ordering, and took the narrowbody anyway. Its widebody "
     "was never starved.",
     "<ul><li>Its 2030 brief showed the trade: UltraFan NB launched on selection is $8B of its own money if selected, "
     "and $5.7B if folded into a Joint Venture in 2035. Erginbilgic framed it: \"The price is that a selection takes our "
     "own narrowbody money to $8B, against Control's $4B bound.\"</li>"
     "<li>Staying inside meant holding everything, worth $8.31B less in expectation, above Rolls-Royce's $3B cap on "
     "objective premium. Every seat named the trade, and the Board approved: \"scored by Control, not a veto "
     "ground\".</li>"
     "<li>Both airframers selected it, and the 2035 fold left $5.71B: the $4B share plus $1.71B written off. Holding in "
     "2030 and joining in 2035 would have met all four objectives and been worth $1.71B more, but only because P&amp;W "
     "launched and the Joint Venture inherited GTF2's 2036 schedule. Rolls-Royce's 2030 record assumed a 2035 Joint "
     "Venture would be ready only in 2041.</li>"
     "<li>Widebody: it held the Trent 1000 upgrade and UltraFan WB in every round. Each lost more than its own bill once "
     "the $5B strain was in the row. Strain stayed $0, and Rolls-Royce keeps 55.2% of widebody engines from 2042.</li>"
     "</ul>"),
    ("CFM/GE paid for the second source: −$69.69B, $31.40B worse than the previous game, on identical orders.",
     "<ul><li>Its narrowbody engine share falls from 76% to 51.7% in 2037 and 27.0% from 2040, against 51-57% in the "
     "previous game. In 2040 it delivers 1,079 narrowbody engines against 3,040 in the status quo.</li>"
     "<li>CFM/GE learned the fps selection only from the 2035 brief, and nothing on its menu could change an airframer's "
     "engine code. Culp: \"Nothing on this grid defends against a switch\". In 2030 it had expected the ducted engine to "
     "keep it \"back above 50%\" if both airframers chose all three makers; the 2035 brief showed 31.7% from 2040, and "
     "the Joint Venture took that to 27.0%. The ducted engine is in that figure: without it CFM/GE would hold 17.5% "
     "(GM computation). Its own ExCo concluded in 2045, wrongly, that the 27.0% left no share for the ducted engine.</li>"
     "<li>It refused to compete for fps source position on price, in 2035 and again in 2050. Its Board: \"That is not "
     "ours to chase with terms.\"</li>"
     "<li>Control added no objective for CFM/GE. It missed both of its own: 27% against its 50% narrowbody target, and "
     "no Open Fan, which no round could make ready by 2050 within its $15B allowance.</li></ul>"),
    ("Airbus made the same orders for a new reason.",
     "<ul><li>NGSA again open to all three makers (code 7), launched in 2030 for 2037. Faury called it \"THE ENABLER "
     "TRAP\": if P&amp;W and Rolls-Royce held, NGSA would fly CFM alone. Code 7 was the only route to three sources, and "
     "only in 2030.</li>"
     "<li>No value was traded for it: \"the engine code is payoff-neutral on this board\".</li>"
     "<li>No Delay Tactics and no A350 Re-engine in any round, each on its own cash line or $1B test. Airbus's 60/40 "
     "edge is missed (53% in 2050), as before.</li></ul>"),
    ("No Board vetoed anything, and no veto check sent a decision back.",
     "<ul><li>Nine orders went to a Board (seven in 2030, two in 2035), all approved, as in the previous game.</li>"
     "<li>The CFOs' and operating heads' test memos marked 60 vetoes binding, all on options the CEOs did not choose.</li>"
     "<li>Of 140 answers to Board recommendations, the one open divergence is again Boeing's ramp. This time the "
     "Board had offered the 10-year as an alternative it would approve.</li></ul>"),
]

TILES = {
    "boeing": "fps 10-year, open to all three engine makers; net debt at its historical level from 2029; two engine sources",
    "airbus": "NGSA in service 2037, open to all three engine makers; two engine sources; A350 held",
    "cfm": "Ducted engine, Embraer partnership, GEnx upgrade; 27% of narrowbody engines from 2040 (76% today)",
    "pratt_whitney": "GTF2 selected for both new narrowbodies, folded into the Joint Venture in 2035: 36.5% of narrowbody engines",
    "rolls_royce": "UltraFan NB on both narrowbodies through the Joint Venture: 36.5%; own narrowbody money $5.71B against a $4B bound",
}

DPV_TITLE = "Each company's ΔPV after each round: settled in 2035, when the Joint Venture moved only the engine makers"

# ─────────────────────────────── Control's objectives ───────────────────────────────
OBJ_LEDE = (
    "Control added three kinds of objective to the base set. They were in every company's private brief from 2030, each "
    "plan on the payoff grid carried its metrics, and the GM scored them. They never change a payoff: the dashboard's "
    "ΔPV, its own debt penalty included, is untouched. A company could give up value for an objective only within its "
    "own premium cap, and had to log it.<ul>"
    "<li><b>Boeing: repair the balance sheet.</b> Net debt back to its historical level (about zero, rounded from its "
    "2010-2018 average of −$0.6B) by end-2030, and held at end-2035, 2040, 2045 and 2050; and the same in a stress case "
    "with free cash flow one-third below consensus. The GM's tracker starts from the analysts' consensus ($22.53B at "
    "end-2026) and their free cash flow to 2030.</li>"
    "<li><b>Boeing and Airbus: an enabler, stable engine supply.</b> Two or three independent engine sources on its new "
    "narrowbody in production in 2040, 2045 and 2050 (the Joint Venture engine is one source), and three narrowbody "
    "engine makers in the market in 2045 and 2050.</li>"
    "<li><b>Rolls-Royce: protect the widebody cash cow.</b> Its own narrowbody development money, committed or written "
    "off, at most $4B (the Joint Venture share; UltraFan NB Solo is $8B); and never a narrowbody and a widebody engine "
    "programme on the record at once (the dashboard's one-off $5B strain).</li></ul>"
    "<b>Thirteen of the nineteen objectives were met.</b> All seven of Control's additions to Boeing and Airbus were "
    "met from 2030 on; Rolls-Royce met the widebody line and missed the risk bound, by its own stated choice in 2030.")

DEBT_TITLE = ("Boeing net debt: at its historical level from 2029 in the base case and from 2030 in the stress case, and "
              "held through the fps spending peak")
DEBT_CAP = (
    "Net debt at year end in 2026 dollars, from the consensus $22.53B at end-2026. Base free cash flow is the analysts' "
    "consensus for 2027-2030, deflated at 2.2%, and flat at $13.79B after; the stress case is one-third lower. Programme "
    "cash is the fps bill spread over 2030-2039 on the standard development curve; the game's profit change counts from "
    "fps's entry into service in 2040. Once net debt is at its historical level, surplus cash goes to the owners, so the "
    "line stays at zero. With no new programme, net debt would also reach zero in 2029: the analysts' cash flow repairs "
    "the balance sheet before any game decision, and the objective tests whether a launch undoes it.")
CASH_TITLE = "fps programme cash against the stress-case free cash flow it must fit inside"
CASH_NOTE = (
    "<ul><li>Stress free cash flow is $9.19B a year from 2030 (2026 dollars). The 10-year fps spends $3.02B in 2030, "
    "rising to a peak of $8.44B in 2036. After the 21% tax effect, the year's free cash flow stays positive in every "
    "year: at least $2.52B (2036) in the stress case and $7.12B in the base case.</li>"
    "<li>The 7-year ramp packs a bigger bill ($65.00B against $60.32B) into fewer years: $12.54B in 2034. In the stress "
    "case that year's free cash flow is −$0.71B, so net debt goes back above zero ($0.71B at end-2034, $0.47B at "
    "end-2035) and the 2035 hold fails.</li>"
    "<li>fps via Embraer fails the same line: $0.29B at end-2035, peaking at $3.31B in 2037.</li>"
    "<li>So in the stress case only the 10-year ramp keeps the balance sheet repaired. In the base case all three "
    "ramps do.</li></ul>")
SOURCES_CAP = (
    "Independent engine sources fitted to each new narrowbody in production, as Control counts them: the Joint Venture "
    "engine is one source. After 2030 each new narrowbody had three (CFM, GTF2 and UltraFan NB, all ready before entry "
    "into service); the Joint Venture formed in 2035 made it two. Rolls-Royce's own narrowbody development money is the "
    "$8B Solo bill while the Solo stood, then $5.71B: its $4B Joint Venture share plus $1.71B written off at the fold. "
    "The previous game's final state (fps on CFM alone) is scored on the same yardstick.")
OBJ_POINTS = [
    ("The supply enabler changed the one order that changed.",
     "<ul><li>Boeing chose code 7 against its own lean to code 3, because of the enabler, at no cost to its value. "
     "Airbus chose code 7 as in the previous game, now argued through the enabler.</li>"
     "<li>On the previous game's orders Boeing's first enabler line fails: fps on CFM alone, one source in 2040-2050. "
     "Both games keep three narrowbody engine makers.</li></ul>"),
    ("Two sources, not three: the Joint Venture merged them.",
     "<ul><li>After 2030 both new narrowbodies had three independent sources; the 2035 Joint Venture made it two. No "
     "seat in either airframer could have stopped it: the codes were set in 2030, and the Joint Venture needed only "
     "the two engine makers' commitments.</li>"
     "<li>The Boeing Board named the Joint Venture engine \"the single point of fragility\", and P&amp;W's own operating "
     "head agreed: \"One finding hits both fleets at once.\"</li></ul>"),
    ("The balance-sheet objective bound the ramp choice, not the launch.",
     "<ul><li>The analysts' consensus repairs the balance sheet in 2029 on its own. The question the objective asked was "
     "whether a launch undoes it.</li>"
     "<li>The 10-year fps keeps every line in both cases. The 7-year and fps via Embraer fail the stress case; a 787 "
     "Re-engine beside the 10-year would not have (it halved the 2036 stress headroom, to about $1.3B, in Malave's "
     "2035 test).</li>"
     "<li>After 2045 the Board turned to capital returns: a dividend of about $3B a year plus up to $5B of buybacks, "
     "capped at $8B and sized on the stress case. That is a Board matter, not a game order.</li></ul>"),
    ("Rolls-Royce's risk bound lost to the grid, openly.",
     "<ul><li>Every seat priced the breach in 2030, and no seat proposed waiting or an early Joint Venture commitment "
     "(the latter was a red line while P&amp;W's commitment was not public).</li>"
     "<li>From 2035 its Board's rule was \"never cancel or fold for the metric alone\". The 2035 Joint Venture "
     "commitment was taken on the grid (+$2.28B if P&amp;W also committed), not on the metric.</li></ul>"),
    ("The widebody was protected by the grid as much as by the objective.",
     "<ul><li>With the $5B strain in the row, the Trent 1000 upgrade lost $5.87-6.72B against holding and UltraFan WB "
     "$6.96-9.00B in 2035-2050, more than their own $2B and $4B bills. From 2035 Rolls-Royce's CFO withheld her "
     "co-signature on both.</li>"
     "<li>Neither airframer re-engined a widebody, so no widebody engine was ever needed.</li></ul>"),
]

# ─────────────────────────────── market and money ───────────────────────────────
SHARES_LEDE = (
    "<ul><li><b>Narrowbody.</b> As in the previous game: NGSA enters service in 2037 and gains 1 point a year while "
    "alone, taking Airbus to 63% in 2039. fps enters service in 2040 and Boeing recovers 1 point a year to 47% in 2049. "
    "NGSA's three-year lead is kept for good, so Boeing settles at 47% (Airbus 53%). Boeing's projected path never "
    "changed after 2030.</li>"
    "<li><b>Widebody.</b> Untouched: nobody re-engined.</li>"
    "<li><b>Engines.</b> The engine selections set the start: each airframer's narrowbody share is split equally among "
    "the engines fitted to it. With fps and NGSA both open to all three makers, the new narrowbodies start CFM/GE, P&amp;W "
    "and Rolls-Royce level. Each engine programme's move then shifts the split before re-normalising: UltraFan NB +15 "
    "points, GTF2 +10, CFM's ducted engine +10 and the Embraer partnership +5. The Joint Venture puts P&amp;W and "
    "Rolls-Royce level, and the extra share comes from CFM/GE (31.7% in 2045 after 2030, 27.0% after 2035). Until fps enters service in 2040, Boeing's share is the 737 MAX, on CFM alone, so CFM/GE keeps "
    "51.7% in 2037 and 50.5% in 2039. From 2040 it has 27.0%, and the two partners 36.5% each. The GEnx upgrade, ready "
    "in 2033, moves 2.8 points of widebody engines to CFM/GE from 2042, the dashboard's default Re-engine date.</li></ul>")
NB_TITLE = "Narrowbody deliveries: Boeing dips to 37% while NGSA is alone, then settles at 47%, as in the previous game"
BOEING_PATH_TITLE = "Boeing's narrowbody share as projected after each round: no revision after 2030"
WB_TITLE = "Widebody deliveries: unchanged, because neither airframer re-engined"
ENG_NB_TITLE = ("Narrowbody engines: from 2040 the Joint Venture engine flies on both new narrowbodies and its partners "
                "hold 36.5% each; CFM/GE falls to 27%")
ENG_WB_TITLE = "Widebody engines: the GEnx upgrade takes 2.8 points from Rolls-Royce, counted from 2042"

MONEY_LEDE = (
    "<ul><li>The airframers' figures are the previous game's: the engine selection does not enter their payoff. Boeing's "
    "fps bill ($14.91B in PV for $60.32B charged in 2040) and debt penalty ($4.73B) absorb all but $0.66B of its "
    "+$20.30B narrowbody gain. Airbus's NGSA bill ($15.23B in PV) and debt penalty ($0.53B) leave it +$23.37B of a "
    "+$39.13B gain.</li>"
    "<li>Engine value is the lifetime value of the engines each maker delivers. Rolls-Royce's rises from $4.39B a year "
    "in 2036 to $11.82B in 2037 (NGSA) and $16.63B in 2040 (fps). CFM/GE's is $12.22B in 2040, against $28.11B in the "
    "status quo: in 2040 it delivers 1,079 narrowbody engines against 3,040. P&amp;W's is $11.84B against $7.78B, "
    "on 1,460 engines against 960.</li>"
    "<li>Engine R&amp;D and write-offs are undiscounted, as on the dashboard: CFM/GE $4B for the ducted engine plus $2B "
    "of strain for three live programmes; P&amp;W $2B and Rolls-Royce $4B, their Joint Venture shares; and Rolls-Royce's "
    "$1.71B write-off when its Solo folded into the Joint Venture.</li></ul>")
MONEY_TITLES = {
    "boeing": "Boeing operating profit: just below the status quo in 2037-39, then $7.65B a year above it from 2040, rising to $10.18B",
    "airbus": ("Airbus operating profit: $9.43B a year above the status quo in 2037, peaking at $10.01B in 2039, then "
               "easing to $7.12B as fps gains share"),
    "cfm": "CFM/GE engine value: $7.37B below the status quo in 2037, $15.89B below in 2040 and $24.21B below by 2060",
    "pratt_whitney": "P&W engine value: just above the status quo in 2037-39 (NGSA), then $4.06B above it in 2040 (fps) and $6.27B by 2060",
    "rolls_royce": "Rolls-Royce engine value: $7.33B above the status quo in 2037, $11.84B in 2040 and $17.94B by 2060",
}

TIMELINE_LEDE = (
    "The same programmes and dates as the previous game. Every programme but one was launched in 2030; the Joint Venture "
    "was launched in 2035, and nothing was cancelled outright. NGSA enters service in 2037 and fps in 2040. P&amp;W's "
    "GTF2 and Rolls-Royce's UltraFan NB, each launched once an airframer selected its maker, folded into the Joint "
    "Venture in 2035. It inherits GTF2's schedule and is ready in 2036; a fresh Joint Venture would have been ready only "
    "in 2041. CFM/GE's ducted engine (ready 2036) and Embraer partnership (2037) count from 2037, NGSA's entry into "
    "service. Its GEnx upgrade, ready in 2033, counts only from 2042, the dashboard's default Re-engine date.")

# ─────────────────────────────── the analyst models ───────────────────────────────
ANALYST_LEDE = (
    "Before this game each company's profile gained a note on the July-August 2026 analyst models: Morgan Stanley and "
    "Goldman Sachs company models, and S&amp;P Capital IQ consensus where the files had it. The notes are real-world "
    "context; the dashboard's numbers still set every payoff. Two things come from them directly: Boeing's net-debt "
    "tracker (start, free cash flow, historical level) and the stress case, set from the spread of estimates and "
    "Boeing's record. Below, what the models say, and how their implications for each company's decisions compare with "
    "what the agents then did.")
ANALYST_TABLE = [
    ("Boeing", "Net debt $22.53B at end-2026 (consensus mean, 5 estimates); GS $22.55B, MS $23.01B. Mid-2026 gross debt $45.9B.",
     "Consensus 'Net Debt'; GS BA BS r63-r64; MS BA Balance_Sheet_Annual"),
    ("Boeing", "Consensus free cash flow 2027-2030: $5.67B, $9.86B, $13.03B, $15.04B ($45.8B over 2026-2030). Free cash flow "
     "was negative in five of the seven years 2019-2025.", "Consensus 'Free Cash Flow'; MS BA Cash_Flow_Annual r77"),
    ("Boeing", "Net debt averaged about −$0.6B in 2010-2018, a small net cash; the objective's historical level is $0, rounded from it.",
     "GS BA BS r64"),
    ("Boeing", "The brokers split on capital allocation: GS buys back $42B in 2027-2030 and ends 2030 with $17.4B of net debt; "
     "MS buys back none and ends with $16.2B of net cash. No new airplane is in any forecast.",
     "GS BA CFLO r45, BS r64; MS BA Balance_Sheet_Annual 'Net Debt'"),
    ("Airbus", "Net cash in every year from 2010A to 2030E; about EUR 31.8-33.1bn in 2030E, with free cash flow above "
     "EUR 10bn. Neither model includes an A320 successor.", "MS CFS r86, r61; GS Balance Sheet r65; MS Airbus r38"),
    ("CFM/GE", "The 737 MAX is 100% CFM; CFM holds 52-59% of the A320neo family against the GTF (2025A). GS GE has LEAP "
     "deliveries falling to 1,000 by 2040E with no successor.", "MS GE CES Annual_Driver r51; GS SAF Propulsion r34; MS SAF Civil OE r184; GS GE Revenue build r9"),
    ("CFM/GE", "The aftermarket carried 75% of GE CES revenue in 2025A; GE returns about 94-124% of free cash flow.",
     "MS GE CES_Annual r53; MS GE Cash_Flow_Annual r96"),
    ("P&amp;W", "On the GS legacy model the GTF loses money on every new engine sold and turns net positive only in 2028E. The "
     "2023 durability precedent cost $5.4bn of sales.", "GS RTX GTF Analysis r14, r24; MS RTX P&W_Annual r29"),
    ("P&amp;W", "RTX net debt is below 1x EBITDA by 2030E; $10-16bn is left after shareholder returns over 2026E-2030E.",
     "MS RTX Balance_Sheet_Annual r82; GS RTX BS r80; calc. from MS RTX Cash_Flow_Annual r72/r40/r41 and GS RTX CFLO r47/r34/r35"),
    ("Rolls-Royce", "About half of group profit rests on widebody; 85% of Trent deliveries in 2025A were for airframes with no "
     "rival engine. Company-funded R&amp;D is only £0.6-0.9bn a year to 2030E.", "MS Civil r14, Civil OE r82-r87; MS IS r129"),
    ("Rolls-Royce", "Neither bank models a Rolls-Royce narrowbody engine (GS narrowbody units zero to 2031E). The Trent ramp "
     "cost about £3.0bn of new-engine losses over nine years.", "GS Civil Aerospace r61; MS Civil OE r52"),
]
ANALYST_CAP = (
    "From the analyst note in each company's profile folder (analyst_models_2026.md), each checked against the "
    "extracted model files. MS = Morgan Stanley, GS = Goldman Sachs; A = actual, E = estimate. Money "
    "is nominal in the reporting currency. The tracker's validation: with base cash flow only it gives Boeing net debt of "
    "$16.49B at end-2027 and $6.70B at end-2028 in 2026 dollars, against consensus $16.57B and $6.90B.")
ANALYST_POINTS = [
    ("Boeing: the analysts' cash flow decided the debt objective before the game did.",
     "<ul><li>The tracker reproduces consensus net debt within $0.2B and reaches zero in 2029 with no new programme. "
     "The fps then competes with returns to owners, not with debt repair, as the note predicted: \"Under debt first, "
     "programme money after 2029 comes out of what would otherwise go to owners.\" (GS models $42B of buybacks in "
     "2027-2030.)</li>"
     "<li>\"A launch in the 2030 round mostly tests the hold years\", the note said, and it did: the 7-year ramp "
     "failed the stress case at the 2035 hold year, not the 2030 deadline. The 10-year's later, lower spending "
     "passed.</li>"
     "<li>The note flagged engine selection as \"a supply-risk choice the models do not price\". Boeing took it as one, "
     "on the enabler.</li></ul>"),
    ("Airbus: money was not the limit, as the note said, but its own cash line was.",
     "<ul><li>The banks show net cash above EUR 31bn in 2030E. Airbus's agents measured NGSA against one year's free "
     "cash flow instead: $5.07B a year against a $5.2B line, 97% used. That line, with its other rules, kept the A350 "
     "Re-engine and Delay Tactics out in 2030 and 2035.</li>"
     "<li>\"Keep two sources if the board allows it\": NGSA flies two.</li></ul>"),
    ("CFM/GE: the note named its biggest risk, and half of it came true: Boeing's slot was shared, not lost.",
     "<ul><li>\"Losing a new Boeing narrowbody to a rival, including a Pratt &amp; Whitney and Rolls-Royce Joint "
     "Venture, costs more than losing an Airbus slot.\" Sharing fps cost CFM/GE $31.40B against the previous game.</li>"
     "<li>\"A Ducted launch is the defence if a rival engine is selected\": it was launched in 2030 and is worth 10 "
     "points before re-normalising, but it could not undo selections sealed in the same round.</li></ul>"),
    ("P&amp;W: launch against a committed airframer, and share the risk.",
     "<ul><li>The note's advice, prefer \"launch only if an airframer selects P&amp;W\" and a Joint Venture to share "
     "new-engine losses, is exactly what P&amp;W did.</li>"
     "<li>Its durability precedent ($5.4bn of sales in 2023) is the risk Boeing now names in public. P&amp;W answered "
     "\"with product and data, not price\".</li></ul>"),
    ("Rolls-Royce: the note's two warnings split.",
     "<ul><li>\"Do not stack projects in the 2030 round\": kept. No widebody programme was ever on the record.</li>"
     "<li>\"An UltraFan narrowbody Solo launch repeats the Trent ramp at bigger volume\" and \"The Joint Venture fits "
     "the R&amp;D budget better\": the conditional Solo it chose cost $1.71B more than its Joint Venture share.</li>"
     "</ul>"),
]

# ─────────────────────────────── how they decided ───────────────────────────────
GOV_LEDE = (
    "<b>As in the previous game, the chain never needed its later steps: no binding veto at the veto check, red-line "
    "flag, revision, Board veto or reversion in 20 company-rounds.</b> "
    "Each company ran the same chain every round. The Board gave guidance. The CEO framed the choice, and the CFO and "
    "operating head tested the options independently. The CEO decided; the CFO and operating head then ran a veto "
    "check on that decision, and the CEO could revise once. Any order other than hold then went to the Board, with one "
    "more revision and a reversion to the default if a Board veto stood. "
    "In their test memos the CFO and operating head could mark any option a veto, some binding; the CEOs treated the "
    "binding ones as ruling those options out before choosing. Control's objectives entered every step: each Board's "
    "guidance, the CFOs' tests (Boeing's debt line, Rolls-Royce's $4B line) and each CEO's objective note. Names below "
    "are the agents profiled on those executives, not the people.")

GOV_POINTS = [
    ("The Boards wrote Control's objectives into their limits.",
     "<ul><li><b>Boeing:</b> \"net debt must reach $0 by end-2030 and stay there, stress case included\", and code 7 "
     "for the enabler \"at no cost to Boeing's payoff\". It offered to approve the 10-year ramp, against its own "
     "worst-column preference, if the $0.46B was logged as objective premium.</li>"
     "<li><b>Airbus:</b> \"A stable engine supply\" as a priority, code 7 preferred, \"the Board never vetoes a "
     "code\".</li>"
     "<li><b>Rolls-Royce:</b> it would accept the $8B against $4B \"only because the trigger is a selection\", and kept "
     "every widebody programme off the record: \"Any widebody programme now carries $5B for good.\"</li>"
     "<li><b>CFM/GE and P&amp;W</b> had no added objective. Their Boards' limits were the previous game's.</li></ul>"),
    ("No seat said an objective changed an order, except Boeing's CEO on the engine code.",
     "<ul><li>Every company logged its objective premium. Boeing: $0.46B in 2030, half of it for the stress-case debt "
     "line. Rolls-Royce declined the $8.31B it would have cost to stay inside its bound. Airbus and CFM/GE paid nothing "
     "for objectives.</li>"
     "<li>Doctrine premiums, logged separately: Boeing $0.65B (2035) and $0.05B (2050); Airbus $0.89B (2045) and $0.57B "
     "(2050) for holding the A350 Re-engine; P&amp;W $0.26B (2030) for launching only on selection.</li></ul>"),
    ("The ExCos agreed at the decision; their binding vetoes fell on the options left out.",
     "<ul><li>The memos marked 60 vetoes binding (Airbus 22, CFM/GE 16, Rolls-Royce 11, P&amp;W 8, Boeing 3), all on "
     "options the CEO did not choose. The previous game had 58.</li>"
     "<li>Failed tests on chosen orders were advice: Rolls-Royce's CFO failed its own $4B line on the conditional "
     "launch (and, later, on the hold that kept it) and an R&amp;D-envelope test; CFM/GE's CFO flagged a \"second stack "
     "of projects\" on its 2030 package.</li></ul>"),
    ("The Boards' advice that was not taken was about words, not orders.",
     "<ul><li>The CEOs answered 140 Board recommendations. Boeing's ramp was the one order where the CEO took the "
     "Board's stated alternative, not its preference.</li>"
     "<li>Airbus's Board asked to soften \"the same will apply to its successor\" on engine choice to \"we intend to offer "
     "a choice of engines\"; the 2030 statement kept the old line, and Faury adopted the new one in 2035.</li>"
     "<li>P&amp;W's CEO recorded in 2045 that a 2035 Board wording change to the Joint Venture statement \"was not taken "
     "up\".</li></ul>"),
    ("Boeing's public sourcing line drew answers, not concessions.",
     "<ul><li>In 2045 Boeing said: \"If the Joint Venture engine stumbles, the fps is back on CFM alone. Any durability "
     "finding is a live problem, and I would then want a third source.\"</li>"
     "<li>P&amp;W's Board: \"Do not answer Boeing's 'third source' remark with a concession.\" Calio: \"fair, and it is "
     "the right test\", answered with fleet data.</li>"
     "<li>CFM/GE's Board: \"That is not ours to chase with terms.\" Culp offered durability data with no commercial "
     "term \"to keep or win a source position\".</li></ul>"),
]

ROUNDS = {
    1: {"title": "2030: both new narrowbodies launch, open to all three engine makers; Rolls-Royce states its breach",
        "lede": ("<ul><li><b>Boeing</b> lifted its rule against a first-round launch: by its CEO's reading the 777X and "
                 "MAX 7/10 were done, and the tracker showed net debt at zero in 2029 with no new programme. It launched fps on the 10-year "
                 "ramp, open to all three engine makers for Control's enabler. Its Board preferred the 7-year but "
                 "approved the 10-year for the stress-case debt line. No rate increase and no 787 Re-engine.</li>"
                 "<li><b>Airbus</b> launched NGSA for 2037, again open to all three makers, now argued as the only route "
                 "to three sources. No A350 Re-engine and no Delay Tactics.</li>"
                 "<li><b>P&amp;W and Rolls-Royce</b> ordered launches conditional on selection, and both airframers "
                 "selected both. Rolls-Royce stated in advance that a selection breaches Control's $4B bound.</li>"
                 "<li><b>CFM/GE</b> launched the ducted engine, the Embraer partnership and the GEnx upgrade, as before.</li>"
                 "<li>The Boards approved all seven orders put to them.</li></ul>")},
    2: {"title": "2035: the Joint Venture forms, and three engine sources become two",
        "lede": ("<ul><li><b>P&amp;W and Rolls-Royce</b> both committed to the Joint Venture on sealed orders. Both solo "
                 "programmes folded into it; it inherits GTF2's schedule and is ready in 2036. Rolls-Royce writes off "
                 "$1.71B, and its own narrowbody money settles at $5.71B.</li>"
                 "<li>Both new narrowbodies now count two engine sources, CFM and the Joint Venture engine; CFM/GE's "
                 "narrowbody share from 2040 falls from 31.7% to 27.0%.</li>"
                 "<li><b>CFM/GE</b> learned the fps selection from this round's brief and held everything: nothing on its "
                 "menu could change an engine code.</li>"
                 "<li><b>Airbus</b> left poaching out (over its cash line, and its stricter condition); <b>Boeing</b> held "
                 "the 787 Re-engine on its overlap rule. Both kept code 7.</li></ul>")},
    3: {"title": "2045: everyone holds; neither airframer re-engines its widebody",
        "lede": ("<ul><li>Both new narrowbodies are in service. The live levers were the Re-engines, the Open Fan and "
                 "Rolls-Royce's widebody engines, and every company held.</li>"
                 "<li><b>Airbus:</b> the A350 Re-engine was worth +$0.89B if Boeing held, under its $1B bar, and no "
                 "widebody engine would be ready for it.</li>"
                 "<li><b>Boeing:</b> its Board would have vetoed the 787 Re-engine on its business case: +$0.30B if "
                 "Airbus held, −$1.26B if Airbus re-engined too. The enabler is met at two sources, \"not the three we "
                 "planned\".</li>"
                 "<li><b>Rolls-Royce:</b> both widebody programmes carried the $5B strain beside the Joint Venture.</li></ul>")},
    4: {"title": "2050: everyone holds again, and the final state is the 2035 state",
        "lede": ("Every company held, and no value has changed since 2035. A Re-engine ordered in 2050 would enter "
                 "service only in 2055. Airbus's A350 Re-engine was worth +$0.57B if Boeing held and −$0.41B if not; "
                 "Boeing's 787 Re-engine +$0.05B or −$1.00B. Boeing's Board turned to capital returns sized on the "
                 "stress case.")},
}

PLAY_LEDE = (
    "The airframers' play and its regret are the previous game's: the engine selection does not enter their payoff. "
    "Their regret is in the widebody Re-engines and, for Airbus, the Delay Tactics it did not order. Rolls-Royce's is "
    "its fold-in write-off. CFM/GE's and P&amp;W's orders were the best reply in every round. The table also shows "
    "Control's objectives for each best alternative.")

PLAY_POINTS = [
    ("The played outcome is on none of the snapshot's equilibrium lists, as before.",
     "<ul><li>Your snapshot's four Pure Nash all pair fps on the 10-year ramp with NGSA plus one Delay Tactics move, "
     "with one airframer re-engining. The game's cell, with no Delay Tactics and no Re-engine, is neither Pure nor "
     "Near-Nash.</li>"
     "<li>In each round's stage game the two pure equilibria have one airframer re-engine and the other hold: Chicken "
     "on the widebody through 2050. Both holding was within $1B of each side's best reply only in 2045 and 2050.</li></ul>"),
    ("Regret: Airbus gave up most, $3.30B in 2030; none of the best alternatives changes an objective result except "
     "Rolls-Royce's.",
     "<ul><li><b>Boeing:</b> $2.20B in 2030, falling to $0.04B in 2050, all from the 787 Re-engine. With the 10-year "
     "ramp it keeps every debt line and the enabler, so Control's objectives would not have stopped it; the "
     "one-development-at-a-time rule and the Board's downside test did.</li>"
     "<li><b>Airbus:</b> $3.30B in 2030 and $3.19B in 2035 (one Delay Tactics move and the A350 Re-engine), then $0.89B "
     "and $0.57B. Its objective results would have been the same.</li>"
     "<li><b>Rolls-Royce:</b> $1.71B in 2030, exactly its fold-in write-off. Holding UltraFan NB in 2030 and joining in "
     "2035 would have brought the same Joint Venture without it, and met all four objectives. Valued as if nobody moved "
     "afterwards, the conditional launch was its best order (no myopic regret).</li></ul>"),
    ("Calibration: the 2030 grids missed the engine selections.",
     "<ul><li>Airbus expected +$45.82B in 2030, in the case where Boeing held fps; it got +$23.37B. Boeing expected "
     "−$1.96B, in the case where Airbus also re-engined the A350; it got +$0.66B.</li>"
     "<li>The engine makers' 2030 cases rarely had both airframers selecting all three makers. CFM/GE expected −$21B "
     "(NGSA on CFM and P&amp;W only) and got −$62.61B; Rolls-Royce +$8.31B (weighted) against +$30.07B; P&amp;W +$0.23B "
     "against +$3.37B.</li>"
     "<li>In 2035 P&amp;W and Rolls-Royce again weighted the other's Joint Venture commitment low (0.10 or less): P&amp;W "
     "expected +$0.39B and got +$8.88B. Calio: \"In a sealed, simultaneous round, Rolls-Royce's conditional commit was as "
     "free and as dominant for it as ours was for us.\" From 2045 every company was within $1.31B.</li></ul>"),
    ("All 20 company-rounds kept to their own information.",
     "<ul><li>An audit of every tool call found all 20 company-rounds clean: no company reached another's material, "
     "the dashboard or the game master's files.</li>"
     "<li>Each company's chain ran as its own workflow, in parallel, in every round, and nothing passed between "
     "companies.</li></ul>"),
]

# ─────────────────────────────── against the previous game ───────────────────────────────
COMPARE_LEDE = (
    "<b>One order differs, Boeing's fps engine selection in 2030, and it moves the engine makers' values by $31.40B "
    "(CFM/GE) and about $11.8B each (P&amp;W and Rolls-Royce).</b> Both games used the same dashboard (combined_dash.py "
    "at the Game_v3.txt snapshot), the same twenty agents, the same rules and the same four decision years. This game "
    "added Control's objectives, the GM's net-debt tracker and the 2026 analyst notes to the companies' files. Each "
    "company's decision record shows why its orders matched or differed.")

COMPARE_POINTS = [
    ("One order differs.",
     "<ul><li>Boeing's fps engine selection: CFM alone (code 3) in the previous game, all three makers (code 7) here. "
     "Ortberg's lean was code 3 in both games; the enabler moved it.</li>"
     "<li>Every other order in all 20 company-rounds is the same, including Boeing's 10-year ramp, both Joint Venture "
     "commitments and every hold.</li></ul>"),
    ("Same orders, different reasons.",
     "<ul><li><b>Boeing's ramp:</b> in the previous game the $0.46B was a doctrine premium and the Board's 7-year "
     "advice was \"Not taken\". Here the Board offered the 10-year as an approved alternative for the stress-case debt "
     "line, and Ortberg split the premium into doctrine and objective parts.</li>"
     "<li><b>Airbus's code 7:</b> previously \"supply certainty and customer choice\"; here \"the enabler "
     "trap\".</li>"
     "<li><b>Rolls-Royce's 2030 launch:</b> the same order, now with the $4B breach priced and stated.</li></ul>"),
    ("The engine makers' values move with one selection.",
     "<ul><li>P&amp;W +$11.81B and Rolls-Royce +$11.80B: from 2040 fps is split among all three makers, with the Joint "
     "Venture engine beside CFM, where before it was all CFM. CFM/GE −$31.40B.</li>"
     "<li>The three engine makers together are $7.79B worse off, so the change is not a pure transfer (inference: the "
     "makers' discount rates and lifecycle values differ).</li>"
     "<li>The airframers' values are identical to the cent.</li></ul>"),
    ("On Control's yardstick, the previous game's orders score one objective lower.",
     "<ul><li>Boeing's first enabler line fails there (fps on CFM alone, one source); every other added objective "
     "scores the same, including Rolls-Royce's $5.71B breach and Boeing's repaired balance sheet.</li>"
     "<li>Among the base objectives, CFM/GE's narrowbody dominance flips: met there (51.1% at worst), missed here "
     "(27.0%). P&amp;W's ΔPV objective flips the other way: missed there (−$2.93B), met here (+$8.88B).</li></ul>"),
]

FOOTER = ("BOEING PROPRIETARY. Built from the dash-2050-obj game record (wargame/runs/dash-2050-obj; record/ here) by "
          "wargame/dashgame/reports.py and wargame/reports/dash-2050-obj/make_game_html.py. Dashboard: combined_dash.py "
          "at the Game_v3.txt snapshot. Previous game: wargame/reports/dash-2050-exco.")

METHOD = """
<h3>How the game was run</h3>
<ul class="cav">
<li><b>A replay.</b> The previous ExCo-and-Board game (run dash-2050-exco) replayed from the start in a fresh run,
dash-2050-obj: the same dashboard, agents, rules and decision years. Three things were added to the companies' files
before 2030, and nothing else changed.
<ul>
<li><b>Control's objectives</b> (listed under Control's objectives), in each company's private brief with its metrics
for every plan on the payoff grid. Boeing's brief also carried its net-debt path, base and stress, and a table of the
engine sources each engine code would give.</li>
<li><b>The GM's balance-sheet tracker</b> for Boeing (below).</li>
<li><b>The analyst notes</b>: a note per company on the July-August 2026 Morgan Stanley and Goldman Sachs models and,
for Boeing, Capital IQ consensus, each checked against the extracted model files. The notes are context; the dashboard
sets every payoff.</li>
</ul></li>
<li><b>Dashboard.</b> Your combined_dash.py, run headless (never in Streamlit) at the Game_v3.txt snapshot. Solved by
the game master (GM), it reproduces the snapshot: airframers 4 Pure Nash and 12 Near-Nash, engines 1 Pure Nash and 11
Near-Nash.</li>
<li><b>Players.</b> 20 AI agents. In each company, the CEO, CFO and operating head of the default 2026 executive
committee, each profiled from that person's own public words, and the Board, profiled from transcripts, filings and web
search, with a culture score. Where an executive's record was thin, the seat's tests were derived from the role or
company doctrine and labelled low confidence (Pope, Toepfer, Wagner). They are AI agents, not the people.</li>
<li><b>Each round, in each company.</b> The Board gives guidance; the CEO frames the choice; the CFO and operating
head test it independently; the CEO decides; the CFO and operating head run a veto check, and the CEO revises once if
a binding veto or red-line flag stands; each Board item goes to Board review, with one more revision and a reversion
to the default if a Board veto stands. Each company's chain ran as its own workflow, in parallel; nothing passed
between companies.</li>
<li><b>Information.</b> The public bulletin plus a private brief per company. Only the GM saw the dashboard and the
other companies' briefs. The isolation hook denies other companies' files and briefs, the dashboard, the snapshot, GM
code, earlier reports and runs, and the GM's scratch files. An audit of every tool call found all 20 company-rounds
clean.</li>
<li><b>Rounds.</b> Four sealed, simultaneous rounds: 2030, 2035, 2045, 2050. Each round's value is the GM valuation of
the state after that round, assuming nobody moves again. The final round's value is the game outcome.</li>
</ul>
<h3>How Control's objectives are scored</h3>
<ul class="cav">
<li><b>They never change a payoff.</b> The dashboard's ΔPV, including its own debt penalty on $45B of debt, is
untouched. A company could give up value for an objective only within its premium cap, and had to log it.</li>
<li><b>Boeing's net debt</b> (total debt less cash and short-term investments) at year end, in 2026 dollars. Start:
$22.53B at end-2026, the consensus mean. Base free cash flow: consensus for 2027-2030 ($5.67B, $9.86B, $13.03B,
$15.04B nominal), deflated at the dashboard's 2.2% CPI, then flat at $13.79B; the stress case is one-third lower. Each
year: free cash flow = base + 79% of (the game's profit change against its baseline − programme cash) − 3% real
interest on any debt the game adds; net debt = last year's in today's money − free cash flow, never below the
historical level once there (surplus goes to owners). Programme cash: each bill spread over its development years on
a standard curve (5% in year 1 of 10, peaking at 14% in year 7), plus the two-front strain over the fps and 787
Re-engine overlap; the 737 rate increase spent evenly to 2032. Profits count from the first decision year, as played.
Historical level $0, rounded from the 2010-2018 average of −$0.6B.</li>
<li><b>Engine sources.</b> The independent engine sources fitted to a new narrowbody in production in 2040, 2045 and
2050: CFM, P&amp;W's GTF2, Rolls-Royce's UltraFan NB, or the P&amp;W-Rolls-Royce Joint Venture engine, which counts as
one. Engine makers in the market: those with narrowbody share above zero in 2045 and 2050.</li>
<li><b>Rolls-Royce's own narrowbody money:</b> $8B for UltraFan NB Solo, $4B for its Joint Venture share; a Solo
cancelled or folded counts its spend to date. Strain: the dashboard's one-off $5B whenever a narrowbody and a widebody
engine programme are both on the record.</li>
</ul>
<h3>Rules the GM added to the static dashboard (as in the previous game)</h3>
<ul class="cav">
<li><b>Time.</b> A programme enters service, or an engine is ready, after its development time from the decision year:
fps 7 or 10 years, fps via Embraer 10, NGSA 7, Re-engines 5; ducted 6, GTF2 6, UltraFan NB 7, UltraFan WB 6, Trent and
GEnx upgrades 3, the Embraer partnership 7, the Joint Venture 6 or an inherited schedule; Open Fan 10, never before
2045.</li>
<li><b>Cancellations</b> write off the bill × years elapsed ÷ development years. <b>Delay Tactics</b> are covert; none
was ordered.</li>
<li><b>Engines.</b> The dashboard's engine game is applied year by year, splitting each airframer's narrowbody share
equally among the engines fitted to it. Each narrowbody engine move counts from the later of its ready year and the
first new narrowbody's entry into service (2037 here); widebody engine upgrades count from the first Re-engine's entry
into service, or 2042.</li>
<li><b>Joint Venture.</b> It forms when both makers commit. It folds in solo programmes, writing off spend beyond each
maker's share, and inherits the most advanced folded schedule. A Joint Venture formed after an airframe's entry into
service does not rewrite the engines fitted before it (a check added for this game).</li>
<li><b>Tests.</b> Dashboard reproduction, the engine move combinations and the snapshot equilibria; both games replay
exactly, and no played year changes; the isolation tests.</li>
</ul>
<h3>What the numbers are</h3>
<ul class="cav">
<li><b>ΔPV and yield.</b> ΔPV is the change in present value at 2026 against the status quo (nobody launches
anything), at each company's dashboard WACC. Yield = 100 + 100 × ΔPV ÷ enterprise value.</li>
<li><b>Dashboard conventions.</b> Airframe programme spend is charged in full at entry into service. Engine R&amp;D is
undiscounted. Engine value is the lifetime value per engine delivered.</li>
<li><b>Regret.</b> The final ΔPV a company would have had with its best alternative orders in that round, holding every
other order in the game as played (later rounds re-run), minus its actual final ΔPV.</li>
<li><b>S1, S2, ….</b> The scenario columns of each company's own payoff grid in that round's brief; they differ by
company and round. Ids in brackets, such as [BX-1239], are the agents' evidence citations. "(inference)" marks a
reading of the record that no single number states.</li>
<li><b>Your dashboard alone.</b> The table below sets each final value next to your dashboard alone. The airframers
match exactly. For the engine makers the dashboard fixes a 50/50 airframer split and locks P&amp;W to GTF2 Solo; the
GM's Joint Venture and year-by-year split account for the difference.</li>
</ul>
"""

# Plain text (the HTML builder escapes it): why the GM's final value differs from the dashboard alone.
BOARD_WHY = {
    "boeing": "No difference. The airframer values are your dashboard's own, at the game's dates.",
    "airbus": "No difference. The airframer values are your dashboard's own, at the game's dates.",
    "cfm": ("Dashboard alone −$71.07B. Both partners' Joint Venture moves −$7.09B: the dashboard locks P&W to GTF2 Solo "
            "for the engine selections, so there only Rolls-Royce's Joint Venture move applies. The year-by-year split "
            "+$8.46B: until fps enters service in 2040, Boeing's narrowbody share is the CFM-only 737 MAX, where the "
            "dashboard splits both airframers three ways from 2037."),
    "pratt_whitney": "Dashboard alone +$9.71B. Both Joint Venture moves +$2.75B. The year-by-year split −$3.59B.",
    "rolls_royce": ("Dashboard alone +$34.91B. The fold-in write-off −$1.71B. Both Joint Venture moves +$2.75B. The "
                    "year-by-year split −$3.59B."),
}

# Headline numbers the builder checks against data/report_data.json: (description, round index, player, field, value)
CHECKS = [
    ("final ΔPV", -1, "boeing", "pv_delta", 0.66), ("final ΔPV", -1, "airbus", "pv_delta", 23.37),
    ("final ΔPV", -1, "cfm", "pv_delta", -69.69), ("final ΔPV", -1, "pratt_whitney", "pv_delta", 8.88),
    ("final ΔPV", -1, "rolls_royce", "pv_delta", 32.35),
    ("round-1 ΔPV", 0, "boeing", "pv_delta", 0.66), ("round-1 ΔPV", 0, "airbus", "pv_delta", 23.37),
    ("round-1 ΔPV", 0, "cfm", "pv_delta", -62.61), ("round-1 ΔPV", 0, "pratt_whitney", "pv_delta", 3.37),
    ("round-1 ΔPV", 0, "rolls_royce", "pv_delta", 30.07),
    ("round-2 ΔPV", 1, "cfm", "pv_delta", -69.69), ("round-2 ΔPV", 1, "pratt_whitney", "pv_delta", 8.88),
    ("round-2 ΔPV", 1, "rolls_royce", "pv_delta", 32.35),
    ("final yield", -1, "rolls_royce", "yield", 129.41), ("final yield", -1, "cfm", "yield", 56.44),
]
# Shares quoted above, checked against the final round's years at the printed precision: (side, key, year, value)
SHARE_CHECKS = [
    ("boeing", "nb_share", 2032, .4), ("boeing", "nb_share", 2036, .4), ("boeing", "nb_share", 2039, .37),
    ("boeing", "nb_share", 2040, .38), ("boeing", "nb_share", 2045, .43), ("boeing", "nb_share", 2049, .47),
    ("boeing", "nb_share", 2050, .47), ("boeing", "nb_share", 2056, .47),
    ("airbus", "nb_share", 2039, .63), ("airbus", "nb_share", 2050, .53),
    ("cfm", "nb_share", 2036, .76), ("cfm", "nb_share", 2037, .517), ("cfm", "nb_share", 2039, .505),
    ("cfm", "nb_share", 2040, .270), ("cfm", "nb_share", 2050, .270),
    ("pratt_whitney", "nb_share", 2037, .241), ("pratt_whitney", "nb_share", 2040, .365), ("pratt_whitney", "nb_share", 2050, .365),
    ("rolls_royce", "nb_share", 2036, 0.0), ("rolls_royce", "nb_share", 2037, .241), ("rolls_royce", "nb_share", 2040, .365),
    ("rolls_royce", "nb_share", 2050, .365),
    ("rolls_royce", "wb_share", 2041, .58), ("rolls_royce", "wb_share", 2042, .552), ("rolls_royce", "wb_share", 2050, .552),
    ("cfm", "wb_share", 2041, .42), ("cfm", "wb_share", 2042, .448),
]
