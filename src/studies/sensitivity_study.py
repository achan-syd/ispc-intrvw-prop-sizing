"""Sensitivity Study."""

import json

import matplotlib.pyplot as plt

from src.constants.assets import SENSITIVITY_STUDY
from src.propulsion_module.sizing.input import SweepDefinition
from src.propulsion_module.sizing.output import SizingResult
from src.studies.common import size_entry
from src.studies.plots import plot_sweep


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
