# SHA-256 r38: bit-sliced grouped birthday search with a pre-last-round key

Lane: exploratory. Target: `sha256-r38-prefix-v1`. Attack class: ordinary
collision. Cost model `collision-frontier-v5`, C = 2728: one 38-round target
compression costs 1 unit; every other 256-bit RAM word operation costs 1/2728.

## 0. Claim, summary and credit

* Output: two distinct 55-byte messages whose complete 38-round SHA-256
  digests agree on all 256 bits (Section 6, unconditional).
* Time: at most 2^124.9678 units in every run (Section 8), under the fixed
  register-bank convention of Section 2 with one placement charged per gate
  result. Claimed `time_log2: 124.968`.
* Success: at least 0.3905 under one heuristic, H1 (Sections 7, 11). Claimed
  0.39.
* Memory below 2^146 bytes (reported only); preprocessing under 2^9 units
  (program generation, inside T); advice zero (Section 9).

This is a generic birthday attack. N = NB * 2^32 messages, NB =
78856234692123534151746250567 (N = 0.99531 * 2^128), are hashed and their
digests looked up in an uninitialised table. Three exact constant-factor
savings make each message cost 335 word operations instead of one compression:
(i) messages are evaluated 256 at a time as bit planes, so the 38-round
compression is a straight-line Boolean circuit; (ii) messages come in groups
that share their first 13 message words, so rounds 0-12 and seven schedule
words are computed once per group and only rounds 13-36 run per message;
(iii) the table key is the 160 digest bits that are fixed before the last
round, so round 37 and the T2 half of round 36 are never computed. No
cryptanalytic weakness of SHA-256 is claimed. `baseline_improved` names the
nominal reference `sha256-r38-nominal-v2` (display value 128, not a baseline
or a bound). The track's displayed current best, 132, is the organizer-
authored unconditional merge-sort candidate shipped in the repository at
f46ab58 in this candidate directory.

Credit. The grouped partial-evaluation birthday search, the never-initialised
sparse-set table and the F1/F2/F3 failure analysis under H1 are jaazinn's
(blake3-r2, 0a5b7ae8). The 256-message bit-plane evaluation and the delta-swap
transpose are may93182's (sha3-256-r6, 11c46f4d); the bit-sliced grouped
search and the transpose-into-sparse-set program are
winglock's (sha3-256-r6, 377eebd5), whose SPARSE listing and transpose counts
we reuse verbatim. The fixed register-bank convention is zeeshan8281's
(sha3-256-r6, d2f84741/cbf7998d, #178) as adopted in our 02d6a703. Computing
only the digest bits the key needs is ercumentyildirim's last-round projection
(c7fa1a56). The 55-byte single-block message domain for this track and the
uninitialised-table candidate cap are jungjipdo's (sha256-r38, 325d628d).
None of them has reviewed this package; the SHA-256 circuit, the polarity-aware
adder, the pre-last-round key, the counted program and any errors are ours.

## 1. Target, messages, groups and the key

The target hashes a byte string with the standard SHA-256 IV, FIPS 180-4
padding, rounds 0..37 of the standard schedule and constants on every block,
feed-forward, and the full big-endian 256-bit digest. A 55-byte message pads
to exactly one block: W[0..13] carry the 55 message bytes and the byte 0x80,
W[14] = 0, W[15] = 440. Its digest is therefore the feed-forward output of a
single reduced compression on that block from the IV.

**Groups.** A group g has a prefix P_g of 13 uniform 32-bit words
W[0..12] (416 fresh coins). The message m(g, z), for z in {0, .., 2^24 - 1},
is

    m(g, z) = BE32(W[0]) || ... || BE32(W[12]) || BE24(z)      (55 bytes),

so W[13] = (z << 8) | 0x80. Distinct (g, z) with distinct prefixes give
distinct messages. Groups are processed in batches of 256 (one group per bit
position of every 256-bit word). N = NB * 256 * 2^24 messages: NB batches,
each 2^24 z-steps of 256 messages. The processing order (batch, z, lane) is
fixed in advance and never depends on a digest.

**Key.** Write the digest words as (A, B, Cw, D, E, F, G, H) and the state
entering round t as (a_t, ..., h_t), so (a_0, ..., h_0) = IV and
(a_38, ..., h_38) is the state after round 37. After 38 rounds, Cw = a_36 +
IV[2], D = a_35 + IV[3], F = e_37 + IV[5], G = e_36 + IV[6], H = e_35 + IV[7].
These five digest words, 160 bits, depend only on rounds 0..36, and e_37 needs
only the T1 half of round 36. The table key of a message is K = these 160 bits
placed in bits 96..255 of a 256-bit word (bits 0..95 zero): H in bits
96..127, G in 128..159, F in 160..191, D in 192..223, Cw in 224..255, each
word with its bit 0 lowest. Equal digests give equal keys; equal keys are
checked by recomputing both full digests (Section 5.3).

## 2. Machine model and register-bank convention

Primitives (each 1/2728): 256-bit load, store; add/sub mod 2^256; AND, OR,
XOR, NOT; shift/rotate; compare; conditional branch; RAND (fresh uniform
256-bit word). A compare plus its branch is 2; a jump is 1; writing a
constant is 1. Instruction fetch is not charged; program text counts as
memory. The algorithm never reads memory it has not written, except the
sparse-set array S, whose garbage is never trusted (Section 5.4). A scalar
compression (verification only) costs 1 unit plus at most 300 operations for
block writes, reads and control.

**Convention.** The bank is the machine's named-operand register file: a
fixed set of at most 2048 words (Lemma 2.1), independent of N, that the
primitive operations address by name, as the cost model's primitives
address their operands. It is the convention of zeeshan8281's #178 (Yukon
d2f8474, 126.902), used by may93182's 11c46f4d (126.995), ercumentyildirim's
c7fa1a5 (126.92) and our 02d6a703 (125.58) on sha3-256-r6, each of which
reached `plausible_not_refuted`; that acceptance is reported from the public
board, not verifiable from this packet. If a judge instead prices every
operand as a main-memory load and every result as a store, the same program
gives the memory-to-memory row of Section 8, 125.88, which we state as the
explicit fallback bound; it is still below the 132 candidate. Each gate is one operation reading its
named bank operands, plus one placement (bank store) per gate result. The
key rows after the transpose, the sparse-set arrays S, DK, DI, the prefix
planes PL and all counters are main memory or registers: every load and
store to them is charged, exactly as in winglock's listing.

