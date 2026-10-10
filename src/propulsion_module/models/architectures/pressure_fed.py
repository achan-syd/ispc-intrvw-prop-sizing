"""Pressure-Fed Architecture."""

from dataclasses import dataclass

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.tank import (
    PressurantTank,
    PropellantTank,
)


@dataclass(frozen=True)
class PressureFedSystem:
    """Pressure-fed propulsion system.

    Attributes:
        propellant_tanks: Propellant tanks.
        pressurant_tanks: Pressurant tanks.
        engines: Engines.

    """

    propellant_tanks: list[PropellantTank]
    pressurant_tanks: list[PressurantTank]
    engines: list[Engine]
