"""Generate machine-readable data quality profiles for both raw datasets."""
from __future__ import annotations

import json
import pandas as pd

from common import *

def profile(df: pd.DataFrame, dataset: str, key: str) -> tuple[pd.DataFrame, dict]:
    rows = []
    for col in df.columns:
        numeric = pd.to_numeric(df[col], errors="coerce")
        numeric_count = int(numeric.notna().sum())
        rows.append({
            "dataset": dataset, "column": col, "rows": len(df),
            "inferred_type": "numeric" if numeric_count == df[col].notna().sum() and numeric_count else "text",
            "non_null_count": int(df[col].notna().sum()), "null_count": int(df[col].isna().sum()),
            "null_pct": round(float(df[col].isna().mean() * 100), 4),
            "unique_count": int(df[col].nunique(dropna=True)),
            "min_numeric": float(numeric.min()) if numeric_count else None,
            "max_numeric": float(numeric.max()) if numeric_count else None,
            "sample_values": " | ".join(df[col].dropna().astype(str).drop_duplicates().head(5)),
        })
    summary = {
        "dataset": dataset, "row_count": len(df), "column_count": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()), "candidate_key": key,
        "duplicate_candidate_keys": int(df[key].duplicated(keep=False).sum()),
        "null_candidate_keys": int(df[key].isna().sum()),
    }
    return pd.DataFrame(rows), summary

def main() -> None:
    ensure_dirs()
    census = read_census()
    facilities = read_facilities()
    a_cols, a_summary = profile(census, "BCHACHSAPO", "CH_SA_CODE")
    b_cols, b_summary = profile(facilities, "ODHF", "index")
    pd.concat([a_cols, b_cols], ignore_index=True).to_csv(DQ / "column_profile.csv", index=False)

    numeric_cols = [c for c in census.columns if c not in {"CH_SA_CODE","HLT_A_CODE","HSD_A_CODE","HAUTH_CODE","SH_FRM_DQF","LG_FRM_DFQ","HSDA_ID","HAUTH_ID","CH_SA_NAME","CHSRBRL_CL","HLT_A_NAME","HSD_A_NAME","HAUTH_NAME","SHAPE"}]
    census_numeric = census[numeric_cols].apply(pd.to_numeric, errors="coerce")
    impossible = {
        "negative_census_values": int((census_numeric < 0).sum().sum()),
        "gnr_outside_0_100": int(((pd.to_numeric(census["LG_FRM_GNR"], errors="coerce") < 0) | (pd.to_numeric(census["LG_FRM_GNR"], errors="coerce") > 100)).sum()),
        "youth_gt_age_total": int((pd.to_numeric(census["0_14_A_TTL"], errors="coerce") > pd.to_numeric(census["GRP_A_TTL"], errors="coerce")).sum()),
    }
    lat = pd.to_numeric(facilities["latitude"], errors="coerce")
    lon = pd.to_numeric(facilities["longitude"], errors="coerce")
    invalid_coordinates = int(((lat.notna() & ~lat.between(-90,90)) | (lon.notna() & ~lon.between(-180,180)) | (lat.isna() ^ lon.isna())).sum())
    vancouver_text = facilities["province"].str.strip().str.upper().eq("BC") & facilities["city"].str.strip().str.casefold().eq("vancouver")
    issues = {
        "BCHACHSAPO": {**a_summary, **impossible, "health_authority_distribution": census["HAUTH_NAME"].value_counts(dropna=False).to_dict(), "source_suppression_note": "Counts are subject to Statistics Canada random rounding. Two long-form GNR values use 1000 outside the valid 0-100 range and are accompanied by DQF flags; cleaned GNR converts them to null while retaining source values."},
        "ODHF": {**b_summary, "missing_coordinate_pairs": int((lat.isna() & lon.isna()).sum()), "invalid_coordinate_rows": invalid_coordinates, "reported_BC_Vancouver_rows": int(vancouver_text.sum()), "reported_BC_Vancouver_with_coordinates": int((vancouver_text & lat.notna() & lon.notna()).sum()), "facility_type_distribution": facilities["odhf_facility_type"].fillna("<NULL>").value_counts().to_dict(), "join_warning": "CSDuid is sparsely populated; city text alone is not a defensible city boundary test. Use coordinate point-in-polygon."},
    }
    write_json(DQ / "dataset_quality_summary.json", issues)
    for name, frame in (("census_categorical_distributions", census[["CHSRBRL_CL","HLT_A_NAME","HSD_A_NAME","HAUTH_NAME"]]), ("facility_categorical_distributions", facilities[["odhf_facility_type","province","city","provider"]])):
        out=[]
        for col in frame.columns:
            for value,count in frame[col].fillna("<NULL>").value_counts().items(): out.append({"column":col,"value":value,"count":int(count)})
        pd.DataFrame(out).to_csv(DQ / f"{name}.csv", index=False)
    print(json.dumps(issues, indent=2))

if __name__ == "__main__":
    main()
