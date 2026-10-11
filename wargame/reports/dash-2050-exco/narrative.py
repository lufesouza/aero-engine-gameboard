"""Narrative for the dash-2050-exco page and report. Every number here is from data/report_data.json, data/crossvalue.json,
the round grids and briefs (record/grids_rN.json, record/brief_rN_<side>.md, as shown to each company) or the companies'
own decision chains (record/exco_result_rN.json); make_game_html.py checks the headline numbers against the data when it
builds (see CHECKS and SHARE_CHECKS). Titles, tiles and chart titles are plain text (the builders escape them); the
other strings are HTML. "The dashboard" is the game-theory model (combined_dash.py); "Board" is always a company's
Board."""

TITLE = ("Airbus wins on value as NGSA leads fps by three years; Boeing settles at 47% of narrowbodies, and no veto "
         "overturns a CEO's decision")

LEDE = (
    "<b>Airbus won on value (ΔPV +$23.37B, against Boeing's +$0.66B). Rolls-Royce had the best yield (118.68%, "
    "ΔPV +$20.55B). CFM/GE lost most (−$38.29B); Pratt &amp; Whitney (P&amp;W) ended at −$2.93B.</b> "
    "Why: Boeing launched fps in 2030 on the 10-year ramp-up, where its Board had recommended the 7-year, so NGSA (in "
    "service 2037) leads fps (2040) by three years, and Boeing settles at 47% of narrowbody deliveries from 2049. "
    "In 2035 P&amp;W and Rolls-Royce formed a Joint Venture, on conditions both their Boards had set in 2030; it cost "
    "CFM/GE $7.09B. "
    "Twenty AI agents played four sealed rounds (2030, 2035, 2045 and 2050) on your dashboard, each company as an "
    "executive committee (ExCo) of CEO, CFO and operating head under a Board agent. "
    "No veto overturned a CEO's decision, and the Boards approved all nine orders put to them. The limits came earlier: "
    "each Board named in advance the orders it would veto, and no CEO ordered one; the CFOs' and operating heads' binding "
    "vetoes (58 in their test memos) struck options before the CEOs chose. Whether those limits "
    "changed any choice is not observed: every final order was the CEO's opening lean.")

FINDINGS = [
    ("Boeing took the 10-year ramp-up against its Board's advice, and NGSA leads by three years.",
     " On the dashboard the two ramps were $0.46B apart in Boeing's expected case, which was also its worst (Airbus "
     "re-engining the A350 beside NGSA): inside the $1B margin its rules treat as a tie. Where Airbus held, the 10-year "
     "led by $1.30B. The CEO chose on his stated preferences.<ul>"
     "<li>The Boeing Board recommended the 7-year ramp for its better worst case (−$1.50B against −$1.96B if Airbus "
     "re-engined the A350 beside NGSA), but said it would approve either.</li>"
     "<li>The CEO agent, profiled on Kelly Ortberg, chose the 10-year: a bill $4.68B smaller ($60.32B against $65.00B) "
     "and about $6.0B a year of spend against $9.3B. He logged the $0.46B he gave up as a premium paid for that "
     "preference. His CFO (Jay Malave) and operating head (Stephanie Pope) recommended the same, and the Board approved "
     "his reasons.</li>"
     "<li>Malave's own worst-column test preferred the 7-year, as the Board did. He set it aside on \"balance sheet "
     "first\", recommended the 10-year, and \"would not veto the 7-year\".</li>"
     "<li>fps enters service in 2040, three years after NGSA. Boeing falls from 40% of narrowbody deliveries to 37% in "
     "2039 while NGSA is alone. It then gains 1 point a year, from 38% in 2040 to 47% in 2049. On the dashboard the "
     "first in service keeps its lead for good.</li>"
     "<li>Airbus launched NGSA with no A350 Re-engine and no Delay Tactics, the case that came true. There the 7-year "
     "ramp was worth +$1.12B to Boeing against +$0.66B, so the $0.46B premium was the real cost. The CEO and the Board "
     "had also recorded the share cost when choosing: Boeing below 40% for some years, and its incumbency objective "
     "missed.</li></ul>"),
    ("Airbus finishes far ahead: its gain comes earlier and is discounted less, and its debt penalty is far smaller.",
     "<ul><li>In PV the narrowbody gain is +$39.13B for Airbus and +$20.30B for Boeing. Airbus's starts in 2037, at an "
     "8% discount rate; Boeing's starts in 2040, at 10.5%.</li>"
     "<li>The fps bill ($14.91B in PV) and the debt penalty ($4.73B) leave Boeing +$0.66B. NGSA's bill ($15.23B in PV) "
     "and debt penalty ($0.53B) leave Airbus +$23.37B.</li>"
     "<li>In nominal terms Boeing's operating profit ends the higher. From 2048 it earns more than Airbus each year "
     "($16.57B against $16.23B in 2048, $16.86B against $15.94B from 2049), and over 2026-60 its gain over the status "
     "quo is the larger ($200.71B against $191.74B).</li></ul>"),
    ("The Joint Venture formed in 2035 on conditions both Boards had set in 2030.",
     " No message passed between the companies. Each Board had set, in its private guidance, a matching condition "
     "for the public record to meet: the partner's commitment, or a live airframe carrying the partner's engine. Rolls-Royce's published line "
     "named only P&amp;W's commitment, and P&amp;W published none. NGSA's selection of all three engine makers met the "
     "airframe clause for both.<ul>"
     "<li>In 2030 the RTX Board (the Board of P&amp;W's parent) ruled out a commitment until one of those held, and the "
     "Rolls-Royce Board set the mirror condition. Both CFOs opposed a 2030 commitment in their memos.</li>"
     "<li>In 2035 both CEOs committed on sealed orders, and both Boards approved: on their grids the commitment was "
     "never worth less than holding. The RTX Board had recommended it.</li>"
     "<li>P&amp;W went from −$8.44B to −$2.93B, Rolls-Royce from +$18.26B to +$20.55B, and CFM/GE from −$31.20B to "
     "−$38.29B.</li>"
     "<li>The Joint Venture moved 4.8 points of narrowbody engines from CFM/GE to P&amp;W in every year from 2037. On "
     "the dashboard's engine rules a Joint Venture puts the two partners level, and the extra share comes from CFM/GE. "
     "Rolls-Royce's UltraFan already had the larger share, so only P&amp;W rose.</li>"
     "<li>Rolls-Royce's share and engine value did not change. Its gain is its R&amp;D halving from $8B to its $4B "
     "share, less a $1.71B write-off on UltraFan spend beyond that share.</li></ul>"),
    ("Engine selections set the narrowbody engine split, and CFM/GE's share tracks Boeing's.",
     " Boeing put fps on CFM alone. Airbus opened NGSA to all three makers, on its Board's, CFO's and operating head's "
     "advice: CFM plus a second maker for supply security, and a selection that could never clash with Boeing's.<ul>"
     "<li>CFM/GE falls from 76% of narrowbody engines to 51.7% in 2037 and a low of 50.5% in 2039. It recovers to "
     "56.8% from 2049 as Boeing's CFM-only fps gains share. It keeps a majority in every year, narrowly.</li>"
     "<li>P&amp;W and Rolls-Royce share the rest equally: 24.1% each in 2037, 21.6% from 2049. Rolls-Royce enters from "
     "0%. P&amp;W is above its status-quo 24% only in 2037-41.</li>"
     "<li>CFM/GE ends −$38.29B: $32.29B of engine value lost against the status quo (the narrowbody loss net of the "
     "GEnx widebody gain), plus $4B of ducted-engine R&amp;D and a $2B strain charge for three live programmes.</li>"
     "<li>The Embraer partnership (a CFM engine offered for an Embraer airframe) adds 5 points to CFM/GE's narrowbody "
     "share before re-normalising, from 2037; it has no R&amp;D on the dashboard.</li>"
     "<li>P&amp;W and Rolls-Royce launched only once NGSA selected them, so no engine was built without an "
     "airframe.</li></ul>"),
    ("Nobody re-engined a widebody, and nobody used Delay Tactics.",
     " Both airframers held, each on its own rules. In 2045 and 2050 neither Re-engine cleared its own company's $1B "
     "launch bar even if the rival held, and both CEOs said the hold did not rest on the rival.<ul>"
     "<li><b>Boeing:</b> in 2030 the CEO ruled out a second development beside fps in the first round; in 2035 a 787 "
     "Re-engine would have overlapped fps by 5 years, against its 2-year limit. In 2045 and 2050 its Board would have "
     "vetoed the 787 Re-engine on its business case.</li>"
     "<li><b>Airbus:</b> the A350 Re-engine fell short of the $1B bar, and its CFO and operating head each opposed it "
     "with a binding veto in their memos: Toepfer on his added-move test, Wagner because no widebody engine would be "
     "ready.</li>"
     "<li><b>Rolls-Royce</b> would spend nothing on a new widebody engine without a Re-engine on the record. With "
     "Wagner's readiness test, that is the one mutual wait in the record (observed).</li>"
     "<li><b>Delay Tactics:</b> the Airbus Board ruled out the bottleneck on integrity. In 2030 it ruled out poaching "
     "too: with no fps yet on the record, one move risked the $48.32B fine. In 2035 poaching was worth +$1.65B on "
     "Airbus's grid, but three things each barred it: it took peak spend $0.07B over the Board's $5.2B cash line, the "
     "CFO's memo vetoed it (binding), and Faury kept the team's stricter condition. He and the Board named cash as "
     "decisive.</li>"
     "<li>Measured ex post, the 2030 holds cost Boeing $2.20B and Airbus $3.30B (regret table).</li></ul>"),
    ("No veto overturned a CEO's decision: the Boards set their limits in advance, and no CEO crossed them.",
     " The CFOs' and operating heads' binding vetoes ruled options out before the CEO chose, never his opening lean. "
     "Details under How the companies decided.<ul>"
     "<li>Nine orders went to a Board (seven in 2030, two in 2035), and the Boards approved all nine. The veto checks "
     "on the CEOs' decisions raised no binding veto or red-line flag, so nothing was revised or reverted.</li>"
     "<li>Each Board's guidance named, with numbers, the orders it would veto. None of them was ordered: among them a "
     "737 rate increase beside fps, Delay Tactics, an A350 Re-engine beside NGSA, and a 787 Re-engine in 2045.</li>"
     "</ul>"),
    ("Objectives: Rolls-Royce met both of its own, Boeing neither; five of ten were met.",
     "<ul><li><b>Boeing</b> missed both: 50% of narrowbodies in 2040-50 (38%, 43%, 47%) and holding 40% (38% in "
     "2040). Its true low, 37% in 2039, falls between the tested years.</li>"
     "<li><b>Airbus</b> lost its 60% share target (53% in 2050) but protected the A320 family (60% until NGSA).</li>"
     "<li><b>CFM/GE</b> kept narrowbody dominance, narrowly (51.1% in its worst tested year), and missed its Open Fan "
     "objective (never launched).</li>"
     "<li><b>P&amp;W</b> met one: credibility, its engine on NGSA through the Joint Venture. It missed the other, a "
     "ΔPV of at least zero (−$2.93B).</li>"
     "<li><b>Rolls-Royce</b> met both: narrowbody entry (21.6% in 2050) and widebody dominance (55.2% at worst).</li>"
     "</ul>"),
]

