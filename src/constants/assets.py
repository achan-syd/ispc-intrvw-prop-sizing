"""Default Asset Files."""

from pathlib import Path
from typing import Final

SRC: Final = Path(__file__).parents[1]
CONFIGS: Final = SRC / "configs"

MATERIAL_DATABASE: Final = SRC / "database" / "material.csv"
PROPELLANT_DATABASE: Final = SRC / "database" / "propellant.csv"
SPECIFICATIONS: Final = CONFIGS / "specification.json"
SIZING_STUDY: Final = CONFIGS / "sizing_study"
COMPARATIVE_STUDY: Final = CONFIGS / "comparative_study"
SENSITIVITY_STUDY: Final = CONFIGS / "sensitivity_study"
