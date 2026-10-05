# Eight-way SWAR-packed birthday search for two-round BLAKE3

## 1. Claim and scope

Target: `blake3-r2-prefix-v1`. Lane: exploratory. Attack class: ordinary
collision. The selected hash is unkeyed BLAKE3-256 with the standard IV, the
first two compression rounds (0 and 1) with the standard message permutation
between them, the standard feed-forward, and the complete 256-bit root output.
Neither the round convention nor the hash domain is changed. Messages are exactly
64 bytes, so each is a single chunk whose single block is also the root block:
one compression with flags `CHUNK_START|CHUNK_END|ROOT` (= 11), `block_len` 64,
`counter` 0, and the 256-bit digest is the first eight output words.

Under `collision-frontier-v5`, with C = 430 (the reference two-round compression
operation count), the algorithm below has:

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^126.67 target-compression equivalents |
| Peak memory (reported only) | 2^167 bytes |
| Preprocessing | no separate precomputed table; constant setup <= 2^20 ops is inside the total |
| Probability of returning an ordinary collision | at least 0.39 |
| Nonuniform advice | zero bytes |

This is an analytical algorithm with astronomically large memory and work. It is
not a measured collision or a practical break. Its improvement is implementation
and accounting within the specified 256-bit word RAM — eight-way packing of the
32-bit BLAKE3 word and an uninitialised sparse-set table — not a new differential
attack on BLAKE3.

The **existence of a full-digest collision (Section 8) is distribution-free**:
it holds for every fixed deterministic 256-bit-output function on the domain, by
a simplex-maximiser argument, with no random-function, round-independence, PRNG
or differential premise. Only the two sparse-set table events of Section 7
(displacement F2' and the confirmation cap Fcap) use the independent-uniform
heuristic H1, which ships the organizer-run experiment manifest of Section 10.

## 2. Exact messages, padding, and digest

Set n = 2^128. A message is a uniform 64-byte string; equivalently it is 16
little-endian 32-bit words m0..m15 drawn uniformly, so the sampling domain D has
size 2^512. Repeated messages are retained and charged. There is one batch of n
messages, no adaptive sampling, no rejection sampling, and no restart.

Each message is a single 64-byte chunk forming one root block. Following
`verifier/blake3.py`, the complete hash is one compression

    v = cv(=IV[0..7]) , IV[0..3] , counter_lo(=0) , counter_hi(=0) , block_len(=64) , flags(=11)

with flags = CHUNK_START|CHUNK_END|ROOT = 1|2|8 = 11, followed by two rounds of
eight G calls with the message permutation between them, and the feed-forward
`o_i = v[i] XOR v[i+8]`. The digest is `struct.pack("<8I", o0..o7)`, the first
eight output words (256 bits). The words `v[i+8] XOR cv[i]` of the standard
sixteen-word output are **not** part of the 256-bit digest and are never
computed (feed-forward early abort, Section 4). Each final witness verification
recomputes this same complete hash with the reference compression.

The round map is the BLAKE3 quarter-round applied in the fixed column/diagonal
schedule of `verifier/blake3.py`:

    G(a,b,c,d,x,y):
      v[a] = (v[a] + v[b] + x) mod 2^32 ;  v[d] = ror32(v[d] XOR v[a], 16)
      v[c] = (v[c] + v[d]) mod 2^32     ;  v[b] = ror32(v[b] XOR v[c], 12)
      v[a] = (v[a] + v[b] + y) mod 2^32 ;  v[d] = ror32(v[d] XOR v[a], 8)
      v[c] = (v[c] + v[d]) mod 2^32     ;  v[b] = ror32(v[b] XOR v[c], 7)

with the message permutation PERMUTATION = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)
applied to m after each round. G uses only 32-bit modular addition, XOR, and
right rotation; no AND, OR or NOT appears in the round. These are FIPS-public and
organizer-fixed facts.

## 3. Eight independent states in one word

For eight 32-bit values define

    pack(a0,...,a7) = sum_{j=0}^{7} a_j * 2^{32 j}.

