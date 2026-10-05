# Grouped partial-evaluation birthday search for 32-round SHA-256

The scalar below is `time_log2` under `collision-frontier-v5` (C = 2224 for
sha256-r32). Memory is a separately reported bound.

This exploratory package targets sha256-r32-prefix-v1. It is a generic
birthday search with three exact cost reductions and a reduced-operation
inner body:

1. every message is 55 bytes, so the complete hash is one padded block and one
   32-round compression;
2. messages come in 2^104 groups of 2^24 that share message words W0..W12 and
   differ only in the 24 free bits of W13, so rounds 0..12, seven schedule
   words and most of round 13 are computed once per group;
3. collisions are detected on the 192-bit partial state after round 30,
   so round 31 and the feed-forward are skipped for every message, and full
   digests are computed only to confirm candidate matches;
4. the per-message word-RAM program is written with three standard software
   identities (Section 4) that lower its counted operation count from 856 to
   856 - 148 = 708 while computing exactly the same digest words.

Each message costs a counted 708-operation inner body plus 35 operations of
table and loop work (charged as 752). The total is T < 2^126.4357 charged
units, time_log2 = 126.44, with success probability 0.39 under one declared
heuristic (H1). This is not a differential attack on SHA-256. The
improvement over a whole-compression generic search is a constant factor.

This construction adopts the grouped single-block method, the W13 dependency
analysis and the after-round-30 early abort of the prior-art package at commit
15d0cb30 (sha256-r32, time_log2 126.695, in review), citing it as prior art.
The only change here is Section 4: the inner body is counted with the standard
reduced-operation round, which is independently verified bit-for-bit against
the reference digest.

## 1. Exact complete hash

A message is 55 bytes. FIPS 180-4 padding appends 0x80 and the 64-bit
big-endian bit length 440, with zero padding bytes (55 + 1 + 8 = 64). So the
padded input is exactly one block, with big-endian words

    W0..W12  = message bytes 0..51
    W13      = (u << 8) | 0x80,  u = message bytes 52..54 (24 bits)
    W14 = 0, W15 = 440.

Each compression executes rounds 0..31 only. The schedule is
W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16} (mod 2^32) for t = 16..31,
with s0(x) = ROR7 ^ ROR18 ^ SHR3 and s1(x) = ROR17 ^ ROR19 ^ SHR10. Round t
computes

    T1 = h + S1(e) + Ch(e,f,g) + K_t + W_t,   T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

with S0 = ROR2 ^ ROR13 ^ ROR22, S1 = ROR6 ^ ROR11 ^ ROR25,
Ch = (e&f)^(~e&g), Maj = (a&b)^(a&c)^(b&c), all modulo 2^32, and the standard
IV and K_t at their original indices. The digest is
H_i = IV_i + s_i (mod 2^32) in standard big-endian order, where
s = (A31, A30, A29, A28, E31, E30, E29, E28) is the working state after round
31 and A_t, E_t denote the new a and e words produced by round t. This is the
complete hash `verifier/hash_functions.py:digest(m, "sha256", 32)` on the
declared domain, not a free-start or compression-only result. The final
collision is re-verified with two whole compressions of the reference hash.

Since H_i = IV_i + s_i with a fixed IV, two messages have equal digests if and
only if their final working states are equal.

## 2. Where W13 enters

W13 is first used in round 13, so the state after rounds 0..12 is a group
constant. Its schedule uses are t = 20 (W_{t-7}), 28 (W_{t-15}) and 29
(W_{t-16}). Through the recurrence, W20, W22, W24, W26, W27, W28, W29, W30 and
W31 depend on W13, while W16, W17, W18, W19, W21, W23 and W25 do not. Those
seven are group constants.

In round 13, every input except W13 is a group constant. With
T13 = h + S1(e) + Ch(e,f,g) + K13 and A13 = T13 + S0(a) + Maj(a,b,c), both
precomputed unreduced, the round is

    a' = (A13 + W13) & M,   e' = (d + T13 + W13) & M          (4 operations)

and correctness follows from (x mod 2^32 + y) mod 2^32 = (x + y) mod 2^32.

