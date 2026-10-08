# sha256-r37: the 37-step collision attack of ePrint 2026/1120, fully charged

## 0. Claim

Track `sha256-r37-exploratory`, target `sha256-r37-prefix-v1`, attack class `ordinary-collision`, cost model
`collision-frontier-v5` with C = 2644: one 37-step compression (with feed-forward) is 1 unit, any other primitive
256-bit word operation is 1/2644 unit.

The algorithm of Section 5 outputs two distinct 128-byte messages M0||M1 and M0||M1' with equal sha256-r37 digests:
standard IV, FIPS 180-4 padding (an identical third block), steps 0..36 on every block, feed-forward, all 256 bits.

| Field | Claimed | Computed |
|---|---|---|
| time_log2 | 78.59 | total 2^78.5830 units (Section 7) |
| preprocessing_log2 | 70.01 | the advice allowance, a fresh Step-1 run, the enumeration of S (Section 7) |
| success_probability | 0.39 | >= 0.3923 with every measured count at an exact one-sided bound, jointly at least 95% (Section 6) |
| memory_log2_bytes | 16 | fewer than 2^16 bytes (Section 8) |
| nonuniform_advice_log2_bytes | 12 | the characteristic tables and the Step-1 words, 2,892 bytes (Section 8) |

No certificate is attached. The claim is the cost of the stated algorithm, not a found pair. The time bound holds on
every coin sequence: the number of first-block trials is fixed, and all data-dependent work runs under hard caps.

Heuristics:
- H1: the published characteristic and Step-1 words are used as printed, with one reading explained in Section 2;
- H2: the measurement model is the attack's distribution, and first-block trials are independent;
- H5: the product of the pooled per-step rates is not above the true probability of steps 16 onward;
- H3: the operation counts;
- H4: the allowance for the search that produced the advice.

### 0.1 Sources and credit

- **The attack.** Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian and Jinwei Zhu, "Pushing Collision
  Attacks on SHA-2 to 39 Steps", IACR ePrint 2026/1120 (revised 2026-09-09). From it come the 37-step characteristic
  (Table 15), the extra conditions (Table 16), the SFS colliding pair (Table 17), and the three-step attack and its
  complexity analysis (Section 4.2, "Application to 37-step SHA-2").
- **The framework it instantiates.** Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision
  Attack Framework for SHA-2", CRYPTO 2026 (ePrint 2026/1080). Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First
  Practical Collision for 31-Step SHA-256", ASIACRYPT 2024. Y. Li, F. Liu, G. Wang, "New Records in Collision Attacks
  on SHA-2", EUROCRYPT 2024 (the SAT/SMT characteristic tool).
- **Ledger conventions** follow the promoted sha256-r32 package: first-block trials at 1 unit plus counted operations,
  hard counters on data-dependent work, and measured rates as declared heuristics.
- **Our own work:**
  - the machine-checked transcription;
  - the exact enumeration of the Step-3 set S;
  - the measurement of the Step-2 rate and of every condition after step 15;
  - the operation counts and the ledger.

  All code is in Appendix A and all outputs in Appendix B.

## 1. Target and notation

Words are 32-bit; `+` and `-` are mod 2^32. Sigma0, Sigma1, sigma0, sigma1, IF (choose) and MAJ are as in FIPS 180-4.
We use the paper's alternate state description. A chaining value is (A_-1, A_-2, A_-3, A_-4, E_-1, E_-2, E_-3, E_-4) =
(a, b, c, d, e, f, g, h). Step i = 0..36 computes

    E_i = A_(i-4) + E_(i-4) + Sigma1(E_(i-1)) + IF(E_(i-1), E_(i-2), E_(i-3)) + K_i + W_i
    A_i = E_i - A_(i-4) + Sigma0(A_(i-1)) + MAJ(A_(i-1), A_(i-2), A_(i-3))

with W_i = M_i for i < 16 and W_i = sigma1(W_(i-2)) + W_(i-7) + sigma0(W_(i-15)) + W_(i-16) otherwise. The output is the
feed-forward (A_(r-1) + A_-1, ..., E_(r-4) + E_-4).

A collision of the second-block compression from a common chaining value CV1 = f(IV, M0) gives a collision of the
128-byte messages. The third (padding) block is the same for both, and so is its input.

