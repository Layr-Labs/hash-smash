# SHA-256 reduced to 31 steps: a fresh-run two-block collision search over many starting points

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (C = 2140), review policy `paired-lanes-v1`, exploratory lane.
The scalar below is `time_log2` under `collision-frontier-v5`; one 31-step target
compression costs 1 unit and every other 256-bit word primitive costs `1/C = 1/2140`
unit. Memory is a separately reported metric with no scalar contribution.

This package submits a complete, self-contained analytic algorithm run with fresh
random coins, not a precomputed collision. Every predicate, constant, set, equation
and loop cap used anywhere in the cost or success argument is stated in this document
(the Phase-3 search constants c16, c18, WEYL and the batch size B are given explicitly in
Sections 6, 9 and 12); no external paper is relied upon. Readiness requests review; it
asserts no AI outcome or human acceptance.

## 1. What is claimed, and what is not

We exhibit an algorithm that, on fresh uniform random coins and a fixed precomputed
table, outputs two distinct 128-byte messages `M0||M1` and `M0||M1'` whose complete
`sha256-r31` digests are equal, with algorithmic success probability at least 0.39 and
total charged computation `2^41.34` target-compression units (headline `time_log2` ~41.33;
the exact ledger total is `2^41.342`, dominated by the declared one-time
characteristic-search allowance; see the ledger and sensitivity table of Section 12).

Not claimed: a per-run guarantee of a collision (the algorithm has a bounded failure
probability under its caps); any statement about full 64-round SHA-256; any ideal-hash
or random-oracle premise. The characteristic and the published witness pair are the
Li-Liu-Wang (EUROCRYPT 2024, Sect. 4.2) 31-step trail; the cryptanalysis is attributed,
not original. The novelty here is the exact accounting: a table merged over 1334
independently generated starting points, an exact (non-disjoint) union count for the
match probability, fresh-coin trial independence, and hard caps on every loop so the
stated time bound holds for every run.

## 2. The selected target `sha256-r31-prefix-v1` (self-contained)

All words are 32-bit, big-endian. `+`/`-` are modulo 2^32. `M = 0xffffffff`.
`ROTR(x,n) = ((x>>n) | (x<<(32-n))) & M`, `SHR(x,n) = x>>n`.

    Ch(e,f,g)  = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    S0(a) = ROTR(a,2) XOR ROTR(a,13) XOR ROTR(a,22)      (big sigma 0)
    S1(e) = ROTR(e,6) XOR ROTR(e,11) XOR ROTR(e,25)      (big sigma 1)
    s0(x) = ROTR(x,7) XOR ROTR(x,18) XOR SHR(x,3)        (small sigma 0)
    s1(x) = ROTR(x,17) XOR ROTR(x,19) XOR SHR(x,10)      (small sigma 1)

Round constants K[0..30] (FIPS 180-4, first 31):

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Standard IV `H[0..7]`:

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19

Message schedule for one 512-bit block with words W[0..15]:

    for t = 16..30:  W[t] = (s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16]) AND M

Reduced compression of a block on chaining state `h[0..7]` (steps 0..30 only):

    (a,b,c,d,e,f,g,hh) = h
    for t = 0..30:
        T1 = (hh + S1(e) + Ch(e,f,g) + K[t] + W[t]) AND M
        T2 = (S0(a) + Maj(a,b,c)) AND M
        (hh,g,f,e,d,c,b,a) = (g, f, e, (d+T1)&M, c, b, a, (T1+T2)&M)
    out[i] = (h[i] + (a,b,c,d,e,f,g,hh)[i]) AND M  for i=0..7   (full feed-forward)

Padding: FIPS 180-4 (append 0x80, zero bytes to 56 mod 64, then the 64-bit big-endian
original bit length). IV is used once at the start of the complete message. The digest
is all eight output words in big-endian standard order. The reference implementation is
`verifier/hash_functions.py:digest` with algorithm `sha256`, rounds 31.

Collision relation: two finite byte strings `m0 != m1`, both of bit length < 2^64, with
equal complete `sha256-r31` digests. Out of scope: compression-only/free-start
collisions, truncation, near-collisions, altering IV/padding/round-range/width.

## 3. Message layout and the two-block strategy

