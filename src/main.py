"""Entry point.

Usage:
    main size <design>    size src/configs/sizing_study/<design>.json
    main compare
    main sweep
"""

import argparse
import json
import sys

from src.constants.assets import SIZING_STUDY, SPECIFICATIONS
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


def size(design: str) -> SizingResult:
    """Size a design from the sizing study against the specification."""
    specification = Specification.from_config(json.loads(SPECIFICATIONS.read_text()))
    config = json.loads((SIZING_STUDY / f"{design}.json").read_text())

    result = size_entry(specification, config)
    sys.stdout.write(report(config["propulsion_module"], result))
    return result


def compare() -> None:
    """Size every case of a comparative study against the specification."""
    raise NotImplementedError


def sweep() -> None:
    """Size an architecture over a range of one parameter."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Run the command line."""
    parser = argparse.ArgumentParser(description="Propulsion system sizing.")
    commands = parser.add_subparsers(dest="command", required=True)
    designs = sorted(path.stem for path in SIZING_STUDY.glob("*.json"))
    commands.add_parser("size").add_argument("design", choices=designs)
    commands.add_parser("compare")
    commands.add_parser("sweep")

    args = parser.parse_args(argv)
    match args.command:
        case "size":
            size(args.design)
        case "compare":
            compare()
        case "sweep":
            sweep()
    return 0


if __name__ == "__main__":
    """Entry Point"""
    sys.exit(main())
