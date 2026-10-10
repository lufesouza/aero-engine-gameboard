# RTX Corporation Board of Directors: board profile (`pratt-whitney-board`)

This is the research synthesis that the `pratt-whitney-board` agent plays from in the dash-2050 war game. Pratt & Whitney
(P&W) is a business of RTX Corporation, so its big capital decisions go to the RTX board. The board does not originate
orders. Before each round it recommends, and it approves or vetoes every Board item in the package from P&W's ExCo:
Chris Calio (RTX Chairman and CEO, `pratt-whitney-calio`), Neil Mitchill (RTX CFO, `pratt-whitney-mitchill`) and Shane
Eddy (President of Pratt & Whitney, `pratt-whitney-eddy`).

Every claim carries evidence ids or is marked **(inference)**.
- PG- ids are in `board/evidence.jsonl`. P- and PX- ids are in the company and executive evidence files.
- Transcript and filing items (PG-0001 to PG-0040, and PG-0062) are verbatim and machine-checked.
- Web items (PG-0041 to PG-0061) restate what a search summary said. They are never quotes.
- Nine web items have no second search (PG-0046, PG-0048, PG-0051, PG-0052, PG-0055, PG-0057, PG-0059, PG-0060,
  PG-0061). They are used only as **(inference)** and carry no score, test, veto ground or reserved matter.
- Verification (2026-10-10): the verifier's own re-searches of the web items could not be run, because the session's
  search budget was exhausted. The twelve corroborated items rest on the drafter's second search. Where the repo's own
  sources allow, they were cross-checked: the board list in the FY2024 10-K (PG-0062) and the call-transcript speaker
  labels support PG-0041, PG-0043 and PG-0044.

One feature of this board shapes everything below: **the chair is the CEO.** Calio chairs the board and is also one of
the three ExCo agents (PG-0043, PG-0042). In the game the board agent plays the board as a body, led by its independent
directors and its Lead Independent Director, Fredric Reynolds (PG-0044). It does not speak for Calio the executive.

---

## 1. Header

- **Board:** RTX Corporation Board of Directors. Before April 2020 the parent was United Technologies Corporation
  (UTC); RTX was formed by the merger of UTC's aerospace businesses with Raytheon Company (PG-0006).
- **As of:**
  - Composition: the 2026 proxy (2026-03-09) and the annual meeting of 2026-04-30, reported in the 8-K of 2026-05-04
    [PG-0041, PG-0042].
  - Committee charters: dated 2025-05-01 [PG-0047, PG-0053].
  - Latest evidence: 2026-05-04 [PG-0059].
  - Research date: 2026-10-10.
- **Evidence (board file), 62 items:**

  | Kind | Items | Ids | Dates | Status |
  |---|---|---|---|---|
  | transcript | 30 | PG-0001 to PG-0030 | 2015-12-10 to 2025-07-22 | verbatim, 30/30 pass `verify_quotes.py` |
  | filing (10-K) | 11 | PG-0031 to PG-0040, PG-0062 | FY2017 to FY2024 | verbatim, 11/11 pass |
  | web | 21 | PG-0041 to PG-0061 | 2023-11-22 to 2026-05-04 | 12 corroborated by a second search; 9 not |

  - The profile also cites company and executive items from 2012 to 2025 (P-, PX-), mainly on the return hurdle the
    board is told about, the dividend, buybacks, the 2023 accelerated share repurchase (ASR) and the GTF crisis.
  - Only 24 web searches could be run before the session's search budget ran out (`sources.md`).
- **The board's own words:** two items from the Executive Chairman, Tom Kennedy, at the 2021 annual meeting
  [PG-0002, PG-0007]. Everything else about the board comes from the CEO or CFO describing it, from 10-Ks and from proxy
  statements. There are no minutes, no chair's letter in our files and no independent director on record.
- **Confidence overall: Medium.**

  | Area | Confidence | Basis |
  |---|---|---|
  | Composition and committees | High | 2026 proxy, 8-K, charters, releases |
  | Capital-allocation record | High | 10-Ks 2017-2024 and calls 2015-2025 |
  | Pay horizon | Medium-High | proxies 2024-2026 (two items uncorroborated) |
  | Matters reserved to the board | Medium | Finance Committee charter, 10-K; no published dollar threshold |
  | Risk appetite and time horizon | Medium | inferred from decisions and management's account |
  | Safety oversight | Medium | Governance and Public Policy Committee charter; P&W's own Safety Board |
  | How votes are taken | Low | no minutes or vote splits |
  | Reading of rivals | Low | management's words only |

