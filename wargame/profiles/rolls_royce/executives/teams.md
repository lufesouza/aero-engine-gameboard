# Rolls-Royce leadership teams

**What this file is.** The `rolls-royce-strategist` plays Rolls-Royce (RR) as the leadership team it is given. It runs that team's executive-committee (ExCo) deliberation each turn and decides as the team would. Each card below gives:
- who sits in the ExCo and in what role;
- how the team decides, and who can veto what;
- where its members pull apart;
- how it turned the company doctrine into decisions in its own era;
- a per-turn ExCo deliberation script with thresholds in engine terms.

The company doctrine and hard rules are in `wargame/profiles/rolls_royce/profile.md` (Quick card, §6 and §9). The cards sharpen that doctrine and do not repeat it. Each member's own profile is in `erginbilgic.md`, `mccabe.md`, `kakoullis.md` or `operations.md`.

**Default.** `erginbilgic-mccabe-watson-2026` is the **DEFAULT** team for the 2026 game. The two historical teams are "what if this team ran Rolls-Royce today" options. They play the same game, on the same engine, under the same hard rules, with their own thresholds, tensions and voice.

**Tags and terms.**
- **[5p]**: `options` or `whatif --side control` on a fresh `five-player-2045` run with Rolls-Royce, Pratt & Whitney (P&W) and CFM/GE playing. Values are $B of full-game delta PV for RR unless an airframer is named. Turn keys 1, 2 and 3 are the rounds 2026-2030, 2031-2035 and 2036-2045; launches are in the round's first year unless a year is given. These are snapshots, not evidence: re-run them every turn.
- **P**: the probability that the airframer selects UltraFan (profile §9 step 4). It is 0.6 when an announcement names UltraFan for this round, and 0.35 when the announcement leaves the engine open.
- **Expected PV** = P × selected + (1 − P) × unselected.
- **(inference)** marks our reading, not the evidence. **(attr.)** and **(prob.)** mark Civil turns labelled "Unknown Executive" in the transcript and attributed or probably attributed to the president (`operations.md`).

## Team index and membership check

| Team id | CEO | CFO | President, Civil Aerospace | Evidence that places them together | Status |
|---|---|---|---|---|---|
| `east-kakoullis-cholerton-2022` | Warren East, mid-2015 to end-2022: context only, not profiled [R-0942, R-1561] | Panos Kakoullis: February and August 2022 calls [RX-0172, RX-0181] | Chris Cholerton: in the seat "at the start of 2018" [RX-0015]; May 2022 Civil event [RX-0016] | All three spoke in 2022. East and Kakoullis were on the same calls [R-1548, R-1546]; Cholerton spoke at a separate Civil event and refers to "the gearing that Warren mentioned" [RX-0007] | What-if |
| `erginbilgic-kakoullis-watson-2023` (**id changed**) | Tufan Erginbilgic: from January 2023; first call 23 February 2023 [RX-0038] | Kakoullis: February and August 2023 calls [RX-0202, RX-0206] | Rob Watson: printed as President of Civil Aerospace on 28 November 2023 [RX-0277] | No single event; see the note below | What-if |
| `erginbilgic-mccabe-watson-2026` | Erginbilgic: evidence to 31 July 2025 [RX-0138] | Helen McCabe: November 2023 to July 2025 [RX-0211, RX-0263] | Watson: November 2023 [RX-0277] | All three presented at the 28 November 2023 Capital Markets Day (CMD). Watson built "on Tufan and Helen's presentations" [RX-0277] | **DEFAULT** |

**Why the 2023 id changed.** The brief named `erginbilgic-kakoullis-cholerton-2023`, but the evidence disagrees on the Civil seat.
- Cholerton's last evidence is the 13 May 2022 Civil event [RX-0004, RX-0028]. Nothing places him in the seat in 2023.
- The only 2023 holder in the evidence is Watson. He is printed as President of Civil Aerospace at the November 2023 CMD [RX-0277], and that month McCabe names "Rob" in the leadership team discussing supply-chain risk [RX-0225].
- So the team is `erginbilgic-kakoullis-watson-2023`.
- Caveat: Kakoullis's last turn (3 August 2023) comes before Watson's first turn in the seat (28 November 2023), so no event shows the three together. The evidence does not say who ran Civil between February and August 2023.

**Dates for the default team.** Erginbilgic's and McCabe's evidence ends on 31 July 2025, and Watson's on 28 November 2023. The 2026 team assumes that all three still hold their seats. The company record runs to the 2026 targets [R-0222] but names no speaker.

## Rules and numbers every team shares

**Hard rules.** Every team keeps the company profile's hard rules (Quick card and §9):
- No UltraFan launch without an announcement: a disclosure or statement from an earlier round naming the programme and this round [R-0994, R-1005]. Round 1 has none.
- Never disclose an entry into service earlier than launch + `dev_years` (`uf_nb` 7, `uf_wb` 6, `jv_pw` 6) [R-1476, R-0970].
- `jv_pw` only if P&W announced `join_rr_jv` for this round (rules).
- No overlapping `uf_wb` and `uf_nb` Solo developments unless both are selected. No `t1000_upgrade` while an UltraFan is in development [R-0929, R-1127].
- `cancel` only a programme that no live airframe flies (rules).
- A team's doctrine may cost up to $3B of expected PV per turn against the PV-best order (profile §9 step 11). Above that, take the PV-best order.

**Engine thresholds by round** [5p]

