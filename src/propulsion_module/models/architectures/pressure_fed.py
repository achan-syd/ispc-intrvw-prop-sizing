"""Pressure-Fed Architecture."""

from dataclasses import dataclass

from typing_extensions import Self

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PressurantSystem
from src.propulsion_module.models.components.tank import PropellantTank


@dataclass(frozen=True)
class PressureFedSystem:
    """Pressure-fed propulsion system.

    Attributes:
        propellant_tanks: Propellant tanks.
        feed_systems: Pressurant systems.
        engines: Engines.

    """

    propellant_tanks: list[PropellantTank]
    feed_systems: list[PressurantSystem]
    engines: list[Engine]

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the system from a loaded JSON config.

        Args:
            config: Parsed pressure-fed config, with a propulsion_module section.

        Returns:
            The system, with one of each component and nothing sized yet.

        """
        module = config["propulsion_module"]
        return cls(
            propellant_tanks=[PropellantTank.from_config(module["tank"])],
            feed_systems=[PressurantSystem.from_config(module["pressurant"])],
            engines=[Engine.from_config(module["engine"])],
        )
