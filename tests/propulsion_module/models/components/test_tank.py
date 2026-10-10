import math

import pytest

from src.propulsion_module.constants.factors import DEFAULT_PRESSURE_VESSEL_FOS
from src.propulsion_module.models.components.tank import PropellantTank, Tank
from src.propulsion_module.models.materials.material import Material


@pytest.fixture
def material() -> Material:
    return Material.from_database("Aluminium")


def test_spherical(material: Material) -> None:
    tank = Tank.spherical(0.5, 2.5e6, material)
    assert tank.fos == DEFAULT_PRESSURE_VESSEL_FOS
    assert tank.thickness == pytest.approx(2.5e6 * 0.5 / (2 * 276e6 / 1.5))
    assert tank.volume == pytest.approx(4 / 3 * math.pi * 0.5**3)
    assert tank.length == 0
    assert tank.mass > 0


def test_cylindrical(material: Material) -> None:
    tank = PropellantTank.cylindrical(0.5, 1.0, 2.5e6, material, fos=2.0)
    assert isinstance(tank, PropellantTank)
    assert tank.fos == 2.0
    assert tank.thickness == pytest.approx(2.5e6 * 0.5 / (276e6 / 2.0))
    assert tank.volume == pytest.approx(
        math.pi * 0.5**2 * 1.0 + 4 / 3 * math.pi * 0.5**3,
    )
    assert tank.mass > 0
