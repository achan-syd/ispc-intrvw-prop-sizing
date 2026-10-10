"""Engine Component."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Engine:
    """Rocket engine.

    Attributes:
        isp: Specific impulse [s].
        inlet_pressure: Engine inlet pressure [Pa].
        mass: Engine mass [kg].

    """

    isp: float
    inlet_pressure: float
    mass: float
