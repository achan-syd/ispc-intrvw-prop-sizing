"""Sizing Study."""

import json
import sys

from src.constants.assets import SIZING_STUDY, SPECIFICATIONS
from src.propulsion_module.sizing.input import Specification
from src.propulsion_module.sizing.output import SizingResult
from src.studies.common import report, report_specification, size_entry


def size(design: str) -> SizingResult:
    """Size a design from the sizing study against the specification."""
    specification = Specification.from_config(json.loads(SPECIFICATIONS.read_text()))
    config = json.loads((SIZING_STUDY / f"{design}.json").read_text())

    result = size_entry(specification, config)
    sys.stdout.write(report_specification(specification))
    sys.stdout.write(report(config["propulsion_module"], result))
    return result