TILES = {
    "boeing": "fps 10-year launched 2030, in service 2040; low of 37% in 2039, 47% from 2049",
    "airbus": "NGSA launched 2030, in service 2037; no Delay Tactics; A350 held",
    "cfm": "Ducted engine, Embraer partnership, GEnx upgrade; no Open Fan",
    "pratt_whitney": "GTF2 on NGSA, folded into the Joint Venture in 2035",
    "rolls_royce": "UltraFan NB on NGSA, folded into the Joint Venture: 0% → 24.1% of narrowbody engines in 2037, 21.6% from 2049",
}

DPV_TITLE = "Each company's ΔPV after each round: settled by 2035, when the Joint Venture moved only the engine makers"

SHARES_LEDE = (
    "<ul><li><b>Narrowbody.</b> NGSA enters service in 2037 and gains 1 point a year while alone, taking Airbus to 63% "
    "in 2039. fps enters service in 2040 and Boeing recovers 1 point a year to 47% in 2049. NGSA's three-year lead is "
    "kept for good, so Boeing settles at 47% of narrowbody deliveries (Airbus 53%), not 50%. Boeing's projected path "
    "never changed after 2030.</li>"
    "<li><b>Widebody.</b> Untouched: nobody re-engined.</li>"
    "<li><b>Engines.</b> fps's CFM-only selection and NGSA's three-way split set the starting narrowbody engine shares. "
    "Each engine programme's move from the public rules then shifts them before re-normalising: UltraFan NB +15 points "
    "(10 from CFM, 5 from P&amp;W), GTF2 +10 (5 each from CFM and Rolls-Royce), CFM's ducted engine +10 and the Embraer "
    "partnership +5. So before the Joint Venture Rolls-Royce led P&amp;W (24.1% against 19.4% in 2037); the Joint Venture "
    "then puts P&amp;W and Rolls-Royce level. Nothing counts before 2037, NGSA's entry into service. The GEnx "
    "upgrade, ready in 2033, moves 2.8 points of widebody engines to CFM/GE only from 2042: the dashboard counts "
    "widebody engine upgrades from its default Re-engine date.</li></ul>")
NB_TITLE = "Narrowbody deliveries: Boeing dips to 37% while NGSA is alone, then settles at 47%"
BOEING_PATH_TITLE = "Boeing's narrowbody share as projected after each round: no revision after 2030"
WB_TITLE = "Widebody deliveries: unchanged, because neither airframer re-engined"
ENG_NB_TITLE = ("Narrowbody engines: CFM/GE keeps a narrow majority; Rolls-Royce enters through NGSA, and the Joint "
                "Venture lifts P&W level with it (21.6% each from 2049)")
ENG_WB_TITLE = "Widebody engines: the GEnx upgrade takes 2.8 points from Rolls-Royce, counted from 2042"

