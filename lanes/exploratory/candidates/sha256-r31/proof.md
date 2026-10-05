# Grouped early-abort birthday search for 31-round SHA-256 (C=2140 ledger)

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2140 for
sha256-r31). Memory is a separately reported bound.

This exploratory package targets sha256-r31-prefix-v1. It is a generic
birthday search with three exact cost reductions:

1. every message is 55 bytes, so the complete hash is one padded block and one
   31-round compression;
2. messages come in 2^104 groups of 2^24 that share message words W0..W12 and
   differ only in the 24 free bits of W13, so rounds 0..12, seven schedule
   words and most of round 13 are computed once per group;
3. collisions are detected on the 192-bit partial state after round 29,
   so round 30 and the feed-forward are skipped for every message, and full
   digests are computed only to confirm candidate matches.

## Ledger premise (difference from public 126.651)

Public submission `35ce075` (commit `27a7d5d`, solver jaazinn) published the
same algorithm family with an inner body of 798 operations under a cheaper
Word convention (4-op rotate of already-reduced words; Maj =
`(a&(b|c))|(b&c)`; white-box whole compression priced at 1770). That mixes
yardsticks with organizer C = 2140 = 15×30 + 31×54 + 16.

This package **rejects that yardstick**. Every white-box operation is priced
with the **same** convention that yields C = 2140:

- narrow rotate = organizer `_ror` / `_rol` = 5 Word ops (`&MASK`, `>>`, `<<`,
  `|`, `&MASK`);
- Maj = reference `(a&b)^(a&c)^(b&c)` = 5 ops (round-14 may use the algebraic
  shortcut with precomputed `b|c` and `b&c`, which only reduces live ops);
- `t1` and `t2` take an `&MASK` as in `verifier/hash_functions.py:_compress`.

Independently instrumented with the organizer `Word` counter from
`scripts/reference_operation_costs.py`:

| quantity | value |
| --- | ---: |
| inner body (this convention) | **953** |
| pack K + id + sparse-set + loop | ≤ 35 |
| counted per message | ≤ 988 |
| **charged per message** | **1000** |
| N | 2^128 |
| T | < 0.46729 · 2^128 < 2^126.9024 |
| claimed `time_log2` | **126.91** |
| success probability | 0.39 under H1 (model > 0.3933) |
| memory_log2_bytes | 146 |

The algorithm family is credited to the public work above; the proof, ledger,
experiments and claim numbers below are an independent rewrite.

## 1. Exact complete hash

A message is 55 bytes. FIPS 180-4 padding appends 0x80 and the 64-bit
big-endian bit length 440, with zero padding bytes (55 + 1 + 8 = 64). So the
padded input is exactly one block, with big-endian words

    W0..W12  = message bytes 0..51
    W13      = (u << 8) | 0x80,  u = message bytes 52..54 (24 bits)
    W14 = 0, W15 = 440.

Each compression executes rounds 0..30 only. The schedule is
W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16} (mod 2^32) for t = 16..30,
with s0(x) = ROR7 ^ ROR18 ^ SHR3 and s1(x) = ROR17 ^ ROR19 ^ SHR10. Round t
computes

    T1 = h + S1(e) + Ch(e,f,g) + K_t + W_t,   T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

with S0 = ROR2 ^ ROR13 ^ ROR22, S1 = ROR6 ^ ROR11 ^ ROR25,
Ch = (e&f)^(~e&g), Maj = (a&b)^(a&c)^(b&c), all modulo 2^32, and the standard
IV and K_t at their original indices. The digest is
H_i = IV_i + s_i (mod 2^32) in standard big-endian order, where
s = (A30, A29, A28, A27, E30, E29, E28, E27) is the working state after round
30 and A_t, E_t denote the new a and e words produced by round t. This is the
complete hash `verifier/hash_functions.py:digest(m, "sha256", 31)` on the
declared domain, not a free-start or compression-only result. The final
collision is re-verified with two whole compressions of the reference hash.

Since H_i = IV_i + s_i with a fixed IV, two messages have equal digests if and
only if their final working states are equal.

## 2. Where W13 enters (dependency lemma)

W13 is first used in round 13, so the state after rounds 0..12 is a group
constant. Its direct schedule uses are t = 20 (W_{t-7}), 28 (W_{t-15}) and 29
(W_{t-16}). Through the recurrence, the dependent expanded words are exactly

    depend on W13:  20, 22, 24, 26, 27, 28, 29, 30
    independent:    16, 17, 18, 19, 21, 23, 25

