"""Study Plots."""

import itertools
from typing import Final

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

from src.propulsion_module.sizing.input import SweepDefinition
from src.propulsion_module.sizing.output import SizingResult

# Colour and line style of each mass
MASS_STYLES: Final[dict[str, tuple[str, str]]] = {
    "allocated mass": ("black", ":"),
    "tanks": ("#6baed6", "--"),
    "feed system": ("#2171b5", "--"),
    "engine": ("#9ecae1", "--"),
    "dry mass": ("#08306b", "--"),
    "propellant": ("tab:orange", "-"),
    "total": ("tab:purple", "-"),
}


def plot_sweep(
    problem: SweepDefinition,
    results: dict[int, list[SizingResult]],
) -> Figure:
    """Plot thrust, every mass component and the margin against the swept value."""
    figure, axes = plt.subplots(
        3,
        len(problem.cases),
        sharex=True,
        sharey="row",
        squeeze=False,
        figsize=(6 * len(problem.cases), 10),
    )

    for column, case in enumerate(problem.cases):
        sized = results[case["case"]]
        module = case["propulsion_module"]
        thrust_axis, mass_axis, margin_axis = axes[:, column]

        thrust_axis.plot(
            problem.values,
            [result.thrust for result in sized],
            color="black",
        )
        thrust_axis.set_title(f"[{module['id']}] {module['name']}")

        # Dry mass is the allocated mass plus the propulsion system mass
        components = {
            "allocated mass": [r.mass.hardware_mass - r.system.mass for r in sized],
            "tanks": [sum(t.mass for t in r.system.propellant_tanks) for r in sized],
            "feed system": [sum(f.mass for f in r.system.feed_systems) for r in sized],
            "engine": [sum(e.mass for e in r.system.engines) for r in sized],
            "dry mass": [r.mass.hardware_mass for r in sized],
            "propellant": [r.mass.propellant_mass for r in sized],
            "total": [r.mass.total_mass for r in sized],
        }
        for label, masses in components.items():
            color, linestyle = MASS_STYLES[label]
            mass_axis.plot(
                problem.values,
                masses,
                label=label,
                color=color,
                linestyle=linestyle,
            )
        mass_axis.legend()

        # Margin in percent, green where the requirement is met and red where not
        margins = [result.margin * 100 for result in sized]
        points = np.column_stack([problem.values, margins]).reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = [
            "tab:green" if (start + end) / 2 >= 0 else "tab:red"
            for start, end in itertools.pairwise(margins)
        ]
        margin_axis.add_collection(LineCollection(segments, colors=colors))
        margin_axis.autoscale_view()
        margin_axis.axhline(0, color="black", linewidth=1)
        margin_axis.set_xlabel(problem.parameter)

    axes[0, 0].set_ylabel("Thrust [N]")
    axes[1, 0].set_ylabel("Mass [kg]")
    axes[2, 0].set_ylabel("Margin [%]")
    for axis in axes.flat:
        axis.grid(visible=True)
    figure.tight_layout()
    return figure
