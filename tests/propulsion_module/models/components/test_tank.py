import math

import pytest

from src.constants.factors import DEFAULT_PRESSURE_VESSEL_FOS
from src.propulsion_module.models.components.tank import (
    PressurantTank,
    PropellantTank,
    Tank,
)
from src.propulsion_module.models.materials.material import Material


@pytest.fixture
def material() -> Material:
    """Aluminium from the database."""
    return Material.from_database("Aluminium")


def test_spherical_tank(material: Material) -> None:
    """Sphere uses the default FOS and thin-wall sizing."""
    tank = Tank.spherical(0.5, 2.5e6, material)
    assert tank.fos == DEFAULT_PRESSURE_VESSEL_FOS
    assert tank.thickness == pytest.approx(2.5e6 * 0.5 / (2 * 276e6 / 1.5))
    assert tank.volume == pytest.approx(4 / 3 * math.pi * 0.5**3)
    assert tank.length == 0
    assert tank.mass > 0


def test_cylindrical_tank(material: Material) -> None:
    """Cylinder keeps its subclass and adds end caps."""
    tank = PropellantTank.cylindrical(0.5, 1.0, 2.5e6, material, fos=2.0)
    assert isinstance(tank, PropellantTank)
    assert tank.fos == 2.0
    assert tank.thickness == pytest.approx(2.5e6 * 0.5 / (276e6 / 2.0))
    assert tank.volume == pytest.approx(
        math.pi * 0.5**2 * 1.0 + 4 / 3 * math.pi * 0.5**3,
    )
    assert tank.mass > 0


def test_propellant_tank_from_config() -> None:
    """Propellant tank also loads its propellant and keeps its subclass."""
    config = {"propellant": "Hydrazine", "material": "Aluminium", "pressure": 1e6}
    tank = PropellantTank.from_config(config)
    assert isinstance(tank, PropellantTank)
    assert tank.propellant.name == "Hydrazine"
    assert tank.max_pressure == 1e6


def test_pressurant_tank_from_config() -> None:
    """Pressurant tank loads its mass factor."""
    tank = PressurantTank.from_config({"mass_factor": 2e-8})
    assert tank.mass_factor == 2e-8
