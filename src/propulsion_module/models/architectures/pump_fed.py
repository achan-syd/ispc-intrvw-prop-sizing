"""Pump-Fed Architecture."""

from dataclasses import dataclass

from typing_extensions import Self

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.pump import Pump
from src.propulsion_module.models.components.tank import (
    PropellantTank,
)


@dataclass(frozen=True)
class PumpFedSystem:
    """Pump-fed propulsion system.

    Attributes:
        propellant_tanks: Propellant tanks.
        engines: Engines.
        pumps: Propellant pumps.

    """

    propellant_tanks: list[PropellantTank]
    engines: list[Engine]
    pumps: list[Pump]

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the system from a loaded JSON config.

        Args:
            config: Parsed pump-fed config, with a propulsion_module section.

        Returns:
            The system, with one of each component and nothing sized yet.

        """
        module = config["propulsion_module"]
        return cls(
            propellant_tanks=[PropellantTank.from_config(module["tank"])],
            engines=[Engine.from_config(module["engine"])],
            pumps=[Pump.from_config(module["pump"])],
        )
