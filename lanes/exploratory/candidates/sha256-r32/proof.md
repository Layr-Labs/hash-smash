# SHA-256 reduced to 32 rounds: a two-block collision algorithm from the ePrint 2026/1080 characteristic

Track `sha256-r32-exploratory`, target `sha256-r32-prefix-v1`, cost model `collision-frontier-v5` (C = 2224 for this
target). Exploratory lane. Submission state: `ready`.

This package specifies a classical probabilistic algorithm that outputs two distinct 128-byte messages with equal
complete 32-round SHA-256 digests. It is the three-step attack of Yingxin Li, Fukang Liu, Gaoli Wang and Jiali
Shi ("Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2", IACR ePrint 2026/1080, Sect. 4),
which they ran on 35 steps, applied to the 32-round target. The algorithm uses their differential characteristic
(Figure 6) truncated to steps 0..31, their start-point and TAB2 construction (Step 1), first-block matching against TAB2
(Step 2) and the (W14, W15) tail (Step 3). Each block, including the first, is compressed with the 32-round
compression. Both success rates of the attack, the matching rate q and the tail yield, are measured by us at 32 rounds;
neither is taken from the paper. The only cited inputs to the cost are those of the trail-search envelope (Section 7).

The required identifier `sha256-r32-nominal-v2` names the organizer's nominal display reference. It is not an
established attack, a qualified baseline or a security bound. Readiness is a request for review, not a claim of
qualification.

## 0. Claim

| Field | Value | Source |
| --- | ---: | --- |
| time_log2 | 53.38 | conservative ledger total 2^53.3265 + 0.05 bit slack, rounded up |
| success_probability | 0.63 | 1 - exp(-μ), μ = 1.0000 expected successes at the charged (95%-worst) rates |
| memory_log2_bytes | 32.78 | peak RSS 7,326,187,520 B (gt-fulltable-build), rounded up |
| preprocessing_log2 | 53.33 | trail search + start point + TAB2 build + combos + tail setup |
| nonuniform_advice_log2_bytes | 9.98 | 1004 B of hard-coded characteristic and start point; their derivation is charged in time |

The claimed time is `2^53.38` target compressions. It is the conservative ledger total 2^53.3265 plus
a declared slack of 0.05 bit, rounded up (Section 7). It includes preprocessing, the differential-trail search,
the start-point search, all failed trials and every logged measurement run.

How the bound is composed:

- **The trail search dominates the claim. It is charged as our measured search plus a declared envelope.** No
  characteristic was found. Every trail-search run is charged at λ = 1 instructions (Section 7):
  - stream T, our own re-derivation of the paper's SAT/SMT trail search: 104 logged runs plus
    8 runs whose ledger record was lost and which are charged at an estimate, 38.62
    CPU-hours (CPU time) or 40.39 thread-hours (wall time times thread cap, the unit of the time box);
  - follow-up trail streams, which together took 17.39 CPU-hours (18.12 thread-hours):
    - T2-CUBE: 25 runs, 5.23 CPU-hours: our own search models.
    - T2-JOINT: 16 runs, 2.32 CPU-hours: our own joint model.
    - T2-PORTFOLIO: 14 runs, 3.89 CPU-hours: our own search models.
    - T3: 52 runs, 2.37 CPU-hours: the public Peace9911/sha_2_attack code (no licence; its content and code tag match ePrint 2024/349, authorship not confirmed): a 35-step configuration we rebuilt, solved with STP 2.4.1 (MiniSat back end), and its result checker; the same 35-step clauses solved with CaDiCaL; the AutoSHA2Collision model generator (Zhang, Li, Gao and Wang; e1080 reference [25]) with STP 2.4.1 (MiniSat back end); a locally patched copy of the AutoSHA2Collision model library under our own CaDiCaL driver.
    - T2-PORTFOLIO: 6 further runs whose ledger record was lost (runner killed, solver orphaned), 3.57 CPU-hours estimated and charged at the stream's highest instructions per CPU-second.

  In all, 56.01 CPU-hours (58.51 thread-hours), charged at 2^38.828 units.
  Stream T stopped inside its 48 thread-hour time box (40.39 thread-hours). The
  follow-up streams then continued the search, to 58.51 thread-hours in all, still without a
  characteristic. This is the cost of our own unsuccessful search. It is charged in full, but it is not a lower bound on the cost of the authors'
  search.

  Because our search found nothing, the charge adds an envelope of 14976 thread-hours priced at the
  `armv8` conversion, the strictest of the 3 conversions considered. The envelope is at most
  8 sequential solver calls of at most 72 hours each on 26 threads
  (576 hours of 26-thread solver time). 8 calls is the minimum the
  4 minimisation steps of the procedure need (e1080:696-733); 72 hours is the example
  per-call time limit of the authors' earlier procedure (e349:1110-1113); 26 threads is the setting of
  every solver call in the public Peace9911/sha_2_attack code (commit 6a9f35f). The paper states no search time, so
  this is the declared heuristic `trail-search-envelope` (Section 6.4), not a proven upper bound. The public code's
  descending one-call-per-integer loops (from 60 or 90) can make many more calls; the envelope then holds only if
  N calls averaged at most 576/N hours (Section 7.4). The trail charge is 2^53.324 units, which is
  99.8% of the total.
- **Everything else** under the same conservative accounting totals 2^44.042 units. That covers the
  attack phases, the start-point charge, every logged run and every HW-engine trial. Charging only the measured trail
  search would give 2^44.081. Neither figure is claimed.
- **Start point: charged at the 2^41.000 cap.** Our own independent start-point search found a start point T′
  at a cost of 2^33.938 units. That is the realized cost of one successful portfolio
  (1 success in 12 full-CNF solver runs). The exact 95% upper bound on its expected
  cost is 2^38.999, under the heuristic of memoryless solve times. T′ fails gate G5: against the published
  T, q moves by -1.50 bit and the yield by +2.38 bits (Section 3). Its cost therefore does not measure the
  cost of finding the published T, so the start point is charged at the cap and T′'s runs are charged as logged work.
  The paper's 2^34.3 (e1080:792-793) has no stated unit, so we do not use it.
- **No midstate credit.** Each first-block trial is charged one full target compression. The 12-step midstate is not
  credited; crediting it at 20/32 would give 2^53.326, and that is not taken.
- **Success probability 0.63.** At the charged 95%-worst rates the algorithm expects μ = 1.0000
  collisions, so 1 − e^−μ = 0.6321. This rests on the declared heuristics in Section 6 and `claim.json`.
- **No end-to-end witness.** No 32-round two-block collision has been produced; the witness hunt was not run. The
  published Table 3 pair is a 35-step collision and is not a 32-round collision (Section 1.2). The tail measurements
  of Section 5 produced 32-step compression collisions from synthetic prefixes and from chaining values obtained by
  resampling W0..W3 of real prefixes and solving back to E−4..E−1. These chaining values are not outputs C32(IV, M0).
  The results are compression collisions only, not target collisions.

## 1. Exact target

### 1.1 The hash function

The target is SHA-256 (FIPS 180-4) with the compression function restricted to its first 32 of
64 rounds, indices 0 through 31, on every padded block. The IV is standard, the padding is standard, the message schedule and constants keep their
original indices, the feed-forward is kept, and all eight output words are serialised big-endian. There is no chosen
IV, no free start and no truncation.

The IV, in standard order a..h, is `6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19`. The constants K0..K31 are:

```
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
```

All additions are modulo 2^32. Rk is a right rotation by k bits and ≫k is a right shift by k bits. Define

```
σ0(x) = R7(x) ⊕ R18(x) ⊕ (x ≫ 3)        σ1(x) = R17(x) ⊕ R19(x) ⊕ (x ≫ 10)
Σ0(x) = R2(x) ⊕ R13(x) ⊕ R22(x)         Σ1(x) = R6(x) ⊕ R11(x) ⊕ R25(x)
IF(x, y, z)  = (x ∧ y) ⊕ (¬x ∧ z)       MAJ(x, y, z) = (x ∧ y) ⊕ (x ∧ z) ⊕ (y ∧ z)
```

The 32-round compression C32(S, B) works as follows:
1. Parse the 64-byte block B as big-endian words W0..W15.
2. Expand W_t = σ1(W_{t−2}) + W_{t−7} + σ0(W_{t−15}) + W_{t−16} for t = 16..31.
3. Write the input chaining value S = (a, b, c, d, e, f, g, h) in the two-register form of the paper (e1080:311-321) as
   (A−1, A−2, A−3, A−4, E−1, E−2, E−3, E−4).
4. For i = 0..31 compute

```
E_i = A_{i−4} + E_{i−4} + Σ1(E_{i−1}) + IF(E_{i−1}, E_{i−2}, E_{i−3}) + K_i + W_i
A_i = E_i − A_{i−4} + Σ0(A_{i−1}) + MAJ(A_{i−1}, A_{i−2}, A_{i−3})
```

5. Output S + (A31, A30, A29, A28, E31, E30, E29, E28), added word by word.

This is the standard step function. With T1 = h + Σ1(e) + IF(e, f, g) + K_i + W_i and T2 = Σ0(a) + MAJ(a, b, c), the
new e = d + T1 is E_i and the new a = T1 + T2 is A_i. The compression is
`verifier/hash_functions.py:_compress('sha256', S, B, 32)`, and every equality in this package is checked with that
function and with `digest(·, 'sha256', 32)`.

### 1.2 Messages, padding and reduction to one compression collision

Every message output by the algorithm has exactly 128 bytes, M = M0 ‖ M1 with two 64-byte blocks. FIPS 180-4 padding
appends one block that depends only on the length 1024 bits:

```
P = 80000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000400
```

so the digest is the serialisation of C32(C32(C32(IV, M0), M1), P). We checked this against the verifier: for a
fixed 128-byte message, `digest(M, 'sha256', 32)` equals that triple composition (equal).

**Lemma 1.** Let CV = C32(IV, M0). If M1 ≠ M1′ and C32(CV, M1) = C32(CV, M1′), then M0 ‖ M1 and M0 ‖ M1′ are
distinct 128-byte messages with equal sha256-r32 digests.

*Proof.* Both messages have length 1024 bits and therefore the same padding block P. The chaining values after the
second block are equal by assumption, so the chaining values after P are equal, and so are the serialised digests.
The messages differ in the second block. ∎

The algorithm outputs (M0 ‖ M1, M0 ‖ M1′) with M1′ = M1 ⊕ ΔM. Here ΔM is the fixed XOR difference listed with the message pair in Section 2.2,
which is nonzero in words 4..8, 12 and 13, so the two messages are always distinct. CV is computed from the
standard IV with the selected 32-round compression. The result is therefore an ordinary collision of the complete
padded 32-round hash, not a free-start, compression-only or truncated one.

The published Table 3 pair of the paper (e1080:819) collides for 35 steps. Our recheck with the trusted verifier gives:

| Check (trusted verifier) | Result |
| --- | --- |
| 35-round two-block digests of Table 3 equal | True |
| second-block 35-round output equals the printed hash (e1080:832) | True |
| C32 second blocks collide from CV35 = C35(IV, M0) | True |
| C32 second blocks collide from C32(IV, M0) | False |
| 32-round two-block digests of Table 3 equal | False |

The pair is therefore **not** a 32-round collision. We use it only as the source of the characteristic, and as an
oracle that follows the characteristic exactly when executed from CV35 = `c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2`.

### 1.3 Notation

- x[j] is bit j of a 32-bit word, and bit 0 is the least significant. A row is the 32 characters of a word written most
  significant bit first, so character p is bit 31 − p.
- For a word X computed in both branches, X is its value in the M1 branch and X′ its value in the M1′ branch. The
  modular difference is δX = X′ − X mod 2^32, and the XOR difference is X ⊕ X′.
- **Signed rows (ours).** `u` at bit j means X[j] = 1 and X′[j] = 0. `n` means X[j] = 0 and X′[j] = 1. `-` means
  X[j] = X′[j].
- **Signed rows (paper).** The paper's eq. (1) (e1080:204-224) writes ∇x between x′ and x, with u = (x = 1, x′ = 0),
  `=` for equal bits, and 0 or 1 for equal bits with that fixed value. Its x is Table 3's M1′. We decided this against
  the executed pair: 0 u/n mismatches with x = M1′, against 119 with x = M1. Every u in Figure 6
  is therefore an n in our rows and vice versa, and the paper's δx = x′ ⊟ x is −δX.
- **Two-branch execution.** Given (CV, M1, M1′), run C32 on both branches from the same CV and record every A_i, E_i
  (i = −4..31) and W_i (i = 0..31). The pair *follows the characteristic through step s* when every A_i, E_i with i ≤ s
  and every W_i with i ≤ s has exactly the signed row given in Section 2.2 (zero rows included).
- **Paper citations.** e1080:N is line N of the `pdftotext -layout` (poppler) text of the ePrint 2026/1080 PDF. The
  PDF has sha256 `3140826cb79709a87bc1d5a20940a354a2695005025a441f0bbbf8a8677462fd` and the text file has sha256 `63482e523a7794e70150c585aaa9f1707315defeab007245dc8ac6fd771148d9`. Page numbers are PDF
  pages. e349:N is line N of the same kind of text of ePrint 2024/349 (Li, Liu and Wang, ref. [7] of the paper,
  e1080:1244). That PDF has sha256 `ca79053516e9110d0e1c99a1f0638f1862d43372ba64e5ba9c50b85631e8ce05` and its text file has sha256 `7861dbe9ae1a0d8f8b83a28a7c719b1b87bc264318fa1b1760b8e9f36bd8eb93`.
- **Attack objects** (defined in Sections 3-5):
  - A TAB2 record fixes (A−1..A13, E3..E13, W7..W13).
  - A first-block trial is one random M0 with CV = C32(IV, M0).
  - A trial is **accepted (level L2)** when a record with A−1 = CV.a gives a two-branch execution that follows the
    characteristic through step 13 (level L1) and also satisfies the prefix-determined expansion conditions of
    Section 2.4.
  - q is the expected number of accepted prefixes per trial, where an accepted prefix is a pair (M0, record).
    Accepts are rare, so this is also the per-trial acceptance probability to within the per-M0 figure of
    Section 4.
  - The yield is the probability that an accepted prefix completes over the tail set V of (W14, W15) to C32(CV, M1) =
    C32(CV, M1′).

## 2. Differential characteristic and conditions

### 2.1 Source

The paper chooses differences in the message words (W4, ..., W8, W12, W13, W20, W22) (e1080:690-699). It searches
for a characteristic with a SAT/SMT-based tool (e1080:692-694) in four steps (e1080:696-733) and prints the result as Figure 6, "The
differential characteristic for 35-step SHA-256" (caption e1080:759, PDF page 16). Table 3 (e1080:819) is a pair
that conforms to it.

We use the characteristic in two forms:

1. **Executed rows.** These are the signed rows of every A_i, E_i and W_i, obtained by two-branch execution of Table 3
   from CV35. They are the ground truth of this package. Every acceptance test of the algorithm (TAB2 build, matching,
   tail set V, final check) compares against these rows by exact two-branch execution, never against a list of
   conditions.
2. **Figure 6 as printed.** We transcribed Figure 6 (Section 2.5) to reconcile the paper's condition counts with our
   measured rates.

The two forms agree in every condition count used below once one unprinted matching condition is added and the
printed errata are corrected (Sections 2.6-2.8).

### 2.2 The local collision

Rows with a nonzero difference, from two-branch execution of Table 3 from CV35:

| Word | Signed difference (MSB first; u: M1 bit 1, M1′ bit 0; n: the reverse) | XOR | M1′ − M1 mod 2^32 |
| --- | --- | --- | --- |
| W4 | `--u-----------------------------` | 20000000 | e0000000 |
| W5 | `-----n---n----------u-----------` | 04400800 | 043ff800 |
| W6 | `--u-----------------------------` | 20000000 | e0000000 |
| W7 | `-------u-------n---n----n---n-n-` | 0101108a | ff01108a |
| W8 | `------------n-------nn----------` | 00080c00 | 00080c00 |
| W12 | `-----u---u----------n-----------` | 04400800 | fbc00800 |
| W13 | `--n-----------------------------` | 20000000 | 20000000 |
| W20 | `-------uu-------n---------------` | 01808000 | fe808000 |
| W22 | `--u-----------------------------` | 20000000 | e0000000 |
| A4 | `--u-----------------------------` | 20000000 | e0000000 |
| A5 | `-----u---u---u-n----u---n--n----` | 04450890 | fbbcf890 |
| A9 | `----------n--------------------n` | 00200001 | 00200001 |
| A11 | `----u---------n-n-------n--u----` | 08028090 | f8028070 |
| A12 | `-nu---n-u-------u---------------` | 62808000 | 217f8000 |
| A14 | `--n-----------------------------` | 20000000 | 20000000 |
| E4 | `--u-----------------------------` | 20000000 | e0000000 |
| E5 | `-----n---u-unn------u------n----` | 045c0810 | 03bbf810 |
| E6 | `---u-------u------u-n---u--u-u-n` | 10102895 | efefe76d |
| E7 | `--n------------u----------------` | 20010000 | 1fff0000 |
| E8 | `nnn-----------------------------` | e0000000 | e0000000 |
| E9 | `-----u-unnn--u-n----u---n--n-nuu` | 05e50897 | fbdcf891 |
| E10 | `nu-------------------n-n--------` | c0000500 | 40000500 |
| E11 | `----u---------n-n-------n-un----` | 080280b0 | f8028070 |
| E12 | `---nnn--nnnnnnnn--u----u-nnn----` | 1cff2170 | 1cfedf70 |
| E13 | `-u----nn-u-----n-n--uuu--------u` | 43414e01 | c2c131ff |
| E15 | `-------------n-------------u----` | 00040010 | 0003fff0 |
| E16 | `------n-u-------u---------------` | 02808000 | 017f8000 |
| E18 | `--n-----------------------------` | 20000000 | 20000000 |

