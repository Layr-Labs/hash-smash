# SHA-256 first 32 rounds, grouped early abort birthday search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately and does not enter the scalar.

This package is bound to `sha256-r32-exploratory`, target profile
`sha256-r32-prefix-v1` and cost model `collision-frontier-v5`. It describes a
classical probabilistic birthday search over `q = 2^128` single block messages. It
evaluates the 32 round hash only up to round 30, shares the early rounds across groups
of `2^24` messages, and confirms candidate pairs with whole compressions. The worst case
charged time is below `2^126.663` target compressions, the address span is about `2^153`
bytes, and the success probability is above `0.3923` under the heuristics `H1` and `H2`.
The claimed success probability is `0.39`. No weakness of SHA-256 is used. The saving over
one compression per message comes from not recomputing shared work, and it is a
constant factor accounting gain.

The identifier `sha256-r32-nominal-v2` names an organizer display reference. It is not an
established attack, a qualified baseline or a security bound. This package does not
claim to beat the nominal `128` by cryptanalysis. Its scalar is below `128` only because
each message costs about `0.396` of a compression in the model's operation pricing.
Setting `submission_state` to `ready` requests review. It is not a claim of qualification.

## 1. Exact target and message encoding

Every message has exactly 55 bytes (440 bits). FIPS 180-4 padding gives one block,
`m || 0x80 || BE64(440)`, so the complete hash is one reduced compression
`C32(IV, B)` with the fixed IV, rounds 0 through 31 and the full feed-forward. The digest
is all eight output words in standard order, big endian, with no truncation.

A message is `W0 || ... || W12 || y`, where `W0..W12` are the 13 big endian 32-bit words
of a 416 bit group prefix and `y` is a 24 bit value written as three bytes. The block
words are `W0..W12`, `W13 = (y << 8) | 0x80`, `W14 = 0` and `W15 = 440`. The map from
(prefix, `y`) to messages is a bijection onto all `2^440` 55-byte strings.

`C32` is the profile's reduced compression. For `t = 16..31`,
`W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2])`. Steps `t = 0..31` start from
`IV` with the standard `Sigma0, Sigma1, Ch, Maj`, constants `K[t]` at their original
indices and additions modulo `2^32`. The result is `IV` plus the working state, word by
word. Write `A_t` and `E_t` for the new `a` and `e` words after step `t`. After step 30 the
state is `(A30, A29, A28, A27, E30, E29, E28, E27)`, and the digest words are
`H0 = IV0 + A31`, `H1 = IV1 + A30`, `H2 = IV2 + A29`, `H3 = IV3 + A28`,
`H4 = IV4 + E31`, `H5 = IV5 + E30`, `H6 = IV6 + E29`, `H7 = IV7 + E28`.

## 2. The grouped evaluator

Equal digests imply equal `H1, H2, H3, H5, H6, H7`, hence equal
`key = (A30, A29, A28, E30, E29, E28)` (192 bits), which is available after step 30. The
evaluator therefore stops after step 30 and never computes step 31, `W31` or the final
feed-forward. A key match is only a candidate and is confirmed by two whole compressions.

**Group constants.** Within a group, `W0..W12` are fixed. Steps 0 through 12 read only
those words, so the state after step 12 is a group constant. Of the schedule words needed
through step 30, the words `W16, W17, W18, W19, W21, W23, W25` do not depend on `y`. The
words `W20, W22, W24, W26, W27, W28, W29, W30` do. Each of those keeps its `y`
independent summands pre-added per group:

```
W20 = P20 + W13                       P20 = W4 + sigma0(W5) + sigma1(W18)
W22 = P22 + sigma1(W20)               P22 = W6 + sigma0(W7) + W15
W24 = P24 + sigma1(W22)               P24 = W8 + sigma0(W9) + W17
W26 = P26 + sigma1(W24)               P26 = W10 + sigma0(W11) + W19
W27 = P27 + W20                       P27 = W11 + sigma0(W12) + sigma1(W25)
W28 = P28 + sigma0(W13) + sigma1(W26) P28 = W12 + W21
W29 = W13 + W22 + sigma1(W27)         (W14 = 0 so sigma0(W14) = 0)
W30 = P30 + sigma1(W28)               P30 = sigma0(W15) + W23
```

