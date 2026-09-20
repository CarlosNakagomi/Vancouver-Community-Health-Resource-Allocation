# Vancouver Community Health Resource Allocation Analytics

> **Independent portfolio project using public/open data. Not affiliated with or commissioned by Vancouver Coastal Health. Resource-allocation outputs are hypothetical planning scenarios and do not represent actual VCH budgets, staffing decisions, service commitments, or recommendations.**

An end-to-end analytics project using Python, SQL, geospatial validation, Power BI, DAX, scenario modelling, and automated data-quality controls. It examines 19 Vancouver-focused Community Health Service Areas (CHSAs) while keeping age-structure vulnerability, census uncertainty, and mapped facility-location scarcity analytically distinct.

## Executive Summary

- **663,894 people** across **19 Vancouver-focused CHSAs**.
- **153 mapped public healthcare-facility locations**, with zero null retained spatial assignments.
- A transparent Resource Priority Score tested under **four weighting scenarios**.
- A hypothetical **60% population / 40% priority** allocation compared with a population-only baseline.
- **13 automated validation controls passed; 0 failed.**

This model does not predict validated clinical need or establish causal healthcare demand.

## Business Question

> How can Vancouver Coastal Health leverage local socio-demographic population profiles and census non-response rates to predict community vulnerability, and how should we strategically distribute and allocate public healthcare resources—such as clinical staff, operational budgets, and community care services—to address geographic service gaps?

Here, “predict community vulnerability” is operationalized as a transparent **age-structure proxy**, not a clinical prediction.

## Dashboard Preview

The completed source-controlled Power BI Project is [powerbi/vch_vancouver_allocation.pbip](powerbi/vch_vancouver_allocation.pbip). Its six analytical pages are Executive Overview, Community Vulnerability, Data Blindspots, Healthcare Supply & Service Gaps, Resource Allocation Scenario, and Methodology & Data Quality.

Real page screenshots have not yet been exported. Required filenames are listed in [images/README.md](images/README.md); no mock dashboard images are used here.

## Key Findings

- **Sunset** has the highest Balanced Resource Priority Score (**76.97**) and ranks first or second under every tested weighting scenario.
- **West Point Grey/Dunbar-Southlands** ranks second, has the highest age-structure Vulnerability Proxy, and approximately **0.57 mapped facilities per 10,000 residents**.
- **Northeast False Creek** ranks fifth, has a Data Blindspot Score of **92.11**, and has zero mapped ODHF facilities in the retained assignment. This does **not** prove lack of healthcare access or unmet need.
- **Downtown Eastside** has the highest Long-Form GNR (**13.5%**), indicating census-data uncertainty—not socioeconomic or clinical vulnerability.
- **Fairview** has the highest mapped facility rate (approximately **5.11 per 10,000**), the lowest supply-gap score, and ranks last.
- **Northeast False Creek** has the largest positive illustrative budget shift versus population-only allocation (**+$160,656.11**). This is not an actual funding increase.
- **Sunset, West Point Grey/Dunbar-Southlands, and Oakridge/Marpole** remain Top 5 under all four scenarios.

## Management Implications

- Investigate Sunset with current operational evidence because several modelled components contribute to its signal.
- Examine cross-boundary access for West Point Grey/Dunbar-Southlands before interpreting facility density.
- Treat Northeast False Creek as a data-validation and service-mapping signal, not proof of unmet need.
- Supplement Downtown Eastside census analysis with local/administrative evidence because of elevated non-response.
- Review component scores and sensitivity ranges rather than relying on one rank.

## Analytical Framework

```text
Public Data → Geographic Validation → Community Profile → Vulnerability Proxy
→ Data Blindspot → Healthcare Supply Gap → Resource Priority → Scenario Allocation
```

## Data Sources