All attack registers hold 256-bit values, with arithmetic reduced modulo 2^256.
There are no wider-word operations. A fixed finite register bank holds the 16
packed state lanes, the 16 packed message words, and scalar temporaries. A
uniform 256-bit random word *is already* a packed word of eight uniform 32-bit
fields, so no input packing is performed; the sixteen message words m0..m15 are
sixteen fresh uniform 256-bit words.

Field-wise XOR acts independently on the eight disjoint 32-bit fields: `X XOR Y`
is exactly eight simultaneous 32-bit XORs. Two operations need boundary
isolation: per-field rotation and per-field addition. Let

    H    = pack(2^31, ..., 2^31)      (the top bit of every field)
    notH = pack(2^31-1, ..., 2^31-1)
    L_r  = pack((2^r-1)·2^{32-r}, ...) (the high r bits of every field)
    R_r  = pack(2^{32-r}-1, ...)       (the low 32-r bits of every field)

These are literal constants of the fixed straight-line program; their one-time
construction is accounted in setup (Section 9), not per message.

### Rotation lemma

For 0 < r < 32 define, using five primitive word operations,

    t1 = (X >> r) AND R_r
    t3 = (X << (32-r)) AND L_r
    Y  = t1 OR t3.

Consider bit position 32 j + k, 0 <= j < 8, 0 <= k < 32. The `X >> r` term
places source bit 32 j + k + r into position 32 j + k when k + r < 32; `AND R_r`
keeps exactly the positions k < 32 - r of field j and discards any bits that the
global shift moved in from field j+1. The `X << (32-r)` term places source bit
32 j + k - (32 - r) into position 32 j + k when k >= 32 - r; `AND L_r` keeps
exactly positions k >= 32 - r of field j and discards bits shifted out of or into
a neighbouring field. The two supports are disjoint and both come from field j,
so

    Y = pack(ror32(a0,r), ..., ror32(a7,r)).

The four BLAKE3 rotation amounts 16, 12, 8, 7 are all in (0,32), so every
rotation costs five operations. No native rotate and no hash oracle is used.

### Addition lemma (per-field carry isolation)

For two packed words define, using six primitive word operations,

    z = ((X AND notH) + (Y AND notH)) XOR ((X XOR Y) AND H).

Claim: field j of z equals `(a_j + b_j) mod 2^32` where a_j, b_j are fields j of
X, Y. Proof. Write a_j = 2^31 u_j + p_j and b_j = 2^31 w_j + q_j with u_j,w_j in
{0,1} and 0 <= p_j, q_j < 2^31. The masked operands `X AND notH` and `Y AND notH`
have field j equal to p_j and q_j, each < 2^31, so p_j + q_j < 2^32 - 1: the
256-bit addition produces, in bits [32 j, 32 j + 32), exactly the 32-bit value
p_j + q_j, and **no carry crosses into field j+1** (the field sum is below 2^32).
Its bit 31 equals the carry c_j out of bit 30 of p_j + q_j. The second term
`(X XOR Y) AND H` has, at bit 32 j + 31, the value u_j XOR w_j and is zero
elsewhere in field j. XORing, field j of z has low 31 bits equal to those of
p_j + q_j (correct, since bits 0..30 of the true sum ignore u_j, w_j) and bit 31
equal to c_j XOR u_j XOR w_j. The true modular sum's bit 31 is exactly
(u_j + w_j + c_j) mod 2 = c_j XOR u_j XOR w_j. Hence field j of z equals
`(a_j + b_j) mod 2^32`, with no cross-field carry. QED.

The three-input additions `v[a] + v[b] + x` are two applications of the lemma
(12 operations); the intermediate per-field value is already reduced mod 2^32 by
the first application, so the second application's precondition holds. No
separate `& 2^32-1` reduction is needed: the lemma yields the reduced value
directly.

### Packed-round lemma