**Lemma 2.1 (bank size).** The per-step program (Section 3) reads 1,163
group words (32 prefix planes and 1,131 results of the group-plane gates),
24 z planes, and defines 37,818 gate results. An exact liveness scan of the
generated straight-line program (each result live from its definition to
its last use; the 160 key planes to the transpose) gives at most 559
simultaneously live step results. With the 1,187 input words and one NOT
temporary, at most 1,747 words are ever resident; we allocate 2048.
Allocation is static (fixed when the program is written).

Sensitivity to the convention is in Section 8.

## 3. The bit-sliced circuit

A signal is a public constant bit, a *group plane* (a word that differs per
lane but not per z, computed once per batch), a *z plane* (0 or all-ones,
the same in every lane, set per step), or a *step value* (a stored word s
with a public flag phi; the true plane is s XOR phi*all-ones). Rules applied
once when the program is written:

* XOR with a constant and NOT flip the flag (no instruction). Rotations
  and shifts of a 32-bit word are index renamings of its 32 planes (SHR
  brings in constant-0 planes).
* XOR of two stored signals: one XOR, flags added mod 2.
* AND: with constant 1 the identity, with 0 the constant 0; flags (0,0):
  one AND; (1,1): one OR with flag 1 (De Morgan); mixed: one NOT, one AND.
  OR is AND of the complements.
* Group-plane gates whose operands are all group planes or constants are
  evaluated once per batch (Section 5.1); a gate with a z-plane or
  step-value operand is a per-step gate.

**Adder (polarity-aware).** For a 32-bit modular add of two words the bits
run from 0 upward with carry c (c_0 = 0; the carry out of bit 31 is dropped).
With x, y, c all stored, choose x as the operand whose flag differs from the
other two (two of three flags always agree); then p = y XOR c, sum = x XOR p
and

    carry = (y AND c) OR (p AND x)                 if flag(x) = flag(y),
    carry = (y OR c) XOR (p AND xbar)              otherwise,

where xbar is the stored word of x. The second identity is
maj(x,y,c) = (y AND c) XOR (x AND (y XOR c)) with x = NOT xbar, using
(y AND c) XOR (y XOR c) = y OR c. Both forms are 5 operations and never
materialise a NOT. When one operand bit is a constant k: sum = x XOR c
(flag flipped if k = 1), carry = x AND c (k = 0) or x OR c (k = 1), 2
operations, plus one NOT when the flags of x and c differ. When c_0 = 0 the
bit-0 carry is x AND y.

