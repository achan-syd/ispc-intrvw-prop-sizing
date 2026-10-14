"""Default Factors."""

from typing import Final

DEFAULT_PRESSURE_VESSEL_FOS: Final[float] = 1.5  # Factor of safety [-]
SIZING_TOLERANCE: Final[float] = 1e-9  # Absolute tolerance on the initial mass [kg]
SIZING_UPPER_BOUND_FACTOR: Final[int] = 10  # Upper mass bound over maximum mass [-]
IMAGINARY_NUMBER_TOLERANCE: Final[float] = 1e-10  # Imaginary root tolerence [-]
