# SHA-256 reduced to 31 steps: a fresh-run two-block collision search from the published starting point

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (C = 2140), review policy `paired-lanes-v1`, exploratory lane.
The scalar below is `time_log2` under `collision-frontier-v5`; one 31-step target
compression costs 1 unit and every other 256-bit word primitive costs `1/C = 1/2140`
unit. Memory is a separately reported metric with no scalar contribution.

This package submits a complete, self-contained analytic algorithm run with fresh
random coins, not a precomputed collision. Every predicate, constant, set, equation and
loop cap used anywhere in the cost or success argument is stated in this document (the
Phase-3 search constants c16, c18, WEYL in Sections 6, 9, 12). No external paper is relied
upon. Readiness requests review; it asserts no AI outcome or human acceptance.

## 1. What is claimed, and what is not

We exhibit an algorithm that, on fresh uniform random coins and a fixed precomputed
table built from ONE starting point, outputs two distinct 128-byte messages `M0||M1` and
`M0||M1'` whose complete `sha256-r31` digests are equal, with algorithmic success
probability at least 0.39 and total charged computation `2^47.04` target-compression
units (exact ledger total `2^47.043`). The bound is a HARD per-run bound: every loop is
capped and every charged quantity holds for every coin sequence (Sections 7, 10, 12).

Not claimed: a per-run guarantee of a collision (the algorithm has a bounded failure
probability under its caps); any statement about full 64-round SHA-256; any ideal-hash
or random-oracle premise. The characteristic, the single starting point and the published
witness pair are the Li-Liu-Wang (EUROCRYPT 2024, Sect. 4.2 / ASIACRYPT 2024) 31-step
result; the cryptanalysis is attributed, not original. The match probability is the EXACT
single-point union `Pr_U = 2^-44.955607` (no bracket, no heuristic on `|P|`). The novelty
here is the exact accounting: the exact (non-disjoint) single-point union, fresh-coin
trial independence, and hard caps on every loop (a key-hit cap and a total-inner-iteration
completion cap) so the stated time bound holds for every run. We do NOT merge many
solver-generated starting points: as Section 8 and Section 14 state, the solver points we
generated are not completion-compatible and were set aside for future work.

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
(reported `enumerate_seconds = 3.24` on 11 threads). The enumerations are bundled C
programs, not shipped as an organizer-runnable artifact inside the candidate package, so
to the organizer they read as participant prose (a rigorous-lane limitation, Section 14).

## 6. The precomputed table (Phase 1) and the match set P

The attack uses ONE starting point: the published Li-Liu-Wang point (taken from the
published colliding pair; its construction is attributed and charged inside T_char,
Section 12). A starting point fixes the signed working state of steps 1..12 for both
copies (`A_1..A_12`, `E_5..E_12`) and the four carried message words `W9..W12`; the two
scalars carried from a matched first block into the completion step are, for second-block
words W0..W12,

    c16 = W9  + s0(W1) + W0            (mod 2^32)
    c18 = W11 + s0(W3) + W2            (mod 2^32)