**Round t** (T1 = h + S1(e) + Ch(e,f,g) + (K_t + W_t), T2 = S0(a) + Maj(a,b,c),
e' = d + T1, a' = T1 + T2): S0, S1 are two XORs per bit; sigma0, sigma1 are
two XORs per bit except where SHR supplies a zero (one XOR). Ch(e,f,g) is
g XOR (e AND (f XOR g)) when flag(e) = flag(f XOR g) and f XOR (ebar AND
(f XOR g)) otherwise: 3 operations, no NOT. Maj(a,b,c) uses whichever of
b XOR ((a XOR b) AND (b XOR c)), a XOR ((a XOR b) AND (a XOR c)),
c XOR ((a XOR c) AND (b XOR c)) has equal flags at the AND, reusing the
previous round's a XOR b as this round's b XOR c when it is the operand
needed: 3 or 4 operations, no NOT. K_t + W_t is a constant add (2 per bit).
The schedule word W_t = sigma1(W_{t-2}) + W_{t-7} + sigma0(W_{t-15}) +
W_{t-16} is built lazily; W[16..19], W[21], W[23], W[25] and their K sums
depend only on the prefix and are group planes.

**Per-step gate counts (256 messages).** The generator (Appendix A) was run
locally on 256 random prefixes and random z, and its 160 key planes were
checked against the reference digest words Cw, D, F, G, H of all 256
messages (0 mismatches, every run; the shipped experiment program repeats
this check on four lanes per trial, and the organizer recomputes every
returned pair). Counts are independent of the data.

| Block | Gates | Block | Gates | Block | Gates |
|---|---:|---|---:|---|---:|
| round 13 | 434 | round 22 | 1436 | round 30 | 1458 |
| round 14 | 1188 | round 23 | 1365 | W31 | 383 |
| round 15 | 1273 | W24 | 371 | round 31 | 1436 |
| round 16 | 1390 | round 24 | 1429 | W32 | 391 |
| round 17 | 1404 | round 25 | 1366 | round 32 | 1444 |
| round 18 | 1382 | W26 | 366 | W33 | 398 |
| round 19 | 1356 | round 26 | 1418 | round 33 | 1419 |
| W20 | 232 | W27 | 232 | W34 | 397 |
| round 20 | 1435 | round 27 | 1446 | round 34 | 1437 |
| round 21 | 1363 | W28 | 581 | W35 | 598 |
| W22 | 259 | round 28 | 1447 | round 35 | 1450 |
| | | W29 | 328 | W36 | 515 |
| | | round 29 | 1425 | round 36 (T1, e only) | 912 |
| | | W30 | 284 | feed-forward (5 words) | 370 |

Total **37,818** gates: 21,295 XOR, 9,111 AND, 4,377 OR, 3,035 NOT, plus
86 fix-up NOTs for key planes stored with flag 1. Round 13 is cheap because
its T1 adds a z-dependent word to group planes and its T2 is a group plane.
Group-plane gates evaluated per batch: 23,727.

## 4. Batches, z-steps and the transpose

Batch beta (0 <= beta < NB) holds groups 256 beta + p, p = 0..255, in lane
p. Its 416 prefix planes PL[beta][i] (i = 32w + bit) are fresh RAND words
stored once (Section 5.1): bit p of PL[beta][32w + i] is bit i of W[w] of
group 256 beta + p. Independent uniform words give independent uniform
prefixes. Step t of a batch sets z = t (t = 0..2^24 - 1): the 24 z planes
are Z[i] = 0 - ((t >> i) AND 1) for i = 0..23, formed by 3 operations and a
placement each.

After the per-step gates, the 160 key planes are rows 96..255 of a 256 x 256
bit matrix whose rows 0..95 are zero. The delta-swap transpose (may93182,
winglock's listing) turns rows into the 256 key words K_p (bits 96..255 of
K_p are the key of lane p). Phase 1 works inside 32-row blocks (stages 1, 2,
4, 8, 16); the three blocks of rows 0..95 are zero and are skipped, so phase 1
is 5 constant moves plus 5 blocks of (32 loads, 5 stages x 16 swaps x 6
operations, 32 stores) = 2,725 operations. Phase 2 (stages 32, 64, 128) is 3
constant moves plus 32 x (8 loads, 3 stages x 4 swaps x 6) = 2,563
operations and leaves each finished key in a register, from which SPARSE
(Section 5.4) consumes it directly. (The zero rows could shorten phase 2 too;
we charge it in full.)

