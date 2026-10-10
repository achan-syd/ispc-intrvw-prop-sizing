"""Propellant Properties."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Propellant:
    """Single-fluid propellant.

    Attributes:
        name: Propellant name.
        density: Bulk density [kg/m3].

    """

    name: str
    density: float
