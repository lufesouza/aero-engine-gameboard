# The operating seat: Presidents of Civil Aerospace

The President of Civil Aerospace runs production, durability, services cost and the airline and airframer relationship. In the executive committee this seat tests production, quality and the supply chain. Three holders are profiled:
- Chris Cholerton, in the 2022 team (`east-kakoullis-cholerton-2022`) only;
- Rob Watson, in the 2023 team (`erginbilgic-kakoullis-watson-2023`) and the default 2026 team;
- Eric Schulz, as historical reference only.

**Evidence.** 70 own-words items (RX). 66 come from three Civil events (November 2016, May 2022 and November 2023); the other 4 are Cholerton's 2016 Defence turn (3) and Watson's 2021 Electrical turn (1).
- **Attribution.** Twelve items come from transcript turns labelled "Unknown Executive" and are marked here:
  - **(attr.)**: the speaker refers back to his own presentation, or the CEO hands the question to him by name;
  - **(prob.)**: probable only.
- **Other speakers.** Presentations by other Civil executives within these turns were not used.

**Confidence.** Low to medium overall. Each person rests on one or two events.

**Tag.** [5p] = engine snapshot, not evidence: `options` or `whatif` on a fresh `five-player-2045` run at turn 1, $B delta PV, re-checked 2026-10-04. Re-run every turn. In the commitment tables, † marks an outcome taken from the reader's note or numbers field of the cited item, not from its quote.

## Chris Cholerton: President, Civil Aerospace, 2018 to at least May 2022 (President, Defence Aerospace, in 2016)

**Era and evidence.** He took the Civil seat "at the start of 2018" and ran the widebody ramp and a productivity drive together [RX-0015]. That was during the Trent 1000 crisis, whose issues surfaced in late 2016-17 [R-1177] and grounded just under 50 aircraft at the peak in mid-2018 [R-1171]. COVID followed. He has 29 items: 3 from his 2016 Defence turn and 26 from the May 2022 Civil investor event. Eight of the 26 are (attr.) or (prob.).

**Quick card**
- **Objective function:**
  1. "sustainable cash generation and margin expansion" [RX-0016];
  2. the installed-base annuity, "about 90% of the services value" captured over an engine's life [RX-0017];
  3. services cost: engines that "last longer on wing" and cost less in the shop [RX-0014];
  4. "approach the returns enjoyed by our competitors" (attr.) [RX-0028].
- **Rules and red lines:**
  - "We're out of launch pricing phase" [RX-0018].
  - Win back 787 share without doing "anything silly ... on pricing" (prob.) [RX-0026].
  - Invest in demonstration "well ahead of a market need" but phase the main investment until the market is real (attr.) [RX-0024, RX-0025].
  - Partnership is the default structure (attr.) [RX-0023], to stay "capital-light" [RX-0004].
- **Risk:**
  - Technology Medium: proof is bought early (attr.) [RX-0024].
  - Schedule Low: phasing kept flexible (attr.) [RX-0025].
  - Pricing Low appetite for concessions [RX-0018; prob. RX-0026].
- **Tempo.** In his 2016 Defence role he waited for signals to convert "into policy and action" [RX-0002]. In the COVID crisis, "tough decisions at pace" [RX-0013].
- **Product.**
  - Powers 4 of 5 new widebodies, with 3 sole-source positions on Airbus [RX-0019].
  - The UltraFan demonstrator is "at the heart of our strategy for future widebody and indeed any future narrowbody opportunities" [RX-0020], and also feeds today's engines [RX-0021].
  - Narrowbody is an "ambition", but "the opportunity isn't there just yet" (attr.) [RX-0022].
- **How he reads airframers and rivals.** He treats Airbus sole sourcing as a strength [RX-0019]. He said RR's "reputation took a knock" on the 787 (prob.) [RX-0012]. He benchmarks against rivals' higher returns (attr.) [RX-0028].
- **Voice:**
  - "it's not the destination, it's the next step in the journey" [RX-0005]
  - "a ticket to the game" (attr.) [RX-0024]
  - "our pricing escalation is always at least as good as the cost escalation" [RX-0027]
