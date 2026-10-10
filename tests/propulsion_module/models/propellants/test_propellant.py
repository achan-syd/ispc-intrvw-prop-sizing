import pytest

from src.propulsion_module.models.propellants.propellant import Propellant


def test_load_propellant() -> None:
    """Known propellant loads its density."""
    propellant = Propellant.from_database("Hydrazine")
    assert propellant.name == "Hydrazine"
    assert propellant.density == 1000


def test_load_unknown_propellant() -> None:
    """Unknown propellant raises ValueError."""
    with pytest.raises(ValueError, match="not found"):
        Propellant.from_database("Invalid Propellant")
