#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv || true
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

ruff check app
bandit -q -r app -x tests
pip-audit --strict
pytest

echo "Done. Coverage HTML at coverage_html/index.html"
