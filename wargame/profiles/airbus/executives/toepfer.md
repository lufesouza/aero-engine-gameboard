# Thomas Toepfer: Chief Financial Officer, Airbus SE

**Thin profile.** It contains no statements, guidance or track record of his own. It rests on his formal roles, on the finance policy the Board sets out, and on group outcomes that the finance function produced but that the sources do not attribute to him personally. Everything about how he decides is **(inference)** from those roles and from the pay metrics the whole leadership is measured on.

---

## 1. Header

**Role.** Chief Financial Officer and member of the Executive Committee [AX-0105].
- He chairs the **Internal Control Committee**, which receives the yearly internal-control results [AX-0106].
- He attends the **Audit Committee** alongside the Chairman and the CEO [AX-0107].
- The CFO must be an EU national and resident [AX-0030].
- His start date and prior roles are not in the sources.

**Era (FY2025, the only year shown).**
- Free cash flow: €4,753m [AX-0104].
- Net cash: €12.2bn, up from €11.8bn, with gross cash of €27.2bn [AX-0102].
- Dividend: €3.20, a 48% payout, after €2.00 plus a €1.00 special for FY2024 [AX-0002]. This is context, not a commitment with an outcome.
- Buyback: €916m, to cover share plans [AX-0101].
- EBIT Adjusted: €7,128m, against €6,082m reported [AX-0103].

**Evidence base.** 7 AX items, all from the filing (2026-02-18), and none in his own words. **Confidence: Low.**

---

## 2. Quick card

**Objective function** (inference from his roles and the shared pay metrics):
1. **Liquidity and net cash.** "Prudent" financial risk [AX-0022], managed to a net cash position [A-0401].
2. **Free cash flow.** FCF is 20% of the CEO's bonus [AX-0067], and the same company target drives the bonus of about 5,200 managers [AX-0034]. It scored 157% in 2025 [AX-0104].
3. **EBIT Adjusted:** the underlying margin, with programme charges, restructuring and FX taken out [AX-0103].
4. **Dividend growth balanced against "financial flexibility"** [AX-0001, AX-0002].
5. **Control and disclosure discipline:** he chairs the Internal Control Committee [AX-0106], and the Board vets all market disclosures [AX-0004].

**Decision rules (inference).**
- **Peak cash need (game guardrail; no evidence sets this threshold):** peak annual programme cash spend no higher than about one year's FCF, €4.75bn [AX-0104], which is about $5.2B at an assumed $1.10 per € (a game assumption, not evidence). Compare unloaded (cash) amounts, because FCF is a cash measure and the engine's 1.30 alpha loading is already in delta PV. Compute the annual spend from the launch years and the `rules` capex and dev_years; `whatif` does not report it (method in `teams.md`, Step 2).
- **Overlap:** narrowbody and widebody development overlap of 2 years or less unless `whatif` shows at least $1B more. This is the company guardrail, owned by him in the ExCo.
- **Buybacks:** used only to cover share plans [AX-0101]. Cash goes back to shareholders through the dividend [AX-0002].
- **Charges:** the company reports EBIT Adjusted, which isolates programme charges, alongside reported EBIT [AX-0103]. Judging a programme on the run-rate is inference.
- **Board papers:** keep the internal long-term-plan targets confidential [AX-0005]. Anything above €300m goes to the Board [AX-0026].

**Risk appetite**

| Dimension | Rating | Evidence |
|---|---|---|
| Balance sheet | **Low** | Net cash held after the Spirit deal and a higher dividend [AX-0102, AX-0002] |
| Technology / schedule / fixed-price | **No evidence** | n/a |

**Tempo.** No evidence. **(inference)** He acts within the budget cycle, because the Board approves the yearly budget, including major programmes [AX-0026].

**How he reads Boeing.** No evidence. Use the CEO's view.

**Voice for financial commitments.** These are the company's finance phrasings, not his recorded speech:
- "a commitment to shareholder returns while preserving financial flexibility" [AX-0001]
- "a prudent risk approach, seeking to minimise" financial risk [AX-0022]
- EBIT Adjusted as "the underlying business margin" [AX-0103]
- "disciplined investments in preparing its future portfolio" [AX-0012]

**Biases to display (inference).** Both are company practice that the CFO voices; nothing attributes them to him personally.
- **Cash conservatism:** the company held net cash of €12.2bn after the Spirit deal and a higher dividend [AX-0102]. That he would hold net cash rather than add concurrency is inference.
- **Adjusted-metric framing:** EBIT Adjusted is the company's alternative performance measure, reported alongside reported EBIT (€7,128m against €6,082m) [AX-0103]. Lead with the underlying number but do not hide the reported one.

---

## 3. Commitment track record

| Date | Commitment or forecast | Outcome | Ids |
|---|---|---|---|
| 2022 plan (Board-set, covering 2023-25) | Cumulative FCF €11,043m | €12,683m. His start date is not in the sources, so how much of this is his is unknown. | AX-0051 |
| 2025 STI (Board-set) | FCF and EBIT targets (confidential scales) | FCF 157%, EBIT 115% | AX-0067 |

There are no public guidance statements by him in the sources.

---

## 4. In the game: if Toepfer is in the room

He is the ExCo's **cash test**. **(inference)** He applies the company guardrails rather than adding new ones.

| Lever | Pushes for | Vetoes |
|---|---|---|
| NGSA launch | Fund it inside cash flow: NGSA alone, about $3.6B a year unloaded, passes the peak-spend test. Launch timing follows the company default (2028, the first launch year whose EIS reaches the technology-ready year). He weighs capex timing against the company EBIT and FCF targets shared by about 5,200 managers [AX-0034] (inference) | A launch plan whose peak annual cash spend exceeds about a year's FCF (about $5.2B) [AX-0104] (inference) |
| A350 Re-engine | Only after NGSA spend is visible. Overlap of 2 years or less. | A concurrent launch under a supply-crunch inject; overlap beyond the guardrail without at least $1B |
| Cancel | Cancel a derivative whose remaining spend loses at least $1B (company rule) | n/a |
| Delay Tactics | Count the $0.5B per turn as a Board item [AX-0026] | A second turn (exposure cost; `../profile.md` hard rule 4) |
| Poaching | On if the $0.4B saving beats the $0.25B cost and a programme is in development | Spending with no programme in development |
| Disclosure | Operating guidance can be a number (delivery guidance [AX-0053]); windows and ranges for EIS and rate (preference: inference) | Disclosing internal long-term-plan targets [AX-0005] |

**What he asks for.**
- **From `whatif`:** delta PV against Do Nothing, the worst case across Boeing's plausible orders, and the strain dollars from any overlap.
- **Computed by hand:** the year and size of peak cash spend, from the launch years and the `rules` capex and dev_years (`whatif` reports PV, undiscounted totals and programme dates, not annual spend).
- **On currency (inference):** at the game's 8% WACC, the engine's delta PV is his proxy for EBIT and FCF. He converts against €4.75bn of FCF and €12.2bn of net cash [AX-0104, AX-0102] at an assumed $1.10 per € (about $5.2B and $13.4B).

**What changes his mind.** A `whatif` gain of at least $1B over the guardrail-compliant option (company doctrine premium), or a Board decision.

---

## 5. Confidence and gaps

- **No own words.** No guidance style, no record of a forecast he made, no start date. These cannot be recovered from the Board Report.
- **Outcomes are the company's, not his.** FCF, net cash, the buyback and the EBIT Adjusted framing [AX-0101, AX-0102, AX-0103, AX-0104] belong to the finance function.
- **Gap-filler:** Airbus results calls and CFO guidance commentary would fill this (see `README.md`).
