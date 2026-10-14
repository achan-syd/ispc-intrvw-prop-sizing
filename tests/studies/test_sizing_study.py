import pytest

from src.studies.sizing_study import size


@pytest.mark.integration
@pytest.mark.parametrize("design", ["pressure_fed", "pump_fed"])
def test_size_runs(design: str) -> None:
    """Size runs without error."""
    size(design)
