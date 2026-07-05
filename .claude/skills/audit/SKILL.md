---
name: audit
description: Use when the user asks for a weekly audit or drift check — sweeps for plan drift, doc/code drift, stale handoff, and slop accumulation; writes docs/reports/<date>-audit.md.
disable-model-invocation: true
---

# /audit — weekly drift & slop sweep

Read-only sweep; findings go to `docs/reports/<yyyy-mm-dd>-audit.md` (same frontmatter schema as /report). Check, in order:

1. **Plan drift** — any plan in `docs/plans/` with `status: approved` but no matching commits since its date; any `status: done` plan not yet archived.
2. **Handoff currency** — `docs/HANDOFF.md` `updated:` older than the latest commit, or its `last_green_verify` stale/failed.
3. **Decision contradictions** — entries in `docs/decisions.md` the code now contradicts (spot-check the newest five).
4. **Doc/code drift** — README and AGENTS.md claims that no longer hold (commands, structure, "What Does NOT Exist" entries that now exist).
5. **Slop accumulation** — duplication trend and new fallback/catch-and-continue branches: run `uv run ast-grep scan --error` and `uv run vulture`, compare against the previous audit report.
6. **Test honesty** — mutation spot-check on modules touched since the last audit: `PYTEST_ADDOPTS=--no-cov uvx --with pytest-cov mutmut run "app.<module>*"` (config lives in `[tool.mutmut]` in pyproject.toml; `--no-cov` because the coverage floor would spuriously kill mutants under test subsetting). Surviving mutants = tests that assert nothing.

Rules: findings only — never fix during the audit; each finding gets file:line and a proposed next action; if a category is clean, say so in one line. If the audit decides something, append it to `docs/decisions.md`.