MONEY_LEDE = (
    "<ul><li>The airframers' ΔPV is narrowbody profit above the status quo, less the new airplane's bill, charged at "
    "entry into service as the dashboard does, and the debt penalty. Neither airframer's widebody profit moved.</li>"
    "<li>Boeing's fps bill ($14.91B in PV for $60.32B charged in 2040) and debt penalty ($4.73B) absorb all but $0.66B "
    "of its +$20.30B narrowbody gain.</li>"
    "<li>Airbus's NGSA bill ($15.23B in PV for $35.52B charged in 2037) and debt penalty ($0.53B) leave it +$23.37B of "
    "a +$39.13B gain.</li>"
    "<li>Engine value is the lifetime value of the engines each maker delivers. Rolls-Royce's narrowbody entry takes "
    "its yearly engine value from $4.39B in 2036 to $11.82B in 2037. CFM/GE's is $18.97B in 2037, against $26.34B in "
    "the status quo.</li>"
    "<li>Engine R&amp;D and write-offs are undiscounted, as on the dashboard: CFM/GE $4B for the ducted engine plus $2B "
    "of strain; P&amp;W $2B and Rolls-Royce $4B, their Joint Venture shares (on the dashboard P&amp;W's Joint Venture "
    "R&amp;D is its $2B, and Rolls-Royce's is half of UltraFan NB's $8B, so only Rolls-Royce's fell); and Rolls-Royce's "
    "$1.71B write-off.</li>"
    "</ul>")

MONEY_TITLES = {
    "boeing": "Boeing operating profit: just below the status quo in 2037-39, then $7.65B a year above it from 2040, rising to $10.18B",
    "airbus": ("Airbus operating profit: $9.43B a year above the status quo in 2037, peaking at $10.01B in 2039, then "
               "easing to $7.12B as fps gains share"),
    "cfm": "CFM/GE engine value: $7.37B below the status quo in 2037, $9.26B below by 2060",
    "pratt_whitney": "P&W engine value: above the status quo only in 2037-41",
    "rolls_royce": "Rolls-Royce engine value: $7.33B above the status quo in 2037, $10.46B by 2060",
}

TIMELINE_LEDE = (
    "Every programme but one was launched in 2030; the Joint Venture was launched in 2035, and nothing was cancelled "
    "outright. NGSA enters service in 2037 and fps in 2040. P&amp;W's GTF2 and Rolls-Royce's UltraFan NB, each "
    "launched once NGSA selected its maker, folded into the Joint Venture in 2035. It inherits GTF2's schedule and is "
    "ready in 2036; a fresh Joint Venture would have been ready only in 2041. CFM/GE's ducted engine (ready 2036) and "
    "Embraer partnership (2037) count from 2037, NGSA's entry into service. Its GEnx upgrade, ready in 2033, counts "
    "only from 2042, the dashboard's default Re-engine date.")

GOV_LEDE = (
    "<b>The chain never needed its later steps: no binding veto at the veto check, red-line flag, revision, Board veto "
    "or reversion in 20 company-rounds.</b> "
    "Each company ran the same chain every round. The Board gave guidance. The CEO framed the choice, and the CFO and "
    "operating head tested the options independently. The CEO decided; the CFO and operating head then ran a veto "
    "check on that decision, and the CEO could revise once. Any order other than hold then went to the Board, with one "
    "more revision and a reversion to the default if a Board veto stood. "
    "Two kinds of veto appear below. In their test memos the CFO and operating head could mark any option a veto, "
    "some binding; the CEOs treated the binding ones as ruling those options out before choosing. Only the veto check "
    "on the CEO's actual decision, or a Board review, could send a decision back, and neither did. "
    "The record shows what came earlier: each Board's guidance, and the tests the CEO wrote into his opening framing. "
    "Whether they changed any choice is not observed. Names below are the agents profiled on those executives, not the people.")

