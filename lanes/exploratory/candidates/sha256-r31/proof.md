# SHA-256 reduced to 31 steps: a two-block collision search with 448 starting points, executed

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(C = 2140), policy `paired-lanes-v1`, exploratory lane.

## 1. What is claimed, and what is not

Claim: a randomized algorithm that outputs two distinct 128-byte messages with the same 31-step
SHA-256 digest with probability at least 0.39 over its own coins, using at most 2^44.14
target-compression units in every run. Memory is below 2^38 bytes.

The attack is the two-block collision attack of Li, Liu and Wang (EUROCRYPT 2024, "New Records in
Collision Attacks on SHA-2", Section 4.2) with several starting points and the memory-efficient
matching of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024, "The First Practical Collision for 31-Step
SHA-256"). The local collision in message words W5..W9, W16, W18 goes back to Mendel, Nad and
Schlaeffer (EUROCRYPT 2013). The differential characteristic is theirs. So are three state words
(E_5, E_6, E_7) that every starting point here shares with their published colliding pair. We
claim no new cryptanalysis and no improvement on the published 2^40.5.

What this package adds is a version of that attack that fits this cost model, and a run of it:

- The 448 starting points are our own. They were found with an SMT solver before the algorithm
  runs, they are stored as advice (Appendix A), and the solver time is measured and charged. No
  solver runs inside the algorithm.
- First blocks are drawn from fresh uniform coins, so trials are independent by construction.
- Every test is an exact modular equation on the two messages, so nothing depends on reading a
  bit-condition table correctly. The output is also checked by full re-hashing.
- The trial count and all loops have hard caps. The time bound holds for every run, not on average.
- The table keeps one tuple per key, so the acceptance probability under a uniform chaining value
  is an exact count: 4606337 * 2^-59.
- We ran the algorithm as specified here for 2^44 trials, sixteen times its trial count
  N, without stopping at the first collision. It returned 15 collisions, and they are
  the certificates of this package.

The remaining premises are three declared heuristics (Section 12): H1 compares the real
chaining-value distribution with the uniform one on two fixed sets, H2 is the success rate of the
final completion search, and H3 is the charge for producing the advice. H3 dominates the score:
2^44 of the 2^44.14 units are an allowance for work done by the cited authors, which we can
bound only by a measured re-run and a margin.

`baseline_improved` names the organizer's nominal reference `sha256-r31-nominal-v2` because the
schema requires it. The claimed scalar is below that nominal value; whether it improves the Yukon
incumbent is for Yukon to decide.

## 2. Target and notation

All words are 32 bits, additions are modulo 2^32, `>>>` is rotation right and `>>` is shift right.

    S0(x) = (x>>>2) ^ (x>>>13) ^ (x>>>22)      S1(x) = (x>>>6) ^ (x>>>11) ^ (x>>>25)
    s0(x) = (x>>>7) ^ (x>>>18) ^ (x>>3)        s1(x) = (x>>>17) ^ (x>>>19) ^ (x>>10)
    Ch(e,f,g) = (e & f) ^ (~e & g)             Maj(a,b,c) = (a & b) ^ (a & c) ^ (b & c)

A block is 16 big-endian words W0..W15, expanded by W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16]
for t = 16..30. The constants K[0..30] are the first 31 SHA-256 constants in their original order:

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

The reduced compression C(H, block) copies the chaining value H into (a,b,c,d,e,f,g,h), runs
steps t = 0..30

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t],   T2 = S0(a) + Maj(a,b,c),
    (a,b,c,d,e,f,g,h) <- (T1+T2, a, b, c, d+T1, e, f, g),

and adds the eight working words to H. The hash pads with 0x80, zero bytes and the 64-bit
big-endian bit length, starts from the standard IV

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19

and outputs the final chaining value in big-endian order. This is the organizer's profile: standard
IV used once, standard padding, step indices 0..30 on every block, full feed-forward, all 256 bits.

State words. Write A_t and E_t for the new values of a and e after step t. Then

    E_t = A_{t-4} + E_{t-4} + S1(E_{t-1}) + Ch(E_{t-1},E_{t-2},E_{t-3}) + K[t] + W[t]        (1)
    A_t = E_t - A_{t-4} + S0(A_{t-1}) + Maj(A_{t-1},A_{t-2},A_{t-3})                          (2)

and the chaining value entering a block is (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4), its
eight words in order.

