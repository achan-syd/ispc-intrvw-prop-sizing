"""Propulsion System."""

from dataclasses import dataclass, replace

from src.propulsion_module.models.components.engine import Engine
from src.propulsion_module.models.components.feed_system import FeedSystem
from src.propulsion_module.models.components.tanks.propellant_tank import (
    PropellantTank,
)
from src.propulsion_module.solvers.volume import volume


@dataclass(frozen=True)
class PropulsionSystem:
    """Propulsion system, what every architecture has in common.

    Attributes:
        propellant_tanks: Propellant tanks.
        feed_systems: Feed systems.
        engines: Engines.

    """

    propellant_tanks: list[PropellantTank]
    feed_systems: list[FeedSystem]
    engines: list[Engine]

    @property
    def mass(self) -> float:
        """Propulsion hardware mass, tanks, feed systems and engines [kg]."""
        return (
            sum(tank.mass for tank in self.propellant_tanks)
            + sum(feed.mass for feed in self.feed_systems)
            + sum(engine.mass or 0.0 for engine in self.engines)
        )

    def _size_tanks(self, prop_mass: float) -> list[PropellantTank]:
        """Size each tank for its share of the propellant, plus its ullage."""
        sized = []
        for tank in self.propellant_tanks:
            # Propellant volume of this tank's share [m3]
            v_prop = volume(tank.propellant, prop_mass / len(self.propellant_tanks))
            # Internal volume [m3], the tank initialiser does the rest of the sizing
            sized.append(replace(tank, volume=v_prop / (1 - tank.ullage)))
        return sized
