#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

if [[ ! -f .env ]]; then
  echo ".env is required for the Amazon Bedrock smoke test" >&2
  exit 2
fi

bash .yukon/setup.sh

set -a
# shellcheck disable=SC1091
source .env
set +a

: "${AWS_BEARER_TOKEN_BEDROCK:?AWS_BEARER_TOKEN_BEDROCK is required in .env}"
python3 scripts/smoke-bedrock.py "$@"
