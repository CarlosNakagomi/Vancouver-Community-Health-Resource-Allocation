# Validation Report

## Automated status

All 13 controls pass. Detailed results are in [validation_results.csv](../outputs/data_quality/validation_results.csv) and [validation_summary.json](../outputs/data_quality/validation_summary.json).

| Control | Status |
|---|---|
| 19 Vancouver City CHSAs included | PASS |
| CHSA keys unique | PASS |
| UBC CHSA excluded | PASS |
| Partial CHSA overlap flagged | PASS |
| Canonical facility keys unique | PASS |
| Facility-to-CHSA referential integrity | PASS |
| No null spatial assignments | PASS |
| Analytical scores within 0–100 | PASS |
| Budget sums to $10,000,000.00 | PASS |
| Clinical FTE sums to 50.0 | PASS |
| Community-care units sum to 1,000 | PASS |
| Four sensitivity scenarios complete | PASS |
| Included-source population sums to 663,894 | PASS |

Additional verified values: 153 mapped facilities, one edge-tolerance assignment, zero failed controls, zero referential-integrity failures, and 76 sensitivity rows (19 CHSAs × 4 scenarios).

## Controls and auditability

Raw-file SHA-256 hashes are captured on each run. Source and processed keys are checked separately. Spatial assignments retain their method status. Largest-remainder allocation prevents rounding drift. Power BI reconciliation measures are included in the source-controlled semantic model.

## Power BI acceptance

The completed PBIP has been opened and visually inspected in Power BI Desktop. Its six analytical pages, Shape Maps, facility point map, interactions, KPI totals, allocation visuals, and methodology page were accepted. Real publication screenshots remain a manual export task.
