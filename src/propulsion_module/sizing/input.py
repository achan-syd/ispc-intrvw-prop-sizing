"""Sizing Input."""

from dataclasses import dataclass
from typing import Final

import numpy as np
from typing_extensions import Self

PARAM: Final = "PARAM"


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
class SweepDefinition:
    """Sensitivity problem, one parameter swept for every case.

    Attributes:
        parameter: Name of the swept parameter, from where "PARAM" is placed.
        values: Values the parameter takes in the sweep.
        requirements: Requirements, "PARAM" left as the placeholder.
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
            config: Parsed sweep config with the PARAM range [start, interval, stop],
                the requirements and the cases.

        Returns:
            The sweep problem.

        """
        start, interval, stop = config[PARAM]

        # Number of values from start to stop, both ends included
        points = round((stop - start) / interval) + 1

        # Names of the keys holding the placeholder, without repeats
        names = _param_names([config["requirements"], config["cases"]])
        return cls(
            parameter=", ".join(dict.fromkeys(names)),
            values=np.linspace(start, stop, points).tolist(),
            requirements=config["requirements"],
            cases=config["cases"],
        )

    def at_point(self, value: float) -> tuple[Specification, list[dict]]:
        """Replace the placeholder with a value in the requirements and cases.

        Args:
            value: Value of the swept parameter.

        Returns:
            The specification and the cases for that value.

        """
        requirements = _replace_param(self.requirements, value)
        cases = _replace_param(self.cases, value)
        return Specification.from_config({"requirements": requirements}), cases


def _param_names(node: object, name: str = "") -> list[str]:
    """Find the names of the keys that hold the placeholder.

    "pressure": "PARAM"           gives "pressure"
    "pressure": ["PARAM", "bar"]  gives "pressure [bar]"
    """
    # The placeholder itself, the name is the key it sits under
    if node == PARAM:
        return [name]
    # A [placeholder, unit] pair, add the unit to the name
    if isinstance(node, list) and node and node[0] == PARAM:
        return [f"{name} [{node[1]}]"]
    # Any other list, look inside every item
    if isinstance(node, list):
        names = []
        for item in node:
            names += _param_names(item, name)
        return names
    # A dictionary, look inside every key
    if isinstance(node, dict):
        names = []
        for key, value in node.items():
            names += _param_names(value, key)
        return names
    # A number or a string, nothing to find
    return []


def _replace_param(node: object, value: float) -> object:
    """Copy a parsed config with every placeholder replaced by the value."""
    if node == PARAM:
        return value
    if isinstance(node, dict):
        return {key: _replace_param(item, value) for key, item in node.items()}
    if isinstance(node, list):
        return [_replace_param(item, value) for item in node]
    return node
