from typing import Final

import pytest

from src.propulsion_module.solvers.rocket_equation import rocket_equation
from tests.constants import RELATIVE_TOLERANCE

DELTA_V: Final[float] = 2000.0
ISP: Final[float] = 310.0
FINAL_MASS: Final[float] = 600.0
INITIAL_MASS: Final[float] = 1158.4186  # 600 * exp(2000 / (310 * 9.80665))


@pytest.mark.unit
def test_solve_initial_mass() -> None:
    """Initial mass matches the hand calculation."""
    initial_mass = rocket_equation(DELTA_V, ISP, final_mass=FINAL_MASS)
    # Hand calculation:
    # m_0 = m_f * exp(dv / (Isp*g0)) = 600 * exp(0.6579) = 1158.42 kg
    assert initial_mass == pytest.approx(INITIAL_MASS, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_solve_final_mass() -> None:
    """Final mass matches the hand calculation."""
    result = rocket_equation(DELTA_V, ISP, initial_mass=INITIAL_MASS)
    # Hand calculation:
    # m_f = m_0 * exp(-dv / (Isp*g0)) = 1158.42 * exp(-0.6579) = 600 kg
    assert result == pytest.approx(FINAL_MASS, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_solve_delta_v() -> None:
    """Delta-V matches the hand calculation."""
    result = rocket_equation(isp=ISP, initial_mass=INITIAL_MASS, final_mass=FINAL_MASS)
    # Hand calculation:
    # dv = Isp * g0 * ln(m_0/m_f) = 310 * 9.80665 * 0.6579 = 2000 m/s
    assert result == pytest.approx(DELTA_V, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_solve_isp() -> None:
    """Isp matches the hand calculation."""
    result = rocket_equation(
        delta_v=DELTA_V,
        initial_mass=INITIAL_MASS,
        final_mass=FINAL_MASS,
    )
    # Hand calculation:
    # Isp = dv / (g0 * ln(m_0/m_f)) = 2000 / (9.80665 * 0.6579) = 310 s
    assert result == pytest.approx(ISP, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
@pytest.mark.parametrize(
    "kwargs",
    [
        {"delta_v": DELTA_V, "isp": ISP},
        {
            "delta_v": DELTA_V,
            "isp": ISP,
            "initial_mass": INITIAL_MASS,
            "final_mass": FINAL_MASS,
        },
    ],
)
def test_invalid_argument_count(kwargs: dict[str, float]) -> None:
    """Anything but three arguments raises ValueError."""
    with pytest.raises(ValueError, match="exactly three"):
        rocket_equation(**kwargs)
