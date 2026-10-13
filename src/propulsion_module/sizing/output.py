"""Sizing Output."""

from dataclasses import dataclass

from src.propulsion_module.models.architectures.propulsion_system import (
    PropulsionSystem,
)


@dataclass(frozen=True)
class SystemMass:
    """Mass breakdown, with the total always the sum of its parts.

    Attributes:
        propellant_mass: Propellant mass [kg].
        hardware_mass: Everything but propellant, dry mass plus hardware [kg].

    """

    propellant_mass: float
    hardware_mass: float

    @property
    def total_mass(self) -> float:
        """Total mass, propellant plus hardware [kg]."""
        return self.propellant_mass + self.hardware_mass


@dataclass(frozen=True)
class SizingResult:
    """Outcome of sizing a propulsion system.

    Attributes:
        system: The system with every component sized.
        mass: Mass breakdown, its total is the initial mass.
        thrust: Thrust for the thrust-to-weight requirement [N].
        margin: Margin to the maximum initial mass, negative if exceeded [-].

    """

    system: PropulsionSystem
    mass: SystemMass
    thrust: float
    margin: float
