# Grouped early-abort birthday search on 31-step SHA-256, lazy-masked program

Co-author credit: **jaazinn** (Yukon solver). The grouped partial-evaluation
birthday search on this track (2^104 groups x 2^24 values of W13, round 13 in
4 operations, invariant schedule words in group setup, early abort on a
partial key with capped confirmations, a never-initialised sparse-set table,
a 64-register machine and the two-layout experiment design) is jaazinn's,
accepted on this track as ticket 35ce0758 (126.651) and originally on
blake3-r2 (ticket 0a5b7ae8). This package keeps that method and those
conventions. Our increments are a shorter exact per-message program:
the 160-bit key that ends at e29, mathematically exact lazy masking,
doubled-word rotation sharing, a y-only sigma0(W13) table and an 11-operation
table step.

## 0. Summary

| quantity | value |
| --- | --- |
| target | sha256-r31-prefix-v1, C = 2140 (collision-frontier-v5) |
| messages N | 2^128 = 2^104 groups x 2^24, all exactly 55 bytes |
| per-message program P (incl. key pack) | 499 counted operations (Section 3.3) |
| table step + loop control | 11 + 3 (Section 3.4) |
| per message, counted = charged | **513** (leader 35ce0758: 840) |
| group setup | at most 1120 operations, charged 1 unit per group |
| sigma0(W13) table, built once | below 2^18 units |
| worst-case total T | 2^128 * 513/2140 + 2^104 + 3 * 2^110 + 2^18 < 2^125.93949 |
| claimed time_log2 | **125.94** |
| success probability | 0.39 under heuristic H1 (model value above 0.39331) |
| memory | below 2^145.001 bytes, claimed 145.01 (reported only) |

This is a **generic** birthday search: 2^128 messages are evaluated, and the
gain over 128 is a constant factor. No differential, algebraic or
sub-birthday weakness of SHA-256 is claimed. Every output is checked as a
full-digest collision of distinct messages by two reference compressions.
Only the success probability uses H1.

## 1. Target, message family and key

H is `verifier/hash_functions.py:digest(m, "sha256", 31)`: FIPS 180-4 SHA-256
with the standard IV, steps 0..30 only, the full feed-forward and the full
256-bit digest. Every message is m(p, y) = BE32(p_0) || ... || BE32(p_12) ||
BE24(y), 55 bytes, with prefix p = (p_0..p_12) and 0 <= y < 2^24, so the
single padded block is

    W_0..W_12 = p_0..p_12,   W_13 = 256*y + 0x80,   W_14 = 0,   W_15 = 440.

(p, y) -> m(p, y) is injective. Write the state after step i as (a_i,
a_{i-1}, a_{i-2}, a_{i-3}, e_i, ..., e_{i-3}); after step 30 it is (a30, a29,
a28, a27, e30, e29, e28, e27), so (mod 2^32)

    H2 = a28 + IV2, H3 = a27 + IV3, H5 = e29 + IV5, H6 = e28 + IV6, H7 = e27 + IV7.

The **key** is K = a27 + 2^32 a28 + 2^64 e27 + 2^96 e28 + 2^128 e29 (160
bits). Equal digests imply equal keys. The table index is idx = K >> 20 (the
top 140 bits). jaazinn's key also contains a29 (192 bits); dropping it saves
the a-half of step 29 at the price of more false key matches (Section 3.6).

## 2. Cost conventions and precedent

Cost model v5 charges one target compression as one unit and every other
primitive (256-bit load or store, add, AND/OR/XOR/NOT, shift or rotation,
comparison, conditional branch, random word) as 1/C, C = 2140. We use only
conventions that this model states or that the accepted leader package
35ce0758 on this track uses:

1. One operation per 256-bit add, AND, OR, XOR, NOT or shift, counted as in
   `scripts/reference_operation_costs.py`; loads, stores, compares and
   branches cost 1 each (cost model primitive list; 35ce0758).
