"""Automated acceptance checks for the analytical pipeline."""
from __future__ import annotations

import json
import pandas as pd
from common import *

def check(name: str, condition: bool, detail: str) -> dict:
    return {"test":name,"status":"PASS" if bool(condition) else "FAIL","detail":detail}

def main() -> None:
    c=pd.read_csv(PROCESSED/"fact_community_profile.csv",dtype={"CH_SA_CODE":str})
    f=pd.read_csv(PROCESSED/"dim_facility.csv",dtype={"CMNTY_HLTH_SERV_AREA_CODE":str})
    a=pd.read_csv(ANALYTICAL/"community_priority_and_allocation.csv",dtype={"CH_SA_CODE":str})
    s=pd.read_csv(ANALYTICAL/"sensitivity_analysis.csv",dtype={"CHSA_Code":str})
    tests=[
        check("Vancouver CHSA count",len(c)==19,f"expected 19, found {len(c)}"),
        check("CHSA primary key unique",c.CH_SA_CODE.is_unique,"CH_SA_CODE unique"),
        check("UBC excluded","3243" not in set(c.CH_SA_CODE),"CHSA 3243 is outside Vancouver CSD"),
        check("Partial boundary flagged",float(c.loc[c.CH_SA_CODE=="3242","CityOverlapShare"].iloc[0])<0.90,"CHSA 3242 overlap below 90%"),
        check("Facility key unique",f.CanonicalFacilityID.is_unique,"CanonicalFacilityID unique"),
        check("Facility referential integrity",f.CMNTY_HLTH_SERV_AREA_CODE.dropna().isin(c.CH_SA_CODE).all(),"all mapped facility CHSAs exist"),
        check("No null spatial assignments",f.CMNTY_HLTH_SERV_AREA_CODE.notna().all(),f"null assignments={f.CMNTY_HLTH_SERV_AREA_CODE.isna().sum()}"),
        check("Score ranges",a[["CommunityVulnerabilityProxyScore","DataBlindspotScore","HealthcareSupplyGapScore","ResourcePriorityScore"]].apply(lambda x:x.between(0,100)).all().all(),"all scores 0-100"),
        check("Budget reconciles",abs(a.ScenarioBudgetAllocation.sum()-DEFAULT_SCENARIO["budget"])<0.005,f"sum={a.ScenarioBudgetAllocation.sum():.2f}"),
        check("Clinical FTE reconciles",abs(a.ScenarioClinicalFTEAllocation.sum()-DEFAULT_SCENARIO["clinical_fte"])<0.05,f"sum={a.ScenarioClinicalFTEAllocation.sum():.1f}"),
        check("Community care reconciles",int(a.ScenarioCommunityCareAllocation.sum())==DEFAULT_SCENARIO["community_care_units"],f"sum={a.ScenarioCommunityCareAllocation.sum()}"),
        check("Sensitivity complete",len(s)==19*len(SENSITIVITY_SCENARIOS),f"rows={len(s)}"),
        check("Population total stable",int(c.CHSPOP_CEN.sum())==663894,f"2016 source total across 19 included CHSAs={int(c.CHSPOP_CEN.sum())}"),
    ]
    out=pd.DataFrame(tests); out.to_csv(DQ/"validation_results.csv",index=False)
    write_json(DQ/"validation_summary.json",{"passed":int((out.status=="PASS").sum()),"failed":int((out.status=="FAIL").sum()),"tests":tests})
    print(out.to_string(index=False))
    if (out.status=="FAIL").any(): raise SystemExit(1)

if __name__ == "__main__": main()
