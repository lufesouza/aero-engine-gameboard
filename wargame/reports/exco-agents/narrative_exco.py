"""Text of the ExCo agent-profiles page. Numbers quoted here are checked against the data by make_exco_html.CHECKS."""

TITLE = "One agent per executive: the fifteen ExCo agents"

LEDE = ("Each company in the war game will now be played by three agents instead of one: its CEO, its CFO and its operating "
        "head. Each agent is built from that person's own words in earnings calls and investor events; Airbus's three are built "
        "from the FY2025 Board Report, which is mostly not their speech. This page profiles the fifteen agents, the evidence "
        "behind each, and how a round will run with them. <b>The game has not been run with them yet.</b>")

FINDINGS = [
    ("Each company now decides as three people, not one.",
     "The CEO frames the round and decides. The CFO and the operating head test the frame independently, each against "
     "their own stated rules, and can block on the grounds their team's rule gives them. How binding that is differs by "
     "company: binding at Boeing, Pratt &amp; Whitney and Rolls-Royce; soft at Airbus (overridable only for a plan at least "
     "$1B better, on the Board's record); inferred at CFM/GE."),
    ("Six agents stand on deep records and play from their own rules.",
     "Culp, Mitchill, Calio, Erginbilgic, Ghai and Ortberg each have more than 100 items in their own words. Their tests "
     "come from what they said: Ortberg asks for a rate step only on KPIs, with \"no subjectivity\" [BX-1259]. Ghai keeps "
     "capex in the 2% to 3% range [CX-0922]. Culp wants \"at least a 20% reduction in fuel burn\" [CX-0217]. McCabe and "
     "Erginbilgic sign off every case above \u00a325 million together, against mid- to high-teens hurdles [RX-0213]."),
    ("Seven agents have thin or filing-based records, and are told to defer rather than invent.",
     "Malave's eleven items come from one call; Pope's eight predate her current role; Ali has 13 and Eddy 21 from one day. "
     "Each of these agents names whom to defer to on what, and marks every view beyond the record as inference. Malave "
     "still carries a sharp test of his own: a baseline with buffer \"from a schedule and cost perspective\" [BX-0553]."),
    ("Airbus is profiled from what its Board says, not from what its executives say.",
     "Faury has one line in his own words [AX-0081]; Toepfer and Wagner have none. Their tests and soft vetoes follow from "
     "their roles, their pay metrics and the Board Report, so the Airbus ExCo is where the agents are least like the people."),
    ("Nothing has been played yet.",
     "The agents are installed and isolated, and the round script is written. The next step is to replay the four dash-2050 "
     "rounds with the fifteen agents and compare their orders with the single company agents' play."),
]

ROSTER_LEDE = ("The default 2026 executive committee of each company. Select a person for the full profile. <b>Record</b> is "
               "the depth of the evidence in the person's own words: deep (100 or more items), moderate (25 to 99), thin "
               "(fewer than 25) or filing-based (Airbus, built from the Board Report). <b>veto</b> marks the members whom the "
               "team's decision rule lets block the CEO's orders.")

EVIDENCE_LEDE = ("The depth of the record varies a lot from person to person. Agents with a deep record play from their own "
                 "stated rules and numbers. Agents with a thin record are told to fall back on the company profile or defer to "
                 "a named colleague, never to invent a view.")

BARS_TITLE = "Evidence behind each agent: from 2 items (Wagner) to 425 (Culp)"
BARS_CAP = ("Items in each person's evidence file, by whose words they are. Culp also has 51 items tagged to the CFM Joint "
            "Venture, Ghai 7 and Ali 7, which are not counted here. Airbus has one line in an executive's own words (Faury's "
            "signed line in the Board Report).")

RUG_TITLE = "When it was said: six items in ten are from 2023-2025"
RUG_CAP = ("One tick per item, at the date of the call, conference or filing. Malave's eleven items come from a single call "
           "(29 October 2025), and Eddy's 21 from a single day (19 June 2023). Pope's eight predate her current role (2012-2022). "
           "Fourteen of Ortberg's items are from his years at Rockwell Collins (2017) and Collins Aerospace (2019). Toepfer's and "
           "Wagner's items, and Faury's 47 Board Report lines, carry the report's issue date, 18 February 2026.")

PROTOCOL_LEDE = ("The game master runs five steps for each company in each round. The companies run side by side and never see "
                 "each other's steps. Inside a company, each executive sees only what the game master passes on.")

STEPS = [
    ("Frame (CEO)", "Reads the company's brief. Writes the question, the levers in play, the options worth testing, the red "
                        "lines, what he or she asks of each colleague, and an initial lean."),
    ("Test (CFO and operating head)", "In parallel, without seeing each other's memo: tests with thresholds and grid numbers, "
                                          "recommended orders, any veto. At P&W the operating head also proposes the engine orders."),
    ("Decide (CEO)", "Reads both memos and decides by the team's rule. Returns the orders, other moves and public statement, "
                         "and records how each memo was weighed."),
    ("Veto check", "The CFO and the operating head each concur, or veto on a ground the team rule gives them. Either "
                    "can also flag a breach of a company red line."),
    ("Revise (CEO)", "Only if a binding veto stands or a red line is flagged: revises once within the veto, or overrides "
                      "where the rule allows, on the record, and strikes any breach it confirms."),
]

