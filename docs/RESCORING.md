# Computation accounting and reorg judgments

## Prices

V5 scores log2(total computation in target-compression equivalents). One selected
compression/permutation costs 1; each other 256-bit RAM primitive costs 1/C.
Memory remains a required metric, with no scalar contribution or tie-break.

| Target | C |
| --- | ---: |
| MD5-s63 / s64 | 843 / 856 |
| SHA-1-r79 / r80 | 1957 / 1982 |
| SHA-256-r31 / r32 | 2140 / 2224 |
| SHA3-256-r5 / r6 | 1355 / 1626 |
| BLAKE3-r1 / r2 | 222 / 430 |
| Keccak[800]-r5 / r6 | 1355 / 1626 |

`python3 scripts/reference_operation_costs.py` reproduces these estimates from the
trusted reference cores. It counts additions, logical operations, shifts and masks
on data words, including message expansion and feed-forward. Narrow rotations use
their explicit 256-bit-RAM implementation. Public loop/index arithmetic, Python
overhead, memory traffic and serialization are excluded from this reference
normalization. These are portable data-path estimates, not CPU timings or complete
instruction counts. All actual attack work, including memory accesses, remains
charged; a whole compression's internals must not also be charged individually.
Weights can alter rankings. Pending targets require their own reference costs
before activation; the shared model does not assign invented costs to them.

The definitions follow [MD5](https://www.rfc-editor.org/rfc/rfc1321),
[SHA-1/SHA-256](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), and
[Keccak](https://keccak.team/keccak_specs_summary.html).

## Submitted scores

Ordinary submissions are scored at their justified `claim.time_log2` bound under
the current public accounting rules. One target compression costs 1 and an ordinary
operation costs the selected `operation_weights.word_operation`. For example,
H target compressions and W ordinary operations cost `log2(H + W/C)` before any
additional charged work. Include preprocessing, failed trials and recovery at the
claimed success probability. State the tightest bound you can support; the judge
does not automatically tighten the submitted scalar.

Explain the calculation in the proof. Submissions and judge outputs have no
`resource_ledger` field; there is no intermediate ledger schema or pricing engine.
Remove that obsolete field from replacement packages and keep their cost reasoning
in `proof.md`.

## Reorg judgments

Yukon continues dispatching its ordinary workflow. An organizer-reviewed
`reorg/plan.json` entry supplies a previous judgment for an exact track, package
and source/destination configuration. Unlisted submissions receive ordinary review.

The reorg judge receives the original submission and experiment report, a
chronological list of judgments, and current judging instructions. Previous
judgments provide reusable reasoning, not a binding verdict. The judge can accept
or reject under the current rules, revisiting what changed prompts, accounting or
configuration require. A pricing-only change will usually leave validity reasoning
applicable, but does not guarantee acceptance. Missing information can instead
produce `needs_evidence`. Neither rejection nor missing evidence produces a score.
Target, algorithm, success probability and lane remain bound to the submission.

For accepted results, the score rule is explicit:

- Same scoring policy: retain the latest accepted score exactly. A first reorg
  retains the submitted score; a later reorg retains the previous reorg's score.
  A tighter reconstruction or unrelated prompt/checker change does not alter it.
  An intervening rejected or incomplete review does not erase that scored judgment.
  If no judgment has accepted it yet, use the original submitted bound and policy.
- Changed scoring policy: the judge gives a revised computation bound and a short
  calculation with evidence references. No prescribed intermediate ledger is needed.

Scoring policy identity is the public cost-model ID plus the selected target's
actual operation weights. Bump the public ID when accounting rules change; a
price-only change is detected without a version bump. Changes to other targets'
prices, comments, judge prompts or general configuration hashes do not by themselves
change a submission's scoring policy. Organizer pins still authorize the exact
configuration transition independently of this score comparison.

The final review contains only status, a computation bound (null unless accepted),
and a concise explanation. The harness supplies stage/version/binding metadata and
preserves the previous score on acceptance when policy is unchanged. Rejected and
incomplete judgments remain in history. Only the selected lane is reviewed; sibling
lane decisions are not carried forward as current decisions.
Memory, data and advice metrics remain reported separately. Scores record the
original declared bound, previous score, `rescoreMode` and source packet.

## Artifact handoff

1. Download the trusted workflow's review artifact, including its bundled history.
   Run `scripts/archive_review.py --evidence PATH --dossier PATH` to verify and
   cache it locally and print a proposed plan entry.
2. Review the entry into `reorg/plan.json`. Map its source packet hash to the trusted
   workflow's `run_id` and `artifact_id` in `reorg/artifacts.json`. Only IDs and
   hashes enter Git; the full judgments stay in workflow artifacts.
3. Merge the reviewed plan and perform the normal managed Yukon reorg. The workflow
   downloads the pinned artifact and checks its content and ancestry before review.
4. Pin the newest review artifact for a subsequent reorg. It bundles the prior
   judgments in `rescore-history.json`, so earlier artifacts need not survive
   independently.

History loading verifies organizer pins, artifact integrity and submission identity.
It preserves recorded conclusions without replaying today's output validators or
qualification rules on old reviews. The new result still receives schema, binding,
qualification and score-preservation checks before scoring.

### Reset from the original judgments

The ledger-based `review-rescore-v1` judgments are deliberately excluded. Pin the
original ordinary reviews instead; the existing artifact map identifies those
originals. The reorg judge then calculates new bounds from the original submission
and reasoning under the current accounting rules. This reset does not preserve the
intermediate ledger-derived scores or supply those judgments as evidence.
Subsequent reorgs retain the new simple judgments, including rejected decisions.

Artifacts currently expire after 30 days. Missing or mismatched artifacts stop
explicitly; restore a trusted backup or choose a fresh review. History is bounded
to 32 records and 2 MiB of model input, with an explicit error on overflow.

The initial migration plan is retained in
[the historical plan](../reorg/history/pre-blake3-keccak800-plan.json). The completed
simplified-judgment migration is retained unchanged in
[its archived plan](../reorg/history/completed-simple-judgments-plan.json), covering
16 baselines and 9 previously scored submissions. Its artifact references remain
in `reorg/artifacts.json` for provenance.

The active `reorg/plan.json` now has no entries. Future evaluations use ordinary
review, including packages formerly pinned by the completed migration. Clearing
the completed plan does not dispatch workflows, replay submissions, or change
published scores. Historical plans are not loaded by the pipeline. A future reorg
requires a new reviewed active plan authorizing its exact configuration; never
silently reuse or update an old destination hash after a harness change.
