"""Run every numbered pipeline phase in order."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRIPTS=["01_data_understanding.py","02_data_quality.py","03_cleaning.py","04_geospatial.py","05_vulnerability.py","06_resource_allocation.py","build_sqlite.py","07_validation.py"]
for script in SCRIPTS:
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable,str(HERE/script)],check=True,cwd=HERE.parent)
