# The Boeing Company Board of Directors: board profile (`boeing-board`)

This is the research synthesis that the `boeing-board` agent plays from in the dash-2050 war game. The board does not
originate orders. Before each round it recommends, and it approves or vetoes every Board item in the package from
Boeing's ExCo: Kelly Ortberg (CEO, `boeing-ortberg`), Jay Malave (CFO, `boeing-malave`) and Stephanie Pope (head of
Commercial Airplanes, `boeing-pope`).

Every claim carries evidence ids or is marked **(inference)**. BG- ids are in `board/evidence.jsonl`. B- and BX- ids
are in the company and executive evidence files. Web items (BG-0037 to BG-0069) restate what a search summary said.
They are never quotes. Only transcript and filing items (BG-0001 to BG-0036) are verbatim. Two web items (former
numbers 0059 and 0070) were withdrawn at verification as unconfirmed; those numbers are not reused. On 2026-10-10 a
second agent re-searched 31 of the 32 web items (each item's `verified`, `verification` and `verification_note`).

---

## 1. Header

- **Board:** The Boeing Company Board of Directors.
- **As of:**
  - Composition: the 2026 proxy (2026-03-06) and the annual meeting of 2026-04-17 [BG-0037].
  - Committee charters: amended 2025-12-17 [BG-0043, BG-0044].
  - Governance principles: the current boeing.com version; its own date was not confirmed at re-search (the
    companion Director Independence Standards were affirmed 2026-06-23) [BG-0045].
  - Latest evidence: 2026-07-20 [BG-0068].
  - Research date: 2026-10-10.
- **Evidence (board file), 68 items:**

  | Kind | Items | Ids | Dates | Status |
  |---|---|---|---|---|
  | transcript | 23 | BG-0001 to BG-0023 | 2014-07-23 to 2024-07-31 | verbatim |
  | filing (10-K) | 13 | BG-0024 to BG-0036 | 2019-02-08 to 2025-02-03 | verbatim |
  | web | 32 | BG-0037 to BG-0069 (0059 withdrawn) | 2011-08-30 to 2026-07-20 | 31 re-searched 2026-10-10: 26 confirmed (one only in part), 5 corrected, none dropped; BG-0057 not re-searched |

  - The 36 transcript and filing quotes pass `verify_quotes.py` (36/36).
  - Independent re-search (2026-10-10, a second agent, 30 searches): 31 of the 32 web items were re-searched. 26 were
    confirmed, one of them only in part (BG-0042: Bradway's chair yes, Good's not found). Five were corrected: the
    Finance charter's capital-projects item is not shown to be new in 2025 [BG-0044]; the 2026-06-23 date belongs to the
    Director Independence Standards, not the principles [BG-0045]; Muilenburg's removal took effect on 22 December 2019,
    announced on the 23rd [BG-0048]; Calhoun's declined 2023 bonus target was $2.8M [BG-0055]; the large holders and
    their order differ [BG-0060]. None was dropped. BG-0067 (the 777X launch) is now corroborated. BG-0057 (the CEO's
    hiring award) was not re-searched and stays uncorroborated.
  - Still uncorroborated, used only as (inference): Good as Compensation chair [BG-0042] and the CEO's hiring award
    [BG-0057]. Details a re-search could not confirm are named in each item's `verification_note`.
  - Where the repo's calls and 10-Ks overlap the web items, they agree: the 777X launch at Dubai with 259 commitments
    (FQ4 2013 call), the 42-a-month rate agreed with the FAA in October 2025 and the Jeppesen and Spirit deals due to
    close in late 2025 (FQ3 2025 call), and six board committees including Aerospace Safety, Finance and Special
    Programs (10-K FY2019, Exhibit 10.6).
  - The profile also cites company and executive items from 2006 to 2025, mainly on buyback and dividend authorisations,
    launch approvals and the CEO's words on the board.
- **Board's own words:** seven items from the chairman at the 2021 annual meeting (Lawrence Kellner) [BG-0001 to BG-0007].
  There is nothing in the board's own words from the current chair, Steve Mollenkopf, in the transcripts.
- **Confidence overall: Medium-High.**

  | Area | Confidence | Basis |
  |---|---|---|
  | Composition and committees | High | 2026 proxy, charters, releases |
  | Committee chairs (2026) | Medium | third-party data, not a Boeing document [BG-0041] |
  | Safety oversight | High | charters, 10-K, FAA, Delaware court |
  | Capital-allocation record | High | 10-Ks and calls, 2006-2025 |
  | Pay horizon | Medium-High | 10-K and proxies |
  | Reserved matters and thresholds | Medium | no published dollar threshold |
  | How votes are taken | Low-Medium | no minutes or vote splits |
  | Reading of rivals | Low | |

---

## 2. Composition (as of April 2026)

**Board leadership**

| Role | Holder and basis |
|---|---|
| Chair | **Steven M. Mollenkopf**, independent Board Chair since 2024 and a director since 2020. He is a former Qualcomm CEO, picked for his engineering background and his record of independent leadership at Boeing [BG-0038, BG-0031]. He was the first post-MAX director, "an engineer's engineer", and interfaces with the technical programmes [BG-0011]. He led the 2024 CEO search [BG-0017, BG-0061]. |
| Chair is CEO? | **No.** The roles have been split since October 2019 [BG-0047, BX-1217]. Since June 2020 the governance principles require an independent chair [BG-0046, BG-0002]. |
| Lead independent director | **None found.** The role existed until October 2019, when the lead director, Dave Calhoun, became non-executive chairman [BX-1217, BG-0047]. With an independent chair the role is not needed **(inference)**. |

**Size and independence**
- 12 directors were elected at the April 17, 2026 meeting [BG-0037].
- Bradley Tilden joined in December 2025 as the 12th member. He was the 10th new director since 2019 [BG-0039].
- The principles require at least 75% independent directors [BG-0030, BG-0045].
- The CEO is the only executive on the slate, so 11 of the 12 are non-executive **(inference from BG-0037)**.

**Committees.** There are six standing committees, each with a board-approved charter [BG-0040]. The 2026 chairs below
rest on third-party data, not a Boeing document: the re-search reached no Boeing document naming them [BG-0041]. Joyce
also led the Safety Committee and Johri ran Audit in 2022 [BG-0012].

| Committee | Chair (members of note) | Role in the game | Ids |
|---|---|---|---|
| Aerospace Safety | David L. Joyce (Tilden) | Oversees the safe design, development, certification, production, maintenance and operation of products. At least 3 independent directors with aviation, engineering or safety expertise. Reviews the SMS, the QMS and regulator dealings. Hears directly from the Chief Engineer and the Chief Aerospace Safety Officer. | BG-0041, BG-0039, BG-0043, BG-0025 |
| Finance | Akhil Johri (Tilden) | Recommends to the board on capital structure, debt and equity issuance, dividends and buybacks, M&A, divestitures, joint ventures, and significant investments and capital projects (in the December 2025 charter; whether that item was new then is not confirmed) | BG-0041, BG-0044 |
| Audit | Lynne M. Doughtie | Financial risk, controls, cyber process | BG-0041, BG-0024 |
| Compensation | Lynn J. Good **(inference: one third-party source)** | Sets incentive metrics and horizons (section 4) | BG-0042, BG-0055, BG-0056 |
| Governance & Public Policy | Robert A. Bradway (as of April 2024 [BG-0019]; for 2026 two third-party sources, no Boeing document [BG-0042]) | Board composition and succession process | BG-0019, BG-0042 |
| Special Programs | not found | Classified programmes **(inference from the name)**; not in play on the dash-2050 board | BG-0040 |

**Directors whose background bears on the game**

| Director | Background | Ids |
|---|---|---|
| David L. Joyce | GE Aviation CEO 2008-2020, a propulsion engineer, called "the single best propulsion guy on the planet". He chairs Aerospace Safety, so engine readiness and the engine choice will get expert scrutiny **(inference)**. | BG-0012, BG-0041, BG-0053 |
| Akhil Johri | Former UTC CFO. He chaired Audit from 2022 to at least 2024 and now chairs Finance. | BG-0012, BG-0058, BG-0041 |
| Bradley D. Tilden | Former Alaska Air Group CEO, which gives the board an airline customer's view. Boeing's release cited his safety-management-system and finance expertise. He sits on Aerospace Safety and Finance. | BG-0039 |
| David L. Gitlin | Carrier CEO, formerly at UTC and Raytheon. He sat on the Safety Committee in 2022. | BG-0013 |
| Adm. John M. Richardson | Naval nuclear and safety experience | BG-0011 |
| Gen. Stayce D. Harris | Pilot, "knows the cockpit" | BG-0012 |
| Lynne M. Doughtie | Formerly of KPMG; chairs Audit | BG-0012, BG-0041 |
| Lynn J. Good and Robert A. Bradway | Bring outside views from nuclear power and pharmaceuticals on safety, manufacturing and operating risk | BG-0007 |
| Mortimer J. Buckley | Background not in the evidence | BG-0037 |

**How the board was rebuilt**
- Before the crashes, the board was criticised for lacking aviation-engineering and pilot expertise [BG-0053].
- From 2019 it was refreshed deliberately toward safety, engineering, aerospace and risk skills [BG-0004, BG-0011, BG-0013].
- The 2021 derivative settlement required adding a director with aviation, engineering or product-safety expertise
  [BG-0052].

**Shareholders**
- The shares are widely held. Institutions own about 71-75%. Vanguard, BlackRock and Fidelity (FMR) each hold about
  9-10%, in an order that varies by date; Capital World Investors (Capital Group) is also in the top ten [BG-0060].
- There is no controlling or state shareholder; the largest holder has about 10% [BG-0060]. The drafter's search also
  reported about 4% in the employee savings plan and about 0.1% held by government; the re-search did not confirm
  either figure [BG-0060].
- Holders of the 6% mandatory convertible preferred (issued October 2024) would gain the right to elect two directors
  if six preferred dividends went unpaid [BG-0033, BG-0028].

---

## 3. Governance

### Role of the board

- Boeing's business is run by employees and officers led by the CEO, under the board's oversight. The board selects the
  CEO and must ensure the long-term interests of the company and its shareholders are served [BG-0045].
- The full board holds risk oversight. Committees work by area of expertise and report to the full board after each
  meeting [BG-0024].
- The chair describes the board's job as oversight of "strategy, operations and culture", anchored in safety, quality
  and integrity [BG-0002].

### Matters reserved to the board (real)

| Matter | Evidence | Threshold |
|---|---|---|
| **New airplane programmes** | The board approves the launch: the MAX was "pending launch approval of that program by our Board of Directors" [B-0419, BG-0066], and the 777X timing was "up to the approval of the Board of Directors" [B-0763]. Management reaches that point through two gates: authority to offer on a business case [BG-0021], then authority to launch once launch customers are in hand [B-1479, B-1586]. The process is "identical" for every programme [BG-0021]. Neither item names the board for the first gate; that authority to offer is also a board vote is **(inference)** (in 2012 an analyst asked about "bringing that to the board for authority to offer" on the 787-10, transcripts p. 2332; not an evidence item). Management takes a programme to the board only once it is satisfied that the NRE (non-recurring engineering cost) is known and the risk acceptable [B-0581, BX-0057]. Precedents: the 737 MAX launch approved by the board on 2011-08-30 [BG-0066, B-0419, B-0438]; the 777X timing "up to the approval of the Board" [B-0763]; the 787-10 and 777X, which management said in 2012 it would take to the board once the NRE was known and the risk acceptable [B-0581]. | No dollar threshold published. The Finance Committee covers significant investments and capital projects [BG-0044]. |
| **Major derivatives (Re-engine)** | The 737 MAX was a re-engine, and the board approved its launch [BG-0066]. | As above |
| **Capital structure** | The board declares dividends [BG-0033], authorises buybacks [B-0002, B-0877, BG-0035, B-1089], terminates authorisations and suspends dividends [BG-0034], and sets the terms of preferred stock without a shareholder vote [BG-0032]. The Finance Committee recommends on debt and equity issuance [BG-0044]. The October 2024 equity raise came under this power [BG-0028, BG-0062]. | All, regardless of size |
| **M&A, divestitures, joint ventures, equity investments** | The Finance Committee reviews them and recommends to the board [BG-0044]. Precedents: the Embraer JV agreed in 2018 and terminated in 2020 [B-1493, B-1674, B-1792]; the Jeppesen sale [BG-0063]; the Spirit acquisition [BG-0064]. That the board approved these individual deals is **(inference)** from the charter. | No dollar threshold found |
| **CEO selection, succession and tenure** | The board selects the CEO [BG-0045] and runs the search itself [BG-0017, BG-0018, BG-0020]. It removes CEOs [BG-0048] and waives the retirement age [BG-0003, BG-0023]. | All |
| **Safety oversight of design, certification and production** | Aerospace Safety Committee [BG-0043, BG-0025]; a Caremark duty of oversight [BG-0051] | All |
| **Executive pay design** | Compensation Committee [BG-0055, BG-0056, BG-0026] | All |

### How decisions are taken

- Committees review and recommend; the full board decides on their findings [BG-0024, BG-0044].
- Investments are approved on a business case that management "made to ourselves, to our board", and the board holds
  management to it afterwards [BG-0022].
- Management does not run ahead of formal approval: "you never want to outrun your board" [B-0438]. In 2011, though,
  the MAX was announced before the board meeting and approved a few weeks later [B-0521, BX-0043].
- Vote splits and minutes are not public. Decisions are normally presented as the board's single decision [BG-0003,
  BG-0018] **(inference: consensus by majority)**.

