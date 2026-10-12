# Paired-lane validation record

## Poseidon target definition: 2026-10-12

Offline checks against base `c2a8d4c7d7716ca9855375a585e50c09ec55a538`:

- `bash .yukon/setup.sh`: **348 tests discovered, 343 passed, five opt-in Docker
  tests skipped** (23 verifier, 84 judge, 241 general). The same base without
  this change discovers 311 and passes 306, so the 37 added tests are the whole
  difference. No live provider or participant code executed.
- `python3 scripts/validate_frontier_config.py`: eight manifest registrations,
  28 runnable local lanes (four historical), 24 current planned slots and zero
  pending slots. `--require-complete` now passes, because every slot has a
  definition. That reports definitions only, never a boundary or a baseline.
- All 22 official Orchard vectors reproduce against the deployed instance:
  **11/11 permutation vectors and 11/11 hash vectors**, pinned from
  `halo2_poseidon` 0.2.0 at tag `halo2_poseidon-0.2.0` with provenance recorded
  in [the fixture notes](../tests/fixtures/orchard-poseidon-vectors.md). All 192
  round constants and the 3x3 MDS matrix equal that pinned source, and every
  value is a canonical field element.
- Negative controls fail as they must: a changed round constant, a changed MDS
  entry, a wrong capacity element, a wrong round count and an all-full-round
  schedule each break the official vectors, measured against a passing baseline
  in the same test class.
- Rounds 1 and 2 have no official vector upstream, so every prefix from 1 to 64
  is checked against a reference written independently from the round
  definition, and the three digests for rounds 1, 2 and 64 are mutually
  distinct.
- Canonical encoding is enforced. An element encoded as `x + p`, an element
  equal to `p`, and any length other than 64 bytes are rejected by the hash and
  reported by certificate verification as a message outside the target domain.
  Without that gate `x` and `x + p` would be a trivial collision. Domain
  failures raise a dedicated error, so a configuration fault such as an
  unsupported round count is never relabeled as a rejected witness.
- Instrumented reference prices are **C = 27 and C = 54**, counting one modular
  addition and one modular multiplication as one primitive operation each: 18
  multiplications and 9 additions for one round, 36 and 18 for two. The same
  counter reports 816 multiplications (240 in S-boxes, 576 in the MDS) and 576
  additions at the deployed 64 rounds. The shared `collision-frontier-v5` policy
  text is unchanged, so this counting rule remains a proposal.
- The nominal reference is 127 for both targets, not 128, because the output
  space is the Pallas field order of about 2^254 rather than the 32-byte digest
  encoding. The draft claim template now reads that exponent from the registry.
- Both draft packages pass `local_tracks.py check` mechanically as drafts, with
  zero certificates and `qualified: false`.
- All 128 existing candidate files, 15 existing target profiles and the reorg
  history are byte-identical to base, and `benchmark.json` is unchanged.
- [Fingerprint comparison](./validation/poseidon-orchard-fingerprints.json)
  records every existing lane before and after: **26/26 hashes change** from the
  shared registry, schema, cost-table and checker inputs. Each change is confined
  to `cost_model`, `qualification_policy` and `reference_checker_sha256`, and
  every existing lane's selected operation weights are unchanged.
  `yukon-unsafe` and a guarded refresh are required; old evidence remains
  historical and cannot satisfy new configuration gates.

These checks define the target. They do not qualify a cryptanalytic baseline,
register a track, or establish any live Yukon state. Both Poseidon packages
remain unqualified drafts, the root manifest still holds eight registrations,
and the round pair is explicitly provisional.

## SHA-256 round migration: 2026-10-07

Offline checks against production base `453b888ec54f554e63250dd2c26d638c254c2358`:

- `bash .yukon/setup.sh`: **311 tests discovered, 306 passed, five opt-in Docker tests skipped**
  (23 verifier, 84 judge, 204 general). No live provider or participant code executed.
- `python3 scripts/validate_frontier_config.py`: eight manifest registrations,
  26 runnable local lanes (four historical), 26 current planned slots and four
  pending Poseidon slots. `--require-complete` must still reject deferred definitions.
- Both new draft packages pass `local_tracks.py check` mechanically, with zero
  certificates and `qualified: false`. Organizer-fixture tests confirm drafts
  stop before provider/score and block import readiness before credential access.
- Eleven new migration regressions cover exact new/retained identities,
  malformed/duplicate history and lane subsets, no rigorous r37/r38 slots,
  instrumented costs 2644/2728, complete padded-message SHA-256 against an independent
  FIPS-derived oracle (validated at 64 rounds against `hashlib`), multi-block
  chaining, wrong-target/lane rejection and unchanged transitive fingerprint gates.
  The existing all-track fake-provider test now covers all 26 lanes and exact
  score artifact paths for all eight manifest entries.
- All 123 existing candidate files, 13 existing profiles and four reorg/history
  files are byte-identical to base. Original six manifest entries are unchanged.
  No r31/r32 claim, witness or score was repurposed for the new targets.
- [Fingerprint comparison](./validation/sha256-r37-r38-fingerprints.json) records
  every existing lane before/after: **24/24 hashes change** from shared registry,
  schema and cost-table inputs. Old selected weights and hash cores are unchanged.
  `yukon-unsafe` and guarded all-eight refresh are required; old evidence remains
  historical and cannot satisfy new configuration gates.

These checks do not qualify a cryptanalytic baseline or establish live closure,
registration, reorg, UI release or admission restoration. New packages remain
unqualified drafts. Follow the [rollout handoff](./SHA256_ROUND_MIGRATION.md),
retaining r31/r32 as closed public registrations rather than archiving them.

## Historical validation record