| Source | Use | Important limitation |
|---|---|---|
| [Statistics Canada 2016 Census / CHSA profile](https://catalogue.data.gov.bc.ca/dataset/da8d93a5-a6b0-4f07-80e5-1a1ec3776595) | Population, age structure, Long-Form GNR | 2016 vintage; not clinical need |
| [Open Database of Healthcare Facilities](https://open.canada.ca/data/en/dataset/a1bcd4ee-8e57-499b-9c6f-94f6902fdf32) | Facility names, types, providers, coordinates | Locations do not measure capacity or confirm VCH ownership |
| [BC CHSA boundaries](https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_admin_boundaries/MapServer/12) | CHSA geography | Administrative boundaries do not measure access |
| [Statistics Canada 2016 CSD boundary](https://open.canada.ca/data/dataset/90db78e2-eda2-4b2c-ae2e-a474187f2bf8) | Vancouver City validation | 2016 boundary vintage |

Attribution is preserved under [data/raw](data/raw/) and [data/reference](data/reference/). No confidential or internal VCH data is used. ODHF is a **supply-location proxy**; it does not measure beds, staffing, volume, hours, utilization, wait times, accessibility, quality, or outcomes.

## Data Pipeline

[python/run_pipeline.py](python/run_pipeline.py) orchestrates profiling, quality assessment, cleaning, geographic validation, scoring, sensitivity analysis, allocation, and acceptance validation. [python/build_sqlite.py](python/build_sqlite.py) materializes SQLite. SQL views and controls are in [sql/04_analytical_views.sql](sql/04_analytical_views.sql) and [sql/05_validation.sql](sql/05_validation.sql).

The executable CHSA inclusion rule is `CityOverlapShare >= 0.50`; it retains 19 CHSAs and excludes UBC CHSA 3243. Facilities are assigned by point-in-polygon. One point required a 25-metre edge tolerance; none has a null retained assignment. Of 196 Vancouver text candidates, 29 lacked coordinates and may contribute to undercounting. Northeast False Creek is not renamed Strathcona.

## Power BI Data Model

The PBIP contains a star schema with CHSA/facility dimensions, community/supply/allocation facts, sensitivity and validation tables, and reusable DAX measures. PBIR, TMDL, Power Query, DAX, and TopoJSON are retained for auditability.

The `pProjectRoot` Power Query parameter contains the author's local path. After cloning, update it in Power BI Desktop to the repository root before refresh; this is local-development configuration, not a secret.

## Resource Priority Methodology

```text
45% Vulnerability Proxy + 25% Data Blindspot + 30% Healthcare Supply Gap
= Resource Priority Score
```

Vulnerability is an age-structure proxy, Data Blindspot is census uncertainty, and Supply Gap is inverse mapped facility-location density. None is a validated clinical-need or capacity measure. Weights are transparent assumptions, not validated allocation coefficients.

## Scenario Allocation Methodology

`Allocation Weight = 60% Population Share + 40% Resource Priority Share`

This is applied to hypothetical pools of **$10,000,000**, **50.0 clinical FTE**, and **1,000 community-care units**. A population-only baseline is retained; largest-remainder reconciliation makes totals exact. Outputs are not actual VCH allocations or recommendations.

## Sensitivity Analysis

Weights are Vulnerability / Blindspot / Supply Gap:

| Scenario | Weights | Spearman vs. Balanced |
|---|---:|---:|
| Balanced | 45 / 25 / 30 | 1.000 |
| Need-focused | 60 / 10 / 30 | 0.869 |
| Uncertainty-aware | 35 / 35 / 30 | 0.918 |
| Supply-gap-focused | 35 / 15 / 50 | 0.892 |

Rank movement demonstrates dependence on modelling assumptions.

## Data Quality & Validation

- 13 controls passed; 0 failed.
- Population **663,894**; CHSAs **19**; mapped facilities **153**.
- Null retained assignments **0**; edge-tolerance assignments **1**; referential-integrity failures **0**.
- Sensitivity rows **76 = 19 × 4**.
- Scenario totals reconcile to **$10,000,000**, **50.0 FTE**, and **1,000 units**.

See [validation results](outputs/data_quality/validation_results.csv), [methodology](docs/methodology.md), and the [validation report](docs/validation_report.md).

## Technology Stack

Python, pandas, NumPy, SciPy, GeoPandas, Shapely, SQLite, SQL, Power BI Desktop, PBIP/PBIR, Power Query, TMDL, DAX, GeoJSON/TopoJSON, pytest, and Git.

## Repository Structure

```text
data/       Raw, reference, interim, and processed data
docs/       Methodology, validation, limitations, and management documentation
images/     Final Power BI screenshots (manual export pending)
outputs/    Analytical tables, validation results, SQLite, and supporting figures
powerbi/    PBIP/PBIR, semantic model, Power Query, DAX, and resources
python/     ETL, geospatial, scoring, allocation, and validation pipeline
sql/        Schema, loading, analytical views, and validation queries
tests/      Automated tests
tools/      Supporting utilities
archive/    Historical prototype artifacts retained for provenance
```

## Reproducibility

Prerequisites: a Python 3.13-compatible environment and Power BI Desktop.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python python\run_pipeline.py
python python\build_sqlite.py
python python\07_validation.py
python -m pytest -q
```

The public source/reference files required by the pipeline are included. Then open [the PBIP](powerbi/vch_vancouver_allocation.pbip), update `pProjectRoot`, and refresh. See [Power BI instructions](powerbi/BUILD_INSTRUCTIONS.md).

## Limitations

- Census data are from 2016; vulnerability uses age structure only.
- GNR measures uncertainty, not disadvantage.
- ODHF is location data, not capacity, staffing, ownership, utilization, accessibility, quality, or outcomes.
- Missing coordinates may undercount supply; cross-boundary services and patient flows are not modelled.
- Weights are assumptions; allocations are hypothetical.
- The model does not establish causal demand or unmet clinical need.

Operational use would require current capacity, staffing, utilization, wait times, patient flows, accessibility, service scope, outcomes, population conditions, and stakeholder/clinical validation.

## Responsible Interpretation

Do not interpret a score, rank, zero mapped-facility count, or scenario allocation as evidence of actual healthcare need, inadequate access, or an approved decision.

## Author / Portfolio Context

This independent portfolio demonstrates business framing, public-data engineering, geospatial validation, SQL, Python, Power BI modelling, DAX, scenario design, sensitivity analysis, validation, and management communication.

## License

The [MIT License](LICENSE) applies only to the author's original code. Third-party datasets and source materials remain subject to their respective source licences, terms, and attribution requirements.

## Documentation

[Management brief](docs/management_brief.md) · [Methodology](docs/methodology.md) · [Business rules](docs/business_rules.md) · [Data dictionary](docs/data_dictionary.md) · [Data-quality report](docs/data_quality_report.md) · [Validation report](docs/validation_report.md) · [Limitations](docs/limitations.md) · [Publication checklist](docs/FINAL_PORTFOLIO_CHECKLIST.md)
