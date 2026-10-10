# Airbus SE Board of Directors: board profile for the war game (`airbus-board`)

**Evidence tags.** AG- ids are in `board/evidence.jsonl` (this folder). A- and AX- ids are the company and executive
files (`../evidence.jsonl`, `../executives/evidence.jsonl`), cited unchanged. Filing quotes are verbatim and machine-checked;
web items record a search summary's statement, never a quote. **(inference)** marks my derivation. Uncorroborated web
items (AG-0060, AG-0061, AG-0069) are used only as (inference) and carry no score, test or veto. AG-0064 is corroborated
but is an analysts' projection, so it too is used only as (inference). **Independent re-check (2026-10-10):** a second
agent re-searched 31 of the 34 web items (30 searches): 30 confirmed, 1 corrected (AG-0070: agreement dated 27 April
2025, not 17 April), none dropped; AG-0060, AG-0061 and AG-0069 were not re-searched (`"verified"` field in the evidence).

---

## 1. Header

| | |
|---|---|
| Board | Airbus SE Board of Directors (one-tier board, Dutch SE, seat in Amsterdam/Leiden) |
| Agent | `airbus-board`; executives `airbus-faury` (CEO), `airbus-toepfer` (CFO), `airbus-wagner` (CEO Commercial Aircraft) |
| As of | **10 October 2026** for composition (latest source: Airbus release of 1 October 2026, AG-0042, AG-0043); governance rules as of the FY2025 Board Report issued 18 February 2026 |
| Evidence | **75 board items**: 0 transcript, **41 filing** (FY2025 Board Report, all pass `verify_quotes.py`), **34 web** (31 corroborated by a second search, 3 not; 31 re-checked by an independent search on 2026-10-10). Plus 65 company and executive items cited by id |
| Dates | Filing 2026-02-18; web 2012-12-05 to 2026-10-10 (undated pages carry the retrieval date, 2026-10-10) |
| Confidence overall | **Medium.** High on rules (reserved matters, majorities, pay design), medium on culture (inferred from decisions, not from board speech), low on individual directors' views and on the new chair's style |

There are no Airbus earnings-call transcripts in the repo, so the board never speaks in its own spoken words here. Its
voice is the Board Report (filing) and Airbus press releases (web).

---

## 2. Composition (as of 10 October 2026)

**Size and structure.** 12 directors on staggered three-year terms [AG-0001]. One executive director, the CEO; eleven
non-executives, all of whom qualified as independent, chair included, at the FY2025 report [AG-0002]. At least a third
of seats are renewed or replaced each year [AG-0005]. The board met 11 times in 2025, with Audit 7, RNGC 6 and ECSC 6
meetings, at 95% attendance [AG-0009].

**Leadership.**
- **Chair: Amparo Moraleda** since 1 October 2026 [AG-0042]. She is Spanish, has been on the board since 2015, and was formerly General Manager of IBM Spain and Portugal and COO of Iberdrola's international division [AG-0044]. She is the first woman and the first Spaniard to chair Airbus [AG-0042]. Until October 2026 she chaired the RNGC and was therefore lead independent director [AG-0023, AG-0024].
- **Lead Independent Director and RNGC chair: Mark Dunkerley** since 1 October 2026 [AG-0043]. The chair of the RNGC is automatically the lead independent director, who appraises the chair and mediates between directors [AG-0024]. He has an airline-industry background and sat on the board of Spirit Airlines [AG-0047].
- **CEO: Guillaume Faury**, the only executive director [AG-0026]. He was selected in October 2018 [AG-0051] and renewed at the 2025 AGM for three years [AG-0072]. His mandate runs to April 2028, and the renewal decision is expected in 2027 [AG-0048].
- **Previous chair: Rene Obermann**, chair from April 2020 [AG-0045] until he left on 1 October 2026 for SAP [AG-0042]. He came from technology and private equity, not aerospace [AG-0008].

**Committees** (membership as of the FY2025 report, updated where 2026 sources say so):

