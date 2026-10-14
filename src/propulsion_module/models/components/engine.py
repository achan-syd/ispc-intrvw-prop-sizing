"""Engine Component."""

from __future__ import annotations

from dataclasses import dataclass, replace

from typing_extensions import Self

from src.utils.units import to_si_quantity


@dataclass(frozen=True)
class Engine:
    """Rocket engine, with mass scaling linearly with inlet pressure.

    Attributes:
        isp: Specific impulse [s].
        inlet_pressure: Engine inlet pressure [Pa].
        mass_factor: Engine mass per unit inlet pressure [kg/Pa].
        mass: Engine mass, None until sized [kg].

    """

    isp: float
    inlet_pressure: float
    mass_factor: float
    mass: float | None = None

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the engine from its config section.

        Args:
            config: Engine section with isp, inlet_pressure and mass_factor.

        Returns:
            The engine.

        """
        return cls(
            isp=config["isp"],
            inlet_pressure=to_si_quantity(config["inlet_pressure"]),
            mass_factor=to_si_quantity(config["mass_factor"]),
        )

    def size(self) -> Self:
        """Size the engine mass, m = k p.

        Returns:
            The engine with its mass set.

        """
        return replace(self, mass=self.mass_factor * self.inlet_pressure)