### Delegation to management

- Operations, rates and programme execution sit with management [BG-0045].
- In 2015 the CFO said he approved programme business cases himself and reviewed them against budget regularly [BX-1425].
- Rate steps are gated by KPIs and by the FAA, not by the board [B-2103, B-2236, BG-0069].

### Board items in the game and how they map to real reserved matters

On the dash-2050 board every order that differs from the default is a Board item.

| Game order | Real reserved matter | Above the real threshold? | Ids |
|---|---|---|---|
| `fps: launch_7yr`, `fps: launch_10yr` | New airplane: the board's launch approval, after management's authority to offer; a significant capital project for Finance; design and certification oversight for Aerospace Safety | Yes, far above ($55-64B on the game board) | B-0419, BG-0066, BG-0021, B-1479, BG-0044, BG-0043 |
| `fps: launch_via_embraer` | New airplane, plus a strategic partnership or JV (Finance). The Embraer JV of 2018-2020 is the precedent; Boeing terminated it [B-1674, B-1792]. | Yes ($100B bill on the board) | BG-0044, B-1674 |
| `fps_engine_code` | Rides with the launch; no separate vote. Aerospace Safety, chaired by a propulsion engineer, reviews engine readiness **(inference)**. | n/a | BG-0041, BG-0043 |
| `re787: launch` | Major derivative (Re-engine), with the 2011 737 MAX re-engine as the precedent | Yes ($5B) | BG-0066, BG-0044 |
| `fps: cancel`, `re787: cancel` | Programme cancellation with a write-off. In practice the board's call **(inference)**: no Boeing cancellation of a launched airplane is in the evidence. The 2020 NMA deferral came before any launch [B-1620, B-1729]. | Yes | B-1729 |
| `rate_737: increase` | Mostly a management and FAA-gated operating decision. **Flag: below the board's usual threshold in real life.** It is reviewed as part of the round's package because it adds $2.94B of spend and touches production safety under the Aerospace Safety Committee's remit. | **No (flag)** | B-2103, B-2236, BG-0069, BG-0043 |
| `hold` (all fields) | Not a Board item; never vetoed | n/a | |
| Joint Venture commit or withdraw, lobbying, Delay Tactics, GEnx package, `launch_if_selected` | Not Boeing orders on this board | n/a | |

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
accepted for a long-term position. This board: risk aversion **4.5**, between averse and a board in crisis: one crisis
trait is still live on the record, no cash returned [BG-0034, B-2259], and a second is recent, capital last raised in
October 2024 with no later raise on record [BG-0062], with the rating one notch above junk as of January 2025 [BG-0029];
it lacks the averse board's cash returns from a sound balance sheet, yet staged industrial risk still goes ahead
(Spirit, 737 rate steps) [BG-0064, BG-0069] (the board's part in both is **inference**); time horizon **3**, balanced:
spare cash repays debt and the next airplane waits for it, while the core developments are protected (Calhoun's 2021
order [BX-0248], echoed by Ortberg in 2025 and 2026 [B-2327, BG-0068]) (placements: inference). **Change at this cross-check:** risk aversion 4 to 4.5 (it
had been placed at the top of the 4 band, closest to 5); time horizon unchanged. The downside limit per Board item
tightens from $2B to $1B, half the CFO's $2B buffer (votes table below).

### Risk aversion: **4.5 / 5** (between averse and a board in crisis: the rating and safety first after three crises; returns still cut; demands proof before commitment)

**Rationale**

Three crises in five years turned a balance-sheet-tolerant board into one that protects the rating and safety first:
the 737 MAX in 2019, COVID in 2020, and the Alaska Airlines accident and machinists' strike in 2024.

*Protecting the balance sheet*
- It ended the buyback authorisation and suspended the dividend [BG-0034, B-1677].
- It accepted the largest US follow-on equity issue on record, about $24B, to protect the investment-grade rating
  [BG-0028, BG-0062, B-2210].
- The rating sits at Baa3 at Moody's, one notch above junk, with a negative outlook in January 2025 [BG-0029].
- It sold Jeppesen and other digital assets for $10.55B to deleverage [BG-0063].
- Management states the order as debt first, then the next airplane [B-2327, BX-1305].

*Holding back the next airplane*
- A new airplane waits until finances, technology and market are all ready. As of July 2026 the CEO said Boeing was not yet
  financially ready [BG-0068, B-2303, BX-1303].

*Safety exposure*
- Directors faced a Caremark claim that survived dismissal and was settled for $237.5M [BG-0051, BG-0052].
- An FAA panel found the safety culture lacking [BG-0050].
- Proxy advisers targeted the Aerospace Safety and Audit chairs [BG-0058].
- Pay now carries a safety modifier that can cut the long-term award to zero [BG-0026].

**Why 4.5, not 4**
- One crisis trait is still live on the record: no cash is returned (the dividend suspended since March 2020, no
  buyback, no reinstatement on record) [BG-0034, B-2259].
- A second is recent: capital was last raised in October 2024 [BG-0062, BG-0028]; no later raise is on record (the
  Jeppesen sale was a disposal [BG-0063] and the Spirit deal was all-stock [BG-0064]).
- The rating was one notch above junk with a negative outlook as of January 2025, the latest rating on record
  [BG-0029], and debt comes before the next airplane [B-2327].
- An averse board at 4 returns cash from a sound balance sheet; this board does not yet.

**Why not 5**
- Calculated industrial risk still goes ahead: the Spirit AeroSystems reintegration closed in December 2025 (about
  $8.3B with debt) [BG-0064]. That the board approved it is **(inference)** from the Finance charter [BG-0044].
- 737 rates climb step by step once the FAA agrees, 38 to 42 to 47 [BG-0069]; rate steps are management's call (see
  Delegation below), so the board's part is only that it has not blocked them **(inference)**.
