# SHA-256 reduced to 32 steps: ordinary collision by truncating the 35-step attack of Li, Liu, Wang and Shi (CRYPTO 2026)

## 0. Claim and status

This package is bound to track `sha256-r32-exploratory`, target profile
`sha256-r32-prefix-v1` and cost model `collision-frontier-v5` (one 32-step
SHA-256 compression = 1 unit; any other 256-bit-RAM word operation = 1/C units
with C = 2224).

Claim: a classical two-block attack that outputs an ordinary collision of the
complete 32-step SHA-256 hash (standard IV, standard padding, all 256 output
bits) with algorithmic success probability at least 0.39 (computed lower bound
0.51, Section 8), total charged time at most 2^47.25 units under grouped
first-block evaluation (computed value 2^47.198, Section 12.2; ungrouped
full-compression value 2^47.385 < 2^47.5, Section 9), preprocessing at most
2^46.9 units, peak memory at most 2^35 bytes (computed value 2^34.415, Section 10).

The scored number is 47.25. It is dominated by a charged budget for the search
that produced the published differential characteristic (2^46.865 units,
heuristic H3, Section 11), because that search time is not published. The
attack phase itself (trials and Step 3) costs 2^44.75 units under grouped
first-block evaluation (2^45.66 units ungrouped).

What is published and what is ours:

- Published (source S): Yingxin Li, Fukang Liu, Gaoli Wang, Jiali Shi,
  "Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2",
  CRYPTO 2026, LNCS, pp. 289-320, doi:10.1007/978-3-032-35412-9_10; full
  version IACR ePrint 2026/1080. Used from S: the 35-step differential
  characteristic (S, Fig. 6), the search procedure that produced it (S, Sect. 3
  Model-1/2/3 and Sect. 4 Steps 1-4), the three-step attack framework (S,
  Sect. 4), the colliding 35-step pair (S, Table 3), S's count of 45 conditions
  on (A16, E16, E17, E18, E19, E20, W20, W22) and of 2^17.585 values of
  (W14, W15), and S's measured Step-2 rate 2^-20.92 (used only as a fallback
  comparison, Section 9).
- Ours (derived, not published): the truncation to 32 steps (Section 4,
  complete proof); the exact-conformance tests of Steps 2 and 3; our own
  construction of the precomputed table; the exact table statistic that
  predicts the 32-step matching rate (Section 7.2); the measurements of
  Section 7; the identification of one condition at step 19 that is not
  printed under S, Fig. 6 (Section 7.4); grouped first-block evaluation
  (Section 12.2); and all cost accounting.
- Novelty statement: we know of no published complexity for an ordinary
  collision on 32-step SHA-256. S (Sect. 3, Case-II) remarks that a 32-step
  semi-free-start (SFS) attack could be converted into a 32-step collision
  attack, but gives no complexity for it, and S's supplementary Tables 5-6 are a
  32-step SFS characteristic and SFS pair only.
- Verified 32-step collision certificate and organizer experiments (Section 12):
  an explicit 128-byte 32-step colliding pair (`certificates/message-a.bin`,
  `certificates/message-b.bin`, digest `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77`)
  found by this exact 32-step truncated route is attached in `certificates/manifest.json`
  and reconstructed by the organizer-executed experiment `fixed-witness-derivation`
  (`experiments/replay.py`), alongside modular-addition carry experiments (`r32-prob-Verify`, etc.).
  The published 35-step pair is NOT a 32-step collision (Section 5).

The required identifier `sha256-r32-nominal-v2` names the organizer's nominal
display reference (128), not an established attack. Three score-critical
heuristics and one supporting heuristic are declared in Section 11.

## 1. Target and notation

Words are 32 bits; + and - are modulo 2^32; ROTR_n is right rotation within 32
bits; SHR_n is logical shift. FIPS 180-4 functions:

```
Sigma0(x) = ROTR2(x) ^ ROTR13(x) ^ ROTR22(x)    Sigma1(x) = ROTR6(x) ^ ROTR11(x) ^ ROTR25(x)
sigma0(x) = ROTR7(x) ^ ROTR18(x) ^ SHR3(x)      sigma1(x) = ROTR17(x) ^ ROTR19(x) ^ SHR10(x)
IF(x,y,z) = (x & y) ^ (~x & z)                   MAJ(x,y,z) = (x & y) ^ (x & z) ^ (y & z)
W[i] = M[i] (i<16),  W[i] = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16] (i>=16)
```

We use the equivalent "alternative description" of the step function used by S.
For an input chaining value CV = (a,b,c,d,e,f,g,h) put
A[-1..-4] = (a,b,c,d) and E[-1..-4] = (e,f,g,h). For i = 0,1,...:

```
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])
```

(This is FIPS 180-4: E[i] = d + T1 and A[i] = T1 + T2 with d = A[i-4],
h = E[i-4].) The R-step compression returns
C_R(CV,M) = CV + (A[R-1],A[R-2],A[R-3],A[R-4],E[R-1],E[R-2],E[R-3],E[R-4]),
word-wise. The target hash executes steps 0..31 (R = 32) on every padded block,
with the standard constants K[0..31] at their original indices and the standard
IV. Our messages are 128 bytes, M0||M1, so the padded input is three blocks
M0, M1, P where P = 0x80000000, 14 zero words, 0x00000400 (bit length 1024).

Signed differences follow S: for a pair of values (x, x'), position j of the
32-character string (most significant bit first, so string position k is bit
31-k) is `n` if x[j]=0, x'[j]=1; `u` if x[j]=1, x'[j]=0; `=` if x[j]=x'[j];
`0`/`1` if x[j]=x'[j] equals 0/1. For a word X, FL(X) is the mask of n/u
positions. The prescribed modular difference of a row is
D(X) = sum over n-positions of 2^j minus sum over u-positions of 2^j.

Two test notions are used throughout.

- XOR-conformance of word X: X' = X xor FL(X).
- Sign values of X: the bits of X at the n/u positions equal the prescribed
  values (0 at `n`, 1 at `u`). XOR-conformance plus correct sign values is
  equivalent to X' - X = D(X) together with X' = X xor FL(X).
- "XOR-conformance at step i" (for E or A): with x' = x xor FL(x) for every
  input word of the step equation, the step equation evaluated on the primed
  words returns E'[i] (resp. A'[i]) = E[i] xor FL(E[i]) (resp. A). This is an
  equality test of 32-bit words.

## 2. The 35-step characteristic of S (Fig. 6), transcribed

Unprimed values x belong to the block labelled M'_1 in S, Table 3; primed values
x' to M_1. Rows 23..34 of all three columns are entirely `=` in S, Fig. 6.

