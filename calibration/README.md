# Organizer baseline calibration

`birthday_wordram.py` is a bounded, organizer-owned interpreter for a **fixed** public
instruction schedule. It independently checks the birthday baseline at small sample
sizes and exposes symbolic cost bounds. Only the standard library is used.

The model does not load or execute participant input. Its program is a literal in
trusted code, not extracted from `candidate/proof.md`. Synthetic digest callbacks are
test-only fixtures for stable sorting and final-verification branches; they are not
SHA-1 collision certificates. The interpreter's Python objects, hashlib performance,
and measured wall-clock time are not the claimed abstract word-RAM resources.

Run `python3 -m unittest tests.test_birthday_baseline` or `bash .yukon/setup.sh`.
The normal setup includes these tests, but they do not require participant submissions
to match the organizer baseline. Changes to candidate content are reviewed by the
existing intake and judge pipeline, not by executing candidate pseudocode.

The small-n interpreter refuses more than 4096 records. The `n = 2^80` resource
and success-threshold checks use exact integer/rational arithmetic; they do not attempt
the full attack, establish the SHA-1 random-function heuristic, or imply human acceptance.

`birthday_probability.py` adds exact-arithmetic checks for the proposed replacement in
`UNCONDITIONAL_BASELINE.md`. The older instruction model remains useful as a historical
accounting fixture, but its heuristic candidate is not qualified under the active
`unconditional-v1` policy. The replacement's complete sampling/three-word-record
instruction schedule has not yet been implemented.
