import math
from typing import Final

import pytest

from src.constants.universal import EARTH_GRAVITY, LUNAR_GRAVITY
from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem
from src.propulsion_module.sizing.input import Specification
from src.propulsion_module.sizing.output import SizingResult
from src.propulsion_module.sizing.sizing import size_system

# Specification
DELTA_V: Final = 2000  # m/s
TWR: Final = 1.5  # -
DRY_MASS: Final = 600  # kg
MAXIMUM_MASS: Final = 1500  # kg

# Pressure fed design
PRESSURE_FED_TANK_PRESSURE: Final = [25, "bar"]
PRESSURE_FED_ISP: Final = 310  # s
PRESSURE_FED_INLET_PRESSURE: Final = [20, "bar"]
PRESSURANT_MASS_FACTOR: Final = 2e-8  # 1/Pa, 0.002 /bar

# Pump fed design
PUMP_FED_TANK_PRESSURE: Final = [10, "bar"]
PUMP_FED_ISP: Final = 330  # s
PUMP_FED_INLET_PRESSURE: Final = [40, "bar"]
PUMP_MASS_FACTOR: Final = 0.008  # kg/N


def assert_meets_specification(result: SizingResult, isp: float) -> None:
    """Check the result meets the specification."""
    total_mass = result.mass.total_mass
    final_mass = total_mass - result.mass.propellant_mass

    # Delta-V from the rocket equation meets the requirement
    assert isp * EARTH_GRAVITY * math.log(total_mass / final_mass) == pytest.approx(
        DELTA_V,
    )
    # Thrust over the weight on the moon meets the requirement
    assert result.thrust / (total_mass * LUNAR_GRAVITY) == pytest.approx(TWR)
    # Hardware mass is the dry mass plus the sized propulsion hardware
    assert result.mass.hardware_mass == pytest.approx(DRY_MASS + result.system.mass)
    # Total mass is within the maximum
    assert total_mass <= MAXIMUM_MASS


@pytest.mark.integration
def test_size_pressure_fed_meets_the_specification() -> None:
    """Pressure fed design meets the specification."""
    specification = Specification(
        delta_v=DELTA_V,
        twr=TWR,
        dry_mass=DRY_MASS,
        maximum_mass=MAXIMUM_MASS,
    )
    system = PressureFedSystem.from_config(
        {
            "propulsion_module": {
                "tank": {
                    "propellant": "Hydrazine",
                    "material": "Aluminium",
                    "pressure": PRESSURE_FED_TANK_PRESSURE,
                },
                "engine": {
                    "isp": PRESSURE_FED_ISP,
                    "inlet_pressure": PRESSURE_FED_INLET_PRESSURE,
                },
                "pressurant": {
                    "mass_factor": PRESSURANT_MASS_FACTOR,
                },
            },
        },
    )

    result = size_system(specification, system)

    assert_meets_specification(result, PRESSURE_FED_ISP)


@pytest.mark.integration
def test_size_pump_fed_meets_the_specification() -> None:
    """Pump fed design meets the specification."""
    specification = Specification(
        delta_v=DELTA_V,
        twr=TWR,
        dry_mass=DRY_MASS,
        maximum_mass=MAXIMUM_MASS,
    )
    system = PumpFedSystem.from_config(
        {
            "propulsion_module": {
                "tank": {
                    "propellant": "Hydrazine",
                    "material": "Aluminium",
                    "pressure": PUMP_FED_TANK_PRESSURE,
                },
                "engine": {
                    "isp": PUMP_FED_ISP,
                    "inlet_pressure": PUMP_FED_INLET_PRESSURE,
                },
                "pump": {
                    "mass_factor": PUMP_MASS_FACTOR,
                },
            },
        },
    )

    result = size_system(specification, system)

    assert_meets_specification(result, PUMP_FED_ISP)
