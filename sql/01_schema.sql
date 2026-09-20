-- SQLite-compatible analytical star schema.
-- Raw CSV ingestion occurs in Python/Power Query; these tables receive cleaned outputs.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS DimCHSA (
    CHSA_Code TEXT PRIMARY KEY,
    CHSA_Name TEXT NOT NULL,
    Local_Health_Area_Name TEXT,
    Health_Authority_Name TEXT,
    City_Overlap_Share REAL NOT NULL CHECK (City_Overlap_Share BETWEEN 0 AND 1),
    Is_Vancouver_City_Included INTEGER NOT NULL CHECK (Is_Vancouver_City_Included IN (0,1))
);

CREATE TABLE IF NOT EXISTS DimFacility (
    Facility_ID TEXT PRIMARY KEY,
    Facility_Name TEXT NOT NULL,
    ODHF_Facility_Type TEXT,
    Source_Facility_Type TEXT,
    Provider TEXT,
    Latitude REAL,
    Longitude REAL,
    Spatial_Assignment_Status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS FactCommunityProfile (
    CHSA_Code TEXT PRIMARY KEY REFERENCES DimCHSA(CHSA_Code),
    Census_Population INTEGER,
    Age_Sample_Total INTEGER,
    Youth_Count INTEGER,
    Senior_Count INTEGER,
    Long_Form_GNR_Pct REAL,
    Youth_Share REAL,
    Senior_Share REAL,
    Vulnerability_Proxy_Score REAL,
    Data_Blindspot_Score REAL
);

CREATE TABLE IF NOT EXISTS FactFacilitySupply (
    CHSA_Code TEXT PRIMARY KEY REFERENCES DimCHSA(CHSA_Code),
    Facility_Count INTEGER,
    Hospital_Count INTEGER,
    Ambulatory_Count INTEGER,
    Residential_Care_Count INTEGER,
    Facilities_Per_10K REAL,
    Population_Per_Facility REAL,
    Supply_Score REAL,
    Supply_Gap_Score REAL
);

CREATE TABLE IF NOT EXISTS BridgeFacilityCHSA (
    Facility_ID TEXT PRIMARY KEY REFERENCES DimFacility(Facility_ID),
    CHSA_Code TEXT NOT NULL REFERENCES DimCHSA(CHSA_Code)
);

CREATE TABLE IF NOT EXISTS ScenarioAllocation (
    Scenario_Name TEXT NOT NULL,
    CHSA_Code TEXT NOT NULL REFERENCES DimCHSA(CHSA_Code),
    Priority_Score REAL NOT NULL,
    Priority_Rank INTEGER NOT NULL,
    Budget_Allocation REAL NOT NULL,
    Clinical_FTE_Allocation REAL NOT NULL,
    Community_Care_Allocation INTEGER NOT NULL,
    Population_Only_Budget_Allocation REAL NOT NULL,
    Population_Only_Clinical_FTE_Allocation REAL NOT NULL,
    Population_Only_Community_Care_Allocation INTEGER NOT NULL,
    Budget_Difference REAL NOT NULL,
    Clinical_FTE_Difference REAL NOT NULL,
    Community_Care_Difference INTEGER NOT NULL,
    PRIMARY KEY (Scenario_Name, CHSA_Code)
);