GOV_POINTS = [
    ("The Boards set the limits in advance, with numbers.",
     "<ul><li>Each Board's guidance listed the orders it would veto and why, with the item's value in each case. No "
     "CEO submitted one of them.</li>"
     "<li>The CEOs answered each Board recommendation in writing: 167 answers, of which one says \"Not taken\".</li>"
     "<li>They wrote the Boards' tests into their own reasons. Ortberg, on the 787 Re-engine in 2030: \"The Board's "
     "Downside test also bars the Re-engine\".</li></ul>"),
    ("The ExCos agreed at the decision; their binding vetoes fell on the options left out.",
     "<ul><li>In all 40 test memos, the CFO's and the operating head's recommended orders were the CEO's final "
     "orders. In all 20 company-rounds, the final orders were the CEO's opening lean.</li>"
     "<li>The memos marked 58 vetoes binding (50 CFO, 8 operating head, all Wagner's), all on options the CEO did not "
     "choose. The other 80 entries in their veto lists were advice, standing conditions or explicit non-vetoes.</li>"
     "<li>Two failed CFO tests fell on chosen orders. Malave's worst-column test preferred the 7-year ramp, and he set "
     "it aside. The volumes-first test of Rahul Ghai, CFM/GE's CFO, failed the Embraer partnership; Larry Culp, the "
     "CEO, answered it with a $0 premium declaration, as the team rule allows.</li>"
     "<li>61 of the CFOs' 297 tests returned a fail, and 20 of the operating heads' 213.</li>"
     "<li>Some seats had little record of their own, and said so. Pope (Boeing): \"My record is thin\". Lars Wagner "
     "(Airbus): \"My tests are role-derived; confidence Very low\".</li></ul>"),
    ("Boeing's ramp: the one open divergence from a Board.",
     "<ul><li>The Board: \"We therefore recommend the ramp with the higher worst column\", the 7-year, and \"If you "
     "choose the 10-year, state why in the rationale.\"</li>"
     "<li>The Board's guidance also said the 7-year was better by $0.05B in S5 (Airbus Delay Tactics). Its own plan "
     "rows show the opposite (10-year −$0.78B, 7-year −$0.83B), as Ortberg noted. Its case rested on the worst column, "
     "which this does not change.</li>"
     "<li>Ortberg chose the 10-year, as he had leaned from the start. Entering service alongside a 2037 NGSA \"would "
     "time our airplane to theirs, which I will not do.\"</li>"
     "<li>Malave's own worst-column test preferred the 7-year, as the Board did. He set it aside: \"Fully restoring the "
     "health of our balance sheet comes first\", and \"I would not veto the 7-year.\" Pope: \"The 7-year also passes "
     "every test of mine.\"</li>"
     "<li>The Board approved: \"We recommended the 7-year ramp; the CEO answered with reasons, which is not a veto "
     "ground.\" It recorded the incumbency objective as not met, with Boeing below 40% for some years.</li>"
     "<li>At the same review the Board corrected its own guidance. It had parked the 787 Re-engine to 2035, but on "
     "the 10-year ramp a 2035 Re-engine overlaps fps by 5 years, so that window was \"closed by arithmetic\".</li>"
     "</ul>"),
    ("The Joint Venture: matching private conditions, one public trigger.",
     "<ul><li>2030, the RTX Board (the Board of P&amp;W's parent): \"No Joint Venture commit until Rolls-Royce's "
     "commitment is on the record or a live airframe carries a Rolls-Royce code\". The Rolls-Royce Board: a commitment "
     "\"fails partner alignment\" until the same holds for P&amp;W. Both were private guidance.</li>"
     "<li>2035: NGSA's selection of all three makers met the airframe clause for both. Neil Mitchill, P&amp;W's CFO, "
     "had opposed a commitment in his 2030 memo for booking unproven upside: \"That condition is met, so the objection "
     "is cleared.\" Helen McCabe, Rolls-Royce's CFO, co-signed the commitment in her memo.</li>"
     "<li>Chris Calio, P&amp;W's CEO, had flagged his own red line at framing: a Joint Venture shares risk and "
     "investment, never the gear or core. In his decision he rebutted it, since GTF2 folds in, and wrote its condition "
     "into the terms: the gear and core stay one P&amp;W module.</li>"
     "<li>The RTX Board recommended the commitment in 2035. The Rolls-Royce Board \"would approve a commit, but we do "
     "not press it\". Its CEO's red line allowed one once a live airframe's engine selection included P&amp;W, the "
     "Board's own partner test.</li>"
     "<li>Both Boards approved: on their grids the commitment was never below holding.</li></ul>"),
    ("Airbus: the cash line and the team's stricter condition kept Delay Tactics out in 2035.",
     "<ul><li>2030: the Board's guidance ruled out the bottleneck on integrity, and poaching as \"naked\": with no fps "
     "on the record, one move could cost $15.74B through the $48.32B fine.</li>"
     "<li>2035: poaching passed the value test (+$1.65B) and the fps-on-the-record condition. The Board still ruled it "
     "out: \"Its cash, not its value, decides it this round.\" NGSA was spending $5.07B a year against a $5.2B line, "
     "and one move took the peak to $5.27B. If the CEO had not recorded setting aside the team's stricter condition, "
     "it added, poaching \"fails on integrity as well\".</li>"
     "<li>Thomas Toepfer, the CFO: \"an override is arithmetically open, but the Board's own line still vetoes it\". "
     "The team's stricter condition, that the move must change who enters service first, cannot be met on this "
     "dashboard: \"On that condition alone, poaching stays off.\" Toepfer and Wagner also barred the bottleneck on "
     "integrity.</li>"
     "<li>Guillaume Faury, the CEO, did not set that condition aside, and \"the cash line decides it\". He logged the "
     "2030 gap to the best plan on his grid, $3.30B, as \"the cost of the red lines, not a premium\".</li></ul>"),
    ("The widebody: both airframers held on their own rules; the one mutual wait was between Airbus and Rolls-Royce.",
     "<ul><li>Boeing held the 787 Re-engine on different grounds each round: its one-development-at-a-time rule and "
     "the Board's downside test in 2030, its 2-year overlap limit in 2035, and in 2045 and 2050 the Board's $1B "
     "business case plus Ortberg's tie-break toward doing less and paying debt first. Ortberg in 2045: \"I'm not "
     "holding because of Airbus either.\"</li>"
     "<li>The Airbus Board on the A350 Re-engine in 2045: \"The Board does not press for the launch and will not "
     "stand in its way.\" Toepfer failed it on his added-move test. Wagner failed it on readiness: \"The engine leads "
     "the airframe.\" Faury held in both rounds: \"The decision rests on our own tests, not on our read of Boeing.\"</li>"
     "<li>No override was available, since the margin was under $1B. Airbus's rules let the CEO overrule one ExCo "
     "veto per game; that override, open only for poaching in 2035, closed unused. Toepfer in 2050: \"Waiting bought "
     "the same case, smaller.\"</li>"
     "<li>Wagner's readiness test waited on a widebody engine, and Rolls-Royce would launch UltraFan WB only with a "
     "Re-engine on the record (observed).</li>"
     "<li>Rolls-Royce also held the Trent 1000 upgrade, which still carried a $5B strain charge while the Joint Venture "
     "ran. Tufan Erginbilgic, the CEO, in 2050: \"the 2035 widebody plan assumed the strain would lift ... It did "
     "not.\" The misread cost nothing: on the Board's 2045 estimate, without the strain the upgrade was still worth about "
     "−$1.48B (and −$1.73B on its 2050 estimate).</li></ul>"),
    ("CFM/GE: a package within its Board's conditions, and a declined objective.",
     "<ul><li>The GE Aerospace Board's guidance had set the conditions under which it would approve all three 2030 "
     "items (the ducted engine, the Embraer partnership and the GEnx upgrade), and Culp's package met them. The package "
     "was the best plan on CFM/GE's grid in four of six cases, so no premium was paid.</li>"
     "<li>The Board ruled out the Open Fan in every round, as a downside with no airframer to fly on: −$8.00B to "
     "−$57.60B against holding in 2030, −$19.17B in 2050. In 2050: \"we make no end-of-game exception for the Open "
     "Fan objective.\"</li>"
     "<li>On the advice of Ghai, the CFO (\"Book about −$50B\"), Culp, the CEO, expected −$50.41B in 2030. The value "
     "after the round was −$31.20B, and −$38.29B once the Joint Venture formed.</li></ul>"),
]

PLAY_LEDE = (
    "Regret measures what a company gave up against its best alternative in a round, holding everything else in the "
    "game as played. The airframers' regret is in the widebody Re-engines and, for Airbus, the Delay Tactics it did not "
    "order. Rolls-Royce's is its fold-in write-off. CFM/GE's and P&amp;W's orders were the best reply in every round. "
    "The airframers' play is on none of your snapshot's equilibrium lists, and in 2030 and 2035 it was not near any of "
    "the stage game's equilibria either (the dashboard's equilibria for each round alone, earlier orders fixed).")

