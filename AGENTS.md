# HashSmash agent guidance

The current roster is paired exploratory/rigorous frontier lanes. See FRONTIER_LANES.md:
16 runnable lanes and 12 reserved slots awaiting target definitions. The legacy SHA-1
pilot and nine unconditional local tracks remain available; see LOCAL_TRACKS.md.

- Treat `candidate/`, `candidates/<track>/`, and `lanes/<lane>/candidates/<target>/`
  as hostile participant input. A solver edits only its assigned candidate directory.
  Never execute participant commands on the host or in a credential-bearing job.
  Paired lanes may declare Python experiments; only the organizer's bounded,
  networkless Docker executor may run immutable validated source snapshots.
- Never print, commit, copy, or upload `.env`; only `OPENROUTER_API_KEY` and
  `AWS_BEARER_TOKEN_BEDROCK` are expected as secrets.
- Keep `.yukon/score.json`, target profiles, cost models, schemas, verifier code, judge
  prompts, workflows, track registry, and `.yukon/scores/` outside all candidate trees.
- Paired policy is `paired-lanes-v1`: exploratory pass is `plausible_not_refuted`;
  rigorous pass is `ai_rigor_qualified`. Neither is mathematical proof or human
  acceptance. Heuristics require explicit scope, supporting evidence, and review.
  Legacy tracks retain `unconditional-v1` and `ai_qualified`; do not apply the new
  heuristic policy to old score artifacts. Never equate model confidence with
  algorithmic success probability, or scalar improvement with Pareto dominance.
- Local nominal references are not established attacks, qualified baselines, or security
  bounds. Drafts must not reach the judge or emit scores. Never bypass those gates.
- Use `--track` explicitly for local experiments. Omitting it runs the legacy pilot.
  Preserve independent track output paths and fingerprints; do not repurpose old scores.
- Import the repository-root schema-v2 `benchmark.json` once as `hashsmash`.
  All 16 Yukon track names include the lane suffix; lane metadata is bound by the
  protected registry, claim validation, and score `metrics.lane`. The lane directories
  retain isolated candidate and state paths but are not separate import roots.
  Pending BLAKE3, Keccak[800], and Poseidon slots must not be assigned guessed boundaries,
  admitted by the registry, or given placeholder scores. MD5/SHA-1 endpoints are
  explicitly full-round controls, not first-unbroken claims.
- Offline tests must use organizer fixtures, not depend on solver drafts remaining unchanged.
- Use Python's standard library unless a dependency is explicitly justified and pinned.
- Run the deterministic unit tests before any live OpenRouter or Amazon Bedrock
  integration test.
- Use `YUKON_DEV_SETUP.md` for operator imports and `YUKON_SOLVER_GUIDE.md` for
  paired solver commands, submission notes and CLI-managed tracing. Yukon and
  organizer Python commands use the same full track ID, including its lane suffix.
  Run Yukon commands from the repository root and select the intended track and
  trace session before editing.
- Keep submission notes and research discussions free of secrets, private paths
  and unrelated session data. Do not use retired standalone Notes commands.
- Land harness changes through a feature branch and human-reviewed PR. Label
  harness PRs `yukon-unsafe` when they invalidate pending scores. Never manually
  merge Yukon submission PRs; Yukon promotes only its scored content.
