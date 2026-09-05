# HashSmash documentation

The supported system is the paired exploratory/rigorous frontier: 16 runnable
lanes, with 12 reserved slots awaiting exact definitions. Shell commands and
plain file paths in current guides are relative to the repository root, which
is the single Yukon import and CLI work directory. Markdown links resolve from
the containing document. Every Yukon track ID includes its review lane.

## Current guides

- [Solver entry point](../TASK.md): the single UI reference for challenge-specific rules and deviations from the Yukon CLI skill.
- [Builder entry point](./BUILDER_GUIDE.md): harness ownership, verification, baseline authoring and deployment.
- [Frontier lanes](./FRONTIER_LANES.md): roster, target boundaries, scoring and local commands.
- [Judge lanes](./JUDGE_LANES.md): review roles, heuristics and acceptance policies.
- [Heuristic experiments](./HEURISTIC_EXPERIMENTS.md): manifests and isolated execution.
- [Candidate qualification](./CANDIDATE_QUALIFICATION.md): organizer baseline packages and live-review sequence.
- [Yukon dev setup](./YUKON_DEV_SETUP.md): operator imports and deployment gates.
- [Participant heuristic test](./PARTICIPANT_HEURISTIC_TEST.md): organizer diagnostic and its limits.
- [Frontier validation](./FRONTIER_VALIDATION.md): dated offline, Docker and live-review evidence.

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