| Committee | Chair | Role that matters in the game | Ids |
|---|---|---|---|
| Audit Committee (5 NEDs: Gemkow, Dunkerley, Guillouard, Hopke, Wood) | Stephan Gemkow (since the 2025 AGM) | Prepares the accounts approval and oversees the enterprise risk system (ERM). Tests the cash and risk case of a programme. The CFO is its management interface | AG-0020, AG-0021, AG-0032, AX-0107 |
| Remuneration, Nomination and Governance Committee (RNGC) | Mark Dunkerley (from 1 Oct 2026) | Pay targets and scenarios, CEO and ExCo appointments, succession. Runs the 2027 CEO decision | AG-0023, AG-0029, AG-0043, AX-0028 |
| Ethics, Compliance and Sustainability Committee (ECSC, 6 NEDs) | not confirmed for 2026 | Integrity and compliance. The natural reviewer of any covert move (Delay Tactics) | AG-0022, AG-0053 |
| No safety or technology committee | | The full board reviews product safety twice a year | AX-0015, AG-0022 (inference) |

**Directors whose background bears on decisions** (as of 10 October 2026):
- **Antony Wood**: former CEO of Meggitt and former President of Rolls-Royce Aerospace (2013-16). He is the engine and supplier-risk insider [AG-0046], sits on the Audit Committee [AG-0020] and was renewed in 2026 [AG-0041].
- **Stephan Gemkow**: chairs the Audit Committee [AG-0020] and is a former Lufthansa CFO, with 22 years at Lufthansa [AG-0047]. He was renewed in 2026 [AG-0041].
- **Henriette Hallberg Thygesen**: CEO of Terma (defence and aerospace). She joined in 2026 for three years [AG-0041].
- **Oliver Zipse**: chairman of the BMW board of management when appointed, a high-volume industrial operator. He joined in April 2026 for one year, completing Victor Chu's mandate [AG-0041].
- **Christophe Fouquet**: CEO of ASML, a technology-intensive manufacturing business. He was co-opted on 1 October 2026 [AG-0042].
- **Jean-Pierre Clamadieu**: RNGC member [AG-0023]. He leaves at the 2027 AGM, and Florent Menegaux (CEO of Michelin) is to succeed him [AG-0043].
- Also: Catherine Guillouard and Doris Hopke (Audit; Hopke also sits on the RNGC) [AG-0020, AG-0023], and Irene Rummelhoff, a director since 2022, re-elected in 2025 to 2028 (FY2025 board list [AG-0075]; no 2026 source records her leaving; background not confirmed in evidence).
- **Skills mix** (2025 skills matrix, before the 2026 changes): seven of twelve had aerospace experience and three defence experience [AG-0007]. Recruiting targets expertise in the industry's technology challenges [AG-0015].
- **Left in 2026:** Victor Chu and Feiyu Xu at the April AGM [AG-0041], and Obermann on 1 October [AG-0042].

**Shareholders and states.**
- At 31 December 2025 the French state held 10.83% (Sogepa), the German state 10.82% (GZBV/KfW) and the Spanish state 4.08% (SEPI); the public held 74.27% [A-0381].
- A 2013 pact keeps the states' combined votes under 30% [A-0382, AG-0050]. Since that reform no group of directors and no shareholder has a veto [AG-0050, AX-0027].
- The states have no right to nominate directors [AG-0003]. However, two directors must also be French, and two German, Defence Outside Directors [AG-0004].
- Under the pact, directors vote freely on reserved matters [AG-0036]. Unless France (Sogepa) and Germany (GZBV) both agree, the pact's holders vote against any change to the Board Rules or the Articles at the AGM, so either state can swing the pact's votes against a governance change [AG-0037].

---

## 3. Governance: reserved matters, votes, delegation

**Delegation.**
- The board approves the strategy and delegates its execution and day-to-day management to the CEO. The CEO may not enter reserved transactions without board approval [AX-0026].
- Requests for board approval are first discussed and approved in the Executive Committee, so the board sees a single management case [AG-0026].

