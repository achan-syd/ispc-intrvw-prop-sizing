"""Shared Study Helpers."""

from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem
from src.propulsion_module.sizing.input import Specification
from src.propulsion_module.sizing.output import SizingResult
from src.propulsion_module.sizing.sizing import size_system


def size_entry(specification: Specification, config: dict) -> SizingResult:
    """Build the system a design config describes and size it."""
    match config["propulsion_module"]["architecture"]:
        case "pressure_fed":
            system = PressureFedSystem.from_config(config)
        case "pump_fed":
            system = PumpFedSystem.from_config(config)
        case architecture:
            raise ValueError(f"Unknown architecture {architecture!r}")
    return size_system(specification, system)


def report_specification(specification: Specification) -> str:
    """Format the specification for the top of the command line output."""
    return (
        "Specification\n"
        f"  delta-V           {specification.delta_v:9.1f} m/s\n"
        f"  thrust-to-weight  {specification.twr:9.2f}\n"
        f"  dry mass          {specification.dry_mass:9.1f} kg\n"
        f"  maximum mass      {specification.maximum_mass:9.1f} kg\n"
        "\n"
    )


def report(module: dict, result: SizingResult) -> str:
    """Format a result for the command line, the name and id are only cosmetic."""
    mass = result.mass
    return (
        f"[{module['id']}] {module['name']}\n"
        f"  propellant mass  {mass.propellant_mass:9.2f} kg\n"
        f"  hardware mass    {mass.hardware_mass:9.2f} kg\n"
        f"  total mass       {mass.total_mass:9.2f} kg\n"
        f"  thrust           {result.thrust:9.1f} N\n"
        f"  margin           {result.margin:9.1%}\n"
    )
