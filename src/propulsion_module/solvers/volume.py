"""Propellant Volume."""

from src.propulsion_module.models.propellants.propellant import Propellant


def volume(propellant: Propellant, mass: float) -> float:
    """Compute the volume of a mass of propellant, V = m / rho.

    Args:
        propellant: Propellant, for its density.
        mass: Propellant mass [kg].

    Returns:
        Volume [m3].

    """
    return mass / propellant.density
