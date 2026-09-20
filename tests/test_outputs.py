from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def test_core_outputs_exist():
    for rel in ["data/processed/fact_community_profile.csv","data/processed/dim_facility.csv","outputs/analytical/community_priority_and_allocation.csv","outputs/analytical/vch_vancouver_allocation.sqlite"]:
        assert (ROOT/rel).exists(), rel

def test_allocation_reconciles():
    df=pd.read_csv(ROOT/"outputs/analytical/community_priority_and_allocation.csv")
    assert round(df.ScenarioBudgetAllocation.sum(),2)==10_000_000.00
    assert round(df.ScenarioClinicalFTEAllocation.sum(),1)==50.0
    assert int(df.ScenarioCommunityCareAllocation.sum())==1000
    assert round(df.PopulationOnlyBudgetAllocation.sum(),2)==10_000_000.00
    assert round(df.PopulationOnlyClinicalFTEAllocation.sum(),1)==50.0
    assert int(df.PopulationOnlyCommunityCareAllocation.sum())==1000
    northeast_false_creek=df.loc[df.CH_SA_CODE.astype(str)=="3222"].iloc[0]
    assert round(northeast_false_creek.BudgetDifference,2)==160_656.11

def test_geography_and_keys():
    c=pd.read_csv(ROOT/"data/processed/fact_community_profile.csv",dtype={"CH_SA_CODE":str})
    f=pd.read_csv(ROOT/"data/processed/dim_facility.csv",dtype={"CMNTY_HLTH_SERV_AREA_CODE":str})
    assert len(c)==19 and c.CH_SA_CODE.is_unique and "3243" not in set(c.CH_SA_CODE)
    assert f.CanonicalFacilityID.is_unique
    assert f.CMNTY_HLTH_SERV_AREA_CODE.isin(c.CH_SA_CODE).all()

def test_sensitivity_robustness():
    s=pd.read_csv(ROOT/"outputs/analytical/sensitivity_analysis.csv",dtype={"CHSA_Code":str})
    assert len(s)==76
    top_five=s.assign(IsTopFive=s.PriorityRank<=5).groupby("CHSA_Name").IsTopFive.sum()
    for name in ["Sunset","West Point Grey/Dunbar-Southlands","Oakridge/Marpole"]:
        assert int(top_five[name])==4
    sunset=s.loc[s.CHSA_Name=="Sunset","PriorityRank"]
    assert sunset.between(1,2).all()

def test_validation_controls():
    v=pd.read_csv(ROOT/"outputs/data_quality/validation_results.csv")
    assert int((v.status=="PASS").sum())==13
    assert int((v.status=="FAIL").sum())==0