In round 14, the b and c inputs are group constants, so Maj(a',b,c) =
(a' & (b|c)) | (b&c) with b|c and b&c precomputed (2 operations). Every
schedule word that depends on W13 keeps its group-invariant summands
pre-added:

    W20 = P20 + W13                 P20 = s1(W18) + s0(W5) + W4
    W22 = s1(W20) + P22             P22 = W15 + s0(W7) + W6
    W24 = s1(W22) + P24             P24 = W17 + s0(W9) + W8
    W26 = s1(W24) + P26             P26 = W19 + s0(W11) + W10
    W27 = W20 + P27                 P27 = s1(W25) + s0(W12) + W11
    W28 = s1(W26) + s0(W13) + P28   P28 = W21 + W12
    W29 = s1(W27) + W22 + W13 + P29 P29 = s0(W14)
    W30 = s1(W28) + P30             P30 = W23 + s0(W15) + W14

Rounds 14..19, 21, 23 and 25 use precomputed K_t + W_t.

## 3. Early abort after round 30

After round 30 the working state is (A30, A29, A28, A27, E30, E29, E28, E27).
The six words A30, A29, A28, E30, E29, E28 are final state words s1, s2, s3,
s5, s6, s7 (round 31 only shifts them). Define the 192-bit key

    K = A30 || A29 || A28 || E30 || E29 || E28.

Equal digests imply equal K. The search therefore stores and compares K and
never computes round 31, W31 or the feed-forward. A K match is only a
candidate. It is confirmed by computing both complete digests (Section 5).

## 4. The two programs, the reduced round, and operation counts

Group setup (once per group, prefix W0..W12): rounds 0..12, the seven
independent schedule words, T13, A13, d+T13, round-14 precomputations, nine
K_t + W_t sums and P20..P30. These are 27 group constants.

Inner body (once per message, input u): W13 = (u<<8)|0x80; round 13 as above;
round 14 with the Maj shortcut; rounds 15..30 in full; the eight dependent
schedule words W20..W30 from their pre-added forms. `inner` in
`experiments/grouped_birthday.py` is this exact code.

Counting convention: one operation per 256-bit add, AND, OR, XOR, NOT or
shift, exactly as counted by `scripts/reference_operation_costs.py`, which
tallies each executed word operation (it assumes no native 32/64-bit rotate).
Under this convention the cost of each primitive is the number of word
operations actually written. The inner body uses three standard, value-exact
identities to minimise that written count:

- **Deferred masks in the Sigma and sigma functions.** A 32-bit right rotation
  of a reduced word x is normally ((x>>r) | (x<<(32-r))) & M, four operations.
  The final `& M` can be dropped: the low 32 bits of (x>>r) | (x<<(32-r)) are
  already the rotated value, and the upper bits are discarded by the next
  reduction. S0(a) = ROR2 ^ ROR13 ^ ROR22 and S1(e) = ROR6 ^ ROR11 ^ ROR25
  each cost three unmasked rotations (3 operations each) plus two XOR, so 11
  operations. The result feeds only the modular additions T1 = h + S1(e) +
  Ch + (K+W) and T2 = S0(a) + Maj, whose values are H_i-correct because
  (A + B) mod 2^32 depends only on A, B mod 2^32, and T1, T2 are consumed only
  as a' = (T1+T2) & M and e' = (d + T1) & M, which mask. Each schedule word is
  also reduced before it is rotated (W20 = (P20+W13) & M and the rest), so the
  message-schedule s0, s1 likewise drop their internal rotation masks, costing
  9 operations each. a and e stay reduced every round, so Sigma inputs are
  always reduced.
- **Ch(e,f,g) = g ^ (e & (f ^ g)).** Three operations (XOR, AND, XOR) instead
  of (e&f) ^ (~e&g). Bit t selects f_t when e_t = 1, else g_t, which is Ch.
- **Maj(a,b,c) = b ^ ((a ^ b) & (b ^ c)).** Verified by its truth table.
  Because the next round's (b, c) equals this round's (a, b), the term
  (b ^ c) of round t+1 equals (a ^ b) of round t, computed as part of Maj and
  carried forward. Each round therefore computes a ^ b (1 op), reuses the
  carried b ^ c, ANDs (1 op) and XORs with b (1 op): 3 operations.

One full reduced round costs 11 (S1) + 3 (Ch) + 3 (adds into T1) + 11 (S0) +
3 (Maj, with the carried term) + 1 (T2) + 2 (a') + 2 (e') = 36 operations,
against 44 for the masked, non-identity round. The inner body is round 13
(4 operations), round 14 with the Maj shortcut, rounds 15..30 at 36 operations
each, and the eight W13-dependent schedule words from their pre-added forms
(each a reduced s1 or s0 of 9 operations plus one or two additions, or 2
operations for W20 and W27). Applying the counter to the whole inner body gives
exactly **708** operations. The same counter applied to the masked,
non-identity round (four-operation rotations, Ch = (e&f)^(~e&g), Maj =
(a&(b|c))|(b&c)) reproduces **856** for the identical computation, and a
white-box whole compression costs 1840.

The identities change no computed value. `experiments/grouped_birthday.py`
runs this exact reduced evaluator, and 3,000 random (prefix, u) evaluations
matched the six corresponding words of the reference digest
`digest(m, "sha256", 32)` minus IV bit for bit (zero mismatches); the two
declared experiments return genuine messages that the organizer recomputes
with the trusted digest, which checks the 708-operation body end to end. The
inner body is 0.385 of a whole compression: the saving is work that is
provably identical across a group, one skipped round, and the reduced round.

## 5. Complete algorithm

Parameters: L = 2^24 messages per group, G = 2^104 groups, N = G*L = 2^128,
sparse index width s = 140, verification cap V_max = 2^90.

Memory: prefix table PT (two 256-bit words per group), record array R
(K, id) of up to N records, and a sparse array P of 2^s one-word entries.
P is never initialised; R is written before it is read; n counts records.

For g = 0 .. G-1:

1. Draw two fresh independent uniform 256-bit words r0, r1 and store them at
   PT[g]. Set W_k = (r0 >> 32k) & M for k = 0..7 and W_{8+k} = (r1 >> 32k) & M
   for k = 0..4.
2. Run group setup. Set Gid = g << 24.
3. For u = 0 .. 2^24 - 1: run the inner body, pack K = A30<<160 | A29<<128 |
   A28<<96 | E30<<64 | E29<<32 | E28 (10 operations), set id = Gid | u, then:

        idx = K >> (192-s); pa = Pbase + (idx << 5); r = load P[idx]
        if r < n:                                   # R[r] is a real record
            ra = Rbase + (r << 6); k2 = load R[r].key
            if k2 == K: go to CONFIRM
            if (k2 >> (192-s)) == idx: go to NEXT   # slot held by another key
        INSERT: ra = Rbase + (n << 6); store R[n].key = K;
                store R[n].id = id (address ra + 32); store P[idx] = n; n = n + 1
        NEXT:   u = u + 1; if u < 2^24 repeat

4. CONFIRM: increment a counter v; if v > V_max halt with failure. Decode both
   ids (g' = id >> 24, u' = id & (2^24-1)), rebuild both 55-byte messages from
   PT, check that they differ, compute both complete reference digests (two
   whole compressions) and compare all eight words. If they are equal, output
   the pair and halt; otherwise go to NEXT, discarding the current message.

If the loops finish, halt with failure.

## 6. Correctness

Every evaluated message is a 55-byte string in the domain, and ids decode
uniquely. Sparse-set invariant (Briggs and Torczon): P may hold arbitrary
values; R[0..n-1] are genuine records. A slot idx is occupied iff
P[idx] = r < n and R[r].key >> (192-s) = idx. Inserts only fill unoccupied
slots, and an occupied slot is never overwritten. So it holds the first
stored record with that index.

Lemma. If record i is stored and a later message j has the same digest, then
K_j = K_i and idx(j) = idx(i), so CONFIRM runs on (i, j) at j unless the run
already ended. CONFIRM accepts exactly when the two complete reference digests
agree and the messages differ. Every output is therefore an ordinary full
256-bit collision of complete 32-round SHA-256.

A record i is not stored only if, when it arrived, its slot held a record k
with idx(k) = idx(i) and K_k != K_i, or a record with K_k = K_i but a
different digest (a rejected candidate).

## 7. Success probability

The coins are the 2G words r0, r1. Failure requires one of:

- F1: no two of the N messages have equal digests;
- F2: some digest-colliding pair (i < j) has i unstored, because an earlier k
  had idx(k) = idx(i) with K_k != K_i, or K_k = K_i with a different digest;
- F3: two groups draw identical 416-bit prefixes, with probability at most
  C(G,2) 2^-416 < 2^-209;
- F4: more than V_max candidate confirmations.

Heuristic H1 treats the N digests (and their K projections) as independent
uniform values for these events. Then
Pr[F1] <= exp(-N(N-1)/2^257) < 0.606531. For F2, the expected number of
triples (k, i, j) with k < i, j != i, idx(k) = idx(i) and equal digests
(i, j) is at most N^3 2^-s 2^-256 / 2 = 2^(127-s) = 2^-13. Each message causes
at most one confirmation, against the single occupant of its slot, and a
non-colliding occupant has an equal K with probability 2^-192. So the
expected number of confirmations is at most N^2 2^-192 = 2^64, and
Pr[F4] <= 2^64/V_max = 2^-26 by Markov. Hence

    Pr[success] >= 1 - 0.606531 - 2^-13 - 2^-26 - 2^-209 > 0.39334.

The claim is 0.39, keeping a 0.0033 allowance for deviation from the model.
The value is algorithmic success probability over the coins, not confidence in
H1. Cross-group pairs with the same u collide with probability >= 2^-256 for
any fixed function (Cauchy-Schwarz over uniform prefixes). Within-group pairs
are a 2^-104 fraction of all pairs.

## 8. Charged time

Per message, worst-case path (insert after the full slot check):

| Work | Operations |
| --- | ---: |
| inner body (Sections 2-4, reduced round) | 708 |
| pack K | 10 |
| id = Gid OR u | 1 |
| table step: 5 shifts, 4 address adds, 2 loads, 3 compares, 3 branches, 3 stores, n+1 | 21 |
| loop: u+1, compare, branch | 3 |
| counted total | 743 |
| charged | 752 |

Machine: 256-bit word RAM with 64 registers, three-address operations and
immediate shift counts. Registers hold MASK, 0x80, the 27 group constants, the
eight round constants K20 and K22, K24 and K26..K30, the 8 working-state
words, the carried Maj term, at most 6 live dependent schedule words, 4
temporaries and 5 loop/table registers: 61 in total. If every one of the 35
group and round constants were instead loaded from memory for each message,
the count would be 778 (Section 10).

Per group (G = 2^104 times), at most 2048 operations are
charged: 2 random draws, 24 unpacking operations, 5 to store PT[g], the group
setup, Gid, u reset and loop control. Once: global setup of at most 2^12
operations. Confirmations: at most V_max = 2^90, each at most two whole
compressions plus 2^10 operations.

    T <= N*752/2224 + G*2048/2224 + V_max*(2 + 2^10/2224) + 2^12/2224
       = 2^128 * 0.3381295... + 2^103.88 + 2^91.3 + 2
       < 0.3381296 * 2^128.

log2(0.3381296) = -1.564304, so T < 2^126.43570 and the claim is
time_log2 = 126.44. This caps every run. It includes random draws, failed
and discarded messages, table work, confirmations, verification and setup.
The two whole compressions per confirmation are charged at one unit each;
everything else, including all partial evaluations, is charged per word
operation. Nothing is charged twice or omitted.

## 9. Memory and other resources

P: 2^140 words of 32 bytes = 2^145 bytes. R: at most 2^128 records of 64
bytes = 2^134 bytes. PT: 2^104 * 64 bytes = 2^110 bytes. Code and constants
are under 2^24 bytes. Peak < 2^146 bytes; memory_log2_bytes = 146. P is never
initialised and costs no time. preprocessing_log2 = 0 covers global setup.
There is no nonuniform advice.

## 10. Sensitivity

| Variation | Bound |
| --- | ---: |
| As claimed (reduced round, 752 charged per message) | 2^126.4357 |
| All 35 group and round constants reloaded per message (778 charged) | 2^126.4847 |
| Rotations kept masked (4 ops) but Ch and Maj reduced (859 charged) | 2^126.6276 |
| Masked rotations and non-identity Ch, Maj (the 856/900 reading) | 2^126.6948 |
| Rotations charged five operations as in the reference script's `_rol` (940 body, 975 charged) | 2^126.8103 |
| A whole compression per message instead (rejects Sections 2-4) | about 2^128.02 |

Even under the strictest five-operation rotation reading, the Ch and Maj
identities (which are independent of the rotation convention) keep the bound
at 2^126.82, below the 856/900 reading's 2^126.695.

## 11. Evidence

Experiments s256-grouped-spread (16 groups x 32 consecutive u) and
s256-single-group (1 group x 512 consecutive u) run the exact reduced grouped
evaluator with N_t = 512 = 2^(18/2) messages per organizer seed, against an
18-bit masked event on digest words H1, H2, H3, H5, H6 and H7. N_t^2/2^18 =
1 = N^2/2^256, so this is the exact scaled analogue of the full attack. The
program computes those six digest words only through the reduced grouped
evaluator (IV plus the after-round-30 state). The organizer recomputes every
returned pair with the trusted digest, which checks the 708-operation body on
genuine messages. Random-model success per trial is
1 - prod_{i<512}(1 - i/2^18) = 0.39307; untrusted observations report
masked-equal pair counts (expected 0.4990 per trial).

Local replay with locally chosen seeds (not organizer evidence), using the
same `trial` function: the spread layout over 4096 trials gave 1624 successes
(model 1610.0, z = +0.45) and 2072 masked pairs (expected 2044). 103 first
matches were within a group, against 31/511 = 6.1% of 1624 = 99 expected. The
single-group layout over 12288 trials gave 4816 successes (model 4830,
z = -0.26) and 6104 masked pairs (expected 6132).

## 12. Limitations

H1 is a heuristic, tested on masked 18-bit projections, not the full event.
Organizer seeds are public. The register machine is a modelling assumption;
Section 10 gives alternatives. This is a constant-factor improvement from
single-block messages, amortised group-invariant work, early abort and a
reduced-operation round. It is not a cryptanalytic weakness of SHA-256 and not
a Pareto improvement (memory is very large). The nominal reference identifier
sha256-r32-nominal-v2 is metadata, not a claimed improvement over a qualified
baseline. The grouped single-block method and early abort are adopted from the
prior-art package at commit 15d0cb30, cited as prior art; the reduced-operation
round is the change introduced here.
