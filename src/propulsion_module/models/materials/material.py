"""Material Properties."""

import csv
from dataclasses import dataclass

from src.constants.assets import MATERIAL_DATABASE


@dataclass(frozen=True)
class Material:
    """Structural material.

    Attributes:
        name: Material name.
        density: Density [kg/m3].
        yield_strength: Yield strength [Pa].
        ultimate_strength: Ultimate strength [Pa].

    """

    name: str
    density: float
    yield_strength: float
    ultimate_strength: float

    @classmethod
    def from_database(cls, name: str) -> "Material":
        """Load a material by name from the material database.

        Args:
            name: Material name, as in the Material column of material.csv.

        Returns:
            The matching material.

        Raises:
            ValueError: If the material is not in the database.

        """
        with MATERIAL_DATABASE.open(newline="") as file:
            for row in csv.DictReader(file):
                if row["Material"] == name:
                    return cls(
                        name=name,
                        density=float(row["Density [kg/m3]"]),
                        yield_strength=float(row["Yield Strength [Pa]"]),
                        ultimate_strength=float(row["Ultimate Strength [Pa]"]),
                    )
        raise ValueError(f"Material {name!r} not found in {MATERIAL_DATABASE}")
