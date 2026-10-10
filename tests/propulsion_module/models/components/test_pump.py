from src.propulsion_module.models.components.pump import Pump


def test_from_config() -> None:
    """Pump section loads its mass factor."""
    pump = Pump.from_config({"mass_factor": 0.008})
    assert pump.mass_factor == 0.008
    assert pump.mass is None
