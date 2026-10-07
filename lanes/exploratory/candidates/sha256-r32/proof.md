# SHA-256 reduced to 32 steps: two-block collision from the CRYPTO 2026 35-step characteristic, run under a hard work counter

## 0. Claim

Track `sha256-r32-exploratory`, target profile `sha256-r32-prefix-v1`, attack class `ordinary-collision`, cost model
`collision-frontier-v5`: one 32-step SHA-256 compression is 1 unit and every other primitive 256-bit word-RAM
operation is 1/C unit with C = 2224.

The algorithm of Sections 4-5 outputs two distinct 128-byte messages whose complete hashes under the target are equal
(standard IV, FIPS 180-4 padding, steps 0..31 on all three padded blocks, feed-forward, all 256 output bits). Bounds:

| Field | Claimed | Computed (Sections 9-11) |
|---|---|---|
| time_log2 | 47.15 | total <= 155,054,793,272,412 units = 2^47.13977 |
| preprocessing_log2 | 46.72 | C + D + E = 115,377,568,590,208 units = 2^46.71336 |
| success_probability | 0.40 | >= 0.41069 |
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
   charge. With T = 2^44.9 trials and a counter cap of 400 T operations, the online phase is 2^45.173 units.
4. An exact integer ledger (Section 10) and a sensitivity table (Section 13).
5. Our own evidence for the CPU-second price (Section 15): a per-instruction costing of the x86-64 CryptoMiniSat
   5.11.21 code under the v5 primitive list, and 17 instruction-rate runs of CryptoMiniSat on SHA-256 CNF. The price
   is derived from the calibrated rate, the class-priced opcode mix and our measured rate spread: 2^22.527 units per
   CPU-second instead of 2^23.

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

T = ceil(2^44.9) = 32,828,179,945,388 trials, and a counter cap W_cap = 400 T counted operations. Nothing is
restarted.

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
| CPU-second price | kappa = 6,042,470 = 2^22.527 units per CPU-s | #396/#296 callgrind rate and opcode mix (Section 7), our rate spread and per-form costing (Section 15) |

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