Replace each 32-bit XOR by `XOR`, each 32-bit addition by the addition lemma, and
each rotation by the rotation lemma; broadcast each fixed initial word
(IV, counter, block_len, flags) to all eight fields. By the two lemmas and the
bitwise identity for XOR, every field of every packed register equals the
corresponding field's ordinary BLAKE3 value after the same step. The message
permutation only relabels packed registers. Induction over the two rounds and the
eight-word feed-forward proves that field j of the eight output words equals the
256-bit digest of message j, exactly, including padding and all output bits. This
is an algebraic identity, not an empirical extrapolation. It was checked
bit-for-bit against `verifier/blake3.py:blake3(·,2)` on 32000 messages
(4000 packed groups of eight): **0 mismatches** (Section 10, Checks).

## 4. Explicit packed-compression instruction bound

The schedule is fixed and unrolled; there are no run-time loops over a/b/c/d or
rotation amounts. Per G call, counting the two lemmas:

| Step | Operations |
| --- | ---: |
| `v[a] = v[a] + v[b] + x` (two packed adds) | 12 |
| `v[d] = ror(v[d] XOR v[a], 16)` (xor + rot) | 6 |
| `v[c] = v[c] + v[d]` (one packed add) | 6 |
| `v[b] = ror(v[b] XOR v[c], 12)` | 6 |
| `v[a] = v[a] + v[b] + y` | 12 |
| `v[d] = ror(v[d] XOR v[a], 8)` | 6 |
| `v[c] = v[c] + v[d]` | 6 |
| `v[b] = ror(v[b] XOR v[c], 7)` | 6 |
| Total per G | 60 |

Each round is eight G calls = 480 operations; two rounds = 960. The digest
feed-forward computes only the first eight output words `o_i = v[i] XOR v[i+8]`,
i = 0..7 = 8 operations; the other eight sixteen-word outputs are not in the
256-bit digest and are skipped. The packed compression therefore costs

    960 + 8 = 968 operations per group of eight messages = 121.0 per message.

This count was reproduced mechanically by an operation-counting `int` subclass
identical in convention to `scripts/reference_operation_costs.py` (which reports
C = 430 for a single `blake3._compress(·, ·, 0, 64, 11, 2)`): the packed program
executes 968 counted add/and/or/xor/shift operations for eight messages.
Evaluating one whole compression in word operations without packing costs 496
operations (16 G * 30 + 16 feed-forward words under the strict convention), more
than C = 430; the saving is entirely from the eight-way packing, which amortises
each boundary-isolated primitive across eight messages: 968/8 = 121 < 430.

Because every field evolves independently and no field is read as an address or a
branch condition inside the packed core, the whole group executes as one
straight-line sequence on the word RAM; this reduces total work, not parallel
latency, and every primitive is counted once in that total.

## 5. Record generation, memory, and grouping

The messages are processed in n/8 = 2^125 groups of eight. For each group:

1. Draw 16 fresh uniform 256-bit words m0..m15 (16 operations) and store them so
   the eight messages can be reconstructed on a later match (16 stores). These 32
   operations per group are 4 per message.
2. Run Section 4 (968 operations) to obtain the eight packed output words o0..o7.
3. For each of the eight lanes j, extract the message's 160-bit table key and run
   one sparse-set table step (Sections 6-7).

The broadcast initial state (IV, counter 0, block_len 64, flags 11) consists of
fixed constants, built once in setup. No per-message packing of inputs is needed
because a random 256-bit word is already eight uniform fields. A group record is
the 16 stored words (512 bits per message, kept for reconstruction); its index is
`id = group*8 + j`, formed from the loop counter.

### Key extraction (18 operations per message)

The 160-bit table key of message j is the concatenation of lane j's fields of the
five output words o0..o4:

    for i in 0..4:  f_i = (o_i >> 32 j) AND (2^32 - 1)          # 2 ops each = 10
    K = f0 OR (f1 << 32) OR (f2 << 64) OR (f3 << 96) OR (f4 << 128)   # 8 ops

