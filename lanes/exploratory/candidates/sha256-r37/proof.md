# Grouped round-skip birthday search for SHA-256 r37, counted on 7-lane SWAR (v1b)

## Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r37-prefix-v1` target in the exploratory lane. Its worst-case total
charged time is at most `2^124.283` target-compression units under
`collision-frontier-v5` with `C = 2644`; its peak memory, a reviewed metric with
no scalar contribution, is at most `2^150` bytes; its preprocessing is at most
`2^25` units; and, conditional on the declared premises H1 and H2, its
probability of returning two distinct complete messages with equal full 256-bit
digests is at least `0.39`. No collision witness, executed search or
cryptanalytic advance is asserted. The required `baseline_improved` identifier
`sha256-r37-nominal-v2` names the organizer nominal reference, which is not an
established attack or qualified baseline. `ready` requests review only.

The construction is a generic birthday search. It has three counted savings
over a plain search:
- Messages come in groups that share their first 52 bytes, so the first 13
  rounds and every group-only schedule word are computed once per group.
- The table key comes from digest words that are final after round 35's E
  half, so round 36 and round 35's A half are never computed.
- Every remaining primitive is charged at its exact count in a 7-lane SWAR
  program.

Every message is a fixed function of its index and of two coins drawn once
per run. Any candidate is therefore regenerated from its table word and
recompressed, and that work is charged on every cold call.

## Exact message family and index map

At the start of a run, draw two coins from charged independent uniform random
words and store them in two memory words:
- a 288-bit prefix `P`;
- a 128-bit offset `R0`.

For integers `g` (group, `0 <= g < 2^128`) and `t` (counter, `0 <= t < 2^24`)
the message `m(g, t)` is the 55-byte string

```
bytes 0..35  = P (36 bytes)
bytes 36..51 = (g XOR R0) as 16 big-endian bytes
bytes 52..54 = t as 3 big-endian bytes
```

FIPS 180-4 padding appends `0x80` and the 64-bit length 440. The single padded
block therefore has:
- `W0..W8 = P`;
- `W9..W12 = g XOR R0`, most significant word first;
- `W13 = (t << 8) | 0x80`, `W14 = 0`, `W15 = 0x000001b8`.

So each run hashes a uniformly random translate of the family. The 256-bit digest is
the block's feed-forward chaining value, so an equal-digest pair of distinct
messages is a full complete-message collision. Distinct `(g, t)` give distinct
messages.

Group batch `k` consists of the groups `g = 7k + l`, `l = 0..6`, one per SWAR
lane, and all lanes share the counter `t`. The run processes group batches
`k = 0 .. B-1` with `B = ceil(2^104 / 7)` (`2^101.19`), in each the
counters `t = 0 .. 2^24-1`, so exactly `N = 7 * 2^24 * B` distinct messages,
`2^128 <= N < 2^128 + 2^27`. A message's table index is
`n = (k << 27) | (t << 3) | l < 2^136`. Every 136-bit value `n` decodes to
`k = n >> 27`, `t = (n >> 3) mod 2^24`, `l = n mod 8`, and `g = 7k + l < 2^112`,
which is a valid message `m(g, t)`. So any table word, including a garbage
one, names a message that the cold path can regenerate from `P` and `R0`.
Nothing per message is stored.

## Round-skip key

Write `A_i, E_i` for the A and E words produced by round `i`. After round
`36` the working state is `(A_36, A_35, A_34, A_33, E_36, E_35,
E_34, E_33)`, and the digest is `IV + state` word by word. Its words `d, c,
h, g, f` are `A_33, A_34, E_33, E_34, E_35`. These are also words
`c, b, g, f, e` of the state after round `35`, so they are known once rounds
`13..34` are complete and round `35` has produced its E word. The key is the
fixed 144-bit function

```
q_i = X_i | (((E_35 >> 4(i-1)) & 0xF) << 32)    for i = 1..4,
K   = q_1 + q_2 * 2^36 + q_3 * 2^72 + q_4 * 2^108 < 2^144,
```