**Matters reserved to the board** (Simple Majority unless noted):
- The strategy, and the **Yearly Budget**, including the plans for investment, R&D and major programmes [AX-0026, A-0297].
- **Any change in the nature and scope of the business**, and the relocation of material activities [AG-0010].
- **Investments, programme launches, acquisitions and divestments above €300 million** [A-0298, AG-0049]. These need a **Qualified Majority above €800 million** [AG-0049].
- **Qualified Majority** also for appointing or removing the Chair and the CEO, for strategic alliances and for moving the headquarters [AG-0049].
- **Shareholder policy, major capital-market actions and announcements, and anything that involves "an abnormal level of risk"** [A-0299]. All key market disclosures are board-approved [AX-0004].
- **Dividend proposals** to the AGM [A-0300]. Buybacks run under an 18-month AGM authority capped at 10% of capital [AG-0035]. The board's own share-issuance authority is tiny, so a real equity raise goes to the shareholders, and the states vote there [AG-0034].
- **Executive Committee appointments** proposed by the CEO [AX-0028]. The CEO's pay and targets are set by the board on RNGC advice [AG-0029, AX-0070].

**Votes.**
- Most decisions pass by Simple Majority; some need two-thirds (Qualified Majority), and no individual director or class of directors has a veto [AX-0027].
- A Qualified Majority matter needs ten of twelve directors present (eight at a reconvened meeting) [AG-0011].
- In the game the board agent speaks as one voice. A Qualified Majority item is read as "the case must persuade a broad majority, including the finance and industrial directors" **(inference)**.

**Tempo.** About monthly meetings [AG-0009], an annual strategy off-site [AG-0016], scheduled and ad hoc reviews of top risks [AG-0014], and rolling forecasts and scenario reviews [AX-0007]; emergency decisions within days in a shock [AG-0054].

### How the game's Board items map onto the real reserved matters

| Order (dash-2050) | Size on the board | Real reserved matter | Majority | Below the real threshold? |
|---|---|---|---|---|
| `ngsa: launch` (+ `ngsa_engine_code`) | $30.07B (slide $20B) | Programme launch above €800m; Yearly Budget, major programmes [AG-0049, A-0297] | Qualified | No |
| `rea350: launch` | $5B | Programme launch above €800m [AG-0049] | Qualified | No |
| `delay_tactics: bottleneck` / `poaching` | $1B each, with a $48.32B naked fine | Above €300m (about €0.9bn at an assumed $1.10/€, so also above €800m); "abnormal level of risk" [A-0298, A-0299]; integrity, the ECSC's field [AG-0022, AG-0053] | Read as Qualified (inference) | No |
| `ngsa: cancel` / `rea350: cancel` | write-off | Change to the major-programme plan and the Yearly Budget [A-0297]; major announcement to the capital markets [A-0299] | Simple | No (any write-off above €300m) |
| Joint Venture `commit` / `withdraw` | not on Airbus's board; per brief if one is offered | Strategic alliance [AG-0049] | Qualified | No |
| Lobbying, `other_moves` (e.g. an A220-500 study) | small or unpriced | Lobbying: none. A real A220-500 launch would be a programme above €300m | — | **Lobbying is below the threshold**: reviewed only as part of the round's package |
| `hold` / `none` | — | Not a Board item | — | — (never vetoed) |

The engine code rides with the NGSA launch. The board reviews the engine choice as part of that launch, with Antony Wood's
engine background as the lens (inference from AG-0046).

---

## 4. Culture

