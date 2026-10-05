# 31-step SHA-256: two-block differential collision search with shared first-block prefixes

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (C = 2140), policy `paired-lanes-v1`, exploratory lane.

## 1. Claim and provenance

A randomized algorithm outputs two distinct 128-byte messages with equal complete
31-step SHA-256 digests with probability at least 0.39 over its own coins, and every
run costs at most 2^47.5610 target-compression units (claim `time_log2` = 47.57).
Memory is below 2^32 bytes. Preprocessing (advice construction + table) is below
2^45.01 units and is included in the total.

Cryptanalysis is published work, not ours: the two-block attack of Li, Liu and Wang
(EUROCRYPT 2024, "New Records in Collision Attacks on SHA-2", ePrint 2024/349) in its
single-starting-point form, with the matching of Li, Liu, Wang, Dong and Sun
(ASIACRYPT 2024, "The First Practical Collision for 31-Step SHA-256"); the local
collision in W5..W9, W16, W18 goes back to Mendel, Nad and Schlaeffer (EUROCRYPT
2013). The characteristic, the starting point and the published colliding pair are
theirs. The package structure (fresh first blocks, exact modular acceptance tests,
hard caps, advice charged as preprocessing) follows public Yukon submission
`654cb3d` by jagnani73 (score 48.35), credited as co-author.

What this package changes relative to `654cb3d`, all re-derived and re-measured
independently (Section 13):

1. First blocks are generated in groups of L = 2^16 that share fresh uniform words
   W0..W14 and use W15 = r15 + j. Steps 0..14 and schedule words W16, W18, W20 are
   computed once per group; each trial pays only for steps 15..30, twelve schedule
   words and the feed-forward, priced per word operation at 1/2140 (Section 11).
   Every trial block is still marginally exactly uniform (Lemma 4); only pairs of
   trials inside one group need a (very weak) pairwise heuristic H4.
2. The per-tuple table work is charged per key hit under a hard global cap of 2^38
   key hits, instead of worst-case on every trial.
3. The advice-construction allowance is doubled (2^45 instead of 2^44 units).
4. Lemma 1 is corrected: the per-tuple acceptance sets are NOT pairwise disjoint
   (explicit witness in Section 6); we use a Bonferroni lower bound instead.

`baseline_improved` is the required nominal reference identifier
`sha256-r31-nominal-v2`; comparison with the Yukon incumbent is left to Yukon.

## 2. Target and notation

Words are 32-bit, additions modulo 2^32, `>>>` rotation right, `>>` shift right.

    S0(x) = (x>>>2) ^ (x>>>13) ^ (x>>>22)      S1(x) = (x>>>6) ^ (x>>>11) ^ (x>>>25)
    s0(x) = (x>>>7) ^ (x>>>18) ^ (x>>3)        s1(x) = (x>>>17) ^ (x>>>19) ^ (x>>10)
    Ch(e,f,g) = (e & f) ^ (~e & g)             Maj(a,b,c) = (a & b) ^ (a & c) ^ (b & c)

A block is W0..W15 (big-endian), expanded by W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15])
+ W[t-16] for t = 16..30; K[0..30] are the first 31 SHA-256 constants at their
original indices. The reduced compression C(H, block) runs steps t = 0..30,

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t],  T2 = S0(a) + Maj(a,b,c),
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

and adds the eight working words to H (feed-forward). The hash pads with 0x80,
zeros and the 64-bit big-endian bit length, starts from the standard IV, applies C
to every padded block and outputs the final chaining value big-endian: exactly
`verifier/hash_functions.py:digest(m, "sha256", 31)`. Standard IV once, standard
padding, steps 0..30 on every block, full feed-forward, all 256 bits.

Writing A_t, E_t for the new a and e after step t,

    E_t = A_{t-4} + E_{t-4} + S1(E_{t-1}) + Ch(E_{t-1},E_{t-2},E_{t-3}) + K[t] + W[t]   (1)
    A_t = E_t - A_{t-4} + S0(A_{t-1}) + Maj(A_{t-1},A_{t-2},A_{t-3})                     (2)

and the chaining value entering a block is (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4).

