"""Clean raw attributes without overwriting source files."""
from __future__ import annotations

import pandas as pd
from common import *

def main() -> None:
    ensure_dirs()
    census = read_census()
    facilities = read_facilities()
    text_cols = census.select_dtypes(include=["object","string"]).columns
    for col in text_cols: census[col] = census[col].map(normalize_text)
    id_cols = {"CH_SA_CODE","HLT_A_CODE","HSD_A_CODE","HAUTH_CODE","SH_FRM_DQF","LG_FRM_DFQ","HSDA_ID","HAUTH_ID"}
    for col in census.columns:
        if col not in id_cols and col not in {"CH_SA_NAME","CHSRBRL_CL","HLT_A_NAME","HSD_A_NAME","HAUTH_NAME","SHAPE"}:
            census[col] = pd.to_numeric(census[col], errors="coerce")
    # Source uses 1000 as a non-percentage sentinel in two GNR records; retain the
    # original value and expose a cleaned nullable measure instead of treating it as 1000%.
    source_gnr = census[["SH_FRM_GNR", "LG_FRM_GNR"]].rename(columns=lambda c: f"{c}_SOURCE_VALUE")
    census = pd.concat([census, source_gnr], axis=1).copy()
    for col in ("SH_FRM_GNR", "LG_FRM_GNR"):
        census.loc[~census[col].between(0, 100), col] = pd.NA
    facilities.columns = [c.strip() for c in facilities.columns]
    for col in facilities.columns: facilities[col] = facilities[col].map(normalize_text)
    facilities["province_normalized"] = facilities["province"].str.upper()
    facilities["city_normalized"] = facilities["city"].str.casefold()
    facilities["facility_name_normalized"] = facilities["facility_name"].map(normalize_key)
    facilities["latitude"] = pd.to_numeric(facilities["latitude"], errors="coerce")
    facilities["longitude"] = pd.to_numeric(facilities["longitude"], errors="coerce")
    facilities["source_record_id"] = facilities["index"].astype("string")
    census.to_parquet(PROCESSED / "stg_chsa_census.parquet", index=False)
    facilities.to_parquet(PROCESSED / "stg_odhf_facilities.parquet", index=False)
    print(f"Wrote {len(census)} census rows and {len(facilities)} facility rows")

if __name__ == "__main__": main()
