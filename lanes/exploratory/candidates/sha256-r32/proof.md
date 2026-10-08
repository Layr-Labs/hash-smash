# SHA-256 reduced to 32 steps: two-block collision from the CRYPTO 2026 35-step characteristic, run under a hard work counter

## 0. Claim

Track `sha256-r32-exploratory`, target profile `sha256-r32-prefix-v1`, attack class `ordinary-collision`, cost model
`collision-frontier-v5`: one 32-step SHA-256 compression is 1 unit and every other primitive 256-bit word-RAM
operation is 1/C unit with C = 2224.

The algorithm of Sections 4-5 outputs two distinct 128-byte messages whose complete hashes under the target are equal
(standard IV, FIPS 180-4 padding, steps 0..31 on all three padded blocks, feed-forward, all 256 output bits). Bounds:

| Field | Claimed | Computed (Sections 9-11) |
|---|---|---|
| time_log2 | 46.49 | total <= 98,278,802,824,929 units = 2^46.48195 |
| preprocessing_log2 | 45.85 | C + D + E = 63,086,936,929,280 units = 2^45.84241 |
| success_probability | 0.39 | >= 0.390105 |
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
   charge. With T = 2^44.8075 trials and a counter cap of 254 T operations (the cap of GordoAR's ddd666d3), the online
   phase is 2^45.0003 units.
4. An exact integer ledger (Section 10) and a sensitivity table (Section 13).
5. Our own evidence for the CPU-second price (Section 15). **New in this package: a callgrind profile of the charged
   workload type itself (Section 15.6).** STP 2.3.4 with CryptoMiniSat 5.11.21, called as
   `stp model.cvc --cryptominisat --threads N` on the authors' model re-parametrised as in #396, ran one call per
   search step with its whole front end, plus one call run to its answer, and every executed instruction in every
   object was priced by its form. We charge m_stp = 0.02 m_once + 0.98 m_search = 3.618 operations per
   instruction: every search instruction at our costliest search minute, and 2% at our costliest one-off part. It
   replaces the composed 3.6874 of our v4 package 23960a0e. The price is 2^21.650 units per CPU-second, instead of
   2^21.677 in 23960a0e, 2^22.527 in 49f8f6d4 (class pricing) and 2^23 in 841646f2. The per-form costing of the
   library, its profile on our SHA-256 CNF and the 17 rate runs of the earlier packages are kept (Sections
   15.1-15.5).

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

T = ceil(2^44.8075) = 30,789,421,617,586 trials, and a counter cap W_cap = 254 T counted operations. Nothing is
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
| CPU-second price | kappa = 3,290,832 = 2^21.650 units per CPU-s | #396/#296 callgrind rate (Section 7); our profile of the charged workload type and our rate spread (Section 15) |

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

**CPU-second price kappa = 3,290,832 units = 2^21.650 units = 2^32.769 primitive operations per CPU-s.**
- Calibration (#296/#396): one deterministic solver call took 40.42, 41.07 and 41.10 native CPU-s, and retired
  44,197,378,388 instructions under callgrind with identical output. At the fastest time this is R_cal = 2^30.026
  instructions per CPU-s.
- Operations per executed instruction (ours, Section 15.6). We profiled the charged workload type under callgrind:
  STP 2.3.4 linked with CryptoMiniSat 5.11.21, called as `stp model.cvc --cryptominisat --threads N`, on the
  authors' model re-parametrised as above. Four calls, one per search step at 1, 2, 4 and 8 threads, each ran its
  whole STP front end (1.61-1.83e11 instructions) and then 4-5 minutes of
  search under callgrind (4.7-7.4e10 instructions). A fifth call, E, repeated
  Step 2 until STP returned its answer. Every executed instruction in every object is priced by its form under the
  v5 primitive list (Section 15.1 table).
  - Front end: 3.931-3.938 operations per instruction; heavy share 0.52%,
    mostly `div` in hash-table indexing.
  - Search: 2.562-3.009 per instruction over each whole search; 1-2 minute windows 2.12-3.59. The
    costliest windows are memmove-heavy phases; run E, which repeated C's model to its answer, passed through one
    (3.58) and returned to 2.06, with a whole-search mean of 2.894.
  - We charge **m_stp = 0.02 m_once + 0.98 m_search = 0.02 * 4.924 + 0.98 * 3.591 = 3.618**: every search
    instruction at our costliest minute, and 2% of the instructions at the costliest one-off part (front end or the
    seconds after a stop signal). One-off parts were at most 0.96% of the charged instructions: 59 calls,
    each with one front end of at most 1.83e11 and one end part of at most
    1.30e10 instructions, against at most S * R_cal * 593,858 = 1.20e15. Our
    profiled calls spent 70-79% in the front end only because we stopped their searches early.
- Rate spread S = 1.85 (ours, Section 15.2): over 14 single-thread CryptoMiniSat runs on SHA-256 CNF, the
  instructions per CPU-s on one machine varied by at most a factor 1.842 (max/min). We allow S = 1.85 for the step
  from the one calibrated call to the 59 charged calls.
- kappa = ceil(R_cal * m_stp * S / C) = ceil((44,197,378,388 / 40.42) * 3.618 * 1.85 / 2224) = 3,290,832. It
  allows 6.69 operations per instruction at R_cal.
- Earlier prices. Our v4 package 23960a0e composed m_dyn = 3.6874 from the ordinary mean 1.956 of the same library
  run through its Python binding on our SHA-256 CNF and the calibrated call's class shares (7.24% PLT stubs at 3,
  0.416% heavy at 400). The measured mean of the charged workload type replaces that composition. Our whole-call
  heavy share, 0.43-0.46%, is close to the credited 0.416%, and PLT stubs are priced at their
  call sites (Section 15.6). 49f8f6d4 priced every ordinary instruction at 5 (m_class = 6.6432). Section 13 gives both
  as sensitivity: 46.499 and 47.097 at this T and cap.

**Charge.** E = 32 * 593,858 * 3,290,832 = 62,537,181,115,392 units = 2^45.829779.

## 8. Starting solution (D) and table build (C)

**D.** S Sect. 4 finds one solution of the characteristic through step 13 and reports about 2^34.3 for this, with no
unit; this solution is our advice. Read as 35-step compressions, 2^34.3 is below 2^34.46 target units. The organizer
reference costs (2140 operations for 31 steps, 2224 for 32) give 84 operations per step, so a 35-step compression costs
at most 2224 + 3 * 84 = 2476 operations, i.e. 1.114 units. #296 ran the same task twice with the authors' exact value model and all signed rows asserted: 534.1 and
374.7 CPU-s, both outputs checked exactly. At the kappa of Section 7 and a factor 32 those runs price the task at
32 * 908.8 * 3,290,832 = 2^36.48 units (2^37.83 at kappa = 2^23). We charge **D = 2^38 = 274,877,906,944 units**,
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
then Pr[U] >= 1 - (1 - s)^T >= 1 - exp(-sT). With T = 30,789,421,617,586, sT = 0.495981, so Pr[U] >= 0.391027.

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
Pr[S > 254 T] <= T * E[X^2] / (T * (254 - 238.943))^2 = 6.436e12 / (226.72 * T) <= 9.22e-4.
```

**Result.** Pr[success] >= 0.391027 - 0.000922 = **0.390105 >= 0.39 claimed** (= the required minimum). The claim
does not rely on rounding: the margin is 0.000105. A second moment 10 times larger than charged would lower the bound
to 0.3818 (Section 13).

## 10. Time ledger (exact)

All figures are in target-compression units; C = 2224.

```
A + B = ceil((T * (2224 + 64) + 254 * T) / 2224) + 8
      = ceil(30,789,421,617,586 * 2,542 / 2224) + 8
      = 35,191,865,895,649 units = 2^45.0003
        (T first-block compressions; 64 fixed ops per trial; the counted cap 254 T;
         8 units for the final 6-compression verification, the comparison and the refused-cap test)
C     =             274,877,906,944 = 2^38
D     =             274,877,906,944 = 2^38
E     =          62,537,181,115,392 = 2^45.829779   (32 * 593,858 CPU-s * 3,290,832)
total =          98,278,802,824,929 = 2^46.481946  <=  2^46.49 = 98,829,022,172,438
C + D + E =      63,086,936,929,280 = 2^45.842407  <=  2^45.85
```

The claimed time_log2 = 46.49 leaves a factor of 1.0056 in reserve. It does not depend on rounding the
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
- `cpu-second-pricing` (score-critical). One solver CPU-second costs at most kappa = 3,290,832 units (2^32.769
  operations).
  - Evidence: the credited callgrind rate (Section 7), our callgrind profile of STP + CryptoMiniSat on the
    re-parametrised model (Section 15.6), our rate runs (Section 15.2).
  - Assumption: the charged calls retire at most 1.85 times the calibrated instructions per CPU-s, and their
    instructions cost at most m_stp = 3.618 operations on average: no long stretch of their search costlier than
    our costliest search minute (3.591), and one-off work (front ends, call ends) at most 2% of their
    instructions.
- `starting-solution-cost` (supporting). The Step-1 starting solution costs at most 2^38 units (Section 8).
- `work-moments` (supporting). These are the occupancy, multiplicity and stage-pass inputs to E[X] and E[X^2].
  - They affect only the 9.22e-4 cap-stop term, and through it the success bound.
- `search-peak-memory` (supporting). The solver peak is at most 2^33 bytes. This affects memory only.

## 13. Sensitivity and limitations

| Change | Total time_log2 |
|---|---|
| as charged (m_stp = 3.618, kappa 2^21.650, factor 32) | 46.482 |
| m_stp + 10% / + 25% | 46.571 / 46.695 |
| optimistic: largest whole-search mean 3.010 with a 25% front-end weight (m = 3.242) | 46.383 |
| search priced at run E's complete-search mean 2.894 (m = 2.935) | 46.297 |
| one-off weight 5% instead of 2% (m = 3.658) | 46.492 |
| end parts merged into the preceding search window (costliest 3.656; m = 3.662) | 46.493 |
| largest whole-call mean of our truncated calls (m = 3.730) | 46.510 |
| m_dyn = 3.6874, the composition of 23960a0e (kappa 2^21.677) | 46.499 |
| class price of 49f8f6d4 (kappa 2^22.527) | 47.097 |
| kappa 2^23 (841646f2) | 47.472 |
| spread S = 1 / 2.5 / 3.63 instead of 1.85 | 45.983 / 46.773 / 47.171 |
| factor 16 | 45.929 |
| factor 64 | 47.192 |
| factor 128 | 48.022 |

| p per entry or second moment | Success bound at T = 2^44.8075, W_cap = 254 T |
|---|---|
| 2^-46 (charged) | 0.3901 |
| 2^-46.5 | 0.2949 (below 0.39) |
| 2^-47 | 0.2187 (below 0.39) |
| E[X^2] 10 times the charged bound | 0.3818 (below 0.39) |

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
  holds if no long stretch of their search cost more per instruction than our costliest minute (3.591). Our whole
  searches averaged 2.562-3.009.
- The cap 254 T leaves 15 operations per trial above the charged mean E[X] <= 238.94, so the cap-stop term
  (9.22e-4) is larger than in 23960a0e. A second moment 10 times the charged bound would lower the success bound to
  0.3818.
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
- m = m_stp = 3.618 is the number of primitive operations per retired instruction, set from our profile of
  STP + CryptoMiniSat on the re-parametrised model: 0.98 times the costliest search window plus 0.02 times the
  costliest one-off part (Section 15.6);
- S = 1.85 allows the charged calls to retire faster than the calibrated call. It comes from the spread we measured
  (Section 15.2).
kappa = 3,290,832 allows 6.69 operations per instruction at R_cal.

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
- If the charged calls retired more than 1.85 times R_cal, or their instructions cost more than m_stp = 3.618
  operations on average, kappa would no longer cover them. Section 13 gives the size of either effect.

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

### 15.6 Profile of the charged workload: STP + CryptoMiniSat on the re-parametrised model (new in this package)

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
  window every 120 s and ran until STP printed its answer (`Valid.`: tE <= 5 is infeasible, as #396 found). Every executed address in every object
  (`stp`, `libstp`, `libcryptominisat5`, libc, libstdc++, libm, libgcc_s, ld.so, Boost) was matched to its
  instruction in `objdump -d -M intel` of that object and priced by the Section 15.1 table (`x86ops.py`, unchanged).
  Multiply and floating-point forms that the table does not list (`cmpnlesd`, `pmuludq`, `vfmadd132sd` and the like)
  are heavy too: 400 per scalar operation, times the lanes of a packed form, times 2 for a fused multiply-add. GNU
  objdump prints string instructions without a size suffix and repeats some prefixes (`data16 cs nop`); we normalise
  both before the lookup, so a `rep movsb` iteration costs 6 and a padding `nop` 1. No executed form was left
  unrecognised (0.00%). The summed per-instruction counts equal callgrind's own totals for every dump.
- **PLT stubs and unmapped code.** callgrind's default `--skip-plt=yes` counts each PLT stub instruction at the call
  instruction that entered it, so stubs are priced as that call (3 or more operations), at least their own price
  (an indirect jump through memory, 3). 0.01-0.47% of the instructions ran outside any file-backed object and could
  not be disassembled; each is charged 8.

| Call | Front end: instructions, m | Search: instructions, m | Search windows: m | End part: instructions, m | Whole call: m |
|---|---|---|---|---|---|
| A | 1.833e11, 3.935 | 4.841e10, 2.562 | 2.68, 2.78, 2.64 | 13.01e9, 2.204 | 3.648 |
| C | 1.611e11, 3.938 | 4.668e10, 3.009 | 2.99, 2.93, 2.76, 3.59 | 0.35e9, 4.924 | 3.729 |
| E | not instrumented | 5.519e10, 2.894 | 2.59, 3.58 | 7.84e9, 2.058 | - |
| D | 1.745e11, 3.931 | 5.473e10, 2.778 | 2.41, 2.47, 2.99, 2.91 | 3.32e9, 3.773 | 3.655 |
| B | 1.745e11, 3.931 | 7.431e10, 2.675 | 2.12, 2.53, 3.01, 2.65 | 11.91e9, 2.982 | 3.556 |

The search columns cover everything after the first solve call. Windows are the parts between
periodic dumps; the end part runs from the last periodic dump to the exit. Heavy shares: front end 0.52%,
search 0.18-0.27%.

- **Front end against search.** The front end is the same code for all four models and costs 3.931-3.938 operations per
  instruction, with a heavy share of 0.52%: mostly `div` in hash-table indexing (libstp at 4.1 and libstdc++ at
  15 operations per instruction). The search runs in libcryptominisat5 (93-96% of its instructions) and libc. It
  costs 2.562-3.009 per instruction, with a heavy share of 0.18-0.27%, mostly `comisd` and `imul`. Its ordinary mean,
  1.689-1.928, is a little below the 1.880-1.956 of our binding runs (Section 15.5).
- **The costly search phase is transient.** Some search windows are dominated by `rep movsb` copying in libc
  memmove (up to 25% of the instructions, 6 operations per iteration), which lifts them to about 3.6. C and D were
  stopped inside such a phase, so their last minute and the few seconds after the stop signal are their costliest
  parts. Run E repeated C's model to completion: its 2-minute windows were 2.59, 3.58, 2.06 (the last one ends with the
  solver's answer), and its whole search averaged 2.894. The phase passes and the search returns to its usual mix.
- **How m is set.** We split every call into one-off parts, which a charged call also runs once (the front end, and
  the end part from the last periodic dump to the exit), and search windows (the parts between periodic dumps, 60-120
  s each). We charge

  **m_stp = 0.02 m_once + 0.98 m_search = 0.02 * 4.924 + 0.98 * 3.591 = 3.618** (rounded up),

  with m_once = 4.924, the costliest one-off part of any call (the few seconds of C after its stop signal; the front
  ends cost 3.931-3.938), and m_search = 3.591, the costliest search window of any call. So every charged search
  instruction is priced as in our costliest minute, although the whole searches averaged 2.562-3.009 and the complete
  search of E 2.894.
- **Why 2% covers the one-off work.** One front end of our models takes at most 1.83e11 instructions (about 170
  CPU-s at R_cal) and one end part at most 1.30e10. Under the spread S the 59 charged calls retired at most
  S * R_cal * 593,858 = 1.20e15 instructions, so their one-off parts were at most
  59 * (1.83e11 + 1.30e10) / 1.20e15 = 0.96% of the instructions; 2% is 2.1 times that. Our
  profiled calls spent 70-79% of their instructions in the front end only because we stopped each search after a
  few minutes; their whole-call means (3.556-3.729) describe those truncated calls, not the charged ones. #396's
  calibrated call (4.42e10 instructions in all) suggests its front ends were smaller than ours, which lowers the share.
- **Agreement with the credited calibration.** The whole-call heavy share of our calls, 0.43-0.46%, is close to the
  0.416% that #296/#396 measured on the calibrated call. The credited 7.24% PLT share needs no separate term here,
  because the stubs are counted and priced at their call sites.
- **What it does not cover.**
  - The binaries are ours: Debian's CryptoMiniSat build and our STP build. #396's builds and compiler flags are not
    published. The ordinary means of the Debian library in the search (1.689-1.928) and of the manylinux library of
    Section 15.5 (1.880-1.956) differ by less than 15%.
  - Our searches lasted 4-6 minutes under callgrind, about 20-40 s of native search on our machine, and only E ran
    to its answer. The charged calls searched for hours. The price assumes that no long stretch of their search was
    costlier per instruction than our costliest minute (3.591); our search windows ranged from 2.12 to 3.59.
  - The models are our regeneration from #396's description, not its files. #396's calibrated Step-1 call (1 thread,
    `--max-num-confl 20000`) retired 4.42e10 instructions in all, fewer than our front end alone (1.61-1.83e11), so
    its models were smaller than ours or were built differently. A smaller front end only lowers a call's front-end
    share.
  - The instruction rate is not re-measured. R_cal and S are unchanged (Sections 7 and 15.2).
- **Reproduction.** Appendix A.7-A.15 lists the scripts with their SHA-256 hashes: `setup_stp.sh` and
  `build_stp.sh` install the toolchain and build STP, `gen396.py` writes the models, `cgrun.sh` and `windows.sh` run
  the profiles (`ffrun.sh` ran E), `mkdis.sh` disassembles every object, `stpdyn.py` prices each call and
  `stpsum.py` sets m_stp.

## Appendix A. Profile scripts (participant tools)

- `setup.sh`: SHA-256 2e814916da4f74b88bbe53fb70fc38da26f58586c137fcc60a4c677256032d25
- `runs.sh`: SHA-256 2dbc751d1bdad0fc478d5e89081f05d7ca6926eda0e75fdbea593df291b4c289
- `lbench.py`: SHA-256 435ef2774d12f639df0c82d946c680be3993178b57ab3ee5d3dc8ddd91b7eac6
- `x86ops.py`: SHA-256 220b1ab3aad0e96fc0c2d21a7977911de832df8aab12017cdfa971feae3fe190
- `dynparse.py`: SHA-256 e67a3fad41a6e530619affacbca11ef71499eb2094b3b810624c2cda419c0e60
- `dynall.py`: SHA-256 29747d0c46ad6e420427e4d39bb40fd35120dfb324b2b363f20af45ce982f818

Scripts of Section 15.6 (they import `x86ops.py` and `dynparse.py` above, unchanged):

- `setup_stp.sh`: SHA-256 d78ad64d88fddf585d7fa513d0245c6049a23f381f01f34e2ebac6e139be84a0
- `build_stp.sh`: SHA-256 97912646526b26eeec37ecff07cfab786c6c1b234316b3499ef578d498bdfa6d
- `gen396.py`: SHA-256 d8f6d3f3b86800b39d270ee5f891fb3f3390142d4033091275bbe8f09dc23526
- `cgrun.sh`: SHA-256 87e122d5937fd47e08f532133860b71f3ff839c456d3712a1faae819be2764cf
- `windows.sh`: SHA-256 9f5fb74d935ebce2d90e62c30f110fcad9b7feaba1acb5d9a85c15a05980b259
- `ffrun.sh`: SHA-256 45410d79921ddc1bac89e1a62f3301024fb8f33c6133dd7eb6ea8b459674b063
- `mkdis.sh`: SHA-256 007fc983efd700078f45aeb5da3028dc532aa903841630669f32219607ff99b6
- `stpdyn.py`: SHA-256 c36ae3c5264a258fe46f8bdb09bc661b08262c1c24ba90d458a2950baeeee083
- `stpsum.py`: SHA-256 a9b7046867ae8f61eae1c181d4b024c3615cf14eff8eac3bdc921491f5546068

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
from x86ops import cost

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
                    if c is None:
                        c = heavy_extra(mn)
                        if c: cls = 'heavy'
                        else: c = 8; unk[mn] += n
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
and search windows (the parts between periodic dumps, 60-120 s each). We charge

    m_stp = W * m_once + (1 - W) * m_search,

with m_once the costliest one-off part, m_search the costliest search window over all calls (each rounded up to
0.001) and W = 0.02 the weight of one-off work: twice the share that 59 front ends and end parts can have among the
instructions of the charged calls.
"""
import json, math, sys

W = 0.02
R_CAL = 44197378388 / 40.42
I_MAX = 1.85 * R_CAL * 593858          # instructions of the 59 charged calls at most, under the spread S = 1.85
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
once_ir_max = max(c['front_end_ir'] for c in full) + max(c['end_ir'] for c in cs)
once_share = 59 * once_ir_max / I_MAX
m_stp = up(W * m_once + (1 - W) * m_search)
out = dict(calls=calls, weight=W, m_front=m_front, m_end=m_end, m_once=m_once, m_search=m_search, m_stp=m_stp,
           m_max_milli=round(m_stp * 1000), front_end_ir_max=max(c['front_end_ir'] for c in full),
           end_ir_max=max(c['end_ir'] for c in cs), i_max=I_MAX, once_share_bound=once_share,
           search_allowed=(m_stp - once_share * m_once) / (1 - once_share),
           search_mean_max=max(c['solve_m'] for c in cs), window_m_min=min(m for c in cs for m in c['windows']),
           m_whole_max=max(c['whole_m'] for c in full), front_end_share_min=min(c['front_end_share'] for c in full))
print(json.dumps(out, indent=1))
```
