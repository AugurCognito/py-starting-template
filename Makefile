.PHONY: setup verify fmt lint typecheck slop test deps dead arch build clean

setup:
	uv sync
	uv run lefthook install

# THE definition of done — cheapest gate first, fail fast.
verify: lint typecheck slop test deps dead arch build

fmt:
	uv run ruff check --fix .
	uv run ruff format .

lint:
	uv run ruff format --check .
	uv run ruff check .

typecheck:
	uv run pyrefly check

slop:
	uv run ast-grep scan --error

test:
	uv run pytest

deps:
	uv run deptry src

dead:
	uv run vulture

arch:
	uv run lint-imports

build:
	uv build

clean:
	rm -rf dist .pytest_cache .coverage .ruff_cache