All other rows A−4..A31, E−4..E31 and W0..W31 are zero. Our independent recheck found 0 mismatches
between this table and a fresh execution (Section 9). The published second blocks and their XOR difference ΔM are:

| Word | M1 (Table 3) | M1′ | XOR |
| --- | --- | --- | --- |
| W0 | c0008214 | c0008214 | 00000000 |
| W1 | ae65f3bf | ae65f3bf | 00000000 |
| W2 | e93c006a | e93c006a | 00000000 |
| W3 | 5f195aa9 | 5f195aa9 | 00000000 |
| W4 | a4d6cd0f | 84d6cd0f | 20000000 |
| W5 | 21811cec | 25c114ec | 04400800 |
| W6 | ea897317 | ca897317 | 20000000 |
| W7 | db9ec665 | da9fd6ef | 0101108a |
| W8 | 6ec17218 | 6ec97e18 | 00080c00 |
| W9 | 5100da8a | 5100da8a | 00000000 |
| W10 | 0912e57b | 0912e57b | 00000000 |
| W11 | a96b2054 | a96b2054 | 00000000 |
| W12 | 45f2222c | 41b22a2c | 04400800 |
| W13 | 4d12f88a | 6d12f88a | 20000000 |
| W14 | d2701ecc | d2701ecc | 00000000 |
| W15 | 140976d1 | 140976d1 | 00000000 |

The local collision has the following structure:
- Differences enter through W4..W8, W12 and W13.
- They live in A_i for i ∈ {4, 5, 9, 11, 12, 14} and in E_i for i ∈ {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18}.
- They vanish from step 19 on.

Every zero row after the first difference is an exact cancellation of the executed rows. Among them, these three involve
A14 and the expanded words W20 and W22. Each is exact for the executed rows: the sums below are 0 mod 2^32, which we
checked in the generator (δE18−δA14 = 00000000, δE16+δW20 = 00000000, δE18+δW22 = 00000000).

- **Step 18:** A18 = E18 − A14 + Σ0(A17) + MAJ(A17, A16, A15), so δE18 − δA14 = 0.
- **Step 20:** E20 = A16 + E16 + Σ1(E19) + IF(E19, E18, E17) + K20 + W20, so δE16 + δW20 = 0. This holds once
  IF(E19, E18, E17) blocks the bit-29 difference of E18, which requires E19[29] = 0 (printed in Figure 6).
- **Step 22:** E22 = A18 + E18 + Σ1(E21) + IF(E21, E20, E19) + K22 + W22, so δE18 + δW22 = 0. In between, step 21
  needs IF(E20, E19, E18) to block E18[29], which requires E20[29] = 1 (printed in Figure 6).

Step 18 makes A18 free of the A14 difference. Steps 20 and 22 keep E20 and E22 free of difference while E16 and E18
are still in the state. The other steps cancel in the same way and are covered by the conditions of Sections 2.4-2.7.
Examples are step 17, where δE13 + δΣ1(E16) + δIF(E16, E15, E14) = 0, and step 19, where
δE15 + δΣ1(E18) + δIF(E18, E17, E16) = 0.

The expanded words W20 and W22 therefore carry the differences that cancel E16 and E18. Every other expanded word up
to W31 must have zero difference (Section 2.4).

### 2.3 Truncation from 35 to 32 steps

**Lemma 2.** Let a pair (M1, M1′ = M1 ⊕ ΔM) follow the characteristic through step 31 from a chaining value CV. Then
C32(CV, M1) = C32(CV, M1′). The truncation to steps 0..31 imposes exactly the conditions of rows −4..31 of the 35-step
characteristic, and the rows for steps 32..34 add no condition.

*Proof.*
1. **Collision.** The rows A28..A31 and E28..E31 are zero, so both branches end in the same working state. The
   feed-forward adds the same CV to both.
2. **Rows 32..34 add nothing.** In the 35-step characteristic the words W32, W33 and W34 are
   σ1(W30) + W25 + σ0(W17) + W16, σ1(W31) + W26 + σ0(W18) + W17 and σ1(W32) + W27 + σ0(W19) + W18. Every term has a
   zero difference once rows up to 31 are followed, so these words have zero difference with no further condition.
   With zero state and message differences, steps 32..34 keep a zero difference with no condition.
3. **Consistency with Figure 6.** Figure 6 prints no condition at all, as a row symbol or in a relation, on A or E
   rows after row 20 or on W rows after row 22. This is counted over the transcription of
   Section 2.5. ∎

At 32 rounds the paper's second-block characteristic is therefore used unchanged on its first 32 steps. The target
changes only the first block: CV is C32(IV, M0) instead of C35(IV, M0). That changes the population of chaining values
against which TAB2 is matched. This is why q is measured on real C32 outputs (Section 4) and not taken from the paper.

### 2.4 Message-expansion conditions

For t = 16..31 the difference of W_t is determined by the four terms of its expansion. The terms of W16, W17, W18,
W25, W26, W30 and W31 all have zero difference, so these words need no condition. The nine remaining words are listed
below. "prefix" means that every term with a difference is fixed by W0..W13, so the condition is decided at matching
time and is part of the level-L2 test. "tail" means the condition involves W14, W15 or later expanded words. W20 has
one condition of each kind: its modular difference is decided at matching, its XOR and signed row only in the tail.

| Word | Equation | Required M1′−M1 (condition) | Phase |
| --- | --- | --- | --- |
| W19 | `W19 = s1(W17) + W12 + s0(W4) + W3` | 00000000 | prefix |
| W20 | `W20 = s1(W18) + W13 + s0(W5) + W4` | modular difference fe808000 | prefix (every differenced term, W13, σ0(W5), W4, is fixed by W0..W13; part of L2) |
| W20 | `W20 = s1(W18) + W13 + s0(W5) + W4` | XOR 01808000, signed row `-------uu-------n---------------`: 3 value bits and 7 σ1(W20) sign relations | tail |
| W21 | `W21 = s1(W19) + W14 + s0(W6) + W5` | 00000000 | prefix |
| W22 | `W22 = s1(W20) + W15 + s0(W7) + W6` | e0000000 | tail |
| W23 | `W23 = s1(W21) + W16 + s0(W8) + W7` | 00000000 | prefix |
| W24 | `W24 = s1(W22) + W17 + s0(W9) + W8` | 00000000 | tail |
| W27 | `W27 = s1(W25) + W20 + s0(W12) + W11` | 00000000 | tail |
| W28 | `W28 = s1(W26) + W21 + s0(W13) + W12` | 00000000 | prefix |
| W29 | `W29 = s1(W27) + W22 + s0(W14) + W13` | 00000000 | tail |

Each expansion addition has an exact XOR-differential probability at the realized differences. Once the trail fixes
one operand's signs, the other operand needs only the σ0/σ1 two-bit sign relations, which for W4..W8 and W22 are
exactly the relations printed in Figure 6. W20 costs 3 value bits and 7 σ1(W20) sign relations,
10 in all, which equals the measured W20 list fraction 2^-10. W22 costs 1 more bit. The experiments in Section 6 sample these additions.

### 2.5 Figure 6: transcription and conditions per attack phase

Figure 6 is a single embedded image on PDF page 16 with no text layer. Two readers transcribed all 113 rows
(A and E rows −4..34, W rows 0..34) and the 32 printed relations, which expand to 73
bit pairs:
- a manual reading of 600 and 1200 dpi renders of the embedded 1561×1796 px JPEG, whose native resolution is
  325 ppi, so both renders are upsampled;
- a template-matching machine reader.

They disagreed in 3 characters, and each disagreement was settled on the 1200 dpi render. Under the polarity of
Section 1.3, the transcription agrees with the two-branch execution of Table 3 over 35 steps in all 3616
characters (0 mismatches).

The figure prints an undefined `+` at E10[6] and E11[6]. Both bits equal 1 in both branches, and the derived
conditions imply E10[6] = E11[6], so the `+` most likely marks that two-bit condition.

We turned every printed symbol and relation into GF(2) equations on the values of one branch (the *printed* system). We
then derived the local conditions of the executed characteristic independently, bit by bit (the *derived* system):
- the signed difference of every word;
- the sign of every Σ0, Σ1, σ0 and σ1 output bit with an odd number of differing taps;
- exact enumeration of every IF and MAJ bit with a differing input.

Every derived condition is an affine bit equation; the derivation found 0 non-affine cases. Each
equation is assigned to the attack phase in which it is decided. The table gives independent conditions per phase as
GF(2) ranks, each conditional on the earlier phases. The rank columns are linear ranks, which ignore the constants of
the equations. A printed equation that the derived system contradicts, with the same bits and the opposite constant,
therefore counts as inside the span of the derived system. The "contradicted" column lists those equations:

| Phase | Words decided in the phase | Printed (rank) | Derived (rank) | Union (rank) | Printed, outside the linear span of derived | Printed, contradicted by derived | Derived, outside the linear span of printed |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| table | A−1..A13, E3..E13, W7..W13 (fixed by the TAB2 record) | 324 | 423 | 423 | 0 | 2 | 99 |
| matching | A−4..A−2, E0..E2, W0..W6 (decided by CV and record) | 14 | 15 | 15 | 0 | 0 | 1 |
| tailset_V | A14, A15, E14, E15, W14, W15 (tail set V) | 51 | 50 | 51 | 1 | 2 | 0 |
| tail | A, E rows 16 and later, W16 and later | 44 | 44 | 46 | 2 | 0 | 2 |

The algorithm does not use these counts. TAB2, matching, V and the final test all use exact execution. The counts
serve only to explain q and the tail rate.

The large table-phase gap is expected. Figure 6 prints most Σ, IF and MAJ sign conditions of the table words only
implicitly, and TAB2 is built by exact enumeration (Section 3). The union of both systems is inconsistent in
4 equations. The 3 printed equations outside the span of the derived system and the
4 contradicted ones are the 7 errata of Section 2.8.

### 2.6 Figure 6 and q (matching phase)

**Printed matching conditions.** The matching phase decides W4, W5 and W6, together with E0..E2 and A−4..A−2.
Figure 6 prints:

| Word | Printed row (paper symbols, MSB first) | Printed relations | Printed conditions | Derived conditions |
| --- | --- | --- | ---: | ---: |
| W4 | `==n=============================` | `W4[1,8] != W4[12,25]`; `W4[18] = W4[14]` | 4 | 4 |
| W5 | `=====u===u==========n===========` | `W5[0,1,30] = W5[28,18,9]` | 6 | 6 |
| W6 | `==n=============================` | `W6[1,8] = W6[12,25]`; `W6[18] != W6[14]` | 4 | 4 |
| E0 | `================================` | none | 0 | 0 |
| E1 | `================================` | none | 0 | 0 |
| E2 | `================================` | none | 0 | 0 |
| A-4 | `================================` | none | 0 | 0 |
| A-3 | `================================` | none | 0 | 0 |
| A-2 | `================================` | none | 0 | 0 |

That is 14 conditions in total. Each of W4, W5 and W6 contributes its difference bits plus the σ0
two-bit relations that make δσ0(W4) + δW12 = 0 (W19), δσ0(W5) + δW4 + δW13 = δW20 and δσ0(W6) + δW5 = 0 (W21) hold.
The derivation finds exactly one further necessary condition that is not printed. It is listed with the tail
corrections:

| Phase | Condition | Words | Status against the printed system |
| --- | --- | --- | --- |
| matching | IF(E4,E3,E2) bit 29, step 5 | E2, E3 | necessary, not printed |
| tail | MAJ(A16,A15,A14) bit 29, step 17 | A15, A16 | necessary, not printed |
| tail | IF(E18,E17,E16) bit 29, step 19 | E16, E17 | necessary, not printed |
| tail | `W20[4]=W20[6]` | W20 | printed, independent of the derived conditions: not a condition of the characteristic |
| tail | `W20[31]=W20[22]` | W20 | printed, independent of the derived conditions: not a condition of the characteristic |

E4's only difference is at bit 29, so the step-5 output IF(E4, E3, E2)[29] has the required difference only for one
relation between E2[29] and E3[29]. Figure 6's E2 row is all `=`.

**Lemma 3 (exact parametrisation).** Fix a TAB2 record r, which fixes A−1..A13, E3..E13 and W7..W13, and fix the CV
word A−1 = CV.a to the record's A−1. The maps

    (A−2, A−3, A−4) → (E2, E1, E0) → (W6, W5, W4)

are bijections of (Z/2^32)^3, given by the step equations solved for E_i (i = 2, 1, 0) and W_i (i = 6, 5, 4):

    E_i = A_i + A_{i−4} − Σ0(A_{i−1}) − MAJ(A_{i−1}, A_{i−2}, A_{i−3})
    W_i = E_i − A_{i−4} − E_{i−4} − Σ1(E_{i−1}) − IF(E_{i−1}, E_{i−2}, E_{i−3}) − K_i

*Proof.* Both maps are triangular translations:
- E2 depends on A−2 alone (plus record words), E1 on (A−3, A−2) and E0 on (A−4, A−3, A−2). Each is a translate of
  the newest argument.
- W6 depends on E2 alone, W5 on (E1, E2) and W4 on (E0, E1, E2). Again each is a translate of the newest argument.

E3, and with it W7..W13, depends only on record words, so it is consistent for every CV. W0..W3 then follow from
E−4..E−1 (Section 4). ∎

**Proposition (q).** Model a trial as follows: A−1 = CV.a is uniform, and (A−4, A−3, A−2) is uniform and independent
of A−1 (a uniform-CV model, used only to interpret q; the charged q is measured on real C32 outputs, Section 4.3).
Then

    q = 2^−32 · Σ_r P_r,

where P_r is the fraction of (W4, W5, W6) for which the record r passes L2. By Lemma 3, P_r is an exact count over
(W4, W5, W6). Steps 0..3 carry no difference. Apart from (W4, W5, W6) and E2 = c_r − W6, where c_r is a record
constant, every quantity the L2 test reads through step 13 is fixed by the record.

- **Printed bound.** The printed matching conditions are independent affine bit equations on (W4, W5, W6). In this
  phase 0 of them lie outside the linear span of the derived system and 0 are
  contradicted by it. The executed pair also satisfies all 14 (0 violations). They
  are therefore implied by the derived system, so they are necessary. Hence
  P_r ≤ 2^−14 for every r, and

      q ≤ 2^(29.1824 − 32 − 14) = 2^-16.818.

- **Exact value.** If the unprinted step-5 condition cost a full independent bit, q would be 2^-17.818. It
  costs less. E2 = c_r − W6, with W6[29] fixed by its difference and the rest of W6 restricted by its own
  conditions, so E2[29] is not a uniform bit independent of the record's E3[29]. The exact average cost over TAB2 is
  0.508 bit. The exact mean is P_r = 2^-14.508, and the exact analytic value is q = 2^-17.325. At
  level L1, without the 9 σ0 relation bits, the analytic value is 2^-8.325.
- **Measured.** Over 91,629 accepts in 2^33.807 real C32(IV, M0) trials we measure
  q = 2^-17.324, 95% interval [-17.333, -17.315] (Section 4). The ledger charges the worst end, 2^-17.333.

The printed figure plus one unprinted condition therefore accounts for the whole measured q:

| Quantity | Figure 6 printed | Derived from the pair | Measured | Paper |
| --- | ---: | ---: | ---: | ---: |
| matching conditions (W4..W6, IF5) | 14 | 15 |  |  |
| log2 q | -16.818 | -17.3254 | -17.324 [-17.333, -17.315] (charged pool) | -20.92 (e1080:786-787) |
| tail conditions | 44 | 44 | 43.994 (real), 44.004 (syn) | 45 (e1080:795-796) |

