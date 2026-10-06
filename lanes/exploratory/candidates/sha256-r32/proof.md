# SHA-256 first 32 rounds, single block birthday search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported
separately and does not enter the scalar.

This package is bound to `sha256-r32-exploratory`, target profile
`sha256-r32-prefix-v1` and cost model `collision-frontier-v5`. It describes a
classical probabilistic birthday search with worst case charged time below
`2^128.397` target compressions, an address span of about `2^153` bytes, and an
algorithmic success probability above `0.3923`. The claimed success probability
is `0.39`. No cryptanalytic weakness of SHA-256 is used or claimed. The gain over
the organizer's sort based placeholder (`136`) is constant factor accounting only.

The identifier `sha256-r32-nominal-v2` names an organizer display reference. It is
not an established attack, a qualified baseline or a security bound. This package
does not claim to beat the nominal value `128`, and its scalar is above it.
Setting `submission_state` to `ready` requests review. It is not a claim of
qualification.

## 1. Exact target and message encoding

Every sampled message has exactly 55 bytes (440 bits), which is a valid input in the
profile's message domain. FIPS 180-4 padding appends `0x80`, then zero bytes up to
56 modulo 64, then the 64-bit big endian length. For 55 bytes this gives exactly one
64-byte block, `m || 0x80 || BE64(440)`. There is no second block. The complete hash
is therefore one reduced compression `C32(IV, B)` with the fixed IV, rounds 0
through 31 and the full feed-forward. The digest is all eight output words in
standard order, big endian, with no truncation.

A sample is a pair of 256-bit words `(u, v)`. Its message is
`BE256(u) || BE184(v >> 72)`, where `BE184` is the 23 byte big endian encoding of the
top 184 bits of `v`. The 72 low bits of `v` are discarded. The map from `(u, v >> 72)`
to messages is a bijection onto all `2^440` 55-byte strings. The block words are

```
W0..W7   = the eight 32-bit big endian words of u, W_k = (u >> (224 - 32k)) & 0xffffffff
v' = v >> 72                      (a 184-bit value)
W8..W12  = (v' >> (152 - 32j)) & 0xffffffff   for j = 0..4
W13      = ((v' & 0xffffff) << 8) | 0x80
W14      = 0
W15      = 440
```

`C32(S, B)` is the profile's reduced compression. Parse `B` as `W0..W15`. For
`t = 16..31`, `W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2])`. Run
steps `t = 0..31` from `S = IV` with the standard `Sigma0`, `Sigma1`, `Ch`, `Maj`,
constants `K[t]` at their original indices and all additions modulo `2^32`. Return
`S` plus the working state, word by word modulo `2^32`. The digest word `d` used
below is the big endian concatenation of the eight returned words into one 256-bit
integer, `H0` in the top 32 bits.

The marshalling above and an independent transcription of `C32` were checked against
`verifier/hash_functions.py:digest(m, "sha256", 32)` on 3000 uniformly random
`(u, v)` pairs. Every digest agreed. This is a check of the encoding, not evidence
for any heuristic.

## 2. Algorithm and storage

Let `q = 2^128`, `N = 2^256` and `s = 148`. A RAM word has 256 bits and 32 bytes.
`Rand()` is the independent uniform 256-bit random word primitive of the model. It
is used afresh, twice per sample, and is never expanded from a seed.

Two regions are used.

* The sparse table `S` has one word per slot. Slot `b` lives at byte address `32 b`
  for `b < 2^148`, so `S` spans addresses `[0, 2^153)`. **No cell of `S` is ever
  initialised.** The algorithm is correct for any initial memory contents.
* The dense array `D` starts at byte address `Db = 2^153`. Record `i` occupies four
  words at `Db + 128 i`, holding `(d, u, v, nxt)`. `nxt` is a record index or the
  constant `NIL = 2^256 - 1`.