---

## 2. Composition (as of 30 April 2026)

**Board leadership**

| Role | Holder and basis |
|---|---|
| Chair | **Christopher T. Calio**, Chairman, President and CEO. The board elected him chair on 31 January 2025, effective 30 April 2025, when Greg Hayes stepped down as Executive Chairman and left the board [PG-0043]. He was President of Pratt & Whitney and of its commercial engines business before he became RTX COO and then CEO in May 2024 [P-1751, PG-0026]. |
| Chair is CEO? | **Yes.** The roles are combined. RTX's guidelines set no fixed policy on separating them, and the Governance Committee reviews the structure [PG-0045] **(inference: this part of PG-0045 rests on one search)**. In 2026 the board still judged a combined chair and CEO, with a largely independent board and an independent lead director, to be the right structure [PG-0042]. |
| Lead Independent Director | **Fredric G. Reynolds**, since 1 December 2023, succeeding Dinesh Paliwal [PG-0044]. Retired CFO of CBS [PG-0002, PG-0003]. He also chairs the Audit Committee [PG-0044]. The independent directors designate the lead director [PG-0045]. The board waived its age-75 rule so that he could stand again in 2026 [PG-0046] **(inference: uncorroborated)**. |
| Size | **10** directors elected on 30 April 2026 [PG-0041]. One search summary counted eleven; the proxy agenda and the 8-K say ten [PG-0041]. In February 2025 the board had 12, including Hayes and Winnefeld [PG-0062]. The 2020 merger agreement set 15 seats [PG-0006]. |
| Independence | **9 of 10**: every director but Calio is independent [PG-0042]. |

**Directors (2026 slate)** [PG-0041]

| Director | Background | Why it matters in the game |
|---|---|---|
| Tracy A. Atkinson | Retired EVP of State Street [PG-0002] | Finance |
| Christopher T. Calio | Chair and CEO; ex-President of P&W [P-1751, PG-0043] | The GTF's own executive chairs the board |
| Leanne G. Caret | A director by February 2025 [PG-0062]; background not in the board evidence. A Leanne G. Caret was named President and CEO of Boeing Defense, Space & Security in 2016 (Boeing call of 2016-06-08 in the repo transcripts); that this is the same person is **(inference)** | Gap; possibly Boeing defence experience |
| Bernard A. Harris Jr. | Astronaut; CEO of Vesalius Ventures [PG-0002] | Technology and space |
| George R. Oliver | Chairman and CEO of Johnson Controls (2021); counted by the CEO as commercial-aerospace experience [PG-0002, PG-0004] | Chairs the Governance and Public Policy Committee (product safety and quality) from 30 April 2026 [PG-0052] **(inference: uncorroborated)** |
| Ellen M. Pawlikowski | Retired USAF general; ex-Commander, Air Force Materiel Command [PG-0002] | Defence acquisition |
| Denise L. Ramos | Retired CEO of ITT; counted as commercial-aerospace experience [PG-0002, PG-0004] | Industrial operations |
| Fredric G. Reynolds | Lead Independent Director; Audit chair; ex-CFO of CBS, "great financial mind" [PG-0044, PG-0003] | Financial controls, risk |
| Brian C. Rogers | Retired Chairman of T. Rowe Price [PG-0002]; brought in as one of the "people focused on what investors ... are focused on" [PG-0003] | The investor's view |
| Robert O. Work | Former Deputy Secretary of Defense [PG-0002]; chaired the Governance and Public Policy Committee in 2025 [PG-0052] **(inference: uncorroborated)** | Defence |

- **Balance:** of the nine independents, three come from finance or investing (Atkinson, Reynolds, Rogers), two are
  former industrial CEOs (Oliver, Ramos) and three bring defence or space credentials (Pawlikowski, Work, Harris)
  [PG-0002, PG-0004]; Caret's background is not in our evidence (see the table).
- **The commercial-aerospace bench has thinned.** In 2021 the CEO named Larsen (ex-Goodrich), Ortberg (ex-Rockwell
  Collins), Ramos and Oliver as the board's commercial-aero experience [PG-0004]. Larsen and Ortberg had left by February
  2025 [PG-0062]; Winnefeld, still a director then [PG-0062], is not on the 2026 slate [PG-0041]. In our evidence the only
  director with engine-programme experience is the CEO-chair **(inference)**.