## 5. Algorithm

Registers: step counter t, batch counter beta, running id IDM, table size n,
bases PL, SB (S), DK, DI, constants ONE, K24 = 2^24, candidate counter v.
Main memory: PL (416 words per batch), S (2^140 words, never initialised),
DK and DI (N words each), the bank, and the output.

### 5.1 Batch setup (once per batch, 2^24 steps)

1. Draw 416 RAND words; store each at PL + 416 beta + i and place it in the
   bank as the prefix plane (416 x (1 + 2 + 1) = 1,664 operations with
   address adds).
2. Evaluate the 23,727 group-plane gates (2 operations each: 47,454),
   producing the 1,131 group words the step program reads (the state
   entering round 13, the Maj reuse plane, the group schedule words with
   their K sums, and the partial sums of round 13's T1).
3. Set t = 0, IDM = beta * 2^32 (ids are beta * 2^32 + p * 2^24 + z, below
   2^128 since NB < 2^96).

Charged setup: fewer than 2^16 operations per batch (49,118 + control),
i.e. 2^16 / 2^24 = 2^-8 per step and 2^-16 per message.

### 5.2 Per z-step program (straight-line, fully unrolled)

    (a) form Z[0..23] from t                       24 x 4 = 96
    (b) the 37,818 per-step gates, 2 each         75,636
        86 key fix-up NOTs, 2 each                   172
    (c) transpose phase 1 (5 blocks)               2,725
    (d) transpose phase 2 feeding SPARSE           2,563
        256 x SPARSE(K_p, p), worst path 17 each   4,352
    (e) t = t + ONE ; c = (t < K24) ; branch           3   (next step or next batch)
    total per step (256 messages)                 85,547

That is 334.17 operations per message; with setup (2^-16) we charge **335**.
IDM is set to beta * 2^32 + z at (a) (one add) and advanced by K24 per lane
inside SPARSE, as in winglock's listing; those operations are inside the
counts above (the extra add is within the spare).

### 5.3 Verification and halting

On MATCH (equal 256-bit key words, Section 5.4): load DI[i] (2). Decode both
ids into (beta, p, z) (at most 20 operations). Read the two prefixes: for
each, 13 words from the bits p of PL[beta][0..415] (416 x (load, shift, AND,
OR, shift) = 2,080 each; charged 4,200 for both). Rebuild the two 55-byte
messages (at most 60). If the messages are equal (only in event F3), halt
with failure. Evaluate both with two scalar reference compressions (2 units
+ 600). Compare the full digests (at most 20). If equal, output the pair and
halt. Otherwise (a false candidate: same key, different digests) increment
v; if v = V = 2^100 halt with failure; else discard the current message
(no insertion) and continue the step. One candidate costs at most 2 units
plus 5,000 operations, charged 4 units.

### 5.4 Sparse set (jaazinn's Briggs-Torczon structure, winglock's listing)

S has 2^140 words and is never initialised. Slot h is *valid* iff S[h] < n
and DK[S[h]] >> 116 = h. Keys are inserted only into invalid slots, which
the insertion makes valid; entries are never rewritten. So a valid slot
holds exactly the first inserted key whose bits 116..255 are h.

    SPARSE(K, p):
    h = K SHR 116 ; a = h + SB ; i = LOAD [a] ; c = (i < n) ; if !c goto INSERT
    e = i + DK ; k2 = LOAD [e] ; u = k2 SHR 116 ; c = (u == h) ; if !c goto INSERT
    c = (k2 == K) ; if c goto MATCH ; IDM = IDM + K24 ; goto NEXT    ; different key: discard
    INSERT: e = n + DK ; STORE [e] = K ; e = n + DI ; STORE [e] = IDM ;
            STORE [a] = n ; n = n + ONE ; IDM = IDM + K24
    NEXT:

Path lengths: empty slot then insert 12; stale pointer then insert 17 (the
worst); occupied by a different key 14; match 12, after which verification
runs. Bits 116..255 of K are the top 140 key bits (Cw, D, F, G and the top 12
bits of H); bits 0..95 of every key word are zero, so K SHR 116 never aliases
across different keys' low bits.

### 5.5 Run

for beta = 0..NB-1: setup; for t = 0..2^24-1: step. Then halt with failure.
There is no restart, no parallel work omitted, and no uncharged loop.

## 6. Every output is a collision (unconditional)

An output is produced only after both messages were rebuilt from their ids,
found distinct, and both full 38-round digests were recomputed by the
reference compression and found equal. Bit slicing changes how a digest is
computed, not its value; Appendix A's check and the organizer-executed
experiments (Section 10) confirm the circuit, but correctness of outputs
does not rely on them.

## 7. Success probability

The run halts at the first successful verification. Failure events:

* **F3**: two groups have equal prefixes. Pr[F3] <= (NB*256)^2/2 * 2^-416 <
  2^207 * 2^-416 = 2^-209. Without F3 all N messages are distinct.
* **F1**: no two of the N messages have equal digests.
* **F2**: some colliding pair (a, b), a processed before b, has a's slot
  held when a arrives by an earlier message c with the same top 140 key bits
  and a different digest (c has either a different key, so a is discarded,
  or the same 160-bit key, so a is a false candidate and discarded).
* **F4**: the false-candidate counter reaches V = 2^100.

**Lemma 7.1.** If none of F1-F4 occurs, the run outputs a collision. Take a
colliding pair (a, b), a first, and suppose no earlier collision was output.
When a arrives, its slot is invalid (a is inserted) or valid and holding the
first key with a's top 140 bits, which belongs to an earlier message c; by
not-F2, c's digest equals a's, so c's key equals a's: MATCH, c != a (not F3,
distinct (g, z)), digests equal: output. If a was inserted, when b arrives
its slot is valid (entries are never rewritten) and holds a's key (the first
key with those top bits, else a would have matched or been discarded, which
not-F2 excludes): MATCH, output. F4 cannot halt the run before that under
not-F4.

