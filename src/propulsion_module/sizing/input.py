"""Sizing Input."""

from dataclasses import dataclass


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
