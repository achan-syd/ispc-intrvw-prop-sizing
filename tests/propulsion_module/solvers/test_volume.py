import pytest

from src.propulsion_module.models.propellants.propellant import Propellant
from src.propulsion_module.solvers.volume import volume
from tests.constants import RELATIVE_TOLERANCE


@pytest.mark.unit
def test_volume() -> None:
    """Volume is mass over density."""
    propellant = Propellant("Hydrazine", 1000)
    assert volume(propellant, 500) == pytest.approx(0.5, rel=RELATIVE_TOLERANCE)
