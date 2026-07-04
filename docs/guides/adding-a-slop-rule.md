# Adding a slop rule

How to add an ast-grep rule to `slop-rules/` — and prove it works before shipping it.

1. Write the rule as `slop-rules/<kebab-name>.yml`:

   ```yaml
   id: no-example-pattern
   language: python
   severity: error
   message: One sentence on WHY this pattern is banned — it shows in the failure output.
   rule:
     # match by AST structure, not text — see existing rules for the idiom
   ```

2. **Plant the failure.** Add a file under `src/app/` that contains exactly the banned pattern.
3. Run `make slop` — it must fail, naming your rule. A rule you never saw fire is a rule you can't trust.
4. Delete the plant, run `make slop` again — it must pass clean.
5. Check the rule doesn't fire on the existing codebase for legitimate code. If it does, tighten the pattern; don't weaken the message.
6. Run `make verify` and commit rule + (if the rule encodes a new convention) an entry in `docs/decisions.md`.

Existing rules in `slop-rules/` are the reference for matcher idioms (`kind`, `pattern`, `inside`, `has`, `regex`).

Before writing a new rule, check whether ruff already covers it: the classic banned patterns — bare `except` (E722), `print()` left behind (T201), commented-out code (ERA001) — are ruff's job (see the `select` list in `pyproject.toml`). Only reach for ast-grep when the pattern is AST-shaped in a way ruff's rule set can't express, e.g. a specific fallback-return shape inside an `except` block.