- **Departures that matter:** Hayes left the board in 2025 [PG-0043]; Paliwal, lead director since the merger, left in
  December 2023 [PG-0044, PG-0001].

**Committees** [PG-0032]

| Committee | Role in the game | Ids |
|---|---|---|
| Finance | Reviews significant capital appropriations, dividend policy and buyback programmes, financing of long-term capital needs, and reports on significant acquisitions and divestitures. Meets about four times a year and reports to the full board. The CEO was a member in 2025 [PG-0048, inference]. **The committee that sees a new engine programme or a Joint Venture first.** | PG-0047 |
| Audit | Financial and compliance risk; receives the top enterprise risks every year; chaired by the lead director | PG-0033, PG-0034, PG-0044 |
| Governance and Public Policy | **Product safety and the quality management system**, safety-regulator engagement, complaint handling; board leadership structure and nominations. Quality and AI were added in 2024 [PG-0051, inference] | PG-0050, PG-0045 |
| Human Capital and Compensation | Executive pay and human capital; sets incentive metrics and adjustments | PG-0032, PG-0058, PG-0020 |
| Special Activities | Classified business, including programmes and deals with special performance, financial or reputational risk; product cybersecurity | PG-0053, PG-0033 |

There is **no stand-alone safety committee and no technology committee** [PG-0032, PG-0050]. Commercial engine
programmes have no board committee of their own; they reach the board through Finance and the full board **(inference
from PG-0047, PG-0053)**.

**Shareholders.** No controlling, family or state shareholder appears in our evidence. Shareholders back the board and
its pay plans by wide margins: 91% for say-on-pay in 2021 [PG-0009], about 96% in 2026 [PG-0059] **(inference:
uncorroborated)**. The US government is RTX's largest defence customer and, since October 2024, a monitor of its
compliance under deferred prosecution agreements [PG-0040]. Half of RTX's business is commercial aerospace [P-1366].
P&W's GTF partners carry 49% of programme costs [P-1563].

---

## 3. Governance

### Matters reserved to the board

| Matter | Rule and threshold | Ids |
|---|---|---|
| Dividends and share repurchases | At the board's discretion, weighed against "other investment opportunities", strategy and financing terms. The board declares each quarterly dividend and authorises each buyback programme | PG-0031, PG-0038, PG-0035, PG-0036, PG-0037 |
| Significant capital appropriations, financing, major transactions | Reviewed by the Finance Committee, reported to the full board. **No published dollar threshold** | PG-0047, PG-0049 |
| Project gate by size | "They come up through me, through Greg, up to our Board, depending on the various sizes": the CFO, then the CEO, then the board | P-1285, PX-0199 |
| New engine bids | Management tells the board the return it must see before it bids, and keeps to it | P-0731 |
| Programme value review | The GTF's NPV is reviewed with the board every year; the intrinsic-value model (8% cost of capital, product-line level) is shared a couple of times a year | P-1191, PG-0024, P-1163 |
| Portfolio and M&A | The UTC separation, Rockwell Collins and the Raytheon merger were board decisions after long reviews | PG-0014, PG-0022, PG-0013 |
| CEO succession | A three-year board process chose Calio; succession is discussed at every meeting | PG-0026, PG-0025, PG-0005 |
| Enterprise risk, cybersecurity, product safety and quality | Annual top-risk review; cyber split between the board, Special Activities and Audit; safety and quality with Governance and Public Policy | PG-0034, PG-0033, PG-0050 |

### How the board decides

- **Process:** committees review and report to the full board [PG-0047]. On a big decision management commits "to
  provide them with all the data, with all the thinking" [PG-0016]. The board frames the question as its own, the best
  way to create "long-term shareowner value", with doing nothing an option [PG-0017], and it ran a year-long review of
  the portfolio before the separation [PG-0014].
- **Debate, then backing:** the ASR was preceded by "a fulsome discussion with the Board about the timing" [PG-0029],
  and the board then backed management's view.
- **Tempo:** slow and evidence-heavy on structural moves (the separation took "more than a yearlong comprehensive
  evaluation") [PG-0014]; fast on capital returns once liquidity allows (a new buyback authority in December 2020, while
  commercial aerospace was still depressed) [PG-0036].
