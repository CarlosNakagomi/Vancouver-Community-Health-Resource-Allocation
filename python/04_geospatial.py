"""Apply authoritative city and CHSA point-in-polygon geography."""
from __future__ import annotations

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from common import *

def main() -> None:
    ensure_dirs()
    census = pd.read_parquet(PROCESSED / "stg_chsa_census.parquet")
    facilities = pd.read_parquet(PROCESSED / "stg_odhf_facilities.parquet")
    chsa = gpd.read_file(CHSA_BOUNDARY_PATH).to_crs(3005)
    city = gpd.read_file(VANCOUVER_BOUNDARY_PATH).to_crs(3005)
    city_geom = city.geometry.union_all()
    chsa["CityOverlapShare"] = chsa.geometry.intersection(city_geom).area / chsa.geometry.area
    chsa["VancouverCityIncluded"] = chsa["CityOverlapShare"] >= VANCOUVER_OVERLAP_THRESHOLD
    included = chsa[chsa["VancouverCityIncluded"]].copy()
    included[["CMNTY_HLTH_SERV_AREA_CODE","CMNTY_HLTH_SERV_AREA_NAME","CityOverlapShare","VancouverCityIncluded"]].to_csv(DQ / "chsa_city_overlap.csv", index=False)
    excluded = chsa[~chsa["VancouverCityIncluded"]][["CMNTY_HLTH_SERV_AREA_CODE","CMNTY_HLTH_SERV_AREA_NAME","CityOverlapShare"]]
    excluded.to_csv(DQ / "chsa_excluded_by_city_rule.csv", index=False)

    # Strict textual prefilter required by the project, followed by authoritative city polygon validation.
    candidate = facilities[
        facilities["province_normalized"].eq("BC") &
        facilities["city_normalized"].eq("vancouver") &
        facilities["latitude"].notna() & facilities["longitude"].notna()
    ].copy()
    points = gpd.GeoDataFrame(candidate, geometry=gpd.points_from_xy(candidate.longitude, candidate.latitude), crs=4326).to_crs(3005)
    points["InsideVancouverCSD2016"] = points.geometry.within(city_geom)
    city_points = points[points["InsideVancouverCSD2016"]].copy()
    joined = gpd.sjoin(city_points, included[["CMNTY_HLTH_SERV_AREA_CODE","CMNTY_HLTH_SERV_AREA_NAME","geometry"]], how="left", predicate="within")
    joined["SpatialAssignmentStatus"] = joined["CMNTY_HLTH_SERV_AREA_CODE"].notna().map({True:"Assigned by point-in-polygon",False:"Inside city but not assigned to included CHSA"})
    # A geocoded point can fall a few metres outside a coastal polygon. Apply a
    # documented 25 m boundary tolerance, never a nearest-centroid assignment.
    for idx in joined.index[joined["CMNTY_HLTH_SERV_AREA_CODE"].isna()]:
        distances = included.geometry.distance(joined.at[idx, "geometry"])
        nearest_idx = distances.idxmin()
        if float(distances.loc[nearest_idx]) <= 25:
            joined.at[idx, "CMNTY_HLTH_SERV_AREA_CODE"] = included.at[nearest_idx, "CMNTY_HLTH_SERV_AREA_CODE"]
            joined.at[idx, "CMNTY_HLTH_SERV_AREA_NAME"] = included.at[nearest_idx, "CMNTY_HLTH_SERV_AREA_NAME"]
            joined.at[idx, "SpatialAssignmentStatus"] = "Assigned to nearest polygon edge within 25 m tolerance"
    joined = joined.drop(columns=[c for c in ["index_right"] if c in joined.columns])
    joined = joined.to_crs(4326)

    # Canonicalize apparent duplicate physical records conservatively; retain a traceable source-record list.
    joined["coord_key"] = joined["latitude"].round(4).astype(str) + "|" + joined["longitude"].round(4).astype(str)
    joined["canonical_key"] = joined["facility_name_normalized"] + "|" + joined["coord_key"]
    joined["CanonicalFacilityID"] = "FAC-" + joined.groupby("canonical_key", dropna=False).ngroup().add(1).astype(str).str.zfill(4)
    source_map = joined[["source_record_id","CanonicalFacilityID","canonical_key"]].copy()
    source_map.to_csv(PROCESSED / "bridge_facility_source_record.csv", index=False)
    canonical = joined.sort_values("source_record_id").drop_duplicates("CanonicalFacilityID").copy()
    canonical["SourceRecordCount"] = joined.groupby("CanonicalFacilityID")["source_record_id"].transform("count")
    canonical.drop(columns=["geometry","coord_key","canonical_key"], errors="ignore").to_csv(PROCESSED / "dim_facility.csv", index=False)
    joined.drop(columns=["geometry"], errors="ignore").to_csv(PROCESSED / "facility_spatial_assignments.csv", index=False)
    included.to_crs(4326).to_file(PROCESSED / "vancouver_chsa_boundaries.geojson", driver="GeoJSON")
    print(f"{len(candidate)} text-filtered candidates; {len(city_points)} inside Vancouver CSD; {len(canonical)} canonical facilities")

if __name__ == "__main__": main()
