#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

if [[ ! -f .env ]]; then
  echo ".env is required for the live OpenRouter committee test" >&2
  exit 2
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

export HASHSMASH_JUDGE_PROVIDER="${HASHSMASH_JUDGE_PROVIDER:-openrouter}"
case "${HASHSMASH_JUDGE_PROVIDER}" in
  openrouter)
    : "${OPENROUTER_API_KEY:?OPENROUTER_API_KEY is required in .env}"
    export HASHSMASH_OPENROUTER_ZDR="${HASHSMASH_OPENROUTER_ZDR:-true}"
    default_committee="judge/committees/committee-calibration-v1.json"
    ;;
  bedrock)
    : "${AWS_BEARER_TOKEN_BEDROCK:?AWS_BEARER_TOKEN_BEDROCK is required in .env}"
    default_committee="judge/committees/committee-bedrock-calibration-v1.json"
    ;;
  *)
    echo "HASHSMASH_JUDGE_PROVIDER must be openrouter or bedrock" >&2
    exit 2
    ;;
esac
export HASHSMASH_JUDGE_MODE="committee"
export HASHSMASH_COMMITTEE_PATH="${HASHSMASH_COMMITTEE_PATH:-${default_committee}}"

python3 scripts/hashsmash_pipeline.py all
