-- Reproducible quality checks after loading the cleaned star schema.
SELECT 'DimCHSA duplicate key' AS check_name, CHSA_Code, COUNT(*) AS issue_count
FROM DimCHSA GROUP BY CHSA_Code HAVING COUNT(*) > 1;

SELECT 'DimFacility duplicate key' AS check_name, Facility_ID, COUNT(*) AS issue_count
FROM DimFacility GROUP BY Facility_ID HAVING COUNT(*) > 1;

SELECT 'Community profile orphan' AS check_name, f.CHSA_Code
FROM FactCommunityProfile f LEFT JOIN DimCHSA d ON d.CHSA_Code=f.CHSA_Code
WHERE d.CHSA_Code IS NULL;

SELECT 'Facility bridge orphan' AS check_name, b.Facility_ID, b.CHSA_Code
FROM BridgeFacilityCHSA b
LEFT JOIN DimFacility f ON f.Facility_ID=b.Facility_ID
LEFT JOIN DimCHSA c ON c.CHSA_Code=b.CHSA_Code
WHERE f.Facility_ID IS NULL OR c.CHSA_Code IS NULL;

SELECT 'Invalid score' AS check_name, CHSA_Code
FROM ScenarioAllocation WHERE Priority_Score NOT BETWEEN 0 AND 100;

