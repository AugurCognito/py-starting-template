# BLUEPRINT — py-starting-template

Design doc for this repo. The Python twin of [ts-starting-template](https://github.com/AugurCognito/ts-starting-template): an agent-ready starter where the harness (verification, hooks, CI, slop scanning) is the product and `src/` is a placeholder. Decisions dated 2026-07-04; every version below was verified live against PyPI / `git ls-remote` on that date.

## Design principles (shared with the TS twin)

1. **Enforcement over prose.** A convention that isn't executed by a tool is a suggestion agents will ignore. Everything in AGENTS.md maps to a gate.
2. **One verify command, three enforcement points.** `make verify` is the single definition of done. It runs in the Claude Code Stop hook, the lefthook pre-push hook, and CI. Local hooks are bypassable; CI is not.
3. **Fast loop / slow gate split.** Per-edit: ruff format+fix (milliseconds, PostToolUse hook). Per-commit: staged-file lint + secret scan. Per-push/per-stop: full verify.
4. **No empty scaffolding.** Nothing ships that doesn't run against the placeholder code today. YAGNI is documented in AGENTS.md's "What does NOT exist" section instead.
5. **Negative space is explicit.** What we deliberately did NOT include, and why, is written down (below and in README) so a future agent doesn't "helpfully" add it.
6. **The code is authoritative.** Docs describe; configs enforce; when they disagree, configs win.

## Stack (verified 2026-07-04)

| Layer | Tool | Version | Why this one |
|---|---|---|---|
| Package manager / task runner / build backend | uv | 0.11.26 (`required-version` pinned) | Single Rust tool: resolver, venv, lock, `uv_build` backend (stable, `uv init` default since 0.11) |
| Supply-chain cooldown | uv `exclude-newer = "7 days"` | — | Rolling-duration form (2026 feature) = pnpm `minimumReleaseAge` equivalent; blocks the takedown window for malicious uploads |
| Lint + format | ruff | ≥0.15.20 | Sole formatter (Black-compatible); explicit strict select — `ALL` is banned because it implicitly enables new rules on upgrade |
| Types | **pyrefly** | ≥1.1.1, `preset = "strict"` | The honest July-2026 pick: 1.0-stable, Rust-fast, ~90% typing-spec conformance. Astral's `ty` is still beta (0.0.56, ~53% conformance) — swap when it hits 1.0. mypy is the legacy incumbent. Pyrefly's *default* preset is permissive — strict must be set explicitly |
| Slop scan | ast-grep (`ast-grep-cli` from PyPI) | latest | 3 bespoke Python rules for what ruff cannot express (see below) |
| Dead code | vulture | ≥2.16 | knip's dead-code half |
| Dependency hygiene | deptry | ≥0.25.1 | unused/missing/transitive deps; native uv support (repo: osprey-oss/deptry) |
| Architecture | import-linter | ≥2.13 | layer contracts = dependency-cruiser equivalent |
| Tests | pytest ≥9.1 + pytest-cov | strict mode | `--strict-markers --strict-config`, `xfail_strict`, `filterwarnings=["error"]`; coverage floor 80% on `src/` |
| Git hooks | lefthook | ≥2.1.9 (PyPI wrapper) | Go binary, parallel, no Node needed; parity with the TS twin. pre-commit (the framework) loses on speed and agent-parseability |
| Conventional commits | commitizen (`cz check`) | ≥4.16.4 | gitlint is unmaintained (last release 2023) |
| Vuln gate | pip-audit in CI | ≥2.10.1 | `uv audit` exists (June 2026) but is preview/unstable — revisit when it graduates |
| Secrets | gitleaks (pre-commit, if installed) + gitleaks-action in CI | v3.0.0 | TruffleHog dropped: no semver-tagged action repo exists to pin cleanly |
| Workflow audit | zizmor | action v0.5.7 | org moved to zizmorcore/ |
| CI | actions SHA-pinned | checkout v7.0.0 | v7 hardens fork-PR checkout (`pull_request_target` pwn-request fix) — do not pin back to v4/v5 |

Python: **3.13** (`requires-python = ">=3.13"`, ruff `target-version = "py313"`). 3.14 exists but 3.13 is where the tooling ecosystem (pyrefly, spacy-class C deps) is fully settled.

## Division of labor: ruff vs ast-grep

Ruff already covers most classic Python slop — these are enabled, not re-implemented:

| Slop pattern | Ruff rule |
|---|---|
| `== None` | E711 |
| bare `except:` | E722 |
| `except: pass` / `except: continue` | S110 / S112 |
| mutable default argument | B006 |
| blanket `# type: ignore` | PGH003 |
| `print()` debugging | T201 |
| commented-out code | ERA001 |
| unused `# noqa` | RUF100 |

ast-grep exists for the three patterns ruff has no rule for (all three were found in the wild in the seed project audit):

- `no-except-return-fallback` — `except` that returns `None`/`[]`/`{}`/`""` — a silent fallback that hides real failures
- `no-raise-exception-wrap` — `raise Exception(e)` inside a handler — destroys the traceback and the type
- `no-narrator-comments` — comments that narrate the next line ("# increment counter", "# now we return")

## The verify pipeline (`make verify`)

```
ruff format --check → ruff check → pyrefly check → ast-grep scan → pytest (cov ≥80%)
→ deptry → vulture → lint-imports → uv build
```

Fail-fast, in cheapest-first order. `uv run` fronts every tool so the env is always synced.

## Test convention

Mirror tree (Elixir convention, adapted to pytest's `test_` prefix requirement): the test for `src/app/foo/bar.py` lives at `tests/foo/test_bar.py`. `tests/` is outside the package — tests never ship in the wheel.

## Negative space — deliberately NOT included

- **release-please / git-cliff** — versioning automation is a per-project choice; wire it when the project has releases (the seed project's config is a good reference).
- **aislop** — the AI-slop scorer stays an optional CI audit (`uvx aislop ci`), referenced in README; the blocking layer must be deterministic rules we own.
- **`uv audit`** — preview; pip-audit is the stable gate until it graduates.
- **TruffleHog** — unpinnable action (see above); gitleaks covers the surface.
- **pre-commit framework** — replaced by lefthook; two hook managers is one too many.
- **Docker/devcontainer runtime images, FastAPI/typer/pydantic** — this template has no runtime opinion. Add with the first real feature.
- **`[tool.uv] dev-dependencies`** — legacy table; its mere presence makes `uv add --dev` keep writing to it. PEP 735 `[dependency-groups]` only.
- **ruff preview mode** — unstable rule set; off.
- **`select = ["ALL"]`** — implicit rule adoption on upgrade; explicit list only.
