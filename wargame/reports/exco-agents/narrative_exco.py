"""Text of the ExCo agent-profiles page. Numbers quoted here are checked against the data by make_exco_html.CHECKS."""

TITLE = "The ExCo and Board agents: twenty agents across five companies"

LEDE = ("In our Boeing vs Airbus war game (with the engine makers CFM/GE, Pratt &amp; Whitney and Rolls-Royce), each company "
        "is now played by four AI agents: its CEO, its CFO and its operating head, who together form its executive committee "
        "(ExCo), and its Board of Directors. The ExCo decides; the Board recommends before each round and can veto any big "
        "decision after it. Each executive agent argues and decides as that person would, from a profile built from the "
        "person's public words in earnings calls and investor events (Airbus's three rest mostly on its FY2025 Board Report). "
        "Each Board agent decides as that board would, from what the transcripts and filings say about it and what web search "
        "finds on its composition, rules and culture: how risk-averse it is, and how far it looks ahead. "
        "<b>The game has not been run with these agents yet.</b>")

FINDINGS = [
    ("Every big decision now passes the company's Board.",
     "Each company's ExCo decides, but every order that differs from the default (a launch, a cancellation, a Joint Venture "
     "commitment, the Rate Increase, Delay Tactics) goes to its Board. The Board recommends before the round, then approves "
     "or vetoes each item; the CEO revises once within a veto, and an item the Board still vetoes reverts to the default. "
     "The Board never originates an order."),
    ("The Boards' cultures differ, and their tests follow from them.",
     "On one shared scale, Boeing's Board is the most risk-averse (4.5 of 5): no cash returned since 2020 [BG-0034] and about "
     "$24 billion of equity raised in 2024 to keep the rating [BG-0062]. In the game we set its veto at any item that can "
     "lose more than $1B in a scenario the brief has not ruled out (half the CFO's $2B buffer; our inference, not a real "
     "board threshold). RTX (P&amp;W) is the least risk-averse (3.5): its Board approved a $10 billion accelerated buyback "
     "three months into the powder-metal crisis [PG-0028]. Airbus looks furthest ahead (4 of 5 on time horizon): management's "
     "NGSA plan is kept whole on its 2030 clock [AG-0063], the Board's approval being an inference. Rolls-Royce looks least "
     "far (2.5): it is returning £7-9 billion over 2026-2028 [RG-0059] while the UltraFan narrowbody waits on a partner."),
    ("The ExCo decides as three people, not one.",
     "The CEO frames the round and decides. The CFO and the operating head test the frame independently, each against "
     "their own stated rules, and can block on the grounds their team's rule gives them. How hard that block is differs by "
     "company. At Boeing, Pratt &amp; Whitney and Rolls-Royce a standing veto binds the CEO, though Boeing's two veto rights "
     "are themselves inferred from what the executives said. At Airbus the vetoes are soft: the CEO may override a failed "
     "test once per game, only for a plan at least $1B better, recorded as a Board item. At CFM/GE a failed test binds "
     "unless Culp answers it with evidence, and whether either colleague holds a veto at all is inferred."),
    ("Six agents stand on deep records and play from their own rules.",
     "Culp, Mitchill, Calio, Erginbilgic, Ghai and Ortberg each have more than 100 items in their own words. Their tests "
     "come from what they said: Ortberg asks for a rate step only on KPIs, with \"no subjectivity\" [BX-1259]. Ghai holds "
     "pricing \"price/cost positive\" [CX-0929]. Culp wants \"at least a 20% reduction in fuel burn\" [CX-0217]. "
     "Erginbilgic says \"until I am sure we will deliver, I'm not committing\" [RX-0124]. Two more, McCabe and Watson, "
     "stand on moderate records (61 and 27 items)."),
    ("Seven agents have thin or filing-based records, and are told to defer rather than invent.",
     "Malave's eleven items come from one call. Pope's eight and Ali's 13 (four investor events, 2022-2024) predate their "
     "current roles. Eddy's 21 come from a single day. "
     "Each of these agents names whom to defer to on what, and marks every view beyond the record as inference. Malave "
     "still carries a sharp test of his own: a baseline with buffer \"from a schedule and cost perspective\" [BX-0553]."),
    ("Airbus is profiled from what its Board says, not from what its executives say.",
     "Faury has one line in his own words [AX-0081]; Toepfer and Wagner have none. Their tests and soft vetoes follow from "
     "their roles, their pay metrics and the Board Report, so the Airbus ExCo is where the agents are least like the people."),
    ("Nothing has been played yet.",
     "The twenty agents are set up and kept apart from each other's files, and the round procedure is written. The next step is to "
     "replay the four rounds of the earlier game (dash-2050, where one agent played each company) with the twenty agents, "
     "and compare their orders with that game."),
]

