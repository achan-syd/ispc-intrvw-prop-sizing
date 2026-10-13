import pytest

from src.propulsion_module.models.materials.material import Material


@pytest.mark.unit
def test_load_material() -> None:
    """Known material loads its properties."""
    material = Material.from_database("Aluminium")
    assert material.density == 2700
    assert material.yield_strength == 276e6


@pytest.mark.unit
def test_load_unknown_material() -> None:
    """Unknown material raises ValueError."""
    with pytest.raises(ValueError, match="not found"):
        Material.from_database("Invalid Material")
