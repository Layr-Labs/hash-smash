# sha1-r40

Reduced SHA-1 with expanded schedule and two function phases; a substantial cryptanalytic challenge.

- Target: `target-profiles/sha1-r40-prefix-v1.json`; 40 rounds of 80, 160-bit output.
- Editable submission: `candidates/sha1-r40/` only.
- Common model: `cost-models/collision-local-v2.json`.
- Scalar: `log2(time) + log2(peak memory bytes)`, lower is better within this track.
- Initial reference: `sha1-r40-nominal-v1`, scalar 160. It is not a proved or qualified baseline and is not evidence for any target property.
- Qualification: `unconditional-v1`; no unproved target-randomness, independence, or differential-probability premises.

Read LOCAL_TRACKS.md for the full workflow and experiment rules. Drafts are never sent
to the provider. A concrete witness does not establish an algorithm's cost or novelty;
count construction, preprocessing, advice, verification, randomness, and working storage.
Document prior-art reproduction separately from new cryptanalytic progress.

```sh
python3 scripts/local_tracks.py show sha1-r40
python3 scripts/hashsmash_pipeline.py intake --track sha1-r40
bash scripts/run-local-track.sh sha1-r40
```

Do not launch agents, schedule work, read .env, change trusted files, push, or call a live
judge unless that action is included in your assigned run's authority and budget.
