# Data dictionary

The full 141-field machine-readable dictionary is `outputs/data_quality/source_data_dictionary.csv`. The tables below document analytical fields used by the portfolio.

## Source fields

| Physical field | Logical meaning | Type/unit | Notes |
|---|---|---|---|
| `CH_SA_CODE` | CHSA code | Text | Source candidate primary key |
| `CH_SA_NAME` | CHSA name | Text | Source geography label |
| `CHSRBRL_CL` | Urban/rural class | Text | Source classification |
| `CHSPOP_CEN` | Census population | Integer persons | Total source census population |
| `HLT_A_CODE`, `HLT_A_NAME` | Local Health Area | Text | Vancouver-named LHA is not itself a city test |
| `HAUTH_CODE`, `HAUTH_NAME` | Health Authority | Text | VCH is broader than Vancouver City |
| `LG_FRM_DFQ` | Long-form data-quality flags | Text code | Preserve leading zeroes |
| `LG_FRM_GNR` | Long-form global non-response | Percentage points | Source value, 0–100 when valid |
| `GRP_A_TTL` | Age groups, all persons | Integer persons | 25% sample universe in private households |
| `0_14_A_TTL` | Age 0–14 | Integer persons | 25% sample, randomly rounded |
| `65PLS_A_TL` | Age 65+ | Integer persons | 25% sample, randomly rounded |
| `index` | ODHF source record ID | Text/integer | Unique in source |
| `facility_name` | Facility name | Text | Source-provided |
| `odhf_facility_type` | Harmonized facility type | Category | Three main classes plus source nulls/case issues |
| `provider` | Contributing data provider | Text | Not necessarily owner/operator |
| `city`, `province` | Reported location text | Text | Normalized before filtering |
| `CSDuid` | Census subdivision UID | Text | Sparse; not used alone |
| `latitude`, `longitude` | Facility coordinate | Decimal degrees | WGS84/EPSG:4326 |

## Derived analytical fields

| Field | Definition | Classification |
|---|---|---|
| `CityOverlapShare` | CHSA polygon area intersecting Vancouver CSD ÷ CHSA polygon area | Derived geographic metric |
| `CanonicalFacilityID` | Stable ID after conservative name/coordinate canonicalization | Derived key |
| `SpatialAssignmentStatus` | Point-in-polygon or documented 25 m edge tolerance | Data lineage |
| `YouthShare` | `0_14_A_TTL / GRP_A_TTL` | Derived metric |
| `SeniorShare` | `65PLS_A_TL / GRP_A_TTL` | Derived metric |
| `CommunityVulnerabilityProxyScore` | Equal-weight youth/senior percentile score | Proxy/index; not validated prediction |
| `DataBlindspotScore` | Within-city GNR percentile rank | Data uncertainty index |
| `FacilitiesPer10K` | Canonical facility count ÷ population × 10,000 | Supply-location metric |
| `HealthcareSupplyGapScore` | Reverse percentile of facilities per 10,000 | Supply proxy |
| `ResourcePriorityScore` | Weighted scenario combination of three separate scores | Scenario output |
| `ScenarioBudgetAllocation` | Balanced scenario allocation of hypothetical $10M | Scenario output |
| `ScenarioClinicalFTEAllocation` | Balanced scenario allocation of hypothetical 50.0 FTE | Scenario output |
| `ScenarioCommunityCareAllocation` | Balanced scenario allocation of hypothetical 1,000 units | Scenario output |

