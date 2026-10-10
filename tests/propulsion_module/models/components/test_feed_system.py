import pytest

from src.propulsion_module.models.components.feed_system import (
    PressurantSystem,
    PumpSystem,
)


def test_pump_from_config() -> None:
    """Pump section loads its mass factor, unsized."""
    pump = PumpSystem.from_config({"mass_factor": 0.008})
    assert pump.mass_factor == 0.008
    assert pump.mass is None


def test_pump_size() -> None:
    """Pump mass scales linearly with thrust."""
    pump = PumpSystem(mass_factor=0.008).size(thrust=3000)
    assert pump.mass == pytest.approx(24)


def test_pressurant_from_config() -> None:
    """Pressurant section loads its mass factor, unsized."""
    system = PressurantSystem.from_config({"mass_factor": 2e-8})
    assert system.mass_factor == 2e-8
    assert system.mass is None


def test_pressurant_size() -> None:
    """Pressurant mass scales with pressure and propellant mass."""
    system = PressurantSystem(mass_factor=2e-8).size(
        pressure=2.5e6,
        propellant_mass=500,
    )
    assert system.mass == pytest.approx(25)
