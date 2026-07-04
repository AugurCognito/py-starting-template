---
updated: 2026-07-04
git_commit: 4c04a87
branch: main
---

# HANDOFF

> Session memory. The `/handoff` skill maintains this file. It describes NOW, not history — overwrite stale sections. Reference code as `file:line`, never pasted blocks.

_No task in flight (2026-07-04). This file is overwritten by `/handoff` when a session ends mid-task._

## Known landmines

- **pyrefly does not follow strict semver** — a minor upgrade may introduce new type errors. That's the tool getting better; fix the code, don't pin forever.
- **`exclude-newer = "7 days"`** means a dependency released yesterday is invisible to the resolver. If `uv add` picks an unexpectedly old version, that's the cooldown working — not a bug to work around.
- **lefthook is installed via uv** (PyPI wrapper around the Go binary). If hooks silently don't fire after a fresh clone, run `make setup`.
