"""Pump-Fed Architecture."""

from dataclasses import dataclass

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.pump import Pump
from src.propulsion_module.models.components.tank import Tank


@dataclass(frozen=True)
class PumpFedSystem:
    """Pump-fed propulsion system.

    Attributes:
        tanks: Propellant tanks.
        engines: Engines.
        pumps: Propellant pumps.

    """

    tanks: list[Tank]
    engines: list[Engine]
    pumps: list[Pump]
