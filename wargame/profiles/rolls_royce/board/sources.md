# Rolls-Royce Holdings plc Board: sources (`rolls-royce-board`)

Sources for the board profile of Rolls-Royce Holdings plc (`board.md`) and its evidence file (`evidence.jsonl`,
RG-0001 to RG-0046). Research date: 2026-10-10.

## 1. Web sources: none

**No web item could be recorded.** The WebSearch tool was loaded, but every query was refused: the web-search budget for
this turn (200 searches, shared by every agent running in it) was already used up when this profile started. The tool
said not to work around the limit, so no page was fetched or searched by any other route.

- Web items in `evidence.jsonl`: **0**. Corroborated web items: **0**.
- Consequence: composition is dated to the latest repo source (the Form F-6 signature page of 8 July 2022, RG-0001),
  not to 2025-2026. Matters reserved to the board, pay-plan metrics and the UK government's position as a shareholder
  rest on transcript evidence or are marked (inference) in `board.md`.
- To fill the gaps, re-run the queries below in a session with search budget (the user can raise
  `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` or continue in a follow-up message).

### Queries attempted (all refused, 2026-10-10)

| # | Query | Result |
|---|---|---|
| 1 | Rolls-Royce Holdings plc board of directors 2026 chair Anita Frew senior independent director | refused: turn search budget used up |
| 2 | Rolls-Royce annual report 2025 board committees Safety and Sustainability Committee Science and Technology Committee members | refused: turn search budget used up |
| 3 | Rolls-Royce Holdings matters reserved for the board document | refused: turn search budget used up |

### Verification pass (2026-10-10)

The verifier tried one fresh query, "Rolls-Royce Holdings board of directors chair 2026"; it was refused for the same
reason (turn search budget used up). No web item was checked, added or dropped. Composition therefore stays dated
8 July 2022; whether Anita Frew still chairs and who the Senior Independent Director is in 2025-2026 remain open.

### Queries planned but not run (the research plan for a follow-up)

| Area | Query |
|---|---|
| Composition | Rolls-Royce board changes 2025 2026 new non-executive director appointment |
| Composition | Rolls-Royce chair succession Anita Frew successor announcement |
| Governance | Rolls-Royce schedule of matters reserved to the board threshold delegated authorities |
| Shareholders | Rolls-Royce UK government special share foreign shareholding limit articles of association |
| Shareholders | Rolls-Royce largest shareholders 2025 register |
| Pay horizon | Rolls-Royce directors' remuneration policy 2024 performance share plan metrics free cash flow holding period |
| Pay horizon | Erginbilgic pay award 2025 long-term incentive vesting |
| Culture | Rolls-Royce principal risks risk appetite annual report 2025 |
| Culture | Rolls-Royce Trent 1000 board safety review oversight |
| Decisions | Rolls-Royce board appoints Tufan Erginbilgic chief executive 2022 announcement |
| Decisions | Rolls-Royce share buyback 2026 announcement board authorises |
| Decisions | Rolls-Royce UltraFan narrowbody investment decision board 2025 |
| Decisions | Rolls-Royce SMR investment approval board |

## 2. Repo sources used (verbatim, machine-checked)

All 46 items pass `wargame/profiles/build/verify_quotes.py` (46/46, 2026-10-10; re-run 46/46 at verification after RG-0030's quote was extended).

| Source key | Document | Pages cited | Items |
|---|---|---|---|
| `rr_sec` | Rolls-Royce Holdings plc Form F-6 (ADR programme), signature pages, 8 July 2022 and 2 February 2021 | 75, 54 | RG-0001, RG-0002 |
| `rr_transcripts` | FH1 2011 Earnings Call (2011-07-28) | 1221 | RG-0013 |
| `rr_transcripts` | Shareholder/Analyst Call, 2014 investor day (2014-06-19) | 1028, 1035 | RG-0045, RG-0036 |
| `rr_transcripts` | Guidance/Update Call (2014-10-17) | 987 | RG-0044 |
| `rr_transcripts` | FY 2014 Earnings Call (2015-02-13) | 892 | RG-0037 |
| `rr_transcripts` | Special Call on the CEO change (2015-04-22) | 876 | RG-0012, RG-0014 |
| `rr_transcripts` | Interim Management Statement Call (2015-11-12) | 817 | RG-0038 |
| `rr_transcripts` | Shareholder/Analyst Call, strategy update (2015-11-24) | 762, 763, 782 | RG-0015, RG-0016, RG-0017, RG-0034 |
| `rr_transcripts` | Analyst/Investor Day (2016-11-16) | 678 | RG-0018 |
| `rr_transcripts` | FY 2016 Earnings Call (2017-02-14) | 669 | RG-0039 |
| `rr_transcripts` | FQ2 2017 Earnings Call (2017-08-01) | 630 | RG-0040 |
| `rr_transcripts` | 2018 AGM (2018-05-03) | 564 | RG-0003, RG-0019, RG-0020, RG-0021, RG-0046 |
| `rr_transcripts` | Special Call, governance and ESG day (2019-04-03) | 457, 461, 462 | RG-0022, RG-0023, RG-0024, RG-0025, RG-0026 |
| `rr_transcripts` | 2019 AGM (2019-05-02) | 441, 442 | RG-0027, RG-0028, RG-0029 |
| `rr_transcripts` | 2020 AGM (2020-05-07) | 367, 368, 377 | RG-0004, RG-0005, RG-0006, RG-0007, RG-0030, RG-0031, RG-0032 |
| `rr_transcripts` | Special Call, recapitalisation (2020-10-01) | 335 | RG-0033 |
| `rr_transcripts` | FY 2020 Earnings Call (2021-03-11) | 306 | RG-0008 |
| `rr_transcripts` | FH1 2021 Earnings Call (2021-08-05) | 252 | RG-0009 |
| `rr_transcripts` | FY 2021 Earnings Call (2022-02-24) | 216 | RG-0010, RG-0011 |
| `rr_transcripts` | FH1 2023 Earnings Call (2023-08-03) | 146 | RG-0035 |
| `rr_transcripts` | FH1 2024 Earnings Call (2024-08-01) | 59 | RG-0041 |
| `rr_transcripts` | FY 2024 Earnings Call (2025-02-27) | 32 | RG-0042, RG-0043 |

The extracted text is in `$WARGAME_BUILD_DIR/text/rr_transcripts.txt` and `rr_sec.txt`, with page markers. The
`rr_sec.txt` file holds the ADR deposit agreements and Form F-6 filings (2015, 2020, 2021, 2022). It has no annual
report, no governance report and no remuneration report.

`board.md` also cites existing company items (R-) and executive items (RX-) from
`wargame/profiles/rolls_royce/evidence.jsonl` and `executives/evidence.jsonl`, unchanged.
