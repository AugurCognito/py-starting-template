---
paths:
  - 'tests/**/*.py'
---

# Test rules

- **Mirror the package tree** (Elixir convention): the test for `src/app/foo/bar.py` lives at `tests/foo/test_bar.py` — same relative path, `test_` prefix. Creating a source module without its mirror is incomplete work.
- Every test asserts behavior, not implementation. No mock-only tests that merely verify a mock was called.
- Cover the failure path of whatever you test — error branches are where agent-written code rots. Assert exception *type and message* (`pytest.raises(..., match=...)`), and `__cause__` chaining where `from exc` is used.
- No `assert True` placeholders; a test that can't fail is slop.
- `filterwarnings = ["error"]` is set — a warning in tests is a failure. Fix the cause, never blanket-ignore.
- Keep branch coverage ≥ 80% (enforced in pyproject) — coverage is a floor, not the goal.
