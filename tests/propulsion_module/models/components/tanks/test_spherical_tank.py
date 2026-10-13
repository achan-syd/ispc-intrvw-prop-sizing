import math

import pytest

from src.constants.factors import DEFAULT_PRESSURE_VESSEL_FOS
from src.propulsion_module.models.components.tanks.spherical_tank import SphericalTank
from src.propulsion_module.models.materials.material import Material


@pytest.fixture
def material() -> Material:
    """Aluminium from the database."""
    return Material.from_database("Aluminium")


@pytest.mark.unit
def test_spherical_tank(material: Material) -> None:
    """Sphere uses the default FOS and thin-wall sizing."""
    tank = SphericalTank(
        max_pressure=2.5e6,
        material=material,
        volume=4 / 3 * math.pi * 0.5**3,
    )
    assert tank.fos == DEFAULT_PRESSURE_VESSEL_FOS
    assert tank.ullage == 0
    assert tank.radius == pytest.approx(0.5)
    assert tank.thickness == pytest.approx(2.5e6 * 0.5 / (2 * 276e6 / 1.5))
    assert tank.mass > 0
