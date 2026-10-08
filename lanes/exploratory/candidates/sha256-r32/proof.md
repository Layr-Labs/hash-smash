# SHA-256 reduced to 32 steps: two-block collision from the CRYPTO 2026 35-step characteristic, run under a hard work counter

## 0. Claim

Track `sha256-r32-exploratory`, target profile `sha256-r32-prefix-v1`, attack class `ordinary-collision`, cost model
`collision-frontier-v5`: one 32-step SHA-256 compression is 1 unit and every other primitive 256-bit word-RAM
operation is 1/C unit with C = 2224.

The algorithm of Sections 4-5 outputs two distinct 128-byte messages whose complete hashes under the target are equal
(standard IV, FIPS 180-4 padding, steps 0..31 on all three padded blocks, feed-forward, all 256 output bits). Bounds:

| Field | Claimed | Computed (Sections 9-11) |
|---|---|---|
| time_log2 | 46.41 | total <= 93,122,144,021,630 units = 2^46.40419 |
| preprocessing_log2 | 45.71 | C + D + E = 57,354,824,376,751 units = 2^45.70498 |
| success_probability | 0.39 | >= 0.390108 |
| memory_log2_bytes | 35 | 28,661,817,348 bytes = 2^34.739 |
| nonuniform_advice_log2_bytes | 13 | < 8,192 bytes |

No certificate is attached; the claim is the cost of the stated algorithm, not a found pair.

The time bound holds on every coin sequence. The run has a fixed number T of trials and a hard counter on all
data-dependent work (Section 5.4). Heuristics enter only the success probability, through measured rates
(Section 12), and the prices of the one-time characteristic search and starting solution (Sections 7-8).

### 0.1 Sources and credit

- **S** - Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2",
  CRYPTO 2026, IACR ePrint 2026/1080. The characteristic (S Fig. 6), the colliding 35-step pair (S Table 3), the
  three-phase attack (S Sect. 4) and the four-step characteristic search all come from S.
- **Tool** - Y. Li, F. Liu, G. Wang, EUROCRYPT 2024, ePrint 2024/349, github.com/Peace9911/sha_2_attack. The
  characteristic search that we charge used this SAT/SMT model with STP and CryptoMiniSat.
- **hash-smash #26/#33 (winglock)** - the 32-step truncation, the concrete table (P1-P4) and Step-2/3 test
  specification that Sections 4-5 restate, the analytic matching-rate prediction, and the unprinted condition
  E16[29] = E17[29].
- **hash-smash #296 and #396 (mitchuski)** - the re-implementation and measurements of that specification: the table
  counts, the matching rate q, the Step-2 and Step-3 stage pass rates, the table multiplicity sums, the starting-solution
  runs and the callgrind calibration of the CPU-second price. #396 also completed the characteristic search until it
  printed Fig. 6 and gave the 59-call ledger that Section 7 charges, together with its blind-rediscovery factor.
- **hash-smash #227 (yudduy)** - a public 32-step pair of exactly this form. We use it only as corroboration (Section 3).
- **hash-smash #134 (jagnani73)** - the precedent of pricing a measured solver run in CPU-seconds.
- **hash-smash ddd666d3 (GordoAR)** - the counter cap W_cap = 254 T of Section 5.1.

Every measured quantity used here is a participant measurement from the public records above. They are named and
bounded in Section 6, and each enters through a declared heuristic. We did not re-run the 22 GB table or the charged
solver calls. The exception is the evidence for the CPU-second price in Section 15, which is our own.

### 0.2 What this package adds

1. A self-contained statement of the attack in one place: characteristic, conditions, all four precomputed sets, both
   online steps, and the exact tests, so that the algorithm can be rebuilt from this file alone.
2. Our own participant checks (Section 14). They recompute S's published pair, the characteristic rows, the 71
   conditions under the stated readings, the advice words, the Step-2 equations and tests, the Step-3 stages and the
   32-step truncation from our own code, cross-checked with the organizer's `verifier/hash_functions.py:digest`.
3. A fixed-work schedule whose counter charges are staged per test and per Step-3 stage (Section 5.4). The
   Step-2/3 work therefore costs about 239 counted operations per trial instead of about 461 under a flat per-candidate
   charge. With T = 2^44.8309 trials and a counter cap of 254 T operations (the cap of GordoAR's ddd666d3), the online
   phase is 2^45.0237 units.
4. An exact integer ledger (Section 10) and a sensitivity table (Section 13).
5. Our own evidence for the price of the characteristic search (Section 15). A callgrind profile of the charged
   workload type (Section 15.6): STP 2.3.4 with CryptoMiniSat 5.11.21, called as
   `stp model.cvc --cryptominisat --threads N` on the authors' model re-parametrised as in #396, one call per search
   step with its whole front end plus one call run to its answer, every executed instruction priced by its form.
   **New in this package:** every multiply, divide and floating-point form is priced by an exact counted emulation
   with the v5 primitives (Section 15.7), and the search is charged as an absolute operation count,
   59 X_once m_once + I_max m_search (Section 7), instead of through a share of one-off work.
6. The changes after the reviews of 21b81d2d, 4e4e600f and d3cd2213 are listed in Sections 16 and 17.

## 1. Target, notation, success event

Words are 32-bit and `+`/`-` are mod 2^32. Sigma0, Sigma1, sigma0, sigma1, IF (choose) and MAJ are as in FIPS 180-4.
The schedule is W[i] = M[i] for i < 16 and W[i] = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16] for i >= 16.

For a chaining value CV = (a, b, c, d, e, f, g, h) set A[-1], A[-2], A[-3], A[-4] = a, b, c, d and E[-1], E[-2],
E[-3], E[-4] = e, f, g, h. Step i (0 <= i < R) computes

```
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])
```

and C_R(CV, M) = CV + (A[R-1], A[R-2], A[R-3], A[R-4], E[R-1], E[R-2], E[R-3], E[R-4]) word-wise. This is the
standard step function written with one new A and one new E per step. The target hashes a 128-byte message
M0 || M1 as C_32(C_32(C_32(IV, M0), M1), P), with P = (80000000, 0, ..., 0, 00000400) the common padding block.

Rearranging the two equations gives the backward forms used below:

```
A[i-4] = E[i] - A[i] + Sigma0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])
W[i]   = E[i] - A[i-4] - E[i-4] - Sigma1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K[i]
E[i]   = A[i] + A[i-4] - Sigma0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])
```

**Signed rows.** A row is a 32-character string; character k describes bit 31-k. For the unprimed value x and the
primed value x': `=` means x = x'; `0`/`1` means x = x' with that bit value; `n` means x = 0, x' = 1; `u` means x = 1,
x' = 0. FL(X) is the mask of `n`/`u` positions and D(X) = sum over `n` of 2^j minus sum over `u` of 2^j (mod 2^32),
which is X' - X. fixX(i) means that the unprimed X[i] has the value demanded by every `0`, `1`, `n` (0) and `u` (1)
symbol of its row. sign(X, i) is the same test restricted to the `n`/`u` symbols.

**Conformance.** Given primed inputs equal to unprimed inputs XOR their FL masks, step i is XOR-conformant for E
(resp. A) if the primed step equation returns E'[i] = E[i] XOR FL(E[i]) (resp. A'[i] = A[i] XOR FL(A[i])). This is an
exact 32-bit equality.

**Success event.** The run outputs (M0 || M1, M0 || M1') with M1 != M1' and equal complete target hashes. Every output
is recomputed with the full three-block 32-step hash before it is returned (Section 5.3), so an output is always
correct. The probability space is the run's fresh uniform coins for a fixed target.

## 2. Characteristic and conditions (S, Fig. 6)

The unprimed message is S's M'_1 and the primed one is S's M_1. Rows -4..-1 and 0..2 are all `=`, and so are rows
23..34. Row 3 of W and rows 9..11, 14..19 and 21 of W are all `=`.

```
 i   nabla A[i]                        nabla E[i]                        nabla W[i]
 3   ================================  =====1=====011======0======0====  ================================
 4   ==n=============================  ==n0=0=1===100=0==0=1===0==1=0=1  ==n=============================
 5   =====n===n===n=u====n===u==u====  01011u001n=nuu=11000n=1=101u=100  =====u===u==========n===========
 6   ================================  101n=0=1=1=n1111==n0u===n=0n=n=u  ==n=============================
 7   ================================  10u0=1=101==00=n==0=0===0==0=0=0  =======n=======u===u====u=1=u=u=
 8   ================================  uuu1=0=111=0=0=01=1=01==1==1=1=0  ============u=======uu==========
 9   ==========u====================u  11=10n0nuuu00n0u101=n11=u01u=unn  ================================
10   ================================  un111111001001111=010u=u0=001100  ================================
11   ====n=========u=u=======u==n====  1011n111100010u1u0111111u=nu1001  ================================
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
```

S prints `+` at one position of E10 and one of E11. We write `=` there; both published messages agree on those bits.
The rows carry 119 `n`/`u` symbols and 360 symbols that fix a bit value (`0`, `1`, `n`, `u`). Their weights are
tw = 22, tE = 6, tA = 21 and tE4 = 76, as in S. We use the machine-readable transcription of #26/#296, compared
symbol by symbol against the published pair (Section 14).

**Two-bit conditions.** S prints the following relations. X[a,b] = Y[c,d] means X[a] = Y[c] and X[b] = Y[d], and bit j
is the bit of weight 2^j.

```
W4[1,8]!=W4[12,25]  W4[18]=W4[14]  W5[0,1,30]=W5[28,18,9]  W6[1,8]=W6[12,25]  W6[18]!=W6[14]
W7[22,13,23]!=W7[18,9,8]  W7[11,14,20]=W7[22,31,31]  W8[0,14,21]=W8[28,25,6]
W8[31,23,30,15,22,8]!=W8[27,2,15,26,7,4]  W20[4,31]=W20[6,22]  W20[31,30,25,21]!=W20[1,0,16,14]
W22[4,31]=W22[6,22]  W22[27]!=W22[20]
E4[10]!=E4[15]  E5[3,21]=E5[8,8]  E6[9,27,9,8]!=E6[23,14,14,27]  E6[1,1,23,6]=E6[6,15,10,25]
E7[21,10]!=E7[3,15]  E16[28,20,20,6]=E16[1,7,2,11]  E16[30,28,10]!=E16[12,10,29]  E18[24]!=E18[11]  E18[2]=E18[16]
A3[29]=A2[29]  A3[29]!=A5[29]  A3[26,4]=A4[26,4]  A3[22,18,16,11,7]!=A4[22,18,16,11,7]  A14[9]=A14[20]
A14[18,8]=A14[6,17]  A13[30,25,23]=A14[30,25,23]  A13[15]!=A14[15]  A13[29]!=A15[29]  A15[29]=A6[29]
```

That is 73 bit relations. On the published pair, 66 hold as printed and 7 do not. We use the reading that matches the
pair, as #26 did:
- E7[21,10] = E7[3,15];
- A14[18,8] != A14[6,17];
- A15[29] = A16[29], reading "A6" as a misprint;
- the two equalities W20[4,31] = W20[6,22] are dropped.

This leaves **71 two-bit conditions**, and all of them hold on the pair. They are used only to shape the precomputed
sets P1-P4: those on E4, W7 (P1), E5..E7, A1..A13 (P2), W8 (P3) and A13..A15 (P4). The conditions on W4..W6, W20,
W22, E16, E18 and A16 are not tested separately online. The exact equality tests of Section 5 take their place, and
every measured rate of Section 6 was measured with exactly those tests.

## 3. Truncation to 32 steps

**Lemma 1.** Let CV be any chaining value and let M, M' be second blocks with A[j] = A'[j] and E[j] = E'[j] for
j = 19, 20, 21, 22 and W[j] = W'[j] for j = 23..31. Then C_32(CV, M) = C_32(CV, M').

*Proof.* Step j reads A[j-4..j-1], E[j-4..j-1] and W[j]. For j = 23 all of these are equal by hypothesis, so
A[23] = A'[23] and E[23] = E'[23]. Induction gives equality through step 31. The outputs A[28..31] and E[28..31] are
equal, and the feed-forward adds the common CV.

**Lemma 2.** If M0 is common, M1 != M1' and C_32(C_32(IV, M0), M1) = C_32(C_32(IV, M0), M1'), then M0 || M1 and
M0 || M1' are distinct 128-byte messages with equal target hashes.

*Proof.* Both have the same length, hence the same padding block P, and P is compressed from the same chaining value.

Rows 19..22 of A and E and rows 23..31 of W are `=` in Fig. 6. A second block that conforms to Fig. 6 through step
22, and whose schedule conforms in W16..W31, therefore collides after 32 steps. Rows W32..W34 and steps 23..34, which
the 35-step attack also needs, are not used. The truncation adds no condition. Its only change is that the first block
is compressed with C_32, so the chaining value CV1 = C_32(IV, M0) is what Step 2 must match. Every matching rate in
Section 6 was measured with C_32 first blocks.

**Checks (ours, Section 14).**
- S's Table 3 pair collides under the 35-step hash. Its full 32-step hashes differ, so the pair itself is not a
  32-step collision.
- From S's 35-step CV1, the second blocks of that pair give C_32(CV1, M1) = C_32(CV1, M1'). This is Lemma 1 on
  published data.
- The public 32-step pair of #227 has equal 32-step hashes (f8a3db11...4e77) and unequal 31-, 35- and 64-step hashes.
  From CV1 = C_32(IV, M0) its second blocks match every symbol of rows -4..22 above with 0 mismatches, and they have
  no difference in W23..W31. This instance corroborates the truncation and is not used as our certificate.

## 4. Precomputation

**Advice.** These are the unprimed values of S's pair, computed from its 35-step CV1:

```
A4..A13 = 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E8..E13 = f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4
W12, W13 = 41b22a2c 6d12f88a
```

The primed advice words are X XOR FL(X). The advice is the starting solution of S's attack Step 1. Its cost is charged
in Section 8.

**P1 (single-word lists).**
- L4 is the set of E4 values with fixE(4) and E4[10] != E4[15]. Row E4 has 18 free bits, so |L4| = 2^17 = 131,072.
- L7 is the set of W7 values with fixW(7) and its six two-bit conditions. Row W7 has 25 free bits, so
  |L7| = 2^19 = 524,288.

**P2 (middle combinations).** Enumerate every (E5, E6, E7) with fixE(5), fixE(6), fixE(7). The rows have 5 + 12 + 15
free bits, so there are 2^32 triples. For each triple:
- compute A3, A2, A1 from the backward A form at steps 7, 6, 5;
- compute W9, W10, W11 from the W form at steps 9, 10, 11.

Keep the triple iff all of these hold:
- fixA(1), fixA(2), fixA(3);
- A is XOR-conformant at steps 5..13 and E at steps 9..13, using the primed advice and the primed triple;
- every two-bit condition among A1..A13, E5..E13 and W9..W13 holds.

The kept set has 10,240 combinations. Each one stores (E5, E6, E7, A1, A2, A3, W9, W10, W11).

**P3 (table TAB2).**
- *E4 loop.* For each combination and each E4 in L4:
  - A0 = E4 - A4 + Sigma0(A3) + MAJ(A3, A2, A1);
  - W8 = E8 - A4 - E4 - Sigma1(E7) - IF(E7, E6, E5) - K[8].

  Keep the pair iff fixA(0) and fixW(8) hold, A is XOR-conformant at step 4 and E at step 8, and the nine two-bit
  conditions on W8 hold. The A2..A5 relations were already enforced in P2. There are 155,008 kept pairs.