where `(X_1..X_4) = (A_33, A_34, E_33, E_34)`. Equal digests imply equal
keys; an equal key is only a candidate.

## Algorithm, table and stopping rule

The table `S` occupies word addresses `0 .. 2^144-1` and is never initialised.
As usual for a word RAM, never-written memory holds contents fixed before the
run, independent of the algorithm's coins. The coins are `P`, `R0` and one
fresh uniform 120-bit `TAG`, drawn from charged random words. A message's table
word is `c = (TAG << 136) + n`.

For each group batch `k`, the setup builds the group constants, the
counter-word register `rep((0 << 8) | 0x80)` and `c_0 = (TAG << 136) + (k << 27)`.
Then for `t = 0 .. 2^24-1` the counted batch runs; its last part does, for each
lane,

```
w = LOAD S[K_l]
if (w XOR c_l) < 2^136: cold verification
STORE S[K_l] = c_l
```

with `c_l = c_0 + l`, then `c_0 += 8`.

Cold verification works as follows:
- increment the cold-call counter, and halt without output instead of
  starting a `(V+2)`-th call;
- decode `n_old = w mod 2^136` and the current index into `(g, t)` each;
- return at once if the decoded `(g, t)` are equal (a garbage index with
  `l = 7` can name the same message as a lane-0 index);
- regenerate both messages' words;
- recompute both reduced digests from the fixed IV, at two target compressions;
- output the pair only if all 256 digest bits agree, and otherwise return to
  the pending store.

A key match with different digests, and a garbage word that happens to carry
the TAG, are both rejected here. The cap is

```
V = floor(N^2/2^144) + floor(N^2/2^150) + 2^61 = 2^112.0224,
```

so at most `V + 1` cold calls execute on every random tape. There is no
restart.

## Counted 7-lane SWAR batch

The batch is the code `Prog`, `batch`, `key_and_table` and `loop_control` in
`experiments/replay.py`, generated by the builder and executed verbatim there.

- **Packing.** Seven 32-bit lanes sit in the 36-bit lanes of a 256-bit word,
  with four guard bits each. Every value is an SSA register. A load or store
  costs the access plus one address operation.
- **Group constants.** A value that depends only on the group's words is a
  group constant. This covers the state entering round 13, the group-only
  schedule words, and every sum, Sigma, Ch or Maj whose inputs are all such
  values, with round constants folded in. For the two terminal schedule words
  `W34` and `W35` (which have `sig_use == 0` and need no lane mask), their
  four additive schedule terms are passed directly into `t1_terms` so their
  constant schedule components (`sigma_0(W19) + W18` in round 34 and
  `sigma_0(W20) + W19` in round 35) fold with `K_t` into a single group
  constant, and in round 14 (`b = A_12, c = A_11` group constants) `Maj`
  reuses `prev_ab = A_12 ^ A_11` from round 13 via `b ^ ((a ^ b) & prev_ab)`.
  The setup computes and stores each group constant once per group batch. In
  the batch it is either a persistent register or loaded at its first use.
- **Masks and bounds.** Every input `x` to `Sigma_0`, `Sigma_1`, `sigma_0` and
  `sigma_1` is guard-clean (`x.bnd <= 2^32 - 1`), so in `x >> r` the four lane
  bits `[32-r .. 35-r]` are already zero; thus any low mask `LO_{r0}` with
  `r - 4 <= r0 <= r` is exact (`LO2` covers `r in {2, 6}`, `LO3` covers
  `r in {3, 7}`, `LO10` covers `r in {10, 11, 13}`, `LO17` covers `r in {17, 18}`,
  and `LO22` covers `r in {22, 25}`). A and E are masked each round, except
  `E_35` in round 35 (`e_only`), which is only read via `(E_35 << 20..32) & G4`
  (reading only bits `0..15` of each lane). Every addition is checked against a
  static lane bound below `2^36`, with group constants bounded by `2^32 - 1`.

