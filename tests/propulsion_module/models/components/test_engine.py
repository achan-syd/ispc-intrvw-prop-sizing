import pytest

from src.propulsion_module.models.components.engine import Engine
from tests.constants import RELATIVE_TOLERANCE


@pytest.mark.unit
def test_from_config() -> None:
    """Engine section converts pressure and mass factor to SI."""
    engine = Engine.from_config(
        {"isp": 310, "inlet_pressure": [20, "bar"], "mass_factor": [0.2, "kg/bar"]},
    )
    assert engine.isp == 310
    assert engine.inlet_pressure == pytest.approx(2e6, rel=RELATIVE_TOLERANCE)
    assert engine.mass_factor == pytest.approx(2e-6, rel=RELATIVE_TOLERANCE)