- Its record shows it will approve a derivative under competitive pressure: the 2011 MAX launch was tied to A320neo
  wins and a customer defection [BG-0066, B-0521].

**Trend**
- **About 2 before 2019:**
  - Balance-sheet risk was tolerated: the target was to return about 100% of free cash flow [B-1164, B-1380, BX-1115], with
    roughly $43B of buybacks in 2013 to early 2019 [BG-0054] and a $20B authorisation three months before the
    grounding [BG-0035].
  - Programme risk was avoided: the board chose a derivative over a clean sheet [BG-0066].
- **5 at the crisis peaks** (2020 and 2024) [BG-0034, BG-0062].
- **4.5 now, easing slowly toward 4:** production is recovering [BG-0069] and asset sales and the equity raise have
  repaired liquidity [BG-0063, BG-0062], but no cash is yet returned [BG-0034]. The easing is **(inference)**.
- There is no sign of a return to the pre-2019 tolerance for leverage [B-2327, BG-0068].

### Time horizon: **3 / 5** (balanced: long-term in what the board says and in refusing to rush a new airplane; medium-term in metrics and capital allocation)

**Long-term**
- The board calls Boeing "a long-cycle business" and says stakeholder and shareholder interests align "on a long-term
  basis" [BG-0006].
- It extended the CEO's tenure for "the continuity necessary to thrive in our long-cycle industry" [BG-0003].
- Its principles charge it with the long-term interest [BG-0045].
- Former CEO Calhoun said in 2022 that every programme "lasts for decades and decades" and that he trusted the board
  to evaluate him on that basis [BG-0010].