```
steps = 0 ; i = 0
while i < q:
    u = Rand() ; v = Rand()
    d = digest(u, v)                       # Section 1, one C32 call
    slot = d >> 108 ; a = 32 * slot
    x = S[a]                               # arbitrary garbage possible
    nxt = NIL
    if x < i and (D[x].d >> 108) == slot:  # x names a real earlier record in this slot
        nxt = x ; cur = x
        loop:
            steps += 1
            if steps > LAMBDA: halt FAIL   # LAMBDA = 2^120
            if D[cur].d == d:
                if (D[cur].u, D[cur].v >> 72) != (u, v >> 72):
                    recompute both digests with two fresh C32 calls
                    return the two messages           # verified collision
                else: halt FAIL            # identical message, negligible
            if D[cur].nxt == NIL: break
            cur = D[cur].nxt
    D[i] = (d, u, v, nxt)
    S[a] = i
    i += 1
halt FAIL
```

All counters, indices and addresses are below `2^256`. `LAMBDA` and `Db` are fixed
constants. The loop is iterative and uses no recursion. The run is one finite pass.
There are no restarts, so there is no success amplification outside the run. The only
stored state of a sample is its record. Randomness is retained only inside records.

## 3. Correctness

**Claim A.** For every initial content of `S`, after sample `k` has been inserted,
the cell `S[32 * slot]` holds the index of the latest sample with that slot, provided
at least one sample has that slot. Following `nxt` from it visits every earlier sample
with that slot, newest first, and no sample of any other slot.

*Proof.* Induct on `k`. Each insertion writes `S[a] = k` and stores `nxt`. If an
earlier sample `j` had the same slot, then `S[a]` was overwritten with the index of the
latest such `j` when `j` was inserted. Since `j < k`, the test `x < i` holds and the
stored digest of `D[x]` has the same slot, so the code sets `nxt = x`, which is the
previous latest sample of the slot by the induction hypothesis. If no earlier sample
has this slot, `S[a]` was never written by this run. It holds arbitrary garbage `x`.
If `x < i`, then `D[x]` is a real earlier record and the slot test compares its true
slot with ours. They differ, because no earlier sample has our slot. The code then
sets `nxt = NIL`. If `x >= i` the first test fails and the same assignment happens.
Hence `nxt = NIL` exactly when the slot is new, and otherwise `nxt` is the previous
latest sample of the slot. Chains therefore partition samples by slot. Every record
read is a previously written one. No garbage is ever dereferenced. `D[x]` is read
only after `x < i` is established. ∎

**Claim B.** If no two samples have equal messages, and `steps` never exceeds
`LAMBDA`, then the algorithm returns a collision whenever two samples have equal
digests.

*Proof.* Equal digests have equal slots. By Claim A, when the later sample `j` is
processed, the earlier sample `i` lies on its chain, so the comparison `D[cur].d == d`
fires at the latest at `cur = i`. The messages differ by hypothesis. The two fresh
recomputations of the complete padded hashes give the same two digests, since `D`
stores exactly the sampled `(u, v)`. The returned messages are distinct and satisfy the
profile's relation. If the chain walk returns earlier on another equal digest, that
pair is also a verified collision. Every successful return satisfies the relation. ∎

## 4. Success probability

The samples `X_1, ..., X_q` are independent and uniform on the `2^440` messages,
because each message is a deterministic bijective image of fresh random words. The
digests `Y_i = H(X_i)` are independent and identically distributed with some
distribution `p` on `N` values. Nothing about `p` is assumed in this step.

**Distribution free birthday bound.** For `2 <= q <= N` the probability that all of
`Y_1..Y_q` are distinct is at most `prod_{j<q}(1 - j/N)`, whatever `p` is. This is
a standard fact and the proof is given for completeness. The probability equals
`q! e_q(p)`, where `e_q` is the elementary symmetric polynomial. On the compact
simplex `e_q` has a maximizer, and among maximizers pick one minimizing the sum of
squared coordinates. If two coordinates `a != b` differ, hold the rest fixed. Then
`e_q = A + (a+b) B + a b C` with `C = e_{q-2}(rest) >= 0`. Replacing `a, b` by their
mean does not decrease `a b`, so it keeps a maximizer and strictly lowers the sum of
squares, a contradiction. The maximizer is uniform, so the bound holds for all `p`.
With `q = 2^128` and `N = 2^256`,
`prod(1 - j/N) <= exp(-q(q-1)/(2N)) = exp(-(1/2 - 2^-129))`.
Since `exp(1/2) > 1 + 1/2 + 1/8 + 1/48 + 1/384 + 1/3840 > 1.6486`, we get
`exp(-1/2) < 0.60660` and the failure bound `exp(-1/2 + 2^-129) < 0.60661`.
Hence `Pr[E] > 0.3933` where `E` is the event that two samples have equal digests.

