"""Pressure-Fed Architecture."""

from dataclasses import dataclass, replace

from typing_extensions import Self

from src.propulsion_module.models.architectures.propulsion_system import (
    PropulsionSystem,
)
from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PressurantSystem
from src.propulsion_module.models.components.tanks.factory import tank_from_config


@dataclass(frozen=True)
class PressureFedSystem(PropulsionSystem):
    """Pressure-fed propulsion system.

    Attributes:
        feed_systems: Pressurant systems.

    """

    feed_systems: list[PressurantSystem]

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
            propellant_tanks=[tank_from_config(module["tank"])],
            feed_systems=[PressurantSystem.from_config(module["pressurant"])],
            engines=[Engine.from_config(module["engine"])],
        )

    def size(self, prop_mass: float, _thrust: float) -> Self:
        """Size the tanks and pressurant systems.

        Args:
            prop_mass: Propellant mass [kg].
            _thrust: Thrust, not used by a pressure-fed system [N].

        Returns:
            The system with its tanks and pressurant systems sized.

        """
        # Propellant tank pressure [Pa]
        pressure = self.propellant_tanks[0].max_pressure
        return replace(
            self,
            propellant_tanks=self._size_tanks(prop_mass),
            feed_systems=[feed.size(pressure, prop_mass) for feed in self.feed_systems],
        )