- **Votes:** no vote splits are public. Board decisions are taken by the directors as a body and announced as "the
  Board" [PG-0028, PG-0008] **(inference: majority rule assumed)**.

### Delegation to management

- RTX sets the self-funded R&D and capex envelope, about $6B a year by 2025 [P-0499, PX-0268]. P&W decides durability
  upgrades, pricing and the fleet plan inside it (`executives/teams.md` §1).
- A new centreline engine is outside the plan: "the outlook we provided today does not contemplate a new centerline
  engine" [P-0745, PX-0202]. Launching one is a board matter **(inference from P-1285, P-0731, PG-0047)**.
- Ending a failing programme has been a CEO decision: Calio terminated a Raytheon fixed-price development and took the
  charge [P-1342, PX-0064].

### Board items in the game

Every order that differs from the default (`hold`) is a Board item.

| Order | Real reserved matter | Below the real threshold? | Ids |
|---|---|---|---|
| `gtf2_solo: launch` | A new engine programme: a significant capital appropriation ($2B over six years on the board) and a strategic commitment. The NMA engine bid went to the board against a set return | No **(inference)**: a $2B programme commitment would go up to the board, though it is only about $0.33B a year, 5-6% of the envelope | P-1285, PG-0047, P-0731, P-0745, P-0499 |
| `gtf2_solo: launch_if_selected` | The same programme, conditional on a selection: the form the real doctrine prefers (no engine without a committed airframe) | No **(inference)** | P-0746, P-0737, P-0711 |
| `gtf2_solo: cancel` | Ending a programme and taking a write-off of up to $2B; in the record a CEO decision | **Possibly yes** **(inference)**: reviewed as part of the round's package | P-1342, PX-0064 |
| `jv_with_rr: commit` | A strategic collaboration with a rival that is public at once, and a $2B share; reported to the Finance Committee as a significant transaction **(inference)**. RTX shares risk and investment through Joint Ventures, never technology | No **(inference)** | PG-0047, P-1233, P-1563 |
| `jv_with_rr: withdraw` | Ending a public commitment before the Joint Venture forms | **Possibly yes** **(inference)**: reviewed as part of the package | P-1875 |
| `hold` (and Do Nothing) | Not a Board item. Never vetoed | n/a | |

Lobbying, Delay Tactics, the 737 rate and GEnx packages are not P&W orders.

### Tests the board can apply from the ExCo package and the brief

The agent file (`pratt-whitney-board.md`, "Your tests") gives the computable form of each test; this table is the
research basis. The board approves or vetoes the items it is given; it never orders one.

