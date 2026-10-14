import pytest

from src.studies.comparative_study import compare


@pytest.mark.integration
def test_compare_runs() -> None:
    """Compare runs without error."""
    compare("pressure_vs_pump")