**The paper's 2^-20.92 (e1080:786-787).** This value lies 3.60 bits below our measurement and
4.10 bits below the upper bound implied by the paper's own Figure 6. No condition in Figure 6, printed or
derived, accounts for it. Under a uniform-CV model the number of first-block rounds does not enter q, so the change from 35
to 32 rounds does not explain it either. The paper gives no raw counts for this experiment. We report the value as an
unexplained discrepancy in the paper and do not use it. Stress row A of Section 7 prices it as a disclosed ceiling:
paper q with our yield gives 2^53.348. That total is dominated by the trail envelope and hides the effect. For
the attack phases alone (matching trials, lookups and tail enumeration at the central yield), paper q gives
2^47.358, against 2^43.762 at our measured q.

### 2.7 Figure 6 and the tail (44 conditions against the paper's 45)

The paper states 45 conditions on (A16, E16, E17, E18, E19, E20, W20, W22) (e1080:795-796) and derives that
2^27.415 valid prefixes are needed (e1080:796-797), from 2^17.585 tail values (e1080:795). Figure 6 prints these independent
conditions on those words:

| Word | printed conditions |
| --- | ---: |
| A16 | 0 |
| E16 | 14 |
| E17 | 5 |
| E18 | 7 |
| E19 | 1 |
| E20 | 1 |
| W20 | 12 |
| W22 | 4 |

That is 44 in total. Of the printed equations, 2 are not conditions of the
characteristic. Of the necessary conditions, 2 are not printed. Both are listed in the table of
Section 2.6:

- **Spurious W20 pair.** `W20[4,31] = W20[6,22]` is independent of the derived system, and the executed pair violates
  both halves. It repeats the W22 relation `W22[4,31] = W22[6,22]`. For W22 those are the σ1 sign conditions of its
  bit-29 difference, but W20 has no bit-29 difference. Without it, W20 carries 10 conditions, not
  12: its value bits plus its σ1 sign relations, as in Section 2.4.
- **Unprinted step-17 condition.** MAJ(A16, A15, A14) at bit 29 needs A16[29] = A15[29]. The paper names A16 among
  the tail words, but its A16 row is all `=`.
- **Unprinted step-19 condition.** IF(E18, E17, E16) at bit 29 constrains E17[29] against E16[29].

Corrected count: 44 − 2 + 2 = **44**, which equals the derived tail rank of
Section 2.5. The exact two-branch measurement gives a probability per V element of 2^−44.004 on synthetic
prefixes and 2^−43.994 on real C32 prefixes (Section 5).

The condition count therefore predicts a yield of 2^(17.585 − 44) = 2^-26.415 per
prefix, where we measure 2^-26.409 (charged at 2^-26.428). The paper's 45 gives 2^-27.415.

The paper's 45 equals the 44 printed conditions (including the spurious W20 pair)
plus one condition on A16, a word the paper lists among the conditioned words (e1080:795-796) but whose Figure 6 row is
all `=`. That is the most likely source of the extra condition, but it is an inference. Our charge
uses the measured yield, not either count.

### 2.8 Errata in the printed relations

Of the 73 printed bit pairs, 7 are violated by the executed Table 3 pair:

| Printed relation (relation line) | Bit pair | Violated by the executed pair | Against the derived conditions | Single-edit repairs consistent with the derived conditions |
| --- | --- | --- | --- | --- |
| `W20[4,31] = W20[6,22]` (3) | `W20[4] = W20[6]` | yes | independent | none (spurious) |
| `W20[4,31] = W20[6,22]` (3) | `W20[31] = W20[22]` | yes | independent | none (spurious) |
| `E7[21,10] != E7[3,15]` (6) | `E7[21] != E7[3]` | yes | contradicted | operator inverted |
| `E7[21,10] != E7[3,15]` (6) | `E7[10] != E7[15]` | yes | contradicted | operator inverted |
| `A14[18,8] = A14[6,17]` (9) | `A14[18] = A14[6]` | yes | contradicted | operator inverted |
| `A14[18,8] = A14[6,17]` (9) | `A14[8] = A14[17]` | yes | contradicted | operator inverted |
| `A15[29] = A6[29]` (9) | `A15[29] = A6[29]` | yes | independent | left word A15 -> A2, left word A15 -> A3, right word A6 -> A10, right word A6 -> A11, right word A6 -> A16 |

Notes on the errata:
- The E7 and A14 relations are the Σ1(E7) and Σ0(A14) sign conditions with the operator inverted. The executed pair
  satisfies the opposite operator, and the derived system contradicts the printed one.
- `A15[29] = A6[29]` is not implied by the derived system. It becomes implied after the single edit A6 → A16, which
  turns it into the unprinted step-17 condition above. Other single edits also work, so this is a likely typo, not a
  certainty.

None of these errata affects the algorithm. The E7 relation belongs to the table phase and the A14 relations to the
tail set V, and both TAB2 and V are enumerated by exact execution against the executed rows. The W20 and A15 items
affect only the condition counts reconciled above.

## 3. Start point and TAB2 (preprocessing)

### 3.1 Start point T and the start-point search cost Tsat

#### 3.1.1 The start point

Step 1 of the attack (e1080:748-755) first finds one valid solution of

```
T = (A1..A13, E5..E13, W9..W13),
```

that is, an assignment of these 27 words under which both message branches follow the characteristic through the
rows these words determine. The 35-step attack uses a single solution (e1080:897-898). We do the same and hard-code
the published one: the realized states of the Table 3 pair evaluated from its 35-round chaining value. These words
are part of the nonuniform advice, and the cost of producing such a solution is charged in time (Section 3.1.2).

| Words | Table 3 realized state (published T) |
| --- | --- |
| A1..A13 | 66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6 4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0 |
| E5..E13 | 58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69 2300f189 fcc08ef5 |
| W9..W13 | 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a |

TAB2 (Section 3.2) keeps A4..A13, E8..E13, W12 and W13 of T fixed; the paper's SHA-512 paragraph names exactly this fixed set
(e1080:893-895). It re-enumerates E5, E6 and E7, as the paper does
(e1080:778), and recomputes A1..A3 and W9..W11 for each re-enumerated triple. The paper's sentence "we fix
(Ei)5≤i≤13, (Ai)1≤i≤13, and (Wi)9≤i≤13" (e1080:775) cannot be meant literally together with that re-enumeration.
The step equation A5 = E5 − A1 + Σ0(A4) + MAJ(A4, A3, A2) forces A1..A3 to change when E5..E7 change and A4..A7 stay
fixed. The same holds for W9..W11, whose step sums contain E5..E7.

#### 3.1.2 Tsat: charged at the 2^41 cap; a measured search corroborates it

The paper gives 2^34.3 for finding a valid solution in Step 1 (e1080:792-793) but states no unit. Its SHA-512
analogue, the time to find the original valid T (e1080:902), is also unitless. We therefore do not use that figure.
Tsat is therefore charged at the cap: **Tsat = 2^41.000 units**.
The reason is Section 3.1.3: our measured independent start point failed gate G5, so the cost of finding it does not measure the
cost of finding a start point like the published T. We report that measurement as corroboration only.

**The corroborating measurement.** We measured the cost of finding a start point ourselves, with our own encoding and solver:

- **Encoding (`cnf2b.py`).** A two-branch CNF for steps 4..15. The unknowns are the branch-1 words A0..A15, E0..E15 and W4..W15.
  Branch 2 gets no variables: each of its words is the branch-1 word XOR the realized difference, and the branch-1 bits
  at the difference positions are fixed, so every word carries its realized signed difference.
- **Constraints.** All are taken from the characteristic file:
  - the step equations (e1080:320) for steps 4..15;
  - the realized signed differences of the outputs of Σ0, Σ1, IF, MAJ and σ0 in every step, and of IF and MAJ in step 16;
  - the single-bit value conditions propagated by nldtool.

  Every term of every step sum carries its realized modular difference, so the branch-2 step equations follow from
  the branch-1 ones. This system is stricter than the paper's Step 1: it also constrains rows 14 and 15 and the step-16
  Boolean functions, so any solution comes with a non-empty tail set.
- **Self-test.** The published pair, fixed by unit clauses, must be satisfiable, and each single-bit flip of a
  constrained word must be unsatisfiable: `selftest_pub` SAT (20261004T162836-7cd288); `neg_E9_3` UNSAT (20261004T162836-2935a3); `neg_W13_0` UNSAT (20261004T162836-2bc233); `neg_A2_5` UNSAT (20261004T162836-dd0273). The published T therefore solves the same system.
- **Solver.** CaDiCaL 1.9.5 (through pysat), one thread per member, run as a portfolio of randomly permuted CNFs. The first
  SAT result stops the other members. Every member, including killed ones, is metered by its retired instructions.

| Quantity | Value |
| --- | --- |
| charged runs (solver runs) | 44 (23) |
| CPU-hours | 2.712 |
| instructions | 3.66e+13 (2^45.06) |
| Tsat charged | 2^41.000 units (cap) |
| measured independent search, re-summed (corroboration only) | 2^33.938 units |
| winning run | 20261004T163012-4b1236 (2^31.03 units) |
| full-CNF portfolio: successes / solver runs | 1 / 12 |
| 95% upper bound on expected cost | 2^39.00 units (cap 2^41) |
| total with Tsat at that upper bound | 53.326 |
| paper (unitless, not claimed) | 2^34.3 (e1080:792-793) |

**What it shows.** The search used 44 runs (23 of them solver runs, 2.712 CPU-hours) and
2^33.938 units in total; the winning run alone cost 2^31.03 units. The total includes a two-stage
attempt that was not used: stage 1 covered rows up to 13 only and found 4 of 7 solutions, and
stage 2 then fixed those solutions and solved rows 14 and 15, UNSAT in 4 of 4 cases. None of
these runs is the Tsat charge. All of them are charged as logged work in the conservative ledger's all-runs line.

One success is a single sample of a random solve time, so we also bound the expected cost. The full-CNF portfolio had
1 success in 12 members and used 2^33.695 units. Assume memoryless solve times (a heuristic
used only for this bound). The exact one-sided 97.5% (two-sided 95%) upper bound on the expected cost per success is then
the exposure divided by the lower 2.5% Poisson limit for one event, 0.0253. That gives 2^39.00 units, which is
2.00 bits below the charged cap, and the measured total is 7.06 bits below it. This is
the sense in which the cap is generous. It rests on one sample of one start point's search, so it is corroboration, not
a charge.

**Effect on the claim (not charged).** With Tsat at that upper bound instead of the cap, the conservative total would be
2^53.326 rather than 2^53.327. After the declared 0.05-bit slack and rounding up, both give the claimed
`time_log2` of 53.38. Reading the paper's unitless figure as compressions would
give 2^53.326. We claim neither alternative.

#### 3.1.3 The independent start point T′ and why the published T stays primary (gate G5)

The solution T′ was completed backwards to a full second block (W0..W3 are free and difference-free, and the chaining
value is back-solved). It was then checked by our own tracer and by the trusted `verifier/hash_functions.py` at 16 rounds.
T′ shares 4 of its 27 words with the published T (E5, E11, E12, E13):

| Words | Published T (Table 3 realized) | Independent T′ (stream B) |
| --- | --- | --- |
| A1..A13 | 66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6 4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0 | fac482d4 e004ff1b 6fc1181f 7fa4f6b4 07441c6b 749713df b6a7b1df d03df959 0b9cec98 b2e38035 7eb5177d bd93c1fa 9f8e19f0 |
| E5..E13 | 58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69 2300f189 fcc08ef5 | 58f38fac b1df6594 8f539562 1bc8b69e d504be2b 7f27924c bf893f69 2300f189 fcc08ef5 |
| W9..W13 | 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a | 66facd50 30ba344c e2fa6747 b5dff0cf 8648579e |

We ran the unchanged phase-1 pipeline on T′: tail set V′, TAB2′, q′ on 2^31 real C32 trials, and yield′ on
4,000 real cores.
- q′ = 2^-18.823 [-18.865, -18.781] from 4,631 accepts.
- Yield′ = 2^-24.034 [-24.066, -24.002] from 32,000 paths, with 14,074 exactly verified successes.
  An independent replicate gave 2^-24.025.

| Quantity | Published T (primary) | Independent T′ | Δ (bits) |
| --- | ---: | ---: | ---: |
| log2 \|V\| | 17.585 | 20.000 | 2.415 |
| log2 TAB2 records | 29.182 | 27.552 | -1.631 |
| non-empty (E5, E6, E7) triples | 1794 | 653 |  |
| log2 q analytic | -17.3254 | -18.8489 | -1.524 |
| log2 q measured (published T: charged pool, Section 4.3; T′: its own run) | -17.3238 | -18.8229 | -1.499 |
| log2 yield (real cores) | -26.4089 | -24.0336 | 2.375 |
| log2 matching trials per success (−log2 q − log2 yield) | 43.733 | 42.856 | -0.876 |
| G5 (within 0.5 bit) |  | FAIL |  |

Our gate G5, fixed before the comparison, required: "q' and yield' within 0.5 bit of the published-T values". It failed: the two values
move in opposite directions by more than that. Under the stop rule, the published T stays primary. Every online number
in this proof (TAB2, q, V, yield) is a published-T number. The variation is a property of the start point, not a defect:
- V′ has 2^20.0 elements over 64 admissible W14, against 2^17.585 for the published T.
- TAB2′ has fewer records.

Because G5 failed, the measured cost of finding T′ is not charged as Tsat (Section 3.1.2). The comparison above is context
only. An algorithm that hard-coded T′ instead of T would need 2^42.856 rather than 2^43.733 first-block trials
per success (0.876 bit fewer), according to the smaller T′ samples. We do not claim that improvement.

### 3.2 TAB2: construction, reading of the paper and counts

#### 3.2.1 Reading of the construction (gate GT)

The paper's text for the TAB2 trick (e1080:778-780) says: "we re-enumerate the already fixed E5, E6, and E7 ... We then
sequentially enumerate W4 to verify E8, and subsequently enumerate W7 to verify E3". We read "W4 to verify E8" as a
typo for **"W8 to verify E4"** (indices 4 and 8 swapped). The evidence:

1. **The literal reading is vacuous.** E8 = A4 + E4 + Σ1(E7) + IF(E7, E6, E5) + K8 + W8 (e1080:320) has no W4 term, so
   an E8 check passes for every W4. Moreover, W4 = E4 − A0 − E0 − Σ1(E3) − IF(E3, E2, E1) − K4 (e1080:859) depends on
   E0..E2 and hence on the chaining value (e1080:854-855), so W4 cannot be fixed at table time. Storing it would multiply
   the table by the 2^28 admissible W4 values, to 2^57.2 records.
2. **The corrected reading matches the procedure.** Step 1 (e1080:751-753) and the general framework (e1080:376-381)
   both say: exhaust (W8, E4) to obtain A0, then (W7, E3) to obtain A−1.
3. **The corrected reading reproduces the paper's count exactly.** The enumeration below gives 609,229,824 records,
   2^29.18241, against the paper's 2^29.1824 (e1080:781 and :803). The re-enumeration tests
   81,920 (E5, E6, E7) triples (64 × 10 × 128 values). Among the non-empty
   triples there are 8, 10 and 48 distinct values, against the paper's
   8, 16 and 2,048 (e1080:779). Only the non-empty E5 count matches.
   Dropping one necessary Boolean relation from the predicate (the step-6 IF condition E4[22] = E3[22]) gives
   2^30.3795 records, which does not match. For the published triple, this relaxed predicate reproduces the
   593,920-record base table of HashSmash PR #166 byte for byte; that table was used for comparison only. That relation is necessary:
   3,000 base-slice records of each kind were each tried with 200 random chaining values matched on
   A−1 (600,000 trials per kind), under exact two-branch execution of steps 0..8:
   - records violating the relation passed all of those steps 0 times;
   - records satisfying it passed 16,531 times (2^-5.18).

**Unresolved.** The paper's per-word counts for E6 and E7, 2^4 and 2^11 (e1080:779), are not
reproduced as distinct-value counts, either over the tested values (10 and 128) or over the
non-empty triples (10 and 48, in 1,794 non-empty triples). The record total is
exact, so this does not affect the table.

#### 3.2.2 Enumeration (exact predicates)

A4..A13, E8..E13, W12 and W13 are fixed to the published T. The enumeration has three levels, and each check is a check of
the realized difference in both branches:

1. **Triples (E5, E6, E7).** E5..E7 carry their realized signed differences. A1, A2, A3, W9, W10 and W11 are recomputed and must
   be difference-free. The modular differences of Σ1(E5), Σ1(E6) and Σ1(E7), of IF in steps 8-10 and of MAJ in steps
   5-7 must equal the realized ones, with exact selector prefilters for IF in steps 6 and 7.
2. **W8 for each surviving triple.** W8 ranges over its 1,048,576 = 2^20 admissible values: the realized
   signed difference and the realized σ0(W8) modular difference, which is the prefix condition of W23. Each W8 determines,
   in both branches,

   ```
   E4 = E8 − A4 − Σ1(E7) − IF(E7, E6, E5) − K8 − W8
   A0 = E4 − A4 + Σ0(A3) + MAJ(A3, A2, A1)
   ```

   We require the realized XOR and modular difference of E4, the realized differences of Σ1(E4) and IF(E6, E5, E4),
   that the step-7 sum leaves E3 difference-free, and a difference-free A0.