| Test | Threshold or rule | Ids |
|---|---|---|
| Unresolved objection | No Board item carries a binding CFO or operating-head veto the CEO did not respect, or an unanswered red-line flag; the team rule allows no override **(inference: mapping)** | P-1285, PX-0199, PG-0016 |
| Return hurdle | The item beats `hold` in weighted expected ΔPV on the grid, which discounts at the dashboard's 10% WACC (`dashboard_game.md` §2), above the 8% of the value model; the return must be "well in excess of cost of capital", as the GTF's had to be. Below it, "buy stock back" | P-0715, P-1163, P-1165, P-0731, P-1243, PG-0024 |
| Committed airframe | An unconditional `launch` needs a selection of P&W on the public record, or a franchise-defence case for Airbus's next single-aisle that beats `launch_if_selected` on the grid (missing a cycle shuts a maker out for decades); otherwise the board expects `launch_if_selected` | P-0746, P-0737, P-0711, P-1367, P-1347, P-1868, P-2058 |
| Bounded downside | No item loses more than its own $2B against `hold` in a plausible column; an unselected `launch` names its cancel round where one exists **(threshold: inference)** | P-0609, PG-0029, PG-0019 |
| Proof before commitment | "When we've seen it and when we feel good about it, we've invested": the case counts selections, partner commitments and money only once they are on the public record | P-1367, PX-0311, PX-0350, PG-0039 |
| Durability first | The operating head's memo shows each engine ready by the EIS it serves, with durability and time on wing, not efficiency alone; no repeat of the 2016-2023 entry-into-service problems | P-1360, P-1214, P-1215, PG-0050, PG-0023 |
| Dividend and envelope | No plan that needs a dividend cut or interrupts the return to pre-ASR debt; on the dashboard, new R&D must fit the self-funded envelope **(inference: mapping)** | P-0566, PG-0010, PG-0031, P-0686, P-0499, PX-0268 |
| Joint Venture | Commit only when Rolls-Royce has committed or an airframer signals the Joint Venture engine; core technology stays with P&W | P-1233, P-1875, P-1563, PG-0047 |
| Premature exit | A `cancel` or `withdraw` passes only if it is no worse than `hold` on the grid; a `cancel` while an airframer can still select GTF2 in time needs the cancel row ahead in every plausible column **(inference from ROIC in pay and the CEO's record of cutting losses)** | P-1342, PG-0019, P-1191 |
| Miss a cycle, disclosure | Recommendations only, never vetoes: suggest `launch_if_selected` where the ExCo holds and GTF2 could still be ready; keep the public statement to proven durability and launch + 6 **(inference)** | P-1347, P-1126, PG-0039, PG-0050 |

---

## 4. Culture

**Calibration (final cross-check across the five boards, 2026-10-10).** The scores are judgements from the evidence,
labelled as such, and were calibrated across the five boards so that a score means the same at each; no score changed
at the cross-check. Risk aversion: 3 = balanced (approves debt-funded returns or large deals while programme risk is
live); 4 = averse (the rating and safety come first and proof comes before commitment, yet staged, shared or
derivative programme risk is approved and cash is returned from a sound balance sheet); 5 = a board in crisis (returns
cut, capital raised, nothing unproven funded). Time horizon: 2 = near-term (development cut first, or cash returned
first while the next programme waits); 3 = balanced (core developments protected, but most spare cash returned or
used to repay debt, and pay on one-to-four-year metrics); 4 = long-term leaning (also a multi-decade programme prepared
for years and kept whole while returns stay moderate). This board: risk aversion at the low end of the 4 band, strict on programmes but with the
debt-funded buyback of October 2023 still recent [PG-0028, P-1554]; time horizon in the 3 band: R&D was the first
cut in the 2020 shock [P-1372], but since 2024 debt and the dividend come before buybacks, inside a self-funded
engine envelope [P-0686, P-0499] (placements: inference).

### Risk aversion: **4 / 5** (averse to programme and integrity risk; demands proof before commitment; has tolerated balance-sheet risk for shareholder returns)

**Rationale**

*Programme risk: strongly averse*
- No new engine without a business case that clears the hurdle the board was told about, and only as sole source on a
  committed airframe [P-0731, P-0715, P-0746, P-0737].
- P&W matched Boeing's non-commitment on the NMA engine and would not spend $1.5B without a proven case [P-0711, P-0713].
- RTX invests "when we've seen it and when we feel good about it" [P-1367]. The 2021-25 plan held no new centreline
  engine [P-0745].
- Since the GTF crisis the chair-CEO puts durability and time on wing ahead of efficiency [P-1360, P-1361].

*Integrity and safety exposure*
- Shareholders allege that directors failed to oversee the GTF and its disclosures (derivative suits pending) [PG-0039];
  the securities class action was dismissed in September 2025 [PG-0060] **(inference: uncorroborated)**.
- Since October 2024 RTX operates under deferred prosecution agreements with an independent compliance monitor [PG-0040].
- The board formalised oversight of product safety and quality in the Governance and Public Policy Committee [PG-0050],
  adding quality in 2024 [PG-0051] **(inference: uncorroborated)**.

*Balance sheet: protected now, but not always*
- The dividend is "sacrosanct", stress-tested with the board in April 2020 and kept through COVID [P-0423, PG-0011,
  PG-0010].
- Since 2024 the order is debt first: buybacks return only once debt is back to pre-ASR levels [P-0686, P-0669,
  PX-0353].

**Why not 5**
- In October 2023, three months into the powder-metal recall, the board approved an $11B buyback authority with a $10B
  debt-funded ASR [PG-0028, PG-0035, P-0603]. It had debated the timing and judged the liability bounded [PG-0029, P-0609]. S&P
  had already cut RTX to BBB+, and both agencies moved to a negative outlook on the ASR; net debt rose from $25.7B to
  $37.2B [P-1554, P-1884, P-1878].
- The board takes large, long-cycle bets when the strategic case is strong: Rockwell Collins (about $30B, accepting
  "a little hit" on return expectations) and the Raytheon merger [PG-0021, PG-0022, P-0320, PG-0013].
- The chair-CEO's stance is "an and, not an or": growth investment and capital returns together [P-1368].

**Trend**
- **About 3 in 2015-2023 (UTC and early RTX):** strict programme discipline [P-0715, P-0731] alongside heavy, partly
  debt-funded buybacks and acquisitions [P-0174, P-1402, PG-0022, PG-0028].
- **4 since 2024:** after the powder-metal charge ($2.9B net to P&W, $2.2B after tax to RTX) [P-1563, P-1545], the
  downgrade [P-1554], the derivative suits [PG-0039] and the compliance monitor [PG-0040], the board puts deleveraging,
  durability and quality first [P-0686, P-1360, PG-0050].
- **Likely to ease as debt falls:** management expects buybacks to become "a more standard part of our playbook" again
  [P-0669]. The easing is **(inference)**.

**How it shapes votes.** The board approves `launch_if_selected` readily and an unconditional `launch` only on a
selection or a franchise-defence case; it approves a Joint Venture only when the partner has committed; it vetoes any plan
whose case rests on unrecorded selections or that strains the dividend or deleveraging **(inference from the tests in §3)**.

### Time horizon: **3 / 5** (balanced: a long-term NPV lens on programmes, medium-term pay, and a steady priority on cash returns)

**Long-term**
- Capital decisions rest on an intrinsic-value model discounted at about 8%, shared with the board a couple of times a
  year, with GTF costs inside it [P-1163, PG-0024].
- UTC "overinvested" in P&W for about a decade, sacrificing margin for the franchise [P-1126, P-1219], and reviewed the
  GTF's whole-programme NPV with the board every year [P-1191].
- By 2016 the long-term incentive EPS goal was 6% instead of the traditional 10% (the 2015-17 plan), because the engine
  investments were weighing on near-term earnings; the compensation committee "looks at all that" [PG-0020]. The board
  reset the pay goal rather than the investment **(inference)**.
- The board asked whether the conglomerate had under-invested in Otis and Carrier in pursuit of margin [PG-0015]; it
  frames its test as "long-term shareowner value" [PG-0017, PG-0013] and approved Rockwell Collins on "the long-term
  nature of the aerospace business" [PG-0022].
- Succession aims at "the right leadership for the business over the long haul" [PG-0005]; Hayes saw Calio leading
  "for the next decade or so", with "the full support of the Board" [PG-0027].

**Short to medium term**
- Pay: the annual bonus rests on one year's adjusted earnings and free cash flow [PG-0056] (80% in 2024 [PG-0057],
  inference); the long-term award is a three-year plan on EPS growth, ROIC and relative TSR [PG-0054, PG-0019].
