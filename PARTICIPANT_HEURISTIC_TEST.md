# End-to-end participant Python heuristic test

This diagnostic submits a Markdown argument, a structured heuristic claim, and an
actual participant Python program through the existing intake, Docker executor,
trusted evidence builder, paired review, and score gate. It does not deploy Yukon,
change an active track, promote a baseline, or claim a cryptanalytic advance.

## What the fixture tests

The immutable organizer test package is in
[`tests/fixtures/participant-heuristic/candidate`](./tests/fixtures/participant-heuristic/candidate).
It uses the existing eight-step MD5 full-message profile, with standard IV,
feed-forward, padding, and the complete 128-bit output. A test-only paired track
instantiates the existing frontier claim schema by changing **only** its allowed
target enum to `md5-s8-prefix-v1`. That schema instance, the driver, the fixture,
and the ordinary verifier/policy files are hash-bound. The production registry
does not admit this calibration ID; no active track definition is edited.

Each batch expands one 256-bit seed into 256 16-bit values using SHA-256. The first
repeated value yields two different 64-byte messages that agree in the words
read by the first eight MD5 steps and differ in an unread word. Their identical
second padding blocks preserve the collision. This witness argument follows the
MD5 schedule and padding in [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321).
Full SHA-256 is only the seed-expansion primitive, as defined in
[FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

The score-critical heuristic is different: the probability of finding a duplicate
in one such batch is claimed to be at least 0.39 over uniform seeds. Independent
uniform 16-bit draws would give

`1 - product(1 - j/65536, j=0..255) = 0.392677526731787...`.

That identity for ideal draws does not establish the joint distribution of the
concrete SHA-256 expansion. The program reports every organizer trial, including
failure. A finite observed frequency supports evaluation of the premise but is
not itself a confidence lower bound or a proof of independence. The experiment
also does not certify the separately stated logical-RAM time/memory ledger.

The construction is deliberately inefficient: deterministic ignored-word
collisions are easier on this shallow target. Its purpose is to give us a real,
auditable execution supporting a disclosed heuristic, not to improve MD5 research.

## Execution and trust boundaries

1. A fresh run directory receives a copy of the frozen fixture and an explicit
   test-only schema instance. Package/configuration hashes are recorded before
   execution; no seed search is performed.
2. In a provider-credential-free process, normal intake invokes the production
   networkless, non-root, read-only Docker executor with its pinned image and
   resource limits. The program receives 256 fixed organizer seeds.
3. Two fresh executions must return byte-identical output. The trusted host
   recomputes both complete target digests for every returned pair. All failures
   remain in the report. Participant-declared success counts are not trusted.
4. A separate credential-bearing process reviews the saved, fingerprint-bound
   evidence. It does not run participant code. Additional fail-closed guards
   prohibit execution calls during this phase. Each model sees the source,
   measured counts, report binding, and experiment scope limitations.
5. The ordinary paired aggregation and score gates run unchanged. At most six
   model stages are permitted, with one transport attempt each. No failed or
   unexpected judgment is retried automatically. Scores, if any, are confined
   to this calibration directory and are not leaderboard results.

The anticipated policy diagnostic is exploratory `plausible_not_refuted` and
rigorous `not_qualified`. Live outputs are recorded whether or not they match.
The claim is not supplied with an expected label to the model. A model may
reasonably expose a different unresolved obligation; inspect its dossier rather
than treating disagreement as an infrastructure defect.

An independent organizer audit in the regression tests reconstructs every seed
and every first duplicate using a dictionary implementation, instead of the
submitted linear scan. This catches incorrect failure rows as well as incorrect
returned pairs. It never imports or executes participant source on the host,
and it is **not** silently added to the judge's evidence. The generic production
runner checks returned witnesses, not the truth of arbitrary internal program
claims or the completeness of a participant's search.

## Commands

Offline regression suite, with no Docker or model calls:

```bash
bash .yukon/setup.sh
```

Real participant execution, followed by explicitly fake model responses, to
test mechanism and aggregation without provider costs (use a secret-free shell):

```bash
HASHSMASH_TEST_DOCKER=1 python3 -m unittest \
  tests.test_participant_heuristic.ParticipantHeuristicTests.test_real_participant_python_then_offline_judges -v
```

Full local Bedrock integration:

```bash
bash scripts/run-participant-heuristic.sh \
  --provider bedrock --model us.openai.gpt-5.6-sol
```

The wrapper first runs the offline suite and sandbox preparation with known
provider/AWS/GitHub credentials removed. Only afterward does it source the
organizer's local `.env` for a separate review process. It never prints or copies
that file. Docker and the pinned image must already be available; there is no
host-execution fallback. Default per-stage limits are 16,384 output tokens and
180 seconds. OpenRouter is also supported with `--provider openrouter` and its
corresponding model identifier.

Raw source snapshots, numerical results, evidence, dossier, and optional score
stay under ignored `.yukon/reports/participant-heuristic/<run-id>/`. The CLI prints
the exact directory. To inspect a completed run without contacting a provider:

```bash
python3 scripts/test_participant_heuristic.py inspect --run-directory PATH
```

Direct `prepare` and `review` commands are available for separate jobs. Preparation
refuses known credential-bearing environments, existing directories, and holdout
overrides. Review refuses already-attempted runs and changed evidence/configuration.
Changing a hash-bound implementation can change the deterministic samples; keep
all previous records and do not select the most favorable run.

## Evaluation criteria and limits

Offline tests cover exact schema isolation, all-trial accounting, source/evidence/
claim/schema tampering, credential boundaries, setup failure, repeated-review
protection, provider failures, and withholding scores. Fake responses test routing
only. The Docker case exercises real participant code; the live case adds real
model judgment. This stage-specific distinction follows the task-specific,
logged evaluation approach in the
[OpenAI evaluation guide](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

One fixture is not a measurement of false-positive or false-negative rates.
Public deterministic seeds are not a blinded holdout. Returned witnesses do not
establish expected attack cost, population success probability, or human acceptance.
The test is local; a full Yukon import/submission/promotion test remains separate.

## Recorded validation

Recorded on 2026-09-04; machine-readable summary:
[`validation/participant-heuristic-20260904.json`](./validation/participant-heuristic-20260904.json).

- Full offline suite: 226 discovered, 221 passed, five opt-in Docker cases skipped.
- New real-Docker integration case: passed with fake reviewers and real scoring
  gates. An initial daemon/image preflight failed; the exact preflight then
  succeeded and the unchanged test passed. No isolation policy was relaxed.
- Preserved prepare-only run: `20260904T210454Z-2b47fa53`.
- Two byte-identical sandbox executions; 82 full collisions and 174 failures in
  256 trials, observed fraction **0.3203125**.
- Independent organizer reconstruction confirmed every trial, including all
  failures and first-duplicate selection. The returned pairs' full 128-bit
  reduced-MD5 digests were checked again.
- **No live model call occurred for this fixture.** The app's permission reviewer
  rejected the live wrapper before execution because it required explicit
  authorization to send the source, proof, and evidence to Bedrock. The saved
  numerical report is ready for a separately authorized review. There is no
  live lane verdict or live diagnostic score to report.

The observed frequency is below both the 0.39 claim and the approximately 0.39268
ideal model. This is not favorable confirmation. Under an *additional iid
Bernoulli model for the 256 trials*, the probability of 82 or fewer successes is
approximately 0.0124133 at p=0.39, or 0.00988012 at the ideal birthday probability.
These are model-conditional tail areas, not validated population probabilities
for the actual deterministic seed set. They are post-run sensitivity diagnostics,
not an added certificate or evidence secretly appended to the judge's input.

The lower-than-predicted sample is retained without altering the fixture, public
seed, hypothesis, or expected-label diagnostic. The original hoped-for exploratory
pass is not guaranteed by this evidence; live disagreement would be informative.
The report hash is
`9300aa7f7dc01daf180e7ffd6791fa68b4a90379acdaaba1c7e6ec0f82fe8087`.
Raw local artifacts remain ignored; the source, reproducible protocol, and this
validation summary are committed for worktree users.
