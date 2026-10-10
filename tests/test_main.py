"""Main Test."""

from src.main import main


def test_main() -> None:
    """Main returns exit code 0."""
    assert main() == 0
