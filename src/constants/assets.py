"""Default Asset Files."""

from pathlib import Path

SRC = Path(__file__).parents[1]

MATERIAL_DATABASE = SRC / "database" / "material.csv"
PROPELLANT_DATABASE = SRC / "database" / "propellant.csv"
STUDY_CONFIG = SRC / "configs" / "study.json"
