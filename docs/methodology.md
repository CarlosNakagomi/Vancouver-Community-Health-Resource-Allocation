# Methodology

## Analytical framing

This project is an independent portfolio analysis using public/open data. It separates five concepts:

1. **Observed source data:** 2016 CHSA population/age counts, long-form GNR, ODHF facility records, and authoritative polygons.
2. **Derived metrics:** youth share, senior share, facilities per 10,000, population per facility, and weighted GNR.
3. **Proxy variables:** age-structure vulnerability and facility-location supply.
4. **Scenario assumptions:** component weights and hypothetical resource pools.
5. **Outputs:** relative priority ranks and reconciled hypothetical allocations.

No supervised prediction is fitted because there is no observed target variable such as unmet need, service utilization, outcomes, wait time, staffing, budget, or capacity. “Predict” in the business question is operationalized as transparent risk prioritization. Causal claims are not made.

## Data lineage

`data/raw` is immutable. `python/run_pipeline.py` executes understanding, quality profiling, cleaning, geographic mapping, proxy scoring, scenario allocation, and validation. Processed facts/dimensions are written to `data/processed`; audit summaries and final analytical tables are written to `outputs`.

### Source A: CHSA census age profile

- Title: Census Age Profiles for Community Health Service Areas — 2016 Census
- Publisher/distributor: BC Data Catalogue / BC Geographic Warehouse; Statistics Canada source licence
- Grain: one row per CHSA
- Coverage: 217 CHSAs in the supplied file; 19 selected for Vancouver City analysis
- The age profile represents persons in private households from 25% sample data. Counts are subject to Statistics Canada random rounding.
- GNR is a data-quality measure. Source values outside 0–100 (two records with value 1000 outside Vancouver) are retained in `_SOURCE_VALUE` fields and set to null in cleaned percentage fields.

### Source B: ODHF v1

- Publisher: Statistics Canada Open Database of Health Facilities
- Grain: one contributed facility record; providers can describe the same physical site
- National rows: 9,039
- Vancouver text-filter candidates: 196; candidates with coordinates: 167; inside 2016 Vancouver CSD: 153
- ODHF is an open compilation with uneven source coverage and update timing. Counts do not represent capacity or VCH ownership.

## Geographic method

Authoritative CHSA polygons come from the Government of British Columbia ArcGIS layer `WHSE_ADMIN_BOUNDARIES.BCHA_CMNTY_HEALTH_SERV_AREA_SP`. Vancouver City is Statistics Canada CSD 5915022 from the 2016 Census boundary service. Both were retrieved 2026-09-18 and stored as GeoJSON in `data/reference`.

Polygons are projected to EPSG:3005 for area and distance operations. CHSAs with `CityOverlapShare >= 0.50` with Vancouver CSD are included. Facility coordinates use EPSG:4326, are projected to EPSG:3005, filtered inside the city polygon, then spatially joined using `within`. One hospice point 14.6 metres outside the nearest CHSA coastal edge is assigned under the documented 25-metre boundary tolerance. No centroid method is used.

## Analytical indices

For CHSA *i*:

- Youth Share = `Age 0–14 / Age Sample Total`
- Senior Share = `Age 65+ / Age Sample Total`
- Vulnerability Proxy = `0.5 × percentile(Youth Share) + 0.5 × percentile(Senior Share)`
- Data Blindspot = `percentile(Long-form GNR)`
- Facilities per 10K = `Canonical Facility Count / Census Population × 10,000`
- Supply Gap = reverse percentile of Facilities per 10K
- Balanced Priority = `0.45 × Vulnerability + 0.25 × Blindspot + 0.30 × Supply Gap`

Percentile ranks are relative to the 19 included CHSAs and are not comparable to another geography or vintage without recalculation.

## Scenario allocation

Default hypothetical pools are $10,000,000, 50.0 clinical FTE, and 1,000 community-care units. These are not actual VCH resources.

`Allocation Weight = 0.60 × Population Share + 0.40 × Priority Score Share`

Each pool is distributed using the allocation weights. A largest-remainder method reconciles currency to cents, FTE to 0.1, and care units to integers.

## Sensitivity analysis

Four weight scenarios are calculated: Balanced, Need-focused, Uncertainty-aware, and Supply-gap-focused. Spearman rank correlation versus Balanced is 1.000, 0.869, 0.918, and 0.892 respectively. The top order changes under reasonable weights, so ranks must be presented as scenario-dependent rather than objective truth.

