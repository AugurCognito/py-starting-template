#!/usr/bin/env bash
f=$(jq -r '.tool_input.file_path // empty')
case "$f" in *.py) ;; *) exit 0 ;; esac
[ -f "$f" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
uv run ruff check --fix "$f" >/dev/null 2>&1
uv run ruff format "$f" >/dev/null 2>&1
if ! remaining=$(uv run ruff check --output-format concise "$f" 2>&1); then
  {
    echo "ruff diagnostics remain after auto-fix in $f:"
    printf '%s\n' "$remaining" | head -14
  } >&2
  exit 2
fi
exit 0
