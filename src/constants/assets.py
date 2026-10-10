"""Default Asset Files."""

from pathlib import Path
from typing import Final

SRC: Final = Path(__file__).parents[1]

MATERIAL_DATABASE: Final = SRC / "database" / "material.csv"
PROPELLANT_DATABASE: Final = SRC / "database" / "propellant.csv"
STUDY_CONFIG: Final = SRC / "configs" / "study.json"
PRESSURE_FED_CONFIG: Final = SRC / "configs" / "pressure_fed.json"
PUMP_FED_CONFIG: Final = SRC / "configs" / "pump_fed.json"