PLAY_POINTS = [
    ("The played outcome is on none of the snapshot's equilibrium lists.",
     "<ul><li>Your snapshot's four Pure Nash all pair fps on the 10-year ramp with NGSA plus one Delay Tactics move, "
     "with one airframer re-engining.</li>"
     "<li>The game's cell, with no Delay Tactics and no Re-engine, is neither Pure nor Near-Nash: not at the snapshot's "
     "dates (Airbus +$25.05B, Boeing −$0.06B), and not at the game's own fps date of 2040 (+$23.37B, +$0.66B).</li>"
     "<li>Moving fps from 2041 to 2040 cuts the Near-Nash from 12 to 8, and every remaining one has Delay Tactics. "
     "In the snapshot's cell, one Delay Tactics move is worth $1.45B to Airbus at 2041, inside the dashboard's Near-Nash band of 1% of value "
     "($1.5B), and $1.57B at 2040, outside it.</li></ul>"),
    ("The stage game is Chicken on the widebody through 2050.",
     "<ul><li>In every round the two pure equilibria have one airframer re-engine and the other hold. Both survive to "
     "2050 on this dashboard; on the earlier version only Airbus re-engining was left by 2050.</li>"
     "<li>2045: Boeing gains $0.29B by re-engining if Airbus holds, and loses $1.26B if Airbus re-engines too. Airbus "
     "gains $0.89B, or loses $0.50B.</li>"
     "<li>2050: Boeing gains $0.04B or loses $1.00B; Airbus gains $0.57B or loses $0.42B.</li>"
     "<li>Both holding was within $1B of each side's best reply in 2045 and 2050 (the stage game's $1B band; the "
     "dashboard's own Near-Nash band is 1% of value), the only such cell in those rounds. In 2030 and 2035 it was not: "
     "Airbus's best reply was worth $3.30B and $3.19B more.</li></ul>"),
    ("Regret: Airbus gave up most, $3.30B in 2030, in a Delay Tactics move and the A350 Re-engine.",
     "<ul><li><b>Boeing:</b> $2.20B in 2030, falling to $0.04B in 2050, all from the 787 Re-engine. It was kept out by "
     "the one-development-at-a-time rule and the Board's downside test in 2030, by the 2-year overlap limit in 2035, "
     "and in 2045 and 2050 by the Board's $1B business case (and its downside test in 2045) and Ortberg's tie-break "
     "toward doing less.</li>"
     "<li>With Boeing's other orders as played, the 7-year ramp was worth $0.46B more, its logged premium. Regret "
     "counts the best full set of orders, a 787 Re-engine with the 10-year ramp (+$2.86B against +$2.39B with the "
     "7-year), so the ramp does not appear in it.</li>"
     "<li><b>Airbus:</b> $3.30B in 2030 and $3.19B in 2035, from one Delay Tactics move and the A350 Re-engine "
     "together; on its 2030 and 2035 grids either alone was worth about $1.5B to $1.7B. Then $0.89B and $0.57B for the A350 Re-engine.</li>"
     "<li><b>Rolls-Royce:</b> $1.71B in 2030, exactly its fold-in write-off. Holding UltraFan NB in 2030 and joining in "
     "2035 would have brought the same Joint Venture without it. Had no Joint Venture formed, holding would have left "
     "it at −$0.56B, so the conditional launch was right when made.</li>"
     "<li>P&amp;W's GTF2 had spent $1.67B by 2035, under its $2B Joint Venture share, so P&amp;W wrote off nothing. "
     "Rolls-Royce had spent $5.71B against a $4B share.</li></ul>"),
    ("Calibration: the airframers were exact on the case that came true; the engine makers missed by up to $19.21B in 2030.",
     "<ul><li>Airbus expected +$23.37B in 2030 and got +$23.37B. Boeing expected −$1.96B, in the case where Airbus "
     "also re-engined the A350, which the Airbus Board had ruled out in private guidance Boeing could not see. Its "
     "figure for the case that came true, +$0.66B, was exact.</li>"
     "<li>The airframers' own logged costs of their fixed rules (2030-35) and premiums (2045-50) each match the game "
     "master's regret to within $0.01B. Boeing's 2030 ramp premium is not regret (above).</li>"
     "<li>The engine makers missed badly in 2030. CFM/GE expected −$50.41B and got −$31.20B; P&amp;W +$3.15B against "
     "−$8.44B; Rolls-Royce +$3.37B against +$18.26B. The actual selection (fps on CFM alone, NGSA on all three) was "
     "not a case in P&amp;W's or Rolls-Royce's grid.</li>"
     "<li>In 2035 each put \"rivals hold\" first and under-weighted the other's Joint Venture commitment: P&amp;W "
     "expected −$10.14B and got −$2.93B, Rolls-Royce +$15.99B against +$20.55B. From 2045 every company was within "
     "$1.31B, and all but CFM/GE within $0.05B.</li></ul>"),
    ("Only Boeing logged premiums: $0.81B in all, within its $2B cap.",
     "<ul><li>Boeing declared $0.46B in 2030 for the 10-year ramp, then $0.30B and $0.05B in 2045 and 2050 for holding "
     "the 787 Re-engine. The last two were holds its Board said it would have vetoed anyway. By the Board's own rule, "
     "which measures premiums against the best plan that passes its tests, they need not have been logged.</li>"
     "<li>Boeing logged separately what its fixed rules cost: $2.20B in 2030 and $0.65B in 2035.</li>"
     "<li>Every other company declared no premium in any round. Airbus logged its gaps as the cost of its red lines "
     "and binding tests (2030-35), and as within the $1B by which its rules let the default trail the best plan "
     "(2045-50). CFM/GE declined to pay $37.34B in 2035 for the Open Fan objective.</li>"
     "<li>No company cancelled a programme.</li></ul>"),
    ("All 20 company-rounds kept to their own information.",
     "<ul><li>An audit of every tool call found all 20 company-rounds clean: no company reached another's material, "
     "the dashboard or the game master's files.</li>"
     "<li>Each company's chain ran as its own workflow, in parallel, in every round, and nothing passed between "
     "companies.</li></ul>"),
]

COMPARE_LEDE = (
    "<b>The orders differ in only four places, all in 2030 and 2035; in 2045 and 2050 every company held in both "
    "games.</b> The earlier game had one strategist agent per company, deciding as its leadership team, on the earlier "
    "version of the dashboard. This game had four agents per company on the new version. Both changed at once, so the "
    "comparison alone cannot say what the ExCo-and-Board structure did. The decision records show why each order "
    "differs. The table below values each game's final state on both versions of the dashboard.")

