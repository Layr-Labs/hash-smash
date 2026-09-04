# md5-s64

Full MD5, historically collision-broken; reproducing an unconditional, fully costed construction is still substantive.

- Target: `target-profiles/md5-s64-prefix-v1.json`; 64 compression steps of 64, 128-bit output.
- Editable submission: `candidates/md5-s64/` only.
- Common model: `cost-models/collision-local-v2.json`.
- Scalar: `log2(time) + log2(peak memory bytes)`, lower is better within this track.
- Initial reference: `md5-s64-nominal-v1`, scalar 128. It is not a proved or qualified baseline and is not evidence for any target property.
- Qualification: `unconditional-v1`; no unproved target-randomness, independence, or differential-probability premises.

Read LOCAL_TRACKS.md for the full workflow and experiment rules. Drafts are never sent
to the provider. A concrete witness does not establish an algorithm's cost or novelty;
count construction, preprocessing, advice, verification, randomness, and working storage.
Document prior-art reproduction separately from new cryptanalytic progress.

```sh
python3 scripts/local_tracks.py show md5-s64
python3 scripts/hashsmash_pipeline.py intake --track md5-s64
bash scripts/run-local-track.sh md5-s64
```

Do not launch agents, schedule work, read .env, change trusted files, push, or call a live
judge unless that action is included in your assigned run's authority and budget.
