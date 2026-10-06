# A distribution-free birthday bound for the fixed-IV 31-round target

This package targets `sha256-r31-exploratory`, target profile `sha256-r31-prefix-v1`, and the ordinary collision cost model `collision-frontier-v5`. It submits a complete analytic algorithm with no differential heuristic, external advice, stored witness, or executed `2^128`-scale experiment. The required `baseline_improved` identifier in the claim is the organizer's nominal reference identifier; it is not an established attack or a proof that this submission improves that reference.

## Exact messages and target

Let `q = 255*2^120 = (255/256)*2^128`. For each `i=0,...,q-1`, draw **two fresh independent uniform 256-bit RAM words** `X_i,Y_i` and form the 40-byte complete message `m_i = BE_32(X_i) || BE_8(Y_i mod 2^64)`. The `m_i` are independent uniform elements of a domain of size `D=2^320`. FIPS padding makes exactly one 64-byte block: the 40 message bytes, byte `80`, fifteen zero bytes, and the big-endian 64-bit length `320`. Hash this block from the standard SHA-256 IV with the original schedule and constants, executing exactly indices 0 through 30 and adding all eight incoming chaining words as feed-forward. Store the **full 256-bit** output, not a prefix. This is one selected-target compression per sample. The algorithm compares complete target hashes of distinct complete messages.

## Complete algorithm

Store each input's `X_i` and low 64 bits of `Y_i` in two 256-bit words of array `M`. Store `(digest_i,i)` in two words of array `R`; allocate another two-word-per-record array `R'` and a dense `B=2^128`-word counter array `C`. Ordinary uninitialized `M/R/R'` storage is written before reading; `C` is explicitly initialized on each pass.

Perform two **stable LSD counting-sort passes** on `R`, first by digest bits 0..127, then bits 128..255. In each pass, zero every `C` word, histogram all `q` records by that 128-bit limb, replace bucket counts with cumulative *word* offsets into the destination record array, then scatter records in original order while advancing each bucket cursor by two words. Swap the source and destination arrays between passes. The complete digest is now sorted. Scan adjacent equal digests; when two adjacent messages differ, independently rehash both complete messages from the fixed IV and return the pair only if the 256-bit outputs agree. A group of equal digests containing at least two distinct messages always has an adjacent transition between distinct messages, so the scan detects any ordinary collision among the samples. On failure it completes the entire scan and returns FAIL. No restart or early success assumption is needed for the time bound.

## Worst-case word-RAM work and memory

The model charges one target compression per one-block message and one unit per 2140 ordinary 256-bit RAM operations. Loads, stores, additions, shifts, bitwise operations, comparisons, branches, and independent random-word draws are counted. Pointers and counts fit in one 256-bit word. Fixed code and constants use at most `2^24` ordinary operations. The following ceilings include loop control, indexing, padding, randomness, and collision checks:

| Work | Ordinary operations |
| --- | ---: |
| Form, hash-interface and store one message/record | at most 32 per sample |
| Histogram one record | at most 12 per pass |
| Stable scatter one record | at most 20 per pass |
| Adjacent-digest and distinct-input scan | at most 32 per sample |
| Zero and prefix each counter array | at most 16 per bucket per pass |

For zeroing, a bucket needs a zero store, pointer increment, end comparison and branch (four operations). In the prefix sweep, load the old count, store the old running word offset as the cursor, double the count by a shift, add it to the running offset, increment the pointer, compare, and branch (seven operations). Sixteen covers those loops and setup slack. A histogram reads the record and bucket, extracts the limb with shift/mask, increments and stores the count, advances its pointer and tests the loop, within twelve. A scatter reads the two record words, extracts the limb, reads and updates its bucket cursor, writes both destination words, advances input/output pointers and tests the loop, within twenty. The thirty-two-operation input and final-scan ceilings leave extra room for byte/word packing, addresses and conditional checks. Up to two final independent verification compressions are charged even if no collision is found.

Thus on **every** coin outcome, including duplicate inputs, failed samples, sorting and verification,

```text
W <= [32+2(12+20)+32]q + 2(16B) + 2^24 = 128q+32B+2^24;
T <= q+2+W/2140 < 2^128.098456 < 2^128.11.
```

The three two-word-per-record arrays use `6q` RAM words, and `C` uses `B` words. With `q=255*2^120` and 32 bytes per word, even adding `2^24` scratch bytes gives `32(6q+B)+2^24 = 223.25*2^128+2^24 < 2^136` bytes. The largest address is below `7*2^128`, and each bucket cursor below `2q`; both fit one word. This is an astronomical theoretical memory bound, honestly reported under a policy that scores time and reviews memory separately.

## Success for any fixed target mapping

Write `p_y` for the digest probability of each output value when the input is uniform over the 40-byte domain. For any fixed function with at most `R=2^256` outputs, the probability of all `q` sampled digests being distinct is `q! e_q(p)`. Pairwise averaging unequal output probabilities cannot decrease this elementary symmetric polynomial, so its maximum occurs at the uniform distribution over `R` outputs. Therefore

```text
Pr[some equal digest] >= 1-(R)_q/R^q
                       >= 1-exp[-q(q-1)/(2R)].
Pr[some repeated input] <= q(q-1)/(2D).
Pr[ordinary collision] >= 1-exp[-q(q-1)/2^257]-q(q-1)/2^321
                        > 0.3911000919602862 > 0.39.
```

The repeated-input subtraction prevents a duplicate sample from masquerading as a collision; the final distinct-message test enforces it. This proof needs no random-oracle premise or assertion that reduced-round SHA-256 outputs are uniform. The random draws are fresh independent algorithmic coins, not a deterministic seed expansion. The declared success probability is the conservative `0.39`, and the `heuristics` list is empty.

## Scope and checks

This construction is a theoretical upper bound for the selected 31-round target, not an executed collision search and not an attack on full 64-round SHA-256. The numerical success and work expressions were independently recomputed. `python3 scripts/local_tracks.py check sha256-r31-exploratory` verifies schema consistency; it does not prove the probability argument, certify a cost bound, or replace AI and human review. AI screening, human acceptance and promotion are separate outcomes.