**CPU-second price kappa = 6,042,470 units = 2^22.527 units = 2^33.646 primitive operations per CPU-s.**
- Calibration (#296/#396): one deterministic solver call took 40.42, 41.07 and 41.10 native CPU-s, and retired
  44,197,378,388 instructions under callgrind with identical output. At the fastest time this is R_cal = 2^30.026
  instructions per CPU-s.
- Opcode mix: ordinary integer 92.3%, unmapped 7.24% (identified as PLT stubs), divide 0.305%, floating point 0.085%,
  multiply 0.026%.
- Class pricing: every instruction outside the 0.416% divide/multiply/floating-point share costs 5 primitive
  operations, and those cost 400. This gives m_class = 0.99584 * 5 + 0.00416 * 400 = 6.6432 operations per instruction.
- Rate spread (ours, Section 15.2): over 14 single-thread CryptoMiniSat runs on SHA-256 CNF, the instructions per CPU-s
  on one machine varied by at most a factor 1.842 (max/min). We allow S = 1.85 for the step from the one calibrated
  call to the 59 charged calls.
- kappa = ceil(R_cal * m_class * S / C) = ceil((44,197,378,388 / 40.42) * 6.6432 * 1.85 / 2224) = 6,042,470.
- Per-form costing (ours, Section 15.1): the x86-64 code of CryptoMiniSat 5.11.21 costs 1.71 operations per ordinary
  instruction in its hot functions and 1.73 over the whole library, so m_static = 3.388. The class pricing is 1.96x
  above this, a reserve on top of S. kappa therefore covers charged calls that retire up to 3.63 times the calibrated
  instructions per CPU-s.
- Section 13 gives the sensitivity. kappa = 2^23, the price of our earlier package, gives 47.504.

**Charge.** E = 32 * 593,858 * 6,042,470 = 114,827,812,776,320 units = 2^46.706465.

## 8. Starting solution (D) and table build (C)

**D.** S Sect. 4 finds one solution of the characteristic through step 13 and reports about 2^34.3 for this, with no
unit; this solution is our advice. Read as 35-step compressions, 2^34.3 is below 2^34.46 target units. The organizer
reference costs (2140 operations for 31 steps, 2224 for 32) give 84 operations per step, so a 35-step compression costs
at most 2224 + 3 * 84 = 2476 operations, i.e. 1.114 units. #296 ran the same task twice with the authors' exact value model and all signed rows asserted: 534.1 and
374.7 CPU-s, both outputs checked exactly. At the kappa of Section 7 and a factor 32 those runs price the task at
32 * 908.8 * 6,042,470 = 2^37.36 units (2^37.83 at kappa = 2^23). We charge **D = 2^38 = 274,877,906,944 units**,
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

- **Per trial.** Pr[V >= 1] >= E[V] - E[C(V,2)] >= q (1 - 2^-5) with q >= 2^-17.3583 (`q-32step-matching-rate`,
  `valid-tuple-pairs`).
- **Per tuple.** E[X] = 196,608 * 2^-46 = 2^-28.415 (`step3-46-conditions`). The entries share W14 in 12 groups of
  2^14, and the 12 W20 sign/carry conditions are common inside a group. Hence
  E[C(X,2)] <= 12 * C(2^14, 2) * 2^-12 * (2^12 p)^2 + C(2^17.585, 2) p^2 <= 2^-49.3, and
  r = Pr[X >= 1] >= E[X] - E[C(X,2)] >= 2^-28.415 (1 - 2^-20).
- **Per trial success.** s >= 2^-17.3583 * (31/32) * 2^-28.415 * (1 - 2^-20) = 2^-45.819143. Different valid
  tuples of the same trial only add chances, so the bound uses one.

Trials use fresh coins and are independent. If U is the event that some trial among the T uncapped trials succeeds,
then Pr[U] >= 1 - (1 - s)^T >= 1 - exp(-sT). With T = 32,828,179,945,388, sT = 0.528823, so Pr[U] >= 0.410701.

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
Pr[S > 400 T] <= T * E[X^2] / (T * (400 - 238.94))^2 = 6.436e12 / (25,940 * T) <= 7.56e-6.
```

**Result.** Pr[success] >= 0.410701 - 0.0000076 = **0.41069 >= 0.40 claimed** (> 0.39 required). The claim does not
rely on rounding: the margin is 0.0107.

## 10. Time ledger (exact)

All figures are in target-compression units; C = 2224.

```
A + B = ceil((T * (2224 + 64) + 400 * T) / 2224) + 8
      = ceil(32,828,179,945,388 * 2,688 / 2224) + 8
      = 39,677,224,682,204 units = 2^45.1734
        (T first-block compressions; 64 fixed ops per trial; the counted cap 400 T;
         8 units for the final 6-compression verification, the comparison and the refused-cap test)
C     =             274,877,906,944 = 2^38
D     =             274,877,906,944 = 2^38
E     =         114,827,812,776,320 = 2^46.706465   (32 * 593,858 CPU-s * 6,042,470)
total =         155,054,793,272,412 = 2^47.139771  <=  2^47.15 = 156,158,020,654,575
C + D + E =     115,377,568,590,208 = 2^46.713356  <=  2^46.72
```

The claimed time_log2 = 47.15 leaves a factor of 1.0071 in reserve, about 74 operations per trial beyond the itemised
charges. It does not depend on rounding the exponent.
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
- `cpu-second-pricing` (score-critical). One solver CPU-second costs at most kappa = 6,042,470 units (2^33.65
  operations).
  - Evidence: the callgrind rate and opcode mix (Section 7), our rate runs and our per-form costing (Section 15).
  - Assumption: the charged calls retire at most 1.85 times the calibrated instructions per CPU-s under the class
    pricing, or 3.63 times under the per-form costing.
- `starting-solution-cost` (supporting). The Step-1 starting solution costs at most 2^38 units (Section 8).
- `work-moments` (supporting). These are the occupancy, multiplicity and stage-pass inputs to E[X] and E[X^2].
  - They affect only the 7.6e-6 cap-stop term, and through it the success bound.
- `search-peak-memory` (supporting). The solver peak is at most 2^33 bytes. This affects memory only.

## 13. Sensitivity and limitations

| Change | Total time_log2 |
|---|---|
| as charged (kappa 2^22.527, factor 32) | 47.140 |
| kappa 2^22 | 46.769 |
| kappa 2^22.5 | 47.120 |
| kappa 2^23 (our earlier package) | 47.504 |
| kappa 2^24 | 48.351 |
| factor 16 | 46.473 |
| factor 64 | 47.939 |
| factor 128 | 48.828 |

| p per entry | Success bound at T = 2^44.9 |
|---|---|
| 2^-46 (charged) | 0.4106 |
| 2^-46.5 | 0.3120 (below 0.39) |
| 2^-47 | 0.2323 (below 0.39) |

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

This section is our own work. It supports `cpu-second-pricing` and does not re-run any charged call. The price is
kappa = R_cal * m * S / C (Section 7):
- R_cal = 2^30.026 is the instruction rate of the calibrated call on the measurement machine (#296/#396);
- m is the number of primitive operations per retired instruction, priced by class at m_class = 6.6432;
- S = 1.85 allows the charged calls to retire faster than the calibrated call. It comes from the spread we measured
  (Section 15.2).
Our per-form costing of m (Section 15.1) is held in reserve. kappa = 6,042,470 allows 12.29 operations per
instruction at R_cal.

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
| multiply, divide, floating-point arithmetic or conversion | 400 (the heavy class of Section 7) |
| any other form | 8 |

| Code set | Instructions | Heavy | Mean operations per ordinary instruction | Ordinary above 5 |
|---|---|---|---|---|
| `PropEngine::propagate_any_order` (4 instantiations) | 1,612 | 0 | 1.70 | 0 |
| hot set: `propagate_any_order`, `propagate_light`, `analyze_conflict`, `litRedundant`, `minimize_using_bins`, `cancelUntil`, `new_decision`, `new_decision_fast_backw`, `enqueue`, `find_conflict_level`, `search`, `attach_and_enqueue_learnt_clause` (26 symbols) | 6,000 | 13 | 1.71 | 0.15% |
| whole library (400 unrecognised forms, mostly lock-prefixed atomics, charged 8) | 253,984 | 3,092 | 1.73 | 0.66% |

The commonest forms in the hot set are mov (38.9%), cmp (7.3%), lea (5.5%) and add (4.4%). These figures are static
counts, not a dynamic profile. We use them only to show that the class price of 5 per ordinary instruction exceeds the
forms the solver contains by a factor of about 2.9. With the measured dynamic heavy share of 0.416% at 400,
m_static = 0.99584 * 1.731 + 1.664 = 3.388. The class pricing m_class = 6.643 is 1.96 times this, and that factor is
held in reserve: the price does not use it.

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
- The per-form costing transfers directly. It describes the x86-64 code of the solver version that ran the charged
  calls, although the STP-linked build may use different compiler flags from the wheel.
- The spread transfers as an empirical range only. It measures how much the per-CPU-second rate moves across instance
  shapes, sizes, seeds, run length and threading for this solver on SHA-256 CNF. We apply its full max/min ratio, as if
  the calibrated call sat at the bottom of the range and every charged CPU-second at the top. The charged calls were
  long, multithreaded and large (5.25 GiB peak). In our runs those three properties lowered the rate or left it
  unchanged.
- If the charged calls retired more than 1.85 times R_cal, the class pricing would no longer cover them. The
  per-form costing would still cover them up to 3.63 times R_cal.

### 15.4 Why no organizer experiment

The organizer runner offers standard-library Python only, with one CPU, 128 MiB and 20 s. It requires byte-identical
output and does not credit runtime or operation counts. It cannot run CryptoMiniSat or read hardware counters, so the
rate cannot be re-measured there. Our scripts are participant tools: the CNF generator and rate harness (SHA-256
8b78762691099e46...), the per-form costing (220b1ab3aad0e96f...) and the run log.
