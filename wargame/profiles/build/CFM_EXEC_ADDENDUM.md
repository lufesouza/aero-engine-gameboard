# Addendum to EXEC_READER_BRIEF.md: CFM International's leaders

Use this together with `EXEC_READER_BRIEF.md`. Where the two differ, this file wins.

## Who decides for CFM

CFM International is a 50/50 joint venture of GE (through Engine Investments Holding Company) and Safran Aircraft Engines. It builds the CFM56 and the LEAP: LEAP-1A for the A320neo, LEAP-1B for the 737 MAX, LEAP-1C for the C919. It also runs the RISE open-fan programme. CFM's own officers do not speak on any call in the corpus. CFM International's chief executive in November 2025 was Gaël Méheust ("Chief Executive Officer and President"; Capital IQ profile, source `cfm_ciq`). The strategic calls are made by the two parents: which engine to launch, pricing and concessions, capacity, durability fixes and partner terms.

The sources hold **GE's** side only: 135 GE / GE Aerospace calls, conferences and investor days from November 2015 to November 2025 (source `ge_transcripts`). The CFM leaders profiled here are therefore the GE executives who decide GE's half of CFM and speak for it:

- **CEO seat:**
  - `culp`: H. Lawrence Culp, Chairman and CEO from October 2018; CEO of GE Aerospace after the 2024 spin-offs;
  - `flannery`: John Flannery, CEO from August 2017 to October 2018 (his earlier turns are as head of GE Healthcare);
  - `immelt`: Jeff Immelt, Chairman and CEO to 2017.
- **CFO seat:**
  - `ghai`: Rahul Ghai, CFO from 2023;
  - `dybeck_happe`: Carolina Dybeck Happe, CFO 2020-2023;
  - `miller`: Jamie Miller, CFO from late 2017 to 2020 (earlier turns in other roles);
  - `bornstein`: Jeff Bornstein, Vice Chair and CFO to 2017.
- **Operating seat (COO type):**
  - `stokes`: Russell Stokes. He led GE Power earlier; later he was President and CEO of GE Aviation, then of Commercial Engines & Services at GE Aerospace;
  - `ali`: Mohamed Ali. VP of Engineering in the transcripts; "Senior VP and Chief Technology & Operations Officer" in the November 2025 Capital IQ profile;
  - `joyce`: David Joyce, President and CEO of GE Aviation and Vice Chairman of GE, to 2020;
  - `slattery`: John Slattery, President and CEO of GE Aviation, about 2020-2022;
  - `fitzgerald`: Bill Fitzgerald, VP and GM of the Commercial Engines Operation, 2017;
  - `mcallister`: Kevin McAllister, CEO of GE Aviation Services, 2016.
- **The partnership as a body:**
  - `cfm_jv`: statements about CFM International itself, the Safran partnership, its governance and the LEAP/RISE programmes, whoever speaks;
  - CFM's own officers as listed by Capital IQ.

Confirm each person's title as printed on the page; the dates above are a guide only.

## Scope inside a slice

GE was a conglomerate until 2024. Its leaders talk about Power, Renewables, Healthcare, GE Capital and the break-up.

- **Take everything on aviation:**
  - CFM, LEAP, CFM56, GE9X, GEnx, the RISE open fan, narrowbody and widebody engines;
  - aftermarket, services, shop visits, time on wing, pricing, spare engines, LTSA/CSA contracts;
  - OE losses and margins, durability fixes, supply chain and rates;
  - customers (Boeing, Airbus, COMAC, airlines, lessors) and rivals (Pratt & Whitney's GTF, Rolls-Royce);
  - the Safran partnership.
- **Take group-level behaviour that shows how the person decides,** wherever it occurs:
  - capital allocation (buybacks, dividends, M&A, deleveraging, ratings);
  - portfolio moves (break-up and spin-offs);
  - guidance and credibility (commitments and outcomes);
  - crisis response (GE Capital, Power, COVID, the 737 MAX grounding);
  - management systems (lean, decentralisation, "fix the house").
- **Skip** business-specific detail on Power, Healthcare or Renewables unless it reveals a general decision rule.
- **Weighting:** where a slice has aviation content, at least 40% of items should be on aviation and CFM.

Use the dimensions in the brief. Tag Safran and partnership items `product_strategy` (programme and partner choices) or `team` (governance, decision rights).

## Item fields

- `"company": "cfm"`.
- `"source"`: `ge_transcripts`, or `cfm_ciq` / `ge_ciq` / `eihc_ciq` for the Capital IQ profiles. Page numbers are the `=== PAGE N ===` markers. Read pages with `WARGAME_BUILD_DIR=<S> python3 wargame/profiles/build/pages.py <source> <first> <last>`.
- `"role_at_time"`: as printed, e.g. "Chairman & CEO", "Senior VP & CFO", "President & CEO, GE Aviation", "President and CEO of Commercial Engines & Services", "VP of Engineering".
- `"perspective"`: `own_words` for the executive's own turns; `analyst_question` for a question; `filing` for Capital IQ facts.
- **Currency:** GE reports in $.

**Personal data.** Record professional conduct only. No private life, health or family. No contact details, even where a profile page prints them.
