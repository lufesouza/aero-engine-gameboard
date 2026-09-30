# Boeing profile: citation audit

Audit date 2026-09-30. It checks every cited claim in the Quick card, §5, §6 (with the resolved tensions) and §9 of `profile.md`, every row of `reaction_function.json`, and every number in the Quick card and `financials.md`. Line numbers refer to `profile.md` **before** the fixes.

## Method

- `audit/extract.py` splits each section into claim units, one per bracketed citation group, one per §5 table row and one per JSON row. It prints each claim next to the cited items' date, speaker, quote and finding. `audit/search.py` searched `evidence.jsonl` for replacement items.
- A claim counts as **SUPPORTED** when the cited quotes say it, **WEAK** when they are related but do not establish it, and **UNSUPPORTED** when they do not say it or the evidence contradicts it. A claim can be SUPPORTED while one of its ids is off-point. Those ids are shown in **bold** and listed as weak pairs.
- Claims labelled [NOW] must cite items dated 2024-25.
- `audit/check_fin.py` compares every §1-§8 table cell in `financials.md` with the same-header table in `evidence/fin_boeing.md`. It also checks every number in the prose, and every §9 value against the cited `tkN.financials.md`. `audit/check_pages.py` checks that each §9 value appears on the same source line as its cited page. The checker was mutation-tested: four injected errors were all caught.
- `[RULES]` was checked against `python3 -m wargame.engine rules`. The `[ENGINE]` landmarks were re-run with `whatif` in a scratch run (base scenario, no injects).

## Summary

| Scope | Claims | Supported | Weak | Unsupported | Claim-id pairs | Weak or unsupported pairs |
|---|---|---|---|---|---|---|
| Quick card | 23 | 15 | 8 | 0 | 46 | 9 |
| §5 | 16 | 15 | 1 | 0 | 84 | 2 |
| §6 | 30 | 24 | 5 | 1 | 43 | 3 |
| §9 (no ids; 6 quoted phrases checked instead) | 6 phrases | 5 | 0 | 1 | – | – |
| reaction_function.json | 16 | 16 | 0 | 0 | 152 | 1 |
| **Total (cited claims)** | **85** | **70** | **14** | **1** | **325** | **15** |

Financial, RULES and ENGINE numbers are counted separately under Numbers: 1,545 financial numbers and 28 RULES/ENGINE numbers, with no mismatches.

## Claim-by-claim table

Bold ids are the off-point citations. Every change listed has been applied to `profile.md` or `reaction_function.json`.