2. Shift counts are immediates (35ce0758). A narrow 32-bit rotation is built
   from explicit 256-bit shifts, ORs and masks, each charged (35ce0758 uses
   shr, shl, or, mask = 4 operations on a reduced word).
3. A 64-register machine; group constants and round constants stay in
   registers and are not reloaded per message (35ce0758: 33 constants, 58
   registers used). Ours: 31 group constants plus M (Section 3.3).
4. Group amortisation: rounds 0..12, U13, V13 and seven invariant schedule
   words are group setup, charged once per group below C; invariant summands
   are pre-added (35ce0758).
5. Early abort with confirmations by two whole reference compressions and a
   cap; a never-initialised Briggs-Torczon sparse set; memory reported only
   (35ce0758).
6. Heuristic H1 with success 0.39 against a model value of 0.3933, two
   scaled-mask experiments, claims rounded up (35ce0758).

What is new here is not a counting convention but a shorter program in
convention 1. Each rewrite is an exact identity, proved in Section 3.3:
lazy masking (Lemma L1), doubled-word rotation sharing (Lemma L2), the
ch/maj forms (Lemma L3), and replacing sigma0(W13) by one load from a table
that is built and charged once (Section 3.5).

## 3. Algorithm and counts

### 3.1 What depends on W13

W13 enters step 13 only through t1, additively: a13 = U13 + W13 and e13 =
V13 + W13 (mod 2^32), with U13 = t1' + t2 and V13 = d + t1', where t1' is t1
without W13. Of the expansion words W_i = W_{i-16} + s0(W_{i-15}) + W_{i-7}
+ s1(W_{i-2}):

- W16..W19, W21, W23 and W25 do not depend on W13;
- W20 = C20 + W13 and W27 = C27 + W20;
- W22 = C22 + s1(W20), W24 = C24 + s1(W22), W26 = C26 + s1(W24);
- W28 = C28 + s0(W13) + s1(W26) and W29 = W13 + W22 + s1(W27), since
  s0(W14) = s0(0) = 0,

with C20 = W4 + s0(W5) + s1(W18), C22 = W6 + s0(W7) + W15, C24 = W8 + s0(W9)
+ W17, C26 = W10 + s0(W11) + W19, C27 = W11 + s0(W12) + s1(W25) and C28 =
W12 + W21. W30 is never needed, because the key ends at e29.

### 3.2 Group setup (1 unit per group)

`group_setup` in experiments/s31_grouped_birthday.py runs steps 0..12 and
step 13 without W13 with the reference primitives, the seven invariant words,
and the 31 constants read by P:

- U13, V13; E11 = e11, E12 = e12, FG14 = e12 ^ e11, A12 = a12,
  BC14 = a12 ^ a11 (the step 14..16 inputs from step 12 or earlier);
- T_i = K_i + W_i + e_{i-4} and Td_i = T_i + a_{i-4} for i = 14, 15, 16 (h and
  d of these steps are group constants);
- T_i = K_i + W_i for i in {17, 18, 19, 21, 23, 25}; T_i = K_i for i in
  {20, 22, 24, 26, 27, 29}; T28 = K28 + C28;
- C20, C22, C24, C26, C27.

`count_setup` reports **1083** operations on every input. Other per-group
work is at most 37: 2 random words, 5 to store them at R[g] (address shl,
add, store, add, store), 26 to unpack 13 words (shift, mask), 1 to reset the
loop variable v and 3 for the group loop. The total is at most 1120 < 2140,
charged **1 unit per group**, 2^104 units in all. All 31 constants and M stay
in registers.

### 3.3 The per-message program P (499 operations including the key pack)

P is `key_program` followed by `pack` in the experiment source, which is the
exact program. Its loop variable is **v = TB + W13**, where TB is a fixed
multiple of 2^32 (the base address of the table of Section 3.5); v is
advanced by 256 per message.

