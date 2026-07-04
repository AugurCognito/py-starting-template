# Why your new dependency is blocked

This repo enforces a supply-chain cooldown: uv's `exclude-newer = "7 days"` (`[tool.uv]` in `pyproject.toml`) refuses to resolve any package version published less than a rolling 7 days ago. Renovate additionally waits 3 days (`minimumReleaseAge` in `.github/renovate.json5`) before proposing updates.

**Why**: most PyPI supply-chain attacks are caught within days of a malicious publish. Refusing day-zero versions means the ecosystem finds the compromise before this repo installs it.

**Symptoms you'll see**:

- `uv add <pkg>` or `uv lock` resolves an *older* version than pypi.org shows — the latest is younger than the cooldown.
- Resolution fails outright when a version floor is only satisfiable by a too-new release (typical when pinning `>=X.Y.Z` to a release published in the last week).

**What to do**:

- Default: use the older version, or wait out the window.
- If a floor genuinely requires a brand-new release (e.g., a security fix), loosen the floor rather than removing the cooldown — and if that's impossible, flag it to the human. Do not delete `exclude-newer` to make an install pass.

**Real incident**: on 2026-07-04, `import-linter` 2.13 (released the day before, 2026-07-03) was blocked by this repo's own cooldown when adding the `quality` dependency group. The fix was loosening the version floor to `import-linter>=2.11` (still satisfied by the older, cooldown-eligible release) — never dropping `exclude-newer`.
