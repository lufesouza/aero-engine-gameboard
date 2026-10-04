# How the behavioural profiles were built

The Boeing and Airbus agents play from `wargame/profiles/<side>/`. Those profiles were built from the source files uploaded to the repository root:

- 151 Boeing earnings calls, conferences and investor days from 2006-2025 (S&P transcripts);
- 16 Boeing 10-Ks (roughly FY2008-FY2024);
- the Goldman Sachs (Jan 2026) and Morgan Stanley Boeing models;
- Capital IQ income-statement and segment histories;
- the Airbus SE Report of the Board of Directors FY2025.

## Pipeline

Working files go to `wargame/profiles/build/work/` (git-ignored), or to `$WARGAME_BUILD_DIR`.

1. **Extract text**: `python3 extract_text.py` (pypdf, xlrd). This writes one text file per source with `=== PAGE N ===` markers, a transcript index, and Capital IQ CSVs.
2. **OCR the Airbus report**: `python3 ocr_airbus.py 3` (pymupdf, rapidocr-onnxruntime). The PDF's Type3 fonts have no text layer, so all 255 pages are rendered and OCR'd. OCR sometimes runs words together, and quote verification tolerates that.
3. **Extract evidence**: 23 reader agents, each following `READER_BRIEF.md`, covered the material in slices:
   - 15 transcript slices by era;
   - 4 groups of 10-Ks;
   - the Airbus-mention pages, forming the action/reaction timeline;
   - 3 slices of the Airbus report;
   - the analyst models, extracted by script.

   Each reader appended cited items (verbatim quote, page, finding, trigger/response/lag) to `work/evidence/<reader>.jsonl`.
4. **Verify**: `python3 verify_quotes.py work/evidence/*.jsonl`. Every quote is machine-checked against its cited page (±1 page, normalised; a space-free comparison for OCR text). Items that fail are dropped. Of 2,942 extracted items, 2,941 passed.
5. **Merge**: `python3 merge_evidence.py boeing|airbus`. This de-duplicates and splits the evidence per side, assigning ids B-#### and A-####:
   - **Boeing:** Boeing's own behaviour, plus Boeing's observations of Airbus (its intel).
   - **Airbus:** Airbus's own report, plus Airbus's behaviour as observed by Boeing and analysts (flagged as an outside view), plus Boeing's 2023+ public statements (its intel).
6. **Synthesise**: separate agents for each side (`DRAFT_BRIEF.md`, `SYNTH_BRIEF.md`). Boeing had five theme drafters (financial, operational, product, reaction function, biases) and an integrator. Airbus had one synthesiser. The two sides never saw each other's drafts.

## Rebuilding

Add sources to the repository root, for example Airbus earnings-call transcripts, which would most improve the Airbus agent. Extend `extract_text.py` and re-run the steps. Readers and synthesisers are Claude Code agents: ask Claude to "rebuild the war-game profiles following wargame/profiles/build/README.md".


## The engine-maker profiles (Rolls-Royce, Pratt & Whitney)

These come from the files uploaded to `main` on 30 Sep 2026:
- `Transcript Digest 2010-26.pdf`: Rolls-Royce earnings calls;
- `Transcript Digest 15-25.pdf`: UTC/RTX calls;
- `Filings.pdf`: UTC/RTX 10-Ks, FY2016-FY2024;
- `Durability news 11-19-25.pdf`;
- `Global Strategy Brief-2019-...pdf`;
- the RR workbooks: the Morgan Stanley model and two Capital IQ reports;
- `GoldmanSachs_RTX102125_Oct_22_2025.xlsx`. `GoldmanSachs_GTF_Oct_22_2025.xlsx` holds identical values.

`SEC Fillings.pdf` is RR's ADR deposit agreement: legal boilerplate with no behavioural content, so it is not used.

1. **Text:** `python3 extract_text_engines.py` (pymupdf). It writes per-page text and event indexes for the transcript digests and the 10-K bundle.
2. **Cells:** `python3 cells_dump.py rr . <out>` and `python3 cells_dump.py pw . <out>` (openpyxl, xlrd). Every non-empty cell is written with its A1 reference, row label and period header.
3. **Readers.** 30 agents (`ENGINE_READER_BRIEF.md` for text, `RR_READER_BRIEF.md` for cells) covered:
   - **RR:** its transcripts in 7 era slices, 7 spreadsheet readers, RR as seen by Boeing and Airbus, and the industry sources;
   - **P&W:** the RTX transcripts in 9 yearly slices, the 10-Ks in 3 groups, 2 readers for the GS model, and the industry sources;
   - one completeness critic and one gap-filler per company.
