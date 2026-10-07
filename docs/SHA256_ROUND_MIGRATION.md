# SHA-256 exploratory rounds 37/38 rollout handoff

Prepared 2026-10-07 against freshly fetched production `Layr-Labs/hash-smash`
`main` at `453b888ec54f554e63250dd2c26d638c254c2358`. This document is a repository
handoff, not evidence of live closure, judging, import, merge or UI deployment.
Re-read production source/state before applying a reviewed release.

## Desired roster and preserved history

The root schema-v2 manifest retains **eight exploratory registrations**. The
original six entries are unchanged, with exactly two entries appended:

| Tracks | Registration action | Intended admission after rollout |
| --- | --- | --- |
| `sha256-r31-exploratory`, `sha256-r32-exploratory` | Retain existing IDs and all records | Closed, publicly readable history |
| `sha3-256-r5-exploratory`, `sha3-256-r6-exploratory` | Retain existing IDs and settings | Restore competing state after refresh |
| `blake3-r1-exploratory`, `blake3-r2-exploratory` | Retain existing IDs and settings | Restore competing state after refresh |
| `sha256-r37-exploratory`, `sha256-r38-exploratory` | Add two new IDs | Open only after qualification and release checks |

Thus **six tracks are intended to compete**. The manifest cannot encode closed
state; a source edit alone does not close a lane. Do not remove r31/r32 from the
manifest, archive their registrations, rename them, or map their results to new
rounds. Yukon archival removes records from normal public benchmark endpoints.
Keeping the old records closed preserves access to their results and URLs.

All four local r31/r32 lane identities, profiles, workflows, candidates and
historical artifact references remain intact. The registry has 26 runnable lanes:
22 current research lanes plus four historical lanes. The current plan has 26
slots: 22 defined and four deferred Poseidon slots. The new SHA pair has only two
exploratory lanes; rigorous r37/r38 packages/workflows are not introduced. Local
registry membership does not imply registration or open admission.

## Exact target and fresh baseline work

Both new selections are `organizer_selected`, with `first_unbroken_round: null`.
No new attack, first-unbroken boundary, score or qualification is asserted.
The [r37 profile](../target-profiles/sha256-r37-prefix-v1.json) and
[r38 profile](../target-profiles/sha256-r38-prefix-v1.json) use:

- All byte-string messages of bit length less than 2^64, with distinct complete messages.
- The standard SHA-256 IV once at the start of the message.
- FIPS 180-4 padding, including the original 64-bit big-endian bit length.
- The first 37 or 38 rounds (indices 0..36 or 0..37) on **every padded block**, with original schedule/constants.
- Standard feed-forward after each reduced compression, chaining across all blocks, and the full big-endian 256-bit digest.

Free-start, compression-only, unpadded, shifted-round or truncated-output results
are different problems. Earlier r31/r32 witness pairs or proofs do not establish
r37/r38 claims. The reference core already implements these semantics; it is
unchanged. Instrumentation in `scripts/reference_operation_costs.py` measures
C=2644/2728 respectively. These are normalization prices, not attack costs:
one target compression costs 1; another primitive word operation costs 1/C.
All old prices and `collision-frontier-v5` accounting rules remain unchanged.

Only the two new candidate directories contain newly authored draft scaffolds.
They have empty certificate manifests, no experiments and nominal placeholder
numbers. Follow [candidate qualification](./CANDIDATE_QUALIFICATION.md) to replace
each scaffold with its own substantive algorithm, success argument, complete
resource accounting and disclosed heuristics. Set `ready` only when complete.
Fresh exploratory review must qualify the exact package/configuration; readiness,
mechanical checks and nominal references cannot seed a successful import.
Existing promoted candidate content must not be overwritten with historical
baseline packages as a shortcut to qualification.

## Protected fingerprint impact

This change requires **`yukon-unsafe`**. The checked-in
[fingerprint comparison](./validation/sha256-r37-r38-fingerprints.json) records
every before/after hash; [validation](./FRONTIER_VALIDATION.md) records offline evidence. Every one of the 24 pre-existing local
lane configuration hashes changes, including all six existing live registrations.
The transitive causes are:

| Protected input | Why it changes | Configuration contribution |
| --- | --- | --- |
| `verifier/frontier_tracks.py` | Explicit lane subsets and preserved historical pairs | All verifier/experiment module bytes feed `reference_checker_sha256` |
| `schemas/claim-frontier-v3.schema.json` | Append the two allowed profile IDs, retain existing IDs | Shared `qualification_policy.sha256` |
| `cost-models/collision-frontier-v5.json` | Append two measured normalization entries | Full shared cost-model object in every benchmark/configuration |

The hash cores, judge implementations/prompts, qualification gates, old target
profiles, old selected operation weights, and all existing candidate bytes remain
unchanged. That does **not** make old dossiers current: exact configuration gates
must still reject stale evidence. Do not exclude protected files from hashing,
patch prior artifact hashes, or weaken stale-configuration checks.

All retained records need the supported guarded configuration refresh. Closed
r31/r32 records are included too. A passing add-only reconciliation does not
refresh retained configuration. Old artifacts stay attached to their original
source and policy; new qualification is a separate result. For an accepted reorg
judgment with unchanged scoring policy (model ID and selected weights), current
[rescore rules](./RESCORING.md) preserve the previous score; they do not guarantee
acceptance or successful requalification. Any future active reorg plan must pin
its exact source/package/destination and trusted artifact provenance. Existing
historical plans are not active authorization and must remain untouched.

## Operator sequence, separately authorized

**Prepare before the maintenance window.** Complete baseline authoring for both
new lanes, offline validation, substantive package review, harness PR review,
and the separate UI implementation/tests/review while existing admission continues.
Prepare the signed release and UI configuration mapping with only the future
production UUIDs unresolved. Confirm the baseline review/qualification evidence
and intended final source are ready for exact-source verification. Do not pause
the live challenge while open-ended research or UI implementation is unfinished.
Agree a bounded maintenance window and recovery owner before the sequence below.

The rollout source inspection used Yukon `9ce213d9c7867c365ce42ad4bd54ebe84522a5ce`. Its
`src/store/benchmark-reorg.ts` includes closed nonarchived siblings, preserves
originally closed tracks as closed after reorg, and leaves other tracks paused.
Verify the deployed version still has that behavior. Do not invent a per-track
reorg exclusion or an empty accepted-submission scope: production has real results.

1. **Freeze and inventory.** Record all six existing benchmark IDs, source refs,
   settings, admission/closing states, baselines, current bests, submissions,
   human review decisions, promotion state, pending jobs and artifact bindings.
   Obtain the actual challenge reference; the GitHub organization is not the
   setter namespace. Include queued/running validation and promotion jobs;
   public baseline-job listings alone are insufficient. Preserve audit exports
   and artifact retention before any lifecycle changes.
2. **Stop admission and settle old work.** Close r31/r32 with the supported owner
   close operation; pause the other four competing records. Drain queued/running
   jobs and promotions and resolve or explicitly preserve pending reviews under
   the supported transition. Do not accept stale scores, discard reviews or
   manually merge submission PRs. Record every human decision separately from
   AI review. Preserve r31/r32's closed state thereafter.
3. **Verify and land the prepared release.** Confirm the already-complete baseline
   packages, offline checks, substantive reviews and UI preparation against the
   frozen production source. Mark the signed harness PR `yukon-unsafe` and merge
   the reviewed harness/candidate release only under separate approval. If production
   moved during preparation, preserve every promoted candidate/sibling change and
   repeat the necessary review before maintenance, rather than beginning research
   during the outage. Record final source/tree and recompute all fingerprints.
   Repository draft scaffolds alone are not rollout-ready.
4. **Preview reconciliation.** On the existing production challenge, inspect the
   supported reconcile preview for the exact reviewed source. Expect `retain=6`,
   `add=2` (only r37/r38), `archive=0`, and no unexpected retries. Apply only the
   inspected revision. A changed state/revision or uncertain response requires
   read-back and a new preview, not blind retry. Verify all six original IDs,
   settings, submissions and public results survive. New r37/r38 baseline jobs
   must qualify; failures do not roll back reconciliation. Keep admission stopped.
