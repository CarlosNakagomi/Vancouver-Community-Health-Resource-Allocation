# Power Query load order

1. Create the text parameter `pProjectRoot` from `pProjectRoot.m` and set it to the cloned repository root.
2. Create `stg_CHSA_Census` and `stg_ODHF_Facilities`; disable load for both staging queries.
3. Create and load `DimCHSA`, `DimFacility`, `FactCommunityProfile`, `FactFacilitySupply`, and `FactAllocationScenario`.
4. Create one-to-many, single-direction relationships from `DimCHSA[CHSA Code]` to each fact table's CHSA key. Link `DimCHSA[CHSA Code]` to `DimFacility[CMNTY_HLTH_SERV_AREA_CODE]` if facility-level maps are used.

The Python pipeline owns the authoritative spatial join because Power Query has no native, auditable point-in-polygon operator. Power Query imports the validated results and retains the raw staging queries for interview-ready lineage.

