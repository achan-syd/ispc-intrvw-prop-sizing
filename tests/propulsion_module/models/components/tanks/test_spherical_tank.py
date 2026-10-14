import math

import pytest

from src.propulsion_module.models.components.tanks.spherical_tank import SphericalTank
from src.propulsion_module.models.materials.material import Material
from tests.constants import RELATIVE_TOLERANCE


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
    assert tank.radius == pytest.approx(0.5, rel=RELATIVE_TOLERANCE)
    assert tank.thickness == pytest.approx(
        2.5e6 * 0.5 / (2 * 276e6 / 1.5),
        rel=RELATIVE_TOLERANCE,
    )
    # Hand calculation:
    # t = p*r / (2*sigma_y/FOS) = 3.397 mm
    # m = rho * V_shell = 29.01 kg
    assert tank.mass == pytest.approx(29.008339, rel=RELATIVE_TOLERANCE)