Messages: m = M0 || M1 and m' = M0 || M1' (128 bytes each); both hashes process M0,
then M1 or M1', then the same padding block (length 1024). If C(CV, M1) = C(CV, M1')
for CV = C(IV, M0) the digests are equal. M1, M1' differ in words 5..9, so m != m'.
Primed quantities belong to M1'; dX = X' - X mod 2^32.

## 3. Differential structure and advice

    d5 = fffff006  d6 = 002087f1  d7 = 4fefb5fa  d8 = 28011100  d9 = 00008004
    d16 = 00008004 (= d9)   d18 = ffff7ffc   no other expanded-word difference.
    c5 = d0018020  c6 = 00000ffa  c7 = ffdf780f  c8 = b00fca02  x18 = 2ffe7fe0

The expansion carries exactly these differences when

    W16: d16 = d9 (W1, W0, W14 have no difference)
    W18: s1(W16 + d16) - s1(W16) = d18                       (W16 in G16)
    W20: [s1(W18+d18) - s1(W18)] + [s0(W5+d5) - s0(W5)] = x18 + c5 = 0
    W21: c6 + d5 = 0;  W22: c7 + d6 = 0;  W23: d16 + c8 + d7 = 0
    W24: s0(W9 + d9) - s0(W9) + d8 = 0 (W9 is an advice word);  W25: d18 + d9 = 0

with V_i = {w : s0(w + d_i) - s0(w) = c_i} (i = 5..8), G16 = {w : s1(w+d16) - s1(w) =
d18}, G18 = {w : s1(w+d18) - s1(w) = x18}. W17, W19, W26..W30 involve no difference.
Exhaustive counts over all 2^32 words (our C code, Section 13):

    |V5| = 16384, |V6| = 8388608, |V7| = 512, |V8| = 49408, |G16| = 64, |G18| = 42467328.

All six constant identities above evaluate to 0 (checked).

