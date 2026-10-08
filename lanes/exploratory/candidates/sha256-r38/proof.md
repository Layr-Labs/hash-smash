# Bit-sliced grouped birthday search for 38-round SHA-256

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2728 for
sha256-r38). Memory is a separately reported bound.

This exploratory package targets sha256-r38-prefix-v1. It is a generic
birthday search. Relative to a whole-compression search it has four exact cost
reductions, all accounted below on a 64-register 256-bit word RAM with every
load and store charged:

1. every message is 55 bytes, so the complete hash is one padded block and one
   38-round compression;
2. messages come in 2^104 groups of 2^24 that share W0..W12 and differ only in
   the 24 free bits u of W13, so rounds 0..12, seven schedule words and every
   gate whose inputs are all group constants are computed once per group;
3. the collision key is 144 bits of digest words that are already final
   before round 37, so round 37, the A half of round 36 and the upper 16
   bits of the E half of round 36 are never computed per message;
4. 256 messages are evaluated together, bit-sliced: a 256-bit register holds
   bit j of one 32-bit word for 256 messages, rotations are free renamings,
   and every modular addition is a counted Boolean adder.

One batch of 256 messages costs exactly **51276** operations, counted by
executing the emitted register-allocated program on a 64-register machine:
200.296875 operations per message, including loads, stores, the transpose to
per-message key words, the table step and batch control. The total is
T < 2^124.23380 charged units, time_log2 = **124.234**, with success probability
0.39 under one declared heuristic (H1). This is not a differential attack on
SHA-256; the improvement is a constant factor. Sources of reused ideas are
listed in Section 14.

## 1. Exact complete hash

A message is 55 bytes. FIPS 180-4 padding appends 0x80 and the 64-bit
big-endian bit length 440, with zero padding bytes (55 + 1 + 8 = 64). So the
padded input is exactly one block, with big-endian words

    W0..W12  = message bytes 0..51
    W13      = (u << 8) | 0x80,  u = message bytes 52..54 (24 bits)
    W14 = 0, W15 = 440.

Each compression executes rounds 0..37 only (indices 0 through 37
inclusive). The schedule is
W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16} (mod 2^32) for t = 16..37,
with s0(x) = ROR7 ^ ROR18 ^ SHR3 and s1(x) = ROR17 ^ ROR19 ^ SHR10. Round t
computes

    T1 = h + S1(e) + Ch(e,f,g) + K_t + W_t,   T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

with S0 = ROR2 ^ ROR13 ^ ROR22, S1 = ROR6 ^ ROR11 ^ ROR25,
Ch = (e&f)^(~e&g), Maj = (a&b)^(a&c)^(b&c), all modulo 2^32, and the standard
IV and K_t at their original indices. The digest is
H_i = IV_i + s_i (mod 2^32) in standard big-endian order, where
s = (A37, A36, A35, A34, E37, E36, E35, E34) is the working state after round
37 and A_t, E_t denote the new a and e words produced by round t. This is the
complete hash `verifier/hash_functions.py:digest(m, "sha256", 38)` on the
declared domain, not a free-start or compression-only result. A reported
collision is re-verified with two whole compressions of the reference hash.

## 2. Group constants and the message-dependent schedule

W13 is first used in round 13, so the state after rounds 0..12 is a group
constant. W13 enters the schedule at t = 20, 28 and 29, so W20, W22, W24, W26, W27, W28, W29, W30, W31, W32, W33, W34, W35, W36
depend on W13 (14 words), while W16..W19, W21, W23 and W25 are group
constants. Every dependent word is computed from its W13-dependent summands
plus one group constant P_t that pre-adds the others (for example
W20 = W13 + P20 with P20 = s1(W18) + s0(W5) + W4, and
W28 = s1(W26) + s0(W13) + P28 with P28 = W21 + W12). The other group constants
used per message are A10..A12, E11, E12, A13pre = T13 + T2(13) and
DT13pre = d + T13 (round 13 without W13, so A13 = A13pre + W13 and
E13 = DT13pre + W13), HKW_t = h + K_t + W_t for t = 14, 15, 16 (where h = E_{t-4}
is itself a group constant) and KW_t = K_t + W_t for t = 17, 18, 19, 21, 23, 25.
Additions are modulo 2^32, so regrouping summands is exact.

