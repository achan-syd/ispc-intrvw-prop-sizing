"""Pump Component."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Pump:
    """Propellant pump.

    Attributes:
        mass: Pump mass [kg].

    """

    mass: float