Advice (starting point), read off the published pair by running its second block from
CV0 = C(IV, M0_pub) = c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b 70b1ac59:

     t   A_t       A'_t      E_t       E'_t
     1   f36e6fcf  =
     2   b741c202  =
     3   90c67413  =
     4   fc7566c3  =
     5   fa9053fb  fa904401  1d1fa7dd  1d1f97e3
     6   11af5d4e  112f5d4f  afe878e7  afe0f8e6
     7   87f5120c  96d50209  4c97cbe5  9c1fcf6c
     8   9180b607  9180b603  946f8048  d96f084c
     9   4f5af3a8  =         61c171d3  61c171db
    10   4b9e4fb8  4b9ecfbc  f02293fa  dfa31402
    11   83e817e6  =         aa270418  bae70410
    12   2be31c3f  =         b1f7f9e8  b1f779e0
    W9 = eb830a58  W10 = 66add94a  W11 = 9669232d  W12 = 45271fa5  (W'9 = W9 + d9)

37 words plus the 10 constants: 188 bytes (`nonuniform_advice_log2_bytes` = 8). Checked
properties: (P1) steps 9..12 of (1),(2) hold for both messages; (P2) (2) holds at steps
5..8 for both messages with A_1..A_4 shared; (P3) step 8 of (1) gives the same E_4 for
both messages for every W8 (with W'8 = W8 + d8), and E'_5 - E_5 = d5; (P4) step 13 gives
no difference for every W13 (the step-13 difference of the W13-free terms is 0);
(P5) A'_10 - A_10 = 00008004 = -d18.

## 4. Phase 1: table and bitmaps

For W8, W7 the starting point determines, by (1) at steps 8, 7 and (2) at steps 4, 3,

    E_4 = E_8 - A_4 - S1(E_7) - Ch(E_7,E_6,E_5) - K[8] - W8
    E_3 = E_7 - A_3 - S1(E_6) - Ch(E_6,E_5,E_4) - K[7] - W7
    A_0 = E_4 - A_4 + S0(A_3) + Maj(A_3,A_2,A_1)
    A_-1 = E_3 - A_3 + S0(A_2) + Maj(A_2,A_1,A_0).

The second message reaches E'_7, E'_6 from the same E_4, E_3 iff

    (F7) Ch(E'_6,E'_5,E_4) - Ch(E_6,E_5,E_4) = dE_7 - [S1(E'_6) - S1(E_6)] - d7 = fff8701d
    (F6) Ch(E'_5,E_4,E_3)  - Ch(E_5,E_4,E_3) = dE_6 - [S1(E'_5) - S1(E_5)] - d6 = ffffffd0

A tuple is (W7 in V7, W8 in V8) satisfying (F7), (F6); its key is A_-1. Exhaustive
result: 2048 W8 in V8 satisfy (F7); 16896 = 33 * 2^9 tuples; 2336 distinct keys;
key multiplicities 1:16, 2:216, 3:8, 4:300, 7:8, 8:1668, 10:8, 12:12, 16:100.

Phase 1 makes one pass over all 2^32 words to build bitmaps B5, B6, B18 (V5, V6, G18)
and the key bitmap BK (2^32 bits each), lists V7 and the W8 passing (F7), tests the
2^20 (W7, W8) pairs, and stores each tuple record (W7, W8, E_3, E_4, A_0 and seven
per-tuple constants of Section 5) in an array sorted by key.

## 5. Phase 2: one trial

Given CV = (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4):

    1. If BK[A_-1] = 0, the trial ends.                         (key test)
    2. Otherwise (key hit; counted against the cap Qk) locate the key's tuples by
       binary search and, for each tuple (W7, W8, E_3, E_4, A_0):
         E_2 = A_2 + A_-2 - S0(A_1) - Maj(A_1, A_0, A_-1)                     [(2), step 2]
         W6  = E_6 - A_2 - E_2 - S1(E_5) - Ch(E_5, E_4, E_3) - K[6]           [(1), step 6]
         if W6 not in V6: next tuple
         E_1 = A_1 + A_-3 - S0(A_0) - Maj(A_0, A_-1, A_-2)                    [(2), step 1]
         W5  = E_5 - A_1 - E_1 - S1(E_4) - Ch(E_4, E_3, E_2) - K[5]           [(1), step 5]
         if W5 not in V5: next tuple
         E_0 = A_0 + A_-4 - S0(A_-1) - Maj(A_-1, A_-2, A_-3)                  [(2), step 0]
         W0..W4 from (1) at steps 0..4 solved for W_t (using E_-4..E_4, A_-4..A_0)
         -> prefix-valid with (W0..W8, advice W9..W12): go to Phase 3.

W6 = kappa_t - A_-2 with kappa_t a per-tuple constant; Maj(A_0, A_-1, x) =
(A_0 & A_-1) ^ ((A_0 ^ A_-1) & x) and Ch(E_4, E_3, x) = (E_4 & E_3) ^ (~E_4 & x) are
linear in x with per-tuple constants, so W5 = lambda_t(A_-2) - A_-3 costs a few
operations. W0..W4 drive the state from CV to (A_0..A_4, E_0..E_4); W5, W6 reach E_5,
E_6; for the second message steps 0..4 are identical, step 5 gives dE_5 = d5 (P3),
(F6), (F7), (P3) handle steps 6..8 and (P2), (P1) the A-words and steps 9..12. So
after step 12 both messages are in the advice states. Running this procedure on CV0
returns the published W0..W8 with exactly one accepting tuple (checked).

## 6. Prefix-valid set P (corrected Lemma 1)

P = chaining values accepted by at least one tuple; P depends on (A_-1, A_-2, A_-3).

Lemma 1. Under uniform CV (distribution U),
Pr[CV in P] >= 33 * 2^-50 * (1 - 5.6 * 10^-7).

Proof. For a tuple t with key k: Pr[A_-1 = k] = 2^-32; given A_-1, A_-2 -> W6 is a
bijection, so Pr[W6 in V6] = 2^-9 exactly; given A_-1, A_-2, A_-3 -> W5 is a bijection,
so Pr[W5 in V5] = 2^-18. Hence |G_t| = 2^37 pairs (A_-2, A_-3) under key k, and the
sum over tuples is 16896 * 2^37 = 2322167278862336. Different keys give disjoint sets.
For same-key pairs (62064 pairs) we computed the exact pairwise intersections: for each
pair and each A_-2 accepted by both (W6 condition), the number of shared A_-3 is
|V5 ∩ (V5 - (lambda_t - lambda_u))|. The pairwise-overlap total is 1,279,000,576
(3,493,888 values of A_-2 contribute). By Bonferroni, |union| >= 2322167278862336 -
1279000576 = 2322165999861760, a relative deficit below 5.6e-7. QED.

The sets are therefore not pairwise disjoint (contrary to the statement in `654cb3d`).
Witness: A_-1, A_-2, A_-3 = 4941c1b9, 1edb092c, 86b0440b is accepted by the tuples
(W7, W8) = (215af27a, 9a048626) and (215af27a, 9a448626); for each, both messages reach
all advice states 5..12 (verified by direct compression). The effect on the score is nil.

Lemma 2. Under U, conditioned on CV in P and on (A_-1..A_-4), the words W0..W3 are
uniform on 2^128 values (for fixed A-words and accepting tuple, E_-1 -> W3, E_-2 -> W2,
E_-3 -> W1, E_-4 -> W0 are successive bijections and the E-words are uniform and
independent of the A-words). Hence c16 = W9 + s0(W1) + W0 and c18 = W11 + s0(W3) + W2
are independent and uniform.

## 7. Phase 3: completion with W13, W14, W15

With W16 = s1(W14) + c16 and W18 = s1(W16) + c18:

    for each g in G16 with s1(g) + c18 in G18:                       (g is W16)
        W14 = s1^-1(g - c16)                 (s1 is GF(2)-linear and invertible)
        r13 <- fresh uniform word; for i < 2^18: x = r13 + i*9e3779b9   (E_13)
            y  = A_10  + E_10  + S1(x) + Ch(x, E_12,  E_11)  + K[14] + W14   (E_14)
            y' = A'_10 + E'_10 + S1(x) + Ch(x, E'_12, E'_11) + K[14] + W14
            (C14) y' - y = 00008004
            (C15) E_11 + S1(y) + Ch(y, x, E_12) = E'_11 + S1(y') + Ch(y', x, E'_12)
            r15 <- fresh uniform word; for k < 2^12: z = r15 + k*9e3779b9    (E_15)
                (C16) E_12 + Ch(z, y, x) = E'_12 + Ch(z, y', x) + d16
                u = A_12 + E_12 + Ch(z, y, x) + S1(z) + K[16] + g            (E_16)
                (C17) Ch(u, z, y) = Ch(u, z, y')
                success: W13 = x - [A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) + K[13]],
                         W15 = z - [A_11 + E_11 + S1(y) + Ch(y, x, E_12) + K[15]]
    A call also stops without result after 2^18 values of z in total.

By (P4) E_13 = x and A_13 agree; (C14) and (P5) give A'_14 = A_14; (C15) is step 15 of
(1) without W15, so E'_15 = E_15, A'_15 = A_15; (C16) is step 16 with W'16 = W16 + d16;
(C17) is the only differing term of step 17; at step 18 dE_14 + d18 = 0. After step 18
the eight state words agree; steps 19..30 then see equal states and equal words.

S = {c18 : some g in G16 has s1(g) + c18 in G18}: |S| = 584683520 (density 0.1361322),
exhaustive. By Lemma 2, Pr_U[c18 in S | CV in P] = |S|/2^32 exactly. The completion rate
given c18 in S is heuristic H2.

## 8. Correctness of outputs

Lemma 3. If Phase 3 succeeds after a prefix-valid trial then C(CV, M1) = C(CV, M1').
(Message words satisfy every line of Section 3; states agree after step 12 by Section 5
and after step 18 by Section 7; feed-forward adds the same CV.) Independently, the
algorithm re-hashes both 128-byte messages (six compressions) and outputs only on
equal digests and m != m', so every output is a genuine collision.

## 9. The algorithm with all caps

    Parameters: L = 2^16, G = 238 * 2^24 groups, N = G*L = 238 * 2^40 trials,
                Qk = 2^38 key hits, Q = 2^20 Phase-3 calls.
    0. Load the advice; run Phase 1.
    1. For g = 1..G:
         draw two fresh uniform 256-bit words -> block words W0..W15 (512 bits);
         r15 <- W15; run steps 0..14 from IV; compute W16, W18, W20.
         For j = 0..L-1:
           W15 = r15 + j (mod 2^32); compute W17, W19, W21..W30, steps 15..30 from
           the stored step-14 state, and the feed-forward -> CV = C(IV, M0_j).
           Key test. On a key hit: if Qk hits already processed, FAIL; else Phase 2.
           If prefix-valid: if Q calls already made, FAIL; else Phase 3.
           If Phase 3 succeeds: build m, m', re-hash, output if equal and distinct; stop.
    2. FAIL.

No restarts. Coins: two words per group, one per r13 / r15 in Phase 3.

## 10. Success probability

Probability space: the algorithm's coins; target and advice fixed. For trial (g, j)
let win(g,j) be the event that its CV is prefix-valid and Phase 3 (with the coins that
call would use) succeeds. Let q_U be the per-trial win probability for CV ~ U and q_D
for the real marginal distribution of one trial.

Lemma 4 (marginal uniformity). For every fixed j, the block M0_{g,j} = (W0..W14,
r15 + j) is uniform on 512 bits, because (W0..W14, r15) is uniform and adding j to
the last word is a bijection. So Pr[win(g,j)] = q_D for every trial, exactly as for
fresh blocks. Different groups use disjoint coins and are independent.

By Lemma 1, |S| and H2, q_U >= 33 * 2^-50 * (1 - 5.6e-7) * 0.1361322 * 0.99 >
3.9501 * 10^-15 (2^-47.847). H1(a): q_D >= q_U/2.

Within a group (H4): for j != j', Pr[win(g,j) and win(g,j')] <= 2^20 * q_U^2.
Bonferroni per group: Pr[some win in g] >= L q_D - C(L,2) 2^20 q_U^2
>= (L q_U / 2)(1 - eps), eps = L * 2^20 * q_U < 2^-11.84.
Independence across groups: Pr[no win] <= exp(-N (q_U/2)(1 - eps)) <= exp(-0.51670)
< 0.59649.