This is an injective map from (o0..o4 of lane j) to K < 2^160; 10 + 8 = 18
operations. A full-digest collision has equal o0..o4, hence equal K, so no
collision is lost by keying on 160 of the 256 digest bits.

### Memory (reported only)

Peak storage is: the sparse index at base 2^160 (addresses 2^160 | K < 2^161
words), the dense confirmation array (<= n records), and the per-group stored
message words (2^125 * 16 * 32 bytes < 2^134). Every address is below 2^161 words
= 2^166 bytes; we report 2^167. Fewer than 2^135 bytes are ever written. No array
is read before being written by the algorithm except the sparse index, whose
uninitialised reads are validated by the Briggs-Torczon test (Section 6). Memory
is reported only and contributes nothing to the score.

## 6. Uninitialised sparse-set collision table

We adopt the **never-displaced Briggs-Torczon sparse-set structure and validity
test** used by the prior-art packages on this track (jaazinn, ticket `0a5b7ae8`,
time_log2 127.481; winglock, ticket `3022205`, time_log2 127.252, both in review),
cited as prior art. The 160-bit key here is o0..o4; winglock used o0,o1,o2,o3,o5.
Any 160 fixed digest bits work: a full-digest collision has all digest words equal,
so it has equal keys under either choice, and the probability arithmetic below
(n·2^-160) is identical. The sparse set replaces a fully charged sort, whose
64-bit-digit radix passes would add about 176 charged operations per message
(Section 7, variant) and push the score above the frontier.

Two conceptual arrays live in reported-only memory: a *sparse* array `S` indexed
by the 160-bit key at `addr = 2^160 | K`, and a *dense* array `Dkey, Did` indexed
by an insertion counter `cnt` (initially 0). A slot of `S` is **valid** for the
current state iff the value `p = S[addr]` read from it satisfies `0 <= p < cnt`
**and** `Dkey[p] == K`. Because `cnt` only grows and `Dkey[p]` was written by the
algorithm whenever `p < cnt`, an uninitialised (garbage) slot cannot forge a
valid match: either its value is `>= cnt` (rejected by the range test) or it is
some `p < cnt` whose stored key `Dkey[p]` differs from `K` (rejected by the key
test). This is the standard sparse-set validity invariant; it needs no memory
initialisation.

Per-message table step (12 charged operations), for message j with key K:

    addr = 2^160 OR K                          # 1 OR
    p    = load S[addr]                         # 1 load
    if p < cnt and Dkey[load p] == K:           # range compare+branch (2), key load+compare+branch (3)  -> MATCH
        confirm (Section 7)
    else:                                       # insert
        Dkey[cnt] = K ; Did[cnt] = id          # 2 stores
        S[addr] = cnt                           # 1 store
        cnt = cnt + 1                            # 1 add

The worst-case non-match path (range test passes, key test fails, then insert) is
OR, load, compare, branch, load, compare, branch, store, store, store, add = 12
operations; the branch not taken on an empty slot is cheaper. We charge 12 for
every message.

## 7. Recovering and checking a collision; table events

The table is **never displaced**: an existing entry for key K is kept, and a
later message with the same key is either confirmed as a collision (equal full
digest) or discarded (different full digest). A full-digest collision between
distinct messages y and z has K_y = K_z; when the second of them is processed, its
slot holds the first message with key K. If that first holder is y or z, the key
test passes and the pair is confirmed. The only way to miss the collision is:

- **F2' (displacement/squatting).** Let (y, z) be the FIRST colliding pair in
  processing order (y before z). F2' is the event that some message x processed
  before y has K_x = K_y but a different digest, so y (and hence z) is discarded
  against x instead of confirmed. Under H1 the expected number of messages before
  y with key K_y is at most n * 2^-160 = 2^-32, so Pr[F2'] < 2^-32. (We bound the
  first colliding pair, not a union over all pairs: confirming that one pair
  succeeds.)

