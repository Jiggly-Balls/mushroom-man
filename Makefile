all: ruff

ruff:
	uv run --group dev  ruff format
	uv run --group dev ruff check --fix

check:
	uv run --group dev  basedpyright .
