# Python agent-harness tooling — research snapshot, 2026-07-04

Live-verified (PyPI JSON API + `git ls-remote`) on 2026-07-04. This is why the stack in BLUEPRINT.md looks the way it does; re-verify before copying into a new context.

## Type checker: why pyrefly, not ty or mypy

| Checker | Version | Status 2026-07 | Typing-spec conformance |
|---|---|---|---|
| **pyrefly** (Meta) | 1.1.1 | 1.0 since May 2026; runs Instagram-scale code; adopted by PyTorch/NumPy/JAX | ~88-90% |
| ty (Astral) | 0.0.56 | **beta**, stable targeted ~2027 | ~53% |
| pyright | 1.1.411 | mature, conformance king (97.8%) | but Node-based |
| mypy | 2.1.0 | maintained; greenfield ecosystem migrating off | 58.3% |

Swap to `ty` when it hits 1.0 if you want an all-Astral toolchain. Two pyrefly gotchas encoded in our config: (1) the unconfigured default is a permissive "basic" preset — `preset = "strict"` **must** be explicit (verified empirically: default misses untyped defs, strict catches them); (2) pyrefly does not follow strict semver — minor upgrades can introduce new errors.

## uv facts the template relies on

- `exclude-newer = "7 days"` — rolling-duration form + `exclude-newer-package` overrides landed in 2026; this is the pnpm-`minimumReleaseAge` equivalent. Side effect: a floor like `pkg>=X` fails resolution if X was released <7 days ago — loosen the floor, don't drop the cooldown (hit this live with import-linter 2.13, released 2026-07-03).
- `uv_build` backend is stable and the `uv init` default since 0.11.
- PEP 735 `[dependency-groups]` replaces `[tool.uv] dev-dependencies`; never include the legacy table (its presence redirects `uv add --dev`).
- `uv audit` exists (2026-06) but is preview — pip-audit stays the blocking CI gate.
- uv.lock schema is public API (VERSION=1, REVISION=3); commit it.
- Renovate updates pyproject + uv.lock together via the `pep621` manager.

## Slop-scanning division of labor (tested against a planted slop file)

Ruff owns: E711 (`== None`), E722 (bare except), S110/S112 (except-pass/continue), B006 (mutable defaults), B904 (raise without `from`), PGH003 (blanket type-ignore), T201 (print), ERA001 (commented-out code), RUF100 (unused noqa).

ast-grep (`slop-rules/`) owns what ruff can't express: except-return-fallback, `raise Exception(e)` wrapping, narrator comments. All three verified firing; `make verify` exits non-zero with the planted file, zero without.

Python AI-slop scorers exist (aislop v0.13.1 — same family as the TS twin's reference; sloppylint; vibecheck) — none bundled; deterministic rules we own stay the blocking layer, `uvx aislop ci` is the optional audit.

## Dead-code trio (knip needs three tools in Python)

vulture 2.16 (dead code; `min_confidence = 80` filters its noisy 60%-confidence unused-function guesses), deptry 0.25.1 (deps; repo moved to osprey-oss/), import-linter 2.13 (layer contracts; seddonym/).

## CI notes

- actions/checkout v7.0.0 is a security release (fork-PR checkout hardening for `pull_request_target`) — don't regress to v4/v5 pins.
- TruffleHog has **no semver-tagged action repo** to pin — dropped; gitleaks (docker image, pinned tag) covers secrets in CI.
- gitleaks-action v3 requires a license key for org-owned repos — another reason we run the gitleaks docker image directly.
- zizmor moved orgs: zizmorcore/.
- Known quirk: path-filtered workflows (zizmor) don't fire on a brand-new branch's initial push — `workflow_dispatch` added as escape hatch.

## Unverified / judgment calls

- `fail_under = 80`: no ecosystem consensus exists (strict greenfields use 100, legacy uses 80); 80 chosen for parity with the TS twin. Ratchet up deliberately.
- Ruff preview mode off: inferred from absence in real-world templates, no authoritative source.
- Watch: `prek` (pre-commit-compatible runner referenced in commitizen docs) — spotted, not evaluated.