ROSTER_LEDE = ("The default 2026 executive committee of each company, and its Board. Select an agent for the full profile. "
               "<b>Volume</b> counts the items in the person's own words: deep (100 or more), moderate (25 to 99), thin "
               "(5 to 24) or filing-based (under 5; Airbus, built from the Board Report). <b>Confidence</b> is the profile's "
               "own rating of how well that evidence supports the agent; low ratings have an orange border. The <b>veto</b> "
               "label says how hard the member can block the CEO's orders. <b>Steps</b> are the parts of each round the agent "
               "plays: the CEO frames, decides and, when needed, revises; the CFO and the operating head test the plan, then "
               "concur or veto; the Board gives guidance, reviews every big decision and confirms any revision (see How a "
               "round will run).")

EVIDENCE_LEDE = ("The depth of the record varies a lot from person to person. Agents with a deep record play from their own "
                 "stated rules and numbers. Agents with a thin record are told to fall back on the company profile or defer to "
                 "a named colleague, never to invent a view.")

BARS_TITLE = "Evidence behind each agent: from 2 items (Wagner) to 425 (Culp)"
BARS_CAP = ("Items in each person's own evidence file, by whose words they are. Not counted here: items in the company's "
            "evidence file where the person is the speaker ({comp}), and items tagged to the CFM Joint Venture (Culp 51, "
            "Ghai 7, Ali 7). Airbus has one line in an executive's own words (Faury's signed line in the Board Report).")

RUG_TITLE = "When it was said: six items in ten are from 2023-2025"
RUG_CAP = ("One tick per item, at the date of the call, conference or filing. Malave's eleven items come from a single call "
           "(29 October 2025), and Eddy's 21 from a single day (19 June 2023). 26 of Watson's 27 come from one day (28 "
           "November 2023), and four of those are turns by an unnamed speaker that the profile attributes to him. Pope's eight "
           "predate her current role (2012-2022). "
           "Fourteen of Ortberg's items are from his years at Rockwell Collins (2017) and Collins Aerospace (2019). Toepfer's and "
           "Wagner's items, and Faury's 47 Board Report lines, carry the report's issue date, 18 February 2026.")

PROTOCOL_LEDE = ("The game master runs up to nine steps for each company in each round: the Board's guidance, five ExCo "
                 "steps, the Board's review of every big decision and, after a Board veto, the CEO's revision and the Board's "
                 "confirmation. The companies run side by side and never see each "
                 "other's steps. Inside a company, each agent sees only what the game master passes on.")

STEPS = [
    ("Board guidance", "The Board reads the brief and gives the ExCo non-binding guidance: priorities, risk appetite, "
                       "what it would approve or veto, recommendations."),
    ("Frame (CEO)", "Reads the brief and the Board's guidance. Writes the question, the levers in play, the options worth "
                    "testing, the red lines, what he or she asks of each colleague, and an initial lean."),
    ("Test (CFO and operating head)", "In parallel, without seeing each other's memo: tests with thresholds and grid numbers, "
                                      "recommended orders, any veto. At P&W the operating head also proposes the engine orders."),
    ("Decide (CEO)", "Reads both memos and decides by the team's rule. Returns the orders, other moves and public statement, "
                     "records how each memo was weighed, and answers each Board recommendation."),
    ("Veto check", "The CFO and the operating head each concur, or veto on a ground the team rule gives them. Either "
                   "can also flag a breach of a company red line."),
    ("Revise (CEO)", "Only if a binding veto stands or a red line is flagged: revises once within the veto, or overrides "
                     "where the rule allows, on the record, and strikes any breach it confirms."),
    ("Board review", "Every order that differs from the default is a Board item. The Board approves or vetoes each, may "
                     "name acceptable alternatives, and recommends. It never originates an order."),
    ("Board revise (CEO)", "Only after a Board veto: the CEO revises once, to an alternative the Board named or the default."),
    ("Board confirm", "The Board approves or vetoes the revised items. A still-vetoed item reverts to the default."),
]

