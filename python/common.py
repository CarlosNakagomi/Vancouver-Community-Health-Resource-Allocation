"""Shared constants and utilities for the VCH Vancouver portfolio pipeline."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import unicodedata

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REFERENCE = ROOT / "data" / "reference"
PROCESSED = ROOT / "data" / "processed"
DQ = ROOT / "outputs" / "data_quality"
ANALYTICAL = ROOT / "outputs" / "analytical"
FIGURES = ROOT / "outputs" / "figures"
DOCS = ROOT / "docs"

CENSUS_PATH = RAW / "BCHACHSAPO.csv"
FACILITY_PATH = RAW / "odhf_bdoes_v1.csv"
CHSA_BOUNDARY_PATH = REFERENCE / "chsa_boundaries_vancouver_lha.geojson"
VANCOUVER_BOUNDARY_PATH = REFERENCE / "vancouver_csd_2016.geojson"
METADATA_PATH = REFERENCE / "BCHACHSAPO_metadata.json"

BUSINESS_QUESTION = (
    "How can Vancouver Coastal Health leverage local\n"
    "socio-demographic population profiles and census non-response rates to predict\n"
    "community vulnerability, and how should we strategically distribute and\n"
    "allocate public healthcare resources—such as clinical staff, operational\n"
    "budgets, and community care services—to address geographic service gaps?"
)

VANCOUVER_CSD_UID = "5915022"
VANCOUVER_OVERLAP_THRESHOLD = 0.50
RETRIEVAL_DATE = "2026-09-18"

DEFAULT_SCENARIO = {
    "name": "Balanced",
    "vulnerability_weight": 0.45,
    "blindspot_weight": 0.25,
    "supply_gap_weight": 0.30,
    "budget": 10_000_000.00,
    "clinical_fte": 50.0,
    "community_care_units": 1_000,
}

SENSITIVITY_SCENARIOS = {
    "Balanced": (0.45, 0.25, 0.30),
    "Need-focused": (0.60, 0.10, 0.30),
    "Uncertainty-aware": (0.35, 0.35, 0.30),
    "Supply-gap-focused": (0.35, 0.15, 0.50),
}

CHA2_RULE = [
    {"BusinessRuleMember": "Downtown Eastside", "SourceCHSAName": "Downtown Eastside", "SourceCHSACode": "3221", "MappingStatus": "Matched"},
    {"BusinessRuleMember": "Strathcona", "SourceCHSAName": None, "SourceCHSACode": None, "MappingStatus": "Not separately represented in 2016 CHSA source"},
    {"BusinessRuleMember": "Grandview-Woodlands", "SourceCHSAName": "Grandview-Woodland", "SourceCHSACode": "3223", "MappingStatus": "Matched after documented spelling normalization"},
]

def ensure_dirs() -> None:
    for path in (PROCESSED, DQ, ANALYTICAL, FIGURES, DOCS):
        path.mkdir(parents=True, exist_ok=True)

def read_census(dtype=str) -> pd.DataFrame:
    return pd.read_csv(CENSUS_PATH, encoding="utf-8-sig", dtype=dtype)

def read_facilities(dtype=str) -> pd.DataFrame:
    return pd.read_csv(FACILITY_PATH, encoding="cp1252", dtype=dtype)

def normalize_text(value: object) -> str | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = unicodedata.normalize("NFKC", str(value)).strip()
    text = re.sub(r"\s+", " ", text)
    return text or None

def normalize_key(value: object) -> str:
    text = normalize_text(value) or ""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def percentile_score(series: pd.Series, higher_is_worse: bool = True) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    pct = values.rank(method="average", pct=True) * 100
    return pct if higher_is_worse else 100 - pct

def allocate_largest_remainder(weights: pd.Series, total: float, decimals: int) -> pd.Series:
    """Allocate exactly to total using largest remainder at the requested precision."""
    scale = 10 ** decimals
    units_total = int(round(total * scale))
    raw = weights / weights.sum() * units_total
    floor = np.floor(raw).astype(int)
    remainder = units_total - int(floor.sum())
    order = (raw - floor).sort_values(ascending=False).index
    floor.loc[order[:remainder]] += 1
    return floor / scale

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")

def load_metadata_map() -> dict[str, dict]:
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if isinstance(metadata, list):
        metadata = metadata[0]
    return {item["short_name"]: item for item in metadata["details"] if item.get("short_name")}