**Heuristic H1 (declared; equivalent text in claim.json).** For the events
F1, F2 and F4, the N digests of the grouped message set {m(g, z)}
(independent uniform prefixes P_g, all z in {0,1}^24, processed in the
fixed order of Section 4) behave like N independent uniform 256-bit values:
Pr[F1] <= exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396, and the number Y of
pairs with equal keys and different digests has E[Y] <= N^2/2^161 and
Var[Y] <= N^2/2^161.

Under H1, with N = NB * 2^32 and x = N(N-1)/2^257:

* Pr[F1] <= exp(-x). Since N > 0.995305 * 2^128, x >= 0.495316 and
  exp(-x) <= 0.609378.
* Pr[F2] <= N^3/6 * 2^-396 < 2^-14.5; we use 2^-13.
* Pr[F4] <= Var[Y]/(V - E[Y])^2 < 2^95/2^198 = 2^-103 (Chebyshev;
  E[Y] < 2^95).
* Pr[F3] < 2^-209.

NB is the smallest batch count for which 1 - exp(-N(N-1)/2^257) - 2^-13 -
2^-209 - 2^-100 - 2^-61 >= 0.3905 (the last term is spare); the script in
Appendix B checks this with 60-digit arithmetic. So Pr[success] >= 0.3905
under H1, claimed **0.39**.

