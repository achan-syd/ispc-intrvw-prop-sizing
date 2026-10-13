"""Sizing Input."""

from dataclasses import dataclass

from typing_extensions import Self


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

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the specification from a loaded JSON config.

        Args:
            config: Parsed specification config, with a requirements section.

        Returns:
            The specification.

        """
        requirements = config["requirements"]
        return cls(
            delta_v=requirements["delta_v"],
            twr=requirements["twr"],
            dry_mass=requirements["dry_mass"],
            maximum_mass=requirements["maximum_mass"],
        )
