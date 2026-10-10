"""Rocket Equation."""

from __future__ import annotations

import math

from src.constants.universal import EARTH_GRAVITY


def rocket_equation(
    delta_v: float | None = None,
    isp: float | None = None,
    initial_mass: float | None = None,
    final_mass: float | None = None,
) -> float:
    """Solve the rocket equation, dv = isp g0 ln(m0 / mf), for the missing term.

    Args:
        delta_v: Change in velocity [m/s].
        isp: Specific impulse [s].
        initial_mass: Mass before the burn [kg].
        final_mass: Mass after the burn [kg].

    Returns:
        The one argument left as None, in its own units.

    Raises:
        ValueError: If anything other than exactly one argument is None.

    """
    if [delta_v, isp, initial_mass, final_mass].count(None) != 1:
        msg = "Provide exactly three of delta_v, isp, initial_mass, final_mass"
        raise ValueError(msg)

    if delta_v is None:
        # Solve for the change in velocity [m/s]
        return isp * EARTH_GRAVITY * math.log(initial_mass / final_mass)
    if isp is None:
        # Solve for the specific impulse [s]
        return delta_v / (EARTH_GRAVITY * math.log(initial_mass / final_mass))
    if initial_mass is None:
        # Solve for the mass before the burn [kg]
        return final_mass * math.exp(delta_v / (isp * EARTH_GRAVITY))
    # Solve for the mass after the burn [kg]
    return initial_mass * math.exp(-delta_v / (isp * EARTH_GRAVITY))