- Cash returns are large and steady: $22B in 2015-17 while the GTF ramped [P-0174, P-0240], a commitment raised to
  $36-37B from the 2020 merger to 2025 [P-0603, PG-0030], dividends above net income in 2023 [P-1888].
- Development spending is the first discretionary cut in a shock [P-0467, P-1372]; R&D fell from 4.2% to 3.6% of sales
  in 2021-24 [P-1885].
- A new engine must beat buying back RTX stock [P-1165, PG-0029].

**Trend**
- **About 4 in 2008-2016:** the GTF build-out and the cut in the long-term EPS goal [P-1126, PG-0020].
- **About 2-3 in 2017-2023:** capital-return commitments grow and the 2023 ASR is timed to the share price [P-0603,
  PG-0029].
- **3 now:** debt paydown and the dividend come first, with continued investment in GTF Advantage and enabling technology
  rather than a new engine [P-0686, P-0788, P-0757]. NGSA is expected "maybe mid-next decade" [P-2058].

**How it shapes votes.** The board accepts a $2B programme whose payback lies beyond the three-year pay window if the NPV
case is clear and the airframe is committed; it resists spending that depresses EPS and ROIC inside the window without a
selection in hand **(inference from PG-0054, P-1163)**.

### Capital allocation priorities

1. **The dividend:** "sacrosanct", declared by the board each quarter [P-0566, PG-0038]; the per-share dividend rose
   every year from 2021 to 2025 [P-1887, PG-0038, P-0677]; paid every year since 1936 [PG-0061 (inference)].
