"""Study Plots."""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from src.propulsion_module.sizing.input import SweepDefinition
from src.propulsion_module.sizing.output import SizingResult


def plot_sweep(
    problem: SweepDefinition,
    results: dict[int, list[SizingResult]],
) -> Figure:
    """Plot thrust and every mass component against the swept value, per case."""
    figure, axes = plt.subplots(
        2,
        len(problem.cases),
        sharex=True,
        sharey="row",
        squeeze=False,
        figsize=(6 * len(problem.cases), 7),
    )

    for column, case in enumerate(problem.cases):
        sized = results[case["case"]]
        module = case["propulsion_module"]
        thrust_axis, mass_axis = axes[0, column], axes[1, column]

        thrust_axis.plot(problem.values, [result.thrust for result in sized])
        thrust_axis.set_title(f"[{module['id']}] {module['name']}")

        components = {
            "propellant": [r.mass.propellant_mass for r in sized],
            "tanks": [sum(t.mass for t in r.system.propellant_tanks) for r in sized],
            "feed system": [sum(f.mass for f in r.system.feed_systems) for r in sized],
            "dry mass": [r.mass.hardware_mass - r.system.mass for r in sized],
            "total": [r.mass.total_mass for r in sized],
        }
        for label, masses in components.items():
            mass_axis.plot(problem.values, masses, label=label)
        mass_axis.legend()
        mass_axis.set_xlabel(problem.parameter)

    axes[0, 0].set_ylabel("Thrust [N]")
    axes[1, 0].set_ylabel("Mass [kg]")
    for axis in axes.flat:
        axis.grid(visible=True)
    figure.tight_layout()
    return figure