- **Biases.**
  - Declares a problem closed once the customer disruption ends: "That disruption is now behind ... us" (May 2022) [RX-0006]. Aircraft on ground had reached zero [R-1239], but intense Trent 1000 check-and-repair was to run to the end of the medium-term plan (attr.) [RX-0282] and the new blade was certified only in June 2025 [R-1023].
  - Cost-led margin defence, as in his Defence role [RX-0001]; (inference) carried into Civil.
  - Traffic forecasts "like most market commentators", checked against RR's own fleet analysis [RX-0008].

**Commitments**

| Date | Commitment or forecast | Outcome in the evidence | ids |
|---|---|---|---|
| 2022-05 | Trent 1000 disruption "behind us"; permanent fixes being implemented | Aircraft on ground had reached zero by early 2021 [R-1239], so the disruption he named had ended. The durability work ran on: intense check-and-repair to the end of the medium-term plan (Watson, attr.) [RX-0282]; new HPT blade certified June 2025 [R-1023] | RX-0006 |
| 2022-05 | Pandemic cost cuts "substantially sustainable" as load returns | Not shown directly; Civil margin 2.5% (2022), 16.6% (2024) under the next leadership [R-0295] | RX-0007 |
| 2022-05 | Passenger flying hours back to 2019 in 2024 | Large-engine flying hours 15.8m in 2024 against 15.3m in 2019 [R-0245] | RX-0008 |
| 2022-05 | UltraFan opportunities "well into the 2030s" (widebody) and in the 2030s (narrowbody) (attr.) | Consistent with the CEO's 2023 rule of no commitment before an airframer launch, not before 2030 [R-1005] | RX-0009 |

**In the game**

| Lever | Default | Flips or vetoes |
|---|---|---|
| `uf_nb` | Do Nothing; demonstrate only (attr.) [RX-0022, RX-0025] | (inference) Flips on an announced fps or NGSA. Vetoes a Solo launch without a customer |
| Solo against Joint Venture | Joint Venture: "as we have in ... all our Trent programs actually in partnership" (attr.) [RX-0023] | Solo only if P&W has not announced its join and selection is certain (inference) |
| `uf_wb` | Launch in the turn Airbus announces an A350 Re-engine, to keep the sole-source positions [RX-0019] (inference) | Vetoes pre-launch |
| Terms | Standard [RX-0018, RX-0027] | Vetoes price-led share, even on the 787 (prob.) [RX-0026] |
| `t1000_upgrade` | Fund: services cost [RX-0014], 787 reputation (prob.) [RX-0012] | (inference) Defer if it overlaps an UltraFan development (strain) |
| `cancel` | Cancel an unselected programme but keep its technology for current engines (inference) [RX-0021] | - |

**Reactions.**
- **CFM/GE launches a ducted engine or the RISE open fan.** (inference) He keeps buying proof and phasing the spend (attr.) [RX-0025], with no launch until the opportunity is real: "depending on the actual reality of any market opportunity" (attr.) [RX-0009].
- **CFM/GE upgrades take share.** (inference) He answers with durability, not price (prob.) [RX-0026].
- **An airframer asks for aggressive terms.** (inference) He refuses, relying on escalation formulae [RX-0027].

**In the executive committee** (inference) he asks for cost-out, time on wing and phasing. What moves him is an airframe programme with a date (attr.) [RX-0009].

## Robert (Rob) Watson: President, Civil Aerospace, from 2023 (Director, Rolls-Royce Electrical, in 2021)