2. **Deleveraging to pre-ASR debt** before buybacks restart [P-0686, P-0669, PX-0353].
3. **Self-funded investment** of about $6B a year in R&D and capex [P-0499, PX-0268].
4. **Buybacks as the residual** ("the fill in") and bolt-on M&A only [P-0566, P-1357, P-1320].
The board renews buyback authorities routinely (2015: $12B; 2020: $5B; 2021: $6B; 2023: $11B) [PG-0037, PG-0036,
P-0500, PG-0035].

### Safety oversight

- **Board level:** product safety and the quality management system sit with the Governance and Public Policy Committee
  [PG-0050]. There is no safety committee [PG-0032].
- **Company level:** P&W's own Safety Board overrode a low inspection fallout rate and forced the 2023 fleet action
  [P-1028]. RTX's stated policy is to "make the airlines whole" [P-0591].
- **Lessons the board heard:** after the GTF's entry-into-service problems, management "talked about this with the board
  ... ad infinitum" and promised it "will never happen again" [P-1215].
- **Exposure:** directors face derivative claims over GTF oversight [PG-0039].
- **The board sees the hardware:** it held a meeting at P&W and visited the GTF test cell [PG-0023].

### Stakeholder influence

- **Shareholders:** widely held; strong support for the board and pay [PG-0009, PG-0059 (inference)]. Investor-minded
  directors were recruited deliberately [PG-0003].
- **US government:** defence customer and compliance monitor [PG-0040].
- **Partners:** GTF partners carry 49% of the programme [P-1563]; RTX values the partnership as "critical" [PX-0038].

### Pay horizon

| Plan | Horizon and metrics | Ids |
|---|---|---|
| Long-term (PSUs) | Three years: adjusted EPS CAGR 35%, ROIC 35%, relative TSR 30% (core A&D peers 15%, S&P 500 15%). Stock awards have rested on company-wide ROIC since before the 2020 merger | PG-0054, PG-0019, PG-0018 |
| Annual bonus | One year: adjusted net income (business units: segment operating income) and free cash flow; purely financial in 2025 | PG-0056 |
| Adjustments | The long-term EPS goal was set at 6%, not 10%, while engine investment weighed on earnings (2015-17 plan), and the committee pre-authorised neutralising tariffs (2025) | PG-0020, PG-0058 |
| Directors | A fixed annual retainer, no bonus | PG-0012 |

ROIC in the long-term plan since 2016 makes capital "not free" [PG-0019]: a $2B engine charged in full weighs on the
three-year ROIC unless a selection brings revenue inside the window **(inference)**.

---

## 5. Decision record

| Date | Decision | Ids |
|---|---|---|
| 2015-10-14 | $12B buyback authorisation (UTC) | PG-0037 |
| 2015 | Sale of Sikorsky for $9B; proceeds returned through a $6B ASR | P-1402 |
| 2015-12 | ROIC added to the long-term incentive plan from 2016 | PG-0019 |
| 2015-16 | Long-term EPS goal set at 6% instead of 10% (2015-17 plan) while engine investment weighed on earnings | PG-0020 |
| 2017-06 | Dividend raised 6%, faster than earnings, on the aerospace backlog | P-0241 |
| 2017 (summer) | Acquisition of Rockwell Collins, accepting a lower return | PG-0022, PG-0021 |
| 2018-11 | Separation of UTC into three companies after a year-long review | PG-0014 |
| 2019-02 | NMA engine bid only against the return told to the board; sole source | P-0731, P-0737 |
| 2019-06 | Merger with Raytheon; 15-seat board, Executive Chairman Kennedy | PG-0013, PG-0006 |
| 2020-04/05 | COVID: dividend kept after stress tests; buybacks suspended; R&D and capex cut | PG-0010, PG-0011, P-0423, P-1372 |
| 2020-12-07 | New $5B buyback authorisation | PG-0036 |
| 2021-04-26 | Dividend raised 7%; Kennedy retires, Hayes to be Chairman and CEO | PG-0008, PG-0007 |
| 2021-12 | $6B buyback authorisation | P-0500 |
| 2022-02 | Calio made COO over all businesses as part of succession | PG-0025 |
| 2023-10-21 | $11B buyback authority including a $10B ASR, during the powder-metal recall | PG-0028, PG-0029, PG-0035 |
| 2023-12-01 | Reynolds named Lead Independent Director | PG-0044 |
| 2023-12 / 2024-05 | Calio named CEO after a three-year process; Hayes Executive Chairman | PG-0026 |
| 2024 | Governance Committee charter extended to product quality and AI | PG-0051 **(inference: uncorroborated)** |
| 2025-01 | Tariff effects neutralised in incentive metrics | PG-0058 |
| 2025-01-31 | Calio elected Chairman (effective 2025-04-30); Hayes leaves the board | PG-0043, PG-0062 |
| 2025-07 | Dividend raised 8% | P-0677 |
| 2026-03 | Age-75 waiver for the Lead Director | PG-0046 **(inference: uncorroborated)** |
| 2026-04-30 | Dividend raised 7.4% | PG-0061 **(inference: uncorroborated)** |

