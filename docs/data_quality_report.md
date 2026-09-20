# Data quality report

## Executive assessment

Both raw files have unique candidate keys and no exact duplicate rows. The CHSA file is structurally strong for population and age analysis, but it is limited to 2016 age-profile variables and does not contain income, housing, immigration, language, education, employment, service use, staffing, budget, capacity, or health outcomes. ODHF has material coordinate and coverage limitations and should support geographic presence analysis only.

Machine-readable evidence is in `outputs/data_quality`.

## BCHACHSAPO.csv

| Test | Result |
|---|---:|
| Rows | 217 |
| Columns | 124 |
| Exact duplicate rows | 0 |
| Duplicate `CH_SA_CODE` values | 0 |
| Null `CH_SA_CODE` values | 0 |
| Negative numeric values | 0 |
| Youth count greater than age-sample total | 0 |
| Geometry/coordinate columns null | 217 rows |
| Long-form GNR outside 0–100 | 2 rows |

The two invalid GNR values are `1000` for Revelstoke and Tumbler Ridge, accompanied by source DQF flags. They are treated as source sentinel values, preserved for traceability, and converted to null in the cleaned percentage field. Neither affects Vancouver results.

The source contains 45 Vancouver Coastal Health Authority CHSAs, which is not equivalent to Vancouver City. City focus is established by polygon overlap, not authority name.

## odhf_bdoes_v1.csv

| Test | Result |
|---|---:|
| Rows | 9,039 |
| Columns | 17 |
| Exact duplicate rows | 0 |
| Duplicate `index` values | 0 |
| Missing coordinate pairs | 1,496 |
| Invalid/non-paired coordinates | 0 |
| Normalized BC + Vancouver text records | 196 |
| Text-filter records with coordinates | 167 |
| Coordinate points inside Vancouver CSD | 153 |
| Canonical mapped facilities | 153 |

Mapped facility categories are 103 nursing/residential care, 33 ambulatory health care, and 17 hospitals. Category counts are kept separate. `CSDuid` is too sparsely populated to be the only city filter. The pipeline uses text filtering plus spatial validation.

## Join and geographic risks

- CHSA source geometry fields are empty in the CSV. External authoritative polygons are required.
- UBC is part of a Vancouver-named health area but outside Vancouver City and is excluded.
- West Point Grey/Dunbar-Southlands has 84.6% area overlap. Whole-CHSA population may modestly overstate city-only population.
- One facility point required a documented 25-metre polygon-edge tolerance. Its source record remains auditable.
- Strathcona is not a separate CHSA in the 2016 source. The custom CHA 2 rule carries an unmatched member rather than inventing a mapping.

## Reproducible outputs

- `source_inventory.csv`: source hashes, grain, row/column counts, and candidate keys
- `repository_inventory.csv`: complete final file inventory excluding Git metadata, virtual environments, and caches
- `source_data_dictionary.csv`: physical-to-logical source fields
- `column_profile.csv`: nulls, uniqueness, type inference, numeric range, and samples for every column
- categorical distribution files
- geographic overlap and exclusion files
- validation summary and detailed results