- **Fcap (confirmation cap).** We cap the number of key-colliding confirmations
  at 2^110 and declare failure if exceeded (bounding time deterministically).
  Under H1 the expected number of 160-bit key-colliding ordered pairs is
  < n^2 / 2 / 2^160 = 2^95, so by Markov Pr[Fcap] <= 2^95 / 2^110 = 2^-15.

On a confirmation, reconstruct both 64-byte messages from their stored group
words (lane extraction), check they differ, recompute both complete two-round
BLAKE3 digests with the reference compression primitive (charged two units), and
return the pair if all 256 bits agree. Halt on the first returned pair. At most
2^110 confirmations occur, each costing <= 2 units plus <= 128 reconstruction
operations; the total confirmation cost is below 2^110 * (2 + 128/430) < 2^111.2
units, i.e. below 2^-15 of the main term.

A radix-sort variant that removes H1 entirely (four fully charged 64-bit-digit
passes over the unpacked records, as in our sha3-256-r5 package) is available; it
adds about 176 charged operations per message, giving time_log2 ~ 127.74, above
the frontier. We therefore use the sparse set and confine the heuristic to F2'
and Fcap.

## 8. Success probability for the fixed target (distribution-free)

This section uses **no heuristic**. Let H be the selected deterministic complete
hash, q = 2^256, and p_y = |H^{-1}(y) ∩ D| / |D|. The sampled messages M_i are
iid uniform on D (each is 16 uniform 32-bit words), so the outputs Y_i = H(M_i)
are iid with probability vector p; p need not be uniform and H is not randomised.
Packing eight independent inputs into one evaluation changes neither input
independence nor H.

For n <= q, the probability that all Y_i differ is `n! e_n(p)`, where e_n is the
elementary symmetric polynomial of degree n. On the compact probability simplex
e_n attains a maximum; among maximisers pick one minimising the sum of squares,
and replace two unequal coordinates a, b by their mean. Using

    e_n(p) = a b · e_{n-2}(r) + (a+b) · e_{n-1}(r) + e_n(r)   (r the other coords)

with nonnegative coefficients, this replacement does not decrease e_n and strictly
decreases the sum of squares — a contradiction unless the maximiser is uniform.
Therefore

    Pr[all outputs distinct] <= prod_{j=0}^{n-1}(1 - j/q) <= exp(-n(n-1)/(2q)).

For n = 2^128, q = 2^256 the exponent is -(1/2 - 2^-129), so the probability of
at least one full-digest output collision is at least
1 - exp(-(1/2 - 2^-129)) > 1 - 0.6066 = 0.3934.