Steps 14 to 19, 21, 23 and 25 add the constants `K[t] + W[t]`, computed once per group.

**Per message.** Steps 13 through 30 are run on full words with the dependent schedule
words above. All values are 256-bit words, and `mask` means `and 0xffffffff`. The
evaluator below is the arithmetic of `experiments/grouped_slice.py`, whose source is
supplied and was checked as follows. On 2000 random messages the six key words, added to
`IV`, agreed with the digest words `H1, H2, H3, H5, H6, H7` of
`verifier/hash_functions.py:digest(m, "sha256", 32)`. I also ran an operation counting
twin of the same arithmetic and asserted exact agreement on 1500 further evaluations.
That twin, not the experiment file, produced the counts in Section 6.

## 3. Algorithm and storage

Let `q = 2^128`, `N = 2^256`, `s = 148` and `GROUPS = 2^104`.

* The sparse table `S` has one word per slot. Slot `b` lives at byte address `32 b` for
  `b < 2^148`. **No cell of `S` is ever initialised.** The algorithm is correct for any
  initial memory content. The slot of a key is its top 148 bits, `key >> 44`.
* The dense array `D` starts at byte address `Db = 2^153`. Record `i`, where
  `i = g * 2^24 + y`, occupies four words at `Db + 128 i`, holding
  `(key, u, v, (y << 128) | nxt)`. `NIL = 2^255`. The group prefix is rebuilt from `u`
  and the top 160 bits of `v`.

```
steps = 0 ; confirms = 0
for g = 0 .. GROUPS-1:
    u = Rand() ; v = Rand()                    # fresh independent words
    prefix = u || top160(v) ; set up the group constants of Section 2
    for y = 0 .. 2^24 - 1:
        i = g * 2^24 + y
        key = grouped evaluator (prefix, y)    # Section 2, rounds up to 30
        slot = key >> 44 ; a = 32 * slot
        x = S[a]                               # arbitrary garbage possible
        nxt = NIL
        if x < i and (D[x].key >> 44) == slot: # x is a real earlier record in this slot
            nxt = x ; cur = x
            loop:
                steps += 1 ; if steps > 2^120: halt FAIL
                if D[cur].key == key:
                    confirms += 1 ; if confirms > 2^90: halt FAIL
                    rebuild both messages, hash both with fresh C32 calls
                    if messages differ and complete digests are equal: return them
                if D[cur].nxt == NIL: break
                cur = D[cur].nxt
        D[i] = (key, u, v, (y << 128) | nxt)
        S[a] = i
halt FAIL
```

The loops are iterative and run once, with no restarts. Counters and addresses are below
`2^256`. Randomness is retained only inside records.

## 4. Correctness

**Claim A.** For every initial content of `S`, chains partition processed messages by
slot, newest first, and no garbage cell is ever dereferenced.

*Proof.* Induct on the number of processed messages. Every insertion writes `S[a] = i`.
If an earlier message has this slot, the latest one was written to `S[a]`, so `x < i` and
the stored key of `D[x]` has our slot, and `nxt = x` is the previous latest. If no
earlier message has this slot, `S[a]` is untouched garbage. Either `x >= i` and the first
test fails, or `x < i` names a real record whose true slot differs from ours, because no
earlier message has our slot, so the second test fails. In both cases `nxt = NIL`. `D[x]`
is read only after `x < i`. ∎

**Claim B.** If `steps` and `confirms` stay within their caps, then whenever two distinct
processed messages have equal digests the algorithm returns a verified collision.

*Proof.* Equal digests give equal keys and equal slots. By Claim A, when the later
message is processed the earlier one lies on its chain, and the test `D[cur].key == key`
fires there. The confirmation hashes the two stored messages with whole `C32` calls and
returns only if they are distinct with equal complete digests. A return is therefore always
a valid collision, and a non-return on a digest equal pair is impossible within the caps. ∎

