# Toy batch-collision method

This organizer toy example is not a SHA-256 round-reduction challenge. Its complete
target H maps a three-byte message to the first ten bits of hashlib.sha256(message).
Every library SHA-256 call is a single opaque toy hash operation; the target's
fixture label 1 denotes one such application and has no SHA-256-round meaning.

The attack samples 32 independent uniform 24-bit messages, evaluates H on each,
compares every pair, and returns a distinct-message collision if one exists.
A failed batch terminates without a witness. The claimed algorithmic success
probability per batch is at least 0.5, conditional on heuristic H1 below.

Under the toy model a hash call, 24-bit uniform draw, fixed-width comparison,
small integer operation, byte access, or output each costs one toy operation.
32 hashes, 32 draws, at most 496 pair checks and fewer than eight operations per
pair fit within 4096 operations. Store 32 three-byte messages, 32 two-byte digest
containers, fixed counters and scratch bytes; this fits within 4096 bytes. There
is no reusable preprocessing or nonuniform advice, and no external data. The
conservative submitted cost is time_log2=12, memory_log2_bytes=12, score_log2=24.

H1: For this exact map and the specified uniform input distribution, a batch of
32 messages has distinct-message collision probability at least 0.5. This is a
heuristic estimate supported by the organizer's finite experiment: 17 of 32
batches found collisions. The experiment uses the fixed Python random.Random(2026)
stream solely for reproducibility; uniform attacker randomness is the algorithm's
probability model. No claim is made that fixing a pseudorandom seed proves that
model or provides a rigorous statistical guarantee for all possible coins.

The tested and claimed target, message size, and batch size coincide; extrapolation
is from a small observed sample to the exact distribution's probability. The
observed frequency is 0.53125. A two-sided 95% Wilson interval is roughly
[0.36, 0.69], so these observations do not establish the lower bound 0.5.
The interval is supplied as an uncertainty diagnostic, not a proof certificate
or a calibrated probability that H1 is true. No exact count of the target's
preimage frequencies, full collision probability, or independent replication is
provided. A uniform-output birthday approximation gives about 0.39, so it does
not independently establish the claimed 0.5 for this fixed target either.

If H1 fails, the claimed one-batch success bound and the submitted result fail;
additional batches would change the charged time and need their own analysis.
This submission makes its score-critical uncertainty explicit and does not assert
that the sample alone discharges it to ordinary cryptanalytic standards.