3. **W7 for each surviving (W8, E4, A0).** W7 ranges over its 524,288 = 2^19 admissible values. Each W7 determines

   ```
   E3  = E7 − A3 − Σ1(E6) − IF(E6, E5, E4) − K7 − W7
   A−1 = E3 − A3 + Σ0(A2) + MAJ(A2, A1, A0)
   ```

   We require the realized modular difference of IF(E5, E4, E3), which includes E4[22] = E3[22]. The record is
   (A−1; combo, W8, W7). E3, E4 and A0 are recomputed from it.

The conditions decided online (IF(E4, E3, E2) in step 5, the W4..W6 conditions, and E0..E2) depend on the chaining
value and are checked at matching time (Section 4).

| Quantity | Value | log2 |
| --- | ---: | ---: |
| (E5,E6,E7) combinations tested | 81,920 | 16.32 |
| non-empty (E5,E6,E7) triples | 1,794 | 10.81 |
| admissible W8 / W7 values | 1,048,576 / 524,288 | 20 / 19 |
| (W8,E4,A0) survivors | 155,008 | 17.24 |
| TAB2 records | 609,229,824 | 29.18241 (paper 2^29.1824) |
| distinct A_-1 keys | 193,525,282 | 27.53 |
| max records per key | 104 |  |
| order-independent checksum | `ae8b4a3c82b3b051` |  |
| compact record size | 6 B; 3,655,378,944 B total |  |

**Base slice and checksums.** For the published triple alone (the base slice) there are 44 (W8, E4, A0)
survivors, 205,824 records and 135,936 distinct keys, checksum `c32e82b21ead1ca9`. The realized record
is present. Two independent builders reproduce the full-table count and the order-independent checksum
`ae8b4a3c82b3b051`, one of them after an encode/decode round trip of the compact format.

#### 3.2.3 Storage and cost

- **Storage.** Records are stored in 6 bytes: the low byte of A−1 plus indices of W7 and of the (combo, W8)
  survivor. They are bucketed by A−1 ≫ 8 with a 64 MiB offset array and a 512 MiB A−1 bitmap. Matching keeps this
  structure resident.
- **Build.** The full build took 21.2 s on 12 threads with peak RSS 7.33 GB.
- **Charges.** The ledger charges one build at 2^31.395 units. The equivalent compact builder (2^30.92) is
  the same table and is not charged twice in the central ledger. The conservative ledger charges every logged run. The
  triple enumeration is charged at 2^27.108 units.

## 4. First block: matching C32(IV, M0) against TAB2

### 4.1 From a chaining value and a record to the prefix

**One trial.** Draw M0 and compute CV = C32(IV, M0) exactly. This is one charged target compression, and no
midstate credit is taken. Read CV = (a, ..., h) as (A−1, A−2, A−3, A−4, E−1, E−2, E−3, E−4). Look up A−1 in TAB2;
there are 0.142 matching records per trial on average. Each matching record r determines A0..A3, E3..E7 and
W7..W11. Together with the words fixed by T (A4..A13, E8..E13, W12 and W13), the CV words A−2..A−4 and E−1..E−4 determine the rest.

**Completing the prefix.** The step equations then determine everything else, in this order:

```
E2 = A2 + A−2 − Σ0(A1) − MAJ(A1, A0, A−1)          (e1080:855)
E1 = A1 + A−3 − Σ0(A0) − MAJ(A0, A−1, A−2)
E0 = A0 + A−4 − Σ0(A−1) − MAJ(A−1, A−2, A−3)
W_i = E_i − A_{i−4} − E_{i−4} − Σ1(E_{i−1}) − IF(E_{i−1}, E_{i−2}, E_{i−3}) − K_i     for i = 0..6   (e1080:857-859)
```

This gives M1's words W0..W13; W14 and W15 stay free. M1′ = M1 ⊕ ΔW, with ΔW nonzero exactly in W4..W8, W12 and W13.

**Acceptance levels.**
- **L1:** exact two-branch execution of steps 0..13 from CV gives the realized XOR and signed differences on W0..W13 and on
  A and E rows −4..13.
- **L2:** L1 plus the five prefix-determined expansion conditions. With Δ the modular difference M1′ − M1:
  - Δσ0(W4) + ΔW12 = 0 (W19);
  - Δσ0(W6) + ΔW5 = 0 (W21);
  - ΔW13 + Δσ0(W5) + ΔW4 = the realized modular difference of W20;
  - Δσ0(W8) + ΔW7 = 0 (W23);
  - Δσ0(W13) + ΔW12 = 0 (W28).

L2 is the paper's "valid (A−4, ..., A13, E−4, ..., E13, W0, ..., W13)" (e1080:785-789) at 32 steps. A trial is
accepted if some matching record passes L2; an accepted (CV, record) pair is a *valid prefix*.

### 4.2 Lemma (bijections) and the analytic q

**Lemma.** Fix a record r and A−1.
- (a) The map (A−2, A−3, A−4) ↦ (W6, W5, W4) is a bijection of (Z/2^32)^3.
- (b) Given everything else, the map (E−1, E−2, E−3, E−4) ↦ (W3, W2, W1, W0) is a bijection.
- (c) Whether a trial is accepted at L2 depends on the chaining value only through A−1, A−2, A−3 and A−4.

*Proof.*
- (a) E2 = A−2 + c2 and W6 = c6 − E2, where c2 and c6 depend only on r. E1 = A−3 + c1(A−2) and W5 = c5(E2) − E1.
  E0 = A−4 + c0(A−2, A−3) and W4 = c4(E2, E1) − E0. Each new variable enters additively with a coefficient of 1,
  so the map is triangular and invertible.
- (b) W3 contains −E−1 additively and no other E−k. W2 contains −E−2 additively, plus E−1 inside IF. W1 and W0
  continue the same pattern. The map is again triangular.
- (c) W0..W3 and rows −4..−1 carry no difference, so L1 and L2 place no condition on them. Every condition on rows
  0..13 and W4..W13 is a function of r and (W4, W5, W6), or equivalently of (A−2, A−3, A−4).

**Analytic q.** Model the CV words as uniform and independent for uniform M0 (a uniform-CV model, used only to interpret
q; the charged q is measured, Section 4.3). Then (W4, W5, W6) is uniform for each record, and the per-record acceptance probability is

```
P_r = N4 · N5 · n6(r) / 2^96,      q = 2^-32 · Σ_r P_r .
```

- **N4 and N5.** N4 = 2^28 and N5 = 2^26 count the W4 and W5 values with the realized signed difference and
  the realized σ0 modular difference: 4 and 6 conditions, exactly Figure 6's printed counts for
  these words.
- **n6(r).** This counts the admissible W6 (4 conditions) for which, with E2 = c6 − W6, the step-5 IF(E4, E3, E2)
  difference is realized. E4's only difference is at bit 29, so this is the condition E2[29] versus E3[29], which
  Figure 6 does not print. Its average effect over TAB2 is 2^-0.508. The mean of P_r over records is
  2^-14.5078.
- **Result.** The exact sum is q = 2^-17.3254.
- **Check of the formula.** The fast predicate and the formula were compared with exact two-branch evaluation on
  1,048,576 constructed and random samples, with 0 mismatches. A Monte Carlo test of L1 on
  67,108,864 trials gave z = -0.515.

Figure 6's printed matching conditions alone (14) would give the upper bound q ≤ 2^-16.818. Counting
the unprinted step-5 condition as a full independent bit would give 2^-17.818. The exact record-dependent average
lies between these two values.

### 4.3 Measured q on real C32 outputs

The charged q does not use the uniform-CV model. It is measured on real C32(IV, M0) outputs with the full table.
- **Sampling.** In each chunk, words 0..14 of M0 come from a seeded generator and word 15 enumerates a counter. The
  chunk's M0 values are distinct, and each C32 is computed exactly; reusing the first 12 steps saves time but earns
  no credit.
- **Counting.** Accepts are counted as lines of the saved accept files.
- **Intervals.** Garwood for k ≤ 3000, normal approximation otherwise.
- **Excluded runs.** Two further full-table runs have no accept file and are not pooled: a fourth seed whose count
  survives only as a metric line, and stream M's hunt benchmark (below), which kept per-chunk counts only.

| Run | Table | Seed | Trials | Accepts (L2) | log2 q [95%] |
| --- | --- | ---: | ---: | ---: | ---: |
| 20261004T145920-2bb844 | full | 2 | 2^33 | 52,275 | -17.326 [-17.339, -17.314] |
| 20261004T150227-7242f7 | full | 3 | 2^32 | 26,214 | -17.322 [-17.340, -17.305] |
| 20261004T155436-ad99be | full | 9 | 2^31 | 13,140 | -17.318 [-17.343, -17.294] |
| **pool, full** | full |  | 2^33.807 | 91,629 | **-17.324 [-17.333, -17.315]** |
| 20261004T145842-45cdd5 | base | 1 | 2^36 | 165 | -28.634 [-28.863, -28.414] |
| 20261004T150200-db7b8b | base | 2 | 2^36 | 167 | -28.616 [-28.844, -28.398] |
| 20261004T155314-ed5946 | base | 9 | 2^35 | 84 | -28.608 [-28.934, -28.300] |
| pool, base slice | base |  | 2^37.322 | 416 | -28.621 [-28.764, -28.483] |

The charged value is q = 2^-17.324 [-17.333, -17.315] (91,629 accepts in 2^33.807 trials). The
conservative ledger uses the 95% worst end, 2^-17.333. In the table below, the first four rows (charged count, per distinct M0, analytic sum and
per-record estimator) agree within 0.003 bit. The unpooled metric-only seed, 2^-17.311
[-17.336, -17.286], contains the charged value.

| Estimate | log2 q |
| --- | ---: |
| real C32(IV,M0), pooled accept-file counts (charged) | -17.324 |
| per distinct accepting M0 | -17.327 |
| exact analytic sum over TAB2 records, uniform CV | -17.325 |
| independent per-record estimator (tail engine, 2^29 attempts) | -17.325 |
| metric-only seed run (no accepts file; not pooled) | -17.311 (13,208) |
| paper, 35 steps (e1080:786-787) | -20.92 |
| Figure 6 printed conditions, upper bound | -16.818 |

Stream M's hunt benchmark (run 20261004T163104-741220, seed 303, 2^33 trials; per-chunk counts only, no accepts
file, not pooled) measured 52,045 L2 accepts over 128 chunks: 2^-17.3325 [-17.345, -17.320],
the lowest point estimate so far. It is homogeneous with the other four full-table runs (χ² = 3.09, 4 df).
Pooling all five gives 2^-17.3256 [-17.3328, -17.3185], inside the charged worst end 2^-17.3332, so the claim does
not change.

Checks of the accepts:
- Every accept is an L2 prefix by exact execution.
- Separately, an independent Python recheck recomputed each CV with the trusted verifier and each trail check with a
  separate checker (no shared code with the matcher): base slice 332/332 confirmed, 0 CV mismatches; full table 2000/2000 confirmed (every 26th), 0 CV mismatches.
- An in-run audit of 7,137,065 record matches against exact evaluation found 0 mismatches.
- Clustering check, as recorded by the matcher: per-chunk (2^20 trials) variance/mean = 0.997-1.000: Poisson, no clustering.
- The review recheck (Section 9.1) re-verified further samples with a fresh tracer.

### 4.4 Comparison with the paper

The paper reports that a random M0 gives a valid prefix with probability about 2^-20.92 at 35 steps (e1080:786-787).
Our measured q is 3.60 bits higher.
The step count does not explain the gap: the matching conditions lie on W4..W6 and rows up to 13, which are the same at
32 and 35 steps, and only the source of the chaining value differs (C32 here, C35 there).

The paper's own Figure 6 bounds q at 2^-16.818 (14 printed conditions on W4..W6). Evaluating the one
necessary unprinted step-5 condition exactly per record (average effect 2^-0.508) gives our analytic 2^-17.3254;
counting it as a full independent bit would give 2^-17.818. No condition in Figure 6, printed or derived,
accounts for the paper's 2^-20.92. We therefore treat it as an unexplained statement of the paper and do not use it.
The ledger keeps it only as a disclosed stress row (2^53.348 total; Section 7).

### 4.5 Per-trial cost

The production matching path costs 86.6 retired instructions per trial, measured as the marginal
difference between two run lengths. Of these, 41.9 are the SHA computation and 44.7 are bitmap,
bucket search, the fast W4/W5/W6/IF5 test and exact rechecks. Each trial is charged 1 unit for the compression.
- The central ledger adds the 44.7 lookup instructions × λ/C (line A2-match-lookup).
- The conservative ledger adds all 86.6 instructions on top of the unit, which double-counts the SHA part.

## 5. Second block: the (W14, W15) tail

### 5.1 Rows 14 and 15: the tail set V by inversion

Rows 10..13 (A10..A13, E10..E13) are fixed by T for every record and every prefix. In both branches,

```
E14 = W14 + [A10 + E10 + Σ1(E13) + IF(E13, E12, E11) + K14],     A14 = E14 − A10 + Σ0(A13) + MAJ(A13, A12, A11)
E15 = W15 + [A11 + E11 + Σ1(E14) + IF(E14, E13, E12) + K15],     A15 = E15 − A11 + Σ0(A14) + MAJ(A14, A13, A12)
```

The bracketed terms depend only on T (and on W14 for row 15). So W14 ↦ (E14, A14) and, for fixed W14, W15 ↦ (E15, A15)
are bijections that do not depend on the prefix.

**Definition of V.** V is the set of (W14, W15) under which, in exact two-branch execution:
- A14, E14, A15 and E15 carry their realized signed differences;
- the step-16 IF(E15, E14, E13) and MAJ(A15, A14, A13) outputs carry their realized XOR differences;
- the nldtool single-bit value conditions on rows 14 and 15 hold.

These are conditions on (W14, W15) alone, so V is computed once, by exhaustive inversion: every W14 ∈ [0, 2^32) is
tested, then every W15 for each admissible W14.

**Size and checks.**
- V has 196,608 = 2^17.585 elements: 12 admissible W14 values with 16,384 W15 values each. This
  equals the paper's count (e1080:795).
- V contains the published (W14, W15). The SHA-256 of its sorted big-endian encoding begins `25fb017b0432d084`.
- Without the nldtool value conditions the set has 6,291,456 = 2^22.585 elements. Elements outside V did not
  survive in practice: in the wide-set run, 181,163 paths drawn outside V contributed zero weight, against
  5,749 paths inside V, and the wide-set yield equals the V yield (Section 5.4). The extra bits are bookkeeping, as
  in the paper.

The remaining conditions concern rows 16 and later and the expanded words W16..W31. Among those words, only W20
and W22 carry differences; W19, W21, W23 and W28 were already enforced at L2. The tail conditions on
(A16, E16..E20, W20, W22) are counted in Section 5.6.

### 5.2 The W20 prefilter and the tail step of the algorithm

W16, W18 and W20 depend on the prefix and on W14 but not on W15:

```
W16 = σ1(W14) + W9 + σ0(W1) + W0,   W18 = σ1(W16) + W11 + σ0(W3) + W2,   W20 = σ1(W18) + W13 + σ0(W5) + W4 .
```

**The list L20.** L20 is the set of W20 values with two properties:
- W20 carries the realized signed difference, with W20′ = W20 + (the realized modular difference);
- σ1(W20′) − σ1(W20) equals the modular difference that W22's equation requires.

L20 has 4,194,304 elements, a fraction 2^-10, and contains the realized W20. W20 ∈ L20 is a necessary condition, so
filtering on it loses nothing.

**Step 3 for one valid prefix (e1080:770-771).**

1. For each of the 12 admissible W14, compute W20. If W20 ∉ L20, skip this W14.
2. For each of the 16,384 W15 with (W14, W15) ∈ V, run exact two-branch evaluation of steps 16..31 in natural
   order (W_i, E_i, A_i), stopping at the first violated item.
3. A candidate that passes every item is rechecked by full exact evaluation from CV through 32 steps, together with
   equality of the two C32 outputs. On success, output (M0 ‖ M1, M0 ‖ M1′) and stop.

**Measured on real prefixes.** W14 passes the prefilter at rate 2^-9.947 (954 of 941,868),
so the step evaluates 12 × 2^-9.947 × 16,384 ≈ 199 candidates per prefix on average.

**Measured cost (synthetic prefixes; defective tool, unbiased in expectation, Section 5.7).**
- The step costs 37,430 retired instructions per prefix (16.83 units). This is the difference of two runs
  (20261004T153639-5e5a23 and 20261004T153648-563e16) over the same 1,494,016 synthetic prefixes, with and without the tail.
- The ledger charges it on the capped number of tail calls (line A3-tail-enum, 2^31.501 in the conservative ledger).

### 5.3 Yield per valid prefix: estimator

