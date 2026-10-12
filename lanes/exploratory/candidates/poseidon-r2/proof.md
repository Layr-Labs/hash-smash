# poseidon-r2-exploratory: organizer draft starter

This is an incomplete draft, not an attack, qualified baseline, or score.
The claim contains nominal template values only. No result from any other
target, round count or Poseidon instance has been transferred here, and the
single-round package cannot supply this one's claims, evidence or scores.

The target is the complete Zcash Orchard PoseidonHash, the deployed
P128Pow5T3 instance over the Pallas base field, reduced to the first two
rounds of its deployed 64-round schedule. Width 3 with rate 2 and capacity 1,
S-box x^5, deployed R_F=8 and R_P=56. Rounds 0 and 1 are both full rounds:
each adds the deployed round constants of its own row to all three state
elements, applies x^5 to all three, then multiplies by the deployed MDS
matrix. Constants are never regenerated for a reduced instance.

A message is exactly 64 bytes holding two 32-byte little-endian field
elements, each strictly less than p. Non-canonical encodings are rejected, so
an element encoded as x + p is not a valid message even though it is
congruent to x; the two messages in a collision must both be canonical. The
digest is state element 0 as 32 little-endian bytes.

The organizer selected rounds 1/2 for exploration without asserting a
first-unbroken boundary. These are deliberately easy starting rounds.

Before setting this package to ready, replace this scaffold with a
self-contained algorithm and correctness/success argument for distinct
complete messages. Justify total computation, including preprocessing, failed
trials, randomness, message construction, memory accesses, collision checks
and amplification under collision-frontier-v5. One selected-round permutation
costs one unit; other primitives cost 1/C each, with C = 54 for this target.
Justify peak memory and advice. Disclose material heuristics and their
support. Add certificates or declared experiments only when they support that
actual argument.

Note two open items for this family. The cost model states that a
field-specific model is required before Poseidon activation, and C = 54 counts
one modular addition and one modular multiplication as one primitive
operation each, which is a proposal rather than settled policy. The nominal
reference poseidon-r2-nominal-v2 is 127 rather than the 128 used for binary
256-bit targets, because the output space is the field order of about 2^254
rather than the full 32-byte encoding.

The nominal reference is not an established attack, a qualified baseline, or a
security bound. These placeholders cannot qualify an import. Fresh evidence
and exploratory review are required after completion.