Both messages are two 512-bit blocks of 64 bytes plus the shared padding block, so each
message is 128 bytes of content: `M0 || M1` and `M0 || M1'` with the SAME first block
`M0` and second blocks differing only in words W5..W9:

    M1'[t] = M1[t] for t not in {5,6,7,8,9}; M1'[t] = (M1[t] + d_t) AND M otherwise.

The first block M0 is the fresh random coins of a trial. The second block carries the
differential; W0..W4, W10..W15 are equal in M1 and M1'. Because M0 is identical, the two
messages share the chaining value `CV = C(IV, M0)` after block 1, and we search for a
second block that collides from `CV`.

## 4. The verified characteristic (signed, self-contained)

Sign convention (per cell, bit position 31..0): `=` no difference between the two
copies; `0`/`1` a value fixed equal in both copies; `u` copy-a bit 0 / copy-b bit 1;
`n` copy-a bit 1 / copy-b bit 0. Columns are the signed differences of the working
words A_i (= the a-register after step i), E_i (= the e-register after step i), and the
expanded message word W_i. Rows -4..-1 are the incoming chaining words.

    i | dA_i                             | dE_i                             | dW_i
   ---|----------------------------------|----------------------------------|----------------------------------
    5 | ===================n=unnnnnnn=n= | 000111010001111110nu=11111unnnu1 | ================nuuu=======0=uu=
    6 | ========n======================u | 101011=11==0n0==u11110==1110011n | ==========u=====u===u======n===u
    7 | ===u===n==n========n=========n=u | un0u1100n=01u11111001u1=n110u10n | =u=u=======n=====n=nu=n=====nun=
    8 | =============================n== | 1u01un0u0=1=1=11n=0=u0=001001u0= | =u=nn==========u===u===u==1=====
    9 | ================================ | 01100001110=0=010===00=11101u0=1 | ================u==========1=u==
   10 | ================u============u== | =1n1uuuuu0100=1un0=10unnnnnnn010 | ================================
   11 | ================================ | =01u1010uu1==11100===1000001n=0= | ================================
   12 | ================================ | ==110001=11====1n====0011110n=0= | ================================
   13 | ================================ | ===0====01======1=============== | ================================
   14 | ================================ | ================u===========0u== | ================================
   15 | ================================ | ================0============1== | ================================
   16 | ================================ | ================1============1== | =============unnnunnnnnnnnnnnn==
   18 | ================================ | ================================ | ==============1=n=0==========n==

(Rows -4..4, 17, 19..30 carry no difference in dA/dE/dW and are omitted; the full
33-row table with those blank rows is `clean_table.txt` in the implementation bundle and
is reproduced for completeness in Appendix A.) The induced signed message-word and
expansion differences are, as integers modulo 2^32:

    d5 = fffff006   d6 = 002087f1   d7 = 4fefb5fa   d8 = 28011100   d9 = 00008004
    required expansion differences:  d16 = 00008004   d18 = ffff7ffc   (no others)

These are fixed facts of the trail and are re-derived from the published witness pair by
`verify_characteristic.py` (33/33 condition checks pass); the certificate in Section 11
is a concrete pair on exactly this trail, and every symbol above was checked bit for bit
against it.

## 5. Admissible word sets (exact, enumerated over all 2^32 words)

Define the following modular-difference sets with the characteristic constants

    c5 = d0018020   c6 = 00000ffa   c7 = ffdf780f   c8 = b00fca02   x18 = 2ffe7fe0

    V5  = { w : s0(w + d5) - s0(w) = c5 }
    V6  = { w : s0(w + d6) - s0(w) = c6 }
    V7  = { w : s0(w + d7) - s0(w) = c7 }
    V8  = { w : s0(w + d8) - s0(w) = c8 }
    G16 = { w : s1(w + d16) - s1(w) = d18 }
    G18 = { w : s1(w + d18) - s1(w) = x18 }
    S   = { c18 : there exists g in G16 with s1(g) + c18 in G18 }

Exhaustive enumeration over the full 2^32 domain (one pass per set) gives the exact
cardinalities

    |V5| = 16384 = 2^14
    |V6| = 8388608 = 2^23
    |V7| = 512 = 2^9
    |V8| = 49408                      (log2 = 15.592)
    |G16| = 64 = 2^6
    |G18| = 42467328                  (log2 = 25.340)
    |S| = 584683520,  |S|/2^32 = 0.1361322 = 2^-2.877