The yield Y is the expected number of (W14, W15) ∈ V that complete a 32-step collision, per valid prefix. The ledger uses
Y as the expected number of collisions per prefix; the Poisson treatment of the total count belongs to the
success-probability section. At Y ≈ 2^-26.409, exhaustive enumeration cannot measure Y directly, so we use an
exact-ratio splitting estimator.

**Reparametrization.** Fix a *core*: a record together with (A−4, A−3, A−2), which fixes rows −4..13 except
E−4..E−1, and W4..W13. Fix also v = (W14, W15) ∈ V. By Lemma Section 4.2(b), uniform (E−4..E−1) is the same as uniform
(W0..W3). For fixed v, (W0..W3) maps bijectively to (W16, W17, W18, W1):
- W16 ↔ W0 given W1;
- W17 = σ1(W15) + W10 + σ0(W2) + W1 ↔ W2 given W1, because σ0 is a GF(2)-linear bijection;
- W18 = σ1(W16) + W11 + σ0(W3) + W2 ↔ W3.

**Stages.** The four stages draw, in order:

| Stage | Word drawn | Draws | Checks (each uses only words already fixed) |
| --- | --- | ---: | --- |
| 1 | W16 | 32,768 | rows 16 and 17 exact. W17 is a difference-free dummy here; row 17 has no difference, so its check does not depend on the dummy. |
| 2 | W17 | 256 | row 18 modular difference |
| 3 | W18 | 16,384 | row 18 exact; W20, W22, W24 exact; row 19 modular difference |
| 4 | W1 | 128 | back-solve W0, W2, W3; all remaining words and rows 19..31 exact |

**The splitting step.** At each stage the estimator draws the listed number of values, counts the s_k that pass, and
continues from one passing value chosen uniformly. The path weight is Π f_k · s_k / N_k. Its expectation equals the
probability that a uniform (W0..W3), together with v, passes all 32 steps (tower property).

**Importance factors.** Both factors are exact and are applied only to necessary conditions:
- Stage 1 fixes the 3 branch-1 bits of E16 at its difference positions. E16 is an affine bijection of W16,
  so f1 = 2^-3.
- Stage 3 draws W20 uniformly from L20 and sets W18 = σ1^{-1}(W20 − W13 − σ0(W5) − W4), so f3 = 2^-10.

The yield per prefix is |V| times the mean weight, with v drawn uniformly from V for each path.

**Checks of the estimator.**
- A run without importance factors (draws 262,144 and 4,194,304 at stages 1 and 3) gives 2^-26.454 from 179
  successes on 541 paths. This is consistent with the charged value, given the statistical error of
  179 successes.
- Every path that reaches the end is rebuilt as a full second block with its back-solved chaining value and rechecked
  by exact evaluation through 32 steps, including C32 output equality: 265,333 real-core successes and 155,432
  synthetic ones, with 0 and 0 failures.
- Independent samples are re-verified with the trusted verifier (Section 9.1).

These successes are 32-step **compression** collisions from chaining values whose E-words were resampled. They are
not two-block collisions from the IV, and this proof does not call them target collisions.

### 5.4 Yield results

| Estimate | Prefixes / paths | log2 yield per prefix [95%] |
| --- | ---: | ---: |
| real C32 cores (charged) | 78,489 / 627,912 | -26.409 [-26.417, -26.402] |
| synthetic prefixes | 23,050 / 368,800 | -26.419 [-26.428, -26.410] |
| wide tail set 2^22.585 | 11,682 / 186,912 | -26.425 [-26.511, -26.355] |
| plain (no importance factors) | 541 | -26.454 |
| conservative end used (min of four 95% lower ends) |  | -26.428 |
| paper (e1080:796-797) |  | -27.415 |

| Stage (free words) | mean conditional log2 rate |
| --- | ---: |
| stage 1 | -15.004 |
| stage 2 | -4.999 |
| stage 3 | -21.997 |
| stage 4 | -2.000 |
| product of stage means | -44.000 |
| measured joint per candidate | -43.994 |
| dependence gap (bits) | 0.0066 |
| design effect (core clusters) | 0.983 |
| core dispersion index | 1.012 |

**Charged values.** The central value is Y = 2^-26.409: 78,489 real C32 cores, 627,912 paths, core-cluster
95% interval [-26.417, -26.402]. The conservative ledger uses 2^-26.428, the smallest of the four 95% lower ends
(real and synthetic prefixes, each with core and chunk clusters). The wide-set run estimates the same quantity with only
about 1 in 33 of its paths inside V, so it is a consistency check, not a charge input; its lower end is
2^-26.511. The per-candidate probability is 2^-43.994, that is,
43.99 effective conditions on real cores and 44.00 on synthetic prefixes.

**Independence.**
- The product of the stage means differs from the joint estimate by 0.0066 bit.
- Design effect 0.983, core dispersion index 1.012.
- The top 1% of cores carry 3.8% of the weight.
- The downstream rate does not depend on the stage-1 rate: -29.00, -29.00, -28.99 by stage-1 tercile.

**Exhaustive cross-check on real prefixes.** 78,489 real prefixes, with their true W0..W3, were each run
against all of V: 2^33.845 candidates in natural order.
- Conditional rates: E16 2^-3.000, E17 2^-10.990, A17 2^-1.002, E18 2^-6.014, E19 2^-6.931
  (2^-27.938 cumulative). W20 passed 7/60, then E20 2/7, then W22 0/2.
- The first three rates sum to 2^-14.993, against the cascade's stage-1 mean in the table above.
- At 2^-43.994 per candidate, no finished collision is expected at this scale.
- A random subsample of 3,768,651 candidates was rechecked by the exact checker, with 0 mismatches.

### 5.5 Why the real-core estimate applies to the attack

The real-core cascade takes (record, A−4..A−1) from real matcher accepts with CV = C32(IV, M0)
(78,489 of 78,489 pass L1 and L2 again; 0 CV mismatches). It redraws E−4..E−1, through
W0..W3. Two facts make this match the attack:
- Under the declared heuristic `uniform-cv-ewords`, the E-words of the chaining value are uniform and independent of the
  A-words and of the matched record.
- By Lemma Section 4.2(c), acceptance depends only on the A-words, so conditioning on acceptance leaves E−4..E−1 uniform.

The cascade draws them uniformly. The joint distribution of (core, E−4..E−1) is therefore the same as in the attack, and
so is the expected yield. Real C32 outputs could depart from this only through the E-words. The real-prefix funnel, with
true E-words, agrees with the cascade's stage 1 (2^-14.993 against 2^-15.004) and with the synthetic funnel
through E19 (2^-27.938 cumulative). The remaining ~16 conditions are measured only on resampled
E-words and rest on `uniform-cv-ewords`.

q is quoted at L2, and the yield is per L2 prefix, so the two levels match.

### 5.6 Condition count against the paper

The measured per-candidate probability corresponds to 43.99 conditions. The paper counts 45
conditions on (A16, E16..E20, W20, W22) (e1080:795-796) and needs 2^-27.415 per tuple (e1080:796-797).
- Our transcription of Figure 6 prints 44 independent conditions on these words. Two of them, the
  W20 pair, are not conditions of the characteristic; two necessary conditions are unprinted.
- Our independent derivation gives 44, equal to the measurement.

The paper's 45 most likely counts the duplicated W20 pair together with the A16 condition. That is an
inference; the details are in the Figure 6 reconciliation. The 1.01-bit gain in yield therefore comes from the condition
count, not from a different tail set.

### 5.7 Implementation note: a W14-grouping defect in the step-3 tool (disclosed)

The phase-1 step-3 tool, and the benchmark-only hunt program built on it (stream M), never assign the W14 group index
of the tail-set elements. As a result, the group of the first admissible W14 spans all of V, and the other 11 groups are
empty. Whenever the first W14 passes the prefilter, the tool evaluates all 196,608 elements of V; otherwise it evaluates
none. The evidence below shows exactly this zero-index behaviour, which is what the tool's cached path produces: it
zero-fills the tail-set array. Its uncached path allocates the
array without initialization, so the index is undefined there and the group-table write can go out of bounds. Any fixed
tool must assign the index explicitly.

The evidence is exact: on the real prefixes the tool evaluated 13,959,168 = 71 × 196,608 candidates.
Step 3 as specified in Section 5.2 would evaluate 15,630,336 = 954 × 16,384. The hunt's positive
control found 348/4000 and 333/4000 known collisions, a fraction 0.085 ≈ 1/12 = 0.083.

Effect on this proof:
- **q and the yield: none.** The cascade draws v uniformly from V, and the exhaustive funnel enumerates all of V.
- **The step-3 cost line.** The defective tool evaluates 196,608 × 1[first W14 passes] candidates, and the specified
  algorithm evaluates 16,384 × #(passing W14). Both have the same expectation, so the measured instructions per prefix
  estimate the specified cost without bias. Even if that line were 12 times larger (every passing W14 enumerating all of V), the
  conservative total would move by 4.3e-06 bit.
- **The witness search: not usable as built.** The hunt program, as built, would find only about 1/12 of the
  collisions. It was benchmarked for matching speed only, no number here depends on its tail, and it must be fixed
  before any witness search.

## 6. Success probability, declared heuristics and experiments

### 6.1 The online phase as a random experiment

The online phase (Sections 4 and 5) has a fixed budget of N = 2^43.761 first-block trials. Trials come in
chunks. Each chunk draws fresh random words for W0..W14 of M0 and enumerates W15 over the chunk's trial indices,
so all first blocks are distinct. For each trial the algorithm computes CV = C32(IV, M0). This is one charged target
compression; the 12-step midstate is not credited. It then looks CV up in TAB2. Each (M0, record) pair that passes the
exact L2 check is a prefix. For each prefix the tail enumerates the tail set V (2^17.585 values of (W14, W15)) and
tests the full 32-step trail. Each candidate that passes is rechecked as a two-block collision of the target with the
trusted digest function. The algorithm stops at the first verified collision.

The number of tail calls is capped at 2 times the expected 2^26.428, and the tail work is charged at that
cap (Section 7). The two output messages are distinct, since ΔM ≠ 0 gives M1 ≠ M1′ and hence M0 ‖ M1 ≠ M0 ‖ M1′.

### 6.2 Expected number of collisions

Let X be the number of verified collisions the budget would produce if the algorithm did not stop at the first one.
Let q be the expected number of prefixes per trial (counted with multiplicity: an M0 that matches two records gives two
prefixes) and y the expected number of collisions per prefix. By linearity of expectation, with no independence
assumption, E[X] = N · q · y. The only premise is that the measured q and y are the rates of the trials and prefixes
this algorithm generates (heuristics `q-real-c32` and `tail-yield`).

| Rates | log2 q | log2 y | log2 (N q y) | μ = E[X] | 1 − e^−μ |
| --- | ---: | ---: | ---: | ---: | ---: |
| charged (95% worst ends) | -17.333 | -26.428 | 0.000 | 1.0000 | 0.6321 |
| central (point estimates) | -17.324 | -26.409 | 0.029 | 1.0201 | 0.6394 |

The budget is N = 1/(q·y) at the charged rates. The charged rates are the lower ends of two-sided 95% intervals of the
measured rates (Sections 4 and 5). If the true product q·y were below the charged product, μ would be below 1 and the
success probability below the claimed value. The stress rows of Section 7 do not test this: they rescale the budget so that μ = 1 at the
paper's rates and report the resulting cost.

### 6.3 From μ to the success probability

**(a) Under independence across trials (heuristic `poisson-success`).** Let r_j be the probability that trial j yields
at least one collision. If trials are independent, P(X = 0) = Π_j (1 − r_j) ≤ exp(−Σ_j r_j). This holds for any values of
the r_j. So, conditional on the realised set of prefixes, variation of the yield from prefix to prefix cannot lower the
bound. Averaging over which TAB2 records the trials select adds only a Jensen term of relative order one over the number
of prefixes, which is negligible here. The step from Σ_j r_j to μ loses only the collisions that arrive in clusters
inside one trial: by Bonferroni, P(S ≥ 1) ≥ E[S] − E[S(S − 1)/2] for the number S of collisions of one trial. An
accepting M0 gives 1.0022 prefixes on average, so the clusters of a trial are essentially those of one prefix.

The one clustering mechanism of this tail is the W20 condition. W16, W18 and W20 depend only on the prefix and W14, and
V contains only 12 distinct W14 values. The 10 W20 condition bits (Section 2.4) are therefore shared by
all 2^14.00 elements of V with the same W14. Given a (prefix, W14) group that passes them, the expected
number of collisions among the group's W15 values is 2^-20.0, if the remaining conditions behave
independently across W15. Pairs inside one group therefore give E[S(S − 1)/2] / E[S] of about 2^-20.0
or less. Pairs in different groups add about E[S] = 2^-26.409. The resulting relative loss does not change
0.6321 at the precision shown. The claim uses
0.63, the exact value rounded down.

**(b) Without the Poisson shape.** By Cauchy–Schwarz, P(X ≥ 1) ≥ E[X]² / E[X²] = μ / (D + μ), where D = Var(X)/E[X]
is the dispersion of the collision count. At μ = 1.0000:
- The v5 minimum of 0.39 holds whenever D ≤ 1.56.
- Poisson counts (D = 1) give 0.50 by this bound. The exact Poisson value is 0.6321.

So the claimed 0.63 needs the Poisson heuristic. The v5 minimum needs only that collisions are not
over-dispersed by more than a factor 1.56.

**(c) Tail-call cap.** Under the same independence the number of prefixes exceeds the cap with probability at most
2^-49,479,628 (Chernoff bound), which is negligible.

**(d) Saving not taken.** Running only to the 0.39 point would save 1.02 bit of the matching term. The
total would fall by only 0.001 bit, because the trail term dominates. We do not take it.

### 6.4 Declared heuristics

v5 adjudicates declared premises under paired-lanes-v1 (v5:38). `claim.json` declares 8 premises
(5 score-critical, 3 supporting), each with scope, extrapolation, limitations and evidence. The
table is generated from that list. The blocks after it give, for each premise, the evidence in this proof.

`q-real-c32`, `tail-yield` and `uniform-cv-ewords` speak of a "uniformly random" M0. The algorithm draws M0 by the chunk
procedure of Section 6.1, and the premises are asserted, and were measured, for that distribution.

| ID | Role | Statement |
| --- | --- | --- |
| `q-real-c32` | score-critical | For a uniformly random first block M0, one trial (compute CV = C32(IV, M0), look up every TAB2 record whose key equals the CV word A-1, and run the exact two-branch check through step 13 plus the prefix-determined expansion conditions on W19, W21, W23 and W28) yields on average q = 2^-17.324 valid L2 prefixes. The ledger and the trial budget use the 95% worst end 2^-17.333. |
| `tail-yield` | score-critical | For a valid L2 prefix with chaining value CV = C32(IV, M0), trying the tail set of 2^17.585 pairs (W14, W15) yields on average 2^-26.409 second-block pairs (M1, M1') with C32(CV, M1) = C32(CV, M1'), M1 != M1'. The ledger uses 2^-26.428, the smallest of four 95% lower ends. |
| `uniform-cv-ewords` | score-critical | For uniformly random M0, the chaining-value words E-4..E-1 of C32(IV, M0) are uniform and independent of A-4..A-1 and of the matched TAB2 record. Hence resampling W0..W3 of a real prefix (keeping A-4..A-1 and E0..E3 and solving back for E-4..E-1) preserves the distribution that the tail yield depends on. |
| `poisson-success` | score-critical | The number of collisions output by the fixed-budget run (2^43.761 first-block trials, tail calls capped at 2 times the expected 2^26.428) is approximately Poisson with mean mu = 1.0000 at the charged rates, so the success probability is 1 - exp(-mu) = 0.6321, at least the claimed 0.63. |
| `trail-search-envelope` | score-critical | We assume that the authors' search for the 35-step characteristic, which the algorithm uses as hard-coded advice, used at most 14,976 thread-hours in total, for example at most 8 sequential solver calls of at most 72 h each on 26 threads (576 h of 26-thread solver time). The paper states no time. Priced at the ARMv8 SHA-256 hardware rate of 2^39.45 target compressions per thread-hour (2^53.324 units), plus the 2^38.828 units (56.01 CPU-hours at lambda = 1) of our own unsuccessful re-derivation, the charge is 2^53.324 units. |
| `start-point-cost` | supporting | The cost of finding the published start point (A1..A13, E5..E13, W9..W13) is at most the charged 2^41 units. The paper's 2^34.3 has no unit and is not used. |
| `instruction-pricing` | supporting | Each retired machine instruction of the logged programs costs at most lambda = 1 primitive operation of the v5 RAM, that is 1/2224 unit; hardware SHA-256 trials are instead charged one unit per compression. |
| `H-local-expansion-additions` | supporting | At the XOR differences of the published pair, each listed message-expansion addition has the exact XOR-differential probability stated in its experiment, and once the trail fixes one operand's signs the other operand needs exactly the listed sigma0/sigma1 two-bit sign relations (W4, W5, W6 equal to Figure 6) plus the stated W20/W22 value bits. |

