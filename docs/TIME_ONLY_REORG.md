# Total-computation scoring migration

`collision-frontier-v4` changes the official scalar from `time_log2 +
memory_log2_bytes` to `time_log2`. Computation units, the 0.39 success requirement,
preprocessing, failed trials, verification, nonuniform construction costs and
qualification gates remain unchanged. Time is total work across all processors,
not parallel latency. Memory is still required, reviewed, and emitted in
`metrics.memoryLog2Bytes`, but never breaks ties. This policy applies to all 28
planned slots; the 12 unresolved slots remain inactive.

New scores identify `costModelId: collision-frontier-v4` and
`scoreMetric: timeLog2`. They do not emit the former `timeMemoryLog2` metric.
The v3 cost model remains as a historical definition. Claim schema v3 is retained
so original submission archives can be replayed without rewriting participants'
claims. Configuration fingerprints change; old reviews and scores are invalid
for the new policy. Archived references to the former scalar are historical
context, while original algorithm and resource bounds receive fresh review.

The trusted judge prompt explicitly states that v3 and v4 use identical resource
units and accounting. A v3 reference does not require a new cost-transfer heuristic.
Original archives can describe the former scalar as current because they predate
the migration; the organizer supplies its present interpretation. This does not
supply missing evidence for the original resource bounds or reuse an old verdict.

## Consequences

- A time bound of 73 with memory exponent 21 changes from score 94 to 73 if the
  submission qualifies again. This is a formula illustration, not a new verdict.
- Larger memory can buy a better score when it reduces total work. Memory access,
  table construction and preprocessing still cost time. Equal time scores tie
  regardless of memory. This policy intentionally does not rank physical cost.
- The nominal MD5 reference remains 64. Keeping the existing instruction units
  does not guarantee an exact implementation score of 64.
- Review is rerun, not just arithmetic. AI verdicts can change, and all baseline
  validations must succeed before Yukon resets and replays submissions.

## Review and rollout order

1. Review the harness PR and its matching Yukon Challenges UI change. Mark the
   harness PR `yukon-unsafe`: pending scores require fresh qualification.
2. Publish the compatible UI before new scores can arrive. It must validate the
   official scalar using the organizer baseline's cost-model markers, retain
   correctly labeled v3 results before migration, and keep different policies
   out of a common frontier. The former adapter rejects every nonzero-memory
   time-only score because it requires score = time + memory.
3. Pause all 16 active tracks and drain validation and promotion jobs. Record
   benchmark/submission/job state, source SHA, and previous score artifacts for
   audit. Recheck source and candidate changes after draining; promotions can
   advance main during preparation.
4. Land the reviewed harness on current `main`. Preserve track membership,
   editable paths, direction, and the inactive target definitions.
5. Choose and record the baseline candidate source. To replay improvement history
   from the original organizer baselines, restore only candidate directories in
   a separate forward commit on top of the new harness. Never reset the entire
   branch or undo the scoring change. Review the exact candidate-only diff.
6. Start one managed reorg from the importing account. Any track reference
   includes all sibling tracks. Let Yukon validate the 16 fresh baselines, then
   replay original submission archives through normal improvement and manual
   review/promotion rules. Do not manually merge submission PRs or overwrite
   scores in the database. Freeze harness edits during replay: Actions resolves
   the current branch tip for each submission.
7. Inspect every baseline, replay outcome, new metric, UI result and pending
   review. Previously closed tracks remain closed; the others remain paused
   until explicitly resumed. Wait for outstanding reorg jobs and promotions
   before reopening. Existing reward calculations/payouts are not recalculated;
   review them separately if this challenge has any. Deadlines do not extend
   automatically, and there is no automatic reorg undo.

## Baseline audit at preparation

The imported repository is `mooselumph/hash-smash`. At inspected main
`7890eca193f058545f420d8a5a6ffa001dda0595`, only
`lanes/exploratory/candidates/md5-s63/` differs from the initial imported
candidate trees at `eb46ab9bdceacf628cf40fdad923725e9261e148`.
Commit `5965256` had already restored the original baselines, and `7890eca`
subsequently promoted a new MD5 candidate.

The original MD5 candidate declares time 79 and memory 72; the current candidate
declares time 73 and memory 21. If both qualify under v4, starting at the current
candidate establishes baseline 73, so replaying that same candidate cannot earn
an improvement. Starting at the original candidate establishes baseline 79 and
preserves the opportunity for that submission's improvement to be recognized.
Other submissions may change the eventual winner. These are declared bounds,
not a prediction of fresh review outcomes.

After pausing and refreshing this audit, the candidate-only restoration is:

```sh
git restore --source=eb46ab9bdceacf628cf40fdad923725e9261e148 -- \
  lanes/exploratory/candidates/md5-s63
git diff -- lanes/exploratory/candidates/md5-s63
```

Commit that reviewed restoration separately from the harness. No restoration,
merge, UI deployment, or reorg is performed merely by applying the scoring PR.

Platform behavior is documented in the
[Yukon managed reorg runbook](https://github.com/Layr-Labs/yukon/blob/2649b169926cabe830f8bb23a5a4c2e695edd11f/docs/benchmark-remediation.md#automated-benchmark-reorg).
