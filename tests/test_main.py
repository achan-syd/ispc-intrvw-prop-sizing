"""Main Test."""

from src.main import main


def test_main() -> None:
    """Main returns exit code 0."""
    assert main(["size", "pressure_fed"]) == 0
