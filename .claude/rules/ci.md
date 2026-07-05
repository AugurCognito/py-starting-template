---
paths:
  - '.github/**'
---

# CI rules

- **Pin every action by full commit SHA** (`uses: owner/repo@<40-char-sha> # vX.Y.Z`) — tags are mutable and have been hijacked.
- **Least-privilege permissions**: top-level `permissions: contents: read`; a job needing more declares it at job level, never workflow-wide.
- **`persist-credentials: false` on every checkout** — the default leaves a write token on disk for later steps.
- **`timeout-minutes` on every job** — a hung job burns the runner budget silently.
- Never `pull_request_target` with checkout of the PR head; never pass secrets to workflows triggered by forks.
