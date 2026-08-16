#!/usr/bin/env bash
# Run every quality gate for the tauren course.
# Stops at the first failing gate. Run from the project root:
#   ./verify.sh
set -euo pipefail

cd "$(dirname "$0")"

echo "==> pytest"
uv run pytest

echo "==> ruff check"
uv run ruff check .

echo "==> ruff format"
uv run ruff format --check .

echo "==> mypy"
uv run mypy

echo "==> ty check"
uv run ty check

echo
echo "All quality gates passed."