```
  i   nabla A[i]                        nabla E[i]                        nabla W[i]
 -4   ================================  ================================
 -3   ================================  ================================
 -2   ================================  ================================
 -1   ================================  ================================
  0   ================================  ================================  ================================
  1   ================================  ================================  ================================
  2   ================================  ================================  ================================
  3   ================================  =====1=====011======0======0====  ================================
  4   ==n=============================  ==n0=0=1===100=0==0=1===0==1=0=1  ==n=============================
  5   =====n===n===n=u====n===u==u====  01011u001n=nuu=11000n=1=101u=100  =====u===u==========n===========
  6   ================================  101n=0=1=1=n1111==n0u===n=0n=n=u  ==n=============================
  7   ================================  10u0=1=101==00=n==0=0===0==0=0=0  =======n=======u===u====u=1=u=u=
  8   ================================  uuu1=0=111=0=0=01=1=01==1==1=1=0  ============u=======uu==========
  9   ==========u====================u  11=10n0nuuu00n0u101=n11=u01u=unn  ================================
 10   ================================  un111111001001111=010u=u0+001100  ================================
 11   ====n=========u=u=======u==n====  1011n111100010u1u0111111u+nu1001  ================================
 12   =un===u=n=======n===============  001uuu11uuuuuuuu11n1000n1uuu1001  =====n===n==========u===========
 13   ================================  =n1111uu1n00000u1u0=nnn01111010n  ==u=============================
 14   ==u=============================  =0=100110000000=101=0000=110===0  ================================
 15   ================================  =1====0011===u10001=011===0n===1  ================================
 16   ================================  ======u=n====1==n=====0===01====  ================================
 17   ================================  ======0=0====1==0==========1====  ================================
 18   ================================  ==u===1=0=======1====1==========  ================================
 19   ================================  ==0=============================  ================================
 20   ================================  ==1=============================  =====0=nn=====0=u=1=============
 21   ================================  ================================  ================================
 22   ================================  ================================  ==n=============================
23-34 all `=` in all three columns
```

(The `+` symbol printed by S in rows E10 and E11 is not defined in S; it is
treated as `=` here. Both published messages agree on those bits.)

Two-bit conditions printed under S, Fig. 6 (X[a,b] = Y[c,d] means X[a]=Y[c]
and X[b]=Y[d]):

```
W4[1,8] != W4[12,25], W4[18] = W4[14], W5[0,1,30] = W5[28,18,9], W6[1,8] = W6[12,25], W6[18] != W6[14]
W7[22,13,23] != W7[18,9,8], W7[11,14,20] = W7[22,31,31], W8[0,14,21] = W8[28,25,6]
W8[31,23,30,15,22,8] != W8[27,2,15,26,7,4], W20[4,31] = W20[6,22], W20[31,30,25,21] != W20[1,0,16,14]
W22[4,31] = W22[6,22], W22[27] != W22[20]
E4[10] != E4[15], E5[3,21] = E5[8,8], E6[9,27,9,8] != E6[23,14,14,27], E6[1,1,23,6] = E6[6,15,10,25]
E7[21,10] != E7[3,15], E16[28,20,20,6] = E16[1,7,2,11], E16[30,28,10] != E16[12,10,29], E18[24] != E18[11]
E18[2] = E18[16]
A3[29] = A2[29], A3[29] != A5[29], A3[26,4] = A4[26,4], A3[22,18,16,11,7] != A4[22,18,16,11,7], A14[9] = A14[20]
A14[18,8] = A14[6,17], A13[30,25,23] = A14[30,25,23], A13[15] != A14[15], A13[29] != A15[29], A15[29] = A6[29]
```

Transcription check (ours). We recomputed the published pair (Section 5) and
compared every symbol: all 362 non-`=` single-bit symbols (21 in the A column,
315 in E, 26 in W) agree with the pair, and every `=` position has equal bits.
Of the 73 printed two-bit conditions, 66 hold for the pair and 7 do not:
W20[4]=W20[6], W20[31]=W20[22], E7[21]!=E7[3], E7[10]!=E7[15],
A14[18]=A14[6], A14[8]=A14[17] and A15[29]=A6[29]. The pair satisfies the
opposite relation in the E7 and A14 cases and satisfies A15[29]=A16[29], which
is the condition that absorbs the A14[29] difference in MAJ at step 17, so we
read "A6" as a misprint of "A16". Our algorithm uses printed conditions only to
define its precomputed sets (Section 6), with these pair-consistent readings
(E7 relations as "=", A14[18,8] != A14[6,17], A15[29] = A16[29], and the two
W20 equalities dropped); every attack-critical test in Steps 2 and 3 is an exact
equality test, not a printed condition.

Counting the printed conditions on (A16, E16, E17, E18, E19, E20, W20, W22):
E16 has 7 single-bit and 7 two-bit, E17 5, E18 5 + 2, E19 1, E20 1, W20 6 + 6,
W22 1 + 3, A16 1 (A15[29] = A16[29]): 14 + 5 + 7 + 1 + 1 + 12 + 4 + 1 = 45,
exactly S's number. Section 7.4 shows that one further condition,
E16[29] = E17[29], is necessary at step 19 and is not printed; we use 46.

## 3. The 35-step attack of S (summary with locations)

