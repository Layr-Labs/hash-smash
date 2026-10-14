# Scalar scoring policy definitions

The approved original-challenge policy is
[hashsmash-scalar-tm-v1](./hashsmash-scalar-tm-v1.json):

```text
score = timeLog2 + max(0, memoryLog2Bytes - 20)
```

Memory uses **1 MiB = 1,048,576 bytes**, with a minimum of one memory unit.
Computation uses existing reviewed v5 target-compression equivalents. Both
resources have equal multiplicative weight; lower scores are better. The
immutable definition hash is
`65f6bd3eb8260395d5a9520ebe14be10f68efba6bf4625d9cebef2221b832c2d`.
The active loader checks this ID/hash and fails closed if the definition changes.
This source describes future evaluations; deploying it and migrating published
scores require the separate authorized operator rollout.

The [schema](./scalar-time-memory-v1.schema.json) requires every parameter:

| Field | Meaning |
| --- | --- |
| `id` | Immutable public policy identifier |
| `version` | Definition format version, currently `1` |
| `formula` | `timeLog2 + log2(memoryUnits)` |
| `sourceCostModelId` | `collision-frontier-v5` |
| `timeUnit` | `target-compressions` |
| `memoryUnitBytes` | Positive integer bytes per normalized memory unit |
| `minimumMemoryUnits` | `1` floors memory at one normalized unit; `null` permits fractional units |

`memoryUnits` is the existing memory-byte bound divided by `memoryUnitBytes`,
with the stated floor applied. Equal multiplicative time-memory weighting is
fixed by this formula. The helper calculates entirely in the log domain:

```text
normalizedMemoryLog2 = memoryLog2Bytes - log2(memoryUnitBytes)
if minimumMemoryUnits is 1:
    normalizedMemoryLog2 = max(0, normalizedMemoryLog2)
score = timeLog2 + normalizedMemoryLog2
```

The generic offline helper requires an explicit definition, with no implicit
rounding or parameters. Its schema supports prior or artificial definitions with
fractional units, which can produce a negative finite scalar. The approved policy
uses the floor above. Resource exponents remain finite and nonnegative; nonfinite
results are rejected. The [organizer fixture](../tests/fixtures/scalar-scoring/policy.json)
uses an artificial 1 KiB unit and is not a public scoring rule.

The pure [helper](../scripts/scalar_scoring_policy.py) accepts the full explicit
definition and existing official resource metrics. It rejects incompatible
resource models or units and never fills missing memory, reparses candidates,
changes reviewed bounds or consults judge reconstructions. The caller must
independently verify the official source and its provenance; numeric validation
alone does not authenticate a result.

The definition hash is SHA-256 of `verifier.io.canonical_json_bytes(definition)`:
ASCII JSON with sorted keys, compact separators, integer parameter spelling and
**one trailing LF**. All permitted string values are ASCII. Public consumers
must recognize the exact policy ID and hash together. Unknown or incomplete
markers must not be interpreted as historical time-only scores.

The scoring projection uses three flat fields inside score `metrics`:

```json
{
  "scoringPolicyId": "hashsmash-scalar-tm-v1",
  "scoringPolicySha256": "65f6bd3eb8260395d5a9520ebe14be10f68efba6bf4625d9cebef2221b832c2d",
  "scoreMetric": "normalizedTimeMemoryLog2"
}
```

The top-level `score` remains
the authoritative scalar; no duplicate normalized scalar is added to metrics.
The projection is separate from `costModelId`, `timeUnit`, `timeLog2`,
`memoryLog2Bytes`, package/target/judge/dossier fingerprints, and qualification.
Historical migration retains these original fields and artifacts and records
its previous scoring projection separately in the operator's audit. It does
not imply that a new judge reviewed the result.

The direct CLI and pipeline share `verifier.score.build_score`. Future target
configuration fingerprints explicitly bind the approved policy JSON and both
`scripts/scalar_scoring_policy.py` and `scripts/scalar_score_resources.py`, in
addition to the existing checker and review sources. Historical rows retain their
original evidence fingerprints during migration. Judge `normalized_score_log2`
and nominal security/reference fields retain their computation meanings; the
nominal reference does not include a memory bound or combined-score baseline.
For a trusted Pareto adapter, this root scorer returns the reviewed time bound
without scalar-policy markers, including Orchard. The separately maintained
production Pareto harness declares its own normalized objectives and projects raw
metrics independently; its objectives are outside this scalar maintenance.

The original v5 cost-model file and resource accounting stay unchanged.

[Golden vectors](../tests/fixtures/scalar-scoring/approved-policy-vectors.json)
cover the floor boundary, fractional exponents and high memory. They are artificial
arithmetic fixtures, not qualified attacks or historical artifacts.

## One-time offline Yukon plan filling

Migration uses a separately reviewed local operator and offline Python filler,
retained outside the application and this repository. Obtain their private
`LOCAL_SCALAR_MAINTENANCE.md` runbook, pinned source and checksum receipt before
use. The one-time tools may be retired after verified migration; the normal
scorer, resource/policy helpers, policy definition, UI decoding, review guards and
audit data remain in use.

The operator accepts only this exact approved policy and the original HashSmash
challenges:

- Production: `24e42a9c-0c09-4876-93c9-f59a1038c0e9`.
- Development: `f7921907-1e83-4b42-93b4-4d4a4dc2607c` (preview/dry-run only; apply is rejected).

Its six-field policy reference is `{id,sourceRef,definitionSha256,scoreMetric,sourceCostModelId,timeUnit}`.
The operator independently verifies finite nonnegative resource exponents and
exact agreement with the approved formula. A frozen preview binds all identities,
source fields, metrics and descriptions. The offline filler changes only null
`newScore` proposals, preserves opaque hashes and uses no database. Any description
proposal is separately reviewed. Follow the local runbook for strict schema,
exclusive mode0600 outputs, snapshot and exact approval-hash checks.

`metricsSha256` binds original PostgreSQL metrics-column text, not the readable
JSON projection; never reconstruct it from parsed metrics. Locked dry-run/apply
must preserve the incumbent as the best baseline/eligible-published score, with
ties allowed. A mismatch or stale plan aborts without choosing a new winner.
Original evidence, reviewed bounds, decisions, publication history and exact
unrelated database values remain intact.

The tools run locally, but live apply must wait for permanent UI support for
normalized scores and stale-review guards to be released. Verify the approved
scalar harness on the registered branch within a paused/drained maintenance
window, holding source, configuration and reviews stable. Policy `sourceRef` is
provenance, not an execution pin; neither tool activates the source branch. Use
only the separately authorized production plan; development remains read-only.