5. **Refresh all eight guarded records.** After additions settle, inventory the
   actual accepted submissions, manual decisions, previous judgments and trusted
   artifacts. Use the supported owner reorg flow and reviewed scope against the
   exact release to refresh all eight baseline/configuration records and eligible
   accepted submissions. Preserve human decisions and inspect actual replay jobs;
   do not assume zero accepted submissions or promise exclusion of closed tracks.
   If rescore history is used, prepare exact organizer pins under
   [RESCORING.md](./RESCORING.md) rather than carrying old judgments forward as
   current. Await every required job and inspect failures before any state restore.
6. **Verify qualification and preservation.** Record package/config hashes, review
   outcome, unresolved obligations, scalar if emitted, baseline/submission job IDs,
   workflow source/attempt, artifact IDs/digests and exact score ZIP entry for
   each record. Failure must emit no successful score artifact. Confirm r31/r32
   remain closed and publicly readable, other records are paused, original IDs
   and all histories/manual decisions remain intact, and new IDs are distinct.
7. **Coordinate UI, then restore intended admission.** Complete the separate Yukon
   UI release below with real new refs. Verify it while tracks remain stopped.
   With explicit opening/resumption approval, restore only the four retained
   competing siblings and open r37/r38. Check six intended competing tracks and
   two closed history records. Never reopen r31/r32 as a side effect of reorg.

On failure, leave affected admission stopped and retain all records/artifacts.
Recover through the supported workflow against the inspected current state.
Deleting/reimporting a challenge or archiving/reintroducing a name loses identity
continuity and is not rollback. No live steps above were performed by this change.

## Separate Yukon UI implementation and release

UI source lives in **`Layr-Labs/yukon/apps/challenges-ui`**. Nothing here implements
or deploys that app. Its follow-up must include:

- Update the HashSmash SHA-family catalog/types to current pair `[37,38]`, remove
  `firstUnbrokenRound:32` as current selection metadata, and express organizer-selected
  exploration. Preserve historical 31/32 track definitions and result attribution.
- Update `challenges/hashsmash/lib/validate-snapshot.ts`. The inspected validator
  accepts only two/four family tracks, requires every track round in `roundPair`,
  and assumes paired lane slots. Six SHA definitions (four historical and two new)
  require an explicit current/history and exploratory-only contract. Simply
  appending IDs or changing `roundPair` breaks validation.
- Extend `lib/hashsmash-refs.ts` and `lib/env.ts` with distinct r37/r38 ref keys.
  Retain r31/r32 refs. Wire the real new production UUIDs after registration;
  neither copy dev UUIDs nor overwrite old environment keys with new IDs.
- Verify `lib/yukon/catalog.ts` and SHA selectors/defaults use the current pair
  while plots/results can show historical rounds. `round-axis.ts` supports active
  plus plotted rounds, but that alone does not update defaults or retirement labels.
- Keep `adapter.ts` authoritative target ID/profile/round checks. Historical
  configuration hashes are provenance, not permission to relabel an r31/r32
  result as r37/r38. A nominal value or unqualified draft must not appear as a
  new result, successful baseline or first-unbroken marker.
- Test snapshot validation, malformed/duplicate historical IDs, exploratory-only
  current slots, new ref/schema parsing, current defaults and closed-track labels.
  Regress old r31/r32 deep links, filters, charts, result details and public proxy
  fetches, plus new results bound to their exact target. Confirm no history is
  lost or remapped and all sibling families still render correctly.
- Release the reviewed app and exact environment/ref changes separately; rebuild
  public environment values as required by that deployment. Read back rendered
  data and API/proxy parity for all eight registrations before restoring admission.

Remaining release decisions are baseline authors/qualified packages, exact human
review/reorg scope and downtime, signed release approval, production UUID/env
mapping, UI implementation/release owner, and explicit admission restoration.
No score, qualification, new UUID or rollout completion is inferred by this patch.