In the bit-sliced circuit any gate whose two inputs are group-constant planes
is not executed per batch: its output plane is computed once per group and
stored (Section 6 charges it). The circuit has 190 such gates.

## 3. The key: digest bits fixed before the last round

After round 36 the final state words c = A35, d = A34, f = E36, g = E35 and
h = E34 are fixed (round 37 only shifts them). Define the 144-bit key

    K = A35 || A34 || (E36 mod 2^16) || E35 || E34      (bits 0..143, A35 lowest).

Equal digests imply equal K. The low 16 bits of E36 = A32 + T1(36) depend only on
the low 16 bits of every summand (carries only move upward), and each of those
summands' low 16 bits is available: S1 and Ch bits j < 16 of round 36 use whole
E35, E34, E33, which are computed in full. So the circuit computes, per message, rounds
13..35 in full and only the low 16 bits of the E half of round 36. A K match is
only a candidate; it is confirmed by two complete digests (Section 7).

## 4. The bit-sliced circuit

A batch is 256 messages of one group with u = 256 b + L, L = 0..255. Plane j of a
32-bit word X is the 256-bit value whose bit L is bit j of X for message L. A
word is 32 planes. Inputs per batch: the group-constant planes (each 0 or all
ones), eight fixed lane planes (bit L of lane plane i is bit i of L; they hold
u bits 0..7, W13 bits 8..15), sixteen batch planes (all ones or zero by bit i
of b; W13 bits 16..31) and the constant 0x80 for W13 bits 0..7.

Gates are 256-bit AND, OR and XOR, one operation each. Every intermediate is
a signed literal: a stored plane plus a compile-time polarity flag, so NOT,
XOR with a constant and every rotation or shift by a constant cost nothing
(rotation renames planes; a shift renames planes and fills with the constant 0).
The rules, each an identity of Boolean algebra:

- X & Y (1), ~X & ~Y = ~(X | Y) (1), X & ~Y = (X | Y) ^ Y (2); OR by duality;
- Maj(x, y, z) is self-dual, so polarities are normalised to at most one
  complemented input; with none, maj = a ^ ((a^b) & (a^c)); with x = ~X,
  maj = (y | z) ^ ((y ^ z) & X). A full adder is sum = a ^ b ^ c and carry =
  maj(a, b, c), sharing a ^ b (or y ^ z): **5 operations**, no materialised NOT;
- a half adder is 2 operations; a constant input bit folds (x + y + 1 gives
  sum ~(x ^ y), carry x | y: 2 operations);
- Ch(e, f, g) = g ^ (e & (f ^ g)); f ^ g of round t equals e ^ f of round t-1,
  so 2 new operations per bit; Maj(a, b, c) = b ^ ((a ^ b) & (b ^ c)) with b ^ c
  shared from the previous round, 2 new operations plus a ^ b;
- every multi-operand sum modulo 2^32 is column compression: in column j,
  full adders reduce the column's bits (with carries from column j-1) to one,
  passing carries to column j+1; column 31 keeps sums only.

The circuit is emitted column by column in lock step: for each round t and bit
j it computes bit j of the dependent schedule word W_t, of T1, of E_t = d + T1
and of A_t = T1 + S0 + Maj, keeping the carry chains of all four sums open.
`build` in `experiments/bitsliced_birthday.py` is this exact generator. Its
outputs are the 144 key planes. The circuit has 34769 gates per batch
(135.82 per message) after group-constant hoisting.

## 5. Transpose to one key word per message

The table needs each message's key as one 256-bit word. Rows 0..143 of a
256 x 256 bit matrix are the key planes (a literal with polarity flag set
contributes its stored plane, so the result is K XOR pol for a fixed constant
pol: an injective relabelling of the key, harmless for collision detection).
Row 144 is the constant all-ones plane; rows 145..255 are zero. A delta-swap
transpose swaps index bit k of rows and columns for k = 0..7: for rows i and
i + 2^k (bit k of i clear) with mask m_k of columns whose bit k is clear,

    t = ((a >> 2^k) ^ b) & m_k;  b' = b ^ t;  a' = a ^ (t << 2^k)     (6 operations)

