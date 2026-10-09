# Bit-sliced grouped birthday search for 37-round SHA-256

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2644 for
sha256-r37). Memory is a separately reported bound.

This exploratory package targets sha256-r37-prefix-v1. It is a generic
birthday search. Relative to a whole-compression search it has four exact cost
reductions, all accounted below on a 64-register 256-bit word RAM with every
load and store charged:

1. every message is 55 bytes, so the complete hash is one padded block and one
   37-round compression;
2. messages come in 2^104 groups of 2^24 that share W0..W12 and differ only in
   the 24 free bits u of W13, so rounds 0..12, seven schedule words and every
   gate whose inputs are all group constants are computed once per group;
3. the collision key is 144 bits of digest words that are already final
   before round 36, so round 36, the A half of round 35 and the upper 16
   bits of the E half of round 35 are never computed per message;
4. 256 messages are evaluated together, bit-sliced: a 256-bit register holds
   bit j of one 32-bit word for 256 messages, rotations are free renamings,
   and every modular addition is a counted Boolean adder.

One batch of 256 messages costs exactly **45518** operations, counted by
executing the emitted register-allocated program on a 64-register machine:
177.804688 operations per message, including loads, stores, the transpose to
per-message key words, the table step and batch control. The total is
T < 2^124.10721 charged units, time_log2 = **124.10721**, with success
probability 0.39 under one declared heuristic (H1). This is not a differential
attack on SHA-256; the improvement is a constant factor.

This package is Th0rgal's 64bca7e2 (46384 operations per batch, 124.135) with
four exact changes to the counted program and nothing else; the circuit
generator, the message family, the key and the scaled experiments are
unchanged (Section 15 lists the changes and their measured effect). Sources of
reused ideas are listed in Section 14.

## 1. Exact complete hash

A message is 55 bytes. FIPS 180-4 padding appends 0x80 and the 64-bit
big-endian bit length 440, with zero padding bytes (55 + 1 + 8 = 64). So the
padded input is exactly one block, with big-endian words

    W0..W12  = message bytes 0..51
    W13      = (u << 8) | 0x80,  u = message bytes 52..54 (24 bits)
    W14 = 0, W15 = 440.

Each compression executes rounds 0..36 only (indices 0 through 36
inclusive). The schedule is
W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16} (mod 2^32) for t = 16..36,
with s0(x) = ROR7 ^ ROR18 ^ SHR3 and s1(x) = ROR17 ^ ROR19 ^ SHR10. Round t
computes

    T1 = h + S1(e) + Ch(e,f,g) + K_t + W_t,   T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

with S0 = ROR2 ^ ROR13 ^ ROR22, S1 = ROR6 ^ ROR11 ^ ROR25,
Ch = (e&f)^(~e&g), Maj = (a&b)^(a&c)^(b&c), all modulo 2^32, and the standard
IV and K_t at their original indices. The digest is
H_i = IV_i + s_i (mod 2^32) in standard big-endian order, where
s = (A36, A35, A34, A33, E36, E35, E34, E33) is the working state after round
36 and A_t, E_t denote the new a and e words produced by round t. This is the
complete hash `verifier/hash_functions.py:digest(m, "sha256", 37)` on the
declared domain, not a free-start or compression-only result. A reported
collision is re-verified with two whole compressions of the reference hash.

## 2. Group constants and the message-dependent schedule

W13 is first used in round 13, so the state after rounds 0..12 is a group
constant. W13 enters the schedule at t = 20, 28 and 29, so W20, W22, W24, W26,
W27, W28, W29, W30, W31, W32, W33, W34, W35 depend on W13 (13 words), while
W16..W19, W21, W23 and W25 are group constants. Every dependent word is
computed from its W13-dependent summands plus one group constant P_t that
pre-adds the others (for example W20 = W13 + P20 with P20 = s1(W18) + s0(W5) + W4,
and W28 = s1(W26) + s0(W13) + P28 with P28 = W21 + W12). The other group
constants used per message are A10..A12, E11, E12, A13pre = T13 + T2(13) and
DT13pre = d + T13 (round 13 without W13, so A13 = A13pre + W13 and
E13 = DT13pre + W13), HKW_t = h + K_t + W_t for t = 14, 15, 16 (where h = E_{t-4}
is itself a group constant) and KW_t = K_t + W_t for t = 17, 18, 19, 21, 23, 25.
Additions are modulo 2^32, so regrouping summands is exact.