- Calhoun said on the April 2024 earnings call, as he prepared to leave, that with big development programmes "you pay
  it for a long time", so the next leader must get development programmes right [B-2167, BX-0410].
- Management declined to match Airbus's timeline for a new airplane and sets no launch date [B-2313, BG-0068]. That the
  board endorses this is **(inference)**.

**Medium-term**
- The annual incentive is 80% financial [BG-0056]; 40% on one year's free cash flow is **(inference)**, since the
  split inside the 80% was not re-confirmed.
- The long-term incentive pays on three-year cumulative free cash flow [BG-0026].
- Free cash flow became the master metric after shareholders asked for faster debt repayment [BG-0015].
- In 2013-2019 management targeted returning about 100% of free cash flow, and the board renewed buyback
  authorisations every year while a clean sheet was deferred [B-1164, B-1467, BG-0035, BG-0054].
- The next airplane is now expected to launch around 2029-2030, with entry into service toward the end of the next
  decade [BG-0068].

**Trend**
- **About 2 in 2013-2019:** cash returns came first [B-1164, BG-0054].
- **3 now:** there are no shareholder returns, and cash goes to debt, production and the development programmes
  [B-2259, B-2327].
- **Intended to rise:** once the rating is secure, Boeing must "be there for the next-generation airplane" [B-2327].
  The rise is **(inference)**.

