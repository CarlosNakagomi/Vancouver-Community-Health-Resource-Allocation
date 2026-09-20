"""Materialize the documented star schema as a portable SQLite database."""
from __future__ import annotations
import sqlite3
import pandas as pd
from common import *

def main() -> None:
    db=ANALYTICAL/"vch_vancouver_allocation.sqlite"
    if db.exists(): db.unlink()
    con=sqlite3.connect(db)
    con.executescript((ROOT/"sql"/"01_schema.sql").read_text(encoding="utf-8"))
    census=pd.read_parquet(PROCESSED/"stg_chsa_census.parquet")
    profile=pd.read_csv(PROCESSED/"fact_community_profile.csv",dtype={"CH_SA_CODE":str})
    supply=pd.read_csv(PROCESSED/"fact_facility_supply.csv",dtype={"CH_SA_CODE":str})
    fac=pd.read_csv(PROCESSED/"dim_facility.csv",dtype={"CMNTY_HLTH_SERV_AREA_CODE":str})
    alloc=pd.read_csv(ANALYTICAL/"community_priority_and_allocation.csv",dtype={"CH_SA_CODE":str})
    chsa=profile[["CH_SA_CODE","CH_SA_NAME","CityOverlapShare"]].merge(census[["CH_SA_CODE","HLT_A_NAME","HAUTH_NAME"]],on="CH_SA_CODE",validate="one_to_one")
    con.executemany("INSERT INTO DimCHSA VALUES (?,?,?,?,?,?)",[(r.CH_SA_CODE,r.CH_SA_NAME,r.HLT_A_NAME,r.HAUTH_NAME,min(1.0,max(0.0,float(r.CityOverlapShare))),1) for r in chsa.itertuples()])
    con.executemany("INSERT INTO FactCommunityProfile VALUES (?,?,?,?,?,?,?,?,?,?)",[(r["CH_SA_CODE"],int(r["CHSPOP_CEN"]),int(r["GRP_A_TTL"]),int(r["0_14_A_TTL"]),int(r["65PLS_A_TL"]),float(r["LG_FRM_GNR"]),float(r["YouthShare"]),float(r["SeniorShare"]),float(r["CommunityVulnerabilityProxyScore"]),float(r["DataBlindspotScore"])) for _,r in profile.iterrows()])
    con.executemany("INSERT INTO FactFacilitySupply VALUES (?,?,?,?,?,?,?,?,?)",[(r["CH_SA_CODE"],int(r["FacilityCount"]),int(r["Hospitals"]),int(r["Ambulatory health care services"]),int(r["Nursing and residential care facilities"]),float(r["FacilitiesPer10K"]),None if pd.isna(r["PopulationPerFacility"]) else float(r["PopulationPerFacility"]),float(r["HealthcareSupplyScore"]),float(r["HealthcareSupplyGapScore"])) for _,r in supply.iterrows()])
    for r in fac.itertuples():
        con.execute("INSERT INTO DimFacility VALUES (?,?,?,?,?,?,?,?)",(r.CanonicalFacilityID,r.facility_name,r.odhf_facility_type,r.source_facility_type,r.provider,float(r.latitude),float(r.longitude),r.SpatialAssignmentStatus))
        con.execute("INSERT INTO BridgeFacilityCHSA VALUES (?,?)",(r.CanonicalFacilityID,r.CMNTY_HLTH_SERV_AREA_CODE))
    con.executemany(
        "INSERT INTO ScenarioAllocation VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                "Balanced", r.CH_SA_CODE, float(r.ResourcePriorityScore), int(r.PriorityRank),
                float(r.ScenarioBudgetAllocation), float(r.ScenarioClinicalFTEAllocation), int(r.ScenarioCommunityCareAllocation),
                float(r.PopulationOnlyBudgetAllocation), float(r.PopulationOnlyClinicalFTEAllocation), int(r.PopulationOnlyCommunityCareAllocation),
                float(r.BudgetDifference), float(r.ClinicalFTEDifference), int(r.CommunityCareDifference),
            )
            for r in alloc.itertuples()
        ],
    )
    con.executescript((ROOT/"sql"/"04_analytical_views.sql").read_text(encoding="utf-8"))
    con.commit(); con.close(); print(f"Wrote {db}")

if __name__ == "__main__": main()
