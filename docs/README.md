# HashSmash documentation

The supported system is the paired exploratory/rigorous frontier: 16 runnable
lanes, with 12 reserved slots awaiting exact definitions. Shell commands and
plain file paths in these guides are relative to the repository root unless a
section explicitly selects a Yukon leaf directory. Markdown links resolve from
the containing document.

## Current guides

- [Frontier lanes](./FRONTIER_LANES.md): roster, target boundaries, scoring and local commands.
- [Judge lanes](./JUDGE_LANES.md): review roles, heuristics and acceptance policies.
- [Heuristic experiments](./HEURISTIC_EXPERIMENTS.md): manifests and isolated execution.
- [Candidate qualification](./CANDIDATE_QUALIFICATION.md): package requirements and readiness sequence.
- [Yukon dev setup](./YUKON_DEV_SETUP.md): operator imports and deployment gates.
- [Yukon solver guide](./YUKON_SOLVER_GUIDE.md): leaf selection, tracing and submission workflow.
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