- *W7 loop.* For each kept pair and each W7 in L7:
  - E3 = E7 - A3 - W7 - Sigma1(E6) - IF(E6, E5, E4) - K[7];
  - A[-1] = E3 - A3 + Sigma0(A2) + MAJ(A2, A1, A0).

  Keep the record iff fixE(3) holds, A is XOR-conformant at step 3 and E at step 7, and
  sigma0(W8') + W7' = sigma0(W8) + W7. That last equality is what makes W23 difference-free.
- *Storage.* A record is 16 bytes: the key A[-1] and the three indices (combination, pair, W7). Records are bucketed by
  the top 27 bits of the key. A counting pass fills 2^27 + 1 offsets of 4 bytes, and a second pass places the records.
  No sorting is needed. N = |TAB2| = 1,396,774,912 = 2^30.3795.

**P4 (second-block tail list).**
- Enumerate E14 with fixE(14) (8 free bits) and set A14 = E14 - A10 + Sigma0(A13) + MAJ(A13, A12, A11). Keep it iff
  fixA(14) holds and the two-bit conditions involving A14 hold (A14 with itself, and A13 with A14).
- For each kept E14, enumerate E15 with fixE(15) (15 free bits) and set A15 = E15 - A11 + Sigma0(A14) +
  MAJ(A14, A13, A12). Keep it iff fixA(15) holds, A13[29] != A15[29], and both A and E are XOR-conformant at
  steps 14 and 15.
- W14 and W15 then follow from the W form. Each entry stores W14, W15, sigma1(W14), sigma1(W15) and the step-16
  constants of both sides, which depend only on the advice and the entry.
- |P4| = 196,608 = 12 * 2^14 = 2^17.585.

Steps 14-15 involve only advice words and the P4 entry, which is why P4 is shared by all tuples.

## 5. Online phase

### 5.1 Parameters

T = ceil(2^44.8309) = 31,292,887,053,577 trials, and a counter cap W_cap = 254 T counted operations. Nothing is
restarted. The cap 254 T follows hash-smash ddd666d3 (GordoAR); T is the smallest exponent at four decimals that keeps
the success bound of Section 9 at or above 0.3901 under that cap.

### 5.2 One trial

1. **Fresh first block.** Draw two fresh uniform 256-bit words and cut them into 16 message words. That gives M0, and
   CV1 = C_32(IV, M0).
2. **Step 2 (match).** Let b be the top 27 bits of CV1[0], with A[-1..-4] = CV1[0..3] and E[-1..-4] = CV1[4..7].
   Scan bucket b. For each record whose key equals CV1[0]:
   - decode the combination, the pair and W7, and recompute E3;
   - compute E0, E1, E2 from the forward E form at i = 0, 1, 2;
   - compute W0..W6 from the W form at steps 0..6. All inputs are now known: E3 and E4 come from the record. The
     words are computed lazily, in the order the tests need them: W4, then W5, then W6, then W0..W3. Section 5.4
     charges them in that order.

   Accept the record iff the following tests pass, aborting at the first failure in this order:
   - (a) sign(W, 4) holds;
   - (b) sigma0(W4') + W12' = sigma0(W4) + W12, so that W19 has no difference;
   - (c) sign(W, 5) holds;
   - (d) sign(W, 6) holds;
   - (e) E is XOR-conformant at steps 0..6 and A at steps 0..2, from the common CV1 with primed W0..W6;
   - (f) sigma0(W6') + W5' = sigma0(W6) + W5, so that W21 has no difference;
   - (g) (W13' - W13) + (sigma0(W5') - sigma0(W5)) + (W4' - W4) = D(W20), so that W20 receives its signed difference.

   An accepted record is a valid tuple. It fixes W0..W13 and the state through step 13 on both sides.
3. **Step 3 (tail).** For each valid tuple and each P4 entry, set M1 = (W0, ..., W15) and M1' = M1 XOR FL(W). Then
   for i = 16, ..., 31, aborting early:
   - require W'[i] = W[i] XOR FL(W[i]), and sign(W, i) for i = 20 and 22;
   - for i <= 22, also require XOR-conformance of A and E at step i.

   Stage 16 needs only one schedule addition and one E step per side, using the stored per-entry constants.

### 5.3 Output and stopping

If a candidate passes stage 31, the algorithm computes both complete three-block 32-step hashes: 6 compressions and
an 8-word comparison. If they are equal, it returns the pair and halts. If they are not equal, it halts with failure;
Lemmas 1-2 rule this out, so the rule costs no probability and bounds the verification work. The run also halts with
failure after T trials, or as soon as the counter would exceed W_cap.

### 5.4 Counter charges

Before each data-dependent action, the counter is increased by an upper bound on that action's primitive operations.
If the new value would exceed W_cap, the run halts before acting. Counted work is therefore at most W_cap on every
coin sequence. The counter's own add, compare and branch are included in each charge.

Operation prices used for the charges: a load, store, add, logic operation, shift, compare or branch is 1 operation. A
32-bit rotation inside a 256-bit word is 4 (two shifts, an OR, a mask). Sigma0 and Sigma1 are 14, sigma0 and sigma1
are 11, IF is 4 and MAJ is 5. A mod-2^32 sum of several terms is one add per term plus one mask.

| Action | Charge (ops) | Content, with an upper count |
|---|---|---|
| bucket of n records | 8 n | TAB2 records sit two per 256-bit word: per word one load, two key extractions (3), two compares and branches (4), pointer increment and loop test (3) = 11, i.e. 5.5 per record; a bucket edge costs at most one extra load, counted in the fixed per-trial work |
| record with key match | 200 | 1 record load and 3 field extracts; side-table loads for the combination (9), the pair (3) and W7 (1); E3 (<= 26); E0..E2 (3 * 25); W4 (<= 28); test (a) (3); counter (3) = 152 |
| (a) passed | +48 | W4', both sigma0 (22), W12, W12' sums (4), compare (2), counter (3) = 32 |
| (a,b) passed | +48 | W5 (<= 28), test (3), counter (3) = 34 |
| (a..c) passed | +48 | W6 (<= 28), test (3), counter (3) = 34 |
| (a..d) passed | +1256 | (e): primed E steps 0..6 (7 * 30) and A steps 0..2 (3 * 30) with compares (20); (f) (30); (g) (40); W0..W3 (4 * 28); tuple constants for Step 3 (<= 100); counter (3) = 605 |
| Step 3 per valid tuple | 400 + 40 * 196,608 | tuple setup for both sides (<= 400); stage 16 per entry: 4 loads, schedule add and mask (2), one E step per side from constants (2 * 12), conformance compare (4), branch (1) = 35 |
| each later stage, after the previous stage passed | 192 | two schedule words (2 * 28), two E steps (2 * 26), two A steps (2 * 25), compares and sign tests (13), counter (3) = 174 |

Fixed per-trial work outside the counter is charged 64 operations: 2 random words and 32 shift/mask extractions for
M0; the bucket index (1), two offset loads with shift-and-mask extraction from packed 4-byte offsets (6) and a
subtraction (1); the bucket charge update (4); a bucket-edge load (1); and trial-loop control (3). That totals 50. C_32(IV, M0) is 1 unit.

## 6. Measured inputs (credited) and their use

| Quantity | Value used | Source and status |
|---|---|---|
| table and list sizes | L4 = 131,072; L7 = 524,288; 10,240 combinations; 155,008 pairs; N = 1,396,774,912; P4 = 196,608 | exact counts of the Section 4 predicates, by #26 and #296 (identical). Our free-bit counts reproduce L4 and L7 and the 2^32 P2 domain |
| bucket occupancy | mean N / 2^27 = 10.4068; maximum 936 | maximum measured on the built table (#296) |
| key multiplicity | sum over the 4 index-parts of sum_v c_v^2 = 5.758e9 | #296; used only in the second moment |
| matching rate q | expected valid tuples per C_32 trial: 99% interval [2^-17.3583, 2^-17.3166] | #296: 2^34 part-trials, 25,936 valid tuples, pooled 2^-17.3373. Corroborated by #26 (2^-17.3337), #227's campaign (14,643,237 tuples over 2.405e12 first blocks = 2^-17.326) and #26's analytic prediction 2^-17.3254 |
| Step-2 cumulative pass fractions after (a), (a,b), (a..c), (a..d) | bounded by 0.51, 1/15, 1/120, 1/240 | #296 measured 0.5000, 0.0625, 0.0078, 0.0039 over about 5.6e9 matches (predicted 1/2, 1/16, 1/128, 1/256) |
| Step-3 cumulative stage pass | stage 16 <= 2^-2.99; stage 17 <= 2^-14.9 | #296: 2^32.248 candidates; 2^-3.000 and 2^-15.000 (155,619 passes) |
| Step-3 per-candidate success p | 2^-46 | the count of conditions: 45 printed by S for steps 16-22 and W20/W22, plus E16[29] = E17[29] (#26). #296's stage rates match the count through step 21 (22 survivors at step 19, 5 at 20, 1 at 21); the 13 W20/W22 carry conditions after step 21 are extrapolated |
| valid-tuple pairs | E[C(V,2)] <= q * 2^-5 for V valid tuples in one trial | #296: 9 within-part pairs in 2^34 part-trials, plus a cross-part bound; the charge exceeds the estimate by more than 20x |
| characteristic search | M_E = 593,858 solver CPU-s over 59 calls; output equals Fig. 6 | #396, Section 7 |
| operations of the characteristic search | at most 59 X_once m_once + I_max m_search = 3.947952e15 per measured run (E: times 32) | #396/#296 callgrind rate (Section 7); our profile of the charged workload type, our heavy-form emulations and our rate spread (Section 15) |

### 6.1 Credited reports (binding)

Each credited quantity comes from a public hash-smash pull request. Heuristic `credited-measurement-binding` states
that these reports describe the exact objects used here; the last column lists our own exact checks of each binding.

| Report | Author, head commit, submission | Files | What we use | Our exact checks |
|---|---|---|---|---|
| #26 | winglock, ff377db450879d36cbe2a9125ef80580af8603d1, 1e318d08-8449-4c9f-9a35-29547d3b7b66 | sha256-r32 `claim.json`, `proof.md` | table and Step-2/3 specification, analytic q = 2^-17.3254, measured 2^-17.3337, condition E16[29] = E17[29] | Section 14 items 2-7: rows, conditions, free-bit counts reproducing L4 = 2^17, L7 = 2^19 and the 2^32 P2 domain, Step-2 equations and tests (a)-(g), Step-3 stages on S's pair |
| #33 | winglock, e571806080ac312a7a2661d8fd5515b417a9bf1a, 9a70281e-e57d-44d9-b0a5-bad1cc234059 | sha256-r32 `claim.json`, `proof.md` | restatement of the #26 specification | as for #26 |
| #227 | yudduy, 689cb95ecd1538f08b536741a696c74f6fb78ea5, 8f955606-9f1f-4e60-9d9f-44b39af4c4b4 | `certificates/message-a.bin`, `message-b.bin`, `experiments/replay.py`, `manifest.json`, `proof.md` | a 32-step pair; campaign counts 14,643,237 valid tuples over 2.405e12 first blocks (2^-17.326) | Section 14 item 8: equal 32-step hashes, 0 mismatches against rows -4..22 |
| #296 | mitchuski, a22d18719c48ea71b6b428099cbe4fcb16a0884e, 1ded36a8-fbc2-4a10-9b6a-2e0c73787b6c | sha256-r32 `claim.json`, `proof.md` | q from four 2^32-trial runs (25,936 valid tuples), stage pass rates, bucket maximum 936, multiplicity sum 5.758e9, starting-solution runs (534.1 and 374.7 CPU-s), callgrind calibration | table sizes N, L4, L7 and P4 = 196,608 recomputed (Section 14 item 5); stage rates agree with the condition count through step 21 |
| #396 | mitchuski, 1b538044fb5afa0acad1de30aba770b602645535, 8bad82c1-1950-4e17-a025-bacdf5dda6ce | `experiments/fig6_replay.py`, `certificates/message-a.bin`, `message-b.bin`, `manifest.json`, `proof.md` | the 59-call search ledger (593,858 CPU-s, output equal to Fig. 6), the rediscovery factor 32, the calibrated call (44,197,378,388 instructions in 40.42 CPU-s) | our STP + CryptoMiniSat run E on the same re-parametrised model proved tE <= 5 infeasible, as the ledger's Step 2 found (Section 15.6); Fig. 6 rows checked against S's pair (Section 14 item 2) |
| #134 | jagnani73, 02177c4d788f7c3f6726872bf580f5e12c7ccaf9, 654cb3d2-47ad-4fdc-a000-85e3d696d09c | sha256-r31 `proof.md`, `experiments/completion.py` | precedent for CPU-second pricing | none needed |

## 7. The characteristic search (E)

v5 charges all advice construction, including search that is not part of the submitted program. S does not report the
running time of its characteristic search. We therefore charge the completed, measured re-run of S's four-step
procedure from public submission #396 (mitchuski).

**What was run (#396).**
- Tooling: the authors' model library (Peace9911/sha_2_attack, commit 6a9f35f, unmodified signed-difference step and
  expansion models) with STP 2.3.4 and CryptoMiniSat 5.11.21, called as `stp model.cvc --cryptominisat --threads N`.
  Every call ran under `/usr/bin/time -v`, which sums user and system CPU over all threads.
- Model: the authors' 31-step model re-parametrised to steps 4..22, expansion W16..W34, differences only in W4..W8,
  W12, W13, W20, W22, zero A/E differences at steps 0..3, zero A at 15..22 and zero E at 19..22.
- Procedure (S's Steps 1-4): (1) minimise tw; (2) with nabla W fixed, minimise tE; (3) lower tA until UNSAT;
  (4) minimise tE4. Each step lowers a `<=` threshold until UNSAT.

**Measured ledger.** 59 calls, including calibration, abandoned and timed-out calls, used 593,858 CPU-s
(99,644 wall-s) with a peak of 5.25 GiB.
- Step 1 proved tw = 22.
- Step 2 proved tE = 6.
- Step 3 proved tA = 19 in the relaxed model; S uses 21.
- Step 4, run at S's thresholds tE = 6 and tA <= 21, returned a characteristic at tE4 <= 76 whose signed rows
  A0..A22, E0..E22 and W0..W34 equal Fig. 6.
- A <= 111 call and a <= 78 call timed out; both are charged.

**Factor 32.** The run used two pieces of information from S: Step 1's nabla W pattern, because its own Step-1 optimum
was a different weight-22 pattern, and the tA = 21 threshold. #396 prices a blind re-derivation from its call ledger:
- Step 4 at one tA level costs 1.2-1.6M CPU-s at its 8-hour, 8-thread call cap.
- Recovering tA = 21 from the relaxed optimum 19 needs Step 4 at three tA levels.
- With Steps 1-3 this gives 3.8-5.0M CPU-s, i.e. 6.3-8.4 times M_E.
- A residual factor 4 covers run-to-run variance of the parallel SAT portfolio (one of two similar Step-4 calls
  timed out) and the choice among weight-22 nabla W patterns and exploratory models.

We adopt the product 32 unchanged and declare it as part of heuristic `route-search-measured`.

**Operations of the search, charged absolutely.**
- Calibration (#296/#396): one deterministic solver call took 40.42, 41.07 and 41.10 native CPU-s, and retired
  44,197,378,388 instructions under callgrind with identical output. At the fastest time this is R_cal = 2^30.026
  instructions per CPU-s.
- Our profile of the charged workload type (Section 15.6): STP 2.3.4 linked with CryptoMiniSat 5.11.21, called as
  `stp model.cvc --cryptominisat --threads N`, on the authors' model re-parametrised as above. Four calls, one per
  search step at 1, 2, 4 and 8 threads, each with its whole front end and 4-5 minutes of search, and a fifth call, E,
  that repeated Step 2 until STP returned its answer. Every executed instruction in every object is priced by its
  form (Section 15.1 table); multiply, divide and floating-point forms by their exact v5 emulation (Section 15.7).
- The measured run (59 calls, 593,858 CPU-s) executed at most I_max = S * R_cal * 593,858 = 1.2013e15
  instructions (`cpu-second-pricing`, with the rate spread S = 1.85 of Section 15.2). Each call runs one front end
  and one end part; ours take at most X_once = 196,316,567,529 instructions together. We charge
  - every instruction at the costliest search window of any profiled call, m_search = 3.247 operations, and
  - in addition 59 * X_once instructions at the costliest one-off part of any call, m_once = 4.084:

  operations <= 59 * X_once * m_once + I_max * m_search = 3.947952e15 (an effective 3.2864 per instruction).

  This needs no bound on the share of one-off work: the one-off instructions are counted absolutely, and counted a
  second time inside I_max. Whole searches averaged 1.828-2.150 operations per instruction, below m_search.
- Earlier prices. Our v4 package 23960a0e composed 3.6874 operations per instruction from a profile on our own CNF and
  the calibrated call's class shares; v5 (21b81d2d) charged 0.02 m_once + 0.98 m_search with a flat 400 for heavy
  forms; 49f8f6d4 priced every ordinary instruction at 5. Section 13 lists their totals at this T and cap: 46.508
  and 47.103 for the first and last.

**Charge.** E = ceil(32 * (59 * X_once * m_once + I_max * m_search) / C) = 56,805,068,562,863 units = 2^45.691085. The factor 32
multiplies the whole measured run, calls included. For comparison, this is 2,989,197 units per charged CPU-second.

## 8. Starting solution (D) and table build (C)

**D.** S Sect. 4 finds one solution of the characteristic through step 13 and reports about 2^34.3 for this, with no
unit; this solution is our advice. Read as 35-step compressions, 2^34.3 is below 2^34.46 target units. The organizer
reference costs (2140 operations for 31 steps, 2224 for 32) give 84 operations per step, so a 35-step compression costs
at most 2224 + 3 * 84 = 2476 operations, i.e. 1.114 units. #296 ran the same task twice with the authors' exact value model and all signed rows asserted: 534.1 and
374.7 CPU-s, both outputs checked exactly. At the kappa of Section 7 and a factor 32 those runs price the task at
32 * 908.8 * 2,989,197 = 2^36.34 units (2^37.83 at kappa = 2^23). We charge **D = 2^38 = 274,877,906,944 units**,
which covers every reading.

**C.** The loop iteration counts are:

| Loop | Count |
|---|---|
| P1 E4 and W7 scans | at most 2^33 |
| P2 triples | 2^32 |
| P3 E4 loop | 10,240 * 131,072 = 2^30.32 |
| P3 W7 loop, counting plus placing passes | 2 * 155,008 * 524,288 = 2^37.24 |
| P4 | at most 2^8 + 12 * 2^15 |

The total is under 2^37.43 iterations. Each iteration recomputes at most two step equations, a few conformance checks
and one record write, which is at most 1024 operations. The 2^27-bucket prefix sum adds at most 2^29 operations.
Thus C <= 2^37.43 * 1024 / 2224 + 2^29 / 2224 < 2^36.32 units. We charge **C = 2^38 = 274,877,906,944 units**.

## 9. Success probability

Let V be the number of valid tuples in a trial and X the number of conforming P4 entries for a valid tuple.

- **Every valid tuple is tried.** Step 2 accepts every record that passes tests (a)-(g), and Step 3 runs on every
  accepted record (Section 5.2). Nothing selects among the valid tuples of a trial. Let X_t be the number of
  conforming P4 entries of valid tuple t, and Y = sum_t X_t. The trial succeeds if Y >= 1.
- **Per tuple.** E[X_t | t valid] = 196,608 * 2^-46 = mu = 2^-28.415 (`step3-46-conditions`). The entries share W14 in
  12 groups of 2^14, and the 12 W20 sign/carry conditions are common inside a group. Hence
  E[C(X_t,2) | t valid] <= 12 * C(2^14, 2) * 2^-12 * (2^12 p)^2 + C(2^17.585, 2) p^2 <= 2^-49.3, so
  E[X_t^2 | t valid] <= mu + 2^-48.3.
- **First moment, by linearity over the records of TAB2.** E[Y] = sum over records of Pr[valid] * E[X_t | t valid]
  = E[V] mu, with E[V] >= q >= 2^-17.3583 (`q-32step-matching-rate`). No conditioning on the other records is used.
- **Second moment.** E[C(Y,2)] = E[sum_t C(X_t,2)] + E[sum over pairs t < t' of X_t X_t']. The first part is at most
  E[V] 2^-49.3. The second involves only trials with two or more valid tuples; their number of pairs is
  E[C(V,2)] <= E[V] 2^-5 (`valid-tuple-pairs`).
- **Dependence between two valid tuples of one trial (Section 9.1).** Two valid tuples t, t' of a trial share CV1.
  Section 9.1 proves that stages 16..19 of t are independent of the validity of t', that the only remaining channel
  is t's two schedule constants c20 and c22, and measures that channel directly, on synthetic and on real TAB2
  records. The measured ratios are at most 1.154 (upper confidence); we charge kappa = 1.5:
  E[X_t X_t' | both valid] <= 1.5 (mu + 2^-48.3). The pair part is then at most E[V] mu 1.5 2^-5 (1 + 2^-19.885).
- **Per trial success.** s >= Pr[Y >= 1] >= E[Y] - E[C(Y,2)] >= 2^-17.3583 * 2^-28.415 * (1 - 1.5 * 2^-5 -
  2^-20.885 - 1.5 * 2^-24.885) = 2^-45.842601. With kappa = 1 the success bound at our T would be 0.3950; with
  kappa = 2 it is 0.3851 (below 0.39), and kappa = 4 would give 0.3648.

Trials use fresh coins and are independent. If U is the event that some trial among the T uncapped trials succeeds,
then Pr[U] >= 1 - (1 - s)^T >= 1 - exp(-sT). With T = 31,292,887,053,577, sT = 0.495961, so Pr[U] >= 0.391015.

**Cap stop.** Let X_t be the counted operations of trial t in the uncapped run, and S = X_1 + ... + X_T. If S <= W_cap,
the capped run behaves exactly like the uncapped one. So Pr[success] >= Pr[U] - Pr[S > W_cap].

The X_t are independent and identically distributed. Using the Section 5.4 charges and the Section 6 inputs:

```
E[X] <= 8 * 10.4068                                              (scan)
      + (N / 2^32) * (200 + 48*0.51 + 48/15 + 48/120 + 1256/240)  (Step 2)
      + 2^-17.3166 * (1 + 2^-5) * (400 + 196,608 * (40 + 192 * (2^-2.99 + 14 * 2^-14.9)))   (Step 3)
      = 83.25 + 75.88 + 79.81 = 238.94 operations.
```

Here 2^-17.3166 is the upper confidence limit of q. A trial's Step-3 work is at most 574,095,760 V operations, with
574,095,760 = 400 + 196,608 * (40 + 15 * 192), and its Step-2 work is at most 1600 m for m key matches. Using
(x + y + z)^2 <= 3(x^2 + y^2 + z^2):
- E[scan^2] <= 64 * 936 * 10.4068;
- E[m^2] <= 4 * 5.758e9 / 2^32 = 5.3626, by Cauchy-Schwarz over the 4 index-parts;
- E[V^2] = E[V] + 2 E[C(V,2)] <= 2^-17.3166 (1 + 2^-4).

This gives E[X^2] <= 3 (6.234e5 + 1.373e7 + 2.145e12) = 6.436e12. By Chebyshev,

```
Pr[S > 254 T] <= T * E[X^2] / (T * (254 - 238.943))^2 = 6.436e12 / (226.72 * T) <= 9.07e-4.
```

**Result.** Pr[success] >= 0.391015 - 0.000907 = **0.390108 >= 0.39 claimed** (= the required minimum). The claim
does not rely on rounding: the margin is 0.000108. A second moment 10 times larger than charged would lower the bound
to 0.3819 (Section 13).

### 9.1 Two valid tuples of one trial: proof and measurement (new in v8)

The pair part of the second moment needs E[X_t X_t' | t and t' valid] for two records t, t' of one key class that
are both valid on the same CV1 = (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]). We first prove what does
not depend on t', then measure the rest.

**Lemma 1 (what validity reads).** Step 2 computes, for a record r, E_i = A[i-4] + A_i - Sigma0(A[i-1]) -
MAJ(A[i-1], A[i-2], A[i-3]) for i = 0, 1, 2 (A0 from the pair, A1, A2 from the combination) and
W_i = E_i - A[i-4] - E[i-4] - Sigma1(E[i-1]) - IF(E[i-1], E[i-2], E[i-3]) - K_i for i = 0..6. Tests (a)-(g) read
W4..W6, the record's E3..E6 and A0..A2, E0..E2 and the advice; steps 0..3 carry no difference, so test (e) concerns
steps 4..6 only. W4..W6 read CV1 only through E0..E2, and E0..E2 read only A[-1..-4] = CV1[0..3]. So the validity of
every record of a trial is a function of CV1[0..3] and that record; CV1[4..7] = E[-1..-4] never enter.

**Lemma 2 (W0..W3 are fresh).** Fix a record t and CV1[0..3]. Then
W3 = d3 - E[-1], W2 = d2(E[-1]) - E[-2], W1 = d1(E[-1], E[-2]) - E[-3], W0 = d0(E[-1], E[-2], E[-3]) - E[-4],
where each d_i depends on CV1[0..3], the record and the words shown. This is a triangular bijection between
CV1[4..7] and (W3, W2, W1, W0). Under the premise already declared in `q-32step-matching-rate` (CV1 words behave as
uniform), CV1[4..7] is uniform and independent of CV1[0..3]. So for every tuple of the trial, (W0, W1, W2, W3) is
uniform on 2^128 and independent of every validity event of the trial (Lemma 1) and of the tuple's W4..W15.

**Lemma 3 (stages 16..19 are independent of t').** With W4..W15 fixed, (W16, W17, W18, W19) =
(s1(W14) + W9 + s0(W1) + W0, s1(W15) + W10 + s0(W2) + W1, s1(W16) + W11 + s0(W3) + W2, s1(W17) + W12 + s0(W4) + W3)
is again a triangular bijection of (W0..W3): W19 gives W3 once W17 is known, then W18 gives W2, W17 gives W1 and W16
gives W0. So W16..W19 are uniform and independent of every Step-2 event of the trial. Their differences are 0:
W0..W3, W9..W11, W14 and W15 carry none, and test (b) cancels s0(W4') + W12' - s0(W4) - W12. Steps 16..19 read only
the advice, the P4 entry and W16..W19. Hence for every P4 entry, stages 16..19 of t pass with the same probability
and the same joint law of states whether or not t' is valid. This is exact, not measured.

**Lemma 4 (the only channel).** From step 20 on, the tuple enters only through
W20 = s1(W18) + c20 with c20 = W13 + s0(W5) + W4 and c20' = c20 + D(W20) (test (g));
W21 = s1(W19) + W14 + c21 with c21 = s0(W6) + W5 = c21' (test (f));
W22 = s1(W20) + W15 + c22 with c22 = s0(W7) + W6, where c22' - c22 depends only on the record word W7;
and the record difference W8' - W8 in W24 (W23, W25, W26, W28, W30 and W31 have no difference once the earlier ones
vanish, and W27's difference is the constant D(W20) + s0(W12') - s0(W12) = 0). W21 adds equally to both sides and the
difference of E21 does not involve it, so c21 has no effect. A second valid record can therefore change t's Step-3
probability only by changing t's c20 and c22, that is t's W4..W6 values inside t's own validity set.

**Measurement 1: the channel on synthetic tuples.** `condexp.c` runs the real two-sided second block from the
advice and the real P4 list (rebuilt from the advice by `secondblock.py`: 196,608 entries, S's entry among them; the
simulator passes S's own tuple at all 16 stages). It draws a uniform entry and uniform W16..W19 (their law under any
Step-2 conditioning, Lemma 3) and, for each history through step 19, evaluates stages 20..31 for every tuple-constant
vector. 64 vectors came from W4..W6 drawn uniformly from the validity set of S's record (signs and tests (b), (f),
(g)). Seeds 1000-1009, 48,814,374 histories through step 19: the pass counts per vector were 670-815
(mean 744, standard error about 26 from the split into ten processes): max/mean
1.095, upper bound (max + 2 SE)/mean 1.154, min/mean 0.900. The
through-19 rate is 2^-28.00 (#296: 2^-27.79) and stage 16 passes at exactly 2^-3.

**Measurement 2: direct, on real TAB2 records.** `table.py` rebuilds P1-P3 exactly as Section 4 states and
reproduces every published count: |L4| = 131,072, |L7| = 524,288, 10,240 combinations, 155,008 pairs and
N = 1,396,774,912 records. It keeps the 1/256 key slice whose top byte is 0x00: 5,618,824 records,
1,116,588 key classes with two or more records. For a record t, CV1[1..3] -> (E0, E1, E2) ->
(W4, W5, W6) is a bijection, so `pairexp.py` draws a uniform CV1 conditioned on "t valid" as a uniform (W4, W5, W6)
passing t's tests, maps it back to CV1[1..3], and runs the full Step-2 tests (a)-(g) of every other record of the
class on that CV1 (checked on S's record: its own CV1 is recovered and it is valid). We used classes of 2 to 16
records and at most 4 records t per class; 254 drawn records that no CV1 makes valid were skipped. Over
3,522,560 valid-t draws
there were 19,317 pair events (another record of the class also valid), a conditional rate of
2^-7.51. For 520 pair events we kept t's tuple constants, and for the same records equally many from
single events. `condexp.c` (24,407,256 histories, seeds 2000-2009) gives a Step-3 pass-rate ratio, pair over single,
of **0.998 +- 0.003**. Within each of 8 real records (32 tuples each from its own validity
set) the largest max/mean was 1.138, at Poisson noise of about 0.05.

**Consequence.** All measured ratios are at most 1.154 at their upper confidence bounds. We charge
kappa = 1.5: E[X_t X_t' | t, t' valid] <= 1.5 (mu + 2^-48.3), stated as heuristic `valid-tuple-pair-dependence`
with this data. The measurements also corroborate `step3-46-conditions`: the simulated per-candidate rate is
2^-44.0, above the charged 2^-46.

## 10. Time ledger (exact)

All figures are in target-compression units; C = 2224.

```
A + B = ceil((T * (2224 + 64) + 254 * T) / 2224) + 8
      = ceil(31,292,887,053,577 * 2,542 / 2224) + 8
      = 35,767,319,644,879 units = 2^45.0237
        (T first-block compressions; 64 fixed ops per trial; the counted cap 254 T;
         8 units for the final 6-compression verification, the comparison and the refused-cap test)
C     =             274,877,906,944 = 2^38
D     =             274,877,906,944 = 2^38
E     =          56,805,068,562,863 = 2^45.691085   (ceil(32 * (59 * X_once * m_once + I_max * m_search) / 2224))
total =          93,122,144,021,630 = 2^46.404190  <=  2^46.41 = 93,497,952,144,648
C + D + E =      57,354,824,376,751 = 2^45.704980  <=  2^45.71
```

The claimed time_log2 = 46.41 leaves a factor of 1.0040 in reserve. It does not depend on rounding the
exponent.
Every term above is a hard bound given its charge: A and B follow from T and W_cap on every coin sequence, and C, D
and E are one-time charges. Parallel execution does not change these totals.

## 11. Memory and advice

| Item | Bytes |
|---|---|
| TAB2: 16 N | 22,348,398,592 |
| bucket offsets: 4 * (2^27 + 1) | 536,870,916 |
| L4, L7, combinations, pairs, P4 with its constants (one 256-bit word per stored 32-bit value, under 80 MB), code and state | < 2^27 |
| largest solver resident set (search and start runs, #296/#396) | 5,642,330,112 |
| **sum** | **28,661,817,348 = 2^34.739** |

The phases run one after another, so adding the solver peak is conservative. We claim 35. The advice consists of the
signed rows, 71 two-bit conditions, the readings, 18 advice words and the round constants. It fits in fewer than
8,192 bytes, so we claim 13.

## 12. Heuristics (IDs as in claim.json)

- `q-32step-matching-rate` (score-critical). A uniform C_32 first block yields at least 2^-17.3583 expected valid
  tuples against TAB2.
  - Evidence: #296's four 2^32-trial runs (Section 6), #26's runs, #227's campaign counts, and the analytic
    prediction.
  - Assumption: CV1 words behave as uniform for the Step-2 tests.
- `step3-46-conditions` (score-critical). Each P4 entry conforms with probability at least 2^-46, and
  r >= 2^-28.415 (1 - 2^-20).
  - Evidence: the condition count, stage rates through step 21, and the #227 instance (Section 3).
  - The 13 carry conditions after step 21 are extrapolated.
- `valid-tuple-pairs` (supporting). E[C(V,2)] <= q 2^-5.
- `route-search-measured` (score-critical). Re-deriving S's characteristic costs at most 32 * 593,858 solver CPU-s.
  - Evidence: #396's completed 59-call run, which printed Fig. 6 (Section 7).
  - The factor 32 is priced from the run ledger, not executed.
- `cpu-second-pricing` (score-critical). The measured 59-call run executed at most S * R_cal * 593,858 instructions,
  i.e. at most 1.85 times the calibrated instructions per CPU-s, and no long stretch of its search cost more operations
  per instruction than our costliest search minute (3.247).
  - Evidence: the credited callgrind rate (Section 7), our rate runs (Section 15.2), our profile of STP + CryptoMiniSat
    on the re-parametrised model with exact heavy-form emulations (Sections 15.6-15.7).
  - The one-off work is charged absolutely (59 front ends and end parts at m_once = 4.084); no share is assumed.
- `starting-solution-cost` (supporting). The Step-1 starting solution costs at most 2^38 units (Section 8).
- `work-moments` (supporting). These are the occupancy, multiplicity and stage-pass inputs to E[X] and E[X^2].
  - They affect only the 9.07e-4 cap-stop term, and through it the success bound.
- `search-peak-memory` (supporting). The solver peak is at most 2^33 bytes. This affects memory only.
- `valid-tuple-pair-dependence` (supporting, measured since v8). For two distinct records valid in the same trial,
  E[X_t X_t' | both valid] <= 1.5 (mu + 2^-48.3).
  - Evidence: the proof of Section 9.1 (stages 16..19 independent; c20, c22 the only channel) and the measurements
    there: Step-3 pass rate over tuple constants flat within 1.154 (synthetic validity set) and
    1.138 (eight real records), and pair-conditioned over single tuples of the same real records
    0.998 +- 0.003.
  - Only the pair part of the second moment uses it. With kappa = 2 the success bound would be 0.3851.
- `credited-measurement-binding` (supporting, new). The credited reports of Section 6.1 (#26, #33, #227, #296, #396)
  measured exactly the predicates, tables, tests, model and accounting restated here.
  - Evidence: the head commits, files and counts of Section 6.1, and our exact checks listed there (Section 14,
    run E of Section 15.6).

## 13. Sensitivity and limitations

| Change | Total time_log2 |
|---|---|
| as charged (absolute charge, m_once = 4.084, m_search = 3.247, factor 32, kappa = 1.5) | 46.404 |
| every heavy-form price doubled | 46.471 |
| one-off instructions 10 times ours | 46.496 |
| m_search + 10% / + 25% | 46.489 / 46.607 |
| search priced at the largest whole-search mean (2.150) instead of the costliest minute | 46.076 |
| v4 composition, 3.6874 per instruction | 46.508 |
| class price of 49f8f6d4 | 47.103 |
| kappa 2^23 (841646f2) | 47.476 |
| spread S = 1 / 2.5 / 3.63 instead of 1.85 | 45.936 / 46.681 / 47.064 |
| factor 16 | 45.879 |
| factor 64 | 47.091 |
| factor 128 | 47.905 |

| p per entry, second moment or pair allowance | Success bound at T = 2^44.8309, W_cap = 254 T |
|---|---|
| 2^-46, kappa = 1.5 (charged) | 0.390108 |
| 2^-46.5 | 0.2949 (below 0.39) |
| 2^-47 | 0.2187 (below 0.39) |
| E[X^2] 10 times the charged bound | 0.3819 (below 0.39) |
| pair allowance kappa = 1 / 2 / 4 | 0.3950 / 0.3851 / 0.3648 |

Limitations, stated plainly:
- No participant run here rebuilt TAB2 or measured q, p or the search. Every rate is a credited public participant
  measurement. Our own checks are the exact finite checks of Section 14, with no extrapolation.
- p = 2^-46 rests on a condition count that is measured through step 21 and extrapolated for the last 13 carry
  conditions. If one more independent condition existed, the success bound would fall below 0.39 at this T. The
  public 32-step pair of #227 shows that the full conformance event is reachable from C_32 first blocks.
- S's historical search time is unpublished. E is a measured re-run times an argued rediscovery factor, not S's own
  cost.
- The CPU-second price uses one calibrated call for the instruction rate. Our rate runs used a different machine,
  instruction set and solver build, and enter only as a relative spread (Section 15.3).
- Our profile of the charged workload type (Section 15.6) used our own binaries (Debian's CryptoMiniSat 5.11.21
  and our STP 2.3.4 build) and our regeneration of the model from #396's description. Its search windows cover the
  first minutes of each search (only E ran to its answer), while the charged calls searched for hours. The price
  holds if no long stretch of their search cost more per instruction than our costliest minute (3.247); with
  m_search 10% higher the total is 46.489.
- The cap 254 T leaves 15 operations per trial above the charged mean E[X] <= 238.94, so the cap-stop term
  (9.07e-4) is larger than in 23960a0e. A second moment 10 times the charged bound would lower the success bound to
  0.3819.
- The organizer sandbox cannot hold a 22 GB table, and it cannot run CryptoMiniSat or read hardware counters, so no
  experiment is declared. The checks of Sections 14 and 15 are participant runs.

## 14. Participant checks (our code)

We wrote a stand-alone Python implementation of the step equations of Section 1, independently of any submitted
package code. Its full-message hash agrees with the organizer's `verifier/hash_functions.py:digest` for 32, 35 and 64
steps on both messages of S's pair. Results:

1. **S's pair.** M0 = a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a cadc14e8 d59ac191
   6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8.
   - M1' (unprimed) = c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef 6ec97e18 5100da8a
     0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1.
   - M1 differs in words 4..8 (a4d6cd0f 21811cec ea897317 db9ec665 6ec17218) and 12..13 (45f2222c 4d12f88a).
   - The 35-step hashes are equal. S's printed "hash" equals the second-block chaining value
     C_35(CV1, M1) = c6209b2b...e444451f. The 31-, 32- and 64-step hashes differ.
   - CV1 = C_35(IV, M0) = c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2.
2. **Rows.** With unprimed = M1', every symbol of rows -4..34 holds: 119 `n`/`u` symbols and 360 value symbols, with
   0 mismatches. The opposite orientation fails on all 119 `n`/`u` symbols, which confirms the orientation.
3. **Two-bit conditions.** 66 of the 73 printed relations hold as printed. The 7 that do not are exactly those
   re-read in Section 2, and under the readings all 71 hold. E16[29] = E17[29] holds on the pair.
4. **Advice.** The advice words of Section 4 are recomputed from the pair.
5. **Free bits.** Free-bit counts per row: E3 26, E4 18, E5 5, E6 12, E7 15, W7 25, E14 8, E15 15. These reproduce
   the 2^32 P2 domain and, after the stated two-bit conditions, |L4| = 2^17 and |L7| = 2^19.
6. **Step 2 on the published record.**
   - The record built from S's tuple has key A[-1] = E3 - A3 + Sigma0(A2) + MAJ(A2, A1, A0) equal to CV1[0].
   - The Section 5.2 equations reproduce W0..W6 = M1'[0..6].
   - Tests (a)-(g) all pass.
7. **Step 3 on S's (W14, W15).** Every stage 16..31 passes, and C_32(CV1, M1) = C_32(CV1, M1').
8. **Public 32-step pair (#227).** The Section 3 results hold: equal 32-step hashes, 0 mismatches against rows -4..22
   from CV1 = C_32(IV, M0) (unprimed = message b), and no difference in W23..W31.

These checks establish that the written specification is consistent with the published instance and with a
32-step instance. They do not measure rates. The rates are the credited inputs of Section 6.

## 15. CPU-second price: our own evidence

This section is our own work. It supports `cpu-second-pricing` and does not re-run any charged call. The charge
for the measured run is 59 * X_once * m_once + I_max * m_search operations (Section 7):
- I_max = S * R_cal * 593,858, with R_cal = 2^30.026 instructions per CPU-s of the calibrated call (#296/#396) and
  S = 1.85 from the spread we measured (Section 15.2);
- m_once = 4.084 and m_search = 3.247 from our profile of STP + CryptoMiniSat on the re-parametrised model
  (Section 15.6), with every heavy form priced by its exact emulation (Section 15.7);
- X_once = 196,316,567,529 instructions, the largest front end plus the largest end part of a profiled call.

### 15.1 Operations per instruction: per-form costing of the solver code

- Code: CryptoMiniSat 5.11.21 for x86-64, the version #396 ran inside STP, taken from the wheel
  `pycryptosat-5.11.21-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (SHA-256 2358aa1453a6cf0d...e2f6fb;
  library SHA-256 878e2f2b2f94a823...8659c0). We disassembled it with Apple LLVM objdump 21 (Intel syntax) and did
  not execute it.
- Charges, under the v5 primitive list. A 256-bit word holds any x86 register or SSE value, and each data field of the
  program sits in its own word; the x86 code already contains its own bit-field shifts and masks, which are charged
  as instructions.

| Form | Primitive operations |
|---|---|
| memory operand | address: 1 per added term, +1 for a scaled index (base+index*s+disp = 3, rip+disp = 1) |
| mov, movabs | 1 + address; +2 to merge into an 8- or 16-bit register |
| movzx; movsx, movsxd | 2 + address; 4 + address |
| add, sub, and, or, xor, cmp, test | 1; +1 memory source; +2 read-modify-write; +1 mask for 32-bit add/sub; +2 merge for 8/16-bit; adc/sbb +2 |
| inc, dec, neg, not, shl, shr | 1; +2 read-modify-write; +1 mask for 32-bit (not shr); +2 merge for 8/16-bit |
| sar; rol, ror, shld, shrd | 3; 4 |
| lea | number of address operations (at least 1) + 32-bit mask |
| jmp; jcc | 1 (2 + address through memory); 2 (3 for signed conditions) |
| cmovcc; setcc | 3 (+1 memory source, +1 mask for 32-bit); 2 (+1 store or +2 merge) |
| call, ret, leave; push, pop | 3 each, call through memory +1 + address; 2 each, push from memory +1 + address |
| cdq/cqo; xchg; cmpxchg, xadd; bt; bts/btr | 3; 3-4; 6; 2; 4 |
| bsf, bsr, tzcnt, lzcnt, popcnt, bswap | 32 |
| string instructions | 6 per iteration |
| SSE moves; SSE logic; packed integer arithmetic; shuffles, unpack, pack | 1 + address; 1; 8; 16 |
| multiply, divide, floating-point arithmetic or conversion | 400 in Sections 15.1-15.5; in this package priced per form by Section 15.7 |
| any other form | 8 |

| Code set | Instructions | Heavy | Mean operations per ordinary instruction | Ordinary above 5 |
|---|---|---|---|---|
| `PropEngine::propagate_any_order` (4 instantiations) | 1,612 | 0 | 1.70 | 0 |
| hot set: `propagate_any_order`, `propagate_light`, `analyze_conflict`, `litRedundant`, `minimize_using_bins`, `cancelUntil`, `new_decision`, `new_decision_fast_backw`, `enqueue`, `find_conflict_level`, `search`, `attach_and_enqueue_learnt_clause` (26 symbols) | 6,000 | 13 | 1.71 | 0.15% |
| whole library (400 unrecognised forms, mostly lock-prefixed atomics, charged 8) | 253,984 | 3,092 | 1.73 | 0.66% |

The commonest forms in the hot set are mov (38.9%), cmp (7.3%), lea (5.5%) and add (4.4%). These figures are static
counts. Section 15.5 weights the same per-form prices by measured execution counts. The dynamic ordinary mean,
1.880-1.956, is a little above the static 1.71-1.73, because cmp, add and conditional branches execute more often
than they occur in the code.

### 15.2 Instruction rate: CryptoMiniSat on SHA-256 CNF (our runs)

- Machine and solver: Apple M4 Pro (8 performance and 4 efficiency cores), macOS, CryptoMiniSat 5.16.0 through
  pycryptosat (arm64). All runs used `nice -n 10` while an unrelated long job kept the load average near 70.
- Instances, from our generator (Tseitin CNF with ripple-carry adders and XOR, Ch and Maj gates; a few message bits
  fixed at random per seed):
  - pair: two N-step SHA-256 compressions from one free chaining value with free message words, a forced difference in
    W0 and k of the 256 state bits equal after N steps. With wt, an adder-tree bound on the Hamming weight of the
    message difference, the shape of the route-search thresholds.
  - pre: N steps from the IV with k output bits fixed.
- Counters: `proc_pid_rusage(RUSAGE_INFO_V6)` instructions, cycles and performance-core split, read immediately
  before and after `solve()`, with `getrusage` user plus system time. `/usr/bin/time -l` on each whole process, which also counts
  the Python generation, agrees within 1% for every run above 5 CPU-s and within 11% for the 1-2 s runs.
- Total solver time: 561 CPU-s.

| Instance | Threads | Variables / clauses | Result | Solve CPU-s | Instructions per CPU-s | IPC | P-core share |
|---|---|---|---|---|---|---|---|
| pair N=20 k=256, seed 1 | 1 | 26,097 / 172,850 | conflict limit | 15.9 | 9.23e9 = 2^33.10 | 2.40 | 0.94 |
| pair N=20 k=256, seed 2 | 1 | 26,097 / 172,850 | conflict limit | 18.6 | 7.74e9 = 2^32.85 | 2.19 | 0.70 |
| pair N=20 k=256, seed 3 | 1 | 26,097 / 172,850 | conflict limit | 18.7 | 8.26e9 = 2^32.94 | 2.33 | 0.71 |
| pair N=20 k=256, wt <= 40, seed 1 | 1 | 29,114 / 189,471 | conflict limit | 1.2 | 8.08e9 = 2^32.91 | 2.24 | 0.77 |
| pair N=20 k=256, wt <= 40, seed 2 | 1 | 29,114 / 189,471 | conflict limit | 1.8 | 7.68e9 = 2^32.84 | 2.15 | 0.74 |
| pre N=24 k=96, seed 1 | 1 | 16,193 / 109,217 | conflict limit | 25.4 | 9.31e9 = 2^33.12 | 2.62 | 0.73 |
| pre N=24 k=96, seed 2 | 1 | 16,193 / 109,217 | conflict limit | 31.0 | 9.58e9 = 2^33.16 | 2.67 | 0.75 |
| pair N=24 k=256, seed 1 | 1 | 32,673 / 218,914 | conflict limit | 280.6 | 6.59e9 = 2^32.62 | 1.84 | 0.74 |
| pre N=32 k=128, seed 1 | 1 | 22,769 / 155,313 | conflict limit | 60.0 | 12.14e9 = 2^33.50 | 3.35 | 0.77 |
| pair N=17 k=160, seed 1 | 1 | 21,165 / 138,110 | SAT | 12.4 | 8.75e9 = 2^33.03 | 2.44 | 0.75 |
| pair N=17 k=160, seed 2 | 1 | 21,165 / 138,110 | SAT | 9.5 | 9.80e9 = 2^33.19 | 2.69 | 0.79 |
| pre N=20 k=48, seed 1 | 1 | 12,905 / 86,137 | time limit | 20.3 | 8.06e9 = 2^32.91 | 2.22 | 0.78 |
| pair N=18 k=128, seed 1 | 1 | 22,809 / 149,562 | time limit | 20.3 | 9.00e9 = 2^33.07 | 2.51 | 0.75 |
| pair N=22 k=256, seed 5 (6 chunks of 30,000 conflicts) | 1 | 29,385 / 195,882 | conflict limit | 7.8 | 7.42e9 = 2^32.79 | 2.09 | 0.72 |
| pair N=20 k=256, seed 1 | 4 | 26,097 / 172,850 | time limit | 12.6 | 8.38e9 = 2^32.96 | 2.33 | 0.76 |
| pre N=24 k=96, seed 1 | 4 | 16,193 / 109,217 | time limit | 12.3 | 7.82e9 = 2^32.86 | 2.19 | 0.74 |
| pair N=20 k=256, wt <= 40, seed 1 | 4 | 29,114 / 189,471 | time limit | 12.6 | 8.06e9 = 2^32.91 | 2.27 | 0.72 |

Three further instances (pair N=16, k=256, seeds 1-3) solved in 0.02-0.03 CPU-s at 1.2-1.7e10 instructions per CPU-s.
They are start-up work only and we leave them out of the spread.

Results for the 14 single-thread runs:
- Instructions per CPU-s: mean 8.69e9 = 2^33.02, median 8.50e9, coefficient of variation 14.9%, range 6.59e9 to
  12.14e9. That is max/min = 1.842 and max/median = 1.43. The CPU-weighted rate is 8.00e9 at IPC 2.23.
- The longest run, with the largest resident set (pair N=24, 281 CPU-s, 348 MB), had the lowest rate.
- Within one run (pair N=22, seed 5), the six consecutive chunks ran at 1.00, 0.99, 0.96, 0.85, 0.91 and 0.96 times
  the first chunk. The rate did not rise as learnt clauses accumulated.
- Four threads against one thread on the same instance gave 0.91, 0.84 and 1.00 times the single-thread rate per
  CPU-s.
- Part of the spread comes from the core type: performance cores ran 70-94% of the CPU time, at IPC 2.04-3.60,
  against 1.0-2.1 on efficiency cores.

### 15.3 What transfers to the measurement machine

- The absolute rate does not transfer. Here the solver retires 2^32.6-2^33.5 arm64 instructions per CPU-s, 6-11 times
  R_cal. A CPU-second on this machine does more solver work, and the ledger counts measurement-machine CPU-seconds, so
  only R_cal prices them.
- The per-form costing and the dynamic profile transfer directly. They describe the x86-64 code of the solver version
  that ran the charged calls, and the instruction stream it executes on SHA-256 CNF, not a property of our machine.
  The STP-linked build may use different compiler flags from the wheel.
- The spread transfers as an empirical range only. It measures how much the per-CPU-second rate moves across instance
  shapes, sizes, seeds, run length and threading for this solver on SHA-256 CNF. We apply its full max/min ratio, as if
  the calibrated call sat at the bottom of the range and every charged CPU-second at the top. The charged calls were
  long, multithreaded and large (5.25 GiB peak). In our runs those three properties lowered the rate or left it
  unchanged.
- If the charged calls retired more than 1.85 times R_cal, or a long stretch of their search cost more than
  m_search = 3.247 operations per instruction, the charge would no longer cover them. Section 13 gives the size of
  either effect.

### 15.4 Why no organizer experiment

The organizer runner offers standard-library Python only, with one CPU, 128 MiB and 20 s. It requires byte-identical
output and does not credit runtime or operation counts. It cannot run CryptoMiniSat or read hardware counters, so the
rate cannot be re-measured there. Our scripts are participant tools: the CNF generator and rate harness (SHA-256
8b78762691099e46...), the per-form costing (220b1ab3aad0e96f...) and the run log.

### 15.5 Dynamic per-form profile of the charged library on our SHA-256 CNF (v4)

- Binary: CryptoMiniSat 5.11.21 for x86-64 from the pycryptosat 5.11.21 manylinux wheel, library SHA-256
  878e2f2b2f94a82331c775db2d05f957593be176e64692cd046f1998968659c0, the same file as Section 15.1. It ran as x86-64
  code in a `python:3.12-slim` linux/amd64 container.
- Tool: valgrind 3.24.0, callgrind with `--dump-instr=yes --toggle-collect='CMSat::SATSolver::solve*'`. Only
  instructions executed inside the solve call are counted, in every object it reaches: CryptoMiniSat, libc,
  libstdc++, libm and libgcc_s. Each counted address was matched to its instruction in `objdump -d -M intel` of the
  same object, with 0 unmatched. Each instruction was priced by the Section 15.1 table (`x86ops.py`), and
  unrecognised forms were charged 8.
- Workloads: our SHA-256 CNF generator (Section 15.2), one solve call of 60,000 conflicts each, single thread.

| Instance | Instructions in solve | m, all instructions | ordinary mean | heavy share | CryptoMiniSat / libc share |
|---|---|---|---|---|---|
| pair N=20 k=256, seed 1 | 23,059,870,223 | 2.797 | 1.880 | 0.230% | 96.2% / 3.4% |
| pre N=24 k=96, seed 1 | 19,971,134,691 | 2.801 | 1.956 | 0.212% | 97.8% / 2.0% |
| pair N=20 k=256, wt <= 40, seed 2 | 19,079,473,631 | 3.106 | 1.925 | 0.297% | 95.6% / 4.0% |
| pair N=17 k=160, seed 1 | 20,426,990,077 | 2.910 | 1.911 | 0.251% | 96.6% / 3.1% |

- Commonest executed forms: mov 27-28%, cmp 13-14%, add 9-12%, jne 7-8%, je 6%, lea 5%.
- Executed cost histogram for pair N=20: 1 operation 44.4%, 2 operations 37.2%, 3 operations 10.7%, 4 operations
  4.2%, 5 operations 2.4%, 8 operations 0.8%, 16-32 operations 0.06%, heavy (400) 0.23%. libm, where floating point
  runs at 72-74 operations per instruction, is 0.035-0.066% of the instructions.
- How the profile entered the v4 price: the largest ordinary mean, 1.956 (pre N=24), the calibrated call's heavy
  share 0.416% (our runs: 0.21-0.30%) and its 7.24% PLT share at 3 operations gave m_dyn = 3.6874. Section 15.6 now
  sets the price from the charged workload type itself. This profile is kept as corroboration of the search mix.
- Why it transfers: the price is for the charged calls on the measurement machine. What we measured is a property
  of the code: the operations per instruction of the instruction stream that this solver executes on SHA-256 CNF.
  The machine-dependent parts, the rate R_cal and the spread S, are unchanged.
- What it does not cover:
  - The STP front end (parsing and bit-blasting) is not profiled. In the charged calls it runs once per call,
    before the search.
  - STP's own build of CryptoMiniSat may use different compiler flags.
  - The charged model's CNF differs from our SHA-256 instances. Across our four shapes the ordinary mean moved by 4%.
  - Multithreaded runs add clause-sharing atomics. Those are lock-prefixed forms, charged 8 here, and our static scan
    found them only outside the hot set.
- Reproduction: Appendix A lists the scripts with their SHA-256 hashes. `setup.sh` installs valgrind and the wheel,
  `runs.sh` runs the four profiles, and `dynall.py` prices them. `lbench.py` is the Section 15.2 generator with the
  macOS hardware counters removed.

### 15.6 Profile of the charged workload: STP + CryptoMiniSat on the re-parametrised model

Sections 15.1-15.5 profiled the solver library on our own SHA-256 CNF. This section profiles the workload type that
was charged: STP calling CryptoMiniSat on the authors' characteristic model, front end included.

- **Software.** STP 2.3.4 (github.com/stp/stp, tag 2.3.4, commit d70085462f07c8a5a2f1225f727cda3ef505b141; its
  version banner still prints 2.3.3), built from source as a CMake Release build with GCC 14.2.0 and linked against
  CryptoMiniSat 5.11.21 from Debian 13 (`libcryptominisat5-5.11t64` 5.11.21+dfsg1-2, library SHA-256
  298eb3cdad9890641386738ed27d1f11790dd0d097e95bfe51d6374795c447f2). STP's MiniSat dependency (stp/minisat
  62a143a12d059b53cf875db79867490d896546a5) is linked but not used under `--cryptominisat`. Binary SHA-256: `stp`
  fc32a941006cd6db...28c7840, `libstp.so.2.3` 4d055c684933d36f...b970973c. Debian 13.7 linux/amd64 container,
  valgrind 3.24.0, binutils 2.44.
- **Call form.** `stp model.cvc --cryptominisat --threads N`, the form of the charged calls, with STP defaults
  otherwise.
- **Model.** The authors' library Peace9911/sha_2_attack at commit 6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32. Its
  step, expansion and value functions (`find_dc/configuration/unit_function_256.py`: `sha_e`, `sha_a`,
  `message_expand`, `sha2_value`) are imported unchanged. Our generator `gen396.py` (Appendix A.9) sets the
  re-parametrisation of Section 7: steps 4..22, words W0..W34, differences only in W4..W8, W12, W13, W20 and W22, zero
  A/E differences at steps 0..3, zero A differences at 15..22 and zero E differences at 19..22. Thresholds are `<=`
  assertions on the sums of the difference bits (tw over W, tE over E, tA over A). From Step 2 on the signed W rows are
  fixed to Fig. 6. The Step-3/4 model uses the signed expansion and the IF/MAJ value model at steps 4..8, as the
  authors' `correct_dc_model_31_256.py` does for its own steps. The models have 41,581-44,400 one-bit variables
  (19.2-20.1 MB of CVC). We did not have #396's model files, so these are our regeneration from its description.
- **Calls.** One per search step, at thresholds at or next to the ledger's, with 1, 2, 4 and 8 threads, and E:

| Call | Model and thresholds | Threads | CVC SHA-256 |
|---|---|---|---|
| A (Step 1) | difference model, tw <= 21 | 1 | dcb972aeb20d81eb... |
| C (Step 2) | nabla W fixed to Fig. 6, tE <= 5 | 2 | be5749564d3c2474... |
| D (Step 3) | signed model, nabla W fixed, tE <= 6, tA <= 18 | 4 | 00d518a6ca9f5e5e... |
| B (Step 4) | signed model, nabla W fixed, tE <= 6, tA <= 21 | 8 | 43786f19e2e0979c... |
| E (Step 2, run to its answer) | as C | 2 | as C |

- **Method.** callgrind with `--dump-instr=yes` and `--dump-before='CMSat::SATSolver::solve*'`. The first dump holds
  everything before the first solve call: parsing, STP's simplifications, bit-blasting and the transfer of the CNF to
  CryptoMiniSat. After that a window was dumped every 60 s (75 s for B), and the call was stopped with SIGTERM after
  240 s of search (300 s for B); valgrind writes the last part on that signal. E ran its front end uninstrumented
  (`--instr-atstart=no`; instrumentation was switched on when CryptoMiniSat started its solver threads), dumped a
  window every 120 s and ran until STP printed its answer (`Valid.`: tE <= 5 is infeasible, as #396 found). Every
  executed address in every object (`stp`, `libstp`, `libcryptominisat5`, libc, libstdc++, libm, libgcc_s, ld.so, Boost) was matched to its
  instruction in `objdump -d -M intel` of that object and priced by the Section 15.1 table (`x86ops.py`, unchanged).
  Multiply, divide and floating-point forms are priced per form by Section 15.7: the exact cost of a counted
  emulation with the v5 primitives, plus operand transfer. GNU objdump prints string instructions without a size
  suffix and repeats some prefixes (`data16 cs nop`); we normalise both before the lookup, so a `rep movsb`
  iteration costs 6 and a padding `nop` 1. No executed form was left unpriced (0.00% unrecognised). The summed
  per-instruction counts equal callgrind's own totals for every dump.
- **PLT stubs and unmapped code.** callgrind's default `--skip-plt=yes` counts each PLT stub instruction at the call
  instruction that entered it, so stubs are priced as that call (3 or more operations), at least their own price
  (an indirect jump through memory, 3). 0.01-0.47% of the instructions ran outside any file-backed object and could
  not be disassembled; each is charged 8.

| Call | Front end: instructions, m | Search: instructions, m | Search windows: m | End part: instructions, m | Whole call: m |
|---|---|---|---|---|---|
| A | 1.833e11, 4.079 | 4.841e10, 2.056 | 1.91, 2.44, 2.18 | 13.01e9, 1.826 | 3.656 |
| C | 1.611e11, 4.084 | 4.668e10, 2.150 | 1.90, 1.90, 2.07, 3.25 | 0.35e9, 2.749 | 3.649 |
| E | not instrumented | 5.519e10, 2.145 | 1.85, 2.59 | 7.84e9, 1.961 | - |
| D | 1.745e11, 4.074 | 5.473e10, 1.859 | 1.80, 1.86, 1.89, 1.82 | 3.32e9, 2.155 | 3.545 |
| B | 1.745e11, 4.074 | 7.431e10, 1.828 | 1.82, 1.78, 1.85, 1.82 | 11.91e9, 1.857 | 3.403 |

The search columns cover everything after the first solve call. Windows are the parts between
periodic dumps; the end part runs from the last periodic dump to the exit. Heavy shares: front end 0.52%,
search 0.18-0.27%.

- **Front end against search.** The front end is the same code for all four models and costs 4.074-4.084 operations per
  instruction, with a heavy share of 0.52%: mostly 64-bit `div` in hash-table indexing (576 + 2 operations each,
  Section 15.7), which lifts libstp and libstdc++ to about 5 operations per instruction. The search runs in
  libcryptominisat5 (89-96% of its instructions) and libc. It costs 1.828-2.150 per instruction, with a heavy share of
  0.18-0.27%, mostly `comisd` (22 operations each) and multiplies. Its ordinary mean, 1.689-1.928, is close to the
  1.880-1.956 of our binding runs (Section 15.5).
- **The costly search phase is transient.** Some search windows are dominated by `rep movsb` copying in libc
  memmove (up to 25% of the instructions, 6 operations per iteration), which lifts them to at most 3.25. C was
  stopped inside such a phase, so its last minute is the costliest window of all calls. Run E repeated C's model to
  completion: its 2-minute windows were 1.85, 2.59, 1.96 (the last one ends with the solver's answer), and its whole search
  averaged 2.145. The phase passes and the search returns to its usual mix.
- **How E is charged (absolute, no ratio).** We split every call into one-off parts, which a charged call also runs
  once (the front end, and the end part from the last periodic dump to the exit), and search windows (the parts
  between periodic dumps, 60-120 s each). For the measured 59-call run we charge

  **operations <= 59 * X_once * m_once + I_max * m_search = 3.947952e15 (m_eff = 3.2864 per instruction)**,

  - X_once = 183,303,636,869 + 13,012,930,660 = 196,316,567,529 instructions: the largest front end plus the largest end part of
    any call, charged once for each of the 59 calls;
  - m_once = 4.084: the costliest one-off part of any call (front ends cost 4.074-4.084, end parts up to 2.749);
  - I_max = S * R_cal * 593,858 = 1.2013e15 instructions: all instructions of the 59 calls under the spread S,
    including those of the one-off parts, which are therefore charged twice;
  - m_search = 3.247: the costliest search window of any call, so every charged search instruction is priced as in our
    costliest minute, although whole searches averaged 1.828-2.150 and the complete search of E 2.145.

  This bound needs only the upper bound I_max on the total and the absolute bound on one-off instructions; no share
  of one-off work is assumed. E multiplies it by the rediscovery factor 32, calls included (Section 7). Our profiled
  calls spent 70-79% of their instructions in the front end only because we stopped each search after a few
  minutes; their whole-call means (3.403-3.656) describe those truncated calls. #396's calibrated call (4.42e10
  instructions in all) suggests its front ends were smaller than ours.
- **Agreement with the credited calibration.** The whole-call heavy share of our calls, 0.43-0.46%, is close to the
  0.416% that #296/#396 measured on the calibrated call. The credited 7.24% PLT share needs no separate term here,
  because the stubs are counted and priced at their call sites.
- **What it does not cover.**
  - The binaries are ours: Debian's CryptoMiniSat build and our STP build. #396's builds and compiler flags are not
    published. The ordinary means of the Debian library in the search (1.689-1.928) and of the manylinux library of
    Section 15.5 (1.880-1.956) differ by less than 15%.
  - Our searches lasted 4-6 minutes under callgrind, about 20-40 s of native search on our machine, and only E ran
    to its answer. The charged calls searched for hours. The price assumes that no long stretch of their search was
    costlier per instruction than our costliest minute (3.247); our search windows ranged from 1.78 to 3.25.
  - The models are our regeneration from #396's description, not its files. #396's calibrated Step-1 call (1 thread,
    `--max-num-confl 20000`) retired 4.42e10 instructions in all, fewer than our front end alone (1.61-1.83e11), so
    its models were smaller than ours or were built differently. A smaller front end only lowers a call's front-end
    share.
  - The instruction rate is not re-measured. R_cal and S are unchanged (Sections 7 and 15.2).
- **Reproduction.** Appendix A.7-A.16 lists the scripts with their SHA-256 hashes: `setup_stp.sh` and
  `build_stp.sh` install the toolchain and build STP, `gen396.py` writes the models, `cgrun.sh` and `windows.sh` run
  the profiles (`ffrun.sh` ran E), `mkdis.sh` disassembles every object, `heavyemu.py` checks the heavy-form
  emulations and writes their tariffs, `stpdyn.py` prices each call with them (`TARIFFS=tariffs.json`) and
  `stpsum.py` forms the absolute charge.

### 15.7 Heavy forms: emulation with the v5 primitives (new in this package)

The v5 primitive list has no multiply, divide or floating-point operation. Our earlier packages charged such
instructions a flat 400 without a reduction. This section replaces that tariff by an
explicit simulation: each heavy form the profiled calls executed is emulated with the v5 primitives only, and its
price is the exact cost of that emulation.

- **Primitives counted** (`heavyemu.py`, Appendix A.16), 1 each: addition or subtraction, AND/OR/XOR, shift,
  comparison, conditional branch, load, store. Every comparison feeds a branch, so it costs 2. A table access costs
  an address addition and a load or store. Constants are immediates. Loops have fixed trip counts.
- **Exact worst case by construction.** Every data-dependent choice goes through `sel()`: both arms are evaluated on
  scratch counters and the costlier arm is charged, whichever is taken. Each emulation therefore costs the same on
  every input, and that cost is its exact worst case over all inputs, not a sample maximum. The runs confirm this:
  every form had a single cost over all tested inputs (`roundsd` has one cost per immediate rounding mode).
- **Algorithms.**
  - Multiply: radix-16 shift-and-add. A table of the 16 multiples of a (15 adds or shifts, 16 stores), then per
    4-bit digit of b one shift, one AND, one table load and one add. Signed high halves are corrected by subtracting
    the other operand when an operand is negative; OF/CF compare the high half with the sign extension of the low.
  - Divide: restoring division, one quotient bit per step (shift, bit insert, compare and branch, conditional
    subtract and quotient bit), w steps for a w-bit quotient; signed forms divide magnitudes and fix the signs.
  - Floating point (IEEE binary64 and binary32, round to nearest even, subnormals, signed zeros, infinities and
    NaNs with x86 propagation and the default NaN): unpack and classify; exact integer significand arithmetic (sums
    after exact alignment, or the larger operand plus a sticky bit when the exponents differ by more than the
    precision plus guard bits; radix-16 products; restoring-division quotients with a sticky bit); then one
    normalise-and-round routine (binary search for the leading bit, sticky shift, subnormal shift, round to nearest
    even, overflow to infinity, pack). Comparisons work on the bit patterns. Conversions reuse the same routine.
- **Validation.** Each emulation was run on 30,000 inputs: uniform bit patterns, all special values, subnormals,
  powers of two, operands with long runs of zero low bits (halfway cases), and near-equal pairs. Results were compared
  with numpy binary64/binary32 arithmetic (and `np.rint`, `np.floor`, `np.ceil`, `np.trunc` for `roundsd`), exact
  rational arithmetic for the fused multiply-add, and Python integers for the integer forms. **0 mismatches in every
  form.**

| x86 forms executed | Emulation | Cost (exact) | Price per instruction |
|---|---|---|---|
| `div r64`, `div QWORD PTR [m]` | restoring division, 64 steps | 576 | 578 |
| `div r32` | restoring division, 32 steps | 288 | 290 |
| `idiv r32` | magnitudes, 32 steps, sign fix | 306 | 308 |
| `idiv r64` | magnitudes, 64 steps, sign fix | 594 | 596 |
| `imul r64, r/m64(, imm)` | radix-16 product, low half, OF/CF | 155 | 157 |
| `imul r32, r/m32(, imm)` | radix-16 product, low half, OF/CF | 107 | 109 |
| `imul r/m64` (one operand) | radix-16 product, signed high half | 155 | 157 |
| `mul r/m64` | radix-16 product, 128 bits | 146 | 148 |
| `pmuludq xmm, xmm` | two 32 x 32 radix-16 products | 196 | 198 |
| `comisd`, `ucomisd`, `comiss`, `cmpnlesd`, `cmpnltsd` | bit-pattern ordering | 20 | 22 |
| `maxsd`, `maxss`, `minsd` | bit-pattern ordering, select | 20 | 22 |
| `cvttsd2si r64/r32` | unpack, shift, sign | 57 | 59 |
| `cvtsi2sd`, `vcvtsi2sd` (r64, r32, m) | magnitude, round | 73 | 75 |
| `cvtss2sd`, `cvtsd2ss` | unpack, round to the other format | 83 | 85 |
| `addsd`, `subsd`, `vaddsd`, `vsubsd` | aligned exact sum, round | 131 (addsd 130) | 133 |
| `addpd` | two lanes of the sum | 268 | 270 |
| `mulsd`, `vmulsd`, `mulss` | radix-16 significand product, round | 239 (mulss 191) | 241 |
| `divsd` | restoring significand division, 57 steps, round | 527 | 529 |
| `vfmadd132/213/231sd`, `vfmsub132sd` | exact product, aligned sum, one rounding | 275 | 277 |
| `roundsd`, `vroundsd` (modes 0-3) | fraction mask, mode increment | 102 | 104 |

The price adds 2 operations for moving the operands and results; a memory operand adds its address computation and
load as in the Section 15.1 table (1 + 1 per added address term). Forms not in the table do not occur in our
profiles. The heavy share of every call is 0.18-0.52% of its instructions, so these
prices move m by at most about 1. With every tariff doubled, the total becomes 46.471 (Section 13).

## 16. Changes after the review of 21b81d2d

The review of our v5 package (21b81d2d, not evaluable) raised four points. Each is fixed here.
1. **Heavy-instruction tariff** (F-heavy-op-tariff, `implicit-heavy-instruction-pricing`). The flat 400 is replaced
   by exact emulations with the v5 primitives, one per executed form, validated against numpy and exact references
   (Section 15.7). 64-bit divide costs 576 (above the old 400) and FP compare 20 (below it). A doubled table changes
   the total to 46.471.
2. **Selected-tuple conditioning** (F-cryptanalysis-001). Step 3 runs on every valid tuple, and Section 9 now bounds
   Pr[Y >= 1] for the total count Y over all valid tuples, by linearity and a second moment. (v7 replaces the
   second-order premise of v6 by an explicit allowance; Section 17.)
3. **Credited-measurement binding** (F-EXP-001). Declared as heuristic `credited-measurement-binding`, with every
   credited report cited by pull request, head commit, submission, files and counts, and our exact checks per
   report (Section 6.1).
4. **One-off share** (F-EXP-003, F-oneoff-share-denominator, F-EVAL-CPU-ONCE-SHARE). The ratio bound is gone. The
   one-off work is charged absolutely, 59 X_once m_once operations, on top of every instruction at m_search
   (Section 7).

## 17. Changes after the reviews of 4e4e600f (v6) and d3cd2213 (v7)

v6 assumed that a valid tuple's Step-3 moments are unchanged when another record of the same trial is valid; v7
replaced that by an unmeasured allowance kappa = 5. Both were rated unsupported for want of a conditioned
experiment (F-SUCCESS-PAIR-CONDITIONING, F-CRYPT-002, F-EXP-004 and the four lanes of d3cd2213). This version proves
what can be proved and measures the rest (Section 9.1):
- **Proof.** Validity reads CV1 only through CV1[0..3]; CV1[4..7] map one to one onto W0..W3 and then onto W16..W19,
  so stages 16..19 of every tuple are exactly independent of every Step-2 event of the trial, under the uniform-CV1
  premise already declared. From step 20 on a tuple enters only through c20 and c22.
- **Measurement on that channel.** On the real two-sided second block (the real P4 list, rebuilt from the advice), the
  Step-3 pass rate over tuple constants drawn from a tuple's validity set is flat: max/mean 1.095
  (upper 1.154) over 64 synthetic tuples, and at most 1.138 within each of
  eight real records.
- **Direct conditioned experiment.** We rebuilt TAB2's P1-P3 exactly (10,240 combinations, 155,008 pairs,
  1,396,774,912 records, the published counts) and kept a 1/256 key slice (5,618,824 records,
  1,116,588 key classes with two or more records). In trials where two records of a class are both
  valid (19317 pair events), the tuple's Step-3 pass rate over that of single events of the same records
  is 0.998 +- 0.003.
- **Charge.** kappa = 1.5, above every upper confidence bound; T = 2^44.8309 keeps the success bound at 0.390108. The
  time bound is 2^46.4042 (claim 46.41).

## Appendix A. Profile scripts (participant tools)

- `setup.sh`: SHA-256 2e814916da4f74b88bbe53fb70fc38da26f58586c137fcc60a4c677256032d25
- `runs.sh`: SHA-256 2dbc751d1bdad0fc478d5e89081f05d7ca6926eda0e75fdbea593df291b4c289
- `lbench.py`: SHA-256 435ef2774d12f639df0c82d946c680be3993178b57ab3ee5d3dc8ddd91b7eac6
- `x86ops.py`: SHA-256 220b1ab3aad0e96fc0c2d21a7977911de832df8aab12017cdfa971feae3fe190
- `dynparse.py`: SHA-256 e67a3fad41a6e530619affacbca11ef71499eb2094b3b810624c2cda419c0e60
- `dynall.py`: SHA-256 29747d0c46ad6e420427e4d39bb40fd35120dfb324b2b363f20af45ce982f818

Scripts of Sections 15.6-15.7 (they import `x86ops.py` and `dynparse.py` above, unchanged; `stpdyn.py` reads the
tariffs that `heavyemu.py` writes):

- `setup_stp.sh`: SHA-256 d78ad64d88fddf585d7fa513d0245c6049a23f381f01f34e2ebac6e139be84a0
- `build_stp.sh`: SHA-256 97912646526b26eeec37ecff07cfab786c6c1b234316b3499ef578d498bdfa6d
- `gen396.py`: SHA-256 d8f6d3f3b86800b39d270ee5f891fb3f3390142d4033091275bbe8f09dc23526
- `cgrun.sh`: SHA-256 87e122d5937fd47e08f532133860b71f3ff839c456d3712a1faae819be2764cf
- `windows.sh`: SHA-256 9f5fb74d935ebce2d90e62c30f110fcad9b7feaba1acb5d9a85c15a05980b259
- `ffrun.sh`: SHA-256 45410d79921ddc1bac89e1a62f3301024fb8f33c6133dd7eb6ea8b459674b063
- `mkdis.sh`: SHA-256 007fc983efd700078f45aeb5da3028dc532aa903841630669f32219607ff99b6
- `stpdyn.py`: SHA-256 e36d96be24f7b86f790eac674f37025e0c03baccd050f0edd4678940188f7b8b
- `stpsum.py`: SHA-256 6bc4e5c0245cd7d325aafcfd50a9b3a49250babeae302580f713af64216c7383
- `heavyemu.py`: SHA-256 a689e88939729befef2aaa56754748f8b3ed3ef218fe8f39a0dd731a63e46d2c

Scripts of Section 9.1 (v8; `secondblock.py` reads `fig6_rows_296.txt`, the Section 2 rows, and `step3ref.py`
reuses `check_route.py`):

- `secondblock.py`: SHA-256 5b0d1aefa2780b18f1b5b5e9ec3a260d35aefe9cc2a273e0743f00f8fefbffe1
- `step3ref.py`: SHA-256 21f5147a06f3e327310d4c050b2860e87133f363bee8f772ca99a75c029ab5e4
- `check_route.py`: SHA-256 fa61c384ba96ec32547c5233a7525113a8d901d7869d3b9625d37f8c98155513
- `mkparams.py`: SHA-256 0cbd2c4843d8694e90533b2b091d85bffff3f6031d98d8b136d36a67d2e4062a
- `gen_cvec.py`: SHA-256 668003ef453e754480d1bf5f5fe9907727327908e9111ff8ac26d1e68d994f87
- `condexp.c`: SHA-256 8ea0d2c6f2faf9f33984df64fcc8e70c078e9970a72d49b7d78c54234e394065
- `analyse.py`: SHA-256 646131303325bece04d31bbef738a682d7b1297e92ea1d5412b26d10b4b92e20
- `table.py`: SHA-256 17faeb7737d929a54bfcf06df06935eb3c5913daaf42d46f3d34322e6f0e6a33
- `pairexp.py`: SHA-256 9e50bb32c4fa4521cf77f478325ce634b0f451de4a413f27d747545764cc28da
- `flatset.py`: SHA-256 03c82d1ef973fa89bfaa9a8f67b07d3d4b4a4142306ca82cc89ac278056af41a
- `analyse2.py`: SHA-256 dd4b3841ed0b89bf18fbbd99c42d3e2aaf3e7264264525a016f14b1e8b454b85
- `runs_v8.sh`: SHA-256 7e0271e05597a84b33e459199191eb0a90b1df195f73518ac9a6b6129191fd9e

### A.4 `x86ops.py`

```python
"""Static primitive-operation cost of x86-64 instructions (collision-frontier-v5 primitive list), per function."""
import re, sys, collections, json
MEM = re.compile(r'\[([^\]]*)\]')
R8 = set('al bl cl dl ah bh ch dh sil dil bpl spl'.split()) | {f'r{i}b' for i in range(8, 16)}
R16 = set('ax bx cx dx si di bp sp'.split()) | {f'r{i}w' for i in range(8, 16)}
R32 = set('eax ebx ecx edx esi edi ebp esp'.split()) | {f'r{i}d' for i in range(8, 16)}
HEAVY = re.compile(r'^(i?mul|i?div|mulx)$|^(v?)(add|sub|mul|div|sqrt|max|min|cvt|ucomi|comi|round|fmadd|rcp|rsqrt)[a-z0-9]*(ss|sd|ps|pd|si2s[sd]|s[sd]2si|tts[sd]2si|si2sd|si2ss|dq2pd|pd2ps|ps2pd)?$|^f[a-z]+$')
FPONLY = re.compile(r'^v?(add|sub|mul|div|sqrt|max|min|ucomi|comi|round|rcp|rsqrt)(ss|sd|ps|pd)$|^v?cvt|^f[a-z]+$')
SIGNED = {'jl', 'jle', 'jg', 'jge', 'js', 'jns', 'jo', 'jno', 'jnge', 'jnl', 'jng', 'jnle'}
def addr(op):
    m = MEM.search(op)
    if not m: return 0
    t = m.group(1)
    if 'rip' in t: return 1
    terms = [x for x in re.split(r'[+-]', t.replace(' ', '')) if x]
    c = len(terms) - 1 + (1 if re.search(r'\*[248]', t) else 0)
    if re.search(r'\b[fg]s:', op): c += 1
    return c
def width(op):
    op = op.strip()
    if op.startswith(('byte', 'word', 'dword', 'qword', 'xmmword', 'ymmword')): return op.split()[0]
    if op in R8: return 'r8'
    if op in R16: return 'r16'
    if op in R32: return 'r32'
    return 'r64'
def cost(mn, ops):
    """Return (ops, class) where class is 'heavy' for multiply/divide/FP, else 'ordinary'."""
    mn = mn.split()[-1] if mn.startswith(('lock', 'rep', 'notrack', 'bnd')) and ' ' in mn else mn
    if HEAVY.match(mn) and (FPONLY.match(mn) or mn in ('mul', 'imul', 'div', 'idiv', 'mulx')):
        return 400, 'heavy'
    a = sum(addr(o) for o in ops)
    dst = ops[0] if ops else ''
    dmem = '[' in dst
    smem = any('[' in o for o in ops[1:])
    w = width(dst) if ops else 'r64'
    merge = 2 if w in ('r8', 'r16') and not dmem else 0
    mask = 1 if w == 'r32' and not dmem else 0
    if mn in ('nop', 'endbr64', 'int3', 'ud2', 'hlt', 'pause', 'lfence', 'mfence', 'sfence', 'prefetcht0', 'prefetcht1', 'prefetcht2', 'prefetchnta', 'prefetchw'):
        return 1, 'ordinary'
    if mn in ('mov', 'movabs'):
        return 1 + a + merge, 'ordinary'
    if mn in ('movzx', 'movsx', 'movsxd'):
        return 1 + a + 1 + (2 if mn != 'movzx' else 0), 'ordinary'
    if mn in ('add', 'sub', 'and', 'or', 'xor', 'cmp', 'test', 'adc', 'sbb'):
        c = 1 + (2 if mn in ('adc', 'sbb') else 0)
        if smem: c += 1
        if dmem and mn not in ('cmp', 'test'): c += 2
        elif dmem: c += 1
        if mn in ('add', 'sub', 'adc', 'sbb'): c += mask
        if mn not in ('cmp', 'test'): c += merge
        return c + a, 'ordinary'
    if mn in ('inc', 'dec', 'neg', 'not'):
        return 1 + (2 if dmem else 0) + mask + merge + a, 'ordinary'
    if mn in ('shl', 'sal', 'shr'):
        return 1 + (2 if dmem else 0) + (mask if mn != 'shr' else 0) + merge + a, 'ordinary'
    if mn == 'sar':
        return 3 + (2 if dmem else 0) + mask + merge + a, 'ordinary'
    if mn in ('rol', 'ror', 'shld', 'shrd', 'rcl', 'rcr'):
        return 4 + (2 if dmem else 0) + merge + a, 'ordinary'
    if mn == 'lea':
        m = MEM.search(ops[1]).group(1) if len(ops) > 1 and MEM.search(ops[1]) else ''
        return max(1, a) + mask, 'ordinary'
    if mn == 'jmp':
        return (2 + a) if smem or dmem else 1, 'ordinary'
    if mn.startswith('j'):
        return 3 if mn in SIGNED else 2, 'ordinary'
    if mn.startswith('cmov'):
        return 3 + (1 if smem else 0) + a + mask, 'ordinary'
    if mn.startswith('set'):
        return 2 + (1 if dmem else merge) + a, 'ordinary'
    if mn == 'call':
        return 3 + ((1 + a) if dmem else 0), 'ordinary'
    if mn == 'ret':
        return 3, 'ordinary'
    if mn == 'push':
        return 2 + ((1 + a) if dmem else 0), 'ordinary'
    if mn == 'pop':
        return 2, 'ordinary'
    if mn == 'leave':
        return 3, 'ordinary'
    if mn in ('cdq', 'cqo', 'cdqe', 'cwde', 'cbw', 'cwd'):
        return 3, 'ordinary'
    if mn in ('xchg',):
        return (3 if not dmem else 4) + a, 'ordinary'
    if mn in ('cmpxchg', 'xadd', 'cmpxchg8b', 'cmpxchg16b'):
        return 6 + a, 'ordinary'
    if mn == 'bt':
        return 2 + (1 if dmem else 0) + a, 'ordinary'
    if mn in ('bts', 'btr', 'btc'):
        return 4 + (2 if dmem else 0) + a, 'ordinary'
    if mn in ('bsf', 'bsr', 'tzcnt', 'lzcnt', 'popcnt', 'bswap'):
        return 32 + a, 'ordinary'
    if mn in ('stosb', 'stosw', 'stosd', 'stosq', 'movsb', 'movsw', 'movsq', 'scasb', 'cmpsb', 'lodsb') or (mn == 'movsd' and not ops) or (mn == 'movsd' and all('ptr [r' in o and ('rsi' in o or 'rdi' in o) and 'xmm' not in o for o in ops)):
        return 6, 'ordinary'   # string instruction, charged per iteration
    if re.match(r'^v?(movd|movq|movdqa|movdqu|movaps|movups|movapd|movupd|movss|movsd|movhps|movlps|movhpd|movlpd|movntdq|movnti|lddqu)$', mn):
        return 1 + a, 'ordinary'
    if re.match(r'^v?(pxor|por|pand|pandn|xorps|xorpd|andps|andpd|orps|orpd|andnps|andnpd)$', mn):
        return 1 + (1 if smem else 0) + a, 'ordinary'
    if re.match(r'^v?(padd|psub|pcmp|pmin|pmax|psll|psrl|psra|pavg|pabs)', mn):
        return 8 + (1 if smem else 0) + a, 'ordinary'
    if re.match(r'^v?(pshuf|punpck|pinsr|pextr|pmovmsk|movmsk|palign|shufp|unpck|pmovzx|pmovsx|pblend|blend|insertps|extractps|vperm|vbroadcast|vpbroadcast|pack|vinsert|vextract|movhlps|movlhps|movddup|movshdup|movsldup|pslldq|psrldq|ptest|vzeroupper)', mn):
        return 16 + (1 if smem else 0) + a, 'ordinary'
    return None, 'unknown'

def parse(path):
    funcs = collections.OrderedDict(); cur = None
    for line in open(path, errors='replace'):
        if line.rstrip().endswith('>:'):
            cur = line.split('<', 1)[1].rsplit('>', 1)[0]; funcs[cur] = []; continue
        m = re.match(r'^\s+[0-9a-f]+:\s+(.*)$', line.rstrip())
        if not m or cur is None: continue
        body = m.group(1).split('<')[0].strip()
        if not body or body.startswith('(bad)'): continue
        parts = body.split('\t')
        mn = parts[0].strip(); ops = [o.strip() for o in parts[1].split(',')] if len(parts) > 1 else []
        if mn in ('lock', 'rep', 'repne', 'notrack', 'bnd', 'data16', 'rex64', 'cs') and len(parts) > 1 and parts[1].strip():
            sub = parts[1].strip().split(None, 1); mn = sub[0]; ops = [o.strip() for o in sub[1].split(',')] if len(sub) > 1 else []
            if parts[0].strip() == 'rep' or parts[0].strip() == 'repne': mn = mn  # rep handled as per-iteration cost below
        funcs[cur].append((mn, ops))
    return funcs

def summarize(name, insns):
    tot = n = heavy = big = unk = 0; dist = collections.Counter(); unkn = collections.Counter()
    for mn, ops in insns:
        c, cls = cost(mn, ops)
        if c is None:
            unk += 1; unkn[mn] += 1; c = 8
        n += 1
        if cls == 'heavy': heavy += 1; continue
        tot += c; dist[min(c, 10)] += 1
        if c > 5: big += 1
    ordn = n - heavy
    return dict(name=name, insns=n, heavy=heavy, ordinary=ordn, mean_ordinary=round(tot / ordn, 3) if ordn else None,
                frac_ordinary_over5=round(big / ordn, 4) if ordn else None, unknown=unk,
                dist={k: dist[k] for k in sorted(dist)}, unknown_top=unkn.most_common(8))

if __name__ == '__main__':
    funcs = parse(sys.argv[1])
    pat = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
    hot = [(k, v) for k, v in funcs.items() if pat and pat.search(k)]
    for k, v in hot: print(json.dumps(summarize(k[:90], v)))
    print(json.dumps(summarize('HOT-SET', [i for _, v in hot for i in v])))
    print(json.dumps(summarize('WHOLE-LIBRARY', [i for v in funcs.values() for i in v])))
```

### A.5 `dynparse.py`

```python
"""Dynamic per-form cost: callgrind per-instruction Ir (--dump-instr=yes) x static per-form price (x86ops.cost)."""
import re, sys, collections, json
from x86ops import cost

def disasm(path):
    ins = {}
    for line in open(path, errors='replace'):
        m = re.match(r'^\s+([0-9a-f]+):\s+(.*)$', line.rstrip())
        if not m: continue
        body = m.group(2).split('<')[0].strip()
        if not body or body.startswith('(bad)'): continue
        parts = body.split(None, 1)
        mn = parts[0].strip(); ops = [o.strip() for o in parts[1].split(',')] if len(parts) > 1 else []
        if mn in ('lock', 'rep', 'repz', 'repe', 'repne', 'repnz', 'notrack', 'bnd', 'data16', 'rex64', 'cs', 'ds') and len(parts) > 1 and parts[1].strip():
            sub = parts[1].strip().split(None, 1); mn = sub[0]; ops = [o.strip() for o in sub[1].split(',')] if len(sub) > 1 else []
        ins[int(m.group(1), 16)] = (mn, ops)
    return ins

def callgrind(path, obj_pat):
    ir = collections.Counter(); ob = None; fl = None; skip = False; objs = collections.Counter()
    for line in open(path, errors='replace'):
        if line.startswith('ob='): ob = line[3:].strip(); continue
        if line.startswith(('fl=', 'fi=', 'fe=', 'fn=', 'cfn=', 'cfi=', 'cfl=', 'cob=')): continue
        if line.startswith('calls='): skip = True; continue
        if line.startswith('0x') or line[:1].isdigit():
            if skip: skip = False; continue
            p = line.split()
            if len(p) < 3: continue
            a = int(p[0], 16); n = int(p[2]) if len(p) > 2 else 0
            objs[ob] += n
            if ob and obj_pat in ob: ir[a] += n
    return ir, objs

if __name__ == '__main__':
    dis = disasm(sys.argv[1])
    out = {}
    for f in sys.argv[2:]:
        ir, objs = callgrind(f, 'pycryptosat')
        tot_ir = sum(ir.values()); ops = 0; heavy = 0; miss = 0; unk = collections.Counter(); bycost = collections.Counter(); mn_ir = collections.Counter()
        for a, n in ir.items():
            if a not in dis: miss += n; ops += 8 * n; continue
            mn, o = dis[a]
            c, cls = cost(mn, o)
            if c is None: unk[mn] += n; c = 8
            if cls == 'heavy': heavy += n
            ops += c * n; bycost[min(c, 10) if c < 400 else 400] += n; mn_ir[mn] += n
        allobj = sum(objs.values())
        out[f] = dict(total_ir_all_objects=allobj, solver_obj_ir=tot_ir, solver_share=round(tot_ir / allobj, 4),
                      ops=ops, m_dynamic=round(ops / tot_ir, 4), heavy_share=round(heavy / tot_ir, 6),
                      m_ordinary=round((ops - 400 * heavy) / (tot_ir - heavy), 4),
                      addr_not_in_disasm_share=round(miss / tot_ir, 6), unknown_share=round(sum(unk.values()) / tot_ir, 6),
                      unknown_top=unk.most_common(6), cost_hist={k: round(v / tot_ir, 4) for k, v in sorted(bycost.items())},
                      top_mnemonics=[(k, round(v / tot_ir, 4)) for k, v in mn_ir.most_common(12)],
                      objects_top=[(k.split('/')[-1] if k else k, v) for k, v in objs.most_common(5)])
    print(json.dumps(out, indent=1))
```

### A.6 `dynall.py`

```python
"""Dynamic per-form cost over every object executed inside CMSat::SATSolver::solve (callgrind --toggle-collect)."""
import sys, json, subprocess, collections, os
from x86ops import cost
from dynparse import disasm

def callgrind_all(path):
    ir = collections.defaultdict(collections.Counter); ob = None; skip = False
    for line in open(path, errors='replace'):
        if line.startswith('ob='): ob = line[3:].strip(); continue
        if line.startswith('calls='): skip = True; continue
        if line.startswith('0x'):
            if skip: skip = False; continue
            p = line.split()
            if len(p) >= 3: ir[ob][int(p[0], 16)] += int(p[2])
    return ir

DIS = {}
def dis_for(ob):
    if ob not in DIS:
        out = '/w/dis/' + ob.strip('/').replace('/', '_') + '.dis'
        os.makedirs('/w/dis', exist_ok=True)
        if not os.path.exists(out):
            subprocess.run(['sh', '-c', f'objdump -d -M intel --no-show-raw-insn "{ob}" > "{out}"'], check=False)
        DIS[ob] = disasm(out)
    return DIS[ob]

res = {}
for f in sys.argv[1:]:
    ir = callgrind_all(f)
    T = O = H = M = 0; per = {}; mn_ir = collections.Counter(); hist = collections.Counter()
    for ob, cnt in ir.items():
        d = dis_for(ob); t = o = h = miss = 0
        for a, n in cnt.items():
            if a in d:
                mn, ops = d[a]; c, cls = cost(mn, ops)
                if c is None: c = 8
                if cls == 'heavy': h += n
                mn_ir[mn] += n
            else:
                c = 8; miss += n
            t += n; o += c * n; hist[c if c < 400 else 400] += n
        per[ob.split('/')[-1]] = dict(ir=t, m=round(o / t, 4) if t else None, heavy=h, miss=miss)
        T += t; O += o; H += h; M += miss
    res[f] = dict(solve_ir=T, m_dynamic=round(O / T, 4), heavy_share=round(H / T, 6), m_ordinary=round((O - 400 * H) / (T - H), 4),
                  unmapped_share=round(M / T, 6), per_object=per,
                  top_mnemonics=[(k, round(v / T, 4)) for k, v in mn_ir.most_common(10)],
                  cost_hist={k: round(v / T, 5) for k, v in sorted(hist.items())})
print(json.dumps(res, indent=1))
```

### A.2 `runs.sh`

```sh
cd /w
cg() { n=$1; shift; valgrind --tool=callgrind --dump-instr=yes --compress-strings=no --compress-pos=no --toggle-collect='CMSat::SATSolver::solve*' --callgrind-out-file=/w/cg.$n.out python lbench.py "$@" > /w/run.$n.json 2> /w/run.$n.err; }
cg pair20 --kind pair --steps 20 --k 256 --confl 60000 --seed 1 &
cg pre24 --kind pre --steps 24 --k 96 --confl 60000 --seed 1 &
cg pairwt --kind pair --steps 20 --k 256 --wt 40 --confl 60000 --seed 2 &
cg pair17 --kind pair --steps 17 --k 160 --confl 60000 --seed 1 &
wait
echo done > /w/runs.done
```

### A.1 `setup.sh`

```sh
set -e
apt-get update -qq >/dev/null && apt-get install -y -qq valgrind binutils >/dev/null
pip install -q pycryptosat==5.11.21
python -c "import pycryptosat,glob,os;d=os.path.dirname(pycryptosat.__file__);print(d);print(glob.glob(d+'/../pycryptosat*')+glob.glob(d+'/../pycryptosat.libs/*'))"
valgrind --version
```

### A.7 `setup_stp.sh`

```sh
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null
apt-get install -y -qq --no-install-recommends ca-certificates git cmake make g++ bison flex libboost-program-options-dev zlib1g-dev libgmp-dev pkg-config libcryptominisat5-dev cryptominisat valgrind binutils python3 time >/dev/null
dpkg -l | grep -E 'cryptominisat|valgrind|g\+\+|boost-program' | awk '{print $2, $3}'
cd /opt
git clone -q https://github.com/stp/minisat.git && cd minisat && git log -1 --format='minisat %H %cd' && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. >/dev/null && make -j8 >/dev/null && make install >/dev/null && cd /opt
git clone -q https://github.com/stp/stp.git && cd stp && git checkout -q 2.3.4 && git log -1 --format='stp %H %cd'
```

### A.8 `build_stp.sh`

```sh
set -e
cd /opt/stp && mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_PYTHON_INTERFACE=OFF -DENABLE_TESTING=OFF .. 2>&1 | grep -i -E 'cryptominisat|minisat|error|warn|build type|flags' | head -30
make -j8 2>&1 | tail -5
ls -la stp* lib* 2>/dev/null | head
./stp --version | head -5
ldd ./stp
```

### A.9 `gen396.py`

```python
"""CVC model of the re-parametrised 31-step SHA-256 search (steps 4..22, W0..W34) from the authors' unit functions.

The step, expansion and value functions are imported unchanged from Peace9911/sha_2_attack@6a9f35f
(find_dc/configuration/unit_function_256.py). Only the parameters, the boundary conditions and the
threshold assertions are ours, following the re-parametrisation described by hash-smash #396.
"""
import argparse, os, sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--signed', action='store_true', help='signed-difference expansion (op6=1) and IF/MAJ value model at steps 4..8')
ap.add_argument('--tw', type=int, help='assert sum of W differences <= tw')
ap.add_argument('--tw-eq', type=int, help='assert sum of W differences == tw')
ap.add_argument('--tE', type=int, help='assert sum of E differences over steps 4..22 <= tE')
ap.add_argument('--tA', type=int, help='assert sum of A differences over steps 4..22 <= tA')
ap.add_argument('--fixw', action='store_true', help='fix the signed W rows to Fig. 6 (Step 2 onwards)')
ap.add_argument('--out', required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.join(a.repo, 'find_dc', 'configuration'))
from unit_function_256 import sha_e, sha_a, message_expand, sha2_value  # noqa: E402

START, END, MB, BS = 4, 23, 35, 32
DIFF = [4, 5, 6, 7, 8, 12, 13, 20, 22]
WROWS = {4: '==n=============================', 5: '=====u===u==========n===========',
         6: '==n=============================', 7: '=======n=======u===u====u=1=u=u=',
         8: '============u=======uu==========', 12: '=====n===n==========u===========',
         13: '==u=============================', 20: '=====0=nn=====0=u=1=============',
         22: '==n============================='}
op2 = [0] * 15 + [1] * (MB - 15)
op5 = [0] * 11 + [1] * (MB - 11)
decl, cons = [], []
seen = set()

def var(s):
    if s not in seen:
        seen.add(s); decl.append(s + ': BITVECTOR(1);\n')
    return s

def add(vs, cs):
    cons.append(''.join(cs))
    for v in vs:
        n = v.split(':')[0]
        if n not in seen:
            seen.add(n); decl.append(v)

def total(name, rows):
    bits = ['0bin000000000@%s' % var('%s_%d_%d' % (name, i, j)) for i in rows for j in range(BS)]
    return 'BVPLUS(10,%s)' % ','.join(bits)

for i in range(START, END):
    add(*sha_e(BS, 1, 1, op2[i], i))
    add(*sha_a(BS, 1, 1, op5[i], i))
    if a.signed and i <= 8:
        add(*sha2_value(BS, 'IF', 'MAJ', i))
for i in range(16, MB):
    add(*message_expand(BS, 1 if a.signed else 0, i))
for i in range(MB):
    if i not in DIFF:
        for j in range(BS):
            cons.append('ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n' % (var('wv_%d_%d' % (i, j)), var('wd_%d_%d' % (i, j))))
for s in range(START - 4, START):
    for j in range(BS):
        for p in ('xv', 'xd', 'yv', 'yd'):
            cons.append('ASSERT %s = 0bin0;\n' % var('%s_%d_%d' % (p, s, j)))
for s in range(END - 8, END):
    for j in range(BS):
        cons.append('ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n' % (var('xv_%d_%d' % (s, j)), var('xd_%d_%d' % (s, j))))
for s in range(END - 4, END):
    for j in range(BS):
        cons.append('ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n' % (var('yv_%d_%d' % (s, j)), var('yd_%d_%d' % (s, j))))
cons.append('ASSERT BVGT(%s, 0bin0000000000);\n' % total('wd', DIFF))
if a.fixw:
    for i, row in WROWS.items():
        for k, ch in enumerate(row):
            j = BS - 1 - k
            v, d = {'u': (1, 1), 'n': (0, 1)}.get(ch, (0, 0))
            cons.append('ASSERT %s = 0bin%d;\nASSERT %s = 0bin%d;\n' % (var('wv_%d_%d' % (i, j)), v, var('wd_%d_%d' % (i, j)), d))
if a.tw is not None:
    cons.append('ASSERT BVLE(%s, 0bin%s);\n' % (total('wd', range(MB)), format(a.tw, '010b')))
if a.tw_eq is not None:
    cons.append('ASSERT %s = 0bin%s;\n' % (total('wd', range(MB)), format(a.tw_eq, '010b')))
if a.tE is not None:
    cons.append('ASSERT BVLE(%s, 0bin%s);\n' % (total('yd', range(START, END)), format(a.tE, '010b')))
if a.tA is not None:
    cons.append('ASSERT BVLE(%s, 0bin%s);\n' % (total('xd', range(START, END)), format(a.tA, '010b')))
with open(a.out, 'w') as f:
    f.write(''.join(decl)); f.write(''.join(cons)); f.write('\nQUERY FALSE;\nCOUNTEREXAMPLE;')
print(a.out, len(decl), 'variables', len(cons), 'assertion groups')
```

### A.10 `cgrun.sh`

```sh
# usage: cgrun.sh NAME MODEL THREADS SOLVE_SECS
n=$1; m=$2; th=$3; ss=$4
cd /w
date -u +"$n start %FT%TZ" >> cg/$n.log
valgrind --tool=callgrind --dump-instr=yes --compress-strings=no --compress-pos=no \
  --dump-before='CMSat::SATSolver::solve*' --callgrind-out-file=/w/cg/$n.out \
  /opt/stp/build/stp models/$m.cvc --cryptominisat --threads $th > cg/$n.stdout 2> cg/$n.err &
pid=$!
while kill -0 $pid 2>/dev/null; do
  if ls /w/cg/$n.out.1 >/dev/null 2>&1; then
    date -u +"$n solve-entered %FT%TZ" >> cg/$n.log
    sleep $ss; kill -TERM $pid; date -u +"$n term-sent %FT%TZ" >> cg/$n.log; break
  fi
  sleep 5
done
wait $pid; echo "$n rc=$?" >> cg/$n.log
date -u +"$n end %FT%TZ" >> cg/$n.log
```

### A.11 `windows.sh`

```sh
# usage: windows.sh NAME MODEL_SUBSTR PERIOD: once the solve-phase dump exists, dump a window every PERIOD s
n=$1; pat=$2; per=$3
pid=$(pgrep -f "valgrind.bin.*$pat" | head -1)
until ls /w/cg/$n.out.1 >/dev/null 2>&1; do kill -0 $pid 2>/dev/null || exit 0; sleep 5; done
while sleep $per; kill -0 $pid 2>/dev/null; do callgrind_control -d $pid >/dev/null 2>&1; date -u +"$n window-dump %FT%TZ" >> /w/cg/$n.log; done
```

### A.12 `ffrun.sh`

```sh
# usage: ffrun.sh NAME MODEL THREADS(>=2) PERIOD WINDOWS
# The STP front end runs uninstrumented; instrumentation starts when CryptoMiniSat starts its solver threads
# (the first extra task of the process), then a window is dumped every PERIOD s and the call is stopped after WINDOWS.
n=$1; m=$2; th=$3; per=$4; win=$5
cd /w
date -u +"$n start %FT%TZ" >> cg/$n.log
valgrind --tool=callgrind --instr-atstart=no --dump-instr=yes --compress-strings=no --compress-pos=no \
  --callgrind-out-file=/w/cg/$n.out /opt/stp/build/stp models/$m.cvc --cryptominisat --threads $th > cg/$n.stdout 2> cg/$n.err &
pid=$!
while kill -0 $pid 2>/dev/null; do
  if [ "$(ls /proc/$pid/task | wc -l)" -gt 1 ]; then
    callgrind_control -i on $pid >/dev/null; date -u +"$n solve-threads-started %FT%TZ" >> cg/$n.log; break
  fi
  sleep 0.5
done
for i in $(seq 1 $win); do
  sleep $per; kill -0 $pid 2>/dev/null || break
  if [ $i -lt $win ]; then callgrind_control -d $pid >/dev/null; date -u +"$n window-dump %FT%TZ" >> cg/$n.log; fi
done
kill -TERM $pid; date -u +"$n term-sent %FT%TZ" >> cg/$n.log
wait $pid; echo "$n rc=$?" >> cg/$n.log
date -u +"$n end %FT%TZ" >> cg/$n.log
```

### A.13 `mkdis.sh`

```sh
# disassemble every object named in the given callgrind parts (GNU objdump, Intel syntax) into /w/dis
mkdir -p /w/dis
grep -h "^ob=" "$@" | sort -u | sed 's/^ob=//' | while read -r ob; do
  [ -f "$ob" ] || continue
  base=/w/dis/$(echo "$ob" | sed 's|^/||; s|/|_|g')
  [ -s "$base.dis" ] || objdump -d -M intel --no-show-raw-insn "$ob" > "$base.dis"
  echo "$(sha256sum "$ob" | cut -c1-64) $ob"
done
```

### A.14 `stpdyn.py`

```python
"""Per-form cost of every instruction executed in one STP + CryptoMiniSat call, from callgrind parts (--dump-instr=yes).

Usage: stpdyn.py [--solve-only] NAME PART [PART ...]
The part written before the first CMSat::SATSolver::solve entry is the STP front end; later parts are solve-phase
windows. With --solve-only every part is a solve window (front end not instrumented). Every executed address of every
object is matched to `objdump -d -M intel` of that object and priced by x86ops.cost. PLT stubs are skipped functions
under callgrind's default --skip-plt=yes: their instructions are counted at the calling instruction and priced as it.
"""
import collections, json, os, re, subprocess, sys
from x86ops import cost, addr

# Multiply and floating-point forms that x86ops.py does not list are heavy too: 400 per scalar operation, times the
# number of lanes for packed forms, times 2 for fused multiply-add.
EXTRA_HEAVY = re.compile(r'^v?(cmp[a-z]*(ss|sd|ps|pd)|pmul[a-z]*|pmadd[a-z]*|f(n)?m(add|sub)[0-9]*(ss|sd|ps|pd))$')
LANES = {'ss': 1, 'sd': 1, 'pd': 2, 'ps': 4, 'pmuludq': 2, 'pmuldq': 2, 'pmulld': 4}

PREFIXES = {'lock', 'rep', 'repz', 'repe', 'repne', 'repnz', 'notrack', 'bnd', 'data16', 'rex64', 'cs', 'ds', 'es', 'ss'}
STRING = {'movs', 'stos', 'lods', 'scas', 'cmps'}

def normalise(mn, ops):
    """GNU objdump repeats prefixes and prints string instructions without a size suffix; undo both."""
    while (mn in PREFIXES or mn.startswith('rex')) and ops:
        sub = ','.join(ops).split(None, 1)
        mn, ops = sub[0], ([o.strip() for o in sub[1].split(',')] if len(sub) > 1 else [])
    if mn in STRING:
        return mn + 'b', []                  # one iteration of a string instruction: 6 operations in x86ops.py
    return mn, ops

DIVIDE = re.compile(r'^(i?div|v?(div|sqrt)(ss|sd|ps|pd)|f(i?div|sqrt)[a-z]*)$')
FUSED = re.compile(r'^vf(n)?m(add|sub)')

def tariff(mn, ops):
    """Price of a heavy form: 1024 for divide and square root, 400 otherwise, per lane, times 2 if fused."""
    base = 1024 if DIVIDE.match(mn) else 400
    core = mn[1:] if mn.startswith('v') else mn
    lanes = LANES.get(core, LANES.get(core[-2:], 8)) if re.search(r'(ps|pd|pmul[a-z]*|pmadd[a-z]*)$', core) or core.startswith(('pmul', 'pmadd')) else 1
    if any('ymm' in o for o in ops): lanes *= 2
    return base * lanes * (2 if FUSED.match(mn) else 1)

TARIFF_FILE = os.environ.get('TARIFFS')
EXACT = json.load(open(TARIFF_FILE)) if TARIFF_FILE else None
R32 = re.compile(r'^(e[a-z]{2}|r\d+d)$')

def family(mn, ops):
    """Heavy-form family of Section 15.7; None if the form has no emulation family."""
    o0 = ops[0] if ops else ''
    w32 = bool(R32.match(o0)) or 'DWORD' in o0
    if mn == 'div': return 'div32' if w32 else 'div64'
    if mn == 'idiv': return 'idiv32' if w32 else 'idiv64'
    if mn == 'mul': return 'mul32' if w32 else 'mul64'
    if mn == 'imul': return ('imul32_1' if w32 else 'imul64_1') if len(ops) == 1 else ('imul32' if w32 else 'imul64')
    if mn == 'pmuludq': return 'pmuludq'
    core = mn[1:] if mn.startswith('v') and not mn.startswith(('vf', 'vfn')) else mn
    if re.match(r'^u?comis[sd]$', core) or re.match(r'^cmp[a-z]+s[sd]$', core): return 'cmp_fp'
    if re.match(r'^(max|min)s[sd]$', core): return 'minmax_fp'
    if core.startswith('cvtt'): return 'cvt_f2i'
    if core.startswith('cvtsi2'): return 'cvt_i2f'
    if core in ('cvtss2sd', 'cvtsd2ss'): return 'cvt_ff'
    if re.match(r'^(add|sub)s[sd]$', core): return 'add_fp'
    if core in ('addpd', 'subpd'): return 'addpd'
    if re.match(r'^muls[sd]$', core): return 'mul_fp'
    if re.match(r'^divs[sd]$', core): return 'div_fp'
    if re.match(r'^vfn?m(add|sub)\d+s[sd]$', mn): return 'fma_fp'
    if re.match(r'^rounds[sd]$', core): return 'round_fp'
    return None

def heavy_extra(mn):
    m = EXTRA_HEAVY.match(mn)
    if not m: return None
    core = mn[1:] if mn.startswith('v') else mn
    lanes = LANES.get(core, LANES.get(core[-2:], 8))
    return 400 * lanes * (2 if re.search(r'm(add|sub)', core) and core.startswith('f') else 1)
from dynparse import disasm

DIS = {}
DISDIR = os.environ.get('DISDIR', '/w/dis')

def objects(ob):
    if ob not in DIS:
        base = os.path.join(DISDIR, ob.strip('/').replace('/', '_'))
        os.makedirs(DISDIR, exist_ok=True)
        if not os.path.exists(base + '.dis'):
            if not os.path.isfile(ob):
                DIS[ob] = {}
                return DIS[ob]
            subprocess.run(['sh', '-c', f'objdump -d -M intel --no-show-raw-insn "{ob}" > "{base}.dis"'], check=False)
        DIS[ob] = disasm(base + '.dis')
    return DIS[ob]

def read_part(path):
    ir = collections.defaultdict(collections.Counter); ob = None; skip = False
    for line in open(path, errors='replace'):
        if line.startswith('ob='): ob = line[3:].strip(); continue
        if line.startswith('calls='): skip = True; continue
        if line.startswith('0x'):
            if skip: skip = False; continue
            p = line.split()
            if len(p) >= 3: ir[ob][int(p[0], 16)] += int(p[2])
    return ir

def price(irs):
    T = O = H = HO = M = 0; per = collections.Counter(); per_ops = collections.Counter()
    mn_ir = collections.Counter(); hv = collections.Counter(); unk = collections.Counter(); hist = collections.Counter()
    for ir in irs:
        for ob, cnt in ir.items():
            d = objects(ob)
            for a, n in cnt.items():
                if a in d:
                    mn, ops = normalise(*d[a]); c, cls = cost(mn, ops)
                    if c is None and heavy_extra(mn): cls = 'heavy'
                    if cls == 'heavy':
                        fm = family(mn, ops) if EXACT else None
                        if fm:   # emulation cost, operand and result transfer (2), memory operand address and load
                            c = EXACT[fm] + 2 + sum(1 + addr(o) for o in ops if '[' in o)
                        else:
                            c = tariff(mn, ops)
                            if EXACT: unk['heavy:' + mn] += n
                    elif c is None: c = 8; unk[mn] += n
                    if cls == 'heavy': H += n; HO += c * n; hv[mn] += n
                    mn_ir[mn] += n
                else:
                    c = 8; M += n
                T += n; O += c * n; hist[c if c < 400 else 400] += n
                key = ob.split('/')[-1]; per[key] += n; per_ops[key] += c * n
    if not T: return None
    return dict(ir=T, ops=O, m=round(O / T, 4), heavy_share=round(H / T, 6),
                m_ordinary=round((O - HO) / (T - H), 4), unmapped_share=round(M / T, 6),
                objects={k: dict(share=round(v / T, 5), m=round(per_ops[k] / v, 3)) for k, v in per.most_common(12)},
                top_mnemonics=[(k, round(v / T, 4)) for k, v in mn_ir.most_common(12)],
                heavy_top=[(k, round(v / T, 6)) for k, v in hv.most_common(6)],
                unknown_share=round(sum(unk.values()) / T, 6), unknown_top=[(k, round(v / T, 6)) for k, v in unk.most_common(6)],
                cost_hist={k: round(v / T, 5) for k, v in sorted(hist.items())})

args = sys.argv[1:]
solve_only = args[0] == '--solve-only'
if solve_only: args = args[1:]
name, parts = args[0], [p for p in args[1:] if os.path.getsize(p)]
parts = sorted(parts, key=lambda p: int(p.rsplit('.', 1)[1]) if p.rsplit('.', 1)[1].isdigit() else 10 ** 9)
irs = [read_part(p) for p in parts]
front, solve = ([], irs) if solve_only else (irs[:1], irs[1:])
res = dict(call=name, parts=[os.path.basename(p) for p in parts],
           front_end=price(front) if front else None, solve=price(solve), whole=price(irs))
res['solve_windows'] = [dict(ir=w['ir'], m=w['m'], heavy_share=w['heavy_share'])
                        for w in (price([ir]) for ir in solve) if w]
res['m_max_phase'] = max(v['m'] for v in (res['front_end'], res['solve']) if v)
print(json.dumps(res, indent=1))
```

### A.15 `stpsum.py`

```python
"""Collect the per-call stpdyn.py results into m_stp.json.

Each call splits into one-off parts (the STP front end, and the end part from the last periodic dump to the exit)
and search windows (the parts between periodic dumps, 60-120 s each). The charge for the characteristic search is
absolute:

    operations <= 32 * (59 * X_once * m_once + I_max * m_search),

with X_once the largest front end plus the largest end part of any call (instructions), m_once the costliest
one-off part, I_max = S * R_cal * 593,858 the instructions of the 59 charged calls at most, and m_search the
costliest search window of any call (m values rounded up to 0.001). Every search instruction is priced at the
costliest minute, every one-off instruction once more at the costliest one-off part.
"""
import json, math, sys

R_CAL = 44197378388 / 40.42
I_MAX = 1.85 * R_CAL * 593858
up = lambda x: math.ceil(x * 1000) / 1000
calls = {}
for path in sys.argv[1:]:
    d = json.load(open(path))
    fe, so, wh = d['front_end'], d['solve'], d['whole']
    parts = d['solve_windows']
    win, end = parts[:-1], parts[-1]
    calls[d['call']] = dict(front_end_ir=fe['ir'] if fe else None, front_end_m=fe['m'] if fe else None,
                            front_end_heavy=fe['heavy_share'] if fe else None,
                            solve_ir=so['ir'], solve_m=so['m'], solve_heavy=so['heavy_share'], solve_ordinary=so['m_ordinary'],
                            windows=[w['m'] for w in win], window_ir=[w['ir'] for w in win],
                            end_ir=end['ir'], end_m=end['m'],
                            whole_ir=wh['ir'], whole_m=wh['m'], whole_heavy=wh['heavy_share'],
                            front_end_share=round(fe['ir'] / wh['ir'], 4) if fe else None,
                            unmapped_share=wh['unmapped_share'], unknown_share=wh['unknown_share'])
cs = calls.values()
full = [c for c in cs if c['front_end_m'] is not None]
m_front = up(max(c['front_end_m'] for c in full))
m_end = up(max(c['end_m'] for c in cs))
m_once = max(m_front, m_end)
m_search = up(max(m for c in cs for m in c['windows']))
x_once = max(c['front_end_ir'] for c in full) + max(c['end_ir'] for c in cs)
ops_run = 59 * x_once * m_once + I_MAX * m_search
out = dict(calls=calls, m_front=m_front, m_end=m_end, m_once=m_once, m_search=m_search,
           front_end_ir_max=max(c['front_end_ir'] for c in full), end_ir_max=max(c['end_ir'] for c in cs),
           x_once=x_once, i_max=I_MAX, ops_run=ops_run, m_eff=ops_run / I_MAX,
           m_max_milli=math.ceil(ops_run / I_MAX * 1000),
           search_mean_max=max(c['solve_m'] for c in cs), window_m_min=min(m for c in cs for m in c['windows']),
           m_whole_max=max(c['whole_m'] for c in full), front_end_share_min=min(c['front_end_share'] for c in full))
print(json.dumps(out, indent=1))
```

### A.16 `heavyemu.py`

```python
"""Counted emulation of the heavy x86-64 forms with the v5 primitives only (collision-frontier-v5).

Primitives counted, 1 each: add/sub mod 2^256, AND/OR/XOR, shift, comparison, conditional branch, load, store.
A comparison is always followed by its conditional branch (2). Table entries cost an address add and a load or
store (2). Constants are immediates. Loops have fixed trip counts and are straight-line code.

Every data-dependent choice goes through sel(): both arms are evaluated on scratch counters and the costlier arm is
charged, whichever is taken. Each emulation therefore costs the same on every input, and that cost is its exact
worst case. main() checks every form against numpy / exact rational references on random and special inputs and
prints the cost per form, which must not exceed the tariff of Section 15.7.
"""
import math, random, struct, sys
from fractions import Fraction
import numpy as np

WM = (1 << 256) - 1
N = [0]

def add(a, b): N[0] += 1; return a + b         # exponents may go below 0: read them with a fixed offset
def sub(a, b): N[0] += 1; return a - b
def and_(a, b): N[0] += 1; return a & b
def or_(a, b): N[0] += 1; return a | b
def xor(a, b): N[0] += 1; return a ^ b
def amt(k): return k if 0 <= k <= 511 else 511     # a shift by 256 or more clears the word
def shl(a, k): N[0] += 1; return (a << amt(k)) & WM
def shr(a, k): N[0] += 1; return a >> amt(k)
def lt(a, b): N[0] += 2; return a < b
def le(a, b): N[0] += 2; return a <= b
def eq(a, b): N[0] += 2; return a == b
def ld(t, i): N[0] += 2; return t[i]
def st(t, i, v): N[0] += 2; t[i] = v

def sel(c, ft, fe):
    """Charge the costlier arm; return the taken one."""
    n0 = N[0]; N[0] = 0; vt = ft(); ct = N[0]; N[0] = 0; ve = fe(); ce = N[0]
    N[0] = n0 + max(ct, ce)
    return vt if c else ve

# ---------------------------------------------------------------- integer
M64, M32 = (1 << 64) - 1, (1 << 32) - 1

def umul(a, b, bits):
    """Radix-16 shift-and-add: table of 16 multiples, then one table add per 4-bit digit of b."""
    T = [0] * 16
    st(T, 0, 0); st(T, 1, a)
    for d in range(2, 16):
        v = shl(T[d // 2], 1) if d % 2 == 0 else add(T[d - 1], a)
        st(T, d, v)
    acc = 0
    for i in reversed(range(0, bits, 4)):
        acc = add(shl(acc, 4), ld(T, and_(shr(b, i), 15)))
    return acc

def imul_low(a, b, w):
    """imul r, r/m(, imm): low w bits and OF/CF (signed product does not fit in w bits)."""
    m, sb = (1 << w) - 1, 1 << (w - 1)
    p = umul(a, b, w)
    lo, hi = and_(p, m), shr(p, w)
    hi = sel(le(sb, a), lambda: sub(hi, b), lambda: hi)
    hi = sel(le(sb, b), lambda: sub(hi, a), lambda: hi)
    hi = and_(hi, m)
    ext = sel(le(sb, lo), lambda: m, lambda: 0)
    of = sel(eq(hi, ext), lambda: 0, lambda: 1)
    return lo, of

def mul_full(a, b, w, signed):
    """mul / imul r/m (one operand): rdx:rax = full product, CF/OF."""
    m, sb = (1 << w) - 1, 1 << (w - 1)
    p = umul(a, b, w)
    lo, hi = and_(p, m), shr(p, w)
    if signed:
        hi = sel(le(sb, a), lambda: sub(hi, b), lambda: hi)
        hi = sel(le(sb, b), lambda: sub(hi, a), lambda: hi)
        hi = and_(hi, m)
        ext = sel(le(sb, lo), lambda: m, lambda: 0)
        cf = sel(eq(hi, ext), lambda: 0, lambda: 1)
    else:
        cf = sel(eq(hi, 0), lambda: 0, lambda: 1)
    return lo, hi, cf

def udiv(nh, nl, d, w):
    """Restoring division of the 2w-bit nh:nl by d (nh < d): w quotient bits, one per step."""
    r, q = nh, 0
    for i in reversed(range(w)):
        r = or_(shl(r, 1), and_(shr(nl, i), 1))
        q = shl(q, 1)
        r, q = sel(le(d, r), lambda: (sub(r, d), or_(q, 1)), lambda: (r, q))
    return q, r

def idiv(nh, nl, d, w):
    """Signed division of nh:nl by d (truncating), via magnitudes."""
    m, sb = (1 << w) - 1, 1 << (w - 1)
    full = or_(shl(nh, w), nl)
    nneg = le(1 << (2 * w - 1), full)
    full = sel(nneg, lambda: and_(sub(0, full), (1 << (2 * w)) - 1), lambda: full)
    dneg = le(sb, d)
    da = sel(dneg, lambda: and_(sub(0, d), m), lambda: d)
    q, r = udiv(shr(full, w), and_(full, m), da, w)
    q = sel(eq(1 if nneg else 0, 1 if dneg else 0), lambda: q, lambda: and_(sub(0, q), m))
    r = sel(nneg, lambda: and_(sub(0, r), m), lambda: r)
    return q, r

def pmuludq(a, b):
    p0 = umul(and_(a, M32), and_(b, M32), 32)
    p1 = umul(and_(shr(a, 64), M32), and_(shr(b, 64), M32), 32)
    return or_(p0, shl(p1, 64))

# ---------------------------------------------------------------- binary floating point
class Fmt:
    def __init__(s, w, m, ebits):
        s.w, s.m, s.e = w, m, ebits
        s.bias, s.emax = (1 << (ebits - 1)) - 1, (1 << ebits) - 1
        s.fmask, s.hidden = (1 << m) - 1, 1 << m
        s.sign, s.abs = 1 << (w - 1), (1 << (w - 1)) - 1
        s.inf, s.qbit = s.emax << m, 1 << (m - 1)
        s.dnan = s.sign | s.inf | s.qbit          # x86 default NaN ("floating-point indefinite")
F64, F32 = Fmt(64, 52, 11), Fmt(32, 23, 8)

def unpack(x, F):
    """(class, sign, sig, scale): value = sig * 2^scale. class 0 finite, 1 inf, 2 NaN."""
    s = shr(x, F.w - 1); e = and_(shr(x, F.m), F.emax); f = and_(x, F.fmask)
    def special(): return sel(eq(f, 0), lambda: (1, s, 0, 0), lambda: (2, s, f, 0))
    def finite():
        return sel(eq(e, 0), lambda: (0, s, f, 1 - F.bias - F.m),
                   lambda: (0, s, or_(f, F.hidden), sub(e, F.bias + F.m)))
    return sel(eq(e, F.emax), special, finite)

def lead(x, width=256):
    """Position of the highest set bit of x > 0, by binary search."""
    L, k = 0, width // 2
    while k:
        L = sel(eq(shr(x, add(L, k)), 0), lambda: L, lambda: add(L, k))
        k //= 2
    return L

def sticky_shr(x, d, cap):
    """x >> d with the lost bits ORed into bit 0; d < cap."""
    lost = and_(x, sub(shl(1, d), 1))
    y = shr(x, d)
    return sel(eq(lost, 0), lambda: y, lambda: or_(y, 1))

def round_pack(s, k, sig, F, width=256):
    """Round sig * 2^k (sig > 0) to nearest-even in F; returns the encoding."""
    L = lead(sig, width)
    eb = add(L, k + F.bias - 1)                 # biased exponent minus 1 of the leading bit
    t = F.m + 3
    x = sel(lt(L, t), lambda: shl(sig, sub(t, L)), lambda: sticky_shr(sig, sub(L, t), width))
    def subn():
        sh = sub(0, eb)
        return sel(lt(t + 1, sh), lambda: (1, 0), lambda: (sticky_shr(x, sh, width), 0))
    x, eb = sel(lt(eb, 0), subn, lambda: (x, eb))
    low, q = and_(x, 7), shr(x, 3)
    q = sel(lt(4, low), lambda: add(q, 1),
            lambda: sel(eq(low, 4), lambda: add(q, and_(q, 1)), lambda: q))
    mag = add(shl(eb, F.m), q)
    mag = sel(le(F.inf, mag), lambda: F.inf, lambda: mag)
    return or_(shl(s, F.w - 1), mag)

def qnan(x, F): return or_(x, F.qbit)

def cmax(ca, cb): return sel(lt(ca, cb), lambda: cb, lambda: ca)

def nan2(a, b, ca, cb, F):
    return sel(eq(ca, 2), lambda: qnan(a, F), lambda: sel(eq(cb, 2), lambda: qnan(b, F), lambda: F.dnan))

def signed_inf(s, F): return or_(shl(s, F.w - 1), F.inf)

def exact_sum(sx, kx, mx, sy, ky, my, lim):
    """x + y for sig*2^k operands (nonzero): an exact integer sum, or the larger operand with a sticky 1."""
    big = le(ky, kx)
    kbig, ksm, mbig, msm, sbig, ssm = (kx, ky, mx, my, sx, sy) if big else (ky, kx, my, mx, sy, sx)
    N[0] += 9                                       # data-dependent swap of three operand pairs (xor-swaps)
    d = sub(kbig, ksm)
    x, y, k = sel(lt(lim, d), lambda: (shl(mbig, lim + 2), 1, sub(kbig, lim + 2)), lambda: (shl(mbig, d), msm, ksm))
    return sel(eq(sbig, ssm), lambda: (add(x, y), sbig, k),
               lambda: sel(lt(x, y), lambda: (sub(y, x), ssm, k), lambda: (sub(x, y), sbig, k)))

def fadd(a, b, F, neg_b=False):
    ca, sa, ma, ka = unpack(a, F)
    cb, sb, mb, kb = unpack(b, F)
    if neg_b: sb = xor(sb, 1)
    cls = cmax(ca, cb)
    def inf_case():
        return sel(eq(ca, 1), lambda: sel(eq(cb, 1), lambda: sel(eq(sa, sb), lambda: signed_inf(sa, F), lambda: F.dnan),
                                            lambda: signed_inf(sa, F)),
                   lambda: signed_inf(sb, F))
    def finite():
        def zero_a():
            return sel(eq(mb, 0), lambda: shl(and_(sa, sb), F.w - 1), lambda: or_(shl(sb, F.w - 1), and_(b, F.abs)))
        def core():
            r, rs, k = exact_sum(sa, ka, ma, sb, kb, mb, F.m + 5)
            return sel(eq(r, 0), lambda: 0, lambda: round_pack(rs, k, r, F))
        return sel(eq(ma, 0), zero_a, lambda: sel(eq(mb, 0), lambda: or_(shl(sa, F.w - 1), and_(a, F.abs)), core))
    return sel(eq(cls, 2), lambda: nan2(a, b, ca, cb, F), lambda: sel(eq(cls, 1), inf_case, finite))

def is_zero(c, m): return sel(eq(c, 0), lambda: eq(m, 0), lambda: False)

def fmul(a, b, F):
    ca, sa, ma, ka = unpack(a, F)
    cb, sb, mb, kb = unpack(b, F)
    s = xor(sa, sb)
    cls = cmax(ca, cb)
    def inf_case():
        z = sel(eq(ca, 1), lambda: is_zero(cb, mb), lambda: is_zero(ca, ma))
        return sel(z, lambda: F.dnan, lambda: signed_inf(s, F))
    def finite():
        z = sel(eq(ma, 0), lambda: True, lambda: eq(mb, 0))
        bits = 56 if F is F64 else 24
        return sel(z, lambda: shl(s, F.w - 1), lambda: round_pack(s, add(ka, kb), umul(ma, mb, bits), F))
    return sel(eq(cls, 2), lambda: nan2(a, b, ca, cb, F), lambda: sel(eq(cls, 1), inf_case, finite))

def norm_sig(m, k, F):
    """Shift a nonzero significand so that its leading one is at bit F.m."""
    L = lead(m, 64)
    return sel(lt(L, F.m), lambda: (shl(m, sub(F.m, L)), sub(k, sub(F.m, L))), lambda: (m, k))

def fdiv(a, b, F):
    ca, sa, ma, ka = unpack(a, F)
    cb, sb, mb, kb = unpack(b, F)
    s = xor(sa, sb)
    cls = cmax(ca, cb)
    def inf_case():
        return sel(eq(ca, 1), lambda: sel(eq(cb, 1), lambda: F.dnan, lambda: signed_inf(s, F)), lambda: shl(s, F.w - 1))
    def finite():
        def bz(): return sel(eq(ma, 0), lambda: F.dnan, lambda: signed_inf(s, F))
        def run():
            x, kx = norm_sig(ma, ka, F)
            y, ky = norm_sig(mb, kb, F)
            nq = F.m + 5
            r, q = x, 0
            for _ in range(nq):
                q = shl(q, 1)
                r, q = sel(le(y, r), lambda: (sub(r, y), or_(q, 1)), lambda: (r, q))
                r = shl(r, 1)
            q = sel(eq(r, 0), lambda: q, lambda: or_(q, 1))
            return round_pack(s, sub(sub(kx, ky), nq - 1), q, F)
        return sel(eq(mb, 0), bz, lambda: sel(eq(ma, 0), lambda: shl(s, F.w - 1), run))
    return sel(eq(cls, 2), lambda: nan2(a, b, ca, cb, F), lambda: sel(eq(cls, 1), inf_case, finite))

def fma(a, b, c, F, neg_c=False):
    """a * b + c with one rounding (vfmadd*sd; vfmsub*sd with neg_c)."""
    ca, sa, ma, ka = unpack(a, F)
    cb, sb, mb, kb = unpack(b, F)
    cc, sc, mc, kc = unpack(c, F)
    if neg_c: sc = xor(sc, 1)
    sp = xor(sa, sb)
    cls = cmax(cmax(ca, cb), cc)
    def nan_case():
        return sel(eq(ca, 2), lambda: qnan(a, F), lambda: sel(eq(cb, 2), lambda: qnan(b, F),
                   lambda: sel(eq(cc, 2), lambda: qnan(c, F), lambda: F.dnan)))
    def inf_case():
        z = sel(eq(ca, 1), lambda: is_zero(cb, mb), lambda: sel(eq(cb, 1), lambda: is_zero(ca, ma), lambda: False))
        pinf = sel(eq(ca, 1), lambda: True, lambda: eq(cb, 1))
        def pi(): return sel(eq(cc, 1), lambda: sel(eq(sp, sc), lambda: signed_inf(sp, F), lambda: F.dnan), lambda: signed_inf(sp, F))
        return sel(z, lambda: F.dnan, lambda: sel(pinf, pi, lambda: signed_inf(sc, F)))
    def finite():
        p = umul(ma, mb, 56 if F is F64 else 24)
        kp = add(ka, kb)
        def pz():
            return sel(eq(mc, 0), lambda: shl(and_(sp, sc), F.w - 1), lambda: or_(shl(sc, F.w - 1), and_(c, F.abs)))
        def both():
            r, rs, k = exact_sum(sp, kp, p, sc, kc, mc, 2 * F.m + 8)
            return sel(eq(r, 0), lambda: 0, lambda: round_pack(rs, k, r, F))
        return sel(eq(p, 0), pz, lambda: sel(eq(mc, 0), lambda: round_pack(sp, kp, p, F), both))
    return sel(eq(cls, 2), nan_case, lambda: sel(eq(cls, 1), inf_case, finite))

def fcmp(a, b, F):
    """Ordering for comisd/ucomisd/comiss and cmp*sd: 'u', 'lt', 'eq', 'gt'."""
    xa, xb = and_(a, F.abs), and_(b, F.abs)
    def ordered():
        def keys():
            ka = sel(le(F.sign, a), lambda: sub(1 << F.w, xa), lambda: add(xa, 1 << F.w))
            kb = sel(le(F.sign, b), lambda: sub(1 << F.w, xb), lambda: add(xb, 1 << F.w))
            return sel(lt(ka, kb), lambda: 'lt', lambda: sel(eq(ka, kb), lambda: 'eq', lambda: 'gt'))
        return sel(eq(or_(xa, xb), 0), lambda: 'eq', keys)
    return sel(lt(F.inf, xa), lambda: 'u', lambda: sel(lt(F.inf, xb), lambda: 'u', ordered))

def comisd(a, b, F):
    o = fcmp(a, b, F); N[0] += 1                      # write ZF, PF, CF as one word
    return {'u': (1, 1, 1), 'lt': (0, 0, 1), 'eq': (1, 0, 0), 'gt': (0, 0, 0)}[o]

def cmpsd(a, b, F, pred):
    o = fcmp(a, b, F); N[0] += 1                      # write the all-ones or zero mask
    r = {'nle': o in ('gt', 'u'), 'nlt': o in ('gt', 'eq', 'u')}[pred]
    return (1 << F.w) - 1 if r else 0

def fmax(a, b, F, is_max=True):
    """maxsd/minsd: the first operand if it is greater (smaller), else the second (also for NaN or equal)."""
    o = fcmp(a, b, F); N[0] += 1                      # select one of the two words
    return a if o == ('gt' if is_max else 'lt') else b

def cvtsi2f(x, w, F):
    neg = le(1 << (w - 1), x)
    mag = sel(neg, lambda: and_(sub(0, x), (1 << w) - 1), lambda: x)
    return sel(eq(mag, 0), lambda: 0, lambda: round_pack(1 if neg else 0, 0, mag, F, 64))

def cvttf2si(x, w, F):
    c, s, m, k = unpack(x, F)
    ind = 1 << (w - 1)
    def fin():
        def go():
            E = add(lead(m, 64), k)
            def inr():
                v = sel(lt(k, 0), lambda: shr(m, sub(0, k)), lambda: shl(m, k))
                return sel(eq(s, 1), lambda: and_(sub(0, v), (1 << w) - 1), lambda: v)
            return sel(le(w - 1, E), lambda: ind, lambda: sel(lt(E, 0), lambda: 0, inr))
        return sel(eq(m, 0), lambda: 0, go)
    return sel(eq(c, 0), fin, lambda: ind)

def cvtff(x, Fi, Fo):
    c, s, m, k = unpack(x, Fi)
    def nan():
        pay = shl(m, Fo.m - Fi.m) if Fo.m > Fi.m else shr(m, Fi.m - Fo.m)
        return or_(or_(shl(s, Fo.w - 1), Fo.inf | Fo.qbit), and_(pay, Fo.fmask))
    def fin(): return sel(eq(m, 0), lambda: shl(s, Fo.w - 1), lambda: round_pack(s, k, m, Fo, 64))
    return sel(eq(c, 2), nan, lambda: sel(eq(c, 1), lambda: signed_inf(s, Fo), fin))

def froundi(x, mode, F):
    """roundsd/vroundsd: round to an integral value; mode 0 nearest-even, 1 down, 2 up, 3 toward zero."""
    c, s, m, k = unpack(x, F)
    one = F.bias << F.m
    def fin():
        def frac():
            d = sub(0, k)
            def small():                              # |x| < 1/2
                r = {0: lambda: 0, 1: lambda: sel(eq(s, 1), lambda: one, lambda: 0),
                     2: lambda: sel(eq(s, 0), lambda: one, lambda: 0), 3: lambda: 0}[mode]()
                return or_(shl(s, F.w - 1), r)
            def mid():
                fr, ip = and_(m, sub(shl(1, d), 1)), shr(m, d)
                half = shl(1, sub(d, 1))
                inc = {0: lambda: sel(lt(half, fr), lambda: 1, lambda: sel(eq(fr, half), lambda: and_(ip, 1), lambda: 0)),
                       1: lambda: sel(eq(s, 1), lambda: sel(eq(fr, 0), lambda: 0, lambda: 1), lambda: 0),
                       2: lambda: sel(eq(s, 0), lambda: sel(eq(fr, 0), lambda: 0, lambda: 1), lambda: 0),
                       3: lambda: 0}[mode]()
                ip = add(ip, inc)
                return sel(eq(ip, 0), lambda: shl(s, F.w - 1), lambda: round_pack(s, 0, ip, F, 64))
            return sel(lt(F.m + 2, d), small, mid)
        return sel(eq(m, 0), lambda: x, lambda: sel(le(0, k), lambda: x, frac))
    return sel(eq(c, 2), lambda: qnan(x, F), lambda: sel(eq(c, 1), lambda: x, fin))

def addpd(a, b):
    lo = fadd(and_(a, M64), and_(b, M64), F64)
    hi = fadd(and_(shr(a, 64), M64), and_(shr(b, 64), M64), F64)
    return or_(lo, shl(hi, 64))

# ---------------------------------------------------------------- references and checks
def f2b(v, F): return int(np.array([v], dtype='<f8' if F is F64 else '<f4').view('<u8' if F is F64 else '<u4')[0])
def b2f(x, F): return np.array([x], dtype='<u8' if F is F64 else '<u4').view('<f8' if F is F64 else '<f4')[0]
def isnanb(x, F): return (x & F.abs) > F.inf

def same(r, ref, F):
    return (isnanb(r, F) and isnanb(ref, F)) or r == ref

def operands(F, n, rng):
    """Random encodings: uniform bits, specials, subnormals, near-equal pairs and halfway cases."""
    sp = [0, F.sign, F.inf, F.inf | F.sign, F.dnan, F.inf | 1, F.inf | F.qbit | 5, 1, F.fmask, F.hidden, F.abs ^ F.fmask ^ F.hidden,
          (F.bias << F.m), (F.bias << F.m) | F.sign, ((F.bias + 1) << F.m) - 1]
    out = []
    for i in range(n):
        r = rng.random()
        if r < 0.15: x = rng.choice(sp)
        elif r < 0.35: x = rng.getrandbits(F.w)
        elif r < 0.5: x = rng.getrandbits(F.m) | (rng.getrandbits(1) << (F.w - 1))
        else:
            e = F.bias + rng.randint(-30, 30)
            x = (rng.getrandbits(1) << (F.w - 1)) | (e << F.m) | rng.getrandbits(F.m)
            if rng.random() < 0.3: x &= ~((1 << rng.randint(1, F.m)) - 1)
        out.append(x)
    return out

def ref_fma(a, b, c, F, neg_c):
    A, B, Cv = (float(b2f(v, F)) for v in (a, b, c))
    if neg_c: Cv = -Cv
    if any(math.isnan(v) for v in (A, B, Cv)): return F.dnan
    if math.isinf(A) or math.isinf(B):
        if A == 0 or B == 0: return F.dnan
        pinf = math.copysign(math.inf, A) * math.copysign(1, B)
        if math.isinf(Cv) and Cv != pinf: return F.dnan
        return f2b(pinf, F)
    if math.isinf(Cv): return f2b(Cv, F)                 # finite exact product plus infinity
    ex = Fraction(A) * Fraction(B) + Fraction(Cv)
    if ex == 0:
        if A * B == 0 and Cv == 0:
            neg = (math.copysign(1, A * B) < 0) and (math.copysign(1, Cv) < 0)
            return F.sign if neg else 0
        return 0
    try:
        r = ex.numerator / ex.denominator
    except OverflowError:
        r = math.inf if ex > 0 else -math.inf
    return f2b(r, F)

def main(n=20000, seed=1):
    rng = random.Random(seed)
    costs, bad = {}, {}
    def rec(name, cost, ok):
        costs.setdefault(name, set()).add(cost)
        if not ok: bad[name] = bad.get(name, 0) + 1
    np.seterr(all='ignore')
    for F, tag in ((F64, 'sd'), (F32, 'ss')):
        xs, ys = operands(F, n, rng), operands(F, n, rng)
        zs = operands(F, n, rng)
        dt = np.float64 if F is F64 else np.float32
        for a, b, c in zip(xs, ys, zs):
            A, B = b2f(a, F), b2f(b, F)
            for nm, fn, rf in (('add', lambda: fadd(a, b, F), lambda: f2b(dt(A) + dt(B), F)),
                               ('sub', lambda: fadd(a, b, F, True), lambda: f2b(dt(A) - dt(B), F)),
                               ('mul', lambda: fmul(a, b, F), lambda: f2b(dt(A) * dt(B), F)),
                               ('div', lambda: fdiv(a, b, F), lambda: f2b(dt(A) / dt(B), F))):
                N[0] = 0; r = fn(); rec(nm + tag, N[0], same(r, rf(), F))
            N[0] = 0; fl = comisd(a, b, F)
            o = 'u' if (np.isnan(A) or np.isnan(B)) else ('lt' if A < B else 'eq' if A == B else 'gt')
            rec('comi' + tag, N[0], fl == {'u': (1, 1, 1), 'lt': (0, 0, 1), 'eq': (1, 0, 0), 'gt': (0, 0, 0)}[o])
            for pred in ('nle', 'nlt'):
                N[0] = 0; r = cmpsd(a, b, F, pred)
                want = {'nle': not (A <= B), 'nlt': not (A < B)}[pred]
                rec('cmp' + pred + tag, N[0], r == ((1 << F.w) - 1 if want else 0))
            for nm, ismax in (('max', True), ('min', False)):
                N[0] = 0; r = fmax(a, b, F, ismax)
                want = a if ((A > B) if ismax else (A < B)) else b
                rec(nm + tag, N[0], r == want)
            if F is F64:
                for neg in (False, True):
                    N[0] = 0; r = fma(a, b, c, F, neg)
                    rec('fmsub' if neg else 'fmadd', N[0], same(r, ref_fma(a, b, c, F, neg), F))
                for mode in range(4):
                    N[0] = 0; r = froundi(a, mode, F)
                    fn = {0: np.rint, 1: np.floor, 2: np.ceil, 3: np.trunc}[mode]
                    rec('roundsd', N[0], same(r, f2b(fn(A), F), F))
                N[0] = 0; r = cvtff(a, F64, F32); rec('cvtsd2ss', N[0], same(r, f2b(np.float32(A), F32), F32))
                for w in (64, 32):
                    N[0] = 0; r = cvttf2si(a, w, F)
                    ok = (not np.isfinite(A)) or abs(math.trunc(float(A))) >= 2 ** (w - 1)
                    want = 1 << (w - 1) if ok and not (np.isfinite(A) and math.trunc(float(A)) == -2 ** (w - 1)) else (math.trunc(float(A)) & ((1 << w) - 1))
                    rec('cvttsd2si' + str(w), N[0], r == want)
            else:
                N[0] = 0; r = cvtff(a, F32, F64); rec('cvtss2sd', N[0], same(r, f2b(np.float64(A), F64), F64))
            N[0] = 0; r = addpd(a | (b << 64), b | (a << 64)) if F is F64 else 0
            if F is F64:
                rec('addpd', N[0], same(r & M64, f2b(A + B, F64), F64) and same(r >> 64, f2b(B + A, F64), F64))
    for w in (64, 32):
        for _ in range(n):
            x = rng.choice([0, 1, (1 << w) - 1, 1 << (w - 1), rng.getrandbits(w), rng.getrandbits(rng.randint(1, w))])
            N[0] = 0; r = cvtsi2f(x, w, F64)
            sx = x - (1 << w) if x >> (w - 1) else x
            rec('cvtsi2sd' + str(w), N[0], r == f2b(float(sx), F64))
    for w in (64, 32):
        m = (1 << w) - 1
        for _ in range(n):
            a = rng.choice([0, 1, m, 1 << (w - 1), rng.getrandbits(w), rng.getrandbits(rng.randint(1, w))])
            b = rng.choice([0, 1, m, 1 << (w - 1), rng.getrandbits(w), rng.getrandbits(rng.randint(1, w))])
            sa, sb2 = (a - (1 << w) if a >> (w - 1) else a), (b - (1 << w) if b >> (w - 1) else b)
            N[0] = 0; lo, of = imul_low(a, b, w)
            p = sa * sb2
            rec('imul%d' % w, N[0], lo == (p & m) and of == (0 if -(1 << (w - 1)) <= p < (1 << (w - 1)) else 1))
            N[0] = 0; lo, hi, cf = mul_full(a, b, w, False)
            rec('mul%d' % w, N[0], (hi << w | lo) == a * b and cf == (1 if (a * b) >> w else 0))
            N[0] = 0; lo, hi, cf = mul_full(a, b, w, True)
            rec('imul%d_1' % w, N[0], ((hi << w | lo) - ((1 << 2 * w) if hi >> (w - 1) else 0)) == p)
            d = b or 1
            nh = rng.randrange(d); nl = rng.getrandbits(w)
            N[0] = 0; q, r = udiv(nh, nl, d, w)
            nn = nh << w | nl
            rec('div%d' % w, N[0], q == nn // d and r == nn % d)
            sd = sb2 or 1
            nsv = rng.randint(-(1 << (2 * w - 2)), (1 << (2 * w - 2)))
            qq = abs(nsv) // abs(sd) * (1 if (nsv >= 0) == (sd > 0) else -1)
            if -(1 << (w - 1)) <= qq < (1 << (w - 1)):
                full = nsv & ((1 << 2 * w) - 1)
                N[0] = 0; q, r = idiv(full >> w, full & m, sd & m, w)
                rr = nsv - qq * sd
                rec('idiv%d' % w, N[0], q == (qq & m) and r == (rr & m))
    for _ in range(n):
        a, b = rng.getrandbits(128), rng.getrandbits(128)
        N[0] = 0; r = pmuludq(a, b)
        rec('pmuludq', N[0], r == ((a & M32) * (b & M32)) | (((a >> 64 & M32) * (b >> 64 & M32)) << 64))
    print('%-14s %8s %8s %6s' % ('form', 'cost', 'tests', 'wrong'))
    for k in sorted(costs):
        cs = costs[k]
        print('%-14s %8s %8d %6d' % (k, max(cs) if len(cs) == 1 else '%d-%d' % (min(cs), max(cs)), n, bad.get(k, 0)))
    return costs, bad

# x86 form family (as classified by stpdyn.py) -> emulations whose largest cost is its tariff
FAMILIES = {'div64': ['div64'], 'div32': ['div32'], 'idiv32': ['idiv32'], 'idiv64': ['idiv64'],
            'imul64': ['imul64'], 'imul32': ['imul32'], 'imul64_1': ['imul64_1'], 'imul32_1': ['imul32_1'],
            'mul64': ['mul64'], 'mul32': ['mul32'], 'pmuludq': ['pmuludq'],
            'cmp_fp': ['comisd', 'comiss', 'cmpnlesd', 'cmpnltsd', 'cmpnless', 'cmpnltss'],
            'minmax_fp': ['maxsd', 'maxss', 'minsd', 'minss'], 'cvt_f2i': ['cvttsd2si64', 'cvttsd2si32'],
            'cvt_i2f': ['cvtsi2sd64', 'cvtsi2sd32'], 'cvt_ff': ['cvtss2sd', 'cvtsd2ss'],
            'add_fp': ['addsd', 'subsd', 'addss', 'subss'], 'addpd': ['addpd'], 'mul_fp': ['mulsd', 'mulss'],
            'div_fp': ['divsd', 'divss'], 'fma_fp': ['fmadd', 'fmsub'], 'round_fp': ['roundsd']}

if __name__ == '__main__':
    costs, bad = main(int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
    if len(sys.argv) > 2:
        assert not bad, bad
        import json
        json.dump({f: max(max(costs[e]) for e in es) for f, es in FAMILIES.items()}, open(sys.argv[2], 'w'), indent=1)
```

### A.17 `secondblock.py`

```python
"""Two-sided second block of the sha256-r32 attack, steps 14..31, vectorised (numpy uint32).

Builds the real P4 list from the advice (proof Section 4) and evaluates Step-3 stages for many candidates at once.
A tuple enters steps 16..31 only through its schedule constants:
    W16 = s1(W14) + [W9 + s0(W1) + W0]     W17 = s1(W15) + [W10 + s0(W2) + W1]
    W18 = s1(W16) + [W11 + s0(W3) + W2]    W19 = s1(W17) + [W12 + s0(W4) + W3]
    W20 = s1(W18) + c20,  c20 = W13 + s0(W5) + W4      W21 = s1(W19) + W14 + c21,  c21 = s0(W6) + W5
    W22 = s1(W20) + W15 + c22,  c22 = s0(W7) + W6      (primed: the same with primed words)
"""
import re
import numpy as np

M32 = np.uint32(0xFFFFFFFF)
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967]
K = [np.uint32(k) for k in K]

def rotr(x, r): return (x >> np.uint32(r)) | (x << np.uint32(32 - r))
def S0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def S1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def s0(x): return rotr(x, 7) ^ rotr(x, 18) ^ (x >> np.uint32(3))
def s1(x): return rotr(x, 17) ^ rotr(x, 19) ^ (x >> np.uint32(10))
def IF(x, y, z): return (x & y) ^ (~x & z)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def parse_rows(path):
    rows = {}
    for line in open(path):
        p = line.split()
        if len(p) == 4 and re.fullmatch(r"\d+", p[0]):
            rows[int(p[0])] = p[1:]
        elif len(p) == 4 and re.fullmatch(r"\d+-\d+", p[0]):
            lo, hi = map(int, p[0].split("-"))
            for i in range(lo, hi + 1):
                rows[i] = p[1:]
    return rows

class Rows:
    def __init__(self, path):
        self.r = parse_rows(path)
    def sym(self, col, i):
        return self.r.get(i, ["=" * 32] * 3)["AEW".index(col)]
    def fl(self, col, i):
        return np.uint32(sum(1 << (31 - k) for k, c in enumerate(self.sym(col, i)) if c in "nu"))
    def signed(self, col, i):
        v = 0
        for k, c in enumerate(self.sym(col, i)):
            if c == "n": v += 1 << (31 - k)
            elif c == "u": v -= 1 << (31 - k)
        return np.uint32(v & 0xFFFFFFFF)
    def fixmask(self, col, i):
        """(mask, value) of the bits a row fixes in the unprimed word (0/n -> 0, 1/u -> 1)."""
        m = v = 0
        for k, c in enumerate(self.sym(col, i)):
            if c in "01nu":
                m |= 1 << (31 - k)
                if c in "1u": v |= 1 << (31 - k)
        return np.uint32(m), np.uint32(v)
    def signmask(self, col, i):
        """(mask, value) of the n/u bits only (the sign of each difference)."""
        m = v = 0
        for k, c in enumerate(self.sym(col, i)):
            if c in "nu":
                m |= 1 << (31 - k)
                if c == "u": v |= 1 << (31 - k)
        return np.uint32(m), np.uint32(v)

ADVICE_A = dict(zip(range(4, 14), [0x98560dbb, 0x633b16ba, 0x9bcf7bbe, 0xf8677ad6, 0x4a299906, 0x44f24ab5, 0x39781650,
                                   0x6422edc8, 0x574542b8, 0x0508c8f0]))
ADVICE_E = dict(zip(range(8, 14), [0xf1cae594, 0xd0e1b7b4, 0xbf27d74c, 0xb78bbfd9, 0x3fffd0f9, 0xbf81c0f4]))
ADVICE_W = {12: 0x41b22a2c, 13: 0x6d12f88a}

def bit(x, j): return (x >> np.uint32(j)) & np.uint32(1)

class SecondBlock:
    def __init__(self, rows_path):
        R = self.R = Rows(rows_path)
        self.A = {i: np.uint32(v) for i, v in ADVICE_A.items()}
        self.E = {i: np.uint32(v) for i, v in ADVICE_E.items()}
        self.Ap = {i: v ^ R.fl("A", i) for i, v in self.A.items()}
        self.Ep = {i: v ^ R.fl("E", i) for i, v in self.E.items()}
        self.W12, self.W13 = np.uint32(ADVICE_W[12]), np.uint32(ADVICE_W[13])
        self.W12p, self.W13p = self.W12 ^ R.fl("W", 12), self.W13 ^ R.fl("W", 13)

    def p4(self):
        """The real P4 list: E14, A14, E15, A15 (both sides), W14, W15."""
        R, A, E, Ap, Ep = self.R, self.A, self.E, self.Ap, self.Ep
        fm, fv = R.fixmask("E", 14)
        free = [31 - k for k, c in enumerate(R.sym("E", 14)) if c == "="]
        n = 1 << len(free)
        idx = np.arange(n, dtype=np.uint64)
        e14 = np.full(n, fv, dtype=np.uint32)
        for t, j in enumerate(free):
            e14 |= (((idx >> np.uint64(t)) & np.uint64(1)).astype(np.uint32) << np.uint32(j))
        a14 = e14 - A[10] + S0(A[13]) + MAJ(A[13], A[12], A[11])
        am, av = R.fixmask("A", 14)
        ok = (a14 & am) == av
        ok &= bit(a14, 9) == bit(a14, 20)
        ok &= (bit(a14, 18) != bit(a14, 6)) & (bit(a14, 8) != bit(a14, 17))
        for j in (30, 25, 23):
            ok &= bit(A[13], j) == bit(a14, j)
        ok &= bit(A[13], 15) != bit(a14, 15)
        e14, a14 = e14[ok], a14[ok]
        fm15, fv15 = R.fixmask("E", 15)
        free15 = [31 - k for k, c in enumerate(R.sym("E", 15)) if c == "="]
        n15 = 1 << len(free15)
        idx = np.arange(n15, dtype=np.uint64)
        e15b = np.full(n15, fv15, dtype=np.uint32)
        for t, j in enumerate(free15):
            e15b |= (((idx >> np.uint64(t)) & np.uint64(1)).astype(np.uint32) << np.uint32(j))
        out = []
        for x14, y14 in zip(e14, a14):
            e15 = e15b
            a15 = e15 - A[11] + S0(y14) + MAJ(y14, A[13], A[12])
            okk = bit(A[13], 29) != bit(a15, 29)
            am15, av15 = R.fixmask("A", 15)
            okk &= (a15 & am15) == av15
            w14 = x14 - A[10] - E[10] - S1(E[13]) - IF(E[13], E[12], E[11]) - K[14]
            w15 = e15 - A[11] - E[11] - S1(x14) - IF(x14, E[13], E[12]) - K[15]
            x14p = Ap[10] + Ep[10] + S1(Ep[13]) + IF(Ep[13], Ep[12], Ep[11]) + K[14] + w14
            y14p = x14p - Ap[10] + S0(Ap[13]) + MAJ(Ap[13], Ap[12], Ap[11])
            c14 = ((x14p ^ x14) == R.fl("E", 14)) & ((y14p ^ y14) == R.fl("A", 14))
            if not c14:
                continue
            e15p = Ap[11] + Ep[11] + S1(x14p) + IF(x14p, Ep[13], Ep[12]) + K[15] + w15
            a15p = e15p - Ap[11] + S0(y14p) + MAJ(y14p, Ap[13], Ap[12])
            okk &= ((e15p ^ e15) == R.fl("E", 15)) & ((a15p ^ a15) == R.fl("A", 15))
            k = int(okk.sum())
            if k:
                sel = okk
                out.append(np.stack([np.full(k, x14), np.full(k, y14), np.full(k, x14p), np.full(k, y14p),
                                     e15[sel], a15[sel], e15p[sel], a15p[sel], np.full(k, w14), w15[sel]], axis=1))
        return np.concatenate(out, axis=0) if out else np.zeros((0, 10), dtype=np.uint32)

    def step(self, a4, e4, a1, a2, a3, e1, e2, e3, w, i):
        """One SHA-256 step from A[i-4], E[i-4], A[i-1..i-3], E[i-1..i-3] and W[i]: returns (A[i], E[i])."""
        e = a4 + e4 + S1(e1) + IF(e1, e2, e3) + K[i] + w
        a = e - a4 + S0(a1) + MAJ(a1, a2, a3)
        return a, e

    def stage_ok(self, i, a, ap, e, ep):
        R = self.R
        return ((a ^ ap) == R.fl("A", i)) & ((e ^ ep) == R.fl("E", i))
```

### A.18 `step3ref.py`

```python
"""Reference (scalar Python) evaluation of Step-3 stages 16..31 from (P4 entry, W16..W19, tuple constants)."""
import sys
sys.argv = ['x', 'fig6_rows_296.txt']
src = open('check_route.py').read().split('\nif __name__ == "__main__":')[0]
ref = {}
exec(src, ref)
M = 0xFFFFFFFF
S0, S1, s0, s1, IF, MAJ, K = ref['S0'], ref['S1'], ref['s0'], ref['s1'], ref['IF'], ref['MAJ'], ref['K']
rows = ref['parse_rows']('fig6_rows_296.txt')
R = lambda col, i: rows.get(i, ['=' * 32] * 3)['AEW'.index(col)]
fl = lambda col, i: sum(1 << (31 - k) for k, c in enumerate(R(col, i)) if c in 'nu')
def signed(col, i):
    v = 0
    for k, c in enumerate(R(col, i)):
        if c == 'n': v += 1 << (31 - k)
        elif c == 'u': v -= 1 << (31 - k)
    return v & M
def sign_ok(col, i, x):
    for k, c in enumerate(R(col, i)):
        b = (x >> (31 - k)) & 1
        if c == 'n' and b != 0: return False
        if c == 'u' and b != 1: return False
    return True
ADV_A = dict(zip(range(4, 14), [0x98560dbb, 0x633b16ba, 0x9bcf7bbe, 0xf8677ad6, 0x4a299906, 0x44f24ab5, 0x39781650, 0x6422edc8, 0x574542b8, 0x0508c8f0]))
ADV_E = dict(zip(range(8, 14), [0xf1cae594, 0xd0e1b7b4, 0xbf27d74c, 0xb78bbfd9, 0x3fffd0f9, 0xbf81c0f4]))
W12, W13 = 0x41b22a2c, 0x6d12f88a

def stages(entry, w16_19, tup):
    """entry = (E14, A14, E14', A14', E15, A15, E15', A15', W14, W15); tup = dict c20, c20p, c21, c21p, c22, c22p, dW8 (W8'-W8),
    dW13 (W13'-W13). Returns the list of stages 16..31 that pass, stopping at the first failure."""
    A = dict(ADV_A); E = dict(ADV_E)
    Ap = {i: v ^ fl('A', i) for i, v in A.items()}; Ep = {i: v ^ fl('E', i) for i, v in E.items()}
    E[14], A[14], Ep[14], Ap[14], E[15], A[15], Ep[15], Ap[15], W14, W15 = entry
    W = {14: W14, 15: W15}; Wp = {14: W14, 15: W15}
    for i, w in zip(range(16, 20), w16_19):
        W[i] = Wp[i] = w
    passed = []
    for i in range(16, 23):
        if i == 20:
            W[20] = (s1(W[18]) + tup['c20']) & M; Wp[20] = (s1(Wp[18]) + tup['c20p']) & M
        if i == 21:
            W[21] = (s1(W[19]) + W14 + tup['c21']) & M; Wp[21] = (s1(Wp[19]) + W14 + tup['c21p']) & M
        if i == 22:
            W[22] = (s1(W[20]) + W15 + tup['c22']) & M; Wp[22] = (s1(Wp[20]) + W15 + tup['c22p']) & M
        for (AA, EE, WW) in ((A, E, W), (Ap, Ep, Wp)):
            EE[i] = (AA[i - 4] + EE[i - 4] + S1(EE[i - 1]) + IF(EE[i - 1], EE[i - 2], EE[i - 3]) + K[i] + WW[i]) & M
            AA[i] = (EE[i] - AA[i - 4] + S0(AA[i - 1]) + MAJ(AA[i - 1], AA[i - 2], AA[i - 3])) & M
        ok = (Wp[i] == W[i] ^ fl('W', i)) and (Ap[i] == A[i] ^ fl('A', i)) and (Ep[i] == E[i] ^ fl('E', i))
        if i in (20, 22): ok = ok and sign_ok('W', i, W[i])
        if not ok: return passed
        passed.append(i)
    # stages 23..31: schedule differences must vanish
    dW = {i: (Wp[i] - W[i]) & M for i in range(14, 23)}
    # W24 = s1(W22) + W17 + s0(W9) + W8: difference s1(W22') - s1(W22) + (W8' - W8)
    d24 = (s1(Wp[22]) - s1(W[22]) + tup['dW8']) & M
    # W27 = s1(W25) + W20 + s0(W12) + W11: difference (W20' - W20) + s0(W12') - s0(W12)
    d27 = (dW[20] + s0(W12 ^ fl('W', 12)) - s0(W12)) & M
    # W28 = s1(W26) + W21 + s0(W13) + W12: difference s0(W13') - s0(W13) + (W12' - W12)
    d28 = (s0(W13 ^ fl('W', 13)) - s0(W13) + ((W12 ^ fl('W', 12)) - W12)) & M
    # W29 = s1(W27) + W22 + s0(W14) + W13: difference (W22' - W22) + (W13' - W13)
    d29 = (dW[22] + tup['dW13']) & M
    for i, d in ((23, 0), (24, d24), (25, 0), (26, 0), (27, d27), (28, d28), (29, d29), (30, 0), (31, 0)):
        if d != 0: return passed
        passed.append(i)
    return passed

def tuple_consts(Wu, Wpu):
    """Tuple constants from unprimed and primed W0..W15."""
    c = lambda X: dict(c20=(X[13] + s0(X[5]) + X[4]) & M, c21=(s0(X[6]) + X[5]) & M, c22=(s0(X[7]) + X[6]) & M,
                       b16=(X[9] + s0(X[1]) + X[0]) & M, b17=(X[10] + s0(X[2]) + X[1]) & M,
                       b18=(X[11] + s0(X[3]) + X[2]) & M, b19=(X[12] + s0(X[4]) + X[3]) & M)
    u, p = c(Wu), c(Wpu)
    return dict(c20=u['c20'], c20p=p['c20'], c21=u['c21'], c21p=p['c21'], c22=u['c22'], c22p=p['c22'],
                b=[u['b16'], u['b17'], u['b18'], u['b19']], bp=[p['b16'], p['b17'], p['b18'], p['b19']],
                dW8=(Wpu[8] - Wu[8]) & M, dW13=(Wpu[13] - Wu[13]) & M)

if __name__ == '__main__':
    cv1 = ref['compress'](ref['IV'], ref['M0'], 35)
    Au, Eu, Wu = ref['trace'](cv1, ref['M1P'], 32)
    Ap_, Ep_, Wp_ = ref['trace'](cv1, ref['M1'], 32)
    t = tuple_consts(Wu[:16], Wp_[:16])
    print('b == b primed:', t['b'] == t['bp'], '| c21 == c21p:', t['c21'] == t['c21p'],
          '| c20p - c20 == D(W20):', (t['c20p'] - t['c20']) & M == signed('W', 20))
    w16 = [(s1(Wu[i - 2]) + t['b'][i - 16]) & M for i in range(16, 20)]
    print('W16..W19 from constants match trace:', w16 == Wu[16:20])
    entry = (Eu[14], Au[14], Ep_[14], Ap_[14], Eu[15], Au[15], Ep_[15], Ap_[15], Wu[14], Wu[15])
    print('stages passed for S:', stages(entry, w16, t))
```

### A.19 `check_route.py`

```python
"""Participant checks of the published CRYPTO 2026 (ePrint 2026/1080) 35-step SHA-256 pair
against the Fig. 6 characteristic transcription used by the package, and of the 32-step truncation.

Run: python3 check_route.py fig6_rows_296.txt twobit_296.txt [official-repo-path]
"""
import re
import struct
import sys

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
MASK = 0xFFFFFFFF


def rotr(x, r):
    return ((x >> r) | (x << (32 - r))) & MASK


def S0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def S1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def s0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def IF(x, y, z):
    return (x & y) ^ (~x & z & MASK)


def MAJ(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def expand(m, steps):
    w = list(m)
    for i in range(16, steps):
        w.append((s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & MASK)
    return w


def trace(cv, m, steps):
    """Return dicts A, E (indices -4..steps-1) and W (0..steps-1)."""
    w = expand(m, steps)
    a, b, c, d, e, f, g, h = cv
    A = {-1: a, -2: b, -3: c, -4: d}
    E = {-1: e, -2: f, -3: g, -4: h}
    for i in range(steps):
        E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + K[i] + w[i]) & MASK
        A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & MASK
    return A, E, w


def compress(cv, m, steps):
    A, E, _ = trace(cv, m, steps)
    r = steps
    out = [A[r - 1], A[r - 2], A[r - 3], A[r - 4], E[r - 1], E[r - 2], E[r - 3], E[r - 4]]
    return [(x + y) & MASK for x, y in zip(cv, out)]


def digest(msg, steps):
    ml = len(msg) * 8
    padded = msg + b"\x80" + b"\x00" * ((55 - len(msg)) % 64) + struct.pack(">Q", ml)
    cv = IV
    for off in range(0, len(padded), 64):
        cv = compress(cv, list(struct.unpack(">16I", padded[off:off + 64])), steps)
    return b"".join(struct.pack(">I", x) for x in cv)


def words(s):
    return [int(x, 16) for x in s.split()]


M0 = words("a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a "
           "cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8")
M1 = words("c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665 "
           "6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1")
M1P = words("c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef "
            "6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1")
HASH35 = "c6209b2b5e3fd4c896087364046304abbbc6dad9403a26d1018e351fe444451f"


def tobytes(ws):
    return b"".join(struct.pack(">I", x) for x in ws)


def parse_rows(path):
    rows = {}
    for line in open(path):
        parts = line.split()
        if len(parts) == 4 and re.fullmatch(r"\d+", parts[0]):
            rows[int(parts[0])] = parts[1:]
        elif len(parts) == 4 and re.fullmatch(r"\d+-\d+", parts[0]):
            lo, hi = map(int, parts[0].split("-"))
            for i in range(lo, hi + 1):
                rows[i] = parts[1:]
    return rows


def check_symbol(sym, x, xp):
    """x = unprimed value bit, xp = primed value bit."""
    if sym == "=":
        return x == xp
    if sym == "0":
        return x == xp == 0
    if sym == "1":
        return x == xp == 1
    if sym == "n":
        return x == 0 and xp == 1
    if sym == "u":
        return x == 1 and xp == 0
    raise ValueError(sym)


def main():
    rows_path, twobit_path = sys.argv[1], sys.argv[2]
    m_a = tobytes(M0 + M1)
    m_b = tobytes(M0 + M1P)
    d35a, d35b = digest(m_a, 35), digest(m_b, 35)
    cv1 = compress(IV, M0, 35)
    h2 = tobytes(compress(cv1, M1, 35)).hex()
    print("35-step digests equal:", d35a == d35b, "| Table 3 hash equals full digest:", d35a.hex() == HASH35,
          "| equals second-block chaining value:", h2 == HASH35)
    for r in (31, 32, 64):
        print(f"{r}-step digests equal:", digest(m_a, r) == digest(m_b, r))
    if len(sys.argv) > 3:
        sys.path.insert(0, sys.argv[3])
        from verifier.hash_functions import digest as off_digest
        print("official digest agrees (35, 32, 64):",
              all(off_digest(m, "sha256", r) == digest(m, r) for m in (m_a, m_b) for r in (35, 32, 64)))

    cv1 = compress(IV, M0, 35)
    print("CV1 = C_35(IV,M0) =", " ".join(f"{x:08x}" for x in cv1))
    print("second block, C_32 from that CV1, M1 vs M1' equal:", compress(cv1, M1, 32) == compress(cv1, M1P, 32))
    print("second block, C_35 from that CV1, M1 vs M1' equal:", compress(cv1, M1, 35) == compress(cv1, M1P, 35))

    rows = parse_rows(rows_path)
    best = None
    for name, (U, P) in {"unprimed=M1'": (M1P, M1), "unprimed=M1": (M1, M1P)}.items():
        Au, Eu, Wu = trace(cv1, U, 35)
        Ap, Ep, Wp = trace(cv1, P, 35)
        bad, nu, fixed = 0, 0, 0
        for i in range(-4, 35):
            sym = rows.get(i, ["=" * 32] * 3)
            for col, (xu, xp) in enumerate(((Au[i], Ap[i]), (Eu[i], Ep[i]),
                                            (Wu[i] if i >= 0 else 0, Wp[i] if i >= 0 else 0))):
                s = sym[col]
                for k in range(32):
                    bit = 31 - k
                    ok = check_symbol(s[k], (xu >> bit) & 1, (xp >> bit) & 1)
                    bad += not ok
                    nu += s[k] in "nu"
                    fixed += s[k] in "01nu"
        print(f"[{name}] rows -4..34: n/u symbols {nu}, single-bit-valued symbols {fixed}, mismatches {bad}")
        if bad == 0:
            best = (Au, Eu, Wu)

    Au, Eu, Wu = best
    print("advice A4..A13 =", " ".join(f"{Au[i]:08x}" for i in range(4, 14)))
    print("advice E8..E13 =", " ".join(f"{Eu[i]:08x}" for i in range(8, 14)))
    print("advice W12, W13 =", f"{Wu[12]:08x} {Wu[13]:08x}")

    val = {"A": Au, "E": Eu, "W": Wu}
    text = open(twobit_path).read()
    conds = re.findall(r"([AEW])(\d+)\[([\d,]+)\](!?=)([AEW])(\d+)\[([\d,]+)\]", text)
    total, held, per = 0, 0, []
    for X, i, bits1, rel, Y, j, bits2 in conds:
        b1 = list(map(int, bits1.split(",")))
        b2 = list(map(int, bits2.split(",")))
        res = []
        for p, q in zip(b1, b2):
            x = (val[X][int(i)] >> p) & 1
            y = (val[Y][int(j)] >> q) & 1
            res.append((x == y) if rel == "=" else (x != y))
        total += len(res)
        held += sum(res)
        per.append((f"{X}{i}[{bits1}]{rel}{Y}{j}[{bits2}]", res))
    print(f"printed two-bit conditions: {total}, hold on pair as printed: {held}")
    for name, res in per:
        if not all(res):
            print("   not as printed:", name, res)
    a16 = trace(cv1, M1P, 35)[0][16]
    print("A15[29] vs A16[29] (misprint reading):", (Au[15] >> 29) & 1, (a16 >> 29) & 1,
          "A13[29]:", (Au[13] >> 29) & 1)
    print("E16[29] = E17[29] holds:", ((Eu[16] >> 29) & 1) == ((Eu[17] >> 29) & 1))


if __name__ == "__main__":
    main()


def fl(sym):
    """n/u mask of a row string (position k is bit 31-k)."""
    return sum(1 << (31 - k) for k, c in enumerate(sym) if c in "nu")


def signed(sym):
    """D(X) = sum over n of 2^j - sum over u of 2^j (primed minus unprimed, mod 2^32)."""
    v = 0
    for k, c in enumerate(sym):
        if c == "n":
            v += 1 << (31 - k)
        elif c == "u":
            v -= 1 << (31 - k)
    return v & MASK


def fix_ok(sym, x):
    for k, c in enumerate(sym):
        b = (x >> (31 - k)) & 1
        if c in "0n" and b != 0:
            return False
        if c in "1u" and b != 1:
            return False
    return True


def spec_checks(rows_path):
    rows = parse_rows(rows_path)
    R = lambda col, i: rows.get(i, ["=" * 32] * 3)[col]
    print("free '=' bits: E3 %d E4 %d E5 %d E6 %d E7 %d W7 %d E14 %d E15 %d" % tuple(
        R(c, i).count("=") for c, i in ((1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (1, 14), (1, 15))))
    cv1 = compress(IV, M0, 35)
    Au, Eu, Wu = trace(cv1, M1P, 35)
    # Step 2 from the record values (A0..A13, E3..E13, W7..W13) and CV1 only
    A = {i: Au[i] for i in range(0, 14)}
    E = {i: Eu[i] for i in range(3, 14)}
    a, b, c, d, e, f, g, h = cv1
    A.update({-1: a, -2: b, -3: c, -4: d})
    E.update({-1: e, -2: f, -3: g, -4: h})
    key_ok = A[-1] == (E[3] - A[3] + S0(A[2]) + MAJ(A[2], A[1], A[0])) & MASK
    for i in range(0, 3):
        E[i] = (A[i] + A[i - 4] - S0(A[i - 1]) - MAJ(A[i - 1], A[i - 2], A[i - 3])) & MASK
    W = {}
    for i in range(0, 7):
        W[i] = (E[i] - A[i - 4] - E[i - 4] - S1(E[i - 1]) - IF(E[i - 1], E[i - 2], E[i - 3]) - K[i]) & MASK
    print("Step 2 on published record: key A[-1] matches:", key_ok,
          "| W0..W6 reproduce M1':", [W[i] for i in range(7)] == M1P[:7])
    Wp = {i: W[i] ^ fl(R(2, i)) for i in range(7)}
    W12, W13 = Wu[12], Wu[13]
    W12p, W13p = W12 ^ fl(R(2, 12)), W13 ^ fl(R(2, 13))
    sgn = lambda i, x: fix_ok("".join(ch if ch in "nu" else "=" for ch in R(2, i)), x)
    t_a = sgn(4, W[4])
    t_b = (s0(Wp[4]) + W12p) & MASK == (s0(W[4]) + W12) & MASK
    t_c = sgn(5, W[5])
    t_d = sgn(6, W[6])
    # (e) conformance of the primed computation at steps 0..6 (E) and 0..2 (A), primed inputs xor FL
    Ap = {i: A[i] ^ fl(R(0, i)) for i in range(-4, 14)}
    Ep = {i: E[i] ^ fl(R(1, i)) for i in range(-4, 14)}
    t_e = True
    for i in range(0, 7):
        ei = (Ap[i - 4] + Ep[i - 4] + S1(Ep[i - 1]) + IF(Ep[i - 1], Ep[i - 2], Ep[i - 3]) + K[i] + Wp[i]) & MASK
        t_e &= ei == Ep[i]
        if i <= 2:
            ai = (Ep[i] - Ap[i - 4] + S0(Ap[i - 1]) + MAJ(Ap[i - 1], Ap[i - 2], Ap[i - 3])) & MASK
            t_e &= ai == Ap[i]
    t_f = (s0(Wp[6]) + Wp[5]) & MASK == (s0(W[6]) + W[5]) & MASK
    t_g = ((W13p - W13) + (s0(Wp[5]) - s0(W[5])) + (Wp[4] - W[4])) & MASK == signed(R(2, 20))
    print("Step 2 tests (a)..(g):", [t_a, t_b, t_c, t_d, t_e, t_f, t_g])
    # Step 3 for the published (W14, W15): stages 16..31
    m = [W[i] for i in range(7)] + [Wu[i] for i in range(7, 16)]
    mp = [x ^ fl(R(2, i)) for i, x in enumerate(m)]
    Aq, Eq, Wq = trace(cv1, m, 32)
    Ar, Er, Wr = trace(cv1, mp, 32)
    stage = []
    for i in range(16, 32):
        ok = Wr[i] == Wq[i] ^ fl(R(2, i))
        if i in (20, 22):
            ok &= sgn(i, Wq[i])
        if i <= 22:
            ok &= Ar[i] == Aq[i] ^ fl(R(0, i)) and Er[i] == Eq[i] ^ fl(R(1, i))
        stage.append(ok)
    print("Step 3 stages 16..31 pass for published (W14,W15):", all(stage))
    print("second blocks equal after C_32:", compress(cv1, m, 32) == compress(cv1, mp, 32))


spec_checks(sys.argv[1])
```

### A.20 `mkparams.py`

```python
"""Write params.h (advice states, masks) and p4.bin (the real P4 list) for condexp.c."""
import numpy as np, warnings
warnings.filterwarnings('ignore')
from secondblock import SecondBlock
from step3ref import fl, signed, R, s0, M
sb = SecondBlock('fig6_rows_296.txt')
P = sb.p4()
assert len(P) == 196608
P.astype('<u4').tofile('p4.bin')
def sm(col, i):
    m = v = 0
    for k, c in enumerate(R(col, i)):
        if c in 'nu':
            m |= 1 << (31 - k)
            if c == 'u': v |= 1 << (31 - k)
    return m, v
lines = ['/* generated by mkparams.py */']
for nm, d in (('A', sb.A), ('E', sb.E), ('AP', sb.Ap), ('EP', sb.Ep)):
    for i in (12, 13):
        lines.append(f'#define {nm}{i} 0x{int(d[i]):08x}u')
for i in range(16, 23):
    lines.append(f'#define FLA{i} 0x{fl("A", i):08x}u')
    lines.append(f'#define FLE{i} 0x{fl("E", i):08x}u')
for i in (20, 22):
    m, v = sm('W', i)
    lines.append(f'#define FLW{i} 0x{fl("W", i):08x}u')
    lines.append(f'#define SGM{i} 0x{m:08x}u')
    lines.append(f'#define SGV{i} 0x{v:08x}u')
open('params.h', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
```

### A.21 `gen_cvec.py`

```python
"""Tuple-constant vectors for condexp.c: S's own tuple first, then K-1 tuples with W4..W6 drawn uniformly subject to the
validity conditions that involve them (signs of W4..W6 and tests (b), (f), (g)); W7, W8 from S's record, W12, W13 advice.
usage: gen_cvec.py K seed > cvec.txt"""
import sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
ARGS = sys.argv[1:]
from step3ref import fl, signed, s0, M, ref, tuple_consts
K, seed = int(ARGS[0]), int(ARGS[1])
rng = np.random.default_rng(seed)
cv1 = ref['compress'](ref['IV'], ref['M0'], 35)
Au, Eu, Wu = ref['trace'](cv1, ref['M1P'], 32)
_, _, Wp = ref['trace'](cv1, ref['M1'], 32)
t = tuple_consts(Wu[:16], Wp[:16])
rows = [(t['c20'], t['c20p'], t['c21'], t['c22'], t['c22p'], t['dW8'], t['dW13'])]
def s0v(x): x = x.astype(np.uint32); return ((x >> 7) | (x << 25)) ^ ((x >> 18) | (x << 14)) ^ (x >> 3)
def sign_fix(i, x):
    m = v = 0
    for k, c in enumerate(ref['parse_rows']('fig6_rows_296.txt').get(i, ['=' * 32] * 3)[2]):
        if c in 'nu':
            m |= 1 << (31 - k)
            if c == 'u': v |= 1 << (31 - k)
    return (x & np.uint32(~m & M)) | np.uint32(v)
F4, F5, F6, F7 = (np.uint32(fl('W', i)) for i in (4, 5, 6, 7))
W12, W13 = np.uint32(Wu[12]), np.uint32(Wu[13])
W12p, W13p = W12 ^ np.uint32(fl('W', 12)), W13 ^ np.uint32(fl('W', 13))
D20 = np.uint32(signed('W', 20))
W7 = np.uint32(Wu[7]); W7p = W7 ^ F7
while len(rows) < K:
    n = 1 << 22
    w4 = sign_fix(4, rng.integers(0, 2**32, n, dtype=np.uint64).astype(np.uint32))
    w4 = w4[(s0v(w4 ^ F4) + W12p) == (s0v(w4) + W12)]
    w5 = sign_fix(5, rng.integers(0, 2**32, len(w4), dtype=np.uint64).astype(np.uint32))
    ok = ((W13p - W13) + (s0v(w5 ^ F5) - s0v(w5)) + ((w4 ^ F4) - w4)) == D20
    w4, w5 = w4[ok], w5[ok]
    w6 = sign_fix(6, rng.integers(0, 2**32, len(w4), dtype=np.uint64).astype(np.uint32))
    ok = (s0v(w6 ^ F6) + (w5 ^ F5)) == (s0v(w6) + w5)
    for a, b, c in zip(w4[ok], w5[ok], w6[ok]):
        if len(rows) >= K: break
        a, b, c = int(a), int(b), int(c)
        ap, bp, cp = a ^ int(F4), b ^ int(F5), c ^ int(F6)
        rows.append(((int(W13) + s0(b) + a) & M, (int(W13p) + s0(bp) + ap) & M, (s0(c) + b) & M,
                     (s0(int(W7)) + c) & M, (s0(int(W7p)) + cp) & M, t['dW8'], t['dW13']))
for r in rows:
    print(' '.join(f'{x:08x}' for x in r))
```

### A.22 `condexp.c`

```c
/* Step-3 stages of the sha256-r32 attack on the real P4 list, with W16..W19 uniform (their law under any Step-2
 * conditioning, proof Section 9.1), counting for each tuple-constant vector c = (c20, c20', c21, c22, c22', dW8, dW13)
 * how many sampled histories pass stages 20..31.
 *
 * Sampling: a uniform P4 entry and a uniform W16; each stage-16 survivor tries M17 uniform W17 (stage 17 is
 * decided before W17, so a failing prefix is dropped after one check), each stage-17 survivor M18 uniform W18, each
 * stage-18 survivor M19 uniform W19. Every history through step 19 then carries the
 * same weight 1 / (M17 * M18 * M19), so the counts estimate the pass probability of uniform (entry, W16..W19)
 * up to that common factor, for every c at once.
 *
 * usage: condexp p4.bin cvec.txt seed n16 M17 M18 M19
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "params.h"

#define ROTR(x, r) (((x) >> (r)) | ((x) << (32 - (r))))
#define BS0(x) (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define BS1(x) (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SS1(x) (ROTR(x, 17) ^ ROTR(x, 19) ^ ((x) >> 10))
#define IFF(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))

static const uint32_t K[32] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967};
static const uint32_t FLA[23] = {[16] = FLA16, [17] = FLA17, [18] = FLA18, [19] = FLA19, [20] = FLA20, [21] = FLA21, [22] = FLA22};
static const uint32_t FLE[23] = {[16] = FLE16, [17] = FLE17, [18] = FLE18, [19] = FLE19, [20] = FLE20, [21] = FLE21, [22] = FLE22};

static uint64_t s[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t next(void) {
    uint64_t r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45);
    return r;
}
static uint64_t splitmix(uint64_t *x) {
    uint64_t z = (*x += 0x9e3779b97f4a7c15ull);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull;
    return z ^ (z >> 31);
}

typedef struct { uint32_t A[23], E[23]; } side;   /* indices 12..22 used */

static inline void step(side *x, int i, uint32_t w) {
    x->E[i] = x->A[i - 4] + x->E[i - 4] + BS1(x->E[i - 1]) + IFF(x->E[i - 1], x->E[i - 2], x->E[i - 3]) + K[i] + w;
    x->A[i] = x->E[i] - x->A[i - 4] + BS0(x->A[i - 1]) + MAJ(x->A[i - 1], x->A[i - 2], x->A[i - 3]);
}
static inline int conf(const side *u, const side *p, int i) {
    return ((u->A[i] ^ p->A[i]) == FLA[i]) && ((u->E[i] ^ p->E[i]) == FLE[i]);
}

#define MAXC 1400
int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END); long nb = ftell(f); fseek(f, 0, SEEK_SET);
    int n4 = (int)(nb / 40);
    uint32_t *P = malloc(nb);
    if (fread(P, 1, nb, f) != (size_t)nb) return 2;
    fclose(f);
    uint32_t C[MAXC][7]; int nc = 0;
    f = fopen(argv[2], "r");
    while (nc < MAXC && fscanf(f, "%x %x %x %x %x %x %x", &C[nc][0], &C[nc][1], &C[nc][2], &C[nc][3], &C[nc][4],
                               &C[nc][5], &C[nc][6]) == 7) nc++;
    fclose(f);
    uint64_t seed = strtoull(argv[3], 0, 10), n16 = strtoull(argv[4], 0, 10);
    int M17 = atoi(argv[5]), M18 = atoi(argv[6]), M19 = atoi(argv[7]);
    for (int k = 0; k < 4; k++) s[k] = splitmix(&seed);
    uint64_t c16 = 0, c17 = 0, c18 = 0, c19 = 0, p20[MAXC] = {0}, p21[MAXC] = {0}, p22[MAXC] = {0}, pall[MAXC] = {0};
    side u0, p0;
    u0.A[12] = A12; u0.A[13] = A13; u0.E[12] = E12; u0.E[13] = E13;
    p0.A[12] = AP12; p0.A[13] = AP13; p0.E[12] = EP12; p0.E[13] = EP13;
    for (uint64_t t = 0; t < n16; t++) {
        uint64_t r = next();
        const uint32_t *e = P + 10 * (uint32_t)((r >> 32) % (uint64_t)n4);
        side u = u0, p = p0;
        u.E[14] = e[0]; u.A[14] = e[1]; p.E[14] = e[2]; p.A[14] = e[3];
        u.E[15] = e[4]; u.A[15] = e[5]; p.E[15] = e[6]; p.A[15] = e[7];
        uint32_t W14 = e[8], W15 = e[9];
        uint32_t W16 = (uint32_t)r;
        step(&u, 16, W16); step(&p, 16, W16);
        if (!conf(&u, &p, 16)) continue;
        c16++;
        {   /* stage 17 does not depend on W17: E17' - E17 and A17' - A17 are free of it and its pattern is 0 */
            side u17 = u, p17 = p;
            step(&u17, 17, 0); step(&p17, 17, 0);
            if (!conf(&u17, &p17, 17)) continue;
        }
        for (int j17 = 0; j17 < M17; j17++) {
            uint32_t W17 = (uint32_t)next();
            side u17 = u, p17 = p;
            step(&u17, 17, W17); step(&p17, 17, W17);
            if (!conf(&u17, &p17, 17)) continue;
            c17++;
            for (int j18 = 0; j18 < M18; j18++) {
                uint32_t W18 = (uint32_t)next();
                side u18 = u17, p18 = p17;
                step(&u18, 18, W18); step(&p18, 18, W18);
                if (!conf(&u18, &p18, 18)) continue;
                c18++;
                for (int j19 = 0; j19 < M19; j19++) {
                    uint32_t W19 = (uint32_t)next();
                    side u19 = u18, p19 = p18;
                    step(&u19, 19, W19); step(&p19, 19, W19);
                    if (!conf(&u19, &p19, 19)) continue;
                    c19++;
                    for (int c = 0; c < nc; c++) {
                        side a = u19, b = p19;
                        uint32_t W20 = SS1(W18) + C[c][0], W20p = SS1(W18) + C[c][1];
                        if ((W20 ^ W20p) != FLW20 || (W20 & SGM20) != SGV20) continue;
                        step(&a, 20, W20); step(&b, 20, W20p);
                        if (!conf(&a, &b, 20)) continue;
                        p20[c]++;
                        uint32_t W21 = SS1(W19) + W14 + C[c][2];
                        step(&a, 21, W21); step(&b, 21, W21);
                        if (!conf(&a, &b, 21)) continue;
                        p21[c]++;
                        uint32_t W22 = SS1(W20) + W15 + C[c][3], W22p = SS1(W20p) + W15 + C[c][4];
                        if ((W22 ^ W22p) != FLW22 || (W22 & SGM22) != SGV22) continue;
                        step(&a, 22, W22); step(&b, 22, W22p);
                        if (!conf(&a, &b, 22)) continue;
                        p22[c]++;
                        uint32_t d24 = SS1(W22p) - SS1(W22) + C[c][5], d29 = (W22p - W22) + C[c][6];
                        if (d24 == 0 && d29 == 0) pall[c]++;
                    }
                }
            }
        }
    }
    printf("n16 %llu c16 %llu c17 %llu c18 %llu c19 %llu M %d %d %d\n", (unsigned long long)n16,
           (unsigned long long)c16, (unsigned long long)c17, (unsigned long long)c18, (unsigned long long)c19, M17, M18, M19);
    for (int c = 0; c < nc; c++)
        printf("c %d %llu %llu %llu %llu\n", c, (unsigned long long)p20[c], (unsigned long long)p21[c],
               (unsigned long long)p22[c], (unsigned long long)pall[c]);
    return 0;
}
```

### A.23 `analyse.py`

```python
"""Sum condexp outputs and report the spread of the Step-3 pass rate over tuple constants.
usage: analyse.py out.0 out.1 ... > summary.json"""
import json, math, sys
tot = None; per = []
for path in sys.argv[1:]:
    lines = open(path).read().split('\n')
    h = lines[0].split()
    hd = dict(n16=int(h[1]), c16=int(h[3]), c17=int(h[5]), c18=int(h[7]), c19=int(h[9]), M=[int(h[11]), int(h[12]), int(h[13])])
    cs = [list(map(int, l.split()[2:6])) for l in lines[1:] if l.startswith('c ')]
    per.append((hd, cs))
K = len(per[0][1])
H = {k: sum(p[0][k] for p in per) for k in ('n16', 'c16', 'c17', 'c18', 'c19')}
M17, M18, M19 = per[0][0]['M']
cnt = [[sum(p[1][c][j] for p in per) for j in range(4)] for c in range(K)]
allp = [x[3] for x in cnt]
mean = sum(allp) / K
# standard error of each per-c count from the spread between independent processes
nproc = len(per)
def se(c):
    xs = [p[1][c][3] for p in per]
    m = sum(xs) / nproc
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (nproc - 1) * nproc) if nproc > 1 else math.sqrt(max(allp[c], 1))
out = dict(processes=nproc, K=K, M=[M17, M18, M19], histories=H['c19'],
           rate16=H['c16'] / H['n16'], rate17_prefix=(H['c17'] / M17) / H['c16'], rate18=H['c18'] / (H['c17'] * M18),
           rate19=H['c19'] / (H['c18'] * M19),
           log2_through19=math.log2(H['c16'] / H['n16']) + math.log2((H['c17'] / M17) / H['c16']) +
                          math.log2(H['c18'] / (H['c17'] * M18)) + math.log2(H['c19'] / (H['c18'] * M19)),
           stage20=[x[0] for x in cnt], stage21=[x[1] for x in cnt], stage22=[x[2] for x in cnt], allpass=allp,
           allpass_mean=mean, allpass_se=[round(se(c), 1) for c in range(K)],
           max_over_mean=max(allp) / mean, min_over_mean=min(allp) / mean,
           own_tuple_over_mean=allp[0] / mean,
           stage20_max_over_mean=max(x[0] for x in cnt) / (sum(x[0] for x in cnt) / K),
           log2_after19=math.log2(mean / H['c19']) if mean else None)
srt = sorted(range(K), key=lambda c: -allp[c])
out['top5'] = [(c, allp[c], round(se(c), 1)) for c in srt[:5]]
# upper bound on max/mean: largest count plus two standard errors, over the mean
out['max_over_mean_upper'] = (allp[srt[0]] + 2 * se(srt[0])) / mean
print(json.dumps(out, indent=1))
```

### A.24 `table.py`

```python
"""Real TAB2 records for a key slice (proof Section 4): P1, P2, P3 with every stated predicate, vectorised.

usage: table.py SLICE_BITS SLICE_VALUE NPROC OUT.npz
Writes the combinations, the pairs, and every record whose key has its top SLICE_BITS bits equal to SLICE_VALUE.
"""
import sys, time, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings('ignore')
from secondblock import Rows, S0, S1, s0, IF, MAJ, K, ADVICE_A, ADVICE_E, ADVICE_W

R = Rows('fig6_rows_296.txt')
u = lambda v: np.uint32(v)
A = {i: u(v) for i, v in ADVICE_A.items()}
E = {i: u(v) for i, v in ADVICE_E.items()}
Ap = {i: v ^ R.fl('A', i) for i, v in A.items()}
Ep = {i: v ^ R.fl('E', i) for i, v in E.items()}
W12, W13 = u(ADVICE_W[12]), u(ADVICE_W[13])
W12p, W13p = W12 ^ R.fl('W', 12), W13 ^ R.fl('W', 13)
def bit(x, j): return (x >> np.uint32(j)) & np.uint32(1)
def fixed_values(col, i):
    """All unprimed words that satisfy row i's fixed bits (enumerating its '=' bits)."""
    m, v = R.fixmask(col, i)
    free = [31 - k for k, c in enumerate(R.sym(col, i)) if c == '=']
    idx = np.arange(1 << len(free), dtype=np.uint64)
    x = np.full(len(idx), v, dtype=np.uint32)
    for t, j in enumerate(free):
        x |= (((idx >> np.uint64(t)) & np.uint64(1)).astype(np.uint32) << np.uint32(j))
    return x
def fix_ok(col, i, x):
    m, v = R.fixmask(col, i)
    return (x & m) == v

def p1():
    e4 = fixed_values('E', 4)
    L4 = e4[bit(e4, 10) != bit(e4, 15)]
    w7 = fixed_values('W', 7)
    ok = (bit(w7, 22) != bit(w7, 18)) & (bit(w7, 13) != bit(w7, 9)) & (bit(w7, 23) != bit(w7, 8))
    ok &= (bit(w7, 11) == bit(w7, 22)) & (bit(w7, 14) == bit(w7, 31)) & (bit(w7, 20) == bit(w7, 31))
    return L4, w7[ok]

def p2():
    e7 = fixed_values('E', 7)
    e7 = e7[(bit(e7, 21) == bit(e7, 3)) & (bit(e7, 10) == bit(e7, 15))]      # E7[21,10] = E7[3,15] (reading)
    a3 = e7 - A[7] + S0(A[6]) + MAJ(A[6], A[5], A[4])                         # backward A form at step 7
    ok = fix_ok('A', 3, a3) & (bit(a3, 29) != bit(A[5], 29))
    for j in (26, 4): ok &= bit(a3, j) == bit(A[4], j)
    for j in (22, 18, 16, 11, 7): ok &= bit(a3, j) != bit(A[4], j)
    e7, a3 = e7[ok], a3[ok]
    e6all = fixed_values('E', 6)
    ok6 = (bit(e6all, 9) != bit(e6all, 23)) & (bit(e6all, 27) != bit(e6all, 14)) & (bit(e6all, 9) != bit(e6all, 14))
    ok6 &= bit(e6all, 8) != bit(e6all, 27)
    ok6 &= (bit(e6all, 1) == bit(e6all, 6)) & (bit(e6all, 1) == bit(e6all, 15)) & (bit(e6all, 23) == bit(e6all, 10))
    ok6 &= bit(e6all, 6) == bit(e6all, 25)
    e6all = e6all[ok6]
    e5all = fixed_values('E', 5)
    e5all = e5all[(bit(e5all, 3) == bit(e5all, 8)) & (bit(e5all, 21) == bit(e5all, 8))]
    out = []
    for x7, y3 in zip(e7, a3):
        a2 = e6all - A[6] + S0(A[5]) + MAJ(A[5], A[4], y3)                    # step 6
        k = fix_ok('A', 2, a2) & (bit(y3, 29) == bit(a2, 29))
        for x6, y2 in zip(e6all[k], a2[k]):
            e5 = e5all
            a1 = e5 - A[5] + S0(A[4]) + MAJ(A[4], y3, y2)                       # step 5
            ok = fix_ok('A', 1, a1)
            if not ok.any(): continue
            e5, a1 = e5[ok], a1[ok]
            n = len(e5)
            x7v, x6v, y3v, y2v = (np.full(n, z) for z in (x7, x6, y3, y2))
            w9 = E[9] - A[5] - e5 - S1(E[8]) - IF(E[8], x7v, x6v) - K[9]
            w10 = E[10] - A[6] - x6v - S1(E[9]) - IF(E[9], E[8], x7v) - K[10]
            w11 = E[11] - A[7] - x7v - S1(E[10]) - IF(E[10], E[9], E[8]) - K[11]
            # primed values: X xor FL(row X)
            PA = {1: a1 ^ R.fl('A', 1), 2: y2v ^ R.fl('A', 2), 3: y3v ^ R.fl('A', 3)}
            PA.update({i: np.full(n, Ap[i]) for i in range(4, 14)})
            PE = {5: e5 ^ R.fl('E', 5), 6: x6v ^ R.fl('E', 6), 7: x7v ^ R.fl('E', 7)}
            PE.update({i: np.full(n, Ep[i]) for i in range(8, 14)})
            PW = {9: w9, 10: w10, 11: w11, 12: np.full(n, W12p), 13: np.full(n, W13p)}
            ok = np.ones(n, dtype=bool)
            for i in range(5, 14):                                              # A conformant at steps 5..13
                ai = PE[i] - PA[i - 4] + S0(PA[i - 1]) + MAJ(PA[i - 1], PA[i - 2], PA[i - 3])
                ok &= ai == PA[i]
            for i in range(9, 14):                                              # E conformant at steps 9..13
                ei = PA[i - 4] + PE[i - 4] + S1(PE[i - 1]) + IF(PE[i - 1], PE[i - 2], PE[i - 3]) + K[i] + PW[i]
                ok &= ei == PE[i]
            if ok.any():
                out.append(np.stack([e5[ok], x6v[ok], x7v[ok], a1[ok], y2v[ok], y3v[ok], w9[ok], w10[ok], w11[ok]], axis=1))
    return np.concatenate(out)

def p3_pairs(comb, L4):
    out = []
    for ci, (e5, e6, e7, a1, a2, a3, w9, w10, w11) in enumerate(comb):
        e4 = L4
        a0 = e4 - A[4] + S0(a3) + MAJ(a3, a2, a1)                               # step 4
        w8 = E[8] - A[4] - e4 - S1(e7) - IF(e7, e6, e5) - K[8]
        ok = fix_ok('A', 0, a0) & fix_ok('W', 8, w8)
        ok &= (bit(w8, 0) == bit(w8, 28)) & (bit(w8, 14) == bit(w8, 25)) & (bit(w8, 21) == bit(w8, 6))
        for p, q in ((31, 27), (23, 2), (30, 15), (15, 26), (22, 7), (8, 4)):
            ok &= bit(w8, p) != bit(w8, q)
        e4p = e4 ^ R.fl('E', 4)
        a0p, a1p, a2p, a3p = a0 ^ R.fl('A', 0), a1 ^ R.fl('A', 1), a2 ^ R.fl('A', 2), a3 ^ R.fl('A', 3)
        a4c = e4p - a0p + S0(a3p) + MAJ(a3p, a2p, a1p)                            # A conformant at step 4
        ok &= a4c == Ap[4]
        w8p = w8 ^ R.fl('W', 8)
        e5p, e6p, e7p = e5 ^ R.fl('E', 5), e6 ^ R.fl('E', 6), e7 ^ R.fl('E', 7)
        e8c = Ap[4] + e4p + S1(e7p) + IF(e7p, e6p, e5p) + K[8] + w8p                # E conformant at step 8
        ok &= e8c == Ep[8]
        k = int(ok.sum())
        if k:
            out.append(np.stack([np.full(k, ci, dtype=np.uint32), e4[ok], a0[ok], w8[ok]], axis=1))
    return np.concatenate(out)

G = {}
def w7_job(rng):
    comb, pairs, L7, sbits, sval = G['comb'], G['pairs'], G['L7'], G['sbits'], G['sval']
    out = []
    cnt = 0
    for pi in range(*rng):
        ci, e4, a0, w8 = pairs[pi]
        e5, e6, e7, a1, a2, a3 = comb[ci][:6]
        w7 = L7
        e3 = e7 - a3 - w7 - S1(e6) - IF(e6, e5, e4) - K[7]                       # W form at step 7 solved for E3
        key = e3 - a3 + S0(a2) + MAJ(a2, a1, a0)                                  # backward A form at step 3
        ok = fix_ok('E', 3, e3)
        w7p, w8p = w7 ^ R.fl('W', 7), w8 ^ R.fl('W', 8)
        ok &= (s0(w8p) + w7p) == (s0(w8) + w7)
        e3p = e3 ^ R.fl('E', 3)
        a3p = a3 ^ R.fl('A', 3)
        e4p, e5p, e6p, e7p = e4 ^ R.fl('E', 4), e5 ^ R.fl('E', 5), e6 ^ R.fl('E', 6), e7 ^ R.fl('E', 7)
        e7c = a3p + e3p + S1(e6p) + IF(e6p, e5p, e4p) + K[7] + w7p                 # E conformant at step 7
        ok &= e7c == e7p
        a3c = e3p - key + S0(a2 ^ R.fl('A', 2)) + MAJ(a2 ^ R.fl('A', 2), a1 ^ R.fl('A', 1), a0 ^ R.fl('A', 0))
        ok &= a3c == a3p                                                           # A conformant at step 3
        cnt += int(ok.sum())
        ok &= (key >> np.uint32(32 - sbits)) == np.uint32(sval)
        k = int(ok.sum())
        if k:
            out.append(np.stack([np.full(k, pi, dtype=np.uint32), w7[ok], e3[ok], key[ok]], axis=1))
    return (np.concatenate(out) if out else np.zeros((0, 4), dtype=np.uint32)), cnt

def init(comb, pairs, L7, sbits, sval):
    G.update(comb=comb, pairs=pairs, L7=L7, sbits=sbits, sval=sval)

if __name__ == '__main__':
    sbits, sval, nproc, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    t = time.time()
    L4, L7 = p1(); print('|L4|', len(L4), '|L7|', len(L7), flush=True)
    comb = p2(); print('combinations', len(comb), round(time.time() - t), 's', flush=True)
    pairs = p3_pairs(comb, L4); print('pairs', len(pairs), round(time.time() - t), 's', flush=True)
    n = len(pairs); step = (n + 4 * nproc - 1) // (4 * nproc)
    with Pool(nproc, initializer=init, initargs=(comb, pairs, L7, sbits, sval)) as pool:
        res = pool.map(w7_job, [(i, min(i + step, n)) for i in range(0, n, step)])
    recs = np.concatenate([r for r, _ in res]); N = sum(c for _, c in res)
    print('records (all keys)', N, '| in slice', len(recs), round(time.time() - t), 's', flush=True)
    np.savez(outp, comb=comb, pairs=pairs, recs=recs, L4=L4, L7=L7, N=N)
```

### A.25 `pairexp.py`

```python
"""Direct conditioned experiment on real TAB2 records: trials in which two records of one key class are both valid.

For a record t, CV1[1..3] -> (E0, E1, E2) -> (W4, W5, W6) is a bijection (Section 9.1), so a uniform CV1 conditioned
on "t valid" is a uniform (W4, W5, W6) passing t's Step-2 tests. We sample those, map back to CV1[1..3], and run the
Step-2 tests (a)-(g) of every other record of the same key class on the same CV1. Each trial in which some other
record t' is also valid is a pair event. For every pair event we keep t's tuple constants, and for the same record t
a tuple drawn from an independent single event; condexp.c then compares the Step-3 pass rates of the two sets.

usage: pairexp.py slice.npz seed max_pairs out_prefix
"""
import sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
from secondblock import Rows, S0, S1, s0, IF, MAJ, K, ADVICE_A, ADVICE_W

R = Rows('fig6_rows_296.txt')
u = np.uint32
W12, W13 = u(ADVICE_W[12]), u(ADVICE_W[13])
W12p, W13p = W12 ^ R.fl('W', 12), W13 ^ R.fl('W', 13)
D20 = R.signed('W', 20)
FL = {i: R.fl('W', i) for i in range(4, 9)}
FE = {i: R.fl('E', i) for i in range(3, 7)}
SG = {i: R.signmask('W', i) for i in (4, 5, 6)}

def w_tests(w4, w5, w6):
    """Tests (a)-(d), (f), (g): they involve only W4..W6 (and the advice W12, W13)."""
    ok = np.ones(len(w4), dtype=bool)
    for i, w in ((4, w4), (5, w5), (6, w6)):
        m, v = SG[i]
        ok &= (w & m) == v
    p4, p5, p6 = w4 ^ FL[4], w5 ^ FL[5], w6 ^ FL[6]
    ok &= (s0(p4) + W12p) == (s0(w4) + W12)
    ok &= (s0(p6) + p5) == (s0(w6) + w5)
    ok &= ((W13p - W13) + (s0(p5) - s0(w5)) + (p4 - w4)) == D20
    return ok

def e_test(r, e0, e1, e2, w4, w5, w6):
    """Test (e): XOR-conformance of E at steps 4..6 (steps 0..3 and A at 0..2 carry no difference)."""
    a0, a1, a2 = r['A0'], r['A1'], r['A2']
    e3, e4, e5, e6 = r['E3'], r['E4'], r['E5'], r['E6']
    e4p, e5p, e6p = e4 ^ FE[4], e5 ^ FE[5], e6 ^ FE[6]
    ok = (a0 + e0 + S1(e3) + IF(e3, e2, e1) + K[4] + (w4 ^ FL[4])) == e4p
    ok &= (a1 + e1 + S1(e4p) + IF(e4p, e3, e2) + K[5] + (w5 ^ FL[5])) == e5p
    ok &= (a2 + e2 + S1(e5p) + IF(e5p, e4p, e3) + K[6] + (w6 ^ FL[6])) == e6p
    return ok

def step2(r, key, am2, am3, am4):
    """Step 2 of record r on CV1[0..3] = (key, am2, am3, am4): returns (valid, W4, W5, W6)."""
    a0, a1, a2 = r['A0'], r['A1'], r['A2']
    e0 = am4 + a0 - S0(key) - MAJ(key, am2, am3)
    e1 = am3 + a1 - S0(a0) - MAJ(a0, key, am2)
    e2 = am2 + a2 - S0(a1) - MAJ(a1, a0, key)
    e3, e4, e5, e6 = r['E3'], r['E4'], r['E5'], r['E6']
    w4 = e4 - a0 - e0 - S1(e3) - IF(e3, e2, e1) - K[4]
    w5 = e5 - a1 - e1 - S1(e4) - IF(e4, e3, e2) - K[5]
    w6 = e6 - a2 - e2 - S1(e5) - IF(e5, e4, e3) - K[6]
    return w_tests(w4, w5, w6) & e_test(r, e0, e1, e2, w4, w5, w6), w4, w5, w6

def from_w(r, key, w4, w5, w6):
    """Inverse map (W4, W5, W6) -> (E0, E1, E2) -> CV1[1..3] for record r."""
    a0, a1, a2 = r['A0'], r['A1'], r['A2']
    e3, e4, e5, e6 = r['E3'], r['E4'], r['E5'], r['E6']
    e2 = e6 - a2 - w6 - S1(e5) - IF(e5, e4, e3) - K[6]
    e1 = e5 - a1 - w5 - S1(e4) - IF(e4, e3, e2) - K[5]
    e0 = e4 - a0 - w4 - S1(e3) - IF(e3, e2, e1) - K[4]
    am2 = e2 - a2 + S0(a1) + MAJ(a1, a0, key)
    am3 = e1 - a1 + S0(a0) + MAJ(a0, key, am2)
    am4 = e0 - a0 + S0(key) + MAJ(key, am2, am3)
    return e0, e1, e2, am2, am3, am4

def record(comb, pairs, rec):
    pi, w7, e3, key = rec
    ci, e4, a0, w8 = pairs[pi]
    e5, e6, e7, a1, a2, a3, w9, w10, w11 = comb[ci]
    return dict(A0=a0, A1=a1, A2=a2, A3=a3, E3=e3, E4=e4, E5=e5, E6=e6, E7=e7, W7=w7, W8=w8, key=key)

def cvec(r, w4, w5, w6):
    w4p, w5p, w6p, w7p, w8p = w4 ^ FL[4], w5 ^ FL[5], w6 ^ FL[6], r['W7'] ^ FL[7], r['W8'] ^ FL[8]
    return (W13 + s0(w5) + w4, W13p + s0(w5p) + w4p, s0(w6) + w5, s0(r['W7']) + w6, s0(w7p) + w6p,
            w8p - r['W8'], W13p - W13)

def sample_valid(r, rng, n, max_batches=64):
    """Uniform (W4, W5, W6) passing all Step-2 tests of record r, by rejection. Some records can never pass test (e);
    if the first batch has no valid draw the record is skipped (empty result)."""
    got = []
    batches = 0
    while sum(len(g[0]) for g in got) < n and batches < max_batches:
        if batches == 1 and sum(len(g[0]) for g in got) == 0:
            break
        batches += 1
        b = 1 << 20
        w4 = rng.integers(0, 2 ** 32, b, dtype=np.uint64).astype(np.uint32)
        w5 = rng.integers(0, 2 ** 32, b, dtype=np.uint64).astype(np.uint32)
        w6 = rng.integers(0, 2 ** 32, b, dtype=np.uint64).astype(np.uint32)
        for i, w in ((4, w4), (5, w5), (6, w6)):
            m, v = SG[i]
            w &= ~m; w |= v
        ok = w_tests(w4, w5, w6)
        w4, w5, w6 = w4[ok], w5[ok], w6[ok]
        e0, e1, e2, *_ = from_w(r, r['key'], w4, w5, w6)
        ok = e_test(r, e0, e1, e2, w4, w5, w6)
        got.append((w4[ok], w5[ok], w6[ok]))
    return tuple(np.concatenate([g[i] for g in got])[:n] for i in range(3))

if __name__ == '__main__':
    slice_path, seed, max_pairs, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    d = np.load(slice_path)
    comb, pairs, recs = d['comb'], d['pairs'], d['recs']
    rng = np.random.default_rng(seed)
    order = np.argsort(recs[:, 3], kind='stable')
    keys = recs[order, 3]
    bounds = np.flatnonzero(np.diff(keys)) + 1
    classes = [g for g in np.split(order, bounds) if 2 <= len(g) <= 16]     # small classes keep the run short
    allc = np.split(order, bounds)
    print('records in slice', len(recs), '| key classes with >= 2 records', sum(len(g) >= 2 for g in allc),
          '| used (2..16 records)', len(classes),
          '| records in them', sum(len(g) for g in classes), flush=True)
    rng.shuffle(classes)
    pair_c, single_c, stats = [], [], dict(t_valid=0, pair_events=0, classes_used=0)
    for g in classes:
        if len(pair_c) >= max_pairs: break
        rs = [record(comb, pairs, recs[i]) for i in g]
        stats['classes_used'] += 1
        for ti, r in enumerate(rs[:4]):
            w4, w5, w6 = sample_valid(r, rng, 1 << 14)
            stats['t_valid'] += len(w4)
            if len(w4) == 0:
                stats['never_valid'] = stats.get('never_valid', 0) + 1
                continue
            _, _, _, am2, am3, am4 = from_w(r, r['key'], w4, w5, w6)
            other = np.zeros(len(w4), dtype=bool)
            for tj, r2 in enumerate(rs):
                if tj == ti: continue
                v, *_ = step2(r2, r['key'], am2, am3, am4)
                other |= v
            # own validity on the mapped CV1 must hold (checks the bijection)
            vself, x4, x5, x6 = step2(r, r['key'], am2, am3, am4)
            assert vself.all() and (x4 == w4).all() and (x5 == w5).all() and (x6 == w6).all()
            idx = np.flatnonzero(other)
            stats['pair_events'] += len(idx)
            for k in idx[:4]:
                if len(pair_c) >= max_pairs: break
                pair_c.append(cvec(r, w4[k], w5[k], w6[k]))
                j = int(rng.integers(0, len(w4)))
                single_c.append(cvec(r, w4[j], w5[j], w6[j]))
    print(stats, flush=True)
    for name, cs in (('pair', pair_c), ('single', single_c)):
        with open(f'{outp}.{name}.txt', 'w') as f:
            for c in cs:
                f.write(' '.join(f'{int(x) & 0xFFFFFFFF:08x}' for x in c) + '\n')
    print('wrote', len(pair_c), 'pair and', len(single_c), 'single tuple-constant vectors', flush=True)
```

### A.26 `flatset.py`

```python
"""Tuple constants of 8 real slice records, 32 each, drawn from each record's own Step-2 validity set.
usage: flatset.py slice.npz seed out.txt"""
import sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
ARGS = sys.argv[1:]
import pairexp as P
d = np.load(ARGS[0]); rng = np.random.default_rng(int(ARGS[1]))
recs = d['recs']
done = 0
with open(ARGS[2], 'w') as f:
    for i in rng.permutation(len(recs)):
        if done == 8: break
        r = P.record(d['comb'], d['pairs'], recs[i])
        w4, w5, w6 = P.sample_valid(r, rng, 32)
        if len(w4) < 32: continue                     # record never valid: skip
        done += 1
        for k in range(32):
            f.write(' '.join(f'{int(x) & 0xFFFFFFFF:08x}' for x in P.cvec(r, w4[k], w5[k], w6[k])) + '\n')
```

### A.27 `analyse2.py`

```python
"""Compare Step-3 pass counts of tuple constants from pair events with those of the same records' single events, and
the spread over each record's own validity set.
usage: analyse2.py NPAIR NFLATREC FLATPER out.0 out.1 ...   (cvec order: NPAIR pair, NPAIR single, NFLATREC*FLATPER flat)"""
import json, math, sys
npair, nrec, per = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
runs = []
for path in sys.argv[4:]:
    lines = open(path).read().split('\n')
    h = lines[0].split()
    runs.append((int(h[9]), [int(l.split()[5]) for l in lines[1:] if l.startswith('c ')]))
hist = sum(r[0] for r in runs)
tot = [sum(r[1][c] for r in runs) for c in range(len(runs[0][1]))]
pair, single, flat = tot[:npair], tot[npair:2 * npair], tot[2 * npair:2 * npair + nrec * per]
ratio = sum(pair) / sum(single)
rs = [sum(r[1][:npair]) / max(sum(r[1][npair:2 * npair]), 1) for r in runs]
m = sum(rs) / len(rs)
se = math.sqrt(sum((x - m) ** 2 for x in rs) / (len(rs) - 1) / len(rs))
recs = []
for k in range(nrec):
    xs = flat[k * per:(k + 1) * per]
    mu = sum(xs) / per
    recs.append(dict(mean=mu, max_over_mean=max(xs) / mu if mu else None, min_over_mean=min(xs) / mu if mu else None,
                     poisson_rel_sd=1 / math.sqrt(mu) if mu else None))
out = dict(histories=hist, pair_sum=sum(pair), single_sum=sum(single), ratio_pair_over_single=ratio,
           ratio_se_from_processes=se, ratio_upper_2se=ratio + 2 * se,
           per_record_flatness=recs, flat_max_over_mean=max(r['max_over_mean'] for r in recs if r['max_over_mean']))
print(json.dumps(out, indent=1))
```

### A.28 `runs_v8.sh`

```sh
#!/bin/sh
# Section 9.1 runs (v8), from this directory with fig6_rows_296.txt and check_route.py present. 10 processes, nice 10.
set -e
python3 mkparams.py > /dev/null                                 # params.h and p4.bin (the real P4 list)
python3 step3ref.py                                             # S's tuple passes stages 16..31 in the reference
cc -O3 -march=native -o condexp condexp.c
# Measurement 1: 64 synthetic tuple-constant vectors from the validity set of S's record
python3 gen_cvec.py 64 20261008 > cvec64.txt
mkdir -p run1
for i in 0 1 2 3 4 5 6 7 8 9; do nice -n 10 ./condexp p4.bin cvec64.txt $((1000 + i)) 20000000000 1024 64 1 > run1/out.$i & done
wait
python3 analyse.py run1/out.* > run1/summary.json
# Measurement 2: real records of the key slice 0x00, pair events and single events of the same records
python3 table.py 8 0 10 slice00.npz
mkdir -p pp
for i in 0 1 2 3 4 5 6 7 8 9; do nice -n 10 python3 pairexp.py slice00.npz $((5000 + i)) 52 pp/p$i > pp/log$i & done
nice -n 10 python3 flatset.py slice00.npz 4242 flat8x32.txt
wait
cat pp/p0.pair.txt pp/p1.pair.txt pp/p2.pair.txt pp/p3.pair.txt pp/p4.pair.txt pp/p5.pair.txt pp/p6.pair.txt \
    pp/p7.pair.txt pp/p8.pair.txt pp/p9.pair.txt > pairs.txt
cat pp/p0.single.txt pp/p1.single.txt pp/p2.single.txt pp/p3.single.txt pp/p4.single.txt pp/p5.single.txt \
    pp/p6.single.txt pp/p7.single.txt pp/p8.single.txt pp/p9.single.txt > singles.txt
cat pairs.txt singles.txt flat8x32.txt > cvec_rec.txt
mkdir -p run2
for i in 0 1 2 3 4 5 6 7 8 9; do nice -n 10 ./condexp p4.bin cvec_rec.txt $((2000 + i)) 10000000000 1024 64 1 > run2/out.$i & done
wait
python3 analyse2.py $(wc -l < pairs.txt) 8 32 run2/out.* > run2/summary.json
```
