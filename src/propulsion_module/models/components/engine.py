"""Engine Component."""

from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Self

from src.utils.units import to_si_quantity


@dataclass(frozen=True)
class Engine:
    """Rocket engine.

    Attributes:
        isp: Specific impulse [s].
        inlet_pressure: Engine inlet pressure [Pa].
        mass: Engine mass, None until sized [kg].

    """

    isp: float
    inlet_pressure: float
    mass: float | None = None

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the engine from its config section.

        Args:
            config: Engine section with isp and inlet_pressure.

        Returns:
            The engine.

        """
        return cls(
            isp=config["isp"],
            inlet_pressure=to_si_quantity(config["inlet_pressure"]),
        )
