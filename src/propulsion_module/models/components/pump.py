"""Pump Component."""

from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Self


@dataclass(frozen=True)
class Pump:
    """Propellant pump.

    Attributes:
        mass_factor: Pump mass per unit thrust [kg/N].
        mass: Pump mass, None until sized [kg].

    """

    mass_factor: float
    mass: float | None = None

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the pump from its config section.

        Args:
            config: Pump section with mass_factor.

        Returns:
            The pump.

        """
        return cls(mass_factor=config["mass_factor"])
