# Grouped birthday search for 37-round SHA-256 with a key read through the last four rounds

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2644 for
sha256-r37). Memory is a separately reported bound.

This exploratory package targets sha256-r37-prefix-v1. It is a generic
birthday search on the complete 37-round hash. It is a derivative of
Th0rgal's public pending package 64bca7e2 on this track (bit-sliced grouped
birthday search, 46384 operations per 256-message batch, claimed
124.135); the full credit list is in Section 14. It changes one thing: the
144-bit collision key. Instead of 144 digest bits that are final before round
36, the key is a 144-bit function of the digest that is obtained by
inverting the last four rounds, and it is already determined after round
33 = R - 4. Consequently the per-message circuit stops four rounds before the
end of the compression:

1. every message is 55 bytes, so the complete hash is one padded block and one
   37-round compression;
2. messages come in 2^104 groups of 2^24 that share W0..W12 and differ only in
   the 24 free bits u of W13, so rounds 0..12, seven schedule words and every
   gate whose inputs are all group constants or fixed lane planes are computed
   once per group;
3. (changed) the key is K = kappa(digest) of Section 3, a fixed function of the
   full 256-bit digest; it needs rounds 13..30 in full, round 31 without
   S0, round 32 without its A half, and only the low 16 bits of T1 in round
   33; rounds 34..36 are never computed per message;
4. 256 messages are evaluated together, bit-sliced: a 256-bit register holds
   bit j of one 32-bit word for 256 messages, rotations are free renamings,
   and every modular addition is a counted Boolean adder.

One batch of 256 messages costs exactly **40453** operations, counted by
executing the emitted register-allocated program on a 64-register machine:
158.019531 operations per message, including loads, stores, the transpose to
per-message key words, the table step and batch control. The total is
T < 2^123.93722 charged units, time_log2 = **123.93722**, with success probability
0.39 under one declared heuristic (H1, unchanged in content from the base
package and stated on digests). This is not a differential attack on SHA-256;
the improvement is a constant factor.

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

    T1_t = h + S1(e) + Ch(e,f,g) + K_t + W_t,   T2_t = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) <- (T1_t + T2_t, a, b, c, d + T1_t, e, f, g),

with S0 = ROR2 ^ ROR13 ^ ROR22, S1 = ROR6 ^ ROR11 ^ ROR25,
Ch = (e&f)^(~e&g), Maj = (a&b)^(a&c)^(b&c), all modulo 2^32, and the standard
IV and K_t at their original indices. A_t and E_t denote the new a and e words
produced by round t, so in round t the inputs are a = A_{t-1}, b = A_{t-2},
c = A_{t-3}, d = A_{t-4}, e = E_{t-1}, f = E_{t-2}, g = E_{t-3}, h = E_{t-4}. The digest is
H_i = IV_i + s_i (mod 2^32) in standard big-endian order, where
s = (A36, A35, A34, A33, E36, E35, E34, E33) is the working state after round
36. This is the complete hash `verifier/hash_functions.py:digest(m, "sha256", 37)`
on the declared domain, not a free-start or compression-only result. A reported
collision is re-verified with two whole compressions of the reference hash.

## 2. Group constants and the message-dependent schedule

W13 is first used in round 13, so the state after rounds 0..12 is a group
constant. W13 enters the schedule at t = 20, 28 and 29. Of the schedule words the
circuit uses, W20, W22, W24, W26, W27, W28, W29, W30, W31, W32, W33 depend on W13 (11 words), while W16..W19, W21, W23 and
W25 are group constants. Every dependent word is computed from its W13-dependent
summands plus one group constant P_t that pre-adds the others (for example
W20 = W13 + P20 with P20 = s1(W18) + s0(W5) + W4, and
W28 = s1(W26) + s0(W13) + P28 with P28 = W21 + W12). In rounds 32 and 33
the word W_t is used by no later computation of the circuit, so it is not formed
as a separate word: its dependent summands go directly into the T1 sum together
with the single group constant PK_t = P_t + K_t. The other group constants used
per message are A10..A12, E11, E12, A13pre = T1 + T2 of round 13 without W13
and DT13pre = d + T1 of round 13 without W13 (so A13 = A13pre + W13 and
E13 = DT13pre + W13), HKW_t = h + K_t + W_t for t = 14, 15, 16 (where h = E_{t-4}
is itself a group constant) and KW_t = K_t + W_t for t = 17, 18, 19, 21, 23, 25.
Additions are modulo 2^32, so regrouping summands is exact.

