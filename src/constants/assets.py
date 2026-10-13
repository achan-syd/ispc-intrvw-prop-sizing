"""Default Asset Files."""

from pathlib import Path
from typing import Final

SRC: Final[Path] = Path(__file__).parents[1]
CONFIGS: Final[Path] = SRC / "configs"

MATERIAL_DATABASE: Final[Path] = SRC / "database" / "material.csv"
PROPELLANT_DATABASE: Final[Path] = SRC / "database" / "propellant.csv"
SPECIFICATIONS: Final[Path] = CONFIGS / "specification.json"
SIZING_STUDY: Final[Path] = CONFIGS / "sizing_study"
COMPARATIVE_STUDY: Final[Path] = CONFIGS / "comparative_study"
SENSITIVITY_STUDY: Final[Path] = CONFIGS / "sensitivity_study"