TEAM_RULES = {
    "boeing": ["Ortberg proposes and decides.",
               "Malave: independent check on programme estimates (buffer, balance sheet first). Pope's seat: rates are KPI-gated.",
               "Malave: any plan that fails his buffer test (the slip leg). KPI doctrine: no 737 Rate Increase while the brief "
               "reports a live quality, FAA or supply-chain problem. Both binding; both inferred from the evidence."],
    "airbus": ["Faury leads the ExCo and takes the final call. NGSA, A350 Re-engine, cancellations and Delay Tactics are Board items.",
               "Toepfer: peak cash, robustness, overlap. Wagner: production readiness, A350F absorption, supply and the ramp "
               "(his engine choice is advice).",
               "Soft vetoes: the CEO may override a failed test once per game, only for a plan at least $1B better than the best "
               "option that passes, recorded as a Board item. The five pillars cannot be overridden."],
    "cfm": ["Culp proposes and decides. Safran is a joint party on pricing and RISE.",
            "Ghai: a launch must pay for itself, volumes before numbers, no launch-era pricing (veto tests); capex within 2-3% "
            "of revenue (advice). Ali: dates only from real testing.",
            "Ghai on terms and capex; Ali on dates no test backs. Both inferred: a failed veto test binds unless Culp answers it "
            "with evidence. Culp's red lines: at least 20% better fuel burn; durability is not traded for fuel burn."],
    "pratt_whitney": ["Calio frames and decides; Eddy proposes the engine orders.",
                      "Mitchill: payback and return gate on every capital order. Eddy: durability, parts and capacity.",
                      "Mitchill on four grounds: dividend or debt path, an unselected engine, aggressive terms, unproven upside. "
                      "Eddy: durability not proven before entry into service, or parts and capacity short. Binding."],
    "rolls_royce": ["Erginbilgic proposes and decides.",
                    "McCabe: mid-to-high-teens hurdle, the unselected downside, the balance sheet. Watson: maturity, and support "
                    "in place before entry into service.",
                    "McCabe: joint sign-off on any launch or aggressive terms, plus balance-sheet vetoes. Watson: compressed "
                    "maturity, a disclosed entry into service earlier than launch plus development time, or no support in place "
                    "before entry into service. Binding."],
}

PROTOCOL_CAP = ("ExCo columns from each company's team file, as adapted to the game in the round script, "
                "<code>wargame/dashgame/workflows/exco_round.js</code>; Board column from each Board's profile, whose dollar "
                "thresholds are mostly the ExCo's game parameters adopted by the Board (an inference). The script has been tried "
                "only with placeholder agents, to check the step order, the output formats, when the CEO revises, when a Board "
                "veto reverts an item, and that a failed Board review fails closed (its items revert to the default). No "
                "executive or Board agent has played a round.")

CARDS_LEDE = ("Each card is the profile its agent plays from. Evidence ids such as BX-0553 show the source line on hover or "
              "keyboard focus. <span class=\"inf\">inference</span> marks a view the evidence does not state directly. Veto "
              "labels: <b>binding</b> (the CEO must revise within it), <b>soft</b> (the CEO may override it on the record, as "
              "the team rule allows), <b>by inference</b> (the evidence shows the test, not the decision right), <b>advice "
              "only</b>. Red lines are company hard rules: anyone may flag a breach and the CEO strikes it. Quotes are word for "
              "word from the evidence files. Airbus Board Report lines are marked as text, not speech, and keep the PDF's "
              "missing spaces. Lever positions, rivals, colleagues and the earlier role-play are under each card's fold.")

GLOSSARY = [
    ("Brief and grid", "Each round the game master gives each company a brief. Its grid shows the value of each of the "
                       "company's plans (rows) against what the others might do (columns, S1, S2 ...)."),
    ("Expected column", "The column the CEO judges most likely; with weights across columns, the weighted value."),
    ("Plausible column", "Any column the public bulletin has not ruled out."),
    ("Risk-case column", "The column that hurts the plan most (for Boeing, the slip leg)."),
    ("Item value", "The plan's value minus the same plan with that one order at its default: what the order itself adds."),
    ("Present value", "Value in $B discounted to 2026, as the grid shows it."),
    ("ΔPV", "A plan's value in $B, at 2026 present value, against the status quo."),
    ("Do Nothing", "Keep the current products; no launch."),
    ("Slip leg, risk case", "The grid column where the rival's moves or a delay hurt the plan most."),
    ("EIS", "Entry into service."),
    ("Premium", "Value a member gives up, in $B, to follow doctrine or an assigned objective; it is declared and capped."),
    ("Tie margin", "$1B: plans closer than this count as equal."),
    ("Hard rules (H1, rule 6 ...)", "The company's red lines, from its profile, as mapped to this board."),
    ("Inference", "A view the evidence does not state directly, labelled as such."),
    ("Board item", "Any order that differs from the default (hold, or none): a launch, a cancellation, a Joint Venture "
                   "commitment, the Rate Increase, Delay Tactics. The Board approves or vetoes each."),
    ("Board guidance", "The Board's non-binding recommendations before a round: priorities, risk appetite, what it would "
                       "approve or veto."),
]