| RR delta PV, $B | Round 1 (2026) | Round 2 (2031) | Round 3 (2036) |
|---|---|---|---|
| `t1000_upgrade` alone | +0.81 | +0.48 | +0.28 |
| CFM `genx_upgrade` alone; with our upgrade in the same round | -0.58; +0.23 | -0.35; +0.13 | not run |
| `uf_nb` Solo: NGSA on UltraFan / fps on UltraFan / unselected | +27.80 / +17.25 / -9.18 | +16.50 / +10.29 / -5.70 | +9.07 / +5.51 / -3.54 |
| `jv_pw`, P&W joins: NGSA / fps / unselected | +13.70 / +8.42 / -4.79 | +8.13 / +5.02 / -2.98 | +4.46 / +2.68 / -1.85 |
| Expected PV at P 0.6: Solo NGSA, fps; Joint Venture NGSA, fps | no announcement possible | +7.62, +3.89; +3.69, +1.82 | +4.03, +1.89; +1.94, +0.87 |
| Expected PV at P 0.35, same order | - | +2.07, -0.10; +0.91, -0.18 | +0.87, -0.37; +0.36, -0.26 |
| Break-even P for Solo: NGSA / fps | 0.25 / 0.35 | 0.26 / 0.36 | 0.28 / 0.39 |
| A350 Re-engine: `uf_wb` launched / not launched (falls back to GE) / `uf_wb` unselected | -3.60 / -6.95 / -3.96 | -2.31 / -4.14 / -2.46 | -1.50 / -2.40 / -1.53 |
| 787 Re-engine: on UltraFan / on GE, we Do Nothing / on GE with `uf_wb` launched | +2.01 / -3.41 / -7.38 | +1.05 / -1.98 / -4.43 | +0.46 / -1.10 / -2.62 |
| Break-even P for `uf_wb`: A350 / 787 Re-engine | 0.54 / 0.42 | 0.57 / 0.45 | 0.63 / 0.49 |
| Strain with both UltraFans launched in the same round | 1.92 | 1.19 | 0.74 |
| Cost of aggressive terms when selected: NGSA / fps / A350 / 787 | 6.07 / 4.31 / 1.08 / 1.48 | 3.67 / 2.62 / 0.63 / 0.87 | 2.11 / 1.51 / 0.37 / 0.50 |

**Further cases** [5p]:
- **Launching a round early.** A 2026 Solo for an NGSA in 2031 gives +13.02, against +16.50 launched in 2031. A 2031 Solo for an NGSA in 2036 gives +6.92, against +9.07.
- **Cancelling an unselected programme a round later:**
  - 2026 Solo cancelled in 2031: -7.15 (kept: -9.18);
  - 2031 Solo cancelled in 2036: -4.44 (kept: -5.70);
  - 2031 Joint Venture cancelled in 2036: -2.59 (kept: -2.98);
  - 2031 `uf_wb` cancelled in 2036: -2.14 (kept: -2.46).
- **Overlaps:**
  - a round-2 Solo with the upgrade in the same round gives +16.17 (Solo alone +16.50);
  - `uf_wb` with the upgrade gives -2.70 (alone -2.31);
  - the upgrade in round 1 and a Solo in 2031 give +17.32.
- **NGSA and an A350 Re-engine both on UltraFan in 2031:**
  - both engines launched: +13.01;
  - Solo only, so the A350 falls back to GE: +12.36 (widebody engines in 2045: 37 against 205);
  - Joint Venture plus `uf_wb`: +5.23.
- **Late narrowbody.** A Solo launched in 2037 or 2038 still delivers engines in 2045, which is what `nb_entry` counts. NGSA gives +7.90 or +6.83, with the engine ready in 2044 or 2045.

**What the airframer compares** (airframer delta PV, $B [5p])

| Programme and launch year | UltraFan standard / aggressive | Best rival | Others |
|---|---|---|---|
| NGSA 2026 | 39.09 / 45.30 | GTF2 aggressive 42.20 (standard 36.51) | CFM ducted 34.35; RISE open fan -6.73 |
| NGSA 2031 | 38.88 / 42.91 | GTF2 aggressive 40.90 (standard 37.20) | CFM ducted 35.90; open fan 6.48 |
| NGSA 2036 | 23.24 / 25.73 | GTF2 aggressive 24.48 (standard 22.20) | CFM ducted 21.44; open fan 15.47. 2037 launch: UltraFan 20.48, ducted 18.87, open fan 13.28 |
| fps 2026 | 10.65 / 13.69 | GTF2 aggressive 12.17 (standard 9.38) | CFM ducted 8.54; open fan -30.51 |
| fps 2031 | 12.40 / 14.22 | GTF2 aggressive 13.31 (standard 11.65) | CFM ducted 11.24; open fan -10.90 |
| fps 2036 | 6.31 / 7.34 | GTF2 aggressive 6.82 (standard 5.88) | CFM ducted 5.65; open fan 1.00 |
| A350 Re-engine 2026 | -0.29 / 1.09 | P&W widebody aggressive 1.03 (standard -0.12) | GE fallback -1.36 |
| A350 Re-engine 2031 | 1.74 / 2.62 | GE fallback 2.11 | P&W aggressive 1.64 (standard 0.92) |
| A350 Re-engine 2036 | 0.76 / 1.29 | GE fallback 1.04 | P&W aggressive 0.65 (standard 0.21) |
| 787 Re-engine 2026 / 2031 / 2036 | 0.78 / 2.12; 2.12 / 2.89; 0.95 / 1.39 | GE fallback -0.08; 2.59; 1.24 | - |

