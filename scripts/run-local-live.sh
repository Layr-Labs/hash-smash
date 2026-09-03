#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

if [[ ! -f .env ]]; then
  echo ".env is required for the live OpenRouter integration test" >&2
  exit 2
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

: "${OPENROUTER_API_KEY:?OPENROUTER_API_KEY is required in .env}"
export HASHSMASH_OPENROUTER_ZDR="${HASHSMASH_OPENROUTER_ZDR:-true}"

python3 scripts/hashsmash_pipeline.py all