**Repeated messages.** The probability that two samples have the same 440-bit message
is at most `binom(q,2) 2^-440 < 2^-185`. Call this event `R`.

**Chain walk budget.** Let `S_tot` be the total number of chain steps in a full
unterminated run. It is at most `sum_k #{i < k : slot(Y_i) = slot(Y_k)}`. By
independence, `E[S_tot] = binom(q,2) sum_b c_b^2`, where `c_b` is the probability that
a uniform message has slot `b`. This is exact and needs no assumption. The size of
`sum_b c_b^2` is the content of heuristic `H1` below. Under `H1`,
`E[S_tot] < 2^255 * 8 * 2^-148 = 2^110`, so by Markov
`Pr[S_tot > 2^120] <= 2^-10`.

**Conclusion.** If `E` holds, `R` does not hold and `S_tot <= 2^120`, the algorithm
succeeds by Claim B. Therefore, under `H1`,

`Pr[success] >= 0.3933 - 2^-10 - 2^-185 > 0.3923 > 0.39`.

The claimed `0.39` keeps a margin of about `0.0023`. It is the success event of the
fixed algorithm under its own fresh coins. It is not a confidence in `H1` or in a
reviewer. The only use of `H1` is to bound the work cap. The existence of a digest
collision among the samples is proved without it.

## 5. Charged time

One `C32` call costs one unit. Every other primitive costs `1/2224` unit. The ledger
follows the organizer baseline's convention that one logical instruction with RAM
operands expands to at most 8 primitives (two operand loads, the operation, a result
store and four instruction word fetches). This is deliberately pessimistic, because it
charges instruction fetches the model does not list as a primitive. `Rand()` is one
instruction. Counts of primitive operations `W` are separate from target compressions.

**Per sample logical instructions (no chain steps).**

| Part | Instructions |
| --- | ---: |
| `u = Rand()`, `v = Rand()` | 2 |
| `v' = v >> 72`; `W0` (1), `W1..W6` (2 each), `W7` (1), `W8` (1), `W9..W12` (2 each), `W13` (3) | 27 |
| Operand transfer into the call, 8 IV words and 16 block words | 24 |
| Pack eight output words into `d`, 7 shifts and 7 ORs | 14 |
| `slot`, address `32 slot`, load `x`, compare `x < i`, branch | 5 |
| Slot check on `D[x]`, shift `x << 7`, add `Db`, load, shift, compare, branch | 6 |
| Select `nxt`, four stores of the record, advance record pointer, store `S[a]`, `i += 1`, loop compare, loop branch | 10 |
| **Total** | **88** |

At 8 primitives each the per sample bound is `704` ordinary operations, plus one
compression call.

**Per chain step logical instructions.** Compute the record address (2), load the
stored digest, compare, branch (3), load `nxt`, compare with `NIL`, branch (3),
increment `steps`, compare with `LAMBDA`, branch (3). That is 11 instructions, at most
88 primitives. The budget of `96` primitives per step is used. The cap is
`LAMBDA = 2^120` steps for the whole run, enforced by the counter.

**Other work.** Initialising constants, `IV`, the shift amounts and the pointers is at
most `2^20` primitives. The final recomputation of two messages (two `C32` calls,
about 65 instructions each, comparisons and output of 110 bytes) is at most `2^16`
primitives plus two extra compression calls. These happen at most once.

**Totals, on every choice of coins.** There are at most `q` samples, each
with exactly one compression call, and at most `LAMBDA` chain steps.

