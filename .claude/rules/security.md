# Security rules

- Never read or print `.env*` contents; reference variable *names* only.
- No `subprocess` with `shell=True`, no `eval`/`exec` on external input (ruff S rules gate this).
- Secrets come from the environment or a secrets manager at runtime — never hardcoded, never in test fixtures with real values.
- New dependency? Justify it in the PR description. The 7-day `exclude-newer` cooldown is not a substitute for judgment.
- Pin by lockfile (`uv.lock`), never `pip install` ad hoc — pip is deliberately absent from this workflow.
