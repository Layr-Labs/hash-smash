# sha1-r80-exploratory

Edit only `lanes/exploratory/candidates/sha1-r80/`. The target is `sha1-r80-prefix-v1`; the lane is
`exploratory`. Use `python3 scripts/local_tracks.py show sha1-r80-exploratory` for its fixed
profile, cost model and reference. The nominal reference is 80, not an established
attack or qualified baseline. MD5/SHA-1 full and preceding rounds are reproduction
controls; they do not have an unbroken standard-round boundary.

Provide claim.json, proof.md and declared certificates. Heuristic-dependent claims
must disclose their premises and evidence. Optional `experiments/manifest.json`
selects organizer exact/sampled checks or isolated Python message-pair experiments.
Read JUDGE_LANES.md and HEURISTIC_EXPERIMENTS.md for evidence requirements.

Run `bash scripts/run-local-track.sh sha1-r80-exploratory` only after replacing the draft with a
complete evaluable submission. That wrapper runs tests before a live judge call.
The exploratory pass label is `plausible_not_refuted`.
A passing AI review is not a mathematical proof or human acceptance. Findings from
both review policies are recorded, while only this selected lane emits a score.