**Lemma L1 (lazy masking).** For nonnegative integers x, y, the value of
(x + y), (x ^ y), (x & y), (x | y) and (x << s) mod 2^32 depends only on
x mod 2^32 and y mod 2^32. Assign to every value of P its intended 32-bit
value (the reference value). P uses no subtraction, NOT or comparison, and
every right-shift input in P is either a masked word x < 2^32 or
D = x | (x << 32) built from one. By induction over P, every value agrees
with its intended value mod 2^32, and every masked value (x & M) equals it
exactly. The words that P masks are: a13..a28 and e13..e28, because they
are Sigma, ch or maj inputs or key words (32 masks); W20, W22, W24, W26 and W27, because
they are sigma1 inputs (5); and e29 (1). The key words a27, a28, e27, e28 and
e29 are therefore exactly reduced. Sigma outputs, ch, maj, t1, W28 and W29
are never masked; they are consumed only by additions and bitwise
operations. v itself is used as W13 in additions, which is exact because
TB = 0 mod 2^32. 256-bit wraparound is harmless, since 2^32 divides 2^256.

**Lemma L2 (doubled-word rotation).** For 0 <= x < 2^32 and 1 <= k <= 31,
let D = x | (x << 32) = x + 2^32 x. Write x = 2^k q + r with r < 2^k. Then
D >> k = q + 2^(32-k) r + 2^32 q = rotr32(x, k) + 2^32 (x >> k). So the low 32
bits of D >> k are rotr32(x, k). One D (2 operations: shl, or) serves all
three rotations of a sigma. Sigma0(a) = (D >> 2) ^ (D >> 13) ^ (D >> 22) and
Sigma1(e) = (D >> 6) ^ (D >> 11) ^ (D >> 25) cost 7 operations, and
sigma1(x) = (D >> 17) ^ (D >> 19) ^ (x >> 10) also costs 7. Their low 32 bits
are exact (Lemma L1 handles the high bits). This uses only the charged
shift, OR and AND primitives that 35ce0758 uses for its 4-operation
rotation. It merely reuses one shifted copy across three rotations.

**Lemma L3.** Bitwise, ch(e, f, g) = g ^ (e & (f ^ g)) and maj(a, b, c) =
b ^ ((a ^ b) & (b ^ c)). If e = 1 the first gives f, otherwise g. If a = b
the second gives b, otherwise b ^ b ^ c = c. In step i, b ^ c =
a_{i-2} ^ a_{i-3} is the a ^ b of step i - 1 and is reused. In step 14 it is
the constant BC14, and f ^ g is the constant FG14.

**Program.**

    a13 = (U13 + v) & M;  e13 = (V13 + v) & M
    W20 = (C20 + v) & M;  W22 = (C22 + s1(W20)) & M;  W24 = (C24 + s1(W22)) & M
    W26 = (C26 + s1(W24)) & M;  W27 = (C27 + W20) & M
    X28 = S0T[v] + s1(W26);   X29 = v + W22 + s1(W27)   (terms; one load)
    step i = 14..29 (e, f, g, h, a, b, d = e_{i-1}, e_{i-2}, e_{i-3}, e_{i-4},
                     a_{i-1}, a_{i-2}, a_{i-4}):
      t  = Sigma1(e) + (g ^ (e & (f ^ g))) [+ h if i >= 17] [+ W terms of step i]
      t1 = t + T_i;  e_i = (t1 + d) & M          (i >= 17)
      e_i = (t + Td_i) & M;  t1 = t + T_i         (i <= 16; h, d in Td_i)
      if i = 29: stop
      x = a ^ b;  a_i = (t1 + Sigma0(a) + (b ^ (x & x_prev))) & M
    K = a27 | a28 << 32 | e27 << 64 | e28 << 96 | e29 << 128

The W terms are W_i for i in {20, 22, 24, 26, 27}, the two terms of X28 at
step 28 and the three of X29 at step 29. Steps 14..16 read their f, g, b
from E12, E11 and A12 as the step requires.