In the bit-sliced circuit any gate whose two inputs are group-constant planes
is not executed per batch: its output plane is computed once per group and
stored (Section 7 charges it). The circuit has 182 such gates.

## 3. The key: digest bits fixed before the last round

After round 35 the final state words c = A34, d = A33, f = E35, g = E34 and
h = E33 are fixed (round 36 only shifts them). Define the 144-bit key

    K = A34 || A33 || (E35 mod 2^16) || E34 || E33      (bits 0..143, A34 lowest).

Equal digests imply equal K. The low 16 bits of E35 = A31 + T1(35) depend only on
the low 16 bits of every summand (carries only move upward), and each of those
summands' low 16 bits is available: S1 and Ch bits j < 16 of round 35 use whole
E34, E33, E32, which are computed in full. So the circuit computes, per message,
rounds 13..34 in full and only the low 16 bits of the E half of round 35. A K
match is only a candidate; it is confirmed by two complete digests (Section 7).

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

- X & Y (1), ~X & ~Y = ~(X | Y) (1), X & ~Y = (X ^ Y) & X (2, and the node
  X ^ Y is shared with any other use of X ^ Y, so it costs 1 new gate when that
  XOR is also needed); OR by duality;
- Ch(e, f, g) is always 3 gates (2 new gates when d = f ^ g is reused from the
  previous round) across all four polarities of e and d = f ^ g:
  g ^ (E & D) when e = E, d = D; f ^ (E & D) when e = ~E, d = D;
  ~(f ^ (E | D)) when e = E, d = ~D; ~(g ^ (E | D)) when e = ~E, d = ~D;
- Maj(a, b, c) = b ^ ((a ^ b) & (b ^ c)) is always 3 new gates (reusing b ^ c
  from the previous round) across all four polarities of d1 = a ^ b and d2 = b ^ c:
  b ^ (D1 & D2), ~(b ^ (D1 | D2)), ~(c ^ (D1 | D2)) or ~(a ^ (D1 | D2));
- A full adder on (a, b, c) computes t = a ^ b, sum = t ^ c, and carry = Ch(t, c, a)
  when t = (T, 0) or Ch((T, 0), a, c) when t = (T, 1), always sharing T = A ^ B
  between sum and carry: **5 operations** in all polarity cases, no materialised NOT;
- a half adder is 2 operations in every polarity case: carry a & b, sum a ^ b,
  and when a and b have opposite polarities the carry X & ~Y = (X ^ Y) & X
  reuses the sum's XOR node; a constant input bit folds (x + y + 1 gives
  sum ~(x ^ y), carry x | y: 2 operations, again sharing X ^ Y when the
  polarities differ);
- every multi-operand sum modulo 2^32 is column compression: in column j,
  full adders reduce the column's bits (with carries from column j-1) to one,
  passing carries to column j+1; column 31 keeps sums only. In round 35, the
  summands of W35, T1(35) and d = A31 are compressed in a single 16-bit column
  adder for E35 mod 2^16.

The circuit is emitted column by column in lock step: for each round t and bit
j it computes bit j of the dependent schedule word W_t, of T1, of E_t = d + T1
and of A_t = T1 + S0 + Maj, keeping the carry chains of all four sums open.
`build` in `experiments/bitsliced_birthday.py` is this exact generator. Its
outputs are the 144 key planes. The circuit has 30259 gates per batch
(118.20 per message) after group-constant hoisting.

## 5. Transpose to one key word per message

The table needs each message's key as one 256-bit word. Row r of a 256 x 256
bit matrix becomes bit r of every key word. The rows are:

- rows 111..250: key bits 4..143 (row = 107 + bit); rows 251..254: key bits
  0..3. A literal with polarity flag set contributes its stored plane, so the
  key part of every word is K XOR pol for a fixed constant pol (an injective
  relabelling of the key, harmless for collision detection);
- row 255: the constant all-ones plane;
- rows 96..103: the eight lane planes, so bits 96..103 of word L are L;
- every other row is zero.

A delta-swap transpose swaps index bit k of rows and columns for k = 0..7: for
rows i and i + 2^k (bit k of i clear) with mask m_k of columns whose bit k is
clear,

    t = ((a >> 2^k) ^ b) & m_k;  b' = b ^ t;  a' = a ^ (t << 2^k)     (6 operations)

and when one row is still zero the swap needs 3 operations
(b = 0: a' = a & m_k, b' = (a >> 2^k) & m_k; a = 0: t = b & m_k, a' = t << 2^k,
b' = b ^ t). Pass 1 applies k = 0, 1, 2 to aligned groups of 8 rows, pass 2
applies k = 3..7 to the 32 rows of each residue class mod 8 and hands each
finished row (the key word of message L) to the table step. A swap operation
whose operands are all global constants (the masks, the all-ones plane, the
lane planes, or outputs of such operations) has the same value in every batch
of every group: those 80 operations are executed once in global setup and their
outputs are stored as constant planes (Section 7). The per-batch transpose
costs 4093 operations. After it, word L is

    Kw_L = 2^255 + sum over key bits (K XOR pol) at rows 251..254 and 111..250
           + L * 2^96,

with every other bit zero, so Kw_L >> 111 lies in [2^144, 2^145) and is an
injective function of K alone, and bits 0..127 of Kw_L are key bits 4..20
(rows 111..127, also determined by K) and L.

The lane rows were placed at 96..103 because, of all aligned positions tried
(every contiguous block of 8 rows in 0..110, and strided placements), this one
adds the fewest transpose operations (16 more than without lane rows), while
the per-message lane-id XOR it replaces costs 256 per batch.

## 6. Machine, register allocation and the exact batch count

Machine: 256-bit word RAM with 64 registers, three-address operations,
immediate shift counts, add or XOR with a small immediate, and loads and stores
with a register address or a small immediate address (all planes, spill slots
and constants live below 2^24; the table lives at [2^144, 2^145); PT at
[2^160, 2^160 + 2^105)). Every load and store is one operation, as are add,
subtract, AND, OR, XOR, shift, compare and branch.

The straight-line program (circuit, transpose, sinks for the table step) is
register-allocated onto all 64 registers by furthest-next-use eviction. At
batch start the 16 batch planes are in registers 0..15 and the batch id word
BID (Section 7) is in register 63. BID and the constant plane 2^128 are
ordinary allocated values: an operand not in a register is loaded; an evicted
value that is used later and is not already in memory is stored first (BID is
stored once if it is evicted during the circuit); inputs (group-constant,
hoisted, lane, mask and precomputed transpose planes) are loaded from memory at
every use that misses the registers. Each table step reads the key word, BID
and 2^128 and takes two temporaries from the free registers, evicting if
needed; the key word's own register then holds the entry. The last instruction
of the batch reads BID and writes BID + 1 into register 63.

`count_batch` executes the emitted program on a 64-register machine and
charges one operation per instruction. Per batch of 256 messages:

| Part | Operations |
| --- | ---: |
| loads | 6847 |
| stores | 2475 |
| XOR | 26115 |
| AND | 4141 |
| OR | 2737 |
| shifts (transpose) | 1359 |
| table steps, 256 x 7 | 1792 |
| batch setup: 16 batch planes x 3 | 48 |
| loop: BID + 1, load limit, compare, branch | 4 |
| **total per batch** | **45518** |
| per message | 177.804688 |

Gates (XOR/AND/OR/shift) are 34352 per batch: 30259 in the circuit and
4093 in the transpose. The trial-0 self-check of both experiments executes this
program for one batch with seed-derived group number and run tag, compares all
256 key words with a scalar compression, checks that bits 96..103 of word L
equal L and bit 255 is set, checks that register 63 ends holding the next
batch id word, and aborts unless the batch costs exactly 45518 operations.

Local exactness evidence (not organizer evidence): 2048 messages from random
prefixes, batch indices, group numbers and run tags through the counted VM
program (8 batches, each costing 45518), and 3072 through the compiled
evaluator in batches that mix 8 groups with random u, all bit-for-bit equal to
the key read from `digest(m, "sha256", 37)` minus the IV; 0 mismatches.

## 7. Complete algorithm

Parameters: L = 2^24 messages per group, G = 2^104 groups, N = 2^128,
table T of 2^144 words at addresses 2^144 + i, never initialised. Candidate cap
V = 2^113 + 2^40 + 1.

Once: draw a uniform 256-bit word and keep its upper half as the 128-bit run
tag RTAG; write the 8 masks m_k, the all-ones plane, the 8 lane planes, the
plane 2^128 and the 80 precomputed transpose planes (under 2^12 operations).

For g = 0 .. G-1:

1. Draw two uniform 256-bit words r0, r1, store them at PT[g], and unpack
   W0..W12 as in our earlier packages.
2. Group setup: the scalar group constants of Section 2, their planes
   (shift, AND 1, negate, store: 4 operations per plane), the hoisted gate
   planes (2 loads, 1 gate, 1 store each), the first batch id word
   BID = bid(0, g) and the limit word bid(2^16, g), where

        bid(b, g) = RTAG * 2^128 + (g >> 80) * 2^104 + (g mod 2^80) * 2^16 + b

   (b in bits 0..15, g in bits 16..95 and 104..127, bits 96..103 zero).
   At most 2^13 operations.
3. For b = 0 .. 2^16 - 1, with BID = bid(b, g) in register 63: write batch
   plane i = 0 - ((BID >> i) & 1) into r[i] for i = 0..15 (bit i of BID is bit i
   of b), run the counted batch program, and for each message L, when its key
   word Kw is produced:

        idx = Kw >> 111                    # 2^144 + injective function of K
        e = load T[idx]
        x = Kw ^ BID
        if (e ^ x) < 2^128: CONFIRM        # bits 128..255 of e and x agree
        store T[idx] = x

   then set BID = BID + 1 and loop while BID < bid(2^16, g).
   The entry of message (g, b, L) is x = Kw_L ^ bid(b, g): its bits 128..255
   are (bits 128..255 of Kw_L) XOR RTAG, and its bits 0..127 hold key bits 4..20
   (rows 111..127), L (bits 96..103), b and g.

4. CONFIRM: increment a counter v; if v > V halt with failure. Recover the
   occupant's id from y = e ^ Kw ^ (L * 2^96): bits 0..15 of y are its b',
   bits 96..103 its L', bits 16..95 and 104..127 its g'; rebuild both 55-byte
   messages from PT, check that they differ, compute both complete reference
   digests and compare all eight words. If equal, output the pair and halt;
   otherwise continue with the store above.

If the loops finish, halt with failure.

## 8. Correctness

Every evaluated message is a 55-byte string in the domain. The batch program
computes Kw_L of Section 5 exactly (Sections 3-6; it is straight-line code made
of the Boolean identities listed, checked on every lane of the trial-0 batch by
the organizer-run experiments and on the local samples above).

The index Kw >> 111 = 2^144 + (an injective function of K), so two messages
share a slot exactly when their 144-bit keys are equal, and no slot overlaps
the planes, spill slots, constants or PT. If a later message j finds in its
slot the entry x_i written by an earlier message i, then K_i = K_j, so
Kw_i ^ Kw_j = (L_i ^ L_j) * 2^96 and

    e ^ x_j = Kw_i ^ Kw_j ^ bid(b_i, g_i) ^ bid(b_j, g_j),

whose bits 128..255 are RTAG ^ RTAG = 0: the test passes. Moreover
y = e ^ Kw_j ^ L_j * 2^96 = bid(b_i, g_i) ^ L_i * 2^96, so CONFIRM decodes
(g_i, b_i, L_i) exactly and rebuilds message i correctly. CONFIRM accepts only
after two complete reference digests agree on distinct messages, so every
output is an ordinary full 256-bit collision of complete 37-round SHA-256. A
slot never written in the run may hold anything; a wrong candidate from it is
rejected by CONFIRM (any decoded id names some 55-byte message, possibly from an
uninitialised PT entry, and is just compared).

## 9. Success probability

The coins are r0, r1 per group and RTAG. Failure requires one of:

- F1: no two of the N messages have equal digests;
- F2: some digest-colliding pair (i < j) where, when j probes, the slot of i
  holds the entry of some k with i < k < j and idx(k) = idx(i) (overwrite);
- F3: two groups draw identical 416-bit prefixes, probability below 2^-209;
- F4: more than V candidates.

Heuristic H1 treats the N digests (and their key projections) as independent
uniform values for F1, F2 and the genuine part of F4. Then
Pr[F1] <= exp(-N(N-1)/2^257) < 0.606531. For F2, idx(k) = idx(i) means
K_k = K_i, so the expected number of triples (k, i, j) with equal 144-bit keys
for (i, k) and equal digests for (i, j) is at most
N^3 2^-144 2^-256 / 2 = 2^-17.

Candidates are of two kinds. Garbage candidates come from slots not written in
the run. For fixed prefixes, the keys and the set of written slots do not
depend on RTAG, and the test compares bits 128..255 of e ^ Kw ^ (RTAG * 2^128)
with zero for a fixed e, so each message is a garbage candidate with
probability 2^-128 over RTAG: at most 1 expected, and more than 2^40 with
probability at most 2^-40 (Markov), without H1. A written slot always holds an
entry with the same 144-bit key (Section 8). Genuine false candidates need an
earlier entry with the same 144-bit key but a different digest. Under H1, given
the history, message j's key is uniform, so this has probability at most
(written slots)/2^144 <= 2^-16 for every j; the count is dominated by a
Binomial(N, 2^-16) variable with mean 2^112, and exceeds 2^113 with probability
below exp(-2^112/3). At most one candidate is a true collision (the run halts).
Hence Pr[F4] < 2^-40 + 2^-1000.

    Pr[success] >= 1 - 0.606531 - 2^-17 - 2^-209 - 2^-40 - 2^-1000 > 0.39346.

The claim is 0.39, keeping a 0.0034 allowance for deviation from the model,
as in our earlier packages. Cross-group pairs with the same u collide with
probability >= 2^-256 for any fixed function (Cauchy-Schwarz over uniform
prefixes); within-group pairs are a 2^-104 fraction of all pairs.

## 10. Charged time

    T <= N * 45518 / (256 * 2644)                       (all batches)
       + G * 2^13 / 2644                                       (group setup)
       + V * (2 + 2^10 / 2644)                                 (confirmations)
       + 2^12 / 2644                                           (global setup)
       = 2^124.10564 + 2^105.64 + 2^114.26 + 2

so T < 2^124.10721 and the claim is time_log2 = 124.10721 (rounded up at the
fifth decimal). This caps every run: it includes all random draws, failed and
discarded messages, loads and stores, transposes, table work, confirmations,
verification and setup. The two whole compressions per confirmation are
charged at one unit each; everything else is charged per word operation.

## 11. Memory and other resources

T: 2^144 words of 32 bytes = 2^149 bytes. PT: 2^104 * 64 bytes = 2^110 bytes.
Planes, spill slots, constants and code are under 2^24 bytes. Peak below
2^150 bytes; memory_log2_bytes = 150. Only 2^128 slots are ever written; T is
never initialised and costs no time. preprocessing_log2 = 0. There is no
nonuniform advice.

## 12. Sensitivity

Same circuit and transpose, re-allocated and re-executed on the machine
(main term plus the same setup and confirmation terms):

| Variation | ops per message | bound |
| --- | ---: | ---: |
| As claimed: 64 registers | 177.80 | 2^124.10721 |
| 48 registers | 181.57 | 2^124.13742 |
| 32 registers | 186.91 | 2^124.17919 |
| Unbounded registers (loads and stores free; lower reference) | 141.39 | 2^123.77700 |
| One extra store charged after every gate | 311.99 | 2^124.91780 |
| The base package 64bca7e2 (same circuit, earlier counted program) | 181.19 | 2^124.13437 |
| Scalar package for this track (no bit-slicing) | 1220 | 2^126.885 |

The claim rests on the 64-register machine with every load and store charged,
the convention of the earlier packages on this track. The 32-register line
shows how much depends on register count.

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

The keys returned by the circuit are the same function of the message as in
64bca7e2, so for any given seeds the experiments return the same pairs as the
base package; only the trial-0 operation count changes. Local replay of this
version with locally chosen seeds fixed before the run (not organizer
evidence; seeds SHA-256("r37-v3-local|<experiment>|<i>"), i < 4096), every
returned pair re-checked with `digest(m, "sha256", 37)` under the mask:

| Layout | Trials | Successes (model 1610.0) | z | Masked pairs (expected 2043.9) | Rejected pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| s256-bs-spread | 4096 | 1610 | -0.00 | 1993 | 0 |
| s256-bs-single-group | 4096 | 1580 | -0.96 | 1971 | 0 |

The runs were not repeated or extended after seeing the results. Each of the
32 requests (256 trials each) reported batch_ops = 45518 from its trial-0
self-check and took at most 4.4 s locally.

## 14. Sources and limitations

Reused with credit: the whole circuit generator, message family, key, scaled
experiments and accounting structure of Th0rgal's 64bca7e2 (124.135), which
this package modifies only as listed in Section 15; through it, the bit-sliced
SHA-256 circuit with 256 messages per batch, free rotations, polarity-aware
majority and the delta-swap transpose to per-message key words (mitchuski's
sha256-r37 bit-sliced packages, crediting earlier sha3-256-r6 work for the
transpose; jaazinn's 256-lane bit-sliced package), the key on digest words
fixed before the last round and the uninitialised table whose entries carry a
per-run random tag with a deterministic candidate cap (jungjipdo's sha256-r37
SWAR package), and the grouped single-block family with its group constants
(earlier r31/r32 and scalar r37 packages). Ours: the four changes of Section
15 and the corresponding analysis in Sections 5-11.

H1 is a heuristic, tested on masked 18-bit projections, not the full event.
Organizer seeds are public. The register machine is a modelling assumption;
Section 12 gives alternatives. This is a constant-factor improvement, not a
cryptanalytic weakness of SHA-256 and not a Pareto improvement (memory is very
large). The nominal reference identifier sha256-r37-nominal-v2 is metadata, not
a claimed improvement over a qualified baseline.

## 15. Changes from 64bca7e2 and their measured effect

Each change was measured by re-running `count_batch` with all earlier changes in
place; every intermediate program was checked lane by lane against the scalar
reference.

| Change | Operations per batch |
| --- | ---: |
| 64bca7e2 as submitted | 46384 |
| 1. X & ~Y as (X ^ Y) & X, sharing the XOR with the adder sum (121 gates) | 46263 |
| 2. All 64 registers allocatable: the batch counter lives in BID bits 0..15 (no separate counter register, no per-batch BID computation), and BID and the table temporaries are allocated values instead of five reserved registers | 45994 |
| 3. Key in the high half of the key word, table index Kw >> 111 over the full key, test (e ^ x) < 2^128 (no shift) | 45742 |
| 4. Lane planes routed through the transpose at rows 96..103 (no per-message lane-id XOR); the 80 transpose operations on constant rows precomputed once | **45518** |

Variants measured and not adopted (all lane-checked): dropping the
same-polarity search for constant-folded full adders (+24); per-column
emission orders other than W, T1, E, A (+7 to +62); skewing round t+1's
columns into round t's tail (+0 to +252); reordering column-adder operands
(+16 to +32); merging W34's summands into T1(34) (+1); cost-weighted eviction
preferring clean values (+0 to +411); lane rows at rows 0..7 (+224 against
rows 96..103).