**Era and evidence.** He was Civil president by the November 2023 Capital Markets Day, presenting the CEO's plan to take Civil from a 2.5% margin [RX-0277]. He sits in the 2023 team and the default 2026 team. He has 27 items: 1 from June 2021, when he led Electrical, and 26 from 28 November 2023. Four of the 26 are (attr.): the CEO handed those questions to "Rob" [RX-0282, RX-0283, RX-0284, RX-0296].

**Quick card**
- **Objective function:**
  1. Civil margin from 2.5% to 15-17% by the midterm [RX-0277];
  2. "6 levers": keeping engines flying for longer, value-driven pricing, contractual rigour, shop visits, product costs and time on wing [RX-0288];
  3. "keeping our engines flying and earning for as long as possible" [RX-0289].
- **Rules and red lines:**
  - No engine into service before its technology is mature and tested (attr.) [RX-0296].
  - Programmes are paced, with a proper testing schedule (attr.) [RX-0284].
  - In-service support is built before entry into service (attr.) [RX-0283].
  - R&D goes to short-payback work with "government gearing" [RX-0273].
  - About 3% gross product cost out a year [RX-0274].
- **Risk:**
  - Technology Low-medium: UltraFan "can be considered" for widebody or narrowbody, with no launch named [RX-0294].
  - Schedule Low (attr.) [RX-0296, RX-0284].
  - Pricing: Low appetite for concessions; (inference) tolerates customer friction [RX-0298].
- **Tempo.** (inference) Executes inside the CEO's frame. On OE cost he cited progress, not a breakeven date [RX-0276].
- **Product.**
  - A 55% widebody OE delivery share in 2022, 36% of installed engines, sole source on 3 platforms [RX-0292].
  - Narrowbody only through the V2500 aftermarket "into the 2030s" [RX-0293].
  - UltraFan is 25% more efficient than the first Trent, and some of its technology goes into today's fleet [RX-0295].
- **How he reads airframers and rivals.**
  - Competitiveness is proven by airline wins: Air India, Air France, EVA, Egyptair, Ethiopian [RX-0297].
  - His Trent 1000 lesson is about RR's own maturity testing; he names no rival (attr.) [RX-0296].
- **Voice:**
  - "we're clearly aligned as one Rolls-Royce. We've got detailed granular plans" [RX-0275]
  - "win-win opportunities" [RX-0290]
  - "a value-driven pricing strategy" [RX-0291]
  - "By midterm, we'll have halved the cost of a Trent XWB shop visit" [RX-0281]
- **Biases.**
  - Maturity over timing (attr.) [RX-0296].
  - Installed base first [RX-0289].
  - He backs hard negotiations with customers [RX-0298].

**Commitments**

