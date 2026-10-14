import math

import pytest

from src.propulsion_module.models.components.tanks.cylindrical_tank import (
    CylindricalTank,
)
from src.propulsion_module.models.materials.material import Material
from tests.constants import RELATIVE_TOLERANCE


@pytest.fixture
def material() -> Material:
    """Aluminium from the database."""
    return Material.from_database("Aluminium")


@pytest.mark.unit
def test_cylindrical_tank(material: Material) -> None:
    """Cylinder length is calculated from the radius."""
    tank = CylindricalTank(
        max_pressure=2.5e6,
        material=material,
        volume=math.pi * 0.5**2 * 1.0 + 4 / 3 * math.pi * 0.5**3,
        radius=0.5,
        fos=2.0,
        ullage=0.05,
    )
    assert tank.length == pytest.approx(1.0, rel=RELATIVE_TOLERANCE)
    assert tank.thickness == pytest.approx(
        2.5e6 * 0.5 / (276e6 / 2.0),
        rel=RELATIVE_TOLERANCE,
    )
    # Hand calculation:
    # t = p*r / (sigma_y/FOS) = 9.058 mm
    # m = rho * (V_cyl + V_caps) = 155.76 kg
    assert tank.mass == pytest.approx(155.761101, rel=RELATIVE_TOLERANCE)