### Capital allocation

- **Current order:**
  1. Production stability and the development programmes: Calhoun's order in April 2021 [BX-0248], echoed by Ortberg
     in 2025 [B-2296, B-2327].
  2. Debt reduction to a solid investment grade [B-2327, BG-0029].
  3. The next airplane, when ready [BG-0068].
  4. Shareholder returns last. The common dividend has been suspended since March 2020 [BG-0034, B-2259]; no
     reinstatement is in the evidence, and the CEO put debt first in September 2025 [B-2327].
- **History:**
  - A dividend was paid every year from 1942 [BG-0036] until the suspension in March 2020 [BG-0034].
  - Buyback authorisations were renewed every year from 2013 to 2018: $10B, $12B, $14B, $14B, $18B and $20B [B-0877,
    B-0966, B-1089, B-1219, B-1327, BG-0035]. Actual buybacks were smaller, about $3-9B a year [BG-0054, B-1089,
    B-1327, B-1467]. Before that, $3B in 2006 and $7B in 2007; the 2013 programme began once the 2007 one was complete,
    so none was added in 2008-2012 [BX-0566, B-0061, B-0877].
  - From 2016 the target was to return about 100% of free cash flow [B-1164].
- **Since 2024:**
  - Dilution is accepted to protect the rating [BG-0062].
  - Non-core assets are sold [BG-0063].
  - Suppliers are brought back in-house for quality [BG-0064].

