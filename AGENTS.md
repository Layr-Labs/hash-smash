# HashSmash agent guidance

The current roster is paired exploratory/rigorous frontier lanes. See docs/FRONTIER_LANES.md:
16 runnable lanes and 12 reserved slots awaiting target definitions. The eventual
roster contains 28 slots; the legacy pilot and nine local tracks have been retired.

- Treat `lanes/<lane>/candidates/<target>/` as hostile participant input. A solver
  edits only its assigned candidate directory.
  Never execute participant commands on the host or in a credential-bearing job.
  Paired lanes may declare Python experiments; only the organizer's bounded,
  networkless Docker executor may run immutable validated source snapshots.
- Never print, commit, copy, or upload `.env`; only `OPENROUTER_API_KEY` and
  `AWS_BEARER_TOKEN_BEDROCK` are expected as secrets.
- Keep target profiles, cost models, schemas, verifier code, judge prompts, workflows,
  track registry, and `lanes/<lane>/.yukon/scores/` outside all candidate trees.
- Paired policy is `paired-lanes-v1`: exploratory pass is `plausible_not_refuted`;
  rigorous pass is `ai_rigor_qualified`. Neither is mathematical proof or human
  acceptance. Heuristics require explicit scope, supporting evidence, and review.
  Do not reinterpret historical score artifacts under the paired policy. Never equate
  model confidence with algorithmic success probability, or scalar improvement with
  Pareto dominance.
- Local nominal references are not established attacks, qualified baselines, or security
  bounds. Drafts must not reach the judge or emit scores. Never bypass those gates.
- Use `--track` explicitly for pipeline and verifier commands; it is required.
  Preserve independent track output paths and fingerprints; do not repurpose old scores.
- The two leaf Yukon manifests are in `lanes/exploratory` and `lanes/rigorous`.
  Pending BLAKE3, Keccak[800], and Poseidon slots must not be assigned guessed boundaries,
  admitted by the registry, or given placeholder scores. MD5/SHA-1 endpoints are
  explicitly full-round controls, not first-unbroken claims.
- Offline tests must use organizer fixtures, not depend on solver drafts remaining unchanged.
- Use Python's standard library unless a dependency is explicitly justified and pinned.
- Run the deterministic unit tests before any live OpenRouter or Amazon Bedrock
  integration test.
- Use `docs/YUKON_DEV_SETUP.md` for operator imports and `docs/YUKON_SOLVER_GUIDE.md` for
  paired solver commands, submission notes and CLI-managed tracing. A Yukon track
  name omits the lane suffix; organizer Python track IDs include it. Select the
  intended leaf and trace session before editing.
- Keep submission notes and research discussions free of secrets, private paths
  and unrelated session data. Do not use retired standalone Notes commands.
- Land harness changes through a feature branch and human-reviewed PR. Label
  harness PRs `yukon-unsafe` when they invalidate pending scores. Never manually
  merge Yukon submission PRs; Yukon promotes only its scored content.
