-- Illustrative, interview-readable transformations once staging tables are loaded.
-- GNR is an uncertainty measure. It is not treated as socioeconomic vulnerability.
WITH community AS (
    SELECT
        CHSA_Code,
        Census_Population,
        Youth_Count * 1.0 / NULLIF(Age_Sample_Total,0) AS Youth_Share,
        Senior_Count * 1.0 / NULLIF(Age_Sample_Total,0) AS Senior_Share,
        Long_Form_GNR_Pct
    FROM FactCommunityProfile
), facility AS (
    SELECT CHSA_Code, COUNT(*) AS Facility_Count
    FROM BridgeFacilityCHSA GROUP BY CHSA_Code
)
SELECT
    c.*,
    COALESCE(f.Facility_Count,0) AS Facility_Count,
    COALESCE(f.Facility_Count,0) * 10000.0 / NULLIF(c.Census_Population,0) AS Facilities_Per_10K
FROM community c LEFT JOIN facility f USING (CHSA_Code);

