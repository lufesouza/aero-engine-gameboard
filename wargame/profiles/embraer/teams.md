# Embraer leadership team for the war game

**What this file is.** Embraer's 2026 executive committee (ExCo) for the dash-2050 game. It gives:
- the members and their roles, as the transcripts show them;
- the decision rule: who proposes, who decides, who can veto what, and which orders go to the Board;
- the tensions between the members;
- how the ExCo, with Antonio Carlos Garcia as CFO, turned company doctrine into decisions from 2020 to 2026 (the record today's team inherits);
- a per-round ExCo deliberation script;
- how the team differs from the company default;
- a ready `TEAMS` entry for `wargame/dashgame/workflows/exco_round.js`.

The company profile (`profile.md`) says what is in bounds: its hard rules H1-H6 bind the team. This file says how the three people decide inside them. Where they collide, the company's hard rules win.

**The default team is `gomes-neto-santana-meijer-2026`.** It seats today's (2026) ExCo, with Felipe Santana as CFO, and it is the only Embraer team: the transcripts give no other ExCo with an airliner decision in front of it. The CFO seat runs the funding test inherited from Antonio Carlos Garcia (CFO from January 2020 to March 2026), whose record is the company's finance doctrine (`wargame/profiles/embraer/executives/garcia.md`).

## 1. Conventions

- **Ids.** `[EB-####]` is a company item in `wargame/profiles/embraer/evidence.jsonl`; executive items (EX-) live in the same file, tagged by executive (grep the file for Santana's and Garcia's items; Garcia's are the inherited record).
- **Tie band and cap (profile H5, inference).** Within 2 yield points (2% of the enterprise value the brief gives) is a tie; a soft doctrine choice may cost at most 5 yield points.
- **The window (profile H3, inference).** Count the new-generation rival types (fps, NGSA) in service at your entry into service (launch + 4). "Due" means launched, with the entry-into-service year the bulletin gives.
  - **Open:** neither in service at your entry into service.
  - **Narrow:** one already in service at your entry into service.
  - **Shut:** each of fps and NGSA in service at your entry into service or due within 2 years after it (hard rule H3: no launch).
  - A 2030 launch always meets an open window (no rival type can be in service by 2034); the test bites from 2035.
- **The brief's columns.** "Expected" is the rival plan the CEO names as most likely in the frame or the decision (if neither names one, the CFO seat picks the plan it judges most likely and says which); the "risk column" is the brief's labelled risk case if there is one, otherwise its worst plausible column (one the public bulletins have not ruled out).
- **Board items.** Every order that differs from Hold: any launch, any cancel. The Board's review binds.
- **(inference)** marks anything beyond the evidence. Decision rights are inferred: the sources are calls, not Board papers. ExCo questions in italics paraphrase the cited items; quotation marks mark verbatim text.

## 2. Team index

| Team id | CEO | CFO | Operating seat | Era in the evidence | Evidence depth | In one line |
|---|---|---|---|---|---|---|
| **`gomes-neto-santana-meijer-2026` (DEFAULT)** | Gomes Neto | Santana (on Garcia's doctrine) | Meijer (CEO, Commercial Aviation) | CEO Aug 2019 to May 2026; CFO Santana May 2026 (Garcia, the inherited doctrine, Mar 2020 to Mar 2026); Meijer Nov 2022 to Nov 2024 | Good / Low (Santana's own; Garcia's inherited doctrine Good) / Low-Medium | Balance sheet first; launch only with a partner, a value proposition and a window |

**The CFO seat in 2026.** On 8 May 2026 Felipe Santana presented the results as CFO and was welcomed "to the call and CFO position" [EB-0152, EB-0153, EX-0700]; Garcia's last call in the record is 6 March 2026 [EB-0055]. The game seats Santana. Santana's one call holds nothing on a new airplane, a partner or a funding threshold, and is consistent with Garcia's six years: leverage reported ex-Eve and tariffs kept in guidance as "a conservative approach" [EB-0052, EB-0128, EX-0721]. So the CFO seat runs Garcia's tests unchanged, citing them as inherited from Garcia, never as the sitting CFO's words **(inference)**.

## 3. `gomes-neto-santana-meijer-2026` (DEFAULT for the 2026 game)

### Members and roles

- **Francisco Gomes Neto, President and CEO.**
  - Joined in May 2019 [EB-0144]; introduced as President and CEO in August 2019 [EB-0145].
  - Owns strategy: the 2021-25 plan, "Fit for Growth" [EB-0029, EB-0030], the $10 billion goal [EB-0025] and the "harvest season" posture [EB-0001].
  - Speaks for new products: studies, the three launch conditions, no timeline [EB-0012, EB-0015, EB-0016].
  - Handled the Boeing termination [EB-0097, EB-0098] and led the tariff lobbying [EB-0113].
  - Evidence: speaker in 30 events, August 2019 to May 2026. **High** on stance; **Medium** on decision rights.
- **Felipe Santana, CFO** (Executive Vice President of Financial & Investor Relations) [EB-0700].
  - Introduced as "Chief Financial Officer" and presented the results on 8 May 2026 [EB-0701, EX-0700]; new in the post that day [EB-0702]. Background and start date are not in the transcripts.
  - The voice of the guidance, leverage and cash on that call: leverage reported without Eve [EX-0708]; the outlook kept until there is visibility, "a conservative approach" [EX-0711, EX-0721].
  - Runs the CFO seat's funding test on the doctrine inherited from Garcia (below).
  - Evidence: speaker in 1 event, May 2026 (EX-0700 to EX-0724). **Low**; nothing in Santana's own words on a new airliner.
- **Antonio Carlos Garcia, CFO from January 2020 to March 2026** (Executive VP Finance and Investor Relations): history, and the inherited finance doctrine (`wargame/profiles/embraer/executives/garcia.md`). Not seated; cited as inherited from Garcia.
  - Joined in January 2020 and presented as the new CFO in March 2020 [EB-0146]; an automotive background [EB-0147].
  - Led the daily cash-management team in the 2020 crisis [EB-0148]; introduced as CFO and responsible for procurement in 2022 [EB-0149].
  - The voice of capital allocation, the balance sheet and guidance [EB-0035, EB-0042, EB-0043, EB-0055].
  - Evidence: speaker in 27 events, March 2020 to March 2026. **Medium-High** on finance; **Low** on a new airliner (one 2021 rule [EB-0035]).
- **Arjan Meijer, President and CEO of Commercial Aviation and Chief Commercial Officer** [EB-0150, EB-0151].
  - Speaks in three events (November 2022, March 2023, November 2024): E2 positioning and economics [EB-0074, EB-0075, EB-0076], price against share [EB-0072, EB-0073], the A220 and COMAC [EB-0080, EB-0140], scope clauses [EB-0081], supply chain and engines [EB-0078, EB-0079], the turboprop's system supply [EB-0021].
  - Absent from the 2025-26 calls, where the CEO answers commercial questions; whether Meijer is still in post in 2026 is not in the transcripts. **Low-Medium.**

### Decision rule

- **Gomes Neto proposes and decides.** A launch must meet the CEO's own conditions: "a strong product with a strong value proposition with a robust, I mean, funding strategy because we don't want to put in risk the financial health of the company" [EB-0015], and technology that is ready [EB-0016].
- **Santana, the CFO, tests the funding on the doctrine inherited from Garcia. A failed test is a binding veto with no override (inference).** The rule rests on Garcia's record: "any large investment will require strategic partners" [EB-0035], diligence on new products [EB-0036], the cash floor [EB-0038], investment grade [EB-0047] and earning the cost of capital [EB-0045]; it binds because the test is the CEO's own funding condition [EB-0015]. A launch passes only if:
  - Team Korea carries its share of the bill in the brief (H1);
  - ΔPV, debt penalty included, is at or above zero in the expected column (H2);
  - in the risk column it loses no more than 5 yield points against Hold.
- **Meijer tests the market window and readiness. A failed test is a soft veto (inference).** The rule rests on the window doctrine [EB-0022], the share aim [EB-0073], supply chain as the binding constraint [EB-0034, EB-0143] and the turboprop's stall on system supply [EB-0021]. A launch fails if:
  - the window is narrow: one new-generation rival type is already in service at its entry into service; or
  - the brief reports a supply-chain or engine problem that would hold the line.
  The soft veto binds unless Gomes Neto records an override, as a Board item, for a plan more than 5 yield points better than Hold in the expected column.
- **Company red lines bind everyone.** No launch into a shut window (H3) or while Boeing's fps via Embraer is live (H6); a colleague's red-line flag forces the CEO to strike the order, unless the CEO shows in the rationale that the flag is mistaken; a flag neither struck nor rebutted is an unresolved objection for the Board.
- **Cancel.** Only before entry into service, when writing off beats continuing by more than 2 yield points (H4), with the CFO's numbers. Never because a rival announced a launch.
- **Tie-break (inference).** Within 2 yield points: Hold in 2030 if, in the expected rival plan, a 2035 launch keeps an open window, otherwise Launch; Launch in 2035 if ΔPV is at or above zero (the last round that meets the 2040 objective). The CEO keeps promises rather than stretching them: "we prefer to have a commitment with you that we will deliver" [EB-0028].

### Veto grounds

| Holder | Ground | Binds? | Evidence |
|---|---|---|---|
| Santana (CFO), on Garcia's doctrine | A launch whose funding fails the test: no partner share in the brief, ΔPV below zero with the debt penalty in the expected column, or a loss of more than 5 yield points against Hold in the risk column | Yes, no override (inference) | EB-0035, EB-0036, EB-0038, EB-0045 (inherited from Garcia), EB-0015 |
| Meijer (Commercial Aviation) | A launch into a narrow window (one rival new-generation type in service at its entry into service), or a supply-chain or engine problem in the brief that would hold the line | Soft: binding unless the CEO records an override, as a Board item, for a plan more than 5 yield points better than Hold in the expected column (inference) | EB-0022, EB-0073, EB-0034, EB-0143, EB-0021 |
| Either | A breach of a company hard rule (H1-H6) | Yes (red-line flag) | profile.md |

### Board items

- **Any launch and any cancel** go to the Embraer Board of Directors, whose review binds **(inference)**. Precedent: the Boeing partnership was approved by the Board "subject to golden share approval", then needed the federal government's approval, Board ratification and the shareholders [EB-0087, EB-0090, EB-0092, EB-0095].
- **The golden share (inference).** A Team Korea co-development in which Embraer keeps control and moves no military technology should not need the state's consent; the share's reported scope is research, unverified [EB-0186]. The 2018 deal was framed as no change of control of Embraer itself [EB-0093].
- **Hold** is the default and is not a Board item.

### Typical tensions

- **Growth against the balance sheet.** The CEO's ambition of "double-digit billion revenues and double-digit EBIT margins" [EB-0026] and products "larger planes than E195-E2" [EB-0007], against the partners-for-any-large-investment rule the CFO seat inherits from Garcia [EB-0035], dividends that are "already a lot" [EB-0044] and the cost-of-capital guard rail [EB-0045].
- **Share against price.** Meijer wants to "build our market share" yet be "very sensitive on the pricing" [EB-0073, EB-0072]; IR in 2016 refused "aggressive movements" [EB-0071]. On the board your campaigns cut the incumbents' prices, not your margin **(inference)**.
- **Study against window.** "we don't have a time line definition" [EB-0009] and "This does not depend only on us" [EB-0016], while the window shuts as fps and NGSA arrive **(inference)**.
- **A thin operating seat.** Meijer's record ends in November 2024 and holds no view on a larger airplane; the team runs mostly on the CEO and on the CFO seat's doctrine inherited from Garcia, since Santana's own record is one call [EX-0700].

### How the ExCo turned doctrine into decisions (2020-26, Garcia as CFO)

- **The Boeing termination, April 2020:** cash first, a floor near $2 billion, no equity, arbitration [EB-0097, EB-0098, EB-0148, EB-0038, EB-0040]; then reintegration and the 2021-25 plan [EB-0104, EB-0029].
- **Deleveraging** from 5.6x to net cash, and investment grade regained [EB-0049, EB-0050, EB-0051, EB-0047, EB-0048].
- **The turboprop:** a partner-funded plan [EB-0019], a business-case gate that slipped [EB-0020], a slowdown for system supply [EB-0021], cancellation in November 2025 [EB-0010].
- **The E175-E2:** on hold for US scope [EB-0011, EB-0081].
- **Capacity:** to about 100 commercial jets in 2027 and 120 by 2030, only where the return justifies it [EB-0033, EB-0032, EB-0142, EB-0141].
- **Shareholders:** dividends resumed at the legal minimum in 2025 [EB-0053, EB-0044].
- **Tariffs:** lobbying on jobs and trade, guidance kept conservative, no politics [EB-0113, EB-0125, EB-0056, EB-0123].
- **The new airplane:** studies, three conditions, no timeline [EB-0012, EB-0015, EB-0009]; "crisis mode since 2020 in some areas" still, in Garcia's words as CFO [EB-0046].

### ExCo deliberation script (every round)

1. **Gomes Neto frames.**
   - *What do the bulletins show of fps and NGSA?* Launched or not, and their entry-into-service years: count the window (§1).
   - *Is there a strong product with a strong value proposition?* The board's airplane beats the A320neo and 737 MAX only slightly, so its value is timing [EB-0023, EB-0024] **(inference)**.
   - *Is the funding robust?* Team Korea's share and the debt penalty in the brief [EB-0015, EB-0035].
   - *Is the technology there?* [EB-0016] The board fits P&W engines, or CFM's if CFM's Embraer partnership is live; this passes unless the brief reports an engine problem.
   - *Are we locked?* Boeing's fps via Embraer live, or ordered this round (H6).
   - **Asks of Santana (CFO):** the expected and risk columns with the debt penalty; Launch against Hold; the write-off for any cancel. **Asks of Meijer:** the window count, the share path through the ramp, supply-chain and engine readiness.
2. **Santana tests the funding** (binding), on the doctrine inherited from Garcia. The three thresholds above. "We are not running the company by hope" (Garcia) [EB-0041]: the conservative case is the baseline [EB-0056, EX-0721].
3. **Meijer tests the window and the line** (soft). Narrow window or a reported supply or engine problem fails.
4. **Gomes Neto decides by the rule.**
   - **Launch** if every test passes and Launch beats Hold by more than 2 yield points in the expected column; ties by the tie-break.
   - **Hold** otherwise. A failed CFO funding test is final; a failed Meijer test may be overridden only as above, and the override is a Board item.
   - **Cancel** only by H4.
   - Answer each Board recommendation; revise once within any Board veto, to an alternative it named or to Hold.
5. **Disclose and speak.**
   - **Before a launch:** no date, no segment: "This does not depend only on us" [EB-0016]; no comment on rivals' choices [EB-0133].
   - **At a launch:** the three conditions [EB-0015], Team Korea named, entry into service 4 years out, delivery promised conservatively [EB-0028].
   - **Commercial lines in Meijer's voice:** "the trip costs are 25%, 30% lower but the seat costs are almost the same" [EB-0075]; "we stopped calling it regional aircraft" [EB-0076].
   - **Financial lines in Santana's voice:** "we're taking a conservative approach because of the current high uncertainties" [EX-0711]; Garcia's line, inherited: "We are not running the company by hope" [EB-0041].
   - **Politics:** none. "Embraer is about engineering" [EB-0122]; argue jobs and zero tariffs if US tariffs bite [EB-0114, EB-0125].

### How this team differs from the company default

- **Very little:** the [NOW] doctrine in `profile.md` is this team's record. The team sharpens three things:
  - **The CFO's funding test (Santana, on Garcia's doctrine) binds** and has no override.
  - **Meijer's window-and-readiness test is soft**: the CEO can override it (a narrow window, or a reported supply-chain or engine problem) only for a plan more than 5 yield points better than Hold in the expected column, and the override is a Board item.
  - **The CFO seat changed in May 2026**: Santana sits; the funding doctrine is Garcia's, inherited.
- **Thin seat.** Every Meijer position beyond pricing, positioning and supply is **(inference)**. Say in the rationale when the thin seat drove a choice.

### `TEAMS` entry for `exco_round.js` (proposed)

Agent names match the persona files the game's workflow names (`embraer-gomes-neto`, `embraer-santana`, `embraer-meijer`, `embraer-board`). Until this entry replaces the script's built-in Embraer defaults, the game master passes its three strings at run time: `args.rules.embraer` (the `rule`), `args.rules.embraer_cfo` (the `cfo` ground) and `args.rules.embraer_ops` (the `ops` ground). The built-in defaults name leverage and cash as CFO veto grounds, give the ops veto a wider ground than Meijer's two legs, and carry no thresholds and no override margin.

```js
  embraer: {
    board: 'embraer-board', boardName: 'the Embraer S.A. Board of Directors (the Brazilian state holds a golden share)',
    company: 'Embraer', ceo: 'embraer-gomes-neto', cfo: 'embraer-santana', ops: 'embraer-meijer',
    names: { ceo: 'Francisco Gomes Neto', cfo: 'Felipe Santana', ops: 'Arjan Meijer' },
    rule: 'Gomes Neto proposes and decides, bound by the CEO\'s own three launch conditions: a strong product, a strong value proposition and a robust funding strategy that does not put the company\'s financial health at risk. Santana, the CFO, tests the funding on the doctrine inherited from Garcia: a launch needs Team Korea carrying its share of the bill in the brief, ΔPV (debt penalty included) at or above zero in the expected column (the rival plan Gomes Neto names as most likely), and no loss of more than 5 yield points against Hold in the risk column; a launch that fails is vetoed and the veto binds, with no override. Meijer tests the market window and readiness: a launch fails if one new-generation rival type (fps or NGSA) is already in service at its entry into service, or if the brief reports a supply-chain or engine problem that would hold the line; this is a soft veto, binding unless Gomes Neto records an override, as a Board item, for a plan more than 5 yield points better than Hold in the expected column. No launch at all when both fps and NGSA are in service, or due within 2 years, at its entry into service, or while Boeing\'s fps via Embraer is live (company hard rules). Cancel only before entry into service, when writing off beats continuing by more than 2 yield points. Within 2 yield points, hold in 2030 if, in the expected rival plan, a 2035 launch keeps an open window, otherwise launch; launch in 2035 if ΔPV is at or above zero. Any launch and any cancel are Board items. (teams.md; both vetoes are inferences.)',
    veto: {
      cfo: { ground: 'a launch whose funding fails your test: no partner share in the brief, ΔPV below zero with the debt penalty included in the expected column, or a loss of more than 5 yield points against Hold in the risk column', binding: true },
      ops: { ground: 'a launch into a narrow window (one new-generation rival type, fps or NGSA, already in service at its entry into service) or with a supply-chain or engine problem in the brief that would hold the line: a soft veto, binding unless Gomes Neto records an override, as a Board item, for a plan more than 5 yield points better than Hold in the expected column', binding: 'soft' },
    },
  },
```

## 4. Confidence and gaps

- **Decision rights are inferred** from calls. No Board papers or internal memos are in the evidence; the Board-approval chain is known only for the 2018-19 Boeing deal [EB-0087, EB-0090].
- **The operating seat is the weakest:** Meijer has three events and none after November 2024.
- **The CFO seat changed** in May 2026 [EB-0152, EB-0153]; the game seats Santana, whose own record is one call, on the funding test inherited from Garcia.
- **No airliner launch decision** by this team: the tests are built from the turboprop, the E175-E2 and the CEO's stated conditions, not from a launch.
- **Thresholds** (2 and 5 yield points, the window tiers) are integration choices **(inference)**, not revealed behaviour.
- **Korea** is research only (unverified) [EB-0168, EB-0169, EB-0170]; the transcripts show KAI only as a KC-390 partner [EB-0109].