COMPARE_POINTS = [
    ("Four orders differ.",
     "<ul><li>2030, Boeing: the 10-year ramp here, the 7-year before; and no 737 rate increase here, an increase "
     "before.</li>"
     "<li>2035, Airbus: no Delay Tactics here, a covert bottleneck before.</li>"
     "<li>2035, Rolls-Royce: a Joint Venture commitment here, a hold before. P&amp;W committed in both games.</li>"
     "<li>Everything else matches: NGSA on all three makers, fps on CFM alone, CFM/GE's three 2030 moves, and "
     "P&amp;W's and Rolls-Royce's conditional launches.</li></ul>"),
    ("In value, the dashboard change repriced one decision: Boeing's ramp.",
     "<ul><li>The earlier version gave the 7-year ramp a 5-point first-mover bonus. On it the 7-year led in every case, "
     "by $5.20B where Airbus launched NGSA alone. The earlier strategist: the 10-year \"costs $5.2B against NGSA, "
     "beyond the $2B cap\".</li>"
     "<li>The new version drops the bonus: the first new narrowbody in service gains 1 point a year while alone, and "
     "keeps it. In Boeing's expected case the two ramps were $0.46B apart, inside the $1B margin its rules treat as a "
     "tie, and the CEO's stated preferences took the 10-year.</li>"
     "<li>The 2030 stage game agrees: its pure equilibria have the 7-year ramp on the earlier version and the 10-year "
     "on the new one.</li>"
     "<li>A replay of all 16 combinations of the four differences on both versions (data/replay16.json) finds the rate "
     "hold, the absent Delay Tactics move and the Joint Venture worth the same on either, within $0.01B. Each order's "
     "effect quoted below is averaged over every combination of the other three; the ramp and the Delay Tactics move "
     "interact, by about ±$0.25B.</li>"
     "<li>All of the dashboard change's effect on the value of the four differences sits in the ramp. It also cut "
     "Airbus's cash headroom (see Delay Tactics).</li></ul>"),
    ("The 737 rate increase: a test declared in advance, and kept.",
     "<ul><li>The grid was the same on both versions: beside an fps launch the increase cost $0.74B in every case.</li>"
     "<li>The earlier strategist took it anyway, as a $0.74B premium under its team rule to raise the rate in the "
     "first round.</li>"
     "<li>Here the Boeing Board listed it among the orders it would veto (\"Its item value is −0.74 in every "
     "column\"), and Ortberg's profile allows the increase only if it adds value. The CEO held; his CFO and operating "
     "head advised the same.</li>"
     "<li>Effect of holding the rate, on either version: +$0.74B for Boeing and +$1.86B for Airbus. Boeing stays at "
     "40% in 2032-36 instead of 45%, and Airbus meets its A320 objective (60% against 55%).</li></ul>"),
    ("Delay Tactics: integrity read two ways, a stricter condition and a cash line.",
     "<ul><li>One move was worth less here (+$1.65B against +$2.16B). The replay puts that on Boeing's 10-year ramp, "
     "not the dashboard: against a 7-year fps the move is worth $2.15B to $2.16B on either version.</li>"
     "<li>The earlier strategist read the bottleneck as Airbus's \"first claim on scarce capacity\", the only form "
     "inside its integrity pillar. It read the team's stricter condition (the move must change who enters service "
     "first) as met, and passed its $5.2B cash guardrail at $4.8B of peak spend.</li>"
     "<li>Here the Airbus Board, its CFO and its operating head barred the bottleneck on integrity. Faury kept the "
     "team's stricter condition, which on its own keeps poaching off, and the Board's cash line also ruled poaching "
     "out. NGSA's bill is larger on the new version ($35.52B against $30.07B), which left only $0.13B of "
     "headroom.</li>"
     "<li>Effect of no Delay Tactics move, averaged over the 16-combination replay: Boeing +$1.69B, Airbus −$1.90B, CFM/GE +$1.61B, P&amp;W and Rolls-Royce "
     "−$0.66B each.</li></ul>"),
    ("The Joint Venture: a red-line clause taken from the Board's test.",
     "<ul><li>In both games a Rolls-Royce commitment in 2035 was worth +$2.29B, but only if P&amp;W committed in the "
     "same round, which it did in both.</li>"
     "<li>The earlier strategist's rule was to commit only after P&amp;W's commitment was public, so with sealed "
     "orders it held. By 2045 joining was worth nothing.</li>"
     "<li>Here the CEO's red line also allowed a commitment once a live airframe's engine selection included P&amp;W, "
     "the Board's partner test, and NGSA met it. For Rolls-Royce, the governance allowed the commitment; no test "
     "required it. For P&amp;W, the RTX Board recommended it.</li>"
     "<li>Worth the same on both versions: Rolls-Royce +$2.29B, P&amp;W +$5.51B, CFM/GE −$7.09B.</li></ul>"),
    ("Company by company.",
     " Each change splits into the dashboard change (the earlier game's state on both versions) and the order change "
     "(both states on the new version).<ul>"
     "<li><b>Boeing</b> −$1.18B: dashboard change −$3.42B, order change +$2.23B.</li>"
     "<li><b>Airbus</b> +$7.76B: dashboard change +$1.98B, order change +$5.79B, mostly Boeing's ramp (+$5.83B) and "
     "rate hold (+$1.86B), less Airbus's own forgone Delay Tactics move (−$1.90B).</li>"
     "<li><b>CFM/GE</b> −$13.11B, with the same orders in both games: dashboard change −$3.45B, others' orders "
     "−$9.66B, mostly the Joint Venture (−$7.09B).</li>"
     "<li><b>P&amp;W</b> +$7.71B, also with the same orders: dashboard change +$1.24B, others' orders +$6.47B, mostly "
     "the Joint Venture (+$5.51B).</li>"
     "<li><b>Rolls-Royce</b> +$4.87B: dashboard change +$1.62B, order change +$3.25B, of which its own commitment "
     "+$2.29B.</li>"
     "<li>Objectives: five of ten met in each game, but different ones. Boeing kept incumbency before and lost it "
     "here, a cost the CEO and Board recorded when choosing the 10-year ramp; Airbus lost A320 protection before and "
     "kept it here.</li></ul>"),
    ("What the comparison cannot say.",
     "<ul><li>The table values fixed end states. It replays no game, so it says nothing about what the companies would "
     "have chosen on the other version of the dashboard.</li>"
     "<li>An order change swaps every company's orders at once. CFM/GE's and P&amp;W's own orders were the same in "
     "both games.</li>"
     "<li>Where the records show a governance mechanism (the rate increase, Delay Tactics, the Joint Venture), it is a "
     "test declared in advance and complied with, never a veto exercised. The ramp changed with the dashboard, and the "
     "ExCo chose it against its Board's advice.</li></ul>"),
]

FOOTER = ("BOEING PROPRIETARY. Built from the dash-2050-exco game record (wargame/runs/dash-2050-exco) by "
          "wargame/dashgame/reports.py and wargame/reports/dash-2050-exco/make_game_html.py. Dashboard: combined_dash.py "
          "at the Game_v3.txt snapshot.")

ROUNDS = {
    1: {"title": "2030: both new narrowbodies launch, and Boeing takes the 10-year ramp-up",
        "lede": ("<ul><li><b>Airbus</b> launched NGSA, open to all three engine makers, for entry into service in "
                 "2037. Its Board, CFO and operating head advised CFM plus a second maker, for supply security. Its "
                 "Board's guidance ruled out an A350 Re-engine beside it, and every Delay Tactics move.</li>"
                 "<li><b>Boeing</b> lifted its rule against a first-round launch: by its CEO's reading the 777X and "
                 "MAX 7/10 were done and debt repair was on track. It launched fps on the 10-year ramp-up, on CFM "
                 "alone, where its Board had recommended the 7-year. No rate increase and no 787 Re-engine.</li>"
                 "<li><b>P&amp;W and Rolls-Royce</b> ordered launches conditional on selection for NGSA, and Airbus "
                 "selected both. Both Boards ruled out a Joint Venture commitment until the partner's was on the "
                 "record or a live airframe carried the partner's engine.</li>"
                 "<li><b>CFM/GE</b> launched the ducted engine, the Embraer partnership and the GEnx upgrade. Its "
                 "Board's guidance had set the conditions under which it would approve all three, and Culp's package "
                 "met them.</li>"
                 "<li>The Boards approved all seven orders put to them.</li></ul>")},
    2: {"title": "2035: the Joint Venture forms; Airbus's cash line and its stricter condition keep Delay Tactics out",
        "lede": ("<ul><li><b>P&amp;W and Rolls-Royce</b> both committed to the Joint Venture on sealed orders. Both "
                 "solo programmes folded into it. It inherits GTF2's schedule and is ready in 2036. Rolls-Royce "
                 "writes off $1.71B.</li>"
                 "<li><b>Airbus</b> left poaching out. It was worth +$1.65B, but it took peak spend $0.07B over its "
                 "Board's $5.2B cash line, and Faury kept the team's stricter condition (the move must change who "
                 "enters service first), which on its own keeps poaching off.</li>"
                 "<li><b>Boeing</b> held the 787 Re-engine: on the 10-year ramp it would overlap fps by 5 years, "
                 "against its 2-year limit. It logged the $0.65B forgone as the cost of that fixed rule.</li>"
                 "<li><b>CFM/GE</b> held everything and declined the Open Fan objective.</li></ul>")},
    3: {"title": "2045: everyone holds; neither airframer re-engines its widebody",
        "lede": ("<ul><li>Both new narrowbodies are in service. The live levers were the Re-engines, the Open Fan and "
                 "Rolls-Royce's widebody engines, and every company held.</li>"
                 "<li><b>Airbus:</b> the A350 Re-engine was worth +$0.89B if Boeing held, under its $1B bar, and no "
                 "widebody engine would be ready for it.</li>"
                 "<li><b>Boeing:</b> its Board would have vetoed the 787 Re-engine on its business case: +$0.29B if "
                 "Airbus held, −$1.26B if Airbus re-engined too.</li>"
                 "<li><b>Rolls-Royce</b> found the Trent 1000 upgrade still carrying a $5B strain charge while the "
                 "Joint Venture ran.</li></ul>")},
    4: {"title": "2050: everyone holds again, and the final state is the 2035 state",
        "lede": ("Every company held, and no value has changed since 2035. A Re-engine ordered in 2050 would enter "
                 "service only in 2055. Airbus's A350 Re-engine was worth +$0.57B if Boeing held and −$0.42B if not; "
                 "Boeing's 787 Re-engine +$0.04B or −$1.00B.")},
}