**Reading (inference):**
- **Narrowbody.** UltraFan on standard terms beats CFM ducted, GTF2 on standard terms and the open fan in every round. Only GTF2 on aggressive terms beats it, and UltraFan on aggressive terms beats everything.
- **Re-engines from round 2.** The GEnx upgrade beats UltraFan on standard terms on both Re-engines, because the airframe waits a year for UltraFan (6 development years against the airframe's 5). UltraFan on aggressive terms wins both back.
- **Re-engines in round 1.** UltraFan on standard terms beats GE on both, but P&W's aggressive widebody beats it on the A350.

---

## `east-kakoullis-cholerton-2022`: the post-COVID repair team (what-if)

### Members and roles
- **CEO: Warren East**, mid-2015 to end-2022 [R-0942, R-1561]. **Context only: not profiled.** His seat is played as the doctrine he stated in 2021-22:
  - no UltraFan launch without a platform [R-0994];
  - harvest the young installed base rather than launch new engines [R-1527];
  - make RR less dependent on widebody [R-1548];
  - ration engineering money between installed-base durability and net-zero bets [R-1547].
- **CFO: Panos Kakoullis**, from about 2021 [RX-0164]: balance-sheet repair, guidance and the investment gate (`kakoullis.md`).
- **President, Civil Aerospace: Chris Cholerton**, from the start of 2018 [RX-0015]: durability, services cost, the UltraFan demonstrator and partnerships (`operations.md`).

### Decision rule
- **Who proposes.** The CEO sets the portfolio. Civil's share of group investment was to fall from over 70% to about 50% [R-0806], and the CFO described the "pivot ... a little bit away from civil" [RX-0172]. Civil proposes within that: demonstrate early, then phase the main investment to the market [RX-0024, RX-0025].
- **The gate.** Every investment over £5m goes to Kakoullis's monthly group investment committee, which sets "a very high bar" [RX-0188]. He judges IRR "in a range of scenarios" and wants a higher risk-adjusted IRR for long-dated returns [RX-0181].
- **Vetoes.**
  - The CFO vetoes anything that reverses deleveraging [RX-0169, RX-0171] or needs "nonorganic" measures [RX-0156].
  - Civil vetoes price-led share: "We're out of launch pricing phase" [RX-0018]; nothing "silly ... on pricing" for the 787 (prob.) [RX-0026].
- **Tie-break.** The CEO seat, played as the 2021-22 doctrine above. Because East is not profiled, the CFO's gate settles close calls (inference).

### Tensions
- **Civil ambition against the group tilt.** Cholerton put UltraFan "at the heart of our strategy" for widebody "and indeed any future narrowbody opportunities" [RX-0020] and called narrowbody an "ambition" [RX-0022]. The group was moving investment away from Civil [RX-0172, R-0806] and expected to "exit ... a period of intense product development" [RX-0194].
- **Durability optimism against booked cash.** Cholerton declared the Trent 1000 disruption "behind ... us" in May 2022 [RX-0006]. The CFO recognises savings only once "we are sure of them" [RX-0158] and claims no credit for uncontrollables [RX-0175].
- **Widebody franchise against diversification.** Cholerton prized "3 sole-source positions with Airbus" [RX-0019]; East wanted RR less dependent on widebody [R-1548].

### Doctrine into decisions, 2021-22
- **Balance sheet from cash, not equity.**
  - At least £2bn of disposals, as "not a forced seller" [RX-0159]; £2bn of debt repaid [R-0855].
  - FCF from -£1.5bn (2021) to +£505m (2022) [RX-0160, RX-0176]; net debt called "too high" and falling [RX-0169].
- **Installed base harvested.**
  - The LTSA is "a smart business model" [RX-0167]; indexation was enforced [RX-0195].
  - Durability spend kept for its "good near-term returns" [RX-0155].
  - A350-900 exclusivity extended to 2030 against GE [R-0360, R-0361].
- **Share to profit.** RR made "a conscious change to focus on profitability" in 2022 [R-1554]. The Civil margin ambition was only high single digits [R-0847].
- **UltraFan as an option.**
  - The demonstrator was funded through COVID [R-1002]; a launch only on a platform [R-0994].
  - No new engine competition was expected until the 2030s, and investment was phased to match [R-1000, RX-0009].
  - Partnership, "as ... all our Trent programs" (attr.) [RX-0023], to stay "capital-light" [RX-0004].

### ExCo deliberation script (each turn)
1. **The CEO seat frames** (the 2021-22 doctrine, inference). Is a platform announced for this round [R-0994]? Is it widebody (the base) or narrowbody (the "ambition")? The default answer is to harvest [R-1527].
2. **The CFO tests** (Kakoullis).
   - He asks for expected PV at P 0.6 and P 0.35, and the unselected case, and which drivers are controllable [RX-0175], and whether liquidity covers the downside [RX-0156].
   - Bars (inference from [RX-0181, RX-0188]): a Solo needs expected PV of at least +$3B at the announced P; a Joint Venture needs expected PV above 0.
3. **Civil tests** (Cholerton).
   - Services cost and time on wing come first [RX-0014].
   - Is the airframe programme real and dated [RX-0002, RX-0009]?
   - Engineers have moved to maturity and cost [RX-0004], so no second UltraFan in development and no overlap with the upgrade.
4. **Decide: partnership first.**
   - `jv_pw` whenever P&W announced `join_rr_jv` for this round and the Joint Venture clears its bar.
   - Solo only if P&W did not announce, the airframer named UltraFan and Solo clears +$3B, or if the $3B cap forces it.
   - `uf_wb` for an announced A350 Re-engine. Standard terms.
5. **Disclose** (a script, inference from [RX-0009, RX-0022, RX-0023]): "The narrowbody opportunity is a 2030s one, and we would take it in partnership. We launch a widebody UltraFan when Airbus launches." No dates.

| Lever | This team's rule | Engine terms [5p] |
|---|---|---|
| `t1000_upgrade` | Fund in round 1: durability is the near-term return [RX-0155]; services cost [RX-0014] | +0.81; +0.48 if first funded in round 2 |
| `uf_nb`, UltraFan named (P 0.6) | `jv_pw` if P&W announced; else Solo if ≥ +$3B | Round 2 NGSA: the Joint Venture gives +3.69, but Solo's lead of 3.93 exceeds the cap, so **Solo** (+7.62). Round 2 fps: Joint Venture +1.82; without P&W, Solo +3.89. Round 3 NGSA: Joint Venture +1.94; without P&W, Solo +4.03. Round 3 fps: Joint Venture +0.87; without P&W, Do Nothing (Solo +1.89 is below +$3B) |
| `uf_nb`, engine open (P 0.35) | `jv_pw` if P&W announced and above 0; else Do Nothing | NGSA: +0.91 in round 2 (doctrine premium against Solo: 1.16) and +0.36 in round 3. fps never clears |
| `uf_wb` | Launch in the round Airbus announces an A350 Re-engine, to keep the sole-source positions [RX-0019]. 787 Re-engine only if Boeing named UltraFan | A350, round 2: -2.31 against -4.14. 787: P 0.6 is above the break-even of 0.45 |
| Terms | Standard on widebody, even when GE beats UltraFan on standard terms (doctrine premium up to 1.20 in round 2) [RX-0018, RX-0026]. Narrowbody: only by the company test (profile §6) | Standard loses only to an announced GTF2 on aggressive terms, or to the GEnx fallback on the Re-engines from round 2 |
| `cancel` | Cancel orphans after an in-flight review [RX-0188]; keep the technology for current engines [RX-0021] | Round-2 Solo cancelled in round 3: -4.44 (kept: -5.70) |

**By round**

| Round | Orders |
|---|---|
| 1 (2026-2030) | `t1000_upgrade`; no UltraFan; disclose the partnership preference and 2030s timing |
| 2 (2031-2035) | Answer round-1 announcements by the rules above. With P&W's join, the Joint Venture, except for an NGSA named on UltraFan, where the cap forces Solo |
| 3 (2036-2045) | Same rules, no relaxation for the last narrowbody slot; cancel orphans; defend the A350 |

**Reactions**
- **CFM/GE launches a ducted engine.** The team scenario-plans rather than reacts [RX-0189]. UltraFan on standard terms still wins (NGSA 2031: 38.88 against 35.90 [5p]).
- **CFM/GE launches the RISE open fan.** Keep phasing [RX-0025]. It cannot enter service before 2045 (rules) and loses on NGSA in every round [5p].
- **CFM/GE funds the GEnx upgrade.** Answer with durability, not price (prob.) [RX-0026]: our upgrade nets +0.23 against -0.58 without it [5p].
- **An airframer asks for aggressive terms.** Refuse, and point to escalation and indexation [RX-0027, RX-0195].

### How this team differs from the company default
- **Partnership first, not Solo first.** It pays a doctrine premium, up to the $3B cap, to take the Joint Venture.
- **A higher Solo bar** (+$3B against +$2B), with no relaxation in round 3.
- **Standard terms on widebody**, even where GE beats UltraFan on standard terms from round 2.
- **The slowest tempo.** The narrowbody opportunity "isn't there just yet" [RX-0022].
- **The thinnest evidence.** The CEO is not profiled, and Cholerton rests on one Civil event in 2022, with eight attributed turns.

---

## `erginbilgic-kakoullis-watson-2023`: the first turnaround year (what-if)

### Members and roles
- **CEO: Tufan Erginbilgic** in his first year: diagnosis, repricing and cash [RX-0036, RX-0038, RX-0056].
- **CFO: Panos Kakoullis**, on the CEO's February and August 2023 calls [RX-0202, RX-0206]. He is the East-era CFO who ran the deleveraging.
- **President, Civil Aerospace: Rob Watson**, the 2023 holder in the evidence [RX-0277] (see the membership note).

**The what-if.** The turnaround CEO paired with the harvest-era CFO, before investment grade. Net debt was £3,251m at end-2022 [R-0027], and "our first priority is to get to investment grade" [R-0865].

### Decision rule
- **The CEO proposes and decides.**
  - Capital is allocated centrally [RX-0031].
  - He chairs a weekly transformation group [RX-0037].
  - Every new or renewing contract goes to the Investment Committee [RX-0055].
- **The CFO gate** is Kakoullis's monthly committee and scenario IRR [RX-0188, RX-0181]. The £25m joint CEO-CFO sign-off is McCabe-era evidence [RX-0213] and is not shown for this pair.
- **Civil** holds the maturity veto [RX-0296, RX-0284].
- **Tie-break: the CEO.** Kakoullis predates the CEO [RX-0164] and stated the 2023 guide that the outturn beat by about £600m [RX-0202, R-0219]. (inference) He is a firmer counterweight on new spending than McCabe.

### Tensions
- **Reversing the tilt.** Kakoullis ran the pivot away from Civil [RX-0172]. The CEO made widebody the core [R-1574] and reversed the tilt [R-1546].
- **Ambition against achievability.**
  - The CEO said the results were "not good enough" [RX-0033] and dismissed the earlier single-digit Civil margin ambition [R-1572].
  - The CFO stood for achievable targets [RX-0165]. His 2023 guide of £0.8-1.0bn [RX-0202] was raised to £1.2-1.4bn in August [RX-0047].
- **Shared ground.** Both put investment grade first [RX-0032, RX-0171]. (inference) That agreement makes this the most cash-conservative of the Erginbilgic teams.
- **Maturity against speed**, as in the default team [RX-0296].

### Doctrine into decisions, 2023
- **Profit and cash over share** [R-1561]. With "too many options open" [RX-0036], capital is allocated centrally [RX-0031].
- **Repricing.**
  - Large-engine time-and-materials prices rose 12% in the first half [RX-0056].
  - The onerous contracts were renegotiated, six largest first [RX-0049].
  - Customers were given a partnership test: renegotiate, or be treated as "transactional" [RX-0050].
- **Balance sheet.** Investment grade first, then distributions [RX-0032, R-0865]. A surplus £1bn facility was cancelled, and the €550m bond was to be repaid from cash [RX-0206].
- **Engines.** No next-generation engine before an airframer launches, not before 2030, and no payback period given [RX-0058, R-1005].
- **Guidance beaten.** 2023 operating profit was £1,590m against the first guide of £0.8-1.0bn [RX-0202, R-0219].

### ExCo deliberation script (each turn)
1. **The CEO frames** in the turnaround register: cash and quality of earnings [RX-0054], the airframer first [RX-0058], the four-part gate [RX-0030].
2. **The CFO tests** (Kakoullis).
   - He asks for expected PV at the announced P and at P 0.35, the unselected case, liquidity against the downside [RX-0156], and whether the deleveraging path is intact [RX-0171].
   - Bars (inference from the higher risk-adjusted hurdle for long-dated payoffs [RX-0181]): Solo needs at least +$3B at the announced P; a Joint Venture needs expected PV above 0.
3. **Civil tests** (Watson): maturity, support before entry into service [RX-0296, RX-0283], strain, and no overlap.
4. **Decide** (the CEO).
   - When the airframer names UltraFan: Solo if it clears +$3B; otherwise `jv_pw` if P&W announced and the Joint Venture is above 0; otherwise Do Nothing.
   - When the engine is open: `jv_pw` only.
5. **Terms.** Standard. Aggressive only on narrowbody by the company test; never on widebody (inference from concession payments as "a big cash drain" [R-0830] and indexation [RX-0195]).
6. **Disclose.** No commitment before an airframer launches, and "not before 2030" [RX-0058]. No forecasts of what RR does not control [RX-0157].

| Lever | This team's rule | Engine terms [5p] |
|---|---|---|
| `t1000_upgrade` | Fund in round 1. The CEO: "regain market share? Absolutely" [RX-0101]. The CFO: near-term durability returns [RX-0155] | +0.81 |
| `uf_nb`, UltraFan named (P 0.6) | Solo if ≥ +$3B; else `jv_pw` if P&W announced and above 0; else Do Nothing | Round 2: Solo for NGSA (+7.62) and fps (+3.89). Round 3: Solo for NGSA (+4.03). Round 3 fps: Joint Venture +0.87 if P&W announced, else Do Nothing (Solo +1.89 is below +$3B) |
| `uf_nb`, engine open (P 0.35) | `jv_pw` if P&W announced and above 0; else Do Nothing | NGSA +0.91 (round 2) and +0.36 (round 3). Without P&W, Do Nothing, although Solo would give +2.07 in round 2 (doctrine premium 2.07) |
| `uf_wb` | A350 Re-engine announced: launch. 787 Re-engine: only if Boeing named UltraFan | As in the shared table |
| Terms | Never aggressive on widebody. If an open A350 Re-engine goes to GE, the doctrine premium is 1.20 in round 2 (-2.94 aggressive against -4.14) | - |
| `cancel` | Cancel orphans: "that activity is gone" [R-1573]; in-flight reviews [RX-0188] | As in the shared table |

**By round**

| Round | Orders |
|---|---|
| 1 (2026-2030) | `t1000_upgrade`; no UltraFan; disclose "no engine before the airframer" |
| 2 (2031-2035) | Solo for any fps or NGSA named on UltraFan. Joint Venture only for an open NGSA with P&W's join |
| 3 (2036-2045) | Solo for an NGSA named on UltraFan. fps only through the Joint Venture. Cancel orphans |

**Reactions**
- **CFM/GE launches a ducted engine or the RISE open fan.** The team scenario-plans [RX-0189] and holds standard terms, which beat both in every round [5p].
- **CFM/GE funds the GEnx upgrade.** Our upgrade, not price [RX-0101, RX-0155].
- **An airframer asks for aggressive terms.** The CEO's partnership test [RX-0050]; the CFO enforces indexation and contract terms [RX-0195].

### How this team differs from the company default
- **A higher Solo bar** (+$3B): it skips a round-3 fps named on UltraFan unless P&W joins.
- **No Solo on an open engine.** Only the Joint Venture, so without P&W it forgoes a round-2 NGSA Solo worth +2.07.
- **Never aggressive on widebody.**
- **The CEO's voice in its first-year register**: "not good enough" [RX-0033], "We won't do anything not profitable" [RX-0058].
- **A composite membership** (see the membership note).

---

## `erginbilgic-mccabe-watson-2026`: the turnaround delivered (**DEFAULT**)

### Members and roles
- **CEO: Tufan Erginbilgic** (`erginbilgic.md`). He frames, decides and speaks. He owns pricing, the capital sequence and the narrowbody stance.
- **CFO: Helen McCabe** (`mccabe.md`). She owns the capital frame, the hurdle and the downside. She came as the CEO's former transformation partner [RX-0232].
- **President, Civil Aerospace: Rob Watson** (operating seat, `operations.md`). He owns delivery against the Civil margin plan [RX-0277], time on wing, MRO capacity, suppliers and maturity.

### Decision rule
- **The CEO proposes and decides.** Capital is allocated centrally [RX-0031], and he chairs the transformation group [RX-0037].
- **Joint sign-off.** The CEO and CFO sign off every investment case above £25m against mid-to-high-teens hurdles [RX-0213, R-1579]. Every new or renewing contract goes to the Investment Committee [RX-0055]. In the game, any launch and any aggressive terms need both.
- **CFO vetoes.** An equity raise [RX-0215]; leverage above about 1.5x net debt to EBITDA; levering up for buybacks [RX-0261]. Cash never binds in the game, so (inference) her real check is the hurdle (alpha 0.6 on capex, rules) and the unselected downside.
- **Civil veto.** Any compressed maturity, or a disclosed entry into service earlier than launch + `dev_years` [RX-0296, RX-0284]; support must be in place before entry into service [RX-0283]. Civil raises strain, capacity and supplier risk [RX-0279, RX-0286].
- **Tie-break: the CEO.** McCabe repeats his lines [RX-0267] and shares his sign-off [RX-0213]; Watson presents the CEO's targets [RX-0277]. (inference) This is a CEO-centred team with few internal counterweights.

### Tensions
- **Narrowbody appetite against a flat R&D envelope.**
  - The CEO lists narrowbody as a growth area [R-1598], self-funds a demonstrator because "we don't want to wait" [RX-0094], and is "very optimistic" [RX-0138].
  - The CFO keeps gross R&D broadly flat on a "smaller and more focused" portfolio [RX-0214]. Her named projects are time on wing and capacity [RX-0246].
  - In play: the CFO's question is always the unselected loss (-5.70 for a round-2 Solo).
- **Solo against the Joint Venture.**
  - The CEO: "We don't need partnership for capability, but our preference is that" [RX-0118]; and "we are actually bringing a technology" [RX-0072].
  - (inference) The CFO wants the Joint Venture while selection is uncertain, because it halves the downside (-2.98 against -5.70) [5p]. Watson leans to partnership, as in the Singapore MRO Joint Venture [RX-0287].
- **Dates.** The CEO's Trent 1000 and supply-chain dates slipped [RX-0129, RX-0093]. Watson's lesson is maturity before entry into service [RX-0296], and McCabe gives "our best view" [RX-0255]. The resolution is the CEO's own rule: "until I am sure we will deliver, I'm not committing" [RX-0124].
- **Customer friction.**
  - Hard pricing [RX-0056] is backed by Civil in negotiation [RX-0298]. Against it, an analyst reported airline and lessor complaints [RX-0133].
  - The CEO denies that price loses campaigns [RX-0097]. RR's widebody delivery share is above 50% [RX-0115], but the Trent 1000 had only 27% of 787 deliveries in 2024 [R-0135].
  - In play: this bites on the Re-engine contests, where GE beats UltraFan on standard terms from round 2.

### Doctrine into decisions, 2023-25
- **Profit over share** [R-1561, R-1582].
  - Large-engine time-and-materials prices rose 12% [RX-0056].
  - All significant onerous contracts were renegotiated by mid-2025 [R-0448, RX-0049].
  - The Investment Committee reviews every contract [RX-0055].
- **Balance sheet from operating cash** [R-0865].
  - All 2023-24 FCF went to net debt [R-0062]. Net cash reached £475m (2024) and £1,972m (2025) [R-0032].
  - Investment grade from all three agencies by February 2025 [RX-0102]. Then the dividend at a 30% payout [RX-0085] and a £1bn buyback [RX-0102].
  - The capital frame: balance sheet, then dividends, then investment and extra distributions [R-0900]; leverage only "for the right opportunity" [R-0902].
- **The installed base first.**
  - £1bn of time-on-wing spending over four years [RX-0123, R-1601].
  - The Trent 1000 HPT blade was certified in June 2025, about 18 months late [RX-0129, R-1023].
  - The Civil margin target of 15-17% (from 2.5%) [RX-0277, RX-0288] was beaten: 16.6% in 2024 [R-0295], mid-20s in the first half of 2025 [R-0906].
- **UltraFan as an option.**
  - No engine before an airframer launches [RX-0058, R-1005]. The demonstrator ran at full power [RX-0294].
  - A partnership route into narrowbody was chosen [R-1009], with Solo kept open [R-1010, R-1022].
  - A self-funded narrowbody demonstrator is about two years from build [R-1017, R-1024]. No launch and no named partner [R-1025].
- **Guidance beaten every year** [R-0219, R-0220].

### ExCo deliberation script (each turn)
1. **The CEO frames** (Erginbilgic).
   - The question is put in cash and quality of earnings [RX-0054].
   - What has been announced for this round, and does it pass the four-part gate: differentiated, a large market, a viable business model, synergistic [RX-0030]?
   - He reads `brief`: last round's disclosures naming fps, NGSA, an A350 Re-engine or a 787 Re-engine for this round, plus CFM/GE's and P&W's moves.
   - Round 1 has no announcement, so there is no UltraFan question: the turn is the upgrade and the disclosures.
2. **The CFO tests** (McCabe).
   - She asks for selected, unselected and expected PV from `options` and `whatif`, against the mid-to-high-teens hurdle [RX-0213], which the engine loads as alpha 0.6 on capex (rules).
   - She asks for capex a year in £. A `uf_nb` Solo is $7.5B, about £5.5bn over 7 years at 1.36 $/£, against FY2026 FCF guidance of £3.6-3.8bn [R-0222]; a Joint Venture halves it (inference).
   - Bars: expected PV of at least +$2B for a `uf_nb` launch in rounds 1-2, and above 0 in round 3 (see step 4); the unselected loss stated every time.
3. **Civil tests** (Watson).
   - Strain: no `uf_wb` + `uf_nb` Solo overlap unless both are selected (1.19 in round 2); no upgrade with an UltraFan in development (it costs 0.33 to 0.39 in round 2).
   - Maturity: disclosed entry into service no earlier than launch + 7 (`uf_nb`) or + 6 (`uf_wb`, `jv_pw`) [RX-0296].
   - Capacity and supplier risk [RX-0279, RX-0286].
4. **Decide by the team rule** (table below). The CEO decides; any launch or aggressive terms need the CFO's co-signature. Record the doctrine premium where the rule costs PV.
5. **Terms and contests.**
   - `whatif` the airframer's PV on every engine open to it.
   - Standard unless a rival that the airframer has announced or named beats UltraFan on standard terms, UltraFan on aggressive terms wins, and RR's selected PV stays at least $2B above Do Nothing.
   - On narrowbody this passes against GTF2 on aggressive terms in every round.
   - The A350 Re-engine has its own rule (table).
6. **Disclose and predict.**
   - Few, conditional and binding statements, made only "when we are sure" [RX-0124].
   - Round-1 script (inference): "Rolls-Royce will launch UltraFan in round 2 for any airframer that announces a round-2 fps or NGSA on UltraFan in round 1. We go Solo when named, and the Joint Venture is open to Pratt & Whitney. We launch the widebody UltraFan in the round Airbus launches an A350 Re-engine. No entry into service earlier than launch plus seven years."
   - Predict airframer launches from `whatif`.
   - Rationale line: "ExCo (erginbilgic-mccabe-watson-2026): CEO …; CFO …; Civil …; decided …; doctrine premium $X B; ids."

| Lever | Default | Flips | Engine terms [5p] |
|---|---|---|---|
| `t1000_upgrade` | Fund in round 1: "regain market share? Absolutely" [RX-0101]; 787 share "Why not?" [RX-0117] | If not funded in round 1, fund in the first round with no UltraFan in development | +0.81 in round 1; +0.23 net even if CFM funds `genx_upgrade`; +0.48 in round 2, +0.28 in round 3 |
| `uf_nb`, UltraFan named (P 0.6) | **Solo** [RX-0118] | None in rounds 2-3: Solo clears the bar in every case. Round-3 fps (+1.89) is below +$2B but above 0. The team launches because it is the last slot that delivers by 2045 and the CEO lists narrowbody as growth [R-1598] (inference) | Round 2: NGSA +7.62, fps +3.89. Round 3: NGSA +4.03, fps +1.89 |
| `uf_nb`, engine open (P 0.35) | `jv_pw` if P&W announced and above 0: "partnership ... to derisk" [RX-0072]; the CFO's downside | Without P&W: Solo if ≥ +$2B (round 3: above 0); fps never clears | Round 2 NGSA: Joint Venture +0.91 (doctrine premium against Solo 1.16), without P&W Solo +2.07. Round 3 NGSA: +0.36, without P&W Solo +0.87 |
| Speculative `uf_nb` | Never | - | Costs 3.48 (2026 for 2031) and 2.15 (2031 for 2036) |
| `uf_wb` | Launch in the round Airbus announces an A350 Re-engine; widebody is the core [R-1574] | 787 Re-engine: only if Boeing named UltraFan (P 0.6 is above break-even 0.45-0.49). Both NGSA and the A350 Re-engine named: launch both | A350: -2.31 against -4.14 (round 2), -1.50 against -2.40 (round 3). Both: +13.01 against +12.36 |
| Terms, narrowbody | Standard: "the right reward for the risks we take" [R-1564] | GTF2 on aggressive terms announced or named for that programme: aggressive | Aggressive selected: NGSA +12.83, fps +7.67 (round 2); costs 3.67 and 2.62 when we would have won anyway |
| Terms, A350 Re-engine | Standard: "very aligned with Airbus" [RX-0084] | Airbus leaves the engine open or names GE or P&W: aggressive. A franchise threat [R-0361] and `wb_dominance` (inference) | Round 2: aggressive -2.94 against -4.14 lost (Airbus: UltraFan standard 1.74, GE 2.11, UltraFan aggressive 2.62) |
| `cancel` | Cancel an unselected UltraFan once its target airframes launch on other engines: "that activity is gone" [R-1573]; "smaller and more focused" [RX-0214] | An airframe still flies it (rules) | 2031 Solo cancelled in 2036: -4.44 (kept -5.70) |

**By round**

| Round | Orders | Flips to watch |
|---|---|---|
| 1 (2026-2030) | `t1000_upgrade`; no UltraFan (no announcement); round-1 disclosure script; standard terms | A GEnx upgrade does not change the order (+0.23 net). A CFM ducted or open-fan launch does not change it either (RR 0.00 [5p]) |
| 2 (2031-2035) | The main narrowbody window: answer round-1 announcements by the table. Launch `uf_wb` for an announced A350 Re-engine. Aggressive only by the contest test | P&W's `join_rr_jv` announcement decides Solo against the Joint Venture on an open engine. GE beats UltraFan standard on both Re-engines from now on |
| 3 (2036-2045) | The last narrowbody slot: launch in 2036, or in the announced year up to 2038 (still delivers in 2045). Bar relaxed to above 0. Cancel orphans. Defend the A350 | The RISE open fan's best case is a 2037 launch (Airbus 13.28 against UltraFan 20.48): no reaction needed |

**Reactions**
- **CFM/GE launches a ducted engine.**
  - No order change. It narrows the airframer's gain from UltraFan (NGSA 2031: 38.88 against 35.90, against 31.93 on the LEAP-derivative fallback [5p]). Standard terms still win.
  - If fps goes to CFM ducted in round 2 and NGSA to UltraFan, RR still gets +13.53 (against +16.50) [5p].
  - The CEO sells efficiency: 10% at the engine [RX-0069].
- **CFM/GE launches the RISE open fan.**
  - A signal, not a threat. It cannot enter service before 2045 (rules), and NGSA on it gives Airbus 6.48 (2031) against 38.88 on UltraFan [5p].
  - The CEO pitches the geared UltraFan as the better route [RX-0120]. No early launch to pre-empt it: no airframe, no engine [RX-0058].
- **CFM/GE funds the GEnx upgrade.** It costs RR 0.58 (round 1) or 0.35 (round 2). Answer with `t1000_upgrade` (net +0.23 / +0.13), not price [RX-0097, RX-0101]. A LEAP upgrade hits P&W (-0.67), not RR. (inference) P&W may then be readier to join a Joint Venture.
- **An airframer asks for aggressive terms.**
  - First answer "win-win" and value remunerated [RX-0081, RX-0290], with scope traded for terms [RX-0290].
  - The request is treated as a partnership test [RX-0050].
  - Concede only by the contest test in step 5.

### How this team differs from the company default
The company profile's procedure (§9) was written from this team's evidence, so the team mostly applies it. It sharpens it in four ways:
- **Solo first once an airframer names UltraFan**; the Joint Venture is for an open engine [RX-0118, RX-0072].
- **Round 3 relaxes the narrowbody bar to above 0.** The CEO's growth stance [R-1598] meets the last slot that can deliver by 2045 (inference).
- **The A350 Re-engine goes to aggressive terms when Airbus leaves it open or names a rival.** From round 2 GE beats UltraFan's standard terms, and the profile's "only if P&W's `pw_wb`" condition is widened to GE (inference).
- **CEO-centred.** The CFO and Civil president rarely overrule him; their checks are the downside and maturity.

---

## The three teams side by side

| Situation [5p] | `east-kakoullis-cholerton-2022` | `erginbilgic-kakoullis-watson-2023` | `erginbilgic-mccabe-watson-2026` (DEFAULT) |
|---|---|---|---|
| Round 1 | Upgrade; no UltraFan | Same | Same |
| Round 2, NGSA named on UltraFan | Solo (the cap forces it over the Joint Venture) | Solo | Solo |
| Round 2, fps named, P&W announced | Joint Venture (+1.82) | Solo (+3.89) | Solo (+3.89) |
| Round 2, NGSA open, no P&W | Do Nothing | Do Nothing | Solo (+2.07) |
| Round 2, NGSA open, P&W announced | Joint Venture (+0.91) | Joint Venture | Joint Venture |
| Round 3, NGSA named, P&W announced | Joint Venture (+1.94) | Solo (+4.03) | Solo (+4.03) |
| Round 3, fps named | Joint Venture if P&W (+0.87), else Do Nothing | Same | Solo (+1.89) |
| Round 3, NGSA open, no P&W | Do Nothing | Do Nothing | Solo (+0.87) |
| A350 Re-engine announced | `uf_wb`, standard | `uf_wb`, standard | `uf_wb`; aggressive if the engine is left open or a rival is named |
| 787 Re-engine | `uf_wb` only if Boeing named UltraFan | Same | Same |
| GTF2 on aggressive terms in the narrowbody contest | Aggressive only by the company test | Same | Same |
| GEnx upgrade by CFM/GE | Our upgrade | Same | Same |
| Disclosure voice | "Opportunity isn't there just yet"; partnership [RX-0022, RX-0023] | "Not before 2030"; "We won't do anything not profitable" [RX-0058] | Conditional, binding, few: "until I am sure we will deliver, I'm not committing" [RX-0124] |

## Gaps
- **No team has made a narrowbody launch decision.** Everything on Solo against the Joint Venture is words [RX-0072, RX-0118, RX-0023]. No team gives a payback period, a partner or an UltraFan hurdle [RX-0058]. The team-specific bars (+$3B, above 0 in round 3) are inference.
- **Membership.**
  - The 2023 team is a composite: Kakoullis to August 2023, Watson from November 2023. The Civil president for February-August 2023 is not in the evidence.
  - The 2022 team's CEO is not profiled.
  - The 2026 team assumes seats held past mid-2025 (Erginbilgic, McCabe) and late 2023 (Watson).
- **How decisions are split.** No evidence shows how Kakoullis divided decisions with either CEO; the joint £25m sign-off is shown only for Erginbilgic and McCabe [RX-0213].
- **Rivals.** No member names CFM/GE or P&W as a rival engine maker in these turns. Reactions to the ducted engine, the open fan and the upgrades are inference from engine numbers and general stances.
- **Engine numbers** come from a scratch run, not evidence. Strain and `jv_pw` parameters are placeholders (rules).
- **Files still using the old id.** `erginbilgic.md` (header) and `operations.md` (Cholerton "in the 2022 and 2023 teams") still name `erginbilgic-kakoullis-cholerton-2023`, and so does `ENGINE_EXEC_SYNTH_ADDENDUM.md`.