Caps (H1(b), H1(c), linearity of expectation over trials, each with marginal D):
- prefix-valid trials: mean <= N * 2^10 * 33 * 2^-50 = 7854; Markov at Q = 2^20: <= 0.00750.
- key hits: mean <= 2 * N * 2336 * 2^-32 < 2^28.08; Markov at Qk = 2^38: <= 0.00104.

The algorithm fails only if no trial wins or a cap is reached, so
Pr[success] >= 1 - 0.59649 - 0.00750 - 0.00104 = 0.39497 > 0.39 (claimed 0.39).
With q_D = q_U the bound is about 0.636.

## 11. Cost (C = 2140)

One 31-step compression (expansion, 31 steps, feed-forward) = 1 unit; any other
256-bit word operation (load, store, add, sub, AND, OR, XOR, NOT, shift, compare,
branch, random word) = 1/2140. Counts use the organizer convention that yields
C = 2140 = 15*30 + 31*54 + 16: a narrow rotation is 5 operations, a modular addition is
add + mask, a reference step is 54 operations including the K+W addition, one schedule
word is 30, the feed-forward is 16.

Per trial (worst-case path, key miss or hit; key-hit work is charged separately):

| work | ops |
| --- | ---: |
| W15 = r15 + j (add, mask) | 2 |
| schedule W17, W19, W21..W30 (12 x 30) | 360 |
| steps 15..30 (16 x 54) | 864 |
| feed-forward (8 add + 8 mask) | 16 |
| key-bitmap test (shift, load, and, shift, and, branch) | 6 |
| loop counter, compare, branch | 3 |
| counted | 1251 |
| allowance for reloads of W0..W14, W16, W18, W20, step-14 state and K | 149 |
| **charged** | **1400** |