and when one row is still zero the swap needs 3 operations
(b = 0: a' = a & m_k, b' = (a >> 2^k) & m_k; a = 0: t = b & m_k, a' = t << 2^k,
b' = b ^ t). Pass 1 applies k = 0, 1, 2 to aligned groups of 8 rows, pass 2
applies k = 3..7 to the 32 rows of each residue class mod 8 and hands each
finished row (the key word of message L) to the table step. The transpose
costs 4077 operations per batch. After it, word L is
K_L XOR pol XOR 2^144, with bits 145..255 zero.

## 6. Machine, register allocation and the exact batch count

Machine: 256-bit word RAM with 64 registers, three-address operations,
immediate shift counts, and loads and stores with a register address or a
small immediate address (all planes, spill slots and constants live below
2^24; the table lives at [2^140, 2^141)). Every load and store is one
operation, as are add, subtract, AND, OR, XOR, shift, compare and branch.

The straight-line program (circuit, transpose, sinks for the table step) is
register-allocated onto registers 0..57 by furthest-next-use eviction. Each
operand not in a register is loaded; an evicted value that is used later and
is not already in memory is stored first; inputs (group-constant, hoisted,
lane, batch and mask planes) are loaded from memory at every use that misses
the registers. Registers 58..63 hold the batch id word, the loaded table
entry, two temporaries, the batch counter and a scratch value. The emitted
program uses at most 58 circuit registers.

`count_batch` executes the emitted program on a 64-register machine and
charges one operation per instruction. Per batch of 256 messages:

| Part | Operations |
| --- | ---: |
| loads | 7461 |
| stores | 2595 |
| XOR | 27320 |
| AND | 6055 |
| OR | 4112 |
| shifts (transpose) | 1359 |
| table steps, 256 x 9 | 2304 |
| batch setup: 16 batch planes x 4, batch id 3, loop 3 | 70 |
| **total per batch** | **51276** |
| per message | 200.296875 |

Gates (XOR/AND/OR/shift) are 38846 per batch: 34769 in the circuit and
4077 in the transpose. The trial-0 self-check of both experiments executes this
program for one batch, compares all 256 key words with a scalar compression,
and aborts unless the batch costs exactly 51276 operations.

Local exactness evidence (not organizer evidence): 3072 messages from random
prefixes and batch indices through the counted VM program, and 3072 through the
compiled evaluator (including batches that mix 8 groups), all bit-for-bit equal
to the key from `digest(m, "sha256", 38)` minus the IV; 0 mismatches.

## 7. Complete algorithm

Parameters: L = 2^24 messages per group, G = 2^104 groups, N = 2^128,
table T of 2^140 words at addresses 2^140 + i, never initialised. Candidate cap
V = 2^113 + 2^40 + 1.

Once: draw a uniform 256-bit word RTAG; write the 8 masks m_k, the all-ones
plane and the 8 lane planes (under 2^12 operations).

For g = 0 .. G-1:

1. Draw two uniform 256-bit words r0, r1, store them at PT[g], and unpack
   W0..W12 as in our earlier packages.
2. Group setup: the scalar group constants of Section 2, their planes
   (shift, AND 1, negate, store: 4 operations per plane), the hoisted gate
   planes (2 loads, 1 gate, 1 store each) and GTAG = (g << 152) XOR RTAG.
   At most 2^13 operations.
3. For b = 0 .. 2^16 - 1: write the 16 batch planes, set
   BID = (b << 136) XOR GTAG, run the counted batch program, and for each
   message L, when its key word Kw is produced:

        idx = Kw >> 4                      # 2^140 + (key bits 4..143)
        e = load T[idx]
        x = Kw ^ BID
        if ((x ^ e) << 128) == 0: CONFIRM  # key bits 0..127 of the difference
        store T[idx] = x ^ (L << 128)      # id = (g, b, L) in bits 128..255 (XOR RTAG)

   The entry of message (g, b, L) is (K XOR pol XOR 2^144) XOR (id << 128) XOR RTAG
   with id = g·2^24 + b·2^8 + L. Bits 128..144 of the key word are index bits
   (bit 144 is the constant), so a later message in the same slot knows them.

4. CONFIRM: increment a counter v; if v > V halt with failure. Recover the
   occupant's id as ((e ^ Kw ^ RTAG) >> 128), its group g' = id >> 24 and
   u' = id mod 2^24, rebuild both 55-byte messages from PT, check that they
   differ, compute both complete reference digests and compare all eight
   words. If equal, output the pair and halt; otherwise continue with the
   store above.

If the loops finish, halt with failure.

## 8. Correctness

Every evaluated message is a 55-byte string in the domain. The batch program
computes K XOR pol XOR 2^144 exactly (Sections 3-6; it is straight-line code made
of the Boolean identities listed, checked on every lane of the trial-0 batch by
the organizer-run experiments and on the local samples above).

If a later message j finds in its slot the entry written by an earlier message
i with K_i = K_j, then bits 4..144 of the two key words agree (same slot) and bits
0..127 agree (the test), so the full keys agree, the test passes, and
e ^ Kw_j ^ RTAG = id_i << 128 exactly: CONFIRM rebuilds message i correctly.
CONFIRM accepts only after two complete reference digests agree on distinct
messages, so every output is an ordinary full 256-bit collision of complete
38-round SHA-256. A slot never written in the run may hold anything; a wrong
candidate from it is rejected by CONFIRM (any decoded id names some 55-byte
message, possibly from an uninitialised PT entry, and is just compared).

## 9. Success probability

The coins are r0, r1 per group and RTAG. Failure requires one of:

- F1: no two of the N messages have equal digests;
- F2: some digest-colliding pair (i < j) where, when j probes, the slot of i
  holds the entry of some k with i < k < j and idx(k) = idx(i) (overwrite);
- F3: two groups draw identical 416-bit prefixes, probability below 2^-209;
- F4: more than V candidates.

Heuristic H1 treats the N digests (and their key projections) as independent
uniform values for F1, F2 and the genuine part of F4. Then
Pr[F1] <= exp(-N(N-1)/2^257) < 0.606531. For F2, the expected number of triples
(k, i, j) with idx(k) = idx(i) and equal digests for (i, j) is at most
N^3 2^-140 2^-256 / 2 = 2^-13.

Candidates are of two kinds. Garbage candidates come from slots not written in
the run. For fixed prefixes, the keys and the set of written slots do not
depend on RTAG, and the test compares bits 0..127 of (e ^ K ^ RTAG) with zero for
a fixed e, so each message is a garbage candidate with probability 2^-128 over
RTAG: at most 1 expected, and more than 2^40 with probability at most 2^-40
(Markov), without H1. Genuine false candidates need an earlier entry with the
same 144-bit key but a different digest. Under H1, given the history, message
j's key is uniform, so this has probability at most (written slots)/2^144 <=
2^-16 for every j; the count is dominated by a Binomial(N, 2^-16) variable with
mean 2^112, and exceeds 2^113 with probability below exp(-2^112/3). At most one
candidate is a true collision (the run halts). Hence Pr[F4] < 2^-40 + 2^-1000.

    Pr[success] >= 1 - 0.606531 - 2^-13 - 2^-209 - 2^-40 - 2^-1000 > 0.39334.

The claim is 0.39, keeping a 0.0033 allowance for deviation from the model,
as in our earlier packages. Cross-group pairs with the same u collide with
probability >= 2^-256 for any fixed function (Cauchy-Schwarz over uniform
prefixes); within-group pairs are a 2^-104 fraction of all pairs.

## 10. Charged time

    T <= N * 51276 / (256 * 2728)                       (all batches)
       + G * 2^13 / 2728                                       (group setup)
       + V * (2 + 2^10 / 2728)                                 (confirmations)
       + 2^12 / 2728                                           (global setup)
       = 2^124.23237 + 2^105.59 + 2^114.25 + 2

so T < 2^124.23380 and the claim is time_log2 = 124.234. This caps every run:
it includes all random draws, failed and discarded messages, loads and stores,
transposes, table work, confirmations, verification and setup. The two whole
compressions per confirmation are charged at one unit each; everything else is
charged per word operation.

## 11. Memory and other resources

T: 2^140 words of 32 bytes = 2^145 bytes. PT: 2^104 * 64 bytes = 2^110 bytes.
Planes, spill slots, constants and code are under 2^24 bytes. Peak below
2^146 bytes; memory_log2_bytes = 146. T is never initialised and costs no
time. preprocessing_log2 = 0. There is no nonuniform advice.

## 12. Sensitivity

Same circuit and transpose, re-allocated and re-executed on the machine
(main term plus the same setup and confirmation terms):

| Variation | ops per message | bound |
| --- | ---: | ---: |
| As claimed: 64 registers | 200.30 | 2^124.23380 |
| 48 registers | 204.56 | 2^124.265 |
| 32 registers | 211.47 | 2^124.313 |
| Unbounded registers (loads and stores free; lower reference) | 161.02 | 2^123.920 |
| One extra store charged after every gate | 352.04 | 2^125.047 |
| Our scalar package for this track (no bit-slicing) | 1280 | 2^126.909 |

The claim rests on the 64-register machine with every load and store charged,
the convention our earlier packages and the current pending SWAR package on
this track use. The 32-register line shows how much depends on register count.

## 13. Evidence

Experiments s256-bs-spread (16 groups x 32 consecutive u) and
s256-bs-single-group (1 group x 512 consecutive u) run the bit-sliced circuit
with N_t = 512 = 2^(18/2) messages per organizer seed against an 18-bit masked
event on digest bits that only the circuit computes (H2, H3, H5 bits 0..15, H6,
H7). N_t^2/2^18 = 1 = N^2/2^256, so this is the exact scaled analogue of the full
attack. The organizer recomputes every returned pair with the trusted digest,
which checks the circuit on genuine messages, and trial 0 checks the counted
program (Section 6). Random-model success per trial is
1 - prod_{i<512}(1 - i/2^18) = 0.39307; untrusted observations report masked-equal
pair counts (expected 0.4990 per trial).

Local replay with locally chosen seeds (not organizer evidence), every returned
pair re-checked with `digest(m, "sha256", 38)` under the mask (0 rejected): the
spread layout over 4096 trials gave 1670 successes (model 1610.0,
z = +1.92) and 2148 masked pairs (expected 2044.0); 113 first matches were within a
group (expected about 101). The single-group layout over 4096 trials gave
1661 successes (model 1610.0, z = +1.63) and 2116 masked pairs (expected 2044.0).
Across the four layouts run for r37 and r38 the largest deviation is |z| = 1.95
(two-sided p about 0.05 for one test, not significant after a Bonferroni
correction for four); three of the four deviations are excesses of successes.
The runs were not repeated or extended after seeing the results.
Each request reported batch_ops = 51276 from its trial-0 self-check. One
256-trial request took at most 4.35 s locally.

## 14. Sources and limitations

Reused with credit (public notes on this track, read before this design; no
code was copied): the bit-sliced SHA-256 circuit with 256 messages per batch,
free rotations, NOT-free polarity-aware majority and the delta-swap transpose
to per-message key words (mitchuski's sha256-r38 bit-sliced package, which
credits earlier sha3-256-r6 work for the transpose); the key on digest words
fixed before the last round and skipping the A half of the round before it,
and the uninitialised table whose entries carry a per-run random tag with a
deterministic candidate cap (jungjipdo's sha256-r38 SWAR package). Our own: the
grouped single-block family and its group constants (our r31/r32 packages
and our scalar r38 port), the column-lockstep circuit and group-gate hoisting,
the 16-bit truncation of f, the explicit register allocation counted on a
64-register machine with all loads and stores, the zero-aware transpose with
a constant row that places the table above 2^140, the 9-operation table step
that stores the id in the index-covered bits, and the analysis above.

H1 is a heuristic, tested on masked 18-bit projections, not the full event.
Organizer seeds are public. The register machine is a modelling assumption;
Section 12 gives alternatives. This is a constant-factor improvement, not a
cryptanalytic weakness of SHA-256 and not a Pareto improvement (memory is very
large). The nominal reference identifier sha256-r38-nominal-v2 is metadata, not
a claimed improvement over a qualified baseline.