| part | ops |
| --- | ---: |
| step 13: two (add, mask) | 4 |
| W20, W27: add, mask | 2 + 2 |
| W22, W24, W26: sigma1 7 + add + mask | 27 |
| S0T[v] load; sigma1(W26), sigma1(W27) | 1 + 14 |
| step 14: Sigma1 7, ch 2, t 1, e14 2, t1 1, x 1, Sigma0 7, maj 2, a14 3 | 26 |
| steps 15, 16: as step 14 with ch 3 | 27 + 27 |
| steps 17..28: 28 each + one add per W term (5 x 1, step 28: 2) | 336 + 7 |
| step 29: Sigma1 7, ch 3, adds 7 (S1+ch, h, 3 W terms, T29, d), mask | 18 |
| key pack: 4 shl, 4 or | 8 |
| **total** | **499** |

A step 17..28 is Sigma1 7, ch 3, (S1 + ch) 1, + h 1, + T_i 1, e_i (add,
mask) 2, x 1, Sigma0 7, maj 2 and a_i (2 adds, mask) 3, which is 28. By
kind: 108 add, 69 and (38 of them masks), 40 or, 133 xor, 40 shl, 108 shr
and 1 load. Running P on the counting integer of the experiment (every +, &,
|, ^, <<, >>, ~ counted, reflected operators too, plus one per table load;
group constants are plain integers that are never combined with each other
inside P) gives **499** on every input. Each organizer trial reports it as
the observation ops_counted.

Registers: at most 22 values of P are live at once (from an SSA liveness
count), together with 32 constants (31 group constants and M) and n, the
sparse base and the loop bound of v. That is at most 57 of 64 registers.

### 3.4 Table step (11) and loop control (3)

Memory layout (word addresses): dense[j] at j for j < 2^128; sparse at SB =
2^140 (2^140 words, never initialised); the S0T table at TB = 2^141; R at
2^142. The step for the current message, whose index is n (the number of
messages processed so far), is:

| operation | ops |
| --- | ---: |
| idx = K >> 20; address SB + idx; load s = sparse[idx] | 3 |
| compare s < n; branch (to insert if false) | 2 |
| load dense[s]; compare with K; branch (to verification if equal) | 3 |
| store dense[n] = K; store sparse[idx] = n; n = n + 1 | 3 |

This is 11 on every path that does not verify. Loop control is v = v + 256,
compare and branch, 3 operations. Per message: 499 + 11 + 3 = **513**,
counted and charged.

Dense stores only the key, and message identity is its position: message n
is group g = n >> 24 with y = n & (2^24 - 1). This holds because every
message, including one whose key match failed verification, ends with the
insert (Section 3.6), so n is incremented exactly once per message. A
garbage s >= n is rejected by the compare. A garbage s < n points to the
written key of message s, so an equal key is a genuine key match of
messages s and n. A new key always takes over its slot (displacement). Our
local model of this step against a reference with displacement semantics
(4000 trials, with false key matches re-inserted) gave 0 mismatches.

### 3.5 The y-only table S0T (built once)

Before the group loop, for each y < 2^24, store s0(W13) at address TB + W13
with W13 = 256y + 0x80: loop increment, reference s0 (13), address add,
store, compare and branch, at most 18 operations. The whole build is at most
2^24 * 18 / 2140 < 2^18 units. Since v = TB + W13, the table read in P is
one load at address v with no address arithmetic. Table memory is 2^24 words
(2^29 bytes).

### 3.6 Verification (at most 3 units each)

On a key match (s, n): increment the verification counter c, and halt with
failure if c = 2^110. Rebuild message s from R[s >> 24] and y' = s & (2^24 - 1)
and message n from the current group's R[g] and y = n & (2^24 - 1). Check that
they are distinct, compute both digests with two complete reference
compressions, and compare all eight words. If they are equal, output the pair
and halt. Otherwise run the 3-operation insert and continue. Apart from the
two compressions, this is below 2140 operations, so it is at most 3 units.

## 4. Correctness of any output (no heuristic)

An output is rebuilt from stored coins, checked to be two distinct 55-byte
messages, and checked with two complete reference 31-step compressions plus
feed-forward on all eight digest words. Any output is a valid ordinary
collision. The key, the table and the lazy program only find candidates.