A hit with equal messages (two groups with identical prefixes and equal `y`) is skipped by
the "messages differ" test. Its probability is at most `2^-208` over the choice of groups.

## 5. Success probability

Let `E` be the event that two distinct processed messages have equal complete digests.
Messages in one group share a prefix, and consecutive `y` are not independent samples, so
the independence argument of a plain birthday search does not apply. I therefore declare
two heuristics and say exactly what each is used for.

`H2` (counting). The number of equal-digest pairs among the `q` grouped messages has the
distribution of the uniform birthday count. In particular, `Pr[E] >= 1 - exp(-q(q-1)/(2N))`
up to an additive `2^-12`. With `q = 2^128` the exponent is `1/2 - 2^-129`, and
`exp(-1/2) < 0.60660`, so `Pr[E] > 0.3933 - 2^-12 > 0.3930`.

`H1` (table load). For any two distinct messages the algorithm can produce, the
probability over the random group prefixes that their keys have equal 148 bit slots is at
most `8 * 2^-148`. Then by linearity of expectation (no independence needed)
`E[steps] <= binom(q,2) * 8 * 2^-148 < 2^110`, so `Pr[steps > 2^120] <= 2^-10` by Markov.

The false candidate count is the number of pairs with equal keys, which has expectation
about `binom(q,2) 2^-192 < 2^63` under the same uniformity. By Markov
`Pr[confirms > 2^90] <= 2^-27`.

By Claim B, `Pr[success] >= Pr[E] - 2^-10 - 2^-27 - 2^-208 > 0.3930 - 0.00098 - 2^-27 > 0.3920`.
The claim of `0.39` keeps a margin of about `0.002`. This is the success event of the fixed
algorithm under its fresh coins. It is not a confidence in `H1` or `H2`.

## 6. Charged time

One `C32` call costs one unit and every other primitive costs `1/2224`. This section uses
the same pricing style as the reference constant `2224`, which counts each addition,
logical operation, shift and mask on a data word once. In addition, every load, store,
comparison, branch and address computation is charged one primitive, and the group
constants are reloaded for every message instead of being kept in registers. Instruction
fetch is not charged because the model lists no such primitive. Section 8 gives the
sensitivity to this choice.

**Evaluator, per message (782 operations).** A reduced word rotation costs 3 operations
(two shifts and an or), and a `Sigma` or `sigma` function masks once after its xors.
A step costs: `Sigma1(e)` 12, `Ch = g xor (e and (f xor g))` 3, adding `h`, `Sigma1`, `Ch`
and `K+W` 3, `Sigma0(a)` 12, `Maj = b xor ((a xor b) and (b xor c))` 3, `T2` 1,
new `a` 2 and new `e` 2 (add and mask). That is 38 per step, plus 1 for `K[t] + W[t]`
when `W[t]` depends on `y`. Steps 13 through 30 are 18 steps, 684 operations, plus 9
dependent `K+W` additions (steps 13, 20, 22, 24, 26, 27, 28, 29, 30), 693 in all. Seven
`sigma` evaluations on dependent words (`sigma1` of `W20, W22, W24, W26, W27, W28` and
`sigma0` of `W13`) cost 10 each, 70. The dependent schedule additions and masks cost 19.
Total 693 + 70 + 19 = 782.

| Part per message | Operations |
| --- | ---: |
| grouped evaluator, rounds 13 to 30 with dependent schedule | 782 |
| form `W13 = (y << 8) \| 0x80` | 2 |
| pack the six key words into one 192 bit key (5 shifts, 5 ors) | 10 |
| reload group constants (8 state words, 8 `P` words, 9 `K+W` words, 9 `K` words), budget | 40 |
| table step, slot, address, load, compares, branches, stale cell check | 11 |
| record stores, pointer updates, loop control (including `(y << 128) \| nxt`) | 14 |
| **counted total** | **859** |

The bound uses `880` operations per message, which keeps 21 spare operations.

