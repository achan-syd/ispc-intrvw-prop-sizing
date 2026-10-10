import json

import pytest

from src.constants.assets import PRESSURE_FED_CONFIG
from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem


def test_from_config() -> None:
    """Default config builds the components in SI."""
    system = PressureFedSystem.from_config(json.loads(PRESSURE_FED_CONFIG.read_text()))
    tank = system.propellant_tanks[0]
    assert tank.propellant.name == "Hydrazine"
    assert tank.material.name == "Aluminium"
    assert tank.max_pressure == pytest.approx(2.5e6)
    assert system.pressurant_tanks[0].mass_factor == pytest.approx(2e-8)
    assert system.engines[0].isp == 310
    assert system.engines[0].inlet_pressure == pytest.approx(2e6)