The dated checks below describe the earlier two-leaf layout and then-current
suite. That import plan has been superseded by the root manifest. Keep this
historical evidence distinct from the current checks above.

Date: 2026-09-04. Local validation only; no new Yukon dev deployment or
challenge import has been exercised. This record describes the initial paired-lane
implementation before the legacy cleanup; its test counts are historical. Run
`bash .yukon/setup.sh` for the current deterministic suite.

## Deterministic and isolated checks

At the recorded revision, `bash .yukon/setup.sh` discovered 212 tests: 208
credential-free tests passed and
four explicit Docker integration tests were skipped by default. The test suites
use organizer fixtures, never mutable solver drafts. They cover:

- All 16 concrete lanes through intake, fake-provider review, deterministic
  reaggregation and score emission, with independent paths and fingerprints.
- Divergent exploratory/rigorous decisions, challenged fatal findings, heuristic
  coverage, cost contradictions, schema failures and provider failures.
- Exact/sampled differential experiments, strict manifests/source inventories,
  measured-scope limitations, and bounded source/report views for the judge.
- Draft, stale package, changed source, report/dossier/configuration tampering,
  wrong-lane and nonfinite-score rejection, and no execution in judge/score stages.
- Committee role/model/strategy selection and provider-specific structured output.
- Independent SHA3/Keccak and MD-family hash reference vectors.
- Pinned-parent submission surface checks, including sibling promotions.

`HASHSMASH_TEST_DOCKER=1 python3 -m unittest tests.test_experiments tests.test_frontier_pipeline`
passes all 33 tests, including the four real Docker checks. These confirm actual
non-root, credential-free, networkless/read-only isolation; timeout and output
limits; repeated identical-request execution; a reduced-MD5 positive witness
control; and the complete selected SHA-256 round-31 experiment-to-score pipeline
with fake judges. No mathematically unsupported real challenge score is created.

The initial unprivileged desktop-sandbox attempt could not reach Docker; rerunning
with approved daemon access passed. Docker/image/socket preflight failures are now
explicit development setup errors, with no host-execution fallback.

All 16 new candidate templates pass mechanical validation as drafts. No template
is submitted to inference and none emits a score. `validate_frontier_config.py`
reports 28 planned slots, 16 runnable lanes and 12 pending definitions.

## Yukon compatibility checks

Both leaf manifests pass the actual local Yukon TypeScript
`loadRepositoryBenchmarkManifest` parser at commit
`d9471fe70a431a3c424758c3eb58d51d38e73d67`. Each loads eight tracks and satisfies
its independent editable/score paths. The current remote source inspected at
`7530a1dc94dcd7d1d24e3b6c758b59dadc231c4b` retains the 20-track limit.
All 16 temporary fake-provider pipeline scores also pass Yukon's actual
`parseBenchmarkScore` with exactly the expected scalar preserved.
All generated workflow YAML files parse; literal per-track wrappers select the
matching lane. `git diff --check` passes.

These checks do not substitute for GitHub Actions dispatch or Yukon import,
baseline, submission and promotion tests. In particular, two leaf challenges on
one branch must be tested for cross-challenge preservation before deployment.

## Live judge diagnostics

The bounded calibration harness uses only organizer toy maps, never real challenge
candidates. Its cases distinguish an exact correct proof, a concrete false proof,
and an evidence-supported but unresolved probability estimate. The third is a
policy diagnostic, not a ground-truth cryptanalytic label. Reports are ignored
under `.yukon/reports/paired-calibration/`; no scores/baselines are emitted.

Bedrock model `us.openai.gpt-5.6-sol`, region `us-east-1`, Responses API, high
reasoning, and the six-role `paired-roles-v1` strategy committee were tested with
one transport attempt per stage. Run ID: `20260904T201841Z-2ff0d5e6`.

| Case | Exploratory | Rigorous | Calls | Input / output tokens |
| --- | --- | --- | --- | --- |
| Exact toy projection collision | `plausible_not_refuted` | `ai_rigor_qualified` | 4 | 15,746 / 7,811 |
| False toy projection collision | `refuted` | `refuted` | 6 | 24,710 / 13,903 |
| Unresolved empirical success estimate | `plausible_not_refuted` | `not_qualified` | 4 | 48,686 / 16,738 |

All three cases matched the intended protocol outcomes (14 live stage calls,
127,594 input-plus-output tokens). The heuristic's finite evidence was admitted
as exploratory support without being elevated to a rigorous probability bound.
Its unknown truth is not counted as a true/false classification label.
The 32 toy batches and 17 successes were independently recomputed during audit.
All reviewers distinguished algorithmic success from uncertainty about the
premise. The experiments reviewer also correctly noted that this toy fixture
contains a source hash and finite results, not a sandbox source/environment/replay
record or measured attack cost. The actual Docker evidence path was tested
separately through the full pipeline with organizer fixtures and fake judges.

Auditing the positive case confirmed the algebra and conservative cost bound;
the cost reviewer correctly noted a minor output-accounting ambiguity that still
fit the declared bound. In the false case, three independent reviewers identified
the unequal outputs, and both defender and adjudicator confirmed every fatal
finding. These are meaningful end-to-end protocol checks, not novel attacks.

Two diagnostic limitations remain visible: some positive-case JSON-pointer
citations were malformed despite valid supporting proof-line citations; reference
existence is not yet fully checked mechanically. The false case's experiments
reviewer repeated the false equality while marking experiments unnecessary.
Independent correctness/cost reviews prevented acceptance, but that specialist
mistake remains in the immutable dossier. Do not equate an aggregate success on
these cases with uniformly reliable individual reviews.

Real cryptanalytic precision/recall remain unmeasured. A labeled corpus with expert
review is still required before interpreting the lane objectives as error rates.