A repeated output might be a repeated input; by the union bound
Pr[some repeated input] <= n(n-1)/(2 · 2^512) < 2^-257. Subtracting the table
events of Section 7,

    Pr[success] >= 0.39343 - 2^-257 - Pr[F2'] - Pr[Fcap] > 0.39343 - 2^-32 - 2^-15 > 0.39.

The claim is 0.39, keeping about 0.0034 of allowance. All runs stop within the
same charged budget: there are no successful-only trial counts, expected-time
substitutions, uncharged failures, or restarts.

**Fallback if H1 is rejected.** The F1 bound above is distribution-free and needs
no heuristic. If a reviewer rejects H1 for the table events entirely, replace the
sparse set with the four-pass 64-bit-digit radix sort of our sha3-256-r5 package
(Section 7 variant, +~176 charged operations per message): sorting makes every
equal-digest pair adjacent, so the collision is found deterministically with no
displacement or cap event, and the whole algorithm becomes distribution-free at
time_log2 ~ 127.74 — still below the 128 nominal reference, though above the
current frontier. H1 buys the drop from 127.74 to 126.67; it is not load-bearing
for correctness.

## 9. Total computation, preprocessing, and memory

Per message the charged operations are

    121 (packed compression) + 4 (generation) + 18 (key extraction)
      + 12 (table step) + 3 (loop control) = 158 counted,

charged as **170** (158 + 12 spare, so a disputed register move, flag or jump
cannot understate the bound). There are n = 2^128 messages, at most 2^110
confirmations, and one-time constant/mask setup below 2^20 operations. Hence

    T <= 2^128 * 170/430                     main loop
       + 2^110 * (2 + 128/430)               confirmations (<= 2^111.2)
       + 2^20 / 430                          constant and mask setup
     = 0.3953488 * 2^128 + (< 2^111.21) + (< 2^11.3).

The leading logarithm is `128 + log2(170/430) = 128 - 1.33881 = 126.66119`. The
confirmation and setup terms are below 2^-15 of the leading term, so
`T < 2^126.6613`, and the claim is **126.67** with more than 0.008 bits of
rounding margin. Every generation, random word, packed primitive, key extraction,
table load/store, confirmation and output write is included.

There is **no separate preprocessing phase**: the sparse set is uninitialised, no
giant table is built, and the only setup is the fixed program, constants and
masks (< 2^20 operations), already inside T. Preprocessing is reported as 0 in
that sense (<= a tiny bound inside T), not added twice. Zero bytes of advice.

Sensitivity (every reading beats the 127.252 frontier):

| charged operations per message | log2 T |
| --- | --- |
| 158 (exact count, no spare) | 126.555 |
| 170 (claimed) | 126.661 |
| 170 with per-field add charged 7 (padd = 7, compression 133/msg) | 126.76 |
| 200 (fully conservative key/table/loop) | 126.896 |
| all constants reloaded from memory before each use (no live register bank: +2 per padd and per pror, compression 1288/8 = 161/msg, ~198 counted, charge 210) | 126.97 |

Peak memory is reported only (Section 5): below 2^167 bytes, fewer than 2^135
written. No infeasible-size object is treated as a unit-cost wider word.

## 10. Evidence, provenance, and limits

The construction is supported by the algebraic rotation and addition lemmas, the
packed-round equivalence, the sparse-set validity invariant, and the
distribution-free (fixed-function) probability proof. The eight-way SWAR packing
and the distribution-free birthday argument are adopted from our in-review
sha3-256-r5 package (four-way packing there; eight-way here because BLAKE3 words
are 32-bit) and generalised with the new per-field addition lemma, which keccak
did not need (keccak has no addition). The uninitialised sparse-set table is
adopted from the prior-art packages jaazinn `0a5b7ae8` (127.481) and winglock
`3022205` (127.252); we reproduce its validity argument in full and do not copy
any organizer implementation. We do not adopt their grouped partial-evaluation
message family; this package packs eight fully independent messages, which keeps
the full-digest-collision event distribution-free.

Checks:

```sh
python3 scripts/local_tracks.py check blake3-r2-exploratory      # mechanically_valid
# packed-evaluator correctness: 0/32000 mismatches vs verifier/blake3.py:blake3(.,2)
# packed op count: 968 for eight messages (121/message), by a reference-convention counter
# experiments b3r2-swar-birthday / b3r2-swar-lowbits: 256 trials, ~0.393 success,
#   every returned pair re-verified as a genuine masked collision of the trusted digest.
```

Heuristic scope. The experiment manifest declares two `python-message-pairs-v1`
experiments that compute digests ONLY through the submitted SWAR packed evaluator
and test the 20-bit masked birthday event (scaled analogue N_t^2/2^w = N^2/2^256
= 1) under spread and concentrated masks. They support heuristic H1 for the two
table events F2' and Fcap. They do NOT bear on the full-digest-collision event
F1, which is distribution-free (Section 8). Only masked 20-bit projections are
tested, organizer seeds are public, and finite frequencies support but do not
prove the population bound.

The required `baseline_improved` identifier denotes the organizer's nominal
reference; the supported scalar is below that nominal exponent, but this is not a
security boundary or a practical defeat of BLAKE3. The larger memory compared
with a distinguished-point search is an explicit tradeoff; no Pareto dominance is
claimed. Mechanical intake cannot certify these resource or probability
arguments; exploratory AI qualification, official scoring, and manual organizer
acceptance remain separate outcomes.

Model: Claude Opus 4.8. Harness: Claude Code.
