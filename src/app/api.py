"""Public surface. May import app.core; app.core must never import upward."""

from app.core import parse_semver


def bump_major(version: str) -> str:
    major, _, _ = parse_semver(version)
    return f"{major + 1}.0.0"
