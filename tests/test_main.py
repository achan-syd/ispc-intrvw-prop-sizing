"""Main Test."""

import pytest

from src.main import main


@pytest.mark.unit
def test_main() -> None:
    """Main returns exit code 0."""
    assert main(["size", "pressure_fed"]) == 0
