# Vancouver Community Health Resource Allocation

Independent portfolio project using public/open Vancouver census, healthcare-facility, and geographic data to model community-level planning priorities and hypothetical resource-allocation scenarios. The completed dashboard covers 19 Vancouver-focused Community Health Service Areas (CHSAs), 663,894 residents, and 153 mapped facility locations.

> **Not affiliated with or commissioned by Vancouver Coastal Health.** The scores are comparative planning proxies, and all resource allocations are hypothetical scenario outputs—not actual VCH budgets, staffing decisions, commitments, or recommendations.

## Quick Access

- **[View Dashboard Report (PDF)](Vancouver_Community_Health_Resource_Allocation.pdf)** — fastest six-page static review
- **[Open Interactive Power BI Report (.pbix)](powerbi/vch_vancouver_allocation.pbix)** — completed dashboard, semantic model, and imported portfolio data; requires Power BI Desktop
- **[Inspect the Power BI source project (.pbip)](powerbi/vch_vancouver_allocation.pbip)** — source-controlled PBIR report, TMDL model, Power Query, and DAX implementation
- [Management Brief](docs/management_brief.md) · [Methodology](docs/methodology.md) · [Validation Report](docs/validation_report.md)
- [Power BI Build Instructions](powerbi/BUILD_INSTRUCTIONS.md) · [Business Rules](docs/business_rules.md) · [Data Dictionary](docs/data_dictionary.md)

## Business Question

> "How can Vancouver Coastal Health leverage local socio-demographic population profiles and census non-response rates to predict community vulnerability, and how should we strategically distribute and allocate public healthcare resources—such as clinical staff, operational budgets, and community care services—to address geographic service gaps?"

Here, “predict community vulnerability” is operationalized as a transparent age-structure proxy—not a clinical prediction.

## Key Findings

- **Sunset** has the highest Balanced Resource Priority Score (**76.97**) and remains first or second across all tested weighting scenarios.
- **West Point Grey/Dunbar-Southlands** has the highest age-structure vulnerability proxy and approximately **0.57 mapped facilities per 10,000 residents**.
- **Downtown Eastside** has the highest Long-Form GNR (**13.5%**), indicating census-response uncertainty—not socioeconomic or clinical vulnerability.
- **Northeast False Creek** has zero mapped ODHF facilities and the largest positive illustrative budget shift (**+$160,656.11**). Zero mapped facilities does **not** prove unmet healthcare need or poor access.
- **All 13 automated validation controls pass**, including exact reconciliation to **$10 million**, **50 FTE**, and **1,000 community-care units**.

## Methodology at a Glance

    Public Data → Geographic Validation → Community Profile → Vulnerability Proxy
    → Data Blindspot → Healthcare Supply Gap → Resource Priority → Scenario Allocation

| Model component | Scenario logic |
|---|---|
| **Resource Priority** | 45% Vulnerability Proxy + 25% Data Blindspot + 30% Healthcare Supply Gap |
| **Hypothetical Allocation** | 60% Population Share + 40% Resource Priority Share |

These weights are transparent modelling assumptions, not empirically validated healthcare-allocation coefficients. See the [detailed methodology](docs/methodology.md) and [validation report](docs/validation_report.md).

## Data Sources

- [Statistics Canada — 2016 Census / Census Profile](https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E)
- [Statistics Canada / Government of Canada — Open Database of Healthcare Facilities (ODHF)](https://open.canada.ca/data/en/dataset/a1bcd4ee-8e57-499b-9c6f-94f6902fdf32)
- [BC Community Health Service Area geography](https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_admin_boundaries/MapServer/12)
- [Statistics Canada — Vancouver Census Subdivision boundary](https://open.canada.ca/data/en/dataset/90db78e2-eda2-4b2c-ae2e-a474187f2bf8)

Raw source inputs are not redistributed in this repository; obtain them from their original public providers. Attribution and source metadata are available in [data/reference](data/reference/) and the [methodology](docs/methodology.md).

## Tech Stack

**Power BI · DAX · Power Query · Python · pandas · SQL/SQLite · GeoPandas/Shapely · Git/GitHub**

## Important Interpretation

The **Vulnerability Proxy** uses age structure and is not a clinical-need or multidimensional deprivation measure; **General Non-Response Rate (GNR)** represents census uncertainty, not disadvantage; **mapped facility counts** are a supply-location proxy, not capacity, access, or ownership; and **scenario allocations are hypothetical**, not actual VCH allocations or recommendations.

## Technical Documentation

[Management Brief](docs/management_brief.md) · [Methodology](docs/methodology.md) · [Business Rules](docs/business_rules.md) · [Validation Report](docs/validation_report.md) · [Data Quality Report](docs/data_quality_report.md) · [Limitations](docs/limitations.md) · [Power BI Build Instructions](powerbi/BUILD_INSTRUCTIONS.md)

## License

The [MIT License](LICENSE) applies only to the author's original code. Third-party datasets and source materials remain subject to their respective licences, terms, and attribution requirements.
