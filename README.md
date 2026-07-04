# py-starting-template

Agent-ready Python starter. Replace `src/app/` with real code — the harness around it (verification, hooks, CI, slop scanning) is the product. Design rationale and verified tool versions: [BLUEPRINT.md](BLUEPRINT.md). The TypeScript twin: [ts-starting-template](https://github.com/AugurCognito/ts-starting-template).

## Quick start

```bash
uv sync            # install everything (uv only — pip is not part of this workflow)
make setup         # uv sync + install git hooks
make verify        # THE definition of done
```

## Enforcement map

Every convention is executed by a tool — nothing is prose-only:

| Concern | Tool | Runs at |
|---|---|---|
| Format + lint (strict explicit ruleset) | ruff | on every agent file-edit (hook), pre-commit, verify |
| Types (strict) | pyrefly | pre-push, verify |
| AI-slop AST patterns | ast-grep (`slop-rules/`) | pre-push, verify |
| Tests + 80% branch coverage | pytest / coverage | pre-push, verify |
| Unused/missing/transitive deps | deptry | verify |
| Dead code | vulture | verify |
| Architecture layers | import-linter | verify |
| Wheel actually builds | uv build | verify |
| Conventional commits | commitizen | commit-msg hook |
| Secrets | gitleaks | pre-commit (if installed), CI |
| Dependency cooldown (7 days) | uv `exclude-newer` | every resolve |
| Vulnerable deps | pip-audit | CI |
| Workflow security | zizmor | CI |
| Static analysis | CodeQL | CI |

`make verify` is the single definition of done, enforced at three points: the Claude Code Stop hook, the lefthook pre-push hook, and CI. Local hooks are bypassable; CI is not.

## Anti-slop

`slop-rules/*.yml` are ast-grep rules for patterns ruff cannot express — silent `except → return None` fallbacks, `raise Exception(e)` traceback destruction, narrator comments. Ruff's own rules cover the classics (`E711`, `E722`, `S110/S112`, `B006`, `PGH003`, `T201`, `ERA001`); see the mapping in [BLUEPRINT.md](BLUEPRINT.md). Extending the rule set = dropping a new `.yml` into `slop-rules/`.

Optional deeper audit: `uvx aislop ci` (kept out of the blocking path deliberately — the gate must be deterministic rules we own).

## After instantiating this template (one-time, manual)

- [ ] Rename the package: `src/app` → yours, plus `module-name`, `known_first_party`, `root_package`, coverage `--cov` target in `pyproject.toml`
- [ ] Update `.github/CODEOWNERS`
- [ ] Enable branch protection on `main` (require CI + code-owner review)
- [ ] Enable secret-scanning push protection (repo Settings → Security)
- [ ] Install the Renovate app (config ships in `.github/renovate.json5`); optionally Socket
- [ ] Keep the shipped `codeql.yml` or switch to GitHub default setup — not both
- [ ] `brew install gitleaks` locally so the pre-commit secret scan is active
- [ ] Releases? Wire release-please + git-cliff then (deliberately not shipped — see BLUEPRINT negative space)
