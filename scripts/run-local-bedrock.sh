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

# Explicit command-line settings take precedence over values loaded from .env.
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model|--region)
      if [[ $# -lt 2 || -z "$2" ]]; then
        echo "$1 requires a value" >&2
        exit 2
      fi
      if [[ "$1" == "--model" ]]; then
        export HASHSMASH_BEDROCK_MODEL="$2"
      else
        export HASHSMASH_BEDROCK_REGION="$2"
      fi
      shift 2
      ;;
    *) echo "Usage: run-local-bedrock.sh [--model MODEL] [--region REGION]" >&2; exit 2 ;;
  esac
done

python3 scripts/hashsmash_pipeline.py all