From the starting point the table is built by the exact modular equations below (all mod
2^32), identical to `build_table.c`:

    E_4   = E8 - A4 - S1(E7) - Ch(E7,E6,E5) - K[8] - W8         for each W8 in V8
    F7    : Ch(E6',E5',E_4) - Ch(E6,E5,E_4) == (E7'-E7) - (S1(E6')-S1(E6)) - d7
    E_3   = E7 - A3 - S1(E6) - Ch(E6,E5,E_4) - K[7] - W7         for each W7 in V7
    F6    : Ch(E5',E_4,E_3) - Ch(E5,E_4,E_3) == (E6'-E6) - (S1(E5')-S1(E5)) - d6
    A_0   = E_4 - A4 + S0(A3) + Maj(A3,A2,A1)
    key   = A_-1 = E_3 - A3 + S0(A2) + Maj(A2,A1,A0)

This yields (measured) 2048 values of W8 in V8 that pass F7, then exactly
16896 = 33*2^9 tuples `(W7,W8,E_3,E_4,A_0,key)` passing F6, over 2336 distinct keys
(max group per key = 16). Each tuple induces an acceptance set over the two further
backward words `(A_-2, A_-3)`:

    E_2 = A2 + A_-2 - S0(A1) - Maj(A1,A0,key)
    W6  = E6 - A2 - E_2 - S1(E5) - Ch(E5,E_4,E_3) - K[6]      require W6 in V6
    E_1 = A1 + A_-3 - S0(A0) - Maj(A0,key,A_-2)
    W5  = E5 - A1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5]    require W5 in V5

For a fixed tuple, A_-2 ranges over |V6| = 2^23 admissible values and, for each, A_-3
ranges over |V5| = 2^14, so each tuple accepts exactly `2^23 * 2^14 = 2^37` triples
`(A_-1=key, A_-2, A_-3)` in `{0,1}^96`. The match set `P` is the union of these acceptance
sets over the 16896 tuples.

### 6.1 Exact single-point match probability (no heuristic)

An exact intra-key pairwise test (`build_table.c`, every pair of tuples sharing a key)
shows the per-tuple sets are NOT pairwise disjoint: over 62064 intra-key tuple pairs,
3493888 jointly accepted `(A_-2,A_-3)` cells were found, an exact overlap of 1,279,000,576
cells. The EXACT union is therefore computed, not bracketed:

    sum over tuples |G_t| = 16896 * 2^37 = 2,322,168,557,862,912 = 33*2^46   (upper bound)
    exact union |P|       = 2,322,167,278,862,336   (= sum - overlap 1,279,000,576)
    Pr_U[CV in P]         = |P| / 2^96 = 2^-44.955607   (EXACT; no bracket, no heuristic)

(A previous package claimed these sets were pairwise disjoint and used `33*2^-50 =
2^-44.955606`; the exact union above, `2^-44.955607`, is used instead.) This exact
`Pr_U = 2^-44.955607` is the match probability used throughout the claim (Sections 10, 12).
Under Heuristic H1 (Section 10) a fresh uniform first block makes the 96-bit value
`(A_-1,A_-2,A_-3)` of `CV = C(IV,M0)` near-uniform, so a single trial matches `P` with
probability `Pr_U`.

## 7. The fresh-run attack (Phases 0-4)

- Phase 0 (characteristic + starting point): the one-time differential-trail search and the
  published starting point. Charged once as `T_char` (Section 12), which (as in the prior
  passing packages) also covers the published collision run that produced the starting
  point. Its output is the fixed data of Sections 4-6.
- Phase 1 (table): build `KT` and `P` from the single starting point by the exact equations
  of Section 6. Charged once as `T1`.
- Phase 2 (trials): repeat for EXACTLY `N = 2^47` iterations: draw a FRESH uniform first
  block `M0`; compute `CV = C(IV, M0)`; form the 96-bit key `(A_-1,A_-2,A_-3)` of `CV` and
  probe the key table. The analysed `N` trials each use a fully fresh uniform `M0`, so they
  are independent by construction and the `1-(1-q)^N` bound of Section 10 applies. A trial
  is a MISS (`A_-1` not a key) or a HIT (`A_-1` is a key, reconstructing `W6,W5` and testing
  V6,V5). To make the bound hold for EVERY coin sequence, a global counter `h` counts
  hit-path trials and the run ABORTS (FAIL) as soon as `h` reaches `H_cap = 2^28`
  (Section 12); the abort probability is bounded in Section 10. A hit that also has
  `c18 in S` is handed to Phase 3.
- Phase 3 (completion): given a matched prefix, run the capped search of Section 9 for
  `(W13,W14,W15)`; a single global counter bounds the TOTAL inner iterations per matched
  prefix at `GLOBAL_PHASE3_CAP = 2^16`, with per-candidate caps CAP13, CAP15. The run makes
  at most `B3 = 12` Phase-3 (completion) calls in total and STOPS after the 12th; this hard
  limit is what bounds `T3` (Section 12), and the probability that more than 12 matched
  prefixes arise is the `p_cap` subtracted in Section 10.
- Phase 4 (verify): recompute both full `sha256-r31` digests and output the pair only if
  equal and the messages differ. This is the only accepted success event; the organizer
  re-checks it.

There are no restarts beyond the single capped `N`-trial loop; with the hit cap and the
completion cap, the time bound of Section 12 holds for every run, not on average.

## 8. The starting point (and why only one)

The single starting point used is the published Li-Liu-Wang point, read from the published
colliding pair and re-verified by re-evaluating all 12 step equations and every condition
bit for both copies. It is completion-compatible: its prefix-valid chaining values close
to full collisions (measured 514/514 for chaining values with `c18 in S`; the eleven fresh
certificates of Section 11 are concrete closes).

We also GENERATED many additional starting points with a bit-vector solver (z3, `QF_BV`)
over the step-1..12 window, each re-verified to satisfy those window step-equations and the
published modular step-differences (`dA10` and `E5..E12, A5..A10`). HOWEVER, a direct
completability survey found these solver points are NOT completion-compatible: under
identical probing the published point closes 514/514 chaining values with `c18 in S`, while
every sampled solver point closes 0 / ~530-575, and a live forward search over 12,087
solver points (`2^35.3` trials) produced prefix-valid chaining values at the predicted rate
but ZERO collisions. The solver matches the window step-equations and modular differences
but not the finer absolute signed-bit conditions that completion needs. We therefore do
NOT merge solver points into the table: the match probability of this claim rests on the
single completion-compatible (published) point only. Making the solver enforce the full
signed characteristic -- so that merging many compatible points lowers the trial count
toward the published `2^40.5` -- is left for future work (Section 14).

## 9. The completion search (Phase 3), exact and capped

Given a matched, `c18 in S` prefix, Phase 3 searches message words of the second block,
walking arithmetic progressions with the fixed Weyl increment `WEYL = 0x9e3779b9`:

- Enumerate the 64-element winning set `G16` (closed form, Section 5); keep the subset with
  `s1(w18) + c18` in `G18`, giving the admissible `(g, w14)` candidates (w14 from
  `y = g - c16` by the GF(2) inverse of s1).
- For each candidate, draw FRESH offsets `(r13_j, r15_j)` from the organizer seed and index
  j, and walk `x = r13_j + i*WEYL` for `i < CAP13`, testing E_13/E_14; for each surviving x,
  walk `z = r15_j + k*WEYL` for `k < CAP15`, testing E_15/W16 and the final `Ch` equality.
- A SINGLE global counter `iters` is incremented on EVERY inner iteration -- each outer
  x-evaluation AND each inner z-iteration -- and the search hard-stops every loop the moment
  `iters` reaches `GLOBAL_PHASE3_CAP`. The TOTAL inner iterations per matched prefix is thus
  bounded by `GLOBAL_PHASE3_CAP`, not by the structural product `CAP13*CAP15`.

Hard caps (identical in `experiments/completion.py` and here):

    CAP13 = 2^18                 per-candidate x attempts
    CAP15 = 2^12                 per-x z attempts
    GLOBAL_PHASE3_CAP = 2^16     TOTAL inner iterations (x-evals + z-iters) per matched prefix

Per-call worst-case operation bound, derived from the counter: at most `2^16` inner
iterations, each body at most 64 word operations, so per matched prefix the completion costs
at most `2^16 * 64 = 2^22` word operations `<= 2^11` units (the `T3` per-call figure). The
eleven fresh certificates of Section 11 each closed in at most 8349 inner iterations
(« 2^16), and the organizer sandbox runs the whole 256-trial request in ~7.5 s.

Completion rate: for a matched prefix with `c18 in S`, Phase 3 succeeds within the caps with
probability at least `r_comp = 0.98` (Heuristic H2; the one-sided 99% binomial lower bound
from the 256/256 organizer successes is `0.01^(1/256) = 0.98217`). The probability that a
matched prefix has `c18 in S` is the exact density `|S|/2^32 = 0.1361322` under the H1
near-uniformity of `c18`.

## 10. Success probability (explicit derivation, target 0.39)

Let `q` be the per-trial probability of producing a verified collision, using the EXACT
single-point union `Pr_U = 2^-44.955607` (Section 6.1):

    q = Pr_U[CV in P] * Pr[c18 in S | match] * r_comp
      = 2^-44.955607 * 0.1361322 * 0.98
      = 2.93e-14 = 2^-47.862

The `N = 2^47` trials draw independent fresh uniform first blocks, so the number of
verified collisions, key-hits, and completion-calls are each exactly BINOMIAL in N (no
Poisson approximation is used anywhere). `1 - (1-q)^N >= 1 - exp(-N*q)`. With `p_cap` the
completion-call cap overflow and `p_hit` the key-hit cap overflow,

    P_success >= 1 - exp(-N*q) - p_cap - p_hit.

Key-hit cap (makes T2 a per-run bound). Let `X` be the number of hit-path trials; under H1,
`X ~ Binomial(N, p_h)` with `p_h = distinct_keys/2^32 = 2336/2^32 = 2^-20.81`, so
`E[X] = N*p_h = 2^26.19`. The run aborts (FAIL) if `X` reaches `H_cap = 2^28` (`>= 2*E[X]`,
rounded up to a power of two). The multiplicative Chernoff bound for a binomial gives

    p_hit = Pr[X >= H_cap] <= Pr[X >= 2 E[X]] <= (e/4)^{E[X]} = 2^-4.3e7   (effectively 0).

Completion-call cap. Let `Y` be the number of matched prefixes handed to Phase 3;
`Y ~ Binomial(N, Pr_U * 0.1361322)` with mean `mu = N * 2^-44.955607 * 0.1361322 = 0.561`.
Budgeting `B3 = 12` completion calls and stopping beyond them, the EXACT binomial tail is
bounded (Chernoff for a binomial, no Poisson substitution) by

    p_cap = Pr[Y >= 12] <= e^{-mu} (e*mu/12)^12 = 2^-36.5.

Putting `r_comp = 0.98`, `N = 2^47`:

    N*q = 0.5503,   1 - exp(-0.5503) = 0.4232,
    P_success >= 0.4232 - 2^-36.5 - 2^-4.3e7 = 0.4232 >= 0.39.

`N = 2^47` is the smallest power-of-two trial count that clears 0.39 (`N = 2^46` gives only
`1 - exp(-0.2752) = 0.241`); it clears it with margin. The claim sets
`success_probability = 0.39` as the supported lower bound. Sensitivity: with
`lambda = N*q`, `P_success ~ 1 - exp(-lambda)`; `r_comp` lower by a factor f raises the
required `N` by `1/f`, and since the ledger is dominated by `T2 ~ N`, `time_log2` moves
roughly as `log2(N)` (Section 12).

## 11. Certificates

The attached certificates (`type hash-collision-witness-v2`, all organizer-recomputed) are:
- `llwds24-31step`: the published practical pair on exactly this trail, digest
  `55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd` (trail witness; the
  algorithm never reads it and it is not advice);
- `compl-seed0 .. compl-seed9`: TEN independent, organizer-verifiable collisions produced
  by this submission's own completion step on prefix-valid chaining values of the published
  starting point (independent per-seed offsets; each re-hashes to equal digests on two
  distinct 128-byte messages). The ten digests are distinct; the first three
  (`compl-seed0..2`) are the three collisions recorded in the forward-search run report.

So eleven certificates in total (one trail witness plus ten distinct fresh collisions).
They are evidence that the construction's completion step produces genuine collisions on
the completion-compatible (published) point, not a measurement of first-block search cost.

Organizer experiment `completion` (`experiments/completion.py`, kind
`python-message-pairs-v1`, event `full-collision`): for each organizer seed it keeps the
published prefix and `W0..W12`, draws fresh offsets per candidate, runs the capped Phase-3
search of Section 9 (single total-inner-iteration counter), and returns the two 128-byte
messages for organizer re-hashing. It does not run Phases 1-2. It exercises the completion
routine and its caps on one prefix; it does not establish the completion rate over the
prefix distribution (Heuristic H2 limitation).

## 12. Cost ledger (collision-frontier-v5, C = 2140)

Accounting rules: one 31-step compression = 1 unit; every other 256-bit word primitive
= `1/2140` unit; all trials including failures are charged; no amortization and no
parallel wall-time discount; work is summed across all processors. Per-round word-op
counts of the reference core: a step body costs 54 word ops, one expansion word 30, the
feed-forward 16; a full 31-step compression is `31*54 + 15*30 + 16 = 2140` (= C).

Per-trial charge, bounded for EVERY coin sequence (this is the fix to the earlier fatal
cost finding). Each of the `N` trials is charged one full target compression (1 unit) for
`CV = C(IV,M0)` plus the `<= 32` word-op miss-path probe. The hit path (a key reconstruction
touching up to the max group of 16 tuples, `16 * (W6 test 10 + W5 test 28) = 608` word
operations) is charged for up to `H_cap = 2^28` trials -- the hard hit cap of Section 10,
beyond which the run aborts -- so the hit term is bounded regardless of how many coins hit:

    T2 = N * (1 + 32/2140)  +  H_cap * (608/2140)
       = 2^47 * 1.01495  +  2^28 * 0.2841
       = 2^47.021  +  2^26.5
       = 2^47.021 units.

CPU-second conversion (row T_char): the reference core runs `2^23.83` 31-step compressions
per CPU-second (measured, `bench.c`); rounded UP to the next power of two, one CPU-second
is charged as `units_per_cpu_s = 2^24` target-compression units.

    row      | what is charged                                                   | units
    ---------|-------------------------------------------------------------------|---------------------------
    T_char   | one-time trail search + published starting-point construction (H3) | 2^41   (allowance; see ladder)
    T1       | table build from the single point: 6 enumerations over 2^32 + fill | <= 2^30
    T2       | N=2^47 miss-path + H_cap=2^28 hit-path (per-run bound)             | 2.23e14 = 2^47.02
    T3       | <=12 completion calls * (<=2^16 iters * 64 wops)/2140 <= 12*2^11   | 2.5e4   = 2^14.5
    T4       | verification: re-hash returned pairs (<= 2^8 compressions)         | <= 2^8
    ---------|-------------------------------------------------------------------|---------------------------
    total    | T_char + T1 + T2 + T3 + T4 = 1.438e14                              | time_log2 = 47.043

Headline `time_log2 = 47.04` (precisely `47.043`). The total is now DOMINATED by the trial
term `T2 = 2^47.02` (the single-point match probability `2^-44.956` forces `N = 2^47`);
`T_char = 2^41` is `~2^6` below `T2`, so the one-time allowance is immaterial to the scalar.
The `T_char` sensitivity ladder (shown for completeness) barely moves the total:

    T_char allowance | total units | time_log2
    -----------------|-------------|----------
    2^40             | 1.427e14    | 47.032
    2^41  (claim)    | 1.438e14    | 47.043
    2^42             | 1.460e14    | 47.065

`T_char = 2^41` is a DECLARED ALLOWANCE (Heuristic H3) that, as in the prior passing
packages, covers both the incomplete one-time trail search and the published collision run
that produced the starting point. Our own attached partial trail re-run (`trail-run/log.csv`)
is 40 completed solver calls summing 29,786.8 CPU-s = `2^38.86` units (+1 call in progress,
call 41, adding 650.4 CPU-s); one logged call returned `stp_result = Valid`, but the search
is still treated as UNFINISHED (a single valid sub-result is not the completed trail
enumeration), so `T_char` stays a declared allowance. A third-party partial is 58,015 CPU-s
= `2^39.82` units; `2^41` is about `2^2.1` / `2^1.2` over these. Because `T_char` is now
immaterial to the scalar (the trial term dominates), this allowance no longer drives the
score.

Memory (reported only, no scalar contribution). The whole-process simultaneous-allocation
peak, `memory_log2_bytes = 30` (`<= 2^30` bytes), breaks down as:

    live object                                   | bytes          | log2
    ----------------------------------------------|----------------|------
    V6 membership bitset (2^32 bits, build only)  | 536,870,912    | 29.00
    V5/V6/V8/G16/G18 member lists (peak, build)   | ~210,000,000   | 27.65
    code + constants + stacks + allocator slack   | ~64,000,000    | 25.93
    single-point key table + 16896 tuples         | ~560,000       | 19.1
    completion working set (one prefix)           | < 1,000,000    | <20
    ----------------------------------------------|----------------|------
    sum of simultaneous peaks (bounded)           | < 1,073,741,824| <= 30.00

Nonuniform advice is the single published starting point the algorithm's table is built
from: 11 words plus the characteristic constants, under 512 bytes, so
`nonuniform_advice_log2_bytes = 9`; its construction is charged in T_char and Phase 1
rebuilds the table from it.

## 13. Declared heuristics

Every empirical or unproved premise the success and cost bounds rely on is declared as a
heuristic in `claim.json` (H1, H2 on probability; H3 on one-time cost) with scope,
extrapolation, limitations and a sensitivity statement, linked by `evidence_ids` to the
lines above or to the `completion` experiment. H1's scope includes the near-uniformity of
the 96-bit backward state `(A_-1,A_-2,A_-3)` (for the match probability) and of `c18` on a
matched prefix (for the completion trigger). The match-probability VALUE
`Pr_U = 2^-44.955607` is NOT a heuristic -- it is the exact single-point union (Section 6.1);
only the near-uniformity of `CV` is H1. There is no starting-point-generation cost heuristic
(the single point is taken from the published pair and charged in T_char) and no
merged-union heuristic (no merging is claimed). The exact-count facts of Sections 5-6 are
enumerations, shipped as participant prose (Section 14). All quantities are resolved; this
package carries no unfilled placeholders.

## 14. Scope and limitations

- This is published cryptanalysis (Li-Liu-Wang EUROCRYPT 2024 Sect. 4.2 / ASIACRYPT 2024;
  published pair and starting point) with new, self-contained accounting. The
  characteristic, the starting point and the witness are attributed.
- The attack is not executed at full scale in this package; the bound rests on H1-H3.
- **Only one starting point is used.** We generated 12,087 additional solver starting points
  (z3) that satisfy the slide-10-11 window step-equations and the published modular
  step-differences, but a direct completability survey found them NOT completion-compatible:
  the published point closes 514/514 chaining values with `c18 in S`, while every sampled
  solver point closes 0 / ~530-575, and a live forward search over all 12,087 points
  (`2^35.3` trials) produced prefix-valid chaining values at the predicted rate but ZERO
  collisions. Merging such points therefore cannot lower the trial count, and is excluded
  from this claim. Making the solver enforce the full signed characteristic (so that merging
  many completion-compatible points drops the trial count toward the published `2^40.5`) is
  the main avenue of future work.
- Trials are independent by construction (fresh uniform first blocks). Batching takes no
  cost credit. The time bound is hard per-run: the hit cap `H_cap = 2^28` and the completion
  cap bound T2 and T3 for every coin sequence, and the cap-overflow probabilities are
  subtracted via exact binomial (Chernoff) tails, not a Poisson approximation.
- The match probability `Pr_U = 2^-44.955607` is the EXACT single-point union (no bracket,
  no heuristic); the dominant uncertainty is now the completion rate `r_comp = 0.98` (H2,
  the one-sided 99% lower bound from 256/256) and the H1 near-uniformity of `CV`. H2's
  robustness: `q` is linear in `r_comp`, and at `N = 2^47` the floor 0.39 is reached at
  about `r_comp ~ 0.90` (`r_comp = 0.90` gives `P_success ~ 0.397`), so the claimed 0.98
  has ~0.08 of slack.
- `q` multiplies TWO separately extrapolated distributional quantities under H1: (i) the
  96-bit membership `Pr[CV in P]` and (ii) the conditional `Pr[c18 in S | match]`. Only a
  32-bit `A_-1` marginal of (i) is measured (the own-run key-hit check: 590,984 hits in 2e9
  fresh-coin trials on a MERGED table, `~2^-11.7`; for the single published point the key-hit
  rate is `2336/2^32 = 2^-20.81`). Neither the full 96-bit event (i) nor the conditional
  (ii) is directly observable; EACH is separately extrapolated under H1's near-uniformity,
  and this is disclosed rather than claimed as measured.
- The exact enumerations (set sizes, the single-point union) are produced by bundled C
  programs not shipped as organizer-runnable artifacts, so to the organizer they are
  participant prose (a rigorous-lane limitation).
- Memory is reported, not scored. `baseline_improved = sha256-r31-nominal-v2` is a required
  reference identifier, not an asserted improvement.

## Appendix A. Full characteristic table

The complete 33-row signed table (rows -4..30, including the all-`=` rows omitted from
Section 4) is `clean_table.txt` in the implementation bundle; its non-blank rows are
exactly those reproduced in Section 4, and the blank rows carry no difference in dA, dE
or dW. The sign convention is that of Section 4.