Messages. The algorithm outputs m = M0 || M1 and m' = M0 || M1', each 128 bytes. Both hashes
process three blocks: M0, then M1 or M1', then the same padding block (0x80, zeros, length 1024).
If C(CV, M1) = C(CV, M1') for CV = C(IV, M0), the two digests are equal. M1 and M1' differ in
words 5..9, so the messages are distinct.

Quantities of the second message M1' carry a prime. For a word X of the second block,
dX = X' - X (mod 2^32).

## 3. The differential structure and the advice

The second blocks differ by fixed modular differences in five message words:

    d5 = fffff006   d6 = 002087f1   d7 = 4fefb5fa   d8 = 28011100   d9 = 00008004

and W'_t = W_t for every other t < 16. The expansion is required to give d16 = 00008004,
d18 = ffff7ffc and no other difference. With the six constants

    c5 = d0018020   c6 = 00000ffa   c7 = ffdf780f   c8 = b00fca02   c9 = d7feef00   x18 = 2ffe7fe0

this holds when the following exact conditions hold (each line is one expanded word; a line is
satisfied when the listed differences cancel):

    W16 = s1(W14)+W9+s0(W1)+W0     d16 = d9
    W18 = s1(W16)+W11+s0(W3)+W2    d18 = s1(W16+d16) - s1(W16)        needs W16 in G16
    W20 = s1(W18)+W13+s0(W5)+W4    [s1(W18+d18)-s1(W18)] + [s0(W5+d5)-s0(W5)] = x18 + c5 = 0
    W21 = s1(W19)+W14+s0(W6)+W5    [s0(W6+d6)-s0(W6)] + d5 = c6 + d5 = 0
    W22 = s1(W20)+W15+s0(W7)+W6    [s0(W7+d7)-s0(W7)] + d6 = c7 + d6 = 0
    W23 = s1(W21)+W16+s0(W8)+W7    d16 + [s0(W8+d8)-s0(W8)] + d7 = d16 + c8 + d7 = 0
    W24 = s1(W22)+W17+s0(W9)+W8    [s0(W9+d9)-s0(W9)] + d8 = c9 + d8 = 0
    W25 = s1(W23)+W18+s0(W10)+W9   d18 + d9 = 0

W17, W19 and W26..W30 only involve words without difference. So define the word sets

    V_i = { w : s0(w + d_i) - s0(w) = c_i }  for i = 5,6,7,8,9,
    G16 = { w : s1(w + d16) - s1(w) = d18 },   G18 = { w : s1(w + d18) - s1(w) = x18 }.

Sizes, by exhaustive enumeration of all 2^32 words (our computation):

    |V5| = 2^14,  |V6| = 2^23,  |V7| = 512,  |V8| = 49408,  |G16| = 64,  |G18| = 42467328.

G16 is the set of 64 words (h << 28) | lo with h in 0..15 and lo in
{031bbffc, 064bbffe, 09b3bffd, 0ce3bfff} (written with h = 0).

State differences. Between steps 5 and 12 the two second blocks have fixed XOR differences, taken
from the published characteristic:

     t   A'_t xor A_t   E'_t xor E_t
     5   000017fa       0000303e
     6   00800001       00088001
     7   11201005       d0880489
     8   00000004       4d008804
     9   00000000       00000008
    10   00008004       2f8187f8
    11   00000000       10c00008
    12   00000000       00008008

and A_1..A_4 have no difference. These sixteen words and the eleven constants above are the first
part of the advice.

Starting points. A starting point is a list of twenty words A_1..A_12, E_5..E_12 for the first
message. The second message's words are obtained by the XOR differences above, and the four
message words W9..W12 follow from equation (1) at steps 9..12. A list is a valid starting point
when the following hold. Each is a finite identity between its words that anyone can recompute:

- (P1) Steps 9..12 of (1) and (2) hold for both messages with the same W10, W11, W12 and with
  W'9 = W9 + d9, and W9 lies in V9.
- (P2) Equation (2) holds for both messages at steps 5..8.
- (P3) Step 8 of (1) gives the same E_4 for both messages whenever W'8 = W8 + d8, and E'_5 - E_5 = d5.
- (P4) Step 13 produces no difference: with any W13, E'_13 = E_13 and A'_13 = A_13.
- (P5) A'_10 - A_10 = 00008004, and 00008004 + d18 = 0.

The second part of the advice is the list of 448 valid starting points in Appendix A. All of them
have E_5 = 1d1fa7dd, E_6 = afe878e7, E_7 = 4c97cbe5, the values in the published colliding pair.
E_1..E_4 are not part of a starting point; they are chosen by the algorithm.

Where the starting points come from. They are not taken from the cited papers. We wrote the
identities (P1)..(P5) as a bit-vector problem over the twenty words and solved it with STP and
CryptoMiniSat on one thread. Besides the identities, the problem asks that at least one tuple
(Section 4) exists and that conditions (C14) and (C15) of Section 7 can be met. It fixes E_5, E_6,
E_7 to the published values and E_8 on the bit positions where the published characteristic has a
condition, and it fixes low bits of E_8 - A_4 and of A_3 to one of two patterns, which decides how
many tuples a starting point has. The search was split by the top five bits of A_1, and every
solution found was excluded from the next call by its A_1. These restrictions only select which
valid starting points we obtained. The algorithm uses nothing about them except (P1)..(P5), and
our loader re-checks (P1)..(P5) with exact arithmetic for all 448 before anything else runs. The
solver time is charged in Section 11 and discussed under H3.

The advice is 27 words of constants and 448 * 20 words of starting points, 35948 bytes.

## 4. Phase 1: the table

Take one starting point. For a choice of W8 and W7 it determines E_4 and E_3 by steps 8 and 7 of
(1):

    E_4 = E_8 - A_4 - S1(E_7) - Ch(E_7,E_6,E_5) - K[8] - W8
    E_3 = E_7 - A_3 - S1(E_6) - Ch(E_6,E_5,E_4) - K[7] - W7

and then A_0 and A_-1 by (2) at steps 4 and 3:

    A_0  = E_4 - A_4 + S0(A_3) + Maj(A_3,A_2,A_1)
    A_-1 = E_3 - A_3 + S0(A_2) + Maj(A_2,A_1,A_0).

The second message must reach its states E'_7 and E'_6 from the same E_4, E_3. Writing step 7 and
step 6 of (1) for both messages and subtracting gives two exact conditions:

    (F7)  Ch(E'_6,E'_5,E_4) - Ch(E_6,E_5,E_4) = (E'_7 - E_7) - (S1(E'_6) - S1(E_6)) - d7 = fff8701d
    (F6)  Ch(E'_5,E_4,E_3)  - Ch(E_5,E_4,E_3) = (E'_6 - E_6) - (S1(E'_5) - S1(E_5)) - d6 = ffffffd0

The right-hand sides are the same for all starting points, because E_5, E_6, E_7 are.

A tuple is a triple (j, W7, W8): a starting point number j, W8 in V8, W7 in V7, with (F7) and (F6)
for starting point j. Its key is A_-1.

Phase 1 lists V7 and V8 by one pass over all 2^32 words. For each starting point it keeps the W8
in V8 that satisfy (F7) and tests (F6) on every pair with a W7 in V7. It sorts all tuples by
(key, j, W8, W7) and keeps, for every key, only the first tuple in this order. Results of this
exhaustive computation (ours):

- 296 starting points have 2048 values of W8 that satisfy (F7) and 16896 tuples each; the other
  152 have 12416 such values and 112128 tuples each. That is 22044672 tuples in total.
- The tuples have exactly 4606337 distinct keys. The table therefore has 4606337 tuples, one per
  key.

The same pass over 2^32 words builds bitmaps of V5, V6 and G18. A direct-address array KT has
KT[k] = number of the tuple kept for key k, or 0.

## 5. Phase 2: one trial

A trial draws two fresh uniform 256-bit words r0, r1, sets M0 = r0 || r1 (a uniform 512-bit
block), and computes CV = C(IV, M0) = (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4).

    1. If KT[A_-1] = 0 the trial ends. Otherwise let (j, W7, W8, E_3, E_4, A_0) be the tuple
       KT[A_-1], and let A_1..A_12, E_5..E_12 be the words of starting point j.
    2.   E_2 = A_2 + A_-2 - S0(A_1) - Maj(A_1,A_0,A_-1)                 [(2) at step 2]
         W6  = E_6 - A_2 - E_2 - S1(E_5) - Ch(E_5,E_4,E_3) - K[6]       [(1) at step 6]
         if W6 is not in V6: the trial ends
         E_1 = A_1 + A_-3 - S0(A_0) - Maj(A_0,A_-1,A_-2)                [(2) at step 1]
         W5  = E_5 - A_1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5]       [(1) at step 5]
         if W5 is not in V5: the trial ends
         E_0 = A_0 + A_-4 - S0(A_-1) - Maj(A_-1,A_-2,A_-3)              [(2) at step 0]
         W0  = E_0 - A_-4 - E_-4 - S1(E_-1) - Ch(E_-1,E_-2,E_-3) - K[0]
         W1  = E_1 - A_-3 - E_-3 - S1(E_0)  - Ch(E_0,E_-1,E_-2)  - K[1]
         W2  = E_2 - A_-2 - E_-2 - S1(E_1)  - Ch(E_1,E_0,E_-1)   - K[2]
         W3  = E_3 - A_-1 - E_-1 - S1(E_2)  - Ch(E_2,E_1,E_0)    - K[3]
         W4  = E_4 - A_0  - E_0  - S1(E_3)  - Ch(E_3,E_2,E_1)    - K[4]
         the trial is prefix-valid with (W0..W8) and the words W9..W12 of starting point j;
         go to Phase 3.

Why this is the right prefix. W0..W4 are the unique words that drive the state from CV to the
chosen (A_0..A_4, E_0..E_4): each line is (1) solved for the message word, and the A-equations (2)
at steps 0..4 hold because E_0, E_1, E_2 were defined from them and A_-1, A_0 come from the tuple.
W5 and W6 are the unique words that reach E_5 and E_6 of the starting point. For the second
message, steps 0..4 are identical. At step 5, E'_5 = E_5 + d5 as required by (P3), and A'_5 follows
by (P2). At step 6, (F6) is exactly the statement that W6 + d6 reaches E'_6; at step 7, (F7) does
the same for W7 + d7 and E'_7; step 8 is (P3); (P2) gives A'_6..A'_8. Steps 9..12 are (P1). So
after step 12 both messages are in the states of starting point j, for every prefix-valid trial.

## 6. The prefix-valid set P and its exact measure

Let P be the set of chaining values for which a trial is prefix-valid. P depends only on
(A_-1, A_-2, A_-3). Let U be the uniform distribution on 256-bit chaining values.

Lemma 1. Under U, Pr[CV in P] = 4606337 * 2^-32 * 2^-9 * 2^-18 = 4606337 * 2^-59 (about 2^-36.865).

Proof. The table has one tuple for each of its 4606337 keys, so the events "A_-1 equals key k" for
different table keys are disjoint, and each has probability 2^-32. Fix a key and its tuple. Given
A_-1, the map A_-2 -> W6 is a bijection of the 32-bit words (W6 = constant - A_-2), so W6 lies in
V6 with probability exactly |V6|/2^32 = 2^-9. Given A_-1 and A_-2, the map A_-3 -> W5 is a
bijection (W5 = constant - A_-3), so W5 lies in V5 with probability exactly |V5|/2^32 = 2^-18.
The three words are independent under U. QED.

No count of overlaps is needed here, because only one tuple per key is used. Section 15 explains
why this replaces the corresponding lemma of our first package, which was wrong.

Lemma 2. Under U, conditioned on (A_-1, A_-2, A_-3, A_-4) with CV in P, the words (W0, W1, W2, W3)
are uniform on 2^128 values.

Proof. With the four A-words and the accepting tuple fixed, E_0, E_1, E_2, E_3 are fixed. Then
W3 = constant - E_-1 - (terms in E_0..E_2), a bijection of E_-1. Given E_-1, W2 is a bijection of
E_-2; given those, W1 is a bijection of E_-3; given those, W0 is a bijection of E_-4. The map
(E_-4, E_-3, E_-2, E_-1) -> (W0, W1, W2, W3) is therefore a bijection, and the four E-words are
uniform and independent of the A-words under U. QED.

## 7. Phase 3: completion with W13, W14, W15

After a prefix-valid trial, W0..W12 are fixed and both messages are in the states of starting
point j after step 12. All state words below are those of starting point j. Put

    c16 = W9 + s0(W1) + W0,      c18 = W11 + s0(W3) + W2,

so that W16 = s1(W14) + c16 and W18 = s1(W16) + c18. Phase 3 does the following.

    for each g in G16 with s1(g) + c18 in G18:                       (g will be W16)
        W14 = s1^-1(g - c16)                    (s1 is an invertible linear map on 32-bit words)
        r13 <- fresh uniform word; for i = 0 .. 2^18 - 1:
            x = r13 + i * 9e3779b9                                    (candidate E_13)
            y  = A_10  + E_10  + S1(x) + Ch(x, E_12,  E_11)  + K[14] + W14        (E_14)
            y' = A'_10 + E'_10 + S1(x) + Ch(x, E'_12, E'_11) + K[14] + W14        (E'_14)
            (C14)  require y' - y = 00008004
            (C15)  require E_11 + S1(y) + Ch(y, x, E_12) = E'_11 + S1(y') + Ch(y', x, E'_12)
            r15 <- fresh uniform word; for k = 0 .. 2^12 - 1:
                z = r15 + k * 9e3779b9                                (candidate E_15)
                (C16)  require E_12 + Ch(z, y, x) = E'_12 + Ch(z, y', x) + d16
                u = A_12 + E_12 + Ch(z, y, x) + S1(z) + K[16] + g     (E_16)
                (C17)  require Ch(u, z, y) = Ch(u, z, y')
                on success: W13 = x - [A_9 + E_9 + S1(E_12) + Ch(E_12,E_11,E_10) + K[13]],
                            W15 = z - [A_11 + E_11 + S1(y) + Ch(y, x, E_12) + K[15]], stop.

A Phase-3 call also stops, without a result, after 2^18 values of z in total. A new r13 is drawn
for every g that is tried and a new r15 for every x that passes (C14) and (C15).

What the four conditions mean. By (P4), E_13 = x and A_13 are the same for both messages. (C14)
makes dE_14 = 00008004 = dA_10, which by (2) at step 14 gives A'_14 = A_14. (C15) is step 15 of (1)
with W15 removed from both sides, so E'_15 = E_15 for every W15, and then A'_15 = A_15. (C16) is
step 16 of (1) for both messages with W'16 = W16 + d16, so E'_16 = E_16 and A'_16 = A_16. (C17) is
the only term of step 17 that could differ, so E'_17 = E_17 and A'_17 = A_17. At step 18 the only
differing terms are E_14 and W18, and dE_14 + d18 = 0 by (P5), so E'_18 = E_18 and A'_18 = A_18.
After step 18 the eight state words (A_15..A_18, E_15..E_18) are equal.

The set S. Let S be the set of 32-bit values c18 for which some g in G16 has s1(g) + c18 in G18.
S does not depend on the starting point. Exhaustive computation over all 2^32 values gives

    |S| = 584683520,   |S| / 2^32 = 0.1361322 (about 2^-2.877).

If c18 is not in S, Phase 3 ends at once. By Lemma 2, under U and given CV in P, c18 is uniform
(for fixed W3 it is a bijection of W2) and so is c16 (a bijection of W0), and the two are
independent. So under U, Pr[c18 in S | CV in P] = |S|/2^32 exactly.

The completion rate. Given c18 in S, the search needs an x with (C14) and (C15) and then a z with
(C16) and (C17). We do not prove that such x and z are found within the caps. This is heuristic H2.
Our simulation: for each of the 448 starting points, 100000 samples of uniform (c16, c18) with the
caps above. In total 6100007 samples had c18 in S (fraction 0.13616, against 0.1361322), and all
6100007 were completed. Each completion was checked by running steps 13..18 for both messages
from the starting point's states and comparing the eight state words and the differences of W16
and W18. A completion took 4122 values of x on average. In our runs of the whole algorithm every
prefix-valid trial with c18 in S was completed as well (Section 12, H2).

## 8. Correctness of an output

Lemma 3. If Phase 3 succeeds after a prefix-valid trial, then C(CV, M1) = C(CV, M1') for
M1 = (W0..W15) and M1' = M1 with d5..d9 added to words 5..9.

Proof. Message words: W5..W8 lie in V5..V8, W9 lies in V9 by (P1), W16 = g lies in G16 and W18
lies in G18, so every line of the expansion table in Section 3 holds: d16 = d9, d18 as stated, and
no difference in W17 and W19..W30. State: Section 5 shows both messages reach the states of the
starting point after step 12. Section 7 shows the eight state words are equal after step 18.
Steps 19..30 use equal states and equal message words. The feed-forward adds the same CV. QED.

The algorithm does not rely on this lemma for its output: it re-hashes both 128-byte messages with
three compressions each, compares the digests, and outputs only on equality (Section 9, step 4).
So a returned pair is always a collision of distinct messages.

## 9. The complete algorithm, with its caps

    Parameters:  N = 2^40 trials,  Q = 2^16 Phase-3 calls.
    0. Load the advice. Check (P1)..(P5) for every starting point. Run Phase 1.
    1. For i = 1 .. N: run one trial (Section 5).
    2. If the trial is prefix-valid: if Q Phase-3 calls have already been made, stop and FAIL.
       Otherwise run Phase 3 (Section 7).
    3. If Phase 3 fails, continue with the next trial.
    4. If Phase 3 succeeds: build m and m', hash both, check the digests are equal and m != m',
       output (m, m') and stop.
    5. After N trials without output, FAIL.

There are no restarts. All coins are fresh uniform 256-bit words from the model's random-word
primitive: two per trial, and one per r13 or r15 in Phase 3.

## 10. Success probability

Probability space: the algorithm's coins only. The target and the advice are fixed.

Trials are independent and identically distributed, because each uses fresh coins and the same
deterministic tables. Let D be the distribution of C(IV, M0) for a uniform block M0. Let

    q_U = probability that one trial ends in a successful Phase 3 when CV is drawn from U,
    q_D = the same probability when CV is drawn from D (the real algorithm).

By Lemma 1, the exact value of |S| and heuristic H2 (completion rate at least 0.99 under U),

    q_U >= (4606337 / 2^59) * (584683520 / 2^32) * 0.99 > 1.0769 * 10^-12 > 2^-39.757.

Heuristic H1 says (a) q_D >= q_U / 2, and (b) Pr_D[CV in P] <= 64 * 4606337 / 2^59.

The algorithm fails only if no trial among N wins, or if more than Q prefix-valid trials occur.

- No win: (1 - q_D)^N <= exp(-N q_D) <= exp(-N q_U / 2). With N = 2^40, N q_U >= 1.1840, so this
  is at most exp(-0.5920) < 0.5533.
- Cap Q: the number of prefix-valid trials has mean at most N * 64 * 4606337 / 2^59 < 562.4 by
  H1(b). By Markov's inequality it exceeds Q = 65536 with probability at most 562.4 / 65536 < 0.0086.

So Pr[success] >= 1 - 0.5533 - 0.0086 = 0.4381 > 0.39. The claim declares 0.39.

Under exact uniformity (q_D = q_U) the success probability would be about 0.685. The factor 2 in
H1(a) is deliberate slack, and N is larger than the claimed 0.39 needs. Section 12 gives the
sensitivity.

## 11. Cost

Units: one 31-step compression (expansion, 31 steps, feed-forward) costs 1. Every other primitive
operation on 256-bit words (load, store, add, subtract, AND, OR, XOR, NOT, shift, rotation,
comparison, branch, random word) costs 1/2140. A 32-bit rotation is charged as shift, shift, OR,
AND. Additions modulo 2^32 are charged as add plus AND. All bounds below hold for every run.

Data layout. KT is an array of 2^32 words. The bitmaps B5, B6, B18 hold one bit per 32-bit value,
256 bits to a word: 2^24 words each. Each tuple record stores j, W7, W8, E_3, E_4, A_0 and seven
precomputed constants, one per word: 13 words per record. Each starting point is stored as 40
words (both messages). A 4 x 256-entry table gives s1^-1 one input byte at a time.

Phase 1 (T1). One pass over the 2^32 words w: membership tests for V5, V6, V7, V8, G18 (each two
evaluations of s0 or s1, at most 14 operations per evaluation, plus add, subtract, compare,
branch: at most 40), three bitmap updates (at most 24) and KT[w] = 0 (2). That is at most 256
operations per w, 2^40 in total. Per starting point: the (F7) test on the 49408 words of V8 (at
most 24 operations each) and the (F6) test on at most 12416 * 512 pairs (at most 64 operations
each), under 2^28.7 operations, so under 2^37.6 for 448 starting points. Building the 22044672
tuple records takes at most 2^10 operations each (2^34.4), and a merge sort of the records by key
takes at most 25 passes of 16 operations per record (2^33.1). In total fewer than 2^41
operations, so T1 < 2^41 / 2140 < 2^30 units. Checking (P1)..(P5) for 448 starting points is far
below one unit.

One trial (always charged in full, whether or not the key is hit). Fixed part: 2 random words,
the compression call with its argument and result moves (8), extraction of A_-1, A_-2, A_-3 (5),
the KT lookup and branch (3), loop counter, comparison and branch (4): at most 32 operations and
one compression. Tuple part, charged on every trial:

    W6 test:  load kappa, subtract A_-2, mask, bitmap index, load, bit select, branch       <= 10
    W5 test:  E_2 = A_-2 + const (3);  Maj(A_0,A_-1,A_-2) = k1 ^ (m1 & A_-2) (4);
              Ch(E_4,E_3,E_2) = k2 ^ (m2 & E_2) (4);  W5 = const + Maj - Ch - A_-3 (5);
              bitmap test (7);  padding (5)                                               <= 28

Here kappa, k1, m1, k2, m2 and the two constants are fixed per tuple and stored in its record. A
trial therefore costs at most 1 compression and 70 operations. We charge 107 operations:

    T2 <= N * (1 + 107/2140) = 1.05 * 2^40 units.

Phase 3 (T3). One call: computing W0..W4, c16, c18 (at most 256 operations); 64 membership tests
in G18 by bitmap with s1(g) precomputed (at most 12 each); for each g, W14 by 4 table lookups (at
most 24) and at most 2^18 values of x at no more than 96 operations each (two Ch, three S1, the
additions and comparisons of (C14), (C15)); and at most 2^18 values of z per call at no more than
64 operations each. That is at most 64 * 2^18 * 96 + 2^18 * 64 + 2^13 < 2^31 operations, under
2^20 units per call. At most Q = 2^16 calls are made:

    T3 <= 2^36 units.

Final check (T4): 6 compressions and fewer than 2140 operations, at most 8 units.

Advice (T0 and Tsp): see H3 in Section 12. T0 = 2^44 units for the work of the cited authors
behind the characteristic and the three shared state words. Tsp = 2^39 units for our own solver
runs that produced the 448 starting points.

Total.

    T1 + T2 + T3 + T4 < 2^30 + 1.05 * 2^40 + 2^36 + 8 < 1.114 * 2^40
    T = T0 + Tsp + T1 + T2 + T3 + T4 < 2^44 + 2^39 + 1.114 * 2^40 = 17.614 * 2^40 < 2^44.139

`time_log2` is 44.14. `preprocessing_log2` is 44.05, a bound on T0 + Tsp + T1 (16.501 * 2^40 <
2^44.045), which is included in the total.

Memory. KT: 2^32 words. Bitmaps: 3 * 2^24 words. Tuple records before the reduction: 22044672 * 13
words, under 2^29 words, and the merge sort uses a second buffer of the same size. Starting
points, code, constants, the s1^-1 table, the current block, state and counters: fewer than 2^15
words. Total below 2^32 + 2^26 + 2^30 + 2^15 words, under 2^32.4 words = 2^37.4 bytes, so
`memory_log2_bytes` = 38. KT is written in full in Phase 1 and the bitmaps are built by stores
into zeroed words, whose zeroing (3 * 2^24 stores) is inside the Phase-1 allowance.

Advice. The stored advice is 35948 bytes; `nonuniform_advice_log2_bytes` = 16. The work that
produced it is charged as T0 + Tsp.

## 12. Declared heuristics

H1 (near-uniformity on two fixed sets; score-critical). For a uniform 512-bit block M0 and
CV = C(IV, M0): (a) the probability that a trial wins is at least half of what it is for a uniform
CV; (b) the probability that CV lies in P is at most 64 times what it is for a uniform CV.

- Role: (a) gives the success bound; (b) only bounds the chance of hitting the cap Q.
- Why it is weaker than the usual assumption: the source attacks assume the chaining values of
  arbitrary first blocks behave uniformly with respect to these conditions. H1 asks for a factor 2
  in one direction and a factor 64 in the other, on two explicit sets, and nothing else.
  Independence of trials is not assumed; it holds because the blocks are fresh coins.
- Evidence, run C (our own run, not organizer-executed). We ran the algorithm of Section 9 with
  the table and caps of this document for 2^44 trials on real 31-step chaining values,
  without stopping at the first collision. First blocks came from eight splitmix64 streams seeded
  by the operating system. Observed against expected under U: key hits 18867676479 against
  18867556352; W6 test passed 36856301 against 36850696; prefix-valid trials
  136 against 140.6; of those with c18 in S 15 against
  19.1; collisions 15. Every collision was re-hashed, and all of them are
  certificates, which the organizer verifies.
- Evidence, runs A and B (our own, earlier). The same starting points with a larger table that
  keeps up to eight tuples per key (16712164 tuples; the table of this document is a subset of
  it). Run A, 125 * 2^32 trials on the processor with xoshiro256** streams: key hits 575750347
  against 575792125 expected under U; W6 test passed 4078714 against 4080118. Run B, 2^42 trials:
  key hits 4716914481 against 4716889088; W6 test passed 33421406 against 33424328; 122
  prefix-valid trials, of which 15 had c18 in S (0.1361 * 122 = 16.6), and all 15 were completed
  and collided. These two runs use a different table and are quoted only as support for the
  uniformity of the three chaining words.
- Not tested: the organizer cannot run a search of this size, so the counts above are ours. The
  organizer experiment `trial-replay` (Section 13) repeats the tests of a trial on stored first
  blocks; it shows that the trial procedure is the one specified and says nothing about rates.
- Sensitivity: if the true ratio in (a) is rho instead of 1/2, the success bound becomes
  1 - exp(-1.1840 * rho) - 0.0086: rho = 0.45 gives 0.404, rho = 0.43 gives 0.390, rho = 1 gives
  0.685. Time scales as 1/rho for a fixed success target. If (b) failed by more than a factor 64
  the cap term would grow in proportion; a factor 2^10 would make it 0.137.

H2 (completion rate; score-critical). For a uniform chaining value conditioned on being in P with
c18 in S, the capped search of Section 7, with its fresh offsets, finds (W13, W14, W15) with
probability at least 0.99.

- Evidence: the simulation of Section 7 (6100007 sampled cases over all 448 starting points, all
  completed and checked); every prefix-valid trial with c18 in S in runs A, B and C was completed;
  and the organizer-run experiment `trial-replay`, which executes the same routine with the same
  caps for each organizer seed and has every returned pair checked as a full collision.
- Limits: the simulation and the runs are our own. The organizer experiment uses 15 stored
  prefixes with varying offsets, so it tests the routine and the caps, not the spread over
  prefixes.
- Sensitivity: a completion rate of 0.9 instead of 0.99 lowers N q_U from 1.1840 to 1.0765 and the
  success bound to 0.407; the claimed 0.39 needs a rate of about 0.85 or more at this N.

H3 (cost of producing the advice; score-critical). (a) The computations by the cited authors that
produced the characteristic and the three state words shared by all starting points cost at most
T0 = 2^44 units in total: the search for the 31-step characteristic (Li, Liu, Wang, EUROCRYPT 2024,
Section 4.2) and the collision run of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024), from whose
colliding pair E_5, E_6, E_7 are read. (b) Our own solver runs that produced the 448 starting
points cost at most Tsp = 2^39 units.

- Conversion: one CPU-second of one thread is charged as 2^23 units, that is 2^34.06 word
  operations per second. For comparison, our compiled 31-step compression runs at 5.8 * 10^6 per
  second per thread on the test machine (2^22.5 units per second), so every CPU-second is charged
  as more than a second of pure compression work. As a second check we counted the instructions of three of the single-thread solver calls with valgrind (cachegrind, cache simulation off): 3.99 * 10^11, 5.12 * 10^11 and 5.17 * 10^11. The native runs of the same three calls took 372.4, 207.4 and 174.9 CPU-seconds, which the conversion charges as 1.35 * 10^13 word operations in total, 9.5 per counted instruction. The solver's answers under valgrind differed from the native ones, so the two executions did not follow the same search path and this comparison is indicative only.
- (a) The collision run. The authors report 1.2 hours on 64 threads for their whole attack,
  including the generation of all their starting points. That is 276480 thread-seconds, charged as
  276480 * 2^23 < 2^41.08 units.
- (a) The characteristic search. Its run time is not published. We re-ran the authors' public
  search script for 31-step SHA-256 (`find_dc_model_31_256.py` from their repository, unmodified,
  which calls STP with CryptoMiniSat on 26 threads) with STP built from tag 2.3.4 and CryptoMiniSat
  5.11.21 on a 32-thread machine. The script lowers a Hamming-weight bound by one per solver call.
  It ran to its end: 40 calls returned a characteristic (bounds 60 down to 21) and the call for
  bound 20 proved that none exists. Seven calls crashed and were repeated; all 48 solver processes
  are counted. They took 113801.5 CPU-seconds, with a peak of 6.1 GB of memory. An earlier start of
  the same script that we stopped took 7282.9 CPU-seconds. The authors' second script
  (`correct_dc_model_31_256.py`) solves one model without a weight bound; 27 calls of it took
  11205.2 CPU-seconds before we stopped it. Together that is 132289.6 CPU-seconds, under 2^40.02
  units. With one solver thread per call the same 41 weight bounds took 10124.1 CPU-seconds in 42
  processes (one repeat after a crash), with 1.15 GB of memory.
- (a) The allowance. 2^44 units is 2^21 CPU-seconds. After the 2^41.08 charged for the collision
  run, 1820672 CPU-seconds (2^43.796 units) remain for the characteristic search. That is 16.0
  times the complete 26-thread run of the search script, 13.8 times all the 26-thread solver work
  listed above, and 180 times the single-thread run.
- (a) Limits. Neither re-run outputs the published characteristic. Each returned 40
  characteristics with the same message words carrying differences, and none has the published
  message differences. We also could not build starting points on the script's own
  characteristics: with all state differences taken from one of them, the starting-point problem
  of Section 3 is unsatisfiable. The authors' second script has rows of the characteristic written
  into it by hand, so the published script is not their whole procedure, and attempts they made
  outside the public scripts are not recorded anywhere. H3(a) is therefore an allowance anchored
  to a measurement of the published search script, not a measurement of the historical search.
- (b) Our starting points. The solver was called 489 times, on one thread each: 448 calls
  returned a starting point, 40 returned "unsatisfiable" and ended their part of the search, and
  one ended without an answer. The 489 calls took 12046.1 CPU-seconds in total (the longest took
  50.5), which is 2^36.56 units. Tsp = 2^39 units is 65536 CPU-seconds, 5.4 times that. The margin
  also covers calls that were still running when we stopped the batch and so left no log line: at
  most one for each of the 64 parts of the search.
- Sensitivity of the total: T0 = 2^45 gives 2^45.07, 2^46 gives 2^46.04, 2^47 gives 2^47.02 and
  2^48 gives 2^48.01. Charging a CPU-second at 2^24 or 2^25 units in (b) gives 2^44.18 or 2^44.26.

## 13. Evidence and how to check it

Certificates (organizer-verified). `collision-01` .. `collision-15` are the outputs of run C:
pairs of distinct 128-byte messages M0 || M1 and M0 || M1' with equal 31-step digests, each with
its own first block and found by the algorithm of Section 9. They show that the algorithm produces
collisions of the target. No certificate is used as a cost.

Organizer experiment `trial-replay` (`experiments/replay.py`, kind `python-message-pairs-v1`,
event `full-collision`). The program stores, for each certificate, its first block M0, the
starting point that accepted it and the tuple (W7, W8). For each organizer seed it picks one of
these records, checks (P1)..(P5) for the starting point, computes CV = C(IV, M0), repeats the
tests of Sections 4 and 5 for that tuple (W8 in V8, W7 in V7, (F7), (F6), the key, W6 in V6, W5
in V5), rebuilds W0..W6, and runs Phase 3 with r13 and r15 taken from a stream derived from the
seed, with the caps of Section 7. It returns M0 || M1 and M0 || M1' only if C(CV, M1) = C(CV, M1').
It does not search for first blocks and does not build the table. Every returned pair is a claimed
full collision that the organizer re-hashes. The records are first blocks that our run had already
found to win, so the experiment cannot be read as a success rate.

Our own computations (not organizer-executed; stated so they can be weighed as such). All were
written in C from the definitions in this document and run on one 32-thread machine with an
8 GB graphics card:

- the sizes of V5..V8, G16, G18 and S, each by a loop over all 2^32 words;
- the check of (P1)..(P5) for the 448 starting points, and the table: 22044672 tuples and 4606337
  distinct keys;
- the completion simulation of Section 7;
- runs A, B and C quoted under H1. In runs B and C the first-block hashing ran on the graphics
  card, which passed on every block whose A_-1 is a table key; the trial of Section 5 was then
  run from scratch on each such block by the same program as in run A. The card's selection was
  compared with a pass on the processor over the first 2^22 blocks of each run and was identical,
  and the number of blocks passed on equals the number of key hits in every run.

Our counts |V5| = 2^14, |V6| = 2^23, |V7| = 512, |V8| = 49408 differ from the figures 2^14, 2^23,
2^27, 2^25 quoted in the source paper for W5..W8. Ours are for the exact modular conditions of
Section 3 with these difference constants, and they are the ones the algorithm uses. Our completion
density 0.136 (2^-2.88) is also lower than the paper's estimate of 2^-1.3 from 100 tests. We use
our own figures throughout; they make the claimed cost higher, not lower.

## 14. Scope and limitations

- This is an application of published cryptanalysis with new accounting and our own starting
  points. The characteristic and the values of E_5, E_6, E_7 come from the cited authors.
- The score is almost entirely H3(a), an allowance for the cited authors' work. Our own measured
  work (solver runs, table, trials, completion) is below 2^40.7 units with the margins above.
- The attack was executed by us at the claimed trial count. The organizer verifies the resulting
  collisions and re-runs the trial and completion steps on their first blocks, but cannot repeat
  the search.
- The time bound is a cap on every run. Only the success probability depends on H1 and H2.
- A passing exploratory review is an AI screening result, not a proof and not human acceptance.

## 15. Changes from our first package (claim 48.35)

- Lemma 1 of the first package was wrong. It said that the acceptance sets of the 16896 tuples of
  the published starting point are pairwise disjoint and that their union has 16896 * 2^37
  triples. Tuples that share a key do overlap: the union is smaller than the sum by 1279000576
  triples. Another solver reported this, and we confirmed it. The claimed score of that package
  did not depend on the difference, but the statement was false. This package avoids the question:
  the table keeps one tuple per key, and tuples with different keys cannot accept the same
  chaining value.
- The first package used the published starting point and was not executed. This one uses 448
  starting points of our own, and its trial count was run in full.
- The completion experiment of the first package reused one offset per trial and did not apply
  the cap of 2^18 values of z. The new experiment draws a fresh r13 for every g and a fresh r15
  for every accepted x, applies all three caps, and also repeats the tests of a trial.
- The re-run of the characteristic search is now complete, and its numbers are given under H3.

## Appendix A. The 448 starting points

One starting point per line: its number, then A_1..A_12 and E_8..E_12. In every starting point
E_5 = 1d1fa7dd, E_6 = afe878e7 and E_7 = 4c97cbe5. The second message's words follow from the XOR
differences of Section 3. SHA-256 of the list as 448 lines of 20 hexadecimal words (A_1..A_12 E_5..E_12,
single spaces, one line feed after each line): e4884d7e3f1ac19782ff8a650a0adcfdb697a170af9e7eccbd998a2078f6ba82.

      0  024f4dc7 b660c003 9d02b412 d06266c3 fad053fb f1ee5d4e 8ff09384 3d9fb6ad e9c5fb04 21c82d79 471b315a 6bf71249 947b8048 a1c301d3 7026b3fa aa2f2419 cffbf20b
      1  072ff0fb fe87da07 098eb413 666666c3 fa9053ff 3bfb554a 87f59204 519bb605 45c6d7f0 2faf4f91 b4363bc5 71cd7544 947f8048 a1c721d1 7026b3fa 6c3f0c18 31f391e8
      2  05674912 5a1fc202 7fff7412 636266c3 fa9053fb f1ef5d4e abf4138c 93d3d73f 0d8cfa04 6a934c88 7fb474aa 16a470cb 946b8048 41d161d3 f00293fa ec3f0418 4f77820b
      3  07463832 cff2c202 a1e4b412 754566c3 fa9053fb f1ee5d4e 8bf09384 97c0d69d 0d5e9362 f00f1049 f5a27e87 0f6a42f6 947f8048 a1c711d3 f02293fa 2a371c18 316fd9ec
      4  01ddd1d4 0e42da07 a141b412 da2566c3 fa9053ff bbbb554a 8ff59204 db9c75e5 ab1c5a0a 4c021580 9cb2abd4 f30abcbc 947f8048 61d101d1 7026b3fa aa370418 8f6dfa0f
      5  002b9013 f682da07 418db413 226166c3 fa9053ff 3bfb554a 0ff59204 f39077e5 05467bca 82ce6f48 014ab986 442aba25 946b8048 41d161d1 7006b3fa 2a2f1c18 cfe7fa0f
      6  05923e77 a8aec003 cf04b413 2a7166c3 fad053fb 11ae5d4e 8ff19204 7b8a7605 89c25818 560b42e3 656be1d4 91bcf794 947b8048 a1d701d3 f02293fa aa3f341d 0f7daa0a
      7  06dea55f 8cbed806 14923413 f16166c3 fad053ff 33fe554a 0bf1120c 35de97f7 c3969cfe cd3b1633 92751463 b08a5f83 947b8048 81d701d1 f00293fa 2a3f2c18 8f618a0e
      8  04e03900 960fda07 1853f413 ef2266c3 fa9053ff 33ff554a 0bf19204 35ce97f5 63c69474 80ed3fca aa9c7ca0 bb34505b 946b8048 61d171d1 f02293fa aa2f1418 8fe5e20f
      9  06eea75f 8c8eda07 14923413 f16166c3 fa9053ff 33fe554a 0bf1120c 35de97f7 c3c69cfe 8d5337b2 f6331743 0f2c7d78 947b8048 81c701d1 7006b3fa 2a2f2419 f1e981ed
     10  0d1ba503 d473c003 be123412 cf7266c3 fad053fb f9eb5d4e 83f0138c 3dcf96bf a5c2bc8a e3d178da 49cb085d 921d2d6f 947b8048 a1d701d3 f02293fa ec37341d b16f91ec
     11  09fe46ef 708eda07 94923413 c57566c3 fa9053ff 33fe554a 8bf5120c f1cf95d7 67def7ee fd3f1111 9f96022b cbfa01a2 947f8048 41d501d1 f00293fa 2a271418 0f79b20a
     12  0978d72c 3221c202 7bb83413 712666c3 fa9053fb 19ab5d4e 0bf1120c 95de97f7 c1c6ba84 56eb7cc3 54704603 332227e9 947f8048 81c721d3 f00293fa ec3f3418 4fff820a
     13  0f0d5ee6 2523c202 84fdf412 ee6166c3 fa9053fb 99ea5d4e a7f59204 d18ab685 e3c1da8e 25eb3c52 6d201179 d70e6ca8 946b8048 61d161d3 7026b3fa 6c2f3c1d f1f181e9
     14  09824910 183eda07 9c463412 e52166c3 fa9053ff b3be554a a3f1120c dfcbd657 6551b8d4 3d2e0631 4a6c6c6a ff8d0152 946b8048 41d161d1 7006b3fa aa373c19 3173c9e9
     15  0998d72b 3251c003 7bf83413 716666c3 fad053fb 19ab5d4e 0bf1120c 95de97f7 c196ba84 16d77a42 be694543 f17d4138 947f8048 81d721d3 f00293fa 2a373c19 8ff1b20a
     16  0e6ba6e3 39c4c202 bbb6b412 7f1666c3 fa9053fb 91ee5d4e 83f19204 1fd9d5d5 8948d2e0 802c064b 53cc7fc7 2e2117b4 946f8048 61d571d3 f02293fa ec270c18 b177f9e9
     17  0be5d790 560fda07 b82ff413 231266c3 fa9053ff 33ff554a a3f59204 93ded675 a743f13a 0fa05db0 bf1b1994 b9a77186 946b8048 41d171d1 7006b3fa 6c2f2c18 0f7d820a
     18  529f17a3 1672c003 840f3412 617166c3 fad053fb 99eb5d4e a3f5120c 5bcbd677 8d03fad2 dc3f05a1 895d78e4 73cc234c 947b8048 a1d701d3 7026b3fa aa2f0c1d b1e7f9ec
     19  51eecf34 0e52da07 a141b412 5a3166c3 fa9053ff bbbb554a 8ff59204 5b8c75e5 0b0e578a 47c17bf0 31739bdc 75f8bd8d 947b8048 a1c301d1 f02293fa aa3f1418 b16fb9ec
     20  556189d3 31c8c202 e1aff412 bb1666c3 fa9053fb 99ea5d4e 0bf59204 b9de97d5 abc4f302 a33951f8 8c632d1d ea2d399e 946f8048 61d171d3 7026b3fa aa2f3c19 716981ec
     21  56e53654 cffec202 0194b413 750166c3 fa9053fb 71ae5d4e 8bf09384 97c0d69d 0d5e9362 f0533049 a82b7c2c 689b60a7 947b8048 a1c711d3 7026b3fa ec2f141d f161d9ec
     22  522545f3 606fc003 80137412 037666c3 fad053fb f1ef5d4e abf4138c f3d3d73f 8545b984 9d7c2091 26da6fd1 61f705fb 947f8048 81c721d3 f00293fa aa272c18 71edc9ed
     23  56e2de9e 2d00c202 8eeeb412 e65266c3 fa9053fb 91ee5d4e a7f59204 d19db685 8fd299e6 0c910c02 f8cf4659 fd027fdb 946b8048 41d161d3 f00293fa 6c2f0c1d cfe7ba0f
     24  5533a63e 8f07d806 6a857412 117566c3 fad053ff bbba554a 8bf1120c b5ca95f7 ab99b91e e51917f2 26764ea3 087c782b 947f8048 81d721d1 f00293fa aa3f2419 b16fc1ed
     25  522547f2 603fc202 80137412 037666c3 fa9053fb f1ef5d4e abf4138c f3d3d73f 8585b984 9d8c1a92 995634d8 3372611b 947f8048 81c721d3 f00293fa 6c270c1c b17fd9e8
     26  544e8fc6 d032c202 bb01f412 d86666c3 fa9053fb f9ea5d4e 87f09384 379f76cd a5905b3a cfa65b12 3bf88477 78d4c087 947f8048 61d101d3 f02293fa 2a3f1c19 f16db9ec
     27  57272fd7 7505c202 b6a43413 bc5666c3 fa9053fb 19ab5d4e 0ff5120c 3b9f77e7 8f021312 1927009a 53dc871d ef59f787 946f8048 61d171d3 f02293fa 2a2f241d f1f1a1e8
     28  54cfc794 a214c003 e9b3f413 c32266c3 fad053fb 19aa5d4e 03f59204 33ded7f5 230794e0 2bc76b18 19ae4657 157228e7 947b8048 81d711d3 7006b3fa aa3f1c19 cfffba0b
     29  57f44e2c 8e57da07 6946b412 123666c3 fa9053ff bbbb554a 87f19204 b58ab5e5 e794db10 0dea3bb0 3dec674f 8c75117c 947f8048 41d101d1 7006b3fa aa3f1c19 cf73820a
     30  50ce85fc 6a32c003 2bc4b413 833566c3 fad053fb 11ae5d4e 8bf59204 11cf95d5 6d82926a 6a9a4a28 2a897c6f f4c70e9d 947f8048 81d711d3 7006b3fa 2a271419 8fe1920e
     31  50e25dbf 9554c003 dcf3f413 d66666c3 fad053fb 19aa5d4e 0ff59204 1f9e77e5 27c61a90 2b4d613b 408ee44e 7f51fe87 947f8048 81c721d3 7006b3fa 2a271419 f16191ec
     32  5c33d7cf 2e50da07 84723413 b35266c3 fa9053ff 53fe554a 83f0138c 31df96bf 8303bcf4 69931a98 caa07ae0 6fe756aa 946b8048 61c161d1 7026b3fa aa2f0418 71fde9e8
     33  5f9b8798 de44da07 8a437412 452266c3 fa9053ff bbba554a abf5120c 79d99657 6dc0bade eda20a13 0fe22c8a 73152a5a 947b8048 a1c301d1 f02293fa 2a37041d 0ff1ba0b
     34  5eaca640 8c4eda07 744a3412 113566c3 fa9053ff b3be554a 8bf1120c b5ca95f7 63d3991e 7e7f7122 c35a2990 33fd40bb 947f8048 41d101d1 7006b3fa ec27041c 7175c9e8
     35  58f3a027 7146c202 18c53413 167566c3 fa9053fb 79ab5d4e 87f0138c f78076cf 891a1414 689e0d29 574186b2 695f9a4a 946f8048 41c571d3 7006b3fa aa3f2419 716df9ec
     36  58692183 5c47da07 6926b412 084666c3 fa9053ff dbbb554a aff09384 fd80b72d 0bc4bb16 0cb51a83 0d2a62da 7e191723 947f8048 41d101d1 f00293fa ec370c1d 31e3f9ed
     37  5dce4814 39ffc202 5fc37413 833266c3 fa9053fb 71af5d4e abf4138c 73d3d73f 45819b84 ad712633 02667478 3df75f01 947b8048 a1c701d3 f02293fa 2a2f041d 71e191ec
     38  5c0d450e fef3d806 2a817412 e56166c3 fad053ff bbba554a 0bf5120c b1df97d7 8f86faee afc26a30 03de4322 0ed1628b 947b8048 a1c301d1 7026b3fa ec2f3418 4fff8a0b
     39  5d23dfe7 693dc202 0ac67413 0e7166c3 fa9053fb 71af5d4e 87f0138c f78076cf 89161414 60990cc9 5e259fd1 0202fb8a 946b8048 41c171d3 7006b3fa aa273c18 71f181e8
     40  586f4f4a 8f03d806 2986b412 527266c3 fad053ff bbbb554a 07f19204 558eb7e5 6f44d9f0 4341607b c01e231d 2fff2ab6 947b8048 81c301d1 f00293fa aa3f1418 31e381ec
     41  5ece471c a213c003 61b1f413 eb2566c3 fad053fb 19aa5d4e abf59204 d1da9655 ed82d022 f1821c58 c6927725 24ef7e16 947f8048 a1d711d3 f02293fa aa2f0c19 8ff1820b
     42  5fdf9014 f642da07 e141b412 a22166c3 fa9053ff bbbb554a 0ff59204 f39077e5 85067bca a2da6f49 7b0aad6c 1df48454 946b8048 41d161d1 7006b3fa 6c27141d 0f65ca0f
     43  5d336766 0704d806 92837412 617666c3 fad053ff bbba554a a3f5120c 5bc9d677 85119adc e9e92d3b 490d7c30 a55325f1 947f8048 81d721d1 7006b3fa ec27041d 71e1e9ed
     44  5e76745b 5830c003 69d2b413 f54266c3 fad053fb 71ae5d4e a3f49384 f9c3971d 619cb120 43e96adb 8b9774a4 73586f4d 947b8048 a1c311d3 f02293fa aa372c1d 4f6b820e
     45  5b9d4910 fe43da07 2a417412 e52166c3 fa9053ff bbba554a 0bf5120c b1df97d7 8fc6faee 2fae4c31 a36b03c8 0a157621 947b8048 a1c301d1 f02293fa 6c3f0c1d 7175c9e9
     46  5e56785c 5800c202 6992b413 f50266c3 fa9053fb 71ae5d4e a3f49384 f9c3971d 61dcb120 43f96cda 3dab7b9f 58b303af 947b8048 a1c311d3 f02293fa 6c272c19 31ffd1e8
     47  59e8110c 164fda07 3b4bf412 ca3666c3 fa9053ff b3bf554a 07f19204 d58eb7e5 2f88fbf0 3b787499 ed940c0e 971802b5 947f8048 a1c721d1 f02293fa aa370419 b1ebe9ed
     48  5e62a8c3 39c0c202 bbb2b412 ff1266c3 fa9053fb 91ee5d4e 83f19204 9fd9d5d5 8948d0e0 700403cb 91e418e7 b48e3477 946b8048 41d171d3 f00293fa aa372c18 0ffde20b
     49  5cb36768 0654da07 92437412 613666c3 fa9053ff bbba554a a3f5120c 5bc9d677 85419adc 29ed2fba 95207d2b 07772b6b 947f8048 81c721d1 7006b3fa ec370419 4fffaa0b
     50  5cbe980a 5e41c202 24103412 097666c3 fa9053fb 99eb5d4e a3f5120c b3cad677 8f46f92a 6b5f771a 537207d7 49fe79d6 947f8048 61d501d3 f02293fa ec3f3419 8ff9920b
     51  600b8796 def4d806 8a837412 456266c3 fad053ff bbba554a abf5120c 79d99657 6d80bade edb20c12 41965d89 69101f23 947b8048 a1c301d1 f02293fa 6c2f2c1d 8ffdda0a
     52  655889b3 31c4c202 e1aff412 bb1266c3 fa9053fb 99ea5d4e 0bf59204 b9de97d5 abc4f302 a33951f8 0c6b151c 6aa7415e 946b8048 61d171d3 7026b3fa 2a372418 716db1ed
     53  64d2c774 a214c003 e9b3f413 c32666c3 fad053fb 19aa5d4e 03f59204 33ded7f5 230794e0 2bc76b18 db965e57 a44a7cae 947f8048 81d711d3 7006b3fa 6c273419 4f7fe20a
     54  67222fb7 7501c202 b6a43413 bc5266c3 fa9053fb 19ab5d4e 0ff5120c 3b9f77e7 8f021312 1927009a 53dc871d 8ccdd7ae 946b8048 61d171d3 f02293fa 2a2f241d 8f65820f
     55  67f24f2c 8e57da07 2946b412 523666c3 fa9053ff bbbb554a 07f19204 558eb7e5 8f88f9f0 0b717299 87a50106 e94e1b0f 947f8048 a1c721d1 f02293fa 6c2f3c19 7161f9ed
     56  66ee3634 cffec202 0198b413 750566c3 fa9053fb 71ae5d4e 8bf09384 97c0d69d 0d5e9362 f0533049 a8336c2c e6df4406 947f8048 a1c711d3 7026b3fa ec37041d 4f73c20b
     57  624e51a6 ce34c202 a506b412 506666c3 fa9053fb f1ee5d4e 87f09384 b79f76cd c5945d3a 8f905f32 06d7893f b647d164 947f8048 61d501d3 f02293fa ec271c19 0fe9c20f
     58  602f8e13 7682da07 c18db413 a26166c3 fa9053ff 3bfb554a 0ff59204 739077e5 454279ca d2e16fe8 7e4399b7 f0fead75 946b8048 61d161d1 7026b3fa 6c373c19 f1fde1e8
     59  62cec7bc b213c003 e9b1f413 db2166c3 fad053fb 19aa5d4e 03f59204 1bdfd7f5 29079488 92825aea 7e5901df 85760207 947b8048 81d711d3 f00293fa ec271419 b1e7f9ec
     60  60bb861c 6a2ec003 2bc0b413 833166c3 fad053fb 11ae5d4e 8bf59204 11cf95d5 6d82926a 6a9a4a28 eca17c6f 08470445 947b8048 81d711d3 7006b3fa ec3f1419 0fedba0e
     61  6e67a8e3 39c4c202 bbb6b412 ff1666c3 fa9053fb 91ee5d4e 83f19204 9fd9d5d5 8948d0e0 700403cb d3dc10e7 c4ee0aaf 946f8048 41d171d3 f00293fa ec2f2418 8ff1ca0b
     62  6ce545f4 3a03c202 dfc77413 033666c3 fa9053fb 71af5d4e abf4138c f3d3d73f 8585b984 9dd03a92 c70f7e78 83272232 947f8048 81c721d3 7006b3fa aa272c1c f179b9e8
     63  69ee0e0c 964fda07 7b4bf412 0a3666c3 fa9053ff b3bf554a 87f19204 b58ab5e5 e798db10 e5ed3b50 a0d7578e 096f110f 947f8048 41d501d1 7006b3fa ec2f0c18 8ffd820a
     64  68f0a047 7142c202 18c53413 167166c3 fa9053fb 79ab5d4e 87f0138c f78076cf a9161414 70bc0c49 e238c80a f61e8f72 946b8048 61c171d3 7026b3fa aa3f2419 f169f1ed
     65  69b246f0 1052da07 b4463412 453566c3 fa9053ff b3be554a 8bf5120c 71cf95d7 67def9ee cda70991 e9db7c51 630a4c4b 947f8048 61d101d1 f02293fa 6c3f0c1c f1f191e9
     66  699cd52b b251c003 fbf83413 f16666c3 fad053fb 19ab5d4e 0bf1120c 15de97f7 c182bc84 b6fe7d62 738c6a62 ebfe7dab 947f8048 a1c721d3 f02293fa 2a3f1c18 0ff58a0b
     67  6a502183 563dda07 5b29f412 084666c3 fa9053ff d3bf554a aff09384 fd80b72d 0bc8bb16 44b21a63 121671d9 67ff7ec2 947f8048 41d501d1 f00293fa aa271c1c cf63920f
     68  6e4a51a6 d032c202 bb01f412 506666c3 fa9053fb f9ea5d4e 87f09384 bf9f76cd 0b823d5a 669449e1 5b5eb99e 5e3992f4 947f8048 a1c721d3 7026b3fa 6c2f2c19 b17fc1e8
     69  6cd7e862 bdffc202 9ff37412 575266c3 fa9053fb f1ef5d4e 8bf0138c b7dfd69f 41909aec 07716471 4dce7e13 59825e7b 946b8048 61d161d3 f02293fa 2a271418 b17ff9e9
     70  69afbe8b 9cc2d806 098db413 247166c3 fad053ff 5bfb554a 8ff49384 b991b6cd c1cadd76 0e8d5880 968577c8 cd180c63 947b8048 81d701d1 7006b3fa aa2f0c18 71e199ed
     71  6a650eea 96ffd806 3b87f412 4a7266c3 fad053ff b3bf554a 07f19204 558eb7e5 6f4cd9f0 6b47603b d8270b9e fe08047c 947b8048 81c701d1 f00293fa aa3f3c19 717df9e8
     72  6a2fceb3 0ec2d806 418db413 3a7166c3 fad053ff 3bfb554a 0ff59204 db9077e5 4b095b2a eeb95980 ba99f5c5 e7e19ad7 947b8048 a1d301d1 7026b3fa ec270c19 317bf9e8
     73  6ba5be70 6104c202 a6c6b413 223666c3 fa9053fb 11ae5d4e aff59204 9b8d7665 c3081bb8 b7506672 6d2a8246 205eee67 947f8048 41d501d3 7006b3fa aa3f3418 b17391e9
     74  697cd92c b221c202 fbb83413 f12666c3 fa9053fb 19ab5d4e 0bf1120c 15de97f7 c1c2bc84 b6ee7f63 a5687868 abfa2643 947f8048 a1c721d3 f02293fa 6c2f241d cfefaa0e
     75  6a21460e 10fed806 f4823412 057166c3 fad053ff b3be554a 0bf5120c 91d397d7 4f90fa4e 4ab54c28 90bb77e8 3f017303 947b8048 a1d301d1 f02293fa aa3f041c 0f6d920f
     76  68724f2a 8f07d806 2986b412 527666c3 fad053ff bbbb554a 07f19204 558eb7e5 8f48f9f0 0be1789a f5d90507 5d8233f7 947f8048 a1c721d1 f02293fa 2a373419 71e981ec
     77  69a14610 104eda07 f4423412 053166c3 fa9053ff b3be554a 0bf5120c 91d397d7 4fc0fa4e 8aa14aa9 9eca6e6a 0a467c50 947b8048 a1c301d1 f02293fa 6c2f041d 0ff9e20b
     78  715dacba 16ffd806 7b83f412 be7266c3 fad053ff b3bf554a 87f59204 f18fb605 4d46ba10 db667638 9a4805f5 a2c7678e 947b8048 a1c301d1 f02293fa 2a2f3c19 4fe7e20f
     79  739b3c77 70b3c003 3d05f413 aa7166c3 fad053fb 19aa5d4e 8ff19204 fb8a7605 29c65a18 461340c3 e26db1c7 9905cd3f 947b8048 a1d701d3 f02293fa 6c3f0418 71e591ec
     80  7685787c 4423c202 05b77413 852666c3 fa9053fb 11af5d4e abf5120c 39de9657 87dafbac a1b21adb 96e77a8b 2c0b25e2 947f8048 41d501d3 7006b3fa aa270c18 31e7f9ec
     81  72cdc7dc b213c003 e9b1f413 db2566c3 fad053fb 19aa5d4e 03f59204 1bdfd7f5 29079488 92825aea bc7109df 33ce19cf 947f8048 81d711d3 f00293fa 2a3f1c19 31e3f9ec
     82  74d3c794 0214c003 09fff412 c32266c3 fad053fb 99ea5d4e 03f59204 b3ded7f5 c30b92e0 63874978 19d875ef e8797bdc 947b8048 81d711d3 f00293fa ec370419 4ff3920a
     83  760a55a3 97e2c003 b1e4b412 894566c3 fad053fb f1ee5d4e 83f09384 7dc096bd 619893c0 c41313e2 ee2c7be4 ad15732e 947f8048 81c711d3 7006b3fa aa2f0c18 f179f9e9
     84  73222643 786fc003 90137412 1f7266c3 fad053fb f1ef5d4e a3f0138c ddd0973f 85ccf922 df676412 30f35f04 a3600047 947b8048 81d701d3 f00293fa ec3f141c b1e7d9ec
     85  764a57a2 97f2c202 b1e4b412 894566c3 fa9053fb f1ee5d4e 83f09384 7dc096bd 61d893c0 c42315e3 204073e5 aaec0187 947f8048 81c711d3 7006b3fa 6c2f0418 f175f9e8
     86  7ea5d8aa b83fc202 6e137412 317666c3 fa9053fb 91ef5d4e 83f5120c 5bcfd5f7 214ef992 e10804d8 882762d4 be553096 947f8048 41d101d3 f00293fa 6c37341c cfefda0f
     87  7dd24614 39ffc202 dfc37413 033266c3 fa9053fb 71af5d4e abf4138c f3d3d73f 85819984 0d4722b3 ce3a12e3 357867c2 947b8048 81c301d3 f00293fa 2a272418 0f6db20e
     88  7ce1dd47 bd52c003 6ef4b413 fe6566c3 fad053fb 11ae5d4e aff59204 bf9e7665 ebc91bb0 514d23db b60585e4 7a45cb05 947f8048 81c721d3 f00293fa 6c27341d 31e3f9ed
     89  7e8fd7ca 102fc202 06037412 d16266c3 fa9053fb 91ef5d4e 0bf1120c b5ce97f7 41c1fa84 a3914ad9 7cfa1598 b91d7fd3 946b8048 41d161d3 7006b3fa 6c27241d b16fb9ed
     90  7eaad9ca b83fc202 2e0f7412 717266c3 fa9053fb 91ef5d4e 03f5120c fbd3d7f7 2942f9b2 d60e4740 1a1524fc 859e79df 947b8048 81c701d3 f00293fa ec2f3c1c f17581e8
     91  7ee5ee9c 864fda07 6b47f412 263266c3 fa9053ff b3bf554a 8ff19204 9f8a7605 25087b82 c08d0eeb 5304d96c 5fc5fefe 947b8048 81c701d1 7006b3fa aa27041d f17df9e8
     92  7b193708 ee43da07 ba417412 672166c3 fa9053ff dbba554a 83f4138c 75d1969f 4b06dc5c 436f7359 e1677189 876675a1 946b8048 41d161d1 f00293fa aa370c18 4fffaa0b
     93  78e2ae3c 964fda07 7b43f412 1e3266c3 fa9053ff b3bf554a 87f59204 918fb605 258dbb90 250112d3 65517ccd ddad6707 947b8048 a1c701d1 7026b3fa 6c273c18 4f6fa20e
     94  783c4e2b 6e93da07 4992b413 927666c3 fa9053ff 3bfb554a 87f19204 358ab5e5 47dcd910 e5f53971 ee2a09e7 c0796a05 947f8048 41d501d1 7006b3fa aa273c18 f17599e8
     95  7be7d7d0 ae50da07 a4263412 331266c3 fa9053ff d3be554a 83f0138c b1df96bf 030fbaf4 09b01838 2ba346f1 99a17e48 946b8048 41d161d1 7006b3fa aa271419 4f63b20f
     96  79ec0f0c 964fda07 3b4bf412 4a3666c3 fa9053ff b3bf554a 07f19204 558eb7e5 6f8cf9f0 6b577639 488b049d c0cb2f3f 947f8048 81c721d1 f00293fa 2a273c18 4fef820e
     97  7f00a63f 6c92da07 54963413 917566c3 fa9053ff 33fe554a 8bf1120c 35ca95f7 c3db9b1e c65074e2 7f7a44a8 751573c2 947f8048 41d501d1 7006b3fa ec3f1c1c 0ff5ea0a
     98  7ed9a824 4dffc202 67cb7413 8f3666c3 fa9053fb 71af5d4e abf0138c 77d0d71f 0188fb84 a1f02cd8 f0225e59 237012ea 947f8048 61d501d3 f02293fa ec370c19 f1e1f9ed
     99  7bfe15c3 91f7c003 bfdff412 914566c3 fad053fb f9ea5d4e 83f09384 7dc096bd 699893c0 c61753c2 48ac23a6 1a594bbe 947f8048 81c711d3 7006b3fa ec2f3418 0fe5fa0f
    100  7a6c0f0a 96ffd806 3b8bf412 4a7666c3 fad053ff b3bf554a 07f19204 558eb7e5 6f4cf9f0 6bc7783a 9acf0d9f fe2a2735 947f8048 81c721d1 f00293fa ec2f3c19 316ff9ec
    101  795b1904 7a02c202 43c33413 c13566c3 fa9053fb 19ab5d4e a3f5120c fbcbd677 8540f852 da5e6708 9ad268b7 989b1e7f 947f8048 61d101d3 f02293fa ec2f1c19 0f69fa0f
    102  7dae17c2 9207c202 bfdff412 914566c3 fa9053fb f9ea5d4e 83f09384 7dc096bd 69d893c0 c62755c3 d6b80ba7 a1977f87 947f8048 81c711d3 7006b3fa 2a271c18 0fe1da0e
    103  84dac774 0218c003 09fff412 c32666c3 fad053fb 99ea5d4e 03f59204 b3ded7f5 c30b92e0 63874978 57d07def 5b1d38a5 947f8048 81d711d3 f00293fa 2a2f0c19 4fff9a0b
    104  81ce4413 40afc003 60037413 837266c3 fad053fb 71af5d4e abf4138c 73d3d73f 45519b84 6d5d27b0 77e76af0 18c67ad3 947b8048 a1d701d3 f02293fa 6c3f0418 4f73820a
    105  85e75583 97dec003 b1e0b412 894166c3 fad053fb f1ee5d4e 83f09384 7dc096bd 619893c0 c41313e2 b02c7be4 f50c4487 947b8048 81c711d3 7006b3fa 6c2f0c18 4ff3ba0a
    106  84f6defe 1c48c202 650ff412 c67666c3 fa9053fb 99ea5d4e a7f59204 f989b685 edc1f9e6 b77a74f1 e57c6f2b 8f9f0103 947f8048 41d101d3 f00293fa 6c272c18 31f399e9
    107  85b38617 704eda07 94703413 c55266c3 fa9053ff 33fe554a 8bf5120c f1de95d7 23ce9766 e9861918 2cdb6932 98ea7968 946b8048 41c161d1 7006b3fa ec3f3c18 b1f781e9
    108  833cae03 5e92da07 498db413 867166c3 fa9053ff 3bfb554a 87f59204 318cb605 89c2f8f8 242302c2 98cf3e0c b3e34a44 947b8048 81c301d1 f00293fa ec2f3418 71fd89e8
    109  86ba5efb 668dda07 6390f413 c87166c3 fa9053ff 53ff554a 87f09384 1f8076cd 6f853b6c 001715c8 65e6c62a 092ea1d0 946b8048 61d161d1 7026b3fa ec3f3c18 8ff5ca0a
    110  806ce19b fc87da07 ad457412 486566c3 fa9053ff bbba554a 87f1120c 7d9ab5e7 21899f7a afb05932 b50460ef 3306346e 947f8048 41d501d1 f00293fa 6c3f3419 0f61820f
    111  8ccac514 1a14c003 01b3f413 632266c3 fad053fb 19aa5d4e 8bf59204 31da95d5 4985d282 718b1ad8 7687580c 0fb902a4 947b8048 a1d311d3 7026b3fa aa272c18 0f69ea0e
    112  8e8677fc 6423c202 25b77413 a52666c3 fa9053fb 11af5d4e abf5120c 19de9657 8fd9fb2c 07cf7af3 b99a1960 527f3782 947f8048 61d501d3 f02293fa 2a2f041d 4f7b8a0b
    113  8dec17b0 ae54da07 ba277412 3b1266c3 fa9053ff dbba554a 83f0138c b1df96bf 030bbaf4 11b11858 bab04f61 28637e49 946b8048 41d161d1 7006b3fa 2a371c19 f1f5b9e8
    114  89aebf0b 44c2d806 d18db413 447166c3 fad053ff 5bfb554a a7f49384 b390772d cf483c64 abe17c39 fec0f36b 333ff471 947b8048 81d301d1 7006b3fa ec2f2418 8fed8a0f
    115  8b2fb063 4e8dda07 b392f413 066566c3 fa9053ff 33ff554a a7f59204 b19fb685 01c6db70 1e9749a1 2d55205d c9647b05 947f8048 a1c721d1 f02293fa 6c273418 4fef920e
    116  8e1fce27 9101c202 dea83413 d05666c3 fa9053fb 19ab5d4e 07f1120c 359eb7e7 8581d300 1a354488 afbb726c e1547807 946f8048 61d571d3 7026b3fa aa370c18 31ffc9e8
    117  8e8b55eb 9661c003 44003412 216666c3 fad053fb 99eb5d4e a3f5120c 9bdad677 8115d94a 17815df2 4ad30aa6 03543a8f 947f8048 a1d721d3 f02293fa ec2f1c18 0ff1aa0a
    118  964659a2 97f2c202 b1e4b412 094566c3 fa9053fb f1ee5d4e 83f09384 fdc096bd 61dc91c0 443c1543 596b57f6 fa5f40b4 947f8048 a1c711d3 7026b3fa ec3f2c19 31ebf9ed
    119  913a6ee3 7e92da07 698db413 ce7166c3 fa9053ff 3bfb554a a7f59204 f18bb685 41c9ba10 7c091282 e52f01ac ad0f606f 947b8048 a1c701d1 f02293fa ec3f3418 b167a9ed
    120  9681767c 4423c202 85b77413 052666c3 fa9053fb 11af5d4e abf5120c b9de9657 27d2f9ac 99a1191b 62dd7058 8b280820 947f8048 41d101d3 7006b3fa aa2f041d 317ff9e9
    121  923ed133 ee92da07 018db413 5a7166c3 fa9053ff 3bfb554a 8ff59204 5b8c75e5 8b4e578a 67cd7bf1 19adbefe 471ce6d4 947b8048 a1c301d1 f02293fa aa3f3419 cf7b820b
    122  9692e0a0 ad00c202 6ea2b413 e61266c3 fa9053fb 11ae5d4e a7f59204 d19db685 8f8299e6 cc9d0983 dcee3d59 9162547a 946b8048 41c161d3 f00293fa ec270c1c 7171e1e8
    123  917df407 6ac2d806 64943413 8f7566c3 fad053ff 53fe554a 8bf0138c 5fd0d69f 034bdbbe 9a25470a 45427aaa 62c04ca3 947f8048 81d721d1 7006b3fa aa2f0c18 7165a9ec
    124  94cfc594 8214c003 09fff412 432266c3 fad053fb 99ea5d4e 03f59204 33ded7f5 230794e0 2b834b18 28d76076 5b13788e 947b8048 81d711d3 f00293fa aa372c18 8f65ca0e
    125  9a400f0b 7693da07 1b97f413 ca7666c3 fa9053ff 33ff554a 07f19204 558eb7e5 6fccf9f0 eb677438 18eb059d 4f170217 947f8048 81c721d1 f00293fa aa3f3c19 71f1d1e8
    126  9edda624 4dffc202 e7cb7413 0f3666c3 fa9053fb 71af5d4e abf0138c f7d0d71f 4188f984 61ca2d58 7c0d0229 f3e5390a 947f8048 41d101d3 f00293fa 6c2f3419 0fede20f
    127  9b91c7db b9bec202 3bd0b412 7b3566c3 fa9053fb 91ee5d4e 03f59204 f3c3d7f5 c71db148 6f526193 ac573b2f 7a0525e7 946f8048 61c571d3 7026b3fa 2a2f2c18 0fedba0e
    128  9f3cee9b 7693da07 4192b413 a67266c3 fa9053ff 3bfb554a 8ff19204 1f8a7605 a5447982 388e0f8a a2109906 f34e81d5 947b8048 a1c701d1 7026b3fa 2a273c18 4fffb20b
    129  9fbd7f0b 6c96da07 718db413 cc7566c3 fa9053ff 5bfb554a 87f49384 139176ad 2f8c7acc 882503aa 1b13c722 59adf820 947f8048 61d501d1 f02293fa 6c2f3c18 717189e9
    130  9e5b4fc7 a952c003 12f5f413 506266c3 fad053fb 79aa5d4e 8ff09384 bd9fb6ad e981fd04 f99d0f18 08894c69 3fa743db 947b8048 81c701d3 f00293fa 6c3f3419 0f61fa0e
    131  999906f0 0e43da07 92457412 6d2166c3 fa9053ff bbba554a a3f1120c 5fcbd657 4d4dbad4 f73046f1 f0d860c8 a2ef2398 946b8048 41d161d1 7006b3fa aa272c1d b16fd9ed
    132  179a3dcf b0b0c003 6706b413 f27266c3 fad053fb 11ae5d4e aff19204 db8a7685 2dc75a78 d41500c3 c0ddbc9e fd6faf06 947b8048 a1d701d3 7026b3fa ec2f0c19 f1f1f9e8
    133  16ff2727 8ec4d806 ea937413 597266c3 fad053ff 3bfa554a abf1120c 75ca9677 078d9a3e 424d73eb c01a7028 16290578 947b8048 81d301d1 f00293fa aa370c1d 7165e9ec
    134  16c5a060 b524c202 44b3f413 be2666c3 fa9053fb 19aa5d4e 87f59204 d99ab605 ed81da0e 908d09eb 9b237473 79de3eb9 947f8048 a1c721d3 7026b3fa aa370418 f171d1e8
    135  10c9851c 9a13c003 81b1f413 632166c3 fad053fb 19aa5d4e 0bf59204 91df97d5 458a926a 80b50ac8 841b69f4 453c1dd4 947b8048 81d711d3 7006b3fa 6c2f0418 4f7b820b
    136  16f3a53f 8cc2d806 14963413 f16566c3 fad053ff 33fe554a 0bf1120c 35de97f7 c386bcfe 8dc33db2 e60f4349 e2582f20 947f8048 81c721d1 7006b3fa 2a272c1d f1edc1ed
    137  14f53920 9613da07 1857f413 ef2666c3 fa9053ff 33ff554a 0bf19204 35ce97f5 63c69474 80ed3fca 6cac74a0 ac8248d1 946f8048 61d171d1 f02293fa 6c3f0c18 7169b1ed
    138  170939d3 cfbec202 a1d0b412 f53166c3 fa9053fb f1ee5d4e 8bf09384 17c0d69d ed54f562 51a10a7a 798a7dde 0b0953ad 946b8048 61c171d3 7026b3fa 6c271418 4fe3820e
    139  15dffeaa b6fdd806 a380f412 3c7166c3 fad053ff d3bf554a 87f49384 9b9576ad c10b3ccc 9ad069aa 2a1a83c2 df139591 947b8048 a1d301d1 f02293fa 6c373418 f1f5e9e8
    140  12350d0b 96c3d806 1b97f413 ea6666c3 fad053ff 33ff554a 07f19204 359eb7e5 4797faf0 dd2b14b1 387c4406 964948dc 947f8048 81d721d1 7006b3fa 6c373419 0f69e20f
    141  116e6ee2 df02d806 8981b412 4e7166c3 fad053ff bbbb554a a7f59204 718bb685 2151b810 647234c0 5b5a05c4 d0174b15 947b8048 a1d301d1 7026b3fa 2a2f3418 8f6d820e
    142  129d1f80 7504c202 bca7f413 2e1266c3 fa9053fb 19aa5d4e 8ff19204 77997605 0f105870 e7335752 914d8836 b336ce9c 946b8048 61d161d3 7026b3fa ec271c18 cff7ba0b
    143  1703a73f 8c92da07 14963413 f16566c3 fa9053ff 33fe554a 0bf1120c 35de97f7 c3c6bcfe 8dd33fb3 38232149 0e1a7d98 947f8048 81c721d1 7006b3fa 6c27041c f171a9e9
    144  16e59c5f b554c003 44f3f413 be6666c3 fad053fb 19aa5d4e 87f59204 d99ab605 ed41da0e 909d0fe8 ab377d70 9d9f779b 947f8048 a1c721d3 7026b3fa 2a370c18 b16789ed
    145  12f9217e b504c202 5cf3f412 2e5266c3 fa9053fb 99ea5d4e 8ff19204 77997605 8f505870 073f5753 27698897 0b20da4d 946b8048 61d161d3 7026b3fa 2a372418 4ffff20b
    146  104e4d4a 0ef3d806 a986b412 f26266c3 fad053ff bbbb554a 87f19204 d59ab5e5 ef5dda10 9879208b 0668001f cbb44b7c 947b8048 a1d301d1 f02293fa aa3f3c18 b173b1e8
    147  103a514b 8e93da07 8992b413 726266c3 fa9053ff 3bfb554a 07f19204 b59eb7e5 87c3dcf0 850600d1 279b0515 90af7fdc 947b8048 a1c301d1 7026b3fa 2a371418 b16f89ed
    148  a77eb947 4e93da07 da8d7413 577166c3 fa9053ff 5bfa554a a3f4138c 9dc0971f 6101da94 8176217b ba900199 17a11672 946b8048 61d161d1 7026b3fa aa3f141c f1e1f9ec
    149  a340b003 5e92da07 c98db413 067166c3 fa9053ff 3bfb554a 87f59204 b18cb605 49c6faf8 94482262 0ca574fd 7db65305 947b8048 a1c301d1 7026b3fa 6c3f3419 b16bc9ec
    150  a4d6c574 8218c003 09fff412 432666c3 fad053fb 99ea5d4e 03f59204 33ded7f5 230794e0 2b834b18 a8cf4876 fdcf4927 947f8048 81d711d3 f00293fa 2a2f1418 317f89e8
    151  a6be9f7b 5c96da07 698db413 e07566c3 fa9053ff 5bfb554a aff49384 1590b74d 4506fa1e 741c0160 77487548 273002b3 947f8048 61d501d1 7026b3fa 6c273418 316fc1ec
    152  a1188de7 b6ffc202 f0a77413 c85266c3 fa9053fb 11af5d4e 07f1120c 359eb7e7 6581d300 0a184308 85a95535 6ee10b17 946b8048 41d171d3 7006b3fa ec373419 3163c1ed
    153  a5f7c597 7ec8d806 6a8f7413 ed7666c3 fad053ff 3bfa554a abf5120c d1c99657 a38598be 5348715b 93d16dc8 c2f14d22 947f8048 81c721d1 7006b3fa ec2f041d f1f181e9
    154  a72bb727 b242da07 a4243412 b74566c3 fa9053ff d3be554a 83f4138c 1dc5969f 610cbd5c 5e824d02 3c5603d3 d9c14f51 947f8048 61d501d1 7026b3fa 6c3f0c19 f1fda9e9
    155  afa7fc93 76bdd806 7b8df413 a47266c3 fad053ff 53ff554a 87f49384 339476ad 434d3b24 9cf53801 a9f19298 c149fec8 947b8048 81d301d1 f00293fa aa3f3c1d f1f5f1e8
    156  aa46100b 7693da07 db97f413 0a7666c3 fa9053ff 33ff554a 87f19204 b58ab5e5 e7d8db10 65fd3d51 111f5c94 5d4970d5 947f8048 41d501d1 7006b3fa 6c370c1d 0f61ba0f
    157  ada719e2 9203c202 bfdff412 114166c3 fa9053fb f9ea5d4e 83f09384 fdc096bd 69d891c0 563f5543 26e7704c f0ce201f 947b8048 a1c311d3 7026b3fa aa3f041d 717589e9
    158  a9eebf0a 6502d806 7181b412 447166c3 fad053ff dbbb554a a7f49384 b390772d cf083c64 2bf17a38 4ca0f86a e1a18552 947b8048 81d301d1 7006b3fa 2a2f2c18 71f591e8
    159  ad7f55ec 5a25c202 a3b43413 212666c3 fa9053fb 19ab5d4e a3f5120c 9bdad677 8145d94a d7ad5f73 55180f6c 16c7454c 947f8048 a1c721d3 f02293fa aa371c1d cf7ba20a
    160  a87fd62f 6e94da07 7a937413 937666c3 fa9053ff 5bfa554a 83f0138c 59cf96bf 4104bc14 37e46b70 01e943e0 546c4e53 947f8048 81c721d1 7006b3fa 6c3f3418 f1e199ed
    161  ad9f55eb 5a55c003 a3f43413 216666c3 fad053fb 19ab5d4e a3f5120c 9bdad677 8115d94a 17c57df2 5b9e1087 94477af7 947f8048 a1d721d3 7026b3fa ec271c19 f1edb1ed
    162  b34bd70c 2030c003 81c2b413 c13266c3 fad053fb 71ae5d4e 8bf49384 3bd4d6bd 8b41b54a 989e0baa bd6d0cb6 2bd473a7 947b8048 a1d711d3 7026b3fa 2a2f1c18 4f7fca0a
    163  b11f8e07 b6ffc202 f0ab7413 c85666c3 fa9053fb 11af5d4e 07f1120c 359eb7e7 6581d300 0a184308 85993534 edf50897 946f8048 41d171d3 7006b3fa ec271418 31e3b9ec
    164  b0bf2163 6c93da07 f192b413 687266c3 fa9053ff 5bfb554a a7f09384 9f80774d e3833ccc 0e1c5720 9fa2ccf3 6cb2ffd3 946b8048 61d161d1 f02293fa ec370419 716999ec
    165  b6e93854 4ffec202 8194b413 f50166c3 fa9053fb 71ae5d4e 8bf09384 17c0d69d 8d5a9562 f04033e9 d90f59b7 3a127ea6 947b8048 81c711d3 7006b3fa ec2f2c18 71ed81ed
    166  b3822e96 8a44c202 8516b412 ac7666c3 fa9053fb f1ee5d4e aff09384 5990b72d ef03990c eb68779b 4d1a50a9 863b7e10 947f8048 41d101d3 f00293fa 2a2f0418 317389e8
    167  b7eaff0f 9078c003 5d0ff412 4a7666c3 fad053fb 99ea5d4e aff59204 73897665 0d007838 48fa3f09 864aed6d c9f5d7e7 947f8048 81d721d3 f00293fa aa2f1418 0fe9920e
    168  b77e2e96 9042c202 9311f412 ac7666c3 fa9053fb f9ea5d4e aff09384 5990b72d ef07990c d36b777b 7a2c018a 13f54cd1 947f8048 41d501d3 f00293fa 6c3f3419 4f77fa0a
    169  bb812e16 6a44c202 8516b412 8c7666c3 fa9053fb f1ee5d4e aff09384 7990b72d 0704998c 8d901893 b1612eb3 5a5a01b2 947f8048 61d101d3 7026b3fa ec270418 316b91ec
    170  ba440f0b 76c3d806 9b97f413 4a7666c3 fad053ff 33ff554a 07f19204 d58eb7e5 af98fbf0 db487319 d19f3fed afe43a44 947f8048 a1d721d1 f02293fa 2a373c18 b1e381ec
    171  bf40f09b 7693da07 c192b413 267266c3 fa9053ff 3bfb554a 8ff19204 9f8a7605 45487b82 30a20e6a 27109e5e b0b7e9bc 947b8048 a1c701d1 7026b3fa 2a370418 f1f5d9e8
    172  b91fef78 4902c202 f2c1f413 643666c3 fa9053fb 79aa5d4e aff49384 918fb74d e1c19d0c 6e854880 a6485d50 07000751 947f8048 41d101d3 7006b3fa 2a372c18 cf6bfa0f
    173  be6c97ef a680da07 048e3413 2b6266c3 fa9053ff 53fe554a 8bf4138c b3d4d6bf 0587bb26 e6ba4d40 426674cb d1c60b99 946b8048 61d161d1 7026b3fa 6c270419 4fe3c20e
    174  bfcec65c 182ec003 d410b412 9b3566c3 fad053fb 91ee5d4e 0bf59204 d9d397d5 c783d12a 61fa2cfa 77337577 3af878a7 947f8048 a1d711d3 f02293fa aa370419 f175e1e8
    175  c25f4dc7 5750c003 7cf6b413 d06266c3 fad053fb 71ae5d4e 8ff09384 3d9fb6ad 6995fb04 41b40df8 336d5818 6d00121a 947b8048 a1d301d3 f02293fa aa2f3c18 cf6fc20e
    176  c2f0ae04 7e52da07 6941b412 063166c3 fa9053ff bbbb554a 87f59204 b18cb605 4986faf8 94340463 c9b67f5e 397a03c5 947b8048 a1c301d1 f02293fa aa272c19 8fe9920e
    177  c1afbe8b 64c2d806 f18db413 247166c3 fad053ff 5bfb554a a7f49384 d390772d 074d3ae4 fe145721 f135824b 6b9dfc39 947b8048 a1d701d1 f02293fa 2a3f3c18 0ffd9a0b
    178  c34ed6ec 2034c003 81c6b413 c13666c3 fad053fb 71ae5d4e 8bf49384 3bd4d6bd 8b41b54a 989e0baa 3d7524b7 8dec5f47 947f8048 a1d711d3 7026b3fa aa373419 f1f591e9
    179  c6c2a17b 5c96da07 e98db413 607566c3 fa9053ff 5bfb554a aff49384 9590b74d a50afc1e 1c040380 dc4b1051 52547be8 947f8048 61d501d1 7026b3fa ec2f0c19 71fdc1e8
    180  c2693453 502ec003 81d4b413 f54166c3 fad053fb 71ae5d4e 8bf09384 17c0d69d 8d1a9562 702c15e8 f85e6457 77143cb4 947b8048 81c711d3 f00293fa 6c273c19 f17df9e8
    181  c6f13453 d7eec003 89dcb412 f54166c3 fad053fb f1ee5d4e a3f49384 f9c4971d 4d9df0e8 cbcf7c1b 41ee5304 908a45ae 947b8048 81c711d3 f00293fa ec37041d 0f69e20f
    182  c50f4914 5a1fc202 5fb37413 e32266c3 fa9053fb 71af5d4e abf4138c 13d3d73f cd88fc04 7afc6e28 3a586c3a 8569701b 946b8048 61d161d3 7026b3fa ec2f1418 8f6dba0e
    183  cfabfe93 76bdd806 fb8df413 247266c3 fad053ff 53ff554a 87f49384 b39476ad c34d3d24 0cf93c81 69d3ea13 2b80b11b 947b8048 a1d701d1 f02293fa 2a271418 cff3f20b
    184  ca0e006e 6920c202 2efeb412 0a6266c3 fa9053fb 91ee5d4e aff59204 b39d7665 e5475bd8 00e32849 aad2ed66 473dec56 947b8048 81c701d3 f00293fa 2a2f1c19 cfe3820e
    185  cfc7c63c 182ec003 d40cb412 9b3166c3 fad053fb 91ee5d4e 0bf59204 d9d397d5 c783d12a 61fa2cfa 772b7d77 3946238d 947b8048 a1d711d3 f02293fa aa2f0c19 0fe9820e
    186  cd80174c 3823c202 15b77413 792666c3 fa9053fb 11af5d4e 83f5120c 13dfd5f7 af4edaf2 29643019 edd90e85 363f1965 947f8048 81c721d3 7006b3fa ec2f2c1c 316f99ed
    187  ca2bccb3 8ec2d806 c18db413 ba7166c3 fad053ff 3bfb554a 0ff59204 5b9077e5 4b05592a ce985920 c386e4e5 2db5f527 947b8048 81d301d1 7006b3fa ec273c19 7165e1ec
    188  cadfae64 6e41da07 5346f412 062566c3 fa9053ff b3bf554a a7f59204 b19fb685 0186db70 9e874ba0 7b552a5d 73fb74a6 947f8048 a1c721d1 f02293fa 2a373c19 b17bf9e8
    189  d717a73e 8ceed806 348a3412 716566c3 fad053ff b3be554a 0bf1120c 35de97f7 c396bcfe cdff3e32 a2265448 b1630d3a 947f8048 81d721d1 7006b3fa 2a273c1c 0fedc20f
    190  d01d455b b86dc003 90127412 db7566c3 fad053fb f1ef5d4e a3f4138c 11d4971f 67ccbc0a 6d3806b2 3ad7487f fdd92f77 947f8048 81d721d3 f00293fa 2a272419 cf63c20e
    191  d6ea3433 d7dec003 89e0b412 f54566c3 fad053fb f1ee5d4e a3f49384 f9c4971d 4d9df0e8 cbcf7c1b ffe65b04 863544df 947f8048 81c711d3 f00293fa aa2f0c1d 3177e9e8
    192  d4aba1a3 4c83da07 c98eb413 586266c3 fa9053ff 5bfb554a aff49384 9d8fb74d cb12dcf6 419f0afb 3f7842d8 97850122 946b8048 41d161d1 f00293fa 2a37141d f1e5e1ec
    193  d46a0dd2 0702d806 a185b412 f27166c3 fad053ff bbbb554a 8ff19204 d38b7605 2bd25a6a 510b115b e0a5e5ad c23ea114 947b8048 a1d301d1 7026b3fa aa2f041c 7175f9e8
    194  d74a3632 d7eec202 89e0b412 f54566c3 fa9053fb f1ee5d4e a3f49384 f9c4971d 4dddf0e8 cbdf7e1a 100270ff 6a564454 947f8048 81c711d3 f00293fa aa3f2419 cfff8a0b
    195  d1f1468f 788eda07 5c923413 856166c3 fa9053ff 33fe554a 83f1120c 37cad5d7 c357bb1c f6b75943 08ed3793 650b65f8 946b8048 41d161d1 f00293fa aa2f0418 0f61ba0e
    196  de4ad5cb b8afc003 0e037413 f17266c3 fad053fb 11af5d4e 03f5120c fbd3d7f7 a912f9b2 366266c1 159f387d a5173197 947b8048 81d701d3 7006b3fa 6c37241c 7169f9ed
    197  d8ffb53f 166fd806 c047f412 7f2266c3 fad053ff b3bf554a 83f19204 3fdad5d5 e506b272 14552041 b129314e aa093c37 947b8048 a1d311d1 f02293fa ec272419 b1e3e1ec
    198  dbf91798 563eda07 5c403412 432166c3 fa9053ff d3be554a abf4138c b3d4d73f 2189ba86 baf66ca8 06630db0 9eb47fd9 946b8048 61d161d1 7026b3fa 6c37341c 4f77fa0b
    199  dde91910 3e17da07 2e2eb413 8b1666c3 fa9053ff 3bfb554a a3f59204 33dad675 0f47f39a 58b31fa8 c9260cdd 314b0054 946f8048 41d571d1 7006b3fa 2a372419 8f69fa0e
    200  dc591797 767eda07 3c8c3413 c36166c3 fa9053ff 53fe554a abf4138c 33d4d73f c185bc86 829e4e48 2da27c08 61ff0159 946b8048 61d161d1 f02293fa 2a270c1c b17389e9
    201  d92d3840 9a50da07 8c423412 9f3266c3 fa9053ff d3be554a 83f4138c 35d4969f 6701bd34 bad47d28 b60c20ca 4d713300 947b8048 a1c701d1 7026b3fa 6c270c18 31ebf9ec
    202  dbead970 560fda07 3833f413 a31666c3 fa9053ff 33ff554a a3f59204 13ded675 074bf33a 77b55f70 133c7d2c 11a37994 946f8048 41d571d1 7006b3fa 6c3f0c18 f1e999ed
    203  deca87b4 ba30c003 13c2b413 fb3266c3 fad053fb 11ae5d4e 0bf59204 f9d297d5 4b8191a2 43fa7b7a 8cdd760d 07f77abf 947b8048 a1d711d3 f02293fa aa3f0c1d 0f6d920f
    204  e3996faf b73dc202 90c27413 fc7166c3 fa9053fb 11af5d4e 87f5120c 9180b607 4f5af3a8 4b9e4fb8 040027e7 0c251197 946b8048 61c171d3 f02293fa 2a3f1419 4fe3aa0e
    205  e77a879b a1e3c202 69bdf412 432166c3 fa9053fb 99ea5d4e a3f59204 7bcad675 c91cb240 147d3041 137d0ffe 16344e0d 946b8048 41c171d3 f00293fa 2a3f0419 7171d1e8
    206  e6ed3653 d7eec003 89dcb412 754166c3 fad053fb f1ee5d4e a3f49384 79c4971d 8d9df2e8 6bf17c9b ebde042f 47992fcf 947b8048 a1c311d3 f02293fa 2a273418 31e7f1ed
    207  e65e60fc c64dda07 8344f412 c83166c3 fa9053ff d3bf554a 87f09384 1f8076cd ef453b6c 208319cb 5be6c349 f3f8c912 946b8048 61d161d1 7026b3fa aa372c18 cff3da0b
    208  e23b4fc8 5720c202 fcb6b413 502266c3 fa9053fb 71ae5d4e 8ff09384 bd9fb6ad 09c1fd04 79ee2f99 b0147991 5ef520d8 947b8048 a1c301d3 7026b3fa 6c272c18 f16181ed
    209  e46ce703 11c4c202 d3b6b412 071666c3 fa9053fb 91ee5d4e 03f19204 77ddd7d5 ef4293e0 747e27c1 392749a6 15ce79ae 946f8048 41d171d3 f00293fa 2a2f1419 b1e7c9ec
    210  e166099a 5a1dc202 7ffe7412 436166c3 fa9053fb f1ef5d4e abf4138c b3d4d73f 2189ba8c 1cf53ca0 a8e8002b 71f03d3b 946b8048 61d161d3 7026b3fa ec372c19 b173f1e9
    211  eb9e9f86 2cfec202 4eecb412 a65166c3 fa9053fb 91ee5d4e a7f59204 119eb685 83d4d8ee 96ef7bc2 1e6908aa fbb4758a 946b8048 61d161d3 7026b3fa 6c3f3c18 0f7dba0a
    212  eccec714 9a14c003 81b3f413 e32266c3 fad053fb 19aa5d4e 8bf59204 b1da95d5 e98dd082 09901b18 a4aa6605 9a351057 947b8048 a1d711d3 7026b3fa ec3f3c19 b1e7a9ec
    213  e9cb01d6 a833c202 6501f412 526166c3 fa9053fb 99ea5d4e a7f19204 7d9bb665 c7c6d8ce aad07c0a bf1a0190 0cf95e78 947b8048 81c701d3 f00293fa 6c27341c 8f7d820b
    214  eb2af63f f244da07 a4263412 f74666c3 fa9053ff d3be554a 83f4138c ddc4969f ad009a54 25990d71 5c8e69e8 e2f64439 947f8048 81c721d1 7006b3fa ec27341d 316bf1ed
    215  efdbfc92 b6fdd806 9b81f412 a47266c3 fad053ff d3bf554a 87f49384 339476ad c30d3b24 7ce13800 71ab83b3 fdfbfef8 947b8048 81d301d1 f00293fa 2a3f3419 4fe79a0f
    216  ede618f0 3e13da07 2e2eb413 8b1266c3 fa9053ff 3bfb554a a3f59204 33dad675 0f43f39a 68ae1f88 522b34dc 44855054 946b8048 41d171d1 7006b3fa 6c3f0c18 0f79c20b
    217  eb42a188 6cfec202 2ea0b413 a61166c3 fa9053fb 11ae5d4e a7f59204 119eb685 0384d8ee b6ff7b43 22380ccb d1fb62a8 946b8048 61c161d3 7026b3fa ec3f3c18 71f981e8
    218  195ac6db b1c7c202 29adf412 7b1566c3 fa9053fb 99ea5d4e 03f59204 fbdfd7f5 c14cf208 2df73e90 7520514e 31731085 946f8048 61d571d3 7026b3fa 6c2f0c18 316ff1ed
    219  1c334972 c847c202 960e3412 637666c3 fa9053fb f9eb5d4e abf4138c 93cfd73f 65839ae4 da0b458b c9a11e90 2a471ab3 947f8048 41d101d3 7006b3fa aa3f2c1d b1ff89e8
    220  1f6d7f0c cc52da07 9141b412 4c3566c3 fa9053ff dbbb554a 87f49384 939176ad 8f447ccc 70820c69 6d25c04a 9971c810 947f8048 61d101d1 f02293fa 2a3f3419 b1e3c1ed
    221  1eecf09c f653da07 6146b412 a63266c3 fa9053ff bbbb554a 8ff19204 1f8a7605 25047982 18a20f8b 6a16842c b9ed89a7 947b8048 a1c701d1 7026b3fa aa372c1d 4f7bb20b
    222  1a5126c2 7623c202 9dfe3412 9f6266c3 fa9053fb f9eb5d4e a3f4138c 55df971f ad02fb52 16466641 cb7a17de ad446f4c 947b8048 a1c301d3 f02293fa ec27041d 8f69ea0f
    223  1fea9174 f652da07 a141b412 e23566c3 fa9053ff bbbb554a 8ff59204 d38c75e5 ed18196a 947c3542 ef448457 d73c9dd6 947f8048 61d101d1 7026b3fa aa3f3c19 f1edf9ed
    224  f469e723 11c0c202 d3b2b412 071266c3 fa9053fb 91ee5d4e 03f19204 77ddd7d5 ef4293e0 747e27c1 392751a5 d5ac7fac 946b8048 41d171d3 f00293fa 2a2f1c18 71fdb9e9
    225  f021475b b86dc003 90127412 5b7566c3 fad053fb f1ef5d4e a3f4138c 91d4971f 47d0ba0a 853602d2 bde27db6 f0d53fe5 947f8048 81d721d3 f00293fa 6c2f1c18 317bf1e9
    226  f6af2928 ee54da07 8a477412 d93266c3 fa9053ff bbba554a abf1120c f5ca9677 a7c5983e 5a6e73aa ea1c6b3b 57745453 947b8048 81c701d1 f00293fa ec370419 8ffdca0b
    227  f02b55ef f644da07 7c263412 e34666c3 fa9053ff d3be554a abf4138c 13c3d73f 4d8f9c7e f6f06843 54016f53 9ccd2d90 947f8048 41d501d1 7006b3fa 2a2f0418 b1e7e1ed
    228  f7413852 cfeec202 a1e0b412 754166c3 fa9053fb f1ee5d4e 8bf09384 97c0d69d 0d5e9362 f00f1049 759a7687 0f480237 947b8048 a1c711d3 f02293fa aa2f1418 316399ed
    229  f2f51f7e 3504c202 5cf3f412 ae5266c3 fa9053fb 99ea5d4e 8ff19204 f7997605 8f4c5a70 27345773 2663c167 4ceabf56 946b8048 41d161d3 7006b3fa 6c2f1c18 cf7b820a
    230  f72b31d7 f505c202 36a43413 3c5666c3 fa9053fb 19ab5d4e 0ff5120c bb9f77e7 af0a1512 b11a055a 85ea92a4 397ea8fd 946f8048 61d571d3 f02293fa ec3f2c1c 31fff1e8
    231  fc9dddc7 bcb2c003 0f04b413 fe7566c3 fad053fb 11ae5d4e 0ff59204 f79377e5 4dd31bd8 b02113c9 85d7991c 561ee0ed 947f8048 a1d721d3 f02293fa 2a2f341d 0fe9820e
    232  fcd3c6f4 9a14c003 81b3f413 e32666c3 fad053fb 19aa5d4e 8bf59204 b1da95d5 e98dd082 09901b18 24a25605 d9f90214 947f8048 a1d711d3 7026b3fa 6c372c19 f1f9a1e8
    233  fb994710 7e43da07 2a417412 652166c3 fa9053ff bbba554a 0bf5120c 31df97d7 cfc6fcee 8f944fb1 fd787b73 b2951d10 947b8048 81c701d1 f00293fa 2a3f0418 4f73fa0a
    234  fc09470e 7ef3d806 2a817412 656166c3 fad053ff bbba554a 0bf5120c 31df97d7 cf86fcee 8f844db0 4f147d72 39312eca 947b8048 81c701d1 f00293fa 6c2f0418 71e999ec
    235  f99d08f0 0e43da07 92457412 ed2166c3 fa9053ff bbba554a a3f1120c dfcbd657 6d51b8d4 3f324611 3bff2d50 29da7428 946b8048 41d161d1 7006b3fa aa3f3c1d 3167c9ed
    236  ff65d6ac b803c202 cdc77413 313666c3 fa9053fb 11af5d4e 83f5120c 5bcfd5f7 a14ef992 414826d8 6d9c72d5 d16d6cc7 947f8048 41d101d3 7006b3fa aa372c1d 0fe9aa0e
    237  272e39b3 cfc2c202 a1d4b412 f53566c3 fa9053fb f1ee5d4e 8bf09384 17c0d69d ed58f562 819e0a5a aec2534f 408e1b0f 946f8048 61c571d3 7026b3fa 2a3f2c19 31f3c1e8
    238  2281e123 e498da07 85477412 507666c3 fa9053ff bbba554a aff1120c 7f8a7687 49027fec 88a81c08 a5eef8f8 af74fc49 947f8048 41d501d1 f00293fa aa372c18 4ff7820a
    239  224b4fc7 b660c003 9d02b412 506266c3 fad053fb f1ee5d4e 8ff09384 bd9fb6ad 09c1fd04 79aa0f99 a0617371 548c13a2 947b8048 a1c301d3 f02293fa 6c271c18 71f1b1e8
    240  252b7848 ee53da07 7a417412 9f3566c3 fa9053ff dbba554a a3f4138c 55d0971f 4b03baf4 a3a659d8 8b017632 1bab4d8b 947f8048 41d101d1 7006b3fa 6c270418 cfeb9a0f
    241  26daa75f 8cbed806 94923413 716166c3 fad053ff 33fe554a 0bf1120c b5de97f7 03869afe 8d793433 ca3f79f8 078b0799 947b8048 a1c301d1 7026b3fa aa3f0c1d 317bf9e9
    242  20b72827 f44eda07 04703413 595266c3 fa9053ff 33fe554a a3f5120c 5bddd677 ad42da3c 59d73f18 12655860 6051734b 946b8048 61c161d1 f02293fa aa372c18 4fefaa0f
    243  25afc998 fe54da07 8a437412 ed3666c3 fa9053ff bbba554a abf5120c d1c99657 a3c598be d378735a 63d978c2 fe8e05e0 947f8048 81c721d1 7006b3fa 6c3f0c18 b177d9e9
    244  27022747 8ec4d806 ea937413 597666c3 fad053ff 3bfa554a abf1120c 75ca9677 2781ba3e 3ae37b0a 910f0580 63eb71db 947f8048 a1c721d1 f02293fa 2a373c1c 71e181ec
    245  27022947 8e94da07 ea937413 597666c3 fa9053ff 3bfa554a abf1120c 75ca9677 27c1ba3e 3ad3790b 01030881 27dd49b9 947f8048 a1c721d1 f02293fa 2a273c1c 7179d9e9
    246  26eaa95f 8c8eda07 94923413 716166c3 fa9053ff 33fe554a 0bf1120c b5de97f7 03c69afe 8d693232 7c137af2 4ed77cba 947b8048 a1c301d1 7026b3fa 6c2f0c18 f1f5e1e8
    247  20ca84fc 9a13c003 81b1f413 632566c3 fad053fb 19aa5d4e 0bf59204 91df97d5 458a926a 80b50ac8 c21b69f5 d13672cf 947f8048 81d711d3 7006b3fa aa2f0419 4febe20e
    248  203e8f73 7696da07 818db413 e27566c3 fa9053ff 3bfb554a 8ff59204 d38c75e5 cd5c196a 0c4c37a3 365ba3af a8b1869d 947f8048 41d501d1 7006b3fa aa2f1c18 b17fe1e8
    249  22540cea 16efd806 bb87f412 ea6266c3 fad053ff b3bf554a 87f19204 d59ab5e5 ef51da10 b070206b 47466fcf f9b64b2f 947b8048 a1c701d1 f02293fa aa272c18 31ebf9ec
    250  202b8c93 76c2d806 c18db413 a27166c3 fad053ff 3bfb554a 0ff59204 739077e5 850819ca 0b28569a f679f6a7 d30ce26f 947b8048 a1d701d1 f02293fa 6c270c19 0ff9b20b
    251  22ecb004 fe52da07 6941b412 863166c3 fa9053ff bbbb554a 87f59204 318cb605 0982f8f8 040f02c3 8ed141ae 38a719ac 947b8048 81c301d1 f00293fa 2a273419 71e9f1ed
    252  222c10eb 968fda07 9b93f413 6a6266c3 fa9053ff 33ff554a 07f19204 b59eb7e5 87cbdcf0 ad080111 0ba346b5 23b67f74 947b8048 a1c701d1 7026b3fa 2a3f1418 4f6f9a0f
    253  202b4f2b 8ec3d806 8992b413 726666c3 fad053ff 3bfb554a 07f19204 b59eb7e5 6797fcf0 fd3817b1 7c835ddd 36307694 947f8048 81d721d1 7006b3fa 6c370c18 b17f89e9
    254  2a11fe6e e920c202 2efeb412 8a6266c3 fa9053fb 91ee5d4e aff59204 339d7665 e54759d8 f0fb28c9 84f38506 e9d7fa1e 947b8048 a1c301d3 f02293fa 6c373419 f16589ed
    255  2b8258c4 7222c202 a3b33413 992166c3 fa9053fb 19ab5d4e 03f5120c 5bd0d7f7 8d439b3a d71550d1 ab9471c5 da51623e 946b8048 41d161d3 7006b3fa 2a2f041c f1fd91e8
    256  28d1b640 967fd806 e093f413 bf2266c3 fad053ff 33ff554a 03f19204 5fded7d5 4d04b392 a9190039 82f6140c 33b65ae4 947b8048 a1d311d1 7026b3fa 2a3f241d b1f781e9
    257  2b53ac62 eef1d806 5386f412 866566c3 fad053ff b3bf554a a7f59204 319fb685 e15ad970 f6fb6fc3 e23c05c6 e6f92465 947f8048 a1d721d1 7026b3fa 2a373419 cf6f820f
    258  306b4f2a f6ffd806 8b8bf412 527666c3 fad053ff b3bf554a aff19204 7b8b7685 29d537ea 4a344128 b0a6e27d 0368a235 947f8048 a1d721d1 7026b3fa 2a371c19 71f1e9e8
    259  31eace53 1641da07 3326f412 fa4566c3 fa9053ff b3bf554a 0ff59204 9b8477e5 ab0c5cca c5b11b70 d43da236 eddb8ea5 947f8048 41d501d1 7006b3fa 2a272c18 71f1d9e8
    260  325d0d0a 16efd806 bb8bf412 ea6666c3 fad053ff b3bf554a 87f19204 d59ab5e5 ef51fa10 b0f0386a 099675cc d9827e54 947f8048 a1c721d1 f02293fa ec2f2c18 0f79da0b
    261  37f0502c 0e57da07 6946b412 923666c3 fa9053ff bbbb554a 87f19204 358ab5e5 c79cd910 c5e93970 45e00586 bf1f5c8d 947f8048 41d501d1 7006b3fa aa2f3c18 f165c1ec
    262  3241110b 9693da07 9b97f413 6a6666c3 fa9053ff 33ff554a 07f19204 b59eb7e5 87cbfcf0 ad881910 4d4368b6 c2d713dd 947f8048 a1c721d1 7026b3fa ec271418 0f69ea0f
    263  36efa73f 8cc2d806 94963413 716566c3 fad053ff 33fe554a 0bf1120c b5de97f7 038abafe bdfc3c92 0f455b39 1b536588 947f8048 a1c721d1 7026b3fa aa3f041d 31eff9ec
    264  3481e123 f692da07 8f4c3412 507666c3 fa9053ff b3be554a aff1120c 7f8a7687 69027fec 18c73b88 fc5fba50 5c1dc6e8 947f8048 61d501d1 7026b3fa 6c2f2418 cfe7b20f
    265  325d8f7e d63ec202 7d10b412 e07566c3 fa9053fb f1ee5d4e aff49384 1594b74d cb09fa44 d4da3fe2 b4bb0a53 44046e80 947f8048 61d501d3 7026b3fa 6c373c19 3163c1ed
    266  36ffa93f 8c92da07 94963413 716566c3 fa9053ff 33fe554a 0bf1120c b5de97f7 03cabafe bdec3a93 df297439 cfc767e9 947f8048 a1c721d1 7026b3fa aa3f1c1c 71e981ec
    267  34f13720 9613da07 9857f413 6f2666c3 fa9053ff 33ff554a 0bf19204 b5ce97f5 63c69274 70e53c4a 7a981281 194901c1 946f8048 41d571d1 f00293fa 2a272c19 b16bb1ec
    268  3b61978c a205c202 e3c43413 693666c3 fa9053fb 19ab5d4e a3f5120c 53cad677 c741faaa 7daa1892 d1980745 617e784e 947f8048 61d501d3 7026b3fa 2a271c1d b16b99ec
    269  39dad134 164dda07 3342f412 da3166c3 fa9053ff b3bf554a 0ff59204 bb9477e5 e3035cca 3bdd7a18 01b5e15e b68e985c 947b8048 a1c701d1 f02293fa aa371418 f17589e9
    270  3c5c9e24 ac43da07 a946b412 382266c3 fa9053ff dbbb554a 8ff09384 b58fb6ad edd19c5e e22b4768 aeaa7a09 5aa12f11 946b8048 61d161d1 f02293fa aa3f1419 0f75ba0b
    271  38692923 01c4c202 c9b3f412 8f1666c3 fa9053fb 99ea5d4e 03f19204 f7ddd7d5 8f4291e0 847d26c1 d1237e1e a6cb4ecd 946f8048 41d171d3 f00293fa aa2f0c19 4fffc20a
    272  3cfb6767 86c8d806 f28f7413 617666c3 fad053ff 3bfa554a a3f5120c 5bc9d677 05119adc 49a90f3b 5f587430 7ab76860 947f8048 81d721d1 f00293fa aa37041d b1e3f9ed
    273  3ba8cf8c 7653da07 6122b412 221266c3 fa9053ff bbbb554a 8ff59204 939b75e5 890a3b02 92a15e69 c072864f c4fde777 946b8048 41c161d1 7006b3fa aa3f3418 cffba20b
    274  3d0b6967 8698da07 f28f7413 617666c3 fa9053ff 3bfa554a a3f5120c 5bc9d677 05419adc 89a50dba 2d7f7d6b 41065980 947f8048 81c721d1 f00293fa 6c270c19 b177f9e9
    275  3e4f4dc7 c862c003 b301f412 d06266c3 fad053fb f9ea5d4e 8ff09384 3d9fb6ad c9d5fb04 41ad0d79 357902f2 34897250 947b8048 81d701d3 f00293fa ec372c19 b167f9ec
    276  3bf8d18b 7653da07 c16eb413 225266c3 fa9053ff 3bfb554a 8ff59204 939b75e5 895a3b02 d2955fe8 4c818a0f abd5bace 946b8048 41d161d1 7006b3fa aa3f3c19 f16dd9ec
    277  40572828 144eda07 a4243412 d91266c3 fa9053ff b3be554a a3f5120c dbddd677 2d4ed83c d9f43db8 2d6411f1 d7997913 946b8048 41d161d1 f00293fa ec2f2419 317b89e9
    278  4553ecc2 f6f1d806 5b86f412 9e6566c3 fad053ff b3bf554a a7f59204 199fb685 c75b9910 5b577039 2a7925fd a59a52bc 947f8048 81d721d1 f00293fa ec2f2418 f1fde9e9
    279  400f8596 def4d806 8a837412 c56266c3 fad053ff bbba554a abf5120c f9d99657 8d8cb8de 35ba0972 eab571c0 253d67fa 947b8048 a1d301d1 f02293fa aa37041c 0fedba0e
    280  43d6d7eb a9c6c202 97adf412 c11666c3 fa9053fb f9ea5d4e abf49384 33dfd73d ad8694e2 b836120a dfe17e95 5fd72125 946f8048 61d571d3 f02293fa ec2f0c1d cf63ea0f
    281  44841186 c644c202 ad16b412 687666c3 fa9053fb f1ee5d4e 87f09384 9f8f76cd eb871d5a d9ff3f38 310bbb3c 654ce8cc 947f8048 61d501d3 f02293fa aa272c18 0ffd8a0b
    282  42524fa6 ce34c202 a506b412 d06666c3 fa9053fb f1ee5d4e 87f09384 379f76cd 85945b3a af865ab2 f2faeb6e 2e4efd1d 947f8048 41d101d3 f00293fa 6c370418 b1f381e9
    283  4ba1c070 6104c202 26c6b413 a23666c3 fa9053fb 11ae5d4e aff59204 1b8d7665 230419b8 5f446792 502bc47e c1d9f23f 947f8048 41d501d3 7006b3fa 2a3f3418 717999e9
    284  4d2ae007 693dc202 0aca7413 0e7566c3 fa9053fb 71af5d4e 87f0138c f78076cf 89161414 60990cc9 202597d1 7af1b842 946f8048 41c171d3 7006b3fa 6c273418 f17df9e8
    285  48662903 01c4c202 c9b3f412 8f1266c3 fa9053fb 99ea5d4e 03f19204 f7ddd7d5 8f4291e0 847d26c1 511b7e1e 48353eef 946b8048 41d171d3 f00293fa 2a270c19 b16bb1ec
    286  49baffd8 8923c202 c4b5f413 522166c3 fa9053fb 19aa5d4e a7f19204 7d9bb665 4786d8ce 8adc7c0b 87080632 0a235b83 947b8048 81c701d3 f00293fa 6c3f341d 4fe3c20e
    287  4d70ecc2 1701d806 5b86f412 be7566c3 fad053ff b3bf554a a7f59204 f98fb685 4f5c9a10 5d820e11 519a3b07 98b204ed 947f8048 a1d721d1 7026b3fa 6c2f0418 cff7820b
    288  4ecd46fc a213c003 61b1f413 eb2166c3 fad053fb 19aa5d4e abf59204 d1da9655 ed82d022 f1821c58 08a27725 bbf404af 947b8048 a1d711d3 f02293fa ec3f0c19 316ff9ec
    289  4f0fa702 c82fc202 a8037412 ef6266c3 fa9053fb f1ef5d4e 8bf0138c 1fcfd69f 4f81dd0c 8aef68ab 0a641099 10987728 946b8048 61d161d3 7026b3fa 6c3f241c cf6fc20f
    290  4d1fa7a3 d473c003 b6123412 6f7666c3 fad053fb f9eb5d4e 8bf0138c 9fcfd69f af479b0c 73d7787a 60ce7c18 b6747c58 947f8048 a1d721d3 f02293fa 2a2f0c1c 317be1e9
    291  4bfdbe6e 2040c202 4712b412 a27666c3 fa9053fb 91ee5d4e aff59204 1b8d7665 a34019b8 6f5167b3 8b54d8a4 9452dbf7 947f8048 41d101d3 7006b3fa 6c37041d 4ffbfa0a
    292  4a7cb8fc a221c202 63b83413 ed2266c3 fa9053fb 19ab5d4e a3f1120c dfcbd657 4d41b8da f97a3618 8bd3061c 96f846ff 946b8048 41d161d3 f00293fa ec373c1c 4f67fa0e
    293  4e3f9e24 b63dda07 9b45f412 382266c3 fa9053ff d3bf554a 8ff09384 b58fb6ad e5d59c5e d02c0768 4f1c52fa 144c673b 946b8048 61d161d1 f02293fa 2a2f2c18 8f61820e
    294  4ebd60e8 a523c202 64b1f413 ee2166c3 fa9053fb 19aa5d4e a7f59204 d18ab685 e381da8e a5fb3a53 bad80479 311c76f8 946b8048 61d161d3 7026b3fa aa372c1c 3163e1ed
    295  49daffd7 8953c003 c4f5f413 526166c3 fad053fb 19aa5d4e a7f19204 7d9bb665 4756d8ce 4af07e88 bb1d11ea 95877acb 947b8048 81d701d3 f00293fa ec373c18 71f9a1e8
    296  01700652 15652779 f3940fa1 d2a2b574 052fb3fe 0e9e46f8 ad2e79b6 ae236c7c b0ac238b ce8b5a01 7c68b24c 4e319dbf 947f8048 41d111d1 f00293fa ec271c19 cffbda0b
    297  06d282cd 4733297a 0484cfa1 2b91b574 056fb3fe 0e9f46f8 a12ef9be 4c760c6e 70fe046b c95b2499 4d88f39f f9b3f7cd 947f8048 41d111d1 7006b3fa 6c2f0418 8ff9b20a
    298  02663cf6 78e92779 ae758fa1 3b82b574 052fb3fe 069b46f8 012af9be 44750e0e 963405cb 8986191a e219efb5 122cae1f 946f8048 61d111d1 7026b3fa ec3f3c19 71f5f1e8
    299  01d1e27d 4737297a 0488cfa1 3f91b574 056fb3fe 0e9f46f8 a12af9be 28670c8e d6eb634b 443c1762 69c3eecd f20cd4b4 946f8048 41d111d1 7006b3fa ec3f3419 b1e7f9ec
    300  071a8b09 4538297a a3890fa1 1a91b574 056fb3fe 0e9e46f8 052a79b6 6428adfc 34eac779 63a24d59 86d643a5 37c873c7 946f8048 61d111d1 7026b3fa 6c3f0418 4f77aa0a
    301  0783f9f2 5f97297a 1db8cfa1 fcc1b574 056fb3fe 0e9f46f8 852af9be 64362bfe 5ee52caf 4bfa7839 6ed69010 9e208132 946f8048 41c521d1 f00293fa 2a373c1d f1e9e1ec
    302  0701bcb6 51452779 86818fa1 2b92b574 052fb3fe 069b46f8 292ef9be 6a78ce8e 94b7865d 9b9e4e19 0ae21991 e8937ed3 947f8048 61d511d1 f02293fa 2a3f1c18 b1ffa9e9
    303  031c4d31 cf56297a 85914fa1 eaa2b574 056fb3fe 069a46f8 2d2e79b6 ae276e7c 306524eb 956320d2 a2bef0d5 67f18bad 947f8048 41d111d1 f00293fa ec371c19 4fefda0e
    304  08132ad9 4f3a297a 25864fa1 1691b574 056fb3fe 069a46f8 8d2a79b6 4a306bdc f861442b 8c0414a1 fd94d244 bfcd8615 947f8048 61d551d1 7026b3fa ec3f2419 0fedd20f
    305  0dac657a 60e82779 1b790fa1 de81b574 052fb3fe 0e9e46f8 8d2a79b6 8a346bdc 78a6034b 460e40e0 d8acef7d bee5c34f 946f8048 41d111d1 7006b3fa ec2f0419 31f3e1e8
    306  084324da 4f4a2779 25864fa1 1691b574 052fb3fe 069a46f8 8d2a79b6 4a306bdc f8a1442b 8c1412a2 cb98cb45 99a8f18f 947f8048 61d551d1 7026b3fa 2a371419 cf63a20f
    307  08436522 4f4a2779 0d854fa1 0692b574 052fb3fe 069a46f8 a52a79b6 6030ac7c 3a2ee5e9 e40907e3 c7402e6c d7607ffe 947f8048 61c551d1 f02293fa 2a3f1419 0f79820a
    308  0bc73d12 4f77297a 07c58fa1 04d1b574 056fb3fe 069b46f8 a52af9be 64332c7e 96ef2de7 43c77d5b f3c9fc40 1a84cd42 947f8048 41d561d1 7006b3fa 2a2f1c1d b1e399ed
    309  0cd05a7a 1f94297a fdd4cfa1 d8e2b574 056fb3fe 0e9f46f8 a52ef9be a0252c5e 5ee24b8f 88960f2a d303aec0 d6d5fe18 947f8048 61d561d1 f02293fa 6c3f2c18 4ffbaa0b
    310  524965fa 574a2779 2d864fa1 de91b574 052fb3fe 069a46f8 852a79b6 8030abfc 9e27e349 4ff36893 4ffd76bc 72fa3427 947f8048 61d551d1 f02293fa ec2f1c19 4f6baa0f
    311  56192b41 5139297a fb880fa1 0e92b574 056fb3fe 0e9e46f8 ad2a79b6 62246c5c 766f468b 9c8d08a1 093eff1e 8b4df24e 946f8048 61d511d1 f02293fa 2a2f0c19 4fff820b
    312  51d7e37d 6737297a 2488cfa1 ff91b574 056fb3fe 0e9f46f8 812af9be 60660c0e 9cee6443 5e8c4920 f577bdad db36fe25 946f8048 41d511d1 7006b3fa aa2f0419 0fe9aa0f
    313  57c8bbd2 4f77297a 27c58fa1 54d1b574 056fb3fe 069b46f8 852af9be 0c322bfe 74e32d2f 26a14841 1a1fc749 e032f87b 947f8048 61c561d1 f02293fa ec273418 b1efd1ec
    314  55f6f5ab 47442779 9584cfa1 64d2b574 052fb3fe 0e9f46f8 052ef9be 2c2a2dde b6206e67 a4be0f42 7441f652 2232a89b 946f8048 61d521d1 7026b3fa aa3f1418 71e1d1ed
    315  56492542 51492779 fb880fa1 0e92b574 052fb3fe 0e9e46f8 ad2a79b6 62246c5c 56ab468b 147d2342 3eb4dc14 2314f5e7 946f8048 41d111d1 7006b3fa 2a2f0c18 31ff89e8
    316  5cd98455 7734297a 7484cfa1 b392b574 056fb3fe 0e9f46f8 292ef9be ea78ce8e b467885d bbcb6d9a aafd5ecb ac014f28 947f8048 61c511d1 7026b3fa 2a2f1c19 f1f1a1e8
    317  5e45a402 4f4a2779 85854fa1 5e92b574 052fb3fe 069a46f8 2d2a79b6 2a246e5c 74a106eb 84110560 ef3ba48e fa9bdbde 946f8048 61d511d1 f02293fa aa2f341c cf639a0e
    318  5b2f3b76 59692779 2e958fa1 1ba2b574 052fb3fe 069b46f8 812af9be 44610c0e b62743ab db6565b8 4feae12c 1c0a85cc 947f8048 41d151d1 f00293fa 6c273418 cfe7ba0f
    319  5cd5422d 4733297a 1c84cfa1 4391b574 056fb3fe 0e9f46f8 812ef9be 2c770bee 70e803c3 e4240363 417fdca5 af73fbaf 947f8048 61d551d1 7026b3fa ec2f2418 317799e8
    320  5d097e56 77442779 7484cfa1 b392b574 052fb3fe 0e9f46f8 292ef9be ea78ce8e 94a3885d b37766f9 7c0f7e03 6c0c53e0 947f8048 41c111d1 7006b3fa 6c3f041c 8f7d820a
    321  59f53613 87472779 6d88cfa1 44d1b574 052fb3fe 0e9f46f8 2d2af9be 4a3aee5e 76a5e039 1b905e3b 90094ff7 d6bf57de 947f8048 61d511d1 f02293fa ec3f3418 4ff7ea0a
    322  5ed642f5 5f34297a 7c84cfa1 1b92b574 056fb3fe 0e9f46f8 292ef9be 8278ce8e 9e7486fd 6e6e6022 b29543ca 33f154f8 947f8048 61d551d1 7026b3fa 2a3f1418 0ff5f20a
    323  6504bbee 51432779 06818fa1 5391b574 052fb3fe 069b46f8 a92ef9be 2275cc8e babf8295 17cf7953 669e3762 600c2961 947f8048 61d111d1 f02293fa aa3f3c19 f17991e9
    324  66d5c4b5 d135297a 86818fa1 ab92b574 056fb3fe 069b46f8 292ef9be ea78ce8e b46f885d a3d16d5a 6d063e0b 7e1701e2 947f8048 61d111d1 7026b3fa 6c273c19 8f65da0e
    325  634443b2 57462779 0d814fa1 6a92b574 052fb3fe 069a46f8 a52e79b6 0c23ac5c 3029c509 50f02eea b8f75c27 28be1807 946f8048 41d511d1 7006b3fa 2a2f041d 317fe9e8
    326  64055be6 51492779 06858fa1 5792b574 052fb3fe 069b46f8 a92af9be 0e61cc6e b2a6e2fd f45e3142 07304839 da6b2583 946f8048 41d111d1 7006b3fa aa2f3c19 7171c1e8
    327  66325c3e 71672779 a6958fa1 2fa1b574 052fb3fe 069b46f8 092af9be 4e65cdee b6ade53d eb6775ba 1a3a7e11 fd3b7b73 947f8048 41d511d1 f00293fa aa272419 3173c9e9
    328  6e4c63fa 61482779 9b890fa1 5e91b574 052fb3fe 0e9e46f8 0d2a79b6 2a286ddc 30ac066b d91c0338 b4cdc524 8949a94f 946f8048 61d511d1 7026b3fa 2a3f0c18 cfe3ca0f
    329  6f2cbeb6 51652779 26918fa1 cba2b574 052fb3fe 069b46f8 892ef9be a265cc0e 1ead8535 4bac5a9b 25111d68 c52c0259 947f8048 41d111d1 f00293fa ec37241d b173e1e8
    330  6e1c69f9 6138297a 1b890fa1 5e91b574 056fb3fe 0e9e46f8 8d2a79b6 0a346bdc f866054b 36024463 00bbad84 78968a34 947f8048 61d511d1 7026b3fa 6c37341d cfeff20f
    331  6f5be3a5 0718297a fc78cfa1 c782b574 056fb3fe 0e9f46f8 a12af9be a0760c8e f0fe64a3 a2944ac8 9bcdab7f 2e06a345 946f8048 41d511d1 f00293fa 6c373419 8ffdfa0b
    332  6a069f46 d9452779 8e818fa1 8f92b574 052fb3fe 069b46f8 212ef9be 08790e6e 72386543 20c03fcb e01e9716 0483d96f 947f8048 61d511d1 f02293fa aa3f3c19 31f7b1e9
    333  724563fa 574a2779 ad864fa1 5e91b574 052fb3fe 069a46f8 052a79b6 2034adfc f62be629 f0f129cb 0c0b5287 1e674764 947f8048 41c551d1 f00293fa aa3f3c1c cfffea0a
    334  721cea39 9138297a 7b890fa1 4e91b574 056fb3fe 0e9e46f8 2d2a79b6 42396e5c f2614823 fc592403 ed1fa29e dada8f9f 947f8048 61c151d1 7026b3fa 6c370c19 4f7fe20a
    335  751a8991 a539297a 7b880fa1 6292b574 056fb3fe 0e9e46f8 252a79b6 2438ae7c 18e2c799 f79d4f51 2c1b229c bd483bd4 947f8048 61c111d1 f02293fa aa372419 3177c9e9
    336  71d3e17d 6737297a 2488cfa1 7f91b574 056fb3fe 0e9f46f8 812af9be e0660c0e 1ce26643 5ea34c00 00889dbc 3de8ed04 946f8048 61c511d1 7026b3fa 2a372418 31f7d9e9
    337  7e1c7533 4f632779 07918fa1 ece1b574 052fb3fe 069b46f8 a52ef9be 8c262c5e 1a206ae7 85a90dd2 7cf9835b 43e5c469 947f8048 41d521d1 f00293fa 2a3f2c19 8f79fa0b
    338  79953393 87272779 6d78cfa1 c4c1b574 052fb3fe 0e9f46f8 2d2af9be ca3aee5e 76a1ee39 fb69669b 66de1d75 c683761f 946f8048 41d521d1 f00293fa 2a3f3c18 4f6b920e
    339  7b1d4cb1 4f56297a 05914fa1 caa2b574 056fb3fe 069a46f8 ad2e79b6 ae236c7c d06c238b ee825b82 9c0cef35 6ae1ceef 947f8048 61d511d1 f02293fa ec3f1419 0fe5c20e
    340  7b6d46b2 4f662779 05914fa1 caa2b574 052fb3fe 069a46f8 ad2e79b6 ae236c7c d0ac238b eeb25981 ea60e037 c51a93b5 947f8048 61d511d1 f02293fa 2a270c1c 0ff5ea0b
    341  82dd84cd 5953297a 0e918fa1 cba1b574 056fb3fe 069b46f8 a12ef9be ac660c6e 30f1456b 2c423483 9d35f245 a42dad07 947f8048 41d551d1 7006b3fa aa270418 f179c1e8
    342  86cc5afa 4f95297a 07d18fa1 f8e2b574 056fb3fe 069b46f8 a52ef9be 80252c5e 36e10b0f 1f9e5f30 a2d0f4b9 94c2da0b 947f8048 61d521d1 7026b3fa aa3f3419 4f6bda0e
    343  836c4732 57662779 0d914fa1 eaa2b574 052fb3fe 069a46f8 a52e79b6 8c23ac5c 902dc309 b8e82e0a 9c024e8e 5840755c 947f8048 41d511d1 7006b3fa 2a2f341c 71ed89ed
    344  860a5ebe f1472779 a6858fa1 af91b574 052fb3fe 069b46f8 092af9be ce65cdee 96a5e73d 4366757a 4c487f38 53211011 946f8048 41d111d1 f00293fa ec2f2418 0ff5ca0b
    345  83dd6465 5159297a 06958fa1 d7a2b574 056fb3fe 069b46f8 a92af9be 8e61cc6e 126ae4fd 3cb41821 3fb16e22 5d856098 947f8048 41d111d1 f00293fa 6c373419 71f191e8
    346  842d5e66 51692779 06958fa1 d7a2b574 052fb3fe 069b46f8 a92af9be 8e61cc6e 12aae4fd bc683222 3e445400 fe35519b 947f8048 41d111d1 7006b3fa aa3f0418 8f6dc20e
    347  8d337ed6 57682779 1c98cfa1 f3a2b574 052fb3fe 0e9f46f8 812af9be 6c650c0e d82f042b 94fc2842 1d0bbe07 58c9cda7 947f8048 61d551d1 7026b3fa aa3f0419 0f7d920a
    348  8f30bcb6 51652779 26918fa1 4ba2b574 052fb3fe 069b46f8 892ef9be 2265cc0e dea98335 bbc1793b c0bb4243 d75f037b 947f8048 61d111d1 7026b3fa 6c3f0418 0fe1b20e
    349  8ce10295 5155297a ae918fa1 43a2b574 056fb3fe 069b46f8 012ef9be 4c6a0dee 94eb04eb 5c472321 d7fadfc5 9aa3bb54 947f8048 41d111d1 f00293fa 2a272418 b173a1e9
    350  8d46c6aa ef462779 ad824fa1 a291b574 052fb3fe 069a46f8 052e79b6 ec39addc f42a84d9 bf696290 8210304c 3b792ba5 947f8048 41c151d1 f00293fa ec3f2418 8f698a0f
    351  8e23f6ab 47642779 1594cfa1 44e2b574 052fb3fe 0e9f46f8 852ef9be 2c262bde b6276d47 1faf4b92 0b74de11 0615ed31 947f8048 61d121d1 7026b3fa ec270419 b1e7a1ed
    352  8a166c79 ef3a297a a5864fa1 be91b574 056fb3fe 069a46f8 0d2a79b6 c2346ddc f26c45ab 8c8b0881 6a3db035 65d2fd17 947f8048 61c511d1 7026b3fa aa2f3c18 0ff5820a
    353  89f7f573 c7472779 7f858fa1 7cd1b574 052fb3fe 069b46f8 2d2af9be 0a36ee5e 76a0eed9 c063274b 85fb0684 e5551ec5 947f8048 41d121d1 f00293fa 2a272c1d 3167e9ec
    354  9622f72b 47642779 9594cfa1 64e2b574 052fb3fe 0e9f46f8 052ef9be 2c2a2dde b6206e67 a4be0f42 7441e653 61f2a09b 947f8048 61d521d1 7026b3fa aa3f0419 f1e9c9ec
    355  949a8c11 a519297a 7b780fa1 e282b574 056fb3fe 0e9e46f8 252a79b6 a438ae7c 38eec599 df934db1 5b2448a4 2c327b84 946f8048 61d111d1 f02293fa 6c370c19 b1fb81e8
    356  9e71a482 4f6a2779 85954fa1 5ea2b574 052fb3fe 069a46f8 2d2a79b6 2a246e5c 74a106eb 84110560 313b8c8f 600be6d4 947f8048 61d511d1 f02293fa ec2f1c1d 0ff9fa0a
    357  99893b92 8797297a edb8cfa1 44c1b574 056fb3fe 0e9f46f8 ad2af9be 2a36ec5e be71ecd9 de9d4820 00cb3c4e b4bc331f 946f8048 61d521d1 7026b3fa ec3f241c f165c1ec
    358  9b214ab1 4f56297a 05914fa1 4aa2b574 056fb3fe 069a46f8 ad2e79b6 2e236c7c 5068258b 6e696222 9a639907 fefd89a4 947f8048 41d511d1 f00293fa aa270c19 31f7a9e9
    359  9b7144b2 4f662779 05914fa1 4aa2b574 052fb3fe 069a46f8 ad2e79b6 2e236c7c 70a4258b 76935c41 667a8cff 2c5affcc 947f8048 61d111d1 f02293fa aa27341c 8f75f20b
    360  104264a2 4f4a2779 8d854fa1 2692b574 052fb3fe 069a46f8 252a79b6 6034ae7c 3a23e889 8f0e4593 676d4e25 de296d6f 947f8048 61c151d1 f02293fa 6c273418 7165d1ec
    361  14c49b5a bf75297a ffc18fa1 70d2b574 056fb3fe 069b46f8 ad2ef9be 0634ec7e 946d8d71 a65a60e1 0a95433e 3fe4432f 947f8048 61d161d1 7026b3fa 2a2f2419 f161f1ed
    362  a3704532 57662779 0d914fa1 6aa2b574 052fb3fe 069a46f8 a52e79b6 0c23ac5c 3029c509 50f02eea 38ff6426 28d80fcc 947f8048 41d511d1 7006b3fa aa370c1c b163d1ed
    363  a652854d 4713297a 0474cfa1 ab81b574 056fb3fe 0e9f46f8 a12ef9be cc760c6e f0ee066b b9732299 f99986a4 ea43cacc 946f8048 61c511d1 7026b3fa ec37141d 4f63920e
    364  a1317c56 51652779 06918fa1 53a2b574 052fb3fe 069b46f8 a92ef9be 2264cc8e deaa831d 58de3989 be8229db 57f10f90 947f8048 41d151d1 f00293fa 2a272c1c f1f1a1e8
    365  a4315c66 51692779 06958fa1 57a2b574 052fb3fe 069b46f8 a92af9be 0e61cc6e b2a6e2fd f45e3142 c9384838 83e72701 947f8048 41d111d1 7006b3fa 6c373c18 0f61da0f
    366  a6f6d4e3 c7432779 ed84cfa1 90d1b574 052fb3fe 0e9f46f8 ad2ef9be ee35ec7e 1aa18bd9 adfd2a90 370e1d2d bdc95d0d 947f8048 61c561d1 7026b3fa aa370419 cf73b20b
    367  afdfe425 0738297a fc88cfa1 c792b574 056fb3fe 0e9f46f8 a12af9be a0760c8e f0fe64a3 a2944ac8 59d58b7e 3b70857f 947f8048 41d511d1 f00293fa 2a3f1418 4f67f20f
    368  a997f3f3 c7272779 7f758fa1 fcc1b574 052fb3fe 069b46f8 2d2af9be 8a36ee5e 76a0ecd9 d07b25cb c8066524 98167bcf 946f8048 61d521d1 f02293fa ec270c1d 4f77ba0a
    369  ae78647a 61682779 9b990fa1 5ea1b574 052fb3fe 0e9e46f8 0d2a79b6 2a286ddc 30ac066b d91c0338 b4cdbd25 6ac1f32c 947f8048 61d511d1 7026b3fa 2a3f0419 3173f9e8
    370  acd90415 d135297a ae818fa1 c392b574 056fb3fe 069b46f8 012ef9be cc6a0dee b4e706eb b4552341 80fcfeee 5d2f8566 946f8048 41d111d1 f00293fa aa2f0419 cff3ea0a
    371  b64d2742 d1492779 fb880fa1 8e92b574 052fb3fe 0e9e46f8 ad2a79b6 e2246c5c b6af448b 7c7b2422 45c9a18d 3fd0e554 946f8048 41d111d1 7006b3fa aa271419 316bb9ec
    372  b1dfe2fd 6757297a 2498cfa1 7fa1b574 056fb3fe 0e9f46f8 812af9be e0660c0e 1ce26643 5ea34c00 0090adbd 1d18c5c7 947f8048 61c511d1 7026b3fa 2a3f3419 716189ec
    373  b61d2d41 d139297a fb880fa1 8e92b574 056fb3fe 0e9e46f8 ad2a79b6 e2246c5c b663448b 4c622681 52e7fe6c 9e558e04 946f8048 41c511d1 7006b3fa 2a272419 b1f3b9e8
    374  b52abd6e d1632779 86918fa1 93a1b574 052fb3fe 069b46f8 292ef9be 0269ce8e 92a1c575 b3a24cd9 d8b87022 76907a9b 947f8048 41d551d1 f00293fa ec2f3419 0f61b20f
    375  b4dac36d d153297a 86918fa1 93a1b574 056fb3fe 069b46f8 292ef9be 0269ce8e 9261c575 33f66eda 79016e02 8ecd0420 947f8048 41d551d1 7006b3fa 6c372c18 71e9c9ed
    376  b9f93413 87472779 6d88cfa1 c4d1b574 052fb3fe 0e9f46f8 2d2af9be ca3aee5e 76a1ee39 fb69669b a8ce1d75 fa876177 947f8048 41d521d1 f00293fa 6c2f3c18 0fedca0e
    377  bcd7c36d d133297a 8e818fa1 f391b574 056fb3fe 069b46f8 212ef9be a47a0e6e b2f207ab a4011561 35daf586 cce6c47f 947f8048 61d551d1 f02293fa ec3f0419 71fdb1e9
    378  c656834d 4713297a 0474cfa1 2b81b574 056fb3fe 0e9f46f8 a12ef9be 4c760c6e 70ee046b 09472519 0973fe1f abb7c1d6 946f8048 41c111d1 7006b3fa ec2f0c18 f169e1ec
    379  c14c05d2 15452779 f3840fa1 d292b574 052fb3fe 0e9e46f8 ad2e79b6 ae236c7c d0b0238b b6a358e1 9d72f944 5c8fe706 946f8048 61d511d1 f02293fa 6c372419 4f63920e
    380  c665bd36 50e52779 86718fa1 2b82b574 052fb3fe 069b46f8 292ef9be 6a78ce8e 94a7865d db924e99 a6d33952 8dd67409 946f8048 61c511d1 f02293fa aa3f3c19 31f781e8
    381  c62e5e3e f1672779 a6958fa1 afa1b574 052fb3fe 069b46f8 092af9be ce65cdee 96a5e73d 4366757a 8a585f39 fda5067a 947f8048 41d111d1 f00293fa 2a3f0419 4f7fba0a
    382  c3184bb1 cf36297a 85814fa1 ea92b574 056fb3fe 069a46f8 2d2e79b6 ae276e7c 306524eb 956320d2 a2b6f8d4 88138d6c 946f8048 41d111d1 f00293fa ec2f2418 4fe7e20e
    383  c449a61a cf4a2779 8d864fa1 c691b574 052fb3fe 069a46f8 252a79b6 c035ae7c d632a601 3cb51a83 a8a1205e dabb7d2f 947f8048 41d551d1 f00293fa 2a373c19 b1e391ec
    384  c9230ad1 b555297a 73940fa1 72a2b574 056fb3fe 0e9e46f8 2d2e79b6 2e276e7c 506126eb 756523f2 07aafb5d e8238727 947f8048 41d111d1 f00293fa aa2f2419 8ff9da0a
    385  d51e8b91 a539297a 7b880fa1 e292b574 056fb3fe 0e9e46f8 252a79b6 a438ae7c 38eec599 df934db1 db1448a7 8bb07f04 947f8048 61d111d1 f02293fa ec270c1c 717989e8
    386  d250e63a 91482779 7b890fa1 ce91b574 052fb3fe 0e9e46f8 2d2a79b6 c2396e5c 12ad4623 a45d23e0 41e7f946 7660a757 947f8048 61d151d1 7026b3fa aa37241c 71fdc9e8
    387  d9c53c12 8777297a edc8cfa1 44d1b574 056fb3fe 0e9f46f8 ad2af9be 2a36ec5e be6decd9 ce9c4880 b1c4652e b88b2fe7 947f8048 61d121d1 7026b3fa aa2f0c1c 8f65820e
    388  e4560315 7115297a 2e718fa1 2382b574 056fb3fe 069b46f8 812ef9be 4c760bee 54e4024b 053c03d1 9d44ab25 e734d7d4 946f8048 41d511d1 7006b3fa 2a373418 f17589e8
    389  e6d684cd 4733297a 0484cfa1 ab91b574 056fb3fe 0e9f46f8 a12ef9be cc760c6e d0fa066b 515f2279 d69ab7ec 166bbe5c 947f8048 41d111d1 7006b3fa 6c37041d 31e7f9ed
    390  e14803d2 95452779 f3840fa1 5292b574 052fb3fe 0e9e46f8 ad2e79b6 2e236c7c 70a8258b 5e965ca1 2978f5ec 42f5c92e 946f8048 61d111d1 f02293fa 6c271c19 b177f9e8
    391  ecdd0495 d155297a ae918fa1 c3a2b574 056fb3fe 069b46f8 012ef9be cc6a0dee b4e706eb b4552341 810cfeed be2394bc 947f8048 41d111d1 f00293fa aa3f0418 3173f9e9
    392  e91b0b51 b535297a 73840fa1 f292b574 056fb3fe 0e9e46f8 2d2e79b6 ae276e7c 306924eb 5d6420b2 fdaee9d4 4b979957 946f8048 41d511d1 f00293fa ec2f1418 b1e7e1ed
    393  ebcb3b12 4f77297a 07c58fa1 84d1b574 056fb3fe 069b46f8 a52af9be e4332c7e f6e72be7 0bb4591b 091c93a3 05f6a13a 947f8048 41d161d1 f00293fa ec3f3c18 b163d1ed
    394  e9fbf373 c7472779 7f858fa1 fcd1b574 052fb3fe 069b46f8 2d2af9be 8a36ee5e 76a0ecd9 d07b25cb 48167d24 78b46854 947f8048 61d521d1 f02293fa 6c37241d 0fe59a0f
    395  e9966af9 6f1a297a a5764fa1 3e81b574 056fb3fe 069a46f8 0d2a79b6 42346ddc f27847ab cc8408a1 4756b946 f707dbac 946f8048 41d511d1 7006b3fa 6c3f0419 71e5b1ec
    396  e94b0552 b5452779 73840fa1 f292b574 052fb3fe 0e9e46f8 2d2e79b6 ae276e7c 50a524eb 758c1b51 6b2bd83d 292e96e7 946f8048 61d111d1 f02293fa 6c2f3418 316791ed
    397  e84726da 4f4a2779 25864fa1 9691b574 052fb3fe 069a46f8 8d2a79b6 ca306bdc 78a5422b 8c071102 1c7bb3b4 d5cd8095 947f8048 41d551d1 7006b3fa aa2f3c18 0f65fa0e
    398  19993593 87272779 6d78cfa1 44c1b574 052fb3fe 0e9f46f8 2d2af9be 4a3aee5e 76a5e039 1b905e3b 100157fc 38ed677c 946f8048 61d511d1 f02293fa 6c373c1d b1e7d9ec
    399  1c5584d5 7714297a 7474cfa1 b382b574 056fb3fe 0e9f46f8 292ef9be ea78ce8e 9473885d 73af4d7a ff897ea2 8c237818 946f8048 41d111d1 f00293fa ec2f0418 0fe1d20f
    400  1c657ed6 76e42779 7474cfa1 b382b574 052fb3fe 0e9f46f8 292ef9be ea78ce8e 94a3885d b37766f9 39ff7e00 fc844250 946f8048 41c111d1 7006b3fa 2a2f0419 317f91e9
    401  f34ac572 3d452779 fb840fa1 fa92b574 052fb3fe 0e9e46f8 ad2e79b6 86336c7c 7aad236b 813506d9 01c7f6f6 d503d7ec 947f8048 61c551d1 7026b3fa aa271c19 3177f1e8
    402  f2162cc1 5736297a 0d814fa1 ae92b574 056fb3fe 069a46f8 a52e79b6 c833ac5c 5ee7e479 a17324d8 d18f06e4 fa86010c 947f8048 41c151d1 f00293fa ec3f3c18 b173a9e9
    403  f67125c2 d1692779 fb980fa1 8ea2b574 052fb3fe 0e9e46f8 ad2a79b6 e2246c5c b6b3448b 0c6e2402 bed6e8ac 4040f07d 947f8048 41d511d1 7006b3fa aa3f1c18 31fbf9e8
    404  f6212bc1 d159297a fb980fa1 8ea2b574 056fb3fe 0e9e46f8 ad2a79b6 e2246c5c b663448b 4c622681 94ffde6f 6b758a6f 947f8048 41c511d1 7006b3fa 6c3f041c cffbc20a
    405  f646a682 4f4a2779 05854fa1 be92b574 052fb3fe 069a46f8 ad2a79b6 aa206c5c b4ac038b d70941f0 527fffa4 924c86ad 946f8048 41d511d1 f00293fa 2a3f0c18 4ffbb20a
    406  f997ec39 4914297a 03750fa1 ee81b574 056fb3fe 0e9e46f8 a52e79b6 8834ac5c 7afbe361 b4000162 6349764f 48fb0366 946f8048 61d511d1 7026b3fa aa37241d 0f75d20a
    407  fb5662e5 7119297a a6758fa1 3782b574 056fb3fe 069b46f8 092af9be 4674cdee 7068e595 fcf82aa3 22107aa0 16731d60 946f8048 41c511d1 f00293fa 6c37241d 4ffff20a
    408  fe1dac81 cf5a297a 85954fa1 dea2b574 056fb3fe 069a46f8 2d2a79b6 aa246e5c 346144eb 04df38e1 9c56941e 794bce3e 947f8048 41d151d1 7006b3fa aa3f3419 b167e9ed
    409  2468bb6e 50e32779 06718fa1 5381b574 052fb3fe 069b46f8 a92ef9be 2275cc8e babf8295 17cf7953 66861761 5ef43543 946f8048 61d111d1 f02293fa aa271c18 4fe3ba0e
    410  2651c535 d115297a 86718fa1 ab82b574 056fb3fe 069b46f8 292ef9be ea78ce8e b46f885d a3d16d5a 2b1e260b 6c595598 946f8048 61d111d1 7026b3fa 2a3f2419 316bf9ec
    411  26065cbe 71472779 a6858fa1 2f91b574 052fb3fe 069b46f8 092af9be 4e65cdee b6ade53d eb6775ba 1a3a6611 db575d99 946f8048 41d511d1 f00293fa aa270c19 cfefba0f
    412  24d20295 7135297a 2e818fa1 2392b574 056fb3fe 069b46f8 812ef9be 4c760bee 54e4024b 053c03d1 df3cb325 f4e6fbad 947f8048 41d511d1 7006b3fa 6c2f3c18 cff3c20a
    413  21740452 95652779 f3940fa1 52a2b574 052fb3fe 0e9e46f8 ad2e79b6 2e236c7c 70a8258b 5e965ca1 2988fdef a0c58ad4 947f8048 61d111d1 f02293fa 6c37241c 4f73aa0b
    414  2f08be36 51452779 26818fa1 cb92b574 052fb3fe 069b46f8 892ef9be a265cc0e 1ead8535 4bac5a9b 63191568 f30a1731 946f8048 41d111d1 f00293fa 2a3f1c1d 71f1d1e8
    415  29629ec6 d8e52779 8e718fa1 8f82b574 052fb3fe 069b46f8 212ef9be 08790e6e 72386543 20c03fcb a2168716 95b7e6b7 946f8048 61d511d1 f02293fa 6c372c19 b1f3e1e9
    416  291f0cd1 b555297a 73940fa1 f2a2b574 056fb3fe 0e9e46f8 2d2e79b6 ae276e7c 506524eb 757c2152 d8bfc13c 550cfbbe 947f8048 61d111d1 f02293fa 2a3f2c18 f1e981ed
    417  2db0637a 60e82779 1b790fa1 5e81b574 052fb3fe 0e9e46f8 8d2a79b6 0a346bdc f8a6054b 36124260 2ecf967c ac4e9fcc 946f8048 61d511d1 7026b3fa 2a372c18 f1f1a1e8
    418  296f06d2 b5652779 73940fa1 f2a2b574 052fb3fe 0e9e46f8 2d2e79b6 ae276e7c 50a524eb 758c1b51 a933b03e 38e4db44 947f8048 61d111d1 f02293fa aa370c19 8fedba0f
    419  2da06979 6118297a 1b790fa1 5e81b574 056fb3fe 0e9e46f8 8d2a79b6 0a346bdc f866054b 36024463 3eaba584 90829837 946f8048 61d511d1 7026b3fa aa272c1d cf77f20a
    420  2a126a79 6f3a297a a5864fa1 3e91b574 056fb3fe 069a46f8 0d2a79b6 42346ddc f27847ab cc8408a1 4756b945 36b7afa7 947f8048 41d511d1 7006b3fa 6c3f0418 f17d91e9
    421  349e8a11 a519297a 7b780fa1 6282b574 056fb3fe 0e9e46f8 252a79b6 2438ae7c 18f2c799 b7a94ed1 7822395f c075760d 946f8048 61d111d1 f02293fa aa373c1c 0ff5a20a
    422  366aa602 4f6a2779 05954fa1 bea2b574 052fb3fe 069a46f8 ad2a79b6 aa206c5c b4ac038b d70941f0 5267ffa5 13da8acc 947f8048 41d511d1 f00293fa 2a270c19 b17fb9e8
    423  37ccb9d2 4f77297a 27c58fa1 d4d1b574 056fb3fe 069b46f8 852af9be 8c322bfe f4f72b2f e6884b61 4f46e6c9 4a8ed00b 947f8048 41d561d1 f00293fa ec3f1418 71f9a9e8
    424  3bd26265 7139297a a6858fa1 3792b574 056fb3fe 069b46f8 092af9be 4674cdee 7068e595 fcf82aa3 e0187a9b 87190899 947f8048 41c511d1 f00293fa 2a3f2418 8fe1fa0f
    425  3cc79ada 5f75297a 7fc18fa1 90d2b574 056fb3fe 069b46f8 2d2ef9be 0638ee7e 74648f11 45672171 87cb003f 9b360505 947f8048 61d161d1 7026b3fa aa3f241c 8ff9f20a
    426  3cf794db 5f452779 7f818fa1 90d2b574 052fb3fe 069b46f8 2d2ef9be 0638ee7e 54a88f11 7d2d0012 3ef97904 2861660e 947f8048 41d561d1 f00293fa ec270418 8f75920b
    427  3b194c31 4f36297a 05814fa1 ca92b574 056fb3fe 069a46f8 ad2e79b6 ae236c7c d06c238b ee825b82 59fcf735 384bb83d 946f8048 61d511d1 f02293fa aa2f1c19 f17989e9
    428  3b494632 4f462779 05814fa1 ca92b574 052fb3fe 069a46f8 ad2e79b6 ae236c7c d0ac238b eeb25981 6a68f834 674ec3d4 946f8048 61d511d1 f02293fa aa2f2419 b1eff9ec
    429  3b2b3d76 59692779 2e958fa1 9ba2b574 052fb3fe 069b46f8 812af9be c4610c0e 362b45ab bb786798 94f2f0ac 6da1d597 947f8048 61d151d1 f02293fa 6c2f0418 0fedd20e
    430  3df873b3 4f432779 07818fa1 ecd1b574 052fb3fe 069b46f8 a52ef9be 8c262c5e 1a206ae7 85a90dd2 bee1835a b7bd8e82 946f8048 41d521d1 f00293fa 6c272c18 71e1b1ed
    431  3cd9442d 4733297a 1c84cfa1 c391b574 056fb3fe 0e9f46f8 812ef9be ac770bee f0ec05c3 640900c3 08879205 0fc9937e 947f8048 41d551d1 7006b3fa aa2f1c18 8f71ea0a
    432  4171c42a 45642779 9b950fa1 22a1b574 052fb3fe 0e9e46f8 052e79b6 6c29addc 3c328759 cd871f90 e4c61325 c89e50ad 947f8048 61d551d1 f02293fa aa371419 4fefb20e
    433  41dde1fd 4757297a 0498cfa1 3fa1b574 056fb3fe 0e9f46f8 a12af9be 28670c8e d6eb634b 443c1762 e9bbbecd 8ec49a8f 947f8048 41d111d1 7006b3fa 6c370419 8f75da0a
    434  46c8597a 4f75297a 07c18fa1 f8d2b574 056fb3fe 069b46f8 a52ef9be 80252c5e 36e10b0f 1f9e5f30 64c0ccb8 45d299a0 946f8048 61d521d1 7026b3fa 6c2f0c18 0f75820b
    435  47c7f972 5f77297a 1dc8cfa1 fcd1b574 056fb3fe 0e9f46f8 852af9be 64362bfe 5ee52caf 4bfa7839 b0d6880b bc77c0b1 947f8048 41c521d1 f00293fa 6c373418 cf6fba0f
    436  47268989 4558297a a3990fa1 1aa1b574 056fb3fe 0e9e46f8 052a79b6 6428adfc 34eec779 53a34d79 4bcf1ae5 db787154 947f8048 61d511d1 7026b3fa 2a371c18 31ffc1e9
    437  43023c76 79492779 ae858fa1 3b92b574 052fb3fe 069b46f8 012af9be 44750e0e 963405cb 8986191a e201bfb5 116089ff 947f8048 61d111d1 7026b3fa ec270c19 4fffd20a
    438  44d8c3ed 5133297a 06818fa1 d391b574 056fb3fe 069b46f8 a92ef9be a275cc8e fa6f8495 77fd7f50 060778d2 7ee04063 947f8048 41c511d1 f00293fa aa37041c 4ff3ea0a
    439  434845b2 57462779 0d814fa1 ea92b574 052fb3fe 069a46f8 a52e79b6 8c23ac5c 902dc309 b8e82e0a ddfa368e 69f8549f 946f8048 41d511d1 7006b3fa 6c271c1c 716181ec
    440  4f04bc36 51452779 26818fa1 4b92b574 052fb3fe 069b46f8 892ef9be 2265cc0e dea98335 3bbd593b 0ff83ae3 41492679 946f8048 61d111d1 f02293fa 6c270418 4fe7da0e
    441  49926cf9 ef1a297a a5764fa1 be81b574 056fb3fe 069a46f8 0d2a79b6 c2346ddc f27c45ab 4c9f0801 1046b3b6 e17d846e 946f8048 61d511d1 7026b3fa ec273c19 4fe3fa0e
    442  4cd50215 5135297a ae818fa1 4392b574 056fb3fe 069b46f8 012ef9be 4c6a0dee 94eb04eb 5c472321 19fadfc6 f39bdc44 946f8048 41d111d1 f00293fa 6c272419 8fe9820f
    443  499bf5f3 c7272779 7f758fa1 7cc1b574 052fb3fe 069b46f8 2d2af9be 0a36ee5e 76a0eed9 c063274b 47fb0e7f 9ad31b64 946f8048 41d121d1 f00293fa ec273418 0fe9da0f
    444  4e5065fa 61482779 1b890fa1 de91b574 052fb3fe 0e9e46f8 8d2a79b6 8a346bdc 78a6034b 460e40e0 96b4ff7c e987d1bc 947f8048 41d111d1 7006b3fa aa371418 0f61820e
    445  4a21f5f3 4f672779 87958fa1 3ce1b574 052fb3fe 069b46f8 252af9be 4c272e7e dcff6067 3f375611 c54fe998 63858eaa 947f8048 61c151d1 f02293fa 6c27141d 8ff9aa0b
    446  4df7f62b 47442779 1584cfa1 44d2b574 052fb3fe 0e9f46f8 852ef9be 2c262bde b6276d47 1faf4b92 497cde11 5497f68b 946f8048 61d121d1 7026b3fa 2a2f0419 0fe19a0f
    447  49cdf9f2 6f97297a 27d58fa1 bce1b574 056fb3fe 069b46f8 852af9be a4222bfe 3ee26b4f 29fa2a3b 06f587d1 436bcbab 947f8048 41d561d1 7006b3fa ec2f2c18 0f71ba0b
