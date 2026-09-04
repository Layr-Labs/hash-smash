#!/usr/bin/env bash
set -euo pipefail
set +x

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

# Always pass the deterministic suite before loading provider credentials.
bash .yukon/setup.sh
if [[ -f .env ]]; then
  set -a
  # Organizer-owned local configuration only; never log or copy its contents.
  # shellcheck disable=SC1091
  source .env
  set +a
fi
python3 scripts/calibrate_paired_judges.py "$@"