| Date | Commitment | Outcome in the evidence | ids |
|---|---|---|---|
| 2023-11 | Civil margin 15-17% by midterm | 16.6% (2024) [R-0295]; 24.9% in H1 2025 [R-0906] | RX-0277 |
| 2023-11 | OE deliveries 190 to 300-350 a year; major refurbishments about 250 to 700-750 | 278 widebody engines and 430† large refurbishments in 2024 [R-1295] | RX-0279 |
| 2023-11 | At least 40% better time on wing in the medium term (the reader's note on RX-0280 says a Civil services executive gave 40% by 2025 in May 2022) | The CEO raised the target to 80% in February 2025 [RX-0110] | RX-0280 |
| 2023-11 | Halve the Trent XWB shop-visit cost | Open | RX-0281 |
| 2023-11 | Trent 1000 intense check-and-repair to the end of the plan (attr.) | New HPT blade certified June 2025; a further build standard by end-2025 [R-1023, R-1306] | RX-0282 |

**In the game**

| Lever | Default | Flips or vetoes |
|---|---|---|
| `uf_nb` | Do Nothing; architecture "scalable" [RX-0294] | (inference) Flips on an announced fps or NGSA. Vetoes any disclosed entry into service earlier than launch plus development years (attr.) [RX-0296] |
| Solo against Joint Venture | No evidence. Leans to partnership (inference from the Singapore MRO Joint Venture [RX-0287]) | Solo PV beats the Joint Venture once selection is announced: NGSA 2031 +16.50 against +8.13 [5p] |
| `uf_wb` | Launch in the turn an A350 Re-engine is announced (inference): Trent XWB will be about 60% of the large fleet in 2027 [R-1279] | Vetoes pre-launch; an unselected 2031 launch costs -2.46 [5p] |
| Terms | Standard; trades coverage for better terms [RX-0290, RX-0291] | (inference) Vetoes concessions on new contracts [RX-0291] |
| `t1000_upgrade` | Strongly for: HP turbine blades on the Trent 1000 and 7000, longer-life parts [RX-0285]; +0.81 [5p] | (inference) Defer if it overlaps an UltraFan development |
| `cancel` | Cancel an unselected programme; keep the technology flowing to the fleet (inference) [RX-0295] | - |

**Reactions.**
- **CFM/GE launches the open fan.** It cannot enter service before 2045 (rules). He would stress RR's own maturity rather than race (inference; attr.) [RX-0296].
- **CFM/GE launches a GEnx upgrade.** It costs RR -0.58 and 10 widebody engines a year; with RR's upgrade the net is +0.23 [5p]. (inference) He answers with time on wing [RX-0285].
- **An airframer asks for aggressive terms.** (inference) He backs his teams in hard negotiations, as he does with airline customers [RX-0298].

**In the executive committee.** He tests production, MRO and supplier capacity [RX-0279, RX-0287, RX-0286], (inference) asks for strain, and keeps a "granular plan" [RX-0275]. What changes his mind: test maturity (attr.) [RX-0296] and named customer wins [RX-0297].

## Eric Schulz: President, Civil Aerospace, 2016

**Era and evidence.** He has 14 items from a single event, the 16 November 2016 investor day. The transcript prints his title as "Former President". This was the widebody production ramp, with Trent-powered 777s and A330s being parked and moved between operators [RX-0146, RX-0151]. Cholerton took the seat at the start of 2018 [RX-0015]. Confidence is low. No team uses him; he is a "what if a share-led president ran Civil" reference.

**Quick card**
- **Objective function:**
  1. Capacity: about 20% growth a year to a peak of about 600 large engines a year [RX-0147];
  2. share: "beaten GE by 2020" [RX-0143];
  3. keep Trent aircraft flying through transitions [RX-0146];
  4. an MRO network for a fleet doubling within ten years [RX-0149].
- **Rules:**
  - Airframers now require "demonstration of technology ... You need to show products" [RX-0152].
  - "only one pilot in command" [RX-0153].
- **Risk:**
  - Schedule and engineering load High: "3 programs in parallel ... unprecedented in Rolls-Royce" [RX-0150].
  - Concession appetite: no evidence.
- **Tempo.** Watchful: "We don't know yet, but we are watching this" [RX-0145].
- **How he reads rivals.** "I rather prefer to see a Pratt or GE aircraft being parked as compared to mine" [RX-0151].
- **Voice:** "We sell fuel burn" [R-0955]; "it doesn't mean that we are anxious about the future of the market" [RX-0140].
- **Biases.** Share-led targets [RX-0143] (the outcome is not in the evidence). Customer reactivity as the test of a crisis [RX-0144].

**Commitments**

| Date | Commitment or forecast | Outcome in the evidence | ids |
|---|---|---|---|
| 2016-11 | About 50% widebody share within 3-4 years | Share in 2019-20 is not in the evidence. 55% of OE deliveries in 2022 but 36% of installed engines [R-0365]; over 60% of deliveries in 2024 [RX-0262] | RX-0141 |
| 2016-11 | "Beaten GE by 2020" in share and deliveries | Not shown in the evidence | RX-0143 |
| 2016-11 | UltraFan "preparing the 2025 deliveries" | "Well into the 2030s" by 2022 (attr.) [RX-0009] | RX-0142 |
| 2016-11 | 20% a year to a peak of about 600 large engines | 357 (2016), 483 (2017), peak 510 (2019) [R-0226]; 190 in 2022 [R-0245] | RX-0147 |
| 2016-11 | Civil overhead cut by more than 20% while growing | Stated as done | RX-0148 |

The 2017 ramp was real (+35%) [R-0226]. The Trent 1000 durability problems surfaced in late 2016-17 [R-1177], during his three-programme load. The evidence does not show that concurrency caused them; RR later tied them to pushing performance past durability limits [R-1436].

**In the game (historical what-if).**
- He would push `uf_wb` and `uf_nb` to win share, and accept overlapping developments [RX-0150, RX-0143] (inference). That runs against today's red line on concurrency.
- He would fund `t1000_upgrade`: "addressing the in-fleet issues is absolutely key" [R-1421].
- He has no stated terms stance.
- (inference) He meets a CFM/GE launch head on [RX-0151].

## What the seat stands for

**From share to margin.** Schulz in 2016 measured himself against GE on share and volume [RX-0143, RX-0147]. Cholerton in 2022 put cash and margin first [RX-0016], and Watson in 2023 named "margin" as the target [RX-0277].

**Constants across all three:**
- the widebody sole-source franchise [RX-0019, RX-0292];
- demonstrate before launch [RX-0152, RX-0294; attr. RX-0024];
- MRO capacity as a constraint [RX-0149, RX-0287];
- durability as the main operating lever [RX-0014, RX-0285].

**How the seat sharpens the company doctrine:**
1. **Maturity is an operating red line.** Watson's Trent 1000 lessons are to mature and test before entry into service, and to have support in place first (attr.) [RX-0296, RX-0283]. In the game: never disclose an entry into service earlier than launch plus development years.
2. **The seat counts engineering load.** Schulz ran three programmes at once [RX-0150]. Cholerton moved engineers to maturity and cost reduction [RX-0004]. In the game: ask for strain before any second UltraFan or an overlapping `t1000_upgrade`. Both UltraFans launched in 2031 cost -9.35, including -1.19 of strain [5p].
3. **Partnership is the default structure** (attr.) [RX-0023], even for MRO [RX-0287].
4. **No price-led share** [RX-0298; prob. RX-0026]. The seat negotiates scope for terms instead [RX-0290].

**In the executive committee.** After the CEO frames and the CFO tests cash, this seat tests:
- production and MRO capacity;
- supplier concentration [RX-0286];
- durability risk;
- strain.

(inference) It can veto a compressed schedule. It pushes `t1000_upgrade` whenever no UltraFan development overlaps it.

## Gaps

- **Coverage.** Only three Civil events, in 2016, 2022 and 2023. Nothing from 2017-21, so this seat gives no first-hand account of the Trent 1000 crisis or of COVID as they happened.
- **Attribution.** Twelve items rest on attributed "Unknown Executive" turns, two of them only probable [RX-0012, RX-0026].
- **Narrowbody.** No holder speaks on a Joint Venture with Pratt & Whitney or a Solo narrowbody engine; those rows are inference.
- **Outcomes not shown:**
  - Cholerton's cost-sustainability claim [RX-0007];
  - the time-on-wing and XWB shop-visit targets [RX-0280, RX-0281];
  - Schulz's "beat GE" [RX-0143].
- **Definitions.** At the same 2023 event, Watson gave total shop visits of 1,100-1,200 [RX-0279] and McCabe 1,400-1,500 [RX-0223]. The definitions are not reconciled in the evidence.
- **Tenure.** Exact dates are not in the evidence. Cholerton's last item is 13 May 2022 [RX-0004]; Watson is first printed as Civil president on 28 November 2023 [RX-0277]. Who held the seat between those dates is not in the evidence: the 2023 team assumes Watson, and the 2026 default team assumes he still holds the seat.