In the bit-sliced circuit any gate whose two inputs are group-constant planes,
fixed lane planes (Section 4) or outputs of such gates is not executed per
batch: the lane planes are the same in every batch, so its output plane is a
per-group constant, computed once per group and stored (Section 7 charges it).
The circuit has 422 such gates.

## 3. The key: a function of the digest, fixed after round 33

Lemma 1 (inverting a round). For every round t, E_t = A_{t-4} + T1_t and
A_t = T1_t + T2_t with T2_t = S0(A_{t-1}) + Maj(A_{t-1}, A_{t-2}, A_{t-3}). Hence

    A_{t-4} = E_t - A_t + S0(A_{t-1}) + Maj(A_{t-1}, A_{t-2}, A_{t-3})   (mod 2^32).

Lemma 2 (the digest determines eight A words). Put s = H - IV wordwise. Then
s gives A36, A35, A34, A33 and E36, E35, E34, E33 directly. Applying Lemma 1 with
t = 36, 35, 34, 33, in this order, gives A32, A31, A30, A29: each step uses only s
and the A words produced by the previous steps. So A29, ..., A36 are functions of
the digest. Conversely E_t = A_{t-4} + A_t - T2_t recovers s from A29..A36, so
H <-> (A29, ..., A36) is a bijection of 256-bit strings.

Definition (L = R - 4 = 33).

    X = T1_33  = E33 - A29
    Y = T1_32 = A32 - S0(A31) - Maj(A31, A30, A29)
    Z = A31 - S0(A30)             (= T1_31 + Maj(A30, A29, A28))
    K = (X mod 2^16) || Y || Z || A30 || A29        (bits 0..15, 16..47, 48..79, 80..111, 112..143)

E33 (L = R - 4) is digest word h minus IV7, and A29, ..., A32 are functions of the
digest by Lemma 2, so K = kappa(H) for a fixed function kappa: **equal digests
imply equal K**. A K match is only a candidate; it is confirmed by two complete
digests (Section 7).

Lemma 3 (K is a projection of a bijective re-encoding). Replace, in the tuple
(A29, ..., A36), the word A31 by Z, A32 by Y and A33 by
X = A33 - T2(A32, A31, A30). Each replacement subtracts from one word a function of
earlier words of the tuple, so the new tuple is again a bijective image of H
(invert left to right: A31 = Z + S0(A30), A32 = Y + T2(A31, A30, A29),
A33 = X + T2(A32, A31, A30)); and X computed this way equals E33 - A29 by Lemma 1.
K consists of 144 of its 256 bits. Hence, if H is uniform on 256-bit strings,
K is uniform on 144-bit strings, and for two independent uniform digests
Pr[K equal] = 2^-144 and Pr[digests equal | K equal] = 2^-112. Every
probability in Section 9 therefore has the same model value as for a key made
of 144 digest bits.

What the circuit computes per message. By Section 1, X = T1_33 =
E29 + S1(E32) + Ch(E32, E31, E30) + K_33 + W33; Y = T1_32 =
E28 + S1(E31) + Ch(E31, E30, E29) + K_32 + W32; Z = T1_31 + Maj(A30, A29, A28).
The low 16 bits of a modular sum depend only on the low 16 bits of its
summands (carries move upward), and bits j < 16 of S1(E32) and Ch use whole
words E32, E31, E30, which are computed in full. So the circuit computes, per
message: rounds 13..30 in full; round 31 with its E half and with the A half
replaced by Z (no S0 term); round 32 with its E half only (E32 = A28 + Y is
needed by round 33, and Y itself is a key word); and the low 16 bits of T1 of
round 33. A31, A32, A33 and everything after round 33 are never computed.
`scalar_key` in `experiments/bitsliced_birthday.py` computes K exactly as
defined here, from the reference digest through Lemmas 1-3, and the trial-0
check compares it with the counted program on all 256 lanes of a batch.

## 4. The bit-sliced circuit

A batch is 256 messages of one group with u = 256 b + L', L' = 0..255. Plane j of a
32-bit word X is the 256-bit value whose bit L' is bit j of X for message L'. A
word is 32 planes. Inputs per batch: the group-constant planes (each 0 or all
ones), eight fixed lane planes (bit L' of lane plane i is bit i of L'; they hold
u bits 0..7, W13 bits 8..15), sixteen batch planes (all ones or zero by bit i
of b; W13 bits 16..31) and the constant 0x80 for W13 bits 0..7.