No board-level decision on a new commercial engine programme since the GTF appears in our evidence.

---

## 6. Relationship with management

- **Combined chair and CEO is the RTX default.** Hayes was Chairman and CEO of UTC; the merger brought an Executive
  Chairman (Kennedy) for one year; Hayes was chair and CEO again from June 2021; Hayes was Executive Chairman beside Calio
  as CEO in 2024-25; Calio has been chair and CEO since April 2025 [PG-0006, PG-0007, PG-0026, PG-0043].
- **The board defers, but questions first.** It ran its own year-long review of the separation [PG-0014, PG-0017],
  demanded all the data on big decisions [PG-0016], and debated the ASR before backing it [PG-0029].
- **Supportive of management's pay and capital plans:** it adjusted incentive goals during the GTF build-out [PG-0020]
  and for tariffs [PG-0058]. No capital-return step that management announced is recorded as refused (§5)
  **(inference)**.
- **Tensions:** none visible between the board and management. The tension is external: shareholders allege a failure
  of board oversight on the GTF [PG-0039].
- **The three ExCo agents:**
  - **Calio (CEO and chair):** the board's own choice after a three-year process, with "the full support of the Board"
    [PG-0026, PG-0027]. His record: durability first [P-1360], cut a failing programme [P-1342], invest when demand is
    visible [P-1367].
  - **Mitchill (CFO):** runs the gate that escalates to the board by size [PX-0199]; holds the dividend and the rating as
    fixed constraints [PX-0282] and puts debt back to pre-ASR levels before buybacks [PX-0353]. The board reads his memo
    for the cash and return case.
  - **Eddy (President of P&W):** the board's evidence on him is the 2023 Investor Day: fleet durability and the
    industrial recovery [PX-0116, PX-0120]. There is no direct board evidence on him. The board reads his memo for
    durability and readiness.

---

## 7. How it reads rivals

There is no board-level statement about CFM/GE, Rolls-Royce or the airframers in our evidence. Management's views that
the board has heard:
- Stand-alone engine makers without big balance sheets find long-term engine investment harder to finance [P-2063]; the
  conglomerate let P&W afford programmes it could not fund alone [P-1138, P-0378].
- Rolls-Royce's own account: it could not make a business case for an A320neo engine when P&W could [P-1868], and a Joint
  Venture with P&W holds only while both partners are on the same new engine [P-1875].
Anything beyond this is **(inference)** and should be avoided.

---

## 8. Confidence and gaps

- **Thin:**
  - Only two items in the board's own words (Kennedy, 2021) [PG-0002, PG-0007]. No independent director, including the
    Lead Director, is on record in our sources.
  - No published dollar threshold for board approval of capital spending [PG-0049].
  - No vote splits or minutes; how the board reaches a decision is inferred from management's account.
  - No board statement on a next-generation narrowbody engine or a Joint Venture with Rolls-Royce.
  - Leanne Caret's background (a likely Boeing defence background is inference only) and the full committee rosters
    were not found; when Winnefeld left the board is not in our evidence.
  - Nine web items lack a second search (search budget exhausted after 24 searches), and the verifier could not re-run
    any web search; the composition is cross-checked against the FY2024 10-K list (February 2025) [PG-0062].
  - Eddy's board relationship rests on one event (2023).
- **Fallback when the evidence is silent:**
  1. Apply the company doctrine in `profile.md` (return hurdle, sole source, dividend first, Joint Ventures share risk
     not technology).
  2. Read the decision record in §5 for the nearest precedent.
  3. Defer to the CEO's case unless a test in §3 fails.
  4. Never invent a board view.
