"""Main Test."""

from src.main import main


def test_main() -> None:
    """Test Main."""
    assert main() == 0
