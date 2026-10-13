from typing import Final

import pytest

from src.propulsion_module.solvers.thrust_to_weight_ratio import (
    thrust_to_weight_ratio,
)

TWR: Final[float] = 1.5
THRUST: Final[float] = 3000.0
MASS: Final[float] = 1000.0
GRAVITY: Final[float] = 2.0


@pytest.mark.unit
def test_solve_twr() -> None:
    """Thrust-to-weight ratio matches a hand calculation."""
    result = thrust_to_weight_ratio(thrust=THRUST, mass=MASS, gravity=GRAVITY)
    assert result == pytest.approx(TWR)


@pytest.mark.unit
def test_solve_thrust() -> None:
    """Thrust round-trips."""
    result = thrust_to_weight_ratio(twr=TWR, mass=MASS, gravity=GRAVITY)
    assert result == pytest.approx(THRUST)


@pytest.mark.unit
def test_solve_mass() -> None:
    """Mass round-trips."""
    result = thrust_to_weight_ratio(twr=TWR, thrust=THRUST, gravity=GRAVITY)
    assert result == pytest.approx(MASS)


@pytest.mark.unit
def test_solve_gravity() -> None:
    """Gravity round-trips."""
    result = thrust_to_weight_ratio(twr=TWR, thrust=THRUST, mass=MASS)
    assert result == pytest.approx(GRAVITY)


@pytest.mark.unit
@pytest.mark.parametrize(
    "kwargs",
    [
        {"twr": TWR, "thrust": THRUST},
        {"twr": TWR, "thrust": THRUST, "mass": MASS, "gravity": GRAVITY},
    ],
)
def test_invalid_argument_count(kwargs: dict[str, float]) -> None:
    """Anything but three arguments raises ValueError."""
    with pytest.raises(ValueError, match="exactly three"):
        thrust_to_weight_ratio(**kwargs)