ISOLATION = """
<p>The same hook that kept the single company agents apart in dash-2050 now covers the fifteen executive agents and
the five Board agents
(<code>.claude/hooks/wargame_isolation.py</code>). It checks every file path and command an agent uses, so it stops access
by name, not a deliberately disguised one. A post-game audit of every tool call (<code>audit.py</code>) backs it up.</p>
<ul class="cav">
<li><b>Own company only.</b> Each executive and each Board has the same limits as its single company agent had. It cannot read another
company's profiles, agent files or folder (<code>/tmp/wargame-&lt;company&gt;</code>). It cannot read the game master's code,
the dashboard, the reports or the game master's run records. Its own company's folder stays readable: the run the game
master names, plus earlier rounds' notes and orders of that run.</li>
<li><b>No earlier game.</b> The earlier games' files have been moved out of the company folders into an archive no player
can read. The executives are also blocked from the earlier dash-2050 run by name, so a replay cannot see its orders.</li>
<li><b>No engine, no game-master code.</b> An executive or Board agent runs no game-engine command and cannot import the
game master's modules. Its numbers come only from the brief that the game master writes into its company's folder.</li>
<li><b>Searches stay at home.</b> Searches, wildcard reads and recursive reads must stay inside the company's own folders.
The game master's scratchpad, the session transcripts and the workflow agents' transcripts are blocked.</li>
<li><b>Inside the company.</b> The ExCo and its Board may read each other's agent files (they know each other), but
memos, guidance and reviews pass only through the game master. Within a round, the CFO and the operating head write their
tests before either sees the other's; the Board sees the ExCo's package only after the CEO has decided.</li>
<li><b>Tested.</b> All {cases} hook test cases behave as expected. They include {new} cases for the executive and Board
agents, and {paths} checks that every file each agent is told to read is allowed for that agent. All 360 tool calls the single company
agents made in dash-2050 are still allowed.</li>
</ul>
"""