```
H_calls <= q + 2
W       <= 2^20 + 704 q + 96 * 2^120 + 2^16
T       =  H_calls + W / 2224
        <= q (1 + 704/2224 + 96 * 2^-8 / 2224 + 2^-108/2224 + ...)
        <  1.31672 q
        <  2^128.397
```

In exact rational arithmetic `T / q = 1.316715...` and
`log2(T) = 128.39694...`. Failed trials, randomness, lookup, collision checking and
verification are all inside `T`, since the run is a single finite pass. The submitted
`time_log2 = 128.4` is a worst case bound, not an expectation. Preprocessing is the
`2^20` primitive setup, which costs `2^20 / 2224 < 2^9` units and is already counted
in `T`.

**Sensitivity.** The scalar is dominated by the per sample ordinary operation count.
Under a register machine reading, where each logical instruction is one primitive,
the same ledger gives `1 + 88/2224` per sample, `log2 = 128.056`. Under the
8 primitive reading used for the claim it is `128.397`. A whole compression
charged per sample without any ordinary overhead gives exactly `128`. Dropping the
hash table and keeping a sort would cost far more, as the organizer's placeholder at
`136` shows.

## 6. Memory, preprocessing and advice

`S` spans byte addresses `[0, 2^153)` and `D` spans `q * 128 = 2^135` bytes starting
at `2^153`. Code, constants and scratch fit in `2^21` bytes. The total address span is
below `2^153.01` bytes, so `memory_log2_bytes = 153.1` is declared. This counts the
address range, although at most `q = 2^128` cells of `S` are ever written, so the
touched memory is about `2^135.2` bytes. The model reports memory without scoring it.

`preprocessing_log2 = 9` states the fixed setup cost in the same time unit as `T`
(`2^20 / 2224 < 2^9`). It is part of `T`. No nonuniform advice is used. The schema
requires a finite value, so `nonuniform_advice_log2_bytes = 0` means an upper bound of
one byte and not permission to hide code. Code storage is charged in memory.

## 7. Heuristic H1 and evidence

`H1` says that for a uniform 55-byte message `X`, the 148 bit slot
`b(X) = top 148 bits of H(X)` has collision probability at most eight times that of a
uniform slot, that is, `sum_b c_b^2 <= 8 * 2^-148`. It is score critical only because
it bounds the work cap. If it fails by a larger factor, the run can exceed `LAMBDA` and
return FAIL. Correctness of any returned pair never depends on it.

The slot is the top 148 bits of the digest, which are the words `H0..H3` and 20 bits
of `H4`. Each of them equals an `IV` word plus a state word of the final rounds, so
each is produced by 32 rounds of mixing from the message words. This is a plausibility
argument and not a proof. The package supplies two scaled
experiments. Each draws `2^9` messages per trial and asks for a pair that agrees on an
18 bit slice, which is the exact analogue of `q^2 / 2^257 = 1/2` (model success
`0.3935`). `slice-top18` uses the top 18 bits of `H0`. `slice-spread` uses the top six
bits of each of `H0`, `H1` and `H3`. A local replication with 4096 trials each (not
organizer evidence) gave `1584` and `1612` successes against a model value of `1610.0`
(`z = -0.83` and `+0.06`).

Limits of this evidence. The experiments probe 18 bit slices and extrapolate to 148
bits. They use seed expanded messages, not independent random words, and the
experiment runner does not give an interval for iid success. The extrapolation rests
on the diffusion argument above. The margin matters, because `H1` allows an eight fold
excess over uniform and the cap leaves a factor `2^7` of Markov slack.

## 8. Limitations and credit

This is an analytic candidate. No full scale run is claimed, and the certificate
manifest is valid and empty. The scalar `128.4` is above the nominal `128`, and other
pending packages on this track may claim lower values. The single block insight and the
uninitialised sparse set table follow ideas published in other solvers' public notes.
This package differs in keeping every collision by chaining, in using one whole
compression per sample without partial evaluation, and in the explicit worst case work
cap. It supersedes the organizer's `136` accounting but inherits no earlier review.