W16, W18, W20 and steps 0..14 do not depend on W15 (W16 = s1(W14)+W9+s0(W1)+W0,
W18 = s1(W16)+W11+s0(W3)+W2, W20 = s1(W18)+W13+s0(W5)+W4), so they are per-group work.
The 149-operation allowance covers one load for each of the 15 + 3 + 8 + 16 = 42 stored
words used per trial plus the 12 schedule-word re-reads, with margin; no register file
assumption beyond that is used.

Per group (G times): 2 random words, unpacking (<= 32), steps 0..14 (15 x 54 = 810),
W16, W18, W20 (90), stores of the step-14 state and the words (<= 40), loop control:
<= 2048 operations.

Key hit (at most Qk = 2^38 times): binary search over 2336 keys (<= 12 x 8 = 96), then
<= 16 tuples x (W6 test 10 + W5 test 28 + record loads 12) = 800; charged 1024.

Phase 1 (once): per word w, membership tests for V5..V8 (two s0, 13 ops each, plus
add, sub, compare, branch: <= 32 each), G18 (<= 36), bitmap updates and zeroing (<= 40),
the (F7) test for V8 members (<= 24): <= 256 per w, 2^40 total; 2^20 (W7, W8) pairs at
<= 64; record building and sorting 16896 records < 2^22. Total < 2^41 ops < 2^30 units.

