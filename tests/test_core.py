import pytest

from app.core import parse_semver


def test_parses_valid_semver() -> None:
    assert parse_semver("1.2.3") == (1, 2, 3)


def test_rejects_wrong_arity() -> None:
    with pytest.raises(ValueError, match="not a semver string"):
        parse_semver("1.2")


def test_rejects_non_numeric_and_chains_cause() -> None:
    with pytest.raises(ValueError, match="non-numeric component") as excinfo:
        parse_semver("1.x.3")
    assert isinstance(excinfo.value.__cause__, ValueError)
