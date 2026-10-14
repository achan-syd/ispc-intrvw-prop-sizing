import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

from src.studies.sensitivity_study import sweep

mpl.use("Agg")


@pytest.mark.integration
def test_sweep_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sweep runs without error."""
    monkeypatch.setattr(plt, "show", lambda: None)
    sweep("sweep_config")
    plt.close("all")