**`q-real-c32` (score-critical).**
- *Evidence.* The pool of Section 4 is 91,629 L2 accepts in 2^33.807 real C32 trials from 3
  independent seeds, giving 2^-17.324 [-17.333, -17.315].
  - A fresh seed (303, 2^33 trials) through the batched matcher of Section 10 gave
    2^-17.332. That matcher reuses the same matching code, so this is a fresh sample, not independent code.
  - The exact analytic sum over TAB2 records under a uniform CV gives 2^-17.325.
  - The independent per-record estimator of the tail engine gives 2^-17.325.
  - The measured and per-record estimates used the same chunk structure (W0..W14 random per chunk, W15 enumerated)
    that the algorithm uses. The analytic sum assumes a uniform CV and was not measured.
- *Limitations.* The paper reports 2^-20.92 at 35 steps (e1080:786-787), 3.60 bits below our value. Section 2.6
  shows that the paper's own Figure 6 implies an upper bound consistent with our value. Stress row A of Section 7
  prices the paper's figure. Trials use a seeded PRNG (v5:37).

**`tail-yield` (score-critical).**
- *Evidence.* The estimate rests on 78,489 real C32 prefixes and 627,912 cascade paths, giving 2^-26.409. The
  chunk-cluster bootstrap over 4,906 clusters, with no cluster above a 0.0003 share, and the
  core-cluster interval agree. Three controls agree:
  - synthetic prefixes give 2^-26.419;
  - the wide tail set gives the same yield (Section 5);
  - a cascade without importance factors gives 2^-26.454 from 179 finished successes.

  Every success counted by the cascade was rechecked by exact execution. Samples were rechecked as 32-round compression
  collisions with the trusted verifier (Section 9).
- *Limitations.*
  - This is an importance-weighted splitting estimate, not a count of finished collisions per prefix.
  - The real-prefix estimate replaces W0..W3 of each prefix by uniform words (the resampling estimator of Section 5).
    It is therefore unbiased only under `uniform-cv-ewords`.
  - The exhaustive funnel over the real prefixes, with their true W0..W3, covers 2^33.84
    candidates. It agrees with the synthetic funnel through E19: -27.94 cumulative per candidate
    (60 passes) against -28.45 (6 passes). It reaches
    0 full collisions, as expected at that size. The yield beyond E19 for prefixes with their true
    W0..W3 is not measured directly.
  - Every success is a compression collision from a chaining value whose W0..W3 were resampled. None is a collision of
    the target (Section 12).

**`poisson-success` (score-critical)** is used in Section 6.3(a). Its evidence:
- Per-chunk counts of matcher accepts (2^20 trials per chunk) have variance/mean 0.997-1.000.
- Accepts per accepting M0 average 1.0022.
- On the tail side:
  - the dispersion index of per-prefix success weight is 1.012 for real prefixes and 1.008 for
    synthetic ones;
  - the design effect of core clustering is 0.983 (real) and 0.944 (synthetic);
  - the product of the 4 stage means differs from the joint rate by 0.0066 bit;
  - the downstream rate does not depend on the stage-1 rate: by stage-1 tercile (medians -16.42, -14.83, -14.09) the downstream
    rates are -29.003, -28.995, -28.986.
- The top 1% of prefixes carry 3.8% of the weight. This heterogeneity does not lower the bound of
  Section 6.3(a).

*Limitations.* These statistics measure the dispersion of matcher accepts and of per-prefix yield weights. They do not
measure the count of finished collisions, because no end-to-end collision exists. Dependence between prefixes from the
same chunk, or prefixes that share a TAB2 record, is bounded only empirically. The within-group step of Section 6.3(a)
assumes independence across W15 values.

**`uniform-cv-ewords` (score-critical).** The premise this proof needs is: for M0 drawn by the chunk procedure of
Section 6.1 and conditioned on an L2 accept with record r, the CV words E−4..E−1 are uniform and independent of r and of
the tail events. It is used twice:
1. To interpret q. The charged q is measured on real C32 outputs, so q itself does not rest on it.
2. In the resampling estimator of the tail yield. That estimator is exact only if the CV words E−4..E−1 are uniform and
   independent of the record and of the acceptance event. Beyond E19 the yield of prefixes with their true W0..W3 is
   not measured (Section 5), so through this use the charged yield rests on the premise. That is why it is
   score-critical.

*Evidence.* The measured, analytic uniform-CV and per-record values of q agree within 0.002 bit. The real and
synthetic tail funnels agree through E19, and the real and synthetic cascade yields agree (-26.409 against -26.419).

*Limitations.* The premise is not proved. Inside a chunk only W15 varies before the 32 rounds.

**`H-local-expansion-additions` (supporting)** is evidenced by the experiments of Section 6.5. q and the tail yield are
measured end to end and do not use it.

The last three premises concern cost, not probability:

**`trail-search-envelope` (score-critical; it sets 99.84% of the charged total).** The premise: the search
that produced the published 35-step characteristic (e1080:690-733) used at most 14976 thread-hours in total, for
example at most 8 sequential solver calls of at most 72 hours each on 26 threads
(576 hours of 26-thread solver time). Every thread-hour is priced at our ARMv8 hardware rate of
32-round compressions. This is an envelope assembled from checked facts. It is not a bound that anyone has
proved or published: neither paper states the search time, and the public code's descending loops can make many more
calls than the minimal sequence. Our own search found no characteristic (Section 7.4). The ledger labels this charge mode
`bound`; it is this envelope. Evidence, alternatives and limitations are in Section 7.4.

**`start-point-cost` (supporting).** The algorithm uses the published start point T as advice, and its derivation is
charged at the 2^41 cap (Section 7.5). The premise is that finding T costs at most that. Our independent
start-point search found T′ at a measured 2^33.938 units, and the 95% upper bound on its expected cost is
2^39.00 (Section 3.1). T′ failed gate G5, so this corroborates the cap but does not measure the cost
of finding T. The paper's 2^34.3 has no unit and is not used.

**`instruction-pricing` (supporting).** Each retired AArch64 instruction of logged code is charged as 1
primitive v5 operation. This is not a proof: a shifted-operand instruction, for example, is more than one RAM
operation. The claim is insensitive to it:
- at λ = 8 the conservative total is 53.328;
- the total reaches the claimed 53.38 only at λ = 348. That figure spends the declared slack, which
  is already committed to unrecorded work. With the slack kept, the claim holds up to λ = 23.2.

This is because the largest terms (the trail envelope, one unit per matching trial and the start-point cap) do not
scale with λ.

### 6.5 Experiments

`experiments/manifest.json` declares 11 `addition-xor-sampled-v1` entries; the file's SHA-256 begins
`2c86f5b41335f2c4`. Each entry is one 32-bit modular addition of the message expansion (W19-W24, W27-W29), at the
XOR differences of the published pair. Its hypothesis states the exact XOR-differential probability (the Lipmaa–Moriai
carry count, cross-checked by a carry DP). It also states the split of that probability into the sign relations, which
the trail fixes, and the value conditions.

We ran the organizer's runner with the public seed `hashsmash-public-seed-v1`:
- at the default budget (256 trials, α = 0.01, Hoeffding ε = 0.102; report SHA-256
  `b32524e4882ccd93`…);
- for information only, at 4096 trials (ε = 0.025).

Every interval contains its prediction. The intake pipeline accepted a scratch copy of the manifest with the same report.

| Experiment | Addition | Input/output XOR | exact log2 p | local run, organizer sampler (public seed, 256 trials) [interval] |
| --- | --- | --- | --- | --- |
| `r32-w20-w13-w4-pairing` | W20: (W13) + (W4) | 20000000, 20000000 → 00000000 | -1.00 | 130/256 [0.406, 0.610] |
| `r32-w20-s0w5-carry` | W20: (s1(W18) + W13 + W4) + (s0(W5)) | 00000000, 02808000 → 01808000 | -4.00 | 12/256 [0.000, 0.149] |
| `r32-w22-s1w20-s0w7-cancel` | W22: (s1(W20)) + (s0(W7)) | 500060d0, 5000a070 → 00000000 | -9.00 | 0/256 [0.000, 0.102] |
| `r32-w22-w6-carry` | W22: (s1(W20) + s0(W7) + W15) + (W6) | 00000000, 20000000 → 20000000 | -1.00 | 127/256 [0.394, 0.598] |
| `r32-w19-s0w4-cancel` | W19: (W12) + (s0(W4)) | 04400800, 04400800 → 00000000 | -3.00 | 33/256 [0.027, 0.231] |
| `r32-w21-s0w6-cancel` | W21: (W5) + (s0(W6)) | 04400800, 04400800 → 00000000 | -3.00 | 33/256 [0.027, 0.231] |
| `r32-w23-s0w8-cancel` | W23: (W7) + (s0(W8)) | 0101108a, 0301119a → 00000000 | -9.00 | 0/256 [0.000, 0.102] |
| `r32-w28-s0w13-cancel` | W28: (W12) + (s0(W13)) | 04400800, 04400800 → 00000000 | -3.00 | 27/256 [0.004, 0.207] |
| `r32-w27-s0w12-cancel` | W27: (W20) + (s0(W12)) | 01808000, 02808000 → 00000000 | -4.00 | 17/256 [0.000, 0.168] |
| `r32-w24-s1w22-cancel` | W24: (W8) + (s1(W22)) | 00080c00, 00081400 → 00000000 | -4.00 | 13/256 [0.000, 0.153] |
| `r32-w29-w22-w13-cancel` | W29: (W22) + (W13) | 20000000, 20000000 → 00000000 | -1.00 | 123/256 [0.379, 0.582] |

What they support:
- The derived σ0/σ1 sign relations equal Figure 6 for s0(W4), s0(W5), s0(W6), s0(W7), s0(W8), s1(W22).
- For s1(W20) they differ:
  - Figure 6 prints [4,6] xor 0, [22,31] xor 0, which the published pair violates (W20[4,6] xor 0, W20[22,31] xor 0);
  - the derivation has [17,26] xor 0 instead.

  These are the printed-relation errata of Section 2.8.
- W20 costs 3 value bits plus 7 sign relations, 10 in all. This equals the measured W20
  list fraction. W22 costs 1 more bit, so W20 and W22 together cost 11 bits.

Limitations:
- Events of probability 2^-9 receive only an upper bound at the default budget.
- The sampled operands are uniform and independent, which is not the attack's distribution.
- The per-addition probabilities are not multiplied into a trail probability anywhere in this proof.
- There is no `python-message-pairs-v1` entry, because no end-to-end witness exists (Section 10).

## 7. Time under collision-frontier-v5

### 7.1 Pricing rules

- **Units.** One selected-round (32-round) SHA-256 compression is 1 unit. Every other primitive word operation costs
  1/2224 (v5:9, v5:51). Parallel work is summed (v5:44). Failed, killed and timed-out runs are charged (v5:23).
- **Measured runs.** A logged run is charged as retired instructions × 1 / 2224. The instruction count covers
  all threads of the run's process (`instruction-pricing`). In the conservative ledger, runs flagged for possible
  undercounting are floored at their CPU-seconds × 1.08e+10 instructions per CPU-second, the phase-1 median.
- **Matching (analytic).** Each trial costs one unit plus the per-trial instructions of the matcher:
  - central ledger: 44.7 non-SHA instructions;
  - conservative ledger: all 86.6 instructions, which counts the SHA work twice.

  The 12-step midstate is not credited.
- **Tail (analytic).** 37430 instructions per prefix, charged at the cap of 2 times the expected number
  of prefixes.
- **Hardware SHA trials.** In the conservative ledger, every HW-engine compression of every logged measurement run
  (264,962,572,288 compressions, 2^37.95) is also charged 1 unit, on top of its instructions.
- **Advice derivations.** The trail search (P0) and the start point (A0) are charged in time, as v5:40 requires for
  advice.

Parameters of this package:

| Input | Mode | log2 units | Basis |
| --- | --- | ---: | --- |
| trail search (P0) | bound | 53.324 | bound: 14976 thread-hours at armv8 (ARMv8 SHA-256 hardware 32-step compressions per thread-second (strictest)), cite: e1080:696-733 (4 sequential minimisation steps, 2 calls each) x e349:1110-1113 (per-call solver time limit "e.g., 72 hours") x 26 solver threads per call (Peace9911/sha_2_attack @6a9f35f: every STP call); measured lower bound 2^38.83 |
| start point (A0) | cap | 41.000 | conservative cap 2^41; the paper's 2^34.3 (e1080:792-793) has no stated unit; charged at the cap because the independent start point failed G5; its measured search (2^33.94 units) is corroboration only |
| λ (operations per retired instruction) | parameter | 1 | v5 primitive word operations; C = 2224 |

### 7.2 Ledgers

Central ledger, using point values and the attack's phases only:

