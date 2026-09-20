"""Inventory source structure, hashes, grain, and field metadata."""
from __future__ import annotations

import pandas as pd

from common import *

def main() -> None:
    ensure_dirs()
    census = read_census()
    facilities = read_facilities()
    metadata = load_metadata_map()

    source_inventory = pd.DataFrame([
        {"dataset": "BCHACHSAPO", "path": str(CENSUS_PATH.relative_to(ROOT)), "rows": len(census), "columns": len(census.columns), "encoding": "UTF-8", "grain": "One row per 2016 Community Health Service Area", "candidate_primary_key": "CH_SA_CODE", "sha256": sha256(CENSUS_PATH)},
        {"dataset": "ODHF", "path": str(FACILITY_PATH.relative_to(ROOT)), "rows": len(facilities), "columns": len(facilities.columns), "encoding": "Windows-1252", "grain": "One source facility record; multiple providers may describe the same physical site", "candidate_primary_key": "index", "sha256": sha256(FACILITY_PATH)},
    ])
    source_inventory.to_csv(DQ / "source_inventory.csv", index=False)
    repo_rows=[]
    for path in sorted(ROOT.rglob("*")):
        rel=path.relative_to(ROOT)
        if any(part in {".git",".venv","__pycache__",".pytest_cache"} for part in rel.parts) or not path.is_file():
            continue
        top=rel.parts[0]
        role={"data":"data asset","python":"pipeline code","sql":"SQL model","powerbi":"Power BI asset","docs":"documentation","outputs":"generated output","archive":"archived prototype","tests":"automated test"}.get(top,"project configuration")
        repo_rows.append({"path":str(rel),"bytes":path.stat().st_size,"extension":path.suffix.lower(),"role":role})
    pd.DataFrame(repo_rows).to_csv(DQ / "repository_inventory.csv",index=False)

    dictionary_rows = []
    for col in census.columns:
        item = metadata.get(col, {})
        dictionary_rows.append({
            "dataset": "BCHACHSAPO", "physical_column": col,
            "logical_name": item.get("column_name"), "source_type": item.get("data_type"),
            "definition": item.get("column_comments"),
        })
    odhf_definitions = {
        "index": "Source record identifier in ODHF v1",
        "facility_name": "Facility name as supplied by source provider",
        "source_facility_type": "Facility type from the contributing source",
        "odhf_facility_type": "Harmonized ODHF facility category",
        "provider": "Organization that supplied the source record, not necessarily operator/owner",
        "unit": "Unit/suite information where available", "street_no": "Street number",
        "street_name": "Street name", "postal_code": "Postal code", "city": "Reported municipality text",
        "province": "Reported province/territory abbreviation", "source_format_str_address": "Source-formatted address",
        "CSDname": "Census subdivision name where populated", "CSDuid": "Census subdivision unique identifier where populated",
        "Pruid": "Province/territory unique identifier", "latitude": "Latitude in decimal degrees",
        "longitude": "Longitude in decimal degrees",
    }
    for col in facilities.columns:
        dictionary_rows.append({"dataset": "ODHF", "physical_column": col, "logical_name": col, "source_type": "text in CSV; explicitly typed during ETL", "definition": odhf_definitions.get(col, "See ODHF source metadata")})
    pd.DataFrame(dictionary_rows).to_csv(DQ / "source_data_dictionary.csv", index=False)
    print(source_inventory.to_string(index=False))

if __name__ == "__main__":
    main()