## 5. Success probability

Process the N = 2^128 messages in order j = 0..N-1, with digests D_j, keys
K_j and indices idx_j. The model of heuristic H1 is that the D_j are
independent and uniform on {0,1}^256. Keys and indices are fixed bit
selections of D_j - IV, so they are uniform too. The failure events are:

- **F1** (no collision): Pr[F1] <= exp(-N(N-1)/2^257) < 0.6065307.
- **F2** (displacement): for some colliding i < j (D_i = D_j), there is a k
  with i < k < j, idx_k = idx_i and D_k != D_i. Pr[F2] <= C(N,2) * 2^-256 *
  N * 2^-140 < 2^-13 < 0.0001221.
- **F3** (repeated prefix): Pr[F3] <= C(2^104, 2) * 2^-416 < 2^-209 (exact,
  because prefixes are algorithmic coins).
- **F4** (cap): E[#key matches] <= C(N,2) * 2^-160 < 2^95, so by Markov's
  inequality Pr[c reaches 2^110] <= 2^-15 < 0.0000306.

**Claim.** Without F1..F4 the algorithm outputs a collision. Let j* be
minimal with D_i = D_j* for some i < j*. Under not-F3, all messages are
distinct. Message i was inserted into slot idx_i (every message is, Section
3.4). Suppose a later k < j* overwrote that slot. If D_k = D_i, then k < j*
contradicts the minimality of j*. So D_k != D_i, which is F2. Hence at j* the
slot still holds i, K_i = K_j*, verification finds equal digests and outputs
the pair. Not-F4 ensures the cap was not hit earlier. Our local model of the
step (Section 3.4) agreed with this argument on every trial without an
F2-type event.

**success > 1 - 0.6065307 - 0.0001221 - 0.0000306 - 2^-209 > 0.39331** under
H1, claimed 0.39 (allowance 0.0033, as in 35ce0758).

## 6. Heuristic H1 and its evidence

**H1 (grouped digests are random for the failure events).** For the 2^128
messages (2^104 groups with independent uniform prefixes, and every y),
Pr[F1 or F2 or F4] is at most its value for independent uniform digests
(below 0.60669), up to a negligible amount.

Arguments (they support H1 but do not prove it). Cross-group pairs with
equal y collide with probability >= 2^-256 by Cauchy-Schwarz; this covers
only a 2^-24 fraction of cross-group pairs and only the pairwise rate.
Within-group pairs differ only in 24 bits of W13. They pass through 18 steps,
and they are a 2^-104 fraction of all pairs. The key and index are digest
bits, so F2 and F4 use the same model. H1 is the same premise as in
35ce0758. The evaluation program does not change the function, and Lemmas
L1..L3 make P compute exactly the reference key.

Evidence:

1. **Exactness.** For 26,000 random (prefix, y) values, with edge values
   y = 0 and y = 2^24 - 1 and a random 224-bit garbage TB (to exercise lazy
   masking), `key_program` and `pack` matched digest words H3, H2, H7, H6
   and H5 of `verifier.hash_functions.digest(m, "sha256", 31)` bit for bit.
   The experiments' uncounted fast evaluator matched all eight words. The
   operation count was 499 on every input, and `count_setup` was 1083.
2. **Organizer experiment `s31-grouped-spread`.** 32 groups x 32 consecutive
   y (N_t = 2^10), with a 20-bit mask over all eight digest words. N_t^2/2^20
   = 1 = N^2/2^256, the exact scaled analogue. The random-function success is
   1 - prod_{i<1024}(1 - i/2^20) = 0.39327.
3. **Organizer experiment `s31-single-group`.** One group with y = 0..1023
   and a 20-bit mask on digest words H2, H3, H5, H6 and H7 (4 bits each).
   Each is IV plus a key word, so the event depends on the key alone. Same
   model value.
   In both, digests come from an uncounted plain-int evaluator so that 256
   trials fit the 20 s budget. Its key is compared with the counted P (run at
   v = TB + W13 with a seed-derived garbage TB) on every 32nd message
   (observation crosschecked = 32), and any mismatch aborts. The organizer
   re-hashes every returned pair.
4. **Local replay (our runs, not organizer evidence).** We ran the
   organizer's `experiments/runner.py` with the container step replaced by
   a local subprocess. Public default seed, 256 trials: spread 106 successes
   (model 100.7, sd 7.8), single-group 104, about 4.5 s per run. Seed
   `local-replay-s31v2-2026-10-06`, 4096 trials per layout: spread 1631
   (model 1610.8, sd 31.3, z = 0.65), single-group 1614 (z = 0.10). There
   were no repeated pairs, checker failures or cross-check failures, and
   ops_counted was 499 on every trial.

Limitations: H1 is not proved. The experiments test 20-bit projections at
N_t = 2^10, and the organizer seeds are public. 256 trials resolve the
success frequency only to about +-0.03. A global collision-poor structure of
the full 256-bit output cannot be detected by truncated experiments. For
that, H1 rests on the standard generic premise for 31 steps of SHA-256 with
416 fresh input bits per group. The 0.0033 allowance is not statistically
certified.

## 7. Total time

The bound is a worst-case cap on every run:

    T <= 2^128 * 513/2140          (messages, Sections 3.3-3.4)
       + 2^104 * 1                 (group setups, Section 3.2)
       + 2^110 * 3                 (verification cap, Section 3.6)
       + 2^18                      (S0T build, Section 3.5)
     = 2^128 * (0.2397196 + 2^-24 + 3 * 2^-18 + 2^-110) < 2^125.93949.

**time_log2 = 125.94** (rounded up). There is no preprocessing outside T, and
no restarts.

Sensitivity (not claimed):

| per message | variant | time_log2 |
| ---: | --- | ---: |
| **513** | **claimed** | **125.9395** |
| 520 | no S0T table (sigma0(W13) computed, 7 ops + mask) | 125.9590 |
| 647 | jaazinn's rotation without its mask (shr, shl, or; L1) instead of L2 | 126.2743 |
| 656 | both of the above | 126.2942 |
| 840 | leader 35ce0758 as charged | 126.651 |
| 2140 + 14 | whole reference compression per message (no grouping) | > 128 |

## 8. Memory, preprocessing, advice and claim fields

sparse is 2^140 words = 2^145 bytes, dense is 2^128 words = 2^133 bytes, R is
2^105 words, S0T is 2^24 words, plus O(1). The total is below 2^145.001
bytes, claimed as memory_log2_bytes = 145.01, reported and not scored. This is
far more than a distinguished-point walk needs, so the package is not a
Pareto improvement. preprocessing_log2 = 18: the S0T build (2^24 * 18/2140
< 2^17.11 units) is the only input-independent precomputation; it runs at the
start of every execution and is already included in T, not additional to it;
nonuniform_advice_log2_bytes = 0. baseline_improved is the required
identifier sha256-r31-nominal-v2.

## 9. Scope and relation to other work

- Method and conventions: jaazinn (35ce0758 on this track, 0a5b7ae8 on
  blake3-r2), credited as co-author. Our previous r31 package (claim 126.91)
  ported the same grouping under a stricter counting (5-op reference
  rotation, a mask after every operation, constants reloaded).
- Increments over 35ce0758 (840 -> 513 per message): the 160-bit key ending
  at e29 (the a-half of step 29 is skipped); lazy masking (L1); doubled-word
  sharing (L2); the ch/maj forms with a reused a ^ b (L3); sigma0(W13) from a
  y-only table addressed by the loop variable; a dense array holding only
  keys (so 11 ops instead of at most 21 per table step).
- A 128-bit key would give about 2^127 false matches at 3 units each, so
  five words is the minimum.
- Published 31-step SHA-256 collision attacks (Li, Liu and Wang, 2024) are
  far cheaper. This package does not use them and claims no cryptanalytic
  advance.
