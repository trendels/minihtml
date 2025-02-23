# Generate, format, typecheck and test code
all: codegen format typecheck test doctest

# Runn all checks (for CI)
check: check-codegen check-format typecheck

# Run code generation
codegen:
    uv run cog --check @codegen.txt || uv run cog -r @codegen.txt

# Check that generated code is up to date
check-codegen:
    uv run cog --check @codegen.txt

# Lint and format all code
format:
    uv run ruff check --fix
    uv run ruff format

# Check that code is linted and formatted
check-format:
    uv run ruff check
    uv run ruff format --check

# Run typechecker
typecheck:
    uv run pyright

# Run tests and measure code coverage
test:
    uv run coverage run -m pytest
    uv run coverage report
    uv run coverage html

# Run doctests
doctest:
    uv run python -m doctest -o ELLIPSIS README.md

# Run tests when code changes (requires "watchexec")
watch:
    watchexec -w src -w tests -e py -c -- 'uv run pytest --exitfirst --failed-first'
