"""Spherical Tank."""

from __future__ import annotations

import math
from dataclasses import dataclass

from typing_extensions import Self

from src.propulsion_module.models.components.tanks.propellant_tank import (
    PropellantTank,
)
from src.propulsion_module.models.materials.material import Material
from src.propulsion_module.models.propellants.propellant import Propellant
from src.utils.units import to_si_quantity


@dataclass
class SphericalTank(PropellantTank):
    """Spherical tank, the radius is calculated from the volume.

    Attributes:
        radius: Inner radius [m].

    """

    radius: float | None = None

    def __post_init__(self) -> None:
        """Calculate the radius, thickness and mass from the volume.

        Raises:
            ValueError: If the volume is not positive.

        """
        if self.volume is None:
            return
        if self.volume <= 0:
            raise ValueError("Tank volume must be positive.")

        # Inner radius [m] from V = 4/3 pi r^3
        self.radius = (3 * self.volume / (4 * math.pi)) ** (1 / 3)
        self._size_shell(self.radius, 0.0, k_stress=2.0)

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build an unsized spherical tank from its config section.

        Args:
            config: Tank section with propellant, pressure and material.

        Returns:
            The tank.

        """
        return cls(
            max_pressure=to_si_quantity(config["pressure"]),
            material=Material.from_database(config["material"]),
            propellant=Propellant.from_database(config["propellant"]),
        )
