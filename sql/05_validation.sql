-- Expected values are source-version controls for the committed raw files.
SELECT CASE WHEN COUNT(*)=19 THEN 'PASS' ELSE 'FAIL' END AS Vancouver_CHSA_Count
FROM DimCHSA WHERE Is_Vancouver_City_Included=1;

SELECT CASE WHEN ABS(SUM(Budget_Allocation)-10000000.00)<0.01 THEN 'PASS' ELSE 'FAIL' END AS Budget_Reconciliation,
       CASE WHEN ABS(SUM(Clinical_FTE_Allocation)-50.0)<0.05 THEN 'PASS' ELSE 'FAIL' END AS FTE_Reconciliation,
       CASE WHEN SUM(Community_Care_Allocation)=1000 THEN 'PASS' ELSE 'FAIL' END AS Community_Care_Reconciliation,
       CASE WHEN ABS(SUM(Population_Only_Budget_Allocation)-10000000.00)<0.01 THEN 'PASS' ELSE 'FAIL' END AS Population_Only_Budget_Reconciliation,
       CASE WHEN ABS(SUM(Population_Only_Clinical_FTE_Allocation)-50.0)<0.05 THEN 'PASS' ELSE 'FAIL' END AS Population_Only_FTE_Reconciliation,
       CASE WHEN SUM(Population_Only_Community_Care_Allocation)=1000 THEN 'PASS' ELSE 'FAIL' END AS Population_Only_Community_Care_Reconciliation
FROM ScenarioAllocation WHERE Scenario_Name='Balanced';

SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS Referential_Integrity
FROM BridgeFacilityCHSA b
LEFT JOIN DimFacility f ON f.Facility_ID=b.Facility_ID
LEFT JOIN DimCHSA c ON c.CHSA_Code=b.CHSA_Code
WHERE f.Facility_ID IS NULL OR c.CHSA_Code IS NULL;
