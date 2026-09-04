#!/usr/bin/env bash
set -euo pipefail
set +x

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null && pwd -P)"
cd "${repo_root}"

for option in "$@"; do
  case "$option" in
    --run-directory|--run-directory=*)
      echo "This wrapper always creates a fresh diagnostic run directory." >&2
      exit 2
      ;;
  esac
done

# The preparation subprocess must not inherit provider/cloud credentials, even
# if the caller has already exported them. The participant still runs only in
# the existing Docker sandbox, with its separately scrubbed environment.
clean_environment=(env
  -u OPENROUTER_API_KEY -u AWS_BEARER_TOKEN_BEDROCK
  -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN
  -u AWS_SECURITY_TOKEN -u AWS_PROFILE -u AWS_DEFAULT_PROFILE
  -u AWS_WEB_IDENTITY_TOKEN_FILE -u AWS_CONTAINER_CREDENTIALS_RELATIVE_URI
  -u AWS_CONTAINER_CREDENTIALS_FULL_URI -u AWS_CONTAINER_AUTHORIZATION_TOKEN
  -u AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE -u GITHUB_TOKEN -u GH_TOKEN
  -u HASHSMASH_EXPERIMENT_HOLDOUT_NONCE)

"${clean_environment[@]}" bash .yukon/setup.sh
run_id="$("${clean_environment[@]}" python3 -c 'from datetime import datetime, timezone; import uuid; print(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12])')"
run_directory="${repo_root}/.yukon/reports/participant-heuristic/${run_id}"
"${clean_environment[@]}" python3 scripts/test_participant_heuristic.py prepare --run-directory "${run_directory}"

# Preparation has completed and its process has exited. Only this subsequent
# review process may receive credentials. It never executes participant source.
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi
python3 scripts/test_participant_heuristic.py review --run-directory "${run_directory}" "$@"