All statements below are from S, Sect. 4 ("The First Practical Collision Attack
on 35-step SHA-2"); numbers are copied exactly.

- Characteristic search (S, Sect. 4, Steps 1-4, using the SAT/SMT tool of
  ePrint 2024/349): Step 1 minimises the total Hamming weight of the message
  differences in W0..W34 with differences only in (W4..W8, W12, W13, W20, W22);
  Step 2 minimises t_E, the number of differences in E14..E18; Step 3 imposes
  a threshold t_r on the A-difference weight and lowers it until the solver
  finds no solution; Step 4 minimises the E-difference weight in E4..E18. Before
  this, S, Sect. 3 runs three exploratory message-expansion models (Model-1,
  Model-2 and Model-3, giving Case-III-1, Case-III-2 and Case-IV, Fig. 5). S
  reports no running time for any of these searches.
- Starting solution (S, Sect. 4, paragraph after Step 3 of the attack): S finds
  one valid solution of the characteristic up to step 13 with a SAT solver and
  writes (subscripts transliterated) "based on this solution, we fix (E_i)
  5<=i<=13, (A_i) 1<=i<=13, and (W_i) 9<=i<=13". S then re-enumerates E5, E6
  and E7 (2^3, 2^4 and 2^11 values), then enumerates W4 (checked against E8)
  and W7 (checked against E3), and obtains 2^29.1824 valid tuples
  (A[-1..13], E[3..13], W[7..13]) in its table TAB2.
- Complexity evaluation (S, Sect. 4, "Complexity Evaluation"): finding the
  Step-1 solution takes about 2^34.3 (unit not stated); a valid first block M0
  is found with probability about 2^-20.92 per 35-step compression; there are
  2^17.585 possible (W14, W15) and 45 conditions on (A16, E16, E17, E18, E19,
  E20, W20, W22); hence 2^27.415 valid tuples and 2^48.335 compressions are
  needed.
- Experimental verification (same paragraph): S used a server with 128
  threads, 378 GB of memory and two AMD EPYC 9354 CPUs and found the pair of
  S, Table 3.

## 4. The truncation argument (ours, complete)

Lemma 1. Let CV be any chaining value and let two blocks have expanded words
W, W'. If A[j] = A'[j] and E[j] = E'[j] for j = 19, 20, 21, 22, and W[j] = W'[j]
for 23 <= j <= 31, then C_32(CV, M) = C_32(CV, M').

Proof. By the step equations, (A[i], E[i]) is a function of
(A[i-4..i-1], E[i-4..i-1], W[i]). By induction on i = 23, ..., 31 the two
computations have equal (A[i], E[i]), since all inputs are equal. C_32 adds the
common CV to (A[31],A[30],A[29],A[28],E[31],E[30],E[29],E[28]), which are equal.

Lemma 2. If CV1 is common and C_32(CV1, M1) = C_32(CV1, M1') with M1 != M1',
then the 128-byte messages X = M0||M1 and X' = M0||M1' are distinct and have
equal complete 32-step hashes.

Proof. Both have bit length 1024, so both get the same padding block P; the
chaining value after M1 is equal, hence so is C_32(., P), which is the digest.

Corollary (truncation). Rows 19-22 of the A and E columns and rows 23-34 of
the W column of S, Fig. 6 are all `=`. Hence any second-block pair that conforms
to S's characteristic up to step 22 and in W[16..31] satisfies Lemma 1, and with
Lemma 2 the two-block messages collide for the 32-step hash. The 35-step
characteristic has no condition after step 22 in the A/E columns, and its W
conditions after step 22 are the zero rows W23..W34; at 32 steps the rows
W32..W34 are simply not used. So the 32-step attack needs exactly the
conditions of the 35-step attack at steps 0-22 plus the zero rows W23..W31: no
condition of S's Step 3 disappears and none is added. The only change is that
every block, including the first block M0, is compressed with 32 steps, so the
chaining value CV1 that must match TAB2 is C_32(IV, M0), not C_35(IV, M0); we
predict and measure the matching rate for C_32 directly (Section 7).

Why no message-expansion difference survives to W31. With nonzero differences
only in W4..W8, W12, W13, W20, W22 (rows of Fig. 6), the recurrence
W[t] = sigma1(W[t-2]) + W[t-7] + sigma0(W[t-15]) + W[t-16] gives: W16, W17, W18,
W25, W26, W30, W31 depend only on difference-free words; W19 (W12, sigma0 W4),
W21 (sigma0 W6, W5), W23 (sigma0 W8, W7), W24 (sigma1 W22, W8), W27 (W20,
sigma0 W12), W28 (sigma0 W13, W12), W29 (W22, W13) need cancellations, which are
part of the characteristic (rows W19..W31 are `=`). W35 = sigma1(W33) + W28 +
sigma0(W20) + W19 is the first word whose difference cannot cancel, which is why
S stops at 35 steps. Our Step 3 (Section 6) checks every row W16..W31 exactly.

## 5. Evidence from the published 35-step pair (our recomputation)

Table 3 of S (we removed the line-break spaces inside some printed words):

```
M0  = a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a
      cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8
M1  = c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665
      6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1
M1' = c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef
      6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1
```

Our recomputation (an independent SHA-256 implementation whose results agree
with the organizer's `verifier/hash_functions.py:digest` on every value below
that is a complete digest):

1. With 35 steps the pair collides. The two-block chaining value
   C_35(C_35(IV, M0), M1) = C_35(C_35(IV, M0), M1') is c6209b2b 5e3fd4c8
   96087364 046304ab bbc6dad9 403a26d1 018e351f e444451f; this is the value S
   prints as "hash" under Table 3, i.e. without the padding block. The complete
   padded 35-step digest of both 128-byte messages is
   8b32c7f0ffa0e0f8a218eecb9470f7e0b0da05ccd061b20b37107cb618c51c5d.
2. Difference trace of the second block from CV1 = C_35(IV, M0) =
   c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2:
   nonzero W differences exactly at {4,5,6,7,8,12,13,20,22}; nonzero A
   differences at {4,5,9,11,12,14}; nonzero E differences at
   {4,...,13,15,16,18}. The last step with any A/E difference is 18; the last
   W difference is W22. The signed differences coincide with Fig. 6 symbol by
   symbol (Section 2).
3. Truncation demonstrated: from the same CV1, the 32-step compressions of M1
   and M1' are equal (22b41993 9458056c e7f8a711 998eb4c0 544191e8 b7a599b1
   91dcfc3a 0d403a72). This is a 32-step semi-free-start collision only (CV1 is
   a 35-step value), so it is NOT claimed as a solution; it instantiates
   Lemma 1.
4. Control: the complete padded 32-step digests of M0||M1 and M0||M1' differ
   (973018980b0c3bd3da0deea9c804113ab4be08195c853fe24bfd07d525f3006e vs
   9a99b338a554379f943507cf724b4fbbb317e1fe89f861ac9921cb77e5e83f16), because
   C_32(IV, M0) does not match the table. A fresh first block is required,
   which is what the algorithm below searches for.

## 6. The algorithm (fully specified)

Fixed advice (all explicit; about 8 KB): the constants, the characteristic of
Section 2, and the values of S's starting solution T obtained from the pair
(x = M'_1 trajectory from the 35-step CV1):

```
A4..A13 = 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E8..E13 = f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4
W12, W13 = 41b22a2c 6d12f88a
```

These are the values S fixes after its Step 1 (S builds TAB2 from a single
solution, quoted in Section 3, and the published pair arises from that TAB2),
so their cost is S's reported Step-1 cost (charged in Section 9). Primed values
of fixed words are X' = X xor FL(X). Appendix A gives the predicates below as
source text.

P1 (lists). L4 = all E4 with the printed single-bit E4 conditions and
E4[10] != E4[15] (2^18 candidates, 131,072 kept). L7 = all W7 with the printed
W7 single-bit conditions and its six two-bit conditions (2^25 candidates,
524,288 kept).

P2 (combinations). For every (E5, E6, E7) satisfying their printed single-bit
conditions (2^5 * 2^12 * 2^15 = 2^32 candidates) compute
A3 = E7 - A7 + Sigma0(A6) + MAJ(A6,A5,A4), A2 = E6 - A6 + Sigma0(A5) +
MAJ(A5,A4,A3), A1 = E5 - A5 + Sigma0(A4) + MAJ(A4,A3,A2) and W9, W10, W11 from
the E-equations of steps 9-11. Keep the combination iff all printed single-bit
conditions on A1..A3, W9..W11 and all (read as in Section 2) two-bit conditions
among words already determined hold, and XOR-conformance holds for the
A-equations of steps 5..13 and the E-equations of steps 9..13. Result: 10,240
combinations.

P3 (table, built in place). For each kept combination and each e4 in L4:
A0 = E4 - A4 + Sigma0(A3) + MAJ(A3,A2,A1), W8 from the step-8 E-equation; keep
iff W8's printed conditions, the two-bit conditions among determined words, and
XOR-conformance at steps 4 (A) and 8 (E) hold (155,008 kept (combination, E4)
pairs). For each kept pair and each w7 in L7: E3 = E7 - A3 - w7 - Sigma1(E6) -
IF(E6,E5,E4) - K7 and A[-1] = E3 - A3 + Sigma0(A2) + MAJ(A2,A1,A0); keep iff E3's
printed single-bit conditions, XOR-conformance at steps 3 (A) and 7 (E),
sigma0(W8') + W7' = sigma0(W8) + W7 (zero W23 difference) and the remaining
two-bit conditions hold. Result: TAB2 with N = 1,396,774,912 = 2^30.379 tuples.
Each tuple is a 16-byte record (A[-1], combination index, index in L4, index
in L7). The table is bucketed by the top 27 bits of A[-1] without any auxiliary
copy: pass 1 runs the W7 loop once and only counts records per bucket in a
2^27-entry array of 32-bit counters; a prefix sum turns the counts into bucket
start offsets; pass 2 runs the same loop again and stores each record at
offset[bucket]++ inside one N * 16-byte array. Afterwards offset[b] is the end
of bucket b and the start of bucket b+1. Peak memory is the record array plus
the offset array (Section 10). Records inside a bucket are not sorted.

P4 ((W14, W15) list). E14 = c14 + W14 and A14 = E14 + d14 with constants of T,
and similarly for step 15. Enumerating E14 over its printed single-bit
conditions (2^8 values), keeping A14's printed conditions (12 values remain),
then E15 over its printed single-bit conditions (2^15 values) and
A13[29] != A15[29] gives exactly 196,608 = 12 * 2^14 = 2^17.585 pairs
(W14, W15), equal to S's count; all of them also pass XOR-conformance at steps
14 and 15. For each entry we store W14, W15, sigma1(W14), sigma1(W15) and the
step-16 constants E16 - W16, E16' - W16, A16 - E16, A16' - E16' (all
independent of M0). The 196,608 entries form 12 groups of 2^14 with a common
W14.

Main loop. For t = 1, ..., T with T = ceil(2^45.3):

1. Draw M0 uniformly (two fresh random 256-bit words); CV1 = C_32(IV, M0).
2. Step 2. For every TAB2 record in bucket (A[-1] >> 5) whose stored A[-1]
   equals the first word of CV1: compute E0, E1, E2 from the A-equations of
   steps 0..2 (A[-4..-1] from CV1, A0..A2 from the tuple) and W0..W6 from the
   E-equations. Accept, with early abort in this order, iff (a) W4 has its sign
   value; (b) sigma0(W4') + W12' = sigma0(W4) + W12 (zero W19 difference);
   (c) W5 has its three sign values; (d) W6 has its sign value; (e)
   XOR-conformance holds for the E-equations of steps 0..6 and the A-equations
   of steps 0..2; (f) sigma0(W6') + W5' = sigma0(W6) + W5 (zero W21
   difference); (g) (W13' - W13) + (sigma0(W5') - sigma0(W5)) + (W4' - W4) =
   D(W20). Call an accepted (M0, tuple) a valid tuple.
3. Step 3. For a valid tuple, for every entry of the P4 list: M1 = (W0..W15),
   M1' = M1 xor FL(W) (differences in W4..W8, W12, W13 only); for i = 16, ...,
   31 in order, with early abort: compute W[i] and W'[i] and require
   W'[i] = W[i] xor FL(W[i]), and for i = 20 and i = 22 also the sign values of
   W[i]; for i <= 22 then compute step i for both computations and require
   A'[i] = A[i] xor FL(A[i]) and E'[i] = E[i] xor FL(E[i]). If all pass,
   Lemma 1 gives C_32(CV1, M1) = C_32(CV1, M1'); recompute both complete
   three-block 32-step hashes, compare all 256 bits, and output
   (M0||M1, M0||M1').
4. Stop after T trials, or after K_max = 2^28.4 Step-3 invocations.

Correctness is unconditional: every output is checked by full recomputation
(Lemma 2 ensures distinct messages). Only the success probability uses
heuristics. The sign checks of W20 and W22 in Step 3 make the test slightly
stricter than XOR-conformance alone; all measured Step-3 rates in Section 7 were
taken with exactly this stricter test.

## 7. Prediction and measurements

All measured counts below come from our own C implementation (Appendix A gives
the exact predicates as source text, the generator and the seeds). They were not
executed by the organizer. Section 7.2 gives an analytic prediction of the
score-critical rate q that does not depend on any random sampling.

### 7.1 Table construction (P1-P4), exact iteration counts

2^32 combination candidates scanned, 10,240 kept; 1,342,177,280 = 2^30.32 E4
iterations; 155,008 kept pairs; 81,268,834,304 = 2^36.24 W7 iterations;
1,396,774,912 tuples; P4: 256 + 12 * 32,768 = 393,472 iterations. For the
experiments the table was split into four parts by combination index mod 4
(sizes 346,078,720; 274,975,232; 366,456,320; 409,264,640).

### 7.2 Analytic prediction of q (ours)

Fix a tuple t and let the first word of CV1 equal its A[-1]. The remaining
words b = A[-2], c = A[-3], d = A[-4] of CV1 enter Step 2 as follows (step
equations of Section 1): E0 = A0 + d - Sigma0(A[-1]) - MAJ(A[-1], b, c), E1 =
A1 + c - Sigma0(A0) - MAJ(A0, A[-1], b), E2 = A2 + b - Sigma0(A1) -
MAJ(A1, A0, A[-1]). So, for uniform (b, c, d): E2 is uniform (through b), E1 is
uniform given b (through c), E0 is uniform given (b, c) (through d). Hence
W4 = E4 - A0 - E0 - ... is uniform and independent of (E1, E2); W5 = E5 - A1 -
E1 - ... is uniform and independent of (E2, W4); and W6 = Y_t - E2 with a
tuple constant Y_t = E6 - A2 - Sigma1(E5) - IF(E5,E4,E3) - K6. The tests then
behave as follows.

```
test                              derivation                                                predicted       measured (run 2)
(a) W4 sign                       one bit of a uniform W4                                   1/2             0.5000
(b) W19 = 0                       sigma0 xor-difference of W4 is {11,22,26}; exactly one   1/8             0.1250
                                  sign pattern of sigma0(W4) at these bits gives -D(W12)
(c) W5 signs                      three bits of a uniform W5                                1/8             0.1250
(d) W6 sign                       one bit of W6 = Y_t - E2, E2 uniform                      1/2             0.5001
(e) steps 0-4 (E), 0-2 (A)        no input of these equations differs except W4 at step     1               1.0000
                                  4, whose difference equals D(E4) after (a)
(e) step 5 (E)                    the only M0-dependent difference is IF(E4,E3,E2) at bit   see below       0.6960
                                  29, i.e. it depends on E2[29] only
(e) step 6 (E)                    every input difference is fixed by the tuple and (d)      see below       0.4411
(f) W21 = 0                       sigma0 xor-difference of W6 is {11,22,26}; one sign       1/8             0.1246
                                  pattern cancels D(W5)
(g) W20 difference                sigma0 xor-difference of W5 is {15,23,25}; one sign       1/8             0.1248
                                  pattern gives D(W20) (D(W13) + D(W4) = 0)
```

For (e) we enumerated TAB2 exactly (no sampling): for every tuple, step 6 holds
for all M0 or for none (609,229,824 of the 1,396,774,912 tuples, i.e. 43.6%,
pass), and step 5 holds for exactly one value e*(t) of E2[29] in every tuple.
Since (d) and E2[29] are correlated through W6 = Y_t - E2, we computed for
every tuple the exact probability P_t = Pr[E2[29] = e*(t) and W6[29] = 0] over
uniform E2 (it depends only on Y_t mod 2^30). With the bits in (a)-(c), (f),
(g) treated as above,

q_pred = 2^-32 * 2^-1 * 2^-3 * 2^-3 * 2^-3 * 2^-3 * sum over t of ok6(t) * P_t
       = 2^-45 * 214,235,406.8 = 6.0889e-6 = 2^-17.3254.

The approximations are: (i) the four CV1 words (a, b, c, d) of C_32(IV, M0)
behave as uniform for these tests; (ii) the sign pattern in (f) is treated as
independent of the conditioning on W6[29] and E2[29] (W6's other bits are
slightly biased by that conditioning). The predicted conditional rate of (e)
given (d), 2 * 0.15338 = 0.3068, matches the measured 0.3070
(1,675,075 / 5,456,132).

### 7.3 Measured q (four independent runs, all reported)

Each run compresses independent pseudo-random M0 with C_32, looks them up in one
table part, and counts valid tuples.

```
run  seed(s)          part  trials           matches       valid   predicted (7.2)
1    11,12,13,14      0     4,294,967,292    346,009,191   6,147   6,269.6
                      1     4,294,967,292    275,021,065   5,486   5,405.5
                      2     4,294,967,292    366,489,445   6,293   6,341.6
                      3     4,294,967,292    409,228,827   8,069   8,135.2
2    101,102,103,104  0     4,294,967,292    346,089,290   6,272   6,269.6
                      1     4,294,967,292    274,987,488   5,309   5,405.5
                      2     4,294,967,292    366,449,236   6,210   6,341.6
                      3     4,294,967,292    409,269,312   8,268   8,135.2
3    777              3     1,073,741,820    102,310,424   1,921   2,033.8
4    15               3     4,294,967,292    409,244,836   8,204   8,135.2
```

Run 3 is a confirmation rerun on part 3 with a quarter of the trials; it is
2.5 standard deviations below its prediction and is included in the pool. Run 4
is the printed-condition run of Section 7.4. Matches per trial agree with
N / 2^32 = 0.32521 (run 1: 0.32521; run 2: 0.32522).

Pooled estimate. Since the parts partition TAB2, q is the sum of the per-part
rates: part 0 12,419 / 8,589,934,584, part 1 10,795 / 8,589,934,584, part 2
12,503 / 8,589,934,584, part 3 26,462 / 13,958,643,696. This gives
q = 2^-17.3337 with relative standard deviation 0.41% (Poisson), a 99% one-sided
lower bound 2^-17.3476 and upper bound 2^-17.3200. The pooled estimate is 0.58%
below the analytic prediction (per-part z-scores -1.07, -0.15, -1.60, +0.14).

Overdispersion check (run 2): trials with exactly 2 valid tuples in one part
were 3, 4, 2, 4 (13 in total), none had 3 or more; the variance inflation of the
per-trial count is therefore below 0.1%.

Controls (run 1, part 0, same trials): C_35 first blocks gave 6,355 valid and
uniformly random CV1 (no compression) gave 6,415, versus 6,147 for C_32 in
run 1 and 6,272 in run 2 (prediction 6,269.6). We use only C_32 counts.

For comparison, S's table (2^29.18 tuples, conditions tested on W4..W6) gave
2^-20.92 per M0. Our table is larger and our Step 2 accepts exactly the M0 that
follow the characteristic through step 6 (with zero W19, W21 differences and the
prescribed W20 modular difference), instead of a sufficient set of bit
conditions; Section 7.2 explains the resulting rate. W4, W5, W6 influence later
steps only through W19, W20, W21 (tested exactly) and through W22 = sigma1(W20)
+ W15 + sigma0(W7) + W6, where W6 enters additively with fixed difference; so
accepting more M0 in Step 2 does not change what Step 3 must achieve.

### 7.4 Step 3: tests per stage, predicted and measured rates

Stage i (i = 16..22) of Step 3 tests, in this order, the W[i] row and then
XOR-conformance of A[i] and E[i]. W16, W17, W18 have zero difference
automatically; W19 and W21 are zero by Step 2; the W20 and W22 tests are the
XOR pattern plus sign values. W23..W31 are tested after stage 22. Predicted
cumulative rates count conditions as fair independent bits; the condition
mapping is ours, derived from the step equations.

```
stage  tested at this stage                                 conditions consumed               cum. pred.  measured (pooled)
16     A16, E16 xor-conformance                             3 of E16's 14 (measured 1/8)      2^-3        1,528,108,551  2^-3.000
17     A17, E17                                             other 11 of E16, A16 (1)          2^-15       373,324        2^-14.999
18     A18, E18                                             E17 (5), E18[29] sign (1)         2^-21       5,823          2^-21.002
19     A19, E19                                             other 6 of E18, E16[29]=E17[29]   2^-28       41             2^-28.15
20     W20 xor + 3 signs, A20, E20                          W20 signs (3), E19[29]=0 (1)      2^-32       5              2^-31.19
21     A21, E21                                             E20[29]=1 (1)                     2^-33       4              2^-31.51
22+    W22 xor + sign, A22, E22, W23..W31 zero              remaining W20 (9), W22 (4)        2^-46       0
```

Pooled over runs 1-4 (12,224,888,832 candidates from 62,179 valid tuples).
Predicted counts at stages 16-21: 1,528,111,104; 373,074; 5,829; 45.5; 2.8;
1.4.

Step-by-step justification of the mapping. Step 17 consumes the E16 conditions
(Sigma1(E16) and IF(E16,E15,E14) at step 17). Step 18: with the printed E17
values, IF(E17,E16,E15) absorbs every E16 and E15 difference, so
E18' - E18 = A14' - A14 = -2^29, which XOR-conforms iff E18[29] = 1 (the `u`).
Step 19: IF(E18,E17,E16) at bit 29 outputs E17[29] for one computation and
E16[29] for the other (E18[29] differs, E16[29] and E17[29] do not); every other difference in the E19 equation (E15, Sigma1(E18), and
IF at bit 23) sums to less than 2^25 in absolute value and cannot cancel
+-2^29, so E19 can conform only if E16[29] = E17[29]. This condition is not
in S's printed list; the pair satisfies it (both bits are 1), and the measured
rate through step 19 (41 against 45.5 predicted with it; 91 would be predicted
without it) supports it. Step 20: only E18[29] differs among the IF inputs and
is absorbed iff E19[29] = 0; D(E16) + D(W20) = 0 exactly (0xfe808000 +
0x017f8000), so, with E16 carrying its sign values (E16 conditions consumed at
step 17), E20 conforms once W20 has its sign values. Step 21:
IF(E20,E19,E18) absorbs E18[29] iff E20[29] = 1.

Why 3 of 22 passing step 20 in run 1 does not contradict the 45-condition
count: at stage 20 only 4 conditions are consumed (above). The other 9 printed
W20 conditions and the 4 printed W22 conditions control the carries of
sigma1(W20) in W22 and of sigma1(W22) in W24 and are tested at stage 22 and in
W23..W31.

Remaining conditions after step 21 (supporting evidence that 2^-13 is not
optimistic). With W20 uniform subject to its modular difference and three sign
values, W22 = sigma1(W20) + X and W24 = sigma1(W22) + Y for uniform X, Y, and
the (sigma0(W7), W6, W8) differences of the published pair's tuple, a Monte
Carlo of 2^21 samples gave: W20 sign values 2^-3.00; W22 XOR pattern and sign
given that 2^-7.94; W24 = W24' given both 2^-3.07. So the tests after step 21
cost about 2^-11.0 for that tuple, against the 2^-13 that the printed count
assigns. W27, W28 and W29 cancel deterministically (D(W20) + the sigma0(W12)
difference, W12 and W13 fixed; D(W22) + D(W13) = 0).

Printed (sufficient) conditions on the unprimed computation (run 4, part 3,
seed 15, 1,612,972,032 = 8,204 * 196,608 candidates): E16 and A16 (15
conditions) 49,332 (independence predicts 49,224; the same run's exact
conformance through step 17 is also 49,332); adding E17 (5) 1,514 (predicts
1,538); adding E18 (7) 9 (predicts 12.0).

No full conformance was observed; none is expected at this sample size (2^33.5
candidates against a per-candidate rate near 2^-46). Sanity check (every run):
the published pair, with its own tuple, its (W14, W15) and its 35-step CV1,
passes our Step 2 and all Step-3 stages, its (W14, W15) is in the P4 list, and
its 32-step second-block compressions are equal.

## 8. Success probability

The T trials use independent random M0, so with a fixed precomputation their
outcomes are independent and each succeeds with the same probability s. Hence
P(success) = 1 - (1 - s)^T >= 1 - exp(-sT), with no further assumption.

Per trial. Let V be the number of valid tuples in a trial and S_1 the event
that Step 3 succeeds on the first valid tuple. Then s >= Pr[V >= 1] * r with
r = Pr[S_1 | V >= 1], and Pr[V >= 1] >= E[V] - E[C(V,2)] = q - E[C(V,2)]. From
run 2, pairs of valid tuples in one part occurred 13 times in 4 * 2^32
part-trials, i.e. 2^-28.3 per whole-table trial; allowing a factor 2.5 for
pairs across parts, E[C(V,2)] <= 2^-27 = q * 2^-9.6. So Pr[V >= 1] >=
q (1 - 2^-9.6).

Step 3 (heuristic H2). Let X be the number of the 196,608 P4 candidates that
fully conform. By Section 7.4, each conforms with probability p >= 2^-46
(28 conditions through step 19 that are supported by the measurement, 5 at
steps 20-21, and the 13 remaining printed conditions). Bonferroni:
r >= E[X] - E[C(X,2)]. Candidates of one valid tuple share W14 within a group
of 2^14, and W16, W18, W20 depend only on W14 and the tuple, so the 12 printed
W20 conditions are common to a group. Charging them once per group:
E[C(X,2)] <= 12 * C(2^14, 2) * 2^-12 * (p * 2^12)^2 + C(196,608, 2) * p^2
= 2^30.58 * 2^-80 + 2^34.17 * 2^-92 <= 2^-49.3, against E[X] = 2^17.585 *
2^-46 = 2^-28.415. So r >= 2^-28.415 * (1 - 2^-20).

Heuristic H1: q >= 2^-17.36 (below the pooled 99% lower bound 2^-17.348 and the
analytic prediction 2^-17.325). Then
s >= 2^-17.36 * (1 - 2^-9.6) * 2^-28.415 * (1 - 2^-20) >= 2^-45.777, and for
T = 2^45.3: sT >= 2^-0.477 = 0.718, P(success) >= 1 - e^-0.718 = 0.512 >= 0.39.

Margin: P >= 0.39 still holds if q is 2^0.1 lower and p is 2^0.4 lower
simultaneously (sT = 2^-0.977 = 0.508, P = 0.398).

The cap K_max = 2^28.4 on Step-3 invocations does not matter: the number of
valid tuples in T trials is a sum of independent per-trial counts with mean at
most T * 2^-17.320 = 2^27.98 (variance inflation below 0.1%), and by the
Chernoff bound the probability of exceeding 2^28.4 = 1.338 * 2^27.98 is below
exp(-0.338^2 * 2^27.98 / 3), which is negligible.

## 9. Charged time (target-compression units, C = 2224)

Word-operation counts follow `collision-frontier-v5`: every load, store,
add/sub, logic op, shift, comparison and branch counts 1/2224; a 32-bit
rotation is charged 4 operations (two shifts, OR, mask); Sigma0, Sigma1,
sigma0, sigma1 are charged 14 operations each; additions modulo 2^32 are
charged 2 (add, mask). The compression C_32 itself is 1 unit (its 2224 already
include message expansion and feed-forward).

A. Main-loop trials, T = 2^45.3. Per trial: 1 unit for C_32 plus at most 160
   operations: random words and unpacking M0 into 16 words (34); bucket index
   (2), two offset loads (2), a linear scan of the bucket at 4 operations per
   record (expected N / 2^27 = 10.41 records, 41.6) and loop control (4), so
   lookup at most 50; Step 2 for the expected N / 2^32 = 0.3252 matching
   records at most 192 operations each in expectation. The 192 is: at most 160
   for decoding the tuple (16), E0, E1, E2 (3 * 25), W4 (28) and its sign test
   (3), paid by every match; 40 for the W19 test, paid by the 1/2 that pass (a);
   40 for W5 and its sign test, paid by the 1/16 that pass (b); 40 for W6 and
   its sign test, paid by the 1/128 that pass (c); and at most 1024 for
   everything else (W0..W3, the primed equations of steps 0..6, W21 and W20
   tests), paid by the 1/256 that pass (d). These fractions are exact
   consequences of Section 7.2 (uniform W4 and W5) and were also measured
   (0.5000, 0.1250, 0.1250, 0.5001). So 160 + 20 + 2.5 + 0.32 + 4 = 186.8
   <= 192, and 34 + 50 + 0.3252 * 192 = 146.4 <= 160.
   A <= 2^45.3 * (1 + 160/2224) = 2^45.400 units.
B. Step 3. At most K_max = 2^28.4 valid tuples, each with at most 300
   operations of setup (W0..W3, the W16 and W17 offsets, per-group sigma1
   values) and 196,608 candidates at at most 288 operations each in
   expectation. Stage 16 (E16 and E16' by one addition each from stored
   constants, A16 and A16' likewise, the two XOR tests, 5 loads, loop) costs at
   most 32; all remaining work of a candidate (steps 17..22 for both
   computations, W17..W31 for both computations, all tests) costs at most 2048
   and is paid only by the candidates that pass stage 16, a fraction measured
   as 1,528,108,551 / 12,224,888,832 = 0.125000 (Section 7.4). So 32 + 2048/8
   = 288. B <= 2^28.4 * (300 + 196,608 * 288) / 2224 = 2^43.036 units. Final
   verification: 6 compressions.
C. Precomputation P1-P4, from the iteration counts in Section 7.1, at 1024
   operations per iteration (each iteration evaluates at most six step or
   message equations, each at most 60 operations, plus at most 71 two-bit and
   mask tests at 4 operations each, about 650 in total): P2 2^32; E4 loop
   2^30.32; W7 loop twice (count pass and place pass) 2 * 2^36.24; L4 and L7
   enumeration 2^18 + 2^25; P4 393,472. Plus 8 operations per stored record
   and 4 per bucket for the prefix sum. Total 2^36.17 units; we charge
   2^36.5.
D. Starting solution T: S reports 2^34.3 for its SAT-based Step 1 without
   stating the unit. We charge 2^35 units, which leaves a factor of
   2^0.7 = 1.6 > 2476/2224 for the case that S counts 35-step compressions
   (2476 = 2224 + 3 * 84, the reference cost of three more expanded steps).
E. Search for the characteristic (S, Sect. 3 Model-1/2/3 and Sect. 4 Steps
   1-4): S reports no time. Heuristic H3 (Section 11) charges a budget of
   2,304 thread-hours, converted at 2^35 word operations per thread-second:
   E = 2,304 * 3,600 * 2^35 / 2224 = 2^(22.984 + 35 - 11.119) = 2^46.865
   units.

Total <= 2^45.400 + 2^43.036 + 6 + 2^36.5 + 2^35 + 2^46.865 = 2^47.385 units.
We claim time_log2 = 47.5, rounded up.
preprocessing_log2 = 46.9 bounds C + D + E (2^46.866). There are no restarts.
The attack phase alone (A + B) is 2^45.66.

Sensitivity to H3 (everything else fixed):

```
search budget                                  E (units)   total
2^44 units (about 320 thread-hours)            2^44.00     2^46.06
1,152 thread-hours (half)                      2^45.87     2^47.06
2,304 thread-hours (charged)                   2^46.87     2^47.38
4,608 thread-hours (or conversion at 2^36)     2^47.87     2^48.15
9,216 thread-hours                             2^48.87     2^49.01
```

Fallback regime for H1. If S's published rate 2^-20.92 were used in place of our
q (keeping p, T scaled to keep sT: T = 2^48.86), A would be 2^48.96 and the total
2^49.28. The scored claim uses our q (H1), not this fallback.

## 10. Memory

TAB2 records: N * 16 = 22,348,398,592 bytes (2^34.38). Bucket offsets:
(2^27 + 1) * 4 bytes (the same array holds the counts during pass 1). No
auxiliary sort buffer exists (Section 6, P3). Combination table (10,240 * 64
bytes), (combination, E4) table (155,008 * 64 bytes), L4 and L7 (2.5 MB), P4
list (196,608 * 28 bytes), code, constants and working state below 2^24 bytes.
Total 22,885,269,508 + 2^24 bytes = 2^34.415 bytes; we claim
memory_log2_bytes = 35. Nonuniform advice (characteristic, two-bit list,
T values, constants) is below 8 KB; nonuniform_advice_log2_bytes = 13.

## 11. Heuristics, evidence and limitations

H1 `q-32step-matching-rate` (score-critical). Claim: a uniformly random first
block yields at least 2^-17.36 expected valid tuples against our TAB2 with
C_32. Evidence: (i) analytic prediction 2^-17.3254 from an exact enumeration of
TAB2 and the structure of the Step-2 equations (Section 7.2), whose
per-test predictions match the measured stage fractions; (ii) four measurement
runs with 2^35.2 part-trials and 62,179 valid tuples in total, pooled 2^-17.3337,
99% lower bound 2^-17.3476 (Section 7.3). Assumptions: the first four words of
C_32(IV, M0) behave as uniform for these tests; the sign pattern of the W21
test is treated as independent of the W6/E2 conditioning. Limitations: the
measurements and the enumeration are our own code (Appendix A), not organizer
executions. Fallback: S's published 35-step rate 2^-20.92 (total 2^49.28,
Section 9).

H2 `step3-46-conditions` (score-critical). Claim: for a valid tuple, each P4
candidate passes Step 3 with probability at least 2^-46, and Step 3 succeeds with
probability r >= 2^-28.415 * (1 - 2^-20). Evidence: S's count of 45 printed
conditions, reproduced (Section 2), plus one necessary unprinted condition at
step 19 derived in Section 7.4; the measured rates through steps 16-21 over
2^33.5 candidates agree with the stage-by-stage mapping (Section 7.4); a Monte
Carlo of the post-step-21 W conditions gives about 2^-11 for the pair's tuple
against the 2^-13 charged. Scope: candidates of one tuple share W14 in groups
of 2^14, and the 12 W20 conditions are common to a group; this is charged in
the second-moment bound of Section 8. Extrapolation: the 13 conditions after
step 21 are not observed jointly (no full conformance at our sample size).
Limitations: independence among conditions and among candidates beyond the W14
grouping is not proved; the Monte Carlo used one tuple's (W6, W7, W8)
differences.

H3 `trail-search-budget` (score-critical). Claim: the SAT/SMT searches that
produced S's characteristic cost at most 2,304 thread-hours, i.e. at most
2^57.98 word operations = 2^46.865 units. Itemisation: S describes 8
minimisation tasks (S, Sect. 3: Model-1, Model-2 in two phases, Model-3;
S, Sect. 4: Steps 1, 2, 3 and 4; Model-3 and Step 1 have the same objective but
are charged twice). Each task is a sequence of solver calls with a tightening
threshold that ends with a call returning no solution. We charge each task 288
thread-hours, i.e. four solver calls at a 72-hour cap each on one thread. The
72-hour figure is the example per-call limit stated by the same first three
authors (Li, Liu, Wang) for the same tool family (ePrint 2024/349, Sect. 4.3, Step 2: a call
that returns no solution within a reasonable time such as 72 hours is
abandoned and the threshold relaxed). Conversion: S's server has two AMD EPYC
9354 CPUs (64 cores, 128 hardware threads, at most 3.8 GHz). A Zen 4 core
dispatches at most 6 macro-operations per cycle; even counting fused
compare-and-branch pairs as two instructions, it executes at most 8 instructions
per cycle, i.e. at most 3.8e9 * 8 = 2^34.82 instructions per second, and a
hardware thread no more. We convert at 2^35 operations per thread-second. This
is above that hardware peak; SAT solvers are memory-bound and run far below
peak, which leaves room for instructions (such as multiplications) that cost
more than one word-RAM primitive. Converting at 2^36 instead is the 4,608-hour
row of the sensitivity table. Evidence: the
published procedure and its per-call limit; no published total time.
Limitations: the number of calls per task (four at the cap) is our assumption,
not derived from a publication; S's descent of t_r ends at the published final
A-difference weight 21 but its starting threshold is unknown; a parallel solver
using several threads per call would count each thread. If the true search
cost was larger, the score increases (sensitivity table in Section 9).

H4 `starting-solution-cost` (supporting). S's reported 2^34.3 for Step 1
covers producing T; we charge 2^35. T is the single solution S used (quoted in
Section 3), not selected among several.

Not claimed: any figure from S as a 32-step result; the 35-step pair or its
second block as a 32-step collision; rigorous qualification.

## Appendix A. Exact predicates as inert source text (ours)

The following C fragments are the predicates used in the measurements (inert
text for audit; nothing here is executed by the organizer). Arrays are indexed
by step + 4. FL_X[i+4] is FL of row X_i; FM_X and FV_X are the mask and values
of the printed single-bit conditions of row X_i, including n/u positions (n -> 0,
u -> 1); T2/T2R is the list of 71 two-bit conditions read as in Section 2.
AX(s,i), EX(s,i), s->w[i] are the unprimed values; AP, EP, WP the values xor FL.

```c
/* XOR-conformance of the primed computation at step i */
aeqP(s,i): AP(s,i) == EP(s,i) - AP(s,i-4) + S0(AP(s,i-1)) + MAJ(AP(s,i-1),AP(s,i-2),AP(s,i-3))
eeqP(s,i): EP(s,i) == AP(s,i-4) + EP(s,i-4) + S1(EP(s,i-1)) + IF(EP(s,i-1),EP(s,i-2),EP(s,i-3)) + K[i] + WP(s,i)
fixX(s,i): (X_i & FM_X[i+4]) == FV_X[i+4]          two_ok(s,lo,hi): all T2 conditions among steps lo..hi hold

/* P2: combination (E5,E6,E7) */
A3 = E7-A7+S0(A6)+MAJ(A6,A5,A4); A2 = E6-A6+S0(A5)+MAJ(A5,A4,A3); A1 = E5-A5+S0(A4)+MAJ(A4,A3,A2);
W[i] = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1},E_{i-2},E_{i-3}) - K[i]   (i = 9,10,11)
keep iff fixE(5..7) && fixA(1..3) && fixW(9..11) && aeqP(5..13) && eeqP(9..13) && two_ok(1,13)

/* P3 inner loops */
E4 loop: A0 = E4-A4+S0(A3)+MAJ(A3,A2,A1); W8 = E8-A4-E4-S1(E7)-IF(E7,E6,E5)-K[8];
         keep iff fixW(8) && fixA(0) && aeqP(4) && eeqP(8) && two_ok(0,13)
W7 loop: c7 = E7-A3-S1(E6)-IF(E6,E5,E4)-K[7]; E3 = c7-W7; require fixE(3);
         A_{-1} = E3-A3+S0(A2)+MAJ(A2,A1,A0); require fixA(-1) && aeqP(3) && eeqP(7);
         require s0(W8^FL_W8)-s0(W8) + (W7^FL_W7)-W7 == 0;  require two_ok(-1,13)

/* Step 2 for CV1 = (a,b,c,d,e,f,g,h) and a matched tuple */
A_{-1..-4} = a,b,c,d; E_{-1..-4} = e,f,g,h;
E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1},A_{i-2},A_{i-3})          (i = 0,1,2)
W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) - IF(E_{i-1},E_{i-2},E_{i-3}) - K[i]   (i = 0..6)
(a) (W4 & FL_W4) == (FV_W4 & FL_W4)          (b) s0(WP4) + WP12 == s0(W4) + W12
(c) (W5 & FL_W5) == (FV_W5 & FL_W5)          (d) (W6 & FL_W6) == (FV_W6 & FL_W6)
(e) eeqP(0..6) && aeqP(0..2)                 (f) s0(WP6) + WP5 == s0(W6) + W5
(g) (WP13-W13) + (s0(WP5)-s0(W5)) + (WP4-W4) == D(W20)

/* Step 3 for one (W14,W15) candidate; both computations are evaluated independently */
for i in 16..31:
  W[i]  = s1(W[i-2])  + W[i-7]  + s0(W[i-15])  + W[i-16];   Wp[i] likewise from Wp
  require (W[i]^Wp[i]) == FL_W[i+4];  if FL_W[i+4] != 0: require (W[i] & FL_W[i+4]) == (FV_W[i+4] & FL_W[i+4])
  if i <= 22: compute (A[i],E[i]) and (Ap[i],Ep[i]) by the step equations;
              require (A[i]^Ap[i]) == FL_A[i+4] && (E[i]^Ep[i]) == FL_E[i+4]
then recompute both complete padded 32-step digests and compare

/* Table statistic of Section 7.2, per tuple (E3,E4,E5,E6,A2 from the tuple) */
ok6 = (E6 + (S1(E5^FL_E5)-S1(E5)) + (IF(E5^FL_E5,E4^FL_E4,E3)-IF(E5,E4,E3)) + D(W6)) == (E6^FL_E6)
for e in {0,1}: E2 = e<<29;
   ok5[e] = (E5 + (S1(E4^FL_E4)-S1(E4)) + (IF(E4^FL_E4,E3,E2)-IF(E4,E3,E2)) + D(W5)) == (E5^FL_E5)
e* = the e with ok5[e] (exactly one in every tuple);  Y = E6 - A2 - S1(E5) - IF(E5,E4,E3) - K[6];
y = Y mod 2^30; end = (y - e* * 2^29) mod 2^30; st = (end - 2^29 + 1) mod 2^30;
P_t = |st - 2^29| / 2^30        /* = Pr over uniform E2 of E2[29] = e* and (Y - E2)[29] = 0 */
accumulate ok6 * P_t
```

Generator and seeds. Pseudo-random words come from xoshiro256** seeded by
splitmix64; thread k (k = 0..11) of a run with seed S and step count R uses
seed S * 1000 + 7919 k + 104729 R. Each part run uses 12 threads x 357,913,941
trials (run 3: 12 x 89,478,485). A trial draws M0 as 8 64-bit outputs split
into 16 words, computes CV1 = C_32(IV, M0) and looks up its first word.

## 12. Grouped First-Block Partial Evaluation (`time_log2 = 47.25`), Verified 32-Step Collision Certificate, and Organizer Experiments

### 12.1 Verified 32-Step Ordinary Collision Certificate (`certificates/message-a.bin`, `certificates/message-b.bin`) and `fixed-witness-derivation`

An executed search of this exact 32-step truncation of the Li-Liu-Wang-Shi (CRYPTO 2026, ePrint 2026/1080) characteristic (from `sha256-r32` campaign chunk 34, seed `202610040034`, counter `2149248237`, local tuple index `15529`, tail index `131794`) produced an explicit, organizer-verified 128-byte colliding pair for `sha256-r32-prefix-v1`, included in `certificates/manifest.json` (`id: sha256-r32-record-witness`) and reconstructed deterministically in `experiments/replay.py` (`fixed-witness-derivation`):
- `certificates/message-a.bin` (128 bytes, SHA-256 `92e9ab74fd94956893727406209e64ed6645d3af8748c56a8bc45096b7f33a84`):
  - `M0`: `04a9b33e 6ea679aa 89f6fb3b f530dfa8 c5828a5e 385388a4 0dbcd14f 77252e33 4fef2ad0 809de1a4 a3b955b6 3a95b0cc 5cadb080 01a17ef2 00000000 801aeced`
  - `M1`: `e37cab30 5f4048fd 95caa0fc 87591d98 fb8464a3 399cc8f3 6c91c8c4 7d608f34 4ee37252 58e49d82 10746273 a96ce154 45f2222c 4d12f88a d2701ece 17d9748f`
- `certificates/message-b.bin` (128 bytes, SHA-256 `0a3f5c00ffacbceda4fa2dd7092b59b01a34ca865ca589c30c9d8b3858c80da8`):
  - `M0`: identical 64-byte first block (`CV1 = C_32(IV, M0) = e890c4ba 6bce94e6 47a0b812 c5ef36b2 ec7b7814 91cf09df a9717904 494bc86f`)
  - `M1'`: `e37cab30 5f4048fd 95caa0fc 87591d98 db8464a3 3ddcc0f3 4c91c8c4 7c619fbe 4eeb7e52 58e49d82 10746273 a96ce154 41b22a2c 6d12f88a d2701ece 17d9748f`
- Both messages collide after the second block (`states[1] = 79389eeb 882fc938 62f355f8 3ebb8d51 4d0b99ce a01e12ed 7058785b dae69307`) and have the identical complete 3-block 32-step SHA-256 digest:
  `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77`.

In addition to `fixed-witness-derivation`, `experiments/manifest.json` declares `r32-prob-Verify`, `r32-w20-s0w5-carry`, `r32-w22-s1w20-s0w7-cancel`, and `r32-w23-s0w8-cancel` (`addition-xor-sampled-v1`) to verify the Lipmaa-Moriai modular-addition carry probabilities in the Step-2 algebraic pre-filter and Step-3 message expansion, while `experiments/replay.py` also verifies on all 256 organizer seeds that the grouped first-block incremental schedule below matches full `C_32(IV, M0)` bit-for-bit.

### 12.2 Tightened Cost Bound via Grouped First-Block Evaluation (`time_log2 = 47.25`, and `47.39` Ungrouped)

1. **Ungrouped bound (`2^47.385 < 2^47.39`)**: Even with every trial computing a full 32-step compression from scratch (`1 + 160/2224` units/trial, Section 9), the total charged time is `2^45.400 + 2^43.036 + 6 + 2^36.5 + 2^35 + 2^46.865 = 2^47.385` units (`< 2^47.39`).
2. **Grouped first-block evaluation (`L = 2^16` trials per group sharing `W0..W14`, `W15 = r15 + j mod 2^32`)**:
   - By the exact same marginal-uniformity bijection used in `sha256-r31` (for fixed `j`, `(W0..W14, r15 + j mod 2^32)` is a uniform 512-bit block), generating `T = 2^45.3` first blocks in `G = 2^29.3` independent groups of `L = 2^16` trials allows steps `0..14`, `W16, W18, W20`, the step-15 base constants, and the group-invariant schedule partial sums `c17, c19, c21..c29` to be computed **once per group** (`<= 2048` ops/group, adding `< 2^29.3` units total).
   - Each trial then computes only `W15 = r15 + j` (`2` ops), the 13 dependent schedule words `W17, W19, W21..W31` (`172 + 28 = 200` ops), steps `15..31` (`802 + 54 = 856` ops), `A[-1] = IV[0] + A31` (`2` ops, with the other 7 feed-forward words computed only for the `0.3252` matched records per trial: `0.3252 * 14 = 4.6` ops), plus a `155`-op reload allowance = `1220` operations for `C_32(IV, M0)` (`1220 + 160 = 1380` ops/trial = `1380 / 2224 = 0.6205` units/trial instead of `1.0719` units/trial).
   - This reduces the main-loop cost `A` from `2^45.400` to **`2^44.611` units**, and the total charged time to:
     `Total <= 2^44.611 + 2^43.036 + 6 + 2^36.5 + 2^35 + 2^46.865 = 2^47.198 < 2^47.25` units!

We therefore claim **`time_log2 = 47.25`** (which holds with `0.052` bits of margin under grouped first-block evaluation, while even the ungrouped full-compression evaluation is `2^47.385 < 2^47.40`).