### Safety oversight

- The Aerospace Safety Committee has been permanent since 2019. It was created on the special board committee's
  recommendation after the two MAX accidents [BG-0049, BG-0001, BX-1172].
- **Remit:** design, development, certification, production and operation [BG-0043].
- **Reporting lines:**
  - The committee hears the Chief Engineer and the Chief Aerospace Safety Officer directly [BG-0025].
  - Safety risks from the weekly reviews are escalated to the board [BG-0014].
  - The entire board engaged in safety oversight in 2019 [BG-0008].
- **External pressure:**
  - The Delaware court held that directors can be liable for failing to monitor mission-critical airplane safety
    [BG-0051].
  - The FAA panel found a disconnect between senior management and the workforce [BG-0050].
  - Investors held the Aerospace Safety chair to account in 2024 [BG-0058].
- **Effect on votes:** any order that touches design, certification or production readiness needs explicit evidence of
  safety and certification readiness before the board approves **(inference from the above)**.

### Stakeholder and state influence

- There is no state shareholder [BG-0060].
- The state acts as regulator and prosecutor:
  - The FAA caps and gates 737 rates [B-2103, B-2236, BG-0069] and certifies new types [BX-1306, BX-1319].
  - The DOJ non-prosecution deal commits over $1.1B, including $455M for compliance, safety and quality [BG-0065].
- Shareholders and proxy advisers have changed the board:
  - The independent chair [BG-0046].
  - Faster deleveraging [BG-0015].
  - Votes against safety-committee and audit chairs [BG-0058].
  - The board says it uses shareholder feedback in its decisions [BG-0005].
- The board consulted customers, suppliers, investors and regulators on the 2024 CEO choice [BG-0018, BG-0020]. It now
  has an airline CEO on its Safety and Finance committees [BG-0039].
- It sees shareholders and stakeholders as aligned over the long run [BG-0006].

### Pay horizon (the incentive plans the board sets)

