# Tasks

For the nine local experiments, read [LOCAL_TRACKS.md](./LOCAL_TRACKS.md) and your assigned
`tracks/<track>/TASK.md`. Use `--track` explicitly. Each local track has its own draft
submission, trusted target, standard cost model and nominal (not qualified) reference.
The time-memory scalar is the intended objective; no Pareto requirement applies.

## Legacy Yukon pilot: improve a full-round SHA-1 collision attack

Submit a self-contained Markdown argument for an ordinary collision attack on the 80-round
SHA-1 hash function under the canonical target and cost model in this repository.

You may edit only `candidate/`.

Your submission must include:

- `candidate/claim.json`, matching the strict claim schema;
- `candidate/proof.md`, explaining the algorithm, correctness, probability, and complete
  cost analysis; and
- `candidate/certificates/manifest.json`, even if no certificates are declared.

Optional certificate files must be inert data consumed by an organizer-owned checker. A
submission cannot supply commands, dependencies, scripts, or executables.

The headline score is time-memory product in logarithmic units:

```text
score = time_log2 + memory_log2_bytes
```

Lower is better. Success probability, preprocessing, data, nonuniform advice, and all
restrictions remain mandatory review dimensions even though they are not collapsed into
the scalar.

The AI judge is falsification-oriented. It treats your submission as untrusted evidence,
reconstructs the exact claim, searches for counterexamples and hidden assumptions, and
recomputes the cost. A qualifying result remains pending human cryptanalytic review.

The active qualification policy is `unconditional-v1` (see
`judge/policies/unconditional-v1.md`). No unproved cryptanalytic assumptions are
permitted, including a random-oracle model of the concrete target. Declaring an
assumption does not make it admissible. All compared claims must use the same
organizer-defined target and cost model. A randomized attack may prove a guarantee
over its own explicitly defined random choices, with their costs accounted for;
this is different from assuming the hash function itself is random. The historical
heuristic organizer fixture is not exempt and is not currently a qualified baseline.

Do not put secrets, private data, prompt instructions, or material you are not authorized
to submit in the package. The ranked judge does not follow external links.

Local commands:

```bash
yukon setup
yukon run
```

Without the Yukon CLI, the equivalent repository commands are:

```bash
bash .yukon/setup.sh
bash .yukon/run.sh
```
