import pytest

from src.propulsion_module.models.components.feed_system import (
    PressurantSystem,
    PumpSystem,
)
from tests.constants import RELATIVE_TOLERANCE


@pytest.mark.unit
def test_pump_size() -> None:
    """Pump mass scales linearly with thrust."""
    pump = PumpSystem(mass_factor=0.008).size(thrust=3000)
    assert pump.mass == pytest.approx(24, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_pressurant_size() -> None:
    """Pressurant mass scales with pressure and propellant mass."""
    system = PressurantSystem(mass_factor=2e-8).size(
        pressure=2.5e6,
        propellant_mass=500,
    )
    assert system.mass == pytest.approx(25, rel=RELATIVE_TOLERANCE)
