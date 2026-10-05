# SHA-256 reduced to 31 steps: a two-block collision search with randomized first blocks

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(C = 2140), policy `paired-lanes-v1`, exploratory lane.

## 1. What is claimed, and what is not

Claim: a randomized algorithm that outputs two distinct 128-byte messages with the same 31-step
SHA-256 digest with probability at least 0.39 over its own coins, using at most 2^48.35
target-compression units in every run. Memory is below 2^38 bytes.

The attack is the two-block collision attack of Li, Liu and Wang (EUROCRYPT 2024, "New Records in
Collision Attacks on SHA-2", Section 4.2) in the single-starting-point form for which they estimate
time 2^49.8, with the memory-efficient matching of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024,
"The First Practical Collision for 31-Step SHA-256"). The local collision in message words
W5..W9, W16, W18 goes back to Mendel, Nad and Schlaeffer (EUROCRYPT 2013). The differential
characteristic, the starting point and the colliding pair used here are theirs. We claim no new
cryptanalysis and no improvement on the published 2^40.5.

What this package adds is a version of that attack that fits this cost model:

- No SAT/SMT solver runs inside the algorithm. One published starting point is used as advice.
- First blocks are drawn from fresh uniform coins, so trials are independent by construction.
- Every test is an exact modular equation on the two messages, so nothing depends on reading a
  bit-condition table correctly. The output is also checked by full re-hashing.
- The trial count and all loops have hard caps. The time bound holds for every run, not on average.
- The acceptance probability under a uniform chaining value is an exact count, 33 * 2^-50.

The remaining premises are three declared heuristics (Section 12): H1 compares the real
chaining-value distribution with the uniform one on two fixed sets, H2 is the success rate of the
final completion search, and H3 is the charge for constructing the advice.

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
d18 = ffff7ffc and no other difference. With the five constants

    c5 = d0018020   c6 = 00000ffa   c7 = ffdf780f   c8 = b00fca02   x18 = 2ffe7fe0

this holds when the following exact conditions hold (each line is one expanded word; a line is
satisfied when the listed differences cancel):

    W16 = s1(W14)+W9+s0(W1)+W0     d16 = d9
    W18 = s1(W16)+W11+s0(W3)+W2    d18 = s1(W16+d16) - s1(W16)        needs W16 in G16
    W20 = s1(W18)+W13+s0(W5)+W4    [s1(W18+d18)-s1(W18)] + [s0(W5+d5)-s0(W5)] = x18 + c5 = 0
    W21 = s1(W19)+W14+s0(W6)+W5    [s0(W6+d6)-s0(W6)] + d5 = c6 + d5 = 0
    W22 = s1(W20)+W15+s0(W7)+W6    [s0(W7+d7)-s0(W7)] + d6 = c7 + d6 = 0
    W23 = s1(W21)+W16+s0(W8)+W7    d16 + [s0(W8+d8)-s0(W8)] + d7 = d16 + c8 + d7 = 0
    W24 = s1(W22)+W17+s0(W9)+W8    [s0(W9+d9)-s0(W9)] + d8 = 0   (W9 is a fixed advice word)
    W25 = s1(W23)+W18+s0(W10)+W9   d18 + d9 = 0

W17, W19 and W26..W30 only involve words without difference. So define the word sets

    V_i = { w : s0(w + d_i) - s0(w) = c_i }  for i = 5,6,7,8,
    G16 = { w : s1(w + d16) - s1(w) = d18 },   G18 = { w : s1(w + d18) - s1(w) = x18 }.

Sizes, by exhaustive enumeration of all 2^32 words (our computation):

    |V5| = 2^14,  |V6| = 2^23,  |V7| = 512,  |V8| = 49408,  |G16| = 64,  |G18| = 42467328.

G16 is the set of 64 words (h << 28) | lo with h in 0..15 and lo in
{031bbffc, 064bbffe, 09b3bffd, 0ce3bfff} (written with h = 0).