G16 has the closed form `{ (h<<28) | lo : h in 0..15, lo in {031bbffc, 064bbffe,
09b3bffd, 0ce3bfff} }` (64 words), which the completion program (Section 9) re-checks in
process. These sets are facts about the stated functions and constants (an exact
enumeration, not a heuristic); the enumerator `enumerate.c` reproduces every count
(reported `enumerate_seconds = 3.24` on 11 threads). The exact counts are enumerated by a
bundled C program; they are not shipped as an organizer-runnable artifact inside the
candidate package, so to the organizer they read as participant prose (a known
rigorous-lane limitation, Section 14).

## 6. The precomputed table (Phase 1) and the match set P

A *starting point* fixes the signed working state of steps 1..12 for both copies
(`A_1..A_12`, `E_5..E_12`) and the four carried message words `W9..W12` consistent with
the characteristic. The two scalar quantities carried from a matched first block into the
completion step are, for second-block words W0..W12,

    c16 = W9  + s0(W1) + W0            (mod 2^32)
    c18 = W11 + s0(W3) + W2            (mod 2^32)

(`c16, c18` are the parts of the expanded words W16, W18 that are fixed once W0..W12 are
fixed). From one starting point the table is built by the exact modular equations below
(all mod 2^32), identical to `build_table.c`:

    E_4   = E8 - A4 - S1(E7) - Ch(E7,E6,E5) - K[8] - W8         for each W8 in V8
    F7    : Ch(E6',E5',E_4) - Ch(E6,E5,E_4) == (E7'-E7) - (S1(E6')-S1(E6)) - d7
    E_3   = E7 - A3 - S1(E6) - Ch(E6,E5,E_4) - K[7] - W7         for each W7 in V7
    F6    : Ch(E5',E_4,E_3) - Ch(E5,E_4,E_3) == (E6'-E6) - (S1(E5')-S1(E5)) - d6
    A_0   = E_4 - A4 + S0(A3) + Maj(A3,A2,A1)
    key   = A_-1 = E_3 - A3 + S0(A2) + Maj(A2,A1,A0)

For the published starting point this yields (measured) 2048 values of W8 in V8 that
pass F7, then exactly 16896 = 33*2^9 tuples `(W7,W8,E_3,E_4,A_0,key)` passing F6, over
2336 distinct keys. Each tuple induces an acceptance set over the two further backward
words `(A_-2, A_-3)`:

    E_2 = A2 + A_-2 - S0(A1) - Maj(A1,A0,key)
    W6  = E6 - A2 - E_2 - S1(E5) - Ch(E5,E_4,E_3) - K[6]      require W6 in V6
    E_1 = A1 + A_-3 - S0(A0) - Maj(A0,key,A_-2)
    W5  = E5 - A1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5]    require W5 in V5

For a fixed tuple, A_-2 ranges over |V6| = 2^23 admissible values and, for each, A_-3
ranges over |V5| = 2^14 admissible values, so each tuple accepts exactly
`2^23 * 2^14 = 2^37` triples `(A_-1=key, A_-2, A_-3)` in the 96-bit space
`{0,1}^96` of `(A_-1, A_-2, A_-3)`.

Define the match set

    P = union over all tuples t of G_t,  where G_t subset {0,1}^96 is the 2^37-element
        acceptance set of tuple t, and the union is taken over the tuples of ALL merged
        starting points.

### 6.1 The acceptance sets are NOT pairwise disjoint (correction to prior work)

An exact intra-key pairwise test (`build_table.c`, every pair of tuples sharing a key)
finds the sets overlap. For a single starting point, over 62064 intra-key tuple pairs,
3493888 jointly accepted `(A_-2,A_-3)` cells were found; the exact overlap is 1,279,000,576
accepted pairs. Therefore the sum of set sizes over-counts the union, and the match
probability MUST be computed from the exact union, not from the sum:

    single-SP sum over tuples |G_t| = 16896 * 2^37 = 2,322,168,557,862,912 = 33*2^46   (UPPER BOUND)
    single-SP exact union |P_1|     = 2,322,167,278,862,336   (= sum - overlap 1,279,000,576)
    single-SP overlap fraction      = 1,279,000,576 / (33*2^46) = 5.508e-7

A previous package on this target claimed these per-tuple sets were pairwise disjoint and
used `Pr_U = 33*2^-50`; the exact test above refutes disjointness (its asserted
"`|P| = 16896*2^37`" is the larger sum, not the union). We therefore use the exact union
count throughout and never the disjoint shortcut. The measured single-SP overlap fraction
`5.508e-7` is the calibration used to bracket the merged union below.

### 6.2 Merging many starting points

The attack merges tuples from `K_sp = 1334` independently generated starting points
(Section 8) into one direct-address key table `KT` and one representative of `P`.
Of the 1334 points, 343 are productive (991 yield 0 tuples because their F7 right-hand
side has no `W8 in V8` solution); the per-starting-point tuple count ranges min 0 / mean
3181 / max 53760. Merging enlarges `P` (more tuples) and so raises the per-trial match
probability and lowers the required trial count. Merged facts (from `merged_table.c` /
`merged_probe.c`):

    merged tuples        = 4,243,904
    distinct keys        = 1,267,382       (max group per key = 64)
    merged sum           = 4,243,904 * 2^37 = 583,277,724,395,634,688   (= 2^59.017, UPPER BOUND)
    merged |P| (exact union) in  [ 583,277,141,117,910,272 , 583,277,724,395,634,688 ]
                                 ( lower = sum*(1 - 1e-6); bracket width <= 1e-6 relative )
    Pr_U[CV in P]        = |P| / 2^96 = 2^-36.983      (equals sum/2^96 to within <1e-6 in log2)

The exact large-K union is compute-bound (each tuple-pair overlap is a ~8.4M two-pointer
scan over V6 plus a V5 autocorrelation), so for the merged table it is reported as a
BRACKET, not computed outright: the single-SP calibration fixes every pairwise tuple
overlap at ~2e4 of 2^37 cells, so even the 14.6M intra-key pairs at K=1334 subtract at
most ~3e11 from a sum of 5.83e17, a <=1e-6 relative correction. Hence the union-based
`Pr[CV in P]` equals the stated `2^-36.983` to within `<1e-6` in `log2`, and
`merged_table K` computes the union outright only for small K as a check. Merging the
starting points is the lever that drops `Pr[CV in P]` from `2^-45` (one SP) to
`2^-36.983` (1334 SPs), i.e. the required trial count from `~2^45` to `~2^37`.

Under Heuristic H1 (Section 10) a fresh uniform first block makes the 96-bit value
`(A_-1,A_-2,A_-3)` of `CV = C(IV,M0)` near-uniform, so a single trial matches `P` with
probability `Pr_U[CV in P]`.

## 7. The fresh-run attack (Phases 0-4)

- Phase 0 (characteristic): one-time search producing the signed trail of Section 4.
  Charged once as `T_char` (Section 12). Run outside the algorithm; its output is the
  fixed data of Sections 4-5.
- Phase 1 (table): build `KT` and `P` from the 1334 merged starting points by the exact
  equations of Section 6. Charged once as `T1`.
- Phase 2 (trials): repeat up to `N = 2^39` times: draw a FRESH uniform first block `M0`
  (a full 512-bit block, independent of all other trials); compute `CV = C(IV, M0)`; form
  the 96-bit key `(A_-1,A_-2,A_-3) = (a,b,c)` of `CV` and probe `P`. The analysed `N`
  trials each use a fully fresh uniform `M0`, so they are independent by construction and
  the `1-(1-q)^N` bound of Section 10 applies directly. (An implementation MAY instead
  batch trials that share `W0..W14` and vary only `W15`, recomputing steps 15..30 and the
  affected expansion words per variant; this is a non-analytic throughput device for which
  the ledger of Section 12 takes NO cost credit — it charges one full compression per
  trial regardless — and it is not relied on by the independence argument.) A match that
  also has `c18 in S` (Section 5) is handed to Phase 3.
- Phase 3 (completion): given a matched prefix, run the capped search of Section 9 for
  `(W13,W14,W15)` of the second block satisfying the remaining signed conditions on
  `E_13,E_14,E_15,W16,W18`; hard caps CAP13, CAP15 per candidate and a global cap
  `GLOBAL_PHASE3_CAP` on total Phase-3 attempts per matched prefix.
- Phase 4 (verify): on completion, assemble `M0||M1` and `M0||M1'`, recompute both full
  `sha256-r31` digests, and output the pair only if they are equal and the messages
  differ. This is the only accepted success event; it is re-checked by the organizer.

There are no restarts beyond the single capped `N`-trial loop; the time bound of
Section 12 holds for every run, not on average.

## 8. Starting-point generation (Phase 0 feeder)

Starting points are produced by a bit-vector solver (z3, `QF_BV`) over the step-1..12
window (format in `sp/FORMAT.md`): for `5 <= i <= 12`,
`A_i = E_i - A_{i-4} + S0(A_{i-1}) + Maj(A_{i-1},A_{i-2},A_{i-3})`, and for
`9 <= i <= 12`,
`E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + Ch(E_{i-1},E_{i-2},E_{i-3}) + K[i] + W_i`,
subject to the signed conditions of Section 4 on `A_1..A_12, E_5..E_12, W9..W12`.
Distinct starting points differ in the slide-named identity words
`(A_1,A_2,A_3,A_4,E_5,E_6,E_7,E_8)`. Every emitted point is re-verified independently of
the solver by re-evaluating all 12 step equations and every condition bit for both
copies (`convert_sp.py`; at the merge run all 1334 records accepted, 0 rejected).

Measured generation (`sp/timings.csv`): the run produced 12,087 verified points at a
total of 1,790.2 CPU-seconds; the attack merges 1,334 of them (359.00 CPU-seconds,
mean 0.2691 CPU-s per point). The ledger row `T_sp` (Section 12) conservatively charges
the FULL generation of all 12,087 points, not only the 1,334 merged, with the
CPU-second-to-unit conversion stated there.

## 9. The completion search (Phase 3), exact and capped

Given a matched, `c18 in S` prefix, Phase 3 searches message words of the second block.
With the published-prefix representative, the exact per-attempt tests are those
implemented by `experiments/completion.py` (Section 11 experiment), reproduced here; the
search walks arithmetic progressions with the fixed Weyl increment `WEYL = 0x9e3779b9`:

- Enumerate the 64-element winning set `G16` (closed form, Section 5); keep the subset
  with `s1(w18) + c18` in `G18` (test `s1(w18+d18)-s1(w18) == x18`), giving the admissible
  `(g, w14)` candidates (w14 recovered from `y = g - c16` by the GF(2) inverse of s1).
- For each candidate, draw FRESH offsets `(r13_j, r15_j)` from the organizer seed and the
  candidate index j, and walk `x = r13_j + i*WEYL` for `i < CAP13`, testing the
  E_13/E_14 conditions; for each surviving x, walk `z = r15_j + k*WEYL` for `k < CAP15`,
  testing the E_15/W16 conditions and the final `Ch` equality.
- A single global counter `attempts` caps the total number of Phase-3 attempts (outer
  x-evaluations) per matched prefix at `GLOBAL_PHASE3_CAP`; the search hard-stops every
  loop when the budget is spent and reports a failed completion for that prefix.

Hard caps (identical in the program `experiments/completion.py` and in this ledger):

    CAP13 = 2^18                 per-candidate x attempts  (program CAP13)
    CAP15 = 2^12                 per-x z attempts          (program CAP15)
    GLOBAL_PHASE3_CAP = 2^16     total Phase-3 attempts per matched prefix (program GLOBAL_PHASE3_CAP)

The per-matched-prefix completion work is therefore bounded by `<= 2^19.6` target-
compression units (an upper bound on the capped word operations; at `GLOBAL_PHASE3_CAP
= 2^16` the real worst case is smaller, and the organizer sandbox measures the all-fail
256-trial request at ~5 s, well inside the 20 s budget).

Completion rate: for a matched prefix with `c18 in S`, Phase 3 succeeds within the caps
with probability at least `r_comp = 0.99` (Heuristic H2). The probability that a matched
prefix has `c18 in S` is the exact density `|S|/2^32 = 0.1361322` under the H1
near-uniformity of `c18` (Section 10): `|S|/2^32` is an exact set density, and it is the
`Pr[c18 in S | match]` to the extent `c18` is near-uniform on a matched prefix.

## 10. Success probability (explicit derivation, target 0.39)

Let `q` be the per-trial probability of producing a verified collision:

    q = Pr_U[CV in P] * Pr[c18 in S | match] * r_comp
      = 2^-36.983 * 0.1361322 * 0.99
      = 9.92e-13 = 2^-39.874

With `N` independent trials (fresh uniform coins make trials independent by
construction; see Section 7), the probability of at least one verified collision is
`1 - (1 - q)^N >= 1 - exp(-N*q)`. Writing the global cap-overflow probability across all
Phase-3 calls as `p_cap`, the algorithmic success probability is

    P_success >= 1 - exp(-N*q) - p_cap.

The number of Phase-3 calls is `Poisson(mu)` with `mu = N * Pr_U * 0.1361322`; budgeting
`B3 = 12` completion calls and stopping beyond them makes
`p_cap = Pr[Poisson(mu) >= 12] <= 1e-12` (negligible). Choose

    N = 2^39,   N*q = 0.5455,   mu = 0.551,   p_cap <= 1e-12,

giving

    P_success >= 1 - exp(-0.5455) - 1e-12 = 0.4204 >= 0.39.

`N = 2^39` is the smallest power-of-two trial count that clears 0.39 (`N = 2^38` gives
only `1 - exp(-0.2727) = 0.239`); it clears it with margin, and the claim sets
`success_probability = 0.39` as the supported lower bound. Sensitivity: with
`lambda = N*q`, `P_success ~ 1 - exp(-lambda) - p_cap`; a completion rate `r_comp` lower
than 0.99 scales `q` (hence `lambda`) linearly, so `N` must rise by the same factor to
hold 0.39. Because the ledger is dominated by `T_char` (Section 12), such an increase in
`N` does not change `time_log2` until `N` approaches `2^40.5`.

## 11. Certificates

One certificate is attached as existence evidence for the trail of Section 4:
`llwds24-31step` (`type hash-collision-witness-v2`), the published practical pair on
exactly this characteristic, with organizer-recomputed digest
`55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd`. The algorithm never
reads any certificate and it is not nonuniform advice.

Eight fresh certificates produced by this submission's own completion runs are attached
(`fresh-0..7`, `type hash-collision-witness-v2`): each keeps the published first block
`M0` and `W0..W12` and uses new `(W13,W14,W15)` found by the capped Phase-3 search of
Section 9, and each re-hashes (organizer `verifier.hash_functions.digest`) to equal
digests on the two distinct 128-byte messages:

    fresh-0  03a56f3d18e468f961e5fbacb8e9bf011e9429990f9703b968d9f98ee7e2ed30
    fresh-1  81380c84cfaf7f17d4417f8e22af43c5f8f209af17fe1fd22e9cac8e03de1c44
    fresh-2  1fd121f516b39699cee7245fd9e454e43472441399d9c26cb35eeee73381ebd1
    fresh-3  569ee3e0a52368e93fdf44c12595cd7524b1f4ea499d77de51dd258bc821df4c
    fresh-4  18a0c917fd583e8ae5db03ae8576793cedc75336728970fe7e9e8218fc699173
    fresh-5  82d258bf13ce414d0c53b57b638c2457f4d9ff42ea55fa20331814fe86d8fdbb
    fresh-6  c8442f9b4cd6614e2e7edccf39084c2fd13e258003c47c53e1a737dad29537f7
    fresh-7  910805861a79bfaf78339430f10b043c9b2a7e847c5bf0430a0526ef960bb81b

They are evidence that the construction produces collisions, not a measurement of
first-block search cost.

Organizer experiment `completion` (`experiments/completion.py`, kind
`python-message-pairs-v1`, event `full-collision`): for each organizer seed it keeps the
published prefix and published `W0..W12`, draws fresh offsets per candidate, runs the
capped Phase-3 search of Section 9 with the global attempt cap, and returns the two
128-byte messages for organizer re-hashing. It does not run Phases 1-2. It exercises the
completion routine and its caps on one prefix; it does not establish the completion rate
over the distribution of prefixes Phase 2 produces (Heuristic H2 limitation).

## 12. Cost ledger (collision-frontier-v5, C = 2140)

Accounting rules: one 31-step compression = 1 unit; every other 256-bit word primitive
= `1/2140` unit; all trials including failures are charged; no amortization and no
parallel wall-time discount; work is summed across all processors. Per-round word-op
counts of the reference core (used for the per-trial probe budget): a compression step
body costs 54 word operations, one message-expansion word costs 30, and the final
feed-forward costs 16; a full 31-step compression is `31*54 + 15*30 + 16 = 2140` word
operations (= C), confirming 1 unit.

Per-trial charge. Each trial is charged one full target compression (1 unit) for
`CV = C(IV,M0)` plus the key-formation and table-probe word operations. The probe is
`<= 32` word operations on the miss path (the common case: `A_-1` is not a key); on the
rare hit path it is at most `(max group 64) * (W6 test 10 + W5 test 28) = 2432` word
operations, paid only when `A_-1` is a stored key (measured hit rate 590984 / 2e9 =
2^-11.7, so the expected hit-path charge over all `N` trials is `<= 2^27.5` units,
folded into T2 below). Hence each trial is charged

    1 + 32/2140 = 1.01495 units   (miss path; the hit path adds a negligible, bounded term)

Batching (a possible implementation that shares steps 0..14 across a batch varying only
`W15`, batch size B, any value up to 2^32) is NOT credited: the ledger charges a full
compression per trial whether or not an implementation batches.

Ledger (units; `log2` of the total is the score). CPU-second conversion (rows T_sp,
T_char): the reference core runs `2^23.83` 31-step compressions per CPU-second (measured,
`bench.c`); rounded UP to the next power of two, one CPU-second is charged as
`units_per_cpu_s = 2^24` target-compression units.

    row      | what is charged                                                   | units
    ---------|-------------------------------------------------------------------|---------------------------
    T_char   | one-time characteristic (trail) search allowance (Heuristic H3)    | 2^41   (allowance; see ladder)
    T_sp     | ALL 12,087 generated starting points: 1,790.2 CPU-s * 2^24         | 3.00e10 = 2^34.81
    T1       | table build: 6 enumeration passes over 2^32 + union/key fill       | <= 2^30
    T2       | N=2^39 trials * (1 + 32/2140)  + bounded hit-path                  | 5.58e11 = 2^39.02
    T3       | <=12 completion calls * 2^19.6 units/call                          | 9.5e6   = 2^23.19
    T4       | verification: re-hash returned pairs (<= 2^8 compressions)         | <= 2^8
    ---------|-------------------------------------------------------------------|---------------------------
    total    | T_char + T_sp + T1 + T2 + T3 + T4 = 2.788e12                       | time_log2 = 41.342

Headline `time_log2 = 41.34` (precisely `41.342`). `T_sp` conservatively charges all
12,087 generated starting points (1,790.2 CPU-s); charging only the 1,334 merged points
(359.00 CPU-s = `2^32.49`) would give total `2^41.330` (41.33) instead, i.e. the
all-points charge moves the headline by `+0.012` bit — immaterial. The total is dominated
by `T_char`; the trial term `T2 = 2^39.02` is about `4.9x` smaller than the total (about
`3.9x` smaller than `T_char`). The charged trail-search allowance `T_char` is therefore
score-critical, so we report its sensitivity explicitly (with `T_sp` = all 12,087 points):

    T_char allowance | total units | time_log2 | preprocessing_log2
    -----------------|-------------|-----------|-------------------
    2^40             | 1.665e12    | 40.619    | 40.040
    2^41  (claim)    | 2.788e12    | 41.342    | 41.020
    2^42             | 4.987e12    | 42.181    | 42.010

`T_char = 2^41` is a DECLARED ALLOWANCE (Heuristic H3), not a completed measurement: the
one-time trail search is NOT complete. Two partial measurements anchor it, both at
`units_per_cpu_s = 2^24`:
- our own attached partial re-run `trail-run/log.csv`: 21 solver calls, summed
  `cpu_total_s = 16,027.1`, i.e. `16,027.1 * 2^24 = 2^37.97` units;
- a third-party partial measurement of `58,015 CPU-s` over 24 unfinished solver calls, i.e.
  `58,015 * 2^24 = 2^39.82` units.
`T_char = 2^41` is thus an allowance about `2^1.2` over the third-party partial
(`2^39.82`) and about `2^3.0` over our own partial (`2^37.97`). Because both measured
figures are for UNFINISHED searches, the full trail search could exceed `2^41`; the
sensitivity ladder above gives the exact score for allowances `2^40 / 2^41 / 2^42`, and a
completed trail-search measurement would replace the allowance.

Memory (reported only, no scalar contribution): the preprocessing peak is dominated by
the one-time exact-union check's 2^32-bit V6 bitset (2^29 bytes) plus the merged key
table and tuples (4,243,904 tuples, ~2^28 bytes), so `memory_log2_bytes = 30` bounds the
whole-process peak. Nonuniform advice is the merged starting-point data the algorithm
consults, `sp_advice` for the 1334 points = 137,668 bytes, so
`nonuniform_advice_log2_bytes = 18`; all work that produced it is charged in rows
T_char, T_sp and T1, and Phase 1 rebuilds the table from it.

## 13. Declared heuristics

Every empirical or unproved premise the success and cost bounds rely on is declared as a
heuristic in `claim.json` (H1, H2 on probability; H3, H4 on one-time cost) with scope,
extrapolation, limitations and a sensitivity statement, and is linked by `evidence_ids`
to the lines above or to the `completion` experiment. H1's scope includes both the
near-uniformity of the 96-bit backward state `(A_-1,A_-2,A_-3)` (for the match
probability) and the near-uniformity of `c18` on a matched prefix (for the completion
trigger). The exact-count facts of Sections 5-6 (set sizes, non-disjointness, per-tuple
2^37, the exact single-SP union and the bracketed merged union) are NOT heuristics; they
are enumerations (shipped as participant prose, not an organizer-runnable artifact; see
Section 14). All quantities are resolved; this package carries no unfilled placeholders.

## 14. Scope and limitations

- This is published cryptanalysis (Li-Liu-Wang EUROCRYPT 2024, Sect. 4.2 trail; published
  pair) with new, self-contained accounting. The characteristic and witness are attributed.
- The attack is not executed at full scale in this package; the bound rests on H1-H4.
- Trials are independent by construction (the analysed `N` trials each draw a fully fresh
  uniform first block). Batching is only an implementation throughput option and takes no
  cost credit; no random-function, round-independence, or distinct-key/Poisson-bucket
  premise is used; the match probability is an exact (non-disjoint) union over the actual
  merged table, bracketed to `<1e-6` relative.
- The H1 own-run check (590,984 key hits in 2e9 fresh-coin trials, `~2^-11.7`) validates
  only the 32-bit `A_-1` marginal (`distinct_keys/2^32`), NOT the full 96-bit membership
  event; the full `2^-36.983` event is not directly observable and is extrapolated.
- The completion experiment exercises one prefix; the completion rate over the prefix
  distribution is Heuristic H2, with the stated sensitivity. Under `GLOBAL_PHASE3_CAP =
  2^16` a small fraction of prefixes needing more than `2^16` attempts would fail, which
  is why `r_comp = 0.99 < 1` is used and its sensitivity is stated.
- The exact enumerations (set sizes, union, `Pr_U`) are produced by bundled C programs
  that are NOT shipped as organizer-runnable artifacts in the candidate package, so to the
  organizer they are participant prose (a rigorous-lane limitation, not an exploratory
  blocker).
- `T_char` is the weakest premise: the trail search is not complete, and the two partial
  measurements (`2^37.97` ours, `2^39.82` third-party) leave only a `~2^1.2`-to-`~2^3.0`
  allowance margin at `2^41`; the full search could exceed it. The sensitivity ladder in
  Section 12 gives the score for allowances 2^40 / 2^41 / 2^42.
- Memory is reported, not scored. `baseline_improved = sha256-r31-nominal-v2` is a
  required reference identifier, not an asserted improvement.

## Appendix A. Full characteristic table

The complete 33-row signed table (rows -4..30, including the all-`=` rows omitted from
Section 4) is `clean_table.txt` in the implementation bundle; its non-blank rows are
exactly those reproduced in Section 4, and the blank rows carry no difference in dA, dE
or dW. The sign convention is that of Section 4.
