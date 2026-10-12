"""Thrust To Weight Ratio."""

from __future__ import annotations


def thrust_to_weight_ratio(
    twr: float | None = None,
    thrust: float | None = None,
    mass: float | None = None,
    gravity: float | None = None,
) -> float:
    """Solve twr = thrust / (mass gravity) for the missing term.

    Args:
        twr: Thrust-to-weight ratio [-].
        thrust: Thrust [N].
        mass: Mass [kg].
        gravity: Gravity the weight is measured in [m/s2].

    Returns:
        The one argument left as None, in its own units.

    Raises:
        ValueError: If anything other than exactly one argument is None.

    """
    if [twr, thrust, mass, gravity].count(None) != 1:
        raise ValueError("Provide exactly three of twr, thrust, mass, gravity")

    if twr is None:
        # Solve for the thrust-to-weight ratio [-]
        return thrust / (mass * gravity)
    if thrust is None:
        # Solve for the thrust [N]
        return twr * mass * gravity
    if mass is None:
        # Solve for the mass [kg]
        return thrust / (twr * gravity)
    # Solve for the gravity [m/s2]
    return thrust / (twr * mass)