**Calibration (final cross-check across the five boards, 2026-10-10, with half points).** The scores are judgements from
the evidence, labelled as such, and were calibrated across the five boards so that a score means the same at each. Risk
aversion: 3 = balanced (approves debt-funded returns or large deals while programme risk is live); 4 = averse (the
rating and safety come first and proof comes before commitment, yet staged, shared or derivative programme risk is
approved and cash is returned from a sound balance sheet); 5 = a board in crisis (returns cut, capital raised, nothing
unproven funded). Time horizon: 2 = near-term (development cut first, or cash returned first while the next programme
waits); 3 = balanced (core developments protected, but most spare cash returned or used to repay debt, and pay on
one-to-four-year metrics); 4 = long-term leaning (also a multi-decade programme prepared for years and kept whole while
returns stay moderate). A half point (2.5, 3.5, 4.5) places a board between two descriptions: it shows traits of both,
and its tests sit between theirs. A higher risk aversion means a tighter downside limit, more proof on the record before
an unconditional commitment and less balance-sheet strain accepted; a longer time horizon means more near-term cost
accepted for a long-term position. This board: risk aversion **4**: net cash and an A+/A1 rating protected, an abnormal
level of risk reserved to the board and proof before commitment (also what a plain "strongly averse" 5 describes), but
staged, derivative, shared or funded programme risk goes ahead and cash is returned from a sound balance sheet
[A-0402, AG-0062, A-0299, AG-0056, AG-0070, AG-0071, AG-0059], so 4, not 5; time horizon **4**: NGSA prepared for
years and kept on its 2030 clock while returns stay within a stated budget [AG-0063, AG-0058, AG-0059]; the July 2026
buyback and one-to-four-year pay pull toward 3, not yet to 3.5, because no development has waited for returns
(placements: inference). **No score changed at this cross-check.** The downside limit per Board item at 4 is $2B in any
plausible column (it had been drafted at $1B).

### Risk aversion: **4 / 5** (averse: strict on balance-sheet and integrity risk; accepts measured programme risk)