**Rigorous partial support (jaazinn's argument, in aggregate form).** For
two groups g != g', let q(v) = sum over z of Pr[digest of m(g, z) = v] over
the uniform prefix. The two groups' prefixes are independent, so the
expected number of colliding pairs between them is sum over v of q(v)^2 >=
(sum over v of q(v))^2 / 2^256 = 2^48 / 2^256 by Cauchy-Schwarz: the 2^48
cross pairs of two groups collide 2^-256 times each on average. Within-group
pairs are a 2^-104 fraction of all pairs. The expected number of colliding
pairs is therefore at least (1 - 2^-104) N(N-1)/2^257 > 0.4953 without any
heuristic. H1 is
needed for the second-moment behaviour behind Pr[F1], for F2 and for Y.
Within a group, rounds 0..12 and the state entering round 13 are identical
for all 2^24 messages, and the messages differ only in W[13]; 24 further
rounds with the full schedule follow. This is a stronger structure than
independent sampling, and is the reason H1 is a heuristic.

## 8. Total charged time (worst case, every run)

| Phase | Count | Units each | Bound |
|---|---|---|---:|
| Steps | NB * 2^24 | 85,547/2728 (335 x 256/2728 charged) | N * 335/2728 |
| Batch setup | NB | <= 2^16/2728 | inside the 335 |
| False candidates | <= 2^100 | 4 | 2^102 |
| Final verification and output | 1 | 4 | 4 |

    T <= N * 335/2728 + 2^102 + 4,   N = 78856234692123534151746250567 * 2^32.

log2(N * 335/2728) = 124.96760; the other terms add a relative 2^-22.97
(1.8e-7 bits). **log2 T <= 124.96761 < 124.968**, the claimed `time_log2`.
The script in Appendix B verifies T < 2^124.968 by exact integer arithmetic:
with T = T_num/2728, T_num = N*335 + (2^102 + 4)*2728, it checks
T_num^100000 < 2728^100000 * 2^12496800.
The spare inside 335 absorbs c <= 334.99 per message against 334.17
itemised plus 2^-16 setup. Every failed step, every discarded message, every
table load, store, compare and branch, every bank read and placement, every
candidate verification and the final output are included. There is no
other precomputation, no stored collision, no parameter search and no
repetition.

Sensitivity (only the circuit charge varies; transposes and SPARSE as above):

| Convention for the same circuit | per message | log2 T |
|---|---:|---:|
| fixed bank, gates only, no placement (not claimed) | 187 | 124.13 |
| **fixed bank, one placement per result (claimed)** | **335** | **124.968** |
| winglock 377eebd charge (+1 per direct access, 64 registers), estimated | ~270 | ~124.66 |
| memory-to-memory, every operand loaded, every result stored | 630 | 125.88 |

The third row is an estimate from winglock's 1.32 ratio on Keccak and is not
claimed. jungjipdo's 325d628d charges a 7-lane SWAR compression at 443.286
operations per message (125.376); the saving here comes from bit planes,
shared group work and the pre-last-round key, not from a different model.

## 9. Memory, preprocessing, advice

S: 2^140 words = 2^145 bytes. DK and DI: N words each, under 2^133 bytes
each. PL: 416 NB words < 2^110 bytes. Bank (2048 words), registers, key
rows, and program text (about 90k straight-line instructions, under 8 MB):
under 2^24 bytes. Total under 2^145.01 bytes: `memory_log2_bytes: 146`.
Messages are never stored; they are rebuilt from (beta, p, z) and PL.

Preprocessing: generating the fixed straight-line program once (about 90k
instructions from the generator rules, under 2^20 operations = 2^8.6 units)
and loading constants. Declared `preprocessing_log2: 9`; it is inside the
spare of T. Batch setup is charged inside T (Section 5.1). Advice: zero.

## 10. Experiments and H1 evidence

Five `python-message-pairs-v1` experiments, declared for organizer
execution, share one stdlib program,
`experiments/grouped_search.py`. It compiles the Section 3 circuit (the same
generator rules as Appendix A) once, and runs it on 256 lanes exactly as the
algorithm does; in every search trial the messages are the family of Section
1 and the lookup mirrors Sections 5.2-5.4 on a scaled key.

* `r-bs-fullwidth-equivalence` (12-bit mask on digest word H): one batch of
  256 groups from the trial seed, one z-step; four lanes are checked in full
  against the program's scalar reference (abort on mismatch); returns two
  lanes whose key words agree on the masked bits. A mechanical cross-check
  of the circuit; the organizer's recomputation on the real target is the
  evidence.
* Four scaled searches with N_t = 512 messages per trial and an 18-bit key
  (the low 18 bits of H; N_t^2/2^18 = 1, against N^2/2^256 = 0.9906 at full
  scale), returning the first match: `r-bs-full-width` (256 groups x 2 z,
  one batch), `r-bs-spread` (16 x 32), `r-bs-single-group` (1 x 512,
  strongest within-group structure) and `r-bs-high-z` (4 x 128 with the
  varying z bits at 17..23). The uniform model gives success 1 - prod(1 - i/2^18, i < 512) = 0.3931
  per trial (100.6 +- 7.8 per 256 trials). Several trials
  share one 256-lane batch, each owning its own lanes; bitwise operations
  never mix lanes.

Local runs, all reported: our dev harness with our own seeds (256 trials per
layout) gave 98, 97, 96 and 87 successes; the organizer's own Docker executor
run locally with the public seed (`hashsmash-public-seed-v1`, two runs each,
byte-identical output) gave 93, 105, 105 and 105, and 256/256 on the
equivalence check. Every returned pair was re-checked by the runner.
A pre-registered larger run with our seeds (8,192 trials per layout, run
once after the 256-trial runs, every pair re-verified with the reference
digest, no bad pair) gave 3288, 3216, 3239 and 3238 against the model's
3222 +- 44 (largest deviation +1.5 sigma).

Numeric observations in the output (gate counts, fix-ups) are untrusted.
The experiments test the circuit and the scaled birthday law on the real
reduced-round target; they cannot certify the full-width second moment, F2
or the 0.0005 allowance.

## 11. Heuristics (complete list)

H1 only (Section 7, equivalent text in claim.json), score-critical, used only for
the success probability. Correctness of every output and all resource bounds
are unconditional.

## 12. Limitations

* H1 is unproved; within a group the state entering round 13 is shared by
  2^24 messages. No evidence of a departure from the uniform model was found
  in the scaled runs, and no full-width inference is drawn from them.
* The register-bank convention is a modelling choice (Section 2); Section 8
  gives the bound under other readings.
* The organizer seeds are public; scaled runs resolve the success frequency
  to about +-0.03 at 256 trials.
* Memory is far above the organizer baseline's and is reported, not scored.

## 13. Prior work

jaazinn 0a5b7ae8; may93182 11c46f4d; winglock 377eebd5; zeeshan8281
d2f84741 and cbf7998d; ercumentyildirim c7fa1a56; jungjipdo 325d628d; our
02d6a703; van Oorschot and Wiener (parallel collision search, 1999) for the
generic context; the organizer-authored sha256-r38 merge-sort candidate at
f46ab58 (132).

## Appendix A. The circuit generator

`experiments/grouped_search.py` contains the generator used for every count
in this proof: a symbolic 38-round SHA-256 over signals (constant, group
plane, z plane, step value with flag) with the rules of Section 3, lazy
schedule, the pre-last-round key projection, and emission of a straight-line
program over 256-bit words. Run on random prefixes and z it (i) counts gates
by type and (ii) evaluates the emitted program on 256 lanes and compares the
five key words of every lane with its scalar reference (our local runs, 0
mismatches at 38 and 37 rounds; in the shipped program four lanes per
trial); counts as in Section 3.

## Appendix B. Certificate script

`cert.py` (stdlib `decimal` at 60 digits and exact integers; listed in
full below): (1) finds NB as the least batch count with success bound
1 - exp(-N(N-1)/2^257) - 2^-13 - 2^-209 - 2^-100 - 2^-61 >= 0.3905 and
prints it (78856234692123534151746250567, N = 0.995306 * 2^128, bound
0.3905000...); (2) forms T_num = N*335 + (2^102 + 4)*2728 and checks
T_num^100000 < 2728^100000 * 2^12496800, i.e. T < 2^124.968, by exact
integer comparison (True), and prints log2 T = 124.96760.

```python
import sys
from decimal import Decimal, getcontext
getcontext().prec = 60
R = int(sys.argv[1]) if len(sys.argv) > 1 else 38
OPS, C, CLAIM5 = {38: (335, 2728, 12496800), 37: (320, 2644, 12494700)}[R]
TWO = Decimal(2)
def success_bound(NB):
    N = Decimal(NB) * TWO**32
    x = N * (N - 1) / TWO**257
    return 1 - (-x).exp() - TWO**-13 - TWO**-209 - TWO**-100 - TWO**-61
lo, hi = 1, 2**96
while lo < hi:
    mid = (lo + hi) // 2
    if success_bound(mid) >= Decimal("0.3905"): hi = mid
    else: lo = mid + 1
NB = lo; N = NB * 2**32
print("NB", NB, "N/2^128", Decimal(N) / TWO**128, "bound", success_bound(NB))
T_num = N * OPS + (2**102 + 4) * C            # T = T_num / C
print("log2 T =", (Decimal(T_num) / C).ln() / TWO.ln())
print("T < 2^%.5f :" % (CLAIM5 / 1e5), T_num ** 100000 < (C ** 100000) << CLAIM5)
```
Output (R = 38): NB 78856234692123534151746250567, N/2^128 0.9953056...,
bound 0.3905000..., log2 T = 124.96760, `T < 2^124.96800 : True`.
