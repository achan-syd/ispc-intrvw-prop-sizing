import pytest

from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from tests.constants import RELATIVE_TOLERANCE

CONFIG = {
    "propulsion_module": {
        "tank": {
            "propellant": "Hydrazine",
            "material": "Aluminium",
            "pressure": [25, "bar"],
        },
        "engine": {"isp": 310, "inlet_pressure": [20, "bar"]},
        "pressurant": {"mass_factor": 2e-8},
    },
}


@pytest.mark.unit
def test_from_config() -> None:
    """Config builds the components in SI."""
    system = PressureFedSystem.from_config(CONFIG)
    tank = system.propellant_tanks[0]
    assert tank.propellant.name == "Hydrazine"
    assert tank.material.name == "Aluminium"
    assert tank.max_pressure == pytest.approx(2.5e6, rel=RELATIVE_TOLERANCE)
    assert system.feed_systems[0].mass_factor == pytest.approx(
        2e-8,
        rel=RELATIVE_TOLERANCE,
    )
    assert system.engines[0].isp == 310
    assert system.engines[0].inlet_pressure == pytest.approx(
        2e6,
        rel=RELATIVE_TOLERANCE,
    )