| # | Where (original line) | Claim | Cited ids | Verdict | Problem and fix |
|---|---|---|---|---|---|
| 1 | Quick card L13 | 1. Stable, safe production, gated on KPIs and supervised by the FAA | B-2221, B-2236, B-2297 | SUPPORTED | – |
| 2 | Quick card L14 | 2. Balance sheet: pay debt down to "solidly investment grade" | B-2327, B-2186 | SUPPORTED | – |
| 3 | Quick card L15 | 3. Free cash flow, driven by the 737 rate | B-2298, B-2314 | SUPPORTED | – |
| 4 | Quick card L16 | 4. Finish the 737-7, 737-10 and 777X | B-2276 | SUPPORTED | – |
| 5 | Quick card L17 | 5. Hold the narrowbody franchise, but not at any price | **B-1936**, **B-1980** | WEAK | Content right but both items are 2022 (Calhoun) under a [NOW] label. Swapped for 2024-25 items: B-2179 (competes campaign by campaign), B-2537 (tracks deliveries vs Airbus), B-2331 (prices for scarcity, not share). |
| 6 | Quick card L18 | 6. A new airplane (fps) once market, money and technology converge | B-2303, B-2316 | SUPPORTED | – |
| 7 | Quick card L19 | 7. Shareholder returns: off | **B-2037** | WEAK | 2023 item under a [NOW] label. Swapped for B-2259 (FY2024 10-K: no common dividends 2022-24) and B-2327 (2025: debt is the priority). |
| 8 | Quick card L22 | H1. No fps order in Turn 1 | B-2276, B-2313, B-2327 | SUPPORTED | Added B-2316 ("not today and probably not tomorrow"). |
| 9 | Quick card L23 | Sole exception: the Turn-1 brief already shows NGSA launched, and whatif (nominal or slip test) shows the exce… | **B-0422** | WEAK | B-0422 supports moving when share is at risk, not a 2028 Joint Venture. Exception labelled (inference); B-0422 kept as context. Noted in §10. |
| 10 | Quick card L25 | H2. fps launch year = max(first year of the turn, tech_ready_year − dev_years (7) − engine eis_add). Never pla… | B-2061, B-2164 | SUPPORTED | – |
| 11 | Quick card L26 | H3. No 787 Re-engine in Turn 1, and none at all once Airbus has launched the A350 Re-engine | B-2276, **B-0917** | WEAK | B-2276 supports 'none in Turn 1'. No item supports 'none ever once the A350 Re-engine launches'; B-0917 is the A330neo case, where Boeing held the newer airplane. Second half relabelled (inference), with the engine as its basis; B-0858 added as the precedent. Noted in §10. |
| 12 | Quick card L27 | H4. One major development at a time. A Solo fps and the 787 Re-engine may overlap for at most 2 years; a longe… | B-0341, B-1526 | WEAK | B-0341 and B-1526 support one development at a time. Nothing supports the 2-year overlap cap or the Joint Venture exception. Added B-1393 ('feather in'); the limits are relabelled (inference, from the engine's strain rule). Noted in §10. |
| 13 | Quick card L28 | H5. Never cancel a launched fps or 787 Re-engine because of slips, charges, a supplier bottleneck or Airbus en… | B-1812, B-2244, **B-2203** | SUPPORTED | B-2203 is about defence contracts, not an airplane program. Swapped for B-0192 (747-8 kept despite >$1B of charges). |
| 14 | Quick card L29 | H6. No Rate Increase as a response to Airbus, or in a turn with a live quality-escape, FAA-scrutiny or supply-… | B-1802, B-2148, B-2308 | SUPPORTED | – |
| 15 | Quick card L30 | H7. No fps launch while a Boeing crisis inject is live (quality escape, FAA certification scrutiny), unless NG… | B-1593, **B-0422** | WEAK | B-1593 supports 'no launch in a crisis'. Nothing supports the Joint Venture exception. Added B-1613 (NMA shelved in the crisis); exception labelled (inference). Noted in §10. |
| 16 | Quick card L43 | NGSA in development: fps no later than the next turn; this turn say "doesn't change our plans" (1 turn) | B-0413, B-1308 | SUPPORTED | – |
| 17 | Quick card L44 | A350 Re-engine launched: no 787 Re-engine, ever (same turn) | **B-0917**, **B-0921** | WEAK | Precedent shows no product against the A330neo; 'ever' comes from the engine. Labelled (inference), pointing to H3. |
| 18 | Quick card L45 | fps "supplier bottleneck": continue, re-baseline once, and launch no overlapping Re-engine (same turn) | B-2097, B-2342 | SUPPORTED | – |
| 19 | Quick card L46 | Delay Tactics exposed, or trade action: a level-playing-field complaint only (same turn) | B-1339, B-0174 | SUPPORTED | – |
| 20 | Quick card L47 | Poaching: absorb it; hire and redeploy | B-1941, B-0729 | SUPPORTED | – |
| 21 | Quick card L48 | Quality escape or FAA scrutiny: no Rate Increase; apply H7 (this turn) | B-2148, B-2133 | SUPPORTED | – |
| 22 | Quick card L49 | Demand shock: keep the plan | B-2287 | SUPPORTED | Added B-2292 (kept the rate plan because others would absorb China's ~10% of the backlog). |
| 23 | Quick card L50 | Airbus rate, price or variant moves: no order change | B-1802, B-2063 | WEAK | Rate (B-1802) and variant (B-2063) covered; nothing cited for price. Added B-1868 (does not react to single campaign losses). |
| 24 | §5 L197 | Row 1: Launches a new narrowbody (NGSA in development) → Said "the market will wait", then reversed to a fast, date-certain ans | B-0291, B-0331, B-0413, B-0419, B-0422, B-0423, B-0521, B-0733, B-0804 | SUPPORTED | – |
| 25 | §5 L198 | Row 2: Signals NGSA without launching it → [NOW] Sets no dates; "market not ready"; gates are internal | B-2313, B-2315, B-2316, B-2536 | SUPPORTED | – |
| 26 | §5 L199 | Row 3: Re-engines a widebody → Launched no product. Stressed the 787's value; declined a 767 re-engin | B-0847, B-0858, B-0917, B-0921, B-2446 | SUPPORTED | – |
| 27 | §5 L200 | Row 4: Launches a new widebody → Waited until it was "real", then bracketed it with derivatives | B-0029, B-0524, B-0764, B-0860 | SUPPORTED | – |
| 28 | §5 L201 | Row 5: Leaves the widebody uncontested → Took share and price where Airbus had no answer | B-0342, B-0979, B-1036, B-2424, **B-0634** | SUPPORTED | B-0634 (most efficient in every segment) does not show taking share or price. Swapped for B-0555 (held strong 777 pricing with no A340/A350-1000 rival). |
| 29 | §5 L202 | Row 6: Stretches or adds a variant → Minimum-capex answers (MAX 10) or none; "no niche" | B-1271, B-1738, B-1814, B-2063, B-2070 | SUPPORTED | – |
| 30 | §5 L203 | Row 7: Raises production rates → Never matched; kept its own gates | **B-0186**, B-1034, B-1428, B-1802, B-2046 | SUPPORTED | B-0186 is about an over-ordered backlog; it mentions neither Airbus nor rates. Swapped for B-0070 (2008: set its own tests for a rate above 31 instead of matching Airbus). |
| 31 | §5 L204 | Row 8: Prices aggressively or wins campaigns → Matched in must-win campaigns and funded it with productivity; walked  | B-0353, B-0592, B-0840, B-0961, B-1868 | SUPPORTED | Added B-0818 (no price war that impairs economics) for 'walked away from ruinous deals'. |
| 32 | §5 L205 | Row 9: Acquires or partners → Said "doesn't change our plans", then partnered, holding control. Exit | B-1308, B-1317, B-1326, B-1492, B-1674 | WEAK | Lag '~3 months to partner' is not in the evidence: talks came ~2 months after the CSeries deal (B-1317) and the MoU ~9 months after (B-1493). Rewritten: '~2 months to open partner talks'. |
| 33 | §5 L206 | Row 10: Stumbles (slip, cancellation) → Took the pricing gain; did not accelerate | B-2424, B-0546, B-1036, B-1529 | SUPPORTED | – |
| 34 | §5 L207 | Row 11: (Shock) narrowbody demand → [HIST] Held narrowbody rates and cut widebodies; reversed within a yea | B-0659, B-0250, B-0318, B-1684, B-2287, B-2294 | SUPPORTED | – |
| 35 | §5 L208 | Row 12: (Shock) supply chain or engines; unattributed fps slip → Never blamed Airbus. Embedded staff, used buffers and second sources,  | B-1923, B-2097, B-2038, B-1303, B-2184, B-1597, B-2243 | SUPPORTED | – |
| 36 | §5 L209 | Row 13: Trade or regulatory action, or exposed unfair conduct → GAO protest 11 days after losing the tanker; WTO cases; trade case aga | B-0174, B-2379, B-1339, B-2509, B-2290 | SUPPORTED | – |
| 37 | §5 L210 | Row 14: Poaches talent → No Airbus precedent. Answered engineering scarcity with transfers, mas | B-0729, B-1941, B-1376, B-1835 | SUPPORTED | – |
| 38 | §5 L211 | Row 15: (Boeing's own crisis) quality escape or FAA action → Froze the rate; stood the line down; took no new program | B-2133, B-2148, B-2136, B-2103, B-2354, B-1593, B-1613 | SUPPORTED | – |
| 39 | §5 L212 | Row 16: Does nothing → No rush; execution first | B-1902, B-2205, B-2218, B-2305 | SUPPORTED | – |
| 40 | §6 L239 | Default: 2029, the first year of Turn 2, whether or not NGSA has launched. The gates set the timing, not Airbu… | B-2313 | SUPPORTED | Added B-2315 (asked about Airbus's NGSA timing, no date). |
| 41 | §6 L241 | Later: under H7; or under an engine-maturity-slip inject, per H2 (2030 if tech_ready_year becomes 2037) | **B-2304** | WEAK | B-2304 shows caution about engine durability, not that launch timing follows technology maturity. Added B-2061 ('not before 35' because the technology will not be mature). |
| 42 | §6 L246 | the pendulum points to control | B-2195, B-0956 | SUPPORTED | – |
| 43 | §6 L247 | the Embraer exit and arbitration | B-1674, B-2131 | SUPPORTED | – |
| 44 | §6 L266 | Precedent: Embraer was sought for capacity and talent once Airbus had consolidated | B-1326, B-1567 | SUPPORTED | – |
| 45 | §6 L266 | partner-funded development | B-0024 | SUPPORTED | – |
| 46 | §6 L268 | fps engine. Default `cfm_ducted` | B-0613, B-2304 | SUPPORTED | – |
| 47 | §6 L269 | `pw_gtf2` scores +0.4 to +0.8, within ε, so doctrine keeps CFM | B-0600 | SUPPORTED | – |
| 48 | §6 L272 | 787 Re-engine. None in Turn 1 (H3): the 777X comes first | B-2276 | SUPPORTED | – |
| 49 | §6 L276 | Otherwise Do Nothing on the widebody; the 787 already aims to be the most efficient in its segment | B-0634, B-0934 | SUPPORTED | – |
| 50 | §6 L277 | Engine: `ge_genx_next`. Rolls-Royce scores +0.4, within ε. GE is the 777X's sole source | B-0747 | SUPPORTED | – |
| 51 | §6 L277 | and Rolls-Royce once threatened the 787's schedule | B-0288 | SUPPORTED | – |
| 52 | §6 L279 | Rate Increase. Commit in Turn 1: it is the cheapest FCF lever | B-2298, B-0164 | WEAK | The evidence says the 737 rate is the main cash driver; 'cheapest lever' is not in it. Rewritten: 'the 737 rate is the main FCF driver'. |
| 53 | §6 L279 | and the ladder is already planned | B-2287 | SUPPORTED | – |
| 54 | §6 L280 | Defer it to the first clean turn under a quality, FAA or supply-crunch inject | B-2148, B-2308 | SUPPORTED | – |
| 55 | §6 L284 | The only exit is the McNerney test: remaining revenue must outweigh remaining cost, with a competitive edge | B-0153 | SUPPORTED | – |
| 56 | §6 L285 | Legacy lines end when demand ends | **B-2245** | WEAK | B-2245 records the end of the 767 freighter but gives no reason. Added B-1031 (end while demand still slightly exceeds airplanes) and B-1236 (747 may end without orders); wording now 'once demand runs out'. |
| 57 | §6 L290 | Orders are sealed at the start of 2026, before the 777X and MAX 7/10 gates close | B-2276, B-2352, B-2353 | SUPPORTED | – |
| 58 | §6 L290 | and before debt is repaired | B-2327 | SUPPORTED | – |
| 59 | §6 L290 | and Ortberg sets no dates | B-2313, B-2221 | SUPPORTED | – |
| 60 | §6 L291 | 2028 is the funding floor and the engine's PV-best year (EIS 2035). It is reachable only through the H1 except… | B-0733, B-0804 | WEAK | B-0733 and B-0804 show Boeing paid a lateness cost in 2011, not that it chose to pay it 'knowingly'. Rewritten to what they show. |
| 61 | §6 L292 | Calhoun's "not this decade" | B-1977 | UNSUPPORTED | The quote is right, but the claim 'it was not restated after 2022' is contradicted by B-2034 (CFO, Mar 2023: 'next decade ... we've been consistent'). Rewritten: echoed in 2023 [B-2034], not restated by Ortberg [B-2313]; still set aside (inference). |
| 62 | §6 L296 | 3. Sequencing the 787 Re-engine and fps. The finance draft said "Re-engine first"; the historical rule was "wi… | B-0802 | SUPPORTED | – |
| 63 | §6 L297 | Current priorities are the single-aisle and finishing the 777X | B-2276, B-2316 | SUPPORTED | – |
| 64 | §6 L302 | A demand shock no longer does. That was the 2009 behaviour | B-0250 | SUPPORTED | – |
| 65 | §6 L302 | in 2025 the ladder held | B-2287 | SUPPORTED | – |
| 66 | §6 L303 | 5. Poaching as a reason for the Joint Venture. The drafts inferred it from Embraer's engineers | B-1420 | SUPPORTED | – |
| 67 | §6 L304 | 6. Deferring fps when Airbus stumbles. A draft row said to defer one turn | B-0546 | SUPPORTED | – |
| 68 | §6 L305 | 7. A crisis in the launch turn. The drafts said "no launch in a crisis" vs "launch the turn after NGSA". H7 re… | B-1593, B-1613 | SUPPORTED | – |
| 69 | §6 L305 | unless NGSA is in development | **B-0422** | WEAK | Already labelled (inference) in the text; no change. |
| 70 | reaction_function.json row 1 | Row 1: Airbus launches a new narrowbody: NGSA appears in the event log as launched or i | B-0291, B-0303, B-0331, B-0413, B-0419, B-0422, B-0423, B-0450, B-0521, B-0733, B-0803, B-0804 | SUPPORTED | Translation: H1 exception marked (inference). |
| 71 | reaction_function.json row 2 | Row 2: Airbus signals a next-generation single-aisle (statements, engine studies) but h | B-2313, B-2315, B-2316, B-2303, B-2327, B-2325, B-2276, B-2536, B-0524 | SUPPORTED | – |
| 72 | reaction_function.json row 3 | Row 3: Airbus re-engines a widebody (the game's A350 Re-engine; analogue A330neo 2014) | B-0847, B-0858, B-0917, B-0920, B-0921, B-1017, B-2446, B-1812 | SUPPORTED | The response is supported. Translation: 'no 787 Re-engine for the rest of the game' is now marked as inference from the engine, not precedent. |
| 73 | reaction_function.json row 4 | Row 4: Airbus launches or redesigns a widebody (A350 XWB, A350-1000) | B-0010, B-0029, B-0067, B-0279, B-0524, B-0546, B-0764, B-0789, B-0860 | SUPPORTED | – |
| 74 | reaction_function.json row 5 | Row 5: Airbus leaves the widebody uncontested (no A350 Re-engine) | B-0342, B-0979, B-1036, B-2424, B-0634, B-0934, B-0919, B-1323 | SUPPORTED | – |
| 75 | reaction_function.json row 6 | Row 6: Airbus stretches or adds a variant (A321neo, LR, XLR, A220-500) | B-0593, B-0931, B-1153, B-1271, B-1401, B-1738, B-1814, B-2063, B-2070, B-1938 | SUPPORTED | – |
| 76 | reaction_function.json row 7 | Row 7: Airbus announces higher production rates | B-0070, **B-0186**, B-1034, B-1054, B-1428, B-1442, B-1802, B-1804, B-2046, B-2351 | SUPPORTED | B-0186 is off-point (see §5 row 7); removed, since B-0070 already covers 2008. |
| 77 | reaction_function.json row 8 | Row 8: Airbus prices aggressively or wins head-to-head campaigns | B-0353, B-0414, B-0592, B-0604, B-0654, B-0840, B-0951, B-1024, B-0818, B-0961, B-1868 | SUPPORTED | – |
| 78 | reaction_function.json row 9 | Row 9: Airbus acquires or partners (CSeries/A220 in 2017) | B-1308, B-1317, B-1318, B-1326, B-1381, B-1492, B-1493, B-1674, B-1666 | SUPPORTED | – |
| 79 | reaction_function.json row 10 | Row 10: Airbus stumbles: NGSA or the A350 Re-engine slips or is cancelled | B-2424, B-0546, B-0555, B-1036, B-1529 | SUPPORTED | – |
| 80 | reaction_function.json row 11 | Row 11: Narrowbody demand shock (inject; analogues 2008-09, COVID, 2025 China tariffs) | B-0156, B-0659, B-0250, B-0318, B-1671, B-1684, B-2287, B-2294 | SUPPORTED | – |
| 81 | reaction_function.json row 12 | Row 12: Supply-chain or engine problem: supply-chain-crunch or engine-maturity-slip inje | B-0495, B-0587, B-1923, B-2029, B-2097, B-2038, B-2043, B-1303, B-2184, B-2273, B-2243, B-1812, B-1710, B-0216, B-1597, B-2304, B-2061, B-2174, B-2264 | SUPPORTED | – |
| 82 | reaction_function.json row 13 | Row 13: Trade or regulatory action by or against Airbus (trade-dispute inject; Delay Tac | B-0077, B-0174, B-0578, B-2379, B-1418, B-1339, B-1077, B-2509, B-2290, B-2289 | SUPPORTED | Strength field is 'strong' while §5 says strong [HIST] / weak [NOW]. Left as is because the field is an enum and the translation already limits the response to statements. |
| 83 | reaction_function.json row 14 | Row 14: Talent pressure (the game's Poaching; there is no Airbus poaching episode in the | B-0729, B-0846, B-1941, B-1376, B-1835, B-0091, B-0248 | SUPPORTED | – |
| 84 | reaction_function.json row 15 | Row 15: Boeing's own crisis: quality-escape or FAA-certification-scrutiny inject | B-2133, B-2148, B-2136, B-2103, B-2236, B-2354, B-1593, B-1613, B-1658, B-2325 | SUPPORTED | Translation: Joint Venture exception marked (inference). |
| 85 | reaction_function.json row 16 | Row 16: Airbus does nothing | B-1902, B-1750, B-2205, B-2218, B-2276, B-2305, B-2303 | SUPPORTED | – |

## §9 quoted phrases (no ids before the audit)

| Phrase | Found in evidence? | Action |
|---|---|---|
| "stability" | Yes, 56 quotes (e.g. B-2218, B-2233) | Kept |
| "KPIs" | Yes: B-2221, B-2234 | Kept; cited B-2221 |
| "when the market, technology and our balance sheet converge" | Paraphrase of B-2316 ("when those 3 work streams all kind of converge") | Kept; marked as a paraphrase with the cite |
| "20-30% better" | Close: B-2164 "20% to 30% more efficient", B-1938 | Replaced with the verbatim B-2164 wording |
| "one conservative reset" | **No.** No quote contains "reset"; it paraphrases the finding of B-2342 | **UNSUPPORTED as a quotation.** Replaced with Ortberg's words "stop this quarterly drumbeat" of cost growth [B-2233] |
| "doesn't change our plans" | Yes: B-1308 "don't change our plans" | Kept; cited B-1308 |

## Dates of claims labelled [NOW] (current, 2024-25)

- Quick card "Ranked objectives [NOW]": items 5 and 7 cited 2022-23 items. Both were fixed (rows 5 and 7 above). Items 1-4 and 6 cite items dated 2024-25.
- The [NOW] statements in §5 rows 2, 11 and 13 and in JSON rows 2, 11, 13 and 15 rest on items dated 2024-25 (B-2313/15/16, B-2536, B-2287, B-2294, B-2290, B-2289; B-2103, B-2133 and B-2136 are January 2024). The older ids in the same lists support the [HIST] halves or the translation (e.g. B-0524 in JSON row 2).

## Numbers

| Check | Numbers checked | Result |
|---|---|---|
| `financials.md` §1-§8 table cells vs `fin_boeing.md` (same header, same row key) | 1,378 | All match |
| `financials.md` §1-§8 prose numbers vs `fin_boeing.md` | 55 | All present |
| `financials.md` §9 values vs cited `tk1-4.financials.md` | 112 | All present |
| `financials.md` §9 value on the same source line as the cited page | 139 value-page pairs | All consistent. Ten script flags were multi-source rows, where each value sits on the line of its own source (e.g. 3,706 is tk4 p.2501; $15.9bn is tk1 p80) |
| Quick card `[RULES]`: 4 turns 2026-28 … 2035-37, fps dev_years 7, fps capex $30B, Joint Venture partner share 35%, Poaching $0.75B a turn, "supplier bottleneck (cause not attributed)" | 6 | All match `rules` |
| Quick card `[ENGINE]`: H1 cost "about $2.1-2.4B" | 1 | Reproduced: Solo 2028 vs 2029 = 2.12 (NGSA 2026) to 2.35 (idle, NGSA 2029/2032) |
| §5/§6 `[ENGINE]` landmarks (spot-check): $5.5B follow cost (-7.50 vs -1.97); T4 -6.21 vs -4.28; Solo-JV table (all 7 cells, slip column included); pw_gtf2 +0.4-0.8; open fan and UltraFan -3.5 to -4.5; 787 Re-engine +1.03 (2034) and +2.96 (2030); RR +0.4; Rate Increase -0.08, +0.8-0.9 with fps, and timing across T1-T3 moving it by at most 0.3; T1 Re-engine -1.2; T2→T3 deferral 4.6-5.8; cancel -14.1 vs continue -4.6; 2030 launch a further ~$2B | 21 | All reproduced. Some hold only under an unstated Airbus plan or with no Rate Increase: the cancel test is NGSA 2029 with Delay Tactics in T2-T3; -6.21/-4.28, -7.50/-1.97, +2.96 and -1.2 assume no Rate Increase |

The ε ($1B) tolerance and the $2B cap are doctrine choices, not rules. They are already labelled (inference) in H8 and §10.

## Observations left unchanged (outside a citation fix)

- The `financials.md` decision summary says "A Solo fps overlapping a 787 Re-engine would exceed the norm". By its own tables, a Solo fps alone also does. Adding $4.29B a year to MS 2029E R&D of 4,692 on revenue of 117,045 gives about 7.7% of revenue, above the 5.69% ceiling. That holds if all of the game's $30B were R&D, but part of it is likely capex. This is a doctrine question, not a citation error.
- `profile.md` §8 B1 also quotes "one conservative reset" [B-2342] as if it were Boeing's words. §8 is outside this audit's scope, so it was left for the owner.
- JSON row 13 strength: see row 82 above.
