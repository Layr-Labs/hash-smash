# HashSmash deterministic verifier

This package is the credential-free, standard-library verification layer for the
[paired frontier lanes](../docs/FRONTIER_LANES.md). Every command requires an
explicit organizer track ID, such as `sha256-r37-exploratory`. That selection binds
the target, round count, digest width, cost model, nominal reference and lane policy.

The organizer pipeline coordinates intake, experiments, review and scoring:

```sh
python3 scripts/hashsmash_pipeline.py intake --track sha256-r37-exploratory
```

For direct mechanical checks, run from the repository root:

```sh
python3 -m verifier intake \
  --track sha256-r37-exploratory \
  --candidate lanes/exploratory/candidates/sha256-r37 \
  --output-dir artifacts/intake
python3 -m verifier certificates \
  --track sha256-r37-exploratory \
  --candidate lanes/exploratory/candidates/sha256-r37 \
  --output artifacts/certificates.json
```

The package contains `claim.json`, `proof.md`, and declared certificate or
experiment files. Intake rejects unknown fields, symlinks, special files,
undeclared files, oversized files and invalid proof encoding or line endings.
It emits a line-numbered review copy without modifying the submitted proof.
Participant Python source is inspected as inert data; only the organizer's
bounded Docker executor may run declared experiments.

`hash-collision-witness-v2` checks distinct complete messages against the selected
organizer hash implementation. It establishes only the witness collision, not
an attack's method, success probability or complexity. The retained v2 certificate
manifest is used by the paired v3 claims.

Scores require `submission_state: ready`, the selected lane's qualifying review
outcome, and matching package, evidence and configuration bindings. The score
builder applies [hashsmash-scalar-tm-v1](../scoring-policies/README.md):
`timeLog2 + max(0, memoryLog2Bytes - 20)`, using the validated submitted v5 bounds.
An organizer-pinned [reorg](../docs/RESCORING.md) uses previous judgments: it retains
the latest accepted time bound unless computation accounting changes, in which
case it uses the judge's final reviewed time bound. Memory remains the submitted,
reviewed bound. No new intermediate operation ledger is required.
New artifacts retain `metrics.costModelId: collision-frontier-v5`, raw resources
and judgment fingerprints, and separately identify the scalar using
`scoringPolicyId`, `scoringPolicySha256` and `scoreMetric: normalizedTimeMemoryLog2`.
The top-level `score` is authoritative; no duplicate normalized value is emitted.
The direct CLI and pipeline share this builder. Policy JSON and effective helper
sources are explicitly bound in new target fingerprints. Historical migration
retains original fingerprints and artifacts. The trusted Pareto adapter continues
to receive time-only output without scalar-policy markers. Drafts, failed review and
nominal-reference values never emit scores. Follow the
[qualification sequence](../docs/CANDIDATE_QUALIFICATION.md) to generate and review
the complete evidence before scoring.

Claims may omit the legacy `data_log2` field. If present, it must still be a finite
nonnegative number and is preserved as optional `metrics.dataLog2` metadata, but
is not scored or reviewed as a resource bound. If absent, score output omits that
metric rather than synthesizing zero. New draft claims omit it. Exact claim and
configuration bindings still apply, including any supplied legacy metadata.
See the [rollout and UI handoff](../docs/OPTIONAL_DATA_METRIC.md) for retiring the
displayed metric without a Yukon reorg.

Run the organizer tests with:

```sh
bash .yukon/setup.sh
```