4. **Verify:**
   - `verify_quotes.py` checks text items (±1 page);
   - `verify_cells.py` (with `RR_CELLS_DIR`) checks spreadsheet items, with numbers within 0.5%;
   - a second independent pass re-checked all 3,385 quotes and 639 cells.
5. **Merge:** `engine_merge_evidence.py rolls_royce|pratt_whitney <dir> <out>` assigns R-#### or P-####.
6. **Calibrate.** For each company, two independent calibrations (bottom-up unit economics; top-down segment reconciliation) and a reconciler. The output is `calibration.md` and the `suppliers.*` values in `config/default.json`.
7. **Synthesise and audit.** Following `ENGINE_SYNTH_BRIEF.md`, each company gets:
   - theme drafters, then an integrator;
   - three independent audits: citations (`cite_check.py --show`), numbers, and a playability red team that plays turn 1;
   - a fix pass, which writes `citation_audit.md`.

   The two companies' builders never saw each other's material.

## CFM International's leaders (GE side)

CFM International is a 50/50 GE-Safran joint venture whose own officers do not speak in the sources. The CFM leadership profiles (`wargame/profiles/cfm/executives/`) therefore cover the GE executives who decide GE's half of CFM and speak for it.

**Sources:**
- `Transcript Digest.pdf`: 135 GE / GE Aerospace calls, conferences and investor days, November 2015 to November 2025;
- the Capital IQ profiles of CFM International, GE and Engine Investments Holding Company (November 2025).

**Steps:**
1. **Text:** `python3 extract_text_engines.py ge_transcripts cfm_ciq ge_ciq eihc_ciq`. This writes the text and the event index. Same-day events are split at their cover pages.
2. **Turns:** `python3 exec_turns.py ge_transcripts <dir>` splits out each GE executive's own speaking turns. The readers worked from 11 slices of them:
   - Culp: 4 slices;
   - Flannery, Immelt, Bornstein, Miller, Dybeck Happe and Ghai: 1 each;
   - one slice for the operating heads (Stokes, Joyce, Ali, Slattery, Fitzgerald, McAllister).
3. **Readers:** each follows `EXEC_READER_BRIEF.md` plus `CFM_EXEC_ADDENDUM.md`. One more reader covered the joint venture itself (`cfm_jv`): the Safran partnership, LEAP and RISE, and CFM's officers per Capital IQ, drawn from 120 pages that mention them.
4. **Verify and merge:**
   - `verify_quotes.py` checked every quote, and a second independent pass re-checked all 1,322;
   - every executive item was also checked to lie in that executive's own turns;
   - `exec_merge_evidence.py` assigns CX-#### ids, giving 1,300 items after duplicates are removed;
   - `exec_digests.py cfm <dir>` writes the per-executive reading digests.
5. **Synthesise and audit.** Writers follow `EXEC_SYNTH_BRIEF.md` plus `CFM_EXEC_SYNTH_ADDENDUM.md`. Two independent citation and fairness audits follow, then a fix pass that writes `citation_audit.md`.

**Not used yet:** the Goldman Sachs and Morgan Stanley CFM and Safran models. They are the inputs for a CFM company profile or a CFM supplier player.

## Plain-text role files (executives)

`python3 make_role_txt.py` turns the executive profiles into one plain-text file per role in `<company>/executives/roles/`:
- Boeing: `boeing_ceo.txt`, `boeing_cfo.txt`, `boeing_coo_bca.txt`;
- Airbus: `airbus_ceo.txt`, `airbus_cfo.txt`, `airbus_coo_commercial_aircraft.txt`;
- CFM: `cfm_ceo.txt`, `cfm_cfo.txt`, `cfm_coo_operations.txt`, plus `cfm_international.txt` on the joint venture;
- each company also gets `<company>_leadership_teams.txt` and a `README.txt`.

Each role file opens with the seat's job in the ExCo and the holders (from the executives `README.md` index), then carries each holder's full profile, current holder first. The text is a conversion, not a rewrite: every evidence id in the Markdown survives. The files stay inside each company's folder, so the isolation hook still keeps each player out of the other company's executives. Re-run the script after editing a profile.
