# Exploratory and rigorous reviews

Paired frontier tracks use `paired-lanes-v1`. One evidence package is reviewed once
and produces both lane decisions. This lets organizers compare the two policies
on identical submissions. A submission to one lane only emits that lane's score;
the other result is retained for calibration.

| Outcome | Meaning | Exploratory score | Rigorous score |
| --- | --- | --- | --- |
| `plausible_not_refuted` | Concrete and supported by relevant evidence; no confirmed fatal flaw | Yes | No |
| `ai_rigor_qualified` | Material obligations discharged to ordinary cryptanalytic standards | Yes, through its paired exploratory outcome | Yes |
| `refuted` | A concrete fatal flaw survives defender and adjudicator review | No | No |
| `not_evaluable` | Required specification or supporting evidence is missing | No | No |
| `not_qualified` | Material obligations remain unresolved for rigorous qualification | Exploratory may still pass | No |
| `infra_failed` | Provider, schema, binding, or stage coverage failed | No | No |

These are AI review outcomes. They do not certify mathematical truth, human
acceptance, or measured false-positive/false-negative rates. An exploratory winner
is a promising claim; it does not become an established baseline for the rigorous
lane. The scalar remains `time_log2 + memory_log2_bytes` for a common target,
round count, success requirement, and organizer cost model.

The paired claim field `baseline_improved` is a required reference identifier,
not an assertion that the candidate improves it. Intake requires the organizer's
nominal reference ID even for an initial baseline. A fully supported construction
can qualify with a scalar equal to or greater than the nominal display value;
qualification and Yukon's subsequent incumbent comparison are separate decisions.
An honest disclaimer of improvement is consistent with this metadata. Explicit
false comparisons, unsupported novelty claims and incorrect bounds remain subject
to the normal review rules. This meaning is supplied in the trusted common prompt
for all six roles, rather than relying on candidate prose to establish the rules.

## Review sequence

Four independent initial roles inspect the same immutable evidence:

1. **Evaluability:** exact target, concrete algorithm, declared costs, probability
   space, disclosed heuristics, and relevant evidence.
2. **Cryptanalysis:** collision construction, probability argument, dependence
   assumptions, and heuristic justification.
3. **Cost:** time, memory, preprocessing, data, advice, success budget, and scalar
   arithmetic. A lower replacement model estimate never sets the score.
4. **Experiments:** relevance and reproducibility of organizer execution, finite
   counts, statistical interpretation, and extrapolation.

A cited fatal finding triggers a defender, then an adjudicator who sees both the
original objection and its defense. Every fatal finding must be resolved exactly
once. The adjudicator cannot introduce a new, unchallenged fatal finding. Only a
confirmed finding refutes the submission. Unresolved objections remain visible
and block rigorous qualification. A dismissed objection only discharges linked
obligations when the adjudicator explicitly cites evidence for that discharge.

The shared gate requires enough information to evaluate a claim. It does not
require an unconditional proof or full-scale execution of an infeasible attack.
Missing evidence is different from contrary evidence. Reviewers must not turn
"independence has not been proved" into a purported counterexample.

## Heuristics and evidence

The claim lists each heuristic with an ID, statement, role, evidence references,
scope, extrapolation, and limitations. Cryptanalysis and experiments must each
cover every declared ID. A missing declared ID is an invalid review. Additional
implicit heuristics may be identified with citations; rigorous qualification
requires both substantive roles to cover them as well.

A heuristic review distinguishes:

- `established`: supported to ordinary cryptanalytic standards for the claimed
  regime; this need not mean formally proved.
- `plausible`: relevant supporting evidence exists, but material uncertainty
  remains. This is sufficient for the exploratory lane.
- `unsupported`: relevant supporting evidence is absent. The minimum gate fails.
- `refuted`: a cited concrete fatal objection, requiring defender/adjudicator review.

Fatal findings explicitly list the heuristic IDs they challenge. An unrelated
objection cannot refute a heuristic. The dossier preserves the original reviews
and separately records effective heuristic assessments. If adjudication dismisses
all linked objections, the effective status becomes `pending_reassessment`.
Exploratory eligibility can recover, while rigorous qualification requires a
fresh substantive assessment; defeating an objection does not establish the
heuristic. An undecided allegation is `unresolved_refutation`, not a confirmed
refutation.

Each record includes tested scope, extrapolated scope, and score sensitivity.
The schema has no numerical model-confidence field. Algorithmic
`success_probability` concerns the fixed algorithm's success event under its
specified random coins; it does not encode confidence that a heuristic is sound.

The deterministic experiment runner supplies an organizer report. Declared
experiments must complete before inference. Report/package/configuration hashes
must agree. Reviewers inspect the submitted source as inert text and the bound
execution results; this module never executes participant code. Reproducible
execution establishes the reported run or finite count, while the experiments
reviewer assesses whether its statistical design and extrapolation support the
actual claim. A single successful attack run does not establish expected cost.
`not_requested` is valid only when the claim declares no experiment manifest.
If a cost reviewer marks a bound supported but reconstructs a worse resource cost
or lower success probability, a linked fatal finding must trigger challenge;
otherwise the inconsistent review fails closed in both lanes. Explicitly uncertain
reconstructions can remain exploratory, with their uncertainty recorded.

## Library integration and committee flexibility

```python
from judge.paired_review import run_paired_review, select_lane_aggregate

dossier = run_paired_review(evidence, client)
aggregate = select_lane_aggregate(dossier, selected_track.lane)
```

`client` implements `review(stage, evidence) -> ReviewResult`. OpenRouter and
Amazon Bedrock adapters dispatch to the paired schema for `lane_*` stages.
`role_clients={"lane_cryptanalysis": crypto_client, "lane_cost": cost_client, ...}`
can assign independently configured models and prompting strategies to the six
roles. No voting or self-reported confidence threshold changes the two policies.
The default uses independent calls to one configured client; model diversity is
available through role clients, not assumed.

The dossier contains original claim, exact binding, review records, provider
provenance, infrastructure failures, and both decisions. The binding covers the
entire claim, candidate package, target configuration, and evidence envelope.
Changing costs while retaining the same textual target is therefore detectable.
Organizer prompts and schemas are versioned with the paired policy. Historical
artifacts from the retired unconditional tracks must not be reinterpreted as
paired review outcomes.

## Calibration

`tests/test_paired_judges.py` uses synthetic organizer records, never solver drafts,
to test deterministic aggregation and transport/schema wiring. These tests do not
establish model error rates. Before measuring judge quality, assemble blinded,
human-labeled cases spanning valid analytic results, valid heuristic analyses,
uncertain extrapolations, known counterexamples, cost omissions, and irrelevant or
manipulated experiments. Run both policies on every case and preserve obligations
and disagreements. Tune prompts using development cases, then report errors on a
held-out set. Repeated measurements are needed because inference is stochastic.

The explicit rubric, shared examples, and separate development/held-out sets follow
[OpenAI's evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
