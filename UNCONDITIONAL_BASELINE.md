# Birthday search without a SHA-1 randomness assumption

Status: analytical replacement argument and exact-arithmetic regression tests; **not
yet a replacement candidate, complete instruction ledger, or qualified score**.

## Policy

The pilot now admits no unproved cryptanalytic assumptions. This supersedes the earlier
proposal to approve the provisional baseline's random-function heuristic. Comparisons
must share the concrete target, round semantics, success criterion, cost model, and
admissibility rules. Listing an assumption does not make a conditional result comparable.

The active instructions are `judge/policies/unconditional-v1.md`. The `assumptions`
field contains only unresolved premises beyond common problem definitions; aggregation
blocks a nonempty array regardless of the model's verdict. Proved lemmas and compliance
with organizer-defined models belong in `verified_steps`. A committee cannot outvote a
reported unproved premise by relaxing its voting thresholds; valid findings in partial
panels also retain this veto. The policy is loaded as
trusted instructions, not participant evidence, and hashed in the judge configuration.
The wire schema remains structurally unchanged.

A randomized algorithm defines a probability space over its own choices. This is not
an assumption that concrete SHA-1 is random. Random-bit access and its charges must
still be standardized in the common computational model before the replacement is
scored. A seeded PRNG is not automatically a substitute for independent random coins.

## Why the old algorithm must change

The current candidate enumerates fixed messages from a 96-bit nonce family. A function
with a 160-bit output could be injective on that entire family. No distribution-free
birthday guarantee follows merely by deleting the heuristic sentence.

Instead, sample inputs independently from a larger domain. A fixed function of iid
inputs has iid outputs with some induced distribution. Independence follows from the
sampling algorithm, not a cryptanalytic hypothesis. Uniformity minimizes repeated
outputs, but repeated copies of the same INPUT also repeat the output and are not
hash collisions. Their probability must be accounted for explicitly.

Uniform output draws are not synonymous with random-oracle evaluation under every
sampling scheme. Without-replacement draws from a balanced finite function have
different probabilities from independent random-oracle outputs. The construction below
uses sampling with replacement and subtracts the repeated-input event.

## Distribution-free finite-function bound

Fix any function `h: D -> {0,1}^160`, including concrete SHA-1. Let `d = |D|` and
`M = 2^160`. Draw `n` messages iid uniformly from `D`. The output probabilities are
`p_y = |h^{-1}(y)|/d`, allowing empty fibers. No uniformity or regularity is assumed.

For `n <= M`, the probability of no repeated output is `n! e_n(p_1,...,p_M)`, where
`e_n` is the elementary symmetric polynomial of degree `n`. Its maximum is

```text
n! choose(M,n)/M^n = product_{i=0}^{n-1}(1-i/M).
```

Proof of the maximum: with all other coordinates fixed, the polynomial has form
`A + (a+b)B + ab C`, with `C >= 0`. Averaging `a,b` preserves their sum and cannot
decrease the expression. On the compact probability simplex choose a maximizer
minimizing the sum of squared coordinates. If two coordinates differ, averaging either
increases the expression, contradicting maximality, or preserves it and decreases the
sum of squares, contradicting the tie-break. Thus a maximizer is uniform. For `n=1`
the result is immediate. This is a bound over all distributions, not an assumption
about which distribution concrete SHA-1 has.

Let `A` be a repeated-output event and `B` a repeated-input event. On `A` without `B`,
distinct inputs collide. The union bound gives `Pr[B] <= choose(n,2)/d`. Hence a full
scan for nontrivial matches succeeds with probability at least

```text
1 - product_{i=0}^{n-1}(1-i/M) - n(n-1)/(2d)
>= 1 - exp(-n(n-1)/(2M)) - n(n-1)/(2d).
```

Pairwise collision EVENTS are not treated as independent. The polynomial proves the
output-event bound, and a union bound handles repeated inputs. The scan must exclude
same-input matches and continue looking for a pair of distinct messages.

## Concrete parameters

Use the same 22-byte prefix followed by a **24-byte uniformly sampled nonce**, so
`d = 2^192`. Each 46-byte message still occupies one SHA-1 block after padding.
For `n = 2^80`,

```text
x = n(n-1)/(2M) = 1/2 - 2^-81 > 499/1000,
n(n-1)/(2d) < 2^-33.
```

The positive exponential series and exact rational comparisons give

```text
exp(x) > 1 + .499 + .499^2/2 + .499^3/6
       = 9865254499/6000000000,
exp(-x) < 6000000000/9865254499 < 609/1000.
```

Thus success is greater than `391/1000 - 2^-33 > 39/100`. This holds for every fixed
160-bit-output function on this domain, with probability over the algorithm's random
inputs. It requires no random-oracle or SHA-1 output-distribution assumption.

Digest plus nonce needs 44 bytes, fitting three 128-bit words (48 bytes). Two buffers
use `96 * 2^80` bytes, leaving space below `2^87` for small fixed state. This is only
a feasibility calculation: the old two-word-record instruction schedule must change.

## Implementation still required

1. Define and charge random-bit access in a common, versioned probabilistic word-RAM
   model. No uncharged exponential random-tape buffer or implicit PRNG assumption.
2. Replace enumeration with iid 192-bit sampling. Report `n` draws, at most `n` distinct
   chosen messages, and the actual random-bit budget.
3. Implement three-word records, 46-byte message construction, sorting, and distinct-input
   checks. Recompute the instruction/memory ledger and update claim/model/frontier data.
4. Extend the trusted small-n model with deterministic test tapes and duplicate-input,
   skewed-output, injective, and constant-function cases. Execute no candidate code.
5. Validate the replacement under the strict judge. Keep the old heuristic fixture as a
   negative control, not a qualified baseline. Do not reuse historical scores.

`calibration/birthday_probability.py` and its tests check small finite distributions,
enumerate toy samples, and verify the full-size rational threshold. They do not execute
the full attack, formally certify the theorem, or establish a new runtime ledger.

## References

Wiener's [Bounds on Birthday Attack Times](https://eprint.iacr.org/2005/318.pdf) discusses
random versus concrete functions and repeated-input false collisions. Bellare and
Kohno's [Hash Function Balance and Its Impact on Birthday Attacks](https://homes.cs.washington.edu/~yoshi/papers/Hash/balance.pdf)
also treats concrete-function birthday attacks. The argument above provides its own
bound and pilot parameters; neither paper validates a full HashSmash implementation.

Official [OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-engineering)
informed separating trusted application policy from untrusted evidence, versioning it
in code, and testing the change. Model, provider, reasoning, and authentication settings
were not changed.