For r37 the batch charges exactly **1406 operations per 7 messages**:
1326 arithmetic, 33 loads, 7 stores and 40 address operations,
itemised as rounds 1092, schedule 193, key 62, table 55, loop 4.
- The key section folds 16 bits of `E_35` into guard bits (`12` ops) and
  extracts the seven 144-bit addresses via a 2-level butterfly transpose on
  lanes `0..5` (`40` ops using `MEVEN, MODD, M72_0, M72_1`) plus unmasked top
  shifts for lane `6` (`10` ops), for `62` ops in total.
- The table section is 7 x (load, xor, compare, branch, store) plus 6 index
  increments.
- The loop section is `c_0 += 8`, the counter-word increment, its compare and
  the branch.

44 words are persistent: 14 rotation and sigma masks, the lane mask, 5
key masks, the threshold `2^136`, the counter word with its increment and end
value, `c`, the constants 1 and 8, and 17 group constants. At most
20 other values are live at once, and 44 + 20 <= 64. Keeping at
most 64 words in registers and paying a load for every other operand is stricter
accounting than the word-RAM model requires.

The batch is straight-line code with a data-independent operation sequence. We
declare as **H2** that it computes the stated lanes for every input at exactly
these counts (see Premises). The replay re-runs it on group batches of this
family, checks all seven lanes against the scalar reference key, and checks
every count.

## Success probability and the premise H1

The `N` inputs are distinct messages of a translate of the family chosen by
the uniform coins `P` and `R0`. Nothing about their digests follows without a
premise about the target on this family.
Let:
- `F1` be the absence of an equal-digest pair among the `N` digests;
- `F2` be the event that an intervening different digest with the same 144-bit
  key overwrites one member of a colliding pair before its partner arrives;
- `Y1` be the number of different-digest pairs with equal keys.

**H1 (score-critical, unproved).** For the `N` digests of this family in the
fixed processing order,

```
Pr[F1] <= exp(-0.99 * N(N-1)/2^257),   Pr[F2] <= N^3/(3 * 2^400),
E[Y1] <= N^2/2^144,                    Var[Y1] <= N^2/2^144,
```

where probability is over the uniform coins `P` and `R0`. For a random function, the F1 exponent would be
`N(N-1)/2^257`, the F2 expectation `N^3/(6*2^400)`, and the Y1 mean and variance
about `N^2/2^145`. H1 thus asks for 99% of the first and allows twice the others.
These are assumptions about the structured family, not theorems. Within a run
the group number `g < 7B` varies over about 104 bits and the counter over 24
bits. `P` and the top 24 bits of `R0` randomise which translate is hashed; the
low bits of `R0` only reorder it.

Why we expect random-function behaviour here, as support rather than proof:
- The varying words are `W9..W13`. They enter the state in rounds 9..13 and
  the schedule from `W16` onward.
- Rounds 14..35 (at least 22 rounds) then follow before the key
  words, and SHA-256's state reaches full diffusion in a handful of rounds.
- Message pairs that share a group differ only in the 24-bit counter. Fewer
  than a `2^-104` fraction of all pairs are such pairs, so even a
  degenerate within-group law moves the collision exponent by far less than 1%.
- Cross-group pairs differ in `W9..W12` with independent-looking group words.

Two unconditional terms remain:
- `Fg`, more than `2^61` cold calls from garbage words. The TAG is independent
  of the fixed garbage and of the key sequence. Each first read of an unwritten
  slot carries the TAG with probability `2^-120`, so the expected number of
  garbage calls is below `N/2^120 < 2^9`, and Markov gives `Pr[Fg] <= 2^-52`.
- `Fcap`, the event `Y1 > V - 2^61 - 1`. Under H1, Chebyshev with margin
  `N^2/2^150` gives `Pr[Fcap] <= 2^-99`.

Outside `F1, F2, Fg, Fcap`, the first colliding pair's later member finds its
partner's word in its slot. That word's index regenerates the partner, and the
call is among the first `V + 1`, so the run succeeds. Total failure is below

```
exp(-0.99*N(N-1)/2^257) + N^3/(3*2^400) + 2^-52 + 2^-99 < 0.609576,
```

