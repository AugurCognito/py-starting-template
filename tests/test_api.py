import pytest

from app.api import bump_major


def test_bumps_major_and_resets_rest() -> None:
    assert bump_major("1.2.3") == "2.0.0"


def test_propagates_parse_errors() -> None:
    with pytest.raises(ValueError, match="not a semver string"):
        bump_major("nonsense")
