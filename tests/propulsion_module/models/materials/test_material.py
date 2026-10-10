import pytest

from src.propulsion_module.models.materials.material import Material


def test_from_database() -> None:
    material = Material.from_database("Aluminium")
    assert material.density == 2700
    assert material.yield_strength == 276e6


def test_unknown_material() -> None:
    with pytest.raises(ValueError, match="not found"):
        Material.from_database("Invalid Material")
