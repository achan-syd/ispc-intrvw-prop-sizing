"""Pressure-Fed Architecture."""

from dataclasses import dataclass, replace

from typing_extensions import Self

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PressurantSystem
from src.propulsion_module.models.components.tanks.factory import (
    PropellantTank,
    size_tanks,
    tank_from_config,
)


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

    @property
    def mass(self) -> float:
        """Propulsion hardware mass, tanks, feed systems and engines [kg]."""
        return (
            sum(tank.mass for tank in self.propellant_tanks)
            + sum(feed.mass for feed in self.feed_systems)
            + sum(engine.mass or 0.0 for engine in self.engines)
        )

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
            propellant_tanks=size_tanks(self.propellant_tanks, prop_mass),
            feed_systems=[feed.size(pressure, prop_mass) for feed in self.feed_systems],
        )
