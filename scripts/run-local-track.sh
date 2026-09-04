#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"
if [[ $# -ne 1 || -z "$1" ]]; then
  echo "Usage: bash scripts/run-local-track.sh TRACK" >&2
  exit 2
fi

# Resolve only organizer-known tracks and run deterministic tests BEFORE loading a key.
python3 scripts/local_tracks.py check "$1"
bash .yukon/setup.sh
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi
export HASHSMASH_JUDGE_PROVIDER="${HASHSMASH_JUDGE_PROVIDER:-bedrock}"
export HASHSMASH_JUDGE_MODE="${HASHSMASH_JUDGE_MODE:-single}"
if [[ "${HASHSMASH_JUDGE_PROVIDER}" == bedrock ]]; then
  export HASHSMASH_BEDROCK_MODEL="${HASHSMASH_BEDROCK_MODEL:-us.openai.gpt-5.6-sol}"
  export HASHSMASH_BEDROCK_REGION="${HASHSMASH_BEDROCK_REGION:-us-east-1}"
fi
python3 scripts/hashsmash_pipeline.py all --track "$1"
