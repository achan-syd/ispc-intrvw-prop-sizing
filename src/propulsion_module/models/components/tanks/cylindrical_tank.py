"""Cylindrical Tank."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

import numpy as np
from typing_extensions import Self

from src.propulsion_module.models.components.tanks.propellant_tank import (
    PropellantTank,
)
from src.propulsion_module.models.materials.material import Material
from src.propulsion_module.models.propellants.propellant import Propellant
from src.utils.units import to_si_quantity

IMAG_TOLERANCE: Final = 1e-10  # Imaginary part below which a root is real [-]


def _cylinder_volume(r_in: float, l_cyl: float) -> float:
    """Compute the volume of a cylinder with two hemispherical end caps [m3]."""
    return math.pi * r_in**2 * l_cyl + 4 / 3 * math.pi * r_in**3


@dataclass
class CylindricalTank(PropellantTank):
    """Cylindrical tank with hemispherical end caps.

    Give the volume and one of the radius and length, the other is calculated.

    Attributes:
        radius: Inner radius [m].
        length: Length of the cylindrical section [m].

    """

    radius: float | None = None
    length: float | None = None

    def __post_init__(self) -> None:
        """Calculate the missing radius or length, thickness and mass.

        Raises:
            ValueError: If the volume is not positive, or both or neither of
                radius and length are given.

        """
        if self.volume is None:
            return
        if self.volume <= 0:
            raise ValueError("Tank volume must be positive.")
        if (self.radius is None) == (self.length is None):
            raise ValueError("Specify exactly one of radius or length.")

        if self.radius is not None:
            self.length = self._length_from_radius(self.radius)
        else:
            self.radius = self._radius_from_length(self.length)

        self._size_shell(self.radius, self.length, k_stress=1.0)

    def _length_from_radius(self, r_in: float) -> float:
        """Calculate the cylinder length for an inner radius [m]."""
        v_caps = _cylinder_volume(r_in, 0.0)
        v_cyl = self.volume - v_caps

        if v_cyl < 0:
            raise ValueError("Radius is too large for the tank volume.")

        return v_cyl / (math.pi * r_in**2)

    def _radius_from_length(self, l_cyl: float) -> float:
        """Calculate the inner radius for a cylinder length [m]."""
        if l_cyl < 0:
            raise ValueError("Cylinder length must be non-negative.")

        # Roots of 4/3 pi r^3 + pi L r^2 - V = 0
        coeffs = [4 / 3 * math.pi, math.pi * l_cyl, 0.0, -self.volume]
        roots = np.roots(coeffs)
        r_pos = roots[(np.abs(roots.imag) < IMAG_TOLERANCE) & (roots.real > 0)].real

        if len(r_pos) == 0:
            raise ValueError("Could not calculate a valid tank radius.")

        return float(r_pos[0])

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build an unsized cylindrical tank from its config section.

        Args:
            config: Tank section with propellant, pressure and material, and a
                radius or a length.

        Returns:
            The tank.

        """
        return cls(
            max_pressure=to_si_quantity(config["pressure"]),
            material=Material.from_database(config["material"]),
            propellant=Propellant.from_database(config["propellant"]),
            radius=to_si_quantity(config["radius"]) if "radius" in config else None,
            length=to_si_quantity(config["length"]) if "length" in config else None,
        )
