"""Tank Component."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tank:
    """Propellant tank.

    Attributes:
        pressure: Tank pressure [Pa].
        mass: Tank mass [kg].

    """

    pressure: float
    mass: float