- **Annual incentive (2025, kept for 2026):** one company-wide score [BG-0056].
  - 80% financial: free cash flow 40%, core EPS 20%, revenue 20% (the 80/20 split is re-confirmed; the split inside
    the 80% rests on the drafter's searches).
  - 20% a Safety & Execution scorecard, judged holistically.
  - Paid 131% for 2025.
- **Annual incentive (2024):** Commercial Airplanes was weighted 60% on safety and quality and 40% on finance [BG-0055].
  Safety metrics have been in the annual plan since 2021 [BX-0251].
- **Long-term incentive:** performance units pay on three-year cumulative free cash flow. A product-safety modifier
  can cut the payout by 25% or to zero [BG-0026]. The earlier relative-TSR units paid nothing in 2023 [BG-0027]. In
  2015 long-term pay had been realigned to shareholder returns [B-1048].
- **Board judgement over formula:**
  - Long-term awards were cut 22% after the January 2024 accident [BG-0055].
  - The CEO declined his 2023 bonus [BG-0055].
  - Former CEO Calhoun said in 2022 that he trusted the board to judge him on decades-long programme outcomes, whether
    or not the pay formula was aligned [BG-0010].
- **CEO hiring award:** premium-priced options vesting over two to four years [BG-0057, uncorroborated and not
  re-searched **(inference)**].
- **Net:** a horizon of one to three years, cash-weighted and gated by safety. That is much shorter than the 10-25-year
  programmes on the dash-2050 board.

### What the culture means for its votes (inputs for the agent's tests and vetoes)

| Proposed test | Rule (computable from the ExCo package and the brief) | Ids |
|---|---|---|
| Rating first | Veto a package whose spend the CFO memo shows would threaten the investment-grade rating, or which fails the CFO's buffer test | BG-0029, BG-0062, B-2327 |
| Downside | No Board item loses more than $1B (the ExCo's ε) against its default in any plausible column: at 4.5, half the CFO's $2B buffer **(threshold: inference)** | BG-0029, BG-0062, BG-0034, BG-0068 |
| Business case | Approve a launch only if it beats Do Nothing in the brief's expected column (by more than the $1B tie band used by the ExCo) | BG-0021, BG-0022, B-1479 |
| Readiness | No launch while the brief reports a live quality, FAA or certification problem, or while the developments are unfinished | BG-0043, BG-0050, BG-0068, B-2303 |
| Market ready, technology ready, Boeing ready | All three needed for fps | BG-0068, B-2303, BX-1303 |
| Do less, better | Prefer the plan with less to execute only when the values are within $1B in every plausible column (the 10-year over the 7-year ramp, no fps and 787 Re-engine overlap); otherwise the plan with the higher worst column. A recommendation, not a veto **(inference)** | BG-0068, BX-1239 |
| Cancellation (time horizon 3) | Core developments protected: veto a cancel unless keeping the programme loses at least $1B in every plausible column **(inference)** | BG-0022, B-1729, B-2167 |
| Rate increase | Approve only with stable KPIs and an FAA-cleared rate path. It is below the real threshold, so defer to management otherwise. | BG-0069, B-2236 |
| Hold | Never vetoed | |

---

## 5. Decision record (decisions the board took or approved)

| Date | Decision | Ids |
|---|---|---|
| 2006-08 | New $3B share repurchase programme | BX-0566 |
| 2007-10 / 2008-01 | $7B buyback; dividend +14% | B-0061, BX-0591 |
| 2011-08-30 | Approved the launch of the 737 MAX (Re-engine) on 496 commitments; announced before the board met | BG-0066, B-0521, B-0419, B-0438 |
| 2013-11 | 777X launch at the Dubai Airshow on 259 orders and commitments; its timing was "up to the approval of the Board" | B-0763, BG-0067 (launch month and orders corroborated; the board's authorisation date not found) |
| 2013-12-16 | $10B buyback; dividend +50% | B-0877, B-0852 |
| 2014 | Let the CEO (McNerney) stay past age 65; implied by his answer on a call, not a board statement | BG-0023 |
| 2014-12 to 2018-12 | Buyback authorisations of $12B, $14B, $14B, $18B and $20B, with dividend increases each year | B-0966, B-1089, B-1219, B-1327, BG-0035 |
| 2018-12-17 | Agreed terms of the Embraer partnership (JV, 80% stake for $4.2B); terminated April 2020 | B-1493, B-1674, B-1792 |
| 2019-04 | Formed a special committee on airplane policies and processes; buybacks suspended | BX-1172, BG-0049, B-1677 |
| 2019-08/09 | Created the permanent Aerospace Safety Committee and a Product and Services Safety organization | BG-0049, BG-0001 |
| 2019-10-11 | Split the chair and CEO roles; Calhoun became non-executive chair | BG-0047, BX-1217 |
| 2019-12-22/23 | Replaced CEO Muilenburg to restore confidence (effective 22 December per the 8-K, announced 23 December); Calhoun CEO, Kellner chair | BG-0048, BG-0009 |
| 2020-03 | Terminated the buyback authorisation; suspended the dividend | BG-0034, B-1677 |
| 2020-06 | Amended the principles to require an independent chair | BG-0046, BG-0002 |
| 2021 | Safety and quality metrics added to annual incentives | BX-0251 |
| 2021-04-20 | Extended the CEO retirement age to 70 for Calhoun | BG-0003 |
| 2021-11 | Directors settled the safety-oversight derivative suit ($237.5M); added an aviation or safety director | BG-0052, BG-0051 |
| 2024 (Q1) | Pay reset after the Alaska accident: 60% safety and quality weight at Commercial Airplanes; long-term awards cut 22% | BG-0055 |
| 2024-03-25 | CEO to leave at year end; Kellner out; Mollenkopf independent chair; new head of Commercial Airplanes | BG-0061 |
| 2024-07-31 | Chose Kelly Ortberg as CEO after a 9-month search led by the chair | BG-0017, BG-0018 |
| 2024-10-30/31 | About $24B equity raise (common plus mandatory convertible preferred) | BG-0028, BG-0062 |
| 2025 | Bonus moved to one company score; safety and execution 20% | BG-0056 |
| 2025-04-22 | $10.55B sale of Jeppesen and other digital assets (closed 2025-11-03) | BG-0063 |
| 2025-05 | DOJ non-prosecution agreement (over $1.1B); board role **(inference)** | BG-0065 |
| 2025-12-03 | Elected Brad Tilden (Safety and Finance committees) | BG-0039 |
| 2025-12-08 | Closed the Spirit AeroSystems acquisition (about $4.7B equity, about $8.3B with debt) | BG-0064 |
| 2025-12-17 | Amended the Finance Committee charter, which covers significant investments and capital projects (that this item was added then is not confirmed) | BG-0044 |

---

## 6. Relationship with management

**Structure and authority**
- The chair and CEO roles are separate. Since 2020 the governance principles require an independent chair
  [BG-0047, BG-0046, BG-0002].
- The board owns CEO selection outright. The 2024 choice was "the Board's call", made after nine months of
  consultation; the outgoing CEO said he "wasn't really in the decision-making process" [BG-0018, BG-0020].
- The board selects the CEO and has removed one [BG-0045, BG-0048]. That the CEO serves at its pleasure is
  **(inference)**; as Calhoun put it in 2021 of his own tenure, it is the board's to set [BG-0016].

**How it uses that authority**
- It acts when trust with the regulator breaks. In 2019 it took the chair from the CEO and then replaced him
  [BG-0047, BG-0048, BG-0009].
- In 2024 it renewed both the chair and the CEO after the door-plug accident [BG-0061].
- It defers to management on operations and rate pacing [BG-0045, B-2236].
- It holds management to the business case presented to it [BG-0022].

**History of deference and tension**
- Until October 2019 the chair and CEO roles were combined, and the board defended that structure; the CEO spoke to it
  "daily" in both roles [BX-1176].
- It opposed splitting the roles in April 2019 [BG-0047].
- It let management announce the MAX ahead of formal approval [B-0521].
- **Tensions:**
  - Investors and proxy advisers [BG-0058, BG-0046].
  - The Delaware court [BG-0051].
  - The FAA panel's finding of a disconnect between senior management and the workforce [BG-0050].

**The three ExCo agents**

| Agent | Relationship with the board | Ids |
|---|---|---|
| **Ortberg (CEO)** | The board's own hire, chosen for 35 years of aerospace operating experience. His priorities match the board's culture: culture and stability, then development execution, then debt first and investment grade before the next airplane, then a new airplane only when market, technology and Boeing converge. The board's guidance should be about holding that line, not pushing him **(inference)**. | BG-0017, BG-0018, BX-1245, B-2327, B-2303, BX-1303 |
| **Malave (CFO)** | No board-specific evidence. His stated first priority, "fully restoring the health of our balance sheet" while supporting the investment-grade rating, is the board's first financial test. The Finance chair (ex-UTC CFO) will read his memo closely **(inference)**. | BX-0556, B-2345, BG-0041 |
| **Pope (head of Commercial Airplanes)** | Boeing named her to lead Commercial Airplanes in the March 2024 shake-up (her appointment was not restated at re-search). Production, quality and rate readiness are her remit, and the Aerospace Safety Committee hears the related engineering and safety reports. | BG-0061, BG-0043, BG-0025, BX-1331 |

---

## 7. How it reads rivals

- **There is no board-level statement on Airbus or the engine makers.**
- **Only indirect evidence:**
  - The board's 2011 Re-engine launch was tied in coverage to A320neo order wins and the defection of a long-time
    customer [BG-0066, B-0521].
  - The CEO the board selected declined to match Airbus's timeline for a new airplane [B-2313, BG-0068]. That the board
    shares this view is **(inference)**.
- **Fallback:** read rivals through the company profile and the CEO's case; do not invent a board view
  **(inference)**.

---

## 8. Confidence and gaps

**Gaps**
1. **No dollar threshold for reserved matters.** Boeing publishes none (unlike Airbus). The mapping relies on the
   Finance Committee charter and the two-gate launch process.
2. **No vote splits or minutes.** How dissent is handled is unknown.
3. **No recent board words in transcripts.** The current chair, Mollenkopf, has none; the 2026 chair letter was not
   reached by search. The voice relies on Kellner (2021) and on the CEO's account of the board.
4. **Uncorroborated details:**
   - the 2026 Aerospace Safety, Finance and Audit chairs rest on third-party data, not a Boeing document [BG-0041];
   - the Compensation Committee chair [BG-0042];
   - the CEO hiring award [BG-0057], not re-searched;
   - the 777X launch day and the date of the board's authorisation [BG-0067] (the launch month and orders are now
     corroborated).
   - Two web items were withdrawn at verification because they could not be confirmed: a reported BlackRock vote
     against the Aerospace Safety chair in 2024 (former 0059) and one analysis's claim that the common dividend restarted
     in 2025 (former 0070), which the filings and the 2025 calls do not support.
5. **Special Programs Committee.** Its remit is not in the evidence.
6. **Web re-search (2026-10-10) was capped at 30 searches.** 31 of 32 web items were re-searched; BG-0057 was not.
   Some details within confirmed items were not re-confirmed (for example the split inside the 2025 bonus's financial
   80% [BG-0056] and the savings-plan and government holdings [BG-0060]); each item's `verification_note` names them.
7. **No evidence after July 2026.** There is no data on the board's view of the 2026 Farnborough-era market or on any
   2026 decisions beyond the annual meeting.
8. **No board statement on rivals, engine choice or partnerships for a new airplane.**

**Fallback**
- Where the record is thin, use the company profile (`profile.md`), past board decisions (section 5) and the culture
  scores above.
- Defer to the CEO's case unless a test fails.
- Never invent a board view.
