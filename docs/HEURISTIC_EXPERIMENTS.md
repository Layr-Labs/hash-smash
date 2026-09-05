# Heuristic evidence experiments

The empirical harness produces reproducible, scoped evidence for the exploratory
and rigorous judges. A successful execution does not automatically qualify a
claim or establish full-scale probability or attack cost. Both judges receive the
same report; their policies determine which unresolved obligations block a score.

## Supported experiments

| Kind | Execution | Independently checked result |
| --- | --- | --- |
| `addition-xor-exact-v1` | Organizer Python, exhaustive enumeration | Exact XOR-differential count for one modular addition at a declared word width |
| `addition-xor-sampled-v1` | Organizer Python, fixed seeded sample | Per-pair predicate, sample frequency and a conservatively qualified interval |
| `python-message-pairs-v1` | Submitted Python inside a bounded Docker container | Selected-target hashes, distinctness, full collisions or a declared output-XOR mask event |

For addition, the event is
`((a+b) mod 2^w) XOR (((a XOR da)+(b XOR db)) mod 2^w) == dc`.
Exact enumeration covers all `2^(2w)` ordered pairs and defaults to `w <= 8`.
This proves only the stated finite count. It does not justify multiplying
dependent local probabilities into a global differential-trail probability.

The sampled evaluator defaults to 256 organizer-generated pairs. Its two-sided
Hoeffding interval has default alpha 0.01. Coverage is explicitly conditional on
independent uniform samples: reproducible SHAKE-derived samples do not prove a
randomness assumption. Fixed seeds, a selected favorable trail, multiple testing,
and changes to the experiment after seeing results can invalidate an advertised
coverage claim. There is no adaptive stopping and no automatic correction for
searching many candidate hypotheses.

Python experiments may emit numeric internal observations, but those observations
are labeled untrusted. The host never credits a submitted success count, claimed
operation count, or runtime as an attack cost. It recomputes the selected output
predicate for every returned pair. A mask-event success is explicitly distinct
from a collision. Repeated pairs are recorded and marked. Arbitrary programs can
ignore seeds or couple trials, so Python reports contain no iid success interval
and no inferred expectation. The judge must assess this remaining proof obligation.

## Candidate format

Declare the manifest through the track's claim schema and place it at
`experiments/manifest.json`. Python sources are single direct regular files named
`experiments/<basename>.py`; nested directories, symlinks, executable file bits,
additional undeclared files, dependencies and shell commands are disallowed by
intake. The executor takes immutable validated byte snapshots, never a candidate
path to execute. Source encoding declarations must be UTF-8 so the executed text
matches the source presented to the judge. Do not include `.env` or credentials.

```json
{
  "schema_version": 1,
  "experiments": [
    {
      "id": "local-addition",
      "kind": "addition-xor-exact-v1",
      "scope": "One four-bit addition; all 256 ordered input pairs.",
      "hypothesis": "The specified local XOR transition has the claimed probability.",
      "word_bits": 4,
      "input_xor_a": 1,
      "input_xor_b": 0,
      "output_xor": 1
    },
    {
      "id": "target-output-event",
      "kind": "python-message-pairs-v1",
      "scope": "Selected target, organizer seeds and bounded generated message pairs.",
      "hypothesis": "The submitted construction produces ordinary collisions.",
      "program": "experiments/probe.py",
      "event": {"kind": "full-collision"}
    }
  ]
}
```

For a partial output event, use
`{"kind":"digest-xor-mask","mask_hex":"...","expected_hex":"..."}`.
Both hex values must have exactly the selected digest width, and expected bits
must be contained in a nonzero mask. The checked event is
`(digest(a) XOR digest(b)) AND mask == expected`, with `a != b`.

The Python program reads one JSON request from stdin:

```json
{
  "schema_version": 1,
  "experiment_id": "target-output-event",
  "target_profile": "organizer-selected-profile",
  "event": {"kind": "full-collision"},
  "max_message_bytes": 4096,
  "trials": [{"trial": 0, "seed": "64-lowercase-hex-characters"}]
}
```

It writes exactly one JSON document, containing every requested trial once in
order. Return two null messages for a failed trial. Omitted failed trials,
participant totals, extra fields, duplicate JSON keys, nonfinite numbers and
oversized output fail the deterministic gate.

```json
{
  "schema_version": 1,
  "trials": [
    {"trial": 0, "message_a_hex": "00", "message_b_hex": "01",
     "observations": {"internal_conditions": 4}}
  ]
}
```

Only Python's standard library is available. Write deterministic code using the
provided per-trial seeds; avoid OS randomness, wall time and ambient state.
The runner fixes `PYTHONHASHSEED`, locale, architecture and image, then repeats
each Python request in a fresh container and requires byte-identical stdout.
It cannot force an arbitrary program to use its supplied seed, and this two-run
check is not proof of reproducibility for every execution.

