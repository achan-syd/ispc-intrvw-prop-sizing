"""Entry point."""

import argparse
import json
import sys

import matplotlib.pyplot as plt

from src.constants.assets import (
    COMPARATIVE_STUDY,
    SENSITIVITY_STUDY,
    SIZING_STUDY,
    SPECIFICATIONS,
)
from src.propulsion_module.models.architectures.pressure_fed import PressureFedSystem
from src.propulsion_module.models.architectures.pump_fed import PumpFedSystem
from src.propulsion_module.sizing.input import Specification, SweepDefinition
from src.propulsion_module.sizing.output import SizingResult
from src.propulsion_module.sizing.plot import plot_sweep
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


def compare(study: str) -> None:
    """Size every case of a comparative study against the specification."""
    specification = Specification.from_config(json.loads(SPECIFICATIONS.read_text()))
    cases = json.loads((COMPARATIVE_STUDY / f"{study}.json").read_text())["cases"]

    # Solve every case
    results = []
    for case in cases:
        result = size_entry(specification, case)
        results.append((case, result))

    # Print every result
    for case, result in results:
        sys.stdout.write(f"Case {case['case']}  ")
        sys.stdout.write(report(case["propulsion_module"], result))


def sweep(study: str) -> dict[int, list[SizingResult]]:
    """Size every case of a sensitivity study over the swept values and plot it."""
    config = json.loads((SENSITIVITY_STUDY / f"{study}.json").read_text())
    problem = SweepDefinition.from_config(config)

    # Solve every case at every value of the parameter
    results = {case["case"]: [] for case in problem.cases}
    for value in problem.values:
        specification, cases = problem.at_point(value)
        for case in cases:
            result = size_entry(specification, case)
            results[case["case"]].append(result)

    # Plot thrust and the masses, the swept value at the bottom
    plot_sweep(problem, results)
    plt.show()
    return results


def main(argv: list[str] | None = None) -> int:
    """Run the command line."""
    parser = argparse.ArgumentParser(description="Propulsion system sizing.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("size").add_argument("design")
    commands.add_parser("compare").add_argument("study")
    commands.add_parser("sweep").add_argument("study")

    args = parser.parse_args(argv)
    match args.command:
        case "size":
            size(args.design)
        case "compare":
            compare(args.study)
        case "sweep":
            sweep(args.study)
    return 0


if __name__ == "__main__":
    """Entry Point"""
    sys.exit(main())