METHOD = """
<h3>How the game was run</h3>
<ul class="cav">
<li><b>Dashboard.</b> Your combined_dash.py, run headless (never in Streamlit) at the Game_v3.txt snapshot. Solved by the
game master (GM), it reproduces the snapshot: airframers 4 Pure Nash and 12 Near-Nash, engines 1 Pure Nash and 11
Near-Nash, with every rounded yield matching. Changes from the earlier version of the dashboard:
<ul>
<li>The second new narrowbody no longer climbs to 50/50. The first in service gains 1 point a year while alone and keeps
that edge: the long-run split is 50/50 shifted 1 point per year of lead, with the leader capped at 80%.</li>
<li>No 7-year fps share bonus. The two-front strain is overlap-aware and built in. Re-engines default to 2042.</li>
<li>Bills: fps $65.00B (7-year) and $60.32B (10-year), NGSA $35.52B. Narrowbody obsolescence 30%.</li>
</ul></li>
<li><b>Players.</b> 20 AI agents. In each company, the CEO, CFO and operating head of the default 2026 executive
committee, each profiled from that person's own public words (transcripts and filings), and the Board, profiled from
transcripts, filings and web search, with a culture score (risk aversion, time horizon). Where an executive's record was
thin, the seat's tests were derived from the role or company doctrine and labelled low confidence (Pope, Toepfer,
Wagner).
<ul>
<li>Boeing: Kelly Ortberg, Jay Malave, Stephanie Pope and the Boeing Board.</li>
<li>Airbus: Guillaume Faury, Thomas Toepfer, Lars Wagner and the Airbus Board.</li>
<li>CFM/GE: Larry Culp, Rahul Ghai, Mohamed Ali and the GE Aerospace Board, with Safran's consent on CFM
programmes.</li>
<li>P&amp;W: Chris Calio, Neil Mitchill, Shane Eddy and the RTX Board.</li>
<li>Rolls-Royce: Tufan Erginbilgic, Helen McCabe, Rob Watson and the Rolls-Royce Board.</li>
<li>They are AI agents, not the people.</li>
</ul></li>
<li><b>Each round, in each company.</b>
<ul>
<li>The Board gives guidance. The CEO frames the choice. The CFO and the operating head test it, independently.</li>
<li>The CEO decides. The CFO and operating head run a veto check, and the CEO revises once if a binding veto or a
red-line flag stands.</li>
<li>Each Board item (any order other than hold) goes to Board review: approve, or veto with acceptable alternatives.
The CEO revises once within a Board veto. The Board confirms, and a still-vetoed item reverts to the default. A missing
Board review fails closed.</li>
<li>Each company's decision rule and veto grounds come from its team profile.</li>
<li>Each company's chain ran as its own workflow, in parallel, in every round; nothing passed between companies.
Within a company the GM passed only that company's own memos between seats.</li>
</ul></li>
<li><b>Information.</b> As in the earlier game: the public bulletin plus a private brief per company, with its own
position, projection and objective status, and its own payoff grid against a few public scenarios. Only the GM saw the
dashboard.</li>
<li><b>Isolation.</b> The hardened path hook from the earlier game, extended to the new dashboard file and snapshot. It
denies other companies' files and briefs, the dashboard file, the snapshot, GM code, earlier reports and runs, and the
GM's scratch files and transcripts. From 2035 each company had its own scratch folder.
<ul>
<li>An audit of every tool call found all 20 company-rounds clean.</li>
<li>In 2030 the agents tried 13 times to write drafts to the session scratchpad their environment advertises. The
hook denied every attempt, and nothing was written.</li>
<li>Other denials were the hook's conservative rules (command substitution, wildcards) applied to the companies' own
files.</li>
</ul></li>
<li><b>Out-of-date figures.</b> The agents' standing instructions load when the session starts, before the Boeing and
Airbus files were updated for the new dashboard. So the running agents still quoted the earlier dashboard's fps and NGSA
bills, and figures derived from them (NGSA's yearly spend, Boeing's debt penalties), in eleven lines.
<ul>
<li>Everything they read during play (brief, public rules, game guide) used the new dashboard.</li>
<li>In 2030 both airframers' agents noticed. Airbus used the current $35.52B NGSA bill; its CFO noted the difference
moves headroom, not any result. Malave flagged Boeing's old debt-penalty figures as stale, so the current ones were
used.</li>
<li>From 2035 each company's prompts stated its own current figures. The engine makers' files had no changed
figures.</li>
</ul></li>
<li><b>Rounds.</b> Four sealed, simultaneous rounds: 2030, 2035, 2045, 2050, the earlier game's decision years, kept so
the two games compare. With no 2040 round, 2035 was the last chance to order Delay Tactics against an fps due in 2040. Each
round's value is the GM valuation of the state after that round, assuming nobody moves again. The final round's value is
the game outcome.</li>
</ul>
<h3>Rules the GM added to the static dashboard (as in the earlier game)</h3>
<ul class="cav">
<li><b>Time.</b> A programme enters service, or an engine is ready, after its development time from the decision year.
<ul>
<li>Airframes: fps 7 or 10 years, fps via Embraer 10, NGSA 7, Re-engines 5.</li>
<li>Engines: ducted 6, GTF2 6, UltraFan NB 7, UltraFan WB 6, Trent and GEnx upgrades 3, the Embraer partnership 7, the
Joint Venture 6 or an inherited schedule. Open Fan takes 10 years and is never ready before 2045.</li>
</ul></li>
<li><b>Cancellations.</b> Airframes write off the bill × years elapsed ÷ development years, with the dashboard's debt
penalty. Engines write off R&amp;D × years elapsed ÷ development years, undiscounted like the dashboard's R&amp;D.</li>
<li><b>Delay Tactics</b> are covert: the order and its cause are never published. None was ordered in this game.</li>
<li><b>Engines.</b> The dashboard's engine game is applied year by year, splitting each airframer's narrowbody share
equally among the engines fitted to it.
<ul>
<li>Each narrowbody engine move counts from the later of its ready year and the first new narrowbody's entry into service (2037 here).</li>
<li>One change from the earlier game: widebody engine upgrades now count from the year the dashboard starts its
widebody changes (the first Re-engine's entry into service, or 2042), as the dashboard does. On the earlier version that
year was always 2035, so the earlier game is unchanged.</li>
</ul></li>
<li><b>Joint Venture.</b> It forms when both makers commit, without an airframer selecting the Joint Venture engine. It
folds in solo programmes, writing off spend beyond the maker's share, and inherits the most advanced folded
schedule.</li>
<li><b>Tests.</b> The model tests, on both versions of the dashboard: dashboard reproduction, 648 engine move
combinations and the snapshot equilibria. The replay tests: both games replay exactly, and no played year changes. The
isolation tests: 292 cases.</li>
</ul>
<h3>What the numbers are</h3>
<ul class="cav">
<li><b>ΔPV and yield.</b> ΔPV is the change in present value at 2026 against the status quo (nobody launches anything),
at each company's dashboard WACC: Boeing 10.5%, Airbus 8%, CFM/GE 8.5%, P&amp;W and Rolls-Royce 10%. Yield = 100 + 100 ×
ΔPV ÷ enterprise value.</li>
<li><b>Dashboard conventions.</b> Airframe programme spend is charged in full at entry into service. Engine R&amp;D is
undiscounted. Engine value is the lifetime value per engine delivered: price × 1.6, rising 2.2% a year.</li>
<li><b>Regret.</b> The final ΔPV a company would have had with its best alternative orders in that round, holding every
other order in the game as played (later rounds re-run), minus its actual final ΔPV. Myopic regret is the same comparison
valued as if nobody moved after that round, which is the view each brief gave.</li>
<li><b>"Observed".</b> Marks a pattern seen in the records that no single test, rule or order produced.</li>
<li><b>S1, S2, ….</b> The scenario columns of each company's own payoff grid in that round's brief. They differ by company
and round. Ids in brackets, such as [BX-1239], are the agents' evidence citations.</li>
<li><b>Your dashboard alone.</b> The table below sets each final value next to your dashboard alone. The airframers
match exactly. For the engine makers the dashboard fixes a 50/50 airframer split and locks P&amp;W to GTF2 Solo for the
engine selections in this game; the GM's Joint Venture and year-by-year split account for the difference.</li>
</ul>
"""

