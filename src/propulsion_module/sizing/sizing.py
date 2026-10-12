"""Sizing Definition."""

from dataclasses import dataclass

from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem


@dataclass(frozen=True)
class Specification:
    """Top-level requirements the system is sized against.

    Attributes:
        delta_v: Required change in velocity [m/s].
        twr: Required thrust-to-weight ratio at ignition [-].
        dry_mass: Dry mass excluding the propulsion system [kg].
        maximum_mass: Maximum initial mass [kg].

    """

    delta_v: float
    twr: float
    dry_mass: float
    maximum_mass: float


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

    system: PressureFedSystem | PumpFedSystem
    mass: SystemMass
    thrust: float
    margin: float


def size_system(
    specification: Specification,
    system: PressureFedSystem | PumpFedSystem,
) -> SizingResult:
    """Size a propulsion system against a specification.

    Args:
        specification: Requirements to size against.
        system: Unsized propulsion system.

    Returns:
        The sized system and its summary.

    """
    raise NotImplementedError