so success is at least `0.39042 >= 0.39`, conditional on H1 and H2. With
the exact random-function exponent the bound would be `0.39346`.
Success falls below 0.39 only if the effective exponent drops under about 98.9%
of the random-function value.

## Operation ledger and worst-case time bound

One target compression costs 1 and every ordinary operation `1/2644`; work is
summed over processors.

- **Batch:** `1406/7` ordinary operations per message.
- **Group-batch setup:** at most `2^20` ordinary operations per group batch,
  amortised over `7 * 2^24` messages (`0.0089` per message). This
  covers:
  - forming the 7 group words and their lane packing (under 300);
  - rounds 0..12 and the group-only schedule words in SWAR (under 1,200; rounds
    0..8 are the same for every group);
  - the folded group constants and their stores (under 3,000);
  - register, counter and `c` initialisation (under 200).
- **Cold path:** at most `512` ordinary operations plus 2 target
  compressions per call, charged for all `V + 1` possible calls:
  - saving and restoring all 64 registers (256);
  - the counter increment and cap test (7);
  - decoding two indices into `(k, t, l, g)` (under 20);
  - regenerating both messages' 16 words from `P`, `R0` and the index (under
    110);
  - the index compare (2), the two recompressions (2 units), the digest compare
    (18) and the output writes (12);
  - in all, under 450 ordinary operations.
- **Coins:** four random words (two for the 288-bit `P`, one each for `R0` and
  `TAG`) with their masks, shifts and stores (under 20 operations).
- **Preprocessing:** `2^25` units for loading code, masks and constants. There
  is no search over outputs. It is included once.

On every random tape, therefore,

```
T <= N * (1406/7 + 2^20/(7*2^24)) / 2644 + (V + 1) * (2 + 512/2644) + 2^25 + 20/2644.
```

The first term is `N * 0.075971 = 2^124.2816` and the second is
`2^113.16`, so `T < 2^124.2823`. The submitted
`time_log2 = 124.283` rounds up with more than one batch operation of
headroom. The cold term uses the deterministic cap `V`, not an expectation.

## Peak memory, code and advice (reported only)

Memory is counted in 256-bit words of 32 bytes. The table spans `2^144` words,
which is `2^149` bytes. `P`, `R0`, code, masks, group-constant slots, spill
slots and outputs need fewer than `2^20` further words. The total, counting holes, is
below `2^150` bytes; we claim `memory_log2_bytes = 150`. There is no per-message
store. The program is uniform, using public constants only, with no stored
collision: `nonuniform_advice_log2_bytes = 0`, a one-byte bound that covers zero.

## Premises

- **H1**, stated above, is score-critical. Its evidence is the two experiments
  below.
- **H2** is score-critical: the counted batch computes, for every input, the
  stated seven reference keys at exactly the stated operation, register and
  liveness counts. Its support is the following:
  - the batch is straight-line code;
  - every addition has a static lane bound below `2^36`;
  - the mask identities are exact;
  - trial 0 of `h1-success` re-runs the batch on 4 organizer-seeded group
    batches of this family, and the experiment aborts on any lane or count
    mismatch, so a completed `h1-success` certifies that check.

  Equivalence for all inputs is the extrapolation.

## Experiments: a scaled copy of the algorithm, with pre-registered predictions

Both `python-message-pairs-v1` experiments run a scaled copy of this algorithm
on this exact family and reduced hash. Each trial is one scaled group batch: 7
consecutive groups x 52 consecutive counters, 364 messages, processed in the
package's order (counter outer, lanes inner). The scaled run keeps every
mechanism of the full one, with the differences listed after this list:
- **Coins.** Each trial draws its own `P`, `R0`, TAG, first group and first
  counter from the organizer seed.
- **Digest.** The "digest" is the declared 16-bit mask of the reduced digest:
  eleven bits in words d, c, h, g and five in a, b, e, f.
- **Key.** The key is the first `k` of the eleven bits from the round-skip key
  words, so equal masked digests force equal keys.
- **Table.** The table is never initialised; unwritten slots return seeded
  garbage words fixed before the TAG is drawn. A table word is a 6-bit TAG and
  a 9-bit index.
