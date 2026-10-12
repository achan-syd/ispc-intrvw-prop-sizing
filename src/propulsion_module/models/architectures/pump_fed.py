"""Pump-Fed Architecture."""

from dataclasses import dataclass

from typing_extensions import Self

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PumpSystem
from src.propulsion_module.models.components.tanks import (
    PropellantTank,
    tank_from_config,
)


@dataclass(frozen=True)
class PumpFedSystem:
    """Pump-fed propulsion system.

    Attributes:
        propellant_tanks: Propellant tanks.
        engines: Engines.
        feed_systems: Pump systems.

    """

    propellant_tanks: list[PropellantTank]
    engines: list[Engine]
    feed_systems: list[PumpSystem]

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
            propellant_tanks=[tank_from_config(module["tank"])],
            engines=[Engine.from_config(module["engine"])],
            feed_systems=[PumpSystem.from_config(module["pump"])],
        )
