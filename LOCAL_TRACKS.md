# Local multi-track experiment

Nine local tracks are ready for solver experiments. The score remains
`log2(total time) + log2(peak memory bytes)`, lower is better **within one track**.
The unconditional policy is unchanged. No agents or recurring overnight jobs have been
started, and no provider calls or qualified baseline searches are required for setup.

## Roster

| Function | Easy protocol control | Exploratory middle | Hard endpoint | Nominal reference score |
| --- | --- | --- | --- | --- |
| MD5 | `md5-s8` | `md5-s24` | `md5-s64` | 128 |
| SHA-1 | `sha1-r8` | `sha1-r40` | `sha1-r80` | 160 |
| SHA-256 | `sha256-r8` | `sha256-r24` | `sha256-r64` | 256 |

MD5 counts **steps**: its full 64-step compression is conventionally organized as four
groups of 16. SHA round counts have their standard meaning. These are qualitative
experiment buckets, not measured difficulty estimates. The three 8-step/round controls
intentionally leave message words unused; simple constructions should be accessible.
Those are protocol/calibration successes, not novel breaks of the full hash. The middle
tracks consume all input words and add mixing/schedule complexity. Full MD5 and SHA-1
have known collision attacks; reproducing a rigorous, completely costed construction
still tests this protocol. Full SHA-256 is a stretch target, not an expected overnight win.

