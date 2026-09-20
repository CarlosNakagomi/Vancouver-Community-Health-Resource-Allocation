"""Build and validate the Power BI CHSA Shape Map topology."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "vancouver_chsa_boundaries.geojson"
OUTPUT = ROOT / "data" / "processed" / "vancouver_chsa_boundaries.topojson"
PROFILE = ROOT / "data" / "processed" / "fact_community_profile.csv"
OBJECT_NAME = "vancouver_chsa_boundaries"
CODE_PROPERTY = "CMNTY_HLTH_SERV_AREA_CODE"
NAME_PROPERTY = "CMNTY_HLTH_SERV_AREA_NAME"


def add_ring(arcs, ring):
    arcs.append(ring)
    return [len(arcs) - 1]


def main():
    feature_collection = json.loads(SOURCE.read_text(encoding="utf-8"))
    arcs = []
    geometries = []

    for feature in feature_collection["features"]:
        geometry = feature["geometry"]
        geometry_type = geometry["type"]

        if geometry_type == "Polygon":
            geometry_arcs = [add_ring(arcs, ring) for ring in geometry["coordinates"]]
        elif geometry_type == "MultiPolygon":
            geometry_arcs = [
                [add_ring(arcs, ring) for ring in polygon]
                for polygon in geometry["coordinates"]
            ]
        else:
            raise ValueError(f"Unsupported geometry type: {geometry_type}")

        properties = feature["properties"]
        geometries.append(
            {
                "type": geometry_type,
                "id": str(properties[CODE_PROPERTY]),
                "properties": properties,
                "arcs": geometry_arcs,
            }
        )

    x_values = [position[0] for arc in arcs for position in arc]
    y_values = [position[1] for arc in arcs for position in arc]
    topology = {
        "type": "Topology",
        "bbox": [min(x_values), min(y_values), max(x_values), max(y_values)],
        "objects": {
            OBJECT_NAME: {"type": "GeometryCollection", "geometries": geometries}
        },
        "arcs": arcs,
    }
    OUTPUT.write_text(
        json.dumps(topology, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with PROFILE.open(encoding="utf-8-sig", newline="") as profile_file:
        dim_codes = {row["CH_SA_CODE"] for row in csv.DictReader(profile_file)}
    topology_codes = {str(item["properties"][CODE_PROPERTY]) for item in geometries}

    assert topology["type"] == "Topology"
    assert len(geometries) == 19
    assert len(topology_codes) == 19
    assert topology_codes == dim_codes
    assert all(item["properties"].get(NAME_PROPERTY) for item in geometries)
    assert all(item["type"] in {"Polygon", "MultiPolygon"} for item in geometries)

    print(f"object={OBJECT_NAME}")
    print(f"code_property={CODE_PROPERTY}")
    print(f"name_property={NAME_PROPERTY}")
    print(f"geometries={len(geometries)}")
    print("code_match=PASS")
    print("validation=PASS")


if __name__ == "__main__":
    main()
