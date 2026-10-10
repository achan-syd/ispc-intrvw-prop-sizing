import json

import pytest

from src.constants.assets import PUMP_FED_CONFIG
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem


def test_from_config() -> None:
    """Default config builds the components in SI."""
    system = PumpFedSystem.from_config(json.loads(PUMP_FED_CONFIG.read_text()))
    tank = system.propellant_tanks[0]
    assert tank.propellant.name == "Hydrazine"
    assert tank.material.name == "Aluminium"
    assert tank.max_pressure == pytest.approx(1e6)
    assert system.engines[0].isp == 330
    assert system.engines[0].inlet_pressure == pytest.approx(4e6)
    assert system.feed_systems[0].mass_factor == pytest.approx(0.008)
