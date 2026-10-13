"""Tank Factory."""

from src.propulsion_module.models.components.tanks.cylindrical_tank import (
    CylindricalTank,
)
from src.propulsion_module.models.components.tanks.propellant_tank import (
    PropellantTank,
)
from src.propulsion_module.models.components.tanks.spherical_tank import SphericalTank


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
