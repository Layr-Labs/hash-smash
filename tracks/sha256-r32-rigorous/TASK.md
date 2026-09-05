# sha256-r32-rigorous

From the repository root, select `yukon switch sha256-r32-rigorous` and verify
`yukon trace status` before editing. The same full track ID is used by Yukon and
organizer commands.

Edit only `lanes/rigorous/candidates/sha256-r32/`. The target is `sha256-r32-prefix-v1`; the lane is
`rigorous`. Use `python3 scripts/local_tracks.py show sha256-r32-rigorous` for its fixed
profile, cost model and reference. The nominal reference is 128, not an established
attack or qualified baseline. MD5/SHA-1 full and preceding rounds are reproduction
controls; they do not have an unbroken standard-round boundary.

Provide claim.json, proof.md and declared certificates. Heuristic-dependent claims
must disclose their premises and evidence. Optional `experiments/manifest.json`
selects organizer exact/sampled checks or isolated Python message-pair experiments.
Read JUDGE_LANES.md and HEURISTIC_EXPERIMENTS.md for evidence requirements.

Run `bash scripts/run-local-track.sh sha256-r32-rigorous` only after replacing the draft with a
complete evaluable submission. That wrapper runs tests before a live judge call.
The rigorous pass label is `ai_rigor_qualified`.
A passing AI review is not a mathematical proof or human acceptance. Findings from
both review policies are recorded, while only this selected lane emits a score.
