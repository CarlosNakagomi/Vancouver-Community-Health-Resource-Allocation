// Vancouver Coastal Health portfolio — display-name cleanup
// Target: Tabular Editor 2 Advanced Scripting
// Scope: semantic names and report-view visibility only.
// This script does not change source columns, Power Query, relationships, data,
// keys, or calculation logic.

var renameColumns = new Dictionary<string, Dictionary<string, string>>
{
    { "DimCHSA", new Dictionary<string, string>
        {
            { "CHSA Code", "CHSA Code" },
            { "CHSA Name", "CHSA Name" },
            { "City Overlap Share", "City Overlap Share" }
        }
    },
    { "DimFacility", new Dictionary<string, string>
        {
            { "CanonicalFacilityID", "Facility ID" },
            { "facility_name", "Facility Name" },
            { "odhf_facility_type", "Facility Type" },
            { "provider", "Provider" },
            { "unit", "Unit" },
            { "street_no", "Street Number" },
            { "street_name", "Street Name" },
            { "postal_code", "Postal Code" },
            { "city", "City" },
            { "province", "Province" },
            { "source_format_str_address", "Street Address" },
            { "latitude", "Latitude" },
            { "longitude", "Longitude" },
            { "CMNTY_HLTH_SERV_AREA_CODE", "CHSA Code" },
            { "CMNTY_HLTH_SERV_AREA_NAME", "CHSA Name" },
            { "SourceRecordCount", "Source Record Count" }
        }
    },
    { "FactCommunityProfile", new Dictionary<string, string>
        {
            { "CH_SA_CODE", "CHSA Code" },
            { "CH_SA_NAME", "CHSA Name" },
            { "CHSPOP_CEN", "Population" },
            { "GRP_A_TTL", "Age Sample Population" },
            { "0_14_A_TTL", "Population Age 0–14" },
            { "65PLS_A_TL", "Population Age 65+" },
            { "LG_FRM_GNR", "Long-Form GNR" },
            { "YouthShare", "Youth Share" },
            { "SeniorShare", "Senior Share" },
            { "AgeDependencyShare", "Age Dependency Share" },
            { "YouthPercentile", "Youth Percentile" },
            { "SeniorPercentile", "Senior Percentile" },
            { "CommunityVulnerabilityProxyScore", "Vulnerability Proxy Score" },
            { "DataBlindspotScore", "Data Blindspot Score" },
            { "GNRRiskBand", "GNR Risk Band" },
            { "CityOverlapShare", "City Overlap Share" }
        }
    },
    { "FactFacilitySupply", new Dictionary<string, string>
        {
            { "CH_SA_CODE", "CHSA Code" },
            { "CH_SA_NAME", "CHSA Name" },
            { "FacilityCount", "Facility Count" },
            { "Hospitals", "Hospitals" },
            { "Ambulatory health care services", "Ambulatory Care Facilities" },
            { "Nursing and residential care facilities", "Nursing and Residential Care Facilities" },
            { "FacilitiesPer10K", "Facilities per 10K Population" },
            { "PopulationPerFacility", "Population per Facility" },
            { "HealthcareSupplyScore", "Healthcare Supply Score" },
            { "HealthcareSupplyGapScore", "Healthcare Supply Gap Score" }
        }
    },
    { "FactAllocationScenario", new Dictionary<string, string>
        {
            { "CH_SA_CODE", "CHSA Code" },
            { "ResourcePriorityScore", "Resource Priority Score" },
            { "PriorityRank", "Priority Rank" },
            { "AllocationWeight", "Allocation Weight" },
            { "ScenarioBudgetAllocation", "Scenario Budget Allocation" },
            { "ScenarioClinicalFTEAllocation", "Scenario Clinical FTE Allocation" },
            { "ScenarioCommunityCareAllocation", "Scenario Community Care Allocation" },
            { "Scenario", "Scenario" }
        }
    }
};

foreach (var tableEntry in renameColumns)
{
    var table = Model.Tables.FirstOrDefault(t => t.Name == tableEntry.Key);
    if (table == null) continue;

    foreach (var rename in tableEntry.Value)
    {
        var column = table.Columns.FirstOrDefault(c => c.Name == rename.Key);
        if (column != null && column.Name != rename.Value)
            column.Name = rename.Value;
    }
}

// Hide only report-irrelevant technical fields. Relationship and map fields,
// including every CHSA key plus latitude/longitude, remain visible.
var hideColumns = new Dictionary<string, string[]>
{
    { "DimFacility", new[]
        {
            "index",
            "source_facility_type",
            "CSDname",
            "CSDuid",
            "Pruid",
            "province_normalized",
            "city_normalized",
            "facility_name_normalized",
            "source_record_id",
            "InsideVancouverCSD2016",
            "SpatialAssignmentStatus",
            "Source Record Count",
            "Placeholder"
        }
    }
};

foreach (var tableEntry in hideColumns)
{
    var table = Model.Tables.FirstOrDefault(t => t.Name == tableEntry.Key);
    if (table == null) continue;

    foreach (var columnName in tableEntry.Value)
    {
        var column = table.Columns.FirstOrDefault(c => c.Name == columnName);
        if (column != null) column.IsHidden = true;
    }
}

// Validation/reconciliation measures are retained but removed from report view.
var measuresTable = Model.Tables.FirstOrDefault(t => t.Name == "_Measures");
if (measuresTable != null)
{
    var hiddenMeasures = new[]
    {
        "Budget Reconciliation",
        "Clinical FTE Reconciliation",
        "Community Care Reconciliation"
    };

    foreach (var measureName in hiddenMeasures)
    {
        var measure = measuresTable.Measures.FirstOrDefault(m => m.Name == measureName);
        if (measure != null) measure.IsHidden = true;
    }
}

Info("Display-name cleanup complete. Review changes, then save manually if approved.");
