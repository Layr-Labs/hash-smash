# sha256-r37-exploratory: organizer draft starter

This is an incomplete draft, not an attack, qualified baseline, or score.
The claim contains nominal template values only. No result from rounds 31/32
has been transferred to this target.

The target is the complete SHA-256 hash with standard IV, ordinary padding,
round indices 0 through 36 on every padded block, standard schedule and
feed-forward, and the full 256-bit digest. The organizer selected rounds
37/38 for exploration without asserting a first-unbroken boundary.

Before setting this package to ready, replace this scaffold with a self-contained
algorithm and correctness/success argument for distinct complete messages.
Justify total computation, including preprocessing, failed trials, randomness,
message construction, memory accesses, collision checks and amplification under
collision-frontier-v5. One selected-round compression costs one unit; other
256-bit RAM primitives cost 1/2644 each. Justify peak memory and advice.
Disclose material heuristics and their support. Add certificates or declared
experiments only when they support that actual argument.

The nominal reference sha256-r37-nominal-v2 is not an established attack,
a qualified baseline, or a security bound. These placeholders cannot qualify
an import. Fresh evidence and exploratory review are required after completion.