Advice (the starting point). The algorithm stores the following state words of the two second
blocks for steps 1..12, and the four message words W9..W12. They are read off the published
colliding pair; Section 13 says how they can be checked.

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

    W9 = eb830a58   W10 = 66add94a   W11 = 9669232d   W12 = 45271fa5   (W'9 = W9 + d9)

The advice is these 37 distinct words plus the ten constants d5..d9, c5..c8, x18: 188 bytes. E_1..E_4 are not part of
it; they are chosen by the algorithm. The starting point has these properties, each a finite
identity between the constants above that anyone can recompute:

- (P1) Steps 9..12 of (1) and (2) hold for both messages with the listed W9..W12, W'9.
- (P2) Equation (2) holds for both messages at steps 5..8, with A_1..A_4 without difference.
- (P3) Step 8 of (1) gives the same E_4 for both messages whenever W'8 = W8 + d8, and E'_5 - E_5 = d5.
- (P4) Step 13 produces no difference: with any W13, E'_13 = E_13 and A'_13 = A_13.
- (P5) A'_10 - A_10 = 00008004, and 00008004 + d18 = 0.

## 4. Phase 1: the table

For a choice of W8 and W7, the starting point determines E_4 and E_3 by steps 8 and 7 of (1):

    E_4 = E_8 - A_4 - S1(E_7) - Ch(E_7,E_6,E_5) - K[8] - W8
    E_3 = E_7 - A_3 - S1(E_6) - Ch(E_6,E_5,E_4) - K[7] - W7

and then A_0 and A_-1 by (2) at steps 4 and 3:

    A_0  = E_4 - A_4 + S0(A_3) + Maj(A_3,A_2,A_1)
    A_-1 = E_3 - A_3 + S0(A_2) + Maj(A_2,A_1,A_0).

The second message must reach its listed states E'_7 and E'_6 from the same E_4, E_3. Writing step 7
and step 6 of (1) for both messages and subtracting gives two exact conditions:

    (F7)  Ch(E'_6,E'_5,E_4) - Ch(E_6,E_5,E_4) = (E'_7 - E_7) - (S1(E'_6) - S1(E_6)) - d7 = fff8701d
    (F6)  Ch(E'_5,E_4,E_3)  - Ch(E_5,E_4,E_3) = (E'_6 - E_6) - (S1(E'_5) - S1(E_5)) - d6 = ffffffd0

A tuple is a pair (W7, W8) with W8 in V8, W7 in V7, (F7) and (F6). Its key is A_-1.

Phase 1 enumerates all 2^32 values of W8, keeps those in V8 that satisfy (F7), enumerates all 2^32
values of W7 to list V7, and tests (F6) on every pair. Results of this exhaustive computation:

- 2048 values of W8 lie in V8 and satisfy (F7);
- there are exactly 16896 = 33 * 2^9 tuples, all with distinct (A_-1, A_0);
- they have 2336 distinct keys; a key has at most 16 tuples (16 keys with 1 tuple, 216 with 2,
  8 with 3, 300 with 4, 8 with 7, 1668 with 8, 8 with 10, 12 with 12, 100 with 16).

The same pass over 2^32 words builds bitmaps of V5, V6 and G18, and a direct-address array KT with
KT[k] = group number of key k, or 0.

## 5. Phase 2: one trial

A trial draws two fresh uniform 256-bit words r0, r1, sets M0 = r0 || r1 (a uniform 512-bit
block), and computes CV = C(IV, M0) = (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4).

    1. g = KT[A_-1]. If g = 0 the trial ends.
    2. For each tuple (W7, W8, E_3, E_4, A_0) of group g:
         E_2 = A_2 + A_-2 - S0(A_1) - Maj(A_1,A_0,A_-1)                 [(2) at step 2]
         W6  = E_6 - A_2 - E_2 - S1(E_5) - Ch(E_5,E_4,E_3) - K[6]       [(1) at step 6]
         if W6 is not in V6: next tuple
         E_1 = A_1 + A_-3 - S0(A_0) - Maj(A_0,A_-1,A_-2)                [(2) at step 1]
         W5  = E_5 - A_1 - E_1 - S1(E_4) - Ch(E_4,E_3,E_2) - K[5]       [(1) at step 5]
         if W5 is not in V5: next tuple
         E_0 = A_0 + A_-4 - S0(A_-1) - Maj(A_-1,A_-2,A_-3)              [(2) at step 0]
         W0  = E_0 - A_-4 - E_-4 - S1(E_-1) - Ch(E_-1,E_-2,E_-3) - K[0]
         W1  = E_1 - A_-3 - E_-3 - S1(E_0)  - Ch(E_0,E_-1,E_-2)  - K[1]
         W2  = E_2 - A_-2 - E_-2 - S1(E_1)  - Ch(E_1,E_0,E_-1)   - K[2]
         W3  = E_3 - A_-1 - E_-1 - S1(E_2)  - Ch(E_2,E_1,E_0)    - K[3]
         W4  = E_4 - A_0  - E_0  - S1(E_3)  - Ch(E_3,E_2,E_1)    - K[4]
         the trial is prefix-valid with (W0..W8) and the advice words W9..W12; go to Phase 3.

Why this is the right prefix. W0..W4 are the unique words that drive the state from CV to the
chosen (A_0..A_4, E_0..E_4): each line is (1) solved for the message word, and the A-equations (2)
at steps 0..4 hold because E_0, E_1, E_2 were defined from them and A_-1, A_0 come from the tuple.
W5 and W6 are the unique words that reach the advice values E_5 and E_6. For the second message,
steps 0..4 are identical. At step 5, E'_5 = E_5 + d5 as required by (P3), and A'_5 follows by (P2).
At step 6, (F6) is exactly the statement that W6 + d6 reaches E'_6; at step 7, (F7) does the same
for W7 + d7 and E'_7; step 8 is (P3); (P2) gives A'_6..A'_8. Steps 9..12 are (P1). So after step 12
both messages are in the advice states, for every prefix-valid trial.

## 6. The prefix-valid set P and its exact measure

Let P be the set of chaining values for which step 2 accepts at least one tuple. P depends only on
(A_-1, A_-2, A_-3). Let U be the uniform distribution on 256-bit chaining values.

Lemma 1. Under U, Pr[CV in P] = 16896 * 2^-32 * 2^-9 * 2^-18 = 33 * 2^-50 (about 2^-44.956).

Proof. Fix a tuple t. Its key is hit with probability 2^-32. Given A_-1, the map A_-2 -> W6 is a
bijection of the 32-bit words (W6 = constant - A_-2), so W6 lies in V6 with probability exactly
|V6|/2^32 = 2^-9. Given A_-1 and A_-2, the map A_-3 -> W5 is a bijection (W5 = constant - A_-3), so
W5 lies in V5 with probability exactly |V5|/2^32 = 2^-18. Hence tuple t accepts a set G_t of
exactly 2^23 * 2^14 pairs (A_-2, A_-3) under its key. Tuples with different keys accept disjoint
sets of triples. For tuples sharing a key the sets G_t could overlap, so we counted the union
exactly: for every key and every A_-2 accepted by at least one of its tuples, we computed the size
of the union of the accepted A_-3 sets. The total is |P restricted to the three words| =
2322167278862336 = 16896 * 2^37, which equals the sum of the |G_t|. So the G_t are pairwise
disjoint, and Pr[CV in P] = 16896 * 2^37 / 2^96. QED.

Two consequences. Every chaining value in P is accepted by exactly one tuple. And the count of
distinct keys alone would give the weaker bound 2336 * 2^-59; the exact union count is what gives
the full 16896.

Lemma 2. Under U, conditioned on (A_-1, A_-2, A_-3, A_-4) with CV in P, the words (W0, W1, W2, W3)
are uniform on 2^128 values.

Proof. With the four A-words and the accepting tuple fixed, E_0, E_1, E_2, E_3 are fixed. Then
W3 = constant - E_-1 - (terms in E_0..E_2), a bijection of E_-1. Given E_-1, W2 is a bijection of
E_-2; given those, W1 is a bijection of E_-3; given those, W0 is a bijection of E_-4. The map
(E_-4, E_-3, E_-2, E_-1) -> (W0, W1, W2, W3) is therefore a bijection, and the four E-words are
uniform and independent of the A-words under U. QED.

## 7. Phase 3: completion with W13, W14, W15

After a prefix-valid trial, W0..W12 are fixed and both messages are in the advice states after
step 12. Put

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

A Phase-3 call also stops, without a result, after 2^18 values of z in total.

What the four conditions mean. By (P4), E_13 = x and A_13 are the same for both messages. (C14)
makes dE_14 = 00008004 = dA_10, which by (2) at step 14 gives A'_14 = A_14. (C15) is step 15 of (1)
with W15 removed from both sides, so E'_15 = E_15 for every W15, and then A'_15 = A_15. (C16) is
step 16 of (1) for both messages with W'16 = W16 + d16, so E'_16 = E_16 and A'_16 = A_16. (C17) is
the only term of step 17 that could differ, so E'_17 = E_17 and A'_17 = A_17. At step 18 the only
differing terms are E_14 and W18, and dE_14 + d18 = 0 by (P5), so E'_18 = E_18 and A'_18 = A_18.
After step 18 the eight state words (A_15..A_18, E_15..E_18) are equal.

The set S. Let S be the set of 32-bit values c18 for which some g in G16 has s1(g) + c18 in G18.
Exhaustive computation over all 2^32 values gives

    |S| = 584683520,   |S| / 2^32 = 0.1361322 (about 2^-2.877).

If c18 is not in S, Phase 3 ends at once. By Lemma 2, under U and given CV in P, c18 is uniform
(for fixed W3 it is a bijection of W2) and so is c16 (a bijection of W0), and the two are
independent. So under U, Pr[c18 in S | CV in P] = |S|/2^32 exactly.

The completion rate. Given c18 in S, the search needs an x with (C14) and (C15) and then a z with
(C16) and (C17). We do not prove that such x and z are found within the caps. This is heuristic H2.
Our simulation: 16777216 samples of uniform (W0..W3) on the advice states, with the caps above;
2282789 had c18 in S (fraction 0.136065, against 0.1361322), and all 2282789 were completed, each
checked by running steps 13..30 for both messages and comparing the states and W19..W30. A
completion took 4117 values of x on average (maximum 69241) and 15 values of z
(maximum 296). The organizer-run experiment `completion` (Section 13) runs the same
routine on the published prefix.

## 8. Correctness of an output

Lemma 3. If Phase 3 succeeds after a prefix-valid trial, then C(CV, M1) = C(CV, M1') for
M1 = (W0..W15) and M1' = M1 with d5..d9 added to words 5..9.

Proof. Message words: W5..W8 lie in V5..V8, W16 = g lies in G16, W18 lies in G18, and W9 is the
advice word, so every line of the expansion table in Section 3 holds: d16 = d9, d18 as stated, and
no difference in W17 and W19..W30. State: Section 5 shows both messages reach the advice states
after step 12. Section 7 shows the eight state words are equal after step 18. Steps 19..30 use
equal states and equal message words. The feed-forward adds the same CV. QED.

The algorithm does not rely on this lemma for its output: it re-hashes both 128-byte messages with
three compressions each, compares the digests, and outputs only on equality (Section 9, step 4).
So a returned pair is always a collision of distinct messages.

## 9. The complete algorithm, with its caps

    Parameters:  N = 238 * 2^40 trials,  Q = 2^20 Phase-3 calls.
    0. Load the advice. Run Phase 1.
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

    q_U >= (33 / 2^50) * (584683520 / 2^32) * 0.99 > 3.95 * 10^-15 > 2^-47.848.

Heuristic H1 says (a) q_D >= q_U / 2, and (b) Pr_D[CV in P] <= 2^10 * 33 / 2^50.

The algorithm fails only if no trial among N wins, or if Q prefix-valid trials occur.

- No win: (1 - q_D)^N <= exp(-N q_D) <= exp(-N q_U / 2). With N = 238 * 2^40 = 2.6168 * 10^14,
  N q_U >= 1.0336, so this is at most exp(-0.5168) < 0.5965.
- Cap Q: the number of prefix-valid trials has mean at most N * 2^10 * 33 * 2^-50 = 238 * 33 =
  7854 by H1(b). By Markov's inequality it reaches Q = 2^20 with probability at most
  7854 / 1048576 < 0.0075.

So Pr[success] >= 1 - 0.5965 - 0.0075 = 0.396 > 0.39. The claim declares 0.39.

Under exact uniformity (q_D = q_U) the success probability would be about 0.64. The factor 2 in
H1(a) is deliberate slack and costs one bit of time. Section 12 gives the sensitivity.

## 11. Cost

Units: one 31-step compression (expansion, 31 steps, feed-forward) costs 1. Every other primitive
operation on 256-bit words (load, store, add, subtract, AND, OR, XOR, NOT, shift, rotation,
comparison, branch, random word) costs 1/2140. A 32-bit rotation is charged as shift, shift, OR,
AND. Additions modulo 2^32 are charged as add plus AND. All bounds below hold for every run.

Data layout. KT is an array of 2^32 words. The bitmaps B5, B6, B18 hold one bit per 32-bit value,
256 bits to a word: 2^24 words each. Each tuple record stores W7, W8, E_3, E_4, A_0 and seven
precomputed constants, one per word: 12 words per record, 16896 records. A 4 x 256-entry table gives s1^-1 one
input byte at a time.

Phase 1 (T1). One pass over the 2^32 words w: membership tests for V5, V6, V7, V8, G18 (each two
evaluations of s0 or s1, at most 14 operations per evaluation, plus add, subtract, compare,
branch: at most 40), the (F7) test (at most 24), three bitmap updates (at most 24) and KT[w] = 0
(2). That is at most 256 operations per w, 2^40 in total. Then 2048 * 512 = 2^20 pairs with at most
64 operations each, and at most 2^10 operations per tuple to fill its record and KT. In total fewer
than 2^41 operations, so T1 < 2^41 / 2140 < 2^30 units.

One trial (always charged in full, whether or not the key is hit). Fixed part: 2 random words,
the compression call with its argument and result moves (8), extraction of A_-1, A_-2, A_-3 (5),
the KT lookup and branch (3), loop counter, comparison and branch (4): at most 32 operations and
one compression. Group part, charged for the largest group of 16 tuples on every trial:

    W6 test:  load kappa_t, subtract A_-2, mask, bitmap index, load, bit select, branch   <= 10
    W5 test:  E_2 = A_-2 + const (3);  Maj(A_0,A_-1,A_-2) = k1 ^ (m1 & A_-2) (4);
              Ch(E_4,E_3,E_2) = k2 ^ (m2 & E_2) (4);  W5 = const + Maj - Ch - A_-3 (5);
              bitmap test (7);  padding (5)                                               <= 28

Here kappa_t, k1, m1, k2, m2 and the two constants are fixed per tuple and stored in its record.
16 * (10 + 28) = 608, so a trial costs at most 1 compression and 640 operations:

    T2 <= N * (1 + 640/2140) = 238 * 2^40 * 1.299066 < 309.18 * 2^40 units.

Phase 3 (T3). One call: computing W0..W4, c16, c18 (at most 256 operations); 64 membership tests
in G18 by bitmap with s1(g) precomputed (at most 12 each); for each g, W14 by 4 table lookups (at
most 24) and at most 2^18 values of x at no more than 96 operations each (two Ch, three S1, the
additions and comparisons of (C14), (C15)); and at most 2^18 values of z per call at no more than
64 operations each. That is at most 64 * 2^18 * 96 + 2^18 * 64 + 2^13 < 2^31 operations, under
2^20 units per call. At most Q = 2^20 calls are made:

    T3 <= 2^40 units.

Final check (T4): 6 compressions and fewer than 2140 operations, at most 8 units.

Advice construction (T0): see H3 in Section 12. T0 = 2^44 units.

Total.

    T1 + T2 + T3 + T4 < 2^30 + 309.18 * 2^40 + 2^40 + 8 < 310.2 * 2^40 < 2^48.278
    T = T0 + T1 + T2 + T3 + T4 < 2^44 + 310.2 * 2^40 = 326.2 * 2^40 < 2^48.35

`time_log2` is 48.35. `preprocessing_log2` is 44.01, a bound on T0 + T1, which is included in the
total.

Memory. KT: 2^32 words. Bitmaps: 3 * 2^24 words. Tuple records: fewer than 2^18 words. Code,
constants, the s1^-1 table, the current block, state and counters: fewer than 2^12 words. Total
below 2^32 + 2^26 words = under 2^37.03 bytes, so `memory_log2_bytes` = 38. KT is written in full
in Phase 1 and the bitmaps are built by stores into zeroed words, whose zeroing (3 * 2^24 stores)
is inside the Phase-1 allowance.

Advice. The stored advice is 188 bytes; `nonuniform_advice_log2_bytes` = 8. The work that
produced it is charged as T0.

## 12. Declared heuristics

H1 (near-uniformity on two fixed sets; score-critical). For a uniform 512-bit block M0 and
CV = C(IV, M0): (a) the probability that a trial wins is at least half of what it is for a uniform
CV; (b) the probability that CV lies in P is at most 2^10 times what it is for a uniform CV.

- Role: (a) gives the success bound; (b) only bounds the chance of hitting the cap Q.
- Why it is weaker than the usual assumption: the source attacks assume the chaining values of
  arbitrary first blocks behave uniformly with respect to these conditions. H1 asks for a factor 2
  in one direction and a factor 1024 in the other, on two explicit sets, and nothing else.
  Independence of trials is not assumed; it holds because the blocks are fresh coins.
- Evidence. (i) Our measurement on the real function: two runs of 2^38 uniform random first
  blocks each, real 31-step chaining values, exact tests. Key hits (a 32-bit condition on A_-1):
  149842 and 148916 observed, 149504 expected under U in each run (combined ratio 0.9992). Hits
  that also pass the W6 test (41 bits of condition): 2115 and 2149 observed, 2112 expected in
  each run (combined ratio 1.0095). Full prefix-valid blocks (59 bits): 1 in the first run and 0
  in the second, against 0.016 expected in total; the block of the first run was not kept, and
  a single event of probability about 1/60 is reported here without drawing a conclusion. (ii) The published
  pair is a chaining value in P that wins, found by the source authors with this matching method
  at the cost their uniform estimate predicted (2^40.5 with a larger table). (iii) The organizer
  verifies that pair and the three derived pairs as certificates.
- Not tested: events of probability 2^-45 and below cannot be sampled. The measurement covers the
  first 41 of the 59 bits of matching condition and says nothing direct about the last 18 bits
  (the W5 test on A_-3) or about c18.
- Sensitivity: if the true ratio in (a) is rho instead of 1/2, the success bound becomes
  1 - exp(-1.0336 * rho) - 0.0075: rho = 0.48 gives 0.384, rho = 1 gives 0.637. Time scales as
  1/rho for a fixed success target. If (b) failed by more than a factor 2^10 the cap term would
  grow in proportion.

H2 (completion rate; score-critical). For a uniform chaining value conditioned on being in P with
c18 in S, the capped search of Section 7, with its fresh offsets, finds (W13, W14, W15) with
probability at least 0.99.

- Evidence: the simulation of Section 7 (all sampled cases completed), and the organizer-run
  experiment `completion`, which executes the same routine on the published prefix for each
  organizer seed and has every returned pair checked as a full collision of the target.
- Limits: the simulation is our own run. The organizer experiment uses one prefix (one value of
  c16 and c18) with varying offsets, so it tests the routine and the caps, not the spread over
  prefixes.
- Sensitivity: a completion rate of 0.9 instead of 0.99 lowers N q_U from 1.0336 to 0.940 and the
  success bound to 0.367; the claimed 0.39 needs a rate of about 0.971 or more at this N.

H3 (cost of constructing the advice; score-critical). The computations that produced the advice
cost at most 2^44 units in total: the search for the 31-step characteristic (Li, Liu, Wang,
EUROCRYPT 2024, Section 4.2) and the collision run of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024)
in which the stored starting point was generated.

- Conversion: one CPU-second of one thread is charged as 2^23 units, that is 2^34.06 word
  operations per second. For comparison, our compiled 31-step compression runs at 5.8 * 10^6 per
  second per thread on the test machine (2^22.5 units per second), so every CPU-second is charged
  as more than a second of pure compression work.
- The collision run. The authors report 1.2 hours on 64 threads for their whole attack, including
  the generation of all their starting points. That is 276480 thread-seconds, charged as
  276480 * 2^23 < 2^41.08 units. Their own figure for one starting point is about 2^31.7.
- The characteristic search. Its run time is not published. We re-ran the authors' public search
  script for 31-step SHA-256 (`find_dc_model_31_256.py` from their repository, unmodified, which
  calls STP with CryptoMiniSat on 26 threads) with STP 2.3.4 and CryptoMiniSat 5.11.21 on a
  32-thread machine. The script lowers a Hamming-weight bound by one per solver call. When this
  package was written, 24 calls had completed and every one had returned a solution. A call took
  between 1960 and 3039 CPU-seconds (158 to 265 seconds of wall time); the 24 calls took 58015
  CPU-seconds in total, with a peak of 5.8 GB of memory. That is 58015 * 2^23 < 2^38.83 units.
- The allowance. 2^44 units is 2^21 CPU-seconds, about 583 thread-hours. After the 2^41.08 charged
  for the collision run, 2^43.8 units remain for the characteristic search: about 32 times the
  CPU time measured so far.
- Limits. The re-run had not finished: the script was still lowering its bound, the final call
  that proves no lower weight exists had not run, and we had not yet compared its output with the
  published characteristic. The public script covers the search for the 31-step characteristic as
  released; the authors may have made other attempts that are not recorded anywhere. The run
  shared the machine with our other computations, which affects wall time, not CPU time. So H3 is
  a measured lower range plus a margin, not a measurement of the historical search.
- Sensitivity of the total: T0 = 2^45 gives 2^48.42, 2^46 gives 2^48.55, 2^47 gives 2^48.78 and
  2^48 gives 2^49.15.

## 13. Evidence and how to check it

Certificates (organizer-verified). `published-pair` is the pair of Li, Liu, Wang, Dong and Sun:

    M0  = 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
          dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
    M1  = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
          9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
    M1' = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
          c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

Its 31-step digest is 55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd, and
C(IV, M0) = c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b 70b1ac59. Running the
second block from this chaining value reproduces every advice word of Section 3 and the constants
d5..d9, c5..c8, x18, which is how they were obtained. `fresh-completion-1..3` keep M0 and W0..W12
and replace (W13, W14, W15) by outputs of Phase 3:

    6df15458 428bbce3 85b249c1     0d0368fe 428bbce3 dfc7b238     f1f288e7 428bbce3 381f59b7

The certificates show that collisions of this shape exist and that Phase 3 produces them. They say
nothing about the cost of finding a first block, and no certificate is used as a cost.

Organizer experiment `completion` (`experiments/completion.py`, kind `python-message-pairs-v1`,
event `full-collision`). For each organizer seed the program derives r13 and r15 from the seed,
runs Phase 3 on the published prefix and returns M0 || M1 and M0 || M1' with the new
(W13, W14, W15). It does not run Phases 1 or 2. Every returned pair is a claimed full collision
that the organizer re-hashes.

Our own computations (not organizer-executed; stated so they can be weighed as such). All were
written in C from the definitions in this document and run on one 32-thread machine:

- the sizes of V5..V8, G16, G18 and S, each by a loop over all 2^32 words;
- the table: 2048 values of W8, 16896 tuples, 2336 keys, and the group sizes;
- the exact union count of Lemma 1 (2^35.05 accepted (key, A_-2) pairs examined);
- a full run of the trial procedure of Section 5 on the published first block, which returns the
  published W0..W12 from the advice alone, with exactly one accepting tuple;
- the completion simulation of Section 7 and the matching measurement quoted under H1.

Our counts |V5| = 2^14, |V6| = 2^23, |V7| = 512, |V8| = 49408 differ from the figures 2^14, 2^23,
2^27, 2^25 quoted in the source paper for W5..W8. Ours are for the exact modular conditions of
Section 3 with these difference constants, and they are the ones the algorithm uses. Our completion
density 0.136 (2^-2.88) is also lower than the paper's estimate of 2^-1.3 from 100 tests. We use
our own figures throughout; they make the claimed cost higher, not lower.

## 14. Scope and limitations

- This is an application of published cryptanalysis with new accounting. The characteristic, the
  starting point and the pair come from the cited authors.
- The attack was not executed at full scale. No first block was found by us. The bound of
  2^48.35 rests on H1, H2 and H3.
- With several starting points the source attack reaches 2^40.5. We do not claim that figure
  because generating starting points needs a SAT/SMT solver whose cost we cannot state in this
  model with evidence.
- The time bound is a cap on every run. Only the success probability depends on H1 and H2.
- A passing exploratory review is an AI screening result, not a proof and not human acceptance.
