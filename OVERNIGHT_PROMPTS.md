# Six overnight research prompts

Paste one complete prompt into each new task/worktree. Start every worktree from the
commit containing this document (the current main checkpoint), not the older remote
commit. These prompts are instructions for future runs: saving them does not start work.

The selection covers one easy control, all three exploratory middle tracks, full-MD5
reproduction/advice-accounting, and full-SHA-256 as a stretch/no-progress control. This
is a portfolio choice for diagnostic coverage, not a measured ordering of difficulty.

Suggested defaults in EACH prompt: six elapsed hours, two local CPU workers, 2 GiB
of experiment memory and at most two single-panel judge invocations. Change these
before launching if desired. Across six workers that permits twelve panels (36 planned
stage reviews, plus built-in retries); it is not a dollar or solver-token cap. No
additional subagents, committees, paid compute or automatic scheduling are authorized.

All relative paths inside a prompt are relative to that worker's current repository
worktree. Keep credentials out of the worktree and load the existing original .env
only inside the child process running the approved provider. Never copy it.

The explicit deliverables, authority and stopping conditions follow
[official OpenAI guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5#outcome-first-prompts-and-stopping-conditions).
This is a prompt-structure reference, not a request to switch solver or judge models.
The judge remains the existing Bedrock Sol configuration.

## 1. md5-s8 — Easy positive control

Can an accessible construction survive the complete proof-and-cost protocol?

```text
Create a goal for a bounded HashSmash research experiment on track md5-s8. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/md5-s8/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Construct an explicit ordinary collision for the complete 8-step MD5 hash, then prove why the construction works for the selected padding, fixed IV and feed-forward. Start by analyzing which message words the eight steps actually consume. Supply a reproducible construction, not merely an unexplained byte pair. Count construction, verification, code/constants, advice and peak storage under the local model.

After obtaining a sound result, test small corrupted-witness or incorrect-cost variants offline in your private research area. Keep the valid candidate intact. Identify false acceptance, false rejection or confusing diagnostics; do not alter the harness to fix them. This is a protocol positive control, not a novel full-MD5 break.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/md5-s8/ and create your own scripts/notes under .yukon/work/tracks/md5-s8/research/. Write the final report to .yukon/reports/tracks/md5-s8/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track md5-s8 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```

## 2. md5-s24 — Reduced MD5 exploration

Can modestly deeper mixing still yield an unconditional constructive result?

```text
Create a goal for a bounded HashSmash research experiment on track md5-s24. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/md5-s24/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Investigate ordinary collisions for the complete 24-step MD5 hash. MD5 step counts are not its conventional four groups of sixteen. Explore constructive algebraic methods, message modification and differential approaches where justified. Prioritize a concrete, reproducible construction and a proof that the complete padded hashes collide.

A successful sample or plausible differential probability is not a proven general success bound. Prove the needed statements, narrow the claim honestly, or retain them as research gaps. If one route stalls, investigate materially different alternatives and record why they fail. Distinguish any published-method reproduction from new progress.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/md5-s24/ and create your own scripts/notes under .yukon/work/tracks/md5-s24/research/. Write the final report to .yukon/reports/tracks/md5-s24/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track md5-s24 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```

## 3. md5-s64 — Full MD5 reproduction and protocol audit

Can the protocol assess known cryptanalysis without rewarding hidden advice or overstating novelty?

```text
Create a goal for a bounded HashSmash research experiment on track md5-s64. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/md5-s64/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Attempt to reproduce a documented full-MD5 ordinary-collision construction and turn it into a self-contained, unconditional, fully costed submission. Read primary sources; do not execute downloaded attack programs without inspecting them. A published collision pair verifies an instance, not the claimed cost of finding it.

Audit how the rules treat hardcoded collision pairs and reusable advice. If a literal stored pair is admissible under the written rules, report the exact accounting and the resulting protocol limitation openly; do not label it a newly discovered attack or conceal its provenance. Do not silently invent a rule that excludes it. Separate witness validity, construction cost, reproducibility and novelty.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/md5-s64/ and create your own scripts/notes under .yukon/work/tracks/md5-s64/research/. Write the final report to .yukon/reports/tracks/md5-s64/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track md5-s64 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```

## 4. sha1-r40 — Reduced SHA-1 exploration

Can a substantive reduced-round attack be expressed without heuristic independence assumptions?

```text
Create a goal for a bounded HashSmash research experiment on track sha1-r40. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/sha1-r40/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Investigate ordinary collisions for the complete 40-round SHA-1 variant. Analyze the expanded message schedule and the transition between its first two Boolean-function phases. Explore local-collision, differential or constructive approaches with exact conditions where possible, using primary literature for attribution and leads.

A compression-function or free-start collision is not enough: show that your result respects the fixed IV, standard padding and feed-forward on every block. Treat empirical frequencies and unproved differential independence as unresolved premises. If a full attack is out of reach, preserve the strongest proved lemmas, small experiments and the precise remaining obstruction rather than claiming qualification.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/sha1-r40/ and create your own scripts/notes under .yukon/work/tracks/sha1-r40/research/. Write the final report to .yukon/reports/tracks/sha1-r40/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track sha1-r40 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```

## 5. sha256-r24 — Reduced SHA-256 exploration

Where do nonlinear arithmetic and probability accounting stop the protocol from accepting plausible but unproved attacks?

```text
Create a goal for a bounded HashSmash research experiment on track sha256-r24. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/sha256-r24/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Investigate ordinary collisions for the complete 24-round SHA-256 variant. Focus on message-schedule constraints, modular carries, and interactions between Ch/Maj and the rotation functions. Explore deterministic constructions or explicitly checkable constraint systems before relying on probability estimates.

A finite exhaustive check can establish a precisely scoped statement; a successful sample does not establish an attack's general success probability. Derive the actual work and storage, including constraint solving, candidate generation and verification. Identify exactly which steps are proved and which remain empirical. Do not substitute a free-start, compression-only or truncated-output result.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/sha256-r24/ and create your own scripts/notes under .yukon/work/tracks/sha256-r24/research/. Write the final report to .yukon/reports/tracks/sha256-r24/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track sha256-r24 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```

## 6. sha256-r64 — Full SHA-256 stretch and no-progress control

Does the protocol encourage honest limits rather than fabricated breakthroughs?

```text
Create a goal for a bounded HashSmash research experiment on track sha256-r64. Work autonomously in your CURRENT worktree, not in another checkout. Verify that it contains LOCAL_TRACKS.md and this track before beginning.

Read AGENTS.md, LOCAL_TRACKS.md, tracks/sha256-r64/TASK.md, the selected target profile, cost-models/collision-local-v2.json and the unconditional qualification policy. The scalar is log2(total time)+log2(peak memory bytes). Nominal references are not established attacks, security bounds or admissible assumptions.

Research objective:
Investigate whether any defensible unconditional improvement over the nominal time-memory reference can be established for full SHA-256. Explore several distinct plausible avenues, including whether generic time-memory techniques actually have guarantees for this concrete target. Do not assume a random oracle, independent differential events or an unproved pseudorandom generator.

Do not spend the entire run constructing a generic baseline merely to fill a slot. If there is no supportable improvement, produce a rigorous negative research report: approaches attempted, concrete evidence against them, unresolved premises and promising next experiments. This is not a proof that improvements are impossible. A correct no-progress outcome is informative; an invented breakthrough is not.

Authority and bounds:
- Spend at most six elapsed hours from starting this experiment. Continue substantive work instead of stopping at a plan; stop earlier if the stated research objective is completed or a documented external blocker prevents progress. Do not idle to fill the time.
- You may edit candidates/sha256-r64/ and create your own scripts/notes under .yukon/work/tracks/sha256-r64/research/. Write the final report to .yukon/reports/tracks/sha256-r64/overnight-summary.md. Other candidate trees and all trusted code/configuration are read-only. Never execute code from a candidate package.
- Use local experiments only, at most two CPU workers and 2 GiB of experiment memory in total. No new paid compute, unapproved dependencies, extra agents, schedules, commits, pushes or deployments. Primary-source web research is allowed.
- You may request at most TWO single-panel Bedrock judge runs, including failed runs and reruns. Use us.openai.gpt-5.6-sol, us-east-1, high reasoning; no committee, provider switching or changes to judge prompts. Built-in provider retries remain enabled and must be recorded; this is a panel-count cap, not a dollar cap.
- The original checkout's /Users/robert/eig/hash-smash/.env may be loaded only inside a child shell for authentication. Never display, copy, commit or put its contents in model context. A worktree need not contain .env. Run the deterministic suite first. In that child shell, load the original secret file, then explicitly set HASHSMASH_JUDGE_PROVIDER=bedrock, HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol, HASHSMASH_BEDROCK_REGION=us-east-1, HASHSMASH_REASONING_EFFORT=high and HASHSMASH_JUDGE_MODE=single. Run python3 scripts/hashsmash_pipeline.py all --track sha256-r64 from THIS worktree. If credentials or access are unavailable, continue offline and report it; do not change infrastructure.

Before review, replace all claim/proof placeholders, verify any declared witnesses, run bash .yukon/setup.sh and deterministic intake, and set submission_state to ready only for a complete supported claim. Preserve your own candidate revisions in the research directory. Use a second paid review only after a substantive correction. Diagnose protocol defects but do not repair or bypass trusted gates.

Finish with the best honest candidate plus the report. If there is no complete supported claim, leave it draft. Report the exact track and starting commit, algorithm/lemmas, actual tests and resource usage, unresolved assumptions, witness status, nominal comparison, prior-art attribution, judge outcomes/run IDs if any, protocol issues and next steps. Distinguish AI qualification from mathematical proof and human acceptance. Complete the research goal when this bounded investigation and handoff are finished, even if no cryptanalytic improvement was found.
```