Verified by flipping one bit of W13 and expanding W16..W30 (exact match).
Those seven independent words are group constants.

### Round-13 reduction

In round 13, every input except W13 is a group constant. With
T13 = h + S1(e) + Ch(e,f,g) + K13 and A13 = T13 + S0(a) + Maj(a,b,c), both
precomputed unreduced, the round is

    a' = (A13 + W13) & M,   e' = (d + T13 + W13) & M          (4 operations)

and correctness follows from (x + y) mod 2^32 = ((x mod 2^32) + y) mod 2^32.

### Round-14 Maj shortcut

After round 13 the state is (a', a12, b12, c12, e', e12, f12, g12). Round 14's
Maj(a', a12, b12) equals `(a' & (a12|b12)) | (a12&b12)` with `a12|b12` and
`a12&b12` precomputed. Algebraically identical to the reference 5-op Maj.

### Pre-added schedule identities (P20..P29)

Every dependent schedule word keeps its group-invariant summands pre-added.
The identities used by the inner body are:

    W20 = (P20 + W13) & M                 P20 = s1(W18) + s0(W5) + W4
    W22 = (s1(W20) + P22) & M             P22 = W15 + s0(W7) + W6
    W24 = (s1(W22) + P24) & M             P24 = W17 + s0(W9) + W8
    W26 = (s1(W24) + P26) & M             P26 = W19 + s0(W11) + W10
    W27 = (W20 + P27) & M                 P27 = s1(W25) + s0(W12) + W11
    W28 = (s1(W26) + s0(W13) + P28) & M   P28 = W21 + W12
    W29 = (s1(W27) + W22 + W13 + P29) & M P29 = s0(W14) = s0(0) = 0

Each follows from the standard expansion by collecting summands that do not
depend on W13. Rounds 14..19, 21, 23 and 25 use precomputed K_t + W_t.

Correctness of the grouped evaluator against the reference digest was checked
on 3000 random (prefix, u) pairs: the six words H1,H2,H3,H5,H6,H7 matched
bit-for-bit (3000/3000).

## 3. Early abort after round 29

After round 29 the working state is (A29, A28, A27, A26, E29, E28, E27, E26).
Round 30 only produces new A30, E30 and shifts the others, so the final state
is (A30, A29, A28, A27, E30, E29, E28, E27). Digest equality (fixed IV)
therefore implies equality of (A29, A28, A27, E29, E28, E27). Define the
192-bit key

    K = A29 || A28 || A27 || E29 || E28 || E27.

Equal digests imply equal K. The search stores and compares K and never
computes round 30, W30 or the feed-forward on the search path. A K match is
only a candidate; it is confirmed by computing both complete digests.

## 4. Operation counts under the C=2140 convention

Counting convention: one operation per 256-bit add, AND, OR, XOR, NOT or
shift, as in `scripts/reference_operation_costs.py`. A narrow rotation is the
organizer `_ror` (5 ops). One reference round with K+W already summed into
`kw` costs 53; with the K+W add it costs 54. One schedule expansion costs 30.
Whole CF31 = 15×30 + 31×54 + 16 = 2140.

### Inner-body breakdown (independent Word instrumentation)

| segment | ops |
| --- | ---: |
| form W13 = (u<<8)\|0x80 | 2 |
| round 13 (two adds + two masks) | 4 |
| round 14 (S1+Ch+S0+shortcut Maj+masks) | 50 |
| rounds 15..19 (5 × 53) | 265 |
| W20 + rounds 20..21 | 109 |
| W22 + rounds 22..23 | 122 |
| W24 + rounds 24..25 | 122 |
| W26 + round 26 | 69 |
| W27 + round 27 | 56 |
| W28 + round 28 | 83 |
| W29 + round 29 | 71 |
| **inner total** | **953** |

Group setup (rounds 0..12, seven independent schedule words, T13/A13/D13,
round-14 precomputations, nine K_t+W_t sums, P20..P29) is under 1100 Word
ops once per group and is charged in the per-group overhead below.

## 5. Complete algorithm

Parameters: L = 2^24 messages per group, G = 2^104 groups, N = G·L = 2^128,
sparse index width s = 140, verification cap V_max = 2^90.

Memory: prefix table PT (two 256-bit words per group), record array R of
(K, id) pairs (at most N records), and a sparse array P of 2^s one-word
entries. P is never initialised; R is written before it is read; n counts
records.

For g = 0 .. G-1:

1. Draw two fresh independent uniform 256-bit words r0, r1 and store them at
   PT[g]. Unpack W0..W12 from them.
2. Run group setup. Set Gid = g << 24.
3. For u = 0 .. 2^24 - 1: run the 953-operation inner body, pack
   K = A29<<160 | A28<<128 | A27<<96 | E29<<64 | E28<<32 | E27 (10 ops),
   set id = Gid | u, then run one Briggs–Torczon sparse-set step indexed by
   the top s = 140 bits of K (at most 21 ops: address arithmetic, 2 loads,
   3 stores, 3 compares, 3 branches). Loop control is 3 ops. On an equal
   key, go to CONFIRM; otherwise continue.
4. CONFIRM: increment confirmation counter v; if v > V_max halt with failure.
   Decode both ids, rebuild both 55-byte messages from PT, check they differ,
   compute both complete reference digests (two whole compressions) and
   compare all eight words. If equal, output the pair and halt; otherwise
   discard the current message and continue.

If the loops finish, halt with failure.

## 6. Sparse-set correctness

Invariant (Briggs–Torczon): P may hold arbitrary values; R[0..n-1] are
genuine records. A slot `idx` is occupied iff P[idx] = r < n and
(R[r].key >> (192-s)) = idx. Inserts only fill unoccupied slots; an occupied
slot is never overwritten, so it holds the first stored record with that
index.

Lemma. If record i is stored and a later message j has the same digest, then
K_j = K_i and idx(j) = idx(i), so CONFIRM runs on (i, j) at j unless the run
already ended. CONFIRM accepts exactly when the two complete reference
digests agree and the messages differ. Every output is therefore an ordinary
full 256-bit collision of complete 31-round SHA-256.

A record i is not stored only if, when it arrived, its slot held a record k
with idx(k) = idx(i) and K_k ≠ K_i, or a record with K_k = K_i but a
different digest (a rejected candidate).

## 7. Success probability

The coins are the 2G words r0, r1. Failure requires one of:

- F1: no two of the N messages have equal digests;
- F2: some digest-colliding pair (i < j) has i unstored, because an earlier k
  had idx(k) = idx(i) with K_k ≠ K_i, or K_k = K_i with a different digest;
- F3: two groups draw identical 416-bit prefixes, with probability at most
  C(G,2)·2^-416 < 2^-209;
- F4: more than V_max candidate confirmations.

Heuristic H1 treats the N digests (and their K projections) as independent
uniform values for these events. Then
Pr[F1] ≤ exp(-N(N-1)/2^257) < 0.606531. For F2, the expected number of
triples (k, i, j) with k < i, j ≠ i, idx(k) = idx(i) and equal digests
(i, j) is at most N^3 · 2^-s · 2^-256 / 2 = 2^(127-s) = 2^-13. Each message
causes at most one confirmation against the single occupant of its slot, and
a non-colliding occupant has an equal K with probability 2^-192. So the
expected number of confirmations is at most N^2 · 2^-192 = 2^64, and
Pr[F4] ≤ 2^64 / V_max = 2^-26 by Markov. Hence

    Pr[success] ≥ 1 - 0.606531 - 2^-13 - 2^-26 - 2^-209 > 0.39334.

The claim is 0.39, keeping a 0.0033 allowance for deviation from the model.
The value is algorithmic success probability over the coins, not confidence
in H1. Cross-group pairs with the same u collide with probability ≥ 2^-256
for any fixed function (Cauchy–Schwarz over uniform prefixes). Within-group
pairs are a 2^-104 fraction of all pairs.

## 8. Charged time

Per message, worst-case path (insert after the full slot check):

| Work | Operations |
| --- | ---: |
| inner body (Section 4) | 953 |
| pack K | 10 |
| id = Gid OR u | 1 |
| table step | 21 |
| loop: u+1, compare, branch | 3 |
| counted total | 988 |
| **charged** | **1000** |

Machine: 256-bit word RAM with 64 registers, three-address operations and
immediate shift counts. Registers hold MASK, 0x80, the group constants
(T13/A13/D13, round-14 precomputes, nine K_t+W_t, P20..P29), the seven live
round constants K20/K22/K24/K26..K29, eight working-state words, at most six
live dependent schedule words, a handful of temporaries and the loop/table
registers — under 64 in total. Section 10 charges a full reload alternative.

Per group (G = 2^104 times), at most 2048 operations are charged: 2 random
draws, unpacking, PT store, setup (< 1100), Gid, u reset and loop control.
Once: global setup ≤ 2^12. Confirmations: ≤ V_max = 2^90, each ≤ two whole
compressions plus 2^10 ordinary ops.

    T ≤ N·1000/2140 + G·2048/2140 + V_max·(2 + 2^10/2140) + 2^12/2140
      = 2^128 · 0.467289776... + 2^103.94 + 2^91.3 + 2
      < 0.46729 · 2^128.

log2(0.46729) ≈ -1.09761, so T < 2^126.9024 and the claim is
time_log2 = 126.91. This caps every run. It includes random draws, failed
and discarded messages, table work, confirmations, verification and setup.
The two whole compressions per confirmation are charged at one unit each;
everything else, including all partial evaluations, is charged per word
operation at 1/2140. Nothing is charged twice or omitted.

## 9. Memory and other resources

P: 2^140 words of 32 bytes = 2^145 bytes. R: at most 2^128 records of 64
bytes = 2^134 bytes. PT: 2^104 · 64 bytes = 2^110 bytes. Code and constants
are under 2^24 bytes. Peak < 2^146 bytes; memory_log2_bytes = 146. P is never
initialised and costs no time. preprocessing_log2 = 0 covers global setup.
There is no nonuniform advice. Memory is unscored under v5 and rules out any
Pareto claim.

## 10. Sensitivity and register micro-audit

| Variation | Bound |
| --- | ---: |
| As claimed (1000 per message) | 2^126.9024 |
| Counted 988 without margin | 2^126.8850 |
| All group/round constants reloaded per message (+33 loads → 1021) | 2^126.932 |
| Reject amortisation; charge one whole CF31 per message | ≈ 2^128.02 |
| Public 35ce075 yardstick (840 / cheaper convention) — **not used** | 2^126.651 |

Register micro-audit: the live set listed in Section 8 fits in 64 registers
without spilling under the modelling assumption of immediate shift counts and
three-address ops. If review requires treating every group constant as a
memory load each message, the reload row still beats 128. If review rejects
partial evaluation entirely, the package is no better than a whole-compression
birthday and should lose to the validating pad-preserving VOW at 128.00463.

## 11. Evidence

Experiments `r31-grouped-spread` (16 groups × 32 consecutive u) and
`r31-single-group` (1 group × 512 consecutive u) run the exact grouped
evaluator with N_t = 512 = 2^(18/2) messages per organizer seed, against an
18-bit masked event on digest words H1, H2, H3, H5, H6 and H7. N_t^2/2^18 =
1 = N^2/2^256, so this is the exact scaled analogue of the full attack. The
program computes those six digest words only through the grouped evaluator
(IV plus the after-round-29 state). The organizer recomputes every returned
pair with the trusted digest, which checks the body on genuine messages.
Random-model success per trial is 1 - ∏_{i<512}(1 - i/2^18) = 0.39307;
untrusted observations report masked-equal pair counts (expected ≈ 0.499
per trial).

Local bit-match (author seeds, not organizer evidence): 3000/3000 agreement
on H1,H2,H3,H5,H6,H7 between the grouped evaluator and
`verifier.hash_functions.digest(..., "sha256", 31)`.

## 12. Limitations

H1 is a heuristic, tested on masked 18-bit projections, not the full event.
Organizer seeds are public. The register machine is a modelling assumption;
Section 10 gives alternatives. This is a constant-factor improvement from
single-block messages, amortised group-invariant work and early abort. It is
not a cryptanalytic weakness of SHA-256 and not a Pareto improvement (memory
is very large). The nominal reference identifier sha256-r31-nominal-v2 is
metadata, not a claimed improvement over a qualified baseline.

Relative to public 35ce075: we keep the algorithm family and deliberately
raise the per-message charge from 840 to 1000 under the C=2140 convention,
producing 126.91 instead of 126.651. The higher scalar is the honest price of
yardstick consistency.
