"""Feed System Component."""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from typing_extensions import Self

from src.utils.units import to_si_quantity


@dataclass(frozen=True)
class FeedSystem:
    """System feeding propellant to the engine, sized by its subclasses.

    Attributes:
        mass: System mass, None until sized [kg].

    """

    mass: float | None = field(default=None, kw_only=True)


@dataclass(frozen=True)
class PumpSystem(FeedSystem):
    """Pump feed system, mass scaling linearly with thrust.

    Attributes:
        mass_factor: Pump mass per unit thrust [kg/N].

    """

    mass_factor: float

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build an unsized pump system from its config section.

        Args:
            config: Pump section with mass_factor, a number or [value, unit].

        Returns:
            The pump system.

        """
        return cls(mass_factor=to_si_quantity(config["mass_factor"]))

    def size(self, thrust: float) -> Self:
        """Size the pump mass, m = k F.

        Args:
            thrust: Thrust [N].

        Returns:
            The pump system with its mass set.

        """
        return replace(self, mass=self.mass_factor * thrust)


@dataclass(frozen=True)
class PressurantSystem(FeedSystem):
    """Pressurant feed system, mass scaling with tank pressure and propellant mass.

    Attributes:
        mass_factor: Pressurant mass per propellant mass per Pa [1/Pa].

    """

    mass_factor: float

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build an unsized pressurant system from its config section.

        Args:
            config: Pressurant section with mass_factor, a number or [value, unit].

        Returns:
            The pressurant system.

        """
        return cls(mass_factor=to_si_quantity(config["mass_factor"]))

    def size(self, pressure: float, propellant_mass: float) -> Self:
        """Size the pressurant mass, m = k p m_p.

        Args:
            pressure: Propellant tank pressure [Pa].
            propellant_mass: Propellant mass [kg].

        Returns:
            The pressurant system with its mass set.

        """
        return replace(self, mass=self.mass_factor * pressure * propellant_mass)
