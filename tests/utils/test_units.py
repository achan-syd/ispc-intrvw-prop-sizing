import pytest

from src.utils.units import to_si, to_si_quantity
from tests.constants import RELATIVE_TOLERANCE


@pytest.mark.unit
def test_si_unit_is_unchanged() -> None:
    """An SI unit returns the value."""
    assert to_si(2e6, "Pa") == 2e6


@pytest.mark.unit
def test_psi_to_pascal() -> None:
    """Psi converts to Pa."""
    assert to_si(1, "psi") == pytest.approx(6894.757, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_unknown_unit() -> None:
    """Unknown unit raises ValueError."""
    with pytest.raises(ValueError, match="Unknown unit"):
        to_si(1, "furlong")


@pytest.mark.unit
def test_quantity_pair_to_si() -> None:
    """A [value, unit] pair converts to SI."""
    assert to_si_quantity([20, "bar"]) == pytest.approx(2e6, rel=RELATIVE_TOLERANCE)


@pytest.mark.unit
def test_quantity_number_is_unchanged() -> None:
    """A plain number is already SI."""
    assert to_si_quantity(2e6) == 2e6
