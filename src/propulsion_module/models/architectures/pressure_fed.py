"""Pressure-Fed Architecture."""

from dataclasses import dataclass

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.tank import Tank


@dataclass(frozen=True)
class PressureFedSystem:
    """Pressure-fed propulsion system.

    Attributes:
        tanks: Propellant tanks.
        engines: Engines.

    """

    tanks: list[Tank]
    engines: list[Engine]
