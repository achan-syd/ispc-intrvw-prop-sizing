"""Tank Factory."""

from dataclasses import replace

from src.propulsion_module.models.components.tanks.cylindrical_tank import (
    CylindricalTank,
)
from src.propulsion_module.models.components.tanks.propellant_tank import (
    PropellantTank,
)
from src.propulsion_module.models.components.tanks.spherical_tank import SphericalTank
from src.propulsion_module.solvers.volume import volume


def tank_from_config(config: dict) -> PropellantTank:
    """Build the tank shape the config describes.

    A radius or a length gives a cylindrical tank, otherwise it is spherical.

    Args:
        config: Tank section with propellant, pressure and material, and
            optionally a radius or a length.

    Returns:
        The unsized tank.

    """
    match config:
        case {"radius": _} | {"length": _}:
            return CylindricalTank.from_config(config)
        case _:
            return SphericalTank.from_config(config)


def size_tanks(tanks: list[PropellantTank], prop_mass: float) -> list[PropellantTank]:
    """Size each tank for its share of the propellant, plus its ullage.

    Args:
        tanks: Unsized propellant tanks.
        prop_mass: Total propellant mass [kg].

    Returns:
        The sized tanks.

    """
    sized = []
    for tank in tanks:
        # Propellant volume of this tank's share [m3]
        v_prop = volume(tank.propellant, prop_mass / len(tanks))
        # Internal volume [m3], the tank initialiser does the rest of the sizing
        sized.append(replace(tank, volume=v_prop / (1 - tank.ullage)))
    return sized