Phase 3 (at most Q = 2^20 calls): computing W0..W4, c16, c18 (<= 256); 64 G18 tests
(<= 12 each); per g: W14 via 32 conditional XORs (<= 96) and <= 2^18 values of x at
<= 110 ops (three S1 at 17, four Ch at 5, nine modular add/subs at 2, two compares,
loop 5: 51 + 20 + 18 + 6 + 5 = 100); <= 2^18 values of z per call at <= 64 ops. Per call
<= 64 * (2^18 * 110 + 96) + 2^18 * 64 + 2^13 < 2^31 ops < 2^20 units; total <= 2^40.

Final check: 6 compressions + < 2140 ops <= 8 units.

Advice construction T0 = 2^45 units (H3).

    T2 (trials)    = 238 * 2^40 * 1400/2140      = 155.701 * 2^40
    T_group        = 238 * 2^24 * 2048/2140      =   0.004 * 2^40
    T_keyhit       = 2^38 * 1024/2140            =   0.120 * 2^40
    T3 (Phase 3)  <= 2^40                        =   1.000 * 2^40
    T1 + T4        < 2^30 + 8                    =   0.001 * 2^40
    T0 (H3)        = 2^45                        =  32.000 * 2^40
    total          < 188.826 * 2^40 < 2^47.5610   -> time_log2 = 47.57

`preprocessing_log2` = 45.01 bounds T0 + T1 and is included above. All bounds are caps
on every run; only the success probability uses heuristics.

Memory: B5, B6, B18, BK: 4 x 2^32 bits = 2^31 bytes; tuple records 16896 x 12 words x
32 bytes < 2^23 bytes; V7/W8 lists, code, constants, per-group state < 2^20 bytes.
Total < 2^32 bytes: `memory_log2_bytes` = 32.

## 12. Declared heuristics

**H1 (near-uniform chaining values; score-critical).** For one trial (marginally a
uniform 512-bit block M0, Lemma 4) and CV = C(IV, M0): (a) Pr[win] >= q_U/2;
(b) Pr[CV in P] <= 2^10 * 33 * 2^-50; (c) Pr[A_-1 is a key] <= 2 * 2336 * 2^-32.
Evidence: our measurement on real 31-step chaining values (Section 13, both fresh
blocks and the grouped generation actually used): key hits (32-bit condition) and
W6-test passes (41-bit condition) match uniform predictions. (c) is measured at its
full size. Not tested: the last 18 bits (W5 test on A_-3) and c18; events near
2^-45 cannot be sampled. Sensitivity: with ratio rho instead of 1/2 in (a) the bound is
1 - exp(-1.0334 rho) - 0.0085 (0.383 at rho = 0.48; 0.636 at rho = 1).

**H2 (completion rate; score-critical).** For uniform CV in P with c18 in S, Phase 3
succeeds with probability >= 0.99. Evidence: our simulation of 4 x 2^22 uniform
(c16, c18) on the advice states: 2,282,381 had c18 in S (0.136041), all 2,282,381
completed within the caps (mean 4115 x-values, max 68411; mean 15 z-values, max 4123),
each verified by running steps 13..18 for both messages and checking the W16/W18/W20
differences. Organizer experiment `completion` (Section 13) runs our Phase 3 on the
published prefix. An independent simulation in `654cb3d` (2,282,789 / 2,282,789)
agrees. Sensitivity: rate 0.9 gives success 0.366; 0.39 needs about 0.975.

