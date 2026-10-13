"""Default Asset Files."""

from pathlib import Path
from typing import Final

SRC: Final = Path(__file__).parents[1]

MATERIAL_DATABASE: Final = SRC / "database" / "material.csv"
PROPELLANT_DATABASE: Final = SRC / "database" / "propellant.csv"
STUDY_CONFIG: Final = SRC / "configs" / "study.json"
PRESSURE_FED_CONFIG: Final = SRC / "configs" / "sizing_study" / "pressure_fed.json"
PUMP_FED_CONFIG: Final = SRC / "configs" / "sizing_study" / "pump_fed.json"
SPECIFICATIONS: Final = SRC / "configs" / "specification.json"
SIZING_STUDY: Final = SRC / "configs" / "sizing_study"
COMPARATIVE_STUDY: Final = SRC / "configs" / "comparative_study"