| Phase | Kind | log2 units | Basis |
| --- | --- | ---: | --- |
| P0-trail-search | analytic | 53.324 | bound: 14976 thread-hours at armv8 (ARMv8 SHA-256 hardware 32-step compressions per thread-second (strictest)), cite: e1080:696-733 (4 seque |
| A2-match-c32 | analytic | 43.733 | Step 2 (e1080:786-787); q=2^-17.3238 (accept-file line counts), prefixes 2^26.4089 (tail-g2.json) |
| A0-start-point-Tsat | analytic | 41.000 | conservative cap 2^41; the paper's 2^34.3 (e1080:792-793) has no stated unit; charged at the cap because the independent start point failed  |
| A2-match-lookup | analytic | 38.097 | tm-cost-probe runs 20261004T151631-dc30dd/20261004T151928-6901df |
| A3-tail-enum | analytic | 31.482 | tail-g2.json step3_cost |
| gt-fulltable-build | measured | 31.395 | one TAB2 build (larger of the two equivalent builders; tm-tab2-build not double-charged) |
| tail-setup | measured | 28.686 |  |
| gt-combos | measured | 27.108 |  |
| **total** |  | **53.326** |  |

Conservative ledger. This is the claim basis. It uses the 95% worst ends of q and y and the full per-trial
instructions. Its "all logged runs" row charges every run record: charged runs (R&D, debugging, failed searches),
legacy records and records marked no-charge (validation, rechecks, benchmarks and these renders). It leaves out only
the runs charged in P0 and the 6 no-charge slot-holder wrappers. A wrapper's CPU time is that of its member
runs, which are charged under their own records, so charging the wrapper as well would count them twice.

| Phase | Kind | log2 units | Basis |
| --- | --- | ---: | --- |
| P0-trail-search | analytic | 53.324 | bound: 14976 thread-hours at armv8 (ARMv8 SHA-256 hardware 32-step compressions per thread-second (strictest)), cite: e1080:696-733 (4 seque |
| A2-match-c32 | analytic | 43.761 | Step 2 (e1080:786-787); q=2^-17.3332 (accept-file line counts), prefixes 2^26.4282 (tail-g2.json) |
| A0-start-point-Tsat | analytic | 41.000 | conservative cap 2^41; the paper's 2^34.3 (e1080:792-793) has no stated unit; charged at the cap because the independent start point failed  |
| A2-match-lookup | analytic | 39.079 | tm-cost-probe runs 20261004T151631-dc30dd/20261004T151928-6901df |
| RD-hw-compressions | analytic | 37.947 | every logged HW-engine trial (tm match, bench, hunt) |
| A3-tail-enum | analytic | 31.501 | tail-g2.json step3_cost |
| all logged runs (95 phases, 357 runs) | measured | 37.202 | every run.sh and legacy record, instructions×λ/C (undercounts floored at the CPU rate) |
| **total** |  | **53.327** |  |

How the claim is derived from the ledger:

| Item | log2 units |
| --- | ---: |
| conservative ledger total | 53.3265 |
| declared slack (bits) | 0.05 |
| slack reason | work outside run.sh records not otherwise charged: compiles, editors and shell utilities during development, and the ledger instruction counters' process-tree coverage; deliberately larger than every itemised omission (T unrecorded runs are charged explicitly) |
| claimed time_log2 (rounded up to 0.01) | 53.38 |

The slack covers work that has no run record: compiles, editors, shell utilities, and the counter's process-tree
coverage. The 8 stream-T runs whose records were lost are not covered by the slack; they are charged
explicitly in P0.

The "all logged runs" row holds 357 records: 91 charged, 44 legacy and
222 no-charge. The no-charge records contribute 2^35.42 units of instructions. Their
HW-engine trials are also charged, by count, in the RD-hw-compressions row.

### 7.3 What dominates

The trail-search term P0 is 99.84% of the conservative total. Every other term together is
2^44.042. Without an envelope for the search we did not complete, the total would be
44.081: P0 charged at our measured work only, at λ = 1. Our measured CPU-hours priced at the
ARMv8 rate would give 45.777. Neither figure is claimed.

### 7.4 Trail search (P0): measured work plus an envelope

**What we ran (stream T, gate G4, and follow-up streams).** We re-implemented the e1080:690-733 search and ran it under
the harness, with exact value models. The search has four steps:
1. Minimise the weight of ∇W.
2. Minimise tE.
3. Minimise tA.
4. Minimise tE4.

Two units are used below. CPU-hours are CPU time. Thread-hours are wall time × thread cap, which is the unit of the time
box and of the envelope. Stream T had a time box of 48 thread-hours. It stopped when its scheduled heavy slots
ended, after 40.39 thread-hours (38.62 charged CPU-hours), without a characteristic. Follow-up streams
(T2-CUBE, T2-JOINT, T2-PORTFOLIO, T3) continued the search with 107 logged and 6 unrecorded charged runs, 17.39 CPU-hours (18.12 thread-hours)
up to the ledger snapshot, also without a characteristic.
Stream T3 ran public third-party SHA-2 trail tools locally (Sections 9.2.2 and 11). All of this work is charged in P0.
The results of each step and strategy are in Section 9.2.2; the charged work per strategy is:

| Strategy | Runs | CPU-hours | Instructions | Timed out / killed |
| --- | ---: | ---: | ---: | ---: |
| calibration on the published sparse part (not a search output) | 2 | 1.257 | 4.293e+13 | 2 |
| step1 nabla-W minimisation (exact value model, CaDiCaL; RC2 cross-check; enumeration) | 4 | 0.832 | 1.461e+13 | 0 |
| steps 2-4 exact two-branch model (tsearch st / probes) | 7 | 2.535 | 3.661e+13 | 4 |
| steps 2-4 signed-difference model / CEGAR with full exact oracle | 6 | 0.605 | 1.513e+13 | 6 |
| sparse-part enumeration (signed model, free optimal nabla-W) | 1 | 0.172 | 4.625e+12 | 0 |
| CEGAR with windowed exact oracle (L=5), rounds p1/p2/p2h | 35 | 12.532 | 2.127e+14 | 26 |
| nldtool (IAIK) guess-and-determine searches | 14 | 10.449 | 3.211e+14 | 0 |
| exact dense completion of our own sparse parts (xdense; bounded tA<=21, tE4<=76, and unbounded) | 27 | 2.676 | 3.521e+13 | 10 |
| sparse-part CEGAR (signed master, exact bounded oracle) | 2 | 1.592 | 2.039e+13 | 2 |
| hybrid master with all 15 windows exact (round p4) | 6 | 5.225 | 6.6e+13 | 5 |
| charged search runs (ledger) | 104 | 37.875 | 7.694e+14 |  |
| unrecorded runs (estimated, charged) | 8 | 0.747 | 4.179e+13 |  |
| follow-up stream T2-CUBE (trail-search) | 25 | 5.226 | 6.805e+13 | 14 |
| follow-up stream T2-JOINT (trail-search-joint) | 16 | 2.320 | 3.465e+13 | 11 |
| follow-up stream T2-PORTFOLIO (trail-search) | 14 | 3.894 | 6.394e+13 | 6 |
| follow-up stream T3 (t3-authors-baseline, t3-authors-improve-proto, autosha2-baseline, t3-improve-bench) | 52 | 2.373 | 2.934e+13 | 6 |
| follow-up stream T2-PORTFOLIO: unrecorded runs (estimated, charged) | 6 | 3.574 | 7.824e+13 | 6 |
| **measured total** |  | **56.009** | **1.085e+15** = 2^38.828 units |  |

All 211 logged runs (104 of stream T, 107 of the follow-up streams) are charged:
failed, killed and timed-out runs included. The 8 stream-T runs whose records were lost (0.747 hours
of single-thread wall time) are charged at the highest instructions per CPU-second of any stream-T run. The measured work
is 56.01 CPU-hours, which is 2^38.828 units at λ = 1. v5 charges failed work, so this
measured work is charged in full. It is a lower bound on what a successful search costs with our methods.

**The envelope.** Neither paper states the running time of the 35-step search. e1080:690-733 gives only the procedure,
and e1080:693 says it used the SAT/SMT tool of Li, Liu and Wang (ePrint 2024/349). We charge an envelope, not a bound.
It multiplies three facts, each checked against its source text when the package is generated:
- **Calls.** Steps 1-4 are 4 sequential minimisations (e1080:696-733). Each ends with a satisfiable
  call at its optimum and a failing call below it; Step 3 lowers tr "until no solution exists". So the procedure needs
  at least 8 sequential solver calls.
- **Hours per call.** The authors' earlier procedure gives "e.g., 72 hours" as the time limit of one solver
  call; when a call reaches it, the threshold is changed and the solver is called again. This is their 31-step SHA-512
  search (e349:1110-1113, Li–Liu–Wang EUROCRYPT 2024, Sect. 4.3, Step 2).
- **Threads per call.** Every STP call in the public Peace9911/sha_2_attack code (commit `6a9f35f`, all
  7 solver scripts) runs CryptoMiniSat with 26 threads. The repository's content and code tag
  match ePrint 2024/349; we have not confirmed its authorship (Section 11). 26 threads fit on the
  128-thread server of the paper's experiments (e1080:802). The paper does not name the machine of the
  trail search.

Option A is 8 calls × 72 hours × 26 threads = 14976 thread-hours: at most
8 sequential solver calls of at most 72 hours each on 26 threads, which is
576 hours of 26-thread solver time.

**What the public code does instead.** It does not run the minimal sequence:
- each objective is a descending loop that asserts weight = k (an equality) from 60 or 90 down to the optimum,
  with one fresh STP process per integer and nothing carried over between calls;
- its correct_dc step has its objective line commented out, so it repeats an identical call up to 61 times.

A search run this way can make many more than 8 calls. If it made N calls on 26 threads, the
envelope holds only if they averaged at most 576/N hours each. We could not time the authors' own solver
configuration: our STP build has no CryptoMiniSat back end (Section 9.2.2).

Option A is priced at our ARMv8 rate of 2^27.64 32-round compressions per thread-second, which is
2^39.45 units per thread-hour. Two properties of this rate:
- It is the highest per-thread full 32-round compression rate we measured. The best 12-thread measurement, 2^31.14/s at low load,
  is 2^27.56 per thread.
- It is 5.43 bits above the λ = 1 conversion (2^34.02 units per thread-hour). That is the same as
  charging every SAT-solver instruction as about 43 primitive operations.

The envelope part is 2^53.324. Adding the measured work (2^38.828) gives the P0 charge,
2^53.324 to three decimals.

The λ = 1 conversion of a cited thread-hour is fixed from phase-1 runs (1.08e+10 instructions per CPU-second). Our
own trail-search runs averaged 5.38e+09. Their 56.01 CPU-hours would therefore be 2^39.83
at that conversion, against the 2^38.828 actually counted.

| Option | Hours (envelope: thread-hours; measured: CPU-hours) | Conversion | Trail charge log2 (bound + measured) | conservative total log2 | Charged |
| --- | ---: | --- | ---: | ---: | --- |
| A (charged): 8 sequential calls x 72 h x 26 threads at armv8 | 14976 | armv8 | 53.324 | 53.327 | yes |
| B (not charged): 8 sequential calls x 72 h x 26 threads at lambda1 | 14976 | lambda1 | 47.894 | 47.991 | no |
| measured lower bound only (no envelope) | 56.01 | λ=1 instructions | 38.828 | 44.081 | no |
| measured CPU-hours at the ARMv8 conversion | 56.01 | armv8 | 45.261 | 45.777 | no |
| envelope and measured both at the ARMv8 rate | 14976 + 56.01 | armv8 | 53.330 | 53.332 | no |

We charge A, the largest row. The other rows are disclosed and not charged. In the table, "bound" means the envelope
part.

**What the envelope does not cover.** It is exceeded by more than 8 calls that run to the time limit, by
calls on more than 26 threads, by a longer time limit, or by more machines. Each doubling adds about one bit:

| Envelope multiple | Conservative total |
| ---: | ---: |
| 1 (charged) | 53.327 |
| 2 | 54.325 |
| 4 | 55.325 |
| 8 | 56.324 |

Multiple 2 would cover 16 sequential 72-hour calls on 26 threads, or
8 such calls on 52 threads; the claim would then be 54.38.

The claimed 53.38 covers an envelope at most 3.8% larger than option A. That margin spends the
declared slack, which is already committed to unrecorded work. With the slack kept, the margin is
0.2%.

Totals if the search took the given number of thread-hours, at each conversion:

| Conversion | log2 units per thread-hour | 24 th | 48 th | 240 th | 2400 th |
| --- | ---: | ---: | ---: | ---: | ---: |
| λ=1 instructions at the median 1.08e+10 instructions per CPU-second | 34.02 | 44.08 | 44.11 | 44.34 | 45.77 |
| portable scalar 32-step compressions per thread-second | 35.45 | 44.13 | 44.21 | 44.74 | 46.90 |
| ARMv8 SHA-256 hardware 32-step compressions per thread-second (strictest) | 39.45 | 45.04 | 45.62 | 47.50 | 50.70 |

### 7.5 Start point (A0): charged at the 2^41 cap

The attack uses the published start point T (Section 3), which is advice. The paper's Tsat of 2^34.3
(e1080:792-793) has no unit and is not used. We tried to replace it with a measured cost by finding a start point ourselves (stream B, Section 3.1.2).
The independent start point T′ failed gate G5 (Section 3.1.3). Because T′ has different q and yield, the cost of finding T′ does not measure the cost of finding T.
A0 is therefore charged at the conservative cap of 2^41 units. The measured search, 2^33.938 units,
is corroboration only.
The search runs, the expected-cost bound and the comparison of T′ with T are in Sections 3.1.2 and 3.1.3.

### 7.6 Stress and sensitivity

| Scenario | log2 T | Status |
| --- | ---: | --- |
| claim basis (conservative) | 53.327 | as charged |
| central point values | 53.326 | measured q and real-core yield; attack phases only |
| Tsat at the cited 2^34.3 read as compressions | 53.326 | not claimed (the paper states no unit) |
| Tsat at the 2^41 cap | 53.327 | cap |
| paper q 2^-20.92, measured yield | 53.348 | stress A, disclosed ceiling |
| paper q and paper yield 2^-27.415 | 53.371 | stress B; the paper itself gives 2^48.335 |
| midstate 20/32 credited | 53.326 | NOT taken (one full target compression per trial) |

- **Midstate credit.** Crediting the 12-step midstate (the midstate stress row) is not taken.
- **λ.** See `instruction-pricing` in Section 6.4.
- **q and yield at the paper's values.** Stress rows A and B rescale the budget so that μ = 1 at the paper's rates.
  They give 53.348 and 53.371.
  - Stress A is at or below the claimed 53.38; with the slack added it is 53.398,
    above the claim.
  - Stress B is at or below the claimed 53.38; with the slack added it is 53.421,
    above the claim.
- **Tail conditions at the paper's count.** With the paper's 45 tail conditions the yield is
  1 bit lower. The total is then 53.329, or 53.379 with the slack, at or below the
  claimed 53.38.

## 8. Memory, preprocessing and advice

The peak resident memory of any algorithm step we ran is 7,326,187,520 bytes (6.82 GiB), during the TAB2
build: `memory_log2_bytes` = 32.78.

This figure does not cover the trail search (P0). The memory of the authors' search is not measured: the paper's
experiments ran on a server with 378 GB (e1080:802), and the paper gives no memory for the search. Our own
trail-search runs peaked at 1,418,690,560 B. Memory is reported, not scored (v5:43).

| Phase | Run | Peak RSS (B) | log2 |
| --- | --- | ---: | ---: |
| gt-fulltable-build | 20261004T144241-bedf2d | 7,326,187,520 | 32.77 |
| gt-fulltable-build | 20261004T144132-139a51 | 7,320,371,200 | 32.77 |
| tm-g3-full-q | 20261004T145920-2bb844 | 5,356,797,952 | 32.32 |
| tm-g3-full-q | 20261004T150227-7242f7 | 5,356,355,584 | 32.32 |
| tail-setup | 20261004T150658-265082 | 341,245,952 | 28.35 |
| gt-combos | 20261004T143429-802b5c | 22,593,536 | 24.43 |

During matching the following are resident:
- the compact TAB2: 6 B per record, 3,655,378,944 B;
- its 512 MiB A−1 bitmap;
- the bucket offsets;
- code and the advice.

The matching runs peaked at 5,356,797,952 B. Other peaks:

| Run type | Peak RSS (B) |
| --- | ---: |
| batched matcher benchmarks | 4,641,603,584 |
| charged trail-search runs | 1,297,088,512 |
| start-point runs | 361,971,712 |

One no-charge validation run of the matcher in audit mode peaked at 7,771,881,472 B RSS (2^32.86). This is
`20261004T145749-459b64`, phase `tm-validate`, label "smoke: full table 2^28 trials, audit every chunk". Its physical footprint was 4,040,267,536 B. The audit
mode is not part of the algorithm. Counting the run would give 2^32.86. Memory is reported, not scored
(v5:43).

`preprocessing_log2` = 53.33 covers:
- the trail search (P0);
- the start point (A0);
- the (E5, E6, E7) combinations;
- the TAB2 build;
- the tail-set setup.

All of it is included in `time_log2`.

**Advice.** Nonuniform advice is 1004 B, so `nonuniform_advice_log2_bytes` = 9.98. It consists of:
- the realized trail: the XOR and sign words of its 104 A, E and W rows (Section 2);
- the 27 start-point words;
- the 16 words of ΔM.

The attack needs only part of this, and we count all of it. Its derivations are charged in time: the trail as P0
(Section 7.4) and the start point as A0 (Section 7.5). TAB2 and V are not advice; they are built by charged
preprocessing.

## 9. Evidence and reproduction

### 9.1 Independent rechecks

The rechecks below use the trusted verifier and a tracer written independently of the attack tools. They re-execute the Table 3 pair, the realized trail, the hardware engine and samples of the matcher accepts and tail successes reported in Sections 4 and 5. Run identifiers are given where each measurement is reported.

| Independent recheck (trusted verifier + fresh tracer) | Result |
| --- | --- |
| Table 3 at 35 rounds | True |
| C32 from CV35 collides | True |
| C32 from C32(IV,M0) collides (expected False) | False |
| trail rows vs own execution, mismatches | 0 |
| HW engine vs verifier | 0 mismatches / 20,000 |
| tail successes succ_real | 600/600 compression collisions, 600 follow trail |
| tail successes succ_syn | 600/600 compression collisions, 600 follow trail |
| matcher accepts full_s9.jsonl | 600/600 CV ok, L2 600 |
| matcher accepts full_s3_accepts.jsonl | 600/600 CV ok, L2 600 |
| matcher accepts g1_base_s9.jsonl | 84/84 CV ok, L2 84 |

### 9.2 The differential-trail search (P0): re-derivation record

#### 9.2.1 What the paper did

The authors found the 35-step characteristic with the SAT/SMT tool of their earlier work [Li, Liu, Wang, EUROCRYPT
2024, ePrint 2024/349] (e1080:690-694), in four steps (e1080:696-733):
1. minimize Σ H(∇W_i) with differences only in W4..W8, W12, W13, W20 and W22;
2. with that ∇W fixed and the difference windows δA_i = 0 outside 4..14 and δE_i = 0 outside 4..18, minimize
   tE = Σ_{14..18} H(∇E_i);
3. lower a threshold tA on Σ H(∇A_i) until the model becomes UNSAT;
4. minimize tE4 = Σ_{4..18} H(∇E_i).

The published characteristic has (tw, tE, tA, tE4) = (22, 6, 21, 76). **The paper states
no running time for this search.** The earlier paper's procedure uses a per-threshold solver limit of "e.g.,
72 hours" before the threshold is changed (ePrint 2024/349, e349:1110-1113). Every solver call of the public
sha_2_attack code runs on 26 threads, and the server of the paper's experiments has 128 threads
(e1080:802). Section 7.4 builds the charged envelope from these facts.

#### 9.2.2 Our re-derivation (stream T and follow-up streams)

**Stream T.** We re-derived the search with our own models and solvers in a 48 thread-hour box:
- exact two-branch value models in CNF (CaDiCaL 1.9.5 through pysat, with an RC2 MaxSAT cross-check);
- a signed-difference relaxation with counterexample-guided refinement against an exact oracle, over full and windowed
  oracles;
- nldtool guess-and-determine searches (IAIK, MIT licence);
- exact dense completion of our own sparse parts.

Results:

- **Step 1 is solved exactly.** The minimum is tw = 22, equal to the published weight. Bounds 9..21 were proved
  UNSAT in 1018.1 s (run 20261004T163210-683089); RC2 confirmed the minimum (run 20261004T163640-369933). 512 optimal ∇W patterns
  were enumerated. The cap was hit, so the enumeration is incomplete. Every enumerated pattern is realized by a message
  pair. The published signed pattern is not among them, although 61 of them share its XOR support.
- **Steps 2-4 produced no valid characteristic.** None was found with (tE, tA, tE4) lexicographically ≤ the published
  values:
  - With the published ∇W, the signed relaxation reaches (6, 19, 69), below the published values, but all 27 such
    candidates are contradictory under the exact model.
  - 28 refinement members ran 340,856 iterations without a locally valid candidate.
  - Of our own sparse parts, 17 were proved to have no valid dense completion within tA ≤ 21,
    tE4 ≤ 76. 10 completion runs timed out, and 0 succeeded.
  - 14 nldtool searches (plus 1 calibration run) stopped at their own internal time limit
    (exit status 1 after 1,676-2,857 CPU-seconds) without a characteristic. The last column of the strategy table (Section 7.4)
    counts only harness timeouts and kills, so it shows 0 for them.
- **Calibration.** Given the *published* sparse part, neither calibration run finished within its limit (2 of
  2 runs, 1.26 CPU-hours, charged). One run was our dense completion and the other was nldtool. So
  there is no sign that our tools are faster than the authors'.

| Quantity | Value |
| --- | --- |
| minimum ∇W weight (Step 1) | 22 |
| bounds proved UNSAT | 9..21 |
| UNSAT proof time (s), run | 1018.1, 20261004T163210-683089 |
| optimal patterns enumerated (capped) | 512 |
| published (tw, tE, tA, tE4) | (22, 6, 21, 76) |
| valid characteristics found | 0 |
| status | not_found |

**Gate G4.** Stream T was frozen with status `not_found` after 40.39 thread-hours (wall time × thread cap) of its
48 thread-hour box: 38.62 charged CPU-hours, including the estimated unrecorded runs. G4 was declared failed at that point because no strategy
had produced a valid characteristic. The box was not exhausted, and the search continued afterwards in follow-up streams.
Every search run is charged, including failed, killed and timed-out runs.
- 8 runs lost their ledger record when a process kill also matched the harness runner. They are charged
  at their wall time × the highest instruction rate observed in any stream-T run (1.55e+10 instructions per
  CPU-second): 0.747 hours of single-thread wall time.
- 12 short model tests on the published pair are uncharged development runs. They are included in the
  conservative ledger's all-runs line.

**Follow-up streams.** After the freeze, streams T2-CUBE, T2-JOINT, T2-PORTFOLIO, T3 continued the search. Their 107 logged and 6 unrecorded runs
(17.39 CPU-hours) up to the ledger snapshot are added to the measured part. None of them had reported a valid
characteristic by then, so the package still charges the envelope.

**Disclosure: third-party trail-search code (stream T3).** Stream T3 ran public third-party code, not only our own
models (Section 11 gives the sources):
- Peace9911/sha_2_attack (commit `6a9f35f`, no licence; its content and code tag match ePrint 2024/349, authorship not
  confirmed). It ships no 35-step configuration, so we rebuilt one from e1080:690-733 with an adapted copy of its 31-step
  model class. We solved it with STP 2.4.1, whose local build has only the MiniSat back end, and on the same clauses with
  CaDiCaL.
- AutoSHA2Collision (Zhang, Li, Gao and Wang; commit `21d1b077`, no licence): its model generator with STP 2.4.1
  (MiniSat), and a locally modified copy of its model library under our own CaDiCaL driver (our changes are listed in
  Section 11).

Their 52 runs (2.37 CPU-hours) up to the snapshot are charged in the measured part. No other number in
this proof depends on them, and no code from either repository, modified or not, is part of the package.

**Snapshot.** Every trail-search number in Sections 7.4 and 9.2 is summed from the run ledger at snapshot `ce6b5c15c96e5e08` (574 records, last run
20261004T230726-122e7a), plus 6 follow-up runs whose ledger record was lost, estimated and charged at their stream's highest instructions per CPU-second. Measured search attempts are charged up to this snapshot; attempts after it are not
included. At the measured rates (the highest rate in the ledger, 3.24e+10 instructions per CPU-second, at λ = 1)
they change the total by less than 0.001 bit unless they exceed 149 CPU-hours, about 8 hours
with all 18 cores of the host busy. The claimed bound is unaffected at its stated precision: moving the rounded
claim would take more than 520 further CPU-hours.
- Further runs that find no characteristic only add to the measured part, within the bound just stated.
- A characteristic they find does not by itself replace the envelope. The algorithm hard-codes the published
  characteristic, and by the reasoning that keeps T′ from replacing T (Section 3.1.3), the cost of finding a different
  characteristic does not measure the cost of finding this one. The measured work would replace the envelope only if the
  found 32-step characteristic is identical to the published one, or if the attack switched to it and its TAB2, q and
  yield were measured again. In the first case the conservative total would fall to about 2^44.081,
  9.2 bits below the current 2^53.327; in the second it would have to be recomputed.

The charged work per strategy is tabulated in Section 7.4.

## 10. Certificates

`certificates/manifest.json` lists 0 certificates. No certificate exists for any of the following reasons:
- No end-to-end 32-round two-block collision has been produced. The witness hunt was not run.
- The published Table 3 pair is a 35-step collision (Section 1.2). Its second blocks collide under C32 from
  CV35 = C35(IV, M0), but not from C32(IV, M0). Its 32-round two-block digests differ; the recheck of Section 9 finds
  exactly this.
- The tail successes of Section 5, and the positive controls below, are 32-round compression collisions from chaining
  values whose W0..W3 had been resampled. No first block is known that produces those chaining values. They are not
  collisions of the target and cannot be certificates (Section 12).

The hunt program that would produce a certificate is built and validated:
- **Matcher.** Its accepts on 2^28 trials are byte-identical to the reference matcher's.
- **Inline tail.** It reproduces the tail engine's candidate counts.
- **Positive controls.** On G2 cascade successes it recovered 348/4000 and 333/4000
  full 32-step compression collisions from resampled CVs, not target collisions. The trusted verifier confirmed
  681/681 of them as compression collisions.
- **Negative control.** With one CV bit flipped, 4000/4000 prefixes fail.

Benchmark (all runs no-charge):

| Quantity (hunt.c benchmark; witness hunt not run) | Value |
| --- | ---: |
| log2 trials/s, stage1_sha_only | 30.64 |
| log2 trials/s, stage2_bitmap | 30.49 |
| log2 trials/s, stage3_bucket | 29.66 |
| log2 trials/s, stage9_full_matcher | 29.70 |
| log2 trials/s, stage9_full_matcher_tail_on | 29.75 |
| log2 expected trials per witness | 43.732 |
| P=0.63: log2 trials, wall hours (12 threads) | 43.732, 4.65 |
| P=0.90: log2 trials, wall hours (12 threads) | 44.935, 10.71 |

At that rate, a witness is a matter of hours on one machine. A found pair would be certified with the organizer's
two-block digest check and a `python-message-pairs-v1` experiment. That would also measure q·y directly.

## 11. Prior work and credit

- **Yingxin Li, Fukang Liu, Gaoli Wang and Jiali Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework
  for SHA-2", IACR ePrint 2026/1080.**
  - We use their 35-step characteristic, truncated to 32 steps (Figure 6 and the realized trail of Table 3), and their
    start point T.
  - We use their three-step attack: TAB2 construction (Step 1, e1080:748-781), first-block matching (Step 2) and the
    (W14, W15) tail over V (Step 3).
  - We re-implemented and ran their trail-search procedure (e1080:690-733). It did not find a characteristic
    (Section 7.4).
  - Every rate in our cost is measured by us at 32 rounds, except the cited trail envelope (Section 7.4).
    Their Table 3 pair is used only as a test vector.
- **Yingxin Li, Fukang Liu and Gaoli Wang, "New Records in Collision Attacks on SHA-2", EUROCRYPT 2024, LNCS 14651,
  pp. 158-186 (ePrint 2024/349).** This is the SAT/SMT trail-search tool and procedure that ePrint 2026/1080 uses. Our
  trail envelope cites its per-call solver time limit (e349:1110-1113).
- **Yingxin Li, Fukang Liu, Gaoli Wang, Xiaoyang Dong and Siwei Sun, "The First Practical Collision for 31-Step SHA-256",
  ASIACRYPT 2024, LNCS 15490, pp. 237-266.** This is the memory-efficient collision framework that ePrint 2026/1080
  extends. It is background and is not used directly.
- **Florian Mendel, Tomislav Nad and Martin Schläffer** (ASIACRYPT 2011, LNCS 7073, pp. 288-307; EUROCRYPT 2013,
  LNCS 7881, pp. 262-278), and **Christophe De Cannière and Christian Rechberger** (ASIACRYPT 2006, LNCS 4284,
  pp. 1-20). They developed the automated search for SHA-2 characteristics and the generalized-condition notation (u, n,
  -) used in Section 2.
- **nldtool (IAIK, Graz University of Technology; MIT licence; Mendel, Schläffer, Eichlseder, Dobraunig, Nad,
  Rechberger).** We used it at commit `641f9bb`:
  - in the exact checker, for condition propagation, as a filter only (ground truth is exact two-branch execution);
  - in the trail search, for the guess-and-determine runs listed in Section 7.4, all charged.
- **Z. Zhang, M. Li, L. Gao and M. Wang, "Collision Attacks on SHA-256 up to 37 Steps with Improved Trail Search",
  EUROCRYPT 2026, Part VI, LNCS, pp. 91-120** (reference [25] of ePrint 2026/1080). AutoSHA2Collision is the tool of
  this paper.
- **Peace9911/sha_2_attack** (GitHub, commit `6a9f35fd`; no licence). Its content and code tag match ePrint 2024/349; we
  have not confirmed its authorship. It ships configurations of its `find_dc` STP models for other step counts but no
  35-step one. Stream T3 rebuilt a 35-step configuration from e1080:690-733 (its unchanged unit functions, driven by an
  adapted copy of its 31-step model class), ran it with STP 2.4.1 (MiniSat back end; the local build has no
  CryptoMiniSat) and, on the same clauses, with CaDiCaL, and ran its `verify_result` checker. The `find_dc` models
  and the descending minimisation procedure are the authors'; our changes were the rebuilt 35-step configuration and
  the CaDiCaL runs. Its solver settings are facts of the envelope (Section 7.4). This work is charged in P0.
- **AutoSHA2Collision** (Zhang-SDU/AutoSHA2Collision, commit `21d1b077`; no licence), by Z. Zhang, M. Li, L. Gao and
  M. Wang. The tool and its idea are theirs: the bit-level SAT/SMT models of signed differences for SHA-2 steps and
  message expansion, the exact value model that checks both branches, the staged minimisation of the characteristic's
  weight and the jump of the threshold to just below each weight found. Stream T3 ran its model generator unmodified
  with STP 2.4.1 (MiniSat back end), and a locally modified copy for measurement. Our changes, with the model
  semantics unchanged:
  - three small fixes to the model library: constant-time duplicate-declaration checks, a missing declaration for one
    operation type, and a corrected variable-name declaration;
  - direct CNF output instead of CVC text through STP;
  - one incremental CaDiCaL 1.9.5 solver per run, with the weight bounds as totalizers and the thresholds (including the
    authors' jump) as assumptions, so learnt clauses survive between thresholds;
  - the staged objectives of ePrint 2026/1080 Steps 2-4 solved in that same solver;
  - exactness added lazily: after each solution, the authors' exact value model is added only for the steps that
    fail it, and the same bound is solved again;
  - seeded variable permutation and clause shuffling for portfolio diversity.

  Charged in P0. No result of these runs is used.
- Both repositories were run locally only, unmodified and in our modified copies. Neither carries a licence, and the
  package includes none of their code, modified or not.
- **STP** (Vijay Ganesh, David L. Dill and contributors; MIT licence), the SMT solver both tools use. Stream T3 ran it,
  charged in P0.
- **CaDiCaL 1.9.5** (Armin Biere et al., MIT licence) through **PySAT** (Alexey Ignatiev, Antonio Morgado and Joao
  Marques-Silva; MIT licence), including its RC2 MaxSAT solver. Used in the start-point search and the trail search.
- **Helger Lipmaa and Shiho Moriai** (FSE 2001, LNCS 2355, pp. 336-350): the exact XOR-differential probability of
  addition, used in the experiment hypotheses.
- **HashSmash organizer code.** `verifier/hash_functions.py` is the trusted reference for every equality we claim. The
  organizer's experiment runner produced the reports of Section 6.5.
- **HashSmash PR #166.** We treated its content as untrusted hints and used some of them:
  - Its TAB2 record and key counts were an early acceptance criterion of our planning. Our table gate replaced that
    criterion after it showed that those records include ones that exact two-branch execution always rejects. Its
    593,920-record table equals our base slice without one Boolean relation.
  - Its judge dossier served as a checklist for this package.
  - Its published numbers (counts, funnel, uniform-CV q and per-prefix survivor counts) served as comparisons, and its
    survivor counts informed a planning margin.
  - We never executed its code and did not copy its Figure 6 corrections. Our Figure 6 transcription and condition
    counts are independent (Section 2.5).
- **Attribution.** Model: Claude Opus 5.5. Harness: Claude Code.

## 12. Limitations

- **The trail search is charged by an envelope, not a measurement or a bound.** It is 99.84% of the claim.
  - Stream T used 40.39 of its 48 box thread-hours (38.62 CPU-hours) without a characteristic
    (G4). Follow-up streams (107 logged and 6 unrecorded runs, 17.39 CPU-hours) have not found one either.
  - Neither paper states the authors' search time.
  - The envelope allows 14976 thread-hours: at most 8 sequential calls of at most 72
    hours on 26 threads. The public code's descending one-call-per-integer loops (from 60 or 90) and its
    repeated correct_dc call can make many more calls; N such calls fit only if they averaged at most 576/N
    hours. The envelope is priced at the strictest conversion we measured.
  - A search that needed more than 3.8% more would exceed the claim, or more than
    0.2% more with the slack kept. Envelope multiple 2 gives a claim of 54.38;
    each doubling adds about one bit (Section 7.4).
- **No end-to-end witness; F8.**
  - The tail measurements of Section 5 and the hunt's positive controls produced 32-round compression collisions from
    chaining values whose W0..W3 (hence E−4..E−1) had been resampled. These chaining values are not known to be outputs
    of C32(IV, ·), so these pairs are not two-block collisions from the IV. They are not collisions of the target and
    are not claimed as such.
  - The published Table 3 pair is a 35-step collision, not a collision of the 32-round target.
  - The success probability therefore rests on the declared heuristics of Section 6.4, not on an observed target
    collision.
- **q against the paper.** Our q is 3.60 bits above the paper's 35-step 2^-20.92. Figure 6 explains the gap
  in our favour (Section 2.6). If the paper's q held, the total would be 53.348 (53.398 with the
  slack, above the claimed 53.38). With the paper's yield as well it would be 53.371
  (53.421 with the slack, above the claim).
- **Tail conditions.** We derive 44 tail conditions and measure 43.99, where the paper
  states 45 (Section 2.7). The paper's count would lower our yield by 1 bit. The total
  would then be 53.329, or 53.379 with the slack, at or below the claimed 53.38.
- **Start point.** Tsat is charged at the 2^41 cap, because the paper's figure has no unit and our
  independent T′ failed G5. T′'s measured search (2^33.938 units) is corroboration only (Section 7.5).
- **Heuristics.** Poisson behaviour, uniform CV words and independence across W15 values within a chunk are supported
  by dispersion and agreement statistics, not proved. The v5 minimum survives over-dispersion up to D = 1.56
  (Section 6.3(b)). Trials use a seeded PRNG, which is reproducibility evidence and not ideal coins (v5:37).
- **λ = 1** is a pricing premise, not a compilation to the RAM. The claim holds up to λ = 348 by
  spending the slack, and up to λ = 23.2 with the slack kept.
- **Ledger hygiene.**
  - 8 trail-search runs lost their records and are charged by estimate.
  - One matcher seed kept only a metric line and is not pooled into q.
  - 44 records written by an earlier engine logger are charged in the conservative ledger only.
  - Unrecorded tooling is covered only by the declared slack.
  - The conservative "all logged runs" row includes the no-charge records, which makes it larger, not smaller.
- **Negative controls are weak (F7).**
  - The recheck's controls are single-bit flips (512 in both messages, 512 in M1′ only and
    256 in the CV), with 0 passes. A single-bit flip breaks the trail trivially.
  - Mutant-trail controls (one flipped signed row) and near-miss controls (L1-valid prefixes with random (W14, W15)) were
    not run.
  - The hunt's CV-flip control is of the same kind.
- **Memory.** The audit-mode validation run peaked above the claimed memory (Section 8). The memory of the authors'
  trail search is not measured and not covered by `memory_log2_bytes`; their experiment server has 378 GB, and
  our own trail-search runs peaked at 1,418,690,560 B (Section 8).
- **Machine.** All rates are measured on one Apple M5 Max under shared load. Instruction counts are unaffected; the
  ARMv8 rate is a measured rate, not a bound on all hardware.
