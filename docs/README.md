# HashSmash documentation

The local registry contains 26 runnable lanes (22 current and four historical),
with four deferred Poseidon slots. The root manifest retains eight exploratory
registrations; six are intended to compete after closing SHA-256 31/32. Shell commands and
plain file paths in current guides are relative to the repository root, which
is the single Yukon import and CLI work directory. Markdown links resolve from
the containing document. Every Yukon track ID includes its review lane.

## Current guides

- [Solver entry point](../TASK.md): the single UI reference for challenge-specific rules and deviations from the Yukon CLI skill.
- [HashSmash solver skill](../.agents/skills/hashsmash-solver/SKILL.md): practical solver workflow, target/cost checks and advisory review packets.
- [Builder entry point](./BUILDER_GUIDE.md): harness ownership, verification, baseline authoring and deployment.
- [Frontier lanes](./FRONTIER_LANES.md): roster, target boundaries, scoring and local commands.
- [Judge lanes](./JUDGE_LANES.md): review roles, heuristics and acceptance policies.
- [Heuristic experiments](./HEURISTIC_EXPERIMENTS.md): manifests and isolated execution.
- [Candidate qualification](./CANDIDATE_QUALIFICATION.md): organizer baseline packages and live-review sequence.
- [SHA-256 round migration](./SHA256_ROUND_MIGRATION.md): rounds 37/38, closed history, qualification, all-lane fingerprints and separate UI rollout.
- [Yukon production setup](./YUKON_PROD_SETUP.md): production source and rollout gates.
- [Yukon dev setup](./YUKON_DEV_SETUP.md): operator imports and deployment gates.
- [Participant heuristic test](./PARTICIPANT_HEURISTIC_TEST.md): organizer diagnostic and its limits.
- [Frontier validation](./FRONTIER_VALIDATION.md): dated offline, Docker and live-review evidence.

## Legal documents

Effective October 5, 2026:

- [HashSmash Terms of Service](./legal/TERMS_OF_SERVICE.md), including [submission licensing and Covered Data](./legal/TERMS_OF_SERVICE.md#5-intellectual-property) in Section 5.
- [HashSmash Privacy Policy](./legal/PRIVACY_POLICY.md).

## Research and context

- [Frontier research](./FRONTIER_RESEARCH.md): sources and unresolved target definitions.
- [Original HashSmash vision](./HashSmash.md): broader research goals and design discussion.
- [Historical MVP validation](./archive/MVP_VALIDATION.md): evidence from the retired pilot.
- [Historical challenge plan](./archive/YUKON_CHALLENGE_PLAN.md): original implementation and rollout design.
- [Historical multi-track plan](./archive/YUKON_MULTITRACK_PLAN.md): earlier Yukon routing investigation.
- [Unconditional birthday argument](./archive/UNCONDITIONAL_BASELINE.md): analytical context under the retired resource model.

The archived documents describe earlier behavior; their old commands and layouts
are not supported workflows. Runtime judge policies and prompts remain in
[`judge/`](../judge), and assigned lane contracts remain in [`tracks/`](../tracks).
The former [Yukon solver guide](./YUKON_SOLVER_GUIDE.md) remains as a compatibility
link to `TASK.md`; generic CLI instructions belong to the installed Yukon skill.