Gates are 256-bit AND, OR and XOR, one operation each. Every intermediate is
a signed literal: a stored plane plus a compile-time polarity flag, so NOT,
XOR with a constant and every rotation or shift by a constant cost nothing
(rotation renames planes; a shift renames planes and fills with the constant 0).
The rules, each an identity of Boolean algebra (unchanged from the base package):

- X & Y (1), ~X & ~Y = ~(X | Y) (1), X & ~Y = (X | Y) ^ Y (2); OR by duality;
- Ch(e, f, g) is always 3 gates (2 new gates when d = f ^ g is reused from the
  previous round) across all four polarities of e and d = f ^ g:
  g ^ (E & D) when e = E, d = D; f ^ (E & D) when e = ~E, d = D;
  ~(f ^ (E | D)) when e = E, d = ~D; ~(g ^ (E | D)) when e = ~E, d = ~D;
- Maj(a, b, c) = b ^ ((a ^ b) & (b ^ c)) is always 3 new gates (reusing b ^ c
  from the previous round) across all four polarities of d1 = a ^ b and d2 = b ^ c:
  b ^ (D1 & D2), ~(b ^ (D1 | D2)), ~(c ^ (D1 | D2)) or ~(a ^ (D1 | D2));
- a full adder on (a, b, c) computes t = a ^ b, sum = t ^ c, and carry = Ch(t, c, a)
  when t = (T, 0) or Ch((T, 0), a, c) when t = (T, 1), always sharing T = A ^ B
  between sum and carry: 5 operations in all polarity cases, no materialised NOT;
- a half adder is 2 operations; a constant input bit folds (x + y + 1 gives
  sum ~(x ^ y), carry x | y: 2 operations when x, y share polarity);
- every multi-operand sum modulo 2^32 (or 2^16 for X) is column compression: in
  column j, full adders reduce the column's bits (with carries from column j-1)
  to one, passing carries to column j+1; the top column keeps sums only.

The circuit is emitted column by column in lock step: for each round t and bit
j it computes bit j of the dependent schedule word W_t (rounds up to 31), of
T1_t, of E_t = d + T1_t and of A_t = T1_t + S0 + Maj (rounds up to 30),
keeping the carry chains of all sums open. In round 31 the A column is
Z = T1 + Maj (two summands); in round 32 only the T1 and E columns exist; in
round 33 only the 16-bit T1 column exists, whose summands are E29, S1(E32),
Ch(E32, E31, E30), the dependent summands of W33 and PK_33. In rounds 32 and 33 the
dependent summands of W_t and PK_t enter the T1 column directly (Section 2).
`build` in `experiments/bitsliced_birthday.py` is this exact generator. Its
outputs are the 144 key planes (X bits 0..15, Y, Z, A30, A29). The circuit has
25860 gates per batch after group-constant hoisting.

## 5. Transpose to one key word per message

Unchanged from the base package. The table needs each message's key as one
256-bit word. Rows 0..143 of a 256 x 256 bit matrix are the key planes (a
literal with polarity flag set contributes its stored plane, so the result is
K XOR pol for a fixed constant pol: an injective relabelling of the key,
harmless for collision detection). Row 144 is the constant all-ones plane;
rows 145..255 are zero. A delta-swap transpose swaps index bit k of rows and
columns for k = 0..7: for rows i and i + 2^k (bit k of i clear) with mask m_k of
columns whose bit k is clear,

    t = ((a >> 2^k) ^ b) & m_k;  b' = b ^ t;  a' = a ^ (t << 2^k)     (6 operations)

