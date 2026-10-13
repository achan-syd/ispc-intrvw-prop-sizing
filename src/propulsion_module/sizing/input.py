"""Sizing Input."""

from dataclasses import dataclass

import numpy as np
from typing_extensions import Self


@dataclass(frozen=True)
class Specification:
    """Top-level requirements the system is sized against.

    Attributes:
        delta_v: Required change in velocity [m/s].
        twr: Required thrust-to-weight ratio at ignition [-].
        dry_mass: Dry mass excluding the propulsion system [kg].
        maximum_mass: Maximum initial mass [kg].

    """

    delta_v: float
    twr: float
    dry_mass: float
    maximum_mass: float

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the specification from a loaded JSON config.

        Args:
            config: Parsed specification config, with a requirements section.

        Returns:
            The specification.

        """
        requirements = config["requirements"]
        return cls(
            delta_v=requirements["delta_v"],
            twr=requirements["twr"],
            dry_mass=requirements["dry_mass"],
            maximum_mass=requirements["maximum_mass"],
        )


@dataclass(frozen=True)
class Sweep:
    """Sensitivity problem, one requirement swept for every case.

    Attributes:
        parameter: Name of the requirement being swept.
        values: Values the parameter takes in the sweep.
        requirements: Requirements, with the swept one still the placeholder.
        cases: Design cases, each with a case number and a propulsion_module.

    """

    parameter: str
    values: list[float]
    requirements: dict
    cases: list[dict]

    @classmethod
    def from_config(cls, config: dict) -> Self:
        """Build the sweep from a loaded JSON config.

        Args:
            config: Parsed sweep config with PARAM as [start, interval, stop],
                requirements where one value is "PARAM", and the cases.

        Returns:
            The sweep problem.

        """
        start, interval, stop = config["PARAM"]
        requirements = config["requirements"]

        # The requirement being swept is the one set to "PARAM"
        for name, value in requirements.items():
            if value == "PARAM":
                parameter = name
                break
        else:
            raise ValueError('No requirement is set to "PARAM"')

        # Number of values from start to stop, both ends included
        points = round((stop - start) / interval) + 1
        return cls(
            parameter=parameter,
            values=np.linspace(start, stop, points).tolist(),
            requirements=requirements,
            cases=config["cases"],
        )
