import pytest

from src.propulsion_module.solvers.rocket_equation import rocket_equation

DELTA_V = 2000.0
ISP = 310.0
FINAL_MASS = 600.0
INITIAL_MASS = rocket_equation(DELTA_V, ISP, final_mass=FINAL_MASS)


@pytest.mark.unit
def test_solve_initial_mass() -> None:
    """Initial mass matches a hand calculation."""
    initial_mass = rocket_equation(DELTA_V, ISP, final_mass=FINAL_MASS)
    assert initial_mass == pytest.approx(1158.42, abs=0.01)


@pytest.mark.unit
def test_solve_final_mass() -> None:
    """Final mass round-trips."""
    result = rocket_equation(DELTA_V, ISP, initial_mass=INITIAL_MASS)
    assert result == pytest.approx(FINAL_MASS)


@pytest.mark.unit
def test_solve_delta_v() -> None:
    """Delta-V round-trips."""
    result = rocket_equation(isp=ISP, initial_mass=INITIAL_MASS, final_mass=FINAL_MASS)
    assert result == pytest.approx(DELTA_V)


@pytest.mark.unit
def test_solve_isp() -> None:
    """Isp round-trips."""
    result = rocket_equation(
        delta_v=DELTA_V,
        initial_mass=INITIAL_MASS,
        final_mass=FINAL_MASS,
    )
    assert result == pytest.approx(ISP)


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
