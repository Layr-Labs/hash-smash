#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

python3 -m unittest discover -s verifier/tests -p 'test_*.py'
python3 -m unittest discover -s judge/tests -p 'test_*.py'
python3 -m unittest discover -s tests -p 'test_*.py'

echo "HashSmash paired-lane setup and tests passed"