TEAM_RULES = {
    "boeing": ["Ortberg proposes and decides.",
               "Malave: independent check on programme estimates (buffer, balance sheet first). Pope's seat: rates are KPI-gated.",
               "Malave: any plan that fails his buffer test (the slip leg). KPI doctrine: no 737 Rate Increase while the brief "
               "reports a live quality, FAA or supply-chain problem. Both binding; both inferred from the evidence."],
    "airbus": ["Faury leads the ExCo and takes the final call. NGSA, A350 Re-engine, cancellations and Delay Tactics are Board items.",
               "Toepfer: cash, overlap and robustness. Wagner: production, engines and quality.",
               "Soft vetoes: a failed test can be overridden only if the plan is at least $1B better than the best option that passes, "
               "recorded as a Board item. The five pillars cannot be overridden."],
    "cfm": ["Culp proposes and decides. Safran is a joint party on pricing and RISE.",
            "Ghai: price/cost positive, capex within 2-3% of revenue, no number before volumes. Ali: dates only from real testing.",
            "Both inferred: a failed test binds unless Culp answers it with evidence. Culp's red lines: at least 20% better fuel "
            "burn; durability is not traded for fuel burn."],
    "pratt_whitney": ["Calio frames and decides; Eddy proposes the engine orders.",
                      "Mitchill: payback and return gate on every capital order. Eddy: durability, parts and capacity.",
                      "Mitchill on four grounds: dividend or debt path, an unselected engine, aggressive terms, unproven upside. "
                      "Eddy: durability not proven before entry into service, or parts and capacity short. Binding."],
    "rolls_royce": ["Erginbilgic proposes and decides.",
                    "McCabe: mid-to-high-teens hurdle, the unselected downside, the balance sheet. Watson: maturity, and support "
                    "in place before entry into service.",
                    "McCabe: joint sign-off on any launch or aggressive terms, plus balance-sheet vetoes. Watson: compressed "
                    "maturity, or entry into service earlier than launch plus development time. Binding."],
}

PROTOCOL_CAP = ("Rules from each company's <code>executives/teams.md</code>. The round script is "
                "<code>wargame/dashgame/workflows/exco_round.js</code>. It has been dry-run with stub agents only, to check the "
                "step order, the output formats and the revise rule. No executive agent has been run in a round.")

CARDS_LEDE = ("Each card is the profile its agent plays from. Evidence ids such as BX-0553 show the source line on hover or "
              "keyboard focus. <span class=\"inf\">inference</span> marks a view the evidence does not state directly. Quotes "
              "are word for word from the evidence files. Airbus Board Report lines are marked as text, not speech, and keep "
              "the PDF's missing spaces. Lever positions, rivals, colleagues and the earlier role-play are under each card's "
              "fold.")

ISOLATION = """
<p>The same hook that kept the five company agents apart in dash-2050 now covers the fifteen executive agents
(<code>.claude/hooks/wargame_isolation.py</code>).</p>
<ul class="cav">
<li><b>Own company only.</b> Each executive has its company strategist's limits. It cannot read another company's
profiles, agent files or private folder (<code>/tmp/wargame-&lt;company&gt;</code>). It also cannot read the game master's
code, the dashboard, the reports, or any earlier run's record.</li>
<li><b>No engine.</b> An executive runs no game-engine command at all. Its numbers come only from the brief that the game
master writes into its company's folder.</li>
<li><b>Searches stay at home.</b> Searches, wildcard reads and recursive reads must stay inside the company's own folders. The
game master's scratch areas and all agent transcripts are off limits.</li>
<li><b>Inside the ExCo.</b> Colleagues may read each other's agent files (they know each other), but memos pass only through
the game master. Within a round, the CFO and the operating head write their tests before either sees the other's.</li>
<li><b>Tested.</b> All 225 hook test cases behave as expected. They include 18 new cases for the executive agents, and 183
checks that every file each agent is told to read is allowed for that agent. All 360 tool calls the company agents made in
dash-2050 are still allowed.</li>
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
finding against the sources before changing anything. Of 165 findings (some reported by both auditors), the fixer made 138
changes to the agent files and rejected 4 with a reason. The 13 that belonged elsewhere are fixed in the round script, the
board notes and the specification.</li>
<li><b>Mechanical check.</b> <code>check_agents.py</code> checks each agent's front matter and section order. It also checks
that every cited id exists, that every quote is an exact substring of its source item, and that each quote's date and
perspective match the source.</li>
<li><b>Limits.</b> Airbus's agents rest on what the Board Report says about them, not on their speech. Four records are thin and
Airbus's three are filing-based; those agents defer instead of inventing. The "as voiced in dash-2050" lines are the earlier single agent's role-play, shown
for comparison, not evidence. How the agents behave in play is untested until the game is run.</li>
</ol>
<p class="label">Files</p>
<ul class="facts small">
<li><code>.claude/agents/&lt;agent&gt;.md</code>: the fifteen agent definitions (for example <code>boeing-ortberg.md</code>).</li>
<li><code>wargame/reports/exco-agents/data/agents/&lt;agent&gt;.json</code>: the profiles behind this page;
<code>data/people.json</code>: evidence counts per person.</li>
<li><code>wargame/reports/exco-agents/check_agents.py</code> and <code>make_exco_html.py</code>: the checker and this page.</li>
<li><code>wargame/dashgame/workflows/exco_round.js</code>, <code>exco.py</code>, <code>workflows/dry_run.js</code>: the round
script (not run), the game master's save helper, and the stub dry run.</li>
</ul>
"""

FOOTER = ("BOEING PROPRIETARY. Built by wargame/reports/exco-agents/make_exco_html.py from the agent profiles in data/agents "
          "and the evidence files in wargame/profiles/*/executives. No game was run with these agents.")
