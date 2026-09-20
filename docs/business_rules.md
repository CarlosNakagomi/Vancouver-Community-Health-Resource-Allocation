# Business rules

## Business question

> How can Vancouver Coastal Health leverage local
> socio-demographic population profiles and census non-response rates to predict
> community vulnerability, and how should we strategically distribute and
> allocate public healthcare resources—such as clinical staff, operational
> budgets, and community care services—to address geographic service gaps?

The available public data do not contain an observed target for unmet need, actual VCH staffing, budgets, capacity, utilization, or program outcomes. The project therefore answers the question with a transparent analytical prioritization and hypothetical allocation scenario, not a validated predictive model or an actual VCH allocation recommendation.

## Vancouver City inclusion

- The geographic unit of analysis is the 2016 Community Health Service Area (CHSA).
- A CHSA is included when its overlap with Statistics Canada Census Subdivision 5915022 produces `CityOverlapShare >= 0.50` (Vancouver, City) for the 2016 Census.
- This includes 19 CHSAs and excludes CHSA 3243, University of British Columbia, whose overlap is effectively zero.
- CHSA 3242, West Point Grey/Dunbar-Southlands, is retained because 84.6% overlaps Vancouver City. Its published population represents the whole CHSA and is not area-apportioned.
- Facilities are first strictly text-filtered to normalized province `BC` and city `Vancouver`, then retained only when their coordinate falls inside the 2016 Vancouver CSD polygon.
- Facilities are assigned to CHSAs by point-in-polygon. A 25-metre polygon-edge tolerance resolves geocoding/boundary slivers; nearest-centroid assignment is prohibited.

## CHA 2 (Mid-East)

The requested mapping is preserved as a **project business rule**, not an official VCH geography:

| Business-rule member | Source match | Status |
|---|---|---|
| Downtown Eastside | CHSA 3221 Downtown Eastside | Matched |
| Strathcona | No separate CHSA in the supplied 2016 source | Unmatched |
| Grandview-Woodlands | CHSA 3223 Grandview-Woodland | Matched after spelling normalization |

The project does not rename CHSA 3222 Northeast False Creek to Strathcona. CHA 2 aggregates only matched source units in analytical totals and explicitly carries the unmatched Strathcona status. This avoids inventing a population value or polygon.

## Scoring rules

- `Community Vulnerability Proxy Score` is the equal-weight average of within-Vancouver percentile ranks for youth share and senior share. It is an age-structure prioritization proxy, not a validated clinical or socioeconomic vulnerability model.
- `Data Blindspot Score` is the within-Vancouver percentile rank of long-form census GNR. It measures relative data uncertainty and is kept separate from vulnerability.
- `Healthcare Supply Gap Score` is the reverse percentile rank of ODHF facility count per 10,000 population. It is a location-count proxy and does not measure capacity or VCH ownership.
- The default `Resource Priority Score` uses scenario weights of 45% vulnerability proxy, 25% data blindspot, and 30% supply gap.
- Scenario allocation weight is 60% population share plus 40% priority-score share. Largest-remainder allocation makes totals reconcile exactly.

## Facility rules

- ODHF provider identifies the contributing data source, not necessarily the facility operator.
- All ODHF facility types are retained and reported separately. Hospitals, ambulatory services, and nursing/residential care are not treated as equivalent.
- Apparent duplicate physical sites are canonicalized only when normalized name and coordinates rounded to four decimal places match. Source-to-canonical lineage is preserved.
- Facility counts are a service-presence proxy, not clinical capacity, VCH capacity, accessibility, quality, or utilization.

