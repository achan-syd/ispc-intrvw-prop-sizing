"""Propellant Tank."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.constants.factors import DEFAULT_PRESSURE_VESSEL_FOS

if TYPE_CHECKING:
    from src.propulsion_module.models.materials.material import Material
    from src.propulsion_module.models.propellants.propellant import Propellant


@dataclass
class PropellantTank:
    """Thin-walled pressure vessel holding propellant, sized from its volume.

    Use SphericalTank or CylindricalTank, they size the tank on initialisation.

    Attributes:
        max_pressure: Maximum pressure [Pa].
        material: Wall material.
        fos: Factor of safety [-].
        ullage: Fraction of the internal volume left unfilled [-].
        propellant: Propellant held.
        volume: Internal volume, the tank stays unsized without it [m3].
        thickness: Wall thickness [m].
        mass: Tank mass [kg].

    """

    max_pressure: float | None = None
    material: Material | None = None
    fos: float = DEFAULT_PRESSURE_VESSEL_FOS
    ullage: float = 0.0
    propellant: Propellant | None = None
    volume: float | None = None
    thickness: float | None = None
    mass: float | None = None

    def _size_shell(self, r_in: float, l_cyl: float, k_stress: float) -> None:
        """Calculate the wall thickness and mass with thin-wall stress equations.

        Args:
            r_in: Inner radius [m].
            l_cyl: Length of the cylindrical section, 0 for a sphere [m].
            k_stress: 2 for a sphere, 1 for the hoop stress of a cylinder [-].

        Raises:
            ValueError: If an input is missing or out of range.

        """
        if self.max_pressure is None or self.material is None:
            raise ValueError("Tank sizing requires max_pressure and material.")
        if self.max_pressure < 0 or self.fos <= 0:
            raise ValueError("Pressure must be non-negative and FOS positive.")
        if r_in <= 0 or l_cyl < 0:
            raise ValueError("Radius must be positive and length non-negative.")

        # Allowable stress [Pa], yield strength over factor of safety
        sigma_allow = self.material.yield_strength / self.fos
        # Wall thickness [m], t = p r / (k sigma)
        self.thickness = self.max_pressure * r_in / (k_stress * sigma_allow)
        # Outer radius [m]
        r_out = r_in + self.thickness
        # Cylinder wall material volume [m3]
        v_cyl = math.pi * (r_out**2 - r_in**2) * l_cyl
        # End caps material volume [m3]
        v_caps = 4 / 3 * math.pi * (r_out**3 - r_in**3)

        self.mass = self.material.density * (v_cyl + v_caps)