**Other work.** Per group: two random words, deriving 13 words, steps 0 through 12 and the
group schedule constants, at most `8192` operations, which is `GROUPS * 8192 / 2224 <
2^91` units in total. A chain step is 11 operations (record address 2, load and compare
the key 3, load `nxt`, compare, branch 3, counter and cap 3) and is charged `16`, for at
most `2^120` steps. Each confirmation is two `C32` calls plus at most `4096` operations,
for at most `2^90` confirmations. Initial constants cost at most `2^20` operations.

**Totals, on every choice of coins.**

```
T <= q * 880/2224 + 16 * 2^120/2224 + 2^104 * 8192/2224
     + 2^90 * (2 + 4096/2224) + 2^20/2224
  = 0.39571... * q   <  2^126.663
```

I computed this in exact rational arithmetic (`T / q = 0.395712`, `log2 T = 126.66252`).
All sampling, randomness, lookup, failed work and confirmation is inside `T` since the run
is one finite pass. The submitted `time_log2 = 126.67` is a worst case bound, not an
expectation. Preprocessing is the `2^20` operation setup, below `2^9` units.

## 7. Memory, preprocessing and advice

`S` spans `[0, 2^153)` bytes and `D` spans `q * 128 = 2^135` bytes. Code and scratch fit in
`2^21` bytes. The address span is below `2^153.01` bytes, so `memory_log2_bytes = 153.1`.
At most `2^128` cells of `S` are written, so touched memory is about `2^135.2` bytes. The
model reports memory without scoring it. `preprocessing_log2 = 9` is `2^20 / 2224` rounded
up. No nonuniform advice is used and the schema value `0` means a bound of one byte.

## 8. Sensitivity, heuristics and limitations

**Accounting sensitivity.** The grouped design wins only because each message costs
`859` data path operations against `2224` for a whole compression, under a pricing that
charges one primitive per operation. Keeping group constants in registers and using one
primitive per operation gives `log2(782/2224) + 128 = 126.49` for the core alone. If every
logical instruction were instead charged 8 primitives (two operand loads, the operation, a
store and four instruction fetches), the grouped evaluator would cost about `3` units and
a plain single block search with one whole compression per message, near `128.4`, would be
cheaper. The claim therefore rests on the reference normalisation convention that the
organizer's own `C = 2224` uses.

**H1 and H2 evidence.** The slot is the top 148 bits of the 192 bit key, which is a
function of `H1, H2, H3` and the upper part of `H5` after 32 rounds. The declared
experiments run the exact grouped evaluator at reduced scale. Each trial draws 512
messages and asks for a pair agreeing on an 18 bit slice, the analogue of
`q^2 / 2^257 = 1/2` (model success `0.3935`). `grouped-spread` uses 16 groups of 32
consecutive `y` values and a mask of 6 bits in each of `H1, H2, H3`. `grouped-single` uses
one group of 512 consecutive `y` values and the top 18 bits of `H5`. A local replication
with 4096 trials each (my own seeds, not organizer evidence) gave `1579` and `1643`
successes against a model value of `1610.0` (`z = -0.99` and `+1.05`). The host recomputes
the reference digest of every returned pair.

Limits. The experiments use 18 bit slices, 512 messages, seed expanded group prefixes and
consecutive `y`, and extrapolate to 148 bit slots at `2^128` messages and `2^24` messages
per group. The runner gives no iid interval. They test the pair collision rate of
`H1, H2, H3, H5`, not `H6, H7` and the interaction of all six words. If `H2` fails, the
success probability changes in either direction. If `H1` fails by a larger factor, the
chain cap can be exceeded. Neither can create an invalid returned pair.

## 9. Credit and status

The single block layout, grouping by `W13`, early abort after step 30 and the
uninitialised sparse set table follow ideas in other solvers' public notes on this track,
notably jaazinn's 126.695 entry. This package differs in an operation count produced by
an exact instrumented evaluator, in chaining so that no collision is displaced, in an
explicit worst case cap on chain work and confirmations, and in declaring both
heuristics. It inherits no earlier review. This is an analytic candidate with no full
scale run.
