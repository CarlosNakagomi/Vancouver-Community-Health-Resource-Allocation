# Build log

## 2026-09-18 — repository audit

- Inventoried the full working tree. Existing content consisted of two raw datasets, BC metadata/licence files, a static web prototype, and a 15 KB PBIX shell.
- Inspected PBIX internals: one page named `Page 1`, zero visuals, and a minimal data model. It contained no reusable analytical report.
- Preserved the web prototype and PBIX. No useful analytical scripts, SQL, Power Query, DAX, documentation, or validation existed.

## 2026-09-18 — source organization and profiling

- Moved source data into `data/raw` without modifying content. Stored metadata and licences in `data/reference`.
- Identified ODHF Windows-1252 encoding; the CHSA CSV is UTF-8.
- Profiled all 124 CHSA fields and 17 ODHF fields. Captured hashes, nulls, uniqueness, ranges, distributions, and candidate keys.
- Identified two out-of-range GNR sentinel values (`1000`) outside Vancouver; retained source values and cleaned them to null.

## 2026-09-18 — geographic correction

- Replaced the prototype's fabricated polygons and centroid assignment with authoritative Government of BC CHSA polygons and the Statistics Canada 2016 Vancouver CSD polygon.
- Adopted `CityOverlapShare >= 0.50` as the explicit city inclusion rule. Excluded UBC and flagged the 84.6% overlap of West Point Grey/Dunbar-Southlands.
- Implemented point-in-polygon facility assignment plus a documented 25 m polygon-edge tolerance for one source point.
- Preserved the CHA 2 project rule without falsely renaming Northeast False Creek as Strathcona.

## 2026-09-18 — analytical model

- Separated age-structure vulnerability proxy, census data blindspot, and facility supply gap.
- Added four sensitivity scenarios. Default priority weights are assumptions, not trained coefficients.
- Added exact largest-remainder allocation for hypothetical budget, clinical FTE, and community-care pools.
- Produced processed star-schema tables, statistical outputs, SQL, Power Query, DAX, figures, and management documentation.

## 2026-09-18 — validation and Power BI status

- All 13 automated pipeline checks pass.
- Historical note: at this stage the PBIX was an inspected blank shell. The report was subsequently completed as the source-controlled PBIP described in `powerbi/BUILD_INSTRUCTIONS.md`.