Specifications: [MD5, RFC 1321](https://www.rfc-editor.org/rfc/rfc1321.html),
[MD5 security update, RFC 6151](https://www.rfc-editor.org/rfc/rfc6151.html), and
[SHA-1/SHA-256, FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).
Difficulty selection beyond the deliberate controls is an organizer judgment.

## Exact common target semantics

Each trusted `target-profiles/<track>-prefix-v1.json` specifies an ordinary collision
of the **complete message hash**, with distinct byte strings of bit length below `2^64`.
Use standard padding, fixed standard IV, full standard digest width and serialization,
and feed-forward after each block. Execute compression indices `0..r-1` on **every padded
block**, with original constants, schedule and phase boundaries. This is not a suffix
round range, free-start/compression-only problem, or output-truncation problem.

The organizer-owned `verifier/hash_functions.py` defines executable checker semantics.
Full variants are compared with independent `hashlib` implementations at padding and
multi-block boundaries. Reduced SHA variants are checked against NIST's published
[SHA-1 intermediate states](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA1.pdf)
and [SHA-256 intermediate states](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA256.pdf),
adding the profile's required feed-forward. Reduced MD5 is also tested with the RFC's
direct A,D,C,B register-update ordering. These are reference tests, not formal verification.

The new shared `collision-local-v2` model uses a 256-bit word RAM, with one unit for a
selected-target block compression and one unit per other primitive operation. Random
256-bit words are independent algorithmic coins and are explicitly charged. Total time
includes preprocessing, construction and verification; memory includes code, advice,
state, messages and tables. See the JSON model for precise accounting. This does not
silently alter the old pilot's different 128-bit model or reuse its scores.

## Nominal starting references, without establishing baselines

For an n-bit digest, the reference uses the idealized birthday-work exponent `n/2`
and nominal memory exponent `n/2`, giving scalar **n**, not `n/2`. The latter is a
collision-work exponent, not a time-memory-product exponent.

These deliberately coarse values ignore storage/implementation constants and actual
cryptanalysis. They are not claims about MD5/SHA-1 security, proofs that a birthday
implementation attains those exact costs, lower bounds, or admissible randomness
assumptions. References are tagged `nominal-reference-only` / `is_qualified_baseline: false`.
They never generate score artifacts and do not require judge approval. There is initially
**no accepted or AI-qualified baseline**. Every submission must establish its own claim.

An AI-qualified result may be recorded even if it does not beat the nominal reference;
`improvesNominalReference` reports that comparison separately. We retain all reviewed
runs, and `status` reports the best AI-reviewed scalar under the current target/model/
checker/policy fingerprint. No automatic human acceptance, branch promotion or cross-track
ranking occurs. Beating a nominal reference is not evidence of novelty.

## Local commands

```sh
bash .yukon/setup.sh
python3 scripts/local_tracks.py list
python3 scripts/local_tracks.py show sha256-r24
python3 scripts/local_tracks.py check
python3 scripts/local_tracks.py status
```

Those commands need no credentials and make no model calls. `check` validates packages
and any declared witnesses, including draft templates; it does not establish proofs.

Each `candidates/<track>/` starts with a draft claim, proof scaffold and empty certificate
manifest. Replace the draft argument and cost placeholders, then explicitly change
`submission_state` from `draft` to `ready`. A draft cannot reach the judge or produce a
score, even with a purported positive verdict. The new claim and certificate contracts
are `schemas/claim-local-v2.schema.json` and `schemas/certificate-manifest-local-v2.schema.json`.
The organizer-selected track additionally binds exact profile, round count and units.

For one completed submission:

```sh
python3 scripts/hashsmash_pipeline.py intake --track sha256-r24
bash scripts/run-local-track.sh sha256-r24
```

The wrapper runs the deterministic tests first, then loads the existing local `.env`
without printing it. It defaults to Bedrock Sol in `us-east-1`; explicit provider/model
configuration in the environment or `.env` is preserved. It does not change accounts,
credentials or GitHub settings. Committee mode uses the existing provider backend:

```sh
HASHSMASH_JUDGE_PROVIDER=bedrock HASHSMASH_JUDGE_MODE=committee \
  HASHSMASH_COMMITTEE_PATH=judge/committees/committee-bedrock-calibration-v1.json \
  bash scripts/run-local-track.sh sha256-r24
```

Values set in `.env` take precedence over inherited shell values in this wrapper; check
your configuration before a paid run. The single/committee policy, effective prompt
hashes, model, request IDs, attempts, latency and token usage are retained in the dossier.
The draft templates are not positive-control proofs; there has been no new live judge
qualification of these tracks during setup.

## Isolation and diagnostics

- Editable input: `candidates/<track>/` only. Treat every candidate as hostile data.
- Work: `.yukon/work/tracks/<track>/`.
- Latest reports: `.yukon/reports/tracks/<track>/`.
- AI-qualified score only: `.yukon/scores/<track>.json`.
- CLI run history: `.yukon/reports/tracks/<track>/runs/<timestamp-id>/`.

The CLI locks one track at a time, non-blockingly; different tracks can run concurrently.
Calling the Python library functions directly requires equivalent caller coordination.
Only the selected track's enumerated stale outputs are cleared. Each CLI invocation
archives its known generated artifacts and exit code; it never copies `.env` or walks
the participant directory. Intake failures are retained as unsuccessful run records.
The score binds the exact candidate package and the target/model/checker/policy fingerprint.
Changing proof text, profile or costs invalidates stale results. Historical reports
remain available, and `status` distinguishes a prior candidate from the current input.

Exit 0 means that command completed successfully, not that a human accepted a theorem.
Exit 2 is a draft, deterministic rejection or substantive review nonqualification;
exit 3 indicates provider/configuration/lock/infrastructure failure. Read the dossier and
run command to distinguish those cases. Template intake uses status `draft_not_submitted`.

The legacy `candidate/`, `.yukon/score.json`, `benchmark.json` and GitHub workflow remain
the original single SHA-1 pilot. Omission of `--track` deliberately retains that behavior.
These local tracks are shaped for Yukon's v2 disjoint-directory mapping, but are **not
imported into Yukon**. Nominal references do not bypass Yukon's qualifying-baseline import
requirement. A remote migration needs suitable baseline handling and per-track workflow
wrappers; it is not part of this local experiment setup.

## Preparing the overnight experiment

Six self-contained launch prompts are provided in [OVERNIGHT_PROMPTS.md](./OVERNIGHT_PROMPTS.md).
They cover one easy control, three exploratory tracks, full-MD5 reproduction and a
full-SHA-256 stretch target, with explicit research and judge-call limits.

Use the per-track briefs at `tracks/<track>/TASK.md`. Start with the three easy controls,
then the middle tracks, and allocate at least one hard endpoint as a no-progress control.
Before launching, assign each worker a time/token budget, an explicit live-judge-call
budget, and one track. Keep solver and judge roles separate. A worker may not rewrite the
verifier, profiles, policy or prompts to secure acceptance. Do not expose credentials to
solver prompts, submit them as artifacts, or execute participant-provided code.

Record independently: witness found, self-contained argument, AI review outcome,
scalar improvement over nominal, reproduction of known work versus novel claim, human
review status, resource usage, and protocol/infrastructure issue. Do not conflate a
constant stored collision with a cheaply constructed one. A single false positive on an
easy control is a protocol problem, not a research success. For concurrent workers,
separate workspace snapshots are preferable; do not start from an old commit that omits
this currently local setup. No workers, schedules, commits, pushes, or deployments were
created by this setup.

The judge's versioned selected-target/reference instructions follow
[official OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-engineering):
application rules stay separate from participant evidence and changes receive regression
tests. No model or provider migration was performed.
