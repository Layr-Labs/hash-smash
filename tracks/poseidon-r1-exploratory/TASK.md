# poseidon-r1-exploratory

Read the repository-root [solver task](../../TASK.md) first. It contains the shared
HashSmash rules, required reading, and differences from the generic Yukon workflow.
This file supplies only the assigned target and lane contract.

| Field | Assignment |
| --- | --- |
| Organizer track ID | `poseidon-r1-exploratory` |
| Editable directory | `lanes/exploratory/candidates/poseidon-r1/` |
| Exact target profile | [poseidon-r1-prefix-v1](../../target-profiles/poseidon-r1-prefix-v1.json) |
| Review lane | `exploratory` |
| Qualifying AI review status | `plausible_not_refuted` |
| Nominal reference | 127; not an established attack, qualified baseline, or security bound |
| Reference operation cost | `C = 27` |

Use `python3 scripts/local_tracks.py show poseidon-r1-exploratory` from the repository
root to inspect the trusted profile, cost model, and reference. Keep the selected
track ID and candidate lane consistent; the other round has its own package.

## The target

The deployed Zcash Orchard `PoseidonHash`, parameter set `P128Pow5T3`, over the
Pallas base field. Width 3 with rate 2 and capacity 1, S-box `x^5`, and a deployed
schedule of `R_F = 8` full rounds and `R_P = 56` partial rounds, so 64 rounds in
total. Rounds 0 to 3 and 60 to 63 are full; rounds 4 to 59 are partial.

This track is the prefix reduction to **round 0 only**, which is a full round: add
the deployed round constants of row 0 to all three state elements, apply `x^5` to
all three, then multiply by the deployed MDS matrix. Round `i` always uses deployed
constant row `i`, and the MDS matrix is never regenerated for a reduced instance.

Hashing uses the deployed `ConstantLength<2>` domain. The initial state is
`[m0, m1, 2^65]`, where the capacity element is `L * 2^64` with `L = 2`. One
permutation is applied and the output is state element 0. No padding element is
absorbed at this length.

## Message domain

A message is **exactly 64 bytes**: two 32-byte little-endian Pallas base field
elements, each **strictly less than**
`p = 0x40000000000000000000000000000000224698fc094cf91b992d30ed00000001`.

Non-canonical encodings are rejected. An element encoded as `x + p` is not a valid
message even though it is congruent to `x`, and any length other than 64 bytes is
rejected. Both messages in a collision must be canonical, and the verifier reports
a witness outside this domain as a failed certificate. This rule is
security-critical: without it, `x` and `x + p` would encode the same field element
and hand out a collision for free.

The digest is state element 0 as 32 little-endian bytes. The output space is the
field order, about `2^254`, not `2^256`, so the generic collision exponent is about
127 rather than 128.

## Open items

The cost model records that a field-specific model is required before Poseidon
activation. `C = 27` counts one modular addition and one modular multiplication as
one primitive operation each, which is a proposal for the organizers rather than
settled policy. Treat both the cost rule and the round pair as provisional.

Follow [TASK.md's evaluation guidance](../../TASK.md#hashsmash-evaluation-differs-from-the-generic-solve-loop)
for setup, mechanical checks, and remote judging. Agents explicitly assigned
organizer baseline preparation instead follow the
[builder baseline workflow](../../docs/BUILDER_GUIDE.md#baseline-authoring-and-local-review)
while preserving this same candidate boundary and scientific contract.

The organizer selected rounds 1/2 for exploration; no first-unbroken boundary or
qualified attack is asserted. This pair has exploratory lanes only. The track is
defined and locally runnable but is not registered in Yukon, because registration
also requires an admissible baseline for the lane.
