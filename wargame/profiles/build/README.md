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
