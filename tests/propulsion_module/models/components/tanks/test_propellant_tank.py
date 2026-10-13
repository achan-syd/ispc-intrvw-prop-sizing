import pytest

from src.propulsion_module.models.components.tanks import tank_from_config
from src.propulsion_module.models.components.tanks.spherical_tank import SphericalTank


@pytest.mark.unit
def test_tank_from_config() -> None:
    """Tank section loads its propellant and defaults to a sphere."""
    config = {"propellant": "Hydrazine", "material": "Aluminium", "pressure": 1e6}
    tank = tank_from_config(config)
    assert isinstance(tank, SphericalTank)
    assert tank.propellant.name == "Hydrazine"
    assert tank.max_pressure == 1e6