**H3 (advice construction cost; score-critical).** The computations that produced the
advice (characteristic search of Li-Liu-Wang 2024 Sec. 4.2 and the collision runs of
Li-Liu-Wang-Dong-Sun 2024 that produced the published pair) cost at most 2^45 units.
Conversion: one thread-second is charged 2^23 units (2^34.06 word operations/s; a
compiled 31-step compression runs at ~2^22.5 per second per thread, so this charges
every CPU second as more than pure compression work). The reported 1.2 h on 64 threads
is < 2^41.08 units. The publisher's page also states that a first run succeeded "in
seconds" and that more experiments followed before the 1.2 h pair; the volume of those
runs is unstated. The characteristic-search time is not published; `654cb3d` reports a
partial re-run of the authors' public `find_dc_model_31_256.py` (STP + CryptoMiniSat):
24 calls, 58,015 CPU-seconds (< 2^38.83 units), unfinished. Our allowance leaves
2^45 - 2^41.08 > 2^44.9 units (about 1,000 thread-hours) for the characteristic search
and all extra collision runs, about 64x the reported partial re-run. We did not
re-run STP ourselves. Sensitivity of the total: T0 = 2^46 -> 2^47.79, 2^47 -> 2^48.16,
2^48 -> 2^48.69.

**H4 (within-group pairwise bound; supporting).** For two trials of one group
(same W0..W14, W15 differing by j - j' != 0), Pr[both win] <= 2^20 * q_U^2. The two
chaining values differ through 16 full steps after the first difference; the bound allows
a 2^20-fold correlation excess. Role: only eps < 2^-11.84 in Section 10; even a bound of
2^24 q_U^2 changes the success bound by < 0.002. Evidence: the grouped H1 measurement
(Section 13) shows marginal key-hit and W6-pass rates of grouped trials matching uniform
predictions; within-group
co-occurrence of 59-bit events cannot be sampled. Marginal per-trial probabilities do
not depend on H4 (Lemma 4).

## 13. Evidence

Organizer-verified certificates (`hash-collision-witness-v2`):
- `published-pair`: the Li-Liu-Wang-Dong-Sun pair, digest 55fdfb37efcbd086...
  M0  = 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
        dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
  M1  = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
        9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
  M1' = M1 + (d5..d9 in words 5..9)
- `own-completion-1`, `own-completion-2`: M0 and W0..W12 of the published pair with new
  (W13, W14, W15) produced by our Phase 3 (experiment trials 7 and 200 of a local run).

Organizer experiment `completion` (`experiments/completion.py`, `python-message-pairs-v1`,
event `full-collision`): for each organizer seed, derive r13, r15 from the seed
(SHAKE-256), run our Phase 3 on the published prefix, return M0||M1, M0||M1'.
Local run: 256/256 seeds returned distinct full collisions (checked with
`verifier.hash_functions.digest`), about 2.4 s total. It exercises Phase 3 and its caps
on one prefix; it does not run Phases 1-2 and is not a cost measurement.

Our own computations (C, from the definitions here; not organizer-executed):
- all counts of Sections 3, 4, 6, 7 by exhaustive loops over 2^32 words, including the
  pairwise-overlap computation of Lemma 1 and the explicit overlap witness;
- Phase 2 on CV0 returns the published W0..W8 (one accepting tuple);
- the H2 simulation above;
- H1 measurement on real chaining values, generated exactly as in Section 9 (groups of
  2^16 sharing pseudo-random W0..W14, W15 = r15 + j; 2^20 groups, N = 2^36 trials, full
  31-step compression and feed-forward, exact tests of Section 5):
  key hits 37,373 vs 37,376.0 expected under U (ratio 0.9999);
  key + W6 passes 494 vs 528.0 expected (ratio 0.936, -1.5 sigma Poisson);
  full prefix-valid 0 vs 0.002 expected. Control with fresh uniform blocks (N = 2^34):
  key hits 9,397 vs 9,344.0 (1.006); key + W6 passes 129 vs 132.0 (0.977); full 0.
  The 18-bit W5 condition and c18 are not reached at this scale.

## 14. Limitations

- Published cryptanalysis with new accounting and a constant-factor grouping saving.
  No first block was found by us; the bound rests on H1-H4.
- H3 is the weakest premise (historical, partly third-party measured).
- Within-group dependence enters only through H4 (Section 10); marginal trial
  probabilities are exact consequences of Lemma 4.
- The register/reload allowance (149 ops per trial) is a modelling bound; even charging
  a whole compression per trial (no partial evaluation) gives about 2^48.09 with T0 = 2^45.
- A passing exploratory review is an AI screening outcome, not proof or acceptance.
