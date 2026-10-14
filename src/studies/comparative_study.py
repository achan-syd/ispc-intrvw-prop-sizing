"""Comparative Study."""

import json
import sys

from src.constants.assets import COMPARATIVE_STUDY, SPECIFICATIONS
from src.propulsion_module.sizing.input import Specification
from src.studies.common import report, report_specification, size_entry


def compare(study: str) -> None:
    """Size every case of a comparative study against the specification."""
    specification = Specification.from_config(json.loads(SPECIFICATIONS.read_text()))
    cases = json.loads((COMPARATIVE_STUDY / f"{study}.json").read_text())["cases"]

    # Solve every case
    results = []
    for case in cases:
        result = size_entry(specification, case)
        results.append((case, result))

    # Print the specification, then every result
    sys.stdout.write(report_specification(specification))
    for case, result in results:
        sys.stdout.write(f"Case {case['case']}  ")
        sys.stdout.write(report(case["propulsion_module"], result))
