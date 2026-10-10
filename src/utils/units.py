"""Unit Conversion."""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

PRESSURE_UNITS: Final = MappingProxyType(
    {
        "Pa": 1.0,
        "kPa": 1e3,
        "MPa": 1e6,
        "bar": 1e5,
        "psi": 6894.757293168,
    },
)

MASS_UNITS: Final = MappingProxyType(
    {
        "kg": 1.0,
        "g": 1e-3,
        "lb": 0.45359237,
    },
)

LENGTH_UNITS: Final = MappingProxyType(
    {
        "m": 1.0,
        "cm": 1e-2,
        "mm": 1e-3,
        "in": 0.0254,
        "ft": 0.3048,
    },
)

FORCE_UNITS: Final = MappingProxyType(
    {
        "N": 1.0,
        "kN": 1e3,
        "lbf": 4.4482216152605,
    },
)

VELOCITY_UNITS: Final = MappingProxyType(
    {
        "m/s": 1.0,
        "km/s": 1e3,
    },
)

DENSITY_UNITS: Final = MappingProxyType(
    {
        "kg/m3": 1.0,
        "g/cm3": 1e3,
    },
)

SI_FACTORS: Final = MappingProxyType(
    {
        **PRESSURE_UNITS,
        **MASS_UNITS,
        **LENGTH_UNITS,
        **FORCE_UNITS,
        **VELOCITY_UNITS,
        **DENSITY_UNITS,
    },
)


def to_si(value: float, unit: str) -> float:
    """Convert a value in the given unit to SI.

    Args:
        value: Value in the given unit.
        unit: Unit name, a key of SI_FACTORS, e.g. "bar".

    Returns:
        The value in SI.

    Raises:
        ValueError: If the unit is not known.

    """
    if unit not in SI_FACTORS:
        msg = f"Unknown unit {unit!r}, expected one of {sorted(SI_FACTORS)}"
        raise ValueError(msg)
    return value * SI_FACTORS[unit]


def to_si_quantity(quantity: float | list) -> float:
    """Convert a plain SI number or a [value, unit] pair to SI.

    Args:
        quantity: A number already in SI, or a [value, unit] pair, e.g. [20, "bar"].

    Returns:
        The value in SI.

    """
    if isinstance(quantity, list):
        value, unit = quantity
        return to_si(value, unit)
    return quantity
