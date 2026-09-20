CREATE VIEW IF NOT EXISTS vw_CHSA_Analytical AS
SELECT
    d.CHSA_Code, d.CHSA_Name, d.City_Overlap_Share,
    c.Census_Population, c.Youth_Share, c.Senior_Share,
    c.Long_Form_GNR_Pct, c.Vulnerability_Proxy_Score, c.Data_Blindspot_Score,
    s.Facility_Count, s.Facilities_Per_10K, s.Population_Per_Facility,
    s.Supply_Score, s.Supply_Gap_Score
FROM DimCHSA d
JOIN FactCommunityProfile c USING (CHSA_Code)
LEFT JOIN FactFacilitySupply s USING (CHSA_Code);

CREATE VIEW IF NOT EXISTS vw_Allocation AS
SELECT a.*, d.CHSA_Name
FROM ScenarioAllocation a JOIN DimCHSA d USING (CHSA_Code);

