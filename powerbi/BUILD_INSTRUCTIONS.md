# Power BI Project instructions

## Current status

The completed report is the Power BI Project [vch_vancouver_allocation.pbip](vch_vancouver_allocation.pbip). It contains six approved analytical pages plus the technical `PBIR Templates` authoring page. Source-controlled PBIR, TMDL, Power Query, DAX, registered TopoJSON, and report resources are retained for reproducibility.

## Open and refresh

1. Clone the repository.
2. Open `powerbi/vch_vancouver_allocation.pbip` in Power BI Desktop.
3. In **Transform data > Manage Parameters**, set `pProjectRoot` to the absolute cloned repository root.
4. Refresh and confirm the analytical controls below.
5. Do not rebuild the report from the legacy PBIX shell.

## Relationships

- `DimCHSA[CHSA Code]` 1 → * `FactCommunityProfile[CH_SA_CODE]`
- `DimCHSA[CHSA Code]` 1 → * `FactFacilitySupply[CH_SA_CODE]`
- `DimCHSA[CHSA Code]` 1 → * `FactAllocationScenario[CH_SA_CODE]`
- `DimCHSA[CHSA Code]` 1 → * `DimFacility[CMNTY_HLTH_SERV_AREA_CODE]`

## Analytical pages

1. Executive Overview
2. Community Vulnerability
3. Data Blindspots
4. Healthcare Supply & Service Gaps
5. Resource Allocation Scenario
6. Methodology & Data Quality

`PBIR Templates` is a technical authoring page. Hide it manually in Desktop before publication if desired.

## Refresh acceptance

- Population: 663,894
- Vancouver-focused CHSAs: 19
- Mapped facilities: 153
- Passed controls: 13; failed controls: 0
- Scenario totals: $10,000,000, 50.0 FTE, 1,000 units
- Reconciliation measures: zero
- All 19 Shape Map polygons render
- Facility point map renders and responds to the CHSA slicer
- UBC is absent; Northeast False Creek is not renamed Strathcona

## Screenshot export

Export each approved analytical page at 1920 × 1080 using the filenames in [images/README.md](../images/README.md). Do not export the technical `PBIR Templates` page.