METHOD = """
<ol class="facts">
<li><b>Sources.</b> The per-person profiles in <code>wargame/profiles/&lt;company&gt;/executives/</code>, built earlier from
the companies' own earnings-call and investor-event transcripts and, for Airbus, the FY2025 Board Report. Also each
team's decision rule (<code>teams.md</code>), the seat's role card, the company doctrine and <code>dashboard_game.md</code>,
which maps the levers to the board.</li>
<li><b>Drafting.</b> One drafting agent per company wrote its three agent files and profiles to a fixed specification:
17 sections in a fixed order, quotes word for word with their ids, inferences labelled, and the round step each seat plays.</li>
<li><b>Verification.</b> A second agent per company re-checked every claim, id and quote against the evidence and corrected
the files in place. A final pass compared the fifteen agents for consistency across companies.</li>
<li><b>Independent audit.</b> Two fresh auditors per company then read the agents again: one checked that each cited item
supports its claim, the other that each agent can play its seat by the rules without leaking. A fixer re-checked every
finding against the sources before changing anything. There were 165 findings; 10 were the same finding reported by both
auditors. Of the other 155, the fixer made 138 changes to the agent files and rejected 4 with a reason. The 13 that belonged
elsewhere are fixed in the round script, the board notes and the specification.</li>
<li><b>Boards.</b> One research agent per company searched the transcripts and filings for what they say about the
board (approvals, authorisations, reserved matters, chairs' remarks) and added new items, each quote checked against its
page by <code>verify_quotes.py</code>. It then used web search for the board's composition, rules, pay horizons, culture
and past decisions. This environment blocks direct page fetches, so web facts come from search results with their URLs
and are shown as search summaries, never as quotes. Each was to be corroborated by a second, differently worded search:
{web_corr} of {web_n} were, and the other {web_unc} are used only as inference, never behind a score, test or veto. A
separate agent then searched again: {web_re} items were re-searched (some corrected, none dropped); {web_not} were not,
because the shared search budget ran out ({web_not_rr} of them Rolls-Royce's, whose web research came last). A drafting agent wrote the Board agent and the executives' new Board sections;
a verifier checked them; a final pass calibrated the culture scores across the five boards.</li>
<li><b>Page review.</b> Two more reviewers read this page: one recomputed its numbers and quotes from the data, the other
read it on desktop and phone. Their 32 findings, including gaps in the isolation, are fixed.</li>
<li><b>Mechanical check.</b> <code>check_agents.py</code> checks each agent's front matter and section order, and that every
cited id exists. It checks every signature quote (each agent's voice lines and the quotes on its card) word for word
against its source item, with "..." marking any gap, and that each card quote's date and perspective match the source.</li>
<li><b>Limits.</b> Airbus's agents rest on what the Board Report says about them, not on their speech. Four records are thin and
Airbus's three are filing-based; those agents defer instead of inventing. Volume is not trust: Watson's 27 items come almost
all from one day, and the profiles' own confidence ratings are shown next to the volume. The "as voiced in dash-2050"
lines are the earlier single company agent's role-play, shown for comparison, not evidence. The Boards' own words
are few and mostly old, and their dollar thresholds are the ExCo's game parameters adopted by inference. How the agents behave in play is untested until the game is run.</li>
</ol>
<p class="label">Files</p>
<ul class="facts small">
<li><code>.claude/agents/&lt;agent&gt;.md</code>: the twenty agent definitions (fifteen executives, for example
<code>boeing-ortberg.md</code>, and five Boards, for example <code>boeing-board.md</code>).</li>
<li><code>wargame/profiles/&lt;company&gt;/board/</code>: each Board's profile (<code>board.md</code>), evidence
(<code>evidence.jsonl</code>) and web sources (<code>sources.md</code>).</li>
<li><code>wargame/reports/exco-agents/data/agents/&lt;agent&gt;.json</code>: the profiles behind this page;
<code>data/people.json</code>: evidence counts per person.</li>
<li><code>wargame/reports/exco-agents/check_agents.py</code> and <code>make_exco_html.py</code>: the checker and this page.</li>
<li><code>wargame/dashgame/workflows/exco_round.js</code>, <code>exco.py</code>, <code>workflows/dry_run.js</code>: the round
script (not run), the game master's save helper, and the stub dry run.</li>
</ul>
"""

FOOTER = ("BOEING PROPRIETARY. Built by wargame/reports/exco-agents/make_exco_html.py from the agent profiles in data/agents "
          "and the evidence files in wargame/profiles/*/ (evidence.jsonl, executives/, board/). No game was run with these "
          "agents.")

# Each profile's own overall confidence, in short (the full wording is on the card). The builder checks that the
# key words appear in the profile's confidence_overall.
CONFIDENCE = {
    "boeing-ortberg": ("Medium-high", "medium-high"),
    "boeing-malave": ("Low", "low"),
    "boeing-pope": ("Very low", "very low"),
    "airbus-faury": ("Medium", "medium overall"),
    "airbus-toepfer": ("Low", "low"),
    "airbus-wagner": ("Very low", "very low"),
    "cfm-culp": ("High in core areas", "high on guidance"),
    "cfm-ghai": ("High in core areas", "high on guidance"),
    "cfm-ali": ("Medium on engineering, low elsewhere", "medium on engineering"),
    "pratt-whitney-calio": ("High in core areas", "high in his core areas"),
    "pratt-whitney-mitchill": ("High in core areas", "high on his core finance areas"),
    "pratt-whitney-eddy": ("Low", "low"),
    "rolls-royce-erginbilgic": ("High in core areas", "high on capital allocation"),
    "rolls-royce-mccabe": ("High in core areas", "high on capital allocation"),
    "rolls-royce-watson": ("Low to medium", "low to medium"),
}
LOW_CONFIDENCE = ("Low", "Very low", "Low to medium", "Medium on engineering, low elsewhere")