## Organizer API and commitments

```python
from experiments import ExperimentLimits, run_experiments

report = run_experiments(
    manifest,
    {"experiments/probe.py": validated_source_bytes},
    target_profile=selected_track.profile_id,
    target_config_sha256=selected_track.config_sha256(),
    digest_fn=trusted_selected_target_digest,
    limits=ExperimentLimits(trials=256),
    seed="hashsmash-public-seed-v1",
    holdout_nonce=None,
)
```

Pass exactly the declared program source mapping; declarative manifests require
an empty mapping. Intake is responsible for regular-file and package-mutation
checks before creating these snapshots. `validate_manifest` and `declared_files`
are exposed to intake. The selected-target callback, seeds, image and all limits
are organizer controlled; none comes from the candidate.

Reports contain the normalized manifest, source text as inert/untrusted material,
manifest/source hashes, target configuration fingerprint, seed protocol, trial
budgets, checked outcomes, limitations and a canonical report SHA-256. They omit
wall time, generated container names and other nondeterministic run metadata.
`verify_report_integrity` detects changes; a hash is not an authenticity mechanism.
Never accept a participant-supplied report as a trusted organizer artifact.

`judge_view(report)` verifies that full report and produces a deterministic bounded
view for review. It retains the entire source text, manifest, parameters, seeds,
hypotheses, checked aggregates, trust flags and hashes. Raw message pairs and
participant numeric observations remain in the full artifact; the view contains
at most three trial previews, table hashes and observation counts. Its
`full_report_sha256` binds the raw report and `view_sha256` binds the view. A global
64-KiB source-text budget and 256-KiB view budget fail explicitly; source text is
never silently truncated. These summaries do not substitute for proof or raw
artifact replay. Keep the complete report in the trusted workflow artifact.

For a holdout run, first commit the candidate and selected experiment, then choose
an unpredictable organizer nonce and rerun. Record the prior commitment in the
trusted job's provenance. The nonce is included in the finished report to permit
reproduction. Merely setting `holdout_nonce` does not prove it was chosen after
the submission. Keep exact small cases, sampled evidence, measured target behavior,
extrapolation and heuristic conclusions distinct in the judge's review.

## Sandbox and setup

The default runtime is official Python 3.12.12 slim Bookworm, Linux amd64, pinned
to its platform manifest digest:

```text
python:3.12.12-slim-bookworm@sha256:2986c55feb36e6cae00fa1fefb454283e4b33f35e75ff8bdd123b134130be301
```

The digest was resolved from the official registry on 2026-09-04. The image is
pulled explicitly during organizer setup; execution uses `--pull=never`:

```sh
docker pull --platform=linux/amd64 python:3.12.12-slim-bookworm@sha256:2986c55feb36e6cae00fa1fefb454283e4b33f35e75ff8bdd123b134130be301
```

The container has no network, read-only root and source mount, user 65534, all
capabilities dropped, no new privileges, default Docker seccomp, one CPU, 128 MiB
memory with no swap allowance, 32 processes, 64 descriptors, no core dumps, and a
16 MiB noexec tmpfs. A host watchdog enforces the default 20-second timeout and
2 MiB combined stdout/stderr limit through bounded pipes; Docker log persistence
is disabled. Hard upper bounds on
organizer settings prevent accidental unlimited workloads. The submitted program
cannot select Docker flags. Cleanup targets only the generated container name.
Docker's documented [run isolation](https://docs.docker.com/engine/containers/run/)
and [resource controls](https://docs.docker.com/engine/containers/resource_constraints/)
define these mechanisms.

Only the exact validated program is mounted; no repository, candidate directory,
Docker socket, home directory or `.env` enters the container. The Docker CLI also
runs with a scrubbed environment and empty configuration, with only a local Unix
socket address preserved. No provider key is forwarded. Missing Docker, an absent
pinned image, or unsupported sandbox settings produce `ExperimentSetupError`.
There is no host-execution fallback.

For Yukon/GitHub Actions deployment, run this step in a disposable, secret-free
experiment job. Its trusted artifact goes to a separate credential-bearing judge
job. Containers share the host kernel; this MVP is not a substitute for a dedicated
disposable VM boundary when handling adversarial public submissions. Do not execute
participant programs in the job that holds the Bedrock credential.

## Tests

Offline checks use only organizer fixtures and mocked container output:

```sh
python3 -m unittest tests.test_experiments -v
```

After the deterministic suite passes, opt into real Docker tests. These execute
only organizer fixtures and verify deterministic reruns, no credentials/network,
read-only input, non-root execution, timeouts, excessive output and program errors:

```sh
HASHSMASH_TEST_DOCKER=1 python3 -m unittest tests.test_experiments.DockerIntegrationTests -v
```

No candidate proof, solver draft or provider credential is used by these tests.
