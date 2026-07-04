# AGENTS.md

Single source of truth for AI coding agents. `CLAUDE.md` imports this file; Codex, Cursor, Copilot, and Gemini read it natively. Keep it under 200 lines.

## What This Is

An agent-ready Python starter. Replace `src/app/` with real code; the harness around it (verification, hooks, CI, slop scanning) is the product.

## Commands

```bash
uv sync             # install — uv only; pip/poetry are not part of this workflow
make setup          # uv sync + install git hooks
make verify         # THE definition of done: lint + types + slop + tests + deps + dead code + arch + build
make fmt            # ruff auto-fix + format (also runs on every file edit via hooks)
uv run pytest       # tests only, TDD loop
uv add <pkg>        # add a dependency (never edit uv.lock by hand)
uv add --group lint <pkg>   # add a tool to a dependency group
```

## Definition of Done

A task is **not complete** until `make verify` passes. No exceptions. The Stop hook, pre-push hook, and CI all run it — a claim of "done" with a failing verify will be caught three times.

## Conventions

1. **The code is authoritative.** Read the current source before acting. When a doc disagrees with the code, the code wins — then fix the doc.
2. **No fallback mechanisms.** They hide real failures. No `except: return None` (the slop scanner rejects it); raise domain errors with `from exc`; flag blockers instead of working around them.
3. **Less code beats more code.** Rewrite existing modules over adding parallel ones. Delete dead code on sight (vulture will catch what you miss).
4. **Every function signature is typed.** pyrefly runs strict; untyped defs fail verify.
5. **Comments state constraints the code cannot express** — never what the next line does. The slop scanner rejects narrator comments.
6. **Don't self-QA claims.** "It works" means `make verify` passed; behavior claims need the human to verify real output.
7. **Conventional commits** (`feat:`, `fix:`, `chore:`, …) — enforced by commitizen.
8. **Absolute dates in docs** (2026-07-04, never "yesterday").
9. **Throwaway output goes in `scratch/`** (gitignored) — never the repo root.
10. **Secrets live in `.env`** (gitignored); commit only `.env.example` with placeholders. Never read or print `.env*` contents.

## Architecture

- `src/app/` — the package (src layout; rename per project). `tests/` — pytest tests **mirroring the package tree** (Elixir convention): `src/app/foo/bar.py` → `tests/foo/test_bar.py`. 80% branch-coverage floor.
- Layering is enforced by import-linter: `app.api` may import `app.core`, never the reverse. Extend the contract in `pyproject.toml` as layers grow.
- `slop-rules/` — ast-grep AST rules against LLM-slop patterns ruff can't express. Ruff covers the classics (E711, E722, S110/S112, B006, PGH003, T201, ERA001).
- Gates: lefthook (`lefthook.yml`) locally, `.github/workflows/ci.yml` in CI. Local hooks are bypassable; CI is not.

## What Does NOT Exist (yet)

No runtime dependencies, no CLI entrypoint, no server, no database, no Docker, no release automation. Don't scaffold any of these speculatively (YAGNI) — add them when a task requires them, and update this section when you do.

## Session Workflow

- Long task? Write a plan first (`/plan` command → `docs/plans/`).
- Ending a session mid-task? Update `docs/HANDOFF.md` (`/handoff` command).
- Found something non-obvious? Record it (`/report` command) or update this file — with the WHY, not just the WHAT.