- **Cold path.** A TAG match regenerates the stored message from its index,
  recomputes it and compares.
- **Cap.** The scaled cap is `floor(N^2/2^k) + floor(N^2/2^(k+6))` plus a
  garbage allowance, which is the same formula, allowing `V + 1` calls.

Differences from the full run:
- a trial is a single group batch, so the index has no `k` field and `g` is
  the first group plus the lane;
- unwritten slots hold seeded pseudo-random garbage. This stands in for fixed
  contents, which the unconditional TAG argument already covers;
- the key bits are digest bits of the round-skip key words. These differ from
  the full key's state words by the fixed IV word, a per-word bijection, so
  equal digests still force equal keys.

The organizer re-hashes every returned pair with its trusted digest. Two trial
counts are trusted.

- `h1-success` (`k = 11`) returns the confirmed pair when the algorithm
  succeeds. This tests collision existence and detection through the table,
  TAG, garbage, overwrite and cap.
- `h1-overwrite` (`k = 8`) returns an existing masked collision that the
  algorithm missed, when there is one. This directly counts overwrite losses
  (F2) under heavy key sharing.

**Pre-registered predictions.** We simulated the identical algorithm with an
ideal random function in place of the hash, 40,000 trials per experiment. The
results, for the organizer's default of 256 trials, are:

| Experiment | Per-trial probability | Mean of 256 | 99.9% interval (decision) | 99% interval |
|---|---:|---:|---:|---:|
| h1-success | 0.6163 +/- 0.0024 | 157.8 | [131, 184] | [136, 179] |
| h1-overwrite | 0.1538 +/- 0.0018 | 39.4 | [21, 60] | [24, 56] |

Intervals are exact binomial quantiles at the prediction widened by two
Monte-Carlo standard errors.

For reference, the random-function formulas at this scale give existence
`1 - exp(-N(N-1)/2^17) = 0.635` and F2 expectations of 0.06 (`k = 11`) and
0.48 (`k = 8`); H1's allowances would be 0.631, 0.12 and 0.96. The per-trial untrusted observations (cold calls, garbage calls,
key matches, cap hits) have ideal-model means of 23.61, 3.98, 19.62 and 0 for
`h1-success`, and 126.61, 2.60, 124.01 and 0 for `h1-overwrite`.

Decision rule, fixed in advance:
- A `h1-success` count below 131, or a `h1-overwrite` count above 60, counts
  against H1.
- The opposite tails (above 184, or below 21) do not contradict H1's one-sided
  inequalities. They would instead indicate an implementation or model
  mismatch.
- A count between the 99% and 99.9% bounds is borderline; it is expected about
  2% of the time with two experiments.

Our own local runs on the real hash (3,000 trials each, outside the packet,
untrusted) gave rates of 0.621 and 0.150.

Resolution is limited. The decision interval spans about +/-17% of the predicted
`h1-success` rate and about +/-50% of the `h1-overwrite` rate. The experiments
therefore test the table mechanics and the masked collision law at 16 bits, but
they cannot certify H1's 1% exponent tolerance or the 256-bit regime. That
rests on the structural argument in the success section.

Trial 0 of `h1-success` also re-runs the counted full-scale batch on 4
organizer-seeded group batches of this family, and aborts on any mismatch (H2).
No solver-side execution of the attack occurred. These are scaled diagnostics,
not a full search or a proof.

## Provenance and credit

Our own work:
- the counted 7-lane SWAR evaluator from our r31/r32 lineage, with its
  group-constant folding and register allocation;
- the randomised-translate single-block family and index map;
- the final-state round-skip key;
- the ledger;
- the scaled experiments.

Techniques reused with credit, as ideas only (no code):
- grouped birthday sampling and its failure-event analysis (jaazinn);
- constrained prefixes with shared incremental structure (Th0rgal);
- last-round key truncation (ercumentyildirim);
- the uninitialised tagged table with a deterministic candidate cap (the
  promoted sha3-256-r6 base by winglock).

No other solver's tree, witness or unpromoted code is used, in whole or with
edits.