and when one row is still zero the swap needs 3 operations
(b = 0: a' = a & m_k, b' = (a >> 2^k) & m_k; a = 0: t = b & m_k, a' = t << 2^k,
b' = b ^ t). Pass 1 applies k = 0, 1, 2 to aligned groups of 8 rows, pass 2
applies k = 3..7 to the 32 rows of each residue class mod 8 and hands each
finished row (the key word of message L') to the table step. The transpose
costs 4077 operations per batch. After it, word L' is
K_L' XOR pol XOR 2^144, with bits 145..255 zero.

## 6. Machine, register allocation and the exact batch count

Machine (unchanged): 256-bit word RAM with 64 registers, three-address
operations, immediate shift counts, and loads and stores with a register address
or a small immediate address (all planes, spill slots and constants live below
2^24; the table lives at [2^140, 2^141)). Every load and store is one
operation, as are add, subtract, AND, OR, XOR, shift, compare and branch.

The straight-line program (circuit, transpose, sinks for the table step) is
register-allocated onto registers 0..58 by furthest-next-use eviction, with the
16 batch planes preloaded into registers 0..15 during batch setup. Each
operand not in a register is loaded; an evicted value that is used later and
is not already in memory is stored first; inputs (group-constant, hoisted,
lane and mask planes) are loaded from memory at every use that misses
the registers. Registers 59..63 hold the batch id word, the loaded table
entry, the table entry temporary, the table index and the batch counter. The
emitted program uses at most 59 circuit registers.

`count_batch` executes the emitted program on a 64-register machine and
charges one operation per instruction. Per batch of 256 messages:

| Part | Operations |
| --- | ---: |
| loads | 6048 |
| stores | 2110 |
| XOR | 22506 |
| AND | 3670 |
| OR | 2402 |
| shifts (transpose) | 735 + 624 |
| table steps, 256 x 9 | 2304 |
| batch setup: 16 batch planes x 3, batch id 3, loop 3 | 54 |
| **total per batch** | **40453** |
| per message | 158.019531 |

Gates (XOR/AND/OR/shift) are 29937 per batch: 25860 in the circuit and
4077 in the transpose. The trial-0 self-check of both experiments executes this
program for one batch, compares all 256 key words with K computed from the
scalar reference digest (Section 3), and aborts unless the batch costs exactly
40453 operations. The same file evaluated at the other round count of this pair
gives its own count; the program reads R from the target profile.

## 7. Complete algorithm

Parameters: 2^24 messages per group, G = 2^104 groups, N = 2^128,
table T of 2^140 words at addresses 2^140 + i, never initialised. Candidate cap
V = 2^113 + 2^40 + 1.

Once: draw a uniform 256-bit word RTAG; write the 8 masks m_k, the all-ones
plane and the 8 lane planes (under 2^12 operations).

For g = 0 .. G-1:

1. Draw two uniform 256-bit words r0, r1, store them at PT[g], and unpack
   W0..W12 (416 bits) from them.
2. Group setup: the scalar group constants of Section 2, their planes
   (shift, AND 1, negate, store: 4 operations per plane; at most 848 planes are
   used), the 422 hoisted gate planes (2 loads, 1 gate, 1 store each) and
   GTAG = (g << 152) XOR RTAG. The scalar part is 13 rounds, 7 schedule words and
   at most 13 sums P_t / PK_t on 32-bit values, under 2^11 word operations including
   masking to 32 bits; the plane and hoisted parts are at most 4 x 848 + 4 x 422.
   In total at most 2^13 operations.
3. For b = 0 .. 2^16 - 1: write the 16 batch planes into r[0..15], set
   BID = (b << 136) XOR GTAG, run the counted batch program, and for each
   message L', when its key word Kw is produced:

        idx = Kw >> 4                      # 2^140 + (key bits 4..143)
        e = load T[idx]
        x = Kw ^ BID
        if ((x ^ e) << 128) == 0: CONFIRM  # key bits 0..127 of the difference
        store T[idx] = x ^ (L' << 128)     # id = (g, b, L') in bits 128..255 (XOR RTAG)

   The entry of message (g, b, L') is (K XOR pol XOR 2^144) XOR (id << 128) XOR RTAG
   with id = g 2^24 + b 2^8 + L'. Bits 128..144 of the key word are index bits
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
of the Boolean identities listed; checked on every lane of the trial-0 batch by
the organizer-run experiments against K derived from the reference digest).

If two messages i < j have equal digests, then K_i = K_j (Section 3). If, when j
probes, its slot still holds the entry written by i, then bits 4..144 of the two
key words agree (same slot) and bits 0..127 agree (the test), the test passes,
and e ^ Kw_j ^ RTAG = id_i << 128 exactly: CONFIRM rebuilds message i correctly
and accepts. CONFIRM accepts only after two complete reference digests agree on
distinct messages, so every output is an ordinary full 256-bit collision of
complete 37-round SHA-256. A slot never written in the run may hold anything; a
wrong candidate from it is rejected by CONFIRM (any decoded id names some
55-byte message, possibly from an uninitialised PT entry, and is just compared).

## 9. Success probability

The coins are r0, r1 per group and RTAG. Failure requires one of:

- F1: no two of the N messages have equal digests;
- F2: some digest-colliding pair (i < j) where, when j probes, the slot of i
  holds the entry of some k with i < k < j and idx(k) = idx(i) (overwrite);
- F3: two groups draw identical 416-bit prefixes, probability below 2^-209;
- F4: more than V candidates.

Heuristic H1 treats the N digests as independent uniform values for F1, F2 and
the genuine part of F4; by Lemma 3 their keys are then independent uniform
144-bit values. Then Pr[F1] <= exp(-N(N-1)/2^257) < 0.606531. For F2, the
expected number of triples (k, i, j) with idx(k) = idx(i) and equal digests for
(i, j) is at most N^3 2^-140 2^-256 / 2 = 2^-13.

Candidates are of two kinds. Garbage candidates come from slots not written in
the run. For fixed prefixes, the keys and the set of written slots do not
depend on RTAG, and the test compares bits 0..127 of (e ^ K ^ RTAG) with zero for
a fixed e, so each message is a garbage candidate with probability 2^-128 over
RTAG: at most 1 expected, and more than 2^40 with probability at most 2^-40
(Markov), without H1. Genuine false candidates need an earlier entry with the
same 144-bit key but a different digest. Under H1, given the history, message
j's key is uniform (Lemma 3), so this has probability at most
(written slots)/2^144 <= 2^-16 for every j; the count is dominated by a
Binomial(N, 2^-16) variable with mean 2^112, and exceeds 2^113 with probability
below exp(-2^112/3). At most one candidate is a true collision (the run halts).
Hence Pr[F4] < 2^-40 + 2^-1000.

    Pr[success] >= 1 - 0.606531 - 2^-13 - 2^-209 - 2^-40 - 2^-1000 > 0.39334.

The claim is 0.39, keeping a 0.0033 allowance for deviation from the model.
Cross-group pairs with the same u collide with probability >= 2^-256 for any
fixed function (Cauchy-Schwarz over uniform prefixes); within-group pairs are a
2^-104 fraction of all pairs. The key change does not alter any of these events:
F1 and F3 do not involve the key, and F2/F4 involve it only through
kappa(digest), which Lemma 3 shows is distributed as 144 digest bits under H1.

## 10. Charged time

    T <= N * 40453 / (256 * 2644)                       (all batches)
       + G * 2^13 / 2644                                       (group setup)
       + V * (2 + 2^10 / 2644)                                 (confirmations)
       + 2^12 / 2644                                           (global setup)
       + 2^50 / 2644                                           (development, below)
       = 2^123.93545 + 2^105.63149 + 2^114.25537 + 2^0.63149 + 2^38.63149

(each logarithm truncated, not rounded). T is a rational number; with q = 10^5 and
p = 12393722, the exact integer comparison
numerator(T)^q < 2^p * denominator(T)^q holds, so T < 2^123.93722 and the claim is
time_log2 = 123.93722. This caps every run: it includes all random draws, failed
and discarded messages, loads and stores, transposes, table work,
confirmations, verification and setup. The two whole compressions per
confirmation are charged at one unit each; everything else is charged per word
operation. The program is uniform; the public constants are part of it.

Development charge. Every computation run for this package before the attack
(generating the program, executing the counted VM for the claimed program and
for each variant whose count was compared while designing it, the self-checks,
and the local experiment runs) used fewer than 2^50 word operations in
total; it is charged as preprocessing at its cap, 2^50 / 2644 < 2^39 units
(preprocessing_log2 = 39), and is included in T above. No target-specific
search, tuning on target outputs or advice enters the algorithm; the program
text, including the inherited parts, is used as written.

## 11. Memory and other resources

T: 2^140 words of 32 bytes = 2^145 bytes. PT: 2^104 * 64 bytes = 2^110 bytes.
Planes, spill slots, constants and code are under 2^24 bytes. Peak below
2^146 bytes; memory_log2_bytes = 146. T is never initialised and costs no
time. There is no nonuniform advice. Preprocessing is the development charge
of Section 10 (preprocessing_log2 = 39), already included in T.

## 12. Sensitivity

Same circuit and transpose, re-allocated and re-executed on the machine
(per-message main term; the setup and confirmation terms above are unchanged):

| Variation | ops per batch | ops per message |
| --- | ---: | ---: |
| As claimed: 64 registers | 40453 | 158.019531 |
| 48 registers | 41328 | 161.44 |
| 32 registers | 42740 | 166.95 |
| Unbounded registers (loads and stores free; lower reference) | 32295 | 126.15 |
| Base package 64bca7e2, same machine | 46384 | 181.19 |

The claim rests on the 64-register machine with every load and store charged,
the convention of the base package and the other pending bit-sliced packages on
this track. With 32 registers the main term is
128 + log2(42740 / (256 * 2644)).

## 13. Evidence

Experiments s256-ek-spread (16 groups x 32 consecutive u) and
s256-ek-single-group (1 group x 512 consecutive u) run the bit-sliced circuit
with N_t = 512 = 2^(18/2) messages per organizer seed against an 18-bit masked
event on digest words H3 and H7, bits 0..15. These bits are recovered from each
message's key words by the inversion of Lemma 3 and Section 3:
A31 = Z + S0(A30), A32 = Y + S0(A31) + Maj(A31, A30, A29), E33 = X + A29 and
A33 = X + S0(A32) + Maj(A32, A31, A30) modulo 2^16; H7 = IV7 + E33, H3 = IV3 + A33.
The organizer recomputes every returned pair with the trusted digest, so each
accepted pair checks the counted circuit's key words and the inversion on
genuine messages. N_t^2/2^18 = 1 = N^2/2^256, so this is the scaled analogue of
the full attack. Random-model success per trial is
1 - prod_{i<512}(1 - i/2^18) = 0.39307; untrusted observations report
masked-equal pair counts (expected 0.4990 per trial). Trial 0 of each request
also executes the counted program on one batch, compares all 256 key words with
K from the scalar reference digest, and asserts batch_ops = 40453; every trial
compares two lanes per batch with the reference.

Local run of the organizer's executor code and pinned image on this exact
package, with the public seed `hashsmash-public-seed-v1` (not organizer
evidence; run with a 120 s timeout and 512 MiB because the local host emulates
linux/amd64): s256-ek-spread 115/256 successes, s256-ek-single-group
91/256 (model 100.6 +- 7.8); every returned pair passed the organizer's
digest check; two runs per request, byte-identical stdout. Under the same
emulation, one 256-trial request of this program peaked at 145908 KB resident
memory and took 34.9 s, against 159824 KB and 34.1 s for the base package
64bca7e2, whose experiments pass the organizer's default limits.

## 14. Sources, credits and limitations

This package is a derivative of public, unpromoted work on this track and
credits it as follows.

- Th0rgal, packages 64bca7e2 (r37) and c65868c3 (r38): the experiment program
  `experiments/bitsliced_birthday.py` (circuit generator with polarity-aware Ch,
  Maj and 5-gate full adders, column-lockstep emission and group-gate hoisting,
  merged last-round column, zero-aware delta-swap transpose, furthest-next-use
  register allocation on 59 registers with preloaded batch planes, the VM and
  the 9-operation table step), and the structure and most text of Sections 1, 2,
  4-11 of this proof. This package reuses that program and text with the changes
  listed below.
- jaazinn (817d444c): the 256-lane bit-sliced grouped birthday package on this
  track from which the base package's program was developed.
- mitchuski (875a5083, fca38c6d, f153f574): the bit-sliced circuit, the
  polarity-aware majority and the delta-swap transpose (as credited by the base
  package), and folding K_t together with the group-constant addends into one
  group word (used here as PK_t in rounds 32 and 33).
- jungjipdo (383bad42, 6a3c483e): the 55-byte single-block grouped domain on this
  track, keying on digest words fixed before the last round, and the tagged
  uninitialised table with a candidate cap (as credited by the base package).

Changes made in this package (Claude Opus 5.5 via Claude Code): the key
K = kappa(digest) of Section 3 with Lemmas 1-3 (inverting the last four rounds,
and the re-encodings X = T1_33, Y = T1_32, Z = A31 - S0(A30)); the circuit stops
after the low 16 bits of T1 of round 33 (the round loop and return value of
`build`); the PK_t group words of rounds 32 and 33;
hoisting also of gates whose inputs are group constants and the fixed lane
planes (one changed condition in `Net.inp`); `scalar_key`, `key_of_digest` and
`digest_words` (key from the reference digest, digest bits from the key); the
experiment ids, masks and descriptions; the
operation counts, sensitivity rows and the time bound. No other part of the
program was changed. None of the credited authors has reviewed this package.

H1 is a heuristic, tested on masked 18-bit projections (H3 and H7 bits 0..15),
not on the full event; the base package tested other digest words. Organizer
seeds are public. The register machine is a modelling assumption; Section 12
gives alternatives. This is a constant-factor improvement, not a cryptanalytic
weakness of SHA-256 and not a Pareto improvement (memory is very large). The
nominal reference identifier sha256-r37-nominal-v2 is metadata, not a claimed
improvement over a qualified baseline.