Notation: the first block is M0 = (M0_0, ..., M0_15). The second-block words are W0..W15 (unprimed message M1) and
W0'..W15' (M1').

## 2. Characteristic and conditions (paper Table 15 and Table 16)

Columns are the signed differences of A_i, E_i and W_i, bit 31 first. Symbols:
- `=` equal bits; `u` means (x, x') = (1, 0); `n` means (0, 1); `0` and `1` fix both bits.
- The paper prints `+` at 20 positions of E. Each marks an equality with the same bit of the adjacent row:
  E5[6] = E6[6], E5[7] = E6[7], E8[25] = E9[25], E9[0] = E10[0], E9[14] = E10[14], E13[17] = E14[17], E13[30] = E14[30], E15[4] = E16[4], E16[15] = E17[15], E16[24] = E17[24]. Those at index 16 or more also appear in Table 16.
- The unprimed message is the one whose bits read as printed. In the paper's SFS pair this is M' (Section 3).
- The rows carry 396 non-`=` symbols.

```
  i  nabla A                           nabla E                           nabla W
 -4  ================================  ================================  
 -3  ================================  ================================  
 -2  ================================  ================================  
 -1  ================================  ================================  
  0  ================================  ================================  ================================
  1  ================================  ================================  ================================
  2  ================================  ================================  ================================
  3  ================================  ================================  ================================
  4  ================================  000=============================  ================================
  5  ================================  111=0=====1==0=====01===++01====  ================================
  6  =nu=============================  uuu=1011=00=10111=0111=0++1011==  ==n=============================
  7  ==========n====n====n======n====  10n=u01001n00n00010nu110unuu0001  =====u===u==========n===========
  8  ================================  011=1n+1=n11u1101=001u1u1010=u=1  ==u=============================
  9  ================================  1=0110+=001=1100=+110100111u=0=+  =====u=u=======n===u==n=u=n=u=n=
 10  ======u===========u=============  10n001u110101==01+u1101011=1110+  ============n======u=n==========
 11  ====u=====u=========u=n====u==n=  =01un000011101=n0n0u1uu101011u1u  ================================
 12  =nu=============================  01101uuuuunu010110110n1u0u0uu0n0  ================================
 13  ====u=========u=u=======n==u====  0+10n110111unn+0n101110110001001  ================================
 14  ======u=n=======n===============  =+0=1000000111+=1==1n010u0=0101=  =0===u===n=1=1====1=u=1=====1=1=
 15  ================================  =u==01===n=011n01==u0=u=1==+====  ==u=============================
 16  ==u=============================  =0=====+00===11=+==01=0=0==+====  ================================
 17  ================================  =0=====+01===u1=+==0==1===1u====  ================================
 18  ================================  ==10===uu====0==n===111===01==1=  ================================
 19  ================================  ==1====00====1==0==========1====  ================================
 20  ================================  ==u====10=======1===00==========  ================================
 21  ================================  ==0=============================  ================================
 22  ================================  ==1=============================  =====0=nn=====1=u=1=============
 23  ================================  ================================  ================================
 24  ================================  ================================  ==n=============================
 25  ================================  ================================  ================================
 26  ================================  ================================  ================================
 27  ================================  ================================  ================================
 28  ================================  ================================  ================================
 29  ================================  ================================  ================================
 30  ================================  ================================  ================================
 31  ================================  ================================  ================================
 32  ================================  ================================  ================================
 33  ================================  ================================  ================================
 34  ================================  ================================  ================================
 35  ================================  ================================  ================================
 36  ================================  ================================  ================================
```

**Two-bit conditions (Table 16)**, the 31 relations as used, where X[j] is the bit of weight 2^j:

- A15[15] != A16[15]
- A15[23] = A16[23]
- A15[25] = A16[25]
- A16[9] != A16[20]
- A16[18] != A16[6]
- A16[8] = A16[17]
- A16[29] != A17[29]
- A17[29] = A18[29]
- E15[4] = E16[4]
- E17[0] != E17[13]
- E16[24] = E17[24]
- E16[15] = E17[15]
- E18[6] != E18[19]
- E18[2] = E18[20]
- E20[2] != E20[16]
- W6[1] = W6[12]
- W6[8] != W6[25]
- W6[14] = W6[18]
- W7[0] = W7[28]
- W7[9] = W7[30]
- W7[1] = W7[18]
- W8[1] != W8[12]
- W8[8] != W8[25]
- W8[14] = W8[18]
- W22[31] != W22[1]
- W22[30] != W22[0]
- W22[16] != W22[25]
- W22[14] != W22[21]
- W24[4] != W24[6]
- W24[22] = W24[31]
- W24[20] != W24[27]

One printed relation needs a reading:

- orientation: A16[29] = A17[29] holds on the primed message (a differing bit); on the unprimed one it reads A16[29] != A17[29]

  The two forms say the same thing: A_17[29] = 0.

With this reading, every symbol and relation holds on the paper's SFS pair (Section 3).

**Message differences.** Nonzero only in (W6, ..., W10, W14, W15, W22, W24).

**Condition counts per step** (value symbols of A_t, E_t, W_t plus relations whose highest index is t), next to the
measured pass rate of step t (pooled over the stage measurement of Section 6):

| step | printed conditions | pooled measured rate |
|---:|---:|---:|
| 16 | 17 | 2^-17.014 |
| 17 | 13 | 2^-13.005 |
| 18 | 15 | 2^-15.000 |
| 19 | 6 | 2^-6.007 |
| 20 | 7 | 2^-7.007 |
| 21 | 1 | 2^-1.002 |
| 22 | 11 | 2^-10.990 |
| 23..36 | 4 | 2^-4.125 (natural, 272 of 4747) |

The printed conditions after step 15 total 74; the paper states 75. Our count is one lower than the paper's; the claim uses the measured rates, not either count.

## 3. Exact checks of the transcription and of steps 14-15

1. **Transcription.** We recompute the paper's SFS pair from its printed words; both messages hash to the printed
   value. In the stated orientation every symbol of rows -4..36 holds. With the readings of Section 2 every
   relation holds too: 0 failures. With the printed relation there is exactly 1 failure. In the opposite orientation
   more than 100 symbols fail. See `verify_sfs.py` and its output in Appendix B.
2. **Steps 14 and 15.** The enumeration of S (Section 5.1) tests exact pair values, not only the printed symbols:
   - the signed differences of A and E at steps 14 and 15, computed for both messages;
   - the modular differences that step 16 needs from (A, E)_13..15: the Sigma1/IF part of E_16 and the Sigma0/MAJ part
     of A_16;
   - every expanded word W_t whose required modular difference involves sigma of a differing word only among W8..W15.

   Without the step-16 modular-difference requirements the set has 4,096 elements (`NOS16=1 exp S` in Appendix B); with them it has 32, the paper's 2^5.
3. **Steps 16 and later.** These are measured as rates (Section 6), with the full pair test of every step: the value
   symbols, the relations, and the exact signed differences of A_t, E_t and W_t of both messages.

## 4. The attack (paper Section 4.2, "Application to 37-step SHA-2"), and what we take from it

- **Step 1.** Fix second-block values (A_i)_(0..13), (E_i)_(4..13) and (W_i)_(8..13) that meet every condition up to
  step 13. The paper finds such values with a SAT solver at about 2^41.3 compression calls. We take them from the
  second block of the paper's SFS pair (Table 17). That pair meets every condition, so these 30 words form a valid Step-1
  solution.

  **These words are nonuniform advice, not a free input.**
  - They come out of the authors' complete SFS search, not from a generic Step-1 run, and S, q2 and G are measured
    for these exact words. So the cost that produced them is the authors' whole search for the characteristic and
    the SFS pair. The cost model requires all advice and any search omitted from the program to be accounted for
    (collision-frontier-v5, nonuniform_advice).
  - We charge that search by an allowance of 2^70 units (H4, Section 7). The paper's Table 1 lists SFS
    collisions at 38 and 39 steps (from earlier works) as practical, and the paper prints its own 37-step SFS pair
    (Table 17); its Step 1 alone costs 2^41.3 calls.
  - We also charge 4 x the paper's Step-1 SAT cost on its own line. This is a voluntary overcharge, not a step the
    algorithm runs.
  - What is shared with the published pair:
    - every output shares the second-block words W8..W13 with the paper's SFS pair, and W14, W15 come from the
      enumeration of S, whose elements include the pair's own;
    - the pair's chaining value and its W0..W7 are never used.
  - Our CV1 = f(IV, M0) comes from the standard IV and a fresh first block. So the output is a new ordinary
    collision of the target, which the SFS pair does not contain. The SFS pair is not a collision of the target,
    because its chaining value is not the IV. No collision of the target, published or not, is used.
- **Step 2.** Try first blocks M0. With CV1 = f(IV, M0), steps 0..3 run backwards from the fixed A_0..A_3 and E_4..E_7.
  This gives E_3..E_0 and then W7..W0. The only conditions that depend on CV1 are on W6 and W7; a first block is valid
  when they hold.
- **Step 3.** For a valid first block, try every (W14, W15) in the set S and test the conditions after step 15. A pair
  that passes every step is a collision.

## 5. The algorithm, with operation counts

### 5.1 Precomputation

The Step-1 words (hex):

```
A_0..A_13: 1b21ce20 62827866 987f24c4 44294b96 a8ccc9b3 a26653f8 210c2860 7246d008 7c4a1e59 edc43977 030eaaa0 1ae4bc99 2fd3ea18 9992b350
E_4..E_13: 1b2d044e e7f2c81f eb0b9c2d 9a404eb1 7b3e8fa7 9a3c74f0 87a8fadc b0741f5f 6fd5b358 66f25d89
W_8..W_13: bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc
```

**The set S.** Fix the Step-1 words. Then E_14 = c14 + W14 and A_14 = E_14 + d14 for constants c14 and d14 of those
words; step 15 is the same with W15. Enumerate:
- E_14 over the bits that carry no condition, keeping the values that meet step 14 (exact pair values) and the
  expansion rule of Section 3;
- for each kept E_14, E_15 over its free bits, keeping the values that meet step 15, the step-16 modular-difference
  requirements and the remaining expansion rules.

S is the list of resulting (W14, W15); every element has W14 = bd1d3f7b. Exactly 32 values:

```
bd1d3f7b fdb41680
bd1d3f7b fdb41681
bd1d3f7b fdb416a0
bd1d3f7b fdb416a1
bd1d3f7b fdb41a80
bd1d3f7b fdb41a81
bd1d3f7b fdb41aa0
bd1d3f7b fdb41aa1
bd1d3f7b fdb43680
bd1d3f7b fdb43681
bd1d3f7b fdb436a0
bd1d3f7b fdb436a1
bd1d3f7b fdb43a80
bd1d3f7b fdb43a81
bd1d3f7b fdb43aa0
bd1d3f7b fdb43aa1
bd1d3f7b 7dd41680
bd1d3f7b 7dd41681
bd1d3f7b 7dd416a0
bd1d3f7b 7dd416a1
bd1d3f7b 7dd41a80
bd1d3f7b 7dd41a81
bd1d3f7b 7dd41aa0
bd1d3f7b 7dd41aa1
bd1d3f7b 7dd43680
bd1d3f7b 7dd43681
bd1d3f7b 7dd436a0
bd1d3f7b 7dd436a1
bd1d3f7b 7dd43a80
bd1d3f7b 7dd43a81
bd1d3f7b 7dd43aa0
bd1d3f7b 7dd43aa1
```

For each element of S we precompute E_14, A_14, E_15, A_15, sigma1(W14), and the step-16 parts that do not depend on
M0. The Step-2 tests use constants built from the Step-1 words.

### 5.2 Step 2: first-block trials

Every first block is 16 fresh independent uniform words, taken from two fresh random 256-bit words. So the trials are
independent by construction, and q2 was measured on exactly these blocks (Section 6). One trial, with its counted
operations:

```
M0 <- 16 words from two fresh random 256-bit words (2 draws, 16 shift+mask)   34
(A_-1, A_-2, ...) <- f37(IV, M0)                                               1 unit
E3 <- A_-1 + k3        k3 = A_3 - Sigma0(A_2) - MAJ(A_2, A_1, A_0)               1
W7 <- k7 - E3          k7 = E_7 - A_3 - Sigma1(E_6) - IF(E_6, E_5, E_4) - K_7     1
value symbols of W7: (W7 AND m7) = v7, branch                                     3
three relations of W7: 2 shifts, XOR, AND 1, compare, branch each                 18
E2 <- A_-2 + k2 - MAJ(A_1, A_0, A_-1)        k2 = A_2 - Sigma0(A_1)              6
W6 <- k6 - E2 - IF(E_5, E_4, E3)             k6 = E_6 - A_2 - Sigma1(E_5) - K_6  5
value symbol and three relations of W6                                            21
loop compare and branch                                                           2
total ordinary operations                                    91, charged 128
```

### 5.3 Step 3 on a valid first block

```
E1 <- A_1 + A_-3 - Sigma0(A_0) - MAJ(A_0, A_-1, A_-2)                          21
E0 <- A_0 + A_-4 - Sigma0(A_-1) - MAJ(A_-1, A_-2, A_-3)                          21
W5..W0: W_i = E_i - A_(i-4) - E_(i-4) - Sigma1(E_(i-1)) - IF(...) - K_i, 6 x 25 150
store M1 words W0..W7 and CV1 for the output                                       16
W16 <- W9 + sigma0(W1) + W0 + sigma1(W14) (one W14 value in S)                    17
every element of S (32), step 16 without early exit, recording the passing elements:
  E_16 <- e_s + W16; value symbols of E_16                                       4
  A_16 <- E_16 + a_s; value symbol of A_16                                        4
  seven relations whose highest index is 16 (6 each)                             42
  record pass (store index, count m)                                              3
  loop                                                                            2
  per element 55, all 32: 1760
total per valid first block                                  1985, charged 2048
every passing element (rare: about one valid first block in 2^12 has one) is
continued on its own: steps 17..36 for both messages (W expansion 31, E 25,
A 24 per message-step), full pair test of each step (value symbols, exact XOR
differences, relations: at most 130)                         <= 20 x 290 = 5800, charged 8192
```

### 5.4 Stopping, caps and output

- N = 2^78.51 first-block trials, fixed in advance. The first collision is output (two 128-byte messages) after
  verification by six full compressions.
- **Cap on valid first blocks.** At most V = 1.02 N 2^-10 valid first blocks are processed. The expected number is
  2^68.51. The 2% slack is many standard deviations of both the count and the q2 estimate (standard error
  below 0.1%), so the cap binds with negligible probability (below 2^-100).
- **Cap on Step-3 continuations.** At most 2 x 2^56.50 + 2^20 = 2^57.50 step-16 survivors
  (element and first block) are continued. Their expected number is N q2 |S| x 2^-17.014, and the cap binds with
  probability below 2^-100. N, V and this cap are integers: each is the ceiling of the stated value.

Reaching a cap stops the run without output, and this counts as failure in Section 6. So the ledger of Section 7 holds
on every coin sequence. The two cap statements use the point estimates of q2 and of the step-16 rate; their margins
are 20 or more standard deviations of those estimates.

## 6. Success probability (heuristic H2)

**Why the measurement model is the attack's distribution.** Fix the Step-1 words. The map from CV1 to (W0, ..., W7)
is one-to-one (Section 5.2):
- A_-1 fixes E_3 and W7;
- A_-2, given A_-1, fixes E_2 and W6;
- A_-3 fixes E_1 and W5;
- A_-4 fixes E_0 and W4;
- E_-1..E_-4 fix W3..W0.

If CV1 is uniform, W0..W7 are uniform. A valid first block (Step 2) then has W6 and W7 uniform on their conditioned
sets and W0..W5 uniform.

The measurement draws exactly this:
- W6 and W7 are drawn from their conditioned sets.
- Steps 16..21 get fresh W16..W21 directly. For fixed other words, W_(t-16) = W_t - sigma1(W_(t-2)) - W_(t-7) -
  sigma0(W_(t-15)) is one-to-one, so this is the same as uniform W0..W5, and W0..W5 are back-solved at the end.
- (38 steps only: W7 is also redrawn there, with W6 re-solved to keep W22. The 37-step run uses only the W6 redraw.)

The remaining premise is that CV1 = f(IV, M0) over the first-block family behaves as uniform for these conditions. It
is supported by the Step-2 rate (2^-9.999 against its bit count), by the natural Step-3 run on real first
blocks (Section 9), and by the organizer experiment (Section 9).

**Step 2 rate.** 2,097,970 of 2,147,483,648 first blocks were valid. Each first block was 16 fresh independent uniform words,
exactly as the attack draws them (Section 5.2): q2 = 2^-9.999.

**Exact bounds.** Every rate in this section is bounded by an exact one-sided Poisson (Garwood) lower bound on its
count, at level 0.00500 each. That is 0.05 split over the 10 bounded quantities (Bonferroni), so all bounds
hold jointly with confidence at least 95%. No normal approximation is used for any claimed figure.

| quantity | count | trials | point | exact lower bound |
|---|---:|---:|---:|---:|
| q2 | 2,097,970 | 2,147,483,648 | 2^-9.999 | 2^-10.002 |
| step 16 | 64,909 | 8,589,934,592 | 2^-17.014 | 2^-17.028 |
| step 17 | 55,534 | 456,654,848 | 2^-13.005 | 2^-13.021 |
| step 18 | 222,908 | 7,304,380,416 | 2^-15.000 | 2^-15.008 |
| step 19 | 80,957 | 5,208,064 | 2^-6.007 | 2^-6.021 |
| step 20 | 40,497 | 5,208,064 | 2^-7.007 | 2^-7.025 |
| step 21 | 162,494 | 325,504 | 2^-1.002 | 2^-1.012 |
| step 22 | 1,310,913 | 2,666,528,768 | 2^-10.990 | 2^-10.993 |
| steps 23..36 (natural) | 272 | 4,747 | 2^-4.125 | 2^-4.359 |

**Steps 16..36 (H5).** P is the probability that a uniformly chosen element of S passes steps 16..36 on a
valid first block. The stage run measures it step by step:
- a start draws an element of S and W6, W7;
- at each step t up to 22 the state gets a fixed number D_t of fresh draws (D_16 = 2^20, D_17 = 2^16, D_18 = 2^20, D_19 = 2^10, D_20 = 2^10, D_21 = 2^6, D_22 = 2^19), each with the full pair
  test of step t, and continues with its first passing draw;
- after step 22 the remaining steps run naturally, and the last test is the exact collision test of both
  messages.

The claim uses the product of the pooled per-step pass rates. Each rate is the passes over the draws at step t, over
the states that reached it. The product is P = 2^-74.151, with exact joint lower bound **P >= 2^-74.467**
(the product of the bounds above).

H5 is the premise that this product is not above the true probability. The per-start estimator from the same runs
is a cross-check: the mean over starts of each start's product of pass fractions times its final collision indicator.
It is unbiased, and it gives 2^-73.961, 0.19 bit above the pooled product. 3,445 of the 8192 starts (first run) reached a state where none of its D_t draws passed (by step: 16: 1224, 17: 2, 18: 1880, 22: 339), more than a uniform rate would leave, so pass rates vary between states (at step 16, through the element of S). The estimator counts these starts as zero.

**Clustering of draws.** The draw-level Poisson bounds treat every draw as an independent trial, but the draws at one
state share that state, and pass rates vary between states. The cluster-level check treats starts as the
independent units: the per-start mean minus 2.58 standard errors (the same one-sided level, relative standard
error 0.093) is 2^-74.358. That is above the claimed bound 2^-74.467, so the claimed P bound also holds
at the level of starts. This is part of H5.

**Elements of S.** Step 3 continues every step-16 survivor, so its success is at least
g = (A_1 + ... + A_|S|)/m pointwise, where A_s = 1 when element s leads to a collision and m is the number of step-16
survivors. Hence G = E[g] >= |S| x P x E[1/m | a collision]. At the 272 stage-run collisions, re-testing every element of S on the collision's own back-solved first block gave m = 2 in 7 cases and m = 1 otherwise. With the exact upper bound 17.1 on that count, E[1/m | a collision] >= 1 - 17.1/(2 x 272) = 0.9685. So G >= 2^-69.513.

**One trial.** It succeeds with probability p >= q2 x G >= 2^-10.002 x 2^-69.513 = 2^-79.515.

**N trials.** With N = 2^78.51, N p >= 0.4982, so success is at least

    1 - exp(-N p) - (two caps) 2 x 2^-100 >= 0.3923 >= 0.39.

At the point estimates the same N gives success 0.469.

**Against the paper.** The paper's 2^79.1 is an expected time from q2 = 2^-9, |S| = 2^5 and
75 conditions. Our measured inputs give an expected 2^79.17 trials. That is close to the paper's figure. q2 is one bit worse than the paper's (2^-10.000 measured against 2^-9: W6 carries one value symbol and three relations, four conditions in all). The steps after 15 are about one bit easier than the paper's count of 75. The claim lies below the expected time because the cost model asks for success 0.39, which needs 0.494/p trials.

## 7. Time ledger (exact)

| term | basis | units | log2 |
|---|---|---:|---:|
| first-block trials (Step 2) | N x (1 unit + 128 ops) | 2^78.5782 | 78.578 |
| valid first blocks (Step 2 tail and Step 3 first stage) | cap V = 1.02 N 2^-10, 2048 ops each | 2^68.1701 | 68.170 |
| Step 3 continuations (first blocks with a step-16 survivor) | cap 2^57.50, 8192 ops each | 2^59.1282 | 59.128 |
| collision verification | 6 compressions + 64 ops | 2^2.5908 | 2.591 |
| fresh Step-1 run (voluntary overcharge; the advice itself is charged by the allowance below) | 4 x the paper's Step-1 cost 2^41.3 calls of 64-step SHA-256, x 64/37 to 37-step units | 2^44.0905 | 44.091 |
| nonuniform advice: the authors' search for the characteristic and the whole SFS pair (H4) | allowance 2^70 | 2^70.0000 | 70.000 |
| enumeration of S and constants | bound | 2^24.0000 | 24.000 |
| **total** | | | **78.5830** |

The claim is time_log2 = 78.59, rounded up. Preprocessing is the Step-1 charge, the allowance and the
enumeration bound (preprocessing_log2 = 70.01); all are inside the total.

**The advice allowance (H4).** The characteristic and the SFS pair, whose second block gives our Step-1 words, were
found by the authors' SAT/SMT search. The paper does not report its running time. A comparable search was re-run and measured for the promoted
r32 package: the four-step search for the CRYPTO 2026 35-step characteristic took 593,858 CPU-s, and a factor 32
covers blind re-derivation (2^45.9 units at that package's price). The paper's Table 1 lists SFS collisions at 38
and 39 steps as practical. We charge 2^70 units for the authors' whole search, far above both. The Step-1 words are charged separately as well, on their own
ledger line.

**Sensitivities** (each changes only the stated item):

| change | total |
|---|---:|
| none (the claim) | 2^78.5830 |
| steps >= 16 at the paper's printed-condition count 75 (times |S|) instead of the measured bound | 2^79.0719 |
| steps >= 16 two bits harder than the measured bound | 2^80.5802 |
| all inputs at their point estimates instead of the exact bounds | 2^78.2440 |
| every first-block trial at 2 units (twice the compression) | 2^79.5470 |
| advice allowance 2^74 instead of 2^70 | 2^78.6384 |

## 8. Memory and advice

The counted program holds, in 256-bit words:
- the Step-1 words and derived constants: under 128;
- S and its per-element constants: 32 x at most 8;
- the first block and chaining value: 24;
- two second-block states for the continuation test: under 256;
- registers and counters: under 64.

Its nonuniform data is 2,892 bytes:
- the condition masks of every row (value mask, value and XOR difference of A, E and W);
- the relation table;
- the 30 Step-1 words;
- the round constants.

Code is far below 2^14 bytes, and the total is below 2^16 bytes. We claim memory 16 and advice 12. Memory is a
reported metric only.

## 9. Evidence (participant runs; code in Appendix A, outputs in Appendix B)

- **Transcription:** `verify_sfs.py` checks the transcription against the paper's SFS pairs (Section 3); the output
  is `verify.txt`.
- **Step-2 derivation:** `check_step2.py` is an independent Python check. For 2000 random first blocks it derives
  E_0..E_3 and W0..W7 from CV1, runs the second block forward, and confirms that steps 0..13 reproduce the Step-1
  values every time.
- **S:** `exp S` and `exp LIST` enumerate S exactly, and `NOS16=1 exp S` gives the count without the step-16
  requirements (`s37.txt`). The SFS pair's own (W14, W15) is in S.
- **Step 2 and natural Step 3 (`run37.txt`):** real first blocks run through the 37-step compression and Step 2.
  Step 3 then runs over S with the full pair test at every step, and the run prints the marginal pass rate of every
  step-16 condition.
- **Organizer experiment** (`experiments/attack37.py`, id `attack37-early-stages`): It draws, per organizer trial, independent uniform first blocks and re-measures q2, the W16-only conditions, the E16 value symbols and the full step-16 pair test for every element of S, and on trial 0 re-checks S at steps 14-15 and the transcribed SFS pair. Its returned pair is a masked digest match that the organizer re-hashes, which confirms the program evaluates the target. Pre-registered: Pre-registered predictions for 256 trials x 128 independent uniform first blocks (32,768 blocks): (1) the checked 12-bit mask event succeeds in about 220.8 of 256 trials (birthday among 128 digests; 99.9% interval [202, 238]); (2) valid first blocks (Step 2) total about 32, 99.9% interval [13, 51] for q2 = 2^-10; (3) among valid blocks x |S| = 32, W16 carries no condition, so w16 equals |S| x valid exactly and the E16 value symbols pass about 2.0 times (interval [0, 8]); (4) trial 0 reports s_steps14_15_ok = s_size = 32 and sfs_pair_collides = 1. pair16 (the full step-16 pair test) is expected near 0.01 in total and is not reached at sandbox scale for 37 steps. A participant run of the same program on 256 local seeds took 3.9 s and gave: valid 35, w16 1120, e16 0, pair16 0, masked pairs 217 of 256, trial-0 checks passed.
- **Stages (`stage37.txt` and any further runs):** `exp STAGE` with fixed draws (Section 6). 
- **End-to-end:** the stage run's starts that collide under their own chaining value are 37-step semi-free-start
  collisions produced by our code. One is printed here and re-verified independently in Python:

```
CV  84b03532 883efbcd bcc9750d d8840cb1 d5ef51d6 f8e65cf6 d9803e4c 3c2a6b0b
M   d83b70ec 1f3acdd5 de31cee0 606e69d1 02c4b47b 8b96f2f8 5c6cf59e 4de6c646 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd436a1
M'  d83b70ec 1f3acdd5 de31cee0 606e69d1 02c4b47b 8b96f2f8 7c6cf59e 49a6ce46 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd436a1
```

These runs were made on an Apple M5 Pro with 12 threads; the seeds are in the commands. They are participant
evidence. The organizer experiment above re-measures the early stages; the deep stages need minutes of 12-thread C
and are beyond the sandbox.

## Appendix A. Code

### sha2char.py (SHA-256 b84435dc670cfa9e)

```
"""SHA-256 step-reduced compression in the alternate (A, E) description of ePrint 2026/1120, its 37/38-step
characteristics (Tables 15/3), extra conditions (Tables 16/4) and SFS pairs (Tables 17/5), and condition checks."""
import re

M32 = 0xFFFFFFFF
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M32


def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def IF(x, y, z): return ((x & y) ^ (~x & z)) & M32
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)


def expand(m, r):
    w = list(m)
    for i in range(16, r):
        w.append((s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & M32)
    return w


def run(cv, m, r):
    """returns (A, E, W) dicts indexed -4..r-1 (W 0..r-1) and the feed-forward output"""
    A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3]}
    E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
    W = expand(m, r)
    for i in range(r):
        E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + K[i] + W[i]) & M32
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M32
    out = [(A[r - 1 - j] + cv[j]) & M32 for j in range(4)] + [(E[r - 1 - j] + cv[4 + j]) & M32 for j in range(4)]
    return A, E, W, out


def parse_tables(txt, title, r):
    """characteristic rows i -> (A, E, W) symbol strings (bit 31 first)"""
    i0 = txt.index(title)
    rows = {}
    for line in txt[i0:].split('\n')[2:]:
        m = re.match(r'^(-?\d+) ([=nu01+]+)$', line.strip())
        if not m:
            if rows and int(max(rows)) >= r - 1:
                break
            continue
        i, s = int(m.group(1)), m.group(2)
        if i < 0:
            assert len(s) == 64, (i, len(s))
            rows[i] = (s[:32], s[32:], None)
        else:
            assert len(s) == 96, (i, len(s), s)
            rows[i] = (s[:32], s[32:64], s[64:])
        if i == r - 1:
            break
    assert sorted(rows) == list(range(-4, r)), sorted(rows)
    return rows


def parse_extra(txt, title, nexttitle):
    """extra two-bit conditions: list of (lhs word, lhs bit, op, rhs word, rhs bit) with op '=' or '!='"""
    seg = txt[txt.index(title):txt.index(nexttitle)]
    seg = seg.replace('̸=', '!=').replace('≠', '!=')
    conds = []
    for m in re.finditer(r'([AEW])\s*(\d+)\[\s*(\d+)\]\s*(!=|=)\s*([AEW])\s*(\d+)\[\s*(\d+)\]', seg):
        conds.append((m.group(1), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5), int(m.group(6)), int(m.group(7))))
    return conds


def check_pair(rows, extra, X, Xp, r, wmin=0):
    """X, Xp: (A, E, W) of the unprimed / primed message. Returns list of failures."""
    bad = []
    for i in range(-4, r):
        for col, name in ((0, 'A'), (1, 'E'), (2, 'W')):
            s = rows[i][col]
            if s is None:
                continue
            if name == 'W' and i < wmin:
                continue
            d = {'A': 0, 'E': 1, 'W': 2}[name]
            x, xp = X[d][i], Xp[d][i]
            for k, c in enumerate(s):
                b = 31 - k
                v, vp = (x >> b) & 1, (xp >> b) & 1
                ok = {'=': v == vp, 'u': (v, vp) == (1, 0), 'n': (v, vp) == (0, 1), '0': (v, vp) == (0, 0),
                      '1': (v, vp) == (1, 1), '+': v == vp}[c]
                if not ok:
                    bad.append((name, i, b, c, v, vp))
    for (w1, i1, b1, op, w2, i2, b2) in extra:
        d1, d2 = {'A': 0, 'E': 1, 'W': 2}[w1], {'A': 0, 'E': 1, 'W': 2}[w2]
        v1, v2 = (X[d1][i1] >> b1) & 1, (X[d2][i2] >> b2) & 1
        if (v1 == v2) != (op == '='):
            bad.append(('extra', w1, i1, b1, op, w2, i2, b2, v1, v2))
    return bad


def words(s):
    return [int(x, 16) for x in s.split()]


# Printed two-bit relations that need a reading (see proof.md Section 2):
#  - index misprint: Table 4 prints W25[4] = W25[9]; bit 19 of sigma1(W25) is W25[4] ^ W25[6] ^ W25[29] and must cancel
#    the difference that W11 carries into W27, as Table 4 does for W16 with W16[4] != W16[6]; we read W25[4] = W25[6].
#  - orientation: a relation on a bit that carries a difference is printed for the paper's M, which is our primed
#    message; we restate it on the unprimed message (the same condition).
INDEX_FIX = {38: {('W', 25, 4, '=', 'W', 25, 9): ('W', 25, 4, '=', 'W', 25, 6)}}


def extras_as_used(R, extra, X, Xp):
    """X, Xp: (A, E, W) of the unprimed and primed SFS messages. Returns (used list, notes)."""
    used, notes = [], []
    for c in extra:
        if c in INDEX_FIX.get(R, {}):
            notes.append('index misprint: %s%d[%d] %s %s%d[%d] read as %s%d[%d] %s %s%d[%d]' % (c + INDEX_FIX[R][c]))
            c = INDEX_FIX[R][c]
        (a, i1, b1, op, w2, i2, b2) = c
        d1, d2 = 'AEW'.index(a), 'AEW'.index(w2)
        v1, v2 = (X[d1][i1] >> b1) & 1, (X[d2][i2] >> b2) & 1
        if (v1 == v2) != (op == '='):
            p1, p2 = (Xp[d1][i1] >> b1) & 1, (Xp[d2][i2] >> b2) & 1
            assert (p1 == p2) == (op == '=') and (p1 != v1 or p2 != v2), c
            nop = '!=' if op == '=' else '='
            notes.append('orientation: %s%d[%d] %s %s%d[%d] holds on the primed message (a differing bit); on the unprimed one it reads %s%d[%d] %s %s%d[%d]' % (a, i1, b1, op, w2, i2, b2, a, i1, b1, nop, w2, i2, b2))
            c = (a, i1, b1, nop, w2, i2, b2)
        used.append(c)
    return used, notes
```

### gen_header.py (SHA-256 5159f4842be716e3)

```
"""Emit charR.h for exp.c: per-word condition masks of the 1120 characteristic (unprimed = the paper's M'),
the extra two-bit conditions, the '+' adjacency relations, and the Step-1 values taken from the paper's SFS pair.
usage: python3 gen_header.py PAPER_TXT R OUT.h"""
import sys
from sha2char import *

txt = open(sys.argv[1]).read()
R = int(sys.argv[2])
T = {37: ('Table 15: The differential characteristic for 37-stepSHA-256', 'Table 16: Extra conditions', 'Table 17:',
          '63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4',
          '4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81',
          '4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81'),
     38: ('Table 3: The differential characteristic for 38-stepSHA-256', 'Table 4: Extra conditions', 'Table 5:',
          'cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e',
          '48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb',
          '48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb')}[R]
rows = parse_tables(txt, T[0], R)
extra = parse_extra(txt, T[1], T[2])
cv, mu = words(T[3]), words(T[4])          # unprimed SFS message = the paper's M'
A, E, W, _ = run(cv, mu, R)
out = ['/* generated by gen_header.py from ePrint 2026/1120 (R = %d) */' % R, '#define RR %d' % R]
for name, col in (('A', 0), ('E', 1), ('W', 2)):
    lo = 0 if name == 'W' else -4
    vm, vv, dm = [], [], []
    for i in range(-4, R):
        s = rows[i][col] if i >= lo else None
        m = v = d = 0
        if s is not None:
            for k, c in enumerate(s):
                b = 31 - k
                if c in 'un01':
                    m |= 1 << b
                    v |= (1 << b) if c in 'u1' else 0
                if c in 'un':
                    d |= 1 << b
        vm.append(m); vv.append(v); dm.append(d)
    for tag, arr in (('VM', vm), ('VV', vv), ('DM', dm)):
        out.append('static const uint32_t %s_%s[%d] = {%s};  /* index i+4 */' % (tag, name, R + 4, ', '.join('0x%08x' % x for x in arr)))
# '+' relations: equal bit in adjacent E rows
plus = sorted((i, 31 - k) for i in range(R) for k, c in enumerate(rows[i][1]) if c == '+')
rel = []
for (i, b) in plus:
    if (i + 1, b) in plus:
        rel.append(('E', i, b, '=', 'E', i + 1, b))
# the primed SFS message (the paper's M) is needed to restate orientation-dependent relations
mp = words(T[5])
Xp = run(cv, mp, R)
extra, notes = extras_as_used(R, extra, (A, E, W), Xp)
for n_ in notes:
    print(n_)
ex = list(extra) + [r_ for r_ in rel if r_[5] < 16 or not any((x[1], x[2], x[5], x[6]) == (r_[1], r_[2], r_[5], r_[6]) for x in extra)]
wid = {'A': 0, 'E': 1, 'W': 2}
out.append('#define NEX %d' % len(ex))
out.append('static const int EX[%d][7] = {%s};  /* w1,i1,b1,eq,w2,i2,b2 ; maxidx is max(i1,i2) */' % (len(ex), ', '.join(
    '{%d,%d,%d,%d,%d,%d,%d}' % (wid[a], i1, b1, 1 if op == '=' else 0, wid[c], i2, b2) for (a, i1, b1, op, c, i2, b2) in ex)))
out.append('static const uint32_t S1_A[%d] = {%s};  /* SFS unprimed A_i, index i+4 */' % (R + 4, ', '.join('0x%08x' % A[i] for i in range(-4, R))))
out.append('static const uint32_t S1_E[%d] = {%s};' % (R + 4, ', '.join('0x%08x' % E[i] for i in range(-4, R))))
out.append('static const uint32_t S1_W[%d] = {%s};' % (R, ', '.join('0x%08x' % W[i] for i in range(R))))
open(sys.argv[3], 'w').write('\n'.join(out) + '\n')
print('R', R, 'extra', len(extra), 'plus relations', len(rel), 'total EX', len(ex))
print('plus rel', rel)
```

### verify_sfs.py (SHA-256 8e895f124ed5c875)

```
"""Check the transcribed characteristics and extra conditions of ePrint 2026/1120 against its SFS pairs."""
import sys
from sha2char import *

txt = open(sys.argv[1]).read()
CASES = {
    37: ('Table 15: The differential characteristic for 37-stepSHA-256', 'Table 16: Extra conditions', 'Table 17:',
         ('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4',
          '4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 2fe12cad 6aa26b0c 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd43a81',
          '4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81',
          'a856d46e 4b46eb28 4935248c 92a2fc98 e0fb2610 10a9951f 54264f5b 80954580')),
    38: ('Table 3: The differential characteristic for 38-stepSHA-256', 'Table 4: Extra conditions', 'Table 5:',
         ('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e',
          '48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb',
          '48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb',
          '5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d')),
}
for r, (t1, t2, t3, (cv, m, mp, h)) in CASES.items():
    rows = parse_tables(txt, t1, r)
    extra = parse_extra(txt, t2, t3)
    cv, m, mp, h = words(cv), words(m), words(mp), words(h)
    X, Xp = run(cv, m, r), run(cv, mp, r)
    print('r%d: hash(M) ok %s, hash(M\') ok %s; extra conditions parsed %d' % (r, X[3] == h, Xp[3] == h, len(extra)))
    nsym = {c: sum(s.count(c) for row in rows.values() for s in row if s) for c in '=nu01+'}
    print('  symbols', nsym)
    # unprimed = the paper's M', primed = the paper's M
    U, Pm = Xp, X
    bad_rev = check_pair(rows, [], Pm, U, r)
    print('  orientation M unprimed (wrong): %d symbol failures' % len(bad_rev))
    bad = check_pair(rows, extra, U, Pm, r)
    print('  orientation M\' unprimed, printed relations: %d failures %s' % (len(bad), [b for b in bad]))
    used, notes = extras_as_used(r, extra, U, Pm)
    for n_ in notes:
        print('   ', n_)
    bad = check_pair(rows, used, U, Pm, r)
    print('  orientation M\' unprimed, relations as used: %d failures' % len(bad))
    # '+' positions: equal on the pair? record values
    plus = [(n, i, 31 - k, (P[d][i] >> (31 - k)) & 1) for i, row in rows.items() for d, (n, s) in enumerate(zip('AEW', row)) if s for k, c in enumerate(s) if c == '+' for P in [X]]
    print('  + positions (word, step, bit, value on M):', plus)
```

### check_step2.py (SHA-256 80507c9f8b18c17b)

```
"""Independent check of Step 2: for random first blocks M0, derive E0..E3 and W0..W7 of the second block from
CV1 = f_R(IV, M0) and the Step-1 values, run the second block forward from CV1, and confirm that steps 0..13
reproduce the Step-1 values A_0..A_13 and E_4..E_13. usage: python3 check_step2.py R"""
import random, sys
from sha2char import *
R = int(sys.argv[1])
SFS = {37: ('63b4986c 35d83dc0 c98894e4 784e08fc 78a7f752 5ed877a8 315a2db3 d5614eb4',
            '4d7f86ff 32ece589 d8accfc4 2cc2e433 068b5b34 eba68a28 0fe12cad 6ee2630c bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd43a81'),
       38: ('cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e',
            '48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb')}[R]
A, E, W, _ = run(words(SFS[0]), words(SFS[1]), R)
random.seed(R)
ok = 0
for trial in range(2000):
    m0 = [random.getrandbits(32) for _ in range(16)]
    cv1 = run(IV, m0, R)[3]
    a = {i: A[i] for i in range(0, 14)}
    e = {i: E[i] for i in range(4, 14)}
    a[-1], a[-2], a[-3], a[-4] = cv1[0], cv1[1], cv1[2], cv1[3]
    e[-1], e[-2], e[-3], e[-4] = cv1[4], cv1[5], cv1[6], cv1[7]
    for i in range(3, -1, -1):
        e[i] = (a[i] + a[i - 4] - S0(a[i - 1]) - MAJ(a[i - 1], a[i - 2], a[i - 3])) & M32
    w = {i: (e[i] - a[i - 4] - e[i - 4] - S1(e[i - 1]) - IF(e[i - 1], e[i - 2], e[i - 3]) - K[i]) & M32 for i in range(7, -1, -1)}
    A2, E2, _, _ = run(cv1, [w[i] for i in range(8)] + [W[i] for i in range(8, 16)], 16)
    ok += all(A2[i] == A[i] for i in range(14)) and all(E2[i] == E[i] for i in range(4, 14))
print('R %d: steps 0..13 of the second block reproduce the Step-1 values for %d of 2000 random first blocks' % (R, ok))
```

### exp.c (SHA-256 21afb6b540139547)

```
/* Experiments for the 37/38-step attacks of ePrint 2026/1120 (Li, Zhang, Li, Liu, Qian, Zhu), Section 4.2 framework.
   Step-1 solution = the second-block values of the paper's SFS pair (unprimed = its M'); see gen_header.py.
   usage: exp S                      -> enumerate the (W14, W15) set S of Step 3
          exp RUN LOG2TRIALS THREADS SEED -> Step 2 rate on random first blocks, then Step 3 depth histogram
   Build: cc -O3 -DCHAR=\"char37.h\" -o exp37 exp.c -lpthread */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <math.h>
#include CHAR
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define BS0(x) (ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22))
#define BS1(x) (ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25))
#define SS0(x) (ROR(x, 7) ^ ROR(x, 18) ^ ((x) >> 3))
#define SS1(x) (ROR(x, 17) ^ ROR(x, 19) ^ ((x) >> 10))
#define IF(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
static const u32 K[64] = {0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
  0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb,
  0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f,
  0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
static const u32 IV[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};

static u32 modd(u32 dm, u32 vv) { u32 r = 0; for (int b = 0; b < 32; b++) if ((dm >> b) & 1) r += ((vv >> b) & 1) ? -(1u << b) : (1u << b); return r; }
typedef struct { u32 A[RR + 4], E[RR + 4], W[RR]; } st_t;   /* A[i+4], E[i+4] */
#define AA(s, i) ((s)->A[(i) + 4])
#define EE(s, i) ((s)->E[(i) + 4])

static void compress(const u32 cv[8], const u32 m[16], u32 out[8]) {   /* RR-step target compression + feed-forward */
  u32 w[16], a = cv[0], b = cv[1], c = cv[2], d = cv[3], e = cv[4], f = cv[5], g = cv[6], h = cv[7];
  memcpy(w, m, 64);
  for (int i = 0; i < RR; i++) {
    u32 wi = i < 16 ? w[i] : (w[i & 15] = SS1(w[(i - 2) & 15]) + w[(i - 7) & 15] + SS0(w[(i - 15) & 15]) + w[i & 15]);
    u32 t1 = h + BS1(e) + IF(e, f, g) + K[i] + wi, t2 = BS0(a) + MAJ(a, b, c);
    h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
  }
  out[0] = a + cv[0]; out[1] = b + cv[1]; out[2] = c + cv[2]; out[3] = d + cv[3];
  out[4] = e + cv[4]; out[5] = f + cv[5]; out[6] = g + cv[6]; out[7] = h + cv[7];
}

static inline u32 word(const st_t *s, int w, int i) { return w == 0 ? AA(s, i) : w == 1 ? EE(s, i) : s->W[i]; }

/* single-message (sufficient) conditions of step index i: value symbols of A_i, E_i, W_i and extras whose max index is i */
static int cond_single(const st_t *s, int i) {
  if ((AA(s, i) & VM_A[i + 4]) != VV_A[i + 4]) return 0;
  if ((EE(s, i) & VM_E[i + 4]) != VV_E[i + 4]) return 0;
  if (i >= 0 && (s->W[i] & VM_W[i + 4]) != VV_W[i + 4]) return 0;
  for (int k = 0; k < NEX; k++) {
    int mi = EX[k][1] > EX[k][5] ? EX[k][1] : EX[k][5];
    if (mi != i) continue;
    u32 v1 = (word(s, EX[k][0], EX[k][1]) >> EX[k][2]) & 1, v2 = (word(s, EX[k][4], EX[k][5]) >> EX[k][6]) & 1;
    if ((v1 == v2) != EX[k][3]) return 0;
  }
  return 1;
}
/* pair test of step i: single conditions on the unprimed message and the exact XOR difference of A_i, E_i, W_i */
static int cond_pair(const st_t *s, const st_t *p, int i) {
  if (!cond_single(s, i)) return 0;
  if ((AA(s, i) ^ AA(p, i)) != DM_A[i + 4]) return 0;
  if ((EE(s, i) ^ EE(p, i)) != DM_E[i + 4]) return 0;
  if (i >= 0 && (s->W[i] ^ p->W[i]) != DM_W[i + 4]) return 0;
  return 1;
}
static void step(st_t *s, int i) {
  if (i >= 16) s->W[i] = SS1(s->W[i - 2]) + s->W[i - 7] + SS0(s->W[i - 15]) + s->W[i - 16];
  EE(s, i) = AA(s, i - 4) + EE(s, i - 4) + BS1(EE(s, i - 1)) + IF(EE(s, i - 1), EE(s, i - 2), EE(s, i - 3)) + K[i] + s->W[i];
  AA(s, i) = EE(s, i) - AA(s, i - 4) + BS0(AA(s, i - 1)) + MAJ(AA(s, i - 1), AA(s, i - 2), AA(s, i - 3));
}

/* ---- Step 2: from CV1 and the Step-1 values, derive E0..E3 and W0..W7; return 1 if the conditions up to index 7 hold */
static int step2(const u32 cv[8], st_t *s) {
  for (int i = 0; i <= 13; i++) AA(s, i) = S1_A[i + 4];
  for (int i = 4; i <= 13; i++) EE(s, i) = S1_E[i + 4];
  for (int i = 8; i <= 13; i++) s->W[i] = S1_W[i];
  AA(s, -1) = cv[0]; AA(s, -2) = cv[1]; AA(s, -3) = cv[2]; AA(s, -4) = cv[3];
  EE(s, -1) = cv[4]; EE(s, -2) = cv[5]; EE(s, -3) = cv[6]; EE(s, -4) = cv[7];
  for (int i = 3; i >= 0; i--)
    EE(s, i) = AA(s, i) + AA(s, i - 4) - BS0(AA(s, i - 1)) - MAJ(AA(s, i - 1), AA(s, i - 2), AA(s, i - 3));
  for (int i = 7; i >= 0; i--)
    s->W[i] = EE(s, i) - AA(s, i - 4) - EE(s, i - 4) - BS1(EE(s, i - 1)) - IF(EE(s, i - 1), EE(s, i - 2), EE(s, i - 3)) - K[i];
  for (int i = -4; i <= 7; i++) if (!cond_single(s, i)) return 0;
  return 1;
}

/* ---- the set S of (W14, W15): conditions of index 14 and 15 depend only on Step-1 values */
/* primed value of step i from the unprimed one (the characteristic fixes every differing bit's value) */
static int NOS16 = 0;
static u32 SW14[1 << 16], SW15[1 << 16]; static int NS; static u64 NSALL;
static void build_S(void) {
  st_t s; memset(&s, 0, sizeof s);
  for (int i = 0; i <= 13; i++) AA(&s, i) = S1_A[i + 4];
  for (int i = 4; i <= 13; i++) EE(&s, i) = S1_E[i + 4];
  for (int i = 8; i <= 13; i++) s.W[i] = S1_W[i];
  u32 c14 = AA(&s, 10) + EE(&s, 10) + BS1(EE(&s, 13)) + IF(EE(&s, 13), EE(&s, 12), EE(&s, 11)) + K[14];
  u64 n14 = 0;
  u32 fr = ~VM_E[14 + 4];                                  /* enumerate E14 over its unconditioned bits */
  u32 x = 0;
  do {
    u32 e14 = VV_E[14 + 4] | x;
    EE(&s, 14) = e14; s.W[14] = e14 - c14;
    AA(&s, 14) = e14 - AA(&s, 10) + BS0(AA(&s, 13)) + MAJ(AA(&s, 13), AA(&s, 12), AA(&s, 11));
    u32 w14 = s.W[14], d16 = SS1(w14 ^ DM_W[14 + 4]) - SS1(w14) + (S1_W[9] ^ DM_W[9 + 4]) - S1_W[9];
    /* pair values of step 14: primed inputs are the unprimed ones XOR the characteristic's differences */
    u32 pe14 = (AA(&s, 10) ^ DM_A[14]) + (EE(&s, 10) ^ DM_E[14]) + BS1(EE(&s, 13) ^ DM_E[17]) + IF(EE(&s, 13) ^ DM_E[17], EE(&s, 12) ^ DM_E[16], EE(&s, 11) ^ DM_E[15]) + K[14] + (w14 ^ DM_W[18]);
    u32 pa14 = pe14 - (AA(&s, 10) ^ DM_A[14]) + BS0(AA(&s, 13) ^ DM_A[17]) + MAJ(AA(&s, 13) ^ DM_A[17], AA(&s, 12) ^ DM_A[16], AA(&s, 11) ^ DM_A[15]);
    int pair14 = ((pe14 ^ EE(&s, 14)) == DM_E[18]) && ((pa14 ^ AA(&s, 14)) == DM_A[18]);
    if (cond_single(&s, 14) && pair14 && d16 == modd(DM_W[16 + 4], VV_W[16 + 4])) {
      n14++;
      u32 c15 = AA(&s, 11) + EE(&s, 11) + BS1(e14) + IF(e14, EE(&s, 13), EE(&s, 12)) + K[15];
      u32 fr5 = ~VM_E[15 + 4], y = 0;
      do {
        u32 e15 = VV_E[15 + 4] | y;
        EE(&s, 15) = e15; s.W[15] = e15 - c15;
        AA(&s, 15) = e15 - AA(&s, 11) + BS0(AA(&s, 14)) + MAJ(AA(&s, 14), AA(&s, 13), AA(&s, 12));
        u32 w15 = s.W[15], d17 = SS1(w15 ^ DM_W[15 + 4]) - SS1(w15) + (S1_W[10] ^ DM_W[10 + 4]) - S1_W[10];
        u32 pe15 = (AA(&s, 11) ^ DM_A[15]) + (EE(&s, 11) ^ DM_E[15]) + BS1(EE(&s, 14) ^ DM_E[18]) + IF(EE(&s, 14) ^ DM_E[18], EE(&s, 13) ^ DM_E[17], EE(&s, 12) ^ DM_E[16]) + K[15] + (w15 ^ DM_W[19]);
        u32 pa15 = pe15 - (AA(&s, 11) ^ DM_A[15]) + BS0(AA(&s, 14) ^ DM_A[18]) + MAJ(AA(&s, 14) ^ DM_A[18], AA(&s, 13) ^ DM_A[17], AA(&s, 12) ^ DM_A[16]);
        int pair15 = ((pe15 ^ EE(&s, 15)) == DM_E[19]) && ((pa15 ^ AA(&s, 15)) == DM_A[19]);
        /* step 16: the parts of E16 and A16 that depend only on (A,E)_{13..15} must carry the characteristic's modular differences */
        u32 pe13 = EE(&s, 13) ^ DM_E[17], pe14x = e14 ^ DM_E[18], pe15x = e15 ^ DM_E[19];
        u32 pa13 = AA(&s, 13) ^ DM_A[17], pa14x = AA(&s, 14) ^ DM_A[18], pa15x = AA(&s, 15) ^ DM_A[19];
        u32 fE = (BS1(pe15x) + IF(pe15x, pe14x, pe13)) - (BS1(e15) + IF(e15, e14, EE(&s, 13)));
        u32 tE = modd(DM_E[20], VV_E[20]) - modd(DM_A[16], VV_A[16]) - modd(DM_E[16], VV_E[16]) - modd(DM_W[20], VV_W[20]);
        u32 fA = (BS0(pa15x) + MAJ(pa15x, pa14x, pa13)) - (BS0(AA(&s, 15)) + MAJ(AA(&s, 15), AA(&s, 14), AA(&s, 13)));
        u32 tA = modd(DM_A[20], VV_A[20]) - modd(DM_E[20], VV_E[20]) + modd(DM_A[16], VV_A[16]);
        int m16 = (fE == tE) && (fA == tA);
        /* every expanded word W_t whose required modular difference involves sigma of a differing word only among W8..W15 */
        int mexp = 1;
        for (int t = 16; t < RR && mexp; t++) {
          int a2 = t - 2, a15 = t - 15;
          int dep2 = DM_W[a2 + 4] != 0, dep15 = DM_W[a15 + 4] != 0;
          if ((dep2 && (a2 < 8 || a2 > 15)) || (dep15 && (a15 < 8 || a15 > 15))) continue;
          u32 d = modd(DM_W[t - 7 + 4], VV_W[t - 7 + 4]) + modd(DM_W[t - 16 + 4], VV_W[t - 16 + 4]);
          if (dep2) d += SS1(s.W[a2] ^ DM_W[a2 + 4]) - SS1(s.W[a2]);
          if (dep15) d += SS0(s.W[a15] ^ DM_W[a15 + 4]) - SS0(s.W[a15]);
          if (d != modd(DM_W[t + 4], VV_W[t + 4])) mexp = 0;
        }
        if (cond_single(&s, 15) && pair15 && d17 == modd(DM_W[17 + 4], VV_W[17 + 4]) && (m16 || NOS16) && mexp) { NSALL++; if (NS < (1 << 16)) { SW14[NS] = s.W[14]; SW15[NS] = s.W[15]; NS++; } }
        y = (y - fr5) & fr5;
      } while (y);
    }
    x = (x - fr) & fr;
  } while (x);
  fprintf(stderr, "S: E14 free bits %d, W14 candidates %llu, |S| = %d (all %llu); SFS (W14,W15) = (%08x,%08x) in S: ", __builtin_popcount(fr),
          (unsigned long long)n14, NS, (unsigned long long)NSALL, S1_W[14], S1_W[15]);
  int in = 0; for (int k = 0; k < NS; k++) in |= SW14[k] == S1_W[14] && SW15[k] == S1_W[15];
  fprintf(stderr, "%s\n", in ? "yes" : "no");
}

/* ---- RNG */
static inline u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
typedef struct { u64 s[4]; } rng_t;
static inline u64 rnext(rng_t *r) { u64 *s = r->s, res = rotl(s[1] * 5, 7) * 9, t = s[1] << 17; s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return res; }
static void rseed(rng_t *r, u64 a, u64 b) { u64 z = a * 0x9e3779b97f4a7c15ULL ^ b; for (int i = 0; i < 4; i++) { z += 0x9e3779b97f4a7c15ULL; u64 q = z; q = (q ^ (q >> 30)) * 0xbf58476d1ce4e5b9ULL; q = (q ^ (q >> 27)) * 0x94d049bb133111ebULL; r->s[i] = q ^ (q >> 31); } }

#define MAXV (1 << 22)
typedef struct { int id; u64 n, valid, nv, nv3; u64 seed; u32 (*cvs)[8]; u64 depth[RR + 6]; u64 coll; u64 mult[8]; } job_t;
static u64 TRIALS, V3; static int NT; static int DIAG = 16;
#define NSUB 64
static u64 SUBP[256][NSUB], SUBN[256];
static void diag(int tid, const st_t *a, const st_t *b, int i) {
  u64 *c = SUBP[tid]; int k = 0;
  c[k++] += (AA(a, i) & VM_A[i + 4]) == VV_A[i + 4];
  c[k++] += (EE(a, i) & VM_E[i + 4]) == VV_E[i + 4];
  c[k++] += (a->W[i] & VM_W[i + 4]) == VV_W[i + 4];
  c[k++] += (AA(a, i) ^ AA(b, i)) == DM_A[i + 4];
  c[k++] += (EE(a, i) ^ EE(b, i)) == DM_E[i + 4];
  c[k++] += (a->W[i] ^ b->W[i]) == DM_W[i + 4];
  c[k++] += (EE(b, i) - EE(a, i)) == modd(DM_E[i + 4], VV_E[i + 4]);
  c[k++] += (AA(b, i) - AA(a, i)) == modd(DM_A[i + 4], VV_A[i + 4]);
  for (int q = 0; q < NEX && k < NSUB; q++) {
    int mi = EX[q][1] > EX[q][5] ? EX[q][1] : EX[q][5];
    if (mi != i) continue;
    u32 v1 = (word(a, EX[q][0], EX[q][1]) >> EX[q][2]) & 1, v2 = (word(a, EX[q][4], EX[q][5]) >> EX[q][6]) & 1;
    c[k++] += (v1 == v2) == EX[q][3];
  }
  SUBN[tid]++;
}

static void *work(void *p) {
  job_t *j = p; rng_t r; rseed(&r, j->seed, j->id);
  u32 m[16], cv[8]; st_t s;
  u64 lo = TRIALS * j->id / NT, hi = TRIALS * (j->id + 1) / NT;
  for (int k = 0; k < 16; k += 2) { u64 z = rnext(&r); m[k] = (u32)z; m[k + 1] = (u32)(z >> 32); }
  for (u64 t = lo; t < hi; t++) {
    /* every first block is 16 fresh independent uniform words */
    for (int k = 0; k < 16; k += 2) { u64 z = rnext(&r); m[k] = (u32)z; m[k + 1] = (u32)(z >> 32); }
    compress(IV, m, cv);
    j->n++;
    if (step2(cv, &s)) { if (j->nv < MAXV / NT) memcpy(j->cvs[j->nv++], cv, 32); j->valid++; }
  }
  /* Step 3 on the stored valid first blocks */
  u64 v3 = V3 / NT; if (v3 > j->nv) v3 = j->nv; j->nv3 = v3;
  for (u64 v = 0; v < v3; v++) {
    st_t a, b; int surv16 = 0;
    step2(j->cvs[v], &a);
    for (int q = 0; q < NS; q++) {
      a.W[14] = SW14[q]; a.W[15] = SW15[q];
      memcpy(&b, &a, sizeof a);
      for (int i = 0; i < 16; i++) b.W[i] ^= DM_W[i + 4];
      for (int i = -4; i < 0; i++) { /* same CV */ }
      int d = -5;
      for (int i = 0; i < RR; i++) {        /* recompute both from the chaining value */
        step(&a, i); step(&b, i);
        if (i == DIAG) diag(j->id, &a, &b, i);
        if (!cond_pair(&a, &b, i)) { d = i; break; }
      }
      if (d == -5 || d > 16) surv16++;
      if (d == -5) {
        int eq = 1;
        for (int k = 0; k < 4; k++) eq &= AA(&a, RR - 1 - k) == AA(&b, RR - 1 - k) && EE(&a, RR - 1 - k) == EE(&b, RR - 1 - k);
        j->coll += eq; j->depth[RR + 5]++;
      } else j->depth[d + 5]++;
    }
    j->mult[surv16 < 7 ? surv16 : 7]++;
  }
  return NULL;
}


/* ---- STAGE: conditional pass rate of each step t = 16..KMAX given that steps 16..t-1 pass.
   Model of Step 3: steps <= 13 carry the Step-1 values, (W14, W15) is drawn from S, W8..W13 are Step-1 words,
   W6 and W7 are drawn uniformly among the values that meet their conditions, and W0..W5 are free uniform words.
   Step t (16 <= t <= 21) gets a fresh uniform W_{t-16}, so E_t = base_t + W_t is uniform; a draw is retried at
   the same step until it passes (at most CAP draws). The primed message's W_t is the unprimed one plus the
   modular difference forced by the expansion (computable because W_{t-16} and W_{t-15} carry no difference
   for t-16 <= 5, and W6/W7 values are known). For t = 22 (W6) and 23 (W7) the fresh word is drawn from the
   conditioned set. */
static u64 CAP = 1ULL << 16; static int FIXED = 0; static u64 CAPT[64];
static u64 ST_ATT[64], ST_PASS[64], ST_DEAD[64], ST_WD[64], ST_WP[64], ST_TAIL[64], ST_COLL, ST_REACH; static double PSUM[256], PSQ[256]; static u64 PNZ[256]; static double GSUM[256], GSQ[256]; static u64 MHIST[256][8]; static u32 EXAMPLE[1 + 8 + 16 + 16]; static int HAVE_EX;
typedef struct { int id; u64 n; u64 seed; int kmax; } sjob_t;
static int wcond(u32 w, int i) {   /* single conditions that involve only W_i (value symbols and W_i-only extras) */
  if ((w & VM_W[i + 4]) != VV_W[i + 4]) return 0;
  for (int k = 0; k < NEX; k++) {
    if (EX[k][0] != 2 || EX[k][4] != 2 || EX[k][1] != i || EX[k][5] != i) continue;
    if ((((w >> EX[k][2]) & 1) == ((w >> EX[k][6]) & 1)) != EX[k][3]) return 0;
  }
  return 1;
}
static void *swork(void *p) {
  sjob_t *j = p; rng_t r; rseed(&r, j->seed, j->id + 1000);
  u64 att[64] = {0}, pas[64] = {0}, dead[64] = {0}, wd[64] = {0}, wp[64] = {0}, tail_ok[64] = {0}, coll = 0, reach = 0;
  for (u64 n = 0; n < j->n; n++) {
    st_t a, b; memset(&a, 0, sizeof a);
    for (int i = -4; i <= 13; i++) { AA(&a, i) = S1_A[i + 4]; EE(&a, i) = S1_E[i + 4]; }
    for (int i = 8; i <= 13; i++) a.W[i] = S1_W[i];
    double prod = 1.0;   /* per-start estimate: product of the per-state pass fractions, times the tail indicator */
    int q = (int)(rnext(&r) % NS); a.W[14] = SW14[q]; a.W[15] = SW15[q];
    u32 w; do { w = (u32)rnext(&r); } while (!wcond(w, 6)); a.W[6] = w;
    do { w = (u32)rnext(&r); } while (!wcond(w, 7)); a.W[7] = w;
    for (int i = 0; i <= 5; i++) a.W[i] = 0;   /* placeholders: back-solved below, never used by steps >= 14 */
    memcpy(&b, &a, sizeof a);
    for (int i = -4; i <= 13; i++) { AA(&b, i) ^= DM_A[i + 4]; EE(&b, i) ^= DM_E[i + 4]; }
    for (int i = 6; i <= 15; i++) b.W[i] ^= DM_W[i + 4];
    for (int i = 14; i <= 15; i++) { step(&a, i); step(&b, i); }
    int ok = 1;
    for (int i = 14; i <= 15; i++) if (!cond_pair(&a, &b, i)) ok = 0;
    if (!ok) { fprintf(stderr, "S element fails at 14/15\n"); exit(1); }
    for (int t = 16; t <= j->kmax && t < RR; t++) {
      int f = t - 16, passed = 0;
      u32 base = AA(&a, t - 4) + EE(&a, t - 4) + BS1(EE(&a, t - 1)) + IF(EE(&a, t - 1), EE(&a, t - 2), EE(&a, t - 3)) + K[t];
      /* modular difference of W_t from the expansion: d(sigma1(W_{t-2})) + d(W_{t-7}) + d(sigma0(W_{t-15})) + d(W_{t-16}) */
      st_t sa, sb; u64 npass = 0;
      u64 cap = CAPT[t] ? CAPT[t] : CAP;
      for (u64 tries = 0; tries < cap; tries++) {
        u32 wt;
        if (f <= 5) { do { wt = (u32)rnext(&r); wd[t]++; } while (!wcond(wt, t)); wp[t]++; }
        else if (f == 6) { u32 wf; do { wf = (u32)rnext(&r); } while (!wcond(wf, f)); a.W[f] = wf; b.W[f] = wf ^ DM_W[f + 4];
               wt = SS1(a.W[t - 2]) + a.W[t - 7] + SS0(a.W[t - 15]) + wf; }
        else {  /* f == 7: W7 also enters W22 through sigma0(W7); keep W22 by re-solving W6 (allowed only if W6 carries no
                   difference, so W21's difference is unchanged, and W6 keeps its conditions); W0..W5 are back-solved later */
          if (DM_W[6 + 4] != 0) { fprintf(stderr, "stage 23 needs a difference-free W6\n"); exit(1); }
          u32 wf, w6;
          do { do { wf = (u32)rnext(&r); } while (!wcond(wf, 7)); w6 = a.W[22] - SS1(a.W[20]) - a.W[15] - SS0(wf); } while (!wcond(w6, 6));
          a.W[7] = wf; b.W[7] = wf ^ DM_W[7 + 4]; a.W[6] = w6; b.W[6] = w6;
          wt = SS1(a.W[t - 2]) + a.W[t - 7] + SS0(a.W[t - 15]) + wf; }
        a.W[t] = wt;
        u32 dw = (SS1(b.W[t - 2]) - SS1(a.W[t - 2])) + (b.W[t - 7] - a.W[t - 7]) + (SS0(b.W[t - 15]) - SS0(a.W[t - 15]));
        if (f >= 6) dw += b.W[f] - a.W[f];
        b.W[t] = wt + dw;
        EE(&a, t) = base + wt;
        AA(&a, t) = EE(&a, t) - AA(&a, t - 4) + BS0(AA(&a, t - 1)) + MAJ(AA(&a, t - 1), AA(&a, t - 2), AA(&a, t - 3));
        EE(&b, t) = AA(&b, t - 4) + EE(&b, t - 4) + BS1(EE(&b, t - 1)) + IF(EE(&b, t - 1), EE(&b, t - 2), EE(&b, t - 3)) + K[t] + b.W[t];
        AA(&b, t) = EE(&b, t) - AA(&b, t - 4) + BS0(AA(&b, t - 1)) + MAJ(AA(&b, t - 1), AA(&b, t - 2), AA(&b, t - 3));
        att[t]++;
        if (cond_pair(&a, &b, t)) { pas[t]++; if (!npass++) { sa = a; sb = b; } if (!FIXED) break; }
      }
      passed = npass > 0;
      prod *= (double)npass / (double)cap;
      if (passed && FIXED) { a = sa; b = sb; }
      if (!passed) { dead[t]++; ok = 0; break; }
    }
    if (ok) {
      reach++;
      int alive = 1;
      for (int t = j->kmax + 1; t < RR && alive; t++) {
        step(&a, t);
        u32 dw = (SS1(b.W[t - 2]) - SS1(a.W[t - 2])) + (b.W[t - 7] - a.W[t - 7]) + (SS0(b.W[t - 15]) - SS0(a.W[t - 15])) + (b.W[t - 16] - a.W[t - 16]);
        b.W[t] = a.W[t] + dw;
        EE(&b, t) = AA(&b, t - 4) + EE(&b, t - 4) + BS1(EE(&b, t - 1)) + IF(EE(&b, t - 1), EE(&b, t - 2), EE(&b, t - 3)) + K[t] + b.W[t];
        AA(&b, t) = EE(&b, t) - AA(&b, t - 4) + BS0(AA(&b, t - 1)) + MAJ(AA(&b, t - 1), AA(&b, t - 2), AA(&b, t - 3));
        if (cond_pair(&a, &b, t)) tail_ok[t]++; else alive = 0;
      }
      if (alive) {
        int eq = 1;
        for (int k = 0; k < 4; k++) eq &= AA(&a, RR - 1 - k) == AA(&b, RR - 1 - k) && EE(&a, RR - 1 - k) == EE(&b, RR - 1 - k);
        coll += eq;
        if (eq) {
          PSUM[j->id] += prod; PSQ[j->id] += prod * prod; PNZ[j->id]++;
          /* m-weighted sample: back-solve W0..W5 on a copy, then count the elements of S that pass steps 14..16 on the
             same W0..W13 (this element always does); the sample |S| * prod / m estimates E[(sum of successes)/m] */
          st_t c0 = a;
          for (int t2 = 21; t2 >= 16; t2--) c0.W[t2 - 16] = c0.W[t2] - SS1(c0.W[t2 - 2]) - c0.W[t2 - 7] - SS0(c0.W[t2 - 15]);
          int mm = 0;
          for (int q2i = 0; q2i < NS; q2i++) {
            st_t x = c0, y;
            x.W[14] = SW14[q2i]; x.W[15] = SW15[q2i];
            y = x;
            for (int i2 = -4; i2 <= 13; i2++) { AA(&y, i2) ^= DM_A[i2 + 4]; EE(&y, i2) ^= DM_E[i2 + 4]; }
            for (int i2 = 0; i2 <= 15; i2++) y.W[i2] = x.W[i2] ^ DM_W[i2 + 4];
            int okq = 1;
            for (int t2 = 14; t2 <= 16 && okq; t2++) { step(&x, t2); step(&y, t2); okq = cond_pair(&x, &y, t2); }
            mm += okq;
          }
          if (mm < 1) { fprintf(stderr, "m-weight: the sampled element fails its own re-check\n"); exit(1); }
          double g = (double)NS * prod / mm;
          GSUM[j->id] += g; GSQ[j->id] += g * g; MHIST[j->id][mm < 7 ? mm : 7]++;
        }
        if (eq && !__atomic_exchange_n(&HAVE_EX, 1, __ATOMIC_ACQ_REL)) {
          /* back-solve W0..W5 from W16..W21, then the chaining value from steps 0..7 */
          for (int t = 21; t >= 16; t--) a.W[t - 16] = a.W[t] - SS1(a.W[t - 2]) - a.W[t - 7] - SS0(a.W[t - 15]);
          /* E_{i-4} + A_{i-4} = E_i - W_i - K_i - Sigma1(E_{i-1}) - IF(..), and A_{i-4} = E_i' ... solve top-down */
          for (int i = 7; i >= 4; i--) {
            u32 sum = EE(&a, i) - a.W[i] - K[i] - BS1(EE(&a, i - 1)) - IF(EE(&a, i - 1), EE(&a, i - 2), EE(&a, i - 3));
            EE(&a, i - 4) = sum - AA(&a, i - 4);
          }
          for (int i = 3; i >= 0; i--) {
            AA(&a, i - 4) = EE(&a, i) - AA(&a, i) + BS0(AA(&a, i - 1)) + MAJ(AA(&a, i - 1), AA(&a, i - 2), AA(&a, i - 3));
            u32 sum = EE(&a, i) - a.W[i] - K[i] - BS1(EE(&a, i - 1)) - IF(EE(&a, i - 1), EE(&a, i - 2), EE(&a, i - 3));
            EE(&a, i - 4) = sum - AA(&a, i - 4);
          }
          EXAMPLE[0] = RR;
          for (int k = 0; k < 4; k++) { EXAMPLE[1 + k] = AA(&a, -1 - k); EXAMPLE[5 + k] = EE(&a, -1 - k); }
          for (int k = 0; k < 16; k++) { EXAMPLE[9 + k] = a.W[k]; EXAMPLE[25 + k] = a.W[k] ^ DM_W[k + 4]; }
        }
      }
    }
  }
  __atomic_add_fetch(&ST_COLL, coll, __ATOMIC_RELAXED); __atomic_add_fetch(&ST_REACH, reach, __ATOMIC_RELAXED);
  for (int t = 0; t < 64; t++) { __atomic_add_fetch(&ST_WD[t], wd[t], __ATOMIC_RELAXED); __atomic_add_fetch(&ST_WP[t], wp[t], __ATOMIC_RELAXED); __atomic_add_fetch(&ST_TAIL[t], tail_ok[t], __ATOMIC_RELAXED); __atomic_add_fetch(&ST_ATT[t], att[t], __ATOMIC_RELAXED); __atomic_add_fetch(&ST_PASS[t], pas[t], __ATOMIC_RELAXED); __atomic_add_fetch(&ST_DEAD[t], dead[t], __ATOMIC_RELAXED); }
  return NULL;
}
static int stage_main(int argc, char **argv) {
  if (getenv("CAP")) CAP = 1ULL << atoi(getenv("CAP"));
  if (getenv("FIXED")) FIXED = 1;
  if (getenv("CAPS")) { char *q = getenv("CAPS"); while (*q) { int t = (int)strtol(q, &q, 10); if (*q == ':') q++; int c = (int)strtol(q, &q, 10); CAPT[t] = 1ULL << c; if (*q == ',') q++; } }   /* exactly CAP draws per state: passes/attempts estimates the mean pass probability */
  u64 n = 1ULL << atoi(argv[2]); int nt = atoi(argv[3]); u64 seed = strtoull(argv[4], 0, 0); int kmax = atoi(argv[5]);
  sjob_t J[256]; pthread_t th[256];
  for (int t = 0; t < nt; t++) { J[t].id = t; J[t].n = n / nt + ((u64)t < n % nt); J[t].seed = seed; J[t].kmax = kmax; pthread_create(&th[t], 0, swork, &J[t]); }
  for (int t = 0; t < nt; t++) pthread_join(th[t], 0);
  double tot = 0;
  printf("STAGE R %d samples %llu |S| %d kmax %d\n", RR, (unsigned long long)n, NS, kmax);
  for (int t = 16; t <= kmax && t < RR; t++) {
    double rate = ST_ATT[t] ? (double)ST_PASS[t] / ST_ATT[t] : 0;
    tot += rate > 0 ? log2(rate) : -99;
    double wr = ST_WD[t] ? (double)ST_WP[t] / ST_WD[t] : 1.0;
    tot += log2(wr);
    printf("  step %d: W-only conditions 2^%.3f (%llu/%llu draws); rest: attempts %llu passes %llu dead %llu rate 2^%.3f; step total 2^%.3f (cumulative 2^%.3f)\n", t,
           log2(wr), (unsigned long long)ST_WP[t], (unsigned long long)ST_WD[t], (unsigned long long)ST_ATT[t],
           (unsigned long long)ST_PASS[t], (unsigned long long)ST_DEAD[t], rate > 0 ? log2(rate) : -99.0, (rate > 0 ? log2(rate) : -99.0) + log2(wr), tot);
  }
  printf("  reached step %d: %llu samples\n", kmax, (unsigned long long)ST_REACH);
  { double sm = 0, sq = 0; u64 nz = 0; for (int t = 0; t < nt; t++) { sm += PSUM[t]; sq += PSQ[t]; nz += PNZ[t]; }
    double wf = 1.0; for (int t = 16; t <= kmax && t < RR; t++) if (ST_WD[t]) wf *= (double)ST_WP[t] / ST_WD[t];
    double mean = sm / n, var = sq / n - mean * mean, se = sqrt(var / n);
    printf("  per-start estimator over %llu starts (%llu nonzero): mean 2^%.4f, standard error %.4f of the mean, mean - 1.96 SE 2^%.4f (W-only factor 2^%.3f included)\n",
           (unsigned long long)n, (unsigned long long)nz, log2(mean * wf), se / mean, mean - 1.96 * se > 0 ? log2((mean - 1.96 * se) * wf) : -999.0, log2(wf));
    double gs = 0, gq = 0; u64 mh[8] = {0}; for (int t = 0; t < nt; t++) { gs += GSUM[t]; gq += GSQ[t]; for (int k = 0; k < 8; k++) mh[k] += MHIST[t][k]; }
    double gm = gs / n, gv = gq / n - gm * gm, gse = sqrt(gv / n);
    printf("  m-weighted estimator (|S| prod / m): mean 2^%.4f, standard error %.4f of the mean, mean - 1.96 SE 2^%.4f; m histogram at collisions:", log2(gm * wf), gse / gm, gm - 1.96 * gse > 0 ? log2((gm - 1.96 * gse) * wf) : -999.0);
    for (int k = 1; k < 8; k++) printf(" %d:%llu", k, (unsigned long long)mh[k]);
    printf("\n"); }
  for (int t = kmax + 1; t < RR; t++) printf("  natural step %d: survivors %llu\n", t, (unsigned long long)ST_TAIL[t]);
  printf("  full collisions (SFS, own chaining value) %llu\n", (unsigned long long)ST_COLL);
  if (HAVE_EX) {
    printf("  example R %u CV", EXAMPLE[0]); for (int k = 1; k < 9; k++) printf(" %08x", EXAMPLE[k]);
    printf("\n  M "); for (int k = 9; k < 25; k++) printf(" %08x", EXAMPLE[k]);
    printf("\n  M'"); for (int k = 25; k < 41; k++) printf(" %08x", EXAMPLE[k]); printf("\n");
  }
  return 0;
}

int main(int argc, char **argv) {
  if (getenv("NOS16")) NOS16 = 1;
  build_S();
  if (argc > 1 && !strcmp(argv[1], "LIST")) { for (int k = 0; k < NS; k++) printf("%08x %08x\n", SW14[k], SW15[k]); return 0; }
  if (argc > 1 && !strcmp(argv[1], "STAGE")) return stage_main(argc, argv);
  if (argc < 2 || strcmp(argv[1], "RUN")) return 0;
  TRIALS = 1ULL << atoi(argv[2]); NT = atoi(argv[3]); u64 seed = strtoull(argv[4], 0, 0); V3 = 1ULL << atoi(argv[5]); if (argc > 6) DIAG = atoi(argv[6]);
  job_t *J = calloc(NT, sizeof(job_t)); pthread_t th[256];
  for (int t = 0; t < NT; t++) { J[t].id = t; J[t].seed = seed; J[t].cvs = malloc(sizeof(u32[8]) * (u64)MAXV / NT + 64); }
  for (int t = 0; t < NT; t++) pthread_create(&th[t], 0, work, &J[t]);
  for (int t = 0; t < NT; t++) pthread_join(th[t], 0);
  u64 n = 0, v = 0, nv = 0, nv3 = 0, dep[RR + 6] = {0}, coll = 0;
  for (int t = 0; t < NT; t++) { n += J[t].n; v += J[t].valid; nv += J[t].nv; nv3 += J[t].nv3; coll += J[t].coll; for (int i = 0; i < RR + 6; i++) dep[i] += J[t].depth[i]; }
  printf("R %d trials %llu valid %llu (2^%.3f) step3 first blocks %llu x |S| %d\n", RR, (unsigned long long)n, (unsigned long long)v,
         v ? log2((double)v / n) : -99.0, (unsigned long long)nv3, NS);
  u64 alive = nv3 * NS;
  printf("step3 trials %llu; first failing step histogram (fail at i; survivors cumulative):\n", (unsigned long long)alive);
  for (int i = -4; i < RR; i++) if (dep[i + 5]) { alive -= dep[i + 5]; printf("  fail@%d %llu  survive>%d %llu (2^%.2f)\n", i, (unsigned long long)dep[i + 5], i, (unsigned long long)alive, alive ? log2((double)alive / (nv3 * NS)) : -99.0); }
  { u64 n = 0, c[NSUB] = {0}; for (int t = 0; t < NT; t++) { n += SUBN[t]; for (int k = 0; k < NSUB; k++) c[k] += SUBP[t][k]; }
    const char *nm[8] = {"A val", "E val", "W val", "A xor", "E xor", "W xor", "E mod", "A mod"};
    printf("diag step %d over %llu trials (marginal pass rates):\n", DIAG, (unsigned long long)n);
    for (int k = 0; k < NSUB && n; k++) { if (!c[k] && k >= 8) break; printf("  %-6s%s%d 2^%.3f\n", k < 8 ? nm[k] : "extra", k < 8 ? "" : "#", k < 8 ? 0 : k - 8, log2((double)c[k] / n)); } }
  { u64 m[8] = {0}; for (int t = 0; t < NT; t++) for (int k = 0; k < 8; k++) m[k] += J[t].mult[k];
    printf("first blocks by number of S elements passing step 16:"); for (int k = 0; k < 8; k++) printf(" %d:%llu", k, (unsigned long long)m[k]); printf("\n"); }
  printf("  full survivors %llu, collisions %llu\n", (unsigned long long)dep[RR + 5], (unsigned long long)coll);
  return 0;
}
```

## Appendix B. Outputs

### `python3 verify_sfs.py PAPER_TXT` (file verify.txt)

```
r37: hash(M) ok True, hash(M') ok True; extra conditions parsed 31
  symbols {'=': 3412, 'n': 45, 'u': 68, '0': 121, '1': 142, '+': 20}
  orientation M unprimed (wrong): 113 symbol failures
  orientation M' unprimed, printed relations: 1 failures [('extra', 'A', 16, 29, '=', 'A', 17, 29, 1, 0)]
    orientation: A16[29] = A17[29] holds on the primed message (a differing bit); on the unprimed one it reads A16[29] != A17[29]
  orientation M' unprimed, relations as used: 0 failures
  + positions (word, step, bit, value on M): [('E', 5, 7, 0), ('E', 5, 6, 0), ('E', 6, 7, 0), ('E', 6, 6, 0), ('E', 8, 25, 1), ('E', 9, 25, 1), ('E', 9, 14, 1), ('E', 9, 0, 0), ('E', 10, 14, 1), ('E', 10, 0, 0), ('E', 13, 30, 1), ('E', 13, 17, 1), ('E', 14, 30, 1), ('E', 14, 17, 1), ('E', 15, 4, 1), ('E', 16, 24, 0), ('E', 16, 15, 1), ('E', 16, 4, 1), ('E', 17, 24, 0), ('E', 17, 15, 1)]
r38: hash(M) ok True, hash(M') ok True; extra conditions parsed 47
  symbols {'=': 3539, 'n': 52, 'u': 58, '0': 109, '1': 120, '+': 26}
  orientation M unprimed (wrong): 110 symbol failures
  orientation M' unprimed, printed relations: 1 failures [('extra', 'W', 25, 4, '=', 'W', 25, 9, 1, 0)]
    index misprint: W25[4] = W25[9] read as W25[4] = W25[6]
  orientation M' unprimed, relations as used: 0 failures
  + positions (word, step, bit, value on M): [('E', 5, 31, 0), ('E', 5, 30, 0), ('E', 5, 29, 0), ('E', 6, 31, 0), ('E', 6, 30, 0), ('E', 6, 29, 0), ('E', 6, 19, 1), ('E', 6, 11, 0), ('E', 7, 26, 0), ('E', 7, 19, 1), ('E', 7, 11, 0), ('E', 8, 26, 0), ('E', 11, 6, 0), ('E', 12, 6, 0), ('E', 13, 7, 0), ('E', 14, 12, 0), ('E', 14, 7, 0), ('E', 15, 12, 0), ('E', 16, 18, 0), ('E', 16, 4, 1), ('E', 17, 24, 1), ('E', 17, 18, 0), ('E', 17, 15, 1), ('E', 17, 4, 1), ('E', 18, 24, 1), ('E', 18, 15, 1)]
```

### `python3 check_step2.py 37` (file check_step2_37.txt)

```
R 37: steps 0..13 of the second block reproduce the Step-1 values for 2000 of 2000 random first blocks
```

### `exp37 S; NOS16=1 exp37 S; exp37 LIST` (file s37.txt)

```
S: E14 free bits 9, W14 candidates 2, |S| = 32 (all 32); SFS (W14,W15) = (bd1d3f7b,7dd43a81) in S: yes
S: E14 free bits 9, W14 candidates 2, |S| = 4096 (all 4096); SFS (W14,W15) = (bd1d3f7b,7dd43a81) in S: yes
S: E14 free bits 9, W14 candidates 2, |S| = 32 (all 32); SFS (W14,W15) = (bd1d3f7b,7dd43a81) in S: yes
bd1d3f7b fdb41680
bd1d3f7b fdb41681
bd1d3f7b fdb416a0
bd1d3f7b fdb416a1
bd1d3f7b fdb41a80
bd1d3f7b fdb41a81
bd1d3f7b fdb41aa0
bd1d3f7b fdb41aa1
bd1d3f7b fdb43680
bd1d3f7b fdb43681
bd1d3f7b fdb436a0
bd1d3f7b fdb436a1
bd1d3f7b fdb43a80
bd1d3f7b fdb43a81
bd1d3f7b fdb43aa0
bd1d3f7b fdb43aa1
bd1d3f7b 7dd41680
bd1d3f7b 7dd41681
bd1d3f7b 7dd416a0
bd1d3f7b 7dd416a1
bd1d3f7b 7dd41a80
bd1d3f7b 7dd41a81
bd1d3f7b 7dd41aa0
bd1d3f7b 7dd41aa1
bd1d3f7b 7dd43680
bd1d3f7b 7dd43681
bd1d3f7b 7dd436a0
bd1d3f7b 7dd436a1
bd1d3f7b 7dd43a80
bd1d3f7b 7dd43a81
bd1d3f7b 7dd43aa0
bd1d3f7b 7dd43aa1
```

### `exp37 RUN 31 12 21 21 16` (file run37.txt)

```
S: E14 free bits 9, W14 candidates 2, |S| = 32 (all 32); SFS (W14,W15) = (bd1d3f7b,7dd43a81) in S: yes
R 37 trials 2147483648 valid 2097970 (2^-9.999) step3 first blocks 2095337 x |S| 32
step3 trials 67050784; first failing step histogram (fail at i; survivors cumulative):
  fail@16 67050273  survive>16 511 (2^-17.00)
  fail@17 511  survive>17 0 (2^-99.00)
diag step 16 over 67050784 trials (marginal pass rates):
  A val 0 2^-1.000
  E val 0 2^-8.997
  W val 0 2^0.000
  A xor 0 2^-1.000
  E xor 0 2^0.000
  W xor 0 2^0.000
  E mod 0 2^0.000
  A mod 0 2^0.000
  extra #0 2^-1.000
  extra #1 2^-1.000
  extra #2 2^-1.000
  extra #3 2^-1.000
  extra #4 2^-1.000
  extra #5 2^-1.000
  extra #6 2^-1.000
first blocks by number of S elements passing step 16: 0:2094829 1:505 2:3 3:0 4:0 5:0 6:0 7:0
  full survivors 0, collisions 0
```

### `FIXED=1 CAPS="16:20,17:16,18:20,19:10,20:10,21:6,22:19" exp37 STAGE 13 12 41 22` (file stage37.txt)

```
S: E14 free bits 9, W14 candidates 2, |S| = 32 (all 32); SFS (W14,W15) = (bd1d3f7b,7dd43a81) in S: yes
STAGE R 37 samples 8192 |S| 32 kmax 22
  step 16: W-only conditions 2^0.000 (8589934592/8589934592 draws); rest: attempts 8589934592 passes 64909 dead 1224 rate 2^-17.014; step total 2^-17.014 (cumulative 2^-17.014)
  step 17: W-only conditions 2^0.000 (456654848/456654848 draws); rest: attempts 456654848 passes 55534 dead 2 rate 2^-13.005; step total 2^-13.005 (cumulative 2^-30.019)
  step 18: W-only conditions 2^0.000 (7304380416/7304380416 draws); rest: attempts 7304380416 passes 222908 dead 1880 rate 2^-15.000; step total 2^-15.000 (cumulative 2^-45.019)
  step 19: W-only conditions 2^0.000 (5208064/5208064 draws); rest: attempts 5208064 passes 80957 dead 0 rate 2^-6.007; step total 2^-6.007 (cumulative 2^-51.027)
  step 20: W-only conditions 2^0.000 (5208064/5208064 draws); rest: attempts 5208064 passes 40497 dead 0 rate 2^-7.007; step total 2^-7.007 (cumulative 2^-58.034)
  step 21: W-only conditions 2^0.000 (325504/325504 draws); rest: attempts 325504 passes 162494 dead 0 rate 2^-1.002; step total 2^-1.002 (cumulative 2^-59.036)
  step 22: W-only conditions 2^0.000 (0/0 draws); rest: attempts 2666528768 passes 1310913 dead 339 rate 2^-10.990; step total 2^-10.990 (cumulative 2^-70.026)
  reached step 22: 4747 samples
  per-start estimator over 8192 starts (272 nonzero): mean 2^-73.9606, standard error 0.0934 of the mean, mean - 1.96 SE 2^-74.2523 (W-only factor 2^0.000 included)
  m-weighted estimator (|S| prod / m): mean 2^-68.9763, standard error 0.0940 of the mean, mean - 1.96 SE 2^-69.2702; m histogram at collisions: 1:265 2:7 3:0 4:0 5:0 6:0 7:0
  natural step 23: survivors 4747
  natural step 24: survivors 272
  natural step 25: survivors 272
  natural step 26: survivors 272
  natural step 27: survivors 272
  natural step 28: survivors 272
  natural step 29: survivors 272
  natural step 30: survivors 272
  natural step 31: survivors 272
  natural step 32: survivors 272
  natural step 33: survivors 272
  natural step 34: survivors 272
  natural step 35: survivors 272
  natural step 36: survivors 272
  full collisions (SFS, own chaining value) 272
  example R 37 CV 84b03532 883efbcd bcc9750d d8840cb1 d5ef51d6 f8e65cf6 d9803e4c 3c2a6b0b
  M  d83b70ec 1f3acdd5 de31cee0 606e69d1 02c4b47b 8b96f2f8 5c6cf59e 4de6c646 bf0d78e1 6d1a90dd faa1d3e0 56aed439 cc2dbbc2 dd2ba0fc bd1d3f7b 7dd436a1
  M' d83b70ec 1f3acdd5 de31cee0 606e69d1 02c4b47b 8b96f2f8 7c6cf59e 49a6ce46 9f0d78e1 681b8277 faa9c7e0 56aed439 cc2dbbc2 dd2ba0fc b95d377b 5dd436a1
```