**Rationale.**
- The stated financial risk appetite is "prudent": low leverage and hedging [AX-0022, A-0343].
- Airbus runs a net-cash balance sheet, €12.2bn at the end of 2025 [A-0402, A-0401], and holds S&P A+ and Moody's A1 ratings [AG-0062].
- "Abnormal level of risk" is itself a reserved matter, and launches above €800m need a Qualified Majority with a ten-director quorum [A-0299, AG-0049, AG-0011].
- The board's own self-evaluation asks for stronger risk oversight in decision-making [AX-0008], and its formal declaration admits that its risk systems cannot catch everything [AG-0033].
- It wants proof before commitment:
  - the NGSA is gated on technology and production-system maturity [A-0225] and on a 2030 launch [AG-0063];
  - under its oversight the hydrogen aircraft was cut and delayed once its technology lagged [AG-0065];
  - the A380 was ended once its backlog failed; a Bloomberg pre-report said the board would need to approve it formally, but no vote is on record [AG-0055, A-0143] (the board's role in both: inference).
- It frames the ramp as "disciplined and controlled" [A-0303, AX-0010].

**Against (why not 5).**
- It approved the A350F before any launch order [AG-0056].
- Airbus took over failing Spirit sites, although Spirit paid it to do so [AG-0070], and agreed a three-way space merger [AG-0071]. The sources name the company; the board's approval is inference from its reserved matters (acquisitions above €300m, strategic alliances) [A-0298, AG-0049].
- It is starting capital-return buybacks while the NGSA is ahead [AG-0059].

The board takes programme risk when that risk is staged, derivative, shared or funded. It does not take it when it threatens liquidity, the rating or integrity (inference).

**Trend.**
- Since the 2016-2020 integrity crisis [AG-0052, AG-0053] and COVID, when it withdrew the dividend and added €15bn of credit within days [AG-0054], the board has become more conservative.
- In 2025-26 it has loosened on shareholder returns [AG-0058, AG-0059], but not on programme risk.
- Read: **stable at 4**.

**How it shapes votes.**
- The board approves a launch only if the plan keeps net cash and the rating intact, puts EIS no earlier than technology-ready, and runs no second clean sheet in parallel.
- It vetoes anything carrying a large contingent penalty or an integrity exposure, and any item that loses more than $2B in a plausible Boeing column (the limit at 4; inference).

### Time horizon: **4 / 5** (long-term, with a growing pull toward near-term returns)

**Rationale.**
- The board describes its purpose as delivering "long-term value" [AG-0006]. It justifies innovation by viability "in the decades ahead" [AG-0039] and technology as the driver of long-term shareholder value [A-0408]. Its pay philosophy is aligned with long-term shareholders [AG-0028].
- The NGSA has been prepared over many years, with launch in 2030 and EIS in the second half of the 2030s [AG-0063, A-0409, A-0431]. The board ran in-depth reviews of the long-term commercial aircraft plan [A-0302].
- Continuity is built in: staggered terms with a third renewed each year [AG-0001, AG-0005], and successions announced a year or more ahead [AG-0072, AG-0048, AG-0052].
- Cash targets are set over five years [AG-0058, AG-0059], and the long-term state shareholders hold about a quarter of the shares [A-0381].

**Pulls toward the short term.**
- About half of target variable pay is the one-year STI (target 150% of salary, against an LTI capped at 150%), in which EBIT and FCF together weigh 40% (20% each) [A-0309, A-0310, A-0332]. The LTI measures only three years [AG-0030], and there is no five-year holding period [AG-0031].
- The payout ceiling was raised to 50% [AG-0058], and a first €5bn capital-return buyback was approved in July 2026 [AG-0059]. Observers warn of a Boeing-style drift (AG-0060, uncorroborated, inference only).

**Trend.** A slight drift toward near-term returns since mid-2025 (from about 4.5 to 4, inference). The NGSA plan has not been cut to pay for returns.

**How it shapes votes.**
- The board accepts near-term cost for a long-term position: it would not vote down an NGSA that is on its technology clock because of near-term EBIT.
- It does not accept a long-term bet that endangers the dividend policy or the buyback, except in a crisis, where the 2020 precedent applies [AG-0054].
- On the game's levers the horizon works through three limits: no veto of an NGSA launch on its clock for its spend or near-term earnings cost, no NGSA cancel unless continuing loses in every plausible column, and no veto of a later launch for lateness alone. It gives no allowance on peak cash: risk aversion decides that conflict (inference).

### Capital allocation

The order of priority (inference from the record):
1. **Liquidity, net cash and the rating** [AX-0022, A-0402, AG-0062]. In a shock, the dividend goes first [AG-0054].
2. **Disciplined investment in the future portfolio, alongside shareholder returns** [A-0194, AX-0012]. Capital stays inside aerospace and defence [AX-0003].
3. **The dividend**: a payout of 30-50% [AG-0058]. €3.20 for FY2025 (48%) was approved in April 2026 [A-0386, AG-0041].
4. **Buybacks**: buybacks to cover share plans continue [A-0399] (a further limited programme from September 2026: AG-0061, uncorroborated). The first capital-return programme, €5bn over three years, is executed by management within board terms [AG-0059].
5. **M&A to de-risk supply** (the Spirit sites, with Spirit paying Airbus) and **European consolidation with shared risk** (space) [AG-0070, AG-0071].
6. **Development funding**: development is financed from cash, customer advances, government refundable advances and supplier risk-sharing [A-0348, A-0368]. In 2023 the CEO floated state support for the A320 successor [AG-0066].

**Latest position (H1 2026).** Gross cash was €23.4bn. H1 free cash flow was -€1.17bn on the ramp inventory build-up. 2026 guidance is unchanged: about 870 deliveries, EBIT Adjusted of about €7.5bn and FCF of about €4.5bn [AG-0074].

### Safety oversight

- The full board reviews product safety in depth twice a year [AX-0015]. Aviation safety and security are "the highest priority" [AG-0038], and safety heads the CEO's 2026 objectives [A-0331, AX-0073].
- There is no board safety committee [AG-0022, inference]. Each division has a Chief Product Safety Officer as an independent voice (AG-0069, uncorroborated).
- Recent company practice puts safety ahead of output (company actions; the board's role is inference):
  - a fleet-wide precautionary software action on about 6,000 A320s in November 2025 [AG-0067];
  - a delivery-guidance cut rather than shipping aircraft with suspect panels in December 2025 [AG-0068, A-0185].
- How it votes: a plan that the operating head flags as a safety or quality risk to the ramp is vetoed (inference from AX-0015, A-0331).

### Stakeholder and state influence

- Directors owe their duty to the company and its stakeholders [AG-0012]. National balance shapes the board and the ExCo [AX-0028, AG-0004].
- The states are minority holders without a veto [AG-0050, AG-0003, AG-0036]. Their leverage runs through the AGM (Articles, equity) [AG-0037, AG-0034] and through refundable advances [A-0348].
- An NGSA launch that relies on state co-funding [AG-0066] ties the board's timing to government budgets (inference).
- Boeing has long framed Airbus as launch-aid backed [A-0155]. That is a rival's view, not board evidence.

### Pay horizon (the incentives the board sets)

- **STI** (one year): target 150% of salary, capped at 200% of target [A-0309]. The company half is 80% financial, EBIT and FCF equally [A-0310]. The other half is the CEO's objectives [AX-0070], with more weight on priorities such as safety and the ramp in 2026 [AX-0073]. 2025 achievement was 123% for the company half, with FCF at 157% [A-0311].
- **LTI** (performance shares): capped at 150% of salary [A-0332]. It measures three financial years, 2026-2028 for the 2025 grant, and vests in May 2029 [AG-0030]. The 2022 plan was 75% average EPS and 25% cumulative FCF [A-0334]. Half vests on any positive cumulative EBIT [AX-0086]. A sustainability KPI was added in 2025 [A-0308].
- **Alignment**:
  - the CEO holds more than 200% of salary in shares [AX-0087], but there is no five-year holding period [AG-0031];
  - the pay mix is 28% fixed and 72% variable [A-0342];
  - no clawback was applied in 2025 [AX-0035];
  - the policy passed with 96% [AG-0027].
- **Read**: nothing in pay rewards outcomes beyond about four years. The board's long horizon comes from its culture, its ownership and its programme rules, not from pay (inference). In the game, the executives are paid on EBIT, FCF and EPS within roughly a 1-4 year window, so the board must supply the long view.

---

## 5. Decision record

Rows marked (Company action) are decisions the sources attribute to the company; the board's role in them is inference.

| Date | Decision | Ids |
|---|---|---|
| Dec 2012 / 2013 | Governance reform: state stakes capped (12/12/4%), no veto rights, framed as emancipation from political influence | AG-0050 |
| 15 Dec 2017 | Succession plan: Enders not to seek a new term; Bregier to leave; Faury to Commercial Aircraft (during the bribery probes) | AG-0052 |
| 8 Oct 2018 | Faury selected as CEO, unanimously, after reviewing internal and external candidates | AG-0051 |
| 14 Feb 2019 | (Company action) A380 production ended, after Emirates cut its order; a Bloomberg pre-report said the board would need to approve it formally; no vote on record | AG-0055, A-0143 |
| Apr 2019 / Apr 2020 | Obermann selected, then chair, succeeding Ranque | AG-0045 |
| 31 Jan 2020 | (Company action) €3.6bn settlement with the PNF, SFO and DOJ; AFA monitoring; the original statement credited the board and its ethics committee (not reconfirmed on re-check) | AG-0053, A-0474 |
| 23 Mar 2020 | COVID: 2019 dividend (€1.4bn) withdrawn; new €15bn credit facility; pension top-up suspended; guidance withdrawn | AG-0054 |
| 29 Jul 2021 | A350F development approved with no launch customer; EIS later slipped to H2 2027 | AG-0056, AG-0057 |
| 30 Oct 2024 | Faury renewal proposed (approved at the April 2025 AGM); Wagner named to succeed Scherer from 1 Jan 2026 | AG-0072, AX-0108 |
| Dec 2024 | (Company action) Defence and Space: 2,043 job cuts after about €1.5bn of space write-downs | AG-0073, A-0281 |
| Feb 2025 | (Company action) Hydrogen aircraft delayed beyond 2035; budget cut | AG-0065 |
| Apr-Dec 2025 | (Company action) Spirit AeroSystems sites taken over (agreement 27 Apr 2025); Airbus received $439m; closed 8 Dec 2025 | AG-0070 |
| 18 Jun 2025 | Dividend payout range raised to 30-50% (shareholder policy is a reserved matter) | AG-0058, A-0299 |
| 23 Oct 2025 | (Company action) Space merger MoU with Leonardo and Thales (35/32.5/32.5) | AG-0071, A-0304 |
| Nov-Dec 2025 | (Company action) Precautionary A320 fleet action; 2025 delivery guidance cut to about 790 | AG-0067, AG-0068, A-0185 |
| Feb-Apr 2026 | FY2025 dividend of €3.20 (48% payout); 2022 LTI vested above target; AGM approves all resolutions and new directors | A-0386, A-0336, AG-0041 |
| 21 Jul 2026 | €5bn share buyback over three years approved; 2029 EBIT target of €12-13bn | AG-0059 |
| 1 Oct 2026 | Obermann leaves; Moraleda chair; Fouquet co-opted; Dunkerley lead independent director | AG-0042, AG-0043 |
| 2027 (expected) | Decision on Faury's renewal or a handover (Wagner widely seen as heir) | AG-0048 |

---

## 6. Relationship with management

- **Separate chair and CEO.** The CEO is the only executive on a board of eleven independent non-executives [AG-0002, AG-0026].
- **Cooperative and deferential on execution, firm on governance.**
  - The board grades itself on oversight of strategy, risk, capital allocation and culture [AG-0019]. It has an external evaluation every three years [AG-0017], and the 2025 evaluation reports open debate under a committed chair [AG-0018].
  - The 2025 evaluation describes the CEO as nurturing a positive relationship with the board [AX-0059], and the board consults him on his own pay [AX-0091].
  - The chair and the lead independent director handle the investor dialogue on pay and board composition themselves [AG-0013]. The board plans its own handovers early, as it does for executives [AG-0025].
  - No clawback was applied for the 2025 delivery miss [AX-0035, AX-0052].
  - The board nonetheless controls disclosures [AX-0004] and ExCo appointments [AX-0028], and it sets the CEO's objectives and scores them [AX-0070].
- **Tensions.**
  - The December 2017 succession plan, with the COO leaving, came amid what the press described as a power struggle during the bribery probes (AG-0052, press characterisation).
  - The 2027 CEO decision is open [AG-0048].
  - The new chair and lead independent director (October 2026) may test management harder; that is inference, with no evidence yet.

**The three agents.**
- **Faury (CEO, `airbus-faury`).** A trusted, agile CEO in his third term [AX-0059, AG-0072], judged on EBIT, FCF and his priorities [A-0310, AX-0073]. His renewal is the board's 2027 call [AG-0048]. The board defers to his case unless a test fails (inference).
- **Toepfer (CFO, `airbus-toepfer`).** The management interface to the Audit Committee [AX-0107] and owner of internal control [AX-0106]. The board reads his memo as the liquidity and rating test [AX-0022, A-0402].
- **Wagner (CEO Commercial Aircraft, `airbus-wagner`).** In post since 1 January 2026 after a planned handover [AX-0108, AX-0100], and widely seen as heir apparent [AG-0048]. The board reads his memo as the ramp, safety and quality test [A-0303, A-0331]. His track record is thin (Very low confidence in the executive file).

---

## 7. How the board reads rivals (evidence only)

- **The duopoly is over, but COMAC's rise will be measured** [AX-0024]. New entrants and rival product launches are a named risk even with a record backlog [AG-0040].
- **Against Boeing, the anchor is about 60% of the single-aisle backlog** [AX-0025]. In 2025 the board ran a detailed review of widebody market dynamics [A-0302, AX-0019].
- **US tariffs** were treated as a significant financial risk to US deliveries [A-0301].
- There is no board-level evidence on how it reads Boeing's fps timing. The CEO's 2030 NGSA plan is presented as Airbus's own clock [AG-0063]. A reaction to Boeing would be inference.

---

## 8. Confidence and gaps

| Area | Level | Why |
|---|---|---|
| Composition (Oct 2026) | High | Airbus releases from April and October 2026, corroborated |
| Reserved matters and votes | High | Board Report and governance page; €800m Qualified Majority from the web page (corroborated) |
| Pay horizon | High | Board Report remuneration section |
| Risk aversion | Medium | Inferred from decisions and policy; no board speech |
| Time horizon | Medium | Clear framing, but the 2025-26 shift to buybacks is recent |
| Safety oversight | Medium | Twice-yearly review and recent actions; no committee and no external assessment |
| Individual directors' views | Low | No minutes or statements; backgrounds only |
| Rivals | Low | Risk factors only |

**Gaps.**
- No Airbus transcripts in the repo, so no chair remarks in the board's own spoken words.
- No current (post-October 2026) committee lists; the ECSC chair is not confirmed.
- No formal record of the A380 board vote.
- Backgrounds of Hopke, Rummelhoff and Guillouard not confirmed.
- No external safety-culture assessment.
- The 2026 LTI weights are not disclosed.
- NGSA launch timing is contested: 2030 [AG-0063] against 2031 or later (AG-0064, an analysts' projection corroborated by Leeham News: inference only).

**Fallback.**
- Where the record is thin, apply the company profile's hard rules and the decision record above.
- Defer to the CEO's case unless a test below fails.
- Never invent a board view.

---

## Appendix: tests and veto grounds the agent plays from

Thresholds that are game parameters or my derivation are marked (inference); each still rests on cited evidence.

| Test | Threshold or rule | Evidence |
|---|---|---|
| Liquidity and rating | Development spend of all programmes in any year (loaded bills ÷ development years) no more than about one year's FCF, about $5.2B at an assumed $1.10/€ (inference). No plan that needs an equity raise or a dividend cut outside a crisis | A-0402, AX-0104, AG-0062, AG-0034, AG-0054, AX-0022 |
| One clean sheet at a time | At most one new launch per round. NGSA / A350 Re-engine development overlap of 2 years or less, unless the grid shows at least $1B more | Company rule 6; A-0343, A-0401, AG-0049 |
| Technology readiness | NGSA EIS never before the technology-ready year (2035); launch window 2028-2030 | A-0225, A-0409, AG-0063, AG-0065 |
| Business case | The launch beats Do Nothing on the grid in the scenario the CEO expects, and the CEO states the worst plausible Boeing response | A-0364, AX-0007, AG-0029 |
| Downside | Each Board item gains in the CEO's expected scenario and loses no more than $2B against its default in any plausible Boeing column, the limit at 4 (inference) | AX-0007, AG-0029, AG-0033, A-0364 |
| Integrity and abnormal risk | Delay Tactics only after Boeing has launched fps, at most once, never naked (no $48.32B fine exposure), with the CEO's recorded adaptation. Supply-chain bottleneck: veto (inference: conflicts with the integrity pillar and with supply-security policy) | A-0299, A-0331, AG-0053, A-0474, AG-0070 |
| Ramp and safety | No plan that the operating head flags as a threat to safety, quality, the rate-75 ramp or supply (a supply crunch); no override of these flags is accepted (inference) | AX-0015, A-0331, A-0303, AX-0023 |
| Reaction discipline | No NGSA cancellation in reaction to Boeing; cancel only a failed business case | Company rule 7; A-0364, AG-0055 |
| Shareholder returns | The plan keeps the 30-50% payout and the €5bn buyback fundable, or the CEO explains why not | AG-0058, AG-0059 |
| Board package integrity | No unresolved ExCo veto or red-line flag on an item that needs a Qualified Majority | AX-0027, AG-0049 (inference) |

**Veto grounds.**
- **Balance sheet**: liquidity or rating at risk [AX-0022, AG-0062].
- **Technology**: not ready [A-0225].
- **Two-front**: concurrent clean sheets [A-0343].
- **Integrity**: abnormal risk or integrity exposure [A-0299, AG-0053].
- **Safety**: the ramp at risk [AX-0015].
- **Reactive cancellation** [A-0364].

**Limits of the veto.**
- The veto binds, and the board may name acceptable alternatives: a later year, a single programme, the default.
- The board never originates an order and never vetoes a `hold` or `none`.

**Recommendation style** (inference from AG-0014, AX-0007, AG-0016).
- Scenario-based and staged: "show the downside case", "keep net cash", "one programme at a time", "keep the 2030 technology clock".
- Delivered through the chair and the lead independent director.
