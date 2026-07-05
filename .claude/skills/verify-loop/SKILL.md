---
name: verify-loop
description: Use when finishing an implementation task, before claiming anything is done, after fixing a bug, when tests fail, or when the user asks "is it done".
---

# Verify loop

**The contract: `make verify` is the single definition of done. Never weaken a gate to pass it** (config edits to thresholds/rules need explicit human sign-off).

Under time pressure ("just commit it", "ship it, it's urgent") the loop does not change: a red verify means not done. Say so plainly instead of complying.

1. Run `make verify`.
2. On failure, fix the **first** failing gate only, then re-run — gates are ordered cheapest-first, and later failures are often downstream of the first.
3. Interpret gates: `lint` → run `make fmt` first, hand-fix what remains; `typecheck` → add real types, never `# type: ignore` (PGH003 rejects blanket ignores); `slop` → the flagged pattern is banned, restructure, don't suppress; `test` → fix code or test, never delete the assertion; `deps`/`dead` → remove the unused thing; `arch` → your import violates the layer contract, invert the dependency.
4. Green = done. Report which gates initially failed and what changed.
