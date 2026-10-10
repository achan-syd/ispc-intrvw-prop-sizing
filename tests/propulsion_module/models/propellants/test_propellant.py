import pytest

from src.propulsion_module.models.propellants.propellant import Propellant


def test_from_database() -> None:
    propellant = Propellant.from_database("Hydrazine")
    assert propellant.name == "Hydrazine"
    assert propellant.density == 1000


def test_unknown_propellant() -> None:
    with pytest.raises(ValueError, match="not found"):
        Propellant.from_database("Invalid Propellant")
