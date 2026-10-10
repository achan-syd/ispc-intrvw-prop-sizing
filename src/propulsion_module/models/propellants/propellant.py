"""Propellant Properties."""

import csv
from dataclasses import dataclass

from typing_extensions import Self

from src.propulsion_module.constants.assets import PROPELLANT_DATABASE


@dataclass(frozen=True)
class Propellant:
    """Single-fluid propellant.

    Attributes:
        name: Propellant name.
        density: Bulk density [kg/m3].

    """

    name: str
    density: float

    @classmethod
    def from_database(cls, name: str) -> Self:
        """Load a propellant by name from the propellant database.

        Args:
            name: Propellant name, as in the Propellant column of propellant.csv.

        Returns:
            The matching propellant.

        Raises:
            ValueError: If the propellant is not in the database.

        """
        with PROPELLANT_DATABASE.open(newline="") as file:
            for row in csv.DictReader(file):
                if row["Propellant"] == name:
                    return cls(name=name, density=float(row["Density [kg/m3]"]))
        msg = f"Propellant {name!r} not found in {PROPELLANT_DATABASE}"
        raise ValueError(msg)
