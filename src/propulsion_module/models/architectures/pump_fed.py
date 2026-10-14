"""Pump-Fed Architecture."""

from dataclasses import dataclass, replace

from typing_extensions import Self

from src.propulsion_module.models.architectures.propulsion_system import (
    PropulsionSystem,
)
from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PumpSystem
from src.propulsion_module.models.components.tanks.factory import tank_from_config


@dataclass(frozen=True)
class PumpFedSystem(PropulsionSystem):
    """Pump-fed propulsion system.

    Attributes:
        feed_systems: Pump systems.

    """

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
            feed_systems=[PumpSystem.from_config(module["pump"])],
            engines=[Engine.from_config(module["engine"])],
        )

    def size(self, prop_mass: float, thrust: float) -> Self:
        """Size the tanks and pump systems.

        Args:
            prop_mass: Propellant mass [kg].
            thrust: Thrust [N].

        Returns:
            The system with its tanks and pump systems sized.

        """
        return replace(
            self,
            propellant_tanks=self._size_tanks(prop_mass),
            engines=[engine.size() for engine in self.engines],
            feed_systems=[feed.size(thrust) for feed in self.feed_systems],
        )
