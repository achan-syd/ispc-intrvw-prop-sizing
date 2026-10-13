import pytest

from src.propulsion_module.models.components.engine import Engine


@pytest.mark.unit
def test_from_config() -> None:
    """Engine section converts pressure to SI."""
    engine = Engine.from_config({"isp": 310, "inlet_pressure": [20, "bar"]})
    assert engine.isp == 310
    assert engine.inlet_pressure == pytest.approx(2e6)
    assert engine.mass is None
