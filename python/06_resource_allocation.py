"""Create facility-supply metrics, priority scenarios, and reconciled allocations."""
from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from common import *

def main() -> None:
    community = pd.read_csv(PROCESSED / "fact_community_profile.csv", dtype={"CH_SA_CODE":str})
    facilities = pd.read_csv(PROCESSED / "dim_facility.csv", dtype={"CMNTY_HLTH_SERV_AREA_CODE":str})
    supply = facilities.groupby(["CMNTY_HLTH_SERV_AREA_CODE","odhf_facility_type"], dropna=False).size().unstack(fill_value=0)
    supply["FacilityCount"] = supply.sum(axis=1)
    supply = supply.reset_index()
    df = community.merge(supply, left_on="CH_SA_CODE", right_on="CMNTY_HLTH_SERV_AREA_CODE", how="left", validate="one_to_one")
    for c in ["Hospitals","Ambulatory health care services","Nursing and residential care facilities","FacilityCount"]:
        if c not in df: df[c]=0
        df[c]=df[c].fillna(0).astype(int)
    df["FacilitiesPer10K"] = df["FacilityCount"] / df["CHSPOP_CEN"] * 10000
    df["PopulationPerFacility"] = df["CHSPOP_CEN"] / df["FacilityCount"].replace(0,pd.NA)
    df["HealthcareSupplyScore"] = percentile_score(df["FacilitiesPer10K"], higher_is_worse=True).round(2)
    # Higher score means a larger relative supply gap.
    df["HealthcareSupplyGapScore"] = percentile_score(df["FacilitiesPer10K"], higher_is_worse=False).round(2)
    sensitivity=[]
    for name,(wv,wb,ws) in SENSITIVITY_SCENARIOS.items():
        score=(wv*df["CommunityVulnerabilityProxyScore"]+wb*df["DataBlindspotScore"]+ws*df["HealthcareSupplyGapScore"]).round(2)
        rank=score.rank(method="min",ascending=False).astype(int)
        df[f"PriorityScore_{name}"]=score; df[f"PriorityRank_{name}"]=rank
    base_rank=df["PriorityRank_Balanced"]
    for name in SENSITIVITY_SCENARIOS:
        corr=float(spearmanr(base_rank,df[f"PriorityRank_{name}"]).statistic)
        for _,r in df.iterrows(): sensitivity.append({"Scenario":name,"CHSA_Code":r.CH_SA_CODE,"CHSA_Name":r.CH_SA_NAME,"PriorityScore":r[f"PriorityScore_{name}"],"PriorityRank":r[f"PriorityRank_{name}"],"SpearmanVsBalanced":corr})
    pd.DataFrame(sensitivity).to_csv(ANALYTICAL / "sensitivity_analysis.csv",index=False)
    df["ResourcePriorityScore"] = df["PriorityScore_Balanced"]
    df["PriorityRank"] = df["PriorityRank_Balanced"]
    priority_share = df["ResourcePriorityScore"] / df["ResourcePriorityScore"].sum()
    population_share = df["CHSPOP_CEN"] / df["CHSPOP_CEN"].sum()
    df["AllocationWeight"] = 0.60*population_share + 0.40*priority_share
    df["ScenarioBudgetAllocation"] = allocate_largest_remainder(df["AllocationWeight"], DEFAULT_SCENARIO["budget"], 2)
    df["ScenarioClinicalFTEAllocation"] = allocate_largest_remainder(df["AllocationWeight"], DEFAULT_SCENARIO["clinical_fte"], 1)
    df["ScenarioCommunityCareAllocation"] = allocate_largest_remainder(df["AllocationWeight"], DEFAULT_SCENARIO["community_care_units"], 0).astype(int)
    df["PopulationOnlyBudgetAllocation"] = allocate_largest_remainder(population_share, DEFAULT_SCENARIO["budget"], 2)
    df["PopulationOnlyClinicalFTEAllocation"] = allocate_largest_remainder(population_share, DEFAULT_SCENARIO["clinical_fte"], 1)
    df["PopulationOnlyCommunityCareAllocation"] = allocate_largest_remainder(population_share, DEFAULT_SCENARIO["community_care_units"], 0).astype(int)
    df["BudgetDifference"] = df["ScenarioBudgetAllocation"] - df["PopulationOnlyBudgetAllocation"]
    df["ClinicalFTEDifference"] = df["ScenarioClinicalFTEAllocation"] - df["PopulationOnlyClinicalFTEAllocation"]
    df["CommunityCareDifference"] = df["ScenarioCommunityCareAllocation"] - df["PopulationOnlyCommunityCareAllocation"]
    df.to_csv(ANALYTICAL / "community_priority_and_allocation.csv",index=False)
    df[["CH_SA_CODE","CH_SA_NAME","FacilityCount","Hospitals","Ambulatory health care services","Nursing and residential care facilities","FacilitiesPer10K","PopulationPerFacility","HealthcareSupplyScore","HealthcareSupplyGapScore"]].to_csv(PROCESSED / "fact_facility_supply.csv",index=False)
    analysis_cols=["CHSPOP_CEN","YouthShare","SeniorShare","LG_FRM_GNR","FacilityCount","FacilitiesPer10K","CommunityVulnerabilityProxyScore","DataBlindspotScore","HealthcareSupplyGapScore","ResourcePriorityScore"]
    df[analysis_cols].describe().T.to_csv(ANALYTICAL/"descriptive_statistics.csv")
    df[analysis_cols].corr(method="spearman").to_csv(ANALYTICAL/"spearman_correlations.csv")
    z=(df[analysis_cols]-df[analysis_cols].mean())/df[analysis_cols].std(ddof=0)
    outliers=[]
    for col in analysis_cols:
        for idx in z.index[z[col].abs()>=2]: outliers.append({"CHSA_Code":df.at[idx,"CH_SA_CODE"],"CHSA_Name":df.at[idx,"CH_SA_NAME"],"Metric":col,"Value":df.at[idx,col],"ZScore":z.at[idx,col]})
    pd.DataFrame(outliers).to_csv(ANALYTICAL/"outlier_analysis.csv",index=False)

    sns.set_theme(style="whitegrid")
    ranked=df.sort_values("ResourcePriorityScore")
    fig,ax=plt.subplots(figsize=(10,7)); ax.barh(ranked.CH_SA_NAME,ranked.ResourcePriorityScore,color="#087b82"); ax.set(xlabel="Resource Priority Score (0–100)",ylabel="",title="Vancouver CHSA resource-priority scenario"); fig.tight_layout(); fig.savefig(FIGURES/"resource_priority_ranking.png",dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,6)); size=(df.CHSPOP_CEN/df.CHSPOP_CEN.max())*900+80; sc=ax.scatter(df.FacilitiesPer10K,df.CommunityVulnerabilityProxyScore,s=size,c=df.DataBlindspotScore,cmap="viridis",alpha=.8,edgecolor="white");
    for _,r in df.nlargest(5,"ResourcePriorityScore").iterrows(): ax.annotate(r.CH_SA_NAME,(r.FacilitiesPer10K,r.CommunityVulnerabilityProxyScore),xytext=(5,4),textcoords="offset points",fontsize=8)
    ax.set(xlabel="Facilities per 10,000 population (count, not capacity)",ylabel="Community Vulnerability Proxy Score",title="Age-structure proxy, facility supply, and census uncertainty"); fig.colorbar(sc,ax=ax,label="Data Blindspot Score"); fig.tight_layout(); fig.savefig(FIGURES/"vulnerability_supply_scatter.png",dpi=180); plt.close(fig)
    print(df.sort_values("PriorityRank")[["CH_SA_CODE","CH_SA_NAME","ResourcePriorityScore","PriorityRank","ScenarioBudgetAllocation"]].head(10).to_string(index=False))

if __name__ == "__main__": main()
