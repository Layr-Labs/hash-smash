#!/usr/bin/env bash
set -euo pipefail

case "${GITHUB_REF:-}" in
  refs/heads/submissions/*) ;;
  *) exit 0 ;;
esac

git_safe=(git -c core.hooksPath=/dev/null -c core.fsmonitor=false -c core.pager=cat)
read -r -a commit_line <<< "$("${git_safe[@]}" rev-list --parents -n 1 "${GITHUB_SHA:?GITHUB_SHA is required}")"
if (( ${#commit_line[@]} != 2 )); then
  echo "Submission must be a single-parent commit" >&2
  exit 1
fi

while IFS= read -r -d '' changed_path; do
  case "${changed_path}" in
    candidate|candidate/*) ;;
    *)
      echo "Submission changed a non-editable path: ${changed_path}" >&2
      exit 1
      ;;
  esac
done < <("${git_safe[@]}" diff --no-ext-diff --no-renames --name-only -z "${GITHUB_SHA}^" "${GITHUB_SHA}")

