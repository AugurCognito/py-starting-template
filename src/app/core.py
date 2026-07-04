"""Placeholder domain logic. Replace with real code; keep the error discipline."""

SEMVER_PARTS = 3


def parse_semver(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) != SEMVER_PARTS:
        raise ValueError(f"not a semver string: {value!r}")
    try:
        major, minor, patch = (int(part) for part in parts)
    except ValueError as exc:
        raise ValueError(f"non-numeric component in {value!r}") from exc
    return (major, minor, patch)
