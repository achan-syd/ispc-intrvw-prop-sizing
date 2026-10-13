"""Pump-Fed Architecture."""

from dataclasses import dataclass, replace

from typing_extensions import Self

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import PumpSystem
from src.propulsion_module.models.components.tanks.factory import (
    PropellantTank,
    size_tanks,
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
            propellant_tanks=size_tanks(self.propellant_tanks, prop_mass),
            feed_systems=[feed.size(thrust) for feed in self.feed_systems],
        )
