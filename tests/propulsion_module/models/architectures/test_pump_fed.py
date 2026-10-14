import pytest

from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem
from tests.constants import RELATIVE_TOLERANCE

CONFIG = {
    "propulsion_module": {
        "tank": {
            "propellant": "Hydrazine",
            "material": "Aluminium",
            "pressure": [10, "bar"],
        },
        "engine": {
            "isp": 330,
            "inlet_pressure": [40, "bar"],
            "mass_factor": [0.2, "kg/bar"],
        },
        "pump": {"mass_factor": [0.008, "kg/N"]},
    },
}


@pytest.mark.unit
def test_from_config() -> None:
    """Config builds the components in SI."""
    system = PumpFedSystem.from_config(CONFIG)
    tank = system.propellant_tanks[0]
    assert tank.propellant.name == "Hydrazine"
    assert tank.material.name == "Aluminium"
    assert tank.max_pressure == pytest.approx(1e6, rel=RELATIVE_TOLERANCE)
    assert system.engines[0].isp == 330
    assert system.engines[0].inlet_pressure == pytest.approx(
        4e6,
        rel=RELATIVE_TOLERANCE,
    )
    assert system.feed_systems[0].mass_factor == pytest.approx(
        0.008,
        rel=RELATIVE_TOLERANCE,
    )
