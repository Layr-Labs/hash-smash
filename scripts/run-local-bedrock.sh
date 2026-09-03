#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

if [[ ! -f .env ]]; then
  echo ".env is required for the live Amazon Bedrock integration test" >&2
  exit 2
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

: "${AWS_BEARER_TOKEN_BEDROCK:?AWS_BEARER_TOKEN_BEDROCK is required in .env}"
export HASHSMASH_JUDGE_PROVIDER="bedrock"
export HASHSMASH_JUDGE_MODE="single"

python3 scripts/hashsmash_pipeline.py all
