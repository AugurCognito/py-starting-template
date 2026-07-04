---
name: verify-loop
description: Run make verify, fix what it finds, repeat until green. Use before claiming any task is done, after multi-file edits, or when CI failed.
---

# Verify loop

1. Run `make verify`.
2. On failure, fix the **first** failing gate only, then re-run — gates are ordered cheapest-first, and later failures are often downstream of the first.
3. Interpret gates: `lint` → run `make fmt` first, hand-fix what remains; `typecheck` → add real types, never `# type: ignore` (PGH003 rejects blanket ignores); `slop` → the flagged pattern is banned, restructure, don't suppress; `test` → fix code or test, never delete the assertion; `deps`/`dead` → remove the unused thing; `arch` → your import violates the layer contract, invert the dependency.
4. Never weaken a gate to pass it (config edits to thresholds/rules need explicit human sign-off).
5. Green = done. Report which gates initially failed and what changed.
