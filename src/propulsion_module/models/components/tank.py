"""Tank Component."""

from __future__ import annotations

import math
from dataclasses import dataclass

from typing_extensions import Self

from src.constants.factors import DEFAULT_PRESSURE_VESSEL_FOS
from src.propulsion_module.models.materials.material import Material
from src.propulsion_module.models.propellants.propellant import Propellant
from src.utils.units import to_si_quantity


@dataclass(frozen=True)
class Tank:
    """Thin-walled pressure vessel, None until sized.

    Attributes:
        max_pressure: Maximum pressure [Pa].
        material: Wall material.
        fos: Factor of safety [-].
        radius: Inner radius [m].
        length: Length of the cylindrical section, 0 for a sphere [m].
        thickness: Wall thickness [m].
        volume: Internal volume [m3].
        mass: Tank mass [kg].

    """

    max_pressure: float | None = None
    material: Material | None = None
    fos: float = DEFAULT_PRESSURE_VESSEL_FOS
    radius: float | None = None
    length: float | None = None
    thickness: float | None = None
    volume: float | None = None
    mass: float | None = None

    @classmethod
    def spherical(
        cls,
        radius: float,
        max_pressure: float,
        material: Material,
        fos: float = DEFAULT_PRESSURE_VESSEL_FOS,
    ) -> Self:
        """Size a spherical tank.

        Args:
            radius: Inner radius [m].
            max_pressure: Maximum pressure [Pa].
            material: Wall material.
            fos: Factor of safety [-].

        Returns:
            The sized tank.

        """
        # Maximum pressure [Pa]
        p_max = max_pressure
        # Inner radius [m]
        r_in = radius
        # Material density [kg/m3]
        rho = material.density
        # Allowable stress [Pa], yield strength over factor of safety
        sigma_allow = material.yield_strength / fos

        # Wall thickness [m], thin-wall sphere: t = p r / 2 sigma
        t_wall = p_max * r_in / (2 * sigma_allow)
        # Outer radius [m]
        r_out = r_in + t_wall
        # Internal volume [m3]
        v_in = 4 / 3 * math.pi * r_in**3
        # Shell material volume [m3]
        v_shell = 4 / 3 * math.pi * (r_out**3 - r_in**3)
        return cls(
            max_pressure=p_max,
            fos=fos,
            material=material,
            radius=r_in,
            length=0.0,
            thickness=t_wall,
            volume=v_in,
            mass=rho * v_shell,
        )

    @classmethod
    def cylindrical(
        cls,
        radius: float,
        length: float,
        max_pressure: float,
        material: Material,
        fos: float = DEFAULT_PRESSURE_VESSEL_FOS,
    ) -> Self:
        """Size a cylindrical tank with hemispherical end caps.

        Args:
            radius: Inner radius [m].
            length: Length of the cylindrical section [m].
            max_pressure: Maximum pressure [Pa].
            material: Wall material.
            fos: Factor of safety [-].

        Returns:
            The sized tank.

        """
        # Maximum pressure [Pa]
        p_max = max_pressure
        # Inner radius [m]
        r_in = radius
        # Cylindrical section length [m]
        l_cyl = length
        # Material density [kg/m3]
        rho = material.density
        # Allowable stress [Pa], yield strength over factor of safety
        sigma_allow = material.yield_strength / fos

        # Wall thickness [m], thin-wall hoop stress: t = p r / sigma
        t_wall = p_max * r_in / sigma_allow
        # Outer radius [m]
        r_out = r_in + t_wall
        # Internal volume [m3], cylinder plus two hemispherical caps
        v_in = math.pi * r_in**2 * l_cyl + 4 / 3 * math.pi * r_in**3
        # Cylinder wall material volume [m3]
        v_cyl = math.pi * (r_out**2 - r_in**2) * l_cyl
        # End caps material volume [m3]
        v_caps = 4 / 3 * math.pi * (r_out**3 - r_in**3)
        return cls(
            max_pressure=p_max,
            fos=fos,
            material=material,
            radius=r_in,
            length=l_cyl,
            thickness=t_wall,
            volume=v_in,
            mass=rho * (v_cyl + v_caps),
        )


@dataclass(frozen=True)
class PropellantTank(Tank):
    """Tank holding propellant.

    Attributes:
        propellant: Propellant held.

    """

    propellant: Propellant | None = None

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build an unsized propellant tank from its config section.

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