# Board texts: filled in from the Board profiles (see make_exco_html.checks()).
BOARD_RULES = {
    "boeing": "Board (independent chair Mollenkopf): a launch must be more than $1B ahead of its default in the CEO's expected "
              "column, no item may lose more than $1B in a plausible column, the plan stays within $2B of Do Nothing in the "
              "risk-case column, developments overlapping at most two years. Dollar limits are the ExCo's game parameters "
              "adopted by the Board (inference). Risk aversion 4.5, time horizon 3.",
    "airbus": "Board (chair Moraleda since October 2026; approval above €300m, two-thirds above €800m): peak spend within about "
              "a year's free cash flow, one clean-sheet launch at a time, no NGSA entry into service before 2035, no item "
              "losing more than $2B in a plausible column, tight limits on Delay Tactics. Risk aversion 4, time horizon 4.",
    "cfm": "GE Aerospace Board (Culp chairs; Lead Director Bush), with Safran's consent on CFM programmes: a Ducted more than $1B "
           "ahead, no item losing more than its own bill, an Open Fan only on an airframer path, new R&D within the payout "
           "floor. Risk aversion 4, time horizon 3.",
    "pratt_whitney": "RTX Board (Calio chairs; lead independent director Reynolds): the return hurdle, an unconditional launch "
                     "only onto a committed airframe or as NGSA franchise defence at least $0.5B ahead of launch if selected, "
                     "no item losing more than its own $2B, durability first, the dividend never gives. Risk aversion 3.5, "
                     "time horizon 3.",
    "rolls_royce": "Board (chair Frew; senior independent director Culmer): safety and maturity first, no unconditional launch "
                   "without an airframe on the record, profit over share, one big programme at a time, the Joint Venture once "
                   "P&W is committed or an airframe's code includes it. Risk aversion 4, time horizon 2.5.",
}
BOARDS_LEDE = ("One agent per company plays its Board of Directors. It does not run the company: it recommends before each "
               "round, then approves or vetoes every big decision, and its veto binds. What it approves follows from its "
               "culture, scored from the evidence on two scales: how risk-averse it is and how far ahead it looks. "
               "Composition is as of the latest source, mostly 2026.")
MAP_TITLE = "Culture map: where each Board sits on risk aversion and time horizon"
MAP_CAP = ("Scores are judgements from the evidence, calibrated on one shared scale; a half point places a Board between "
           "two descriptions. Risk aversion: 3 balanced; 4 averse (rating and safety first, proof before commitment, staged "
           "programme risk still approved); 5 a board in crisis. Time horizon: 2 near-term; 3 balanced; 4 long-term "
           "leaning. Within each Board the scores set its limits (Boeing's downside limit moved from $2B to $1B when it was "
           "scored 4.5 rather than 4). Across companies the limits are stated in each company's own terms, so they are not "
           "directly comparable: the airframers' in dollars, the engine makers' against the item's own bill, which is $2-8B. "
           "The table below gives each Board's own statement of how its scores change its votes. Each Board agent knows only "
           "its own scores. Airbus, GE (CFM) and Rolls-Royce tie on risk aversion, and Boeing, GE (CFM) and RTX (P&amp;W) on "
           "time horizon, where the evidence does not separate them.")

BOARD_SHORT = {"boeing": "Boeing Board", "airbus": "Airbus Board", "cfm": "GE Aerospace Board (CFM)",
               "pratt_whitney": "RTX Board (P&W)", "rolls_royce": "Rolls-Royce Board"}
MAP_LABEL = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "GE (CFM)", "pratt_whitney": "RTX (P&W)", "rolls_royce": "Rolls-Royce"}
GOV = {   # short facts; the builder checks the names against each Board's profile
    "boeing": {"chair": "Steven Mollenkopf, independent", "lid": "None (independent chair)",
               "launch": "No published threshold: the Board approves every new-airplane launch, in two gates", "as_of": "Apr 2026",
               "conf": "Medium-high"},
    "airbus": {"chair": "Amparo Moraleda, independent (since Oct 2026)", "lid": "Mark Dunkerley",
               "launch": "Above €300m; a two-thirds majority above €800m", "as_of": "Oct 2026", "conf": "Medium"},
    "cfm": {"chair": "Larry Culp, Chairman and CEO", "lid": "Wes Bush (Lead Director)",
            "launch": "No published threshold (a 'major' action); CFM programmes also need Safran's consent", "as_of": "Oct 2026",
            "conf": "Medium"},
    "pratt_whitney": {"chair": "Chris Calio, Chairman and CEO", "lid": "Fredric Reynolds",
                      "launch": "No published threshold; a new engine or Joint Venture is outside the self-funded plan, so a Board matter",
                      "as_of": "Apr 2026", "conf": "Medium"},
    "rolls_royce": {"chair": "Dame Anita Frew, independent", "lid": "George Culmer (Senior Independent Director)",
                    "launch": "Board threshold not public; CEO and CFO sign off every case above £25m", "as_of": "Sep 2026",
                    "conf": "Medium"},
}