# Plain text (the HTML builder escapes it): why the GM's final value differs from the dashboard alone.
BOARD_WHY = {
    "boeing": "No difference. The airframer values are your dashboard's own, at the game's dates.",
    "airbus": "No difference. The airframer values are your dashboard's own, at the game's dates.",
    "cfm": ("Dashboard alone −$23.83B. Both partners' Joint Venture moves −$7.09B: the dashboard locks P&W to GTF2 Solo "
            "for the engine selections in this game, so there only Rolls-Royce's Joint Venture move applies. The "
            "year-by-year split −$7.37B: Boeing has 37-47% of narrowbodies, not 50%, and fps carries only CFM "
            "engines."),
    "pratt_whitney": "Dashboard alone −$8.65B. Both Joint Venture moves +$2.75B. The year-by-year split +$2.96B.",
    "rolls_royce": ("Dashboard alone +$16.55B. The fold-in write-off −$1.71B. Both Joint Venture moves +$2.75B. The "
                    "year-by-year split +$2.96B."),
}

# Headline numbers the builder checks against data/report_data.json: (description, round index, player, field, value)
CHECKS = [
    ("final ΔPV", -1, "boeing", "pv_delta", 0.66), ("final ΔPV", -1, "airbus", "pv_delta", 23.37),
    ("final ΔPV", -1, "cfm", "pv_delta", -38.29), ("final ΔPV", -1, "pratt_whitney", "pv_delta", -2.93),
    ("final ΔPV", -1, "rolls_royce", "pv_delta", 20.55),
    ("round-1 ΔPV", 0, "boeing", "pv_delta", 0.66), ("round-1 ΔPV", 0, "airbus", "pv_delta", 23.37),
    ("round-1 ΔPV", 0, "cfm", "pv_delta", -31.20), ("round-1 ΔPV", 0, "pratt_whitney", "pv_delta", -8.44),
    ("round-1 ΔPV", 0, "rolls_royce", "pv_delta", 18.26),
    ("round-2 ΔPV", 1, "cfm", "pv_delta", -38.29), ("round-2 ΔPV", 1, "pratt_whitney", "pv_delta", -2.93),
    ("round-2 ΔPV", 1, "rolls_royce", "pv_delta", 20.55),
    ("round-3 ΔPV", 2, "boeing", "pv_delta", 0.66), ("round-3 ΔPV", 2, "airbus", "pv_delta", 23.37),
    ("final yield", -1, "rolls_royce", "yield", 118.68),
]
# Shares quoted above, checked against the final round's years at the printed precision: (side, key, year, value)
SHARE_CHECKS = [
    ("boeing", "nb_share", 2032, .4), ("boeing", "nb_share", 2036, .4), ("boeing", "nb_share", 2039, .37),
    ("boeing", "nb_share", 2040, .38), ("boeing", "nb_share", 2045, .43), ("boeing", "nb_share", 2049, .47),
    ("boeing", "nb_share", 2050, .47), ("boeing", "nb_share", 2056, .47),
    ("airbus", "nb_share", 2036, .6), ("airbus", "nb_share", 2039, .63), ("airbus", "nb_share", 2049, .53),
    ("airbus", "nb_share", 2050, .53),
    ("cfm", "nb_share", 2036, .76), ("cfm", "nb_share", 2037, .517), ("cfm", "nb_share", 2039, .505),
    ("cfm", "nb_share", 2040, .511), ("cfm", "nb_share", 2049, .568), ("cfm", "nb_share", 2050, .568),
    ("pratt_whitney", "nb_share", 2036, .24), ("pratt_whitney", "nb_share", 2037, .241),
    ("pratt_whitney", "nb_share", 2041, .241), ("pratt_whitney", "nb_share", 2042, .238),
    ("pratt_whitney", "nb_share", 2049, .216), ("pratt_whitney", "nb_share", 2050, .216),
    ("rolls_royce", "nb_share", 2036, 0.0), ("rolls_royce", "nb_share", 2037, .241),
    ("rolls_royce", "nb_share", 2049, .216), ("rolls_royce", "nb_share", 2050, .216),
    ("rolls_royce", "wb_share", 2041, .58), ("rolls_royce", "wb_share", 2042, .552), ("rolls_royce", "wb_share", 2050, .552),
    ("cfm", "wb_share", 2041, .42), ("cfm", "wb_share", 2042, .448),
]
