"""Sizing Definition."""

from scipy.optimize import brentq

from src.constants.factors import SIZING_TOLERANCE, SIZING_UPPER_BOUND_FACTOR
from src.constants.universal import LUNAR_GRAVITY
from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem
from src.propulsion_module.sizing.input import Specification
from src.propulsion_module.sizing.output import SizingResult, SystemMass
from src.propulsion_module.solvers.rocket_equation import rocket_equation
from src.propulsion_module.solvers.thrust_to_weight_ratio import (
    thrust_to_weight_ratio,
)


def _size_at(
    specification: Specification,
    system: PressureFedSystem | PumpFedSystem,
    init_mass: float,
) -> SizingResult:
    """Size the system for a trial initial mass."""
    # Propellant mass [kg] from the rocket equation, final mass is what is left
    isp = system.engines[0].isp
    final_mass = rocket_equation(specification.delta_v, isp, initial_mass=init_mass)
    prop_mass = init_mass - final_mass

    # Thrust [N] for the thrust-to-weight ratio at ignition
    thrust = thrust_to_weight_ratio(
        twr=specification.twr,
        mass=init_mass,
        gravity=LUNAR_GRAVITY,
    )

    # Size the hardware from the propellant and the thrust
    sized = system.size(prop_mass, thrust)

    # Hardware mass [kg], dry mass plus the sized propulsion hardware
    hardware_mass = specification.dry_mass
    hardware_mass += sum(tank.mass for tank in sized.propellant_tanks)
    hardware_mass += sum(feed.mass for feed in sized.feed_systems)
    hardware_mass += sum(engine.mass or 0.0 for engine in sized.engines)

    mass = SystemMass(prop_mass, hardware_mass)
    margin = (specification.maximum_mass - mass.total_mass) / specification.maximum_mass
    return SizingResult(sized, mass, thrust, margin)


def _residual_function(
    init_mass: float,
    specification: Specification,
    system: PressureFedSystem | PumpFedSystem,
) -> float:
    """Compute the residual function.

    f(m_0) = m_0 - (m_prop + m_hw) = 0

    Where:
        f(m_0): residual function
        m_0: initial mass [kg]
        m_prop: propellant mass [kg]
        m_hw: hardware mass, dry mass plus the sized propulsion hardware [kg]
    """
    return init_mass - _size_at(specification, system, init_mass).mass.total_mass


def size_system(
    specification: Specification,
    system: PressureFedSystem | PumpFedSystem,
) -> SizingResult:
    """Size a propulsion system against a specification.

    A trial initial mass sizes the system, and it is right when the sized system
    adds up to that same mass. brentq finds that initial mass.

    Args:
        specification: Requirements to size against.
        system: Unsized propulsion system.

    Returns:
        The sized system and its summary.

    Raises:
        ValueError: If the design does not close.

    """
    lower_mass_bound = specification.dry_mass
    upper_mass_bound = SIZING_UPPER_BOUND_FACTOR * specification.maximum_mass
    if _residual_function(upper_mass_bound, specification, system) <= 0:
        raise ValueError("Unable to meet design constraints")

    init_mass = brentq(
        _residual_function,
        lower_mass_bound,
        upper_mass_bound,
        args=(specification, system),
        xtol=SIZING_TOLERANCE,
    )
    return _size_at(specification, system, init_mass)
